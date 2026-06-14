"""
bq_truth.py -- GROUND TRUTH B(q) from the genuine full Taha G_q-BCZ map, q=7..40.
Uses double precision (fast) but with deep sampling; the runs are robust integers so
fp is fine for the COUNT (we separately re-confirm the deepest q=23/24 runs at dps=50
in bq_exact_mechanism.py).  B(q) = max consecutive (last-branch i=q-1 AND P=a*b < 1/lam^3).
"""
import math, sys
import numpy as np
rng = np.random.default_rng(20260614)

def lam_of(q): return 2.0*math.cos(math.pi/q)
def t_of(q):   return 1.0/lam_of(q)**3
def hecke_w(q):
    lam = lam_of(q); w=[(1.0,0.0)]
    for _ in range(q+2):
        x,y=w[-1]; w.append((lam*x-y,x))
    return lam,w
def step(a,b,lam,w,q):
    sub=q-1; d_prev=w[1][0]*a+w[1][1]*b
    for i in range(2,q):
        di=w[i][0]*a+w[i][1]*b
        if d_prev>1 and di<=1: sub=i; break
        d_prev=di
    wi=w[sub][0]*a+w[sub][1]*b; wi1=w[sub+1][0]*a+w[sub+1][1]*b; yi=w[sub][1]
    P=a*wi/yi; k=math.floor((1-wi1)/(lam*wi))
    return wi, wi1+k*lam*wi, sub, P, k
def Bq(q, nstarts=24, nsteps=600000, burn=500):
    lam,w=hecke_w(q); t=t_of(q); best=0; bestkp=None
    for _ in range(nstarts):
        while True:
            a=rng.random(); b=rng.random()
            if 0<a<=1 and (1-lam*a)<b<=1: break
        for _ in range(burn): a,b,_,_,_=step(a,b,lam,w,q)
        cur=0; curkp=[]
        for _ in range(nsteps):
            a,b,i,P,k=step(a,b,lam,w,q)
            # observable belongs to PRE-image; we test the point that was just consumed.
            # Re-derive: easier to track previous. Use post-hoc: store as we go.
            if i==q-1 and P<t:
                cur+=1; curkp.append(k)
            else:
                if cur>best: best=cur; bestkp=curkp[:]
                cur=0; curkp=[]
        if cur>best: best=cur; bestkp=curkp[:]
    return best, bestkp

if __name__=="__main__":
    qs=range(int(sys.argv[1]) if len(sys.argv)>1 else 7, (int(sys.argv[2]) if len(sys.argv)>2 else 40)+1)
    for q in qs:
        b,kp=Bq(q)
        print(f"q={q:2d}  B={b}  kpattern_of_deepest={kp}", flush=True)
