#!/usr/bin/env python3
"""
mirror_u4.py -- LANE G, TASK B: the U4 mirror test.

The guard (lane_g/law_probes/probe_u1_sup.py) uses the PROXY
    P_q(s) := | det(1 - L^+_{s,q}) * det(1 - L^-_{s,q}) |
for |Z_{G_q}(s)|.  The identification P_q = |Z_{G_q}| is obligation U4, a GAP
for q != 5.  The phi_q side (lane_g/LAW_U1PHI_PROOF_ROUTE.md) computes phi_q
independently, from the Eisenstein constant term.  The two have never been
compared.

THE COMPARABLE COMBINATION.  P_q and phi_q are not the same kind of object;
what IS comparable is the functional-equation kernel.  Teo Prop. 2.5
(LAW_U1_GROWTH.md Sec 3.1) gives Z_{G_q}(1-s) = kappa_q(s) Z_{G_q}(s) with

  kappa_q(s) = (+-1) * 2^{-(2s-1)} * phi_q(s) * tan(pi s/2)^{1/2} * E_q(s)
               * [ (2pi)^{2s-1} G2(s)^2 Gamma(1-s) / (G2(1-s)^2 Gamma(s)) ]^{(1-2/q)/2}
               * Gamma(3/2-s)/Gamma(s+1/2)
  E_q(s) = prod_{k=0}^{q-1} sin(pi(s+k)/q)^{(q-2k-1)/q}

Write K_q(s) for everything except phi_q.  Then, U4 being true,

      P_q(1-s) / P_q(s)   ==   |kappa_q(s)|   =   |phi_q(s)| * |K_q(s)| .    (*)

LHS: transfer operator only.  RHS: Eisenstein series + Teo kernel only.  No
shared machinery.  A clean disagreement in (*) refutes U4-as-identification.

TEST B2 (non-tautological).  Points with Re s > 1, where phi_q is computable
from its (convergent, main-term-corrected) Dirichlet series, and Re(1-s) > -1,
where the determinant still evaluates: sigma in {1.25, 1.40, 1.50}, t = t_inf.
(At sigma = 2 the mirror point Re s = -1 returns NaN from the Arb builder, so
sigma <= 1.5 is forced.)

TEST B1 (the guard's own dU points).  dU_j = s_inf + (1/4) e^{2 pi i j / 8},
j = 0,1,2.  Here phi_q is NOT directly computable (Re s and Re(1-s) both lie
where the Dirichlet series diverges), so (*) cannot be checked -- instead it is
INVERTED to read a U4-CONDITIONAL value of |phi_q| off the guard:

      |phi_q^proxy(s)| := [ P_q(1-s)/P_q(s) ] / |K_q(s)| ,
      |phi_q^proxy(1-s)| = 1/|phi_q^proxy(s)|   (scattering FE, phi(s)phi(1-s)=1)

dU_2 mirrors to Re s = 0.75 exactly -- the edge of the (U1-phi-a') crux strip
-- so this yields a U4-CONDITIONAL reading of the crux quantity
|phi_q(sigma+it)| * q^{2 sigma - 1}.

NON-RIGOROUS: float midpoints of the Arb determinant builder, no winding
certificate; phi_q from a truncated group enumeration; parent note
LAW_U1PHI_PROOF_ROUTE.md is PENDING ADVERSARIAL VERIFICATION.
"""
from __future__ import annotations
import cmath, json, math, sys, time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import zeta_cert_rosen_even as E                                    # noqa: E402
from flint import acb, arb, ctx                                     # noqa: E402
from mpmath import (mp, mpf, mpc, gamma, sqrt, pi, sin, tan,        # noqa: E402
                    barnesg, fabs, power)

from strip_phi_continuation import enumerate_c_spectrum, phi_cont   # noqa: E402

mp.dps = 30
TINF = mpf('7.0673625708673465')
S_INF = complex(0.25, float(TINF))
NB, CM = 1200.0, 120.0          # group enumeration budget (see strip probe)


# ------------------------------------------------------------------ kappa side
def E_q(s, q):
    v = mpc(1)
    for k in range(q):
        v *= power(sin(pi * (s + k) / q), mpf(q - 2*k - 1) / q)
    return v


def K_q(s, q):
    """kappa_q(s) / phi_q(s): every factor of the Teo kernel except phi."""
    ex = power(2, -(2*s - 1))
    el2 = sqrt(tan(pi * s / 2))
    elq = E_q(s, q)
    bar = power((power(2*pi, 2*s - 1) * barnesg(s)**2 * gamma(1 - s)
                 / (barnesg(1 - s)**2 * gamma(s))), (1 - mpf(2)/q) / 2)
    par = gamma(mpf(3)/2 - s) / gamma(s + mpf(1)/2)
    return ex * el2 * elq * bar * par


# ------------------------------------------------------------------ proxy side
def P_q(q, s, N):
    """|det(1-L^+) det(1-L^-)| at s, plus the two sector moduli."""
    sb = acb(arb(s.real), arb(s.imag))
    o = {}
    for sign in (+1, -1):
        v = E.cert_det_complex_mid(sb, N, sign, q, n_head=4)
        z = complex(float(v.real), float(v.imag))
        o[f"det{sign:+d}"] = [z.real, z.imag]
        o[f"abs{sign:+d}"] = abs(z)
    o["P"] = o["abs+1"] * o["abs-1"]
    return o


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 32
    ctx.prec = 400
    qs = [12, 16, 22, 30]

    out = {"description": "TASK B: U4 mirror test -- guard proxy vs directly "
                          "computed phi_q through the FE kernel",
           "relation": "P_q(1-s)/P_q(s) == |phi_q(s)| * |K_q(s)|  (U4 + Teo)",
           "params": {"N": N, "norm_bound": NB, "cmax": CM, "prec": ctx.prec},
           "caveat": "float midpoints, no winding cert; parent LAW_U1PHI_PROOF_"
                     "ROUTE.md PENDING ADVERSARIAL VERIFICATION",
           "assembly_check": [], "B2_rows": [], "B1_rows": []}

    # ---- assembly check: |K_q(1/2+it)| must be 1 (since |phi|=1 there)
    for q in qs:
        v = fabs(K_q(mpc(mpf('0.5'), TINF), q))
        out["assembly_check"].append({"q": q, "abs_K_at_half": float(v),
                                      "dev_from_1": float(fabs(v - 1))})
        print(f"assembly q={q}: |K_q(1/2+i t_inf)| = {float(v):.12f}", flush=True)

    dU = [S_INF + 0.25 * cmath.exp(2j * math.pi * j / 8) for j in range(3)]

    for q in qs:
        t0 = time.time()
        lam, cls, ne = enumerate_c_spectrum(q, NB, CM)
        print(f"\n--- q={q}  lam={lam:.6f}  n_elts={ne}", flush=True)

        # ---------- B2: sigma > 1, phi_q directly computable
        for sg in (1.25, 1.40, 1.50):
            s = complex(sg, float(TINF))
            ms = mpc(mpf(repr(sg)), TINF)
            try:
                ps = P_q(q, s, N)
                pm = P_q(q, complex(1 - s.real, -s.imag), N)
            except Exception as exc:                       # noqa: BLE001
                print(f"  B2 sigma={sg} DET FAIL {exc!r}"[:150], flush=True)
                continue
            if not (math.isfinite(ps["P"]) and math.isfinite(pm["P"])):
                print(f"  B2 sigma={sg} non-finite det", flush=True)
                continue
            lhs = pm["P"] / ps["P"]
            phi = phi_cont(cls, ms, q, CM)
            kk = K_q(ms, q)
            rhs = float(fabs(phi) * fabs(kk))
            row = {"q": q, "point": f"sigma={sg}", "s": [s.real, s.imag],
                   "P_at_s": ps["P"], "P_at_1ms": pm["P"], "LHS_ratio": lhs,
                   "abs_phi_direct": float(fabs(phi)), "abs_K": float(fabs(kk)),
                   "RHS_kappa": rhs, "ratio_LHS_over_RHS": lhs / rhs}
            out["B2_rows"].append(row)
            print(f"  B2 q={q} sigma={sg}: LHS={lhs:.6e}  RHS={rhs:.6e}  "
                  f"ratio={lhs/rhs:.6f}   (|phi|={float(fabs(phi)):.6e})",
                  flush=True)

        # ---------- B1: the guard's dU points, U4-conditional inversion
        for j, z in enumerate(dU):
            s = z
            ms = mpc(mpf(repr(s.real)), mpf(repr(s.imag)))
            try:
                ps = P_q(q, s, N)
                pm = P_q(q, complex(1 - s.real, -s.imag), N)
            except Exception as exc:                       # noqa: BLE001
                print(f"  B1 dU_{j} DET FAIL {exc!r}"[:150], flush=True)
                continue
            lhs = pm["P"] / ps["P"]
            kk = float(fabs(K_q(ms, q)))
            phi_proxy = lhs / kk
            sig_m = 1 - s.real
            row = {"q": q, "point": f"dU_{j}", "s": [s.real, s.imag],
                   "P_at_s": ps["P"], "P_at_1ms": pm["P"], "LHS_ratio": lhs,
                   "abs_K": kk, "abs_phi_proxy_at_s": phi_proxy,
                   "abs_phi_proxy_at_1ms": 1.0 / phi_proxy if phi_proxy else None,
                   "sigma_mirror": sig_m,
                   "crux_quantity_at_mirror":
                       (1.0 / phi_proxy) * q ** (2 * sig_m - 1) if phi_proxy else None}
            out["B1_rows"].append(row)
            print(f"  B1 q={q} dU_{j} s={s.real:.4f}{s.imag:+.4f}i: "
                  f"P(s)={ps['P']:.4e} P(1-s)={pm['P']:.4e} |K|={kk:.4e} "
                  f"|phi^proxy(s)|={phi_proxy:.6e}  "
                  f"|phi^proxy(1-s)|q^(2s'-1)={row['crux_quantity_at_mirror']}",
                  flush=True)

        print(f"  q={q} wall={time.time()-t0:.0f}s", flush=True)
        with open(__file__.replace('.py', '.json'), 'w') as f:
            json.dump(out, f, indent=1, default=str)

    # ---- q-slopes of the U4-conditional crux quantity
    sl = {}
    for j in range(3):
        rows = [r for r in out["B1_rows"] if r["point"] == f"dU_{j}"
                and r.get("crux_quantity_at_mirror")]
        if len(rows) < 2:
            continue
        xs = [math.log(r["q"]) for r in rows]
        ys = [math.log(r["abs_phi_proxy_at_1ms"]) for r in rows]
        n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
        num = sum((a-mx)*(b-my) for a, b in zip(xs, ys))
        den = sum((a-mx)**2 for a in xs)
        sig_m = rows[0]["sigma_mirror"]
        sl[f"dU_{j}"] = {"sigma_mirror": sig_m, "slope_abs_phi_proxy": num/den,
                         "required": -(2*sig_m - 1)}
    out["B1_slopes"] = sl
    print("\n=== U4-conditional q-slope of |phi_q| at the mirrored dU points ===")
    for k, v in sl.items():
        print(f"  {k}: Re(1-s)={v['sigma_mirror']:.4f}  measured slope="
              f"{v['slope_abs_phi_proxy']:+.4f}   required={v['required']:+.4f}")

    with open(__file__.replace('.py', '.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("\nwrote", __file__.replace('.py', '.json'))


if __name__ == "__main__":
    main()
