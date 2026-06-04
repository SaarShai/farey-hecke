import Mathlib

/-!
# Q-Linear Independence of Logarithms of Distinct Primes

This file proves that the set {log p : p prime} is Q-linearly independent.
Specifically: for any finite set S of distinct primes and rational coefficients
q_p, if Σ_{p ∈ S} q_p * log p = 0, then every q_p = 0.

## Main result

`log_prime_Q_linear_indep`: The logarithms of distinct primes are linearly
independent over ℚ.
-/

open Real Finset BigOperators

/-! ### Helper lemmas about factorization of products of prime powers -/

/-
The factorization of a product of prime powers ∏_{p ∈ S} p^{f(p)} over a
set of distinct primes evaluates to f(q) at any prime q ∈ S.
-/
lemma factorization_prod_prime_pow (S : Finset ℕ) (hS : ∀ p ∈ S, Nat.Prime p)
    (f : ℕ → ℕ) (q : ℕ) (hq : q ∈ S) :
    (∏ p ∈ S, p ^ f p).factorization q = f q := by
  rw [ Nat.factorization_prod ];
  · simp +contextual [ *, Finset.sum_apply' ];
    rw [ Finset.sum_eq_single q ] <;> aesop;
  · exact fun p hp => pow_ne_zero _ ( Nat.Prime.ne_zero ( hS p hp ) )

/-
If two products of prime powers over a set of distinct primes are equal,
then the exponents agree at every prime in the set.
-/
lemma prod_prime_pow_eq_imp_eq (S : Finset ℕ) (hS : ∀ p ∈ S, Nat.Prime p)
    (f g : ℕ → ℕ)
    (heq : ∏ p ∈ S, p ^ f p = ∏ p ∈ S, p ^ g p) :
    ∀ p ∈ S, f p = g p := by
  intro p hp;
  apply_fun fun x => x.factorization p at heq;
  rw [ Nat.factorization_prod, Nat.factorization_prod ] at heq;
  · simp_all +decide [ Finset.sum_apply' ];
    rw [ Finset.sum_eq_single p, Finset.sum_eq_single p ] at heq <;> aesop;
  · exact fun x hx => pow_ne_zero _ ( Nat.Prime.ne_zero ( hS x hx ) );
  · exact fun x hx => pow_ne_zero _ ( Nat.Prime.ne_zero ( hS x hx ) )

/-! ### From integer linear combination of logs to equal products -/

/-
If ∑_{p ∈ S} a(p) * log(p) = 0 with integer coefficients and S primes,
then all a(p) = 0.
-/
lemma int_log_sum_zero (S : Finset ℕ) (hS : ∀ p ∈ S, Nat.Prime p)
    (a : ℕ → ℤ)
    (hsum : ∑ p ∈ S, (a p : ℝ) * Real.log p = 0) :
    ∀ p ∈ S, a p = 0 := by
  -- Split the sum: $\sum \text{posExp}(p) \log(p) = \sum \text{negExp}(p) \log(p)$.
  have split_sum : (∑ p ∈ S, ((a p).toNat : ℝ) * Real.log p) = (∑ p ∈ S, ((-a p).toNat : ℝ) * Real.log p) := by
    convert congr_arg ( fun x : ℝ => x + ∑ p ∈ S, ( Int.toNat ( -a p ) : ℝ ) * Real.log p ) hsum using 1 <;> norm_num [ Finset.sum_add_distrib ];
    rw [ ← Finset.sum_add_distrib ] ; refine' Finset.sum_congr rfl fun p hp => _ ; cases' Int.eq_nat_or_neg ( a p ) with h h ; aesop;
  -- By exponentiating both sides, we obtain $\prod_{p \in S} p^{\text{posExp}(p)} = \prod_{p \in S} p^{\text{negExp}(p)}$.
  have exp_eq : (∏ p ∈ S, p ^ (Int.toNat (a p))) = (∏ p ∈ S, p ^ (Int.toNat (-a p))) := by
    have exp_eq : Real.exp (∑ p ∈ S, ((a p).toNat : ℝ) * Real.log p) = Real.exp (∑ p ∈ S, ((-a p).toNat : ℝ) * Real.log p) := by
      rw [split_sum];
    rw [ Real.exp_sum, Real.exp_sum ] at exp_eq;
    rw [ ← @Nat.cast_inj ℝ ] ; push_cast ; convert exp_eq using 2 <;> rw [ Real.exp_nat_mul, Real.exp_log ( Nat.cast_pos.mpr <| Nat.Prime.pos <| hS _ _ ) ];
    · assumption;
    · assumption;
  intro p hp; replace exp_eq := prod_prime_pow_eq_imp_eq S hS ( fun p ↦ Int.toNat ( a p ) ) ( fun p ↦ Int.toNat ( -a p ) ) ( mod_cast exp_eq ) p hp;
  grind

/-! ### Main theorems -/

/-
Logarithms of distinct primes are linearly independent over ℚ.

For any finite set S of distinct primes and rational coefficients (q : ℕ → ℚ),
if the weighted sum Σ_{p ∈ S} q(p) * log p = 0, then q(p) = 0 for all p ∈ S.
-/
theorem log_prime_Q_linear_indep
    (S : Finset ℕ) (hS : ∀ p ∈ S, Nat.Prime p)
    (q : ℕ → ℚ)
    (hsum : ∑ p ∈ S, (q p : ℝ) * Real.log p = 0) :
    ∀ p ∈ S, q p = 0 := by
  intro p hp;
  -- Let $D = \prod_{p \in S} (q p).den$. Then $D > 0$ and for each $p \in S$, $D * (q p)$ is an integer.
  set D := ∏ p ∈ S, (q p).den with hD
  have hD_pos : 0 < D := by
    exact Finset.prod_pos fun p hp => Rat.pos _
  have hD_int : ∀ p ∈ S, ∃ k : ℤ, D * (q p) = k := by
    intro p hp
    use D * (q p).num / (q p).den;
    rw [ Int.cast_div ] <;> norm_num;
    · rw [ mul_div_assoc, Rat.num_div_den ];
    · exact dvd_mul_of_dvd_left ( mod_cast Finset.dvd_prod_of_mem _ hp ) _;
  -- By multiplying both sides of the equation $\sum_{p \in S} q(p) \log(p) = 0$ by $D$, we obtain $\sum_{p \in S} (D q(p)) \log(p) = 0$.
  have h_mul_D : ∑ p ∈ S, ((D * (q p)) : ℝ) * (Real.log p) = 0 := by
    simp_all +decide [ mul_assoc, ← Finset.mul_sum _ _ _ ];
  choose! k hk using hD_int;
  -- By the properties of logarithms and the fact that $k(p)$ are integers, we can apply the lemma `int_log_sum_zero`.
  have h_int_log_sum_zero : ∀ p ∈ S, k p = 0 := by
    convert int_log_sum_zero S hS k _;
    convert h_mul_D using 2 ; norm_cast at * ; aesop;
  simpa [ hD_pos.ne', h_int_log_sum_zero p hp ] using hk p hp

/-
Equivalent formulation: the family (Real.log ·) on primes is ℚ-linearly
independent as a family of real numbers, in the sense that any finite ℚ-linear
combination that equals zero has all coefficients zero.
-/
theorem log_prime_Q_linear_indep' :
    LinearIndependent ℚ (fun p : {p : ℕ // Nat.Prime p} => Real.log (p : ℝ)) := by
  refine' linearIndependent_iff'.mpr fun S f hf => _;
  convert log_prime_Q_linear_indep ( S.image Subtype.val ) ( by aesop ) ( fun p => if h : p.Prime then f ⟨ p, h ⟩ else 0 ) ?_ using 1;
  · aesop;
  · convert hf using 1;
    simp +zetaDelta at *;
    exact Finset.sum_congr rfl fun x hx => by erw [ if_pos x.2 ] ; norm_num [ Algebra.smul_def ] ;