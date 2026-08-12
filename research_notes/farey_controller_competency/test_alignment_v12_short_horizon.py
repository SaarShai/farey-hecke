"""Tests for the public-table V12 short-horizon alignment audit."""

from __future__ import annotations

import inspect
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from . import alignment_v12_short_horizon as alignment
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class AlignmentV12ShortHorizonTests(unittest.TestCase):
    @staticmethod
    def task(seed: int, goal: GoalState) -> RepairTask:
        return RepairTask(6, DamagePattern.RANDOM_ISOLATED, goal, seed, 2)

    def train(self) -> tuple[RepairTask, ...]:
        return (self.task(1, GoalState.COVERAGE), self.task(2, GoalState.SPECTRAL))

    def test_train_records_are_canonical_quantized_public_tuples(self) -> None:
        transitions = alignment.collect_train_transitions(self.train())
        self.assertEqual(len(transitions), 32)
        self.assertEqual(len(transitions[0].state), 23)
        self.assertTrue(all(-8 <= item.visible_reward_bin <= 8 for item in transitions))
        support = alignment.support_by_action_and_cell(transitions)
        self.assertEqual(support["sample_count"], 32)
        self.assertEqual(len(support["action_counts_by_cell"]), 2)

    def test_selectors_are_source_guarded_from_exact_or_hidden_channels(self) -> None:
        self.assertTrue(alignment._selector_source_guard())
        for selector in (alignment.public_argmax_action, alignment.public_planner_actions, alignment.visible_state_only_action, alignment.zero_reward_action, alignment.random_action):
            source = inspect.getsource(selector)
            for forbidden in ("_points", "_cursor", "deepcopy", "evaluator_metrics"):
                self.assertNotIn(forbidden, source)

    def test_train_table_planning_is_deterministic_and_horizon_limited(self) -> None:
        table = alignment.fit_public_transition_table(alignment.collect_train_transitions(self.train()))
        state = alignment.collect_train_transitions(self.train())[0].state
        self.assertEqual(alignment.public_planner_actions(table, state, 4), alignment.public_planner_actions(table, state, 4))
        self.assertEqual(len(alignment.public_argmax_action(table, state).__str__()) > 0, True)
        with self.assertRaisesRegex(ValueError, "horizon"):
            alignment.public_planner_actions(table, state, 5)

    def test_negative_fixture_detects_public_hidden_disagreement(self) -> None:
        fixture = alignment.negative_fixtures()
        self.assertTrue(fixture["passed"])
        self.assertTrue(fixture["discordant"]["discordant"])
        self.assertTrue(fixture["aligned"]["aligned"])

    def test_compact_run_freezes_train_table_before_validation(self) -> None:
        with TemporaryDirectory() as directory:
            result = alignment.run_alignment(train_tasks=self.train(), validation_tasks=self.train(), output_dir=Path(directory), bootstrap_resamples=20)
            receipt = Path(directory) / alignment.RECEIPT_NAME
            written = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(result["counts"]["validation_updates"], 0)
            self.assertEqual(result["counts"]["validation_policy_rows"], 32)
            self.assertEqual({row["horizon"] for row in result["validation_policy_rows"]}, {1, 2, 3, 4})
            self.assertEqual(result["train_table"]["digest"], result["train_table"]["digest_after_validation"])
            self.assertEqual(written["counts"], result["counts"])
            self.assertTrue(written["selector_guard"])
            self.assertTrue(written["negative_fixtures"]["passed"])
            self.assertIn(written["alignment_status"]["status"], {"negative", "unverified_underpowered"})
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                alignment.run_alignment(train_tasks=self.train(), validation_tasks=self.train(), output_dir=Path(directory))

    def test_paired_bootstrap_rejects_unpaired_rows(self) -> None:
        treatment = [{"split": "validation", "task_index": 0, "horizon": 1, "hidden_f1": 1.0}]
        baseline = [{"split": "validation", "task_index": 1, "horizon": 1, "hidden_f1": 0.0}]
        with self.assertRaisesRegex(ValueError, "identical"):
            alignment.paired_bootstrap(treatment, baseline, metric="hidden_f1", resamples=10, seed=0)


if __name__ == "__main__":
    unittest.main()
