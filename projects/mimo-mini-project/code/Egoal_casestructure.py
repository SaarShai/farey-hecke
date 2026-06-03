#!/usr/bin/env python3
"""Design the g5_core case structure. q=5, lam=phi, thr=1/phi^3.
For 5-coord windows (a,b,c,d,e) following the scalar map (floors K0,K1,K2>=1),
domain sums>1, study:
 (1) Is the cap ESSENTIAL? Compare ALL4-below feasibility WITH vs WITHOUT cap.
 (2) Under 'P0,P1,P2 < thr + cap + domain', the feasible (K0,K1,K2) and min(P3).
 (3) Bounds forced on each coord (b<?, c in [?,?], etc.) -> certificate hints.
"""
import math
import numpy as np
phi = (1+math.sqrt(5))/2
l = phi; thr = 1.0/phi**3
print(f"phi={phi:.6f} thr=1/phi^3={thr:.8f}  2/phi^4={2/phi**4:.6f}  sqrt(2)/phi^2={math.sqrt(2)/phi**2:.6f}")

def windows(cap, require_first3_below, Nab=900, nb=400):
    """enumerate (a,b), follow map 3 steps -> coords[0..4], floors[0..2].
    yield (a,b,coords,Ks,Ps) satisfying domain(all pairs)>1, pos, [cap], [first3 below]."""
    for ia in range(1, Nab+1):
        a = ia/Nab
        blo = max(1 - l*a, 1e-9)
        if blo >= 1: continue
        for ib in range(nb+1):
            b = blo + (1.0-blo)*ib/nb
            if not (0 < b <= 1): continue
            if not (a + l*b > 1): continue
            coords=[a,b]; Ks=[]
            ok=True
            for s in range(3):
                cc,cp = coords[-2],coords[-1]
                if not (cp>0 and cc+l*cp>1): ok=False;break
                K=math.floor((1+cc)/(l*cp))
                if K<1: ok=False;break
                coords.append(K*l*cp-cc); Ks.append(K)
            if len(coords)<5: continue
            if any(x<=0 for x in coords): continue
            if cap and any(x>1+1e-12 for x in coords): continue
            if not all(coords[j]+l*coords[j+1]>1 for j in range(4)): continue
            Ps=[coords[j]*coords[j+1] for j in range(4)]
            if require_first3_below and not all(Ps[j]<thr-1e-12 for j in range(3)): continue
            yield a,b,coords,Ks,Ps

print("\n(1) ALL-4-below feasible?  cap vs nocap:")
for cap in (True, False):
    hits=0; ex=None
    for a,b,coords,Ks,Ps in windows(cap, require_first3_below=True):
        if all(p<thr-1e-12 for p in Ps):
            hits+=1
            if ex is None: ex=(round(a,4),round(b,4),Ks,[round(p,5) for p in Ps],[round(c,4) for c in coords])
    print(f"  cap={cap}: all4-below hits={hits}  ex={ex}")

print("\n(2) Under P0,P1,P2<thr + cap + domain: floor words and min(P3):")
from collections import defaultdict
minP3 = defaultdict(lambda: 9.0)
exP3 = {}
coordrange = defaultdict(lambda:[9,-9,9,-9,9,-9,9,-9,9,-9])  # min/max each coord
for a,b,coords,Ks,Ps in windows(True, require_first3_below=True):
    key=tuple(Ks)
    if Ps[3]<minP3[key]:
        minP3[key]=Ps[3]
        exP3[key]=(round(a,4),round(b,4),[round(p,5) for p in Ps],[round(c,4) for c in coords])
    cr=coordrange[key]
    for j in range(5):
        cr[2*j]=min(cr[2*j],coords[j]); cr[2*j+1]=max(cr[2*j+1],coords[j])
for key in sorted(minP3, key=lambda k:minP3[k]):
    print(f"  K={key}: min P3={minP3[key]:.6f} (thr={thr:.6f}, margin={minP3[key]-thr:+.6f})")
    print(f"        ex {exP3[key]}")
    cr=coordrange[key]
    print(f"        coord ranges: a[{cr[0]:.3f},{cr[1]:.3f}] b[{cr[2]:.3f},{cr[3]:.3f}] "
          f"c[{cr[4]:.3f},{cr[5]:.3f}] d[{cr[6]:.3f},{cr[7]:.3f}] e[{cr[8]:.3f},{cr[9]:.3f}]")

print("\n(3) symmetric: under P1,P2,P3<thr + cap + domain: min(P0) and floors:")
minP0 = defaultdict(lambda: 9.0); exP0={}
for a,b,coords,Ks,Ps in windows(True, require_first3_below=False):
    if not all(Ps[j]<thr-1e-12 for j in (1,2,3)): continue
    key=tuple(Ks)
    if Ps[0]<minP0[key]:
        minP0[key]=Ps[0]; exP0[key]=(round(a,4),round(b,4),[round(p,5) for p in Ps])
for key in sorted(minP0,key=lambda k:minP0[k]):
    print(f"  K={key}: min P0={minP0[key]:.6f} (margin={minP0[key]-thr:+.6f}) ex {exP0[key]}")
