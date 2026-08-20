#!/usr/bin/env python3
"""Independent checker for receipt L-OUT (q=8 omitted-output projection tail).

Evaluates the seven PASS/FAIL conditions of
``lane_g/Q8_OUTPUT_TAIL_REFEREE.md`` sec 3.4.  It never trusts a
``rho_theta`` value from the receipt: every rho is recomputed here from the
exact Moebius image of the enlarged disc.  ``lane_f`` is imported read-only;
``load_operator_bounds`` is the UNMODIFIED lane_f function.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from flint import acb, arb, ctx

LANE_G = Path(__file__).resolve().parent.parent
LANE_F = LANE_G.parent / "lane_f"
sys.path.insert(0, str(LANE_F))

import q8_schur_contour as sc  # noqa: E402

TAIL_NAME_TO_BLOCKS = sc.TAIL_NAME_TO_BLOCKS
SINGLE_NAME_TO_BLOCK = sc.SINGLE_NAME_TO_BLOCK
DEFAULT_R2 = LANE_F / "f8_receipts" / "Q8_R2_F1024_LOCAL_RECEIPT.json"
DEFAULT_TB = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"
DEFAULT_W = LANE_F / "f8_receipts" / "Q8_W_ENVELOPE_F1024_RECEIPT.json"


def text(value: arb, digits: int = 30) -> str:
    return value.str(digits, more=True)


def mobius_image_ratio(c_i: arb, radius: arb, c_j: arb, r_j: arb, lam: arb, n: int, neg: bool) -> arb:
    """Exact image of disc(c_i, radius) under theta_n, as a ratio to r_j.

    neg:  theta_n(z) =  1/(z - n lam),  a = c_i - n lam
    else: theta_n(z) = -1/(z + n lam),  a = c_i + n lam
    Image disc: centre = (+/-) a/(a^2 - R^2), radius = R/(a^2 - R^2).
    """

    a = c_i - arb(n) * lam if neg else c_i + arb(n) * lam
    denominator = a * a - radius * radius
    if not (denominator.lower() > arb(0)):
        raise ArithmeticError(f"pole inside enlarged disc for n={n}")
    centre = a / denominator if neg else -a / denominator
    image_radius = radius / denominator
    return (((centre - c_j).abs_upper() + image_radius) / r_j).upper()


def mobius_rho(block, centers, radii, radius_theta, lam, n_sweep):
    i, j, n0, neg, tail = block
    c_i, c_j, r_j = centers[i - 1], centers[j - 1], radii[j - 1]
    top = n_sweep if tail else n0
    best, worst = arb(0), n0
    for n in range(n0, top + 1):
        value = mobius_image_ratio(c_i, radius_theta, c_j, r_j, lam, n, neg)
        if value.upper() > best.upper():
            best, worst = value, n
    if tail:
        denominator = arb(top + 1) * lam - c_i.abs_upper() - radius_theta
        if not (denominator.lower() > arb(0)):
            raise ArithmeticError("deep-tail denominator not positive")
        deep = ((arb(1) / denominator + c_j.abs_upper()) / r_j).upper()
        if deep.upper() > best.upper():
            best, worst = deep, top + 1
    return best.upper(), worst


def envelope_terms(row: dict, K: int) -> list[arb]:
    """M_k majorant from the receipt's own closed form, k = 0 .. K-1."""

    if row["kind"] == "single_branch":
        weight = arb(row["weight_theta_sup_upper_bound"]).upper()
        rho = arb(row["rho_theta_upper_bound"]).upper()
        return [(weight * rho**k).upper() for k in range(K)]
    A = arb(row["A_theta_upper_bound"]).upper()
    C = arb(row["C_theta_upper_bound"]).upper()
    q = arb(row["q_upper_bound"]).upper()
    rho = arb(row["rho_theta_upper_bound"]).upper()
    out = [A]
    for k in range(1, K):
        out.append((A * q**k + C * arb(k) * rho ** (k - 1)).upper())
    return out


def tau_out_block(row: dict, theta: arb, N: int, selected: bool = False) -> tuple[arb, arb]:
    """(trace, HS) omitted-output bounds theta^-N * sum_{k<N} M_k for one block."""

    terms = envelope_terms(row, N)
    if selected:
        recorded = [arb(v).upper() for v in row["selected_column_bounds_theta"]]
        for k in range(min(len(recorded), N)):
            terms[k] = arb.min(terms[k], recorded[k]).upper()
    total = sum(terms, arb(0)).upper()
    square = sum(((t * t).upper() for t in terms), arb(0)).upper()
    scale = theta ** (-N)
    return (scale * total).upper(), (scale * square.sqrt()).upper()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lout", type=Path, required=True)
    parser.add_argument("--r2", type=Path, default=DEFAULT_R2)
    parser.add_argument("--tb", type=Path, default=DEFAULT_TB)
    parser.add_argument("--w", type=Path, default=DEFAULT_W)
    parser.add_argument("--N-targets", type=int, nargs="+", default=[104, 181, 200, 214])
    parser.add_argument("--n-sweep", type=int, default=400)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    ctx.prec = 384

    lout = json.loads(args.lout.read_text(encoding="utf-8"))
    if lout.get("schema") != "q8-r2out-local/v1":
        raise ValueError("unexpected L-OUT receipt schema")
    r2 = json.loads(args.r2.read_text(encoding="utf-8"))
    tb = json.loads(args.tb.read_text(encoding="utf-8"))
    w = json.loads(args.w.read_text(encoding="utf-8"))
    # Geometry is taken from the PINNED TB receipt, not from the L-OUT echo,
    # so that the only thing under test is the rho/envelope computation.  The
    # L-OUT echo is separately checked for overlap below.
    lam = arb(tb["lambda"])
    centers = [arb(v) for v in tb["centers"]]
    radii = [arb(v) for v in tb["source_radii"]]
    geometry_echo_ok = (
        arb(lout["geometry"]["lambda"]).overlaps(lam)
        and all(arb(a).overlaps(b) for a, b in zip(lout["geometry"]["centers"], centers))
        and all(arb(a).overlaps(b) for a, b in zip(lout["geometry"]["source_radii"], radii))
    )
    theta = [arb(t) for t in lout["theta_exact_strings"]]
    radii_theta = [(theta[i] * radii[i]).upper() for i in range(3)]
    rows = {tuple(row["block"]): row for row in lout["blocks"]}
    r2_rows = {tuple(row["block"]): row for row in r2["blocks"]}
    tb_rows = {tuple(row["block"]): row for row in tb["blocks"]}
    w_rows = {tuple(row["block"]): row for row in w["boxes"][0]["blocks"]}

    report: dict = {"schema": "q8-lout-check/v1", "lout_receipt": str(args.lout.resolve()),
                    "theta_exact_strings": lout["theta_exact_strings"],
                    "N_targets": args.N_targets, "n_sweep": args.n_sweep}

    # --- Condition 1: theta_i > 1 strictly ---------------------------------
    c1_rows = [{"disc": i + 1, "theta": lout["theta_exact_strings"][i],
                "strictly_greater_than_one": bool(theta[i].lower() > arb(1))} for i in range(3)]
    c1 = all(row["strictly_greater_than_one"] for row in c1_rows)
    report["condition_1_theta_gt_1"] = {"pass": c1, "rows": c1_rows}

    # --- Condition 2: holomorphy gate at the enlarged radius ---------------
    gate_rows = []
    for gate in lout["holomorphy_gate"]:
        block = tuple(gate["block"])
        i, j, n0, neg, tail = block
        # recompute independently
        pole = arb(n0) * lam if neg else -arb(n0) * lam
        margin = (acb(pole) - acb(centers[i - 1])).abs_lower() - radii_theta[i - 1]
        cut = (arb(n0) * lam - centers[i - 1] - radii_theta[i - 1]) if neg else (
            centers[i - 1] + arb(n0) * lam - radii_theta[i - 1])
        first_n = int(tb_rows[block]["deep_tail"]["first_n"]) if tail else n0
        d_deep = (arb(first_n) * lam - centers[i - 1] - radii_theta[i - 1]) if neg else (
            arb(first_n) * lam + centers[i - 1] - radii_theta[i - 1])
        slope = (radii_theta[i - 1] / lam).upper()
        row = {
            "block": list(block), "label": gate["label"],
            "recomputed_pole_margin_lower": text(margin.lower()),
            "pole_clearance_pass": bool(margin.lower() > arb(0)),
            "recomputed_branch_cut_margin_lower": text(cut.lower()),
            "branch_cut_clearance_pass": bool(cut.lower() > arb(0)),
            "recomputed_deep_tail_d_lower": text(d_deep.lower()),
            "deep_tail_d_positive": bool(d_deep.lower() > arb(0)),
            "hurwitz_slope_upper": text(slope), "a0_floor": n0 + 4,
            "hurwitz_slope_less_than_a0": bool(slope.upper() < arb(n0 + 4).lower()),
            "receipt_agrees": (gate["pole_clearance_pass"] and gate["branch_cut_clearance_pass"]
                               and gate["deep_tail_d_positive"]),
        }
        row["pass"] = all([row["pole_clearance_pass"], row["branch_cut_clearance_pass"],
                           row["deep_tail_d_positive"], row["hurwitz_slope_less_than_a0"],
                           row["receipt_agrees"]])
        gate_rows.append(row)
    c2 = all(row["pass"] for row in gate_rows)
    report["condition_2_holomorphy_gate"] = {"pass": c2, "rows": gate_rows}

    # --- Condition 3: rho_theta reproduced by the checker's own Moebius ----
    rho_rows = []
    for block, row in rows.items():
        receipt_rho = arb(row["rho_theta_upper_bound"]).upper()
        own_rho, own_n = mobius_rho(block, centers, radii, radii_theta[block[0] - 1], lam, args.n_sweep)
        # TOLERANCE: the receipt value is an 80-digit decimal round trip of an
        # Arb ball, so it can sit ~1e-24 relative BELOW the freshly computed
        # ball's upper endpoint.  Coverage is therefore tested at 1e-20
        # relative, and the raw ratio is recorded so the margin is auditable.
        covers = receipt_rho.upper() >= (own_rho * (arb(1) - arb("1e-20"))).upper()
        ratio = (receipt_rho / own_rho).upper()
        rho_rows.append({
            "block": list(block), "label": row["label"],
            "receipt_rho_theta": text(receipt_rho, 24),
            "checker_mobius_rho_theta": text(own_rho, 24),
            "checker_worst_n": own_n, "receipt_worst_n": row["rho_theta_worst_n"],
            "receipt_covers_checker": bool(covers),
            "ratio_receipt_over_checker": text(ratio, 12),
            "agreement_within_1pct": bool(ratio.upper() < arb("1.01")),
            "rho_theta_below_one": bool(receipt_rho.upper() < arb(1)),
        })
    c3 = (geometry_echo_ok
          and all(r["receipt_covers_checker"] and r["agreement_within_1pct"] and r["rho_theta_below_one"]
                  for r in rho_rows))
    report["condition_3_rho_theta_independent"] = {
        "pass": c3, "geometry_echo_overlaps_pinned_TB": bool(geometry_echo_ok),
        "coverage_tolerance": "1e-20 relative (80-digit decimal round trip of an Arb ball)",
        "rows": rho_rows,
    }

    # --- Condition 4: self-consistency / monotonicity in theta -------------
    mono_rows = []
    for block, row in rows.items():
        selected = [arb(v).upper() for v in row["selected_column_bounds_theta"]]
        direct = [arb(v).upper() for v in row["direct_column_sups_theta"]]
        envelope = [arb(v).upper() for v in row["envelope_column_bounds_theta"]]
        if row["kind"] == "single_branch":
            r2row = r2_rows[block]
            weight0 = arb(r2row["weight_sup_upper_bound"]).upper()
            rho0 = arb(r2row["center_included_image_ratio_upper_bound"]).upper()
            base = [(weight0 * rho0**k).upper() for k in range(len(selected))]
            base_source = "recomputed from pinned R2 single-branch weight*rho^k"
        else:
            base = [arb(v).upper() for v in r2_rows[block]["selected_column_bounds"]]
            base_source = "pinned R2 selected_column_bounds"
        cut = [arb(v).upper() for v in row["selected_column_bounds_theta_tb_cutoff"]]
        ge_direct = [bool(selected[k].upper() >= direct[k].upper()) for k in range(len(selected))]
        ge_base = [bool(selected[k].upper() >= base[k].upper()) for k in range(len(selected))]
        ge_base_cut = [bool(cut[k].upper() >= base[k].upper()) for k in range(len(selected))]
        env_ge_direct = [bool(envelope[k].upper() >= direct[k].upper()) for k in range(len(selected))]
        mono_rows.append({
            "block": list(block), "label": row["label"], "base_source": base_source,
            "selected_ge_direct_all_k": all(ge_direct),
            "first_k_selected_below_direct": next((k for k, ok in enumerate(ge_direct) if not ok), None),
            "envelope_ge_direct_all_k": all(env_ge_direct),
            "selected_ge_pinned_R2_all_k": all(ge_base),
            "first_k_selected_below_R2": next((k for k, ok in enumerate(ge_base) if not ok), None),
            "min_ratio_selected_over_R2": text(min((selected[k] / base[k]).upper() for k in range(len(selected))), 12),
            "like_for_like_tb_cutoff_selected_ge_pinned_R2_all_k": all(ge_base_cut),
            "min_ratio_tb_cutoff_selected_over_R2": text(min((cut[k] / base[k]).upper() for k in range(len(selected))), 12),
        })
    # Baseline control: does the PINNED R2 receipt itself satisfy sub-test 4a?
    baseline_control = []
    for block, row in r2_rows.items():
        if row["kind"] != "hurwitz_closed_tail_family":
            continue
        sel = [arb(v).upper() for v in row["selected_column_bounds"]]
        dir_ = [arb(v).upper() for v in row["direct_column_sups"]]
        bad = [k for k in range(len(sel)) if not sel[k].upper() >= dir_[k].upper()]
        baseline_control.append({"block": list(block), "label": row["label"],
                                 "pinned_R2_selected_ge_direct_all_k": not bad,
                                 "first_k_selected_below_direct": bad[0] if bad else None})
    baseline_4a = all(r["pinned_R2_selected_ge_direct_all_k"] for r in baseline_control)
    c4a = all(r["selected_ge_direct_all_k"] for r in mono_rows)
    c4b = all(r["selected_ge_pinned_R2_all_k"] for r in mono_rows)
    c4b_like = all(r["like_for_like_tb_cutoff_selected_ge_pinned_R2_all_k"] for r in mono_rows)
    c4 = c4a and c4b
    report["condition_4_self_consistency"] = {
        "pass": c4,
        "sub_4a_selected_ge_direct": c4a,
        "sub_4b_monotonicity_vs_pinned_R2": c4b,
        "sub_4b_like_for_like_tb_cutoff": c4b_like,
        "baseline_control_pinned_R2_satisfies_4a": baseline_4a,
        "baseline_control_rows": baseline_control,
        "note": ("4a as written is failed by the PINNED R2 receipt itself (see baseline_control): "
                 "q8_r2_local.py:206 deliberately takes min(direct_sup, envelope), and the direct "
                 "arc-cover sup is inflated by interval wrapping under the r_j^-k binomial sum at "
                 "large k.  4b's production arm is confounded because the mandated n-sweep to 400 "
                 "gives a TIGHTER rho than the pinned R2 (TB cut its deep tail at first_n=14/15); "
                 "the like-for-like arm repeats it with the TB cutoff so theta is the only change."),
        "rows": mono_rows,
    }

    # --- Condition 5: output_projection_tail and full_tau ------------------
    tau_rows = {}
    for N in args.N_targets:
        bounds = sc.load_operator_bounds(args.r2, args.tb, args.w, N)
        hs, trace = bounds["hs"], bounds["trace"]
        tau_out = {}
        tau_out_sel = {}
        per_block = {}
        for name, block in SINGLE_NAME_TO_BLOCK.items():
            value, hs_value = tau_out_block(rows[block], theta[block[0] - 1], N)
            selected_value, _ = tau_out_block(rows[block], theta[block[0] - 1], N, selected=True)
            tau_out[name], tau_out_sel[name] = value, selected_value
            per_block[name] = {"trace": text(value, 12), "HS": text(hs_value, 12)}
        for name, blocks in TAIL_NAME_TO_BLOCKS.items():
            total = arb(0)
            total_sel = arb(0)
            hs_total = arb(0)
            for block in blocks:
                value, hs_value = tau_out_block(rows[block], theta[block[0] - 1], N)
                selected_value, _ = tau_out_block(rows[block], theta[block[0] - 1], N, selected=True)
                total += value
                total_sel += selected_value
                hs_total += hs_value
            tau_out[name], tau_out_sel[name] = total.upper(), total_sel.upper()
            per_block[name] = {"trace": text(total.upper(), 12), "HS": text(hs_total.upper(), 12)}
        a2, a3 = hs["A2"], hs["A3"]
        b1, b2 = hs["B1"], hs["B2"]

        def telescope(term: dict) -> arb:
            return (term["B3"] + a3 * term["B2"] + a3 * a2 * term["B1"]
                    + term["A3"] * b2 + term["A3"] * a2 * b1
                    + a3 * term["A2"] * b1).upper()

        output_projection_tail = telescope(tau_out)
        output_projection_tail_selected = telescope(tau_out_sel)
        input_tail_only = bounds["input_tail_only"]
        full_tau = (input_tail_only + output_projection_tail).upper()
        recomputed_input = telescope(trace)
        tau_rows[str(N)] = {
            "N": N,
            "input_tail_only": text(input_tail_only, 12),
            "input_tail_only_recomputed_by_same_telescoping": text(recomputed_input, 12),
            "output_projection_tail": text(output_projection_tail, 12),
            "output_projection_tail_selected_variant": text(output_projection_tail_selected, 12),
            "full_tau": text(full_tau, 12),
            "full_tau_finite": bool(full_tau.is_finite()),
            "per_block_tau_out": per_block,
            "hs_factors": {k: text(v, 12) for k, v in hs.items()},
        }
        print(f"L_OUT_CHECK N={N} input={text(input_tail_only,8)} output={text(output_projection_tail,8)} full={text(full_tau,8)}", flush=True)
    c5 = all(row["full_tau_finite"] for row in tau_rows.values())
    report["condition_5_full_tau"] = {
        "pass": c5,
        "substitution_note": ("output tail substituted into EACH trace[.] slot of the "
                              "q8_schur_contour.py:351-358 telescoping; hs[.] factors unchanged"),
        "rows": tau_rows,
    }

    # --- Condition 6: N=104 regression / red flag --------------------------
    c6 = None
    if "104" in tau_rows:
        value = arb(tau_rows["104"]["full_tau"])
        red_flag = value.upper() <= arb("1e-14")
        c6 = not red_flag
        report["condition_6_regression_N104"] = {
            "pass": bool(c6), "full_tau_at_104": tau_rows["104"]["full_tau"],
            "red_flag_full_tau_le_1e-14": bool(red_flag),
            "input_tail_only_at_104": tau_rows["104"]["input_tail_only"],
        }
    else:
        report["condition_6_regression_N104"] = {"pass": None, "reason": "N=104 not in targets"}

    # --- Condition 7 -------------------------------------------------------
    conditions = [c1, c2, c3, c4, c5, c6]
    c7 = all(value is True for value in conditions)
    report["condition_7_full_tail_certified"] = {
        "full_tail_certified": bool(c7),
        "conditions_1_to_6": [None if v is None else bool(v) for v in conditions],
        "note": "lane_f q8_schur_contour.py:395 full_tail_certified remains False; no lane_f file was modified",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"conditions_1_to_7": [None if v is None else bool(v) for v in conditions] + [bool(c7)],
                      "report": str(args.out.resolve())}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
