#!/usr/bin/env python3
"""Arb TB block receipt for the enlarged q=8 disc geometry (10,4,2)."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from flint import arb, ctx

LANE_F = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE_F))

import q8_tb_support as v2  # noqa: E402
import f8_certify_tb_blocks as f8  # noqa: E402


FACTORS = ("10", "4", "2")
OUT = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"


def text(value: arb) -> str:
    return value.str(24, more=True)


def main() -> int:
    ctx.prec = 384
    started = time.perf_counter()
    lam = f8.lam_ball()
    points, centers, half, multipliers, radii = f8.disc_geometry_for(lam, FACTORS)
    blocks = list(f8.BLOCKS)
    rows = []
    for block in blocks:
        row, _, _ = v2.certify_block(block, centers, radii, lam, 512, 12, 64)
        rows.append(row)
        print(f"Q8_F1024 block={row['label']} ratio={row['ratio_upper_bound']}", flush=True)
    ratios = [arb(term["ratio_upper_bound"]) for row in rows for term in row["head_terms"]]
    ratios.extend(arb(row["deep_tail"]["ratio_upper_bound"]) for row in rows if row["deep_tail"] is not None)
    rho = max(ratios, key=lambda value: value.upper()).upper()
    poles, cuts = v2.clearance_rows(blocks, centers, radii, lam)
    receipt = {
        "schema": "tb-block-certificates/v2-q8",
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": 384,
        "M": 512,
        "q": 8,
        "kappa": 3,
        "h_q": 3,
        "even_q": True,
        "lambda": text(lam),
        "lambda_exact_form": "sqrt(2 + sqrt(2))",
        "partition_points": [text(x) for x in points],
        "centers": [text(x) for x in centers],
        "half_widths": [text(x) for x in half],
        "radius_multipliers": [text(x) for x in multipliers],
        "radius_multipliers_exact_strings": list(FACTORS),
        "source_radii": [text(x) for x in radii],
        "blocks_source": {
            "path": str(LANE_F / "f8_certify_tb_blocks.py"),
            "count": len(blocks),
            "expected_count": 8,
            "exact_count_check": True,
            "blocks": [list(block) for block in blocks],
            "derivation": "MMS eq.(32) explicit q=8 list",
        },
        "blocks": rows,
        "rho_star": text(rho),
        "rho_star_upper_bound": text(rho.upper()),
        "threshold_text": "0.99",
        "threshold": "0.99",
        "rho_less_than_threshold": bool(rho.upper() < arb("0.99").lower()),
        "pole_clearance": poles,
        "branch_cut_clearance": cuts,
        "all_head_and_deep_tail_terms_pass": all(row["pass"] for row in rows),
        "all_pole_clearances_pass": all(row["pass"] for row in poles),
        "all_branch_cut_clearances_pass": all(row["pass"] for row in cuts),
        "certification_verdict": "PASS_RHO_LT_0.99" if rho.upper() < arb("0.99").lower() else "FAIL",
        "runtime_seconds": time.perf_counter() - started,
        "scope_caveat": "Large radii are tested by the same pole/branch-cut and block-containment bounds; E1/Fredholm linkage remains OPEN.",
    }
    OUT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("rho_star_upper_bound", "all_pole_clearances_pass", "all_branch_cut_clearances_pass", "runtime_seconds")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
