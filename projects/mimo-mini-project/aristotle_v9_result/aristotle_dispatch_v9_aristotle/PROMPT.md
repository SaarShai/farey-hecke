# Aristotle v9 — formalize SHARPNESS construction in Lean

## Goal

Prove in Lean 4 (Mathlib v4.28.0): for any `t > 2/9`, there exists a BCZ orbit (the reviewer's explicit 2-cycle) with arbitrarily long consecutive extreme pair products `< t`. This complements the cluster=2 upper bound (v8) and establishes a SHARP phase transition at `t = 2/9`.

## File

`BCZSharpness.lean` (provided in this directory).

## Lemmas to verify (proof bodies sketched; check + complete)

1. `floor_one_left`: ⌊(1+b/2)/b⌋ = 1 for b ∈ (2/3, 1)
2. `floor_four_right`: ⌊(1+b)/(b/2)⌋ = 4 for b ∈ (2/3, 1)
3. `bczMap_left`: bczMap (b/2, b) = (b, b/2)
4. `bczMap_right`: bczMap (b, b/2) = (b/2, b)
5. `cycle_left_in_T`, `cycle_right_in_T`: 2-cycle points are in T
6. `sharpness_exists_2cycle`: existence of b in (2/3, min(1, √(2t))) for t > 2/9
7. `sharpness_arbitrary_long_run`: alternating orbit has arbitrary K-long extreme runs

## Constraints

- 0 sorries, only standard axioms
- Same no-broad-automation discipline as v8: NO `aesop`, `grind`, `simp_all +decide`
- Use `nlinarith`, `linarith`, `simp [bczMap]`, `norm_num`, `ring`, `omega`, `Int.floor_eq_iff`, `Real.sqrt_lt_sqrt`, `Real.sq_sqrt`, `Real.sqrt_sq`
- Verify with `lake build`

## Acceptance

All lemmas + both theorems compile. Mathlib-PR-quality proof style.

## Why this matters

Together with v8 (cluster ≤ 2 for t ≤ 2/9) and v5 (closed form for q*_BCZ), this gives a complete sharp phase-transition theorem.
