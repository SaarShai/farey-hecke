/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Cluster=2 Threshold via Integration

## Goal
Prove via REAL integration that the BCZ-density probability satisfies:
  P_BCZ(XY < 2/9) = (8·ln(3/2) − 2)/9

This implies the cluster=2 universality threshold:
  q*_BCZ = 1 − P_BCZ(XY < 2/9) = (11 − 8·ln(3/2))/9 ≈ 0.86181

## Setup (continues from BCZDenominatorRepulsion.lean v4)

We reuse the bczTriangle T = {(x,y) ∈ (0,1)² : x + y > 1} and the
Fubini reduction `setIntegral_bczTriangle_eq_iterated`:
  ∫ p in T, g p = ∫ x in 0..1, ∫ y in (1-x)..1, g(x,y)

## Geometric analysis

The integrand 2·𝟙_{xy<2/9} over T splits into 4 regions in x:

1. **x ∈ (0, 2/9)**: y ranges in (1-x, 1). All y satisfy xy < x ≤ 2/9.
   Inner integral = ∫_{1-x}^1 2 dy = 2x.
   Outer: ∫_0^{2/9} 2x dx = (2/9)² = 4/81.

2. **x ∈ (2/9, 1/3)**: y ∈ (1-x, min(1, 2/(9x))) = (1-x, 2/(9x)) (since x > 2/9 ⟹ 2/(9x) < 1).
   Need (1-x) < 2/(9x), i.e., 9x(1-x) < 2. Quadratic 9x²-9x+2 = 0 at x = 1/3, 2/3.
   For x ∈ (2/9, 1/3): 9x²-9x+2 > 0 (since 1/3 root), so 9x(1-x) < 2, condition satisfied.
   Inner: ∫_{1-x}^{2/(9x)} 2 dy = 2·(2/(9x) - 1 + x) = 4/(9x) + 2x - 2.
   Outer: ∫_{2/9}^{1/3} (4/(9x) + 2x - 2) dx = (4/9)·ln(3/2) - 13/81.

3. **x ∈ (1/3, 2/3)**: No valid y range (9x(1-x) ≥ 2 means 1-x ≥ 2/(9x)).
   Inner integral = 0.

4. **x ∈ (2/3, 1)**: Symmetric to case 2.
   Inner: same integrand 4/(9x) + 2x - 2.
   Outer: ∫_{2/3}^1 (4/(9x) + 2x - 2) dx = (4/9)·ln(3/2) - 1/9.

## Total
P(XY < 2/9) = 4/81 + (4/9)·ln(3/2) - 13/81 + 0 + (4/9)·ln(3/2) - 9/81
            = (4 - 13 - 9)/81 + (8/9)·ln(3/2)
            = -2/9 + (8/9)·ln(3/2)
            = (8·ln(3/2) - 2)/9

## Status of proofs
The geometric setup uses results from the v4 file. The bulk of the work
is intervalIntegral evaluation for each region (∫ 1/x dx = ln, ∫ x dx = x²/2).
Mathlib provides these. The region split requires careful Set.Ioo splitting
and case analysis on the indicator function.

References:
- BCZDenominatorRepulsion.lean (v4) for the Fubini reduction
- Mathlib `intervalIntegral.integral_one_div`, `integral_inv_of_pos`
-/

open Real MeasureTheory Set
open scoped Classical

noncomputable section

/-- The BCZ triangle (reused from v4). -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The set {(x,y) : xy < 2/9}. -/
def lowProductRegion : Set (ℝ × ℝ) :=
  {p | p.1 * p.2 < 2/9}

/-- Probability under BCZ density (= 2·𝟙_T integrated against Lebesgue prod). -/
noncomputable def bczProbXYLessTwoNinths : ℝ :=
  ∫ p in bczTriangle ∩ lowProductRegion, (2 : ℝ)

/-- Cluster=2 universality threshold. -/
noncomputable def clusterTwoThreshold : ℝ := 1 - bczProbXYLessTwoNinths

/-- **Target theorem**: P_BCZ(XY < 2/9) = (8·ln(3/2) − 2)/9.
    Proof via region split + Fubini. -/
theorem bczProbXYLessTwoNinths_eq :
    bczProbXYLessTwoNinths = (8 * Real.log (3/2) - 2) / 9 := by
  sorry  -- RESEARCH-OPEN: requires region-split argument + intervalIntegral.integral_one_div

/-- **Cluster=2 threshold closed form**. -/
theorem clusterTwoThreshold_eq :
    clusterTwoThreshold = (11 - 8 * Real.log (3/2)) / 9 := by
  unfold clusterTwoThreshold
  rw [bczProbXYLessTwoNinths_eq]
  ring

/-- Numerical bounds: 0.86 < q*_BCZ < 0.87. -/
theorem clusterTwoThreshold_bounds :
    0.86 < clusterTwoThreshold ∧ clusterTwoThreshold < 0.87 := by
  rw [clusterTwoThreshold_eq]
  constructor
  · -- 0.86 < (11 - 8 ln(3/2))/9
    -- Equivalent: 7.74 < 11 - 8 ln(3/2), i.e., 8 ln(3/2) < 3.26, ln(3/2) < 0.4075
    -- Mathlib: Real.log_lt_of_lt_exp, exp_one_lt_d9 etc.
    sorry  -- MATHLIB-PREREQ: needs Real.log_lt with specific exp bounds
  · -- (11 - 8 ln(3/2))/9 < 0.87
    -- Equivalent: 11 - 8 ln(3/2) < 7.83, i.e., 8 ln(3/2) > 3.17, ln(3/2) > 0.3963
    sorry  -- MATHLIB-PREREQ: needs Real.log_gt_of_gt_exp

end
