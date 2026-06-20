import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat
open scoped Classical
open scoped Pointwise

open Polynomial Chebyshev

set_option maxHeartbeats 8000000
set_option maxRecDepth 4000

/-- Lemma 1 (q = 5, golden ratio): with `x = 2 cos(π/5)`, the golden-ratio
minimal polynomial vanishes: `x² - x - 1 = 0`. -/
theorem hecke_lambda_five :
    let x : ℝ := 2 * Real.cos (Real.pi / 5)
    x ^ 2 - x - 1 = 0 := by
  intro x
  have h := Real.cos_pi_div_five
  have hs : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  show (2 * Real.cos (Real.pi / 5)) ^ 2 - 2 * Real.cos (Real.pi / 5) - 1 = 0
  rw [h]
  nlinarith [hs]

/-- Lemma 2 (q = 7): with `x = 2 cos(π/7)`, the degree-3 minimal polynomial
vanishes: `x³ - x² - 2x + 1 = 0`. -/
theorem hecke_lambda_seven :
    let x : ℝ := 2 * Real.cos (Real.pi / 7)
    x ^ 3 - x ^ 2 - 2 * x + 1 = 0 := by
  intro x
  set c := Real.cos (Real.pi / 7) with hcdef
  -- Expand the 7th Chebyshev polynomial of the first kind via its recurrence.
  have hexp : eval c (T ℝ 7) = 64 * c ^ 7 - 112 * c ^ 5 + 56 * c ^ 3 - 7 * c := by
    have hrec : ∀ n : ℤ,
        eval c (T ℝ (n + 2)) = 2 * c * eval c (T ℝ (n + 1)) - eval c (T ℝ n) := by
      intro n
      rw [Polynomial.Chebyshev.T_add_two ℝ n]
      simp only [eval_sub, eval_mul, eval_X, eval_ofNat]
    have e2 := hrec 0
    have e3 := hrec 1
    have e4 := hrec 2
    have e5 := hrec 3
    have e6 := hrec 4
    have e7 := hrec 5
    have e0 : eval c (T ℝ 0) = 1 := by simp
    have e1 : eval c (T ℝ 1) = c := by simp
    norm_num at e2 e3 e4 e5 e6 e7
    rw [e7, e6, e5, e4, e3, e2]; ring
  -- `T_7(cos(π/7)) = cos(π) = -1`.
  have hcos : eval c (T ℝ (7 : ℤ)) = -1 := by
    rw [hcdef, Polynomial.Chebyshev.T_real_cos (Real.pi / 7) 7]
    have h7 : ((7 : ℤ) : ℝ) * (Real.pi / 7) = Real.pi := by push_cast; ring
    rw [h7, Real.cos_pi]
  rw [hcos] at hexp
  have hkey : 64 * c ^ 7 - 112 * c ^ 5 + 56 * c ^ 3 - 7 * c = -1 := hexp.symm
  have hcpos : 0 < c := by
    rw [hcdef]
    apply Real.cos_pos_of_mem_Ioo
    constructor
    · nlinarith [Real.pi_pos]
    · nlinarith [Real.pi_pos]
  have hxpos : 0 < x := by simp only [x]; positivity
  -- `x⁷ - 7x⁵ + 14x³ - 7x + 2 = (x+2)·(x³-x²-2x+1)²`.
  have hfac : (x + 2) * (x ^ 3 - x ^ 2 - 2 * x + 1) ^ 2 = 0 := by
    show (2 * c + 2) * ((2 * c) ^ 3 - (2 * c) ^ 2 - 2 * (2 * c) + 1) ^ 2 = 0
    nlinarith [hkey]
  have hx2 : x + 2 > 0 := by linarith
  have hsq : (x ^ 3 - x ^ 2 - 2 * x + 1) ^ 2 = 0 := by
    rcases mul_eq_zero.mp hfac with h | h
    · linarith
    · exact h
  exact pow_eq_zero_iff (by norm_num) |>.mp hsq
