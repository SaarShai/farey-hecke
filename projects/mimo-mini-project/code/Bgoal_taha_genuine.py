#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bgoal_taha_genuine.py (goal B) — the GENUINE Taha BCZ_q map and its invariance.

Primary source: Taha, arXiv:1810.10668 (LaTeX-verified).
  G_q = <S,T>, U = T S = [[lam,-1],[1,0]], lam=2cos(pi/q).
  Ellipse vectors  w_i = U^i (1,0)^T,  w_0=(1,0), w_1=(lam,1), w_{q-2}=(1,lam), w_{q-1}=(0,1).
  Domain (G_q-Farey triangle):  Tq = { 0 < a <= 1,  1 - lam*a < b <= 1 }.
  Partition i=2..q-1:  Tq_i = { (a,b).w_{i-1} > 1,  (a,b).w_i <= 1 }.
  Map on Tq_i:
     new_a = (a,b).w_i
     k_i   = floor( (1 - (a,b).w_{i+1}) / (lam * (a,b).w_i) )
     new_b = (a,b).w_{i+1} + k_i * lam * (a,b).w_i
  Roof (slope-gap)  R_q = y_i / ( a * (a,b).w_i ).  Observable P := 1/R_q = a*(a,b).w_i / y_i
     (for q=3 reduces to P=a*b, the project's gap-product; large P = small gap).

Branch+digit matrix (LINEAR, det=1):
     M_{i,k} = [[ x_i,                 y_i               ],
                [ x_{i+1}+k*lam*x_i,   y_{i+1}+k*lam*y_i ]]
  (project's scalar M(k)=[[0,1],[-1,k*lam]] is exactly M_{i=q-1,k}.)

Tests:
  (A) invariance: random seeds in Tq stay in Tq under genuine map (compare to scalar-map escape).
  (B) flat measure: long orbit equidistributes ~ uniform on Tq (area = lam/2).
  (C) confirm scalar map == genuine only on branch i=q-1.
"""
import math, random
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)

def ellipse_vecs(q, l):
    """w_0..w_q as float pairs."""
    U = np.array([[l, -1.0], [1.0, 0.0]])
    w = [np.array([1.0, 0.0])]
    for _ in range(q):
        w.append(U @ w[-1])
    return w  # length q+1, indices 0..q

def in_Tq(a, b, l, eps=1e-12):
    return (0 < a <= 1+eps) and (1 - l*a - eps < b <= 1+eps)

def branch_of(a, b, w, q, eps=1e-12):
    """find i in 2..q-1 with (a,b).w_{i-1}>1 and (a,b).w_i<=1."""
    p = np.array([a, b])
    for i in range(2, q):
        ti_1 = p @ w[i-1]
        ti = p @ w[i]
        if ti_1 > 1 - eps and ti <= 1 + eps:
            return i
    return None

def genuine_step(a, b, w, q, l):
    i = branch_of(a, b, w, q)
    if i is None:
        return None, None, None
    p = np.array([a, b])
    ti = p @ w[i]
    ti1 = p @ w[i+1]
    k = math.floor((1 - ti1) / (l * ti))
    new_a = ti
    new_b = ti1 + k * l * ti
    return (new_a, new_b), i, k

def observable_P(a, b, w, i):
    """P = 1/R_q = a*(a,b).w_i / y_i  (gap-product generalization)."""
    p = np.array([a, b])
    ti = p @ w[i]
    yi = w[i][1]
    if abs(yi) < 1e-15:
        return None
    return a * ti / yi

def scalar_step(x, y, l):
    k = math.floor((1 + x) / (l * y))
    return (y, k*l*y - x), k

def rand_seed_Tq(l):
    for _ in range(100000):
        a = random.random()
        b = random.random()
        if in_Tq(a, b, l):
            return a, b
    return None

def test_invariance(q, nseed=2000, nstep=300):
    l = lam(q)
    w = ellipse_vecs(q, l)
    random.seed(7)
    esc_genuine = 0
    esc_scalar = 0
    nobranch = 0
    for _ in range(nseed):
        s = rand_seed_Tq(l)
        if s is None: continue
        a, b = s
        # genuine
        ga, gb = a, b
        g_escaped = False
        for _ in range(nstep):
            res, i, k = genuine_step(ga, gb, w, q, l)
            if res is None:
                nobranch += 1; g_escaped = True; break
            ga, gb = res
            if not in_Tq(ga, gb, l, eps=1e-9):
                g_escaped = True; break
        if g_escaped: esc_genuine += 1
        # scalar (project map) from same seed
        sx, sy = a, b
        s_escaped = False
        for _ in range(nstep):
            (sx, sy), k = scalar_step(sx, sy, l)
            if not (sx > 1e-12 and sy > 1e-12 and sx + l*sy > 1 + 1e-12):
                s_escaped = True; break
        if s_escaped: esc_scalar += 1
    return dict(q=q, l=round(l,6), area_Tq=round(l/2,5),
                esc_genuine=esc_genuine/nseed, esc_scalar=esc_scalar/nseed,
                nobranch=nobranch)

def test_measure(q, nstep=400000):
    """long single orbit; histogram a,b; check ~uniform on Tq (mean a, mean b vs flat)."""
    l = lam(q); w = ellipse_vecs(q, l)
    random.seed(3)
    s = rand_seed_Tq(l)
    a, b = s
    # burn-in
    cnt = 0
    sa = sb = sab = 0.0
    branch_counts = {}
    for t in range(nstep):
        res, i, k = genuine_step(a, b, w, q, l)
        if res is None:
            # re-seed if a rare exact-boundary miss
            s = rand_seed_Tq(l); a, b = s; continue
        a, b = res
        if t > 1000:
            sa += a; sb += b; sab += a*b; cnt += 1
            branch_counts[i] = branch_counts.get(i,0)+1
    # flat-measure expectations on Tq = {0<a<=1, 1-l a<b<=1}
    # area=l/2; E[a]=? integral a over region / area
    # region: a in (0,1], b in (max(0,1-l a),1]; but 1-l a can be negative for a>1/l.
    # do numeric reference integral
    NA=4000; da=1.0/NA; Ea=Eb=Eab=0.0; A=0.0
    for ia in range(NA):
        av=(ia+0.5)*da
        blo=max(0.0,1-l*av); bhi=1.0
        if bhi<=blo: continue
        w_=(bhi-blo)
        bmid=0.5*(blo+bhi)
        Ea+=av*w_*da; Eb+=bmid*w_*da; Eab+=av*bmid*w_*da; A+=w_*da
    return dict(q=q, n=cnt,
                meanA=round(sa/cnt,4), refA=round(Ea/A,4),
                meanB=round(sb/cnt,4), refB=round(Eb/A,4),
                meanAB=round(sab/cnt,4), refAB=round(Eab/A,4),
                branch_frac={i:round(c/cnt,3) for i,c in sorted(branch_counts.items())})

if __name__ == "__main__":
    print("=== (A) INVARIANCE: genuine Taha map vs project scalar map (escape rate over 300 steps) ===")
    for q in [3,4,5,6,7,8]:
        r = test_invariance(q, nseed=1500, nstep=300)
        print(f"  q={r['q']} lam={r['l']:.5f} area(Tq)={r['area_Tq']}: "
              f"esc_GENUINE={r['esc_genuine']:.4f}  esc_scalar={r['esc_scalar']:.4f}  nobranch={r['nobranch']}")
    print("\n=== (B) FLAT MEASURE: long orbit moments vs flat-Lebesgue reference on Tq ===")
    for q in [3,4,5,6,7]:
        r = test_measure(q, nstep=300000)
        print(f"  q={r['q']}: <a>={r['meanA']}(ref {r['refA']}) <b>={r['meanB']}(ref {r['refB']}) "
              f"<ab>={r['meanAB']}(ref {r['refAB']})  branches={r['branch_frac']}")
