---
model: mimo-v2.5-pro
max_tokens: 16000
---

# D5 — L-zero phase tomography from Chebyshev-bias class-splits (deep dive)

## Setup — the "inverse" use of our previous-sprint discovery

In the previous sprint we found that for the cyclotomic function field K = F_2(T)(ζ_{T³}):

  LHS_n(A) = π_{1/2,K}(2^n) − 4 · π_{1/2}(2^n; T³, A)

has a class-dependent constant term

  Δ(A) = −2 Re[χ̄_4(A) · log L(1/√2, χ_4)]

where χ_4 is the order-4 character of (F_2[T]/T³)^* = ℤ/4ℤ. The numerical residuals Δ(1) − Δ(5) ≈ +1.23 − (−1.23) = +2.46 etc. encode information about the COMPLEX LOG of L(1/√2, χ_4).

**The classical direction**: compute L(1/√2, χ_4) directly (we did — got 0.5 + i(√2−1)/2, modulus ≈ 0.541, argument ≈ 22.5°).

**The inverse direction (this dive)**: given ONLY the empirical Δ(A) values from prime-counting, can we RECONSTRUCT the L-function zeros?

## The question

**Q1**: For a cyclotomic function field K = F_q(T)(ζ_M), the L-functions L(u, χ) for nontrivial χ are polynomials of degree d = deg(M) − 1. Their zeros lie on the circle |u| = q^{-1/2} (Weil's RH). Each zero α_j = q^{-1/2} e^{i θ_j}.

The class-bias residuals Δ(A) at any fixed n are sums over zeros:
  Δ_n(A) = − Σ_{χ ≠ trivial} χ̄(A) · (1/n) · Σ_{α zero of L(u,χ)} (q^{1/2}/α)^n · (something)

Equivalently, the bias has a FOURIER expansion in n with frequencies given by the L-zero phases θ_j.

**Inverse problem**: given Δ_n(A) measured at many n, extract the phases θ_j of all L-zeros across all χ.

**Q2**: When is this inverse problem **well-posed**? Specifically: how many residue classes A do we need to measure, and how many degrees n, to identify all L-zero phases?

**Q3**: This is similar to **spectral tomography** in physics (extract spectra from time-domain measurements). What's the analogue here? Is there a Wiener-Khinchin-style identity for L-zero spectra?

**Q4** — practical algorithmic question: For a general number field K with conductor of moderate size where computing L-zeros directly is HARD (large dimension), would prime-counting + bias-decomposition be a FASTER way to extract L-zero phases? Compare:
  - Direct: compute L(s) at s = 1/2 + it for many t, find zeros. Complexity O(N) per evaluation where N = conductor.
  - Via bias tomography: count primes p ≤ X in residue classes mod conductor, decompose into characters. Complexity O(X) total but X needs to be large for accuracy.

**Q5** — bridge to active research: this connects to:
  - Selberg's trace formula (relates spectrum to primes)
  - Hilbert-Pólya conjecture (RH from a self-adjoint operator)
  - Computing zeros of L-functions for number-theoretic crypto

## What I want

1. Explicit formula relating Δ_n(A) to L-zero phases (as a finite sum).
2. Statement of when the inverse problem is well-posed (rank conditions).
3. Algorithm sketch: input = measured Δ_n(A) for various n, A; output = list of L-zero phases.
4. Complexity comparison to direct L-zero computation.
5. Where this could be USEFUL beyond just our concrete (q=2, M=T³) case.

Look for: is there a **bridge to inverse problems in physics** (e.g., quantum scattering, density-of-states reconstruction)? That's the counter-intuitive payoff.
