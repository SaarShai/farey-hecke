#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GOAL H — THE critical question: are longest sub-thr runs pure-scalar (i=q-1) or multi-branch?
Plus: per-branch min-P band, and transience (steps-to-exit from a low-P middle-branch vertex)."""
import math, random

def build(q):
    lam = 2*math.cos(math.pi/q)
    x = {-1: 0.0, 0: 1.0}
    for i in range(1, q+3): x[i] = lam*x[i-1] - x[i-2]
    return lam, x
def Lf(a,b,j,x): return a*x[j]+b*x[j-1]
def branch(a,b,x,q,eps=1e-9):
    for i in range(2,q):
        if Lf(a,b,i-1,x)>1-eps and Lf(a,b,i,x)<=1+eps: return i
    return None
def step(a,b,x,q,lam):
    i=branch(a,b,x,q)
    if i is None: return None
    Li=Lf(a,b,i,x); Li1=Lf(a,b,i+1,x)
    if lam*Li<=1e-12: return None
    k=math.floor((1-Li1)/(lam*Li))
    return (Li, Li1+k*lam*Li), i, k
def Pval(a,b,i,x): return a*Lf(a,b,i,x)/x[i-1]
def inT(a,b,lam,e=1e-9): return (1e-12<a<=1+e) and (1-lam*a-e<b<=1+e)

print("=== per-branch min-P band (which branches dip below thr) ===")
for q in [16,20,30,50]:
    lam,x=build(q); thr=1/lam**3
    below=[]
    for i in range(2,q):
        m=x[i-1]; c=x[i-2]; minP=m/(1+c)**2; vert=m/(1+c)
        if minP<thr-1e-12:
            tag = "SCALAR" if i==q-1 else ("CUSP" if i==q-2 else "mid")
            below.append((i,round(minP,5),tag,round(vert,4)))
    mids=[t[0] for t in below if t[2]=="mid"]
    print(f"  q={q} thr={thr:.5f}: below={below}")
    if mids: print(f"        mid band i in [{min(mids)},{max(mids)}], scalar={q-1}, cusp={q-2}")

print("\n=== longest sub-thr run: itinerary (pure scalar i=q-1, or multi-branch?) ===")
for q in [16,20,30]:
    rng=random.Random(100+q); lam,x=build(q); thr=1/lam**3
    best=0; best_itin=None
    NS=15000 if q<30 else 8000
    for _ in range(NS):
        a=rng.uniform(1e-3,1.0); b=rng.uniform(max(1-lam*a,-1)+1e-6,1.0)
        if not inT(a,b,lam): continue
        cur=0; itin=[]
        for n in range(150):
            r=step(a,b,x,q,lam)
            if r is None: break
            (na,nb),i,k=r; p=Pval(a,b,i,x)
            if p<thr-1e-11:
                cur+=1; itin.append((i,k))
                if cur>best: best=cur; best_itin=list(itin)
            else: cur=0; itin=[]
            a,b=na,nb
            if not inT(a,b,lam): break
    iseq=[t[0] for t in best_itin] if best_itin else []
    kseq=[t[1] for t in best_itin] if best_itin else []
    allscalar = all(i==q-1 for i in iseq)
    print(f"  q={q}: max-run={best} (q/3={q/3:.1f}) pure-scalar={allscalar}")
    print(f"        i={iseq}")
    print(f"        k={kseq}")

print("\n=== transience: from middle-branch low-P vertex, steps until P>=thr ===")
for q in [16,20,30]:
    lam,x=build(q); thr=1/lam**3
    # pick the worst middle branch (min minP among mids)
    worst=None
    for i in range(2,q-1):
        m=x[i-1]; c=x[i-2]; minP=m/(1+c)**2
        if minP<thr-1e-12 and (worst is None or minP<worst[1]):
            worst=(i,minP,m,c)
    if worst is None:
        print(f"  q={q}: no middle branch below thr"); continue
    i,minP,m,c=worst
    # vertex a=v=m/(1+c). reconstruct (a,b): a=vert, v=L_i=a x_i+b x_{i-1} => b=(v-a x_i)/x_{i-1}
    vert=m/(1+c); a=vert; v=vert
    b=(v-a*x[i])/x[i-1]
    # nudge just inside the open constraints
    a2=a; b2=b+1e-7
    print(f"  q={q} worst mid branch i={i} minP={minP:.5f}<thr={thr:.5f} vertex(a,b)=({a:.5f},{b:.5f}) inT={inT(a2,b2,lam)}")
    aa,bb=a2,b2; seq=[]
    for n in range(8):
        r=step(aa,bb,x,q,lam)
        if r is None: seq.append("ESC"); break
        (na,nb),bi,bk=r; p=Pval(aa,bb,bi,x)
        seq.append((bi,round(p,5)))
        aa,bb=na,nb
        if not inT(aa,bb,lam): seq.append("OUT"); break
    print(f"        forward (branch,P): {seq}")
