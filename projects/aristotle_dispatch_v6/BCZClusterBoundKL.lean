/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Cluster Bound — Key Lemma (KL)

## Goal

Prove the missing algebraic step in the proof of the cluster=2 universality theorem
for the BCZ chain.

## Companion files
- `BCZDenominatorRepulsion.lean` (v4) — Fubini reduction + BCZ moments + Corr = −1/2
- `BCZThresholdIntegration.lean` (v5) — closed form P(XY < 2/9) = (8·ln(3/2) − 2)/9

## Setting

The BCZ map is `T_BCZ : T → T`, `(x, y) ↦ (y, k·y − x)` where `k = ⌊(1 + x)/y⌋`,
on the triangle `T = {(x,y) ∈ (0,1)² : x + y > 1}`.

A BCZ orbit `(X₀, X₁) → (X₁, X₂) → (X₂, X₃) → ...` has "extreme" pairs when
`X_i · X_{i+1} < 2/9`. We want to show that THREE consecutive extreme pairs cannot occur.

## Reduction (from research_notes/stern_brocot_to_cluster2.md §3)

The case `x_{i+1} ∈ (0, 2/3)` is rigorously handled by the algebraic squeeze:
combining `x_i + x_{i+1} > 1` and `x_i x_{i+1} < 2/9` gives `9 x_{i+1}² − 9 x_{i+1} + 2 > 0`
which forces `x_{i+1} ∉ (1/3, 2/3)`. Time-reversal symmetry of T_BCZ then gives the
WLOG case `x_{i+1} > 2/3`.

For `x_{i+1} ∈ (2/3, 1 − 2/(3·√5))` ≈ `(2/3, 0.702)`, the naive bound
`x_{i+2} x_{i+3} > k_{i+2} x_{i+2}² − x_{i+1} x_{i+2}` with `k_{i+2} ≥ 5` and
`x_{i+2} > 1 − x_{i+1}` gives `x_{i+2} x_{i+3} > (1 − x_{i+1})² · 5 − 2/9 ≥ 2/9`
when `(1 − x_{i+1})² ≥ 4/45` i.e. `x_{i+1} ≤ 1 − 2/(3√5)`.

The remaining case is the "0.702-band": `x_{i+1} ∈ (1 − 2/(3√5), 1)`.

## Key Lemma (KL) — to be proved

For `(x, y) ∈ T` with the BCZ orbit constraints, suppose:
- `(X₀, X₁) ∈ T`, `X₀ X₁ < 2/9`
- `X₁ ∈ (1 − 2/(3·√5), 1)` (the 0.702-band)
- `k₀ = ⌊(1 + X₀)/X₁⌋`, `X₂ = k₀ X₁ − X₀` (BCZ step 1)
- `X₁ X₂ < 2/9` (second extreme)
- `k₁ = ⌊(1 + X₁)/X₂⌋`, `X₃ = k₁ X₂ − X₁` (BCZ step 2)

Then `X₂ X₃ ≥ 2/9`.

## Why we believe KL holds

Empirically: 0 size-3+ clusters observed in 38.97M BCZ chain steps at `q = q*_BCZ`
exact (Kaggle 500M MC, May 2026). The dynamical orbit avoids the conjunction of
"X₁ in band" + "X₁X₂ extreme" + "X₂X₃ extreme" entirely.

The orbit constraint `X₂ = k₀ X₁ − X₀` couples X₀, X₁, X₂ algebraically; combined with
`(X₀, X₁) ∈ T` and `X₀ X₁ < 2/9`, the achievable `X₂` is more restricted than the
naive analysis suggests. We conjecture that the additional orbit-coupling closes the
gap.

## Sketch of proof strategy

The orbit constraint chains:
  X₂ = k₀ X₁ − X₀,  with  k₀ = ⌊(1 + X₀)/X₁⌋
  X₃ = k₁ X₂ − X₁,  with  k₁ = ⌊(1 + X₁)/X₂⌋

Given X₁ ∈ (0.702, 1), X₀ ∈ (1 − X₁, 2/(9 X₁)) (triangle + extreme), and X₀ X₁ < 2/9.

For each k₀ ∈ {1, 2, 3, ...}, X₂ = k₀ X₁ − X₀ is forced. For k₀ = 1:
  X₂ = X₁ − X₀ ∈ (X₁ − 2/(9 X₁), X₁ − (1 − X₁)) = (X₁ − 2/(9X₁), 2X₁ − 1)

For X₁ ∈ (0.702, 1): X₂ ∈ (0.385, 1) roughly. **Not** small.

Check X₁ X₂: X₁(X₁ − X₀) = X₁² − X₀ X₁ > X₁² − 2/9.
For X₁ > 0.702: X₁² > 0.493, so X₁² − 2/9 > 0.27 > 2/9 ≈ 0.222.
**So if k₀ = 1, the second pair (X₁, X₂) is NOT extreme.** Done for k₀ = 1.

For k₀ = 2: X₂ = 2X₁ − X₀ ∈ (2X₁ − 2/(9X₁), 2X₁ − (1 − X₁)) = (2X₁ − 2/(9X₁), 3X₁ − 1).
But k₀ = ⌊(1 + X₀)/X₁⌋ = 2 requires 2 ≤ (1+X₀)/X₁ < 3, i.e. X₀ ∈ [2X₁−1, 3X₁−1).
Combined with X₀ ∈ (1−X₁, 2/(9X₁)): need 2X₁−1 ≤ 2/(9X₁), i.e. 18X₁² − 9X₁ − 2 ≤ 0.
Discriminant: 81 + 144 = 225, roots: X₁ = (9 ± 15)/36 = {-1/6, 2/3}. So X₁ ≤ 2/3.
**But X₁ > 0.702 > 2/3 contradicts k₀ = 2.** Done for k₀ ≥ 2.

**So for X₁ ∈ (0.702, 1), only k₀ = 1 is possible, and then (X₁, X₂) is NOT extreme.**

This closes KL for this case. The argument is essentially algebraic / case-analytic
on integer values of k₀, all handled by polynomial inequalities.

## Goal: formalise the sketch above

-/

open Real Set
open scoped Classical

noncomputable section

/-- The BCZ triangle (reused from v4). -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The BCZ map T_BCZ : T → T, (x, y) ↦ (y, k·y − x), k = ⌊(1+x)/y⌋. -/
noncomputable def bczMap (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / p.2⌋
  (p.2, (k : ℝ) * p.2 - p.1)

/-- KL — Key Lemma: in the 0.702-band, X₀X₁ extreme + X₁ in band ⟹ X₁X₂ NOT extreme. -/
theorem KL_X1_band_forces_X1X2_nonextreme :
    ∀ x y : ℝ,
      (x, y) ∈ bczTriangle →
      x * y < 2 / 9 →
      y > 1 - 2 / (3 * Real.sqrt 5) →  -- y in (0.702, 1)
      y * ((bczMap (x, y)).2) ≥ 2 / 9 := by
  sorry  -- TARGET: prove this via case analysis on k₀ = ⌊(1+x)/y⌋

/-- Corollary: above q*_BCZ, three consecutive extreme pairs cannot occur. -/
theorem cluster_size_le_two :
    ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ bczTriangle) →
      (∀ n, orbit (n + 1) = bczMap (orbit n)) →
      ∀ i,
        (orbit i).1 * (orbit i).2 < 2 / 9 →
        (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
        (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9 := by
  sorry  -- Follows from KL + the (0, 2/3) case (rigorous in §3) + time-reversal symmetry

end
