---
model: mimo-v2.5-pro
max_tokens: 16000
---

# N14 — More L-function families for MUSIC tomography

We've validated MUSIC L-zero extraction in 8 settings:

1. Function field L (Weil RH) — 0.0° error
2. Riemann ζ — 10 zeros to 0.04–0.5%
3. Dirichlet L(χ_3, χ_4) — 6 zeros to 0.06–2%
4. Modular form L(s, Δ) — 5/6 zeros to 0–2.7%
5. Elliptic curve L(11a1) — 3 zeros to 0.4–3.5%
6. Selberg/Maass spectrum on SL(2,Z)\H — 7/10 eigenvalues to 0.12–5%
7. Sym² Δ — degree 3, 5 candidates
8. Sym³ Δ — degree 4, 4 candidates

The algorithm needs:
- A way to compute λ_p (coefficient at prime p, normalized so that the L-function has functional equation s ↔ 1−s)
- The bias signal ψ_L(x) = Σ_{p≤x} λ_p · log p
- MUSIC line-spectral estimation on log-spaced samples → zero imaginary parts

## What I want

For each of the following families, provide:
- A specific LMFDB-style label or identifier
- Formula for λ_p in terms of computable arithmetic data
- First 5–6 known γ values (imaginary parts of nontrivial zeros)
- Estimated MUSIC accuracy expected with prime data up to 10⁵

### Families of interest

A. **Hecke Grossencharacter L over Q(i)** — degree 2 over Q. Examples: L(s, ψ) for ψ the canonical Hecke character of conductor (1+i).

B. **Artin L-function of an irreducible 2-dimensional Galois representation** — e.g., from the splitting field of x³ − x − 1 (a non-abelian cubic).

C. **L-function of an elliptic curve over a quadratic field**, e.g., E/Q(√5).

D. **Eisenstein-related L** (e.g., Riemann ζ × ζ(s−1) or shifted) — would test if MUSIC catches DEGENERATE / repeated zeros.

E. **Symmetric 4th power Sym⁴ Δ** — degree 5 L-function. Even harder than Sym³.

F. **GL(3) Maass cusp form** with smallest spectral parameter ~λ ≈ 9.218. Tables of Hecke eigenvalues if available.

G. **Twisted L-functions** L(s, Δ × χ_5) where χ_5 is the quadratic character mod 5.

H. **Rankin-Selberg L(s, Δ × Δ)** — degree 4.

If a family is unrealistic (insufficient data), say so. PREFER concrete computable predictions over hand-waving. Honest "I don't know specific γ" is more useful than confabulation.
