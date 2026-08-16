"""q=7 T-b disc-geometry block source (analogue of lane_g/tb_disc_sweep.py).

The BLOCKS assignment below is the AUTHORITATIVE 19-block eq.(34) structure of
the reduced q=7 operator, captured verbatim from
``zeta_mayer_rosen.build_reduced_matrix`` (q=7, sign=+1, n_head=4) via
``family_prep_constants.capture_allowed_blocks`` and cross-checked against
F7_CONSTANTS_MANIFEST.md section 3 (9 heads + 10 Hurwitz tails).  Tuple format
is the q=5 one: ``(out_i, in_j, n, neg, is_tail)``, 1-indexed.

The float sweep at the bottom is NON-RIGOROUS PREPARATION only; the certified
values come from f7_certify_tb_blocks.py (Arb).  This file exists so the Arb
certifier can bind to a single hashed, AST-parsed block source, exactly as the
q=5 chain binds to lane_g/tb_disc_sweep.py.
"""
import math, sys, json
sys.path.insert(0, "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
from zeta_mayer_rosen import hecke_params, partition_points
import numpy as np

q = 7
lam, hq, kappa = hecke_params(q)
pts = partition_points(q)
half = [(pts[i]-pts[i-1])/2 for i in range(1,len(pts))]
cs   = [(pts[i]+pts[i-1])/2 for i in range(1,len(pts))]
th = np.exp(2j*np.pi*np.arange(4096)/4096)

def theta(z, n, neg):
    return 1.0/(z - n*lam) if neg else -1.0/(z + n*lam)

# allowed blocks (out_i, in_j, n, neg, is_tail) 1-indexed, from eq.34 code
BLOCKS = [(1,4,2,False,False),(1,5,3,False,True),(1,4,1,True,False),(1,5,2,True,True),
          (2,5,2,False,True),(2,4,1,True,False),(2,5,2,True,True),
          (3,1,1,False,False),(3,5,2,False,True),(3,4,1,True,False),(3,5,2,True,True),
          (4,2,1,False,False),(4,5,2,False,True),(4,4,1,True,False),(4,5,2,True,True),
          (5,3,1,False,False),(5,5,2,False,True),(5,4,1,True,False),(5,5,2,True,True)]
NTAIL = 80
# ADOPTED disc inflation factors (F7_MITIGATION_REPORT.md section 7, option 2).
FACTORS = (3.522, 2.622, 2.372, 1.79, 1.6)

if __name__ == "__main__":
    print("factors | rho_star | worst block | N for tail 1e-7 (per-mode rho^N)")
    results = []
    for factors in (FACTORS,):
        rho = 0.0
        worst = None
        for (i, j, n, neg, tail) in BLOCKS:
            z = cs[i-1] + factors[i-1]*half[i-1]*th
            ns = range(n, NTAIL) if tail else [n]
            for nn in ns:
                img = theta(z, nn, neg)
                r = np.max(np.abs(img - cs[j-1]))/(factors[j-1]*half[j-1])
                if r > rho:
                    rho, worst = r, (i, j, (-nn if neg else nn))
        N7 = math.log(1e-7)/math.log(rho) if rho < 1 else float('inf')
        print(f"{factors} | {rho:.12f} | {worst} | {N7:.0f}")
        results.append({"factors": list(factors), "rho_star": float(rho),
                        "worst_block": list(worst),
                        "N_1e-7": (None if rho >= 1 else N7),
                        "label": "NON-RIGOROUS FLOAT PREPARATION"})
    json.dump(results, open("/Users/za/Documents/farey-hecke/research_notes/"
                            "rh_goals_2026-08-14/lane_f/f7_tb_disc_sweep.json", "w"), indent=1)
