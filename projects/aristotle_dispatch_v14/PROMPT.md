# Aristotle v14 — `three_cluster_q7`: Explicit 3-cluster witness for Taha G₇-BCZ map (q=7)

## Goal

Make `BCZ7Witness.lean` compile (`lake build`, Mathlib **v4.28.0**), **0 sorry**,
`#print axioms three_cluster_q7` = `[propext, Classical.choice, Quot.sound]`.

This is the **first machine-verified 3-cluster in a cubic algebraic number field**: exhibit three
consecutive orbit points in `T⁷` (q=7, λ=2cos(π/7)) with observable `P < X(7) = 1/λ₇³`.
This formally proves `cluster_size_le_two` FAILS at q=7 (non-arithmetic Hecke group G₇),
complementing the proved arithmetic trio {3,4,6} (v8, v11, v12) and the q=5 witness (v13).

## Structure

The file is a **certificate-based witness proof** — no sorry stubs for math (unless otherwise noted).

Key definitions (do NOT change):
- `lam7 : ℝ := 2 * Real.cos (Real.pi / 7)` (λ₇)
- `X7 : ℝ := -5 * lam7^2 + 3*lam7 + 11` (= 1/λ₇³, cubic field identity)
- `a0,b0` = (20/61, 25/61); `a1,b1` = (25/61, −20/61+(25/61)·λ); `a2,b2` = (b1, (25/61)λ²−(20/61)λ−25/61)
- `inT7`, `inLastBranch7`, `Pobs7`, `bczMap7`
- `X7_eq_inv_lam7_cubed : X7 = 1/lam7^3`

**Main theorem** `three_cluster_q7`: conjunction of
1. domain membership: all 3 points in T⁷
2. last-branch membership: all 3 points satisfy a+λb > 1
3. map steps: `bczMap7 (a0,b0) = (a1,b1)` and `bczMap7 (a1,b1) = (a2,b2)` (both k=1)
4. observables: `Pobs7(aᵢ,bᵢ) < X7` for i=0,1,2

## Field: Q(λ₇)

- λ₇ satisfies **minimal polynomial** `L^3 - L^2 - 2L + 1 = 0`, proved from trig identity  
  `cos(3π/7) + cos(4π/7) = 0` factoring the quartic `(L+2)(L^3-L^2-2L+1)=0`.
- **Reduction**: `L^3 = L^2 + 2L - 1` (key lemma: `lam7_cubic'`).
- **Interval**: 1.8019 < λ₇ < 1.8020 (proved from cubic + mean-value argument via `nlinarith`).
- `X(7) = 1/λ₇³ = -5λ² + 3λ + 11` verified by: `(-5L²+3L+11)·L³ = 1` using L^3→L^2+2L-1 and L^4→3L^2+L-1.

## Exact witness certificates (sympy-verified, code/goal1_q7_witness_exact.py)

**λ₇ ≈ 1.8019, X(7) = 1/λ₇³ ≈ 0.17092**

| Point | a | b | k | P = a·b | X − P |
|-------|---|---|---|---------|-------|
| 0 | 20/61 | 25/61 | 1 | 500/3721 | 40431/3721 + 3λ − 5λ² |
| 1 | 25/61 | −20/61 + (25/61)λ | 1 | −500/3721 + (625/3721)λ | 41431/3721 + (10538/3721)λ − 5λ² |
| 2 | b1 | (25/61)λ²−(20/61)λ−25/61 | — | −375/3721·λ²+1025/3721·λ−125/3721 | 41056/3721+(10138/3721)λ−(18230/3721)λ² |

**k₁=1 floor certificate:**
- (1+20/61)/(λ·25/61) = 81/(25λ) ∈ [1,2) since λ ∈ (1.8019, 1.8020)
- Lower: 25λ < 81 (since λ < 3.24) ✓ ; Upper: 81 < 50λ (since λ > 1.62) ✓

**k₂=1 floor certificate:**
- (1+25/61)/(λ·b₁) = 86/(25λ²−20λ) ∈ [1,2)
- Lower: 25λ²−20λ ≤ 86 (at λ=1.802: ≈45.1 ≤ 86 ✓)
- Upper: 86 < 2(25λ²−20λ) = 50λ²−40λ (at λ=1.8019: ≈90.3 > 86 ✓)

**Margins positive** (for nlinarith via hcub + h_lo + h_hi + sq_nonneg):
- margin₀ = 40431/3721 + 3λ − 5λ² > 0 (at λ=1.802: ≈0.0356 > 0 ✓)
- margin₁ = 41431/3721 + (10538/3721)λ − 5λ² > 0 (at λ=1.802: ≈0.0017 > 0 ✓)
- margin₂ = 41056/3721 + (10138/3721)λ − (18230/3721)λ² > 0 (at λ=1.802: ≈0.0344 > 0 ✓)

## Key lemmas and proof status

| Lemma | Status | Notes |
|-------|--------|-------|
| `lam7_pos` | should compile | Uses `cos_pos_of_mem_Ioo` |
| `lam7_cubic` | should compile | Trig: cos(3π/7)+cos(4π/7)=0, triple/quadruple angle formulas, factoring |
| `lam7_cubic'` | trivial from cubic | |
| `lam7_gt_one` | should compile | Uses `cos_le_cos_of_nonneg_of_le_pi`, `cos_pi_div_four = √2/2` |
| `lam7_gt` | may need nlinarith help | Mean value via factor polynomial + `nlinarith` with `sq_nonneg` hints |
| `lam7_lt` | may need nlinarith help | Symmetric argument |
| `X7_eq_inv_lam7_cubed` | should compile | Ring identity via `lam7_cubic'` |
| `k1_eq_one`, `k2_eq_one` | should compile | `Int.floor_eq_iff`, `le_div_iff₀` |
| `P0_lt_X7`, `P1_lt_X7` | should compile | Linear in λ |
| `P2_lt_X7` | **needs nlinarith with cubic** | Degree 3 reduces via `lam7_cubic'`; margin₂ needs h_lo+h_hi+sq_nonneg |
| `three_cluster_q7` | should compile | Assembles the above |

## Most likely failures

1. **`lam7_cubic` trig steps**: `hcos3` (triple angle) and `hcos4` (quadruple angle) use `nlinarith` with `sin_sq_add_cos_sq`. May need `Real.sin_add`, `Real.cos_add` patterns. If nlinarith fails, try `ring_nf; nlinarith [...]`.

2. **`lam7_gt`/`lam7_lt`**: The `hfactor` nlinarith needs `lam7 > 1` hint. Use `lam7_gt_one` explicitly. If nlinarith times out, add `set_option maxHeartbeats 400000`.

3. **`P2_lt_X7`**: After unfolding, goal has lam7^3. Need `hcub := lam7_cubic'` to reduce; nlinarith with `[sq_nonneg lam7, hcub, h_lo, h_hi, mul_pos lam7_pos lam7_pos]`. If times out, extract the intermediate step: first compute `a2*b2` symbolically via `have hP2 : a2*b2 = ...` using `ring_nf` and `hcub`, then `nlinarith` on the reduced form.

4. **`map_step_01`/`map_step_12`**: Should compile with `ring`. If `a1 = b0` doesn't close with `norm_num`, try `rfl` or `simp [a1, b0]`.

## Constraints

- 0 sorry; standard axioms `[propext, Classical.choice, Quot.sound]` only.
- Do NOT use `aesop`, `grind`, `simp_all`, or `decide` for arithmetic goals.
- Allowed: `nlinarith`, `linarith`, `norm_num`, `ring`, `rw`, `simp only [named]`, `push_cast`, `positivity`, `Int.floor_eq_iff`, `Real.cos_add`, `Real.sin_sq_add_cos_sq`, `Real.cos_pi_sub`.
- Do NOT change theorem statement, witness coordinates, threshold X7.
- `set_option maxHeartbeats` up to 800000 for heavy calls.
- No `nlinarith` with degree > 4 products (expand manually if needed).

## Report

List all changes made, exact hint sets for hard nlinarith calls, paste `#print axioms three_cluster_q7` output.
