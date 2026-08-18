import Mathlib

/-!
# RATE lemma — M1 refinement + N4 counting (v27 dispatch)

Source: `research_notes/rh_goals_2026-08-14/lane_g/LAW_R2_RATE_LEMMA_DRAFT.md`
(the (RATE) lemma, DRAFT status) and the v26 harvest `RateCore.lean`
(P1–P6 machine-verified 2026-08-17).

This file targets the two remaining formalizable pieces:

1. **M1 word-level refutation + repair scaffolding.** v26 recorded the general
   M1 claim as the axiom `wordLimitMap_injective_on_matched` (injectivity of
   `w ↦ c 2 w` on matched words of bounded depth). Numeric evidence
   (2026-08-17, three λ values) says this WORD-level statement is FALSE
   already at depth 3: the closed form is `c_λ([n,m]) = λ(n·m·λ² − 1)`, so
   `[1,2]` and `[2,1]` collide at every λ. The theorems below ask for:
   (a) the depth-3 closed form; (b) the machine-certified disproof of the
   axiom's K = 3 instance; (c) the repaired injectivity statement on
   *unordered* exponent data at depth 3 (injectivity of `(n,m) ↦ λ(nmλ²−1)`
   in the product `n·m` — the invariant that survives).
2. **N4 (φ(2n) multiplicity), now with the printed source.** Hejhal LNM 1001
   Vol. 2, Ch. 11 §3 Lemma 3.1 (received 2026-08-17): theta-group double
   cosets are indexed by pairs `⟨c d⟩` with `c > 0`, `0 ≤ d < 2c`,
   `c + d ≡ 1 mod 2`, `gcd(c,d) = 1`. The count of such `d` for fixed `c`
   is `φ(2c)` — the multiplicity constant the draft's N4 uses numerically.
3. **λ = 2 evenness.** At the theta limit `λ = 2`, every `c`-value is an even
   integer (`c 2 w = 2m`, `m : ℤ`) — the integrality backbone for matching
   word classes to Lemma 3.1's integer pairs. (Hint: conjugating by
   `diag(1,2)` makes the λ=2 word matrices integral; or induct with the
   auxiliary claim that `wordMatrix 2 w` has integer lower-left and diagonal
   entries and half-integer upper-right entry, i.e. `2 · wordMatrix 2 w`
   is integral.)

Conventions are IDENTICAL to v26 `RateCore.lean` (same `Qmat`, `Spow`,
`wordMatrix`, `c`, `depth`; `wordMatrix [] = Qmat`, so depth 1 ↦ the single
letter `Q` and `c 2 [] = 2`).

As in v26: if any statement is FALSE as stated, please prove its negation
and state + prove the corrected version rather than forcing the original.
-/

namespace RateCoreII

/-- `Q_λ = (0, -1/λ; λ, 0)`. -/
noncomputable def Qmat (lam : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![0, -1 / lam; lam, 0]

/-- `S^n = (1, n; 0, 1)` for `n : ℤ`. -/
def Spow (n : ℤ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![1, (n : ℝ); 0, 1]

/-- Word matrix of `Q S^{n_1} Q ⋯ S^{n_{k-1}} Q`, exponent list
`[n_1, …, n_{k-1}]`. -/
noncomputable def wordMatrix (lam : ℝ) : List ℤ → Matrix (Fin 2) (Fin 2) ℝ
  | [] => Qmat lam
  | n :: ns => Qmat lam * Spow n * wordMatrix lam ns

/-- Word depth (number of `Q` letters). -/
def depth (w : List ℤ) : ℕ := w.length + 1

/-- `c_w(λ)`, the lower-left entry. -/
noncomputable def c (lam : ℝ) (w : List ℤ) : ℝ := wordMatrix lam w 1 0

/-! ## 1. Depth-3 closed form -/

/-- Closed form at depth 3: `c_λ([n,m]) = λ (n m λ² − 1)`.
(Numerically verified at λ = 2cos(π/7), λ = 2, several (n,m).) -/
theorem c_depth_three (lam : ℝ) (hlam : lam ≠ 0) (n m : ℤ) :
    c lam [n, m] = lam * ((n : ℝ) * (m : ℝ) * lam ^ 2 - 1) := by
  sorry

/-! ## 2. M1 word-level injectivity REFUTATION (K = 3)

v26's axiom `wordLimitMap_injective_on_matched` asserts, for every `q ≥ 3`
and `K`, that `w ↦ c 2 w` is injective on
`{w | depth w ≤ K ∧ c (2cos(π/q)) w ≠ 0}`. The depth-3 closed form makes
`[1,2]` and `[2,1]` a collision (both matched: `c_λ = λ(2λ² − 1) ≠ 0` for
`λ` in the Hecke range `√2 < λ ≤ 2`; note the formula VANISHES at
`λ = 1/√2`, so the nonvanishing is range-dependent, not universal in `λ`),
so the `K = 3` instance is false. Certify this.

[CORRECTION 2026-08-18 audit-17] This comment previously asserted
`c_λ ≠ 0` "for `λ > 0`", which is false at `λ = 1/√2`. Comment only:
no theorem statement in this file is changed, and every `λ` actually used
(`2cos(π/q)`, `q ≥ 3`, and `λ = 2`) lies in the safe Hecke range. -/

/-- **Disproof of the v26 axiom's `K = 3` instance** (stated here as the
negation of the corresponding `Set.InjOn`, for `q = 7` as a concrete
witness level; any `q ≥ 3` works). -/
theorem wordLimitMap_not_injective_depth_three :
    ¬ Set.InjOn (fun w : List ℤ => c 2 w)
      {w : List ℤ | depth w ≤ 3 ∧ c (2 * Real.cos (Real.pi / 7)) w ≠ 0} := by
  sorry

/-- **Repaired depth-3 injectivity**: at depth exactly 3 the surviving
invariant is the product `n·m`; the λ→2 map is injective in it. -/
theorem c_depth_three_injective_in_product (n m n' m' : ℤ)
    (h : c 2 [n, m] = c 2 [n', m']) : n * m = n' * m' := by
  sorry

/-! ## 3. λ = 2 evenness (integrality backbone) -/

/-- `2 · wordMatrix 2 w` has integer entries. -/
theorem two_smul_wordMatrix_two_integral (w : List ℤ) :
    ∃ M : Matrix (Fin 2) (Fin 2) ℤ,
      (2 : ℝ) • wordMatrix 2 w = M.map (Int.cast : ℤ → ℝ) := by
  sorry

/-- At the theta limit, every `c`-value is an even integer. -/
theorem c_two_even (w : List ℤ) : ∃ m : ℤ, c 2 w = 2 * (m : ℝ) := by
  sorry

/-! ## 4. N4 — theta-coset multiplicity is `φ(2c)`

Hejhal Vol. 2, Ch. 11 §3, Lemma 3.1: coset representatives for fixed `c` are
the `d` with `0 ≤ d < 2c`, `gcd(c,d) = 1`, `c + d` odd. Their number is
`φ(2c)`. (Sanity: c=1 → {0}, φ(2)=1; c=2 → {1,3}, φ(4)=2; c=3 → {2,4},
φ(6)=2.) -/

theorem theta_coset_count (cc : ℕ) (hc : 0 < cc) :
    ((Finset.range (2 * cc)).filter
        (fun d => Nat.gcd cc d = 1 ∧ (cc + d) % 2 = 1)).card
      = Nat.totient (2 * cc) := by
  sorry

end RateCoreII
