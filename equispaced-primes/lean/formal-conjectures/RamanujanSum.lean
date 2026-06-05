/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai, formalized by Harmonic
-/

import Mathlib

set_option linter.unusedVariables false
set_option maxHeartbeats 400000

/-!
# Ramanujan Sum and the Primitive-Roots Identity

## Summary

We define the Ramanujan sum and prove the identity needed to
discharge the `h_ramanujan_decomp` hypothesis in
`formal-conjectures/FareyBridgeIdentity.lean`.

The key result is: for q ≥ 2 and gcd(n, q) = 1,
  c_q(n) = ∑_{a coprime to q} exp(2πi a n / q) = μ(q).

## Proof strategy

1. **Geometric sum**: ∑_{j=0}^{q-1} exp(2πi j k / q) = 0 for q ∤ k, q ≥ 1.
2. **Primitive roots sum = μ**: ∑_{a coprime to q} exp(2πi a / q) = μ(q),
   proved by showing both sides satisfy the same Dirichlet-convolution
   identity (S * ζ = 1 = μ * ζ).
3. **Coprime permutation**: when gcd(n,q) = 1, multiplication by n
   permutes the coprime residues mod q, so c_q(n) = c_q(1) = μ(q).
4. **FareySet decomposition**: the Farey exponential sum splits by
   denominator into Ramanujan sums plus boundary terms.

## References

* Hardy & Wright, *An Introduction to the Theory of Numbers*, 6th ed.,
  Theorem 304.
* Apostol, *Introduction to Analytic Number Theory*, Chapter 8.
-/

namespace RamanujanSum

open Nat Finset Complex BigOperators ArithmeticFunction

/-! ### Part 1: Geometric sum for roots of unity -/

/-- The q-th root of unity ω_q = exp(2πi/q). -/
noncomputable def rootOfUnity (q : ℕ) : ℂ :=
  Complex.exp (2 * Real.pi * Complex.I / q)

/-
Sum of all q-th roots of unity raised to the k-th power is 0
when q ≥ 1 and q ∤ k. This is the geometric sum identity.
-/
lemma geom_sum_roots_of_unity (q : ℕ) (hq : 0 < q) (k : ℤ) (hk : ¬ (q : ℤ) ∣ k) :
    ∑ j ∈ Finset.range q, Complex.exp (2 * ↑Real.pi * Complex.I * ↑k * ↑j / ↑q) = 0 := by
  -- Let $\omega = e^{2 \pi i k / q}$. Since $q \nmid k$, $\omega \neq 1$.
  set ω : ℂ := Complex.exp (2 * Real.pi * Complex.I * k / q)
  have hω_ne_one : ω ≠ 1 := by
    rw [ Ne.eq_def, Complex.exp_eq_one_iff ];
    exact fun ⟨ n, hn ⟩ => hk <| ⟨ n, by rw [ ← @Int.cast_inj ℂ ] ; push_cast; rw [ div_eq_iff ( Nat.cast_ne_zero.mpr hq.ne' ) ] at hn; norm_num [ Complex.ext_iff ] at *; nlinarith [ Real.pi_pos ] ⟩;
  convert geom_sum_eq hω_ne_one q using 1;
  · exact Finset.sum_congr rfl fun _ _ => by rw [ ← Complex.exp_nat_mul ] ; ring;
  · rw [ ← Complex.exp_nat_mul, mul_comm, Complex.exp_eq_one_iff.mpr ⟨ k, by ring_nf; norm_num [ hq.ne' ] ⟩ ] ; ring

/-
Sum of all q-th roots of unity is 0 when q ≥ 2.
-/
lemma sum_roots_of_unity_eq_zero (q : ℕ) (hq : 2 ≤ q) :
    ∑ j ∈ Finset.range q, Complex.exp (2 * ↑Real.pi * Complex.I * ↑j / ↑q) = 0 := by
  convert geom_sum_roots_of_unity q ( by positivity ) 1 _ using 3 <;> norm_num;
  exact_mod_cast Nat.not_dvd_of_pos_of_lt Nat.one_pos hq

/-
exp(2πi * n) = 1 for any integer n.
-/
lemma exp_two_pi_int_mul_I (n : ℤ) :
    Complex.exp (2 * ↑Real.pi * Complex.I * ↑n) = 1 := by
  exact Complex.exp_eq_one_iff.mpr ⟨ n, by ring ⟩

/-! ### Part 2: Primitive roots sum equals Möbius function -/

/-- The sum of primitive q-th roots of unity:
    S(q) = ∑_{a coprime to q, 0 ≤ a < q} exp(2πi a / q). -/
noncomputable def primRootsSum (q : ℕ) : ℂ :=
  ∑ a ∈ (Finset.range q).filter (fun a => Nat.Coprime a q),
    Complex.exp (2 * ↑Real.pi * Complex.I * ↑a / ↑q)

/-
S(1) = 1.
-/
lemma primRootsSum_one : primRootsSum 1 = 1 := by
  unfold primRootsSum;
  norm_num

/-
The key identity: S(q) = μ(q) for all q ≥ 1.
    This is the sum of primitive q-th roots of unity.
-/
theorem primRootsSum_eq_moebius (q : ℕ) (hq : 0 < q) :
    primRootsSum q = ↑(ArithmeticFunction.moebius q : ℤ) := by
  -- We'll use the fact that if the sum of the Möbius function over the divisors of $n$ is zero, then $n$ must be 1.
  have h_sum_zero : ∀ n : ℕ, 0 < n → (∑ d ∈ n.divisors, (primRootsSum d : ℂ)) = if n = 1 then 1 else 0 := by
    intro n hn; split_ifs <;> simp_all +decide [ primRootsSum ] ;
    -- For each divisor $d$ of $n$, the inner sum $\sum_{a \in \text{coprime}(d)} \exp(2\pi i a / d)$ is the sum of all primitive $d$-th roots of unity.
    have h_inner_sum : ∀ d ∈ n.divisors, ∑ a ∈ Finset.filter (fun a => Nat.Coprime a d) (Finset.range d), Complex.exp (2 * Real.pi * Complex.I * a / d) = ∑ a ∈ Finset.filter (fun a => Nat.gcd a n = n / d) (Finset.range n), Complex.exp (2 * Real.pi * Complex.I * a / n) := by
      intro d hd
      have h_inner_sum_eq : Finset.filter (fun a => Nat.gcd a n = n / d) (Finset.range n) = Finset.image (fun a => a * (n / d)) (Finset.filter (fun a => Nat.Coprime a d) (Finset.range d)) := by
        ext a;
        constructor;
        · intro ha
          obtain ⟨k, hk⟩ : ∃ k, a = k * (n / d) := by
            exact exists_eq_mul_left_of_dvd ( Nat.dvd_trans ( by aesop ) ( Finset.mem_filter.mp ha |>.2 ▸ Nat.gcd_dvd_left _ _ ) );
          simp_all +decide [ Nat.gcd_mul_left, Nat.gcd_mul_right ];
          cases hd.1 ; simp_all +decide [ Nat.gcd_mul_left, Nat.gcd_mul_right ];
          tauto;
        · simp +zetaDelta at *;
          rintro x hx₁ hx₂ rfl; refine' ⟨ _, _ ⟩;
          · nlinarith [ Nat.div_mul_cancel hd.1 ];
          · cases hd.1 ; simp_all +decide [ Nat.gcd_mul_left, Nat.gcd_mul_right ];
      rw [ h_inner_sum_eq, Finset.sum_image ];
      · refine' Finset.sum_congr rfl fun x hx => _;
        rw [ Nat.cast_mul, Nat.cast_div ( Nat.dvd_of_mem_divisors hd ) ] <;> ring <;> norm_num [ hn.ne' ];
        grind +splitImp;
      · exact fun x hx y hy hxy => mul_right_cancel₀ ( Nat.ne_of_gt ( Nat.div_pos ( Nat.le_of_dvd hn ( Nat.dvd_of_mem_divisors hd ) ) ( Nat.pos_of_mem_divisors hd ) ) ) hxy;
    rw [ Finset.sum_congr rfl h_inner_sum, ← Finset.sum_biUnion ];
    · rw [ show ( Finset.biUnion ( Nat.divisors n ) fun x => Finset.filter ( fun a => Nat.gcd a n = n / x ) ( Finset.range n ) ) = Finset.range n from ?_ ];
      · convert sum_roots_of_unity_eq_zero n ( Nat.lt_of_le_of_ne hn ( Ne.symm ‹_› ) ) using 1;
      · ext a; simp [Finset.mem_biUnion];
        constructor;
        · aesop;
        · exact fun ha => ⟨ n / Nat.gcd a n, ⟨ Nat.div_dvd_of_dvd <| Nat.gcd_dvd_right _ _, hn.ne' ⟩, ha, by rw [ Nat.div_div_self ( Nat.gcd_dvd_right _ _ ) hn.ne' ] ⟩;
    · intros x hx y hy hxy; simp_all +decide [ Finset.disjoint_left ] ;
      intro a ha₁ ha₂ ha₃; have := Nat.div_mul_cancel hx.1; have := Nat.div_mul_cancel hy; simp_all +decide [ Nat.mul_div_cancel' ] ;
      exact hxy ( by nlinarith );
  have h_induction_step : ∀ n : ℕ, 0 < n → (∀ d ∈ n.divisors, d < n → primRootsSum d = (moebius d : ℂ)) → primRootsSum n = (moebius n : ℂ) := by
    intros n hn h_ind_hyp
    have h_sum_eq : ∑ d ∈ n.divisors, (primRootsSum d : ℂ) = ∑ d ∈ n.divisors, (moebius d : ℂ) := by
      have h_sum_eq : ∑ d ∈ n.divisors, (moebius d : ℂ) = (ArithmeticFunction.moebius * ArithmeticFunction.zeta : ArithmeticFunction ℂ) n := by
        simp +decide [ ArithmeticFunction.moebius, ArithmeticFunction.zeta ];
        rw [ Nat.sum_divisorsAntidiagonal fun x y => if y = 0 then 0 else if Squarefree x then ( -1 : ℂ ) ^ cardFactors x else 0 ];
        exact Finset.sum_congr rfl fun x hx => by rw [ if_neg ( Nat.ne_of_gt ( Nat.div_pos ( Nat.le_of_dvd hn ( Nat.dvd_of_mem_divisors hx ) ) ( Nat.pos_of_mem_divisors hx ) ) ) ] ;
      aesop;
    rw [ ← Finset.sum_erase_add _ _ ( Nat.mem_divisors_self _ hn.ne' ), ← Finset.sum_erase_add _ _ ( Nat.mem_divisors_self _ hn.ne' ) ] at h_sum_eq;
    rw [ Finset.sum_congr rfl fun x hx => h_ind_hyp x ( Finset.mem_of_mem_erase hx ) ( Nat.lt_of_le_of_ne ( Nat.le_of_dvd hn ( Nat.dvd_of_mem_divisors ( Finset.mem_of_mem_erase hx ) ) ) ( by aesop ) ) ] at h_sum_eq ; aesop;
  induction' q using Nat.strongRecOn with n ih;
  exact h_induction_step n hq fun d hd hd' => ih d hd' ( Nat.pos_of_mem_divisors hd )

/-! ### Part 3: Ramanujan sum at coprime arguments -/

/-- The Ramanujan sum c_q(n) = ∑_{a coprime to q, 0 ≤ a < q} exp(2πi a n / q). -/
noncomputable def ramanujanSum (q n : ℕ) : ℂ :=
  ∑ a ∈ (Finset.range q).filter (fun a => Nat.Coprime a q),
    Complex.exp (2 * ↑Real.pi * Complex.I * ↑(a * n) / ↑q)

/-
c_q(n) = μ(q) when gcd(n, q) = 1 and q ≥ 1.
-/
theorem ramanujanSum_eq_moebius_of_coprime (q n : ℕ) (hq : 0 < q) (hcop : Nat.Coprime n q) :
    ramanujanSum q n = ↑(ArithmeticFunction.moebius q : ℤ) := by
  have h_bij : Finset.image (fun a => (a * n) % q) ((Finset.range q).filter (fun a => Nat.Coprime a q)) = (Finset.range q).filter (fun a => Nat.Coprime a q) := by
    refine' Finset.eq_of_subset_of_card_le ( Finset.image_subset_iff.mpr _ ) _;
    · simp +zetaDelta at *;
      exact fun x hx₁ hx₂ => ⟨ Nat.mod_lt _ hq, hx₂.mul_left hcop ⟩;
    · rw [ Finset.card_image_of_injOn ];
      intros a ha b hb hab ; simp_all +decide [ ← ZMod.natCast_eq_natCast_iff' ];
      have h_eq : (a : ZMod q) = (b : ZMod q) := by
        have h_eq : IsUnit (n : ZMod q) := by
          exact (ZMod.isUnit_iff_coprime n q).mpr hcop;
        exact h_eq.mul_left_inj.mp hab;
      exact Nat.mod_eq_of_lt ha.1 ▸ Nat.mod_eq_of_lt hb.1 ▸ by simpa [ ← ZMod.natCast_eq_natCast_iff' ] using h_eq;
  convert primRootsSum_eq_moebius q hq using 1;
  refine' Eq.trans _ ( Finset.sum_bij ( fun a ha => a * n % q ) _ _ _ _ );
  convert rfl;
  · grind;
  · intro a₁ ha₁ a₂ ha₂ h; have := Finset.card_image_iff.mp ( by aesop : Finset.card ( Finset.image ( fun a => a * n % q ) ( Finset.filter ( fun a => Nat.Coprime a q ) ( Finset.range q ) ) ) = Finset.card ( Finset.filter ( fun a => Nat.Coprime a q ) ( Finset.range q ) ) ) ; aesop;
  · intro b hb; replace h_bij := Finset.ext_iff.mp h_bij b; aesop;
  · intro a ha; rw [ Complex.exp_eq_exp_iff_exists_int ] ; use a * n / q; push_cast [ Nat.mod_def ] ; ring;
    rw [ Nat.cast_sub ( Nat.mul_div_le _ _ ) ] ; push_cast ; ring;
    norm_num [ hq.ne' ];
    norm_cast ; aesop

/-! ### Part 4: FareySet decomposition -/

-- Import the FareySet definition
-- We redefine it here for self-containment
/-- `FareySet n` is the set of coprime pairs `(a, b)` in `ℕ × ℕ` with
`b ≥ 1` and `b ≤ n` and `a ≤ b` (so `a/b ∈ [0, 1]`). -/
def FareySet (n : ℕ) : Finset (ℕ × ℕ) :=
  (Finset.range (n + 1)).biUnion (fun b =>
    if h : b = 0 then ∅
    else
      (Finset.range (b + 1)).filter
        (fun a => Nat.Coprime a b)
      |>.image (fun a => (a, b))
    )

/-
The Farey exponential sum decomposes by denominator into
Ramanujan sums c_b(p), each equal to μ(b) since gcd(p,b) = 1
for all b ≤ p-1 when p is prime, plus boundary terms.

This discharges the `h_ramanujan_decomp` hypothesis in
`FareyBridgeIdentity.lean`.
-/
theorem farey_ramanujan_decomp (p : ℕ) (hp : Nat.Prime p) :
    ∑ pair ∈ FareySet (p - 1),
        Complex.exp
          ((2 * ↑Real.pi : ℂ) * Complex.I * (↑p : ℂ) *
           (↑pair.1 : ℂ) / (↑pair.2 : ℂ))
      = 1 + ∑ b ∈ Finset.Icc 1 (p - 1),
          (↑(ArithmeticFunction.moebius b : ℤ) : ℂ) := by
  have h_sum : ∀ b ∈ Finset.Icc 1 (p - 1), ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), Complex.exp (2 * Real.pi * Complex.I * (p * a) / b) = (ArithmeticFunction.moebius b : ℂ) := by
    intros b hb
    have h_coprime : Nat.Coprime p b := by
      exact hp.coprime_iff_not_dvd.mpr fun h => by have := Nat.le_of_dvd ( by linarith [ Finset.mem_Icc.mp hb ] ) h; linarith [ Finset.mem_Icc.mp hb, Nat.sub_add_cancel hp.pos ] ;
    have h_sum_eq : ∑ a ∈ Finset.filter (fun a => Nat.Coprime a b) (Finset.range b), Complex.exp (2 * Real.pi * Complex.I * (p * a) / b) = ramanujanSum b p := by
      exact Finset.sum_congr rfl fun x hx => by push_cast; ring;
    rw [ h_sum_eq, ramanujanSum_eq_moebius_of_coprime ] <;> aesop;
  rw [ ← Finset.sum_congr rfl h_sum ];
  erw [ Finset.sum_biUnion ];
  · erw [ Finset.sum_Ico_eq_sub _ ] <;> norm_num [ Finset.sum_range_succ' ];
    simp +decide [ Finset.sum_filter, Finset.sum_range_succ, mul_assoc, mul_div_assoc ];
    rw [ Finset.sum_add_distrib ] ; norm_num [ add_comm, add_left_comm, add_assoc ];
    rw [ if_pos hp.one_lt ] ; rw [ Complex.exp_eq_one_iff ] ; use p ; push_cast ; ring;
  · grind +suggestions

end RamanujanSum