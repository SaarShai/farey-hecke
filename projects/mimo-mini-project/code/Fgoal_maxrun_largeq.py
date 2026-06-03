#!/usr/bin/env python3
"""
GOAL F: (1) pin exact q-range where per-branch envelope (B) / scalar reduction holds.
        (2) adversarial max-run of consecutive P<1/lam^3 at large q -- does it stay finite?
           (finite => no sustained orbit => esssup>=1/lam^3 => headline X=1/lam^3 survives,
            but via genuine multi-branch dynamics, NOT scalar reduction.)
        (3) confirm cusp orbit P->1/lam^3 still feasible at large q.
"""
import math, random
import numpy as np
random.seed(5)

def build(q):
    L=2*math.cos(math.pi/q); X={-1:0.0,0:1.0}
    for i in range(1,q+2): X[i]=L*X[i-1]-X[i-2]
    return L,X
def branch(a,b,X,q,eps=1e-9):
    for i in range(2,q):
        if a*X[i-1]+b*X[i-2]>1-eps and a*X[i]+b*X[i-1]<=1+eps: return i
    return None
def step(a,b,X,q,L):
    i=branch(a,b,X,q)
    if i is None: return None
    Li=a*X[i]+b*X[i-1]; Li1=a*X[i+1]+b*X[i]
    if L*Li<=0: return None
    k=math.floor((1-Li1)/(L*Li))
    return (Li, Li1+k*L*Li), i
def Pf(a,b,i,X): return a*(a*X[i]+b*X[i-1])/X[i-1]
def inT(a,b,L,e=1e-9): return (1e-12<a<=1+e and 1-L*a-e<b<=1+e)

print("=== (1) exact q-range of reduction (P<thr only on scalar branch q-1) ===")
for q in range(13,19):
    L,X=build(q); thr=1/L**3
    # static: any non-scalar branch with a point P<thr?
    fail=None
    for i in range(2,q-1):
        m=X[i-1]; c=X[i-2]; minP=m/(1+c)**2  # vertex min (valid since a=v<=1)
        if minP<thr-1e-9: fail=(i,round(minP,5)); break
    print(f"  q={q}: thr={thr:.5f} reduction {'HOLDS' if fail is None else f'FAILS at branch {fail}'}")

print("\n=== (2) adversarial max-run of P<thr (random orbits) ===")
for q in [10,13,15,16,20,30,50,80]:
    L,X=build(q); thr=1/L**3
    best=0; NS=30000; STEPS=60
    for _ in range(NS):
        a=random.uniform(1e-4,1.0); blo=1-L*a
        b=random.uniform(max(blo,-1)+1e-7,1.0)
        if not inT(a,b,L): continue
        cur=0
        for n in range(STEPS):
            r=step(a,b,X,q,L)
            if r is None: break
            (na,nb),bi=r; p=Pf(a,b,bi,X)
            if p<thr-1e-11:
                cur+=1; best=max(best,cur)
            else: cur=0
            a,b=na,nb
            if not inT(a,b,L): break
    print(f"  q={q}: thr={thr:.5f} max-run(P<thr)={best}")

print("\n=== (3) cusp orbit [(q-2,0)] : P at (s,0), s->1/lam ; value s^2/lam -> 1/lam^3 ===")
for q in [16,30,50,80]:
    L,X=build(q); thr=1/L**3
    s=1/L+1e-6  # just inside
    Pcusp=s*s/L
    print(f"  q={q}: 1/lam={1/L:.5f} cusp P(s=1/lam+eps)={Pcusp:.6f}  1/lam^3={thr:.6f}  diff={Pcusp-thr:.2e}")
