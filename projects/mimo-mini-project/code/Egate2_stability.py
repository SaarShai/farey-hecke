#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GATE 2 preliminary-signs probe (E2 + E3 + E6).

Question: is the sub-threshold region S = {P < 1/lam^3} of the genuine BCZ_q map
UNIFORMLY HYPERBOLIC except along the finite-dwell F-rotation? If yes, no KAM
island can trap an orbit in S => no sustained sub-threshold orbit => X_Omega>=1/lam^3.

Method (area-preserving map, det DT = 1 exactly):
  per-step Jacobian on branch i with floor k:
     DT = [[ X(i),            X(i-1)          ],
           [ X(i+1)+k*lam*X(i), X(i)+k*lam*X(i-1)]],  det = X(i)^2 - X(i-1)X(i+1) = 1.
  Sample sub-threshold starts; iterate; for each maximal consecutive run inside S,
  accumulate M = prod DT_t and classify by |tr M|:  <2 elliptic (ISLAND RISK),
  >2 hyperbolic (escapes), ~2 parabolic (marginal). Report:
   - longest sustained sub-threshold run L_max(q)            [E6 scaling]
   - stability of every long run (any elliptic composite?)   [E2 KAM test]
   - per-step trace census: which (branch,k) are neutral?    [E3 mechanism]
"""
import math, sys
import numpy as np

def build(q):
    xx = {-1: 0.0, 0: 1.0}
    for i in range(1, q+3):
        xx[i] = 2*math.cos(math.pi/q)*xx[i-1] - xx[i-2]
    return 2*math.cos(math.pi/q), xx

def step(q, lam, X, a, b):
    """one genuine BCZ_q step; returns (a',b',P,i,k,DT) or None if out-of-domain."""
    if not (a > 1e-13 and a <= 1+1e-9 and b > 1 - lam*a - 1e-9 and b <= 1+1e-9):
        return None
    i = None
    for j in range(2, q):
        Lm = a*X(j-1) + b*X(j-2)
        Lj = a*X(j)   + b*X(j-1)
        if Lm > 1-1e-9 and Lj <= 1+1e-9:
            i = j; break
    if i is None:
        return None
    Li  = a*X(i)   + b*X(i-1)
    Li1 = a*X(i+1) + b*X(i)
    if X(i-1) <= 0:
        return None
    P = a*Li/X(i-1)
    denom = lam*Li
    if denom <= 0:
        return None
    k = math.floor((1.0 - Li1)/denom)
    ap = Li
    bp = Li1 + k*denom
    DT = np.array([[X(i),            X(i-1)],
                   [X(i+1)+k*lam*X(i), X(i)+k*lam*X(i-1)]], dtype=float)
    return ap, bp, P, i, k, DT

def run_q(q, Nsamp=60, Tmax=400, seed_grid=True):
    lam, xx = build(q)
    thr = 1.0/lam**3
    X = lambda j: xx[j]
    # seed sub-threshold starts on a grid over T^q
    starts = []
    if seed_grid:
        for a in np.linspace(0.02, 0.999, Nsamp):
            for b in np.linspace(1-lam*a+1e-3, 1.0, Nsamp):
                s = step(q, lam, X, a, b)
                if s is not None and s[2] < thr:
                    starts.append((a, b))
    # track longest sustained sub-threshold run + its composite stability
    Lmax = 0
    long_runs = []     # (length, |trM|, itinerary, kseq)
    perstep = {}       # (i,k) -> [traces]  (per-step neutrality census)
    for (a0, b0) in starts:
        a, b = a0, b0
        M = np.eye(2)
        runlen = 0
        itin = []; kseq = []
        for t in range(Tmax):
            s = step(q, lam, X, a, b)
            if s is None:
                break
            ap, bp, P, i, k, DT = s
            tr1 = DT[0,0]+DT[1,1]
            perstep.setdefault((i,k), []).append(tr1)
            if P < thr - 1e-12:
                M = DT @ M
                runlen += 1
                itin.append(i); kseq.append(k)
                if runlen > Lmax:
                    Lmax = runlen
                    trM = M[0,0]+M[1,1]
                    long_runs = [(runlen, abs(trM), list(itin), list(kseq))]
                elif runlen == Lmax:
                    trM = M[0,0]+M[1,1]
                    long_runs.append((runlen, abs(trM), list(itin), list(kseq)))
            else:
                M = np.eye(2); runlen = 0; itin = []; kseq = []
            a, b = ap, bp
    # neutral per-step census: (i,k) with |trace|<2 (elliptic, island-capable)
    neutral = sorted([(ik, np.mean(v), len(v)) for ik, v in perstep.items()
                      if abs(np.mean(v)) < 2.0 - 1e-9])
    hyp = sum(1 for ik, v in perstep.items() if abs(np.mean(v)) > 2.0 + 1e-9)
    print(f"q={q:3d}  lam={lam:.5f} thr={thr:.6f}  seeds={len(starts):4d}")
    print(f"   L_max (longest sustained sub-thr run) = {Lmax}   (~q/4 = {q/4:.1f})")
    # are any longest runs elliptic (|trM|<2)?  -> island risk
    ell = [r for r in long_runs if r[1] < 2.0 - 1e-9]
    print(f"   longest-run composite |tr M|: "
          f"min={min(r[1] for r in long_runs):.3f} max={max(r[1] for r in long_runs):.3f}"
          f"  ELLIPTIC longest-runs={len(ell)} / {len(long_runs)}")
    print(f"   per-step (branch,floor) cells: total={len(perstep)}  hyperbolic={hyp}  "
          f"NEUTRAL(|tr|<2)={len(neutral)}")
    for ik, mt, n in neutral[:8]:
        i, k = ik
        tag = "F-rot(q-1,k=1)" if (i == q-1 and k == 1) else "<-- non-F neutral!"
        print(f"        branch i={i:3d} floor k={k}  mean tr={mt:+.5f}  n={n:5d}  {tag}")
    return Lmax, len(ell), neutral

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [18, 25, 40]
    print("=== GATE 2 probe: hyperbolicity of the sub-threshold region ===")
    print("    GOAL SIGN: every long sub-thr run hyperbolic (|trM|>2); the ONLY")
    print("    neutral per-step cell is the F-rotation (branch q-1, k=1).\n")
    for q in qs:
        run_q(q)
        print()
