#!/usr/bin/env python3
"""
mirror_q3.py -- LANE G, TASK B, the NAMED NEXT ACT of LAW_STRIP_AND_MIRROR.md Sec 5.

The q >= 4 mirror test (mirror_u4.py, mirror_arith.py) finds
      P_q(1-s) / P_q(s)   ==   |phi_q(s)| * |K_q(s)|                     (*)
failing by 12-19 orders of magnitude, N-converged, and surviving at the
ARITHMETIC levels q = 4, 6 where phi_q is the exact closed form.  Exactly one
of two things is false: (a) hypothesis U4, or (b) the Teo kappa_q assembly.

This run separates them by re-running the IDENTICAL test at q = 3 = PSL(2,Z),
using the ODD-q determinant module zeta_cert_rosen.py (the even-q module used
by mirror_u4.py raises NotImplementedError at q=3).  At q = 3:
  * phi_3(s) = sqrt(pi) Gamma(s-1/2) zeta(2s-1) / (Gamma(s) zeta(2s))  -- exact,
  * Z_{PSL(2,Z)} and its functional equation are classical,
  * signature (0;1;2,3), so Teo's formula applies verbatim.

PRE-REGISTERED INTERPRETATION RULE (LAW_STRIP_AND_MIRROR.md Sec 5, verbatim):
  FAILURE at q=3  ==> the fault is the Teo assembly (b).
  SUCCESS at q=3 with failure at q>=4 ==> the fault is U4 (a).

Controls, the same three as the parent where applicable:
  C1  |K_3(1/2 + i t_inf)| == 1        (unitarity / assembly identity check)
  C2  determinant N-convergence at every test point, N = 24,32,48,64;
      pre-registered: rel drift <= 1e-6 => informative, >= 1e-2 => out of domain
  C3  phi_3 exact closed form -- the evaluator (c) cannot enter.

NON-RIGOROUS: float midpoints of the Arb determinant builder, no winding
certificate.  Same status as the parent note.
"""
from __future__ import annotations
import json, math, sys, time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import zeta_cert_rosen as O                                        # noqa: E402  ODD-q module
from flint import acb, arb, ctx                                    # noqa: E402
from mpmath import mp, mpf, mpc, gamma, sqrt, pi, fabs, zeta       # noqa: E402

from mirror_u4 import K_q                                          # noqa: E402

mp.dps = 30
TINF = mpf('7.0673625708673465')
SIGMAS = (1.25, 1.40, 1.50)


def phi3(s):
    """phi_3 = g(s), the exact PSL(2,Z) scattering determinant."""
    return sqrt(pi) * gamma(s - mpf(1)/2) * zeta(2*s - 1) / (gamma(s) * zeta(2*s))


def P3(s, N):
    """|det(1-L^+) det(1-L^-)| at s, ODD-q builder, q = 3."""
    sb = acb(arb(s.real), arb(s.imag))
    o = {}
    for sign in (+1, -1):
        v = O.cert_det_complex_mid(sb, N, sign, 3, n_head=4)
        z = complex(float(v.real), float(v.imag))
        o[f"det{sign:+d}"] = [z.real, z.imag]
        o[f"abs{sign:+d}"] = abs(z)
    o["P"] = o["abs+1"] * o["abs-1"]
    return o


def main():
    ctx.prec = 400
    N = 32
    out = {"description": "q=3 mirror discriminator: (a) U4 vs (b) Teo kappa assembly",
           "relation": "P_3(1-s)/P_3(s) == |phi_3(s)| * |K_3(s)|   (U4 + Teo)",
           "module": "zeta_cert_rosen.py (ODD q, eq.33/34)",
           "params": {"q": 3, "N": N, "prec": ctx.prec, "t": float(TINF)},
           "pre_registered_rule": {
               "fail_at_q3": "fault is (b) the Teo kappa assembly",
               "hold_at_q3": "fault is (a) U4"},
           "controls": {}, "rows": []}

    # ---- C1: assembly / unitarity check on Re s = 1/2
    k_half = fabs(K_q(mpc(mpf('0.5'), TINF), 3))
    out["controls"]["abs_K3_at_half"] = float(k_half)
    out["controls"]["abs_K3_at_half_dev"] = float(fabs(k_half - 1))
    print(f"C1 assembly q=3: |K_3(1/2+i t_inf)| = {float(k_half):.12f}", flush=True)
    # phi_3 on the critical line must have modulus 1 too
    ph_half = fabs(phi3(mpc(mpf('0.5'), TINF)))
    out["controls"]["abs_phi3_at_half"] = float(ph_half)
    print(f"C1 unitarity: |phi_3(1/2+i t_inf)| = {float(ph_half):.12f}", flush=True)

    # ---- the mirror test proper
    for sg in SIGMAS:
        s = complex(sg, float(TINF))
        ms = mpc(mpf(repr(sg)), TINF)
        t0 = time.time()
        try:
            ps = P3(s, N)
            pm = P3(complex(1 - s.real, -s.imag), N)
        except Exception as exc:                              # noqa: BLE001
            print(f"sigma={sg} DET FAIL {exc!r}"[:200], flush=True)
            out["rows"].append({"sigma": sg, "error": repr(exc)[:200]})
            continue
        if not (math.isfinite(ps["P"]) and math.isfinite(pm["P"])):
            print(f"sigma={sg} non-finite det", flush=True)
            out["rows"].append({"sigma": sg, "error": "non-finite"})
            continue
        lhs = pm["P"] / ps["P"]
        phi = phi3(ms)
        kk = K_q(ms, 3)
        rhs = float(fabs(phi) * fabs(kk))
        row = {"sigma": sg, "s": [s.real, s.imag],
               "P_at_s": ps["P"], "P_at_1ms": pm["P"], "LHS_ratio": lhs,
               "abs_phi3_exact": float(fabs(phi)), "abs_K3": float(fabs(kk)),
               "RHS_kappa": rhs, "ratio_LHS_over_RHS": lhs / rhs,
               "wall_s": time.time() - t0}
        out["rows"].append(row)
        print(f"q=3 sigma={sg}: P(s)={ps['P']:.6e} P(1-s)={pm['P']:.6e} "
              f"LHS={lhs:.6e} |phi3|exact={float(fabs(phi)):.6e} "
              f"|K3|={float(fabs(kk)):.6e} RHS={rhs:.6e}  "
              f"ratio={lhs/rhs:.6e}", flush=True)

    # ---- C2: N-convergence at every test point
    print("\nC2 N-convergence, N = 24,32,48,64", flush=True)
    nconv = []
    pts = []
    for sg in SIGMAS:
        pts.append((f"s sigma={sg}", complex(sg, float(TINF))))
        pts.append((f"mirror sigma={1-sg:.2f}", complex(1 - sg, -float(TINF))))
    for label, z in pts:
        vals = {}
        for NN in (24, 32, 48, 64):
            try:
                vals[NN] = P3(z, NN)["P"]
            except Exception as exc:                          # noqa: BLE001
                vals[NN] = None
                print(f"  {label} N={NN} FAIL {exc!r}"[:150], flush=True)
        ok = [v for v in vals.values() if v is not None and math.isfinite(v)]
        drift = (abs(vals[64] - vals[48]) / abs(vals[48])
                 if vals.get(48) and vals.get(64) else None)
        nconv.append({"point": label, "Re_s": z.real, "P_by_N": vals,
                      "rel_drift_48_to_64": drift})
        print(f"  {label:22s} Re s={z.real:+.4f}  P={ok[-1] if ok else None!r:>14}  "
              f"drift(48->64)={drift}", flush=True)
    out["controls"]["N_convergence"] = nconv

    # ---- verdict
    ratios = [r["ratio_LHS_over_RHS"] for r in out["rows"] if "ratio_LHS_over_RHS" in r]
    if ratios:
        worst = max(abs(math.log10(abs(r))) for r in ratios)
        holds = worst < 1.0          # within one order of magnitude
        out["verdict"] = {
            "max_abs_log10_ratio": worst,
            "identity_holds_at_q3": bool(holds),
            "call": "(a) U4 is the fault" if holds else "(b) Teo kappa assembly is the fault"}
        print(f"\nVERDICT: max |log10(LHS/RHS)| = {worst:.3f} -> "
              f"{out['verdict']['call']}", flush=True)

    with open(__file__.replace('.py', '.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", __file__.replace('.py', '.json'))


if __name__ == "__main__":
    main()
