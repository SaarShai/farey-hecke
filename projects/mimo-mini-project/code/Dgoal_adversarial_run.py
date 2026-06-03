#!/usr/bin/env python3
"""Adversarial search for the max run of consecutive P<1/lam^3 on the GENUINE map.
Grid + edge-following + near-cusp + periodic-word transients. Report explicit witness."""
import math, itertools
import numpy as np

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
    ti=a*w[i][0]+b*w[i][1]
    return a*ti/w[i][1]
def in_Tq(a,b,l,eps=1e-9):
    return (a>1e-12 and a<=1+eps and 1-l*a-eps<b<=1+eps)

def maxrun_from(a,b,w,q,l,thr,steps=60):
    """run of consecutive P<thr starting at seed (only count the initial maximal run+track global)."""
    best=0; cur=0; bestseg=[]; seg=[]
    for n in range(steps):
        if not in_Tq(a,b,l): break
        r=step(a,b,w,q,l)
        if r is None: break
        (na,nb),i,k=r
        P=P_obs(a,b,i,w)
        if P<thr-1e-11:
            cur+=1; seg.append((round(a,6),round(b,6),i,k,round(P,6)))
            if cur>best: best=cur; bestseg=seg[:]
        else:
            cur=0; seg=[]
        a,b=na,nb
    return best,bestseg

for q in [5,6,7,8,10,13]:
    l=lam(q); w=ellipse_vecs(q,l); thr=1.0/l**3
    gmax=0; gseg=None
    # 1. dense grid
    NA=400
    for ia in range(1,NA):
        a=ia/NA
        blo=1-l*a
        NB=400
        for ib in range(NB+1):
            b=max(blo,-1.0)+ (1.0-max(blo,-1.0))*ib/NB
            if not in_Tq(a,b,l): continue
            r,seg=maxrun_from(a,b,w,q,l,thr,steps=40)
            if r>gmax: gmax=r; gseg=(a,b,seg)
    # 2. near-cusp vertex (a~1/l, b~0+) and near edges, very fine
    for a in np.linspace(1/l-0.05, min(1/l+0.3,1.0), 600):
        if a<=0: continue
        for b in list(np.linspace(1e-6, 0.05, 400)) + list(np.linspace(max(1-l*a,0)+1e-7, max(1-l*a,0)+0.05, 200)):
            if not in_Tq(a,b,l): continue
            r,seg=maxrun_from(a,b,w,q,l,thr,steps=50)
            if r>gmax: gmax=r; gseg=(a,b,seg)
    print(f"q={q}: thr={thr:.6f}  ADVERSARIAL maxrun={gmax}")
    if gseg:
        a0,b0,seg=gseg
        print(f"    witness seed=({a0:.6f},{b0:.6f}) seg(a,b,i,k,P)={seg[:6]}")
