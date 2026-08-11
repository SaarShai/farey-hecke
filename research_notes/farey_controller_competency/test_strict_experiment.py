"""Focused controller-boundary tests for the strict experiment."""

from dataclasses import fields
from fractions import Fraction
import unittest

from .strict_environment import Action, StrictEnvironment
from .strict_experiment import ControllerView, LinearController, controller_view


class StrictExperimentTests(unittest.TestCase):
    def test_controller_view_is_fixed_primitive_and_excludes_generator_facts(self) -> None:
        views = [controller_view(StrictEnvironment(order, seed=4), cue=True) for order in (6, 11, 17)]
        self.assertEqual({len(view.features(0)) for view in views}, {11})
        forbidden = {"order", "n", "fraction", "target", "survivors", "menu", "damage"}
        self.assertTrue({field.name for field in fields(ControllerView)}.isdisjoint(forbidden))
        for view in views:
            for value in view.features(0):
                self.assertNotIsInstance(value, Fraction)

    def test_controller_receives_fixed_actions_and_feedback_updates_weights(self) -> None:
        environment = StrictEnvironment(8, seed=76, action_budget=2)
        view = controller_view(environment, cue=True)
        controller = LinearController(1)
        before = controller.digest()
        controller.update(view, Action.INSERT_MEDIANT, 0.1)
        self.assertNotEqual(before, controller.digest())
        controller.learning = False
        frozen = controller.digest()
        controller.update(view, Action.INSERT_MIDPOINT, 1.0)
        self.assertEqual(frozen, controller.digest())

    def test_controller_view_rejects_variable_width_or_unbounded_channels(self) -> None:
        with self.assertRaises(ValueError):
            ControllerView((0, 0, 0), 1.0, 0.0, 0, -1, 0)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            ControllerView((0, 0, 0, 0), 1.0, 0.0, 7, -1, 0)


if __name__ == "__main__":
    unittest.main()
