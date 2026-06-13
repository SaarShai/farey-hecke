"""
exp_rosen_lagrange_v2.py  -- robust Rosen lambda_q-CF Lagrange-bottom estimator.

Rosen nearest-multiple CF on I=[-L,L], L=lambda/2, lambda=2cos(pi/q):
    given x_n in I,  r_n = -1/x_n  (the Hecke generator S:x->-1/x then translate),
    d_n = round(r_n / lambda) (>=1 in abs after we ensure |r_n|>=L which holds since |x_n|<=L),
    x_{n+1} = r_n - lambda*d_n = -1/x_n - lambda*d_n  in I.

Convergent matrices: alpha = M_n . x_{n+1}  with  M_n = T_1 S T_2 S ... where each
"letter" is  A_n = [[lambda*d_n, -1],[1, 0]]  (this is T^{d_n} S in PSL2, T=[[1,lambda],[0,1]], S=[[0,-1],[1,0]]).
Then  M_n = A_1 A_2 ... A_n = [[p_n, p_{n-1}],[q_n, q_{n-1}]],  and
    alpha = (p_n x_{n+1} + p_{n-1}) / (q_n x_{n+1} + q_{n-1}),
    convergent  P_n/Q_n = p_n/q_n -> alpha.
Approximation coefficient: theta_n = |q_n (q_n alpha - p_n)| = |q_n|^2 |alpha - p_n/q_n|.

Lagrange number L_q(alpha) = limsup_n 1/theta_n = 1/liminf_n theta_n.
Bottom of Lagrange spectrum = inf_alpha L_q(alpha) = 1/ sup_alpha liminf_n theta_n.

ANCHOR q=3: Rosen q=3 CF = nearest-integer CF (NICF). The NICF Lagrange/Hurwitz bottom
is the SAME spectrum bottom as the regular CF = sqrt5 (Hurwitz). We must reproduce ~2.236.
"""
from __future__ import annotations
import math
import numpy as np
from mpmath import mp, mpf, fabs

mp.dps = 60
rng = np.random.default_rng(7)


def rosen_thetas(alpha, lam, n_terms):
    """High-precision Rosen CF; returns list of theta_n."""
    L = lam / 2
    x = mpf(alpha)
    lam = mpf(lam)
    A_prod = [[mpf(1), mpf(0)], [mpf(0), mpf(1)]]   # M_0 = I -> p0=1,p-1=0,q0=0,q-1=1
    p_n, p_nm1 = mpf(1), mpf(0)
    q_n, q_nm1 = mpf(0), mpf(1)
    a0 = mpf(alpha)
    thetas = []
    for n in range(n_terms):
        if fabs(x) < mpf(10) ** (-50):
            break
        r = -1 / x                       # -1/x_n
        d = int(mp.nint(r / lam))
        if d == 0:
            d = 1 if r > 0 else -1
        # letter A = [[lam*d, -1],[1,0]]
        new_p = lam * d * p_n - p_nm1
        new_q = lam * d * q_n - q_nm1
        # Wait: M_{n} = M_{n-1} A_n => columns shift. Use standard:
        # [p_n p_{n-1}; q_n q_{n-1}] = [p_{n-1} p_{n-2}; q_{n-1} q_{n-2}] [[lam d,1],[ -1? ...]]
        # Cleanest: recurrence p_n = lam*d_n*p_{n-1} - p_{n-2}, q_n = lam*d_n*q_{n-1} - q_{n-2}
        # (the -1 off-diagonal of S gives the minus sign).
        p_new = lam * d * p_n + (-1) * p_nm1
        q_new = lam * d * q_n + (-1) * q_nm1
        p_nm1, p_n = p_n, p_new
        q_nm1, q_n = q_n, q_new
        x = r - lam * d                  # x_{n+1}
        if q_n != 0:
            theta = fabs(q_n * (q_n * a0 - p_n))
            thetas.append(float(theta))
        # renormalize
        m = max(fabs(p_n), fabs(q_n))
        if m > mpf(10) ** 200:
            p_n /= m; p_nm1 /= m; q_n /= m; q_nm1 /= m
    return thetas


def estimate_bottom(q, n_alpha, n_terms, burn_frac=0.3):
    lam = 2 * math.cos(math.pi / q)
    L = lam / 2
    sup_liminf = 0.0
    best_alpha = None
    lis = []
    for _ in range(n_alpha):
        alpha = rng.uniform(-L, L)
        if abs(alpha) < 1e-4:
            continue
        th = rosen_thetas(alpha, lam, n_terms)
        if len(th) < 40:
            continue
        tail = th[int(len(th) * burn_frac):]
        li = min(tail)               # liminf over orbit ~ min of decorrelated tail
        lis.append(li)
        if li > sup_liminf:
            sup_liminf = li
            best_alpha = alpha
    lis = np.array(lis)
    bottom = 1.0 / sup_liminf if sup_liminf > 0 else float('inf')
    return dict(q=q, lam=lam, bottom=bottom, sup_liminf=sup_liminf, best_alpha=best_alpha,
                p99=float(np.percentile(lis, 99)), p9999=float(np.percentile(lis, 99.99)),
                n=len(lis))


def HS(q):
    lam = 2 * math.cos(math.pi / q)
    return 2.0 if q % 2 == 0 else 2 * math.sqrt(1 + (1 - lam / 2) ** 2)


if __name__ == "__main__":
    print("Rosen lambda_q-CF Lagrange bottom (mpmath, robust convergent recurrence)")
    print(f"{'q':>2} {'lam':>8} {'HS h_q':>9} {'1/p99':>9} {'1/p9999':>9} {'bottom':>10} {'best_a':>9}")
    for q in [3, 4, 5, 6, 7, 8]:
        r = estimate_bottom(q, n_alpha=8000, n_terms=300)
        print(f"{q:>2} {r['lam']:8.5f} {HS(q):9.5f} {1/r['p99']:9.5f} {1/r['p9999']:9.5f} "
              f"{r['bottom']:10.6f} {r['best_alpha']:+9.5f}")
    print("\nNOTE: 'bottom' = global worst-case (sensitive to outliers/non-converged tails).")
    print("'1/p99' and '1/p9999' are robust upper estimates of the spectrum bottom.")
    print(f"q=3 anchor target sqrt5={math.sqrt(5):.5f}")
