Prove the following in Lean 4 with Mathlib, sorry-free.

This is the minimal-polynomial identity for the Hecke triangle-group parameter
lambda_9 = 2*cos(pi/9), the q=9 case of the lambda_q = 2*cos(pi/q) family.

Lemma (q = 9): let x : Real := 2 * Real.cos (Real.pi / 9).
  Then x^3 - 3*x - 1 = 0.

Hint (Chebyshev, the same method that worked for q=7).
  Set c = Real.cos (Real.pi / 9) and theta = pi/9. Then cos(9*theta) = cos pi = -1.
  Use the Chebyshev relation cos(9*theta) = T_9(cos theta) (Mathlib
  Polynomial.Chebyshev.T_real_cos). Expand the 9th Chebyshev polynomial of the
  first kind via its recurrence (Polynomial.Chebyshev.T_add_two):

      eval c (T R 9) = 256*c^9 - 576*c^7 + 432*c^5 - 120*c^3 + 9*c.

  Evaluating with Polynomial.Chebyshev.T_real_cos at theta = pi/9 gives
  T_9(c) = cos(pi) = -1, hence

      256*c^9 - 576*c^7 + 432*c^5 - 120*c^3 + 9*c = -1,   i.e.
      256*c^9 - 576*c^7 + 432*c^5 - 120*c^3 + 9*c + 1 = 0.

  Substituting x = 2*c, this factors EXACTLY as

      (x - 1)^2 * (x + 2) * (x^3 - 3*x - 1)^2 = 0

  (equivalently, with c: (1/2)*(2c-1)^2*(2c+2)*((2c)^3 - 3*(2c) - 1)^2 = 0 equals
  the polynomial above; expand and check by `nlinarith`/`ring` from the hkey
  equation). Since x = 2*cos(pi/9) and pi/9 in (0, pi/3) we have
  cos(pi/9) > cos(pi/3) = 1/2, so x = 2*cos(pi/9) > 1, hence x - 1 > 0 and also
  x + 2 > 0. Therefore the two linear cofactors are nonzero, forcing the squared
  cubic factor to vanish, hence the cubic x^3 - 3*x - 1 itself is 0.

Note the difference from q=7: there is an extra (x-1)^2 cofactor here, so you
must rule out x = 1 as well (use cos(pi/9) > 1/2, e.g. via
Real.cos_lt_cos / strict antitone on [0, pi], or
Real.cos_pos_of_mem_Ioo together with a bound giving cos(pi/9) > 1/2).

Return a complete sorry-free Lean 4 proof of the lemma.
