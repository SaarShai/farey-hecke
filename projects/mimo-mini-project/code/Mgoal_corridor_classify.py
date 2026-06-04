#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL M — corridor classification: TEST the structural backbone of (L2).

THESIS (Hecke triangle group rigidity): the genuine BCZ_q branch matrices M_{i,k}
generate (a subgroup of) the Hecke group G_q = (2,q,inf) triangle group.  Hence EVERY
elliptic word monodromy (|tr|<2) has FINITE order in G_q, so its trace lies in the
finite explicit set  {0} U {2cos(j*pi/q) : j=1..q-1}  (order-2 and order-q torsion).
The SLOWEST rotation (|trace| largest, < 2) is j=1, trace = lam = 2cos(pi/q) = the
W_q / F-family / fundamental rotation R.  =>  no corridor rotates slower than pi/q
=>  the F-family has the LONGEST sub-threshold arc.

This script DECISIVELY tests that thesis:
  (1) broad float sweep over words (branches q-1..q-5, digits 0..K, len<=L): collect all
      DISTINCT elliptic traces |tr|<2.
  (2) for each distinct elliptic trace t, find best integer j with |t - 2cos(j*pi/q)| min;
      report max residual.  (Thesis: residual ~ 0 for ALL.)
  (3) confirm max |trace| over elliptic words == lam (j=1), realised by the F-family.
  (4) ADVERSARIAL: report any elliptic word whose trace is NOT 2cos(j*pi/q) (would break
      the classification) or |trace|>lam (would be a slower rotation -> longer arc).
  (5) high-precision (mpmath dps=50) re-verification of the distinct traces found.

Anchors: q=5 -> the elliptic traces should be multiples 2cos(j*pi/5); W_q trace=lam.
"""
import math, itertools, sys
import numpy as np

def build(q):
    lam = 2*math.cos(math.pi/q)
    xx = {-1: 0.0, 0: 1.0}
    for i in range(1, q+5):
        xx[i] = lam*xx[i-1] - xx[i-2]
    return lam, xx

def Mik(lam, xx, i, k):
    return np.array([[xx[i], xx[i-1]],
                     [xx[i+1]+k*lam*xx[i], xx[i]+k*lam*xx[i-1]]], float)

def classify(q, L=4, K=3, branches=None, tol=2e-6):
    lam, xx = build(q)
    if branches is None:
        branches = [b for b in (q-1, q-2, q-3, q-4, q-5) if 2 <= b <= q-1]
    letters = [(i, k) for i in branches for k in range(0, K+1)]
    gens = {ltr: Mik(lam, xx, ltr[0], ltr[1]) for ltr in letters}
    # allowed quantized traces: order-q torsion {2cos(j pi/q)} PLUS order-2 torsion {0}
    quant = {j: 2*math.cos(j*math.pi/q) for j in range(0, q+1)}
    quant['S'] = 0.0   # order-2 elliptic (the "2" in the (2,q,inf) triangle group)
    distinct = {}     # rounded trace -> (word, trace, det)
    n_ell = 0
    worst_resid = 0.0; worst_word = None
    slower_than_lam = []   # |tr|>lam but <2  (would be a slower rotation than F-family)
    nonquant = []          # elliptic trace not matching any 2cos(j pi/q)
    for ln in range(1, L+1):
        for w in itertools.product(letters, repeat=ln):
            M = np.eye(2)
            for ltr in w:
                M = gens[ltr] @ M
            tr = M[0,0]+M[1,1]
            det = M[0,0]*M[1,1]-M[0,1]*M[1,0]
            if abs(det-1) > 1e-6:
                continue
            if abs(tr) < 2 - 1e-9:    # elliptic
                n_ell += 1
                key = round(tr, 6)
                if key not in distinct:
                    distinct[key] = (list(w), tr, det)
                # quantization residual
                jbest = min(quant.keys(), key=lambda j: abs(abs(tr)-abs(quant[j])))
                resid = abs(abs(tr) - abs(quant[jbest]))
                if resid > worst_resid:
                    worst_resid = resid; worst_word = (list(w), tr, jbest)
                if resid > tol:
                    nonquant.append((list(w), tr, jbest, resid))
                if abs(tr) > lam + 1e-7:
                    slower_than_lam.append((list(w), tr))
    return lam, distinct, n_ell, worst_resid, worst_word, nonquant, slower_than_lam, quant

def report(q, L=4, K=3):
    lam, distinct, n_ell, worst_resid, worst_word, nonquant, slower, quant = classify(q, L, K)
    print(f"\n=== q={q}  (lam={lam:.10f}, L<={L}, K<={K}) ===")
    print(f"  elliptic words found: {n_ell}   distinct elliptic traces: {len(distinct)}")
    # max |trace|
    maxtr = max((abs(t) for (_,t,_) in distinct.values()), default=0.0)
    print(f"  max |elliptic trace| = {maxtr:.10f}   lam = {lam:.10f}   "
          f"(F-family slowest? {abs(maxtr-lam)<1e-6})")
    print(f"  WORST quantization residual |tr - 2cos(j pi/q)| = {worst_resid:.2e}"
          f"  (word {worst_word[0]}, tr={worst_word[1]:.6f}, j={worst_word[2]})")
    # list a few distinct traces with their j
    print("  distinct elliptic traces (top 10 by |tr|) -> nearest j:")
    for t in sorted(distinct, key=lambda k: -abs(k))[:10]:
        w, tr, det = distinct[t]
        jbest = min(quant.keys(), key=lambda j: abs(abs(tr)-abs(quant[j])))
        ang = math.acos(max(-1,min(1,tr/2)))
        print(f"    tr={tr:+.8f}  j={jbest}  2cos(j pi/q)={quant[jbest]*(1 if tr>0 else -1):+.8f}"
              f"  rot=pi*{ang/math.pi:.4f}  word={w}")
    if nonquant:
        print(f"  !!! NON-QUANTIZED elliptic traces (CLASSIFICATION BREAK): {len(nonquant)}")
        for w, tr, j, r in nonquant[:6]:
            print(f"      word={w} tr={tr:.8f} resid={r:.2e}")
    else:
        print("  OK: every elliptic trace matches 2cos(j pi/q) within tol.")
    if slower:
        print(f"  !!! SLOWER-THAN-lam elliptic words (|tr|>lam, <2): {len(slower)} "
              f"-> would beat F-family arc!")
        for w, tr in slower[:6]:
            print(f"      word={w} tr={tr:.8f}")
    else:
        print("  OK: no elliptic word slower than lam (F-family = slowest rotation).")
    return distinct

def hp_verify(q, distinct):
    """High-precision (mpmath) recompute of the distinct traces: confirm quantization."""
    try:
        import mpmath as mp
    except ImportError:
        print("  (mpmath unavailable; skipping HP verify)"); return
    mp.mp.dps = 50
    lam = 2*mp.cos(mp.pi/q)
    xx = {-1: mp.mpf(0), 0: mp.mpf(1)}
    for i in range(1, q+5):
        xx[i] = lam*xx[i-1] - xx[i-2]
    def Mik_hp(i, k):
        return mp.matrix([[xx[i], xx[i-1]],
                          [xx[i+1]+k*lam*xx[i], xx[i]+k*lam*xx[i-1]]])
    worst = mp.mpf(0)
    for t, (w, trf, det) in distinct.items():
        M = mp.eye(2)
        for (i, k) in w:
            M = Mik_hp(i, k) * M
        tr = M[0,0]+M[1,1]
        cands = [abs(2*mp.cos(j*mp.pi/q)) for j in range(0,q+1)] + [mp.mpf(0)]
        jbest = min(range(len(cands)), key=lambda j: abs(abs(tr)-cands[j]))
        resid = abs(abs(tr) - cands[jbest])
        if resid > worst: worst = resid
    print(f"  HP(dps=50) worst quantization residual over {len(distinct)} distinct traces: {mp.nstr(worst,5)}")

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [5, 17, 20, 23, 29, 37, 50]
    for q in qs:
        d = report(q, L=4, K=3)
        hp_verify(q, d)
