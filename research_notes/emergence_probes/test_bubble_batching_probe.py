from pathlib import Path
import json
import tempfile
import unittest

from .bubble_batching_probe import N, run_once, run_probe


class BubbleBatchingProbeTests(unittest.TestCase):
    def test_sort_goal_is_reached(self):
        row = run_once(1)
        self.assertEqual(row.values, tuple(range(N)))
        self.assertGreater(row.goal_steps, 0)

    def test_determinism(self):
        self.assertEqual(run_once(11), run_once(11))

    def test_probe_receipt_and_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_probe(Path(tmp))
            receipt = json.loads((Path(tmp) / "bubble_batching_receipt.json").read_text())
            self.assertTrue(result["checks"]["all_sorted"])
            self.assertFalse(result["checks"]["positive_preliminary_signal"])
            self.assertEqual(receipt["sha256"], result["sha256"])


if __name__ == "__main__":
    unittest.main()
