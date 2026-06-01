import Mathlib

open Finset

namespace Farey

/-- The `q`-th **Farey level**: the reduced fractions `a/q` in `[0,1)` with denominator exactly
`q`, namely `a/q` for `0 ≤ a < q` with `gcd(q, a) = 1`. Its cardinality is `Nat.totient q`. -/
def fareyLevel (q : ℕ) : Finset ℚ :=
  ((range q).filter fun a => q.Coprime a).image fun a : ℕ => (a : ℚ) / q

/-- The **Farey sequence** `F n`: the reduced rationals in `[0,1]` with denominator at most `n`.
Built as the endpoint `1` together with the levels `fareyLevel q` for `1 ≤ q ≤ n` (which cover
`[0,1)`). For `n = 0` this degenerates to `{1}`; the intended object is for `n ≥ 1`. -/
def farey (n : ℕ) : Finset ℚ :=
  insert 1 ((Icc 1 n).biUnion fareyLevel)

/-- Each Farey level has cardinality `Nat.totient q`. -/
lemma card_fareyLevel (q : ℕ) (hq : 0 < q) : (fareyLevel q).card = q.totient := by
  have hinj : Set.InjOn (fun a : ℕ => (a : ℚ) / q)
      ↑((range q).filter fun a => q.Coprime a) := by
    intro a _ b _ hab
    dsimp only at hab
    have hq' : (q : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr hq.ne'
    rw [div_eq_div_iff hq' hq'] at hab
    exact_mod_cast mul_right_cancel₀ hq' hab
  unfold fareyLevel
  rw [card_image_of_injOn hinj]
  exact (Nat.totient_eq_card_coprime q).symm

/-- The denominator of an element of the `q`-th Farey level is exactly `q`. -/
lemma den_of_mem_fareyLevel {q : ℕ} {x : ℚ} (hx : x ∈ fareyLevel q) : x.den = q := by
  unfold fareyLevel at hx
  rw [mem_image] at hx
  obtain ⟨a, ha, rfl⟩ := hx
  rw [mem_filter, mem_range] at ha
  obtain ⟨haq, hcop⟩ := ha
  have hq : 0 < q := by omega
  have hb0 : (0 : ℤ) < (q : ℤ) := by exact_mod_cast hq
  have hcop' : Nat.Coprime ((a : ℤ).natAbs) ((q : ℤ).natAbs) := by
    simpa [Int.natAbs_natCast] using hcop.symm
  have h := Rat.den_div_eq_of_coprime hb0 hcop'
  have hbridge : ((a : ℚ) / (q : ℚ)) = (((a : ℤ) : ℚ) / ((q : ℤ) : ℚ)) := by push_cast; ring
  rw [hbridge]
  exact_mod_cast h

/-- Elements of any Farey level are `< 1`. -/
lemma mem_fareyLevel_lt_one {q : ℕ} {x : ℚ} (hx : x ∈ fareyLevel q) : x < 1 := by
  unfold fareyLevel at hx
  rw [mem_image] at hx
  obtain ⟨a, ha, rfl⟩ := hx
  rw [mem_filter, mem_range] at ha
  obtain ⟨haq, _⟩ := ha
  have hq : 0 < q := by omega
  rw [div_lt_one (by exact_mod_cast hq)]
  exact_mod_cast haq

/-- Elements of any Farey level are `≥ 0`. -/
lemma mem_fareyLevel_nonneg {q : ℕ} {x : ℚ} (hx : x ∈ fareyLevel q) : 0 ≤ x := by
  unfold fareyLevel at hx
  rw [mem_image] at hx
  obtain ⟨a, _, rfl⟩ := hx
  exact div_nonneg (Nat.cast_nonneg _) (Nat.cast_nonneg _)

/-- **The length of the Farey sequence.** `|F n| = 1 + ∑_{k=1}^n φ(k)`, where `φ` is Euler's
totient. (Hardy–Wright, *An Introduction to the Theory of Numbers*, Theorem 330.) -/
theorem card_farey (n : ℕ) : (farey n).card = 1 + ∑ q ∈ Icc 1 n, q.totient := by
  have h1 : (1 : ℚ) ∉ (Icc 1 n).biUnion fareyLevel := by
    rw [mem_biUnion]
    rintro ⟨q, _, hx⟩
    exact absurd (mem_fareyLevel_lt_one hx) (lt_irrefl 1)
  have hdisj : ((Icc 1 n : Finset ℕ) : Set ℕ).PairwiseDisjoint fareyLevel := by
    intro q _ q' _ hqq'
    show Disjoint (fareyLevel q) (fareyLevel q')
    rw [Finset.disjoint_left]
    intro x hxq hxq'
    exact hqq' ((den_of_mem_fareyLevel hxq).symm.trans (den_of_mem_fareyLevel hxq'))
  have hsum : ((Icc 1 n).biUnion fareyLevel).card = ∑ q ∈ Icc 1 n, q.totient := by
    rw [card_biUnion hdisj]
    exact Finset.sum_congr rfl fun q hq => card_fareyLevel q (mem_Icc.mp hq).1
  unfold farey
  rw [card_insert_of_notMem h1, hsum]
  omega

/-- Sanity check: `|F₁| = 2` (the fractions `0/1, 1/1`). -/
example : (farey 1).card = 2 := by rw [card_farey]; decide

/-- Sanity check: `|F₂| = 3` (the fractions `0/1, 1/2, 1/1`). -/
example : (farey 2).card = 3 := by rw [card_farey]; decide

/-- Sanity check: `|F₃| = 5` (the fractions `0/1, 1/3, 1/2, 2/3, 1/1`). -/
example : (farey 3).card = 5 := by rw [card_farey]; decide

end Farey
