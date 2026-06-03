#!/usr/bin/env python3
"""
GOAL F (B) — verify the CLEAN reformulation and the uniform inequality.

Reformulation (via det x_{i-1}^2 - x_i x_{i-2} = 1, equiv. E: m^2+c^2-lam m c =1, m=x_{i-1},c=x_{i-2}):
  branch i constraints in (a, v=L_i):
     (i)  a + c v > m            [L_{i-1} > 1]
     (ii) c a + v > m            [domain lam a + b > 1]
     a in (0,1], v in (0,1].
  P_i = a v / m.  Want P_i >= 1/lam^3  <=>  a v >= m/lam^3.

Claims to verify:
  (1) min of a*v over the region is at a=v=m/(1+c)  (when c>1); =  m^2/(1+c)^2.
      => min P_i = m/(1+c)^2.
  (2) Uniform inequality  lam^3 * x_{i-1} >= (1 + x_{i-2})^2   for i=2..q-2, all q>=5,
      with EQUALITY iff cusp (i=q-2, m=lam, c=lam^2-1).
  (3) Cross-check P_i min from (1) == 1/lam^3 at cusp, > else.
"""
import math, numpy as np
from itertools import combinations

def build(q):
    lam=2*math.cos(math.pi/q); x={-1:0.0,0:1.0}
    for i in range(1,q+2): x[i]=lam*x[i-1]-x[i-2]
    return lam,x

def min_av_region(m,c,N=2000):
    """brute min of a*v over a,v in (0,1], a+cv>m, ca+v>m."""
    best=1e9; arg=None
    for ia in range(1,N+1):
        a=ia/N
        for iv in range(1,N+1):
            v=iv/N
            if a+c*v>m-1e-12 and c*a+v>m-1e-12:
                if a*v<best: best=a*v; arg=(a,v)
    return best,arg

print("=== Verify clean reformulation: min(a*v) == m^2/(1+c)^2, and uniform ineq ===")
maxviol=0.0
for q in range(5,15):
    lam,x=build(q); thr=1/lam**3
    for i in range(2,q-1):
        m=x[i-1]; c=x[i-2]
        Erel = m*m+c*c-lam*m*c   # should be 1
        # uniform inequality
        lhs=lam**3*m; rhs=(1+c)**2
        gap=lhs-rhs
        # predicted min P
        minP_pred = m/(1+c)**2
        cusp = (i==q-2)
        if gap < -1e-9: maxviol=min(maxviol,gap)
        flag=""
        if cusp and abs(gap)>1e-6: flag="  !!cusp not tight"
        if not cusp and gap<1e-9: flag="  !!noncusp tight/violated"
        print(f"  q={q} i={i:<2}{'CUSP' if cusp else '    '}: E={Erel:.6f} "
              f"lam^3*x_{{i-1}}-(1+x_{{i-2}})^2={gap:+.6e}  minP_pred={minP_pred:.6f} "
              f"(thr={thr:.6f}, ratio={minP_pred/thr:.5f}){flag}")
print(f"\nmax violation of uniform inequality (should be 0): {maxviol:.2e}")

print("\n=== Brute-min check (small q) that min(a*v)=m^2/(1+c)^2 ===")
for q in [5,7,9]:
    lam,x=build(q)
    for i in range(2,q-1):
        m=x[i-1]; c=x[i-2]
        if c<=1+1e-9:  # i=2 special (c=1): both constraints same line a+v>m
            bf,arg=min_av_region(m,c,1500)
            pred=None
            print(f"  q={q} i={i}: c={c:.4f}(=1 case) brute min av={bf:.6f} at {arg}; "
                  f"corner a=1,v=m-1 -> av={1*(m-1):.6f}")
            continue
        bf,arg=min_av_region(m,c,1500)
        pred=(m/(1+c))**2
        print(f"  q={q} i={i}: brute min(a*v)={bf:.6f} at {arg}  pred m^2/(1+c)^2={pred:.6f}  diff={bf-pred:+.2e}")
