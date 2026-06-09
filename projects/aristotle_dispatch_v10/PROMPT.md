# Aristotle v10 — bczOnsetEqualsQStar: onset = q*_BCZ

## Goal

Prove `bczOnsetEqualsQStar` in `BCZOnsetQStar.lean`: the BCZ extreme-gap cluster
onset quantile equals

  q*_BCZ = (11 − 8·ln(3/2)) / 9 ≈ 0.86181.

This bridges two previously dispatched results (v5 and v8), both included as
clearly-labeled `axiom` stubs with their source files and proof methods.

## File

`BCZOnsetQStar.lean` (provided). It contains:
- Two definitions: `bczProbLow`, `bczOnset`.
- Two axiom stubs: `bczProb_eq_value` (from v5) and `cluster_size_le_two_clean` (from v8).
- The main theorem `bczOnsetEqualsQStar` (conjunction of 3 parts).
- Supporting theorems: `bczOnset_eq`, `bczProbLow_pos`, `bczProbLow_lt_one`,
  `bczOnset_in_unit_interval`, `onset_plus_measure_eq_one`, `bczOnset_lt_one`, `bczOnset_pos`.

## What you need to do

1. **Make the file compile** against Mathlib v4.28.0 with `lake build`.

2. **Fix any proof terms** that don't type-check as written. The core theorems
   (`bczOnsetEqualsQStar`, `bczOnset_eq`, `onset_plus_measure_eq_one`) should be
   trivial (ring + the two axioms). The work is in `bczProbLow_pos` and
   `bczProbLow_lt_one`.

3. **Key proofs that need care**:

   ### bczProbLow_lt_one
   Goal: `(8 * Real.log (3/2) - 2) / 9 < 1`, i.e., `log(3/2) < 1`.
   Since `3/2 < e = exp(1)`:
   ```
   have h := Real.add_one_le_exp (1 : ℝ)  -- gives 1 + 1 ≤ exp(1), so exp(1) ≥ 2 > 3/2
   ```
   Actually `add_one_le_exp` gives `1 + x ≤ exp(x)` at `x = 1`, so `exp(1) ≥ 2 > 3/2`. ✓

   ### bczProbLow_pos
   Goal: `(8 * Real.log (3/2) - 2) / 9 > 0`, i.e., `log(3/2) > 1/4`.
   Strategy: show `exp(1/4) < 3/2` via `(3/2)^4 > exp(1)` (since `(3/2)^4 = 81/16 > 2.7 > exp(1)`),
   then apply monotonicity of exp/log.

   The exact sequence:
   ```
   -- exp(1) < 81/16 = (3/2)^4  (since exp(1) ≥ 2 from add_one_le_exp, and... actually
   --   exp(1) ≈ 2.718 and (3/2)^4 = 5.0625, so exp(1) < (3/2)^4).
   -- From this: exp(1/4) < 3/2 (taking 4th roots).
   -- From this: log(3/2) > 1/4 (log is strictly increasing).
   ```

   The Lean proof of `exp(1) < (3/2)^4` can use:
   - `Real.sum_le_exp_of_nonneg (x := 1) (n := N)` gives a LOWER bound on `exp(1)`,
     which isn't directly what we need for an UPPER bound.
   - Better: use `Real.exp_lt_pow` or prove `exp(1) < 3` first (simpler target):
     `Real.sum_le_exp_of_nonneg` at `n = 5` gives `exp(1) ≥ 1 + 1 + 1/2 + 1/6 + 1/24 + 1/120 ≈ 2.717`.
     But we need an UPPER bound. Use `exp(1) ≤ exp(1)` is circular.
   - Instead prove `exp(1) < 3` from the known `Real.exp_one_lt_d9` (if available) or
     from the bound `exp(1) < 4` via `exp_le_pow_of_le_log` type lemmas.
   - Actually, the simplest path: Mathlib has `Real.exp_one_lt_d9 : exp 1 < 2.7182818286`
     or similar. Check if available.
   - If not, use: from `sum_le_exp` at n=5, exp(1) ≥ 163/60. Upper bound: note
     exp(x) ≤ (1-x)⁻¹ for 0 < x < 1 (geometric series, but this gives exp(1) ≤ ∞, useless).
   - Cleanest: prove `exp(1) < 3` using the fact that `exp` is continuous, and the
     Taylor polynomial bound. `Real.sum_le_exp_of_nonneg` can be combined with
     `Finset.geom_sum_mul` type tricks, or just `norm_num` with a numerically verified bound.
   - **Recommended**: use `native_decide` or `norm_num` with a `Real.exp_bound`-type lemma.
     In Mathlib4 / Lean4.28: try `norm_num [Real.exp_approx_succ]` or look for
     `Real.exp_one_gt_d9` / `Real.exp_one_lt_d9`.

   Alternative proof of `log(3/2) > 1/4` without exp bounds:
   - Use `Real.log_nonneg (by norm_num : 1 ≤ 3/2)` for `log(3/2) ≥ 0`, which is too weak.
   - Use `Real.log_lt_of_lt_exp` and the fact that `3/2 = exp(log(3/2))` is circular.
   - Use the bound `log(1+t) ≥ t/(1+t)` for `t > 0`:
     at `t = 1/2`: `log(3/2) ≥ (1/2)/(3/2) = 1/3 > 1/4`.
     Mathlib: `Real.log_le_sub_one_of_le` or `Real.add_pow_le_pow_mul_pow_of_sq_le_sq`.
     Or prove it from `exp(log(3/2)) = 3/2 ≥ 1 + log(3/2)` (add_one_le_exp at log(3/2)):
     this gives `1 + log(3/2) ≤ 3/2`, so `log(3/2) ≤ 1/2` — UPPER bound, wrong direction.
   - Use: `log(1+t) ≥ t - t²/2` (Taylor with Lagrange remainder) at `t = 1/2`:
     `log(3/2) ≥ 1/2 - 1/8 = 3/8 > 1/4`. Need `Real.log_le_sub_sq_of_pos` or prove it.
     From exp: `exp(log(3/2)) = 3/2`. Bound `3/2 ≤ exp(1/2 - log(3/2) + (1/2-log(3/2))²/2 + ...)`?
     Circular again.
   - **Most direct in Mathlib**: use `Real.one_sub_inv_le_log`:
     NOT standard. Use `Real.log_one_plus_le` / `Real.log_le_...`.
   - **Recommendation**: Rewrite `bczProbLow_pos` as:
     ```lean
     have hlog : Real.log (3 / 2) > 0 := Real.log_pos (by norm_num)
     have hlog2 : Real.log (3 / 2) ≤ 1 / 2 := by
       have := Real.add_one_le_exp (Real.log (3/2))
       rw [Real.exp_log (by norm_num)] at this
       linarith
     -- So log(3/2) ∈ (0, 1/2). We need > 1/4.
     -- Use: 3/2 ≥ exp(1/4)? Need to show exp(1/4) ≤ 3/2. Try:
     -- exp(1/4) ≤ 1 + 1/4 + (1/4)^2/2 + (1/4)^3/6 + ... but sum_le_exp gives lower bound.
     ```
   - **Fallback**: if the exp bound is hard to formalize, use a different pivot:
     `Real.log (3/2) > 0` (log_pos, since 3/2 > 1) and `bczProbLow_pos` can be proved
     more directly by arguing `bczProbLow = (8*log(3/2)-2)/9 > 0` iff `log(3/2) > 1/4`,
     and since `3/2 = (3/2)^1 > 1` we at least get `log(3/2) > 0`. But `0 > 1/4` is false.
     The `1/4` lower bound on log really requires a nontrivial argument.
   - **Final recommendation**: prove `bczProbLow_pos` using the chain:
     `(3/2)^4 = 81/16 > 3 > exp(1)` [since exp(1) < 3 from e < 3], so `3/2 > exp(1/4)`,
     so `log(3/2) > 1/4`. For `exp(1) < 3`:
     use `Real.sum_le_exp_of_nonneg (1:ℝ) 5` to get `exp(1) ≥ 163/60 ≈ 2.717` (lower bound),
     then... we still need the upper bound. Try `norm_num` extended with `Real.exp_approx`:
     ```lean
     have : Real.exp 1 < 3 := by norm_num [show Real.exp 1 = Real.exp 1 from rfl]
     ```
     OR use:
     ```lean
     have : Real.exp 1 < 3 := by
       have h4 : (4 : ℝ) ≤ Real.exp 1 * Real.exp 1 := by
         have := Real.add_one_le_exp (Real.exp 1 - 1)  -- not helpful
         ...
     ```
     OR simply:
     ```lean
     have hlt3 : Real.exp 1 < 3 := by
       have : (2 : ℝ) ≤ Real.exp 1 := by
         have := Real.add_one_le_exp (1 : ℝ); linarith
       -- exp(1)^3 = exp(3) and exp(3) > 20, so exp(1) > 20^(1/3) > 2.7... Still needs UB.
       -- Use: exp(1) < exp(2) = exp(1)^2 and exp(2) ≤ exp(1)^2... circular.
       -- Just: exp(1) < 3 is in Mathlib as Real.exp_one_lt_d9 or similar.
       exact Real.exp_one_lt_three  -- check if this exists
     ```

## Approach: if standard Mathlib lemma names fail

If `Real.exp_one_lt_three` or `Real.exp_one_lt_d9` is not available, use this proof:
```lean
-- exp(1) < 3 via: 1 + 1 ≤ exp(1) [from add_one_le_exp] and
-- exp(1) * exp(-1) = 1 → if exp(1) ≥ 3 then exp(-1) ≤ 1/3.
-- But add_one_le_exp at -1: 1 + (-1) ≤ exp(-1), so 0 ≤ exp(-1). Not useful.
-- Use: sum_le_exp at n=5 for x=1 gives exp(1) ≥ 163/60 ≈ 2.716... (lower bound only).
-- For UPPER bound: note exp(1) ≤ (1 + 1/n)^n * e correction... complex.
-- Most direct Mathlib path: Real.exp_lt_pow (Real.two_le_exp_iff...) or
-- use Nat.lt_exp_self type results, or just use:
have : (Real.exp 1)^3 ≥ 20 := by ...  -- still needs UB for exp(1).
-- Cleanest known-good proof:
have hlt : Real.exp 1 < 3 := by
  have h := Real.sum_le_exp_of_nonneg (show (0:ℝ) ≤ 1 by norm_num) (n := 5)
  -- h : ∑ k in Finset.range 5, 1^k / k! ≤ exp(1)
  -- That's only a lower bound. We need an upper bound.
  -- Use: for x > 0, exp(x) = ∑ x^k/k! + remainder(x,N) where
  -- remainder ≤ x^(N+1) / (N+1)! * exp(x) (standard Lagrange).
  -- This requires knowing exp(1) first... circular.
  -- ALTERNATIVE: just use decide / norm_num with the Mathlib4 exp approximation.
  norm_num [Real.exp_approx_succ, Real.exp_approx_zero]
```

## Constraints

1. 0 sorries in any proved theorem (sorries in axiom stubs are documented, not compile errors).
2. No broad `aesop`/`grind`/`simp_all +decide`.
3. Acceptable: `ring`, `linarith`, `nlinarith`, `norm_num`, `exact`, `rw`, `simp [specific_lemma]`,
   `Real.log_pos`, `Real.log_lt'`, `Real.exp_pos`, `Real.exp_log`, `Real.log_exp`,
   `Real.log_lt_log`, `Real.sum_le_exp_of_nonneg`, `Real.add_one_le_exp`.

## Acceptance

- `lake build` succeeds with 0 errors.
- `bczOnsetEqualsQStar` compiles (it is a conjunction of the 3 parts).
- `bczOnset_eq` compiles (ring + rw [bczProb_eq_value]).
- `bczProbLow_pos` and `bczProbLow_lt_one` compile.
- Report any proof terms changed and why.

## Mathematical note on the theorem statement

The theorem packages all three facts:
1. onset value = (11 - 8·ln(3/2))/9   [ring from bczProb_eq_value]
2. cluster_size_le_two_clean            [axiom, the v8 six-step proof]  
3. bczProbLow = (8·ln(3/2)-2)/9        [axiom, the v5 Fubini integration]

The "bridge" sentence is:
  onset = 1 − bczProbLow = 1 − (8·ln(3/2)−2)/9 = (11−8·ln(3/2))/9.
This is the only non-trivial content beyond the two axiom stubs.
