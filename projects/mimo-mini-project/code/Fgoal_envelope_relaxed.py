#!/usr/bin/env python3
"""
GOAL F (B) — find the MINIMAL hypothesis set for P_i >= 1/lam^3.
P_i = a*L_i/x_{i-1}, L_j = a x_j + b x_{j-1}.
Lower constraints only (drop upper guards L_i<=1, b<=1):
  H = { 0<a<=1, L_{i-1}>1, lam a + b > 1 }.
Test min of P_i under H (superset region). If still >=1/lam^3, the envelope has a CLEANER
proof (fewer hypotheses). Also test which single hypotheses can be dropped.
"""
import math, random
random.seed(11)

def build(q):
    lam = 2*math.cos(math.pi/q)
    x = {-1:0.0,0:1.0}
    for i in range(1,q+2): x[i]=lam*x[i-1]-x[i-2]
    return lam,x

def test(q, NS=4_000_000):
    lam,x = build(q); thr=1/lam**3
    res={}
    for i in range(2,q-1):  # i=2..q-2
        minP_H = 1e9; argH=None
        # H: 0<a<=1, L_{i-1}>1, lam a + b >1   (drop upper guards)
        for _ in range(NS//(q)):
            a=random.uniform(1e-5,1.0)
            # need L_{i-1}=a x_{i-1}+b x_{i-2}>1 and lam a+b>1; pick b in a wide range
            b=random.uniform(-3.0, 2.0)
            if not (a*x[i-1]+b*x[i-2] > 1.0): continue
            if not (lam*a+b > 1.0): continue
            Li = a*x[i]+b*x[i-1]
            P = a*Li/x[i-1]
            if P<minP_H: minP_H=P; argH=(a,b)
        res[i]=(minP_H,thr,argH)
    return res

for q in [5,6,7,8,10]:
    print(f"\n=== q={q} (lower-constraints-only: 0<a<=1, L_{{i-1}}>1, lam a+b>1) ===")
    r=test(q)
    lam,x=build(q); thr=1/lam**3
    for i in sorted(r):
        mp,_,arg=r[i]
        tag=" <CUSP>" if i==q-2 else ""
        flag = "  ** BELOW thr! **" if mp<thr-1e-6 else ""
        print(f"  i={i}{tag}: minP={mp:.6f} thr={thr:.6f} ratio={mp/thr:.4f} at {arg}{flag}")
