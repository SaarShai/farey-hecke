#!/usr/bin/env python3
"""Outcome-blind replay on the public NetEaseCrowd human-annotation corpus.

The freeze reads only task, worker, capability, and completion-time metadata.
Answers and truth labels are read only by ``reveal``.  The resulting comparison
uses real human annotations and errors, but it does *not* turn completion
timestamps into active labor time: timestamps are reported as provenance and an
elapsed-time proxy only.  A professional workflow study is still required for
any labor-saving claim.

The Parquet reader is optional for the core project.  Install ``pyarrow`` only
when running this external-data audit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import statistics
import tempfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator
from urllib.request import Request, urlopen

from coprimebatch.prefix_balance import quota_order, verify_quota_result


SCHEMA = "neteasecrowd-human-freeze-v1"
RESULT_SCHEMA = "neteasecrowd-human-result-v1"
PILOT_ID = "neteasecrowd-human-annotation-2026-08-01"
DATASET_URL = "https://huggingface.co/datasets/liuhyuu/NetEaseCrowd/resolve/main/annotation.parquet"
DATASET_SHA256 = "40336e3d5f24a846892be6065e25e99923e15b2e3b1b32bc79ee175faf9f1151"
DATASET_ROWS = 6_016_319
DATASET_LICENSE = "CC-BY-SA-4.0"
DEFAULT_TASKSETS = 12
DEFAULT_PER_TASKSET = 2_000
DEFAULT_WARMUP = 100
DEFAULT_SEED = 20260801
METADATA_COLUMNS = ("tasksetId", "taskId", "workerId", "completeTime", "capability")
OUTCOME_COLUMNS = METADATA_COLUMNS + ("answer", "truth")


class AuditError(RuntimeError):
    """Fail-closed external-data audit error."""


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
        raise AuditError(f"timestamp lacks timezone: {value}")
    return parsed.astimezone(timezone.utc)


def _manifest_core(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key != "commitment_sha256"}


def _result_core(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if key != "commitment_sha256"}


def _semantic_core(value: dict[str, Any], *, result: bool = False) -> dict[str, Any]:
    core = _result_core(value) if result else _manifest_core(value)
    core.pop("generator_sha256", None)
    return core


def _script_sha256() -> str:
    return sha256_file(Path(__file__).resolve())


def _pyarrow_parquet(path: Path) -> Any:
    try:
        import pyarrow.parquet as parquet
    except ModuleNotFoundError as exc:
        raise AuditError("pyarrow is required for this external audit") from exc
    try:
        return parquet.ParquetFile(path)
    except Exception as exc:  # pyarrow exposes several reader-specific errors
        raise AuditError(f"cannot open Parquet source {path}: {exc}") from exc


def _rows(path: Path, columns: tuple[str, ...]) -> Iterator[dict[str, int]]:
    parquet = _pyarrow_parquet(path)
    names = set(parquet.schema_arrow.names)
    missing = set(columns) - names
    if missing:
        raise AuditError(f"Parquet source is missing columns: {sorted(missing)}")
    for batch in parquet.iter_batches(columns=list(columns), batch_size=100_000):
        arrays = [batch.column(index).to_pylist() for index in range(len(columns))]
        for values in zip(*arrays, strict=True):
            yield {column: int(value) for column, value in zip(columns, values, strict=True)}


def download_dataset(path: Path, *, offline: bool = False) -> Path:
    path = path.expanduser().resolve()
    if path.is_file() and sha256_file(path) == DATASET_SHA256:
        return path
    if offline:
        raise AuditError(f"no checksum-valid offline dataset at {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        request = Request(DATASET_URL, headers={"User-Agent": "farey-hecke-netease-audit/1"})
        with os.fdopen(descriptor, "wb") as output:
            with urlopen(request, timeout=120) as response:
                while block := response.read(1 << 20):
                    output.write(block)
            output.flush()
            os.fsync(output.fileno())
        observed = sha256_file(temporary_path)
        if observed != DATASET_SHA256:
            raise AuditError(f"dataset checksum mismatch: expected {DATASET_SHA256}, found {observed}")
        os.replace(temporary_path, path)
    except BaseException:
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass
        raise
    return path


def _selection_digest(items: list[dict[str, Any]]) -> str:
    return sha256_bytes(canonical_bytes(items))


def select_metadata(
    dataset_path: Path,
    *,
    tasksets: int = DEFAULT_TASKSETS,
    per_taskset: int = DEFAULT_PER_TASKSET,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Select tasksets using only metadata and return outcome-free rows."""

    if tasksets < 2 or per_taskset < 1:
        raise AuditError("require at least two tasksets and one row per taskset")
    if sha256_file(dataset_path) != DATASET_SHA256:
        raise AuditError("dataset checksum does not match the pinned source")
    counts: dict[int, int] = defaultdict(int)
    capabilities: dict[int, set[int]] = defaultdict(set)
    row_count = 0
    for row in _rows(dataset_path, ("tasksetId", "capability")):
        row_count += 1
        counts[row["tasksetId"]] += 1
        capabilities[row["tasksetId"]].add(row["capability"])
    if row_count != DATASET_ROWS:
        raise AuditError(f"expected {DATASET_ROWS} rows, found {row_count}")
    ranked = sorted(
        (taskset for taskset, count in counts.items() if count >= per_taskset),
        key=lambda value: sha256_bytes(f"selection-v1|{value}".encode("ascii")),
    )
    selected_tasksets = ranked[:tasksets]
    if len(selected_tasksets) != tasksets:
        raise AuditError("not enough tasksets meet the requested sample size")
    selected = set(selected_tasksets)
    items: list[dict[str, Any]] = []
    taken: dict[int, int] = defaultdict(int)
    for source_row, row in enumerate(_rows(dataset_path, METADATA_COLUMNS)):
        taskset = row["tasksetId"]
        if taskset not in selected or taken[taskset] >= per_taskset:
            continue
        taken[taskset] += 1
        items.append(
            {
                "item_id": f"annotation-{source_row:07d}",
                "source_row": source_row,
                "taskset_id": taskset,
                "task_id": row["taskId"],
                "worker_id": row["workerId"],
                "complete_time_ms": row["completeTime"],
                "capability": row["capability"],
            }
        )
    if any(taken[taskset] != per_taskset for taskset in selected_tasksets):
        raise AuditError("metadata selection did not collect the requested quota")
    selection = {
        "rule": "rank tasksets by SHA256(selection-v1|tasksetId), then take the first fixed rows per taskset",
        "tasksets": selected_tasksets,
        "per_taskset": per_taskset,
        "counts": {str(taskset): counts[taskset] for taskset in selected_tasksets},
        "capabilities": {
            str(taskset): sorted(capabilities[taskset]) for taskset in selected_tasksets
        },
        "item_count": len(items),
        "metadata_digest": _selection_digest(items),
    }
    return items, selection


def _order_digest(name: str, item_ids: list[str]) -> str:
    return sha256_bytes(
        canonical_bytes({"schema": "netease-human-order-v1", "name": name, "item_ids": item_ids})
    )


def _build_orders(items: list[dict[str, Any]], seed: int) -> tuple[dict[str, Any], dict[str, Any]]:
    queues: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(items):
        queues[str(item["taskset_id"])].append(index)
    quota = quota_order({category: len(queue) for category, queue in queues.items()})
    report = verify_quota_result(quota)
    if not report.passed:
        raise AuditError(f"quota certificate failed: {report.errors}")
    priorities = {
        index: sha256_bytes(f"human-audit-priority-v1|{seed}|{items[index]['item_id']}".encode("ascii"))
        for index in range(len(items))
    }
    random_indices = sorted(range(len(items)), key=lambda index: (priorities[index], index))
    ranked_queues = {
        category: sorted(queue, key=lambda index: (priorities[index], index))
        for category, queue in queues.items()
    }
    positions = {category: 0 for category in ranked_queues}
    quota_indices: list[int] = []
    for code in quota.order_codes:
        category = quota.categories[code]
        position = positions[category]
        quota_indices.append(ranked_queues[category][position])
        positions[category] = position + 1
    production_indices = sorted(
        range(len(items)),
        key=lambda index: (items[index]["complete_time_ms"], items[index]["source_row"]),
    )
    index_orders = {
        "production": production_indices,
        "seeded_random": random_indices,
        "quota_balanced": quota_indices,
    }
    orders: dict[str, Any] = {}
    item_ids = [item["item_id"] for item in items]
    for name, indices in index_orders.items():
        ordered_ids = [item_ids[index] for index in indices]
        orders[name] = {
            "item_ids": ordered_ids,
            "sha256": _order_digest(name, ordered_ids),
            "randomization_certified": name in {"seeded_random", "quota_balanced"},
        }
    certificate = {
        "verified": True,
        "algorithm": quota.algorithm,
        "categories": list(quota.categories),
        "counts": list(quota.counts),
        "order_codes_sha256": quota.order_sha256,
        "max_declared_cell_discrepancy": str(quota.max_discrepancy),
        "lower_bound": str(quota.lower_bound),
        "ratio_bound": str(quota.ratio_bound) if quota.ratio_bound is not None else None,
    }
    return orders, certificate


def build_freeze_manifest(
    dataset_path: Path,
    *,
    frozen_at: str,
    tasksets: int = DEFAULT_TASKSETS,
    per_taskset: int = DEFAULT_PER_TASKSET,
    seed: int = DEFAULT_SEED,
    warmup: int = DEFAULT_WARMUP,
    pilot_id: str = PILOT_ID,
) -> dict[str, Any]:
    if warmup < 1:
        raise AuditError("warmup must be positive")
    items, selection = select_metadata(
        dataset_path, tasksets=tasksets, per_taskset=per_taskset
    )
    if warmup > len(items):
        raise AuditError("warmup cannot exceed the selected item count")
    orders, certificate = _build_orders(items, seed)
    manifest: dict[str, Any] = {
        "schema": SCHEMA,
        "pilot_id": pilot_id,
        "frozen_at_utc": frozen_at,
        "outcome_state": "ABSENT_BY_DESIGN",
        "dataset": {
            "name": "NetEaseCrowd: A Dataset for Long-term and Online Crowdsourcing Truth Inference",
            "url": DATASET_URL,
            "arxiv": "https://arxiv.org/abs/2403.08826",
            "license": DATASET_LICENSE,
            "archive_sha256": sha256_file(dataset_path),
            "row_count": DATASET_ROWS,
        },
        "selection": selection,
        "items": items,
        "orders": orders,
        "quota_certificate": certificate,
        "randomization": {"seed": seed},
        "analysis_preregistration": {
            "primary_metric": "integrated absolute human-annotation accuracy error after warmup",
            "secondary_metric": "integrated squared human-annotation accuracy error after warmup",
            "warmup": warmup,
            "production_definition": "chronological order by recorded completeTime, source-row tie break",
            "labels_available_at_freeze": False,
            "timing_boundary": (
                "completeTime is provenance and an elapsed-time proxy; it is not active labor time"
            ),
        },
        "generator_sha256": _script_sha256(),
    }
    manifest["commitment_sha256"] = sha256_bytes(canonical_bytes(_manifest_core(manifest)))
    return manifest


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditError(f"invalid JSON {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuditError(f"expected JSON object: {path}")
    return value


def _expected_digest(path: Path, name: str) -> str:
    try:
        parts = path.read_text(encoding="ascii").strip().split()
    except OSError as exc:
        raise AuditError(f"missing digest sidecar: {path}") from exc
    if len(parts) != 2 or parts[1] != f"{name}.json":
        raise AuditError(f"malformed digest sidecar: {path}")
    return parts[0]


def write_freeze(pilot_dir: Path, manifest: dict[str, Any]) -> None:
    if pilot_dir.exists():
        raise AuditError(f"pilot directory already exists; refusing overwrite: {pilot_dir}")
    pilot_dir.mkdir(parents=True)
    atomic_json(pilot_dir / "freeze.json", manifest)
    digest = sha256_file(pilot_dir / "freeze.json")
    _atomic_write(pilot_dir / "freeze.sha256", f"{digest}  freeze.json\n".encode("ascii"))
    _atomic_write(
        pilot_dir / "README.md",
        (
            f"# NetEaseCrowd human-annotation audit\n\n"
            f"Pilot: `{manifest['pilot_id']}`\n\n"
            f"Frozen: `{manifest['frozen_at_utc']}`\n\n"
            f"Items: **{len(manifest['items'])}**\n\n"
            "Outcome state: **ABSENT_BY_DESIGN**\n\n"
            f"Freeze SHA-256: `{digest}`\n\n"
            "The freeze reads metadata only. It reports real human annotations after reveal, "
            "but recorded completion timestamps are not active labor time.\n"
        ).encode("utf-8"),
    )


def _read_freeze(pilot_dir: Path) -> dict[str, Any]:
    path = pilot_dir / "freeze.json"
    if not path.is_file():
        raise AuditError(f"missing freeze manifest: {path}")
    return _read_json(path)


def verify_freeze(pilot_dir: Path, dataset_path: Path) -> dict[str, Any]:
    manifest = _read_freeze(pilot_dir)
    if manifest.get("schema") != SCHEMA or manifest.get("outcome_state") != "ABSENT_BY_DESIGN":
        raise AuditError("freeze schema or outcome state is invalid")
    actual = sha256_file(pilot_dir / "freeze.json")
    if actual != _expected_digest(pilot_dir / "freeze.sha256", "freeze"):
        raise AuditError("freeze.json does not match freeze.sha256")
    if sha256_bytes(canonical_bytes(_manifest_core(manifest))) != manifest.get(
        "commitment_sha256"
    ):
        raise AuditError("freeze commitment does not match")
    if sha256_file(dataset_path) != manifest["dataset"]["archive_sha256"]:
        raise AuditError("dataset checksum does not match freeze")
    rebuilt = build_freeze_manifest(
        dataset_path,
        frozen_at=str(manifest["frozen_at_utc"]),
        tasksets=len(manifest["selection"]["tasksets"]),
        per_taskset=int(manifest["selection"]["per_taskset"]),
        seed=int(manifest["randomization"]["seed"]),
        warmup=int(manifest["analysis_preregistration"]["warmup"]),
        pilot_id=str(manifest["pilot_id"]),
    )
    if _semantic_core(rebuilt) != _semantic_core(manifest):
        raise AuditError("freeze does not recompute from metadata-only selection")
    return {
        "freeze_verified": True,
        "pilot_id": manifest["pilot_id"],
        "item_count": len(manifest["items"]),
        "freeze_file_sha256": actual,
        "commitment_sha256": manifest["commitment_sha256"],
        "orders": {name: order["sha256"] for name, order in manifest["orders"].items()},
    }


def _outcome_rows(dataset_path: Path, source_rows: set[int]) -> dict[int, dict[str, int]]:
    found: dict[int, dict[str, int]] = {}
    if not source_rows:
        raise AuditError("source-row set is empty")
    for source_row, row in enumerate(_rows(dataset_path, OUTCOME_COLUMNS)):
        if source_row in source_rows:
            found[source_row] = row
            if len(found) == len(source_rows):
                break
    if set(found) != source_rows:
        raise AuditError("reveal is missing one or more selected source rows")
    return found


def _order_indices(manifest: dict[str, Any], name: str) -> list[int]:
    index = {item["item_id"]: int(position) for position, item in enumerate(manifest["items"])}
    try:
        return [index[item_id] for item_id in manifest["orders"][name]["item_ids"]]
    except KeyError as exc:
        raise AuditError(f"unknown item in order {name}: {exc}") from exc


def _metrics(outcomes: list[int], order: list[int], warmup: int) -> dict[str, Any]:
    final_accuracy = sum(outcomes) / len(outcomes)
    running = 0
    absolute: list[float] = []
    squared: list[float] = []
    for index in order:
        running += outcomes[index]
        error = running / (len(absolute) + 1) - final_accuracy
        absolute.append(abs(error))
        squared.append(error * error)
    tail = absolute[warmup - 1 :]
    tail_squared = squared[warmup - 1 :]
    settling = next(
        (
            prefix
            for prefix in range(1, len(absolute) + 1)
            if all(value <= 0.01 for value in absolute[prefix - 1 :])
        ),
        len(absolute),
    )
    return {
        "integrated_absolute_prefix_error": statistics.fmean(tail),
        "integrated_squared_prefix_error": statistics.fmean(tail_squared),
        "one_percent_settling_prefix": settling,
    }


def build_result(pilot_dir: Path, dataset_path: Path, *, revealed_at: str) -> dict[str, Any]:
    freeze = verify_freeze(pilot_dir, dataset_path)
    manifest = _read_freeze(pilot_dir)
    if iso_utc(revealed_at) <= iso_utc(str(manifest["frozen_at_utc"])):
        raise AuditError("reveal timestamp must be after freeze")
    source_rows = {int(item["source_row"]) for item in manifest["items"]}
    revealed = _outcome_rows(dataset_path, source_rows)
    outcomes: list[int] = []
    revealed_items: list[dict[str, Any]] = []
    for item in manifest["items"]:
        row = revealed[int(item["source_row"])]
        metadata_pairs = (
            ("tasksetId", "taskset_id"),
            ("taskId", "task_id"),
            ("workerId", "worker_id"),
            ("completeTime", "complete_time_ms"),
            ("capability", "capability"),
        )
        if any(row[source] != item[frozen] for source, frozen in metadata_pairs):
            raise AuditError(f"metadata changed for source row {item['source_row']}")
        correct = int(row["answer"] == row["truth"])
        outcomes.append(correct)
        revealed_items.append(
            {
                "item_id": item["item_id"],
                "answer": row["answer"],
                "truth": row["truth"],
                "correct": correct,
            }
        )
    warmup = int(manifest["analysis_preregistration"]["warmup"])
    orders: dict[str, Any] = {}
    for name in ("production", "seeded_random", "quota_balanced"):
        orders[name] = {
            "metrics": _metrics(outcomes, _order_indices(manifest, name), warmup),
        }
    result: dict[str, Any] = {
        "schema": RESULT_SCHEMA,
        "pilot_id": manifest["pilot_id"],
        "outcome_state": "REVEALED",
        "revealed_at_utc": revealed_at,
        "freeze_file_sha256": freeze["freeze_file_sha256"],
        "freeze_commitment_sha256": manifest["commitment_sha256"],
        "dataset_archive_sha256": manifest["dataset"]["archive_sha256"],
        "analysis": {
            "final_accuracy": sum(outcomes) / len(outcomes),
            "correct_count": sum(outcomes),
            "item_count": len(outcomes),
            "warmup": warmup,
            "orders": orders,
            "timing_status": "recorded completion timestamps; no active labor time inferred",
        },
        "revealed_items": revealed_items,
        "claim_boundary": (
            "This is real human-annotation error evidence from a public corpus. "
            "It does not establish active-time, production, or monetary savings."
        ),
        "generator_sha256": _script_sha256(),
    }
    result["commitment_sha256"] = sha256_bytes(canonical_bytes(_result_core(result)))
    return result


def render_result(result: dict[str, Any]) -> str:
    lines = [
        "# NetEaseCrowd human-annotation audit result",
        "",
        f"Pilot: `{result['pilot_id']}`",
        f"Revealed: `{result['revealed_at_utc']}`",
        f"Selected annotations: **{result['analysis']['item_count']}**",
        f"Final observed human-label accuracy: `{result['analysis']['final_accuracy']:.6f}`",
        "",
        "| Order | Integrated absolute error | Integrated squared error | 1% settling prefix |",
        "|---|---:|---:|---:|",
    ]
    for name, data in result["analysis"]["orders"].items():
        metrics = data["metrics"]
        lines.append(
            f"| {name} | {metrics['integrated_absolute_prefix_error']:.8f} | "
            f"{metrics['integrated_squared_prefix_error']:.8f} | "
            f"{metrics['one_percent_settling_prefix']} |"
        )
    lines.extend(["", result["claim_boundary"], ""])
    return "\n".join(lines)


def write_result(pilot_dir: Path, result: dict[str, Any]) -> None:
    if (pilot_dir / "result.json").exists():
        raise AuditError("result already exists; refusing overwrite")
    atomic_json(pilot_dir / "result.json", result)
    digest = sha256_file(pilot_dir / "result.json")
    _atomic_write(pilot_dir / "result.sha256", f"{digest}  result.json\n".encode("ascii"))
    _atomic_write(pilot_dir / "RESULT.md", render_result(result).encode("utf-8"))


def verify_result(pilot_dir: Path, dataset_path: Path) -> dict[str, Any]:
    path = pilot_dir / "result.json"
    if not path.is_file():
        raise AuditError(f"missing result: {path}")
    result = _read_json(path)
    if result.get("schema") != RESULT_SCHEMA or result.get("outcome_state") != "REVEALED":
        raise AuditError("result schema or outcome state is invalid")
    actual = sha256_file(path)
    if actual != _expected_digest(pilot_dir / "result.sha256", "result"):
        raise AuditError("result.json does not match result.sha256")
    if sha256_bytes(canonical_bytes(_result_core(result))) != result.get("commitment_sha256"):
        raise AuditError("result commitment does not match")
    rebuilt = build_result(
        pilot_dir, dataset_path, revealed_at=str(result["revealed_at_utc"])
    )
    if _semantic_core(rebuilt, result=True) != _semantic_core(result, result=True):
        raise AuditError("result does not recompute from the freeze and source")
    return {
        "result_verified": True,
        "pilot_id": result["pilot_id"],
        "result_file_sha256": actual,
        "commitment_sha256": result["commitment_sha256"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    freeze = subparsers.add_parser("freeze")
    freeze.add_argument("--dataset", type=Path, required=True)
    freeze.add_argument("--pilot-dir", type=Path, required=True)
    freeze.add_argument("--frozen-at", default=_utc_now())
    freeze.add_argument("--tasksets", type=int, default=DEFAULT_TASKSETS)
    freeze.add_argument("--per-taskset", type=int, default=DEFAULT_PER_TASKSET)
    freeze.add_argument("--seed", type=int, default=DEFAULT_SEED)
    freeze.add_argument("--warmup", type=int, default=DEFAULT_WARMUP)
    for name in ("verify", "reveal"):
        command = subparsers.add_parser(name)
        command.add_argument("--dataset", type=Path, required=True)
        command.add_argument("--pilot-dir", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        if arguments.command == "freeze":
            manifest = build_freeze_manifest(
                arguments.dataset,
                frozen_at=arguments.frozen_at,
                tasksets=arguments.tasksets,
                per_taskset=arguments.per_taskset,
                seed=arguments.seed,
                warmup=arguments.warmup,
            )
            write_freeze(arguments.pilot_dir, manifest)
            print(json.dumps({"freeze_written": True, "pilot_id": manifest["pilot_id"]}))
        elif arguments.command == "verify":
            print(json.dumps(verify_freeze(arguments.pilot_dir, arguments.dataset), indent=2))
        else:
            result = build_result(arguments.pilot_dir, arguments.dataset, revealed_at=_utc_now())
            write_result(arguments.pilot_dir, result)
            print(json.dumps({"result_written": True, "pilot_id": result["pilot_id"]}))
    except (AuditError, OSError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
