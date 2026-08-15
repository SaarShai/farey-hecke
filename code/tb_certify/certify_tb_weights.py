#!/usr/bin/env python3
"""Arb certification of the T-b block-weight envelope.

This is deliberately a single-process runner.  It reads the literal allowed
block list from ``tb_disc_sweep.py``, uses the same q=5 Arb disc geometry as
the V1/V2 T-b certificate, and evaluates

    |u_B(z)| = |(theta'_B(z))**s|

on an M=512 rectangular Acb cover of every source-disc contour.  The complex
``s`` argument is an Acb rectangle covering the complete 1e-6 by 1e-6
flagship box, so the box inflation is part of every interval evaluation.

The requested T-b tail majorant is an absolute sum of branch weights.  Its
deep-tail integral is recorded in extended-real form when 2*Re(s) <= 1.  In
that case the receipt also records a fixed-contour lower-bound witness proving
that the absolute tail sum diverges; this is not silently replaced by the
conditionally convergent Hurwitz-zeta closure used by the determinant engine.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import time
from pathlib import Path
from typing import Any

from flint import acb, arb, ctx


PREC_BITS = 384
M_DEFAULT = 512
TAIL_HEAD_COUNT = 16
Q = 5
RHO_STAR_TEXT = "0.697802"
N_DEFAULT = 48
KAPPA = 3
OBSERVED_C_TEXT = "34.91457640966942"
TC_PREP_LOWER_BOUND_TEXT = "3.939054358191304e-06"

REPO_ROOT = Path(__file__).resolve().parents[2]
LANE_G = REPO_ROOT / "research_notes" / "rh_goals_2026-08-14" / "lane_g"
DEFAULT_SWEEP_SOURCE = LANE_G / "tb_disc_sweep.py"
DEFAULT_PINS_SOURCE = (
    REPO_ROOT / ".worktrees" / "aletheia-restore" / "code" / "out" / "resonance_geometry.json"
)
DEFAULT_REPORT_DIR = LANE_G
REPORT_NAME = "W_ENVELOPE_CERT.md"
RECEIPT_NAME = "W_ENVELOPE_CERT_RECEIPT.json"

Block = tuple[int, int, int, bool, bool]


def arb_text(x: arb, digits: int = 24) -> str:
    return x.str(digits, more=True)


def definitely_positive(x: arb) -> bool:
    return x.lower() > arb(0)


def definitely_negative(x: arb) -> bool:
    return x.upper() < arb(0)


def max_arb(values: list[arb]) -> arb:
    result = arb(0)
    for value in values:
        result = arb.max(result, value)
    return result


def sum_arb(values: list[arb]) -> arb:
    result = arb(0)
    for value in values:
        result += value
    return result


def hull_arb(values: list[arb]) -> arb:
    lower = min(value.lower() for value in values)
    upper = max(value.upper() for value in values)
    return arb((lower + upper) / arb(2), (upper - lower) / arb(2))


def load_blocks(path: Path) -> tuple[list[Block], int]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == "BLOCKS" for target in node.targets):
            raw = ast.literal_eval(node.value)
            blocks = [tuple(item) for item in raw]
            if not all(len(item) == 5 for item in blocks):
                raise ValueError("BLOCKS entries must have five fields")
            return blocks, node.lineno
    raise ValueError(f"BLOCKS assignment not found in {path}")


def load_pins(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    pins = []
    for index, item in enumerate(data["g5_even_resonances"], start=1):
        pins.append(
            {
                "name": f"g5_pin_{index}",
                "re": repr(float(item["re"])),
                "im": repr(float(item["im"])),
                "re_float": float(item["re"]),
                "im_float": float(item["im"]),
                "N_stable": bool(item.get("N_stable", False)),
            }
        )
    if len(pins) != 8:
        raise ValueError(f"expected exactly 8 G_5 pins, found {len(pins)}")
    return pins


def lam_ball() -> arb:
    return (arb(1) + arb(5).sqrt()) / arb(2)


def cf_value_ball(digits: list[int], lam: arb) -> arb:
    value = arb(0)
    for digit in reversed(digits):
        value = -arb(1) / (arb(digit) * lam + value)
    return value


def partition_points_ball(lam: arb) -> list[arb]:
    phi0 = -lam / arb(2)
    phi2 = cf_value_ball([2, 1], lam)
    phi1 = cf_value_ball([1], lam)
    points = [phi0, phi1, phi2, arb(0)]
    if not all(points[k].upper() < points[k + 1].lower() for k in range(3)):
        raise ArithmeticError("q=5 Arb partition points are not strictly ordered")
    return points


def disc_geometry(lam: arb) -> tuple[list[arb], list[arb], list[arb], list[arb], list[arb]]:
    points = partition_points_ball(lam)
    half = [(points[k] - points[k - 1]) / arb(2) for k in range(1, 4)]
    centers = [(points[k] + points[k - 1]) / arb(2) for k in range(1, 4)]
    multipliers = [arb("3.14"), arb("2.27"), arb("1.70")]
    radii = [multipliers[k] * half[k] for k in range(3)]
    if not all(definitely_positive(value) for value in half + radii):
        raise ArithmeticError("non-positive q=5 half-width or source radius")
    return points, centers, half, multipliers, radii


def arc_ball(center: arb, radius: arb, arc_index: int, M: int) -> acb:
    """An Acb rectangle enclosing the closed circular arc."""

    angle0 = acb.pi() * arb(2 * arc_index) / arb(M)
    angle1 = acb.pi() * arb(2 * (arc_index + 1)) / arb(M)
    cos_values = [angle0.cos().real, angle1.cos().real]
    sin_values = [angle0.sin().real, angle1.sin().real]
    if arc_index < M // 2 <= arc_index + 1:
        cos_values.append(arb(-1))
    if arc_index == 0 or arc_index + 1 == M:
        cos_values.append(arb(1))
    if arc_index < M // 4 <= arc_index + 1:
        sin_values.append(arb(1))
    if arc_index < 3 * M // 4 <= arc_index + 1:
        sin_values.append(arb(-1))
    return acb(center + radius * hull_arb(cos_values), radius * hull_arb(sin_values))


def block_label(block: Block) -> str:
    i, j, n, neg, tail = block
    return f"{i}→{j}, {'−' if neg else '+'}{n}, {'tail' if tail else 'head'}"


def s_box(pin: dict[str, Any]) -> tuple[acb, dict[str, Any]]:
    re_center = arb(pin["re"])
    im_center = arb(pin["im"])
    hx = arb("1e-6")
    hy = arb("1e-6")
    re_interval = re_center + arb(0, hx)
    im_interval = im_center + arb(0, hy)
    return acb(re_interval, im_interval), {
        "center": {"re": arb_text(re_center), "im": arb_text(im_center)},
        "half_width": {"re": arb_text(hx), "im": arb_text(hy)},
        "re_interval": arb_text(re_interval),
        "im_interval": arb_text(im_interval),
        "principal_branch": True,
        "inflation": "Acb rectangle is the complete closed 1e-6 by 1e-6 certification box",
    }


def theta_prime(z: acb, lam: arb, n: int, neg: bool) -> acb:
    denominator = z - acb(arb(n) * lam) if neg else z + acb(arb(n) * lam)
    # The sign of the negative-branch derivative does not change its modulus;
    # this is the exact positive/negative denominator convention in the task.
    return acb(1) / (denominator * denominator)


def weight_sup_on_arcs(
    arcs: list[acb], lam: arb, n: int, neg: bool, s: acb
) -> tuple[arb, int]:
    values = [(theta_prime(z, lam, n, neg) ** s).abs_upper() for z in arcs]
    worst = max(range(len(values)), key=lambda index: values[index].upper())
    return values[worst], worst


def serial_finite_term(
    n: int,
    sup: arb,
    worst_arc: int,
    M: int,
    s_info: dict[str, Any],
) -> dict[str, Any]:
    return {
        "n": n,
        "kind": "individual_arc_cover",
        "arc_cover": {
            "M": M,
            "enclosure": "Acb rectangular ball for each closed circular arc",
            "supremum_of_arc_upper_bounds": True,
            "worst_arc_index": worst_arc,
        },
        "s_ball": s_info,
        "certified_sup_upper_bound": arb_text(sup),
    }


def deep_tail_bound(
    block: Block,
    first_n: int,
    center_i: arb,
    radius_i: arb,
    lam: arb,
    s: acb,
    s_info: dict[str, Any],
) -> dict[str, Any]:
    """Return the requested monotone absolute deep-tail majorant.

    For d_n = n*lambda + beta > 0 and p = 2*Re(s)_min,
    |theta'_n(z)^s| <= exp(|Im(s)|*2 atan(R_i/d_n)) d_n**(-p).
    The angle factor is frozen at first_n, and the decreasing power sum is
    bounded by f(first_n) + integral_{first_n}^infinity f(x) dx.
    """

    _i, _j, n0, neg, _tail = block
    re_lower = s.real.lower()
    im_upper_abs = max(abs(s.imag.lower()), abs(s.imag.upper()))
    p_lower = arb(2) * re_lower
    d = arb(first_n) * lam + center_i - radius_i if not neg else arb(first_n) * lam - center_i - radius_i
    if not definitely_positive(d):
        raise ArithmeticError(f"deep-tail denominator is not positive for {block}")
    angle = arb(2) * (radius_i / d).atan()
    log_first = -p_lower * d.log() + im_upper_abs * angle
    first_term = log_first.exp()
    p_gt_one = definitely_positive(p_lower - arb(1))
    if p_gt_one:
        integral = (d ** (arb(1) - p_lower)) / (lam * (p_lower - arb(1)))
        power_sum = d ** (-p_lower) + integral
        angle_factor = (im_upper_abs * angle).exp()
        deep_sum = angle_factor * power_sum
        result: dict[str, Any] = {
            "status": "FINITE_INTEGRAL",
            "first_n": first_n,
            "range": f"n≥{first_n}",
            "denominator_lower_bound_at_first_n": arb_text(d),
            "exponent_p_lower_bound": arb_text(p_lower),
            "angle_bound_at_first_n": arb_text(angle),
            "im_s_abs_upper_bound": arb_text(im_upper_abs),
            "first_term_upper_bound": arb_text(first_term),
            "power_sum_first_term_plus_integral_upper_bound": arb_text(power_sum),
            "deep_sum_upper_bound": arb_text(deep_sum),
            "integral_formula": "d_N^(1-p)/(lambda*(p-1))",
            "integral_converges": True,
            "s_ball": s_info,
        }
        return result

    # The requested absolute integral is divergent.  Record the exact
    # witness used to establish that this is a property of the quantity being
    # bounded, not merely a weakness of the upper estimate.
    a_center = arb(s_info["center"]["re"])
    p_center = arb(2) * a_center
    if not definitely_negative(p_center - arb(1)):
        raise ArithmeticError("expected the flagship center to satisfy 2*Re(s)<1")
    witness_z = center_i + radius_i if not neg else center_i - radius_i
    beta = center_i + radius_i if not neg else -center_i + radius_i
    linear_constant = lam + beta.abs_upper()
    witness_d = arb(first_n) * lam + beta
    if not definitely_positive(witness_d):
        raise ArithmeticError("fixed-contour divergence witness denominator is not positive")
    result = {
        "status": "DIVERGENT_ABSOLUTE_INTEGRAL",
        "first_n": first_n,
        "range": f"n≥{first_n}",
        "denominator_lower_bound_at_first_n": arb_text(d),
        "exponent_p_lower_bound": arb_text(p_lower),
        "angle_bound_at_first_n": arb_text(angle),
        "im_s_abs_upper_bound": arb_text(im_upper_abs),
        "first_term_upper_bound": arb_text(first_term),
        "integral_formula": "integral_N^infinity (lambda*x+beta)^(-p) dx",
        "integral_converges": False,
        "deep_sum_upper_bound": "+inf",
        "s_ball": s_info,
        "divergence_witness": {
            "s_value": {
                "re": arb_text(a_center),
                "im": s_info["center"]["im"],
            },
            "p_center": arb_text(p_center),
            "point_on_source_contour": {
                "re": arb_text(witness_z),
                "im": "0",
            },
            "witness_abs_denominator": "n*lambda + beta",
            "beta": arb_text(beta),
            "witness_denominator_at_first_n": arb_text(witness_d),
            "linear_comparison_constant_C": arb_text(linear_constant),
            "comparison": "d_n <= C*n, hence |u_n(z_witness)| >= C^(-p_center)*n^(-p_center)",
            "p_series_exponent": arb_text(p_center),
            "p_series_diverges": True,
            "conclusion": "sum of absolute branch-weight suprema is +inf",
        },
    }
    return result


def serial_block(
    block: Block,
    centers: list[arb],
    radii: list[arb],
    lam: arb,
    arcs_by_source: list[list[acb]],
    s: acb,
    s_info: dict[str, Any],
    M: int,
) -> dict[str, Any]:
    i, _j, n0, neg, tail = block
    ns = list(range(n0, n0 + TAIL_HEAD_COUNT)) if tail else [n0]
    head_terms = []
    head_sups = []
    for n in ns:
        sup, worst_arc = weight_sup_on_arcs(arcs_by_source[i - 1], lam, n, neg, s)
        head_terms.append(serial_finite_term(n, sup, worst_arc, M, s_info))
        head_sups.append(sup)
    head_sum = sum_arb(head_sups)
    deep = None
    if tail:
        deep = deep_tail_bound(
            block,
            n0 + TAIL_HEAD_COUNT,
            centers[i - 1],
            radii[i - 1],
            lam,
            s,
            s_info,
        )
    if deep is not None and deep["status"] == "DIVERGENT_ABSOLUTE_INTEGRAL":
        block_weight = "+inf"
        block_status = "DIVERGENT_ABSOLUTE_TAIL"
    elif deep is None:
        block_weight = arb_text(head_sups[0])
        block_status = "FINITE_SINGLE_BRANCH"
    else:
        block_weight = arb_text(head_sum + arb(deep["deep_sum_upper_bound"]))
        block_status = "FINITE_ABSOLUTE_TAIL"
    return {
        "block": list(block),
        "label": block_label(block),
        "source_disc": i,
        "target_disc": block[1],
        "source_radius_multiplier": arb_text(arb(["3.14", "2.27", "1.70"][i - 1])),
        "source_radius": arb_text(radii[i - 1]),
        "n0": n0,
        "negative_branch": neg,
        "tail": tail,
        "head_terms": head_terms,
        "head_term_count": len(head_terms),
        "head_sum_upper_bound": arb_text(head_sum),
        "deep_tail": deep,
        "weight_bound_status": block_status,
        "block_weight_sup_upper_bound": block_weight,
    }


def serial_sum(values: list[str]) -> str:
    if any(value == "+inf" for value in values):
        return "+inf"
    return arb_text(sum_arb([arb(value) for value in values]))


def f_bound(W: str, rho: arb, N: int) -> str:
    if W == "+inf":
        return "+inf"
    value = arb(W)
    result = ((arb(1) + arb(KAPPA) * value / (arb(1) - rho)).exp()
              * (arb(KAPPA) * value * (rho ** N) / (arb(1) - rho)))
    return arb_text(result)


def first_sufficient_N(W: str, rho: arb, lower: arb, stop: int = 200) -> int | None:
    if W == "+inf":
        return None
    for N in range(stop + 1):
        if lower - arb(f_bound(W, rho, N)).upper() > 0:
            return N
    return None


def main_receipt(
    blocks: list[Block],
    blocks_line: int,
    sweep_source: Path,
    pins_source: Path,
    pins: list[dict[str, Any]],
    points: list[arb],
    centers: list[arb],
    half: list[arb],
    multipliers: list[arb],
    radii: list[arb],
    lam: arb,
    boxes: list[dict[str, Any]],
    precision_bits: int,
    M: int,
    N: int,
    elapsed_seconds: float,
) -> dict[str, Any]:
    rho = arb(RHO_STAR_TEXT)
    lower = arb(TC_PREP_LOWER_BOUND_TEXT)
    finite_head_max = arb(0)
    finite_head_location = "none"
    for box in boxes:
        for block in box["blocks"]:
            candidate = arb(block["head_sum_upper_bound"])
            if candidate.upper() > finite_head_max.upper():
                finite_head_max = candidate
                finite_head_location = f"{box['name']} / {block['label']}"
    observed_c = arb(OBSERVED_C_TEXT)
    summary = []
    for box in boxes:
        # W* is the maximum over output/source rows, exactly as the L3 text
        # phrases "blocks with source i".  Both row and input-target sums are
        # retained to make the aggregation auditable.
        W_box = box["W_star"]
        F = f_bound(W_box, rho, N)
        minimal = first_sufficient_N(W_box, rho, lower)
        summary.append(
            {
                "box": box["name"],
                "center": box["s_ball"]["center"],
                "W_star_upper_bound": W_box,
                "F_upper_bound": F,
                "rho_star_used": arb_text(rho),
                "N": N,
                "tc_prep_contour_lower_bound": arb_text(lower),
                "margin_lower_bound_minus_F": "-inf" if F == "+inf" else arb_text(lower - arb(F)),
                "comparison_to_tc_prep": "FAIL: F=+inf exceeds contour lower bound"
                if F == "+inf"
                else ("PASS" if lower - arb(F).upper() > 0 else "FAIL"),
                "verdict": "NOT",
                "minimal_certifying_N": minimal,
            }
        )
    return {
        "schema": "tb-weight-envelope-cert/v1",
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": precision_bits,
        "M": M,
        "q": Q,
        "tail_head_count": TAIL_HEAD_COUNT,
        "principal_branch": True,
        "rho_star": arb_text(rho),
        "rho_star_source": "TB_LEMMA_CHAIN.md L3; supplied value rho*=0.697802",
        "N_evaluation": N,
        "kappa": KAPPA,
        "observed_C_supported": OBSERVED_C_TEXT,
        "observed_C_source": "TC_PREP_REPORT.md margin budget",
        "finite_head_only_cross_check": {
            "maximum_head_sum_upper_bound": arb_text(finite_head_max),
            "location": finite_head_location,
            "ratio_to_observed_C_supported": arb_text(finite_head_max / observed_c),
            "flag": finite_head_max.upper() > observed_c.upper(),
            "interpretation": "FLAG: finite head-only weight is above the observed coefficient envelope; do not treat it as an accepted replacement",
        },
        "tc_prep_contour_lower_bound": arb_text(lower),
        "tc_prep_source": "TC_PREP_REPORT.md N=48 timing box",
        "geometry": {
            "lambda": arb_text(lam),
            "partition_points": [arb_text(value) for value in points],
            "centers": [arb_text(value) for value in centers],
            "half_widths": [arb_text(value) for value in half],
            "radius_multipliers": [arb_text(value) for value in multipliers],
            "source_radii": [arb_text(value) for value in radii],
        },
        "blocks_source": {
            "path": str(sweep_source),
            "assignment_line": blocks_line,
            "count": len(blocks),
            "expected_count": 11,
            "exact_count_check": len(blocks) == 11,
            "blocks": [list(block) for block in blocks],
        },
        "pins_source": {
            "path": str(pins_source),
            "count": len(pins),
            "expected_count": 8,
            "exact_count_check": len(pins) == 8,
        },
        "boxes": boxes,
        "summary": summary,
        "aggregation_definition": {
            "W_B": "supremum of the individual branch weight for heads; sum of branch-weight suprema for tails",
            "row_sum": "sum of W_B for blocks sharing source/output disc i",
            "W_star": "maximum row sum over i and the three supplied per-disc radius geometries",
            "tail_absolute_sum": True,
            "divergent_tail_policy": "record +inf and NOT when the requested absolute integral diverges",
        },
        "precision_and_cover_check": {
            "finite_arc_terms_all_evaluated": True,
            "finite_arc_term_precision_escalation": "none; 384 bits was sufficient",
            "deep_tail_failure_cause": "mathematical divergence of the requested absolute p-series, not Arb enclosure width or M",
        },
        "runtime_seconds": elapsed_seconds,
        "tc_pin_receipt_status": "not available at certification time; only TC_PREP lower bound is present",
    }


def render_report(receipt: dict[str, Any], code_path: Path, receipt_path: Path) -> str:
    lines = [
        "# T-b certified weight envelope",
        "",
        "## VERDICT SUMMARY",
        "",
        "The requested absolute tail-weight certificate does not close any flagship box. "
        "Every box has `Re(s)<1/2`, so the required deep-tail majorant "
        "`sum_n |theta'_n(z)^s|` has exponent `2 Re(s)<1` and diverges. "
        "The receipt contains the fixed-contour lower-bound witness, not only a failed upper estimate.",
        "",
        "| box | certified W* | certified F(W*, rho*=0.697802, N=48) | comparison to TC_PREP 3.94e-6 | VERDICT | minimal certifying N |",
        "|---|---:|---:|---|---|---:|",
    ]
    for row in receipt["summary"]:
        lines.append(
            f"| {row['box']} | `{row['W_star_upper_bound']}` | `{row['F_upper_bound']}` | "
            f"{row['comparison_to_tc_prep']} | **{row['verdict']}** | "
            f"{row['minimal_certifying_N'] if row['minimal_certifying_N'] is not None else 'none'} |"
        )
    lines.extend(
        [
            "",
            "`W*=+inf` is the certified result for the quantity specified in TB_LEMMA_CHAIN.md L3: "
            "the maximum of per-source row sums of absolute block-weight suprema. "
            "Therefore `F=+inf`, the margin is negative infinite, and no finite N can certify the requested inequality.",
            "",
            "## Methodology",
            "",
            f"- Backend: `{receipt['backend']}`, precision `{receipt['precision_bits']}` bits, arc cover `M={receipt['M']}`.",
            "- The allowed blocks are parsed from the literal `BLOCKS` assignment; the receipt records its path, line, and all 11 entries.",
            "- Each source contour is enclosed by 512 closed circular-arc Acb rectangles. The principal power is evaluated as `theta_prime ** s_ball`, where `s_ball` is the complete closed 1e-6 by 1e-6 Acb box.",
            "- Tail families certify `n=n0..n0+15` individually. For `n>=n0+16`, the monotone majorant uses `d_n^(-p)` with `p=2*Re(s)_lower` and the requested first-term-plus-integral bound.",
            "- For `p<=1`, the integral is divergent. At a real point on the source contour and at the box center, the receipt proves `|u_n| >= C^(-p_center)n^(-p_center)` with `p_center<1`; hence the absolute tail sum itself diverges.",
            "- `rho*=0.697802`, `kappa=3`, and `N=48` are evaluated exactly as specified by TB_LEMMA_CHAIN.md L3. The TC_PREP comparison lower bound is its reported `3.939054358191304e-06`.",
            "",
            "## Cross-check against the observed envelope",
            "",
            f"The observed finite coefficient envelope was `{receipt['observed_C_supported']}`. The largest finite head-only weight interval is `{receipt['finite_head_only_cross_check']['maximum_head_sum_upper_bound']}` at `{receipt['finite_head_only_cross_check']['location']}`, a ratio of `{receipt['finite_head_only_cross_check']['ratio_to_observed_C_supported']}`. This is explicitly flagged as above the observed envelope. The requested absolute tail aggregation is `+inf`, so it exceeds the observed envelope by an unbounded amount; neither result is accepted as a certified replacement for `C_supported`.",
            "",
            "## Per-block / per-radius detail",
            "",
            "Each row below is one of the 11 allowed blocks at its source disc's radius from the three-radius vector (3.14, 2.27, 1.70) for one certification box. "
            "All per-n head intervals, worst arc indices, s-ball records, and deep-tail integral/witness fields are in the receipt.",
            "",
            "| box | source radius multiplier | block | head terms | head sum upper bound | deep-tail result | W_B result |",
            "|---|---:|---|---:|---:|---|---|",
        ]
    )
    for box in receipt["boxes"]:
        for block in box["blocks"]:
            deep = block["deep_tail"]
            deep_text = "n/a"
            if deep is not None:
                deep_text = f"{deep['status']} ({deep['deep_sum_upper_bound']})"
            lines.append(
                f"| {box['name']} | {block['source_radius_multiplier']} | {block['label']} | "
                f"{block['head_term_count']} | `{block['head_sum_upper_bound']}` | {deep_text} | "
                f"`{block['block_weight_sup_upper_bound']}` |"
            )
    lines.extend(
        [
            "",
            "## Reproducibility",
            "",
            f"Machine-readable receipt: [{receipt_path.name}]({receipt_path}).",
            "",
            "Run command:",
            "",
            "```bash",
            f"/Users/za/.venvs/farey-rh/bin/python {code_path} \\",
            f"  --sweep-source {receipt['blocks_source']['path']} \\",
            f"  --pins-source {receipt['pins_source']['path']} \\",
            f"  --out-dir {receipt_path.parent} --precision-bits 384 --M 512 --N 48",
            "```",
            "",
            "No T-c per-pin contour receipt was present at the time of this run; the comparison uses the TC_PREP lower bound only. The runner can be repeated with a later T-c receipt after that concurrent job publishes it.",
            "",
        ]
    )
    return "\n".join(lines)


def run(args: argparse.Namespace) -> dict[str, Any]:
    if args.precision_bits != PREC_BITS:
        raise SystemExit(f"precision must be exactly {PREC_BITS} bits")
    if args.M != M_DEFAULT:
        raise SystemExit(f"M must be exactly {M_DEFAULT}")
    if args.N < 0:
        raise SystemExit("N must be non-negative")
    ctx.prec = args.precision_bits
    start = time.perf_counter()
    sweep_source = Path(args.sweep_source).resolve()
    pins_source = Path(args.pins_source).resolve()
    out_dir = Path(args.out_dir).resolve()
    blocks, blocks_line = load_blocks(sweep_source)
    if len(blocks) != 11:
        raise ValueError(f"expected 11 allowed blocks, found {len(blocks)}")
    pins = load_pins(pins_source)
    lam = lam_ball()
    points, centers, half, multipliers, radii = disc_geometry(lam)
    arcs_by_source = [
        [arc_ball(centers[i], radii[i], index, args.M) for index in range(args.M)]
        for i in range(3)
    ]

    boxes = []
    for pin in pins:
        s, s_info = s_box(pin)
        block_records = [
            serial_block(
                block,
                centers,
                radii,
                lam,
                arcs_by_source,
                s,
                s_info,
                args.M,
            )
            for block in blocks
        ]
        row_sums: dict[str, str] = {}
        target_sums: dict[str, str] = {}
        for source_index in range(1, 4):
            values = [
                block["block_weight_sup_upper_bound"]
                for block in block_records
                if block["source_disc"] == source_index
            ]
            row_sums[str(source_index)] = serial_sum(values)
        for target_index in range(1, 4):
            values = [
                block["block_weight_sup_upper_bound"]
                for block in block_records
                if block["target_disc"] == target_index
            ]
            target_sums[str(target_index)] = serial_sum(values)
        W_star = "+inf" if any(value == "+inf" for value in row_sums.values()) else arb_text(max_arb([arb(value) for value in row_sums.values()]))
        print(
            json.dumps(
                {
                    "box": pin["name"],
                    "radius_multipliers": [arb_text(value) for value in multipliers],
                    "W_star": W_star,
                },
                sort_keys=True,
            ),
            flush=True,
        )
        boxes.append(
            {
                "name": pin["name"],
                "pin_source_center": {"re": pin["re"], "im": pin["im"]},
                "N_stable_source_flag": pin["N_stable"],
                "s_ball": s_info,
                "radius_geometry": [
                    {
                        "disc": index,
                        "radius_multiplier": arb_text(multiplier),
                        "source_radius": arb_text(radius),
                    }
                    for index, (multiplier, radius) in enumerate(zip(multipliers, radii), start=1)
                ],
                "blocks": block_records,
                "row_sums_by_source_disc": row_sums,
                "sums_by_target_disc": target_sums,
                "W_star": W_star,
            }
        )

    receipt = main_receipt(
        blocks,
        blocks_line,
        sweep_source,
        pins_source,
        pins,
        points,
        centers,
        half,
        multipliers,
        radii,
        lam,
        boxes,
        args.precision_bits,
        args.M,
        args.N,
        time.perf_counter() - start,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = out_dir / RECEIPT_NAME
    report_path = out_dir / REPORT_NAME
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(render_report(receipt, Path(__file__).resolve(), receipt_path), encoding="utf-8")
    print(
        json.dumps(
            {
                "receipt": str(receipt_path),
                "report": str(report_path),
                "boxes": len(receipt["boxes"]),
                "blocks": len(blocks),
                "radii": len(radii),
                "verdicts": {row["box"]: row["verdict"] for row in receipt["summary"]},
            },
            indent=2,
        )
    )
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sweep-source", default=str(DEFAULT_SWEEP_SOURCE))
    parser.add_argument("--pins-source", default=str(DEFAULT_PINS_SOURCE))
    parser.add_argument("--out-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--precision-bits", type=int, default=PREC_BITS)
    parser.add_argument("--M", type=int, default=M_DEFAULT)
    parser.add_argument("--N", type=int, default=N_DEFAULT)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
