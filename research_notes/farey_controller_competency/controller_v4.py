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
TRAINING_PROTOCOL = "offline_reward_attribution_replay"


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
        task_goal = GoalState.coerce(task.goal)
        active_goal = GoalState.coerce(goal) if goal is not None else task_goal
        base = StrictEnvironment(
            task.order,
            task.pattern,
            damage_count=task.damage_count,
            seed=task.seed,
            rotation=True,
            action_budget=ACTION_BUDGET,
            goal=active_goal,
        )
        self._target = tuple(base._target)
        self._initial_points = tuple(base._initial_points)
        self._deleted_points = tuple(base._deleted_points)
        self._points = tuple(base._points)
        self._cursor = int(base._cursor)
        self._initial_cursor = int(base._initial_cursor)
        self._remaining = ACTION_BUDGET
        self._goal = active_goal
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
        if right > left and right >= outer_right:
            return "move_right"
        if left > right and left >= outer_left:
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
    precision: float
    recall: float
    f1: float
    exact: float


@dataclass(frozen=True, slots=True)
class TrainedLane:
    """One frozen offline reward-attribution learner and its audit receipt."""

    mode: str
    controller: LinearQ
    trajectories: tuple[Trajectory, ...]
    before_digest: str
    after_digest: str
    before_updates: int
    after_updates: int
    update_delta: int
    action_schedule: tuple[tuple[str, ...], ...]
    nonzero_reward_count: int


def batch_diagnostics(trajectories: Sequence[Trajectory]) -> dict[str, object]:
    actions = tuple(step.action for trajectory in trajectories for step in trajectory.steps)
    rewards = tuple(step.reward for trajectory in trajectories for step in trajectory.steps)
    informative = sum(abs(reward) > 1.0e-12 for reward in rewards)
    return {
        "trajectory_count": len(trajectories),
        "transition_count": len(actions),
        "action_set": tuple(action for action in V4_ACTIONS if action in set(actions)),
        "action_coverage": len(set(actions)),
        "nonzero_reward_count": informative,
        "distinct_reward_count": len(set(rewards)),
    }


def assert_informative_batch(
    trajectories: Sequence[Trajectory], *, require_all_actions: bool = True
) -> dict[str, object]:
    diagnostics = batch_diagnostics(trajectories)
    if int(diagnostics["nonzero_reward_count"]) == 0:
        raise AssertionError("training batch has no nonzero physical rewards")
    if require_all_actions and int(diagnostics["action_coverage"]) != len(V4_ACTIONS):
        raise AssertionError("training batch does not cover all twelve V3.4 actions")
    return diagnostics


def collect_trajectory(task: RepairTask, *, seed: int = 0, epsilon: float = 0.0) -> Trajectory:
    """Collect one fixed exploratory trajectory before offline replay."""

    environment = V4Environment(task)
    steps: list[TrajectoryStep] = []
    # A seeded cyclic schedule is deliberately action-covering.  Feedback
    # lanes replay these same physical transitions; no lane controls data
    # collection, so reward attribution is the only intervention.
    offset = (int(seed) + int(task.seed)) % len(V4_ACTIONS)
    for step_index in range(ACTION_BUDGET):
        view = _view(environment, 0.0)
        action = V4_ACTIONS[(offset + step_index) % len(V4_ACTIONS)]
        if epsilon and random.Random(seed ^ step_index).random() < epsilon:
            action = V4_ACTIONS[random.Random(seed ^ (step_index << 8)).randrange(len(V4_ACTIONS))]
        reward = environment.step(action)
        next_view = _view(environment, 0.0)
        steps.append(TrajectoryStep(view, action, reward, next_view, environment._done))
    hidden = evaluator_metrics(environment)
    return Trajectory(tuple(steps), hidden.precision, hidden.recall, hidden.f1, hidden.exact)


def train_reward_lanes(
    tasks: Sequence[RepairTask],
    *,
    seed: int = 0,
    seeds: Sequence[int] | None = None,
    init_seed: int = 0,
    modes: Sequence[str] = ("true", "within_episode_permuted", "zero"),
    require_all_actions: bool = True,
) -> dict[str, TrainedLane]:
    """Train matched true/permuted/zero lanes by offline reward replay.

    Physical trajectories are collected once with an action-covering schedule;
    every lane receives identical states, actions, initialization, and update
    count.  The resulting learners are frozen before held-out evaluation.
    """

    task_list = tuple(tasks)
    if not task_list:
        raise ValueError("at least one training task is required")
    collector_seeds = (
        tuple(int(value) for value in seeds)
        if seeds is not None
        else tuple(seed + index * ACTION_BUDGET for index in range(len(task_list)))
    )
    if len(collector_seeds) != len(task_list):
        raise ValueError("seeds must match the number of training tasks")
    trajectories = tuple(
        collect_trajectory(
            task,
            seed=collector_seeds[index] - int(task.seed),
        )
        for index, task in enumerate(task_list)
    )
    assert_informative_batch(trajectories, require_all_actions=require_all_actions)
    lanes: dict[str, TrainedLane] = {}
    for lane_index, mode in enumerate(modes):
        learner = LinearQ(init_seed)
        before_digest, before_updates = learner.digest(), learner.updates
        for trajectory_index, trajectory in enumerate(trajectories):
            _replay_feedback(
                learner,
                trajectory,
                mode,
                seed ^ (lane_index << 16) ^ trajectory_index,
            )
        after_digest, after_updates = learner.digest(), learner.updates
        learner.freeze()
        lanes[mode] = TrainedLane(
            mode,
            learner,
            trajectories,
            before_digest,
            after_digest,
            before_updates,
            after_updates,
            after_updates - before_updates,
            tuple(tuple(step.action for step in trajectory.steps) for trajectory in trajectories),
            int(batch_diagnostics(trajectories)["nonzero_reward_count"]),
        )
    return lanes


def evaluate_frozen_lanes(
    lanes: dict[str, TrainedLane], heldout_tasks: Sequence[RepairTask]
) -> dict[str, tuple[dict[str, object], ...]]:
    """Evaluate frozen learners greedily on held-out tasks without updates."""

    results: dict[str, tuple[dict[str, object], ...]] = {}
    for mode, lane in lanes.items():
        before_digest, before_updates = lane.controller.digest(), lane.controller.updates
        rows = tuple(evaluate_policy(lane.controller, task) for task in heldout_tasks)
        if lane.controller.digest() != before_digest or lane.controller.updates != before_updates:
            raise AssertionError("frozen held-out evaluation changed learner state")
        results[mode] = rows
    return results


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
    """Run a baseline episode or offline reward-attribution replay for LinearQ."""

    if isinstance(controller, LinearQ):
        trajectory = collect_trajectory(task, seed=task.seed ^ 0xC0FFEE, epsilon=epsilon)
        transmitted = _replay_feedback(controller, trajectory, feedback_mode, task.seed ^ 0xBEEF)
        return {
            "f1": trajectory.f1,
            "exact": trajectory.exact,
            "precision": trajectory.precision,
            "recall": trajectory.recall,
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


def _derangement_indices(size: int, seed: int) -> tuple[int, ...]:
    if size < 2:
        raise ValueError("at least two batch items are required")
    permutation = list(range(size))
    rng = random.Random(seed)
    for _ in range(128):
        rng.shuffle(permutation)
        if all(index != permutation[index] for index in range(size)):
            return tuple(permutation)
    return tuple(range(1, size)) + (0,)


@dataclass(frozen=True, slots=True)
class DerangedControllerBatch:
    views: tuple[ControllerView, ...]
    source_indices: tuple[int, ...]


def derange_controller_views(
    views: Sequence[ControllerView], seed: int = 0
) -> tuple[ControllerView, ...]:
    """Derange only ``G`` while preserving each view's ``U`` channels.

    ``U`` is (remaining budget, last transmitted reward, trusted goal).  The
    physical environments are not touched; this is a batch-synchronous
    observation intervention for a controller ablation.
    """

    permutation = _derangement_indices(len(views), seed)
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


def derange_controller_batch(
    views: Sequence[ControllerView], seed: int = 0
) -> DerangedControllerBatch:
    """Return G-deranged views plus source indices, including duplicate Gs."""

    source_indices = _derangement_indices(len(views), seed)
    return DerangedControllerBatch(derange_controller_views(views, seed), source_indices)


@dataclass(frozen=True, slots=True)
class BatchRollout:
    """Synchronous policy rollout receipt; all exact state stays evaluator-side."""

    view_schedule: tuple[tuple[ControllerView, ...], ...]
    source_index_schedule: tuple[tuple[int, ...], ...]
    action_schedule: tuple[tuple[str, ...], ...]
    reward_schedule: tuple[tuple[float, ...], ...]


def synchronous_batch_rollout(
    tasks: Sequence[RepairTask],
    controller: LinearQ | FixedRandom | LocalHeuristic | VisibleGreedy | None = None,
    *,
    seed: int = 0,
    derange: bool = False,
    replay_actions: Sequence[Sequence[str]] | None = None,
) -> BatchRollout:
    """Roll out a batch synchronously, optionally deranging only controller G.

    ``replay_actions`` allows a matched physical replay: changing observations
    cannot change the recorded rewards or reachable states when actions are
    held fixed.  Source indices are retained even if two G tuples are equal.
    """

    task_list = tuple(tasks)
    if not task_list:
        raise ValueError("at least one batch task is required")
    if replay_actions is not None and len(replay_actions) != ACTION_BUDGET:
        raise ValueError("replay_actions must have eight synchronous rows")
    environments = [V4Environment(task) for task in task_list]
    previous = [0.0] * len(task_list)
    views_by_step: list[tuple[ControllerView, ...]] = []
    indices_by_step: list[tuple[int, ...]] = []
    actions_by_step: list[tuple[str, ...]] = []
    rewards_by_step: list[tuple[float, ...]] = []
    for step_index in range(ACTION_BUDGET):
        base_views = tuple(_view(environment, previous[index]) for index, environment in enumerate(environments))
        packet = (
            derange_controller_batch(base_views, seed + step_index)
            if derange and len(base_views) >= 2
            else DerangedControllerBatch(base_views, tuple(range(len(base_views))))
        )
        if replay_actions is not None:
            actions = tuple(str(action) for action in replay_actions[step_index])
            if len(actions) != len(task_list) or any(action not in V4_ACTIONS for action in actions):
                raise ValueError("each replay action row must match the batch and vocabulary")
        elif controller is None:
            actions = tuple(V4_ACTIONS[(seed + step_index + index) % len(V4_ACTIONS)] for index in range(len(task_list)))
        else:
            actions = tuple(
                controller.choose(view) if not isinstance(controller, LinearQ) else controller.choose(view)
                for view in packet.views
            )
        rewards = tuple(environment.step(action) for environment, action in zip(environments, actions))
        previous = list(rewards)
        views_by_step.append(packet.views)
        indices_by_step.append(packet.source_indices)
        actions_by_step.append(actions)
        rewards_by_step.append(rewards)
    return BatchRollout(
        tuple(views_by_step),
        tuple(indices_by_step),
        tuple(actions_by_step),
        tuple(rewards_by_step),
    )


def geometry_multiset(geometries: Iterable[tuple[Fraction, ...]]) -> tuple[tuple[Fraction, ...], ...]:
    """Canonical evaluator-side multiset representation for invariant tests."""

    return tuple(sorted((tuple(geometry) for geometry in geometries), key=repr))


derange_geometry_observations = derange_whole_geometry_batch
derange_whole_geometry = derange_whole_geometry_batch
derange_views = derange_controller_views
RandomBaseline = FixedRandom
FixedBaseline = LocalHeuristic
VisibleGreedyBaseline = VisibleGreedy


def task_environment(task: RepairTask) -> V4Environment:
    """Public constructor for tests; the returned environment is evaluator-owned."""

    return V4Environment(task)


__all__ = [
    "ACTION_BUDGET", "POLICY_ACTIONS", "V4_ACTIONS", "TRAINING_PROTOCOL", "ControllerView", "V4Environment",
    "HiddenMetrics", "LinearQ", "FixedRandom", "LocalHeuristic", "VisibleGreedy",
    "TrajectoryStep", "Trajectory", "TrainedLane", "collect_trajectory", "replay_trajectory",
    "train_reward_lanes", "evaluate_frozen_lanes", "batch_diagnostics", "assert_informative_batch",
    "evaluate_policy", "BatchRollout", "synchronous_batch_rollout",
    "episode_feedback", "run_episode", "evaluator_metrics", "derange_whole_geometry_batch",
    "derange_geometry_observations", "derange_whole_geometry", "controller_geometry",
    "derange_controller_views", "derange_controller_batch", "DerangedControllerBatch", "derange_views", "geometry_multiset",
    "task_environment", "RandomBaseline", "FixedBaseline", "VisibleGreedyBaseline", "_geometry_tuple",
]
