#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rotation_sweep_test.py — numerical pre-test of the ROTATION-SWEEP lower bound (goal A).

Claim under test (B-strong, sharp lower bound, feasible range q=5..11):
  No orbit of T_q in D = {x>0,y>0,x+λy>1} keeps every product P_n = c_n c_{n+1} ≤ V(q).
Equivalently every orbit has sup_n P_n > V(q), so X(q) ≥ V(q); with the family upper bound
X(q) ≤ V(q) ⇒ X(q)=V(q), unattained (no ground state).

Window form (rotation-sweep): in any window of W = q-2 consecutive in-D steps,
  max product ≥ V(q).
Equivalently the longest run of consecutive products ≤ V(q) along an in-D orbit is < W.

Map:  T_q(x,y) = (y, ⌊(1+x)/(λ y)⌋·λ y − x),  λ = 2 cos(π/q).
"""
import math, itertools
import mpmath as mp
mp.mp.dps = 50

def lam(q): return 2*math.cos(math.pi/q)

def Vq(q):
    """Exact V(q) = X(q) = s_lo^2 * maxprod, parity closed form (verified)."""
    th = mp.pi/q
    s_lo = 1/(2*mp.sin(2*th))
    if q % 2 == 0:
        maxprod = mp.cos(th)
    else:
        maxprod = mp.cos(th/2)**2
    return s_lo*s_lo*maxprod

def Tq(x, y, l):
    """One BCZ step. Returns (y, k*l*y - x, k, indomain_next)."""
    k = math.floor((1+x)/(l*y))
    yn = k*l*y - x
    return yn, k

def in_D(x, y, l):
    return x > 0 and y > 0 and (x + l*y) > 1

def run_orbit(x0, y0, l, maxsteps=2000):
    """Iterate T_q from (x0,y0); stop when leaving D or hitting maxsteps.
    Returns list of coords c[0..m] (c_n) where consecutive pairs are in-D."""
    coords = [x0, y0]
    x, y = x0, y0
    for _ in range(maxsteps):
        if not in_D(x, y, l): break
        yn, k = Tq(x, y, l)
        if yn <= 0: break
        x, y = y, yn
        coords.append(yn)
        if not in_D(x, y, l): break
    return coords

def products(coords):
    return [coords[n]*coords[n+1] for n in range(len(coords)-1)]

def max_low_run(prods, V, eps):
    """Longest run of consecutive products ≤ V*(1+eps)."""
    best = cur = 0
    thr = V*(1+eps)
    for p in prods:
        if p <= thr:
            cur += 1; best = max(best, cur)
        else:
            cur = 0
    return best

def main():
    eps = 1e-9
    print(f"{'q':>3} {'λ':>9} {'V(q)':>14} {'W=q-2':>6} {'maxrun(rand)':>12} {'#orbits':>8} {'longest in-D seg':>16}")
    rng_seed = 12345
    import random
    for q in range(5, 12):
        l = lam(q)
        V = float(Vq(q))
        W = q-2
        random.seed(rng_seed)
        worst_run = 0
        longest_seg = 0
        nseeds = 200000
        for _ in range(nseeds):
            # sample seed in D: x,y in (0, ymax), require x+l y>1
            x = random.uniform(0.0, 1.5)
            y = random.uniform(0.0, 1.5)
            if not in_D(x, y, l): continue
            coords = run_orbit(x, y, l, maxsteps=400)
            longest_seg = max(longest_seg, len(coords)-1)
            pr = products(coords)
            r = max_low_run(pr, V, eps)
            if r > worst_run:
                worst_run = r
        print(f"{q:>3} {l:>9.5f} {V:>14.10f} {W:>6} {worst_run:>12} {nseeds:>8} {longest_seg:>16}")

if __name__ == "__main__":
    main()
