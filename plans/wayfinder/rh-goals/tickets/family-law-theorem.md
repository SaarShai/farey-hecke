# LAW: off-line resonances for ALL non-arithmetic Hecke groups — TOP PRIORITY

- status: open — TOP PRIORITY (owner directive 2026-08-16: "aim for a law")
- kind: research (theorem program)
- mode: AFK lanes + frontier gates; HITL only at dissemination
- created: 2026-08-16 (upgrade of family-offline-theorem per owner directive)
- blocked by: none (subsumes family-offline-theorem's q=7 execution, in flight)
- claimed by: lane_f (q=7 leg)

## What "a law" means here (honest scoping)
No finite number of surfaces makes a law. The Hecke family has infinitely
many non-arithmetic members (all q ∉ {3,4,6}), so the law is the UNIFORM
theorem:

> **Every non-arithmetic Hecke group G_q has a Selberg-zeta zero
> (scattering resonance) strictly off the critical line.**

Finite instances (q=5 done, q=7 running) are the *evidence and the
template*; the law needs finitely many certified instances PLUS a uniform
argument covering the infinite tail. The repo already holds the shape of
such a two-part structure: the onset theorem X_Ω(q)=1/λ_q³ is
machine-verified NON-VACUOUSLY for q=5..21 and REDUCED to one interface
residual for q≥22. That is the model to follow.

## Program (ordered)
1. **q=7 certification** — in flight (stages 1–2 certified; 4b fixed,
   ρ̂ ≤ 0.9152; Kaggle launch lane running). Second instance.
2. **Template hardening**: fold the three q=7 lessons (N* decision rule,
   endpoint-B radius coupling, enlargement cap e_B = min(clearance/4,
   0.15R)) back into a q-generic certification pipeline so each further
   instance is a run, not a port. Receipt: a single parametrized runner.
3. **Instance sweep q = 8, 9, 10, 11, 12** (skip arithmetic none — all
   non-arithmetic ≥7 except none; note q=8,9,10,11,12 all non-arithmetic):
   Kaggle-chunked, one surface per ~week of free quota. Gate per surface:
   same 8-link chain as flagship.
4. **Uniform tail argument** (the mathematical heart, frontier + Aristotle):
   prove that for q ≥ Q₀ the certified machinery's gates hold uniformly —
   candidates: (a) uniform Fraczek–Mayer-side asymptotics of the pin
   locations (the empirical pins drift slowly with q); (b) uniform ρ*/ρ̂
   bounds from the λ_q → 2 limit geometry; (c) transplant the onset
   theorem's q≥22 reduction technique. Any one closes the tail.
5. **Assembly**: finite certified base (q ≤ Q₀) + uniform tail = the law.
   Then the paper upgrades from "first instance + template" to "the
   theorem for the family".

## Fallback (still valuable)
If the uniform tail resists: publish the finite-family theorem (q = 5..Q₀
certified) + the dichotomy + the scattering mechanism — already beyond
anything in the literature.

## Receipts
lane_f/ (q=7 chain), lane_g/ (flagship chain + mechanism M1d–M1g),
tickets/family-offline-theorem.md (subsumed instance-level ticket).
