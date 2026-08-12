import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from .probe import CONDITIONS, farey_tokens, perturb_restart, run, run_experiment


class FareyNativeProbeTests(unittest.TestCase):
    def test_farey_tokens_are_reduced_and_deterministic(self):
        first, second = farey_tokens(), farey_tokens()
        self.assertEqual(first, second)
        self.assertTrue(all(token.gap > 0 for token in first))

    def test_all_conditions_reach_coarse_objective(self):
        for condition in CONDITIONS:
            final, _, _ = run(list(farey_tokens()), condition, 1)
            self.assertEqual(sum(a.gap_bin > b.gap_bin for a, b in zip(final, final[1:])), 0)

    def test_perturbation_preserves_objective(self):
        final, _, _ = run(list(farey_tokens()), "farey_stable", 2)
        result = perturb_restart(final, 3)
        self.assertTrue(result["applied"])
        self.assertEqual(result["after"]["coarse_error"], 0)

    def test_experiment_is_deterministic_and_invariant_checked(self):
        first = run_experiment()
        second = run_experiment()
        self.assertEqual(first, second)
        self.assertTrue(first["invariants"]["same_exact_gap_multiset"])
        self.assertTrue(first["checks"]["all_objectives_reached"])
        json.dumps(first)

    def test_receipt_writer(self):
        with TemporaryDirectory() as directory:
            result = run_experiment(Path(directory))
            receipt = json.loads((Path(directory) / "receipt.json").read_text())
            self.assertEqual(receipt, result)


if __name__ == "__main__":
    unittest.main()
