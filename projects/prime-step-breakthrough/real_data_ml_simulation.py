#!/usr/bin/env python3
"""Real-data downstream-value experiment for categorical prefix balance.

The experiment uses the UCI Optical Recognition of Handwritten Digits train/test
split, a dependency-free nearest-centroid classifier, and only pre-audit
metadata: predicted digit and a classifier-margin bin learned from the training
set.  It compares random audit order with the quota constructor while holding
the random within-stratum priority of every test item fixed. Ground truth is
used only to score the simulated audits, never to construct an order.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import io
import json
import math
import os
from pathlib import Path
import random
import statistics
import tempfile
import urllib.request
import zipfile

from coprimebatch.prefix_balance import QuotaResult, quota_order, verify_quota_result


DATASET_URL = (
    "https://archive.ics.uci.edu/static/public/80/"
    "optical%2Brecognition%2Bof%2Bhandwritten%2Bdigits.zip"
)
DATASET_SHA256 = "0d7b054fea010270e9b3f06411c654c5e59547732ad626381980baffe0a23fb0"
DATASET_DOI = "https://doi.org/10.24432/C50P49"
TRAIN_MEMBER = "optdigits.tra"
TEST_MEMBER = "optdigits.tes"
EXPECTED_TRAIN_ROWS = 3823
EXPECTED_TEST_ROWS = 1797
DEFAULT_TRIALS = 2000
DEFAULT_WARMUP = 50
DEFAULT_MARGIN_BINS = 5
CHECKPOINTS = (25, 50, 100, 200, 500, 1000)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def obtain_dataset(cache_path: Path, *, offline: bool = False) -> Path:
    """Return a checksum-verified UCI archive, downloading it when allowed."""

    cache_path = cache_path.expanduser().resolve()
    if cache_path.exists() and _sha256(cache_path) == DATASET_SHA256:
        return cache_path
    if offline:
        raise FileNotFoundError(
            f"no checksum-valid offline dataset at {cache_path}; expected {DATASET_SHA256}"
        )
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=cache_path.parent, prefix=cache_path.name + ".", delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)
        with urllib.request.urlopen(DATASET_URL, timeout=60) as response:
            while block := response.read(1 << 20):
                temporary.write(block)
    try:
        observed = _sha256(temporary_path)
        if observed != DATASET_SHA256:
            raise ValueError(
                f"dataset checksum mismatch: expected {DATASET_SHA256}, observed {observed}"
            )
        os.replace(temporary_path, cache_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return cache_path


def _load_member(archive: zipfile.ZipFile, member: str) -> tuple[list[tuple[int, ...]], list[int]]:
    features: list[tuple[int, ...]] = []
    labels: list[int] = []
    with archive.open(member) as raw:
        reader = csv.reader(io.TextIOWrapper(raw, encoding="ascii", newline=""))
        for row_number, row in enumerate(reader, 1):
            if len(row) != 65:
                raise ValueError(f"{member}:{row_number}: expected 65 columns, found {len(row)}")
            values = tuple(int(value) for value in row)
            features.append(values[:-1])
            labels.append(values[-1])
    return features, labels


def load_dataset(path: Path) -> tuple[list[tuple[int, ...]], list[int], list[tuple[int, ...]], list[int]]:
    if _sha256(path) != DATASET_SHA256:
        raise ValueError("dataset archive is not the pinned UCI artifact")
    with zipfile.ZipFile(path) as archive:
        train_x, train_y = _load_member(archive, TRAIN_MEMBER)
        test_x, test_y = _load_member(archive, TEST_MEMBER)
    if len(train_x) != EXPECTED_TRAIN_ROWS or len(test_x) != EXPECTED_TEST_ROWS:
        raise ValueError(
            f"unexpected split sizes: train={len(train_x)}, test={len(test_x)}"
        )
    if set(train_y) != set(range(10)) or set(test_y) != set(range(10)):
        raise ValueError("expected digit labels 0 through 9 in both splits")
    return train_x, train_y, test_x, test_y


def train_centroids(features: list[tuple[int, ...]], labels: list[int]) -> tuple[tuple[float, ...], ...]:
    dimensions = len(features[0])
    sums = [[0.0] * dimensions for _ in range(10)]
    counts = [0] * 10
    for row, label in zip(features, labels, strict=True):
        counts[label] += 1
        for index, value in enumerate(row):
            sums[label][index] += value
    return tuple(
        tuple(value / counts[label] for value in sums[label]) for label in range(10)
    )


def predict_with_margin(
    features: list[tuple[int, ...]], centroids: tuple[tuple[float, ...], ...]
) -> tuple[list[int], list[float]]:
    predictions: list[int] = []
    margins: list[float] = []
    for row in features:
        distances = [
            sum((value - center) ** 2 for value, center in zip(row, centroid, strict=True))
            for centroid in centroids
        ]
        ranked = sorted(range(10), key=distances.__getitem__)
        best, second = ranked[:2]
        predictions.append(best)
        margins.append((distances[second] - distances[best]) / max(distances[second], 1e-12))
    return predictions, margins


def margin_thresholds(training_margins: list[float], bins: int) -> tuple[float, ...]:
    if bins < 1:
        raise ValueError("margin bins must be positive")
    if bins == 1:
        return ()
    return tuple(statistics.quantiles(training_margins, n=bins, method="inclusive"))


def margin_thresholds_by_prediction(
    training_predictions: list[int], training_margins: list[float], bins: int
) -> dict[int, tuple[float, ...]]:
    return {
        predicted: margin_thresholds(
            [
                margin
                for prediction, margin in zip(
                    training_predictions, training_margins, strict=True
                )
                if prediction == predicted
            ],
            bins,
        )
        for predicted in sorted(set(training_predictions))
    }


def joint_strata(
    predictions: list[int],
    margins: list[float],
    thresholds_by_prediction: dict[int, tuple[float, ...]],
) -> list[str]:
    """Use only pre-audit prediction metadata—not ground truth/correctness."""

    return [
        f"predicted-{prediction}:margin-"
        f"{bisect.bisect_right(thresholds_by_prediction[prediction], margin)}"
        for prediction, margin in zip(predictions, margins, strict=True)
    ]


def _queues(strata: list[str]) -> dict[str, list[int]]:
    queues: dict[str, list[int]] = {}
    for index, stratum in enumerate(strata):
        queues.setdefault(stratum, []).append(index)
    return queues


def quota_plan(strata: list[str]) -> tuple[QuotaResult, dict[str, list[int]]]:
    queues = _queues(strata)
    result = quota_order({stratum: len(queue) for stratum, queue in queues.items()})
    report = verify_quota_result(result)
    if not report.passed:
        raise AssertionError(f"quota certificate failed: {report.errors}")
    return result, queues


def materialize_order(
    result: QuotaResult, queues: dict[str, list[int]]
) -> list[int]:
    positions = {stratum: 0 for stratum in queues}
    order: list[int] = []
    for code in result.order_codes:
        stratum = result.categories[code]
        position = positions[stratum]
        order.append(queues[stratum][position])
        positions[stratum] = position + 1
    return order


def priority_orders(
    seed: int,
    result: QuotaResult,
    base_queues: dict[str, list[int]],
) -> tuple[list[int], list[int]]:
    """Return paired random/tool orders using identical per-item priorities."""

    item_count = sum(len(queue) for queue in base_queues.values())
    generator = random.Random(seed)
    priorities = [generator.random() for _ in range(item_count)]
    random_order = sorted(range(item_count), key=priorities.__getitem__)
    ranked_queues = {
        stratum: sorted(queue, key=priorities.__getitem__)
        for stratum, queue in base_queues.items()
    }
    return random_order, materialize_order(result, ranked_queues)


def prefix_errors(correct: list[int], order: list[int]) -> list[float]:
    final_accuracy = sum(correct) / len(correct)
    running = 0
    errors: list[float] = []
    for prefix, index in enumerate(order, 1):
        running += correct[index]
        errors.append(running / prefix - final_accuracy)
    return errors


def integrated_metrics(errors: list[float], warmup: int) -> dict[str, float | int]:
    if not 1 <= warmup <= len(errors):
        raise ValueError("warmup must lie inside the evaluated prefix range")
    tail = errors[warmup - 1 :]
    mae = sum(abs(value) for value in tail) / len(tail)
    mse = sum(value * value for value in tail) / len(tail)
    above = [index for index, value in enumerate(errors, 1) if abs(value) > 0.01]
    return {
        "warmup": warmup,
        "mean_absolute_error": mae,
        "mean_squared_error": mse,
        "root_mean_squared_error": math.sqrt(mse),
        "max_absolute_error": max(abs(value) for value in tail),
        "one_percent_settling_prefix": (above[-1] + 1 if above else 1),
    }


def settling_prefix(curve: list[float], threshold: float) -> int:
    """Return the first prefix after the curve's last threshold violation."""

    if threshold <= 0:
        raise ValueError("threshold must be positive")
    violations = [index for index, value in enumerate(curve, 1) if value > threshold]
    return violations[-1] + 1 if violations else 1


def _relative_reduction(tool: float, baseline: float) -> float:
    return 1.0 - tool / baseline


def bootstrap_reduction_interval(
    tool_values: list[float],
    baseline_values: list[float],
    *,
    replicates: int = 2000,
    seed: int = 20260716,
) -> tuple[float, float]:
    if len(tool_values) != len(baseline_values) or not tool_values:
        raise ValueError("bootstrap inputs must be non-empty paired vectors")
    generator = random.Random(seed)
    count = len(tool_values)
    reductions: list[float] = []
    for _ in range(replicates):
        tool_sum = 0.0
        baseline_sum = 0.0
        for _ in range(count):
            index = generator.randrange(count)
            tool_sum += tool_values[index]
            baseline_sum += baseline_values[index]
        reductions.append(1.0 - tool_sum / baseline_sum)
    reductions.sort()
    return reductions[int(0.025 * replicates)], reductions[int(0.975 * replicates)]


def _summarize_paired(
    tool_values: list[float], baseline_values: list[float], *, bootstrap_seed: int
) -> dict[str, object]:
    tool_mean = statistics.fmean(tool_values)
    baseline_mean = statistics.fmean(baseline_values)
    interval = bootstrap_reduction_interval(
        tool_values, baseline_values, seed=bootstrap_seed
    )
    return {
        "tool_mean": tool_mean,
        "random_mean": baseline_mean,
        "relative_reduction": _relative_reduction(tool_mean, baseline_mean),
        "bootstrap_95_interval": list(interval),
        "paired_win_rate": sum(
            tool < baseline
            for tool, baseline in zip(tool_values, baseline_values, strict=True)
        )
        / len(tool_values),
    }


def run_simulation(
    dataset_path: Path,
    *,
    trials: int = DEFAULT_TRIALS,
    warmup: int = DEFAULT_WARMUP,
    bins: int = DEFAULT_MARGIN_BINS,
) -> dict[str, object]:
    if trials < 1:
        raise ValueError("trials must be positive")
    train_x, train_y, test_x, test_y = load_dataset(dataset_path)
    centroids = train_centroids(train_x, train_y)
    train_predictions, train_margins = predict_with_margin(train_x, centroids)
    test_predictions, test_margins = predict_with_margin(test_x, centroids)
    thresholds_by_prediction = margin_thresholds_by_prediction(
        train_predictions, train_margins, bins
    )
    correct = [int(prediction == label) for prediction, label in zip(test_predictions, test_y, strict=True)]
    final_accuracy = sum(correct) / len(correct)

    strata = joint_strata(test_predictions, test_margins, thresholds_by_prediction)
    joint_result, joint_queues = quota_plan(strata)
    label_result, label_queues = quota_plan(
        [f"predicted-{prediction}" for prediction in test_predictions]
    )

    random_mae: list[float] = []
    random_mse: list[float] = []
    joint_mae: list[float] = []
    joint_mse: list[float] = []
    label_mae: list[float] = []
    label_mse: list[float] = []
    checkpoint_sums = {
        prefix: {"tool_abs": 0.0, "tool_sq": 0.0, "random_abs": 0.0, "random_sq": 0.0}
        for prefix in CHECKPOINTS
        if prefix <= len(test_y)
    }
    curve_sums = {
        "tool_abs": [0.0] * len(test_y),
        "tool_sq": [0.0] * len(test_y),
        "random_abs": [0.0] * len(test_y),
        "random_sq": [0.0] * len(test_y),
    }

    for seed in range(trials):
        random_order, joint_order = priority_orders(seed, joint_result, joint_queues)
        _, label_order = priority_orders(seed, label_result, label_queues)
        random_errors = prefix_errors(correct, random_order)
        joint_errors = prefix_errors(correct, joint_order)
        label_errors = prefix_errors(correct, label_order)
        random_metrics = integrated_metrics(random_errors, warmup)
        joint_metrics = integrated_metrics(joint_errors, warmup)
        label_metrics = integrated_metrics(label_errors, warmup)
        random_mae.append(float(random_metrics["mean_absolute_error"]))
        random_mse.append(float(random_metrics["mean_squared_error"]))
        joint_mae.append(float(joint_metrics["mean_absolute_error"]))
        joint_mse.append(float(joint_metrics["mean_squared_error"]))
        label_mae.append(float(label_metrics["mean_absolute_error"]))
        label_mse.append(float(label_metrics["mean_squared_error"]))
        for index, (tool_error, random_error) in enumerate(
            zip(joint_errors, random_errors, strict=True)
        ):
            curve_sums["tool_abs"][index] += abs(tool_error)
            curve_sums["tool_sq"][index] += tool_error * tool_error
            curve_sums["random_abs"][index] += abs(random_error)
            curve_sums["random_sq"][index] += random_error * random_error
        for prefix, sums in checkpoint_sums.items():
            tool_error = joint_errors[prefix - 1]
            random_error = random_errors[prefix - 1]
            sums["tool_abs"] += abs(tool_error)
            sums["tool_sq"] += tool_error * tool_error
            sums["random_abs"] += abs(random_error)
            sums["random_sq"] += random_error * random_error

    original_order = list(range(len(test_y)))
    original_tool_order = materialize_order(joint_result, joint_queues)
    adversarial_queues = {
        stratum: sorted(queue, key=lambda index: (correct[index], index))
        for stratum, queue in joint_queues.items()
    }
    adversarial_order = materialize_order(joint_result, adversarial_queues)

    checkpoints: dict[str, object] = {}
    for prefix, sums in checkpoint_sums.items():
        tool_mae = sums["tool_abs"] / trials
        random_mae_at_prefix = sums["random_abs"] / trials
        tool_mse = sums["tool_sq"] / trials
        random_mse_at_prefix = sums["random_sq"] / trials
        checkpoints[str(prefix)] = {
            "tool_mean_absolute_error": tool_mae,
            "random_mean_absolute_error": random_mae_at_prefix,
            "absolute_error_reduction": _relative_reduction(tool_mae, random_mae_at_prefix),
            "tool_root_mean_squared_error": math.sqrt(tool_mse),
            "random_root_mean_squared_error": math.sqrt(random_mse_at_prefix),
            "squared_error_reduction": _relative_reduction(tool_mse, random_mse_at_prefix),
        }

    mean_curves = {
        "tool_mean_absolute_error": [value / trials for value in curve_sums["tool_abs"]],
        "random_mean_absolute_error": [value / trials for value in curve_sums["random_abs"]],
        "tool_root_mean_squared_error": [
            math.sqrt(value / trials) for value in curve_sums["tool_sq"]
        ],
        "random_root_mean_squared_error": [
            math.sqrt(value / trials) for value in curve_sums["random_sq"]
        ],
    }
    threshold_results: dict[str, object] = {}
    for metric, tool_key, random_key in (
        (
            "mean_absolute_error",
            "tool_mean_absolute_error",
            "random_mean_absolute_error",
        ),
        (
            "root_mean_squared_error",
            "tool_root_mean_squared_error",
            "random_root_mean_squared_error",
        ),
    ):
        metric_results: dict[str, object] = {}
        for threshold in (0.03, 0.02, 0.01, 0.005):
            tool_prefix = settling_prefix(mean_curves[tool_key], threshold)
            random_prefix = settling_prefix(mean_curves[random_key], threshold)
            metric_results[f"{threshold:.3f}"] = {
                "tool_settling_prefix": tool_prefix,
                "random_settling_prefix": random_prefix,
                "item_reduction": _relative_reduction(tool_prefix, random_prefix),
            }
        threshold_results[metric] = metric_results

    class_accuracy = {
        str(label): sum(correct[index] for index, value in enumerate(test_y) if value == label)
        / sum(value == label for value in test_y)
        for label in range(10)
    }

    return {
        "schema_version": "real-data-ml-simulation-v1",
        "dataset": {
            "name": "UCI Optical Recognition of Handwritten Digits",
            "doi": DATASET_DOI,
            "url": DATASET_URL,
            "license": "CC BY 4.0",
            "archive_sha256": DATASET_SHA256,
            "train_rows": len(train_y),
            "test_rows": len(test_y),
            "features": len(train_x[0]),
        },
        "classifier": {
            "type": "nearest class centroid, squared Euclidean distance",
            "training_source": "UCI designated training split only",
            "audit_design": (
                "predictions and confidence margins are treated as existing metadata; "
                "ground-truth reveal/validation is the ordered audit operation"
            ),
            "test_accuracy": final_accuracy,
            "correct": sum(correct),
            "incorrect": len(correct) - sum(correct),
            "accuracy_by_digit": class_accuracy,
        },
        "strata": {
            "definition": "predicted digit x within-predicted-digit margin bin",
            "ground_truth_used_to_define_strata": False,
            "correctness_used_to_define_strata": False,
            "margin_threshold_source": (
                "UCI designated training split, grouped by training prediction"
            ),
            "margin_bins": bins,
            "margin_thresholds_by_prediction": {
                str(prediction): list(thresholds)
                for prediction, thresholds in thresholds_by_prediction.items()
            },
            "nonempty_joint_cells": len(joint_queues),
        },
        "certificate": {
            "algorithm": joint_result.algorithm,
            "verified": verify_quota_result(joint_result).passed,
            "positions": len(joint_result.order_codes),
            "max_discrepancy": str(joint_result.max_discrepancy),
            "lower_bound": str(joint_result.lower_bound),
            "ratio_bound": (
                str(joint_result.ratio_bound) if joint_result.ratio_bound is not None else None
            ),
            "strict_factor": joint_result.strict_factor,
            "order_sha256": joint_result.order_sha256,
        },
        "simulation": {
            "trials": trials,
            "seed_range": [0, trials - 1],
            "warmup_prefix": warmup,
            "paired_design": (
                "each trial assigns identical random priorities to items; random order sorts all "
                "items, tool order sorts within each fixed stratum then quota-interleaves strata"
            ),
            "integrated_prefix_error": {
                "mean_absolute_error": _summarize_paired(
                    joint_mae, random_mae, bootstrap_seed=20260716
                ),
                "mean_squared_error": _summarize_paired(
                    joint_mse, random_mse, bootstrap_seed=20260717
                ),
                "label_only_ablation": {
                    "mean_absolute_error": _summarize_paired(
                        label_mae, random_mae, bootstrap_seed=20260718
                    ),
                    "mean_squared_error": _summarize_paired(
                        label_mse, random_mse, bootstrap_seed=20260719
                    ),
                },
            },
            "checkpoints": checkpoints,
            "expected_error_thresholds": {
                "definition": (
                    "first prefix after which the across-trial expected error curve never "
                    "again exceeds the stated threshold"
                ),
                **threshold_results,
            },
        },
        "observed_orders": {
            "original_uci_order": integrated_metrics(
                prefix_errors(correct, original_order), warmup
            ),
            "quota_order_with_original_within_stratum_queues": integrated_metrics(
                prefix_errors(correct, original_tool_order), warmup
            ),
        },
        "negative_control": {
            "description": (
                "within every predicted-digit x confidence stratum, incorrect cases are placed "
                "first; the tool still balances declared cells but cannot control hidden "
                "within-cell outcome order"
            ),
            "outcome_leakage_intentional": True,
            "metrics": integrated_metrics(prefix_errors(correct, adversarial_order), warmup),
        },
        "claim_boundary": (
            "Observed reductions apply to this classifier, dataset, pre-audit metadata, "
            "accuracy-audit metric, and simulation design. They do not establish universal "
            "accuracy, inference-compute, human-time, monetary, or production savings."
        ),
    }


def render_report(payload: dict[str, object]) -> str:
    dataset = payload["dataset"]
    classifier = payload["classifier"]
    strata = payload["strata"]
    certificate = payload["certificate"]
    simulation = payload["simulation"]
    integrated = simulation["integrated_prefix_error"]
    mae = integrated["mean_absolute_error"]
    mse = integrated["mean_squared_error"]
    ablation = integrated["label_only_ablation"]["mean_absolute_error"]
    observed = payload["observed_orders"]
    negative = payload["negative_control"]

    def pct(value: float) -> str:
        return f"{100 * value:.1f}%"

    checkpoint_rows = []
    for prefix in sorted(simulation["checkpoints"], key=int):
        values = simulation["checkpoints"][prefix]
        checkpoint_rows.append(
            f"| {prefix} | {values['tool_mean_absolute_error']:.5f} | "
            f"{values['random_mean_absolute_error']:.5f} | "
            f"{pct(values['absolute_error_reduction'])} | "
            f"{pct(values['squared_error_reduction'])} |"
        )

    threshold_rows = []
    threshold_payload = simulation["expected_error_thresholds"]
    for metric_label, metric_key in (
        ("Mean absolute error", "mean_absolute_error"),
        ("Root mean squared error", "root_mean_squared_error"),
    ):
        for threshold in ("0.020", "0.010", "0.005"):
            values = threshold_payload[metric_key][threshold]
            threshold_rows.append(
                f"| {metric_label} | {float(threshold):.1%} | "
                f"{values['tool_settling_prefix']} | {values['random_settling_prefix']} | "
                f"{pct(values['item_reduction'])} |"
            )

    return "\n".join(
        [
            "# Real-data ML prefix-balance simulation",
            "",
            "## Result",
            "",
            f"Across **{simulation['trials']:,} paired simulations**, balancing the declared "
            f"predicted-digit × training-derived confidence strata reduced integrated mean "
            f"absolute prefix error by **{pct(mae['relative_reduction'])}** and integrated mean "
            f"squared prefix error by **{pct(mse['relative_reduction'])}** relative to random "
            f"audit order.",
            "",
            f"The bootstrap 95% intervals for the reductions are "
            f"**{pct(mae['bootstrap_95_interval'][0])} to "
            f"{pct(mae['bootstrap_95_interval'][1])}** for absolute error and "
            f"**{pct(mse['bootstrap_95_interval'][0])} to "
            f"{pct(mse['bootstrap_95_interval'][1])}** for squared error.",
            "",
            "This demonstrates a repeatable statistical gain on one real workload. It does "
            "not demonstrate universal savings or a production deployment.",
            "",
            "At prefix 25 the tool was worse than random order; the specified integrated "
            "metric begins at prefix 50. The observed advantage is therefore not a claim about "
            "the smallest possible prefixes.",
            "",
            "## Data and model",
            "",
            f"- Dataset: [{dataset['name']}]({dataset['doi']}), CC BY 4.0; pinned archive "
            f"SHA-256 `{dataset['archive_sha256']}`.",
            f"- Split: {dataset['train_rows']:,} official training cases and "
            f"{dataset['test_rows']:,} official test cases, each with {dataset['features']} features.",
            f"- Classifier: {classifier['type']}; test accuracy "
            f"**{pct(classifier['test_accuracy'])}** ({classifier['correct']}/{dataset['test_rows']}).",
            f"- Audit model: predictions and confidence margins are assumed to exist before "
            f"audit ordering; revealing/validating ground truth is the ordered operation.",
            f"- Strata: {strata['definition']}, with {strata['nonempty_joint_cells']} nonempty "
            f"cells. Thresholds come only from the training split; test ground truth and "
            f"correctness are not used to define strata.",
            "",
            "## Simulation design",
            "",
            f"For every seed from 0 through {simulation['seed_range'][1]}, each test case receives "
            "one random priority. The random baseline sorts all audit cases by that priority. The "
            "tool uses the same priorities inside each fixed stratum, then quota-interleaves the "
            "strata. This isolates the interleaving policy instead of giving the tool a friendlier "
            "within-stratum shuffle.",
            "",
            f"The downstream quantity is absolute error between prefix accuracy and the final "
            f"{pct(classifier['test_accuracy'])} test accuracy. Integrated metrics start at prefix "
            f"{simulation['warmup_prefix']}.",
            "",
            "| Prefix | Tool mean absolute error | Random mean absolute error | Absolute-error reduction | Squared-error reduction |",
            "|---:|---:|---:|---:|---:|",
            *checkpoint_rows,
            "",
            "## Equivalent audit work",
            "",
            "The table below reports the first prefix after which the across-trial expected "
            "error curve stays below the target for the rest of the run.",
            "",
            "| Expected-error metric | Target | Tool audits | Random-order audits | Fewer audited items |",
            "|---|---:|---:|---:|---:|",
            *threshold_rows,
            "",
            "These are audit-count reductions in an offline replay, not measured human time, "
            "money, wall time, or inference savings. They become operational savings only when "
            "ground-truth review/validation is costly and early stopping is allowed. The model "
            "predictions themselves must already exist.",
            "",
            "## What the extra stratification contributes",
            "",
            f"Balancing predicted digit labels alone changed integrated absolute error by "
            f"**{pct(ablation['relative_reduction'])}** versus random order. The joint confidence "
            f"strata produced the stronger {pct(mae['relative_reduction'])} reduction. This is "
            "evidence that declared features must relate to the downstream loss; the ordering "
            "algorithm cannot invent that relationship.",
            "",
            "## Actual supplied order",
            "",
            f"On the UCI file's original test order, integrated absolute prefix error was "
            f"`{observed['original_uci_order']['mean_absolute_error']:.6f}`. Using the certificate "
            f"while preserving the original within-stratum queues produced "
            f"`{observed['quota_order_with_original_within_stratum_queues']['mean_absolute_error']:.6f}`.",
            "",
            "## Certificate",
            "",
            f"- Independent verifier passed: `{str(certificate['verified']).lower()}`.",
            f"- Positions: {certificate['positions']:,}; max declared-cell discrepancy "
            f"`{certificate['max_discrepancy']}`; lower bound `{certificate['lower_bound']}`.",
            f"- Order digest: `{certificate['order_sha256']}`.",
            "",
            "## Negative control",
            "",
            f"When incorrect cases are intentionally placed first inside every fixed stratum, "
            f"the certificate still balances declared cells but integrated absolute accuracy "
            f"error rises to `{negative['metrics']['mean_absolute_error']:.6f}`. This refutes the "
            "stronger claim that categorical prefix balance alone guarantees estimator quality.",
            "",
            "## Honest conclusion",
            "",
            payload["claim_boundary"],
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache",
        type=Path,
        default=Path("/tmp/coprimebatch-uci-optdigits.zip"),
        help="checksum-verified dataset cache",
    )
    parser.add_argument("--offline", action="store_true", help="refuse network download")
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--warmup", type=int, default=DEFAULT_WARMUP)
    parser.add_argument("--margin-bins", type=int, default=DEFAULT_MARGIN_BINS)
    parser.add_argument(
        "--json-out",
        type=Path,
        default=Path("artifacts/real_data_ml_simulation.json"),
    )
    parser.add_argument(
        "--report-out",
        type=Path,
        default=Path("artifacts/REAL_DATA_ML_SIMULATION.md"),
    )
    arguments = parser.parse_args()
    dataset_path = obtain_dataset(arguments.cache, offline=arguments.offline)
    payload = run_simulation(
        dataset_path,
        trials=arguments.trials,
        warmup=arguments.warmup,
        bins=arguments.margin_bins,
    )
    arguments.json_out.parent.mkdir(parents=True, exist_ok=True)
    arguments.report_out.parent.mkdir(parents=True, exist_ok=True)
    arguments.json_out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    arguments.report_out.write_text(render_report(payload))
    print(json.dumps(payload["simulation"]["integrated_prefix_error"], indent=2))
    print(f"wrote {arguments.json_out}")
    print(f"wrote {arguments.report_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
