/-
Copyright (c) 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Saar Shai
-/
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Set
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic
import Mathlib.Topology.Order.Compact

/-!
# The Boca–Cobeli–Zaharescu Triangle: Moments and Denominator Correlation

The Boca–Cobeli–Zaharescu (BCZ) limit theorem (Boca–Cobeli–Zaharescu,
*J. Reine Angew. Math.* **535** (2001), 207–236) states that for consecutive
denominators `bᵢ, bᵢ₊₁` of the Farey fractions in `F_N`, the pair
`(bᵢ / N, bᵢ₊₁ / N)` has limiting joint density
$$ f(x, y) = 2 \cdot \mathbf{1}_T(x, y), \qquad T = \{(x, y) \in (0,1)^2 : x + y > 1\}. $$

This file computes the first moments of that distribution by direct
integration via Fubini, and deduces that the Pearson correlation of the
two marginals equals `-1 / 2`.

## Main definitions

* `bczTriangle` : the open triangle `T = {(x,y) ∈ (0,1)² : x + y > 1}`.
* `bczMean`, `bczSecondMoment`, `bczMixedMoment` : the moments
  `∫∫_T 2 x`, `∫∫_T 2 x²`, `∫∫_T 2 x y`.
* `bczVariance`, `bczCovariance` : `E[X²] - E[X]²` and `E[XY] - E[X] E[Y]`
  (using symmetry `E[Y] = E[X]`).

## Main results

* `setIntegral_bczTriangle_eq_iterated` : Fubini reduction
  `∫_T g = ∫ x in 0..1, ∫ y in (1-x)..1, g (x, y)`
  for continuous `g`.
* `bczMean_eq` : `E[X] = 2 / 3`.
* `bczSecondMoment_eq` : `E[X²] = 1 / 2`.
* `bczMixedMoment_eq` : `E[XY] = 5 / 12`.
* `bczVariance_eq` : `Var(X) = 1 / 18`.
* `bczCovariance_eq` : `Cov(X, Y) = -1 / 36`.
* `bcz_denominator_correlation_neg_half` : `Cov / Var = -1 / 2`.

## References

* A. Boca, C. Cobeli, A. Zaharescu, *On the distribution of the Farey
  sequence with respect to spacings*, J. Reine Angew. Math. **535** (2001).
* J. S. Athreya, Y. Cheung, *A Poincaré section for the horocycle flow on
  the space of lattices*, IMRN (2014).
-/

open Real MeasureTheory Set
open scoped Classical

noncomputable section

namespace BCZ

/-! ## The BCZ triangle and density -/

/-- The BCZ triangle `T = {(x, y) ∈ (0,1)² : x + y > 1}`. -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- Membership in `bczTriangle` rewritten as an iterated condition:
for `p = (x, y)`, `p ∈ T ↔ x ∈ Ioo 0 1 ∧ y ∈ Ioo (1 - x) 1`. -/
lemma mem_bczTriangle_iff (x y : ℝ) :
    (x, y) ∈ bczTriangle ↔ x ∈ Ioo (0 : ℝ) 1 ∧ y ∈ Ioo (1 - x) 1 := by
  simp only [bczTriangle, Set.mem_setOf_eq, Set.mem_Ioo]
  constructor
  · rintro ⟨hx0, hx1, hy0, hy1, hxy⟩
    refine ⟨⟨hx0, hx1⟩, ?_, hy1⟩
    linarith
  · rintro ⟨⟨hx0, hx1⟩, hy1x, hy1⟩
    refine ⟨hx0, hx1, ?_, hy1, ?_⟩
    · linarith
    · linarith

/-- The BCZ triangle is a measurable subset of `ℝ × ℝ`. -/
lemma measurableSet_bczTriangle : MeasurableSet bczTriangle := by
  unfold bczTriangle
  have h1 : MeasurableSet {p : ℝ × ℝ | 0 < p.1} :=
    measurableSet_Ioi.preimage measurable_fst
  have h2 : MeasurableSet {p : ℝ × ℝ | p.1 < 1} :=
    measurableSet_Iio.preimage measurable_fst
  have h3 : MeasurableSet {p : ℝ × ℝ | 0 < p.2} :=
    measurableSet_Ioi.preimage measurable_snd
  have h4 : MeasurableSet {p : ℝ × ℝ | p.2 < 1} :=
    measurableSet_Iio.preimage measurable_snd
  have h5 : MeasurableSet {p : ℝ × ℝ | p.1 + p.2 > 1} := by
    have hsum : Measurable (fun p : ℝ × ℝ => p.1 + p.2) :=
      measurable_fst.add measurable_snd
    exact measurableSet_Ioi.preimage hsum
  exact h1.inter (h2.inter (h3.inter (h4.inter h5)))

/-! ## Reduction to iterated integrals

For any continuous `g : ℝ × ℝ → ℝ`, the integral of `g` over the BCZ
triangle equals the iterated `intervalIntegral`
`∫ x in 0..1, ∫ y in (1-x)..1, g (x, y)`.

This is Fubini applied to the bounded square `Ioo 0 1 ×ˢ Ioo 0 1`,
combined with the iterated description of `T` from `mem_bczTriangle_iff`.
-/

/-- The slice of `bczTriangle` in `y` at fixed `x ∈ (0, 1)` is `Ioo (1 - x) 1`. -/
lemma bczTriangle_slice (x : ℝ) (hx : x ∈ Ioo (0 : ℝ) 1) :
    {y : ℝ | (x, y) ∈ bczTriangle} = Ioo (1 - x) 1 := by
  ext y
  simp only [Set.mem_setOf_eq, Set.mem_Ioo]
  rw [mem_bczTriangle_iff]
  simp [hx]

/-- **Fubini reduction.** For continuous `g : ℝ × ℝ → ℝ`,
the integral of `g` over the BCZ triangle equals the iterated interval
integral `∫ x in 0..1, ∫ y in (1 - x)..1, g (x, y)`. -/
lemma setIntegral_bczTriangle_eq_iterated
    (g : ℝ × ℝ → ℝ) (hg : Continuous g) :
    ∫ p in bczTriangle, g p
      = ∫ x in (0 : ℝ)..1, ∫ y in (1 - x)..1, g (x, y) := by
  set S : Set (ℝ × ℝ) := Ioo (0 : ℝ) 1 ×ˢ Ioo (0 : ℝ) 1 with hS_def
  have hT_sub_S : bczTriangle ⊆ S := by
    rintro ⟨a, b⟩ hp
    rw [mem_bczTriangle_iff] at hp
    obtain ⟨hx, hy⟩ := hp
    refine ⟨hx, ?_, hy.2⟩
    exact lt_trans (by linarith [hx.2] : (0 : ℝ) < 1 - a) hy.1
  have hT_meas : MeasurableSet bczTriangle := measurableSet_bczTriangle
  have hT_eq : bczTriangle = S ∩ bczTriangle :=
    (Set.inter_eq_self_of_subset_right hT_sub_S).symm
  have step12 : (∫ p in bczTriangle, g p)
      = ∫ p in S, bczTriangle.indicator (fun q => g q) p := by
    conv_lhs => rw [hT_eq]
    rw [← setIntegral_indicator hT_meas]
  rw [step12]
  have hg_intOn_S : IntegrableOn g S volume := by
    have hSub : S ⊆ Set.Icc ((0 : ℝ), (0 : ℝ)) (1, 1) := by
      rintro ⟨a, b⟩ ⟨⟨ha₁, ha₂⟩, ⟨hb₁, hb₂⟩⟩
      exact ⟨⟨ha₁.le, hb₁.le⟩, ⟨ha₂.le, hb₂.le⟩⟩
    have hg_intOn_Icc : IntegrableOn g (Set.Icc ((0 : ℝ), (0 : ℝ)) (1, 1)) volume :=
      hg.continuousOn.integrableOn_compact isCompact_Icc
    exact hg_intOn_Icc.mono_set hSub
  have hg_intOn_T : IntegrableOn g bczTriangle volume :=
    hg_intOn_S.mono_set hT_sub_S
  have hindicator_intOn :
      IntegrableOn (fun p : ℝ × ℝ => bczTriangle.indicator (fun q => g q) p) S volume := by
    have hI : Integrable (bczTriangle.indicator (fun q => g q)) volume :=
      hg_intOn_T.integrable_indicator hT_meas
    exact hI.integrableOn
  have hfubini :
      (∫ p in S, bczTriangle.indicator (fun q => g q) p)
        = ∫ x in (Ioo (0 : ℝ) 1), ∫ y in (Ioo (0 : ℝ) 1),
            bczTriangle.indicator (fun q => g q) (x, y) := by
    rw [show S = (Ioo (0 : ℝ) 1) ×ˢ (Ioo (0 : ℝ) 1) from rfl,
        show (volume : Measure (ℝ × ℝ)) = (volume : Measure ℝ).prod volume from rfl]
    exact setIntegral_prod _ hindicator_intOn
  rw [hfubini]
  have hindicator_slice : ∀ (x y : ℝ),
      bczTriangle.indicator (fun q => g q) (x, y)
        = ({y' | (x, y') ∈ bczTriangle}).indicator (fun y' => g (x, y')) y := by
    intro x y
    simp only [Set.indicator]
    split_ifs with h₁ h₂ h₂
    · rfl
    · exact absurd h₁ h₂
    · exact absurd h₂ h₁
    · rfl
  simp_rw [hindicator_slice]
  have hinner : ∀ x ∈ Ioo (0 : ℝ) 1,
      (∫ y in Ioo (0 : ℝ) 1, ({y' | (x, y') ∈ bczTriangle}).indicator
                                  (fun y' => g (x, y')) y)
        = ∫ y in (1 - x)..1, g (x, y) := by
    intro x hx
    rw [bczTriangle_slice x hx]
    rw [setIntegral_indicator measurableSet_Ioo]
    have hinter : Ioo (0 : ℝ) 1 ∩ Ioo (1 - x) 1 = Ioo (1 - x) 1 := by
      ext y
      simp only [Set.mem_inter_iff, Set.mem_Ioo]
      refine ⟨fun ⟨_, h⟩ => h, fun h => ⟨⟨?_, h.2⟩, h⟩⟩
      linarith [hx.2]
    rw [hinter]
    have h1mx : (1 - x : ℝ) ≤ 1 := by
      have : 0 < x := hx.1
      linarith
    rw [← integral_Ioc_eq_integral_Ioo, ← intervalIntegral.integral_of_le h1mx]
  have hreplace_inner :
      (∫ x in Ioo (0 : ℝ) 1, ∫ y in Ioo (0 : ℝ) 1,
          ({y' | (x, y') ∈ bczTriangle}).indicator (fun y' => g (x, y')) y)
      = ∫ x in Ioo (0 : ℝ) 1, ∫ y in (1 - x)..1, g (x, y) := by
    refine setIntegral_congr_fun measurableSet_Ioo ?_
    intro x hx
    exact hinner x hx
  rw [hreplace_inner]
  rw [← integral_Ioc_eq_integral_Ioo,
      ← intervalIntegral.integral_of_le (by norm_num : (0 : ℝ) ≤ 1)]

/-! ## Moments as set integrals -/

/-- `E[X]` under the BCZ density, defined as `∫∫_T 2 x`. -/
def bczMean : ℝ :=
  ∫ p in bczTriangle, 2 * p.1

/-- `E[X²]` under the BCZ density, defined as `∫∫_T 2 x²`. -/
def bczSecondMoment : ℝ :=
  ∫ p in bczTriangle, 2 * p.1 ^ 2

/-- `E[XY]` under the BCZ density, defined as `∫∫_T 2 x y`. -/
def bczMixedMoment : ℝ :=
  ∫ p in bczTriangle, 2 * (p.1 * p.2)

/-- `Var(X) = E[X²] - E[X]²`. -/
def bczVariance : ℝ := bczSecondMoment - bczMean ^ 2

/-- `Cov(X, Y) = E[XY] - E[X] E[Y]`. By symmetry of the triangle in
`(x, y)`, `E[Y] = E[X]`, so we use `bczMean ^ 2`. -/
def bczCovariance : ℝ := bczMixedMoment - bczMean ^ 2

/-! ## Inner-integral computations -/

/-- `∫_{1 - x}^{1} 1 dy = x`. -/
lemma inner_const (x : ℝ) :
    ∫ _ in (1 - x)..1, (1 : ℝ) = x := by
  rw [intervalIntegral.integral_const, smul_eq_mul]
  ring

/-- `∫_{1 - x}^{1} y dy = x - x² / 2`. -/
lemma inner_y (x : ℝ) :
    ∫ y in (1 - x)..1, y = x - x ^ 2 / 2 := by
  rw [integral_id]
  ring

/-- `∫_{1 - x}^{1} y² dy = x - x² + x³ / 3`. -/
lemma inner_y_sq (x : ℝ) :
    ∫ y in (1 - x)..1, y ^ 2 = x - x ^ 2 + x ^ 3 / 3 := by
  rw [integral_pow]
  ring

/-! ## The three moment theorems -/

/-- The first moment under the BCZ density is `2 / 3`:
`E[X] = ∫∫_T 2 x = 2 / 3`. -/
theorem bczMean_eq : bczMean = 2 / 3 := by
  unfold bczMean
  have hcont : Continuous (fun p : ℝ × ℝ => 2 * p.1) :=
    continuous_const.mul continuous_fst
  rw [setIntegral_bczTriangle_eq_iterated _ hcont]
  have inner : ∀ x : ℝ, (∫ _y in (1 - x)..1, (2 * x : ℝ)) = 2 * x * x := by
    intro x
    rw [intervalIntegral.integral_const, smul_eq_mul]
    ring
  simp_rw [inner]
  have h : (∫ x in (0 : ℝ)..1, 2 * x * x) = (∫ x in (0 : ℝ)..1, 2 * x ^ 2) := by
    refine intervalIntegral.integral_congr ?_
    intro x _; ring
  rw [h, intervalIntegral.integral_const_mul, integral_pow]
  norm_num

/-- The second moment under the BCZ density is `1 / 2`:
`E[X²] = ∫∫_T 2 x² = 1 / 2`. -/
theorem bczSecondMoment_eq : bczSecondMoment = 1 / 2 := by
  unfold bczSecondMoment
  have hcont : Continuous (fun p : ℝ × ℝ => 2 * p.1 ^ 2) :=
    continuous_const.mul (continuous_fst.pow 2)
  rw [setIntegral_bczTriangle_eq_iterated _ hcont]
  have inner : ∀ x : ℝ, (∫ _y in (1 - x)..1, (2 * x ^ 2 : ℝ)) = 2 * x ^ 2 * x := by
    intro x
    rw [intervalIntegral.integral_const, smul_eq_mul]
    ring
  simp_rw [inner]
  have h : (∫ x in (0 : ℝ)..1, 2 * x ^ 2 * x) = (∫ x in (0 : ℝ)..1, 2 * x ^ 3) := by
    refine intervalIntegral.integral_congr ?_
    intro x _; ring
  rw [h, intervalIntegral.integral_const_mul, integral_pow]
  norm_num

/-- The mixed moment under the BCZ density is `5 / 12`:
`E[XY] = ∫∫_T 2 x y = 5 / 12`. -/
theorem bczMixedMoment_eq : bczMixedMoment = 5 / 12 := by
  unfold bczMixedMoment
  have hcont : Continuous (fun p : ℝ × ℝ => 2 * (p.1 * p.2)) :=
    continuous_const.mul (continuous_fst.mul continuous_snd)
  rw [setIntegral_bczTriangle_eq_iterated _ hcont]
  have inner : ∀ x : ℝ,
      (∫ y in (1 - x)..1, (2 * (x * y) : ℝ)) = 2 * x * (x - x ^ 2 / 2) := by
    intro x
    have h₁ : (∫ y in (1 - x)..1, (2 * (x * y) : ℝ))
        = (2 * x) * ∫ y in (1 - x)..1, y := by
      rw [← intervalIntegral.integral_const_mul]
      refine intervalIntegral.integral_congr ?_
      intro y _; ring
    rw [h₁, inner_y]
  simp_rw [inner]
  have hreduce :
      (∫ x in (0 : ℝ)..1, 2 * x * (x - x ^ 2 / 2))
        = (∫ x in (0 : ℝ)..1, 2 * x ^ 2 - x ^ 3) := by
    refine intervalIntegral.integral_congr ?_
    intro x _; ring
  rw [hreduce, intervalIntegral.integral_sub
        ((intervalIntegral.intervalIntegrable_pow 2).const_mul 2)
        (intervalIntegral.intervalIntegrable_pow 3),
      intervalIntegral.integral_const_mul, integral_pow, integral_pow]
  norm_num

/-! ## Variance, covariance, correlation -/

/-- The variance of `X` under the BCZ density is `1 / 18`. -/
theorem bczVariance_eq : bczVariance = 1 / 18 := by
  unfold bczVariance
  rw [bczSecondMoment_eq, bczMean_eq]
  norm_num

/-- The covariance of `X` and `Y` under the BCZ density is `-1 / 36`. -/
theorem bczCovariance_eq : bczCovariance = -1 / 36 := by
  unfold bczCovariance
  rw [bczMixedMoment_eq, bczMean_eq]
  norm_num

/-- **BCZ Denominator Level Repulsion.** Under the BCZ joint density
`f(x, y) = 2 · 𝟙_T` on the triangle `T = {x + y > 1} ∩ (0,1)²`, the Pearson
correlation of the two marginals is exactly `-1 / 2`. By symmetry of the
triangle, `Var(Y) = Var(X)`, so the Pearson correlation reduces to
`Cov / Var`. -/
theorem bcz_denominator_correlation_neg_half :
    bczCovariance / bczVariance = -1 / 2 := by
  rw [bczCovariance_eq, bczVariance_eq]
  norm_num

end BCZ

end
