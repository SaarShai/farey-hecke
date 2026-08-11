"""Tests for the V5 evaluator-only exact shortest-path audit."""

import unittest

from .competency_v5_feasibility import (
    ACTION_BUDGET,
    ACTION_VOCABULARY,
    CELL_RECOVERY_THRESHOLD,
    EXACT_RECOVERY_THRESHOLD,
    MOVEMENT_ACTIONS,
    _bruteforce_exact_within,
    _manifest_and_receipt,
    shortest_exact_recovery,
)


class V5FeasibilityTests(unittest.TestCase):
    def test_locked_generic_vocabulary_and_thresholds(self) -> None:
        self.assertEqual(ACTION_BUDGET, 16)
        self.assertEqual(len(MOVEMENT_ACTIONS), 14)
        self.assertEqual(len(ACTION_VOCABULARY), 18)
        self.assertIn("move_left_half", ACTION_VOCABULARY)
        self.assertIn("move_right_sixty_fourth", ACTION_VOCABULARY)
        self.assertEqual(EXACT_RECOVERY_THRESHOLD, 0.90)
        self.assertEqual(CELL_RECOVERY_THRESHOLD, 0.80)

    def test_retired_v4_manifest_is_pinned_and_unchanged(self) -> None:
        manifest, receipt = _manifest_and_receipt()
        self.assertEqual(sum(len(tasks) for tasks in manifest["tasks_by_split"].values()), 720)
        self.assertEqual(receipt["manifest_seal"]["private_sha256"], manifest["private_hash"])
        self.assertEqual(receipt["manifest_seal"]["public_sha256"], manifest["public_hash"])

    def test_shortest_path_matches_full_action_bruteforce_on_small_fixture(self) -> None:
        manifest, _receipt = _manifest_and_receipt()
        task = manifest["tasks_by_split"]["train"][0]
        exact = shortest_exact_recovery(task)
        self.assertIsNotNone(exact["min_actions"])
        self.assertLessEqual(exact["min_actions"], ACTION_BUDGET)
        brute = _bruteforce_exact_within(task, exact["min_actions"])
        self.assertEqual(brute, exact["min_actions"])

    def test_negative_fixture_one_action_cannot_recover_two_targets(self) -> None:
        manifest, _receipt = _manifest_and_receipt()
        result = shortest_exact_recovery(manifest["tasks_by_split"]["train"][0])
        self.assertTrue(result["min_actions"] is None or result["min_actions"] > 1)


if __name__ == "__main__":
    unittest.main()
