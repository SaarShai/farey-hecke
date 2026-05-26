---
model: mimo-v2.5-pro
max_tokens: 12000
---

# N20 — ML / Neural approaches to L-zero prediction

Our killer-app result: MUSIC algorithm (1986, Schmidt) recovers L-zeros from prime-bias data in 8 settings, using the information-theoretic minimum N=2d samples (Prony).

This raises a question: can a NEURAL NETWORK or other ML method LEARN the prime-to-L-zero map and apply it to predict zeros of UNKNOWN L-functions?

## Specific framing

Training set: Pairs (prime-bias signal ψ_L(x) at log-spaced x ∈ {10², 10²·⁰⁵, ..., 10⁵}, true γ_1 ... γ_k for that L-function). Curate ~1000 known L-functions from LMFDB.

Test: Given new prime-bias signal of an UNTABULATED L-function, predict γ_1...γ_k.

## Questions

1. Is this already done? (Any papers using ML to find/verify L-zeros?)

2. Does a transformer architecture (treating prime-bias as a sequence) outperform MUSIC at this task?

3. The MUSIC algorithm has a closed-form (no learning). What would a neural model learn beyond MUSIC?

4. **Practical use**: Given an L-function known only up to L(s, χ) for s in some narrow strip, could ML predict zeros from limited prime data?

5. Connection to recent work on AI for math: DeepMind's mathematical discovery papers (knot theory, AlphaTensor), but specifically for analytic number theory.

## What I want

3-paragraph assessment:
- Whether this is novel
- Whether it's worth pursuing
- The fastest path to a publishable result (datasets, baselines, evaluation protocol)

If this is uninteresting (just an ML re-implementation of an existing closed-form algorithm), say so. Strong "no, skip" is fine.
