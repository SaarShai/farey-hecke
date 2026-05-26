---
model: mimo-v2.5-pro
max_tokens: 12000
---

# D2 — Stoica-Nehorai 1989: is the CR bound for L-zeros EXPLICITLY there?

## Z4's claim

Z4 said: "The CR bound 3/2 is a relabeled Stoica-Nehorai (1989). It's in Kay Vol I §7.6. The mapping is: frequency f_k → γ_k, SNR → 1/σ², observation length T → 1."

## Test this claim DIRECTLY

1. **Stoica & Nehorai 1989** "MUSIC, maximum likelihood, and Cramér-Rao bound" (IEEE Trans. ASSP, vol. 37, pp. 720-741):
   - Does this paper EXPLICITLY state the CR bound for a signal model y(t) = Σ A_k exp(2πi f_k t) + noise?
   - What's the EXACT formula they derive?
   - In particular: does it have the (3/2) coefficient when adapted to OUR signal z(t) = -2 Re Σ exp(iγ_k t)/(1/2 + iγ_k)?

2. **Kay Vol I "Fundamentals of Statistical Signal Processing", Theorem 7.6 or §7.6**:
   - Does this section state the CR bound for sinusoidal frequency estimation?
   - What's the EXACT formula?

3. **Does ANYONE write down the CR bound for L-function zeros from prime data explicitly?**
   - This is the precise question of "novelty in our domain"
   - The Stoica-Nehorai formula is for f_k. Replacing f_k with γ_k is mathematically routine, but is it EXPLICITLY written down for L-zeros?

4. **What does it take for "novelty"?**
   - In number theory: an explicit CR bound for L-zero estimation is genuinely new (per AV1 search)
   - In signal processing: the underlying math is textbook
   - Cross-disciplinary: where does this fit?

## Specific factual checks (be precise, no confabulation)

A. The classical CR bound for a single complex sinusoid y(t) = A exp(2πi f t) + Gaussian noise (variance σ²) sampled at N equally-spaced points over time T:

   Var(f̂) ≥ ?

What is the EXACT formula? Is it 12 σ²/(4π² A² N(N²-1)) or 3σ²/(A² T³) or 12σ²/(A² T³) or something else?

Resolve the coefficient ambiguity from W3 (factor of 4) using THE CANONICAL textbook source.

B. For our signal z(t) = -2 Re Σ_k (1/ρ_k) exp(iγ_k t):
   - amplitude A_k = 2/|ρ_k| ≈ 2/γ_k
   - The signal is REAL (not complex one-sided)
   
   With A_k = 2/γ_k, Var(γ̂_k) ≥ ? Use the canonical CR formula.

C. **The actual key question**: with our specific amplitude/noise model, what's the SHARP CR coefficient?

## What I want

1. The CANONICAL textbook CR formula (be specific about source — page numbers if possible)
2. The COEFFICIENT for our L-zero signal model (resolve 3 vs 12 vs 3/2 vs 6 ambiguity)
3. An HONEST assessment of whether the L-zero application is novel:
   - If the formula is direct textbook adaptation: novelty is "modest, applied"
   - If the noise model requires non-trivial derivation: novelty is "moderate"
   - If σ² needs number-theoretic input: novelty is "real"

Don't be afraid to say "yes Z4 was right" or "no Z4 oversimplified". State which clearly.
