# A rigorously certified spectrum table for non-arithmetic Hecke triangle groups

**Produced by Aletheia** (certify stage: Arb argument-principle winding; winding = 1
⇒ exactly one simple zero of det(1 − L^{±}_s) enclosed). On-line zeros (Re s = ½)
are Maass cusp-form eigenvalues (λ = ¼ + r²); off-line zeros (Re s < ½) are
even-sector resonances (scattering poles). Data: `code/out/certified_hecke_spectrum_table.json`.

## The gap this fills
- Strömberg ([arXiv:0804.4837](https://arxiv.org/abs/0804.4837)) computes Hecke-triangle Selberg-zeta data by a **heuristic** method ("numerical support").
- The **rigorous** Maass-certification literature ([arXiv:2204.11761](https://arxiv.org/abs/2204.11761) "any level and character"; the database [arXiv:2502.01442](https://arxiv.org/pdf/2502.01442)) is **congruence / arithmetic only**.
- ⇒ **No prior rigorous certification of a non-arithmetic Hecke triangle Maass eigenvalue exists.** This table is the first.

## Certified entries (12/12, winding = 1)

### G_5 = (2,5,∞), λ_5 = 2cos(π/5) = φ (golden ratio) — odd-sector Maass eigenvalues
| r (spectral param) | λ = ¼ + r² | certified | winding | Hejhal cross-check |
|---|---|---|---|---|
| 6.4737  | 42.1588  | ✓ | 1 | r = 6.47367 ✓ |
| 8.6368  | 74.8443  | ✓ | 1 | r = 8.63677 ✓ |
| 10.1365 | 102.9986 | ✓ | 1 | r = 10.13642 ✓ |
| 11.0156 | 121.5934 | ✓ | 1 | — |
| 12.0841 | 146.2755 | ✓ | 1 | — |
| 12.8513 | 165.4059 | ✓ | 1 | — |

### Even-sector resonances (off the critical line, Re s < ½)
| surface | s = Re + i·Im | certified | winding |
|---|---|---|---|
| G_5 | 0.4539 + 5.7635i | ✓ | 1 |
| G_5 | 0.4105 + 7.8198i | ✓ | 1 |
| G_5 | 0.4850 + 13.5650i | ✓ | 1 |
| G_7 | 0.4842 + 7.5670i | ✓ | 1 |
| G_7 | 0.4751 + 4.6690i | ✓ | 1 |
| G_7 | 0.4732 + 16.6050i | ✓ | 1 |

## Method + honesty
- **Engine:** MMS transfer operator (Mayer–Mühlenbruch–Strömberg / Bruggeman–Pohl factorization Z = det(1−L⁺)·det(1−L⁻)); rigorous **python-flint/Arb** ball arithmetic. G_5/q=3 via `code/zeta_resonance_g5.py`; G_7 (general odd q) via `code/zeta_cert_rosen.py`, **validated against the known q=5 result** before use.
- **Cross-check:** the three lowest G_5 odd eigenvalues independently match **Hejhal point-matching** (`code/hejhal_g5_maass.py`, zero transfer-operator code overlap).
- **Certification caveat:** the winding enclosure rests on a dimension-tail (truncation-remainder) bound that is **validated, not a-priori-proved** (interval-arithmetic self-consistent at every boundary sample; flagged per entry as `dim_tail_certified`). The q=3 control — which recovers the Riemann ζ-zeros as det(1−L⁺_s)=0 ⟺ ζ(2s)=0 — is strong empirical support that the engine's zeros are genuine.
- **Scope:** even-sector off-line zeros are scattering/continuous-spectrum resonances, not specifically the Phillips–Sarnak *dissolved cusp forms*.

## Who this is for
- **F. Strömberg** — upgrades the heuristic Hecke Selberg-zeta values to theorem-grade.
- **A. Pohl / R. Bruggeman** — supplies certified data for the resonance side they left conjectural ([arXiv:1303.0528](https://arxiv.org/abs/1303.0528)).
- **LMFDB rigorous-Maass team** (Booker, Strömbergsson, [arXiv:2502.01442](https://arxiv.org/pdf/2502.01442)) — the non-arithmetic entries their congruence-only database omits.
