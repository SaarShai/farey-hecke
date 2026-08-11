"""V7 development-only learner probe.

This module never opens the consumed V6 test accessor.  It compares the
committed V6 one-pass TD replay with a fixed backward Monte-Carlo return-to-go
replay on the same public training trajectories.  The evaluator may compute
hidden identity metrics on validation rows; those labels never enter a view,
reward vector, or learner update.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass, replace
from hashlib import sha256
import json
from pathlib import Path
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
    from .controller_v6 import (
        MATCHED_SEED_COUNT,
        V6_ACTIONS,
        V6_BUDGET,
        ControllerView,
        Trajectory,
        V6Environment,
        V6LinearQ,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        _make_view,
        episode_feedback,
        evaluator_metrics,
        paired_hierarchical_bootstrap,
        collect_trajectory,
        feedback_gate,
        recovery_gate,
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
    from controller_v6 import (  # type: ignore[no-redef]
        MATCHED_SEED_COUNT,
        V6_ACTIONS,
        V6_BUDGET,
        ControllerView,
        Trajectory,
        V6Environment,
        V6LinearQ,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        _make_view,
        episode_feedback,
        evaluator_metrics,
        paired_hierarchical_bootstrap,
        collect_trajectory,
        feedback_gate,
        recovery_gate,
    )
    from repair_experiment import RepairTask, make_manifest  # type: ignore[no-redef]
    from strict_environment import StrictEnvironment  # type: ignore[no-redef]


ROOT_SEED = 20261001
LEARNER_SEEDS = tuple(range(MATCHED_SEED_COUNT))
BOOTSTRAP_RESAMPLES = 1000
TD_KIND = "one_pass_td"
MC_KIND = "backward_return_to_go"
TILE_KIND = "backward_return_to_go_coarse_tiles"
FEEDBACK_MODES = ("true", "within_episode_permuted", "zero")
RECEIPT_NAME = "controller_v7_dev_receipt.json"
RESULTS_NAME = "V7_DEV_RESULTS.md"
CLAIM_BOUNDARY = (
    "Development-only validation probe.  This is offline reward-attribution "
    "replay, not online adaptation, and it does not authorize a V7 sealed run."
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
    payload = json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def _environment(task: RepairTask) -> V6Environment:
    strict = StrictEnvironment(
        task.order,
        task.pattern,
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=V6_BUDGET,
        goal=task.goal,
    )
    return V6Environment.from_strict(strict)


@dataclass(frozen=True, slots=True)
class PublicEpisode:
    """Evaluator-owned task wrapper; only a fresh V6 environment crosses over."""

    task: RepairTask

    def fresh_environment(self) -> V6Environment:
        return _environment(self.task)


class PublicStream:
    def __init__(self, tasks: Sequence[RepairTask]) -> None:
        self._episodes = tuple(PublicEpisode(task) for task in tasks)

    def __iter__(self):
        return iter(self._episodes)


class MonteCarloQ(V6LinearQ):
    """V6 learner shell with one fixed return-to-go target per transition."""

    def update_return(self, view: ControllerView, action: str, target: float, *, alpha: float = 0.10) -> None:
        if not self.learning:
            return
        index = V6_ACTIONS.index(action)
        features = view.features()
        prediction = sum(weight * feature for weight, feature in zip(self._weights[index], features))
        error = float(target) - prediction
        for position, feature in enumerate(features):
            self._weights[index][position] += alpha * error * feature
        self.updates += 1


TILE_BUCKETS = 64


def _tile_index(values: Sequence[int], salt: int) -> int:
    value = int(salt) & 0xFFFFFFFF
    for item in values:
        value = (value * 16777619) ^ (int(item) + 0x9E3779B9)
        value &= 0xFFFFFFFF
    return value % TILE_BUCKETS


def tile_features(view: ControllerView) -> tuple[float, ...]:
    """Fixed coarse interactions; no exact fractions, N, target, or list size."""

    gaps = tuple(value // 4 for value in view.local_gap_bins)
    ratios = tuple(value // 4 for value in view.local_ratio_bins)
    relation = (view.cursor_relation_bin + 8) // 4
    phase = max(0, min(3, int((1.0 - view.remaining_budget_fraction) * 4.0)))
    reward_bucket = -1 if view.last_scalar_reward < -1e-9 else 1 if view.last_scalar_reward > 1e-9 else 0
    geometry = _tile_index((*gaps, *ratios, relation), 11)
    active = {
        _tile_index((view.trusted_goal, phase), 17),
        _tile_index((view.trusted_goal, relation), 23),
        _tile_index((geometry, view.trusted_goal), 31),
        _tile_index((phase, geometry), 47),
        _tile_index((reward_bucket,), 59),
    }
    return (*view.features(), *(1.0 if index in active else 0.0 for index in range(TILE_BUCKETS)))


class TileMonteCarloQ:
    """Small fixed hashed tile table over the public coarse view."""

    def __init__(self, seed: int = 0, *, learning: bool = True, gamma: float = 0.90) -> None:
        del seed  # initialization is intentionally all zero and deterministic
        self._weights = [[0.0] * len(tile_features(ControllerView((0, 0, 0, 0), (0, 0), 0, 1.0, 0.0, 0))) for _ in V6_ACTIONS]
        self.learning = learning
        self.gamma = float(gamma)
        self.updates = 0

    def choose(self, view: ControllerView) -> str:
        features = tile_features(view)
        values = [sum(weight * feature for weight, feature in zip(row, features)) for row in self._weights]
        best = max(values)
        return V6_ACTIONS[next(index for index, value in enumerate(values) if value == best)]

    def update_return(self, view: ControllerView, action: str, target: float, *, alpha: float = 0.10) -> None:
        if not self.learning:
            return
        index = V6_ACTIONS.index(action)
        features = tile_features(view)
        prediction = sum(weight * feature for weight, feature in zip(self._weights[index], features))
        error = float(target) - prediction
        for position, feature in enumerate(features):
            self._weights[index][position] += alpha * error * feature
        self.updates += 1

    def freeze(self) -> None:
        self.learning = False

    def digest(self) -> str:
        return sha256(json.dumps(self._weights, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True, slots=True)
class DevLane:
    kind: str
    mode: str
    learner_seed: int
    controller: Any
    trajectories: tuple[Trajectory, ...]
    before_digest: str
    after_digest: str
    update_delta: int
    transmitted_rewards: tuple[tuple[float, ...], ...]


def _replay_td(controller: V6LinearQ, trajectory: Trajectory, mode: str, seed: int) -> tuple[float, ...]:
    transmitted = episode_feedback(tuple(step.reward for step in trajectory.steps), mode, seed)
    previous = 0.0
    for step, reward in zip(trajectory.steps, transmitted):
        view = replace(step.view, last_scalar_reward=previous)
        next_view = replace(step.next_view, last_scalar_reward=reward)
        controller.update(view, step.action, reward, next_view=next_view, done=step.done)
        previous = reward
    return transmitted


def _replay_mc(controller: MonteCarloQ, trajectory: Trajectory, mode: str, seed: int) -> tuple[float, ...]:
    """Replay a trajectory backward for targets, then update in causal order."""

    transmitted = episode_feedback(tuple(step.reward for step in trajectory.steps), mode, seed)
    returns = [0.0] * len(transmitted)
    running = 0.0
    for index in range(len(transmitted) - 1, -1, -1):
        running = float(transmitted[index]) + controller.gamma * running
        returns[index] = running
    previous = 0.0
    for step, target, reward in zip(trajectory.steps, returns, transmitted):
        view = replace(step.view, last_scalar_reward=previous)
        controller.update_return(view, step.action, target)
        previous = reward
    return transmitted


def _trajectories(tasks: Sequence[RepairTask], *, seed: int) -> tuple[Trajectory, ...]:
    return tuple(
        collect_trajectory(PublicEpisode(task).fresh_environment(), seed=seed + index * V6_BUDGET)
        for index, task in enumerate(tasks)
    )


def train_lane(
    kind: str,
    mode: str,
    tasks: Sequence[RepairTask],
    *,
    learner_seed: int,
    behavior_seed: int,
    trajectories: Sequence[Trajectory] | None = None,
) -> DevLane:
    if kind not in {TD_KIND, MC_KIND, TILE_KIND} or mode not in FEEDBACK_MODES:
        raise ValueError("unsupported V7 dev lane")
    if trajectories is None:
        trajectories = _trajectories(tasks, seed=behavior_seed)
    trajectories = tuple(trajectories)
    controller: Any = (
        V6LinearQ(learner_seed)
        if kind == TD_KIND
        else MonteCarloQ(learner_seed)
        if kind == MC_KIND
        else TileMonteCarloQ(learner_seed)
    )
    before = controller.digest()
    transmitted: list[tuple[float, ...]] = []
    for index, trajectory in enumerate(trajectories):
        replay = _replay_td if kind == TD_KIND else _replay_mc
        transmitted.append(replay(controller, trajectory, mode, behavior_seed ^ index))  # type: ignore[arg-type]
    after = controller.digest()
    controller.freeze()
    return DevLane(
        kind, mode, learner_seed, controller, trajectories, before, after,
        controller.updates, tuple(transmitted),
    )


def _task_id(task: RepairTask) -> str:
    return "dev-" + _digest((task.order, task.pattern.value, task.goal.value, task.seed))[:20]


def _evaluate_one(policy: Any, task: RepairTask) -> dict[str, Any]:
    environment = _environment(task)
    feedback = 0.0
    reward_sum = 0.0
    actions: list[str] = []
    for _ in range(V6_BUDGET):
        action = policy.choose(_make_view(environment, feedback))
        actions.append(action)
        feedback = environment.step(action)
        reward_sum += feedback
    hidden = evaluator_metrics(environment)
    return {
        "precision": hidden.precision,
        "recall": hidden.recall,
        "f1": hidden.f1,
        "exact": hidden.exact,
        "visible_reward_sum": float(reward_sum),
        "action_count": len(actions),
        "actions_sha256": _digest(actions),
    }


def rows_for_policy(policy: Any, tasks: Sequence[RepairTask], *, learner_seed: int, name: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in tasks:
        cell = f"N{task.order}:{task.pattern.value}:{task.goal.value}"
        rows.append({
            "task_id": _task_id(task),
            "seed": learner_seed,
            "learner_seed": learner_seed,
            "N": task.order,
            "family": task.pattern.value,
            "goal": task.goal.value,
            "cell": cell,
            "policy": name,
            **_evaluate_one(policy, task),
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
    return {metric: statistics.fmean(float(row[metric]) for row in rows) if rows else 0.0 for metric in ("precision", "recall", "f1", "exact")}


def _status(gate: Mapping[str, Any]) -> str:
    if gate.get("positive"):
        return "positive"
    if gate.get("valid"):
        return "negative"
    return "unverified"


def _gate_report(rows_by_policy: Mapping[str, Sequence[Mapping[str, Any]]]) -> dict[str, Any]:
    feedback = feedback_gate(rows_by_policy["true"], rows_by_policy["within_episode_permuted"], rows_by_policy["zero"], resamples=BOOTSTRAP_RESAMPLES)
    recovery = recovery_gate(
        rows_by_policy["true"],
        {name: rows_by_policy[name] for name in ("random", "local", "visible_greedy")},
        resamples=BOOTSTRAP_RESAMPLES,
    )
    return {
        "feedback": {"status": _status(feedback), **feedback},
        "recovery": {"status": _status(recovery), **recovery},
        "core": bool(feedback.get("positive") and recovery.get("positive")),
    }


def _source_hashes(directory: Path) -> dict[str, str]:
    names = ("controller_v7_dev.py", "controller_v6.py", "competency_v6_final_manifest.py", "strict_environment.py", "competency_v5_feasibility.py")
    return {name: sha256((directory / name).read_bytes()).hexdigest() for name in names}


def run_dev(
    *,
    train_tasks: Sequence[RepairTask],
    validation_tasks: Sequence[RepairTask],
    learner_seeds: Sequence[int] = LEARNER_SEEDS,
    output_dir: Path | None = None,
    manifest_hashes: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Run only train/validation; no FinalManifestAccess test method exists here."""

    if not train_tasks or not validation_tasks:
        raise ValueError("V7 dev probe needs non-empty train and validation tasks")
    if output_dir is not None:
        receipt = output_dir / RECEIPT_NAME
        results = output_dir / RESULTS_NAME
        if receipt.exists() or results.exists():
            raise RuntimeError("V7 dev receipt already exists; refusing to overwrite")
    behavior_seed = ROOT_SEED
    lanes: dict[str, dict[int, DevLane]] = {kind: {} for kind in (TD_KIND, MC_KIND, TILE_KIND)}
    trajectory_by_seed = {
        int(seed): _trajectories(train_tasks, seed=behavior_seed + int(seed) * 1009)
        for seed in learner_seeds
    }
    for kind in lanes:
        for seed in learner_seeds:
            lanes[kind][int(seed)] = {
                mode: train_lane(
                    kind,
                    mode,
                    train_tasks,
                    learner_seed=int(seed),
                    behavior_seed=behavior_seed + int(seed) * 1009,
                    trajectories=trajectory_by_seed[int(seed)],
                )
                for mode in FEEDBACK_MODES
            }
    policy_names = (*FEEDBACK_MODES, "random", "local", "visible_greedy")
    task_rows: dict[str, list[dict[str, Any]]] = {name: [] for name in policy_names}
    tile_task_rows: dict[str, list[dict[str, Any]]] = {name: [] for name in policy_names}
    for seed in learner_seeds:
        seed = int(seed)
        for mode, lane in lanes[MC_KIND][seed].items():
            task_rows[mode].extend(rows_for_policy(lane.controller, validation_tasks, learner_seed=seed, name=mode))
        for mode, lane in lanes[TILE_KIND][seed].items():
            tile_task_rows[mode].extend(rows_for_policy(lane.controller, validation_tasks, learner_seed=seed, name=mode))
        baselines = {"random": V6Random(ROOT_SEED ^ seed), "local": V6Local(), "visible_greedy": V6VisibleGreedy()}
        for name, policy in baselines.items():
            baseline_rows = rows_for_policy(policy, validation_tasks, learner_seed=seed, name=name)
            task_rows[name].extend(baseline_rows)
            tile_task_rows[name].extend(baseline_rows)
    rows = {name: aggregate_rows(values) for name, values in task_rows.items()}
    tile_rows = {name: aggregate_rows(values) for name, values in tile_task_rows.items()}
    gates = _gate_report(rows)
    tile_gates = _gate_report(tile_rows)
    summaries = {name: _summary(values) for name, values in rows.items()}
    tile_summaries = {name: _summary(values) for name, values in tile_rows.items()}
    td_summary = {}
    for mode in FEEDBACK_MODES:
        td_rows = []
        for seed in learner_seeds:
            td_rows.extend(rows_for_policy(lanes[TD_KIND][int(seed)][mode].controller, validation_tasks, learner_seed=int(seed), name=mode))
        td_summary[mode] = _summary(aggregate_rows(td_rows))
    expected_updates = len(train_tasks) * V6_BUDGET
    lane_receipt = {
        kind: {
            str(seed): {
                mode: {
                    "updates": lane.update_delta,
                    "expected_updates": expected_updates,
                    "frozen": not lane.controller.learning,
                    "digest": lane.after_digest,
                }
                for mode, lane in modes.items()
            }
            for seed, modes in seed_lanes.items()
        }
        for kind, seed_lanes in lanes.items()
    }
    result = {
        "protocol": {
            "kind": "V7 development-only learner probe",
            "learner_seeds": [int(seed) for seed in learner_seeds],
            "action_count": len(V6_ACTIONS),
            "action_budget": V6_BUDGET,
            "behavior": "fixed cyclic action-covering trajectories",
            "lanes": [TD_KIND, MC_KIND, TILE_KIND, *FEEDBACK_MODES],
            "tile_feature_buckets": TILE_BUCKETS,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "manifest_hashes": dict(manifest_hashes or {}),
        "counts": {"train_tasks": len(train_tasks), "validation_tasks": len(validation_tasks), "validation_cells": len(rows["true"])},
        "costs": {"train_updates_per_lane": expected_updates, "validation_actions_per_policy": len(validation_tasks) * V6_BUDGET, "test_openings": 0, "test_updates": 0},
        "lanes": lane_receipt,
        "td_validation_summary": td_summary,
        "mc_validation_summary": summaries,
        "tile_validation_summary": tile_summaries,
        "validation_aggregated_rows": rows,
        "validation_task_rows": task_rows,
        "validation_variants": {
            "mc": {"aggregated_rows": rows, "task_rows": task_rows, "summaries": summaries},
            "tile": {"aggregated_rows": tile_rows, "task_rows": tile_task_rows, "summaries": tile_summaries},
        },
        "gates": {
            "feedback": gates["feedback"],
            "recovery": gates["recovery"],
            "core": gates["core"],
            "mc": gates,
            "tile": tile_gates,
        },
        "source_hashes": _source_hashes(Path(__file__).resolve().parent),
        "status": "positive" if gates["core"] else "negative" if all(gates[name]["status"] != "unverified" for name in ("feedback", "recovery")) else "unverified",
    }
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / RECEIPT_NAME).write_text(json.dumps(_jsonable(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (output_dir / RESULTS_NAME).write_text(result_markdown(result), encoding="utf-8")
    return result


def result_markdown(result: Mapping[str, Any]) -> str:
    gates = result["gates"]
    tile_gates = gates["tile"]
    lines = [
        "# V7 development learner probe",
        "",
        str(result["protocol"]["claim_boundary"]),
        "",
        f"Learner seeds: `{len(result['protocol']['learner_seeds'])}`; action budget: `{result['protocol']['action_budget']}`; test openings: `0`.",
        "",
        "| gate | status | positive |",
        "| --- | --- | --- |",
        f"| feedback true vs permuted/zero | `{gates['feedback']['status']}` | `{gates['feedback']['positive']}` |",
        f"| MC recovery vs baselines | `{gates['recovery']['status']}` | `{gates['recovery']['positive']}` |",
        f"| tile feedback true vs permuted/zero | `{tile_gates['feedback']['status']}` | `{tile_gates['feedback']['positive']}` |",
        f"| tile recovery vs baselines | `{tile_gates['recovery']['status']}` | `{tile_gates['recovery']['positive']}` |",
        f"| core | `{'positive' if gates['core'] else 'negative'}` | `{gates['core']}` |",
        f"| tile core | `{'positive' if tile_gates['core'] else 'negative'}` | `{tile_gates['core']}` |",
        "",
        "## Validation summaries (Monte-Carlo return-to-go)",
        "",
        "| policy | precision | recall | F1 | exact |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for name, summary in sorted(result["mc_validation_summary"].items()):
        lines.append(f"| {name} | {summary['precision']:.4f} | {summary['recall']:.4f} | {summary['f1']:.4f} | {summary['exact']:.4f} |")
    lines.extend([
        "",
        "## Validation summaries (coarse interaction/tile variant)",
        "",
        "| policy | precision | recall | F1 | exact |",
        "| --- | ---: | ---: | ---: | ---: |",
    ])
    for name, summary in sorted(result["tile_validation_summary"].items()):
        lines.append(f"| {name} | {summary['precision']:.4f} | {summary['recall']:.4f} | {summary['f1']:.4f} | {summary['exact']:.4f} |")
    lines.extend(["", "## Boundary", "", str(result["protocol"]["claim_boundary"]), ""])
    return "\n".join(lines)


def run_from_v6_manifest(*, output_dir: Path | None = None) -> dict[str, Any]:
    """Reconstruct only the sealed V6 train/validation task generators.

    This intentionally does not instantiate :class:`FinalManifestAccess` and
    has no path to ``open_test``.  The committed manifest receipt supplies the
    hashes; task rows remain evaluator-owned and are never serialized.
    """

    directory = Path(__file__).resolve().parent
    train_tasks = make_manifest(
        TRAIN_ORDERS,
        PATTERNS,
        damage_count=2,
        replicates=SPLIT_REPLICATES["train"],
        seed=_split_seed("train", DEFAULT_CONFIG),
    )
    validation_tasks = make_manifest(
        VALIDATION_ORDERS,
        PATTERNS,
        damage_count=2,
        replicates=SPLIT_REPLICATES["validation"],
        seed=_split_seed("validation", DEFAULT_CONFIG),
    )
    manifest_receipt = json.loads((directory / "competency_v6_final_manifest_receipt.json").read_text(encoding="utf-8"))
    return run_dev(
        train_tasks=train_tasks,
        validation_tasks=validation_tasks,
        output_dir=output_dir,
        manifest_hashes={
            "public": str(manifest_receipt["manifest_seal"]["public_sha256"]),
            "private": str(manifest_receipt["manifest_seal"]["private_sha256"]),
        },
    )


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    run_from_v6_manifest(output_dir=here)
