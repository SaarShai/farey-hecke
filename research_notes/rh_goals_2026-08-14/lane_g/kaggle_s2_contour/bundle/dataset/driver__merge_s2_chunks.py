#!/usr/bin/env python3
"""Merge the 16 S2 N=288 chunk receipts and certify the closed-contour winding.

Runs LOCALLY after harvest.  Loads every S2_CHUNK_a*.json orchestrator receipt
from --chunk-dir, extracts ``closed_contour["288"]``, verifies chunk-level
consistency (same N, same F_R, contiguous arc ranges, chunk_gate_pass), then
runs the B3 seam-aware merge + adjacent-box overlap-polygon winding check
(``certify_r3b_flagship.merge_chunks_and_verify_closure`` — accepts subdivided
chunks, verifies dyadic leaf tiling per base arc).

Writes S2_MERGED_CONTOUR_RECEIPT.json beside the chunks.  UNREFEREED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE_G = HERE.parent
SP_CODE = LANE_G.parents[2] / ".worktrees" / "aletheia-restore" / "code" / "second_pin"
sys.path.insert(0, str(SP_CODE))

from flint import arb, ctx  # noqa: E402

import certify_r3b_flagship as orch  # noqa: E402

N_PRIMARY = 288
EXPECTED_BASE_ARCS = 192
EXPECTED_CHUNKS = 16


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-dir", type=Path, default=HERE / "chunk_receipts")
    parser.add_argument(
        "--out", type=Path, default=HERE / "chunk_receipts" / "S2_MERGED_CONTOUR_RECEIPT.json"
    )
    args = parser.parse_args()
    ctx.prec = orch.PRECISION_BITS_DEFAULT
    t0 = time.time()

    paths = sorted(args.chunk_dir.glob("S2_CHUNK_a*.json"))
    paths = [p for p in paths if not p.name.endswith(".ckpt.json")]
    if len(paths) != EXPECTED_CHUNKS:
        raise SystemExit(
            f"expected {EXPECTED_CHUNKS} chunk receipts, found {len(paths)} in {args.chunk_dir}"
        )
    chunk_states = []
    chunk_meta = []
    f_values = set()
    for path in paths:
        state = json.loads(path.read_text())
        attempt = state.get("closed_contour", {}).get(str(N_PRIMARY))
        if attempt is None:
            raise SystemExit(f"{path.name}: no closed_contour[{N_PRIMARY}] block")
        if attempt.get("chunk_arc_range") is None:
            raise SystemExit(f"{path.name}: not a chunk receipt (arc_range is None)")
        if not state.get("immutable_hashes_verified"):
            raise SystemExit(f"{path.name}: immutable hashes not verified in-kernel")
        f_text = state.get("endpoint_trace_bounds", {}).get(str(N_PRIMARY), {}).get(
            "F_R_upper_bound"
        )
        if f_text is None:
            raise SystemExit(f"{path.name}: no F_R at N={N_PRIMARY}")
        f_values.add(f_text)
        chunk_states.append(attempt)
        chunk_meta.append(
            {
                "file": path.name,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "chunk_arc_range": attempt["chunk_arc_range"],
                "status": attempt.get("status"),
                "chunk_gate_pass": attempt.get("chunk_gate_pass"),
                "accepted_leaves": attempt.get("accepted_closed_subarc_count"),
                "subdivisions": attempt.get("adaptive_subdivision_count"),
                "min_margin": attempt.get("minimum_finite_lower_minus_F_margin"),
                "F_R_upper_bound": f_text,
            }
        )
    if len(f_values) != 1:
        raise SystemExit(
            f"chunks disagree on F_R({N_PRIMARY}) — {len(f_values)} distinct values; "
            "refusing to merge across inconsistent endpoint bounds"
        )

    winding, info = orch.merge_chunks_and_verify_closure(chunk_states, EXPECTED_BASE_ARCS)
    all_margins = [
        arb(meta["min_margin"]) for meta in chunk_meta if meta["min_margin"] is not None
    ]
    result = {
        "schema": "s2-merged-contour/v1",
        "status": "UNREFEREED",
        "N": N_PRIMARY,
        "expected_base_closed_arc_count": EXPECTED_BASE_ARCS,
        "chunks": chunk_meta,
        "F_R_upper_bound": next(iter(f_values)),
        "merged_winding": winding,
        "winding_info": info,
        "minimum_finite_lower_minus_F_margin": (
            orch.arb_text(orch.min_arb(all_margins)) if all_margins else None
        ),
        "closed_contour_gate_pass": bool(winding is not None and winding >= 1),
        "note": (
            "winding >= 1 with every chunk CHUNK_ARCS_CLEAR certifies at least "
            "one zero of the finite/Fredholm determinant inside the S2 box "
            "(same straight-line homotopy argument as the flagship). The "
            "N=128 control arm and the assembly doc are separate steps."
        ),
        "wall_seconds": time.time() - t0,
    }
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "merged_winding": winding,
        "gate_pass": result["closed_contour_gate_pass"],
        "reason": info.get("reason"),
        "out": str(args.out),
    }, indent=2))
    return 0 if result["closed_contour_gate_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
