#!/usr/bin/env python3
"""Receipt L-OUT generator: enlarged-contour (theta) q=8 R2 column envelope.

This is the ``q8_r2_local.py`` computation re-run with the ARC COVER built at
radius ``theta_i * r_i`` on the OUTPUT disc ``i``, while every target-disc
quantity (``c_j``, ``r_j``) stays UNSCALED.  No lane_f file is modified or
imported in a mutated form; ``q8_r2_local`` / ``q8_tb_support`` /
``q8_weight_support`` are imported read-only.

Spec: research_notes/rh_goals_2026-08-14/lane_g/Q8_OUTPUT_TAIL_REFEREE.md sec 3.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

from flint import acb, arb, ctx

LANE_G = Path(__file__).resolve().parent.parent
LANE_F = LANE_G.parent / "lane_f"
sys.path.insert(0, str(LANE_F))

import f8_certify_tb_blocks as f8  # noqa: E402
import q8_r2_local as r2local  # noqa: E402
import q8_tb_support as tb  # noqa: E402
import q8_weight_support as wsup  # noqa: E402

KAPPA = 3
PIN_RE = r2local.PIN_RE
PIN_IM = r2local.PIN_IM
HALF_WIDTH = r2local.HALF_WIDTH
DEFAULT_TB = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"
DEFAULT_W = LANE_F / "f8_receipts" / "Q8_W_ENVELOPE_F1024_RECEIPT.json"
DEFAULT_R2 = LANE_F / "f8_receipts" / "Q8_R2_F1024_LOCAL_RECEIPT.json"

# rho_theta sweep: exact per-n arc sup for n <= N_SWEEP, crude deep-tail bound
# for n > N_SWEEP.  The referee requires the sweep to reach at least 400.
N_SWEEP = 400


def arb_text(value: arb, digits: int = 80) -> str:
    return value.str(digits, more=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deep_first_moment_bound_theta(block, first_n, centers, radii, r_i_theta, lam, s):
    """``q8_r2_local.deep_first_moment_bound`` with the SOURCE radius enlarged.

    Only ``radii[i-1]`` is replaced by ``r_i_theta``; ``radii[j-1]`` (target)
    is untouched.  This is the one change the referee's spec allows.
    """

    i, j, _n0, neg, _tail = block
    p = arb(2) * s.real.lower()
    d = (
        arb(first_n) * lam + centers[i - 1] - r_i_theta
        if not neg
        else arb(first_n) * lam - centers[i - 1] - r_i_theta
    )
    if not r2local.definitely_positive(p) or not r2local.definitely_positive(d):
        raise ArithmeticError(f"invalid deep-tail exponent/denominator for {block}")
    im_abs = arb(max(abs(s.imag.lower()), abs(s.imag.upper())))
    angle = arb(2) * (r_i_theta / d).atan()
    angle_factor = (im_abs * angle).exp()
    exponent = p + arb(1)
    first_term = angle_factor / radii[j - 1] * d ** (-exponent)
    integral = angle_factor / radii[j - 1] * d ** (-p) / (lam * p)
    total = (first_term + integral).upper()
    return total, {
        "first_n": first_n,
        "denominator_lower_bound": arb_text(d),
        "weight_exponent_p": arb_text(p),
        "first_moment_sum_upper_bound": arb_text(total),
    }


def image_ratio_sup_on_arcs(arcs_i, c_j, r_j, lam, n, neg):
    """sup over the enlarged arc cover of |theta_n(z) - c_j| / r_j."""

    target = acb(c_j)
    values = [(tb.theta_ball(z, lam, n, neg) - target).abs_upper() for z in arcs_i]
    return (tb.max_arb(values) / r_j).upper()


def deep_ratio_bound(c_i, r_i_theta, c_j, r_j, lam, first_n):
    """Crude n >= first_n image-ratio bound at the enlarged radius."""

    denominator = arb(first_n) * lam - c_i.abs_upper() - r_i_theta
    if not r2local.definitely_positive(denominator):
        raise ArithmeticError("deep-tail denominator not positive at enlarged radius")
    image_radius = arb(1) / denominator
    return ((image_radius + c_j.abs_upper()) / r_j).upper(), denominator


def rho_theta_arccover(block, centers, radii, r_i_theta, lam, arcs_i, n_sweep):
    """rho_theta by the TB arc-cover route: max over n = n0..n_sweep plus tail."""

    i, j, n0, neg, tail = block
    c_j, r_j = centers[j - 1], radii[j - 1]
    per_n = {}
    best = arb(0)
    worst_n = n0
    top = n_sweep if tail else n0
    for n in range(n0, top + 1):
        value = image_ratio_sup_on_arcs(arcs_i, c_j, r_j, lam, n, neg)
        if n <= n0 + 20 or n % 50 == 0 or n == top:
            per_n[str(n)] = arb_text(value, 24)
        if value.upper() > best.upper():
            best, worst_n = value, n
    deep = None
    if tail:
        deep_value, denominator = deep_ratio_bound(centers[i - 1], r_i_theta, c_j, r_j, lam, top + 1)
        deep = {
            "first_n": top + 1,
            "denominator_lower_bound": arb_text(denominator, 24),
            "ratio_upper_bound": arb_text(deep_value, 24),
        }
        if deep_value.upper() > best.upper():
            best, worst_n = deep_value, top + 1
    return best.upper(), worst_n, per_n, deep


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tb", type=Path, default=DEFAULT_TB)
    parser.add_argument("--w", type=Path, default=DEFAULT_W)
    parser.add_argument("--r2", type=Path, default=DEFAULT_R2)
    parser.add_argument("--theta", type=str, nargs="+", default=["1.2"],
                        help="one value (uniform) or three (per output disc)")
    parser.add_argument("--M", type=int, default=512)
    parser.add_argument("--K-head", type=int, default=16)
    parser.add_argument("--n-sweep", type=int, default=N_SWEEP)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.M % 4:
        raise SystemExit("M must be divisible by four")
    if len(args.theta) not in (1, 3):
        raise SystemExit("--theta takes one or three values")
    theta_strings = list(args.theta) * 3 if len(args.theta) == 1 else list(args.theta)
    ctx.prec = 384
    started = time.perf_counter()

    tb_v2 = json.loads(args.tb.read_text(encoding="utf-8"))
    w_v2 = json.loads(args.w.read_text(encoding="utf-8"))
    if tb_v2.get("q") != 8 or len(tb_v2.get("blocks", [])) != 8:
        raise ValueError("unexpected q=8 TB receipt")
    if w_v2.get("schema") != "tb-weight-envelope-cert/v2":
        raise ValueError("unexpected q=8 W receipt")
    blocks = [tuple(item) for item in tb_v2["blocks_source"]["blocks"]]
    if blocks != f8.BLOCKS:
        raise ValueError("q8 block source mismatch")

    lam = arb(tb_v2["lambda"])
    centers = [arb(v) for v in tb_v2["centers"]]
    radii = [arb(v) for v in tb_v2["source_radii"]]
    theta = [arb(t) for t in theta_strings]
    for value in theta:
        if not (value.lower() > arb(1)):
            raise ArithmeticError("theta must be strictly greater than one")
    radii_theta = [(theta[i] * radii[i]).upper() for i in range(KAPPA)]
    # THE one structural change: arcs at theta_i * r_i.
    arcs = [[tb.arc_ball(centers[i], radii_theta[i], index, args.M) for index in range(args.M)]
            for i in range(KAPPA)]
    s = r2local.s_box()

    tb_rows = {tuple(row["block"]): row for row in tb_v2["blocks"]}
    w_rows = {tuple(row["block"]): row for row in w_v2["boxes"][0]["blocks"]}

    # --- holomorphy gate at the enlarged radius -----------------------------
    gates = []
    for block in blocks:
        i, j, n0, neg, tail = block
        c_i, r_it = centers[i - 1], radii_theta[i - 1]
        pole = tb.branch_pole(c_i, lam, n0, neg)
        pole_margin = tb.pole_margin(c_i, r_it, pole)
        cut = (arb(n0) * lam - c_i - r_it) if neg else (c_i + arb(n0) * lam - r_it)
        first_n = int(tb_rows[block]["deep_tail"]["first_n"]) if tail else n0
        d_deep = (arb(first_n) * lam - c_i - r_it) if neg else (arb(first_n) * lam + c_i - r_it)
        slope = (r_it / lam).upper()
        gates.append({
            "block": list(block), "label": tb.label_for(block),
            "theta": theta_strings[i - 1],
            "enlarged_radius": arb_text(r_it, 30),
            "pole_location": arb_text(pole, 30),
            "pole_margin_lower_bound": arb_text(pole_margin.lower(), 30),
            "pole_clearance_pass": bool(r2local.definitely_positive(pole_margin)),
            "branch_cut_margin_lower_bound": arb_text(cut.lower(), 30),
            "branch_cut_clearance_pass": bool(r2local.definitely_positive(cut)),
            "deep_tail_d_lower_bound": arb_text(d_deep.lower(), 30),
            "deep_tail_d_positive": bool(r2local.definitely_positive(d_deep)),
            "hurwitz_slope_upper_bound": arb_text(slope, 30),
            "hurwitz_slope_less_than_a0": bool(slope.upper() < arb(n0 + 4).lower()),
        })

    records = []
    for block in blocks:
        i, j, n0, neg, tail = block
        r_it = radii_theta[i - 1]
        rho_t, worst_n, per_n, deep_ratio = rho_theta_arccover(
            block, centers, radii, r_it, lam, arcs[i - 1], args.n_sweep
        )
        # Like-for-like diagnostic: the same rho with the DEEP-TAIL CUTOFF the
        # pinned R2/TB receipt used (first_n from TB), so the monotonicity-in-
        # theta comparison of referee condition 4 is apples-to-apples.  The
        # production rho above uses the mandated n-sweep to 400 and is tighter.
        rho_tb_cut = rho_t
        if tail:
            cutoff = int(tb_rows[block]["deep_tail"]["first_n"])
            rho_tb_cut, _, _, _ = rho_theta_arccover(
                block, centers, radii, r_it, lam, arcs[i - 1], cutoff - 1
            )
        q = (abs(centers[j - 1]) / radii[j - 1]).upper()
        if not tail:
            weight_t, weight_arc = wsup.weight_sup(arcs[i - 1], lam, n0, neg, s)
            weight_t = weight_t.upper()
            # direct enlarged-arc column sups for the single branch
            direct = []
            for k in range(args.K_head + 1):
                values = []
                for z in arcs[i - 1]:
                    denominator = z - acb(arb(n0) * lam) if neg else z + acb(arb(n0) * lam)
                    weight = (acb(1) / (denominator * denominator)) ** s
                    base = ((acb(1) / denominator if neg else acb(-1) / denominator)
                            - acb(centers[j - 1])) / acb(radii[j - 1])
                    values.append((weight * base**k).abs_upper())
                direct.append(tb.max_arb(values).upper())
            # W_theta is the k=0 boundary sup; two Arb routes compute it (the
            # weight_sup selector and the max_arb hull) and differ by ~1e-19
            # relative.  Round the certified sup UP to the larger of the two.
            weight_t = arb.max(weight_t, direct[0]).upper()
            envelope = [(weight_t * rho_t**k).upper() for k in range(args.K_head + 1)]
            selected = [min(direct[k].upper(), envelope[k].upper()) for k in range(args.K_head + 1)]
            records.append({
                "block": list(block), "label": tb.label_for(block), "kind": "single_branch",
                "theta_exact_string": theta_strings[i - 1],
                "weight_theta_sup_upper_bound": arb_text(weight_t),
                "weight_worst_arc_index": weight_arc,
                "rho_theta_upper_bound": arb_text(rho_t),
                "rho_theta_tb_cutoff_diagnostic": arb_text(rho_tb_cut),
                "rho_theta_worst_n": worst_n,
                "rho_theta_per_n_sample": per_n,
                "q_upper_bound": arb_text(q),
                "direct_column_sups_theta": [arb_text(v) for v in direct],
                "envelope_column_bounds_theta": [arb_text(v) for v in envelope],
                "selected_column_bounds_theta": [arb_text(v) for v in selected],
                "selected_column_bounds_theta_tb_cutoff": [arb_text(v) for v in selected],
                "consumption_formula": "theta^-N * W_theta * G1(N,rho_theta) (trace); theta^-N * W_theta * sqrt(G2(N,rho_theta)) (HS)",
            })
            print(f"L_OUT block={tb.label_for(block)} W_theta={arb_text(weight_t,20)} rho_theta={arb_text(rho_t,20)}", flush=True)
            continue

        direct = [arb(0) for _ in range(args.K_head + 1)]
        worst_arcs = [0] * (args.K_head + 1)
        for arc_index, z in enumerate(arcs[i - 1]):
            cols = r2local.exact_tail_columns_on_arc(
                s, z, centers[j - 1], radii[j - 1], lam, n0, neg, args.K_head
            )
            for k, column in enumerate(cols):
                bound = column.abs_upper()
                if bound.upper() > direct[k].upper():
                    direct[k] = bound.upper()
                    worst_arcs[k] = arc_index
        moments, heads = [], []
        for term in tb_rows[block]["head_terms"]:
            n = int(term["n"])
            product, weight, theta_ratio, worst = r2local.direct_head_first_moment_sup(
                arcs[i - 1], s, lam, radii[j - 1], n, neg
            )
            moments.append(product)
            heads.append({"n": n, "weighted_first_moment_sup_upper_bound": arb_text(product),
                          "worst_arc_index": worst})
        first_n = int(tb_rows[block]["deep_tail"]["first_n"])
        deep_C, deep_record = deep_first_moment_bound_theta(
            block, first_n, centers, radii, r_it, lam, s
        )
        C = (sum(moments, arb(0)) + deep_C).upper()
        A = direct[0].upper()
        envelope = [A] + [r2local.tail_envelope(A, C, q, rho_t, k).upper()
                          for k in range(1, args.K_head + 1)]
        selected = [min(direct[k].upper(), envelope[k].upper()) for k in range(args.K_head + 1)]
        envelope_cut = [A] + [r2local.tail_envelope(A, C, q, rho_tb_cut, k).upper()
                              for k in range(1, args.K_head + 1)]
        selected_cut = [min(direct[k].upper(), envelope_cut[k].upper()) for k in range(args.K_head + 1)]
        records.append({
            "block": list(block), "label": tb.label_for(block),
            "kind": "hurwitz_closed_tail_family",
            "theta_exact_string": theta_strings[i - 1],
            "A_theta_upper_bound": arb_text(A),
            "C_theta_upper_bound": arb_text(C),
            "q_upper_bound": arb_text(q),
            "rho_theta_upper_bound": arb_text(rho_t),
            "rho_theta_tb_cutoff_diagnostic": arb_text(rho_tb_cut),
            "rho_theta_worst_n": worst_n,
            "rho_theta_per_n_sample": per_n,
            "rho_theta_deep_tail": deep_ratio,
            "direct_column_sups_theta": [arb_text(v) for v in direct],
            "worst_arcs": worst_arcs,
            "head_first_moments": heads,
            "deep_first_moment": deep_record,
            "envelope_column_bounds_theta": [arb_text(v) for v in envelope],
            "selected_column_bounds_theta": [arb_text(v) for v in selected],
            "selected_column_bounds_theta_tb_cutoff": [arb_text(v) for v in selected_cut],
            "consumption_formula": "theta^-N * (A_theta*G1(N,q) + C_theta*S1(N,rho_theta)) (trace)",
        })
        print(f"L_OUT block={tb.label_for(block)} A={arb_text(A,20)} C={arb_text(C,20)} rho_theta={arb_text(rho_t,20)}", flush=True)

    receipt = {
        "schema": "q8-r2out-local/v1",
        "status": "ENLARGED_CONTOUR_OUTPUT_ENVELOPE",
        "theorem_grade_verdict": "NO",
        "analytic_linkage": "OPEN",
        "q": 8, "sign": 1, "M": args.M, "K_head": args.K_head, "n_head": 4,
        "precision_bits": 384,
        "pin": {"re": PIN_RE, "im": PIN_IM, "half_width": HALF_WIDTH},
        "theta_exact_strings": theta_strings,
        "theta_uniform": len(set(theta_strings)) == 1,
        "n_sweep": args.n_sweep,
        "geometry": {
            "lambda": arb_text(lam),
            "centers": [arb_text(v) for v in centers],
            "source_radii": [arb_text(v) for v in radii],
            "enlarged_arc_radii": [arb_text(v) for v in radii_theta],
            "note": "source_radii are the UNSCALED target-disc radii used for c_j/r_j; the arc cover only uses enlarged_arc_radii",
        },
        "holomorphy_gate": gates,
        "blocks": records,
        "source_bindings": {
            "engine": str((LANE_G / "law_probes" / "kaggle_boundary_rate" / "zeta_cert_rosen_q5.py").resolve()),
            "r2_local_engine": str((LANE_F / "q8_r2_local.py").resolve()),
            "r2_local_sha256": sha256(LANE_F / "q8_r2_local.py"),
            "TB": str(args.tb.resolve()), "TB_sha256": sha256(args.tb),
            "W": str(args.w.resolve()), "W_sha256": sha256(args.w),
            "R2": str(args.r2.resolve()), "R2_sha256": sha256(args.r2),
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": str(args.out.resolve()),
                      "theta": theta_strings,
                      "runtime_seconds": receipt["runtime_seconds"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
