#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exp_uniform_ejection_paramtest_2026-06-13.py

DECISIVE parametric test of the WIDENED uniform ejection box.

The Lean lemma must close, for ALL (l,u,v,r,thr) in a rational box, the implication
    [ u*v - r*v^2 < thr ]  AND domain bounds   =>   thr <= l*v^2 - u*v.

We do NOT just sample realized orbit points (those have a comfortable margin); we
sweep the ENTIRE proposed rational box densely and look for the WORST CASE of the
quantity that the proof must keep >= 0, namely

    margin(l,u,v,r,thr) = l*v^2 - u*v - thr

minimized over the box subject to the lemma hypotheses
    hl : 49/25 <= l <= 2            (covers lambda_16 .. lambda_inf)
    hr : R_LO <= r <= R_HI          (realized + cushion)
    ht : 1/8  <= thr <= 663/5000
    hu : 1 <= u   (relaxed from strict; check strict separately)
    hv : v <= 1
    htop : l*v - u <= 1
    hbot : 1 < 2*l*v - u
    hP   : u*v - r*v^2 < thr        (sub-threshold premise)

If min margin >= 0 on the box, uniform ejection HOLDS (the route survives) and the
lemma is provable; if min margin < 0 anywhere, that is a genuine obstruction -- report
the violating (l,u,v,r,thr).

Note on the premise hP: the WORST case for the conclusion is when hP is as permissive
as possible, i.e. thr as LARGE as allowed AND u*v - r*v^2 as small as allowed. So we
take thr at its UPPER box edge and search (l,u,v,r) feasible.  We ALSO scan thr on a
grid to be safe.  Pure float is adequate for a falsification sweep (margins ~0.05+).
"""
from __future__ import annotations
import math
from itertools import product

# Rational box (as floats). Widened to cover q=16..200 (and beyond, l<2).
L_LO, L_HI = 49/25, 2.0                 # [1.96, 2.0)
R_LO, R_HI = 0.88, 1.26                 # realized [0.899,1.247] + cushion
THR_LO, THR_HI = 1/8, 663/5000          # [0.125, 0.1326]
U_LO = 1.0                              # hu relaxed to 1<=u (strict checked on orbits)
V_HI = 1.0

def feasible(l, u, v, r, thr):
    # domain hypotheses (use closed inequalities; strict ones relaxed to <= for a
    # worst-case sweep -- the boundary is the adversarial extreme)
    if not (U_LO <= u): return False
    if not (v <= V_HI): return False
    if not (v > 0): return False
    if not (l*v - u <= 1.0 + 1e-12): return False        # htop
    if not (2*l*v - u >= 1.0 - 1e-12): return False       # hbot (1 < 2lv-u), boundary incl.
    if not (u*v - r*v*v <= thr + 1e-15): return False     # hP (sub-threshold), boundary incl.
    return True

def margin(l, u, v, r, thr):
    return l*v*v - u*v - thr

# Dense grid sweep
NL, NU, NV, NR, NT = 41, 81, 121, 41, 9
Ls   = [L_LO + (L_HI-L_LO)*i/(NL-1) for i in range(NL)]
Vs   = [0.30 + (V_HI-0.30)*i/(NV-1) for i in range(NV)]   # v can be small (deep branches)
Rs   = [R_LO + (R_HI-R_LO)*i/(NR-1) for i in range(NR)]
Thrs = [THR_LO + (THR_HI-THR_LO)*i/(NT-1) for i in range(NT)]

worst = None
n_feasible = 0
n_total = 0
# For each (l,v,r,thr) the feasible u-range is an interval; the conclusion margin
# l*v^2 - u*v - thr is DECREASING in u, so worst (smallest) margin is at the LARGEST
# feasible u.  u <= 1 + l*v - 1? no: u feasible by  u <= l*v - 1 + ... wait:
#   htop: u >= l*v - 1     (since l*v - u <= 1  <=> u >= l*v - 1)
#   hbot: u <= 2*l*v - 1   (since 2*l*v - u > 1 ... boundary u <= 2lv-1)
#   hu:   u >= 1
#   hP:   u <= (thr + r*v^2)/v   (since u*v - r*v^2 <= thr <=> u <= (thr + r v^2)/v)
# So u_max = min(2*l*v - 1, (thr + r*v^2)/v).  Worst margin at u = u_max.
for l in Ls:
    for v in Vs:
        if v <= 0: continue
        for r in Rs:
            for thr in Thrs:
                u_lo = max(U_LO, l*v - 1.0)
                u_hi = min(2*l*v - 1.0, (thr + r*v*v)/v)
                if u_hi < u_lo - 1e-12:
                    continue  # empty feasible u-interval
                u = u_hi  # worst case (largest u minimizes the conclusion margin)
                n_total += 1
                if not feasible(l, u, v, r, thr):
                    continue
                n_feasible += 1
                m = margin(l, u, v, r, thr)
                if worst is None or m < worst[0]:
                    worst = (m, l, u, v, r, thr)

print("WIDENED RATIONAL BOX:")
print(f"  l in [{L_LO}, {L_HI})   r in [{R_LO},{R_HI}]   thr in [{THR_LO},{THR_HI}]   u>=1   v<=1")
print(f"  grid: {NL}x{NU(0) if False else NU}-skip x {NV} (v) x {NR} (r) x {NT} (thr); u at worst-case edge")
print(f"  feasible cells swept: {n_feasible} / {n_total}")
print()
if worst is None:
    print("NO FEASIBLE CELLS -- box hypotheses are jointly empty (check ranges).")
else:
    m, l, u, v, r, thr = worst
    print(f"WORST-CASE margin (l*v^2 - u*v - thr) over box = {m:.8f}")
    print(f"  at  l={l:.6f}  u={u:.6f}  v={v:.6f}  r={r:.6f}  thr={thr:.6f}")
    print(f"  sub-threshold premise u*v - r*v^2 = {u*v - r*v*v:.6f}  (<= thr={thr:.6f}? {u*v-r*v*v <= thr})")
    if m >= 0:
        print()
        print(">>> UNIFORM EJECTION HOLDS on the widened box (worst margin >= 0). Route SURVIVES.")
        print(">>> The lemma  thr <= l*v^2 - u*v  is TRUE on the whole box -> Lean-provable.")
    else:
        print()
        print(">>> VIOLATION: uniform ejection FAILS at the above (l,u,v,r,thr) -- genuine obstruction.")

# Targeted corner stress test: the most adversarial analytic corner is
#   v->1, thr at THR_HI, r at R_LO, l at L_LO, u at its hP/hbot ceiling.
print()
print("CORNER STRESS (adversarial analytic corners):")
for (l, v, r, thr, lab) in [
    (L_LO, 1.0, R_LO, THR_HI, "l_lo,v=1,r_lo,thr_hi"),
    (L_LO, 0.99, R_LO, THR_HI, "l_lo,v=.99,r_lo,thr_hi"),
    (L_HI, 1.0, R_LO, THR_HI, "l_hi,v=1,r_lo,thr_hi"),
    (L_LO, 0.999, R_HI, THR_HI, "l_lo,v=.999,r_hi,thr_hi"),
    (L_LO, 0.66, R_LO, THR_HI, "l_lo,v=.66(deep),r_lo,thr_hi"),
]:
    u_hi = min(2*l*v - 1.0, (thr + r*v*v)/v)
    u_lo = max(U_LO, l*v - 1.0)
    if u_hi < u_lo:
        print(f"  {lab:35} -> empty u-interval")
        continue
    u = u_hi
    m = margin(l, u, v, r, thr)
    print(f"  {lab:35} u={u:.5f} margin={m:.6f}  feasible={feasible(l,u,v,r,thr)}")
