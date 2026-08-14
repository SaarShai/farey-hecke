from __future__ import annotations

from datetime import datetime, timezone
import sys
from pathlib import Path
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import oasst1_public_replay as replay


def item(index: int, stratum: str, outcomes: tuple[float, ...], reviews: int = 3) -> replay.Item:
    return replay.Item(
        item_id=f"i{index}",
        created=datetime(2023, 1, 2, 0, index, tzinfo=timezone.utc),
        week="2023-W01",
        stratum=stratum,
        reviews=reviews,
        outcomes=outcomes,
    )


class Oasst1ReplayTests(unittest.TestCase):
    def test_length_bands_are_outcome_blind_and_stable(self) -> None:
        self.assertEqual(replay._length_band("x" * 199), "short")
        self.assertEqual(replay._length_band("x" * 200), "medium")
        self.assertEqual(replay._length_band("x" * 600), "long")
        self.assertEqual(replay._length_band("x" * 1_500), "very-long")

    def test_checkpoint_metric_matches_full_population_target(self) -> None:
        items = [
            item(0, "a", (0.0, 0.0, 0.0, 0.0)),
            item(1, "b", (1.0, 1.0, 1.0, 1.0)),
        ]
        original = replay.CHECKPOINTS
        replay.CHECKPOINTS = (0.5, 1.0)
        try:
            result = replay.checkpoint_metrics(items, [0, 1])
        finally:
            replay.CHECKPOINTS = original
        self.assertEqual(result["checkpoints"][-1]["mean_absolute_error"], 0.0)
        self.assertEqual(result["checkpoints"][-1]["reviews"], 6)

    def test_permuted_control_preserves_items_and_outcome_multiset(self) -> None:
        items = [item(i, str(i % 2), (float(i), 0.0, 0.0, 0.0)) for i in range(8)]
        shuffled = replay._permuted_outcomes(items, seed=9)
        self.assertEqual([candidate.item_id for candidate in shuffled], [candidate.item_id for candidate in items])
        self.assertEqual(sorted(candidate.outcomes for candidate in shuffled), sorted(candidate.outcomes for candidate in items))
        self.assertNotEqual([candidate.outcomes for candidate in shuffled], [candidate.outcomes for candidate in items])

    def test_weekly_batches_drops_small_partial_weeks(self) -> None:
        items = [item(i, "a", (0.0, 0.0, 0.0, 0.0)) for i in range(4)]
        self.assertEqual(replay.weekly_batches(items, minimum=5), {})
        self.assertEqual(list(replay.weekly_batches(items, minimum=4)), ["2023-W01"])


if __name__ == "__main__":
    unittest.main()
