---
schema_version: 2
title: Independent Hejhal confirmation of G_5 odd Maass spectrum (transfer-operator eq.34)
type: fact
domain: experiments
tier: semantic
confidence: 0.95
created: 2026-06-20
updated: 2026-06-20
verified: 2026-06-20
sources:
  - code/hejhal_g5_maass.py
  - code/out/hejhal_g5_maass.json
tags:
  - hecke
  - G_5
  - maass
  - hejhal
  - transfer-operator
  - spectrum
  - verification
  - golden-ratio
---

## VERIFIED FINDING

The project's Mayer transfer-operator computation of the first odd Maass spectral parameters for G_5 (Hecke triangle group with λ₅ = 2cos(π/5), the golden ratio) has been **independently confirmed** via Hejhal's automorphy point-matching algorithm.

### Transfer-Operator Claim (eq. 34)
- r₁ = 6.4737, r₂ = 8.6368, r₃ = 10.1365, r₄ = 11.0156, r₅ = 12.0841, r₆ = 12.8513
- Each corresponds to eigenvalue λ = 1/4 + r²

### Hejhal Confirmation (Independent Method)
Five-figure match on the first two odd eigenvalues:
- **r₁ˢ = 6.47367** (TO claim 6.4737, diff −0.00003)
  - Smallest singular value dip: 4.8e−5 (refined to grid dip 4.05e−7)
- **r₂ˢ = 8.63677** (TO claim 8.6368, diff −0.00003)
  - Smallest singular value dip: 2.7e−6 (grid dip 1.7e−5)

### Method: Automorphy Point-Matching
- Odd (sine) Fourier expansion: u = √y ∑_{n≥1} aₙ K_{ir}(2πny/λ) sin(2πnx/λ)
- Horocycle height Y₀ = 0.5; M ∼ 17–18 Fourier modes; Q ∼ 42–44 collocation points
- Pullback into fundamental domain |z| ≥ 1, |Re z| ≤ λ/2 via nearest-λ translation + S-inversion
- Indicator: smallest singular value of column-normalized implicit-automorphy matrix W(r) = I − C(r)
- Implementation: numpy/scipy/mpmath (dps=30), no transfer-operator code reused
- Eigenvalue location: grid scan + golden-section refinement

### Validation
- **Modular group test (SL(2,Z), λ = 1)**:
  - First odd Maass r₁ = 9.533695 (refined 9.53370) ✓ matches documented value
  - r₂ = 12.173008 at grid resolution
  - Confirms implementation fidelity before trusting G₅ results

### Critical Bug Found & Fixed
The **sqrt(y) Whittaker/Maass prefactor** must appear on the implicit-automorphy (pulled-back) side:
- Since u = √y·(·), automorphy carries √Y₀ on the sample side vs √y* on the pulled-back side
- **Omission produced Y₀-dependent eigenvalue offset:**
  - Y₀ = 0.5 → offset +0.176
  - Y₀ = 0.7 → offset +0.096
  - Y₀ = 0.85 → offset −0.084
  - Mode-independent, indicating systematic error
- **After adding the factor, offset vanished:**
  - Y₀ = 0.5 and Y₀ = 0.6 both yield exactly 6.4737
  - Height-independence is the signature of genuine eigenfunction vs discretization artifact

### Conclusion
**CONFIRMED.** The transfer-operator odd-q formula (eq. 34) is independently corroborated for G₅'s first two odd Maass eigenvalues via a completely different numerical method. This closes the residual credibility uncertainty for the low end of the odd-q spectrum.

**Note:** The two highest claimed values (r₅ = 12.08, r₆ = 12.85) were not independently verified in this run.

### Files
- Implementation: `/Users/za/Documents/farey-hecke/code/hejhal_g5_maass.py`
- Output: `/Users/za/Documents/farey-hecke/code/out/hejhal_g5_maass.json`
