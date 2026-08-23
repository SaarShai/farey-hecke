#!/usr/bin/env python3
"""mms_q5_indep.py — independent from-paper mpmath implementation of the
MMS q=5 reduced transfer operator L_{s,eps} (arXiv:0912.2236, three-row
reduced display p.20-21 [repo-labelled "eq.(34)"; LaTeX label `reduced3`],
with the p.21 negative-index definitions and the squared-weight
principal-sheet convention).

REGENERATED artifact for S2_SECOND_WINDING_BOX_SOL.md §1.3(b) (referee C3):
the original scratchpad script was session-local and lost. This is a fresh
implementation with the same declared design: mpmath only (no Arb, no code
shared with the certified engine `zeta_cert_rosen_q5.py`), Cauchy-trapezoid
Taylor coefficients (NOT Arb series AD), dps = 30, n_head = 6 (engine: 4).

Operator (q=5, h_q=1, kappa=3), components g_1,g_2,g_3 on discs D_i:
  (L g)_1 = L_2 g_2 + Linf_3 g_3 + eps*( L_{-1} g_2 + Linf_{-2} g_3 )
  (L g)_2 =           Linf_2 g_3 + eps*( L_{-1} g_2 + Linf_{-2} g_3 )
  (L g)_3 = L_1 g_1 + Linf_2 g_3 + eps*( L_{-1} g_2 + Linf_{-2} g_3 )
pos branch (n>=1): arg = -1/(z + n*lam), weight = ((z+n*lam)^2)^(-s)
neg branch (n>=1): arg = +1/(z - n*lam), weight = ((z-n*lam)^2)^(-s)
Linf_{+-n0} = sum_{l>=n0}: finite head l = n0..n0+n_head-1 evaluated
directly, remainder closed EXACTLY by Hurwitz zeta after binomial expansion
of the normalized input monomial (analytic continuation supplies the
conditionally convergent sum its true value):
  sum_{l>=L} ((z+-l*lam)^2)^(-s) * arg^m
    = (lam^2)^(-s) * (-1/lam)^m * zeta(2s+m, L +- z/lam).

Usage: mms_q5_indep.py [--N 16] [--dps 30] [--selftest]
"""
import argparse
from mpmath import mp, mpc, mpf, zeta, exp, pi, sqrt, binomial, det, matrix, eye


def lam_val():
    return (1 + sqrt(5)) / 2  # lambda_5 = 2 cos(pi/5), golden ratio


def cf_value(digits, lam):
    x = mpc(0)
    for a in reversed(digits):
        x = -1 / (a * lam + x)
    return x


def geometry(lam, safety=mpf(5) / 4):
    """Markov partition of [-lam/2, 0] for q=5 (h_q=1, kappa=3):
    phi_0 = -lam/2, phi_1 = [[0;1]], phi_2 = [[0;2 1]], phi_3 = [[0;]] = 0.
    Disc centers = cell midpoints, radii = safety * half-gap * 2 = gap*5/4."""
    hq, kappa = 1, 3
    phi = {0: mpc(-lam / 2)}
    for i in range(1, hq + 1):
        phi[2 * i] = cf_value([1] * (hq - i) + [2] + [1] * hq, lam)
    for i in range(0, (kappa - 1) // 2 + 1):
        d = [1] * (hq - i)
        phi[2 * i + 1] = cf_value(d, lam) if d else mpc(0)
    pts = sorted((phi[k] for k in range(kappa + 1)), key=lambda z: float(z.real))
    c = [(pts[i - 1] + pts[i]) / 2 for i in range(1, len(pts))]
    rho = [(pts[i] - pts[i - 1]).real * safety for i in range(1, len(pts))]
    return c, rho


def block_point(s, z, c_j, rho_j, lam, kind, n, neg, k, n_head):
    """Value at z of (block applied to input monomial e_k^{(j)})."""
    if kind == "single":
        d = z + n * lam if not neg else z - n * lam
        arg = -1 / d if not neg else 1 / d
        return (d * d) ** (-s) * ((arg - c_j) / rho_j) ** k
    # tail Linf from n0=n: finite head + exact Hurwitz closure
    val = mpc(0)
    for l in range(n, n + n_head):
        val += block_point(s, z, c_j, rho_j, lam, "single", l, neg, k, n_head)
    L0 = n + n_head
    a = L0 + z / lam if not neg else L0 - z / lam
    pref = (lam * lam) ** (-s)
    acc = mpc(0)
    fac = mpc(1)  # (-1/lam)^m
    for m in range(k + 1):
        acc += binomial(k, m) * (-c_j) ** (k - m) * fac * zeta(2 * s + m, a)
        fac *= -1 / lam
    return val + pref * acc * rho_j ** (-k)


# eq.(34) block plan: list of (i, j, kind, n, neg, eps_weighted)
PLAN = [
    (1, 2, "single", 2, False, False), (1, 3, "tail", 3, False, False),
    (1, 2, "single", 1, True, True), (1, 3, "tail", 2, True, True),
    (2, 3, "tail", 2, False, False),
    (2, 2, "single", 1, True, True), (2, 3, "tail", 2, True, True),
    (3, 1, "single", 1, False, False), (3, 3, "tail", 2, False, False),
    (3, 2, "single", 1, True, True), (3, 3, "tail", 2, True, True),
]


def build_matrix(s, N, eps, n_head=6, P_mult=4, r_contour=mpf(1) / 2):
    """kappa*N x kappa*N matrix of L_{s,eps} in the normalized monomial
    bases; output Taylor coefficients by Cauchy-trapezoid on |u| = r < 1
    (r < 1 suppresses trapezoid aliasing by r^P; coeff_m = mean/r^m)."""
    lam = lam_val()
    c, rho = geometry(lam)
    kappa = 3
    P = P_mult * N
    r = mpf(r_contour)
    thetas = [2 * pi * p / P for p in range(P)]
    M = matrix(kappa * N, kappa * N)
    for (i, j, kind, n, neg, epsw) in PLAN:
        zs = [c[i - 1] + rho[i - 1] * r * exp(1j * th) for th in thetas]
        w = mpc(eps) if epsw else mpc(1)
        for k in range(N):
            fv = [block_point(s, z, c[j - 1], rho[j - 1], lam, kind, n, neg,
                              k, n_head) for z in zs]
            for m in range(N):
                cm = sum(fv[p] * exp(-1j * m * thetas[p])
                         for p in range(P)) / (P * r ** m)
                M[(i - 1) * N + m, (j - 1) * N + k] += w * cm
    return M


def det_IminusL(s, N, eps, n_head=6, P_mult=4, r_contour=mpf(1) / 2):
    M = build_matrix(s, N, eps, n_head=n_head, P_mult=P_mult,
                     r_contour=r_contour)
    return det(eye(3 * N) - M)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=16)
    ap.add_argument("--dps", type=int, default=30)
    ap.add_argument("--eps", type=int, default=1)
    args = ap.parse_args()
    mp.dps = args.dps
    pins = [
        ("flagship", mpc("0.45389518", "5.76353724")),
        ("sonnet", mpc("0.43318010", "5.67574682")),
        ("fallback", mpc("0.41054374", "7.81976825")),
        ("generic", mpc("0.30", "6.00")),
    ]
    print(f"# mms_q5_indep independent builder  N={args.N} dps={args.dps} "
          f"eps={args.eps:+d} n_head=6")
    for label, s in pins:
        d = det_IminusL(s, args.N, args.eps)
        print(f"{label:9s} ({float(s.real):.8f},{float(s.imag):.8f}): "
              f"|det| = {float(abs(d)):.3g}")


if __name__ == "__main__":
    main()
