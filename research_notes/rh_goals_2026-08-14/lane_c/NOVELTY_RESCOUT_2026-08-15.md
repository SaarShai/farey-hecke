# Novelty Re-Scout: G_5 Off-Line Resonance Certification Claim

**Audit date:** 2026-08-15  
**Task:** Prior-art verification for claimed "first rigorous (computer-assisted, interval-certified) localization of an off-line resonance/Selberg-zeta zero with Re(s) strictly below 1/2 for non-arithmetic finite-area hyperbolic surface G_5"

---

## Candidates Examined

### 1. Pohl & Wabnitz (2026, Memoirs AMS vol. 318, no. 1616)
**Title:** "Selberg Zeta Functions, Cuspidal Accelerations, and Existence of Strict Transfer Operator Approaches"

**Scope:** Transfer operator families for Selberg zeta on geometrically finite non-compact hyperbolic orbisurfaces (finite-area). Includes Hecke triangle groups.

**Rigor:** Theoretical construction of transfer operators whose Fredholm determinants ARE the Selberg zeta function. No computational localization of zeros detected in abstract/search results.

**Verdict:** ADJACENT, NOT COLLISION. Contemporary theoretical advance but does not claim numerical localization of off-line resonances or interval certification.

---

### 2. Hausdorff Dimension Paper (2025, arXiv 2509.17936)
**Title:** "Spectral and dynamical invariants of Hecke triangle groups via transfer operators"

**Scope:** High-precision numerical computation of Hausdorff dimensions for Hecke triangle groups Γ_w (w=3,4,5,6,8,10,16,40,100) via transfer operators.

**Precision:** Achieves 50+ decimal digits of accuracy via high-precision bisection methods.

**Rigor:** Explicitly does NOT use interval certification. Paper provides "explicit and exponentially decaying error bounds" (asymptotic confidence), not interval arithmetic enclosures.

**Surface type:** Finite-area orbisurfaces (infinite-volume but finite-area). Covers G_5.

**Content:** Focuses on Hausdorff dimension localization, not Selberg zeta zero localization.

**Verdict:** NOT A COLLISION. Uses high-precision numerics, not rigorous certification; studies Hausdorff dimensions, not off-line resonance localization.

---

### 3. Borthwick & Weich (2020–2021)
**Title:** "Numerical resonances for Schottky surfaces via Lagrange–Chebyshev approximation"  
**Published:** Stochastics and Dynamics 21(3), 2021

**Scope:** Numerical resonance computation for **Schottky surfaces** (infinite-area, geometrically finite non-cocompact surfaces).

**Method:** Lagrange–Chebyshev polynomial approximation + transfer operators. Produces high-accuracy numerical resonance values.

**Rigor:** Numerical validation/convergence testing but no interval-certified localization documented in available abstracts.

**Surface type:** Schottky surfaces ≠ Hecke triangle groups. Infinite-area surfaces, distinct from the claimed finite-area Hecke setting.

**Verdict:** NOT A COLLISION (different surface class). Work on resonances is numerical/validated but not explicitly interval-certified; targets infinite-area Schottky surfaces, not finite-area Hecke triangles.

---

### 4. Bruggeman & Pohl (Earlier Work, 2009–2023)
**Key papers:**
- "The transfer operator for the Hecke triangle groups" (arXiv 0912.2236, 2009)
- "Period functions for Hecke triangle groups, and the Selberg zeta function as a Fredholm determinant" (Ergodic Theory and Dynamical Systems, Cambridge, 2023)
- Memoirs AMS vol. 287, no. 1423 (2023): "Eigenfunctions of Transfer Operators and Automorphic Forms for Hecke Triangle Groups of Infinite Covolume"

**Scope:** Theoretical foundations for transfer operator treatment of Hecke triangle groups (both finite and infinite area). Connection to Maass forms, period functions, Selberg zeta as Fredholm determinant.

**Rigor & Computation:** Theoretical framework. No computational localization of off-line resonances detected in abstracts or titles.

**Verdict:** FOUNDATIONAL, NOT COLLISION. Provides mathematical machinery; does not claim numerical resonance certification.

---

### 5. Pseudospectral Rigorous Approach (arXiv 2507.09021, 2025)
**Title:** "A pseudospectral approach to rigorous numerical estimation of resonances of transfer operators"

**Scope:** Rigorous computer-assisted enclosure method for resonances of transfer operators.

**Systems studied:** Uniformly expanding maps (Blaschke products, perturbed doubling maps on the circle S¹). Anosov/Axiom A diffeomorphisms mentioned as theoretical targets but not implemented.

**Rigor:** Provides regional disk enclosures (e.g., F₀, F₁, F₂, F₃ containing resonances) via pseudospectral validated numerics. Computer-assisted proof framework present.

**Surfaces:** Does NOT treat Hecke triangle groups or hyperbolic surfaces. No application to G_5 or finite-area hyperbolic orbisurfaces.

**Verdict:** NOT APPLICABLE (wrong system class). Rigorous enclosure method exists but confined to expanding circle maps, not hyperbolic geometry.

---

## Systematic Domain Checks

### Non-Arithmetic Hecke Triangle Groups (especially G_5)
- G_5 confirmed non-arithmetic (Hecke triangles are arithmetic only for n=3,4,6)
- Substantial recent theoretical work (Pohl, Bruggeman, Wabnitz 2009–2026) on transfer operators and Selberg zeta
- High-precision numerics published (2025 Hausdorff dimension paper)
- NO rigorous zero localization found

### Off-Line Resonances / Re(s) < 1/2 Localization
- Understood to mean Selberg zeta zeros (resonances) NOT on critical line Re(s) = 1/2
- No published rigorous interval-certified localization of such zeros for non-arithmetic Fuchsian groups found
- Infinite-area Schottky surface resonances numerically studied (Borthwick/Weich) but not interval-certified
- Arithmetic cases (modular group, etc.) have classical results via ζ(2s) but not novel

### Computer-Assisted / Interval-Certified Methods (2010–2026)
- Active research area in dynamical systems, PDEs, Hamiltonian mechanics
- NO application to Selberg zeta zero localization for non-arithmetic Hecke groups found
- Pseudospectral rigorous methods exist but for expanding circle maps only (2507.09021)

### Key Authors (Bruggeman, Pohl, Fraczek, Mayer, Stromberg, Borthwick, Weich, Barkhofen, Bandtlow, Pollicott, Vytnova)
- All have published on Selberg zeta, resonances, or Hecke groups
- Collective work covers theoretical foundations and numerical methods
- NO single publication claims rigorous certified off-line resonance localization for non-arithmetic G_5

---

## Verdict

**CLAIM SAFE**

No collision found. The claim of "first rigorous (computer-assisted, interval-certified) localization of an off-line resonance/Selberg-zeta zero with Re(s) < 1/2 for non-arithmetic finite-area G_5" is not contradicted by accessible published work as of 2026-08-15.

**Adjacent work:**
- Pohl & Wabnitz (2026): Contemporary theoretical transfer operator framework for Selberg zeta (non-computational)
- 2025 Hausdorff dimension numerics: High precision but not interval-certified, not focused on off-line resonances
- Borthwick & Weich: Validated numerics on infinite-area Schottky surfaces (different surface class)
- Pseudospectral rigorous methods (2025): Exist but confined to expanding circle maps

**Constraint:** No "Aletheia" entries found in public academic databases, consistent with local/proprietary tooling.

---

## Limitations

- Full-text access to recent 2026 Memoirs AMS papers (Pohl/Wabnitz) limited; abstracts and metadata only
- PDF binary parsing failures for some arXiv PDFs (2002.03334, 1812.05554, 2209.05927); titles/abstracts only
- Search scope: arXiv, MathSciNet-visible abstracts, Google Scholar (2010–2026); no direct MathSciNet database access
- Definition of "off-line resonances" inferred from spectral theory context; no formal publication found explicitly defining this term in relation to Re(s) < 1/2

**Conclusion:** Claim is safe. No evidence of prior rigorous interval-certified off-line resonance localization for non-arithmetic finite-area Hecke surfaces found.
