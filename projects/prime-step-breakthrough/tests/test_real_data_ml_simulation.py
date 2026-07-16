from __future__ import annotations

import json
import math
from pathlib import Path
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import real_data_ml_simulation as simulation


class RealDataSimulationUnitTests(unittest.TestCase):
    def test_joint_strata_use_prediction_and_margin_bin(self) -> None:
        strata = simulation.joint_strata(
            [7, 7, 2, 2],
            [0.1, 0.7, 0.4, 0.9],
            {2: (0.25, 0.5, 0.75), 7: (0.25, 0.5, 0.75)},
        )
        self.assertEqual(
            strata,
            [
                "predicted-7:margin-0",
                "predicted-7:margin-2",
                "predicted-2:margin-1",
                "predicted-2:margin-3",
            ],
        )

    def test_materialized_order_preserves_each_fixed_queue(self) -> None:
        strata = ["b", "a", "b", "a", "b"]
        result, queues = simulation.quota_plan(strata)
        queues = {"a": [3, 1], "b": [4, 0, 2]}
        order = simulation.materialize_order(result, queues)
        self.assertEqual([index for index in order if index in queues["a"]], queues["a"])
        self.assertEqual([index for index in order if index in queues["b"]], queues["b"])
        self.assertEqual(sorted(order), list(range(5)))

    def test_paired_orders_share_within_stratum_priorities(self) -> None:
        strata = ["a", "b", "a", "b", "a", "b"]
        result, queues = simulation.quota_plan(strata)
        random_order, tool_order = simulation.priority_orders(19, result, queues)
        for queue in queues.values():
            random_filtered = [index for index in random_order if index in queue]
            tool_filtered = [index for index in tool_order if index in queue]
            self.assertEqual(tool_filtered, random_filtered)

    def test_prefix_metrics_match_hand_calculation(self) -> None:
        errors = simulation.prefix_errors([1, 0, 1, 1], [0, 1, 2, 3])
        self.assertEqual(len(errors), 4)
        self.assertAlmostEqual(errors[0], 0.25)
        self.assertAlmostEqual(errors[1], -0.25)
        self.assertAlmostEqual(errors[2], -1 / 12)
        self.assertEqual(errors[3], 0.0)
        metrics = simulation.integrated_metrics(errors, 1)
        self.assertAlmostEqual(metrics["mean_absolute_error"], 7 / 48)
        self.assertAlmostEqual(
            metrics["root_mean_squared_error"],
            math.sqrt((0.25**2 + 0.25**2 + (1 / 12) ** 2) / 4),
        )

    def test_bootstrap_interval_is_deterministic_and_positive(self) -> None:
        tool = [0.4, 0.5, 0.6, 0.7]
        baseline = [0.8, 0.9, 1.0, 1.1]
        first = simulation.bootstrap_reduction_interval(
            tool, baseline, replicates=200, seed=7
        )
        second = simulation.bootstrap_reduction_interval(
            tool, baseline, replicates=200, seed=7
        )
        self.assertEqual(first, second)
        self.assertGreater(first[0], 0)

    def test_settling_prefix_is_after_last_violation(self) -> None:
        self.assertEqual(simulation.settling_prefix([0.2, 0.09, 0.11, 0.04], 0.1), 4)
        self.assertEqual(simulation.settling_prefix([0.02, 0.01], 0.1), 1)
        with self.assertRaises(ValueError):
            simulation.settling_prefix([0.1], 0.0)

    def test_dataset_checksum_is_pinned(self) -> None:
        self.assertEqual(len(simulation.DATASET_SHA256), 64)
        int(simulation.DATASET_SHA256, 16)

    def test_invalid_or_missing_dataset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / "bad.zip"
            bad.write_bytes(b"not the pinned UCI archive")
            with self.assertRaises(ValueError):
                simulation.load_dataset(bad)
            with self.assertRaises(FileNotFoundError):
                simulation.obtain_dataset(
                    Path(directory) / "missing.zip", offline=True
                )

    def test_report_round_trips_from_sorted_json_artifact(self) -> None:
        artifact = PROJECT_ROOT / "artifacts" / "real_data_ml_simulation.json"
        report = PROJECT_ROOT / "artifacts" / "REAL_DATA_ML_SIMULATION.md"
        payload = json.loads(artifact.read_text())
        self.assertEqual(simulation.render_report(payload), report.read_text())


if __name__ == "__main__":
    unittest.main()
