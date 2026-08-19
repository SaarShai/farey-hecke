"""Branch-local q=8 weight aggregation for the T-b receipt."""

from __future__ import annotations

import sys
from pathlib import Path

from flint import acb, arb

LANE_F = Path(__file__).resolve().parent
TRACKED_ENGINE_DIR = LANE_F.parent / "lane_g" / "law_probes" / "kaggle_boundary_rate"
sys.path.insert(0, str(TRACKED_ENGINE_DIR))

import zeta_cert_rosen_q5 as engine  # noqa: E402
import q8_tb_support as tb  # noqa: E402

KAPPA = 3


def arb_text(value: arb, digits: int = 24) -> str:
    return value.str(digits, more=True)


def max_arb(values: list[arb]) -> arb:
    if not values:
        raise ValueError("max_arb requires at least one value")
    result = values[0]
    for value in values[1:]:
        result = arb.max(result, value)
    return result


def sum_arb(values: list[arb]) -> arb:
    result = arb(0)
    for value in values:
        result += value
    return result


def theta_prime(z: acb, lam: arb, n: int, neg: bool) -> acb:
    denominator = z - acb(arb(n) * lam) if neg else z + acb(arb(n) * lam)
    return acb(1) / (denominator * denominator)


def weight_sup(arcs: list[acb], lam: arb, n: int, neg: bool, s: acb) -> tuple[arb, int]:
    values = [(theta_prime(z, lam, n, neg) ** s).abs_upper() for z in arcs]
    worst = max(range(len(values)), key=lambda index: values[index].upper())
    return values[worst], worst


def hurwitz_phi0_sup(arcs: list[acb], lam: arb, n0: int, neg: bool, s: acb) -> tuple[arb, int]:
    values = []
    for z in arcs:
        a0 = acb(n0) + (-z / lam if neg else z / lam)
        closed_tail = (lam * lam) ** (-s) * engine.hurwitz_series_in_a(
            2 * s, a0, acb(0), 1
        )[0]
        values.append(closed_tail.abs_upper())
    worst = max(range(len(values)), key=lambda index: values[index].upper())
    return values[worst], worst


def deep_weight_image_bound(block, first_n, centers, radii, lam, s):
    i, j, _n0, neg, _tail = block
    sigma_lower = s.real.lower()
    p = arb(2) * sigma_lower
    if not tb.definitely_positive(p):
        raise ArithmeticError(f"non-positive weight exponent for {block}")
    d = (
        arb(first_n) * lam + centers[i - 1] - radii[i - 1]
        if not neg else arb(first_n) * lam - centers[i - 1] - radii[i - 1]
    )
    if not tb.definitely_positive(d):
        raise ArithmeticError(f"deep denominator is not positive for {block}")
    im_abs = arb(max(abs(s.imag.lower()), abs(s.imag.upper())))
    angle = arb(2) * (radii[i - 1] / d).atan()
    angle_factor = (im_abs * angle).exp()
    exponent = p + arb(1)
    first_product = angle_factor / radii[j - 1] * d ** (-exponent)
    integral = angle_factor / radii[j - 1] * d ** (-p) / (lam * p)
    total = first_product + integral
    return {
        "status": "FINITE_IMAGE_RADIUS_INTEGRAL", "first_n": first_n, "range": f"n≥{first_n}",
        "denominator_lower_bound": arb_text(d), "sigma_lower": arb_text(sigma_lower),
        "weight_exponent_p": arb_text(p), "integral_exponent_1_plus_p": arb_text(exponent),
        "angle_bound": arb_text(angle), "im_s_abs_upper_bound": arb_text(im_abs),
        "angle_factor": arb_text(angle_factor), "target_radius": arb_text(radii[j - 1]),
        "image_ratio_bound": "1/(R_j*d_n)", "first_product_upper_bound": arb_text(first_product),
        "integral_upper_bound": arb_text(integral), "deep_sum_upper_bound": arb_text(total),
        "integral_converges": tb.definitely_positive(exponent - arb(1)),
    }


def f_bound(W: arb, rho: arb, N: int) -> arb:
    value = (arb(1) + arb(KAPPA) * W / (arb(1) - rho)).exp()
    return value * (arb(KAPPA) * W * rho**N / (arb(1) - rho))


def certify_block(block, v2_block, centers, radii, lam, arcs, s, s_info):
    i, j, n0, neg, tail = block
    if list(block) != v2_block["block"]:
        raise ValueError(f"TB block mismatch for {tb.label_for(block)}")
    head_terms, weighted_products = [], []
    for term in v2_block["head_terms"]:
        n = int(term["n"])
        sup, worst_arc = weight_sup(arcs[i - 1], lam, n, neg, s)
        ratio = arb(term["ratio_upper_bound"])
        product = sup * ratio
        head_terms.append({
            "n": n, "weight_sup_upper_bound": arb_text(sup), "weight_worst_arc_index": worst_arc,
            "v2_image_ratio_upper_bound": arb_text(ratio), "weighted_head_product_upper_bound": arb_text(product),
            "source_v2_term": term, "s_ball": s_info,
        })
        weighted_products.append(product)
    deep = None
    phi0_sup = None
    phi0_arc = None
    if tail:
        first_n = int(v2_block["deep_tail"]["first_n"])
        deep = deep_weight_image_bound(block, first_n, centers, radii, lam, s)
        phi0_sup, phi0_arc = hurwitz_phi0_sup(arcs[i - 1], lam, n0, neg, s)
        deep["phi0_closed_tail_sup_upper_bound"] = arb_text(phi0_sup)
        deep["phi0_closed_tail_worst_arc_index"] = phi0_arc
        weighted_products.append(arb(deep["deep_sum_upper_bound"]))
    contribution = sum_arb(weighted_products)
    plain_sup = plain_arc = None
    if not tail:
        plain_sup, plain_arc = weight_sup(arcs[i - 1], lam, n0, neg, s)
        contribution = plain_sup
    return {
        "block": list(block), "label": tb.label_for(block), "source_disc": i, "target_disc": j,
        "n0": n0, "negative_branch": neg, "tail": tail, "head_terms": head_terms,
        "head_weighted_sum_upper_bound": arb_text(sum_arb([arb(item["weighted_head_product_upper_bound"]) for item in head_terms])),
        "deep_tail": deep, "plain_weight_sup_upper_bound": arb_text(plain_sup) if plain_sup is not None else None,
        "plain_weight_worst_arc_index": plain_arc, "W_ge1_block_upper_bound": arb_text(contribution),
        "W0_block_upper_bound": arb_text(phi0_sup) if phi0_sup is not None else arb_text(plain_sup),
        "W0_worst_arc_index": phi0_arc if phi0_arc is not None else plain_arc,
    }
