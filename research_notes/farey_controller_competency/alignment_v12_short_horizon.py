"""Public-only train/validation alignment audit for the V12 reward channel.

Train trajectories are reduced to canonical V9 ``RichView`` tuples, action
identifiers, and quantized scalar V12 visible rewards.  Selectors consume only
the resulting fitted public table.  They cannot see an environment, exact
geometry, or an evaluator metric.  Validation never mutates that table; hidden
exact-recovery F1 is calculated only after a validation rollout is complete.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, is_dataclass
from hashlib import sha256
import inspect
import json
from pathlib import Path
import random
import statistics
from typing import Any, Mapping, Sequence

try:
    from .controller_v6 import V6_ACTIONS, evaluator_metrics
    from .controller_v8_dev import ROOT_SEED, _environment, _make_v6_split
    from .controller_v9_feasibility import _reward_bin, _rich_view
    from .controller_v12_dev import active_search_reward
    from .repair_experiment import RepairTask
except ImportError:  # Direct execution from this directory.
    from controller_v6 import V6_ACTIONS, evaluator_metrics  # type: ignore[no-redef]
    from controller_v8_dev import ROOT_SEED, _environment, _make_v6_split  # type: ignore[no-redef]
    from controller_v9_feasibility import _reward_bin, _rich_view  # type: ignore[no-redef]
    from controller_v12_dev import active_search_reward  # type: ignore[no-redef]
    from repair_experiment import RepairTask  # type: ignore[no-redef]


HORIZONS = (1, 2, 3, 4)
BOOTSTRAP_RESAMPLES = 1000
HIDDEN_F1_MARGIN = 0.01
RECEIPT_NAME = "alignment_v12_short_horizon_receipt.json"
RESULTS_NAME = "ALIGNMENT_V12_SHORT_HORIZON_RESULTS.md"
EPSILON = 1e-12
CLAIM_BOUNDARY = (
    "Development-only train/validation public-table audit. The selectors use "
    "only canonical public views and train-fitted quantized visible rewards; "
    "hidden F1 is evaluator-only and no sealed test access occurs."
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


def _cell(task: RepairTask) -> str:
    return f"N{task.order}:{task.pattern.value}:{task.goal.value}"


def _task_commitment(task: RepairTask) -> str:
    return _digest((task.order, task.pattern.value, task.goal.value, task.seed, task.damage_count))


def canonical_public_state(environment: Any, action_history: Sequence[int], reward_history: Sequence[int]) -> tuple[object, ...]:
    """Fixed V9 quantized controller state; no exact state is retained here."""

    return _rich_view(environment, action_history, reward_history).as_tuple()


@dataclass(frozen=True, slots=True)
class PublicTransition:
    state: tuple[object, ...]
    action_index: int
    visible_reward_bin: int
    next_state: tuple[object, ...]
    cell: str


def collect_train_transitions(tasks: Sequence[RepairTask]) -> tuple[PublicTransition, ...]:
    """Collect one deterministic public trajectory per task without hidden reads."""

    output: list[PublicTransition] = []
    for task_index, task in enumerate(tasks):
        environment = _environment(task)
        action_history: list[int] = []
        reward_history: list[int] = []
        for step_index in range(16):
            state = canonical_public_state(environment, action_history, reward_history)
            action_index = (ROOT_SEED + task_index * 17 + step_index * 7) % len(V6_ACTIONS)
            visible_reward = active_search_reward(environment, V6_ACTIONS[action_index])
            environment.step(V6_ACTIONS[action_index])
            reward_bin = _reward_bin(visible_reward)
            action_history.append(action_index + 1)
            reward_history.append(reward_bin)
            output.append(PublicTransition(
                state,
                action_index,
                reward_bin,
                canonical_public_state(environment, action_history, reward_history),
                _cell(task),
            ))
    return tuple(output)


@dataclass(frozen=True, slots=True)
class PublicTransitionTable:
    """Immutable train-fitted public reward and successor table."""

    reward_by_state_action: Mapping[tuple[tuple[object, ...], int], float]
    next_state_by_state_action: Mapping[tuple[tuple[object, ...], int], tuple[object, ...]]
    reward_by_action: tuple[float, ...]
    train_update_count: int
    digest: str

    def reward(self, state: tuple[object, ...], action_index: int) -> float:
        return self.reward_by_state_action.get((state, action_index), self.reward_by_action[action_index])

    def successor(self, state: tuple[object, ...], action_index: int) -> tuple[object, ...]:
        return self.next_state_by_state_action.get((state, action_index), state)


def fit_public_transition_table(transitions: Sequence[PublicTransition]) -> PublicTransitionTable:
    if not transitions:
        raise ValueError("public table needs at least one train transition")
    rewards: dict[tuple[tuple[object, ...], int], list[int]] = defaultdict(list)
    successors: dict[tuple[tuple[object, ...], int], Counter[tuple[object, ...]]] = defaultdict(Counter)
    by_action: dict[int, list[int]] = defaultdict(list)
    for transition in transitions:
        key = (transition.state, transition.action_index)
        rewards[key].append(transition.visible_reward_bin)
        successors[key][transition.next_state] += 1
        by_action[transition.action_index].append(transition.visible_reward_bin)
    reward_table = {key: statistics.fmean(values) for key, values in rewards.items()}
    successor_table = {
        key: max(counts, key=lambda value: (counts[value], repr(value)))
        for key, counts in successors.items()
    }
    global_reward = tuple(statistics.fmean(by_action[index]) if by_action[index] else 0.0 for index in range(len(V6_ACTIONS)))
    payload = {
        "rewards": sorted((repr(state), action, value) for (state, action), value in reward_table.items()),
        "successors": sorted((repr(state), action, repr(next_state)) for (state, action), next_state in successor_table.items()),
        "global": global_reward,
    }
    return PublicTransitionTable(reward_table, successor_table, global_reward, len(transitions), _digest(payload))


def public_argmax_action(table: PublicTransitionTable, state: tuple[object, ...]) -> int:
    """H=1 public baseline. It reads only the fitted public table and state."""

    return max(range(len(V6_ACTIONS)), key=lambda action: (table.reward(state, action), -action))


def public_planner_actions(table: PublicTransitionTable, state: tuple[object, ...], horizon: int) -> tuple[int, ...]:
    """H-step public-table planner. It has no environment or hidden channel."""

    if horizon < 1 or horizon > max(HORIZONS):
        raise ValueError(f"horizon must be in [1, {max(HORIZONS)}]")
    cache: dict[tuple[tuple[object, ...], int], tuple[float, tuple[int, ...]]] = {}

    def best(current: tuple[object, ...], remaining: int) -> tuple[float, tuple[int, ...]]:
        if remaining == 0:
            return 0.0, ()
        key = (current, remaining)
        if key not in cache:
            values = []
            for action in range(len(V6_ACTIONS)):
                future, suffix = best(table.successor(current, action), remaining - 1)
                values.append((table.reward(current, action) + future, (action, *suffix)))
            cache[key] = max(values, key=lambda item: (item[0], tuple(-action for action in item[1])))
        return cache[key]

    return best(state, horizon)[1]


def visible_state_only_action(state: tuple[object, ...]) -> int:
    """Fixed visible-state control using only the first eight gap bins."""

    gaps = tuple(int(value) for value in state[:8])
    left, right = gaps[3], gaps[4]
    if max(left, right) >= max(gaps[0], gaps[7]):
        return V6_ACTIONS.index("insert_mediant")
    return V6_ACTIONS.index("move_left" if gaps[0] > gaps[7] else "move_right")


def zero_reward_action(state: tuple[object, ...]) -> int:
    """Zero-feedback control: fixed legal choice independent of reward values."""

    del state
    return 0


def random_action(state: tuple[object, ...], seed: int) -> int:
    """Seeded legal-action control; state is accepted but intentionally unused."""

    del state
    return random.Random(seed).randrange(len(V6_ACTIONS))


def _selector_source_guard() -> bool:
    forbidden = ("_points", "_cursor", "deepcopy", "evaluator_metrics")
    selectors = (public_argmax_action, public_planner_actions, visible_state_only_action, zero_reward_action, random_action)
    return all(all(banned_text not in inspect.getsource(selector) for banned_text in forbidden) for selector in selectors)


def _actions_for_policy(
    policy: str,
    table: PublicTransitionTable,
    state: tuple[object, ...],
    horizon: int,
    seed: int,
) -> tuple[int, ...]:
    if policy == "public_h1":
        return (public_argmax_action(table, state),)
    if policy == "public_selected":
        return public_planner_actions(table, state, horizon)
    if policy == "visible_state_only":
        return tuple(visible_state_only_action(state) for _ in range(horizon))
    if policy == "zero_reward":
        return tuple(zero_reward_action(state) for _ in range(horizon))
    if policy == "random":
        return tuple(random_action(state, seed ^ step_index) for step_index in range(horizon))
    raise ValueError(f"unknown policy: {policy}")


def _rollout_public_return(
    tasks: Sequence[RepairTask],
    table: PublicTransitionTable,
    *,
    horizon: int,
    policy: str,
    include_hidden: bool,
    split: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task_index, task in enumerate(tasks):
        environment = _environment(task)
        action_history: list[int] = []
        reward_history: list[int] = []
        state = canonical_public_state(environment, action_history, reward_history)
        actions = _actions_for_policy(policy, table, state, horizon, ROOT_SEED ^ task.seed ^ horizon)
        total = 0.0
        for action_index in actions:
            visible_reward = active_search_reward(environment, V6_ACTIONS[action_index])
            total += visible_reward
            environment.step(V6_ACTIONS[action_index])
            action_history.append(action_index + 1)
            reward_history.append(_reward_bin(visible_reward))
        row: dict[str, Any] = {
            "split": split,
            "task_index": task_index,
            "task_commitment": _task_commitment(task),
            "horizon": horizon,
            "policy": policy,
            "public_return": total,
            "action_count": len(actions),
            "actions_sha256": _digest(actions),
        }
        if include_hidden:
            hidden = evaluator_metrics(environment)
            row.update({"hidden_f1": hidden.f1, "hidden_exact": hidden.exact})
        rows.append(row)
    return rows


def select_horizon_by_train_public_return(tasks: Sequence[RepairTask], table: PublicTransitionTable) -> tuple[int, dict[int, float]]:
    """Select among H=2..4 with train public return alone, never hidden F1."""

    scores = {
        horizon: statistics.fmean(
            row["public_return"]
            for row in _rollout_public_return(tasks, table, horizon=horizon, policy="public_selected", include_hidden=False, split="train")
        )
        for horizon in HORIZONS[1:]
    }
    return max(scores, key=lambda horizon: (scores[horizon], -horizon)), scores


def paired_bootstrap(treatment: Sequence[Mapping[str, Any]], baseline: Sequence[Mapping[str, Any]], *, metric: str, resamples: int, seed: int) -> dict[str, Any]:
    def key(row: Mapping[str, Any]) -> tuple[str, int, int]:
        return str(row["split"]), int(row["task_index"]), int(row["horizon"])
    left, right = {key(row): float(row[metric]) for row in treatment}, {key(row): float(row[metric]) for row in baseline}
    if not left or left.keys() != right.keys():
        raise ValueError("paired bootstrap requires identical nonempty task keys")
    differences = tuple(left[key] - right[key] for key in sorted(left))
    rng = random.Random(seed)
    samples = sorted(statistics.fmean(rng.choice(differences) for _ in differences) for _ in range(max(1, resamples)))
    return {
        "effect": statistics.fmean(differences),
        "ci_low": samples[max(0, int(0.025 * len(samples)))],
        "ci_high": samples[min(len(samples) - 1, int(0.975 * len(samples)))],
        "pairs": len(differences),
        "resamples": max(1, resamples),
    }


def _sign(value: float) -> int:
    return 1 if value > EPSILON else -1 if value < -EPSILON else 0


def alignment_record(treatment: Mapping[str, Any], baseline: Mapping[str, Any]) -> dict[str, Any]:
    public_delta = float(treatment["public_return"]) - float(baseline["public_return"])
    hidden_delta = float(treatment["hidden_f1"]) - float(baseline["hidden_f1"])
    public_sign, hidden_sign = _sign(public_delta), _sign(hidden_delta)
    return {
        "split": treatment["split"], "task_index": treatment["task_index"], "task_commitment": treatment["task_commitment"],
        "horizon": treatment["horizon"], "treatment": treatment["policy"], "baseline": baseline["policy"],
        "public_return_delta": public_delta, "hidden_f1_delta": hidden_delta,
        "aligned": public_sign == hidden_sign, "discordant": public_sign * hidden_sign == -1,
        "ambiguous": (public_sign == 0) != (hidden_sign == 0),
    }


def negative_fixtures() -> dict[str, Any]:
    base = {"split": "fixture", "task_index": 0, "task_commitment": "fixture", "horizon": 1}
    discordant = alignment_record(
        {**base, "policy": "public", "public_return": 1.0, "hidden_f1": 0.0},
        {**base, "policy": "control", "public_return": 0.0, "hidden_f1": 1.0},
    )
    aligned = alignment_record(
        {**base, "policy": "public", "public_return": 1.0, "hidden_f1": 1.0},
        {**base, "policy": "control", "public_return": 0.0, "hidden_f1": 0.0},
    )
    return {"discordant": discordant, "aligned": aligned, "passed": discordant["discordant"] and aligned["aligned"]}


def support_by_action_and_cell(transitions: Sequence[PublicTransition]) -> dict[str, Any]:
    by_action = {V6_ACTIONS[index]: 0 for index in range(len(V6_ACTIONS))}
    by_cell: dict[str, int] = defaultdict(int)
    by_cell_action: dict[str, dict[str, int]] = defaultdict(lambda: {action: 0 for action in V6_ACTIONS})
    nonzero = 0
    for transition in transitions:
        by_action[V6_ACTIONS[transition.action_index]] += 1
        by_cell[transition.cell] += 1
        by_cell_action[transition.cell][V6_ACTIONS[transition.action_index]] += 1
        nonzero += int(transition.visible_reward_bin != 0)
    return {
        "sample_count": len(transitions), "nonzero_reward_count": nonzero,
        "action_counts": by_action, "cell_counts": dict(sorted(by_cell.items())),
        "action_counts_by_cell": {cell: by_cell_action[cell] for cell in sorted(by_cell_action)},
        "all_actions_supported": all(count > 0 for count in by_action.values()),
        "all_actions_supported_per_cell": all(all(count > 0 for count in counts.values()) for counts in by_cell_action.values()),
    }


def source_hashes(directory: Path) -> dict[str, str]:
    names = ("alignment_v12_short_horizon.py", "controller_v12_dev.py", "controller_v11_dev.py", "controller_v9_feasibility.py", "controller_v8_dev.py", "controller_v6.py")
    return {name: sha256((directory / name).read_bytes()).hexdigest() for name in names}


def result_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# V12 public-table short-horizon alignment audit", "", result["protocol"]["claim_boundary"], "",
        f"Train transitions: `{result['counts']['train_transitions']}`; validation updates: `{result['counts']['validation_updates']}`; train-selected H: `{result['selection']['selected_horizon']}`; alignment status: `{result['alignment_status']['status']}`.", "",
        "| treatment vs control | H | public-return effect [95% CI] | hidden-F1 effect [95% CI] | pairs |",
        "| --- | ---: | --- | --- | ---: |",
    ]
    for key, value in sorted(result["paired_bootstrap"].items()):
        public, hidden = value["public_return"], value["hidden_f1"]
        lines.append(f"| {key} | {value['horizon']} | {public['effect']:.5f} [{public['ci_low']:.5f}, {public['ci_high']:.5f}] | {hidden['effect']:.5f} [{hidden['ci_low']:.5f}, {hidden['ci_high']:.5f}] | {public['pairs']} |")
    lines.extend([
        "", "Receipt evaluates every preregistered H=1..4 on validation. Train selection is reported separately and never filters evaluator-only hidden F1 rows.",
        f"Support: all actions `{result['support']['all_actions_supported']}`; all actions per cell `{result['support']['all_actions_supported_per_cell']}`; negative fixtures `{result['negative_fixtures']['passed']}`; selector guard `{result['selector_guard']}`.", "",
    ])
    return "\n".join(lines)


def run_alignment(*, train_tasks: Sequence[RepairTask], validation_tasks: Sequence[RepairTask], output_dir: Path | None = None, bootstrap_resamples: int = BOOTSTRAP_RESAMPLES) -> dict[str, Any]:
    if output_dir is not None and ((output_dir / RECEIPT_NAME).exists() or (output_dir / RESULTS_NAME).exists()):
        raise RuntimeError("alignment receipt already exists; refusing to overwrite")
    transitions = collect_train_transitions(train_tasks)
    table = fit_public_transition_table(transitions)
    selected_horizon, train_scores = select_horizon_by_train_public_return(train_tasks, table)
    validation_rows: list[dict[str, Any]] = []
    for horizon in HORIZONS:
        public_policy = "public_h1" if horizon == 1 else "public_selected"
        for policy in (public_policy, "random", "visible_state_only", "zero_reward"):
            validation_rows.extend(_rollout_public_return(validation_tasks, table, horizon=horizon, policy=policy, include_hidden=True, split="validation"))
    if table.digest != fit_public_transition_table(transitions).digest:
        raise AssertionError("validation mutated the train-fitted public table")
    alignment_rows: list[dict[str, Any]] = []
    comparisons: dict[str, Any] = {}
    qualified_negative = False
    supported_horizons: list[int] = []
    for horizon in HORIZONS:
        public_policy = "public_h1" if horizon == 1 else "public_selected"
        treatment = [row for row in validation_rows if row["horizon"] == horizon and row["policy"] == public_policy]
        hidden_support = sum(float(row["hidden_f1"]) > EPSILON for row in treatment)
        if horizon >= 2 and hidden_support:
            supported_horizons.append(horizon)
        for control in ("random", "visible_state_only", "zero_reward"):
            baseline = [row for row in validation_rows if row["horizon"] == horizon and row["policy"] == control]
            records = [alignment_record(left, right) for left, right in zip(treatment, baseline, strict=True)]
            alignment_rows.extend(records)
            key = f"H{horizon}:{public_policy}_minus_{control}"
            comparisons[key] = {
                "horizon": horizon,
                "hidden_repair_support": hidden_support,
                "public_return": paired_bootstrap(treatment, baseline, metric="public_return", resamples=bootstrap_resamples, seed=ROOT_SEED ^ horizon ^ len(control)),
                "hidden_f1": paired_bootstrap(treatment, baseline, metric="hidden_f1", resamples=bootstrap_resamples, seed=ROOT_SEED ^ horizon ^ len(key)),
            }
            if horizon >= 2 and hidden_support and comparisons[key]["hidden_f1"]["ci_high"] < HIDDEN_F1_MARGIN:
                qualified_negative = True
    alignment_status = {
        "margin": HIDDEN_F1_MARGIN,
        "supported_horizons": supported_horizons,
        "status": "negative" if qualified_negative else "unverified_underpowered",
        "rule": "negative requires H>=2 nonzero hidden-repair support and a paired hidden-F1 CI upper bound below the preregistered margin; otherwise unverified_underpowered",
    }
    result = {
        "protocol": {"kind": "V12 train-fitted public transition-table alignment audit", "horizons": list(HORIZONS), "claim_boundary": CLAIM_BOUNDARY},
        "counts": {"train_tasks": len(train_tasks), "validation_tasks": len(validation_tasks), "train_transitions": len(transitions), "validation_updates": 0, "validation_policy_rows": len(validation_rows), "alignment_records": len(alignment_rows)},
        "train_table": {"digest": table.digest, "update_count": table.train_update_count, "digest_after_validation": table.digest},
        "support": support_by_action_and_cell(transitions), "selection": {"h1_baseline": 1, "selected_horizon": selected_horizon, "train_public_return_by_horizon": train_scores},
        "selector_guard": _selector_source_guard(), "negative_fixtures": negative_fixtures(), "alignment_status": alignment_status,
        "validation_policy_rows": validation_rows, "per_task_alignment": alignment_rows, "paired_bootstrap": comparisons,
        "source_hashes": source_hashes(Path(__file__).resolve().parent),
    }
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / RECEIPT_NAME).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        (output_dir / RESULTS_NAME).write_text(result_markdown(result), encoding="utf-8")
    return result


def run_from_v12_public_splits(*, output_dir: Path | None = None) -> dict[str, Any]:
    return run_alignment(train_tasks=_make_v6_split("train"), validation_tasks=_make_v6_split("validation"), output_dir=output_dir)


if __name__ == "__main__":
    run_from_v12_public_splits(output_dir=Path(__file__).resolve().parent)
