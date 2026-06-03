#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hunt_sparse.py — find feasible parabolic optimizer words via SPARSE multi-defect enumeration.
A word = blocks of 1's separated by 'defect' entries m_i>=2:  1^{a_0} m_0 1^{a_1} m_1 ... .
Single-defect (1^{p-1},m) is parabolic iff m-1 = tan(p*pi/2q)*tan(pi/q) -> for m=2 only p=q-2,
which is infeasible for q>=12. So large q needs t>=2 defects. We enumerate t=1,2,3 defects with
small block lengths and defect values, check trace 2 + positive orbit + nonempty OPEN scale window,
and report the minimal-X feasible word. Usage: hunt_sparse.py q1 q2 ..."""
import itertools, math, sys

def lam(q): return 2*math.cos(math.pi/q)
def mat_mul(A,B):
    a,b,c,d=A; e,f,g,h=B
    return (a*e+b*g, a*f+b*h, c*e+d*g, c*f+d*h)
def monodromy(word,l):
    A=(1.0,0.0,0.0,1.0)
    for k in word: A=mat_mul((0.0,1.0,-1.0,k*l),A)
    return A
def canonical(word): return min(tuple(word[i:]+word[:i]) for i in range(len(word)))

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
        if kn-r>1e-12:
            s_up=1.0/(l*vn1*(kn-r));  s_hi=min(s_hi,s_up)
        denom=kn+1-r
        if denom<=1e-12: return None
        s_dn=1.0/(l*vn1*denom)
        if s_dn>s_lo: s_lo=s_dn; binding=('floor-jump',n)
    for n in range(p):
        thr=1.0/(v[n]+l*v[(n+1)%p])
        if thr>s_lo: s_lo=thr; binding=('triangle',n)
    if s_lo>=s_hi*(1-1e-12): return None
    return s_lo,s_hi,binding

def gen_sparse(q, max_defects=3, Mmax=4, Pmax=None):
    """Yield candidate words (tuples) built from blocks 1^a then defect m, t defects total."""
    if Pmax is None: Pmax=2*q+2
    # t defects: choose block lengths a_0..a_{t-1}>=0 and defect values m_0..m_{t-1} in 2..Mmax
    for t in range(1, max_defects+1):
        # bound each block length so total <= Pmax
        for blocks in itertools.product(range(0, Pmax), repeat=t):
            p=sum(blocks)+t
            if p<1 or p>Pmax: continue
            for ms in itertools.product(range(2,Mmax+1), repeat=t):
                word=[]
                for i in range(t):
                    word += [1]*blocks[i] + [ms[i]]
                yield tuple(word)

def hunt(q, max_defects=3, Mmax=4, topN=12):
    l=lam(q); seen=set(); feas=[]
    for word in gen_sparse(q, max_defects, Mmax):
        c=canonical(list(word))
        if c in seen: continue
        seen.add(c)
        M=monodromy(c,l)
        if abs(M[0]+M[3]-2.0)>1e-7: continue
        v=orbit_dir(c,l,M)
        if v is None: continue
        rng=svalid(list(c),v,l)
        if rng is None: continue
        s_lo,s_hi,b=rng
        maxprod=max(v[n]*v[(n+1)%len(c)] for n in range(len(c)))
        feas.append((s_lo*s_lo*maxprod,c,s_lo,s_hi,b))
    feas.sort(key=lambda t:t[0])
    return l,feas[:topN],len(feas)

if __name__=="__main__":
    qs=[int(x) for x in sys.argv[1:]] or list(range(4,21))
    for q in qs:
        l,top,nf=hunt(q)
        print(f"\nq={q} lam={l:.6f} #feasible={nf}")
        for Xc,c,s_lo,s_hi,b in top:
            print(f"  X={Xc:.8f} P={len(c):>2} word={c} window=({s_lo:.5f},{s_hi:.5f}) bind={b}")
