import json
import unittest

try:
    from .probe import CONDITIONS, N, SEED, coarse_error, initial_state, perturb_restart, run, run_experiment
except ImportError:  # Direct execution from this directory.
    from probe import CONDITIONS, N, SEED, coarse_error, initial_state, perturb_restart, run, run_experiment


class CoarseBinProbeTests(unittest.TestCase):
    def test_every_condition_reaches_coarse_objective(self) -> None:
        for condition in CONDITIONS:
            state, _, _ = run(initial_state(SEED, shuffle_labels=condition == "shuffled_labels"), condition, seed=SEED)
            self.assertEqual(coarse_error(state), 0, condition)

    def test_role_tie_has_more_unnecessary_within_bin_adjacency_than_controls(self) -> None:
        result = run_experiment()["summaries"]
        role = result["role_tie"]["final_within_bin_same_label_rate"]["mean"]
        randomized = result["randomized_ties"]["final_within_bin_same_label_rate"]["mean"]
        anti = result["anti_clustering"]["final_within_bin_same_label_rate"]["mean"]
        self.assertGreater(role, randomized + 0.10)
        self.assertGreater(role, anti + 0.10)

    def test_objective_does_not_require_fine_sorting(self) -> None:
        state, _, _ = run(initial_state(SEED, shuffle_labels=False), "role_tie", seed=SEED)
        self.assertEqual(coarse_error(state), 0)
        self.assertLess(sum(state[i].value > state[i + 1].value for i in range(N - 1)), N - 1)

    def test_perturbation_restart_is_applied_and_recovers_objective(self) -> None:
        state, _, _ = run(initial_state(SEED, shuffle_labels=False), "role_tie", seed=SEED)
        result = perturb_restart(state, seed=SEED + 1)
        self.assertTrue(result["applied"])
        self.assertEqual(result["after"]["coarse_error"], 0)

    def test_experiment_is_deterministic_and_json_serializable(self) -> None:
        first = run_experiment()
        second = run_experiment()
        self.assertEqual(first, second)
        json.dumps(first)


if __name__ == "__main__":
    unittest.main()
