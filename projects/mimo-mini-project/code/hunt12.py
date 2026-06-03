#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hunt12.py — thorough feasible-parabolic-word search for X(q), restricted to small floors.
All periodic orbits of T_q in D are parabolic-word (trace-2) scale-free families (floors-fixed map
is linear => periodic point must be +1-eigenvector of monodromy). So minimizing X(q) over invariant
measures' essSup is (conjecturally, Jenkinson) the min over feasible parabolic words of the boundary
value. We search words over floors in [1..Kmax] up to length Pmax, find feasible ones (nonempty OPEN
scale window), report the min-X word and the full sorted list."""
import itertools, math, sys
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)
def Mmat(k,l): return np.array([[0.0,1.0],[-1.0,k*l]])
def monodromy(word,l):
    A=np.eye(2)
    for k in word: A=Mmat(k,l)@A
    return A
def canonical(word):
    return min(tuple(word[i:]+word[:i]) for i in range(len(word)))

def orbit_direction(word,l):
    p=len(word); M=monodromy(word,l)
    if abs(np.trace(M)-2.0)>1e-7: return None
    A=M-np.eye(2)
    _,sv,Vt=np.linalg.svd(A)
    if sv[-1]>1e-6: return None
    v01=Vt[-1]
    if v01[0]<0: v01=-v01
    v=[v01[0],v01[1]]
    for n in range(p-2): v.append(word[n]*l*v[n+1]-v[n])
    ap=word[p-2]*l*v[p-1]-v[p-2]; ap1=word[p-1]*l*ap-v[p-1]
    if abs(ap-v[0])>1e-6 or abs(ap1-v[1])>1e-6: return None
    if any(x<=1e-9 for x in v): return None
    return v

def svalid_range(word,v,l):
    p=len(word); s_lo,s_hi=0.0,math.inf; binding=None
    for n in range(p):
        vn,vn1,kn=v[n],v[(n+1)%p],word[n]
        r=vn/(l*vn1)
        if kn-r>1e-12:
            s_up=1.0/(l*vn1*(kn-r))
            if s_up<s_hi: s_hi=s_up
        denom=(kn+1-r)
        if denom<=1e-12: return None
        s_dn=1.0/(l*vn1*denom)
        if s_dn>s_lo: s_lo=s_dn; binding=('floor-jump',n)
    for n in range(p):
        thr=1.0/(v[n]+l*v[(n+1)%p])
        if thr>s_lo: s_lo=thr; binding=('triangle',n)
    if s_lo>=s_hi: return None
    return s_lo,s_hi,binding

def hunt(q,Pmax,Kmax,topN=8):
    l=lam(q); seen=set(); feas=[]
    for p in range(1,Pmax+1):
        for word in itertools.product(range(1,Kmax+1),repeat=p):
            c=canonical(list(word))
            if c in seen: continue
            seen.add(c)
            v=orbit_direction(list(c),l)
            if v is None: continue
            rng=svalid_range(list(c),v,l)
            if rng is None: continue
            s_lo,s_hi,binding=rng
            maxprod=max(v[n]*v[(n+1)%len(c)] for n in range(len(c)))
            Xc=s_lo*s_lo*maxprod
            feas.append((Xc,c,s_lo,s_hi,binding))
    feas.sort(key=lambda t:t[0])
    return l,feas[:topN],len(feas)

if __name__=="__main__":
    qs = [int(x) for x in sys.argv[1:]] or list(range(13,19))
    Kmax=2; Pmax=24
    for q in qs:
        l,top,nf=hunt(q,Pmax,Kmax)
        print(f"\nq={q} lam={l:.6f}  Kmax={Kmax} Pmax={Pmax}  #feasible={nf}")
        if not top: print("  NONE feasible"); continue
        for Xc,c,s_lo,s_hi,b in top:
            print(f"  X={Xc:.8f} word={c} window=({s_lo:.5f},{s_hi:.5f}) bind={b}")
