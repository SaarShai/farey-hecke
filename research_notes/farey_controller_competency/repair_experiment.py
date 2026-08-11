#!/usr/bin/env python3
"""Leak-tight repair-only experiment over the strict Farey shell.

The learner sees only :class:`CoarseRepairView`: four quantized local gaps,
two local ratios, a quantized cursor relation, budget, scalar feedback, and a
trusted goal bit.  In particular, it is never passed an order, a fraction,
the survivor or target sets, deletion ranks, a target metric, or the evaluator
arm.  Policies use the four nonterminal fixed actions from
``strict_environment``—move left/right and insert mediant/midpoint—and every
chosen action is charged.  STOP is unavailable so every training episode has
the same eight update opportunities.

This is a finite deterministic competency probe.  It reports null and
unverified gates as such; it does not make an agency claim.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, replace
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import random
import statistics
import sys
from typing import Any, Iterable, Protocol, Sequence

try:  # Package import.
    from .strict_environment import (
        ACTIONS,
        Action,
        DamagePattern,
        GoalState,
        StrictEnvironment,
        StrictObservation,
        StrictTransition,
        UntrustedCue,
        _circular_distance,
        _coverage,
        _gap_bin,
        _ratio_bin,
        _round_reward,
        _spectral,
    )
except ImportError:  # Direct script execution from this directory.
    from strict_environment import (  # type: ignore[no-redef]
        ACTIONS,
        Action,
        DamagePattern,
        GoalState,
        StrictEnvironment,
        StrictObservation,
        StrictTransition,
        UntrustedCue,
        _circular_distance,
        _coverage,
        _gap_bin,
        _ratio_bin,
        _round_reward,
        _spectral,
    )


class ExactGapScrambleAdapter(Protocol):
    """Evaluator-side interface supplied by ``repair_ablation``.

    This interface intentionally contains rank masks and exact points because
    it is used only before a controller view is constructed.  The module is
    imported, never copied into this experiment.
    """

    def exact_gap_scramble(self, points: Sequence[Fraction], seed: int = 0) -> Any: ...

    def map_rank_damage(self, mask: Iterable[int], result: Any) -> tuple[int, ...]: ...


try:
    from .repair_ablation import exact_gap_scramble, map_rank_damage
except ImportError:
    try:
        from repair_ablation import exact_gap_scramble, map_rank_damage  # type: ignore[no-redef]
    except ImportError as error:  # A clean interface remains when integration is pending.
        exact_gap_scramble = None  # type: ignore[assignment]
        map_rank_damage = None  # type: ignore[assignment]
        _ABLATON_IMPORT_ERROR = f"{type(error).__name__}: {error}"
    else:
        _ABLATON_IMPORT_ERROR = None
else:
    _ABLATON_IMPORT_ERROR = None


SEED = 20260811
TRAIN_ORDERS = (6, 7, 8, 9, 10)
TEST_ORDERS = (11, 13, 17)
TRAIN_PATTERN = DamagePattern.RANDOM_ISOLATED
TEST_PATTERNS = (
    DamagePattern.RANDOM_ISOLATED,
    DamagePattern.BURST,
    DamagePattern.DENOMINATOR_BIASED,
)
GOALS = (GoalState.COVERAGE, GoalState.SPECTRAL)
ACTION_BUDGET = 8
# Repair-only policies cannot terminate training early. This keeps every
# feedback condition at the same eight charged decisions per episode.
POLICY_ACTIONS = tuple(action for action in ACTIONS if action != Action.STOP.value)


@dataclass(frozen=True, slots=True)
class ExperimentConfig:
    """Preregistered compact experiment sizes and practical margins."""

    seed: int = SEED
    train_episodes: int = 1_000
    train_replicates_per_order_goal: int = 12
    in_domain_replicates_per_order_goal: int = 10
    test_replicates_per_cell: int = 10
    bootstrap_resamples: int = 600
    action_budget: int = ACTION_BUDGET
    feedback_f1_margin: float = 0.03
    recovery_f1_margin: float = 0.03
    transfer_f1_margin: float = 0.03
    structural_f1_margin: float = 0.02

    def __post_init__(self) -> None:
        if self.action_budget != ACTION_BUDGET:
            raise ValueError("repair action budget is fixed at eight")


DEFAULT_CONFIG = ExperimentConfig()


@dataclass(frozen=True, slots=True)
class RepairTask:
    """Evaluator-owned episode specification; never supplied to policies."""

    order: int
    pattern: DamagePattern
    goal: GoalState
    seed: int
    damage_count: int

    @property
    def cell(self) -> tuple[int, str, str]:
        return (self.order, self.pattern.value, self.goal.value)


@dataclass(frozen=True, slots=True)
class CoarseRepairView:
    """The entire fixed controller observation.

    Fields deliberately contain no target, population, identity, arm, family,
    exact coordinate, order, mask, action menu, or metric value.
    """

    local_gap_bins: tuple[int, int, int, int]
    local_ratio_bins: tuple[int, int]
    cursor_relation_bin: int
    remaining_budget_fraction: float
    last_scalar_feedback: float
    trusted_goal: int

    def __post_init__(self) -> None:
        if len(self.local_gap_bins) != 4 or any(
            type(value) is not int or not 0 <= value <= 15 for value in self.local_gap_bins
        ):
            raise ValueError("local_gap_bins must be four bins in [0, 15]")
        if len(self.local_ratio_bins) != 2 or any(
            type(value) is not int or not 0 <= value <= 15 for value in self.local_ratio_bins
        ):
            raise ValueError("local_ratio_bins must be two bins in [0, 15]")
        if type(self.cursor_relation_bin) is not int or not -8 <= self.cursor_relation_bin <= 8:
            raise ValueError("cursor_relation_bin must be in [-8, 8]")
        if type(self.remaining_budget_fraction) is not float or not 0.0 <= self.remaining_budget_fraction <= 1.0:
            raise ValueError("remaining budget must be a fraction in [0, 1]")
        if type(self.last_scalar_feedback) is not float:
            raise TypeError("last scalar feedback must be a float")
        if type(self.trusted_goal) is not int or self.trusted_goal not in (0, 1):
            raise ValueError("trusted_goal must be 0 (coverage) or 1 (spectral)")

    def features(self) -> tuple[float, ...]:
        """Fixed numeric encoding used by the learned and visible policies."""

        return (
            1.0,
            *(value / 15.0 for value in self.local_gap_bins),
            *(value / 15.0 for value in self.local_ratio_bins),
            self.cursor_relation_bin / 8.0,
            self.remaining_budget_fraction,
            max(-1.0, min(1.0, self.last_scalar_feedback * 40.0)),
            float(self.trusted_goal),
        )


def coarse_view(
    observation: StrictObservation, *, visible_feedback: float | None = None
) -> CoarseRepairView:
    """Erase every strict-shell channel except the preregistered coarse view."""

    return CoarseRepairView(
        observation.neighbor_gap_bins,
        observation.neighbor_gap_ratio_bins,
        observation.cursor_position_bin,
        observation.remaining_budget_fraction,
        observation.last_scalar_reward if visible_feedback is None else float(visible_feedback),
        0 if observation.trusted_goal_state is GoalState.COVERAGE else 1,
    )


@dataclass(frozen=True, slots=True)
class HiddenRepairMetrics:
    """Evaluator-only exact repair accounting; never placed in a view."""

    precision: float
    recall: float
    f1: float
    exact_recovery: float
    true_positive: int
    false_positive: int
    deleted_count: int


class _PointSetRepairEnvironment:
    """Strict-shell-compatible evaluator adapter for a scrambled target.

    This is intentionally only an environment adapter.  Exact-gap scrambling,
    rank mapping, and structural proof come from ``repair_ablation``.
    """

    __slots__ = (
        "_target",
        "_deleted_indices",
        "_deleted_points",
        "_initial_points",
        "_points",
        "_cursor",
        "_initial_cursor",
        "_remaining_budget",
        "_action_budget",
        "_goal",
        "_last_reward",
        "_done",
    )

    def __init__(
        self,
        target: Sequence[Fraction],
        deleted_indices: Iterable[int],
        *,
        seed: int,
        goal: GoalState,
        action_budget: int,
    ) -> None:
        self._target = tuple(sorted(set(point % 1 for point in target)))
        if not self._target:
            raise ValueError("scrambled target must contain a point")
        self._deleted_indices = tuple(sorted(set(int(index) for index in deleted_indices)))
        if not self._deleted_indices or self._deleted_indices[-1] >= len(self._target):
            raise ValueError("scrambled rank mask is outside the target")
        self._deleted_points = tuple(self._target[index] for index in self._deleted_indices)
        deleted = set(self._deleted_points)
        self._initial_points = tuple(point for point in self._target if point not in deleted)
        if not self._initial_points:
            raise ValueError("scrambled rank mask must leave a survivor")
        self._points = self._initial_points
        self._initial_cursor = random.Random(seed ^ 0x5EED).randrange(len(self._points))
        self._cursor = self._initial_cursor
        self._remaining_budget = action_budget
        self._action_budget = action_budget
        self._goal = GoalState.coerce(goal)
        self._last_reward = 0.0
        self._done = False

    @property
    def observation(self) -> StrictObservation:
        return self._make_observation()

    @property
    def done(self) -> bool:
        return self._done

    @property
    def evaluator_metrics(self) -> Any:
        visible = set(self._points)
        recovered = sum(point in visible for point in self._deleted_points)
        identity = recovered / len(self._deleted_points) if self._deleted_points else 1.0
        return type(
            "EvaluatorMetrics",
            (),
            {"identity_recovery": identity, "coverage": _coverage(self._points), "spectral": _spectral(self._points)},
        )()

    def step(self, action: Action | str) -> StrictTransition:
        if self._done:
            raise RuntimeError("episode is already done")
        chosen = Action.coerce(action)
        before = self._goal_metric()
        self._remaining_budget -= 1
        changed = False
        if chosen is Action.MOVE_LEFT:
            self._cursor = (self._cursor - 1) % len(self._points)
        elif chosen is Action.MOVE_RIGHT:
            self._cursor = (self._cursor + 1) % len(self._points)
        elif chosen is Action.INSERT_MEDIANT:
            changed = self._insert(mediant=True)
        elif chosen is Action.INSERT_MIDPOINT:
            changed = self._insert(mediant=False)
        else:
            self._done = True
        self._last_reward = _round_reward(before - self._goal_metric())
        if self._remaining_budget <= 0:
            self._done = True
        return StrictTransition(
            self._make_observation(), chosen, self._last_reward, self._done, changed, True, True
        )

    def _goal_metric(self) -> float:
        return _coverage(self._points) if self._goal is GoalState.COVERAGE else _spectral(self._points)

    def _insert(self, *, mediant: bool) -> bool:
        left = self._points[self._cursor]
        right = self._points[(self._cursor + 1) % len(self._points)]
        lifted_right = right if right > left else right + 1
        if mediant:
            candidate = Fraction(
                left.numerator + lifted_right.numerator,
                left.denominator + lifted_right.denominator,
            )
        else:
            candidate = (left + lifted_right) / 2
        candidate %= 1
        if candidate in self._points:
            return False
        points = list(self._points)
        points.append(candidate)
        points.sort()
        self._points = tuple(points)
        self._cursor = points.index(candidate)
        return True

    def _make_observation(self) -> StrictObservation:
        points = self._points
        left_one = _circular_distance(points[(self._cursor - 1) % len(points)], points[self._cursor])
        right_one = _circular_distance(points[self._cursor], points[(self._cursor + 1) % len(points)])
        left_two = _circular_distance(points[(self._cursor - 2) % len(points)], points[(self._cursor - 1) % len(points)])
        right_two = _circular_distance(points[(self._cursor + 1) % len(points)], points[(self._cursor + 2) % len(points)])
        local_left = left_one + left_two
        local_right = right_one + right_two
        total = local_left + local_right
        cursor = int(round(float((local_right - local_left) / total if total else 0) * 8.0))
        return StrictObservation(
            tuple(_gap_bin(value) for value in (left_two, left_one, right_one, right_two)),
            (_ratio_bin(left_one, right_one), _ratio_bin(left_two, right_two)),
            max(-8, min(8, cursor)),
            float(round(self._remaining_budget / self._action_budget, 6)),
            float(_round_reward(self._last_reward)),
            self._goal,
            UntrustedCue(),
        )


class RepairPolicy(Protocol):
    """Policy boundary: policies receive only a coarse view and fixed actions."""

    updates: int

    def choose(self, view: CoarseRepairView) -> Action: ...


class RewardLearner:
    """Small linear action-value learner with no evaluator-side fields."""

    def __init__(self, seed: int, *, learning: bool = True) -> None:
        self._rng = random.Random(seed)
        width = len(CoarseRepairView((0, 0, 0, 0), (0, 0), 0, 1.0, 0.0, 0).features())
        self._weights = [[0.0 for _ in range(width)] for _ in POLICY_ACTIONS]
        self.learning = learning
        self.updates = 0

    def choose(self, view: CoarseRepairView, *, epsilon: float = 0.0) -> Action:
        if epsilon and self._rng.random() < epsilon:
            return self._rng.choice(tuple(Action(item) for item in POLICY_ACTIONS))
        features = view.features()
        values = [sum(weight * value for weight, value in zip(row, features)) for row in self._weights]
        best = max(values)
        return Action(POLICY_ACTIONS[next(index for index, value in enumerate(values) if value == best)])

    def update(self, view: CoarseRepairView, action: Action, feedback: float, *, alpha: float = 0.10) -> None:
        if not self.learning:
            return
        features = view.features()
        index = POLICY_ACTIONS.index(action.value)
        prediction = sum(weight * value for weight, value in zip(self._weights[index], features))
        error = feedback - prediction
        for position, value in enumerate(features):
            self._weights[index][position] += alpha * error * value
        self.updates += 1

    def freeze(self) -> None:
        self.learning = False

    def digest(self) -> str:
        return sha256(json.dumps(self._weights, sort_keys=True).encode("utf-8")).hexdigest()


class UniformRandom:
    updates = 0

    def __init__(self, seed: int) -> None:
        self._rng = random.Random(seed)

    def choose(self, view: CoarseRepairView) -> Action:
        return self._rng.choice(tuple(Action(item) for item in POLICY_ACTIONS))


class LocalGapMediant:
    """Deterministic baseline: local gap bins plus a fixed mediant preference."""

    updates = 0

    def choose(self, view: CoarseRepairView) -> Action:
        left_outer, left, right, right_outer = view.local_gap_bins
        if max(left, right) >= max(left_outer, right_outer):
            return Action.INSERT_MEDIANT
        return Action.MOVE_LEFT if left_outer > right_outer else Action.MOVE_RIGHT


class VisibleOneStepGreedy:
    """Greedy over a public, fixed coarse proxy; not an evaluator oracle."""

    updates = 0

    def choose(self, view: CoarseRepairView) -> Action:
        outer_left, left, right, outer_right = view.local_gap_bins
        imbalance = abs(left - right)
        scores = {
            Action.MOVE_LEFT: outer_left - left,
            Action.MOVE_RIGHT: outer_right - right,
            Action.INSERT_MEDIANT: 2 * max(left, right) - imbalance,
            Action.INSERT_MIDPOINT: max(left, right) - imbalance - 1,
            Action.STOP: -1 if view.remaining_budget_fraction > 0.125 else 0,
        }
        best = max(scores.values())
        return next(action for action in (Action(item) for item in POLICY_ACTIONS) if scores[action] == best)


class EvaluatorOneStepOracle:
    """Evaluator-only reference: exact but myopic one-step hidden lookahead."""

    updates = 0

    def choose(self, view: CoarseRepairView) -> Action:
        raise AssertionError("oracle selection must receive an evaluator environment, not a view")


def _task_environment(task: RepairTask, arm: str) -> StrictEnvironment | _PointSetRepairEnvironment:
    farey = StrictEnvironment(
        task.order,
        task.pattern,
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=ACTION_BUDGET,
        goal=task.goal,
    )
    if arm == "farey":
        return farey
    if arm != "scramble":
        raise ValueError("arm must be evaluator-owned farey or scramble")
    if exact_gap_scramble is None:
        raise RuntimeError("exact-gap scramble adapter unavailable: " + str(_ABLATON_IMPORT_ERROR))
    scrambled = exact_gap_scramble(farey._target, seed=task.seed ^ 0x51A7)  # evaluator side
    # Keep the same sorted-rank damage geometry. Mapping gap-token identity
    # instead would destroy burst/isolation structure after scrambling.
    matched_rank_mask = farey._deleted_indices
    return _PointSetRepairEnvironment(
        scrambled.points,
        matched_rank_mask,
        seed=task.seed,
        goal=task.goal,
        action_budget=ACTION_BUDGET,
    )


def _hidden_repair_metrics(environment: StrictEnvironment | _PointSetRepairEnvironment) -> HiddenRepairMetrics:
    """Score exact identities only after an episode, on the evaluator side."""

    target = set(environment._target)
    initial = set(environment._initial_points)
    current = set(environment._points)
    deleted = target - initial
    additions = current - initial
    true_positive = len(additions & deleted)
    false_positive = len(additions - target)
    precision = true_positive / len(additions) if additions else 0.0
    recall = true_positive / len(deleted) if deleted else 1.0
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    return HiddenRepairMetrics(
        precision=precision,
        recall=recall,
        f1=f1,
        exact_recovery=float(current == target),
        true_positive=true_positive,
        false_positive=false_positive,
        deleted_count=len(deleted),
    )


def _oracle_action(environment: StrictEnvironment | _PointSetRepairEnvironment) -> Action:
    """Use hidden identities only for the labelled myopic one-step reference."""

    ranked: list[tuple[tuple[float, float, float, float, int], Action]] = []
    for action_text in POLICY_ACTIONS:
        probe = deepcopy(environment)
        transition = probe.step(action_text)
        hidden = _hidden_repair_metrics(probe)
        ranked.append(
            ((hidden.f1, hidden.recall, hidden.precision, transition.reward, int(transition.changed)), Action(action_text))
        )
    return max(ranked, key=lambda item: item[0])[1]


def run_episode(
    policy: RepairPolicy | EvaluatorOneStepOracle,
    task: RepairTask,
    *,
    arm: str = "farey",
    training: bool = False,
    feedback_mode: str = "true",
    feedback_reservoir: list[float] | None = None,
    epsilon: float = 0.0,
) -> dict[str, Any]:
    """Run a charged episode while retaining evaluator facts outside policy calls."""

    environment = _task_environment(task, arm)
    visible_progress = 0.0
    actions: list[str] = []
    last_transmitted = 0.0
    for _ in range(ACTION_BUDGET):
        view = coarse_view(
            environment.observation,
            visible_feedback=last_transmitted if training else None,
        )
        if isinstance(policy, EvaluatorOneStepOracle):
            action = _oracle_action(environment)
        elif isinstance(policy, RewardLearner):
            action = policy.choose(view, epsilon=epsilon)
        else:
            action = policy.choose(view)
        transition = environment.step(action)
        visible_progress += transition.reward
        actions.append(action.value)
        if training:
            if feedback_mode == "true":
                transmitted = transition.reward
            elif feedback_mode == "zero":
                transmitted = 0.0
            elif feedback_mode == "prior_reward_shuffled":
                transmitted = (
                    random.Random(task.seed ^ len(actions)).choice(feedback_reservoir)
                    if feedback_reservoir
                    else 0.0
                )
            else:
                raise ValueError("feedback_mode must be true, zero, or prior_reward_shuffled")
            if isinstance(policy, RewardLearner):
                policy.update(view, action, transmitted)
            last_transmitted = transmitted
            if feedback_reservoir is not None:
                feedback_reservoir.append(transition.reward)
        if transition.done:
            break
    hidden = _hidden_repair_metrics(environment)
    return {
        "order": task.order,
        "pattern": task.pattern.value,
        "goal": task.goal.value,
        "seed": task.seed,
        "arm": arm,
        "precision": hidden.precision,
        "recall": hidden.recall,
        "f1": hidden.f1,
        "exact_recovery": hidden.exact_recovery,
        "visible_progress": visible_progress,
        "cost": len(actions),
        "charged_actions": len(actions),
    }


def make_manifest(
    orders: Iterable[int],
    patterns: Iterable[DamagePattern],
    *,
    damage_count: int,
    replicates: int,
    seed: int,
) -> list[RepairTask]:
    """Balanced evaluator manifest with every order/pattern/goal cell complete."""

    generator = random.Random(seed)
    tasks: list[RepairTask] = []
    for order in orders:
        for pattern in patterns:
            for goal in GOALS:
                for _ in range(replicates):
                    tasks.append(RepairTask(order, pattern, goal, generator.randrange(1 << 60), damage_count))
    return tasks


def complete_cells(tasks: Sequence[RepairTask], *, replicates: int) -> bool:
    expected = {(order, pattern.value, goal.value) for order in {task.order for task in tasks} for pattern in {task.pattern for task in tasks} for goal in GOALS}
    return bool(tasks) and all(sum(task.cell == cell for task in tasks) == replicates for cell in expected)


def train_reward_learner(
    feedback_mode: str, tasks: Sequence[RepairTask], config: ExperimentConfig, *, seed_offset: int = 0
) -> RewardLearner:
    """Train only on the preregistered low-order random-isolated d=2 tasks."""

    # Identical initialization, exploration stream, and task schedule isolate
    # the feedback channel as the only training intervention.
    learner = RewardLearner(config.seed)
    schedule = list(tasks)
    generator = random.Random(config.seed ^ 0xA11CE)
    reservoir: list[float] = []
    for episode in range(config.train_episodes):
        if episode % len(schedule) == 0:
            generator.shuffle(schedule)
        task = schedule[episode % len(schedule)]
        epsilon = max(0.04, 0.28 * (1.0 - episode / config.train_episodes))
        run_episode(
            learner,
            task,
            training=True,
            feedback_mode=feedback_mode,
            feedback_reservoir=reservoir,
            epsilon=epsilon,
        )
    learner.freeze()
    return learner


def evaluate(
    policy: RepairPolicy | EvaluatorOneStepOracle,
    tasks: Sequence[RepairTask],
    *,
    arm: str = "farey",
    random_seed: int = 0,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, task in enumerate(tasks):
        active: RepairPolicy | EvaluatorOneStepOracle
        if policy == "uniform_random":  # type: ignore[comparison-overlap]
            active = UniformRandom(random_seed ^ task.seed ^ index)
        else:
            active = policy
        rows.append(run_episode(active, task, arm=arm))
    return rows


def _mean(rows: Sequence[dict[str, Any]], key: str) -> float:
    return statistics.fmean(float(row[key]) for row in rows) if rows else 0.0


def _paired_bootstrap(
    treatment: Sequence[dict[str, Any]],
    control: Sequence[dict[str, Any]],
    key: str,
    *,
    alpha: float,
    resamples: int,
    seed: int,
) -> dict[str, float]:
    if len(treatment) != len(control):
        raise ValueError("paired bootstrap needs equally sized rows")
    differences = [float(left[key]) - float(right[key]) for left, right in zip(treatment, control)]
    if not differences:
        return {"effect": 0.0, "ci_low": 0.0, "ci_high": 0.0}
    generator = random.Random(seed)
    means = []
    for _ in range(resamples):
        means.append(statistics.fmean(generator.choice(differences) for _ in differences))
    means.sort()
    lower_index = max(0, min(len(means) - 1, int((alpha / 2.0) * len(means))))
    upper_index = max(0, min(len(means) - 1, int((1.0 - alpha / 2.0) * len(means)) - 1))
    return {
        "effect": statistics.fmean(differences),
        "ci_low": means[lower_index],
        "ci_high": means[upper_index],
    }


def _gate(
    name: str,
    treatment: Sequence[dict[str, Any]],
    controls: dict[str, Sequence[dict[str, Any]]],
    *,
    key: str,
    margin: float,
    valid: bool,
    reason: str,
    config: ExperimentConfig,
) -> dict[str, Any]:
    """Bonferroni-adjusted paired-bootstrap gate against named controls."""

    comparisons = {
        control_name: _paired_bootstrap(
            treatment,
            rows,
            key,
            alpha=0.05 / max(1, len(controls)),
            resamples=config.bootstrap_resamples,
            seed=config.seed
            ^ int.from_bytes(
                sha256(f"{name}|{control_name}|{key}".encode("utf-8")).digest()[:8],
                "big",
            ),
        )
        for control_name, rows in controls.items()
    }
    lows = [result["ci_low"] for result in comparisons.values()]
    highs = [result["ci_high"] for result in comparisons.values()]
    effects = [result["effect"] for result in comparisons.values()]
    simultaneous = {
        "effect_min": min(effects) if effects else 0.0,
        "ci_low": min(lows) if lows else 0.0,
        "ci_high": max(highs) if highs else 0.0,
    }
    if not valid:
        status = "unverified"
    elif simultaneous["ci_low"] >= margin:
        status = "positive"
    elif simultaneous["ci_high"] < 0.0:
        status = "negative"
    elif simultaneous["ci_low"] <= 0.0 <= simultaneous["ci_high"]:
        status = "null"
    else:
        status = "unverified"
    return {
        "name": name,
        "status": status,
        "metric": key,
        "margin": margin,
        "valid": valid,
        "reason": reason,
        "method": f"paired percentile bootstrap ({config.bootstrap_resamples} resamples), Bonferroni over {len(controls)} preregistered controls",
        "comparisons": comparisons,
        "simultaneous": simultaneous,
    }


def _structural_proof(tasks: Sequence[RepairTask]) -> dict[str, Any]:
    if exact_gap_scramble is None:
        return {"available": False, "reason": "adapter unavailable: " + str(_ABLATON_IMPORT_ERROR)}
    checks = []
    for task in tasks:
        farey = _task_environment(task, "farey")
        scrambled = exact_gap_scramble(farey._target, seed=task.seed ^ 0x51A7)
        metrics = scrambled.metrics
        checks.append(
            {
                "same_point_count": metrics.point_count_equal,
                "same_rank_mask_count": len(farey._deleted_indices) == task.damage_count,
                "same_exact_gap_multiset": metrics.gap_multiset_equal,
                "nontrivial_gap_order": metrics.is_nontrivial,
                "closes": metrics.closes_to_one,
            }
        )
    return {
        "available": True,
        "pairs": len(checks),
        "all_same_point_count": all(check["same_point_count"] for check in checks),
        "all_same_rank_mask_count": all(check["same_rank_mask_count"] for check in checks),
        "all_same_exact_gap_multiset": all(check["same_exact_gap_multiset"] for check in checks),
        "all_nontrivial_gap_order": all(check["nontrivial_gap_order"] for check in checks),
        "all_close": all(check["closes"] for check in checks),
    }


def _initial_action_reachability(
    environment: StrictEnvironment | _PointSetRepairEnvironment,
) -> float:
    """Fraction of hidden points generated by one legal local insertion.

    The evaluator scans every initially visible adjacent pair, but only applies
    the same two insertion formulas available to the controller.  This is a
    structural diagnostic, not a controller score or a finite-horizon oracle.
    """

    points = tuple(environment._initial_points)
    deleted = set(environment._target) - set(points)
    candidates: set[Fraction] = set()
    for index, left in enumerate(points):
        right = points[(index + 1) % len(points)]
        lifted_right = right if right > left else right + 1
        candidates.add(
            Fraction(
                left.numerator + lifted_right.numerator,
                left.denominator + lifted_right.denominator,
            )
            % 1
        )
        candidates.add(((left + lifted_right) / 2) % 1)
    return len(deleted & candidates) / len(deleted) if deleted else 1.0


def _structural_reachability_rows(
    tasks: Sequence[RepairTask], arm: str
) -> list[dict[str, Any]]:
    return [
        {
            "order": task.order,
            "pattern": task.pattern.value,
            "goal": task.goal.value,
            "seed": task.seed,
            "initial_reachable_fraction": _initial_action_reachability(
                _task_environment(task, arm)
            ),
        }
        for task in tasks
    ]


def _source_hashes() -> dict[str, str]:
    names = (
        "repair_experiment.py",
        "strict_environment.py",
        "repair_ablation.py",
        "test_repair_experiment.py",
        "test_repair_ablation.py",
    )
    return {
        name: sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
        for name in names
        if Path(__file__).with_name(name).exists()
    }


def run_experiment(config: ExperimentConfig = DEFAULT_CONFIG) -> dict[str, Any]:
    """Train, freeze, evaluate the full balanced grid, and return a receipt."""

    source_hashes = _source_hashes()
    train_tasks = make_manifest(
        TRAIN_ORDERS,
        (TRAIN_PATTERN,),
        damage_count=2,
        replicates=config.train_replicates_per_order_goal,
        seed=config.seed,
    )
    in_domain_tasks = make_manifest(
        TRAIN_ORDERS,
        (TRAIN_PATTERN,),
        damage_count=2,
        replicates=config.in_domain_replicates_per_order_goal,
        seed=config.seed + 1,
    )
    transfer_tasks = make_manifest(
        TEST_ORDERS,
        TEST_PATTERNS,
        damage_count=4,
        replicates=config.test_replicates_per_cell,
        seed=config.seed + 2,
    )

    true = train_reward_learner("true", train_tasks, config, seed_offset=1)
    shuffled = train_reward_learner("prior_reward_shuffled", train_tasks, config, seed_offset=2)
    zero = train_reward_learner("zero", train_tasks, config, seed_offset=3)
    frozen_digests = {"true": true.digest(), "prior_reward_shuffled": shuffled.digest(), "zero": zero.digest()}
    train_updates = {"true": true.updates, "prior_reward_shuffled": shuffled.updates, "zero": zero.updates}

    feedback_true = evaluate(true, in_domain_tasks)
    feedback_shuffled = evaluate(shuffled, in_domain_tasks)
    feedback_zero = evaluate(zero, in_domain_tasks)
    feedback_updates = {"true": true.updates, "prior_reward_shuffled": shuffled.updates, "zero": zero.updates}
    feedback_gate = _gate(
        "feedback_learning",
        feedback_true,
        {"prior_reward_shuffled": feedback_shuffled, "zero_feedback": feedback_zero},
        key="f1",
        margin=config.feedback_f1_margin,
        valid=(
            complete_cells(in_domain_tasks, replicates=config.in_domain_replicates_per_order_goal)
            and feedback_updates == train_updates
            and len(set(train_updates.values())) == 1
            and next(iter(train_updates.values())) == config.train_episodes * ACTION_BUDGET
        ),
        reason="matched initialization/schedule/eight updates per episode; frozen held-out low-order cells; hidden F1 never entered view or reward",
        config=config,
    )

    transfer_true = evaluate(true, transfer_tasks)
    transfer_shuffled = evaluate(shuffled, transfer_tasks)
    transfer_zero = evaluate(zero, transfer_tasks)
    transfer_random = evaluate("uniform_random", transfer_tasks, random_seed=config.seed)  # type: ignore[arg-type]
    transfer_local = evaluate(LocalGapMediant(), transfer_tasks)
    transfer_greedy = evaluate(VisibleOneStepGreedy(), transfer_tasks)
    oracle = evaluate(EvaluatorOneStepOracle(), transfer_tasks)
    test_updates = {"true": true.updates, "prior_reward_shuffled": shuffled.updates, "zero": zero.updates}
    test_digests = {"true": true.digest(), "prior_reward_shuffled": shuffled.digest(), "zero": zero.digest()}
    complete_transfer = complete_cells(transfer_tasks, replicates=config.test_replicates_per_cell)

    recovery_gate = _gate(
        "recovery",
        transfer_true,
        {"uniform_random": transfer_random, "local_gap_mediant": transfer_local, "visible_one_step_greedy": transfer_greedy},
        key="f1",
        margin=config.recovery_f1_margin,
        valid=complete_transfer,
        reason="balanced larger-order recovery, primary evaluator-only precision/recall/F1/exact accounting",
        config=config,
    )
    transfer_gate = _gate(
        "frozen_transfer",
        transfer_true,
        {
            "prior_reward_shuffled": transfer_shuffled,
            "zero_feedback": transfer_zero,
            "uniform_random": transfer_random,
            "local_gap_mediant": transfer_local,
            "visible_one_step_greedy": transfer_greedy,
        },
        key="f1",
        margin=config.transfer_f1_margin,
        valid=(complete_transfer and test_updates == train_updates and test_digests == frozen_digests),
        reason="N={11,13,17}, d=4, all three damage families, both goals, ten repetitions/cell; measured test updates must be zero",
        config=config,
    )

    # Denominator bias has no invariant meaning after exact-gap scrambling;
    # structural pairs therefore use only rank-geometric isolated/burst masks.
    structural_tasks = [
        task for task in transfer_tasks if task.pattern is not DamagePattern.DENOMINATOR_BIASED
    ]
    proof = _structural_proof(structural_tasks)
    reachability_diagnostic: dict[str, Any]
    if proof.get("available"):
        structural_farey_true = evaluate(true, structural_tasks)
        scramble_true = evaluate(true, structural_tasks, arm="scramble")
        farey_reachability = _structural_reachability_rows(structural_tasks, "farey")
        scramble_reachability = _structural_reachability_rows(structural_tasks, "scramble")
        reachability_diagnostic = _gate(
            "structural_reachability_payoff",
            farey_reachability,
            {"exact_gap_scramble": scramble_reachability},
            key="initial_reachable_fraction",
            margin=config.structural_f1_margin,
            valid=len(structural_tasks) == 120,
            reason=(
                "evaluator-only diagnostic: share of deleted identities generated "
                "by a mediant or midpoint from any initially visible adjacent pair"
            ),
            config=config,
        )
        reachability_matched = abs(
            _mean(farey_reachability, "initial_reachable_fraction")
            - _mean(scramble_reachability, "initial_reachable_fraction")
        ) <= 0.01
        structural_valid = all(
            bool(proof[key])
            for key in (
                "all_same_point_count",
                "all_same_rank_mask_count",
                "all_same_exact_gap_multiset",
                "all_nontrivial_gap_order",
                "all_close",
            )
        ) and len(structural_tasks) == 120 and reachability_matched
        structural_gate = _gate(
            "farey_vs_exact_gap_scramble",
            structural_farey_true,
            {"exact_gap_scramble": scramble_true},
            key="f1",
            margin=config.structural_f1_margin,
            valid=structural_valid,
            reason=(
                "controller contrast is invalid/confounded unless initial local-action "
                f"reachability is matched; matched={reachability_matched}"
            ),
            config=config,
        )
    else:
        reachability_diagnostic = {
            "name": "structural_reachability_payoff",
            "status": "unverified",
            "valid": False,
            "reason": proof["reason"],
        }
        structural_gate = {
            "name": "farey_vs_exact_gap_scramble",
            "status": "unverified",
            "metric": "f1",
            "margin": config.structural_f1_margin,
            "valid": False,
            "reason": proof["reason"],
            "method": "adapter interface declared; no duplicated scramble implementation",
            "comparisons": {},
            "simultaneous": {"effect_min": 0.0, "ci_low": 0.0, "ci_high": 0.0},
        }

    core = (feedback_gate, recovery_gate, transfer_gate)
    conjunction_valid = all(gate["valid"] for gate in core)
    conjunction_status = "positive" if conjunction_valid and all(gate["status"] == "positive" for gate in core) else "unverified"
    conjunction_gate = {
        "name": "core_conjunction",
        "status": conjunction_status,
        "metric": "all core gates",
        "margin": None,
        "valid": conjunction_valid,
        "reason": "positive only when feedback learning, recovery, and frozen transfer are all positive on the same manifest",
    }

    if source_hashes != _source_hashes():
        raise RuntimeError("sources changed while the experiment was running")
    return {
        "schema_version": 1,
        "experiment": "repair-only strict Farey competency probe",
        "seed": config.seed,
        "provenance": {"command": "PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/repair_experiment.py", "python": sys.version.split()[0]},
        "controller_boundary": {
            "visible": list(CoarseRepairView.__dataclass_fields__),
            "hidden": ["N/order", "exact fractions", "full target", "survivors", "deletion identities/ranks", "target metric values", "arm/family"],
            "fixed_charged_actions": list(POLICY_ACTIONS),
        },
        "predeclaration": {
            "train": {"orders": list(TRAIN_ORDERS), "pattern": TRAIN_PATTERN.value, "damage_count": 2, "frozen_before_evaluation": True},
            "test": {"orders": list(TEST_ORDERS), "patterns": [pattern.value for pattern in TEST_PATTERNS], "damage_count": 4, "goals": [goal.value for goal in GOALS], "replicates_per_cell": config.test_replicates_per_cell, "complete_cells": complete_transfer},
            "statistics": "paired percentile bootstrap with Bonferroni-adjusted marginal intervals; positive/null/negative/unverified taxonomy",
            "gates": ["feedback_learning", "recovery", "frozen_transfer", "core_conjunction"],
        },
        "model": {
            "training_updates": train_updates,
            "measured_test_updates": {name: test_updates[name] - train_updates[name] for name in train_updates},
            "frozen_digest_unchanged": {name: test_digests[name] == frozen_digests[name] for name in frozen_digests},
            "digests": frozen_digests,
        },
        "baselines": ["history-resampled prior-reward learner", "zero-feedback learner", "uniform random", "deterministic local-gap/mediant", "visible one-step greedy", "evaluator-only one-step oracle reference (not a finite-horizon ceiling)"],
        "primary_hidden_metrics": {name: _mean(transfer_true, name) for name in ("precision", "recall", "f1", "exact_recovery")},
        "visible_metrics": {name: _mean(transfer_true, name) for name in ("visible_progress", "cost", "charged_actions")},
        "evaluator_one_step_oracle_reference": {name: _mean(oracle, name) for name in ("precision", "recall", "f1", "exact_recovery", "visible_progress", "cost")},
        "structural_proof": proof,
        "structural_diagnostics": {
            reachability_diagnostic["name"]: reachability_diagnostic,
        },
        "gates": {gate["name"]: gate for gate in (*core, structural_gate, conjunction_gate)},
        "source_and_test_hashes": source_hashes,
    }


def _result_markdown(result: dict[str, Any]) -> str:
    gates = result["gates"]
    hidden = result["primary_hidden_metrics"]
    visible = result["visible_metrics"]
    lines = [
        "# Repair-only strict Farey experiment results",
        "",
        "This deterministic run is a finite repair probe, not an agency claim.",
        "",
        "## Primary evaluator-only recovery",
        "",
        "| precision | recall | F1 | exact recovery |",
        "| ---: | ---: | ---: | ---: |",
        f"| {hidden['precision']:.3f} | {hidden['recall']:.3f} | {hidden['f1']:.3f} | {hidden['exact_recovery']:.3f} |",
        "",
        "## Visible feedback-derived outcomes",
        "",
        "| progress | charged cost |",
        "| ---: | ---: |",
        f"| {visible['visible_progress']:.5f} | {visible['cost']:.2f} |",
        "",
        "## Predeclared gates",
        "",
        "| gate | status | criterion |",
        "| --- | --- | --- |",
    ]
    for key in ("feedback_learning", "recovery", "frozen_transfer", "farey_vs_exact_gap_scramble", "core_conjunction"):
        gate = gates[key]
        criterion = gate.get("reason", "")
        lines.append(f"| {key} | {gate['status']} | {criterion} |")
    updates = result["model"]["measured_test_updates"]
    proof = result["structural_proof"]
    reachability = result["structural_diagnostics"]["structural_reachability_payoff"]
    lines.extend(
        [
            "",
            "## Validity",
            "",
            f"All held-out test updates were measured as `{updates}`; the frozen model digests were unchanged.",
            "",
            "The larger-order test grid is complete: N = 11, 13, 17; d = 4; random-isolated, burst, and denominator-biased damage; both goals; ten repetitions per cell.",
            "",
            f"Exact-gap scramble proof: `{proof}`.",
            "",
            "## Structural diagnostic",
            "",
            f"The initial local-action reachability contrast is **{reachability['status']}**: `{reachability['simultaneous']}`. This is a payoff of the Farey organization for this repair vocabulary, not evidence that the controller learned to exploit it.",
            "",
            "Positive requires every Bonferroni-adjusted paired-bootstrap lower bound to clear its preregistered margin. `null` means the simultaneous interval crosses zero; `negative` means it is wholly below zero; `unverified` covers an invalid design or an interval that is directionally positive but below the margin.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(result: dict[str, Any]) -> None:
    directory = Path(__file__).parent
    (directory / "repair_receipt.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (directory / "REPAIR_RESULTS.md").write_text(_result_markdown(result), encoding="utf-8")


def main() -> None:
    result = run_experiment()
    write_outputs(result)
    print("wrote repair_receipt.json and REPAIR_RESULTS.md")
    print(", ".join(f"{name}={gate['status']}" for name, gate in result["gates"].items()))


if __name__ == "__main__":
    main()
