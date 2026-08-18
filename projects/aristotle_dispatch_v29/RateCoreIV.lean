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

/-- The lower-left entry is `lam` times the negative continuant.

Source/status: `M2_LOCALIZATION_THEOREM_SOL.md:484-501` and
`M1_LOCALIZATION_TRIPLE_REFEREE.md:229-242`; REFEREE-CONFIRMED algebraic
identity, Lean target OPEN in this dispatch. -/
theorem c_eq_lam_mul_continuant (lam : ℝ) (w : List ℤ) :
    c lam w = lam * continuant lam w := by
  sorry

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
  sorry

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
  sorry

/-! ## 2. Sharp finite no-wrap law -/

/-- Sharp finite no-wrap lower envelope for every syntactically reduced raw
word of `Q`-depth `k <= N-1`.

Source/status: `M2_LOCALIZATION_THEOREM_SOL.md:484-578`, with the omitted
ordering repaired at lines 556-568; `M1_LOCALIZATION_TRIPLE_REFEREE.md:223-280`
adjudicates the theorem TRUE after that repair.  PAPER/REFEREE CONFIRMED;
Lean target OPEN.  This is not an unrestricted-depth or global localization
statement. -/
theorem sharp_no_wrap
    (N k : ℕ) (hN : 3 ≤ N) (w : List ℤ)
    (hred : SyntacticallyReduced w) (hdepth : depth w = k)
    (hk0 : 1 ≤ k) (hkN : k ≤ N - 1) :
    |c (lamN N) w| ≥
      lamN N *
        (Real.sin ((k : ℝ) * Real.pi / (N : ℝ)) /
          Real.sin (Real.pi / (N : ℝ))) := by
  sorry

/-! ## 3. Equality at the two constant-sign Chebyshev words -/

/-- The all-`+1` word of depth `m`, copied exactly from v26. -/
def chebyshevWord (m : ℕ) : List ℤ := List.replicate (m - 1) (1 : ℤ)

/-- The all-`-1` word of depth `m`. -/
def negativeChebyshevWord (m : ℕ) : List ℤ :=
  List.replicate (m - 1) (-1 : ℤ)

/-- Local standalone copy of the v26 Chebyshev bridge
`c = lam * U_{m-1}(lam/2)`.

Source/status: harvested v26
`projects/aristotle_dispatch_v26/result/aristotle_dispatch_v26_aristotle/RateCore.lean:332-340`;
MACHINE-VERIFIED there by an independent sorry-free rebuild.  Re-dispatched
here only because v29 is a standalone `import Mathlib` file. -/
theorem c_chebyshevWord (m : ℕ) (hm : 1 ≤ m) (lam : ℝ) :
    c lam (chebyshevWord m) =
      lam * aeval (lam / 2) (Polynomial.Chebyshev.U ℝ ((m : ℤ) - 1)) := by
  sorry

/-- Referee-required signed form of the all-`-1` equality: the signed
lower-left entry differs from the all-`+1` entry by `(-1)^(m-1)`.  Equality in
the sharp envelope is therefore an equality of absolute values.

Source/status: `M2_LOCALIZATION_THEOREM_SOL.md:580-587` and
`M1_LOCALIZATION_TRIPLE_REFEREE.md:267-280`; REFEREE-CONFIRMED sign repair,
Lean target OPEN. -/
theorem c_negativeChebyshevWord_sign (m : ℕ) (hm : 1 ≤ m) (lam : ℝ) :
    c lam (negativeChebyshevWord m) =
      (-1 : ℝ) ^ (m - 1) * c lam (chebyshevWord m) := by
  sorry

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
  sorry

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
  sorry

/-- For `lamN N = 2 cos(pi/N)`, the `SL(2, R)` lift satisfies `R^N = -I`.
The associated PSL relation is `bar R^N = 1`; this theorem deliberately keeps
the lift sign visible and asserts no PSL presentation API.

Source/status: `M1_ROUTE_B_REPAIR_SOL.md:285-320`, with q=5,7 exact checks at
`M1_LOCALIZATION_TRIPLE_REFEREE.md:70-92`; ROUTE-B PAPER/REFEREE CONFIRMED,
Lean target OPEN. -/
theorem Rmat_pow_lamN_neg_one (N : ℕ) (hN : 3 ≤ N) :
    (Rmat (lamN N)) ^ N = -(1 : Matrix (Fin 2) (Fin 2) ℝ) := by
  sorry

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
  sorry

end RateCoreIV
