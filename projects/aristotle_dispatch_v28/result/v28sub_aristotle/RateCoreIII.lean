import Mathlib

/-!
# RATE lemma — Shimizu/Ford reduction + M1 key algebra (v28 dispatch)

Sources:

* `research_notes/rh_goals_2026-08-14/lane_g/M2_FORD_PACKING_REFEREE.md`
  (Ford replacement CONFIRMED at paper level; Lean formalization OPEN), and
  `M2_G1G2_CLOSURE_SOL.md` §6 (Lean dispatch candidates 9–10).
* `research_notes/rh_goals_2026-08-14/lane_g/M1_COSET_STRATEGY_SOL.md`
  §6 (translation action and arithmetic key normalization are a CONJECTURAL
  TARGET marked Lean-formalizable).

Mathlib v4.28.0 has generic `SL(2, ℝ)` matrix algebra, `PSL(n, R)` as a
quotient, and an upper-half-plane Möbius action.  The cached source has no
Shimizu lemma, Jørgensen inequality, or Fuchsian-group API.  Therefore §1 is
the honest weaker target: the commutator trace is computed from matrix algebra,
while the Jørgensen inequality supplied by discreteness/non-elementarity is an
explicit hypothesis.  No predicate below is claimed to *define* discreteness.

The Ford theorem in §2 is only the finite combinatorial core after geometry has
produced pairwise-disjoint arcs on a circle of circumference one.  The
horoball-to-arc injection is not smuggled into an assumption called a theorem.

Conventions in §0 are copied verbatim from v26 `RateCore.lean` and v27
`RateCoreII.lean`: `Qmat`, `Spow`, `wordMatrix`, `depth`, and `c` have exactly
the same definitions.

**FALSE-statement escape hatch (same rule as v27).** If any target is FALSE as
stated, do not force its `sorry`.  Retain the original statement only inside a
`FALSE AS STATED` comment, prove a named `<target>_false` negation with an exact
witness, and then state and prove the weakest corrected `<target>'` theorem.
-/

open scoped BigOperators

namespace RateCoreIII

/-! ## 0. Setup: v26/v27 conventions, verbatim -/

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

/-- `d_w(λ)`, the lower-right entry needed for the coset key `(c, d mod c)`. -/
noncomputable def d (lam : ℝ) (w : List ℤ) : ℝ := wordMatrix lam w 1 1

/-! ## 1. Shimizu's lemma: matrix core with explicit Jørgensen input -/

/-- The explicit adjugate of a `2 × 2` matrix.  If `det B = 1`, this is
`B⁻¹`; using it avoids pretending that Mathlib already connects arbitrary
Fuchsian subgroups of `PSL(2, ℝ)` to a matrix representative API. -/
def detOneInverse (B : Matrix (Fin 2) (Fin 2) ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![B 1 1, -B 0 1; -B 1 0, B 0 0]

/-- `[S,B] = S B S⁻¹ B⁻¹` for `S : z ↦ z+1`, using `detOneInverse B` for
the final factor. -/
def unitTranslationCommutator (B : Matrix (Fin 2) (Fin 2) ℝ) :
    Matrix (Fin 2) (Fin 2) ℝ :=
  Spow 1 * B * Spow (-1) * detOneInverse B

/-- The exact inequality input supplied by Jørgensen in the classical proof.
This is deliberately *not* named `Discrete` or `NonElementary`: Mathlib v4.28
does not provide the theorem connecting those geometric hypotheses to this
inequality.

Source/status: Series, Theorem 2.21 and Lemma 2.22 as transcribed in
`M2_FORD_PACKING_REFEREE.md:21-41`; PAPER-LEVEL CONFIRMED, Lean bridge OPEN. -/
def WidthOneJorgensenAssumption
    (Gamma : Set (Matrix (Fin 2) (Fin 2) ℝ)) : Prop :=
  ∀ B ∈ Gamma, B 1 0 ≠ 0 →
    Matrix.det B = 1 ∧ 1 ≤ |Matrix.trace (unitTranslationCommutator B) - 2|

/-- For a determinant-one matrix `B = [[a,b],[c,d]]`,
`tr([S,B]) = 2 + c²`.

Source/status: the matrix identity used in Series' proof, recorded at
`M2_FORD_PACKING_REFEREE.md:33-38`; PAPER-LEVEL RECEIPTED, Lean target OPEN. -/
theorem trace_unitTranslationCommutator (B : Matrix (Fin 2) (Fin 2) ℝ)
    (hdet : Matrix.det B = 1) :
    Matrix.trace (unitTranslationCommutator B) = 2 + (B 1 0) ^ 2 := by
  rw [Matrix.det_fin_two] at hdet
  rw [Matrix.eta_fin_two B]
  simp [unitTranslationCommutator, Spow, detOneInverse, Matrix.trace_fin_two]
  nlinarith [hdet]

/-- Honest Mathlib-facing form of Shimizu's lower-left bound: matrices in the
explicit width-one Jørgensen domain with nonzero lower-left entry satisfy
`|c| ≥ 1`.

Source/status: Shimizu's lemma in Series, transcribed in
`M2_FORD_PACKING_REFEREE.md:21-41` and `M2_G1G2_CLOSURE_SOL.md:51-55`;
PAPER-LEVEL CONFIRMED, full discrete/Fuchsian Lean bridge OPEN.  This theorem
only asks Aristotle for the algebraic implication from the explicit input. -/
theorem shimizu_lower_left_of_explicit_jorgensen
    (Gamma : Set (Matrix (Fin 2) (Fin 2) ℝ))
    (hGamma : WidthOneJorgensenAssumption Gamma)
    {B : Matrix (Fin 2) (Fin 2) ℝ} (hB : B ∈ Gamma) (hc : B 1 0 ≠ 0) :
    1 ≤ |B 1 0| := by
  obtain ⟨hdet, hineq⟩ := hGamma B hB hc
  rw [trace_unitTranslationCommutator B hdet] at hineq
  have hsq : 1 ≤ (B 1 0) ^ 2 := by
    have : |2 + (B 1 0) ^ 2 - 2| = (B 1 0) ^ 2 := by
      rw [show 2 + (B 1 0) ^ 2 - 2 = (B 1 0) ^ 2 by ring, abs_of_nonneg (sq_nonneg _)]
    linarith [this ▸ hineq]
  nlinarith [abs_nonneg (B 1 0), sq_abs (B 1 0)]

/-! ## 2. Ford packing: finite circle-arc core -/

/-- Finite combinatorial core of `A_Γ(X) ≤ ⌊X²⌋`.

`arcLength i` is the length of the cross-section arc belonging to one double
coset.  Geometry must separately prove that the arcs are pairwise disjoint on
the unit circle and hence that their length sum is at most `1`; that reduced
consequence is the hypothesis `hcircle`.  The Ford computation supplies the
lower bound `1 / X²`, represented by `hmin`.

Source/status: `M2_FORD_PACKING_REFEREE.md:74-116` and
`M2_G1G2_CLOSURE_SOL.md:315-331`; the group-level result is PAPER-LEVEL
CONFIRMED and Lean OPEN.  This statement is only its finite arithmetic layer. -/
theorem ford_count_le_floor_sq_of_circle_arcs
    {ι : Type*} [DecidableEq ι] (arcs : Finset ι) (arcLength : ι → ℝ)
    (X : ℝ) (hX : 1 ≤ X)
    (hmin : ∀ i ∈ arcs, 1 / X ^ 2 ≤ arcLength i)
    (hcircle : ∑ i ∈ arcs, arcLength i ≤ 1) :
    arcs.card ≤ ⌊X ^ 2⌋₊ := by
  have hX0 : (0 : ℝ) < X ^ 2 := by nlinarith
  have h := Finset.card_nsmul_le_sum arcs arcLength (1 / X ^ 2) hmin
  rw [nsmul_eq_mul] at h
  have hle : (arcs.card : ℝ) * (1 / X ^ 2) ≤ 1 := le_trans h hcircle
  have h2 : (arcs.card : ℝ) ≤ X ^ 2 := by
    rw [mul_one_div, div_le_one hX0] at hle
    linarith
  exact Nat.le_floor h2

/-! ## 3. M1-coset algebra: translations and normalized `(c,d mod c)` key -/

/-- The representative of `d mod c` in `[0,c)` when `c>0`:
`d - c floor(d/c)`.

Source/status: `M1_COSET_STRATEGY_SOL.md:82-87,363-378,470-483`;
CONJECTURAL TARGET marked Lean-formalizable. -/
noncomputable def red (cc dd : ℝ) : ℝ :=
  dd - cc * ((⌊dd / cc⌋ : ℤ) : ℝ)

/-- The normalized bottom-row key.  Its intended coset use always carries the
separate sign/nonparabolic hypothesis `0 < c`.

Source/status: `M1_COSET_STRATEGY_SOL.md:69-87`; CONJECTURAL TARGET,
Lean-formalizable arithmetic layer only. -/
noncomputable def bottomRowKey (M : Matrix (Fin 2) (Fin 2) ℝ) : ℝ × ℝ :=
  (M 1 0, red (M 1 0) (M 1 1))

/-- Exact left/right translation action on the lower row:
`S^u M S^v` keeps `c` fixed and sends `d` to `d + v c`.

Source/status: `M1_COSET_STRATEGY_SOL.md:69-87,363-378,470-483`;
CONJECTURAL TARGET marked Lean-formalizable.  This does not assert key
completeness, the NF–Rosen bridge, or any of M1-W/I/S/L. -/
theorem doubleTranslation_bottomRow (lam : ℝ) (w : List ℤ) (u v : ℤ) :
    (Spow u * wordMatrix lam w * Spow v) 1 0 = c lam w ∧
      (Spow u * wordMatrix lam w * Spow v) 1 1 =
        d lam w + (v : ℝ) * c lam w := by
  simp only [c, d]
  rw [Matrix.eta_fin_two (wordMatrix lam w)]
  refine ⟨by simp [Spow], ?_⟩
  simp [Spow]
  ring

/-- Floor normalization lands in the half-open interval `[0,c)`.

Source/status: the arithmetic normalization target in
`M1_COSET_STRATEGY_SOL.md:82-87,470-483`; CONJECTURAL TARGET marked
Lean-formalizable. -/
theorem red_mem_Ico (cc dd : ℝ) (hcc : 0 < cc) : red cc dd ∈ Set.Ico 0 cc := by
  constructor
  · have h := Int.floor_le (dd / cc)
    have h2 := mul_le_mul_of_nonneg_left h hcc.le
    rw [mul_div_cancel₀ _ hcc.ne'] at h2
    simpa [red] using h2
  · have h := Int.lt_floor_add_one (dd / cc)
    have h2 := mul_lt_mul_of_pos_left h hcc
    rw [mul_div_cancel₀ _ hcc.ne'] at h2
    simp only [red]
    nlinarith

/-- Floor normalization is invariant under an integral multiple of `c`.

Source/status: the arithmetic normalization target in
`M1_COSET_STRATEGY_SOL.md:82-87,470-483`; CONJECTURAL TARGET marked
Lean-formalizable. -/
theorem red_add_int_mul (cc dd : ℝ) (n : ℤ) (hcc : 0 < cc) :
    red cc (dd + (n : ℝ) * cc) = red cc dd := by
  have h : (dd + (n : ℝ) * cc) / cc = dd / cc + n := by field_simp
  simp only [red, h, Int.floor_add_intCast, Int.cast_add]
  ring

/-- The normalized `(c,d mod c)` key is invariant under both parabolic
translations, provided the PSL sign has been chosen so `c>0`.

Source/status: this is only the exact matrix/arithmetic sub-obligation of
M1-W in `M1_COSET_STRATEGY_SOL.md:284-305`; §6 (`:470-483`) marks it a
CONJECTURAL TARGET and Lean-formalizable.  It does not prove representative
independence for arbitrary raw words, endpoint ties, or key completeness. -/
theorem bottomRowKey_doubleTranslation (lam : ℝ) (w : List ℤ) (u v : ℤ)
    (hc : 0 < c lam w) :
    bottomRowKey (Spow u * wordMatrix lam w * Spow v) =
      bottomRowKey (wordMatrix lam w) := by
  obtain ⟨h0, h1⟩ := doubleTranslation_bottomRow lam w u v
  simp only [c, d] at h0 h1 hc
  simp only [bottomRowKey, h0, h1, red_add_int_mul _ _ v hc]

end RateCoreIII
