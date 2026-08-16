#!/usr/bin/env python3
"""
q3diag_rosen_mp.py -- LANE G / PC.9 diagnosis, step 1.

An mpmath re-implementation of the repo's q=3 "scalar eq.(33)" Rosen transfer
operator, so that its START INDICES can be varied cheaply (the Arb builder costs
~240 s per point; this costs ~1 s).

The repo (zeta_cert_rosen.build_reduced_matrix_ball, q == 3 branch) builds

    (L_{s,e} f)(z) = sum_{n >= 3} ((z+n)^2)^{-s} f(-1/(z+n))
                   + e * sum_{n >= 2} ((z-n)^2)^{-s} f( 1/(z-n))          (REPO)

acting on the single Markov component: the disc about c = -lambda/4 = -1/4 of
radius rho = (5/2)*(1/2)/2 = 5/16, e = `sign` in {+1,-1}, lambda_3 = 1.
P_3(s) = |det(1 - L_{s,+1})| * |det(1 - L_{s,-1})|.

Closed form used here (derived in this file, continuation carried by Hurwitz
zeta exactly as in the independent Mayer probe):

  f(w) = sum_m a_m (w - c)^m,   and with  A(m,j) = C(m,j) (-c)^{m-j} (-1)^j,

  positive branch, start n0:
     sum_{n>=n0} ((z+n)^2)^{-s} (-1/(z+n) - c)^m
        = sum_j A(m,j) zeta(2s+j, z+n0),
     [(z-c)^k coefficient]  ->  (-1)^k C(2s+j+k-1, k) zeta(2s+j+k, n0+c)

  negative branch, start m0:
     sum_{n>=m0} ((z-n)^2)^{-s} (1/(z-n) - c)^m
        = sum_j A(m,j) zeta(2s+j, m0-z),
     [(z-c)^k coefficient]  ->  (+1)^k C(2s+j+k-1, k) zeta(2s+j+k, m0-c)

(the basis is (z-c)^m rather than the repo's ((z-c)/rho)^m; a diagonal rescale
of the matrix, which leaves det(1-L) unchanged).

GATE: `python3 q3diag_rosen_mp.py --gate` reproduces the banked Arb values in
q3cont_repo_builder.json for (n0, m0) = (3, 2).

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 q3diag_rosen_mp.py
"""
from __future__ import annotations
import sys
from mpmath import mp, mpf, mpc, zeta, binomial, matrix, det

mp.dps = 60

TINF = mpf('7.0673625708673465')
C = -mpf(1) / 4                      # disc centre, = -lambda_3 / 4


def rosen_matrix(s, N, n0=3, m0=2, c=C):
    """Matrix of the Rosen q=3 operator pieces (A, B) in the basis (z-c)^m."""
    two_s = 2 * s
    # zeta(2s+u, n0+c) and zeta(2s+u, m0-c), u = j+k = 0 .. 2N-2
    U = 2 * N
    zA = [zeta(two_s + u, n0 + c) for u in range(U + 1)]
    zB = [zeta(two_s + u, m0 - c) for u in range(U + 1)]
    poch = {}
    for k in range(N):
        for u in range(k, U + 1):
            poch[(k, u)] = binomial(two_s + u - 1, k)
    A = matrix(N, N)
    B = matrix(N, N)
    for m in range(N):
        coef = [binomial(m, j) * ((-c) ** (m - j)) * ((-1) ** (j % 2))
                for j in range(m + 1)]
        for k in range(N):
            sk = (-1) ** (k % 2)
            ta = mpc(0)
            tb = mpc(0)
            for j in range(m + 1):
                u = j + k
                p = coef[j] * poch[(k, u)]
                ta += p * zA[u]
                tb += p * zB[u]
            A[k, m] = sk * ta
            B[k, m] = tb
    return A, B


def rosen_dets(s, N, n0=3, m0=2, c=C):
    """(det(1-L_{s,+1}), det(1-L_{s,-1}))."""
    A, B = rosen_matrix(s, N, n0, m0, c)
    out = []
    for e in (1, -1):
        D = matrix(N, N)
        for i in range(N):
            for j in range(N):
                D[i, j] = (1 if i == j else 0) - (A[i, j] + e * B[i, j])
        out.append(det(D))
    return out[0], out[1]


def P_rosen(s, N, n0=3, m0=2, c=C):
    dp, dm = rosen_dets(s, N, n0, m0, c)
    return abs(dp) * abs(dm), dp, dm


# --------------------------------------------------------------------------
if __name__ == "__main__":
    # GATE: reproduce q3cont_repo_builder.json (Arb, N=32/64, prec 400)
    banked = {
        (1.25, +1): complex(0.8426924709469149, 0.03748577116193969),
        (1.25, -1): complex(0.9957446736832332, 0.11621014719658354),
        (-0.25, +1): complex(-1.2593536976249755, 0.6817655253753618),
        (-0.25, -1): complex(-0.33917226441910153, -1.6762659759938432),
        (1.40, +1): complex(0.8811611464957751, 0.030447348415945947),
        (1.40, -1): complex(1.0010443267924065, 0.08741007344491837),
    }
    print("GATE  mpmath Rosen (n0=3, m0=2) vs banked Arb values")
    for (sig, e), ref in sorted(banked.items()):
        t = TINF if sig > 0.5 else -TINF
        s = mpc(mpf(repr(sig)), t)
        for N in (20, 28, 36):
            dp, dm = rosen_dets(s, N)
            v = complex(dp if e == 1 else dm)
            print(f"  sigma={sig:+.2f} sign={e:+d} N={N:2d}  {v.real:+.12f}{v.imag:+.12f}j"
                  f"   |rel err| = {abs(v-ref)/abs(ref):.3e}")
        sys.stdout.flush()
