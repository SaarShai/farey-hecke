"""
exp_diophantine_lagrange_numeric.py
===================================
Numerically estimate the BOTTOM of the Lagrange spectrum for Rosen lambda_q-continued
fractions, q = 3,5,7 (and 4,6,8 for cross-check), VALIDATING q=3 against the classical
sqrt5 / Hurwitz constant before trusting anything.

ROSEN lambda-CF (Rosen 1954; nearest-integer-multiple form on I = [-lambda/2, lambda/2]):
    lambda = 2 cos(pi/q),  L = lambda/2.
    Map T(x) = |1/x| - lambda * round(|1/x|/lambda)          (so T(x) in [-L, L])
    digit  d_n = round(|1/x|/lambda) >= 1,   sign e_n = sign(x).
    Convergents via the standard recursion with partial quotients (e_n, d_n):
        p_n = e_n*lambda*d_n? -- we instead track the Mobius matrix product directly.

We measure, for the orbit of x_0=alpha under T, the APPROXIMATION COEFFICIENT.  The
Hecke/Rosen Lagrange number (Haas-Series / Kim-Sim normalization) of alpha is
    L_q(alpha) = limsup_n  |q_n|^{-2} / |alpha - p_n/q_n|         (= limsup of 1/theta_n)
where theta_n = q_n^2 |alpha - p_n/q_n| = |q_n| |q_n alpha - p_n|.
The BOTTOM of the Lagrange spectrum = inf_alpha L_q(alpha) = Hurwitz constant h'_q.

We compute theta_n from the convergent matrices, then L_q(alpha)=1/liminf_n theta_n
(since L = limsup 1/theta = 1/liminf theta).  The Hurwitz constant = inf over alpha,
which is achieved by the "worst approximable" alpha = the eventually-periodic CF with the
smallest digits; the spectral bottom = MIN over alpha of L_q(alpha)
                                      = 1 / MAX over alpha of liminf_n theta_n.

So: bottom_estimate = 1 / max_alpha( liminf_n theta_n(alpha) ).

q=3 ANCHOR: bottom must come out ~ sqrt5 = 2.2360679...
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(20260613)


def rosen_cf_theta(alpha, lam, n_terms, burn=0):
    """Run the Rosen lambda-CF on alpha; return the list of approximation coefficients
    theta_n = |q_n| * |q_n*alpha - p_n| using the Mobius-product convergents.

    Matrix form: each step x_{n+1} = e/x_n - lam*d  (where we write T(x)=|1/x|-lam*round,
    with e=sign(x), d=round(|1/x|/lam)).  Equivalent map on x: x -> e/x - lam*d is the
    inverse-branch generator of the Hecke group.  The convergent recurrence:
        [p_n  p_{n-1}]   [p_{n-1} p_{n-2}] [ -lam*d_n*e_n? ...]
    We instead accumulate M_n = A_1 A_2 ... A_n with A = [[lam*d, e],[1,0]] acting so that
    alpha = (p_n * t + p_{n-1}) / (q_n * t + q_{n-1}); convergent p_n/q_n -> alpha.
    """
    L = lam / 2.0
    x = alpha
    # convergent recurrence (Hecke/Rosen): a_n = lam*d_n (with sign e_n)
    p_nm1, p_nm2 = 1.0, 0.0
    q_nm1, q_nm2 = 0.0, 1.0
    thetas = []
    for n in range(n_terms):
        if abs(x) < 1e-14:
            break
        inv = 1.0 / x                       # signed
        a = abs(inv)
        d = round(a / lam)
        if d < 1:
            d = 1
        e = 1.0 if inv > 0 else -1.0
        # partial quotient term  b_n = e * lam * d
        b = e * lam * d
        # recurrence p_n = b*p_{n-1} + p_{n-2}; q_n = b*q_{n-1} + q_{n-2}
        p_n = b * p_nm1 + p_nm2
        q_n = b * q_nm1 + q_nm2
        # next x:  T(x) = |1/x| - lam*d  with sign carried so x_{n+1} in [-L,L]
        x = e * inv - b   # = e*(1/x) - e*lam*d = e/x - e*lam*d ; |.|<=L
        # (equivalently x_{n+1} = inv - b but inv already signed; use signed inv - b)
        x = inv - b
        # approximation coefficient
        if q_n != 0:
            theta = abs(q_n) * abs(q_n * alpha - p_n)
            if n >= burn:
                thetas.append(theta)
        p_nm2, p_nm1 = p_nm1, p_n
        q_nm2, q_nm1 = q_nm1, q_n
        # renormalize to avoid overflow
        if abs(q_nm1) > 1e150:
            s = abs(q_nm1)
            p_nm1 /= s; p_nm2 /= s; q_nm1 /= s; q_nm2 /= s
    return thetas


def lagrange_bottom_estimate(q, n_alpha=4000, n_terms=300, burn=20):
    """Estimate bottom of Lagrange spectrum = 1 / max_alpha liminf_n theta_n.
    Use a tail liminf (min over the last portion of the orbit) per alpha; take the
    MAX of that liminf over many random alpha (worst-approximable alpha)."""
    lam = 2.0 * math.cos(math.pi / q)
    L = lam / 2.0
    best_liminf = 0.0
    best_alpha = None
    liminfs = []
    for _ in range(n_alpha):
        alpha = rng.uniform(-L, L)
        if abs(alpha) < 1e-6:
            continue
        th = rosen_cf_theta(alpha, lam, n_terms, burn=burn)
        if len(th) < 30:
            continue
        tail = th[len(th)//2:]          # liminf ~ min over the (decorrelated) tail
        li = min(tail)
        liminfs.append(li)
        if li > best_liminf:
            best_liminf = li
            best_alpha = alpha
    liminfs = np.array(liminfs)
    bottom = 1.0 / best_liminf if best_liminf > 0 else float('inf')
    return dict(q=q, lam=lam, bottom=bottom, best_liminf=best_liminf,
                best_alpha=best_alpha,
                liminf_p99=float(np.percentile(liminfs, 99)) if len(liminfs) else None,
                liminf_p999=float(np.percentile(liminfs, 99.9)) if len(liminfs) else None,
                n=len(liminfs))


def periodic_lagrange(q, digit_pattern, n_repeat=200):
    """Exact-ish: Lagrange number of the alpha with a purely periodic Rosen CF
    given by (e,d) digit_pattern repeated. Returns limsup 1/theta = 1/liminf theta."""
    lam = 2.0 * math.cos(math.pi / q)
    # build alpha as the fixed point of the periodic CF by long backward iteration
    x = 0.0
    for _ in range(n_repeat):
        for (e, d) in reversed(digit_pattern):
            b = e * lam * d
            x = 1.0 / (b + x)
    alpha = x
    th = rosen_cf_theta(alpha, lam, n_terms=len(digit_pattern)*n_repeat, burn=50)
    if not th:
        return None
    tail = th[len(th)//2:]
    li = min(tail)
    return dict(alpha=alpha, bottom=1.0/li if li > 0 else float('inf'),
                liminf=li, theta_min=li)


if __name__ == "__main__":
    print("=" * 80)
    print("ROSEN lambda_q-CF Lagrange-spectrum BOTTOM (numeric)")
    print("bottom = 1 / max_alpha liminf_n theta_n ;  theta_n=|q_n||q_n alpha - p_n|")
    print("=" * 80)

    # Haas-Series reference values:
    def HS(q):
        lam = 2*math.cos(math.pi/q)
        return 2.0 if q % 2 == 0 else 2*math.sqrt(1 + (1-lam/2)**2)

    print(f"\n{'q':>2} {'lam':>8} {'HS h_q':>9} {'numeric bottom':>15} {'ratio':>8} {'n_alpha':>8}")
    for q in [3, 4, 5, 6, 7, 8]:
        r = lagrange_bottom_estimate(q, n_alpha=6000, n_terms=400, burn=30)
        ref = HS(q)
        ratio = r['bottom'] / ref if ref else float('nan')
        print(f"{q:>2} {r['lam']:8.5f} {ref:9.5f} {r['bottom']:15.6f} {ratio:8.4f} {r['n']:8d}")

    print("\n--- q=3 ANCHOR DETAIL: worst-approximable should be golden alpha, bottom~sqrt5 ---")
    r3 = lagrange_bottom_estimate(3, n_alpha=20000, n_terms=500, burn=40)
    print(f"   bottom = {r3['bottom']:.6f}   sqrt5 = {math.sqrt(5):.6f}   "
          f"best_alpha = {r3['best_alpha']:.6f}  (golden-ish: {(math.sqrt(5)-1)/2:.6f})")
    # classical golden mean periodic CF: all digits 1
    pg = periodic_lagrange(3, [(1, 1)], n_repeat=400)
    print(f"   periodic all-1 (q=3): alpha={pg['alpha']:.6f}, bottom={pg['bottom']:.6f}")
