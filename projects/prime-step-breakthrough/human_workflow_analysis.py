#!/usr/bin/env python3
"""Reveal and analyze sealed browser sessions for the UCI human pilot.

This command is deliberately a post-session step.  It verifies the immutable
workflow JSONL first, then reads the UCI test labels and joins them by the
frozen item IDs.  The output contains aggregate metrics only; it does not
rewrite the event file or make a labor-saving claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

import prospective_uci_blind as uci
from workflow_measurement import WorkflowSession


SCHEMA = "uci-human-workflow-result-v1"
ORDER_SCHEMA = "uci-human-workflow-order-v1"
DEFAULT_WARMUP = 5


class AnalysisError(ValueError):
    """Fail-closed post-session analysis error."""


def _canonical(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _sha256_value(value: object) -> str:
    return hashlib.sha256(_canonical(value)).hexdigest()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AnalysisError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AnalysisError(f"expected JSON object: {path}")
    return value


def _atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=True, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _manifest_by_digest(manifest_dir: Path) -> dict[str, dict[str, Any]]:
    metadata = _read_json(manifest_dir / "metadata.json")
    if metadata.get("outcome_state") != "ABSENT_BY_DESIGN":
        raise AnalysisError("participant metadata is not label-blind")
    metadata_hashes = metadata.get("manifest_sha256")
    if not isinstance(metadata_hashes, dict):
        raise AnalysisError("participant metadata lacks manifest hashes")
    manifests: dict[str, dict[str, Any]] = {}
    for path in sorted(manifest_dir.glob("manifest-*.json")):
        expected_file_hash = metadata_hashes.get(path.name)
        if not isinstance(expected_file_hash, str) or _sha256_file(path) != expected_file_hash:
            raise AnalysisError(f"participant manifest file hash mismatch: {path}")
        manifest = _read_json(path)
        digest = manifest.get("order_digest")
        cohort = manifest.get("cohort_digest")
        items = manifest.get("items")
        if not isinstance(digest, str) or not isinstance(cohort, str) or not isinstance(items, list):
            raise AnalysisError(f"invalid participant manifest: {path}")
        item_ids = [item.get("item_id") for item in items if isinstance(item, dict)]
        if len(item_ids) != len(items) or len(set(item_ids)) != len(item_ids):
            raise AnalysisError(f"manifest has invalid item IDs: {path}")
        condition = manifest.get("condition")
        if not isinstance(condition, str) or not condition.startswith("uci-human-"):
            raise AnalysisError(f"manifest has invalid condition: {path}")
        order_name = condition.removeprefix("uci-human-")
        recomputed_digest = _sha256_value(
            {"schema": ORDER_SCHEMA, "name": order_name, "item_ids": item_ids}
        )
        if digest != recomputed_digest:
            raise AnalysisError(f"manifest order digest mismatch: {path}")
        if cohort != metadata.get("cohort_digest"):
            raise AnalysisError(f"manifest cohort digest mismatch: {path}")
        if digest in manifests:
            raise AnalysisError(f"duplicate order digest: {digest}")
        manifests[digest] = {
            "path": str(path),
            "condition": condition,
            "order_digest": digest,
            "cohort_digest": cohort,
            "item_ids": item_ids,
        }
    if not manifests:
        raise AnalysisError(f"no manifest-*.json files found in {manifest_dir}")
    return manifests


def _load_labels(dataset_path: Path, freeze_path: Path) -> dict[str, int]:
    freeze = _read_json(freeze_path)
    dataset = freeze.get("dataset")
    if not isinstance(dataset, dict) or dataset.get("archive_sha256") != _sha256_file(dataset_path):
        raise AnalysisError("dataset archive does not match the frozen UCI digest")
    complete = uci._load_dataset(dataset_path)
    _train_x, _train_y, _test_x, test_y = complete
    expected_rows = dataset.get("test_rows")
    if expected_rows != len(test_y):
        raise AnalysisError("revealed test-label count does not match the freeze")
    labels: dict[str, int] = {}
    for item in freeze.get("items", []):
        if not isinstance(item, dict):
            raise AnalysisError("freeze contains a non-object item")
        item_id = item.get("item_id")
        source_row = item.get("source_row")
        if not isinstance(item_id, str) or not isinstance(source_row, int):
            raise AnalysisError("freeze item lacks item_id/source_row")
        if source_row < 0 or source_row >= len(test_y):
            raise AnalysisError(f"source row outside revealed labels: {item_id}")
        labels[item_id] = int(test_y[source_row])
    return labels


def _expected_items(session: WorkflowSession, manifest: Mapping[str, Any]) -> None:
    if session.order_digest != manifest["order_digest"]:
        raise AnalysisError("session order digest does not match its participant manifest")
    if session.cohort_digest != manifest["cohort_digest"]:
        raise AnalysisError("session cohort digest does not match its participant manifest")
    expected_ids = tuple(manifest["item_ids"])
    if session.item_ids != expected_ids:
        raise AnalysisError("session item IDs/order do not match its participant manifest")


def analyze_session(
    session: WorkflowSession,
    manifest: Mapping[str, Any],
    labels: Mapping[str, int],
    *,
    warmup: int = DEFAULT_WARMUP,
) -> dict[str, Any]:
    """Return post-reveal metrics for one already-verified session."""

    if warmup < 1:
        raise AnalysisError("warmup must be positive")
    _expected_items(session, manifest)
    if session.condition != manifest.get("condition"):
        raise AnalysisError("session condition does not match its participant manifest")
    if set(session.item_ids) - set(labels):
        raise AnalysisError("revealed labels do not cover the session cohort")
    responses: list[dict[str, Any]] = []
    for event in session.events:
        if event.event_type != "response":
            continue
        if event.item_id is None:
            raise AnalysisError("response event has no item_id")
        selection = event.payload.get("selection")
        if isinstance(selection, bool) or not isinstance(selection, str) or not selection.isdigit():
            raise AnalysisError(f"response selection is not a digit: {selection!r}")
        selected_digit = int(selection)
        if not 0 <= selected_digit <= 9:
            raise AnalysisError(f"response selection outside digit range: {selection!r}")
        actual = int(labels[event.item_id])
        responses.append(
            {
                "item_id": event.item_id,
                "correct": selected_digit == actual,
            }
        )
    if not responses:
        raise AnalysisError("session contains no responses")
    correct = sum(1 for response in responses if response["correct"])
    final_accuracy = correct / len(responses)
    prefix_accuracy: list[float] = []
    running_correct = 0
    for index, response in enumerate(responses, 1):
        running_correct += int(response["correct"])
        prefix_accuracy.append(running_correct / index)
    tail = prefix_accuracy[warmup - 1 :]
    integrated_abs_error = sum(abs(value - final_accuracy) for value in tail) / len(tail) if tail else None
    summary = session.summary()
    return {
        "schema": SCHEMA,
        "session_id": session.session_id,
        "condition": session.condition,
        "order_digest": session.order_digest,
        "cohort_digest": session.cohort_digest,
        "item_count": len(session.item_ids),
        "shown_items": summary["shown_items"],
        "responses": len(responses),
        "skips": summary["skips"],
        "response_coverage": len(responses) / len(session.item_ids),
        "response_accuracy": final_accuracy,
        "warmup_responses": warmup,
        "integrated_absolute_prefix_accuracy_error": integrated_abs_error,
        "active_review_seconds": summary["active_review_seconds"],
        "adjudication_seconds": summary["adjudication_seconds"],
        "operator_overhead_seconds": summary["operator_overhead_seconds"],
        "cost": summary["cost"],
        "marketing_status": "NOT_CLEARED_UNTIL_PROSPECTIVE_HUMAN_STUDY",
    }


def analyze_file(
    session_path: Path,
    dataset_path: Path,
    freeze_path: Path,
    manifest_dir: Path,
    *,
    warmup: int = DEFAULT_WARMUP,
) -> dict[str, Any]:
    """Verify a sealed session, reveal labels, and analyze it."""

    session = WorkflowSession.read_jsonl(session_path)
    manifests = _manifest_by_digest(manifest_dir)
    manifest = manifests.get(session.order_digest)
    if manifest is None:
        raise AnalysisError("session order digest is not one of the frozen manifests")
    labels = _load_labels(dataset_path, freeze_path)
    return analyze_session(session, manifest, labels, warmup=warmup)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", type=Path, help="sealed browser workflow JSONL")
    parser.add_argument("--dataset", type=Path, required=True, help="pinned UCI archive")
    parser.add_argument("--freeze", type=Path, required=True, help="label-blind freeze.json")
    parser.add_argument("--manifest-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--warmup", type=int, default=DEFAULT_WARMUP)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    result = analyze_file(
        args.session,
        args.dataset,
        args.freeze,
        args.manifest_dir,
        warmup=args.warmup,
    )
    _atomic_json(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
