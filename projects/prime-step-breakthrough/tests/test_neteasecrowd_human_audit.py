from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import neteasecrowd_human_audit as audit


def items() -> list[dict[str, int | str]]:
    return [
        {
            "item_id": f"annotation-{index:07d}",
            "source_row": index,
            "taskset_id": 10 + index % 3,
            "task_id": 1000 + index,
            "worker_id": 2000 + index % 2,
            "complete_time_ms": 1_000 + (index * 7) % 23,
            "capability": 50 + index % 2,
        }
        for index in range(15)
    ]


class NetEaseCrowdHumanAuditTests(unittest.TestCase):
    def test_orders_are_complete_and_quota_certificate_is_verified(self) -> None:
        orders, certificate = audit._build_orders(items(), seed=17)
        self.assertTrue(certificate["verified"])
        expected = sorted(item["item_id"] for item in items())
        for order in orders.values():
            self.assertEqual(sorted(order["item_ids"]), expected)

    def test_metrics_use_only_revealed_binary_outcomes(self) -> None:
        metrics = audit._metrics([1, 0, 1, 1], [0, 1, 2, 3], warmup=2)
        self.assertAlmostEqual(metrics["integrated_absolute_prefix_error"], 1 / 9)
        self.assertEqual(metrics["one_percent_settling_prefix"], 4)

    def test_metadata_selection_digest_is_stable_and_outcome_free(self) -> None:
        rows = []
        for taskset in range(100, 104):
            for index in range(3):
                rows.append(
                    {
                        "tasksetId": taskset,
                        "taskId": taskset * 10 + index,
                        "workerId": index,
                        "completeTime": 1000 + index,
                        "capability": 50 + taskset % 2,
                    }
                )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.parquet"
            path.write_bytes(b"fixture")
            with mock.patch.object(audit, "DATASET_SHA256", audit.sha256_file(path)), mock.patch.object(
                audit, "DATASET_ROWS", len(rows)
            ), mock.patch.object(audit, "_rows", side_effect=[
                ({"tasksetId": row["tasksetId"], "capability": row["capability"]} for row in rows),
                (row for row in rows),
            ]):
                selected, selection = audit.select_metadata(path, tasksets=2, per_taskset=3)
        self.assertEqual(len(selected), 6)
        self.assertIn("metadata_digest", selection)
        self.assertTrue(all("answer" not in item and "truth" not in item for item in selected))


if __name__ == "__main__":
    unittest.main()
