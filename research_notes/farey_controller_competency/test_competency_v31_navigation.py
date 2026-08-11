"""Tests for the v3.1 navigation-only reachability redesign."""

import unittest

from .competency_v3_feasibility import DEFAULT_CONFIG as STAGE0_CONFIG, _manifest as stage0_manifest
from .competency_v31_navigation import (
    DEFAULT_CONFIG,
    EXACT_THRESHOLD,
    F1_THRESHOLD,
    NAVIGATION_ACTIONS,
    QUARTER_ACTIONS,
    _negative_fixture,
    _replay_witness,
    exact_navigation_ceiling,
    quarter_step,
)
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class NavigationDiagnosticsTests(unittest.TestCase):
    def test_quarter_stride_is_scale_free_and_bounded(self) -> None:
        self.assertEqual(quarter_step(1), 1)
        self.assertEqual(quarter_step(3), 1)
        self.assertEqual(quarter_step(4), 1)
        self.assertEqual(quarter_step(8), 2)
        self.assertEqual(quarter_step(17), 4)
        with self.assertRaises(ValueError):
            quarter_step(0)

    def test_action_vocabulary_only_adds_two_navigation_actions(self) -> None:
        self.assertEqual(set(NAVIGATION_ACTIONS) - set(QUARTER_ACTIONS), {
            "move_left",
            "move_right",
            "insert_mediant",
            "insert_midpoint",
        })
        self.assertEqual(set(NAVIGATION_ACTIONS) & set(QUARTER_ACTIONS), set(QUARTER_ACTIONS))
        self.assertEqual(len(NAVIGATION_ACTIONS), 6)

    def test_exact_navigation_ceiling_uses_all_eight_actions(self) -> None:
        task = RepairTask(6, DamagePattern.RANDOM_ISOLATED, GoalState.COVERAGE, 31, 2)
        ceiling = exact_navigation_ceiling(task)
        self.assertEqual(len(ceiling.best_f1_actions), 8)
        witness = _replay_witness(task, ceiling.best_f1_actions)
        self.assertEqual(witness["actions_used"], 8)
        self.assertEqual(witness["actions_remaining"], 0)
        self.assertEqual(witness["f1"], ceiling.max_f1)
        self.assertGreater(ceiling.visited_states, 0)

    def test_navigation_search_is_deterministic_for_a_task(self) -> None:
        task = RepairTask(6, DamagePattern.BURST, GoalState.SPECTRAL, 73, 2)
        self.assertEqual(exact_navigation_ceiling(task), exact_navigation_ceiling(task))

    def test_manifest_is_identical_to_stage0(self) -> None:
        tasks = stage0_manifest(STAGE0_CONFIG)
        self.assertEqual(len(tasks), 18)
        self.assertEqual(
            [(task.order, task.pattern.value, task.goal.value, task.seed, task.damage_count) for task in tasks],
            [(task.order, task.pattern.value, task.goal.value, task.seed, task.damage_count) for task in stage0_manifest(STAGE0_CONFIG)],
        )

    def test_thresholds_are_locked_and_negative_fixture_trips(self) -> None:
        self.assertEqual(DEFAULT_CONFIG.f1_threshold, F1_THRESHOLD)
        self.assertEqual(DEFAULT_CONFIG.exact_threshold, EXACT_THRESHOLD)
        with self.assertRaises(ValueError):
            type(DEFAULT_CONFIG)(f1_threshold=0.79)
        task = RepairTask(6, DamagePattern.RANDOM_ISOLATED, GoalState.COVERAGE, 31, 2)
        fixture = _negative_fixture(task, 1)
        self.assertEqual(fixture["status"], "negative")
        self.assertLess(fixture["max_f1"], F1_THRESHOLD)


if __name__ == "__main__":
    unittest.main()
