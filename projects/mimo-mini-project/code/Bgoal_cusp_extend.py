#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bgoal_cusp_extend.py (goal B) — closed-form cusp-line value + genuine hunt (global vs interior)
across q, including past the naive q=11 wall (q=12,13).

Cusp-line fixed points (b=0) of genuine BCZ_q:  family (s,0), s in (1/x_{i-1}, 1/x_i], branch i.
   w_i=(x_i,y_i)=U^i(1,0),  x_i=sin((i+1)pi/q)/sin(pi/q),  y_i=x_{i-1}=sin(i pi/q)/sin(pi/q).
   P(s,0)=s^2 x_i/y_i, min at s->1/x_{i-1}+  =>  f(i)=x_i/(y_i x_{i-1}^2)
        = sin^2(pi/q) * sin((i+1)pi/q) / sin^3(i pi/q).
   X_cusp(q)=min_{i=2..q-2} f(i)  (no-GS: s->lower edge, OPEN; cusp escape).
q=3 has no cusp line (range empty). Compare to naive V(q) and the genuine interior optimum.
"""
import math, itertools
import numpy as np
from Bgoal_genuine_hunt import (lam, ellipse_vecs, Mik, word_family, feasible_window,
                                 Phat, hunt, verify_orbit_numeric)

def f_cusp(i, q):
    s = math.sin
    return s(math.pi/q)**2 * s((i+1)*math.pi/q) / s(i*math.pi/q)**3

def X_cusp(q):
    if q < 5:
        cand = [(i, f_cusp(i,q)) for i in range(2, q-1)]
        if not cand: return None, None
    cand = [(i, f_cusp(i,q)) for i in range(2, q-1)]
    i_star, v = min(cand, key=lambda t: t[1])
    return v, i_star

def interior_hunt(q, Pmax, Kmax):
    """global hunt but EXCLUDE cusp orbits (any v_n[1] ~ 0)."""
    l = lam(q); w = ellipse_vecs(q, l)
    branches = list(range(2, q))
    alphabet = [(i, k) for i in branches for k in range(0, Kmax+1)]
    best_global = None; best_interior = None
    seen = set()
    def canon(word):
        return min(tuple(word[j:]+word[:j]) for j in range(len(word)))
    for p in range(1, Pmax+1):
        for word in itertools.product(alphabet, repeat=p):
            c = canon(list(word))
            if c in seen: continue
            seen.add(c)
            vs = word_family(list(c), w, l)
            if vs is None: continue
            win = feasible_window(list(c), vs, w, q, l)
            if win is None: continue
            s_lo, s_hi, _ = win
            mph = max(Phat(vs[n], c[n][0], w) for n in range(len(c)))
            Xc = s_lo*s_lo*mph
            is_cusp = any(abs(v[1]) < 1e-7 for v in vs)
            if best_global is None or Xc < best_global[0]-1e-12:
                best_global = (Xc, list(c), s_lo, s_hi, is_cusp)
            if not is_cusp and (best_interior is None or Xc < best_interior[0]-1e-12):
                best_interior = (Xc, list(c), s_lo, s_hi, False)
    return best_global, best_interior

if __name__ == "__main__":
    Vref = {3:2/9, 4:math.sqrt(2)/8, 5:0.25, 6:math.sqrt(3)/6, 7:0.3887395,
            8:math.cos(math.pi/8)/2, 9:0.5868241, 10:0.6881910, 11:0.8379846}
    print("=== closed-form cusp-line value X_cusp(q)=min_i f(i),  f(i)=sin^2(pi/q)sin((i+1)pi/q)/sin^3(i pi/q) ===")
    print(f"{'q':>3} {'X_cusp(q)':>12} {'argmin i':>9} {'V(q) naive':>12} {'cusp<V?':>8}")
    for q in range(3, 21):
        xc, istar = X_cusp(q)
        vr = Vref.get(q)
        if xc is None:
            print(f"{q:>3} {'(none: q<5)':>12} {'-':>9} {vr if vr else '-':>12}")
            continue
        cl = '' if vr is None else ('YES' if xc < vr else 'no')
        vs_ = f"{vr:.6f}" if vr is not None else "  (naive n/a)"
        print(f"{q:>3} {xc:>12.6f} {istar:>9} {vs_:>12} {cl:>8}")

    print("\n=== genuine hunt: GLOBAL vs INTERIOR optimum (validates cusp dominance for q>=5) ===")
    cfg = {5:(5,2), 6:(5,2), 7:(4,2), 8:(4,2)}
    for q in [5,6,7,8]:
        Pm, Km = cfg[q]
        bg, bi = interior_hunt(q, Pm, Km)
        xc, istar = X_cusp(q)
        gstr = f"X={bg[0]:.6f} word={bg[1]} cusp={bg[4]}" if bg else "none"
        istr = f"X={bi[0]:.6f} word={bi[1]}" if bi else "none"
        print(f" q={q}: GLOBAL[{gstr}]")
        print(f"        INTERIOR[{istr}]   X_cusp(closed)={xc:.6f}(i={istar})  V_naive={Vref.get(q):.6f}")

    print("\n=== PAST THE NAIVE WALL: q=12,13 (naive infeasible) — genuine well-posed? ===")
    for q in [12, 13, 16]:
        xc, istar = X_cusp(q)
        # confirm the cusp fixed-line orbit is a genuine feasible periodic orbit
        l = lam(q); w = ellipse_vecs(q, l)
        word = [(istar, 0)]
        vs = word_family(word, w, l)
        win = feasible_window(word, vs, w, q, l) if vs is not None else None
        chk = verify_orbit_numeric(q, word, win[0]) if win else None
        ok = chk is not None and chk[1.001]['periodic'] and chk[1.001]['match_itin']
        print(f" q={q}: X_Omega(cusp)={xc:.6f} (branch i={istar}), feasible_window={None if win is None else (round(win[0],4),round(win[1],4))}, "
              f"genuine-periodic-verified={ok}, no-GS(open lower)={win[2] if win else None}")
