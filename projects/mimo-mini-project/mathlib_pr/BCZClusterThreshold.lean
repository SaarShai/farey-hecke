/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Cluster=2 Universality Threshold

## Source
Saar Shai, "MiMo mini-project: cluster=2 universality threshold" (2026).

## Background

Continuing the BCZ analysis from `BCZDenominatorRepulsion.lean` (Aristotle v1,
FULLY PROVEN: Corr(X,Y) = -1/2) and `BCZChainAntiClustering.lean` (Aristotle v2).

The main result of this dispatch is the closed-form threshold for cluster=2
universality under the BCZ Markov chain dynamics.

## Setup

Under the BCZ joint density f(x,y) = 2·𝟙_T on T := {(x,y) : x+y > 1, 0<x,y<1},
the gap d(X,Y) := 1/(X·Y) defines a sequence (d_i) via the BCZ chain.

For quantile q ∈ (0,1), let θ_q := q-quantile of d under BCZ. Define cluster
size at q = maximal run of consecutive exceedances {i : d_i > θ_q}.

## Closed-form derivation (this session)

The critical BCZ-chain threshold is t* = 2/9 (corresponds to the boundary
pair (X,Y) = (1/3, 2/3) in the BCZ chain's invariant region under the
minimal step pattern (k₁=1, k₂=2)).

The BCZ-density probability P(XY < 2/9) is computed exactly via
direct integration on T:

  P_BCZ(XY < 2/9) = (8·ln(3/2) - 2) / 9

Hence the cluster=2 universality threshold is:

  **q*_BCZ = (11 - 8·ln(3/2)) / 9 ≈ 0.861809**

## Theorem statement (to prove)

For q ≥ q*_BCZ, the BCZ chain admits no cluster of size ≥ 3.

This follows from: P_BCZ(XY < t_q) = 1-q < (8·ln(3/2)-2)/9 = P_BCZ(XY < 2/9),
hence t_q < 2/9 and pairs in T with XY ≥ 2/9 cannot be extreme. The BCZ
chain dynamics then preclude size ≥ 3 clusters (proven separately in
BCZChainAntiClustering.lean).

This file focuses on the ARITHMETIC closed-form derivation P(XY<2/9) = (8 ln(3/2)-2)/9.
-/

open Real

noncomputable section

/-- The BCZ probability P(XY < 2/9) closed form, derived via direct integration. -/
def bczProbXYLessTwoNinths : ℝ := (8 * Real.log (3/2) - 2) / 9

/-- The cluster=2 universality threshold under BCZ density. -/
def clusterTwoThreshold : ℝ := (11 - 8 * Real.log (3/2)) / 9

/-- The threshold value, complementary form. -/
theorem cluster_two_threshold_def :
    clusterTwoThreshold = 1 - bczProbXYLessTwoNinths := by
  unfold clusterTwoThreshold bczProbXYLessTwoNinths
  ring

private lemma cluster_two_threshold_value_upper :
    (11 - 8 * Real.log (3 / 2)) / 9 < 0.87 := by
  -- We'll use the fact that $Real.log (3 / 2) > 0.405$ to conclude the proof.
  have h_log : Real.log (3 / 2) > 0.405 := by
    norm_num [ Real.lt_log_iff_exp_lt ] at *;
    -- We can raise both sides to the power of 200 to remove the fraction.
    suffices h_exp : Real.exp 81 < (3 / 2) ^ 200 by
      contrapose! h_exp;
      exact le_trans ( pow_le_pow_left₀ ( by norm_num ) h_exp 200 ) ( by norm_num [ ← Real.exp_nat_mul ] );
    have := Real.exp_one_lt_d9.le ; norm_num1 at * ; rw [ show Real.exp 81 = ( Real.exp 1 ) ^ 81 by rw [ ← Real.exp_nat_mul ] ; norm_num ] ; exact lt_of_le_of_lt ( pow_le_pow_left₀ ( by positivity ) this _ ) ( by norm_num ) ;
  grind

/-
Numerical value: q*_BCZ ≈ 0.861809.
-/
theorem cluster_two_threshold_value :
    0.86 < clusterTwoThreshold ∧ clusterTwoThreshold < 0.87 := by
  unfold clusterTwoThreshold
  -- Need: 0.86 < (11 - 8 ln(3/2))/9 < 0.87
  -- Equivalently: 7.74 < 11 - 8 ln(3/2) < 7.83
  -- 8 ln(3/2) ∈ (3.17, 3.26)
  -- ln(3/2) ∈ (0.396, 0.408)
  -- ln 1.5 = 0.405465...
  constructor
  · -- 0.86 < (11 - 8 ln(3/2))/9
    -- We'll use the fact that $ln(3/2) \approx 0.405$ to show that $0.86 < (11 - 8 * ln(3/2)) / 9$.
    have h_log_approx : Real.log (3 / 2) < 326 / 800 := by
      rw [ Real.log_lt_iff_lt_exp ] <;> norm_num;
      -- We'll use the exponential property to simplify the expression. Note that $e^{163/400} = \left(e^{1/400}\right)^{163}$.
      have h_exp : Real.exp (163 / 400) = (Real.exp (1 / 400)) ^ 163 := by
        norm_num [ ← Real.exp_nat_mul ];
      exact h_exp.symm ▸ lt_of_lt_of_le ( by norm_num ) ( pow_le_pow_left₀ ( by positivity ) ( Real.add_one_le_exp _ ) _ );
    linarith
  · -- (11 - 8 ln(3/2))/9 < 0.87
    exact cluster_two_threshold_value_upper

/-- The complementary identity: bczProbXYLessTwoNinths + clusterTwoThreshold = 1. -/
theorem cluster_two_threshold_complementary :
    bczProbXYLessTwoNinths + clusterTwoThreshold = 1 := by
  unfold bczProbXYLessTwoNinths clusterTwoThreshold
  ring

/-- The "median run" cutoff q_median = 3/2 - ln 2.
    Below this, median pairs (b ≈ b' ≈ N/2) ARE in the extreme set.
    Above this, median pairs CANNOT be extreme.
    Derived from P(XY < 1/4) = ln 2 - 1/2. -/
def medianRunCutoff : ℝ := 3/2 - Real.log 2

/-- P(XY < 1/4) under BCZ density. -/
def bczProbXYLessQuarter : ℝ := Real.log 2 - 1/2

theorem median_run_cutoff_complementary :
    bczProbXYLessQuarter + medianRunCutoff = 1 := by
  unfold bczProbXYLessQuarter medianRunCutoff
  ring

/-
The two thresholds (median-run cutoff and cluster-2 threshold) are distinct,
    with median-run cutoff strictly less than cluster-2 threshold.
-/
theorem median_cutoff_lt_cluster_threshold :
    medianRunCutoff < clusterTwoThreshold := by
  unfold medianRunCutoff clusterTwoThreshold
  -- Need: 3/2 - ln 2 < (11 - 8 ln(3/2))/9
  -- Multiply by 9: 13.5 - 9 ln 2 < 11 - 8 ln(3/2)
  -- Rearrange: 2.5 < 9 ln 2 - 8 ln(3/2)
  -- = 9 ln 2 - 8 (ln 3 - ln 2)
  -- = 17 ln 2 - 8 ln 3
  -- Numerically: 17 · 0.693 - 8 · 1.099 = 11.78 - 8.79 = 2.99 > 2.5 ✓
  -- We'll use that $e \approx 2.718$ to show that $5/2 < \log (131072 / 6561)$.
  have h_exp_approx : Real.exp (5 / 2) < 131072 / 6561 := by
    -- We can raise both sides to the power of 2 to remove the square root.
    have h_exp_sq : Real.exp 5 < (131072 / 6561) ^ 2 := by
      have := Real.exp_one_lt_d9.le ; norm_num1 at * ; rw [ show Real.exp 5 = ( Real.exp 1 ) ^ 5 by rw [ ← Real.exp_nat_mul ] ; norm_num ] ; nlinarith [ Real.exp_pos 1, pow_pos ( Real.exp_pos 1 ) 2, pow_pos ( Real.exp_pos 1 ) 3, pow_pos ( Real.exp_pos 1 ) 4 ] ;
    rw [ show ( 5 : ℝ ) = 5 / 2 + 5 / 2 by norm_num, Real.exp_add ] at h_exp_sq ; nlinarith [ Real.exp_pos ( 5 / 2 ) ];
  -- Use the fact that $\exp(5/2) < 131072 / 6561$ to show that $5/2 < \log (131072 / 6561)$.
  have h_log_approx : 5 / 2 < Real.log (131072 / 6561) := by
    rwa [ Real.lt_log_iff_exp_lt ( by norm_num ) ];
  rw [ show ( 131072 / 6561 : ℝ ) = ( 2 ^ 17 ) / ( 3 ^ 8 ) by norm_num, Real.log_div, Real.log_pow, Real.log_pow ] at h_log_approx <;> norm_num at *;
  rw [ Real.log_div ] <;> linarith


/-- Main theorem (BCZ cluster=2 universality, RESEARCH-OPEN):
    Under BCZ chain dynamics, the probability of a cluster of size ≥ 3
    at quantile q ≥ clusterTwoThreshold equals 0. -/
theorem bcz_cluster_two_universality (q : ℝ) (hq : q ≥ clusterTwoThreshold) :
    ∀ (X : ℕ → ℝ × ℝ),
      -- X is a BCZ chain trajectory (placeholder def)
      True := by
  -- This requires the BCZ chain definition + the t* = 2/9 critical pair argument
  -- + integration theory for P_BCZ.
  sorry -- RESEARCH-OPEN

end