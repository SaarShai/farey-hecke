from __future__ import annotations

import dataclasses
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from coprimebatch.applications import (
    APPLICATION_PRESET_IDS,
    application_preset,
    application_preset_payload,
    application_presets,
)
from coprimebatch.prefix_balance import quota_order, verify_quota_result


class ApplicationPresetTests(unittest.TestCase):
    def test_registry_has_the_three_scoped_demonstrations(self) -> None:
        self.assertEqual(
            APPLICATION_PRESET_IDS,
            (
                "rendering-progressive-joint-cells",
                "finance-scenario-cells",
                "laboratory-prerandomized-strata",
            ),
        )
        self.assertEqual(
            tuple(preset.preset_id for preset in application_presets()),
            APPLICATION_PRESET_IDS,
        )

    def test_registered_totals_and_dimensions_are_canonical(self) -> None:
        expected = {
            "rendering-progressive-joint-cells": (4096, 16, 2),
            "finance-scenario-cells": (65536, 64, 3),
            "laboratory-prerandomized-strata": (512, 32, 3),
        }
        for preset_id, (total, categories, dimensions) in expected.items():
            with self.subTest(preset_id=preset_id):
                preset = application_preset(preset_id)
                self.assertEqual(preset.total_items, total)
                self.assertEqual(preset.category_count, categories)
                self.assertEqual(len(preset.feature_axes), dimensions)
                self.assertEqual(len(set(category for category, _ in preset.counts)), categories)
                self.assertTrue(all(count > 0 for _category, count in preset.counts))
                self.assertTrue(all(type(count) is int for _category, count in preset.counts))

    def test_definitions_are_immutable_and_payloads_are_fresh(self) -> None:
        first_preset = application_preset(APPLICATION_PRESET_IDS[0])
        second_preset = application_preset(APPLICATION_PRESET_IDS[0])
        self.assertIsNot(first_preset, second_preset)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            first_preset.status = "production"  # type: ignore[misc]

        first = application_preset_payload(APPLICATION_PRESET_IDS[0])
        second = application_preset_payload(APPLICATION_PRESET_IDS[0])
        self.assertIsNot(first, second)
        self.assertIsNot(first["counts"], second["counts"])
        self.assertIsNot(first["metadata"], second["metadata"])
        first["counts"]["forged"] = 1  # type: ignore[index]
        first["metadata"]["limitations"].append("forged")  # type: ignore[index,union-attr]
        third = application_preset_payload(APPLICATION_PRESET_IDS[0])
        self.assertNotIn("forged", third["counts"])
        self.assertNotIn("forged", third["metadata"]["limitations"])

    def test_application_status_and_negative_controls_are_explicit(self) -> None:
        for preset in application_presets():
            with self.subTest(preset=preset.preset_id):
                self.assertIn("demonstration", preset.status)
                self.assertTrue(preset.negative_control)
                self.assertGreaterEqual(len(preset.limitations), 3)
                self.assertIn("unconstrained categorical", preset.theorem_scope)

        laboratory = application_preset("laboratory-prerandomized-strata")
        self.assertIn("never treatment allocation", laboratory.status)
        self.assertIn("never assigns", laboratory.limitations[0])

    def test_every_preset_runs_through_the_quota_certificate(self) -> None:
        expected_digests = {
            "rendering-progressive-joint-cells": "1b19f50c79473efd260ba7d19889e9620c1c7c01b5dfaf21934257b673b6bab5",
            "finance-scenario-cells": "cafb8f1f469cc43a890619aac7306ce6149a013bcfc4095fb91bf329db378aec",
            "laboratory-prerandomized-strata": "e155f05a310ceea212458c74ff700bf4a061b2b151e21518c2636aedd6e9e449",
        }
        for preset in application_presets():
            with self.subTest(preset=preset.preset_id):
                result = quota_order(preset.counts_dict())
                self.assertEqual(len(result.order_codes), preset.total_items)
                self.assertEqual(result.order_sha256, expected_digests[preset.preset_id])
                self.assertTrue(verify_quota_result(result).passed)
                self.assertLess(result.max_discrepancy, 1)
                self.assertIsNotNone(result.ratio_bound)
                self.assertLess(result.ratio_bound, 3)

    def test_payloads_contain_no_registered_positive_overclaims(self) -> None:
        serialized = json.dumps(
            [application_preset_payload(preset_id) for preset_id in APPLICATION_PRESET_IDS]
        ).lower()
        forbidden_positive_claims = (
            "production validated",
            "production-ready",
            "guaranteed monetary savings",
            "improves final-image accuracy",
            "controls value-at-risk",
            "controls expected shortfall",
            "allocates treatment",
            "validates causal inference",
            "replaces randomization",
        )
        for claim in forbidden_positive_claims:
            with self.subTest(claim=claim):
                self.assertNotIn(claim, serialized)

    def test_unknown_and_nonstr_ids_fail_cleanly(self) -> None:
        with self.assertRaisesRegex(KeyError, "unknown application preset"):
            application_preset("missing")
        with self.assertRaisesRegex(TypeError, "must be a string"):
            application_preset(1)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
