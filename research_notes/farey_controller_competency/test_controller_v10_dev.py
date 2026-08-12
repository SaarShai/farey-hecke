"""Tests for the predeclared V10 local Farey-defect objective."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from .controller_v10_dev import (
    ACTION_BUDGET,
    ACTION_COUNT,
    FEEDBACK_MODES,
    DefectLinearQ,
    _environment,
    _transmit,
    defect_reward_support,
    local_defect_bin,
    local_defect_reward,
    local_farey_defect,
    run_dev,
    train_lane,
)
from . import controller_v10_dev
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class ControllerV10DevTests(unittest.TestCase):
    @staticmethod
    def task(seed: int, goal: GoalState) -> RepairTask:
        return RepairTask(6, DamagePattern.RANDOM_ISOLATED, goal, seed, 2)

    def tasks(self) -> tuple[RepairTask, ...]:
        return (self.task(1, GoalState.COVERAGE), self.task(2, GoalState.SPECTRAL))

    def test_local_defect_is_visible_and_quantized(self) -> None:
        environment = _environment(self.task(3, GoalState.COVERAGE))
        before = local_farey_defect(environment)
        action = "insert_mediant"
        reward = local_defect_reward(environment, action)
        branch = deepcopy(environment)
        branch.step(action)
        self.assertEqual(reward, before - local_farey_defect(branch))
        self.assertTrue(0 <= local_defect_bin(before) <= 15)
        self.assertEqual(ACTION_COUNT, 18)
        self.assertEqual(ACTION_BUDGET, 16)

    def test_support_diagnostic_is_deterministic_and_predeclared(self) -> None:
        first = defect_reward_support(self.tasks())
        second = defect_reward_support(self.tasks())
        self.assertEqual(first, second)
        self.assertEqual(first["sample_count"], len(self.tasks()) * ACTION_COUNT)
        self.assertGreaterEqual(first["distinct_nonzero_values"], 0)
        self.assertEqual(len(first["by_action"]), ACTION_COUNT)
        self.assertTrue(set(first["by_action"]))

    def test_causal_lagged_null_uses_previous_raw_reward(self) -> None:
        self.assertEqual([_transmit("causal_lagged_null", previous, raw) for previous, raw in ((0.0, 0.2), (0.2, -0.1), (-0.1, 0.3))], [0.0, 0.2, -0.1])
        self.assertNotEqual(_transmit("causal_lagged_null", 0.2, -0.1), _transmit("zero", 0.2, -0.1))

    def test_defect_learner_has_extra_quantized_feature_and_freezes(self) -> None:
        learner = DefectLinearQ(0)
        self.assertEqual(len(learner._weights[0]), 25)
        learner.freeze()
        before = learner.digest()
        self.assertFalse(learner.learning)
        self.assertEqual(before, learner.digest())

    def test_matched_lanes_have_equal_updates_and_reward_distinct_digests(self) -> None:
        tasks = self.tasks()
        lanes = {mode: train_lane(tasks, mode, 0) for mode in FEEDBACK_MODES}
        self.assertEqual({lane.updates for lane in lanes.values()}, {len(tasks) * ACTION_BUDGET})
        self.assertEqual(len({lane.digest for lane in lanes.values()}), 3)
        self.assertNotEqual(lanes["true"].transmitted_reward_digest, lanes["causal_lagged_null"].transmitted_reward_digest)
        self.assertNotEqual(lanes["true"].transmitted_reward_digest, lanes["zero"].transmitted_reward_digest)

    def test_source_declares_no_sealed_accessor_or_hidden_controller_fields(self) -> None:
        source = Path(controller_v10_dev.__file__).read_text(encoding="utf-8")
        for forbidden in ("open_test", "FinalManifestAccess", "_target", "_deleted_points"):
            self.assertNotIn(forbidden, source)

    def test_compact_temp_run_writes_negative_or_unverified_receipt(self) -> None:
        tasks = self.tasks()
        with TemporaryDirectory() as directory:
            result = run_dev(train_tasks=tasks, validation_tasks=tasks, learner_seeds=(0, 1), output_dir=Path(directory))
            receipt = Path(directory) / "controller_v10_dev_receipt.json"
            self.assertTrue(receipt.exists())
            written = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertNotIn("validation_task_rows", written)
            self.assertEqual(written["costs"]["test_openings"], 0)
            self.assertEqual(written["costs"]["test_updates"], 0)
            self.assertEqual(written["support"], result["support"])
            self.assertEqual(receipt.read_text(encoding="utf-8"), json.dumps(written, indent=2, sort_keys=True) + "\n")
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                run_dev(train_tasks=tasks, validation_tasks=tasks, learner_seeds=(0,), output_dir=Path(directory))


if __name__ == "__main__":
    unittest.main()
