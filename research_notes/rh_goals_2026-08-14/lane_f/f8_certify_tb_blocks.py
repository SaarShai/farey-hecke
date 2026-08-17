#!/usr/bin/env python3
"""Arb certification of the q=8 T-b disc block bounds (stage 1 of F8_CERT_PLAN,
EVEN-q analogue of f7_certify_tb_blocks.py).

Port of f7_certify_tb_blocks.py to q=8.  Everything mathematical below the
geometry is REUSED, not re-implemented: arc cover (`arc_ball`), contour
supremum (`contour_sup`), the crude centred-at-zero deep-tail bound, pole/
branch-cut clearances and the K-search all come from the q=5 chain's
`tb_certify/certify_tb_blocks.py` (v1) / `certify_tb_blocks_v2.py` (v2), which
take (centers, radii, lam) as plain arguments and are therefore q-independent.
Only the geometry and the BLOCK LIST are new, and both are EVEN-q (MMS
eq.(32)), not odd-q (eq.(34)) like q=7:

  * lambda_8 = 2 cos(pi/8) = sqrt(2 + sqrt(2)) as an EXACT algebraic Arb ball
    (q=7 used a generic acb-cosine ball; q=8 has a closed radical form, same
    as `zeta_cert_rosen_even.lam_ball(8)`);
  * the kappa_8 = h_8 = 3 Markov partition points of [-lambda/2, 0], built
    with the EVEN-q CF rule phi_i = CF([1]*(h-i)), i = 0..h, phi_0 overridden
    to -lambda/2 (odd q needs TWO interleaved CF families, even q needs only
    ONE -- see F8_CERT_PLAN.md "even-q deltas" for the full derivation delta
    against eq.(34));
  * 3 disc inflation factors (radius multiplier), default 2.5 each -- the
    SAME safety factor `zeta_cert_rosen_even.disc_radii_ball` already uses
    (5/2), which that module's own `selfcheck_vs_doubleprec(8, ...)` has
    cross-validated against the double-precision reference at q=8;
  * the 8-block source (2 finite head-only blocks + 6 Hurwitz-tail families),
    hand-derived from `zeta_cert_rosen_even.build_reduced_matrix_ball`'s
    EVEN-q eq.(32) assembly loop at h=kappa=3 (q=7's odd-q eq.(34) needed 19
    blocks; q=8's even-q eq.(32) needs only 8 -- see F8_CERT_PLAN.md).

The rho* value here is REPORTED, not gated to a pre-chosen threshold: q=8 has
no prior float stage-0 optimization run (F7_MITIGATION_REPORT's analogue does
not exist yet for q=8), so there is no "chosen target" to re-target against.
Threshold PASS_RHO_LT_1 (rho* < 1, the basic convergence requirement) is used
as the only gate; N_PRIMARY/N_COMPARISON selection (F7_CERT_PLAN section 3
analogue) is a SEPARATE later step driven by the measured tail decay, not by
this rho* gate.

All reported bounds are Arb upper endpoints (rounded outward, i.e. UP);
margins are certified lower endpoints (DOWN).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

CODE_DIR = Path("/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
sys.path.insert(0, str(CODE_DIR / "tb_certify"))
sys.path.insert(0, str(CODE_DIR))

from flint import arb, ctx  # noqa: E402

import certify_tb_blocks as v1  # noqa: E402
import certify_tb_blocks_v2 as v2  # noqa: E402


PREC_BITS = 384
M_DEFAULT = 512
K_START_DEFAULT = 12
MAX_K_DEFAULT = 64
Q = 8
HQ = 3
KAPPA = 3  # even q: kappa == h_q (odd q=7 had kappa = 2*h+1 = 5)
THRESHOLD_TEXT = "0.99"  # GATE 2 target (F8_CERT_PLAN.md sec "gates")
# ADOPTED disc inflation factors: GATE-2 hardened, coarse-grid + local-refine
# search over the 8 eq.(32) blocks (see F8_CERT_PLAN.md "gates" section for
# the full search log). The uniform safety=5/2 default zeta_cert_rosen_even.py
# uses for the DETERMINANT build (chosen there for numerical robustness, not
# for this ratio bound) does NOT certify: at factor 2.5 uniform, the two
# finite head-only blocks (2->1, 3->2, both n=1 direct partition-adjacency
# maps) have ratio 1.26/1.63 > 1. Uniform scaling makes it WORSE, not better
# (ratio grows with the factor). An UNCONSTRAINED Nelder-Mead search finds
# ratio -> 0.65 at factors ~(14.7, 5.0, 2.2) -- rejected as geometrically
# unsound (disc 1 would then extend past Re=0 and heavily overlap discs 2,3,
# untested against pole/branch-cut clearance at that scale). Search was
# capped at factors <=5.0 (~1.4x q=7's own largest adopted factor 3.522) and
# the adopted point (3.4, 2.2, 1.4) gives certified ratio ~0.80 -- comfortably
# under the 0.99 gate and in the SAME range as q=7's own adopted rho*
# (0.7623 float / 0.762251293807 certified).
EXACT_FACTORS = ("3.4", "2.2", "1.4")
LANE_F = Path("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f")
DEFAULT_OUT_DIR = LANE_F / "f8_receipts"
REPORT_NAME = "F8_TB_BLOCK_CERTIFICATES.md"
RECEIPT_NAME = "F8_TB_BLOCK_CERTIFICATES_RECEIPT.json"

Block = tuple[int, int, int, bool, bool]

# ---------------------------------------------------------------------------
# The 8-block EVEN-q eq.(32) list at h = kappa = 3, hand-derived from
# zeta_cert_rosen_even.build_reduced_matrix_ball's assembly loop:
#
#   add_cols(1, h, inf_block(1, h, 2, False))
#   add_cols(1, h, inf_block(1, h, 1, True), prefac=sgn)
#   for i in 2..h:
#       add_cols(i, i-1, single_block(i, i-1, 1, False))
#       add_cols(i, h, inf_block(i, h, 2, False))
#       add_cols(i, h, inf_block(i, h, 1, True), prefac=sgn)
#
# Tuple format (out_i, in_j, n, neg, is_tail), 1-indexed -- same convention
# as f7_tb_disc_sweep.py's BLOCKS.
# ---------------------------------------------------------------------------
BLOCKS: list[Block] = [
    (1, 3, 2, False, True),
    (1, 3, 1, True, True),
    (2, 1, 1, False, False),
    (2, 3, 2, False, True),
    (2, 3, 1, True, True),
    (3, 2, 1, False, False),
    (3, 3, 2, False, True),
    (3, 3, 1, True, True),
]
assert len(BLOCKS) == 8, "even-q q=8 eq.(32) block count must be 8 (2 finite + 6 tail)"


def lam_ball() -> arb:
    """lambda_8 = 2 cos(pi/8) = sqrt(2 + sqrt(2)), exact algebraic Arb ball."""

    return (arb(2) + arb(2).sqrt()).sqrt()


def partition_points_ball(lam: arb) -> list[arb]:
    """q=8 counterpart of zeta_cert_rosen_even.partition_points_ball(8, .), in Arb.

    EVEN-q branch, h = 3, kappa = 3:
      phi_i = CF([1]*(h-i)),  i = 0..h   (single CF family -- odd q needs two
      interleaved families; see F8_CERT_PLAN.md "even-q deltas")
      phi_0 overridden to -lambda/2 (the h-i=3 word CF value is NOT phi_0 in
      the even-q convention; zeta_cert_rosen_even.partition_points_ball does
      the same override then re-sorts).
    """

    phis: dict[int, arb] = {}
    for i in range(0, HQ + 1):
        digits = [1] * (HQ - i)
        phis[i] = v1.cf_value_ball(digits, lam) if digits else arb(0)
    phis[0] = -lam / arb(2)
    points = sorted(phis.values(), key=lambda x: float(x.mid()))
    if not all(points[k].upper() < points[k + 1].lower() for k in range(HQ)):
        raise ArithmeticError("q=8 Arb partition points are not strictly ordered")
    return points


def disc_geometry_for(lam: arb, factors: tuple[str, ...] = EXACT_FACTORS):
    points = partition_points_ball(lam)
    half = [(points[k] - points[k - 1]) / arb(2) for k in range(1, KAPPA + 1)]
    centers = [(points[k] + points[k - 1]) / arb(2) for k in range(1, KAPPA + 1)]
    multipliers = [arb(value) for value in factors]
    radii = [multipliers[k] * half[k] for k in range(KAPPA)]
    if not all(v1.definitely_positive(value) for value in half + radii):
        raise ArithmeticError("non-positive q=8 half-width or source radius")
    return points, centers, half, multipliers, radii


def disc_geometry(lam: arb):
    return disc_geometry_for(lam, EXACT_FACTORS)


def make_receipt(
    blocks: list[Block],
    points: list[arb],
    centers: list[arb],
    half: list[arb],
    multipliers: list[arb],
    radii: list[arb],
    lam: arb,
    block_results: list[dict[str, Any]],
    pole_rows: list[dict[str, Any]],
    cut_rows: list[dict[str, Any]],
    precision_bits: int,
    M: int,
    K_start: int,
    max_K: int,
    runtime: float,
) -> dict[str, Any]:
    threshold = v2.THRESHOLD
    ratios: list[arb] = []
    for block in block_results:
        for term in block["head_terms"]:
            ratios.append(arb(term["ratio_upper_bound"]))
        if block["deep_tail"] is not None:
            ratios.append(arb(block["deep_tail"]["ratio_upper_bound"]))
    rho = v1.max_arb(ratios)
    worst = max(
        ((block["label"], arb(block["ratio_upper_bound"]), block) for block in block_results),
        key=lambda item: item[1].upper(),
    )[2]
    all_terms_pass = all(
        term["pass"] for block in block_results for term in block["head_terms"]
    ) and all(
        block["deep_tail"] is None or block["deep_tail"]["pass"] for block in block_results
    )
    all_poles_clear = all(row["pass"] for row in pole_rows)
    all_cuts_clear = all(row["pass"] for row in cut_rows)
    tail_families = [block for block in block_results if block["tail"]]
    rho_pass = v1.definitely_negative(rho - threshold)
    return {
        "schema": "tb-block-certificates/v2-q8",
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": precision_bits,
        "M": M,
        "q": Q,
        "kappa": KAPPA,
        "h_q": HQ,
        "even_q": True,
        "lambda": v1.arb_text(lam),
        "lambda_exact_form": "sqrt(2 + sqrt(2))",
        "partition_points": [v1.arb_text(x) for x in points],
        "centers": [v1.arb_text(x) for x in centers],
        "half_widths": [v1.arb_text(x) for x in half],
        "radius_multipliers": [v1.arb_text(x) for x in multipliers],
        "radius_multipliers_exact_strings": list(EXACT_FACTORS),
        "source_radii": [v1.arb_text(x) for x in radii],
        "tail_split": {
            "K_start": K_start,
            "max_K": max_K,
            "head_range": "n0..n0+K inclusive, individually arc-certified",
            "deep_range": "n>n0+K",
            "deep_first_index": "n0+K+1",
            "deep_bound": "1/(n*lambda-|c_i|-R_i) + |c_j|, centered at 0",
            "deep_supremum_at_first_index": True,
        },
        "blocks_source": {
            "path": str(Path(__file__).resolve()),
            "derivation": "hand-derived from zeta_cert_rosen_even.build_reduced_matrix_ball "
            "eq.(32) assembly loop at h=kappa=3, NOT a swept/captured file (q=7 used a "
            "captured sweep source; q=8's eq.(32) loop is short enough to transcribe "
            "directly -- see module docstring)",
            "count": len(blocks),
            "expected_count": 8,
            "exact_count_check": len(blocks) == 8,
            "blocks": [list(block) for block in blocks],
        },
        "blocks": block_results,
        "tail_families": [
            {
                "label": block["label"],
                "block": block["block"],
                "n0": block["n0"],
                "K_used": block["K_used"],
                "worst_head_ratio_upper_bound": v1.arb_text(
                    v1.max_arb([arb(term["ratio_upper_bound"]) for term in block["head_terms"]])
                ),
                "crude_tail_first_n": block["deep_tail"]["first_n"],
                "crude_tail_ratio_upper_bound": block["deep_tail"]["ratio_upper_bound"],
                "crude_tail_pass": block["deep_tail"]["pass"],
            }
            for block in tail_families
        ],
        "rho_star": v1.arb_text(rho),
        "rho_star_upper_bound": v1.arb_text(rho.upper()),
        "worst_block": worst["block"],
        "worst_block_label": worst["label"],
        "threshold_text": THRESHOLD_TEXT,
        "threshold": v1.arb_text(threshold),
        "threshold_rationale": (
            "No q=8 float stage-0 optimization exists yet (unlike q=7's "
            "F7_MITIGATION_REPORT.md), so there is no chosen target to re-target "
            "against. rho* < 1 (basic convergence) is used as the only gate here; "
            "the true certified rho* value (not the gate) is what should drive any "
            "later disc-radius optimization or R2/R3b N-budget decision."
        ),
        "rho_less_than_threshold": rho_pass,
        "pole_clearance": pole_rows,
        "branch_cut_clearance": cut_rows,
        "all_head_and_deep_tail_terms_pass": all_terms_pass,
        "all_pole_clearances_pass": all_poles_clear,
        "all_branch_cut_clearances_pass": all_cuts_clear,
        "runtime_seconds": runtime,
        "certification_verdict": (
            f"PASS_RHO_LT_{THRESHOLD_TEXT}"
            if rho_pass and all_terms_pass and all_poles_clear and all_cuts_clear
            else "FAIL_RHO_THRESHOLD_OR_CLEARANCE_REPORT_TRUE_CERTIFIED_VALUES"
        ),
    }


def report_text(receipt: dict[str, Any], code_path: Path, receipt_path: Path) -> str:
    lines = [
        "# F8 stage 1 — q=8 T-b block certificates (Arb, even-q eq.(32))",
        "",
        f"certified rho* = {receipt['rho_star']} "
        f"({'PASS' if receipt['rho_less_than_threshold'] else 'FAIL'} rho* < {THRESHOLD_TEXT})",
        "",
        f"Worst block: {receipt['worst_block_label']}.",
        "",
        "## Certification parameters",
        "",
        f"Backend: `{receipt['backend']}`; precision: `{receipt['precision_bits']}` bits; "
        f"arc cover: `M={receipt['M']}`; q: `{receipt['q']}`; kappa: `{receipt['kappa']}` "
        f"(even q, kappa == h_q).",
        "",
        f"Disc inflation factors: `{', '.join(receipt['radius_multipliers_exact_strings'])}` "
        "(GATE-2 hardened, non-uniform per-disc; NOT zeta_cert_rosen_even's fixed "
        "safety=5/2 determinant-build geometry -- see F8_CERT_PLAN.md 'gates').",
        "",
        f"Block source: {receipt['blocks_source']['count']} blocks "
        f"(expected 8 = 2 finite + 6 tail, eq.(32) derivation).",
        "",
        "## Per-block and per-n certified bounds",
        "",
        "| block/family | term | method | certified sup / target-distance upper bound | ratio to a_j*h_j | pass |",
        "|---|---|---|---:|---:|---|",
    ]
    for block in receipt["blocks"]:
        for term in block["head_terms"]:
            lines.append(
                f"| {block['label']} | n={term['n']} | individual M={receipt['M']} arc | "
                f"{term['certified_sup_upper_bound']} | {term['ratio_upper_bound']} | "
                f"{'PASS' if term['pass'] else 'FAIL'} |"
            )
        deep = block["deep_tail"]
        if deep is not None:
            lines.append(
                f"| {block['label']} | {deep['range']} (max at n={deep['first_n']}) | "
                "crude centered-at-zero ball | "
                f"{deep['target_distance_upper']} | {deep['ratio_upper_bound']} | "
                f"{'PASS' if deep['pass'] else 'FAIL'} |"
            )
    lines.extend(
        [
            "",
            "## Tail-family summary",
            "",
            "| tail family | n0 | K used | worst individual-head ratio | crude-tail ratio at n0+K+1 | verdict |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for family in receipt["tail_families"]:
        lines.append(
            f"| {family['label']} | {family['n0']} | {family['K_used']} | "
            f"{family['worst_head_ratio_upper_bound']} | "
            f"{family['crude_tail_ratio_upper_bound']} | "
            f"{'PASS' if family['crude_tail_pass'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "## Pole clearance",
            "",
            "| block | used branch | pole location | margin to closed source disc | verdict |",
            "|---|---|---:|---:|---|",
        ]
    )
    for row in receipt["pole_clearance"]:
        lines.append(
            f"| {v2.label_for(row['block'])} | {row['branch']} | {row['pole_location']} | "
            f"{row['margin']} | {'PASS' if row['pass'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "## Branch-cut clearance",
            "",
            "| block | branch-cut expression | certified lower-bound interval | verdict |",
            "|---|---|---:|---|",
        ]
    )
    for row in receipt["branch_cut_clearance"]:
        lines.append(
            f"| {v2.label_for(row['block'])} | `{row['expression']}` | {row['margin']} | "
            f"{'PASS' if row['pass'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "## Reproducibility",
            "",
            f"Receipt: [{receipt_path.name}]({receipt_path}).",
            "",
            "```bash",
            f"/Users/za/.venvs/farey-rh/bin/python {code_path} \\",
            f"  --out-dir {receipt_path.parent} \\",
            f"  --precision-bits {receipt['precision_bits']} --M {receipt['M']} \\",
            f"  --K-start {receipt['tail_split']['K_start']} --max-K {receipt['tail_split']['max_K']}",
            "```",
            "",
            f"Wall time: {receipt['runtime_seconds']:.1f} s.",
            "",
        ]
    )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.M != M_DEFAULT:
        raise SystemExit(f"M must be exactly {M_DEFAULT} for this certification")
    if args.precision_bits != PREC_BITS:
        raise SystemExit(f"precision must be exactly {PREC_BITS} bits")
    if args.K_start < 0 or args.max_K < args.K_start:
        raise SystemExit("require 0 <= K-start <= max-K")
    started = time.perf_counter()
    ctx.prec = args.precision_bits
    v2.THRESHOLD_TEXT = THRESHOLD_TEXT
    v2.THRESHOLD = arb(THRESHOLD_TEXT)

    out_dir = Path(args.out_dir).resolve()
    blocks = BLOCKS

    lam = lam_ball()
    points, centers, half, multipliers, radii = disc_geometry(lam)

    block_results: list[dict[str, Any]] = []
    for block in blocks:
        result, _terms, _trials = v2.certify_block(
            block, centers, radii, lam, args.M, args.K_start, args.max_K
        )
        block_results.append(result)
        print(
            f"[{len(block_results):2d}/8] {result['label']:24s} "
            f"ratio<= {result['ratio_upper_bound']} K={result['K_used']}",
            flush=True,
        )
    pole_rows, cut_rows = v2.clearance_rows(blocks, centers, radii, lam)
    receipt = make_receipt(
        blocks, points, centers, half, multipliers,
        radii, lam, block_results, pole_rows, cut_rows, args.precision_bits,
        args.M, args.K_start, args.max_K, time.perf_counter() - started,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = out_dir / RECEIPT_NAME
    report_path = out_dir / REPORT_NAME
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(report_text(receipt, Path(__file__).resolve(), receipt_path), encoding="utf-8")
    print(
        json.dumps(
            {
                "receipt": str(receipt_path),
                "report": str(report_path),
                "rho_star": receipt["rho_star"],
                "rho_star_upper_bound": receipt["rho_star_upper_bound"],
                "worst_block": receipt["worst_block_label"],
                "verdict": receipt["certification_verdict"],
                "runtime_seconds": receipt["runtime_seconds"],
                "K_used_by_family": {
                    family["label"]: family["K_used"] for family in receipt["tail_families"]
                },
            },
            indent=2,
        )
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--precision-bits", type=int, default=PREC_BITS)
    parser.add_argument("--M", type=int, default=M_DEFAULT)
    parser.add_argument("--K-start", type=int, default=K_START_DEFAULT)
    parser.add_argument("--max-K", type=int, default=MAX_K_DEFAULT)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
