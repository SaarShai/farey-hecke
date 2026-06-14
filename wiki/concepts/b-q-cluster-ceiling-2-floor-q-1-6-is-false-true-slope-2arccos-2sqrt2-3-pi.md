---
schema_version: 2
title: "B(q) cluster ceiling: 2+floor((q-1)/6) is FALSE; true slope 2arccos(2sqrt2/3)/pi"
type: concept
domain: "hecke-bcz"
tier: semantic
confidence: 0.9
trust: verified
created: "2026-06-14"
updated: "2026-06-14"
verified: "2026-06-14"
sources: []
supersedes: []
superseded-by:
contradicts: []
tags: [cluster, Bq, hecke, formula-false, rotation, chebyshev, arithmeticity]
---

# B(q) cluster ceiling: 2+floor((q-1)/6) is FALSE; true slope 2arccos(2sqrt2/3)/pi

## Summary

The conjectured last-branch cluster ceiling `B(q) = 2 + floor((q-1)/6)` for the Taha
G_q-BCZ map is **FALSE as a uniform law**. It is exact only on the calibration window
q=7..22 (where it was fit); it **undershoots by +1** at q=5,23,24,29,30,33-36,39-41 and
systematically for large q. The true asymptotic slope is `s = 2*arccos(2*sqrt2/3)/pi
= 0.216347` (period 1/s = 4.622), **not** 1/6 = 0.1667. So `B(q) ~ 2 + 0.2163*q`.

## Evidence

- **Exact algebraic witnesses** (sympy `is_positive` over Q(lambda_q), ZERO float in any
  threshold decision; `/tmp/exact_witness_strict.py`): certified last-branch sub-X clusters
  STRICTLY LONGER than the formula:
  - q=5: len 3 (formula 2), entry (7/17,8/17) or (3/5,1/3)
  - q=23: len 6 (formula 5), entry (100/303,35/101) [repo's OWN committed witness]
  - q=24: len 6 (formula 5), entry (43/130,9/26)
  - q=30: len 7 (formula 6), entry (29/87,30/87)
  - q=40: len 9 (formula 8), entry (39/117,40/117)
- **Two independent deterministic full-grid sweeps** (local + M1, mpmath dps=50, exact-floor
  full map) agree on B(q) for q=5..41 and confirm the failure set.
- **Mechanism (the Chebyshev/rotation hint, corrected slope):** the longest cluster is
  internally **pure k=1** (verified all q>=7) where the last-branch map is the LINEAR
  rotation M=[[0,1],[-1,lambda]], trace lambda=2cos(pi/q), so a_n = R*cos(n*theta+delta),
  theta=pi/q, solving exactly a_{n+1}=lambda*a_n - a_{n-1} (Chebyshev U). The run = #
  consecutive rotation steps inside the slab `1/3 < a < 1/(2*sqrt2)`, ended by a k=2
  ejection step. Optimal amplitude R=1/(2sqrt2) puts the slab at the turning point ->
  angular half-width phi* = arccos((1/3)/(1/(2sqrt2))) = arccos(2sqrt2/3); run ~
  2*phi*/theta = (2*arccos(2sqrt2/3)/pi)*q. Slab endpoints confirmed empirically
  (q=40 cluster a in [0.3310, 0.3545] -> (1/3, 0.35355)).
- **Arithmetic floor (UNCHANGED and correct):** B(q)=2 <=> lambda^2 in Z <=> q in {3,4,6}
  (Takeuchi finite arithmetic Hecke groups; lambda^2 = 1,2,3). Verified exactly. This is
  the ONLY place arithmeticity enters; for q>=5 NO arithmetic invariant tracks B(q)
  (degree [Q(lambda^2):Q] oscillates while B grows).
- **No clean closed form:** no `floor(linear)` is exact everywhere (best empirical
  floor(q/4.68+0.95) = 28/36; rotation-floor 2+floor(s(q-2)) = 16/36). The staircase step
  positions are a Diophantine/three-distance phenomenon (where the lattice n*pi/q lands vs
  the slab edges), not a single floor formula.

## Why this corrects prior records

The repo's `exp_Bformula_2026-06-12.md`, `goal1.5_uniform_obstruction.md`, and
`goal1_last_branch_ceiling.py` all carried `2+floor((q-1)/6)` as the cleanest fit and
recorded slope ~1/6. They were honest that it was a [CONJECTURE]/empirical-bulk-fit, but
the slope claim 1/6 is **wrong asymptotically** because the calibration window q<=24 was
too short to see the true slope ~0.216 (the +1 failures only become dense for q>=29). The
upper bound B(q) <= formula was never proved (Monte-Carlo only) and is now refuted.

## Related

- [[concepts/track-c-extremal-index-theta-q-for-bcz-extreme-gap-process]]
- [[index]]

## Open Questions

- Exact closed form for the integer staircase B(q) (likely a Beatty/3-distance expression
  in pi/q, not floor(linear)).
- Rigorous uniform UPPER bound proof: needs (a) confine in-cluster points to the slab and
  k=1 regime, (b) the rotation step-count bound, (c) rule out k>=2 mid-cluster extension.
