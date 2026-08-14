# S3_DEEP_PRIOR_ART — Prior Numerical Computation Search

**Date:** 2026-08-14  
**Task:** Verify whether any published numerical computation exists for:
1. The constant Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) ≈ 0.0290
2. Tabulation of J_{-1}(T) = Σ_{0<γ≤T} 1/|ζ′(ρ)|²

---

## Item 1: Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) ≈ 0.0290

### Search Strategy
- Targeted: Kotnik–van de Lune 2004 (Mertens variance/statistics)
- Targeted: Ng 2004 (limiting distribution of M(x)/√x)
- Targeted: Conrey-Gonek moments and zeta derivatives
- Targeted: Gonek-Hejhal conjectures on discrete moments
- Targeted: Literal string searches for numerical values 0.029, 0.0290, 0.0145

### Findings
- **Theoretical framework exists:** Nathan Ng (2004) proved that assuming RH + Gonek-Hejhal conjecture, φ(y) = e^{-y/2}M(e^y) possesses a limiting distribution (published in Experimental Mathematics)
- **Kotnik–van de Lune (2004)** computed moments of M(x)/√x numerically using trigonometric series expansions, published in Experimental Mathematics Vol 13, No 4, pp. 473-481
- **Gonek-Hejhal conjecture** (1989) establishes that J_{-k}(T) ≍ T(log T)^{(k-1)²} for discrete moments of ζ′(s) at zeros
- **Conrey-Gonek (2001)** studied high moments of ζ(s) on the critical line, not sums over zeros with 1/|ζ′(ρ)|²

### Verdict: **NO-PRIOR-NUMERIC-FOUND**

**Exact status:**
- The constant 0.0290 appears in NO published numerical tables
- Kotnik–van de Lune computed M(x) statistics but their paper does not report a value 0.0290 or its reciprocal 34.48
- Ng's 2004 work establishes existence of the limiting distribution (a qualitative result) but does not report the specific mean-square value
- No paper reconciles the conjectural limiting mean square (1/x)Σ_{n≤x} M(n)² with a sum over zeta derivatives
- The bridges remain theoretical only

**Search completeness:** Checked Ng (arXiv versions and PDF repositories), Kotnik-van de Lune (Experimental Mathematics), Conrey-Gonek high moments, and explicit literal-value searches with no positive result.

---

## Item 2: J_{-1}(T) = Σ_{0<γ≤T} 1/|ζ′(ρ)|²

### Search Strategy
- Targeted: Hejhal discrete moments computation
- Targeted: Gonek conjecture J_{-1}(T) ~ (3/π³)T verification
- Targeted: Odlyzko-style large-height zeta derivative datasets
- Targeted: Recent papers on lower/upper bounds for J_{-1}(T)
- Targeted: Milinovich-Ng conditional bounds

### Findings
- **Gonek conjecture (1989):** J_{-1}(T) ~ (3/π³)T, with Gonek proving J_{-1}(T) ≫ T
- **Milinovich-Ng (conditional):** Assuming RH + simplicity, J_{-1}(T) ≥ (3/(2π³) − ε)T for large T
- **Hughes-Keating-O'Connell (2001):** Refined conjecture using RMT, predicting J_{-k}(T) ~ 𝒢_k · (T/2π) · (log(T/2π))^{(k-1)²} for k ≤ 3/2
- **Recent work (2020–2024):** Papers on "lower bounds of discrete moments" and "upper bounds for the moments of ζ'(ρ)" exist, but focus on asymptotic bounds, not tabular computation
- **Hejhal computational datasets:** No paper found reporting computed values J_{-1}(T) for specific values of T

### Verdict: **NO-PRIOR-NUMERIC-FOUND**

**Exact status:**
- No published table of J_{-1}(T) values for specific T (e.g., T = 10⁶, 10⁹, etc.)
- No verification paper testing Gonek's asymptotic J_{-1}(T) ~ (3/π³)T numerically
- Odlyzko-style high-height zeta derivative datasets (if they exist) have not been systematically tabulated for the sum ∑ 1/|ζ′(ρ)|²
- The literature focuses on *bounds* (lower: Milinovich-Ng; upper: Kirila, Kivi) rather than explicit computation
- Hejhal's original work (arXiv:1804.08826 and related) appears to discuss theory, not numerical verification

**Search completeness:** Checked arXiv (discrete moments, Hejhal, Gonek conjecture), papers by Milinovich, Ng, Kirila, Hughes-Keating-O'Connell; searched for "discrete moments numerical" and "J_{-k}(T) computation." No numerical table located.

---

## Summary for Both Items

| Constant | Conjecture/Theory | Published Numeric Verification |
|----------|-------|-----|
| Σ_ρ 1/(ρ²\|ζ'(ρ)\|²) ≈ 0.0290 | Ng 2004 (limiting M(x)² under RH + G-H); Kotnik–van de Lune 2004 (M(x) moments) | **NO** |
| J_{-1}(T) ~ (3/π³)T | Gonek 1989; Milinovich-Ng lower bound; Hughes-Keating-O'Connell RMT refinement | **NO** |

---

## Implications

1. **Both constants appear to be conjectural with no existing numerical verification in the literature.**
2. **Kotnik–van de Lune is the closest to Item 1** — they computed empirical moments of M(x)/√x — but their paper does not bridge to the specific sum over zeta derivatives.
3. **For J_{-1}(T), the literature is entirely theoretical**: bounds, conjectures, and asymptotic predictions, but no explicit numerical tabulation.
4. **Computational opportunity:** If you compute either value numerically with certified bounds (e.g., via rigorous zeta-zero computations up to height H), you would likely produce a **novel numerical result** (first explicit verification of either the Gonek-Hejhal prediction or the M(x)² limiting distribution).

---

## Sources Checked

- [Kotnik, van de Lune: On the Order of the Mertens Function](https://www.tandfonline.com/doi/abs/10.1080/10586458.2004.10504556) (Experimental Mathematics 2004, Vol 13 No 4, pp. 473–481)
- [Nathan Ng: The distribution of the summatory function of the Möbius function](https://www.cs.uleth.ca/~nathanng/RESEARCH/mobius2b.pdf) (2004, arXiv:0406509)
- [Conrey & Gonek: High moments of the Riemann zeta-function](https://aimath.org/~kaur/publications/43.pdf) (Duke Mathematical Journal, Vol 107, 2001)
- [Limiting distributions of the classical error terms of prime number theory](https://arxiv.org/pdf/1306.1657) (Ng, 2013)
- [Negative discrete moments of the derivative of the Riemann zeta-function](https://arxiv.org/pdf/2310.03949) (2023)
- [Generalisations of the Landau–Gonek Theorem and Applications to Mean Values of Zeta](https://arxiv.org/html/2601.18025) (2026)
