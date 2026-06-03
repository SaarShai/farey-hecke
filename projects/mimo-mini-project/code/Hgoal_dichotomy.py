#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL H — confirm the elliptic/parabolic/hyperbolic dichotomy operationally:
 (1) second parabolic word (q-1,1)(q-3,0) [trace 2]: min-esssup vs thr (>=thr expected).
 (2) hyperbolic words (k1=0 or 4 in the family) ESCAPE: run genuine map from near their
     pseudo-fixed direction, count steps to leave Tq or exceed thr (expect O(1)).
 (3) confirm: along the actual longest run, the per-3-block monodromy trace == lam (rotation).
"""
import math
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)
def build(q):
    l=lam(q); x={-1:0.0,0:1.0}
    for i in range(1,q+3): x[i]=l*x[i-1]-x[i-2]
    return l,x
def ellipse_vecs(q,l):
    U=np.array([[l,-1.0],[1.0,0.0]]); w=[np.array([1.0,0.0])]
    for _ in range(q+3): w.append(U@w[-1])
    return w
def Mik(i,k,w,l):
    xi,yi=w[i]; xi1,yi1=w[i+1]
    return np.array([[xi,yi],[xi1+k*l*xi,yi1+k*l*yi]])
def eig1(M):
    A=M-np.eye(2); _,sv,Vt=np.linalg.svd(A)
    if sv[-1]>1e-7: return None
    v=Vt[-1]
    if v[0]<0: v=-v
    return v
def family(word,w,l):
    M=np.eye(2)
    for (i,k) in word: M=Mik(i,k,w,l)@M
    if abs(np.trace(M)-2.0)>1e-6: return None
    v0=eig1(M)
    if v0 is None: return None
    vs=[v0]
    for (i,k) in word[:-1]: vs.append(Mik(i,k,w,l)@vs[-1])
    if any(v[0]<=1e-9 for v in vs): return None
    return vs
def fwin(word,vs,w,q,l):
    s_lo=0.0;s_hi=math.inf;E=1e-12
    for n in range(len(word)):
        vx,vy=vs[n]; i,k=word[n]
        s_hi=min(s_hi,1.0/vx)
        if vy>E: s_hi=min(s_hi,1.0/vy)
        ed=vy+l*vx
        if ed>E: s_lo=max(s_lo,1.0/ed)
        dp=vx*w[i-1][0]+vy*w[i-1][1]; dc=vx*w[i][0]+vy*w[i][1]
        if dp>E: s_lo=max(s_lo,1.0/dp)
        if dc>E: s_hi=min(s_hi,1.0/dc)
        else: return None
        A=dc; B=vx*w[i+1][0]+vy*w[i+1][1]
        up=B+k*l*A
        if up>E: s_hi=min(s_hi,1.0/up)
        lo=B+(k+1)*l*A
        if lo>E: s_lo=max(s_lo,1.0/lo)
    if s_lo>=s_hi-1e-14: return None
    return s_lo,s_hi
def Phat(vn,i,w): return vn[0]*(vn[0]*w[i][0]+vn[1]*w[i][1])/w[i][1]

print("=== (1) second parabolic word (q-1,1)(q-3,0) [trace 2] : min-esssup vs thr ===")
for q in [16,20,30,50]:
    l,x=build(q); w=ellipse_vecs(q,l); thr=1/l**3
    word=[(q-1,1),(q-3,0)]
    vs=family(word,w,l)
    if vs is None:
        print(f"  q={q}: not a feasible parabolic family"); continue
    win=fwin(word,vs,w,q,l)
    if win is None:
        print(f"  q={q}: parabolic but empty scale window (infeasible)"); continue
    s_lo,s_hi=win
    Xc=s_lo*s_lo*max(Phat(vs[n],word[n][0],w) for n in range(len(word)))
    print(f"  q={q}: {word} s in ({s_lo:.5f},{s_hi:.5f}] min-esssup={Xc:.6f} thr={thr:.6f} "
          f"ratio={Xc/thr:.5f} {'<<<BELOW' if Xc<thr-1e-7 else 'OK(>=thr)'}")

print("\n=== (3) along longest run: per-3-block monodromy trace == lam? (universality) ===")
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
import random
for q in [16,20,30,40,50]:
    rng=random.Random(2024+q); l,x=build(q); thr=1/l**3
    best=0; bstate=None
    NS=20000 if q<=30 else 9000
    for _ in range(NS):
        a=rng.uniform(1e-3,1.0); b=rng.uniform(max(1-l*a,-1)+1e-6,1.0)
        if not inT(a,b,l): continue
        cur=0; st=[]
        for n in range(240):
            r=step(a,b,x,q,l)
            if r is None: break
            (na,nb),i,k=r; p=Pval(a,b,i,x)
            if p<thr-1e-11:
                cur+=1; st.append((i,k))
                if cur>best: best=cur; bstate=list(st)
            else: cur=0; st=[]
            a,b=na,nb
            if not inT(a,b,l): break
    # per-3-block trace from a steady middle block
    w=ellipse_vecs(q,l)
    if bstate and len(bstate)>=6:
        block=bstate[2:5]
        M=np.eye(2)
        for (i,k) in block: M=Mik(i,k,w,l)@M
        print(f"  q={q}: run={best} block{block} trace={np.trace(M):.5f} lam={l:.5f} "
              f"match={abs(np.trace(M)-l)<1e-3}")
    else:
        print(f"  q={q}: run={best} (short) itin={bstate}")
