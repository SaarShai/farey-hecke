#!/usr/bin/env python3
"""V3.2 evaluator-only closure test for hidden Farey repair.

V3.1 added scale-free quarter-circle cursor moves and raised the mean
reachability ceiling, but consecutive burst deletions still lacked a legal
local insertion.  This preregistered closure test adds exactly two fixed
weighted mediants to the unchanged v3.1 six-action vocabulary:

* ``left2_right1``: ``(2L + R) / (2qL + qR)``
* ``left1_right2``: ``(L + 2R) / (qL + 2qR)``

The right endpoint is lifted across the circle before either formula, exactly
as in the existing mediant transition.  The actions are fixed, target-
independent, and candidate-independent.  No controller is trained.  An exact
memoized finite-horizon evaluator searches all eight-action sequences on the
unchanged 18-task Stage-0 manifest and reports global and per-damage-family
closure gates, paired v3.1 deltas, witnesses, negative fixtures, and hashes.
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
        _task_environment,
    )
    from .competency_v31_navigation import (
        NAVIGATION_ACTIONS,
        quarter_step,
    )
    from .repair_experiment import ACTION_BUDGET, POLICY_ACTIONS, RepairTask
    from .strict_environment import Action, DamagePattern, StrictEnvironment
except ImportError:  # Direct script execution from this directory.
    from competency_v3_feasibility import (  # type: ignore[no-redef]
        DEFAULT_CONFIG as STAGE0_CONFIG,
        _manifest as stage0_manifest,
        _task_environment,
    )
    from competency_v31_navigation import (  # type: ignore[no-redef]
        NAVIGATION_ACTIONS,
        quarter_step,
    )
    from repair_experiment import ACTION_BUDGET, POLICY_ACTIONS, RepairTask  # type: ignore[no-redef]
    from strict_environment import Action, DamagePattern, StrictEnvironment  # type: ignore[no-redef]


SEED = STAGE0_CONFIG.seed
F1_THRESHOLD = 0.95
MIN_TASK_F1_THRESHOLD = 0.80
EXACT_TASK_FRACTION_THRESHOLD = 0.90
EXACT_RECOVERY_THRESHOLD = EXACT_TASK_FRACTION_THRESHOLD
WEIGHTED_ACTIONS = ("left2_right1", "left1_right2")
CLOSURE_ACTIONS = (*NAVIGATION_ACTIONS, *WEIGHTED_ACTIONS)
# Search weighted actions first to find exact witnesses early.  The receipt's
# vocabulary order remains the preregistered v3.1 order plus the two additions.
SEARCH_ACTIONS = (*WEIGHTED_ACTIONS, *NAVIGATION_ACTIONS)
MOVEMENT_ACTIONS = (
    Action.MOVE_LEFT.value,
    Action.MOVE_RIGHT.value,
    "move_left_quarter",
    "move_right_quarter",
)
INSERTION_ACTIONS = (
    Action.INSERT_MEDIANT.value,
    Action.INSERT_MIDPOINT.value,
    *WEIGHTED_ACTIONS,
)
V31_RECEIPT_NAME = "competency_v31_navigation_receipt.json"
# Pinned committed evidence; verified before any v3.2 task is evaluated.
V31_RECEIPT_SHA256 = "7b8b9958a813d5f851fcd97f488ce2fb1e3bf8c8a575e13258fca907926d54a8"


@dataclass(frozen=True, slots=True)
class ClosureConfig:
    """Locked v3.2 thresholds and unchanged Stage-0 manifest identity."""

    seed: int = SEED
    action_budget: int = ACTION_BUDGET
    mean_f1_threshold: float = F1_THRESHOLD
    minimum_task_f1_threshold: float = MIN_TASK_F1_THRESHOLD
    exact_task_fraction_threshold: float = EXACT_TASK_FRACTION_THRESHOLD
    negative_fixture_budget: int = 1

    def __post_init__(self) -> None:
        if self.action_budget != ACTION_BUDGET:
            raise ValueError("v3.2 keeps the fixed eight-action budget")
        if (
            self.mean_f1_threshold != F1_THRESHOLD
            or self.minimum_task_f1_threshold != MIN_TASK_F1_THRESHOLD
            or self.exact_task_fraction_threshold != EXACT_TASK_FRACTION_THRESHOLD
        ):
            raise ValueError("v3.2 thresholds are locked before results")
        if self.negative_fixture_budget <= 0 or self.negative_fixture_budget >= self.action_budget:
            raise ValueError("negative fixture must use a strictly smaller positive budget")


DEFAULT_CONFIG = ClosureConfig()


@dataclass(frozen=True, slots=True)
class ClosureCeiling:
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


def _weighted_candidate(left: Fraction, lifted_right: Fraction, action_text: str) -> Fraction:
    if action_text == WEIGHTED_ACTIONS[0]:
        return Fraction(
            2 * left.numerator + lifted_right.numerator,
            2 * left.denominator + lifted_right.denominator,
        )
    if action_text == WEIGHTED_ACTIONS[1]:
        return Fraction(
            left.numerator + 2 * lifted_right.numerator,
            left.denominator + 2 * lifted_right.denominator,
        )
    raise ValueError(f"unsupported weighted action: {action_text}")


def _transition(
    state: tuple[tuple[Fraction, ...], int, int], action_text: str
) -> tuple[tuple[Fraction, ...], int, int]:
    """Pure transition for all eight fixed actions."""

    points, cursor, remaining = state
    remaining -= 1
    if action_text == Action.MOVE_LEFT.value:
        return points, (cursor - 1) % len(points), remaining
    if action_text == Action.MOVE_RIGHT.value:
        return points, (cursor + 1) % len(points), remaining
    if action_text == "move_left_quarter":
        return points, (cursor - quarter_step(len(points))) % len(points), remaining
    if action_text == "move_right_quarter":
        return points, (cursor + quarter_step(len(points))) % len(points), remaining
    left = points[cursor]
    right = points[(cursor + 1) % len(points)]
    lifted_right = right if right > left else right + 1
    if action_text in WEIGHTED_ACTIONS:
        candidate = _weighted_candidate(left, lifted_right, action_text)
    elif action_text == Action.INSERT_MEDIANT.value:
        candidate = Fraction(left.numerator + lifted_right.numerator, left.denominator + lifted_right.denominator)
    elif action_text == Action.INSERT_MIDPOINT.value:
        candidate = (left + lifted_right) / 2
    else:
        raise ValueError(f"unsupported closure action: {action_text}")
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


def _optimistic_metrics(
    metrics: tuple[float, float, float, float, int, int],
    deleted_count: int,
    remaining: int,
) -> tuple[float, float, float, float]:
    """Upper-bound all hidden metrics after the remaining action budget.

    Each action can add at most one previously deleted identity.  Existing
    false positives cannot be removed by this fixed vocabulary, so the bound
    is admissible.  It is used only to prune states that cannot improve any
    already established exact maximum; no candidate is discarded on a mere
    heuristic score.
    """

    _, _, _, _, true_positive, false_positive = metrics
    possible_true_positive = min(deleted_count, true_positive + max(0, remaining))
    possible_recall = possible_true_positive / deleted_count if deleted_count else 1.0
    possible_precision = (
        possible_true_positive / (possible_true_positive + false_positive)
        if possible_true_positive + false_positive
        else 0.0
    )
    possible_f1 = (
        2.0 * possible_precision * possible_recall / (possible_precision + possible_recall)
        if possible_precision + possible_recall
        else 0.0
    )
    possible_exact = float(false_positive == 0 and possible_true_positive >= deleted_count)
    return possible_precision, possible_recall, possible_f1, possible_exact


def exact_closure_ceiling(
    task: RepairTask, *, action_budget: int = ACTION_BUDGET
) -> ClosureCeiling:
    """Exhaustively maximize hidden metrics under the eight fixed actions.

    Movement runs are enumerated as reachable cursor positions rather than as
    four-way action trees.  This is an exact dynamic-programming factorization:
    between two insertions, only the resulting cursor and the number of charged
    movement steps affect the next state.  Every insertion count and every
    cursor position reachable in that count remains represented.
    """

    if action_budget != ACTION_BUDGET:
        raise ValueError("v3.2 ceiling must use the fixed eight-action budget")
    environment = _task_environment(task, "farey")
    target = tuple(environment._target)
    initial_points = tuple(environment._initial_points)
    deleted_count = len(set(target) - set(initial_points))
    initial_state = (initial_points, int(environment._initial_cursor), action_budget)
    cache: dict[tuple[Any, ...], _Frontier] = {}
    visited_states: set[tuple[Any, ...]] = set()
    movement_cache: dict[tuple[int, int, int], list[dict[int, tuple[str, ...]]]] = {}

    def movement_paths(point_count: int, start_cursor: int, maximum: int) -> list[dict[int, tuple[str, ...]]]:
        key = (point_count, start_cursor, maximum)
        cached = movement_cache.get(key)
        if cached is not None:
            return cached
        levels: list[dict[int, tuple[str, ...]]] = [{start_cursor: ()}]
        stride = quarter_step(point_count)
        for _ in range(maximum):
            previous = levels[-1]
            current: dict[int, tuple[str, ...]] = {}
            for cursor, prefix in previous.items():
                options = (
                    (Action.MOVE_LEFT.value, (cursor - 1) % point_count),
                    (Action.MOVE_RIGHT.value, (cursor + 1) % point_count),
                    ("move_left_quarter", (cursor - stride) % point_count),
                    ("move_right_quarter", (cursor + stride) % point_count),
                )
                for action_text, next_cursor in options:
                    current.setdefault(next_cursor, (*prefix, action_text))
            levels.append(current)
        movement_cache[key] = levels
        return levels

    def search(
        state: tuple[tuple[Fraction, ...], int, int],
        metrics_hint: tuple[float, float, float, float, int, int] | None = None,
    ) -> _Frontier:
        points, cursor, remaining = state
        signature = (points, cursor, remaining)
        visited_states.add(signature)
        cached = cache.get(signature)
        if cached is not None:
            return cached
        current_metrics = metrics_hint or _witness_metrics(points, target, initial_points)
        current_precision, current_recall, current_f1, current_exact, _, _ = current_metrics
        if current_exact == 1.0:
            result = _Frontier(1.0, 1.0, 1.0, 1.0, (Action.MOVE_LEFT.value,) * remaining)
            cache[signature] = result
            return result
        if remaining <= 0:
            result = _Frontier(current_precision, current_recall, current_f1, current_exact, ())
            cache[signature] = result
            return result

        max_precision = current_precision
        max_recall = current_recall
        max_f1 = current_f1
        max_exact = current_exact
        branches: list[tuple[tuple[str, ...], _Frontier]] = []
        candidates: list[tuple[float, int, int, int, tuple[str, ...], tuple[tuple[Fraction, ...], int, int], tuple[float, float, float, float, int, int]]] = []
        seen_children: set[tuple[Any, ...]] = set()
        for movement_count in range(remaining):
            paths = movement_paths(len(points), cursor, movement_count)
            for moved_cursor, movement_prefix in paths[movement_count].items():
                before_insert = (points, moved_cursor, remaining - movement_count)
                for insertion_order, action_text in enumerate(INSERTION_ACTIONS):
                    child = _transition(before_insert, action_text)
                    if child in seen_children:
                        continue
                    seen_children.add(child)
                    child_metrics = _witness_metrics(child[0], target, initial_points)
                    optimistic = _optimistic_metrics(child_metrics, deleted_count, child[2])
                    if (
                        optimistic[0] <= max_precision
                        and optimistic[1] <= max_recall
                        and optimistic[2] <= max_f1
                        and optimistic[3] <= max_exact
                    ):
                        continue
                    candidates.append(
                        (
                            optimistic[2],
                            child_metrics[4],
                            movement_count,
                            insertion_order,
                            movement_prefix + (action_text,),
                            child,
                            child_metrics,
                        )
                    )
        candidates.sort(key=lambda item: (-item[1], -item[0], item[2], item[3], item[4]))
        for _, _, _, _, prefix, child, child_metrics in candidates:
            frontier = search(child, child_metrics)
            branches.append((prefix, frontier))
            max_precision = max(max_precision, frontier.max_precision)
            max_recall = max(max_recall, frontier.max_recall)
            max_f1 = max(max_f1, frontier.max_f1)
            max_exact = max(max_exact, frontier.max_exact_recovery)
            if max_precision == max_recall == max_f1 == max_exact == 1.0:
                break

        best_branches = [(prefix, frontier) for prefix, frontier in branches if frontier.max_f1 == max_f1]
        if not best_branches:
            result = _Frontier(current_precision, current_recall, current_f1, current_exact, (Action.MOVE_LEFT.value,) * remaining)
            cache[signature] = result
            return result
        prefix, selected = max(
            best_branches,
            key=lambda item: (
                item[1].max_f1,
                item[1].max_exact_recovery,
                item[1].max_recall,
                item[1].max_precision,
                tuple(reversed(item[1].best_f1_actions)),
                tuple(reversed(item[0])),
            ),
        )
        result = _Frontier(
            max_precision,
            max_recall,
            max_f1,
            max_exact,
            (*prefix, *selected.best_f1_actions),
        )
        cache[signature] = result
        return result

    frontier = search(initial_state)
    return ClosureCeiling(
        frontier.max_precision,
        frontier.max_recall,
        frontier.max_f1,
        frontier.max_exact_recovery,
        frontier.best_f1_actions,
        len(visited_states),
    )


def _replay_witness(task: RepairTask, actions: Sequence[str]) -> dict[str, Any]:
    environment = _task_environment(task, "farey")
    state = (tuple(environment._initial_points), int(environment._initial_cursor), ACTION_BUDGET)
    cursor_trace = [state[1]]
    counts = {"movement_count": 0, "quarter_move_count": 0, "insertion_count": 0, "weighted_insertion_count": 0}
    for action_text in actions:
        if action_text in WEIGHTED_ACTIONS:
            counts["weighted_insertion_count"] += 1
            counts["insertion_count"] += 1
        elif action_text in {Action.INSERT_MEDIANT.value, Action.INSERT_MIDPOINT.value}:
            counts["insertion_count"] += 1
        else:
            counts["movement_count"] += 1
            counts["quarter_move_count"] += action_text in {"move_left_quarter", "move_right_quarter"}
        state = _transition(state, action_text)
        cursor_trace.append(state[1])
    points, final_cursor, _ = state
    precision, recall, f1, exact, recovered, false_positive = _witness_metrics(
        points, tuple(environment._target), tuple(environment._initial_points)
    )
    return {
        "initial_cursor_index": cursor_trace[0],
        "final_cursor_index": final_cursor,
        "cursor_trace": cursor_trace,
        **counts,
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
    """Budget-starved closure fixture; deliberately outside v3.2 protocol."""

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
    initial_state = (tuple(environment._initial_points), int(environment._initial_cursor), budget)
    cache: dict[tuple[Any, ...], float] = {}

    def search(state: tuple[tuple[Fraction, ...], int, int]) -> float:
        points, cursor, remaining = state
        key = (points, cursor, remaining)
        if key in cache:
            return cache[key]
        if remaining <= 0:
            value = _witness_metrics(points, target, initial_points)[2]
        else:
            value = max(search(_transition(state, action)) for action in SEARCH_ACTIONS)
        cache[key] = value
        return value

    value = search(initial_state)
    return {"action_budget": budget, "max_f1": value, "status": "negative" if value < F1_THRESHOLD else "unexpected_positive"}


def _closure_gate(
    name: str,
    rows: Sequence[dict[str, Any]],
    *,
    valid: bool,
    reason: str,
) -> dict[str, Any]:
    mean_f1 = statistics.fmean(row["max_f1"] for row in rows) if rows else 0.0
    minimum_f1 = min((row["max_f1"] for row in rows), default=0.0)
    exact_fraction = statistics.fmean(row["max_exact_recovery"] for row in rows) if rows else 0.0
    status = (
        "unverified"
        if not valid
        else "positive"
        if mean_f1 >= F1_THRESHOLD
        and minimum_f1 >= MIN_TASK_F1_THRESHOLD
        and exact_fraction >= EXACT_TASK_FRACTION_THRESHOLD
        else "negative"
    )
    return {
        "name": name,
        "status": status,
        "valid": valid,
        "reason": reason,
        "mean_max_f1": mean_f1,
        "mean_f1_threshold": F1_THRESHOLD,
        "minimum_task_max_f1": minimum_f1,
        "minimum_task_f1_threshold": MIN_TASK_F1_THRESHOLD,
        "exact_recovery_task_fraction": exact_fraction,
        "exact_recovery_task_fraction_threshold": EXACT_TASK_FRACTION_THRESHOLD,
        "task_count": len(rows),
    }


def _source_hashes() -> dict[str, str]:
    directory = Path(__file__).parent
    names = (
        "competency_v32_closure.py",
        "competency_v31_navigation.py",
        "competency_v3_feasibility.py",
        "repair_experiment.py",
        "strict_environment.py",
        "test_competency_v32_closure.py",
    )
    return {
        name: sha256((directory / name).read_bytes()).hexdigest()
        for name in names
        if (directory / name).exists()
    }


def _load_v31_baseline(tasks: Sequence[RepairTask]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Load and independently verify the committed v3.1 exact baseline.

    Recomputing the six-action baseline would duplicate an already cold-
    audited exact run. The receipt hash and every source hash recorded by that
    receipt are pinned before closure evaluation, so this is evidence reuse,
    not a reduction of the v3.2 manifest or search.
    """

    path = Path(__file__).with_name(V31_RECEIPT_NAME)
    raw = path.read_bytes()
    digest = sha256(raw).hexdigest()
    if digest != V31_RECEIPT_SHA256:
        raise RuntimeError(f"v3.1 receipt hash mismatch: expected {V31_RECEIPT_SHA256}, got {digest}")
    receipt = json.loads(raw.decode("utf-8"))
    if (
        receipt.get("seed") != SEED
        or receipt.get("experiment")
        != "V3.1 exact reachability with scale-free quarter-circle cursor moves"
    ):
        raise RuntimeError("v3.1 baseline receipt identity mismatch")
    directory = path.parent
    for name, expected in receipt.get("source_hashes", {}).items():
        source = directory / name
        if not source.exists() or sha256(source.read_bytes()).hexdigest() != expected:
            raise RuntimeError(f"v3.1 baseline source hash mismatch: {name}")
    rows = receipt.get("new_ceiling", {}).get("tasks", [])
    expected_keys = [
        (task.order, task.pattern.value, task.goal.value, task.seed, task.damage_count)
        for task in tasks
    ]
    actual_keys = [
        (
            row.get("order"),
            row.get("pattern"),
            row.get("goal"),
            row.get("seed"),
            STAGE0_CONFIG.representative_damage_count,
        )
        for row in rows
    ]
    if actual_keys != expected_keys:
        raise RuntimeError("v3.1 baseline manifest does not match Stage-0 task order/seed/damage")
    return rows, {
        "receipt": V31_RECEIPT_NAME,
        "sha256": digest,
        "source_hashes_verified": True,
        "recomputed_in_v32": False,
    }


def run_closure(config: ClosureConfig = DEFAULT_CONFIG) -> dict[str, Any]:
    """Run v3.1 and v3.2 exact ceilings on the identical 18-task manifest."""

    if config.seed != STAGE0_CONFIG.seed:
        raise ValueError("v3.2 must use the identical Stage-0 manifest seed")
    tasks = stage0_manifest(STAGE0_CONFIG)
    v31_rows, v31_provenance = _load_v31_baseline(tasks)
    baseline_rows: list[dict[str, Any]] = []
    new_rows: list[dict[str, Any]] = []
    paired: list[dict[str, Any]] = []
    for task, old in zip(tasks, v31_rows):
        old_row = {
            "order": task.order,
            "pattern": task.pattern.value,
            "goal": task.goal.value,
            "seed": task.seed,
            "max_f1": old["max_f1"],
            "max_exact_recovery": old["max_exact_recovery"],
            "max_precision": old["max_precision"],
            "max_recall": old["max_recall"],
            "visited_states": old["visited_states"],
            "best_f1_actions": list(old["best_f1_actions"]),
        }
        old_metrics = (old["max_precision"], old["max_recall"], old["max_f1"], old["max_exact_recovery"])
        if all(value == 1.0 for value in old_metrics):
            # The v3.2 action set strictly contains v3.1's. All four hidden
            # metrics are bounded by one, so an old all-one ceiling pins the
            # new ceiling exactly without redundant state enumeration.
            new_row = {
                "order": task.order,
                "pattern": task.pattern.value,
                "goal": task.goal.value,
                "seed": task.seed,
                "max_f1": 1.0,
                "max_exact_recovery": 1.0,
                "max_precision": 1.0,
                "max_recall": 1.0,
                "visited_states": 0,
                "search_mode": "monotonic_pinned_from_v31",
                "best_f1_actions": list(old["best_f1_actions"]),
                "witness": _replay_witness(task, old["best_f1_actions"]),
            }
        else:
            new = exact_closure_ceiling(task)
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
                "search_mode": "exact_v32_movement_run_dp",
                "best_f1_actions": list(new.best_f1_actions),
                "witness": _replay_witness(task, new.best_f1_actions),
            }
        baseline_rows.append(old_row)
        new_rows.append(new_row)
        paired.append(
            {
                "order": task.order,
                "pattern": task.pattern.value,
                "goal": task.goal.value,
                "seed": task.seed,
                "v31_max_f1": old["max_f1"],
                "v32_max_f1": new_row["max_f1"],
                "delta_max_f1": new_row["max_f1"] - old["max_f1"],
                "v31_max_exact_recovery": old["max_exact_recovery"],
                "v32_max_exact_recovery": new_row["max_exact_recovery"],
                "delta_max_exact_recovery": new_row["max_exact_recovery"] - old["max_exact_recovery"],
            }
        )

    family_rows: dict[str, list[dict[str, Any]]] = {}
    for family in sorted({row["pattern"] for row in new_rows}):
        family_rows[family] = [row for row in new_rows if row["pattern"] == family]
    family_gates = {
        family: _closure_gate(
            f"damage_family_{family}",
            rows,
            valid=len(rows) == 6,
            reason="same locked mean/minimum/exact closure thresholds applied within each damage family",
        )
        for family, rows in family_rows.items()
    }
    closure_gate = _closure_gate(
        "closure",
        new_rows,
        valid=len(tasks) == len(baseline_rows) == len(new_rows) == 18,
        reason="all three locked closure thresholds applied jointly to the unchanged 18-task Stage-0 manifest",
    )
    family_gate = {
        "name": "damage_family_closure",
        "status": "positive" if closure_gate["status"] == "positive" and all(gate["status"] == "positive" for gate in family_gates.values()) else "negative",
        "valid": all(gate["valid"] for gate in family_gates.values()),
        "reason": "every damage family must satisfy the locked closure thresholds independently",
        "families": family_gates,
    }
    old_mean_f1 = statistics.fmean(row["max_f1"] for row in baseline_rows)
    new_mean_f1 = statistics.fmean(row["max_f1"] for row in new_rows)
    old_mean_exact = statistics.fmean(row["max_exact_recovery"] for row in baseline_rows)
    new_mean_exact = statistics.fmean(row["max_exact_recovery"] for row in new_rows)
    fixture = _negative_fixture(tasks[0], config.negative_fixture_budget)
    source_hashes = _source_hashes()
    if source_hashes != _source_hashes():
        raise RuntimeError("sources changed while v3.2 was running")
    return {
        "schema_version": 1,
        "experiment": "V3.2 exact repair closure with weighted mediants",
        "seed": config.seed,
        "provenance": {
            "command": "PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/competency_v32_closure.py",
            "python": sys.version.split()[0],
            "controller_training": False,
        },
        "predeclaration": {
            "manifest_inherited_from": "competency_v3_feasibility.DEFAULT_CONFIG",
            "v31_baseline": v31_provenance,
            "orders": list(STAGE0_CONFIG.representative_orders),
            "patterns": [pattern.value for pattern in STAGE0_CONFIG.representative_patterns],
            "goals": sorted({task.goal.value for task in tasks}),
            "damage_count": STAGE0_CONFIG.representative_damage_count,
            "replicates_per_cell": 1,
            "action_budget": ACTION_BUDGET,
            "v31_actions": list(NAVIGATION_ACTIONS),
            "weighted_actions": list(WEIGHTED_ACTIONS),
            "closure_actions": list(CLOSURE_ACTIONS),
            "weighted_formulas": {
                "left2_right1": "(2L + R) / (2qL + qR)",
                "left1_right2": "(L + 2R) / (qL + 2qR)",
            },
            "quarter_move_step": "max(1, visible_count // 4)",
            "mean_f1_threshold": F1_THRESHOLD,
            "minimum_task_f1_threshold": MIN_TASK_F1_THRESHOLD,
            "exact_recovery_task_fraction_threshold": EXACT_TASK_FRACTION_THRESHOLD,
            "negative_fixture_budget": config.negative_fixture_budget,
        },
        "v31_ceiling": {
            "tasks": baseline_rows,
            "mean_max_f1": old_mean_f1,
            "mean_max_exact_recovery": old_mean_exact,
        },
        "v32_ceiling": {
            "tasks": new_rows,
            "mean_max_f1": new_mean_f1,
            "mean_max_exact_recovery": new_mean_exact,
        },
        "paired_v31_vs_v32": {
            "tasks": paired,
            "mean_delta_max_f1": new_mean_f1 - old_mean_f1,
            "mean_delta_max_exact_recovery": new_mean_exact - old_mean_exact,
            "strictly_improved_f1_task_count": sum(row["delta_max_f1"] > 0.0 for row in paired),
            "strictly_improved_exact_task_count": sum(row["delta_max_exact_recovery"] > 0.0 for row in paired),
        },
        "search_provenance": {
            "pinned_from_v31_task_count": sum(row["search_mode"] == "monotonic_pinned_from_v31" for row in new_rows),
            "exact_v32_task_count": sum(row["search_mode"] == "exact_v32_movement_run_dp" for row in new_rows),
            "monotonic_superset_proof": "v3.2 actions strictly contain v3.1 actions; an all-one v3.1 ceiling is an exact all-one v3.2 ceiling because no hidden metric exceeds one",
        },
        "damage_family_rows": {
            family: {
                "tasks": rows,
                "mean_max_f1": statistics.fmean(row["max_f1"] for row in rows),
                "minimum_task_max_f1": min(row["max_f1"] for row in rows),
                "exact_recovery_task_fraction": statistics.fmean(row["max_exact_recovery"] for row in rows),
            }
            for family, rows in family_rows.items()
        },
        "gates": {
            "closure": closure_gate,
            "damage_family_closure": family_gate,
            "negative_budget_fixture": {
                "name": "negative_budget_fixture",
                "status": "negative" if fixture["max_f1"] < F1_THRESHOLD else "unexpected_positive",
                "valid": True,
                "reason": "same eight-action vocabulary deliberately budget-starved to one action",
                "max_f1": fixture["max_f1"],
                "threshold": F1_THRESHOLD,
            },
        },
        "negative_fixtures": {"budget_starved": fixture},
        "source_hashes": source_hashes,
        "claim_boundary": (
            "This is an evaluator-only action-vocabulary closure result. Even a "
            "positive gate establishes only finite attainability with hidden-state "
            "search; it is not feedback learning, hidden repair by a controller, "
            "transfer, or a Levin-style competency."
        ),
    }


def _fmt(value: float) -> str:
    return f"{value:.4f}"


def result_markdown(result: dict[str, Any]) -> str:
    v31 = result["v31_ceiling"]
    v32 = result["v32_ceiling"]
    paired = result["paired_v31_vs_v32"]
    closure = result["gates"]["closure"]
    family_gate = result["gates"]["damage_family_closure"]
    lines = [
        "# V3.2 weighted-mediant closure results",
        "",
        "This evaluator-only run keeps the Stage-0 manifest, eight-action budget, and v3.1 navigation actions unchanged. It adds only fixed weighted mediants.",
        "",
        "## Locked protocol",
        "",
        f"V3.1 actions: `{result['predeclaration']['v31_actions']}`. Added actions: `{result['predeclaration']['weighted_actions']}`. Formulas: `{result['predeclaration']['weighted_formulas']}`. Manifest: orders `{result['predeclaration']['orders']}`, all three damage families, both goals, two deletions, one task per cell.",
        "",
        "## Paired exact ceilings",
        "",
        "| metric | v3.1 six-action | v3.2 eight-action | paired change | locked threshold |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| mean max F1 | {_fmt(v31['mean_max_f1'])} | {_fmt(v32['mean_max_f1'])} | {_fmt(paired['mean_delta_max_f1'])} | {_fmt(F1_THRESHOLD)} |",
        f"| mean max exact recovery | {_fmt(v31['mean_max_exact_recovery'])} | {_fmt(v32['mean_max_exact_recovery'])} | {_fmt(paired['mean_delta_max_exact_recovery'])} | {_fmt(EXACT_TASK_FRACTION_THRESHOLD)} task fraction |",
        "",
        f"Global closure gate: **{closure['status']}**. Damage-family closure gate: **{family_gate['status']}**.",
        "",
        "## Damage-family closure",
        "",
        "| family | mean max F1 | minimum task F1 | exact task fraction | status |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for family, gate in family_gate["families"].items():
        rows = result["damage_family_rows"][family]
        lines.append(
            f"| {family} | {_fmt(rows['mean_max_f1'])} | {_fmt(rows['minimum_task_max_f1'])} | {_fmt(rows['exact_recovery_task_fraction'])} | {gate['status']} |"
        )
    lines.extend(
        [
            "",
            f"The exact search records per-task witnesses and visited states. Every witness uses all eight charged actions; the receipt records weighted insertion counts, cursor traces, recovered identities, and false positives. Strict improvements occurred on `{paired['strictly_improved_f1_task_count']}` F1 tasks and `{paired['strictly_improved_exact_task_count']}` exact-recovery tasks.",
            "",
            f"Negative one-action fixture: max F1 `{_fmt(result['negative_fixtures']['budget_starved']['max_f1'])}`, status `{result['gates']['negative_budget_fixture']['status']}`.",
            "",
            result["claim_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(result: dict[str, Any]) -> None:
    directory = Path(__file__).parent
    (directory / "competency_v32_closure_receipt.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (directory / "CLOSURE_RESULTS.md").write_text(result_markdown(result), encoding="utf-8")


def main() -> None:
    result = run_closure()
    write_outputs(result)
    print("wrote competency_v32_closure_receipt.json and CLOSURE_RESULTS.md")
    print(", ".join(f"{name}={gate['status']}" for name, gate in result["gates"].items()))


if __name__ == "__main__":
    main()
