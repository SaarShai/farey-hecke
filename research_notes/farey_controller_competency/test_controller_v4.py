"""Contract tests for the compact V4 controller harness."""

from __future__ import annotations

from dataclasses import fields
from fractions import Fraction
import unittest

try:
    from .controller_v4 import (
        ACTION_BUDGET,
        V4_ACTIONS,
        ControllerView,
        FixedRandom,
        LinearQ,
        LocalHeuristic,
        VisibleGreedy,
        controller_geometry,
        collect_trajectory,
        derange_controller_views,
        _geometry_tuple,
        derange_whole_geometry_batch,
        episode_feedback,
        evaluator_metrics,
        geometry_multiset,
        replay_trajectory,
        run_episode,
        task_environment,
    )
    from .repair_experiment import RepairTask
    from .strict_environment import DamagePattern, GoalState
except ImportError:
    from controller_v4 import (  # type: ignore[no-redef]
        ACTION_BUDGET,
        V4_ACTIONS,
        ControllerView,
        FixedRandom,
        LinearQ,
        LocalHeuristic,
        VisibleGreedy,
        controller_geometry,
        collect_trajectory,
        derange_controller_views,
        _geometry_tuple,
        derange_whole_geometry_batch,
        episode_feedback,
        evaluator_metrics,
        geometry_multiset,
        replay_trajectory,
        run_episode,
        task_environment,
    )
    from repair_experiment import RepairTask  # type: ignore[no-redef]
    from strict_environment import DamagePattern, GoalState  # type: ignore[no-redef]


def _task(seed: int = 19) -> RepairTask:
    return RepairTask(6, DamagePattern.RANDOM_ISOLATED, GoalState.COVERAGE, seed, 2)


class ControllerV4Tests(unittest.TestCase):
    def test_fixed_v34_vocabulary_and_eight_charged_steps(self) -> None:
        self.assertEqual(len(V4_ACTIONS), 12)
        self.assertEqual(ACTION_BUDGET, 8)
        result = run_episode(FixedRandom(4), _task())
        self.assertEqual(result["charged"], ACTION_BUDGET)
        self.assertEqual(result["updates"], 0)

    def test_reward_masking_is_exact_and_has_equal_update_counts(self) -> None:
        rewards = (0.25, -0.1, 0.03, 0.7)
        self.assertEqual(episode_feedback(rewards, "true", 7), rewards)
        self.assertEqual(episode_feedback(rewards, "zero", 7), (0.0,) * len(rewards))
        permuted = episode_feedback(rewards, "within_episode_permuted", 7)
        self.assertEqual(sorted(permuted), sorted(rewards))
        self.assertTrue(all(left != right for left, right in zip(rewards, permuted)))
        results = []
        for mode in ("true", "within_episode_permuted", "zero"):
            learner = LinearQ(31)
            result = run_episode(learner, _task(), feedback_mode=mode)
            results.append((result["charged"], learner.updates))
        self.assertEqual(results, [(8, 8), (8, 8), (8, 8)])

    def test_reward_lanes_replay_identical_transitions(self) -> None:
        trajectory = collect_trajectory(_task(41), seed=99)
        action_schedule = tuple(step.action for step in trajectory.steps)
        for mode in ("true", "within_episode_permuted", "zero"):
            learner = LinearQ(99)
            delivered = replay_trajectory(learner, trajectory, mode, seed=101)
            self.assertEqual(len(delivered), ACTION_BUDGET)
            self.assertEqual(tuple(step.action for step in trajectory.steps), action_schedule)
            self.assertEqual(learner.updates, ACTION_BUDGET)

    def test_freeze_blocks_updates_and_preserves_digest(self) -> None:
        learner = LinearQ(3)
        run_episode(learner, _task(5), feedback_mode="true")
        digest = learner.digest()
        updates = learner.updates
        learner.freeze()
        run_episode(learner, _task(6), feedback_mode="true")
        self.assertEqual(learner.digest(), digest)
        self.assertEqual(learner.updates, updates)

    def test_view_has_fixed_shape_and_no_hidden_evaluator_fields(self) -> None:
        view = task_environment(_task()).view
        self.assertIsInstance(view, ControllerView)
        self.assertEqual(view.shape, (4, 2, 1, 1, 1, 1))
        self.assertEqual(len(view.as_tuple()), 10)
        fields_seen = {field.name for field in fields(ControllerView)}
        self.assertTrue(fields_seen.isdisjoint({"order", "n", "target", "damage", "fractions", "f1", "exact", "points"}))
        self.assertFalse(any(isinstance(value, Fraction) for value in view.as_tuple()))

    def test_evaluator_identity_is_not_in_view(self) -> None:
        environment = task_environment(_task(8))
        hidden = evaluator_metrics(environment)
        self.assertGreaterEqual(hidden.f1, 0.0)
        self.assertIn(hidden.exact, (0.0, 1.0))
        self.assertNotIn("f1", {field.name for field in fields(ControllerView)})
        self.assertNotIn("exact", {field.name for field in fields(ControllerView)})

    def test_controller_derangement_swaps_only_g_and_preserves_u(self) -> None:
        environments = [task_environment(_task(seed)) for seed in (10, 11, 12)]
        views = tuple(environment.view for environment in environments)
        output = derange_controller_views(views, seed=17)
        self.assertEqual(
            sorted(controller_geometry(view) for view in views),
            sorted(controller_geometry(view) for view in output),
        )
        self.assertTrue(all(controller_geometry(left) != controller_geometry(right) for left, right in zip(views, output)))
        for original, observed in zip(views, output):
            self.assertEqual(
                (original.remaining_budget_fraction, original.last_scalar_reward, original.trusted_goal),
                (observed.remaining_budget_fraction, observed.last_scalar_reward, observed.trusted_goal),
            )

    def test_whole_geometry_derangement_preserves_multiset_and_is_batch_deranged(self) -> None:
        environments = [task_environment(_task(seed)) for seed in (1, 2, 3, 4)]
        source = tuple(_geometry_tuple(environment) for environment in environments)
        output = derange_whole_geometry_batch(source, seed=9)
        self.assertEqual(geometry_multiset(source), geometry_multiset(output))
        self.assertTrue(all(left != right for left, right in zip(source, output)))
        self.assertTrue(all(sum(gaps, Fraction(0)) == 1 for gaps in output))

    def test_derangement_does_not_change_physical_rewards_or_action_reachability(self) -> None:
        task = _task(23)
        first, second = task_environment(task), task_environment(task)
        actions = V4_ACTIONS
        first_rewards = [first.step(action) for action in actions[:ACTION_BUDGET]]
        second_rewards = [second.step(action) for action in actions[:ACTION_BUDGET]]
        self.assertEqual(first_rewards, second_rewards)
        self.assertEqual(first._remaining, 0)
        self.assertEqual(second._remaining, 0)
        self.assertEqual(set(actions), set(V4_ACTIONS))

    def test_baselines_share_the_same_view_boundary(self) -> None:
        view = task_environment(_task(29)).view
        for baseline in (FixedRandom(1), LocalHeuristic(), VisibleGreedy()):
            self.assertIn(baseline.choose(view), V4_ACTIONS)


if __name__ == "__main__":
    unittest.main()
