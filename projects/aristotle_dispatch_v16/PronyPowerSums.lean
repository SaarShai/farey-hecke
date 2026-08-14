import Mathlib

/-!
# Prony / power-sum uniqueness for multisets of nonzero complex numbers

Classical fact (Prony 1795 / Newton identities; infrastructure lemma, not a
novelty claim): a multiset of at most `d` NONZERO complex numbers is
determined by its first `2*d` power sums.

This is the anchor lemma for a sample-complexity program: for a curve over a
finite field, the point counts `#C(F_{q^k})` are (up to explicit known terms)
the power sums of the Frobenius eigenvalues, so `2g` counts determine the
L-polynomial. We formalize the pure power-sum statement over ℂ.

## Suggested proof route (rational generating function)

For a multiset `a` of nonzero complexes define
`G_a(x) = ∑_{α ∈ a} α/(1 - α x)` as a formal power series / rational
function. Its k-th Taylor coefficient at 0 is the power sum `s_{k+1}(a)`.
Given the hypothesis, `G_a - G_b` has Taylor coefficients 0 in degrees
`0 .. 2*d - 1`. Writing `G_a - G_b = P/Q` over the common denominator
`Q(x) = ∏_{α ∈ a}(1-αx) · ∏_{β ∈ b}(1-βx)` (degree ≤ card a + card b ≤ 2d),
the numerator `P` has degree ≤ card a + card b - 1 < 2*d, but vanishes to
order ≥ 2*d at 0, hence `P = 0`, hence `G_a = G_b`. Matching poles (all at
`1/α` with `α` nonzero) and their residues recovers the multisets with
multiplicity, giving `a = b`.

An alternative route: first deduce `card a = card b` (from the vanishing of
the numerator / or by comparing the rational functions at ∞), then apply
Newton's identities over a characteristic-zero field to identify the
elementary symmetric functions, hence the char polynomials, hence the
multisets. Use whichever route is most convenient in Mathlib.

Constraints: no new axioms, no `sorry` in the final artifact; `#print axioms`
of the main theorem must show only `[propext, Classical.choice, Quot.sound]`.
-/

open Multiset

/-- Power sum `s_k(a) = ∑_{α ∈ a} α ^ k` of a multiset of complex numbers. -/
noncomputable def powerSum (a : Multiset ℂ) (k : ℕ) : ℂ :=
  (a.map (· ^ k)).sum

/-- **Prony / power-sum uniqueness.** Two multisets of at most `d` nonzero
complex numbers whose power sums agree for `k = 1, …, 2*d` are equal. -/
theorem prony_power_sum_uniqueness (d : ℕ) (a b : Multiset ℂ)
    (ha : a.card ≤ d) (hb : b.card ≤ d)
    (h0a : (0 : ℂ) ∉ a) (h0b : (0 : ℂ) ∉ b)
    (h : ∀ k : ℕ, 1 ≤ k → k ≤ 2 * d → powerSum a k = powerSum b k) :
    a = b := by
  sorry

/-- Sharpness scaffold (OPTIONAL — prove only if it goes smoothly; the main
theorem above is the deliverable): with only `2*d - 1` matching power sums
the conclusion can fail. Witness for `d = 1`: `a = {1}`, `b = {-1}` share
`s_1`? No — `s_1` differs; a correct witness needs `d ≥ 2`, e.g. multisets
with matching `s_1..s_2` but different size. If no convenient witness is
found, SKIP this and deliver only the main theorem. -/
theorem prony_sharpness_placeholder : True := trivial
