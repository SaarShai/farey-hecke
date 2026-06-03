#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bgoal_optimize.py (goal B) — genuine ergodic optimization X_Omega(q)=inf_mu esssup_mu P
on the GENUINE Taha BCZ_q map (domain Tq, flat measure). Method: sublevel-set confinement.

X_Omega(q) = min V s.t. {(a,b) in Tq : P<=V} contains a BCZ_q-invariant subset
(an orbit confined forever). Found by grid-survival + bisection on V.

P(a,b) = a*(a,b).w_i / y_i  on branch i  (= a*b for q=3; large P = small gap).

Reference V(q) (project naive scalar map, feasible q<=11):
   q: 3->2/9, 4->sqrt2/8, 5->1/4, 6->sqrt3/6, 7->0.3887395, 8->cos(pi/8)/2.
"""
import math
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)

def ellipse_vecs(q, l):
    U = np.array([[l, -1.0], [1.0, 0.0]])
    w = [np.array([1.0, 0.0])]
    for _ in range(q):
        w.append(U @ w[-1])
    return w

def Pmax_over_Tq(q, ng=1200):
    """max of P over Tq, and argmax."""
    l = lam(q); w = ellipse_vecs(q, l)
    xs = (np.arange(ng)+0.5)/ng
    best = -1; arg=None
    for ai in range(ng):
        a = xs[ai]
        blo = 1 - l*a
        bs = np.linspace(max(blo,1e-6)+1e-6, 1.0, ng)
        # branch for each b
        for b in bs[::max(1,ng//200)]:
            # find branch
            for i in range(2, q):
                t1 = a*w[i-1][0]+b*w[i-1][1]
                ti = a*w[i][0]+b*w[i][1]
                if t1 > 1 and ti <= 1:
                    P = a*ti/w[i][1] if abs(w[i][1])>1e-12 else None
                    if P is not None and P>best: best=P; arg=(a,b,i)
                    break
    return best, arg

def survivor_under_cap(q, V, ng=400, nsteps=150):
    """Grid Tq; keep cells with P<=V; iterate genuine map (vectorized per branch);
    cell dies if it leaves Tq or P>V. Return surviving fraction (of Tq cells)."""
    l = lam(q); w = ellipse_vecs(q, l)
    xs = (np.arange(ng)+0.5)/ng
    ys = (np.arange(ng)+0.5)/ng*1.0  # b in (0,1]; (b<0 sliver excluded - negligible & P-irrelevant near optimum)
    A, B = np.meshgrid(xs, ys, indexing='ij')
    a = A.copy(); b = B.copy()
    # initial Tq membership
    inTq = (a > 0) & (a <= 1) & (b > 1 - l*a) & (b <= 1)
    alive = inTq.copy()
    ntq = inTq.sum()
    # precompute w arrays
    wx = np.array([w[i][0] for i in range(q+1)])
    wy = np.array([w[i][1] for i in range(q+1)])
    def Pval(a, b):
        # branch-dependent P; compute t_i for all i, pick branch
        P = np.full(a.shape, np.nan)
        assigned = np.zeros(a.shape, dtype=bool)
        for i in range(2, q):
            t1 = a*wx[i-1] + b*wy[i-1]
            ti = a*wx[i] + b*wy[i]
            mask = (~assigned) & (t1 > 1) & (ti <= 1)
            if wy[i] != 0:
                P[mask] = a[mask]*ti[mask]/wy[i]
            assigned |= mask
        return P, assigned
    # initial cap
    P0, asg0 = Pval(a, b)
    alive &= asg0 & (P0 <= V + 1e-12)
    for _ in range(nsteps):
        # apply genuine map to alive cells
        na = a.copy(); nb = b.copy()
        assigned = np.zeros(a.shape, dtype=bool)
        for i in range(2, q):
            t1 = a*wx[i-1] + b*wy[i-1]
            ti = a*wx[i] + b*wy[i]
            ti1 = a*wx[i+1] + b*wy[i+1]
            mask = alive & (~assigned) & (t1 > 1) & (ti <= 1)
            if not mask.any():
                continue
            k = np.floor((1 - ti1[mask])/(l*ti[mask]))
            na[mask] = ti[mask]
            nb[mask] = ti1[mask] + k*l*ti[mask]
            assigned |= mask
        a, b = na, nb
        # recompute membership + cap
        P, asg = Pval(a, b)
        inT = (a > 0) & (a <= 1) & (b > 1 - l*a - 1e-12) & (b <= 1 + 1e-12)
        alive = alive & assigned & asg & inT & (P <= V + 1e-12)
        if alive.sum() == 0:
            break
    return alive.sum()/max(ntq,1)

def find_Xomega(q, lo, hi, ng=350, nsteps=120, iters=22):
    """bisection: smallest V with nonzero survivors."""
    # ensure hi survives, lo doesn't
    for _ in range(iters):
        mid = 0.5*(lo+hi)
        s = survivor_under_cap(q, mid, ng=ng, nsteps=nsteps)
        if s > 0:
            hi = mid
        else:
            lo = mid
    return hi

if __name__ == "__main__":
    Vref = {3:2/9, 4:math.sqrt(2)/8, 5:0.25, 6:math.sqrt(3)/6,
            7:0.3887395, 8:math.cos(math.pi/8)/2}
    print(f"{'q':>3} {'Pmax(Tq)':>10} {'X_Omega(q)':>12} {'V(q) naive':>12} {'match?':>8}")
    for q in [3,4,5,6,7,8]:
        pm, arg = Pmax_over_Tq(q, ng=600)
        # bracket: X_Omega in (0, Pmax)
        X = find_Xomega(q, 0.0, pm, ng=320, nsteps=120, iters=20)
        vr = Vref.get(q, float('nan'))
        match = "yes" if abs(X-vr) < 0.01 else "NO"
        print(f"{q:>3} {pm:>10.5f} {X:>12.6f} {vr:>12.6f} {match:>8}  argPmax(a,b,i)={arg}")
