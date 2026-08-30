#!/usr/bin/env python3
"""Leaf-sharded driver for the q=8 Schur contour subdivision campaign.

The lane_f checker ``q8_schur_contour.py`` is imported UNMODIFIED.  This driver
adds no mathematics: it reconstructs one uniform-depth adaptive leaf with the
checker's own ``segment_from_initial_path`` and certifies it with the checker's
own ``arc_certificate``.  Every gate, every bound, every hash check stays inside
lane_f.

Why a driver at all: the checker's CLI shards only by initial arc
(``--arc-start/--arc-end``), and with ``K = 1`` there are exactly four arcs.  At
the pinned arc ``qOp = 83.79 >= 1`` at depth 0 and halves per bisection, so
depth 7 is required -- 128 leaves per arc, 512 leaves in total, ~1290 s each at
``N = 262``.  That is ~1.8e2 CPU-hours and must be spread over many machines.
Sharding by ``(arc, leaf_range)`` is the finest split the checker's own leaf
addressing supports.

Determinism / receipts
----------------------
* The hashed payload contains no wall-clock value and no host detail.  Timing
  is reported in a sibling ``timing`` object that is NOT hashed.
* Every Arb/Acb quantity is emitted as a string by the checker's own
  ``arb_text``/``acb_text`` (80 digits, ``more=True``).
* ``payload_sha256`` = sha256 of ``json.dumps(payload, sort_keys=True,
  separators=(",", ":"))`` -- recomputable by any verifier.
* ``params`` is the checker's own ``checkpoint_parameters(...)`` dict, so the
  shard is bound to the exact checker bytes, source bytes and receipt bytes.
  A shard produced by a different checker cannot be merged.

Uniform depth, not adaptive
---------------------------
``certify_adaptive`` stops early when a parent segment passes.  This driver
always evaluates at the full target depth.  That is strictly more work and
strictly finer; a uniform depth-``D`` family of leaves is an exact partition of
its arc, which is exactly what the checker's ``validate_checkpoint_records``
requires.  It also makes the shard map static, so a dead kernel can be re-run
without re-planning.

Leaf addressing: leaf index ``i`` in ``[0, 2**D)`` maps to the big-endian bit
path ``[b_{D-1}, ..., b_0]``, i.e. the same left-to-right order the checker's
``split_segment`` produces.  Leaf ``i`` is the ``i``-th sub-segment of the arc
in path order.

Usage
-----
    python q8_leaf_shard.py --arc 0 --leaf-start 0 --leaf-end 64 \
        --depth 7 --N 262 --workers 4 \
        --out SHARD_a0_l0-64.json --checkpoint SHARD_a0_l0-64.ckpt.json

Exit codes: 0 = shard complete (all requested leaves certified, whatever their
status), 3 = shard incomplete (deadline hit; partial receipt written).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any

SHARD_SCHEMA = "q8-schur-contour-leaf-shard/v1"

# --- checker import (unmodified) -------------------------------------------

_CHECKER: Any = None
_SEGMENTS: Any = None
_BOUNDS: Any = None
_N: int = 0


def import_checker(lane_f: Path):
    """Import the lane_f checker unmodified from an explicit lane_f directory."""

    lane_f = lane_f.resolve()
    if str(lane_f) not in sys.path:
        sys.path.insert(0, str(lane_f))
    import q8_schur_contour as checker  # noqa: E402

    resolved = Path(checker.__file__).resolve()
    if resolved.parent != lane_f:
        raise SystemExit(
            f"imported checker from {resolved}, expected inside {lane_f}; "
            "a stale q8_schur_contour.py is shadowing the packaged one"
        )
    return checker


def leaf_path(leaf: int, depth: int) -> list[int]:
    """Big-endian bit path of a uniform-depth leaf index."""

    if not (0 <= leaf < (1 << depth)):
        raise ValueError(f"leaf {leaf} out of range for depth {depth}")
    return [(leaf >> (depth - 1 - k)) & 1 for k in range(depth)]


# --- worker ----------------------------------------------------------------


def _worker_init(lane_f_str: str, paths: dict[str, str], N: int, K: int) -> None:
    global _CHECKER, _SEGMENTS, _BOUNDS, _N
    checker = import_checker(Path(lane_f_str))
    checker.ctx.prec = checker.PRECISION_BITS
    _CHECKER = checker
    _N = N
    _BOUNDS = checker.load_operator_bounds(
        Path(paths["r2"]),
        Path(paths["tb"]),
        Path(paths["w"]),
        N,
        Path(paths["lout"]),
    )
    segments = checker.helper.closed_boundary_segments(
        checker.arb(checker.PIN_RE),
        checker.arb(checker.PIN_IM),
        checker.arb(checker.HALF_WIDTH),
        checker.arb(checker.HALF_WIDTH),
        K,
    )
    for segment in segments:
        segment["initial_arc"] = segment["arc_index"]
        segment["path"] = []
    _SEGMENTS = segments


def _certify_leaf(job: tuple[int, int, int]) -> dict[str, Any]:
    arc, leaf, depth = job
    checker = _CHECKER
    started = time.perf_counter()
    path = leaf_path(leaf, depth)
    segment = checker.segment_from_initial_path(_SEGMENTS, arc, path)
    record, _box = checker.arc_certificate(_N, segment, _BOUNDS)
    record["subdivision_depth"] = depth
    if record.get("status") != "PASS":
        # Terminal at the target depth: the checker's own certify_adaptive
        # relabels a non-PASS leaf at max depth exactly this way, and
        # validate_checkpoint_records accepts only PASS / OPEN_MAX_DEPTH.
        record["status"] = "OPEN_MAX_DEPTH"
    return {"leaf": leaf, "record": record, "seconds": time.perf_counter() - started}


# --- receipt ---------------------------------------------------------------


def canonical(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def payload_hash(payload: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest()


def build_payload(
    checker: Any,
    params: dict[str, Any],
    arc: int,
    depth: int,
    leaf_start: int,
    leaf_end: int,
    done: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    leaves = sorted(done)
    records = [done[leaf] for leaf in leaves]
    qop_lt_1 = [
        bool(record.get("qOp_lt_1")) for record in records
    ]
    return {
        "schema": SHARD_SCHEMA,
        "implementation": checker.CERTIFICATE_IMPLEMENTATION,
        "checkpoint_schema": checker.CHECKPOINT_SCHEMA,
        "params": params,
        "arc": arc,
        "depth": depth,
        "leaf_start": leaf_start,
        "leaf_end": leaf_end,
        "leaves_certified": leaves,
        "leaves_complete": leaves == list(range(leaf_start, leaf_end)),
        "status_counts": {
            status: sum(1 for record in records if record.get("status") == status)
            for status in ("PASS", "OPEN_MAX_DEPTH")
        },
        "qOp_lt_1_all": all(qop_lt_1) if qop_lt_1 else False,
        "records": records,
    }


def write_receipt(path: Path, payload: dict[str, Any], timing: dict[str, Any]) -> None:
    document = {
        "payload": payload,
        "payload_sha256": payload_hash(payload),
        "timing": timing,  # NOT hashed
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_checkpoint(path: Path, params: dict[str, Any]) -> dict[int, dict[str, Any]]:
    """Resume already-certified leaves, refusing any foreign-parameter file."""

    if not path.exists():
        return {}
    document = json.loads(path.read_text(encoding="utf-8"))
    payload = document.get("payload", {})
    if payload.get("schema") != SHARD_SCHEMA:
        raise SystemExit(f"{path}: not a leaf-shard checkpoint")
    if payload.get("params") != params:
        raise SystemExit(f"{path}: checkpoint parameters do not match this run")
    if document.get("payload_sha256") != payload_hash(payload):
        raise SystemExit(f"{path}: checkpoint payload hash mismatch")
    done: dict[int, dict[str, Any]] = {}
    for record in payload.get("records", []):
        leaf = 0
        for bit in record["path"]:
            leaf = 2 * leaf + bit
        done[leaf] = record
    return done


# --- main ------------------------------------------------------------------


def main() -> int:
    default_lane_f = (
        Path(__file__).resolve().parents[2] / "lane_f"
    )
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane-f", type=Path, default=default_lane_f)
    parser.add_argument("--arc", type=int, required=True)
    parser.add_argument("--leaf-start", type=int, required=True)
    parser.add_argument("--leaf-end", type=int, required=True)
    parser.add_argument("--depth", type=int, default=7)
    parser.add_argument("--N", type=int, default=None, help="default: checker DEFAULT_N")
    parser.add_argument("--K", type=int, default=None, help="default: checker DEFAULT_K")
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 1)))
    parser.add_argument("--r2", type=Path, default=None)
    parser.add_argument("--tb", type=Path, default=None)
    parser.add_argument("--w", type=Path, default=None)
    parser.add_argument("--lout", type=Path, default=None)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--checkpoint", type=Path, default=None)
    parser.add_argument(
        "--deadline-seconds",
        type=float,
        default=None,
        help="stop dispatching new leaves after this wall time; write a partial receipt",
    )
    args = parser.parse_args()

    checker = import_checker(args.lane_f)
    checker.ctx.prec = checker.PRECISION_BITS
    N = checker.DEFAULT_N if args.N is None else args.N
    K = checker.DEFAULT_K if args.K is None else args.K
    lane_f = args.lane_f.resolve()
    paths = {
        "r2": str(args.r2 or checker.DEFAULT_R2),
        "tb": str(args.tb or checker.DEFAULT_TB),
        "w": str(args.w or checker.DEFAULT_W),
        "lout": str(args.lout or checker.DEFAULT_LOUT),
    }

    if args.depth < 0:
        raise SystemExit("depth >= 0 required")
    total = 1 << args.depth
    if not (0 <= args.leaf_start < args.leaf_end <= total):
        raise SystemExit(f"leaf range must satisfy 0 <= start < end <= {total}")
    if not (0 <= args.arc < 4 * K):
        raise SystemExit(f"arc must satisfy 0 <= arc < {4 * K}")

    # The shard is bound to the exact checker/source/receipt bytes through the
    # checker's own parameter block.  arc_start/arc_end are the single-arc
    # window this shard belongs to, so a merged checkpoint can be re-derived.
    params = checker.checkpoint_parameters(N, K, args.depth, args.arc, args.arc + 1)

    done = load_checkpoint(args.checkpoint, params) if args.checkpoint else {}
    pending = [
        leaf for leaf in range(args.leaf_start, args.leaf_end) if leaf not in done
    ]
    print(
        f"Q8_SHARD arc={args.arc} leaves=[{args.leaf_start},{args.leaf_end}) "
        f"depth={args.depth} N={N} workers={args.workers} "
        f"resumed={len(done)} pending={len(pending)}",
        flush=True,
    )

    started = time.time()
    per_leaf: list[float] = []
    interrupted = False
    if pending:
        jobs = [(args.arc, leaf, args.depth) for leaf in pending]
        context = mp.get_context("spawn")
        with context.Pool(
            processes=max(1, args.workers),
            initializer=_worker_init,
            initargs=(str(lane_f), paths, N, K),
        ) as pool:
            for result in pool.imap_unordered(_certify_leaf, jobs):
                done[result["leaf"]] = result["record"]
                per_leaf.append(result["seconds"])
                elapsed = time.time() - started
                print(
                    f"Q8_SHARD leaf={result['leaf']} "
                    f"status={result['record']['status']} "
                    f"qOp={result['record']['qOp_upper'][:24]} "
                    f"leaf_seconds={result['seconds']:.1f} elapsed={elapsed:.1f} "
                    f"done={len(done)}/{args.leaf_end - args.leaf_start}",
                    flush=True,
                )
                if args.checkpoint is not None:
                    write_receipt(
                        args.checkpoint,
                        build_payload(
                            checker, params, args.arc, args.depth,
                            args.leaf_start, args.leaf_end, done,
                        ),
                        {"elapsed_seconds": elapsed, "partial": True},
                    )
                if args.deadline_seconds is not None and elapsed > args.deadline_seconds:
                    print("Q8_SHARD deadline reached; terminating pool", flush=True)
                    interrupted = True
                    pool.terminate()
                    break

    payload = build_payload(
        checker, params, args.arc, args.depth, args.leaf_start, args.leaf_end, done
    )
    timing = {
        "wall_seconds": time.time() - started,
        "leaf_seconds_mean": (sum(per_leaf) / len(per_leaf)) if per_leaf else None,
        "leaf_seconds_max": max(per_leaf) if per_leaf else None,
        "workers": args.workers,
        "host_platform": platform.platform(),
        "python": platform.python_version(),
        "deadline_interrupted": interrupted,
    }
    write_receipt(args.out, payload, timing)
    print(
        json.dumps(
            {
                "arc": args.arc,
                "leaf_range": [args.leaf_start, args.leaf_end],
                "leaves_complete": payload["leaves_complete"],
                "status_counts": payload["status_counts"],
                "qOp_lt_1_all": payload["qOp_lt_1_all"],
                "payload_sha256": payload_hash(payload),
                "wall_seconds": timing["wall_seconds"],
            },
            indent=2,
        ),
        flush=True,
    )
    return 0 if payload["leaves_complete"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
