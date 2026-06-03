#!/usr/bin/env python3
"""Goal D pre-test: on the GENUINE Taha map, test (A) max run-length of P<1/lam^3,
and (B) min time-average of P. Determines window vs sub-action feasibility."""
import math, random
import numpy as np
random.seed(1)

def lam(q): return 2*math.cos(math.pi/q)
def ellipse_vecs(q,l):
    U=np.array([[l,-1.0],[1.0,0.0]]); w=[np.array([1.0,0.0])]
    for _ in range(q+3): w.append(U@w[-1])
    return w
def branch_of(a,b,w,q,eps=1e-9):
    for i in range(2,q):
        t1=a*w[i-1][0]+b*w[i-1][1]; ti=a*w[i][0]+b*w[i][1]
        if t1>1-eps and ti<=1+eps: return i
    return None
def step(a,b,w,q,l):
    i=branch_of(a,b,w,q)
    if i is None: return None
    ti=a*w[i][0]+b*w[i][1]; ti1=a*w[i+1][0]+b*w[i+1][1]
    k=math.floor((1-ti1)/(l*ti))
    return (ti, ti1+k*l*ti), i, k
def P_obs(a,b,i,w):  # P = a*(a,b).w_i / y_i,  y_i=w[i][1]
    ti=a*w[i][0]+b*w[i][1]
    return a*ti/w[i][1]
def rand_seed(l):
    # uniform in Tq: 0<a<=1, 1-l a < b <=1
    a=random.uniform(1e-6,1.0)
    blo=1-l*a
    b=random.uniform(max(blo,-1.0)+1e-9, 1.0)
    return a,b

for q in [5,6,7,8,9,12]:
    l=lam(q); w=ellipse_vecs(q,l); thr=1.0/l**3
    maxrun=0; run_example=None
    min_avg=1e9; min_avg_word=None
    NS=4000; STEPS=2000
    global_minP=1e9
    for _ in range(NS):
        a,b=rand_seed(l)
        run=0; Psum=0.0; cnt=0; ok=True
        seq=[]
        for n in range(STEPS):
            r=step(a,b,w,q,l)
            if r is None: ok=False; break
            (na,nb),i,k=r
            P=P_obs(a,b,i,w)
            Psum+=P; cnt+=1
            global_minP=min(global_minP,P)
            if P<thr-1e-12:
                run+=1
                if run>maxrun: maxrun=run; run_example=(a,b)
            else:
                run=0
            a,b=na,nb
        if cnt>200:
            avg=Psum/cnt
            if avg<min_avg: min_avg=avg
    print(f"q={q}: 1/lam^3={thr:.6f}  maxrun(P<thr)={maxrun}  min_time_avg={min_avg:.6f}  "
          f"(min_avg/thr={min_avg/thr:.4f})  global_minP={global_minP:.6f}")
