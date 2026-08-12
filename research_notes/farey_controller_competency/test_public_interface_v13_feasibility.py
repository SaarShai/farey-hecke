"""Tests for the V13 public-interface feasibility probe."""

from __future__ import annotations

import inspect
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from .public_interface_v13_feasibility import (
    ACTION_COUNT,
    ACTION_BUDGET,
    SIGNALS,
    _environment,
    V6_ACTIONS,
    public_signal_values,
    collect_samples,
    leakage_audit,
    public_view,
    run_probe,
    split_diagnostic,
)
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class PublicInterfaceV13Tests(unittest.TestCase):
    @staticmethod
    def task(seed: int, goal: GoalState) -> RepairTask:
        return RepairTask(6, DamagePattern.RANDOM_ISOLATED, goal, seed, 2)

    def tasks(self) -> tuple[RepairTask, ...]:
        return (self.task(1, GoalState.COVERAGE), self.task(2, GoalState.SPECTRAL))

    def test_public_view_is_fixed_width_and_has_no_hidden_fields(self) -> None:
        view = public_view(_environment(self.task(3, GoalState.COVERAGE)))
        self.assertEqual(len(view.as_tuple()), 23)
        serialized = view.serialize()
        self.assertEqual(len(serialized), 7)
        self.assertFalse(any(token in key.lower() for key in serialized for token in ("target", "order", "mask", "deleted", "survivor")))
        self.assertTrue(leakage_audit()["passed"])

    def test_public_signals_are_action_wide_and_do_not_mutate_state(self) -> None:
        environment = _environment(self.task(4, GoalState.COVERAGE))
        before = (tuple(environment._points), environment._cursor, environment._remaining)
        for action in V6_ACTIONS:
            values = public_signal_values(environment, action)
            self.assertEqual(set(values), set(SIGNALS))
            self.assertEqual(len(values), 4)
        self.assertEqual(before, (tuple(environment._points), environment._cursor, environment._remaining))

    def test_hidden_values_are_not_in_serialized_public_view(self) -> None:
        sample = collect_samples(self.tasks())[0]
        view_blob = json.dumps(sample.view_key)
        self.assertEqual(len(sample.hidden_values), ACTION_COUNT)
        self.assertNotIn("hidden", view_blob.lower())
        self.assertNotIn("target", view_blob.lower())

    def test_diagnostics_are_deterministic_and_have_train_validation_shape(self) -> None:
        first = split_diagnostic(self.tasks())
        second = split_diagnostic(self.tasks())
        self.assertEqual(first, second)
        self.assertEqual(set(first["by_signal"]), set(SIGNALS))
        self.assertEqual(first["sample_count"], len(self.tasks()) * ACTION_BUDGET)
        self.assertGreaterEqual(first["hidden_positive_action_count"], 0)
        self.assertIn("min_alignment_auc", first["thresholds"])
        self.assertFalse(first["feasible"])

    def test_selector_source_does_not_read_hidden_environment_fields(self) -> None:
        source = inspect.getsource(public_view)
        self.assertNotIn("_target", source)
        self.assertNotIn("_deleted", source)
        self.assertNotIn("open_test", source)
        self.assertNotIn("FinalManifestAccess", source)

    def test_temp_receipt_is_deterministic_and_no_sealed_access(self) -> None:
        tasks = self.tasks()
        with TemporaryDirectory() as directory:
            result = run_probe(train_tasks=tasks, validation_tasks=tasks, output_dir=Path(directory))
            receipt = Path(directory) / "public_interface_v13_feasibility_receipt.json"
            self.assertTrue(receipt.exists())
            written = json.loads(receipt.read_text())
            self.assertEqual(written["status"], result["status"])
            self.assertIn(result["status"], {"negative", "unverified_underpowered", "positive"})
            self.assertEqual(written["costs"], {"test_openings": 0, "test_updates": 0})
            self.assertNotIn("hidden_values", receipt.read_text())
            self.assertNotIn("open_test", receipt.read_text())
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                run_probe(train_tasks=tasks, validation_tasks=tasks, output_dir=Path(directory))


if __name__ == "__main__":
    unittest.main()
