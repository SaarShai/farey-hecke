"""V9 development feasibility probe for richer public observability.

This probe measures a fixed-width egocentric view before fitting a learner.  It
reports public-history collisions, a target-independent immediate-reward action
ceiling, and leave-one-out action-value AUC.  A small online learner is run only
when locked observability thresholds pass.  No hidden target metric enters a
view, reward, diagnostic, or update; repair metrics are evaluator-only.
"""

from __future__ import annotations

from copy import deepcopy
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
    )
    from .controller_v6 import (
        V6_ACTIONS,
        V6_BUDGET,
        V6Environment,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        _make_view,
        evaluator_metrics,
    )
    from .controller_v8_dev import (
        ROOT_SEED as V8_ROOT_SEED,
        feedback_gate_v8,
        recovery_gate_v8,
        _environment,
        _make_v6_split,
        verify_manifest_reconstruction,
    )
    from .controller_v4 import ControllerView
    from .repair_experiment import RepairTask
    from .strict_environment import _gap_bin, _ratio_bin
except ImportError:  # direct execution from this directory
    from competency_v6_final_manifest import (  # type: ignore[no-redef]
        DEFAULT_CONFIG,
        PATTERNS,
        SPLIT_REPLICATES,
        TRAIN_ORDERS,
        VALIDATION_ORDERS,
    )
    from controller_v6 import (  # type: ignore[no-redef]
        V6_ACTIONS,
        V6_BUDGET,
        V6Environment,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        _make_view,
        evaluator_metrics,
    )
    from controller_v8_dev import (  # type: ignore[no-redef]
        ROOT_SEED as V8_ROOT_SEED,
        feedback_gate_v8,
        recovery_gate_v8,
        _environment,
        _make_v6_split,
        verify_manifest_reconstruction,
    )
    from controller_v4 import ControllerView  # type: ignore[no-redef]
    from repair_experiment import RepairTask  # type: ignore[no-redef]
    from strict_environment import _gap_bin, _ratio_bin  # type: ignore[no-redef]


ROOT_SEED = V8_ROOT_SEED ^ 0x9A17
ACTION_COUNT = len(V6_ACTIONS)
ACTION_BUDGET = V6_BUDGET
HISTORY_LENGTH = 4
OBSERVABILITY_AUC_MIN = 0.60
OBSERVABILITY_CEILING_MIN = 0.35
OBSERVABILITY_COLLISION_MAX = 0.90
BOOTSTRAP_RESAMPLES = 1000
FEEDBACK_MODES = ("true", "causal_lagged_null", "zero")
RECEIPT_NAME = "controller_v9_feasibility_receipt.json"
RESULTS_NAME = "V9_FEASIBILITY_RESULTS.md"
CLAIM_BOUNDARY = (
    "Development-only observability feasibility probe.  No sealed test was "
    "opened and no V9 competency claim is authorized by this receipt."
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


def _reward_bin(value: float) -> int:
    return max(-8, min(8, int(round(float(value) * 1000.0))))


@dataclass(frozen=True, slots=True)
class RichView:
    """Fixed-width quantized egocentric view (no exact geometry or labels)."""

    gap_bins: tuple[int, ...]
    ratio_bins: tuple[int, ...]
    cursor_relation_bin: int
    remaining_budget_fraction: float
    action_history: tuple[int, ...]
    reward_history: tuple[int, ...]
    trusted_goal: int

    def __post_init__(self) -> None:
        if len(self.gap_bins) != 8 or any(type(v) is not int or not 0 <= v <= 15 for v in self.gap_bins):
            raise ValueError("RichView needs eight gap bins in [0,15]")
        if len(self.ratio_bins) != 4 or any(type(v) is not int or not 0 <= v <= 15 for v in self.ratio_bins):
            raise ValueError("RichView needs four ratio bins in [0,15]")
        if type(self.cursor_relation_bin) is not int or not -8 <= self.cursor_relation_bin <= 8:
            raise ValueError("RichView relation must be in [-8,8]")
        if type(self.remaining_budget_fraction) is not float or not 0.0 <= self.remaining_budget_fraction <= 1.0:
            raise ValueError("RichView budget must be a float in [0,1]")
        if len(self.action_history) != HISTORY_LENGTH or any(type(v) is not int or not 0 <= v <= ACTION_COUNT for v in self.action_history):
            raise ValueError("RichView action history has fixed bounded width")
        if len(self.reward_history) != HISTORY_LENGTH or any(type(v) is not int or not -8 <= v <= 8 for v in self.reward_history):
            raise ValueError("RichView reward history has fixed bounded width")
        if type(self.trusted_goal) is not int or self.trusted_goal not in (0, 1):
            raise ValueError("RichView trusted goal must be 0 or 1")

    def as_tuple(self) -> tuple[object, ...]:
        return (
            *self.gap_bins,
            *self.ratio_bins,
            self.cursor_relation_bin,
            self.remaining_budget_fraction,
            *self.action_history,
            *self.reward_history,
            self.trusted_goal,
        )

    def features(self) -> tuple[float, ...]:
        return (
            1.0,
            *(value / 15.0 for value in self.gap_bins),
            *(value / 15.0 for value in self.ratio_bins),
            self.cursor_relation_bin / 8.0,
            self.remaining_budget_fraction,
            *(value / ACTION_COUNT for value in self.action_history),
            *(value / 8.0 for value in self.reward_history),
            float(self.trusted_goal),
        )


def _rich_view(
    environment: V6Environment,
    action_history: Sequence[int] = (),
    reward_history: Sequence[int] = (),
) -> RichView:
    points, cursor = environment._points, environment._cursor
    left_gaps = tuple(
        (points[(cursor - distance + 1) % len(points)] - points[(cursor - distance) % len(points)]) % 1
        for distance in range(4, 0, -1)
    )
    right_gaps = tuple(
        (points[(cursor + distance) % len(points)] - points[(cursor + distance - 1) % len(points)]) % 1
        for distance in range(1, 5)
    )
    gap_bins = tuple(_gap_bin(value) for value in (*left_gaps, *right_gaps))
    ratio_bins = tuple(_ratio_bin(left_gaps[-1 - index], right_gaps[index]) for index in range(4))
    left_total, right_total = sum(left_gaps), sum(right_gaps)
    total = left_total + right_total
    relation = int(round(float((right_total - left_total) / total) * 8.0)) if total else 0
    relation = max(-8, min(8, relation))
    actions = tuple(max(0, min(ACTION_COUNT, int(value))) for value in action_history[-HISTORY_LENGTH:])
    rewards = tuple(max(-8, min(8, int(value))) for value in reward_history[-HISTORY_LENGTH:])
    return RichView(
        gap_bins,
        ratio_bins,
        relation,
        float(round(environment._remaining / ACTION_BUDGET, 6)),
        (0,) * (HISTORY_LENGTH - len(actions)) + actions,
        (0,) * (HISTORY_LENGTH - len(rewards)) + rewards,
        int(environment._goal.value == "spectral"),
    )


@dataclass(frozen=True, slots=True)
class PublicSample:
    view_key: tuple[object, ...]
    action_values: tuple[float, ...]
    chosen_action: int


def _counterfactual_values(environment: V6Environment) -> tuple[float, ...]:
    values: list[float] = []
    for action in V6_ACTIONS:
        clone = deepcopy(environment)
        values.append(float(clone.step(action)))
    return tuple(values)


def collect_public_samples(tasks: Sequence[RepairTask]) -> tuple[PublicSample, ...]:
    samples: list[PublicSample] = []
    for task_index, task in enumerate(tasks):
        environment = _environment(task)
        action_history: list[int] = []
        reward_history: list[int] = []
        for step_index in range(ACTION_BUDGET):
            view = _rich_view(environment, action_history, reward_history)
            values = _counterfactual_values(environment)
            chosen = (ROOT_SEED + task_index * ACTION_BUDGET + step_index) % ACTION_COUNT
            action = V6_ACTIONS[chosen]
            reward = float(environment.step(action))
            action_history.append(chosen + 1)
            reward_history.append(_reward_bin(reward))
            samples.append(PublicSample(view.as_tuple(), values, chosen))
    return tuple(samples)


def public_history_diagnostic(tasks: Sequence[RepairTask]) -> dict[str, Any]:
    samples = collect_public_samples(tasks)
    if not samples:
        raise ValueError("observability diagnostic needs public samples")
    by_view: dict[tuple[object, ...], list[PublicSample]] = {}
    for sample in samples:
        by_view.setdefault(sample.view_key, []).append(sample)
    collision_count = sum(len(group) - 1 for group in by_view.values())
    ceiling_values: list[float] = []
    pair_total = 0
    pair_correct = 0.0
    global_action_means = [statistics.fmean(sample.action_values[action] for sample in samples) for action in range(ACTION_COUNT)]
    for group in by_view.values():
        best_actions = [max(range(ACTION_COUNT), key=lambda action: sample.action_values[action]) for sample in group]
        counts = {action: best_actions.count(action) for action in set(best_actions)}
        ceiling_values.append(max(counts.values()) / len(group))
        for index, sample in enumerate(group):
            peers = group[:index] + group[index + 1 :]
            if peers:
                scores = [statistics.fmean(peer.action_values[action] for peer in peers) for action in range(ACTION_COUNT)]
            else:
                scores = global_action_means
            for left in range(ACTION_COUNT):
                for right in range(left + 1, ACTION_COUNT):
                    value_delta = sample.action_values[left] - sample.action_values[right]
                    if abs(value_delta) <= 1e-12:
                        continue
                    score_delta = scores[left] - scores[right]
                    pair_total += 1
                    pair_correct += 1.0 if score_delta * value_delta > 0 else 0.5 if abs(score_delta) <= 1e-12 else 0.0
    unique_views = len(by_view)
    total = len(samples)
    collision_rate = collision_count / total
    action_ceiling = statistics.fmean(ceiling_values)
    action_auc = pair_correct / pair_total if pair_total else 0.5
    feasible = (
        action_ceiling >= OBSERVABILITY_CEILING_MIN
        and action_auc >= OBSERVABILITY_AUC_MIN
        and collision_rate <= OBSERVABILITY_COLLISION_MAX
    )
    return {
        "sample_count": total,
        "unique_view_count": unique_views,
        "collision_count": collision_count,
        "collision_rate": collision_rate,
        "public_history_action_ceiling": action_ceiling,
        "action_value_auc": action_auc,
        "action_value_pair_count": pair_total,
        "thresholds": {
            "ceiling_min": OBSERVABILITY_CEILING_MIN,
            "auc_min": OBSERVABILITY_AUC_MIN,
            "collision_max": OBSERVABILITY_COLLISION_MAX,
        },
        "feasible": feasible,
        "method": "leave-one-out view-conditioned immediate metric-delta ordering; no target labels",
    }


class RichLinearQ:
    def __init__(self, seed: int = 0, *, learning: bool = True) -> None:
        del seed
        sample = RichView((0,) * 8, (0,) * 4, 0, 1.0, (0,) * 4, (0,) * 4, 0)
        self._weights = [[0.0] * len(sample.features()) for _ in V6_ACTIONS]
        self.learning = learning
        self.gamma = 0.90
        self.alpha = 0.08
        self.updates = 0

    def choose(self, view: RichView, *, epsilon: float = 0.0, action_seed: int = 0) -> str:
        rng = random.Random(action_seed)
        if epsilon and rng.random() < epsilon:
            return rng.choice(V6_ACTIONS)
        values = [sum(weight * feature for weight, feature in zip(row, view.features())) for row in self._weights]
        best = max(values)
        return V6_ACTIONS[next(index for index, value in enumerate(values) if value == best)]

    def update(self, view: RichView, action: str, reward: float, next_view: RichView, done: bool) -> None:
        if not self.learning:
            return
        index = V6_ACTIONS.index(action)
        features = view.features()
        prediction = sum(weight * feature for weight, feature in zip(self._weights[index], features))
        bootstrap = 0.0 if done else self.gamma * max(
            sum(weight * feature for weight, feature in zip(row, next_view.features())) for row in self._weights
        )
        error = float(reward) + bootstrap - prediction
        for position, feature in enumerate(features):
            self._weights[index][position] += self.alpha * error * feature
        self.updates += 1

    def freeze(self) -> None:
        self.learning = False

    def digest(self) -> str:
        return _digest(self._weights)


def _reward_channel(mode: str, previous: float, raw: float) -> float:
    if mode == "true":
        return raw
    if mode == "zero":
        return 0.0
    if mode == "causal_lagged_null":
        return previous
    raise ValueError(f"unsupported V9 reward mode: {mode}")


def _train_lane(tasks: Sequence[RepairTask], mode: str, seed: int) -> RichLinearQ:
    learner = RichLinearQ(seed)
    for task_index, task in enumerate(tasks):
        environment = _environment(task)
        action_history: list[int] = []
        reward_history: list[int] = []
        previous = 0.0
        for step_index in range(ACTION_BUDGET):
            view = _rich_view(environment, action_history, reward_history)
            action_seed = ROOT_SEED ^ seed ^ (task_index * 0x45D9F3B) ^ step_index
            epsilon = 0.25 - 0.20 * step_index / max(1, ACTION_BUDGET - 1)
            action = learner.choose(view, epsilon=epsilon, action_seed=action_seed)
            raw = float(environment.step(action))
            transmitted = _reward_channel(mode, previous, raw)
            action_history.append(V6_ACTIONS.index(action) + 1)
            reward_history.append(_reward_bin(transmitted))
            next_view = _rich_view(environment, action_history, reward_history)
            learner.update(view, action, transmitted, next_view, environment._done)
            previous = transmitted
    learner.freeze()
    return learner


def _evaluate(policy: Any, task: RepairTask) -> dict[str, float | int]:
    environment = _environment(task)
    action_history: list[int] = []
    reward_history: list[int] = []
    previous = 0.0
    for _ in range(ACTION_BUDGET):
        view = _rich_view(environment, action_history, reward_history)
        if isinstance(policy, RichLinearQ):
            action = policy.choose(view)
        else:
            legacy = ControllerView(
                view.gap_bins[2:6],
                view.ratio_bins[:2],
                view.cursor_relation_bin,
                view.remaining_budget_fraction,
                float(view.reward_history[-1]) / 1000.0,
                view.trusted_goal,
            )
            action = policy.choose(legacy)
        raw = float(environment.step(action))
        action_history.append(V6_ACTIONS.index(action) + 1)
        reward_history.append(_reward_bin(raw))
        previous = raw
    del previous
    metrics = evaluator_metrics(environment)
    return {"precision": metrics.precision, "recall": metrics.recall, "f1": metrics.f1, "exact": metrics.exact}


def _rows(policy: Any, tasks: Sequence[RepairTask], seed: int, name: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in tasks:
        rows.append({
            "seed": seed,
            "learner_seed": seed,
            "cell": f"N{task.order}:{task.pattern.value}:{task.goal.value}",
            "N": task.order,
            "family": task.pattern.value,
            "goal": task.goal.value,
            "policy": name,
            **_evaluate(policy, task),
        })
    return rows


def _aggregate(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[tuple[int, str], list[Mapping[str, Any]]] = {}
    for row in rows:
        groups.setdefault((int(row["learner_seed"]), str(row["cell"])), []).append(row)
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
        for (seed, cell), group in sorted(groups.items())
    ]


def _summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, float]:
    return {metric: statistics.fmean(float(row[metric]) for row in rows) if rows else 0.0 for metric in ("precision", "recall", "f1", "exact")}


def _compact(result: Mapping[str, Any]) -> dict[str, Any]:
    variants = result.get("validation_variants", {})
    task_rows = variants.get("online", {}).get("task_rows", {})
    compact = {key: value for key, value in result.items() if key not in {"validation_task_rows", "validation_variants"}}
    compact["validation_variants"] = {
        "online": {
            "aggregated_rows": variants.get("online", {}).get("aggregated_rows", {}),
            "summaries": result.get("validation_summary", {}),
        }
    }
    compact["omitted_task_rows"] = {
        "validation": {
            name: {"count": len(rows), "sha256": _digest(rows)} for name, rows in sorted(task_rows.items())
        },
        "note": "Task-level rows omitted; per-policy count and canonical digest retained.",
    }
    compact["protocol"] = {**dict(result["protocol"]), "receipt_format": "compact aggregate-only; task rows omitted"}
    return compact


def _source_hashes(directory: Path) -> dict[str, str]:
    names = ("controller_v9_feasibility.py", "controller_v8_dev.py", "controller_v6.py", "repair_experiment.py", "strict_environment.py")
    return {name: sha256((directory / name).read_bytes()).hexdigest() for name in names}


def run_probe(
    *,
    train_tasks: Sequence[RepairTask],
    validation_tasks: Sequence[RepairTask],
    learner_seeds: Sequence[int] = tuple(range(12)),
    output_dir: Path | None = None,
    manifest_hashes: Mapping[str, str] | None = None,
    manifest_commitments: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if output_dir is not None and ((output_dir / RECEIPT_NAME).exists() or (output_dir / RESULTS_NAME).exists()):
        raise RuntimeError("V9 feasibility receipt already exists; refusing to overwrite")
    diagnostics = public_history_diagnostic(train_tasks)
    result: dict[str, Any] = {
        "protocol": {
            "kind": "V9 observability feasibility probe",
            "action_count": ACTION_COUNT,
            "action_budget": ACTION_BUDGET,
            "view_width": len(RichView((0,) * 8, (0,) * 4, 0, 1.0, (0,) * 4, (0,) * 4, 0).as_tuple()),
            "history_length": HISTORY_LENGTH,
            "feature_scope": "8 gap bins + 4 ratio bins + relation + budget + 4 action/reward history bins + trusted goal",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "manifest_hashes": dict(manifest_hashes or {}),
        "manifest_commitments": dict(manifest_commitments or {}),
        "counts": {"train_tasks": len(train_tasks), "validation_tasks": len(validation_tasks)},
        "costs": {"test_openings": 0, "test_updates": 0},
        "observability": diagnostics,
        "source_hashes": _source_hashes(Path(__file__).resolve().parent),
    }
    if not diagnostics["feasible"]:
        result.update({
            "learner": {"ran": False, "reason": "locked observability stop gate", "seed_count": 0},
            "gates": {"status": "unverified", "reason": "learner not run after observability failure"},
            "status": "unverified",
        })
    else:
        lanes: dict[str, dict[int, RichLinearQ]] = {
            mode: {int(seed): _train_lane(train_tasks, mode, int(seed)) for seed in learner_seeds}
            for mode in FEEDBACK_MODES
        }
        task_rows: dict[str, list[dict[str, Any]]] = {mode: [] for mode in FEEDBACK_MODES}
        for seed in learner_seeds:
            seed = int(seed)
            for mode in FEEDBACK_MODES:
                task_rows[mode].extend(_rows(lanes[mode][seed], validation_tasks, seed, mode))
        baseline_rows = {name: [] for name in ("random", "local", "visible_greedy")}
        for seed in learner_seeds:
            seed = int(seed)
            policies = {"random": V6Random(ROOT_SEED ^ seed), "local": V6Local(), "visible_greedy": V6VisibleGreedy()}
            for name, policy in policies.items():
                baseline_rows[name].extend(_rows(policy, validation_tasks, seed, name))
        task_rows.update(baseline_rows)
        aggregated = {name: _aggregate(rows) for name, rows in task_rows.items()}
        feedback = feedback_gate_v8(aggregated["true"], aggregated["causal_lagged_null"], aggregated["zero"])
        recovery = recovery_gate_v8(
            aggregated["true"],
            {name: aggregated[name] for name in ("random", "local", "visible_greedy")},
        )
        gates = {"feedback": feedback, "recovery": recovery, "core": bool(feedback["positive"] and recovery["positive"])}
        result.update({
            "learner": {
                "ran": True,
                "seed_count": len(tuple(learner_seeds)),
                "updates_per_lane": len(train_tasks) * ACTION_BUDGET,
                "frozen": True,
                "lane_digests": {mode: {str(seed): lanes[mode][int(seed)].digest() for seed in learner_seeds} for mode in FEEDBACK_MODES},
            },
            "counts": {**result["counts"], "logical_validation_cells": len({row["cell"] for row in aggregated["true"]}), "validation_seed_cell_aggregates": len(aggregated["true"])},
            "costs": {**result["costs"], "train_updates_per_lane": len(train_tasks) * ACTION_BUDGET, "validation_actions_per_policy": len(validation_tasks) * ACTION_BUDGET},
            "validation_summary": {name: _summary(rows) for name, rows in aggregated.items()},
            "validation_aggregated_rows": aggregated,
            "validation_variants": {"online": {"aggregated_rows": aggregated, "task_rows": task_rows}},
            "gates": gates,
            "status": "positive" if gates["core"] else "negative" if feedback["valid"] and recovery["valid"] else "unverified",
        })
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / RECEIPT_NAME).write_text(json.dumps(_jsonable(_compact(result)), indent=2, sort_keys=True) + "\n")
        (output_dir / RESULTS_NAME).write_text(result_markdown(result))
    return result


def result_markdown(result: Mapping[str, Any]) -> str:
    diagnostics = result["observability"]
    lines = [
        "# V9 observability feasibility probe",
        "",
        str(result["protocol"]["claim_boundary"]),
        "",
        f"View width: `{result['protocol']['view_width']}`; samples: `{diagnostics['sample_count']}`; unique views: `{diagnostics['unique_view_count']}`.",
        "",
        "| diagnostic | value | threshold |",
        "| --- | ---: | ---: |",
        f"| collision rate | {diagnostics['collision_rate']:.4f} | ≤ {diagnostics['thresholds']['collision_max']:.2f} |",
        f"| public-history action ceiling | {diagnostics['public_history_action_ceiling']:.4f} | ≥ {diagnostics['thresholds']['ceiling_min']:.2f} |",
        f"| target-independent action-value AUC | {diagnostics['action_value_auc']:.4f} | ≥ {diagnostics['thresholds']['auc_min']:.2f} |",
        f"| observability stop gate | `{diagnostics['feasible']}` | locked |",
        "",
    ]
    learner = result["learner"]
    lines.append(f"Learner ran: `{learner['ran']}`; status: `{result['status']}`.")
    if learner["ran"]:
        for name, summary in sorted(result["validation_summary"].items()):
            lines.append(f"- {name}: F1={summary['f1']:.4f}, exact={summary['exact']:.4f}")
        lines.extend([
            "",
            f"Feedback gate: `{result['gates']['feedback']['status']}`; recovery gate: `{result['gates']['recovery']['status']}`; core: `{result['gates']['core']}`.",
        ])
    else:
        lines.append("No learner was fit after the locked observability stop gate.")
    lines.extend(["", str(result["protocol"]["claim_boundary"]), ""])
    return "\n".join(lines)


def run_from_v6_manifest(*, output_dir: Path | None = None) -> dict[str, Any]:
    directory = Path(__file__).resolve().parent
    train_tasks, validation_tasks = _make_v6_split("train"), _make_v6_split("validation")
    manifest_receipt = json.loads((directory / "competency_v6_final_manifest_receipt.json").read_text(encoding="utf-8"))
    commitments = verify_manifest_reconstruction(train_tasks, validation_tasks, manifest_receipt)
    return run_probe(
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
