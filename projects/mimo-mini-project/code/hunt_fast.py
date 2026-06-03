#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hunt_fast.py — fast pure-python parabolic-word search for X(q). 2x2 matmul in tuples (no numpy
overhead). Finds feasible parabolic words (trace 2, positive orbit, nonempty OPEN scale window),
reports min-X word + sorted list. Usage: hunt_fast.py Kmax Pmax q1 q2 ..."""
import itertools, math, sys

def lam(q): return 2*math.cos(math.pi/q)

def mat_mul(A, B):
    a,b,c,d = A; e,f,g,h = B
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)

def monodromy(word, l):
    A = (1.0,0.0,0.0,1.0)
    for k in word:
        A = mat_mul((0.0,1.0,-1.0,k*l), A)   # M(k) @ A,  apply k_0 first
    return A

def canonical(word):
    return min(tuple(word[i:]+word[:i]) for i in range(len(word)))

def orbit_dir(word, l, M):
    # M has trace ~2; +1 eigenvector of (M-I): (M01, 1-M00) (row0 of M-I: (M00-1)v0+M01 v1=0)
    a,b,c,d = M
    v0, v1 = b, 1.0-a
    if abs(v0) < 1e-14 and abs(v1) < 1e-14:
        return None
    if v0 < 0: v0,v1 = -v0,-v1
    p = len(word); v = [v0, v1]
    for n in range(p-2):
        v.append(word[n]*l*v[n+1]-v[n])
    # periodicity
    ap  = word[p-2]*l*v[p-1]-v[p-2]
    ap1 = word[p-1]*l*ap   -v[p-1]
    if abs(ap-v[0])>1e-7 or abs(ap1-v[1])>1e-7: return None
    if any(x<=1e-9 for x in v): return None
    return v

def svalid(word, v, l):
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
    if s_lo>=s_hi*(1-1e-12): return None     # require strictly nonempty OPEN window
    return s_lo,s_hi,binding

def hunt(q, Kmax, Pmax, topN=10):
    l=lam(q); seen=set(); feas=[]
    for p in range(1,Pmax+1):
        for word in itertools.product(range(1,Kmax+1),repeat=p):
            c=canonical(list(word))
            if c in seen: continue
            seen.add(c)
            M=monodromy(c,l)
            if abs(M[0]+M[3]-2.0)>1e-7: continue
            v=orbit_dir(c,l,M)
            if v is None: continue
            rng=svalid(list(c),v,l)
            if rng is None: continue
            s_lo,s_hi,binding=rng
            maxprod=max(v[n]*v[(n+1)%len(c)] for n in range(len(c)))
            feas.append((s_lo*s_lo*maxprod, c, s_lo, s_hi, binding))
    feas.sort(key=lambda t:t[0])
    return l, feas[:topN], len(feas)

if __name__=="__main__":
    Kmax=int(sys.argv[1]); Pmax=int(sys.argv[2]); qs=[int(x) for x in sys.argv[3:]]
    for q in qs:
        l,top,nf=hunt(q,Kmax,Pmax)
        print(f"\nq={q} lam={l:.6f} Kmax={Kmax} Pmax={Pmax} #feasible={nf}")
        for Xc,c,s_lo,s_hi,b in top:
            print(f"  X={Xc:.8f} P={len(c):>2} word={c} window=({s_lo:.5f},{s_hi:.5f}) bind={b}")
