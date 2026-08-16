#!/usr/bin/env python3
"""Arb certification of the q=7 T-b disc block bounds (stage 1 of F7_CERT_PLAN).

Port of the q=5 chain `tb_certify/certify_tb_blocks_v2.py` to q=7.  Everything
mathematical is REUSED, not re-implemented: the arc cover (`arc_ball`), the
contour supremum (`contour_sup`), the crude centred-at-zero deep-tail bound,
the pole/branch-cut clearances and the K-search are the q=5 modules' own
functions, which take (centers, radii, lam) as arguments and are therefore
q-independent.  Only the geometry is new:

  * lambda_7 = 2 cos(pi/7) as an Arb ball (q=5 used the golden-ratio form);
  * the kappa_7 = 5 Markov partition points of [-lambda/2, 0] built with the
    odd-q CF rules of `zeta_mayer_rosen.partition_points` in Arb;
  * the five ADOPTED disc inflation factors of F7_MITIGATION_REPORT.md
    section 7 (option 2), (3.522, 2.622, 2.372, 1.79, 1.6);
  * the 19-block source `f7_tb_disc_sweep.py` (9 heads + 10 Hurwitz tails).

The rho* gate is re-targeted from the q=5 chain's chosen 0.70 to 0.80, per
F7_CERT_PLAN.md section 2 / F7_CONSTANTS_MANIFEST.md item 5.  That re-target is
a CHOSEN target, not a theorem constant; the receipt records both the threshold
and the true certified bound, and the report states the derivation.

All reported bounds are Arb upper endpoints (rounded outward, i.e. UP);
margins are certified lower endpoints (DOWN).
"""

from __future__ import annotations

import argparse
import hashlib
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
Q = 7
KAPPA = 5
HQ = 2
THRESHOLD_TEXT = "0.80"
EXACT_FACTORS = ("3.522", "2.622", "2.372", "1.79", "1.6")
LANE_F = Path("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_f")
DEFAULT_SWEEP_SOURCE = LANE_F / "f7_tb_disc_sweep.py"
DEFAULT_OUT_DIR = LANE_F / "f7_receipts"
REPORT_NAME = "F7_TB_BLOCK_CERTIFICATES.md"
RECEIPT_NAME = "F7_TB_BLOCK_CERTIFICATES_RECEIPT.json"

Block = tuple[int, int, int, bool, bool]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def lam_ball() -> arb:
    """lambda_7 = 2 cos(pi/7) as a certified Arb ball."""

    return arb(2) * (arb.pi() / arb(Q)).cos()


def partition_points_ball(lam: arb) -> list[arb]:
    """q=7 counterpart of zeta_mayer_rosen.partition_points(7), in Arb.

    Odd-q branch with hq=2, kappa=5:
      phi_0 = -lambda/2
      phi_{2i}   = CF([1]*(hq-i) + [2] + [1]*hq),  1 <= i <= hq
      phi_{2i+1} = CF([1]*(hq-i)),                 0 <= i <= (kappa-1)/2
    """

    phi: dict[int, arb] = {0: -lam / arb(2)}
    for i in range(1, HQ + 1):
        phi[2 * i] = v1.cf_value_ball([1] * (HQ - i) + [2] + [1] * HQ, lam)
    for i in range(0, (KAPPA - 1) // 2 + 1):
        digits = [1] * (HQ - i)
        phi[2 * i + 1] = v1.cf_value_ball(digits, lam) if digits else arb(0)
    points = [phi[k] for k in range(0, KAPPA + 1)]
    if not all(points[k].upper() < points[k + 1].lower() for k in range(KAPPA)):
        raise ArithmeticError("q=7 Arb partition points are not strictly ordered")
    return points


def disc_geometry(lam: arb):
    points = partition_points_ball(lam)
    half = [(points[k] - points[k - 1]) / arb(2) for k in range(1, KAPPA + 1)]
    centers = [(points[k] + points[k - 1]) / arb(2) for k in range(1, KAPPA + 1)]
    multipliers = [arb(value) for value in EXACT_FACTORS]
    radii = [multipliers[k] * half[k] for k in range(KAPPA)]
    if not all(v1.definitely_positive(value) for value in half + radii):
        raise ArithmeticError("non-positive q=7 half-width or source radius")
    return points, centers, half, multipliers, radii


def make_receipt(
    blocks: list[Block],
    blocks_line: int,
    sweep_source: Path,
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
        "schema": "tb-block-certificates/v2",
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": precision_bits,
        "M": M,
        "q": Q,
        "kappa": KAPPA,
        "h_q": HQ,
        "lambda": v1.arb_text(lam),
        "lambda_min_poly": "x^3 - x^2 - 2x + 1",
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
            "path": str(sweep_source),
            "sha256": sha256(sweep_source),
            "assignment_line": blocks_line,
            "count": len(blocks),
            "expected_count": 19,
            "exact_count_check": len(blocks) == 19,
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
            "F7_CERT_PLAN.md section 2 / F7_CONSTANTS_MANIFEST.md item 5: the q=5 chain's "
            "0.70 gate is a chosen target, not a theorem constant; q=7's float stage-0 "
            "optimum sits at 0.7623 so the q=7 target is re-set to 0.80.  The certified "
            "value, not the gate, is what propagates to R2/R3b."
        ),
        "rho_less_than_threshold": rho_pass,
        "float_comparison_non_rigorous": {
            "float_rho_star": "0.762251293807",
            "source": "F7_MITIGATION_REPORT.md section 2 (option 2), reproduced by f7_tb_disc_sweep.py",
            "role": "NON-RIGOROUS FLOAT PREPARATION; not used in any certified value",
        },
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
    over: list[str] = []
    for block in receipt["blocks"]:
        for term in block["head_terms"]:
            if not term["ratio_less_than_0_70"]:
                over.append(f"{block['label']} n={term['n']}")
        deep = block["deep_tail"]
        if deep is not None and not deep["ratio_less_than_0_70"]:
            over.append(f"{block['label']} {deep['range']} crude tail")
    if receipt["rho_less_than_threshold"]:
        verdict = f"PASS: certified Arb upper bound is below {THRESHOLD_TEXT}"
    else:
        verdict = (
            f"FAIL: certified Arb upper bound is not below {THRESHOLD_TEXT}; "
            "over-threshold terms: " + (", ".join(over) if over else "none")
        )
    lines = [
        f"# F7 stage 1 — q=7 T-b block certificates (Arb)",
        "",
        f"certified rho* = {receipt['rho_star']} — {verdict}",
        "",
        f"Worst block: {receipt['worst_block_label']}.",
        "",
        "## Certification parameters",
        "",
        f"Backend: `{receipt['backend']}`; precision: `{receipt['precision_bits']}` bits; "
        f"arc cover: `M={receipt['M']}`; q: `{receipt['q']}`; kappa: `{receipt['kappa']}`.",
        "",
        f"Disc inflation factors (ADOPTED, F7_MITIGATION_REPORT section 7): "
        f"`{', '.join(receipt['radius_multipliers_exact_strings'])}`.",
        "",
        f"Block source: `{receipt['blocks_source']['path']}` "
        f"(sha256 `{receipt['blocks_source']['sha256']}`), "
        f"{receipt['blocks_source']['count']} blocks (expected 19).",
        "",
        "The rho* gate is re-targeted 0.70 -> 0.80 for q=7. Rationale: "
        + receipt["threshold_rationale"],
        "",
        "Non-rigorous float comparison (preparation only): float rho* = "
        f"`{receipt['float_comparison_non_rigorous']['float_rho_star']}`.",
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
            f"  --sweep-source {receipt['blocks_source']['path']} \\",
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
    # Re-target the shared V2 gate for q=7 before any term is certified.
    v2.THRESHOLD_TEXT = THRESHOLD_TEXT
    v2.THRESHOLD = arb(THRESHOLD_TEXT)

    sweep_source = Path(args.sweep_source).resolve()
    out_dir = Path(args.out_dir).resolve()
    blocks_raw, blocks_line = v1.load_blocks(sweep_source)
    blocks: list[Block] = [tuple(block) for block in blocks_raw]
    if len(blocks) != 19:
        raise SystemExit(f"BLOCKS count is {len(blocks)}, expected 19 for q=7")

    lam = lam_ball()
    points, centers, half, multipliers, radii = disc_geometry(lam)

    block_results: list[dict[str, Any]] = []
    for block in blocks:
        result, _terms, _trials = v2.certify_block(
            block, centers, radii, lam, args.M, args.K_start, args.max_K
        )
        block_results.append(result)
        print(
            f"[{len(block_results):2d}/19] {result['label']:24s} "
            f"ratio<= {result['ratio_upper_bound']} K={result['K_used']}",
            flush=True,
        )
    pole_rows, cut_rows = v2.clearance_rows(blocks, centers, radii, lam)
    receipt = make_receipt(
        blocks, blocks_line, sweep_source, points, centers, half, multipliers,
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
    parser.add_argument("--sweep-source", default=str(DEFAULT_SWEEP_SOURCE))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--precision-bits", type=int, default=PREC_BITS)
    parser.add_argument("--M", type=int, default=M_DEFAULT)
    parser.add_argument("--K-start", type=int, default=K_START_DEFAULT)
    parser.add_argument("--max-K", type=int, default=MAX_K_DEFAULT)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
