---
schema_version: 2
title: "Track-C extremal index theta_q for BCZ extreme-gap process"
type: concept
domain: "hecke-bcz"
tier: semantic
confidence: 0.7
trust: verified
created: "2026-06-14"
updated: "2026-06-14"
verified: "2026-06-14"
sources: []
supersedes: []
superseded-by:
contradicts: []
tags: [extremal-index, EVT, BCZ, hecke, cluster, theta, parabolic, cusp]
---

# Track-C extremal index theta_q for BCZ extreme-gap process

## Summary

EVT-for-dynamics of the Taha G_q-BCZ map, observable P = gap-product (a*b on last
branch; gap ~ 1/P, so small-P = LARGE Farey gap). The rare event is {P < u}.

VERDICT: the hoped-for lambda_q-dependent exactly-solvable theta_q family is
FALSIFIED. The genuine LIMITING extremal index is theta_q = 1/2 for ALL q >= 4
(no lambda_q), because extreme gaps come in deterministic period-2 cusp-swap PAIRS.
The limiting cluster-size distribution is a point mass at L=2. The lambda_q
dependence only appears at the FINITE onset threshold u=X(q)=1/lambda^3, where the
cluster ratio is q-dependent but has NO clean elementary closed form (q>=4).

## Evidence

- Mechanism (analytic): on last branch M(a,b)=(b,-a+k*lambda*b). A point a~1,b~0
  (P=ab small) has large k; image is (b, k*lambda*b-a) with k*lambda*b~1+a~2 so
  b'~1 => image (b,~1) also has small P=b. Its image has a''~1 (large) => generic
  escape. So the cluster is exactly the swap-PAIR, coordinate-universal => theta=1/2.
- Numerics (proper invariant-domain sampling — see PITFALL): theta(u)=1-pi2(u)/pi(u)
  -> 1/2 monotonically as u->0 for q=3..7. At u=0.05 the finite-u correction is
  lambda-ordered (q3..7: 0.509,0.513,0.515,0.517,0.518) but the LIMIT is 1/2.
- Finite onset-threshold u=X(q) (high-stat, SE~2e-5):
  q=3: theta=0.564121 E[L]=1.77267 Pr(L1)=0.2273 Pr(L2)=0.7727 Pr(>=3)=0
  q=4: theta=0.592285 E[L]=1.68838 Pr(L1)=0.3116 Pr(L2)=0.6884 Pr(>=3)=0
  q=5: theta=0.592364 E[L]=1.68815 Pr(L1)=0.3372 Pr(L2)=0.6375 Pr(>=3)=0.0253
- q=3 ONLY clean closed form (uniform density f=2 on Farey triangle):
  exceedance prob pi_3 = Pr(P<2/9) = (8 ln(3/2)-2)/9 = 0.13819120720725722 (verified).
  theta_3 = 1 - pi2_3/pi_3, pi2_3 = 0.060223 (P(two consecutive exceedances);
  per-k floor-region dilog integral, NO elementary closed form; PSLQ vs
  {1,ln2,ln3,ln(3/2),pi^2,Li2(1/3,2/3,1/2,1/9,-1/2)} found only the trivial
  ln(3/2)+ln2-ln3=0 with pi2-coeff 0 => pi2 not in that span).
- Near-misses RULED OUT (gap >> SE): theta_4=0.592285 vs 16/27=0.592593 (15 sigma);
  E[L]_4=1.68838 vs 27/16=1.68750. NOT exact.
- q=3 is degenerate for the limit: P=ab lower-tail has O(u^2) measure (lambda=1),
  orbit Pmin~0.09; the parabolic edge is not reached the same way as q>=4.
- Repro scripts: code/goal1_bcz_hecke_cluster.py (exact Taha G_q-BCZ map);
  code/cluster_size_distribution_at_threshold.py (q=3 numerics, but note its
  start-point convention); /tmp/onset_theta_hi.py + /tmp/theta_extrap.py (this run).

## PITFALL (cost me a wrong intermediate result)

Starting the BCZ orbit at a FIXED point like (0.5, 0.9) lands on a degenerate
periodic-ish orbit that does NOT sample the invariant measure: it reports
theta=1/2, Pr(L=2)=1 at EVERY threshold (even u=2/9), masking the true ergodic
average. ALWAYS reject-sample the initial (a,b) from the invariant domain
{0<a<=1, 1-lambda*a<b<=1} (q=3: {x+y>1}). With proper sampling theta_3(2/9)=0.5641,
matching the stored 5e9 JSON, not 0.5.

## Related

- [[index]]
- [[schema]]

## Open Questions

- Rigorous REPP (rare-event point process) limit theorem for the parabolic,
  polynomial-mixing G_q-BCZ cross-section confirming theta=1/2 and the compound
  Poisson limit. This is the HARD step (cf. Freitas-Freitas-Todd periodic theory,
  but the cusp is PARABOLIC not repelling so standard |D| formula gives 0).
- Closed form (dilog) for the finite onset cluster ratio at u=X(q), q>=4 — open.
