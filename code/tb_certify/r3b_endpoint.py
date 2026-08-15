"""Enlarged-disc Cauchy bounds for the retained-column output tails.

This module consumes the immutable TB V2 clearances.  For each atomic block it
chooses an enlarged output/source disc strictly inside the certified pole and
branch-cut margins, bounds the block columns on that enlarged contour, and
converts those bounds into omitted normalized-output coefficient tails.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable

from flint import acb, arb, ctx


CODE_DIR = Path(__file__).resolve().parent
WORKTREE_ROOT = CODE_DIR.parents[1]
TC_DIR = WORKTREE_ROOT / "code" / "tc_rerun"
sys.path.insert(0, str(CODE_DIR))
sys.path.insert(0, str(TC_DIR))

import certify_tb_blocks as arc_helper  # noqa: E402
import tc_rerun as source_builder  # noqa: E402


EXACT_FACTORS = ("3.14", "2.27", "1.70")
ENLARGEMENT_MARGIN_DIVISOR = 4


def arb_text(value: arb, digits: int = 100) -> str:
    return value.str(digits, more=True)


def definitely_positive(value: arb) -> bool:
    return value.lower() > arb(0)


def definitely_less(left: arb, right: arb) -> bool:
    return left.upper() < right.lower()


def max_arb(values: list[arb]) -> arb:
    if not values:
        raise ValueError("max_arb requires values")
    result = values[0]
    for value in values[1:]:
        result = arb.max(result, value)
    return result


def flagship_s_box() -> acb:
    return acb(
        arb("0.4538951800749447") + arb(0, arb("1e-6")),
        arb("5.7635372417301305") + arb(0, arb("1e-6")),
    )


def _clearance_map(rows: list[dict[str, Any]]) -> dict[tuple[Any, ...], arb]:
    return {tuple(row["block"]): arb(row["margin"]).lower() for row in rows}


def derive_enlarged_discs(tb_v2: dict[str, Any]) -> dict[tuple[Any, ...], dict[str, arb]]:
    """Use one quarter of each certified clearance as enlargement slack."""

    radii = [arb(value) for value in tb_v2["source_radii"]]
    pole = _clearance_map(tb_v2["pole_clearance"])
    branch_cut = _clearance_map(tb_v2["branch_cut_clearance"])
    result: dict[tuple[Any, ...], dict[str, arb]] = {}
    for row in tb_v2["blocks"]:
        block = tuple(row["block"])
        i = int(block[0])
        clearance = arb.min(pole[block], branch_cut[block]).lower()
        if not definitely_positive(clearance):
            raise ArithmeticError(f"nonpositive source clearance for {block}")
        original = radii[i - 1].upper()
        enlargement = (clearance / arb(ENLARGEMENT_MARGIN_DIVISOR)).lower()
        enlarged = (original + enlargement).lower()
        eta = (original / enlarged).upper()
        remaining = (clearance - enlargement).lower()
        if not definitely_less(eta, arb(1)) or not definitely_positive(remaining):
            raise ArithmeticError(f"invalid enlarged disc for {block}")
        result[block] = {
            "original_radius": original,
            "certified_clearance": clearance,
            "enlargement": enlargement,
            "enlarged_radius": enlarged,
            "remaining_clearance": remaining,
            "eta": eta,
        }
    return result


def _tail_phi_zero(s: acb, z: acb, lam: arb, n0: int, neg: bool) -> acb:
    a0 = acb(n0) + (-z / lam if neg else z / lam)
    return (lam * lam) ** (-s) * (2 * s).zeta(a0)


def _deep_first_moment(
    s: acb,
    center_i: arb,
    enlarged_radius: arb,
    radius_j: arb,
    lam: arb,
    first_n: int,
    neg: bool,
    center_ratio: arb,
) -> tuple[arb, arb, dict[str, Any]]:
    sigma_lower = s.real.lower()
    exponent = (arb(2) * sigma_lower).lower()
    denominator = (
        arb(first_n) * lam - center_i - enlarged_radius
        if neg
        else arb(first_n) * lam + center_i - enlarged_radius
    ).lower()
    if not definitely_positive(exponent) or not definitely_positive(denominator):
        raise ArithmeticError("enlarged-disc deep-tail denominator/exponent failed")
    imaginary_abs = arb(max(abs(s.imag.lower()), abs(s.imag.upper())))
    angle = (arb(2) * (enlarged_radius / denominator).atan()).upper()
    angle_factor = (imaginary_abs * angle).exp().upper()
    first_term = (
        angle_factor / radius_j * denominator ** (-(exponent + arb(1)))
    ).upper()
    integral = (
        angle_factor / radius_j * denominator ** (-exponent) / (lam * exponent)
    ).upper()
    moment = (first_term + integral).upper()
    theta_ratio = (arb(1) / (radius_j * denominator)).upper()
    rho_deep = (center_ratio + theta_ratio).upper()
    return moment, rho_deep, {
        "first_n": first_n,
        "denominator_lower_bound": arb_text(denominator),
        "angle_upper_bound": arb_text(angle),
        "angle_factor_upper_bound": arb_text(angle_factor),
        "first_term_upper_bound": arb_text(first_term),
        "integral_upper_bound": arb_text(integral),
        "first_moment_upper_bound": arb_text(moment),
        "theta_over_target_radius_upper_bound": arb_text(theta_ratio),
        "center_included_ratio_upper_bound": arb_text(rho_deep),
    }


def certify_enlarged_contour_sups(
    tb_v2: dict[str, Any],
    max_N: int,
    M: int,
    progress_callback: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Certify U_{B,k} on enlarged contours for k=0,...,max_N-1."""

    if max_N < 1 or M < 8:
        raise ValueError("max_N must be positive and M at least 8")
    lam_ball, engine_centers, engine_radii = source_builder.geometry_for_factors(
        EXACT_FACTORS
    )
    if any(value.imag != 0 for value in [lam_ball, *engine_centers, *engine_radii]):
        raise ArithmeticError("q=5 geometry was not real-valued")
    lam = lam_ball.real
    centers = [arb(value) for value in tb_v2["centers"]]
    radii = [arb(value) for value in tb_v2["source_radii"]]
    geometry_overlap = all(
        (engine_radii[i].real - radii[i]).abs_lower() == 0
        and (engine_centers[i].real - centers[i]).abs_lower() == 0
        for i in range(3)
    )
    if not geometry_overlap:
        raise ValueError("TB V2 geometry does not overlap the exact-factor engine")

    s = flagship_s_box()
    enlarged = derive_enlarged_discs(tb_v2)
    completed: list[dict[str, Any]] = []
    for block_index, source_row in enumerate(tb_v2["blocks"]):
        block = tuple(source_row["block"])
        i, j, n0, neg, tail = block
        geometry = enlarged[block]
        enlarged_radius = geometry["enlarged_radius"]
        arcs = [
            arc_helper.arc_ball(centers[i - 1], enlarged_radius, arc_index, M)
            for arc_index in range(M)
        ]

        if not tail:
            weight_sup = arb(0)
            base_sup = arb(0)
            for arc_index, z in enumerate(arcs):
                denominator = z - acb(arb(n0) * lam) if neg else z + acb(arb(n0) * lam)
                theta = acb(1) / denominator if neg else -acb(1) / denominator
                weight = (denominator * denominator) ** (-s)
                base = (theta - acb(centers[j - 1])) / radii[j - 1]
                weight_sup = arb.max(weight_sup, weight.abs_upper()).upper()
                base_sup = arb.max(base_sup, base.abs_upper()).upper()
                if progress_callback is not None:
                    progress_callback({
                        "phase": "enlarged_contour_sups",
                        "block_index": block_index,
                        "block": list(block),
                        "arc_index": arc_index,
                        "arcs_completed_for_block": arc_index + 1,
                        "arcs_required_for_block": M,
                        "completed_block_count": len(completed),
                    })
            column_sups = [
                (weight_sup * base_sup**k).upper() for k in range(max_N)
            ]
            method = {
                "kind": "single_branch_direct_enlarged_arc_cover",
                "weight_sup_upper_bound": arb_text(weight_sup),
                "center_included_base_ratio_upper_bound": arb_text(base_sup),
            }
        else:
            phi_zero_sup = arb(0)
            head_ns = [int(item["n"]) for item in source_row["head_terms"]]
            head_product_sups = {n: arb(0) for n in head_ns}
            head_base_sups = {n: arb(0) for n in head_ns}
            for arc_index, z in enumerate(arcs):
                phi_zero_sup = arb.max(
                    phi_zero_sup, _tail_phi_zero(s, z, lam, n0, bool(neg)).abs_upper()
                ).upper()
                for n in head_ns:
                    denominator = z - acb(arb(n) * lam) if neg else z + acb(arb(n) * lam)
                    theta = acb(1) / denominator if neg else -acb(1) / denominator
                    weight = (denominator * denominator) ** (-s)
                    normalized_theta = theta / radii[j - 1]
                    normalized_base = (theta - acb(centers[j - 1])) / radii[j - 1]
                    head_product_sups[n] = arb.max(
                        head_product_sups[n], (weight * normalized_theta).abs_upper()
                    ).upper()
                    head_base_sups[n] = arb.max(
                        head_base_sups[n], normalized_base.abs_upper()
                    ).upper()
                if progress_callback is not None:
                    progress_callback({
                        "phase": "enlarged_contour_sups",
                        "block_index": block_index,
                        "block": list(block),
                        "arc_index": arc_index,
                        "arcs_completed_for_block": arc_index + 1,
                        "arcs_required_for_block": M,
                        "completed_block_count": len(completed),
                    })

            center_ratio = (
                abs(centers[j - 1]).upper() / radii[j - 1].lower()
            ).upper()
            deep_first = int(source_row["deep_tail"]["first_n"])
            deep_moment, deep_rho, deep_record = _deep_first_moment(
                s,
                centers[i - 1],
                enlarged_radius,
                radii[j - 1],
                lam,
                deep_first,
                bool(neg),
                center_ratio,
            )
            first_moment = (
                sum(head_product_sups.values(), arb(0)) + deep_moment
            ).upper()
            rho = max_arb([*head_base_sups.values(), deep_rho]).upper()
            column_sups = [phi_zero_sup.upper()]
            for k in range(1, max_N):
                column_sups.append(
                    (
                        phi_zero_sup * center_ratio**k
                        + first_moment * arb(k) * rho ** (k - 1)
                    ).upper()
                )
            method = {
                "kind": "hurwitz_phi0_plus_center_split_enlarged_arc_cover",
                "Phi0_sup_upper_bound": arb_text(phi_zero_sup),
                "target_center_ratio_upper_bound": arb_text(center_ratio),
                "first_moment_upper_bound": arb_text(first_moment),
                "center_included_rho_upper_bound": arb_text(rho),
                "head_first_moment_sups": {
                    str(n): arb_text(value) for n, value in head_product_sups.items()
                },
                "head_base_ratio_sups": {
                    str(n): arb_text(value) for n, value in head_base_sups.items()
                },
                "deep_first_moment": deep_record,
                "all_k_formula": "A*q^k + C*k*rho^(k-1), k>=1; A at k=0",
            }

        eta = geometry["eta"]
        record = {
            "block": list(block),
            "label": source_row["label"],
            "tail": bool(tail),
            "M_enlarged_contour_arcs": M,
            "original_radius_upper_bound": arb_text(geometry["original_radius"]),
            "certified_clearance_lower_bound": arb_text(geometry["certified_clearance"]),
            "enlargement_clearance_fraction": f"1/{ENLARGEMENT_MARGIN_DIVISOR}",
            "enlargement_lower_bound": arb_text(geometry["enlargement"]),
            "enlarged_radius": arb_text(enlarged_radius),
            "remaining_pole_cut_clearance_lower_bound": arb_text(
                geometry["remaining_clearance"]
            ),
            "eta_R_over_R_enlarged_upper_bound": arb_text(eta),
            "eta_strictly_below_one": bool(definitely_less(eta, arb(1))),
            "method": method,
            "U_B_k_upper_bounds": [arb_text(value) for value in column_sups],
        }
        completed.append(record)
        if progress_callback is not None:
            progress_callback({
                "phase": "enlarged_contour_sups",
                "block_index": block_index,
                "block": list(block),
                "block_complete": True,
                "completed_block_count": len(completed),
                "completed_block_record": record,
            })

    return {
        "status": "CERTIFIED",
        "max_N": max_N,
        "M_enlarged_contour_arcs": M,
        "s_region": {
            "re_center": "0.4538951800749447",
            "im_center": "5.7635372417301305",
            "coordinate_half_width": "1e-6",
        },
        "geometry_matches_exact_factor_engine": geometry_overlap,
        "coefficient_bound": "|a_m(B,k)| <= U_B,k * eta_B^m",
        "l1_output_tail_bound": "U_B,k * eta_B^N / (1-eta_B)",
        "blocks": completed,
    }


def output_tail_corrections(
    certificate: dict[str, Any], N: int
) -> dict[str, Any]:
    """Aggregate atomic l1 row tails for each retained input column."""

    if N > int(certificate["max_N"]):
        raise ValueError("certificate does not contain enough retained columns")
    per_input = {j: [arb(0) for _ in range(N)] for j in (1, 2, 3)}
    by_block: dict[str, list[str]] = {}
    for record in certificate["blocks"]:
        block = tuple(record["block"])
        j = int(block[1])
        eta = arb(record["eta_R_over_R_enlarged_upper_bound"]).upper()
        factor = (eta**N / (arb(1) - eta)).upper()
        bounds = [
            (arb(value) * factor).upper()
            for value in record["U_B_k_upper_bounds"][:N]
        ]
        by_block[record["label"]] = [arb_text(value) for value in bounds]
        for k, value in enumerate(bounds):
            per_input[j][k] += value
            per_input[j][k] = per_input[j][k].upper()
    flat = [per_input[j][k].upper() for j in (1, 2, 3) for k in range(N)]
    return {
        "N": N,
        "combination": (
            "For each retained input (j,k), sum atomic block l1 coefficient tails; "
            "this dominates the omitted-output H2 norm."
        ),
        "per_input_component": {
            str(j): [arb_text(value) for value in per_input[j]] for j in (1, 2, 3)
        },
        "flat_column_corrections": [arb_text(value) for value in flat],
        "by_block": by_block,
        "sum_all_column_corrections_upper_bound": arb_text(sum(flat, arb(0)).upper()),
        "max_column_correction_upper_bound": arb_text(max_arb(flat).upper()),
    }

