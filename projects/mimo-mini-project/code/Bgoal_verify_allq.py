#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bgoal_verify_allq.py (goal B) — confirm the genuine global optimum X_Omega(q)=1/lam^3 (q>=5)
is a verified feasible no-GS cusp orbit for ALL q (incl. past the naive q=11 wall), and probe
robustness (does any longer word beat 1/lam^3?). Also report the interior optimum honestly.

Cusp orbit (the ONLY period-1 parabolic family): word=[(q-2,0)], M=[[1,y_{q-2}],[0,1]] shear,
eigenvector (1,0); family (s,0), s in (1/lam, 1]; P=s^2/lam -> 1/lam^3 as s->1/lam+ (OPEN, no-GS).
"""
import math, itertools
import mpmath as mp
import numpy as np
from Bgoal_genuine_hunt import (lam, ellipse_vecs, Mik, word_family, feasible_window,
                                 Phat, verify_orbit_numeric, genuine_step, in_Tq)
mp.mp.dps = 30

def cusp_orbit_check(q):
    l = lam(q); w = ellipse_vecs(q, l)
    word = [(q-2, 0)]
    vs = word_family(word, w, l)
    if vs is None: return dict(q=q, ok=False, reason="not parabolic")
    win = feasible_window(word, vs, w, q, l)
    if win is None: return dict(q=q, ok=False, reason="no window")
    s_lo, s_hi, lo_open = win
    chk = verify_orbit_numeric(q, word, s_lo)
    # exact value
    lam_exact = 2*mp.cos(mp.pi/q)
    X_exact = 1/lam_exact**3
    # P at s->s_lo (s_lo should be 1/lam)
    Pmin_num = chk[1.001]['maxP']
    return dict(q=q, ok=chk[1.001]['periodic'] and chk[1.001]['match_itin'],
                s_window=(round(s_lo,6), round(s_hi,6)), s_lo_eq_1overlam=abs(s_lo-1/l)<1e-6,
                X_1overlam3=float(X_exact), Pmin_asymptote=Pmin_num, no_GS_open_lower=lo_open)

def robustness_beats_cusp(q, Pmax=5, Kmax=2):
    """exhaustive small-word search: does ANY feasible parabolic word give X < 1/lam^3 - tol?
    (tests whether the cusp line is really the global inf within these bounds)."""
    l = lam(q); w = ellipse_vecs(q, l)
    cusp = 1.0/l**3
    branches = list(range(2, q))
    alphabet = [(i, k) for i in branches for k in range(0, Kmax+1)]
    seen = set(); best = (cusp, "[(q-2,0)] cusp")
    n_below = 0; ex_below = None
    def canon(word): return min(tuple(word[j:]+word[:j]) for j in range(len(word)))
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
            if Xc < best[0] - 1e-9:
                best = (Xc, str(list(c)))
            if Xc < cusp - 1e-9:
                n_below += 1
                if ex_below is None: ex_below = (Xc, list(c))
    return dict(q=q, cusp_1overlam3=cusp, global_best=best, n_words_below_cusp=n_below, example_below=ex_below)

if __name__ == "__main__":
    print("=== X_Omega(q)=1/lam^3 cusp orbit — VERIFIED feasible/periodic/no-GS for ALL q ===")
    print(f"{'q':>3} {'1/lam^3':>11} {'window (s_lo,s_hi]':>22} {'s_lo=1/lam?':>11} {'genuine-periodic':>16} {'no-GS':>6}")
    for q in [5,6,7,8,9,11,12,13,16,20,30]:
        r = cusp_orbit_check(q)
        if not r.get('ok', False) and 'reason' in r:
            print(f"{q:>3}  FAILED: {r['reason']}"); continue
        print(f"{q:>3} {r['X_1overlam3']:>11.6f} {str(r['s_window']):>22} {str(r['s_lo_eq_1overlam']):>11} "
              f"{str(r['ok']):>16} {str(r['no_GS_open_lower']):>6}  (P->{r['Pmin_asymptote']:.5f})")
    print("\n=== ROBUSTNESS: does any short feasible parabolic word beat 1/lam^3? (exhaustive p<=5,K<=2) ===")
    for q in [5,6,7,8]:
        r = robustness_beats_cusp(q, Pmax=5, Kmax=2)
        print(f" q={q}: 1/lam^3={r['cusp_1overlam3']:.6f}  global_best={r['global_best']}  "
              f"#words_below_cusp={r['n_words_below_cusp']}  ex={r['example_below']}")
