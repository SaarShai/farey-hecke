#!/usr/bin/env python3
"""Interval-parameter probe for the fixed q=8 MMS-(32) block model.

This is intentionally a slab diagnostic.  It does not assert that the q=8
model represents any other integer q; the block dimension changes with q.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from flint import arb, ctx

LANE_F = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE_F))

import f8_certify_tb_blocks as f8  # noqa: E402
import q8_tb_support as tb  # noqa: E402


FACTORS = ("10", "4", "2")
DEFAULT_SLABS = [("1.8477590650225735", "1.848"), ("1.848", "1.850")]
OUT_DEFAULT = LANE_F / "f8_receipts" / "Q8_LAMBDA_SLAB_PROBE_RECEIPT.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slab", nargs=2, action="append", metavar=("LO", "HI"))
    parser.add_argument("--M", type=int, default=512)
    parser.add_argument("--K-start", type=int, default=12)
    parser.add_argument("--K-max", type=int, default=128)
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = parser.parse_args()
    slabs = args.slab or DEFAULT_SLABS
    ctx.prec = 384
    started = time.perf_counter()
    results = []
    for lo_text, hi_text in slabs:
        lo, hi = arb(lo_text), arb(hi_text)
        lam = arb((lo.lower() + hi.upper()) / arb(2), (hi.upper() - lo.lower()) / arb(2))
        points = f8.partition_points_ball(lam)
        half = [(points[k] - points[k - 1]) / arb(2) for k in range(1, f8.KAPPA + 1)]
        centers = [(points[k] + points[k - 1]) / arb(2) for k in range(1, f8.KAPPA + 1)]
        radii = [arb(FACTORS[k]) * half[k] for k in range(f8.KAPPA)]
        rows = []
        for block in f8.BLOCKS:
            try:
                row, _, _ = tb.certify_block(block, centers, radii, lam, args.M, args.K_start, args.K_max)
                rows.append({"block": list(block), "label": row["label"], "ratio_upper_bound": row["ratio_upper_bound"], "pass": row["pass"]})
            except Exception as error:
                rows.append({"block": list(block), "label": tb.label_for(block), "error": f"{type(error).__name__}: {error}", "pass": False})
        rho = max((arb(row.get("ratio_upper_bound", "1e100")) for row in rows), key=lambda x: x.upper())
        result = {"lambda_interval": [lo_text, hi_text], "lambda_ball": lam.str(80, more=True), "factors": list(FACTORS), "M": args.M, "K_start": args.K_start, "K_max": args.K_max, "rows": rows, "rho_upper_bound": rho.str(80, more=True), "all_block_pass": all(row["pass"] for row in rows)}
        results.append(result)
        print(f"Q8_LAMBDA_SLAB {lo_text}..{hi_text} rho={result['rho_upper_bound']} all_block_pass={result['all_block_pass']}", flush=True)
    receipt = {"schema": "q8-fixed-model-lambda-slab-probe/v1", "status": "DIAGNOSTIC_ONLY", "q": 8, "mms_equation": "(32)", "results": results, "scope": "OPEN: this fixed q=8 model is not a q-generic certificate; E1, contour, R2/R3, Ks and factorization remain open", "runtime_seconds": time.perf_counter() - started}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": str(args.out.resolve()), "results": [{"lambda_interval": r["lambda_interval"], "rho_upper_bound": r["rho_upper_bound"], "all_block_pass": r["all_block_pass"]} for r in results]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
