Prove the following in Lean 4 with Mathlib, sorry-free.

Lemma (n=11): let x : Real := 2 * Real.cos (Real.pi / 11).
  Then x^5 - x^4 - 4*x^3 + 3*x^2 + 3*x - 1 = 0.

This is the minimal-polynomial identity for the Hecke triangle-group parameter
lambda_11 = 2*cos(pi/11) (degree phi(22)/2 = 5).

Suggested route (analogous to a proven n=7 proof): with c = cos(pi/11) and
theta = pi/11, we have cos(11*theta) = cos(pi) = -1. Use the Chebyshev relation
cos(11*theta) = T_11(cos theta) via Mathlib's Polynomial.Chebyshev.T_real_cos
(eval (cos theta) (T R 11) = cos (11 * theta)). Expand T_11 via its recurrence
Polynomial.Chebyshev.T_add_two to get
  eval c (T R 11) = 1024 c^11 - 2816 c^9 + 2816 c^7 - 1232 c^5 + 220 c^3 - 11 c.
Setting this equal to -1 gives, with x = 2c, the factorization
  (x + 2) * (x^5 - x^4 - 4 x^3 + 3 x^2 + 3 x - 1)^2 = 0
(equivalently 2*(T_11(x/2) + 1) = (x+2)*(x^5 - x^4 - 4x^3 + 3x^2 + 3x - 1)^2).
Since x = 2 cos(pi/11) > 0 we have x + 2 > 0, so the quintic factor vanishes,
hence the quintic itself is 0 (the square is 0).

You may instead use any other valid route. Return a complete sorry-free Lean 4
proof of the lemma. Name it lambda_11_min_poly.
