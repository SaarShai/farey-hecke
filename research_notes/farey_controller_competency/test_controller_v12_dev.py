"""Tests for the predeclared V12 active-search eligibility-trace objective."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from .controller_v12_dev import (
    ACTION_BUDGET,
    ACTION_COUNT,
    FEEDBACK_MODES,
    INSERTION_ACTIONS,
    MOVEMENT_ACTIONS,
    TRACE_ALPHA,
    TRACE_GAMMA,
    TRACE_LAMBDA,
    TraceLinearQ,
    _environment,
    _transmit,
    V6_ACTIONS,
    active_reward_support,
    active_search_reward,
    local_defect_bin,
    local_farey_defect,
    run_dev,
    train_lane,
)
from . import controller_v12_dev
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class ControllerV12DevTests(unittest.TestCase):
    @staticmethod
    def task(seed: int, goal: GoalState) -> RepairTask:
        return RepairTask(6, DamagePattern.RANDOM_ISOLATED, goal, seed, 2)

    def tasks(self) -> tuple[RepairTask, ...]:
        return (self.task(1, GoalState.COVERAGE), self.task(2, GoalState.SPECTRAL))

    def test_local_defect_is_visible_and_quantized(self) -> None:
        environment = _environment(self.task(3, GoalState.COVERAGE))
        before = local_farey_defect(environment)
        action = "insert_mediant"
        reward = active_search_reward(environment, action)
        branch = deepcopy(environment)
        branch.step(action)
        self.assertAlmostEqual(reward, before - local_farey_defect(branch))
        self.assertTrue(0 <= local_defect_bin(before) <= 15)
        self.assertEqual(ACTION_COUNT, 18)
        self.assertEqual(ACTION_BUDGET, 16)

    def test_movement_and_insertion_sign_semantics(self) -> None:
        task = self.task(1, GoalState.COVERAGE)
        movement_action = next(action for action in MOVEMENT_ACTIONS if abs(active_search_reward(_environment(task), action)) > 1e-12)
        insertion_action = next(action for action in INSERTION_ACTIONS if abs(active_search_reward(_environment(task), action)) > 1e-12)
        for action in (movement_action, insertion_action):
            environment = _environment(task)
            before = local_farey_defect(environment)
            branch = deepcopy(environment)
            branch.step(action)
            delta = local_farey_defect(branch) - before
            expected = delta if action in MOVEMENT_ACTIONS else -delta
            self.assertAlmostEqual(active_search_reward(environment, action), expected)
        self.assertEqual(len(MOVEMENT_ACTIONS) + len(INSERTION_ACTIONS), ACTION_COUNT)

    def test_support_diagnostic_is_deterministic_and_predeclared(self) -> None:
        first = active_reward_support(self.tasks())
        second = active_reward_support(self.tasks())
        self.assertEqual(first, second)
        self.assertEqual(first["sample_count"], len(self.tasks()) * ACTION_COUNT)
        self.assertGreaterEqual(first["distinct_nonzero_values"], 0)
        self.assertEqual(len(first["by_action"]), ACTION_COUNT)
        self.assertTrue(set(first["by_action"]))
        self.assertEqual(set(first["by_family"]), {"movement", "insertion"})
        self.assertGreater(first["by_family"]["movement"]["nonzero_count"], 0)
        self.assertGreater(first["by_family"]["insertion"]["nonzero_count"], 0)

    def test_causal_lagged_null_uses_previous_raw_reward(self) -> None:
        self.assertEqual([_transmit("causal_lagged_null", previous, raw) for previous, raw in ((0.0, 0.2), (0.2, -0.1), (-0.1, 0.3))], [0.0, 0.2, -0.1])
        self.assertNotEqual(_transmit("causal_lagged_null", 0.2, -0.1), _transmit("zero", 0.2, -0.1))

    def test_trace_learner_has_extra_quantized_feature_and_freezes(self) -> None:
        learner = TraceLinearQ(0)
        self.assertEqual(len(learner._weights[0]), 25)
        learner.freeze()
        before = learner.digest()
        self.assertFalse(learner.learning)
        self.assertEqual(before, learner.digest())

    def test_trace_accumulates_decays_and_resets(self) -> None:
        learner = TraceLinearQ(0)
        environment = _environment(self.task(3, GoalState.COVERAGE))
        view = controller_v12_dev._rich_view(environment)
        next_view = controller_v12_dev._rich_view(environment)
        defect_bin = local_defect_bin(local_farey_defect(environment))
        features = learner.features(view, defect_bin)
        zero_digest = learner.trace_digest()
        learner.update(view, defect_bin, "move_left", 0.0, next_view, defect_bin, False)
        first = learner.trace_digest()
        self.assertNotEqual(first, zero_digest)
        move_index = V6_ACTIONS.index("move_left")
        self.assertEqual(tuple(learner._eligibility[move_index]), features)
        learner.update(view, defect_bin, "move_left", 0.0, next_view, defect_bin, False)
        second = learner.trace_digest()
        self.assertNotEqual(second, first)
        self.assertAlmostEqual(learner._eligibility[move_index][0], (1.0 + TRACE_GAMMA * TRACE_LAMBDA) * features[0])
        self.assertEqual(learner.updates, 2)
        learner.update(view, defect_bin, "insert_mediant", 1.0, next_view, defect_bin, True)
        self.assertEqual(learner.trace_digest(), zero_digest)
        self.assertEqual((learner.alpha, learner.gamma, learner.trace_lambda), (TRACE_ALPHA, TRACE_GAMMA, TRACE_LAMBDA))

    def test_matched_lanes_have_equal_updates_and_reward_distinct_digests(self) -> None:
        tasks = self.tasks()
        lanes = {mode: train_lane(tasks, mode, 0) for mode in FEEDBACK_MODES}
        self.assertEqual({lane.updates for lane in lanes.values()}, {len(tasks) * ACTION_BUDGET})
        self.assertEqual(len({lane.digest for lane in lanes.values()}), 3)
        self.assertNotEqual(lanes["true"].transmitted_reward_digest, lanes["causal_lagged_null"].transmitted_reward_digest)
        self.assertNotEqual(lanes["true"].transmitted_reward_digest, lanes["zero"].transmitted_reward_digest)

    def test_source_declares_no_sealed_accessor_or_hidden_controller_fields(self) -> None:
        source = Path(controller_v12_dev.__file__).read_text(encoding="utf-8")
        for forbidden in ("open_test", "FinalManifestAccess", "_target", "_deleted_points"):
            self.assertNotIn(forbidden, source)

    def test_compact_temp_run_writes_negative_or_unverified_receipt(self) -> None:
        tasks = self.tasks()
        with TemporaryDirectory() as directory:
            result = run_dev(train_tasks=tasks, validation_tasks=tasks, learner_seeds=(0, 1), output_dir=Path(directory))
            receipt = Path(directory) / "controller_v12_dev_receipt.json"
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
