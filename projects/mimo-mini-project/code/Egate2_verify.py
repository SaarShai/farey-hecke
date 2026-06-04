#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFY the q=60 'closed loop' flags from Egate2_periodic.
Decisive: (1) exact monodromy trace of the flagged word W_q=(q-1,3)(q-1,0)(q-3,0)
          -> elliptic (|tr|<2)? rotation number?  (2) does the rigorous grid
survivor_set (the q<=50-EMPTY tool) find a survivor at q=60,70?  If survivors=0,
the eps-returns are artifacts (rotation escapes within the period). If >0, a real
sub-threshold invariant set -> would REFUTE X_Omega=1/lam^3. Honest either way.
"""
import math
import numpy as np

def build(q):
    xx = {-1: 0.0, 0: 1.0}
    for i in range(1, q+3):
        xx[i] = 2*math.cos(math.pi/q)*xx[i-1] - xx[i-2]
    return 2*math.cos(math.pi/q), xx

def M_step(lam, X, i, k):
    return np.array([[X(i),               X(i-1)],
                     [X(i+1)+k*lam*X(i),   X(i)+k*lam*X(i-1)]], dtype=float)

def classify(tr):
    if abs(abs(tr)-2) < 1e-9: return "PARABOLIC (eigval 1 -> can fix a ray)"
    if abs(tr) < 2:
        phi = math.acos(tr/2)
        return f"ELLIPTIC rot phi={phi:.5f}=pi*{phi/math.pi:.4f}; near-period={2*math.pi/phi:.1f} steps"
    return "HYPERBOLIC (|tr|>2 -> only fixed pt = origin, NO interior periodic orbit)"

def word_trace(q, word):
    lam, xx = build(q); X = lambda j: xx[j]
    M = np.eye(2)
    for (i, k) in word:
        M = M_step(lam, X, i, k) @ M
    tr = M[0,0]+M[1,1]; det = M[0,0]*M[1,1]-M[0,1]*M[1,0]
    return tr, det, M

if __name__ == "__main__":
    print("=== (1) monodromy trace of W_q=(q-1,3)(q-1,0)(q-3,0) ===")
    for q in (18, 25, 40, 60, 70):
        w = [(q-1,3),(q-1,0),(q-3,0)]
        tr, det, M = word_trace(q, w)
        print(f"  q={q:3d}: tr(M)={tr:+.6f}  det={det:.6f}  lam={2*math.cos(math.pi/q):.6f}")
        print(f"         {classify(tr)}")
    print("\n=== (2) RIGOROUS survivor_set (grid forward-invariant fixpoint) ===")
    try:
        import sys; sys.path.insert(0, "code")
        from Igoal_survivor import survivor_set
        for q in (60, 70):
            nsurv, nS, thr, _ = survivor_set(q, Na=1600, Nb=1600, verbose=True)
            print(f"  -> q={q}: survivors={nsurv}  (0 => NO sub-thr invariant set => q=60 eps-flags are ARTIFACTS)")
    except Exception as e:
        print("  survivor_set import/run failed:", repr(e))
