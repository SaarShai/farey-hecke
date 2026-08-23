#!/usr/bin/env python3
"""Merge leaf-shard receipts into one lane_f checkpoint, refusing anything short.

Verification performed here, all of it fail-closed:

1. Every shard re-hashes: ``payload_sha256`` must equal the sha256 of the
   canonical payload encoding.  A hand-edited receipt is refused.  A *partial*
   shard (a kernel that hit its deadline) is accepted and noted -- its leaves
   are real leaves, and rule 3 below is what actually decides whether the cover
   is complete.
2. Every shard's ``params`` must agree on ``checker_sha256``,
   ``source_sha256``, ``receipt_sha256``, ``implementation``, ``N``, ``K``,
   ``max_depth`` and ``precision_bits``.  Shards from two different checker
   builds cannot be merged.
3. Coverage: the union of leaves must be exactly ``{0..2**D-1}`` for each of the
   ``4*K`` arcs, each leaf appearing exactly once.  Missing, duplicated or
   out-of-range leaves are refused.
4. Per-leaf gate: an arc certifies only if EVERY one of its leaves has
   ``qOp_lt_1 == True`` and ``status == "PASS"``.  One ``OPEN_MAX_DEPTH`` leaf
   opens the whole arc, and one open arc opens the contour.
5. The merged record set is then handed to the checker's OWN
   ``validate_checkpoint_records``, which independently re-derives the exact
   partition property from the recorded paths.

Output is a ``q8-schur-contour-checkpoint/v3`` file.  Feeding it back to the
unmodified checker::

    python q8_schur_contour.py --N 262 --K 1 --max-depth 7 \
        --arc-start 0 --arc-end 4 --resume MERGED.json --out VERDICT.json

re-derives the verdict INCLUDING the winding number.  Note honestly: the
checker's ``recompute_saved_pass_records`` recomputes every PASS leaf from
scratch, so that audit run costs the full campaign again single-threaded.  It is
the cold-audit path, not the harvest path; the harvest claim is this merge's own
report.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from q8_leaf_shard import SHARD_SCHEMA, import_checker, payload_hash  # noqa: E402

BOUND_KEYS = (
    "schema",
    "implementation",
    "checker_sha256",
    "N",
    "K",
    "max_depth",
    "precision_bits",
    "pin",
    "sign",
    "n_head",
    "factor_strings",
    "receipt_sha256",
    "source_sha256",
)


def load_shard(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    payload = document.get("payload")
    if not isinstance(payload, dict) or payload.get("schema") != SHARD_SCHEMA:
        raise SystemExit(f"{path}: not a {SHARD_SCHEMA} receipt")
    recomputed = payload_hash(payload)
    if document.get("payload_sha256") != recomputed:
        raise SystemExit(
            f"{path}: payload hash mismatch\n"
            f"  recorded   {document.get('payload_sha256')}\n"
            f"  recomputed {recomputed}"
        )
    if not payload.get("leaves_complete"):
        # A kernel that hit its deadline writes a partial receipt.  Its leaves
        # are still certified leaves; what must not be relaxed is the coverage
        # check below, which is the real gate.  Accept the leaves it did
        # produce, and let the union either cover 0..511 exactly or not.
        print(
            f"NOTE {path}: partial shard, "
            f"{len(payload.get('records', []))} of "
            f"{payload['leaf_end'] - payload['leaf_start']} leaves; "
            "coverage must be completed by another shard",
            file=sys.stderr,
        )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("shards", nargs="+", type=Path)
    parser.add_argument(
        "--lane-f",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "lane_f",
    )
    parser.add_argument("--out", type=Path, required=True, help="merged v3 checkpoint")
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    checker = import_checker(args.lane_f)
    payloads = [load_shard(path) for path in args.shards]
    if not payloads:
        raise SystemExit("no shards")

    reference = payloads[0]["params"]
    for path, payload in zip(args.shards, payloads):
        for key in BOUND_KEYS:
            if payload["params"].get(key) != reference.get(key):
                raise SystemExit(
                    f"{path}: shard parameter {key!r} disagrees with {args.shards[0]}"
                )
        if payload["depth"] != reference["max_depth"]:
            raise SystemExit(f"{path}: shard depth != params max_depth")

    depth = int(reference["max_depth"])
    N = int(reference["N"])
    K = int(reference["K"])
    arc_count = 4 * K
    leaves_per_arc = 1 << depth

    seen: dict[tuple[int, int], Path] = {}
    records: list[dict[str, Any]] = []
    for path, payload in zip(args.shards, payloads):
        arc = int(payload["arc"])
        if not (0 <= arc < arc_count):
            raise SystemExit(f"{path}: arc {arc} outside 0..{arc_count - 1}")
        for record in payload["records"]:
            if int(record["initial_arc"]) != arc:
                raise SystemExit(f"{path}: record initial_arc != shard arc")
            if len(record["path"]) != depth:
                raise SystemExit(f"{path}: record is not at uniform depth {depth}")
            leaf = 0
            for bit in record["path"]:
                leaf = 2 * leaf + bit
            key = (arc, leaf)
            if key in seen:
                raise SystemExit(f"{path}: leaf {key} already supplied by {seen[key]}")
            seen[key] = path
            records.append(record)

    missing = [
        (arc, leaf)
        for arc in range(arc_count)
        for leaf in range(leaves_per_arc)
        if (arc, leaf) not in seen
    ]
    coverage_complete = not missing
    expected = arc_count * leaves_per_arc

    per_arc: dict[int, dict[str, Any]] = {}
    for arc in range(arc_count):
        arc_records = [r for r in records if int(r["initial_arc"]) == arc]
        per_arc[arc] = {
            "leaves": len(arc_records),
            "pass": sum(1 for r in arc_records if r.get("status") == "PASS"),
            "open": sum(1 for r in arc_records if r.get("status") != "PASS"),
            "qOp_lt_1_all": bool(arc_records)
            and all(bool(r.get("qOp_lt_1")) for r in arc_records),
            "certified": (
                len(arc_records) == leaves_per_arc
                and all(r.get("status") == "PASS" for r in arc_records)
                and all(bool(r.get("qOp_lt_1")) for r in arc_records)
            ),
        }

    all_arcs_certified = coverage_complete and all(
        info["certified"] for info in per_arc.values()
    )

    report = {
        "schema": "q8-schur-contour-shard-merge/v1",
        "shards": [str(path) for path in args.shards],
        "shard_payload_sha256": {
            str(path): payload_hash(payload)
            for path, payload in zip(args.shards, payloads)
        },
        "N": N,
        "K": K,
        "depth": depth,
        "leaves_expected": expected,
        "leaves_supplied": len(seen),
        "coverage_exact": coverage_complete,
        "missing_leaves": missing[:32],
        "missing_leaf_count": len(missing),
        "per_arc": per_arc,
        "all_arcs_certified": all_arcs_certified,
        "checker_sha256": reference["checker_sha256"],
        "means": (
            "every depth-%d leaf of every arc satisfies qOp < 1 and all strict "
            "gates; the finite-section arc cover is complete" % depth
            if all_arcs_certified
            else "the arc cover is NOT complete; the contour verdict stays OPEN"
        ),
        "does_not_mean": (
            "This is checker output, not a theorem.  E1, the q=8 MMS/Hilbert "
            "identification, K_s, analytic gates 5-6 and continuation condition "
            "8 of the 12-item ledger are untouched and remain OPEN."
        ),
    }

    params = checker.checkpoint_parameters(N, K, depth, 0, arc_count)
    for key in BOUND_KEYS:
        if params.get(key) != reference.get(key):
            raise SystemExit(
                f"local checker parameter {key!r} disagrees with the shards; "
                "the merging host does not hold the bytes the shards were run against"
            )

    if coverage_complete:
        completed = set(range(arc_count))
        # The checker's own partition validator, not ours.
        checker.validate_checkpoint_records(params, completed, records)
        checker.write_checkpoint(args.out, params, sorted(completed), records)
        report["merged_checkpoint"] = str(args.out)
        report["merged_checkpoint_validated_by_checker"] = True
    else:
        report["merged_checkpoint"] = None
        report["merged_checkpoint_validated_by_checker"] = False

    text = json.dumps(report, indent=2) + "\n"
    if args.report is not None:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    print(text)
    return 0 if all_arcs_certified else 2


if __name__ == "__main__":
    raise SystemExit(main())
