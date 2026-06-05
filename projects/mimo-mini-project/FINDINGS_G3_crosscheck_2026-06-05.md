# G_3 / PSL(2,Z) cross-check — min-ess-sup extremizer is NOT the Lagrange golden ratio

**Date:** 2026-06-05. Purpose: decide whether the X_Omega(q)=inf_mu ess-sup_mu P phenomenon
coincides with the classical Lagrange-Markov picture (which extremizes over HYPERBOLIC
badly-approximable orbits) or is genuinely different. Triggered by the applications/bridge workflow
(wf_91e91fe3) whose adversarial refuter had deflated the "dynamics<->group bridge" to a re-instance
of Lagrange-Markov. Validated genuine Taha map reused verbatim from `code/Bgoal_taha_genuine.py`.
Scratch driver: `code/g3_crosscheck.py`. Trust-EXIT verified numerics + analytic period-2 argument.

## Result (decisive)

| q | min-ess-sup extremizer            | monodromy trace | type      | attained? | value      |
|---|-----------------------------------|-----------------|-----------|-----------|------------|
| 3 | period-2 family (a,2a), a -> 1/3+ | 2               | PARABOLIC | no (bdy)  | 2/9        |
| 4 | corridor M_(3,1)                  | sqrt2 = lam     | ELLIPTIC  | no        | sqrt2/8    |
| 5 | corridor W_5=[(4,3),(4,0),(2,0)]  | phi  = lam      | ELLIPTIC  | no        | 1/lam^3    |

**The golden-ratio orbit is explicitly REJECTED at q=3.** (phi,phi) is a genuine fixed point of the
q=3 map (k=2, T(phi,phi)=(phi,phi)), monodromy trace=2, with sup-P = phi^2 = 0.38197 — **1.72x worse
than 2/9 = 0.22222**. The classical Lagrange / most-badly-approximable element (hyperbolic, trace 3,
bottom of the Markov spectrum 1/sqrt5 ~ 0.447) is exactly what min-ess-sup does NOT select.

## q=3 structure (exact, analytic)
lam(3)=1, single branch i=2, M_(2,k)=[[0,1],[-1,k]] trace=k. Map T(a,b)=(b, k b - a),
k=floor((1+a)/b), P=a*b. Closed periodic orbit requires det(M_word - I)=0 => trace=2 => ALL closed
q=3 orbits are PARABOLIC words. Minimizing family: (a,2a) <-> (2a,a) [itinerary (2,1),(2,4)],
P=2a^2; inf 2/9 as a->1/3+, non-attained (k flips 4->1 at a=1/3, family breaks at the boundary
b=1-a, the cusp edge). Word M_4 M_1 = [[-1,1],[-4,3]] trace 2 = parabolic.

## What it decides (novelty / bridge)
- Classical Lagrange-Markov extremizes over HYPERBOLIC orbits (golden ratio, 1/sqrt5).
- Our inf-of-ess-sup extremizes over PARABOLIC (q=3) / ELLIPTIC (q>=4) torsion, and REJECTS the
  hyperbolic golden ratio (1.72x worse). Different value, different extremal element type, different
  objective => NOT a re-instance of Lagrange-Markov. The "extremal orbit = distinguished group
  element" bridge holds, but the distinguished element is the slowest elliptic torsion (q>=4) /
  cusp parabolic (q=3), NOT the hyperbolic badly-approximable element. The refuter's deflation is
  answered on this specific point; still "novelty of formulation" within geodesic-coding / triangle
  groups, not a famous-problem result.

## Honest caveats
- q=3 value 2/9 verified ANALYTICALLY (period-2 family P=2a^2 -> 2/9, directly confirmed at 8 a-values);
  random-seed brute search gets 0.248 (misses the rare boundary orbit) — expected, not a contradiction.
- q=4 value sqrt2/8 NOT re-derived from first principles here; only the elliptic mechanism (single-step
  M_(3,1) trace=sqrt2) confirmed. q=4 corridor is likely a longer word analogous to W_5.
- q=3 is the genuine borderline (lam=1, trace exactly 2 = the (2,3,inf) cusp); non-attained for an
  algebraically different reason than q>=4 (boundary cutoff vs no-real-fixed-point rotation). So
  "elliptic at all q" is q>=4 only; q=3 is parabolic/cusp.

## Disposition
No repo logic changed. Validated map untouched. This is a characterization result, numerical +
analytic, supporting the internal write-up's novelty framing (min-ess-sup selects elliptic/parabolic,
not hyperbolic Lagrange). Highest-leverage open follow-ups remain: (a) derive sqrt2/8 q=4 corridor
word; (b) if pursuing the "exact ergodic-optimization benchmark" thread, run a peak-estimation
moment-SOS hierarchy on P at q=5,7 and confirm convergence to 1/lam^3 from below with mass -> cusp.
