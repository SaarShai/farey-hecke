#!/usr/bin/env python3
"""
rate_measure_validate.py -- pre-registered gate for rate_measure.py's two new
ingredients before any q>6 number is trusted:

  GATE 1: phi_q(q,s,N) (branch-corrected determinant route) vs agp_phi.phi_exact
          at q = 3, 4, 6, across the FULL target (sigma,t) grid of
          rate_measure.py. Must agree to <= 1e-6 relative (N=24).
  GATE 2: |phi_infty(1/2+it)| is NOT 1 in general (sanity: phi_infty is one
          entry of a 2x2 unitary matrix, not unitary alone) -- reports the
          actual values instead of assuming the naive expectation.
  GATE 3: phi_infty has a pole at s = rho_1/2 = 0.25 + 7.0673625708673469i
          (first nontrivial zeta zero over 2) -- reports |phi_infty| growth
          approaching that point.
"""
import cmath
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rate_measure as R                                              # noqa: E402
import agp_phi as A                                                   # noqa: E402
from mpmath import mpc, mpf                                           # noqa: E402

SIGMAS = [1.1, 1.25]
TS = [0.5, 1.5, 3.5, 7.0665, 14.0]


def gate1():
    print("=== GATE 1: phi_q branch-corrected vs exact closed form, q=3,4,6 ===")
    rows = []
    N = 24
    worst = 0.0
    for q in (3, 4, 6):
        for sig in SIGMAS:
            for t in TS:
                s = mpc(sig, t)
                exact = complex(A.phi_exact(q, s))
                t0 = time.time()
                gen = R.phi_q(q, s, N)
                rel = abs(exact - gen) / abs(exact)
                worst = max(worst, rel)
                dt = time.time() - t0
                rows.append((q, sig, t, rel, dt))
                print(f"  q={q} sig={sig} t={t}: reldiff={rel:.3e}  ({dt:.1f}s)")
    print(f"GATE1 worst reldiff = {worst:.3e}  {'PASS' if worst <= 1e-6 else 'FAIL'}")
    return worst <= 1e-6, rows


def gate2():
    print("\n=== GATE 2: |phi_infty(1/2+it)| -- is it 1? (naive task expectation) ===")
    for t in [1.0, 3.0, 5.0, 7.0665, 10.0, 20.0]:
        s = mpc(0.5, t)
        v = R.phi_infty(s)
        print(f"  t={t}: phi_infty(1/2+it)={complex(v)}  |phi_infty|={abs(v):.6f}")


def gate3():
    print("\n=== GATE 3: pole of phi_infty at s=rho_1/2 ===")
    s_inf = mpc(mpf('0.25'), mpf('7.0673625708673468952'))
    for r in (1e-2, 1e-3, 1e-4, 1e-5):
        s = s_inf + mpc(r, 0)
        v = R.phi_infty(s)
        print(f"  r={r}: |phi_infty(s_inf+r)|={abs(v):.6e}")


if __name__ == "__main__":
    R.set_prec()
    ok, rows = gate1()
    gate2()
    gate3()
    if not ok:
        print("\nGATE 1 FAILED -- do not trust q>6 measurements without further repair.")
        sys.exit(1)
    print("\nGATE 1 PASSED.")
