import Mathlib
open Real
/-! # Hecke λ-bound: the isolating lower bound `9/5 < λ_q = 2cos(π/q)` for all q ≥ 10.

This DISCHARGES the `hlo : 9/5 < lam` hypothesis carried by the multi-root window lemmas
`g{q}_no_window_below_genuine` (q ∈ {10,11,13,14,16}), where the minimal-polynomial relation `hps`
alone does NOT isolate `λ_q` from its smaller conjugate roots in (1,2).  Proof: `1 - x²/2 ≤ cos x`
(Mathlib) with `x = π/q` and `π < 3.15` (`Real.pi_lt_d2`).  `9/5 < λ_q < 2` is the unique interval
separating `λ_q` (≥ 1.802) from every other minpoly root in (1,2) (≤ 1.663). -/
theorem hecke_lam_lo (q : ℕ) (hq : 10 ≤ q) : (9:ℝ)/5 < 2 * Real.cos (Real.pi / q) := by
  have hlb := Real.one_sub_sq_div_two_le_cos (x := Real.pi / q)
  have hpi : Real.pi < 3.15 := by have h := Real.pi_lt_d2; norm_num at h ⊢; linarith
  have hpip : (0:ℝ) < Real.pi := Real.pi_pos
  have hqr : (10:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have hx2 : (Real.pi / q)^2 < 1/5 := by
    rw [div_pow, div_lt_iff₀ (by positivity)]
    nlinarith [hpi, hpip, hqr, sq_nonneg ((q:ℝ)-10)]
  linarith [hlb, hx2]

#print axioms hecke_lam_lo
