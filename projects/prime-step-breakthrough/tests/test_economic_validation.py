from __future__ import annotations

import unittest
import math
from pathlib import Path
import json

import economic_validation as validation


class EconomicValidationTests(unittest.TestCase):
    def test_exact_interval_is_exact_at_full_census(self) -> None:
        self.assertEqual(validation.hypergeom_interval(10, 10, 7, 9), (7, 7))

    def test_confidence_path_uses_only_revealed_prefix(self) -> None:
        strata = ["a", "b", "a", "b"]
        order = [0, 1, 2, 3]
        first = validation.confidence_path([1, 0, 1, 0], order, strata, alpha=0.05)
        second = validation.confidence_path([1, 0, 0, 1], order, strata, alpha=0.05)
        self.assertEqual(first["lower"][:2], second["lower"][:2])
        self.assertEqual(first["upper"][:2], second["upper"][:2])

    def test_final_interval_collapses_to_observed_population(self) -> None:
        outcomes = [1, 0, 1, 1, 0]
        path = validation.confidence_path(outcomes, [4, 2, 0, 1, 3], ["a", "b", "a", "b", "a"], alpha=0.05)
        self.assertEqual(path["lower"][-1], 3 / 5)
        self.assertEqual(path["upper"][-1], 3 / 5)
        self.assertTrue(path["simultaneous_coverage"])

    def test_invalid_order_and_nonbinary_outcome_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            validation.confidence_path([1, 0], [0, 0], ["a", "a"], alpha=0.05)
        with self.assertRaises(ValueError):
            validation.confidence_path([2, 0], [0, 1], ["a", "a"], alpha=0.05)

    def test_online_state_enforces_manifest_sequence_without_label_vector(self) -> None:
        state = validation.SafeStopState([1, 0], ["a", "b"])
        self.assertNotIn("outcomes", vars(state))
        with self.assertRaises(ValueError):
            state.reveal(0, 1)
        state.reveal(1, 0)
        with self.assertRaises(ValueError):
            state.reveal(0, 2)
        state.reveal(0, 1)
        with self.assertRaises(ValueError):
            state.reveal(0, 1)

    def test_manifest_digest_changes_with_order_or_strata(self) -> None:
        first = validation.SafeStopState([0, 1], ["a", "b"])
        second = validation.SafeStopState([1, 0], ["a", "b"])
        third = validation.SafeStopState([0, 1], ["a", "a"])
        self.assertNotEqual(first.manifest_sha256, second.manifest_sha256)
        self.assertNotEqual(first.manifest_sha256, third.manifest_sha256)

    def test_small_fixed_look_noncoverage_is_below_allocated_delta(self) -> None:
        for population in range(2, 8):
            looks = population - 1
            for sampled in range(1, population):
                for total in range(population + 1):
                    failure = 0.0
                    for observed in range(max(0, sampled - population + total), min(sampled, total) + 1):
                        probability = math.comb(total, observed) * math.comb(population - total, sampled - observed) / math.comb(population, sampled)
                        lo, hi = validation.hypergeom_interval(population, sampled, observed, looks)
                        if not lo <= total <= hi:
                            failure += probability
                    self.assertLessEqual(failure, 0.05 / looks + 1e-15)

    def test_committed_artifact_preserves_no_go_boundary(self) -> None:
        path = Path(__file__).resolve().parents[1] / "artifacts" / "economic_validation.json"
        payload = json.loads(path.read_text())
        self.assertIn("not observed human savings", payload["claim_boundary"])
        self.assertLess(payload["estimation_stops"]["0.05"]["mean_items_saved"], 0)


if __name__ == "__main__":
    unittest.main()
