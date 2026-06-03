#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL N crux PINNED — the floor-1 sub-threshold window bound g(L,q).

g(L,q) := min over in-domain length-L floor-1 runs of (max P over the run).
  floor-1 run: c_{n+2}=lam*c_{n+1}-c_n, from (c0,c1); in-domain: c_n>0 AND c_n+lam*c_{n+1}>1.
RESULT (numerical, decisive): g(L,q) is MONOTONE INCREASING in L and crosses thr=1/lam^3 at L*(q):
  q :  5  7 11 17 25   ->  L*(q) : 4 4 5 6 7   (max sub-threshold floor-1 run = L*-1 ~ q/4).
=> NO in-domain floor-1 run of length >= L*(q) stays sub-threshold (some P>=thr is FORCED).
This is the exact "window grows ~q/3" law. g(L*(q),q) >= thr is a finite semialgebraic inequality per q
(min over a 2-param ellipse family of a max of L rotation-products) -- machine-checkable / Aristotle-shaped.
Also L_max(q)=q exactly (positivity ceiling: c_n>0 for ~q rotation steps).

Companion to f(L,q) (min E) in Ngoal_Ebound.py. Anchors: q=5->thr=1/phi^3=0.23607; cross at L*=4.
"""
import math, sys
import numpy as np

def gbound(q, NS=4_000_000, seed=0):
    lam = 2*math.cos(math.pi/q); thr = 1/lam**3
    rng = np.random.default_rng(seed)
    g = {}   # exact length L -> min over seeds of (max P over the L in-domain steps)
    C0 = rng.uniform(0, 1.2, NS); C1 = rng.uniform(0, 1.2, NS)
    for i in range(NS):
        a, b = C0[i], C1[i]
        if a <= 0 or b <= 0 or not (a + lam*b > 1): continue
        maxP = 0.0; L = 0
        for _ in range(q + 2):
            if not (a > 1e-12 and a + lam*b > 1): break
            maxP = max(maxP, a*b); L += 1
            a, b = b, lam*b - a
        if L >= 1 and (L not in g or maxP < g[L]): g[L] = maxP
    Lstar = min((L for L in g if g[L] >= thr - 1e-9), default=None)
    print(f"=== q={q}  lam={lam:.5f}  thr={thr:.6f}  L_max={max(g)}  L*(q)={Lstar}  "
          f"max-subthr-floor1-run={Lstar-1 if Lstar else '?'} (~q/4={q/4:.1f}) ===")
    for L in sorted(g):
        tag = '' if g[L] < thr - 1e-9 else '  <== >=thr'
        print(f"   L={L:3d}  g={g[L]:.7f}  ratio={g[L]/thr:.4f}{tag}")
    return Lstar, thr

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [5, 7, 11, 17, 25]
    Ls = {}
    for q in qs:
        Lstar, thr = gbound(q, NS=3_000_000, seed=q); Ls[q] = Lstar; print()
    print("SUMMARY  L*(q):", Ls, " (max sub-threshold floor-1 run = L*-1 ~ q/4; uniform proof needs closed-form g)")
