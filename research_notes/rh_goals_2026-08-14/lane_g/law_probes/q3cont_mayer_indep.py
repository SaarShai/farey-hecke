#!/usr/bin/env python3
"""
q3cont_mayer_indep.py -- LANE G: is the O(1) mirror residual the DETERMINANT
BUILDER'S ANALYTIC CONTINUATION to Re s <= 0?

LAW_TEO_KAPPA_CORRECTED.md Sec 3.4 leaves a TODO-VERIFY: after the Gamma_2 = 1/G
fix, the mirror identity

      P_q(1-s)/P_q(s)  ==  |phi_q(s)| |K_q(s)|                             (*)

still carries an O(1) residual (0.42-2.05), smooth in sigma, ~1 on Re s = 1/2,
growing once the MIRROR point Re(1-s) < 0.  The named hypothesis: it is the
determinant proxy's continuation to Re s <= 0, not the kernel.

THIS PROBE tests that hypothesis at q = 3 with a SECOND, INDEPENDENT evaluator.

At q = 3, G_3 = PSL(2,Z) and U4 is Mayer's THEOREM:

      Z_{PSL(2,Z)}(s) = det(1 - L_s) det(1 + L_s)

with L_s the Gauss-Kuzmin-Wirsing transfer operator

      (L_s f)(z) = sum_{n>=1} (z+n)^{-2s} f(1/(z+n))

nuclear of order 0 on the disk D = {|z-1| < 3/2}.  So P_3(s) has a classical
target, and both sides of the comparison are the SAME analytic object -- no
normalisation constant to guess.

WHAT IS INDEPENDENT, PRECISELY
------------------------------
SHARED with the repo builder: nothing but the mathematical claim.  This file
does NOT import zeta_cert_rosen.py, zeta_cert_rosen_q5.py, flint/Arb, or any
lane_g probe.  Different library (mpmath), different Markov partition (the
single full-branch Gauss map on [0,1], not the Rosen/MMS kappa-component
partition of [-lambda/2, 0]), different basis (Taylor at z = 1, not the
acb_series expansion about the MMS disc centres), different continuation
mechanism (see below), different determinant routine (mpmath LU vs acb_mat.det).

THE MATRIX, DERIVED HERE (so the continuation is explicit and checkable)
-----------------------------------------------------------------------
Write f(z) = sum_m a_m (z-1)^m on D.  Then

  (L_s f)(z) = sum_{n>=1} (z+n)^{-2s} sum_m a_m (1/(z+n) - 1)^m
             = sum_m a_m sum_{n>=1} (z+n)^{-2s-m} (1 - (z+n))^m
             = sum_m a_m sum_{j=0}^{m} C(m,j)(-1)^j sum_{n>=1} (z+n)^{-(2s+m-j)}
             = sum_m a_m sum_{j=0}^{m} C(m,j)(-1)^j zeta(2s+m-j, z+1).

d^k/dz^k zeta(a, z+1) = (-1)^k (a)_k zeta(a+k, z+1); at z = 1, zeta(a+k, 2) =
zeta(a+k) - 1.  Hence, with r = m - j,

  M_{k,m}(s) = sum_{r=0}^{m} C(m,r) (-1)^{m-r+k} C(2s+r+k-1, k) [zeta(2s+r+k) - 1].

Every entry is a FINITE sum of Riemann zeta values at 2s + (integer) and a
Pochhammer symbol.  Both are meromorphic in s on all of C with NO reference to
the half-plane where the n-sum converged.  The continuation to Re s <= 0 is
therefore carried entirely by the classical zeta function -- it is the standard
Mayer continuation, and it shares no code and no device with the Rosen/MMS
engine's "exact-Hurwitz branch-tail closure" (zeta_cert_rosen_q5.hurwitz_series_in_a
+ _tail_block_allcols with n_head heads split off).

VALIDATIONS RUN BEFORE ANY COMPARISON (all classical, all independent of the
repo):
  V1  det(1 - L_1) -> 0.  Z_{PSL(2,Z)}(1) = 0 (the constant eigenfunction; the
      Gauss-Kuzmin operator L_1 has eigenvalue 1).
  V2  Z(1/4 + i gamma_1/2) = 0, gamma_1 = 14.134725141734693 the first Riemann
      zero: the modular surface's Selberg zeta has "resonance" zeros at s = rho/2
      coming from the scattering determinant phi_3 = xi(2s-1)/xi(2s).
      NOTE t_inf = 7.0673625708673465 = gamma_1/2 exactly, so this validation
      sits at the very height the mirror test uses.
  V3  det(1 + L_s) -> 0 at s = 1/2 + i r with r = 9.533695261352... the first
      ODD Maass eigenvalue parameter of PSL(2,Z).

NON-RIGOROUS: mpmath floats at dps = 60, truncation at finite N, no interval
arithmetic and no winding certificate.  Same epistemic status as the probes it
is compared against.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 q3cont_mayer_indep.py
"""
from __future__ import annotations
import json, time
from pathlib import Path

from mpmath import mp, mpf, mpc, zeta, binomial, matrix, det, nstr, fabs

mp.dps = 60

TINF = mpf('7.0673625708673465')          # = gamma_1 / 2
SIGMAS = ('1.25', '1.40', '1.50')
NS = (12, 16, 20, 24, 28)


def mayer_matrix(s, N):
    """M_{k,m}(s), k,m = 0..N-1, of the Gauss-map transfer operator in the
    Taylor basis (z-1)^m.  zeta and Pochhammer values are cached over the
    integer offset, so the build is O(N^3) cheap arithmetic + O(N) zeta calls."""
    two_s = 2 * s
    zc = [zeta(two_s + u) - 1 for u in range(2 * N + 1)]      # u = r + k
    # poch[k][u] = C(2s + u - 1, k) with u = r + k  ->  C(2s+r+k-1, k)
    poch = {}
    for k in range(N):
        for u in range(k, 2 * N + 1):
            poch[(k, u)] = binomial(two_s + u - 1, k)
    binc = [[binomial(m, r) for r in range(m + 1)] for m in range(N)]
    M = matrix(N, N)
    for m in range(N):
        for k in range(N):
            tot = mpc(0)
            for r in range(m + 1):
                u = r + k
                s_ = (-1) ** ((m - r + k) % 2)
                tot += s_ * binc[m][r] * poch[(k, u)] * zc[u]
            M[k, m] = tot
    return M


def dets(s, N):
    """(det(1 - L_s), det(1 + L_s)) at truncation N."""
    M = mayer_matrix(s, N)
    A = matrix(N, N)
    B = matrix(N, N)
    for i in range(N):
        for j in range(N):
            A[i, j] = (1 if i == j else 0) - M[i, j]
            B[i, j] = (1 if i == j else 0) + M[i, j]
    return det(A), det(B)


def P_mayer(s, N):
    dm, dp = dets(s, N)
    return abs(dm) * abs(dp), dm, dp


def main():
    out = {"description": "independent Mayer/Gauss-map determinant for q=3, "
                          "and its continuation to Re s <= 0",
           "shares_no_code_with": ["zeta_cert_rosen.py", "zeta_cert_rosen_q5.py",
                                   "mirror_u4.py", "mirror_q3.py", "flint/Arb"],
           "params": {"dps": mp.dps, "N_sweep": list(NS), "t": float(TINF)},
           "validations": {}, "points": []}

    # ---------------- V1: Z(1) = 0
    print("V1  det(1-L_s) at s=1  (Z_{PSL(2,Z)}(1)=0)", flush=True)
    v1 = []
    for N in NS:
        dm, dp = dets(mpf(1), N)
        v1.append({"N": N, "det_minus": float(dm.real if hasattr(dm, 'real') else dm),
                   "det_plus": float(dp.real if hasattr(dp, 'real') else dp)})
        print(f"   N={N:2d}  det(1-L)={nstr(dm,8):>16}  det(1+L)={nstr(dp,10)}", flush=True)
    out["validations"]["V1_Z_at_1"] = v1

    # ---------------- V2: Z(rho/2) = 0 at the mirror test's own height
    print("\nV2  |Z| at s = 1/4 + i gamma_1/2  (scattering zero)", flush=True)
    v2 = []
    for N in NS:
        z = mpc(mpf('0.25'), TINF)
        P, dm, dp = P_mayer(z, N)
        v2.append({"N": N, "abs_det_minus": float(fabs(dm)),
                   "abs_det_plus": float(fabs(dp)), "P": float(P)})
        print(f"   N={N:2d}  |det(1-L)|={float(fabs(dm)):.6e}  "
              f"|det(1+L)|={float(fabs(dp)):.6e}  P={float(P):.6e}", flush=True)
    out["validations"]["V2_Z_at_quarter_plus_i_gamma1_over_2"] = v2

    # ---------------- V3: first odd Maass form
    print("\nV3  |det(1+L_s)| at s = 1/2 + i*9.533695261352 (odd Maass)", flush=True)
    v3 = []
    for N in NS:
        z = mpc(mpf('0.5'), mpf('9.533695261352'))
        dm, dp = dets(z, N)
        v3.append({"N": N, "abs_det_minus": float(fabs(dm)),
                   "abs_det_plus": float(fabs(dp))})
        print(f"   N={N:2d}  |det(1-L)|={float(fabs(dm)):.6e}  "
              f"|det(1+L)|={float(fabs(dp)):.6e}", flush=True)
    out["validations"]["V3_first_odd_Maass"] = v3

    # ---------------- the six comparison points
    print("\nTARGETS  P_3^Mayer at s and at the mirror 1-s", flush=True)
    for sg in SIGMAS:
        for lab, z in (("s", mpc(mpf(sg), TINF)),
                       ("1-s", mpc(1 - mpf(sg), -TINF))):
            row = {"sigma": float(sg), "which": lab,
                   "Re_s": float(z.real), "Im_s": float(z.imag), "by_N": {}}
            t0 = time.time()
            for N in NS:
                P, dm, dp = P_mayer(z, N)
                row["by_N"][str(N)] = float(P)
            vs = [row["by_N"][str(N)] for N in NS]
            row["P"] = vs[-1]
            row["rel_drift_last_two"] = abs(vs[-1] - vs[-2]) / abs(vs[-2])
            row["wall_s"] = time.time() - t0
            out["points"].append(row)
            print(f"   sigma={sg} {lab:>3}  Re s={float(z.real):+.4f}  "
                  f"P={vs[-1]:.10e}  drift({NS[-2]}->{NS[-1]})="
                  f"{row['rel_drift_last_two']:.2e}", flush=True)

    p = str(Path(__file__).with_suffix('.json'))
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("\nwrote", p)


if __name__ == "__main__":
    main()
