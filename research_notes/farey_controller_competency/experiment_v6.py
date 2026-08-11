#!/usr/bin/env python3
"""One-shot V6 sealed Farey repair experiment.

The real run is deliberately guarded by the absence of FINAL_RECEIPT.  Unit
tests exercise helpers only; they never construct or open the sealed test
accessor.  Training is fixed offline reward-attribution replay, not online
adaptation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from hashlib import sha256
import json
from pathlib import Path
import statistics
from typing import Any, Iterable, Mapping, Sequence

try:
    from .competency_v6_final_manifest import (
        VALIDATION_PURPOSE,
        FinalManifestAccess,
        seal_manifest,
    )
    from .controller_v6 import (
        MATCHED_SEED_COUNT,
        V6_BUDGET,
        TrainedLane,
        V6Environment,
        V6LinearQ,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        _make_view,
        core_conjunction,
        evaluator_metrics,
        feedback_gate,
        recovery_gate,
        structural_gate,
        synchronous_structural_rollout,
        train_reward_lanes,
        train_structural_lanes,
        transfer_gate,
    )
    from .repair_experiment import RepairTask
    from .strict_environment import StrictEnvironment
except ImportError:
    from competency_v6_final_manifest import (  # type: ignore[no-redef]
        VALIDATION_PURPOSE,
        FinalManifestAccess,
        seal_manifest,
    )
    from controller_v6 import (  # type: ignore[no-redef]
        MATCHED_SEED_COUNT,
        V6_BUDGET,
        TrainedLane,
        V6Environment,
        V6LinearQ,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        _make_view,
        core_conjunction,
        evaluator_metrics,
        feedback_gate,
        recovery_gate,
        structural_gate,
        synchronous_structural_rollout,
        train_reward_lanes,
        train_structural_lanes,
        transfer_gate,
    )
    from repair_experiment import RepairTask  # type: ignore[no-redef]
    from strict_environment import StrictEnvironment  # type: ignore[no-redef]


ROOT_SEED = 20261001
BOOTSTRAP_RESAMPLES = 5000
HERE = Path(__file__).resolve().parent
FINAL_RECEIPT = HERE / "experiment_v6_final_receipt.json"
FINAL_RESULTS = HERE / "EXPERIMENT_V6_RESULTS.md"
FINAL_OPENING_MARKER = HERE / "experiment_v6_test_opened.marker.json"
CLAIM_SCOPE = "offline_reward_attribution_replay_with_frozen_transfer"
FINAL_MANIFEST_ACCESS_POLICY = "train_then_validation_then_one_shot_frozen_test"


def _canonical(value: Any) -> bytes:
    return json.dumps(_jsonable(value), sort_keys=True, separators=(",", ":")).encode()


def _digest(value: Any) -> str:
    return sha256(_canonical(value)).hexdigest()


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


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
    """Evaluator-held task wrapper; policies receive only ControllerView."""

    _task: RepairTask

    def fresh_environment(self) -> V6Environment:
        return _environment(self._task)


class PublicStream:
    def __init__(self, tasks: Sequence[RepairTask]) -> None:
        self._episodes = tuple(PublicEpisode(task) for task in tasks)

    def __iter__(self):
        return iter(self._episodes)


def _task_key(task: RepairTask) -> tuple[int, str, str, int, int]:
    return task.order, task.pattern.value, task.goal.value, task.seed, task.damage_count


def _runtime_task_id(task: RepairTask) -> str:
    """Opaque evaluator ID; avoids reading sealed private rows before opening."""

    return "runtime-" + _digest(_task_key(task))[:20]


def _evaluate_one(policy: Any, task: RepairTask) -> tuple[dict[str, Any], tuple[str, ...]]:
    environment = _environment(task)
    feedback = 0.0
    reward_sum = 0.0
    actions: list[str] = []
    for _ in range(V6_BUDGET):
        view = _make_view(environment, feedback)
        action = policy.choose(view)
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
    }, tuple(actions)


def _rows_for_policy(
    policy: Any,
    tasks: Sequence[RepairTask],
    *,
    learner_seed: int,
    policy_name: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for task in tasks:
        metrics, actions = _evaluate_one(policy, task)
        rows.append({
            "task_id": _runtime_task_id(task),
            "learner_seed": learner_seed,
            "seed": learner_seed,
            "N": task.order,
            "family": task.pattern.value,
            "goal": task.goal.value,
            "cell": f"N{task.order}:{task.pattern.value}:{task.goal.value}",
            "policy": policy_name,
            "actions_sha256": _digest(actions),
            **metrics,
        })
    return rows


def _structural_rows(
    policy: V6LinearQ,
    tasks: Sequence[RepairTask],
    *,
    learner_seed: int,
    arm: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    target_channel = arm.split("→", 1)[1]
    rows: list[dict[str, Any]] = []
    permutation_hashes: list[str] = []
    for goal in sorted({task.goal.value for task in tasks}):
        group = [task for task in tasks if task.goal.value == goal]
        environments = [_environment(task) for task in group]
        rollout = synchronous_structural_rollout(
            environments,
            policy,
            channel=target_channel,
            seed=ROOT_SEED ^ learner_seed ^ (0 if goal == "coverage" else 0x5A5A),
        )
        permutation_hashes.append(_digest(rollout.source_indices))
        for task, environment, action_column in zip(group, environments, zip(*rollout.actions)):
            hidden = evaluator_metrics(environment)
            rows.append({
                "task_id": _runtime_task_id(task),
                "learner_seed": learner_seed,
                "seed": learner_seed,
                "N": task.order,
                "family": task.pattern.value,
                "goal": task.goal.value,
                "cell": f"N{task.order}:{task.pattern.value}:{task.goal.value}",
                "policy": arm,
                "precision": hidden.precision,
                "recall": hidden.recall,
                "f1": hidden.f1,
                "exact": hidden.exact,
                "action_count": V6_BUDGET,
                "actions_sha256": _digest(action_column),
            })
    return rows, permutation_hashes


def aggregate_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Aggregate task rows to one paired row per learner seed and test cell."""

    grouped: dict[tuple[int, str], list[Mapping[str, Any]]] = {}
    for row in rows:
        grouped.setdefault((int(row["learner_seed"]), str(row["cell"])), []).append(row)
    output: list[dict[str, Any]] = []
    for (learner_seed, cell), group in sorted(grouped.items()):
        first = group[0]
        output.append({
            "seed": learner_seed,
            "learner_seed": learner_seed,
            "cell": cell,
            "N": int(first["N"]),
            "family": str(first["family"]),
            "goal": str(first["goal"]),
            "task_count": len(group),
            **{
                metric: statistics.fmean(float(row[metric]) for row in group)
                for metric in ("precision", "recall", "f1", "exact")
            },
        })
    return output


def _combined_model_digest(
    reward_lanes: Mapping[int, Mapping[str, TrainedLane]],
    structural_lanes: Mapping[int, Mapping[str, TrainedLane]],
    manifest: Mapping[str, Any],
) -> str:
    payload = {
        "claim_scope": CLAIM_SCOPE,
        "root_seed": ROOT_SEED,
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "manifest_private_hash": manifest["private_hash"],
        "manifest_public_hash": manifest["public_hash"],
        "reward": {
            str(seed): {
                name: {
                    "digest": lane.controller.digest(),
                    "updates": lane.controller.updates,
                    "update_delta": lane.update_delta,
                    "learning": lane.controller.learning,
                }
                for name, lane in lanes.items()
            }
            for seed, lanes in reward_lanes.items()
        },
        "structural": {
            str(seed): {
                name: {
                    "digest": lane.controller.digest(),
                    "updates": lane.controller.updates,
                    "update_delta": lane.update_delta,
                    "learning": lane.controller.learning,
                }
                for name, lane in lanes.items()
            }
            for seed, lanes in structural_lanes.items()
        },
        "baselines": {
            "names": ["random", "local", "visible_greedy"],
            "random_seed_rule": "ROOT_SEED xor learner_seed",
        },
        "source_hashes": source_hashes(),
    }
    return "sha256:" + _digest(payload)


def source_hashes() -> dict[str, str]:
    names = (
        "experiment_v6.py",
        "controller_v6.py",
        "competency_v6_final_manifest.py",
        "competency_v5_feasibility.py",
        "strict_environment.py",
    )
    return {name: sha256((HERE / name).read_bytes()).hexdigest() for name in names}


def _summaries(rows_by_policy: Mapping[str, Sequence[Mapping[str, Any]]]) -> dict[str, Any]:
    return {
        name: {
            metric: statistics.fmean(float(row[metric]) for row in rows)
            for metric in ("precision", "recall", "f1", "exact")
        }
        for name, rows in rows_by_policy.items()
    }


def _assert_unopened(receipt_path: Path, results_path: Path, marker_path: Path) -> None:
    if receipt_path.exists() or results_path.exists() or marker_path.exists():
        raise RuntimeError("V6 final test has already been opened; refusing to rerun")


def _commit_opening(marker_path: Path, *, model_digest: str, manifest_private_hash: str) -> None:
    with marker_path.open("x", encoding="utf-8") as marker:
        json.dump({
            "model_digest": model_digest,
            "manifest_private_hash": manifest_private_hash,
            "status": "controller_test_opening_committed",
        }, marker, sort_keys=True)
        marker.write("\n")


def run_final() -> dict[str, Any]:
    """Perform the sole real V6 test opening and write its immutable receipt."""

    receipt_path, results_path, opening_marker_path = FINAL_RECEIPT, FINAL_RESULTS, FINAL_OPENING_MARKER
    _assert_unopened(receipt_path, results_path, opening_marker_path)
    manifest = seal_manifest()
    access = FinalManifestAccess(manifest)
    train_tasks = access.training_tasks()
    validation_tasks = access.validation_tasks(purpose=VALIDATION_PURPOSE)
    train_stream = PublicStream(train_tasks)
    reward_lanes: dict[int, Mapping[str, TrainedLane]] = {}
    structural_lanes: dict[int, Mapping[str, TrainedLane]] = {}
    validation_rows: dict[str, list[dict[str, Any]]] = {}
    for learner_seed in range(MATCHED_SEED_COUNT):
        lane_seed = ROOT_SEED + learner_seed * 1009
        reward_lanes[learner_seed] = train_reward_lanes(
            train_stream, seed=lane_seed, init_seed=lane_seed ^ 0x1111
        )
        structural_lanes[learner_seed] = train_structural_lanes(
            train_stream, seed=lane_seed ^ 0x2222, init_seed=lane_seed ^ 0x3333
        )
        for name, lane in reward_lanes[learner_seed].items():
            validation_rows.setdefault(name, []).extend(_rows_for_policy(
                lane.controller, validation_tasks, learner_seed=learner_seed,
                policy_name=name,
            ))
    expected_train_updates = len(train_tasks) * V6_BUDGET
    train_update_receipt: dict[str, dict[str, Any]] = {}
    for learner_seed in range(MATCHED_SEED_COUNT):
        for family, lanes in (("reward", reward_lanes[learner_seed]), ("structural", structural_lanes[learner_seed])):
            for name, lane in lanes.items():
                key = f"seed{learner_seed}:{family}:{name}"
                if lane.update_delta != expected_train_updates or lane.controller.updates != expected_train_updates:
                    raise AssertionError("lane training update count differs from the preregistered budget")
                if lane.controller.learning:
                    raise AssertionError("lane was not frozen before model digest")
                train_update_receipt[key] = {
                    "updates": lane.controller.updates,
                    "update_delta": lane.update_delta,
                    "expected": expected_train_updates,
                    "learning": lane.controller.learning,
                }
    model_digest = _combined_model_digest(reward_lanes, structural_lanes, manifest)
    opening_token = access.freeze_model(model_digest)
    # Durable one-shot guard is created before hidden test tasks are returned.
    _commit_opening(
        opening_marker_path,
        model_digest=model_digest,
        manifest_private_hash=str(manifest["private_hash"]),
    )
    test_tasks = access.open_test(frozen_model_digest=model_digest, opening_token=opening_token)

    task_rows: dict[str, list[dict[str, Any]]] = {}
    train_digests: dict[str, str] = {}
    test_digests: dict[str, str] = {}
    test_updates: dict[str, int] = {}
    permutation_hashes: dict[str, list[str]] = {}
    for learner_seed in range(MATCHED_SEED_COUNT):
        for name, lane in reward_lanes[learner_seed].items():
            key = f"seed{learner_seed}:{name}"
            before = lane.controller.digest(), lane.controller.updates
            task_rows.setdefault(name, []).extend(_rows_for_policy(
                lane.controller, test_tasks, learner_seed=learner_seed,
                policy_name=name,
            ))
            after = lane.controller.digest(), lane.controller.updates
            train_digests[key], test_digests[key] = before[0], after[0]
            test_updates[key] = after[1] - before[1]
        baselines = {
            "random": V6Random(ROOT_SEED ^ learner_seed),
            "local": V6Local(),
            "visible_greedy": V6VisibleGreedy(),
        }
        for name, policy in baselines.items():
            task_rows.setdefault(name, []).extend(_rows_for_policy(
                policy, test_tasks, learner_seed=learner_seed,
                policy_name=name,
            ))
        for arm, lane in structural_lanes[learner_seed].items():
            key = f"seed{learner_seed}:{arm}"
            before = lane.controller.digest(), lane.controller.updates
            rows, hashes = _structural_rows(
                lane.controller, test_tasks, learner_seed=learner_seed,
                arm=arm,
            )
            task_rows.setdefault(arm, []).extend(rows)
            permutation_hashes.setdefault(arm, []).extend(hashes)
            after = lane.controller.digest(), lane.controller.updates
            train_digests[key], test_digests[key] = before[0], after[0]
            test_updates[key] = after[1] - before[1]

    aggregated = {name: aggregate_rows(rows) for name, rows in task_rows.items()}
    feedback = feedback_gate(
        aggregated["true"], aggregated["within_episode_permuted"], aggregated["zero"],
        resamples=BOOTSTRAP_RESAMPLES,
    )
    recovery = recovery_gate(
        aggregated["true"],
        {name: aggregated[name] for name in ("within_episode_permuted", "zero", "random", "local", "visible_greedy")},
        resamples=BOOTSTRAP_RESAMPLES,
    )
    transfer = transfer_gate(
        aggregated["true"],
        {name: aggregated[name] for name in ("random", "local", "visible_greedy")},
        test_updates=test_updates,
        train_digests=train_digests,
        test_digests=test_digests,
        resamples=BOOTSTRAP_RESAMPLES,
    )
    structural = structural_gate(
        aggregated["I→I"], aggregated["I→S"], aggregated["S→S"],
        resamples=BOOTSTRAP_RESAMPLES,
    )
    core = core_conjunction(feedback, recovery, transfer)
    all_positive = bool(core and structural["positive"])
    access.test_updates = sum(test_updates.values())
    result = {
        "protocol": {
            "claim_scope": CLAIM_SCOPE,
            "learner_seeds": MATCHED_SEED_COUNT,
            "action_budget": V6_BUDGET,
            "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
            "manifest_private_hash": manifest["private_hash"],
            "manifest_public_hash": manifest["public_hash"],
            "access_policy": FINAL_MANIFEST_ACCESS_POLICY,
            "model_digest": model_digest,
        },
        "access": access.audit_snapshot(),
        "validation_summary_not_used_for_tuning": _summaries(validation_rows),
        "test_summary": _summaries(task_rows),
        "gates": {
            "feedback": feedback,
            "recovery": recovery,
            "transfer": transfer,
            "structural": structural,
            "core_conjunction": core,
            "full_structural_conjunction": all_positive,
        },
        "freeze": {
            "train_updates": train_update_receipt,
            "train_digests": train_digests,
            "test_digests": test_digests,
            "test_update_deltas": test_updates,
            "all_unchanged": all(value == 0 for value in test_updates.values()) and train_digests == test_digests,
        },
        "structural_permutation_hashes": permutation_hashes,
        "aggregated_rows": aggregated,
        "task_rows": task_rows,
        "source_hashes": source_hashes(),
        "claim_boundary": (
            "This is fixed offline reward-attribution replay with frozen transfer, not online adaptation. "
            "A narrow Levin-style competency claim requires every core gate plus the structural gate; "
            "otherwise the result is negative or unverified and no agency claim is made."
        ),
    }
    receipt_path.write_bytes(json.dumps(_jsonable(result), sort_keys=True, indent=2).encode() + b"\n")
    results_path.write_text(result_markdown(result), encoding="utf-8")
    return result


def result_markdown(result: Mapping[str, Any]) -> str:
    gates = result["gates"]
    core_valid = all(gates[name]["valid"] for name in ("feedback", "recovery", "transfer"))
    full_valid = core_valid and gates["structural"]["valid"]
    lines = [
        "# V6 final Farey repair experiment",
        "",
        f"Claim scope: `{result['protocol']['claim_scope']}`. Test accessor openings: `{result['access']['test_openings']}`; test updates: `{result['access']['test_updates']}`.",
        "",
        "| gate | valid | positive |",
        "| --- | --- | --- |",
    ]
    for name in ("feedback", "recovery", "transfer", "structural"):
        gate = gates[name]
        lines.append(f"| {name} | `{gate['valid']}` | `{gate['positive']}` |")
    lines.extend([
        f"| core conjunction | `{core_valid}` | `{gates['core_conjunction']}` |",
        f"| core + structural | `{full_valid}` | `{gates['full_structural_conjunction']}` |",
        "",
        "## Test summaries",
        "",
        "| policy | precision | recall | F1 | exact |",
        "| --- | ---: | ---: | ---: | ---: |",
    ])
    for name, row in sorted(result["test_summary"].items()):
        lines.append(f"| {name} | {row['precision']:.4f} | {row['recall']:.4f} | {row['f1']:.4f} | {row['exact']:.4f} |")
    lines.extend(["", "## Claim boundary", "", str(result["claim_boundary"])])
    return "\n".join(lines) + "\n"


def main() -> None:
    run_final()


if __name__ == "__main__":
    main()
