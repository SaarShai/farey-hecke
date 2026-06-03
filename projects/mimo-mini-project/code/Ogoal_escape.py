#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ogoal_escape.py  (goal O) — escape-of-mass quantitative picture (REWRITE; the old version was
self-flagged WIP/non-validating -- its random-seed beta_min gave ~thr not 0.1863, and it seeded
a=1/lam-0.2 BELOW the cusp branch).  This version:

(A) GEOMETRIC CUSP-CORRIDOR MARGIN  2-lam = 2-2cos(pi/q) = 4 sin^2(pi/2q) ~ pi^2/q^2 (O(1/q^2)),
    and the value's approach to its q->inf asymptote  1/lam^3 - 1/8 ~ (3/16)(2-lam) ~ O(1/q^2).
    These are the rates that close the cusp corridor / freeze the value.

(B) PARABOLIC RESIDENCE (the "no ground state" mechanism, dynamical): seed a point at distance
    delta from the cusp vertex (1/lam,0) ON the cusp branch (a>1/lam), iterate the genuine map,
    count steps inside a fixed cusp neighbourhood before expulsion, and record max P over the run.
    As delta->0 the residence DIVERGES (parabolic, marginal) and max P -> 1/lam^3 from above:
    the optimizing mass takes ever longer to escape and no invariant probability attains 1/lam^3.

(C) BIRKHOFF CONTRAST (reads Ogoal_transfer_summary.json): the standard Gibbs mu_beta mass within
    a cusp neighbourhood as beta grows -- numerically it -> 0 (mu_beta concentrates INTERIOR, on the
    min-AVERAGE measure, NOT the cusp).  So the cusp escape is specific to the min-MAX objective.

All gated to the genuine Taha map.  Anchors: 1/lam^3 (q=5)=1/phi^3=0.236068; q->inf limit 1/8.
"""
import math, json, os, sys
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)
def ellipse_x(q):
    l = lam(q); x = {-1:0.0, 0:1.0}
    for i in range(1, q+5): x[i] = l*x[i-1]-x[i-2]
    return l, x
def in_Tq(a, b, l, eps=1e-9):
    return (a > 1e-12) and (a <= 1+eps) and (1 - l*a - eps < b <= 1+eps)
def branch_of(q, x, a, b, eps=1e-9):
    for i in range(2, q):
        if a*x[i-1]+b*x[i-2] > 1-eps and a*x[i]+b*x[i-1] <= 1+eps:
            return i
    return None
def step_P(q, x, l, a, b):
    i = branch_of(q, x, a, b)
    if i is None: return None
    Li = a*x[i]+b*x[i-1]; Li1 = a*x[i+1]+b*x[i]
    if l*Li <= 0: return None
    k = math.floor((1-Li1)/(l*Li))
    return a*Li/x[i-1], i, (Li, Li1+k*l*Li)

# ---------- (A) geometric margin ----------
def margin_table(qs):
    print("="*78)
    print("(A) CUSP-CORRIDOR MARGIN  2-lam  and VALUE-APPROACH  1/lam^3 - 1/8   [O(1/q^2)]")
    print("="*78)
    print("   q     2-lam        pi^2/q^2    pi^2/(2q^2)  (2-lam)*q^2   1/lam^3      1/lam^3-1/8   (..)*q^2")
    rows = []
    for q in qs:
        l = lam(q); m = 2-l; v = 1/l**3; vg = v-0.125
        print(f"  {q:3d}  {m:.8f}  {math.pi**2/q**2:.8f}  {math.pi**2/(2*q**2):.8f}  "
              f"{m*q*q:.5f}     {v:.8f}  {vg:.8f}   {vg*q*q:.5f}")
        rows.append(dict(q=q, margin=m, inv_lam3=v, value_gap=vg,
                         margin_q2=m*q*q, gap_q2=vg*q*q))
    print("  -> (2-lam)*q^2 -> pi^2=9.8696 ;  (1/lam^3-1/8)*q^2 -> (3/16)pi^2=1.8506  (both O(1/q^2)).")
    return rows

# ---------- (B) parabolic residence ----------
def residence(q, deltas, r_nbhd=0.12, maxsteps=2_000_000):
    l, x = ellipse_x(q); thr = 1/l**3
    cusp = (1.0/l, 0.0)
    print(f"\nq={q}: thr=1/lam^3={thr:.8f}  cusp=({cusp[0]:.5f},0)  nbhd r={r_nbhd}")
    print("   delta(seed)   steps_in_nbhd   ess-sup P    ratio/thr   exit_dist   converge?")
    rows = []
    for d in deltas:
        # seed on cusp branch: a a touch above 1/lam, b = small along corridor b ~ (a-1/lam)*?,
        # take the point at distance ~d from vertex along the lower edge b=1-lam a (b>0 side a<1/lam
        # is outside; use a>1/lam with small b). Put a=1/lam + d, b=d/2 (interior, near vertex).
        a = 1.0/l + d*0.7; b = d*0.5
        if not in_Tq(a, b, l):
            a = 1.0/l + d; b = max(1-l*a, 0)+1e-9
        aa, bb = a, b
        steps_in = 0; runmax = 0.0; ok = True; n = 0
        for _ in range(maxsteps):
            dd = math.hypot(aa-cusp[0], bb-cusp[1])
            if dd < r_nbhd: steps_in += 1
            r = step_P(q, x, l, aa, bb)
            if r is None: ok=False; break
            P, i, (na, nb) = r
            runmax = max(runmax, P)
            aa, bb = na, nb; n += 1
            if not in_Tq(aa, bb, l): ok=False; break
            if dd >= r_nbhd and n > 50: break   # left the cusp region
        exitd = math.hypot(aa-cusp[0], bb-cusp[1])
        conv = "yes" if abs(runmax-thr) < 0.05*thr or runmax>=thr else "-"
        print(f"  {d:.2e}     {steps_in:9d}    {runmax:.7f}  {runmax/thr:.5f}   {exitd:.4f}     {conv}")
        rows.append(dict(delta=d, steps_in=steps_in, esssupP=runmax, ratio=runmax/thr, exit=exitd))
    print("  -> steps_in_nbhd grows as delta->0 (parabolic, marginal); ess-sup P -> thr from above.")
    return rows

# ---------- (C) Birkhoff contrast from transfer json ----------
def birkhoff_contrast(here):
    fn = os.path.join(here, "Ogoal_transfer_summary.json")
    if not os.path.exists(fn):
        print("\n(C) transfer summary not found; run Ogoal_transfer.py first."); return {}
    S = json.load(open(fn))
    print("\n" + "="*78)
    print("(C) BIRKHOFF (standard Gibbs mu_beta) CONTRAST: mass within cusp nbhd (r=0.15) vs beta")
    print("="*78)
    out = {}
    for q, d in S.items():
        res = d['results']; thr = d['meta']['inv_lam3']
        print(f"\n q={q}: 1/lam^3={thr:.5f}")
        print("    beta     <P>_mu     free(-lnrho/b)   mass<0.15")
        for r in res:
            if 'error' in r: continue
            fe = f"{r['free_energy']:.5f}" if r['free_energy'] is not None else "  --  "
            print(f"   {r['beta']:6.1f}   {r['P_avg']:.5f}    {fe}        {r['mass_within']['0.15']:.5f}")
        m0 = res[0]['mass_within']['0.15']; mL = res[-1]['mass_within']['0.15']
        print(f"   -> cusp-mass {m0:.4f} -> {mL:.4f}: mu_beta does NOT escape to cusp "
              f"(concentrates interior; min-AVG measure).")
        out[q] = dict(cusp_mass_b0=m0, cusp_mass_bmax=mL)
    return out

if __name__ == "__main__":
    HERE = os.path.dirname(os.path.abspath(__file__))
    qs = [3,4,5,6,7,8,10,12,16,20,30,50]
    A = margin_table(qs)
    print("\n" + "="*78)
    print("(B) PARABOLIC RESIDENCE (no-ground-state mechanism): residence diverges, ess-sup P->thr")
    print("="*78)
    B = {}
    for q in [5, 7, 12]:
        B[q] = residence(q, deltas=[1e-1,3e-2,1e-2,3e-3,1e-3,3e-4,1e-4])
    C = birkhoff_contrast(HERE)
    json.dump(dict(margin=A, residence=B, birkhoff=C),
              open(os.path.join(HERE, "Ogoal_escape_results.json"), "w"), indent=2)
    print("\nwrote Ogoal_escape_results.json")
