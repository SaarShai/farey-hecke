#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ff_exact.py -- EXACT, UNCONDITIONAL function-field variance ordering for prime (irreducible)
moduli M over F_q[t], via the L-polynomial of each Dirichlet character. Confirms the analogue
of Fiorilli-Martin Thm 1.10:  a = -1 is the variance-MAX (least-biased) non-residue, with the
mechanism = the place-at-infinity parity gap (odd characters have one more Frobenius zero).

For M irreducible of degree d:  A/M = F_{q^d},  units = F_{q^d}^* (cyclic, order q^d - 1).
For a character chi mod M, the Dirichlet L-function is the polynomial
    L(u,chi) = sum_{n=0}^{d-1} c_n u^n ,   c_n = sum_{f monic, deg f = n} chi(f mod M),
and by Weil's RH (a THEOREM) every inverse zero has absolute value sqrt q. The RS limiting
variance of the prime race (a vs 1) is, UNCONDITIONALLY (per-zero weight uniform = 1):
    V(M;a,1) = sum_{chi != chi0} |chi(a) - 1|^2 * N_chi ,   N_chi = deg L(u,chi) = #Frobenius zeros.
PARITY: chi "even" (chi|F_q^* trivial)  -> N_chi = d-2 ;  chi "odd" (chi(-1) = -1) -> N_chi = d-1.
So a=-1 (the constant), which has |chi(-1)-1|^2 = 4 exactly on the ODD chars and 0 on even,
concentrates ALL weight on the maximal-N_chi characters  =>  V(M;-1,1) is MAXIMAL among NR.
(Requires deg M odd & q == 3 mod 4 for -1 to be a non-residue, i.e. q^d == 3 mod 4.)

Everything here is UNCONDITIONAL (Weil); no Grand Simplicity / Linear Independence is used.
"""
import math, cmath
from itertools import product
import numpy as np

# ---- F_q[t] poly ops (coeffs low->high) ----
def norm(p, q):
    p = [c % q for c in p]
    while len(p) > 1 and p[-1] == 0: p.pop()
    return tuple(p)
def pdeg(p):
    p = norm(p, 10**9)
    return -1 if (len(p) == 1 and p[0] == 0) else len(p) - 1
def pmul(a, b, q):
    if (len(a)==1 and a[0]==0) or (len(b)==1 and b[0]==0): return (0,)
    r = [0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b): r[i+j]=(r[i+j]+x*y)%q
    return norm(r,q)
def pmod(a, m, q):
    a=list(norm(a,q)); m=list(norm(m,q)); dm=len(m)-1; inv=pow(m[-1],q-2,q)
    while len(a)-1>=dm and not(len(a)==1 and a[0]==0):
        da=len(a)-1; coef=(a[-1]*inv)%q
        for i in range(len(m)): a[da-dm+i]=(a[da-dm+i]-coef*m[i])%q
        while len(a)>1 and a[-1]==0: a.pop()
    return norm(a,q)

def mult_order(g, M, q, n):
    x=(1,); o=0
    for _ in range(n+1):
        x=pmod(pmul(x,g,q),M,q); o+=1
        if x==(1,): return o
    return -1

def find_generator(M, q, d):
    n=q**d-1
    # try low polys as generators
    cands=[]
    for coeffs in product(range(q), repeat=d):
        r=norm(tuple(coeffs),q)
        if r==(0,): continue
        cands.append(r)
    for g in cands:
        if mult_order(g,M,q,n)==n: return g
    raise RuntimeError("no generator")

def analyze_irreducible(M, q, verbose=True):
    d=pdeg(M); n=q**d-1
    # units = all nonzero residues deg<d ; dlog table
    g=find_generator(M,q,d)
    dlog={}; x=(1,)
    for e in range(n):
        dlog[x]=e; x=pmod(pmul(x,g,q),q if False else M,q)
    units=list(dlog.keys())
    minus1=norm((q-1,),q)
    # precompute monic polys of each degree 0..d-1 and their residues (=themselves, deg<d)
    monic={0:[(1,)]}
    for nn in range(1,d):
        monic[nn]=[norm(tuple(tail)+(1,),q) for tail in product(range(q),repeat=nn)]
    # for each character k: c_n and N_chi
    def chi(k, r): return cmath.exp(2j*math.pi*k*dlog[r]/n)
    results={}
    Nsplit={'even':set(),'odd':set()}
    for k in range(1,n):  # non-principal
        c=[]
        for nn in range(0,d):
            s=sum(chi(k, f) for f in monic[nn])  # f deg<d so f mod M = f
            c.append(s)
        # N_chi = highest index with |c|>tol
        Nchi=0
        for idx in range(d-1,-1,-1):
            if abs(c[idx])>1e-7: Nchi=idx; break
        par='odd' if abs(chi(k,minus1)+1)<1e-7 else 'even'
        Nsplit[par].add(Nchi)
        results[k]=(Nchi, par, c)
    # Weil check: pick one odd char with Nchi=d-1, check roots
    weil="n/a"
    for k,(Nchi,par,c) in results.items():
        if Nchi==d-1 and d>=2:
            coeffs=[complex(z) for z in c[:Nchi+1]]
            roots=np.roots(coeffs[::-1])  # poly c0+c1u+...; np.roots wants high->low
            invabs=[1/abs(rt) for rt in roots]  # inverse zeros = Frobenius eigenvalues
            weil=f"|Frob|={[round(v,4) for v in invabs]} (sqrt q={math.sqrt(q):.4f})"
            break
    # variance V(a)=sum_k |chi(a)-1|^2 N_k
    def V(a): return sum(abs(chi(k,a)-1)**2 * results[k][0] for k in results)
    squares=set(pmod(pmul(u,u,q),M,q) for u in units)
    NR=[u for u in units if u not in squares]
    Vs={a:V(a) for a in units if a!=(1,)}
    NRsorted=sorted(NR,key=lambda a:-Vs[a]) if NR else []
    if verbose:
        print(f"\n=== M={M} irreducible deg {d} over F_{q}: |F_{q}^{d}*|={n}, #NR={len(NR)} ===")
        print(f"    N_chi by parity: even chars -> {sorted(Nsplit['even'])} (expect d-2={d-2}); "
              f"odd chars -> {sorted(Nsplit['odd'])} (expect d-1={d-1})")
        print(f"    Weil check (one odd char): {weil}")
        is_m1_nr = minus1 in NR
        print(f"    -1={minus1}; non-residue? {is_m1_nr}  (expect True iff q^d==3 mod4: {q**d%4==3})")
        if is_m1_nr:
            rank=NRsorted.index(minus1)+1
            print(f"    V_exact(-1)={Vs[minus1]:.3f}; rank {rank}/{len(NR)} (1=max); "
                  f"argmax V={Vs[NRsorted[0]]:.3f}")
            uniq = all(abs(Vs[a]-Vs[minus1])>1e-6 for a in NR if a!=minus1)
            print(f"    -> a=-1 is {'the UNIQUE variance-MAX non-residue' if rank==1 and uniq else 'rank %d'%rank}"
                  f"  [UNCONDITIONAL, Weil]")
        # show distinct V values among NR
        from collections import Counter
        print(f"    distinct V values over NR: {sorted(set(round(Vs[a],3) for a in NR), reverse=True)}")
    return Vs, NR, minus1, Nsplit

if __name__=="__main__":
    print("EXACT unconditional function-field variance ordering (Weil; no GSH/LI).")
    # irreducible moduli, several (q,d); need q^d == 3 mod 4 for -1 to be a non-residue
    cases=[
        (3, norm((1,2,0,1),3)),     # F_3, deg3  t^3+2t+1   (3^3=27==3 mod4 -> -1 is NR)
        (3, norm((2,0,0,0,0,1),3)), # F_3, deg5  t^5+2 (check irreducible) 27 cases
        (7, norm((3,0,1),7)),       # F_7, deg2  t^2+3 (7^2=49==1 mod4 -> -1 square; control)
        (3, norm((1,0,1),3)),       # F_3, deg2  t^2+1 (control: -1 square)
        (7, norm((1,1,1),7)),       # F_7 deg2 control
    ]
    for q,M in cases:
        try:
            analyze_irreducible(M,q)
        except Exception as e:
            print(f"  M={M} q={q}: {e}")
    # the headline clean cases: odd-degree irreducible over F_3 and F_7 (q==3 mod4)
    print("\n--- headline: odd-degree prime moduli (q^d == 3 mod 4) ---")
    analyze_irreducible(norm((1,2,0,1),3),3)   # deg3/F3 repeat as anchor
