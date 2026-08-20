#!/usr/bin/env python3
"""Independent mpmath cross-check of the L-OUT receipt (no Arb, no flint).

Recomputes, in plain mpmath floating point at 60 digits:
  * rho_theta for every block from the exact Moebius image (n swept to 400
    plus the crude deep-tail bound);
  * the per-block trace tau_out(N) = theta^-N * sum_{k<N} M_k;
  * the Schur telescoping full_tau(N) using the hs factors quoted by the
    certified checker;
  * the smallest N with full_tau(N) <= 1e-15.
Agreement with the Arb pipeline is a cross-check only; the Arb run is the
certified one.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from mpmath import mp, mpf

mp.dps = 60

HS_FACTORS = {"A2": "37.1900706769", "A3": "22.7436858371", "B1": "13.3870991026",
              "B2": "4.07640688778", "B3": "11.3345795885"}
NAME_TO_BLOCKS = {
    "A2": [(2, 1, 1, False, False)], "A3": [(3, 2, 1, False, False)],
    "B1": [(1, 3, 2, False, True), (1, 3, 1, True, True)],
    "B2": [(2, 3, 2, False, True), (2, 3, 1, True, True)],
    "B3": [(3, 3, 2, False, True), (3, 3, 1, True, True)],
}
OUTPUT_DISC = {"A2": 2, "A3": 3, "B1": 1, "B2": 2, "B3": 3}


def mid(text: str) -> mpf:
    """Midpoint of an Arb ball string such as '[0.5024998 +/- 1e-21]'."""

    match = re.match(r"\[?\s*([-+0-9.eE]+)", text.strip())
    return mpf(match.group(1))


def mobius_rho(block, centers, radii, radius_theta, lam, n_sweep):
    i, j, n0, neg, tail = block
    c_i, c_j, r_j = centers[i - 1], centers[j - 1], radii[j - 1]
    top = n_sweep if tail else n0
    best = mpf(0)
    for n in range(n0, top + 1):
        a = c_i - n * lam if neg else c_i + n * lam
        denominator = a * a - radius_theta * radius_theta
        centre = a / denominator if neg else -a / denominator
        best = max(best, (abs(centre - c_j) + radius_theta / denominator) / r_j)
    if tail:
        denominator = (top + 1) * lam - abs(c_i) - radius_theta
        best = max(best, (1 / denominator + abs(c_j)) / r_j)
    return best


def block_terms(row, K):
    if row["kind"] == "single_branch":
        weight = mid(row["weight_theta_sup_upper_bound"])
        rho = mid(row["rho_theta_upper_bound"])
        return [weight * rho**k for k in range(K)]
    A, C = mid(row["A_theta_upper_bound"]), mid(row["C_theta_upper_bound"])
    q, rho = mid(row["q_upper_bound"]), mid(row["rho_theta_upper_bound"])
    return [A] + [A * q**k + C * k * rho ** (k - 1) for k in range(1, K)]


def full_tau(rows, theta, N, input_tail):
    tau = {}
    for name, blocks in NAME_TO_BLOCKS.items():
        total = mpf(0)
        for block in blocks:
            total += theta[OUTPUT_DISC[name] - 1] ** (-N) * sum(block_terms(rows[block], N))
        tau[name] = total
    a2, a3 = mpf(HS_FACTORS["A2"]), mpf(HS_FACTORS["A3"])
    b1, b2 = mpf(HS_FACTORS["B1"]), mpf(HS_FACTORS["B2"])
    out = (tau["B3"] + a3 * tau["B2"] + a3 * a2 * tau["B1"]
           + tau["A3"] * b2 + tau["A3"] * a2 * b1 + a3 * tau["A2"] * b1)
    return out, input_tail + out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lout", type=Path, required=True)
    parser.add_argument("--check", type=Path, required=True)
    parser.add_argument("--n-sweep", type=int, default=400)
    args = parser.parse_args()
    lout = json.loads(args.lout.read_text(encoding="utf-8"))
    check = json.loads(args.check.read_text(encoding="utf-8"))
    lam = mid(lout["geometry"]["lambda"])
    centers = [mid(v) for v in lout["geometry"]["centers"]]
    radii = [mid(v) for v in lout["geometry"]["source_radii"]]
    theta = [mpf(t) for t in lout["theta_exact_strings"]]
    radii_theta = [theta[i] * radii[i] for i in range(3)]
    rows = {tuple(row["block"]): row for row in lout["blocks"]}

    print("rho_theta cross-check (mpmath exact Moebius vs Arb receipt):")
    worst = mpf(0)
    for block, row in rows.items():
        own = mobius_rho(block, centers, radii, radii_theta[block[0] - 1], lam, args.n_sweep)
        receipt = mid(row["rho_theta_upper_bound"])
        rel = abs(receipt - own) / own
        worst = max(worst, rel)
        print(f"  {row['label']:<18} receipt={mp.nstr(receipt,12):<16} mpmath={mp.nstr(own,12):<16} rel_diff={mp.nstr(rel,3)}")
    print(f"  worst relative difference: {mp.nstr(worst, 3)}")

    print("full_tau cross-check (mpmath vs Arb checker):")
    for key, row in sorted(check["condition_5_full_tau"]["rows"].items(), key=lambda kv: int(kv[0])):
        N = int(key)
        out, total = full_tau(rows, theta, N, mid(row["input_tail_only"]))
        arb_total = mid(row["full_tau"])
        rel = abs(total - arb_total) / arb_total
        print(f"  N={N:<4} mpmath={mp.nstr(total,10):<16} arb={mp.nstr(arb_total,10):<16} rel_diff={mp.nstr(rel,3)}")

    input_by_n = {int(k): mid(v["input_tail_only"])
                  for k, v in check["condition_5_full_tau"]["rows"].items()}
    largest_input = input_by_n[max(input_by_n)]
    crossing = None
    for N in range(100, 400):
        _, total = full_tau(rows, theta, N, largest_input)
        if total <= mpf("1e-15"):
            crossing = N
            break
    print(f"smallest N with full_tau <= 1e-15 (mpmath, input tail bounded by {mp.nstr(largest_input,4)}): {crossing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
