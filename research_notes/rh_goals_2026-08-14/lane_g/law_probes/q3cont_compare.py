#!/usr/bin/env python3
"""
q3cont_compare.py -- LANE G: the verdict table.  Does the O(1) mirror residual
of LAW_TEO_KAPPA_CORRECTED.md Sec 3.1/3.4 disappear when the repo determinant
proxy P_3 is replaced by the INDEPENDENT classical Mayer determinant?

Inputs (both produced by this q3cont probe set, neither modified here):
  q3cont_repo_builder.json  -- P_3 from zeta_cert_rosen.py (flint/Arb, MMS eq.33)
  q3cont_mayer_indep.json   -- P_3 from the Gauss-map transfer operator (mpmath)

The kernel |phi_3(s)| |K_3(s)| is imported UNCHANGED from mirror_u4_corrected.py
(the Gamma_2 = 1/G corrected Teo assembly), so the only thing that differs
between the two ratio columns is the determinant evaluator.

PRE-REGISTERED READING (LAW_TEO_KAPPA_CORRECTED.md Sec 3.4's own hypothesis):
  * Mayer ratio ~ 1 while repo ratio reproduces 1.308/1.663/1.983
        => the residual IS the repo builder; U4 at q=3 and the corrected Teo
           kappa are both confirmed.
  * both ratios equal and != 1
        => the residual is NOT the builder; it sits in the kernel or in U4, and
           this lane must say so and stop.

Also reported, because it is the sharper statement:
  the per-point ratio P_repo / P_Mayer at Re s > 1 and at Re s < 0 separately.
  The mirror residual is the QUOTIENT of those two, so this column says how much
  of the residual comes from the mirror side and how much from the right side.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 q3cont_compare.py
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mpmath import mpf, mpc, fabs                                    # noqa: E402
from mirror_u4_corrected import K_q_corrected, phi_exact, TINF       # noqa: E402

SIGMAS = ('1.25', '1.40', '1.50')


def main():
    repo = json.load(open(HERE / "q3cont_repo_builder.json"))
    may = json.load(open(HERE / "q3cont_mayer_indep.json"))

    rp = {}
    for pt in repo["points"]:
        rp[round(pt["Re_s"], 4)] = pt["P"]
    mp_ = {}
    for pt in may["points"]:
        mp_[round(pt["Re_s"], 4)] = pt["P"]

    out = {"description": "verdict: is the O(1) mirror residual the repo "
                          "determinant builder?",
           "kernel": "mirror_u4_corrected.K_q_corrected (Gamma_2 = 1/G), unmodified",
           "inputs": ["q3cont_repo_builder.json", "q3cont_mayer_indep.json"],
           "rows": []}

    print(f"{'sig':>5} {'ratio_repo':>12} {'ratio_Mayer':>13} "
          f"{'P_repo/P_May @s':>16} {'@1-s':>10} {'residual=quot':>14}")
    for sg in SIGMAS:
        a, b = round(float(sg), 4), round(1 - float(sg), 4)
        if a not in rp or b not in rp or a not in mp_ or b not in mp_:
            print(f"  sigma={sg}: missing point"); continue
        ms = mpc(mpf(sg), TINF)
        phi = float(fabs(phi_exact(3, ms)))
        kk = float(fabs(K_q_corrected(ms, 3)))
        rhs = phi * kk
        lhs_repo = rp[b] / rp[a]
        lhs_may = mp_[b] / mp_[a]
        q_s = rp[a] / mp_[a]
        q_m = rp[b] / mp_[b]
        row = {"sigma": float(sg), "RHS_kernel": rhs,
               "P_repo_at_s": rp[a], "P_repo_at_1ms": rp[b],
               "P_mayer_at_s": mp_[a], "P_mayer_at_1ms": mp_[b],
               "LHS_repo": lhs_repo, "LHS_mayer": lhs_may,
               "ratio_repo": lhs_repo / rhs, "ratio_mayer": lhs_may / rhs,
               "P_repo_over_P_mayer_at_s": q_s,
               "P_repo_over_P_mayer_at_1ms": q_m,
               "residual_reconstructed_as_quotient": q_m / q_s}
        out["rows"].append(row)
        print(f"{sg:>5} {row['ratio_repo']:12.6f} {row['ratio_mayer']:13.9f} "
              f"{q_s:16.6f} {q_m:10.6f} {q_m/q_s:14.6f}")

    rm = [r["ratio_mayer"] for r in out["rows"]]
    rr = [r["ratio_repo"] for r in out["rows"]]
    if rm:
        out["verdict"] = {
            "mayer_ratio_max_abs_dev_from_1": max(abs(x - 1) for x in rm),
            "repo_ratio_range": [min(rr), max(rr)],
            "mayer_max_abs_log10": max(abs(math.log10(abs(x))) for x in rm),
            "call": ("residual IS the repo determinant builder"
                     if max(abs(x - 1) for x in rm) < 1e-3
                     else "residual is NOT localised to the builder")}
        print(f"\nMayer ratios deviate from 1 by at most "
              f"{out['verdict']['mayer_ratio_max_abs_dev_from_1']:.3e}")
        print("VERDICT:", out["verdict"]["call"])

    p = str(Path(__file__).with_suffix('.json'))
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
