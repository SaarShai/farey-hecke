"""Tests for the v3.2 weighted-mediant closure diagnostics."""

import unittest
from fractions import Fraction

from .competency_v3_feasibility import DEFAULT_CONFIG as STAGE0_CONFIG, _manifest as stage0_manifest
from .competency_v32_closure import (
    CLOSURE_ACTIONS,
    DEFAULT_CONFIG,
    EXACT_TASK_FRACTION_THRESHOLD,
    F1_THRESHOLD,
    MIN_TASK_F1_THRESHOLD,
    WEIGHTED_ACTIONS,
    _negative_fixture,
    _load_v31_baseline,
    _transition,
    _weighted_candidate,
    _replay_witness,
    exact_closure_ceiling,
)
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class ClosureDiagnosticsTests(unittest.TestCase):
    def test_weighted_formulas_are_exact(self) -> None:
        left = Fraction(1, 5)
        right = Fraction(2, 5)
        self.assertEqual(_weighted_candidate(left, right, WEIGHTED_ACTIONS[0]), Fraction(4, 15))
        self.assertEqual(_weighted_candidate(left, right, WEIGHTED_ACTIONS[1]), Fraction(1, 3))

    def test_action_vocabulary_is_v31_plus_two_weighted_mediants(self) -> None:
        self.assertEqual(len(CLOSURE_ACTIONS), 8)
        self.assertEqual(set(CLOSURE_ACTIONS) - set(WEIGHTED_ACTIONS), {
            "move_left",
            "move_right",
            "insert_mediant",
            "insert_midpoint",
            "move_left_quarter",
            "move_right_quarter",
        })
        self.assertEqual(set(CLOSURE_ACTIONS) & set(WEIGHTED_ACTIONS), set(WEIGHTED_ACTIONS))

    def test_weighted_transition_inserts_a_new_fraction_and_charges_budget(self) -> None:
        points = (Fraction(0, 1), Fraction(1, 2), Fraction(1, 1))
        state = (points, 0, 8)
        updated, cursor, remaining = _transition(state, WEIGHTED_ACTIONS[0])
        self.assertEqual(remaining, 7)
        self.assertIn(Fraction(1, 4), updated)
        self.assertEqual(updated[cursor], Fraction(1, 4))

    def test_exact_closure_ceiling_uses_all_eight_actions(self) -> None:
        task = RepairTask(6, DamagePattern.RANDOM_ISOLATED, GoalState.COVERAGE, 31, 2)
        ceiling = exact_closure_ceiling(task)
        self.assertEqual(len(ceiling.best_f1_actions), 8)
        witness = _replay_witness(task, ceiling.best_f1_actions)
        self.assertEqual(witness["actions_used"], 8)
        self.assertEqual(witness["actions_remaining"], 0)
        self.assertEqual(witness["f1"], ceiling.max_f1)
        self.assertGreater(ceiling.visited_states, 0)

    def test_closure_search_is_deterministic_for_a_task(self) -> None:
        task = RepairTask(6, DamagePattern.BURST, GoalState.SPECTRAL, 73, 2)
        self.assertEqual(exact_closure_ceiling(task), exact_closure_ceiling(task))

    def test_manifest_is_the_unchanged_stage0_18_task_manifest(self) -> None:
        tasks = stage0_manifest(STAGE0_CONFIG)
        self.assertEqual(len(tasks), 18)
        self.assertEqual(
            [(task.order, task.pattern.value, task.goal.value, task.seed, task.damage_count) for task in tasks],
            [(task.order, task.pattern.value, task.goal.value, task.seed, task.damage_count) for task in stage0_manifest(STAGE0_CONFIG)],
        )

    def test_pinned_v31_baseline_receipt_and_source_hashes_verify(self) -> None:
        rows, provenance = _load_v31_baseline(stage0_manifest(STAGE0_CONFIG))
        self.assertEqual(len(rows), 18)
        self.assertTrue(provenance["source_hashes_verified"])
        self.assertFalse(provenance["recomputed_in_v32"])

    def test_closure_thresholds_are_locked_and_negative_fixture_trips(self) -> None:
        self.assertEqual(DEFAULT_CONFIG.mean_f1_threshold, F1_THRESHOLD)
        self.assertEqual(DEFAULT_CONFIG.minimum_task_f1_threshold, MIN_TASK_F1_THRESHOLD)
        self.assertEqual(DEFAULT_CONFIG.exact_task_fraction_threshold, EXACT_TASK_FRACTION_THRESHOLD)
        with self.assertRaises(ValueError):
            type(DEFAULT_CONFIG)(mean_f1_threshold=0.94)
        task = RepairTask(6, DamagePattern.RANDOM_ISOLATED, GoalState.COVERAGE, 31, 2)
        fixture = _negative_fixture(task, 1)
        self.assertEqual(fixture["status"], "negative")
        self.assertLess(fixture["max_f1"], F1_THRESHOLD)


if __name__ == "__main__":
    unittest.main()
