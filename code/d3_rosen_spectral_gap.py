"""
d3_rosen_spectral_gap.py
========================
Per-q spectral-gap table for the 1-D Rosen lambda_q-CF transfer (Ruelle) operator.

GOAL
----
Determine whether the 1-D Rosen-CF transfer operator has a numerically STABLE,
ISOLATED spectral gap (the precondition for any certified effective
decay-of-correlations result), and produce the first per-q gap table

    alpha_q = -log|lambda_2 / lambda_1|

where lambda_1 >= |lambda_2| >= ... are the moduli of the operator's eigenvalues
at the conformal parameter s = D_q (the bounded-type dimension, where the leading
eigenvalue lambda_1 = 1 by construction of the Bowen/pressure equation).

STRUCTURAL CAVEAT (DO NOT VIOLATE)
----------------------------------
The 2-D BCZ-Farey horocycle section is parabolic / zero-entropy with POLYNOMIAL
mixing (C(n) ~ n^-0.9), NO spectral gap, 1 in essential spectrum
(research_notes/bcz_mixing_rate_2026-06-14.md). This 1-D CF-map gap therefore
does NOT prove horocycle effective equidistribution. The deliverable is the
1-D CF-map decay-of-correlations gap ONLY.

METHOD
------
We reuse the EXACT operator builders from d3_rosen_round3.py:
  - _build_gauss_q3(digits, s, N)        : Gauss map (q=3), branches 1/(a+x) on [0,1]
  - _build_full_rosen_qge4(lam, digits, s, N) : full both-sign Rosen op on [0, lam/2]
  - dim_full_rosen(q, B, N)              : bisects max-eigenvalue to 1 -> D_q(B)

At s = D_q the discretized operator matrix M has spectral radius ~ 1 (lambda_1).
The gap is gap = |lambda_2| / |lambda_1| and alpha_q = -log(gap). A clean isolated
gap means |lambda_2| is well-separated from |lambda_1| ~ 1 and stable as the
collocation resolution N grows.
"""

from __future__ import annotations
import math
import json
import os
import numpy as np

import d3_rosen_round3 as r3

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

KNOWN_E12 = 0.5312805062772051416   # q=3, B=2 Jenkinson-Pollicott guardrail


def build_operator(q, digits, s, N):
    """Build the transfer-operator matrix M at parameter s for given q."""
    lam = 2.0 * math.cos(math.pi / q)
    if q == 3:
        return r3._build_gauss_q3(digits, s, N)
    return r3._build_full_rosen_qge4(lam, digits, s, N)


def spectrum_sorted(M):
    """Return eigenvalue moduli sorted descending (and the complex eigenvalues)."""
    ev = np.linalg.eigvals(M)
    mods = np.abs(ev)
    order = np.argsort(mods)[::-1]
    return mods[order], ev[order]


def gap_at(q, digits, s, N):
    """Compute lambda_1, lambda_2, gap=lambda_2/lambda_1, alpha=-log(gap)."""
    M = build_operator(q, digits, s, N)
    mods, ev = spectrum_sorted(M)
    l1 = float(mods[0])
    l2 = float(mods[1]) if len(mods) > 1 else 0.0
    gap = l2 / l1 if l1 > 0 else float("nan")
    alpha = -math.log(gap) if gap > 0 else float("inf")
    return {
        "lambda1": l1,
        "lambda2": l2,
        "lambda3": float(mods[2]) if len(mods) > 2 else 0.0,
        "gap": gap,
        "alpha": alpha,
    }


def main():
    print("=" * 74)
    print("D3 SPECTRAL GAP: 1-D Rosen lambda_q-CF transfer operator")
    print("  alpha_q = -log|lambda_2/lambda_1| at s = D_q (Bowen dimension).")
    print("  CAVEAT: 1-D CF-map decay-of-correlations gap ONLY.")
    print("          Does NOT touch the 2-D parabolic horocycle (no gap there).")
    print("=" * 74)

    N_DEFAULT = 80
    B_DIM = 12   # truncation for D_q computation

    # ── STEP 0: HARD GUARDRAIL ──────────────────────────────────────────────
    print("\nSTEP 0: HARD GUARDRAIL  (q=3, B=2 -> 0.5312805062772051416)")
    d_guard = r3.dim_gauss_q3(2, N=N_DEFAULT)
    residual = d_guard - KNOWN_E12
    print(f"  computed = {d_guard:.16f}")
    print(f"  known    = {KNOWN_E12:.16f}")
    print(f"  residual = {residual:.3e}")
    guard_pass = abs(residual) < 1e-10
    print(f"  {'GUARDRAIL PASS' if guard_pass else 'GUARDRAIL FAIL'}")
    if not guard_pass:
        print("\n  STOP: operator code does not reproduce the q=3 anchor to 1e-10.")
        print("        Nothing downstream is trustworthy. Aborting.")
        out = {"guardrail": {"computed": float(d_guard), "known": KNOWN_E12,
                             "residual": float(residual), "pass": False},
               "aborted": True}
        with open(os.path.join(OUT, "d3_rosen_spectral_gap.json"), "w") as f:
            json.dump(out, f, indent=2)
        raise SystemExit("Guardrail failed; aborted.")

    # ── STEP 1: per-q gap at N=80 ───────────────────────────────────────────
    q_vals = [5, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18, 20, 21]
    digits = list(range(1, B_DIM + 1))

    print(f"\nSTEP 1: per-q gap table  (B={B_DIM} for D_q, N={N_DEFAULT})")
    print(f"  {'q':>3}  {'lam':>8}  {'D_q':>11}  {'lam1':>11}  {'lam2':>11}  "
          f"{'gap':>11}  {'alpha_q':>10}")
    print("-" * 78)

    per_q = {}
    for q in q_vals:
        lam = 2.0 * math.cos(math.pi / q)
        Dq = r3.dim_full_rosen(q, B_DIM, N=N_DEFAULT)
        g = gap_at(q, digits, Dq, N_DEFAULT)
        per_q[q] = {"lambda": float(lam), "D_q": float(Dq), **g}
        print(f"  {q:3d}  {lam:8.5f}  {Dq:11.8f}  {g['lambda1']:11.8f}  "
              f"{g['lambda2']:11.8f}  {g['gap']:11.8f}  {g['alpha']:10.6f}")

    # ── STEP 2: N-convergence study ─────────────────────────────────────────
    N_grid = [40, 60, 80, 100, 120]
    print(f"\nSTEP 2: N-convergence of gap (and alpha)  N in {N_grid}")
    print("  Re-computes D_q at each N, rebuilds M, reports gap & delta(gap).")

    conv = {}
    max_drift_overall = 0.0
    for q in q_vals:
        lam = 2.0 * math.cos(math.pi / q)
        print(f"\n  q={q}  (lam={lam:.5f})")
        print(f"    {'N':>5}  {'D_q':>11}  {'lam1':>11}  {'lam2':>11}  "
              f"{'gap':>13}  {'alpha':>10}  {'d(gap)':>11}")
        rows = []
        prev_gap = None
        max_drift_q = 0.0
        for N in N_grid:
            Dq = r3.dim_full_rosen(q, B_DIM, N=N)
            g = gap_at(q, digits, Dq, N)
            d_gap = abs(g["gap"] - prev_gap) if prev_gap is not None else float("nan")
            if not math.isnan(d_gap):
                max_drift_q = max(max_drift_q, d_gap)
            dgap_s = f"{d_gap:.3e}" if not math.isnan(d_gap) else "      ---"
            print(f"    {N:5d}  {Dq:11.8f}  {g['lambda1']:11.8f}  "
                  f"{g['lambda2']:11.8f}  {g['gap']:13.10f}  {g['alpha']:10.6f}  "
                  f"{dgap_s:>11}")
            rows.append({"N": N, "D_q": float(Dq), "lambda1": g["lambda1"],
                         "lambda2": g["lambda2"], "gap": g["gap"],
                         "alpha": g["alpha"],
                         "delta_gap": None if math.isnan(d_gap) else float(d_gap)})
            prev_gap = g["gap"]
        # drift between the two finest grids (N=100,120) is the headline stability number
        fine_drift = abs(rows[-1]["gap"] - rows[-2]["gap"])
        conv[q] = {"rows": rows, "max_drift": float(max_drift_q),
                   "fine_drift_100_120": float(fine_drift)}
        max_drift_overall = max(max_drift_overall, fine_drift)
        stable = fine_drift < 1e-6
        print(f"    => max d(gap) across grid = {max_drift_q:.3e}; "
              f"fine drift (100->120) = {fine_drift:.3e}  "
              f"[{'STABLE <1e-6' if stable else 'DRIFT >1e-6 (FLAG)'}]")

    # ── STEP 3: verdict ─────────────────────────────────────────────────────
    print("\n" + "=" * 74)
    print("STEP 3: STABILITY VERDICT")
    stable_qs = [q for q in q_vals if conv[q]["fine_drift_100_120"] < 1e-6]
    unstable_qs = [q for q in q_vals if conv[q]["fine_drift_100_120"] >= 1e-6]
    print(f"  Stable (fine drift N=100->120 < 1e-6): {stable_qs}")
    print(f"  Unstable / flagged (>= 1e-6):          {unstable_qs}")
    print(f"  Overall max fine drift: {max_drift_overall:.3e}")
    if unstable_qs:
        print("  FLAG: collocation has NOT resolved the gap to 1e-6 for the flagged q;"
              " certification premature there.")
    else:
        print("  All q: gap stable under N-refinement to < 1e-6.")

    out = {
        "description": "1-D Rosen lambda_q-CF transfer operator spectral gap "
                       "alpha_q = -log|lambda_2/lambda_1| at s=D_q.",
        "caveat": "1-D CF-map decay-of-correlations gap ONLY; does NOT imply "
                  "horocycle effective equidistribution (2-D BCZ section is "
                  "parabolic/zero-entropy, no gap, 1 in essential spectrum).",
        "B_dim": B_DIM,
        "N_default": N_DEFAULT,
        "N_grid": N_grid,
        "guardrail": {"computed": float(d_guard), "known": KNOWN_E12,
                      "residual": float(residual), "pass": True},
        "per_q_gap": {str(q): per_q[q] for q in q_vals},
        "N_convergence": {str(q): conv[q] for q in q_vals},
        "stability": {
            "stable_qs": stable_qs,
            "unstable_qs": unstable_qs,
            "max_fine_drift": float(max_drift_overall),
            "threshold": 1e-6,
        },
    }
    out_json = os.path.join(OUT, "d3_rosen_spectral_gap.json")
    with open(out_json, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  Saved: {out_json}")
    return out


if __name__ == "__main__":
    main()
