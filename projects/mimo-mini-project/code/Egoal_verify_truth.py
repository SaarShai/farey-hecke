#!/usr/bin/env python3
"""CRITICAL: is g5_no_four_below TRUE (with cap)? For each integer floor combo
(K0,K1,K2), coords are LINEAR in (a,b): c=K0 phi b-a, d=K1 phi c-b, e=K2 phi d-c.
Minimize  max(P0,P1,P2,P3)  over the feasible (a,b)-polygon (cap+domain+pos+floorUB).
If the global min-over-combos of [min-max] >= thr, window-4 holds. Use scipy."""
import math, itertools
import numpy as np
from scipy.optimize import linprog, minimize
phi=(1+math.sqrt(5))/2; l=phi; thr=1.0/phi**3
print(f"phi={phi:.10f} thr=1/phi^3={thr:.10f}")

def coords(a,b,K0,K1,K2):
    c=K0*l*b-a; d=K1*l*c-b; e=K2*l*d-c
    return a,b,c,d,e

def maxP(ab,K):
    a,b=ab; cc=coords(a,b,*K)
    Ps=[cc[j]*cc[j+1] for j in range(4)]
    return max(Ps)

def feasible_penalty(ab,K):
    a,b=ab; cc=coords(a,b,*K)
    pen=0.0
    for x in cc:
        if x<=0: pen+=(1e-6-x)*100+1
        if x>1: pen+=(x-1)*100
    for j in range(4):
        s=cc[j]+l*cc[j+1]
        if s<=1: pen+=(1-s)*100
    # floor consistency: K_i = floor((1+c_i)/(phi c_{i+1}))
    for (ci,cj,K_) in [(cc[0],cc[1],K[0]),(cc[1],cc[2],K[1]),(cc[2],cc[3],K[2])]:
        if cj<=0: pen+=10; continue
        v=(1+ci)/(l*cj)
        if v<K_: pen+=(K_-v)*100
        if v>=K_+1: pen+=(v-(K_+1))*100
    return pen

best_overall=(9,None,None)
for K in itertools.product(range(1,4),range(1,4),range(1,4)):
    # fine grid then local refine
    bestv=9; bestab=None
    for ia in range(1,1201):
        a=ia/1200.0
        # b s.t. coords in range; scan b in (0,1]
        for ib in range(1,801):
            b=ib/800.0
            cc=coords(a,b,*K)
            if any(x<=1e-9 for x in cc): continue
            if any(x>1+1e-12 for x in cc): continue
            if not all(cc[j]+l*cc[j+1]>1 for j in range(4)): continue
            okf=True
            for (ci,cj,K_) in [(cc[0],cc[1],K[0]),(cc[1],cc[2],K[1]),(cc[2],cc[3],K[2])]:
                v=(1+ci)/(l*cj)
                if not (K_<=v<K_+1): okf=False;break
            if not okf: continue
            m=max(cc[j]*cc[j+1] for j in range(4))
            if m<bestv: bestv=m; bestab=(a,b)
    if bestab is not None:
        # refine with Nelder-Mead minimizing maxP + penalty
        def obj(ab): return maxP(ab,K)+feasible_penalty(ab,K)*10
        res=minimize(obj,np.array(bestab),method='Nelder-Mead',
                     options=dict(xatol=1e-10,fatol=1e-12,maxiter=20000))
        if feasible_penalty(res.x,K)<1e-7:
            v=maxP(res.x,K)
            if v<bestv: bestv=v; bestab=tuple(res.x)
    if bestab is not None and bestv<best_overall[0]:
        best_overall=(bestv,K,bestab)
    if bestab is not None:
        cc=coords(*bestab,*K)
        flag="  <<< BELOW THR!" if bestv<thr-1e-9 else ""
        print(f"K={K}: min-max P = {bestv:.8f}  (margin {bestv-thr:+.8f}) at (a,b)=({bestab[0]:.5f},{bestab[1]:.5f}) coords={[round(x,4) for x in cc]}{flag}")

print(f"\nGLOBAL min-over-combos of min-max P = {best_overall[0]:.8f} at K={best_overall[1]} (a,b)={best_overall[2]}")
print(f"thr = {thr:.8f}")
print("=> window-4 (with cap) is", "TRUE" if best_overall[0]>=thr-1e-7 else "FALSE (!!!)")
