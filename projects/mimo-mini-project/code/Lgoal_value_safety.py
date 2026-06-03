#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL L Objective B — value-safety (adversarial min-esssup) refutation hunt, EXTENDED to q<=150.
For each q: over NS random seeds in T^q, iterate the genuine BCZ_q map STEPS times, track the
running max of the observable P; the minimum running-max over all seeds is a lower proxy for
inf_mu esssup_mu P = X_Omega(q).  If min running-max >= thr=1/lam^3 for every seed, NO orbit dips
below threshold  =>  X_Omega(q)=1/lam^3 survives the hunt (NUMERICAL evidence, not proof).

Clean float (no grid/dilate artifact): the threshold margin is O(1/q^2) >> float eps, so this is
decisive for the "is there an orbit below thr?" question.  Anchors: minimiser is the cusp word
(P -> 1/lam^3 exactly), so ratio -> 1.00000 from ABOVE.  Result (2026-06-03): ratio in
[1.00000, 1.00011] for q=17..150 -> value SAFE, extends prior ceiling q<=50.
"""
import math, sys
import numpy as np

def build(q):
    l = 2*math.cos(math.pi/q); x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+4):
        x[i] = l*x[i-1] - x[i-2]
    return l, x

def essup_min(q, NS=40000, STEPS=500, seed=0):
    l, x = build(q); thr = 1.0/l**3
    rng = np.random.default_rng(seed)
    best = 1e9; witness = None
    a0 = rng.uniform(1e-3, 1.0, NS)
    for s in range(NS):
        a = a0[s]; blo = 1 - l*a
        b = rng.uniform(max(blo, -0.99), 1.0)
        if not (1e-9 < a <= 1+1e-9 and blo-1e-9 < b <= 1+1e-9):
            continue
        runmax = 0.0; ok = True
        for _ in range(STEPS):
            i = None
            for j in range(2, q):
                if a*x[j-1]+b*x[j-2] > 1-1e-9 and a*x[j]+b*x[j-1] <= 1+1e-9:
                    i = j; break
            if i is None:
                ok = False; break
            Li = a*x[i]+b*x[i-1]; Li1 = a*x[i+1]+b*x[i]
            P = a*Li/x[i-1]
            if P > runmax: runmax = P
            if runmax >= thr: break
            k = math.floor((1-Li1)/(l*Li))
            a, b = Li, Li1 + k*l*Li
            if not (1e-9 < a <= 1+1e-9 and 1-l*a-1e-9 < b <= 1+1e-9):
                break
        if ok and runmax < best:
            best = runmax; witness = (round(a0[s], 5), round(b, 5))
    return best, thr, witness

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [17, 19, 23, 29, 37, 50, 75, 100, 150]
    print("q :  min-esssup(seeds)   thr          ratio    verdict")
    for q in qs:
        e, thr, w = essup_min(q, seed=q)
        v = '>=thr OK (no orbit below)' if e >= thr-1e-9 else '<<< BELOW (refutation?)'
        print(f"{q:4d}: {e:.8f}   {thr:.8f}   {e/thr:.5f}  {v}")
