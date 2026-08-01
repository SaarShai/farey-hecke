from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import prospective_uci_blind as pilot


def fixture_rows() -> tuple[list[tuple[int, ...]], list[int], list[tuple[int, ...]], list[int]]:
    train_x = [(label, 0) for label in range(10)]
    train_y = list(range(10))
    test_y = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
    test_x = [(label, 0) for label in test_y]
    return train_x, train_y, test_x, test_y


class ProspectiveUciBlindTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = fixture_rows()
        self.full_loader = patch.object(pilot, "_load_dataset", return_value=self.rows)
        self.feature_loader = patch.object(
            pilot,
            "_load_features_for_freeze",
            return_value=(self.rows[0], self.rows[1], self.rows[2]),
        )
        self.full_loader.start()
        self.feature_loader.start()
        self.addCleanup(self.full_loader.stop)
        self.addCleanup(self.feature_loader.stop)

    def make_freeze(self, root: Path) -> tuple[Path, Path, dict[str, object]]:
        dataset = root / "fixture.zip"
        dataset.write_bytes(b"fixture-dataset")
        manifest = pilot.build_freeze_manifest(
            dataset,
            frozen_at="2026-08-01T00:00:00Z",
            seed=17,
            warmup=2,
            bins=1,
            pilot_id="fixture-uci",
        )
        target = root / "pilot"
        pilot.write_freeze(target, manifest)
        return dataset, target, manifest

    def test_freeze_contains_only_outcome_blind_items_and_three_orders(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dataset, target, manifest = self.make_freeze(Path(directory))
            verified = pilot.verify_freeze(target, dataset)
            self.assertTrue(verified["freeze_verified"])
            self.assertEqual(manifest["outcome_state"], "ABSENT_BY_DESIGN")
            self.assertEqual(
                set(manifest["orders"]), {"production", "seeded_random", "quota_balanced"}
            )
            for item in manifest["items"]:
                self.assertFalse(pilot.FORBIDDEN_ITEM_KEYS.intersection(item))
            self.assertNotIn('"correct"', (target / "freeze.json").read_text())

    def test_freeze_tampering_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dataset, target, _manifest = self.make_freeze(Path(directory))
            payload = json.loads((target / "freeze.json").read_text())
            payload["items"][0]["predicted_label"] = 99
            pilot.atomic_json(target / "freeze.json", payload)
            with self.assertRaisesRegex(pilot.PilotError, "freeze.json does not match"):
                pilot.verify_freeze(target, dataset)

    def test_reveal_is_bound_to_freeze_and_recomputed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dataset, target, _manifest = self.make_freeze(Path(directory))
            with self.assertRaisesRegex(pilot.PilotError, "after the freeze"):
                pilot.build_result(
                    target,
                    dataset,
                    revealed_at="2026-08-01T00:00:00Z",
                )
            result = pilot.build_result(
                target,
                dataset,
                revealed_at="2026-08-02T00:00:00Z",
            )
            pilot.write_result(target, result)
            verified = pilot.verify_result(target, dataset)
            self.assertTrue(verified["result_verified"])
            self.assertEqual(result["outcome_state"], "REVEALED")
            self.assertEqual(result["analysis"]["item_count"], 12)
            self.assertIn("quota_balanced", result["analysis"]["orders"])

    def test_result_sidecar_rejects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dataset, target, _manifest = self.make_freeze(Path(directory))
            result = pilot.build_result(
                target,
                dataset,
                revealed_at="2026-08-02T00:00:00Z",
            )
            pilot.write_result(target, result)
            payload = json.loads((target / "result.json").read_text())
            payload["analysis"]["final_accuracy"] = 0.0
            pilot.atomic_json(target / "result.json", payload)
            with self.assertRaisesRegex(pilot.PilotError, "result.json does not match"):
                pilot.verify_result(target, dataset)


if __name__ == "__main__":
    unittest.main()
