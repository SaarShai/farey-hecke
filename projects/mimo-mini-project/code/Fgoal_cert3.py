#!/usr/bin/env python3
"""
GOAL F (B) Step B: lam^3 m >= (1+c)^2.
We have three consecutive Chebyshev values c=x_{i-2}, m=x_{i-1}, p=x_i, with:
  R1: m = lam*c - x_{i-3}   (x_{i-3}>=0  =>  m <= lam c)
  R2: p = lam*m - c
  det: m^2 = 1 + p c   (equiv. m^2+c^2-lam m c = 1)
  positivity: c>=1, p>=1 (x_i>=1 for i<=q-2), m>=lam.
Question: which MINIMAL subset of {c>=1, p>=1, m>=lam, m<=lam c, m<=lam p, E=0, phi<=lam<2}
proves  lam^3 m - (1+c)^2 >= 0  for ALL reals satisfying them (not just Chebyshev)?
If a clean subset works, nlinarith can close it.
"""
import numpy as np, math

def test_subset(name, feas, NT=400000, lam_range=(1.61803,1.9999)):
    """sample (lam,m,c) with E=0 enforced (solve p,m), check feas->inequality."""
    rng=np.random.default_rng(0)
    worst=1e9; worstpt=None; n=0
    for _ in range(NT):
        lam=rng.uniform(*lam_range)
        c=rng.uniform(1.0, 1.0/math.sin(math.pi/ max(5, math.pi/math.acos(lam/2))) if False else 8.0)
        # E: m^2 - lam c m + (c^2-1)=0 -> m = [lam c +- sqrt(lam^2 c^2 -4(c^2-1))]/2
        disc=lam*lam*c*c-4*(c*c-1)
        if disc<0: continue
        for sign in (+1,-1):
            m=(lam*c+sign*math.sqrt(disc))/2
            if m<=0: continue
            p=lam*m-c
            if not feas(lam,m,c,p): continue
            n+=1
            val=lam**3*m-(1+c)**2
            if val<worst: worst=val; worstpt=(lam,m,c,p)
    return name,worst,worstpt,n

subsets = {
 "c>=1,p>=1":            lambda L,m,c,p: c>=1 and p>=1,
 "c>=1,m>=lam":          lambda L,m,c,p: c>=1 and m>=L,
 "c>=1,p>=1,m>=lam":     lambda L,m,c,p: c>=1 and p>=1 and m>=L,
 "c>=1,p>=1,m<=lam*p":   lambda L,m,c,p: c>=1 and p>=1 and m<=L*p,
 "c>=1,p>=1,m<=lam*c":   lambda L,m,c,p: c>=1 and p>=1 and m<=L*c,
 "p>=1,m<=lam*p,c>=1":   lambda L,m,c,p: p>=1 and m<=L*p and c>=1,
 "p>=1,m<=lam*p,m<=lam*c":lambda L,m,c,p: p>=1 and m<=L*p and m<=L*c,
}
print("Scan: does the subset imply lam^3 m-(1+c)^2 >=0 ? (worst value should be >=0)")
for nm,f in subsets.items():
    name,worst,pt,n=test_subset(nm,f)
    flag="  OK" if worst>=-1e-6 else "  ** FAILS **"
    print(f"  [{nm}] worst={worst:+.6f} (n={n}) at {None if pt is None else tuple(round(z,4) for z in pt)}{flag}")

print("\nNow the factor form D=(p-1)*Q, Q=p^2+(3c+1)p+(1+2c+c^2-c^3); with linkage m<=lam p (x_{i+1}>=0):")
print("  test Q(p)>=0 under p>=1,c>=1,m<=lam p, p=lam m-c, m^2=1+pc:")
def feasQ(L,m,c,p): return p>=1 and c>=1 and m<=L*p+1e-12
rng=np.random.default_rng(1); worstQ=1e9; pt=None
for _ in range(800000):
    L=rng.uniform(1.61803,1.9999); c=rng.uniform(1,8)
    disc=L*L*c*c-4*(c*c-1)
    if disc<0: continue
    for s in(+1,-1):
        m=(L*c+s*math.sqrt(disc))/2
        if m<=0: continue
        p=L*m-c
        if not feasQ(L,m,c,p): continue
        Q=p*p+(3*c+1)*p+(1+2*c+c*c-c**3)
        if Q<worstQ: worstQ=Q; pt=(L,m,c,p)
print(f"  worst Q={worstQ:+.5f} at {None if pt is None else tuple(round(z,4) for z in pt)}")
