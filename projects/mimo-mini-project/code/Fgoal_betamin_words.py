#!/usr/bin/env python3
"""
GOAL F task3: beta_min via PERIODIC scalar words (proper, not random orbits).
Scalar map matrix M_k = [[0,1],[-1,k*lam]] acts on (c_n,c_{n+1}).  A periodic floor-word
(k_0..k_{p-1}) has product Mword; a real periodic orbit = its eigen-direction (real eigenvalue).
Build the orbit c_0..c_{p-1}, require feasibility (0<c_n<=1, c_n+lam c_{n+1}>1), compute
time-average of P=c_n c_{n+1}. min over feasible words = upper bound on beta_min (genuine <= scalar).
If min < 1/lam^3 -> averaging/sub-action route DEAD for that q.
"""
import math, itertools
import numpy as np

def lam(q): return 2*math.cos(math.pi/q)
def Mk(k,L): return np.array([[0.0,1.0],[-1.0,k*L]])

def word_orbit_avg(word,L):
    M=np.eye(2)
    for k in word: M=Mk(k,L)@M
    ev,V=np.linalg.eig(M)
    best=None
    for j in range(2):
        if abs(ev[j].imag)>1e-9: continue
        v=V[:,j].real
        # scale: pick scale so orbit feasible; the orbit point is direction v=(c0,c1)
        # iterate the word from (c0,c1), collect c_n; scale invariant for P? P scales as s^2.
        # We need actual feasible scale: try to find s with all c_n in (0,1], c_n+lam c_{n+1}>1.
        c0,c1=v
        if c0==0 and c1==0: continue
        # generate full period
        cs=[c0,c1]
        ok=True
        cc0,cc1=c0,c1
        for k in word:
            cc0,cc1 = cc1, k*L*cc1-cc0
            cs.append(cc1)
        cs=cs[:len(word)]  # one period of c_n (approx)
        cs=np.array(cs)
        if np.any(cs==0): continue
        if np.any(cs<0) and np.any(cs>0):  # mixed sign -> not a positive orbit
            continue
        cs=np.abs(cs)
        # scale so max c =1 (largest feasible); then check c_n+lam c_{n+1}>1 and <=1
        s=1.0/cs.max()
        cs2=cs*s
        # feasibility
        feas=all(cs2[i]+L*cs2[(i+1)%len(cs2)]>1+1e-9 for i in range(len(cs2))) and all(0<x<=1+1e-9 for x in cs2)
        # time-average of product
        prods=[cs2[i]*cs2[(i+1)%len(cs2)] for i in range(len(cs2))]
        avg=sum(prods)/len(prods)
        if feas:
            if best is None or avg<best: best=avg
    return best

for q in [5,7,9,11,13,15]:
    L=lam(q); thr=1/L**3
    best=1e9; bw=None
    for p in range(1,8):
        for word in itertools.product([1,2,3],repeat=p):
            if sum(word)==p and p>1: pass
            a=word_orbit_avg(list(word),L)
            if a is not None and a<best: best=a; bw=word
    flag="DEAD (beta_min<thr)" if best<thr-1e-4 else "beta_min>=thr (route not excluded this q)"
    print(f"q={q}: 1/lam^3={thr:.6f}  min feasible word-avg P={best:.6f} ratio={best/thr:.4f} word={bw}  {flag}")
