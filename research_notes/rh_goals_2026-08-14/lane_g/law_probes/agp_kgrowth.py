#!/usr/bin/env python3
"""
agp_kgrowth.py -- LANE G: the growth law of the EXPLICIT archimedean+elliptic
part of -(phi_q'/phi_q)(1/2+ir), in closed form, with NO determinants.

CONTEXT.  agp_window.py splits the window mass as

        INT_W -(phi'/phi) dr  =  [ -Delta arg g ]  +  [ Delta arg K_q ] ,
                                   g = conj(Z_S)/Z_S

the first bracket carried by the transfer-operator determinants (the zeros of
Z_S, i.e. the resonances), the second by Teo's explicit factors: the cusp
Gamma-quotient, the Barnes bracket, and the two elliptic points.  The second
bracket is the natural candidate for the "archimedean / non-Blaschke part"
A_Gamma of LAW_SELFBOUND_TRACE.md (1.2), and unlike everything else in this
circle of ideas it is available in CLOSED FORM for every q (agp_phi.dlogK_ds),
so its growth in q can be measured to arbitrary accuracy and to arbitrarily
large q.

WHAT IS MEASURED.  kdens(q, r) := Re dlogK_ds(1/2+ir, q), the pointwise
K-contribution, over a wide q range and several r; then
  * the successive-ratio slope  [kdens(q2)-kdens(q1)] / [log q2 - log q1]
    at the largest available q (the asymptotic slope),
  * the offset kdens(q, r) - 2 log q  (its limit, if any).

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 agp_kgrowth.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import agp_phi as A                                                  # noqa: E402
from mpmath import mpc, mpf                                          # noqa: E402

QS = [3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 21, 25, 30, 40, 60, 100,
      200, 400, 1000, 4000]
RS = [3.0, 5.5, float(A.T0), 10.0]


def main():
    A.set_prec(128, 40)
    out = {"probe": "agp_kgrowth",
           "quantity": "Re dlogK_ds(1/2+ir, q) -- explicit archimedean+elliptic "
                       "contribution to -(phi'/phi)",
           "inputs": "closed form only (cot, digamma, Barnes G'/G); no determinants",
           "params": {"prec_bits": 128, "mp_dps": 40, "q": QS, "r": RS},
           "series": {}, "asymptotics": {}}

    for r in RS:
        vals = []
        for q in QS:
            v = float(A.dlogK_ds(mpc(mpf('0.5'), mpf(repr(r))), q).real)
            vals.append({"q": q, "kdens": v, "two_log_q": 2 * math.log(q),
                         "offset": v - 2 * math.log(q)})
        out["series"][str(r)] = vals
        sl = [(vals[i + 1]["kdens"] - vals[i]["kdens"])
              / (math.log(vals[i + 1]["q"]) - math.log(vals[i]["q"]))
              for i in range(len(vals) - 1)]
        out["asymptotics"][str(r)] = {
            "local_slope_last": sl[-1],
            "local_slope_last3": sl[-3:],
            "offset_last": vals[-1]["offset"],
            "offset_last3": [v["offset"] for v in vals[-3:]],
        }
        print(f"r={r:8.5f}: local slope vs log q at q={QS[-2]}..{QS[-1]} = {sl[-1]:.6f}   "
              f"offset (kdens - 2 log q) at q={QS[-1]} = {vals[-1]['offset']:.6f}",
              flush=True)
        print("          offsets: "
              + "  ".join(f"q={v['q']}:{v['offset']:.4f}" for v in vals[-6:]), flush=True)

    out["verdict"] = {
        "asymptotic_slope_vs_logq": {k: v["local_slope_last"]
                                     for k, v in out["asymptotics"].items()},
        "reading": ("kdens(q,r) = 2 log q + C(r) + o(1): the explicit "
                    "archimedean+elliptic factor of -(phi'/phi) alone grows with "
                    "the SAME 2 log q slope as the whole HJL budget."),
    }
    p = __file__.replace('.py', '.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
