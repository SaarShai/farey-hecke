#!/usr/bin/env python3
"""q=8 enlarged-disc E1 geometry probe from tracked Arb routines."""

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
OUT_DEFAULT = LANE_F / "f8_receipts" / "Q8_E1_ENLARGED_PROBE_RECEIPT.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--M", type=int, default=512)
    parser.add_argument("--K-start", type=int, default=12)
    parser.add_argument("--K-max", type=int, default=64)
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = parser.parse_args()
    ctx.prec = 384
    started = time.perf_counter()
    lam = f8.lam_ball()
    points, centers, half, multipliers, base_radii = f8.disc_geometry_for(lam, FACTORS)
    pole_rows, cut_rows = tb.clearance_rows(f8.BLOCKS, centers, base_radii, lam)
    source_clearances = []
    for source in range(1, f8.KAPPA + 1):
        margins = [arb(row["margin"]) for row in pole_rows + cut_rows if row["block"][0] == source]
        source_clearances.append(min(margins, key=lambda value: value.lower()).lower())
    enlargements = []
    for index, radius in enumerate(base_radii):
        enlargements.append(min(source_clearances[index] / arb(4), arb("0.15") * radius.lower()))
    enlarged_radii = [base_radii[i] + enlargements[i] for i in range(f8.KAPPA)]
    # E1 only needs the strict contraction target rho_hat<1; the base TB
    # support's stronger .70 internal threshold would reject legitimate E1
    # enlargements, so this probe uses .99.
    tb.THRESHOLD = arb("0.99")
    tb.THRESHOLD_TEXT = "0.99"
    rows = []
    for block in f8.BLOCKS:
        try:
            row, _, _ = tb.certify_block(block, centers, enlarged_radii, lam, args.M, args.K_start, args.K_max)
            rows.append({"block": list(block), "label": row["label"], "ratio_upper_bound": row["ratio_upper_bound"], "pass": row["pass"]})
        except Exception as error:
            rows.append({"block": list(block), "label": tb.label_for(block), "error": f"{type(error).__name__}: {error}", "pass": False})
    rho = max((arb(row.get("ratio_upper_bound", "1e100")) for row in rows), key=lambda value: value.upper())
    receipt = {"schema": "q8-e1-enlarged-probe/v1", "status": "DIAGNOSTIC_ONLY", "q": 8, "M": args.M, "K_start": args.K_start, "K_max": args.K_max, "lambda": lam.str(80, more=True), "base_radii": [x.str(80, more=True) for x in base_radii], "source_clearance_lower": [x.str(80, more=True) for x in source_clearances], "enlargement_lower": [x.str(80, more=True) for x in enlargements], "enlarged_radii": [x.str(80, more=True) for x in enlarged_radii], "rows": rows, "rho_hat_upper_bound": rho.str(80, more=True), "rho_hat_less_than_one": rho.upper() < arb(1).lower(), "scope": "OPEN: full E1 weight holomorphy, contour, R2/R3, Ks and MMS linkage remain open", "runtime_seconds": time.perf_counter() - started}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rho_hat_upper_bound": receipt["rho_hat_upper_bound"], "rho_hat_less_than_one": receipt["rho_hat_less_than_one"], "enlargement_lower": receipt["enlargement_lower"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
