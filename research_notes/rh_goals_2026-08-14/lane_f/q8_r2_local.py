#!/usr/bin/env python3
"""Tracked q=8 R2 column-envelope replay.

This is the q-independent center-split majorant specialized to the eight
MMS-(32) blocks.  It deliberately emits an R2-only receipt: no Fredholm
determinant or Selberg factorization claim is made here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path

from flint import acb, arb, ctx

LANE_F = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE_F))
TRACKED_ENGINE_DIR = LANE_F.parent / "lane_g" / "law_probes" / "kaggle_boundary_rate"
sys.path.insert(0, str(TRACKED_ENGINE_DIR))

import f8_certify_tb_blocks as f8  # noqa: E402
import q8_tb_support as tb  # noqa: E402
import zeta_cert_rosen_q5 as engine  # noqa: E402


PIN_RE = "0.4252310423737965"
PIN_IM = "4.345760788321986"
HALF_WIDTH = "1e-6"
KAPPA = 3
N_HEAD_ENGINE = 4
DEFAULT_TB = LANE_F / "f8_receipts" / "Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json"
DEFAULT_W = LANE_F / "f8_receipts" / "Q8_W_ENVELOPE_F1024_RECEIPT.json"
DEFAULT_OUT = LANE_F / "f8_receipts" / "Q8_R2_F1024_LOCAL_RECEIPT.json"


def arb_text(value: arb, digits: int = 80) -> str:
    return value.str(digits, more=True)


def definitely_positive(value: arb) -> bool:
    return value.lower() > arb(0)


def definitely_less(left: arb, right: arb) -> bool:
    return left.upper() < right.lower()


def max_arb(values: list[arb]) -> arb:
    result = values[0]
    for value in values[1:]:
        result = arb.max(result, value)
    return result.upper()


def s_box() -> acb:
    return acb(arb(PIN_RE) + arb(0, arb(HALF_WIDTH)), arb(PIN_IM) + arb(0, arb(HALF_WIDTH)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_tail_columns_on_arc(s: acb, z: acb, c_j: arb, r_j: arb, lam: arb, n0: int, neg: bool, k_head: int) -> list[acb]:
    a0 = acb(n0) + (-z / lam if neg else z / lam)
    lam2s = (lam * lam) ** (-s)
    neg_inv_lam = acb(-1) / lam
    z_terms: list[acb] = []
    m_factor = acb(1)
    for m in range(k_head + 1):
        hurwitz = engine.hurwitz_series_in_a(2 * s + m, a0, acb(0), 1)[0]
        z_terms.append(lam2s * m_factor * hurwitz)
        m_factor *= neg_inv_lam
    columns = []
    for k in range(k_head + 1):
        total = acb(0)
        r_factor = r_j ** (-k)
        for m in range(k + 1):
            total += acb(math.comb(k, m)) * ((-c_j) ** (k - m)) * r_factor * z_terms[m]
        columns.append(total)
    return columns


def direct_head_first_moment_sup(arcs, s, lam, r_j, n, neg):
    products, weights, theta_ratios = [], [], []
    for z in arcs:
        denominator = z - acb(arb(n) * lam) if neg else z + acb(arb(n) * lam)
        theta = acb(1) / denominator if neg else acb(-1) / denominator
        weight = (denominator * denominator) ** (-s)
        products.append((weight * theta / r_j).abs_upper())
        weights.append(weight.abs_upper())
        theta_ratios.append((theta / r_j).abs_upper())
    worst = max(range(len(products)), key=lambda index: products[index].upper())
    return max_arb(products), max_arb(weights), max_arb(theta_ratios), worst


def deep_first_moment_bound(block, first_n, centers, radii, lam, s):
    i, j, _n0, neg, _tail = block
    p = arb(2) * s.real.lower()
    d = (arb(first_n) * lam + centers[i - 1] - radii[i - 1] if not neg else arb(first_n) * lam - centers[i - 1] - radii[i - 1])
    if not definitely_positive(p) or not definitely_positive(d):
        raise ArithmeticError(f"invalid deep-tail exponent/denominator for {block}")
    im_abs = arb(max(abs(s.imag.lower()), abs(s.imag.upper())))
    angle = arb(2) * (radii[i - 1] / d).atan()
    angle_factor = (im_abs * angle).exp()
    exponent = p + arb(1)
    first_term = angle_factor / radii[j - 1] * d ** (-exponent)
    integral = angle_factor / radii[j - 1] * d ** (-p) / (lam * p)
    total = (first_term + integral).upper()
    q_center = (abs(centers[j - 1]) / radii[j - 1]).upper()
    theta_first = (arb(1) / (radii[j - 1] * d)).upper()
    return total, {"first_n": first_n, "denominator_lower_bound": arb_text(d), "sigma_lower": arb_text(s.real.lower()),
                   "weight_exponent_p": arb_text(p), "first_moment_sum_upper_bound": arb_text(total),
                   "center_included_ratio_at_first_n": arb_text((q_center + theta_first).upper()),
                   "integral_converges": definitely_positive(p)}


def tail_envelope(A, C, q, rho, k):
    if k == 0:
        return A.upper()
    return (A * q**k + C * arb(k) * rho ** (k - 1)).upper()


def derivative_geometric_tail(rho, N):
    return (rho ** (N - 1) * (arb(N) - arb(N - 1) * rho) / (arb(1) - rho) ** 2).upper()


def tail_block_tail(A, C, q, rho, N):
    return (A * q**N / (arb(1) - q) + C * derivative_geometric_tail(rho, N)).upper()


def single_block_tail(weight, rho, N):
    return (weight * rho**N / (arb(1) - rho)).upper()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tb", type=Path, default=DEFAULT_TB)
    parser.add_argument("--w", type=Path, default=DEFAULT_W)
    parser.add_argument("--N-targets", type=int, nargs="+", default=[256, 320])
    parser.add_argument("--M", type=int, default=512)
    parser.add_argument("--K-head", type=int, default=16)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    if args.M % 4:
        raise SystemExit("M must be divisible by four")
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
    centers = [arb(value) for value in tb_v2["centers"]]
    radii = [arb(value) for value in tb_v2["source_radii"]]
    arcs = [[tb.arc_ball(centers[i], radii[i], index, args.M) for index in range(args.M)] for i in range(KAPPA)]
    s = s_box()
    tb_rows = {tuple(row["block"]): row for row in tb_v2["blocks"]}
    w_rows = {tuple(row["block"]): row for row in w_v2["boxes"][0]["blocks"]}
    if set(tb_rows) != set(blocks) or set(w_rows) != set(blocks):
        raise ValueError("receipt block maps mismatch")
    low_bounds: dict[tuple, list[arb]] = {}
    high_params: dict[tuple, dict[str, arb]] = {}
    records = []
    for block in blocks:
        i, j, n0, neg, tail = block
        tb_row, w_row = tb_rows[block], w_rows[block]
        rho = arb(tb_row["ratio_upper_bound"]).upper()
        if not definitely_less(rho, arb(1)):
            raise ArithmeticError(f"rho not below one for {block}")
        if not tail:
            weight = arb(w_row["plain_weight_sup_upper_bound"]).upper()
            low_bounds[block] = [(weight * rho**k).upper() for k in range(args.K_head + 1)]
            high_params[block] = {"weight": weight, "rho": rho}
            records.append({"block": list(block), "label": tb.label_for(block), "kind": "single_branch", "weight_sup_upper_bound": arb_text(weight), "center_included_image_ratio_upper_bound": arb_text(rho)})
            continue
        direct_sups = [arb(0) for _ in range(args.K_head + 1)]
        worst_arcs = [0] * (args.K_head + 1)
        for arc_index, z in enumerate(arcs[i - 1]):
            cols = exact_tail_columns_on_arc(s, z, centers[j - 1], radii[j - 1], lam, n0, neg, args.K_head)
            for k, column in enumerate(cols):
                bound = column.abs_upper()
                if bound.upper() > direct_sups[k].upper():
                    direct_sups[k] = bound.upper(); worst_arcs[k] = arc_index
        moments = []
        heads = []
        for term in tb_row["head_terms"]:
            n = int(term["n"])
            product, weight, theta_ratio, worst = direct_head_first_moment_sup(arcs[i - 1], s, lam, radii[j - 1], n, neg)
            moments.append(product)
            heads.append({"n": n, "weighted_first_moment_sup_upper_bound": arb_text(product), "weight_sup_upper_bound": arb_text(weight), "theta_over_target_radius_sup_upper_bound": arb_text(theta_ratio), "worst_arc_index": worst})
        first_n = int(tb_row["deep_tail"]["first_n"])
        deep_C, deep_record = deep_first_moment_bound(block, first_n, centers, radii, lam, s)
        C = (sum(moments, arb(0)) + deep_C).upper()
        A = direct_sups[0].upper()
        q = (abs(centers[j - 1]) / radii[j - 1]).upper()
        low_bounds[block] = [A] + [min(direct_sups[k].upper(), tail_envelope(A, C, q, rho, k).upper()) for k in range(1, args.K_head + 1)]
        high_params[block] = {"A": A, "C": C, "q": q, "rho": rho}
        records.append({"block": list(block), "label": tb.label_for(block), "kind": "hurwitz_closed_tail_family", "A_upper_bound": arb_text(A), "C_upper_bound": arb_text(C), "q_upper_bound": arb_text(q), "rho_upper_bound": arb_text(rho), "direct_column_sups": [arb_text(v) for v in direct_sups], "worst_arcs": worst_arcs, "head_first_moments": heads, "deep_first_moment": deep_record, "selected_column_bounds": [arb_text(v) for v in low_bounds[block]]})
        print(f"Q8_R2_LOCAL block={tb.label_for(block)} A={arb_text(A)} C={arb_text(C)} rho={arb_text(rho)}", flush=True)
    b_head = []
    for k in range(args.K_head + 1):
        by_input = {j: sum((low_bounds[b][k] for b in blocks if b[1] == j), arb(0)).upper() for j in range(1, KAPPA + 1)}
        b_head.append({"k": k, "input_component_bounds": {str(j): arb_text(v) for j, v in by_input.items()}, "b_k_upper_bound": arb_text(sum(by_input.values(), arb(0)).upper())})
    def block_tail(block, N):
        p = high_params[block]
        return tail_block_tail(p["A"], p["C"], p["q"], p["rho"], N) if block[4] else single_block_tail(p["weight"], p["rho"], N)
    tail_bounds = {}
    for N in args.N_targets:
        vals = {tb.label_for(b): block_tail(b, N) for b in blocks}
        total = sum(vals.values(), arb(0)).upper()
        tail_bounds[str(N)] = {"N": N, "T_tail_upper_bound": arb_text(total), "by_block": {k: arb_text(v) for k, v in vals.items()}}
        print(f"Q8_R2_LOCAL N={N} T_tail={arb_text(total)}", flush=True)
    high_start = args.K_head + 1
    B_total = (sum((arb(row["b_k_upper_bound"]) for row in b_head), arb(0)) + sum((block_tail(b, high_start) for b in blocks), arb(0))).upper()
    receipt = {"schema": "q8-r2-local/v1", "status": "CERTIFIED_R2_COLUMN_ENVELOPE_R3_PENDING", "theorem_grade_verdict": "NO", "analytic_linkage": "OPEN", "q": 8, "sign": 1, "M": args.M, "K_head": args.K_head, "precision_bits": 384, "pin": {"re": PIN_RE, "im": PIN_IM, "half_width": HALF_WIDTH}, "geometry": {"lambda": arb_text(lam), "centers": [arb_text(v) for v in centers], "source_radii": [arb_text(v) for v in radii]}, "blocks": records, "b_k_head": b_head, "B_total_full_operator_column_sum_upper_bound": arb_text(B_total), "tail_bounds": tail_bounds, "source_bindings": {"engine": str((TRACKED_ENGINE_DIR / "zeta_cert_rosen_q5.py").resolve()), "TB": str(args.tb.resolve()), "TB_sha256": sha256(args.tb), "W": str(args.w.resolve()), "W_sha256": sha256(args.w)}, "runtime_seconds": time.perf_counter() - started}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"receipt": str(args.out.resolve()), "B_total": receipt["B_total_full_operator_column_sum_upper_bound"], "T_tail": {k: v["T_tail_upper_bound"] for k, v in tail_bounds.items()}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
