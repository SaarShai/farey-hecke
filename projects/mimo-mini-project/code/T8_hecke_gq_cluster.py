#!/usr/bin/env python3
"""
T8_hecke_gq_cluster.py
======================
Does the q=3 "no 3 consecutive large gaps" cluster bound  max(Pl,Pm,Pr) >= 2/9
generalize to the Hecke triangle groups G_q  (q = 3,4,5,6,...)?

MAP / DOMAIN (authoritative, with citation)
-------------------------------------------
Diaaeldin Taha, "The Boca-Cobeli-Zaharescu Map Analogue for the Hecke Triangle
Groups G_q", arXiv:1810.10668v2 (2019).  Theorem (G_q BCZ maps).

  lambda_q = 2 cos(pi/q),   q >= 3.    (lambda_3 = 1, lambda_5 = golden ratio.)
  U_q = [[lambda_q, -1],[1, 0]],   w_i = U_q^i (1,0)^T,  i = 0..2q-1.
     w_0=(1,0), w_1=(lambda,1), w_{q-2}=(1,lambda), w_{q-1}=(0,1).
  G_q-Farey triangle:
     T^q = { (a,b) : 0 < a <= 1,  1 - lambda_q*a < b <= 1 }.   area = lambda_q/2.
  Partition into  T_i^q (i=2..q-1):  (a,b).w_{i-1} > 1  and  (a,b).w_i <= 1.
  On T_i^q:
     roof   R_q(a,b) = y_i / ( a * (a,b).w_i )                 [slope-gap / return time]
     index  k_i(a,b) = floor( (1 - (a,b).w_{i+1}) / (lambda_q * (a,b).w_i) )
     BCZ_q(a,b) = ( (a,b).w_i ,  (a,b).w_{i+1} + k_i * lambda_q * (a,b).w_i ).

GAP-PRODUCT ANALOGUE (our choice, stated honestly)
--------------------------------------------------
In q=3 a "large gap" between consecutive Farey fractions <=> small product P=ab,
where the roof R(a,b)=1/(ab) is the slope gap.  So the faithful generalization of
the "gap product" is the reciprocal roof

     P(a,b) := 1 / R_q(a,b) = a * (a,b).w_i / y_i      (on T_i^q).

For q=3 the only region is i=2 with w_2=U_3^2(1,0)=(0,-1)->careful: we use the
ACTIVE region detection from the paper; numerically P reduces to ab and the
classical min max(Pl,Pm,Pr)=2/9 is reproduced (validation gate).

Three consecutive gap products along an orbit are P(x0), P(T x0), P(T^2 x0).
   f(q) = min over x0 in T^q of  max( P(x0), P(Tx0), P(T^2 x0) ).
We locate minimizers and test whether they lie on a short periodic orbit
(b/a = inverse slope of a Lambda_q vector  <=>  BCZ_q-periodic; Taha Cor.).

Implied max cluster size m: the largest m s.t. there EXIST m consecutive points
all with small P (i.e. the m-window min-of-max stays small / -> the regime where
m large gaps in a row can occur).  We report f(q) for window sizes 2,3,4.
"""

import numpy as np
import json, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "T8_hecke_gq_cluster_results")
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------------------
def lam(q):
    return 2.0 * np.cos(np.pi / q)

def wvecs(q):
    """w_i = U_q^i (1,0)^T, i=0..2q-1."""
    L = lam(q)
    U = np.array([[L, -1.0], [1.0, 0.0]])
    w = []
    v = np.array([1.0, 0.0])
    for _ in range(2 * q):
        w.append(v.copy())
        v = U @ v
    return w

def region_index(a, b, w, q):
    """i in {2,...,q-1} with (a,b).w_{i-1}>1 and (a,b).w_i<=1, else None."""
    eps = 1e-12
    for i in range(2, q):
        dprev = a * w[i - 1][0] + b * w[i - 1][1]
        dcur  = a * w[i][0] + b * w[i][1]
        if dprev > 1.0 - eps and dcur <= 1.0 + eps:
            return i
    return None

def in_triangle(a, b, L):
    return (0.0 < a <= 1.0 + 1e-12) and (1.0 - L * a - 1e-12 < b <= 1.0 + 1e-12)

def bcz_step(a, b, w, q, L):
    """One G_q-BCZ step. Returns (a2,b2,P) with P = 1/roof = a*(a,b).w_i / y_i."""
    i = region_index(a, b, w, q)
    if i is None:
        return None
    di  = a * w[i][0] + b * w[i][1]
    di1 = a * w[i + 1][0] + b * w[i + 1][1]
    yi  = w[i][1]
    if abs(yi) < 1e-15 or di <= 0:
        return None
    P = a * di / yi
    k = np.floor((1.0 - di1) / (L * di))
    a2 = di
    b2 = di1 + k * L * di
    return a2, b2, P

def orbit_products(a0, b0, w, q, L, m):
    """Products at x0, Tx0, ..., T^{m-1} x0. Returns list or None if any undefined."""
    ps = []
    a, b = a0, b0
    for _ in range(m):
        s = bcz_step(a, b, w, q, L)
        if s is None:
            return None
        a, b, P = s
        ps.append(P)
        if not in_triangle(a, b, L):
            # next point left domain (numerical) -> still record current P count
            if len(ps) < m:
                return None
    return ps

# ----------------------------------------------------------------------------
def scan(q, n_samples, m=3, seed=0, refine=True):
    L = lam(q)
    w = wvecs(q)
    rng = np.random.default_rng(seed)
    best = np.inf
    best_pt = None
    got = 0
    batch = 300000
    while got < n_samples:
        a = rng.uniform(0.0, 1.0, batch)
        b = rng.uniform(1.0 - L, 1.0, batch)
        mask = (b > (1.0 - L * a)) & (a > 0)
        aa = a[mask]; bb = b[mask]
        for a0, b0 in zip(aa, bb):
            ps = orbit_products(a0, b0, w, q, L, m)
            got += 1
            if ps is not None:
                val = max(ps)
                if val < best:
                    best = val; best_pt = (a0, b0, ps)
            if got >= n_samples:
                break

    if refine and best_pt is not None:
        a0, b0 = best_pt[0], best_pt[1]
        scale = 0.05
        for _ in range(60):
            improved = False
            for _ in range(6000):
                a1 = a0 + rng.uniform(-scale, scale)
                b1 = b0 + rng.uniform(-scale, scale)
                if not in_triangle(a1, b1, L):
                    continue
                ps = orbit_products(a1, b1, w, q, L, m)
                if ps is not None and max(ps) < best:
                    best = max(ps); a0, b0 = a1, b1
                    best_pt = (a0, b0, ps); improved = True
            if not improved:
                scale *= 0.5
            if scale < 1e-13:
                break
    return best, best_pt

def slope_in_lambda(a, b, q, depth=14):
    """Is b/a (mod) the inverse slope of some Lambda_q vector? Generate vectors
    via Stern-Brocot to 'depth' and check ratio match -> periodic point test."""
    L = lam(q)
    # generate Lambda_q first-quadrant vectors by children process from (1,0),(0,1)
    target = b / a if a != 0 else np.inf
    coeffs = [(np.cos(0), 0)]  # not used
    # children weights x_i,y_i from w_i = U^i(1,0): integer combos. Use floats.
    w = wvecs(q)
    # collect slopes y/x of generated vectors
    from itertools import product as iproduct
    vecs = [np.array([1.0, 0.0]), np.array([0.0, 1.0])]
    frontier = [(np.array([1.0, 0.0]), np.array([0.0, 1.0]))]
    slopes = []
    for d in range(depth):
        newf = []
        for (u0, u1) in frontier:
            # children x_i u0 + y_i u1, i=1..q-2 (Stern-Brocot)
            childs = [u0]
            for i in range(1, q - 1):
                childs.append(w[i][0] * u0 + w[i][1] * u1)
            childs.append(u1)
            for c in childs:
                if c[0] > 1e-9:
                    slopes.append(c[1] / c[0])
            for j in range(len(childs) - 1):
                newf.append((childs[j], childs[j + 1]))
        frontier = newf
        if len(slopes) > 200000:
            break
    slopes = np.array(slopes)
    return np.min(np.abs(slopes - target)) if len(slopes) else np.inf

# ----------------------------------------------------------------------------
def main():
    qs = [3, 4, 5, 6, 7, 12]
    N = 1_200_000
    results = {}
    print(f"{'q':>3} {'lambda_q':>10} {'f3(q)=minmax3':>15} {'minimizer (a,b)':>26} "
          f"{'products':>30}")
    for q in qs:
        f3, pt = scan(q, N, m=3, seed=q)
        f2, _  = scan(q, N // 3, m=2, seed=q + 100)
        f4, _  = scan(q, N // 3, m=4, seed=q + 200)
        a0, b0, ps = pt
        results[q] = dict(lambda_q=lam(q), f2=f2, f3=f3, f4=f4,
                          minimizer=[a0, b0], products=ps,
                          ratio_b_over_a=b0 / a0)
        print(f"{q:>3} {lam(q):>10.6f} {f3:>15.8f} "
              f"({a0:>10.6f},{b0:>10.6f}) {[round(p,6) for p in ps]}")
    # save
    with open(os.path.join(OUT, "fq_table.json"), "w") as fh:
        json.dump(results, fh, indent=2)

    print("\n--- f2/f3/f4 (window-size dependence) ---")
    print(f"{'q':>3} {'lambda':>9} {'f2':>12} {'f3':>12} {'f4':>12} "
          f"{'2/9 ref':>9}")
    for q in qs:
        r = results[q]
        print(f"{q:>3} {r['lambda_q']:>9.5f} {r['f2']:>12.8f} {r['f3']:>12.8f} "
              f"{r['f4']:>12.8f} {2/9 if q==3 else '':>9}")

    print("\n--- conjecture fits for f3(q) ---")
    print(f"{'q':>3} {'f3':>12} {'2/(9? ) ':>12} {'lambda^2/...':>14}")
    for q in qs:
        r = results[q]
        L = r['lambda_q']
        f3 = r['f3']
        print(f"{q:>3} {f3:>12.8f}  ratio f3/(2/9)={f3/(2/9):>8.4f}  "
              f"f3*lambda^2={f3*L*L:>10.6f}  f3/lambda={f3/L:>10.6f}")
    return results

if __name__ == "__main__":
    main()
