#!/usr/bin/env python3
"""
GOAL F large-q: (a) transience of low-P middle-branch points; (b) min esssup P over orbits.
Efficient: branch lookup via the fact that L_i is unimodal; just linear scan but fewer steps.
"""
import math, random
import numpy as np
random.seed(3)

def build(q):
    L=2*math.cos(math.pi/q); x=[0.0]*(q+3)
    # x[k] stores x_{k-1}; we want x_{-1}=0,x_0=1,... use dict-like via offset 1
    X={-1:0.0,0:1.0}
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

def P(a,b,i,X): return a*(a*X[i]+b*X[i-1])/X[i-1]
def inT(a,b,L,e=1e-9): return (1e-12<a<=1+e and 1-L*a-e<b<=1+e)

print("=== (a) TRANSIENCE: iterate forward from each branch's min-P vertex (a=v=m/(1+c)) ===")
for q in [20,30]:
    L,X=build(q); thr=1/L**3
    print(f"  q={q}, thr={thr:.4f}")
    for i in range(8, q-2, max(1,(q-10)//4)):
        m=X[i-1]; c=X[i-2]
        a=m/(1+c)
        # vertex: u=L_{i-1}=1 -> b from L_{i-1}=a x_{i-1}+b x_{i-2}=1
        b=(1 - a*X[i-1])/X[i-2]
        if not inT(a,b,L): continue
        seq=[]; aa,bb=a,b; ok=True
        for n in range(40):
            r=step(aa,bb,X,q,L)
            if r is None: ok=False;break
            (na,nb),bi=r; seq.append(P(aa,bb,bi,X)); aa,bb=na,nb
            if not inT(aa,bb,L): ok=False;break
        if seq:
            rm=max(seq); first_above=next((n for n,p in enumerate(seq) if p>=thr),None)
            print(f"    branch i={i}: P0={seq[0]:.4f} runmax(40)={rm:.4f} ({'>=thr' if rm>=thr else 'BELOW thr whole 40!'}) "
                  f"first-step>=thr at n={first_above}")

print("\n=== (b) MIN esssup P over random orbits (transient dropped) ===")
for q in [20,30]:
    L,X=build(q); thr=1/L**3
    best=1e9; NS=3000; STEPS=600
    for _ in range(NS):
        a=random.uniform(1e-3,1.0); blo=1-L*a
        b=random.uniform(max(blo,-1)+1e-6,1.0)
        if not inT(a,b,L): continue
        mx=0;cnt=0;ok=True
        for n in range(STEPS):
            r=step(a,b,X,q,L)
            if r is None: ok=False;break
            (na,nb),bi=r
            if n>40: mx=max(mx,P(a,b,bi,X)); cnt+=1
            a,b=na,nb
            if not inT(a,b,L): ok=False;break
        if ok and cnt>300 and mx<best: best=mx
    print(f"  q={q}: thr={thr:.5f} min esssup over {NS} orbits = {best:.5f} ratio={best/thr:.4f} "
          f"{'**X<1/lam^3!**' if best<thr-1e-4 else '(>=thr: cusp may still win)'}")
