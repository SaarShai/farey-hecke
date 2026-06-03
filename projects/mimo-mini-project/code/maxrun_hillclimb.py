#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
maxrun_hillclimb.py — aggressively MAXIMIZE the longest sub-V(q) in-D run, to test whether it is
BOUNDED (no-ground-state lemma) and find the true window W*(q). Random restart + local perturbation
hill-climb on the seed (x0,y0). If the max run stays ~3(q-2)/2 under hard search, runs are bounded.
"""
import math, random
import mpmath as mp
mp.mp.dps = 40

def lam(q): return 2*mp.cos(mp.pi/q)
def Vq(q):
    th=mp.pi/q; s=1/(2*mp.sin(2*th))
    return s*s*(mp.cos(th) if q%2==0 else mp.cos(th/2)**2)
def in_D(x,y,l): return x>0 and y>0 and (x+l*y)>1
def step(x,y,l):
    k=int(mp.floor((1+x)/(l*y))); return k*l*y-x,k

def run_len(x0,y0,l,V,eps,maxsteps=4000):
    thr=V*(1+eps); x,y=x0,y0; best=cur=0
    for _ in range(maxsteps):
        if not in_D(x,y,l): break
        if x*y<=thr: cur+=1; best=max(best,cur)
        else: cur=0
        yn,k=step(x,y,l)
        if yn<=0: break
        x,y=y,yn
    return best

def maximize(q,restarts=4000,iters=400):
    l=lam(q); V=Vq(q); eps=mp.mpf('1e-10')
    best=0; bestseed=None
    for _ in range(restarts):
        x=mp.mpf(random.uniform(0,1.6)); y=mp.mpf(random.uniform(0,1.6))
        if not in_D(x,y,l): continue
        r=run_len(x,y,l,V,eps)
        scale=mp.mpf('0.05')
        for _ in range(iters):
            nx=x+mp.mpf(random.uniform(-1,1))*scale
            ny=y+mp.mpf(random.uniform(-1,1))*scale
            if not in_D(nx,ny,l): continue
            nr=run_len(nx,ny,l,V,eps)
            if nr>=r:
                if nr>r: scale=mp.mpf('0.05')
                x,y,r=nx,ny,nr
            else:
                scale*=mp.mpf('0.98')
        if r>best: best=r; bestseed=(x,y)
    return best,bestseed

if __name__=="__main__":
    random.seed(2024)
    print(f"{'q':>3} {'q-2':>4} {'3(q-2)/2':>9} {'MAXRUN':>7}")
    for q in range(5,12):
        b,seed=maximize(q)
        print(f"{q:>3} {q-2:>4} {3*(q-2)/2:>9.1f} {b:>7}", flush=True)
