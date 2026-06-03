#!/usr/bin/env python3
"""Per-branch behaviour of P vs 1/lam^3: which branches ever have P<thr, and min P per branch.
If below-threshold steps are confined to the scalar branch i=q-1, the run-bound reduces to the
3-term scalar recurrence (existing Lean machinery)."""
import math, random
import numpy as np
random.seed(3)
def lam(q): return 2*math.cos(math.pi/q)
def ellipse_vecs(q,l):
    U=np.array([[l,-1.0],[1.0,0.0]]); w=[np.array([1.0,0.0])]
    for _ in range(q+3): w.append(U@w[-1])
    return w
def branch_of(a,b,w,q,eps=1e-9):
    for i in range(2,q):
        t1=a*w[i-1][0]+b*w[i-1][1]; ti=a*w[i][0]+b*w[i][1]
        if t1>1-eps and ti<=1+eps: return i
    return None
def step(a,b,w,q,l):
    i=branch_of(a,b,w,q)
    if i is None: return None
    ti=a*w[i][0]+b*w[i][1]; ti1=a*w[i+1][0]+b*w[i+1][1]
    k=math.floor((1-ti1)/(l*ti))
    return (ti, ti1+k*l*ti), i, k
def P_obs(a,b,i,w):
    ti=a*w[i][0]+b*w[i][1]; return a*ti/w[i][1]
def in_Tq(a,b,l,eps=1e-9):
    return (a>1e-12 and a<=1+eps and 1-l*a-eps<b<=1+eps)

for q in [5,6,7,8]:
    l=lam(q); w=ellipse_vecs(q,l); thr=1.0/l**3
    minP={i:1e9 for i in range(2,q)}
    below={i:0 for i in range(2,q)}
    tot={i:0 for i in range(2,q)}
    for _ in range(40000):
        a=random.uniform(1e-4,1.0); blo=1-l*a
        b=random.uniform(max(blo,-1)+1e-7,1.0)
        if not in_Tq(a,b,l): continue
        for n in range(300):
            if not in_Tq(a,b,l): break
            r=step(a,b,w,q,l)
            if r is None: break
            (na,nb),i,k=r; P=P_obs(a,b,i,w)
            tot[i]+=1; minP[i]=min(minP[i],P)
            if P<thr-1e-11: below[i]+=1
            a,b=na,nb
    print(f"q={q} thr={thr:.5f}:")
    for i in range(2,q):
        tag=" <-- SCALAR (q-1)" if i==q-1 else (" <-- CUSP (q-2)" if i==q-2 else "")
        frac = below[i]/tot[i] if tot[i] else 0
        print(f"   branch i={i}: minP={minP[i]:.6f}  P<thr frac={frac:.4f}  (n={tot[i]}){tag}")
