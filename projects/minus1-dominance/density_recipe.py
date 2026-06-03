"""
RS limiting distribution and the density delta(N; -1, a).

SETUP (Rubinstein-Sarnak 1994).  For modulus q, the normalized error vector
E(x) = (E_a(x))_a, indexed by residue classes a coprime to q, with

  E_a(x) = (log x / sqrt(x)) ( phi(q) pi(x;q,a) - pi(x) ).

Under GRH (all L(s,chi) zeros on Re=1/2) and the Linear Independence hypothesis
LI (the positive imaginary parts gamma_chi of zeros, over all chi mod q, are
linearly independent over Q), E(x) has a limiting logarithmic distribution that
equals the distribution of the random vector

  X_a = -C(q,a) + sum_{chi != chi0} chi(a) * Z_chi,        (RS, "explicit-formula" form)

where
  C(q,a) = -1 + #{ b mod q : b^2 = a (mod q) }     (= the MEAN of E_a; note E[X_a]=-C),
  and for each chi != chi0,
     Z_chi = 2 sum_{gamma_chi > 0} ( Re or sin combination ) / sqrt(1/4+gamma^2) * (random phase),
  realized concretely as a sum of independent random variables, one per zero pair:

     Z_chi = sum_{gamma>0} (2 / sqrt(1/4+gamma^2)) * Re( chi-phase * e^{i theta_gamma} )

  with theta_gamma i.i.d. Uniform(0,2pi) (this is the LI consequence: the
  values gamma log x mod 2pi equidistribute independently).

The DIFFERENCE that governs the a-vs-1 race is
  D_a := X_a - X_1 = -(C(q,a) - C(q,1)) + sum_{chi!=chi0} (chi(a)-chi(1)) Z_chi
                   = (C(q,1) - C(q,a)) -- wait sign; E[D_a]=E[X_a]-E[X_1].
Since C(q,1) = -1 + #sqrt(1)  (large, = number of square roots of 1), and
C(q,a)=-1 for non-residue a, we have E[X_a]-E[X_1] = -C(q,a)+C(q,1)
   = -(-1) + (-1+#sqrt(1)) = #sqrt(1) -... let's just compute with the mean
   mu_a := E[X_a] = -1 + #sqrt(a)   (the value printed by verify_mean.py).
So mu_a - mu_1 = #sqrt(a) - #sqrt(1) = (0 for NR) - (#sqrt of 1) < 0.
The race D(x;q,a)=pi(x;q,a)-pi(x;q,1): note E_a - E_1 = (log x/sqrt x) phi(q)(pi(x;q,a)-pi(x;q,1)),
so sign(D(x;q,a)) = sign(X_a - X_1).  Thus

  delta(q; a, 1) := log-density{ x : pi(x;q,a) > pi(x;q,1) } = P( X_a > X_1 ) = P(D_a > 0).

THE COVARIANCE (the real discriminant among NR).  Var/Cov of the X-vector:
  Cov(X_a, X_b) = sum_{chi != chi0} c_chi * conj(chi(a)) chi(b),   c_chi = sum_gamma 1/(1/4+gamma^2).
(Each Z_chi has variance c_chi; Z_chi and Z_{chi'} independent for chi'!=chi, chi'!=conj chi;
 the conj-pairing makes the real vector's covariance the Hermitian form above.)
This is the B(N;a,b) in the task statement.

=> Var(D_a) = Cov(X_a,X_a)+Cov(X_1,X_1)-2Re Cov(X_a,X_1)
            = sum_chi c_chi ( |chi(a)-chi(1)|^2 )   [since chi(1)=1]
            = sum_chi c_chi |chi(a)-1|^2.

This file: assemble Cov from c_chi values (computed elsewhere) and produce
delta via the characteristic function (RS Fourier method), NOT a Gaussian.
"""
print("recipe documented; computation engine in delta_compute.py")
