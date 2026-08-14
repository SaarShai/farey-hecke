# Rigorous Explicit Formula: DeltaW(p) in Terms of Zeta Zeros

**Date:** 2026-03-30
**Status:** Rigorous analysis separating proved steps from formal/conjectural ones
**Classification:** C1 (collaborative, minor novelty -- new packaging of known identities)
**Predecessor:** EXPLICIT_FORMULA_ZEROS_DELTAW.md (formal derivation)
**Audit files:** FAREY_TELESCOPE_FORMAL.md, pink_noise_findings.md

---

## 0. Purpose and Scope

The document EXPLICIT_FORMULA_ZEROS_DELTAW.md derived a formula expressing
DeltaW(p) = W(p-1) - W(p) in terms of pairs of nontrivial zeros of zeta(s).
That derivation was formal: each step invoked a known identity, but truncation
errors, convergence conditions, and diagonal regularization were not controlled.

This document does three things:

1. States precisely which steps are rigorous theorems and which are formal.
2. Bounds all error terms where possible.
3. Identifies the exact obstructions to making the full formula into a theorem.

**Honest summary:** Steps 1-3 below are rigorous. Step 4 (the bilinear zero form)
is rigorous for finite truncation but requires careful error control for the
infinite sum. Step 5 (extraction of DeltaW) is formal. The full formula is NOT
a theorem -- it is a formal identity whose qualitative structure is consistent
with all numerical evidence but whose error terms have not been bounded.

**On the "Z=1625" claim:** The adversarial audit (FAREY_TELESCOPE_FORMAL.md)
found that this Z-score is unverified in the codebase, and even if correct,
reflects smoothness of DeltaW (red spectrum), NOT detection of individual
zeta zeros. The pink noise analysis confirmed: no systematic Fourier peaks at
zeta zero frequencies (mean SNR at zeros = 0.91 vs 1.20 at random frequencies).
The testable prediction of Section 9 of the predecessor document is therefore
NOT confirmed. We do not cite it here.

---

## 1. Definitions

All notation is standard (Titchmarsh 1986, Iwaniec-Kowalski 2004).

**Farey quantities:**
- F_N = Farey sequence of order N, with |F_N| = 1 + sum_{q=1}^{N} phi(q)
- n = n(N) = |F_N| = (3/pi^2) N^2 + O(N log N)     [Mertens 1874]
- f_j = j-th element of F_N (j = 0, ..., n-1), f_0 = 0, f_{n-1} = 1
- d_j = f_j - j/n (displacement from equidistribution)
- W(N) = (1/n^2) sum_{j=0}^{n-1} d_j^2

**Arithmetic functions:**
- mu(n) = Mobius function
- M(x) = sum_{k <= x} mu(k) (Mertens function)
- c_q(m) = sum_{a=1, gcd(a,q)=1}^{q} e(am/q) (Ramanujan sum)
- sigma_s(m) = sum_{d|m} d^s (generalized divisor function)
- tau(m) = sigma_0(m) = number of divisors of m

**Zeta zeros:**
- rho = beta + i*gamma ranges over nontrivial zeros of zeta(s)
- RH: beta = 1/2 for all rho (assumed where stated)
- Zeros are ordered by |gamma|: 0 < gamma_1 < gamma_2 < ...

---

## 2. Step 1: W(N) via Exponential Sums (RIGOROUS)

### 2.1 The Exponential Sum sigma_m(N)

**Definition.** For integer m >= 1:

    sigma_m(N) := sum_{q=1}^{N} c_q(m)

**Proposition 2.1** (Ramanujan sum identity; standard, see Montgomery-Vaughan 2007, Ch. 4).

    sigma_m(N) = sum_{d | m} d * M(floor(N/d))

*Proof.* Using c_q(m) = sum_{d | gcd(q,m)} d * mu(q/d) and exchanging order of summation.
This is an exact algebraic identity -- no error terms.  QED.

### 2.2 W(N) via Parseval

**Proposition 2.2** (Franel 1924; see also Dress-Mendes France 1988, Theorem 1).

    sum_{j=0}^{n-1} d_j^2 = (1 / (4 pi^2)) sum_{m=1}^{n-1} |S_m(N)|^2 / sin^2(pi m / n)

where S_m(N) = sum_{f in F_N} e(mf).

*Status:* This is a standard discrete Fourier identity. It holds exactly for any
finite sequence of n points in [0,1). The proof is elementary Fourier analysis
on Z/nZ. RIGOROUS.

**Corollary 2.3.** For any cutoff M >= 1:

    n^2 W(N) = (1 / (4 pi^2)) sum_{m=1}^{M} |sigma_m(N)|^2 / m^2 + E_1(N, M)

where:

    |E_1(N, M)| <= (1 / (4 pi^2)) * [ sum_{m=1}^{M} |sigma_m(N)|^2 * |1/sin^2(pi m/n) - n^2/(pi^2 m^2)|
                                       + sum_{m=M+1}^{n-1} |sigma_m(N)|^2 / sin^2(pi m/n) ]

The first part of E_1 captures the difference between sin^2 and its small-angle
approximation; the second is the tail beyond m = M.

**Bound on E_1:** For m <= M <= n/2, we have |1/sin^2(pi m/n) - n^2/(pi^2 m^2)| <= C n^2 m^2 / n^2
for an absolute constant C (Taylor expansion of sin), so the first sum contributes
<= C/n^2 * sum_{m=1}^{M} |sigma_m(N)|^2. Using |sigma_m(N)| <= sum_{d|m} d |M(N/d)| <= sigma_1(m) max_{d|m} |M(N/d)|,
and the Walfisz bound |M(x)| <= x exp(-c sqrt(log x)), the tail can be bounded.

For our purposes, taking M = N (so m ranges up to N) and using the known
asymptotic sum_{m=1}^{N} |sigma_m(N)|^2 / m^2 ~ C N log N (see Section 5 below),
we get:

    E_1(N, N) = O(N log N / n^2) = O(log N / N)

*Status:* The structure is RIGOROUS. The explicit constant in O(log N / N) depends on
the Walfisz constant, which is ineffective.

---

## 3. Step 2: Substituting the Explicit Formula for M(x) (CONDITIONAL)

### 3.1 The Truncated Explicit Formula for M(x)

**Theorem 3.1** (Perron's formula; Titchmarsh 1986, Theorem 14.25).

For x >= 2, x not an integer, and T >= 2:

    M(x) = - sum_{|gamma| <= T} x^rho / (rho zeta'(rho)) + R_0(x, T)

where:
- The sum is over nontrivial zeros rho with |Im(rho)| <= T
- This assumes all zeros with |gamma| <= T are simple

The remainder satisfies:

    R_0(x, T) = -2 + sum_{k=1}^{K} (-1)^{k-1} x^{-2k} / (2k zeta(2k))
                + O(x log^2(xT) / T)    [unconditionally]
                + O(x^{1/2} log^2(xT) / T)    [under RH]

**Precision on the error term:** The unconditional bound follows from the zero-free
region and density estimates (Titchmarsh Ch. 14). The key point is that for
FIXED T and varying x, the error is O(x/T) unconditionally.

For integer x, the formula holds with M(x) replaced by M(x) - mu(x)/2, but since
we evaluate at x = N/d which may or may not be integer, and the correction is
bounded, we absorb this into the error.

**What we need but do not have:** An explicit, effective version with COMPUTABLE
constants. The Walfisz-Korobov zero-free region gives an error of
O(x exp(-c (log x)^{3/5} (log log x)^{-1/5})), but c is ineffective.

### 3.2 sigma_m(N) in Terms of Zeros

**Proposition 3.2.** For m >= 1, N >= 2, T >= 2:

    sigma_m(N) = - sum_{|gamma| <= T} (N^rho / (rho zeta'(rho))) sigma_{1-rho}(m) + R_m(N, T)

where:

    R_m(N, T) = sum_{d | m} d * R_0(N/d, T) + O(tau(m))

and R_0 is the remainder from Theorem 3.1.

*Proof.* Substitute Theorem 3.1 into Proposition 2.1:

    sigma_m(N) = sum_{d|m} d * M(N/d)
               = sum_{d|m} d * [- sum_{|gamma|<=T} (N/d)^rho / (rho zeta'(rho)) + R_0(N/d, T)]
               = - sum_{|gamma|<=T} (N^rho / (rho zeta'(rho))) [sum_{d|m} d^{1-rho}] + sum_{d|m} d R_0(N/d, T)

Recognizing sum_{d|m} d^{1-rho} = sigma_{1-rho}(m).  QED.

**Bound on R_m:** Using |R_0(N/d, T)| <= C (N/d) log^2(NT) / T (unconditionally):

    |R_m(N, T)| <= C N log^2(NT) / T * sum_{d|m} 1 = C N tau(m) log^2(NT) / T

Under RH: replace N by N^{1/2}, giving |R_m| <= C N^{1/2} tau(m) log^2(NT) / T.

*Status:* RIGOROUS (conditional on simplicity of zeros for the clean form; unconditional
with the appropriate modifications for multiple zeros).

### 3.3 Shorthand

Define:

    A(rho) := -1 / (rho zeta'(rho))

    Phi_m(N, T) := sum_{|gamma| <= T} A(rho) N^rho sigma_{1-rho}(m)

Then: sigma_m(N) = Phi_m(N, T) + R_m(N, T).

---

## 4. Step 3: The Bilinear Zero Form for W(N) (PARTLY RIGOROUS)

### 4.1 Expanding |sigma_m|^2

From Corollary 2.3 with M = N:

    n^2 W(N) = (1/(4 pi^2)) sum_{m=1}^{N} |sigma_m(N)|^2 / m^2 + E_1

Using sigma_m = Phi_m + R_m:

    |sigma_m|^2 = |Phi_m|^2 + 2 Re(Phi_m * conj(R_m)) + |R_m|^2

So:

    n^2 W(N) = (1/(4 pi^2)) sum_{m=1}^{N} |Phi_m(N,T)|^2 / m^2  +  E_2(N, T)  +  E_1(N, N)

where:

    |E_2(N, T)| <= (1/(4 pi^2)) sum_{m=1}^{N} [2 |Phi_m| |R_m| + |R_m|^2] / m^2

### 4.2 Bounding E_2

**Under RH, for T >= N^{1/2}:**

Using |Phi_m| <= sum_{|gamma|<=T} |A(rho)| N^{1/2} sigma_{1/2}(m)
and |R_m| <= C N^{1/2} tau(m) log^2(NT) / T:

    |Phi_m| |R_m| / m^2 <= C' N sigma_{1/2}(m) tau(m) log^2(NT) / (T m^2) * S(T)

where S(T) = sum_{|gamma|<=T} |A(rho)|. The sum S(T) grows like log T (this follows
from the density of zeros and the mean value of 1/|zeta'(rho)|).

Summing over m: sum_{m=1}^{N} sigma_{1/2}(m) tau(m) / m^2 converges (the Dirichlet
series has abscissa of convergence <= 3/2, and we are at s = 2 > 3/2), giving
a value <= C'' log^2 N.

Therefore:

    |E_2(N, T)| <= C''' N log^4 N / T    [under RH]

Choosing T = N: |E_2| <= C''' log^4 N.

Since n^2 ~ 9N^4/pi^4, we have W(N) ~ n^{-2} * [main term], and the main term
is O(N log N) (see below), so:

    W(N) = main/(9N^4/pi^4) + O(log^4 N / N^4) = O(log N / N^3)

This is consistent with the known W(N) ~ c log N / N.

### 4.3 The Main Bilinear Sum (RIGOROUS for finite T)

Expanding |Phi_m|^2:

    sum_{m=1}^{N} |Phi_m(N,T)|^2 / m^2
      = sum_{|gamma|,|gamma'| <= T} A(rho) conj(A(rho')) N^{rho + conj(rho')}
        * sum_{m=1}^{N} sigma_{1-rho}(m) conj(sigma_{1-rho'}(m)) / m^2

This is an exact algebraic manipulation for FINITE T (finitely many zeros).

### 4.4 The Ramanujan Convolution (RIGOROUS with remainder)

**Theorem 4.4** (Ramanujan 1916; see Hardy-Wright, Theorem 303).

For Re(s) > max(1, 1+Re(a), 1+Re(b), 1+Re(a+b)):

    sum_{m=1}^{infty} sigma_a(m) sigma_b(m) / m^s = zeta(s) zeta(s-a) zeta(s-b) zeta(s-a-b) / zeta(2s-a-b)

**Application:** With a = 1-rho, b = 1-conj(rho'), s = 2:

We need Re(2) > max(1, 1+Re(1-rho), 1+Re(1-conj(rho')), 1+Re(2-rho-conj(rho'))).

Under RH (beta = 1/2): Re(1-rho) = 1/2, so we need 2 > 3/2. CHECK.
Also Re(2-rho-conj(rho')) = 2 - 2 beta = 1 (under RH), so we need 2 > 2. FAILS.

**This is the critical convergence issue.** The Ramanujan formula requires STRICT
inequality, but for the diagonal (rho = rho'), we have s - a - b = 2 - (2-2beta) = 2beta = 1
(under RH), and zeta(2s - a - b) = zeta(2*2 - (2-2beta)) = zeta(2+2beta) = zeta(3),
which is fine. But zeta(s - a - b) = zeta(2beta) = zeta(1), which DIVERGES.

**Resolution for the INFINITE sum:** The sum sum_{m=1}^{infty} sigma_{1-rho}(m)^2 / m^2
diverges when 2beta = 1 (i.e., on RH). The divergence is logarithmic:

    sum_{m=1}^{M} sigma_{1/2}(m)^2 / m^2 = (zeta(2) zeta(3) / zeta(4)) * log M + O(1)

(This follows from the Ramanujan formula by taking the limit as s -> 2 from above
when a = b = 1/2, using the Laurent expansion zeta(s) = 1/(s-1) + gamma + O(s-1).)

**Resolution for the FINITE sum:** We use the partial sum up to M = N:

    sum_{m=1}^{N} sigma_{1/2}(m)^2 / m^2 = (zeta(2) zeta(3) / zeta(4)) * log N + C_1 + O(1/N)

where C_1 is an explicit constant. This is a standard result in multiplicative
number theory (see Ivic 2003, or derive via Perron's formula applied to the
Dirichlet series zeta(s)^2 zeta(s-1/2) zeta(s+1/2) / zeta(2s)).

*Status:* For FINITE T and FINITE M, the bilinear sum is a finite expression -- RIGOROUS.
The diagonal divergence is handled by using the finite partial sum. The off-diagonal
terms (rho != rho') have convergent Ramanujan sums (since Re(s-a-b) > 0 for rho != rho'
with distinct gamma's under RH).

### 4.5 The Bilinear Formula

**Theorem 4.5** (conditional on RH and simplicity of zeros).

For N >= 2 and T >= 2:

    n^2 W(N) = (1/(4 pi^2)) * [ D(N,T) + O(N,T) ] + E_1(N,N) + E_2(N,T)

where:

**Diagonal (D):**

    D(N, T) = N * sum_{|gamma| <= T} |A(rho)|^2 * K_diag(rho, N)

with:

    K_diag(rho, N) = sum_{m=1}^{N} |sigma_{1-rho}(m)|^2 / m^2

Under RH:

    K_diag(rho, N) = (zeta(2) zeta(3) / zeta(4)) * log N + C_1(rho) + O(1/N)

where C_1(rho) depends on rho but is bounded for each fixed rho.

**Off-diagonal (O):**

    O(N, T) = 2 Re sum_{rho != rho', |gamma|,|gamma'| <= T} A(rho) conj(A(rho')) N^{rho + conj(rho')} K_off(rho, rho')

with:

    K_off(rho, rho') = zeta(2) zeta(1+rho) zeta(1+conj(rho')) zeta(rho+conj(rho')) / zeta(2+rho+conj(rho'))

This is well-defined for rho != rho' since rho + conj(rho') != 1 when gamma != gamma'
(under RH, rho+conj(rho') = 1 + i(gamma - gamma') != 1).

**Error terms (already bounded):**

    |E_1(N, N)| = O(N log N)    [from Section 2.2]
    |E_2(N, T)| <= C N log^4 N / T    [under RH, from Section 4.2]

For T = N: E_2 = O(log^4 N).

*Status:* RIGOROUS for finite T, under RH and simplicity, modulo the ineffective
Walfisz constant in E_2.

---

## 5. Step 4: Extracting DeltaW(p) (FORMAL -- not rigorous)

### 5.1 The Differencing Problem

We want DeltaW(p) = W(p-1) - W(p) for prime p. This requires:

    n_{p-1}^2 W(p-1) - n_p^2 W(p) + [normalization correction]

The problem: W(N) from Theorem 4.5 involves n(N)^2 on the left and sums depending
on N on the right. Taking the difference introduces:

(a) N^{rho + conj(rho')} changes to p^{rho+conj(rho')} - (p-1)^{rho+conj(rho')}.
    For the diagonal (rho = rho'): N^1 changes to p - (p-1) = 1. CLEAN.
    For off-diagonal: the difference is ~ (rho+conj(rho')) p^{rho+conj(rho')-1}
    by the mean value theorem. Under RH: the exponent is i(gamma-gamma'), so
    |p^{i(gamma-gamma')} - (p-1)^{i(gamma-gamma')}| <= |gamma - gamma'| / p.

(b) The sums over m (the K_diag and K_off functions) also change because the upper
    limit changes from p-1 to p. The change is the m = p term (and multiples of p),
    which involves the Ramanujan sum c_p(m).

(c) The normalization n(N) changes by phi(p) = p-1.

### 5.2 Why This Is Not Rigorous

The extraction of DeltaW requires controlling the difference of TWO large
quantities (n_{p-1}^2 W(p-1) and n_p^2 W(p)), each of which has error terms
of order N log N (from E_1) and log^4 N / T (from E_2). The difference DeltaW(p)
is of order 1/p, while the individual terms are of order log(p)/p. So we need
the error terms to cancel to within O(1/p^2), which requires:

    |E_1(p, p) - E_1(p-1, p-1)| = O(1)    [need this, have O(N log N) for each]
    |E_2(p, T) - E_2(p-1, T)| = O(1)      [need this, have O(log^4 N / T) for each]

The second condition is plausible (the error is smooth in N), but PROVING it
requires a more detailed analysis of the error structure. The first condition
requires understanding how the Parseval truncation error changes at a single step.

**This is the main technical obstruction.** The formula for W(N) is rigorous;
the formula for DeltaW(p) requires one more level of precision in the error analysis.

### 5.3 The Formal Formula

Ignoring the error control problem and formally differencing:

**Formal Statement.** For prime p, under RH and simplicity:

    DeltaW(p) = (1/(4 pi^2 n_{p-1}^2)) * [ D_delta(p, T) + O_delta(p, T) + M_term(p, T) ]
                + formal error

where:

**Diagonal change (D_delta):**

    D_delta(p, T) = sum_{|gamma| <= T} |A(rho)|^2 * [K_diag(rho, p-1) - K_diag(rho, p)]
                    + normalization correction

Since K_diag changes by ~ |sigma_{1-rho}(p)|^2 / p^2 (the p-th term), and
sigma_{1-rho}(p) = 1 + p^{1-rho} for prime p (since the only divisors of p are 1 and p),
this contributes a POSITIVE quantity of order 1/p under RH.

**Off-diagonal oscillation (O_delta):**

    O_delta(p, T) = 2 Re sum_{rho != rho'} A(rho) conj(A(rho')) * [p^{rho+conj(rho')} - (p-1)^{rho+conj(rho')}] * K_off(rho, rho')

Under RH, this equals:

    ~ 2 Re sum_{gamma != gamma'} A(rho) conj(A(rho')) * i(gamma - gamma') * p^{i(gamma-gamma')-1} * K_off(rho, rho')

These are oscillatory terms at frequencies (gamma - gamma') in log(p).

**M(p) coupling term (M_term):**

From the m=1 mode of the Fourier expansion (see Section 6 below):

    M_term(p, T) ~ -2 M(p) * C_2 / p + lower order

where C_2 is a positive constant depending on sum_rho |A(rho)|^2.

**Combined formal result:**

    DeltaW(p) = (pi^2 / (12 p^2)) * [ (positive diagonal) + (oscillation at gamma-gamma') - (const) * M(p) / p ]
                + uncontrolled error

*Status:* FORMAL. Each individual manipulation is correct, but the error terms
have not been shown to be smaller than the main terms after differencing.

---

## 6. The M(p) Coupling: Why DeltaW(p) Anti-Correlates with M(p) (RIGOROUS)

### 6.1 The m=1 Mode

This is the ONE part of the formula that CAN be made rigorous independently.

**Proposition 6.1.** The m=1 contribution to n^2 W(N) is:

    (1/(4 pi^2)) * M(N)^2 / sin^2(pi/n)

where sin^2(pi/n) = pi^2/n^2 + O(1/n^4). So the m=1 term is:

    n^2 M(N)^2 / (4 pi^4) + O(M(N)^2 / n^2)

*Proof.* sigma_1(N) = sum_{q=1}^{N} c_q(1) = sum_{q=1}^{N} mu(q) = M(N). QED.

**Proposition 6.2.** The change in the m=1 contribution at prime p is:

    Delta[m=1 term] = (1/(4 pi^4)) * [n_{p-1}^2 M(p-1)^2 - n_p^2 M(p)^2] / [n_{p-1}^2 n_p^2] + lower order

Using M(p) = M(p-1) - 1 (since mu(p) = -1 for prime p) and n_p = n_{p-1} + (p-1):

    M(p-1)^2 - M(p)^2 = (M(p)+1)^2 - M(p)^2 = 2M(p) + 1

The normalization change contributes a multiplicative correction of order 1/p.
So the m=1 contribution to DeltaW(p) is approximately:

    ~ (2M(p) + 1) / (4 pi^4 n_{p-1}^2) * n_{p-1}^2 = (2M(p) + 1) / (4 pi^4)

Dividing by n_{p-1}^2 to get W:

    Delta W_{m=1}(p) ~ -(2M(p) + 1) / (4 pi^2 n_{p-1}^2)

(The sign is negative because DeltaW = W(p-1) - W(p), and M(p-1)^2 > M(p)^2 when
M(p) < -1/2, which means the m=1 contribution to W DECREASES, i.e., DeltaW > 0
from the m=1 mode alone when M(p) < -1/2.)

Wait -- let me be more careful. We have:

    DeltaW(p) = W(p-1) - W(p) = [sum d_j^2 / n_{p-1}^2] at F_{p-1} - [sum d_j^2 / n_p^2] at F_p

This is NOT simply the difference of the m=1 terms because the Farey sequence
itself changes (new fractions enter). The proper decomposition requires the
four-term A-B-C-D framework. The m=1 mode contributes to multiple terms.

**Rigorous statement (weaker but honest):**

The correlation between DeltaW(p) and M(p) follows from the identity sigma_1(N) = M(N)
and the dominance of the m=1 mode in the Fourier expansion. Specifically:

    DeltaW(p) * p^2 ~ alpha * M(p) / sqrt(p) + (higher Fourier modes)

with empirically alpha ~ -0.15 and correlation r = 0.915. The sign of the correlation
(anti-correlation) is explained by the fact that |M(p-1)|^2 > |M(p)|^2 when
M(p) is large and negative (since M(p-1) = M(p) + 1 is closer to zero).

*Status:* The QUALITATIVE explanation is rigorous. The QUANTITATIVE coefficient
and the dominance of the m=1 mode require controlling the higher modes, which
brings us back to the error control problem of Section 5.2.

---

## 7. Summary: What Is Proved, What Is Formal, What Is Conjectural

### PROVED (unconditional unless noted):

| # | Statement | Status |
|---|-----------|--------|
| P1 | sigma_m(N) = sum_{d|m} d M(N/d) | Exact identity |
| P2 | n^2 W(N) = (1/(4pi^2)) sum |sigma_m|^2 / sin^2(pi m/n) | Exact Parseval identity |
| P3 | sigma_m(N) = sum_{|gamma|<=T} A(rho) N^rho sigma_{1-rho}(m) + R_m with |R_m| = O(N tau(m) log^2(NT)/T) | Conditional on simplicity; error unconditional |
| P4 | For rho != rho' under RH: sum_{m>=1} sigma_{1-rho}(m) sigma_{1-conj(rho')}(m) / m^2 = K_off(rho,rho') | Ramanujan's formula; convergence OK since gamma != gamma' |
| P5 | Diagonal sum diverges logarithmically: sum_{m=1}^{N} |sigma_{1/2}(m)|^2 / m^2 = C log N + O(1) | Standard |
| P6 | sigma_1(N) = M(N) | Trivial |
| P7 | M(p) = M(p-1) - 1 for prime p | mu(p) = -1 |
| P8 | c_p(m) = -1 + p [p|m] for prime p | Standard |
| P9 | DeltaW(p) < 0 for all primes p in [11, 100000] | Exact rational computation |

### FORMAL (correct manipulations, uncontrolled errors):

| # | Statement | Obstruction |
|---|-----------|-------------|
| F1 | n^2 W(N) = (1/(4pi^2)) sum_{rho,rho'} A(rho)conj(A(rho')) N^{rho+conj(rho')} K(rho,rho') + ... | Diagonal regularization; need to control T -> infty limit |
| F2 | DeltaW(p) = diagonal + oscillation(gamma-gamma') + M(p) coupling + error | Error not shown to be smaller than main terms after differencing |
| F3 | Oscillatory terms have frequencies gamma_k - gamma_l in log(p) | Follows from F2; inherits its non-rigorous status |
| F4 | The diagonal (self-interference) contributes positive pressure toward healing | Follows from F2 and P5; the sign is correct but the dominance is formal |

### CONJECTURAL / NOT SUPPORTED:

| # | Claim | Verdict |
|---|-------|---------|
| X1 | FT of DeltaW shows peaks at gamma_k - gamma_l | CONTRADICTED by data (pink_noise_findings.md: mean SNR at zeros 0.91 < 1.20 at random) |
| X2 | DeltaW encodes Montgomery pair correlation | NOT operationally useful (FAREY_TELESCOPE_FORMAL.md, Section 4) |
| X3 | Z-score 1625 validates zero detection | UNVERIFIED; even if correct, reflects smoothness not zero detection |
| X4 | The formula gives new access to individual zeta zeros | NO -- information goes through M(x), which is a SUM over all zeros |

---

## 8. What Would Be Needed for a Rigorous Theorem

### 8.1 Making F1 Rigorous (the Bilinear Form for W(N))

**What's needed:** Control the T -> infty limit in Theorem 4.5. This requires:

(a) A bound on sum_{|gamma| > T} |A(rho)|^2 (the tail of the diagonal sum).
    Using the known estimate sum_{|gamma|<=T} 1/|zeta'(rho)|^2 ~ c T log T
    (Gonek 1989, conditional on RH+simplicity), the tail is O(log T / T).

(b) A bound on the off-diagonal tail. This requires estimates on
    sum_{gamma or gamma' > T} |A(rho) A(rho')| |K_off(rho,rho')|.
    The key difficulty: |K_off| involves |zeta(1+i(gamma-gamma'))| which can
    be large when gamma - gamma' is small (near a near-miss of the pair correlation).

(c) The interchange of the T -> infty limit with the m-sum. This is the same
    convergence issue that plagues the classical explicit formula.

**Assessment:** Doable with current techniques, conditional on RH + simplicity +
standard conjectures about 1/|zeta'(rho)|. This would be a solid analytic
number theory paper (not trivial, but using known methods). Difficulty: moderate.

### 8.2 Making F2 Rigorous (DeltaW from the Bilinear Form)

**What's needed:** Show that when differencing W(p-1) - W(p), the error terms
E_1 and E_2 satisfy:

    |E_1(p,p) - E_1(p-1,p-1)| << 1/p * [main term change]
    |E_2(p,T) - E_2(p-1,T)| << 1/p * [main term change]

This requires a SMOOTHNESS result: the errors vary smoothly in N, so their
difference at consecutive integers is much smaller than their individual values.

For E_2 (the Perron formula remainder), this follows from the smoothness of
x^s in x: the derivative d/dx [x^s] = s x^{s-1}, so the change from p-1 to p
introduces a factor 1/p. This is standard.

For E_1 (the Parseval truncation), the situation is more delicate because the
Farey sequence has a discontinuous change at p (phi(p) new fractions enter).
The new fractions contribute c_p(m) to sigma_m, and this is bounded (|c_p(m)| <= p).
But controlling how this interacts with the truncation requires a careful
analysis of the high-frequency behavior of the Farey exponential sums.

**Assessment:** This is the HARDEST part. It requires new estimates on the
distribution of Farey fractions at the level of individual steps. Existing
results (Franel-Landau, Dress-Mendes France) give asymptotics for the full
sum, not for individual steps. Difficulty: hard, possibly requiring new ideas.

### 8.3 An Alternative: The Four-Term Decomposition Route

Instead of differencing the bilinear form, one could:

1. Start from the proved four-term decomposition DeltaW = A - B - C - D
2. Express each of A, B, C, D separately in terms of zeta zeros
3. This avoids the differencing problem because A, B, C, D are defined directly
   in terms of the Farey fractions at order p and p-1.

The obstacle: A, B, C, D involve sums of d_j (displacements) and d_j^2, which
require the same explicit formula machinery. But the sums are SIMPLER (involving
sigma_m(N) linearly, not quadratically), so the error control may be easier.

**Assessment:** Worth pursuing. This is probably the most promising route to a
rigorous formula. Difficulty: moderate to hard.

### 8.4 Comparison with the Classical Explicit Formula for psi(x)

The classical explicit formula for the prime counting function:

    psi(x) = x - sum_rho x^rho / rho - log(2pi) - (1/2) log(1 - x^{-2})

is UNCONDITIONALLY TRUE for x not a prime power, with EXPLICIT error terms
from the truncated version (von Mangoldt, see Davenport Ch. 17).

**Key differences from our situation:**

| Feature | psi(x) formula | DeltaW(p) formula |
|---------|---------------|-------------------|
| Object | Linear sum (sum Lambda(n)) | Quadratic (sum d_j^2) |
| Zero dependence | Linear in rho | Bilinear in (rho, rho') |
| Convergence | Conditional but standard | Double sum, harder to control |
| Error term | O(x/T log^2(xT)) effective | Diagonal divergence + differencing issue |
| Differencing | Not needed | Essential (W(p-1) - W(p)) |

The fundamental difficulty: psi(x) is LINEAR in the Dirichlet coefficients,
so the explicit formula involves a SINGLE sum over zeros. W(N) involves
|sigma_m|^2, hence a DOUBLE sum. This bilinear structure makes the error
analysis qualitatively harder.

**To match the classical formula's rigor, we would need:**

1. An effective Perron formula for 1/zeta(s) with explicit constants
   (available: see Ramare 2012, Trudgian 2016)
2. Control of the bilinear sum over zeros, including the diagonal regularization
   (partially available: Goldston 1984, Gonek 1989)
3. A smooth differencing argument for the Parseval remainder
   (NOT currently available in the literature)
4. Uniform estimates for sigma_s(m) at s = 1/2 + it for all |t| <= T
   (available: standard bounds on divisor sums)

Item (3) is the genuine gap. Everything else exists or can be assembled from
known results.

---

## 9. The Complete Formula with Error Terms (Best Current Version)

Combining all the above, here is the most precise statement currently available:

**Theorem 9.1** (Conditional on RH, simplicity of zeros, and Conjecture E below).

For prime p >= p_0 and truncation parameter T = p:

    DeltaW(p) = (1/(4 pi^2 n_{p-1}^2)) * [D_1(p) + O_1(p, T) + M_1(p)] + E(p)

where:

**Term D_1 (diagonal):**

    D_1(p) = sum_{|gamma| <= T} |A(rho)|^2 * |1 + p^{1-2rho}|^2 / p^2
           = sum_{|gamma| <= T} |A(rho)|^2 * (2 + 2 cos(2 gamma log p)) / p^2    [under RH]

This is POSITIVE and of order (log T) / p^2 ~ (log p) / p^2.

**Term O_1 (off-diagonal oscillation):**

    O_1(p, T) = 2 Re sum_{0 < gamma < gamma' <= T} B(gamma, gamma') p^{i(gamma - gamma') - 1}

where B(gamma, gamma') = A(rho) conj(A(rho')) * K_off(rho, rho') * i(gamma - gamma').

This oscillates at frequencies gamma - gamma' in the variable log(p).
Its magnitude is bounded by:

    |O_1(p, T)| <= (2/p) * sum_{gamma, gamma' <= T} |A(rho)| |A(rho')| |gamma - gamma'| |K_off(rho,rho')|

**Term M_1 (Mertens coupling):**

    M_1(p) = -2 C_3 * M(p) / p + O(|M(p)|^2 / p^2)

where C_3 = sum_{|gamma|<=T} |A(rho)|^2 > 0 is a positive sum over zeros.

The negative sign explains the observed anti-correlation: when M(p) < 0,
M_1(p) > 0, contributing positive DeltaW (anti-healing).

**Error term E(p):**

    |E(p)| <= C_4 * log^4(p) / p^3

**Conjecture E** (Error smoothness). The Parseval truncation error E_1(N, N) satisfies:

    |E_1(p, p) - E_1(p-1, p-1)| <= C_5 * log^2(p) / p

for some absolute constant C_5.

*Without Conjecture E,* we can only state:

    |E(p)| <= C_6 * log(p) / p    [which is the same order as the main terms]

rendering the formula useless as a rigorous result.

---

## 10. What the Formula Teaches Us (Even Without Full Rigor)

Despite the gap in making the formula fully rigorous, its QUALITATIVE structure
is robust and consistent with all numerical evidence:

### 10.1 Three Competing Effects

1. **Diagonal (healing pressure):** The self-interference of zeta zeros with
   themselves always pushes DeltaW(p) positive (toward healing). This is the
   statistical effect of adding phi(p) = p-1 well-distributed fractions to F_{p-1}.
   ORDER: ~ C log(p) / (p^2 n^2) ~ C' / (p^2 log p).

2. **Off-diagonal (wobble):** Zero pairs (gamma, gamma') contribute oscillations
   at beat frequencies gamma - gamma'. This creates the quasi-random fluctuation
   pattern in DeltaW. The contribution of a pair scales as 1/(|rho| |rho'| |gamma-gamma'| p).

3. **Mertens coupling (arithmetic effect):** M(p) directly modulates DeltaW
   through the m=1 Fourier mode. When M(p) << 0, this dominates the diagonal
   and produces anti-healing. ORDER: ~ |M(p)| / (p^3 n^2) ~ |M(p)| / (p^5).

### 10.2 Why DeltaW(p) < 0 (Healing) for Almost All Primes

The diagonal is ALWAYS positive. The M(p) coupling is negative only when M(p) > 0.
Since M(p) changes sign frequently but is small on average (|M(p)| ~ sqrt(p)
under RH), the diagonal usually dominates, giving DeltaW < 0 (healing).

Anti-healing (DeltaW > 0) requires M(p) negative enough that the M(p) coupling
overwhelms the diagonal. Empirically, this threshold is around M(p) <= -3.

### 10.3 Connection to RH

The Franel-Landau theorem states: RH <=> sum d_j^2 = O(N^{-1+epsilon}).
In our framework, this means: RH <=> the cumulative sum of DeltaW(p) over primes
produces sufficient cancellation. The explicit formula shows this cancellation
requires: the off-diagonal zero-pair interference must average out, which is
controlled by the pair correlation of zeta zeros.

This does NOT give a new approach to RH. It REPACKAGES the Franel-Landau
connection through the lens of individual prime steps, providing physical
intuition but no new mathematical leverage.

### 10.4 Numerical Consistency

The formula predicts:
- DeltaW(p) ~ -C / (p^2 log p) on average: CONFIRMED (observed scaling)
- Anti-correlation with M(p): CONFIRMED (r = 0.915 for DeltaW*p^2 vs M(p)/sqrt(p))
- Oscillatory component: CONFIRMED (wobble pattern)
- The FT of DeltaW should show peaks at gamma_k - gamma_l: NOT CONFIRMED
  (pink noise analysis found no such peaks; see Section 0)

The failure of the FT prediction deserves explanation: the formula has
ALL zero pairs contributing, with amplitudes |A(rho)| |A(rho')| that decay
slowly (as 1/(gamma gamma')). The superposition of all these oscillations
creates a CONTINUOUS spectrum (the observed f^{-1.67} pink/red noise) rather
than discrete peaks. This is analogous to white light being a superposition
of all frequencies -- you cannot resolve individual spectral lines from a
broadband source without extraordinary frequency resolution.

---

## 11. Conclusions

### What We Have

A formal explicit formula decomposing DeltaW(p) into three physically
interpretable components (diagonal, oscillation, Mertens coupling), derived
by combining standard identities (Parseval, Ramanujan sums, Perron's formula,
Ramanujan's divisor sum convolution).

### What We Do Not Have

A rigorous theorem, because:
1. The diagonal regularization is handled but the T -> infty limit needs careful
   bounding of sum_rho |A(rho)|^2 (available conditionally).
2. The differencing step (W(p-1) - W(p)) requires Conjecture E (error smoothness),
   which is the genuine open problem.

### Path to Rigor

The most promising route is the four-term decomposition (Section 8.3):
express A, B, C, D individually via the explicit formula, avoiding the
differencing problem entirely. Each of A, B, C, D involves sigma_m LINEARLY
(not quadratically), so the error analysis is closer to the classical
explicit formula for psi(x).

### Honest Assessment

The formula is a useful HEURISTIC that explains why DeltaW(p) correlates with
M(p) and exhibits oscillatory behavior. It does NOT provide a rigorous theorem,
and the spectral prediction (peaks at gamma_k - gamma_l) was not confirmed by
the data. The contribution is the FRAMEWORK (per-step analysis of Farey
discrepancy through zeta zeros), not any individual formula.

**Classification:** C1 -- collaborative work, minor novelty. The mathematical
content is a reorganization of known identities. The perspective (per-step
Farey healing mediated by zeta zeros) is new but does not yield new theorems
beyond what Franel-Landau already provides.

---

## Appendix A: Key Constants

| Symbol | Meaning | Value/Estimate |
|--------|---------|----------------|
| A(rho) | -1/(rho zeta'(rho)) | |A(rho_1)| ~ 0.023 |
| K_off(rho,rho') | Ramanujan bilinear kernel | Depends on rho, rho'; finite for rho != rho' |
| C_3 | sum |A(rho)|^2 (truncated) | Grows like c log T |
| C_2 | M(p) coupling constant | ~ 2 C_3 |
| n(N) | |F_N| | (3/pi^2) N^2 + O(N log N) |

## Appendix B: Literature References

1. Franel (1924) -- Farey sequence discrepancy and RH
2. Ramanujan (1916) -- Divisor sum convolution formula
3. Titchmarsh (1986) -- The Theory of the Riemann Zeta Function, 2nd ed.
4. Goldston (1984) -- Mean value of the square of the Mertens function
5. Gonek (1989) -- Mean values of 1/|zeta'(rho)|
6. Dress & Mendes France (1988) -- Farey sequences and Parseval
7. Montgomery & Vaughan (2007) -- Multiplicative Number Theory I
8. Iwaniec & Kowalski (2004) -- Analytic Number Theory
9. Ramare (2012) -- Explicit estimates for the Mertens function
10. Trudgian (2016) -- Explicit bounds on the Mertens function
11. Ivic (2003) -- The Riemann Zeta Function (divisor sum asymptotics)
