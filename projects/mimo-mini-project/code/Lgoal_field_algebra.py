#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL L, Objective A prep: per-q field algebra for the scalar window Lean lemma.
For each q in 7..16 compute, EXACTLY (sympy):
  - lam = 2 cos(pi/q); its minimal polynomial m(t) over Q (degree d_q = phi(2q)/2),
  - the Lean field relation hps: lam^d = (power-basis tail),
  - lam^3 and lam^4 reduced to the power basis {1,lam,...,lam^{d-1}},
  - the slack form 1 - x*y*lam^3 (used for P<1/lam^3),
  - the floor bound Kmax(q): smallest case-cap so that K>=Kmax+1 is contradicted by the
    floor-helper kernel  (lam^4) x^2 < 2/(Kmax+1),  (lam^4) y^2 < 2,  1-lam x < y.
  - W(q) window (from brief: 4 for q<=12, 5 for q in 13..16); cross-check max sub-thr run.
Anchors: q=5 -> d=2 (phi), q=6 -> d=2 (lam^2=3). Validate those reproduce the known files.
"""
import sympy as sp
from sympy import cos, pi, Rational, minimal_polynomial, sqrt

def field_data(q):
    lam = 2*cos(pi/q)
    t = sp.symbols('t')
    m = sp.Poly(minimal_polynomial(lam, t), t)
    d = m.degree()
    # power-basis reduction: lam^d = -(lower terms)/leadcoeff. minpoly is monic over Z? make monic.
    mc = m.all_coeffs()  # leading first
    lead = mc[0]
    mm = [Rational(c, lead) for c in mc]  # monic
    # lam^d = -(mm[1] lam^{d-1} + ... + mm[d])
    tail = [-mm[i] for i in range(1, d+1)]  # coeff of lam^{d-1},...,lam^0 for lam^d
    # build reduction table: lam^k as vector over basis 0..d-1
    # start with identity for 0..d-1, then extend
    pb = {}
    for k in range(d):
        v = [Rational(0)]*d
        v[k] = Rational(1)
        pb[k] = v
    def shift(v):  # multiply a power-basis vector by lam
        # v[d-1]*lam^d + sum_{k<d-1} v[k] lam^{k+1}
        out = [Rational(0)]*d
        for k in range(d-1):
            out[k+1] += v[k]
        top = v[d-1]
        # lam^d -> tail (coeff of lam^{d-1}..lam^0)
        for j in range(d):
            # tail[j] is coeff of lam^{d-1-j}
            out[d-1-j] += top*tail[j]
        return out
    for k in range(d, max(d+1, 6)):
        pb[k] = shift(pb[k-1])
    lam3 = pb[3] if 3 in pb else shift(shift(shift(pb[0]))) if d>3 else None
    # ensure we have lam^3, lam^4
    cur = pb[d-1]
    allp = dict(pb)
    kk = d
    while kk <= 5:
        if kk not in allp:
            allp[kk] = shift(allp[kk-1])
        kk += 1
    def vec_to_expr(v):
        lamS = sp.symbols('lam')
        return sum(v[k]*lamS**k for k in range(d))
    lamf = float(lam.evalf(40))
    lam3v = allp[3]; lam4v = allp[4]
    # numeric check
    def vnum(v): return sum(float(v[k])*lamf**k for k in range(d))
    assert abs(vnum(lam3v)-lamf**3) < 1e-9, (q, "lam3")
    assert abs(vnum(lam4v)-lamf**4) < 1e-9, (q, "lam4")
    lam4_num = lamf**4
    # floor bound Kmax: need contradiction for K>=Kt where
    #   (lam^4)x^2 < 2/Kt,  (lam^4)y^2 < 2,  y > 1-lam x, x,y>0
    # worst: x as large as allowed -> x = sqrt(2/(Kt lam^4)); then need 1-lam x <= y < sqrt(2/lam^4)
    #   contradiction iff (1-lam x) >= sqrt(2/lam^4)  AND 1-lam x>0
    # i.e. 1 - lam*sqrt(2/(Kt lam^4)) >= sqrt(2)/lam^2
    import math
    def contradicts(Kt):
        xmax = math.sqrt(2.0/(Kt*lam4_num))
        lhs = 1 - lamf*xmax            # lower bound forced on y by edge (if >0)
        ymax = math.sqrt(2.0/lam4_num) # upper bound on y
        return lhs > ymax + 1e-12       # forced y-lower exceeds y-upper -> contradiction
    Kt = None
    for k in range(2, 60):
        if contradicts(k):
            Kt = k; break
    Kmax = (Kt-1) if Kt else None
    return dict(q=q, d=d, monic=mm, tail=tail, lam3=lam3v, lam4=lam4v,
                lam_num=lamf, Kmax=Kmax, Kt=Kt, vec_to_expr=vec_to_expr)

def fmt_vec(v, d):
    lamS = sp.symbols('lam')
    e = sum(v[k]*lamS**k for k in range(d))
    return str(sp.expand(e)).replace('**','^')

if __name__ == "__main__":
    print("q  d  Kmax  Kt   lam^d-relation                         lam^3                  lam^4")
    print("-"*110)
    for q in list(range(5,17)):
        fd = field_data(q)
        d = fd['d']
        lamS = sp.symbols('lam')
        # lam^d = sum tail[j] lam^{d-1-j}
        rel = sum(fd['tail'][j]*lamS**(d-1-j) for j in range(d))
        relstr = f"lam^{d} = " + str(sp.expand(rel)).replace('**','^')
        print(f"{q:2d} {d:2d}  {str(fd['Kmax']):>4} {str(fd['Kt']):>4}  {relstr:38s}  "
              f"{fmt_vec(fd['lam3'],d):20s}  {fmt_vec(fd['lam4'],d)}")
