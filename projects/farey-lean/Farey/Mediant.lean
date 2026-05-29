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

end Farey
