#!/usr/bin/env python3
import math, random
random.seed(11)
def lam(q): return 2*math.cos(math.pi/q)
for q in [5,6,7,8,13]:
    l=lam(q); thr=1.0/l**3
    maxrun=0
    for _ in range(400000):
        c=random.uniform(0.01,1.5); cp=random.uniform(0.01,1.5)
        if not (c+l*cp>1): continue
        run=0
        for n in range(50):
            if not (c>0 and cp>0 and c+l*cp>1): break
            K=math.floor((1+c)/(l*cp))
            if K<1: break
            P=c*cp; c2=K*l*cp-c
            if P<thr-1e-12: run+=1; maxrun=max(maxrun,run)
            else: run=0
            c,cp=cp,c2
    print(f"q={q}: SCALAR thr={thr:.6f} maxrun_below={maxrun}  (window={maxrun+1})")
print()
# per-branch exact minima for q=5 via fine grid + report minimizer
import numpy as np
q=5; l=lam(q); thr=1.0/l**3
U=np.array([[l,-1.0],[1.0,0.0]]); w=[np.array([1.0,0.0])]
for _ in range(q+3): w.append(U@w[-1])
def branch_of(a,b,eps=1e-9):
    for i in range(2,q):
        t1=a*w[i-1][0]+b*w[i-1][1]; ti=a*w[i][0]+b*w[i][1]
        if t1>1-eps and ti<=1+eps: return i
    return None
def P_obs(a,b,i):
    ti=a*w[i][0]+b*w[i][1]; return a*ti/w[i][1]
mins={2:(9,None),3:(9,None)}
N=2000
for ia in range(1,N):
    a=ia/N; blo=1-l*a
    for ib in range(N+1):
        b=max(blo,-1)+(1-max(blo,-1))*ib/N
        if not(0<a<=1 and 1-l*a<b<=1): continue
        i=branch_of(a,b)
        if i in (2,3):
            P=P_obs(a,b,i)
            if P<mins[i][0]: mins[i]=(P,(a,b))
print(f"q=5 thr=1/phi^3={thr:.6f}")
for i in (2,3):
    print(f"  branch {i}: minP={mins[i][0]:.6f} at (a,b)={tuple(round(x,4) for x in mins[i][1])}")
