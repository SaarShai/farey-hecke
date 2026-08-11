"""Contract tests for the V6 controller/experiment engine.

The fixtures use only public stream adapters and synthetic evaluator rows.  No
sealed task manifest or private test label is imported here.
"""

from __future__ import annotations

from dataclasses import fields
from fractions import Fraction
import unittest
from unittest.mock import patch

try:
    from . import controller_v6
    from .controller_v6 import (
        FEEDBACK_MODES,
        MATCHED_SEED_COUNT,
        V6_ACTIONS,
        V6_BUDGET,
        BatchRollout,
        ControllerView,
        V6Environment,
        V6LinearQ,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        controller_geometry,
        core_conjunction,
        derange_controller_views,
        episode_feedback,
        evaluate_frozen_lanes,
        evaluate_structural_lanes,
        feedback_gate,
        paired_hierarchical_bootstrap,
        recovery_gate,
        structural_gate,
        synchronous_structural_rollout,
        train_reward_lanes,
        train_structural_lanes,
        transfer_gate,
    )
    from .strict_environment import DamagePattern, GoalState, StrictEnvironment
except ImportError:
    import controller_v6  # type: ignore[no-redef]
    from controller_v6 import (  # type: ignore[no-redef]
        FEEDBACK_MODES,
        MATCHED_SEED_COUNT,
        V6_ACTIONS,
        V6_BUDGET,
        BatchRollout,
        ControllerView,
        V6Environment,
        V6LinearQ,
        V6Local,
        V6Random,
        V6VisibleGreedy,
        controller_geometry,
        core_conjunction,
        derange_controller_views,
        episode_feedback,
        evaluate_frozen_lanes,
        evaluate_structural_lanes,
        feedback_gate,
        paired_hierarchical_bootstrap,
        recovery_gate,
        structural_gate,
        synchronous_structural_rollout,
        train_reward_lanes,
        train_structural_lanes,
        transfer_gate,
    )
    from strict_environment import DamagePattern, GoalState, StrictEnvironment  # type: ignore[no-redef]


class Episode:
    def __init__(self, seed: int, goal: GoalState | str = GoalState.COVERAGE) -> None:
        self.seed = seed
        self.goal = goal

    def fresh_environment(self) -> V6Environment:
        strict = StrictEnvironment(
            6,
            DamagePattern.RANDOM_ISOLATED,
            damage_count=2,
            seed=self.seed,
            rotation=True,
            action_budget=V6_BUDGET,
            goal=self.goal,
        )
        return V6Environment.from_strict(strict)


class Stream:
    def __init__(self, count: int = MATCHED_SEED_COUNT) -> None:
        self.episodes = tuple(
            Episode(index + 1, GoalState.SPECTRAL if index % 2 else GoalState.COVERAGE)
            for index in range(count)
        )

    def __iter__(self):
        return iter(self.episodes)


def _rows(value: float, *, exact: float | None = None):
    exact_value = value if exact is None else exact
    return tuple(
        {
            "seed": seed,
            "cell": f"cell-{cell}",
            "precision": value,
            "recall": value,
            "f1": value,
            "exact": exact_value,
        }
        for seed in range(4)
        for cell in range(2)
    )


class FrozenAccessor:
    def evaluate_frozen(self, policies):
        return {name: _rows(0.5) for name in policies}

    def evaluate_structural_frozen(self, policies):
        return {name: _rows(0.5) for name in policies}


class ControllerV6Tests(unittest.TestCase):
    def test_fixed_v5_boundary_and_exact_transition_shell(self) -> None:
        self.assertEqual(len(V6_ACTIONS), 18)
        self.assertEqual(V6_BUDGET, 16)
        first = Episode(17, GoalState.SPECTRAL).fresh_environment()
        second = Episode(17, GoalState.SPECTRAL).fresh_environment()
        rewards = [first.step(action) for action in V6_ACTIONS[:V6_BUDGET]]
        replayed = [second.step(action) for action in V6_ACTIONS[:V6_BUDGET]]
        self.assertEqual(rewards, replayed)
        self.assertEqual(first._remaining, 0)
        self.assertEqual(first._points, second._points)
        self.assertEqual(first._cursor, second._cursor)

    def test_view_is_fixed_width_and_excludes_exact_evaluator_fields(self) -> None:
        view = Episode(3).fresh_environment().view
        self.assertEqual(view.shape, (4, 2, 1, 1, 1, 1))
        self.assertEqual(len(view.as_tuple()), 10)
        names = {field.name for field in fields(ControllerView)}
        self.assertTrue(names.isdisjoint({"N", "n", "order", "target", "damage", "fractions", "points", "exact", "f1"}))
        self.assertFalse(any(isinstance(value, Fraction) for value in view.as_tuple()))

    def test_goal_coercion_and_non_oracle_baselines(self) -> None:
        view = Episode(4, "spectral").fresh_environment().view
        self.assertEqual(view.trusted_goal, 1)
        for policy in (V6Random(1), V6Local(), V6VisibleGreedy()):
            self.assertIn(policy.choose(view), V6_ACTIONS)
        right = ControllerView((2, 1, 6, 3), (4, 5), 0, 1.0, 0.0, 0)
        left = ControllerView((6, 5, 1, 2), (4, 5), 0, 1.0, 0.0, 0)
        self.assertIn(V6VisibleGreedy().choose(right), V6_ACTIONS)
        self.assertIn(V6VisibleGreedy().choose(left), V6_ACTIONS)

    def test_feedback_masking_is_exact_and_lane_budgets_match(self) -> None:
        rewards = (0.25, -0.1, 0.03, 0.7)
        self.assertEqual(episode_feedback(rewards, "true", 7), rewards)
        self.assertEqual(episode_feedback(rewards, "zero", 7), (0.0,) * len(rewards))
        permuted = episode_feedback(rewards, "within_episode_permuted", 7)
        self.assertEqual(sorted(permuted), sorted(rewards))
        self.assertTrue(all(left != right for left, right in zip(rewards, permuted)))
        lanes = train_reward_lanes(Stream(2), seed=7, init_seed=21)
        self.assertEqual(set(lanes), set(FEEDBACK_MODES))
        self.assertEqual({lane.update_delta for lane in lanes.values()}, {2 * V6_BUDGET})
        self.assertEqual({lane.action_schedule for lane in lanes.values()}, {lanes["true"].action_schedule})
        self.assertNotEqual(lanes["true"].after_digest, lanes["within_episode_permuted"].after_digest)
        self.assertNotEqual(lanes["true"].after_digest, lanes["zero"].after_digest)
        self.assertTrue(all(not lane.controller.learning for lane in lanes.values()))

    def test_training_is_deterministic_and_frozen_eval_is_state_stable(self) -> None:
        first = train_reward_lanes(Stream(), seed=5, init_seed=9)
        second = train_reward_lanes(Stream(), seed=5, init_seed=9)
        self.assertEqual(
            {mode: lane.after_digest for mode, lane in first.items()},
            {mode: lane.after_digest for mode, lane in second.items()},
        )
        before = {mode: (lane.controller.digest(), lane.controller.updates) for mode, lane in first.items()}
        rows = evaluate_frozen_lanes(first, FrozenAccessor())
        self.assertEqual(set(rows), set(first))
        self.assertEqual(before, {mode: (lane.controller.digest(), lane.controller.updates) for mode, lane in first.items()})

    def test_lane_rejects_noncausal_permutation_and_coincident_digests(self) -> None:
        with patch.object(controller_v6, "episode_feedback", side_effect=lambda rewards, mode, seed: tuple(rewards)):
            with self.assertRaisesRegex(AssertionError, "permutation"):
                train_reward_lanes(Stream(2), seed=7)

        def no_update_replay(learner, trajectory, mode, seed):
            del learner, trajectory, seed
            return (0.25,) if mode == "true" else (0.5,)

        with patch.object(controller_v6, "_replay", side_effect=no_update_replay):
            with self.assertRaisesRegex(AssertionError, "same post-training digest"):
                train_reward_lanes(Stream(2), seed=7)

    def test_g_only_derangement_preserves_u_and_records_source_indices(self) -> None:
        environments = tuple(Episode(seed, GoalState.SPECTRAL).fresh_environment() for seed in (1, 2, 3))
        views = tuple(environment.view for environment in environments)
        packet = derange_controller_views(views, seed=17)
        self.assertEqual(sorted(controller_geometry(view) for view in views), sorted(controller_geometry(view) for view in packet.views))
        self.assertTrue(all(source != index for index, source in enumerate(packet.source_indices)))
        for original, observed in zip(views, packet.views):
            self.assertEqual(
                (original.remaining_budget_fraction, original.last_scalar_reward, original.trusted_goal),
                (observed.remaining_budget_fraction, observed.last_scalar_reward, observed.trusted_goal),
            )
        duplicate = derange_controller_views((views[0], views[0], views[0]), seed=4)
        self.assertEqual(sorted(duplicate.source_indices), [0, 1, 2])
        self.assertTrue(all(source != index for index, source in enumerate(duplicate.source_indices)))

    def test_structural_replay_keeps_physical_rewards_and_actions_identical(self) -> None:
        identity_envs = tuple(Episode(seed, GoalState.SPECTRAL).fresh_environment() for seed in (7, 8, 9))
        scrambled_envs = tuple(Episode(seed, GoalState.SPECTRAL).fresh_environment() for seed in (7, 8, 9))
        identity = synchronous_structural_rollout(identity_envs, channel="I", seed=3)
        scrambled = synchronous_structural_rollout(
            scrambled_envs, channel="S", seed=3, replay_actions=identity.actions
        )
        self.assertIsInstance(identity, BatchRollout)
        self.assertEqual(identity.actions, scrambled.actions)
        self.assertEqual(identity.rewards, scrambled.rewards)
        self.assertTrue(all(source != index for row in scrambled.source_indices for index, source in enumerate(row)))
        self.assertEqual(
            tuple((environment._points, environment._cursor, environment._remaining) for environment in identity_envs),
            tuple((environment._points, environment._cursor, environment._remaining) for environment in scrambled_envs),
        )

    def test_structural_training_arms_and_frozen_eval(self) -> None:
        lanes = train_structural_lanes(Stream(2), seed=3, init_seed=11)
        self.assertEqual(set(lanes), {"I→I", "I→S", "S→I", "S→S"})
        self.assertEqual({lane.update_delta for lane in lanes.values()}, {2 * V6_BUDGET})
        before = {name: (lane.controller.digest(), lane.controller.updates) for name, lane in lanes.items()}
        rows = evaluate_structural_lanes(lanes, FrozenAccessor())
        self.assertEqual(set(rows), set(lanes))
        self.assertEqual(before, {name: (lane.controller.digest(), lane.controller.updates) for name, lane in lanes.items()})

    def test_locked_bootstrap_gates_and_negative_fixtures(self) -> None:
        treatment = _rows(0.80, exact=0.80)
        permuted = _rows(0.70, exact=0.70)
        zero = _rows(0.65, exact=0.65)
        bootstrap = paired_hierarchical_bootstrap(treatment, permuted, resamples=300, seed=1)
        self.assertEqual(bootstrap.groups, 4)
        self.assertGreaterEqual(bootstrap.ci_low, 0.09)
        feedback = feedback_gate(treatment, permuted, zero, resamples=300)
        recovery = recovery_gate(
            treatment,
            {"random": _rows(0.60), "local": _rows(0.65), "visible": _rows(0.62)},
            resamples=300,
        )
        transfer = transfer_gate(
            treatment,
            {"baseline": _rows(0.65)},
            test_updates={"true": 0},
            train_digests={"true": "digest"},
            test_digests={"true": "digest"},
            resamples=300,
        )
        structural = structural_gate(treatment, permuted, zero, resamples=300)
        self.assertTrue(feedback["valid"] and feedback["positive"])
        self.assertTrue(recovery["valid"] and recovery["positive"])
        self.assertTrue(transfer["valid"] and transfer["positive"])
        self.assertTrue(structural["valid"] and structural["positive"])
        self.assertTrue(core_conjunction(feedback, recovery, transfer))
        self.assertFalse(feedback_gate(treatment, _rows(0.78), _rows(0.77), resamples=300)["positive"])
        self.assertFalse(structural_gate(treatment, _rows(0.79), _rows(0.78), resamples=300)["positive"])
        self.assertFalse(
            transfer_gate(
                treatment,
                {"baseline": _rows(0.65)},
                test_updates={"true": 1},
                train_digests={"true": "digest"},
                test_digests={"true": "digest"},
                resamples=300,
            )["positive"]
        )


if __name__ == "__main__":
    unittest.main()
