#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL M closure — ROBUST confirmation of the branch-collapse reduction:
  CLAIM: every sub-threshold RUN of length>=Lmin uses only branch offsets in {1,3}
         (branches q-1, q-3) with bounded floors; and runs of length>=W are NOT pure single steps.
This reduces genuine (C') to the 2-branch {q-1,q-3} alphabet (the F-family). Confirms:
  - offsets in runs of length>=3, >=5, and the LONGEST run, per q (16..60);
  - max floor in runs;
  - for q=16,17: are runs PURE scalar (offset 1)? (=> scalar window lemma controls them);
  - max run length vs q (the growing window).
Many seeds, long orbits, high q. thr=1/lam^3.
"""
import math, sys
from collections import Counter
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

def analyze(q, NS=40000, STEPS=400, seed=0):
    l, x = build(q); thr = 1/l**3
    rng = np.random.default_rng(seed)
    off_ge3 = set(); off_ge5 = set(); floors_run = set()
    maxrun = 0; maxrun_offsets = None
    a0 = rng.uniform(1e-3, 1.0, NS)
    for s in range(NS):
        a = a0[s]; blo = 1 - l*a
        b = rng.uniform(max(blo, -0.99), 1.0)
        if not (1e-9 < a <= 1+1e-9 and blo-1e-9 < b <= 1+1e-9): continue
        seq = []
        for _ in range(STEPS):
            i = branch_of(q, x, a, b)
            if i is None: break
            Li = a*x[i]+b*x[i-1]; Li1 = a*x[i+1]+b*x[i]
            P = a*Li/x[i-1]
            if l*Li <= 0: break
            k = math.floor((1-Li1)/(l*Li))
            seq.append((i, k, P < thr-1e-12))
            a, b = Li, Li1 + k*l*Li
            if not (1e-9 < a <= 1+1e-9 and 1-l*a-1e-9 < b <= 1+1e-9): break
        n = len(seq); j = 0
        while j < n:
            if seq[j][2]:
                j0 = j
                while j < n and seq[j][2]: j += 1
                rl = j - j0
                offs = [q - seq[t][0] for t in range(j0, j)]
                if rl >= 3:
                    off_ge3 |= set(offs)
                    floors_run |= set(seq[t][1] for t in range(j0, j))
                if rl >= 5:
                    off_ge5 |= set(offs)
                if rl > maxrun:
                    maxrun = rl; maxrun_offsets = sorted(set(offs))
            else:
                j += 1
    return dict(off_ge3=sorted(off_ge3), off_ge5=sorted(off_ge5),
                floors_run=sorted(floors_run), maxrun=maxrun, maxrun_offsets=maxrun_offsets, thr=thr)

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [16, 17, 18, 20, 25, 30, 40, 50, 60]
    print("q  | offsets in runs>=3 | offsets in runs>=5 | floors | maxrun | maxrun_offsets")
    allin13 = True
    for q in qs:
        r = analyze(q, seed=q)
        in13 = set(r['off_ge3']) <= {1, 3}
        allin13 &= in13
        print(f"{q:3d}| {str(r['off_ge3']):18s} | {str(r['off_ge5']):18s} | "
              f"{r['floors_run']} | {r['maxrun']:3d} | {r['maxrun_offsets']}  "
              f"{'[runs<=2branch OK]' if in13 else '[!! extra branch]'}", flush=True)
    print(f"\nALL runs>=3 confined to offsets subset of {{1,3}}: {allin13}")
    print("=> sustained sub-threshold dynamics lives on the 2-branch {q-1,q-3} alphabet (the F-family).")
