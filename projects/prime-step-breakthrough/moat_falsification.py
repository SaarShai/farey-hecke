#!/usr/bin/env python3
"""Retrospective moat test against a simple proportional-deficit baseline.

The experiment reuses frozen, outcome-blind strata and revealed outcomes from
the prospective UCI and NetEaseCrowd pilots.  For every trial it assigns the
same pre-outcome random priority to each item, then compares:

* a global seeded shuffle;
* a simple proportional-deficit interleaving; and
* the certified quota category schedule.

The deficit baseline is intentionally easy to reproduce.  The experiment tests
algorithmic marginal value over cheap ordering substitutes; it does not test
customer willingness to pay or human-time savings.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import statistics
from typing import Any

from coprimebatch.prefix_balance import quota_order, verify_quota_result


DEFAULT_TRIALS = 500
DEFAULT_BOOTSTRAPS = 2_000
MOAT_THRESHOLD = 0.10


def _priority(seed: int, item_id: str) -> str:
    return hashlib.sha256(f"moat-v1|{seed}|{item_id}".encode("ascii")).hexdigest()


def proportional_deficit_schedule(counts: dict[str, int]) -> list[str]:
    """Return a transparent largest-entitlement-deficit category schedule."""

    if not counts or any(count <= 0 for count in counts.values()):
        raise ValueError("counts must be non-empty and positive")
    categories = sorted(counts)
    rank = {category: index for index, category in enumerate(categories)}
    total = sum(counts.values())
    used = Counter[str]()
    schedule: list[str] = []
    for prefix in range(1, total + 1):
        eligible = [category for category in categories if used[category] < counts[category]]
        category = max(
            eligible,
            key=lambda candidate: (
                Fraction(prefix * counts[candidate], total) - used[candidate],
                -rank[candidate],
            ),
        )
        schedule.append(category)
        used[category] += 1
    return schedule


def quota_schedule(counts: dict[str, int]) -> tuple[list[str], dict[str, Any]]:
    result = quota_order(counts)
    verification = verify_quota_result(result)
    if not verification.passed:
        raise RuntimeError(f"quota certificate failed: {verification.errors}")
    schedule = [result.categories[code] for code in result.order_codes]
    return schedule, {
        "algorithm": result.algorithm,
        "max_discrepancy": str(result.max_discrepancy),
        "lower_bound": str(result.lower_bound),
        "ratio_bound": str(result.ratio_bound) if result.ratio_bound is not None else None,
        "order_sha256": result.order_sha256,
    }


def materialize(schedule: list[str], queues: dict[str, list[int]]) -> list[int]:
    positions = Counter[str]()
    order: list[int] = []
    for category in schedule:
        position = positions[category]
        order.append(queues[category][position])
        positions[category] += 1
    return order


def max_prefix_discrepancy(schedule: list[str], counts: dict[str, int]) -> Fraction:
    total = len(schedule)
    used = Counter[str]()
    maximum = Fraction(0)
    for prefix, category in enumerate(schedule, 1):
        used[category] += 1
        maximum = max(
            maximum,
            *(
                abs(Fraction(used[candidate]) - Fraction(prefix * count, total))
                for candidate, count in counts.items()
            ),
        )
    return maximum


def prefix_metrics(outcomes: list[int], order: list[int], warmup: int) -> dict[str, float | int]:
    final_mean = statistics.fmean(outcomes)
    running = 0
    absolute: list[float] = []
    squared: list[float] = []
    for prefix, index in enumerate(order, 1):
        running += outcomes[index]
        error = running / prefix - final_mean
        absolute.append(abs(error))
        squared.append(error * error)
    if not 1 <= warmup <= len(order):
        raise ValueError("warmup must lie within the workload")
    violations = [index for index, value in enumerate(absolute, 1) if value > 0.01]
    return {
        "integrated_absolute_error": statistics.fmean(absolute[warmup - 1 :]),
        "integrated_squared_error": statistics.fmean(squared[warmup - 1 :]),
        "one_percent_settling_prefix": violations[-1] + 1 if violations else 1,
    }


def _load_workload(pilot_dir: Path) -> dict[str, Any]:
    freeze = json.loads((pilot_dir / "freeze.json").read_text(encoding="utf-8"))
    result = json.loads((pilot_dir / "result.json").read_text(encoding="utf-8"))
    items = freeze["items"]
    revealed = {item["item_id"]: int(item["correct"]) for item in result["revealed_items"]}
    item_ids = [str(item["item_id"]) for item in items]
    if set(item_ids) != set(revealed):
        raise ValueError(f"freeze/reveal item mismatch in {pilot_dir}")
    if all("stratum" in item for item in items):
        strata = [str(item["stratum"]) for item in items]
    elif all("taskset_id" in item for item in items):
        strata = [str(item["taskset_id"]) for item in items]
    else:
        raise ValueError(f"no supported pre-outcome stratum field in {pilot_dir}")
    index = {item_id: position for position, item_id in enumerate(item_ids)}
    production = [index[item_id] for item_id in freeze["orders"]["production"]["item_ids"]]
    return {
        "pilot_id": freeze["pilot_id"],
        "item_ids": item_ids,
        "strata": strata,
        "outcomes": [revealed[item_id] for item_id in item_ids],
        "production": production,
        "warmup": int(freeze["analysis_preregistration"]["warmup"]),
    }


def _bootstrap_reduction(
    tool: list[float], baseline: list[float], *, replicates: int, seed: int
) -> list[float]:
    generator = random.Random(seed)
    count = len(tool)
    values: list[float] = []
    for _ in range(replicates):
        indices = [generator.randrange(count) for _ in range(count)]
        tool_mean = statistics.fmean(tool[index] for index in indices)
        baseline_mean = statistics.fmean(baseline[index] for index in indices)
        values.append(1.0 - tool_mean / baseline_mean)
    values.sort()
    return [values[int(0.025 * replicates)], values[int(0.975 * replicates)]]


def _comparison(
    quota_values: list[float], baseline_values: list[float], *, bootstraps: int, seed: int
) -> dict[str, Any]:
    quota_mean = statistics.fmean(quota_values)
    baseline_mean = statistics.fmean(baseline_values)
    return {
        "quota_mean": quota_mean,
        "baseline_mean": baseline_mean,
        "quota_relative_reduction": 1.0 - quota_mean / baseline_mean,
        "bootstrap_95_interval": _bootstrap_reduction(
            quota_values, baseline_values, replicates=bootstraps, seed=seed
        ),
        "quota_win_rate": statistics.fmean(
            float(tool < baseline)
            for tool, baseline in zip(quota_values, baseline_values, strict=True)
        ),
    }


def run_workload(pilot_dir: Path, *, trials: int, bootstraps: int) -> dict[str, Any]:
    workload = _load_workload(pilot_dir)
    item_ids = workload["item_ids"]
    strata = workload["strata"]
    outcomes = workload["outcomes"]
    counts = dict(Counter(strata))
    quota_categories, certificate = quota_schedule(counts)
    deficit_categories = proportional_deficit_schedule(counts)
    values = {name: [] for name in ("seeded_random", "proportional_deficit", "quota")}
    settling = {name: [] for name in values}
    base_queues: dict[str, list[int]] = defaultdict(list)
    for index, category in enumerate(strata):
        base_queues[category].append(index)
    for seed in range(trials):
        priorities = [_priority(seed, item_id) for item_id in item_ids]
        random_order = sorted(range(len(item_ids)), key=lambda index: (priorities[index], index))
        queues = {
            category: sorted(queue, key=lambda index: (priorities[index], index))
            for category, queue in base_queues.items()
        }
        orders = {
            "seeded_random": random_order,
            "proportional_deficit": materialize(deficit_categories, queues),
            "quota": materialize(quota_categories, queues),
        }
        for name, order in orders.items():
            metrics = prefix_metrics(outcomes, order, workload["warmup"])
            values[name].append(float(metrics["integrated_absolute_error"]))
            settling[name].append(int(metrics["one_percent_settling_prefix"]))
    comparisons = {
        "vs_seeded_random": _comparison(
            values["quota"], values["seeded_random"], bootstraps=bootstraps, seed=71
        ),
        "vs_proportional_deficit": _comparison(
            values["quota"], values["proportional_deficit"], bootstraps=bootstraps, seed=73
        ),
    }
    supported = all(
        comparison["bootstrap_95_interval"][0] >= MOAT_THRESHOLD
        for comparison in comparisons.values()
    )
    return {
        "pilot_id": workload["pilot_id"],
        "items": len(item_ids),
        "strata": len(counts),
        "trials": trials,
        "warmup": workload["warmup"],
        "production_metrics": prefix_metrics(
            outcomes, workload["production"], workload["warmup"]
        ),
        "category_schedules": {
            "quota": {
                **certificate,
                "max_prefix_discrepancy": str(max_prefix_discrepancy(quota_categories, counts)),
            },
            "proportional_deficit": {
                "algorithm": "largest proportional entitlement deficit",
                "max_prefix_discrepancy": str(
                    max_prefix_discrepancy(deficit_categories, counts)
                ),
            },
        },
        "mean_metrics": {
            name: {
                "integrated_absolute_error": statistics.fmean(metric_values),
                "one_percent_settling_prefix": statistics.fmean(settling[name]),
            }
            for name, metric_values in values.items()
        },
        "comparisons": comparisons,
        "ordering_moat_supported": supported,
    }


def run(*, trials: int, bootstraps: int, pilot_dirs: list[Path]) -> dict[str, Any]:
    workloads = [
        run_workload(path, trials=trials, bootstraps=bootstraps) for path in pilot_dirs
    ]
    return {
        "schema": "prefix-balance-moat-falsification-v1",
        "preregistered_primary_metric": "mean integrated absolute prefix error after frozen warmup",
        "decision_rule": (
            "ordering moat is supported only if quota improves at least 10% over both seeded "
            "random and proportional-deficit baselines, with the paired bootstrap 95% lower "
            "bound at or above 10%, on every workload"
        ),
        "claim_boundary": (
            "Retrospective algorithmic moat test on previously revealed public data; does not "
            "establish customer demand, human-time savings, safe stopping, or monetary value."
        ),
        "workloads": workloads,
        "overall_ordering_moat_supported": all(
            workload["ordering_moat_supported"] for workload in workloads
        ),
    }


def render_report(payload: dict[str, Any]) -> str:
    lines = [
        "# Prefix-balance ordering moat falsification",
        "",
        f"Decision rule: {payload['decision_rule']}",
        "",
    ]
    for workload in payload["workloads"]:
        lines.extend(
            [
                f"## {workload['pilot_id']}",
                "",
                f"Items: **{workload['items']}**; strata: **{workload['strata']}**; "
                f"paired trials: **{workload['trials']}**.",
                "",
                "| Order | Mean integrated absolute error | Mean 1% settling prefix |",
                "|---|---:|---:|",
            ]
        )
        for name, metrics in workload["mean_metrics"].items():
            lines.append(
                f"| {name} | {metrics['integrated_absolute_error']:.8f} | "
                f"{metrics['one_percent_settling_prefix']:.1f} |"
            )
        lines.extend(["", "| Comparison | Quota reduction | 95% interval | Win rate |", "|---|---:|---:|---:|"])
        for name, comparison in workload["comparisons"].items():
            low, high = comparison["bootstrap_95_interval"]
            lines.append(
                f"| {name} | {comparison['quota_relative_reduction']:.1%} | "
                f"[{low:.1%}, {high:.1%}] | {comparison['quota_win_rate']:.1%} |"
            )
        lines.extend(
            [
                "",
                f"Ordering-moat gate: **{'PASS' if workload['ordering_moat_supported'] else 'FAIL'}**.",
                "",
            ]
        )
    lines.extend(
        [
            f"Overall ordering-moat gate: **{'PASS' if payload['overall_ordering_moat_supported'] else 'FAIL'}**.",
            "",
            payload["claim_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--bootstraps", type=int, default=DEFAULT_BOOTSTRAPS)
    parser.add_argument(
        "--pilot-dir",
        type=Path,
        action="append",
        dest="pilot_dirs",
        default=[],
        help="pilot directory containing freeze.json and result.json; repeatable",
    )
    parser.add_argument("--json-out", type=Path, default=Path("artifacts/moat_falsification.json"))
    parser.add_argument("--report-out", type=Path, default=Path("artifacts/MOAT_FALSIFICATION.md"))
    arguments = parser.parse_args()
    pilot_dirs = arguments.pilot_dirs or [
        Path("pilots/uci-optdigits-2026-08-01-label-blind-v2"),
        Path("pilots/neteasecrowd-human-annotation-2026-08-01"),
    ]
    payload = run(trials=arguments.trials, bootstraps=arguments.bootstraps, pilot_dirs=pilot_dirs)
    arguments.json_out.parent.mkdir(parents=True, exist_ok=True)
    arguments.report_out.parent.mkdir(parents=True, exist_ok=True)
    arguments.json_out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    arguments.report_out.write_text(render_report(payload), encoding="utf-8")
    print(render_report(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
