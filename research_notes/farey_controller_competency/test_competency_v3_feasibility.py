"""Tests for evaluator-only Stage-0 feasibility diagnostics."""

import json
import unittest

from .competency_v3_feasibility import (
    DEFAULT_CONFIG,
    FeasibilityConfig,
    _serialize_view,
    exact_reachability_ceiling,
    observation_collision_ceiling,
    run_diagnostics,
)
from .repair_experiment import RepairTask, _task_environment, coarse_view
from .strict_environment import DamagePattern, GoalState


class FeasibilityDiagnosticsTests(unittest.TestCase):
    def _small_config(self) -> FeasibilityConfig:
        return FeasibilityConfig(
            seed=20260811,
            representative_orders=(6,),
            representative_patterns=(DamagePattern.RANDOM_ISOLATED,),
            representative_damage_count=2,
            collision_depth=1,
        )

    def test_fixed_budget_and_actions_bound_exact_search(self) -> None:
        task = RepairTask(6, DamagePattern.RANDOM_ISOLATED, GoalState.COVERAGE, 31, 2)
        ceiling = exact_reachability_ceiling(task)
        self.assertEqual(len(ceiling.best_f1_actions), 8)
        self.assertGreater(ceiling.visited_states, 0)
        for value in (
            ceiling.max_precision,
            ceiling.max_recall,
            ceiling.max_f1,
            ceiling.max_exact_recovery,
        ):
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_default_reachability_rows_include_cursor_and_budget_evidence(self) -> None:
        result = run_diagnostics(self._small_config())
        witness = result["reachability"]["tasks"][0]["witness"]
        self.assertEqual(witness["actions_used"], 8)
        self.assertEqual(witness["actions_remaining"], 0)
        self.assertEqual(len(witness["cursor_trace"]), 9)
        self.assertGreaterEqual(witness["recovered_count"], 0)
        self.assertLessEqual(witness["recovered_count"], witness["deleted_count"])

    def test_view_serialization_is_primitive_and_does_not_leak_identity(self) -> None:
        task = RepairTask(6, DamagePattern.RANDOM_ISOLATED, GoalState.COVERAGE, 31, 2)
        view = coarse_view(_task_environment(task, "farey").observation)
        serialized = _serialize_view(view)
        decoded = json.loads(serialized)
        self.assertEqual(set(decoded), {
            "cursor_relation_bin",
            "last_scalar_feedback",
            "local_gap_bins",
            "local_ratio_bins",
            "remaining_budget_fraction",
            "trusted_goal",
        })
        forbidden = {"target", "survivor", "fraction", "order", "deleted", "identity", "metric"}
        self.assertTrue(forbidden.isdisjoint(serialized.lower()))

    def test_collision_summary_has_a_valid_ceiling(self) -> None:
        task = RepairTask(6, DamagePattern.RANDOM_ISOLATED, GoalState.COVERAGE, 31, 2)
        summary = observation_collision_ceiling([task], depth=1)
        self.assertGreater(summary["samples"], 0)
        self.assertGreaterEqual(summary["action_accuracy_ceiling"], 0.0)
        self.assertLessEqual(summary["action_accuracy_ceiling"], 1.0)
        self.assertGreaterEqual(summary["unique_views"], 1)

    def test_default_gate_thresholds_and_negative_fixtures(self) -> None:
        result = run_diagnostics(self._small_config())
        self.assertEqual(result["provenance"]["controller_training"], False)
        self.assertIn(result["gates"]["reachability_ceiling"]["status"], {"positive", "negative", "unverified"})
        self.assertIn(result["gates"]["observation_identifiability"]["status"], {"positive", "negative", "unverified"})
        self.assertIn(result["gates"]["scalar_feedback_informativeness"]["status"], {"positive", "negative", "unverified"})
        self.assertEqual(result["gates"]["reachability_negative_fixture"]["status"], "negative")
        self.assertEqual(result["gates"]["observation_negative_fixture"]["status"], "negative")
        self.assertEqual(result["gates"]["scalar_feedback_negative_fixture"]["status"], "negative")

    def test_small_receipt_is_bytewise_deterministic(self) -> None:
        config = self._small_config()
        self.assertEqual(run_diagnostics(config), run_diagnostics(config))

    def test_nonstandard_budget_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            FeasibilityConfig(action_budget=7)


if __name__ == "__main__":
    unittest.main()
