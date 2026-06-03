#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL H — THE rotation mechanism.  Hypothesis: every sustained sub-thr run is conjugate to a
rotation by pi/q (monodromy trace = lam = 2cos(pi/q)), so the product observable oscillates and
MUST exceed thr within a bounded number of steps => no infinite sub-thr orbit => (C').

Tests:
 (1) For longest runs at several q, accumulate the step-matrix product M_run; report trace.
     Also report trace of the running product after each step (does it stay |.|<2, elliptic?).
 (2) Conserved-form test: does the run preserve a quadratic form ~ E=c^2+c'^2-lam c c'?
     Track E_n=c_n^2+c_{n+1}^2-lam c_n c_{n+1}; report drift.
 (3) Extract recurring period-3-ish word, compute its monodromy trace; is it == lam universally?
 (4) Rotation-number estimate: total angle turned over the run / steps ~ theta=pi/q ?
"""
import math, random
import numpy as np

def build(q):
    lam=2*math.cos(math.pi/q); x={-1:0.0,0:1.0}
    for i in range(1,q+3): x[i]=lam*x[i-1]-x[i-2]
    return lam,x
def Lf(a,b,j,x): return a*x[j]+b*x[j-1]
def branch(a,b,x,q,eps=1e-9):
    for i in range(2,q):
        if Lf(a,b,i-1,x)>1-eps and Lf(a,b,i,x)<=1+eps: return i
    return None
def Mik(i,k,x,lam):
    xi=x[i]; yi=x[i-1]; xi1=x[i+1]; yi1=x[i]
    return np.array([[xi,yi],[xi1+k*lam*xi, yi1+k*lam*yi]])
def step(a,b,x,q,lam):
    i=branch(a,b,x,q)
    if i is None: return None
    Li=Lf(a,b,i,x); Li1=Lf(a,b,i+1,x)
    if lam*Li<=1e-12: return None
    k=math.floor((1-Li1)/(lam*Li))
    return (Li, Li1+k*lam*Li), i, k
def Pval(a,b,i,x): return a*Lf(a,b,i,x)/x[i-1]
def inT(a,b,lam,e=1e-9): return (1e-12<a<=1+e) and (1-lam*a-e<b<=1+e)

def longest_run(q, NS=40000, STEPS=220, seed=3):
    rng=random.Random(seed); lam,x=build(q); thr=1/lam**3
    best=0; best_state=None
    for _ in range(NS):
        a=rng.uniform(1e-3,1.0); b=rng.uniform(max(1-lam*a,-1)+1e-6,1.0)
        if not inT(a,b,lam): continue
        cur=0; states=[]  # (a,b,i,k,P)
        for n in range(STEPS):
            r=step(a,b,x,q,lam)
            if r is None: break
            (na,nb),i,k=r; p=Pval(a,b,i,x)
            if p<thr-1e-11:
                cur+=1; states.append((a,b,i,k,p))
                if cur>best: best=cur; best_state=list(states)
            else: cur=0; states=[]
            a,b=na,nb
            if not inT(a,b,lam): break
    return best,best_state,lam,x,thr

print("=== rotation mechanism along longest sub-thr runs ===")
for q in [16,20,30,40,50]:
    run,states,lam,x,thr=longest_run(q)
    if not states:
        print(f"  q={q}: no run"); continue
    # (1) monodromy product over the run
    M=np.eye(2); traces=[]
    Es=[]
    for (a,b,i,k,p) in states:
        M=Mik(i,k,x,lam)@M
        traces.append(round(np.trace(M),4))
    # E along run (first coords)
    cs=[s[0] for s in states]+[ Lf(states[-1][0],states[-1][1],states[-1][2],x) ]
    for n in range(len(cs)-1):
        Es.append(round(cs[n]**2+cs[n+1]**2-lam*cs[n]*cs[n+1],6))
    # (3) recurring per-3 word trace (use the steady middle of the run)
    mid=states[1:1+3] if len(states)>=4 else states
    Mw=np.eye(2)
    for (a,b,i,k,p) in mid: Mw=Mik(i,k,x,lam)@Mw
    trw=np.trace(Mw)
    iks=[(s[2],s[3]) for s in states]
    print(f"  q={q}: run={run} thr={thr:.5f}  per-3-word {[ (s[2],s[3]) for s in mid]} trace={trw:.5f} (lam={lam:.5f})")
    print(f"        E along run (should be ~const if rotation-on-ellipse): {Es}")
    print(f"        cumulative-monodromy traces: {traces}")
    print(f"        full itinerary (i,k): {iks}")

print("\n=== universality: trace of EVERY observed maximal recurring word vs lam ===")
print("    (does trace == lam = 2cos(pi/q) for all sustained words?)")
