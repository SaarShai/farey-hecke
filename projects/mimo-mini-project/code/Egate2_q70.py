#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFY q=70 survivor_set=33 flag: artifact or real island?
The rigorous grid fixpoint flagged 33 survivor cells at a~b~0.334. Memory warns
'survivor COUNT unreliable at fine grid'. Decisive test: iterate the EXACT (float64,
no grid binning) genuine map on a fine sweep of that cluster; if EVERY point reaches
P>=thr within the horizon (escapes), the 33 are artifacts and X_Omega(70)=1/lam^3
stands. If any point stays sub-threshold for the whole horizon -> real concern.
"""
import math
import numpy as np

def build(q):
    xx = {-1: 0.0, 0: 1.0}
    for i in range(1, q+3):
        xx[i] = 2*math.cos(math.pi/q)*xx[i-1] - xx[i-2]
    return 2*math.cos(math.pi/q), xx

def step(q, lam, X, a, b):
    if not (a > 1e-13 and a <= 1+1e-9 and b > 1 - lam*a - 1e-9 and b <= 1+1e-9):
        return None
    i = None
    for j in range(2, q):
        if a*X(j-1)+b*X(j-2) > 1-1e-9 and a*X(j)+b*X(j-1) <= 1+1e-9:
            i = j; break
    if i is None: return None
    Li  = a*X(i)   + b*X(i-1)
    Li1 = a*X(i+1) + b*X(i)
    if X(i-1) <= 0: return None
    P = a*Li/X(i-1)
    denom = lam*Li
    if denom <= 0: return None
    k = math.floor((1.0 - Li1)/denom)
    return Li, Li1 + k*denom, P, i, k

def escape_test(q, box=(0.330,0.358,0.330,0.358), Ng=140, horizon=4000):
    lam, xx = build(q); X = lambda j: xx[j]
    thr = 1.0/lam**3
    a0,a1,b0,b1 = box
    worst_dwell = 0; worst_pt = None; n_in = 0; n_trapped = 0
    for a in np.linspace(a0, a1, Ng):
        for b in np.linspace(b0, b1, Ng):
            s = step(q, lam, X, a, b)
            if s is None or s[2] >= thr: continue
            n_in += 1
            ca, cb = a, b
            dwell = 0; trapped = True
            for t in range(horizon):
                s = step(q, lam, X, ca, cb)
                if s is None:
                    trapped = False; break          # left domain -> escaped
                ap, bp, P, i, k = s
                if P >= thr - 1e-13:
                    trapped = False; break          # P reached threshold -> escaped
                dwell += 1
                ca, cb = ap, bp
            if dwell > worst_dwell:
                worst_dwell = dwell; worst_pt = (a, b)
            if trapped:
                n_trapped += 1
    print(f"q={q} thr={thr:.6f} box={box} grid {Ng}x{Ng} horizon={horizon}")
    print(f"   sub-thr seeds tested = {n_in}")
    print(f"   max sub-thr DWELL before escape = {worst_dwell}  at {worst_pt}")
    print(f"   seeds still trapped at horizon (CANDIDATE ISLANDS) = {n_trapped}")
    if n_trapped == 0:
        print(f"   => ALL escape => survivor_set=33 was a GRID ARTIFACT; X_Omega(70)=1/lam^3 stands.")
    else:
        print(f"   => {n_trapped} seeds did NOT escape in {horizon} steps => investigate (real?).")
    return n_trapped, worst_dwell

if __name__ == "__main__":
    print("=== q=70 cluster true-map escape test (a~b~0.334) ===")
    escape_test(70)
    print("\n=== control: q=60 same box (survivor_set said 0) ===")
    escape_test(60)
