#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL M — run down the q=60 survivor anomaly (0 @1500^2 -> 35 @3000^2).
Is it a real sub-threshold invariant set (REFUTATION) or a finer-grid near-cusp artifact?

(1) survivor counts at 1500/3000/5000/7000^2 -- track the trend.
(2) for the 3000^2 survivor cells, run EACH forward on the TRUE float map (not the grid):
    record how many steps until P >= thr (escape). If ALL escape within the known max-run
    (~0.22*q), they are NOT an invariant set -- pure grid artifact. A cell that stays
    sub-threshold for >> max-run (or forever) would be a refutation lead.
Also q=55,65,70 sanity at 3000^2 + escape test, to see if 'nonzero at fine grid' is generic.
"""
import math, sys
import numpy as np
sys.path.insert(0, "code")
from Igoal_survivor import survivor_set

def build(q):
    l = 2*math.cos(math.pi/q); x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+5): x[i] = l*x[i-1] - x[i-2]
    return l, x

def branch_of(q, x, a, b, eps=1e-9):
    for i in range(2, q):
        if a*x[i-1]+b*x[i-2] > 1-eps and a*x[i]+b*x[i-1] <= 1+eps:
            return i
    return None

def escape_steps(q, a, b, maxstep=400):
    """Run TRUE float map from (a,b); return #steps until P>=thr (escape S), or maxstep if never."""
    l, x = build(q); thr = 1/l**3
    for n in range(maxstep):
        i = branch_of(q, x, a, b)
        if i is None: return n, 'left-domain'
        Li = a*x[i]+b*x[i-1]; Li1 = a*x[i+1]+b*x[i]
        P = a*Li/x[i-1]
        if P >= thr - 1e-12: return n, 'P>=thr'
        if l*Li <= 0: return n, 'degenerate'
        k = math.floor((1-Li1)/(l*Li))
        a, b = Li, Li1 + k*l*Li
        if not (1e-12 < a <= 1+1e-9 and 1-l*a-1e-9 < b <= 1+1e-9): return n, 'left-T'
    return maxstep, 'NEVER(<thr all maxstep)'

def probe(q):
    l, x = build(q); thr = 1/l**3
    maxrun_expect = 0.22*q
    print(f"\n=== q={q}  thr={thr:.8f}  expected max-run ~{maxrun_expect:.0f} ===")
    counts = {}
    for N in (1500, 3000, 5000, 7000):
        n, nS, _, data = survivor_set(q, Na=N, Nb=N, verbose=False)
        counts[N] = n
        print(f"  survivors @{N}^2 = {n}  (|S|={nS})", flush=True)
        if N == 3000 and n > 0:
            A, B, P, surv = data
            idx = np.where(surv)[0]
            esc = []
            for j in idx:
                a, b = float(A[j]), float(B[j])
                steps, why = escape_steps(q, a, b)
                esc.append((steps, why, round(a,5), round(b,5), round(float(P[j]),6)))
            esc.sort(reverse=True)
            longest = esc[0][0]
            n_never = sum(1 for e in esc if e[1].startswith('NEVER'))
            print(f"    forward-escape on TRUE map for {len(idx)} survivor cells:")
            print(f"      longest sub-thr run = {longest} steps (expected max-run ~{maxrun_expect:.0f})")
            print(f"      cells NEVER escaping in 400 steps = {n_never}  "
                  f"{'<<< POSSIBLE REFUTATION LEAD' if n_never>0 else '(all escape -> ARTIFACT)'}")
            for e in esc[:5]:
                print(f"        steps={e[0]:3d} {e[1]:12s} a={e[2]} b={e[3]} P0={e[4]}")
    trend = [counts[N] for N in (1500,3000,5000,7000)]
    print(f"  TREND {trend}: {'-> 0 (artifact, resolution-confirmed)' if trend[-1]==0 else '-> nonzero at finest (escape-test above is decisive)'}")

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [60, 55, 65, 70]
    for q in qs:
        probe(q)
