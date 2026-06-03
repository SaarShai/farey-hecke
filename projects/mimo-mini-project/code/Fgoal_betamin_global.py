#!/usr/bin/env python3
"""
GOAL F task: is the AVERAGING (sub-action / Mañé) route globally dead?
beta_min = inf_mu int P dmu = min over orbits of time-average P.
If beta_min < 1/lam^3 for q, then no sub-action calibrated at 1/lam^3 (Mañé) -> averaging dead.
q=5 known: beta_min<1/lam^3 (scalar word (1,1,2), avg 0.186). Test q=5..14 on the GENUINE map.
Method: many random long genuine orbits, track min time-average of P (after transient).
Also short-period exhaustive on the scalar branch for a clean witness.
"""
import math, random
random.seed(9)
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

print("Genuine-map min time-average of P vs 1/lam^3  (beta_min < thr  =>  averaging route DEAD):")
for q in [5,6,7,8,9,10,12,14]:
    L,X=build(q); thr=1/L**3
    best=1e9; NS=6000; STEPS=2500
    for _ in range(NS):
        a=random.uniform(1e-4,1.0); blo=1-L*a; b=random.uniform(max(blo,-1)+1e-7,1.0)
        if not inT(a,b,L): continue
        s=0.0;cnt=0;ok=True
        for n in range(STEPS):
            r=step(a,b,X,q,L)
            if r is None: ok=False;break
            (na,nb),bi=r
            if n>40: s+=Pf(a,b,bi,X); cnt+=1
            a,b=na,nb
            if not inT(a,b,L): ok=False;break
        if ok and cnt>STEPS//2:
            avg=s/cnt
            if avg<best: best=avg
    print(f"  q={q}: 1/lam^3={thr:.6f}  min time-avg(P)={best:.6f}  ratio={best/thr:.4f}  "
          f"{'DEAD (avg<thr)' if best<thr-1e-4 else 'avg>=thr (sub-action not excluded this way)'}")
