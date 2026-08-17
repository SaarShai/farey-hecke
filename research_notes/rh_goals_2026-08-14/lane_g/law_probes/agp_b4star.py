#!/usr/bin/env python3
"""
agp_b4star.py -- LANE G: direct test of the (B4*) budget premise at ARITHMETIC q,
where phi_q is known in CLOSED FORM and no determinant pipeline is involved.

WHAT IS BEING TESTED.  LAW_SELFBOUND_TRACE.md sec.1.1 quotes HJL Lemma 5.3 as

    -phi'/phi(1/2+ir) - SUM_k (1 - s_{k,q}) / ((s_{k,q}-1/2)^2 + r^2) >= 2 log q_{M_q} > 0

and the lane's sec.1.2(d) identifies q_{M_q} = q for the Hecke group G_q.  Since the
subtracted sum is NON-NEGATIVE for s_k in (1/2, 1] (both transcriptions -- see the
parent's sec.1.5 discrepancy -- have non-negative numerators there), the quoted lemma
implies the strictly weaker, fully testable

        (B4-POINTWISE)      -(phi_q'/phi_q)(1/2+ir)  >=  2 log q     for all real r.

At q = 3, 4, 6 the Hecke group is arithmetic and phi_q is the exact closed form
(mirror_u4.py:phi_exact, standard).  This probe scans r and reports
inf_r LHS(q,r), hence an upper bound on 2 log q_{M_q} -- i.e. on what the cited
lemma can possibly be asserting.

NO determinant, NO transfer operator, NO Teo kernel is used here.  The only inputs
are Gamma, zeta and the closed form, so the result is independent of every
MEASURED ingredient in the lane.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 agp_b4star.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agp_phi as A                                                  # noqa: E402
from mpmath import mp, mpf                                           # noqa: E402

RANGES = [(2.0, 12.0, 1001), (12.0, 40.0, 1401), (0.5, 2.0, 301)]


def main():
    mp.dps = 30
    out = {"probe": "agp_b4star",
           "tests": "(B4-POINTWISE): -(phi'/phi)(1/2+ir) >= 2 log q, at arithmetic q",
           "inputs": "exact closed-form phi only; no determinants, no Teo kernel",
           "method": "analytic log-derivative via mp.diff on log phi_exact",
           "rows": []}
    for q in (3, 4, 6):
        two = 2.0 * math.log(q)
        allvals = []
        for (a, b, n) in RANGES:
            for i in range(n):
                r = a + (b - a) * i / (n - 1)
                v = float(A.minus_dlogphi_exact_analytic(q, r).real)
                allvals.append((r, v))
        mn = min(allvals, key=lambda t: t[1])
        viol = [t for t in allvals if t[1] < two]
        row = {"q": q, "two_log_q": two,
               "n_samples": len(allvals),
               "inf_LHS": mn[1], "argmin_r": mn[0],
               "n_violations": len(viol),
               "frac_violating": len(viol) / len(allvals),
               "implied_max_2logqM": mn[1],
               "implied_max_qM": math.exp(mn[1] / 2) if mn[1] > -50 else None,
               "B4_pointwise_holds": bool(len(viol) == 0),
               "mean_over_2_to_12": sum(v for r, v in allvals if 2 <= r <= 12)
                                    / max(1, sum(1 for r, v in allvals if 2 <= r <= 12)),
               "sample_violations": [{"r": r, "LHS": v} for r, v in viol[:12]]}
        out["rows"].append(row)
        print(f"q={q}: 2log q={two:.5f}  inf_r LHS={mn[1]:.6f} at r={mn[0]:.4f}  "
              f"violations {len(viol)}/{len(allvals)} ({100*row['frac_violating']:.1f}%)  "
              f"=> q_M <= {row['implied_max_qM']:.4f}   "
              f"{'HOLDS' if row['B4_pointwise_holds'] else 'REFUTED'}", flush=True)

    out["verdict"] = {
        "B4_pointwise_with_qM_eq_q":
            "HOLDS" if all(r["B4_pointwise_holds"] for r in out["rows"]) else "REFUTED",
        "note": ("An upper bound on q_{M_q} follows from inf_r LHS: the cited lemma "
                 "cannot assert more than 2 log q_M <= inf_r LHS.")}
    print("\nVERDICT:", out["verdict"]["B4_pointwise_with_qM_eq_q"], flush=True)

    p = __file__.replace('.py', '.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
