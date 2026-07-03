/-
The θ_edge = 2/3 exit-flux computation for hard-edge clusters of Farey gaps.

Continuum model: exceedance states form the triangle
  T_δ = {(x,y) : 0 < x, 0 < y, x + y < δ}
with the uniform (Lebesgue) measure; the in-region dynamics is the shear
(x,y) ↦ (y, 2y − x). A state EXITS the cluster in one step iff either
  (i)  x > 2y                     (branch switch, ejection to the far cusp), or
  (ii) 3y − x > δ                 (image sum exceeds δ, drift out),
and these two sets are disjoint inside T_δ.

The extremal index is the exit flux fraction
  θ = (vol E1 + vol E2) / vol T_δ = (δ²/6 + δ²/6)/(δ²/2) = 2/3.

Formalize the three area computations below (Lebesgue volume on ℝ × ℝ,
`MeasureTheory.volume`), for any δ > 0.
-/

import Mathlib

open MeasureTheory

/-- Area of the exceedance triangle. -/
theorem volume_T (δ : ℝ) (hδ : 0 < δ) :
    volume {p : ℝ × ℝ | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + p.2 < δ} =
      ENNReal.ofReal (δ ^ 2 / 2) := by
  sorry

/-- Area of exit set (i): branch-switch region x > 2y. -/
theorem volume_E1 (δ : ℝ) (hδ : 0 < δ) :
    volume {p : ℝ × ℝ | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + p.2 < δ ∧ 2 * p.2 < p.1} =
      ENNReal.ofReal (δ ^ 2 / 6) := by
  sorry

/-- Area of exit set (ii): drift-out region 3y − x > δ. -/
theorem volume_E2 (δ : ℝ) (hδ : 0 < δ) :
    volume {p : ℝ × ℝ | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + p.2 < δ ∧ δ < 3 * p.2 - p.1} =
      ENNReal.ofReal (δ ^ 2 / 6) := by
  sorry

/-- The two exit sets are disjoint (inside the triangle). -/
theorem exit_sets_disjoint (δ : ℝ) :
    ∀ p : ℝ × ℝ, 0 < p.1 → 0 < p.2 → p.1 + p.2 < δ →
      ¬(2 * p.2 < p.1 ∧ δ < 3 * p.2 - p.1) := by
  sorry
