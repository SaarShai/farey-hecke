#!/usr/bin/env python3
"""
test_detk_repair.py -- gate for the ADDITIVE det(1 - K_s) repair.

MMS (arXiv:0912.2236, Theorem `main-theorem`) states

      Z_S(s) = det(1 - L_s) / det(1 - K_s),   det(1-K_s) = prod_{n>=0}(1-b_q^{s+n}),

and the repo builders `zeta_cert_rosen.py` / `zeta_cert_rosen_even.py` return the
NUMERATOR only (diagnosis: research_notes/rh_goals_2026-08-14/lane_g/
LAW_Q3_BRANCH_DIAGNOSIS.md; blast radius: LAW_DETK_IMPACT_AUDIT.md).  The repair
adds `det_K` / `selberg_Z` and changes NOTHING that existing certificates bound.

FOUR TESTS
  A  det_K's Euler-factor structure at q=3: 1/b_3 = phi^4 = 6.854101966..., and
     det_K(3,s) == prod_{k>=0}(1 - N(P)^{-s-k}) with N(P) = phi^4 -- the Selberg
     Euler factor of the shortest closed geodesic on the modular surface.
     Also: b_q vs the banked law_probes/q3diag_detK.json for q = 3,4,5,6.
  B  |selberg_Z(3,s)| == the INDEPENDENT Mayer/Gauss-map determinant
     (law_probes/q3cont_mayer_indep.py, no shared code) to <= 1e-8 rel, at
     s = sigma + i*7.067362570867346, sigma = 1.25, 1.40, 1.50.
  C  no zero introduced or removed on Re s > 0: |det_K| is bounded away from 0
     and from infinity there (its zeros are exactly -N_0 + i(2pi/log(1/b))Z,
     and one such zero is exhibited to confirm the pole/zero bookkeeping).
  D  BYTE-REPRODUCIBILITY of the pre-existing path: cert_det_complex_mid at
     q=3, N=32, prec 400 still gives the P values banked in
     law_probes/mirror_q3.json.

Interpreter: /Users/za/miniforge3/envs/pari-arb/bin/python3  (flint + mpmath).
Run:  python3 test_detk_repair.py
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
CODE = Path(__file__).resolve().parent
PROBES = REPO / "research_notes/rh_goals_2026-08-14/lane_g/law_probes"
sys.path.insert(0, str(CODE))
sys.path.insert(0, str(PROBES))

from flint import acb, arb, ctx                          # noqa: E402
from mpmath import mp, mpf, mpc, sqrt, fabs              # noqa: E402

import zeta_cert_rosen as O                              # noqa: E402

TINF = '7.067362570867346'          # the mirror tests' height, gamma_1 / 2
SIGMAS = ('1.25', '1.40', '1.50')

mp.dps = 60
FAILS = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{'  ' + detail if detail else ''}",
          flush=True)
    if not ok:
        FAILS.append(name)


def cmid(z):
    return complex(float(z.real.mid()), float(z.imag.mid()))


# ---------------------------------------------------------------- A
def test_A_euler_factor():
    print("\nA  det_K Euler-factor structure at q = 3 (and b_q vs banked JSON)")
    ctx.prec = 400
    b3, k3 = O.b_q_ball(3)
    inv = 1.0 / cmid(b3).real
    phi = (1 + mp.sqrt(5)) / 2
    phi4 = float(phi ** 4)
    check("kappa_3 == 1", k3 == 1, f"kappa={k3}")
    check("1/b_3 == phi^4", abs(inv - phi4) / phi4 < 1e-13,
          f"1/b_3={inv:.12f}  phi^4={phi4:.12f}  rel={abs(inv-phi4)/phi4:.2e}")

    # det_K(3, s) == prod_{k>=0} (1 - N^{-s-k}), N = phi^4 -- the Euler factor.
    NP = mpf(phi) ** 4
    for sig in ('1.25', '2.00', '0.75'):
        s = mpc(mpf(sig), mpf(TINF))
        euler = mpc(1)
        for k in range(0, 300):
            t = NP ** (-(s + k))
            euler *= (1 - t)
            if abs(t) < mpf(10) ** (-mp.dps - 5) and k > 2:
                break
        got = cmid(O.det_K(3, complex(float(s.real), float(s.imag))))
        want = complex(float(euler.real), float(euler.imag))
        rel = abs(got - want) / abs(want)
        check(f"det_K(3, {sig}+it) == Euler factor N(P)=phi^4", rel < 1e-12,
              f"rel={rel:.2e}")

    banked = json.loads((PROBES / "q3diag_detK.json").read_text())["b_q"]
    for q in (3, 4, 5, 6):
        want = banked[str(q)]["b_q"]
        got = cmid(O.b_q_ball(q)[0]).real
        rel = abs(got - want) / want
        check(f"b_{q} matches q3diag_detK.json", rel < 1e-13,
              f"got={got:.15f} banked={want:.15f} rel={rel:.2e}")


# ---------------------------------------------------------------- B
def test_B_vs_independent_mayer():
    print("\nB  |selberg_Z(3,s)| vs the INDEPENDENT Mayer determinant (<= 1e-8)")
    ctx.prec = 400
    import q3cont_mayer_indep as MAY      # no shared code with the Arb engine
    N_ARB, N_MAY = 32, 28
    for sig in SIGMAS:
        s = complex(float(mpf(sig)), float(mpf(TINF)))
        z = cmid(O.selberg_Z(3, s, N_ARB))
        P_may, _dm, _dp = MAY.P_mayer(mpc(mpf(sig), mpf(TINF)), N_MAY)
        want = float(P_may)
        rel = abs(abs(z) - want) / want
        check(f"sigma={sig}: |Z_S| == P_mayer", rel <= 1e-8,
              f"|Z_S|={abs(z):.12f}  P_mayer={want:.12f}  rel={rel:.2e}")


# ---------------------------------------------------------------- C
def test_C_no_zero_moved():
    print("\nC  no zero introduced/removed on Re s > 0 (det_K zero-free there)")
    ctx.prec = 400
    pts = [(0.05, 0.0), (0.05, 7.067362570867346), (0.45, 5.764),
           (0.5, 6.4737), (1.0, 3.0), (1.25, 7.067362570867346),
           (2.0, 0.5), (4.0, 12.0)]
    for q in (3, 5):
        worst = None
        for re, im in pts:
            v = abs(cmid(O.det_K(q, complex(re, im))))
            if worst is None or v < worst[0]:
                worst = (v, re, im)
            ok = 1e-3 < v < 1e3
            if not ok:
                check(f"q={q} det_K finite & nonzero at s={re}+{im}i", False,
                      f"|det_K|={v:.3e}")
        check(f"q={q}: |det_K| bounded away from 0 on Re s > 0 sample",
              worst[0] > 1e-3,
              f"min |det_K|={worst[0]:.6f} at s={worst[1]}+{worst[2]}i")
        # the ratio Z_S/raw = 1/det_K is finite and nonzero => identical zero set
        # the nearest genuine det_K zero sits on Re s = 0 (Q3D.7):
        b = cmid(O.b_q_ball(q)[0]).real
        spacing = 2 * 3.141592653589793 / mp.log(1 / b)
        zero = complex(0.0, float(spacing))
        vz = abs(cmid(O.det_K(q, zero)))
        # the zero abscissa is fed in at DOUBLE precision, so the residual floor
        # is the input's ~1e-16 offset, not the ball arithmetic (O(1) nearby).
        check(f"q={q}: det_K vanishes at s = 0 + i*2pi/log(1/b_q) (Re s = 0)",
              vz < 1e-13, f"|det_K|={vz:.3e}, spacing={float(spacing):.9f}")


# ---------------------------------------------------------------- D
def test_D_existing_path_unchanged():
    print("\nD  pre-existing call path unchanged vs law_probes/mirror_q3.json")
    ctx.prec = 400
    N = 32
    banked = json.loads((PROBES / "mirror_q3.json").read_text())
    assert banked["params"] == {"q": 3, "N": 32, "prec": 400,
                                "t": 7.067362570867346}, banked["params"]
    for row in banked["rows"]:
        sig = row["sigma"]
        for label, s in (("s", complex(sig, float(TINF))),
                         ("1-s", complex(1 - sig, -float(TINF)))):
            sb = acb(arb(s.real), arb(s.imag))
            P = 1.0
            for sign in (+1, -1):
                P *= abs(O.cert_det_complex_mid(sb, N, sign, 3, n_head=4))
            want = row["P_at_s"] if label == "s" else row["P_at_1ms"]
            rel = abs(P - want) / want
            check(f"P_3(sigma={sig}, {label}) reproduces banked value",
                  rel < 1e-14, f"got={P!r} banked={want!r} rel={rel:.2e}")


def main():
    print("det(1-K_s) repair gate -- MMS arXiv:0912.2236 Theorem `main-theorem`")
    test_A_euler_factor()
    test_B_vs_independent_mayer()
    test_C_no_zero_moved()
    test_D_existing_path_unchanged()
    print(f"\n{'ALL TESTS PASS' if not FAILS else 'FAILURES: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
