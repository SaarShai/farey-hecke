"""Small, branch-local q=8 copy of the q-independent T-b bounds.

Only the routines used by the explicit q=8 geometry are kept here.  The
formulas are the same Arb arc-cover and centred-tail inequalities used by the
q=5/q=7 certifiers; keeping them local makes every q=8 receipt reproducible
from tracked files without relying on an ephemeral worktree.
"""

from __future__ import annotations

from typing import Any

from flint import acb, arb


PREC_BITS = 384
THRESHOLD_TEXT = "0.70"
THRESHOLD = arb(THRESHOLD_TEXT)


def arb_text(value: arb, digits: int = 24) -> str:
    return value.str(digits, more=True)


def definitely_positive(value: arb) -> bool:
    return value.lower() > arb(0)


def definitely_negative(value: arb) -> bool:
    return value.upper() < arb(0)


def max_arb(values: list[arb]) -> arb:
    if not values:
        raise ValueError("max_arb requires at least one value")
    result = values[0]
    for value in values[1:]:
        result = arb.max(result, value)
    return result


def hull_arb(values: list[arb]) -> arb:
    lower = min(value.lower() for value in values)
    upper = max(value.upper() for value in values)
    return arb((lower + upper) / arb(2), (upper - lower) / arb(2))


def cf_value_ball(digits: list[int], lam: arb) -> arb:
    value = arb(0)
    for digit in reversed(digits):
        value = -arb(1) / (arb(digit) * lam + value)
    return value


def arc_ball(center: arb, radius: arb, arc_index: int, M: int) -> acb:
    """Closed rectangular enclosure of one circular contour arc."""

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
    values = []
    target = acb(center_j)
    for arc_index in range(M):
        values.append((theta_ball(arc_ball(center_i, radius_i, arc_index, M), lam, n, neg) - target).abs_upper())
    return max_arb(values)


def branch_pole(center_i: arb, lam: arb, n: int, neg: bool) -> arb:
    return arb(n) * lam if neg else -arb(n) * lam


def pole_margin(center_i: arb, radius_i: arb, pole: arb) -> arb:
    return (acb(pole) - acb(center_i)).abs_lower() - radius_i


def branch_cut_margin(center_i: arb, radius_i: arb, lam: arb, n: int, neg: bool) -> arb:
    if neg:
        return arb(n) * lam - center_i - radius_i
    return center_i + arb(n) * lam - radius_i


def label_for(block: list[Any] | tuple[int, int, int, bool, bool]) -> str:
    i, j, n, neg, tail = block
    return f"{i}→{j}, {'−' if neg else '+'}{n}, {'tail' if tail else 'head'}"


def head_term(block, n, centers, radii, lam, M):
    i, j, _n0, neg, _tail = block
    sup = contour_sup(centers[i - 1], radii[i - 1], centers[j - 1], lam, n, neg, M)
    ratio = sup / radii[j - 1]
    passed = definitely_negative(ratio - THRESHOLD)
    return {
        "n": n,
        "kind": "individual_arc",
        "arc_cover": {"M": M, "arc_enclosure": "Acb rectangular ball"},
        "certified_sup": sup,
        "ratio": ratio,
        "ratio_less_than_0_70": passed,
        "pass": passed,
    }


def deep_tail_term(block, first_n, centers, radii, lam):
    i, j, _n0, _neg, _tail = block
    ci, cj = centers[i - 1], centers[j - 1]
    ri, rj = radii[i - 1], radii[j - 1]
    denominator = arb(first_n) * lam - ci.abs_upper() - ri
    if not definitely_positive(denominator):
        raise ArithmeticError(f"deep-tail denominator is not positive for {label_for(block)}")
    image_radius = arb(1) / denominator
    target_distance = image_radius + cj.abs_upper()
    margin = rj - target_distance
    ratio = target_distance / rj
    inside = definitely_positive(margin)
    ratio_pass = definitely_negative(ratio - THRESHOLD)
    return {
        "first_n": first_n,
        "kind": "crude_deep_tail",
        "range": f"n≥{first_n}",
        "denominator_lower_bound": denominator,
        "image_ball_center": "0",
        "image_ball_radius": image_radius,
        "target_distance_upper": target_distance,
        "target_disc_margin": margin,
        "inside_with_margin": inside,
        "ratio": ratio,
        "ratio_less_than_0_70": ratio_pass,
        "pass": inside and ratio_pass,
    }


def serial_term(term):
    return {
        "n": term["n"],
        "kind": term["kind"],
        "arc_cover": term["arc_cover"],
        "certified_sup_upper_bound": arb_text(term["certified_sup"]),
        "ratio_upper_bound": arb_text(term["ratio"]),
        "ratio_less_than_0_70": term["ratio_less_than_0_70"],
        "pass": term["pass"],
    }


def serial_deep(term):
    return {
        "first_n": term["first_n"],
        "range": term["range"],
        "kind": term["kind"],
        "image_ball_center": term["image_ball_center"],
        "denominator_lower_bound": arb_text(term["denominator_lower_bound"]),
        "image_ball_radius": arb_text(term["image_ball_radius"]),
        "target_distance_upper": arb_text(term["target_distance_upper"]),
        "target_disc_margin": arb_text(term["target_disc_margin"]),
        "inside_with_margin": term["inside_with_margin"],
        "ratio_upper_bound": arb_text(term["ratio"]),
        "ratio_less_than_0_70": term["ratio_less_than_0_70"],
        "pass": term["pass"],
    }


def certify_block(block, centers, radii, lam, M, K_start, max_K):
    i, j, n0, _neg, tail = block
    if not tail:
        term = head_term(block, n0, centers, radii, lam, M)
        return ({
            "block": list(block), "label": label_for(block), "tail": False,
            "n0": n0, "K_used": None, "head_terms": [serial_term(term)],
            "deep_tail": None, "certified_sup_upper_bound": arb_text(term["certified_sup"]),
            "ratio_upper_bound": arb_text(term["ratio"]), "pass": term["pass"],
        }, {n0: term}, [])
    terms = {}
    trials = []
    K = K_start
    while K <= max_K:
        for n in range(n0, n0 + K + 1):
            if n not in terms:
                terms[n] = head_term(block, n, centers, radii, lam, M)
        deep = deep_tail_term(block, n0 + K + 1, centers, radii, lam)
        heads_pass = all(term["pass"] for term in terms.values())
        trial_pass = heads_pass and deep["pass"]
        trials.append({"K": K, "head_terms_pass": heads_pass, "deep_first_n": deep["first_n"],
                       "deep_ratio_upper_bound": arb_text(deep["ratio"]),
                       "deep_inside_with_margin": deep["inside_with_margin"],
                       "deep_ratio_less_than_0_70": deep["ratio_less_than_0_70"], "pass": trial_pass})
        if trial_pass:
            head_list = [terms[n] for n in range(n0, n0 + K + 1)]
            all_ratios = [term["ratio"] for term in head_list] + [deep["ratio"]]
            all_sups = [term["certified_sup"] for term in head_list] + [deep["target_distance_upper"]]
            return ({
                "block": list(block), "label": label_for(block), "tail": True,
                "n0": n0, "K_used": K, "head_terms": [serial_term(term) for term in head_list],
                "deep_tail": serial_deep(deep), "certified_sup_upper_bound": arb_text(max_arb(all_sups)),
                "ratio_upper_bound": arb_text(max_arb(all_ratios)), "pass": True,
                "K_search_trials": trials,
            }, terms, trials)
        K += 1
    raise RuntimeError(f"no passing K through {max_K} for {label_for(block)}")


def clearance_rows(blocks, centers, radii, lam):
    pole_rows, cut_rows = [], []
    for block in blocks:
        i, _j, n0, neg, tail = block
        ci, ri = centers[i - 1], radii[i - 1]
        pole = branch_pole(ci, lam, n0, neg)
        margin = pole_margin(ci, ri, pole)
        pole_rows.append({"block": list(block), "branch": f"theta_{'-' if neg else ''}{n0}" + (f" (n≥{n0})" if tail else ""),
                          "pole_location": arb_text(pole), "margin": arb_text(margin), "pass": definitely_positive(margin)})
        cut = branch_cut_margin(ci, ri, lam, n0, neg)
        cut_rows.append({"block": list(block), "expression": f"Re(nλ−z), n≥{n0}" if neg else f"Re(z+nλ), n≥{n0}",
                         "margin": arb_text(cut), "pass": definitely_positive(cut)})
    return pole_rows, cut_rows
