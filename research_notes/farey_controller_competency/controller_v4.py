"""Small V4 controller harness over the fixed V3.4 action vocabulary.

The evaluator owns exact points, damage identities, rewards, and F1/exact
metrics.  A policy receives only :class:`ControllerView`: fixed-width coarse
local geometry, a budget fraction, scalar feedback, and a goal bit.  The
whole-geometry derangement helpers are evaluator-side null machinery; they
never alter the physical environment.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from hashlib import sha256
import json
import random
from typing import Iterable, Sequence

try:
    from .competency_v34_multiscale_navigation import _transition
    from .repair_experiment import RepairTask
    from .strict_environment import (
        DamagePattern,
        GoalState,
        StrictEnvironment,
        _coverage,
        _gap_bin,
        _ratio_bin,
        _spectral,
    )
except ImportError:  # direct execution from this directory
    from competency_v34_multiscale_navigation import _transition  # type: ignore[no-redef]
    from repair_experiment import RepairTask  # type: ignore[no-redef]
    from strict_environment import (  # type: ignore[no-redef]
        DamagePattern,
        GoalState,
        StrictEnvironment,
        _coverage,
        _gap_bin,
        _ratio_bin,
        _spectral,
    )


V4_ACTIONS: tuple[str, ...] = (
    "move_left",
    "move_right",
    "insert_mediant",
    "insert_midpoint",
    "move_left_quarter",
    "move_right_quarter",
    "left2_right1",
    "left1_right2",
    "move_left_half",
    "move_right_half",
    "move_left_eighth",
    "move_right_eighth",
)
ACTION_BUDGET = 8
POLICY_ACTIONS = V4_ACTIONS


def _circular_gaps(points: Sequence[Fraction]) -> tuple[Fraction, ...]:
    ordered = tuple(sorted(points))
    if not ordered:
        return ()
    return tuple(
        (ordered[(index + 1) % len(ordered)] - ordered[index]) % 1
        for index in range(len(ordered))
    )


def _geometry_tuple(environment: "V4Environment") -> tuple[Fraction, ...]:
    """Evaluator-only exact geometry; never passed to a controller."""

    return _circular_gaps(environment._points)


@dataclass(frozen=True, slots=True)
class ControllerView:
    """Fixed-width view with no order, fraction, target, or damage field."""

    local_gap_bins: tuple[int, int, int, int]
    local_ratio_bins: tuple[int, int]
    cursor_relation_bin: int
    remaining_budget_fraction: float
    last_scalar_reward: float
    trusted_goal: int

    def __post_init__(self) -> None:
        if len(self.local_gap_bins) != 4 or any(type(v) is not int or not 0 <= v <= 15 for v in self.local_gap_bins):
            raise ValueError("local_gap_bins must contain four bins in [0, 15]")
        if len(self.local_ratio_bins) != 2 or any(type(v) is not int or not 0 <= v <= 15 for v in self.local_ratio_bins):
            raise ValueError("local_ratio_bins must contain two bins in [0, 15]")
        if type(self.cursor_relation_bin) is not int or not -8 <= self.cursor_relation_bin <= 8:
            raise ValueError("cursor_relation_bin must be in [-8, 8]")
        if type(self.remaining_budget_fraction) is not float or not 0.0 <= self.remaining_budget_fraction <= 1.0:
            raise ValueError("remaining_budget_fraction must be a float in [0, 1]")
        if type(self.last_scalar_reward) is not float:
            raise TypeError("last_scalar_reward must be a float")
        if type(self.trusted_goal) is not int or self.trusted_goal not in (0, 1):
            raise ValueError("trusted_goal must be 0 or 1")

    @property
    def shape(self) -> tuple[int, ...]:
        return (4, 2, 1, 1, 1, 1)

    def as_tuple(self) -> tuple[object, ...]:
        return (
            *self.local_gap_bins,
            *self.local_ratio_bins,
            self.cursor_relation_bin,
            self.remaining_budget_fraction,
            self.last_scalar_reward,
            self.trusted_goal,
        )

    def features(self) -> tuple[float, ...]:
        return (
            1.0,
            *(value / 15.0 for value in self.local_gap_bins),
            *(value / 15.0 for value in self.local_ratio_bins),
            self.cursor_relation_bin / 8.0,
            self.remaining_budget_fraction,
            max(-1.0, min(1.0, self.last_scalar_reward * 40.0)),
            float(self.trusted_goal),
        )


def _view(environment: "V4Environment", feedback: float = 0.0) -> ControllerView:
    points = environment._points
    cursor = environment._cursor
    left1 = (points[cursor] - points[(cursor - 1) % len(points)]) % 1
    right1 = (points[(cursor + 1) % len(points)] - points[cursor]) % 1
    left2 = (points[(cursor - 1) % len(points)] - points[(cursor - 2) % len(points)]) % 1
    right2 = (points[(cursor + 2) % len(points)] - points[(cursor + 1) % len(points)]) % 1
    local_left, local_right = left1 + left2, right1 + right2
    total = local_left + local_right
    relation = int(round(float((local_right - local_left) / total) * 8.0)) if total else 0
    return ControllerView(
        tuple(_gap_bin(value) for value in (left2, left1, right1, right2)),
        (_ratio_bin(left1, right1), _ratio_bin(left2, right2)),
        max(-8, min(8, relation)),
        float(round(environment._remaining / ACTION_BUDGET, 6)),
        float(feedback),
        0 if environment._goal is GoalState.COVERAGE else 1,
    )


class V4Environment:
    """Evaluator-owned physical state using all twelve V3.4 actions."""

    __slots__ = (
        "_target", "_initial_points", "_deleted_points", "_points", "_cursor",
        "_initial_cursor", "_remaining", "_goal", "_done", "_action_budget",
    )

    def __init__(self, task: RepairTask, *, goal: GoalState | None = None) -> None:
        base = StrictEnvironment(
            task.order,
            task.pattern,
            damage_count=task.damage_count,
            seed=task.seed,
            rotation=True,
            action_budget=ACTION_BUDGET,
            goal=goal or task.goal,
        )
        self._target = tuple(base._target)
        self._initial_points = tuple(base._initial_points)
        self._deleted_points = tuple(base._deleted_points)
        self._points = tuple(base._points)
        self._cursor = int(base._cursor)
        self._initial_cursor = int(base._initial_cursor)
        self._remaining = ACTION_BUDGET
        self._goal = goal or task.goal
        self._done = False
        self._action_budget = ACTION_BUDGET

    @property
    def view(self) -> ControllerView:
        return _view(self)

    def step(self, action: str) -> float:
        if self._done:
            raise RuntimeError("episode is already done")
        if action not in V4_ACTIONS:
            raise ValueError(f"unknown V4 action: {action}")
        before = self._metric()
        self._points, self._cursor, self._remaining = _transition(
            (self._points, self._cursor, self._remaining), action
        )
        after = self._metric()
        self._done = self._remaining <= 0
        return float(round(before - after, 6))

    def _metric(self) -> float:
        return _coverage(self._points) if self._goal is GoalState.COVERAGE else _spectral(self._points)


@dataclass(frozen=True, slots=True)
class HiddenMetrics:
    precision: float
    recall: float
    f1: float
    exact: float


def evaluator_metrics(environment: V4Environment) -> HiddenMetrics:
    """Compute identity recovery only on the evaluator side."""

    target, initial, current = set(environment._target), set(environment._initial_points), set(environment._points)
    deleted, additions = target - initial, current - initial
    true_positive = len(additions & deleted)
    false_positive = len(additions - target)
    precision = true_positive / len(additions) if additions else 0.0
    recall = true_positive / len(deleted) if deleted else 1.0
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    return HiddenMetrics(precision, recall, f1, float(current == target))


class LinearQ:
    """Deterministic linear action-value learner over the coarse view."""

    def __init__(self, seed: int = 0, *, learning: bool = True, gamma: float = 0.90) -> None:
        self._rng = random.Random(seed)
        width = len(ControllerView((0, 0, 0, 0), (0, 0), 0, 1.0, 0.0, 0).features())
        self._weights = [[0.0] * width for _ in V4_ACTIONS]
        self.learning = learning
        self.gamma = float(gamma)
        self.updates = 0

    def choose(self, view: ControllerView, *, epsilon: float = 0.0) -> str:
        if epsilon and self._rng.random() < epsilon:
            return self._rng.choice(V4_ACTIONS)
        values = [sum(weight * feature for weight, feature in zip(row, view.features())) for row in self._weights]
        best = max(values)
        return V4_ACTIONS[next(i for i, value in enumerate(values) if value == best)]

    def update(
        self,
        view: ControllerView,
        action: str,
        reward: float,
        *,
        next_view: ControllerView | None = None,
        done: bool = False,
        alpha: float = 0.10,
    ) -> None:
        if not self.learning:
            return
        index = V4_ACTIONS.index(action)
        features = view.features()
        prediction = sum(weight * feature for weight, feature in zip(self._weights[index], features))
        bootstrap = 0.0
        if next_view is not None and not done:
            bootstrap = self.gamma * max(
                sum(weight * feature for weight, feature in zip(row, next_view.features()))
                for row in self._weights
            )
        error = float(reward) + bootstrap - prediction
        for position, feature in enumerate(features):
            self._weights[index][position] += alpha * error * feature
        self.updates += 1

    def freeze(self) -> None:
        self.learning = False

    def digest(self) -> str:
        return sha256(json.dumps(self._weights, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class FixedRandom:
    updates = 0

    def __init__(self, seed: int = 0) -> None:
        self._rng = random.Random(seed)

    def choose(self, view: ControllerView) -> str:
        del view
        return self._rng.choice(V4_ACTIONS)


class LocalHeuristic:
    updates = 0

    def choose(self, view: ControllerView) -> str:
        left_outer, left, right, right_outer = view.local_gap_bins
        if max(left, right) >= max(left_outer, right_outer):
            return "insert_mediant"
        return "move_left" if left_outer > right_outer else "move_right"


class VisibleGreedy:
    updates = 0

    def choose(self, view: ControllerView) -> str:
        outer_left, left, right, outer_right = view.local_gap_bins
        if right > left and right >= right_outer:
            return "move_right"
        if left > right and left >= left_outer:
            return "move_left"
        return "insert_mediant" if max(left, right) >= max(outer_left, outer_right) else "insert_midpoint"


@dataclass(frozen=True, slots=True)
class TrajectoryStep:
    """A matched physical transition with feedback deliberately blanked."""

    view: ControllerView
    action: str
    reward: float
    next_view: ControllerView
    done: bool


@dataclass(frozen=True, slots=True)
class Trajectory:
    steps: tuple[TrajectoryStep, ...]
    f1: float
    exact: float


def collect_trajectory(task: RepairTask, *, seed: int = 0, epsilon: float = 0.0) -> Trajectory:
    """Collect one fixed behavior trajectory before any feedback lane runs."""

    environment = V4Environment(task)
    behavior = LinearQ(seed, learning=False)
    steps: list[TrajectoryStep] = []
    for _ in range(ACTION_BUDGET):
        # Feedback is intentionally zero in the common behavior policy.  All
        # reward lanes replay this identical action/state schedule.
        view = _view(environment, 0.0)
        action = behavior.choose(view, epsilon=epsilon)
        reward = environment.step(action)
        next_view = _view(environment, 0.0)
        steps.append(TrajectoryStep(view, action, reward, next_view, environment._done))
    hidden = evaluator_metrics(environment)
    return Trajectory(tuple(steps), hidden.f1, hidden.exact)


def _replay_feedback(
    controller: LinearQ, trajectory: Trajectory, mode: str, seed: int
) -> tuple[float, ...]:
    true_rewards = tuple(step.reward for step in trajectory.steps)
    transmitted = episode_feedback(true_rewards, mode, seed)
    previous = 0.0
    for step, reward in zip(trajectory.steps, transmitted):
        view = replace(step.view, last_scalar_reward=float(previous))
        next_view = replace(step.next_view, last_scalar_reward=float(reward))
        controller.update(view, step.action, reward, next_view=next_view, done=step.done)
        previous = reward
    return transmitted


def replay_trajectory(
    controller: LinearQ, trajectory: Trajectory, feedback_mode: str, seed: int = 0
) -> tuple[float, ...]:
    """Apply one matched reward lane to a pre-collected trajectory."""

    return _replay_feedback(controller, trajectory, feedback_mode, seed)


def evaluate_policy(
    controller: LinearQ | FixedRandom | LocalHeuristic | VisibleGreedy,
    task: RepairTask,
) -> dict[str, object]:
    """Greedy/frozen evaluation with ordinary visible feedback and no updates."""

    environment = V4Environment(task)
    previous = 0.0
    actions: list[str] = []
    rewards: list[float] = []
    for _ in range(ACTION_BUDGET):
        view = _view(environment, previous)
        action = controller.choose(view) if not isinstance(controller, LinearQ) else controller.choose(view)
        actions.append(action)
        previous = environment.step(action)
        rewards.append(previous)
    hidden = evaluator_metrics(environment)
    return {
        "f1": hidden.f1,
        "exact": hidden.exact,
        "precision": hidden.precision,
        "recall": hidden.recall,
        "reward": sum(rewards),
        "actions": tuple(actions),
        "charged": len(actions),
        "updates": controller.updates,
    }


def episode_feedback(rewards: Sequence[float], mode: str, seed: int) -> tuple[float, ...]:
    """Return true, exact within-episode-permuted, or zero feedback."""

    if mode == "true":
        return tuple(float(value) for value in rewards)
    if mode == "zero":
        return (0.0,) * len(rewards)
    if mode != "within_episode_permuted":
        raise ValueError("mode must be true, within_episode_permuted, or zero")
    if len(rewards) < 2:
        return tuple(float(value) for value in rewards)
    permutation = list(range(len(rewards)))
    rng = random.Random(seed)
    for _ in range(128):
        rng.shuffle(permutation)
        if all(index != permutation[index] for index in range(len(permutation))):
            break
    else:
        permutation = list(range(1, len(permutation))) + [0]
    return tuple(float(rewards[index]) for index in permutation)


def run_episode(
    controller: LinearQ | FixedRandom | LocalHeuristic | VisibleGreedy,
    task: RepairTask,
    *,
    feedback_mode: str = "true",
    epsilon: float = 0.0,
) -> dict[str, object]:
    """Run exactly eight charged decisions; hidden metrics remain evaluator-side."""

    if isinstance(controller, LinearQ):
        trajectory = collect_trajectory(task, seed=task.seed ^ 0xC0FFEE, epsilon=epsilon)
        transmitted = _replay_feedback(controller, trajectory, feedback_mode, task.seed ^ 0xBEEF)
        return {
            "f1": trajectory.f1,
            "exact": trajectory.exact,
            "precision": 0.0,
            "recall": 0.0,
            "reward": sum(step.reward for step in trajectory.steps),
            "actions": tuple(step.action for step in trajectory.steps),
            "feedback": transmitted,
            "charged": len(trajectory.steps),
            "updates": controller.updates,
        }
    return evaluate_policy(controller, task)


def derange_whole_geometry_batch(
    geometries: Sequence[tuple[Fraction, ...]], seed: int = 0
) -> tuple[tuple[Fraction, ...], ...]:
    """Batch-synchronously derange whole geometry observations.

    Only the observation payload is permuted.  The source tuple multiset is
    preserved exactly, no item remains in its original batch slot, and no
    physical state, reward, or action reachability is touched.
    """

    if len(geometries) < 2:
        raise ValueError("at least two geometries are required")
    order = list(range(len(geometries)))
    rng = random.Random(seed)
    for _ in range(128):
        rng.shuffle(order)
        if all(source != target for source, target in enumerate(order)):
            break
    else:
        order = list(range(1, len(order))) + [0]
    return tuple(tuple(geometries[index]) for index in order)


def controller_geometry(view: ControllerView) -> tuple[object, ...]:
    """The fixed-width controller-facing geometry tuple ``G``."""

    return (*view.local_gap_bins, *view.local_ratio_bins, view.cursor_relation_bin)


def derange_controller_views(
    views: Sequence[ControllerView], seed: int = 0
) -> tuple[ControllerView, ...]:
    """Derange only ``G`` while preserving each view's ``U`` channels.

    ``U`` is (remaining budget, last transmitted reward, trusted goal).  The
    physical environments are not touched; this is a batch-synchronous
    observation intervention for a controller ablation.
    """

    if len(views) < 2:
        raise ValueError("at least two views are required")
    permutation = list(range(len(views)))
    rng = random.Random(seed)
    for _ in range(128):
        rng.shuffle(permutation)
        if all(index != permutation[index] for index in range(len(permutation))):
            break
    else:
        permutation = list(range(1, len(permutation))) + [0]
    output: list[ControllerView] = []
    for original, source_index in zip(views, permutation):
        source = views[source_index]
        output.append(
            ControllerView(
                source.local_gap_bins,
                source.local_ratio_bins,
                source.cursor_relation_bin,
                original.remaining_budget_fraction,
                original.last_scalar_reward,
                original.trusted_goal,
            )
        )
    return tuple(output)


def geometry_multiset(geometries: Iterable[tuple[Fraction, ...]]) -> tuple[tuple[Fraction, ...], ...]:
    """Canonical evaluator-side multiset representation for invariant tests."""

    return tuple(sorted((tuple(geometry) for geometry in geometries), key=repr))


derange_geometry_observations = derange_whole_geometry_batch
derange_whole_geometry = derange_whole_geometry_batch
derange_views = derange_controller_views
derange_controller_batch = derange_controller_views
RandomBaseline = FixedRandom
FixedBaseline = LocalHeuristic
VisibleGreedyBaseline = VisibleGreedy


def task_environment(task: RepairTask) -> V4Environment:
    """Public constructor for tests; the returned environment is evaluator-owned."""

    return V4Environment(task)


__all__ = [
    "ACTION_BUDGET", "POLICY_ACTIONS", "V4_ACTIONS", "ControllerView", "V4Environment",
    "HiddenMetrics", "LinearQ", "FixedRandom", "LocalHeuristic", "VisibleGreedy",
    "TrajectoryStep", "Trajectory", "collect_trajectory", "replay_trajectory", "evaluate_policy",
    "episode_feedback", "run_episode", "evaluator_metrics", "derange_whole_geometry_batch",
    "derange_geometry_observations", "derange_whole_geometry", "controller_geometry",
    "derange_controller_views", "derange_views", "derange_controller_batch", "geometry_multiset",
    "task_environment", "RandomBaseline", "FixedBaseline", "VisibleGreedyBaseline", "_geometry_tuple",
]
