#!/usr/bin/env python3
"""
DECISIVE q=5 test. Two measurements:

 (A) Max run of consecutive products < 1/4 over GENUINE forward orbits in D.
     Seed a fine grid of in-D points, iterate T_5 while staying in D, record the
     longest run of P_n < 1/4. If bounded by W0 -> a (W0+1)-window bound holds on
     forward orbits; if it can be made arbitrarily long / infinite -> no finite
     window works (and X(5)<1/4 would follow, refuting the goal entirely).

 (B) Min over in-D forward orbits of  sup_n P_n  (orbit must stay in D >= L steps).
     If some orbit keeps sup P < 1/4 over a long horizon -> X(5) < 1/4 (goal false).
     If inf of sup P -> 1/4 from above and never below -> X(5)=1/4 lower bound OK.
"""
import math
phi = (1+math.sqrt(5))/2
T = 0.25
EPS = 1e-9

def in_D(x,y):
    return x>EPS and y>EPS and x+phi*y > 1+1e-12

def step(x,y):
    k = math.floor((1+x)/(phi*y))
    return y, k*phi*y - x

def forward_run_and_sup(x0,y0,maxsteps=2000):
    """iterate; return (longest below-run while in D, sup product while in D, steps in D)."""
    x,y = x0,y0
    if not in_D(x,y): return None
    run=best=0; supP=0.0; n=0
    while n < maxsteps and in_D(x,y):
        P = x*y
        supP = max(supP,P)
        if P < T - 1e-12: run+=1; best=max(best,run)
        else: run=0
        x,y = step(x,y)
        n+=1
    return best, supP, n

def scan(grid=600, maxsteps=4000):
    print("="*72)
    print("(A)/(B) forward orbits in D: longest below-1/4 run, min sup-product")
    print("="*72)
    longest_run = 0; run_witness=None
    # for min sup, only count orbits that survive a decent horizon L
    L = 200
    min_sup = math.inf; sup_witness=None
    survivors=0; total=0
    # grid over (x,y) in (0,1.2]x(0,1.2] intersect D
    for i in range(1,grid+1):
        x = 1.3*i/grid
        for j in range(1,grid+1):
            y = 1.3*j/grid
            if not in_D(x,y): continue
            total+=1
            r = forward_run_and_sup(x,y,maxsteps)
            if r is None: continue
            best,supP,steps = r
            if best > longest_run:
                longest_run=best; run_witness=(round(x,4),round(y,4),steps)
            if steps >= L:
                survivors+=1
                if supP < min_sup:
                    min_sup=supP; sup_witness=(round(x,4),round(y,4),steps,supP)
    print("  in-D seeds scanned:", total, " survivors(>=%d steps):"%L, survivors)
    print("  LONGEST below-1/4 run over forward orbits:", longest_run,
          " witness(x,y,steps)=", run_witness)
    print("  MIN sup-product over orbits surviving >=%d steps: %.8f" % (L, min_sup),
          " witness=", sup_witness)
    print()
    if min_sup < T - 1e-6:
        print("  !!! FOUND long-horizon orbit with sup P < 1/4  => X(5) < 1/4, GOAL FALSE.")
    else:
        print("  No long-horizon in-D orbit keeps sup P below 1/4 (min sup >= ~1/4).")
        print("  => X(5)=1/4 lower bound consistent; below-runs bounded by", longest_run, ".")
        print("  => smallest provable window length would be", longest_run+1,
              "(local window must exceed max forward run).")

if __name__ == "__main__":
    scan(grid=500, maxsteps=4000)
