import Mathlib

/-!
# The LAW — statement skeleton and the divergence core (v33 dispatch, rung 1)

Source of record:
`research_notes/rh_goals_2026-08-14/lane_g/LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`
(§4.1–§4.3, §5, and the 2026-08-19 promotion block), double-audited by
`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_REFEREE.md` (first referee) and
`LAW_SECOND_AUDIT_REFEREE.md` (cold, independent lineage; verdict
**CONFIRMED**, mathematical statement only).

The promoted paper-level theorem is:

> For every finite integer `q ≥ 3`, the scalar trivial-character scattering
> determinant `φ_q` of the one-cusp Hecke triangle orbifold has infinitely
> many nonreal zeros `ρ` with `Re ρ > 1/2`, hence infinitely many
> multiplicity-matched poles `1 - ρ` with `Re (1 - ρ) < 1/2`.

## What this file is

This is the **first rung** of the formalization ladder. It formalizes the
*combinatorial / real-analytic finish* of that proof — the step

    growth of the weighted Jensen count  +  finiteness of the real zeros
      ⟹  infinitely many strictly-off-line zeros, and their reflections —

together with the small explicit-constant lemmas the second audit had to
verify by hand. It does **not** formalize any spectral theory, any
meromorphic continuation, any Jensen/Littlewood rectangle, or any property
of `φ_q` itself. Those enter only as **named hypotheses** `H1`–`H5`
(see `DISPATCH.md` §2), in exactly the v32 `hconv`/`hford` style.

`φ_q` has no Lean definition in this dispatch, and deliberately so: the zero
family is an abstract predicate `Zero : ℂ → Prop` and the weighted count is an
abstract function `F : ℝ → ℝ` constrained by hypotheses. Proving the targets
below proves the *finish*, and nothing about the orbifold.

## LEDGER RULE

Nothing is stated more strongly than the second audit confirmed.

* No `q`-uniformity, no effective first height, no explicit `A_q`: the
  audit's promotion block certifies none of these, and none appear here.
* The growth input is used in the weak `O_q(T²)` form of the promotion block
  (`F_q(1/2,T) = (1/4π) T² log T + O_q(T²)`), **not** the sharper `(C)`
  asymptotic — the audit records that the weak form is strictly more robust.
* `Section 4` records the audit's own arithmetic corrections to Kelmer's
  printed constants. The corrected values are stated; Kelmer's printed
  `B_Γ` is stated only as a *disequality* target. Neither `A_q`, `B_q` nor
  `C_q` is consumed anywhere in Sections 1–3.
* No arithmeticity content. The second audit (attack 5b) records that the
  "in particular, nonarithmetic" clause carries **zero** arithmeticity
  information (`q = 3` has the same property). Nothing in this file mentions
  arithmeticity, and nothing here may be used as an arithmeticity signature.

Everything below with a `sorry` body is **CONJECTURAL at the Lean level**.
This file machine-verifies nothing.

## FALSE-statement escape hatch

If a requested target is false, do **not** force an inconsistent proof.
Retain the original statement only inside a `FALSE AS STATED` comment, prove a
named `<target>_false` negation with an exact witness, then state and prove
the weakest corrected theorem, and report the downstream status change.
Same convention as v30/v32.
-/

namespace LawSkeletonI

open scoped BigOperators

/-! ## 0. The abstract model

`Zero ρ` stands for "`ρ` is a zero of `φ_q`, counted without multiplicity".
`RightZeros` is the right half-plane zero set of the source note's `F_{q,1}`.
`weight ρ = Re ρ - 1/2` is the Jensen weight `(β - α)` at `α = 1/2`.

Multiplicity is deliberately dropped: the LAW asserts *infinitely many*
zeros, and an infinite set of distinct points is the weaker, safer reading.
A multiplicity-weighted version would be a strictly stronger statement than
the audit confirmed for a set-level conclusion. -/

/-- The Jensen weight at `α = 1/2`. -/
noncomputable def weight (ρ : ℂ) : ℝ := ρ.re - 1 / 2

/-- The right half-plane zero set. -/
def RightZeros (Zero : ℂ → Prop) : Set ℂ := {ρ | Zero ρ ∧ 1 / 2 < ρ.re}

/-! ### Locally proved scaffolding (no LAW content, no `sorry`) -/

theorem weight_pos {ρ : ℂ} (h : 1 / 2 < ρ.re) : 0 < weight ρ := by
  simpa [weight] using sub_pos.mpr h

theorem weight_nonneg {ρ : ℂ} (h : 1 / 2 ≤ ρ.re) : 0 ≤ weight ρ := by
  simpa [weight] using sub_nonneg.mpr h

theorem mem_RightZeros_iff {Zero : ℂ → Prop} {ρ : ℂ} :
    ρ ∈ RightZeros Zero ↔ Zero ρ ∧ 1 / 2 < ρ.re := Iff.rfl

/-! ## 1. Rung group A — the divergence core

This is the mathematical content of `LAW_..._SOL.md` §5 together with the
promotion block's shorter triangular argument: a *finite* right zero set can
only make the weighted count `O(T)`, while the growth input makes it
`≫ T² log T`. -/

/-- **Target A1** (the divergence engine).

For every `a > 0` and all reals `C`, `M`, the function `a T² log T` eventually
beats `C T² + M T`. This is the exact quantitative content of the promotion
block sentence *"finitely many total right zeros would make the defining sum
only `O_q(T)`"*, with `C T²` absorbing the `O_q(T²)` error.

Self-contained real analysis. No LAW content. -/
theorem growth_beats_quadratic_target (a C M : ℝ) (ha : 0 < a) :
    ∃ T : ℝ, 1 ≤ T ∧ C * T ^ 2 + M * T < a * T ^ 2 * Real.log T := by
  sorry

/-- **Target A2** (finite families are `O(T)`).

If the right zero set is a finite set `S` with nonnegative weights, the
weighted Jensen sum `∑ (T - |Im ρ|) w ρ` over any subfamily is at most
`T · ∑_{S} w`. This is the "bounded independently of `T`" step of §5, made
exact.

Self-contained finite-sum inequality. No LAW content. -/
theorem finite_family_linear_bound_target
    (S : Finset ℂ) (w : ℂ → ℝ) (hw : ∀ ρ ∈ S, 0 ≤ w ρ)
    (S' : Finset ℂ) (hS' : S' ⊆ S) (T : ℝ) (hT : 0 ≤ T)
    (him : ∀ ρ ∈ S', |ρ.im| ≤ T) :
    ∑ ρ ∈ S', (T - |ρ.im|) * w ρ ≤ T * ∑ ρ ∈ S, w ρ := by
  sorry

/-- **Target A3** — *the LAW's statement skeleton*.

Hypotheses, and what each stands for (see `DISPATCH.md` §2):

* `Zfin T` — the finite truncation of the right zero set at height `T`,
  with the membership characterization `hZfin`. This is bookkeeping, not an
  analytic input.
* `hFdef` — the *definition* of the weighted Jensen count `F_q(1/2, T)`
  of `LAW_..._SOL.md` §4.1. Definitional, not an analytic import.
* **`H3` = `hgrowth`** — the analytic import. It is the promotion block's
  `F_q(1/2,T) = (1/4π) T² log T + O_q(T²)`, used only in its lower-bound
  half. This is the Jensen/Littlewood rectangle `(J)` composed with the
  critical-line integral `(I)`; it is **NOT** proved here and must not be
  proved here.

Conclusion: the right zero set is infinite.

This is the theorem the LAW rests on, with the analytic content quarantined
into `hgrowth`. -/
theorem law_right_zeros_infinite_target
    (Zero : ℂ → Prop) (F : ℝ → ℝ) (Zfin : ℝ → Finset ℂ)
    (hZfin : ∀ T : ℝ, 1 ≤ T → ∀ ρ : ℂ,
      ρ ∈ Zfin T ↔ (ρ ∈ RightZeros Zero ∧ |ρ.im| ≤ T))
    (hFdef : ∀ T : ℝ, 1 ≤ T →
      F T = ∑ ρ ∈ Zfin T, (T - |ρ.im|) * weight ρ)
    -- H3, the analytic import: the `O_q(T²)` growth of the promotion block.
    (hgrowth : ∃ C : ℝ, ∀ T : ℝ, 1 ≤ T →
      (1 / (4 * Real.pi)) * T ^ 2 * Real.log T - C * T ^ 2 ≤ F T) :
    (RightZeros Zero).Infinite := by
  sorry

/-! ## 2. Rung group B — strictness, nonreality, and the reflection

`LAW_..._SOL.md` §5 plus second-audit attacks 4a and 4b. -/

/-- **Target B1** (strictness — attack 4a, forcing (i)).

A zero on the line contributes weight exactly `0`. Hence a divergent weighted
sum forces `Re ρ > 1/2` **strictly**; membership in `RightZeros` already
carries this, so the target records the contrapositive fact that the weight
detects strictness. -/
theorem weight_eq_zero_iff_target (ρ : ℂ) :
    weight ρ = 0 ↔ ρ.re = 1 / 2 := by
  sorry

/-- **Target B2** (nonreality — §5 / attack 4b).

**`H4` = `hreal_finite`**: FJS/Hejhal give only *finitely many real* zeros of
`φ_q` in `Re s > 1/2`. That is a literature import, carried as a hypothesis.
Given it, an infinite right zero set has infinitely many members off the real
axis. -/
theorem nonreal_right_zeros_infinite_target
    (Zero : ℂ → Prop)
    (hinf : (RightZeros Zero).Infinite)
    -- H4, literature import.
    (hreal_finite : {ρ ∈ RightZeros Zero | ρ.im = 0}.Finite) :
    {ρ ∈ RightZeros Zero | ρ.im ≠ 0}.Infinite := by
  sorry

/-- **Target B3** (the reflection arithmetic — §5).

`Re (1 - ρ) < 1/2` exactly when `Re ρ > 1/2`, and `Im (1 - ρ) = -Im ρ`, so
nonreality is preserved. Elementary; it is the half of §5 that does not
consume the functional equation. -/
theorem reflection_strict_left_target (ρ : ℂ) :
    ((1 : ℂ) - ρ).re < 1 / 2 ↔ 1 / 2 < ρ.re := by
  sorry

/-- **Target B4** (reflection preserves nonreality). -/
theorem reflection_nonreal_target (ρ : ℂ) (h : ρ.im ≠ 0) :
    ((1 : ℂ) - ρ).im ≠ 0 := by
  sorry

/-- **Target B5** — *the LAW's conclusion skeleton*.

**`H5` = `hpole`**: the functional equation `φ_q(s) φ_q(1-s) = 1` turns an
order-`m` zero at `ρ` into an order-`m` pole at `1 - ρ`. That is the one
analytic fact §5 uses, and it is carried as an abstract hypothesis relating
two predicates.

Conclusion: infinitely many poles, each strictly left of the critical line
and off the real axis. -/
theorem law_offline_poles_infinite_target
    (Zero Pole : ℂ → Prop)
    (hinf : {ρ ∈ RightZeros Zero | ρ.im ≠ 0}.Infinite)
    -- H5, functional-equation import.
    (hpole : ∀ ρ, ρ ∈ RightZeros Zero → Pole (1 - ρ)) :
    {s : ℂ | Pole s ∧ s.re < 1 / 2 ∧ s.im ≠ 0}.Infinite := by
  sorry

/-! ## 3. Rung group C — the critical-line leading coefficient

`LAW_..._SOL.md` §4.2 and second-audit attack 2c. Only the *elementary
calculus* half is requested; the gamma-quotient modulus is a separate,
clearly-flagged optional rung. -/

/-- **Target C1** (the displayed identity of §4.2).

`2 ∫₀^T (T - t) log t dt = T² log T - (3/2) T²`.

This is the identity from which the audit re-derived the `1/(4π)` leading
coefficient (attack 2c, verdict SOUND). Pure calculus. -/
theorem jensen_leading_integral_target (T : ℝ) (hT : 0 < T) :
    2 * (∫ t in (0 : ℝ)..T, (T - t) * Real.log t)
      = T ^ 2 * Real.log T - (3 / 2) * T ^ 2 := by
  sorry

/-- **Target C2** (OPTIONAL, hardest rung — the gamma quotient, `(GT)`).

`|Γ(1/2 + it) / Γ(it)|² = |t| tanh (π |t|)`.

Used in §4.2 to get the `1/2 · log|t|` critical-line behaviour, and the exact
identity the audit used to catch Kelmer's spurious `/π` (finding C). It is
self-contained special-function algebra but is expected to be the most
expensive target here; prefer the other rungs first. -/
theorem gamma_quotient_modulus_target (t : ℝ) (ht : t ≠ 0) :
    ‖Complex.Gamma (1 / 2 + t * Complex.I) / Complex.Gamma (t * Complex.I)‖ ^ 2
      = |t| * Real.tanh (Real.pi * |t|) := by
  sorry

/-! ## 4. Rung group D — the second audit's constant corrections

`LAW_SECOND_AUDIT_REFEREE.md` finding C. These are stated because the audit
found **two** printed-constant errors in Kelmer and verified the corrections
numerically; machine-checking the algebra retires the numerics.

None of `A_q`, `B_q`, `C_q` is consumed by Sections 1–3. These rungs are
ledger hygiene, not LAW dependencies. -/

/-- **Target D1** (the finite-difference expansion, `(DIF)` step of §4.3).

`(T+1)² log(T+1) - T² log T = 2T log T + T + O(log T)`.

This is the expansion the audit used to show that the `D` (linear) coefficient
cancels in `F(T+1) - F(T)`. -/
theorem finite_difference_leading_target :
    ∃ c : ℝ, ∀ T : ℝ, 1 ≤ T →
      |((T + 1) ^ 2 * Real.log (T + 1) - T ^ 2 * Real.log T)
        - (2 * T * Real.log T + T)| ≤ c * (1 + Real.log T) := by
  sorry

/-- **Target D2** (`A = a + 2B`, and `D` cancels — audit finding C).

If `F T = a T² log T + B T² + D T + r T` with `|r T| ≤ K (1 + log T)`, then
`F(T+1) - F T = 2a T log T + (a + 2B) T + O(log T)`.

Note that `D` — which in Kelmer carries `C_Γ` and the pole sum — cancels
exactly. This refutes Kelmer's printed post-(4.22) formula
`A_Γ = 2(C_Γ + Σ(σ_j - α)) + B_Γ`. -/
theorem constant_A_eq_a_add_two_B_target
    (a B D K : ℝ) (F r : ℝ → ℝ)
    (hF : ∀ T : ℝ, 1 ≤ T → F T = a * T ^ 2 * Real.log T + B * T ^ 2 + D * T + r T)
    (hr : ∀ T : ℝ, 1 ≤ T → |r T| ≤ K * (1 + Real.log T)) :
    ∃ c : ℝ, ∀ T : ℝ, 1 ≤ T →
      |(F (T + 1) - F T) - (2 * a * T * Real.log T + (a + 2 * B) * T)|
        ≤ c * (1 + Real.log T) := by
  sorry

/-- **Target D3** (the corrected numeric chain at `d = 2, κ = 1`).

With the *true* `B = (-2 log π - 3)/(8π)` and `a = 1/(4π)`, the audit's
`A = a + 2B` equals `-(1 + log π)/(2π)`, which is the Riemann–von Mangoldt
value at `q = 3`. Pure field arithmetic. -/
theorem corrected_A_value_target :
    (1 / (4 * Real.pi)) + 2 * ((-2 * Real.log Real.pi - 3) / (8 * Real.pi))
      = -(1 + Real.log Real.pi) / (2 * Real.pi) := by
  sorry

/-- **Target D4** (Kelmer's printed `B_Γ` is *not* the true `B`).

Kelmer's printed `B_Γ = (-4 log π - 1)/(8π)` differs from the corrected
`B = (-2 log π - 3)/(8π)`; they agree only if `log π = 1`, i.e. `π = e`.
Stating the disequality makes the ledger warning machine-checked: nobody may
consume `B_q` from that paper. -/
theorem kelmer_printed_B_ne_true_B_target :
    (-4 * Real.log Real.pi - 1) / (8 * Real.pi)
      ≠ (-2 * Real.log Real.pi - 3) / (8 * Real.pi) := by
  sorry

end LawSkeletonI
