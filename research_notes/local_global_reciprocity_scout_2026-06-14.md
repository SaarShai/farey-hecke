# Local-global / reciprocity-obstruction FALSIFICATION scout — 2026-06-14

VERDICT = PURSUE (sig 8 / object 9 / findability 7). Corrects prior "needs theory partner" caveat.

## Core: the obstruction is a SELF-CERTIFYING FINITE THEOREM (no collaborator)
Apollonian disproof (Haag-Kertzer-Rickards-Stange, Annals 2024, arXiv:2307.02749):
- χ₂ = a Kronecker-symbol invariant, PROVEN CONSTANT across a packing (Cor 4.8) via
  quadratic reciprocity on coprime-tangency paths (Prop 4.4 + Cor 4.7).
- If χ₂ ≡ -1 then square-class curvature families (n², 3n², ...) are ENTIRELY ABSENT
  (Prop 4.2 exclusion). This is a finite algebraic proof from the GENERATORS — Lean/Aristotle-checkable.
- Computation to 10^10–10^12 curvatures is only for the REVISED conj (sporadic set finite, Conj 1.5),
  NOT for the obstruction proof itself. So the prized half (the obstruction) IS the self-certifying half.

## Discovery primitive is CHEAP (our edge)
Given a candidate thin (semi)group / packing: (1) compute χ₂ (Kronecker symbol) on the GENERATORS —
cheap finite check; (2) verify Hausdorff dim > 1/2 — our JP/transfer-op engine native to 1e-15.
Flag χ₂≡-1 on an admissible square class ⇒ NEW obstruction = self-certifying counterexample.

## The enumerable catalogs nobody has systematically searched
1. Kontorovich-Nakamura taxonomy arXiv:1903.03563: FINITELY many superintegral crystallographic
   sphere packings, dim ≤ 20, explicit Coxeter data. Only ~5 have been tested (Apollonian +
   octahedral/cubic/square/triangular, all 2D, arXiv:2510.21702 Oct 2025).
2. Rehwinkel-Whitehead plane-tiling packings arXiv:2302.06202 (symmetry groups fully described).
3. SL(2,Z) finite-alphabet semigroups (Rickards-Stange Duke 2025 arXiv:2401.01860) — disproved
   Bourgain-Kontorovich generalized-Zaremba. Authors: "We expect these reciprocity obstructions
   to exist for many other (thin) (semi)groups" + DID NOT do a systematic search.
   GitHub JamesRickards-Canada/Semigroup-Reciprocity = orbit/missing-integer tools, NO discovery engine.

## Honest NEGATIVE (ruled out, do not chase)
3D Soddy/orthoplicial packings are CLOSED: Nakamura 1401.2980 proves local-global via KLOOSTERMAN's
theorem on quaternary quadratic forms (bend set = single quadratic form ⇒ local=global is a real
theorem; no thin-group obstruction possible). "Overturn a 3D proof" = dead end.
Markoff mod-p connectivity: Chen's theorem (Inventiones 2025, arXiv:2502.15960) ⇒ connected for all
but finitely many p; no known disconnected prime. Likely empty exceptional set — not a findable object.

## First experiment
Port χ₂ (Kronecker-symbol) computation to our exact-arith stack; run it on the FULL Kontorovich-Nakamura
taxonomy generators (finite list) + a swept SL(2,Z) alphabet family. Any χ₂≡-1 on a square class with
dim>1/2 (JP-certified) and no congruence explanation = NEW self-certifying obstruction. Cross-check the
two Apollonian-open types (6,1,1,1) and (8,11,1) for a missed higher-power (quartic/octic) obstruction.
