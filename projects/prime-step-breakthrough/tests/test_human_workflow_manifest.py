from __future__ import annotations

import copy
import unittest

from human_workflow_manifest import ManifestError, build_manifests


def fixture_freeze() -> dict[str, object]:
    items = []
    for index in range(20):
        items.append(
            {
                "item_id": f"test-{index:04d}",
                "source_row": index,
                "predicted_label": index % 10,
                "margin_bin": index % 2,
            }
        )
    ids = [item["item_id"] for item in items]
    return {
        "outcome_state": "ABSENT_BY_DESIGN",
        "items": items,
        "orders": {
            "production": {"item_ids": ids},
            "seeded_random": {"item_ids": ids[::2] + ids[1::2]},
            "quota_balanced": {"item_ids": ids[1::2] + ids[::2]},
        },
    }


class HumanWorkflowManifestTests(unittest.TestCase):
    def test_three_orders_share_one_cohort_and_no_outcome_fields(self) -> None:
        freeze = fixture_freeze()
        features = [tuple((value + index) % 17 for value in range(64)) for index in range(20)]
        manifests = build_manifests(freeze, features, per_prediction=2)
        self.assertEqual(set(manifests), {"production", "seeded_random", "quota_balanced"})
        cohort_digests = {manifest["cohort_digest"] for manifest in manifests.values()}
        self.assertEqual(len(cohort_digests), 1)
        item_orders = [tuple(item["item_id"] for item in manifest["items"]) for manifest in manifests.values()]
        self.assertEqual({len(order) for order in item_orders}, {20})
        self.assertEqual(len(set(item_orders[0])), 20)
        for manifest in manifests.values():
            self.assertNotIn("truth", str(manifest).lower())
            self.assertEqual(len(manifest["items"][0]["choices"]), 10)
            self.assertEqual(manifest["items"][0]["prompt"].count("\n"), 11)

    def test_forbidden_freeze_field_is_rejected(self) -> None:
        freeze = fixture_freeze()
        freeze["items"] = copy.deepcopy(freeze["items"])
        freeze["items"][0]["ground_truth"] = 7
        features = [tuple(0 for _ in range(64)) for _ in range(20)]
        with self.assertRaises(ManifestError):
            build_manifests(freeze, features, per_prediction=2)

    def test_invalid_feature_shape_is_rejected(self) -> None:
        with self.assertRaises(ManifestError):
            build_manifests(fixture_freeze(), [tuple(0 for _ in range(63)) for _ in range(20)], per_prediction=2)


if __name__ == "__main__":
    unittest.main()
