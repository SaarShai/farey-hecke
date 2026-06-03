#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GOAL H — boundary q-scan: where does the SUSTAINED longest run stop being pure-scalar
(i=q-1) and start using branch q-3 (multi-branch W_q)?  Also: are sustained runs EVER using a
DEEP middle branch (i <= q-4), or only {q-1, q-3}?  (Needed for the characterization.)"""
import math, random

def build(q):
    lam=2*math.cos(math.pi/q); x={-1:0.0,0:1.0}
    for i in range(1,q+3): x[i]=lam*x[i-1]-x[i-2]
    return lam,x
def Lf(a,b,j,x): return a*x[j]+b*x[j-1]
def branch(a,b,x,q,eps=1e-9):
    for i in range(2,q):
        if Lf(a,b,i-1,x)>1-eps and Lf(a,b,i,x)<=1+eps: return i
    return None
def step(a,b,x,q,l):
    i=branch(a,b,x,q)
    if i is None: return None
    Li=Lf(a,b,i,x); Li1=Lf(a,b,i+1,x)
    if l*Li<=1e-12: return None
    k=math.floor((1-Li1)/(l*Li))
    return (Li,Li1+k*l*Li),i,k
def Pval(a,b,i,x): return a*Lf(a,b,i,x)/x[i-1]
def inT(a,b,l,e=1e-9): return (1e-12<a<=1+e) and (1-l*a-e<b<=1+e)

print("=== boundary scan: longest-run itinerary branch-set per q ===")
print("   (pure-scalar => {q-1}; multi-branch W_q => {q-1,q-3}; deep => has i<=q-4)")
for q in range(16,23):
    rng=random.Random(7*q+1); l,x=build(q); thr=1/l**3
    best=0; bset=None; bitin=None
    NS=25000
    for _ in range(NS):
        a=rng.uniform(1e-3,1.0); b=rng.uniform(max(1-l*a,-1)+1e-6,1.0)
        if not inT(a,b,l): continue
        cur=0; itin=[]
        for n in range(200):
            r=step(a,b,x,q,l)
            if r is None: break
            (na,nb),i,k=r; p=Pval(a,b,i,x)
            if p<thr-1e-11:
                cur+=1; itin.append(i)
                if cur>best: best=cur; bitin=list(itin)
            else: cur=0; itin=[]
            a,b=na,nb
            if not inT(a,b,l): break
    bset=sorted(set(bitin)) if bitin else []
    pure = (bset==[q-1])
    usesq3 = (q-3) in bset
    deep = any(i<=q-4 for i in bset)
    print(f"  q={q}: max-run={best} branch-set={bset} "
          f"{'PURE-SCALAR' if pure else ('multi{q-1,q-3}' if (set(bset)<= {q-1,q-3}) else 'DEEP!')}")

print("\n=== transience depth: for each below-thr branch i, steps-to-exit from its low-P vertex ===")
for q in [20,30]:
    l,x=build(q); thr=1/l**3
    print(f"  q={q} thr={thr:.5f}:")
    for i in range(max(2,q-8),q):
        m=x[i-1]; c=x[i-2]; minP=m/(1+c)**2
        if minP>=thr-1e-12: continue
        vert=m/(1+c); a=vert; v=vert; b=(v-a*x[i])/x[i-1]
        a2,b2=a,b+1e-7
        if not inT(a2,b2,l):
            print(f"     i={i}(minP={minP:.4f}): vertex not in T"); continue
        aa,bb=a2,b2; nbelow=0
        for n in range(12):
            r=step(aa,bb,x,q,l)
            if r is None: break
            (na,nb),bi,bk=r; p=Pval(aa,bb,bi,x)
            if p<thr-1e-11: nbelow+=1
            else: break
            aa,bb=na,nb
            if not inT(aa,bb,l): break
        tag = "scalar" if i==q-1 else ("q-3" if i==q-3 else ("cusp" if i==q-2 else "DEEP-mid"))
        print(f"     i={i:<3}({tag}, minP={minP:.4f}): consecutive-below from vertex = {nbelow}")
