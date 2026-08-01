#!/usr/bin/env python3
"""Build matched label-blind browser manifests for a human UCI pilot.

The exporter consumes the frozen UCI metadata and test *features* only.  It
never converts or stores the test-label column.  Three manifests share one
deterministic cohort and differ only in the committed production, seeded-random,
and quota-balanced order.  The resulting JSON is accepted by ``web/pilot.html``
and contains no model metadata or outcome fields that could reveal a label.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

import prospective_uci_blind as uci


SCHEMA = "uci-human-workflow-manifest-v1"
COHORT_SCHEMA = "uci-human-workflow-cohort-v1"
ORDER_SCHEMA = "uci-human-workflow-order-v1"
ORDER_NAMES = ("production", "seeded_random", "quota_balanced")
FORBIDDEN_KEYS = frozenset(
    {
        "actual",
        "answer",
        "correct",
        "gold",
        "ground_truth",
        "label",
        "loss",
        "outcome",
        "target",
        "truth",
        "y",
    }
)
ASCII_LEVELS = " .:-=+*#%@"


class ManifestError(ValueError):
    """Fail-closed manifest-generation error."""


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def sha256_value(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


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


def _walk_forbidden(value: object, path: str = "manifest") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_KEYS:
                raise ManifestError(f"{path}.{key} is forbidden in a label-blind manifest")
            _walk_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden(child, f"{path}[{index}]")


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ManifestError(f"cannot read JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ManifestError(f"expected JSON object: {path}")
    return value


def _freeze_items(freeze: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if freeze.get("outcome_state") != "ABSENT_BY_DESIGN":
        raise ManifestError("freeze is not marked ABSENT_BY_DESIGN")
    items = freeze.get("items")
    if not isinstance(items, list) or not items:
        raise ManifestError("freeze items are missing or empty")
    _walk_forbidden(items, "freeze.items")
    by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ManifestError(f"freeze.items[{index}] must be an object")
        item_id = item.get("item_id")
        if not isinstance(item_id, str) or not item_id:
            raise ManifestError(f"freeze.items[{index}] has an invalid item_id")
        if item_id in by_id:
            raise ManifestError(f"duplicate freeze item_id: {item_id}")
        if not isinstance(item.get("source_row"), int):
            raise ManifestError(f"freeze item {item_id} lacks an integer source_row")
        if not isinstance(item.get("predicted_label"), int) or not 0 <= item["predicted_label"] <= 9:
            raise ManifestError(f"freeze item {item_id} lacks a digit prediction")
        if not isinstance(item.get("margin_bin"), int):
            raise ManifestError(f"freeze item {item_id} lacks a margin_bin")
        by_id[item_id] = item
    orders = freeze.get("orders")
    if not isinstance(orders, dict):
        raise ManifestError("freeze orders are missing")
    for name in ORDER_NAMES:
        order = orders.get(name)
        if not isinstance(order, dict) or not isinstance(order.get("item_ids"), list):
            raise ManifestError(f"freeze order {name} is missing")
        if set(order["item_ids"]) != set(by_id):
            raise ManifestError(f"freeze order {name} does not cover the frozen cohort")
    return sorted(by_id.values(), key=lambda item: item["source_row"]), by_id


def _round_robin_margin_selection(
    items: Iterable[dict[str, Any]], per_prediction: int
) -> list[dict[str, Any]]:
    buckets: dict[int, dict[int, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for item in sorted(items, key=lambda row: row["source_row"]):
        buckets[item["predicted_label"]][item["margin_bin"]].append(item)
    selected: list[dict[str, Any]] = []
    for prediction in sorted(buckets):
        streams = [buckets[prediction][margin] for margin in sorted(buckets[prediction])]
        count = 0
        while count < per_prediction:
            progressed = False
            for stream in streams:
                if stream:
                    selected.append(stream.pop(0))
                    count += 1
                    progressed = True
                    if count == per_prediction:
                        break
            if not progressed:
                raise ManifestError(
                    f"prediction {prediction} has fewer than {per_prediction} available items"
                )
    return selected


def render_feature_prompt(features: Iterable[int]) -> str:
    values = tuple(int(value) for value in features)
    if len(values) != 64 or any(value < 0 or value > 16 for value in values):
        raise ManifestError("UCI feature row must contain 64 values in [0, 16]")
    lines = []
    for row in range(8):
        pixels = values[row * 8 : (row + 1) * 8]
        line = "".join(ASCII_LEVELS[round(value * (len(ASCII_LEVELS) - 1) / 16)] for value in pixels)
        lines.append(line)
    return (
        "Identify the handwritten digit shown below.\n\n"
        + "\n".join(lines)
        + "\n\nSelect one digit from 0 to 9."
    )


def _choices() -> list[dict[str, str]]:
    return [{"choice_id": str(digit), "text": str(digit)} for digit in range(10)]


def build_manifests(
    freeze: dict[str, Any],
    test_features: list[tuple[int, ...]],
    *,
    per_prediction: int = 10,
) -> dict[str, dict[str, Any]]:
    """Return three matched manifests without reading test outcomes."""

    if per_prediction < 1:
        raise ManifestError("per_prediction must be positive")
    ordered_items, by_id = _freeze_items(freeze)
    if len(test_features) != len(ordered_items):
        raise ManifestError("test feature count does not match freeze item count")
    selected = _round_robin_margin_selection(ordered_items, per_prediction)
    cohort_ids = [item["item_id"] for item in selected]
    cohort_digest = sha256_value({"schema": COHORT_SCHEMA, "item_ids": cohort_ids})
    cohort_set = set(cohort_ids)
    outputs: dict[str, dict[str, Any]] = {}
    for name in ORDER_NAMES:
        full_order = freeze["orders"][name]["item_ids"]
        ordered_ids = [item_id for item_id in full_order if item_id in cohort_set]
        if set(ordered_ids) != cohort_set or len(ordered_ids) != len(cohort_ids):
            raise ManifestError(f"projected order {name} does not cover the selected cohort")
        order_digest = sha256_value(
            {"schema": ORDER_SCHEMA, "name": name, "item_ids": ordered_ids}
        )
        participant_items = []
        for item_id in ordered_ids:
            item = by_id[item_id]
            source_row = item["source_row"]
            participant_items.append(
                {
                    "item_id": item_id,
                    "prompt": render_feature_prompt(test_features[source_row]),
                    "choices": _choices(),
                }
            )
        manifest = {
            "condition": f"uci-human-{name}",
            "order_digest": order_digest,
            "cohort_digest": cohort_digest,
            "items": participant_items,
        }
        _walk_forbidden(manifest)
        outputs[name] = manifest
    return outputs


def generate_manifests(
    dataset_path: Path,
    freeze_path: Path,
    output_dir: Path,
    *,
    per_prediction: int = 10,
) -> dict[str, dict[str, Any]]:
    """Load only feature rows and write three new manifest files."""

    if output_dir.exists():
        raise ManifestError(f"refusing to overwrite existing directory: {output_dir}")
    freeze = _read_json(freeze_path)
    _freeze_items(freeze)
    _train_x, _train_y, test_features = uci._load_features_for_freeze(dataset_path)
    manifests = build_manifests(freeze, test_features, per_prediction=per_prediction)
    output_dir.mkdir(parents=True)
    for name, manifest in manifests.items():
        _atomic_json(output_dir / f"manifest-{name}.json", manifest)
    manifest_hashes = {
        f"manifest-{name}.json": sha256_file(output_dir / f"manifest-{name}.json")
        for name in manifests
    }
    metadata = {
        "schema": SCHEMA,
        "freeze_sha256": hashlib.sha256(freeze_path.read_bytes()).hexdigest(),
        "dataset_archive_sha256": uci.sha256_file(dataset_path),
        "per_prediction": per_prediction,
        "item_count": len(next(iter(manifests.values()))["items"]),
        "cohort_digest": next(iter(manifests.values()))["cohort_digest"],
        "conditions": list(ORDER_NAMES),
        "manifest_sha256": manifest_hashes,
        "outcome_state": "ABSENT_BY_DESIGN",
        "labels_read": False,
    }
    _atomic_json(output_dir / "metadata.json", metadata)
    return manifests


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True, help="pinned UCI archive")
    parser.add_argument("--freeze", type=Path, required=True, help="label-blind freeze.json")
    parser.add_argument("--output", type=Path, required=True, help="new output directory")
    parser.add_argument("--per-prediction", type=int, default=10)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    generate_manifests(
        args.dataset,
        args.freeze,
        args.output,
        per_prediction=args.per_prediction,
    )
    print(f"HUMAN WORKFLOW MANIFESTS WRITTEN: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
