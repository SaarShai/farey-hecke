#!/usr/bin/env python3
"""
mirror_arith.py -- LANE G, TASK B discriminator.

mirror_u4.py finds P_q(1-s)/P_q(s) disagreeing with |kappa_q(s)| by 12-19
orders of magnitude at q = 12,16,22,30, with the determinant N-converged to
1e-16 at BOTH s and 1-s.  Exactly one of three things must be false:
  (a) U4 -- the det product is |Z_{G_q}|,
  (b) the Teo kappa assembly as transcribed in LAW_U1_GROWTH.md Sec 3.1,
  (c) the phi_q evaluator.
This run removes (c) entirely: at q = 3, 4, 6 phi_q is the exact closed form
(g(s), and M1F (3.6)), so any surviving disagreement is (a) or (b).
"""
import json, math, sys
from pathlib import Path
REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import zeta_cert_rosen_even as E
from flint import acb, arb, ctx
from mpmath import mp, mpf, mpc, gamma, sqrt, pi, sin, tan, barnesg, fabs, power, zeta
from mirror_u4 import K_q, P_q
mp.dps = 30
TINF = mpf('7.0673625708673465')

def g_of_s(s):
    return sqrt(pi)*gamma(s-mpf(1)/2)*zeta(2*s-1)/(gamma(s)*zeta(2*s))

def phi_exact(q, s):
    if q == 3: return g_of_s(s)
    p = {4: 2, 6: 3}[q]
    return g_of_s(s)*(1+mpf(p)**(1-s))/(1+mpf(p)**s)

def main():
    ctx.prec = 400
    N = 32
    out = {"description": "TASK B discriminator: mirror test at arithmetic q "
                          "where phi_q is EXACT", "rows": []}
    for q in (3, 4, 6):
        for sg in ('1.25', '1.50'):
            s = complex(float(sg), float(TINF))
            ms = mpc(mpf(sg), TINF)
            try:
                ps = P_q(q, s, N); pm = P_q(q, complex(1-s.real, -s.imag), N)
            except Exception as exc:
                print(f"q={q} sigma={sg} DET FAIL {exc!r}"[:160], flush=True); continue
            if not (math.isfinite(ps["P"]) and math.isfinite(pm["P"])):
                print(f"q={q} sigma={sg} non-finite det", flush=True); continue
            lhs = pm["P"]/ps["P"]
            phi = phi_exact(q, ms); kk = K_q(ms, q)
            rhs = float(fabs(phi)*fabs(kk))
            r = {"q": q, "sigma": float(sg), "P_at_s": ps["P"], "P_at_1ms": pm["P"],
                 "LHS_ratio": lhs, "abs_phi_exact": float(fabs(phi)),
                 "abs_K": float(fabs(kk)), "RHS_kappa": rhs,
                 "ratio_LHS_over_RHS": lhs/rhs}
            out["rows"].append(r)
            print(f"q={q} sigma={sg}: P(s)={ps['P']:.4e} P(1-s)={pm['P']:.4e} "
                  f"LHS={lhs:.6e} |phi|exact={float(fabs(phi)):.6e} |K|={float(fabs(kk)):.4e} "
                  f"RHS={rhs:.6e}  ratio={lhs/rhs:.4e}", flush=True)
    with open(__file__.replace('.py', '.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)

if __name__ == "__main__":
    main()
