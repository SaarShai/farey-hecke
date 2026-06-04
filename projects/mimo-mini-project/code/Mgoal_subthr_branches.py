#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL M closure — does the SUB-THRESHOLD set collapse to few (branch,floor) pairs?

If genuine sub-threshold steps only ever use a SMALL set of (branch i, floor k) pairs, a genuine
multi-branch window lemma becomes Lean-tractable (few cases per window step) -> rigorous per-q
extension of the proven band past q=15 via essSup_ge_of_window.

Measures, over many genuine orbits at q=16,17,20,25,30:
  (1) the set of (i, k) pairs that occur on a SUB-THRESHOLD step (P<thr);
  (2) the same restricted to steps INSIDE a sub-threshold RUN of length>=3 (the sustained part);
  (3) histogram of branch i on sub-thr steps (which branches carry sub-thr at all);
  (4) the floors k that occur on sub-thr steps.
thr=1/lam^3. Anchor: F-family branches are q-1,q-3 with floors {3,0,0}; cusp q-2 at thr (k=0).
"""
import math, sys
from collections import Counter
import numpy as np

def build(q):
    l = 2*math.cos(math.pi/q); x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+5): x[i] = l*x[i-1] - x[i-2]
    return l, x

def branch_of(q, x, a, b, eps=1e-9):
    for i in range(2, q):
        if a*x[i-1]+b*x[i-2] > 1-eps and a*x[i]+b*x[i-1] <= 1+eps:
            return i
    return None

def analyze(q, NS=30000, STEPS=300, seed=0):
    l, x = build(q); thr = 1/l**3
    rng = np.random.default_rng(seed)
    pairs_all = Counter()       # (i,k) on any sub-thr step
    pairs_run = Counter()       # (i,k) on sub-thr step inside a run>=3
    branch_hist = Counter()
    floor_hist = Counter()
    a0 = rng.uniform(1e-3, 1.0, NS)
    for s in range(NS):
        a = a0[s]; blo = 1 - l*a
        b = rng.uniform(max(blo, -0.99), 1.0)
        if not (1e-9 < a <= 1+1e-9 and blo-1e-9 < b <= 1+1e-9): continue
        seq = []   # (i,k,subthr) per step
        for _ in range(STEPS):
            i = branch_of(q, x, a, b)
            if i is None: break
            Li = a*x[i]+b*x[i-1]; Li1 = a*x[i+1]+b*x[i]
            P = a*Li/x[i-1]
            if l*Li <= 0: break
            k = math.floor((1-Li1)/(l*Li))
            sub = P < thr - 1e-12
            seq.append((i, k, sub))
            a, b = Li, Li1 + k*l*Li
            if not (1e-9 < a <= 1+1e-9 and 1-l*a-1e-9 < b <= 1+1e-9): break
        # tally
        n = len(seq)
        for idx, (i, k, sub) in enumerate(seq):
            if sub:
                pairs_all[(i, k)] += 1
                branch_hist[i] += 1
                floor_hist[k] += 1
        # runs >=3
        j = 0
        while j < n:
            if seq[j][2]:
                j0 = j
                while j < n and seq[j][2]: j += 1
                if j - j0 >= 3:
                    for t in range(j0, j):
                        i, k, _ = seq[t]; pairs_run[(i, k)] += 1
            else:
                j += 1
    # report in terms of branch OFFSET from q (q-1, q-2, ...) for q-uniformity
    def off(i): return q - i
    print(f"\n=== q={q} thr={thr:.6f}: sub-threshold (branch,floor) structure ===")
    print(f"  distinct (i,k) on ANY sub-thr step: {len(pairs_all)}")
    print(f"  branch offsets (q-i) on sub-thr steps: "
          f"{sorted(set(off(i) for (i,k) in pairs_all))}")
    print(f"  floors k on sub-thr steps: {sorted(floor_hist)}")
    # the RUN (sustained) structure -- the part that matters for window lemma
    run_offsets = sorted(set(off(i) for (i,k) in pairs_run))
    run_floors = sorted(set(k for (i,k) in pairs_run))
    print(f"  --- inside runs>=3 (sustained): distinct (i,k)={len(pairs_run)} ---")
    print(f"    branch offsets (q-i): {run_offsets}")
    print(f"    floors k:             {run_floors}")
    # top pairs (offset,k) by frequency in runs
    top = sorted(pairs_run.items(), key=lambda kv: -kv[1])[:10]
    print(f"    top (offset,k) pairs in runs: {[((off(i),k), c) for (i,k),c in top]}")
    return run_offsets, run_floors

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [16, 17, 20, 25, 30]
    summary = {}
    for q in qs:
        ro, rf = analyze(q, seed=q)
        summary[q] = (ro, rf)
    print("\n=== SUMMARY: sustained-run branch offsets & floors per q ===")
    for q,(ro,rf) in summary.items():
        print(f"  q={q}: offsets(q-i)={ro}  floors={rf}  "
              f"-> #pairs ~ {len(ro)}x{len(rf)}")
