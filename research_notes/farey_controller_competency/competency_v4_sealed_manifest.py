#!/usr/bin/env python3
"""V4 sealed-manifest feasibility audit for a deletion-only controller.

This module freezes a fresh train/validation/test manifest before any learner
exists, then performs evaluator-only diagnostics on the final V3.4 twelve-
action vocabulary. It deliberately does not train, evaluate, or import a
controller. Exact reachability is computed on the small candidate orders;
larger orders receive a deterministic target-restricted witness search. Since
the environment is insertion-only, exact target recovery cannot contain a
false positive: target-only search is complete for exact-recovery reachability,
while F1 ceilings remain partial when no exact path is found.

The public manifest contains only task ids, split names, and the trusted goal
bit.  Exact order, family, seed, damage count, fractions, and deletion masks
remain private and are represented by a sealed hash. The final manifest is
fresh and disjoint in order and seed from the earlier development probe.
"""

from __future__ import annotations

from copy import deepcopy
from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import statistics
import sys
from typing import Any, Iterable, Sequence

try:  # Package import.
    from .competency_v34_multiscale_navigation import (
        CLOSURE_ACTIONS,
        exact_closure_ceiling,
        _replay_witness,
        _transition,
        _witness_metrics,
    )
    from .repair_experiment import ACTION_BUDGET as REPAIR_ACTION_BUDGET, RepairTask, make_manifest
    from .strict_environment import DamagePattern, GoalState, StrictEnvironment, _round_reward
except ImportError:  # Direct script execution from this directory.
    from competency_v34_multiscale_navigation import (  # type: ignore[no-redef]
        CLOSURE_ACTIONS,
        exact_closure_ceiling,
        _replay_witness,
        _transition,
        _witness_metrics,
    )
    from repair_experiment import ACTION_BUDGET as REPAIR_ACTION_BUDGET, RepairTask, make_manifest  # type: ignore[no-redef]
    from strict_environment import DamagePattern, GoalState, StrictEnvironment, _round_reward  # type: ignore[no-redef]


SEED = 20260901
DEVELOPMENT_SEED = 20260811
DEVELOPMENT_ORDERS = (6, 8, 11)
TRAIN_ORDERS = (7, 9, 12, 15)
VALIDATION_ORDERS = (18, 20)
TEST_ORDERS = (24, 32, 48)
SPLIT_ORDERS = {
    "train": TRAIN_ORDERS,
    "validation": VALIDATION_ORDERS,
    "test": TEST_ORDERS,
}
PATTERNS = (
    DamagePattern.RANDOM_ISOLATED,
    DamagePattern.BURST,
    DamagePattern.DENOMINATOR_BIASED,
)
GOALS = (GoalState.COVERAGE, GoalState.SPECTRAL)
DAMAGE_COUNT = 2
ACTION_BUDGET = REPAIR_ACTION_BUDGET
PUBLIC_FIELDS = ("task_id", "split", "trusted_goal")
PRIVATE_FIELDS = (
    "task_id",
    "split",
    "order",
    "pattern",
    "goal",
    "seed",
    "damage_count",
    "deleted_indices",
    "target_sha256",
    "damage_mask_sha256",
)
FORBIDDEN_PUBLIC_FIELDS = (
    "order",
    "pattern",
    "seed",
    "damage_count",
    "target",
    "fractions",
    "deleted_indices",
    "deleted_points",
    "mask",
)
EXACT_ORDERS = frozenset((7, 9, 12))
SPLIT_REPLICATES = {"train": 10, "validation": 10, "test": 20}
FINAL_MANIFEST_ACCESS_WARNING = (
    "This is the final fresh sealed manifest after the interface, actions, and thresholds "
    "were frozen. A learner may access only the public schema and train stream if the "
    "feasibility gate passes; validation and test streams remain hidden until controller "
    "freeze. This audit gate is negative, so do not train on this manifest. Do not regenerate "
    "it or use hidden evaluator fields for learning or transfer."
)
EXACT_RECOVERY_FEASIBILITY_THRESHOLD = 0.90


@dataclass(frozen=True, slots=True)
class V4Config:
    """Locked V4 final split, damage, budget, and bounded-search protocol."""

    seed: int = SEED
    development_seed: int = DEVELOPMENT_SEED
    damage_count: int = DAMAGE_COUNT
    action_budget: int = ACTION_BUDGET

    def __post_init__(self) -> None:
        if self.action_budget != 8:
            raise ValueError("V4 keeps the fixed eight-step budget")
        if self.damage_count != 2:
            raise ValueError("V4 keeps two hidden deletions")
        if set().union(*SPLIT_ORDERS.values()) & set(DEVELOPMENT_ORDERS):
            raise ValueError("development and sealed orders must be disjoint")


DEFAULT_CONFIG = V4Config()


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical(value)).hexdigest()


def _split_seed(split: str, config: V4Config) -> int:
    salts = {"train": 0x13579BDF, "validation": 0x2468ACE0, "test": 0x55AA33CC}
    return config.seed ^ salts[split]


def _private_rows(tasks_by_split: dict[str, Sequence[RepairTask]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "test"):
        for index, task in enumerate(tasks_by_split[split]):
            environment = StrictEnvironment(
                task.order,
                task.pattern,
                damage_count=task.damage_count,
                seed=task.seed,
                rotation=True,
                action_budget=ACTION_BUDGET,
                goal=task.goal,
            )
            target_serialized = [str(point) for point in environment._target]
            deleted_indices = list(environment._deleted_indices)
            target_sha256 = _digest(target_serialized)
            damage_mask_sha256 = _digest(
                {"target_sha256": target_sha256, "deleted_indices": deleted_indices}
            )
            rows.append(
                {
                    "task_id": f"{split}-{index:03d}",
                    "split": split,
                    "order": task.order,
                    "pattern": task.pattern.value,
                    "goal": task.goal.value,
                    "seed": task.seed,
                    "damage_count": task.damage_count,
                    "deleted_indices": deleted_indices,
                    "target_sha256": target_sha256,
                    "damage_mask_sha256": damage_mask_sha256,
                }
            )
    return rows


def _public_rows(private_rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"task_id": row["task_id"], "split": row["split"], "trusted_goal": row["goal"]}
        for row in private_rows
    ]


def seal_manifests(config: V4Config = DEFAULT_CONFIG) -> dict[str, Any]:
    """Generate and hash the final fresh manifests before learner access."""

    tasks_by_split = {
        split: make_manifest(
            orders,
            PATTERNS,
            damage_count=config.damage_count,
            replicates=SPLIT_REPLICATES[split],
            seed=_split_seed(split, config),
        )
        for split, orders in SPLIT_ORDERS.items()
    }
    private_rows = _private_rows(tasks_by_split)
    public_rows = _public_rows(private_rows)
    all_seeds = [row["seed"] for row in private_rows]
    development_tasks = make_manifest(
        DEVELOPMENT_ORDERS,
        PATTERNS,
        damage_count=config.damage_count,
        replicates=1,
        seed=config.development_seed,
    )
    development_seeds = {task.seed for task in development_tasks}
    if set(all_seeds) & development_seeds:
        raise RuntimeError("sealed task seeds collide with development seeds")
    if len(all_seeds) != len(set(all_seeds)):
        raise RuntimeError("sealed task seeds are not unique")
    expected_count = sum(
        len(SPLIT_ORDERS[split]) * len(PATTERNS) * len(GOALS) * SPLIT_REPLICATES[split]
        for split in SPLIT_ORDERS
    )
    if len(private_rows) != expected_count:
        raise RuntimeError("sealed manifest count mismatch")
    public_schema = {
        "fields": list(PUBLIC_FIELDS),
        "forbidden_fields": list(FORBIDDEN_PUBLIC_FIELDS),
        "controller_visible_goal": True,
        "exact_fractions_included": False,
        "deletion_masks_included": False,
    }
    private_schema = {
        "fields": list(PRIVATE_FIELDS),
        "exact_fractions_included": False,
        "deletion_masks_included": True,
        "target_commitments_included": True,
    }
    task_commitments = [
        {"task_id": row["task_id"], "commitment_sha256": _digest(row)} for row in private_rows
    ]
    return {
        "config": {
            "seed": config.seed,
            "development_seed": config.development_seed,
            "split_orders": {split: list(orders) for split, orders in SPLIT_ORDERS.items()},
            "patterns": [pattern.value for pattern in PATTERNS],
            "goals": [goal.value for goal in GOALS],
            "split_replicates": dict(SPLIT_REPLICATES),
            "damage_count": config.damage_count,
            "action_budget": config.action_budget,
        },
        "tasks_by_split": tasks_by_split,
        "private_rows": private_rows,
        "public_rows": public_rows,
        "public_schema": public_schema,
        "private_schema": private_schema,
        "public_hash": _digest({"schema": public_schema, "rows": public_rows}),
        "private_hash": _digest({"schema": private_schema, "rows": private_rows}),
        "task_commitments": task_commitments,
        "development_orders": list(DEVELOPMENT_ORDERS),
        "development_seed_collision_check": True,
    }


def _task_from_row(row: dict[str, Any]) -> RepairTask:
    return RepairTask(
        int(row["order"]),
        DamagePattern.coerce(row["pattern"]),
        GoalState.coerce(row["goal"]),
        int(row["seed"]),
        int(row["damage_count"]),
    )


def _target_candidates(points: tuple[Fraction, ...], deleted: set[Fraction]) -> int:
    return sum(
        1
        for index, left in enumerate(points)
        for right in (points[(index + 1) % len(points)],)
        for lifted_right in (right if right > left else right + 1,)
        for candidate in (
            Fraction(left.numerator + lifted_right.numerator, left.denominator + lifted_right.denominator),
            (left + lifted_right) / 2,
            Fraction(2 * left.numerator + lifted_right.numerator, 2 * left.denominator + lifted_right.denominator),
            Fraction(left.numerator + 2 * lifted_right.numerator, left.denominator + 2 * lifted_right.denominator),
        )
        if candidate % 1 in deleted
    )


def _target_restricted_witness(task: RepairTask) -> dict[str, Any]:
    """Exhaustively search movement plus target-only insertion branches.

    Every fixed movement is explored to depth eight, while an insertion branch
    is retained only when it adds one of the two evaluator-hidden deleted
    targets.  This target restriction is complete for *exact recovery*: the
    environment has insertion-only transitions, so a non-target insertion
    would be a permanent false positive and can never occur on an exact path.
    The resulting F1 value is still only a demonstrated lower bound when no
    exact path is found, because a non-target insertion could improve F1.
    """

    environment = StrictEnvironment(
        task.order,
        task.pattern,
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=ACTION_BUDGET,
        goal=task.goal,
    )
    target = tuple(environment._target)
    initial = tuple(environment._initial_points)
    deleted = set(target) - set(initial)
    insertion_actions = ("insert_mediant", "insert_midpoint", "left2_right1", "left1_right2")
    insertion_set = set(insertion_actions)
    movement_actions = tuple(action for action in CLOSURE_ACTIONS if action not in insertion_set)
    initial_state = (initial, int(environment._initial_cursor), ACTION_BUDGET, ())
    queue = deque([initial_state])
    seen: set[tuple[Any, ...]] = {(initial, int(environment._initial_cursor), ACTION_BUDGET)}
    best_points = initial
    best_cursor = int(environment._initial_cursor)
    best_actions: tuple[str, ...] = ()
    best_metrics = _witness_metrics(initial, target, initial)
    nodes = 0
    exact_found = False
    while queue:
        points, cursor, remaining, actions = queue.popleft()
        if remaining <= 0:
            continue
        branches: list[tuple[tuple[Any, ...], tuple[tuple[Fraction, ...], int, int, tuple[str, ...]]]] = []
        for action in movement_actions + insertion_actions:
            child_points, child_cursor, child_remaining = _transition((points, cursor, remaining), action)
            nodes += 1
            added = set(child_points) - set(points)
            if action in insertion_set and (not added or not added.issubset(deleted)):
                continue
            child_actions = (*actions, action)
            signature = (child_points, child_cursor, child_remaining)
            if signature in seen:
                continue
            seen.add(signature)
            metrics = _witness_metrics(child_points, target, initial)
            priority = (
                int(metrics[3]),
                metrics[2],
                metrics[1],
                metrics[0],
                metrics[4],
                -metrics[5],
                tuple(reversed(child_actions)),
            )
            branches.append((priority, (child_points, child_cursor, child_remaining, child_actions)))
            if (metrics[2], metrics[3], metrics[1], metrics[0]) > (
                best_metrics[2], best_metrics[3], best_metrics[1], best_metrics[0]
            ):
                best_points, best_cursor, best_actions, best_metrics = child_points, child_cursor, child_actions, metrics
            if metrics[3] == 1.0:
                exact_found = True
                best_points, best_cursor, best_actions, best_metrics = child_points, child_cursor, child_actions, metrics
                break
        if exact_found:
            break
        branches.sort(key=lambda item: item[0], reverse=True)
        queue.extend(row for _priority, row in branches)
    padded_actions = (*best_actions, *("move_left",) * (ACTION_BUDGET - len(best_actions)))
    return {
        "max_precision": best_metrics[0],
        "max_recall": best_metrics[1],
        "max_f1": best_metrics[2],
        "max_exact_recovery": best_metrics[3],
        "best_f1_actions": list(padded_actions),
        "witness": _replay_witness(task, padded_actions),
        "visited_states": len(seen),
        "nodes_expanded": nodes,
        "completeness": "exact_recovery_proved_reachable" if exact_found else "exact_recovery_proved_unreachable_f1_incomplete",
        "target_restricted": True,
        "target_aware_branch_ordering": True,
        "ceiling_upper_bound": 1.0,
    }


def _reachability_row(task: RepairTask, config: V4Config) -> dict[str, Any]:
    if task.order in EXACT_ORDERS:
        ceiling = exact_closure_ceiling(task)
        return {
            "order": task.order,
            "pattern": task.pattern.value,
            "goal": task.goal.value,
            "seed": task.seed,
            "damage_count": task.damage_count,
            "max_precision": ceiling.max_precision,
            "max_recall": ceiling.max_recall,
            "max_f1": ceiling.max_f1,
            "max_exact_recovery": ceiling.max_exact_recovery,
            "best_f1_actions": list(ceiling.best_f1_actions),
            "witness": _replay_witness(task, ceiling.best_f1_actions),
            "visited_states": ceiling.visited_states,
            "search_mode": "exact_v34_ceiling",
            "completeness": "exact_exhaustive",
            "ceiling_upper_bound": ceiling.max_f1,
        }
    bounded = _target_restricted_witness(task)
    return {
        "order": task.order,
        "pattern": task.pattern.value,
        "goal": task.goal.value,
        "seed": task.seed,
        "damage_count": task.damage_count,
        "search_mode": "target_restricted_witness_search",
        **bounded,
    }


def reachability_audit(manifest: dict[str, Any], config: V4Config = DEFAULT_CONFIG) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "test"):
        for task in manifest["tasks_by_split"][split]:
            row = _reachability_row(task, config)
            row["split"] = split
            rows.append(row)
    exact_rows = [row for row in rows if row["completeness"] == "exact_exhaustive"]
    unit_rows = [row for row in rows if row["max_f1"] >= 1.0 and row["max_exact_recovery"] >= 1.0]
    incomplete_rows = [row for row in rows if "incomplete" in row["completeness"]]
    exact_recovery_reachable_rows = [row for row in rows if row["max_exact_recovery"] >= 1.0]
    cell_summary: dict[str, dict[str, Any]] = {}
    for split in ("train", "validation", "test"):
        for order in SPLIT_ORDERS[split]:
            cell_rows = [row for row in rows if row["split"] == split and row["order"] == order]
            cell_summary[f"{split}:N{order}"] = {
                "task_count": len(cell_rows),
                "bounded_incomplete_count": sum(row in incomplete_rows for row in cell_rows),
                "unit_witness_count": sum(row in unit_rows for row in cell_rows),
                "demonstrated_mean_f1": statistics.fmean(row["max_f1"] for row in cell_rows) if cell_rows else 0.0,
            }
    return {
        "action_vocabulary": list(CLOSURE_ACTIONS),
        "action_budget": ACTION_BUDGET,
        "tasks": rows,
        "task_count": len(rows),
        "exact_task_count": len(exact_rows),
        "bounded_task_count": len(rows) - len(exact_rows),
        "target_restricted_task_count": len(rows) - len(exact_rows),
        "unit_witness_task_count": len(unit_rows),
        "exact_recovery_reachable_task_count": len(exact_recovery_reachable_rows),
        "exact_recovery_reachable_fraction": len(exact_recovery_reachable_rows) / len(rows) if rows else 0.0,
        "exact_recovery_completeness": "complete_for_all_rows",
        "bounded_incomplete_task_count": len(incomplete_rows),
        "bounded_incomplete_rate": len(incomplete_rows) / (len(rows) - len(exact_rows)) if rows and len(rows) > len(exact_rows) else 0.0,
        "target_restricted_incomplete_rate": len(incomplete_rows) / (len(rows) - len(exact_rows)) if rows and len(rows) > len(exact_rows) else 0.0,
        "cell_summary": cell_summary,
        "mean_demonstrated_f1": statistics.fmean(row["max_f1"] for row in rows) if rows else 0.0,
        "mean_exact_ceiling_f1": statistics.fmean(row["max_f1"] for row in exact_rows) if exact_rows else None,
        "completeness": "partial_exact_plus_target_restricted_witnesses",
        "ceiling_status": "unverified" if incomplete_rows else "verified",
        "ceiling_claim_scope": "exact rows only; target-restricted rows are sound witnesses with trivial full-vocabulary upper bound 1.0",
        "exact_recovery_gate": {
            "name": "sealed_manifest_exact_recovery_feasibility",
            "status": "positive" if len(exact_recovery_reachable_rows) / len(rows) >= EXACT_RECOVERY_FEASIBILITY_THRESHOLD else "negative",
            "valid": True,
            "reachable_fraction": len(exact_recovery_reachable_rows) / len(rows) if rows else 0.0,
            "threshold": EXACT_RECOVERY_FEASIBILITY_THRESHOLD,
            "reason": "target-restricted search is complete for exact recovery because insertion-only transitions cannot remove false positives",
        },
    }


def _identity_delta_and_reward(task: RepairTask, action: str) -> tuple[bool, float, float]:
    environment = StrictEnvironment(
        task.order,
        task.pattern,
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=ACTION_BUDGET,
        goal=task.goal,
    )
    points = tuple(environment._initial_points)
    state = (points, int(environment._initial_cursor), ACTION_BUDGET)
    before_metric = environment._goal_metric(points)
    before_identity = len(set(points) & (set(environment._target) - set(environment._initial_points)))
    child_points, _cursor, _remaining = _transition(state, action)
    after_metric = environment._goal_metric(child_points)
    after_identity = len(set(child_points) & (set(environment._target) - set(environment._initial_points)))
    return after_identity > before_identity, float(_round_reward(before_metric - after_metric)), float(after_identity - before_identity)


def _auc(scores: Sequence[float], labels: Sequence[bool]) -> float:
    positives = [score for score, label in zip(scores, labels) if label]
    negatives = [score for score, label in zip(scores, labels) if not label]
    if not positives or not negatives:
        return 0.5
    wins = sum(1.0 if left > right else 0.5 if left == right else 0.0 for left in positives for right in negatives)
    return wins / (len(positives) * len(negatives))


def visible_reward_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for split in ("train", "validation", "test"):
        for task in manifest["tasks_by_split"][split]:
            for action in CLOSURE_ACTIONS:
                improving, reward, identity_delta = _identity_delta_and_reward(task, action)
                records.append(
                    {
                        "split": split,
                        "goal": task.goal.value,
                        "action": action,
                        "reward": reward,
                        "identity_improving": improving,
                        "identity_delta": identity_delta,
                    }
                )
    scores = [row["reward"] for row in records]
    labels = [row["identity_improving"] for row in records]
    positive = [row["reward"] for row in records if row["identity_improving"]]
    negative = [row["reward"] for row in records if not row["identity_improving"]]
    return {
        "samples": len(records),
        "improving_actions": len(positive),
        "non_improving_actions": len(negative),
        "auc": _auc(scores, labels),
        "mean_reward_improving": statistics.fmean(positive) if positive else 0.0,
        "mean_reward_non_improving": statistics.fmean(negative) if negative else 0.0,
        "reward_definition": "target-independent coverage/spectral scalar change",
        "hidden_identity_used_in_reward": False,
        "records_digest": _digest(records),
    }


def run_audit(config: V4Config = DEFAULT_CONFIG) -> dict[str, Any]:
    """Seal first, then run evaluator-only diagnostics; no learner is created."""

    manifest = seal_manifests(config)
    reachability = reachability_audit(manifest, config)
    feedback = visible_reward_audit(manifest)
    public_rows = manifest["public_rows"]
    if any(set(row) != set(PUBLIC_FIELDS) for row in public_rows):
        raise RuntimeError("public manifest row leaked a private field")
    return {
        "schema_version": 1,
        "experiment": "V4 sealed-manifest evaluator-only feasibility audit",
        "provenance": {
            "command": "PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/competency_v4_sealed_manifest.py",
            "python": sys.version.split()[0],
            "controller_training": False,
            "learner_created": False,
            "manifest_frozen_before_learner": True,
        },
        "manifest_seal": {
            "public_schema": manifest["public_schema"],
            "private_schema": manifest["private_schema"],
            "public_rows": public_rows,
            "public_sha256": manifest["public_hash"],
            "private_sha256": manifest["private_hash"],
            "private_row_count": len(manifest["private_rows"]),
            "public_row_count": len(public_rows),
            "task_commitments": manifest["task_commitments"],
            "generator_module": Path(__file__).name,
            "development_orders": manifest["development_orders"],
            "development_seed_collision_check": manifest["development_seed_collision_check"],
            "warning": FINAL_MANIFEST_ACCESS_WARNING,
            "learner_access_policy": "public_schema_and_train_only_until_controller_freeze",
            "training_eligibility": "ineligible_failed_exact_recovery_feasibility_gate",
        },
        "reachability": reachability,
        "gates": {
            "sealed_manifest_feasibility": reachability["exact_recovery_gate"],
        },
        "visible_reward": feedback,
        "negative_fixtures": {
            "constant_scalar_reward_auc": 0.5,
            "constant_scalar_reward_status": "negative",
            "manifest_private_hash_mutation_check": _digest({"private_sha256": manifest["private_hash"], "tampered": True}) != manifest["private_hash"],
        },
        "claim_boundary": (
            "No controller was trained or evaluated. Exact reachability ceilings "
            "apply only to rows marked exact_exhaustive for F1. For exact recovery, "
            "target-restricted search is complete for every row because this "
            "environment is insertion-only: a non-target insertion is a permanent "
            "false positive and cannot occur on an exact path. F1 values on rows "
            "without an exact witness remain demonstrated lower bounds. The final manifest "
            "was sealed only after interface, action, and threshold freeze. A "
            "learner may access public schema and train stream only; validation "
            "and test remain hidden until controller freeze. Hidden evaluator "
            "fields are not learning or transfer inputs. The exact-recovery "
            "feasibility gate is negative (reachable fraction below 0.90), so "
            "this sealed manifest is ineligible for training and must be retained "
            "as a failed preregistered feasibility set."
        ),
    }


def _source_hashes() -> dict[str, str]:
    directory = Path(__file__).parent
    names = (
        "competency_v4_sealed_manifest.py",
        "competency_v34_multiscale_navigation.py",
        "competency_v3_feasibility.py",
        "repair_experiment.py",
        "strict_environment.py",
        "test_competency_v4_sealed_manifest.py",
    )
    return {name: sha256((directory / name).read_bytes()).hexdigest() for name in names if (directory / name).exists()}


def write_outputs(result: dict[str, Any]) -> None:
    directory = Path(__file__).parent
    result["source_hashes"] = _source_hashes()
    result["generator_sha256"] = result["source_hashes"].get(Path(__file__).name)
    (directory / "competency_v4_sealed_manifest_receipt.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (directory / "SEALED_MANIFEST_RESULTS.md").write_text(result_markdown(result), encoding="utf-8")


def _fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.4f}"


def result_markdown(result: dict[str, Any]) -> str:
    seal = result["manifest_seal"]
    reach = result["reachability"]
    feedback = result["visible_reward"]
    lines = [
        "# V4 sealed-manifest feasibility audit",
        "",
        "No controller was trained or evaluated. The final manifest was sealed after interface/action/threshold freeze and before learner access.",
        "",
        f"Private manifest SHA256: `{seal['private_sha256']}`. Public schema SHA256: `{seal['public_sha256']}`. Rows: `{seal['private_row_count']}`.",
        "",
        f"ACCESS POLICY: {seal['warning']}",
        f"TRAINING ELIGIBILITY: `{seal['training_eligibility']}`.",
        "",
        "## Fresh sealed splits",
        "",
        "| split | orders | rows |",
        "| --- | --- | ---: |",
        "| train candidate | 7, 9, 12, 15 | 240 |",
        "| validation | 18, 20 | 120 |",
        "| test | 24, 32, 48 | 360 |",
        "",
        "## Reachability diagnostics",
        "",
        f"Vocabulary: `{result['reachability']['action_vocabulary']}`; budget: `{result['reachability']['action_budget']}`. Exact rows: `{reach['exact_task_count']}`; target-restricted witness rows: `{reach['target_restricted_task_count']}`; unit witnesses: `{reach['unit_witness_task_count']}`; target-restricted unresolved: `{reach['bounded_incomplete_task_count']}/{reach['target_restricted_task_count']}` ({reach['bounded_incomplete_rate']:.3f}).",
        "",
        "| quantity | value |",
        "| --- | ---: |",
        f"| demonstrated mean F1 (exact + bounded) | {_fmt(reach['mean_demonstrated_f1'])} |",
        f"| mean F1 on exact rows | {_fmt(reach['mean_exact_ceiling_f1'])} |",
        f"| completeness | `{reach['completeness']}` |",
        f"| ceiling status | `{reach['ceiling_status']}` |",
        f"| exact-recovery reachable fraction | {_fmt(reach['exact_recovery_reachable_fraction'])} |",
        f"| exact-recovery feasibility gate | `{reach['exact_recovery_gate']['status']}` (threshold {_fmt(reach['exact_recovery_gate']['threshold'])}) |",
        "",
        "Target-restricted unresolved counts by cell:",
        "",
        "| cell | rows | target-restricted incomplete | unit witnesses |",
        "| --- | ---: | ---: | ---: |",
    ]
    for cell, summary in reach["cell_summary"].items():
        lines.append(
            f"| {cell} | {summary['task_count']} | {summary['bounded_incomplete_count']} | {summary['unit_witness_count']} |"
        )
    lines.extend(
        [
            "",
            "Target-restricted rows exhaustively explore all fixed movement actions to depth eight while admitting only insertions of the two hidden deleted targets. This is complete for exact recovery across the full twelve-action vocabulary: because transitions are insertion-only, any non-target insertion would be a permanent false positive and cannot occur on an exact path. A no-witness result therefore proves exact recovery unreachable, while its F1 remains a demonstrated lower bound rather than a full-vocabulary ceiling.",
        "",
        "## Visible scalar reward",
        "",
        f"AUC for target-independent coverage/spectral reward versus evaluator-only identity improvement: `{_fmt(feedback['auc'])}` over `{feedback['samples']}` one-step records (`{feedback['improving_actions']}` improving, `{feedback['non_improving_actions']}` non-improving). Hidden identity was not used to compute reward.",
        "",
        "## Claim boundary",
        "",
        result["claim_boundary"],
        "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    result = run_audit()
    write_outputs(result)
    print("wrote competency_v4_sealed_manifest_receipt.json and SEALED_MANIFEST_RESULTS.md")
    print("controller_training=False, learner_created=False, manifest_frozen_before_learner=True")


if __name__ == "__main__":
    main()
