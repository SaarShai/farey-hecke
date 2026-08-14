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

## Proof route used here (Vandermonde / Lagrange-style separation)

Let `S` be the (finite) set of values occurring in `a` or `b`, and let
`c α = (count α a : ℂ) - (count α b)`. Since `S.card ≤ card a + card b ≤ 2*d`,
the hypothesis says `∑_{α ∈ S} c α * α ^ k = 0` for all `1 ≤ k ≤ S.card`.
Taking linear combinations, `∑_{α ∈ S} c α * α * p.eval α = 0` for every
polynomial `p` of degree `< S.card`. Applying this to the separating
polynomial `p = ∏_{γ ∈ S.erase β} (X - C γ)` isolates a single term and
gives `c β * β * ∏_{γ ≠ β} (β - γ) = 0`; as `β ≠ 0` and the values in `S`
are distinct, `c β = 0`. Hence all multiplicities agree and `a = b`.

Constraints: no new axioms, no `sorry` in the final artifact; `#print axioms`
of the main theorem must show only `[propext, Classical.choice, Quot.sound]`.
-/

open Multiset

/-- Power sum `s_k(a) = ∑_{α ∈ a} α ^ k` of a multiset of complex numbers. -/
noncomputable def powerSum (a : Multiset ℂ) (k : ℕ) : ℂ :=
  (a.map (· ^ k)).sum

namespace PronyAux

open Polynomial

/-- The separating polynomial `∏_{γ ∈ S.erase β} (X - C γ)`. -/
noncomputable def sep (S : Finset ℂ) (β : ℂ) : ℂ[X] :=
  ∏ γ ∈ S.erase β, (X - C γ)

lemma sep_natDegree (S : Finset ℂ) (β : ℂ) :
    (sep S β).natDegree = (S.erase β).card := by
  rw [sep, natDegree_prod_of_monic _ _ (fun γ _ => monic_X_sub_C γ)]
  simp

lemma sep_eval_ne (S : Finset ℂ) {β γ : ℂ} (hγ : γ ∈ S) (hne : γ ≠ β) :
    (sep S β).eval γ = 0 := by
  rw [sep, eval_prod]
  refine Finset.prod_eq_zero (i := γ) (Finset.mem_erase.2 ⟨hne, hγ⟩) ?_
  simp

lemma sep_eval_self_ne_zero (S : Finset ℂ) (β : ℂ) : (sep S β).eval β ≠ 0 := by
  rw [sep, eval_prod]
  refine Finset.prod_ne_zero_iff.2 fun γ hγ => ?_
  have : γ ≠ β := (Finset.mem_erase.1 hγ).1
  simp only [eval_sub, eval_X, eval_C]
  exact sub_ne_zero.2 (Ne.symm this)

/-- If `∑_{α ∈ S} c α * α ^ k = 0` for `1 ≤ k ≤ S.card`, then the same
combination against `α * p.eval α` vanishes, for any `p` of degree `< S.card`. -/
lemma sum_mul_eval_eq_zero (S : Finset ℂ) (c : ℂ → ℂ)
    (hvan : ∀ k : ℕ, 1 ≤ k → k ≤ S.card → ∑ α ∈ S, c α * α ^ k = 0)
    (p : ℂ[X]) (hp : p.natDegree < S.card) :
    ∑ α ∈ S, c α * α * p.eval α = 0 := by
  have hexp : ∀ α : ℂ, p.eval α = ∑ j ∈ Finset.range S.card, p.coeff j * α ^ j :=
    fun α => eval_eq_sum_range' hp α
  have step1 : ∑ α ∈ S, c α * α * p.eval α
      = ∑ α ∈ S, ∑ j ∈ Finset.range S.card, p.coeff j * (c α * α ^ (j + 1)) := by
    refine Finset.sum_congr rfl fun α _ => ?_
    rw [hexp α, Finset.mul_sum]
    exact Finset.sum_congr rfl fun j _ => by ring
  rw [step1, Finset.sum_comm]
  refine Finset.sum_eq_zero fun j hj => ?_
  rw [← Finset.mul_sum, hvan (j + 1) (Nat.le_add_left 1 j)
    (Nat.succ_le_of_lt (Finset.mem_range.1 hj)), mul_zero]

/-- Vanishing of the first `S.card` weighted power sums over a finite set of
nonzero complex numbers forces all weights to vanish. -/
lemma weights_eq_zero (S : Finset ℂ) (c : ℂ → ℂ) (h0 : (0 : ℂ) ∉ S)
    (hvan : ∀ k : ℕ, 1 ≤ k → k ≤ S.card → ∑ α ∈ S, c α * α ^ k = 0) :
    ∀ β ∈ S, c β = 0 := by
  intro β hβ
  have hcard : (S.erase β).card < S.card := Finset.card_erase_lt_of_mem hβ
  have hdeg : (sep S β).natDegree < S.card := by
    rw [sep_natDegree]; exact hcard
  have hsum := sum_mul_eval_eq_zero S c hvan (sep S β) hdeg
  have hsingle : ∑ α ∈ S, c α * α * (sep S β).eval α
      = c β * β * (sep S β).eval β := by
    refine Finset.sum_eq_single_of_mem β hβ fun γ hγ hne => ?_
    rw [sep_eval_ne S hγ hne, mul_zero]
  rw [hsingle] at hsum
  have hβ0 : β ≠ 0 := fun h => h0 (h ▸ hβ)
  rcases mul_eq_zero.1 hsum with h | h
  · rcases mul_eq_zero.1 h with h | h
    · exact h
    · exact absurd h hβ0
  · exact absurd h (sep_eval_self_ne_zero S β)

/-- Power sums as a sum over any finite set containing the support. -/
lemma powerSum_eq_sum (a : Multiset ℂ) (S : Finset ℂ) (hS : a.toFinset ⊆ S) (k : ℕ) :
    powerSum a k = ∑ α ∈ S, (a.count α : ℂ) * α ^ k := by
  rw [powerSum, Finset.sum_multiset_map_count]
  rw [Finset.sum_subset hS]
  · exact Finset.sum_congr rfl fun α _ => by rw [nsmul_eq_mul]
  · intro α _ hα
    have : a.count α = 0 := Multiset.count_eq_zero.2 (fun h => hα (Multiset.mem_toFinset.2 h))
    simp [this]

end PronyAux

/-- **Prony / power-sum uniqueness.** Two multisets of at most `d` nonzero
complex numbers whose power sums agree for `k = 1, …, 2*d` are equal. -/
theorem prony_power_sum_uniqueness (d : ℕ) (a b : Multiset ℂ)
    (ha : a.card ≤ d) (hb : b.card ≤ d)
    (h0a : (0 : ℂ) ∉ a) (h0b : (0 : ℂ) ∉ b)
    (h : ∀ k : ℕ, 1 ≤ k → k ≤ 2 * d → powerSum a k = powerSum b k) :
    a = b := by
  classical
  set S : Finset ℂ := (a + b).toFinset with hSdef
  have hsub : ∀ x : ℂ, x ∈ a ∨ x ∈ b → x ∈ S := by
    intro x hx
    rw [hSdef, Multiset.mem_toFinset, Multiset.mem_add]
    exact hx
  have hSa : a.toFinset ⊆ S := fun x hx => hsub x (Or.inl (Multiset.mem_toFinset.1 hx))
  have hSb : b.toFinset ⊆ S := fun x hx => hsub x (Or.inr (Multiset.mem_toFinset.1 hx))
  have h0S : (0 : ℂ) ∉ S := by
    intro hx
    rw [hSdef, Multiset.mem_toFinset, Multiset.mem_add] at hx
    rcases hx with hx | hx
    · exact h0a hx
    · exact h0b hx
  have hcard : S.card ≤ 2 * d := by
    have h1 : S.card ≤ (a + b).card := Multiset.toFinset_card_le _
    have h2 : (a + b).card = a.card + b.card := Multiset.card_add a b
    omega
  set c : ℂ → ℂ := fun α => (a.count α : ℂ) - (b.count α : ℂ) with hc
  have hvan : ∀ k : ℕ, 1 ≤ k → k ≤ S.card → ∑ α ∈ S, c α * α ^ k = 0 := by
    intro k hk1 hk2
    have hk : k ≤ 2 * d := le_trans hk2 hcard
    have heq := h k hk1 hk
    rw [PronyAux.powerSum_eq_sum a S hSa k, PronyAux.powerSum_eq_sum b S hSb k] at heq
    have hsub0 : (∑ α ∈ S, (a.count α : ℂ) * α ^ k) - (∑ α ∈ S, (b.count α : ℂ) * α ^ k) = 0 :=
      sub_eq_zero.2 heq
    rw [← Finset.sum_sub_distrib] at hsub0
    simpa [hc, sub_mul] using hsub0
  have hzero := PronyAux.weights_eq_zero S c h0S hvan
  ext α
  by_cases hα : α ∈ S
  · have hcz := hzero α hα
    rw [hc] at hcz
    simp only [sub_eq_zero] at hcz
    exact_mod_cast hcz
  · have hA : a.count α = 0 :=
      Multiset.count_eq_zero.2 (fun hx => hα (hsub α (Or.inl hx)))
    have hB : b.count α = 0 :=
      Multiset.count_eq_zero.2 (fun hx => hα (hsub α (Or.inr hx)))
    rw [hA, hB]

/-- Sharpness scaffold (OPTIONAL — prove only if it goes smoothly; the main
theorem above is the deliverable): with only `2*d - 1` matching power sums
the conclusion can fail. Witness for `d = 1`: `a = {1}`, `b = {-1}` share
`s_1`? No — `s_1` differs; a correct witness needs `d ≥ 2`, e.g. multisets
with matching `s_1..s_2` but different size. If no convenient witness is
found, SKIP this and deliver only the main theorem. -/
theorem prony_sharpness_placeholder : True := trivial

-- Axiom audit: reports `[propext, Classical.choice, Quot.sound]`.
#print axioms prony_power_sum_uniqueness
