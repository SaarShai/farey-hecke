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
  sorry

theorem coeff_bound_of_uniform (M : ℕ) (hM : 0 < M)
    (f w : Fin M → ℂ) (B : ℝ)
    (hf : ∀ t, ‖f t‖ ≤ B) (hw : ∀ t, ‖w t‖ = 1) :
    ‖(1 / (M : ℂ)) * ∑ t, f t * w t‖ ≤ B := by
  sorry

theorem geom_tail_le (ρ b : ℝ) (hρ0 : 0 < ρ) (hρ1 : ρ < 1) (hb : 0 ≤ b)
    (N K : ℕ) (hNK : N ≤ K) :
    (∑ k ∈ Icc N K, b * ρ ^ k) ≤ b * ρ ^ N / (1 - ρ) := by
  sorry
