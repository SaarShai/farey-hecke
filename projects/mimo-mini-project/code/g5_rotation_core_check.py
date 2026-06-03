#!/usr/bin/env python3
"""
Verify the all-floor-1 (pure-rotation) sub-case sub-lemma BEFORE Lean.

All-floor-1: every step uses k=1, i.e. c_{n+2}=phi*c_{n+1}-c_n (rotation by 36 deg),
E = c_n^2+c_{n+1}^2 - phi*c_n*c_{n+1} conserved.

Q1: in a pure-rotation segment with region (c_n+phi c_{n+1} > 1) on all pairs and
    FLOOR-CONSISTENCY (each step really has floor 1: 1<= (1+c_n)/(phi c_{n+1}) <2),
    what is the MAX run of consecutive products < 1/4 ?  -> decides window for g5_rot.
Q2: is g5_rot3 ('no 3 consecutive products <1/4 in a floor-1 segment') TRUE?
    (i.e. is the max run <= 2?)  Search hard for a counterexample (run>=3).
"""
import math, random
phi=(1+math.sqrt(5))/2
T=0.25; EPS=1e-9
random.seed(7)

def floor1_ok(x,y):
    """step (x,y)->(y, phi*y-x) genuinely has floor 1: 1 <= (1+x)/(phi*y) < 2."""
    v=(1+x)/(phi*y)
    return 1-1e-12 <= v < 2-1e-12

def region(x,y): return x>EPS and y>EPS and x+phi*y>1+1e-12

def rot_run_from(c0,c1, maxlen=40):
    """build pure-rotation segment; return max run of consecutive products<T while
    region AND floor-1-consistency hold at each step (a genuine all-floor-1 segment)."""
    c=[c0,c1]
    # extend forward as long as floor stays 1 and region holds
    prods=[]
    for _ in range(maxlen):
        x,y=c[-2],c[-1]
        if not region(x,y): break
        if not floor1_ok(x,y): break          # if floor != 1, segment (as all-floor-1) ends
        z=phi*y-x
        if z<=EPS: break
        prods.append(x*y)
        c.append(z)
    # longest run of consecutive products < T
    run=best=0
    for p in prods:
        if p<T-1e-12: run+=1; best=max(best,run)
        else: run=0
    return best, prods

def search(N=4000000):
    best=0; wit=None; bestprods=None
    # also direct: violate g5_rot3 => find a,b,c,d with ab,bc,cd<T, region, both steps floor1
    rot3_violated=False; rot3_wit=None
    for _ in range(N):
        b=random.random()*0.7+0.02
        c=random.random()*0.7+0.02
        # try as the middle pair; pick a via floor-1 step a+c=phi b => a=phi b - c
        a=phi*b-c
        d=phi*c-b
        if min(a,b,c,d)<=EPS: continue
        # both interior steps floor-1 consistent
        if not floor1_ok(a,b): continue
        if not floor1_ok(b,c): continue
        if not floor1_ok(c,d): continue   # need 3 floor-1-consistent pairs for window-3
        if not (region(a,b) and region(b,c) and region(c,d)): continue
        P=[a*b,b*c,c*d]
        if all(p<T-1e-12 for p in P):
            rot3_violated=True; rot3_wit=(a,b,c,d,P); break
    # max-run scan via segment extension from random seeds
    for _ in range(200000):
        c0=random.random()*0.9+0.02
        c1=random.random()*0.9+0.02
        if not region(c0,c1): continue
        r,prods=rot_run_from(c0,c1)
        if r>best: best=r; wit=(c0,c1); bestprods=prods
    return best,wit,bestprods,rot3_violated,rot3_wit

if __name__=="__main__":
    print("phi=",phi," 1/(4phi)=",1/(4*phi))
    b,w,bp,v3,w3 = search()
    print("MAX below-1/4 run in pure-rotation (all-floor-1) segments:",b)
    if w: print("  witness seed (c0,c1)=",tuple(round(x,5) for x in w))
    print("g5_rot3 ('no 3 consecutive <1/4 in floor-1 segment') counterexample found?",v3)
    if v3:
        a,b2,c2,d2,P=w3
        print("  !! VIOLATED: (a,b,c,d)=",tuple(round(x,5) for x in (a,b2,c2,d2)),
              " products=",[round(p,5) for p in P])
        print("  => g5_rot3 is FALSE; the rotation core needs a larger window.")
    else:
        print("  no counterexample => g5_rot3 (window-3 rotation core) appears TRUE.")
