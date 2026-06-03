#!/usr/bin/env python3
"""
GOAL F — CRITICAL: does X_Omega(q)=1/lam^3 survive for LARGE q?
The per-branch envelope (B) FAILS for q>=16 (middle branches have P<1/lam^3 statically).
Question: can genuine ORBITS sustain esssup P < 1/lam^3 ? If yes, X_Omega(q) < 1/lam^3 and
the headline is FALSE for large q. If no (every orbit forced to hit P>=1/lam^3 infinitely
often -> esssup>=1/lam^3), the headline survives but the REDUCTION proof strategy is dead.
"""
import math, random
import numpy as np
random.seed(20)

def build(q):
    L=2*math.cos(math.pi/q); x={-1:0.,0:1.}
    for i in range(1,q+2): x[i]=L*x[i-1]-x[i-2]
    return L,x

def branch(a,b,x,q,eps=1e-9):
    for i in range(2,q):
        if a*x[i-1]+b*x[i-2]>1-eps and a*x[i]+b*x[i-1]<=1+eps: return i
    return None

def step(a,b,x,q,L):
    i=branch(a,b,x,q)
    if i is None: return None
    Li=a*x[i]+b*x[i-1]; Li1=a*x[i+1]+b*x[i]
    k=math.floor((1-Li1)/(L*Li))
    return (Li, Li1+k*L*Li), i, k

def Pobs(a,b,i,x):
    return a*(a*x[i]+b*x[i-1])/x[i-1]

def in_T(a,b,L,eps=1e-9):
    return (1e-12<a<=1+eps and 1-L*a-eps<b<=1+eps)

for q in [10,20,30,50]:
    L,x=build(q); thr=1/L**3
    NS=20000; STEPS=1500
    best_max=1e9; best_seed=None
    # also: over a long generic orbit, what fraction has P<thr, and running-max
    for _ in range(NS):
        a=random.uniform(1e-4,1.0); blo=1-L*a
        b=random.uniform(max(blo,-1)+1e-7,1.0)
        if not in_T(a,b,L): continue
        mx=0.0; ok=True; cnt=0
        for n in range(STEPS):
            r=step(a,b,x,q,L)
            if r is None: ok=False; break
            (na,nb),i,k=r
            P=Pobs(a,b,i,x)
            if n>50:  # after transient
                mx=max(mx,P); cnt+=1
            a,b=na,nb
            if not in_T(a,b,L): ok=False; break
        if ok and cnt>500 and mx<best_max:
            best_max=mx; best_seed=(round(a,4),round(b,4))
    print(f"q={q}: 1/lam^3={thr:.5f}  min over {NS} orbits of (esssup P after transient) = {best_max:.5f}  "
          f"ratio={best_max/thr:.4f}  {'**BELOW thr -> X<1/lam^3**' if best_max<thr-1e-4 else 'all orbits hit >=thr'}")
