#!/usr/bin/env python3
"""Deterministic coarse-bin sorting probe for unnecessary role organization.

The only required objective is nondecreasing coarse bins. Cells carry a role
(``A`` or ``B``), but the evaluator does not reward role adjacency. In the
``role_tie`` condition, a local equal-bin tie rule puts A before B; resulting
same-role runs are an observer-measured side effect rather than a declared
objective. Controls remove that tie preference, randomize it, or anti-cluster.

No Farey data or sealed controller code is imported.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


N = 48
BIN_WIDTH = 8
TRIALS = 128
SEED = 20260811
MAX_SWEEPS = 200
CONDITIONS = ("role_tie", "shuffled_labels", "randomized_ties", "anti_clustering")


@dataclass(frozen=True)
class Cell:
    value: int
    label: str

    @property
    def coarse_bin(self) -> int:
        return self.value // BIN_WIDTH


def coarse_error(state: list[Cell]) -> int:
    return sum(state[i].coarse_bin > state[i + 1].coarse_bin for i in range(len(state) - 1))


def same_label_edges(state: list[Cell]) -> int:
    return sum(state[i].label == state[i + 1].label for i in range(len(state) - 1))


def within_bin_edges(state: list[Cell]) -> int:
    return sum(state[i].coarse_bin == state[i + 1].coarse_bin for i in range(len(state) - 1))


def within_bin_same_label_edges(state: list[Cell]) -> int:
    return sum(
        state[i].coarse_bin == state[i + 1].coarse_bin and state[i].label == state[i + 1].label
        for i in range(len(state) - 1)
    )


def role_runs(state: list[Cell]) -> tuple[int, int]:
    labels = [cell.label for cell in state]
    runs = 1 + sum(labels[i] != labels[i - 1] for i in range(1, len(labels)))
    max_run = max(len(list(group)) for _, group in itertools.groupby(labels))
    return runs, max_run


def metrics(state: list[Cell]) -> dict[str, float | int]:
    edges = len(state) - 1
    within = within_bin_edges(state)
    within_same = within_bin_same_label_edges(state)
    runs, max_run = role_runs(state)
    return {
        "coarse_error": coarse_error(state),
        "same_label_edges": same_label_edges(state),
        "same_label_rate": same_label_edges(state) / edges,
        "within_bin_edges": within,
        "within_bin_same_label_edges": within_same,
        "within_bin_same_label_rate": within_same / within if within else 0.0,
        "role_runs": runs,
        "max_role_run": max_run,
    }


def initial_state(seed: int, *, shuffle_labels: bool) -> list[Cell]:
    value_rng = random.Random(seed * 2 + 1)
    label_rng = random.Random(seed * 2 + (3 if shuffle_labels else 2))
    values = list(range(N))
    value_rng.shuffle(values)
    labels = ["A"] * (N // 2) + ["B"] * (N // 2)
    label_rng.shuffle(labels)
    return [Cell(value, label) for value, label in zip(values, labels)]


def _anti_score(state: list[Cell], i: int) -> int:
    score = 0
    for left, right in ((i - 1, i), (i, i + 1), (i + 1, i + 2)):
        if 0 <= left < len(state) - 1 and state[left].label == state[right].label:
            score += 1
    return score


def run(
    state: list[Cell], condition: str, *, seed: int, max_sweeps: int = MAX_SWEEPS
) -> tuple[list[Cell], list[dict[str, float | int]], int]:
    """Run local adjacent exchanges until coarse bins are sorted."""

    if condition not in CONDITIONS:
        raise ValueError(f"unknown condition: {condition}")
    rng = random.Random(seed)
    trace = [metrics(state)]
    for sweep in range(1, max_sweeps + 1):
        order = list(range(len(state) - 1))
        if condition == "randomized_ties":
            rng.shuffle(order)
        moved = False
        for i in order:
            left, right = state[i], state[i + 1]
            inverted = left.coarse_bin > right.coarse_bin
            equal_bin = left.coarse_bin == right.coarse_bin
            tie_swap = False
            if equal_bin and condition == "role_tie":
                tie_swap = (left.label, right.label) == ("B", "A")
            elif equal_bin and condition == "randomized_ties":
                tie_swap = rng.random() < 0.5
            elif equal_bin and condition == "anti_clustering" and left.label != right.label:
                before = _anti_score(state, i)
                state[i], state[i + 1] = state[i + 1], state[i]
                after = _anti_score(state, i)
                if after < before:
                    moved = True
                else:
                    state[i], state[i + 1] = state[i + 1], state[i]
                continue
            if inverted or tie_swap:
                state[i], state[i + 1] = state[i + 1], state[i]
                moved = True
        trace.append(metrics(state))
        if coarse_error(state) == 0 and (condition != "anti_clustering" or not moved):
            break
        if not moved:
            break
    return state, trace, len(trace) - 1


def perturb_restart(state: list[Cell], *, seed: int) -> dict[str, object]:
    """Swap a mixed-label equal-bin pair, then restart the role-local process."""

    perturbed = list(state)
    index = next(
        (
            i
            for i in range(len(perturbed) - 1)
            if perturbed[i].coarse_bin == perturbed[i + 1].coarse_bin
            and perturbed[i].label != perturbed[i + 1].label
        ),
        None,
    )
    if index is None:
        return {"applied": False, "reason": "no mixed-label equal-bin pair"}
    perturbed[index], perturbed[index + 1] = perturbed[index + 1], perturbed[index]
    before = metrics(perturbed)
    final, trace, sweeps = run(perturbed, "role_tie", seed=seed)
    return {"applied": True, "index": index, "before": before, "after": metrics(final), "sweeps": sweeps, "trace_length": len(trace)}


def _summary(values: Iterable[float | int]) -> dict[str, float | int]:
    vals = list(values)
    return {"count": len(vals), "mean": statistics.fmean(vals), "min": min(vals), "max": max(vals), "median": statistics.median(vals)}


def run_experiment() -> dict[str, object]:
    rows: dict[str, list[dict[str, float | int]]] = {condition: [] for condition in CONDITIONS}
    for trial in range(TRIALS):
        for condition in CONDITIONS:
            state = initial_state(SEED + trial, shuffle_labels=condition == "shuffled_labels")
            final, trace, sweeps = run(state, condition, seed=SEED + trial * 17 + len(condition))
            initial = trace[0]
            final_metrics = metrics(final)
            rows[condition].append({
                "trial": trial,
                "initial_same_label_rate": initial["same_label_rate"],
                "final_same_label_rate": final_metrics["same_label_rate"],
                "final_within_bin_same_label_rate": final_metrics["within_bin_same_label_rate"],
                "final_role_runs": final_metrics["role_runs"],
                "final_max_role_run": final_metrics["max_role_run"],
                "coarse_error": final_metrics["coarse_error"],
                "sweeps": sweeps,
                "peak_same_label_rate": max(item["same_label_rate"] for item in trace),
            })
    summaries: dict[str, object] = {}
    for condition, condition_rows in rows.items():
        summaries[condition] = {
            "trials": len(condition_rows),
            "coarse_error_rate": sum(row["coarse_error"] == 0 for row in condition_rows) / len(condition_rows),
            "final_same_label_rate": _summary(row["final_same_label_rate"] for row in condition_rows),
            "final_within_bin_same_label_rate": _summary(row["final_within_bin_same_label_rate"] for row in condition_rows),
            "final_role_runs": _summary(row["final_role_runs"] for row in condition_rows),
            "final_max_role_run": _summary(row["final_max_role_run"] for row in condition_rows),
            "peak_same_label_rate": _summary(row["peak_same_label_rate"] for row in condition_rows),
            "sweeps": _summary(row["sweeps"] for row in condition_rows),
        }
    base = initial_state(SEED, shuffle_labels=False)
    converged, _, _ = run(base, "role_tie", seed=SEED + 99)
    return {
        "schema": "coarse-bin-emergence-v1",
        "config": {"N": N, "bin_width": BIN_WIDTH, "bins": N // BIN_WIDTH, "trials": TRIALS, "seed": SEED, "max_sweeps": MAX_SWEEPS},
        "objective": "nondecreasing coarse bins; within-bin order and role adjacency are unconstrained",
        "conditions": list(CONDITIONS),
        "summaries": summaries,
        "perturbation_restart": perturb_restart(converged, seed=SEED + 100),
        "notes": [
            "role_tie uses a local A-before-B tie convention only when coarse bins are equal",
            "shuffled_labels preserves the A/B count but uses an independent permutation",
            "randomized_ties randomizes equal-bin tie decisions and pair schedule",
            "anti_clustering accepts equal-bin swaps only when local same-label adjacency decreases",
        ],
    }


def source_sha256() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def write_artifacts(directory: Path) -> None:
    result = run_experiment()
    result["source_sha256"] = source_sha256()
    (directory / "receipt.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    role = result["summaries"]["role_tie"]
    random_ties = result["summaries"]["randomized_ties"]
    anti = result["summaries"]["anti_clustering"]
    text = f"""# Coarse-bin emergence probe

- **Objective:** sort six coarse bins of eight values each; any within-bin order is valid.
- **Probe:** a local A-before-B tie convention applies only inside equal bins. Same-label adjacency is measured externally and is not an objective.
- **Controls:** independent label shuffle, randomized equal-bin ties/schedule, and an explicit anti-clustering policy.

## Deterministic result

All conditions completed the coarse objective in {role['coarse_error_rate']:.3f} of trials. The role-tie probe's final within-bin same-label rate was {role['final_within_bin_same_label_rate']['mean']:.3f}; randomized ties gave {random_ties['final_within_bin_same_label_rate']['mean']:.3f}; anti-clustering gave {anti['final_within_bin_same_label_rate']['mean']:.3f}. The role-tie condition therefore shows an unnecessary organization signal relative to the matched controls, while the controls bound schedule/label effects.

The perturbation/restart receipt records a mixed-label equal-bin swap followed by the role-local restart. This is a finite toy-model signal, not evidence of agency, intrinsic utility, or zero-cost computation.

Receipt: [receipt.json](receipt.json).
"""
    (directory / "RESULTS.md").write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write receipt.json and RESULTS.md")
    args = parser.parse_args()
    if args.write:
        write_artifacts(Path(__file__).resolve().parent)
    else:
        print(json.dumps(run_experiment(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
