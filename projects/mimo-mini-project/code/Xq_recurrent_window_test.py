#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xq_recurrent_window_test.py  (goal #7)

Disambiguate: is the 3-window floor max(P_n,P_{n+1},P_{n+2}) >= X(q) FALSE for q>=5, or just an
artifact of transient/escaping orbits?

Method:
 - iterate T_q from many seeds; KEEP only orbits that survive >= SURV steps (recurrent dynamics);
 - drop a burn-in; measure on the recurrent TAIL:
     * longest run of consecutive P_n < X(q)
     * # 3-windows with max < X(q)   (genuine refutation if > 0 on recurrent points)
     * also longest run / windows for the (q-2)-window  [the optimizer-period generalization]
 - print one explicit violating triple (consecutive in-domain points) for q=5 as proof.

Cross-check: q=3,4 must give run<=2 and ZERO 3-window violations (they are PROVEN).
"""
import math, random
random.seed(2718)

def lam(q): return 2.0*math.cos(math.pi/q)

def Xq(q):
    table={3:2/9,4:math.sqrt(2)/8,5:0.25,6:math.sqrt(3)/6,7:0.3887395330218428,
           8:0.5*math.cos(math.pi/8),9:0.5868240888334652,10:0.6881909602355868,
           11:0.8379846460292439,12:math.cos(math.pi/12)}
    return table[q]

def in_dom(x,y,L): return (0<x<=1+1e-12) and (0<y<=1+1e-12) and (x+L*y>1-1e-12)

def Tq(x,y,L):
    k=math.floor((1+x)/(L*y))
    return y,k*L*y-x,k

def orbit(q,x0,y0,maxsteps):
    L=lam(q); x,y=x0,y0; pts=[]
    for _ in range(maxsteps):
        if not in_dom(x,y,L): break
        pts.append((x,y))
        x,y,k=Tq(x,y,L)
        if k<1: break
    return pts

def longest_run_below(P,X,eps=1e-9):
    best=cur=0
    for v in P:
        if v<X-eps: cur+=1; best=max(best,cur)
        else: cur=0
    return best

def window_violations(P,X,w,eps=1e-7):
    """# of length-w windows whose MAX is < X (i.e. all w consecutive products < X)."""
    n=0
    for i in range(len(P)-w+1):
        if max(P[i:i+w])<X-eps: n+=1
    return n

def analyze(q,n_seeds=3000,maxsteps=2000,SURV=200,burn=50):
    L=lam(q); X=Xq(q)
    tail_P=[]            # concatenated recurrent tails (per-orbit, kept separate for runs)
    runs3=0; viol3=0; viol_qm2=0
    max_run=0
    n_recurrent=0
    example=None
    total_tail=0
    for _ in range(n_seeds):
        for _ in range(50):
            x0=random.random(); y0=random.random()
            if x0+L*y0>1: break
        pts=orbit(q,x0,y0,maxsteps)
        if len(pts)<SURV: continue
        n_recurrent+=1
        tpts=pts[burn:]                       # recurrent tail
        P=[x*y for (x,y) in tpts]
        total_tail+=len(P)
        max_run=max(max_run,longest_run_below(P,X))
        viol3+=window_violations(P,X,3)
        viol_qm2+=window_violations(P,X,max(3,q-2))
        if example is None:
            # find an explicit 3-window all < X
            for i in range(len(P)-2):
                if P[i]<X-1e-7 and P[i+1]<X-1e-7 and P[i+2]<X-1e-7:
                    example=(tpts[i],tpts[i+1],tpts[i+2],tpts[i+3] if i+3<len(tpts) else None,
                             P[i],P[i+1],P[i+2])
                    break
    return dict(q=q,lam=L,X=X,n_recurrent=n_recurrent,total_tail=total_tail,
                max_run_below_X=max_run,viol_3window=viol3,
                viol_qm2_window=viol_qm2,example=example)

if __name__=="__main__":
    print(f"{'q':>3} {'X(q)':>11} {'#recur':>7} {'#tailP':>9} {'maxRun<X':>9} "
          f"{'viol(3win)':>11} {'viol(q-2 win)':>13}")
    examples={}
    for q in [3,4,5,6,7,8]:
        r=analyze(q)
        print(f"{r['q']:>3} {r['X']:>11.7f} {r['n_recurrent']:>7} {r['total_tail']:>9} "
              f"{r['max_run_below_X']:>9} {r['viol_3window']:>11} {r['viol_qm2_window']:>13}")
        examples[q]=r['example']
    print("\nq=3,4 are PROVEN cluster<=2: must show maxRun<X<=2 and viol(3win)=0.")
    print("If q>=5 shows viol(3win)>0 on RECURRENT tails, the 3-window floor is genuinely FALSE for q>=5.\n")
    for q in [5,6,7]:
        ex=examples.get(q)
        if ex:
            print(f"q={q} explicit 3 consecutive recurrent points with P<X(q)={Xq(q):.6f}:")
            print(f"   (x,y)_0={ex[0]}, P0={ex[4]:.6f}")
            print(f"   (x,y)_1={ex[1]}, P1={ex[5]:.6f}")
            print(f"   (x,y)_2={ex[2]}, P2={ex[6]:.6f}")
            # verify they are genuine consecutive T_q images
            L=lam(q); x,y=ex[0]
            y2,yn,k=Tq(x,y,L)
            print(f"   check T_q(p0)=({y2:.6f},{yn:.6f}) vs p1={ex[1]}  (k={k})")
