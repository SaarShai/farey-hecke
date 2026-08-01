#!/usr/bin/env python3
"""Freeze and reveal a label-blind UCI ML prefix-audit study.

The freeze contains only model metadata that would exist before an audit label
is inspected: predicted class, confidence stratum, item identity, and three
complete order commitments.  Test labels are deliberately absent from the
freeze.  A later reveal recomputes the committed metadata, reads the labels,
and writes a result bound to the freeze digest.

This is prospective with respect to the declared analysis and order commit. It
is still an offline public-dataset study, not a production or human-workflow
result; the report keeps that boundary explicit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import real_data_ml_simulation as audit


SCHEMA = "prospective-uci-blind-freeze-v1"
RESULT_SCHEMA = "prospective-uci-blind-result-v1"
PILOT_ID = "uci-optdigits-2026-08-01"
DEFAULT_SEED = 20260801
DEFAULT_WARMUP = 50
DEFAULT_MARGIN_BINS = 5
FORBIDDEN_ITEM_KEYS = frozenset(
    {"actual", "correct", "ground_truth", "label", "outcome", "target", "truth", "y"}
)


class PilotError(RuntimeError):
    """Fail-closed protocol error."""


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _atomic_write(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def atomic_json(path: Path, value: object) -> None:
    _atomic_write(path, json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def iso_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise PilotError(f"timestamp lacks timezone: {value}")
    return parsed.astimezone(timezone.utc)


def _manifest_core(manifest: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in manifest.items() if key != "commitment_sha256"}


def _result_core(result: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in result.items() if key != "commitment_sha256"}


def _script_sha256() -> str:
    return sha256_file(Path(__file__).resolve())


def _load_dataset(path: Path) -> tuple[
    list[tuple[int, ...]], list[int], list[tuple[int, ...]], list[int]
]:
    """Small indirection that keeps unit tests offline and deterministic."""

    return audit.load_dataset(path)


def _order_digest(name: str, item_ids: list[str]) -> str:
    return sha256_bytes(
        canonical_bytes(
            {"schema": "prospective-uci-order-v1", "name": name, "item_ids": item_ids}
        )
    )


def _metadata_from_rows(
    train_x: list[tuple[int, ...]],
    train_y: list[int],
    test_x: list[tuple[int, ...]],
    *,
    seed: int,
    bins: int,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, list[int]]]:
    """Build frozen metadata and orders without reading test labels."""

    if not test_x:
        raise PilotError("test feature set is empty")
    centroids = audit.train_centroids(train_x, train_y)
    train_predictions, train_margins = audit.predict_with_margin(train_x, centroids)
    test_predictions, test_margins = audit.predict_with_margin(test_x, centroids)
    thresholds = audit.margin_thresholds_by_prediction(train_predictions, train_margins, bins)
    strata = audit.joint_strata(test_predictions, test_margins, thresholds)
    quota_result, queues = audit.quota_plan(strata)
    random_indices, quota_indices = audit.priority_orders(seed, quota_result, queues)
    item_ids = [f"test-{index:04d}" for index in range(len(test_x))]
    items: list[dict[str, Any]] = []
    for index, (prediction, margin, stratum) in enumerate(
        zip(test_predictions, test_margins, strata, strict=True)
    ):
        prefix = stratum.rsplit("margin-", 1)[-1]
        items.append(
            {
                "item_id": item_ids[index],
                "source_row": index,
                "predicted_label": prediction,
                "margin": margin,
                "margin_bin": int(prefix),
                "stratum": stratum,
            }
        )
    index_orders = {
        "production": list(range(len(items))),
        "seeded_random": random_indices,
        "quota_balanced": quota_indices,
    }
    orders: dict[str, Any] = {}
    for name, indices in index_orders.items():
        ordered_ids = [item_ids[index] for index in indices]
        orders[name] = {
            "item_ids": ordered_ids,
            "sha256": _order_digest(name, ordered_ids),
            "randomization_certified": name in {"seeded_random", "quota_balanced"},
        }
    certificate_report = audit.verify_quota_result(quota_result)
    if not certificate_report.passed:
        raise PilotError(f"quota certificate failed: {certificate_report.errors}")
    certificate = {
        "verified": True,
        "algorithm": quota_result.algorithm,
        "categories": list(quota_result.categories),
        "counts": list(quota_result.counts),
        "order_codes_sha256": quota_result.order_sha256,
        "max_declared_cell_discrepancy": str(quota_result.max_discrepancy),
        "lower_bound": str(quota_result.lower_bound),
        "ratio_bound": (
            str(quota_result.ratio_bound) if quota_result.ratio_bound is not None else None
        ),
    }
    return items, {"orders": orders, "certificate": certificate}, thresholds


def build_freeze_manifest(
    dataset_path: Path,
    *,
    frozen_at: str,
    seed: int = DEFAULT_SEED,
    warmup: int = DEFAULT_WARMUP,
    bins: int = DEFAULT_MARGIN_BINS,
    pilot_id: str = PILOT_ID,
) -> dict[str, Any]:
    """Create a freeze manifest whose items contain no test outcomes."""

    if warmup < 1 or bins < 1:
        raise PilotError("warmup and margin bins must be positive")
    train_x, train_y, test_x, _test_y = _load_dataset(dataset_path)
    if warmup > len(test_x):
        raise PilotError("warmup cannot exceed the test item count")
    items, order_payload, thresholds = _metadata_from_rows(
        train_x, train_y, test_x, seed=seed, bins=bins
    )
    item_ids = [item["item_id"] for item in items]
    manifest: dict[str, Any] = {
        "schema": SCHEMA,
        "pilot_id": pilot_id,
        "frozen_at_utc": frozen_at,
        "outcome_state": "ABSENT_BY_DESIGN",
        "dataset": {
            "name": "UCI Optical Recognition of Handwritten Digits",
            "doi": audit.DATASET_DOI,
            "url": audit.DATASET_URL,
            "license": "CC BY 4.0",
            "archive_sha256": sha256_file(dataset_path),
            "train_rows": len(train_y),
            "test_rows": len(test_x),
            "features": len(test_x[0]),
        },
        "model": {
            "name": "nearest class centroid, squared Euclidean distance",
            "training_source": "UCI designated training split only",
            "outcomes_used": False,
        },
        "strata": {
            "definition": "predicted digit x within-predicted-digit margin bin",
            "ground_truth_used_to_define_strata": False,
            "correctness_used_to_define_strata": False,
            "margin_bins": bins,
            "margin_thresholds_by_prediction": {
                str(prediction): list(values) for prediction, values in thresholds.items()
            },
        },
        "randomization": {
            "seed": seed,
            "pairing": "the same per-item priorities define the random and quota orders",
        },
        "analysis_preregistration": {
            "primary_metric": "integrated absolute prefix accuracy error after warmup",
            "secondary_metric": "integrated squared prefix accuracy error after warmup",
            "warmup": warmup,
            "comparison": "production order, seeded random order, quota-balanced order",
            "labels_available_at_freeze": False,
            "claim_boundary": (
                "offline public-dataset ML audit evidence; not a production or human-time result"
            ),
        },
        "items": items,
        "orders": order_payload["orders"],
        "quota_certificate": order_payload["certificate"],
        "item_count": len(item_ids),
        "generator_sha256": _script_sha256(),
    }
    manifest["commitment_sha256"] = sha256_bytes(canonical_bytes(_manifest_core(manifest)))
    return manifest


def render_freeze_readme(manifest: dict[str, Any], freeze_sha256: str) -> str:
    return "\n".join(
        [
            "# Prospective UCI blind audit",
            "",
            f"Pilot: `{manifest['pilot_id']}`",
            f"Frozen: `{manifest['frozen_at_utc']}`",
            f"Items: **{manifest['item_count']}**",
            "Outcome state: **ABSENT_BY_DESIGN**",
            "",
            "## Commitments",
            "",
            f"- freeze.json SHA-256: `{freeze_sha256}`",
            f"- manifest core SHA-256: `{manifest['commitment_sha256']}`",
            *[
                f"- {name} order: `{order['sha256']}`"
                for name, order in manifest["orders"].items()
            ],
            "",
            "The freeze contains predicted labels and confidence strata only. Test labels are not written to the manifest.",
            "The result must be generated in a later reveal step and remains bound to this freeze digest.",
            "",
            "## Commands",
            "",
            "```bash",
            "PYTHONPATH=src python3 prospective_uci_blind.py verify --dataset /path/to/optdigits.zip --pilot-dir pilots/uci-optdigits-2026-08-01",
            "PYTHONPATH=src python3 prospective_uci_blind.py reveal --dataset /path/to/optdigits.zip --pilot-dir pilots/uci-optdigits-2026-08-01",
            "```",
            "",
        ]
    )


def write_freeze(pilot_dir: Path, manifest: dict[str, Any]) -> None:
    if pilot_dir.exists():
        raise PilotError(f"pilot directory already exists; refusing overwrite: {pilot_dir}")
    pilot_dir.mkdir(parents=True)
    atomic_json(pilot_dir / "freeze.json", manifest)
    freeze_sha = sha256_file(pilot_dir / "freeze.json")
    _atomic_write(pilot_dir / "freeze.sha256", f"{freeze_sha}  freeze.json\n".encode("ascii"))
    _atomic_write(
        pilot_dir / "README.md", render_freeze_readme(manifest, freeze_sha).encode("utf-8")
    )


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PilotError(f"invalid JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise PilotError(f"expected an object: {path}")
    return value


def _expected_digest(path: Path, name: str) -> str:
    try:
        parts = path.read_text(encoding="ascii").strip().split()
    except OSError as exc:
        raise PilotError(f"missing digest sidecar: {path}") from exc
    if len(parts) != 2 or parts[1] != f"{name}.json":
        raise PilotError(f"malformed digest sidecar: {path}")
    return parts[0]


def _read_freeze(pilot_dir: Path) -> dict[str, Any]:
    path = pilot_dir / "freeze.json"
    if not path.is_file():
        raise PilotError(f"missing freeze manifest: {path}")
    return _read_json(path)


def verify_freeze(pilot_dir: Path, dataset_path: Path) -> dict[str, Any]:
    manifest = _read_freeze(pilot_dir)
    if manifest.get("schema") != SCHEMA or manifest.get("outcome_state") != "ABSENT_BY_DESIGN":
        raise PilotError("freeze schema or outcome state is invalid")
    actual_sha = sha256_file(pilot_dir / "freeze.json")
    if actual_sha != _expected_digest(pilot_dir / "freeze.sha256", "freeze"):
        raise PilotError("freeze.json does not match freeze.sha256")
    if sha256_bytes(canonical_bytes(_manifest_core(manifest))) != manifest.get(
        "commitment_sha256"
    ):
        raise PilotError("manifest core commitment does not match")
    if sha256_file(dataset_path) != manifest["dataset"]["archive_sha256"]:
        raise PilotError("dataset archive digest does not match the freeze")
    for item in manifest["items"]:
        forbidden = FORBIDDEN_ITEM_KEYS.intersection(item)
        if forbidden:
            raise PilotError(f"freeze item contains outcome-bearing keys: {sorted(forbidden)}")
    train_x, train_y, test_x, _test_y = _load_dataset(dataset_path)
    rebuilt = build_freeze_manifest(
        dataset_path,
        frozen_at=str(manifest["frozen_at_utc"]),
        seed=int(manifest["randomization"]["seed"]),
        warmup=int(manifest["analysis_preregistration"]["warmup"]),
        bins=int(manifest["strata"]["margin_bins"]),
        pilot_id=str(manifest["pilot_id"]),
    )
    if _manifest_core(rebuilt) != _manifest_core(manifest):
        raise PilotError("freeze does not recompute from the pinned dataset")
    if len(train_x) != manifest["dataset"]["train_rows"] or len(test_x) != manifest["dataset"]["test_rows"]:
        raise PilotError("dataset row counts do not match the freeze")
    return {
        "freeze_verified": True,
        "pilot_id": manifest["pilot_id"],
        "item_count": manifest["item_count"],
        "freeze_file_sha256": actual_sha,
        "commitment_sha256": manifest["commitment_sha256"],
        "orders": {name: order["sha256"] for name, order in manifest["orders"].items()},
    }


def _order_indices(manifest: dict[str, Any], name: str) -> list[int]:
    index = {item["item_id"]: int(item["source_row"]) for item in manifest["items"]}
    try:
        return [index[item_id] for item_id in manifest["orders"][name]["item_ids"]]
    except KeyError as exc:
        raise PilotError(f"unknown item in {name} order: {exc}") from exc


def _trajectory(outcomes: list[int], order: list[int], manifest: dict[str, Any]) -> list[dict[str, Any]]:
    final_accuracy = sum(outcomes) / len(outcomes)
    running = 0
    rows: list[dict[str, Any]] = []
    for prefix, index in enumerate(order, 1):
        running += outcomes[index]
        estimate = running / prefix
        rows.append(
            {
                "prefix": prefix,
                "item_id": manifest["items"][index]["item_id"],
                "correct": outcomes[index],
                "running_accuracy": estimate,
                "signed_error": estimate - final_accuracy,
                "absolute_error": abs(estimate - final_accuracy),
            }
        )
    return rows


def _order_analysis(rows: list[dict[str, Any]], warmup: int) -> dict[str, Any]:
    tail = rows[warmup - 1 :]
    return {
        "integrated_absolute_prefix_error": statistics.fmean(
            row["absolute_error"] for row in tail
        ),
        "integrated_squared_prefix_error": statistics.fmean(
            row["signed_error"] ** 2 for row in tail
        ),
        "one_percent_settling_prefix": next(
            (
                prefix
                for prefix in range(1, len(rows) + 1)
                if all(row["absolute_error"] <= 0.01 for row in rows[prefix - 1 :])
            ),
            len(rows),
        ),
    }


def build_result(
    pilot_dir: Path,
    dataset_path: Path,
    *,
    revealed_at: str,
) -> dict[str, Any]:
    freeze_report = verify_freeze(pilot_dir, dataset_path)
    manifest = _read_freeze(pilot_dir)
    if iso_utc(revealed_at) <= iso_utc(str(manifest["frozen_at_utc"])):
        raise PilotError("reveal timestamp must be after the freeze")
    train_x, train_y, test_x, test_y = _load_dataset(dataset_path)
    centroids = audit.train_centroids(train_x, train_y)
    predictions, _margins = audit.predict_with_margin(test_x, centroids)
    outcomes = [int(prediction == label) for prediction, label in zip(predictions, test_y, strict=True)]
    warmup = int(manifest["analysis_preregistration"]["warmup"])
    order_results: dict[str, Any] = {}
    for name in ("production", "seeded_random", "quota_balanced"):
        rows = _trajectory(outcomes, _order_indices(manifest, name), manifest)
        metrics = _order_analysis(rows, warmup)
        order_results[name] = {
            "metrics": metrics,
            "trajectory_sha256": sha256_bytes(canonical_bytes(rows)),
            "trajectory": rows,
        }
    revealed_items = [
        {
            "item_id": item["item_id"],
            "label": int(label),
            "predicted_label": int(prediction),
            "correct": int(correct),
        }
        for item, label, prediction, correct in zip(
            manifest["items"], test_y, predictions, outcomes, strict=True
        )
    ]
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "pilot_id": manifest["pilot_id"],
        "outcome_state": "REVEALED",
        "revealed_at_utc": revealed_at,
        "freeze_file_sha256": freeze_report["freeze_file_sha256"],
        "freeze_commitment_sha256": manifest["commitment_sha256"],
        "dataset_archive_sha256": manifest["dataset"]["archive_sha256"],
        "analysis": {
            "final_accuracy": sum(outcomes) / len(outcomes),
            "correct_count": sum(outcomes),
            "item_count": len(outcomes),
            "warmup": warmup,
            "orders": order_results,
        },
        "revealed_items": revealed_items,
        "claim_boundary": (
            "This is prospective public-dataset ML audit evidence. It does not establish "
            "human-time, production, universal, or monetary savings."
        ),
        "generator_sha256": _script_sha256(),
    }
    result["commitment_sha256"] = sha256_bytes(canonical_bytes(_result_core(result)))
    return result


def render_result_report(result: dict[str, Any]) -> str:
    orders = result["analysis"]["orders"]
    lines = [
        "# Prospective UCI blind-audit result",
        "",
        f"Pilot: `{result['pilot_id']}`",
        f"Revealed: `{result['revealed_at_utc']}`",
        f"Final accuracy: `{result['analysis']['final_accuracy']:.6f}`",
        "",
        "| Order | Integrated absolute error | Integrated squared error | 1% settling prefix |",
        "|---|---:|---:|---:|",
    ]
    for name, data in orders.items():
        metrics = data["metrics"]
        lines.append(
            f"| {name} | {metrics['integrated_absolute_prefix_error']:.8f} | "
            f"{metrics['integrated_squared_prefix_error']:.8f} | "
            f"{metrics['one_percent_settling_prefix']} |"
        )
    lines.extend(
        [
            "",
            f"Freeze file SHA-256: `{result['freeze_file_sha256']}`",
            f"Result commitment SHA-256: `{result['commitment_sha256']}`",
            "",
            result["claim_boundary"],
            "",
        ]
    )
    return "\n".join(lines)


def write_result(pilot_dir: Path, result: dict[str, Any]) -> None:
    if (pilot_dir / "result.json").exists():
        raise PilotError(f"result already exists; refusing overwrite: {pilot_dir / 'result.json'}")
    atomic_json(pilot_dir / "result.json", result)
    result_sha = sha256_file(pilot_dir / "result.json")
    _atomic_write(pilot_dir / "result.sha256", f"{result_sha}  result.json\n".encode("ascii"))
    _atomic_write(
        pilot_dir / "RESULT.md", render_result_report(result).encode("utf-8")
    )


def verify_result(pilot_dir: Path, dataset_path: Path) -> dict[str, Any]:
    result_path = pilot_dir / "result.json"
    if not result_path.is_file():
        raise PilotError(f"missing result: {result_path}")
    result = _read_json(result_path)
    if result.get("schema") != RESULT_SCHEMA or result.get("outcome_state") != "REVEALED":
        raise PilotError("result schema or outcome state is invalid")
    actual_sha = sha256_file(result_path)
    if actual_sha != _expected_digest(pilot_dir / "result.sha256", "result"):
        raise PilotError("result.json does not match result.sha256")
    if sha256_bytes(canonical_bytes(_result_core(result))) != result.get("commitment_sha256"):
        raise PilotError("result commitment does not match")
    rebuilt = build_result(
        pilot_dir,
        dataset_path,
        revealed_at=str(result["revealed_at_utc"]),
    )
    if _result_core(rebuilt) != _result_core(result):
        raise PilotError("result does not recompute from the freeze and dataset")
    return {
        "result_verified": True,
        "pilot_id": result["pilot_id"],
        "result_file_sha256": actual_sha,
        "commitment_sha256": result["commitment_sha256"],
    }


def status(pilot_dir: Path) -> dict[str, Any]:
    freeze = _read_freeze(pilot_dir)
    result_path = pilot_dir / "result.json"
    return {
        "pilot_id": freeze.get("pilot_id"),
        "freeze_state": freeze.get("outcome_state"),
        "result_state": "REVEALED" if result_path.exists() else "NOT_REVEALED",
        "item_count": freeze.get("item_count"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("verify", "reveal"):
        subparser = subparsers.add_parser(name)
        subparser.add_argument("--dataset", type=Path, required=True)
        subparser.add_argument("--pilot-dir", type=Path, required=True)
    freeze_parser = subparsers.add_parser("freeze")
    freeze_parser.add_argument("--dataset", type=Path, required=True)
    freeze_parser.add_argument("--pilot-dir", type=Path, required=True)
    freeze_parser.add_argument("--frozen-at", default=_utc_now())
    freeze_parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    freeze_parser.add_argument("--warmup", type=int, default=DEFAULT_WARMUP)
    freeze_parser.add_argument("--margin-bins", type=int, default=DEFAULT_MARGIN_BINS)
    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("--pilot-dir", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        if arguments.command == "freeze":
            manifest = build_freeze_manifest(
                arguments.dataset,
                frozen_at=arguments.frozen_at,
                seed=arguments.seed,
                warmup=arguments.warmup,
                bins=arguments.margin_bins,
            )
            write_freeze(arguments.pilot_dir, manifest)
            print(json.dumps({"freeze_written": True, "pilot_id": manifest["pilot_id"]}))
        elif arguments.command == "verify":
            print(json.dumps(verify_freeze(arguments.pilot_dir, arguments.dataset), indent=2))
        elif arguments.command == "reveal":
            result = build_result(
                arguments.pilot_dir,
                arguments.dataset,
                revealed_at=_utc_now(),
            )
            write_result(arguments.pilot_dir, result)
            print(json.dumps({"result_written": True, "pilot_id": result["pilot_id"]}))
        else:
            print(json.dumps(status(arguments.pilot_dir), indent=2))
    except (OSError, PilotError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
