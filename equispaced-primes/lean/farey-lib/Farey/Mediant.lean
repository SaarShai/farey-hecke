import Mathlib

/-!
# Mediants and unimodular neighbours

This file develops the elementary algebra underlying **Farey sequences** and the
**Stern–Brocot tree**: the *mediant* of two fractions `a/b`, `c/d` is `(a+c)/(b+d)`, and
two fractions are *unimodular neighbours* when `b*c - a*d = 1`.

These are the foundational facts on which the Farey-sequence neighbour theorem and the
Stern–Brocot construction rest. None of this is currently in Mathlib.

## Main results

* `Farey.det_mediant_left`, `Farey.det_mediant_right`: inserting the mediant preserves the
  determinant on each side.
* `Farey.Unimodular.mediant_left`, `Farey.Unimodular.mediant_right`: the mediant of a
  unimodular pair is a unimodular neighbour of each parent.
* `Farey.Unimodular.isCoprime_mediant`: the mediant of a unimodular pair is already in
  lowest terms.
* `Farey.mediant_strictAnti_left`, `Farey.mediant_strictMono_right`: for positive
  denominators the mediant lies strictly between the two fractions (cross-multiplied form).

## References

The Stern–Brocot tree and Farey sequences; see e.g. Graham–Knuth–Patashnik,
*Concrete Mathematics*, §4.5.
-/

namespace Farey

variable {a b c d : ℤ}

/-- The determinant `b*c - a*d` of the ordered pair of fractions `a/b`, `c/d`. It equals `+1`
for unimodular (Farey/Stern–Brocot) neighbours and is positive exactly when `a/b < c/d`
(for positive denominators). -/
def det (a b c d : ℤ) : ℤ := b * c - a * d

/-- Two fractions `a/b`, `c/d` are **unimodular neighbours** when `b*c - a*d = 1`. This is the
defining adjacency relation of the Farey sequence and the Stern–Brocot tree. -/
def Unimodular (a b c d : ℤ) : Prop := det a b c d = 1

@[simp] lemma det_def (a b c d : ℤ) : det a b c d = b * c - a * d := rfl

/-- Inserting the mediant `(a+c)/(b+d)` to the right of `a/b` leaves the determinant unchanged. -/
lemma det_mediant_left (a b c d : ℤ) : det a b (a + c) (b + d) = det a b c d := by
  simp only [det_def]; ring

/-- Inserting the mediant `(a+c)/(b+d)` to the left of `c/d` leaves the determinant unchanged. -/
lemma det_mediant_right (a b c d : ℤ) : det (a + c) (b + d) c d = det a b c d := by
  simp only [det_def]; ring

/-- The mediant of a unimodular pair is a unimodular neighbour of the left parent. -/
lemma Unimodular.mediant_left (h : Unimodular a b c d) : Unimodular a b (a + c) (b + d) := by
  unfold Unimodular at h ⊢; rw [det_mediant_left]; exact h

/-- The mediant of a unimodular pair is a unimodular neighbour of the right parent. -/
lemma Unimodular.mediant_right (h : Unimodular a b c d) : Unimodular (a + c) (b + d) c d := by
  unfold Unimodular at h ⊢; rw [det_mediant_right]; exact h

/-- **The mediant of a unimodular pair is in lowest terms.** This is why every fraction produced
by Stern–Brocot mediant insertion is automatically reduced. The witness comes from
`c*(b+d) - d*(a+c) = b*c - a*d = 1`. -/
lemma Unimodular.isCoprime_mediant (h : Unimodular a b c d) : IsCoprime (a + c) (b + d) :=
  ⟨-d, c, by unfold Unimodular det at h; linear_combination h⟩

/-- For positive denominators, `a/b < c/d` (cross-multiplied) implies `a/b` is strictly below its
mediant with `c/d`, in cross-multiplied form: `a*(b+d) < (a+c)*b`. -/
lemma mediant_strictAnti_left (h : a * d < c * b) : a * (b + d) < (a + c) * b := by
  nlinarith [h]

/-- For positive denominators, `a/b < c/d` (cross-multiplied) implies the mediant is strictly
below `c/d`, in cross-multiplied form: `(a+c)*d < c*(b+d)`. -/
lemma mediant_strictMono_right (h : a * d < c * b) : (a + c) * d < c * (b + d) := by
  nlinarith [h]

/-- A unimodular pair is strictly ordered in cross-multiplied form: `a*d < c*b` (which is
`a/b < c/d` once the denominators are positive). This needs only `det = 1`, not positivity. -/
lemma Unimodular.ad_lt_cb (h : Unimodular a b c d) : a * d < c * b := by
  unfold Unimodular det at h; linarith [h]

/-! ## Farey / Stern–Brocot chains

A **Farey chain** is a list of fractions (as `(numerator, denominator)` pairs) whose consecutive
entries are unimodular neighbours. Because unimodularity forces strict order
(`Unimodular.ad_lt_cb`), a Farey chain is automatically strictly increasing. The Farey sequence
`F_n` is a Farey chain, and the Stern–Brocot construction extends Farey chains by *mediant
insertion*; the key invariant is that mediant insertion preserves the chain (proved below).
-/

/-- A fraction as a `(numerator, denominator)` pair. -/
abbrev Frac := ℤ × ℤ

/-- The mediant `(a+c, b+d)` of fractions `p = (a,b)` and `q = (c,d)`. -/
def medFrac (p q : Frac) : Frac := (p.1 + q.1, p.2 + q.2)

/-- The unimodular-neighbour relation on fractions: `Adj (a,b) (c,d) ↔ b*c - a*d = 1`. -/
def Adj (p q : Frac) : Prop := Unimodular p.1 p.2 q.1 q.2

/-- Mediant insertion makes the mediant a unimodular neighbour of the left parent. -/
lemma Adj.medFrac_left {p q : Frac} (h : Adj p q) : Adj p (medFrac p q) :=
  Unimodular.mediant_left h

/-- Mediant insertion makes the mediant a unimodular neighbour of the right parent. -/
lemma Adj.medFrac_right {p q : Frac} (h : Adj p q) : Adj (medFrac p q) q :=
  Unimodular.mediant_right h

/-- Farey-chain neighbours are strictly increasing (cross-multiplied): `a*d < c*b`. So a Farey
chain is sorted. -/
lemma Adj.lt {p q : Frac} (h : Adj p q) : p.1 * q.2 < q.1 * p.2 :=
  Unimodular.ad_lt_cb h

/-- A **Farey chain**: a list of fractions whose consecutive entries are unimodular neighbours. -/
def IsFareyChain (l : List Frac) : Prop := l.IsChain Adj

/-- The base Farey chain `[0/1, 1/1]`. -/
lemma isFareyChain_base : IsFareyChain [((0 : ℤ), (1 : ℤ)), ((1 : ℤ), (1 : ℤ))] := by
  unfold IsFareyChain
  rw [List.isChain_pair]
  simp only [Adj, Unimodular, det]; norm_num

/-- **Mediant insertion preserves the Farey-chain property.** Given a Farey chain beginning
`p :: q :: l`, inserting the mediant of the first two entries yields the Farey chain
`p :: medFrac p q :: q :: l`. This is the inductive step of the Stern–Brocot construction of the
Farey sequence, and the source of the Farey neighbour theorem (consecutive Farey fractions are
unimodular). -/
lemma isFareyChain_insert_mediant {p q : Frac} {l : List Frac}
    (h : IsFareyChain (p :: q :: l)) :
    IsFareyChain (p :: medFrac p q :: q :: l) := by
  unfold IsFareyChain at h ⊢
  rw [List.isChain_cons_cons] at h
  obtain ⟨hpq, hrest⟩ := h
  rw [List.isChain_cons_cons, List.isChain_cons_cons]
  exact ⟨hpq.medFrac_left, hpq.medFrac_right, hrest⟩

/-! ## The denominator bound: Farey neighbours are spread out

The key quantitative fact behind the Farey neighbour theorem and the Stern–Brocot tree: between
two unimodular neighbours `a/b < c/d`, every intermediate fraction `p/q` has denominator
`q ≥ b + d`. Since the mediant achieves `q = b + d` and is reduced (`Unimodular.isCoprime_mediant`),
**the mediant is the unique simplest fraction strictly between two unimodular neighbours.**
-/

/-- **Between unimodular neighbours, every intermediate fraction has denominator `≥ b + d`.**
If `b*c - a*d = 1` (with `b, d > 0`) and `a/b < p/q < c/d` (cross-multiplied), then `b + d ≤ q`.
The one-line identity `q = d*(b*p - a*q) + b*(c*q - d*p)` (valid because `b*c - a*d = 1`) makes both
summands `≥ d` and `≥ b` respectively. -/
lemma Unimodular.den_ge_of_strictBetween {p q : ℤ} (h : Unimodular a b c d)
    (hb : 0 < b) (hd : 0 < d) (h1 : a * q < p * b) (h2 : p * d < c * q) : b + d ≤ q := by
  unfold Unimodular det at h
  have e1 : (1 : ℤ) ≤ p * b - a * q := by omega
  have e2 : (1 : ℤ) ≤ c * q - p * d := by omega
  have key : d * (p * b - a * q) + b * (c * q - p * d) = q := by
    have hexp : d * (p * b - a * q) + b * (c * q - p * d) = q * (b * c - a * d) := by ring
    rw [hexp, h, mul_one]
  nlinarith [mul_nonneg hd.le (by omega : (0 : ℤ) ≤ p * b - a * q - 1),
             mul_nonneg hb.le (by omega : (0 : ℤ) ≤ c * q - p * d - 1), key]

/-- **Adjacency criterion (sufficient direction).** If `a/b, c/d` are unimodular neighbours with
`n < b + d`, then *no* fraction `p/q` with `0 < q ≤ n` lies strictly between them — i.e. they are
adjacent in the Farey sequence `F_n`. (Immediate from `den_ge_of_strictBetween`.) -/
lemma Unimodular.not_strictBetween_of_den_le {p q n : ℤ} (h : Unimodular a b c d)
    (hb : 0 < b) (hd : 0 < d) (hqn : q ≤ n) (hn : n < b + d)
    (h1 : a * q < p * b) (h2 : p * d < c * q) : False := by
  have := h.den_ge_of_strictBetween hb hd h1 h2
  omega

/-! ## The Farey gap formula (in ℚ)

Two unimodular neighbours, viewed as rationals, differ by exactly `1/(b*d)`. This is the classical
fact that consecutive Farey fractions `a/b < c/d` satisfy `c/d - a/b = 1/(b*d)`.
-/

/-- **Farey gap formula.** Unimodular neighbours `a/b < c/d` (with `b, d > 0`) differ by exactly
`1/(b*d)` in `ℚ`. -/
lemma Unimodular.rat_sub (h : Unimodular a b c d) (hb : 0 < b) (hd : 0 < d) :
    (c : ℚ) / d - (a : ℚ) / b = 1 / ((b : ℚ) * d) := by
  have hb0 : (b : ℚ) ≠ 0 := Int.cast_ne_zero.mpr hb.ne'
  have hd0 : (d : ℚ) ≠ 0 := Int.cast_ne_zero.mpr hd.ne'
  have h' : (b : ℚ) * c - a * d = 1 := by unfold Unimodular det at h; exact_mod_cast h
  rw [div_sub_div _ _ hd0 hb0, div_eq_div_iff (mul_ne_zero hd0 hb0) (mul_ne_zero hb0 hd0)]
  linear_combination (b : ℚ) * d * h'

end Farey
