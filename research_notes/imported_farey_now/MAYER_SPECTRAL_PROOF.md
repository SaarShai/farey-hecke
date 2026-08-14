# Mayer Transfer Operator and Spectral Proof of the Sign Theorem

## Status: EXPLORATORY RESEARCH -- Mostly Speculative

**Date:** 2026-03-28
**Classification:** C1 (collaborative, minor novelty) -- connects known frameworks, no new theorems
**Verification status:** Unverified -- this is a research direction, not a claimed result

---

## 1. Executive Summary

This document investigates whether the Mayer transfer operator framework can provide a spectral proof of our Sign Theorem (that Delta_W(p) < 0 for all primes p >= 11). The short answer: **there is no clean path from Mayer's framework to our Sign Theorem, but there are suggestive structural parallels that deserve further study.** The honest assessment is that the existing literature connects Farey sequences to spectral theory primarily through equidistribution and the Riemann Hypothesis, not through the kind of prime-by-prime monotonicity statement our Sign Theorem requires.

---

## 2. The Mayer Transfer Operator: What It Actually Is

### 2.1 Definition

The **Gauss map** T: [0,1] -> [0,1] is defined by T(x) = {1/x} (fractional part of 1/x). Its **transfer operator** (Ruelle-Mayer operator) is:

    (L_s f)(x) = sum_{n=1}^{infty} 1/(n+x)^{2s} * f(1/(n+x))

for Re(s) > 1/2, acting on a Banach space of holomorphic functions on a disk containing [0,1].

### 2.2 The Farey Map Variant

The **Farey map** F: [0,1] -> [0,1] is the "slow" version of the Gauss map:

    F(x) = x/(1-x)     if x in [0, 1/2]
    F(x) = (1-x)/x     if x in [1/2, 1]

Its transfer operator P acts on function spaces and has been studied by Isola, Bonanno, and others. The Farey map has a neutral fixed point at 0, making it a model of intermittency -- this causes the spectral theory to be more delicate than for uniformly expanding maps.

### 2.3 Mayer's Central Result

**Theorem (Mayer, 1990-1991):** The Selberg zeta function Z(s) for PSL(2,Z)\H can be expressed as:

    Z(s) = det(I - L_s) * det(I + L_s)

where L_s is the transfer operator of the Gauss map. The zeros of Z(s) occur at values where L_s has eigenvalue +1 (from the first factor) or -1 (from the second factor).

### 2.4 Connection to the Riemann Zeta Function

The Selberg zeta function for PSL(2,Z) is related to the Riemann zeta function through:
- The eigenvalues of the Laplacian on PSL(2,Z)\H (Maass cusp forms)
- The Eisenstein series E(z,s), whose spectral parameter s connects to zeta(2s)

**Zagier's result:** Setting s = rho (a nontrivial zero of zeta) in the Eisenstein series E(z,s) produces functions with remarkable properties. The spectrum of a certain representation of SL_2(R) contains rho(1-rho) discretely with multiplicity >= n if rho is an n-fold zero of zeta(s).

**IMPORTANT:** The oft-cited claim "det(I - L_s) = zeta(s)/zeta(s+1)" does NOT appear in the literature in this form. What is true is that the *matrix elements* of L_s involve the Riemann zeta function (via sums of (zeta(k+m+2s) - 1) terms), and the Selberg zeta function (expressed as det(I - L_s)) has zeros related to the eigenvalues of the Laplacian, which in turn connect to the Riemann zeta through the Selberg trace formula. The connection is real but indirect.

---

## 3. Spectrum of the Farey Transfer Operator

### 3.1 Isola's Results (2002)

**Theorem (Isola, 2002):** The transfer operator P of the Farey map, acting on a suitable Hilbert space of holomorphic functions (defined via generalized Borel transforms), has:

- **Continuous spectrum:** The interval [0, 1]
- **Embedded eigenvalues:** 0 and 1
- **Additional eigenvalues:** A finite or countably infinite set of eigenvalues of finite multiplicity

The presence of continuous spectrum on [0,1] is a direct consequence of the neutral fixed point at x = 0.

### 3.2 Bonanno-Graffi-Isola (2008)

**Theorem:** A one-parameter family of *signed* transfer operators (parametrized by a real number beta) associated to the Farey map, when acting on a Hilbert space of analytic functions, are:
- **Self-adjoint**
- Have **absolutely continuous spectrum**
- Have **no non-zero point spectrum** (generically)
- Have **polynomial eigenfunctions** when beta is a negative half-integer

### 3.3 Induced Operator and the Gauss Map

There is a precise relationship between the Farey and Gauss transfer operators via *inducing*. Let Q_z be the induced operator of the Farey map. Then:

    1 is an eigenvalue of Q_z  <=>  z^{-1} is an eigenvalue of both P and its dual P~

with the same geometric multiplicity. The zeta function of the Farey map extends meromorphically to C \ [1, infinity).

---

## 4. The Franel-Landau Connection: What We Actually Know

### 4.1 The L2 Franel Identity

For the Farey sequence F_N of order N with |F_N| = Phi(N) terms, define discrepancies:

    d_{k,N} = a_{k,N} - k/Phi(N)

where a_{k,N} is the k-th Farey fraction. Then:

**Franel-Landau Theorem (1924):**

    RH <=> sum_{k=1}^{Phi(N)} d_{k,N}^2 = O(N^r) for all r > -1

    RH <=> sum_{k=1}^{Phi(N)} |d_{k,N}| = O(N^r) for all r > 1/2

### 4.2 Connection to Mertens Function

The crucial formula is:

    M(N) = -1 + sum_{a in F_N} e^{2*pi*i*a}

where M(N) = sum_{n<=N} mu(n) is the Mertens function. This is used in proving the Franel-Landau theorem.

### 4.3 Our W_N in This Framework

Our wobble statistic is:

    W_N = (1/|F_N|^2) * sum_{f in F_N} D(f)^2

where D(f) = rank(f, F_N) - |F_N|*f. This is related to but not identical to the Franel sum. Specifically:

    D(f) = rank(f) - |F_N|*f
    d_{k,N} = f_k - k/|F_N|

These are related by D(f_k) = k - |F_N|*f_k = -|F_N| * d_{k,N}, so:

    **W_N = sum d_{k,N}^2**

(up to normalization). This means W_N IS the L2 Franel sum (normalized). The Franel-Landau theorem directly says RH controls the growth rate of W_N.

### 4.4 Modern Generalization (Karvonen-Zhigljavsky, 2025)

A large class of positive-semidefinite kernels K has been identified for which:

    MMD_K(F_N)^2 = O(N^{-3/2+epsilon}) <=> RH

where MMD is the Maximum Mean Discrepancy. This includes Matern kernels of order >= 1/2. Our W_N is essentially the MMD for the flat kernel on [0,1].

---

## 5. Can W_N Be Written as a Spectral Sum?

### 5.1 The Spectral Decomposition of L2 on the Modular Surface

The key spectral decomposition is:

    L^2(PSL(2,Z)\H) = C (constants) + L^2_cusp (cusp forms) + L^2_cont (Eisenstein)

where:
- **Cusp forms:** Maass cusp forms u_j with eigenvalues lambda_j = s_j(1-s_j), s_j = 1/2 + it_j
- **Continuous spectrum:** Eisenstein series E(z,1/2+it) for t in R, forming the continuous part of the spectrum starting at lambda = 1/4

### 5.2 The Horocycle Flow Connection

**Athreya-Cheung (2014):** The BCZ map (Boca-Cobeli-Zaharescu map) arises as a Poincare section of the horocycle flow on SL(2,R)/SL(2,Z). This map encodes the transition F_{N-1} -> F_N.

**Key insight:** The distribution of Farey fractions is controlled by the equidistribution of horocycle orbits on the modular surface. The RATE of equidistribution is determined by the spectral gap.

### 5.3 Spectral Gap and Equidistribution Rates

For the modular surface PSL(2,Z)\H:
- The first nonzero eigenvalue of the Laplacian is lambda_1 ~ 91.14... (very large spectral gap)
- By Sarnak (1981), the rate of equidistribution of periodic horocycles depends on the spectral parameters of Maass forms and the behavior of Eisenstein series

**Effective equidistribution (Flaminio-Forni-Tanis, 2016):** The rate of equidistribution for horocycle flows is determined by the spectral decomposition of test functions against the eigenbasis of the Laplacian. For a test function phi:

    (1/T) integral_0^T phi(h_t * x) dt = <phi, 1> + sum_j c_j(x) * T^{s_j - 1} + integral c_t(x) * T^{it-1/2} dmu(t) + ...

where the sum is over Maass cusp forms and the integral is over the Eisenstein contribution.

### 5.4 Attempting to Express W_N Spectrally

**Speculative framework (NOT established in the literature):**

If we could lift the Farey discrepancy to a function on PSL(2,Z)\H and apply the spectral decomposition, we would get:

    W_N ~ sum_j |<D_N, u_j>|^2 + integral |<D_N, E(.,1/2+it)>|^2 dt

where the inner products are computed via the horocycle-Farey correspondence. The growth of W_N would then be controlled by:
1. How fast the cusp form coefficients <D_N, u_j> grow with N
2. The Eisenstein contribution, which involves zeta(1/2+it) through the Fourier coefficients

**HONESTY CHECK:** This spectral decomposition of W_N has NOT been carried out in the literature. It is a plausible program but not an established result.

---

## 6. Can the Sign Theorem Follow from Spectral Monotonicity?

### 6.1 What We Would Need

For a spectral proof of Delta_W(p) < 0 for primes p >= 11, we would need to show that when N increases through a prime p:

    W_p > W_{p-1}

In spectral terms, this would require showing that the "spectral energy" of the discrepancy function increases at every prime step.

### 6.2 The Fundamental Obstacle

**The core difficulty:** The Mayer/horocycle framework gives *asymptotic* information about the distribution of Farey fractions (equidistribution rates as N -> infinity). Our Sign Theorem is a *pointwise* statement about what happens at each individual prime p.

The spectral decomposition gives us:
- Long-range asymptotics: W_N grows like N^{1+epsilon} under RH (from Franel-Landau)
- The rate is controlled by the spectral gap and zeta zeros

But it does NOT directly give:
- The sign of Delta_W(p) for individual primes
- Why primes specifically cause wobble to increase
- The role of the Mertens function M(p) in determining the sign

### 6.3 A Possible Spectral Monotonicity Argument (Highly Speculative)

**Sketch of an approach that MIGHT work but is NOT proven:**

1. The transition F_{p-1} -> F_p adds Phi(p) = p-1 new fractions (all a/p with gcd(a,p)=1)
2. Via the BCZ map / horocycle correspondence, this corresponds to a specific horocycle segment on the modular surface
3. The "new energy" contributed by these p-1 fractions could potentially be expressed as:

    Delta_W(p) = (something involving the p-th Hecke eigenvalues of Maass forms)

4. If the Hecke eigenvalues have a definite sign property at primes (which they do NOT in general -- this is the problem), then monotonicity would follow.

**Why this probably fails:** Hecke eigenvalues a_p(u_j) for Maass cusp forms satisfy the Ramanujan-Petersson bound |a_p| <= 2*p^{-1/2} but do NOT have definite sign. The Sato-Tate distribution governs them, and they oscillate. So a direct Hecke eigenvalue argument will not yield a sign theorem.

### 6.4 The Perturbation Theory Approach (Also Speculative)

When N increases by 1, the transfer operator changes. One could try:

    L_{s,N+1} = L_{s,N} + delta_L

and use perturbation theory (resolvent expansion) to track how eigenvalues move. The difficulty is:
- L_s is defined for the Gauss/Farey map, which is independent of N
- The N-dependence enters through the Farey sequence itself, not the map
- There is no natural "family of operators parametrized by N"

**Assessment:** The Mayer transfer operator does not naturally parametrize by N, so perturbation theory does not directly apply.

---

## 7. What Boca-Cobeli-Zaharescu Pair Correlation Implies

### 7.1 Their Main Results

**Theorem (Boca-Zaharescu, 2005):** All correlations of Farey fractions exist. The k-point correlation measures have explicit formulas.

**Theorem (BCZ, 2001):** The limiting gap distribution of Farey fractions exists and is given by an explicit formula involving the BCZ map.

### 7.2 Implications for W_N

The pair correlation of Farey fractions converges to a specific limit related to the hyperbolic geometry of PSL(2,Z)\H. This limit is NOT the GUE sine kernel (despite suggestive parallels with random matrix theory). It is instead related to the Hall distribution.

**What this tells us about W_N:**
- The pair correlation controls the *variance* of D(f), which is the main contribution to W_N
- The existence of a limiting correlation means W_N/|F_N| converges to a specific limit
- But this is an asymptotic statement -- it does not immediately yield the sign of Delta_W(p)

### 7.3 The BCZ Map as Poincare Section

The BCZ map was shown by Athreya-Cheung (2014) to be a Poincare section of the horocycle flow. This means:
- The dynamics of F_{N-1} -> F_N is literally a discrete time step of the horocycle flow
- The ergodic properties of the BCZ map (recently shown to be weakly mixing, 2024) control the long-time behavior
- But again, these are asymptotic/ergodic results, not individual prime-step results

---

## 8. The Zagier Representation and Zeta Zeros

### 8.1 Zagier's Key Observation

Zagier showed that setting s = rho (a zeta zero) in the Eisenstein series E(z,s) produces functions that satisfy remarkable identities. The spectrum of a representation of SL_2(R) naturally associated to the modular surface contains rho(1-rho) discretely.

### 8.2 Relevance to W_N

If W_N could be expressed as a spectral integral involving E(z,s), then the poles/zeros of zeta would contribute via residues:

    W_N ~ main_term + sum_{rho} (contribution from zeta zero rho)

The sum over zeta zeros would oscillate, and the growth of W_N would be controlled by the location of zeros (i.e., by RH). This is essentially what the Franel-Landau theorem says in different language.

### 8.3 But Not the Sign Theorem

Even with a spectral decomposition over zeta zeros, the sign of Delta_W(p) at individual primes would require understanding the PHASES of the zero contributions at that particular prime. This is equivalent to understanding the distribution of Im(rho)*log(p) mod 2*pi, which is precisely the kind of thing that is extremely hard in analytic number theory.

---

## 9. The Lewis-Zagier Period Function Connection

### 9.1 The Three-Term Functional Equation

The Lewis-Zagier theory shows that Maass cusp forms u_j with spectral parameter s are in 1-1 correspondence with period functions psi(z) satisfying:

    psi(z) = psi(z+1) + (z+1)^{-2s} * psi(z/(z+1))

This is the three-term functional equation. Its solutions are eigenfunctions of the Mayer transfer operator L_s with eigenvalue 1.

### 9.2 Series Expansions from the Farey Map (Bonanno-Isola-Knauf Framework)

Recent work (arXiv:1607.03414, Bruggeman-Lewis-Zagier) obtained new series expansions for Maass cusp forms and Eisenstein series using the inverse of the Lewis-Zagier integral transform, working directly with the Farey transfer operator. This gives explicit formulas:

- For Maass cusp forms restricted to the imaginary axis
- For Eisenstein series restricted to the imaginary axis
- New series for the divisor function

### 9.3 Potential Relevance

The Farey transfer operator encodes the same information as Maass forms. If we could express D(f) for Farey fractions in terms of the period functions psi(z), then W_N = sum D(f)^2 could potentially be decomposed using the completeness of the period function basis. This would give a spectral decomposition of W_N.

**However:** This program has not been carried out, and it is unclear whether the period function basis is "complete" in the right sense for decomposing W_N.

---

## 10. Synthesis: An Honest Assessment

### 10.1 What Is Rigorous

1. **W_N = (normalized) Franel L2 sum.** Our wobble is the classical Franel sum up to normalization.

2. **RH controls the growth of W_N.** By Franel-Landau, sum d_{k,N}^2 = O(N^{-1+epsilon}) iff RH.

3. **The Mayer transfer operator encodes the spectral data of PSL(2,Z)\H.** The Selberg zeta function Z(s) = det(I - L_s)*det(I + L_s), and its zeros correspond to Maass eigenvalues.

4. **The BCZ map is a Poincare section of horocycle flow.** The transition F_{N-1} -> F_N is a step in the horocycle dynamics.

5. **The rate of equidistribution of Farey fractions is controlled by the spectral gap.** Effective equidistribution results (Flaminio-Forni-Tanis) give explicit rates.

### 10.2 What Is Suggestive but Not Proven

1. **W_N should have a spectral decomposition** in terms of Maass cusp forms and Eisenstein series, via the horocycle connection. This is a natural program but has not been carried out.

2. **The growth of W_N is controlled by zeta zeros** through the Eisenstein contribution to the spectral decomposition. This is essentially Franel-Landau rephrased spectrally.

3. **The prime-step behavior Delta_W(p) might be related to Hecke eigenvalues** of Maass cusp forms at the prime p. This is speculative.

### 10.3 What Is Almost Certainly NOT True

1. **A clean spectral monotonicity argument for the Sign Theorem.** The Hecke eigenvalues oscillate (Sato-Tate), so there is no "monotone increase of the leading eigenvalue through primes."

2. **A direct perturbation theory argument.** The Mayer transfer operator does not parametrize by N.

3. **The pair correlation / BCZ results implying the Sign Theorem.** These are asymptotic results about the limiting distribution, not about individual prime steps.

### 10.4 The Gap Between Franel-Landau and the Sign Theorem

The Franel-Landau theorem says: W_N grows (on average) like N^{1+epsilon} under RH.

The Sign Theorem says: W_N increases at EVERY prime step (not just on average).

The gap between "grows on average" and "increases at every prime step" is enormous. This is analogous to the gap between the Prime Number Theorem (primes have density ~1/log(N)) and Bertrand's Postulate (there is a prime between N and 2N). The former follows from spectral methods; the latter requires elementary but clever arguments.

**Assessment:** A spectral proof of the Sign Theorem would likely require understanding cancellations among zeta zero contributions at individual primes, which is a problem of comparable difficulty to understanding short-interval prime counts. This is not a tractable path with current technology.

---

## 11. Most Promising Direction

If one insists on pursuing a spectral/operator-theoretic proof, the most promising approach would be:

### 11.1 The BCZ Map Approach

1. Express Delta_W(p) in terms of the BCZ map dynamics
2. The BCZ map step at a prime p has specific geometric meaning (adding a full row of fractions a/p)
3. Use the weak mixing of the BCZ map (recently proven, 2024) to show that the "energy" injected by a prime step is positive

### 11.2 Why This Might Work

- The BCZ map directly encodes F_{N-1} -> F_N transitions
- The weak mixing property means correlations decay, which could imply the injected fractions always increase variance
- The horocycle equidistribution gives quantitative control

### 11.3 Why This Still Faces Obstacles

- Weak mixing is an asymptotic property; we need a statement for each individual prime
- The "energy injection" needs to be positive, not just non-negative on average
- Small primes (p = 11, 13, ...) may not be in the "asymptotic regime"

---

## 12. Key References

### Mayer Transfer Operator
- Mayer, D. "On the Thermodynamic Formalism for the Gauss Map," Commun. Math. Phys. 130 (1990), 311-333.
- Mayer, D. "The thermodynamic formalism approach to Selberg's zeta function for PSL(2,Z)," Bull. AMS 25(1) (1991), 55-60.
- Chang & Mayer, "The Transfer Operator Approach to Selberg's Zeta Function," IMA Vol. 109 (1999).

### Spectrum of the Farey Transfer Operator
- Isola, S. "On the spectrum of Farey and Gauss maps," Nonlinearity 15 (2002), 1521-1539.
- Bonanno, Graffi, Isola, "Spectral analysis of transfer operators associated to Farey fractions," Atti Accad. Naz. Lincei 19 (2008).

### Lewis-Zagier Period Functions
- Lewis, J. & Zagier, D. "Period Functions for Maass Wave Forms. I," Ann. Math. 153(1) (2001), 191-258.
- Bruggeman, Lewis & Zagier, "Period Functions for Maass Wave Forms and Cohomology."
- arXiv:1607.03414: Series expansions for Maass forms from Farey transfer operators.

### BCZ Map and Horocycle Flow
- Boca, Cobeli, Zaharescu, "A conjecture of R.R. Hall on Farey points," J. Reine Angew. Math. 535 (2001), 207-236.
- Boca & Zaharescu, "The correlations of Farey fractions," J. London Math. Soc. 72(1) (2005), 25-39.
- Athreya & Cheung, "A Poincare section for horocycle flow on the space of lattices," IMRN (2014).
- arXiv:2403.14976: BCZ map is weakly mixing (2024).

### Equidistribution and Spectral Theory
- Sarnak, P. "Asymptotic behavior of periodic orbits of the horocycle flow and Eisenstein series," Comm. Pure Appl. Math. 34 (1981), 719-739.
- Flaminio, Forni & Tanis, "Effective equidistribution of twisted horocycle flows," GAFA (2016).
- Zagier, D. "Eisenstein Series and the Riemann Zeta-Function."

### Farey Discrepancy and RH
- Franel, J. "Les suites de Farey et le probleme des nombres premiers," Gott. Nachr. (1924), 198-201.
- Kanemitsu & Yoshimoto, "Farey series and the Riemann hypothesis," Acta Arith. 75 (1996), 351-374.
- Karvonen & Zhigljavsky, "Maximum mean discrepancies of Farey sequences," Acta Math. Hungar. (2025).

### Phase Transitions and Generalized Farey Dynamics
- Degli Esposti, Isola, Knauf, "Generalized Farey Trees, Transfer Operators and Phase Transitions," Commun. Math. Phys. 275 (2007).

---

## 13. Conclusions and Recommendations

### Bottom Line

The Mayer transfer operator framework is deeply connected to Farey sequences through:
1. The Selberg zeta function (Mayer's det formula)
2. Period functions (Lewis-Zagier correspondence with Maass forms)
3. The horocycle flow (BCZ map as Poincare section)

However, **none of these connections directly yield a proof of the Sign Theorem.** The fundamental problem is that spectral methods give asymptotic/average information, while the Sign Theorem is a pointwise statement about individual primes.

### What To Do Next

1. **DO NOT pursue** a direct spectral proof of the Sign Theorem via Mayer operators. The gap is too large.

2. **DO consider** whether the BCZ map / horocycle framework can give insight into the *mechanism* of why primes increase wobble. The geometric picture (adding a full row of fractions a/p corresponds to a specific horocycle segment) might yield intuition even if not a proof.

3. **DO note** that W_N = Franel L2 sum (up to normalization). This is a known and important object. Any prior results on the Franel sum apply directly to our W_N.

4. **DO investigate** whether the Karvonen-Zhigljavsky kernel framework (2025) gives new information about the prime-step behavior of W_N when specialized to specific kernels.

5. **The most honest path to the Sign Theorem remains our arithmetic/algebraic approach** (the four-term decomposition, the B+C geometric identity, the M(p) correlation). The spectral framework is beautiful context but not a proof tool for this specific result.
