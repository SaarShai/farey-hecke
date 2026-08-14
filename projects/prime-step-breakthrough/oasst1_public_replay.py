#!/usr/bin/env python3
"""Zero-cash retrospective replay on the public OpenAssistant OASST1 corpus.

The experiment uses only fields available before a hypothetical offline review
(language, author role, and text length) to construct strata.  Human review
outcomes are revealed only for scoring.  Historical creation time is treated as
a chronological baseline, not as a claim about the unpublished annotation
queue.  ``review_count`` is an observed work-volume proxy, not elapsed time.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
import gzip
import hashlib
import json
from pathlib import Path
import random
import statistics
from typing import Any, Iterable
import urllib.request

from moat_falsification import (
    materialize,
    proportional_deficit_schedule,
    quota_schedule,
)


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_URL = (
    "https://huggingface.co/datasets/OpenAssistant/oasst1/resolve/main/"
    "2023-04-12_oasst_all.messages.jsonl.gz"
)
DATA_SHA256 = "2ff4aa8999c911ffec7972ddf70359f220b3da184b731f3649f68b1391e19341"
DEFAULT_DATA = PROJECT_ROOT / ".cache/oasst1/2023-04-12_oasst_all.messages.jsonl.gz"
CHECKPOINTS = (0.05, 0.10, 0.20, 0.30, 0.50)
OUTCOMES = ("rejection", "quality", "toxicity", "spam")
TRIALS = 200
BOOTSTRAPS = 2_000
SIGNAL_THRESHOLD = 0.10


@dataclass(frozen=True)
class Item:
    item_id: str
    created: datetime
    week: str
    stratum: str
    reviews: int
    outcomes: tuple[float, ...]


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def obtain_dataset(path: Path, *, offline: bool) -> Path:
    if path.exists():
        actual = sha256_path(path)
        if actual != DATA_SHA256:
            raise ValueError(f"OASST1 SHA-256 {actual} != pinned {DATA_SHA256}")
        return path
    if offline:
        raise FileNotFoundError(f"offline OASST1 cache missing: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(DATA_URL, timeout=120) as response:
        payload = response.read()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != DATA_SHA256:
        raise ValueError(f"downloaded OASST1 SHA-256 {actual} != pinned {DATA_SHA256}")
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_bytes(payload)
    temporary.replace(path)
    return path


def _length_band(text: str) -> str:
    size = len(text)
    if size < 200:
        return "short"
    if size < 600:
        return "medium"
    if size < 1_500:
        return "long"
    return "very-long"


def _label_value(labels: dict[str, Any], name: str) -> float | None:
    payload = labels.get(name)
    if not isinstance(payload, dict) or payload.get("value") is None:
        return None
    return float(payload["value"])


def parse_items(path: Path) -> tuple[list[Item], dict[str, int]]:
    if sha256_path(path) != DATA_SHA256:
        raise ValueError("OASST1 source does not match the pinned SHA-256")
    items: list[Item] = []
    census = Counter[str]()
    with gzip.open(path, "rt", encoding="utf-8") as source:
        for line in source:
            census["source_rows"] += 1
            row = json.loads(line)
            reviews = int(row.get("review_count") or 0)
            review_result = row.get("review_result")
            labels = row.get("labels") or {}
            values = tuple(
                value
                for value in (
                    None if review_result is None else float(not review_result),
                    _label_value(labels, "quality"),
                    _label_value(labels, "toxicity"),
                    _label_value(labels, "spam"),
                )
            )
            if reviews <= 0 or any(value is None for value in values):
                census["excluded_incomplete"] += 1
                continue
            created = datetime.fromisoformat(str(row["created_date"]))
            iso = created.isocalendar()
            language = str(row.get("lang") or "unknown")
            role = str(row.get("role") or "unknown")
            stratum = f"{language}|{role}|{_length_band(str(row.get('text') or ''))}"
            items.append(
                Item(
                    item_id=str(row["message_id"]),
                    created=created,
                    week=f"{iso.year}-W{iso.week:02d}",
                    stratum=stratum,
                    reviews=reviews,
                    outcomes=tuple(float(value) for value in values),
                )
            )
            census["eligible_rows"] += 1
    return items, dict(census)


def weekly_batches(items: Iterable[Item], *, minimum: int) -> dict[str, list[Item]]:
    batches: dict[str, list[Item]] = defaultdict(list)
    for item in items:
        batches[item.week].append(item)
    return {
        week: sorted(batch, key=lambda item: (item.created, item.item_id))
        for week, batch in sorted(batches.items())
        if len(batch) >= minimum
    }


def _priority(seed: int, item_id: str) -> str:
    return hashlib.sha256(f"oasst1-replay-v1|{seed}|{item_id}".encode("ascii")).hexdigest()


def checkpoint_metrics(items: list[Item], order: list[int]) -> dict[str, Any]:
    totals = tuple(statistics.fmean(item.outcomes[j] for item in items) for j in range(len(OUTCOMES)))
    checkpoints = sorted({max(1, round(len(items) * fraction)) for fraction in CHECKPOINTS})
    running = [0.0] * len(OUTCOMES)
    reviews = 0
    rows: list[dict[str, Any]] = []
    checkpoint_set = set(checkpoints)
    for prefix, index in enumerate(order, 1):
        item = items[index]
        reviews += item.reviews
        for outcome_index, value in enumerate(item.outcomes):
            running[outcome_index] += value
        if prefix in checkpoint_set:
            errors = [abs(running[j] / prefix - totals[j]) for j in range(len(OUTCOMES))]
            rows.append(
                {
                    "prefix": prefix,
                    "fraction": prefix / len(items),
                    "reviews": reviews,
                    "mean_absolute_error": statistics.fmean(errors),
                    "maximum_absolute_error": max(errors),
                    "outcome_errors": dict(zip(OUTCOMES, errors, strict=True)),
                }
            )
        if prefix >= checkpoints[-1]:
            break
    return {
        "checkpoint_mean_absolute_error": statistics.fmean(row["mean_absolute_error"] for row in rows),
        "checkpoint_maximum_absolute_error": max(row["maximum_absolute_error"] for row in rows),
        "reviews_to_one_percent_mean_error": next(
            (row["reviews"] for row in rows if row["mean_absolute_error"] <= 0.01),
            None,
        ),
        "checkpoints": rows,
    }


def _paired_interval(tool: list[float], baseline: list[float], *, seed: int) -> list[float]:
    generator = random.Random(seed)
    count = len(tool)
    values: list[float] = []
    for _ in range(BOOTSTRAPS):
        indices = [generator.randrange(count) for _ in range(count)]
        tool_mean = statistics.fmean(tool[index] for index in indices)
        baseline_mean = statistics.fmean(baseline[index] for index in indices)
        values.append(1.0 - tool_mean / baseline_mean)
    values.sort()
    return [values[int(0.025 * BOOTSTRAPS)], values[int(0.975 * BOOTSTRAPS)]]


def _comparison(tool: list[float], baseline: list[float], *, seed: int) -> dict[str, Any]:
    reduction = 1.0 - statistics.fmean(tool) / statistics.fmean(baseline)
    interval = _paired_interval(tool, baseline, seed=seed)
    return {
        "relative_reduction": reduction,
        "bootstrap_95_interval": interval,
        "win_rate": statistics.fmean(a < b for a, b in zip(tool, baseline, strict=True)),
        "passes_ten_percent_gate": reduction >= SIGNAL_THRESHOLD and interval[0] > 0,
    }


def _permuted_outcomes(items: list[Item], *, seed: int) -> list[Item]:
    outcomes = [item.outcomes for item in items]
    random.Random(seed).shuffle(outcomes)
    return [
        Item(item.item_id, item.created, item.week, item.stratum, item.reviews, outcome)
        for item, outcome in zip(items, outcomes, strict=True)
    ]


def run_batches(batches: dict[str, list[Item]], *, trials: int, permute: bool) -> dict[str, Any]:
    values = {name: [] for name in ("seeded_random", "proportional_deficit", "quota")}
    production_values: list[float] = []
    week_summaries: list[dict[str, Any]] = []
    for week_index, (week, source_items) in enumerate(batches.items()):
        items = _permuted_outcomes(source_items, seed=80_000 + week_index) if permute else source_items
        counts = dict(Counter(item.stratum for item in items))
        deficit_categories = proportional_deficit_schedule(counts)
        quota_categories, certificate = quota_schedule(counts)
        base_queues: dict[str, list[int]] = defaultdict(list)
        for index, item in enumerate(items):
            base_queues[item.stratum].append(index)
        production = checkpoint_metrics(items, list(range(len(items))))
        production_values.append(float(production["checkpoint_mean_absolute_error"]))
        per_week = {name: [] for name in values}
        for seed in range(trials):
            priorities = [_priority(seed, item.item_id) for item in items]
            queues = {
                category: sorted(queue, key=lambda index: (priorities[index], index))
                for category, queue in base_queues.items()
            }
            orders = {
                "seeded_random": sorted(range(len(items)), key=lambda index: (priorities[index], index)),
                "proportional_deficit": materialize(deficit_categories, queues),
                "quota": materialize(quota_categories, queues),
            }
            for name, order in orders.items():
                metric = float(checkpoint_metrics(items, order)["checkpoint_mean_absolute_error"])
                values[name].append(metric)
                per_week[name].append(metric)
        week_summaries.append(
            {
                "week": week,
                "items": len(items),
                "human_reviews": sum(item.reviews for item in items),
                "strata": len(counts),
                "production_checkpoint_mae": production["checkpoint_mean_absolute_error"],
                "mean_checkpoint_mae": {
                    name: statistics.fmean(observations) for name, observations in per_week.items()
                },
                "quota_certificate": certificate,
            }
        )
    comparisons = {
        "deficit_vs_random": _comparison(values["proportional_deficit"], values["seeded_random"], seed=101),
        "quota_vs_random": _comparison(values["quota"], values["seeded_random"], seed=103),
        "quota_vs_deficit": _comparison(values["quota"], values["proportional_deficit"], seed=107),
    }
    week_win_rates = {
        "deficit_vs_random": statistics.fmean(
            week["mean_checkpoint_mae"]["proportional_deficit"]
            < week["mean_checkpoint_mae"]["seeded_random"]
            for week in week_summaries
        ),
        "quota_vs_random": statistics.fmean(
            week["mean_checkpoint_mae"]["quota"] < week["mean_checkpoint_mae"]["seeded_random"]
            for week in week_summaries
        ),
    }
    return {
        "permuted_outcome_control": permute,
        "weeks": len(week_summaries),
        "trials_per_week": trials,
        "observations_per_method": len(values["seeded_random"]),
        "mean_checkpoint_mae": {name: statistics.fmean(observations) for name, observations in values.items()},
        "mean_production_checkpoint_mae": statistics.fmean(production_values),
        "descriptive_reduction_vs_creation_chronology": {
            name: 1.0 - statistics.fmean(observations) / statistics.fmean(production_values)
            for name, observations in values.items()
        },
        "comparisons": comparisons,
        "week_win_rates": week_win_rates,
        "week_summaries": week_summaries,
    }


def run(path: Path, *, trials: int, minimum_week: int) -> dict[str, Any]:
    items, census = parse_items(path)
    batches = weekly_batches(items, minimum=minimum_week)
    if len(batches) < 3:
        raise ValueError("fewer than three eligible weekly batches")
    observed = run_batches(batches, trials=trials, permute=False)
    control = run_batches(batches, trials=trials, permute=True)
    operational_signal = (
        observed["comparisons"]["deficit_vs_random"]["passes_ten_percent_gate"]
        and observed["week_win_rates"]["deficit_vs_random"] >= 0.70
        and not control["comparisons"]["deficit_vs_random"]["passes_ten_percent_gate"]
    )
    proprietary_signal = (
        observed["comparisons"]["quota_vs_deficit"]["passes_ten_percent_gate"]
        and operational_signal
    )
    return {
        "schema_version": "oasst1-public-replay-v1",
        "preregistered_before_replay": True,
        "source": {
            "name": "OpenAssistant OASST1",
            "url": DATA_URL,
            "sha256": DATA_SHA256,
            "license": "Apache-2.0",
        },
        "census": census,
        "design": {
            "batch": "ISO creation week; weeks with at least minimum_week eligible items",
            "minimum_week_items": minimum_week,
            "outcome_blind_strata": "language x role x text-length band",
            "outcomes": list(OUTCOMES),
            "checkpoints": list(CHECKPOINTS),
            "trials": trials,
            "bootstrap_replicates": BOOTSTRAPS,
            "signal_gate": "at least 10% reduction vs random, positive paired bootstrap lower bound, wins >=70% of weeks, negative control fails",
        },
        "observed": observed,
        "negative_control": control,
        "verdict": {
            "operational_ordering_signal": operational_signal,
            "proprietary_quota_signal": proprietary_signal,
            "product_demand_proven": False,
        },
        "claim_boundary": (
            "This retrospective replay tests early representativeness on real human-feedback records. "
            "Creation time is not annotation-queue time; review_count is work volume, not duration. "
            "It does not establish labor savings, causal deployment benefit, or willingness to pay."
        ),
    }


def render_report(payload: dict[str, Any]) -> str:
    observed = payload["observed"]
    control = payload["negative_control"]
    lines = [
        "# OASST1 public-data prefix replay",
        "",
        "## Verdict",
        "",
        f"- Operational ordering signal: **{'PASS' if payload['verdict']['operational_ordering_signal'] else 'FAIL'}**",
        f"- Proprietary quota signal: **{'PASS' if payload['verdict']['proprietary_quota_signal'] else 'FAIL'}**",
        "- Product demand proven: **NO**",
        "",
        "## Frozen corpus",
        "",
        f"- Source rows: {payload['census']['source_rows']:,}",
        f"- Eligible reviewed rows: {payload['census']['eligible_rows']:,}",
        f"- SHA-256: `{payload['source']['sha256']}`",
        f"- Weekly batches: {observed['weeks']}",
        f"- Paired trials per week: {observed['trials_per_week']}",
        "",
        "## Observed replay",
        "",
    ]
    for name, comparison in observed["comparisons"].items():
        interval = comparison["bootstrap_95_interval"]
        lines.append(
            f"- {name}: {comparison['relative_reduction']:.1%} reduction; "
            f"95% interval [{interval[0]:.1%}, {interval[1]:.1%}]; "
            f"paired win rate {comparison['win_rate']:.1%}."
        )
    lines.extend(["", "## Descriptive creation-chronology comparison", ""])
    for name, reduction in observed["descriptive_reduction_vs_creation_chronology"].items():
        lines.append(f"- {name}: {reduction:.1%} lower checkpoint error than creation chronology.")
    lines.append(
        "- This is not an annotation-queue comparison: OASST1 publishes creation time, not review-order time."
    )
    lines.extend(["", "## Global-permutation negative control", ""])
    for name, comparison in control["comparisons"].items():
        interval = comparison["bootstrap_95_interval"]
        lines.append(
            f"- {name}: {comparison['relative_reduction']:.1%} reduction; "
            f"95% interval [{interval[0]:.1%}, {interval[1]:.1%}]."
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            payload["claim_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--trials", type=int, default=TRIALS)
    parser.add_argument("--minimum-week", type=int, default=2_000)
    parser.add_argument("--json", type=Path, default=PROJECT_ROOT / "artifacts/oasst1_public_replay.json")
    parser.add_argument("--report", type=Path, default=PROJECT_ROOT / "artifacts/OASST1_PUBLIC_REPLAY.md")
    args = parser.parse_args()
    if args.trials < 10:
        parser.error("--trials must be at least 10")
    source = obtain_dataset(args.data, offline=args.offline)
    payload = run(source, trials=args.trials, minimum_week=args.minimum_week)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.report.write_text(render_report(payload), encoding="utf-8")
    print(json.dumps(payload["verdict"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
