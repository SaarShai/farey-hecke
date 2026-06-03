#!/usr/bin/env python3
"""CORRECTED truth test. Genuine branch-4 orbit point (x,y) satisfies BOTH:
  (branch-4 guard)  x + phi*y > 1
  (T5 lower edge)   phi*x + y > 1     [= Taha 1-phi*x < y, the MISSING constraint]
plus cap x,y in (0,1]. Require both edges on all consecutive pairs.
Per integer floor combo, minimize max(P0..P3); window-4 holds iff global min-max >= thr."""
import math, itertools
import numpy as np
from scipy.optimize import minimize
phi=(1+math.sqrt(5))/2; l=phi; thr=1.0/phi**3
print(f"phi={phi:.10f} thr={thr:.10f}")
def coords(a,b,K0,K1,K2):
    c=K0*l*b-a; d=K1*l*c-b; e=K2*l*d-c; return (a,b,c,d,e)
def edges_ok(cc):
    for j in range(4):
        x,y=cc[j],cc[j+1]
        if not (x+l*y>1 and l*x+y>1): return False
    return True
def floors_ok(cc,K):
    for (ci,cj,K_) in [(cc[0],cc[1],K[0]),(cc[1],cc[2],K[1]),(cc[2],cc[3],K[2])]:
        if cj<=0: return False
        v=(1+ci)/(l*cj)
        if not (K_<=v<K_+1): return False
    return True

best=(9,None,None)
for K in itertools.product(range(1,5),range(1,5),range(1,5)):
    bv=9; bab=None
    for ia in range(1,1401):
        a=ia/1400.0
        for ib in range(1,901):
            b=ib/900.0
            cc=coords(a,b,*K)
            if any(x<=1e-9 for x in cc): continue
            if any(x>1+1e-12 for x in cc): continue
            if not edges_ok(cc): continue
            if not floors_ok(cc,K): continue
            m=max(cc[j]*cc[j+1] for j in range(4))
            if m<bv: bv=m; bab=(a,b)
    if bab is None: continue
    if bv<best[0]: best=(bv,K,bab)
    cc=coords(*bab,*K)
    flag="  <<< BELOW THR!!!" if bv<thr-1e-9 else ""
    print(f"K={K}: min-max={bv:.8f} (margin {bv-thr:+.8f}) (a,b)=({bab[0]:.5f},{bab[1]:.5f}) coords={[round(x,4) for x in cc]}{flag}")
print(f"\nGLOBAL min-max = {best[0]:.8f} at K={best[1]} (a,b)={best[2]}, thr={thr:.8f}")
print("=> window-4 with BOTH edges is", "TRUE" if best[0]>=thr-1e-7 else "FALSE(!!!)")
