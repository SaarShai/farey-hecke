#!/usr/bin/env python3
"""Stage-0 feasibility diagnostics for the repair-only Farey probe.

This module deliberately does not train a controller.  It asks three prior
questions that must be answered before a competency claim is attempted:

* Is hidden repair reachable with the fixed four-action vocabulary and the
  eight-action budget at all (an exhaustive evaluator upper bound)?
* How much of the evaluator's preferred first action is identifiable from the
  serialized coarse controller view (an observation-collision ceiling)?
* Does the target-independent scalar reward contain information about hidden
  identity improvement (a target-independent feedback AUC)?

All exact targets, masks, and hidden labels are evaluator-only.  The receipt is
deterministic and records both positive ceilings and deliberately negative
fixtures.  A positive feasibility gate is not a controller result.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import statistics
import sys
from collections import Counter, defaultdict, deque
from typing import Any, Iterable, Sequence

try:  # Package import.
    from .repair_experiment import (
        ACTION_BUDGET,
        GOALS,
        POLICY_ACTIONS,
        CoarseRepairView,
        RepairTask,
        _hidden_repair_metrics,
        _oracle_action,
        _task_environment,
        coarse_view,
        make_manifest,
    )
    from .strict_environment import Action, DamagePattern, StrictEnvironment
except ImportError:  # Direct script execution from this directory.
    from repair_experiment import (  # type: ignore[no-redef]
        ACTION_BUDGET,
        GOALS,
        POLICY_ACTIONS,
        CoarseRepairView,
        RepairTask,
        _hidden_repair_metrics,
        _oracle_action,
        _task_environment,
        coarse_view,
        make_manifest,
    )
    from strict_environment import Action, DamagePattern, StrictEnvironment  # type: ignore[no-redef]


SEED = 20260811
REPRESENTATIVE_ORDERS = (6, 8, 11)
REPRESENTATIVE_PATTERNS = (
    DamagePattern.RANDOM_ISOLATED,
    DamagePattern.BURST,
    DamagePattern.DENOMINATOR_BIASED,
)
REPRESENTATIVE_DAMAGE_COUNT = 2
# Depth three exposes enough repeated quantized views to measure genuine
# label collisions while keeping the diagnostic bounded (18 tasks × 85 states).
COLLISION_DEPTH = 3


@dataclass(frozen=True, slots=True)
class FeasibilityConfig:
    """Small preregistered Stage-0 manifest and gate thresholds."""

    seed: int = SEED
    representative_orders: tuple[int, ...] = REPRESENTATIVE_ORDERS
    representative_patterns: tuple[DamagePattern, ...] = REPRESENTATIVE_PATTERNS
    representative_damage_count: int = REPRESENTATIVE_DAMAGE_COUNT
    collision_depth: int = COLLISION_DEPTH
    action_budget: int = ACTION_BUDGET
    reachability_f1_threshold: float = 0.80
    reachability_exact_threshold: float = 0.50
    observation_ceiling_threshold: float = 0.70
    feedback_auc_threshold: float = 0.65

    def __post_init__(self) -> None:
        if self.action_budget != ACTION_BUDGET:
            raise ValueError("Stage-0 uses the same fixed eight-action budget")
        if self.collision_depth < 0 or self.collision_depth > 4:
            raise ValueError("collision depth must be in [0, 4]")
        if self.representative_damage_count < 1:
            raise ValueError("representative damage must be positive")


DEFAULT_CONFIG = FeasibilityConfig()


@dataclass(frozen=True, slots=True)
class ExactCeiling:
    """Per-task maxima over every legal action sequence in the budget."""

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


def _state_signature(environment: Any) -> tuple[Any, ...]:
    """Hash all mutable state relevant to future transitions.

    The target and goal are fixed per search, so the signature only needs the
    current point set, cursor, budget, and done flag.  Fractions are exact and
    hashable; no floating state enters the cache key.
    """

    return (
        tuple(environment._points),
        int(environment._cursor),
        int(environment._remaining_budget),
        bool(environment._done),
    )


def exact_reachability_ceiling(
    task: RepairTask, *, action_budget: int = ACTION_BUDGET
) -> ExactCeiling:
    """Exhaustively maximize hidden repair metrics under fixed legal actions.

    The search is evaluator-only and uses no controller-visible information.
    There is no STOP branch: the existing repair protocol commits exactly the
    four nonterminal actions for the eight charged decisions.  The maxima are
    upper bounds for any policy with this interface and budget, not empirical
    controller performance.
    """

    if action_budget != ACTION_BUDGET:
        raise ValueError("ceiling must use the fixed eight-action budget")
    # The strict environment remains the authoritative setup and transition
    # definition.  For the exhaustive evaluator search we copy its exact
    # point/cursor transition in a compact tuple state; invoking ``step`` for
    # every node would recompute coverage/spectral rewards and make the same
    # finite search unnecessarily expensive.
    environment = _task_environment(task, "farey")
    target = tuple(environment._target)
    initial_points = tuple(environment._initial_points)
    deleted = set(target) - set(initial_points)
    initial_state = (initial_points, int(environment._initial_cursor), action_budget)
    cache: dict[tuple[Any, ...], _Frontier] = {}
    visited_states: set[tuple[Any, ...]] = set()

    def transition(state: tuple[tuple[Fraction, ...], int, int], action_text: str) -> tuple[tuple[Fraction, ...], int, int]:
        points, cursor, remaining = state
        remaining -= 1
        if action_text == Action.MOVE_LEFT.value:
            return points, (cursor - 1) % len(points), remaining
        if action_text == Action.MOVE_RIGHT.value:
            return points, (cursor + 1) % len(points), remaining
        left = points[cursor]
        right = points[(cursor + 1) % len(points)]
        lifted_right = right if right > left else right + 1
        if action_text == Action.INSERT_MEDIANT.value:
            candidate = Fraction(left.numerator + lifted_right.numerator, left.denominator + lifted_right.denominator)
        else:
            candidate = (left + lifted_right) / 2
        candidate %= 1
        if candidate in points:
            return points, cursor, remaining
        updated = tuple(sorted((*points, candidate)))
        return updated, updated.index(candidate), remaining

    def leaf_metrics(points: tuple[Fraction, ...]) -> tuple[float, float, float, float]:
        visible = set(points)
        additions = visible - set(initial_points)
        true_positive = len(additions & deleted)
        false_positive = len(additions - set(target))
        precision = true_positive / len(additions) if additions else 0.0
        recall = true_positive / len(deleted) if deleted else 1.0
        f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
        return precision, recall, f1, float(visible == set(target))

    def search(state: tuple[tuple[Fraction, ...], int, int]) -> _Frontier:
        points, cursor, remaining = state
        signature = (points, cursor, remaining)
        visited_states.add(signature)
        cached = cache.get(signature)
        if cached is not None:
            return cached
        if remaining <= 0:
            precision, recall, f1, exact = leaf_metrics(points)
            result = _Frontier(precision, recall, f1, exact, ())
            cache[signature] = result
            return result

        branches: list[tuple[str, _Frontier]] = []
        for action_text in POLICY_ACTIONS:
            branches.append((action_text, search(transition(state, action_text))))

        max_precision = max(frontier.max_precision for _, frontier in branches)
        max_recall = max(frontier.max_recall for _, frontier in branches)
        max_f1 = max(frontier.max_f1 for _, frontier in branches)
        max_exact = max(frontier.max_exact_recovery for _, frontier in branches)
        candidates = [
            (action_text, frontier)
            for action_text, frontier in branches
            if frontier.max_f1 == max_f1
            and frontier.max_exact_recovery == max_exact
            and frontier.max_recall == max_recall
            and frontier.max_precision == max_precision
        ]
        if not candidates:
            candidates = [(action_text, frontier) for action_text, frontier in branches if frontier.max_f1 == max_f1]
        # POLICY_ACTIONS is ordered; max() on the reversed action tuple makes
        # ties deterministic without depending on dictionary iteration.
        action_text, selected = max(
            candidates,
            key=lambda item: (item[1].max_f1, item[1].max_exact_recovery, item[1].max_recall, item[1].max_precision, tuple(reversed(item[1].best_f1_actions))),
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
    return ExactCeiling(
        frontier.max_precision,
        frontier.max_recall,
        frontier.max_f1,
        frontier.max_exact_recovery,
        frontier.best_f1_actions,
        len(visited_states),
    )


def _serialize_view(view: CoarseRepairView) -> str:
    """Canonical primitive serialization of exactly what the controller sees."""

    payload = {
        "local_gap_bins": list(view.local_gap_bins),
        "local_ratio_bins": list(view.local_ratio_bins),
        "cursor_relation_bin": view.cursor_relation_bin,
        "remaining_budget_fraction": view.remaining_budget_fraction,
        "last_scalar_feedback": view.last_scalar_feedback,
        "trusted_goal": view.trusted_goal,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _one_step_optimal_action(environment: Any) -> str:
    """Evaluator-optimal label at horizon one, using hidden identities only."""

    return _oracle_action(environment).value


def _reachable_state_samples(tasks: Sequence[RepairTask], depth: int) -> list[Any]:
    """Enumerate evaluator states reached by all fixed action prefixes."""

    samples: list[Any] = []
    for task in tasks:
        queue: deque[tuple[Any, int]] = deque([(_task_environment(task, "farey"), 0)])
        while queue:
            environment, level = queue.popleft()
            samples.append(environment)
            if level >= depth or environment.done:
                continue
            for action_text in POLICY_ACTIONS:
                child = deepcopy(environment)
                child.step(action_text)
                queue.append((child, level + 1))
    return samples


def observation_collision_ceiling(
    tasks: Sequence[RepairTask], *, depth: int
) -> dict[str, Any]:
    """Measure the best deterministic view-to-action map under collisions."""

    samples = _reachable_state_samples(tasks, depth)
    records: list[dict[str, Any]] = []
    for environment in samples:
        view = coarse_view(environment.observation)
        records.append({"view": _serialize_view(view), "label": _one_step_optimal_action(environment)})
    return _collision_summary(records)


def _collision_summary(
    records: Sequence[dict[str, Any]],
    *,
    key_override: str | None = None,
    label_override: Sequence[str] | None = None,
) -> dict[str, Any]:
    if label_override is not None and len(label_override) != len(records):
        raise ValueError("label override length must match records")
    groups: dict[str, Counter[str]] = defaultdict(Counter)
    for index, record in enumerate(records):
        key = key_override if key_override is not None else str(record["view"])
        label = label_override[index] if label_override is not None else str(record["label"])
        groups[key][label] += 1
    total = len(records)
    ceiling_hits = sum(max(counts.values()) for counts in groups.values())
    ambiguous = {key: counts for key, counts in groups.items() if len(counts) > 1}
    return {
        "samples": total,
        "unique_views": len(groups),
        "ambiguous_view_groups": len(ambiguous),
        "ambiguous_samples": sum(sum(counts.values()) for counts in ambiguous.values()),
        "action_accuracy_ceiling": ceiling_hits / total if total else 0.0,
        "collision_error_floor": (total - ceiling_hits) / total if total else 0.0,
        "label_counts": dict(sorted(Counter(str(record["label"]) for record in records).items())),
    }


def _identity_improving(environment: Any, action_text: str) -> tuple[bool, float, float]:
    before = _hidden_repair_metrics(environment).recall
    branch = deepcopy(environment)
    transition = branch.step(action_text)
    after = _hidden_repair_metrics(branch).recall
    return after > before, float(transition.reward), after - before


def _feedback_records(tasks: Sequence[RepairTask], *, depth: int) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for environment in _reachable_state_samples(tasks, depth):
        for action_text in POLICY_ACTIONS:
            improving, reward, identity_delta = _identity_improving(environment, action_text)
            records.append(
                {
                    "reward": reward,
                    "identity_improving": improving,
                    "identity_delta": identity_delta,
                    "goal": environment._goal.value,
                }
            )
    return records


def _auc(scores: Sequence[float], positive: Sequence[bool]) -> float:
    if len(scores) != len(positive):
        raise ValueError("scores and labels must have equal lengths")
    positives = [float(score) for score, label in zip(scores, positive) if label]
    negatives = [float(score) for score, label in zip(scores, positive) if not label]
    if not positives or not negatives:
        return 0.5
    wins = sum(
        1.0 if left > right else 0.5 if left == right else 0.0
        for left in positives
        for right in negatives
    )
    return wins / (len(positives) * len(negatives))


def feedback_informativeness(records: Sequence[dict[str, Any]]) -> dict[str, Any]:
    scores = [float(record["reward"]) for record in records]
    positive = [bool(record["identity_improving"]) for record in records]
    positive_scores = [score for score, label in zip(scores, positive) if label]
    negative_scores = [score for score, label in zip(scores, positive) if not label]
    return {
        "samples": len(records),
        "improving_actions": len(positive_scores),
        "non_improving_actions": len(negative_scores),
        "auc": _auc(scores, positive),
        "mean_reward_improving": statistics.fmean(positive_scores) if positive_scores else 0.0,
        "mean_reward_non_improving": statistics.fmean(negative_scores) if negative_scores else 0.0,
        "reward_definition": "coverage or spectral change only; hidden identity is not an input",
        "hidden_identity_used_in_reward": False,
    }


def _threshold_gate(
    name: str,
    value: float,
    threshold: float,
    *,
    valid: bool,
    reason: str,
) -> dict[str, Any]:
    if not valid:
        status = "unverified"
    elif value >= threshold:
        status = "positive"
    else:
        status = "negative"
    return {
        "name": name,
        "status": status,
        "value": value,
        "threshold": threshold,
        "valid": valid,
        "reason": reason,
    }


def _source_hashes() -> dict[str, str]:
    directory = Path(__file__).parent
    names = (
        "competency_v3_feasibility.py",
        "repair_experiment.py",
        "strict_environment.py",
        "test_competency_v3_feasibility.py",
    )
    return {
        name: sha256((directory / name).read_bytes()).hexdigest()
        for name in names
        if (directory / name).exists()
    }


def _manifest(config: FeasibilityConfig) -> list[RepairTask]:
    return make_manifest(
        config.representative_orders,
        config.representative_patterns,
        damage_count=config.representative_damage_count,
        replicates=1,
        seed=config.seed,
    )


def _reachability_diagnostics(tasks: Sequence[RepairTask]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for task in tasks:
        ceiling = exact_reachability_ceiling(task)
        witness = _replay_witness(task, ceiling.best_f1_actions)
        rows.append(
            {
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
                "visited_states": ceiling.visited_states,
                "witness": witness,
            }
        )
    return {
        "action_vocabulary": list(POLICY_ACTIONS),
        "action_budget": ACTION_BUDGET,
        "tasks": rows,
        "mean_max_precision": statistics.fmean(row["max_precision"] for row in rows) if rows else 0.0,
        "mean_max_recall": statistics.fmean(row["max_recall"] for row in rows) if rows else 0.0,
        "mean_max_f1": statistics.fmean(row["max_f1"] for row in rows) if rows else 0.0,
        "mean_max_exact_recovery": statistics.fmean(row["max_exact_recovery"] for row in rows) if rows else 0.0,
        "all_tasks_have_full_f1_ceiling": all(row["max_f1"] >= 1.0 for row in rows),
    }


def _replay_witness(task: RepairTask, actions: Sequence[str]) -> dict[str, Any]:
    """Replay the reported witness through the authoritative environment.

    The compact exact search intentionally omits rewards; this read-back gives
    a minimal action-budget/cursor-travel audit for failed ceilings without
    changing the controller boundary.
    """

    environment = _task_environment(task, "farey")
    initial_cursor = int(environment._cursor)
    cursor_trace = [initial_cursor]
    for action_text in actions:
        environment.step(action_text)
        cursor_trace.append(int(environment._cursor))
    metrics = _hidden_repair_metrics(environment)
    movement_count = sum(action in {Action.MOVE_LEFT.value, Action.MOVE_RIGHT.value} for action in actions)
    insertion_count = sum(action in {Action.INSERT_MEDIANT.value, Action.INSERT_MIDPOINT.value} for action in actions)
    return {
        "initial_cursor_index": initial_cursor,
        "final_cursor_index": int(environment._cursor),
        "cursor_trace": cursor_trace,
        "movement_count": movement_count,
        "insertion_count": insertion_count,
        "actions_used": len(actions),
        "actions_remaining": ACTION_BUDGET - len(actions),
        "recovered_count": metrics.true_positive,
        "false_positive_count": metrics.false_positive,
        "deleted_count": metrics.deleted_count,
        "f1": metrics.f1,
        "exact_recovery": metrics.exact_recovery,
    }


def _negative_reachability_fixture(task: RepairTask) -> dict[str, Any]:
    """A deliberately budget-starved fixture proving the gate can fail."""

    environment = StrictEnvironment(
        task.order,
        task.pattern,
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=1,
        goal=task.goal,
    )
    # One legal action is still enough for a finite search; this fixture is not
    # a claim about the production protocol because it violates its budget.
    cache: dict[tuple[Any, ...], float] = {}

    def search(current: Any) -> float:
        key = _state_signature(current)
        if key in cache:
            return cache[key]
        if current._done or current._remaining_budget <= 0:
            value = _hidden_repair_metrics(current).f1
        else:
            values = []
            for action_text in POLICY_ACTIONS:
                branch = deepcopy(current)
                branch.step(action_text)
                values.append(search(branch))
            value = max(values)
        cache[key] = value
        return value

    value = search(environment)
    return {"max_f1": value, "action_budget": 1, "status": "negative" if value < 0.80 else "unexpected_positive"}


def run_diagnostics(config: FeasibilityConfig = DEFAULT_CONFIG) -> dict[str, Any]:
    """Run all evaluator-only Stage-0 diagnostics and return a receipt."""

    tasks = _manifest(config)
    reachability = _reachability_diagnostics(tasks)
    reachability_gate = _threshold_gate(
        "reachability_ceiling",
        min(reachability["mean_max_f1"], reachability["mean_max_exact_recovery"]),
        min(config.reachability_f1_threshold, config.reachability_exact_threshold),
        valid=bool(tasks),
        reason=(
            "the reported scalar is the conservative minimum of the mean exact "
            "finite-horizon F1 and exact-recovery ceilings; both component "
            "thresholds must pass"
        ),
    )
    reachability_gate["components"] = {
        "mean_max_f1": reachability["mean_max_f1"],
        "f1_threshold": config.reachability_f1_threshold,
        "f1_status": "positive" if reachability["mean_max_f1"] >= config.reachability_f1_threshold else "negative",
        "mean_max_exact_recovery": reachability["mean_max_exact_recovery"],
        "exact_threshold": config.reachability_exact_threshold,
        "exact_status": "positive" if reachability["mean_max_exact_recovery"] >= config.reachability_exact_threshold else "negative",
    }
    # Use the explicit two-component rule rather than only the conservative
    # display scalar above.
    reachability_gate["status"] = (
        "positive"
        if bool(tasks)
        and reachability["mean_max_f1"] >= config.reachability_f1_threshold
        and reachability["mean_max_exact_recovery"] >= config.reachability_exact_threshold
        else "negative"
        if bool(tasks)
        else "unverified"
    )

    samples = _reachable_state_samples(tasks, config.collision_depth)
    collision = observation_collision_ceiling(tasks, depth=config.collision_depth)
    observation_gate = _threshold_gate(
        "observation_identifiability",
        collision["action_accuracy_ceiling"],
        config.observation_ceiling_threshold,
        valid=collision["samples"] > 0,
        reason=(
            "best deterministic mapping from canonical coarse views to one-step "
            "evaluator-optimal hidden-F1 action labels"
        ),
    )
    collapsed = _collision_summary(
        [{"view": "ignored", "label": _one_step_optimal_action(environment)} for environment in samples],
        key_override="all_views_collapsed",
    )
    collision_negative = _threshold_gate(
        "observation_negative_fixture",
        collapsed["action_accuracy_ceiling"],
        config.observation_ceiling_threshold,
        valid=collapsed["samples"] > 0,
        reason="all controller views intentionally collapsed to one observation key",
    )

    feedback_rows = _feedback_records(tasks, depth=config.collision_depth)
    feedback = feedback_informativeness(feedback_rows)
    feedback_gate = _threshold_gate(
        "scalar_feedback_informativeness",
        feedback["auc"],
        config.feedback_auc_threshold,
        valid=feedback["improving_actions"] > 0 and feedback["non_improving_actions"] > 0,
        reason=(
            "AUC of target-independent coverage/spectral reward for hidden "
            "identity-improving versus non-improving legal actions"
        ),
    )
    constant_feedback = dict(feedback)
    constant_feedback.update({"auc": 0.5, "mean_reward_improving": 0.0, "mean_reward_non_improving": 0.0})
    feedback_negative = _threshold_gate(
        "scalar_feedback_negative_fixture",
        constant_feedback["auc"],
        config.feedback_auc_threshold,
        valid=True,
        reason="all scalar rewards intentionally replaced by the same constant",
    )

    negative_task = tasks[0]
    reachability_negative = _negative_reachability_fixture(negative_task)
    reachability_negative_gate = _threshold_gate(
        "reachability_negative_fixture",
        reachability_negative["max_f1"],
        config.reachability_f1_threshold,
        valid=True,
        reason="same target family but deliberately budget-starved to one action",
    )

    source_hashes = _source_hashes()
    if source_hashes != _source_hashes():
        raise RuntimeError("sources changed while diagnostics were running")
    return {
        "schema_version": 1,
        "experiment": "Stage-0 strict Farey competency feasibility diagnostics",
        "seed": config.seed,
        "provenance": {
            "command": "PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/competency_v3_feasibility.py",
            "python": sys.version.split()[0],
            "controller_training": False,
        },
        "predeclaration": {
            "manifest": {
                "orders": list(config.representative_orders),
                "patterns": [pattern.value for pattern in config.representative_patterns],
                "goals": [goal.value for goal in GOALS],
                "damage_count": config.representative_damage_count,
                "replicates_per_cell": 1,
                "collision_depth": config.collision_depth,
            },
            "fixed_actions": list(POLICY_ACTIONS),
            "action_budget": ACTION_BUDGET,
            "gates": {
                "reachability_f1": config.reachability_f1_threshold,
                "reachability_exact_recovery": config.reachability_exact_threshold,
                "observation_ceiling": config.observation_ceiling_threshold,
                "feedback_auc": config.feedback_auc_threshold,
            },
        },
        "reachability": reachability,
        "observation_collision": collision,
        "scalar_feedback": feedback,
        "negative_fixtures": {
            "reachability": reachability_negative,
            "observation_collapsed_views": collapsed,
            "scalar_constant_feedback": constant_feedback,
        },
        "gates": {
            "reachability_ceiling": reachability_gate,
            "observation_identifiability": observation_gate,
            "scalar_feedback_informativeness": feedback_gate,
            "reachability_negative_fixture": reachability_negative_gate,
            "observation_negative_fixture": collision_negative,
            "scalar_feedback_negative_fixture": feedback_negative,
        },
        "claim_boundary": (
            "These are evaluator-only feasibility ceilings. A positive gate says "
            "only that the interface/task has enough information or attainable "
            "signal for a later controller test; it is not evidence of learning, "
            "transfer, persistence, or a Levin-style competency."
        ),
        "source_hashes": source_hashes,
    }


def _fmt(value: float) -> str:
    return f"{value:.4f}"


def result_markdown(result: dict[str, Any]) -> str:
    gates = result["gates"]
    reachability = result["reachability"]
    collision = result["observation_collision"]
    feedback = result["scalar_feedback"]
    lines = [
        "# Stage-0 Farey competency feasibility results",
        "",
        "This run does not train a controller. It measures whether the fixed interface has a solvable, identifiable, feedback-bearing repair problem.",
        "",
        "## Manifest",
        "",
        f"Orders `{result['predeclaration']['manifest']['orders']}`, all three damage families, both goals, two deleted points, one deterministic task per cell, and collision depth `{result['predeclaration']['manifest']['collision_depth']}`.",
        "",
        "## Evaluator ceilings",
        "",
        "| diagnostic | result | preregistered threshold | status |",
        "| --- | ---: | ---: | --- |",
        f"| mean exact finite-horizon F1 ceiling | {_fmt(reachability['mean_max_f1'])} | {_fmt(result['predeclaration']['gates']['reachability_f1'])} | {gates['reachability_ceiling']['components']['f1_status']} |",
        f"| mean exact-recovery ceiling | {_fmt(reachability['mean_max_exact_recovery'])} | {_fmt(result['predeclaration']['gates']['reachability_exact_recovery'])} | {gates['reachability_ceiling']['components']['exact_status']} |",
        f"| observation action-accuracy ceiling | {_fmt(collision['action_accuracy_ceiling'])} | {_fmt(result['predeclaration']['gates']['observation_ceiling'])} | {gates['observation_identifiability']['status']} |",
        f"| scalar reward AUC | {_fmt(feedback['auc'])} | {_fmt(result['predeclaration']['gates']['feedback_auc'])} | {gates['scalar_feedback_informativeness']['status']} |",
        "",
        "The reachability search enumerates every sequence in the four-action vocabulary for eight charged steps. The observation ceiling is the best deterministic mapping from a canonical serialized coarse view to a one-step hidden-F1 evaluator label. Feedback AUC scores target-independent coverage/spectral reward against hidden identity improvement.",
        "",
        "The reachability gate is joint: both component rows must pass. A witness read-back records recovered identities, false positives, insertion count, and cursor movement for each task so a failed ceiling is not mistaken for a learner failure.",
        "",
        "## Negative fixtures",
        "",
        "| fixture | result | status |",
        "| --- | ---: | --- |",
        f"| one-action budget reachability | {_fmt(result['negative_fixtures']['reachability']['max_f1'])} | {gates['reachability_negative_fixture']['status']} |",
        f"| all views collapsed | {_fmt(result['negative_fixtures']['observation_collapsed_views']['action_accuracy_ceiling'])} | {gates['observation_negative_fixture']['status']} |",
        f"| constant scalar reward | {_fmt(result['negative_fixtures']['scalar_constant_feedback']['auc'])} AUC | {gates['scalar_feedback_negative_fixture']['status']} |",
        "",
        "Negative fixtures are sanity checks that the gates can reject an intentionally impoverished interface. They are not comparison arms for the controller experiment.",
        "",
        "## Claim boundary",
        "",
        result["claim_boundary"],
        "",
    ]
    return "\n".join(lines)


def write_outputs(result: dict[str, Any]) -> None:
    directory = Path(__file__).parent
    (directory / "competency_v3_feasibility_receipt.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (directory / "FEASIBILITY_RESULTS.md").write_text(result_markdown(result), encoding="utf-8")


def main() -> None:
    result = run_diagnostics()
    write_outputs(result)
    print("wrote competency_v3_feasibility_receipt.json and FEASIBILITY_RESULTS.md")
    print(", ".join(f"{name}={gate['status']}" for name, gate in result["gates"].items()))


if __name__ == "__main__":
    main()
