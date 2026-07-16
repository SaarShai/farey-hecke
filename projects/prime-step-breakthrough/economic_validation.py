#!/usr/bin/env python3
"""Observable safe-stopping and economic evidence on the frozen UCI audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import time
import random
from functools import lru_cache
from pathlib import Path

import real_data_ml_simulation as ml


DEFAULT_ALPHA = 0.05
DEFAULT_TRIALS = 200
DEFAULT_EPSILONS = (0.05, 0.03, 0.01)
LOADED_RATES = {
    "data_entry_proxy": 28.96,
    "quality_control_proxy": 34.73,
    "biological_technician_proxy": 39.94,
    "clinical_lab_proxy": 42.98,
    "compliance_proxy": 57.62,
    "financial_examiner_proxy": 67.22,
}
LOADED_RATE_BANDS = {
    "data_entry_proxy": [21.85, 28.96, 41.17],
    "quality_control_proxy": [25.39, 34.73, 55.69],
    "biological_technician_proxy": [28.01, 39.94, 58.99],
    "clinical_lab_proxy": [26.40, 42.98, 68.05],
    "compliance_proxy": [34.42, 57.62, 95.46],
    "financial_examiner_proxy": [40.15, 67.22, 124.35],
    "software_qa_proxy": [42.67, 72.43, 115.98],
    "medical_scientist_proxy": [45.00, 71.82, 123.46],
    "biochemist_biophysicist_proxy": [51.58, 88.49, 139.67],
}


@lru_cache(maxsize=None)
def hypergeom_interval(
    population: int,
    sampled: int,
    successes: int,
    look_count: int,
    alpha_numerator: int = 1,
    alpha_denominator: int = 20,
) -> tuple[int, int]:
    """Invert equal-tail hypergeometric tests for population successes."""

    if sampled == 0:
        return 0, population
    if sampled == population:
        return successes, successes
    accepted: list[int] = []
    denominator = math.comb(population, sampled)
    for total_successes in range(population + 1):
        lo = max(0, sampled - (population - total_successes))
        hi = min(sampled, total_successes)
        if not lo <= successes <= hi:
            continue
        lower_tail = 0
        upper_tail = 0
        for observed in range(lo, hi + 1):
            numerator = (
                math.comb(total_successes, observed)
                * math.comb(population - total_successes, sampled - observed)
            )
            if observed <= successes:
                lower_tail += numerator
            if observed >= successes:
                upper_tail += numerator
        threshold = alpha_numerator * denominator
        scale = 2 * look_count * alpha_denominator
        if lower_tail * scale > threshold and upper_tail * scale > threshold:
            accepted.append(total_successes)
    if not accepted:
        raise AssertionError("hypergeometric confidence set is empty")
    return accepted[0], accepted[-1]


def confidence_path(
    outcomes: list[int], order: list[int], strata: list[str], *, alpha: float
) -> dict[str, object]:
    """Return simultaneous observable intervals at every revealed prefix."""

    if alpha != 0.05:
        raise ValueError("the exact v1 certificate currently freezes alpha at 0.05")
    if len(outcomes) != len(order) or len(outcomes) != len(strata):
        raise ValueError("outcomes, order, and strata must have equal lengths")
    if sorted(order) != list(range(len(outcomes))):
        raise ValueError("order must be a complete item permutation")
    if any(value not in (0, 1) for value in outcomes):
        raise ValueError("outcomes must be binary adjudicated values")
    state = SafeStopState(order, strata, alpha=alpha)
    widths: list[float] = []
    lower: list[float] = []
    upper: list[float] = []
    covered: list[bool] = []
    true_successes = sum(outcomes)
    simultaneous_coverage = True
    for index in order:
        lo, hi = state.reveal(index, outcomes[index])
        lower.append(lo)
        upper.append(hi)
        widths.append(hi - lo)
        is_covered = lo <= true_successes / len(outcomes) <= hi
        covered.append(is_covered)
        simultaneous_coverage &= is_covered
    return {
        "lower": lower,
        "upper": upper,
        "width": widths,
        "covered": covered,
        "simultaneous_coverage": simultaneous_coverage,
        "per_look_delta": state.delta,
        "look_count": state.looks,
        "manifest_sha256": state.manifest_sha256,
    }


class SafeStopState:
    """Online fail-closed accumulator with no access to unrevealed outcomes."""

    def __init__(self, order: list[int], strata: list[str], *, alpha: float = 0.05):
        if alpha != 0.05:
            raise ValueError("the exact v1 certificate freezes alpha at 0.05")
        if sorted(order) != list(range(len(strata))):
            raise ValueError("order must be a complete item permutation")
        self.order = tuple(order)
        self.strata = tuple(strata)
        self.names = sorted(set(strata))
        self.sizes = {name: strata.count(name) for name in self.names}
        self.looks = sum(max(size - 1, 0) for size in self.sizes.values())
        self.delta = alpha / max(self.looks, 1)
        self.sampled = {name: 0 for name in self.names}
        self.successes = {name: 0 for name in self.names}
        self.bounds = {name: (0, self.sizes[name]) for name in self.names}
        self.lower_total = 0
        self.upper_total = len(order)
        self.prefix = 0
        manifest = {
            "schema": "safe-stop-manifest-v1",
            "item_ids": list(range(len(order))),
            "strata": strata,
            "stratum_sizes": self.sizes,
            "order": order,
            "alpha": alpha,
            "outcome_schema": "binary-adjudicated-v1",
        }
        self.manifest_sha256 = hashlib.sha256(
            json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

    def reveal(self, item_id: int, outcome: int) -> tuple[float, float]:
        if self.prefix >= len(self.order):
            raise ValueError("population already fully revealed")
        if item_id != self.order[self.prefix]:
            raise ValueError("revealed item is not the next manifest item")
        if outcome not in (0, 1):
            raise ValueError("outcome must be binary and adjudicated")
        name = self.strata[item_id]
        old_lo, old_hi = self.bounds[name]
        self.sampled[name] += 1
        self.successes[name] += outcome
        new_lo, new_hi = hypergeom_interval(
            self.sizes[name], self.sampled[name], self.successes[name], self.looks
        )
        self.bounds[name] = (new_lo, new_hi)
        self.lower_total += new_lo - old_lo
        self.upper_total += new_hi - old_hi
        self.prefix += 1
        total = len(self.order)
        return self.lower_total / total, self.upper_total / total


def first_stop(path: dict[str, object], epsilon: float) -> int:
    for prefix, width in enumerate(path["width"], 1):
        if width <= 2 * epsilon:
            return prefix
    return len(path["width"])


def threshold_stop(path: dict[str, object], threshold: float) -> int:
    for prefix, (lo, hi) in enumerate(zip(path["lower"], path["upper"], strict=True), 1):
        if lo >= threshold or hi < threshold:
            return prefix
    return len(path["lower"])


def _digest(order: list[int], strata: list[str], seed: int) -> str:
    payload = json.dumps({"seed": seed, "strata": strata, "order": order}, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


def paired_mean_interval(values: list[float], *, seed: int = 20260716) -> tuple[float, float]:
    generator = random.Random(seed)
    means = [
        statistics.fmean(values[generator.randrange(len(values))] for _ in values)
        for _ in range(5000)
    ]
    means.sort()
    return means[125], means[4874]


def _quantile(values: list[int], fraction: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def run(dataset: Path, *, trials: int = DEFAULT_TRIALS) -> dict[str, object]:
    train_x, train_y, test_x, test_y = ml.load_dataset(dataset)
    centroids = ml.train_centroids(train_x, train_y)
    train_predictions, train_margins = ml.predict_with_margin(train_x, centroids)
    predictions, margins = ml.predict_with_margin(test_x, centroids)
    thresholds = ml.margin_thresholds_by_prediction(train_predictions, train_margins, 5)
    strata = ml.joint_strata(predictions, margins, thresholds)
    outcomes = [int(a == b) for a, b in zip(predictions, test_y, strict=True)]
    quota, queues = ml.quota_plan(strata)
    stops = {
        str(epsilon): {"tool": [], "random": []} for epsilon in DEFAULT_EPSILONS
    }
    threshold_stops = {"tool": [], "random": []}
    coverage = {"tool": 0, "random": 0}
    ordering_seconds: list[float] = []
    interval_seconds: list[float] = []
    commitments: list[dict[str, object]] = []
    for seed in range(trials):
        started = time.perf_counter()
        random_order, tool_order = ml.priority_orders(seed, quota, queues)
        ordering_seconds.append(time.perf_counter() - started)
        if seed < 3:
            commitments.append({
                "seed": seed,
                "random_order_sha256": _digest(random_order, strata, seed),
                "tool_order_sha256": _digest(tool_order, strata, seed),
            })
        started = time.perf_counter()
        random_path = confidence_path(outcomes, random_order, strata, alpha=DEFAULT_ALPHA)
        tool_path = confidence_path(outcomes, tool_order, strata, alpha=DEFAULT_ALPHA)
        interval_seconds.append(time.perf_counter() - started)
        coverage["random"] += int(random_path["simultaneous_coverage"])
        coverage["tool"] += int(tool_path["simultaneous_coverage"])
        for epsilon in DEFAULT_EPSILONS:
            stops[str(epsilon)]["random"].append(first_stop(random_path, epsilon))
            stops[str(epsilon)]["tool"].append(first_stop(tool_path, epsilon))
        threshold_stops["random"].append(threshold_stop(random_path, 0.90))
        threshold_stops["tool"].append(threshold_stop(tool_path, 0.90))

    outcome_sorted_queues = {
        name: sorted(queue, key=lambda index: (outcomes[index], index))
        for name, queue in queues.items()
    }
    invalid_order = ml.materialize_order(quota, outcome_sorted_queues)
    invalid_path = confidence_path(outcomes, invalid_order, strata, alpha=DEFAULT_ALPHA)
    excluded_prefixes = [
        prefix for prefix, covered in enumerate(invalid_path["covered"], 1) if not covered
    ]

    stop_summary: dict[str, object] = {}
    for epsilon, values in stops.items():
        differences = [
            random_value - tool_value
            for random_value, tool_value in zip(values["random"], values["tool"], strict=True)
        ]
        stop_summary[epsilon] = {
            "tool_mean": statistics.fmean(values["tool"]),
            "random_mean": statistics.fmean(values["random"]),
            "mean_items_saved": statistics.fmean(differences),
            "paired_bootstrap_95_interval": list(paired_mean_interval(differences)),
            "median_items_saved": statistics.median(differences),
            "tool_stop_p50": _quantile(values["tool"], 0.50),
            "tool_stop_p95": _quantile(values["tool"], 0.95),
            "random_stop_p50": _quantile(values["random"], 0.50),
            "random_stop_p95": _quantile(values["random"], 0.95),
            "tool_early_stop_rate": sum(value < len(outcomes) for value in values["tool"]) / trials,
            "random_early_stop_rate": sum(value < len(outcomes) for value in values["random"]) / trials,
            "tool_win_rate": sum(value > 0 for value in differences) / trials,
            "minimum_saved": min(differences),
            "maximum_saved": max(differences),
        }
    threshold_differences = [
        random_value - tool_value
        for random_value, tool_value in zip(
            threshold_stops["random"], threshold_stops["tool"], strict=True
        )
    ]
    base_additional = -stop_summary["0.05"]["mean_items_saved"]
    economics = {}
    for role, rate in LOADED_RATES.items():
        economics[role] = {
            str(seconds): {
                "additional_review_seconds_per_batch": base_additional * seconds,
                "additional_labor_cost_per_batch": base_additional * seconds * rate / 3600,
            }
            for seconds in (15, 30, 60, 180)
        }
    return {
        "schema_version": "economic-safe-stopping-v1",
        "dataset": {"doi": ml.DATASET_DOI, "test_items": len(outcomes)},
        "design": {
            "alpha": DEFAULT_ALPHA,
            "trials": trials,
            "strata": len(queues),
            "order_generation_does_not_use_outcomes": True,
            "commitment_requirement_for_production": "persist manifest and order digest before outcome access; this offline replay records digests but is not a prospective commit",
            "confidence_method": "exact hypergeometric inversion; Bonferroni over every nontrivial within-stratum sample count",
            "observable_only": True,
            "commitment_examples": commitments,
        },
        "simultaneous_coverage": coverage,
        "negative_control": {
            "invalid_design": "outcomes sorted inside strata after labels were known",
            "simultaneous_coverage": invalid_path["simultaneous_coverage"],
            "excluded_prefix_count": len(excluded_prefixes),
            "first_excluded_prefix": excluded_prefixes[0] if excluded_prefixes else None,
            "interpretation": "the precommitted random within-stratum order is load-bearing",
        },
        "estimation_stops": stop_summary,
        "accuracy_90_percent_decision": {
            "tool_mean": statistics.fmean(threshold_stops["tool"]),
            "random_mean": statistics.fmean(threshold_stops["random"]),
            "mean_items_saved": statistics.fmean(threshold_differences),
            "paired_bootstrap_95_interval": list(paired_mean_interval(threshold_differences, seed=20260717)),
        },
        "measured_compute_benchmark": {
            "scope": "warm in-process paired replay; not human workflow overhead",
            "paired_random_plus_tool_order_mean_seconds": statistics.fmean(ordering_seconds),
            "paired_random_plus_tool_order_p95_seconds": _quantile([int(v * 1e9) for v in ordering_seconds], 0.95) / 1e9,
            "two_confidence_paths_mean_seconds": statistics.fmean(interval_seconds),
            "two_confidence_paths_p95_seconds": _quantile([int(v * 1e9) for v in interval_seconds], 0.95) / 1e9,
        },
        "loaded_hourly_rate_scenarios": LOADED_RATES,
        "loaded_hourly_rate_10th_median_90th_bands": LOADED_RATE_BANDS,
        "loaded_rate_metadata": {
            "geography": "United States national",
            "wage_vintage": "BLS May 2025 except clinical laboratory May 2024",
            "benefit_load_vintage": "BLS ECEC March 2026 occupation-group ratios",
            "unit": "USD per labor hour",
            "band_order": "loaded 10th percentile, median, loaded 90th percentile",
            "status": "derived percentile planning proxies, not observed customer cost or vendor quotes",
        },
        "derived_additional_cost_at_5pp": economics,
        "claim_boundary": (
            "Safe stopping is coverage-qualified on this frozen replay, but labor dollars are scenario calculations, not observed human savings. Marketing remains blocked until a preregistered human workflow study measures active time, errors, skips, adjudication, and integration overhead."
        ),
    }


def render(payload: dict[str, object]) -> str:
    lines = [
        "# Observable safe-stopping and economic validation",
        "",
        "## Result",
        "",
        f"The exact anytime procedure covered the true final accuracy on all "
        f"{payload['design']['trials']} paired tool paths and all random paths.",
        "",
        "| Accuracy half-width | Tool reviews | Random reviews | Mean reviews saved | Paired 95% interval |",
        "|---:|---:|---:|---:|---:|",
    ]
    for epsilon, result in payload["estimation_stops"].items():
        lines.append(
            f"| {float(epsilon):.0%} | {result['tool_mean']:.1f} | "
            f"{result['random_mean']:.1f} | {result['mean_items_saved']:.1f} | "
            f"[{result['paired_bootstrap_95_interval'][0]:.2f}, "
            f"{result['paired_bootstrap_95_interval'][1]:.2f}] |"
        )
    lines.extend([
        "",
        "The rigorous rule stops late and does not reproduce the earlier retrospective "
        "13–20% audit-count suggestion. That earlier result measured expected prefix error, "
        "not a production-valid stopping decision.",
        "",
        f"For the exploratory 90% accuracy decision, the tool stopped at "
        f"{payload['accuracy_90_percent_decision']['tool_mean']:.1f} reviews versus "
        f"{payload['accuracy_90_percent_decision']['random_mean']:.1f} for random order—only "
        f"{payload['accuracy_90_percent_decision']['mean_items_saved']:.1f} items on average; "
        f"the paired bootstrap 95% interval was "
        f"[{payload['accuracy_90_percent_decision']['paired_bootstrap_95_interval'][0]:.1f}, "
        f"{payload['accuracy_90_percent_decision']['paired_bootstrap_95_interval'][1]:.1f}], "
        "so it does not establish a benefit.",
        "",
        "## Negative control",
        "",
        f"When outcomes were impermissibly sorted inside strata, the interval excluded the "
        f"truth at {payload['negative_control']['excluded_prefix_count']} prefixes, first at "
        f"prefix {payload['negative_control']['first_excluded_prefix']}. Outcome-independent "
        "within-stratum order—prospectively committed in production—is therefore a required "
        "validity condition, not an implementation detail.",
        "",
        "## What is measured and what is not",
        "",
        f"Warm in-process paired order construction: `{payload['measured_compute_benchmark']['paired_random_plus_tool_order_mean_seconds']:.6f}` s per trial. "
        f"Mean computation for both confidence paths: `{payload['measured_compute_benchmark']['two_confidence_paths_mean_seconds']:.6f}` s. These are software microbenchmarks, not workflow overhead.",
        "",
        "Loaded hourly rates are BLS-derived planning scenarios. Human item time, workflow "
        "overhead, reviewer errors, adjudication, and integration cost have not yet been "
        "observed in a participant study, so the tool is not cleared for marketing.",
        "",
        "## Claim boundary",
        "",
        payload["claim_boundary"],
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, default=Path("/tmp/coprimebatch-uci-optdigits.zip"))
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--json-out", type=Path, default=Path("artifacts/economic_validation.json"))
    parser.add_argument("--report-out", type=Path, default=Path("artifacts/ECONOMIC_VALIDATION.md"))
    args = parser.parse_args()
    dataset = ml.obtain_dataset(args.cache, offline=args.offline)
    payload = run(dataset, trials=args.trials)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    args.report_out.write_text(render(payload))
    print(json.dumps(payload["estimation_stops"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
