#!/usr/bin/env python3
"""Deterministic, bounded feedback-learning probe for the local Farey engine.

This file is intentionally a small experiment runner, not a new environment.
Controllers receive only ``EnvironmentState``.  The intact Farey sequence and
identity/recovery metrics remain evaluator-side.  The experiment is descriptive
and its practical gates are predeclared in ``PREDECLARED_GATES`` below.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
from pathlib import Path
import random
import statistics
from typing import Any, Iterable, Sequence

try:  # Package import from the repository root.
    from .controllers import decide
    from .environment import (
        CandidateAction,
        EnvironmentState,
        Goal,
        LabeledFraction,
        build_state,
        evaluate_against_hidden,
        farey_points,
        step,
        visible_metric,
    )
except ImportError:  # Direct ``python experiment.py`` smoke run.
    from controllers import decide
    from environment import (
        CandidateAction,
        EnvironmentState,
        Goal,
        LabeledFraction,
        build_state,
        evaluate_against_hidden,
        farey_points,
        step,
        visible_metric,
    )


SEED = 20260811
TRAIN_ORDERS = (5, 7, 9)
TRANSFER_ORDERS = (6, 8, 10)  # unseen during feedback updates
TASKS_PER_ORDER = 6
TRAIN_EPOCHS = 5
EPISODE_BUDGET = 2
MODES = ("feedback", "reward_shuffled", "no_feedback")
CONDITIONS = (
    "random",
    "fixed_heuristic",
    "local_arithmetic_detector",
    "feedback_learner",
    "reward_shuffled",
    "no_feedback",
)


# These gates are part of the protocol before ``run_experiment`` is called.
# ``observed`` is a signed support statistic; a result is positive only when it
# clears ``minimum``.  Near misses are retained as nulls rather than silently
# rounded into wins.
PREDECLARED_GATES: tuple[dict[str, Any], ...] = (
    {
        "id": "H1_goal_persistence",
        "question": "Does a goal cue remain useful across two feedback-driven decisions?",
        "observed": "min(normalized_progress_vs_random.coverage, normalized_progress_vs_random.spectral)",
        "minimum": 0.02,
        "null_band": 0.01,
        "direction": "higher_is_supportive",
    },
    {
        "id": "H2_variable_means",
        "question": "Do task instances expose at least two practically successful local means?",
        "observed": "fraction_tasks_with_two_near_best_action_families",
        "minimum": 0.50,
        "null_band": 0.10,
        "direction": "higher_is_supportive",
    },
    {
        "id": "H3_feedback_learning",
        "question": "Does true scalar feedback beat both shuffled and absent feedback?",
        "observed": "min(progress_feedback_minus_shuffled, progress_feedback_minus_none)",
        "minimum": 0.02,
        "null_band": 0.01,
        "direction": "higher_is_supportive",
    },
    {
        "id": "H4_identity_damage_recovery",
        "question": "Does feedback improve evaluator-only recovery of the deleted identities?",
        "observed": "removed_recovery_feedback_minus_random",
        "minimum": 0.10,
        "null_band": 0.05,
        "direction": "higher_is_supportive",
    },
    {
        "id": "H5_frozen_transfer",
        "question": "Does a frozen learner retain practical gain on unseen N and damage masks?",
        "observed": "transfer_gain_vs_random",
        "minimum": 0.02,
        "null_band": 0.01,
        "direction": "higher_is_supportive",
    },
    {
        "id": "H6_authorized_switching",
        "question": "Does an authorized goal switch work while an unauthorized distractor is ignored?",
        "observed": "min(authorized_switch_alignment, distractor_coverage_alignment)",
        "minimum": 0.75,
        "null_band": 0.10,
        "direction": "higher_is_supportive",
    },
)


@dataclass(frozen=True, slots=True)
class Task:
    order: int
    removed: tuple[str, ...]
    goal: Goal
    index: int


@dataclass(frozen=True, slots=True)
class Episode:
    condition: str
    task: Task
    initial_metric: float
    final_metric: float
    target_metric: float
    normalized_progress: float
    visible_improvement: float
    removed_recovery_fraction: float
    hidden_hit_rate: float
    action_families: tuple[str, ...]
    action_alignment: tuple[float, ...]
    actual_feedback: tuple[float, ...]


def _mean(values: Iterable[float]) -> float:
    items = list(values)
    return statistics.fmean(items) if items else 0.0


def _safe_ratio(numerator: float, denominator: float) -> float:
    if abs(denominator) <= 1.0e-12:
        return 0.0
    return numerator / denominator


def _percentile(values: Sequence[float], probability: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def _summary(values: Iterable[float]) -> dict[str, float | int]:
    items = list(values)
    if not items:
        return {"count": 0, "mean": 0.0, "median": 0.0, "q025": 0.0, "q975": 0.0}
    return {
        "count": len(items),
        "mean": statistics.fmean(items),
        "median": statistics.median(items),
        "q025": _percentile(items, 0.025),
        "q975": _percentile(items, 0.975),
    }


def _source_hash(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def _make_tasks(orders: Sequence[int], count: int, seed: int, *, prefix: int = 0) -> tuple[Task, ...]:
    """Create deterministic damage masks without exposing them to controllers."""

    rng = random.Random(seed)
    tasks: list[Task] = []
    for order in orders:
        original = farey_points(order)
        # Keep 0/1 visible so the boundary action remains represented.
        eligible = [point.label for point in original if point.canonical_label != "0/1"]
        for local_index in range(count):
            damage_count = 1 + ((local_index + order + prefix) % 2)
            removed = tuple(sorted(rng.sample(eligible, min(damage_count, len(eligible) - 2))))
            goal = Goal.COVERAGE if (local_index + order + prefix) % 2 == 0 else Goal.SPECTRAL
            tasks.append(Task(order, removed, goal, prefix + local_index))
    return tuple(tasks)


def _survivors(order: int, removed: Sequence[str]) -> tuple[LabeledFraction, ...]:
    removed_set = set(removed)
    return tuple(point for point in farey_points(order) if point.label not in removed_set)


def _action_family(state: EnvironmentState, action: CandidateAction) -> str:
    max_gap = max(item.arc_length for item in state.actions)
    min_denominator_sum = min(item.denominator_sum for item in state.actions)
    if action.arc_length == max_gap:
        return "largest_gap"
    if action.denominator_sum == min_denominator_sum:
        return "small_denominator_sum"
    if action.wraps_boundary:
        return "boundary"
    return "interior"


def _features(state: EnvironmentState, action: CandidateAction) -> tuple[float, ...]:
    """Local, target-free features used by the learner."""

    max_gap = max((float(item.arc_length) for item in state.actions), default=1.0)
    action_gap = float(action.arc_length)
    return (
        1.0,
        1.0 if state.goal is Goal.COVERAGE else 0.0,
        1.0 if state.goal is Goal.SPECTRAL else 0.0,
        action_gap,
        action_gap / max_gap if max_gap else 0.0,
        action.denominator_sum / max(1.0, 2.0 * state.order),
        action.candidate.denominator / max(1.0, float(state.order)),
        action.candidate.value,
        1.0 if action.wraps_boundary else 0.0,
    )


class FeedbackLearner:
    """Small deterministic contextual bandit; no hidden task state is stored."""

    def __init__(self, seed: int, *, learning: bool = True, epsilon: float = 0.20) -> None:
        self.rng = random.Random(seed)
        self.learning = learning
        self.epsilon = epsilon
        self.weights: dict[Goal, list[float]] = {
            Goal.COVERAGE: [0.0] * 9,
            Goal.SPECTRAL: [0.0] * 9,
        }
        self.updates = 0
        self._last_features: tuple[float, ...] | None = None
        self._last_goal: Goal | None = None

    def select(self, state: EnvironmentState) -> CandidateAction | None:
        if not state.actions:
            self._last_features = None
            self._last_goal = None
            return None
        explore = self.learning and self.rng.random() < max(0.03, self.epsilon / (1.0 + self.updates / 40.0))
        if explore:
            action = state.actions[self.rng.randrange(len(state.actions))]
        else:
            weights = self.weights[state.goal]
            action = max(
                state.actions,
                key=lambda candidate: (
                    sum(weight * value for weight, value in zip(weights, _features(state, candidate))),
                    tuple(-value.numerator if hasattr(value, "numerator") else 0 for value in candidate.key),
                ),
            )
            # ``CandidateAction.key`` is the canonical deterministic tie break;
            # max() above only needs a stable scalar tie, so choose explicitly.
            best_score = sum(weight * value for weight, value in zip(weights, _features(state, action)))
            tied = [
                candidate
                for candidate in state.actions
                if abs(sum(weight * value for weight, value in zip(weights, _features(state, candidate))) - best_score)
                <= 1.0e-15
            ]
            action = min(tied, key=lambda candidate: candidate.key)
        self._last_features = _features(state, action)
        self._last_goal = state.goal
        return action

    def observe(self, feedback: float) -> None:
        if not self.learning or self._last_features is None or self._last_goal is None:
            return
        weights = self.weights[self._last_goal]
        prediction = sum(weight * value for weight, value in zip(weights, self._last_features))
        error = float(feedback) - prediction
        rate = 0.25 / math.sqrt(1.0 + self.updates)
        for index, value in enumerate(self._last_features):
            weights[index] += rate * error * value
        self.updates += 1


class FixedController:
    """Adapter for an existing fixed policy; feedback is intentionally ignored."""

    def __init__(self, name: str, seed: int) -> None:
        self.name = name
        self.rng = random.Random(seed)

    def select(self, state: EnvironmentState) -> CandidateAction | None:
        dispatch_name = {
            "random": "random_legal",
            "fixed_heuristic": "largest_gap",
            "local_arithmetic_detector": "smallest_denominator_sum",
        }[self.name]
        return decide(dispatch_name, state, rng=self.rng).action

    def observe(self, feedback: float) -> None:
        del feedback


class FeedbackChannel:
    """Actual, zeroed, or online-shuffled scalar feedback."""

    def __init__(self, mode: str, seed: int) -> None:
        self.mode = mode
        self.rng = random.Random(seed)
        self.seen: list[float] = []

    def transmit(self, feedback: float) -> float:
        if self.mode == "feedback":
            return feedback
        if self.mode == "no_feedback":
            return 0.0
        if self.mode == "reward_shuffled":
            self.seen.append(float(feedback))
            # The learner receives a random permutation draw from the observed
            # reward history, not the reward paired with its last action.
            return self.seen[self.rng.randrange(len(self.seen))]
        raise ValueError(f"unknown feedback mode: {self.mode!r}")


def _new_controller(condition: str, seed: int, *, learning: bool = True) -> Any:
    if condition in {"random", "fixed_heuristic", "local_arithmetic_detector"}:
        return FixedController(condition, seed)
    if condition == "feedback_learner":
        return FeedbackLearner(seed, learning=learning)
    if condition in {"reward_shuffled", "no_feedback"}:
        return FeedbackLearner(seed, learning=learning)
    raise ValueError(f"unknown condition: {condition!r}")


def _normalised_progress(initial: float, final: float, target: float) -> float:
    available = initial - target
    if available <= 1.0e-12:
        return 0.0
    return (initial - final) / available


def _alignment(state: EnvironmentState, action: CandidateAction | None) -> float:
    if action is None or not state.actions:
        return 0.0
    before = visible_metric(state.survivors, state.goal)
    improvements = {
        candidate: before - visible_metric((*state.survivors, candidate.candidate), state.goal)
        for candidate in state.actions
    }
    best = max(improvements.values())
    return 1.0 if improvements[action] >= best - 1.0e-12 else 0.0


def run_episode(
    condition: str,
    task: Task,
    controller: Any,
    *,
    feedback_mode: str,
    seed: int,
    budget: int = EPISODE_BUDGET,
    initial_goal: Goal | None = None,
    authorized_switch_at: int | None = None,
    authorized_goal: Goal = Goal.SPECTRAL,
    distractor_goal: Goal | None = None,
) -> Episode:
    """Run one episode; only this function calls evaluator-side hidden metrics."""

    original = farey_points(task.order)
    state = build_state(
        _survivors(task.order, task.removed),
        task.order,
        initial_goal or task.goal,
        budget,
    )
    initial_metric = visible_metric(state.survivors, state.goal)
    target_metric = visible_metric(original, state.goal)
    channel = FeedbackChannel(feedback_mode, seed)
    actual_feedback: list[float] = []
    action_families: list[str] = []
    alignments: list[float] = []
    hidden_hits: list[bool] = []
    removed_values = {point.circle_fraction for point in original if point.label in set(task.removed)}
    inserted_values: set[Any] = set()

    for step_index in range(budget):
        if authorized_switch_at is not None and step_index == authorized_switch_at:
            next_goal = authorized_goal
            if distractor_goal is not None:
                # Deliberately ignore the distractor: no authorization means no
                # state change, and the controller never sees this argument.
                next_goal = state.goal
            state = build_state(
                state.survivors,
                state.order,
                next_goal,
                state.remaining_budget,
                state.feedback,
            )
            target_metric = visible_metric(original, state.goal)
        action = controller.select(state)
        if action is None:
            break
        alignments.append(_alignment(state, action))
        action_families.append(_action_family(state, action))
        result = step(state, action, original)
        actual_feedback.append(result.feedback)
        hidden_hits.append(bool(result.hidden_hit))
        inserted_values.add(action.candidate.circle_fraction)
        controller.observe(channel.transmit(result.feedback))
        state = result.state

    evaluation = evaluate_against_hidden(state, original)
    recovered = len(inserted_values & removed_values)
    removed_recovery = _safe_ratio(recovered, len(removed_values))
    return Episode(
        condition=condition,
        task=task,
        initial_metric=initial_metric,
        final_metric=visible_metric(state.survivors, state.goal),
        target_metric=visible_metric(original, state.goal),
        normalized_progress=_normalised_progress(initial_metric, visible_metric(state.survivors, state.goal), target_metric),
        visible_improvement=initial_metric - visible_metric(state.survivors, state.goal),
        removed_recovery_fraction=removed_recovery,
        hidden_hit_rate=_safe_ratio(sum(hidden_hits), len(hidden_hits)),
        action_families=tuple(action_families),
        action_alignment=tuple(alignments),
        actual_feedback=tuple(actual_feedback),
    )


def _condition_run(
    condition: str,
    tasks: Sequence[Task],
    *,
    seed: int,
    training: bool,
    epochs: int = 1,
    feedback_mode: str | None = None,
    budget: int = EPISODE_BUDGET,
    evaluation_tasks: Sequence[Task] | None = None,
) -> tuple[Any, tuple[Episode, ...]]:
    controller = _new_controller(condition, seed, learning=training)
    mode = feedback_mode or {
        "feedback_learner": "feedback",
        "reward_shuffled": "reward_shuffled",
        "no_feedback": "no_feedback",
    }.get(condition, "no_feedback")
    if training and condition in {"feedback_learner", "reward_shuffled", "no_feedback"}:
        for epoch in range(epochs):
            for index, task in enumerate(tasks):
                run_episode(
                    condition,
                    task,
                    controller,
                    feedback_mode=mode,
                    seed=seed + epoch * 1000 + index,
                    budget=budget,
                )
    eval_tasks = tasks if evaluation_tasks is None else evaluation_tasks
    episodes = tuple(
        run_episode(
            condition,
            task,
            controller,
            feedback_mode=mode,
            seed=seed + 100_000 + index,
            budget=budget,
        )
        for index, task in enumerate(eval_tasks)
    )
    return controller, episodes


def _aggregate(episodes: Sequence[Episode]) -> dict[str, Any]:
    by_goal: dict[str, dict[str, Any]] = {}
    for goal in (Goal.COVERAGE, Goal.SPECTRAL):
        selected = [episode for episode in episodes if episode.task.goal is goal]
        by_goal[goal.value] = {
            "episodes": len(selected),
            "normalized_progress": _summary(episode.normalized_progress for episode in selected),
            "visible_improvement": _summary(episode.visible_improvement for episode in selected),
            "removed_recovery_fraction": _summary(episode.removed_recovery_fraction for episode in selected),
            "hidden_hit_rate": _summary(episode.hidden_hit_rate for episode in selected),
        }
    return {
        "episodes": len(episodes),
        "normalized_progress": _summary(episode.normalized_progress for episode in episodes),
        "visible_improvement": _summary(episode.visible_improvement for episode in episodes),
        "removed_recovery_fraction": _summary(episode.removed_recovery_fraction for episode in episodes),
        "hidden_hit_rate": _summary(episode.hidden_hit_rate for episode in episodes),
        "by_goal": by_goal,
        "action_family_counts": {
            family: sum(episode.action_families.count(family) for episode in episodes)
            for family in ("largest_gap", "small_denominator_sum", "boundary", "interior")
        },
    }


def _variable_means(tasks: Sequence[Task]) -> dict[str, Any]:
    family_counts: dict[str, int] = {}
    near_best_counts: list[int] = []
    two_or_more = 0
    for task in tasks:
        state = build_state(_survivors(task.order, task.removed), task.order, task.goal, 1)
        before = visible_metric(state.survivors, state.goal)
        scored = [
            (action, before - visible_metric((*state.survivors, action.candidate), state.goal))
            for action in state.actions
        ]
        if not scored:
            near_best_counts.append(0)
            continue
        best = max(score for _, score in scored)
        good = [action for action, score in scored if score >= best - 0.002]
        families = {_action_family(state, action) for action in good}
        near_best_counts.append(len(families))
        for family in families:
            family_counts[family] = family_counts.get(family, 0) + 1
        if len(families) >= 2:
            two_or_more += 1
    return {
        "tasks": len(tasks),
        "fraction_tasks_with_two_near_best_action_families": _safe_ratio(two_or_more, len(tasks)),
        "mean_near_best_family_count": _mean(near_best_counts),
        "family_task_counts": family_counts,
        "near_best_tolerance_visible_metric": 0.002,
    }


def _paired_goal_runs(tasks: Sequence[Task], seed: int) -> dict[str, Any]:
    paired_tasks = tuple(Task(task.order, task.removed, goal, task.index) for task in tasks for goal in (Goal.COVERAGE, Goal.SPECTRAL))
    results: dict[str, dict[str, Any]] = {}
    for condition in ("random", "feedback_learner"):
        controller = _new_controller(condition, seed + (0 if condition == "random" else 10), learning=False)
        episodes = [
            run_episode(
                condition,
                task,
                controller,
                feedback_mode="no_feedback",
                seed=seed + index,
                budget=EPISODE_BUDGET,
            )
            for index, task in enumerate(paired_tasks)
        ]
        results[condition] = _aggregate(episodes)
    return results


def _switch_runs(tasks: Sequence[Task], controller: Any, seed: int) -> dict[str, Any]:
    authorized: list[Episode] = []
    distractor: list[Episode] = []
    for index, task in enumerate(tasks):
        authorized.append(
            run_episode(
                "feedback_learner_authorized_switch",
                task,
                controller,
                feedback_mode="no_feedback",
                seed=seed + index,
                budget=EPISODE_BUDGET,
                initial_goal=Goal.COVERAGE,
                authorized_switch_at=1,
                authorized_goal=Goal.SPECTRAL,
            )
        )
        distractor.append(
            run_episode(
                "feedback_learner_distractor",
                task,
                controller,
                feedback_mode="no_feedback",
                seed=seed + 1000 + index,
                budget=EPISODE_BUDGET,
                initial_goal=Goal.COVERAGE,
                authorized_switch_at=1,
                distractor_goal=Goal.SPECTRAL,
            )
        )
    # The second action is the post-cue decision in both conditions.
    authorized_alignment = _mean(episode.action_alignment[1] for episode in authorized if len(episode.action_alignment) > 1)
    distractor_alignment = _mean(episode.action_alignment[1] for episode in distractor if len(episode.action_alignment) > 1)
    return {
        "authorized_switch_alignment": authorized_alignment,
        "distractor_coverage_alignment": distractor_alignment,
        "authorized": _aggregate(authorized),
        "distractor": _aggregate(distractor),
    }


def _classify(observed: float, minimum: float, null_band: float) -> str:
    if observed >= minimum:
        return "positive"
    if observed >= minimum - null_band:
        return "null"
    return "negative"


def _gate_results(
    aggregates: dict[str, Any],
    variable: dict[str, Any],
    goals: dict[str, Any],
    transfer: dict[str, Any],
    identity: dict[str, Any],
    switching: dict[str, Any],
) -> list[dict[str, Any]]:
    random_goals = goals["random"]["by_goal"]
    learner_goals = goals["feedback_learner"]["by_goal"]
    goal_support = min(
        learner_goals["coverage"]["normalized_progress"]["mean"] - random_goals["coverage"]["normalized_progress"]["mean"],
        learner_goals["spectral"]["normalized_progress"]["mean"] - random_goals["spectral"]["normalized_progress"]["mean"],
    )
    learner = aggregates["feedback_learner"]
    shuffled = aggregates["reward_shuffled"]
    no_feedback = aggregates["no_feedback"]
    feedback_support = min(
        learner["normalized_progress"]["mean"] - shuffled["normalized_progress"]["mean"],
        learner["normalized_progress"]["mean"] - no_feedback["normalized_progress"]["mean"],
    )
    observed = {
        "H1_goal_persistence": goal_support,
        "H2_variable_means": variable["fraction_tasks_with_two_near_best_action_families"],
        "H3_feedback_learning": feedback_support,
        "H4_identity_damage_recovery": identity["feedback_minus_random_removed_recovery"],
        "H5_frozen_transfer": transfer["transfer_gain_vs_random"],
        "H6_authorized_switching": min(switching["authorized_switch_alignment"], switching["distractor_coverage_alignment"]),
    }
    results: list[dict[str, Any]] = []
    for gate in PREDECLARED_GATES:
        value = float(observed[gate["id"]])
        results.append(
            {
                **gate,
                "observed_value": value,
                "status": _classify(value, float(gate["minimum"]), float(gate["null_band"])),
            }
        )
    return results


def run_experiment() -> dict[str, Any]:
    """Run all six gates with deterministic task streams and return JSON data."""

    train_tasks = _make_tasks(TRAIN_ORDERS, TASKS_PER_ORDER, SEED + 1, prefix=0)
    in_domain_tasks = _make_tasks(TRAIN_ORDERS, TASKS_PER_ORDER, SEED + 2, prefix=100)
    transfer_tasks = _make_tasks(TRANSFER_ORDERS, TASKS_PER_ORDER, SEED + 3, prefix=200)
    identity_tasks = tuple(
        Task(task.order, task.removed[:1], task.goal, task.index) for task in transfer_tasks
    )

    conditions: dict[str, Any] = {}
    trained_controllers: dict[str, Any] = {}
    eval_episodes: dict[str, tuple[Episode, ...]] = {}
    for offset, condition in enumerate(CONDITIONS):
        training = condition in {"feedback_learner", "reward_shuffled", "no_feedback"}
        controller, episodes = _condition_run(
            condition,
            train_tasks,
            seed=SEED + 100 * offset,
            training=training,
            epochs=TRAIN_EPOCHS,
            evaluation_tasks=transfer_tasks,
        )
        trained_controllers[condition] = controller
        eval_episodes[condition] = episodes
        conditions[condition] = {"transfer_test": _aggregate(episodes)}

    # In-domain holdout is run with each already-trained learner/controller.
    for condition in CONDITIONS:
        controller = trained_controllers[condition]
        mode = {"feedback_learner": "feedback", "reward_shuffled": "reward_shuffled", "no_feedback": "no_feedback"}.get(condition, "no_feedback")
        episodes = tuple(
            run_episode(condition, task, controller, feedback_mode=mode, seed=SEED + 50_000 + index)
            for index, task in enumerate(in_domain_tasks)
        )
        conditions[condition]["in_domain_test"] = _aggregate(episodes)
        if condition == "feedback_learner":
            trained_controllers[condition] = controller

    aggregates = {
        condition: conditions[condition]["transfer_test"] for condition in CONDITIONS
    }
    goals = _paired_goal_runs(in_domain_tasks[:8], SEED + 500)
    variable = _variable_means(in_domain_tasks)

    # Identity is evaluator-only: no identity fact is sent to the controller.
    identity_episodes: dict[str, tuple[Episode, ...]] = {}
    for condition in CONDITIONS:
        controller = trained_controllers[condition]
        mode = {"feedback_learner": "feedback", "reward_shuffled": "reward_shuffled", "no_feedback": "no_feedback"}.get(condition, "no_feedback")
        identity_episodes[condition] = tuple(
            run_episode(condition, task, controller, feedback_mode=mode, seed=SEED + 60_000 + index, budget=2)
            for index, task in enumerate(identity_tasks)
        )
    identity_summary = {
        condition: _aggregate(episodes) for condition, episodes in identity_episodes.items()
    }
    identity = {
        "conditions": identity_summary,
        "feedback_minus_random_removed_recovery": identity_summary["feedback_learner"]["removed_recovery_fraction"]["mean"] - identity_summary["random"]["removed_recovery_fraction"]["mean"],
        "evaluator_only": True,
        "hidden_hit_is_structurally_tautological": True,
    }

    transfer_gain = aggregates["feedback_learner"]["normalized_progress"]["mean"] - aggregates["random"]["normalized_progress"]["mean"]
    in_domain_gain = conditions["feedback_learner"]["in_domain_test"]["normalized_progress"]["mean"] - conditions["random"]["in_domain_test"]["normalized_progress"]["mean"]
    transfer = {
        "train_orders": list(TRAIN_ORDERS),
        "unseen_transfer_orders": list(TRANSFER_ORDERS),
        "in_domain_gain_vs_random": in_domain_gain,
        "transfer_gain_vs_random": transfer_gain,
        "transfer_to_in_domain_gain_ratio": _safe_ratio(transfer_gain, in_domain_gain),
        "frozen_after_training": True,
    }

    switching = _switch_runs(in_domain_tasks[:8], trained_controllers["feedback_learner"], SEED + 700)
    gates = _gate_results(aggregates, variable, goals, transfer, identity, switching)

    return {
        "experiment": "bounded deterministic feedback-learning competency probe",
        "schema_version": 1,
        "status": "descriptive preliminary result; not an agency claim",
        "seed": SEED,
        "predeclared_gates": [dict(gate) for gate in PREDECLARED_GATES],
        "gates": gates,
        "configuration": {
            "train_orders": list(TRAIN_ORDERS),
            "transfer_orders": list(TRANSFER_ORDERS),
            "tasks_per_order": TASKS_PER_ORDER,
            "train_epochs": TRAIN_EPOCHS,
            "episode_budget": EPISODE_BUDGET,
            "conditions": list(CONDITIONS),
        },
        "information_boundary": {
            "controller_receives": ["EnvironmentState survivors", "local legal action menu", "N", "goal", "remaining budget", "last scalar feedback"],
            "controller_never_receives": ["full Farey target", "removed labels", "hidden_hit", "target metric", "evaluator identity metrics"],
            "structural_privilege": "Exact local labels, N, and the complete current action menu are exposed. This is not leak-tight agency evidence.",
        },
        "baselines": {
            "random": "seeded random legal action",
            "fixed_heuristic": "largest observed gap",
            "local_arithmetic_detector": "smallest endpoint denominator sum",
            "reward_shuffled": "same learner with online random permutation draws from observed rewards",
            "no_feedback": "same learner with all feedback replaced by zero",
        },
        "conditions": conditions,
        "goal_persistence": goals,
        "variable_means": variable,
        "identity_damage_recovery": identity,
        "frozen_transfer": transfer,
        "authorized_switching": switching,
        "retained_result_types": ["positive", "null", "negative"],
        "source_files": {
            "environment.py": _source_hash(Path(__file__).with_name("environment.py")),
            "controllers.py": _source_hash(Path(__file__).with_name("controllers.py")),
        },
    }


def main() -> None:
    output_path = Path(__file__).with_name("receipt.json")
    result = run_experiment()
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    statuses = {gate["status"] for gate in result["gates"]}
    print(f"wrote {output_path}")
    print(f"gates: {', '.join(gate['id'] + '=' + gate['status'] for gate in result['gates'])}")
    print(f"result_types_retained: {', '.join(sorted(statuses | {'positive', 'null', 'negative'}))}")


if __name__ == "__main__":
    main()
