from __future__ import annotations

import unittest
import shutil
import tempfile
from pathlib import Path

from human_workflow_analysis import AnalysisError, _manifest_by_digest, analyze_session
from workflow_measurement import CostInputs, WorkflowSession


class HumanWorkflowAnalysisTests(unittest.TestCase):
    def make_session(self) -> tuple[WorkflowSession, dict[str, object], dict[str, int]]:
        session = WorkflowSession(
            session_id="human-001",
            condition="uci-human-production",
            order_digest="order-1",
            cohort_digest="cohort-1",
            item_ids=("test-0000", "test-0001", "test-0002"),
            cost_inputs=CostInputs(reviewer_rate_per_hour=60),
            created_utc="2026-08-01T00:00:00Z",
        )
        session.record("session_start", monotonic_ns=1, utc="2026-08-01T00:00:00Z")
        session.record("item_shown", monotonic_ns=2, utc="2026-08-01T00:00:00Z", item_id="test-0000")
        session.record("response", monotonic_ns=4, utc="2026-08-01T00:00:00Z", item_id="test-0000", payload={"selection": "1"})
        session.record("item_shown", monotonic_ns=5, utc="2026-08-01T00:00:00Z", item_id="test-0001")
        session.record("response", monotonic_ns=8, utc="2026-08-01T00:00:00Z", item_id="test-0001", payload={"selection": "2"})
        session.record("item_shown", monotonic_ns=9, utc="2026-08-01T00:00:00Z", item_id="test-0002")
        session.record("skip", monotonic_ns=12, utc="2026-08-01T00:00:00Z", item_id="test-0002", payload={"reason": "participant_skip"})
        session.record("session_end", monotonic_ns=13, utc="2026-08-01T00:00:00Z")
        manifest = {
            "condition": "uci-human-production",
            "order_digest": "order-1",
            "cohort_digest": "cohort-1",
            "item_ids": list(session.item_ids),
        }
        labels = {"test-0000": 1, "test-0001": 3, "test-0002": 2}
        return session, manifest, labels

    def test_reveal_reports_time_cost_accuracy_and_coverage(self) -> None:
        session, manifest, labels = self.make_session()
        result = analyze_session(session, manifest, labels, warmup=1)
        self.assertEqual(result["responses"], 2)
        self.assertEqual(result["skips"], 1)
        self.assertEqual(result["response_coverage"], 2 / 3)
        self.assertEqual(result["response_accuracy"], 0.5)
        self.assertEqual(result["active_review_seconds"], 0.0)
        self.assertEqual(result["marketing_status"], "NOT_CLEARED_UNTIL_PROSPECTIVE_HUMAN_STUDY")

    def test_manifest_mismatch_fails_closed(self) -> None:
        session, manifest, labels = self.make_session()
        manifest["order_digest"] = "wrong"
        with self.assertRaises(AnalysisError):
            analyze_session(session, manifest, labels)

    def test_no_responses_fails_closed(self) -> None:
        session, manifest, labels = self.make_session()
        labels.clear()
        with self.assertRaises(AnalysisError):
            analyze_session(session, manifest, labels)

    def test_manifest_file_tamper_fails_closed(self) -> None:
        source = Path(__file__).resolve().parents[1] / "pilots" / "uci-human-workflow-2026-08-01"
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "manifests"
            shutil.copytree(source, target)
            path = target / "manifest-production.json"
            path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            with self.assertRaises(AnalysisError):
                _manifest_by_digest(target)


if __name__ == "__main__":
    unittest.main()
