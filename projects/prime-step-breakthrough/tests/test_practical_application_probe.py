from __future__ import annotations

import json
from pathlib import Path
import random
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import practical_application_probe as probe


class PracticalApplicationProbeTests(unittest.TestCase):
    def test_stratified_split_is_deterministic_disjoint_and_complete(self) -> None:
        features = [(float(index), float(index % 3)) for index in range(30)]
        labels = ["a" if index % 2 else "b" for index in range(30)]
        first = probe.stratified_split(features, labels, seed=7)
        second = probe.stratified_split(features, labels, seed=7)
        self.assertEqual(first, second)
        train_x, train_y, test_x, test_y = first
        self.assertEqual(len(train_x) + len(test_x), len(features))
        self.assertEqual(set(train_y), {"a", "b"})
        self.assertEqual(set(test_y), {"a", "b"})
        self.assertFalse(set(train_x) & set(test_x))

    def test_centroid_margin_orders_easy_points_above_boundary_points(self) -> None:
        train_x = [(-3.0,), (-2.0,), (2.0,), (3.0,)]
        train_y = ["left", "left", "right", "right"]
        model = probe.train_centroid_model(train_x, train_y)
        predictions, margins = probe.predict_with_margin(model, [(-2.5,), (0.0,), (2.5,)])
        self.assertEqual(predictions[0], "left")
        self.assertEqual(predictions[2], "right")
        self.assertGreater(margins[0], margins[1])
        self.assertGreater(margins[2], margins[1])

    def test_audit_strata_do_not_receive_outcomes(self) -> None:
        strata = probe.audit_strata(
            ["a", "a", "b", "b"],
            [0.1, 0.9, 0.2, 0.8],
            ["a", "b"],
            [0.3, 0.7],
            bins=2,
        )
        self.assertEqual(strata, ["predicted-a:margin-0", "predicted-b:margin-1"])

    def test_empirical_risk_uses_worst_tail(self) -> None:
        result = probe.empirical_risk([float(value) for value in range(1, 101)])
        self.assertEqual(result["mean"], 50.5)
        self.assertEqual(result["var_97_5"], 98.0)
        self.assertEqual(result["expected_shortfall_97_5"], 99.0)

    def test_risk_population_matches_frozen_finance_preset(self) -> None:
        strata, losses = probe.generate_risk_population(seed=9)
        self.assertEqual(len(strata), 65_536)
        self.assertEqual(len(losses), len(strata))
        self.assertEqual(len(set(strata)), 64)
        self.assertTrue(all(value >= 0 for value in losses))

    def test_shuffled_null_preserves_loss_multiset(self) -> None:
        _, losses = probe.generate_risk_population(seed=11)
        shuffled = list(losses)
        random.Random(12).shuffle(shuffled)
        self.assertEqual(sorted(losses), sorted(shuffled))

    def test_cached_dataset_rejects_wrong_digest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            spec = probe.DATASETS[0]
            target = Path(directory) / f"{spec.name}.zip"
            target.write_bytes(b"wrong")
            with self.assertRaises(ValueError):
                probe.obtain_dataset(spec, Path(directory), offline=True)

    def test_report_round_trips_from_committed_artifact(self) -> None:
        artifact = PROJECT_ROOT / "artifacts" / "practical_application_probe.json"
        report = PROJECT_ROOT / "artifacts" / "PRACTICAL_APPLICATION_PROBE.md"
        if not artifact.exists() or not report.exists():
            self.skipTest("full probe artifact has not been generated")
        payload = json.loads(artifact.read_text())
        self.assertEqual(probe.render_report(payload), report.read_text())


if __name__ == "__main__":
    unittest.main()
