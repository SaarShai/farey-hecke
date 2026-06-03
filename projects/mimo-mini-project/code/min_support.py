#!/usr/bin/env python3
"""Greedy-minimal support certificate (numeric phi). For each tight combo, find the
SMALLEST set of pairwise products whose nonneg cone (+ eq multipliers) contains -1.
Then test that subset feasibility. Output minimal product lists for a lean nlinarith."""
import numpy as np
from itertools import combinations_with_replacement
from scipy.optimize import linprog
phi=(1+5**0.5)/2
import sympy as sp
a,b,c,d,e=sp.symbols('a b c d e'); V=[a,b,c,d,e]

def gens(K0,K1,K2):
    G={'a':a,'b':b,'c':c,'d':d,'e':e,
       'reg_ab':a+phi*b-1,'reg_bc':b+phi*c-1,'reg_cd':c+phi*d-1,'reg_de':d+phi*e-1,
       'gen_ab':phi*a+b-1,'gen_bc':phi*b+c-1,'gen_cd':phi*c+d-1,'gen_de':phi*d+e-1,
       'f0':(K0+1)*phi*b-1-a,'f1':(K1+1)*phi*c-1-b,'f2':(K2+1)*phi*d-1-c,
       's0':1-a*b*(2*phi+1),'s1':1-b*c*(2*phi+1),'s2':1-c*d*(2*phi+1),'s3':1-d*e*(2*phi+1),
       'ca':1-a,'cb':1-b,'cc':1-c,'cd':1-d,'ce':1-e}
    E={'r0':a+c-K0*phi*b,'r1':b+d-K1*phi*c,'r2':c+e-K2*phi*d}
    return G,E

def setup(K):
    G,E=gens(*K); gn=list(G); en=list(E)
    terms=[(('G',n),G[n]) for n in gn]
    for i,j in combinations_with_replacement(range(len(gn)),2):
        terms.append((('P',gn[i],gn[j]),sp.expand(G[gn[i]]*G[gn[j]])))
    monosE=[sp.Integer(1),a,b,c,d,e]
    eqt=[(('E',n,str(m)),sp.expand(E[n]*m)) for n in en for m in monosE]
    allt=terms+eqt; nNon=len(terms)
    # monomial index (numeric phi substituted)
    polys=[sp.Poly(sp.expand(ex.subs(phi, sp.Float(phi,20))),*V) for _,ex in allt]
    mset=set()
    for p in polys:
        for mono in p.monoms(): mset.add(mono)
    ml=sorted(mset); mi={m:i for i,m in enumerate(ml)}; M=len(ml)
    A=np.zeros((M,len(allt)))
    for k,p in enumerate(polys):
        for mono,co in zip(p.monoms(),p.coeffs()): A[mi[mono],k]=float(co)
    const=tuple([0]*5); ci=mi[const]
    beq=np.zeros(M); beq[ci]=-1.0
    return A,beq,allt,nNon

def feasible_subset(A,beq,allt,nNon,prod_idx,eq_idx):
    cols=prod_idx+eq_idx
    bounds=[(0,None)]*len(prod_idx)+[(None,None)]*len(eq_idx)
    res=linprog(c=np.zeros(len(cols)),A_eq=A[:,cols],b_eq=beq,bounds=bounds,method='highs')
    return res

for K in [(2,1,2),(1,2,1),(1,1,2),(2,1,1)]:
    A,beq,allt,nNon=setup(K)
    eq_idx=[k for k in range(len(allt)) if allt[k][0][0]=='E']
    prod_all=[k for k in range(nNon) if allt[k][0][0]=='P']
    # full feasibility
    res=feasible_subset(A,beq,allt,nNon,prod_all,eq_idx)
    if not res.success: print(f"K={K}: full infeasible?!"); continue
    # greedy prune: start from support, drop one at a time if still feasible
    support=[prod_all[i] for i in range(len(prod_all)) if abs(res.x[i])>1e-7]
    changed=True
    while changed:
        changed=False
        for k in list(support):
            trial=[x for x in support if x!=k]
            r=feasible_subset(A,beq,allt,nNon,trial,eq_idx)
            if r.success:
                support=trial; changed=True; break
    print(f"K={K}: MINIMAL support size={len(support)}")
    for k in support:
        print(f"   {allt[k][0]}")
