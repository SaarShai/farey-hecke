import Mathlib

/-!
# The Farey neighbour theorem

If `a/b < c/d` are reduced fractions with denominators in `[1, n]` and **no** fraction `x/y` with
`0 < y ≤ n` lies strictly between them (i.e. they are consecutive in the Farey sequence `F_n`), then
they are *unimodular neighbours*: `b*c - a*d = 1`. This is Hardy–Wright, *An Introduction to the
Theory of Numbers*, Theorem 28. It is currently absent from Mathlib.

The proof is the Bézout/lattice argument: pick a solution of `b*x - a*y = 1` with denominator
`y ∈ (n-b, n]`; adjacency forces `c/d ≤ x/y`; the determinant identity
`(b*c-a*d)·(y,x) = (d,c) - (d*x-c*y)·(b,a)` then splits into two cases, one impossible (`d > n`),
the other forcing `(b*c-a*d) ∣ gcd(c,d) = 1`.
-/

namespace Farey

/-- **Farey neighbour theorem (Hardy–Wright, Thm 28).** Consecutive Farey fractions are unimodular
neighbours. Here `hadj` is the consecutiveness hypothesis: no `x/y` with `0 < y ≤ n` lies strictly
between `a/b` and `c/d` (in cross-multiplied form). -/
theorem neighbour_unimodular {a b c d n : ℤ}
    (hb : 0 < b) (hbn : b ≤ n) (hdn : d ≤ n)
    (hab : IsCoprime a b) (hcd : IsCoprime c d)
    (hlt : a * d < c * b)
    (hadj : ∀ x y : ℤ, 0 < y → y ≤ n → a * y < x * b → ¬ (x * d < c * y)) :
    b * c - a * d = 1 := by
  have hmpos : 1 ≤ b * c - a * d := by
    have h2 : a * d < b * c := by linarith [hlt, mul_comm c b]
    omega
  -- Bézout solution of `b*x - a*y = 1` with denominator `y ∈ (n - b, n]`.
  obtain ⟨x, y, hbez, hylo, hyhi⟩ :
      ∃ x y : ℤ, b * x - a * y = 1 ∧ n - b < y ∧ y ≤ n := by
    obtain ⟨u, v, huv⟩ := hab
    have hQb : ((n + u) / b) * b = (n + u) - (n + u) % b := by
      have h := Int.mul_ediv_add_emod (n + u) b
      linarith [h, mul_comm b ((n + u) / b)]
    have hmod1 : 0 ≤ (n + u) % b := Int.emod_nonneg _ hb.ne'
    have hmod2 : (n + u) % b < b := Int.emod_lt_of_pos _ hb
    refine ⟨v + ((n + u) / b) * a, -u + ((n + u) / b) * b, by linear_combination huv, ?_, ?_⟩
    · rw [hQb]; linarith [hmod2]
    · rw [hQb]; linarith [hmod1]
  have hy0 : 0 < y := by omega
  have hax : a * y < x * b := by nlinarith [hbez]
  have hcle : c * y ≤ x * d := not_lt.mp (hadj x y hy0 hyhi hax)
  -- determinant identity: `(b*c-a*d)·(y,x) = (d,c) - (d*x-c*y)·(b,a)`
  have eqd : (b * c - a * d) * y = d - (d * x - c * y) * b := by linear_combination d * hbez
  have eqc : (b * c - a * d) * x = c - (d * x - c * y) * a := by linear_combination c * hbez
  have hm'0 : 0 ≤ d * x - c * y := by nlinarith [hcle]
  rcases eq_or_lt_of_le hm'0 with hm'eq | hm'pos
  · -- `d*x - c*y = 0`: then `(b*c-a*d) ∣ c` and `∣ d`, so it divides `gcd(c,d) = 1`.
    rw [← hm'eq, zero_mul, sub_zero] at eqd eqc
    have hunit : IsUnit (b * c - a * d) := hcd.isUnit_of_dvd' ⟨x, eqc.symm⟩ ⟨y, eqd.symm⟩
    rcases Int.isUnit_iff.mp hunit with h1 | h1
    · exact h1
    · omega
  · -- `d*x - c*y ≥ 1`: then `d = (b*c-a*d)*y + (d*x-c*y)*b ≥ y + b > n`, contradicting `d ≤ n`.
    exfalso
    have hp1 : (0 : ℤ) ≤ b * c - a * d - 1 := by linarith [hmpos]
    have hp2 : (0 : ℤ) ≤ d * x - c * y - 1 := by omega
    nlinarith [eqd, mul_nonneg hp1 hy0.le, mul_nonneg hp2 hb.le, hylo, hdn]

end Farey
