import Mathlib

/-!
# RATE lemma — sharp no-wrap law + Route-B algebra (v29 dispatch)

Sources:

* `research_notes/rh_goals_2026-08-14/lane_g/M2_LOCALIZATION_THEOREM_SOL.md`
  §0 and §3 (sharp finite no-wrap law and Chebyshev equality cases).
* `research_notes/rh_goals_2026-08-14/lane_g/M1_LOCALIZATION_TRIPLE_REFEREE.md`
  §2.1 (the theorem is TRUE at paper level, but the written induction omitted
  one magnitude-ordering line; the all-`-1` equality case also needs an
  alternating sign before absolute values are taken).
* `research_notes/rh_goals_2026-08-14/lane_g/M1_ROUTE_B_REPAIR_SOL.md`
  §§1 and 3 (Tietze-letter matrix identities and four-sign boundary
  cancellation; paper-level CLOSED/PROVED, Lean formalization OPEN here).
* The harvested v26 `RateCore.lean`, whose `c_chebyshevWord` theorem was
  independently rebuilt sorry-free.  Its theorem signature is copied here so
  the v29 file remains a standalone `import Mathlib` dispatch.

Conventions in §0 are copied verbatim from v27 `RateCoreII.lean`: the exponent
list `[n_1, ..., n_{k-1}]` encodes
`Q S^{n_1} Q ... S^{n_{k-1}} Q`, `wordMatrix [] = Qmat`, and `depth` is the
number of `Q` letters.  In particular, `c lam [] = lam`; `c` is the lower-left
entry `(1, 0)`.

Only the finite no-wrap theorem is dispatched.  The global localization laws
`(LOC_0)`, `(LOC)`, `(LOC_mu)`, the RATE-strength `O(N^{1-2*sigma})` estimate,
and unrestricted raw-depth growth are not statements in this file: the source
marks the localization laws CONJECTURAL and the unrestricted/global targets
FALSE.

**FALSE-statement escape hatch (same rule as v27/v28).** If any target is FALSE
as stated, do not force its `sorry`.  Retain the original statement only inside
a `FALSE AS STATED` comment, prove a named `<target>_false` negation with an
exact witness, and then state and prove the weakest corrected `<target>'`
theorem.  Report the downstream status change.

**Status of this dispatch.** Every target below is TRUE as stated and is proved
here; no `FALSE AS STATED` escape hatch was needed.
-/

open Polynomial

namespace RateCoreIV

/-! ## 0. Setup: v26/v27 word conventions, verbatim -/

/-- `Q_lam = (0, -1/lam; lam, 0)`. -/
noncomputable def Qmat (lam : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![0, -1 / lam; lam, 0]

/-- `S^n = (1, n; 0, 1)` for `n : ℤ`. -/
def Spow (n : ℤ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![1, (n : ℝ); 0, 1]

/-- Word matrix of `Q S^{n_1} Q ... S^{n_{k-1}} Q`, exponent list
`[n_1, ..., n_{k-1}]`. -/
noncomputable def wordMatrix (lam : ℝ) : List ℤ → Matrix (Fin 2) (Fin 2) ℝ
  | [] => Qmat lam
  | n :: ns => Qmat lam * Spow n * wordMatrix lam ns

/-- Word depth (number of `Q` letters). -/
def depth (w : List ℤ) : ℕ := w.length + 1

/-- `c_w(lam)`, the lower-left entry. -/
noncomputable def c (lam : ℝ) (w : List ℤ) : ℝ := wordMatrix lam w 1 0

/-- `lambda_N = 2 cos(pi/N)`. -/
noncomputable def lamN (N : ℕ) : ℝ :=
  2 * Real.cos (Real.pi / (N : ℝ))

/-- Raw syntactic reduction in the v26/v27 `List ℤ` convention: every interior
`S`-exponent is nonzero.  This is raw `Q,S` syntax, not free-product depth or
minimal double-coset depth. -/
def SyntacticallyReduced (w : List ℤ) : Prop :=
  ∀ n ∈ w, n ≠ 0

/-! ## 1. Continuant bridge and the referee-required ordering lemma -/

/-- Negative continuant for the exponent list.  It has initial values `1` and
`lam*n` and recurrence `K(n :: m :: ns) = lam*n*K(m :: ns) - K(ns)`. -/
noncomputable def continuant (lam : ℝ) : List ℤ → ℝ
  | [] => 1
  | [n] => lam * (n : ℝ)
  | n :: m :: ns =>
      lam * (n : ℝ) * continuant lam (m :: ns) - continuant lam ns

/-! ### Matrix-entry recursions -/

lemma Qmat_zero : Qmat 0 = 0 := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Qmat]

lemma wordMatrix_zero (w : List ℤ) : wordMatrix (0 : ℝ) w = 0 := by
  induction w with
  | nil => simpa [wordMatrix] using Qmat_zero
  | cons n ns _ => simp [wordMatrix, Qmat_zero]

lemma wordMatrix_cons_lower (lam : ℝ) (n : ℤ) (ns : List ℤ) :
    wordMatrix lam (n :: ns) 1 0 =
      lam * wordMatrix lam ns 0 0 + lam * (n : ℝ) * wordMatrix lam ns 1 0 := by
  simp [wordMatrix, Qmat, Spow, Matrix.mul_apply, Fin.sum_univ_succ]

lemma wordMatrix_cons_upper (lam : ℝ) (n : ℤ) (ns : List ℤ) :
    wordMatrix lam (n :: ns) 0 0 = -(wordMatrix lam ns 1 0) / lam := by
  simp [wordMatrix, Qmat, Spow, Matrix.mul_apply, Fin.sum_univ_succ]
  ring

lemma c_nil (lam : ℝ) : c lam [] = lam := by
  simp [c, wordMatrix, Qmat]

lemma c_singleton (lam : ℝ) (n : ℤ) : c lam [n] = lam * (lam * (n : ℝ)) := by
  rw [c, wordMatrix_cons_lower]
  simp [wordMatrix, Qmat]
  ring

/-- The lower-left entry is `lam` times the negative continuant.

Source/status: `M2_LOCALIZATION_THEOREM_SOL.md:484-501` and
`M1_LOCALIZATION_TRIPLE_REFEREE.md:229-242`; REFEREE-CONFIRMED algebraic
identity, Lean target OPEN in this dispatch. -/
theorem c_eq_lam_mul_continuant (lam : ℝ) (w : List ℤ) :
    c lam w = lam * continuant lam w := by
  rcases eq_or_ne lam 0 with rfl | hlam
  · simp [c, wordMatrix_zero]
  · induction w using continuant.induct with
    | case1 => simp [c_nil, continuant]
    | case2 n => simp [c_singleton, continuant]
    | case3 n m ns ih1 ih2 =>
        have hup : wordMatrix lam (m :: ns) 0 0 = -continuant lam ns := by
          rw [wordMatrix_cons_upper]
          have : wordMatrix lam ns 1 0 = lam * continuant lam ns := ih2
          rw [this]
          field_simp
        have hlow : wordMatrix lam (m :: ns) 1 0 = lam * continuant lam (m :: ns) := ih1
        show wordMatrix lam (n :: m :: ns) 1 0 = _
        rw [wordMatrix_cons_lower, hup, hlow]
        simp [continuant]
        ring

/-- The magnitude ordering omitted from the written no-wrap induction:
`lam*|n| >= lam > 1/p >= 1/|r|`.

The hypothesis `0 < lam - 1/p` is the already-established positivity of the
next Chebyshev ratio; `p <= |r|` is the induction hypothesis.  This lemma must
be proved and used before the subtract-branch reverse-triangle estimate.

Source/status: `M1_LOCALIZATION_TRIPLE_REFEREE.md:249-265` and the correction
at `M2_LOCALIZATION_THEOREM_SOL.md:556-568`; REQUIRED GAP-REPAIR LINE,
referee-confirmed, Lean target OPEN. -/
theorem subtract_branch_magnitude_ordering
    (lam p r : ℝ) (n : ℤ)
    (hlam : 0 < lam) (hn : n ≠ 0) (hp : 0 < p)
    (hdom : p ≤ |r|) (hnext : 0 < lam - 1 / p) :
    lam * |(n : ℝ)| ≥ lam ∧ lam > 1 / p ∧ 1 / p ≥ 1 / |r| := by
  refine ⟨?_, by linarith, ?_⟩
  · have h1 : (1 : ℝ) ≤ |(n : ℝ)| := by
      have h : (1 : ℤ) ≤ |n| := Int.one_le_abs (by omega)
      have h' : ((1 : ℤ) : ℝ) ≤ ((|n| : ℤ) : ℝ) := by exact_mod_cast h
      rwa [Int.cast_abs, Int.cast_one] at h'
    nlinarith
  · exact one_div_le_one_div_of_le hp hdom

/-- Algebraic subtract branch after the missing ordering has been established.
Its proof should invoke `subtract_branch_magnitude_ordering`, then the reverse
triangle inequality; it must not silently assume which magnitude is larger.

Source/status: `M2_LOCALIZATION_THEOREM_SOL.md:548-568` and
`M1_LOCALIZATION_TRIPLE_REFEREE.md:249-265`; REFEREE-CONFIRMED repair,
Lean target OPEN. -/
theorem subtract_branch_lower_bound
    (lam p r : ℝ) (n : ℤ)
    (hlam : 0 < lam) (hn : n ≠ 0) (hp : 0 < p)
    (hdom : p ≤ |r|) (hnext : 0 < lam - 1 / p) :
    lam - 1 / p ≤ |lam * (n : ℝ) - 1 / r| := by
  obtain ⟨h1, h2, h3⟩ :=
    subtract_branch_magnitude_ordering lam p r n hlam hn hp hdom hnext
  have habs : |lam * (n : ℝ)| = lam * |(n : ℝ)| := by
    rw [abs_mul, abs_of_pos hlam]
  have hrev : |lam * (n : ℝ)| - |1 / r| ≤ |lam * (n : ℝ) - 1 / r| :=
    abs_sub_abs_le_abs_sub _ _
  have hr : |1 / r| = 1 / |r| := by rw [abs_div, abs_one]
  rw [habs] at hrev
  rw [hr] at hrev
  linarith

/-! ## 2. Sharp finite no-wrap law -/

/-- `sinRatio N j = sin(j*pi/N) / sin(pi/N)`, i.e. the Chebyshev value
`U_{j-1}(lam_N/2)`. -/
noncomputable def sinRatio (N j : ℕ) : ℝ :=
  Real.sin ((j : ℝ) * Real.pi / (N : ℝ)) / Real.sin (Real.pi / (N : ℝ))

lemma sin_pi_div_N_pos {N : ℕ} (hN : 3 ≤ N) : 0 < Real.sin (Real.pi / (N : ℝ)) := by
  have hN' : (3 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have hpi := Real.pi_pos
  refine Real.sin_pos_of_pos_of_lt_pi (by positivity) ?_
  rw [div_lt_iff₀ (by linarith)]
  nlinarith

lemma sinRatio_zero (N : ℕ) : sinRatio N 0 = 0 := by
  simp [sinRatio]

lemma sinRatio_one {N : ℕ} (hN : 3 ≤ N) : sinRatio N 1 = 1 := by
  have h := (sin_pi_div_N_pos hN).ne'
  simp [sinRatio, div_self h]

lemma sinRatio_rec (N j : ℕ) :
    sinRatio N (j + 2) = lamN N * sinRatio N (j + 1) - sinRatio N j := by
  have e1 : ((j : ℝ) + 2) * Real.pi / (N : ℝ)
      = (((j : ℝ) + 1) * Real.pi / (N : ℝ)) + Real.pi / (N : ℝ) := by
    field_simp; ring
  have e2 : (j : ℝ) * Real.pi / (N : ℝ)
      = (((j : ℝ) + 1) * Real.pi / (N : ℝ)) - Real.pi / (N : ℝ) := by
    field_simp; ring
  have key : Real.sin (((j : ℝ) + 2) * Real.pi / (N : ℝ))
      = 2 * Real.cos (Real.pi / (N : ℝ)) *
          Real.sin (((j : ℝ) + 1) * Real.pi / (N : ℝ))
        - Real.sin ((j : ℝ) * Real.pi / (N : ℝ)) := by
    rw [e1, e2, Real.sin_add, Real.sin_sub]; ring
  unfold sinRatio lamN
  push_cast
  rw [key]
  ring

lemma sinRatio_two (N : ℕ) (hN : 3 ≤ N) : sinRatio N 2 = lamN N := by
  have := sinRatio_rec N 0
  rw [sinRatio_zero, sinRatio_one hN] at this
  simpa using this

lemma sinRatio_pos {N j : ℕ} (hN : 3 ≤ N) (hj : 1 ≤ j) (hjN : j ≤ N - 1) :
    0 < sinRatio N j := by
  have hs := sin_pi_div_N_pos hN
  have hN' : (0 : ℝ) < (N : ℝ) := by positivity
  have hjN' : (j : ℝ) < (N : ℝ) := by
    have : j < N := by omega
    exact_mod_cast this
  have hj' : (1 : ℝ) ≤ (j : ℝ) := by exact_mod_cast hj
  have hpi := Real.pi_pos
  have hnum : 0 < Real.sin ((j : ℝ) * Real.pi / (N : ℝ)) := by
    refine Real.sin_pos_of_pos_of_lt_pi (by positivity) ?_
    rw [div_lt_iff₀ hN']
    nlinarith
  exact div_pos hnum hs

lemma sinRatio_nonneg {N j : ℕ} (hN : 3 ≤ N) (hjN : j ≤ N - 1) :
    0 ≤ sinRatio N j := by
  rcases Nat.eq_zero_or_pos j with rfl | hj
  · simp [sinRatio_zero]
  · exact (sinRatio_pos hN hj hjN).le

lemma lamN_pos {N : ℕ} (hN : 3 ≤ N) : 0 < lamN N := by
  have hN' : (3 : ℝ) ≤ (N : ℝ) := by exact_mod_cast hN
  have hpi := Real.pi_pos
  have h1 : 0 < Real.pi / (N : ℝ) := by positivity
  have h2 : Real.pi / (N : ℝ) < Real.pi / 2 := by
    rw [div_lt_div_iff₀ (by linarith) (by norm_num)]
    nlinarith
  have := Real.cos_pos_of_mem_Ioo ⟨by linarith, h2⟩
  simpa [lamN] using this

/-! ### The two-part continuant induction -/

/-- Ratio step of the no-wrap induction: consing a nonzero digit multiplies the
continuant magnitude by at least the next Chebyshev ratio. -/
lemma continuant_ratio_bound {N : ℕ} (hN : 3 ≤ N) :
    ∀ w : List ℤ, SyntacticallyReduced w → w.length + 1 ≤ N - 1 →
      ∀ n : ℤ, n ≠ 0 →
        sinRatio N (w.length + 2) * |continuant (lamN N) w| ≤
          sinRatio N (w.length + 1) * |continuant (lamN N) (n :: w)| := by
  intro w
  induction w with
  | nil =>
      intro _ _ n hn
      have hlam := lamN_pos hN
      have h1 : (1 : ℝ) ≤ |(n : ℝ)| := by
        have h : (1 : ℤ) ≤ |n| := Int.one_le_abs (by omega)
        have h' : ((1 : ℤ) : ℝ) ≤ ((|n| : ℤ) : ℝ) := by exact_mod_cast h
        rwa [Int.cast_abs, Int.cast_one] at h'
      have hc : |continuant (lamN N) [n]| = lamN N * |(n : ℝ)| := by
        show |lamN N * (n : ℝ)| = _
        rw [abs_mul, abs_of_pos hlam]
      simp only [List.length_nil, zero_add, hc]
      rw [sinRatio_one hN, sinRatio_two N hN]
      have : |continuant (lamN N) ([] : List ℤ)| = 1 := by
        show |(1 : ℝ)| = 1
        norm_num
      rw [this]
      nlinarith
  | cons m ns ih =>
      intro hred hlen n hn
      have hredns : SyntacticallyReduced ns := fun x hx => hred x (List.mem_cons_of_mem _ hx)
      have hm : m ≠ 0 := hred m (List.mem_cons_self ..)
      have hlenns : ns.length + 1 ≤ N - 1 := by
        simp only [List.length_cons] at hlen; omega
      have IH := ih hredns hlenns m hm
      -- notation
      set L := ns.length with hL
      have hlam := lamN_pos hN
      have h1 : (1 : ℝ) ≤ |(n : ℝ)| := by
        have h : (1 : ℤ) ≤ |n| := Int.one_le_abs (by omega)
        have h' : ((1 : ℤ) : ℝ) ≤ ((|n| : ℤ) : ℝ) := by exact_mod_cast h
        rwa [Int.cast_abs, Int.cast_one] at h'
      have hrec : continuant (lamN N) (n :: m :: ns)
          = lamN N * (n : ℝ) * continuant (lamN N) (m :: ns) - continuant (lamN N) ns := rfl
      have hstep : lamN N * |continuant (lamN N) (m :: ns)| - |continuant (lamN N) ns|
          ≤ |continuant (lamN N) (n :: m :: ns)| := by
        have hrev : |lamN N * (n : ℝ) * continuant (lamN N) (m :: ns)|
            - |continuant (lamN N) ns|
            ≤ |lamN N * (n : ℝ) * continuant (lamN N) (m :: ns)
                - continuant (lamN N) ns| := abs_sub_abs_le_abs_sub _ _
        have habs : |lamN N * (n : ℝ) * continuant (lamN N) (m :: ns)|
            = lamN N * |(n : ℝ)| * |continuant (lamN N) (m :: ns)| := by
          rw [abs_mul, abs_mul, abs_of_pos hlam]
        have hnn : 0 ≤ |continuant (lamN N) (m :: ns)| := abs_nonneg _
        have hmono : lamN N * |continuant (lamN N) (m :: ns)|
            ≤ lamN N * |(n : ℝ)| * |continuant (lamN N) (m :: ns)| := by
          have := mul_le_mul_of_nonneg_right
            (mul_le_mul_of_nonneg_left h1 hlam.le) hnn
          simpa using this
        rw [habs] at hrev
        rw [hrec]
        linarith
      have hpos : 0 ≤ sinRatio N (L + 2) := by
        have : L + 2 ≤ N - 1 := by
          simp only [List.length_cons, hL] at hlen ⊢; omega
        exact sinRatio_nonneg hN this
      -- assemble
      have hgoal : sinRatio N (L + 3) * |continuant (lamN N) (m :: ns)|
          ≤ sinRatio N (L + 2) * |continuant (lamN N) (n :: m :: ns)| := by
        have h2 : sinRatio N (L + 2) *
            (lamN N * |continuant (lamN N) (m :: ns)| - |continuant (lamN N) ns|)
            ≤ sinRatio N (L + 2) * |continuant (lamN N) (n :: m :: ns)| :=
          mul_le_mul_of_nonneg_left hstep hpos
        have hIH' : sinRatio N (L + 2) * |continuant (lamN N) ns|
            ≤ sinRatio N (L + 1) * |continuant (lamN N) (m :: ns)| := by
          simpa [hL] using IH
        have hrec3 : sinRatio N (L + 3)
            = lamN N * sinRatio N (L + 2) - sinRatio N (L + 1) := by
          have := sinRatio_rec N (L + 1)
          simpa [show L + 1 + 2 = L + 3 from rfl, show L + 1 + 1 = L + 2 from rfl] using this
        have expand : sinRatio N (L + 3) * |continuant (lamN N) (m :: ns)|
            = sinRatio N (L + 2) * (lamN N * |continuant (lamN N) (m :: ns)|)
              - sinRatio N (L + 1) * |continuant (lamN N) (m :: ns)| := by
          rw [hrec3]; ring
        have h2' : sinRatio N (L + 2) * (lamN N * |continuant (lamN N) (m :: ns)|)
            - sinRatio N (L + 2) * |continuant (lamN N) ns|
            ≤ sinRatio N (L + 2) * |continuant (lamN N) (n :: m :: ns)| := by
          have : sinRatio N (L + 2) *
              (lamN N * |continuant (lamN N) (m :: ns)| - |continuant (lamN N) ns|)
              = sinRatio N (L + 2) * (lamN N * |continuant (lamN N) (m :: ns)|)
                - sinRatio N (L + 2) * |continuant (lamN N) ns| := by ring
          linarith [h2, this]
        linarith [expand, h2', hIH']
      simpa [hL, show ns.length + 1 + 2 = L + 3 from rfl,
        show ns.length + 1 + 1 = L + 2 from rfl] using hgoal

/-- Sharp lower bound on the continuant magnitude of a syntactically reduced
word. -/
lemma continuant_abs_lower {N : ℕ} (hN : 3 ≤ N) :
    ∀ w : List ℤ, SyntacticallyReduced w → w.length + 1 ≤ N - 1 →
      sinRatio N (w.length + 1) ≤ |continuant (lamN N) w| := by
  intro w
  induction w with
  | nil =>
      intro _ _
      simp only [List.length_nil, zero_add]
      rw [sinRatio_one hN]
      show (1 : ℝ) ≤ |(1 : ℝ)|
      norm_num
  | cons n ns ih =>
      intro hred hlen
      have hredns : SyntacticallyReduced ns := fun x hx => hred x (List.mem_cons_of_mem _ hx)
      have hn : n ≠ 0 := hred n (List.mem_cons_self ..)
      have hlenns : ns.length + 1 ≤ N - 1 := by
        simp only [List.length_cons] at hlen; omega
      have IH := ih hredns hlenns
      have hratio := continuant_ratio_bound hN ns hredns hlenns n hn
      have hposprev : 0 < sinRatio N (ns.length + 1) :=
        sinRatio_pos hN (by omega) hlenns
      have hposnext : 0 ≤ sinRatio N (ns.length + 2) := by
        have : ns.length + 2 ≤ N - 1 := by
          simp only [List.length_cons] at hlen; omega
        exact sinRatio_nonneg hN this
      have key : sinRatio N (ns.length + 2) * sinRatio N (ns.length + 1)
          ≤ sinRatio N (ns.length + 1) * |continuant (lamN N) (n :: ns)| := by
        have := mul_le_mul_of_nonneg_left IH hposnext
        linarith [hratio]
      have := le_of_mul_le_mul_left (by linarith [key] : sinRatio N (ns.length + 1) *
        sinRatio N (ns.length + 2) ≤ sinRatio N (ns.length + 1) *
          |continuant (lamN N) (n :: ns)|) hposprev
      simpa [show ns.length + 1 + 1 = ns.length + 2 from rfl] using this

/-- Sharp finite no-wrap lower envelope for every syntactically reduced raw
word of `Q`-depth `k <= N-1`.

Source/status: `M2_LOCALIZATION_THEOREM_SOL.md:484-578`, with the omitted
ordering repaired at lines 556-568; `M1_LOCALIZATION_TRIPLE_REFEREE.md:223-280`
adjudicates the theorem TRUE after that repair.  PAPER/REFEREE CONFIRMED;
Lean target OPEN.  This is not an unrestricted-depth or global localization
statement.

The hypothesis `hk0 : 1 <= k` is kept as dispatched, but it is automatically
implied by `depth w = k`; the proof does not use it. -/
theorem sharp_no_wrap
    (N k : ℕ) (hN : 3 ≤ N) (w : List ℤ)
    (hred : SyntacticallyReduced w) (hdepth : depth w = k)
    (hk0 : 1 ≤ k) (hkN : k ≤ N - 1) :
    |c (lamN N) w| ≥
      lamN N *
        (Real.sin ((k : ℝ) * Real.pi / (N : ℝ)) /
          Real.sin (Real.pi / (N : ℝ))) := by
  have hlen : w.length + 1 = k := hdepth
  have hlam := lamN_pos hN
  have hbound := continuant_abs_lower hN w hred (by omega)
  have habs : |c (lamN N) w| = lamN N * |continuant (lamN N) w| := by
    rw [c_eq_lam_mul_continuant, abs_mul, abs_of_pos hlam]
  rw [habs]
  have : sinRatio N k ≤ |continuant (lamN N) w| := by rwa [hlen] at hbound
  have hgoal := mul_le_mul_of_nonneg_left this hlam.le
  simpa [sinRatio] using hgoal

/-! ## 3. Equality at the two constant-sign Chebyshev words -/

/-- The all-`+1` word of depth `m`, copied exactly from v26. -/
def chebyshevWord (m : ℕ) : List ℤ := List.replicate (m - 1) (1 : ℤ)

/-- The all-`-1` word of depth `m`. -/
def negativeChebyshevWord (m : ℕ) : List ℤ :=
  List.replicate (m - 1) (-1 : ℤ)

lemma continuant_replicate_one (lam : ℝ) (j : ℕ) :
    continuant lam (List.replicate j (1 : ℤ))
      = aeval (lam / 2) (Polynomial.Chebyshev.U ℝ (j : ℤ)) := by
  induction j using Nat.twoStepInduction with
  | zero => simp [continuant, Polynomial.Chebyshev.U_zero]
  | one =>
      show lam * ((1 : ℤ) : ℝ) = _
      rw [show ((1 : ℕ) : ℤ) = 1 from rfl, Polynomial.Chebyshev.U_one]
      simp
      ring
  | more j ih1 ih2 =>
      have hrep : List.replicate (j + 2) (1 : ℤ)
          = (1 : ℤ) :: (1 : ℤ) :: List.replicate j (1 : ℤ) := by
        simp [List.replicate_succ]
      rw [hrep]
      show lam * ((1 : ℤ) : ℝ) * continuant lam ((1 : ℤ) :: List.replicate j 1)
          - continuant lam (List.replicate j 1) = _
      rw [show ((1 : ℤ) :: List.replicate j (1 : ℤ)) = List.replicate (j + 1) (1 : ℤ) by
        simp [List.replicate_succ], ih2, ih1]
      have : ((j : ℤ) + 2) = ((j + 2 : ℕ) : ℤ) := by push_cast; ring
      rw [← this, Polynomial.Chebyshev.U_add_two]
      have h1 : ((j : ℤ) + 1) = ((j + 1 : ℕ) : ℤ) := by push_cast; ring
      rw [← h1, map_sub, map_mul, map_mul, aeval_X]
      simp only [map_ofNat, Int.cast_one]
      ring

/-- Local standalone copy of the v26 Chebyshev bridge
`c = lam * U_{m-1}(lam/2)`.

Source/status: harvested v26
`projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/RateCore.lean:332-340`;
MACHINE-VERIFIED there by an independent sorry-free rebuild.  Re-dispatched
here only because v29 is a standalone `import Mathlib` file. -/
theorem c_chebyshevWord (m : ℕ) (hm : 1 ≤ m) (lam : ℝ) :
    c lam (chebyshevWord m) =
      lam * aeval (lam / 2) (Polynomial.Chebyshev.U ℝ ((m : ℤ) - 1)) := by
  rw [chebyshevWord, c_eq_lam_mul_continuant, continuant_replicate_one]
  congr 3
  omega

lemma continuant_replicate_neg_one (lam : ℝ) (j : ℕ) :
    continuant lam (List.replicate j (-1 : ℤ))
      = (-1 : ℝ) ^ j * continuant lam (List.replicate j (1 : ℤ)) := by
  induction j using Nat.twoStepInduction with
  | zero => simp [continuant]
  | one =>
      show lam * ((-1 : ℤ) : ℝ) = _
      show _ = (-1 : ℝ) ^ 1 * (lam * ((1 : ℤ) : ℝ))
      push_cast
      ring
  | more j ih1 ih2 =>
      have hrepn : List.replicate (j + 2) (-1 : ℤ)
          = (-1 : ℤ) :: (-1 : ℤ) :: List.replicate j (-1 : ℤ) := by
        simp [List.replicate_succ]
      have hrepp : List.replicate (j + 2) (1 : ℤ)
          = (1 : ℤ) :: (1 : ℤ) :: List.replicate j (1 : ℤ) := by
        simp [List.replicate_succ]
      rw [hrepn, hrepp]
      show lam * ((-1 : ℤ) : ℝ) * continuant lam ((-1 : ℤ) :: List.replicate j (-1)) -
          continuant lam (List.replicate j (-1))
        = (-1 : ℝ) ^ (j + 2) *
          (lam * ((1 : ℤ) : ℝ) * continuant lam ((1 : ℤ) :: List.replicate j 1) -
            continuant lam (List.replicate j 1))
      rw [show ((-1 : ℤ) :: List.replicate j (-1 : ℤ)) = List.replicate (j + 1) (-1 : ℤ) by
        simp [List.replicate_succ],
        show ((1 : ℤ) :: List.replicate j (1 : ℤ)) = List.replicate (j + 1) (1 : ℤ) by
        simp [List.replicate_succ], ih2, ih1]
      push_cast
      ring

/-- Referee-required signed form of the all-`-1` equality: the signed
lower-left entry differs from the all-`+1` entry by `(-1)^(m-1)`.  Equality in
the sharp envelope is therefore an equality of absolute values.

Source/status: `M2_LOCALIZATION_THEOREM_SOL.md:580-587` and
`M1_LOCALIZATION_TRIPLE_REFEREE.md:267-280`; REFEREE-CONFIRMED sign repair,
Lean target OPEN.

The hypothesis `hm : 1 <= m` is kept as dispatched; the identity also holds
degenerately at `m = 0` (both words are empty), so the proof does not use
it. -/
theorem c_negativeChebyshevWord_sign (m : ℕ) (hm : 1 ≤ m) (lam : ℝ) :
    c lam (negativeChebyshevWord m) =
      (-1 : ℝ) ^ (m - 1) * c lam (chebyshevWord m) := by
  rw [negativeChebyshevWord, chebyshevWord, c_eq_lam_mul_continuant,
    c_eq_lam_mul_continuant, continuant_replicate_neg_one]
  ring

lemma continuant_replicate_one_eq_sinRatio {N : ℕ} (hN : 3 ≤ N) (j : ℕ) :
    continuant (lamN N) (List.replicate j (1 : ℤ)) = sinRatio N (j + 1) := by
  induction j using Nat.twoStepInduction with
  | zero => simpa [continuant] using (sinRatio_one hN).symm
  | one =>
      show lamN N * ((1 : ℤ) : ℝ) = _
      rw [show (1 : ℕ) + 1 = 2 from rfl, sinRatio_two N hN]
      push_cast; ring
  | more j ih1 ih2 =>
      have hrep : List.replicate (j + 2) (1 : ℤ)
          = (1 : ℤ) :: (1 : ℤ) :: List.replicate j (1 : ℤ) := by
        simp [List.replicate_succ]
      rw [hrep]
      show lamN N * ((1 : ℤ) : ℝ) * continuant (lamN N) ((1 : ℤ) :: List.replicate j 1)
          - continuant (lamN N) (List.replicate j 1) = _
      rw [show ((1 : ℤ) :: List.replicate j (1 : ℤ)) = List.replicate (j + 1) (1 : ℤ) by
        simp [List.replicate_succ], ih2, ih1]
      have := sinRatio_rec N (j + 1)
      push_cast
      rw [show j + 2 + 1 = (j + 1) + 2 from rfl, this]
      ring

/-- Both constant-sign unit-digit words attain the sharp no-wrap envelope.
The `eps = -1` branch uses `c_negativeChebyshevWord_sign`; it does not claim
equality of the signed `c`-values.

Source/status: `M2_LOCALIZATION_THEOREM_SOL.md:503-587` and
`M1_LOCALIZATION_TRIPLE_REFEREE.md:267-280`; PAPER/REFEREE CONFIRMED,
Lean target OPEN. -/
theorem sharp_no_wrap_eq_chebyshev_words
    (N k : ℕ) (hN : 3 ≤ N) (hk0 : 1 ≤ k) (hkN : k ≤ N - 1)
    (eps : ℤ) (heps : eps = 1 ∨ eps = -1) :
    |c (lamN N) (List.replicate (k - 1) eps)| =
      lamN N *
        (Real.sin ((k : ℝ) * Real.pi / (N : ℝ)) /
          Real.sin (Real.pi / (N : ℝ))) := by
  have hlam := lamN_pos hN
  have hval : |continuant (lamN N) (List.replicate (k - 1) eps)| = sinRatio N k := by
    have hpos : 0 ≤ sinRatio N k := sinRatio_nonneg hN hkN
    rcases heps with rfl | rfl
    · rw [continuant_replicate_one_eq_sinRatio hN, show k - 1 + 1 = k by omega,
        abs_of_nonneg hpos]
    · rw [continuant_replicate_neg_one, abs_mul, continuant_replicate_one_eq_sinRatio hN,
        show k - 1 + 1 = k by omega, abs_of_nonneg hpos, abs_pow]
      simp
  rw [c_eq_lam_mul_continuant, abs_mul, abs_of_pos hlam, hval]
  simp [sinRatio]

/-! ## 4. Route B: three bounded algebraic targets -/

/-- `R = Q S` in the Route-B Tietze dictionary. -/
noncomputable def Rmat (lam : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  Qmat lam * Spow 1

/-- The `SL(2, R)` lift satisfies `Q^2 = -I` (not `+I`).

Source/status: `M1_ROUTE_B_REPAIR_SOL.md:285-320`, confirmed again at
`M1_LOCALIZATION_TRIPLE_REFEREE.md:70-92`; ROUTE-B PAPER/REFEREE CONFIRMED,
Lean target OPEN. -/
theorem Qmat_sq_neg_one (lam : ℝ) (hlam : lam ≠ 0) :
    Qmat lam * Qmat lam = -(1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Qmat, Matrix.mul_apply, Fin.sum_univ_succ] <;>
    field_simp

lemma Rmat_eq (lam : ℝ) : Rmat lam = !![0, -1 / lam; lam, lam] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Rmat, Qmat, Spow, Matrix.mul_apply, Fin.sum_univ_succ]

lemma Rmat_sq (lam : ℝ) (hlam : lam ≠ 0) :
    Rmat lam * Rmat lam = lam • Rmat lam - (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  rw [Rmat_eq]
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_succ] <;>
    (field_simp; try ring)

/-- The `SL(2)` power expansion `R^{j+1} = v_{j+1} R - v_j I`. -/
lemma Rmat_pow_succ_eq {N : ℕ} (hN : 3 ≤ N) (j : ℕ) :
    (Rmat (lamN N)) ^ (j + 1)
      = sinRatio N (j + 1) • Rmat (lamN N)
        - sinRatio N j • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  have hlam := (lamN_pos hN).ne'
  induction j with
  | zero => simp [sinRatio_one hN, sinRatio_zero]
  | succ j ih =>
      have hsq := Rmat_sq (lamN N) hlam
      calc (Rmat (lamN N)) ^ (j + 2)
          = (Rmat (lamN N)) ^ (j + 1) * Rmat (lamN N) := by rw [pow_succ]
        _ = (sinRatio N (j + 1) • Rmat (lamN N)
              - sinRatio N j • (1 : Matrix (Fin 2) (Fin 2) ℝ)) * Rmat (lamN N) := by rw [ih]
        _ = sinRatio N (j + 1) • (Rmat (lamN N) * Rmat (lamN N))
              - sinRatio N j • Rmat (lamN N) := by
              simp [sub_mul]
        _ = sinRatio N (j + 1) • (lamN N • Rmat (lamN N)
              - (1 : Matrix (Fin 2) (Fin 2) ℝ)) - sinRatio N j • Rmat (lamN N) := by
              rw [hsq]
        _ = (lamN N * sinRatio N (j + 1) - sinRatio N j) • Rmat (lamN N)
              - sinRatio N (j + 1) • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
              rw [smul_sub, smul_smul]
              module
        _ = sinRatio N (j + 2) • Rmat (lamN N)
              - sinRatio N (j + 1) • (1 : Matrix (Fin 2) (Fin 2) ℝ) := by
              rw [sinRatio_rec N j]

/-- For `lamN N = 2 cos(pi/N)`, the `SL(2, R)` lift satisfies `R^N = -I`.
The associated PSL relation is `bar R^N = 1`; this theorem deliberately keeps
the lift sign visible and asserts no PSL presentation API.

Source/status: `M1_ROUTE_B_REPAIR_SOL.md:285-320`, with q=5,7 exact checks at
`M1_LOCALIZATION_TRIPLE_REFEREE.md:70-92`; ROUTE-B PAPER/REFEREE CONFIRMED,
Lean target OPEN. -/
theorem Rmat_pow_lamN_neg_one (N : ℕ) (hN : 3 ≤ N) :
    (Rmat (lamN N)) ^ N = -(1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  obtain ⟨j, rfl⟩ : ∃ j, N = j + 1 := ⟨N - 1, by omega⟩
  have hs := sin_pi_div_N_pos hN
  have hN0 : ((j + 1 : ℕ) : ℝ) ≠ 0 := by positivity
  have hvN : sinRatio (j + 1) (j + 1) = 0 := by
    unfold sinRatio
    rw [show ((j + 1 : ℕ) : ℝ) * Real.pi / ((j + 1 : ℕ) : ℝ) = Real.pi by
      field_simp]
    simp
  have hvN1 : sinRatio (j + 1) j = 1 := by
    unfold sinRatio
    have : (j : ℝ) * Real.pi / ((j + 1 : ℕ) : ℝ)
        = Real.pi - Real.pi / ((j + 1 : ℕ) : ℝ) := by
      field_simp
      push_cast
      ring
    rw [this, Real.sin_pi_sub, div_self hs.ne']
  rw [Rmat_pow_succ_eq hN j, hvN, hvN1]
  simp

/-! ### List-syllable core of the four-sign cancellation lemma -/

/-- A tagged free-product syllable: `q` is the nonidentity `C_2` syllable and
`r a` is an `R`-syllable with exponent `a : ZMod N`. -/
inductive Syllable (N : ℕ)
  | q : Syllable N
  | r : ZMod N → Syllable N
  deriving DecidableEq

/-- A tagged syllable is nontrivial exactly when an `R` exponent is nonzero. -/
def syllableNontrivial {N : ℕ} : Syllable N → Prop
  | .q => True
  | .r a => a ≠ 0

/-- The free factor containing a syllable. -/
def syllableKind {N : ℕ} : Syllable N → Bool
  | .q => false
  | .r _ => true

/-- Syntactic reducedness for a list of free-product syllables: every syllable
is nontrivial and adjacent syllables come from different factors. -/
def SyllableReduced {N : ℕ} : List (Syllable N) → Prop
  | [] => True
  | [x] => syllableNontrivial x
  | x :: y :: xs =>
      syllableNontrivial x ∧ syllableKind x ≠ syllableKind y ∧
        SyllableReduced (y :: xs)

/-! #### Structural lemmas for `SyllableReduced` -/

lemma syllableReduced_cons_iff {N : ℕ} (x : Syllable N) (l : List (Syllable N)) :
    SyllableReduced (x :: l) ↔
      syllableNontrivial x ∧ SyllableReduced l ∧
        ∀ y ∈ l.head?, syllableKind x ≠ syllableKind y := by
  cases l with
  | nil => simp [SyllableReduced]
  | cons y ys =>
      constructor
      · rintro ⟨h1, h2, h3⟩; exact ⟨h1, h3, by simpa using h2⟩
      · rintro ⟨h1, h2, h3⟩
        exact ⟨h1, by simpa using h3, h2⟩

lemma syllableReduced_head_replace {N : ℕ} {x x' : Syllable N} {l : List (Syllable N)}
    (h : SyllableReduced (x :: l)) (hk : syllableKind x' = syllableKind x)
    (hnt : syllableNontrivial x') : SyllableReduced (x' :: l) := by
  rw [syllableReduced_cons_iff] at h ⊢
  obtain ⟨_, h2, h3⟩ := h
  exact ⟨hnt, h2, by intro y hy; rw [hk]; exact h3 y hy⟩

lemma syllableReduced_cons {N : ℕ} {y x : Syllable N} {l : List (Syllable N)}
    (h : SyllableReduced (x :: l)) (hnt : syllableNontrivial y)
    (hk : syllableKind y ≠ syllableKind x) : SyllableReduced (y :: x :: l) :=
  ⟨hnt, hk, h⟩

lemma syllableReduced_snoc {N : ℕ} :
    ∀ (l : List (Syllable N)) (x y : Syllable N),
      SyllableReduced (l ++ [x]) → syllableNontrivial y →
      syllableKind y ≠ syllableKind x → SyllableReduced (l ++ [x, y]) := by
  intro l
  induction l with
  | nil =>
      intro x y h hnt hk
      exact ⟨h, Ne.symm hk, hnt⟩
  | cons z zs ih =>
      intro x y h hnt hk
      rw [List.cons_append, syllableReduced_cons_iff] at h ⊢
      obtain ⟨h1, h2, h3⟩ := h
      refine ⟨h1, ih x y h2 hnt hk, ?_⟩
      intro w hw
      apply h3
      cases zs with
      | nil => simpa using hw
      | cons a as => simpa using hw

lemma syllableReduced_last_replace {N : ℕ} :
    ∀ (l : List (Syllable N)) (x x' : Syllable N),
      SyllableReduced (l ++ [x]) → syllableKind x' = syllableKind x →
      syllableNontrivial x' → SyllableReduced (l ++ [x']) := by
  intro l
  induction l with
  | nil => intro x x' _ _ hnt; exact hnt
  | cons z zs ih =>
      intro x x' h hk hnt
      rw [List.cons_append, syllableReduced_cons_iff] at h ⊢
      obtain ⟨h1, h2, h3⟩ := h
      refine ⟨h1, ih x x' h2 hk hnt, ?_⟩
      intro w hw
      cases zs with
      | nil =>
          simp only [List.nil_append, List.head?_cons, Option.mem_def,
            Option.some.injEq] at hw
          subst hw
          rw [hk]
          exact h3 x (by simp)
      | cons a as => exact h3 w (by simpa using hw)

lemma zmod_one_ne_zero {N : ℕ} (hN : 3 ≤ N) : (1 : ZMod N) ≠ 0 := by
  haveI : Fact (1 < N) := ⟨by omega⟩
  exact one_ne_zero

/-- Four-sign boundary cancellation, stated at the exact `List`-syllable
level.  Assume the Route-B middle
`R^a0 :: middle ++ [R^ak]` is reduced, all endpoint syllables are nontrivial,
and `a0 != -1`, `ak != 1` in `ZMod N`.  Then the four local displays produced
by left-positive, left-negative, right-positive, and right-negative
translations are still reduced.  The literal `middle` sublist is unchanged,
so cancellation cannot enter or traverse it.

This is only the finite free-product list algebra.  It does not assert the
group presentation, canonical-section existence, or a localization/RATE
estimate.

The nontriviality hypotheses `ha0`, `hak` are kept as dispatched; they are
already consequences of `hcore`, so the proof does not use them.

Source/status: `M1_ROUTE_B_REPAIR_SOL.md:508-556`, independently confirmed at
`M1_LOCALIZATION_TRIPLE_REFEREE.md:136-175`; ROUTE-B PAPER/REFEREE CONFIRMED,
Lean target OPEN. -/
theorem four_sign_boundary_cancellation
    (N : ℕ) (hN : 3 ≤ N) (a0 ak : ZMod N)
    (middle : List (Syllable N))
    (hcore : SyllableReduced
      ([Syllable.r a0] ++ middle ++ [Syllable.r ak]))
    (ha0 : a0 ≠ 0) (hak : ak ≠ 0)
    (hleft : a0 ≠ -1) (hright : ak ≠ 1) :
    SyllableReduced
        ([Syllable.q, Syllable.r (a0 + 1)] ++ middle ++ [Syllable.r ak]) ∧
      SyllableReduced
        ([Syllable.r (-1), Syllable.q, Syllable.r a0] ++
          middle ++ [Syllable.r ak]) ∧
      SyllableReduced
        ([Syllable.r a0] ++ middle ++
          [Syllable.r ak, Syllable.q, Syllable.r 1]) ∧
      SyllableReduced
        ([Syllable.r a0] ++ middle ++
          [Syllable.r (ak - 1), Syllable.q]) := by
  have h1ne : (1 : ZMod N) ≠ 0 := zmod_one_ne_zero hN
  have hm1ne : (-1 : ZMod N) ≠ 0 := neg_ne_zero.2 h1ne
  have ha1 : a0 + 1 ≠ 0 := fun h => hleft (eq_neg_of_add_eq_zero_left h)
  have hak1 : ak - 1 ≠ 0 := sub_ne_zero.2 hright
  -- normalise the core hypothesis to a `cons` shape
  have hcore' : SyllableReduced (Syllable.r a0 :: (middle ++ [Syllable.r ak])) := by
    simpa using hcore
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- left, positive
    have h := syllableReduced_head_replace (x' := Syllable.r (a0 + 1)) hcore' rfl ha1
    have := syllableReduced_cons (y := Syllable.q) h trivial (by simp [syllableKind])
    simpa using this
  · -- left, negative
    have h1 := syllableReduced_cons (y := Syllable.q) hcore' trivial (by simp [syllableKind])
    have h2 := syllableReduced_cons (y := Syllable.r (-1)) h1 hm1ne (by simp [syllableKind])
    simpa using h2
  · -- right, positive
    have hcore'' : SyllableReduced
        ((Syllable.r a0 :: middle) ++ [Syllable.r ak]) := by simpa using hcore
    have h1 := syllableReduced_snoc (Syllable.r a0 :: middle) (Syllable.r ak)
      Syllable.q hcore'' trivial (by simp [syllableKind])
    have h2 := syllableReduced_snoc ((Syllable.r a0 :: middle) ++ [Syllable.r ak])
      Syllable.q (Syllable.r 1) (by simpa using h1) h1ne (by simp [syllableKind])
    simpa using h2
  · -- right, negative
    have hcore'' : SyllableReduced
        ((Syllable.r a0 :: middle) ++ [Syllable.r ak]) := by simpa using hcore
    have h1 := syllableReduced_last_replace (Syllable.r a0 :: middle) (Syllable.r ak)
      (Syllable.r (ak - 1)) hcore'' rfl hak1
    have h2 := syllableReduced_snoc (Syllable.r a0 :: middle) (Syllable.r (ak - 1))
      Syllable.q h1 trivial (by simp [syllableKind])
    simpa using h2

end RateCoreIV
