#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hunt_necklace.py — EXHAUSTIVE feasible-parabolic-word search over an alphabet of floors, up to a
period bound L, using FKM necklace generation (each rotation-class once, no dedup set => low memory).
Reports minimal-X feasible parabolic word. Usage: hunt_necklace.py Kmax Lmax q1 q2 ..."""
import math, sys

def lam(q): return 2*math.cos(math.pi/q)
def mat_mul(A,B):
    a,b,c,d=A; e,f,g,h=B
    return (a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def monodromy(word,l):
    A=(1.0,0.0,0.0,1.0)
    for k in word: A=mat_mul((0.0,1.0,-1.0,k*l),A)
    return A

def orbit_dir(word,l,M):
    a,b,c,d=M; v0,v1=b,1.0-a
    if abs(v0)<1e-13 and abs(v1)<1e-13: return None
    if v0<0: v0,v1=-v0,-v1
    p=len(word); v=[v0,v1]
    for n in range(p-2): v.append(word[n]*l*v[n+1]-v[n])
    ap=word[p-2]*l*v[p-1]-v[p-2]; ap1=word[p-1]*l*ap-v[p-1]
    if abs(ap-v[0])>1e-7 or abs(ap1-v[1])>1e-7: return None
    if any(x<=1e-9 for x in v): return None
    return v

def svalid(word,v,l):
    p=len(word); s_lo,s_hi=0.0,math.inf; binding=None
    for n in range(p):
        vn,vn1,kn=v[n],v[(n+1)%p],word[n]; r=vn/(l*vn1)
        if kn-r>1e-12: s_hi=min(s_hi,1.0/(l*vn1*(kn-r)))
        denom=kn+1-r
        if denom<=1e-12: return None
        s_dn=1.0/(l*vn1*denom)
        if s_dn>s_lo: s_lo=s_dn; binding=('floor-jump',n)
    for n in range(p):
        thr=1.0/(v[n]+l*v[(n+1)%p])
        if thr>s_lo: s_lo=thr; binding=('triangle',n)
    if s_lo>=s_hi*(1-1e-12): return None
    return s_lo,s_hi,binding

def necklaces(n,k):
    a=[0]*(n+1)
    def gen(t,p):
        if t>n:
            if n%p==0: yield tuple(a[1:n+1])
        else:
            a[t]=a[t-p]
            yield from gen(t+1,p)
            for j in range(a[t-p]+1,k):
                a[t]=j; yield from gen(t+1,t)
    yield from gen(1,1)

def hunt(q,Kmax,Lmax,topN=12):
    l=lam(q); feas=[]; ncheck=0
    for n in range(1,Lmax+1):
        for neck in necklaces(n,Kmax):
            word=tuple(x+1 for x in neck)   # 0..Kmax-1 -> 1..Kmax
            ncheck+=1
            M=monodromy(word,l)
            if abs(M[0]+M[3]-2.0)>1e-7: continue
            v=orbit_dir(word,l,M)
            if v is None: continue
            rng=svalid(list(word),v,l)
            if rng is None: continue
            s_lo,s_hi,b=rng
            mxp=max(v[i]*v[(i+1)%len(word)] for i in range(len(word)))
            feas.append((s_lo*s_lo*mxp,word,s_lo,s_hi,b))
    feas.sort(key=lambda t:t[0])
    return l,feas[:topN],len(feas),ncheck

if __name__=="__main__":
    Kmax=int(sys.argv[1]); Lmax=int(sys.argv[2]); qs=[int(x) for x in sys.argv[3:]]
    for q in qs:
        l,top,nf,nc=hunt(q,Kmax,Lmax)
        print(f"\nq={q} lam={l:.6f} Kmax={Kmax} Lmax={Lmax} #feasible={nf} #checked={nc}")
        for Xc,c,s_lo,s_hi,b in top:
            print(f"  X={Xc:.8f} P={len(c):>2} word={c} window=({s_lo:.5f},{s_hi:.5f}) bind={b}")
