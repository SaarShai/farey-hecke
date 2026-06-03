import Mathlib
/-!
# Goal H — the ROTATION skeleton of the sub-threshold dynamics (ALL q, parametric in `l = λ`)

For `q ≥ 16` the per-branch scalar reduction is FALSE (middle branches carry `P < 1/l³`), so the
genuine lower bound `X_Ω(q) ≥ 1/l³` is multi-branch.  The numerically-discovered mechanism is that
the *sustained* low-`P` runs are governed by an ELLIPTIC monodromy conjugate to the fundamental
rotation `R = [[l,-1],[1,0]]` (trace `l = 2cos(π/q)`, rotation by `π/q`), NOT a fixed orbit.  The
cusp word (parabolic, trace `2`) is the unique infimum realizer; everything else rotates and the
product `P` oscillates back above `1/l³` within `O(q)` steps.

This file machine-checks the EXACT ALGEBRAIC SKELETON of that mechanism, for every `q ≥ 5`
(parametric in `l`), using only the universal boundary Chebyshev values
`x_{q-1}=0, x_{q-2}=1, x_{q-3}=l, x_{q-4}=l²-1`, hence the q-independent top-branch generators

  `A k = M_{q-1,k} = [[0,1],[-1,k·l]]`   (scalar branch, digit `k`)
  `B   = M_{q-3,0} = [[l,l²-1],[1,l]]`   (branch `q-3`)
  `Cc  = M_{q-2,0} = [[1,l],[0,1]]`      (cusp branch — parabolic, realizes `1/l³`)
  `Rr  = [[l,-1],[1,0]]`                 (fundamental rotation; companion of the Chebyshev rec.)

RESULTS (all `ring`, valid for every real `l`):
1. `det_Wq`, `trace_Wq` : the observed sustained word `W_q = (q-1,3)(q-1,0)(q-3,0)` has
   `det = 1`, `trace = l`  ⇒ it is SL₂ with the SAME trace as the fundamental rotation `Rr`
   ⇒ **elliptic, conjugate to a rotation by `π/q`** (NOT parabolic) for every `q ≥ 5`.
2. `trace_family` : the whole family `(q-1,k)(q-1,0)(q-3,0)` has `trace = l·(k-2)`.  With
   `0 < l < 2` this is `|trace| < 2` (ELLIPTIC, a sustainable rotation) **iff `k ∈ {1,2,3}`**, and
   `|trace| > 2` (HYPERBOLIC ⇒ the orbit escapes) for `k = 0` or `k ≥ 4`.  This is the clean
   elliptic-vs-hyperbolic dichotomy that bounds the sustained-run length.
3. `trace_cusp = 2`, `det_cusp = 1` : the cusp word is the parabolic extremal (the realizer).
4. `trace_secondParabolic = 2` : the 2-letter word `(q-1,1)(q-3,0)` is a SECOND parabolic word
   (trace exactly `2`); numerically it also realizes `1/l³` (never below).
5. `Wq_preserves_ellipse` : `W_q`'s monodromy `[[-l,2l²+1],[-1,2l]]` preserves the positive-definite
   quadratic form `Q'(a,b) = a² - 3l·a·b + (2l²+1)·b²` (its invariant ellipse), the exact sense in
   which the renormalized state ROTATES.  Positive-definiteness (`0<l<2`) is `Qp_posdef`.

Together: the sustained sub-threshold dynamics is a rotation on an invariant ellipse — the
transience handle made exact.  (The remaining analytic step — "rotation ⇒ `P` exceeds `1/l³`
within `O(q)` steps, with the domain constraint forcing the ellipse large enough" — is the honest
open crux; see `FINDINGS_goalH_2026-06-03.md`.)

`#print axioms` on every proved theorem is `[propext, Classical.choice, Quot.sound]`.
-/
namespace HeckeRotation

/-- A 2×2 real matrix `[[a,b],[c,d]]`. -/
structure M2 where
  a : ℝ
  b : ℝ
  c : ℝ
  d : ℝ

@[ext] theorem M2.ext {X Y : M2}
    (ha : X.a = Y.a) (hb : X.b = Y.b) (hc : X.c = Y.c) (hd : X.d = Y.d) : X = Y := by
  cases X; cases Y; simp_all

/-- Matrix product (standard, `X·Y`). -/
def mul (X Y : M2) : M2 :=
  ⟨X.a * Y.a + X.b * Y.c, X.a * Y.b + X.b * Y.d,
   X.c * Y.a + X.d * Y.c, X.c * Y.b + X.d * Y.d⟩

def tr  (X : M2) : ℝ := X.a + X.d
def det (X : M2) : ℝ := X.a * X.d - X.b * X.c

variable (l : ℝ)

/-- Scalar branch generator `M_{q-1,k} = [[0,1],[-1,k l]]`. -/
def A (k : ℝ) : M2 := ⟨0, 1, -1, k * l⟩
/-- Branch `q-3` generator `M_{q-3,0} = [[l,l²-1],[1,l]]`. -/
def B : M2 := ⟨l, l ^ 2 - 1, 1, l⟩
/-- Cusp branch generator `M_{q-2,0} = [[1,l],[0,1]]` (parabolic realizer). -/
def Cc : M2 := ⟨1, l, 0, 1⟩
/-- Fundamental rotation `R = [[l,-1],[1,0]]` (Chebyshev companion; trace `l`). -/
def Rr : M2 := ⟨l, -1, 1, 0⟩

/-- Monodromy of the sustained word `W_q = (q-1,3)(q-1,0)(q-3,0)`:
    `M = B · A0 · A3`. -/
def Wq : M2 := mul (mul (B l) (A l 0)) (A l 3)

/-- `W_q` is unimodular. -/
theorem det_Wq : det (Wq l) = 1 := by
  simp only [Wq, mul, det, A, B]; ring

/-- **`W_q` has trace `l`** — the same trace as the fundamental rotation `Rr`, hence ELLIPTIC
    (conjugate to a rotation by `π/q`) for every Hecke `l = 2cos(π/q) ∈ (1,2)`. -/
theorem trace_Wq : tr (Wq l) = l := by
  simp only [Wq, mul, tr, A, B]; ring

/-- Explicit entries of `W_q`'s monodromy: `[[-l, 2l²+1],[-1, 2l]]`. -/
theorem Wq_entries : Wq l = ⟨-l, 2 * l ^ 2 + 1, -1, 2 * l⟩ := by
  simp only [Wq, mul, A, B]; ext <;> ring

/-- **Trace law of the family** `(q-1,k)(q-1,0)(q-3,0)`: `trace = l·(k-2)`.
    For `0 < l < 2`: ELLIPTIC (`|trace|<2`, sustainable rotation) iff `k ∈ {1,2,3}`;
    HYPERBOLIC (`|trace|>2`, escapes) for `k = 0` or `k ≥ 4`. -/
theorem trace_family (k : ℝ) :
    tr (mul (mul (B l) (A l 0)) (A l k)) = l * (k - 2) := by
  simp only [mul, tr, A, B]; ring

/-- The fundamental rotation `Rr` has trace `l` and det `1`. -/
theorem trace_Rr : tr (Rr l) = l := by simp only [Rr, tr]; ring
theorem det_Rr : det (Rr l) = 1 := by simp only [Rr, det]; ring

/-- The cusp word is parabolic: trace `2`, det `1` (the infimum realizer). -/
theorem trace_cusp : tr (Cc l) = 2 := by simp only [Cc, tr]; ring
theorem det_cusp : det (Cc l) = 1 := by simp only [Cc, det]; ring

/-- A SECOND parabolic word `(q-1,1)(q-3,0)` also has trace exactly `2`.  (It is parabolic but
    does NOT realize the infimum: its scale-family value is `≈ 0.50 ≫ 1/l³`, and it is infeasible
    at some q, e.g. empty scale window at q=20.  Only the cusp word `Cc` realizes `1/l³`.) -/
theorem trace_secondParabolic : tr (mul (B l) (A l 1)) = 2 := by
  simp only [mul, tr, A, B]; ring

/-- The invariant quadratic form (ellipse) of `W_q`'s monodromy. -/
def Qp (a b : ℝ) : ℝ := a ^ 2 - 3 * l * (a * b) + (2 * l ^ 2 + 1) * b ^ 2

/-- **`W_q` preserves its invariant ellipse `Q'`.** Applying the monodromy
    `[[-l,2l²+1],[-1,2l]]` leaves `Q'` unchanged — the exact sense in which the renormalized
    state ROTATES on a fixed ellipse (the transience mechanism). -/
theorem Wq_preserves_ellipse (a b : ℝ) :
    Qp l ((-l) * a + (2 * l ^ 2 + 1) * b) ((-1) * a + (2 * l) * b) = Qp l a b := by
  simp only [Qp]; ring

/-- The invariant ellipse is positive-definite for `0 < l < 2` (genuinely an ellipse): its
    discriminant `(3l)² - 4(2l²+1) = l² - 4 < 0`.  Concretely `Q'(a,b) > 0` unless `a=b=0`. -/
theorem Qp_posdef (hl0 : 0 < l) (hl2 : l < 2) (a b : ℝ) (hab : a ≠ 0 ∨ b ≠ 0) :
    0 < Qp l a b := by
  have hb := sq_nonneg b
  -- 4·Q' = (2a - 3l b)² + (4 - l²)·b² ,  with 4 - l² > 0
  have h4 : 4 * Qp l a b = (2 * a - 3 * l * b) ^ 2 + (4 - l ^ 2) * b ^ 2 := by
    simp only [Qp]; ring
  have hpos : 0 < 4 - l ^ 2 := by nlinarith [hl0, hl2]
  rcases hab with ha | hb0
  · -- a ≠ 0
    rcases eq_or_ne b 0 with hbz | hbz
    · subst hbz; have : (0:ℝ) < a ^ 2 := by positivity
      nlinarith [h4, this]
    · nlinarith [h4, sq_nonneg (2 * a - 3 * l * b), mul_pos hpos (by positivity : (0:ℝ) < b ^ 2)]
  · -- b ≠ 0
    nlinarith [h4, sq_nonneg (2 * a - 3 * l * b), mul_pos hpos (by positivity : (0:ℝ) < b ^ 2)]

/-! ### Quantitative core of (L1): the product-oscillation range on the rotation ellipse.

On the rotation-invariant ellipse `E = c² + c'² − l·c·c'` (preserved by the fundamental rotation `R`
and, via conjugacy, by every elliptic sub-threshold regime), the product `c·c'` oscillates in the
EXACT range `[−E/(2+l), E/(2−l)]` — both endpoints tight (at `c=∓c'`).  As the orbit rotates it
sweeps this whole range; the maximum `E/(2−l)` is what eventually exceeds `1/l³` and ends the run.
Both bounds are trivial squares (`(c∓c')² ≥ 0`), valid for every `l ∈ (-2,2)`, i.e. all q. -/

/-- **Upper oscillation bound.** On the ellipse `E = c²+c'²−l·c c'` (any `l<2`): `c·c' ≤ E/(2−l)`,
    tight at `c=c'`.  (`E − c c'(2−l) = (c−c')² ≥ 0`.) -/
theorem product_le_on_ellipse (c c' E : ℝ) (hl2 : l < 2)
    (hE : c ^ 2 + c' ^ 2 - l * (c * c') = E) : c * c' ≤ E / (2 - l) := by
  have h2l : (0:ℝ) < 2 - l := by linarith
  rw [le_div_iff₀ h2l]; nlinarith [sq_nonneg (c - c'), hE]

/-- **Lower oscillation bound.** On the ellipse `E = c²+c'²−l·c c'` (any `l>−2`):
    `−E/(2+l) ≤ c·c'`, tight at `c=−c'`.  (`E + c c'(2+l) = (c+c')² ≥ 0`.) -/
theorem product_ge_on_ellipse (c c' E : ℝ) (hl : -2 < l)
    (hE : c ^ 2 + c' ^ 2 - l * (c * c') = E) : (-E) / (2 + l) ≤ c * c' := by
  have h2l : (0:ℝ) < 2 + l := by linarith
  rw [div_le_iff₀ h2l]; nlinarith [sq_nonneg (c + c'), hE]

#print axioms det_Wq
#print axioms trace_Wq
#print axioms Wq_entries
#print axioms trace_family
#print axioms trace_cusp
#print axioms trace_secondParabolic
#print axioms Wq_preserves_ellipse
#print axioms Qp_posdef
#print axioms product_le_on_ellipse
#print axioms product_ge_on_ellipse

end HeckeRotation
