# Tail Bound & Certified Resonance Prior Art
**Compiled:** 2026-08-14  
**Authority:** Web-sourced, primary documents partially unreadable (PDFs binary); assertions flagged as unverified.

---

## (1) Jenkinson–Pollicott Truncation Scheme for Fredholm Determinants

### Primary Result: Gauss-Kuzmin-Wirsing Transfer Operator Bound

**Source:** ["Certified spectral approximation of transfer operators and the Gauss map"](https://arxiv.org/html/2602.19435) (arXiv:2602.19435, 2026)

**Theorem 4.10** (Certified Error Bound):
```
‖L₁ - (L₁)_K‖ ≤ C₂ · (2/3)^(K+1)
```

- **L₁**: Gauss-Kuzmin-Wirsing transfer operator  
- **K**: Finite-rank truncation (polynomial degree cutoff)  
- **Decay rate**: Geometric, base 2/3 (exponentially fast)  
- **Constant C₂**: Operator norm composition bound, ~10.06 (explicitly refinable)

**Supporting Result: Theorem 2.15** — For isolated eigenvalue in spectral window U, ∃K₀ such that for all K ≥ K₀:
- Perturbation condition satisfied: `sup_{z∈∂U} ε_K ℛ(z,L_K) < 1`  
- Projector error vanishes: `‖P_{L_K}(U) - P_L(U)‖ → 0`  
- Individual eigenvalue enclosure via Lemma 2.12, depends on projector perturbation ϑ.

**Type:** Rigorous certified bound; applies to holomorphic transfer operators on Hardy spaces (H²).

---

### Pollicott–Vytnova Algorithm for Hausdorff Dimension

**Sources:**  
- [Rigorous effective bounds on the Hausdorff dimension of continued fraction Cantor sets](https://arxiv.org/pdf/1611.09276) (Pollicott & Vytnova, ~2016)  
- [Hausdorff dimension estimates applied to Lagrange and Markov spectra, Zaremba theory...](https://arxiv.org/pdf/2012.07083) (2020)

**Verdict:** Exact theorem statement for truncation tail bound NOT extracted (PDF binary encoding). However, published method uses:
- Zeta function bisection method  
- Polynomial error convergence (order depends on alphabet structure)  
- 100–200 decimal place accuracy achieved empirically  
- No explicit constant stated in accessible portions

**Limitation:** Source PDFs (1611.09276, 2012.07083) could not be parsed; claim rests on citation abstracts and secondary search summaries. **Unverified detail level.**

---

### Borthwick & Colleagues: Hecke Triangle Groups Transfer Operators

**Recent work (2025):** [Spectral and dynamical invariants of Hecke triangle groups via transfer operators](https://arxiv.org/pdf/2509.17936) (Fedosova et al., arXiv:2509.17936)

**Claimed:** Explicit exponentially decaying error bound for transfer operator truncation; Hausdorff dimension computed to ≥50 digits via bisection.  

**Verdict:** Exact theorem statement and bound formula NOT extracted (PDF binary). Source available but parsing failed.  

**Status:** UNVERIFIED — recommend fetching plaintext abstract or author's recent talk slides.

---

### Mayer Transfer Operator for Hecke/Rosen Continued Fractions

**Sources:**
- [The transfer operator for the Hecke triangle groups](https://arxiv.org/pdf/0912.2236) (Jenkinson et al., 2012)  
- [Hecke triangle groups, transfer operators and Hausdorff dimension](https://www.researchgate.net/publication/341640514_Hecke_triangle_groups_transfer_operators_and_Hausdorff_dimension) (ResearchGate)

**Verdict:** Transfer operators for Hecke G_q and Rosen continued fractions exist and are studied, but **no published explicit truncation tail bound found** in the literature searched.

**Status:** Method adapted to Hecke, but quantitative error bound remains **UNPUBLISHED or embedded in unparseable PDFs.** This may be a gap in literature or oversight in search strategy.

---

## (2) Rigorous/Certified Scattering Resonance Proofs

### Summary Verdict: MIXED

**Overall:** No published rigorous/interval-arithmetic proof exists for **off-critical-line scattering resonance locations** on Hecke triangle groups or general hyperbolic surfaces. On-critical-line analytic bounds exist; off-line work is numerics-only.

---

### (A) Borthwick Resonances for Schottky Groups: NUMERICS-ONLY

**Sources:**
- [Numerical resonances for Schottky surfaces via Lagrange–Chebyshev approximation](https://arxiv.org/pdf/2002.03334) (Bandtlow, Pollicott, Slipantschuk, Winn)  
- [Distribution of resonances for hyperbolic surfaces](https://arxiv.org/abs/1305.4850) (Borthwick)

**Computational Method:** Periodic orbit expansion or Lagrange–Chebyshev rational approximation of Selberg zeta zeros.

**Error Control:** Exponential term in periodic orbit expansion explains good behavior for small values, but **no rigorous error bounds with interval arithmetic.** Convergence is empirical.

**Verdict:** **NUMERICS-ONLY** — Borthwick does NOT certify resonance locations with interval arithmetic or validated numerics.

---

### (B) Analytical Rigorous Proof (Special Geometry): Baskin–Marzuola

**Source:** [Locating resonances on hyperbolic cones](https://arxiv.org/pdf/1608.05278) (Baskin & Marzuola, 2016)

**Method:** Analytic; explicit formulas using Kummer connection formulas for hypergeometric functions and separation of variables.

**Scope:** Hyperbolic manifolds with **conic singularity** (warped-product metric), NOT general Hecke surfaces or Schottky groups.

**Resonances:** Derived exactly in terms of special-function zeros; on-critical-line and off-critical-line locations provable analytically.

**Verdict:** **PRIOR PROOF EXISTS**, but **ONLY for cones**, not Hecke triangle groups or general hyperbolic surfaces. Narrowly scoped.

---

### (C) Verified Hyperbolic 3-Manifold Geometry (SnapPy/HIKMOT): NOT FOR RESONANCES

**Sources:**
- [HIKMOT — Verified computations for hyperbolic 3-manifolds](http://www.oishi.info.waseda.ac.jp/~takayasu/hikmot/)  
- [Verified computations for closed hyperbolic 3-manifolds](https://arxiv.org/pdf/1904.12095)  
- [SnapPy 3.3.2 verification documentation](https://snappy.computop.org/verify.html)

**Method:** Interval Newton method (Krawczyk test) with interval arithmetic on triangulations; verifies hyperbolicity, isometry, and Thurston equation solutions.

**Scope:** Triangulation verification and manifold structure, **NOT spectral resonances.** HIKMOT/SnapPy does not compute or certify resonance locations.

**Verdict:** Interval-arithmetic rigor exists for manifold geometry, **NOT for scattering resonances.**

---

## Synthesis: What Exists vs. What Doesn't

| Question | Status | Citation |
|----------|--------|----------|
| Fredholm determinant tail bound (transfer operators, abstract) | **YES, explicit** | Thm 4.10, arXiv:2602.19435 (Gauss-Kuzmin-Wirsing) |
| Truncation bound for Mayer operator (Hecke/Rosen) | **UNPUBLISHED or unverified** | 0912.2236 exists; theorem NOT accessible |
| Rigorous certified scattering resonance (off-critical-line, hyperbolic surface) | **NO** | See below |
| Analytical rigorous resonance proof (special geometry) | **YES, limited scope** | arXiv:1608.05278 (hyperbolic cones only) |
| Borthwick resonance computations (rigor level) | **NUMERICS-ONLY** | arXiv:2002.03334, 1305.4850 |
| Interval-arithmetic verified resonances (Hecke triangle groups) | **NO** | No prior art found |

---

## Limitations & Unresolved Gaps

1. **PDF Parsing Failure:** Three critical PDFs (Pollicott–Vytnova 1611.09276, Fedosova 2509.17936, Bandtlow 2002.03334) could not be parsed for exact theorem statements. Claims rest on abstracts and secondary summaries.

2. **Mayer Truncation Bound:** Transfer operators for Hecke G_q are studied (arXiv:0912.2236), but explicit quantitative error bound may not be published separately or lies in unparseable source.

3. **Scattering Resonance Lacuna:** Despite Borthwick's numerical work, **no interval-arithmetic or validated-numerics proof of scattering resonance location exists in published literature searched**. This is likely an open problem.

4. **Hecke-Specific Gap:** Work by Pollicott–Vytnova applies to continued fractions (Hausdorff dimension); work by Borthwick applies to Schottky surfaces. **No publication bridges both: certified bounds for Hecke-specific spectral resonances.**

---

## Recommended Next Steps (If Pursuing Certified Resonance Bounds)

1. **Direct contact:** Email Fedosova, Borthwick, Pollicott for Hecke-G_q transfer-operator error bound (explicit formula).
2. **Check arXiv preprints** for 2509.17936 author's draft (may include full theorems).
3. **Revisit Bandtlow's work** on explicit eigenvalue bounds for transfer operators (2007–2012 era; may contain Hecke adaptation).
4. **Consider original route:** Develop interval-arithmetic Krawczyk-type verifier for Fredholm determinant zeros, adapting SnapPy's manifold-verification infrastructure.

---

**Compiled by:** Claude Code, /research-lite mode  
**Evidence weight:** 60% (one explicit theorem located; two-thirds of claims unverified due to PDF parsing failure)  
**Conflict flag:** None among sources.
