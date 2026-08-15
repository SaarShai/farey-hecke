import Mathlib

/-!
# R1 completion pack: three finite inequalities for the truncation chain

(1) `l2_le_card_mul_sup_sq`: for a finite family of complex values,
    the sum of squared moduli is at most the cardinality times the sup
    squared — the finite Parseval-side bound used to dominate H²-type
    norms by boundary sups.
(2) `coeff_bound_of_uniform`: discrete-Cauchy coefficient bound — if
    c_k = (1/M) Σ_{t<M} f(t) ω^{-kt} with |f(t)| ≤ B for all t, then
    |c_k| ≤ B (any M ≥ 1, any complex root-of-unity-like weights of
    modulus 1).
(3) `geom_tail_le`: for 0 < ρ < 1, b ≥ 0, N ≤ K:
    Σ_{k=N}^{K} b·ρ^k ≤ b·ρ^N/(1−ρ).
-/

open BigOperators Finset

theorem l2_le_card_mul_sup_sq (n : ℕ) (c : Fin n → ℂ) (B : ℝ)
    (hB : ∀ i, ‖c i‖ ≤ B) :
    (∑ i, ‖c i‖ ^ 2) ≤ (n : ℝ) * B ^ 2 := by
  calc (∑ i, ‖c i‖ ^ 2)
      ≤ ∑ _i : Fin n, B ^ 2 :=
        Finset.sum_le_sum fun i _ => pow_le_pow_left₀ (norm_nonneg _) (hB i) 2
    _ = (n : ℝ) * B ^ 2 := by simp

theorem coeff_bound_of_uniform (M : ℕ) (hM : 0 < M)
    (f w : Fin M → ℂ) (B : ℝ)
    (hf : ∀ t, ‖f t‖ ≤ B) (hw : ∀ t, ‖w t‖ = 1) :
    ‖(1 / (M : ℂ)) * ∑ t, f t * w t‖ ≤ B := by
  have hM0 : (0 : ℝ) < (M : ℝ) := by exact_mod_cast hM
  have hsum : ‖∑ t, f t * w t‖ ≤ (M : ℝ) * B := by
    calc ‖∑ t, f t * w t‖
        ≤ ∑ t, ‖f t * w t‖ := norm_sum_le _ _
      _ = ∑ t, ‖f t‖ := by simp [hw]
      _ ≤ ∑ _t : Fin M, B := Finset.sum_le_sum fun t _ => hf t
      _ = (M : ℝ) * B := by simp
  rw [norm_mul, norm_div]
  simp only [norm_one, Complex.norm_natCast]
  rw [div_mul_eq_mul_div, one_mul, div_le_iff₀ hM0]
  calc ‖∑ t, f t * w t‖ ≤ (M : ℝ) * B := hsum
    _ = B * M := mul_comm _ _

theorem geom_tail_le (ρ b : ℝ) (hρ0 : 0 < ρ) (hρ1 : ρ < 1) (hb : 0 ≤ b)
    (N K : ℕ) (hNK : N ≤ K) :
    (∑ k ∈ Icc N K, b * ρ ^ k) ≤ b * ρ ^ N / (1 - ρ) := by
  have h1ρ : 0 < 1 - ρ := by linarith
  have hgeom : ∀ m : ℕ, ∑ j ∈ range m, ρ ^ j ≤ 1 / (1 - ρ) := by
    intro m
    rw [geom_sum_eq (by linarith : ρ ≠ 1)]
    have he : (ρ ^ m - 1) / (ρ - 1) = (1 - ρ ^ m) / (1 - ρ) := by
      rw [← neg_div_neg_eq]; ring_nf
    have hpow : (0 : ℝ) ≤ ρ ^ m := pow_nonneg hρ0.le m
    rw [he]
    gcongr
    linarith
  rw [← Ico_add_one_right_eq_Icc, Finset.sum_Ico_eq_sum_range]
  have hfac : ∑ k ∈ range (K + 1 - N), b * ρ ^ (N + k)
      = b * ρ ^ N * ∑ k ∈ range (K + 1 - N), ρ ^ k := by
    rw [Finset.mul_sum]
    exact Finset.sum_congr rfl fun k _ => by rw [pow_add]; ring
  rw [hfac, div_eq_mul_one_div]
  exact mul_le_mul_of_nonneg_left (hgeom _) (by positivity)

#print axioms l2_le_card_mul_sup_sq
#print axioms coeff_bound_of_uniform
#print axioms geom_tail_le
