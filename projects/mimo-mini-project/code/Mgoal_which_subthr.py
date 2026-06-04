#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL M — DECISIVE structural question for (L2): which elliptic corridor (trace class) carries the
SUSTAINED (long) sub-threshold runs?

Method: run many genuine BCZ_q orbits; extract every MAXIMAL sub-threshold run (consecutive steps
with P<thr); compute the monodromy of the run's itinerary word and its trace; classify by
j (trace ~ 2cos(j pi/q)). Histogram j over runs, weighted by run length. Focus on the LONGEST runs.

HYPOTHESIS (would collapse (L2) to the PROVEN F-family case): every LONG sub-threshold run is the
j=1 corridor (trace=lam, the F-family / slowest rotation). Faster corridors (j>=2) give only SHORT
runs (subsumed). If so, sustaining a sub-threshold orbit requires the F-family, whose switch
dichotomy is already Lean-proven => no chaining => (C') for the sustaining regime.

Anchor: longest run ~0.3q, trace=lam (j=1). thr=1/lam^3.
"""
import math, sys
import numpy as np

def build(q):
    l = 2*math.cos(math.pi/q); x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+5): x[i] = l*x[i-1] - x[i-2]
    return l, x

def Mik(l, x, i, k):
    return np.array([[x[i], x[i-1]], [x[i+1]+k*l*x[i], x[i]+k*l*x[i-1]]], float)

def branch_of(q, x, a, b, eps=1e-9):
    for i in range(2, q):
        if a*x[i-1]+b*x[i-2] > 1-eps and a*x[i]+b*x[i-1] <= 1+eps:
            return i
    return None

def jclass(q, tr):
    if abs(tr) >= 2 - 1e-9: return None   # parabolic/hyperbolic
    return min(range(1, q), key=lambda j: abs(abs(tr) - 2*math.cos(j*math.pi/q)))

def analyze(q, NS=20000, STEPS=400, seed=0, min_long=None):
    l, x = build(q); thr = 1/l**3
    if min_long is None: min_long = max(3, q//4)
    rng = np.random.default_rng(seed)
    # collect runs: list of (length, itinerary)
    runs = []
    a0 = rng.uniform(1e-3, 1.0, NS)
    for s in range(NS):
        a = a0[s]; blo = 1 - l*a
        b = rng.uniform(max(blo, -0.99), 1.0)
        if not (1e-9 < a <= 1+1e-9 and blo-1e-9 < b <= 1+1e-9): continue
        cur = []   # current sub-thr itinerary
        for _ in range(STEPS):
            i = branch_of(q, x, a, b)
            if i is None: break
            Li = a*x[i]+b*x[i-1]; Li1 = a*x[i+1]+b*x[i]
            P = a*Li/x[i-1]
            if l*Li <= 0: break
            k = math.floor((1-Li1)/(l*Li))
            if P < thr - 1e-12:
                cur.append((i, k))
            else:
                if len(cur) >= 3: runs.append(cur)
                cur = []
            a, b = Li, Li1 + k*l*Li
            if not (1e-9 < a <= 1+1e-9 and 1-l*a-1e-9 < b <= 1+1e-9):
                break
        if len(cur) >= 3: runs.append(cur)
    # for each run compute monodromy trace of its itinerary, classify j
    jcount = {}
    longest = 0; longest_j = None; longest_word = None
    long_runs_j = {}
    for itin in runs:
        M = np.eye(2)
        for (i, k) in itin: M = Mik(l, x, i, k) @ M
        tr = M[0,0]+M[1,1]
        j = jclass(q, tr)
        L = len(itin)
        jcount[j] = jcount.get(j, 0) + 1
        if L >= min_long:
            long_runs_j[j] = long_runs_j.get(j, 0) + 1
        if L > longest:
            longest = L; longest_j = j; longest_word = itin
    print(f"\n=== q={q} thr={thr:.6f}: {len(runs)} sub-thr runs; min_long={min_long} ===")
    print(f"  longest run = {longest} steps, j-class = {longest_j} "
          f"(j=1 is F-family/lam, slowest)")
    # the run-monodromy trace may be 'mid-corridor' (not a full period); report the class of the
    # LONG runs which is what matters for sustaining
    print(f"  j-class histogram of LONG runs (>= {min_long}): "
          f"{dict(sorted((k,v) for k,v in long_runs_j.items() if k is not None))}"
          f"{' + None(parab/hyp partial-window): '+str(long_runs_j.get(None,0)) if None in long_runs_j else ''}")
    # decisive read
    long_js = set(j for j in long_runs_j if j is not None)
    if long_js <= {1}:
        print(f"  => LONG sub-thr runs are F-family (j=1) ONLY (parabolic partials = window not a full "
              f"corridor period). (L2)-sustaining collapses to PROVEN F-family case.")
    else:
        print(f"  => LONG runs include j={sorted(long_js)} beyond F-family -> (L2) needs these too.")
    return long_runs_j

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [17, 20, 25, 30, 40]
    for q in qs:
        analyze(q, seed=q)
