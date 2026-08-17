"""evenxval_mp.py -- INDEPENDENT mpmath reimplementation of det(1 - L_{s,sign})
for the EVEN-q Hecke triangle group G_12 (lambda_12 = 2 cos(pi/12)), plain
mpmath at 50 digits.

INDEPENDENCE STATEMENT
----------------------
This file shares NO code with the Arb builder `zeta_cert_rosen_even.py` /
`zeta_cert_rosen_q5.py`.  It was written directly from the MMS paper structure
(Mayer--Muehlenbruch--Stroemberg, arXiv:0912.2236):

  * Even-q reduced operators, their eq. labeled `reduced1` (q = 2 h_q + 2,
    kappa = h_q), on B_{kappa} = direct-sum_{i=1}^{h_q} B(D_i):

        (L_{s,+-} g)_1(z) = Linf_{2,s} g_{h_q}(z) +- Linf_{-1,s} g_{h_q}(z)
        (L_{s,+-} g)_i(z) = L_{1,s} g_{i-1}(z) + Linf_{2,s} g_{h_q}(z)
                            +- Linf_{-1,s} g_{h_q}(z),          2 <= i <= h_q

  * Branch operators (their `aux` family, squared-weight principal sheet):
        L_{n,s}  g(z) = ((z + n lam)^2)^{-s} g(-1/(z + n lam))   (n > 0)
        L_{-n,s} g(z) = ((z - n lam)^2)^{-s} g(+1/(z - n lam))   (n > 0)
        Linf_{+-n,s} = sum_{l>=n} L_{+-l,s}.

  * Even-q Markov partition of [-lam/2, 0] (MMS Sec 2.6): phi_i = f_q^i(-L),
    i.e. the lambda-CF values [[0; 1^{h_q - i}]]_(-) (minus-CF), phi_0 = -lam/2,
    phi_{h_q} = 0; discs D_i centered at (phi_{i-1}+phi_i)/2 with radius
    (phi_i - phi_{i-1}) * safety/2, safety = 5/2.

  * Finite matrix in the NORMALIZED monomial bases ((z-c_i)/rho_i)^m out,
    ((w-c_j)/rho_j)^k in, truncated at N: M[(i-1)N+m, (j-1)N+k] = m-th Taylor
    coefficient (in u, z = c_i + rho_i u) of column k of block (i,j).

  * The Linf tails are closed EXACTLY with Hurwitz zeta: factoring
    z +- l lam = +-lam (l +- z/lam) (positive for l >= 1 on the discs) gives,
    for both branches, the common factor (lam^2)^{-s} (-1/lam)^m and
        sum_{l>=n0} (l +- z/lam)^{-(2s+m)} = zeta(2s+m, a0 + slope u),
    pos: a0 = n0 + c_i/lam, slope = +rho_i/lam;
    neg: a0 = n0 - c_i/lam, slope = -rho_i/lam;
    and ((arg - c_j)/rho_j)^k = rho_j^{-k} sum_m C(k,m) (-c_j)^{k-m} arg^m.

Deliberate differences from the Arb builder (same exact math, different
conditioning): n_head = 6 here vs 4 there (the Hurwitz tail closure is exact,
so the split point cannot change the value), power-series arithmetic is a
hand-rolled truncated-Cauchy implementation on mpc, and the determinant is
mpmath LU rather than acb_mat.  What is returned is det(1 - L_{s,sign}), the
MMS NUMERATOR (Z_S = det(1-L)/det(1-K)); no K_s factor anywhere.

Usage: evenxval_mp.py  ->  evenxval_mp.json  (24 evaluations: 12 s-points x
2 sign sectors at N = 24).
"""
from __future__ import annotations
import json
import math
import os
import sys
import time

import mpmath as mp

mp.mp.dps = 50

Q = 12
N = 24
N_HEAD = 6          # head/tail split; exact tail => value-independent
SAFETY = mp.mpf(5) / 2

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "evenxval_mp.json")

SIGMAS = [0.1, 0.25, 0.4]
TS = [2.0, 7.0, 12.0, 17.0]
SIGNS = [+1, -1]


# ---------------------------------------------------------------------------
# Truncated power series on mpc (lists of coefficients, index = degree).
# ---------------------------------------------------------------------------
def ps_pad(a, n):
    return list(a) + [mp.mpc(0)] * (n - len(a))


def ps_mul(a, b, n):
    c = [mp.mpc(0)] * n
    for i, ai in enumerate(a):
        if i >= n:
            break
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if i + j >= n:
                break
            c[i + j] += ai * bj
    return c


def ps_inv(a, n):
    """1/a for a[0] != 0."""
    a = ps_pad(a, n)
    b = [mp.mpc(0)] * n
    b[0] = 1 / a[0]
    for k in range(1, n):
        acc = mp.mpc(0)
        for j in range(1, k + 1):
            acc += a[j] * b[k - j]
        b[k] = -acc / a[0]
    return b


def ps_log(a, n):
    """Log of series a with principal mp.log of the constant term."""
    a = ps_pad(a, n)
    L = [mp.mpc(0)] * n
    L[0] = mp.log(a[0])
    for k in range(1, n):
        # a' = a * L'  =>  k*a[k] = sum_{j=0}^{k-1} (j+1) L[j+1] a[k-1-j]
        acc = k * a[k]
        for j in range(0, k - 1):
            acc -= (j + 1) * L[j + 1] * a[k - 1 - j]
        L[k] = acc / (k * a[0])
    return L


def ps_exp(b, n):
    E = [mp.mpc(0)] * n
    E[0] = mp.exp(b[0])
    for k in range(1, n):
        acc = mp.mpc(0)
        for j in range(1, k + 1):
            acc += j * b[j] * E[k - j]
        E[k] = acc / k
    return E


def ps_pow_neg_s(a, s, n):
    """(a^2)^{-s}: square the series, principal log, scale by -s, exp."""
    a2 = ps_mul(a, a, n)
    lg = ps_log(a2, n)
    return ps_exp([(-s) * x for x in lg], n)


# ---------------------------------------------------------------------------
# Geometry: lambda, Markov partition, discs (q = 12 => h_q = kappa = 5).
# ---------------------------------------------------------------------------
def geometry(q):
    lam = 2 * mp.cos(mp.pi / q)
    hq = (q - 2) // 2                     # even q only; kappa = hq
    phis = []
    for i in range(0, hq + 1):
        digits = [1] * (hq - i)
        x = mp.mpf(0)
        for a in reversed(digits):        # minus lambda-CF [[0; digits]]
            x = -1 / (a * lam + x)
        phis.append(x)
    phis[0] = -lam / 2
    phis.sort()
    c = [(phis[i - 1] + phis[i]) / 2 for i in range(1, len(phis))]
    rho = [(phis[i] - phis[i - 1]) * SAFETY / 2 for i in range(1, len(phis))]
    return lam, hq, c, rho


# ---------------------------------------------------------------------------
# Operator blocks: columns 0..N-1, each an N-term series in u (z = c_i+rho_i u).
# ---------------------------------------------------------------------------
def single_branch_cols(s, ci, ri, cj, rj, lam, n, neg):
    """One branch L_{+-n,s}: weight * ((arg - c_j)/rho_j)^k, k = 0..N-1."""
    z1 = ri                                # z(u) = ci + ri u, linear
    d = [ci + (-n * lam if neg else n * lam), z1]
    invd = ps_inv(d, N)
    arg = invd if neg else [-x for x in invd]
    w = ps_pow_neg_s(d, s, N)
    base = [(arg[0] - cj) / rj] + [x / rj for x in arg[1:]]
    cols = []
    powk = [mp.mpc(1)] + [mp.mpc(0)] * (N - 1)
    for _k in range(N):
        cols.append(ps_mul(w, powk, N))
        powk = ps_mul(powk, base, N)
    return cols


def tail_cols(s, ci, ri, cj, rj, lam, n0, neg):
    """Exact Linf tail sum_{l>=n0}, closed by Hurwitz zeta (see header)."""
    if not neg:
        a0 = ci / lam + n0
        slope = ri / lam
    else:
        a0 = -ci / lam + n0
        slope = -ri / lam
    lam2s = mp.exp(-s * mp.log(lam * lam))
    # Z[m] series: (lam^2)^{-s} (-1/lam)^m zeta(2s+m, a0 + slope u)
    Z = []
    mfac = mp.mpc(1)
    for m in range(N):
        t = 2 * s + m
        ser = [mp.mpc(0)] * N
        pref = mp.mpc(1)                   # prod_{l<j} -(t+l)
        fact = mp.mpf(1)
        spow = mp.mpc(1)
        for j in range(N):
            if j == 0:
                ser[0] = mp.zeta(t, a0)
            else:
                pref *= -(t + (j - 1))
                fact *= j
                spow *= slope
                ser[j] = mp.zeta(t + j, a0) * pref * spow / fact
        Z.append([(lam2s * mfac) * x for x in ser])
        mfac *= (-1 / lam)
    cols = []
    for k in range(N):
        invrj = rj ** (-k)
        acc = [mp.mpc(0)] * N
        for m in range(k + 1):
            coef = mp.binomial(k, m) * ((-cj) ** (k - m)) * invrj
            for j in range(N):
                acc[j] += coef * Z[m][j]
        cols.append(acc)
    return cols


def linf_cols(s, ci, ri, cj, rj, lam, n0, neg):
    """Linf_{+-n0,s} = head single branches + exact tail from n0+N_HEAD."""
    cols = tail_cols(s, ci, ri, cj, rj, lam, n0 + N_HEAD, neg)
    for l in range(n0, n0 + N_HEAD):
        hc = single_branch_cols(s, ci, ri, cj, rj, lam, l, neg)
        for k in range(N):
            for j in range(N):
                cols[k][j] += hc[k][j]
    return cols


# ---------------------------------------------------------------------------
# Assemble the kappa*N x kappa*N matrix of L_{s,sign} (MMS reduced1) and
# return det(1 - L).
# ---------------------------------------------------------------------------
def build_matrix(s, sign, lam, h, c, rho):
    dim = h * N
    M = mp.zeros(dim, dim)

    def add_block(i, j, cols, prefac=mp.mpc(1)):
        for k in range(N):
            col = cols[k]
            base_r = (i - 1) * N
            cc = (j - 1) * N + k
            pf = prefac
            for m in range(N):
                v = pf * col[m]
                if v != 0:
                    M[base_r + m, cc] += v

    # (L g)_1 = Linf_2 g_h +- Linf_{-1} g_h
    add_block(1, h, linf_cols(s, c[0], rho[0], c[h - 1], rho[h - 1], lam,
                              2, False))
    add_block(1, h, linf_cols(s, c[0], rho[0], c[h - 1], rho[h - 1], lam,
                              1, True), prefac=mp.mpc(sign))
    # (L g)_i = L_1 g_{i-1} + Linf_2 g_h +- Linf_{-1} g_h, 2 <= i <= h
    for i in range(2, h + 1):
        add_block(i, i - 1,
                  single_branch_cols(s, c[i - 1], rho[i - 1],
                                     c[i - 2], rho[i - 2], lam, 1, False))
        add_block(i, h, linf_cols(s, c[i - 1], rho[i - 1],
                                  c[h - 1], rho[h - 1], lam, 2, False))
        add_block(i, h, linf_cols(s, c[i - 1], rho[i - 1],
                                  c[h - 1], rho[h - 1], lam, 1, True),
                  prefac=mp.mpc(sign))
    return M


def det_one(sigma, t, sign, lam, h, c, rho):
    s = mp.mpc(sigma, t)
    M = build_matrix(s, sign, lam, h, c, rho)
    dim = h * N
    Iden = mp.eye(dim)
    return mp.det(Iden - M)


def main():
    t0 = time.time()
    lam, h, c, rho = geometry(Q)
    rows = []
    for sign in SIGNS:
        for sigma in SIGMAS:
            for t in TS:
                ta = time.time()
                d = det_one(sigma, t, sign, lam, h, c, rho)
                rows.append({
                    "sigma": sigma, "t": t, "sign": sign,
                    "det_re": mp.nstr(mp.re(d), 40),
                    "det_im": mp.nstr(mp.im(d), 40),
                    "wall_s": round(time.time() - ta, 3),
                })
                print(f"sign={sign:+d} s={sigma}+i{t}: "
                      f"{mp.nstr(d, 12)}  ({rows[-1]['wall_s']} s)",
                      flush=True)
    rec = {
        "probe": "evenxval_mp",
        "what": "INDEPENDENT mpmath det(1 - L_{s,sign}) for even q=12, "
                "MMS reduced1 block structure, exact Hurwitz tails",
        "interpreter": sys.executable,
        "dps": mp.mp.dps, "q": Q, "N": N, "n_head": N_HEAD,
        "safety": float(SAFETY),
        "returns": "det(1-L) MMS numerator only; NO det(1-K) factor",
        "points": rows,
        "wall_s_total": round(time.time() - t0, 2),
    }
    with open(OUT, "w") as f:
        json.dump(rec, f, indent=2)
    print(f"wrote {OUT}  total {rec['wall_s_total']} s")


if __name__ == "__main__":
    main()
