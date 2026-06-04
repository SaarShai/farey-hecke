/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

-- Aristotle's auto-generated proof of `local_perron_residue` emits a
-- handful of redundant simp-argument linter warnings. The proof is
-- correct (0 sorry, only the standard `propext` / `Classical.choice` /
-- `Quot.sound` axioms); we silence the cosmetic linter warnings.
set_option linter.unusedSimpArgs false
set_option linter.unusedTactic false

/-!
# Local Perron Residue Formula

## Source
Saar Shai, "Corrected B_∞ Identity" (2026), Lemma 2.1.
GitHub: https://github.com/SaarShai/Primes-Equispaced
AI Disclosure: Formalized with assistance from Claude (Anthropic).

## Statement
For an analytic function L with a simple zero at 0 (i.e. L(0) = 0, L'(0) ≠ 0),
and K > 1, the residue at w = 0 of K^w / (w · L(w)) equals:

  Res_{w=0} [K^w / (w · L(w))] = log K / L'(0) - L''(0) / (2 · L'(0)²)

This is a standard Laurent expansion computation: since L has a simple zero at 0,
1/L(w) has a simple pole, making K^w/(w·L(w)) have a double pole at w = 0.

## Mathlib API Status
Mathlib v4.28.0 has `MeromorphicAt` but does NOT have a `residue` function
for computing residues of meromorphic functions. We therefore formulate
the residue computation as a limit statement that extracts the w^{-1}
Laurent coefficient.
-/

open Complex Real Filter

noncomputable section

namespace LocalPerronResidue

/-- The residue value: the coefficient of w^{-1} in the Laurent expansion
    of K^w/(w·L(w)) at w = 0, when L has a simple zero at 0.

    log K / L'(0) - L''(0) / (2·L'(0)²) -/
def perronResidueValue (K : ℝ) (L'0 L''0 : ℂ) : ℂ :=
  ↑(Real.log K) / L'0 - L''0 / (2 * L'0 ^ 2)

/-
**Local Perron Residue Formula**: For analytic L with L(0) = 0, L'(0) ≠ 0,
    and K > 1, the Laurent coefficient of w^{-1} in K^w/(w·L(w)) at w = 0 is
      log K / L'(0) - L''(0) / (2·L'(0)²).

    We formulate this as: the function
      w ↦ (K^w · w / L(w) - 1/L'(0)) / w
    tends to the residue value as w → 0 (w ≠ 0).

    This is equivalent to saying that the w^{-1} Laurent coefficient is
    the residue value, since K^w/(w·L(w)) = 1/(L'(0)·w²) + residue/w + O(1).
-/
theorem local_perron_residue
    (K : ℝ) (hK : (1 : ℝ) < K)
    (L : ℂ → ℂ) (hL : AnalyticAt ℂ L 0)
    (hL0 : L 0 = 0) (hL'0 : deriv L 0 ≠ 0) :
    -- MATHLIB-PREREQ: `MeromorphicAt.residue` (meromorphic residue functional)
    -- MATHLIB-PREREQ: Laurent coefficient extraction API
    Tendsto
      (fun w : ℂ => ((↑K : ℂ) ^ w * w / L w - 1 / deriv L 0) / w)
      (nhdsWithin 0 {0}ᶜ)
      (nhds (perronResidueValue K (deriv L 0) (deriv (deriv L) 0))) := by
  -- RESEARCH-OPEN: This is a standard one-page Laurent expansion calculation.
  -- The key steps are:
  -- 1. Write L(w) = L'(0)·w·(1 + h(w)) where h is analytic with h(0) = 0
  -- 2. Then K^w·w/L(w) = K^w/(L'(0)·(1+h(w)))
  -- 3. (K^w/(L'(0)·(1+h(w))) - 1/L'(0)) / w
  --    = (1/L'(0)) · (K^w/(1+h(w)) - 1) / w
  -- 4. As w → 0: K^w = 1 + w·log K + O(w²), 1/(1+h(w)) = 1 - h(w) + O(w²)
  --    where h(w) = L''(0)/(2L'(0))·w + O(w²)
  -- 5. K^w/(1+h(w)) - 1 = w·(log K - L''(0)/(2L'(0))) + O(w²)
  -- 6. Dividing by w gives log K - L''(0)/(2L'(0)) + O(w)
  -- 7. Limit = (1/L'(0))·(log K - L''(0)/(2L'(0))) = perronResidueValue
  unfold perronResidueValue;
  -- Write $L(w) = w \cdot g(w)$ where $g(w) = L(w) / w$ for $w \neq 0$, extended by $g(0) = L'(0)$.
  set g : ℂ → ℂ := fun w => if w = 0 then deriv L 0 else L w / w;
  -- We need to show that $g$ is differentiable at $0$ with $g'(0) = \frac{L''(0)}{2}$.
  have hg_diff : HasDerivAt g (deriv (deriv L) 0 / 2) 0 := by
    have hg_analytic : Filter.Tendsto (fun w => (L w - deriv L 0 * w) / w^2) (nhdsWithin 0 {0}ᶜ) (nhds (deriv (deriv L) 0 / 2)) := by
      have hL'' : HasDerivAt (deriv L) (deriv (deriv L) 0) 0 := by
        have hL'' : AnalyticAt ℂ (deriv L) 0 := by
          exact hL.deriv;
        exact hL''.differentiableAt.hasDerivAt;
      have hL'' : Filter.Tendsto (fun w => (∫ t in (0 : ℝ)..1, (deriv L (t * w) - deriv L 0)) / w) (nhdsWithin 0 {0}ᶜ) (nhds (deriv (deriv L) 0 / 2)) := by
        have hL'' : Filter.Tendsto (fun w => (∫ t in (0 : ℝ)..1, (deriv L (t * w) - deriv L 0) / w)) (nhdsWithin 0 {0}ᶜ) (nhds (∫ t in (0 : ℝ)..1, deriv (deriv L) 0 * t)) := by
          refine' intervalIntegral.tendsto_integral_filter_of_dominated_convergence _ _ _ _ _;
          use fun x => ‖deriv ( deriv L ) 0‖ * x + 1;
          · filter_upwards [ self_mem_nhdsWithin ] with n hn;
            refine' Measurable.aestronglyMeasurable _;
            fun_prop;
          · rw [ eventually_nhdsWithin_iff ];
            rw [ Metric.eventually_nhds_iff ];
            have := Metric.tendsto_nhds_nhds.mp hL''.isLittleO.tendsto_div_nhds_zero;
            obtain ⟨ δ, hδ, H ⟩ := this 1 zero_lt_one; use δ, hδ; intro y hy hy'; filter_upwards [ ] with x hx; by_cases hx' : x = 0 <;> simp_all +decide [ div_eq_mul_inv, mul_assoc, mul_comm, mul_left_comm ] ;
            have := @H ( y * x ) ?_ <;> simp_all +decide [ mul_assoc, mul_comm, mul_left_comm ];
            · rw [ inv_mul_lt_iff₀ ( by aesop ) ] at this;
              rw [ abs_of_nonneg hx.1.le ] at this;
              have := norm_sub_le ( deriv L ( y * x ) - deriv L 0 - y * ( x * deriv ( deriv L ) 0 ) ) ( -y * ( x * deriv ( deriv L ) 0 ) ) ; simp_all +decide [ mul_assoc, mul_comm, mul_left_comm ];
              rw [ inv_mul_le_iff₀ ( norm_pos_iff.mpr hy' ) ] at *;
              rw [ inv_mul_eq_div, div_lt_iff₀ ( norm_pos_iff.mpr hy' ) ] at *;
              rw [ abs_of_nonneg hx.1.le ] at this ; nlinarith [ norm_nonneg y, norm_nonneg ( deriv ( deriv L ) 0 ) ];
            · exact lt_of_le_of_lt ( mul_le_of_le_one_left ( norm_nonneg _ ) ( abs_le.mpr ⟨ by linarith, by linarith ⟩ ) ) hy;
          · exact Continuous.intervalIntegrable ( by continuity ) _ _;
          · refine' Filter.Eventually.of_forall fun x hx => _;
            have hL'' : HasDerivAt (fun n => deriv L (x * n)) (deriv (deriv L) 0 * x) 0 := by
              convert HasDerivAt.comp 0 ( show HasDerivAt ( deriv L ) ( deriv ( deriv L ) 0 ) ( x * 0 ) from by simpa using hL'' ) ( HasDerivAt.const_mul ( x : ℂ ) ( hasDerivAt_id 0 ) ) using 1 ; norm_num;
            simpa [ div_eq_inv_mul ] using hL''.tendsto_slope_zero;
        convert hL'' using 2 <;> norm_num [ mul_comm ];
        erw [ intervalIntegral.integral_ofReal ] ; norm_num ; ring;
      refine' hL''.congr' _;
      rw [ Filter.EventuallyEq, eventually_nhdsWithin_iff ];
      rw [ Metric.eventually_nhds_iff ];
      obtain ⟨ ε, hε, h ⟩ := Metric.eventually_nhds_iff.mp ( hL.eventually_analyticAt );
      refine' ⟨ ε, hε, fun y hy hy' => _ ⟩;
      rw [ intervalIntegral.integral_eq_sub_of_hasDerivAt ];
      rotate_right;
      use fun t => L ( t * y ) / y - deriv L 0 * t;
      · simp +decide [ *, sq, mul_assoc, div_eq_mul_inv ];
        ring;
        simp +decide [ sq, mul_assoc, hy' ];
        aesop;
      · intro t ht; convert HasDerivAt.sub ( HasDerivAt.div_const ( HasDerivAt.comp _ ( h _ |> AnalyticAt.differentiableAt |> DifferentiableAt.hasDerivAt ) ( HasDerivAt.mul ( hasDerivAt_id _ |> HasDerivAt.ofReal_comp ) ( hasDerivAt_const _ _ ) ) ) _ ) ( HasDerivAt.mul ( hasDerivAt_const _ _ ) ( hasDerivAt_id _ |> HasDerivAt.ofReal_comp ) ) using 1 ; norm_num;
        · rw [ mul_div_cancel_right₀ _ hy' ];
        · simp_all +decide [ dist_eq_norm ];
          exact lt_of_le_of_lt ( mul_le_of_le_one_left ( norm_nonneg _ ) ( abs_le.mpr ⟨ by linarith, by linarith ⟩ ) ) hy;
      · apply_rules [ ContinuousOn.intervalIntegrable ];
        refine' ContinuousOn.sub _ continuousOn_const;
        refine' ContinuousOn.comp ( show ContinuousOn ( deriv L ) ( Metric.ball 0 ε ) from _ ) _ _;
        · exact fun x hx => ( h ( by simpa using hx ) |> AnalyticAt.deriv |> AnalyticAt.continuousAt |> ContinuousAt.continuousWithinAt );
        · exact Continuous.continuousOn ( by continuity );
        · norm_num [ Set.MapsTo ];
          exact fun x hx₁ hx₂ => by rw [ abs_of_nonneg hx₁ ] ; exact lt_of_le_of_lt ( mul_le_of_le_one_left ( norm_nonneg _ ) hx₂ ) ( by simpa using hy ) ;
    rw [ hasDerivAt_iff_tendsto_slope_zero ];
    refine' hg_analytic.congr' _;
    filter_upwards [ self_mem_nhdsWithin ] with w hw ; by_cases hw' : w = 0 <;> simp_all +decide [ div_eq_mul_inv, sq, mul_assoc, mul_comm, mul_left_comm ];
    grind;
  -- We need to show that the limit of the difference quotient is the derivative of $f(w) = K^w / g(w)$ at $w = 0$.
  have h_diff_quot : Filter.Tendsto (fun w => (K ^ w / g w - K ^ 0 / g 0) / w) (nhdsWithin 0 {0}ᶜ) (nhds ((Real.log K) / deriv L 0 - deriv (deriv L) 0 / (2 * (deriv L 0) ^ 2))) := by
    have h_diff_quot : HasDerivAt (fun w => K ^ w / g w) ((Real.log K) / deriv L 0 - deriv (deriv L) 0 / (2 * (deriv L 0) ^ 2)) 0 := by
      convert HasDerivAt.div ( HasDerivAt.const_cpow ( hasDerivAt_id 0 ) _ ) hg_diff _ using 1 <;> norm_num [ hL'0 ];
      · rw [ Complex.ofReal_log ( by positivity ) ] ; ring;
        grind +qlia;
      · linarith;
      · aesop;
    simpa [ div_eq_inv_mul ] using h_diff_quot.tendsto_slope_zero;
  grind

end LocalPerronResidue

end