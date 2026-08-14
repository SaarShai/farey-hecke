from __future__ import annotations

from fractions import Fraction
import unittest

import moat_falsification as moat


class MoatFalsificationTests(unittest.TestCase):
    def test_deficit_schedule_is_complete_and_deterministic(self) -> None:
        counts = {"a": 5, "b": 3, "c": 2}
        first = moat.proportional_deficit_schedule(counts)
        second = moat.proportional_deficit_schedule(counts)
        self.assertEqual(first, second)
        self.assertEqual({category: first.count(category) for category in counts}, counts)

    def test_materialize_preserves_within_stratum_queues(self) -> None:
        schedule = ["a", "b", "a", "b", "a"]
        queues = {"a": [4, 2, 0], "b": [3, 1]}
        order = moat.materialize(schedule, queues)
        self.assertEqual([index for index in order if index in queues["a"]], queues["a"])
        self.assertEqual([index for index in order if index in queues["b"]], queues["b"])

    def test_prefix_discrepancy_is_exact(self) -> None:
        schedule = ["a", "b", "a", "a"]
        self.assertEqual(
            moat.max_prefix_discrepancy(schedule, {"a": 3, "b": 1}), Fraction(1, 2)
        )

    def test_prefix_metrics_match_manual_result(self) -> None:
        metrics = moat.prefix_metrics([1, 0, 1, 1], [0, 1, 2, 3], warmup=1)
        self.assertAlmostEqual(metrics["integrated_absolute_error"], 7 / 48)
        self.assertEqual(metrics["one_percent_settling_prefix"], 4)


if __name__ == "__main__":
    unittest.main()
