#!/usr/bin/env python3
"""
Diagnostic: does the 4-below local window found at floors (1,1,2) extend to a
GENUINE bi-infinite T_5 orbit staying in D, or does it escape?

If it escapes (fwd or bwd) within a few steps -> the local 4-window bound failure
is a "naive-D-not-forward-invariant" artifact (FINDINGS sec 5/T7): the bound holds
on real recurrent orbits but is NOT provable from local window data alone => the
goal-C `g5_core` *local* lemma is FALSE and the proof route as posed is infeasible.

If it does NOT escape -> the 4-window bound is genuinely false and X(5)=1/4 lower
bound itself is in question.
"""
import math
phi = (1+math.sqrt(5))/2
T = 0.25

def fwd(x, y):
    k = math.floor((1+x)/(phi*y))
    return y, k*phi*y - x, k

def bwd(y, z):
    # invert: from (x,y)->(y,z) with z=k*phi*y-x, k=floor((1+x)/(phi*y)).
    # given (y,z) recover x: x = k*phi*y - z, with k=floor((1+x)/(phi*y)).
    # solve self-consistently over small k.
    for k in range(1, 30):
        x = k*phi*y - z
        if x <= 1e-12: continue
        if math.floor((1+x)/(phi*y)) == k:
            return x, y, k
    return None

def in_D(x, y):
    return x > 1e-9 and y > 1e-9 and x + phi*y > 1 - 1e-9

def trace(a,b,c,d,e, label):
    print("\n--- %s ---" % label)
    seq = [a,b,c,d,e]
    print("  window coords:", [round(v,4) for v in seq])
    print("  window products:", [round(seq[i]*seq[i+1],4) for i in range(4)],
          " (all < 1/4 ?", all(seq[i]*seq[i+1] < T-1e-9 for i in range(4)), ")")
    # extend forward from (d,e)
    print("  FORWARD from (d,e):")
    x,y = d,e
    okf = True
    prods=[]
    for n in range(12):
        if not in_D(x,y):
            print("    step %d: (%.4f,%.4f) ESCAPED D" % (n,x,y)); okf=False; break
        x,y,k = fwd(x,y)
        prods.append(round(x*y,4))   # product of NEW pair
        if not (y>1e-9):
            print("    step %d: coord<=0 (y=%.4f) ESCAPED" % (n,y)); okf=False; break
    if okf: print("    stayed in D 12 steps; new products:", prods)
    # extend backward from (a,b)
    print("  BACKWARD from (a,b):")
    y,z = a,b
    okb=True
    prods=[]
    for n in range(12):
        r = bwd(y,z)
        if r is None:
            print("    step %d: no valid preimage in D ESCAPED (backward)" % n); okb=False; break
        x,_,k = r
        if not in_D(x,y):
            print("    step %d: preimage (%.4f,%.4f) not in D ESCAPED" % (n,x,y)); okb=False; break
        prods.append(round(x*y,4))
        z,y = y,x
    if okb: print("    stayed in D 12 steps (backward); products:", prods)
    return okf, okb

if __name__ == "__main__":
    # the (1,1,2) all-below config found by the grid search (recompute cleanly)
    # solve exactly: pick b,c then a=phi*b-c (k0=1), d=phi*c-b (k1=1), e=2*phi*d-c (k2=2)
    # search a clean rational-ish witness near the grid hit (b~0.459,c~0.483)
    best=None
    for bi in range(300,520):
        for ci in range(300,560):
            b=bi/1000; c=ci/1000
            a=phi*b-c; d=phi*c-b; e=2*phi*d-c
            seq=[a,b,c,d,e]
            if any(v<=1e-6 for v in seq): continue
            if not all(in_D(seq[i],seq[i+1]) for i in range(4)): continue
            if math.floor((1+a)/(phi*b))!=1: continue
            if math.floor((1+b)/(phi*c))!=1: continue
            if math.floor((1+c)/(phi*d))!=2: continue
            mp=max(seq[i]*seq[i+1] for i in range(4))
            if mp < T-1e-6:
                if best is None or mp<best[0]:
                    best=(mp,a,b,c,d,e)
    if best:
        mp,a,b,c,d,e=best
        print("Cleanest 4-below (1,1,2) window: maxP=%.5f"%mp)
        trace(a,b,c,d,e,"(1,1,2) 4-below window")
    else:
        print("no (1,1,2) all-below witness re-found")
