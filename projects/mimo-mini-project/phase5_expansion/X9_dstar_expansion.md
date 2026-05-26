---
model: mimo-v2.5-pro
max_tokens: 12000
---

# X9 — D*(F_N) expansion: verify or refute

## Current state

Claimed: D*(F_N) = 1/N − π²/(3N²) + O(1/N³)

AV7 verdict: "Potentially publishable if D* properly defined and expansion derived."

## Tasks

### A. Precise definition of D*

What is D* here? Likely the L^∞-discrepancy (star discrepancy):
  D*(F_N) = sup_{x ∈ [0,1]} |#{α ∈ F_N : α ≤ x}/|F_N| − x|

Verify this is the right definition.

### B. Derive the expansion from first principles

For Farey F_N with |F_N| = Φ(N) + 1 = 1 + Σ_{n≤N} φ(n) ~ 3N²/π²:

The discrepancy E_N(x) = (#{F_N ≤ x}) - Φ(N) · x has L^∞ norm:
  ||E_N||_∞ ≤ 1 (at jumps of count function)

Normalized:
  D*(F_N) = ||E_N||_∞ / |F_N| ≤ 1 / |F_N| ~ π²/(3N²)

Hmm, this gives 1/N² scaling, not 1/N as claimed.

Maybe a different normalization? Or maybe the claim is for a different discrepancy?

### C. Check the leading coefficient

If D*(F_N) ~ 1/N, that means the L^∞ jump is normalized by N (not by |F_N|). What discrepancy does this?

Possible: Niederreiter's "true" discrepancy:
  D_N* = sup_x |N_F(x)/N - x|
where N_F is the count of Farey points and we divide by N (not by Φ(N)).

OR: the Mikolás L^2 discrepancy.

OR: total variation distance from uniform on [0,1].

Identify which one gives 1/N − π²/(3N²) + O(1/N³).

### D. Connection to RH

The Franel-Landau theorem connects L^2 Farey discrepancy to RH. Specifically:
  Σ_{a/q ∈ F_N} (a/q - some_uniform)² = O(N^{-1+ε}) ⟺ RH

Is the claimed 1/N − π²/(3N²) expansion CONSISTENT with RH? Or stronger?

If the expansion implies RH (because the error term is too tight), then it's CONJECTURAL.
If the expansion is consistent with both RH and not-RH, then it could be unconditional.

Determine which.

### E. Higher-order terms

Compute or predict the O(1/N³) coefficient. Is there a clean closed form?

## What I want

- Precise definition of D* in our claim
- Derivation of expansion 1/N − π²/(3N²) + O(1/N³)
- Verification at multiple N
- Connection to RH (conditional or unconditional?)
- Higher-order terms

Honesty: state if the expansion doesn't actually hold or needs reformulation.
