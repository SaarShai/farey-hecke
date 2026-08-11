"""Validation-only contract tests for the V7 development probe."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from .controller_v6 import V6_ACTIONS, V6_BUDGET, V6LinearQ, collect_trajectory
from .controller_v7_dev import (
    FEEDBACK_MODES,
    MC_KIND,
    TILE_KIND,
    TD_KIND,
    MonteCarloQ,
    PublicEpisode,
    PublicStream,
    _replay_mc,
    _replay_td,
    aggregate_rows,
    compact_result,
    result_markdown,
    run_dev,
    tile_features,
    TileMonteCarloQ,
    train_lane,
)
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class ControllerV7DevTests(unittest.TestCase):
    @staticmethod
    def task(seed: int, goal: GoalState) -> RepairTask:
        return RepairTask(6, DamagePattern.RANDOM_ISOLATED, goal, seed, 2)

    def tasks(self) -> tuple[RepairTask, ...]:
        return (
            self.task(1, GoalState.COVERAGE),
            self.task(2, GoalState.SPECTRAL),
            self.task(3, GoalState.SPECTRAL),
            self.task(4, GoalState.COVERAGE),
        )

    def test_public_stream_preserves_fixed_budget_without_task_fields_in_view(self) -> None:
        episode = PublicEpisode(self.task(7, GoalState.COVERAGE))
        first = episode.fresh_environment()
        self.assertEqual(first._remaining, V6_BUDGET)
        self.assertEqual(len(first.view.as_tuple()), 10)
        self.assertNotIn("target", first.view.__dataclass_fields__)
        self.assertEqual(len(tuple(PublicStream(self.tasks()))), 4)

    def test_mc_return_propagates_late_reward_where_one_pass_td_does_not(self) -> None:
        trajectory = collect_trajectory(PublicEpisode(self.task(9, GoalState.SPECTRAL)).fresh_environment(), seed=4)
        # Keep the same transitions, but make only the final transmitted reward
        # nonzero.  This isolates temporal credit assignment, not geometry.
        rewards = tuple(0.0 for _ in trajectory.steps[:-1]) + (1.0,)
        altered = replace(
            trajectory,
            steps=tuple(replace(step, reward=reward) for step, reward in zip(trajectory.steps, rewards)),
        )
        td_probe = V6LinearQ(1)
        _replay_td(td_probe, altered, "true", 4)
        mc = MonteCarloQ(1)
        _replay_mc(mc, altered, "true", 4)
        first_action = altered.steps[0].action
        first_index = V6_ACTIONS.index(first_action)
        first_features = altered.steps[0].view.features()
        self.assertNotEqual(sum(mc._weights[first_index][i] * first_features[i] for i in range(len(first_features))), 0.0)
        td_value = sum(td_probe._weights[first_index][i] * first_features[i] for i in range(len(first_features)))
        self.assertEqual(td_value, 0.0)
        self.assertNotEqual(mc_value := sum(mc._weights[first_index][i] * first_features[i] for i in range(len(first_features))), 0.0)

    def test_matched_lanes_have_equal_updates_and_schedules(self) -> None:
        tasks = self.tasks()
        lanes = {
            (kind, mode): train_lane(kind, mode, tasks, learner_seed=3, behavior_seed=17)
            for kind in (TD_KIND, MC_KIND)
            for mode in FEEDBACK_MODES
        }
        schedules = {
            tuple(tuple(step.action for step in trajectory.steps) for trajectory in lane.trajectories)
            for lane in lanes.values()
        }
        self.assertEqual(len(schedules), 1)
        self.assertEqual({lane.update_delta for lane in lanes.values()}, {len(tasks) * V6_BUDGET})
        self.assertNotEqual(lanes[(MC_KIND, "true")].transmitted_rewards, lanes[(MC_KIND, "within_episode_permuted")].transmitted_rewards)
        self.assertNotEqual(lanes[(MC_KIND, "true")].after_digest, lanes[(MC_KIND, "zero")].after_digest)

    def test_tile_variant_is_fixed_coarse_and_matched(self) -> None:
        view = PublicEpisode(self.task(5, GoalState.SPECTRAL)).fresh_environment().view
        self.assertEqual(tile_features(view), tile_features(view))
        self.assertGreater(len(tile_features(view)), len(view.features()))
        lane = train_lane(TILE_KIND, "true", self.tasks(), learner_seed=2, behavior_seed=19)
        self.assertEqual(lane.update_delta, 4 * V6_BUDGET)
        self.assertFalse(lane.controller.learning)

    def test_aggregation_keys_are_learner_seed_and_cell(self) -> None:
        rows = [
            {"learner_seed": 2, "cell": "N6:random_isolated:coverage", "N": 6, "family": "random_isolated", "goal": "coverage", "precision": 1.0, "recall": 0.5, "f1": 0.5, "exact": 0.0},
            {"learner_seed": 2, "cell": "N6:random_isolated:coverage", "N": 6, "family": "random_isolated", "goal": "coverage", "precision": 0.0, "recall": 0.5, "f1": 0.5, "exact": 1.0},
        ]
        aggregate = aggregate_rows(rows)
        self.assertEqual(len(aggregate), 1)
        self.assertEqual((aggregate[0]["seed"], aggregate[0]["cell"], aggregate[0]["task_count"]), (2, "N6:random_isolated:coverage", 2))

    def test_validation_probe_writes_only_temp_dev_outputs_and_no_test_access(self) -> None:
        tasks = self.tasks()
        with TemporaryDirectory() as directory:
            result = run_dev(
                train_tasks=tasks,
                validation_tasks=tasks,
                learner_seeds=(0, 1),
                output_dir=Path(directory),
            )
            self.assertEqual(result["costs"]["test_openings"], 0)
            self.assertEqual(result["costs"]["test_updates"], 0)
            self.assertTrue((Path(directory) / "controller_v7_dev_receipt.json").exists())
            self.assertTrue((Path(directory) / "V7_DEV_RESULTS.md").exists())
            self.assertIn("offline reward-attribution", result_markdown(result))
            self.assertIn("coarse interaction/tile variant", result_markdown(result))
            self.assertIn("tile", result["gates"])
            compact = compact_result(result)
            self.assertNotIn("validation_task_rows", compact)
            self.assertEqual(set(compact["validation_variants"]), {"mc", "tile"})
            self.assertTrue(all("task_rows" not in variant for variant in compact["validation_variants"].values()))
            self.assertEqual(compact, compact_result(result))
            written = (Path(directory) / "controller_v7_dev_receipt.json").read_text(encoding="utf-8")
            self.assertLess(len(written), 500_000)
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                run_dev(train_tasks=tasks, validation_tasks=tasks, learner_seeds=(0,), output_dir=Path(directory))


if __name__ == "__main__":
    unittest.main()
