---
model: mimo-v2.5-pro
max_tokens: 10000
---

# T1C — Re-verify Aistleitner-Hofer 2014 (arXiv:1405.6532) carefully

## Background

Earlier MiMo dispatches disagreed:
- Z2 confidently said paper exists, JNT 147 (2015), 121-136, with asymptotic involving Σ M(n)²/n³
- Z6 cautiously said "I cannot verify"

This matters because if the paper exists and proves something close to NW(Q) ~ C + corrections involving M(n)², then OUR Mertens-NW finding may be partly known.

## Tasks

1. **Cite-or-disclaim with care**:
   - Does arXiv:1405.6532 exist? Title? Authors?
   - Is it published in JNT 147 (2015)?
   - If yes, what's the precise asymptotic statement?
   - Specifically: does the constant involve Σ_n M(n)²/n³ or some related Möbius/Mertens sum?

2. **Closely-related papers to check**:
   - Aistleitner & Berkes (various) on extremes of multiplicative functions
   - Aistleitner & El-Baz — Farey-related?
   - Kanemitsu & Yoshimoto on Farey discrepancy
   - Hooley on Farey discrepancy / additive sieves
   - Tóth on Farey sequences
   - K. Soundararajan on M(x) extremes

3. **Specifically: what is the BEST KNOWN asymptotic formula for J(Q)?**

  Known classical: J(Q) ~ C_1 · Q (linear), with C_1 some constant. Our claim: NW(Q) = Q·J(Q)/Φ(Q) → C = 0.66989.

  Is this LINEAR (J ~ Q) asymptotic already proven? By whom?

4. **The "Σ M(n)²/n³ involved in constant" claim** (per Z2):

  Σ_n M(n)²/n³ — does this sum converge? Under RH, |M(n)|² ≤ n^{1+ε} so |M(n)²/n³| ≤ n^{-2+ε}, so the sum converges absolutely under RH. Unconditionally, the bound is M(n) = O(n) so M²/n³ = O(1/n), divergent.

  So "Σ M(n)²/n³" convergence is RH-equivalent? Interesting.

5. **If Aistleitner-Hofer DOES prove a formula with M(n)²**:
   - Their "constant" would absorb the AVERAGE contribution.
   - Our pointwise M(Q)²/(6Q) would be the FLUCTUATION around their constant.
   - These are COMPLEMENTARY: average vs pointwise.

## What I want

Honest answer:
- Does the paper exist? (verifiable claim)
- If yes, what does it actually prove?
- Does it overlap with our pointwise correlation finding?
- Or is our pointwise finding genuinely new on top of their average-asymptotic?

NO CONFABULATION. If you cannot verify, say so clearly.
