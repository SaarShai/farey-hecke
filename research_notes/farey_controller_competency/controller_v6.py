"""V6 controller/experiment engine over the frozen V5 shell.

The V5 interface is fixed at eighteen actions and sixteen charged decisions.
This module contains no manifest, task generator, or private test labels.  A
public training stream supplies fresh evaluator-owned environments; a frozen
test accessor supplies held-out result rows after policies are frozen.  Exact
points and identity metrics remain evaluator-side.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from hashlib import sha256
import json
import math
import random
import statistics
from typing import Any, Iterable, Iterator, Mapping, Protocol, Sequence

try:
    from .competency_v5_feasibility import (
        ACTION_BUDGET,
        ACTION_VOCABULARY,
        INSERTION_ACTIONS,
        _insert_transition,
        _movement_offset,
    )
    from .controller_v4 import ControllerView
    from .strict_environment import GoalState, StrictEnvironment, _coverage, _gap_bin, _ratio_bin, _spectral
except ImportError:  # direct execution from this directory
    from competency_v5_feasibility import (  # type: ignore[no-redef]
        ACTION_BUDGET,
        ACTION_VOCABULARY,
        INSERTION_ACTIONS,
        _insert_transition,
        _movement_offset,
    )
    from controller_v4 import ControllerView  # type: ignore[no-redef]
    from strict_environment import GoalState, StrictEnvironment, _coverage, _gap_bin, _ratio_bin, _spectral  # type: ignore[no-redef]


V6_ACTIONS: tuple[str, ...] = tuple(ACTION_VOCABULARY)
V6_BUDGET = int(ACTION_BUDGET)
TRAINING_PROTOCOL = "offline_reward_attribution_replay"
FEEDBACK_MODES = ("true", "within_episode_permuted", "zero")
CHANNELS = ("I", "S")
MIN_TRAIN_EPISODES = 2
# The sealed adapter supplies twelve paired public training seeds.  The core
# remains stream-shaped so deterministic unit fixtures can use fewer replicas.
MATCHED_SEED_COUNT = 12

# Locked gate thresholds.  They are constants, not fit to result rows.
FEEDBACK_DELTA = 0.05
RECOVERY_PRECISION = 0.75
RECOVERY_RECALL = 0.50
RECOVERY_F1 = 0.50
RECOVERY_EXACT = 0.25
TRANSFER_DELTA = 0.05
STRUCTURAL_DELTA = 0.05
STRUCTURAL_CI_LOW = 0.02


class PublicTrainEpisode(Protocol):
    """Public adapter boundary; no task labels are required by the engine."""

    def fresh_environment(self) -> "V6Environment": ...


class PublicTrainStream(Protocol):
    def __iter__(self) -> Iterator[PublicTrainEpisode]: ...


class FrozenTestAccessor(Protocol):
    """Final adapter boundary for gated held-out evaluation."""

    def evaluate_frozen(
        self, policies: Mapping[str, "V6LinearQ"]
    ) -> Mapping[str, Sequence[Mapping[str, Any]]]: ...

    def evaluate_structural_frozen(
        self, policies: Mapping[str, "V6LinearQ"]
    ) -> Mapping[str, Sequence[Mapping[str, Any]]]: ...


def _goal(value: GoalState | str) -> GoalState:
    return GoalState.coerce(value)


class V6Environment:
    """Evaluator-owned physical state with exact V5 action semantics."""

    __slots__ = (
        "_target", "_initial_points", "_deleted_points", "_points", "_cursor",
        "_initial_cursor", "_remaining", "_goal", "_done", "_action_budget",
    )

    @classmethod
    def from_strict(cls, source: StrictEnvironment) -> "V6Environment":
        if int(source._action_budget) != V6_BUDGET:
            raise ValueError("V6 requires a sixteen-action-budget strict shell")
        instance = cls.__new__(cls)
        instance._target = tuple(source._target)
        instance._initial_points = tuple(source._initial_points)
        instance._deleted_points = tuple(source._deleted_points)
        instance._points = tuple(source._points)
        instance._cursor = int(source._cursor)
        instance._initial_cursor = int(source._initial_cursor)
        instance._remaining = int(source._remaining_budget)
        instance._goal = _goal(source._goal)
        instance._done = bool(source._done)
        instance._action_budget = V6_BUDGET
        return instance

    @property
    def view(self) -> ControllerView:
        return _make_view(self)

    def step(self, action: str) -> float:
        if self._done:
            raise RuntimeError("episode is already done")
        if action not in V6_ACTIONS:
            raise ValueError(f"unknown V6 action: {action}")
        before = self._metric()
        self._remaining -= 1
        if action in V6_ACTIONS[:14]:
            self._cursor = (self._cursor + _movement_offset(action, len(self._points))) % len(self._points)
        else:
            self._points, self._cursor, _added = _insert_transition(self._points, self._cursor, action)
        after = self._metric()
        self._done = self._remaining <= 0
        return float(round(before - after, 6))

    def _metric(self) -> float:
        return _coverage(self._points) if self._goal is GoalState.COVERAGE else _spectral(self._points)


def _make_view(environment: V6Environment, feedback: float = 0.0) -> ControllerView:
    points, cursor = environment._points, environment._cursor
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
        float(round(environment._remaining / V6_BUDGET, 6)),
        float(feedback),
        0 if environment._goal is GoalState.COVERAGE else 1,
    )


@dataclass(frozen=True, slots=True)
class HiddenMetrics:
    precision: float
    recall: float
    f1: float
    exact: float


def evaluator_metrics(environment: V6Environment) -> HiddenMetrics:
    target, initial, current = set(environment._target), set(environment._initial_points), set(environment._points)
    deleted, additions = target - initial, current - initial
    true_positive = len(additions & deleted)
    false_positive = len(additions - target)
    precision = true_positive / len(additions) if additions else 0.0
    recall = true_positive / len(deleted) if deleted else 1.0
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    return HiddenMetrics(precision, recall, f1, float(current == target))


class V6LinearQ:
    """Linear Q learner with fixed features and no evaluator-side fields."""

    def __init__(self, seed: int = 0, *, learning: bool = True, gamma: float = 0.90) -> None:
        self._rng = random.Random(seed)
        width = len(ControllerView((0, 0, 0, 0), (0, 0), 0, 1.0, 0.0, 0).features())
        self._weights = [[0.0] * width for _ in V6_ACTIONS]
        self.learning = learning
        self.gamma = float(gamma)
        self.updates = 0

    def choose(self, view: ControllerView, *, epsilon: float = 0.0) -> str:
        if epsilon and self._rng.random() < epsilon:
            return self._rng.choice(V6_ACTIONS)
        values = [sum(weight * feature for weight, feature in zip(row, view.features())) for row in self._weights]
        best = max(values)
        return V6_ACTIONS[next(index for index, value in enumerate(values) if value == best)]

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
        index = V6_ACTIONS.index(action)
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

    def clone_frozen(self) -> "V6LinearQ":
        clone = V6LinearQ(0, learning=False, gamma=self.gamma)
        clone._weights = [list(row) for row in self._weights]
        clone.updates = self.updates
        return clone


class V6Random:
    updates = 0

    def __init__(self, seed: int = 0) -> None:
        self._rng = random.Random(seed)

    def choose(self, view: ControllerView) -> str:
        del view
        return self._rng.choice(V6_ACTIONS)


class V6Local:
    updates = 0

    def choose(self, view: ControllerView) -> str:
        outer_left, left, right, outer_right = view.local_gap_bins
        if max(left, right) >= max(outer_left, outer_right):
            return "insert_mediant"
        return "move_left" if outer_left > outer_right else "move_right"


class V6VisibleGreedy:
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


def episode_feedback(rewards: Sequence[float], mode: str, seed: int) -> tuple[float, ...]:
    if mode == "true":
        return tuple(float(value) for value in rewards)
    if mode == "zero":
        return (0.0,) * len(rewards)
    if mode != "within_episode_permuted":
        raise ValueError("feedback mode must be true, within_episode_permuted, or zero")
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


def collect_trajectory(environment: V6Environment, *, seed: int = 0) -> Trajectory:
    """Collect a fixed action-covering schedule before any reward lane runs."""

    steps: list[TrajectoryStep] = []
    offset = int(seed) % len(V6_ACTIONS)
    for step_index in range(V6_BUDGET):
        view = _make_view(environment, 0.0)
        action = V6_ACTIONS[(offset + step_index) % len(V6_ACTIONS)]
        reward = environment.step(action)
        next_view = _make_view(environment, 0.0)
        steps.append(TrajectoryStep(view, action, reward, next_view, environment._done))
    hidden = evaluator_metrics(environment)
    return Trajectory(tuple(steps), hidden.precision, hidden.recall, hidden.f1, hidden.exact)


def _replay(controller: V6LinearQ, trajectory: Trajectory, mode: str, seed: int) -> tuple[float, ...]:
    transmitted = episode_feedback(tuple(step.reward for step in trajectory.steps), mode, seed)
    previous = 0.0
    for step, reward in zip(trajectory.steps, transmitted):
        view = replace(step.view, last_scalar_reward=previous)
        next_view = replace(step.next_view, last_scalar_reward=reward)
        controller.update(view, step.action, reward, next_view=next_view, done=step.done)
        previous = reward
    return transmitted


@dataclass(frozen=True, slots=True)
class TrainedLane:
    mode: str
    controller: V6LinearQ
    trajectories: tuple[Trajectory, ...]
    before_digest: str
    after_digest: str
    before_updates: int
    after_updates: int
    update_delta: int
    action_schedule: tuple[tuple[str, ...], ...]
    transmitted_rewards: tuple[tuple[float, ...], ...]


def train_reward_lanes(
    stream: PublicTrainStream,
    *,
    seed: int = 0,
    init_seed: int = 0,
    modes: Sequence[str] = FEEDBACK_MODES,
    require_action_coverage: bool = True,
) -> dict[str, TrainedLane]:
    """Train matched offline reward-attribution lanes from a public stream."""

    episodes = tuple(stream)
    if not episodes:
        raise ValueError("public training stream is empty")
    trajectories = tuple(
        collect_trajectory(episode.fresh_environment(), seed=seed + index * V6_BUDGET)
        for index, episode in enumerate(episodes)
    )
    actions = {step.action for trajectory in trajectories for step in trajectory.steps}
    nonzero = [step.reward for trajectory in trajectories for step in trajectory.steps if abs(step.reward) > 1e-12]
    if len(nonzero) < 2 or len(set(nonzero)) < 2:
        raise AssertionError("training stream lacks preregistered informative reward variation")
    if require_action_coverage and actions != set(V6_ACTIONS):
        raise AssertionError("training stream does not cover all eighteen actions")
    lanes: dict[str, TrainedLane] = {}
    transmitted_by_mode: dict[str, tuple[tuple[float, ...], ...]] = {}
    for mode in modes:
        if mode not in FEEDBACK_MODES:
            raise ValueError(f"unsupported feedback mode: {mode}")
        learner = V6LinearQ(init_seed)
        before_digest, before_updates = learner.digest(), learner.updates
        # Every lane sees the same transition order and the same permutation
        # seed.  Only the transmitted reward transform differs.
        rows = tuple(
            _replay(learner, trajectory, mode, seed ^ index)
            for index, trajectory in enumerate(trajectories)
        )
        after_digest, after_updates = learner.digest(), learner.updates
        learner.freeze()
        transmitted_by_mode[mode] = rows
        lanes[mode] = TrainedLane(
            mode, learner, trajectories, before_digest, after_digest,
            before_updates, after_updates, after_updates - before_updates,
            tuple(tuple(step.action for step in trajectory.steps) for trajectory in trajectories), rows,
        )
    if "true" in transmitted_by_mode and "within_episode_permuted" in transmitted_by_mode:
        if transmitted_by_mode["true"] == transmitted_by_mode["within_episode_permuted"]:
            raise AssertionError("within-episode permutation was not causal on the stream")
    if len(lanes) > 1 and len({lane.after_digest for lane in lanes.values()}) == 1:
        raise AssertionError("all reward lanes have the same post-training digest")
    return lanes


def evaluate_frozen_lanes(
    lanes: Mapping[str, TrainedLane], accessor: FrozenTestAccessor
) -> Mapping[str, Sequence[Mapping[str, Any]]]:
    policies = {name: lane.controller for name, lane in lanes.items()}
    before = {name: (lane.controller.digest(), lane.controller.updates) for name, lane in lanes.items()}
    rows = accessor.evaluate_frozen(policies)
    for name, lane in lanes.items():
        if before[name] != (lane.controller.digest(), lane.controller.updates):
            raise AssertionError("frozen test accessor changed a learner")
    return rows


def _derangement_indices(size: int, seed: int) -> tuple[int, ...]:
    if size < 2:
        raise ValueError("a structural batch needs at least two replicas")
    permutation = list(range(size))
    rng = random.Random(seed)
    for _ in range(128):
        rng.shuffle(permutation)
        if all(index != permutation[index] for index in range(size)):
            return tuple(permutation)
    return tuple(range(1, size)) + (0,)


def controller_geometry(view: ControllerView) -> tuple[int, ...]:
    return (*view.local_gap_bins, *view.local_ratio_bins, view.cursor_relation_bin)


@dataclass(frozen=True, slots=True)
class DerangedBatch:
    views: tuple[ControllerView, ...]
    source_indices: tuple[int, ...]


def derange_controller_views(views: Sequence[ControllerView], seed: int = 0) -> DerangedBatch:
    source_indices = _derangement_indices(len(views), seed)
    output = tuple(
        ControllerView(
            views[source].local_gap_bins,
            views[source].local_ratio_bins,
            views[source].cursor_relation_bin,
            views[index].remaining_budget_fraction,
            views[index].last_scalar_reward,
            views[index].trusted_goal,
        )
        for index, source in enumerate(source_indices)
    )
    return DerangedBatch(output, source_indices)


@dataclass(frozen=True, slots=True)
class BatchRollout:
    views: tuple[tuple[ControllerView, ...], ...]
    source_indices: tuple[tuple[int, ...], ...]
    actions: tuple[tuple[str, ...], ...]
    rewards: tuple[tuple[float, ...], ...]


def _batch_rollout(
    environments: Sequence[V6Environment],
    controller: V6LinearQ | None,
    *,
    channel: str,
    seed: int,
    replay_actions: Sequence[Sequence[str]] | None = None,
) -> BatchRollout:
    if channel not in CHANNELS:
        raise ValueError("channel must be I or S")
    if len(environments) < 2:
        raise ValueError("structural rollout needs at least two replicas")
    previous = [0.0] * len(environments)
    views_rows: list[tuple[ControllerView, ...]] = []
    source_rows: list[tuple[int, ...]] = []
    action_rows: list[tuple[str, ...]] = []
    reward_rows: list[tuple[float, ...]] = []
    if replay_actions is not None and len(replay_actions) != V6_BUDGET:
        raise ValueError("replay action schedule must contain sixteen rows")
    for step_index in range(V6_BUDGET):
        identity = tuple(_make_view(environment, previous[index]) for index, environment in enumerate(environments))
        packet = derange_controller_views(identity, seed + step_index) if channel == "S" else DerangedBatch(identity, tuple(range(len(identity))))
        if replay_actions is None:
            if controller is None:
                actions = tuple(V6_ACTIONS[(seed + step_index + index) % len(V6_ACTIONS)] for index in range(len(environments)))
            else:
                actions = tuple(controller.choose(view) for view in packet.views)
        else:
            actions = tuple(str(action) for action in replay_actions[step_index])
        if len(actions) != len(environments) or any(action not in V6_ACTIONS for action in actions):
            raise ValueError("action row does not match structural batch")
        rewards = tuple(environment.step(action) for environment, action in zip(environments, actions))
        previous = list(rewards)
        views_rows.append(packet.views)
        source_rows.append(packet.source_indices)
        action_rows.append(actions)
        reward_rows.append(rewards)
    return BatchRollout(tuple(views_rows), tuple(source_rows), tuple(action_rows), tuple(reward_rows))


def synchronous_structural_rollout(
    environments: Sequence[V6Environment],
    controller: V6LinearQ | None = None,
    *,
    channel: str = "I",
    seed: int = 0,
    replay_actions: Sequence[Sequence[str]] | None = None,
) -> BatchRollout:
    """Public wrapper for one synchronous identity/scrambled channel rollout."""

    return _batch_rollout(
        environments,
        controller,
        channel=channel,
        seed=seed,
        replay_actions=replay_actions,
    )


def train_structural_lanes(
    stream: PublicTrainStream, *, seed: int = 0, init_seed: int = 0
) -> Mapping[str, TrainedLane]:
    """Train identity and scrambled channel lanes on matched physical replay."""

    episodes = tuple(stream)
    if len(episodes) < MIN_TRAIN_EPISODES:
        raise ValueError("structural training needs at least two public replicas")
    lanes: dict[str, TrainedLane] = {}
    for source_channel in CHANNELS:
        environments = [episode.fresh_environment() for episode in episodes]
        rollout = _batch_rollout(environments, None, channel=source_channel, seed=seed)
        trajectories = []
        for index in range(len(environments)):
            steps = tuple(
                TrajectoryStep(
                    rollout.views[step][index],
                    rollout.actions[step][index],
                    rollout.rewards[step][index],
                    rollout.views[step + 1][index] if step + 1 < V6_BUDGET else rollout.views[step][index],
                    step == V6_BUDGET - 1,
                )
                for step in range(V6_BUDGET)
            )
            hidden = evaluator_metrics(environments[index])
            trajectories.append(Trajectory(steps, hidden.precision, hidden.recall, hidden.f1, hidden.exact))
        learner = V6LinearQ(init_seed)
        before_digest, before_updates = learner.digest(), learner.updates
        for index, trajectory in enumerate(trajectories):
            _replay(learner, trajectory, "true", seed ^ index)
        after_digest, after_updates = learner.digest(), learner.updates
        learner.freeze()
        frozen = TrainedLane(
            source_channel, learner, tuple(trajectories), before_digest, after_digest,
            before_updates, after_updates, after_updates - before_updates,
            tuple(tuple(step.action for step in trajectory.steps) for trajectory in trajectories),
            tuple(tuple(step.reward for step in trajectory.steps) for trajectory in trajectories),
        )
        target_channels = ("I", "S")
        for target_channel in target_channels:
            lanes[f"{source_channel}\u2192{target_channel}"] = replace(frozen, mode=f"{source_channel}\u2192{target_channel}", controller=learner.clone_frozen())
    return lanes


def evaluate_structural_lanes(
    lanes: Mapping[str, TrainedLane], accessor: FrozenTestAccessor
) -> Mapping[str, Sequence[Mapping[str, Any]]]:
    policies = {name: lane.controller for name, lane in lanes.items()}
    before = {name: (lane.controller.digest(), lane.controller.updates) for name, lane in lanes.items()}
    rows = accessor.evaluate_structural_frozen(policies)
    for name, lane in lanes.items():
        if before[name] != (lane.controller.digest(), lane.controller.updates):
            raise AssertionError("frozen structural accessor changed a learner")
    return rows


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    effect: float
    ci_low: float
    ci_high: float
    groups: int
    pairs: int


def _row_cell(row: Mapping[str, Any], cell_key: str = "cell") -> Any:
    """Resolve an explicit cell, or the adapter's N/family/goal composite."""

    if row.get(cell_key) is not None:
        return row[cell_key]
    if cell_key == "cell":
        return (row.get("N", row.get("n")), row.get("family"), row.get("goal"))
    return row.get(cell_key)


def paired_hierarchical_bootstrap(
    treatment: Sequence[Mapping[str, Any]],
    control: Sequence[Mapping[str, Any]],
    *,
    metric: str = "f1",
    group_key: str = "seed",
    cell_key: str = "cell",
    resamples: int = 1000,
    seed: int = 0,
) -> BootstrapResult:
    """Bootstrap group means, resampling groups then cells within groups."""

    treatment_map = {(row.get(group_key), _row_cell(row, cell_key)): float(row[metric]) for row in treatment}
    control_map = {(row.get(group_key), _row_cell(row, cell_key)): float(row[metric]) for row in control}
    keys = tuple(sorted(set(treatment_map) & set(control_map), key=repr))
    if not keys or set(treatment_map) != set(control_map):
        raise ValueError("paired bootstrap requires identical group/cell keys")
    by_group: dict[Any, list[float]] = {}
    for key in keys:
        by_group.setdefault(key[0], []).append(treatment_map[key] - control_map[key])
    group_values = tuple(statistics.fmean(values) for values in by_group.values())
    effect = statistics.fmean(group_values)
    rng = random.Random(seed)
    samples: list[float] = []
    groups = tuple(by_group.values())
    for _ in range(max(1, resamples)):
        sampled_groups = []
        for _group in groups:
            values = [rng.choice(_group) for _ in _group]
            sampled_groups.append(statistics.fmean(values))
        samples.append(statistics.fmean(sampled_groups))
    samples.sort()
    low = samples[max(0, int(0.025 * len(samples)))]
    high = samples[min(len(samples) - 1, int(0.975 * len(samples)))]
    return BootstrapResult(effect, low, high, len(groups), len(keys))


def _positive(
    result: BootstrapResult,
    threshold: float,
    ci_floor: float = 0.0,
    *,
    inclusive_floor: bool = False,
) -> bool:
    ci_ok = result.ci_low >= ci_floor if inclusive_floor else result.ci_low > ci_floor
    return result.effect >= threshold and ci_ok


def feedback_gate(
    true_rows: Sequence[Mapping[str, Any]],
    permuted_rows: Sequence[Mapping[str, Any]],
    zero_rows: Sequence[Mapping[str, Any]],
    *,
    resamples: int = 1000,
) -> dict[str, Any]:
    comparisons: dict[str, BootstrapResult] = {}
    try:
        comparisons = {
            "permuted": paired_hierarchical_bootstrap(true_rows, permuted_rows, resamples=resamples, seed=11),
            "zero": paired_hierarchical_bootstrap(true_rows, zero_rows, resamples=resamples, seed=13),
        }
    except (ValueError, KeyError, statistics.StatisticsError):
        comparisons = {}
    valid = bool(comparisons) and all(result.groups >= 2 for result in comparisons.values())
    positive = valid and all(_positive(result, FEEDBACK_DELTA) for result in comparisons.values())
    return {"gate": "feedback", "valid": valid, "positive": positive, "comparisons": comparisons, "threshold": FEEDBACK_DELTA}


def recovery_gate(
    treatment_rows: Sequence[Mapping[str, Any]],
    baselines: Mapping[str, Sequence[Mapping[str, Any]]],
    *,
    resamples: int = 1000,
) -> dict[str, Any]:
    try:
        absolute = {
            "precision": statistics.fmean(float(row["precision"]) for row in treatment_rows),
            "recall": statistics.fmean(float(row["recall"]) for row in treatment_rows),
            "f1": statistics.fmean(float(row["f1"]) for row in treatment_rows),
            "exact": statistics.fmean(float(row["exact"]) for row in treatment_rows),
        }
    except (KeyError, statistics.StatisticsError):
        return {"gate": "recovery", "valid": False, "positive": False, "absolute": {}, "thresholds": {}, "comparisons": {}}
    thresholds = {"precision": RECOVERY_PRECISION, "recall": RECOVERY_RECALL, "f1": RECOVERY_F1, "exact": RECOVERY_EXACT}
    comparisons: dict[str, BootstrapResult] = {}
    try:
        for name, rows in baselines.items():
            stable_seed = int.from_bytes(sha256(name.encode("utf-8")).digest()[:4], "big")
            comparisons[name] = paired_hierarchical_bootstrap(treatment_rows, rows, resamples=resamples, seed=stable_seed)
    except (ValueError, KeyError, statistics.StatisticsError):
        comparisons = {}
    valid = bool(comparisons) and all(result.groups >= 2 for result in comparisons.values())
    positive = valid and all(absolute[key] >= value for key, value in thresholds.items()) and all(
        _positive(result, FEEDBACK_DELTA) for result in comparisons.values()
    )
    return {"gate": "recovery", "valid": valid, "positive": positive, "absolute": absolute, "thresholds": thresholds, "comparisons": comparisons}


def transfer_gate(
    treatment_rows: Sequence[Mapping[str, Any]],
    baselines: Mapping[str, Sequence[Mapping[str, Any]]],
    *,
    test_updates: Mapping[str, int],
    train_digests: Mapping[str, str],
    test_digests: Mapping[str, str],
    resamples: int = 1000,
) -> dict[str, Any]:
    strongest: dict[Any, float] = {}
    for rows in baselines.values():
        for row in rows:
            key = (row.get("seed"), _row_cell(row))
            strongest[key] = max(strongest.get(key, -math.inf), float(row["f1"]))
    cell_effects = {
        key: float(row["f1"]) - strongest[key]
        for row in treatment_rows
        for key in [(row.get("seed"), _row_cell(row))]
        if key in strongest
    }
    baseline_rows = next(iter(baselines.values())) if baselines else ()
    try:
        comparison = paired_hierarchical_bootstrap(treatment_rows, baseline_rows, resamples=resamples, seed=17) if baseline_rows else None
    except (ValueError, KeyError, statistics.StatisticsError):
        comparison = None
    treatment_keys = {(row.get("seed"), _row_cell(row)) for row in treatment_rows}
    frozen_keys_match = set(test_updates) == set(train_digests) == set(test_digests)
    frozen_ok = frozen_keys_match and all(value == 0 for value in test_updates.values()) and all(
        test_digests.get(name) == digest for name, digest in train_digests.items()
    )
    valid = comparison is not None and comparison.groups >= 2 and bool(cell_effects) and set(cell_effects) == treatment_keys
    positive = valid and frozen_ok and _positive(comparison, TRANSFER_DELTA) and all(value >= 0.0 for value in cell_effects.values())
    return {"gate": "transfer", "valid": valid, "positive": positive, "aggregate": comparison, "cell_effects": cell_effects, "frozen_ok": frozen_ok}


def structural_gate(
    ii_rows: Sequence[Mapping[str, Any]],
    is_rows: Sequence[Mapping[str, Any]],
    ss_rows: Sequence[Mapping[str, Any]],
    *,
    resamples: int = 1000,
) -> dict[str, Any]:
    try:
        comparisons = {
            "I_to_S": paired_hierarchical_bootstrap(ii_rows, is_rows, resamples=resamples, seed=19),
            "S_to_S": paired_hierarchical_bootstrap(ii_rows, ss_rows, resamples=resamples, seed=23),
        }
    except (ValueError, KeyError, statistics.StatisticsError):
        comparisons = {}
    valid = bool(comparisons) and all(result.groups >= 2 for result in comparisons.values())
    positive = valid and all(
        _positive(result, STRUCTURAL_DELTA, STRUCTURAL_CI_LOW, inclusive_floor=True)
        for result in comparisons.values()
    )
    return {"gate": "structural", "valid": valid, "positive": positive, "comparisons": comparisons, "threshold": STRUCTURAL_DELTA, "ci_floor": STRUCTURAL_CI_LOW}


def core_conjunction(
    feedback: Mapping[str, Any], recovery: Mapping[str, Any], transfer: Mapping[str, Any]
) -> bool:
    return bool(feedback.get("positive") and recovery.get("positive") and transfer.get("positive"))


__all__ = [
    "ACTION_BUDGET", "V6_BUDGET", "V6_ACTIONS", "TRAINING_PROTOCOL", "MATCHED_SEED_COUNT", "ControllerView",
    "PublicTrainEpisode", "PublicTrainStream", "FrozenTestAccessor", "V6Environment",
    "HiddenMetrics", "evaluator_metrics", "V6LinearQ", "V6Random", "V6Local", "V6VisibleGreedy",
    "TrajectoryStep", "Trajectory", "episode_feedback", "collect_trajectory", "TrainedLane",
    "train_reward_lanes", "evaluate_frozen_lanes", "controller_geometry", "DerangedBatch",
    "derange_controller_views", "BatchRollout", "synchronous_structural_rollout",
    "train_structural_lanes", "evaluate_structural_lanes",
    "paired_hierarchical_bootstrap", "BootstrapResult", "feedback_gate", "recovery_gate", "transfer_gate",
    "structural_gate", "core_conjunction",
]
