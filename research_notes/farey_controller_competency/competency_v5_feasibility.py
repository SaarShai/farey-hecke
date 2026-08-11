#!/usr/bin/env python3
"""V5 exact shortest-path feasibility audit for the retired V4 task set.

V4's 720-task manifest is intentionally retired from any learning or final
transfer claim.  This module only asks whether a generic, target-independent
action interface could make exact two-point repair reachable within a larger
budget.  The movement vocabulary is fixed before looking at a task:

* ``move_left``/``move_right`` use offset ``1``;
* for ``k = 1..6``, the named half/quarter/eighth/sixteenth/
  thirty-second/sixty-fourth actions use ``max(1, visible_count // 2**k)``;
* the four V3.4 insertion rules are retained.

There are eighteen fixed actions (fourteen movements and four insertions) and
the locked budget is sixteen.  The evaluator exploits ``d=2`` rather than
enumerating an 18-way action tree.  For each visible-count cursor graph it
computes shortest movement distances, enumerates both deleted-target insertion
orders and every cursor/insertion action that creates the next target, and
then repeats after the first insertion.  Because the shell is insertion-only,
an exact path cannot contain a non-target insertion; this factorization is an
exact shortest-path calculation for exact recovery.

No controller is trained or imported.  The result is development feasibility
evidence only.  The retired V4 task set is permanently excluded from any
later learning, transfer, or competency claim.
"""

from __future__ import annotations

from bisect import bisect_left
from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
from typing import Any

try:  # Package import.
    from .competency_v4_sealed_manifest import (
        seal_manifests,
    )
    from .strict_environment import DamagePattern, GoalState, StrictEnvironment
except ImportError:  # Direct script execution from this directory.
    from competency_v4_sealed_manifest import seal_manifests  # type: ignore[no-redef]
    from strict_environment import DamagePattern, GoalState, StrictEnvironment  # type: ignore[no-redef]


V4_RECEIPT_NAME = "competency_v4_sealed_manifest_receipt.json"
V4_RECEIPT_SHA256 = "aaeebebb8a95770a9919f1a627faf4a703e4dd9ff6c60a65bab24c0b169ec474"
V4_PRIVATE_MANIFEST_SHA256 = "e9ffa6077c116615d2061421f3e222f9d85ffab70e7eacadba1f5411f2c76d31"
V4_PUBLIC_MANIFEST_SHA256 = "16451545b25dbedc44d47a57dcca2583c108d1b06dd88dc7dc5acfb25df2ede6"
V4_TASK_COUNT = 720

ACTION_BUDGET = 16
EXACT_RECOVERY_THRESHOLD = 0.90
CELL_RECOVERY_THRESHOLD = 0.80
DAMAGE_COUNT = 2
SCALE_EXPONENTS = (1, 2, 3, 4, 5, 6)
SCALE_NAMES = {
    1: "half",
    2: "quarter",
    3: "eighth",
    4: "sixteenth",
    5: "thirty_second",
    6: "sixty_fourth",
}
BASE_MOVEMENT_ACTIONS = ("move_left", "move_right")
SCALE_MOVEMENT_ACTIONS = tuple(
    action
    for exponent in SCALE_EXPONENTS
    for action in (f"move_left_{SCALE_NAMES[exponent]}", f"move_right_{SCALE_NAMES[exponent]}")
)
MOVEMENT_ACTIONS = (*BASE_MOVEMENT_ACTIONS, *SCALE_MOVEMENT_ACTIONS)
INSERTION_ACTIONS = ("insert_mediant", "insert_midpoint", "left2_right1", "left1_right2")
ACTION_VOCABULARY = (*MOVEMENT_ACTIONS, *INSERTION_ACTIONS)
PUBLIC_CLAIM_BOUNDARY = (
    "V5 is an evaluator-only development feasibility audit. No controller was "
    "trained or evaluated. The unchanged V4 720-task manifest is retired and "
    "permanently excluded from final learning, transfer, and competency claims."
)


@dataclass(frozen=True, slots=True)
class V5Config:
    """Locked V5 shortest-path budget and feasibility gates."""

    action_budget: int = ACTION_BUDGET
    exact_recovery_threshold: float = EXACT_RECOVERY_THRESHOLD
    cell_recovery_threshold: float = CELL_RECOVERY_THRESHOLD
    negative_fixture_budget: int = 1

    def __post_init__(self) -> None:
        if self.action_budget != ACTION_BUDGET:
            raise ValueError("V5 action budget is locked at sixteen")
        if self.exact_recovery_threshold != EXACT_RECOVERY_THRESHOLD:
            raise ValueError("V5 overall gate is locked before evaluation")
        if self.cell_recovery_threshold != CELL_RECOVERY_THRESHOLD:
            raise ValueError("V5 cell gate is locked before evaluation")
        if self.negative_fixture_budget <= 0 or self.negative_fixture_budget >= self.action_budget:
            raise ValueError("negative fixture budget must be positive and below sixteen")


DEFAULT_CONFIG = V5Config()


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical(value)).hexdigest()


def _movement_offset(action: str, visible_count: int) -> int:
    """Return the signed cursor offset for one fixed movement action."""

    if visible_count <= 0:
        raise ValueError("visible_count must be positive")
    if action == "move_left":
        return -1
    if action == "move_right":
        return 1
    for exponent in SCALE_EXPONENTS:
        if action == f"move_left_{SCALE_NAMES[exponent]}":
            return -max(1, visible_count // (2**exponent))
        if action == f"move_right_{SCALE_NAMES[exponent]}":
            return max(1, visible_count // (2**exponent))
    raise ValueError(f"unsupported movement action: {action}")


@dataclass(frozen=True, slots=True)
class MovementGraph:
    """Shortest movement distances and predecessor data for one cursor graph."""

    visible_count: int
    start_cursor: int
    distances: tuple[int, ...]
    parents: tuple[int, ...]
    parent_actions: tuple[str, ...]


def _movement_bfs(visible_count: int, start_cursor: int) -> MovementGraph:
    """Compute exact shortest paths on the fixed-offset cursor graph."""

    if visible_count <= 0 or not 0 <= start_cursor < visible_count:
        raise ValueError("cursor graph start is outside the visible circle")
    distances = [-1] * visible_count
    parents = [-1] * visible_count
    parent_actions = [""] * visible_count
    distances[start_cursor] = 0
    queue: deque[int] = deque([start_cursor])
    while queue:
        cursor = queue.popleft()
        for action in MOVEMENT_ACTIONS:
            offset = _movement_offset(action, visible_count)
            child = (cursor + offset) % visible_count
            if distances[child] >= 0:
                continue
            distances[child] = distances[cursor] + 1
            parents[child] = cursor
            parent_actions[child] = action
            queue.append(child)
    if any(distance < 0 for distance in distances):
        raise AssertionError("the fixed +/-1 actions must make every cursor reachable")
    return MovementGraph(
        visible_count,
        start_cursor,
        tuple(distances),
        tuple(parents),
        tuple(parent_actions),
    )


def _movement_path(graph: MovementGraph, target_cursor: int) -> tuple[str, ...]:
    """Reconstruct one deterministic shortest path from a movement BFS."""

    if not 0 <= target_cursor < graph.visible_count or graph.distances[target_cursor] < 0:
        raise ValueError("movement target cursor is unreachable")
    path: list[str] = []
    cursor = target_cursor
    while cursor != graph.start_cursor:
        path.append(graph.parent_actions[cursor])
        cursor = graph.parents[cursor]
    path.reverse()
    return tuple(path)


def _insert_transition(
    points: tuple[Fraction, ...], cursor: int, action: str
) -> tuple[tuple[Fraction, ...], int, Fraction | None]:
    """Apply one insertion action and return the added identity, if any."""

    if action not in INSERTION_ACTIONS:
        raise ValueError(f"unsupported insertion action: {action}")
    left = points[cursor]
    right = points[(cursor + 1) % len(points)]
    lifted_right = right if right > left else right + 1
    if action == "insert_mediant":
        candidate = Fraction(left.numerator + lifted_right.numerator, left.denominator + lifted_right.denominator)
    elif action == "insert_midpoint":
        candidate = (left + lifted_right) / 2
    elif action == "left2_right1":
        candidate = Fraction(
            2 * left.numerator + lifted_right.numerator,
            2 * left.denominator + lifted_right.denominator,
        )
    else:  # left1_right2
        candidate = Fraction(
            left.numerator + 2 * lifted_right.numerator,
            left.denominator + 2 * lifted_right.denominator,
        )
    candidate %= 1
    if candidate in points:
        return points, cursor, None
    updated = tuple(sorted((*points, candidate)))
    return updated, updated.index(candidate), candidate


def _target_insertion_options(
    points: tuple[Fraction, ...], target: Fraction
) -> tuple[tuple[int, str, tuple[Fraction, ...], int], ...]:
    """Enumerate every cursor/action pair that inserts one exact target.

    A missing point has exactly one containing circular gap.  ``bisect_left``
    identifies that gap, including the wrap-around gap for target ``0``; only
    the four fixed insertion formulas can then be candidates.  This is
    equivalent to scanning every cursor/action pair, but avoids sorting a
    large point tuple for the many pairs that cannot possibly produce the
    requested target.
    """

    if target in points:
        return ()
    insertion_index = bisect_left(points, target)
    cursor = insertion_index - 1 if insertion_index else len(points) - 1
    options: list[tuple[int, str, tuple[Fraction, ...], int]] = []
    for action in INSERTION_ACTIONS:
        updated, updated_cursor, added = _insert_transition(points, cursor, action)
        if added == target:
            options.append((cursor, action, updated, updated_cursor))
    return tuple(options)


def _task_environment(task: Any) -> StrictEnvironment:
    return StrictEnvironment(
        task.order,
        DamagePattern.coerce(task.pattern),
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=ACTION_BUDGET,
        goal=GoalState.coerce(task.goal),
    )


def _choose_better(candidate: tuple[Any, ...], incumbent: tuple[Any, ...] | None) -> bool:
    """Use total action count then action text as a deterministic tie-break."""

    return incumbent is None or (candidate[0], candidate[1]) < (incumbent[0], incumbent[1])


def shortest_exact_recovery(task: Any) -> dict[str, Any]:
    """Find the exact minimum action count for a two-deletion task.

    The only branching left after movement BFS is the two possible target
    insertion orders and the finite insertion-action/cursor choices.  Movement
    distances are independent of the target and are computed on the visible
    circle before and after the first insertion.
    """

    environment = _task_environment(task)
    target = tuple(environment._target)
    initial = tuple(environment._initial_points)
    deleted = tuple(sorted(set(target) - set(initial)))
    if len(deleted) != DAMAGE_COUNT:
        raise ValueError(f"V5 requires exactly two deleted targets, got {len(deleted)}")
    initial_cursor = int(environment._initial_cursor)
    first_graph = _movement_bfs(len(initial), initial_cursor)
    best: tuple[Any, ...] | None = None
    insertion_options = 0
    second_graphs: dict[tuple[tuple[Fraction, ...], int], MovementGraph] = {}

    for first_index, first_target in enumerate(deleted):
        second_target = deleted[1 - first_index]
        for first_cursor, first_action, points_after_first, cursor_after_first in _target_insertion_options(
            initial, first_target
        ):
            insertion_options += 1
            first_distance = first_graph.distances[first_cursor]
            graph_key = (points_after_first, cursor_after_first)
            second_graph = second_graphs.get(graph_key)
            if second_graph is None:
                second_graph = _movement_bfs(len(points_after_first), cursor_after_first)
                second_graphs[graph_key] = second_graph
            for second_cursor, second_action, points_after_second, _cursor_after_second in _target_insertion_options(
                points_after_first, second_target
            ):
                second_distance = second_graph.distances[second_cursor]
                if points_after_second != target:
                    continue
                first_path = _movement_path(first_graph, first_cursor)
                second_path = _movement_path(second_graph, second_cursor)
                actions = (*first_path, first_action, *second_path, second_action)
                candidate = (
                    first_distance + second_distance + 2,
                    actions,
                    first_index,
                    first_cursor,
                    first_action,
                    second_cursor,
                    second_action,
                )
                if _choose_better(candidate, best):
                    best = candidate

    if best is None:
        return {
            "min_actions": None,
            "reachable_within_budget": False,
            "witness_actions": [],
            "first_target": None,
            "second_target": None,
            "insertion_options": insertion_options,
            "movement_graphs": len(second_graphs) + 1,
            "exact_shortest_path": True,
        }
    length, actions, first_index, first_cursor, first_action, second_cursor, second_action = best
    return {
        "min_actions": length,
        "reachable_within_budget": length <= ACTION_BUDGET,
        "witness_actions": list(actions),
        "first_target": str(deleted[first_index]),
        "second_target": str(deleted[1 - first_index]),
        "first_cursor": first_cursor,
        "first_insertion_action": first_action,
        "second_cursor": second_cursor,
        "second_insertion_action": second_action,
        "insertion_options": insertion_options,
        "movement_graphs": len(second_graphs) + 1,
        "exact_shortest_path": True,
    }


def _manifest_and_receipt() -> tuple[dict[str, Any], dict[str, Any]]:
    """Load and independently pin the unchanged V4 manifest evidence."""

    receipt_path = Path(__file__).parent / V4_RECEIPT_NAME
    receipt_bytes = receipt_path.read_bytes()
    receipt_sha256 = sha256(receipt_bytes).hexdigest()
    if receipt_sha256 != V4_RECEIPT_SHA256:
        raise RuntimeError("retired V4 receipt hash changed; do not regenerate V5 tasks")
    receipt = json.loads(receipt_bytes)
    if receipt["manifest_seal"]["private_sha256"] != V4_PRIVATE_MANIFEST_SHA256:
        raise RuntimeError("retired V4 private manifest hash changed")
    if receipt["manifest_seal"]["public_sha256"] != V4_PUBLIC_MANIFEST_SHA256:
        raise RuntimeError("retired V4 public manifest hash changed")
    manifest = seal_manifests()
    if manifest["private_hash"] != V4_PRIVATE_MANIFEST_SHA256 or manifest["public_hash"] != V4_PUBLIC_MANIFEST_SHA256:
        raise RuntimeError("deterministic V4 task reconstruction does not match the pinned receipt")
    if sum(len(tasks) for tasks in manifest["tasks_by_split"].values()) != V4_TASK_COUNT:
        raise RuntimeError("retired V4 task count changed")
    return manifest, receipt


def evaluate_manifest(config: V5Config = DEFAULT_CONFIG) -> dict[str, Any]:
    manifest, receipt = _manifest_and_receipt()
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "test"):
        for index, task in enumerate(manifest["tasks_by_split"][split]):
            result = shortest_exact_recovery(task)
            rows.append(
                {
                    "task_id": f"{split}-{index:03d}",
                    "split": split,
                    "order": task.order,
                    "pattern": task.pattern.value,
                    "goal": task.goal.value,
                    "seed": task.seed,
                    **result,
                }
            )
    reachable = [row for row in rows if row["reachable_within_budget"]]
    reachable_fraction = len(reachable) / len(rows) if rows else 0.0
    cell_summary: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = f"N{row['order']}:{row['pattern']}:{row['goal']}"
        cell = cell_summary.setdefault(key, {"task_count": 0, "reachable_count": 0, "reachable_fraction": 0.0})
        cell["task_count"] += 1
        cell["reachable_count"] += int(row["reachable_within_budget"])
    for cell in cell_summary.values():
        cell["reachable_fraction"] = cell["reachable_count"] / cell["task_count"]
    lengths = sorted(row["min_actions"] for row in reachable if row["min_actions"] is not None)

    def quantile(q: float) -> float | None:
        if not lengths:
            return None
        if len(lengths) == 1:
            return float(lengths[0])
        position = q * (len(lengths) - 1)
        lower = int(position)
        upper = min(len(lengths) - 1, lower + 1)
        weight = position - lower
        return lengths[lower] + weight * (lengths[upper] - lengths[lower])

    minimum_cell_fraction = min((cell["reachable_fraction"] for cell in cell_summary.values()), default=0.0)
    overall_gate = reachable_fraction >= config.exact_recovery_threshold
    cell_gate = minimum_cell_fraction >= config.cell_recovery_threshold
    negative_task = manifest["tasks_by_split"]["train"][0]
    negative_result = shortest_exact_recovery(negative_task)
    negative_fixture = {
        "task_id": "train-000",
        "budget": config.negative_fixture_budget,
        "minimum_actions": negative_result["min_actions"],
        "status": "negative"
        if negative_result["min_actions"] is None
        or negative_result["min_actions"] > config.negative_fixture_budget
        else "invalid",
        "reason": "two insertions are required, so a one-action budget cannot recover both hidden targets",
    }
    return {
        "schema_version": 1,
        "experiment": "V5 exact shortest-path feasibility audit on retired V4 manifest",
        "provenance": {
            "controller_training": False,
            "controller_evaluated": False,
            "learner_created": False,
            "manifest_status": "retired_development_only",
            "claim_boundary": PUBLIC_CLAIM_BOUNDARY,
        },
        "configuration": {
            "action_budget": config.action_budget,
            "damage_count": DAMAGE_COUNT,
            "movement_offsets": "+/-1 and +/-max(1, visible_count // 2**k), k=1..6",
            "movement_actions": list(MOVEMENT_ACTIONS),
            "insertion_actions": list(INSERTION_ACTIONS),
            "action_vocabulary": list(ACTION_VOCABULARY),
            "action_count": len(ACTION_VOCABULARY),
            "exact_recovery_threshold": config.exact_recovery_threshold,
            "cell_recovery_threshold": config.cell_recovery_threshold,
            "search": "exact shortest movement BFS plus two target insertion orders",
        },
        "retired_v4": {
            "receipt_name": V4_RECEIPT_NAME,
            "receipt_sha256": V4_RECEIPT_SHA256,
            "private_manifest_sha256": V4_PRIVATE_MANIFEST_SHA256,
            "public_manifest_sha256": V4_PUBLIC_MANIFEST_SHA256,
            "task_count": V4_TASK_COUNT,
            "receipt_generator_sha256": receipt["generator_sha256"],
            "permanently_excluded_from_final_eval": True,
        },
        "tasks": rows,
        "task_count": len(rows),
        "reachable_within_budget_count": len(reachable),
        "reachable_within_budget_fraction": reachable_fraction,
        "unreachable_within_budget_count": len(rows) - len(reachable),
        "cell_summary": cell_summary,
        "minimum_cell_reachable_fraction": minimum_cell_fraction,
        "action_length_summary_reachable": {
            "count": len(lengths),
            "min": min(lengths) if lengths else None,
            "q25": quantile(0.25),
            "median": quantile(0.50),
            "q75": quantile(0.75),
            "q90": quantile(0.90),
            "max": max(lengths) if lengths else None,
        },
        "gates": {
            "overall_exact_recovery": {
                "status": "positive" if overall_gate else "negative",
                "reachable_fraction": reachable_fraction,
                "threshold": config.exact_recovery_threshold,
            },
            "per_cell_exact_recovery": {
                "status": "positive" if cell_gate else "negative",
                "minimum_cell_fraction": minimum_cell_fraction,
                "threshold": config.cell_recovery_threshold,
                "cell_count": len(cell_summary),
            },
            "combined_v5_feasibility": {
                "status": "positive" if overall_gate and cell_gate else "negative",
                "reason": "both overall and every N-by-family-by-goal cell gate are required",
            },
        },
        "negative_fixture": negative_fixture,
    }


def _bruteforce_exact_within(task: Any, max_actions: int) -> int | None:
    """Small-depth full action-tree checker used only for equivalence tests."""

    environment = _task_environment(task)
    target = tuple(environment._target)
    initial = tuple(environment._initial_points)
    start = (initial, int(environment._initial_cursor))
    queue: deque[tuple[tuple[Fraction, ...], int, int]] = deque([(initial, start[1], 0)])
    seen = {(initial, start[1], 0)}
    while queue:
        points, cursor, depth = queue.popleft()
        if set(points) == set(target):
            return depth
        if depth >= max_actions:
            continue
        for action in ACTION_VOCABULARY:
            if action in MOVEMENT_ACTIONS:
                child = (points, (cursor + _movement_offset(action, len(points))) % len(points))
            else:
                child_points, child_cursor, _added = _insert_transition(points, cursor, action)
                child = (child_points, child_cursor)
            signature = (*child, depth + 1)
            if signature in seen:
                continue
            seen.add(signature)
            queue.append((child[0], child[1], depth + 1))
    return None


def _source_hashes() -> dict[str, str]:
    directory = Path(__file__).parent
    names = (
        "competency_v5_feasibility.py",
        "competency_v4_sealed_manifest.py",
        "competency_v4_sealed_manifest_receipt.json",
        "strict_environment.py",
        "test_competency_v5_feasibility.py",
    )
    return {name: sha256((directory / name).read_bytes()).hexdigest() for name in names if (directory / name).exists()}


def result_markdown(result: dict[str, Any]) -> str:
    config = result["configuration"]
    gate = result["gates"]
    summary = result["action_length_summary_reachable"]
    lines = [
        "# V5 exact shortest-path feasibility audit",
        "",
        PUBLIC_CLAIM_BOUNDARY,
        "",
        f"Retired V4 receipt SHA256: `{result['retired_v4']['receipt_sha256']}`; private manifest SHA256: `{result['retired_v4']['private_manifest_sha256']}`; public manifest SHA256: `{result['retired_v4']['public_manifest_sha256']}`; tasks: `{result['task_count']}`.",
        "",
        "## Locked generic interface",
        "",
        f"Budget: `{config['action_budget']}`; damage count: `{config['damage_count']}`; action count: `{config['action_count']}`. Movement offsets are `{config['movement_offsets']}`. Insertion actions are `{config['insertion_actions']}`.",
        "",
        "## Exact shortest-path results",
        "",
        f"Reachable within budget: `{result['reachable_within_budget_count']}/{result['task_count']}` ({result['reachable_within_budget_fraction']:.4f}); unreachable: `{result['unreachable_within_budget_count']}`.",
        f"Reachable action lengths: n=`{summary['count']}`, min=`{summary['min']}`, q25=`{summary['q25']}`, median=`{summary['median']}`, q75=`{summary['q75']}`, q90=`{summary['q90']}`, max=`{summary['max']}`.",
        "",
        "| gate | status | observed | threshold |",
        "| --- | --- | ---: | ---: |",
        f"| overall exact recovery | `{gate['overall_exact_recovery']['status']}` | {gate['overall_exact_recovery']['reachable_fraction']:.4f} | {gate['overall_exact_recovery']['threshold']:.2f} |",
        f"| every N×family×goal cell | `{gate['per_cell_exact_recovery']['status']}` | {gate['per_cell_exact_recovery']['minimum_cell_fraction']:.4f} minimum | {gate['per_cell_exact_recovery']['threshold']:.2f} |",
        f"| combined V5 feasibility | `{gate['combined_v5_feasibility']['status']}` | — | both required |",
        "",
        "| cell | tasks | reachable | fraction |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key, cell in result["cell_summary"].items():
        lines.append(f"| {key} | {cell['task_count']} | {cell['reachable_count']} | {cell['reachable_fraction']:.4f} |")
    lines.extend(
        [
            "",
            "The evaluator is exact for d=2: a valid exact path must insert the two deleted targets in one of two orders, and insertion-only transitions make any non-target insertion permanently incompatible with exact equality. Movement costs are exact shortest distances on each visible-count graph, so reported minimum action counts are not beam or heuristic ceilings.",
            "",
            f"Negative fixture: budget `{result['negative_fixture']['budget']}` on `{result['negative_fixture']['task_id']}` is `{result['negative_fixture']['status']}` (minimum actions `{result['negative_fixture']['minimum_actions']}`).",
            "",
            "The V4 manifest is retained only as a failed/development feasibility artifact. It must not be used to train, select, tune, or claim transfer for a controller; final evaluation requires a newly sealed manifest.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(result: dict[str, Any]) -> None:
    directory = Path(__file__).parent
    result["source_hashes"] = _source_hashes()
    result["generator_sha256"] = result["source_hashes"].get(Path(__file__).name)
    (directory / "competency_v5_feasibility_receipt.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (directory / "V5_FEASIBILITY_RESULTS.md").write_text(result_markdown(result), encoding="utf-8")


def main() -> None:
    result = evaluate_manifest()
    write_outputs(result)
    print("wrote competency_v5_feasibility_receipt.json and V5_FEASIBILITY_RESULTS.md")
    print(
        f"reachable={result['reachable_within_budget_count']}/{result['task_count']}, "
        f"overall_gate={result['gates']['overall_exact_recovery']['status']}, "
        f"cell_gate={result['gates']['per_cell_exact_recovery']['status']}"
    )


if __name__ == "__main__":
    main()
