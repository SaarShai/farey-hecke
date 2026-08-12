"""V10 development probe with a predeclared local Farey-defect objective.

This is a structural task objective, not spontaneous discovery: the visible
reward is the change in an adjacent-determinant defect around the cursor.  It
uses only current public points, has no target/N/mask input, and is evaluated
through matched true/causal-lagged-null/zero online lanes before frozen
validation.  No sealed accessor is imported or opened.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, is_dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import statistics
from typing import Any, Mapping, Sequence

try:
    from .controller_v4 import ControllerView
    from .controller_v6 import (
        V6_ACTIONS,
        V6_BUDGET,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        evaluator_metrics,
    )
    from .controller_v8_dev import (
        ROOT_SEED as V8_ROOT_SEED,
        _environment,
        _make_v6_split,
        feedback_gate_v8,
        recovery_gate_v8,
        verify_manifest_reconstruction,
    )
    from .controller_v9_feasibility import (
        RichView,
        _rich_view,
        _reward_bin,
    )
    from .repair_experiment import RepairTask
except ImportError:  # direct execution from this directory
    from controller_v4 import ControllerView  # type: ignore[no-redef]
    from controller_v6 import (  # type: ignore[no-redef]
        V6_ACTIONS,
        V6_BUDGET,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        evaluator_metrics,
    )
    from controller_v8_dev import (  # type: ignore[no-redef]
        ROOT_SEED as V8_ROOT_SEED,
        _environment,
        _make_v6_split,
        feedback_gate_v8,
        recovery_gate_v8,
        verify_manifest_reconstruction,
    )
    from controller_v9_feasibility import RichView, _rich_view, _reward_bin  # type: ignore[no-redef]
    from repair_experiment import RepairTask  # type: ignore[no-redef]


ROOT_SEED = V8_ROOT_SEED ^ 0xA10
ACTION_COUNT = len(V6_ACTIONS)
ACTION_BUDGET = V6_BUDGET
FEEDBACK_MODES = ("true", "causal_lagged_null", "zero")
LOCAL_RADIUS = 2
DEFECT_BIN_SCALE = 4.0
MIN_NONZERO_REWARD_COUNT = 8
MIN_DISTINCT_REWARD_VALUES = 2
MIN_NONZERO_ACTIONS = 2
BOOTSTRAP_RESAMPLES = 1000
RECEIPT_NAME = "controller_v10_dev_receipt.json"
RESULTS_NAME = "V10_DEV_RESULTS.md"
CLAIM_BOUNDARY = (
    "Development-only V10 probe.  This is a preregistered structural local "
    "Farey-defect objective over V6 train/validation; it is not a sealed test "
    "or a spontaneous-discovery claim."
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


def _adjacent_determinant(left: Fraction, right: Fraction) -> int:
    return abs(left.numerator * right.denominator - left.denominator * right.numerator)


def local_farey_defect(environment: Any) -> float:
    """Mean squared adjacent-determinant excess in a fixed cursor window."""

    points, cursor = environment._points, environment._cursor
    pairs = []
    for distance in range(LOCAL_RADIUS, 0, -1):
        pairs.append((cursor - distance, cursor - distance + 1))
    for distance in range(0, LOCAL_RADIUS):
        pairs.append((cursor + distance, cursor + distance + 1))
    defects = []
    for left_index, right_index in pairs:
        left = points[left_index % len(points)]
        right = points[right_index % len(points)]
        excess = max(0, _adjacent_determinant(left, right) - 1)
        defects.append(float(excess * excess))
    return statistics.fmean(defects) if defects else 0.0


def local_defect_bin(defect: float) -> int:
    return max(0, min(15, int(round(float(defect) * DEFECT_BIN_SCALE))))


def local_defect_reward(environment: Any, action: str) -> float:
    before = local_farey_defect(environment)
    branch = deepcopy(environment)
    branch.step(action)
    return float(before - local_farey_defect(branch))


def defect_reward_support(tasks: Sequence[RepairTask]) -> dict[str, Any]:
    rewards: list[float] = []
    by_action: dict[str, int] = {action: 0 for action in V6_ACTIONS}
    by_goal: dict[str, int] = {}
    for task in tasks:
        environment = _environment(task)
        for action in V6_ACTIONS:
            reward = local_defect_reward(environment, action)
            rewards.append(reward)
            if abs(reward) > 1e-12:
                by_action[action] += 1
                by_goal[task.goal.value] = by_goal.get(task.goal.value, 0) + 1
    distinct = sorted({round(value, 12) for value in rewards if abs(value) > 1e-12})
    nonzero = sum(abs(value) > 1e-12 for value in rewards)
    support = {
        "sample_count": len(rewards),
        "nonzero_count": nonzero,
        "positive_count": sum(value > 1e-12 for value in rewards),
        "negative_count": sum(value < -1e-12 for value in rewards),
        "distinct_nonzero_values": len(distinct),
        "nonzero_action_count": sum(value > 0 for value in by_action.values()),
        "by_action": by_action,
        "by_goal": by_goal,
        "thresholds": {
            "min_nonzero_count": MIN_NONZERO_REWARD_COUNT,
            "min_distinct_values": MIN_DISTINCT_REWARD_VALUES,
            "min_nonzero_actions": MIN_NONZERO_ACTIONS,
        },
    }
    support["feasible"] = (
        nonzero >= MIN_NONZERO_REWARD_COUNT
        and len(distinct) >= MIN_DISTINCT_REWARD_VALUES
        and support["nonzero_action_count"] >= MIN_NONZERO_ACTIONS
    )
    return support


class DefectLinearQ:
    def __init__(self, seed: int = 0, *, learning: bool = True) -> None:
        del seed
        sample = RichView((0,) * 8, (0,) * 4, 0, 1.0, (0,) * 4, (0,) * 4, 0)
        width = len(sample.features()) + 1
        self._weights = [[0.0] * width for _ in V6_ACTIONS]
        self.learning = learning
        self.gamma = 0.90
        self.alpha = 0.08
        self.updates = 0

    @staticmethod
    def features(view: RichView, defect_bin: int) -> tuple[float, ...]:
        return (*view.features(), max(0, min(15, int(defect_bin))) / 15.0)

    def choose(self, view: RichView, defect_bin: int, *, epsilon: float = 0.0, action_seed: int = 0) -> str:
        import random

        rng = random.Random(action_seed)
        if epsilon and rng.random() < epsilon:
            return rng.choice(V6_ACTIONS)
        features = self.features(view, defect_bin)
        values = [sum(weight * feature for weight, feature in zip(row, features)) for row in self._weights]
        best = max(values)
        return V6_ACTIONS[next(index for index, value in enumerate(values) if value == best)]

    def update(self, view: RichView, defect_bin: int, action: str, reward: float, next_view: RichView, next_defect_bin: int, done: bool) -> None:
        if not self.learning:
            return
        index = V6_ACTIONS.index(action)
        features = self.features(view, defect_bin)
        prediction = sum(weight * feature for weight, feature in zip(self._weights[index], features))
        next_features = self.features(next_view, next_defect_bin)
        bootstrap = 0.0 if done else self.gamma * max(
            sum(weight * feature for weight, feature in zip(row, next_features)) for row in self._weights
        )
        error = float(reward) + bootstrap - prediction
        for position, feature in enumerate(features):
            self._weights[index][position] += self.alpha * error * feature
        self.updates += 1

    def freeze(self) -> None:
        self.learning = False

    def digest(self) -> str:
        return _digest(self._weights)


@dataclass(frozen=True, slots=True)
class LaneEvidence:
    mode: str
    controller: DefectLinearQ
    updates: int
    digest: str
    raw_reward_digest: str
    transmitted_reward_digest: str
    transmitted_nonzero_count: int


def _transmit(mode: str, previous_raw: float, raw: float) -> float:
    if mode == "true":
        return raw
    if mode == "zero":
        return 0.0
    if mode == "causal_lagged_null":
        return previous_raw
    raise ValueError(f"unsupported feedback mode {mode}")


def train_lane(tasks: Sequence[RepairTask], mode: str, seed: int) -> LaneEvidence:
    learner = DefectLinearQ(seed)
    raw_rewards: list[float] = []
    transmitted_rewards: list[float] = []
    previous_raw = 0.0
    for task_index, task in enumerate(tasks):
        environment = _environment(task)
        action_history: list[int] = []
        reward_history: list[int] = []
        previous_raw = 0.0
        for step_index in range(ACTION_BUDGET):
            view = _rich_view(environment, action_history, reward_history)
            defect_bin = local_defect_bin(local_farey_defect(environment))
            action_seed = ROOT_SEED ^ seed ^ (task_index * 0x45D9F3B) ^ step_index
            epsilon = 0.25 - 0.20 * step_index / max(1, ACTION_BUDGET - 1)
            action = learner.choose(view, defect_bin, epsilon=epsilon, action_seed=action_seed)
            raw = local_defect_reward(environment, action)
            environment.step(action)
            transmitted = _transmit(mode, previous_raw, raw)
            action_history.append(V6_ACTIONS.index(action) + 1)
            reward_history.append(_reward_bin(transmitted))
            next_view = _rich_view(environment, action_history, reward_history)
            next_defect_bin = local_defect_bin(local_farey_defect(environment))
            learner.update(view, defect_bin, action, transmitted, next_view, next_defect_bin, environment._done)
            raw_rewards.append(raw)
            transmitted_rewards.append(transmitted)
            previous_raw = raw
    learner.freeze()
    return LaneEvidence(
        mode,
        learner,
        learner.updates,
        learner.digest(),
        _digest(raw_rewards),
        _digest(transmitted_rewards),
        sum(abs(value) > 1e-12 for value in transmitted_rewards),
    )


def _legacy_view(view: RichView) -> ControllerView:
    return ControllerView(
        view.gap_bins[2:6],
        view.ratio_bins[:2],
        view.cursor_relation_bin,
        view.remaining_budget_fraction,
        float(view.reward_history[-1]) / 1000.0,
        view.trusted_goal,
    )


def evaluate(policy: Any, task: RepairTask) -> dict[str, float]:
    environment = _environment(task)
    action_history: list[int] = []
    reward_history: list[int] = []
    previous_raw = 0.0
    for _ in range(ACTION_BUDGET):
        view = _rich_view(environment, action_history, reward_history)
        defect_bin = local_defect_bin(local_farey_defect(environment))
        if isinstance(policy, DefectLinearQ):
            action = policy.choose(view, defect_bin)
        else:
            action = policy.choose(_legacy_view(view))
        raw = local_defect_reward(environment, action)
        environment.step(action)
        action_history.append(V6_ACTIONS.index(action) + 1)
        reward_history.append(_reward_bin(raw))
        previous_raw = raw
    del previous_raw
    metrics = evaluator_metrics(environment)
    return {"precision": metrics.precision, "recall": metrics.recall, "f1": metrics.f1, "exact": metrics.exact}


def rows(policy: Any, tasks: Sequence[RepairTask], seed: int, name: str) -> list[dict[str, Any]]:
    return [
        {
            "seed": seed,
            "learner_seed": seed,
            "cell": f"N{task.order}:{task.pattern.value}:{task.goal.value}",
            "N": task.order,
            "family": task.pattern.value,
            "goal": task.goal.value,
            "policy": name,
            **evaluate(policy, task),
        }
        for task in tasks
    ]


def aggregate(rows_by_task: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, str], list[Mapping[str, Any]]] = {}
    for row in rows_by_task:
        grouped.setdefault((int(row["learner_seed"]), str(row["cell"])), []).append(row)
    return [
        {
            "seed": seed,
            "learner_seed": seed,
            "cell": cell,
            "N": int(group[0]["N"]),
            "family": str(group[0]["family"]),
            "goal": str(group[0]["goal"]),
            "task_count": len(group),
            **{metric: statistics.fmean(float(row[metric]) for row in group) for metric in ("precision", "recall", "f1", "exact")},
        }
        for (seed, cell), group in sorted(grouped.items())
    ]


def summary(rows_by_cell: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    return {metric: statistics.fmean(float(row[metric]) for row in rows_by_cell) if rows_by_cell else 0.0 for metric in ("precision", "recall", "f1", "exact")}


def compact(result: Mapping[str, Any]) -> dict[str, Any]:
    variants = result.get("validation_variants", {})
    task_rows = variants.get("online", {}).get("task_rows", {})
    output = {key: value for key, value in result.items() if key not in {"validation_task_rows", "validation_variants"}}
    output["validation_variants"] = {
        "online": {
            "aggregated_rows": variants.get("online", {}).get("aggregated_rows", {}),
            "summaries": result.get("validation_summary", {}),
        }
    }
    output["omitted_task_rows"] = {
        "validation": {name: {"count": len(rows), "sha256": _digest(rows)} for name, rows in sorted(task_rows.items())},
        "note": "Task rows omitted; per-policy counts and canonical digests retained.",
    }
    output["protocol"] = {**dict(result["protocol"]), "receipt_format": "compact aggregate-only; task rows omitted"}
    return output


def source_hashes(directory: Path) -> dict[str, str]:
    names = ("controller_v10_dev.py", "controller_v9_feasibility.py", "controller_v8_dev.py", "controller_v6.py", "repair_experiment.py", "strict_environment.py")
    return {name: sha256((directory / name).read_bytes()).hexdigest() for name in names}


def run_dev(
    *,
    train_tasks: Sequence[RepairTask],
    validation_tasks: Sequence[RepairTask],
    learner_seeds: Sequence[int] = tuple(range(12)),
    output_dir: Path | None = None,
    manifest_hashes: Mapping[str, str] | None = None,
    manifest_commitments: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if output_dir is not None and ((output_dir / RECEIPT_NAME).exists() or (output_dir / RESULTS_NAME).exists()):
        raise RuntimeError("V10 receipt already exists; refusing to overwrite")
    support = defect_reward_support(train_tasks)
    result: dict[str, Any] = {
        "protocol": {
            "kind": "V10 development-only local Farey-defect probe",
            "action_count": ACTION_COUNT,
            "action_budget": ACTION_BUDGET,
            "objective": "structural local adjacent-determinant defect reduction around cursor",
            "reward": "defect_before - defect_after, visible points only",
            "view": "V9 fixed coarse view plus quantized local-defect feature",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "manifest_hashes": dict(manifest_hashes or {}),
        "manifest_commitments": dict(manifest_commitments or {}),
        "counts": {"train_tasks": len(train_tasks), "validation_tasks": len(validation_tasks)},
        "costs": {"test_openings": 0, "test_updates": 0},
        "support": support,
        "source_hashes": source_hashes(Path(__file__).resolve().parent),
    }
    if not support["feasible"]:
        result.update({
            "learner": {"ran": False, "reason": "locked local-defect support stop gate", "seed_count": 0},
            "gates": {"status": "unverified", "reason": "learner not run after support failure"},
            "status": "unverified",
        })
    else:
        lanes = {mode: {int(seed): train_lane(train_tasks, mode, int(seed)) for seed in learner_seeds} for mode in FEEDBACK_MODES}
        task_rows: dict[str, list[dict[str, Any]]] = {mode: [] for mode in FEEDBACK_MODES}
        for seed in learner_seeds:
            seed = int(seed)
            for mode in FEEDBACK_MODES:
                task_rows[mode].extend(rows(lanes[mode][seed].controller, validation_tasks, seed, mode))
        baseline_rows = {name: [] for name in ("random", "local", "visible_greedy")}
        for seed in learner_seeds:
            seed = int(seed)
            policies = {"random": V6Random(ROOT_SEED ^ seed), "local": V6Local(), "visible_greedy": V6VisibleGreedy()}
            for name, policy in policies.items():
                baseline_rows[name].extend(rows(policy, validation_tasks, seed, name))
        task_rows.update(baseline_rows)
        aggregated = {name: aggregate(values) for name, values in task_rows.items()}
        feedback = feedback_gate_v8(aggregated["true"], aggregated["causal_lagged_null"], aggregated["zero"])
        recovery = recovery_gate_v8(aggregated["true"], {name: aggregated[name] for name in ("random", "local", "visible_greedy")})
        gates = {"feedback": feedback, "recovery": recovery, "core": bool(feedback["positive"] and recovery["positive"])}
        result.update({
            "learner": {
                "ran": True,
                "seed_count": len(tuple(learner_seeds)),
                "updates_per_lane": len(train_tasks) * ACTION_BUDGET,
                "frozen": True,
                "lane_evidence": {
                    mode: {
                        str(seed): {
                            "updates": lanes[mode][int(seed)].updates,
                            "digest": lanes[mode][int(seed)].digest,
                            "raw_reward_digest": lanes[mode][int(seed)].raw_reward_digest,
                            "transmitted_reward_digest": lanes[mode][int(seed)].transmitted_reward_digest,
                            "transmitted_nonzero_count": lanes[mode][int(seed)].transmitted_nonzero_count,
                        }
                        for seed in learner_seeds
                    }
                    for mode in FEEDBACK_MODES
                },
            },
            "counts": {**result["counts"], "logical_validation_cells": len({row["cell"] for row in aggregated["true"]}), "validation_seed_cell_aggregates": len(aggregated["true"])},
            "costs": {**result["costs"], "train_updates_per_lane": len(train_tasks) * ACTION_BUDGET, "validation_actions_per_policy": len(validation_tasks) * ACTION_BUDGET},
            "validation_summary": {name: summary(values) for name, values in aggregated.items()},
            "validation_aggregated_rows": aggregated,
            "validation_variants": {"online": {"aggregated_rows": aggregated, "task_rows": task_rows}},
            "gates": gates,
            "status": "positive" if gates["core"] else "negative" if feedback["valid"] and recovery["valid"] else "unverified",
        })
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / RECEIPT_NAME).write_text(json.dumps(_jsonable(compact(result)), indent=2, sort_keys=True) + "\n")
        (output_dir / RESULTS_NAME).write_text(result_markdown(result))
    return result


def result_markdown(result: Mapping[str, Any]) -> str:
    support = result["support"]
    lines = [
        "# V10 local Farey-defect development probe",
        "",
        str(result["protocol"]["claim_boundary"]),
        "",
        "| support diagnostic | value |",
        "| --- | ---: |",
        f"| samples | {support['sample_count']} |",
        f"| nonzero rewards | {support['nonzero_count']} |",
        f"| positive / negative | {support['positive_count']} / {support['negative_count']} |",
        f"| distinct nonzero values | {support['distinct_nonzero_values']} |",
        f"| nonzero action count | {support['nonzero_action_count']} |",
        f"| locked support gate | `{support['feasible']}` |",
        "",
        f"Learner ran: `{result['learner']['ran']}`; status: `{result['status']}`.",
    ]
    if result["learner"]["ran"]:
        for name, summary_value in sorted(result["validation_summary"].items()):
            lines.append(f"- {name}: F1={summary_value['f1']:.4f}, exact={summary_value['exact']:.4f}")
        lines.append(f"Feedback gate: `{result['gates']['feedback']['status']}`; recovery gate: `{result['gates']['recovery']['status']}`; core: `{result['gates']['core']}`.")
    else:
        lines.append("No learner was fit after the locked local-defect support gate.")
    lines.extend(["", str(result["protocol"]["claim_boundary"]), ""])
    return "\n".join(lines)


def run_from_v6_manifest(*, output_dir: Path | None = None) -> dict[str, Any]:
    directory = Path(__file__).resolve().parent
    train_tasks, validation_tasks = _make_v6_split("train"), _make_v6_split("validation")
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
    run_from_v6_manifest(output_dir=Path(__file__).resolve().parent)
