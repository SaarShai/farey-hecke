#!/usr/bin/env python3
"""Falsifiable probes for audit ordering and interruptible risk scenarios.

This is research software.  It tests finite-population prefix behavior; it does
not establish clinical utility, regulatory compliance, labor savings, or a
production risk-management benefit.
"""

from __future__ import annotations

import argparse
import bisect
from collections import defaultdict
from dataclasses import dataclass
import hashlib
import io
import json
import math
from pathlib import Path
import random
import statistics
import sys
import tempfile
import urllib.request
import zipfile


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_ROOT = PROJECT_ROOT / "src"
for import_root in (PROJECT_ROOT, SRC_ROOT):
    if str(import_root) not in sys.path:
        sys.path.insert(0, str(import_root))

import economic_validation as economic
import real_data_ml_simulation as audit_base
from coprimebatch.applications import application_preset
from coprimebatch.prefix_balance import verify_quota_result


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    url: str
    doi: str
    sha256: str
    member: str
    parser: str


DATASETS = (
    DatasetSpec(
        name="banknote-authentication",
        url="https://archive.ics.uci.edu/static/public/267/banknote+authentication.zip",
        doi="https://doi.org/10.24432/C55P57",
        sha256="1e2acd9a2085fadf3d8145c12d3d22af853320d52294a6590c2eaf75fdc05227",
        member="data_banknote_authentication.txt",
        parser="label-last",
    ),
    DatasetSpec(
        name="spambase",
        url="https://archive.ics.uci.edu/static/public/94/spambase.zip",
        doi="https://doi.org/10.24432/C53G6X",
        sha256="813ac1df8effac70463c09c9c4b11e8803eefcab54771af66150852bcdcd1636",
        member="spambase.data",
        parser="label-last",
    ),
    DatasetSpec(
        name="breast-cancer-wisconsin-diagnostic",
        url="https://archive.ics.uci.edu/static/public/17/breast+cancer+wisconsin+diagnostic.zip",
        doi="https://doi.org/10.24432/C5DW2B",
        sha256="bc154869ef13f753f9e2b5a17e248cfe1ba4b6721db7c4da9f4880e40b05d3af",
        member="wdbc.data",
        parser="wdbc",
    ),
)

RISK_SOURCE = "https://www.bis.org/bcbs/publ/d457_note.pdf"
AUDIT_SPLIT_SEED = 20260801
NULL_SEED_OFFSET = 90_000


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def obtain_dataset(spec: DatasetSpec, cache_dir: Path, *, offline: bool) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    target = cache_dir / f"{spec.name}.zip"
    if target.exists() and sha256_path(target) == spec.sha256:
        return target
    if target.exists():
        raise ValueError(f"cached {spec.name} archive has the wrong SHA-256")
    if offline:
        raise FileNotFoundError(f"offline cache missing for {spec.name}: {target}")
    with urllib.request.urlopen(spec.url, timeout=60) as response:
        payload = response.read()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != spec.sha256:
        raise ValueError(
            f"downloaded {spec.name} SHA-256 {actual} != pinned {spec.sha256}"
        )
    with tempfile.NamedTemporaryFile(dir=cache_dir, delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(payload)
    temporary.replace(target)
    return target


def parse_dataset(
    path: Path, spec: DatasetSpec
) -> tuple[list[tuple[float, ...]], list[str]]:
    if sha256_path(path) != spec.sha256:
        raise ValueError(f"{spec.name} archive does not match its pinned SHA-256")
    with zipfile.ZipFile(path) as archive:
        raw = archive.read(spec.member).decode("utf-8").strip().splitlines()
    features: list[tuple[float, ...]] = []
    labels: list[str] = []
    for line in raw:
        fields = line.strip().split(",")
        if not fields or not fields[0]:
            continue
        if spec.parser == "wdbc":
            labels.append(fields[1])
            features.append(tuple(float(value) for value in fields[2:]))
        elif spec.parser == "label-last":
            labels.append(fields[-1])
            features.append(tuple(float(value) for value in fields[:-1]))
        else:
            raise ValueError(f"unknown dataset parser {spec.parser!r}")
    if not features or len(features) != len(labels):
        raise ValueError(f"{spec.name} did not yield aligned feature and label rows")
    dimensions = {len(row) for row in features}
    if dimensions != {len(features[0])} or len(set(labels)) < 2:
        raise ValueError(f"{spec.name} has an invalid rectangular classification table")
    return features, labels


def _stable_label_seed(label: str, seed: int) -> int:
    payload = f"{seed}:{label}".encode()
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def stratified_split(
    features: list[tuple[float, ...]],
    labels: list[str],
    *,
    train_fraction: float = 0.65,
    seed: int = AUDIT_SPLIT_SEED,
) -> tuple[
    list[tuple[float, ...]],
    list[str],
    list[tuple[float, ...]],
    list[str],
]:
    if not 0 < train_fraction < 1:
        raise ValueError("train_fraction must be strictly between zero and one")
    by_label: dict[str, list[int]] = defaultdict(list)
    for index, label in enumerate(labels):
        by_label[label].append(index)
    train_indices: list[int] = []
    test_indices: list[int] = []
    for label, indices in sorted(by_label.items()):
        random.Random(_stable_label_seed(label, seed)).shuffle(indices)
        cut = min(max(round(len(indices) * train_fraction), 1), len(indices) - 1)
        train_indices.extend(indices[:cut])
        test_indices.extend(indices[cut:])
    train_indices.sort()
    test_indices.sort()
    if set(train_indices) & set(test_indices):
        raise AssertionError("train and test indices overlap")
    return (
        [features[index] for index in train_indices],
        [labels[index] for index in train_indices],
        [features[index] for index in test_indices],
        [labels[index] for index in test_indices],
    )


@dataclass(frozen=True)
class CentroidModel:
    labels: tuple[str, ...]
    means: tuple[float, ...]
    scales: tuple[float, ...]
    centroids: tuple[tuple[float, ...], ...]


def train_centroid_model(
    features: list[tuple[float, ...]], labels: list[str]
) -> CentroidModel:
    dimensions = len(features[0])
    means = tuple(statistics.fmean(row[index] for row in features) for index in range(dimensions))
    scales = tuple(
        max(
            math.sqrt(
                statistics.fmean(
                    (row[index] - means[index]) ** 2 for row in features
                )
            ),
            1e-12,
        )
        for index in range(dimensions)
    )
    standardized = [
        tuple(
            (value - means[index]) / scales[index]
            for index, value in enumerate(row)
        )
        for row in features
    ]
    class_labels = tuple(sorted(set(labels)))
    centroids = tuple(
        tuple(
            statistics.fmean(
                row[index]
                for row, observed in zip(standardized, labels, strict=True)
                if observed == label
            )
            for index in range(dimensions)
        )
        for label in class_labels
    )
    return CentroidModel(class_labels, means, scales, centroids)


def predict_with_margin(
    model: CentroidModel, features: list[tuple[float, ...]]
) -> tuple[list[str], list[float]]:
    predictions: list[str] = []
    margins: list[float] = []
    for row in features:
        standardized = tuple(
            (value - model.means[index]) / model.scales[index]
            for index, value in enumerate(row)
        )
        distances = [
            sum(
                (value - center) ** 2
                for value, center in zip(standardized, centroid, strict=True)
            )
            for centroid in model.centroids
        ]
        ranking = sorted(range(len(distances)), key=distances.__getitem__)
        best, second = ranking[:2]
        predictions.append(model.labels[best])
        margins.append(
            (distances[second] - distances[best]) / max(distances[second], 1e-12)
        )
    return predictions, margins


def quantile_thresholds(values: list[float], bins: int) -> tuple[float, ...]:
    if bins < 1 or not values:
        raise ValueError("quantile bins and values must be nonempty")
    if bins == 1:
        return ()
    ordered = sorted(values)
    thresholds: list[float] = []
    for step in range(1, bins):
        position = (len(ordered) - 1) * step / bins
        lower = int(position)
        upper = min(lower + 1, len(ordered) - 1)
        thresholds.append(
            ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)
        )
    return tuple(thresholds)


def audit_strata(
    train_predictions: list[str],
    train_margins: list[float],
    predictions: list[str],
    margins: list[float],
    *,
    bins: int,
) -> list[str]:
    thresholds = {
        label: quantile_thresholds(
            [
                margin
                for prediction, margin in zip(
                    train_predictions, train_margins, strict=True
                )
                if prediction == label
            ],
            bins,
        )
        for label in sorted(set(train_predictions))
    }
    return [
        f"predicted-{prediction}:margin-{bisect.bisect_right(thresholds[prediction], margin)}"
        for prediction, margin in zip(predictions, margins, strict=True)
    ]


def paired_summary(tool: list[float], random_values: list[float], *, seed: int) -> dict[str, object]:
    tool_mean = statistics.fmean(tool)
    random_mean = statistics.fmean(random_values)
    interval = audit_base.bootstrap_reduction_interval(
        tool, random_values, replicates=3000, seed=seed
    )
    return {
        "tool_mean": tool_mean,
        "random_mean": random_mean,
        "relative_reduction": 1.0 - tool_mean / random_mean,
        "bootstrap_95_interval": list(interval),
        "paired_win_rate": sum(
            a < b for a, b in zip(tool, random_values, strict=True)
        )
        / len(tool),
    }


def _integrated_absolute_error(outcomes: list[int], order: list[int], warmup: int) -> float:
    errors = audit_base.prefix_errors(outcomes, order)
    return float(audit_base.integrated_metrics(errors, warmup)["mean_absolute_error"])


def _stratum_accuracy_range(outcomes: list[int], strata: list[str]) -> tuple[float, float]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for outcome, stratum in zip(outcomes, strata, strict=True):
        grouped[stratum].append(outcome)
    rates = [statistics.fmean(values) for values in grouped.values()]
    return min(rates), max(rates)


def run_audit_dataset(
    spec: DatasetSpec,
    cache_dir: Path,
    *,
    trials: int,
    safe_trials: int,
    offline: bool,
) -> dict[str, object]:
    archive = obtain_dataset(spec, cache_dir, offline=offline)
    features, labels = parse_dataset(archive, spec)
    train_x, train_y, test_x, test_y = stratified_split(features, labels)
    model = train_centroid_model(train_x, train_y)
    train_predictions, train_margins = predict_with_margin(model, train_x)
    predictions, margins = predict_with_margin(model, test_x)
    outcomes = [
        int(prediction == observed)
        for prediction, observed in zip(predictions, test_y, strict=True)
    ]
    joint_strata = audit_strata(
        train_predictions,
        train_margins,
        predictions,
        margins,
        bins=5,
    )
    label_strata = [f"predicted-{value}" for value in predictions]
    joint_quota, joint_queues = audit_base.quota_plan(joint_strata)
    label_quota, label_queues = audit_base.quota_plan(label_strata)
    warmup = max(25, len(outcomes) // 20)

    random_errors: list[float] = []
    joint_errors: list[float] = []
    label_errors: list[float] = []
    null_random_errors: list[float] = []
    null_joint_errors: list[float] = []
    for seed in range(trials):
        random_order, joint_order = audit_base.priority_orders(
            seed, joint_quota, joint_queues
        )
        _, label_order = audit_base.priority_orders(seed, label_quota, label_queues)
        null_outcomes = list(outcomes)
        random.Random(NULL_SEED_OFFSET + seed).shuffle(null_outcomes)
        random_errors.append(_integrated_absolute_error(outcomes, random_order, warmup))
        joint_errors.append(_integrated_absolute_error(outcomes, joint_order, warmup))
        label_errors.append(_integrated_absolute_error(outcomes, label_order, warmup))
        null_random_errors.append(
            _integrated_absolute_error(null_outcomes, random_order, warmup)
        )
        null_joint_errors.append(
            _integrated_absolute_error(null_outcomes, joint_order, warmup)
        )

    stop_differences: list[float] = []
    coverage = {"tool": 0, "random": 0}
    for seed in range(safe_trials):
        random_order, joint_order = audit_base.priority_orders(
            1_000_000 + seed, joint_quota, joint_queues
        )
        random_path = economic.confidence_path(
            outcomes, random_order, joint_strata, alpha=0.05
        )
        joint_path = economic.confidence_path(
            outcomes, joint_order, joint_strata, alpha=0.05
        )
        coverage["random"] += int(random_path["simultaneous_coverage"])
        coverage["tool"] += int(joint_path["simultaneous_coverage"])
        stop_differences.append(
            economic.first_stop(random_path, 0.05)
            - economic.first_stop(joint_path, 0.05)
        )
    accuracy_min, accuracy_max = _stratum_accuracy_range(outcomes, joint_strata)
    safe_interval = economic.paired_mean_interval(
        stop_differences, seed=AUDIT_SPLIT_SEED
    )
    return {
        "name": spec.name,
        "source": {
            "url": spec.url,
            "doi": spec.doi,
            "archive_sha256": spec.sha256,
        },
        "population": {
            "rows": len(features),
            "features": len(features[0]),
            "train_rows": len(train_y),
            "test_rows": len(test_y),
            "classes": len(set(labels)),
            "test_accuracy": statistics.fmean(outcomes),
        },
        "design": {
            "classifier": "training-standardized nearest class centroid",
            "split": "deterministic label-stratified 65/35",
            "joint_strata": len(set(joint_strata)),
            "margin_bins": 5,
            "warmup": warmup,
            "trials": trials,
            "safe_stop_trials": safe_trials,
            "outcomes_used_for_ordering": False,
        },
        "stratum_accuracy_range": [accuracy_min, accuracy_max],
        "integrated_absolute_prefix_error": {
            "prediction_and_margin": paired_summary(
                joint_errors, random_errors, seed=AUDIT_SPLIT_SEED
            ),
            "prediction_only": paired_summary(
                label_errors, random_errors, seed=AUDIT_SPLIT_SEED + 1
            ),
            "shuffled_outcome_null": paired_summary(
                null_joint_errors,
                null_random_errors,
                seed=AUDIT_SPLIT_SEED + 2,
            ),
        },
        "exact_safe_stopping_5pp": {
            "mean_items_saved": statistics.fmean(stop_differences),
            "paired_bootstrap_95_interval": list(safe_interval),
            "tool_win_rate": sum(value > 0 for value in stop_differences)
            / len(stop_differences),
            "simultaneous_coverage_count": coverage,
            "trial_count": safe_trials,
        },
        "certificate": {
            "joint_order_sha256": joint_quota.order_sha256,
            "max_declared_cell_discrepancy": str(joint_quota.max_discrepancy),
            "verified": verify_quota_result(joint_quota).passed,
        },
    }


def run_audit_probe(
    cache_dir: Path, *, trials: int, safe_trials: int, offline: bool
) -> dict[str, object]:
    datasets = [
        run_audit_dataset(
            spec,
            cache_dir,
            trials=trials,
            safe_trials=safe_trials,
            offline=offline,
        )
        for spec in DATASETS
    ]
    positive = [
        result["integrated_absolute_prefix_error"]["prediction_and_margin"]
        ["bootstrap_95_interval"][0]
        > 0
        for result in datasets
    ]
    null_contains_zero = [
        result["integrated_absolute_prefix_error"]["shuffled_outcome_null"]
        ["bootstrap_95_interval"][0]
        <= 0
        <= result["integrated_absolute_prefix_error"]["shuffled_outcome_null"]
        ["bootstrap_95_interval"][1]
        for result in datasets
    ]
    return {
        "schema_version": "audit-generalization-probe-v1",
        "datasets": datasets,
        "cross_dataset_verdict": {
            "positive_datasets": sum(positive),
            "dataset_count": len(datasets),
            "all_shuffled_null_intervals_include_zero": all(null_contains_zero),
            "representative_prefix_signal": (
                "supported" if sum(positive) >= 2 else "not supported"
            ),
            "safe_stopping_claim": (
                "not established; exact intervals are evaluated separately and may erase retrospective gains"
            ),
        },
        "claim_boundary": (
            "These are offline classification-audit replays. They do not validate a medical device, spam filter, banknote system, human-review workflow, or monetary saving."
        ),
    }


def _cell_coordinates(cell: str) -> tuple[int, int, int]:
    coordinates: list[int] = []
    for component in cell.split("|"):
        coordinates.append(int(component.rsplit("q", 1)[1]) - 1)
    if len(coordinates) != 3:
        raise ValueError(f"unexpected finance cell {cell!r}")
    return tuple(coordinates)  # type: ignore[return-value]


def generate_risk_population(
    *, seed: int = 20260801
) -> tuple[list[str], list[float]]:
    preset = application_preset("finance-scenario-cells")
    generator = random.Random(seed)
    strata: list[str] = []
    losses: list[float] = []
    for cell, count in preset.counts:
        shock, volatility, liquidity = _cell_coordinates(cell)
        location = (
            0.7
            + 1.10 * shock
            + 0.55 * volatility
            + 0.35 * liquidity
            + 0.18 * shock * volatility
        )
        scale = 0.25 + 0.10 * volatility + 0.08 * liquidity
        tail_probability = 0.002 + 0.003 * shock + 0.002 * volatility + 0.001 * liquidity
        tail_severity = 7.0 + 2.0 * shock + 1.3 * volatility + 0.8 * liquidity
        for _ in range(count):
            loss = location + scale * abs(generator.gauss(0.0, 1.0))
            if generator.random() < tail_probability:
                loss += tail_severity * (1.0 + generator.expovariate(1.0))
            strata.append(cell)
            losses.append(loss)
    return strata, losses


def empirical_risk(values: list[float], *, quantile: float = 0.975) -> dict[str, float]:
    if not values:
        raise ValueError("risk sample must be nonempty")
    ordered = sorted(values)
    index = min(math.ceil(quantile * len(ordered)) - 1, len(ordered) - 1)
    tail_count = max(math.ceil((1.0 - quantile) * len(ordered)), 1)
    tail = ordered[-tail_count:]
    return {
        "mean": statistics.fmean(ordered),
        "var_97_5": ordered[index],
        "expected_shortfall_97_5": statistics.fmean(tail),
    }


def _risk_prefix_error(
    losses: list[float], order: list[int], checkpoints: tuple[int, ...]
) -> dict[str, float]:
    final = empirical_risk(losses)
    observed: list[float] = []
    errors = {name: [] for name in final}
    checkpoint_set = set(checkpoints)
    for position, index in enumerate(order, 1):
        observed.append(losses[index])
        if position not in checkpoint_set:
            continue
        current = empirical_risk(observed)
        for name, target in final.items():
            errors[name].append(abs(current[name] - target) / max(abs(target), 1e-12))
    return {name: statistics.fmean(values) for name, values in errors.items()}


def _risk_metric_summaries(
    tool: dict[str, list[float]], baseline: dict[str, list[float]], *, seed: int
) -> dict[str, object]:
    return {
        name: paired_summary(tool[name], baseline[name], seed=seed + offset)
        for offset, name in enumerate(sorted(tool))
    }


def run_risk_probe(*, trials: int) -> dict[str, object]:
    strata, aligned_losses = generate_risk_population()
    quota, queues = audit_base.quota_plan(strata)
    if not verify_quota_result(quota).passed:
        raise AssertionError("finance quota certificate did not verify")
    checkpoints = tuple(
        sorted(
            {
                max(100, round(len(strata) * fraction))
                for fraction in (0.02, 0.05, 0.10, 0.20, 0.40, 0.80)
            }
        )
    )
    null_losses = list(aligned_losses)
    random.Random(20260802).shuffle(null_losses)
    metric_names = tuple(empirical_risk(aligned_losses))
    aligned_tool = {name: [] for name in metric_names}
    aligned_random = {name: [] for name in metric_names}
    null_tool = {name: [] for name in metric_names}
    null_random = {name: [] for name in metric_names}
    for seed in range(trials):
        random_order, tool_order = audit_base.priority_orders(seed, quota, queues)
        aligned_random_error = _risk_prefix_error(
            aligned_losses, random_order, checkpoints
        )
        aligned_tool_error = _risk_prefix_error(aligned_losses, tool_order, checkpoints)
        null_random_error = _risk_prefix_error(null_losses, random_order, checkpoints)
        null_tool_error = _risk_prefix_error(null_losses, tool_order, checkpoints)
        for name in metric_names:
            aligned_random[name].append(aligned_random_error[name])
            aligned_tool[name].append(aligned_tool_error[name])
            null_random[name].append(null_random_error[name])
            null_tool[name].append(null_tool_error[name])

    hidden_tail_queues = {
        name: sorted(queue, key=aligned_losses.__getitem__)
        for name, queue in queues.items()
    }
    hidden_tail_order = audit_base.materialize_order(quota, hidden_tail_queues)
    hostile_errors = _risk_prefix_error(
        aligned_losses, hidden_tail_order, checkpoints
    )
    certificate_only_order = audit_base.materialize_order(quota, queues)
    certificate_only_errors = _risk_prefix_error(
        aligned_losses, certificate_only_order, checkpoints
    )
    aligned_summary = _risk_metric_summaries(
        aligned_tool, aligned_random, seed=20260801
    )
    null_summary = _risk_metric_summaries(null_tool, null_random, seed=20260811)
    aligned_positive = {
        name: summary["bootstrap_95_interval"][0] > 0
        for name, summary in aligned_summary.items()
    }
    null_contains_zero = {
        name: summary["bootstrap_95_interval"][0]
        <= 0
        <= summary["bootstrap_95_interval"][1]
        for name, summary in null_summary.items()
    }
    return {
        "schema_version": "risk-scenario-probe-v1",
        "source": {
            "risk_metric": "empirical 97.5% one-tailed expected shortfall",
            "basel_reference": RISK_SOURCE,
            "preset": "finance-scenario-cells",
        },
        "population": {
            "scenarios": len(strata),
            "declared_cells": len(set(strata)),
            "final_risk": empirical_risk(aligned_losses),
        },
        "design": {
            "trials": trials,
            "checkpoints": list(checkpoints),
            "paired_priorities": True,
            "aligned_case": "loss location, scale, and tail rate depend on all three declared cell axes",
            "null_case": "the same losses are permuted independently of declared cells",
            "hostile_case": "losses are sorted low-to-high inside every cell before quota interleaving",
        },
        "aligned_driver_case": aligned_summary,
        "permuted_cell_null": null_summary,
        "hostile_within_cell_order": {
            "integrated_relative_error": hostile_errors,
            "unscrambled_stable_queue_error": certificate_only_errors,
            "categorical_certificate_still_passes": verify_quota_result(quota).passed,
        },
        "certificate": {
            "order_sha256": quota.order_sha256,
            "max_declared_cell_discrepancy": str(quota.max_discrepancy),
            "verified": verify_quota_result(quota).passed,
        },
        "verdict": {
            "aligned_metrics_with_positive_95_interval": aligned_positive,
            "null_intervals_include_zero": null_contains_zero,
            "application_signal": (
                "supported for metrics whose aligned-case interval is positive; not universal"
            ),
            "falsification_signal": (
                "the categorical certificate does not control hidden within-cell tail ordering"
            ),
        },
        "claim_boundary": (
            "This is a stylized finite-population simulation, not a bank model, regulatory backtest, pricing engine, capital calculation, or measured cost saving."
        ),
    }


def _percent(value: float) -> str:
    return f"{100 * value:.1f}%"


def render_report(payload: dict[str, object]) -> str:
    audit = payload["audit_ordering"]
    risk = payload["risk_scenarios"]
    lines = [
        "# Practical application probes: model audits and risk scenarios",
        "",
        "Date: 2026-08-01",
        "",
        "## Bottom line",
        "",
        f"- Audit ordering: **{audit['cross_dataset_verdict']['representative_prefix_signal']}** for retrospective prefix representativeness across the new datasets; safe stopping remains separately gated.",
        "- Risk scenarios: declared-cell balancing is useful only when the cells predict the downstream loss distribution; the null and hostile controls reject a universal risk-estimation claim.",
        "",
        "## Direction 1: costly model-audit ordering",
        "",
        "Every ordering uses predictions and training-derived margins only. Ground-truth correctness is revealed after the order is fixed.",
        f"Design: {audit['datasets'][0]['design']['trials']} paired priority replays and {audit['datasets'][0]['design']['safe_stop_trials']} exact safe-stopping trials per dataset; 95% reduction intervals use 2,000 paired bootstrap replicates.",
        "",
        "| dataset | test n | accuracy | joint-stratum error reduction (95% interval) | prediction-only reduction | shuffled-outcome null | exact 5pp reviews saved |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for dataset in audit["datasets"]:
        metrics = dataset["integrated_absolute_prefix_error"]
        joint = metrics["prediction_and_margin"]
        label = metrics["prediction_only"]
        null = metrics["shuffled_outcome_null"]
        safe = dataset["exact_safe_stopping_5pp"]
        lines.append(
            f"| {dataset['name']} | {dataset['population']['test_rows']} | "
            f"{_percent(dataset['population']['test_accuracy'])} | "
            f"{_percent(joint['relative_reduction'])} "
            f"[{_percent(joint['bootstrap_95_interval'][0])}, {_percent(joint['bootstrap_95_interval'][1])}] | "
            f"{_percent(label['relative_reduction'])} | "
            f"{_percent(null['relative_reduction'])} "
            f"[{_percent(null['bootstrap_95_interval'][0])}, {_percent(null['bootstrap_95_interval'][1])}] | "
            f"{safe['mean_items_saved']:.1f} "
            f"[{safe['paired_bootstrap_95_interval'][0]:.1f}, {safe['paired_bootstrap_95_interval'][1]:.1f}] |"
        )
    lines.extend(
        [
            "",
            "Interpretation: a positive joint-stratum interval is early evidence that balancing outcome-blind metadata improves the accuracy trajectory of the audited prefix. The shuffled-outcome control asks whether the same result survives after the metadata/outcome relationship is destroyed. The exact safe-stopping column is the stronger operational gate: retrospective error reduction is not labor saving unless a valid observable stopping rule also stops earlier.",
            "",
            "## Direction 2: interruptible risk-scenario evaluation",
            "",
            f"Population: {risk['population']['scenarios']:,} scenarios in {risk['population']['declared_cells']} return-shock × volatility × liquidity cells. The reported tail metric is empirical 97.5% expected shortfall.",
            f"Design: {risk['design']['trials']} paired priority trials evaluated at {len(risk['design']['checkpoints'])} fixed checkpoints; 95% reduction intervals use 2,000 paired bootstrap replicates.",
            "",
            "| metric | aligned-driver error reduction (95% interval) | permuted-cell null (95% interval) | hostile within-cell relative error |",
            "|---|---:|---:|---:|",
        ]
    )
    for name in sorted(risk["aligned_driver_case"]):
        aligned = risk["aligned_driver_case"][name]
        null = risk["permuted_cell_null"][name]
        hostile = risk["hostile_within_cell_order"]["integrated_relative_error"][name]
        lines.append(
            f"| {name} | {_percent(aligned['relative_reduction'])} "
            f"[{_percent(aligned['bootstrap_95_interval'][0])}, {_percent(aligned['bootstrap_95_interval'][1])}] | "
            f"{_percent(null['relative_reduction'])} "
            f"[{_percent(null['bootstrap_95_interval'][0])}, {_percent(null['bootstrap_95_interval'][1])}] | "
            f"{_percent(hostile)} |"
        )
    lines.extend(
        [
            "",
            "Interpretation: the aligned case is a positive control in which the declared axes really drive location, scale, and tail frequency. The null permutes losses away from those cells. The hostile case sorts losses inside every cell while leaving the categorical quota certificate valid; it directly tests the certificate's stated limitation.",
            "",
            "## Decision",
            "",
            "1. Continue the model-audit direction only as an **anytime representativeness** claim until exact stopping improves on at least two prospective datasets.",
            "2. Continue the risk direction only with preregistered downstream error metrics and cell definitions learned without evaluated losses. Never present category balance itself as VaR or expected-shortfall control.",
            "3. The next external pilot should compare quota-balanced, seeded-random, and production order on identical items and commit every order digest before labels or losses are revealed.",
            "",
            "## Claim boundaries",
            "",
            f"- {audit['claim_boundary']}",
            f"- {risk['claim_boundary']}",
            "- All percentage improvements are finite-population replay/simulation results, not general guarantees.",
            "",
            "## Reproduction",
            "",
            "Machine-readable evidence: `artifacts/practical_application_probe.json`.",
            "",
            "```bash",
            "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 practical_application_probe.py",
            "PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python3 -m unittest tests.test_practical_application_probe",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def run_all(
    cache_dir: Path,
    *,
    audit_trials: int,
    safe_trials: int,
    risk_trials: int,
    offline: bool,
) -> dict[str, object]:
    return {
        "schema_version": "practical-application-probes-v1",
        "audit_ordering": run_audit_probe(
            cache_dir,
            trials=audit_trials,
            safe_trials=safe_trials,
            offline=offline,
        ),
        "risk_scenarios": run_risk_probe(trials=risk_trials),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("/tmp/coprimebatch-practical-probe-data"),
    )
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--audit-trials", type=int, default=500)
    parser.add_argument("--safe-trials", type=int, default=20)
    parser.add_argument("--risk-trials", type=int, default=40)
    parser.add_argument(
        "--json-out",
        type=Path,
        default=Path("artifacts/practical_application_probe.json"),
    )
    parser.add_argument(
        "--report-out",
        type=Path,
        default=Path("artifacts/PRACTICAL_APPLICATION_PROBE.md"),
    )
    arguments = parser.parse_args()
    if min(arguments.audit_trials, arguments.safe_trials, arguments.risk_trials) < 1:
        raise ValueError("all trial counts must be positive")
    payload = run_all(
        arguments.cache_dir,
        audit_trials=arguments.audit_trials,
        safe_trials=arguments.safe_trials,
        risk_trials=arguments.risk_trials,
        offline=arguments.offline,
    )
    arguments.json_out.parent.mkdir(parents=True, exist_ok=True)
    arguments.report_out.parent.mkdir(parents=True, exist_ok=True)
    arguments.json_out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    arguments.report_out.write_text(render_report(payload))
    print(json.dumps({
        "audit": payload["audit_ordering"]["cross_dataset_verdict"],
        "risk": payload["risk_scenarios"]["verdict"],
    }, indent=2))
    print(f"wrote {arguments.json_out}")
    print(f"wrote {arguments.report_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
