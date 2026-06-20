import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat
open scoped Classical
open scoped Pointwise

set_option maxHeartbeats 8000000
set_option maxRecDepth 4000
set_option synthInstance.maxHeartbeats 20000
set_option synthInstance.maxSize 128

set_option relaxedAutoImplicit false
set_option autoImplicit false

set_option pp.fullNames true
set_option pp.structureInstances true
set_option pp.coercions.types true
set_option pp.funBinderTypes true
set_option pp.letVarTypes true
set_option pp.piBinderTypes true

set_option grind.warning false

lemma lambda_11_min_poly :
    let x : Real := 2 * Real.cos (Real.pi / 11)
    x^5 - x^4 - 4*x^3 + 3*x^2 + 3*x - 1 = 0 := by
  -- Set θ := π/11, c := cos θ.
  set θ : ℝ := Real.pi / 11
  set c : ℝ := Real.cos θ
  set x : ℝ := 2 * c
  have h_key : 1024 * c^11 - 2816 * c^9 + 2816 * c^7 - 1232 * c^5 + 220 * c^3 - 11 * c + 1 = 0 := by
    -- Use the recurrence relation for Chebyshev polynomials to compute $T_{11}(c)$.
    have h_recurrence : ∀ n : ℕ, Polynomial.eval c (Polynomial.Chebyshev.T ℝ n) = Real.cos (n * θ) := by
      aesop;
    have := h_recurrence 11;
    simp +zetaDelta at *;
    rw [ ← Complex.ofReal_inj ] ; norm_num [ Complex.cos, Complex.exp_re, Complex.exp_im ] ; ring_nf ; norm_num [ ← Complex.exp_nat_mul, ← Complex.exp_add ] ; ring_nf ; norm_num [ Complex.ext_iff, Complex.exp_re, Complex.exp_im ] ;
  exact sq_eq_zero_iff.mp ( by nlinarith [ show 0 < Real.cos ( Real.pi / 11 ) from Real.cos_pos_of_mem_Ioo ⟨ by linarith [ Real.pi_pos ], by linarith [ Real.pi_pos ] ⟩ ] )