#!/usr/bin/env python3
"""Arb certification of the q=5 T-b disc block bounds.

The source reconnaissance uses float64.  This module deliberately does not
reuse its floating-point geometry: the q=5 partition construction from
``zeta_mayer_rosen.partition_points`` is reproduced with Arb, and every
reported enclosure is formed with Arb/Acb operations.

For a head branch, each of the M contour arcs is enclosed by an Acb rectangle
formed from Arb endpoint/critical-point hulls for its Cartesian coordinates.
For a tail family, the finite n0 arc is checked with the same cover and the
all-n bound requested by T-b is used for the certified family supremum.
"""

from __future__ import annotations

import argparse
import ast
import cmath
import json
import math
from pathlib import Path
from typing import Any

from flint import acb, arb, ctx


PREC_BITS = 256
M_DEFAULT = 512
Q = 5
RADIUS_MULTIPLIERS = ("3.14", "2.27", "1.70")
DEFAULT_SWEEP_SOURCE = Path(
    "/Users/za/Documents/farey-hecke/research_notes/"
    "rh_goals_2026-08-14/lane_g/tb_disc_sweep.py"
)
DEFAULT_OPT_JSON = Path(
    "/Users/za/Documents/farey-hecke/research_notes/"
    "rh_goals_2026-08-14/lane_g/tb_disc_opt.json"
)
DEFAULT_REPORT_DIR = Path(
    "/Users/za/Documents/farey-hecke/research_notes/"
    "rh_goals_2026-08-14/lane_g"
)
LEAN_PATTERN_SOURCE = (
    "projects/aristotle_dispatch_v17/TailBranchBound.lean:"
    "image_in_disc_with_margin"
)


def arb_text(x: arb, digits: int = 24) -> str:
    """A parseable Arb enclosure, not a binary float rendering."""

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


def hull_arb(values: list[arb]) -> arb:
    """Return an Arb interval containing the union of real Arb intervals."""

    lower = min((value.lower() for value in values))
    upper = max((value.upper() for value in values))
    return arb((lower + upper) / arb(2), (upper - lower) / arb(2))


def load_blocks(path: Path) -> tuple[list[tuple[int, int, int, bool, bool]], int]:
    """Read the literal BLOCKS assignment from the requested source file."""

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


def lam_ball() -> arb:
    """The q=5 algebraic value (1 + sqrt(5))/2 in Arb."""

    return (arb(1) + arb(5).sqrt()) / arb(2)


def cf_value_ball(digits: list[int], lam: arb) -> arb:
    x = arb(0)
    for digit in reversed(digits):
        x = -arb(1) / (arb(digit) * lam + x)
    return x


def partition_points_ball(lam: arb) -> list[arb]:
    """q=5 counterpart of zeta_mayer_rosen.partition_points(5)."""

    # zeta_mayer_rosen.py uses hq=1, kappa=3 and the odd-q finite CF rules.
    phi0 = -lam / arb(2)
    phi2 = cf_value_ball([2, 1], lam)
    phi1 = cf_value_ball([1], lam)
    phi3 = arb(0)
    points = [phi0, phi1, phi2, phi3]
    if not all(points[k].upper() < points[k + 1].lower() for k in range(3)):
        raise ArithmeticError("q=5 Arb partition points are not strictly ordered")
    return points


def disc_geometry(lam: arb) -> tuple[list[arb], list[arb], list[arb], list[arb], list[arb]]:
    points = partition_points_ball(lam)
    half = [(points[k] - points[k - 1]) / arb(2) for k in range(1, 4)]
    centers = [(points[k] + points[k - 1]) / arb(2) for k in range(1, 4)]
    multipliers = [arb(value) for value in RADIUS_MULTIPLIERS]
    radii = [multipliers[k] * half[k] for k in range(3)]
    if not all(definitely_positive(value) for value in half + radii):
        raise ArithmeticError("non-positive q=5 half-width or source radius")
    return points, centers, half, multipliers, radii


def arc_ball(center: arb, radius: arb, arc_index: int, M: int) -> acb:
    """Return an Acb rectangle containing one closed circular contour arc."""

    # Arc k is [2*pi*k/M, 2*pi*(k+1)/M].  Endpoint/critical-point hulls are
    # tighter than a generic midpoint +/- R*pi/M box while remaining exact:
    # the only interior extrema of cos and sin are at multiples of pi/2.
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
    cos_hull = hull_arb(cos_values)
    sin_hull = hull_arb(sin_values)
    return acb(center + radius * cos_hull, radius * sin_hull)


def theta_ball(z: acb, lam: arb, n: int, neg: bool) -> acb:
    if neg:
        return acb(1) / (z - acb(arb(n) * lam))
    return -acb(1) / (z + acb(arb(n) * lam))


def contour_sup(
    center_i: arb,
    radius_i: arb,
    center_j: arb,
    lam: arb,
    n: int,
    neg: bool,
    M: int,
) -> arb:
    values: list[arb] = []
    target = acb(center_j)
    for arc_index in range(M):
        z_arc = arc_ball(center_i, radius_i, arc_index, M)
        image = theta_ball(z_arc, lam, n, neg)
        values.append((image - target).abs_upper())
    return max_arb(values)


def tail_dominating_bound(
    center_i: arb,
    radius_i: arb,
    center_j: arb,
    radius_j: arb,
    lam: arb,
    n0: int,
) -> tuple[arb, arb, arb, arb]:
    """Requested all-n tail bound plus the image-ball target check.

    The denominator is n0*lambda - |c_i| - R_i.  For n >= n0 it only grows,
    so 1/denominator dominates every branch modulus.  The target distance is
    bounded by |image| + |c_j|, exactly the triangle-inequality pattern in
    TailBranchBound.lean:image_in_disc_with_margin.
    """

    denominator = arb(n0) * lam - center_i.abs_upper() - radius_i
    if not definitely_positive(denominator):
        raise ArithmeticError("tail denominator is not certified positive")
    image_radius = arb(1) / denominator
    target_distance = image_radius + center_j.abs_upper()
    target_margin = radius_j - target_distance
    return denominator, image_radius, target_distance, target_margin


def branch_pole(centers_i: arb, lam: arb, n: int, neg: bool) -> arb:
    return arb(n) * lam if neg else -arb(n) * lam


def pole_margin(center_i: arb, radius_i: arb, pole: arb) -> arb:
    distance = (acb(pole) - acb(center_i)).abs_lower()
    return distance - radius_i


def branch_cut_margin(center_i: arb, radius_i: arb, lam: arb, n: int, neg: bool) -> arb:
    if neg:
        # Re(n*lambda - z) is minimized at Re(z)=c_i+R_i.
        return arb(n) * lam - center_i - radius_i
    # Re(z+n*lambda) is minimized at Re(z)=c_i-R_i.
    return center_i + arb(n) * lam - radius_i


def block_label(block: tuple[int, int, int, bool, bool]) -> str:
    i, j, n, neg, tail = block
    sign = "-" if neg else "+"
    family = "tail" if tail else "head"
    return f"{i}->{j}, {sign}{n} ({family})"


def float_recon(
    centers: list[arb],
    half: list[arb],
    multipliers: list[arb],
    lam: arb,
    blocks: list[tuple[int, int, int, bool, bool]],
) -> list[dict[str, Any]]:
    """Diagnostic-only reproduction of the float reconnaissance formula.

    It is deliberately kept out of all certified values and report tables.
    """

    c = [float(x.mid()) for x in centers]
    h = [float(x.mid()) for x in half]
    a = [float(x.mid()) for x in multipliers]
    l = float(lam.mid())
    samples = [cmath.exp(2j * math.pi * k / 2048) for k in range(2048)]
    result: list[dict[str, Any]] = []
    for block in blocks:
        i, j, n0, neg, tail = block
        ns = range(n0, 60) if tail else (n0,)
        best = 0.0
        n_worst = n0
        n0_best = 0.0
        for n in ns:
            current = 0.0
            for unit in samples:
                z = c[i - 1] + a[i - 1] * h[i - 1] * unit
                image = 1.0 / (z - n * l) if neg else -1.0 / (z + n * l)
                current = max(current, abs(image - c[j - 1]))
            ratio = current / (a[j - 1] * h[j - 1])
            if n == n0:
                n0_best = current
            if ratio > best:
                best, n_worst = ratio, n
        result.append(
            {
                "block": list(block),
                "float_sup_sampled": best * (a[j - 1] * h[j - 1]),
                "float_ratio_sampled": best,
                "float_n_worst": n_worst,
                "float_n0_sup_sampled": n0_best,
            }
        )
    return result


def compare_arc_diagnostics(
    rows: list[dict[str, Any]],
    float_rows: list[dict[str, Any]],
    tolerance: float = 5.0e-4,
) -> list[dict[str, Any]]:
    by_block = {tuple(row["block"]): row for row in float_rows}
    comparisons = []
    for row in rows:
        key = tuple(row["block"])
        frow = by_block[key]
        cert_arc = float(row["arc_n0_sup"].upper())
        float_arc = frow["float_n0_sup_sampled"]
        delta = abs(cert_arc - float_arc)
        comparisons.append(
            {
                "block": row["block"],
                "comparison": "Arb 512-arc n0 bound vs float 2048-point n0 sample",
                "float_arc_n0_sup_sampled": float_arc,
                "arb_arc_n0_upper_as_float_diagnostic": cert_arc,
                "absolute_difference": delta,
                "tolerance": tolerance,
                "flag": delta > tolerance,
            }
        )
    return comparisons


def make_receipt(
    blocks: list[tuple[int, int, int, bool, bool]],
    blocks_line: int,
    sweep_source: Path,
    opt_json_path: Path,
    opt_json: dict[str, Any],
    points: list[arb],
    centers: list[arb],
    half: list[arb],
    multipliers: list[arb],
    radii: list[arb],
    lam: arb,
    rows: list[dict[str, Any]],
    pole_rows: list[dict[str, Any]],
    cut_rows: list[dict[str, Any]],
    float_rows: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    precision_bits: int,
    M: int,
) -> dict[str, Any]:
    rho = max_arb([row["ratio"] for row in rows])
    worst = rows[0]
    for row in rows[1:]:
        if row["ratio"].upper() > worst["ratio"].upper():
            worst = row
    threshold = arb("0.70")
    tail_rows = [row for row in rows if row["tail"]]
    all_poles_clear = all(row["pass"] for row in pole_rows)
    all_cuts_clear = all(row["pass"] for row in cut_rows)
    all_tail_inside = all(row["tail_inside"] for row in tail_rows)
    return {
        "schema": "tb-block-certificates/v1",
        "backend": "python-flint Arb/Acb ball arithmetic",
        "precision_bits": precision_bits,
        "M": M,
        "q": Q,
        "lambda": arb_text(lam),
        "partition_points": [arb_text(x) for x in points],
        "centers": [arb_text(x) for x in centers],
        "half_widths": [arb_text(x) for x in half],
        "radius_multipliers": [arb_text(x) for x in multipliers],
        "source_radii": [arb_text(x) for x in radii],
        "blocks_source": {
            "path": str(sweep_source),
            "assignment_line": blocks_line,
            "count": len(blocks),
            "expected_count": 11,
            "exact_count_check": len(blocks) == 11,
            "blocks": [list(block) for block in blocks],
        },
        "blocks": [
            {
                "block": row["block"],
                "label": row["label"],
                "tail": row["tail"],
                "n0": row["n0"],
                "arc_cover": row["arc_cover"],
                "arc_n0_sup": arb_text(row["arc_n0_sup"]),
                "tail_denominator_at_n0": (
                    arb_text(row["tail_denominator"]) if row["tail"] else None
                ),
                "tail_image_radius": (
                    arb_text(row["tail_image_radius"]) if row["tail"] else None
                ),
                "tail_target_distance_upper": (
                    arb_text(row["tail_target_distance"]) if row["tail"] else None
                ),
                "tail_image_ball_margin": (
                    arb_text(row["tail_margin"]) if row["tail"] else None
                ),
                "tail_image_ball_inside_with_margin": (
                    row["tail_inside"] if row["tail"] else None
                ),
                "certified_sup_upper_bound": arb_text(row["sup"]),
                "ratio_upper_bound": arb_text(row["ratio"]),
                "ratio_less_than_0_70": definitely_negative(row["ratio"] - arb("0.70")),
            }
            for row in rows
        ],
        "rho_star": arb_text(rho),
        "rho_star_upper_bound": arb_text(rho.upper()),
        "worst_block": worst["block"],
        "threshold_0_70": arb_text(threshold),
        "rho_less_than_0_70": definitely_negative(rho - threshold),
        "pole_clearance": pole_rows,
        "branch_cut_clearance": cut_rows,
        "tail_pattern_source": LEAN_PATTERN_SOURCE,
        "tail_pattern": (
            "|theta_pm_n(z)| <= 1/(n*lambda-|c_i|-R_i), n>=n0; "
            "then |w-c_j| <= |w|+|c_j|"
        ),
        "all_pole_clearances_pass": all_poles_clear,
        "all_branch_cut_clearances_pass": all_cuts_clear,
        "all_tail_image_balls_inside_with_margin": all_tail_inside,
        "float_recon_diagnostic_only": {
            "source_opt_json": str(opt_json_path),
            "source_opt_json_has_per_block_results": any(
                key in opt_json for key in ("results", "blocks", "per_block")
            ),
            "comparison_performed": True,
            "arc_comparisons": [
                {
                    "block": item["block"],
                    "flag": item["flag"],
                    "status": (
                        "FLAGGED_OVER_DIAGNOSTIC_TOLERANCE"
                        if item["flag"]
                        else "WITHIN_DIAGNOSTIC_TOLERANCE"
                    ),
                }
                for item in comparisons
            ],
            "note": "Float samples are not used in any certified value or verdict.",
        },
        "certification_verdict": (
            "PASS_RHO_LT_0.70"
            if definitely_negative(rho - threshold)
            else "FAIL_RHO_THRESHOLD_REPORT_TRUE_CERTIFIED_VALUES"
        ),
    }


def report_text(receipt: dict[str, Any], code_path: Path, receipt_path: Path) -> str:
    def label(block: list[Any]) -> str:
        i, j, n, neg, tail = block
        return f"{i}→{j}, {'−' if neg else '+'}{n}, {'tail' if tail else 'head'}"

    over_threshold = [
        label(block["block"])
        for block in receipt["blocks"]
        if not block["ratio_less_than_0_70"]
    ]
    verdict_suffix = (
        "PASS: < 0.70)"
        if receipt["rho_less_than_0_70"]
        else "WORSE THAN 0.70: true Arb result reported; blocks over threshold: "
        + ", ".join(over_threshold)
        + ")"
    )
    lines = [
        f"certified rho* = {receipt['rho_star']} (upper-bound object; "
        + verdict_suffix,
        "",
        "## 2. Certified block bounds",
        "",
        "| block | certified sup |θ_n(z)−c_j| upper bound | ratio to a_j·h_j |",
        "|---|---:|---:|",
    ]
    for block in receipt["blocks"]:
        lines.append(
            f"| {label(block['block'])} | {block['certified_sup_upper_bound']} | "
            f"{block['ratio_upper_bound']} |"
        )
    lines.extend(
        [
            "",
            "Tail rows use the requested all-n dominating inequality; the `arc_n0_sup` "
            "field in the receipt is the independent M=512 contour check at n0.",
            "The centered-at-zero tail image-ball inclusion check is recorded with its "
            "certified margin in the receipt; it is not silently replaced by the tighter "
            "pointwise contour value.",
            "",
            "## 3. Pole clearance",
            "",
            "The pole margin is the certified distance from the pole to the closed source "
            "disc: `|pole−c_i|−R_i`. For a tail row, the displayed n0 pole is the "
            "closest pole and the same positive margin holds for every n≥n0.",
            "",
            "| block | used branch | pole location | margin to closed source disc | verdict |",
            "|---|---|---:|---:|---|",
        ]
    )
    for row in receipt["pole_clearance"]:
        lines.append(
            f"| {label(row['block'])} | {row['branch']} | {row['pole_location']} | "
            f"{row['margin']} | {'PASS' if row['pass'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "## 4. Branch-cut clearance",
            "",
            "For positive branches the table gives the lower bound for "
            "`Re(z+nλ)`; for negative branches it gives the lower bound for "
            "`Re(nλ−z)`. Tail rows use n0, and the expression increases with n.",
            "",
            "| block | branch-cut expression | certified lower-bound interval | verdict |",
            "|---|---|---:|---|",
        ]
    )
    for row in receipt["branch_cut_clearance"]:
        lines.append(
            f"| {label(row['block'])} | `{row['expression']}` | {row['margin']} | "
            f"{'PASS' if row['pass'] else 'FAIL'} |"
        )
    lines.extend(
        [
            "",
            "## 5. Receipt JSON",
            "",
            "Float reconciliation is diagnostic-only: the input `tb_disc_opt.json` "
            "contains an overall reconnaissance value but no per-block result list. "
            + (
                "No M=512 n0 arc comparison exceeded the configured diagnostic tolerance. "
                if not any(item["flag"] for item in receipt["float_recon_diagnostic_only"]["arc_comparisons"])
                else "The receipt flags the following n0 arc comparisons: "
                + ", ".join(label(item["block"]) for item in receipt["float_recon_diagnostic_only"]["arc_comparisons"] if item["flag"])
                + "."
            ),
            "The final tail-family values are intentionally compared against the tail "
            "inequality, not against the pointwise float sample.",
            "",
            f"Standalone receipt: [{receipt_path.name}]({receipt_path}).",
            "",
            "```json",
            json.dumps(receipt, indent=2, sort_keys=True),
            "```",
            "",
            "## 6. Code listing/reference",
            "",
            f"The executable Arb certifier is [{code_path.name}]({code_path}:1). "
            "Its `arc_ball`, `contour_sup`, `tail_dominating_bound`, "
            "`pole_margin`, and `branch_cut_margin` functions are the code paths "
            "that generated this receipt. The tail inclusion proof pattern is "
            f"cited at `{LEAN_PATTERN_SOURCE}`.",
            "",
            "```python",
            "# Exact entry point used to generate this report",
            "# /Users/za/.venvs/farey-rh/bin/python code/tb_certify/certify_tb_blocks.py \\",
            f"#   --sweep-source {receipt['blocks_source']['path']} \\",
            f"#   --opt-json {receipt['float_recon_diagnostic_only']['source_opt_json']} \\",
            f"#   --out-dir {receipt_path.parent}",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def run(args: argparse.Namespace) -> dict[str, Any]:
    ctx.prec = args.precision_bits
    sweep_source = Path(args.sweep_source).resolve()
    opt_json_path = Path(args.opt_json).resolve()
    out_dir = Path(args.out_dir).resolve()
    blocks, blocks_line = load_blocks(sweep_source)
    if len(blocks) != 11:
        count_note = f"BLOCKS count is {len(blocks)}, not 11; certifying exact source list."
        print(count_note)
    opt_json = json.loads(opt_json_path.read_text(encoding="utf-8"))
    lam = lam_ball()
    points, centers, half, multipliers, radii = disc_geometry(lam)
    M = args.M

    rows: list[dict[str, Any]] = []
    pole_rows: list[dict[str, Any]] = []
    cut_rows: list[dict[str, Any]] = []
    for block in blocks:
        i, j, n0, neg, tail = block
        ci, cj = centers[i - 1], centers[j - 1]
        ri, rj = radii[i - 1], radii[j - 1]
        arc_sup = contour_sup(ci, ri, cj, lam, n0, neg, M)
        denominator = image_radius = target_distance = tail_margin = None
        tail_inside = None
        if tail:
            denominator, image_radius, target_distance, tail_margin = tail_dominating_bound(
                ci, ri, cj, rj, lam, n0
            )
            certified_sup = arb.max(arc_sup, target_distance)
            tail_inside = definitely_positive(tail_margin)
        else:
            certified_sup = arc_sup
        ratio = certified_sup / rj
        row = {
            "block": list(block),
            "label": block_label(block),
            "tail": tail,
            "n0": n0,
            "arc_cover": {"M": M, "arc_enclosure": "Acb rectangular ball"},
            "arc_n0_sup": arc_sup,
            "tail_denominator": denominator,
            "tail_image_radius": image_radius,
            "tail_target_distance": target_distance,
            "tail_margin": tail_margin,
            "tail_inside": tail_inside,
            "sup": certified_sup,
            "ratio": ratio,
        }
        rows.append(row)

        pole = branch_pole(ci, lam, n0, neg)
        margin = pole_margin(ci, ri, pole)
        pole_rows.append(
            {
                "block": list(block),
                "branch": f"theta_{'-' if neg else ''}{n0}" + (f" (n≥{n0})" if tail else ""),
                "pole_location": arb_text(pole),
                "margin": arb_text(margin),
                "pass": definitely_positive(margin),
            }
        )

        cut_margin = branch_cut_margin(ci, ri, lam, n0, neg)
        cut_rows.append(
            {
                "block": list(block),
                "expression": (
                    f"Re(nλ−z), n≥{n0}" if neg else f"Re(z+nλ), n≥{n0}"
                ),
                "margin": arb_text(cut_margin),
                "pass": definitely_positive(cut_margin),
            }
        )

    float_rows = float_recon(centers, half, multipliers, lam, blocks)
    comparisons = compare_arc_diagnostics(rows, float_rows)
    receipt = make_receipt(
        blocks,
        blocks_line,
        sweep_source,
        opt_json_path,
        opt_json,
        points,
        centers,
        half,
        multipliers,
        radii,
        lam,
        rows,
        pole_rows,
        cut_rows,
        float_rows,
        comparisons,
        args.precision_bits,
        M,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    receipt_path = out_dir / "TB_BLOCK_CERTIFICATES_RECEIPT.json"
    report_path = out_dir / "TB_BLOCK_CERTIFICATES.md"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(
        report_text(receipt, Path(__file__).resolve(), receipt_path), encoding="utf-8"
    )
    print(json.dumps({"receipt": str(receipt_path), "report": str(report_path), "rho_star": receipt["rho_star"], "verdict": receipt["certification_verdict"]}, indent=2))
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sweep-source", default=str(DEFAULT_SWEEP_SOURCE))
    parser.add_argument("--opt-json", default=str(DEFAULT_OPT_JSON))
    parser.add_argument("--out-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--precision-bits", type=int, default=PREC_BITS)
    parser.add_argument("--M", type=int, default=M_DEFAULT)
    args = parser.parse_args()
    if args.M != M_DEFAULT:
        raise SystemExit(f"M must be exactly {M_DEFAULT} for this certification")
    run(args)


if __name__ == "__main__":
    main()
