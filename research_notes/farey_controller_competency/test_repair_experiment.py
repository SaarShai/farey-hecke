"""Boundary, manifest, ablation, and small-run tests for repair_experiment."""

from dataclasses import fields, replace
from fractions import Fraction
import unittest

from .repair_experiment import (
    ACTION_BUDGET,
    DEFAULT_CONFIG,
    GOALS,
    TEST_ORDERS,
    TEST_PATTERNS,
    CoarseRepairView,
    ExperimentConfig,
    LocalGapMediant,
    RepairTask,
    RewardLearner,
    _gate,
    _hidden_repair_metrics,
    _initial_action_reachability,
    _structural_proof,
    _task_environment,
    coarse_view,
    complete_cells,
    make_manifest,
    run_episode,
    run_experiment,
)


class RepairExperimentTests(unittest.TestCase):
    def test_coarse_view_is_fixed_and_has_no_evaluator_fields(self) -> None:
        view = coarse_view(_task_environment(RepairTask(7, TEST_PATTERNS[0], GOALS[0], 31, 2), "farey").observation)
        self.assertEqual(len(view.features()), 11)
        self.assertTrue(all(not isinstance(value, Fraction) for value in view.features()))
        forbidden = {"order", "n", "fraction", "target", "survivor", "menu", "delete", "identity", "metric", "arm", "family"}
        self.assertTrue({field.name for field in fields(CoarseRepairView)}.isdisjoint(forbidden))

    def test_larger_test_manifest_is_complete_and_balanced(self) -> None:
        tasks = make_manifest(TEST_ORDERS, TEST_PATTERNS, damage_count=4, replicates=10, seed=99)
        self.assertEqual(len(tasks), 3 * 3 * 2 * 10)
        self.assertTrue(complete_cells(tasks, replicates=10))
        self.assertEqual({task.damage_count for task in tasks}, {4})

    def test_hidden_metrics_are_evaluator_only_and_actions_are_charged(self) -> None:
        task = RepairTask(8, TEST_PATTERNS[0], GOALS[0], 91, 2)
        row = run_episode(LocalGapMediant(), task)
        self.assertLessEqual(row["charged_actions"], ACTION_BUDGET)
        self.assertEqual(row["cost"], row["charged_actions"])
        self.assertTrue(0.0 <= row["precision"] <= 1.0)
        self.assertTrue(0.0 <= row["recall"] <= 1.0)
        self.assertTrue(0.0 <= row["f1"] <= 1.0)
        hidden = _hidden_repair_metrics(_task_environment(task, "farey"))
        self.assertNotIn("f1", {field.name for field in fields(CoarseRepairView)})
        self.assertEqual(hidden.deleted_count, 2)

    def test_exact_gap_adapter_preserves_structure_and_maps_rank_damage(self) -> None:
        task = RepairTask(11, TEST_PATTERNS[1], GOALS[1], 123, 4)
        farey = _task_environment(task, "farey")
        scrambled = _task_environment(task, "scramble")
        self.assertEqual(len(farey._target), len(scrambled._target))
        self.assertEqual(len(farey._deleted_indices), len(scrambled._deleted_indices))
        self.assertEqual(len(coarse_view(farey.observation).features()), len(coarse_view(scrambled.observation).features()))
        proof = _structural_proof([task])
        self.assertTrue(proof["all_same_exact_gap_multiset"])
        self.assertTrue(proof["all_same_rank_mask_count"])

    def test_reachability_is_a_direct_initial_state_diagnostic(self) -> None:
        task = RepairTask(11, TEST_PATTERNS[0], GOALS[0], 123, 4)
        farey = _initial_action_reachability(_task_environment(task, "farey"))
        scrambled = _initial_action_reachability(_task_environment(task, "scramble"))
        self.assertTrue(0.0 <= farey <= 1.0)
        self.assertTrue(0.0 <= scrambled <= 1.0)
        self.assertGreater(farey, scrambled)

    def test_nondefault_action_budget_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            replace(DEFAULT_CONFIG, action_budget=7)

    def test_gate_negative_fixture_proves_a_gate_can_trip(self) -> None:
        treatment = [{"f1": 0.0} for _ in range(12)]
        control = [{"f1": 1.0} for _ in range(12)]
        gate = _gate(
            "negative_fixture",
            treatment,
            {"control": control},
            key="f1",
            margin=0.03,
            valid=True,
            reason="test fixture",
            config=replace(DEFAULT_CONFIG, bootstrap_resamples=20),
        )
        self.assertEqual(gate["status"], "negative")

    def test_small_experiment_freezes_before_test_updates(self) -> None:
        config = replace(
            DEFAULT_CONFIG,
            train_episodes=80,
            train_replicates_per_order_goal=2,
            in_domain_replicates_per_order_goal=1,
            test_replicates_per_cell=1,
            bootstrap_resamples=40,
        )
        result = run_experiment(config)
        self.assertEqual(result["model"]["measured_test_updates"], {"true": 0, "prior_reward_shuffled": 0, "zero": 0})
        self.assertTrue(result["predeclaration"]["test"]["complete_cells"])
        self.assertIn(result["gates"]["core_conjunction"]["status"], {"positive", "null", "negative", "unverified"})
        expected_updates = config.train_episodes * ACTION_BUDGET
        self.assertEqual(set(result["model"]["training_updates"].values()), {expected_updates})


if __name__ == "__main__":
    unittest.main()
