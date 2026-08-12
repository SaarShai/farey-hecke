"""Small Levin-style probe: does local sorting transiently batch unrelated labels?

The task is only to sort numeric values. Labels are passive cargo and never enter
the transition rule. Same-label adjacency is therefore an evaluator diagnostic,
not an objective. The probe is deliberately modest: a positive result would be a
repeatable transient effect surviving label shuffles and schedule controls, not a
claim about agency.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import random
import statistics
from typing import Iterable


ROOT_SEED = 20260811
N = 24
LABELS = ("A", "B", "C")
RUNS = 256
RECEIPT = "bubble_batching_receipt.json"
RESULTS = "BUBBLE_BATCHING_RESULTS.md"


@dataclass(frozen=True)
class Run:
    values: tuple[int, ...]
    labels: tuple[str, ...]
    schedule: tuple[int, ...]
    goal_steps: int
    max_same_label_edges: int
    final_same_label_edges: int
    max_excess_edges: float


def _edges(labels: tuple[str, ...]) -> int:
    return sum(left == right for left, right in zip(labels, labels[1:]))


def _expected_edges(labels: tuple[str, ...]) -> float:
    counts = {label: labels.count(label) for label in LABELS}
    denominator = max(1, len(labels) - 1)
    return sum(count * (count - 1) for count in counts.values()) / max(1, len(labels))


def _swap(state: list[tuple[int, str]], index: int) -> None:
    state[index], state[index + 1] = state[index + 1], state[index]


def run_once(seed: int, *, label_shuffle: bool = False, randomized_schedule: bool = False) -> Run:
    rng = random.Random(seed)
    values = list(range(N))
    rng.shuffle(values)
    labels = [LABELS[index % len(LABELS)] for index in range(N)]
    rng.shuffle(labels)
    if label_shuffle:
        rng.shuffle(labels)
    state = list(zip(values, labels))
    order = list(range(N - 1))
    rng.shuffle(order)
    schedule: list[int] = []
    max_edges = _edges(tuple(labels))
    baseline = _expected_edges(tuple(labels))
    max_excess = max_edges - baseline
    while True:
        candidates = [i for i in order if state[i][0] > state[i + 1][0]]
        if not candidates:
            break
        index = rng.choice(candidates) if randomized_schedule else candidates[0]
        _swap(state, index)
        schedule.append(index)
        current = tuple(label for _, label in state)
        edges = _edges(current)
        max_edges = max(max_edges, edges)
        max_excess = max(max_excess, edges - _expected_edges(current))
        rng.shuffle(order)
    final_values = tuple(value for value, _ in state)
    final_labels = tuple(label for _, label in state)
    assert final_values == tuple(range(N))
    return Run(final_values, final_labels, tuple(schedule), len(schedule), max_edges, _edges(final_labels), max_excess)


def _summary(runs: Iterable[Run]) -> dict[str, float]:
    rows = list(runs)
    return {
        "runs": len(rows),
        "mean_goal_steps": statistics.fmean(row.goal_steps for row in rows),
        "mean_max_same_label_edges": statistics.fmean(row.max_same_label_edges for row in rows),
        "mean_final_same_label_edges": statistics.fmean(row.final_same_label_edges for row in rows),
        "mean_max_excess_edges": statistics.fmean(row.max_excess_edges for row in rows),
        "p_max_excess_positive": statistics.fmean(row.max_excess_edges > 0 for row in rows),
    }


def run_probe(output_dir: Path | None = None) -> dict[str, object]:
    normal = [run_once(ROOT_SEED + i) for i in range(RUNS)]
    shuffled = [run_once(ROOT_SEED + i, label_shuffle=True) for i in range(RUNS)]
    randomized = [run_once(ROOT_SEED + i, randomized_schedule=True) for i in range(RUNS)]
    # Zero-signal reference: it is an evaluator floor, not a fair solver.
    anti = [{**asdict(row), "max_excess_edges": 0.0} for row in normal]
    result: dict[str, object] = {
        "protocol": {
            "objective": "sort numeric values ascending",
            "labels_in_transition": False,
            "label_batching_is_required": False,
            "metric": "transient same-label adjacent edges above random-label expectation",
            "claim_boundary": "preliminary dynamical probe only; no agency or competency claim",
        },
        "config": {"seed": ROOT_SEED, "runs": RUNS, "N": N, "labels": LABELS},
        "summaries": {
            "stable_local_schedule": _summary(normal),
            "shuffled_labels": _summary(shuffled),
            "randomized_schedule": _summary(randomized),
            "zero_signal_reference": _summary(Run(**row) for row in anti),
        },
        "checks": {
            "all_sorted": all(row.values == tuple(range(N)) for row in normal + shuffled + randomized),
            "schedule_deterministic": normal == [run_once(ROOT_SEED + i) for i in range(RUNS)],
            "label_shuffle_changes_some_trace": any(a.labels != b.labels for a, b in zip(normal, shuffled)),
            "positive_preliminary_signal": False,
        },
    }
    stable = result["summaries"]["stable_local_schedule"]  # type: ignore[index]
    shuffled_summary = result["summaries"]["shuffled_labels"]  # type: ignore[index]
    result["checks"]["positive_preliminary_signal"] = bool(  # type: ignore[index]
        stable["mean_max_excess_edges"] > shuffled_summary["mean_max_excess_edges"] + 1.0  # type: ignore[index]
        and stable["p_max_excess_positive"] >= 0.8  # type: ignore[index]
    )
    result["sha256"] = sha256(json.dumps(result, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / RECEIPT).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (output_dir / RESULTS).write_text(result_markdown(result), encoding="utf-8")
    return result


def result_markdown(result: dict[str, object]) -> str:
    lines = ["# Bubble batching emergence probe", "", str(result["protocol"]["claim_boundary"]), "", "| condition | max excess edges | positive rate |", "| --- | ---: | ---: |"]
    for name, summary in result["summaries"].items():  # type: ignore[union-attr]
        lines.append(f"| {name} | {summary['mean_max_excess_edges']:.3f} | {summary['p_max_excess_positive']:.3f} |")
    lines.extend(["", f"All runs sorted: `{result['checks']['all_sorted']}`; preliminary signal: `{result['checks']['positive_preliminary_signal']}`.", "Labels are passive cargo; the task never rewards batching.", ""])
    return "\n".join(lines)


if __name__ == "__main__":
    run_probe(Path(__file__).resolve().parent)
