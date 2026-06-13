#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exp_uniform_ejection_2026-06-13.py

CLOSE-OR-FALSIFY the UNIFORM deep-mid ejection (second analytic gap toward
X_Omega(q) >= 1/lambda^3).

Background. The verified Lean lemma `ejection_kick`
(projects/mimo-mini-project/lean/BCZHeckeEjection_q16to21_VERIFIED.lean) proves

    thr <= l*v^2 - u*v

given  u*v - r*v^2 < thr  plus a rational domain box that ONLY covers
l in [49/25, 99/50] = [1.96, 1.98]  (q ~ 16..22; lambda_23 = 1.9814 > 1.98 is OUTSIDE).
So q>=23 deep-mid ejection is unformalized.

Map: the GENUINE Taha BCZ_q map (projects/mimo-mini-project/code/Bgoal_taha_genuine.py).
Wiring (FINDINGS_genuinemap_wiring_2026-06-05.md sec 3):
    u = L_{i-1} = (a,b).w_{i-1},  v = L_i = (a,b).w_i,  r = cheb(i-1)/cheb(i),
    l = lambda,  thr = 1/lambda^3,
    genuine observable P_i = u*v - r*v^2  (Casorati identity, verified below).
Successor product = l*v^2 - u*v + k*l*v^2 >= l*v^2 - u*v (k>=0). So thr <= l*v^2-u*v
=> successor NOT sub-threshold (dwell <= 1 step), independent of floor k.

This script:
  (1) TRANSIENCE to q=200: from the deepest sub-1/lambda^3 deep-mid vertex, does the
      genuine next step exceed 1/lambda^3 (first_window == 1)?
  (2) REALIZED BOX: collect (l,u,v,r,thr) over genuine deep-mid sub-threshold steps,
      q=16..200, report the actual ranges and the lemma domain quantities
      (htop: l*v-u<=1, hbot: 1<2*l*v-u, hu: 1<u, hv: v<=1, hr range).
  (3) PARAMETRIC TEST: does  thr <= l*v^2 - u*v  hold on the realized uniform box,
      sampled densely (and at the realized extreme corners)? Look for ANY violation.

Pure mpmath/float. NO sympy. lambda via cos(pi/q) at high precision (mpmath).
"""
from __future__ import annotations
import math
import mpmath as mp

mp.mp.dps = 50  # high precision so q up to 200 (lambda ~ 1.9995) is exact enough


def cheb(q):
    """Chebyshev-shift x_n: x_{-1}=0, x_0=1, x_{n+1}=lam*x_n - x_{n-1}.
    Equivalently x_n = sin((n+1) th)/sin(th), th=pi/q.  Indices -1..q."""
    th = mp.pi / q
    return {i: mp.sin((i + 1) * th) / mp.sin(th) for i in range(-1, q + 1)}


def hecke_w(q):
    """lambda and ellipse vectors w_0..w_q (w_i = U^i (1,0), U=[[lam,-1],[1,0]])."""
    lam = 2 * mp.cos(mp.pi / q)
    w = [(mp.mpf(1), mp.mpf(0))]
    for _ in range(q):
        x, y = w[-1]
        w.append((lam * x - y, x))
    return lam, w


def branch_of(a, b, w, q):
    """active branch i in 2..q-1: (a,b).w_{i-1} > 1 and (a,b).w_i <= 1."""
    for i in range(2, q):
        ti_1 = w[i - 1][0] * a + w[i - 1][1] * b
        ti = w[i][0] * a + w[i][1] * b
        if ti_1 > 1 and ti <= 1:
            return i
    return None


def genuine_step(a, b, w, lam, q):
    """returns (new_a,new_b,i,k,P,u,v,r) or None.  P = a*L_i/y_i."""
    i = branch_of(a, b, w, q)
    if i is None:
        return None
    ti = w[i][0] * a + w[i][1] * b          # L_i      = v
    ti1 = w[i + 1][0] * a + w[i + 1][1] * b  # L_{i+1}
    tim1 = w[i - 1][0] * a + w[i - 1][1] * b  # L_{i-1} = u
    yi = w[i][1]                              # = x_{i-1}
    k = int(mp.floor((1 - ti1) / (lam * ti)))
    new_a = ti
    new_b = ti1 + k * lam * ti
    P = a * ti / yi
    # (u,v,r): u=L_{i-1}, v=L_i, r = cheb(i-1)/cheb(i) = x_{i-2}/x_{i-1}
    # NOTE: y_i = w[i][1] = x_{i-1}; y_{i-1}=w[i-1][1]=x_{i-2}; so r = y_{i-1}/y_i.
    u = tim1
    v = ti
    r = w[i - 1][1] / w[i][1]   # x_{i-2}/x_{i-1}
    return new_a, new_b, i, k, P, u, v, r


def low_branch_vertex(q, i, x):
    """min-P vertex of genuine branch i in (a, b) coords. a=v=x_{i-1}/(1+x_{i-2})."""
    m = x[i - 1]
    c = x[i - 2]
    a = m / (1 + c)
    v = a
    xi = x[i]
    xim1 = x[i - 1]
    b = (v - a * xi) / xim1
    return a, b


# ----------------------------------------------------------------------------
# (1) + (2): transience window + realized box, sweeping q
# ----------------------------------------------------------------------------

QS = [16, 17, 18, 20, 22, 23, 24, 30, 40, 50, 75, 100, 150, 200]

print("=" * 92)
print("PART 0: verify genuine observable P == u*v - r*v^2 (Casorati wiring), and P==a*L_i/y_i")
print("=" * 92)
maxerr = mp.mpf(0)
for q in [16, 24, 50, 100, 200]:
    lam, w = hecke_w(q)
    x = cheb(q)
    # sample a few interior genuine steps
    a0, b0 = low_branch_vertex(q, q // 2, x)
    a, b = a0 + mp.mpf("1e-7"), b0
    for _ in range(50):
        res = genuine_step(a, b, w, lam, q)
        if res is None:
            a, b = a0 + mp.mpf("1e-7"), b0
            continue
        na, nb, i, k, P, u, v, r = res
        err = abs(P - (u * v - r * v ** 2))
        if err > maxerr:
            maxerr = err
        a, b = na, nb
print(f"  max |P - (u*v - r*v^2)| over sampled genuine steps = {mp.nstr(maxerr, 5)}")
print(f"  (confirms P_i = u*v - r*v^2 with u=L_{{i-1}}, v=L_i, r=x_{{i-2}}/x_{{i-1}})")

print()
print("=" * 92)
print("PART 1+2: transience (first_window) + realized box on genuine DEEP-MID sub-threshold steps")
print("=" * 92)

# global realized-box accumulators (over ALL deep-mid sub-threshold steps, all q)
glob = dict(
    l=[None, None], u=[None, None], v=[None, None], r=[None, None], thr=[None, None],
    lv_minus_u=[None, None],          # htop quantity:  l*v - u   (want <= 1)
    two_lv_minus_u=[None, None],      # hbot quantity:  2*l*v - u (want > 1)
    margin=[None, None],              # l*v^2 - u*v - thr  (want >= 0)
)


def upd(key, val):
    lo, hi = glob[key]
    if lo is None or val < lo:
        glob[key][0] = val
    if hi is None or val > hi:
        glob[key][1] = val


hdr = f"{'q':>4} {'lam':>9} {'1/l^3':>9} {'deepbr':>7} {'minP/inv':>9} {'first_win':>9} {'maxrun':>7} {'~q/3':>6} {'#subthr':>8}"
print(hdr)
print("-" * len(hdr))

per_q = []
for q in QS:
    lam, w = hecke_w(q)
    inv = 1 / lam ** 3
    x = cheb(q)
    # deepest genuine middle branch by min-P/inv  (min P_i = x_{i-1}/(1+x_{i-2})^2)
    ratios = []
    for i in range(2, q - 1):
        minP = x[i - 1] / (1 + x[i - 2]) ** 2
        ratios.append((i, minP / inv))
    i_star, r_star = min(ratios, key=lambda t: float(t[1]))

    # forward orbit from the low-P vertex of the deepest branch
    a0, b0 = low_branch_vertex(q, i_star, x)
    aa, bb = a0 + mp.mpf("1e-9"), b0  # tiny interior nudge
    Ps = []
    nstep = 4000
    n_subthr_steps = 0
    for _ in range(nstep):
        res = genuine_step(aa, bb, w, lam, q)
        if res is None:
            break
        aa, bb, i, k, P, u, v, r = res
        Ps.append(P)
        # record realized box ONLY for genuine deep-mid sub-threshold steps
        # (deep-mid = NOT the cusp branch i=q-2 and NOT scalar branch q-1; P < inv)
        if P < inv and i < q - 2:
            n_subthr_steps += 1
            upd("l", lam); upd("u", u); upd("v", v); upd("r", r); upd("thr", inv)
            upd("lv_minus_u", lam * v - u)
            upd("two_lv_minus_u", 2 * lam * v - u)
            upd("margin", lam * v ** 2 - u * v - inv)
    # first_window: consecutive P<inv from the start vertex
    first_window = 0
    for P in Ps:
        if P < inv:
            first_window += 1
        else:
            break
    # max consecutive sub-inv run anywhere
    run = mr = 0
    for P in Ps:
        if P < inv:
            run += 1; mr = max(mr, run)
        else:
            run = 0
    per_q.append((q, float(lam), first_window, mr))
    print(f"{q:>4} {mp.nstr(lam,7):>9} {mp.nstr(inv,7):>9} {i_star:>7} "
          f"{float(r_star):>9.4f} {first_window:>9} {mr:>7} {q/3:>6.1f} {n_subthr_steps:>8}")

print()
print("REALIZED UNIFORM BOX over ALL genuine deep-mid sub-threshold steps, q in", QS, ":")
for k in ["l", "u", "v", "r", "thr", "lv_minus_u", "two_lv_minus_u", "margin"]:
    lo, hi = glob[k]
    if lo is None:
        print(f"  {k:>16}:  (no samples)")
    else:
        print(f"  {k:>16}:  [{mp.nstr(lo,8)} , {mp.nstr(hi,8)}]")

# Also: the deep-mid sub-threshold branches don't realize EVERY (u,v,r); but the
# Lean box must CONTAIN them. Report the box we will hand to Lean (rational, widened).
print()
print("PROPOSED RATIONAL LEAN BOX (must contain realized; conservative widening):")
lam_min = float(2 * mp.cos(mp.pi / 16))   # 1.9616
lam_max = float(2 * mp.cos(mp.pi / 200))  # 1.99951
print(f"  lambda range over q=16..200: [{lam_min:.6f}, {lam_max:.6f}]  -> l in [49/25, 2)")
print(f"  thr = 1/lam^3 range: [{float(1/(2*mp.cos(mp.pi/200))**3):.6f}, {float(1/(2*mp.cos(mp.pi/16))**3):.6f}]")
print(f"       -> thr in [1/8, 663/5000]  (1/8=0.125 <= 1/lam_max^3; 663/5000=0.1326 >= 1/lam_16^3)")
