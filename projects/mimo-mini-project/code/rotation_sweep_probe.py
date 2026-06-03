#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rotation_sweep_probe.py — find & dissect longest sub-V(q) IN-D runs (mpmath, exact V).
FIX: a product P_n counts only if the pair (c_n,c_{n+1}) is in D. The final escaping pair
does NOT count. Question: true window W*(q) such that any W*(q) consecutive in-D products
contain one > V (rotation-sweep). Print floor + product sequence of the worst orbit.
"""
import math, random
import mpmath as mp
mp.mp.dps = 60

def lam(q): return 2*mp.cos(mp.pi/q)

def Vq(q):
    th = mp.pi/q
    s_lo = 1/(2*mp.sin(2*th))
    maxprod = mp.cos(th) if q%2==0 else mp.cos(th/2)**2
    return s_lo*s_lo*maxprod

def in_D(x,y,l): return x>0 and y>0 and (x+l*y)>1

def step(x,y,l):
    k = int(mp.floor((1+x)/(l*y)))
    return k*l*y - x, k

def run_orbit(x0,y0,l,maxsteps=4000):
    """Return list of in-D pairs as (c_n, c_{n+1}, k_n). Stops at first out-of-D pair."""
    pairs=[]
    x,y=x0,y0
    for _ in range(maxsteps):
        if not in_D(x,y,l): break
        yn,k = step(x,y,l)
        pairs.append((x,y,k))
        if yn<=0: break
        x,y=y,yn
    return pairs

def longest_run(pairs,V,eps):
    """Longest run of consecutive in-D pairs with product ≤ V*(1+eps)."""
    thr=V*(1+eps)
    best=cur=0; bi=0; cs=0
    for n,(a,b,k) in enumerate(pairs):
        if a*b<=thr:
            if cur==0: cs=n
            cur+=1
            if cur>best: best=cur; bi=cs
        else: cur=0
    return best,bi

def main():
    eps=mp.mpf('1e-12')
    for q in [5,6,7,8,9,10,11]:
        l=lam(q); V=Vq(q); W=q-2
        random.seed(7)
        best=0; bestorb=None
        for _ in range(80000):
            x=mp.mpf(random.uniform(0,1.5)); y=mp.mpf(random.uniform(0,1.5))
            if not in_D(x,y,l): continue
            pairs=run_orbit(x,y,l,maxsteps=800)
            r,bi=longest_run(pairs,V,eps)
            if r>best:
                best=r; bestorb=(pairs,bi)
        pairs,bi=bestorb
        print(f"\n=== q={q}  V={mp.nstr(V,12)}  q-2={W}  longest sub-V IN-D run = {best} (idx {bi}) ===")
        a=max(0,bi-1); b=min(len(pairs), bi+best+2)
        for n in range(a,b):
            x,y,k=pairs[n]; p=x*y
            mark='*' if p<=V*(1+eps) else ' '
            print(f"  n={n:>3} (c_n,c_n+1)=({mp.nstr(x,7):>10},{mp.nstr(y,7):>10}) P={mp.nstr(p,9):>12} ({mp.nstr(p/V,6)}V) k={k}{mark}")

if __name__=="__main__":
    main()
