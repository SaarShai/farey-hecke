---
model: mimo-v2.5-pro
max_tokens: 10000
---

# N24 — Sym⁴ Δ and Sym⁵ Δ extensions

We've tested MUSIC L-zero tomography on Sym²Δ (degree 3) and Sym³Δ (degree 4). Both give peaks consistent with L-zeros, though independent verification pending.

## Want

Push further:

### Sym⁴ Δ — degree 5 L-function

Hecke eigenvalues: λ_p(Sym⁴) = some polynomial in λ_p(Δ).

If λ_p(Δ) = α + β (with αβ = 1), then:
- Sym⁰: 1
- Sym¹: α + β = λ_p(Δ)
- Sym²: α² + αβ + β² = λ_p(Δ)² − 1
- Sym³: α³ + α²β + αβ² + β³ = λ_p(Δ)³ − 2λ_p(Δ)
- Sym⁴: α⁴ + α³β + α²β² + αβ³ + β⁴ = λ_p(Δ)⁴ − 3λ_p(Δ)² + 1
- Sym⁵: λ_p(Δ)⁵ − 4λ_p(Δ)³ + 3λ_p(Δ)

Confirm the recurrence:
  λ_p(Sym^{k+1}) = λ_p(Δ) · λ_p(Sym^k) − λ_p(Sym^{k-1})

## Asks

1. Verify the Sym^k recurrence above.

2. For Sym⁴ Δ:
   - First 5 γ-values (low-lying zeros)
   - LMFDB label
   - Expected MUSIC accuracy with primes up to 10⁵

3. For Sym⁵ Δ:
   - First 5 γ-values (if known)
   - LMFDB label
   - Predicted MUSIC accuracy

4. Order-of-vanishing of Sym^k Δ at s = 1/2: any known patterns? (For Sym^odd Δ, sign of functional equation alternates?)

5. Limit on MUSIC: as k → ∞, λ_p(Sym^k) grows like 2^k, which makes the signal-to-noise ratio worse. What's the theoretical limit on Sym^k that MUSIC can handle with primes up to 10⁵?

Be specific or say "I don't know."
