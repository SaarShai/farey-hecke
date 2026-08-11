"""Contract tests for the leak-tight strict Farey environment."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from fractions import Fraction
import unittest

try:  # Package-style test invocation from the repository root.
    from .strict_environment import (
        ACTIONS,
        Action,
        DamageMask,
        DamagePattern,
        GoalState,
        StrictEnvironment,
        StrictObservation,
        UntrustedCue,
        generate_damage_mask,
        rotate_damage_mask,
    )
except ImportError:  # Direct invocation from this directory.
    from strict_environment import (  # type: ignore[no-redef]
        ACTIONS,
        Action,
        DamageMask,
        DamagePattern,
        GoalState,
        StrictEnvironment,
        StrictObservation,
        UntrustedCue,
        generate_damage_mask,
        rotate_damage_mask,
    )


def _assert_no_leak(test: unittest.TestCase, value: object, *, tuple_limit: int = 4) -> None:
    """Reject exact rationals, mutable arrays, and variable global payloads."""

    test.assertNotIsInstance(value, Fraction)
    test.assertNotIsInstance(value, list)
    if isinstance(value, tuple):
        test.assertLessEqual(len(value), tuple_limit)
        for item in value:
            _assert_no_leak(test, item, tuple_limit=tuple_limit)
    elif is_dataclass(value):
        for field in fields(value):
            _assert_no_leak(test, getattr(value, field.name), tuple_limit=tuple_limit)


class StrictEnvironmentContractTests(unittest.TestCase):
    def test_observation_is_fixed_width_quantized_and_has_no_evaluator_payload(self) -> None:
        observations = [
            StrictEnvironment(3, damage_count=1, seed=3).observation,
            StrictEnvironment(11, damage_count=3, seed=3).observation,
            StrictEnvironment(
                17,
                DamagePattern.BURST,
                damage_count=5,
                seed=3,
                action_budget=13,
                goal=GoalState.SPECTRAL,
                untrusted_cue=("hint", 7),
            ).observation,
        ]
        self.assertTrue(all(isinstance(observation, StrictObservation) for observation in observations))
        self.assertEqual({observation.shape for observation in observations}, {(4, 2, 1, 1, 1, 1, 2)})
        self.assertEqual({len(observation.as_tuple()) for observation in observations}, {12})
        for observation in observations:
            self.assertEqual(len(observation.neighbor_gap_bins), 4)
            self.assertEqual(len(observation.neighbor_gap_ratio_bins), 2)
            self.assertIsInstance(observation.remaining_budget_fraction, float)
            self.assertIsInstance(observation.last_scalar_reward, float)
            _assert_no_leak(self, observation)

        names = {field.name for field in fields(StrictObservation)}
        forbidden = {
            "fraction",
            "fractions",
            "order",
            "n",
            "survivors",
            "actions",
            "menu",
            "missing",
            "damage_count",
            "target",
            "identity",
            "evaluator",
        }
        self.assertTrue(names.isdisjoint(forbidden))

    def test_goal_and_untrusted_cue_are_distinct_tagged_fields(self) -> None:
        observation = StrictEnvironment(
            7,
            goal=GoalState.SPECTRAL,
            untrusted_cue=("untrusted_hint", -4),
        ).observation
        self.assertEqual(observation.trusted_goal_state, GoalState.SPECTRAL)
        self.assertEqual(observation.untrusted_cue, UntrustedCue("untrusted_hint", -4))
        self.assertNotEqual(observation.trusted_goal_state.value, observation.untrusted_cue.tag)

        environment = StrictEnvironment(7, goal=GoalState.COVERAGE)
        changed = environment.set_cue_channels(
            trusted_goal=GoalState.SPECTRAL,
            untrusted_cue=("conflicting_goal", 0),
        )
        self.assertEqual(changed.trusted_goal_state, GoalState.SPECTRAL)
        self.assertEqual(changed.untrusted_cue, UntrustedCue("conflicting_goal", 0))
        with self.assertRaises(ValueError):
            UntrustedCue("hidden-order-17", 0)

    def test_action_set_is_exactly_fixed(self) -> None:
        self.assertEqual(
            ACTIONS,
            ("move_left", "move_right", "insert_mediant", "insert_midpoint", "stop"),
        )
        self.assertEqual({action.value for action in Action}, set(ACTIONS))
        self.assertEqual(StrictEnvironment(5).available_actions, ACTIONS)
        self.assertEqual(StrictEnvironment(5).action_space, ACTIONS)

    def test_every_action_is_committed_and_charged(self) -> None:
        for action in ACTIONS:
            environment = StrictEnvironment(5, damage_count=1, action_budget=1)
            transition = environment.step(action)
            self.assertTrue(transition.committed)
            self.assertTrue(transition.charged)
            self.assertTrue(transition.done)
            self.assertEqual(transition.observation.remaining_budget_fraction, 0.0)
        finished = StrictEnvironment(5, action_budget=1)
        finished.step(Action.STOP)
        with self.assertRaises(RuntimeError):
            finished.step(Action.MOVE_LEFT)

    def test_budget_is_independent_of_damage_count(self) -> None:
        one = StrictEnvironment(13, damage_count=1, action_budget=9, seed=1)
        many = StrictEnvironment(13, damage_count=7, action_budget=9, seed=1)
        self.assertEqual(one.observation.remaining_budget_fraction, 1.0)
        self.assertEqual(many.observation.remaining_budget_fraction, 1.0)
        one.step(Action.MOVE_RIGHT)
        many.step(Action.MOVE_RIGHT)
        self.assertEqual(one.observation.remaining_budget_fraction, many.observation.remaining_budget_fraction)

    def test_metrics_are_evaluator_only_and_identity_recovery_is_exact(self) -> None:
        environment = StrictEnvironment(
            5,
            damage_mask=DamageMask((1,), DamagePattern.BURST),
            action_budget=3,
        )
        before = environment.evaluator_metrics
        self.assertEqual(before.identity_recovery, 0.0)
        self.assertIsInstance(before.coverage, float)
        self.assertIsInstance(before.spectral, float)
        self.assertNotIn("identity_recovery", {field.name for field in fields(environment.observation)})
        transition = environment.step(Action.INSERT_MEDIANT)
        self.assertTrue(transition.changed)
        self.assertEqual(environment.evaluator_metrics.identity_recovery, 1.0)

    def test_damage_families_and_rotation_are_seeded(self) -> None:
        for pattern in DamagePattern:
            first = generate_damage_mask(19, pattern, 4, seed=41)
            second = generate_damage_mask(19, pattern, 4, seed=41)
            self.assertEqual(first, second)
            self.assertEqual(len(first.indices), 4)
            self.assertEqual(len(set(first.indices)), 4)

        unrotated = generate_damage_mask(19, DamagePattern.BURST, 2, seed=41, rotation=0)
        rotated = generate_damage_mask(19, DamagePattern.BURST, 2, seed=41, rotation=3)
        self.assertNotEqual(unrotated.indices, rotated.indices)
        self.assertEqual(rotated.rotation_offset, 3)
        self.assertEqual(len(rotate_damage_mask(unrotated.indices, 64, 3)), 2)

        # A rotated cursor frame must not rotate denominator-biased target
        # indices into unrelated denominators.
        biased_a = StrictEnvironment(
            17, DamagePattern.DENOMINATOR_BIASED, damage_count=2, seed=9, rotation=False
        )
        biased_b = StrictEnvironment(
            17, DamagePattern.DENOMINATOR_BIASED, damage_count=2, seed=9, rotation=True
        )
        self.assertEqual(biased_a._deleted_indices, biased_b._deleted_indices)

    def test_rotation_randomizes_initial_cursor_frame_deterministically(self) -> None:
        first = StrictEnvironment(13, seed=8, rotation=True)
        second = StrictEnvironment(13, seed=8, rotation=True)
        self.assertEqual(first.observation, second.observation)
        baseline = StrictEnvironment(13, seed=8, rotation=0)
        # The rotated frame is deterministic, and either local geometry or the
        # cursor frame changes; no global cursor index is exposed.
        self.assertNotEqual(first.observation, baseline.observation)


if __name__ == "__main__":
    unittest.main()
