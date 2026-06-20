Prove the following in Lean 4 with Mathlib, sorry-free. These are minimal-polynomial
identities for the Hecke triangle-group parameters lambda_q = 2*cos(pi/q), used to
formalize per-q realizations of the B(q) rotation-arc theorem.

Lemma 1 (q=5, golden ratio): let x : Real := 2 * Real.cos (Real.pi / 5).
  Then x^2 - x - 1 = 0.
  Hint: Mathlib has Real.cos_pi_div_five : Real.cos (pi/5) = (1 + Real.sqrt 5)/4.
  So x = (1 + sqrt 5)/2; finish with (sqrt 5)^2 = 5 (Real.sq_sqrt).

Lemma 2 (q=7): let x : Real := 2 * Real.cos (Real.pi / 7).
  Then x^3 - x^2 - 2*x + 1 = 0.
  Hint: with theta = pi/7, cos(7*theta) = cos pi = -1. Use the Chebyshev relation
  cos(7*theta) = T_7(cos theta) (Mathlib Polynomial.Chebyshev.T_real_cos /
  Polynomial.Chebyshev.cos_nat_mul). Expanding T_7 and setting c = cos(pi/7) gives
  64 c^7 - 112 c^5 + 56 c^3 - 7 c = -1. With x = 2c this factors as
  (x + 2)*(x^3 - x^2 - 2 x + 1)^2 = 0; since x = 2cos(pi/7) > 0 the cubic factor
  vanishes. (You may instead verify the cubic directly via the multiple-angle expansion.)

Return complete sorry-free Lean 4 proofs of both lemmas.
