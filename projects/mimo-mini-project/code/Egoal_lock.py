#!/usr/bin/env python3
"""Lock the proof facts: (1) floor upper bound under all-4-below; (2) cap necessity;
(3) the worst-case margins per floor combo with both edges (+/- cap)."""
import math, itertools
phi=(1+math.sqrt(5))/2; l=phi; thr=1.0/phi**3
def coords(a,b,K): c=K[0]*l*b-a; d=K[1]*l*c-b; e=K[2]*l*d-c; return (a,b,c,d,e)
def floors_ok(cc,K):
    for (ci,cj,K_) in [(cc[0],cc[1],K[0]),(cc[1],cc[2],K[1]),(cc[2],cc[3],K[2])]:
        if cj<=0: return False
        v=(1+ci)/(l*cj)
        if not (K_<=v<K_+1): return False
    return True
def edges_ok(cc):
    return all(cc[j]+l*cc[j+1]>1 and l*cc[j]+cc[j+1]>1 for j in range(4))

for use_cap in (True,False):
    print(f"\n===== cap={use_cap} =====")
    feas_all4={}; feas3={}
    for K in itertools.product(range(1,7),repeat=3):
        mm=9; ex=None; got3=False
        for ia in range(1,1601):
            a=ia/1600.0
            for ib in range(1,1001):
                b=ib/1000.0
                cc=coords(a,b,K)
                if any(x<=1e-9 for x in cc): continue
                if use_cap and any(x>1+1e-12 for x in cc): continue
                if not edges_ok(cc): continue
                if not floors_ok(cc,K): continue
                Ps=[cc[j]*cc[j+1] for j in range(4)]
                m=max(Ps)
                if m<mm: mm=m; ex=(round(a,4),round(b,4),[round(p,4) for p in Ps])
                if all(p<thr-1e-12 for p in Ps): feas_all4[K]=ex
                if sum(1 for p in Ps if p<thr-1e-12)>=3: got3=True
        if ex is not None and mm<thr+0.03:  # near-threshold combos
            feas3[K]=(round(mm,6),ex)
    print(f"  ALL-4-below feasible combos: {feas_all4 if feas_all4 else 'EMPTY (window-4 TRUE)'}")
    maxK=max(max(k) for k in feas3) if feas3 else 0
    print(f"  near-thr combos (min-max<thr+0.03), max floor seen = {maxK}:")
    for K in sorted(feas3,key=lambda k:feas3[k][0]):
        print(f"    K={K}: min-max={feas3[K][0]:.6f} margin={feas3[K][0]-thr:+.6f} ex{feas3[K][1]}")
