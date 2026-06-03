# Route 3 (genuine (C′) assembly) — verification verdict

**Date:** 2026-06-03 (orchestrated agent + independent verification). **Verdict: VERIFIED Lean assembly,
but it does NOT close `X_Ω(q)≥1/λ³` — wrong (overestimating) observable.** Honest record.

## What was produced + verified (HARD RULE: re-compiled /tmp/lean-minus1, EXIT=0, no sorryAx)
`lean/BCZHeckeGenuineAssembly_qge18_VERIFIED.lean` — 11 theorems, all axioms
`[propext,Classical.choice,Quot.sound]`. The (C′)→engine logical chain is genuinely machine-checked:
`essSup_ge_of_no_sustained(_strict)` (engine), `infinitely_many_high_floor`+`no_infinite_rotation` (L1,
reused), `cusp_envelope` (reused), and the new glue `genuine_no_sustained_scalar` (sub-threshold ⟹ all
floors=1 ⟹ contradicts infinitely_many_high_floor — a CORRECT, clean proof), `essSup_genuine_ge(_via_cusp)`.

**STRENGTHENED this verification:** the assembly's key hypothesis `hkick` ("K≥2 ⟹ Pgen≥1/λ³") is a PURE
ALGEBRAIC inequality — proven unconditionally as `lean/BCZHeckeKickPureAlgebra_VERIFIED.lean` `kick_pure`
(EXIT=0, axiom-clean): for `l²≥3` (q≥7), `0<a,0<b, a+lb>1, 2lb≤1+a ⟹ a(a+lb)/l ≥ 1/l³`. Chain:
domain `lb>1−a` + K≥2 `2lb≤1+a` ⟹ `a>1/3` ⟹ `a(a+lb)>a>1/3≥1/l²`. So `hcuspAtKick` is NOT needed.

## Why it does NOT close X_Ω (the catch — found by independent verification)
The observable is `Pgen(a,b)=a(a+lb)/l` (the cusp-branch FORM). But the genuine gap-product `P=a·L_i/x_{i-1}`
is BRANCH-DEPENDENT; on the scalar branch `P=ab`, and `Pgen−P = a²/l > 0`. **Numerically `Pgen ≥ P_actual`
at 100% of genuine points (q=18,30).** Since `Pgen≥P`, `essSup Pgen ≥ essSup P`, so the proven
`1/λ³ ≤ essSup Pgen` does NOT give `1/λ³ ≤ essSup P` — wrong direction for the lower bound
`X_Ω=inf_μ essSup P`. The pure-algebra kick works for `Pgen` PRECISELY because it is the overestimate;
for the real product `ab` the high-floor step itself can be sub-threshold (verified earlier: q=30 K=2 step
had `ab≈0.118<thr`), which is exactly why the real observable needs the WINDOW argument (routes 1/2), not
a per-step kick.

## Net
- REUSABLE (verified): `kick_pure` (clean algebraic lemma), `essSup_ge_of_no_sustained_strict` (strict
  engine variant), the assembly skeleton.
- DEAD END as a close: the per-step-kick structure does not transfer to the real gap-product observable.
- The real q≥18 closes use the ACTUAL product `c_n c_{n+1}`: the uniform floor-1 window inequality
  (route 1), the per-q window certs (route 2), and Aristotle's `scalar_no_sustained_below` (route 4) —
  all on the right observable.
- Lesson (re-confirmed): a file that COMPILES can still not prove the intended theorem — independent
  verification of the STATEMENT (observable, direction) is as essential as the axiom check.
