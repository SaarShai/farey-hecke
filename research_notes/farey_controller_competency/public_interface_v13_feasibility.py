"""V13 public-interface feasibility probe.

This module measures whether fixed-width, target-independent public signals
align with evaluator-only one-step hidden repair value.  It does not train a
controller and never opens a sealed accessor.  Exact points are used only
inside evaluator-side counterfactuals; the serialized public view contains
quantized local bins, bounded history, budget fraction, and trusted goal.
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from dataclasses import asdict, dataclass, is_dataclass
from hashlib import sha256
import json
from pathlib import Path
import statistics
from typing import Any, Mapping, Sequence

try:
    from .controller_v6 import V6_ACTIONS, V6_BUDGET, evaluator_metrics
    from .controller_v8_dev import _environment, _make_v6_split, verify_manifest_reconstruction
    from .controller_v9_feasibility import _rich_view, _reward_bin
    from .repair_experiment import RepairTask
    from .strict_environment import _coverage, _spectral
except ImportError:  # direct execution from this directory
    from controller_v6 import V6_ACTIONS, V6_BUDGET, evaluator_metrics  # type: ignore[no-redef]
    from controller_v8_dev import _environment, _make_v6_split, verify_manifest_reconstruction  # type: ignore[no-redef]
    from controller_v9_feasibility import _rich_view, _reward_bin  # type: ignore[no-redef]
    from repair_experiment import RepairTask  # type: ignore[no-redef]
    from strict_environment import _coverage, _spectral  # type: ignore[no-redef]


ROOT_SEED = 20260811 ^ 0x13F
ACTION_COUNT = len(V6_ACTIONS)
ACTION_BUDGET = V6_BUDGET
HISTORY_LENGTH = 4
SIGNALS = ("coverage_gain", "spectral_gain", "defect_reduction", "active_search")
MIN_HIDDEN_POSITIVE_ACTIONS = 8
MIN_ALIGNMENT_PAIRS = 100
MIN_ALIGNMENT_AUC = 0.60
RECEIPT_NAME = "public_interface_v13_feasibility_receipt.json"
RESULTS_NAME = "V13_PUBLIC_INTERFACE_FEASIBILITY_RESULTS.md"
CLAIM_BOUNDARY = (
    "Development-only public-interface feasibility probe. Hidden action values "
    "are evaluator diagnostics only; no sealed test or competency claim is "
    "authorized."
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


@dataclass(frozen=True, slots=True)
class PublicView:
    """Fixed-width controller-facing view; no exact geometry or labels."""

    gap_bins: tuple[int, ...]
    ratio_bins: tuple[int, ...]
    cursor_relation_bin: int
    remaining_budget_fraction: float
    action_history: tuple[int, ...]
    reward_history: tuple[int, ...]
    trusted_goal_bin: int

    def __post_init__(self) -> None:
        if len(self.gap_bins) != 8 or any(type(v) is not int or not 0 <= v <= 15 for v in self.gap_bins):
            raise ValueError("public gap bins must be fixed eight integers in [0,15]")
        if len(self.ratio_bins) != 4 or any(type(v) is not int or not 0 <= v <= 15 for v in self.ratio_bins):
            raise ValueError("public ratio bins must be fixed four integers in [0,15]")
        if type(self.cursor_relation_bin) is not int or not -8 <= self.cursor_relation_bin <= 8:
            raise ValueError("public cursor relation must be in [-8,8]")
        if type(self.remaining_budget_fraction) is not float or not 0.0 <= self.remaining_budget_fraction <= 1.0:
            raise ValueError("public budget must be a float fraction")
        if len(self.action_history) != HISTORY_LENGTH or any(type(v) is not int or not 0 <= v <= ACTION_COUNT for v in self.action_history):
            raise ValueError("public action history has fixed bounded width")
        if len(self.reward_history) != HISTORY_LENGTH or any(type(v) is not int or not -8 <= v <= 8 for v in self.reward_history):
            raise ValueError("public reward history has fixed bounded width")
        if type(self.trusted_goal_bin) is not int or self.trusted_goal_bin not in (0, 1):
            raise ValueError("public trusted goal bin must be 0 or 1")

    def as_tuple(self) -> tuple[object, ...]:
        return (*self.gap_bins, *self.ratio_bins, self.cursor_relation_bin,
                self.remaining_budget_fraction, *self.action_history,
                *self.reward_history, self.trusted_goal_bin)

    def serialize(self) -> dict[str, Any]:
        return {
            "gap_bins": self.gap_bins,
            "ratio_bins": self.ratio_bins,
            "cursor_relation_bin": self.cursor_relation_bin,
            "remaining_budget_fraction": self.remaining_budget_fraction,
            "action_history": self.action_history,
            "reward_history": self.reward_history,
            "trusted_goal_bin": self.trusted_goal_bin,
        }


def public_view(environment: Any, action_history: Sequence[int] = (), reward_history: Sequence[int] = ()) -> PublicView:
    rich = _rich_view(environment, action_history, reward_history)
    return PublicView(
        tuple(rich.gap_bins), tuple(rich.ratio_bins), int(rich.cursor_relation_bin),
        float(rich.remaining_budget_fraction), tuple(rich.action_history),
        tuple(rich.reward_history), int(rich.trusted_goal),
    )


def _local_defect(environment: Any) -> float:
    points, cursor = environment._points, environment._cursor
    pairs = ((cursor - 2, cursor - 1), (cursor - 1, cursor),
             (cursor, cursor + 1), (cursor + 1, cursor + 2))
    values = []
    for left_index, right_index in pairs:
        left, right = points[left_index % len(points)], points[right_index % len(points)]
        determinant = abs(left.numerator * right.denominator - left.denominator * right.numerator)
        values.append(float(max(0, determinant - 1) ** 2))
    return statistics.fmean(values) if values else 0.0


def _is_movement(action: str) -> bool:
    return action in V6_ACTIONS[:14]


def public_signal_values(environment: Any, action: str) -> dict[str, float]:
    """Evaluator computes visible counterfactual signals; no target is used."""

    before_coverage, before_spectral, before_defect = _coverage(environment._points), _spectral(environment._points), _local_defect(environment)
    branch = deepcopy(environment)
    branch.step(action)
    after_coverage, after_spectral, after_defect = _coverage(branch._points), _spectral(branch._points), _local_defect(branch)
    defect_reduction = before_defect - after_defect
    return {
        "coverage_gain": float(before_coverage - after_coverage),
        "spectral_gain": float(before_spectral - after_spectral),
        "defect_reduction": float(defect_reduction),
        "active_search": float(-defect_reduction if _is_movement(action) else defect_reduction),
    }


def _hidden_action_gain(environment: Any, action: str) -> float:
    """Evaluator-only hidden F1 gain; never serialized in ``PublicView``."""

    before = evaluator_metrics(environment).f1
    branch = deepcopy(environment)
    branch.step(action)
    return float(evaluator_metrics(branch).f1 - before)


@dataclass(frozen=True, slots=True)
class Sample:
    view_key: tuple[object, ...]
    public_values: tuple[tuple[str, float], ...]
    hidden_values: tuple[float, ...]
    goal: str


def collect_samples(tasks: Sequence[RepairTask]) -> tuple[Sample, ...]:
    samples: list[Sample] = []
    for task_index, task in enumerate(tasks):
        environment = _environment(task)
        action_history: list[int] = []
        reward_history: list[int] = []
        for step_index in range(ACTION_BUDGET):
            view = public_view(environment, action_history, reward_history)
            public = {name: tuple(public_signal_values(environment, action)[name] for action in V6_ACTIONS) for name in SIGNALS}
            hidden = tuple(_hidden_action_gain(environment, action) for action in V6_ACTIONS)
            samples.append(Sample(view.as_tuple(), tuple((name, tuple(values)) for name, values in public.items()), hidden, task.goal.value))
            chosen_index = (ROOT_SEED + task_index * ACTION_BUDGET + step_index) % ACTION_COUNT
            chosen = V6_ACTIONS[chosen_index]
            behavior_reward = public_signal_values(environment, chosen)["active_search"]
            environment.step(chosen)
            action_history.append(chosen_index + 1)
            reward_history.append(_reward_bin(behavior_reward))
    return tuple(samples)


def _pair_auc(public: Sequence[float], hidden: Sequence[float]) -> tuple[float, int]:
    correct = 0.0; total = 0
    for left in range(ACTION_COUNT):
        for right in range(left + 1, ACTION_COUNT):
            hidden_delta = hidden[left] - hidden[right]
            if abs(hidden_delta) <= 1e-12:
                continue
            public_delta = public[left] - public[right]
            total += 1
            correct += 1.0 if public_delta * hidden_delta > 0 else 0.5 if abs(public_delta) <= 1e-12 else 0.0
    return (correct / total if total else 0.5), total


def split_diagnostic(tasks: Sequence[RepairTask]) -> dict[str, Any]:
    samples = collect_samples(tasks)
    if not samples:
        raise ValueError("public-interface diagnostic requires non-empty tasks")
    collisions = len(samples) - len({sample.view_key for sample in samples})
    by_signal: dict[str, dict[str, Any]] = {}
    for signal_index, signal in enumerate(SIGNALS):
        auc_values: list[float] = []; pair_count = 0; hit = 0; nonzero = 0
        for sample in samples:
            public = dict(sample.public_values)[signal]
            auc, pairs = _pair_auc(public, sample.hidden_values)
            auc_values.append(auc); pair_count += pairs
            public_best = max(range(ACTION_COUNT), key=lambda index: public[index])
            hidden_best = max(sample.hidden_values)
            hit += int(sample.hidden_values[public_best] >= hidden_best - 1e-12)
            nonzero += sum(abs(value) > 1e-12 for value in public)
        by_signal[signal] = {
            "auc": statistics.fmean(auc_values),
            "pair_count": pair_count,
            "top_action_hit_rate": hit / len(samples),
            "nonzero_action_values": nonzero,
            "sample_count": len(samples),
        }
    hidden_positive = sum(value > 1e-12 for sample in samples for value in sample.hidden_values)
    return {
        "sample_count": len(samples),
        "unique_view_count": len({sample.view_key for sample in samples}),
        "collision_rate": collisions / len(samples),
        "hidden_positive_action_count": hidden_positive,
        "by_signal": by_signal,
        "method": "public visible-signal ranking versus evaluator-only one-step hidden F1 gain",
        "feasible": hidden_positive >= MIN_HIDDEN_POSITIVE_ACTIONS and all(
            row["pair_count"] >= MIN_ALIGNMENT_PAIRS and row["auc"] >= MIN_ALIGNMENT_AUC for row in by_signal.values()
        ),
        "thresholds": {"min_hidden_positive_actions": MIN_HIDDEN_POSITIVE_ACTIONS, "min_alignment_pairs": MIN_ALIGNMENT_PAIRS, "min_alignment_auc": MIN_ALIGNMENT_AUC},
        "task_rows_sha256": _digest([(sample.view_key, sample.goal, sample.hidden_values) for sample in samples]),
    }


def leakage_audit() -> dict[str, Any]:
    environment = _environment(_make_v6_split("train")[0])
    view = public_view(environment)
    serialized = view.serialize()
    forbidden = ("target", "order", "deleted", "mask", "survivor", "initial_points", "exact_points", "list_length")
    keys = tuple(serialized)
    violations = [key for key in keys if any(token in key.lower() for token in forbidden)]
    blob = json.dumps(_jsonable(serialized), sort_keys=True)
    return {
        "shape": len(view.as_tuple()),
        "keys": keys,
        "fixed_shape": len(view.as_tuple()) == 23,
        "fraction_objects": False,
        "forbidden_key_violations": violations,
        "forbidden_serialized_tokens": [token for token in forbidden if token in blob.lower()],
        "trusted_goal_present": "trusted_goal_bin" in serialized,
        "passed": len(view.as_tuple()) == 23 and not violations and not any(token in blob.lower() for token in forbidden),
    }


def source_hashes(directory: Path) -> dict[str, str]:
    names = ("public_interface_v13_feasibility.py", "controller_v9_feasibility.py", "controller_v8_dev.py", "controller_v6.py", "repair_experiment.py", "strict_environment.py")
    return {name: sha256((directory / name).read_bytes()).hexdigest() for name in names}


def run_probe(*, train_tasks: Sequence[RepairTask], validation_tasks: Sequence[RepairTask], output_dir: Path | None = None, manifest_hashes: Mapping[str, str] | None = None, manifest_commitments: Mapping[str, Any] | None = None) -> dict[str, Any]:
    if output_dir is not None and ((output_dir / RECEIPT_NAME).exists() or (output_dir / RESULTS_NAME).exists()):
        raise RuntimeError("V13 receipt already exists; refusing to overwrite")
    result = {
        "protocol": {"kind": "V13 public-interface feasibility", "action_count": ACTION_COUNT, "action_budget": ACTION_BUDGET, "signals": SIGNALS, "claim_boundary": CLAIM_BOUNDARY},
        "manifest_hashes": dict(manifest_hashes or {}),
        "manifest_commitments": dict(manifest_commitments or {}),
        "counts": {"train_tasks": len(train_tasks), "validation_tasks": len(validation_tasks)},
        "costs": {"test_openings": 0, "test_updates": 0},
        "leakage_audit": leakage_audit(),
        "train": split_diagnostic(train_tasks),
        "validation": split_diagnostic(validation_tasks),
        "source_hashes": source_hashes(Path(__file__).resolve().parent),
    }
    result["status"] = "positive" if result["leakage_audit"]["passed"] and result["train"]["feasible"] and result["validation"]["feasible"] else "unverified_underpowered"
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / RECEIPT_NAME).write_text(json.dumps(_jsonable(result), indent=2, sort_keys=True) + "\n")
        (output_dir / RESULTS_NAME).write_text(result_markdown(result))
    return result


def result_markdown(result: Mapping[str, Any]) -> str:
    lines = ["# V13 public-interface feasibility", "", str(result["protocol"]["claim_boundary"]), "", f"Status: `{result['status']}`; leakage audit: `{result['leakage_audit']['passed']}`.", ""]
    for split in ("train", "validation"):
        row = result[split]
        lines += [f"## {split}", "", f"Samples: `{row['sample_count']}`; unique views: `{row['unique_view_count']}`; collision rate: `{row['collision_rate']:.4f}`; hidden positive actions: `{row['hidden_positive_action_count']}`; feasible: `{row['feasible']}` (AUC gate ≥ `{MIN_ALIGNMENT_AUC:.2f}`).", "", "| signal | AUC | top-action hit | pairs |", "| --- | ---: | ---: | ---: |"]
        for signal, values in row["by_signal"].items():
            lines.append(f"| {signal} | {values['auc']:.4f} | {values['top_action_hit_rate']:.4f} | {values['pair_count']} |")
        lines.append("")
    return "\n".join(lines)


def run_from_v6_manifest(*, output_dir: Path | None = None) -> dict[str, Any]:
    directory = Path(__file__).resolve().parent
    train_tasks, validation_tasks = _make_v6_split("train"), _make_v6_split("validation")
    manifest_receipt = json.loads((directory / "competency_v6_final_manifest_receipt.json").read_text(encoding="utf-8"))
    commitments = verify_manifest_reconstruction(train_tasks, validation_tasks, manifest_receipt)
    return run_probe(train_tasks=train_tasks, validation_tasks=validation_tasks, output_dir=output_dir, manifest_hashes={"public": str(manifest_receipt["manifest_seal"]["public_sha256"]), "private": str(manifest_receipt["manifest_seal"]["private_sha256"])}, manifest_commitments=commitments)


if __name__ == "__main__":
    run_from_v6_manifest(output_dir=Path(__file__).resolve().parent)
