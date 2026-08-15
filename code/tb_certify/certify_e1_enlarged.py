#!/usr/bin/env python3
"""Receipted E1 certification on the enlarged q=5 source contours.

This is a narrow adaptation of ``certify_tb_blocks_v2.py``.  It keeps the
same q=5 Arb/Acb geometry, 512-arc enclosure, split-tail construction, and
pole/cut expressions, but replaces V2's ``rho < 0.70`` gate by the E1 gate
``rho_hat < 1`` and uses ``R_i + 0.1`` only for source contours.  Target
radii remain the original V2 radii.

The receipt is written after initialization and after every family.  Thus
the JSON at the requested output path is also a valid checkpoint if a run is
interrupted before finalization.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from flint import arb, ctx

import certify_tb_blocks_v2 as v2


PREC_BITS = 384
M_DEFAULT = 512
EPSILON_TEXT = "0.1"
K_START_DEFAULT = 12
MAX_K_DEFAULT = 64
RHO_LIMIT_TEXT = "1"
REVIEW_RHO_LIMIT_TEXT = "0.948343590351"
REVIEW_MARGIN_LIMIT_TEXT = "1.00238"
REVIEW_WORST_LABEL = "3â1, +1, head"

DEFAULT_SWEEP_SOURCE = v2.DEFAULT_SWEEP_SOURCE
DEFAULT_OPT_JSON = v2.DEFAULT_OPT_JSON
DEFAULT_REPORT_DIR = v2.DEFAULT_REPORT_DIR
REPORT_NAME = "E1_ENLARGED_CONTRACTION_CERT.md"
RECEIPT_NAME = "E1_ENLARGED_CONTRACTION_RECEIPT.json"

Block = tuple[int, int, int, bool, bool]


def label_for(block: list[Any] | Block) -> str:
    i, j, n, neg, tail = block
    return f"{i}â{j}, {'â' if neg else '+'}{n}, {'tail' if tail else 'head'}"


def arb_text(value: arb, digits: int = 24) -> str:
    return v2.v1.arb_text(value, digits)


def less_than_one(value: arb) -> bool:
    return v2.v1.definitely_negative(value - arb(RHO_LIMIT_TEXT))


def positive(value: arb) -> bool:
    return v2.v1.definitely_positive(value)


def max_ball(values: list[arb]) -> arb:
    return v2.v1.max_arb(values)


def min_ball(values: list[arb]) -> arb:
    """Enclose the minimum of a finite list of Arb balls."""

    lower = min(value.lower() for value in values)
    upper = min(value.upper() for value in values)
    return arb((lower + upper) / arb(2), (upper - lower) / arb(2))


def serial_head(term: dict[str, Any]) -> dict[str, Any]:
    return {
        "n": term["n"],
        "kind": term["kind"],
        "arc_cover": term["arc_cover"],
        "certified_sup_upper_bound": arb_text(term["certified_sup"]),
        "ratio_upper_bound": arb_text(term["ratio"]),
        "ratio_less_than_1": term["ratio_less_than_1"],
        "pass": term["pass"],
    }


def serial_deep(term: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "first_n": term["first_n"],
        "range": term["range"],
        "kind": term["kind"],
        "image_ball_center": term["image_ball_center"],
        "denominator_lower_bound": (
            arb_text(term["denominator"]) if term["denominator"] is not None else None
        ),
        "image_ball_radius": (
            arb_text(term["image_radius"]) if term["image_radius"] is not None else None
        ),
        "target_distance_upper": (
            arb_text(term["target_distance"])
            if term["target_distance"] is not None
            else None
        ),
        "target_disc_margin": (
            arb_text(term["target_margin"])
            if term["target_margin"] is not None
            else None
        ),
        "inside_with_margin": term["inside_with_margin"],
        "ratio_upper_bound": (
            arb_text(term["ratio"]) if term["ratio"] is not None else None
        ),
        "ratio_less_than_1": term["ratio_less_than_1"],
        "pass": term["pass"],
        "failure": term.get("failure"),
    }
    return result


def enlarged_head_term(
    block: Block,
    n: int,
    centers: list[arb],
    source_radii: list[arb],
    target_radii: list[arb],
    lam: arb,
    M: int,
) -> dict[str, Any]:
    i, j, _n0, neg, _tail = block
    certified_sup = v2.v1.contour_sup(
        centers[i - 1],
        source_radii[i - 1],
        centers[j - 1],
        lam,
        n,
        neg,
        M,
    )
    ratio = certified_sup / target_radii[j - 1]
    return {
        "n": n,
        "kind": "individual_arc",
        "arc_cover": {"M": M, "arc_enclosure": "Acb rectangular ball"},
        "certified_sup": certified_sup,
        "ratio": ratio,
        "ratio_less_than_1": less_than_one(ratio),
        "pass": less_than_one(ratio),
    }


def enlarged_deep_tail_term(
    block: Block,
    first_n: int,
    centers: list[arb],
    source_radii: list[arb],
    target_radii: list[arb],
    lam: arb,
) -> dict[str, Any]:
    """Apply V2's centered-at-zero monotone first-n bound at R_i+0.1."""

    i, j, _n0, _neg, _tail = block
    ci, cj = centers[i - 1], centers[j - 1]
    source_radius, target_radius = source_radii[i - 1], target_radii[j - 1]
    denominator = arb(first_n) * lam - ci.abs_upper() - source_radius
    if not positive(denominator):
        return {
            "first_n": first_n,
            "range": f"nâ¥{first_n}",
            "kind": "crude_deep_tail",
            "image_ball_center": "0",
            "denominator": denominator,
            "image_radius": None,
            "target_distance": None,
            "target_margin": None,
            "ratio": None,
            "inside_with_margin": False,
            "ratio_less_than_1": False,
            "pass": False,
            "failure": "deep-tail denominator is not definitely positive",
        }
    image_radius = arb(1) / denominator
    target_distance = image_radius + cj.abs_upper()
    target_margin = target_radius - target_distance
    ratio = target_distance / target_radius
    return {
        "first_n": first_n,
        "range": f"nâ¥{first_n}",
        "kind": "crude_deep_tail",
        "image_ball_center": "0",
        "denominator": denominator,
        "image_radius": image_radius,
        "target_distance": target_distance,
        "target_margin": target_margin,
        "ratio": ratio,
        "inside_with_margin": positive(target_margin),
        "ratio_less_than_1": less_than_one(ratio),
        "pass": positive(target_margin) and less_than_one(ratio),
        "failure": None,
    }


def family_result(
    block: Block,
    centers: list[arb],
    source_radii: list[arb],
    target_radii: list[arb],
    lam: arb,
    M: int,
    K_start: int,
    max_K: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    i, j, n0, neg, tail = block
    if not tail:
        term = enlarged_head_term(
            block, n0, centers, source_radii, target_radii, lam, M
        )
        result = {
            "block": list(block),
            "label": label_for(block),
            "tail": False,
            "n0": n0,
            "K_used": None,
            "head_terms": [serial_head(term)],
            "deep_tail": None,
            "certified_sup_upper_bound": arb_text(term["certified_sup"]),
            "ratio_upper_bound": arb_text(term["ratio"]),
            "pass": term["pass"],
            "failure": None if term["pass"] else "head ratio is not definitely below 1",
        }
        return result, [term["ratio"]]

    terms: dict[int, dict[str, Any]] = {}
    trials: list[dict[str, Any]] = []
    last_deep: dict[str, Any] | None = None
    K = K_start
    while K <= max_K:
        for n in range(n0, n0 + K + 1):
            if n not in terms:
                terms[n] = enlarged_head_term(
                    block, n, centers, source_radii, target_radii, lam, M
                )
        deep = enlarged_deep_tail_term(
            block, n0 + K + 1, centers, source_radii, target_radii, lam
        )
        last_deep = deep
        heads_pass = all(term["pass"] for term in terms.values())
        trial_pass = heads_pass and deep["pass"]
        trials.append(
            {
                "K": K,
                "head_terms_pass": heads_pass,
                "deep_first_n": deep["first_n"],
                "deep_ratio_upper_bound": (
                    arb_text(deep["ratio"]) if deep["ratio"] is not None else None
                ),
                "deep_inside_with_margin": deep["inside_with_margin"],
                "deep_ratio_less_than_1": deep["ratio_less_than_1"],
                "pass": trial_pass,
            }
        )
        if trial_pass:
            selected_terms = [terms[n] for n in range(n0, n0 + K + 1)]
            ratios = [term["ratio"] for term in selected_terms]
            ratios.append(deep["ratio"])
            sups = [term["certified_sup"] for term in selected_terms]
            sups.append(deep["target_distance"])
            result = {
                "block": list(block),
                "label": label_for(block),
                "tail": True,
                "n0": n0,
                "K_used": K,
                "head_terms": [serial_head(term) for term in selected_terms],
                "deep_tail": serial_deep(deep),
                "certified_sup_upper_bound": arb_text(max_ball(sups)),
                "ratio_upper_bound": arb_text(max_ball(ratios)),
                "pass": True,
                "failure": None,
                "K_search_trials": trials,
            }
            return result, ratios
        K += 1

    selected_terms = [terms[n] for n in range(n0, n0 + max_K + 1)]
    assert last_deep is not None
    ratios = [term["ratio"] for term in selected_terms]
    if last_deep["ratio"] is not None:
        ratios.append(last_deep["ratio"])
    sups = [term["certified_sup"] for term in selected_terms]
    if last_deep["target_distance"] is not None:
        sups.append(last_deep["target_distance"])
    result = {
        "block": list(block),
        "label": label_for(block),
        "tail": True,
        "n0": n0,
        "K_used": None,
        "head_terms": [serial_head(term) for term in selected_terms],
        "deep_tail": serial_deep(last_deep),
        "certified_sup_upper_bound": arb_text(max_ball(sups)),
        "ratio_upper_bound": arb_text(max_ball(ratios)),
        "pass": False,
        "failure": f"no passing K through {max_K}; exact trial values retained",
        "K_search_trials": trials,
    }
    return result, ratios


def clearance_for_block(
    block: Block,
    centers: list[arb],
    source_radii: list[arb],
    lam: arb,
) -> tuple[dict[str, Any], dict[str, Any]]:
    i, _j, n0, neg, tail = block
    ci, ri = centers[i - 1], source_radii[i - 1]
    pole = v2.v1.branch_pole(ci, lam, n0, neg)
    pole_margin = v2.v1.pole_margin(ci, ri, pole)
    pole_row = {
        "block": list(block),
        "branch": f"theta_{'-' if neg else ''}{n0}"
        + (f" (nâ¥{n0})" if tail else ""),
        "pole_location": arb_text(pole),
        "margin": arb_text(pole_margin),
        "pass": positive(pole_margin),
    }
    cut_margin = v2.v1.branch_cut_margin(ci, ri, lam, n0, neg)
    cut_row = {
        "block": list(block),
        "expression": f"Re(nÎ»âz), nâ¥{n0}" if neg else f"Re(z+nÎ»), nâ¥{n0}",
        "margin": arb_text(cut_margin),
        "pass": positive(cut_margin),
    }
    return pole_row, cut_row


def checkpoint_write(receipt: dict[str, Any], receipt_path: Path, event: dict[str, Any]) -> None:
    receipt["checkpoint_trail"].append(event)
    receipt["checkpoint_count"] = len(receipt["checkpoint_trail"])
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def current_min_margin(
    pole_rows: list[dict[str, Any]], cut_rows: list[dict[str, Any]]
) -> tuple[str | None, str | None]:
    rows = pole_rows + cut_rows
    if not rows:
        return None, None
    margins = [arb(row["margin"]) for row in rows]
    ball = min_ball(margins)
    return arb_text(ball), arb_text(ball.lower())


def finalize_receipt(
    receipt: dict[str, Any],
    raw_ratios: list[tuple[str, int | None, arb]],
    pole_rows: list[dict[str, Any]],
    cut_rows: list[dict[str, Any]],
) -> None:
    rho = max_ball([value for _label, _n, value in raw_ratios])
    worst_label, worst_n, _worst_value = max(
        raw_ratios, key=lambda item: item[2].upper()
    )
    margin_rows = pole_rows + cut_rows
    margin_values = [arb(row["margin"]) for row in margin_rows]
    min_margin = min_ball(margin_values)
    min_margin_row = min(
        margin_rows, key=lambda row: arb(row["margin"]).upper()
    )
    all_families_pass = all(block["pass"] for block in receipt["blocks"])
    all_poles_clear = all(row["pass"] for row in pole_rows)
    all_cuts_clear = all(row["pass"] for row in cut_rows)
    rho_pass = less_than_one(rho)
    failures: list[dict[str, Any]] = []
    for block in receipt["blocks"]:
        if not block["pass"]:
            failures.append(
                {
                    "family": block["label"],
                    "failure": block["failure"],
                    "ratio_upper_bound": block["ratio_upper_bound"],
                }
            )
        for term in block["head_terms"]:
            if not term["pass"]:
                failures.append(
                    {
                        "family": block["label"],
                        "branch": f"n={term['n']}",
                        "failure": "head ratio is not definitely below 1",
                        "ratio_upper_bound": term["ratio_upper_bound"],
                    }
                )
        deep = block["deep_tail"]
        if deep is not None and not deep["pass"]:
            failures.append(
                {
                    "family": block["label"],
                    "branch": deep["range"],
                    "failure": deep["failure"] or "deep-tail bound failed",
                    "ratio_upper_bound": deep["ratio_upper_bound"],
                    "target_disc_margin": deep["target_disc_margin"],
                }
            )
    failures.extend(
        {
            "family": label_for(row["block"]),
            "failure": "pole clearance is not definitely positive",
            "margin": row["margin"],
        }
        for row in pole_rows
        if not row["pass"]
    )
    failures.extend(
        {
            "family": label_for(row["block"]),
            "failure": "branch-cut clearance is not definitely positive",
            "margin": row["margin"],
        }
        for row in cut_rows
        if not row["pass"]
    )
    review_rho = arb(REVIEW_RHO_LIMIT_TEXT)
    review_margin = arb(REVIEW_MARGIN_LIMIT_TEXT)
    rho_relation = (
        "BEATS" if rho.upper() < review_rho else "REPRODUCES" if rho.upper() <= review_rho else "FALLS_SHORT"
    )
    margin_relation = (
        "BEATS"
        if min_margin.lower() > review_margin
        else "REPRODUCES"
        if min_margin.lower() >= review_margin
        else "FALLS_SHORT"
    )
    exact_review_note = (
        "The reviewerâs unrounded value 1.0023798735622528932 rounds to 1.00238; "
        "the literal unrounded comparison with 1.00238 is reported without relabeling."
    )
    receipt.update(
        {
            "status": "FINALIZED",
            "rho_hat_ball": arb_text(rho),
            "rho_hat_upper_bound": arb_text(rho.upper()),
            "rho_hat_less_than_1": rho_pass,
            "worst_branch": {
                "label": worst_label,
                "n": worst_n,
                "rho_ball": arb_text(
                    next(value for label, n, value in raw_ratios if label == worst_label and n == worst_n)
                ),
            },
            "minimum_pole_cut_margin_ball": arb_text(min_margin),
            "minimum_pole_cut_margin_lower_bound": arb_text(min_margin.lower()),
            "minimum_pole_cut_margin_source": {
                "kind": "pole" if min_margin_row in pole_rows else "branch_cut",
                "block": min_margin_row["block"],
                "label": label_for(min_margin_row["block"]),
            },
            "all_families_pass": all_families_pass,
            "all_pole_clearances_pass": all_poles_clear,
            "all_branch_cut_clearances_pass": all_cuts_clear,
            "failure_values": failures,
            "reviewer_diagnostic": {
                "source": "ADVERSARIAL_REVIEW_V7_R5V3.md Â§(ii)",
                "rho_hat_upper_bound": REVIEW_RHO_LIMIT_TEXT,
                "worst_branch": REVIEW_WORST_LABEL,
                "minimum_margin_lower_bound": REVIEW_MARGIN_LIMIT_TEXT,
                "rho_comparison": rho_relation,
                "worst_branch_comparison": (
                    "REPRODUCES" if worst_label == REVIEW_WORST_LABEL else "FALLS_SHORT"
                ),
                "margin_comparison": margin_relation,
                "note": exact_review_note,
            },
            "certification_verdict": (
                "PASS_RHO_HAT_LT_1_AND_CLEARANCE_POSITIVE"
                if rho_pass and all_families_pass and all_poles_clear and all_cuts_clear
                else "FAIL_REPORT_EXACT_RHO_OR_CLEARANCE_VALUES"
            ),
        }
    )


def report_text(receipt: dict[str, Any], code_path: Path, receipt_path: Path) -> str:
    verdict = receipt["certification_verdict"]
    lines = [
        f"VERDICT: {verdict}",
        "",
        f"Global rho_hat ball: `{receipt['rho_hat_ball']}`; certified upper bound: `{receipt['rho_hat_upper_bound']}`.",
        f"Worst branch: **{receipt['worst_branch']['label']}** (n={receipt['worst_branch']['n']}), rho ball `{receipt['worst_branch']['rho_ball']}`.",
        f"Minimum pole/cut margin ball: `{receipt['minimum_pole_cut_margin_ball']}`; certified lower bound: `{receipt['minimum_pole_cut_margin_lower_bound']}`.",
        "",
        "## Per-family summary",
        "",
        "| family | finite head range | deep tail first n | family rho upper bound | pole margin | cut margin | verdict |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for block in receipt["blocks"]:
        head_ns = ", ".join(str(term["n"]) for term in block["head_terms"])
        deep = block["deep_tail"]
        pole = next(row for row in receipt["pole_clearance"] if row["block"] == block["block"])
        cut = next(row for row in receipt["branch_cut_clearance"] if row["block"] == block["block"])
        lines.append(
            f"| {block['label']} | {head_ns} | "
            f"{deep['first_n'] if deep is not None else 'n/a'} | "
            f"{block['ratio_upper_bound']} | {pole['margin']} | {cut['margin']} | "
            f"{'PASS' if block['pass'] and pole['pass'] and cut['pass'] else 'FAIL'} |"
        )
    review = receipt["reviewer_diagnostic"]
    lines.extend(
        [
            "",
            "## Reviewer diagnostic cross-check",
            "",
            f"The receipted run **{review['rho_comparison'].lower()}** the reviewer rho diagnostic: `{receipt['rho_hat_upper_bound']}` versus `â¤ {review['rho_hat_upper_bound']}`.",
            f"Worst-branch identity: **{review['worst_branch_comparison'].lower()}** ({receipt['worst_branch'] ['label']} versus `{review['worst_branch']}`).",
            f"For the printed margin diagnostic it **{review['margin_comparison'].lower()}**: `{receipt['minimum_pole_cut_margin_lower_bound']}` versus `â¥ {review['minimum_margin_lower_bound']}`.",
            review["note"],
            "",
            "## Certification parameters and source boundary",
            "",
            f"Backend: `{receipt['backend']}`; precision: `{receipt['precision_bits']}` bits; arc cover: `M={receipt['M']}`; q: `{receipt['q']}`.",
            f"Radius-factor strings: `{', '.join(receipt['radius_factor_strings'])}`. Original target radii are unchanged; source radii are `R_i + {receipt['source_radius_increment']}`.",
            "The finite head terms use individual closed-contour Acb arc covers. Each deep tail uses the V2 centered-at-zero bound `1/(n*lambda-|c_i|-R_i_enlarged) + |c_j|`, whose supremum is at the first deep-tail index.",
            "Pole and branch-cut rows use the V2 expressions with the enlarged source radius and are independently re-evaluated here.",
            "",
            "## Per-family detail",
            "",
        ]
    )
    for block in receipt["blocks"]:
        lines.extend(
            [
                f"### {block['label']}",
                "",
                f"Family verdict: **{'PASS' if block['pass'] else 'FAIL'}**; K used: `{block['K_used']}`.",
                "",
                "| branch | certified sup / target-distance upper bound | ratio upper bound | verdict |",
                "|---|---:|---:|---|",
            ]
        )
        for term in block["head_terms"]:
            lines.append(
                f"| finite n={term['n']} M={receipt['M']} arc | {term['certified_sup_upper_bound']} | {term['ratio_upper_bound']} | {'PASS' if term['pass'] else 'FAIL'} |"
            )
        deep = block["deep_tail"]
        if deep is not None:
            lines.append(
                f"| {deep['range']} crude monotone tail | {deep['target_distance_upper']} | {deep['ratio_upper_bound']} | {'PASS' if deep['pass'] else 'FAIL'} |"
            )
            lines.extend(
                [
                    "",
                    f"Deep-tail denominator lower bound: `{deep['denominator_lower_bound']}`; image radius: `{deep['image_ball_radius']}`; target-disc margin: `{deep['target_disc_margin']}`.",
                ]
            )
        pole = next(row for row in receipt["pole_clearance"] if row["block"] == block["block"])
        cut = next(row for row in receipt["branch_cut_clearance"] if row["block"] == block["block"])
        lines.extend(
            [
                "",
                f"Pole `{pole['branch']}` at `{pole['pole_location']}`: margin `{pole['margin']}` â **{'PASS' if pole['pass'] else 'FAIL'}**.",
                f"Branch cut `{cut['expression']}`: margin `{cut['margin']}` â **{'PASS' if cut['pass'] else 'FAIL'}**.",
                "",
            ]
        )
    lines.extend(
        [
            "## Receipt and reproducibility",
            "",
            f"Checkpointed receipt: [{receipt_path.name}]({receipt_path}).",
            "",
            "```bash",
            f"/Users/za/.venvs/farey-rh/bin/python {code_path} \\",
            f"  --sweep-source {receipt['blocks_source']['path']} \\",
            f"  --opt-json {receipt['source_opt_json']} \\",
            f"  --out-dir {receipt_path.parent} \\",
            f"  --precision-bits {receipt['precision_bits']} --M {receipt['M']} \\",
            f"  --K-start {receipt['tail_split']['K_start']} --max-K {receipt['tail_split']['max_K']}",
            "```",
            "",
            f"Source code: [{code_path.name}]({code_path}:1). V2 source used unchanged: `{receipt['v2_source']}`.",
            "",
        ]
    )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.precision_bits != PREC_BITS:
        raise SystemExit(f"precision must be exactly {PREC_BITS} bits for this certification")
    if args.M != M_DEFAULT:
        raise SystemExit(f"M must be exactly {M_DEFAULT} for this certification")
    if args.K_start < 0 or args.max_K < args.K_start:
        raise SystemExit("require 0 <= K-start <= max-K")
    ctx.prec = args.precision_bits

    sweep_source = Path(args.sweep_source).resolve()
    opt_json_path = Path(args.opt_json).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = out_dir / RECEIPT_NAME
    report_path = out_dir / REPORT_NAME

    blocks_raw, blocks_line = v2.v1.load_blocks(sweep_source)
    blocks: list[Block] = [tuple(block) for block in blocks_raw]
    if len(blocks) != 11:
        print(f"BLOCKS count is {len(blocks)}, not 11; exact source list is retained")
    opt_json = json.loads(opt_json_path.read_text(encoding="utf-8"))
    lam = v2.v1.lam_ball()
    points, centers, half, multipliers, original_radii = v2.v1.disc_geometry(lam)
    source_increment = arb(EPSILON_TEXT)
    enlarged_radii = [radius + source_increment for radius in original_radii]

    receipt: dict[str, Any] = {
        "schema": "tb-block-certificates/e1-enlarged",
        "status": "RUNNING",
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": args.precision_bits,
        "M": args.M,
        "q": v2.v1.Q,
        "lambda": arb_text(lam),
        "partition_points": [arb_text(value) for value in points],
        "centers": [arb_text(value) for value in centers],
        "half_widths": [arb_text(value) for value in half],
        "radius_factor_strings": list(v2.v1.RADIUS_MULTIPLIERS),
        "source_radii_original": [arb_text(value) for value in original_radii],
        "source_radii_enlarged": [arb_text(value) for value in enlarged_radii],
        "source_radius_increment": EPSILON_TEXT,
        "target_radii_unchanged": [arb_text(value) for value in original_radii],
        "source_contour": "|z-c_i| = R_i + 0.1",
        "blocks_source": {
            "path": str(sweep_source),
            "assignment_line": blocks_line,
            "count": len(blocks),
            "expected_count": 11,
            "exact_count_check": len(blocks) == 11,
            "blocks": [list(block) for block in blocks],
        },
        "source_opt_json": str(opt_json_path),
        "source_opt_json_loaded": bool(opt_json),
        "opt_json_role": "diagnostic provenance only; no float value enters certification",
        "v2_source": str(Path(v2.__file__).resolve()),
        "tail_split": {
            "K_start": args.K_start,
            "max_K": args.max_K,
            "head_range": "n0..n0+K inclusive, individually arc-certified",
            "deep_range": "n>n0+K",
            "deep_first_index": "n0+K+1",
            "deep_bound": "1/(n*lambda-|c_i|-R_i_enlarged) + |c_j|, centered at 0",
            "deep_supremum_at_first_index": True,
        },
        "blocks": [],
        "pole_clearance": [],
        "branch_cut_clearance": [],
        "checkpoint_trail": [],
    }
    checkpoint_write(
        receipt,
        receipt_path,
        {
            "step": "initialized",
            "status": "RUNNING",
            "completed_families": 0,
            "total_families": len(blocks),
            "partial_results": [],
        },
    )

    raw_ratios: list[tuple[str, int | None, arb]] = []
    for index, block in enumerate(blocks, start=1):
        result, ratios = family_result(
            block,
            centers,
            enlarged_radii,
            original_radii,
            lam,
            args.M,
            args.K_start,
            args.max_K,
        )
        pole_row, cut_row = clearance_for_block(block, centers, enlarged_radii, lam)
        receipt["blocks"].append(result)
        receipt["pole_clearance"].append(pole_row)
        receipt["branch_cut_clearance"].append(cut_row)
        if result["tail"]:
            for term in result["head_terms"]:
                raw_ratios.append((result["label"], term["n"], arb(term["ratio_upper_bound"])))
            deep = result["deep_tail"]
            if deep["ratio_upper_bound"] is not None:
                raw_ratios.append((result["label"], deep["first_n"], arb(deep["ratio_upper_bound"])))
        else:
            term = result["head_terms"][0]
            raw_ratios.append((result["label"], term["n"], arb(term["ratio_upper_bound"])))
        partial_rho = max_ball([value for _label, _n, value in raw_ratios])
        partial_min_ball, partial_min_lower = current_min_margin(
            receipt["pole_clearance"], receipt["branch_cut_clearance"]
        )
        checkpoint_write(
            receipt,
            receipt_path,
            {
                "step": "family_completed",
                "status": "RUNNING",
                "family_index": index,
                "completed_families": index,
                "total_families": len(blocks),
                "family": result["label"],
                "family_pass": result["pass"] and pole_row["pass"] and cut_row["pass"],
                "partial_result": result,
                "pole_clearance": pole_row,
                "branch_cut_clearance": cut_row,
                "rho_hat_so_far": arb_text(partial_rho),
                "minimum_margin_so_far": partial_min_ball,
                "minimum_margin_lower_bound_so_far": partial_min_lower,
            },
        )

    finalize_receipt(receipt, raw_ratios, receipt["pole_clearance"], receipt["branch_cut_clearance"])
    checkpoint_write(
        receipt,
        receipt_path,
        {
            "step": "finalized",
            "status": "FINALIZED",
            "completed_families": len(blocks),
            "total_families": len(blocks),
            "rho_hat_ball": receipt["rho_hat_ball"],
            "rho_hat_upper_bound": receipt["rho_hat_upper_bound"],
            "worst_branch": receipt["worst_branch"],
            "minimum_pole_cut_margin_ball": receipt["minimum_pole_cut_margin_ball"],
            "minimum_pole_cut_margin_lower_bound": receipt["minimum_pole_cut_margin_lower_bound"],
            "certification_verdict": receipt["certification_verdict"],
        },
    )
    report_path.write_text(
        report_text(receipt, Path(__file__).resolve(), receipt_path), encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "receipt": str(receipt_path),
                "report": str(report_path),
                "rho_hat_ball": receipt["rho_hat_ball"],
                "rho_hat_upper_bound": receipt["rho_hat_upper_bound"],
                "worst_branch": receipt["worst_branch"],
                "minimum_pole_cut_margin_ball": receipt["minimum_pole_cut_margin_ball"],
                "minimum_pole_cut_margin_lower_bound": receipt["minimum_pole_cut_margin_lower_bound"],
                "verdict": receipt["certification_verdict"],
                "checkpoint_count": receipt["checkpoint_count"],
            },
            indent=2,
        )
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sweep-source", default=str(DEFAULT_SWEEP_SOURCE))
    parser.add_argument("--opt-json", default=str(DEFAULT_OPT_JSON))
    parser.add_argument("--out-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--precision-bits", type=int, default=PREC_BITS)
    parser.add_argument("--M", type=int, default=M_DEFAULT)
    parser.add_argument("--K-start", type=int, default=K_START_DEFAULT)
    parser.add_argument("--max-K", type=int, default=MAX_K_DEFAULT)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
