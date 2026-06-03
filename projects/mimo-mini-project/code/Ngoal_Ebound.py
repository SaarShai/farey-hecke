#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL N crux — pin the E-lower-bound f(L,q): "a floor-1 run of length L staying in-domain forces E>=f(L,q)".

Floor-1 run: c_{n+2}=lam*c_{n+1}-c_n (rotation by theta=pi/q), determined by (c0,c1).
E = c0^2 + c1^2 - lam*c0*c1 (conserved). In-domain at step n: c_n>0 AND c_n+lam*c_{n+1}>1.
L_dom(c0,c1) = number of consecutive in-domain steps. f(L,q) = min E over runs with L_dom>=L.

Target relationship to TEST: as L grows toward the positivity ceiling (~q), does f(L,q)/(2-lam) -> thr=1/lam^3?
i.e. is the rotation's max product E/(2-lam) forced up to thr by the domain over a long run?
Also: the max in-domain floor-1 run length L_max(q) (the positivity/rotation ceiling).
"""
import math, sys
import numpy as np

def run_floor1(lam, c0, c1, maxL=400):
    """return (L_dom, E): consecutive in-domain steps for the floor-1 rotation from (c0,c1)."""
    E = c0*c0 + c1*c1 - lam*c0*c1
    a, b = c0, c1; L = 0
    for _ in range(maxL):
        if not (a > 1e-12 and a + lam*b > 1):   # in-domain test at current (c_n=a, c_{n+1}=b)
            break
        L += 1
        a, b = b, lam*b - a                       # floor-1 step
    return L, E

def fLq(q, NS=4_000_000, seed=0):
    lam = 2*math.cos(math.pi/q); thr = 1/lam**3
    rng = np.random.default_rng(seed)
    # min E for each achieved length
    minE = {}
    Lmax = 0
    # scan (c0,c1); the interesting region is near the domain boundary, c in ~(0,1.2)
    C0 = rng.uniform(0.0, 1.2, NS); C1 = rng.uniform(0.0, 1.2, NS)
    for i in range(NS):
        c0, c1 = C0[i], C1[i]
        if c0 <= 0 or c1 <= 0: continue
        if not (c0 + lam*c1 > 1): continue
        L, E = run_floor1(lam, c0, c1, maxL=3*q+10)
        if L > Lmax: Lmax = L
        if L >= 1:
            if L not in minE or E < minE[L]: minE[L] = E
    # min E for length >= L = min over all l>=L of minE[l]
    thr2l = thr*(2-lam)
    print(f"\n=== q={q}  lam={lam:.6f}  thr=1/lam^3={thr:.6f}  thr*(2-lam)={thr2l:.6f}  L_max(in-domain floor1)={Lmax} ===")
    print("   L    f(L,q)=minE(len>=L)   f/(2-lam)   ratio f/(2-lam) / thr   [thr reached?]")
    cum = math.inf
    for L in range(Lmax, 0, -1):
        if L in minE: cum = min(cum, minE[L])
    # print ascending with cumulative-min from top
    fvals = {}
    cum = math.inf
    for L in range(Lmax, 0, -1):
        if L in minE: cum = min(cum, minE[L])
        fvals[L] = cum
    for L in range(1, Lmax+1):
        f = fvals[L]
        if not math.isfinite(f): continue
        mp = f/(2-lam)
        print(f"  {L:3d}   {f:.8f}        {mp:.8f}   {mp/thr:.5f}              {'>=thr' if mp>=thr-1e-6 else ''}")
    print(f"  => as L->L_max, does f/(2-lam) -> thr? (the domain forces the rotation max product up to thr)")
    return Lmax, thr

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [5, 7, 17]
    for q in qs:
        fLq(q, NS=3_000_000, seed=q)
