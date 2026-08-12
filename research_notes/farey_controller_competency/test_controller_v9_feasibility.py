"""Tests for V9 public-observability feasibility diagnostics."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from .controller_v9_feasibility import (
    ACTION_BUDGET,
    ACTION_COUNT,
    RichView,
    _environment,
    _rich_view,
    _reward_channel,
    collect_public_samples,
    public_history_diagnostic,
    run_probe,
)
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class ControllerV9FeasibilityTests(unittest.TestCase):
    @staticmethod
    def task(seed: int, goal: GoalState) -> RepairTask:
        return RepairTask(6, DamagePattern.RANDOM_ISOLATED, goal, seed, 2)

    def tasks(self) -> tuple[RepairTask, ...]:
        return (
            self.task(1, GoalState.COVERAGE),
            self.task(2, GoalState.SPECTRAL),
        )

    def test_rich_view_is_fixed_width_and_quantized(self) -> None:
        view = RichView((0,) * 8, (0,) * 4, 0, 1.0, (0,) * 4, (0,) * 4, 0)
        self.assertEqual(len(view.as_tuple()), 23)
        self.assertEqual(len(view.features()), 24)
        self.assertEqual(ACTION_COUNT, 18)
        self.assertEqual(ACTION_BUDGET, 16)
        self.assertNotIn("target", view.__dataclass_fields__)
        self.assertNotIn("order", view.__dataclass_fields__)
        self.assertNotIn("fractions", view.__dataclass_fields__)

    def test_history_is_bounded_and_egocentric(self) -> None:
        environment = _environment(self.task(7, GoalState.COVERAGE))
        view = _rich_view(environment, action_history=tuple(range(20)), reward_history=tuple(range(-20, 20)))
        self.assertEqual(len(view.action_history), 4)
        self.assertEqual(len(view.reward_history), 4)
        self.assertTrue(all(0 <= value <= ACTION_COUNT for value in view.action_history))
        self.assertTrue(all(-8 <= value <= 8 for value in view.reward_history))

    def test_public_history_diagnostic_is_deterministic_and_target_independent(self) -> None:
        first = public_history_diagnostic(self.tasks())
        second = public_history_diagnostic(self.tasks())
        self.assertEqual(first, second)
        self.assertEqual(first["sample_count"], len(self.tasks()) * ACTION_BUDGET)
        self.assertGreaterEqual(first["collision_rate"], 0.0)
        self.assertLessEqual(first["collision_rate"], 1.0)
        self.assertGreaterEqual(first["public_history_action_ceiling"], 0.0)
        self.assertLessEqual(first["public_history_action_ceiling"], 1.0)
        self.assertGreaterEqual(first["action_value_auc"], 0.0)
        self.assertLessEqual(first["action_value_auc"], 1.0)
        self.assertGreater(first["action_value_pair_count"], 0)

    def test_counterfactual_action_values_have_fixed_public_width(self) -> None:
        samples = collect_public_samples(self.tasks()[:1])
        self.assertEqual(len(samples), ACTION_BUDGET)
        self.assertTrue(all(len(sample.action_values) == ACTION_COUNT for sample in samples))
        self.assertTrue(all(isinstance(value, float) for sample in samples for value in sample.action_values))

    def test_source_has_no_sealed_accessor_or_exact_view_fields(self) -> None:
        source = Path(__file__).with_name("controller_v9_feasibility.py").read_text(encoding="utf-8")
        self.assertNotIn("open_test", source)
        self.assertNotIn("FinalManifestAccess", source)
        view_fields = set(RichView.__dataclass_fields__)
        self.assertTrue(view_fields.isdisjoint({"target", "mask", "order", "fractions", "N"}))

    def test_action_history_ids_are_bounded_to_the_fixed_vocabulary(self) -> None:
        environment = _environment(self.task(8, GoalState.SPECTRAL))
        view = _rich_view(environment, action_history=(0, 1, 18, 99), reward_history=(-9, -1, 0, 9))
        self.assertEqual(view.action_history, (0, 1, 18, ACTION_COUNT))
        self.assertEqual(view.reward_history, (-8, -1, 0, 8))

    def test_causal_lagged_null_uses_previous_raw_reward(self) -> None:
        previous_raw = 0.0
        transmitted = []
        for raw in (0.2, -0.1, 0.3):
            transmitted.append(_reward_channel("causal_lagged_null", previous_raw, raw))
            previous_raw = raw
        self.assertEqual(transmitted, [0.0, 0.2, -0.1])
        self.assertNotEqual(transmitted, [0.0, 0.0, 0.0])

    def test_feasibility_probe_writes_compact_deterministic_receipt(self) -> None:
        tasks = self.tasks()
        with TemporaryDirectory() as directory:
            result = run_probe(
                train_tasks=tasks,
                validation_tasks=tasks,
                learner_seeds=(0, 1),
                output_dir=Path(directory),
            )
            receipt_path = Path(directory) / "controller_v9_feasibility_receipt.json"
            self.assertTrue(receipt_path.exists())
            self.assertTrue((Path(directory) / "V9_FEASIBILITY_RESULTS.md").exists())
            written = json.loads(receipt_path.read_text(encoding="utf-8"))
            self.assertNotIn("validation_task_rows", written)
            self.assertEqual(written["costs"]["test_openings"], 0)
            self.assertEqual(written["costs"]["test_updates"], 0)
            self.assertEqual(written["observability"], result["observability"])
            self.assertEqual(receipt_path.read_text(encoding="utf-8"), json.dumps(written, indent=2, sort_keys=True) + "\n")
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                run_probe(train_tasks=tasks, validation_tasks=tasks, learner_seeds=(0,), output_dir=Path(directory))


if __name__ == "__main__":
    unittest.main()
