/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ Onset = q* (v10)

## Goal

Prove `bczOnsetEqualsQStar`: the onset quantile q* at which size-≥3 runs of
extreme BCZ-orbit pairs vanish is exactly

  q*_BCZ = (11 − 8·ln(3/2)) / 9.

The theorem bridges two independently established results:

1. **`bczProb_eq_value`** (the measure result, axiom stub from v5):
   The BCZ-invariant probability of the low-product region
     S = {(x,y) ∈ T : x·y < 2/9}
   is `(8·ln(3/2) − 2)/9 ≈ 0.138`.
   Proved via four-region Fubini split in `BCZThresholdIntegration.lean` (v5).

2. **`cluster_size_le_two_clean`** (the cluster bound, axiom stub from v8):
   For any BCZ orbit in T: P_i < 2/9 ∧ P_{i+1} < 2/9 → P_{i+2} ≥ 2/9.
   Proved via six named lemmas in `BCZClusterCleanProof.lean` (v8).

**Bridge**: q*_BCZ = 1 − μ(S) = 1 − (8·ln(3/2)−2)/9 = (11 − 8·ln(3/2))/9.
The `ring` tactic closes this once `bczProb_eq_value` is substituted.

## Terminology clarification

- The **product threshold** is t* = 2/9: pairs (x,y) with x·y < t* are "extreme".
- The **BCZ probability** of extreme pairs is μ(S) = (8·ln(3/2)−2)/9 ≈ 0.138
  (NOT equal to 2/9 ≈ 0.222; these are different objects).
- The **onset quantile** q* = 1 − μ(S) ≈ 0.862 is the largest quantile level at
  which the cluster-size-2 bound holds at the invariant-measure level.

## Proof architecture

```
bczProb_eq_value               cluster_size_le_two_clean
  (v5 axiom stub)                (v8 axiom stub)
        |                                |
        |  μ(S) = (8·ln(3/2)−2)/9       |  P_i < 2/9 ∧ P_{i+1} < 2/9
        |                                |  → P_{i+2} ≥ 2/9
        +---------------+----------------+
                        |
               bczOnsetEqualsQStar:
          bczOnset = (11 − 8·ln(3/2)) / 9
          and the cluster bound holds at threshold 2/9
          and μ(S) = (8·ln(3/2)−2)/9
```

## Axiom inventory

This file introduces exactly TWO axioms:
- `bczProb_eq_value`           ← BCZThresholdIntegration.lean (v5)
- `cluster_size_le_two_clean`  ← BCZClusterCleanProof.lean (v8)

All remaining theorems are proved from these two axioms with `ring`, `linarith`,
`nlinarith`, `Real.log_pos`, `Real.add_one_le_exp`, and `norm_num`.
-/

open Real Set MeasureTheory

noncomputable section

/-! ## §1. Definitions -/

/-- The (open) BCZ triangle T = {(x,y) : 0 < x,y < 1, x+y > 1}. -/
def bczTriangle : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 < 1 ∧ 0 < p.2 ∧ p.2 < 1 ∧ p.1 + p.2 > 1}

/-- The BCZ map T(x, y) = (y, ⌊(1+x)/y⌋·y − x). -/
noncomputable def bczMap (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / p.2⌋
  (p.2, (k : ℝ) * p.2 - p.1)

/-- The BCZ probability of the low-product region:
    μ_BCZ({xy < 2/9}) = 2 · λ({(x,y) ∈ T : xy < 2/9})
    where λ is Lebesgue measure on ℝ². -/
noncomputable def bczProbLow : ℝ :=
  ∫ _x in (bczTriangle ∩ {p | p.1 * p.2 < 2 / 9}), (2 : ℝ)

/-- The onset quantile: q*_BCZ = 1 − μ_BCZ({xy < 2/9}). -/
noncomputable def bczOnset : ℝ := 1 - bczProbLow

/-! ## §2. Axiom stubs for the dependency results -/

/-- ### bczProb_eq_value
    SOURCE: `BCZThresholdIntegration.lean` (aristotle_dispatch_v5).
    The BCZ invariant-measure probability of the region {xy < 2/9} equals
    (8·ln(3/2)−2)/9 ≈ 0.13819.
    PROOF METHOD (in v5): Fubini → iterated integral → four x-regions:
      (i)   x ∈ (0, 2/9):   ∫_{1-x}^1 2 dy = 2x; outer = 4/81
      (ii)  x ∈ (2/9, 1/3): upper y-limit = 2/(9x); → (4/9)ln(3/2) − 13/81
      (iii) x ∈ (1/3, 2/3): empty; integral = 0
      (iv)  x ∈ (2/3, 1):   symmetric to (ii); → (4/9)ln(3/2) − 9/81
    Sum = (8/9)·ln(3/2) − 2/9 = (8·ln(3/2) − 2)/9. -/
axiom bczProb_eq_value :
    bczProbLow = (8 * Real.log (3 / 2) - 2) / 9

/-- ### cluster_size_le_two_clean
    SOURCE: `BCZClusterCleanProof.lean` (aristotle_dispatch_v8).
    In every BCZ orbit confined to T, two consecutive extreme products
    (both < 2/9) force the next product ≥ 2/9.
    PROOF METHOD (in v8): six named lemmas —
      Step 1: (a+b>1, ab<2/9) → b<1/3 ∨ b>2/3 (quadratic squeeze)
      Step 2: b>2/3 contradicts a+c = k·b ≥ b with a,c < 2/(9b) → a+c < 4/(9b) < b
      Step 3: therefore b < 1/3
      Step 4: b+c > 1 and b<1/3 → c > 2/3
      Step 5: ⌊(1+b)/c⌋ = 1 when b<1/3, c>2/3
      Step 6: d = c−b, so cd = c(c−b) > (1−b)(1−2b) > 2/9 for b ∈ (0,1/3). -/
axiom cluster_size_le_two_clean :
    ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ bczTriangle) →
      (∀ n, orbit (n + 1) = bczMap (orbit n)) →
      ∀ i,
        (orbit i).1 * (orbit i).2 < 2 / 9 →
        (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
        (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9

/-! ## §3. Main theorem -/

/-- **bczOnset_eq**: the onset quantile equals (11 − 8·ln(3/2)) / 9.
    Proof: unfold bczOnset, substitute bczProb_eq_value, ring. -/
theorem bczOnset_eq :
    bczOnset = (11 - 8 * Real.log (3 / 2)) / 9 := by
  unfold bczOnset
  rw [bczProb_eq_value]
  ring

/-- **bczOnsetEqualsQStar** (the headline theorem):

    The BCZ extreme-gap cluster structure pins the onset quantile at
      q*_BCZ = (11 − 8·ln(3/2)) / 9 ≈ 0.86181.

    The conjunction has three parts:

    (1) **Onset value**: `bczOnset = (11 − 8·ln(3/2)) / 9`.
    (2) **Cluster bound** (from v8): maximal cluster size ≤ 2 at threshold 2/9.
    (3) **Measure value** (from v5): μ_BCZ({xy < 2/9}) = (8·ln(3/2)−2)/9. -/
theorem bczOnsetEqualsQStar :
    bczOnset = (11 - 8 * Real.log (3 / 2)) / 9
    ∧ (∀ (orbit : ℕ → ℝ × ℝ),
        (∀ n, orbit n ∈ bczTriangle) →
        (∀ n, orbit (n + 1) = bczMap (orbit n)) →
        ∀ i,
          (orbit i).1 * (orbit i).2 < 2 / 9 →
          (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
          (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9)
    ∧ (bczProbLow = (8 * Real.log (3 / 2) - 2) / 9) :=
  ⟨bczOnset_eq, cluster_size_le_two_clean, bczProb_eq_value⟩

/-! ## §4. Elementary consequences -/

/-- log(3/2) > 1/4, needed for bczProbLow_pos. -/
theorem log_three_halves_gt_quarter : Real.log (3 / 2) > 1 / 4 := by
  rw [show (1:ℝ)/4 = Real.log (Real.exp (1/4)) from (Real.log_exp (1/4)).symm]
  apply Real.log_lt_log (Real.exp_pos _)
  have h1 : Real.exp (1/4) ^ 4 < (3/2 : ℝ) ^ 4 := by
    have : Real.exp (1/4) ^ 4 = Real.exp 1 := by
      rw [← Real.exp_nat_mul]
      norm_num
    rw [this]
    have := Real.exp_one_lt_three
    norm_num
    linarith
  exact lt_of_pow_lt_pow_left₀ 4 (by positivity) h1

/-- log(3/2) < 1, needed for bczProbLow_lt_one. -/
theorem log_three_halves_lt_one : Real.log (3 / 2) < 1 := by
  rw [show (1:ℝ) = Real.log (Real.exp 1) from (Real.log_exp 1).symm]
  apply Real.log_lt_log (by norm_num : (0:ℝ) < 3/2)
  have h := Real.add_one_le_exp (1 : ℝ)
  linarith

/-- bczProbLow is positive: the threshold region has positive measure. -/
theorem bczProbLow_pos : 0 < bczProbLow := by
  rw [bczProb_eq_value]
  have h := log_three_halves_gt_quarter
  linarith

/-- bczProbLow is less than 1. -/
theorem bczProbLow_lt_one : bczProbLow < 1 := by
  rw [bczProb_eq_value]
  have h := log_three_halves_lt_one
  linarith

/-- The onset is strictly between 0 and 1: it is a genuine quantile level. -/
theorem bczOnset_in_unit_interval : 0 < bczOnset ∧ bczOnset < 1 := by
  constructor
  · show 0 < 1 - bczProbLow
    linarith [bczProbLow_lt_one]
  · show 1 - bczProbLow < 1
    linarith [bczProbLow_pos]

/-- q*_BCZ + μ(S) = 1: the onset and the low-product measure are complementary. -/
theorem onset_plus_measure_eq_one :
    bczOnset + bczProbLow = 1 := by
  unfold bczOnset; ring

theorem bczOnset_lt_one : bczOnset < 1 :=
  bczOnset_in_unit_interval.2

theorem bczOnset_pos : 0 < bczOnset :=
  bczOnset_in_unit_interval.1

end
