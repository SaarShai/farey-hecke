#!/usr/bin/env python3
"""V6 final-manifest seal, access protocol, and evaluator-only feasibility audit.

V5 fixed the generic interface before this manifest was generated: eighteen
target-independent actions, a sixteen-step budget, and exact-recovery gates of
0.90 overall and 0.80 in every order-by-family-by-goal cell.  V6 now seals a
fresh manifest on disjoint orders and seeds, runs the exact V5 d=2
shortest-path evaluator before any learner access, and records a leak-tight
train/validation/test access protocol.

This module deliberately does not train or evaluate a controller.  Training
may construct only train tasks; validation access requires the exact
preregistered model-selection purpose; test access is one-shot and requires a
frozen model digest plus an evaluator-issued token.  The V6 manifest is the
only candidate for a later final controller experiment.  The retired V4/V5
task set is never reused here.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import re
import statistics
from typing import Any, Sequence

try:  # Package import.
    from .competency_v4_sealed_manifest import seal_manifests as seal_v4_manifests
    from .competency_v5_feasibility import (
        ACTION_BUDGET,
        ACTION_VOCABULARY,
        MOVEMENT_ACTIONS,
        INSERTION_ACTIONS,
        _insert_transition,
        _movement_offset,
        shortest_exact_recovery,
    )
    from .repair_experiment import RepairTask, make_manifest
    from .strict_environment import DamagePattern, GoalState, StrictEnvironment, _round_reward
except ImportError:  # Direct script execution from this directory.
    from competency_v4_sealed_manifest import seal_manifests as seal_v4_manifests  # type: ignore[no-redef]
    from competency_v5_feasibility import (  # type: ignore[no-redef]
        ACTION_BUDGET,
        ACTION_VOCABULARY,
        MOVEMENT_ACTIONS,
        INSERTION_ACTIONS,
        _insert_transition,
        _movement_offset,
        shortest_exact_recovery,
    )
    from repair_experiment import RepairTask, make_manifest  # type: ignore[no-redef]
    from strict_environment import DamagePattern, GoalState, StrictEnvironment, _round_reward  # type: ignore[no-redef]


ROOT_SEED = 20261001
TRAIN_ORDERS = (10, 13, 16, 19)
VALIDATION_ORDERS = (22, 26)
TEST_ORDERS = (28, 36, 52)
SPLIT_ORDERS = {
    "train": TRAIN_ORDERS,
    "validation": VALIDATION_ORDERS,
    "test": TEST_ORDERS,
}
PATTERNS = (
    DamagePattern.RANDOM_ISOLATED,
    DamagePattern.BURST,
    DamagePattern.DENOMINATOR_BIASED,
)
GOALS = (GoalState.COVERAGE, GoalState.SPECTRAL)
SPLIT_REPLICATES = {"train": 10, "validation": 10, "test": 20}
DAMAGE_COUNT = 2
TASK_COUNT = 720
PUBLIC_FIELDS = ("task_id", "split", "trusted_goal")
FORBIDDEN_PUBLIC_FIELDS = (
    "order",
    "pattern",
    "goal",
    "seed",
    "damage_count",
    "fractions",
    "target",
    "deleted_indices",
    "deleted_points",
    "mask",
)
PRIVATE_FIELDS = (
    "task_id",
    "split",
    "order",
    "pattern",
    "goal",
    "seed",
    "damage_count",
    "deleted_indices",
    "target_sha256",
    "damage_mask_sha256",
)
EXACT_RECOVERY_THRESHOLD = 0.90
CELL_RECOVERY_THRESHOLD = 0.80
VALIDATION_PURPOSE = "preregistered_model_selection"
MODEL_DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")

# Earlier development and retired V4/V5 orders.  V6 must never overlap them.
DEVELOPMENT_ORDERS = (6, 8, 11)
RETIRED_V4_ORDERS = (7, 9, 12, 15, 18, 20, 24, 32, 48)
V4_RECEIPT_NAME = "competency_v4_sealed_manifest_receipt.json"
V4_RECEIPT_SHA256 = "aaeebebb8a95770a9919f1a627faf4a703e4dd9ff6c60a65bab24c0b169ec474"
V4_PRIVATE_MANIFEST_SHA256 = "e9ffa6077c116615d2061421f3e222f9d85ffab70e7eacadba1f5411f2c76d31"
V4_PUBLIC_MANIFEST_SHA256 = "16451545b25dbedc44d47a57dcca2583c108d1b06dd88dc7dc5acfb25df2ede6"
V4_DEVELOPMENT_SEED = 20260811
V4_DEVELOPMENT_REPLICATES = 1
PUBLIC_CLAIM_BOUNDARY = (
    "V6 is a sealed final-manifest and evaluator-only feasibility audit. No "
    "controller was trained or evaluated. The retired V4/V5 task set is "
    "permanently excluded; this fresh V6 manifest is the only candidate for a "
    "later controller run."
)


@dataclass(frozen=True, slots=True)
class V6Config:
    """Locked V6 manifest identity, action budget, and feasibility gates."""

    root_seed: int = ROOT_SEED
    action_budget: int = ACTION_BUDGET
    damage_count: int = DAMAGE_COUNT
    exact_recovery_threshold: float = EXACT_RECOVERY_THRESHOLD
    cell_recovery_threshold: float = CELL_RECOVERY_THRESHOLD

    def __post_init__(self) -> None:
        if self.root_seed != ROOT_SEED:
            raise ValueError("V6 root seed is sealed before evaluation")
        if self.action_budget != ACTION_BUDGET:
            raise ValueError("V6 action budget is inherited from the frozen V5 interface")
        if self.damage_count != DAMAGE_COUNT:
            raise ValueError("V6 uses two hidden deletions")
        if self.exact_recovery_threshold != EXACT_RECOVERY_THRESHOLD:
            raise ValueError("V6 overall threshold is sealed before evaluation")
        if self.cell_recovery_threshold != CELL_RECOVERY_THRESHOLD:
            raise ValueError("V6 per-cell threshold is sealed before evaluation")


DEFAULT_CONFIG = V6Config()


class AccessProtocolError(RuntimeError):
    """Raised when a caller violates the sealed manifest access protocol."""


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def _digest(value: Any) -> str:
    return sha256(_canonical(value)).hexdigest()


def _split_seed(split: str, config: V6Config) -> int:
    salts = {"train": 0x1A2B3C4D, "validation": 0x5E6F7081, "test": 0x92A3B4C5}
    return config.root_seed ^ salts[split]


def _private_rows(tasks_by_split: dict[str, Sequence[RepairTask]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "test"):
        for index, task in enumerate(tasks_by_split[split]):
            environment = StrictEnvironment(
                task.order,
                task.pattern,
                damage_count=task.damage_count,
                seed=task.seed,
                rotation=True,
                action_budget=ACTION_BUDGET,
                goal=task.goal,
            )
            target_serialized = [str(point) for point in environment._target]
            deleted_indices = list(environment._deleted_indices)
            target_sha256 = _digest(target_serialized)
            damage_mask_sha256 = _digest(
                {"target_sha256": target_sha256, "deleted_indices": deleted_indices}
            )
            rows.append(
                {
                    "task_id": f"{split}-{index:03d}",
                    "split": split,
                    "order": task.order,
                    "pattern": task.pattern.value,
                    "goal": task.goal.value,
                    "seed": task.seed,
                    "damage_count": task.damage_count,
                    "deleted_indices": deleted_indices,
                    "target_sha256": target_sha256,
                    "damage_mask_sha256": damage_mask_sha256,
                }
            )
    return rows


def _public_rows(private_rows: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"task_id": row["task_id"], "split": row["split"], "trusted_goal": row["goal"]}
        for row in private_rows
    ]


def _retired_seed_set() -> set[int]:
    """Collect seeds from V4 private rows and its development generator."""

    receipt_path = Path(__file__).parent / V4_RECEIPT_NAME
    receipt_bytes = receipt_path.read_bytes()
    if sha256(receipt_bytes).hexdigest() != V4_RECEIPT_SHA256:
        raise RuntimeError("retired V4 receipt changed; V6 must not regenerate against it")
    receipt = json.loads(receipt_bytes)
    if receipt["manifest_seal"]["private_sha256"] != V4_PRIVATE_MANIFEST_SHA256:
        raise RuntimeError("retired V4 private manifest hash changed")
    if receipt["manifest_seal"]["public_sha256"] != V4_PUBLIC_MANIFEST_SHA256:
        raise RuntimeError("retired V4 public manifest hash changed")
    # Commitment rows intentionally omit seed; reconstruct the deterministic
    # retired V4 tasks and verify their hashes above before collecting seeds.
    v4_manifest = seal_v4_manifests()
    if (
        v4_manifest["private_hash"] != V4_PRIVATE_MANIFEST_SHA256
        or v4_manifest["public_hash"] != V4_PUBLIC_MANIFEST_SHA256
    ):
        raise RuntimeError("deterministic V4 reconstruction does not match the pinned receipt")
    retired = {
        task.seed
        for tasks in v4_manifest["tasks_by_split"].values()
        for task in tasks
    }
    development_tasks = make_manifest(
        DEVELOPMENT_ORDERS,
        PATTERNS,
        damage_count=DAMAGE_COUNT,
        replicates=V4_DEVELOPMENT_REPLICATES,
        seed=V4_DEVELOPMENT_SEED,
    )
    retired.update(task.seed for task in development_tasks)
    return retired


def seal_manifest(config: V6Config = DEFAULT_CONFIG) -> dict[str, Any]:
    """Generate and seal the fresh V6 manifest exactly once per deterministic run."""

    if set().union(*SPLIT_ORDERS.values()) & set(DEVELOPMENT_ORDERS + RETIRED_V4_ORDERS):
        raise RuntimeError("V6 orders overlap a retired development order")
    tasks_by_split = {
        split: make_manifest(
            orders,
            PATTERNS,
            damage_count=config.damage_count,
            replicates=SPLIT_REPLICATES[split],
            seed=_split_seed(split, config),
        )
        for split, orders in SPLIT_ORDERS.items()
    }
    private_rows = _private_rows(tasks_by_split)
    public_rows = _public_rows(private_rows)
    all_seeds = [row["seed"] for row in private_rows]
    retired_seeds = _retired_seed_set()
    if set(all_seeds) & retired_seeds:
        raise RuntimeError("V6 task seeds overlap retired V4/development seeds")
    if len(all_seeds) != len(set(all_seeds)):
        raise RuntimeError("V6 task seeds are not unique")
    expected_count = sum(
        len(SPLIT_ORDERS[split]) * len(PATTERNS) * len(GOALS) * SPLIT_REPLICATES[split]
        for split in SPLIT_ORDERS
    )
    if expected_count != TASK_COUNT or len(private_rows) != TASK_COUNT:
        raise RuntimeError("V6 manifest count mismatch")
    public_schema = {
        "fields": list(PUBLIC_FIELDS),
        "forbidden_fields": list(FORBIDDEN_PUBLIC_FIELDS),
        "controller_visible_goal": True,
        "exact_fractions_included": False,
        "deletion_masks_included": False,
    }
    private_schema = {
        "fields": list(PRIVATE_FIELDS),
        "exact_fractions_included": False,
        "deletion_masks_included": True,
        "target_commitments_included": True,
    }
    task_commitments = [
        {"task_id": row["task_id"], "commitment_sha256": _digest(row)} for row in private_rows
    ]
    return {
        "config": {
            "root_seed": config.root_seed,
            "split_orders": {split: list(orders) for split, orders in SPLIT_ORDERS.items()},
            "patterns": [pattern.value for pattern in PATTERNS],
            "goals": [goal.value for goal in GOALS],
            "split_replicates": dict(SPLIT_REPLICATES),
            "damage_count": config.damage_count,
            "action_budget": config.action_budget,
        },
        "tasks_by_split": tasks_by_split,
        "private_rows": private_rows,
        "public_rows": public_rows,
        "public_schema": public_schema,
        "private_schema": private_schema,
        "public_hash": _digest({"schema": public_schema, "rows": public_rows}),
        "private_hash": _digest({"schema": private_schema, "rows": private_rows}),
        "task_commitments": task_commitments,
        "retired_order_disjoint": True,
        "retired_seed_overlap_check": True,
    }


def _validate_model_digest(model_digest: str) -> None:
    if not isinstance(model_digest, str) or not MODEL_DIGEST_PATTERN.fullmatch(model_digest):
        raise AccessProtocolError("frozen model digest must be sha256:<64 lowercase hex characters>")


def _opening_token(private_manifest_sha256: str, model_digest: str) -> str:
    return _digest(
        {
            "manifest_private_sha256": private_manifest_sha256,
            "model_digest": model_digest,
            "purpose": "v6_one_shot_test_opening",
        }
    )


class FinalManifestAccess:
    """Leak-tight access adapter for the sealed V6 evaluator manifest."""

    def __init__(self, manifest: dict[str, Any]) -> None:
        self._manifest = manifest
        self._model_digest: str | None = None
        self._test_opened = False
        self._token_issued = False
        self._events: list[dict[str, Any]] = []
        self.test_updates = 0

    def training_tasks(self) -> tuple[RepairTask, ...]:
        if self._model_digest is not None:
            raise AccessProtocolError("training access closes when the model is frozen")
        tasks = tuple(self._manifest["tasks_by_split"]["train"])
        self._events.append({"operation": "training", "task_count": len(tasks)})
        return tasks

    def validation_tasks(self, *, purpose: str) -> tuple[RepairTask, ...]:
        if purpose != VALIDATION_PURPOSE:
            raise AccessProtocolError("validation is available only for preregistered model selection")
        if self._model_digest is not None:
            raise AccessProtocolError("validation access closes when the model is frozen")
        tasks = tuple(self._manifest["tasks_by_split"]["validation"])
        self._events.append({"operation": "validation", "purpose": purpose, "task_count": len(tasks)})
        return tasks

    def freeze_model(self, model_digest: str) -> str:
        _validate_model_digest(model_digest)
        if self._test_opened:
            raise AccessProtocolError("the one-shot test opening has already occurred")
        if self._model_digest is not None and self._model_digest != model_digest:
            raise AccessProtocolError("model digest is already frozen to a different value")
        self._model_digest = model_digest
        token = _opening_token(self._manifest["private_hash"], model_digest)
        self._token_issued = True
        self._events.append({"operation": "freeze_model", "model_digest": model_digest})
        return token

    def open_test(self, *, frozen_model_digest: str, opening_token: str) -> tuple[RepairTask, ...]:
        _validate_model_digest(frozen_model_digest)
        if self._test_opened:
            raise AccessProtocolError("test access is one-shot")
        if self._model_digest != frozen_model_digest:
            raise AccessProtocolError("test access requires the previously frozen model digest")
        expected = _opening_token(self._manifest["private_hash"], frozen_model_digest)
        if opening_token != expected:
            raise AccessProtocolError("test opening token does not match the sealed manifest and model")
        self._test_opened = True
        tasks = tuple(self._manifest["tasks_by_split"]["test"])
        self._events.append({"operation": "test_open", "task_count": len(tasks), "test_updates": 0})
        return tasks

    def audit_snapshot(self) -> dict[str, Any]:
        return {
            "events": list(self._events),
            "test_openings": int(self._test_opened),
            "test_updates": self.test_updates,
            "model_frozen": self._model_digest is not None,
            "token_issued": self._token_issued,
        }


def exact_feasibility_audit(manifest: dict[str, Any], config: V6Config = DEFAULT_CONFIG) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "test"):
        for index, task in enumerate(manifest["tasks_by_split"][split]):
            result = shortest_exact_recovery(task)
            rows.append(
                {
                    "task_id": f"{split}-{index:03d}",
                    "split": split,
                    "order": task.order,
                    "pattern": task.pattern.value,
                    "goal": task.goal.value,
                    "seed": task.seed,
                    **result,
                }
            )
    reachable = [row for row in rows if row["reachable_within_budget"]]
    overall_fraction = len(reachable) / len(rows) if rows else 0.0
    cells: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = f"N{row['order']}:{row['pattern']}:{row['goal']}"
        cell = cells.setdefault(key, {"task_count": 0, "reachable_count": 0, "reachable_fraction": 0.0})
        cell["task_count"] += 1
        cell["reachable_count"] += int(row["reachable_within_budget"])
    for cell in cells.values():
        cell["reachable_fraction"] = cell["reachable_count"] / cell["task_count"]
    lengths = sorted(row["min_actions"] for row in reachable if row["min_actions"] is not None)

    def quantile(q: float) -> float | None:
        if not lengths:
            return None
        position = q * (len(lengths) - 1)
        lower = int(position)
        upper = min(len(lengths) - 1, lower + 1)
        return lengths[lower] + (position - lower) * (lengths[upper] - lengths[lower])

    minimum_cell_fraction = min((cell["reachable_fraction"] for cell in cells.values()), default=0.0)
    overall_status = overall_fraction >= config.exact_recovery_threshold
    cell_status = minimum_cell_fraction >= config.cell_recovery_threshold
    return {
        "action_budget": ACTION_BUDGET,
        "action_vocabulary": list(ACTION_VOCABULARY),
        "action_count": len(ACTION_VOCABULARY),
        "damage_count": DAMAGE_COUNT,
        "search": "exact V5 shortest movement BFS plus both deleted-target insertion orders",
        "tasks": rows,
        "task_count": len(rows),
        "reachable_within_budget_count": len(reachable),
        "reachable_within_budget_fraction": overall_fraction,
        "unreachable_within_budget_count": len(rows) - len(reachable),
        "cell_summary": cells,
        "minimum_cell_reachable_fraction": minimum_cell_fraction,
        "action_length_summary": {
            "count": len(lengths),
            "min": min(lengths) if lengths else None,
            "q25": quantile(0.25),
            "median": quantile(0.50),
            "q75": quantile(0.75),
            "q90": quantile(0.90),
            "max": max(lengths) if lengths else None,
        },
        "gates": {
            "overall": {
                "status": "positive" if overall_status else "negative",
                "reachable_fraction": overall_fraction,
                "threshold": config.exact_recovery_threshold,
            },
            "per_cell": {
                "status": "positive" if cell_status else "negative",
                "minimum_cell_fraction": minimum_cell_fraction,
                "threshold": config.cell_recovery_threshold,
                "cell_count": len(cells),
            },
            "combined": {
                "status": "positive" if overall_status and cell_status else "negative",
                "reason": "both overall and every order-by-family-by-goal cell gate are required",
            },
        },
    }


def _identity_reward_record(task: RepairTask, action: str) -> tuple[bool, float, float]:
    environment = StrictEnvironment(
        task.order,
        task.pattern,
        damage_count=task.damage_count,
        seed=task.seed,
        rotation=True,
        action_budget=ACTION_BUDGET,
        goal=task.goal,
    )
    points = tuple(environment._initial_points)
    cursor = int(environment._initial_cursor)
    before_metric = environment._goal_metric(points)
    deleted = set(environment._target) - set(environment._initial_points)
    before_identity = len(set(points) & deleted)
    if action in MOVEMENT_ACTIONS:
        child_points = points
    else:
        child_points, _child_cursor, _added = _insert_transition(points, cursor, action)
    after_metric = environment._goal_metric(child_points)
    after_identity = len(set(child_points) & deleted)
    identity_delta = float(after_identity - before_identity)
    return identity_delta > 0.0, float(_round_reward(before_metric - after_metric)), identity_delta


def _auc(scores: Sequence[float], labels: Sequence[bool]) -> float:
    positive = [score for score, label in zip(scores, labels) if label]
    negative = [score for score, label in zip(scores, labels) if not label]
    if not positive or not negative:
        return 0.5
    wins = sum(
        1.0 if left > right else 0.5 if left == right else 0.0
        for left in positive
        for right in negative
    )
    return wins / (len(positive) * len(negative))


def visible_reward_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for split in ("train", "validation", "test"):
        for task in manifest["tasks_by_split"][split]:
            for action in ACTION_VOCABULARY:
                identity_improving, reward, identity_delta = _identity_reward_record(task, action)
                records.append(
                    {
                        "split": split,
                        "goal": task.goal.value,
                        "action": action,
                        "reward": reward,
                        "identity_improving": identity_improving,
                        "identity_delta": identity_delta,
                    }
                )
    scores = [row["reward"] for row in records]
    labels = [row["identity_improving"] for row in records]
    positive = [row["reward"] for row in records if row["identity_improving"]]
    negative = [row["reward"] for row in records if not row["identity_improving"]]
    return {
        "samples": len(records),
        "improving_actions": len(positive),
        "non_improving_actions": len(negative),
        "auc": _auc(scores, labels),
        "mean_reward_improving": statistics.fmean(positive) if positive else 0.0,
        "mean_reward_non_improving": statistics.fmean(negative) if negative else 0.0,
        "reward_definition": "target-independent coverage/spectral scalar change",
        "hidden_identity_used_in_reward": False,
        "records_digest": _digest(records),
    }


def public_leakage_probe(manifest: dict[str, Any]) -> dict[str, Any]:
    rows = manifest["public_rows"]
    bad_key_rows = [row["task_id"] for row in rows if set(row) != set(PUBLIC_FIELDS)]
    forbidden_value_rows = [
        row["task_id"]
        for row in rows
        if any(field in row for field in FORBIDDEN_PUBLIC_FIELDS)
    ]
    invalid_goals = [
        row["task_id"] for row in rows if row["trusted_goal"] not in {goal.value for goal in GOALS}
    ]
    return {
        "rows": len(rows),
        "public_fields": list(PUBLIC_FIELDS),
        "bad_key_row_count": len(bad_key_rows),
        "forbidden_value_row_count": len(forbidden_value_rows),
        "invalid_goal_row_count": len(invalid_goals),
        "status": "pass" if not (bad_key_rows or forbidden_value_rows or invalid_goals) else "fail",
        "public_rows_digest": _digest(rows),
    }


def access_protocol_probe(manifest: dict[str, Any]) -> dict[str, Any]:
    """Exercise protocol behavior on a separate evaluator-only probe.

    The controller-facing accessor is instantiated separately and remains
    unopened, unfrozen, and token-free.  Only the evaluator feasibility probe
    consumes its synthetic one-shot opening to verify the guard behavior.
    """

    evaluator_adapter = FinalManifestAccess(manifest)
    train_count = len(evaluator_adapter.training_tasks())
    validation_count = len(evaluator_adapter.validation_tasks(purpose=VALIDATION_PURPOSE))
    probe_digest = "sha256:" + sha256(b"v6-access-protocol-probe").hexdigest()
    token = evaluator_adapter.freeze_model(probe_digest)
    test_count = len(evaluator_adapter.open_test(frozen_model_digest=probe_digest, opening_token=token))
    evaluator_snapshot = evaluator_adapter.audit_snapshot()
    controller_adapter = FinalManifestAccess(manifest)
    controller_snapshot = controller_adapter.audit_snapshot()
    return {
        "evaluator_feasibility_access": {
            "training_task_count": train_count,
            "validation_task_count": validation_count,
            "test_task_count": test_count,
            "validation_purpose": VALIDATION_PURPOSE,
            "test_openings": evaluator_snapshot["test_openings"],
            "test_updates": evaluator_snapshot["test_updates"],
            "model_frozen": evaluator_snapshot["model_frozen"],
            "one_shot_test_opening": evaluator_snapshot["test_openings"] == 1,
        },
        "controller_test_accessor": {
            "test_openings": controller_snapshot["test_openings"],
            "test_updates": controller_snapshot["test_updates"],
            "model_frozen": controller_snapshot["model_frozen"],
            "token_issued": controller_snapshot["token_issued"],
            "status": "sealed_until_frozen_model",
        },
        "test_token_sha256": sha256(token.encode("ascii")).hexdigest(),
        "evaluator_events": evaluator_snapshot["events"],
    }


def run_audit(config: V6Config = DEFAULT_CONFIG) -> dict[str, Any]:
    manifest = seal_manifest(config)
    # Exact feasibility is intentionally computed before any access adapter is
    # exercised, so a failed gate can halt a learner run before train access.
    reachability = exact_feasibility_audit(manifest, config)
    reward = visible_reward_audit(manifest)
    leakage = public_leakage_probe(manifest)
    access = access_protocol_probe(manifest)
    eligible = reachability["gates"]["combined"]["status"] == "positive"
    return {
        "schema_version": 1,
        "experiment": "V6 sealed final-manifest evaluator-only feasibility audit",
        "provenance": {
            "command": "PYTHONDONTWRITEBYTECODE=1 python3 research_notes/farey_controller_competency/competency_v6_final_manifest.py",
            "controller_training": False,
            "controller_evaluated": False,
            "learner_created": False,
            "exact_feasibility_before_access": True,
            "manifest_sealed_once_before_learner": True,
        },
        "manifest_seal": {
            "config": manifest["config"],
            "public_schema": manifest["public_schema"],
            "private_schema": manifest["private_schema"],
            "public_sha256": manifest["public_hash"],
            "private_sha256": manifest["private_hash"],
            "public_row_count": len(manifest["public_rows"]),
            "private_row_count": len(manifest["private_rows"]),
            "task_commitments": manifest["task_commitments"],
            "generator_module": Path(__file__).name,
            "retired_order_disjoint": manifest["retired_order_disjoint"],
            "retired_seed_overlap_check": manifest["retired_seed_overlap_check"],
            "public_access_policy": {
                "training": "train_split_only",
                "validation": VALIDATION_PURPOSE,
                "test": "one_shot_after_frozen_model_digest_and_token",
            },
            "training_eligibility": "eligible_for_later_controller_run" if eligible else "ineligible_failed_feasibility_gate",
        },
        "retired_v4": {
            "receipt_name": V4_RECEIPT_NAME,
            "receipt_sha256": V4_RECEIPT_SHA256,
            "private_manifest_sha256": V4_PRIVATE_MANIFEST_SHA256,
            "public_manifest_sha256": V4_PUBLIC_MANIFEST_SHA256,
            "orders": list(DEVELOPMENT_ORDERS + RETIRED_V4_ORDERS),
            "permanently_excluded": True,
        },
        "reachability": reachability,
        "visible_reward": reward,
        "public_leakage": leakage,
        "access_protocol": access,
        "negative_fixtures": {
            "constant_reward_auc": 0.5,
            "constant_reward_status": "negative",
            "public_schema_forbidden_field_status": "negative" if FORBIDDEN_PUBLIC_FIELDS[0] in PUBLIC_FIELDS else "positive",
        },
        "claim_boundary": PUBLIC_CLAIM_BOUNDARY,
    }


def _source_hashes() -> dict[str, str]:
    directory = Path(__file__).parent
    names = (
        "competency_v6_final_manifest.py",
        "competency_v5_feasibility.py",
        "competency_v4_sealed_manifest_receipt.json",
        "repair_experiment.py",
        "strict_environment.py",
        "test_competency_v6_final_manifest.py",
    )
    return {
        name: sha256((directory / name).read_bytes()).hexdigest()
        for name in names
        if (directory / name).exists()
    }


def _fmt(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.4f}"


def result_markdown(result: dict[str, Any]) -> str:
    seal = result["manifest_seal"]
    reach = result["reachability"]
    length = reach["action_length_summary"]
    gate = reach["gates"]
    lines = [
        "# V6 sealed final-manifest feasibility audit",
        "",
        PUBLIC_CLAIM_BOUNDARY,
        "",
        f"Private manifest SHA256: `{seal['private_sha256']}`; public schema SHA256: `{seal['public_sha256']}`; rows: `{seal['private_row_count']}`.",
        "",
        "## Fresh disjoint manifest",
        "",
        "| split | orders | rows |",
        "| --- | --- | ---: |",
        "| train | 10, 13, 16, 19 | 240 |",
        "| validation | 22, 26 | 120 |",
        "| test | 28, 36, 52 | 360 |",
        "",
        "The V4/V5 development orders and task seeds were checked for disjointness before evaluation.",
        "",
        "## Exact V5 feasibility",
        "",
        f"Action vocabulary: `{reach['action_vocabulary']}`; budget: `{reach['action_budget']}`; d=`{reach['damage_count']}`.",
        f"Reachable within budget: `{reach['reachable_within_budget_count']}/{reach['task_count']}` ({reach['reachable_within_budget_fraction']:.4f}); unreachable: `{reach['unreachable_within_budget_count']}`.",
        f"Action lengths: min=`{length['min']}`, q25=`{_fmt(length['q25'])}`, median=`{_fmt(length['median'])}`, q75=`{_fmt(length['q75'])}`, q90=`{_fmt(length['q90'])}`, max=`{length['max']}`.",
        "",
        "| gate | status | observed | threshold |",
        "| --- | --- | ---: | ---: |",
        f"| overall exact recovery | `{gate['overall']['status']}` | {gate['overall']['reachable_fraction']:.4f} | {gate['overall']['threshold']:.2f} |",
        f"| every N×family×goal cell | `{gate['per_cell']['status']}` | {gate['per_cell']['minimum_cell_fraction']:.4f} minimum | {gate['per_cell']['threshold']:.2f} |",
        f"| combined | `{gate['combined']['status']}` | — | both required |",
        "",
        "## Access protocol",
        "",
        "Training can construct only train tasks. Validation requires the literal preregistered model-selection purpose. The evaluator-only feasibility probe verifies one-shot test opening after a frozen `sha256:<digest>` and matching token; the controller-facing test accessor remains unopened until a real frozen-model run.",
        f"Evaluator feasibility probe: train=`{result['access_protocol']['evaluator_feasibility_access']['training_task_count']}`, validation=`{result['access_protocol']['evaluator_feasibility_access']['validation_task_count']}`, test=`{result['access_protocol']['evaluator_feasibility_access']['test_task_count']}`; one-shot openings=`{result['access_protocol']['evaluator_feasibility_access']['test_openings']}`; test updates=`{result['access_protocol']['evaluator_feasibility_access']['test_updates']}`.",
        f"Controller test accessor: openings=`{result['access_protocol']['controller_test_accessor']['test_openings']}`, token issued=`{result['access_protocol']['controller_test_accessor']['token_issued']}`, test updates=`{result['access_protocol']['controller_test_accessor']['test_updates']}`; status=`{result['access_protocol']['controller_test_accessor']['status']}`.",
        "",
        "## Reward and leakage probes",
        "",
        f"Visible target-independent scalar reward AUC versus evaluator-only identity improvement: `{result['visible_reward']['auc']:.4f}` over `{result['visible_reward']['samples']}` records; hidden identity was not used in reward.",
        f"Public schema probe: `{result['public_leakage']['status']}`; bad-key rows=`{result['public_leakage']['bad_key_row_count']}`, forbidden-value rows=`{result['public_leakage']['forbidden_value_row_count']}`.",
        "",
        "## Claim boundary",
        "",
        PUBLIC_CLAIM_BOUNDARY,
        "",
    ]
    return "\n".join(lines)


def write_outputs(result: dict[str, Any]) -> None:
    directory = Path(__file__).parent
    result["source_hashes"] = _source_hashes()
    result["generator_sha256"] = result["source_hashes"].get(Path(__file__).name)
    (directory / "competency_v6_final_manifest_receipt.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (directory / "V6_FINAL_MANIFEST_RESULTS.md").write_text(result_markdown(result), encoding="utf-8")


def main() -> None:
    result = run_audit()
    write_outputs(result)
    print("wrote competency_v6_final_manifest_receipt.json and V6_FINAL_MANIFEST_RESULTS.md")
    print(
        f"reachable={result['reachability']['reachable_within_budget_count']}/{result['reachability']['task_count']}, "
        f"gate={result['reachability']['gates']['combined']['status']}, "
        f"eligible={result['manifest_seal']['training_eligibility']}"
    )


if __name__ == "__main__":
    main()
