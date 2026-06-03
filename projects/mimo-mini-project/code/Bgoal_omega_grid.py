#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bgoal_omega_grid.py (goal B) — assumption-free maximal-invariant-set Omega_q of the BCZ map T_q.

T_q(x,y) = (y, k*lam*y - x), k = floor((1+x)/(lam*y)), lam=2cos(pi/q).
D = {x>0,y>0,x+lam*y>1}. Farey coords => also expect x,y in (0,1].

Omega_q = support of invariant measure = set whose BI-infinite orbit stays in D.
Approximate on a grid:
  FWD survivors after N steps: F_N = {p : T^j(p) in D, j=0..N}  (shrinks to forward-invariant set)
  BWD survivors after N steps: B_N via inverse map T^{-1}.
  Omega ~ F_inf ∩ B_inf (recurrent set).
We report area(F_N) vs N (does it converge to positive measure = real domain, or ->0 = wrong coords),
and the shape (column heights y_max(x)).

Inverse map: from (x,y)=(c_n,c_{n+1}), predecessor (c_{n-1},c_n)=(x', x) with
c_{n-1} = k'*lam*x - y for the digit k' that mapped (x',x)->(x,y). Inverse is multivalued (choose k').
We instead get backward survivors by iterating forward on the TRANSPOSE/reverse: simpler to just
test forward-invariance thoroughly and separately confirm recurrence by long-orbit return.
"""
import math
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)

def fwd_survivor_mask(q, ngrid=600, nsteps=60, xmax=1.0, ymax=1.0):
    """Grid [0,xmax]x[0,ymax]; mark cells whose forward orbit stays in D for nsteps."""
    l = lam(q)
    xs = (np.arange(ngrid)+0.5)/ngrid*xmax
    ys = (np.arange(ngrid)+0.5)/ngrid*ymax
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    x = X.copy(); y = Y.copy()
    alive = (x > 0) & (y > 0) & (x + l*y > 1.0)
    for _ in range(nsteps):
        with np.errstate(divide='ignore', invalid='ignore'):
            k = np.floor((1.0 + x) / (l*y))
        yp = k*l*y - x
        xn = y; yn = yp
        # update only alive cells
        nx = np.where(alive, xn, x)
        ny = np.where(alive, yn, y)
        x, y = nx, ny
        still = alive & (x > 1e-12) & (y > 1e-12) & (x + l*y > 1.0 + 1e-12)
        alive = still
    return xs, ys, alive  # alive[i,j] over (xs[i], ys[j])

def column_profile(xs, ys, alive):
    """For each x-column, the min and max y that survive (the staircase)."""
    prof = []
    for i, xv in enumerate(xs):
        col = np.where(alive[i])[0]
        if len(col) == 0:
            prof.append((xv, None, None, 0))
        else:
            prof.append((xv, ys[col[0]], ys[col[-1]], len(col)))
    return prof

if __name__ == "__main__":
    for q in [3,4,5,6,7]:
        l = lam(q)
        print(f"\n=== q={q} lam={l:.6f} ===")
        prev_area = None
        for N in [1,2,4,8,16,32,64]:
            xs, ys, alive = fwd_survivor_mask(q, ngrid=500, nsteps=N)
            area = alive.mean()  # fraction of unit box
            tag = "" if prev_area is None else f" (ratio {area/prev_area:.3f})" if prev_area>0 else ""
            print(f"  N={N:>3}: fwd-survivor area = {area:.5f}{tag}")
            prev_area = area
        # final-shape staircase profile at N=64
        xs, ys, alive = fwd_survivor_mask(q, ngrid=200, nsteps=80)
        prof = column_profile(xs, ys, alive)
        print(f"  staircase (x: ymin..ymax  count), sampled:")
        for idx in range(0, 200, 20):
            xv, ymn, ymx, cnt = prof[idx]
            if ymn is None:
                print(f"    x={xv:.3f}: empty")
            else:
                print(f"    x={xv:.3f}: y in [{ymn:.3f},{ymx:.3f}]  (n={cnt})")
