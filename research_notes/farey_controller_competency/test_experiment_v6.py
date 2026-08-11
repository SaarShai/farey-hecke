from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from .controller_v6 import V6Local
from .experiment_v6 import (
    CLAIM_SCOPE,
    PublicEpisode,
    PublicStream,
    _assert_unopened,
    _commit_opening,
    _environment,
    _evaluate_one,
    _rows_for_policy,
    aggregate_rows,
    result_markdown,
    run_final,
)
from .repair_experiment import RepairTask
from .strict_environment import DamagePattern, GoalState


class ExperimentV6Tests(unittest.TestCase):
    def task(self, seed: int = 1) -> RepairTask:
        return RepairTask(10, DamagePattern.RANDOM_ISOLATED, GoalState.COVERAGE, seed, 2)

    def test_public_episode_returns_fresh_sixteen_step_environment(self) -> None:
        episode = PublicEpisode(self.task())
        first, second = episode.fresh_environment(), episode.fresh_environment()
        self.assertIsNot(first, second)
        self.assertEqual(first._remaining, 16)
        self.assertEqual(first._points, second._points)
        self.assertEqual(len(tuple(PublicStream((self.task(),)))), 1)

    def test_task_rows_and_aggregation_keep_learner_cell_pairs_unique(self) -> None:
        task = self.task()
        rows = _rows_for_policy(V6Local(), (task,), learner_seed=3, policy_name="local")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["action_count"], 16)
        aggregate = aggregate_rows(rows)
        self.assertEqual(len(aggregate), 1)
        self.assertEqual(aggregate[0]["seed"], 3)
        self.assertEqual(aggregate[0]["task_count"], 1)

    def test_guard_refuses_before_constructing_real_manifest(self) -> None:
        with TemporaryDirectory() as directory:
            receipt = Path(directory) / "receipt.json"
            results = Path(directory) / "results.md"
            marker = Path(directory) / "opened.json"
            receipt.write_text("already opened", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "already been opened"):
                _assert_unopened(receipt, results, marker)

    def test_visible_reward_sum_is_the_full_telescoping_episode(self) -> None:
        task = self.task()
        policy = V6Local()
        metrics, actions = _evaluate_one(policy, task)
        environment = _environment(task)
        feedback = 0.0
        expected = 0.0
        for action in actions:
            feedback = environment.step(action)
            expected += feedback
        self.assertAlmostEqual(metrics["visible_reward_sum"], expected)

    def test_opening_marker_is_exclusive_and_durable(self) -> None:
        with TemporaryDirectory() as directory:
            marker = Path(directory) / "opened.json"
            _commit_opening(marker, model_digest="sha256:" + "a" * 64, manifest_private_hash="b" * 64)
            self.assertIn("controller_test_opening_committed", marker.read_text(encoding="utf-8"))
            with self.assertRaises(FileExistsError):
                _commit_opening(marker, model_digest="sha256:" + "a" * 64, manifest_private_hash="b" * 64)

    def test_result_markdown_keeps_offline_claim_boundary(self) -> None:
        result = {
            "protocol": {"claim_scope": CLAIM_SCOPE},
            "access": {"test_openings": 1, "test_updates": 0},
            "gates": {
                name: {"valid": True, "positive": False}
                for name in ("feedback", "recovery", "transfer", "structural")
            } | {"core_conjunction": False, "full_structural_conjunction": False},
            "test_summary": {"true": {"precision": 0.0, "recall": 0.0, "f1": 0.0, "exact": 0.0}},
            "claim_boundary": "offline only",
        }
        markdown = result_markdown(result)
        self.assertIn(CLAIM_SCOPE, markdown)
        self.assertIn("offline only", markdown)


if __name__ == "__main__":
    unittest.main()
