---
model: mimo-v2.5-pro
max_tokens: 16000
---

# P1 — PROOF ATTEMPT: Farey gap clusters of size ≥ 3 have vanishing probability

## Claim to prove

**Claim**: For the Farey sequence F_N, threshold u_N = quantile q < 1 (specifically u_N such that #{d_i > u_N}/|F_N| → 1 - q), define a "large-gap cluster" as a maximal run of consecutive indices i, i+1, ..., i+k-1 with d_i, d_{i+1}, ..., d_{i+k-1} all > u_N. The probability that a cluster has size k satisfies:

  P(cluster size = k | cluster occurred) → δ_{k, 2} as N → ∞ at high quantile

I.e., the cluster size distribution concentrates at size 2.

## Mechanism (sketch from BCZ recurrence)

Consecutive Farey gaps share denominators: d_i = 1/(k_i k_{i+1}), d_{i+1} = 1/(k_{i+1} k_{i+2}). A "large" d_i requires k_{i+1} to be small. By the BCZ recurrence k_{i+2} = κ k_{i+1} − k_i with κ = ⌊(N + k_i)/k_{i+1}⌋, the new denominator k_{i+2} = κ k_{i+1} − k_i.

For small k_{i+1}: κ ≈ N/k_{i+1} is large, so k_{i+2} ≈ N - k_i, which is large. Hence d_{i+2} = 1/(k_{i+2} k_{i+3}) is small (not a large gap).

So: large d_i forces k_{i+1} small → forces k_{i+2} ≈ N - k_i large → d_{i+2} is NOT large.

This intuitively gives exactly 2-gap clusters: d_i and d_{i+1} both large, then d_{i+2} forced small.

## Your task

Make this rigorous.

1. State the precise probabilistic claim (extremal index = 1/2, or stronger: cluster size 2 with prob → 1).

2. Use the explicit BCZ joint distribution to derive the cluster size distribution.

3. Compute analytically:
   - P(cluster size = 1 | started)
   - P(cluster size = 2 | started)
   - P(cluster size ≥ 3 | started)

The empirical fact at u=99.99%, N=30000 is P(=1)≈0.7%, P(=2)≈99.3%, P(≥3)≈0.

4. If you can derive these probabilities in closed form, do so.

5. If not, derive what their asymptotic behavior should be: do P(=1) and P(≥3) BOTH decay to 0 as u → 1?

Use the BCZ joint density f(x, y) = 2 on the triangle x + y > 1 and the deterministic recurrence z = ⌊(1+x)/y⌋ y − x.

## What I want

A rigorous derivation, not just hand-waving. Show the integrals. Compute limits. If a proof is incomplete, identify what's missing.

This would settle Discovery #7 to publication-grade rigor.
