/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Extended Moments

## Source
Saar Shai, "MiMo mini-project: BCZ extended moments" (2026).
GitHub: https://github.com/SaarShai/Primes-Equispaced (projects/mimo-mini-project)

## Background

Continuation of `BCZDenominatorRepulsion.lean` (FULLY PROVEN by Aristotle
in project 56972ade). We have the moments E[X] = 2/3, E[X²] = 1/2,
E[XY] = 5/12 from direct integration of f(x,y) = 2 over the triangle
T = {(x,y) : x+y > 1, 0 < x,y < 1}.

This file derives several COROLLARIES — pure arithmetic from the above
moments. All should be closeable by `unfold` + `norm_num`.

## Theorems to prove

1. **BCZ_sum_mean**: E[X + Y] = 4/3
2. **BCZ_sum_variance**: Var(X + Y) = 2 Var(X) + 2 Cov(X,Y) = 2·(1/18) + 2·(-1/36) = 1/18
3. **BCZ_diff_mean**: E[Y - X] = 0
4. **BCZ_diff_variance**: Var(Y - X) = 2 Var(X) - 2 Cov(X,Y) = 2·(1/18) - 2·(-1/36) = 1/6
5. **BCZ_diff_second_moment**: E[(Y-X)²] = Var(Y-X) + E[Y-X]² = 1/6
6. **BCZ_product_second_moment**: E[(XY)²] = ?  (requires E[X²Y²] which is a new integral, NOT prove)
-/

open Real

noncomputable section

/-- E[X] under BCZ. -/
def bczMean : ℝ := 2 / 3

/-- E[X²] under BCZ. -/
def bczSecondMoment : ℝ := 1 / 2

/-- Var(X) = E[X²] − E[X]² = 1/2 − 4/9 = 1/18 -/
def bczVariance : ℝ := bczSecondMoment - bczMean^2

/-- E[XY] under BCZ. -/
def bczMixedMoment : ℝ := 5 / 12

/-- Cov(X, Y) = E[XY] − E[X]E[Y] = 5/12 − 4/9 = −1/36 -/
def bczCovariance : ℝ := bczMixedMoment - bczMean^2

/-- E[X + Y] = 2 · E[X] = 4/3 (by linearity + symmetry) -/
theorem bcz_sum_mean : 2 * bczMean = 4 / 3 := by
  unfold bczMean
  norm_num

/-- Var(X + Y) = Var(X) + Var(Y) + 2 Cov(X,Y) = 2·(1/18) + 2·(-1/36) = 1/18 -/
theorem bcz_sum_variance : 2 * bczVariance + 2 * bczCovariance = 1 / 18 := by
  unfold bczVariance bczCovariance bczSecondMoment bczMean bczMixedMoment
  norm_num

/-- E[Y − X] = 0 (by symmetry of f under x ↔ y) -/
theorem bcz_diff_mean : (bczMean - bczMean : ℝ) = 0 := by
  ring

/-- Var(Y − X) = 2 Var(X) − 2 Cov(X,Y) = 2·(1/18) + 2·(1/36) = 1/6 -/
theorem bcz_diff_variance : 2 * bczVariance - 2 * bczCovariance = 1 / 6 := by
  unfold bczVariance bczCovariance bczSecondMoment bczMean bczMixedMoment
  norm_num

/-- The Pearson correlation of (X, Y) under the BCZ joint density f = 2·1_T
    is exactly -1/2. (Already proven in BCZDenominatorRepulsion.lean by
    Aristotle; restated here for completeness.) -/
theorem bcz_corr_neg_half : bczCovariance / bczVariance = -1/2 := by
  unfold bczCovariance bczVariance bczMixedMoment bczSecondMoment bczMean
  norm_num

/-- A consequence: the variance of the SUM equals the variance of an
    individual marginal. This is a coincidence of the BCZ triangle. -/
theorem bcz_sum_var_equals_marginal : 2 * bczVariance + 2 * bczCovariance = bczVariance := by
  unfold bczVariance bczCovariance bczMixedMoment bczSecondMoment bczMean
  norm_num

/-- A second consequence: Var(Y - X) is 3 × Var(X). -/
theorem bcz_diff_var_three_times_marginal : 2 * bczVariance - 2 * bczCovariance = 3 * bczVariance := by
  unfold bczVariance bczCovariance bczMixedMoment bczSecondMoment bczMean
  norm_num

end
