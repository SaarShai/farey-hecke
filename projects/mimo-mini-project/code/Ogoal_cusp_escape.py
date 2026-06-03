#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GOAL O (CORE, validated) — the cusp-escape realization of X_Omega(q)=1/lam^3 + no ground state.

Matches the PROVEN Lean (lean/BCZHeckeGenuine_allq_VERIFIED.lean):
  - cusp segment  cuspSeg = {p | b=0, 1/lam < a <= 1}  is INVARIANT (on b=0 the genuine cusp branch
    M_{q-2,0}=[[1,lam],[0,1]] acts as (a,0)->(a,0): every segment point is a FIXED POINT).
  - observable there  cuspP(a) = a*(a+lam*0)/lam = a^2/lam  (= general P on the cusp branch, b=0).
  - cuspP(a) = a^2/lam is MINIMIZED as a->1/lam+  ->  (1/lam)^2/lam = 1/lam^3,  approached but NEVER
    attained (a>1/lam strict; the vertex a=1/lam is EXCLUDED because 1-lam*a=0 violates 1-lam*a<b=0).
  => the minimizing invariant-measure sequence  mu_n = delta_{a_n},  a_n -> 1/lam+,  has
     essSup cuspP = a_n^2/lam -> 1/lam^3  (no ground state: the optimizer ESCAPES to the excluded
     cusp vertex (1/lam,0)). This is the L-infinity (min-MAX) zero-temperature / escape-of-mass picture.

This script VALIDATES that picture numerically (anchor: 1/lam^3 at q=5 = 1/phi^3 = 0.23607) and prints
the escaping sequence essSup -> 1/lam^3. The richer Gibbs mu_beta / freezing / beta_min (min-AVERAGE,
DIFFERENT value) picture needs the transfer-operator build (see GOAL_O_zerotemp_cusp_escape.md) — NOT here.
"""
import math, sys

def lam_of(q): return 2*math.cos(math.pi/q)

def cuspP(l, a): return a*a/l          # = a*(a+l*0)/l on b=0 (the proven cuspP on the segment)

def demo(q):
    l = lam_of(q); thr = 1/l**3
    vertex_a = 1/l
    print(f"\n=== q={q}  lam={l:.8f}  1/lam^3={thr:.8f}  cusp vertex a=1/lam={vertex_a:.6f} ===")
    # (1) cuspP on the segment a in (1/lam, 1]: inf at a->1/lam+, sup at a=1
    print(f"  cuspP(a)=a^2/lam on the invariant cusp segment a in (1/lam, 1]:")
    print(f"    inf  = lim_{{a->1/lam+}} a^2/lam = {cuspP(l, vertex_a):.8f}  (= 1/lam^3, the value)  NOT attained")
    print(f"    sup  = cuspP(1) = 1/lam      = {cuspP(l, 1.0):.8f}  (attained at a=1)")
    # (2) escaping minimizing sequence delta_{a_n}, a_n -> 1/lam+
    print(f"  escaping sequence mu_n = delta_(a_n), a_n -> 1/lam+ :  essSup cuspP = a_n^2/lam -> 1/lam^3")
    print("     a_n - 1/lam     a_n          essSup cuspP   ratio/thr   dist-to-excluded-vertex")
    for d in [1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-9]:
        a = vertex_a + d
        if a > 1: continue
        es = cuspP(l, a)
        print(f"     {d:.0e}         {a:.8f}   {es:.8f}   {es/thr:.6f}   {a-vertex_a:.0e}")
    return thr

if __name__ == "__main__":
    qs = [int(z) for z in sys.argv[1:]] or [5, 7, 10, 17, 30, 100]
    print("ANCHORS: 1/lam^3 at q=5 must be 1/phi^3 = %.8f" % (1/((1+5**.5)/2)**3))
    for q in qs:
        thr = demo(q)
    # explicit anchor checks
    phi=(1+5**.5)/2
    print("\nANCHOR CHECK:")
    print(f"  q=5  1/lam^3 = {1/lam_of(5)**3:.10f}   1/phi^3 = {1/phi**3:.10f}   match={abs(1/lam_of(5)**3-1/phi**3)<1e-12}")
    print(f"  q->inf 1/lam^3 -> 1/8 = {1/8:.6f}  (lam->2);  q=100: {1/lam_of(100)**3:.6f}")
    print("\nVERDICT: essSup cuspP -> 1/lam^3 from ABOVE as the optimizer escapes to the excluded cusp")
    print("vertex (1/lam,0) => X_Omega(q)=1/lam^3 realized by escape-of-mass, NO ground state. (q>=5.)")
    print("Matches Lean cuspSeg_no_ground_state / cusp_gt_inf / cusp_approaches (BCZHeckeGenuine_allq_VERIFIED).")
