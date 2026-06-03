#!/usr/bin/env python3
"""For each floor combo (K0,K1,K2) in a box, decide feasibility of the g5_core
hypotheses via dense sampling of the 2 free vars (a,b) -> coords determined.
Hyps: a,b,c,d,e>0; (cap: <=1); domain a+phi b>1,b+phi c>1,c+phi d>1,d+phi e>1;
floor-consistency K_i = floor((1+c_i)/(phi c_{i+1}));
and target: P0,P1,P2,P3 all < thr (=1/phi^3).
Report which combos are feasible for: (i) all-4-below (should be NONE),
(ii) first-3-below (the run-3 boundary). Establish floor upper bounds."""
import math
phi=(1+math.sqrt(5))/2; l=phi; thr=1.0/phi**3

def coords_from(a,b):
    coords=[a,b]; Ks=[]
    for s in range(3):
        cc,cp=coords[-2],coords[-1]
        if not (cp>1e-12 and cc+l*cp>1): return None
        K=math.floor((1+cc)/(l*cp))
        if K<1: return None
        coords.append(K*l*cp-cc); Ks.append(K)
    return coords,Ks

def feasible(below_idx, cap, Kmax_report=6, Nab=1500, nb=700):
    """below_idx: set of product indices required < thr. Return dict K->example."""
    found={}
    for ia in range(1,Nab+1):
        a=ia/Nab
        blo=max(1-l*a,1e-9)
        if blo>=1: continue
        for ib in range(nb+1):
            b=blo+(1.0-blo)*ib/nb
            if not(0<b<=1 and a+l*b>1): continue
            r=coords_from(a,b)
            if r is None: continue
            coords,Ks=r
            if any(x<=0 for x in coords): continue
            if cap and any(x>1+1e-12 for x in coords): continue
            if not all(coords[j]+l*coords[j+1]>1 for j in range(4)): continue
            Ps=[coords[j]*coords[j+1] for j in range(4)]
            if not all(Ps[j]<thr-1e-12 for j in below_idx): continue
            key=tuple(Ks)
            if key not in found:
                found[key]=(round(a,4),round(b,4),[round(p,5) for p in Ps],[round(c,4) for c in coords])
    return found

for cap in (True, False):
    print(f"\n########## cap={cap} ##########")
    print("ALL-4-below feasible floor combos (target: EMPTY):")
    f4=feasible({0,1,2,3}, cap)
    print(f"  -> {dict(f4) if f4 else 'EMPTY (window-4 holds)'}")
    print("first-3-below {0,1,2} feasible floor combos (run-3 boundary):")
    f3=feasible({0,1,2}, cap)
    for k in sorted(f3): print(f"  K={k}: ex {f3[k]}")
    print("last-3-below {1,2,3} feasible floor combos:")
    f3b=feasible({1,2,3}, cap)
    for k in sorted(f3b): print(f"  K={k}: ex {f3b[k]}")
    # floor upper bounds observed under first-3-below
    if f3:
        k0s=[k[0] for k in f3]; k1s=[k[1] for k in f3]; k2s=[k[2] for k in f3]
        print(f"  floor ranges under first-3-below: K0<= {max(k0s)}, K1<= {max(k1s)}, K2<= {max(k2s)}")
