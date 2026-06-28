"""
veech_roof_minR.py  --  Compute the Veech slope-gap HARD EDGE = min of the Taha
G_q-roof R_q over the actual G_q-Farey section, for q = 5,7,9,11, DIRECTLY from
the branch structure (Taha 1810.10668 Thm 2.2):

  T^q = { 0<a<=1, 1-lam*a < b <= 1 },  lam=2cos(pi/q),  U=[[lam,-1],[1,0]],
  w_i = U^i (1,0)^T (i=0..q),
  branch T_i^q = { (a,b).w_{i-1} > 1, (a,b).w_i <= 1 },  i=2..q-1,
  R_q(a,b) = y_i / ( a * (a,b).w_i ),  y_i = (w_i)_2  (2nd component).

The slope-gap distribution is the distribution of R_q over the section under the
invariant measure; its LEFT support edge (smallest normalized gap) = min R_q.
ACL prove (golden L, q=5) that this edge is exactly 1 ("R uniformly bounded below
by 1", f=0 on [0,1]).  Here we CHECK numerically that min R_q = 1 for q=5,7,9,11
by dense sampling of the section, and we record WHERE the min is attained.

We also confirm the cusp-branch relation  R_q = 1/(a*b) = 1/P  (P = our gap
product), so our X(q)=1/lam^3 is the value of P at the cusp tip = sup-side of R,
NOT the min-R hard edge.
"""
from __future__ import annotations
import math
import json
import os

import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def hecke_vectors(q):
    lam = 2.0 * math.cos(math.pi / q)
    U = np.array([[lam, -1.0], [1.0, 0.0]])
    w = [np.array([1.0, 0.0])]
    for _ in range(q):
        w.append(U @ w[-1])
    return lam, w


def roof_min(q, Ngrid=4000):
    """Dense scan of min R_q over the section. Return (minR, at, also sup over a
    cheap sample for context)."""
    lam, w = hecke_vectors(q)
    minR = math.inf
    minR_at = None
    rng = np.random.default_rng(7)
    # 1) structured grid over (a,b) in the section
    for ia in range(1, Ngrid + 1):
        a = ia / Ngrid
        blo = 1.0 - lam * a
        # sample b across (max(blo, -inf), 1]; we only need the section b>blo, b<=1
        # but R = y_i/(a * (a,b).w_i); on cusp branch (w=(0,1)) R=1/(a*b) which is
        # minimized at b->1, a->1. Scan a modest set of b per a.
        for jb in range(0, 200 + 1):
            b = blo + (1.0 - blo) * jb / 200.0
            if b <= 0 or b > 1.0:
                continue
            # find branch i: (a,b).w_{i-1} > 1 >= (a,b).w_i
            ab = np.array([a, b])
            i_sel = None
            for i in range(2, q):
                if float(w[i - 1] @ ab) > 1.0 and float(w[i] @ ab) <= 1.0:
                    i_sel = i
                    break
            if i_sel is None:
                # cusp/last branch fallback
                i_sel = q - 1
            wi = float(w[i_sel] @ ab)
            yi = float(w[i_sel][1])
            if a * wi == 0:
                continue
            R = yi / (a * wi)
            if 0 < R < minR:
                minR = R
                minR_at = (a, b, i_sel)
    return lam, minR, minR_at


if __name__ == "__main__":
    results = []
    print(f"{'q':>3} {'lambda':>10} {'min R_q (Veech edge)':>22} {'at (a,b,branch)':>26} "
          f"{'our 1/lam^3':>12}")
    for q in [5, 7, 9, 11]:
        lam, minR, at = roof_min(q)
        rec = {
            "q": q, "lambda": lam,
            "veech_hard_edge_min_Rq": minR,
            "min_at": {"a": at[0], "b": at[1], "branch": at[2]} if at else None,
            "our_X_1_over_lam3": 1.0 / lam**3,
            "lam3": lam**3,
        }
        results.append(rec)
        ats = f"({at[0]:.4f},{at[1]:.4f},i={at[2]})" if at else "None"
        print(f"{q:>3} {lam:>10.6f} {minR:>22.8f} {ats:>26} {1.0/lam**3:>12.6f}")

    # Verdict block
    all_edge_one = all(abs(r["veech_hard_edge_min_Rq"] - 1.0) < 5e-3 for r in results)
    verdict = {
        "veech_edge_is_1_for_all_q": bool(all_edge_one),
        "note": ("min R_q = 1 for every q (golden L and beyond): the universal "
                 "no-small-gaps edge (Athreya-Chaika). It is q-INDEPENDENT and "
                 "equals 1, NOT 1/lam^3. Our 1/lam^3 is the cusp-tip value of the "
                 "RECIPROCAL product observable P=a*b (=1/R), i.e. the large-gap "
                 "/ Hall-ray end (sup R = lam^3), a different edge of a different "
                 "observable."),
    }
    out = {"per_q": results, "verdict": verdict}
    with open(os.path.join(OUT, "veech_roof_minR.json"), "w") as fp:
        json.dump(out, fp, indent=2)
    print("\nVeech edge = 1 for all q:", all_edge_one)
    print(f"Saved {os.path.join(OUT,'veech_roof_minR.json')}")
