"""Tests for the V6 sealed final-manifest and access protocol."""

import unittest

from .competency_v6_final_manifest import (
    ACTION_BUDGET,
    ACTION_VOCABULARY,
    CELL_RECOVERY_THRESHOLD,
    EXACT_RECOVERY_THRESHOLD,
    PUBLIC_FIELDS,
    VALIDATION_PURPOSE,
    AccessProtocolError,
    FinalManifestAccess,
    _opening_token,
    _validate_model_digest,
    exact_feasibility_audit,
    access_protocol_probe,
    public_leakage_probe,
    seal_manifest,
    shortest_exact_recovery,
)


class V6FinalManifestTests(unittest.TestCase):
    def test_fresh_manifest_is_deterministic_balanced_and_disjoint(self) -> None:
        first = seal_manifest()
        second = seal_manifest()
        self.assertEqual(first["private_hash"], second["private_hash"])
        self.assertEqual(first["public_hash"], second["public_hash"])
        self.assertEqual(len(first["private_rows"]), 720)
        self.assertEqual(
            {split: len(tasks) for split, tasks in first["tasks_by_split"].items()},
            {"train": 240, "validation": 120, "test": 360},
        )
        self.assertTrue(first["retired_order_disjoint"])
        self.assertTrue(first["retired_seed_overlap_check"])

    def test_public_schema_and_frozen_interface(self) -> None:
        manifest = seal_manifest()
        self.assertEqual(set(manifest["public_rows"][0]), set(PUBLIC_FIELDS))
        self.assertEqual(ACTION_BUDGET, 16)
        self.assertEqual(len(ACTION_VOCABULARY), 18)
        self.assertEqual(EXACT_RECOVERY_THRESHOLD, 0.90)
        self.assertEqual(CELL_RECOVERY_THRESHOLD, 0.80)
        probe = public_leakage_probe(manifest)
        self.assertEqual(probe["status"], "pass")
        self.assertEqual(probe["bad_key_row_count"], 0)
        self.assertEqual(probe["forbidden_value_row_count"], 0)

    def test_exact_v5_evaluator_reaches_a_small_fresh_task(self) -> None:
        manifest = seal_manifest()
        result = shortest_exact_recovery(manifest["tasks_by_split"]["train"][0])
        self.assertIsNotNone(result["min_actions"])
        self.assertLessEqual(result["min_actions"], ACTION_BUDGET)
        self.assertTrue(result["reachable_within_budget"])

    def test_access_adapter_enforces_train_validation_and_one_shot_test(self) -> None:
        manifest = seal_manifest()
        adapter = FinalManifestAccess(manifest)
        self.assertEqual(len(adapter.training_tasks()), 240)
        with self.assertRaises(AccessProtocolError):
            adapter.validation_tasks(purpose="ordinary_validation")
        self.assertEqual(len(adapter.validation_tasks(purpose=VALIDATION_PURPOSE)), 120)
        with self.assertRaises(AccessProtocolError):
            adapter.freeze_model("not-a-digest")
        model_digest = "sha256:" + "a" * 64
        token = adapter.freeze_model(model_digest)
        self.assertEqual(token, _opening_token(manifest["private_hash"], model_digest))
        with self.assertRaises(AccessProtocolError):
            adapter.training_tasks()
        with self.assertRaises(AccessProtocolError):
            adapter.open_test(frozen_model_digest=model_digest, opening_token="wrong")
        self.assertEqual(
            len(adapter.open_test(frozen_model_digest=model_digest, opening_token=token)),
            360,
        )
        with self.assertRaises(AccessProtocolError):
            adapter.open_test(frozen_model_digest=model_digest, opening_token=token)
        snapshot = adapter.audit_snapshot()
        self.assertEqual(snapshot["test_openings"], 1)
        self.assertEqual(snapshot["test_updates"], 0)

    def test_combined_gate_shape_is_explicit(self) -> None:
        manifest = seal_manifest()
        result = exact_feasibility_audit(manifest)
        self.assertEqual(result["task_count"], 720)
        self.assertIn("overall", result["gates"])
        self.assertIn("per_cell", result["gates"])
        self.assertIn("combined", result["gates"])
        self.assertEqual(result["gates"]["combined"]["status"], "positive")

    def test_feasibility_probe_does_not_open_controller_test_accessor(self) -> None:
        protocol = access_protocol_probe(seal_manifest())
        self.assertEqual(protocol["evaluator_feasibility_access"]["test_openings"], 1)
        controller = protocol["controller_test_accessor"]
        self.assertEqual(controller["test_openings"], 0)
        self.assertFalse(controller["token_issued"])
        self.assertEqual(controller["test_updates"], 0)


if __name__ == "__main__":
    unittest.main()
