#!/usr/bin/env python3
"""Hash-chained human-workflow measurement for prospective ordering pilots.

The module records only workflow events and prefix-observable stop decisions.
It does not construct an audit order and it does not infer customer savings.
The resulting JSONL file is an evidence record: timestamps, event ordering,
and a tamper-evident chain can be independently recomputed after a study.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping


SCHEMA_VERSION = "workflow-measurement-v1"
EVENT_TYPES = frozenset(
    {
        "session_start",
        "session_end",
        "item_shown",
        "response",
        "correction",
        "skip",
        "pause",
        "resume",
        "adjudication_start",
        "adjudication_end",
        "stop_evaluation",
        "import_start",
        "import_end",
        "mapping_start",
        "mapping_end",
        "export_start",
        "export_end",
    }
)
OPERATION_SPANS = {
    "import_start": "import",
    "mapping_start": "mapping",
    "export_start": "export",
}
OPERATION_ENDS = {
    "import_end": "import",
    "mapping_end": "mapping",
    "export_end": "export",
}
STOP_FORBIDDEN_KEYS = frozenset(
    {"correct", "error", "ground_truth", "label", "loss", "outcome", "truth"}
)


def _canonical(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _sha256(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _nonnegative_finite(value: float, name: str) -> float:
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError(f"{name} must be a finite nonnegative number")
    return result


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


@dataclass(frozen=True)
class CostInputs:
    """Loaded rates and non-labor costs supplied by the study owner."""

    reviewer_rate_per_hour: float
    operator_rate_per_hour: float = 0.0
    compute_usd: float = 0.0
    rework_usd: float = 0.0
    integration_usd: float = 0.0
    license_usd: float = 0.0

    def __post_init__(self) -> None:
        for name in (
            "reviewer_rate_per_hour",
            "operator_rate_per_hour",
            "compute_usd",
            "rework_usd",
            "integration_usd",
            "license_usd",
        ):
            _nonnegative_finite(getattr(self, name), name)

    def to_dict(self) -> dict[str, float]:
        return {
            "reviewer_rate_per_hour": self.reviewer_rate_per_hour,
            "operator_rate_per_hour": self.operator_rate_per_hour,
            "compute_usd": self.compute_usd,
            "rework_usd": self.rework_usd,
            "integration_usd": self.integration_usd,
            "license_usd": self.license_usd,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, object]) -> "CostInputs":
        return cls(
            reviewer_rate_per_hour=float(value["reviewer_rate_per_hour"]),
            operator_rate_per_hour=float(value.get("operator_rate_per_hour", 0.0)),
            compute_usd=float(value.get("compute_usd", 0.0)),
            rework_usd=float(value.get("rework_usd", 0.0)),
            integration_usd=float(value.get("integration_usd", 0.0)),
            license_usd=float(value.get("license_usd", 0.0)),
        )


@dataclass(frozen=True)
class CostEstimate:
    reviewer_labor_usd: float
    operator_labor_usd: float
    compute_usd: float
    rework_usd: float
    integration_usd: float
    license_usd: float
    total_usd: float

    def to_dict(self) -> dict[str, float]:
        return {
            "reviewer_labor_usd": round(self.reviewer_labor_usd, 6),
            "operator_labor_usd": round(self.operator_labor_usd, 6),
            "compute_usd": round(self.compute_usd, 6),
            "rework_usd": round(self.rework_usd, 6),
            "integration_usd": round(self.integration_usd, 6),
            "license_usd": round(self.license_usd, 6),
            "total_usd": round(self.total_usd, 6),
        }


@dataclass(frozen=True)
class WorkflowEvent:
    sequence: int
    event_type: str
    monotonic_ns: int
    utc: str
    item_id: str | None
    payload: dict[str, object]
    previous_hash: str
    event_hash: str

    def to_dict(self) -> dict[str, object]:
        return {
            "sequence": self.sequence,
            "event_type": self.event_type,
            "monotonic_ns": self.monotonic_ns,
            "utc": self.utc,
            "item_id": self.item_id,
            "payload": self.payload,
            "previous_hash": self.previous_hash,
            "event_hash": self.event_hash,
        }


class WorkflowSession:
    """Fail-closed event recorder for one prospective workflow session."""

    def __init__(
        self,
        *,
        session_id: str,
        condition: str,
        order_digest: str,
        item_ids: tuple[str, ...],
        cost_inputs: CostInputs,
        cohort_digest: str | None = None,
        created_utc: str | None = None,
    ) -> None:
        if not session_id.strip():
            raise ValueError("session_id cannot be blank")
        if not condition.strip():
            raise ValueError("condition cannot be blank")
        if not order_digest.strip():
            raise ValueError("order_digest cannot be blank")
        if not item_ids:
            raise ValueError("item_ids cannot be empty")
        if len(set(item_ids)) != len(item_ids):
            raise ValueError("item_ids must be unique")
        if any(not item_id.strip() for item_id in item_ids):
            raise ValueError("item_ids cannot contain blanks")
        self.session_id = session_id
        self.condition = condition
        self.order_digest = order_digest
        self.item_ids = tuple(item_ids)
        self.cost_inputs = cost_inputs
        self.cohort_digest = cohort_digest
        self.created_utc = created_utc or _utc_now()
        self.manifest = {
            "schema_version": SCHEMA_VERSION,
            "session_id": self.session_id,
            "condition": self.condition,
            "order_digest": self.order_digest,
            "cohort_digest": self.cohort_digest,
            "item_ids": list(self.item_ids),
            "item_count": len(self.item_ids),
            "cost_inputs": self.cost_inputs.to_dict(),
            "created_utc": self.created_utc,
        }
        self.manifest_sha256 = _sha256(self.manifest)
        self._events: list[WorkflowEvent] = []
        self._previous_hash = self.manifest_sha256
        self._last_monotonic_ns = -1
        self._started = False
        self._ended = False
        self._shown_items: set[str] = set()
        self._current_item: str | None = None
        self._item_start_ns: int | None = None
        self._item_pause_start_ns: int | None = None
        self._item_paused_ns = 0
        self._session_pause_start_ns: int | None = None
        self._session_paused_ns = 0
        self._adjudication_start_ns: int | None = None
        self._adjudication_item: str | None = None
        self._operation_starts: dict[str, int] = {}
        self._active_review_ns = 0
        self._adjudication_ns = 0
        self._operator_overhead_ns = 0
        self._counts = {"responses": 0, "corrections": 0, "skips": 0, "stop_evaluations": 0}

    @property
    def events(self) -> tuple[WorkflowEvent, ...]:
        return tuple(self._events)

    def _require_item(self, item_id: str | None) -> str:
        if item_id is None:
            raise ValueError("item_id is required for this event")
        if item_id not in self.item_ids:
            raise ValueError(f"unknown item_id {item_id!r}")
        return item_id

    def _close_item(self, monotonic_ns: int, item_id: str | None) -> None:
        current = self._require_item(item_id)
        if current != self._current_item:
            raise ValueError("event item_id does not match the currently shown item")
        if self._item_pause_start_ns is not None:
            raise ValueError("resume before closing a paused item")
        assert self._item_start_ns is not None
        elapsed = monotonic_ns - self._item_start_ns - self._item_paused_ns
        if elapsed < 0:
            raise ValueError("item elapsed time cannot be negative")
        self._active_review_ns += elapsed
        self._current_item = None
        self._item_start_ns = None
        self._item_paused_ns = 0

    def _apply_state(self, event_type: str, monotonic_ns: int, item_id: str | None, payload: dict[str, object]) -> None:
        if event_type == "session_start":
            if self._started or self._events:
                raise ValueError("session_start must be the first event")
            self._started = True
            return
        if not self._started:
            raise ValueError("record session_start before other events")
        if self._ended:
            raise ValueError("session already ended")
        if event_type == "session_end":
            if any(
                (
                    self._current_item,
                    self._item_pause_start_ns,
                    self._session_pause_start_ns,
                    self._adjudication_start_ns,
                    self._operation_starts,
                )
            ):
                raise ValueError("close every active item, pause, adjudication, and operation before session_end")
            self._ended = True
        elif event_type == "item_shown":
            current = self._require_item(item_id)
            if self._current_item is not None:
                raise ValueError("an item is already active")
            if self._session_pause_start_ns is not None:
                raise ValueError("resume the session before showing an item")
            if current in self._shown_items:
                raise ValueError("an item may be shown only once per session")
            self._shown_items.add(current)
            self._current_item = current
            self._item_start_ns = monotonic_ns
            self._item_pause_start_ns = None
            self._item_paused_ns = 0
        elif event_type in {"response", "skip"}:
            self._close_item(monotonic_ns, item_id)
            self._counts["responses" if event_type == "response" else "skips"] += 1
        elif event_type == "correction":
            current = self._require_item(item_id)
            if current not in self._shown_items:
                raise ValueError("correction item must have been shown")
            duration = _nonnegative_finite(float(payload.get("duration_seconds", -1)), "correction duration_seconds")
            self._active_review_ns += int(round(duration * 1_000_000_000))
            self._counts["corrections"] += 1
        elif event_type == "pause":
            if self._session_pause_start_ns is not None or self._item_pause_start_ns is not None:
                raise ValueError("workflow is already paused")
            if self._current_item is not None:
                if item_id != self._current_item:
                    raise ValueError("pause item_id must match the active item")
                self._item_pause_start_ns = monotonic_ns
            else:
                if item_id is not None:
                    raise ValueError("session-level pause cannot carry item_id")
                self._session_pause_start_ns = monotonic_ns
        elif event_type == "resume":
            if self._item_pause_start_ns is not None:
                self._item_paused_ns += monotonic_ns - self._item_pause_start_ns
                self._item_pause_start_ns = None
            elif self._session_pause_start_ns is not None:
                self._session_paused_ns += monotonic_ns - self._session_pause_start_ns
                self._session_pause_start_ns = None
            else:
                raise ValueError("resume requires an active pause")
        elif event_type == "adjudication_start":
            if self._adjudication_start_ns is not None:
                raise ValueError("an adjudication is already active")
            if item_id is not None:
                self._require_item(item_id)
            self._adjudication_start_ns = monotonic_ns
            self._adjudication_item = item_id
        elif event_type == "adjudication_end":
            if self._adjudication_start_ns is None:
                raise ValueError("adjudication_end requires adjudication_start")
            if item_id != self._adjudication_item:
                raise ValueError("adjudication item_id does not match its start")
            self._adjudication_ns += monotonic_ns - self._adjudication_start_ns
            self._adjudication_start_ns = None
            self._adjudication_item = None
        elif event_type == "stop_evaluation":
            forbidden = STOP_FORBIDDEN_KEYS.intersection(payload)
            if forbidden:
                raise ValueError(f"stop_evaluation cannot contain outcome keys: {sorted(forbidden)}")
            prefix_size = payload.get("prefix_size")
            if isinstance(prefix_size, bool) or not isinstance(prefix_size, int):
                raise ValueError("stop_evaluation prefix_size must be an integer")
            if not 0 <= prefix_size <= len(self.item_ids):
                raise ValueError("stop_evaluation prefix_size is outside the cohort")
            self._counts["stop_evaluations"] += 1
        elif event_type in OPERATION_SPANS:
            operation = OPERATION_SPANS[event_type]
            if operation in self._operation_starts:
                raise ValueError(f"{operation} operation is already active")
            self._operation_starts[operation] = monotonic_ns
        elif event_type in OPERATION_ENDS:
            operation = OPERATION_ENDS[event_type]
            start = self._operation_starts.pop(operation, None)
            if start is None:
                raise ValueError(f"{operation}_end requires its start event")
            self._operator_overhead_ns += monotonic_ns - start

    def record(
        self,
        event_type: str,
        *,
        monotonic_ns: int | None = None,
        utc: str | None = None,
        item_id: str | None = None,
        payload: Mapping[str, object] | None = None,
    ) -> WorkflowEvent:
        if event_type not in EVENT_TYPES:
            raise ValueError(f"unknown event_type {event_type!r}")
        timestamp = time.monotonic_ns() if monotonic_ns is None else int(monotonic_ns)
        if timestamp <= self._last_monotonic_ns:
            raise ValueError("monotonic_ns must strictly increase")
        event_payload = dict(payload or {})
        _canonical(event_payload)
        self._apply_state(event_type, timestamp, item_id, event_payload)
        body = {
            "sequence": len(self._events),
            "event_type": event_type,
            "monotonic_ns": timestamp,
            "utc": utc or _utc_now(),
            "item_id": item_id,
            "payload": event_payload,
            "previous_hash": self._previous_hash,
        }
        event_hash = _sha256(body)
        event = WorkflowEvent(
            sequence=body["sequence"],
            event_type=event_type,
            monotonic_ns=timestamp,
            utc=body["utc"],
            item_id=item_id,
            payload=event_payload,
            previous_hash=self._previous_hash,
            event_hash=event_hash,
        )
        self._events.append(event)
        self._previous_hash = event_hash
        self._last_monotonic_ns = timestamp
        return event

    def summary(self) -> dict[str, object]:
        active_seconds = self._active_review_ns / 1_000_000_000
        adjudication_seconds = self._adjudication_ns / 1_000_000_000
        operator_seconds = self._operator_overhead_ns / 1_000_000_000
        reviewer_cost = (active_seconds + adjudication_seconds) * self.cost_inputs.reviewer_rate_per_hour / 3600
        operator_cost = operator_seconds * self.cost_inputs.operator_rate_per_hour / 3600
        total = (
            reviewer_cost
            + operator_cost
            + self.cost_inputs.compute_usd
            + self.cost_inputs.rework_usd
            + self.cost_inputs.integration_usd
            + self.cost_inputs.license_usd
        )
        estimate = CostEstimate(
            reviewer_labor_usd=reviewer_cost,
            operator_labor_usd=operator_cost,
            compute_usd=self.cost_inputs.compute_usd,
            rework_usd=self.cost_inputs.rework_usd,
            integration_usd=self.cost_inputs.integration_usd,
            license_usd=self.cost_inputs.license_usd,
            total_usd=total,
        )
        return {
            "schema_version": SCHEMA_VERSION,
            "session_id": self.session_id,
            "condition": self.condition,
            "manifest_sha256": self.manifest_sha256,
            "event_chain_sha256": self._previous_hash,
            "event_count": len(self._events),
            "item_count": len(self.item_ids),
            "shown_items": len(self._shown_items),
            "responses": self._counts["responses"],
            "corrections": self._counts["corrections"],
            "skips": self._counts["skips"],
            "stop_evaluations": self._counts["stop_evaluations"],
            "active_review_seconds": round(active_seconds, 6),
            "adjudication_seconds": round(adjudication_seconds, 6),
            "operator_overhead_seconds": round(operator_seconds, 6),
            "paused_seconds": round(self._session_paused_ns / 1_000_000_000, 6),
            "cost": estimate.to_dict(),
            "marketing_status": "NOT_CLEARED_UNTIL_PROSPECTIVE_HUMAN_STUDY",
        }

    def write_jsonl(self, path: Path, *, include_summary: bool = True) -> None:
        """Write an immutable evidence file; refuse to overwrite an existing file."""

        records = [{"record_type": "manifest", "manifest": self.manifest, "manifest_sha256": self.manifest_sha256}]
        records.extend({"record_type": "event", "event": event.to_dict()} for event in self._events)
        if include_summary:
            records.append({"record_type": "summary", "summary": self.summary()})
        with path.open("x", encoding="utf-8") as stream:
            for record in records:
                stream.write(_canonical(record) + "\n")

    @classmethod
    def read_jsonl(cls, path: Path) -> "WorkflowSession":
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not records or records[0].get("record_type") != "manifest":
            raise ValueError("workflow file must start with a manifest record")
        manifest_record = records[0]
        manifest = manifest_record["manifest"]
        if manifest_record["manifest_sha256"] != _sha256(manifest):
            raise ValueError("manifest hash mismatch")
        session = cls(
            session_id=manifest["session_id"],
            condition=manifest["condition"],
            order_digest=manifest["order_digest"],
            item_ids=tuple(manifest["item_ids"]),
            cost_inputs=CostInputs.from_dict(manifest["cost_inputs"]),
            cohort_digest=manifest.get("cohort_digest"),
            created_utc=manifest["created_utc"],
        )
        for record in records[1:]:
            if record.get("record_type") == "event":
                event = record["event"]
                rebuilt = session.record(
                    event["event_type"],
                    monotonic_ns=event["monotonic_ns"],
                    utc=event["utc"],
                    item_id=event.get("item_id"),
                    payload=event.get("payload", {}),
                )
                if rebuilt.to_dict() != event:
                    raise ValueError(f"event hash or body mismatch at sequence {event.get('sequence')}")
            elif record.get("record_type") == "summary":
                if record["summary"] != session.summary():
                    raise ValueError("summary does not match the event stream")
            else:
                raise ValueError("unknown workflow record type")
        return session


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="immutable workflow JSONL evidence file")
    parser.add_argument("--json", action="store_true", help="emit the recomputed summary as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    session = WorkflowSession.read_jsonl(args.path)
    if args.json:
        print(json.dumps(session.summary(), indent=2, sort_keys=True))
    else:
        summary = session.summary()
        print("WORKFLOW MEASUREMENT VERIFY PASS")
        print(f"session_id={summary['session_id']}")
        print(f"events={summary['event_count']} chain={summary['event_chain_sha256']}")
        print(f"active_review_seconds={summary['active_review_seconds']}")
        print(f"total_usd={summary['cost']['total_usd']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
