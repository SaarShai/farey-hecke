---
model: mimo-v2.5-pro
max_tokens: 14000
---

# V9 — Adversarial review of killer-app (Discovery #3)

## The claim

MUSIC algorithm (Prony / line-spectral estimation, ~1986) applied to prime-bias data ψ_L(x) − x recovers low-lying L-zeros across 8 settings:

| # | Family | L-degree | Result |
|---|---|---|---|
| 1 | Function field L | — | 0.0° error |
| 2 | Riemann ζ | 1 | 10/10 zeros to 0.04–0.5% |
| 3 | Dirichlet L(χ_3, χ_4) | 1 | 6 zeros to 0.06–2% |
| 4 | Modular L(s, Δ) | 2 | 5/6 to 0–2.7% |
| 5 | EC L(11a1) | 2 | 3 zeros to 0.4–3.5% |
| 6 | Selberg/Maass | (spectral) | 7/10 to 0.12–5% |
| 7 | Sym² Δ | 3 | 5 candidates plausible |
| 8 | Sym³ Δ | 4 | 4 candidates |

## Specific adversarial questions

1. **Is MUSIC's application to L-zeros actually new?** The explicit formula ψ(x) = x − Σ x^ρ/ρ has been known since Riemann. Applying line-spectral estimation to this signal is a small step. Was it really not done before? Where would I find prior work if any?

2. **Does Prony (1795) suffice, making MUSIC overkill?** If so, the claim "MUSIC L-zero tomography" is misleading.

3. **The Sym²Δ and Sym³Δ peaks (γ ≈ 7.2, 10.5, ...) — are they actually the LMFDB-tabulated zeros, or could they be artifacts of the truncation/window?**

4. **Are the 8 settings truly distinct algorithmic tests, or just 8 instances of the same algorithm with different input data? What's the actual algorithmic novelty?**

5. **The "function field — 0.0° error" claim**: function field zeros are eigenvalues of Frobenius on cohomology, finite count, fully classical. MUSIC just recovers them — is that novel?

6. **What's the actual paper that comes out of this?** Just "Apply MUSIC to prime data" doesn't sound publishable. What's the contribution beyond the application?

## What I want

Write the REFEREE REPORT for this work. Find the weakest links. Then write the AUTHOR RESPONSE addressing each. Identify what genuinely new contribution exists, vs what's just demonstration of an existing pipeline.

If the work isn't actually novel in a publishable way, say so honestly.
