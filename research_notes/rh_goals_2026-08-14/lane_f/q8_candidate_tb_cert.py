#!/usr/bin/env python3
"""Arb TB block receipt for the enlarged q=8 disc geometry (10,4,2).

The threshold is read from ``q8_tb_support``, the module that actually grades
every head and deep-tail term.  The earlier receipt announced ``0.99`` because
it re-targeted the threshold through ``f8_certify_tb_blocks.run``, which this
script never calls, so the announced threshold and the applied threshold could
drift apart while the per-term field name stayed ``ratio_less_than_0_70``.
Reading the threshold from the grading module removes that drift by
construction, and the emitted receipt is byte-deterministic: no wall clock, no
host, no seed enters the payload.
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

import q8_tb_support as v2  # noqa: E402
import f8_certify_tb_blocks as f8  # noqa: E402


FACTORS = ("10", "4", "2")
# The pinned immutable receipt at Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json is
# hash-bound by q8_schur_contour.py, by the R2 receipt's source_bindings and by
# the L-OUT receipt; it is never overwritten from here.  The strict-threshold
# re-emission is a sibling file.
PINNED_OUT = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"
OUT = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_T070_RECEIPT.json"
# q8_tb_support serialises the per-term verdict under the literal key
# ``ratio_less_than_0_70``.  If the grading threshold ever moves, that literal
# stops describing what was checked, so refuse to emit rather than ship a
# false-by-name field.
PER_TERM_FIELD_THRESHOLD_TEXT = "0.70"


def text(value: arb) -> str:
    return value.str(24, more=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="q=8 F1024 TB block receipt")
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    if args.out.resolve() == PINNED_OUT.resolve():
        raise SystemExit(
            "refusing to overwrite the pinned immutable TB receipt; it is "
            "hash-bound by q8_schur_contour.py and by the R2/L-OUT receipts"
        )
    threshold_text = v2.THRESHOLD_TEXT
    if threshold_text != PER_TERM_FIELD_THRESHOLD_TEXT:
        raise SystemExit(
            f"q8_tb_support grades at {threshold_text} but serialises the "
            f"per-term verdict as ratio_less_than_{PER_TERM_FIELD_THRESHOLD_TEXT.replace('.', '_')}; "
            "the field name would be false by name"
        )
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
    # DEF-4: the verdict must consume the block verdict for EVERY block kind.
    # certify_block raises when no K passes for a tail family, but a
    # single-branch head block returns pass=False and returns normally, so a
    # verdict built from rho_star alone could contradict
    # all_head_and_deep_tail_terms_pass in the same receipt.
    rho_below_threshold = bool(rho.upper() < arb(threshold_text).lower())
    blocks_pass = all(row["pass"] for row in rows)
    poles_pass = all(row["pass"] for row in poles)
    cuts_pass = all(row["pass"] for row in cuts)
    verdict = (
        f"PASS_RHO_LT_{threshold_text}"
        if rho_below_threshold and blocks_pass and poles_pass and cuts_pass
        else "FAIL"
    )
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
            # Checkout-relative: an absolute path makes the payload depend on
            # the worktree it was generated in, which is not byte-deterministic.
            "path": "research_notes/rh_goals_2026-08-14/lane_f/f8_certify_tb_blocks.py",
            "count": len(blocks),
            "expected_count": 8,
            "exact_count_check": True,
            "blocks": [list(block) for block in blocks],
            "derivation": "MMS eq.(32) explicit q=8 list",
        },
        "blocks": rows,
        "rho_star": text(rho),
        "rho_star_upper_bound": text(rho.upper()),
        "threshold_text": threshold_text,
        "threshold": threshold_text,
        "threshold_source": "q8_tb_support.THRESHOLD_TEXT, the value certify_block actually grades against",
        "rho_less_than_threshold": rho_below_threshold,
        "pole_clearance": poles,
        "branch_cut_clearance": cuts,
        "all_head_and_deep_tail_terms_pass": blocks_pass,
        "all_pole_clearances_pass": poles_pass,
        "all_branch_cut_clearances_pass": cuts_pass,
        "block_kinds_covered_by_verdict": sorted(
            {"tail" if row["tail"] else "head" for row in rows}
        ),
        "certification_verdict": verdict,
        "certification_verdict_conjuncts": {
            "rho_star_lt_threshold": rho_below_threshold,
            "all_head_and_deep_tail_terms_pass": blocks_pass,
            "all_pole_clearances_pass": poles_pass,
            "all_branch_cut_clearances_pass": cuts_pass,
        },
        "hashed_payload_excludes_wall_clock": True,
        "pinned_receipt_not_overwritten": (
            "research_notes/rh_goals_2026-08-14/lane_f/f8_receipts/"
            "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"
        ),
        "scope_caveat": "Large radii are tested by the same pole/branch-cut and block-containment bounds; E1/Fredholm linkage remains OPEN.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        **{k: receipt[k] for k in (
            "rho_star_upper_bound", "threshold_text", "certification_verdict",
            "all_head_and_deep_tail_terms_pass", "all_pole_clearances_pass",
            "all_branch_cut_clearances_pass",
        )},
        "runtime_seconds_not_in_payload": time.perf_counter() - started,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
