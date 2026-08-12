"""Focused integrity and replay tests for the Farey-guided experiment."""

from __future__ import annotations

from pathlib import Path
import unittest

try:
    from .experiment import (
        GATE_METRICS,
        ExperimentConfig,
        RELATIVE_ACTIONS,
        SYMBOLS,
        build_tasks,
        cyclic_run_signature,
        exact_count_permutation,
        euler_transition_surrogate,
        evaluate_discovery_confirmation,
        farey_denominator_chain,
        open_grid,
        rank_balanced_word,
        run_experiment,
        run_length_surrogate,
        sign_permutation_pvalue,
        simulate_episode,
        tape_signature,
        transition_signature,
        verify_farey_bcz,
    )
except ImportError:  # unittest discover with this directory as top-level
    from experiment import (
    GATE_METRICS,
    ExperimentConfig,
    RELATIVE_ACTIONS,
    SYMBOLS,
    build_tasks,
    cyclic_run_signature,
    exact_count_permutation,
    euler_transition_surrogate,
    evaluate_discovery_confirmation,
    farey_denominator_chain,
    open_grid,
    rank_balanced_word,
    run_experiment,
    run_length_surrogate,
    sign_permutation_pvalue,
    simulate_episode,
    tape_signature,
    transition_signature,
    verify_farey_bcz,
    )


class FareyIntegrityTests(unittest.TestCase):
    def test_exact_denominator_and_bcz_recurrence(self):
        result = verify_farey_bcz(13)
        self.assertTrue(result["exact_denominator_recurrence"])
        self.assertTrue(result["bcz_recurrence"])
        self.assertEqual(farey_denominator_chain(5), (1, 5, 4, 3, 5, 2, 5, 3, 4, 5, 1))

    def test_rank_balanced_quartiles(self):
        word = rank_balanced_word(37, 96, 9)
        self.assertEqual(len(word), 96)
        self.assertEqual(tuple(word.count(symbol) for symbol in SYMBOLS), (24, 24, 24, 24))
        self.assertEqual(set(word), set(SYMBOLS))

    def test_controls_preserve_their_claimed_signatures(self):
        genuine = rank_balanced_word(37, 96, 5)
        counts = tape_signature(genuine)["counts"]
        runs = cyclic_run_signature(genuine)
        transitions = transition_signature(genuine)
        control_c = exact_count_permutation(genuine, 883)
        control_r = run_length_surrogate(genuine, 884)
        control_k2 = euler_transition_surrogate(genuine, 885)
        self.assertEqual(tape_signature(control_c)["counts"], counts)
        self.assertEqual(cyclic_run_signature(control_r), runs)
        self.assertEqual(transition_signature(control_k2), transitions)
        self.assertNotEqual(control_c, genuine)
        self.assertNotEqual(control_r, genuine)
        self.assertNotEqual(control_k2, genuine)


class EnvironmentTests(unittest.TestCase):
    def test_families_connected_and_perturbation_preserves_connectivity(self):
        config = ExperimentConfig(width=7, height=7, dev_seeds=(7,), heldout_seeds=(17,), horizon=16, perturbation_step=8)
        tasks = build_tasks(config)
        self.assertEqual({task.family for task in tasks}, {"dfs", "prim"})
        for task in tasks:
            self.assertTrue(task.maze.connected())
            self.assertTrue(task.maze.with_closed_edge(task.perturbation_edge).connected())

    def test_fixed_horizon_and_blocked_noop(self):
        maze = open_grid(3, 3)
        result = simulate_episode(maze, (0, 0), 0, (0, 0, 0, 0), RELATIVE_ACTIONS, horizon=4)
        self.assertEqual(result["horizon"], 4)
        self.assertEqual(result["blocked_actions"], 4)
        self.assertEqual(result["positions"], ((0, 0),) * 5)

    def test_open_grid_path_fixture(self):
        maze = open_grid(3, 3)
        result = simulate_episode(maze, (0, 0), 1, (0, 0), RELATIVE_ACTIONS, horizon=2)
        self.assertEqual(result["positions"], ((0, 0), (1, 0), (2, 0)))
        self.assertEqual(result["metrics"]["unique_cell_coverage"], 3)
        self.assertEqual(result["metrics"]["blocked_rate"], 0.0)

    def test_frontier_return_interval_uses_actual_frontier_returns(self):
        maze = open_grid(3, 3)
        mapping = ("F", "B", "L", "R")
        result = simulate_episode(maze, (1, 1), 1, (0, 1, 1), mapping, horizon=3)
        self.assertEqual(result["frontier_return_events"], (2, 3))
        self.assertEqual(result["metrics"]["frontier_return_interval_mean"], 1.0)
        self.assertEqual(result["metrics"]["frontier_return_hazard"], 2 / 3)

    def test_longest_no_new_cell_streak_counts_actions_not_event_gaps(self):
        maze = open_grid(3, 3)
        mapping = ("F", "B", "L", "R")
        result = simulate_episode(maze, (0, 0), 1, (1, 0), mapping, horizon=2)
        self.assertEqual(result["positions"], ((0, 0), (0, 0), (1, 0)))
        self.assertEqual(result["metrics"]["longest_no_new_cell_streak"], 1)


class GateAndReplayTests(unittest.TestCase):
    def test_discovery_confirmation_negative_fixture(self):
        metrics = {metric: 1.0 for metric in GATE_METRICS}
        rows = []
        for split in ("development", "heldout"):
            for task_index in range(3):
                for arm in ("G", "K2"):
                    rows.append({"task_id": f"{split}-{task_index}", "split": split,
                                 "mapping_id": "m00", "arm": arm, "metrics": dict(metrics)})
        result = evaluate_discovery_confirmation(rows, ("m00",), alpha=0.05)
        self.assertEqual(result["label"], "unverified_underpowered")
        self.assertFalse(result["discovery_capable"])
        self.assertTrue(result["discovery"])
        self.assertFalse(any(item["candidate"] for item in result["discovery"]))
        self.assertEqual(result["confirmation"], [])

    def test_resampled_sign_test_is_deterministic_at_v2_size(self):
        differences = tuple(float(index + 1) for index in range(24))
        first = sign_permutation_pvalue(differences, resamples=20_000, seed=77)
        second = sign_permutation_pvalue(differences, resamples=20_000, seed=77)
        self.assertEqual(first, second)
        self.assertLessEqual(first, 0.05)

    def test_replay_is_deterministic_and_receipt_invariants_pass(self):
        config = ExperimentConfig(width=5, height=5, horizon=16, perturbation_step=8,
                                  dev_seeds=(3,), heldout_seeds=(13,), control_replicates=1)
        first = run_experiment(config)
        second = run_experiment(config)
        self.assertEqual(first["receipt"], second["receipt"])
        self.assertEqual(first["rows"], second["rows"])
        invariants = first["receipt"]["tape_invariants"]
        self.assertTrue(invariants["genuine_rank_balanced"])
        self.assertTrue(invariants["C_exact_counts"])
        self.assertTrue(invariants["R_exact_typed_cyclic_run_multiset"])
        self.assertTrue(invariants["K2_exact_cyclic_transition_counts"])
        perturbation = first["receipt"]["perturbation_invariants"]
        self.assertTrue(perturbation["all_tasks_connectivity_preserved"])
        self.assertTrue(perturbation["all_rows_use_locked_step"])
        self.assertTrue(perturbation["same_edge_across_arms"])

    def test_no_legacy_experiment_reference(self):
        source = Path(__file__).with_name("experiment.py").read_text()
        legacy_name = "_".join(("farey", "controller", "competency"))
        self.assertNotIn(legacy_name, source)


if __name__ == "__main__":
    unittest.main()
