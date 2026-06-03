#!/usr/bin/env python3
"""Find the MINIMAL hypothesis set for g5_core (all-4-below => False).
Variables a,b free; floors K0,K1,K2 either INT>=1 or REAL>=1; coords
c=K0 phi b - a, d=K1 phi c - b, e=K2 phi d - c.
Hyp toggles: cap (all coords<=1); floorUB (K_i <= (1+c_i)/(phi c_{i+1}), the floor
upper bound); domain (4 sums>1); pos (all coords>0). Target all4 products<thr.
Report feasibility (search hardest = most relaxed)."""
import math, random
random.seed(5)
phi=(1+math.sqrt(5))/2; l=phi; thr=1.0/phi**3

def test(real_floors, use_cap, use_floorUB, use_domain, N=4000000):
    hits=0; ex=None
    for _ in range(N):
        a=random.uniform(0.05,1.0 if use_cap else 2.0)
        b=random.uniform(0.05,1.0 if use_cap else 2.0)
        if real_floors:
            K0=random.uniform(1.0,4.0); K1=random.uniform(1.0,4.0); K2=random.uniform(1.0,4.0)
        else:
            K0=random.randint(1,4); K1=random.randint(1,4); K2=random.randint(1,4)
        c=K0*l*b-a; d=K1*l*c-b; e=K2*l*d-c
        coords=[a,b,c,d,e]
        if any(x<=1e-9 for x in coords): continue
        if use_cap and any(x>1+1e-9 for x in coords): continue
        if use_domain and not all(coords[j]+l*coords[j+1]>1 for j in range(4)): continue
        if use_floorUB:
            ok=True
            for (ci,cj,K) in [(a,b,K0),(b,c,K1),(c,d,K2)]:
                # K = floor((1+ci)/(phi cj)) <=> K <= (1+ci)/(phi cj) < K+1
                v=(1+ci)/(l*cj)
                if not (K<=v+1e-9 and v<K+1+1e-9): ok=False;break
            if not ok: continue
        Ps=[coords[j]*coords[j+1] for j in range(4)]
        if all(p<thr-1e-9 for p in Ps):
            hits+=1
            if ex is None: ex=(round(a,3),round(b,3),(round(K0,2),round(K1,2),round(K2,2)),
                               [round(p,4) for p in Ps],[round(c,3) for c in coords])
    return hits,ex

print(f"thr={thr:.6f}")
configs=[
 ("REAL floors>=1, +cap +domain, NO floorUB", dict(real_floors=True,use_cap=True,use_floorUB=False,use_domain=True)),
 ("REAL floors>=1, +cap +domain +floorUB",    dict(real_floors=True,use_cap=True,use_floorUB=True,use_domain=True)),
 ("REAL floors>=1, NOcap +domain +floorUB",   dict(real_floors=True,use_cap=False,use_floorUB=True,use_domain=True)),
 ("INT floors>=1, +cap +domain, NO floorUB",  dict(real_floors=False,use_cap=True,use_floorUB=False,use_domain=True)),
 ("INT floors>=1, NOcap +domain +floorUB",    dict(real_floors=False,use_cap=False,use_floorUB=True,use_domain=True)),
]
for name,kw in configs:
    h,ex=test(**kw)
    print(f"{name}: hits={h}  {'FEASIBLE ex='+str(ex) if h else 'EMPTY'}")
