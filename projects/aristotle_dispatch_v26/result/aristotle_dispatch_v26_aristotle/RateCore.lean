import Mathlib

/-!
# RATE lemma — formalizable core (v26 dispatch)

Source: `research_notes/rh_goals_2026-08-14/lane_g/LAW_R2_RATE_LEMMA_DRAFT.md`
(the (RATE) lemma, DRAFT status). This file formalizes the P1–P6 chain the
draft marks "Aristotle: YES" or "Aristotle: MAYBE" (§5 "Proved in this
draft"), plus the finite depth-`k` instances of the structural gap M1
(word-level `λ → 2` map), left as a clearly-marked hypothesis for the
general/infinite case.

**Conventions (matching the draft §1 exactly).**

`S : z ↦ z + 1` and `Q = Q_λ = (0, -1/λ; λ, 0)`, `λ = λ_q = 2cos(π/q) ∈ [√2,
2)`, theta group at `λ = 2`. A double-coset representative is a reduced word

    w = Q S^{n_1} Q S^{n_2} … S^{n_{k-1}} Q,   k ≥ 1, n_i ∈ ℤ ∖ {0}

encoded here as a `List ℤ` of the exponents `n_1, …, n_{k-1}` (so `k =
w.length + 1`, matching the draft's "k = number of Q letters"). `c_w(λ)` is
the lower-left entry of the product matrix.

Nothing about the analytic assembly of §3 (the candidate lemma, `Δ_X`, `E_q`,
`E_θ`, `T_X`) is formalized here — only the algebraic/derivative core P1–P6
and the finite-depth M1 instances, per the dispatch task.

**Two statements of the original draft file are false as stated** (P4 without
a half-plane hypothesis on `s`, and the depth-1 instance of M1). They are
kept below, commented out, together with a proof that they fail and a
corrected version; see the comments at the relevant sections.
-/

open Polynomial

namespace RateCore

/-! ## 0. Setup: `Q_λ`, `S^n`, word matrices, `c_w` -/

/-- `Q_λ = (0, -1/λ; λ, 0)`. -/
noncomputable def Qmat (lam : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![0, -1 / lam; lam, 0]

/-- `S^n = (1, n; 0, 1)` for `n : ℤ`, computed directly (no group-power
machinery needed since this closed form is immediate by induction and matches
the draft's convention `S : z ↦ z + 1`). -/
def Spow (n : ℤ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![1, (n : ℝ); 0, 1]

/-- `E = diag(-1, 1)`, the matrix in P2. -/
def Emat : Matrix (Fin 2) (Fin 2) ℝ := !![-1, 0; 0, 1]

/-- Matrix of the word `Q S^{n_1} Q S^{n_2} ⋯ S^{n_{k-1}} Q` at parameter
`lam`, encoded by the exponent list `[n_1, …, n_{k-1}]`. `k = ns.length + 1`
Q-letters. -/
noncomputable def wordMatrix (lam : ℝ) : List ℤ → Matrix (Fin 2) (Fin 2) ℝ
  | [] => Qmat lam
  | n :: ns => Qmat lam * Spow n * wordMatrix lam ns

/-- `k_w`, the word depth (number of `Q` letters). -/
def depth (w : List ℤ) : ℕ := w.length + 1

/-- `c_w(λ)`, the lower-left entry of the word matrix. -/
noncomputable def c (lam : ℝ) (w : List ℤ) : ℝ := wordMatrix lam w 1 0

/-! ## 1. P1 — integer-Laurent structure (`§1 (P1)`)

Each entry of the product is a Laurent polynomial in `λ` with integer
coefficients; equivalently, `λ^{k_w}` times the entry is (the real
coefficients of) an integer polynomial evaluated at `λ`. Stated for the
`c_w` entry used throughout the draft. -/

/-- Degree bookkeeping for a product of two `2 × 2` polynomial matrices. -/
private lemma natDegree_matrix_mul_le {a b : ℕ}
    (M N : Matrix (Fin 2) (Fin 2) (Polynomial ℤ))
    (hM : ∀ i j, (M i j).natDegree ≤ a) (hN : ∀ i j, (N i j).natDegree ≤ b) :
    ∀ i j, ((M * N) i j).natDegree ≤ a + b := by
  intro i j
  rw [Matrix.mul_apply]
  exact natDegree_sum_le_of_forall_le _ _ fun k _ =>
    le_trans natDegree_mul_le (add_le_add (hM i k) (hN k j))

/-- **P1, matrix form.** `λ^{k_w}` times the word matrix is, entrywise, an
integer polynomial of degree at most `2 k_w` evaluated at `λ`. -/
theorem wordMatrix_intPoly (w : List ℤ) :
    ∃ P : Matrix (Fin 2) (Fin 2) (Polynomial ℤ),
      (∀ i j, (P i j).natDegree ≤ 2 * depth w) ∧
      ∀ lam : ℝ, lam ≠ 0 → ∀ i j,
        lam ^ depth w * wordMatrix lam w i j = aeval lam (P i j) := by
  induction w with
  | nil =>
      refine ⟨!![0, -1; X ^ 2, 0], ?_, ?_⟩
      · intro i j
        fin_cases i <;> fin_cases j <;> simp [depth]
      · intro lam hlam i j
        fin_cases i <;> fin_cases j <;>
          simp [Qmat, wordMatrix, depth] <;> field_simp
  | cons n ns ih =>
      obtain ⟨P, hdeg, hval⟩ := ih
      refine ⟨!![0, -1; X ^ 2, C n * X ^ 2] * P, ?_, ?_⟩
      · have hd : ∀ i j,
            ((!![0, -1; X ^ 2, C n * X ^ 2] :
              Matrix (Fin 2) (Fin 2) (Polynomial ℤ)) i j).natDegree ≤ 2 := by
          intro i j
          fin_cases i <;> fin_cases j <;> simp
          exact le_trans natDegree_mul_le (by simp)
        intro i j
        have hmul := natDegree_matrix_mul_le _ _ hd hdeg i j
        have hdd : depth (n :: ns) = depth ns + 1 := by simp [depth]
        omega
      · intro lam hlam i j
        have hA : ∀ i t : Fin 2, lam * ((Qmat lam * Spow n) i t)
            = aeval lam ((!![0, -1; X ^ 2, C n * X ^ 2] :
                Matrix (Fin 2) (Fin 2) (Polynomial ℤ)) i t) := by
          intro i t
          fin_cases i <;> fin_cases t <;>
            simp [Qmat, Spow, Matrix.mul_apply, Fin.sum_univ_two] <;> field_simp
        have hdd : depth (n :: ns) = depth ns + 1 := by simp [depth]
        rw [hdd]
        show lam ^ (depth ns + 1) *
          ((Qmat lam * Spow n) * wordMatrix lam ns) i j = _
        rw [Matrix.mul_apply, Matrix.mul_apply, Finset.mul_sum, map_sum]
        refine Finset.sum_congr rfl fun t _ => ?_
        have h1 := hA i t
        have h2 := hval lam hlam t j
        rw [map_mul, ← h1, ← h2]
        ring

theorem c_eq_scaled_int_poly (w : List ℤ) :
    ∃ p : Polynomial ℤ, p.natDegree ≤ 2 * depth w ∧
      ∀ lam : ℝ, lam ≠ 0 →
        c lam w * lam ^ depth w = aeval lam p := by
  obtain ⟨P, hdeg, hval⟩ := wordMatrix_intPoly w
  refine ⟨P 1 0, hdeg 1 0, fun lam hlam => ?_⟩
  rw [mul_comm]
  exact hval lam hlam 1 0

/-! ## 2. P2 — `dQ/dλ = (1/λ) E Q` (`§1 (P2)`) -/

/-- Each entry of `Q_λ` is differentiable in `λ` (away from `0`) with
derivative matrix `(1/λ) • (E * Q_λ)`, i.e. `dQ/dλ = (1/λ) E Q`. Stated
entrywise since `Matrix`-valued `HasDerivAt` is entrywise in this Mathlib. -/
theorem hasDerivAt_Qmat (lam : ℝ) (hlam : lam ≠ 0) (i j : Fin 2) :
    HasDerivAt (fun l => Qmat l i j) ((1 / lam) • (Emat * Qmat lam) i j) lam := by
  have hinv : HasDerivAt (fun l : ℝ => -1 / l) ((lam ^ 2)⁻¹) lam := by
    have h := (hasDerivAt_inv hlam).neg
    simpa [neg_div, div_eq_mul_inv] using h
  fin_cases i <;> fin_cases j
  · refine HasDerivAt.congr_deriv (hasDerivAt_const lam (0 : ℝ)) ?_
    simp [Emat, Qmat, Matrix.mul_apply, Fin.sum_univ_two]
  · refine HasDerivAt.congr_deriv hinv ?_
    simp only [Emat, Qmat, Matrix.mul_apply, Fin.sum_univ_two]
    norm_num
    field_simp
  · refine HasDerivAt.congr_deriv (hasDerivAt_id lam) ?_
    simp only [Emat, Qmat, Matrix.mul_apply, Fin.sum_univ_two]
    norm_num
    field_simp
  · refine HasDerivAt.congr_deriv (hasDerivAt_const lam (0 : ℝ)) ?_
    simp [Emat, Qmat, Matrix.mul_apply, Fin.sum_univ_two]

/-! ## 3. P3 — mean value bound (`§1 (P3)`)

`|c_w(λ_q) − c_w(2)| ≤ (2 − λ_q) · sup_{λ ∈ [λ_q,2]} |c_w'(λ)|`. Stated as
the generic (word-independent) mean value inequality it is an instance of:
for `f` differentiable on `[a, b]` with `|f'| ≤ M` there, `|f b − f a| ≤ M ·
(b − a)`. -/

theorem mvt_bound (f f' : ℝ → ℝ) (a b M : ℝ) (hab : a ≤ b)
    (hderiv : ∀ x ∈ Set.Icc a b, HasDerivAt f (f' x) x)
    (hbound : ∀ x ∈ Set.Icc a b, |f' x| ≤ M) :
    |f b - f a| ≤ M * (b - a) := by
  have h := Convex.norm_image_sub_le_of_norm_hasDerivWithin_le
    (f := f) (f' := f') (s := Set.Icc a b) (C := M)
    (fun x hx => (hderiv x hx).hasDerivWithinAt) hbound (convex_Icc a b)
    (Set.left_mem_Icc.2 hab) (Set.right_mem_Icc.2 hab)
  simpa [Real.norm_eq_abs, abs_of_nonneg (sub_nonneg.2 hab)] using h

/-! ## 4. P4 — mean value bound on `t ↦ t^{-2s}` (`§1 (P4)`)

For `x, y > 0`, `s = σ + it`: `|x^{-2s} − y^{-2s}| ≤ 2|s| · min(x,y)^{-2σ-1}
· |x − y|`.

**The statement as written in the draft is false**: the mean value bound
produces `sup_{t ∈ [min, max]} 2|s| t^{-2σ-1}`, which equals
`2|s| min(x,y)^{-2σ-1}` only when the exponent `-2σ-1` is nonpositive, i.e.
when `σ ≥ -1/2`. For `σ < -1/2` the supremum is attained at `max(x,y)`
instead, and the inequality genuinely fails; see
`cpow_neg_two_s_bound_false` (with `x = 1`, `y = 2`, `s = -1`: the left side
is `|1 - 4| = 3`, the right side is `2`). The original statement is kept
commented out below, and the corrected version
`cpow_neg_two_s_bound'`, carrying the (harmless, since the draft works in a
right half-plane) hypothesis `-1/2 ≤ σ`, is proved. -/

/- FALSE AS STATED — see `cpow_neg_two_s_bound_false` below.
theorem cpow_neg_two_s_bound (x y : ℝ) (s : ℂ) (hx : 0 < x) (hy : 0 < y) :
    ‖(x : ℂ) ^ (-2 * s) - (y : ℂ) ^ (-2 * s)‖ ≤
      2 * ‖s‖ * (min x y) ^ (-2 * s.re - 1) * |x - y| := by
  sorry
-/

/-- The draft's P4, stated without any hypothesis on `Re s`, is false. -/
theorem cpow_neg_two_s_bound_false :
    ¬ ∀ (x y : ℝ) (s : ℂ), 0 < x → 0 < y →
      ‖(x : ℂ) ^ (-2 * s) - (y : ℂ) ^ (-2 * s)‖ ≤
        2 * ‖s‖ * (min x y) ^ (-2 * s.re - 1) * |x - y| := by
  intro h
  have hcex := h 1 2 (-1) one_pos two_pos
  norm_num at hcex

/-- One-sided (`x ≤ y`) form of the corrected P4. -/
private lemma cpow_aux (x y : ℝ) (s : ℂ) (hx : 0 < x) (hxy : x ≤ y)
    (hs : -1 / 2 ≤ s.re) :
    ‖(x : ℂ) ^ (-2 * s) - (y : ℂ) ^ (-2 * s)‖ ≤
      2 * ‖s‖ * x ^ (-2 * s.re - 1) * (y - x) := by
  rcases eq_or_ne s 0 with rfl | hs0
  · simp
  set C : ℝ := 2 * ‖s‖ * x ^ (-2 * s.re - 1) with hC
  have hderiv : ∀ t ∈ Set.Icc x y,
      HasDerivWithinAt (fun t : ℝ => (t : ℂ) ^ (-2 * s))
        ((-2 * s) * (t : ℂ) ^ (-2 * s - 1)) (Set.Icc x y) t := by
    intro t ht
    have ht0 : t ≠ 0 := ne_of_gt (lt_of_lt_of_le hx ht.1)
    exact (hasDerivAt_ofReal_cpow_const ht0 (by simpa using hs0)).hasDerivWithinAt
  have hbound : ∀ t ∈ Set.Icc x y, ‖(-2 * s) * (t : ℂ) ^ (-2 * s - 1)‖ ≤ C := by
    intro t ht
    have ht0 : 0 < t := lt_of_lt_of_le hx ht.1
    rw [norm_mul, Complex.norm_cpow_eq_rpow_re_of_pos ht0]
    have h1 : ‖(-2 : ℂ) * s‖ = 2 * ‖s‖ := by rw [norm_mul]; norm_num
    have h2 : (-2 * s - 1).re = -2 * s.re - 1 := by simp
    rw [h1, h2, hC]
    have h3 : t ^ (-2 * s.re - 1) ≤ x ^ (-2 * s.re - 1) :=
      Real.rpow_le_rpow_of_nonpos hx ht.1 (by linarith)
    exact mul_le_mul_of_nonneg_left h3 (by positivity)
  have h := Convex.norm_image_sub_le_of_norm_hasDerivWithin_le hderiv hbound
    (convex_Icc x y) (Set.left_mem_Icc.2 hxy) (Set.right_mem_Icc.2 hxy)
  rw [← norm_neg, neg_sub]
  calc ‖(y : ℂ) ^ (-2 * s) - (x : ℂ) ^ (-2 * s)‖ ≤ C * ‖y - x‖ := h
    _ = C * (y - x) := by rw [Real.norm_eq_abs, abs_of_nonneg (by linarith)]

/-- **P4, corrected.** For `x, y > 0` and `s = σ + it` with `σ ≥ -1/2`,
`|x^{-2s} − y^{-2s}| ≤ 2|s| · min(x,y)^{-2σ-1} · |x − y|`. The hypothesis
`-1/2 ≤ σ` is necessary (`cpow_neg_two_s_bound_false`) and is satisfied
throughout the draft, which works in a right half-plane. -/
theorem cpow_neg_two_s_bound' (x y : ℝ) (s : ℂ) (hx : 0 < x) (hy : 0 < y)
    (hs : -1 / 2 ≤ s.re) :
    ‖(x : ℂ) ^ (-2 * s) - (y : ℂ) ^ (-2 * s)‖ ≤
      2 * ‖s‖ * (min x y) ^ (-2 * s.re - 1) * |x - y| := by
  rcases le_total x y with h | h
  · rw [min_eq_left h, abs_of_nonpos (by linarith)]
    simpa using cpow_aux x y s hx h hs
  · rw [min_eq_right h, abs_of_nonneg (by linarith)]
    rw [← norm_neg, neg_sub]
    simpa using cpow_aux y x s hy h hs

/-! ## 5. P5 — cosine inequality (`§1 (P5)`)

`2 − λ_q = 2(1 − cos(π/q)) ≤ π²/q²`. -/

/-- P5. The hypothesis `1 ≤ q` is kept because the draft states it, but it
turns out to be unnecessary: the bound follows from `1 - cos x ≤ x²/2` for
every real `x`, and at `q = 0` both sides are `0`. -/
theorem two_sub_lam_le (q : ℕ) (hq : 1 ≤ q) :
    2 * (1 - Real.cos (Real.pi / q)) ≤ Real.pi ^ 2 / (q : ℝ) ^ 2 := by
  have h := Real.one_sub_sq_div_two_le_cos (x := Real.pi / q)
  have hsq : (Real.pi / q) ^ 2 = Real.pi ^ 2 / (q : ℝ) ^ 2 := div_pow _ _ 2
  nlinarith [h]

/-! ## 6. P6 — the Chebyshev subfamily, exact (`§1 (P6)`)

`w = (QS)^{m-1}Q`, i.e. all `n_i = 1`: `c_w(λ) = λ · U_{m-1}(λ/2)`, with
`U` the Chebyshev polynomial of the second kind (Mathlib
`Polynomial.Chebyshev.U`). Encoded here as the exponent list
`List.replicate (m - 1) (1 : ℤ)`. -/

/-- The Chebyshev-subfamily word of depth `m` (`m ≥ 1`): all inner exponents
equal `1`. -/
def chebyshevWord (m : ℕ) : List ℤ := List.replicate (m - 1) (1 : ℤ)

/-- At `λ = 0` the matrix `Q_0` degenerates to `0` (Lean's `-1/0 = 0`), so
every word matrix vanishes. -/
private lemma wordMatrix_zero (w : List ℤ) : wordMatrix 0 w = 0 := by
  have hQ : Qmat 0 = 0 := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [Qmat]
  induction w with
  | nil => simpa [wordMatrix] using hQ
  | cons n ns ih => simp [wordMatrix, hQ]

private lemma c_zero (w : List ℤ) : c 0 w = 0 := by
  simp [c, wordMatrix_zero]

open Polynomial.Chebyshev in
/-- The `U`-recurrence, evaluated at `λ/2`. -/
private lemma cheb_rec (lam : ℝ) (n : ℤ) :
    aeval (lam / 2) (U ℝ (n + 2)) =
      lam * aeval (lam / 2) (U ℝ (n + 1)) - aeval (lam / 2) (U ℝ n) := by
  rw [U_add_two]
  simp only [map_sub, map_mul, map_ofNat, aeval_X]
  ring

open Polynomial.Chebyshev in
/-- The left column of the Chebyshev-word matrix, by induction on the word
length: `(0,0)`-entry `= -U_{m-1}(λ/2)` and `(1,0)`-entry `= λ U_m(λ/2)`. -/
private lemma cheb_pair (lam : ℝ) (hlam : lam ≠ 0) (m : ℕ) :
    wordMatrix lam (List.replicate m (1 : ℤ)) 0 0
        = -aeval (lam / 2) (U ℝ ((m : ℤ) - 1)) ∧
      wordMatrix lam (List.replicate m (1 : ℤ)) 1 0
        = lam * aeval (lam / 2) (U ℝ (m : ℤ)) := by
  induction m with
  | zero => constructor <;> simp [wordMatrix, Qmat, U_neg_one]
  | succ m ih =>
      obtain ⟨h0, h1⟩ := ih
      rw [List.replicate_succ]
      constructor
      · show (Qmat lam * Spow 1 * wordMatrix lam (List.replicate m 1)) 0 0 = _
        rw [Matrix.mul_apply]
        simp only [Fin.sum_univ_two]
        rw [h0, h1]
        simp [Qmat, Spow, Matrix.mul_apply, Fin.sum_univ_two]
        field_simp
      · show (Qmat lam * Spow 1 * wordMatrix lam (List.replicate m 1)) 1 0 = _
        rw [Matrix.mul_apply]
        simp only [Fin.sum_univ_two]
        rw [h0, h1]
        have hr : (((m + 1 : ℕ) : ℤ)) = ((m : ℤ) - 1) + 2 := by push_cast; ring
        rw [hr, cheb_rec]
        have hr2 : ((m : ℤ) - 1 + 1) = (m : ℤ) := by ring
        rw [hr2]
        simp [Qmat, Spow, Matrix.mul_apply, Fin.sum_univ_two]
        ring

theorem c_chebyshevWord (m : ℕ) (hm : 1 ≤ m) (lam : ℝ) :
    c lam (chebyshevWord m) =
      lam * aeval (lam / 2) (Polynomial.Chebyshev.U ℝ ((m : ℤ) - 1)) := by
  rcases eq_or_ne lam 0 with rfl | hlam
  · simp [c_zero]
  · have hcast : (((m - 1 : ℕ)) : ℤ) = (m : ℤ) - 1 := by omega
    have h := (cheb_pair lam hlam (m - 1)).2
    rw [hcast] at h
    simpa [c, chebyshevWord] using h

/-- At `λ = 2`: `c_w(2) = 2m` for the Chebyshev word of depth `m`, per the
draft's "At λ = 2: c = 2m". -/
theorem c_chebyshevWord_two (m : ℕ) (hm : 1 ≤ m) :
    c 2 (chebyshevWord m) = 2 * (m : ℝ) := by
  rw [c_chebyshevWord m hm]
  have h : (aeval ((2 : ℝ) / 2)) (Polynomial.Chebyshev.U ℝ ((m : ℤ) - 1))
      = (((m : ℤ) - 1 : ℤ) : ℝ) + 1 := by norm_num
  rw [h]
  push_cast
  ring

/-! ## 7. M1 — the word-level `λ → 2` structural map (`§5`, gap M1)

**General statement: NOT proved here (draft: "Aristotle: NOT as stated").**
Recorded as an explicit hypothesis, matching the draft's characterization
("a bijection {matched q-cosets} → {θ-cosets with c ≤ c*(q)}, complement
confined to the near-relation region"). The finite depth-bounded restriction
(all words of depth ≤ K) is the part the draft tags "YES per (q, K)"; two
smallest such instances (K = 1, 2) are stated and left as lemmas Aristotle is
asked to discharge by finite computation, as a down payment on M1 rather than
a proof of the general claim. -/

/-- **M1, general form (HYPOTHESIS, not proved here).** The word-level
`λ → 2` evaluation map, restricted to words of depth `≤ K` at level `q`
(`lam = 2 * Real.cos (Real.pi / q)`), is injective on the words it does not
send to `0` — the "matched" half of M1's bijection claim. This is recorded
as a standing hypothesis for the general case; see the draft §5 M1 for why
the unrestricted (`K → ∞`) statement needs a normal-form/geodesic argument
not attempted here. -/
axiom wordLimitMap_injective_on_matched (q K : ℕ) (hq : 3 ≤ q) :
    Set.InjOn (fun w : List ℤ => c 2 w)
      {w : List ℤ | depth w ≤ K ∧ c (2 * Real.cos (Real.pi / q)) w ≠ 0}

/-! **The depth-1 instance as stated in the draft file is false.** With the
draft's own conventions — `Q_λ = (0, -1/λ; λ, 0)` and `c_w` the *lower-left*
entry — the depth-1 word `w = []` (the single letter `Q`) has
`c_{[]}(λ) = λ`, not `-1/λ`; the value `-1/λ` is the *upper-right* entry.
The original statement is kept commented out below, its failure is recorded
in `wordLimitMap_matched_depth_one_false`, and the corrected identity is
`wordLimitMap_matched_depth_one'`. (The corrected value is the one consistent
with P6: `c_{[]}(λ) = λ = λ · U_0(λ/2)`.) -/

/- FALSE AS STATED — see `wordLimitMap_matched_depth_one_false` below.
theorem wordLimitMap_matched_depth_one (lam : ℝ) (hlam : lam ≠ 0) :
    c lam ([] : List ℤ) = -1 / lam := by
  sorry
-/

/-- The draft's depth-1 identity `c_{[]}(λ) = -1/λ` is false (take `λ = 1`,
where `c_{[]}(1) = 1 ≠ -1`). -/
theorem wordLimitMap_matched_depth_one_false :
    ¬ ∀ lam : ℝ, lam ≠ 0 → c lam ([] : List ℤ) = -1 / lam := by
  intro h
  have h1 := h 1 one_ne_zero
  simp [c, wordMatrix, Qmat] at h1
  exact absurd h1 (by norm_num)

/-- **M1, depth-1 instance (finite), corrected.** At depth `1` the only word
is the empty exponent list (`w = []`, i.e. the single letter `Q`); its
lower-left entry is `c_{[]}(λ) = λ`, so the depth-`1` matching is the single
pair `(λ_q, 2)` — injective (and onto the depth-1 theta value) trivially. -/
theorem wordLimitMap_matched_depth_one' (lam : ℝ) : c lam ([] : List ℤ) = lam := by
  simp [c, wordMatrix, Qmat]

/-- **M1, depth-2 instance (finite, Aristotle-ready).** At depth `2` the
words are `[n]` for `n ∈ ℤ ∖ {0}` (i.e. `Q S^n Q`); the explicit matrix
product gives the closed form `c_{[n]}(λ) = n · λ²`, a polynomial identity
(no `λ⁻¹` survives the two-`Q` cancellation) — the finite (`q`-independent)
instance of the matching map at `K = 2`. In particular `c_{[n]}(λ) → 0` only
at `λ = 0`, so the depth-`2` word-limit map `λ ↦ c_{[n]}(λ)` is injective on
`n` for fixed `λ ≠ 0`, matching M1's claim at this depth. The hypothesis
`λ ≠ 0` is kept because the draft states it, but it turns out to be
unnecessary: at `λ = 0` both sides vanish. -/
theorem c_depth_two (lam : ℝ) (hlam : lam ≠ 0) (n : ℤ) :
    c lam [n] = (n : ℝ) * lam ^ 2 := by
  simp [c, wordMatrix, Qmat, Spow, Matrix.mul_apply, Fin.sum_univ_two]
  ring

end RateCore
