#!/usr/bin/env python3
"""V3.1 reachability-only redesign: scale-free quarter-circle navigation.

Stage-0 found that the original four-action shell could be information-rich
yet unable to reach both hidden identities on many fixed eight-action tasks.
This module tests the smallest preregistered action-vocabulary repair: add two
target-independent cursor moves whose step is
``max(1, visible_point_count // 4)``.  No candidate list, target identity,
fraction, order, damage mask, or controller training is introduced.

The evaluator exhaustively searches every sequence in the six-action
vocabulary for the same Stage-0 manifest and budget.  It reports paired old
versus new ceilings, per-task witnesses, negative fixtures, and deterministic
source hashes.  A ceiling result is not a controller or competency claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import statistics
import sys
from typing import Any, Sequence

try:  # Package import.
    from .competency_v3_feasibility import (
        DEFAULT_CONFIG as STAGE0_CONFIG,
        _manifest as stage0_manifest,
        _hidden_repair_metrics,
        _task_environment,
        exact_reachability_ceiling as old_exact_reachability_ceiling,
    )
    from .repair_experiment import ACTION_BUDGET, POLICY_ACTIONS, RepairTask
    from .strict_environment import Action, DamagePattern, StrictEnvironment
except ImportError:  # Direct script execution from this directory.
    from competency_v3_feasibility import (  # type: ignore[no-redef]
        DEFAULT_CONFIG as STAGE0_CONFIG,
        _manifest as stage0_manifest,
        _hidden_repair_metrics,
        _task_environment,
        exact_reachability_ceiling as old_exact_reachability_ceiling,
    )
    from repair_experiment import ACTION_BUDGET, POLICY_ACTIONS, RepairTask  # type: ignore[no-redef]
    from strict_environment import Action, DamagePattern, StrictEnvironment  # type: ignore[no-redef]


SEED = STAGE0_CONFIG.seed
F1_THRESHOLD = 0.80
EXACT_THRESHOLD = 0.50
QUARTER_ACTIONS = ("move_left_quarter", "move_right_quarter")
NAVIGATION_ACTIONS = (*POLICY_ACTIONS, *QUARTER_ACTIONS)


@dataclass(frozen=True, slots=True)
class NavigationConfig:
    """Locked v3.1 protocol; the manifest is inherited byte-for-byte."""

    seed: int = SEED
    action_budget: int = ACTION_BUDGET
    f1_threshold: float = F1_THRESHOLD
    exact_threshold: float = EXACT_THRESHOLD
    negative_fixture_budget: int = 1

    def __post_init__(self) -> None:
        if self.action_budget != ACTION_BUDGET:
            raise ValueError("v3.1 keeps the fixed eight-action budget")
        if self.f1_threshold != F1_THRESHOLD or self.exact_threshold != EXACT_THRESHOLD:
            raise ValueError("v3.1 thresholds are locked before results")
        if self.negative_fixture_budget <= 0 or self.negative_fixture_budget >= self.action_budget:
            raise ValueError("negative fixture must use a strictly smaller positive budget")


DEFAULT_CONFIG = NavigationConfig()


@dataclass(frozen=True, slots=True)
class NavigationCeiling:
    max_precision: float
    max_recall: float
    max_f1: float
    max_exact_recovery: float
    best_f1_actions: tuple[str, ...]
    visited_states: int


@dataclass(frozen=True, slots=True)
class _Frontier:
    max_precision: float
    max_recall: float
    max_f1: float
    max_exact_recovery: float
    best_f1_actions: tuple[str, ...]


def quarter_step(visible_count: int) -> int:
    """Scale-free navigation stride based only on currently visible points."""

    if visible_count < 1:
        raise ValueError("visible_count must be positive")
    return max(1, visible_count // 4)


def _transition(
    state: tuple[tuple[Fraction, ...], int, int], action_text: str
) -> tuple[tuple[Fraction, ...], int, int]:
    """Pure fixed-action transition matching ``StrictEnvironment`` semantics."""

    points, cursor, remaining = state
    remaining -= 1
    if action_text == Action.MOVE_LEFT.value:
        return points, (cursor - 1) % len(points), remaining
    if action_text == Action.MOVE_RIGHT.value:
        return points, (cursor + 1) % len(points), remaining
    if action_text == QUARTER_ACTIONS[0]:
        return points, (cursor - quarter_step(len(points))) % len(points), remaining
    if action_text == QUARTER_ACTIONS[1]:
        return points, (cursor + quarter_step(len(points))) % len(points), remaining
    left = points[cursor]
    right = points[(cursor + 1) % len(points)]
    lifted_right = right if right > left else right + 1
    if action_text == Action.INSERT_MEDIANT.value:
        candidate = Fraction(left.numerator + lifted_right.numerator, left.denominator + lifted_right.denominator)
    elif action_text == Action.INSERT_MIDPOINT.value:
        candidate = (left + lifted_right) / 2
    else:
        raise ValueError(f"unsupported navigation action: {action_text}")
    candidate %= 1
    if candidate in points:
        return points, cursor, remaining
    updated = tuple(sorted((*points, candidate)))
    return updated, updated.index(candidate), remaining


def _witness_metrics(
    points: tuple[Fraction, ...],
    target: tuple[Fraction, ...],
    initial_points: tuple[Fraction, ...],
) -> tuple[float, float, float, float, int, int]:
    visible = set(points)
    target_set = set(target)
    initial_set = set(initial_points)
    deleted = target_set - initial_set
    additions = visible - initial_set
    true_positive = len(additions & deleted)
    false_positive = len(additions - target_set)
    precision = true_positive / len(additions) if additions else 0.0
    recall = true_positive / len(deleted) if deleted else 1.0
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    exact = float(visible == target_set)
    return precision, recall, f1, exact, true_positive, false_positive


def exact_navigation_ceiling(
    task: RepairTask, *, action_budget: int = ACTION_BUDGET
) -> NavigationCeiling:
    """Exhaustively maximize hidden repair metrics under six legal actions."""

    if action_budget != ACTION_BUDGET:
        raise ValueError("v3.1 ceiling must use the fixed eight-action budget")
    environment = _task_environment(task, "farey")
    target = tuple(environment._target)
    initial_points = tuple(environment._initial_points)
    initial_state = (initial_points, int(environment._initial_cursor), action_budget)
    cache: dict[tuple[Any, ...], _Frontier] = {}
    visited_states: set[tuple[Any, ...]] = set()

    def search(state: tuple[tuple[Fraction, ...], int, int]) -> _Frontier:
        points, cursor, remaining = state
        signature = (points, cursor, remaining)
        visited_states.add(signature)
        cached = cache.get(signature)
        if cached is not None:
            return cached
        if remaining <= 0:
            precision, recall, f1, exact, _, _ = _witness_metrics(points, target, initial_points)
            result = _Frontier(precision, recall, f1, exact, ())
            cache[signature] = result
            return result
        branches = [(action_text, search(_transition(state, action_text))) for action_text in NAVIGATION_ACTIONS]
        max_precision = max(frontier.max_precision for _, frontier in branches)
        max_recall = max(frontier.max_recall for _, frontier in branches)
        max_f1 = max(frontier.max_f1 for _, frontier in branches)
        max_exact = max(frontier.max_exact_recovery for _, frontier in branches)
        candidates = [(action_text, frontier) for action_text, frontier in branches if frontier.max_f1 == max_f1]
        action_text, selected = max(
            candidates,
            key=lambda item: (
                item[1].max_f1,
                item[1].max_exact_recovery,
                item[1].max_recall,
                item[1].max_precision,
                tuple(reversed(item[1].best_f1_actions)),
            ),
        )
        result = _Frontier(
            max_precision,
            max_recall,
            max_f1,
            max_exact,
            (action_text, *selected.best_f1_actions),
        )
        cache[signature] = result
        return result

    frontier = search(initial_state)
    return NavigationCeiling(
        frontier.max_precision,
        frontier.max_recall,
        frontier.max_f1,
        frontier.max_exact_recovery,
        frontier.best_f1_actions,
        len(visited_states),
    )


def _replay_witness(task: RepairTask, actions: Sequence[str]) -> dict[str, Any]:
    environment = _task_environment(task, "farey")
    points = tuple(environment._initial_points)
    cursor = int(environment._initial_cursor)
    state = (points, cursor, ACTION_BUDGET)
    cursor_trace = [cursor]
    insertion_count = 0
    movement_count = 0
    for action_text in actions:
        if action_text in {Action.INSERT_MEDIANT.value, Action.INSERT_MIDPOINT.value}:
            insertion_count += 1
        else:
            movement_count += 1
        state = _transition(state, action_text)
        cursor_trace.append(state[1])
    final_points, final_cursor, _ = state
    precision, recall, f1, exact, recovered, false_positive = _witness_metrics(
        final_points, tuple(environment._target), tuple(environment._initial_points)
    )
    return {
        "initial_cursor_index": cursor_trace[0],
        "final_cursor_index": final_cursor,
        "cursor_trace": cursor_trace,
        "movement_count": movement_count,
        "insertion_count": insertion_count,
        "quarter_move_count": sum(action in QUARTER_ACTIONS for action in actions),
        "actions_used": len(actions),
        "actions_remaining": ACTION_BUDGET - len(actions),
        "recovered_count": recovered,
        "false_positive_count": false_positive,
        "deleted_count": task.damage_count,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "exact_recovery": exact,
    }


def _negative_fixture(task: RepairTask, budget: int) -> dict[str, Any]:
    """Budget-starved navigation fixture; intentionally outside v3.1 protocol."""

    environment = StrictEnvironment(
        task.order,
        task.pattern,
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=budget,
        goal=task.goal,
    )
    target = tuple(environment._target)
    initial_points = tuple(environment._initial_points)
    initial_state = (initial_points, int(environment._initial_cursor), budget)
    cache: dict[tuple[Any, ...], float] = {}

    def search(state: tuple[tuple[Fraction, ...], int, int]) -> float:
        points, cursor, remaining = state
        key = (points, cursor, remaining)
        if key in cache:
            return cache[key]
        if remaining <= 0:
            value = _witness_metrics(points, target, initial_points)[2]
        else:
            value = max(search(_transition(state, action)) for action in NAVIGATION_ACTIONS)
        cache[key] = value
        return value

    value = search(initial_state)
    return {"action_budget": budget, "max_f1": value, "status": "negative" if value < F1_THRESHOLD else "unexpected_positive"}


def _gate(name: str, f1: float, exact: float, *, valid: bool, reason: str) -> dict[str, Any]:
    status = (
        "unverified"
        if not valid
        else "positive"
        if f1 >= F1_THRESHOLD and exact >= EXACT_THRESHOLD
        else "negative"
    )
    return {
        "name": name,
        "status": status,
        "valid": valid,
        "reason": reason,
        "f1": f1,
        "f1_threshold": F1_THRESHOLD,
        "exact_recovery": exact,
        "exact_threshold": EXACT_THRESHOLD,
    }


def _source_hashes() -> dict[str, str]:
    directory = Path(__file__).parent
    names = (
        "competency_v31_navigation.py",
        "competency_v3_feasibility.py",
        "repair_experiment.py",
        "strict_environment.py",
        "test_competency_v31_navigation.py",
    )
    return {
        name: sha256((directory / name).read_bytes()).hexdigest()
        for name in names
        if (directory / name).exists()
    }


def run_navigation(config: NavigationConfig = DEFAULT_CONFIG) -> dict[str, Any]:
    """Run old/new exact ceilings on the unchanged Stage-0 manifest."""

    if config.seed != STAGE0_CONFIG.seed:
        raise ValueError("v3.1 must use the identical Stage-0 manifest seed")
    tasks = stage0_manifest(STAGE0_CONFIG)
    old_rows: list[dict[str, Any]] = []
    new_rows: list[dict[str, Any]] = []
    paired: list[dict[str, Any]] = []
    for task in tasks:
        old = old_exact_reachability_ceiling(task)
        old_row = {
            "order": task.order,
            "pattern": task.pattern.value,
            "goal": task.goal.value,
            "seed": task.seed,
            "max_f1": old.max_f1,
            "max_exact_recovery": old.max_exact_recovery,
            "max_precision": old.max_precision,
            "max_recall": old.max_recall,
            "visited_states": old.visited_states,
            "best_f1_actions": list(old.best_f1_actions),
        }
        new = exact_navigation_ceiling(task)
        new_row = {
            "order": task.order,
            "pattern": task.pattern.value,
            "goal": task.goal.value,
            "seed": task.seed,
            "max_f1": new.max_f1,
            "max_exact_recovery": new.max_exact_recovery,
            "max_precision": new.max_precision,
            "max_recall": new.max_recall,
            "visited_states": new.visited_states,
            "best_f1_actions": list(new.best_f1_actions),
            "witness": _replay_witness(task, new.best_f1_actions),
        }
        old_rows.append(old_row)
        new_rows.append(new_row)
        paired.append(
            {
                "order": task.order,
                "pattern": task.pattern.value,
                "goal": task.goal.value,
                "seed": task.seed,
                "old_max_f1": old.max_f1,
                "new_max_f1": new.max_f1,
                "delta_max_f1": new.max_f1 - old.max_f1,
                "old_max_exact_recovery": old.max_exact_recovery,
                "new_max_exact_recovery": new.max_exact_recovery,
                "delta_max_exact_recovery": new.max_exact_recovery - old.max_exact_recovery,
            }
        )
    old_mean_f1 = statistics.fmean(row["max_f1"] for row in old_rows)
    new_mean_f1 = statistics.fmean(row["max_f1"] for row in new_rows)
    old_mean_exact = statistics.fmean(row["max_exact_recovery"] for row in old_rows)
    new_mean_exact = statistics.fmean(row["max_exact_recovery"] for row in new_rows)
    source_hashes = _source_hashes()
    if source_hashes != _source_hashes():
        raise RuntimeError("sources changed while v3.1 was running")
    fixture = _negative_fixture(tasks[0], config.negative_fixture_budget)
    return {
        "schema_version": 1,
        "experiment": "V3.1 exact reachability with scale-free quarter-circle cursor moves",
        "seed": config.seed,
        "provenance": {
            "command": "PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/competency_v31_navigation.py",
            "python": sys.version.split()[0],
            "controller_training": False,
        },
        "predeclaration": {
            "manifest_inherited_from": "competency_v3_feasibility.DEFAULT_CONFIG",
            "orders": list(STAGE0_CONFIG.representative_orders),
            "patterns": [pattern.value for pattern in STAGE0_CONFIG.representative_patterns],
            "goals": sorted({task.goal.value for task in tasks}),
            "damage_count": STAGE0_CONFIG.representative_damage_count,
            "replicates_per_cell": 1,
            "action_budget": ACTION_BUDGET,
            "old_actions": list(POLICY_ACTIONS),
            "new_actions": list(NAVIGATION_ACTIONS),
            "quarter_move_step": "max(1, visible_count // 4)",
            "f1_threshold": F1_THRESHOLD,
            "exact_recovery_threshold": EXACT_THRESHOLD,
            "negative_fixture_budget": config.negative_fixture_budget,
        },
        "old_ceiling": {
            "tasks": old_rows,
            "mean_max_f1": old_mean_f1,
            "mean_max_exact_recovery": old_mean_exact,
        },
        "new_ceiling": {
            "tasks": new_rows,
            "mean_max_f1": new_mean_f1,
            "mean_max_exact_recovery": new_mean_exact,
        },
        "paired_old_vs_new": {
            "tasks": paired,
            "mean_delta_max_f1": new_mean_f1 - old_mean_f1,
            "mean_delta_max_exact_recovery": new_mean_exact - old_mean_exact,
            "nonnegative_f1_task_count": sum(row["delta_max_f1"] >= 0.0 for row in paired),
            "strictly_improved_f1_task_count": sum(row["delta_max_f1"] > 0.0 for row in paired),
            "strictly_improved_exact_task_count": sum(row["delta_max_exact_recovery"] > 0.0 for row in paired),
        },
        "gates": {
            "navigation_reachability": _gate(
                "navigation_reachability",
                new_mean_f1,
                new_mean_exact,
                valid=len(tasks) == len(old_rows) == len(new_rows) == 18,
                reason="joint exact-ceiling thresholds locked before evaluation on the unchanged Stage-0 manifest",
            ),
            "negative_budget_fixture": {
                "name": "negative_budget_fixture",
                "status": fixture["status"],
                "valid": True,
                "reason": "same navigation vocabulary deliberately budget-starved to one action",
                "max_f1": fixture["max_f1"],
                "threshold": F1_THRESHOLD,
            },
        },
        "negative_fixtures": {"budget_starved": fixture},
        "source_hashes": source_hashes,
        "claim_boundary": (
            "This is an evaluator-only action-vocabulary feasibility result. "
            "Even a positive navigation ceiling would establish attainability, "
            "not feedback learning, hidden recovery by a controller, transfer, "
            "or a Levin-style competency."
        ),
    }


def _fmt(value: float) -> str:
    return f"{value:.4f}"


def result_markdown(result: dict[str, Any]) -> str:
    old = result["old_ceiling"]
    new = result["new_ceiling"]
    paired = result["paired_old_vs_new"]
    gate = result["gates"]["navigation_reachability"]
    lines = [
        "# V3.1 navigation-only reachability results",
        "",
        "This evaluator-only run keeps the Stage-0 manifest, eight-action budget, and four original actions unchanged. It adds only target-independent quarter-circle cursor moves.",
        "",
        "## Locked protocol",
        "",
        f"Original actions: `{result['predeclaration']['old_actions']}`. New actions: `{result['predeclaration']['new_actions']}`. Quarter stride: `{result['predeclaration']['quarter_move_step']}`. Manifest: orders `{result['predeclaration']['orders']}`, all three damage families, both goals, two deletions, one task per cell.",
        "",
        "## Paired exact ceilings",
        "",
        "| metric | old four-action | new six-action | paired change | locked threshold |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| mean max F1 | {_fmt(old['mean_max_f1'])} | {_fmt(new['mean_max_f1'])} | {_fmt(paired['mean_delta_max_f1'])} | {_fmt(F1_THRESHOLD)} |",
        f"| mean max exact recovery | {_fmt(old['mean_max_exact_recovery'])} | {_fmt(new['mean_max_exact_recovery'])} | {_fmt(paired['mean_delta_max_exact_recovery'])} | {_fmt(EXACT_THRESHOLD)} |",
        "",
        f"Joint navigation ceiling gate: **{gate['status']}**. Both new-celing component thresholds must pass; the result still says only that the environment is attainable for an evaluator with hidden state.",
        "",
        "## Task-level witness evidence",
        "",
        f"The exact search visited up to `{max(row['visited_states'] for row in new['tasks'])}` memoized states in a task. Every witness used all eight actions; the receipt records cursor trace, quarter moves, insertions, recovered identities, and false positives for each task.",
        "",
        "## Negative fixture",
        "",
        f"A one-action budget fixture reached max F1 `{_fmt(result['negative_fixtures']['budget_starved']['max_f1'])}` and is `{result['gates']['negative_budget_fixture']['status']}` against the locked `{_fmt(F1_THRESHOLD)}` threshold.",
        "",
        result["claim_boundary"],
        "",
    ]
    return "\n".join(lines)


def write_outputs(result: dict[str, Any]) -> None:
    directory = Path(__file__).parent
    (directory / "competency_v31_navigation_receipt.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (directory / "NAVIGATION_RESULTS.md").write_text(result_markdown(result), encoding="utf-8")


def main() -> None:
    result = run_navigation()
    write_outputs(result)
    print("wrote competency_v31_navigation_receipt.json and NAVIGATION_RESULTS.md")
    print(", ".join(f"{name}={gate['status']}" for name, gate in result["gates"].items()))


if __name__ == "__main__":
    main()
