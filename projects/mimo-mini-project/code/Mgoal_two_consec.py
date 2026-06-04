#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL M closure — RIGOROUS route for q<=17: the "2-consecutive => scalar" lemma.

CLAIM (to test, then prove by Positivstellensatz): for q in the pure-scalar regime,
  if P(a,b) < thr  AND  P(T(a,b)) < thr   then  (a,b) is on the SCALAR branch q-1.
Equivalently: a NON-scalar sub-threshold step is ALWAYS followed by an above-threshold step
(non-scalar sub-thr steps are ISOLATED). If so, then 5 consecutive sub-thr steps => the first 4
are scalar => the scalar recurrence holds across the window => goal-L g16/g17 (no 5 consecutive
scalar sub-thr) gives a contradiction => no 5 consecutive genuine sub-thr => essSup_ge_of_window
(W=5) => X_Omega(q) >= 1/lam^3.  RIGOROUSLY closes q=16,17.

Test via a FINE GRID over T^q (deterministic, not random): for every cell with P<thr and next
also P<thr, record its branch. If all == q-1, claim holds at grid resolution. Also report the
worst non-scalar sub-thr step's successor P (margin above thr) to see how robust.
thr=1/lam^3.
"""
import math, sys
import numpy as np

def build(q):
    l = 2*math.cos(math.pi/q); x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+6): x[i] = l*x[i-1] - x[i-2]
    return l, x

def branch_of(q, x, a, b, eps=1e-9):
    for i in range(2, q):
        if a*x[i-1]+b*x[i-2] > 1-eps and a*x[i]+b*x[i-1] <= 1+eps:
            return i
    return None

def step(q, x, l, a, b):
    i = branch_of(q, x, a, b)
    if i is None: return None
    Li = a*x[i]+b*x[i-1]; Li1 = a*x[i+1]+b*x[i]
    if l*Li <= 0: return None
    P = a*Li/x[i-1]
    k = math.floor((1-Li1)/(l*Li))
    a2, b2 = Li, Li1 + k*l*Li
    if not (1e-12 < a2 <= 1+1e-9 and 1-l*a2-1e-9 < b2 <= 1+1e-9):
        return (P, i, None)
    return (P, i, (a2, b2))

def test(q, N=2400):
    l, x = build(q); thr = 1/l**3
    bad = []          # non-scalar steps with P<thr AND successor P<thr
    nonscalar_subthr = 0
    worst_succ_margin = math.inf   # min over non-scalar sub-thr of (succ P - thr); >0 => claim holds
    a_lo = 1e-4
    da = (1.0 - a_lo)/N
    for ia in range(N):
        a = a_lo + (ia+0.5)*da
        blo = 1 - l*a
        db = (1.0 - blo)/N
        for ib in range(N):
            b = blo + (ib+0.5)*db
            if not (1e-9 < a <= 1+1e-9 and blo-1e-9 < b <= 1+1e-9): continue
            r = step(q, x, l, a, b)
            if r is None: continue
            P, i, nxt = r
            if P < thr - 1e-12 and i != q-1:
                nonscalar_subthr += 1
                if nxt is not None:
                    r2 = step(q, x, l, nxt[0], nxt[1])
                    if r2 is not None:
                        P2 = r2[0]
                        worst_succ_margin = min(worst_succ_margin, P2 - thr)
                        if P2 < thr - 1e-12:
                            bad.append((round(a,5), round(b,5), i, round(P,6), round(P2,6)))
    print(f"q={q:2d} thr={thr:.6f} grid {N}^2: non-scalar sub-thr cells={nonscalar_subthr}  "
          f"violations(2-consec non-scalar)={len(bad)}  "
          f"worst successor margin (P2-thr)={worst_succ_margin:.6f}")
    if bad:
        print(f"   !! CLAIM FALSE at q={q}: examples (a,b,branch,P,P_next):")
        for z in bad[:8]: print(f"      {z}")
    else:
        print(f"   CLAIM HOLDS at q={q} (grid): every non-scalar sub-thr step has successor >= thr "
              f"=> 2 consecutive sub-thr => scalar branch.")
    return len(bad) == 0

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [16, 17, 18, 20]
    for q in qs:
        test(q)
