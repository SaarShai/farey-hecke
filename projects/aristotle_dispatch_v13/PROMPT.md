# Aristotle v13 — `three_cluster_q5`: Explicit 3-cluster witness for Taha G₅-BCZ map (q=5)

## Goal

Make `BCZ5Witness.lean` compile (`lake build`, Mathlib **v4.28.0**), **0 sorry**,
`#print axioms three_cluster_q5` = `[propext, Classical.choice, Quot.sound]`.

This is the **reverse direction of the arithmeticity dichotomy at q=5**: exhibit three
consecutive orbit points in `T⁵` (q=5, λ=φ=(1+√5)/2) with observable `P < X(5) = 1/φ³ = √5−2`.
This formally proves `cluster_size_le_two` FAILS at q=5 (non-arithmetic Hecke group G₅),
complementing the proved arithmetic trio {3,4,6} (v8, v11, v12).

## Structure

The file is a **certificate-based witness proof** — no sorry stubs for math, only
Lean mechanics may need fixing.

Key definitions (do NOT change):
- `phi5 : ℝ := (1 + Real.sqrt 5) / 2`  (φ = golden ratio)
- `s5 : ℝ := Real.sqrt 5`
- `X5 : ℝ := s5 - 2`  (= √5−2 = 1/φ³)
- `a0,b0` = (3/5, 1/3);  `a1,b1` = (1/3, −4/15+√5/3);  `a2,b2` = (−4/15+√5/3, 11/30+√5/30)
- `inT5`, `inLastBranch`, `Pobs5`, `bczMap5` — domain, branch, observable, map definitions
- `X5_eq_inv_phi5_cubed : X5 = 1 / phi5 ^ 3`  (companion identity lemma)

**Main theorem** `three_cluster_q5`: conjunction of
1. domain membership: all 3 points in T⁵
2. last-branch membership: all 3 points satisfy a + φb > 1
3. map steps: `bczMap5 (a0,b0) = (a1,b1)` and `bczMap5 (a1,b1) = (a2,b2)`
4. observables: `Pobs5(aᵢ,bᵢ) < X5` for i=0,1,2

## Exact witness certificates (sympy-verified, exact Q(√5) arithmetic)

**φ = (1+√5)/2, X(5) = √5 − 2 ≈ 0.2361**

| Point | a | b | k | P = a·b | X − P |
|-------|---|---|---|---------|-------|
| 0 | 3/5 | 1/3 | 2 | 1/5 | √5 − 11/5 |
| 1 | 1/3 | −4/15 + √5/3 | 1 | −4/45 + √5/9 | −86/45 + 8√5/9 |
| 2 | −4/15+√5/3 | 11/30+√5/30 | — | −19/450+17√5/150 | −881/450+133√5/150 |

**k₁=2 floor certificate:**
- (1 + 3/5)/(φ·1/3) = 12(√5−1)/5 ≈ 2.9666
- ratio − 2 = −22/5 + 12√5/5 > 0  (since 12√5 > 22, i.e., 5·144 > 484 ✓)
- 3 − ratio = 27/5 − 12√5/5 > 0  (since 27 > 12√5, i.e., 729 > 720 ✓)

**k₂=1 floor certificate:**
- (1 + 1/3)/(φ·b₁) = 210/109 − 10√5/109 ≈ 1.7215
- ratio − 1 = 101/109 − 10√5/109 > 0  (since 101 > 10√5, i.e., 10201 > 500 ✓)
- 2 − ratio = 8/109 + 10√5/109 > 0  (trivially, both terms positive ✓)

**All inequalities of the form p + q·√5 > 0:**
- Strategy: `nlinarith [s5_sq, s5_pos, s5_gt_two, s5_lt_3]` with squaring hints.
- Core fact: `s5 * s5 = 5` (from `Real.mul_self_sqrt`).
- Bounds: 2 < √5 < 3.

**Floor evaluation strategy:**
- Use `Int.floor_eq_iff.mpr` with `⟨lower_bound_proof, upper_bound_proof⟩`.
- `le_div_iff` / `div_lt_iff` with `positivity` for denominator positivity.

## Constraints

- 0 `sorry` at completion; standard axioms `[propext, Classical.choice, Quot.sound]` only.
- Do NOT use `aesop`, `grind`, `simp_all`, or `decide` for the arithmetic goals.
- Acceptable: `nlinarith`, `linarith`, `norm_num`, `ring`, `rw`, `simp only [named]`,
  `by_contra`, `rcases`, `omega`, `Int.floor_eq_iff`, `push_cast`, `positivity`.
- Do NOT change the theorem statement, the witness coordinates, or the threshold `X5`.
- Do NOT change `phi5`, `s5`, `X5`, `a0..b2`, `inT5`, `inLastBranch`, `Pobs5`, `bczMap5`.
- `nlinarith` hints should use explicit products from `s5_sq` (i.e., `s5 * s5 = 5`);
  do NOT use `Real.sqrt_lt'` or floating-point approximations.
- The file may need `set_option maxHeartbeats` for heavy nlinarith calls (up to 800000).

## What likely needs fixing (Lean mechanics only)

1. **`Int.floor_eq_iff` usage**: in Mathlib v4.28.0 the signature may require a cast
   or `show (n : ℝ) ≤ ...` wrapper; adjust if needed.
2. **`le_div_iff` / `div_lt_iff`**: may need `₀` suffix (`le_div_iff₀`) in v4.28.0.
3. **`push_cast` after `rw [k1_eq_two]`**: coercion `((2:ℤ):ℝ) = 2` must be resolved.
4. **`map_step_01 / map_step_12` ring equations**: `ring_nf; linarith` vs `ring`; adjust
   if `phi5` definition unfolding is needed.
5. **`nlinarith` hint sufficiency**: for domain/branch membership proofs, may need products
   like `mul_pos phi5_pos b0_pos` or `sq_nonneg (s5 - 2)` added to hint list.
6. **`positivity`** for denominator proofs in floor certificates: verify it handles
   `phi5 * b1 > 0` (may need `mul_pos phi5_pos b1_pos`).

## Report

List all changes made, the exact `nlinarith` hint sets for any hard inequalities,
and paste `#print axioms three_cluster_q5` and `#print axioms X5_eq_inv_phi5_cubed`.
