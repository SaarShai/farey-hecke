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

**Status update.** No `sorry` bodies remain: every target A1–A3, B1–B5, C1,
C2 and D1–D4 is now proved, with the named hypotheses `hgrowth`
(`H3`), `hreal_finite` (`H4`) and `hpole` (`H5`) left as hypotheses exactly
as dispatched. The statements were not weakened, strengthened, or stripped of
any hypothesis.

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
  set K : ℝ := (|C| + |M| + 1) / a with hK
  have hKpos : 0 < K := by
    apply div_pos _ ha
    have := abs_nonneg C; have := abs_nonneg M; linarith
  refine ⟨Real.exp K, Real.one_le_exp hKpos.le, ?_⟩
  set T := Real.exp K with hT
  have hT1 : 1 ≤ T := Real.one_le_exp hKpos.le
  have hlog : Real.log T = K := Real.log_exp K
  have haK : a * K = |C| + |M| + 1 := by
    rw [hK]; field_simp
  have hC : C ≤ |C| := le_abs_self C
  have hM : M ≤ |M| := le_abs_self M
  have hT2 : T ≤ T ^ 2 := by nlinarith
  rw [hlog]
  nlinarith [abs_nonneg C, abs_nonneg M, sq_nonneg T,
    mul_le_mul_of_nonneg_right hC (by positivity : (0:ℝ) ≤ T ^ 2),
    mul_le_mul_of_nonneg_right hM (by linarith : (0:ℝ) ≤ T)]

/-- **Target A2** (finite families are `O(T)`).

If the right zero set is a finite set `S` with nonnegative weights, the
weighted Jensen sum `∑ (T - |Im ρ|) w ρ` over any subfamily is at most
`T · ∑_{S} w`. This is the "bounded independently of `T`" step of §5, made
exact.

Self-contained finite-sum inequality. No LAW content.

Note: the hypothesis `him` (the height truncation `|Im ρ| ≤ T` on `S'`) turned
out not to be needed — the bound follows from `0 ≤ |Im ρ|` alone — but it is
kept because it is part of the dispatched statement. -/
theorem finite_family_linear_bound_target
    (S : Finset ℂ) (w : ℂ → ℝ) (hw : ∀ ρ ∈ S, 0 ≤ w ρ)
    (S' : Finset ℂ) (hS' : S' ⊆ S) (T : ℝ) (hT : 0 ≤ T)
    (him : ∀ ρ ∈ S', |ρ.im| ≤ T) :
    ∑ ρ ∈ S', (T - |ρ.im|) * w ρ ≤ T * ∑ ρ ∈ S, w ρ := by
  have h1 : ∑ ρ ∈ S', (T - |ρ.im|) * w ρ ≤ ∑ ρ ∈ S', T * w ρ := by
    refine Finset.sum_le_sum ?_
    intro ρ hρ
    have hwρ : 0 ≤ w ρ := hw ρ (hS' hρ)
    nlinarith [abs_nonneg ρ.im]
  have h2 : ∑ ρ ∈ S', T * w ρ ≤ ∑ ρ ∈ S, T * w ρ := by
    refine Finset.sum_le_sum_of_subset_of_nonneg hS' ?_
    intro ρ hρ _
    exact mul_nonneg hT (hw ρ hρ)
  have h3 : T * ∑ ρ ∈ S, w ρ = ∑ ρ ∈ S, T * w ρ := Finset.mul_sum S w T
  linarith

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
  obtain ⟨C, hC⟩ := hgrowth
  intro hfin
  set S : Finset ℂ := hfin.toFinset with hS
  have hwS : ∀ ρ ∈ S, 0 ≤ weight ρ := by
    intro ρ hρ
    rw [hS, Set.Finite.mem_toFinset] at hρ
    exact weight_nonneg hρ.2.le
  set M : ℝ := ∑ ρ ∈ S, weight ρ with hM
  obtain ⟨T, hT1, hlt⟩ :=
    growth_beats_quadratic_target (1 / (4 * Real.pi)) C M (by positivity)
  have hT0 : (0:ℝ) ≤ T := by linarith
  have hsub : Zfin T ⊆ S := by
    intro ρ hρ
    rw [hS, Set.Finite.mem_toFinset]
    exact ((hZfin T hT1 ρ).mp hρ).1
  have him : ∀ ρ ∈ Zfin T, |ρ.im| ≤ T := fun ρ hρ => ((hZfin T hT1 ρ).mp hρ).2
  have hbound :=
    finite_family_linear_bound_target S weight hwS (Zfin T) hsub T hT0 him
  rw [← hFdef T hT1] at hbound
  have hgr := hC T hT1
  rw [← hM] at hbound
  nlinarith [sq_nonneg T]

/-! ## 2. Rung group B — strictness, nonreality, and the reflection

`LAW_..._SOL.md` §5 plus second-audit attacks 4a and 4b. -/

/-- **Target B1** (strictness — attack 4a, forcing (i)).

A zero on the line contributes weight exactly `0`. Hence a divergent weighted
sum forces `Re ρ > 1/2` **strictly**; membership in `RightZeros` already
carries this, so the target records the contrapositive fact that the weight
detects strictness. -/
theorem weight_eq_zero_iff_target (ρ : ℂ) :
    weight ρ = 0 ↔ ρ.re = 1 / 2 := by
  simp [weight, sub_eq_zero]

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
  intro hfin
  refine hinf (Set.Finite.subset (hreal_finite.union hfin) ?_)
  intro ρ hρ
  by_cases h : ρ.im = 0
  · exact Or.inl ⟨hρ, h⟩
  · exact Or.inr ⟨hρ, h⟩

/-- **Target B3** (the reflection arithmetic — §5).

`Re (1 - ρ) < 1/2` exactly when `Re ρ > 1/2`, and `Im (1 - ρ) = -Im ρ`, so
nonreality is preserved. Elementary; it is the half of §5 that does not
consume the functional equation. -/
theorem reflection_strict_left_target (ρ : ℂ) :
    ((1 : ℂ) - ρ).re < 1 / 2 ↔ 1 / 2 < ρ.re := by
  simp only [Complex.sub_re, Complex.one_re]
  constructor <;> intro h <;> linarith

/-- **Target B4** (reflection preserves nonreality). -/
theorem reflection_nonreal_target (ρ : ℂ) (h : ρ.im ≠ 0) :
    ((1 : ℂ) - ρ).im ≠ 0 := by
  simpa [Complex.sub_im] using h

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
  have hinj : Set.InjOn (fun ρ : ℂ => 1 - ρ) {ρ ∈ RightZeros Zero | ρ.im ≠ 0} := by
    intro x _ y _ h
    simpa [sub_right_inj] using h
  refine Set.Infinite.mono ?_ (hinf.image hinj)
  rintro s ⟨ρ, ⟨hρ, hρim⟩, rfl⟩
  refine ⟨hpole ρ hρ, ?_, ?_⟩
  · have := hρ.2
    simp only [Complex.sub_re, Complex.one_re]
    linarith
  · simpa [Complex.sub_im] using hρim

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
  have key : (∫ t in (0:ℝ)..T, (T - t) * Real.log t)
      = T ^ 2 / 2 * Real.log T - 3 / 4 * T ^ 2 := by
    have hint : IntervalIntegrable (fun t : ℝ => (T - t) * Real.log t)
        MeasureTheory.volume 0 T :=
      IntervalIntegrable.continuousOn_mul intervalIntegral.intervalIntegrable_log'
        (by fun_prop)
    have hderiv : ∀ x ∈ Set.Ioo (0:ℝ) T,
        HasDerivAt (fun x : ℝ => (T * x - x ^ 2 / 2) * Real.log x - T * x + x ^ 2 / 4)
          ((T - x) * Real.log x) x := by
      intro x hx
      have hx0 : x ≠ 0 := ne_of_gt hx.1
      have h1 : HasDerivAt (fun x : ℝ => T * x - x ^ 2 / 2) (T - x) x := by
        simpa using ((hasDerivAt_id x).const_mul T).sub ((hasDerivAt_pow 2 x).div_const 2)
      have h2 : HasDerivAt Real.log x⁻¹ x := Real.hasDerivAt_log hx0
      have h3 := h1.mul h2
      have h4 : HasDerivAt (fun x : ℝ => T * x) T x := by
        simpa using (hasDerivAt_id x).const_mul T
      have h5 : HasDerivAt (fun x : ℝ => x ^ 2 / 4) (2 * x / 4) x := by
        simpa using (hasDerivAt_pow 2 x).div_const 4
      have h6 := (h3.sub h4).add h5
      convert h6 using 1
      field_simp
      ring
    have hfa : Filter.Tendsto
        (fun x : ℝ => (T * x - x ^ 2 / 2) * Real.log x - T * x + x ^ 2 / 4)
        (nhdsWithin 0 (Set.Ioi 0)) (nhds 0) := by
      have hcont : Continuous (fun x : ℝ =>
          T * (x * Real.log x) - x / 2 * (x * Real.log x) - T * x + x ^ 2 / 4) := by
        have := Real.continuous_mul_log
        fun_prop
      refine Filter.Tendsto.mono_left ?_ nhdsWithin_le_nhds
      have heq : (fun x : ℝ => (T * x - x ^ 2 / 2) * Real.log x - T * x + x ^ 2 / 4)
          = fun x : ℝ =>
            T * (x * Real.log x) - x / 2 * (x * Real.log x) - T * x + x ^ 2 / 4 := by
        funext x; ring
      rw [heq]
      simpa using hcont.tendsto 0
    have hfb : Filter.Tendsto
        (fun x : ℝ => (T * x - x ^ 2 / 2) * Real.log x - T * x + x ^ 2 / 4)
        (nhdsWithin T (Set.Iio T))
        (nhds ((T * T - T ^ 2 / 2) * Real.log T - T * T + T ^ 2 / 4)) := by
      refine Filter.Tendsto.mono_left ?_ nhdsWithin_le_nhds
      have hca : ContinuousAt
          (fun x : ℝ => (T * x - x ^ 2 / 2) * Real.log x - T * x + x ^ 2 / 4) T := by
        refine ContinuousAt.add (ContinuousAt.sub ?_ (by fun_prop)) (by fun_prop)
        exact ContinuousAt.mul (by fun_prop) (Real.continuousAt_log (ne_of_gt hT))
      exact hca.tendsto
    rw [intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto hT hderiv hint hfa hfb]
    ring
  rw [key]; ring

/-- **Target C2** (OPTIONAL, hardest rung — the gamma quotient, `(GT)`).

`|Γ(1/2 + it) / Γ(it)|² = |t| tanh (π |t|)`.

Used in §4.2 to get the `1/2 · log|t|` critical-line behaviour, and the exact
identity the audit used to catch Kelmer's spurious `/π` (finding C). It is
self-contained special-function algebra but is expected to be the most
expensive target here; prefer the other rungs first. -/
theorem norm_sq_Gamma_half_add_I_mul (t : ℝ) :
    ‖Complex.Gamma (1 / 2 + (t : ℂ) * Complex.I)‖ ^ 2
      = Real.pi / Real.cosh (Real.pi * t) := by
  set s : ℂ := 1 / 2 + (t : ℂ) * Complex.I with hs
  have hconj : (starRingEnd ℂ) s = 1 - s := by
    simp [hs, Complex.ext_iff]
    norm_num
  have h1 : Complex.Gamma s * (starRingEnd ℂ) (Complex.Gamma s)
      = (Real.pi : ℂ) / Complex.sin ((Real.pi : ℂ) * s) := by
    rw [← Complex.Gamma_conj, hconj, Complex.Gamma_mul_Gamma_one_sub]
  have hsin : Complex.sin ((Real.pi : ℂ) * s) = (Real.cosh (Real.pi * t) : ℂ) := by
    have he : (Real.pi : ℂ) * s
        = (Real.pi / 2 : ℂ) + ((Real.pi * t : ℝ) : ℂ) * Complex.I := by
      rw [hs]; push_cast; ring
    rw [he, Complex.sin_add, Complex.sin_pi_div_two, Complex.cos_pi_div_two,
      Complex.cos_mul_I, ← Complex.ofReal_cosh]
    ring
  rw [hsin, Complex.mul_conj, Complex.normSq_eq_norm_sq, ← Complex.ofReal_div] at h1
  exact_mod_cast h1

theorem norm_sq_Gamma_I_mul (t : ℝ) (ht : t ≠ 0) :
    ‖Complex.Gamma ((t : ℂ) * Complex.I)‖ ^ 2
      = Real.pi / (t * Real.sinh (Real.pi * t)) := by
  have hsinh : Real.sinh (Real.pi * t) ≠ 0 := by
    simp [Real.sinh_eq_zero, Real.pi_ne_zero, ht]
  set s : ℂ := (t : ℂ) * Complex.I with hs
  have hs0 : s ≠ 0 := by
    simp [hs]
    exact_mod_cast ht
  have hconj : (starRingEnd ℂ) s = -s := by
    simp [hs]
  have hGone : Complex.Gamma (1 - s) = (-s) * Complex.Gamma (-s) := by
    have h : (1 : ℂ) - s = -s + 1 := by ring
    rw [h, Complex.Gamma_add_one (-s) (neg_ne_zero.mpr hs0)]
  have h2 : Complex.Gamma (-s) = (starRingEnd ℂ) (Complex.Gamma s) := by
    rw [← Complex.Gamma_conj, hconj]
  have hsin : Complex.sin ((Real.pi : ℂ) * s)
      = (Real.sinh (Real.pi * t) : ℂ) * Complex.I := by
    have he : (Real.pi : ℂ) * s = ((Real.pi * t : ℝ) : ℂ) * Complex.I := by
      rw [hs]; push_cast; ring
    rw [he, Complex.sin_mul_I, ← Complex.ofReal_sinh]
  have h1 : Complex.Gamma s * ((-s) * (starRingEnd ℂ) (Complex.Gamma s))
      = (Real.pi : ℂ) / ((Real.sinh (Real.pi * t) : ℂ) * Complex.I) := by
    rw [← h2, ← hGone, Complex.Gamma_mul_Gamma_one_sub, hsin]
  have hd1 : ((Real.sinh (Real.pi * t) : ℂ) * Complex.I) ≠ 0 := by
    apply mul_ne_zero _ Complex.I_ne_zero
    exact_mod_cast hsinh
  rw [eq_div_iff hd1] at h1
  have hden : ((Real.sinh (Real.pi * t) : ℂ) * Complex.I) * (-s)
      = ((t * Real.sinh (Real.pi * t) : ℝ) : ℂ) := by
    rw [Complex.ofReal_mul, hs,
      show ((Real.sinh (Real.pi * t) : ℂ) * Complex.I) * (-((t : ℂ) * Complex.I))
        = -((t : ℂ) * (Real.sinh (Real.pi * t) : ℂ)) * (Complex.I * Complex.I) from by ring,
      Complex.I_mul_I]
    ring
  have hd2 : ((t * Real.sinh (Real.pi * t) : ℝ) : ℂ) ≠ 0 := by
    rw [Ne, Complex.ofReal_eq_zero]
    exact mul_ne_zero ht hsinh
  have h3 : Complex.Gamma s * (starRingEnd ℂ) (Complex.Gamma s)
      = (Real.pi : ℂ) / ((t * Real.sinh (Real.pi * t) : ℝ) : ℂ) := by
    rw [eq_div_iff hd2, ← hden]
    linear_combination h1
  rw [Complex.mul_conj, Complex.normSq_eq_norm_sq, ← Complex.ofReal_div] at h3
  exact_mod_cast h3

theorem gamma_quotient_modulus_target (t : ℝ) (ht : t ≠ 0) :
    ‖Complex.Gamma (1 / 2 + t * Complex.I) / Complex.Gamma (t * Complex.I)‖ ^ 2
      = |t| * Real.tanh (Real.pi * |t|) := by
  have hsinh : Real.sinh (Real.pi * t) ≠ 0 := by
    simp [Real.sinh_eq_zero, Real.pi_ne_zero, ht]
  have hcosh : Real.cosh (Real.pi * t) ≠ 0 := (Real.cosh_pos _).ne'
  rw [norm_div, div_pow, norm_sq_Gamma_half_add_I_mul t, norm_sq_Gamma_I_mul t ht]
  have hstep : Real.pi / Real.cosh (Real.pi * t) / (Real.pi / (t * Real.sinh (Real.pi * t)))
      = t * Real.tanh (Real.pi * t) := by
    rw [Real.tanh_eq_sinh_div_cosh]
    field_simp
  rw [hstep]
  rcases lt_or_gt_of_ne ht with h | h
  · rw [abs_of_neg h, show Real.pi * -t = -(Real.pi * t) by ring, Real.tanh_neg]
    ring
  · rw [abs_of_pos h]

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
theorem finite_difference_bound_three (T : ℝ) (hT : 1 ≤ T) :
    |((T + 1) ^ 2 * Real.log (T + 1) - T ^ 2 * Real.log T)
        - (2 * T * Real.log T + T)| ≤ 3 * (1 + Real.log T) := by
  have hT0 : (0:ℝ) < T := by linarith
  have hT1 : (0:ℝ) < T + 1 := by linarith
  set L : ℝ := Real.log (T + 1) - Real.log T with hL
  have hup : L ≤ 1 / T := by
    have h := Real.log_le_sub_one_of_pos (x := (T + 1) / T) (by positivity)
    have h1 : Real.log ((T + 1) / T) = L := by
      rw [Real.log_div (by linarith) (by linarith)]
    have h2 : (T + 1) / T - 1 = 1 / T := by field_simp; ring
    rw [h1, h2] at h
    exact h
  have hlow : 1 / (T + 1) ≤ L := by
    have h := Real.log_le_sub_one_of_pos (x := T / (T + 1)) (by positivity)
    have h1 : Real.log (T / (T + 1)) = -L := by
      rw [Real.log_div (by linarith) (by linarith), hL]; ring
    have h2 : T / (T + 1) - 1 = -(1 / (T + 1)) := by field_simp; ring
    rw [h1, h2] at h
    linarith
  have hlogT : 0 ≤ Real.log T := Real.log_nonneg hT
  have hexp : ((T + 1) ^ 2 * Real.log (T + 1) - T ^ 2 * Real.log T)
      - (2 * T * Real.log T + T) = Real.log T + ((T + 1) ^ 2 * L - T) := by
    rw [hL]; ring
  rw [hexp]
  have hA : T + 1 ≤ (T + 1) ^ 2 * L := by
    have h : (T + 1) ^ 2 * (1 / (T + 1)) ≤ (T + 1) ^ 2 * L :=
      mul_le_mul_of_nonneg_left hlow (by positivity)
    calc T + 1 = (T + 1) ^ 2 * (1 / (T + 1)) := by field_simp
      _ ≤ _ := h
  have hB : (T + 1) ^ 2 * L ≤ T + 3 := by
    have h1 : (T + 1) ^ 2 * L ≤ (T + 1) ^ 2 * (1 / T) :=
      mul_le_mul_of_nonneg_left hup (by positivity)
    have h2 : (T + 1) ^ 2 * (1 / T) ≤ T + 3 := by
      rw [mul_one_div, div_le_iff₀ hT0]
      nlinarith [sq_nonneg (T - 1)]
    linarith
  rw [abs_le]
  constructor <;> linarith

theorem finite_difference_leading_target :
    ∃ c : ℝ, ∀ T : ℝ, 1 ≤ T →
      |((T + 1) ^ 2 * Real.log (T + 1) - T ^ 2 * Real.log T)
        - (2 * T * Real.log T + T)| ≤ c * (1 + Real.log T) :=
  ⟨3, finite_difference_bound_three⟩

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
  have hK : 0 ≤ K := by
    have h := hr 1 le_rfl
    simp at h
    exact le_trans (abs_nonneg _) h
  refine ⟨3 * |a| + |B| + |D| + 3 * K, ?_⟩
  intro T hT
  have hT0 : (0:ℝ) < T := by linarith
  have hlogT : 0 ≤ Real.log T := Real.log_nonneg hT
  have h1 := hF T hT
  have h2 := hF (T + 1) (by linarith)
  set X : ℝ := ((T + 1) ^ 2 * Real.log (T + 1) - T ^ 2 * Real.log T)
        - (2 * T * Real.log T + T) with hX
  have key : (F (T + 1) - F T) - (2 * a * T * Real.log T + (a + 2 * B) * T)
      = a * X + B + D + (r (T + 1) - r T) := by
    rw [h1, h2, hX]; ring
  rw [key]
  have hfd : |X| ≤ 3 * (1 + Real.log T) := finite_difference_bound_three T hT
  have hrT : |r T| ≤ K * (1 + Real.log T) := hr T hT
  have hrT1 : |r (T + 1)| ≤ 2 * K * (1 + Real.log T) := by
    have h := hr (T + 1) (by linarith)
    have hl : Real.log (T + 1) ≤ Real.log 2 + Real.log T := by
      have hle : Real.log (T + 1) ≤ Real.log (2 * T) :=
        Real.log_le_log (by linarith) (by linarith)
      rwa [Real.log_mul (by norm_num) (by linarith)] at hle
    have hlog2 : Real.log 2 ≤ 1 := by
      have := Real.log_le_sub_one_of_pos (x := (2:ℝ)) (by norm_num)
      linarith
    calc |r (T + 1)| ≤ K * (1 + Real.log (T + 1)) := h
      _ ≤ 2 * K * (1 + Real.log T) := by nlinarith
  have hax : |a * X| ≤ |a| * (3 * (1 + Real.log T)) := by
    rw [abs_mul]
    exact mul_le_mul_of_nonneg_left hfd (abs_nonneg a)
  have h3 : |a * X + B + D + (r (T + 1) - r T)|
      ≤ |a * X| + |B| + |D| + (|r (T + 1)| + |r T|) := by
    calc |a * X + B + D + (r (T + 1) - r T)|
        ≤ |a * X + B + D| + |r (T + 1) - r T| := abs_add_le _ _
      _ ≤ (|a * X + B| + |D|) + (|r (T + 1)| + |r T|) := by
          gcongr
          · exact abs_add_le _ _
          · exact abs_sub _ _
      _ ≤ ((|a * X| + |B|) + |D|) + (|r (T + 1)| + |r T|) := by
          gcongr
          exact abs_add_le _ _
      _ = _ := by ring
  have hone : (1:ℝ) ≤ 1 + Real.log T := by linarith
  nlinarith [abs_nonneg B, abs_nonneg D, abs_nonneg a]

/-- **Target D3** (the corrected numeric chain at `d = 2, κ = 1`).

With the *true* `B = (-2 log π - 3)/(8π)` and `a = 1/(4π)`, the audit's
`A = a + 2B` equals `-(1 + log π)/(2π)`, which is the Riemann–von Mangoldt
value at `q = 3`. Pure field arithmetic. -/
theorem corrected_A_value_target :
    (1 / (4 * Real.pi)) + 2 * ((-2 * Real.log Real.pi - 3) / (8 * Real.pi))
      = -(1 + Real.log Real.pi) / (2 * Real.pi) := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  field_simp
  ring

/-- **Target D4** (Kelmer's printed `B_Γ` is *not* the true `B`).

Kelmer's printed `B_Γ = (-4 log π - 1)/(8π)` differs from the corrected
`B = (-2 log π - 3)/(8π)`; they agree only if `log π = 1`, i.e. `π = e`.
Stating the disequality makes the ledger warning machine-checked: nobody may
consume `B_q` from that paper. -/
theorem kelmer_printed_B_ne_true_B_target :
    (-4 * Real.log Real.pi - 1) / (8 * Real.pi)
      ≠ (-2 * Real.log Real.pi - 3) / (8 * Real.pi) := by
  have hpi : (0:ℝ) < Real.pi := Real.pi_pos
  have hlog : 1 < Real.log Real.pi := by
    have h1 : Real.exp 1 < Real.pi := by
      have h2 := Real.exp_one_lt_d9
      have h3 := Real.pi_gt_three
      linarith
    calc (1:ℝ) = Real.log (Real.exp 1) := by simp
      _ < Real.log Real.pi := Real.log_lt_log (Real.exp_pos 1) h1
  intro h
  rw [div_eq_div_iff (by positivity) (by positivity)] at h
  nlinarith

end LawSkeletonI
