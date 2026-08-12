"""V8 development-only online learner probe over the frozen V6 shell.

The learner chooses every training action online, receives a target-independent
scalar metric delta, and updates immediately.  True, causal lagged-null, and
zero-reward lanes use identical task/episode/action seeds and budgets.  No
sealed accessor is imported here; hidden repair metrics are computed only after
each frozen validation rollout by the evaluator.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from hashlib import sha256
import json
from pathlib import Path
import random
import statistics
from typing import Any, Mapping, Sequence

try:
    from .competency_v6_final_manifest import (
        DEFAULT_CONFIG,
        PATTERNS,
        SPLIT_REPLICATES,
        TRAIN_ORDERS,
        VALIDATION_ORDERS,
        _split_seed,
    )
    from .controller_v4 import ControllerView
    from .controller_v6 import (
        MATCHED_SEED_COUNT,
        V6_ACTIONS,
        V6_BUDGET,
        V6Environment,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        _make_view,
        derange_controller_views,
        evaluator_metrics,
    )
    from .repair_experiment import RepairTask, make_manifest
    from .strict_environment import StrictEnvironment
except ImportError:  # direct execution from this directory
    from competency_v6_final_manifest import (  # type: ignore[no-redef]
        DEFAULT_CONFIG,
        PATTERNS,
        SPLIT_REPLICATES,
        TRAIN_ORDERS,
        VALIDATION_ORDERS,
        _split_seed,
    )
    from controller_v4 import ControllerView  # type: ignore[no-redef]
    from controller_v6 import (  # type: ignore[no-redef]
        MATCHED_SEED_COUNT,
        V6_ACTIONS,
        V6_BUDGET,
        V6Environment,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        _make_view,
        derange_controller_views,
        evaluator_metrics,
    )
    from repair_experiment import RepairTask, make_manifest  # type: ignore[no-redef]
    from strict_environment import StrictEnvironment  # type: ignore[no-redef]


ROOT_SEED = 20260811
LEARNER_SEEDS = tuple(range(MATCHED_SEED_COUNT))
BOOTSTRAP_RESAMPLES = 1000
FEEDBACK_MODES = ("true", "causal_lagged_null", "zero")
ACTION_COUNT = len(V6_ACTIONS)
ACTION_BUDGET = V6_BUDGET
ALPHA = 0.08
GAMMA = 0.90
EPSILON_START = 0.30
EPSILON_END = 0.05
TILE_BUCKETS = 64
FEEDBACK_DELTA = 0.05
RECOVERY_PRECISION = 0.75
RECOVERY_RECALL = 0.50
RECOVERY_F1 = 0.50
RECOVERY_EXACT = 0.25
RECEIPT_NAME = "controller_v8_dev_receipt.json"
RESULTS_NAME = "V8_DEV_RESULTS.md"
CLAIM_BOUNDARY = (
    "Development-only online probe.  This is a train/validation result over "
    "the public V6 shell; it is not a sealed test or a V8 claim."
)


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _digest(value: Any) -> str:
    return sha256(json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _environment(task: RepairTask) -> V6Environment:
    strict = StrictEnvironment(
        task.order,
        task.pattern,
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=ACTION_BUDGET,
        goal=task.goal,
    )
    return V6Environment.from_strict(strict)


def _tile_index(values: Sequence[int], salt: int) -> int:
    state = (salt * 0x9E3779B1) & 0xFFFFFFFF
    for value in values:
        state ^= (int(value) + 0x9E3779B9 + ((state << 6) & 0xFFFFFFFF) + (state >> 2)) & 0xFFFFFFFF
        state &= 0xFFFFFFFF
    return state % TILE_BUCKETS


def online_features(view: ControllerView) -> tuple[float, ...]:
    """Locked target-independent base plus five hashed local interactions."""

    gaps = tuple(value // 4 for value in view.local_gap_bins)
    ratios = tuple(value // 4 for value in view.local_ratio_bins)
    relation = (view.cursor_relation_bin + 8) // 4
    phase = max(0, min(3, int((1.0 - view.remaining_budget_fraction) * 4.0)))
    reward_bucket = -1 if view.last_scalar_reward < -1e-9 else 1 if view.last_scalar_reward > 1e-9 else 0
    tiles = (
        _tile_index((*gaps, *ratios, relation), 11),
        _tile_index((view.trusted_goal, phase), 17),
        _tile_index((view.trusted_goal, relation), 23),
        _tile_index((_tile_index((*gaps, *ratios, relation), 11), view.trusted_goal), 31),
        _tile_index((phase, reward_bucket), 47),
    )
    one_hot = [0.0] * TILE_BUCKETS
    for tile in tiles:
        one_hot[tile] = 1.0
    return (*view.features(), *one_hot)


class OnlineTileQ:
    """Deterministic linear Q learner used identically by all feedback lanes."""

    def __init__(self, seed: int = 0, *, learning: bool = True) -> None:
        del seed  # action randomness is supplied by a shared per-step seed
        sample = ControllerView((0, 0, 0, 0), (0, 0), 0, 1.0, 0.0, 0)
        self._weights = [[0.0] * len(online_features(sample)) for _ in V6_ACTIONS]
        self.learning = bool(learning)
        self.gamma = GAMMA
        self.updates = 0

    def choose(self, view: ControllerView, *, epsilon: float = 0.0, action_seed: int = 0) -> str:
        rng = random.Random(int(action_seed))
        if epsilon > 0.0 and rng.random() < epsilon:
            return rng.choice(V6_ACTIONS)
        features = online_features(view)
        values = [sum(weight * feature for weight, feature in zip(row, features)) for row in self._weights]
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
    ) -> None:
        if not self.learning:
            return
        index = V6_ACTIONS.index(action)
        features = online_features(view)
        prediction = sum(weight * feature for weight, feature in zip(self._weights[index], features))
        bootstrap = 0.0
        if next_view is not None and not done:
            next_features = online_features(next_view)
            bootstrap = self.gamma * max(
                sum(weight * feature for weight, feature in zip(row, next_features))
                for row in self._weights
            )
        error = float(reward) + bootstrap - prediction
        for position, feature in enumerate(features):
            self._weights[index][position] += ALPHA * error * feature
        self.updates += 1

    def freeze(self) -> None:
        self.learning = False

    def digest(self) -> str:
        return _digest(self._weights)


@dataclass(frozen=True, slots=True)
class OnlineStep:
    action: str
    raw_reward: float
    transmitted_reward: float


@dataclass(frozen=True, slots=True)
class OnlineLane:
    mode: str
    controller: OnlineTileQ
    before_digest: str
    after_digest: str
    before_updates: int
    after_updates: int
    update_delta: int
    task_count: int
    episode_seed_digest: str
    action_seed_digest: str
    action_schedule_digest: str
    raw_reward_digest: str
    transmitted_reward_digest: str
    transmitted_nonzero_count: int


class _RewardChannel:
    """Target-independent online reward transform.

    The null lane is a causal one-step lag: it transmits the previous observed
    metric delta, with a fixed zero at the first action.  This is an
    online-safe temporal null; no future reward is exposed before its action
    commits.  The historical lane name is retained for matched gate reports.
    """

    def __init__(self, mode: str) -> None:
        if mode not in FEEDBACK_MODES:
            raise ValueError(f"unsupported feedback mode: {mode}")
        self.mode = mode
        self.pending = 0.0

    def transmit(self, raw_reward: float) -> float:
        if self.mode == "true":
            transmitted = float(raw_reward)
        elif self.mode == "zero":
            transmitted = 0.0
        else:
            transmitted = float(self.pending)
            self.pending = float(raw_reward)
        if self.mode != "causal_lagged_null":
            self.pending = float(raw_reward)
        return transmitted


def _epsilon(step_index: int) -> float:
    fraction = step_index / max(1, ACTION_BUDGET - 1)
    return EPSILON_START + (EPSILON_END - EPSILON_START) * fraction


def _train_episode(
    controller: OnlineTileQ,
    environment: V6Environment,
    *,
    mode: str,
    action_seed: int,
) -> tuple[tuple[OnlineStep, ...], tuple[int, ...]]:
    previous = 0.0
    channel = _RewardChannel(mode)
    steps: list[OnlineStep] = []
    seeds: list[int] = []
    for step_index in range(ACTION_BUDGET):
        view = _make_view(environment, previous)
        step_seed = int(action_seed) ^ (step_index * 0x9E3779B1)
        action = controller.choose(view, epsilon=_epsilon(step_index), action_seed=step_seed)
        raw_reward = environment.step(action)
        transmitted = channel.transmit(raw_reward)
        next_view = _make_view(environment, transmitted)
        controller.update(view, action, transmitted, next_view=next_view, done=environment._done)
        steps.append(OnlineStep(action, float(raw_reward), float(transmitted)))
        seeds.append(step_seed)
        previous = float(transmitted)
    return tuple(steps), tuple(seeds)


def train_online_lane(
    tasks: Sequence[RepairTask],
    *,
    mode: str,
    learner_seed: int,
    behavior_seed: int,
) -> OnlineLane:
    if not tasks:
        raise ValueError("online training requires non-empty tasks")
    controller = OnlineTileQ(learner_seed)
    before_digest, before_updates = controller.digest(), controller.updates
    all_steps: list[OnlineStep] = []
    all_episode_seeds: list[int] = []
    all_seeds: list[int] = []
    for task_index, task in enumerate(tasks):
        episode_seed = int(behavior_seed) ^ (int(learner_seed) * 0x45D9F3B) ^ (task_index * 0x9E3779B1)
        steps, seeds = _train_episode(
            controller,
            _environment(task),
            mode=mode,
            action_seed=episode_seed,
        )
        all_episode_seeds.append(episode_seed)
        all_steps.extend(steps)
        all_seeds.extend(seeds)
    after_digest, after_updates = controller.digest(), controller.updates
    controller.freeze()
    transmitted = tuple(step.transmitted_reward for step in all_steps)
    return OnlineLane(
        mode,
        controller,
        before_digest,
        after_digest,
        before_updates,
        after_updates,
        after_updates - before_updates,
        len(tasks),
        _digest(all_episode_seeds),
        _digest(all_seeds),
        _digest(tuple(step.action for step in all_steps)),
        _digest(tuple(step.raw_reward for step in all_steps)),
        _digest(transmitted),
        sum(abs(value) > 1e-12 for value in transmitted),
    )


def train_matched_lanes(
    tasks: Sequence[RepairTask], *, learner_seed: int, behavior_seed: int
) -> dict[str, OnlineLane]:
    lanes = {
        mode: train_online_lane(tasks, mode=mode, learner_seed=learner_seed, behavior_seed=behavior_seed)
        for mode in FEEDBACK_MODES
    }
    if len({lane.update_delta for lane in lanes.values()}) != 1:
        raise AssertionError("matched online lanes have unequal update counts")
    if lanes["true"].action_seed_digest != lanes["causal_lagged_null"].action_seed_digest:
        raise AssertionError("matched lanes did not share action seeds")
    if (
        lanes["true"].transmitted_nonzero_count > 0
        and lanes["true"].transmitted_reward_digest == lanes["causal_lagged_null"].transmitted_reward_digest
    ):
        raise AssertionError("causal reward permutation was not distinct")
    if lanes["true"].transmitted_nonzero_count > 0 and len({lane.after_digest for lane in lanes.values()}) == 1:
        raise AssertionError("all online reward lanes have the same post-training digest")
    return lanes


def _evaluate_policy(policy: Any, task: RepairTask) -> dict[str, float | int]:
    environment = _environment(task)
    previous = 0.0
    action_digest: list[str] = []
    for _ in range(ACTION_BUDGET):
        view = _make_view(environment, previous)
        action = policy.choose(view)
        if action not in V6_ACTIONS:
            raise AssertionError("policy selected an unknown action")
        action_digest.append(action)
        previous = float(environment.step(action))
    metrics = evaluator_metrics(environment)
    return {
        "precision": metrics.precision,
        "recall": metrics.recall,
        "f1": metrics.f1,
        "exact": metrics.exact,
        "action_count": ACTION_BUDGET,
        "actions_sha256": _digest(action_digest),
    }


def _task_id(task: RepairTask) -> str:
    return sha256(
        repr((task.order, task.pattern.value, task.goal.value, task.seed, task.damage_count)).encode()
    ).hexdigest()[:20]


def _rows_for_policy(policy: Any, tasks: Sequence[RepairTask], *, learner_seed: int, name: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in tasks:
        cell = f"N{task.order}:{task.pattern.value}:{task.goal.value}"
        rows.append({
            "task_id": _task_id(task),
            "seed": int(learner_seed),
            "learner_seed": int(learner_seed),
            "N": task.order,
            "family": task.pattern.value,
            "goal": task.goal.value,
            "cell": cell,
            "policy": name,
            **_evaluate_policy(policy, task),
        })
    return rows


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, str], list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((int(row["learner_seed"]), str(row["cell"])), []).append(row)
    output: list[dict[str, Any]] = []
    for (seed, cell), group in sorted(grouped.items()):
        first = group[0]
        output.append({
            "seed": seed,
            "learner_seed": seed,
            "cell": cell,
            "N": int(first["N"]),
            "family": str(first["family"]),
            "goal": str(first["goal"]),
            "task_count": len(group),
            **{metric: statistics.fmean(float(row[metric]) for row in group) for metric in ("precision", "recall", "f1", "exact")},
        })
    return output


def _summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    return {
        metric: statistics.fmean(float(row[metric]) for row in rows) if rows else 0.0
        for metric in ("precision", "recall", "f1", "exact")
    }


def _status(gate: Mapping[str, Any]) -> str:
    if gate.get("positive"):
        return "positive"
    if gate.get("valid"):
        return "negative"
    return "unverified"


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    effect: float
    ci_low: float
    ci_high: float
    groups: int
    pairs: int


def paired_hierarchical_bootstrap(
    treatment: Sequence[Mapping[str, Any]],
    control: Sequence[Mapping[str, Any]],
    *,
    metric: str = "f1",
    resamples: int = BOOTSTRAP_RESAMPLES,
    seed: int = 0,
) -> BootstrapResult:
    """Two-stage paired bootstrap: groups and then cells within groups.

    Group identities are learner seeds; cells are the N/family/goal rows.
    Both levels are sampled with replacement, unlike the historical V6 helper
    whose outer loop iterated each observed group exactly once.
    """

    def key(row: Mapping[str, Any]) -> tuple[Any, Any]:
        cell = row.get("cell")
        if cell is None:
            cell = (row.get("N", row.get("n")), row.get("family"), row.get("goal"))
        return row.get("learner_seed", row.get("seed")), cell

    treatment_map = {key(row): float(row[metric]) for row in treatment}
    control_map = {key(row): float(row[metric]) for row in control}
    if not treatment_map or treatment_map.keys() != control_map.keys():
        raise ValueError("paired bootstrap requires identical group/cell keys")
    by_group: dict[Any, list[float]] = {}
    for group_cell, value in treatment_map.items():
        by_group.setdefault(group_cell[0], []).append(value - control_map[group_cell])
    group_values = tuple(by_group.values())
    group_means = tuple(statistics.fmean(values) for values in group_values)
    effect = statistics.fmean(group_means)
    rng = random.Random(seed)
    samples: list[float] = []
    for _ in range(max(1, int(resamples))):
        # First resample learner-seed groups with replacement.
        sampled_groups = [rng.choice(group_values) for _ in group_values]
        # Then resample cells within each selected group with replacement.
        sampled_means = [statistics.fmean(rng.choice(values) for _ in values) for values in sampled_groups]
        samples.append(statistics.fmean(sampled_means))
    samples.sort()
    low = samples[max(0, int(0.025 * len(samples)))]
    high = samples[min(len(samples) - 1, int(0.975 * len(samples)))]
    return BootstrapResult(effect, low, high, len(group_values), len(treatment_map))


def _positive(result: BootstrapResult, threshold: float) -> bool:
    return result.effect >= threshold and result.ci_low > 0.0


def feedback_gate_v8(
    true_rows: Sequence[Mapping[str, Any]],
    null_rows: Sequence[Mapping[str, Any]],
    zero_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    comparisons: dict[str, BootstrapResult] = {}
    try:
        comparisons = {
            "causal_lagged_null": paired_hierarchical_bootstrap(true_rows, null_rows, seed=11),
            "zero": paired_hierarchical_bootstrap(true_rows, zero_rows, seed=13),
        }
    except (ValueError, KeyError, statistics.StatisticsError):
        comparisons = {}
    valid = bool(comparisons) and all(item.groups >= 2 for item in comparisons.values())
    positive = valid and all(_positive(item, FEEDBACK_DELTA) for item in comparisons.values())
    return {
        "gate": "feedback",
        "status": "positive" if positive else "negative" if valid else "unverified",
        "valid": valid,
        "positive": positive,
        "comparisons": comparisons,
        "threshold": FEEDBACK_DELTA,
    }


def recovery_gate_v8(
    treatment_rows: Sequence[Mapping[str, Any]],
    baselines: Mapping[str, Sequence[Mapping[str, Any]]],
) -> dict[str, Any]:
    try:
        absolute = {
            metric: statistics.fmean(float(row[metric]) for row in treatment_rows)
            for metric in ("precision", "recall", "f1", "exact")
        }
    except (KeyError, statistics.StatisticsError):
        return {"gate": "recovery", "status": "unverified", "valid": False, "positive": False, "absolute": {}, "thresholds": {}, "comparisons": {}}
    thresholds = {
        "precision": RECOVERY_PRECISION,
        "recall": RECOVERY_RECALL,
        "f1": RECOVERY_F1,
        "exact": RECOVERY_EXACT,
    }
    comparisons: dict[str, BootstrapResult] = {}
    try:
        for name, rows in baselines.items():
            stable_seed = int.from_bytes(sha256(name.encode("utf-8")).digest()[:4], "big")
            comparisons[name] = paired_hierarchical_bootstrap(treatment_rows, rows, seed=stable_seed)
    except (ValueError, KeyError, statistics.StatisticsError):
        comparisons = {}
    valid = bool(comparisons) and all(item.groups >= 2 for item in comparisons.values())
    positive = valid and all(absolute[key] >= value for key, value in thresholds.items()) and all(
        _positive(item, FEEDBACK_DELTA) for item in comparisons.values()
    )
    return {
        "gate": "recovery",
        "status": "positive" if positive else "negative" if valid else "unverified",
        "valid": valid,
        "positive": positive,
        "absolute": absolute,
        "thresholds": thresholds,
        "comparisons": comparisons,
    }


def _gate_report(rows: Mapping[str, Sequence[Mapping[str, Any]]]) -> dict[str, Any]:
    feedback = feedback_gate_v8(rows["true"], rows["causal_lagged_null"], rows["zero"])
    baselines = {name: rows[name] for name in ("random", "local", "visible_greedy")}
    recovery = recovery_gate_v8(rows["true"], baselines)
    return {
        "feedback": feedback,
        "recovery": recovery,
        "core": bool(feedback.get("positive") and recovery.get("positive")),
    }


def derangement_diagnostic(tasks: Sequence[RepairTask]) -> dict[str, Any]:
    """Check G-only derangement leaves U, reachability, and physics unchanged."""

    if len(tasks) < 2:
        raise ValueError("G-only diagnostic needs two tasks")
    identity_envs = [_environment(task) for task in tasks[:2]]
    scrambled_envs = [_environment(task) for task in tasks[:2]]
    no_fixed_points = True
    geometry_multisets = True
    own_u_preserved = True
    physical_states_equal = True
    rewards_equal = True
    reachability_preserved = True
    geometry_changed = 0
    geometry_positions = 0
    source_rows: list[tuple[int, ...]] = []
    for step_index in range(ACTION_BUDGET):
        identity = tuple(_make_view(environment, 0.0) for environment in identity_envs)
        batch = derange_controller_views(identity, seed=ROOT_SEED + step_index)
        source_rows.append(batch.source_indices)
        no_fixed_points &= all(index != source for index, source in enumerate(batch.source_indices))
        geometry_multisets &= sorted(
            tuple((*view.local_gap_bins, *view.local_ratio_bins, view.cursor_relation_bin) for view in identity)
        ) == sorted(
            tuple((*view.local_gap_bins, *view.local_ratio_bins, view.cursor_relation_bin) for view in batch.views)
        )
        geometry_changed += sum(
            tuple((*identity[index].local_gap_bins, *identity[index].local_ratio_bins, identity[index].cursor_relation_bin))
            != tuple((*batch.views[index].local_gap_bins, *batch.views[index].local_ratio_bins, batch.views[index].cursor_relation_bin))
            for index in range(len(identity))
        )
        geometry_positions += len(identity)
        own_u_preserved &= all(
            (view.remaining_budget_fraction, view.last_scalar_reward, view.trusted_goal)
            == (identity[index].remaining_budget_fraction, identity[index].last_scalar_reward, identity[index].trusted_goal)
            for index, view in enumerate(batch.views)
        )
        actions = tuple(V6_ACTIONS[(ROOT_SEED + step_index + index) % ACTION_COUNT] for index in range(2))
        for identity_environment, scrambled_environment, action in zip(identity_envs, scrambled_envs, actions):
            if action not in V6_ACTIONS:
                reachability_preserved = False
            left = identity_environment.step(action)
            right = scrambled_environment.step(action)
            rewards_equal &= left == right
        physical_states_equal &= all(
            (left._points, left._cursor, left._remaining, left._done)
            == (right._points, right._cursor, right._remaining, right._done)
            for left, right in zip(identity_envs, scrambled_envs)
        )
    return {
        "replicas": 2,
        "steps": ACTION_BUDGET,
        "source_indices": source_rows,
        "no_fixed_points": no_fixed_points,
        "geometry_multiset_equal": geometry_multisets,
        "effective_geometry_change_rate": geometry_changed / geometry_positions if geometry_positions else 0.0,
        "intervention_effective": bool(geometry_changed),
        "own_u_preserved": own_u_preserved,
        "physical_states_equal": physical_states_equal,
        "rewards_equal": rewards_equal,
        "action_reachability_preserved": reachability_preserved,
        "valid": all((no_fixed_points, geometry_multisets, bool(geometry_changed), own_u_preserved, physical_states_equal, rewards_equal, reachability_preserved)),
        "arms": {
            "I→I": "identity G to identity policy (descriptive diagnostic only)",
            "I→S": "identity G to scrambled policy (not run in this probe)",
            "S→I": "scrambled G to identity policy (not run in this probe)",
            "S→S": "scrambled G to scrambled policy (not run in this probe)",
        },
        "role": "descriptive reachability/serialization diagnostic; not a competency gate",
    }


def compact_result(result: Mapping[str, Any]) -> dict[str, Any]:
    variants = result.get("validation_variants", {})
    task_rows = result.get("validation_task_rows")
    if task_rows is None:
        task_rows = variants.get("online", {}).get("task_rows", {})
    compact = {
        key: value
        for key, value in result.items()
        if key not in {"validation_task_rows", "validation_variants", "validation_aggregated_rows"}
    }
    compact["protocol"] = {
        **dict(result["protocol"]),
        "receipt_format": "compact aggregate-only; per-task rows omitted",
    }
    compact["validation_aggregated_rows"] = result.get("validation_aggregated_rows", variants.get("online", {}).get("aggregated_rows", {}))
    compact["validation_variants"] = {
        "online": {
            "aggregated_rows": variants.get("online", {}).get("aggregated_rows", {}),
            "summaries": result.get("validation_summary", {}),
        }
    }
    omitted = {
        str(name): {"count": len(rows), "sha256": _digest(rows), "sha256_scope": "task_rows"}
        for name, rows in sorted(task_rows.items())
    }
    if not omitted:
        aggregate_rows = result.get("validation_aggregated_rows", {})
        omitted = {
            str(name): {
                "count": sum(int(row.get("task_count", 0)) for row in rows),
                "sha256": _digest(rows),
                "sha256_scope": "aggregate_rows_fallback",
            }
            for name, rows in sorted(aggregate_rows.items())
        }
    compact["omitted_task_rows"] = {
        "validation": omitted,
        "note": "Per-task validation rows are omitted; counts and canonical digests bind the compact receipt.",
    }
    return compact


def _source_hashes(directory: Path) -> dict[str, str]:
    names = (
        "controller_v8_dev.py",
        "controller_v6.py",
        "competency_v6_final_manifest.py",
        "competency_v5_feasibility.py",
        "repair_experiment.py",
        "strict_environment.py",
    )
    return {name: sha256((directory / name).read_bytes()).hexdigest() for name in names}


def _task_commitment(tasks: Sequence[RepairTask]) -> str:
    payload = [
        {
            "index": index,
            "order": task.order,
            "pattern": task.pattern.value,
            "goal": task.goal.value,
            "seed": task.seed,
            "damage_count": task.damage_count,
        }
        for index, task in enumerate(tasks)
    ]
    return _digest(payload)


def _make_v6_split(split: str) -> list[RepairTask]:
    if split not in {"train", "validation"}:
        raise ValueError("V8 reconstruction is limited to train and validation splits")
    orders = TRAIN_ORDERS if split == "train" else VALIDATION_ORDERS
    return make_manifest(
        orders,
        PATTERNS,
        damage_count=2,
        replicates=SPLIT_REPLICATES[split],
        seed=_split_seed(split, DEFAULT_CONFIG),
    )


def verify_manifest_reconstruction(
    train_tasks: Sequence[RepairTask],
    validation_tasks: Sequence[RepairTask],
    manifest_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Bind regenerated public split rows to the committed V6 configuration."""

    seal = manifest_receipt["manifest_seal"]
    config = seal["config"]
    split_tasks = {"train": tuple(train_tasks), "validation": tuple(validation_tasks)}
    commitments: dict[str, dict[str, Any]] = {}
    for split, tasks in split_tasks.items():
        expected_orders = tuple(config["split_orders"][split])
        expected_count = (
            len(expected_orders)
            * len(config["patterns"])
            * len(config["goals"])
            * int(config["split_replicates"][split])
        )
        if len(tasks) != expected_count or {task.order for task in tasks} != set(expected_orders):
            raise AssertionError(f"{split} reconstruction does not match committed manifest configuration")
        regenerated = _make_v6_split(split)
        commitment = _task_commitment(tasks)
        regenerated_commitment = _task_commitment(regenerated)
        if commitment != regenerated_commitment:
            raise AssertionError(f"{split} reconstruction is not deterministic")
        cells = sorted({task.cell for task in tasks})
        commitments[split] = {
            "count": len(tasks),
            "cell_count": len(cells),
            "sha256": commitment,
            "regenerated_sha256": regenerated_commitment,
            "deterministic": True,
        }
    return {
        "verified": True,
        "generator_sha256": str(manifest_receipt["generator_sha256"]),
        "config_sha256": _digest(config),
        "splits": commitments,
    }


def run_dev(
    *,
    train_tasks: Sequence[RepairTask],
    validation_tasks: Sequence[RepairTask],
    learner_seeds: Sequence[int] = LEARNER_SEEDS,
    output_dir: Path | None = None,
    manifest_hashes: Mapping[str, str] | None = None,
    manifest_commitments: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if not train_tasks or not validation_tasks:
        raise ValueError("V8 dev probe needs non-empty train and validation tasks")
    if output_dir is not None:
        if (output_dir / RECEIPT_NAME).exists() or (output_dir / RESULTS_NAME).exists():
            raise RuntimeError("V8 dev receipt already exists; refusing to overwrite")
    behavior_seed = ROOT_SEED
    lanes: dict[str, dict[int, OnlineLane]] = {mode: {} for mode in FEEDBACK_MODES}
    for learner_seed in learner_seeds:
        lanes_by_mode = train_matched_lanes(
            train_tasks,
            learner_seed=int(learner_seed),
            behavior_seed=behavior_seed,
        )
        for mode, lane in lanes_by_mode.items():
            lanes[mode][int(learner_seed)] = lane
    true_rewards = [
        lane.transmitted_nonzero_count
        for lane in (lanes["true"][int(seed)] for seed in learner_seeds)
    ]
    if not any(true_rewards):
        raise AssertionError("training stream produced no nonzero visible rewards")
    task_rows: dict[str, list[dict[str, Any]]] = {mode: [] for mode in FEEDBACK_MODES}
    baseline_rows: dict[str, list[dict[str, Any]]] = {name: [] for name in ("random", "local", "visible_greedy")}
    for learner_seed in learner_seeds:
        seed = int(learner_seed)
        for mode in FEEDBACK_MODES:
            task_rows[mode].extend(_rows_for_policy(lanes[mode][seed].controller, validation_tasks, learner_seed=seed, name=mode))
        baselines = {
            "random": V6Random(ROOT_SEED ^ seed),
            "local": V6Local(),
            "visible_greedy": V6VisibleGreedy(),
        }
        for name, policy in baselines.items():
            baseline_rows[name].extend(_rows_for_policy(policy, validation_tasks, learner_seed=seed, name=name))
    task_rows.update(baseline_rows)
    aggregated = {name: aggregate_rows(rows) for name, rows in task_rows.items()}
    gates = _gate_report(aggregated)
    summaries = {name: _summary(rows) for name, rows in aggregated.items()}
    expected_updates = len(train_tasks) * ACTION_BUDGET
    lane_receipt = {
        mode: {
            str(seed): {
                "updates": lane.after_updates,
                "expected_updates": expected_updates,
                "update_delta": lane.update_delta,
                "frozen": not lane.controller.learning,
                "before_digest": lane.before_digest,
                "after_digest": lane.after_digest,
                "episode_seed_digest": lane.episode_seed_digest,
                "action_seed_digest": lane.action_seed_digest,
                "action_schedule_digest": lane.action_schedule_digest,
                "raw_reward_digest": lane.raw_reward_digest,
                "transmitted_reward_digest": lane.transmitted_reward_digest,
                "transmitted_nonzero_count": lane.transmitted_nonzero_count,
            }
            for seed, lane in by_seed.items()
        }
        for mode, by_seed in lanes.items()
    }
    result = {
        "protocol": {
            "kind": "V8 development-only online learner probe",
            "learner_seeds": [int(seed) for seed in learner_seeds],
            "action_count": ACTION_COUNT,
            "action_budget": ACTION_BUDGET,
            "training": "online exploratory action/update loop",
            "epsilon": {"start": EPSILON_START, "end": EPSILON_END},
            "alpha": ALPHA,
            "gamma": GAMMA,
            "features": "V6 public view plus five fixed hashed local interaction tiles",
            "reward_null": "causal one-step lagged-null; previous observed reward only",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "manifest_hashes": dict(manifest_hashes or {}),
        "manifest_commitments": dict(manifest_commitments or {}),
        "counts": {
            "train_tasks": len(train_tasks),
            "validation_tasks": len(validation_tasks),
            "logical_validation_cells": len({str(row["cell"]) for row in aggregated["true"]}),
            "validation_seed_cell_aggregates": len(aggregated["true"]),
        },
        "costs": {
            "train_updates_per_lane": expected_updates,
            "validation_actions_per_policy": len(validation_tasks) * ACTION_BUDGET,
            "test_openings": 0,
            "test_updates": 0,
        },
        "lanes": lane_receipt,
        "validation_summary": summaries,
        "validation_aggregated_rows": aggregated,
        "validation_variants": {"online": {"aggregated_rows": aggregated, "summaries": summaries, "task_rows": task_rows}},
        "gates": gates,
        "derangement": derangement_diagnostic(train_tasks),
        "source_hashes": _source_hashes(Path(__file__).resolve().parent),
        "status": "positive" if gates["core"] else "negative" if all(gates[name]["status"] != "unverified" for name in ("feedback", "recovery")) else "unverified",
    }
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        compact = compact_result(result)
        (output_dir / RECEIPT_NAME).write_text(json.dumps(_jsonable(compact), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (output_dir / RESULTS_NAME).write_text(result_markdown(result), encoding="utf-8")
    return result


def result_markdown(result: Mapping[str, Any]) -> str:
    gates = result["gates"]
    lines = [
        "# V8 development online learner probe",
        "",
        str(result["protocol"]["claim_boundary"]),
        "",
        f"Learner seeds: `{len(result['protocol']['learner_seeds'])}`; action budget: `{result['protocol']['action_budget']}`; test openings: `0`.",
        "",
        "| gate | status | positive |",
        "| --- | --- | --- |",
        f"| feedback true vs lagged-null/zero | `{gates['feedback']['status']}` | `{gates['feedback']['positive']}` |",
        f"| online recovery vs baselines | `{gates['recovery']['status']}` | `{gates['recovery']['positive']}` |",
        f"| core | `{'positive' if gates['core'] else 'negative'}` | `{gates['core']}` |",
        "",
        "## Validation summaries",
        "",
        "| policy | precision | recall | F1 | exact |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, summary in sorted(result["validation_summary"].items()):
        lines.append(f"| {name} | {summary['precision']:.4f} | {summary['recall']:.4f} | {summary['f1']:.4f} | {summary['exact']:.4f} |")
    diagnostic = result["derangement"]
    lines.extend([
        "",
        "## G-only derangement diagnostic",
        "",
        f"valid=`{diagnostic['valid']}`; effective_geometry_change_rate=`{diagnostic['effective_geometry_change_rate']:.3f}`; no_fixed_points=`{diagnostic['no_fixed_points']}`; geometry_multiset_equal=`{diagnostic['geometry_multiset_equal']}`; own_u_preserved=`{diagnostic['own_u_preserved']}`; physical_states_equal=`{diagnostic['physical_states_equal']}`; rewards_equal=`{diagnostic['rewards_equal']}`.",
        "",
        str(result["protocol"]["claim_boundary"]),
        "",
    ])
    return "\n".join(lines)


def run_from_v6_manifest(*, output_dir: Path | None = None) -> dict[str, Any]:
    """Reconstruct only committed V6 train and validation task generators."""

    directory = Path(__file__).resolve().parent
    train_tasks = _make_v6_split("train")
    validation_tasks = _make_v6_split("validation")
    manifest_receipt = json.loads((directory / "competency_v6_final_manifest_receipt.json").read_text(encoding="utf-8"))
    commitments = verify_manifest_reconstruction(train_tasks, validation_tasks, manifest_receipt)
    return run_dev(
        train_tasks=train_tasks,
        validation_tasks=validation_tasks,
        output_dir=output_dir,
        manifest_hashes={
            "public": str(manifest_receipt["manifest_seal"]["public_sha256"]),
            "private": str(manifest_receipt["manifest_seal"]["private_sha256"]),
        },
        manifest_commitments=commitments,
    )


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    run_from_v6_manifest(output_dir=here)
