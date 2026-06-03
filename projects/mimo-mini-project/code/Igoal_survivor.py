#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL I — (L2) no regime-chaining: the DECISIVE refutation hunt.

Maximal forward-invariant set inside S = {P < 1/lam^3} for the genuine BCZ_q map.
A KAM-style sub-threshold invariant island (which would REFUTE X_Omega(q)=1/lam^3)
shows up as a NON-EMPTY survivor set; (L2) <=> survivor set is EMPTY.

Method (grid, rigorous-at-resolution):
  - grid (a,b) over T^q; S-cells = inT and P<thr-tol.
  - precompute for each cell the image cell (one BCZ step).
  - survivor fixpoint: cell survives iff it is in S AND its image survives.
    iterate surv <- S & surv[image] until stable; survivors = cells whose
    ENTIRE forward orbit stays in S (a sub-threshold invariant set, grid res).

Anchors: q=3->2/9, q=4->sqrt2/8, q=5->1/phi^3 (X_Omega = 1/lam^3 always).
"""
import math, sys
import numpy as np

def build(q):
    lam = 2*math.cos(math.pi/q)
    x = np.empty(q+4)
    x[0] = 0.0  # x[-1] stored at index 0 via shift: we index x via helper
    # store x_{-1..q+2} in dict-like array with offset 1
    xx = {-1: 0.0, 0: 1.0}
    for i in range(1, q+3):
        xx[i] = lam*xx[i-1] - xx[i-2]
    return lam, xx

def survivor_set(q, Na=1400, Nb=1400, tol=1e-9, max_iter=4000, verbose=True,
                 a_lo=1e-4, dilate=False):
    lam, xx = build(q)
    thr = 1.0/lam**3
    xv = np.array([xx[j] for j in range(-1, q+3)])  # index j -> xv[j+1]
    def X(j): return xv[j+1]
    # grid rectangle
    a0, a1 = a_lo, 1.0
    b1 = 1.0
    b0 = 1.0 - lam  # lowest possible b (a=1)
    da = (a1-a0)/Na
    db = (b1-b0)/Nb
    ai = (np.arange(Na)+0.5)*da + a0
    bi = (np.arange(Nb)+0.5)*db + b0
    A, B = np.meshgrid(ai, bi, indexing='ij')   # shape (Na,Nb)
    A = A.ravel(); B = B.ravel()
    N = A.size
    # inT mask
    inT = (A > 1e-12) & (A <= 1.0+1e-9) & (B > 1.0-lam*A-1e-9) & (B <= 1.0+1e-9)
    # branch index i for each cell: smallest i in 2..q-1 with L_{i-1}>1 and L_i<=1
    bri = np.full(N, -1, dtype=np.int32)
    found = np.zeros(N, dtype=bool)
    for i in range(2, q):
        Lm = A*X(i-1) + B*X(i-2)
        Li = A*X(i)   + B*X(i-1)
        cond = (~found) & (Lm > 1-1e-9) & (Li <= 1+1e-9)
        bri[cond] = i
        found |= cond
    valid = inT & found
    # observable P and image (a',b') vectorized over branch
    P = np.full(N, np.inf)
    Ap = np.full(N, np.nan); Bp = np.full(N, np.nan)
    for i in range(2, q):
        m = (bri == i) & valid
        if not m.any(): continue
        a = A[m]; b = B[m]
        Li  = a*X(i)   + b*X(i-1)
        Li1 = a*X(i+1) + b*X(i)
        P[m] = a*Li/X(i-1)
        denom = lam*Li
        k = np.floor((1.0 - Li1)/denom)
        Ap[m] = Li
        Bp[m] = Li1 + k*denom
    # S = in-domain, has a branch, P below threshold
    S = valid & (P < thr - tol)
    # image cell index
    ia = np.floor((Ap - a0)/da).astype(np.int64)
    ib = np.floor((Bp - b0)/db).astype(np.int64)
    img_ok = (ia >= 0) & (ia < Na) & (ib >= 0) & (ib < Nb) & np.isfinite(Ap)
    img_idx = np.where(img_ok, ia*Nb + ib, 0)
    # CONSERVATIVE-KEEP (dilate): a cell counts as "image survives" if the image
    # cell OR any of its 4-neighbours survives. Over-keeps => empty result is rigorous.
    if dilate:
        neigh = []
        for dia, dib in ((0,0),(1,0),(-1,0),(0,1),(0,-1)):
            ja = ia+dia; jb = ib+dib
            ok = (ja>=0)&(ja<Na)&(jb>=0)&(jb<Nb)&np.isfinite(Ap)
            neigh.append((ok, np.where(ok, ja*Nb+jb, 0)))
    # survivor fixpoint: surv <- S & img_ok & surv[image]
    surv = S.copy()
    prev = -1
    for it in range(max_iter):
        if dilate:
            img_surv = np.zeros(N, dtype=bool)
            for ok, idx in neigh:
                img_surv |= ok & surv[idx]
            nxt = surv & img_surv
        else:
            nxt = surv & img_ok & surv[img_idx]
        c = int(nxt.sum())
        if c == prev or c == 0:
            surv = nxt
            break
        prev = c
        surv = nxt
    nsurv = int(surv.sum())
    nS = int(S.sum())
    if verbose:
        print(f"  q={q} grid {Na}x{Nb} thr={thr:.6f}: |S|={nS} -> survivors={nsurv} "
              f"(iters={it})", flush=True)
        if nsurv > 0:
            idx = np.where(surv)[0]
            print(f"    SURVIVOR CELLS: a in [{A[idx].min():.5f},{A[idx].max():.5f}] "
                  f"b in [{B[idx].min():.5f},{B[idx].max():.5f}] "
                  f"P in [{P[idx].min():.6f},{P[idx].max():.6f}] thr={thr:.6f}")
    return nsurv, nS, thr, (A, B, P, surv)

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [17, 20, 30]
    print("=== (L2) refutation hunt: maximal sub-threshold invariant set (survivor) ===")
    print("    survivors==0  =>  NO sub-threshold invariant set => (L2) holds at grid res")
    for q in qs:
        survivor_set(q, Na=1400, Nb=1400)
