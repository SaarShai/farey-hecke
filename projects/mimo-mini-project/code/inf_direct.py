#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""inf_direct.py — model-free estimate of X(q)=inf over invariant measures of essSup P.
Key fact: X(q) = inf over seeds (x,y) in D of sup_{n>=0} P(T^n(x,y))  (smallest c s.t. sublevel
{P<=c} contains a forward-invariant orbit). We minimize J_N(seed)=max_{n<N} P(T^n seed) over seeds
via random search + local refine. Reveals X(q) AND attainment: if the minimizing orbit stays
bounded away from the boundary x+lam y=1 (and floors don't jump), the inf is ATTAINED (ground
state); if it creeps onto the open boundary / a floor edge, NOT attained (no ground state).
Also reports the floor-word of the near-optimal orbit. Usage: inf_direct.py q [N] [tries]"""
import math, random, sys

def lam(q): return 2*math.cos(math.pi/q)

def step(x,y,l):
    k=math.floor((1.0+x)/(l*y))
    return y, k*l*y - x, k

def run(x,y,l,N):
    """return (maxP, escaped?, min_margin, floors[:40]) where margin=min(x+λy-1) along orbit."""
    maxP=0.0; floors=[]; margin=math.inf; ok=True
    for n in range(N):
        if not (x>0 and y>0):
            ok=False; break
        m=x+l*y-1.0
        if m<margin: margin=m
        if m<=0: ok=False; break
        P=x*y
        if P>maxP: maxP=P
        ny=(1.0+x)/(l*y)
        k=math.floor(ny)
        if k<1: ok=False; break
        if n<40: floors.append(k)
        x,y = y, k*l*y-x
    return maxP, ok, margin, floors

def J(seed,l,N):
    x,y=seed
    if not(x>0 and y>0 and x+l*y>1): return math.inf
    mp,ok,margin,_=run(x,y,l,N)
    return mp if ok else math.inf

def minimize(q,N=300,tries=20000,seedpts=None):
    l=lam(q); best=(math.inf,None)
    # sample seeds: focus near the binding boundary x+λy=1 and small P
    cand=[]
    for _ in range(tries):
        # parametrize a point near boundary: choose x in (0, 1.5), y so that x+λy slightly >1
        x=random.uniform(0.01,1.2)
        ymin=max(1e-6,(1.0-x)/l)
        y=ymin+random.uniform(0.0,1.2)
        cand.append((x,y))
    if seedpts: cand+=seedpts
    for s in cand:
        j=J(s,l,N)
        if j<best[0]: best=(j,s)
    # local refine around best
    for _ in range(6):
        b=best[1];
        if b is None: break
        scale=0.05*best[0]+1e-3
        for _ in range(4000):
            s=(b[0]+random.uniform(-scale,scale), b[1]+random.uniform(-scale,scale))
            j=J(s,l,N)
            if j<best[0]: best=(j,s)
        scale*=0.4
    return l,best

if __name__=="__main__":
    q=int(sys.argv[1]); N=int(sys.argv[2]) if len(sys.argv)>2 else 400
    tries=int(sys.argv[3]) if len(sys.argv)>3 else 30000
    random.seed(12345)
    l,(jbest,sbest)=minimize(q,N,tries)
    print(f"q={q} lam={l:.6f}  X_est = {jbest:.8f}")
    if sbest:
        mp,ok,margin,floors=run(sbest[0],sbest[1],l,N)
        print(f"  best seed=({sbest[0]:.6f},{sbest[1]:.6f}) maxP={mp:.8f} ok={ok} min_margin(x+λy-1)={margin:.2e}")
        print(f"  floor-word(first 40)={floors}")
    # references
    refs={3:2/9,4:math.sqrt(2)/8,5:0.25,6:math.sqrt(3)/6}
    if q in refs: print(f"  known X({q})={refs[q]:.8f}")
