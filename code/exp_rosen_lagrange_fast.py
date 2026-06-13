"""
exp_rosen_lagrange_fast.py -- fast float64 Rosen lambda_q-CF Lagrange-bottom estimator,
with EXPLICIT q=3 anchor validation against the classical Hurwitz value sqrt5.

Convention (Rosen nearest-multiple CF, q=3 == nearest-integer CF):
  I = [-L, L], L = lam/2,  lam = 2 cos(pi/q).
  x_{n+1} = -1/x_n - lam * round(-1/x_n / lam).
  Convergent recurrence (S = [[0,-1],[1,0]], T=[[1,lam],[0,1]], letter T^{d} S):
    p_n = lam*d_n*p_{n-1} - p_{n-2},   q_n = lam*d_n*q_{n-1} - q_{n-2}
  with d_n = round(-1/x_n / lam) (signed integer), p_{-1}=1,p_{-2}=0,q_{-1}=0,q_{-2}=1.
  theta_n = |q_n| * |q_n*alpha - p_n|.
  Lagrange number L_q(alpha) = limsup 1/theta_n = 1 / liminf_n theta_n.
  Spectrum bottom = inf_alpha L_q(alpha) = 1 / sup_alpha liminf_n theta_n.

We estimate sup_alpha liminf_n theta_n by sampling many alpha and, per alpha, taking
the liminf as the min over a long DECORRELATED orbit tail; then taking a high quantile
/ max over alpha.  (The worst-approximable alpha maximises the liminf.)
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(20260613)


def thetas(alpha, lam, n):
    x = alpha
    pm1, pm2 = 1.0, 0.0
    qm1, qm2 = 0.0, 1.0
    out = []
    for _ in range(n):
        if abs(x) < 1e-13:
            break
        r = -1.0 / x
        d = round(r / lam)
        if d == 0:
            break
        b = lam * d
        p = b * pm1 - pm2
        qq = b * qm1 - qm2
        x = r - b
        if qq != 0.0:
            out.append(abs(qq) * abs(qq * alpha - p))
        pm2, pm1 = pm1, p
        qm2, qm1 = qm1, qq
        m = max(abs(pm1), abs(qm1))
        if m > 1e150:
            pm1 /= m; pm2 /= m; qm1 /= m; qm2 /= m
    return out


def liminf_orbit(alpha, lam, n, tail_frac=0.5):
    th = thetas(alpha, lam, n)
    if len(th) < 20:
        return None
    tail = th[int(len(th) * tail_frac):]
    return min(tail)


def estimate(q, n_alpha=40000, n_terms=200):
    lam = 2.0 * math.cos(math.pi / q)
    L = lam / 2.0
    best = 0.0
    best_a = None
    lis = []
    for _ in range(n_alpha):
        alpha = rng.uniform(-L, L)
        if abs(alpha) < 1e-3:
            continue
        li = liminf_orbit(alpha, lam, n_terms)
        if li is None:
            continue
        lis.append(li)
        if li > best:
            best = li
            best_a = alpha
    lis = np.array(lis)
    return dict(q=q, lam=lam, sup_liminf=best, best_a=best_a,
                bottom_max=1.0 / best if best else float('inf'),
                bottom_p99=1.0 / np.percentile(lis, 99),
                bottom_p999=1.0 / np.percentile(lis, 99.9),
                bottom_p9999=1.0 / np.percentile(lis, 99.99), n=len(lis))


def HS(q):
    lam = 2 * math.cos(math.pi / q)
    return 2.0 if q % 2 == 0 else 2 * math.sqrt(1 + (1 - lam / 2) ** 2)


if __name__ == "__main__":
    print("Rosen lambda_q-CF Lagrange-spectrum BOTTOM (float64). bottom = 1/sup_a liminf theta")
    print(f"{'q':>2} {'lam':>8} {'HS h_q':>8} {'b_max':>8} {'b_p99':>8} {'b_p999':>8} {'b_p9999':>8} {'ratio_p9999':>11}")
    res = {}
    for q in [3, 4, 5, 6, 7, 8]:
        r = estimate(q, n_alpha=40000, n_terms=220)
        res[q] = r
        ratio = r['bottom_p9999'] / HS(q)
        print(f"{q:>2} {r['lam']:8.5f} {HS(q):8.5f} {r['bottom_max']:8.4f} "
              f"{r['bottom_p99']:8.4f} {r['bottom_p999']:8.4f} {r['bottom_p9999']:8.4f} {ratio:11.4f}")

    print(f"\nANCHOR: q=3 HS h_3 = sqrt5 = {math.sqrt(5):.6f}")
    print("Interpretation: the spectrum bottom is the SUP of liminf over alpha; the highest")
    print("quantiles (p999/p9999) approach it from below as sampling grows. b_max can overshoot")
    print("if a near-rational alpha gives an anomalously large tail-min, so trust p999/p9999.")

    # Explicit worst-approximable periodic points for q=3 (golden) and general q (all-1 digits):
    print("\n--- periodic all-digit-1 'noble' point per q (the natural worst-approximable) ---")
    for q in [3, 4, 5, 6, 7, 8]:
        lam = 2 * math.cos(math.pi / q)
        # fixed point of x -> 1/(lam + x)  (purely periodic CF, all d=1, positive)
        x = 0.3
        for _ in range(2000):
            x = 1.0 / (lam + x)
        alpha = x
        li = liminf_orbit(alpha, lam, 400)
        bot = 1.0 / li if li else float('inf')
        print(f"  q={q}: alpha*={alpha:.6f}  liminf theta={li:.6f}  L_q(alpha*)={bot:.6f}  "
              f"(HS h_q={HS(q):.6f})")
