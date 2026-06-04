# Per-Prime Decomposition of Farey Discrepancy and the Mertens Function
## Paper Outline

### Authors
[To be determined]

### Target Journal
Experimental Mathematics (primary) / Mathematics of Computation (backup)

---

## Abstract
We introduce a per-step decomposition of the squared Farey discrepancy W(N) = sum (f_j - j/|F_N|)^2, studying how W changes when a single integer N is added to the Farey sequence. We discover that primes almost universally increase W (disrupt uniformity), while composites tend to decrease it. More precisely, we prove that the Fourier coefficient of the Farey discrepancy at frequency p is exactly -1 - M(p)/2, where M(p) is the Mertens function, and conjecture that a positive change DeltaW(p) > 0 implies M(p) >= 0. This conjecture, verified computationally for all primes up to [500K when complete], provides a new geometric characterization of Mertens function positivity through Farey sequence uniformity, connecting to the Riemann Hypothesis through the Franel-Landau framework.

## 1. Introduction
- Farey sequences and the Franel-Landau theorem (1924)
- The Mertens function and its connection to RH
- Our contribution: per-step decomposition reveals new structure
- Summary of results

## 2. Definitions and Background
- 2.1 Farey sequences F_N, size |F_N| = 1 + sum phi(k)
- 2.2 Squared Farey discrepancy W(N) = sum (f_j - j/n)^2
- 2.3 Per-step wobble change DeltaW(N) = W(N-1) - W(N)
- 2.4 The Mertens function M(N) = sum mu(k)
- 2.5 Ramanujan sums c_q(n)

## 3. Main Results

### 3.1 Exact Identities (Formally Proved in Lean 4)

**Theorem 3.1** (Bridge Identity): For prime p >= 2,
  sum_{f in F_{p-1}} exp(2*pi*i*p*f) = M(p) + 2

**Theorem 3.2** (Displacement-Cosine Identity): For prime p >= 2,
  sum D(f_j) * cos(2*pi*p*f_j) = -1 - M(p)/2
  where D(f_j) = j - n*f_j is the rank discrepancy.

**Theorem 3.3** (Fractional Parts Sum): For prime p >= 2,
  sum {p*f_j} over F_{p-1} = (n-2)/2

**Theorem 3.4** (Insertion Orthogonality): For prime p >= 2,
  sum D_{p-1}(k/p) * cos(2*pi*k/p) = 0

**Theorem 3.5** (General Involution Principle): For any symmetric function g,
  sum D(f) * g(f) = -(1/2) * sum g(f)

### 3.2 Computational Discoveries

**Observation 3.6** (Prime-Composite Sign Flip):
  ~85% of primes increase W; ~69% of composites decrease W.

**Observation 3.7** (Violation-Mertens Correlation):
  DeltaW(p) > 0 implies M(p) >= 0, verified for [N] primes with 0 counterexamples.

**Observation 3.8** (Burst-Quiet Pattern):
  Violations cluster in zones where M(N)/sqrt(N) > 0, with growing cluster sizes.

**Observation 3.9** (M/sqrt(p) Threshold):
  P(violation | M/sqrt(p) >= 0.26) = 100%. The violation probability follows
  a logistic curve in M/sqrt(p) with midpoint at 0.14.

### 3.3 The Main Conjecture

**Conjecture 3.10**: For all primes p >= 11, DeltaW(p) > 0 implies M(p) >= 0.

**Partial Results toward the Conjecture:**
- Analytical proof for the range [5000, 30000) via bounded residuals
- Computational verification for all primes up to [500K]
- The involution principle explains WHY: M controls the symmetric (cosine) component
  of the discrepancy-frequency interaction, while the antisymmetric (sine) component
  is largely M-independent.

## 4. Proofs of Exact Identities

### 4.1 The Farey Involution
- sigma(a/q) = (q-a)/q maps f to 1-f
- D(sigma(f)) = -D(f) - 1
- Consequence: sum D*g = -(1/2)*sum g for symmetric g

### 4.2 Proof of Theorem 3.1 (Bridge Identity)
- Decompose by denominator b
- For b < p: c_b(p) = mu(b) since gcd(p,b) = 1
- Sum gives M(p-1) + 1 = M(p) + 2

### 4.3 Proof of Theorem 3.2 (Displacement-Cosine Identity)
- cos(2*pi*p*f) is symmetric under f -> 1-f
- Apply involution principle (Theorem 3.5)
- Get -(1/2)*(M(p)+2) = -1 - M(p)/2

### 4.4 Proof of Theorem 3.3 (Fractional Parts Sum)
- Multiplication by p permutes coprime residues mod b
- Sum of coprime residues = b*phi(b)/2
- Total sum = sum phi(b)/2 = (n-2)/2

### 4.5 Proof of Theorem 3.4 (Insertion Orthogonality)
- Involution k -> p-k on insertion points
- D(k/p) + D((p-k)/p) = 0 and cos(2*pi*k/p) = cos(2*pi*(p-k)/p)
- Antisymmetric * symmetric = 0

## 5. The Symmetric-Antisymmetric Decomposition
- Decompose {pf} = 1/2 + ({pf} - 1/2)
- Symmetric part (constant 1/2): gives sum D * {pf}_sym = -n/4
- Antisymmetric part ({pf}-1/2): not controlled by involution
- Numerical evidence: antisymmetric part ~ C(p)*n, weakly M-dependent
- Connection to the Fourier series of the sawtooth function

## 6. Computational Methods and Results
- 6.1 Fast C implementation using Farey next-term generator
- 6.2 Exact arithmetic verification at small N
- 6.3 Results up to N = [500K]
- 6.4 Violation rate analysis and M/sqrt(p) threshold
- 6.5 Residual bound analysis

## 7. Formal Verification
- 7.1 Lean 4 / Mathlib framework
- 7.2 Aristotle automated theorem prover
- 7.3 List of formally verified theorems (22+)
- 7.4 Comparison with other formal verification efforts in number theory

## 8. Connections and Applications
- 8.1 Connection to Rubinstein-Sarnak bias theory
- 8.2 Refinement of Erdos-Turan inequality for Farey sequences
- 8.3 Maximum mean discrepancy and RH equivalence
- 8.4 Potential applications to ZK proof systems (speculative)

## 9. Open Problems
- 9.1 Prove Conjecture 3.10 (the main conjecture)
- 9.2 Determine the asymptotic violation rate
- 9.3 Extend to composite N: is there an analogue for DeltaW(N) at composites?
- 9.4 Generalize to Farey sequences of arithmetic progressions
- 9.5 Connect the antisymmetric part to known number-theoretic quantities

## 10. Conclusion

## Appendix A: Complete List of Lean 4 Theorems
## Appendix B: Computational Data and Reproducibility
## Appendix C: Visualization Gallery

---

## Key Figures
1. Farey fractions on the unit circle (prime vs composite insertion)
2. Wobble trajectory W(N) for N up to 20,000
3. DeltaW sign plot (violations in red)
4. Mertens function vs violation density (dual panel)
5. M/sqrt(p) violation probability (logistic curve)
6. Burst-quiet strip chart
7. Zeta zero interference pattern
8. Residual bound convergence plot
