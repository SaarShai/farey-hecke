#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G4_hecke_farey_v2.py  (goal #7) — correct generator.

G_4 = <S, T>, S(z)=-1/z, T(z)=z+lam (lam=sqrt2). Cusps = orbit of oo, a/c with a,c in Z[sqrt2].
Denominator c changes ONLY under S (c -> a); T fixes c and shifts value by lam. So canonicalize
every cusp into the strip value in [0,lam) by T-reduction, then expand by S only; bound by Galois
height H(c)=max(|c|,|c'|) <= Q (finite by Northcott). This yields all G_4-Farey points in [0,lam)
with height-bounded denominator.

Then: sort by value, take denominators |c| (real embedding), form P_n=|c_n||c_{n+1}|/Q^2, and test
whether X(4)=sqrt2/8 acts as the cluster floor on REAL points -- and which window length.
"""
import math
S2=math.sqrt(2.0)
def val(z): return z[0]+z[1]*S2
def conj(z): return (z[0],-z[1])
def hgt(z): return max(abs(val(z)),abs(val(conj(z))))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def neg(a): return (-a[0],-a[1])
def mul(a,b): return (a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0])
LAM=(0,1); ONE=(1,0); ZERO=(0,0)

def canon(ac):
    """T-reduce so value in [0,lam); also fix sign of c so val(c)>0."""
    a,c=ac
    if val(c)<0: a,c=neg(a),neg(c)
    if val(c)==0: return (a,c)
    # number of lam-steps to subtract: k = floor( (a/c)/lam )
    k=math.floor((val(a)/val(c))/S2)
    a=sub(a, mul((0,k), c))   # a -= k*lam*c
    return (a,c)

def applyS(ac):
    a,c=ac; return (neg(c),a)

def generate(Q,max_nodes=2000000):
    seen=set()
    out={}
    # seed: 0/1 and 1/0(oo) and 1/lam etc come out of S-orbit; start from 0/1 and oo
    start=[canon((ZERO,ONE)), (ONE,ZERO)]
    stack=list(start)
    n=0
    while stack and n<max_nodes:
        ac=stack.pop(); n+=1
        a,c=ac
        if val(c)==0:
            key=('oo',)
        else:
            v=val(a)/val(c); key=(round(v,9),)
        if key in seen: continue
        seen.add(key)
        if val(c)!=0 and hgt(c)<=Q+1e-9 and -1e-9<=val(a)/val(c)<val(LAM)+1e-9:
            out[round(val(a)/val(c),10)]=ac
        # expand by S, then by S-of-T-translates within the strip:
        # neighbors that keep things reachable: S(ac), and S(T^{+-1} ac).
        for shift in (0,1,-1,2,-2):
            t=(a if shift==0 else add(a,mul((0,shift),c)), c)
            nb=canon(applyS(t))
            na,nc=nb
            if val(nc)==0:
                continue
            if hgt(nc)<=Q*1.5+2:    # allow slight slack so all height<=Q cusps are reached
                k2=(round(val(na)/val(nc),9),)
                if k2 not in seen:
                    stack.append(nb)
    return out

def analyze(Q):
    cusps=generate(Q)
    items=sorted(cusps.items())
    if len(items)<5:
        return dict(Q=Q,n_cusps=len(items),fail=True)
    vals=[v for v,_ in items]
    dens=[abs(val(ac[1])) for _,ac in items]
    X4=S2/8
    P=[dens[n]*dens[n+1]/(Q*Q) for n in range(len(dens)-1)]
    gaps=[vals[n+1]-vals[n] for n in range(len(vals)-1)]
    # neighbor determinant in Z[sqrt2]
    dets=[]
    for n in range(len(items)-1):
        (_,(a0,c0)),(_,(a1,c1))=items[n],items[n+1]
        dets.append(sub(mul(a1,c0),mul(a0,c1)))
    detvals=sorted(set(round(val(d),4) for d in dets))
    # cluster: longest run of P<X4, and window violations of various lengths
    def longest_run(pred):
        b=cur=0
        for v in P:
            if pred(v): cur+=1; b=max(b,cur)
            else: cur=0
        return b
    run=longest_run(lambda v:v<X4-1e-9)
    def winviol(w): return sum(1 for i in range(len(P)-w+1) if max(P[i:i+w])<X4-1e-7)
    return dict(Q=Q,n_cusps=len(items),X4=X4,
                min_gap=min(gaps),max_gap=max(gaps),min_P=min(P),max_P=max(P),
                run_below_X=run, viol_w2=winviol(2),viol_w3=winviol(3),
                n_below=sum(1 for p in P if p<X4-1e-9),
                detvals=detvals[:12])

if __name__=="__main__":
    print("X(4)=sqrt2/8 =",S2/8)
    for Q in [10,20,40,80,160]:
        r=analyze(Q)
        if r.get('fail'):
            print(f"Q={Q}: only {r['n_cusps']} cusps -- generation incomplete"); continue
        print(f"Q(height)={Q:>4}  #cusps={r['n_cusps']:>6}  "
              f"P in [{r['min_P']:.5f},{r['max_P']:.5f}]  #P<X4={r['n_below']}  "
              f"runBelowX={r['run_below_X']}  viol(w2)={r['viol_w2']} viol(w3)={r['viol_w3']}")
        print(f"     consecutive-neighbor determinants (distinct real vals): {r['detvals']}")
