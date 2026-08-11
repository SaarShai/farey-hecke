"""Contract tests for the V8 online development probe."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from .controller_v4 import ControllerView
from .controller_v8_dev import (
    ACTION_BUDGET,
    ACTION_COUNT,
    FEEDBACK_MODES,
    OnlineTileQ,
    aggregate_rows,
    compact_result,
    derangement_diagnostic,
    _make_v6_split,
    online_features,
    paired_hierarchical_bootstrap,
    run_dev,
    train_matched_lanes,
    verify_manifest_reconstruction,
)
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class ControllerV8DevTests(unittest.TestCase):
    @staticmethod
    def task(seed: int, goal: GoalState) -> RepairTask:
        return RepairTask(6, DamagePattern.RANDOM_ISOLATED, goal, seed, 2)

    def tasks(self) -> tuple[RepairTask, ...]:
        return (
            self.task(1, GoalState.COVERAGE),
            self.task(2, GoalState.SPECTRAL),
            self.task(3, GoalState.COVERAGE),
            self.task(4, GoalState.SPECTRAL),
        )

    def test_online_view_features_are_fixed_width_and_public(self) -> None:
        view = ControllerView((1, 2, 3, 4), (5, 6), -1, 0.5, 0.0, 1)
        self.assertEqual(len(online_features(view)), len(online_features(view)))
        self.assertEqual(len(online_features(view)), len(view.features()) + 64)
        self.assertNotIn("target", view.__dataclass_fields__)
        self.assertEqual(ACTION_COUNT, 18)
        self.assertEqual(ACTION_BUDGET, 16)

    def test_matched_online_lanes_share_seeds_and_updates(self) -> None:
        lanes = train_matched_lanes(self.tasks(), learner_seed=3, behavior_seed=19)
        self.assertEqual(set(lanes), set(FEEDBACK_MODES))
        self.assertEqual({lane.update_delta for lane in lanes.values()}, {len(self.tasks()) * ACTION_BUDGET})
        self.assertEqual({lane.episode_seed_digest for lane in lanes.values()}, {lanes["true"].episode_seed_digest})
        self.assertEqual({lane.action_seed_digest for lane in lanes.values()}, {lanes["true"].action_seed_digest})
        self.assertGreater(lanes["true"].transmitted_nonzero_count, 0)
        self.assertNotEqual(lanes["true"].transmitted_reward_digest, lanes["causal_lagged_null"].transmitted_reward_digest)
        self.assertGreater(len({lane.after_digest for lane in lanes.values()}), 1)
        self.assertTrue(all(not lane.controller.learning for lane in lanes.values()))

    def test_bootstrap_resamples_both_group_levels(self) -> None:
        treatment = []
        control = []
        for seed in (0, 1, 2):
            for cell, value in (("a", 1.0 + seed), ("b", 2.0 + seed)):
                treatment.append({"learner_seed": seed, "cell": cell, "f1": value})
                control.append({"learner_seed": seed, "cell": cell, "f1": 0.0})
        result = paired_hierarchical_bootstrap(treatment, control, resamples=200, seed=7)
        self.assertEqual((result.groups, result.pairs), (3, 6))
        self.assertEqual(result, paired_hierarchical_bootstrap(treatment, control, resamples=200, seed=7))
        self.assertGreater(result.ci_high, result.ci_low)

    def test_g_only_diagnostic_reports_effective_intervention_and_arms(self) -> None:
        diagnostic = derangement_diagnostic(self.tasks())
        self.assertTrue(diagnostic["valid"])
        self.assertGreater(diagnostic["effective_geometry_change_rate"], 0.0)
        self.assertEqual(set(diagnostic["arms"]), {"I→I", "I→S", "S→I", "S→S"})
        self.assertTrue(diagnostic["own_u_preserved"])
        self.assertTrue(diagnostic["physical_states_equal"])
        self.assertTrue(diagnostic["rewards_equal"])

    def test_v6_train_validation_reconstruction_is_deterministically_committed(self) -> None:
        root = Path(__file__).resolve().parent
        import json

        receipt = json.loads((root / "competency_v6_final_manifest_receipt.json").read_text(encoding="utf-8"))
        result = verify_manifest_reconstruction(_make_v6_split("train"), _make_v6_split("validation"), receipt)
        self.assertTrue(result["verified"])
        self.assertEqual(result["splits"]["train"]["count"], 240)
        self.assertEqual(result["splits"]["validation"]["count"], 120)
        self.assertTrue(all(item["deterministic"] for item in result["splits"].values()))

    def test_compact_temp_run_and_aggregation(self) -> None:
        tasks = self.tasks()
        with TemporaryDirectory() as directory:
            result = run_dev(train_tasks=tasks, validation_tasks=tasks, learner_seeds=(2, 4), output_dir=Path(directory))
            compact = compact_result(result)
            task_rows = result["validation_variants"]["online"]["task_rows"]
            self.assertNotIn("validation_task_rows", compact)
            self.assertEqual(set(compact["validation_variants"]), {"online"})
            self.assertEqual(set(compact["omitted_task_rows"]["validation"]), set(task_rows))
            self.assertTrue(all(item["count"] == len(task_rows[name]) for name, item in compact["omitted_task_rows"]["validation"].items()))
            self.assertTrue(all(item["sha256_scope"] == "task_rows" for item in compact["omitted_task_rows"]["validation"].values()))
            self.assertTrue((Path(directory) / "controller_v8_dev_receipt.json").exists())
            self.assertTrue((Path(directory) / "V8_DEV_RESULTS.md").exists())
            self.assertLess((Path(directory) / "controller_v8_dev_receipt.json").stat().st_size, 500_000)
            import json

            written_result = json.loads((Path(directory) / "controller_v8_dev_receipt.json").read_text(encoding="utf-8"))
            self.assertNotIn("validation_cells", written_result["counts"])
            self.assertEqual(written_result["counts"]["logical_validation_cells"], 2)
            self.assertEqual(written_result["counts"]["validation_seed_cell_aggregates"], 4)
            bootstrap = written_result["gates"]["feedback"]["comparisons"]["causal_lagged_null"]
            self.assertEqual(set(bootstrap), {"effect", "ci_low", "ci_high", "groups", "pairs"})
            self.assertEqual(len(result["validation_aggregated_rows"]["true"]), len(result["validation_aggregated_rows"]["random"]))
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                run_dev(train_tasks=tasks, validation_tasks=tasks, learner_seeds=(0,), output_dir=Path(directory))

    def test_aggregate_keys_include_learner_seed_and_cell(self) -> None:
        rows = [
            {"learner_seed": 2, "cell": "N6:x:coverage", "N": 6, "family": "x", "goal": "coverage", "precision": 1.0, "recall": 0.5, "f1": 0.5, "exact": 0.0},
            {"learner_seed": 2, "cell": "N6:x:coverage", "N": 6, "family": "x", "goal": "coverage", "precision": 0.0, "recall": 0.5, "f1": 0.5, "exact": 1.0},
        ]
        aggregate = aggregate_rows(rows)
        self.assertEqual((aggregate[0]["learner_seed"], aggregate[0]["cell"], aggregate[0]["task_count"]), (2, "N6:x:coverage", 2))


if __name__ == "__main__":
    unittest.main()
