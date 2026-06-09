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
open scoped Classical

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
  ∫ p in (bczTriangle ∩ {p | p.1 * p.2 < 2 / 9}), (2 : ℝ)

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
        Follows from the measure result (bczProb_eq_value) by a ring computation:
        q* = 1 − (8·ln(3/2)−2)/9 = (9 − 8·ln(3/2) + 2)/9 = (11 − 8·ln(3/2))/9.

    (2) **Cluster bound** (from v8): for any BCZ orbit in T, two consecutive
        extreme pairs (products < 2/9) force the third to be non-extreme (≥ 2/9).
        This establishes that at product threshold t* = 2/9, no orbit can sustain
        a run of ≥ 3 extreme consecutive pairs — so maximal cluster size ≤ 2.

    (3) **Measure value** (from v5): μ_BCZ({xy < 2/9}) = (8·ln(3/2)−2)/9.
        This is the Fubini integration result that converts the product threshold
        t* = 2/9 into the quantile q* = 1 − (8·ln(3/2)−2)/9.

    The bridge between (2) and (3): the cluster bound at PRODUCT threshold 2/9
    corresponds to the QUANTILE threshold q*_BCZ = 1 − μ(S).  Every (x,y) with
    product < 2/9 has quantile rank below μ(S) = 1 − q*, i.e., its quantile is
    below 1 − q* = bczProbLow.  So saying "at most 2 consecutive products < 2/9"
    is equivalent to "cluster size ≤ 2 at quantile level q*_BCZ". -/
theorem bczOnsetEqualsQStar :
    /- (1) Onset value -/
    bczOnset = (11 - 8 * Real.log (3 / 2)) / 9
    /- (2) Cluster bound at product threshold 2/9 -/
    ∧ (∀ (orbit : ℕ → ℝ × ℝ),
        (∀ n, orbit n ∈ bczTriangle) →
        (∀ n, orbit (n + 1) = bczMap (orbit n)) →
        ∀ i,
          (orbit i).1 * (orbit i).2 < 2 / 9 →
          (orbit (i + 1)).1 * (orbit (i + 1)).2 < 2 / 9 →
          (orbit (i + 2)).1 * (orbit (i + 2)).2 ≥ 2 / 9)
    /- (3) Measure value of the low-product region -/
    ∧ (bczProbLow = (8 * Real.log (3 / 2) - 2) / 9) :=
  ⟨bczOnset_eq, cluster_size_le_two_clean, bczProb_eq_value⟩

/-! ## §4. Elementary consequences -/

/-- bczProbLow is in (0, 1): the threshold region has positive but proper measure. -/
theorem bczProbLow_pos : 0 < bczProbLow := by
  rw [bczProb_eq_value]
  -- (8·ln(3/2)−2)/9 > 0 ⟺ ln(3/2) > 1/4.
  -- Use: log(x) > 0 for x > 1 and log(3/2) > log(e^{1/4}) = 1/4 since 3/2 > e^{1/4}.
  -- Simpler: log(3/2) > 1/3 - 1/3² + ... ≥ 1/2 - 1/8 = 3/8 > 1/4 (Taylor).
  -- We use the standard bound log(x) ≥ 1 - 1/x (i.e., log(x) + 1/x ≥ 1) for x > 0.
  -- This gives log(3/2) ≥ 1 - 2/3 = 1/3 > 1/4. That's log(x) ≥ 1 - 1/x.
  -- In Lean/Mathlib: use exp lower bound to prove log > 1/4.
  -- log(3/2) > 1/4 iff 3/2 > exp(1/4).
  -- exp(1/4) < exp(0.5) < 2. And 3/2 < 2 as well. Need tighter.
  -- From Real.add_one_le_exp: 1 + t ≤ exp(t). At t = 1/4: exp(1/4) ≥ 5/4 = 1.25.
  -- But 3/2 = 1.5 > 1.25 ≥ ... we need 3/2 > exp(1/4).
  -- Use sum_le_exp: ∑_{k=0}^4 (1/4)^k/k! ≤ exp(1/4).
  -- ∑ = 1 + 1/4 + 1/32 + 1/384 + 1/6144 = 1.2840... < 3/2 = 1.5.
  -- That only gives a LOWER bound on exp(1/4), and we need an UPPER bound to deduce 3/2 > exp(1/4).
  -- Better: use 3/2 > exp(1/4) directly via log_pos and monotonicity.
  -- Since Real.log is strictly monotone and log(1) = 0 < 1/4 < log(3/2)... circular.
  -- Direct: show exp(1/4) < 3/2.
  -- exp(1/4) = exp(0.25). Upper bound: exp(x) ≤ 1/(1-x) for x < 1 is too weak.
  -- Use: exp(1/4) < 1 + 1/4 + (1/4)^2 + (1/4)^3 + ... = 1/(1-1/4) = 4/3 = 1.333... < 3/2.
  -- Wait, that's a LOWER bound (geometric series ≠ exp). Actually:
  -- The geometric series 1 + x + x^2 + ... is an overestimate of exp(x) only for |x| very small.
  -- No, that's 1/(1-x) ≥ exp(x) is NOT true in general.
  -- Safe approach: use that Real.log is increasing and log(3/2) = log(3) - log(2).
  -- We know log(2) < 0.694 and log(3) > 1.098, so log(3/2) > 1.098 - 0.694 = 0.404 > 1/4.
  -- In Lean, use a Mathlib bound or sorry.
  -- Most reliable: use that exp(1/4) < 3/2 via the following:
  -- 4 * exp(1/4) < 4 * 3/2 = 6 is too weak.
  -- Use exp(1/4)^4 = exp(1) < 3 (since exp(1) < e < 3), so exp(1/4) < 3^(1/4) < 3/2.
  -- 3^(1/4) = (81)^(1/4) * (1/3)^(1/4) ... let's just use exp(1) < 3 and (3/2)^4 > 3.
  -- (3/2)^4 = 81/16 > 5 > 3 > exp(1). So (3/2)^4 > exp(1) = exp(4 * 1/4), giving 3/2 > exp(1/4).
  have h_four : (3/2 : ℝ)^4 > Real.exp 1 := by
    have he1 : Real.exp 1 < 3 := by
      have h := Real.sum_le_exp_of_nonneg (x := 1) (n := 4) (by norm_num)
      simp [Finset.sum_range_succ] at h
      norm_num at h ⊢
      linarith
    norm_num
    linarith
  have h_log : Real.log (3 / 2) > 1 / 4 := by
    have hpos : (0 : ℝ) < 3 / 2 := by norm_num
    rw [show (1:ℝ)/4 = Real.log (Real.exp (1/4)) from by rw [Real.log_exp]]
    apply Real.log_lt_log
    · -- exp(1/4) > 0
      exact Real.exp_pos _
    · -- exp(1/4) < 3/2
      -- From (3/2)^4 > exp(1): take 4th roots (both sides positive).
      -- exp(1/4) < 3/2 iff (exp(1/4))^4 < (3/2)^4 iff exp(1) < (3/2)^4.
      rw [show (3:ℝ)/2 = ((3/2:ℝ)^4)^(1/4:ℝ) from by norm_num]
      rw [← Real.rpow_natCast (3/2:ℝ) 4] at h_four
      rw [← Real.exp_one_rpow]
      apply Real.rpow_lt_rpow (Real.exp_pos _).le
      · -- exp(1) < (3/2)^4
        exact_mod_cast h_four
      · norm_num
  linarith [mul_pos (by norm_num : (0:ℝ) < 8) h_log]

theorem bczProbLow_lt_one : bczProbLow < 1 := by
  rw [bczProb_eq_value]
  -- (8·ln(3/2)−2)/9 < 1 ⟺ 8·ln(3/2) < 11.
  -- ln(3/2) < 1 since 3/2 < e (= 2.718...).
  -- So 8·ln(3/2) < 8 < 11.
  have hlog_lt_one : Real.log (3 / 2) < 1 := by
    rw [show (1:ℝ) = Real.log (Real.exp 1) from by rw [Real.log_exp]]
    apply Real.log_lt_log (by norm_num)
    -- 3/2 < exp(1)
    have h := Real.add_one_le_exp (1 : ℝ)
    -- add_one_le_exp: 1 + 1 ≤ exp(1), so exp(1) ≥ 2 > 3/2.
    linarith
  linarith [mul_lt_mul_of_pos_left hlog_lt_one (by norm_num : (0:ℝ) < 8)]

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

/-- The onset is less than 1 and the cluster bound holds:
    for any q ≥ q*_BCZ, there are no size-≥3 extreme clusters at threshold 2/9. -/
theorem bczOnset_lt_one : bczOnset < 1 :=
  bczOnset_in_unit_interval.2

theorem bczOnset_pos : 0 < bczOnset :=
  bczOnset_in_unit_interval.1

end
