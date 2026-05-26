---
model: mimo-v2.5-pro
max_tokens: 16000
---

# B1 — Formalize the L-Zero Optimal Sample Complexity Theorem + lit check

## Empirical setup (what I've shown)

Take a cyclotomic function field K = F_q(T)(ζ_M) with G = (F_q[T]/M)^*, and let
L(u, χ) be the Dirichlet L-function for a nontrivial character χ. By
Weil's RH for function fields, L(u, χ) is a polynomial in u of degree
d = deg(M) − 1, all of whose zeros have |u| = q^{−1/2}.

I define the **class-bias signal**:
  Δ_n(A) := π_{1/2,K}(q^n) − Φ(M)·π_{1/2}(q^n; M, A)

By character orthogonality + the explicit formula, after character-summing
Δ_n^(χ) := Σ_A χ̄(A)·Δ_n(A), the signal s_n = Δ_n^(χ) has the form

  s_n = Σ_{j=1}^{d} C_j · (q^{1/2} e^{iθ_{χ,j}})^n + lower-order terms

where θ_{χ,j} are the L-zero phases (Weil RH zeros + trivial zeros at u=1).

The Prony / MUSIC / Matrix Pencil algorithms recover the d phases θ_j from
N ≥ 2d measurements s_1, s_2, …, s_N.

**Empirical demonstration at (q=2, M=T^3, d=2)**:
- N=4 (= 2d minimum): Prony recovers Weil-RH zero phase to 6.7° error
- N=10: 0.8° error
- N=22: 0.0° error (machine epsilon)
- Error decays roughly as O(N^{-α}) for some α ≥ 1.

## The claim

(A) **Sample complexity** for L-zero phase extraction from prime-count bias
is N = O(d), where d = deg(L-poly). The constant in O() is 2 (Prony lower
bound). This **matches the information-theoretic lower bound** for recovering d
complex exponentials from a complex signal.

(B) **Phase extraction error** scales as O(N^{-α}) for α ≥ 1 in the noiseless
regime. Empirically α ≈ 1 to 2.

(C) **Per-measurement cost** is O(X/log X) for sieving primes up to X. Total
cost: O(d · X). Compare to direct L-function evaluation: requires computing the
L-polynomial (Kedlaya's algorithm: O(d² · deg(M)^3)) plus root-finding (O(d³)).
For function fields, direct is cheaper. For number fields, sieving may be
preferred (parallel-friendly, no L-function code needed).

## The questions

### Q1 — Precise theorem statement

Write a precise theorem statement of the form "Given (q, M, χ), the L-zero
phases θ_j of L(u, χ) can be extracted from N prime-count bias measurements
Δ_n(A) using MUSIC, with phase error bounded by Ψ(N, d, residual) where the
explicit form is …". State the conditions, the bound, and the proof sketch
(use Prony+CRLB analysis).

### Q2 — Literature check

Is this theorem (or anything equivalent) already in the literature?

Candidate sources to consider:
- Sarnak's work on Quantum Chaos and trace formulas (the explicit formula bridge
  to spectral estimation might be classical).
- Iwaniec-Kowalski "Analytic Number Theory" textbook on character sums.
- Atkin-Lehner "Asymptotic mean square of partial sums" type results.
- Weng-Murty / Garrett on L-zeros from prime data.
- Signal processing classics: Pisarenko, Schmidt, Hua-Sarkar.

For each, list whether the result IS the same as my claim, GENERALIZES my claim,
or is INDEPENDENT.

If the theorem is known in the SP literature for general frequency estimation
but NOT applied to L-zeros, then my contribution is the BRIDGE / FRAMING, not
the theorem itself.

### Q3 — Novel implications

Beyond the recoverability claim itself, what does this framing UNLOCK?

Examples I've considered:
- "Compressed L-function commitments": store O(d) prime counts, reconstruct
  zeros (but: smaller than the L-poly itself? maybe not).
- Sampling theorem for L-data: minimum d measurements is information-theoretic.
- Cross-domain bridge to quantum cavity tomography (Sarnak-Berry style).

What OTHER consequences should I list?

### Q4 — Open questions

- For number fields (not function fields), what's the corresponding theorem?
  L-functions there have infinitely many zeros — does the algorithm still
  work for the FIRST d zeros?
- For complex Dirichlet characters in F_q[T], the algorithm works cleanly.
  For real (quadratic) characters, there's a 180° ambiguity. How to resolve?

## What I want

1. A precise theorem statement, with assumptions and conclusion.
2. Literature comparison: is this known, novel, or a known result with new framing?
3. ≥3 implied consequences that are novel.
4. 1-2 open problems to leave for future work.

If you find this is already known, **be honest about that** — the framing
contribution might still be useful even if the math isn't new.
