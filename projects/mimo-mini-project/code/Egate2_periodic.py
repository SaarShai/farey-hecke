#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GATE 2 probe E2b: do any SUB-THRESHOLD trajectories CLOSE (periodic)?
An invariant island REQUIRES an elliptic periodic orbit lying in S={P<1/lam^3}.
Finite elliptic stretches (seen at q=18) are harmless if they never close.

Test: fine grid of sub-threshold starts; iterate; flag any orbit that returns
within eps of a previous sub-threshold point WHILE every step stayed in S
(a closed sub-threshold loop). Classify its monodromy. Also dump the (branch,k)
symbolic WORD of the longest sub-threshold runs -> are they pure generator words
of G_q=(2,q,inf)? [order-2 gen = (q-1,k=0) trace 0; order-q gen = (q-1,k=1) trace lam]
"""
import math, sys
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

def run_q(q, Ng=220, Tmax=600, eps=2e-4):
    lam, xx = build(q)
    thr = 1.0/lam**3
    X = lambda j: xx[j]
    closed = []          # closed sub-threshold loops found (would be islands)
    longest = (0, None)  # (len, word)
    n_seed = 0
    for a0 in np.linspace(0.02, 0.999, Ng):
        for b0 in np.linspace(1-lam*a0+1e-3, 1.0, Ng):
            s = step(q, lam, X, a0, b0)
            if s is None or s[2] >= thr: continue
            n_seed += 1
            a, b = a0, b0
            hist = []          # sub-threshold points in the current run
            word = []
            for t in range(Tmax):
                s = step(q, lam, X, a, b)
                if s is None: break
                ap, bp, P, i, k = s
                if P < thr - 1e-12:
                    # check closure: did we return near an earlier point of THIS run?
                    for (ha, hb) in hist:
                        if abs(a-ha) < eps and abs(b-hb) < eps:
                            closed.append((q, len(word), list(word)))
                            break
                    hist.append((a, b)); word.append((i, k))
                    if len(word) > longest[0]:
                        longest = (len(word), list(word))
                else:
                    hist = []; word = []
                a, b = ap, bp
    # summarize the longest run's word: pure branch-(q-1) generator word?
    L, w = longest
    if w is None: w = []
    branches = sorted(set(i for i, k in w))
    only_qm1 = (branches == [q-1]) if w else True
    floors = sorted(set(k for i, k in w))
    print(f"q={q:3d} thr={thr:.6f} seeds={n_seed:5d}: "
          f"CLOSED sub-thr loops (islands) = {len(closed)}")
    print(f"     longest sub-thr run L={L}  branches={branches}  floors={floors}  "
          f"{'PURE branch-(q-1) generator word' if only_qm1 else 'MIXED branches'}")
    if w:
        print(f"     word (i,k): {w[:14]}{' ...' if L>14 else ''}")
    if closed:
        cl = min(closed, key=lambda z: z[1])
        print(f"     !! shortest closed loop period={cl[1]} word={cl[2][:10]}")
    return len(closed), L, only_qm1

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [18, 25, 40, 60]
    print("=== GATE 2 probe E2b: closed (periodic) sub-threshold orbits = islands? ===")
    print("    GOAL SIGN: ZERO closed sub-thr loops; longest run = pure branch-(q-1) word\n")
    for q in qs:
        run_q(q); print()
