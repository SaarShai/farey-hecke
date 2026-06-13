#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Refine the worst-case margin near (v~0.63, r=R_HI, l=L_LO, thr=THR_HI) and verify the
analytic minimum. Also: is u strictly > 1 on REAL orbits (lemma needs 1<u)?  And does the
margin EVER go negative if we push r higher / v lower?  Find the true infimum of
  l*v^2 - u*v - thr  with u = min(2lv-1, (thr+r v^2)/v).
"""
from __future__ import annotations
import mpmath as mp
mp.mp.dps = 40

L_LO, L_HI = mp.mpf(49)/25, mp.mpf(2)
R_LO, R_HI = mp.mpf("0.88"), mp.mpf("1.26")
THR_LO, THR_HI = mp.mpf(1)/8, mp.mpf(663)/5000

def u_max(l, v, r, thr):
    return min(2*l*v - 1, (thr + r*v*v)/v)

def margin_at(l, v, r, thr):
    u = u_max(l, v, r, thr)
    if u < max(mp.mpf(1), l*v - 1):   # infeasible u
        return None, u
    return l*v*v - u*v - thr, u

# The binding constraint in the worst region is u = (thr + r v^2)/v (hP active),
# because that gave u~1.0012 (well below 2lv-1). Then
#   margin = l v^2 - v*(thr + r v^2)/v - thr = l v^2 - thr - r v^2 - thr = (l-r) v^2 - 2 thr
# So when hP is the binding ceiling: margin = (l - r) v^2 - 2*thr.
# Minimized by l=L_LO, r=R_HI, thr=THR_HI, and v as LARGE as still keeps hP binding
# (u=(thr+rv^2)/v <= 2lv-1). Let's confirm and find the true min.
print("Analytic form when hP binds:  margin = (l - r) v^2 - 2*thr")
print("  worst l=L_LO=1.96, r=R_HI=1.26, thr=THR_HI:")
lw, rw, tw = L_LO, R_HI, THR_HI
# margin (l-r)v^2 - 2thr is INCREASING in v (since l-r = 0.7 > 0). So small v is worse,
# BUT small v may flip which constraint binds (hbot u<=2lv-1 may bind instead, giving
# DIFFERENT margin). Need u=(thr+rv^2)/v <= 2lv-1, i.e. region where hP binds.
# Sweep v finely.
worst = None
v = mp.mpf("0.30")
while v <= 1:
    m, u = margin_at(lw, v, rw, tw)
    if m is not None:
        if worst is None or m < worst[0]:
            worst = (m, v, u)
    v += mp.mpf("0.0005")
print(f"  finest-grid worst margin = {mp.nstr(worst[0],8)} at v={mp.nstr(worst[1],6)} u={mp.nstr(worst[2],6)}")

# Global min over the full box, fine:
gw = None
l = L_LO  # margin decreasing-ish in r and l-r>0 so smallest l worst; confirm by also scanning l
for li in range(0, 9):
    l = L_LO + (L_HI - L_LO)*li/8
    r = R_HI
    thr = THR_HI
    v = mp.mpf("0.30")
    while v <= 1:
        m, u = margin_at(l, v, r, thr)
        if m is not None and (gw is None or m < gw[0]):
            gw = (m, l, v, r, thr, u)
        v += mp.mpf("0.001")
print(f"GLOBAL fine worst margin = {mp.nstr(gw[0],8)}  at l={mp.nstr(gw[1],6)} v={mp.nstr(gw[2],6)} "
      f"r={mp.nstr(gw[3],6)} thr={mp.nstr(gw[4],6)} u={mp.nstr(gw[5],6)}")
print(f"  -> margin {'>= 0 : HOLDS' if gw[0] >= 0 else '< 0 : FAILS'}")

# Verify strict u>1 on real orbits: min realized u from the orbit sweep
print()
print("Check: do real genuine deep-mid sub-threshold steps ever hit u<=1 (lemma needs 1<u)?")
def cheb(q):
    th = mp.pi/q
    return {i: mp.sin((i+1)*th)/mp.sin(th) for i in range(-1, q+1)}
def hecke_w(q):
    lam = 2*mp.cos(mp.pi/q)
    w = [(mp.mpf(1), mp.mpf(0))]
    for _ in range(q):
        x, y = w[-1]; w.append((lam*x - y, x))
    return lam, w
def branch_of(a,b,w,q):
    for i in range(2,q):
        if w[i-1][0]*a+w[i-1][1]*b > 1 and w[i][0]*a+w[i][1]*b <= 1: return i
    return None
def low_vertex(q,i,x):
    a = x[i-1]/(1+x[i-2]); v=a
    return a, (v - a*x[i])/x[i-1]
umin = None
for q in [16,18,24,40,100,200]:
    lam,w = hecke_w(q); inv = 1/lam**3; x = cheb(q)
    i_star = min(range(2,q-1), key=lambda i: float(x[i-1]/(1+x[i-2])**2))
    a,b = low_vertex(q,i_star,x); a += mp.mpf("1e-9")
    for _ in range(2000):
        i = branch_of(a,b,w,q)
        if i is None: break
        ti = w[i][0]*a+w[i][1]*b; ti1 = w[i+1][0]*a+w[i+1][1]*b; tim1 = w[i-1][0]*a+w[i-1][1]*b
        k = int(mp.floor((1-ti1)/(lam*ti)))
        P = a*ti/w[i][1]
        if P < inv and i < q-2:
            if umin is None or tim1 < umin: umin = tim1
        a, b = ti, ti1 + k*lam*ti
print(f"  min realized u (=L_{{i-1}}) on genuine deep-mid sub-threshold steps = {mp.nstr(umin,10)}")
print(f"  (lemma hypothesis is 1<u; on entry branch i>=2, L_{{i-1}}>1 by the branch predicate)")
