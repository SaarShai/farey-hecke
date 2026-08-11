"""Tests for the V4 sealed-manifest evaluator-only audit."""

import unittest

from .competency_v4_sealed_manifest import (
    ACTION_BUDGET,
    CLOSURE_ACTIONS,
    DEFAULT_CONFIG,
    DEVELOPMENT_ORDERS,
    FORBIDDEN_PUBLIC_FIELDS,
    PUBLIC_FIELDS,
    TEST_ORDERS,
    TRAIN_ORDERS,
    VALIDATION_ORDERS,
    _target_restricted_witness,
    _digest,
    _task_from_row,
    run_audit,
    seal_manifests,
    visible_reward_audit,
)
from .strict_environment import DamagePattern, GoalState


class SealedManifestTests(unittest.TestCase):
    def test_splits_are_fresh_and_disjoint_from_development(self) -> None:
        self.assertEqual(set(DEVELOPMENT_ORDERS) & set(TRAIN_ORDERS), set())
        self.assertEqual(set(DEVELOPMENT_ORDERS) & set(VALIDATION_ORDERS), set())
        self.assertEqual(set(DEVELOPMENT_ORDERS) & set(TEST_ORDERS), set())
        manifest = seal_manifests()
        self.assertEqual(len(manifest["private_rows"]), 720)
        self.assertEqual(manifest["public_rows"][0].keys(), set(PUBLIC_FIELDS))

    def test_manifest_hashes_are_deterministic_and_public_rows_are_leakage_safe(self) -> None:
        first = seal_manifests()
        second = seal_manifests()
        self.assertEqual(first["private_hash"], second["private_hash"])
        self.assertEqual(first["public_hash"], second["public_hash"])
        for row in first["public_rows"]:
            self.assertFalse(set(row) & set(FORBIDDEN_PUBLIC_FIELDS))
            self.assertEqual(set(row), set(PUBLIC_FIELDS))
        self.assertNotEqual(first["private_hash"], _digest({"tampered": True}))
        self.assertEqual(len(first["task_commitments"]), 720)
        self.assertIn("deleted_indices", first["private_rows"][0])
        self.assertIn("target_sha256", first["private_rows"][0])
        self.assertIn("damage_mask_sha256", first["private_rows"][0])

    def test_action_vocabulary_is_final_v34_and_budget_is_eight(self) -> None:
        self.assertEqual(len(CLOSURE_ACTIONS), 12)
        self.assertEqual(ACTION_BUDGET, 8)
        self.assertIn("move_left_eighth", CLOSURE_ACTIONS)
        self.assertIn("move_right_eighth", CLOSURE_ACTIONS)

    def test_target_restricted_witness_is_deterministic_and_explicitly_scoped(self) -> None:
        manifest = seal_manifests()
        row = next(row for row in manifest["private_rows"] if row["order"] == 24)
        task = _task_from_row(row)
        first = _target_restricted_witness(task)
        second = _target_restricted_witness(task)
        self.assertEqual(first, second)
        self.assertIn(
            first["completeness"],
            {
                "exact_recovery_proved_reachable",
                "exact_recovery_proved_unreachable_f1_incomplete",
            },
        )
        self.assertEqual(len(first["best_f1_actions"]), ACTION_BUDGET)

    def test_visible_reward_is_target_independent_and_has_both_classes(self) -> None:
        manifest = seal_manifests()
        result = visible_reward_audit(manifest)
        self.assertFalse(result["hidden_identity_used_in_reward"])
        self.assertGreater(result["improving_actions"], 0)
        self.assertGreater(result["non_improving_actions"], 0)
        self.assertGreaterEqual(result["auc"], 0.0)
        self.assertLessEqual(result["auc"], 1.0)

    def test_audit_explicitly_makes_no_controller_claim(self) -> None:
        result = run_audit()
        self.assertFalse(result["provenance"]["controller_training"])
        self.assertFalse(result["provenance"]["learner_created"])
        self.assertTrue(result["provenance"]["manifest_frozen_before_learner"])
        self.assertEqual(result["gates"]["sealed_manifest_feasibility"]["status"], "negative")
        self.assertEqual(
            result["manifest_seal"]["training_eligibility"],
            "ineligible_failed_exact_recovery_feasibility_gate",
        )
        self.assertIn("validation", result["claim_boundary"])
        self.assertIn("train stream", result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
