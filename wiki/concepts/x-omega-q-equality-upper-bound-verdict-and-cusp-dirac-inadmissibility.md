---
schema_version: 2
title: "X_Omega(q) equality upper bound — verdict and cusp-Dirac inadmissibility"
type: concept
domain: "hecke-ergodic-optimization"
tier: semantic
confidence: 0.8
trust: verified
created: "2026-06-14"
updated: "2026-06-14"
verified: "2026-06-14"
sources:
  - "research_notes/equality_upperbound_2026-06-14.md"
  - "projects/aristotle_dispatch_v15/uniform_q5to18/EqualityUpperBound.lean"
supersedes: []
superseded-by:
contradicts: []
tags: [hecke, BCZ, Xomega, ergodic-optimization, cusp, lean, upper-bound, ground-state]
---

# X_Omega(q) equality upper bound — verdict and cusp-Dirac inadmissibility

## Summary

The verified Hecke uniform-onset footprint is the LOWER bound `X_Ω(q) ≥ 1/λ_q³` ONLY
(`UniformOnset_q5to18.Xomega_lb_q5to18` + `GenuineMapFacts.Xomega_lb_q5to21`, q∈{5,7,8,…,21},
axiom-clean). The EQUALITY `X_Ω(q) = 1/λ³` is NOT machine-verified for any q, and CANNOT be
closed by the proposed cusp-tip Dirac witness in the engine's measure class.

## Evidence

The proposed matching upper-bound witness — the cusp-tip Dirac `δ_{(1/λ,0)}` ("ground state")
— is INADMISSIBLE in the exact lower-bound class, machine-checked THREE ways in
`projects/aristotle_dispatch_v15/uniform_q5to18/EqualityUpperBound.lean` (capstone
`cusp_dirac_inadmissible`, axiom-clean `[propext, Classical.choice, Quot.sound]`, build EXIT 0):

- (O1) WRONG OBSERVABLE — the lower bound uses `Pprod = a·b`, and `Pprod(s,0)=0 < 1/λ³`
  (the `1/λ³` corner value is for the GENUINE observable `Pgen = a(a+λb)/λ`, a different function).
- (O2) WRONG DOMAIN — `Dcorr` requires `0<b` strictly, the cusp tip has `b=0`, so `δ(Dcorrᶜ)=1≠0`.
- (O3) WRONG MAP — the scalar `Tmap(s,0)=(0,−s)≠(s,0)`, so the Dirac is not `Tmap`-invariant.

This obstruction holds because the cusp Dirac IS admissible for a DIFFERENT engine (the genuine
map `Tcusp` on the Taha domain with observable `Pgen` — verified in
`BCZHeckeCuspNonVacuity_VERIFIED.lean`), but that triple (`Pgen`/`Taha`/`Tcusp`) is not the
lower-bound statement (`Pprod`/`Dcorr`/`Tmap`), so it does not discharge an upper bound. The
verdict is recorded in order to keep the published claim honest: the verified result is `≥`,
not `=`.

## Open Questions

- For q≥5, is the infimum equal to `1/λ³` (approached, unattained) or strictly greater? The
  engine proves only `¬(∀n, P<1/λ³)` (no orbit stays strictly below) → `≥`, not strict. A
  strict "no ground state" (`essSup>1/λ³`, infimum unattained) is verified only for q=3,4
  (`BCZHecke_noGroundState_q3q4_VERIFIED.lean`: `no_ground_state`, `g4_no_ground_state` via
  `not_two_ninths_at` / `g4_not_t_at`) and is NOT yet generalized to q≥5.
- Non-vacuity of the q≥5 `Dcorr` invariant-measure class is delicate (orbits barely stay in
  Dcorr for large q; audit Front 1d).

## Related

- [[index]]
- [[concepts/track-c-extremal-index-theta-q-for-bcz-extreme-gap-process]]
