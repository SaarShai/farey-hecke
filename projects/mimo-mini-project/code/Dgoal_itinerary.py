#!/usr/bin/env python3
"""Mechanism: find the worst (longest) runs of P<1/lam^3 and print their full branch/digit
itinerary + coordinates, to reveal the proof's case structure. Also: is the run always
'entering the cusp branch q-2'? And what is min over orbit of P (does an orbit sustain P<=thr)?"""
import math, random
import numpy as np
random.seed(7)
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

for q in [5,6,7]:
    l=lam(q); w=ellipse_vecs(q,l); thr=1.0/l**3
    print(f"\n=== q={q}, thr=1/lam^3={thr:.6f}, branches i=2..{q-1}, cusp branch q-2={q-2} ===")
    best=0; bestrec=None
    for _ in range(200000):
        a=random.uniform(1e-4,1.0); blo=1-l*a
        b=random.uniform(max(blo,-1)+1e-7,1.0)
        if not in_Tq(a,b,l): continue
        rec=[]; cur=0; curseg=[]
        for n in range(30):
            if not in_Tq(a,b,l): break
            r=step(a,b,w,q,l)
            if r is None: break
            (na,nb),i,k=r; P=P_obs(a,b,i,w)
            below=P<thr-1e-11
            curseg.append((i,k,round(P,5)))
            if below: cur+=1
            else:
                if cur>best: best=cur; bestrec=curseg[-(cur+1):]
                cur=0
            a,b=na,nb
    print(f"  max run below = {best}")
    print(f"  worst segment (i,k,P), last entry is first >=thr: {bestrec}")
