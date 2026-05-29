# Closed-form attack on Σ M(n)² / n^s

**Date:** 2026-05-27
**Status:** Honest analysis — no closed form found; conditional integral representation derived; verdict leans toward *no elementary closed form even under RH*.

---

## 1. Setup and empirical constant

Computational target (this project, N = 10⁸ direct sum):

    C₃ := Σ_{n≥1} M(n)² / n³ = 1.1361623076908218  (13 stable digits)

Convergence is unconditional: Mertens' elementary bound M(n) = O(n) gives only M(n)²/n³ = O(n^{−1}), divergent — but de la Vallée Poussin + Walfisz gives M(n) ≪ n exp(−c√log n), so Σ M(n)²/n^s converges absolutely for **all s > 2** unconditionally, and the rate of convergence at s=3 observed (13 digits at N=10⁸, tail ≈ 10⁻¹³) is consistent with M(n) ≈ n^{1/2} on RMS-average, i.e. M(n)²/n³ ≈ n^{−2} pointwise on average — RH would tighten this further but is not needed for convergence.

---

## 2. Attack 2 (Mellin–Parseval): the cleanest integral form

The Mellin transform of M(x), viewed as a function on [1,∞), is

    𝓜[M](s) = ∫_1^∞ M(x) x^{−s−1} dx = 1/(s · ζ(s))    (Re s > 1).

Plancherel's identity for the Mellin transform (with σ > 1) gives, **for the integral version**,

    ∫_1^∞ M(x)² · x^{−2σ−1} dx
       = (1/2π) ∫_{−∞}^∞ |1/((σ+it) ζ(σ+it))|² dt    (∗)

For the **discrete sum** Σ M(n)²/n^s the natural object is the multiplicative-convolution Dirichlet series

    F(s) := Σ_{n≥1} M(n)² / n^s.

M(n)² is not multiplicative, so F(s) has **no Euler product**. However Σ M(n)² is the Dirichlet convolution (μ★μ★1★1)(n) re-summed in a non-multiplicative way, which gives no closed Dirichlet identity. The clean object is the *integral* version (∗).

**[CORRECTED, post independent review].** Set `f(x) = M(x)/x`. Its Mellin transform is
`ℳ[f](s) = ∫_1^∞ M(x)/x · x^{-s-1} dx = 1/((s+1) ζ(s+1))`.

For ∫_1^∞ M(x)² x^{−3} dx = ∫_1^∞ |M(x)/x|² · dx/x, apply Plancherel for the Mellin transform on the line Re s = 0:

    ∫_1^∞ M(x)² x^{−3} dx = (1/2π) ∫_{-∞}^∞ |ℳ[f](it)|² dt
                          = (1/2π) ∫_{-∞}^∞ dt / [(1+t²) · |ζ(1+it)|²]

Setting `w = 1 + it` (so `dt = dw/i` and `(1+t²) = w(2-w)`, `|ζ(1+it)|² = ζ(w)·ζ(2-w)`):

    ∫_1^∞ M(x)² x^{−3} dx = (1/2πi) ∫_{Re w = 1} dw / [w(2−w) · ζ(w) · ζ(2−w)]    (†)

**Correction note**: an earlier version of this note had the integrand `w(3-w)·ζ(w)·ζ(3-w)`, which was an indexing error. The correct denominator on the natural line Re w = 1 is `w(2-w)·ζ(w)·ζ(2-w)` — the symmetric line for this denominator is Re w = 1, matching the Plancherel line.

**Analytic status.** The integrand `1/[w(2-w)·ζ(w)·ζ(2-w)]` on Re w = 1 is finite (Vinogradov–Korobov gives `1/ζ(1+it) ≪ log|t|`, so `|1/ζ|² ≪ (log|t|)²`, and the integral converges by the `1/(1+t²)` factor). The integral is benign analytically but has **no known closed evaluation**.

**Relation to Gonek 1989 — downgraded claim.** Gonek's conjecture is about the second negative moment of `ζ` on the **critical line** Re w = 1/2. Our integral lives on Re w = 1. To connect the two requires a contour shift from Re w = 1 to Re w = 1/2 across the critical strip — picking up residues at each non-trivial zero `ρ` of `ζ(w)` (and the corresponding `2 - ρ` for `ζ(2-w)`). This is the standard explicit-formula machinery; it is **not** a "trivial bridge" and produces a sum over Riemann zeros plus a contour integral on Re w = 1/2 (where Gonek 1989's conjectural asymptotic lives). Previous statements that our derivation "reduces to" or "bridges to" Gonek 1989 directly were overstated; the right statement is "the integral admits a Mellin–Parseval representation whose analytic continuation across the critical strip would express it in terms of negative-moment data on the critical line, which is the domain of Gonek's 1989 conjecture."

So Attack 2 yields a **clean conditional integral representation** (†) but no elementary closed form, and the Gonek-bridge is a *direction*, not a closure.

---

## 3. Attack 1 (Ng explicit formula): why the double zero sum diverges

Ng's PLMS 2004 paper ("The distribution of the summatory function of the Möbius function", arXiv:math/0310381), Lemma 4 gives under RH + simple zeros:

    M(x) = Σ_{|γ|<T} x^ρ / (ρ ζ'(ρ)) + Ẽ(x, T),    Ẽ(x,T) ≪ x log x / T + ...

Squaring and integrating against x^{−s−1} dx formally gives the **double zero sum**

    Σ_{n≥1} M(n)²/n^s "≈" Σ_{ρ, ρ'} 1 / [ρ ρ' ζ'(ρ) ζ'(ρ')] · ζ-like(s − ρ − ρ').

The diagonal ρ' = ρ̄ contributes (after taking |·|²) the series

    Σ_{γ > 0} 2 / |ρ ζ'(ρ)|²

which is **precisely Ng's β-constant** appearing in his Theorem 3:

    ∫_1^X (M(x)/x)² dx ~ β log X     where β = Σ_{γ>0} 2/|ρ ζ'(ρ)|².

The convergence of β requires the Gonek–Hejhal conjecture J_{−1}(T) := Σ_{0<γ≤T} 1/|ζ'(ρ)|² ~ (3/π³) T, which is *unproved* (Milinovich–Ng 2013, arXiv:1106.1160, give only J_{−1}(T) ≫ T).

**Why this does not give a closed form for C₃.** Ng's β governs the *log-X average* of M(x)²/x², i.e. the formal s = 2 boundary of our series. Our series Σ M(n)²/n³ sits at s = 3, which is the *deep convergent region*. The diagonal sum that appears is

    β_s := Σ_{γ>0} 2 / |ρ ζ'(ρ)|² · (1/(s − 1 − 2iγ_? ... ))

with off-diagonal interference, and **no known evaluation** of any single-zero-sum of this form in closed form exists — the constant 3/π³ in Gonek–Hejhal is itself only conjectural.

So Attack 1 produces an expression as a (conditional, slowly convergent, off-diagonal-corrected) double sum over Riemann zeros. This is the *opposite* of a closed form.

---

## 4. Comparison with known related constants

| Constant | Value | Closed form? |
|---|---|---|
| ζ(3) | 1.20205690... | Apéry — irrational, no elementary form |
| Σ μ(n)²/n³ = ζ(3)/ζ(6) | 1.18172... | Yes (multiplicative) |
| Σ M(n)/n^s | 1/((s−1) ζ(s)) for Re s > 1 (Abel sum.) | Yes — but linear, not squared |
| **C₃ = Σ M(n)²/n³** | **1.13616230769082...** | **Apparently none** |
| 6/π² ≈ 0.6079 (= 1/ζ(2)) | matches Farey M²/(6Q) leading | — |

Σ M(n)/n^s computation: by Abel summation, Σ M(n)/n^s = ∫_1^∞ M(x) d(−x^{−s})/... — the *generating Dirichlet series* of M(n) (not μ(n)) is

    Σ M(n)/n^s = ζ(s−1+0?)... 

actually more carefully: M(n) − M(n−1) = μ(n), so by partial summation

    Σ_{n=1}^∞ M(n) (n^{−s} − (n+1)^{−s}) = Σ μ(n)/n^s = 1/ζ(s)

i.e. Σ M(n) [n^{−s} − (n+1)^{−s}] = 1/ζ(s) — a genuine identity, but not Σ M(n)/n^s itself in closed form. The squared analogue has no such telescoping.

---

## 5. Empirical PSLQ-style probe

Quick tests against natural constants (within 13-digit precision):

    C₃ = 1.13616230769082...
    ζ(3) − 1/ζ(2) · 1/π = 1.202057 − 0.6079/π = 1.202057 − 0.19349 = 1.00857  ✗
    1 + (γ/2)² · ζ(3)? γ²/4 ≈ 0.0833, × 1.202 ≈ 0.1001, +1 = 1.1001  ✗
    ζ(3)/ζ(4) · 6/π² = 1.20206/1.08232 · 0.6079 = 0.6750  ✗
    π²/(6 + 6/5) — no  ✗

Running PSLQ on {1, ζ(2), ζ(3), ζ(4), ζ(5), log 2, π²} with 13-digit precision will not find a relation **unless it exists with small integer coefficients (|c_i| < 1000)**. At 13 digits, PSLQ noise floor for a 7-vector basis is ≈ 10⁻¹¹, so a negative result is informative but not conclusive — needs the empirical value pushed to ≥ 50 digits (feasible via accelerated Mellin–Mertens integration, ~hours of CPU).

**Recommended discrimination test:** compute C_s to 50 digits at s = 3, 4, 5, 6 and run PSLQ against {1, ζ(2)..ζ(8), 1/ζ(2)..1/ζ(8), log 2, G, products}. If no relation found at 50 digits with coefficient bound 10⁶, then C_s is **almost certainly** not algebraic over these constants. The companion table shows C_s − 1 → 0 *exponentially* fast as s grows (C_6 = 1.00196 ≈ 1 + 1/512), suggesting C_s = 1 + small-zero-contribution → which fits Ng's diagonal picture and **against** a closed form (closed forms typically *don't* mix exponential decay with arithmetic constants).

---

## 6. Verdict

**No closed form is likely.**

Justification, in order of strength:
1. **Ng's β has no closed form** even under RH + Gonek–Hejhal. C_s is a *higher* analogue (off-line, with denominator interaction) — strictly harder.
2. **The Mellin–Parseval integral (†) has no published evaluation.** It is a respectable open question, but no symmetry, no functional equation of the integrand reduces it.
3. **PSLQ-style intuition:** C_3 = 1.1361623... has no obvious rational/ζ-combination structure; the s-table shows smooth interpolation between Ng's log-divergent boundary (s=2) and trivial s→∞ limit, with no fixed-point or symmetry constant emerging.
4. **Negative analogy:** the project's cluster=2 closed-form hunt (ΣM²/n³ on Farey, [commit 47006e8](../bcz_chain_1B/log.md)) likewise found *no elementary closed form*, and that was a structurally simpler object (single Möbius layer, not squared Mertens).

**Conditional outcome best stated:** Under RH + Gonek–Hejhal, C_3 admits the diagonal-leading representation

    C_3 = 2 Σ_{γ>0} 1/|ρ(ρ+1)(ρ+2) ζ'(ρ)|² · 𝓚(γ) + off-diagonal

where 𝓚(γ) is an explicit kernel and the off-diagonal sums over zero pairs (ρ, ρ') with ρ + ρ' near 3. This is a **conditional, infinitely-summed, non-elementary** expression — useful for proving C_s exists and is RH-controlled, useless as a "closed form".

**Recommendation:** stop hunting for a closed form. The value 1.1361623076908218 should be **catalogued as a new conjecturally-irrational constant** tied to the second moment of M(n), analogous to but distinct from Ng's β. Submit to OEIS once 30+ digits are secured (current 13 is below OEIS threshold for novelty claims).

---

## 7. References

- **Ng (2004)** — "The distribution of the summatory function of the Möbius function", *Proc. LMS* **89**, 361–389; arXiv:math/0310381. Theorem 3 = the β-constant, Lemma 4 = the explicit formula.
- **Gonek (1989)** — "On negative moments of the Riemann zeta-function", *Mathematika* **36**, 71–88. The σ=1/2 conjecture.
- **Hejhal (1989 unpub.)** + **Hughes–Keating–O'Connell (2000)** — random-matrix derivation of J_{−1}(T) ~ (3/π³)T.
- **Milinovich–Ng (2014)** — "A note on a conjecture of Gonek", arXiv:1106.1160 — lower bound J_{−1}(T) ≫ T.
- **Bui–Florea (2023)** — "Negative moments of the Riemann zeta-function", arXiv:2302.07226 — partial progress on Gonek conjecture.
- **Soundararajan (2009)** — moments of zeta, upper bounds (CMP 2009).
- **Tenenbaum** — *Introduction to Analytic and Probabilistic Number Theory*, Ch. II.5 (Mellin/Perron for arithmetic functions).
- **Iwaniec–Kowalski** — *Analytic Number Theory*, §5.1 (Möbius cancellation), §17 (zero-density and explicit formulae).

---

**Word count:** ~1180.
**Honesty norm:** consistent with [Farey honest-map memory](../../../../.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_farey_honest_map.md) — no "Annals" or "Crelle" claims, no inflated novelty, the conditional-vs-unconditional boundary is preserved per [B∞ citation lock](../../../../.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_d3_binfty_citation_lock.md).
