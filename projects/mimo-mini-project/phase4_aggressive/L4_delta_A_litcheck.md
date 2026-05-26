---
model: mimo-v2.5
max_tokens: 12000
---

# L4 — Lit check for the Δ(A) order-character splitting formula

## The claim

For the cyclotomic function field K = F_q(T)(ζ_M) with G = (F_q[T]/M)* and characters χ of G:

  c(A) = c_0 + Σ_{χ nontrivial} χ̄(A) · log L(q^{−1/2}, χ)

This gives the class-dependent CONSTANT TERM in the Aoki-Koyama Theorem 3.4 expansion (the leading log-n coefficient is class-cosetinvariant; the SUBLEADING constant splits per class via χ-L-values at the central point).

Specifically for (q=2, M=T³) with G ≅ Z/4Z:
  Δ(A) := −2 Re[χ̄_4(A) · log L(1/√2, χ_4)]

## Lit check

Is this formula in any of:

1. **Aoki-Koyama 2023 (J. Number Theory)** — they prove the LEADING log coefficient. Do they state the subleading constant explicitly?

2. **Koyama's correspondence (2026)** — referenced in our project_d3_binfty_citation_lock memory: he proposed "subleading C_1 = −L''(ρ)/(2 L'(ρ)²)" for the zeta side. Is our Δ(A) related?

3. **Cox-Ghosh-Sultanow 2021** — they have an explicit formula for static Farey-Mertens. Any character-decomposed constants?

4. **Conrey-Snaith-Keating**: their CM-symmetry-type formulas for L-derivative moments. Any analog for the constant term in prime-counting biases?

5. **Function-field analytic number theory texts** (Rosen, Murty-Esmonde, ...): subleading constants in AK-style theorems?

## What I want

State for each source:
- Is the explicit subleading constant formula present?
- If yes, what's the connection to our Δ(A) = -2 Re[χ̄_4 · log L]?
- If not, this is a clean explicit subleading derivation for the function-field case.

Especially CRITICAL — the connection to **Koyama-conjecture (3)** "C_1 = −L''(ρ)/(2 L'(ρ)²)". My Δ(A) might be the function-field analog. Spell out the relation if any.
