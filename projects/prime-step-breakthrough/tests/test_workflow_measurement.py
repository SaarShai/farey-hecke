from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from workflow_measurement import CostInputs, WorkflowSession


class WorkflowMeasurementTests(unittest.TestCase):
    def make_session(self) -> WorkflowSession:
        return WorkflowSession(
            session_id="pilot-001",
            condition="quota-balanced",
            order_digest="order-digest",
            cohort_digest="cohort-digest",
            item_ids=("a", "b"),
            cost_inputs=CostInputs(
                reviewer_rate_per_hour=60.0,
                operator_rate_per_hour=30.0,
                compute_usd=1.25,
                rework_usd=2.0,
            ),
            created_utc="2026-08-01T00:00:00Z",
        )

    def test_hash_chain_and_cost_include_active_pause_adjudication_and_overhead(self) -> None:
        session = self.make_session()
        session.record("session_start", monotonic_ns=100, utc="2026-08-01T00:00:00Z")
        session.record("import_start", monotonic_ns=1_000_000, utc="2026-08-01T00:00:00Z")
        session.record("import_end", monotonic_ns=1_100_000, utc="2026-08-01T00:00:00Z")
        session.record("item_shown", monotonic_ns=2_000_000, utc="2026-08-01T00:00:00Z", item_id="a")
        session.record("pause", monotonic_ns=2_500_000, utc="2026-08-01T00:00:00Z", item_id="a")
        session.record("resume", monotonic_ns=3_000_000, utc="2026-08-01T00:00:00Z", item_id="a")
        session.record("response", monotonic_ns=4_000_000, utc="2026-08-01T00:00:00Z", item_id="a")
        session.record("adjudication_start", monotonic_ns=5_000_000, utc="2026-08-01T00:00:00Z", item_id="a")
        session.record("adjudication_end", monotonic_ns=5_200_000, utc="2026-08-01T00:00:00Z", item_id="a")
        session.record("stop_evaluation", monotonic_ns=6_000_000, utc="2026-08-01T00:00:00Z", payload={"prefix_size": 1, "decision": "continue"})
        session.record("session_end", monotonic_ns=7_000_000, utc="2026-08-01T00:00:00Z")
        summary = session.summary()
        self.assertEqual(summary["active_review_seconds"], 0.0015)
        self.assertEqual(summary["adjudication_seconds"], 0.0002)
        self.assertEqual(summary["operator_overhead_seconds"], 0.0001)
        self.assertEqual(summary["responses"], 1)
        self.assertEqual(summary["stop_evaluations"], 1)
        self.assertAlmostEqual(summary["cost"]["total_usd"], 3.250029, places=5)
        self.assertEqual(len(summary["event_chain_sha256"]), 64)

    def test_state_and_stop_gate_reject_invalid_or_outcome_looking_events(self) -> None:
        session = self.make_session()
        with self.assertRaises(ValueError):
            session.record("item_shown", monotonic_ns=1, item_id="a")
        session.record("session_start", monotonic_ns=1)
        with self.assertRaises(ValueError):
            session.record("stop_evaluation", monotonic_ns=2, payload={"prefix_size": 0, "outcome": 1})
        session.record("item_shown", monotonic_ns=3, item_id="a")
        with self.assertRaises(ValueError):
            session.record("response", monotonic_ns=3, item_id="a")
        session.record("response", monotonic_ns=4, item_id="a")
        with self.assertRaises(ValueError):
            session.record("response", monotonic_ns=5, item_id="a")

    def test_jsonl_round_trip_and_tamper_detection(self) -> None:
        session = self.make_session()
        session.record("session_start", monotonic_ns=1, utc="2026-08-01T00:00:00Z")
        session.record("item_shown", monotonic_ns=2, utc="2026-08-01T00:00:00Z", item_id="a")
        session.record("response", monotonic_ns=3, utc="2026-08-01T00:00:00Z", item_id="a")
        session.record("session_end", monotonic_ns=4, utc="2026-08-01T00:00:00Z")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            session.write_jsonl(path)
            rebuilt = WorkflowSession.read_jsonl(path)
            self.assertEqual(rebuilt.summary(), session.summary())
            records = [json.loads(line) for line in path.read_text().splitlines()]
            records[2]["event"]["payload"]["tampered"] = True
            path.write_text("\n".join(json.dumps(record, sort_keys=True) for record in records) + "\n")
            with self.assertRaises(ValueError):
                WorkflowSession.read_jsonl(path)

    def test_negative_cost_inputs_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            CostInputs(reviewer_rate_per_hour=-1)
        with self.assertRaises(ValueError):
            CostInputs(reviewer_rate_per_hour=1, compute_usd=float("nan"))


if __name__ == "__main__":
    unittest.main()
