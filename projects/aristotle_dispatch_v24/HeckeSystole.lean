import Mathlib

/-!
# U2b Hecke-systole anchor: finite-algebra obligations (v24 dispatch)

Source: `research_notes/rh_goals_2026-08-14/lane_g/LAW_U2B_CLOSURE.md` §6,
Aristotle-able items **A1, A2, A3, A6**. Each statement below is finite/algebraic
— a Chebyshev-recursion matrix identity, a nonnegative-matrix trace-path
inequality, a systole case-analysis given A1+A2 (stated over a fixed finite
alphabet), and an explicit real-polynomial non-monotonicity witness — matching
the note's own scoping.

Skipped: **A5** (the `t cot t` strict antitonicity lemma, Theorem U2b-B's
engine) and **A4** (`W_q` antitone in `q`, which depends on A5). Both are
genuine analysis (derivative/limit arguments over `(0, π)` and an infinite
family indexed by `q`), not finite algebra — recorded in `SKIPPED.md`.
-/

open Matrix

/-! ## A1 (§6, "the Chebyshev normal form"). The load-bearing algebra:
`S R^a = -M_a`, `det M_a = 1`, via the Chebyshev-type recursion
`u_0 = 0, u_1 = 1, u_{n+2} = lam * u_{n+1} - u_n`. -/

variable {R : Type*} [CommRing R]

/-- Chebyshev-type sequence `u_j(lam)` attached to the recursion
`R^2 = lam R - 1`. -/
def u (lam : R) : ℕ → R
  | 0 => 0
  | 1 => 1
  | (n + 2) => lam * u lam (n + 1) - u lam n

/-- `S = [[0,-1],[1,0]]`. -/
def Smat : Matrix (Fin 2) (Fin 2) R := !![0, -1; 1, 0]

/-- `R = [[0,-1],[1,lam]]`. -/
def Rmat (lam : R) : Matrix (Fin 2) (Fin 2) R := !![0, -1; 1, lam]

/-- `M_a := [[u_a, u_{a+1}],[u_{a-1}, u_a]]` (indices `a ≥ 1`; `u_{a-1}` uses
`ℕ`-truncated subtraction, valid since `a ≥ 1`). -/
def Mmat (lam : R) (a : ℕ) : Matrix (Fin 2) (Fin 2) R :=
  !![u lam a, u lam (a + 1); u lam (a - 1), u lam a]

/-- `R^2 = lam • R - 1`, the defining relation of the recursion. -/
theorem Rmat_sq (lam : R) : Rmat lam ^ 2 = lam • Rmat lam - 1 := by
  sorry

/-- `R^a = u_a • R - u_{a-1} • 1` for `a ≥ 1`, by induction on the recursion. -/
theorem Rmat_pow (lam : R) (a : ℕ) (ha : 1 ≤ a) :
    Rmat lam ^ a = u lam a • Rmat lam - u lam (a - 1) • (1 : Matrix (Fin 2) (Fin 2) R) := by
  sorry

/-- `S * R^a = -M_a` for `a ≥ 1`. -/
theorem SR_pow (lam : R) (a : ℕ) (ha : 1 ≤ a) :
    Smat * Rmat lam ^ a = - Mmat lam a := by
  sorry

/-- `det M_a = 1` for `a ≥ 1`, the Chebyshev identity `u_a^2 - u_{a+1} u_{a-1} = 1`. -/
theorem det_Mmat (lam : R) (a : ℕ) (ha : 1 ≤ a) :
    (Mmat lam a).det = 1 := by
  sorry

/-! ## A2 (§6, "the trace-path expansion is a sum of nonnegative terms"). A
finite product of entrywise-nonnegative `2×2` matrices has trace bounded below
by the sum of the two diagonal-path products, and more generally by any single
cyclic state-path product. -/

/-- The trace of a finite product of entrywise-nonnegative `2×2` real matrices
is nonnegative. -/
theorem trace_prod_nonneg {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ i p q, 0 ≤ A i p q) : 0 ≤ Matrix.trace (∏ i, A i) := by
  sorry

/-- The two constant diagonal paths (`i ≡ 0` and `i ≡ 1`) lower-bound the trace
of a product of entrywise-nonnegative `2×2` matrices. -/
theorem trace_ge_diag {n : ℕ} (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ i p q, 0 ≤ A i p q) :
    (∏ i, A i 0 0) + (∏ i, A i 1 1) ≤ Matrix.trace (∏ i, A i) := by
  sorry

/-- More generally, every cyclic state-path product lower-bounds the trace of a
product of entrywise-nonnegative `2×2` matrices (`n > 0`; the path is a
function `ZMod n → Fin 2` closing up cyclically). -/
theorem trace_ge_path {n : ℕ} (hn : 0 < n) (A : Fin n → Matrix (Fin 2) (Fin 2) ℝ)
    (hA : ∀ i p q, 0 ≤ A i p q) (i : ZMod n → Fin 2) :
    (∏ k : Fin n, A k (i k) (i (k + 1))) ≤ Matrix.trace (∏ k, A k) := by
  sorry

/-! ## A3 (§6, "the systole theorem, given A1 + A2"). Stated over a FIXED
finite level `q` and a fixed finite word length `m`, so the statement is a
concrete finite claim about real numbers (`lam_q := 2 * Real.cos (π / q)`), not
a scheme quantified over all `q`. -/

/-- `lam_q := 2 cos(pi/q)`. -/
noncomputable def lamQ (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)

/-- For a fixed level `q ≥ 4` and a fixed word length `m ≥ 1`, every hyperbolic
cyclically reduced word `S R^{a_1} ... S R^{a_m}` with letters `a_i ∈ [1, q-1]`
has `|tr w| ≥ 2 * lam_q`. The word is represented by its letters `a : Fin m →
ℕ` and its trace by the real number `t`, related by the (already-established,
A1-level) fact that `t = tr(∏ Mmat (lamQ q) (a i))` up to sign — taken here as
a hypothesis `htr` so the statement isolates the systole inequality itself. -/
theorem systole_trace_bound (q m : ℕ) (hq : 4 ≤ q) (hm : 1 ≤ m)
    (a : Fin m → ℕ) (ha : ∀ i, 1 ≤ a i ∧ a i ≤ q - 1)
    (t : ℝ) (htr : t = Matrix.trace (∏ i : Fin m, Mmat (lamQ q) (a i)))
    (hhyp : 2 < |t|) :
    2 * lamQ q ≤ |t| := by
  sorry

/-! ## A6 (§6, "the counterexample, worth banking as a decide-style fact"). The
literal statement of `Conjecture U1-2` — `|tr S R^5| = 2|u_5(lam)|` nondecreasing
on `(1,2]` — is false: `u_5(lam) = lam^4 - 3 lam^2 + 1` is non-monotone, witnessed
by the explicit triple `lam = 1, 1.2434, sqrt 2` from `LAW_U2B_CLOSURE.md` §3.2. -/

/-- `u_5(lam) = lam^4 - 3 lam^2 + 1` fails to be monotone on `(1, 2]`: it rises
from `lam = 1` to `lam = 1.2434` and falls back by `lam = sqrt 2`. -/
theorem u5_not_monotone :
    ¬ MonotoneOn (fun lam : ℝ => 2 * (lam ^ 4 - 3 * lam ^ 2 + 1)) (Set.Ioc (1 : ℝ) 2) := by
  sorry

/-- The explicit witness inequality triple: at `lam = 1`, `|2 u_5| = 2`; at
`lam = 1.2434`, `|2 u_5| > 2.49`; at `lam = sqrt 2`, `|2 u_5| = 2`. This pins
down the rise-then-fall shape used by `u5_not_monotone`. -/
theorem u5_witness_triple :
    |2 * ((1 : ℝ) ^ 4 - 3 * 1 ^ 2 + 1)| = 2 ∧
    2.49 < |2 * ((1.2434 : ℝ) ^ 4 - 3 * 1.2434 ^ 2 + 1)| ∧
    |2 * ((Real.sqrt 2) ^ 4 - 3 * (Real.sqrt 2) ^ 2 + 1)| = 2 := by
  sorry
