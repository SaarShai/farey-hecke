# Certified Hecke Maass spectrum — EXTENSION (2026-06-20)

**Extends** the first rigorously interval-certified non-arithmetic Hecke triangle
Maass spectrum table (`research_notes/certified_hecke_spectrum_table.md`,
`code/out/certified_hecke_spectrum_table.json`) with the **first certified
G_7 = (2,7,∞) odd-sector Maass cusp-form eigenvalue**, an independent Hejhal
cross-check, and a prepared Kaggle batch certify-sweep for further extension.

This note is **additive** — it does not modify the published table/JSON or the
evidence package; new artifacts live under `code/out/spectrum_extend/`.

Certification standard is unchanged: **Arb argument-principle winding = 1**
(⇒ exactly one simple zero of `det(1 − L^{sign}_s)` enclosed in the box,
`det ≠ 0` certified on the box boundary in Arb balls, dimension tail certified).

---

## NEW certified entries — G_7 odd Maass eigenvalues (k = 1, k = 2)

**Two** new G_7 odd-sector Maass eigenvalues certified **locally** this session
(Arb winding = 1 + certified dim-tail), `code/zeta_cert_rosen.py`, N = 22,
n_head = 4:

| surface | sector | k | r* (Re s = ½) | λ = ¼ + r² | winding | winding ball | dim-tail | located |det⁻| | artifact |
|---|---|---|---|---|---|---|---|---|---|
| G_7 = (2,7,∞) | odd (mms−) | 1 | **5.921981251** | 35.31986 | **1** | [0.99999963, 1.00000037] | certified | 5.46e−12 | `certified_g7_odd.json` |
| G_7 = (2,7,∞) | odd (mms−) | 2 | **7.933888770** | 63.19659 | **1** | [0.99998459, 1.00001541] | certified | 1.26e−11 | `certified_g7_odd_k2.json` |

- λ_7 = 2 cos(π/7) ≈ 1.8019377358; q = 7 ⇒ h_q = 2, κ = 5 ⇒ a 110×110 Arb-ball
  determinant at N = 22. Boxes: Re s ∈ ½ ± 8e−5, r ∈ r* ± 8e−5.
- For k = 1 the even sector (mms+) has |det⁺| = **1.797** at r* — confirms it is
  an **odd** zero, not an even one.

- λ_7 = 2 cos(π/7) ≈ 1.8019377358; q = 7 ⇒ h_q = 2, κ = 5 ⇒ a 110×110 Arb-ball
  determinant at N = 22.
- **Winding ball** = [0.9999996330589, 1.0000003688037] → winding = 1, certified.
  Box: Re s ∈ ½ ± 8e−5, r ∈ 5.921981 ± 8e−5; tail_fix = 2.79e−12.
- Located |det⁻| at r* = **5.46e−12** (certified engine, N = 22, n_head = 4).
- The even sector (mms+, sign = +1) has |det⁺| = **1.797** at the same r* —
  confirms this is an **odd** zero, not an even one.
- **Why this is new:** the published table carried only G_7 *even-sector
  resonances* (off-line scattering poles); it had **no G_7 odd Maass eigenvalue
  on the critical line**. These are the first two certified ones.
- Artifacts: `code/out/spectrum_extend/certified_g7_odd.json` (k=1, driver
  `code/spectrum_extend/cert_g7_odd.py`); `certified_g7_odd_k2.json` (k=2).
- Engine self-check before the claim: the general-odd-q certified builder
  reproduces the hard-coded q = 5 engine **bit-for-bit** (max midpoint diff =
  0.0, all balls overlap) — `selfcheck_q5` in the JSON.

### Independent cross-check (Hejhal point-matching — zero TO code overlap)

| method | r* | σ_min at dip | diff vs certified |
|---|---|---|---|
| Arb winding (this work) | 5.921981251 | — | — |
| Hejhal automorphy point-matching | 5.922010656 | 3.83e−5 | **+2.97e−5** |

- `code/spectrum_extend/hejhal_g7_crosscheck.py` →
  `code/out/spectrum_extend/hejhal_g7_maass.json`.
- Reuses the **validated** `code/hejhal_g8_maass.py` machinery (parametrized by
  λ): the *same* code reproduces SL(2,ℤ) odd Maass r₁ = 9.533695 to 5 decimals
  and the published G_5 / G_8 eigenvalues to 5 sig figs. It imports **none** of
  the Mayer/MMS transfer-operator code — the only shared object is the surface.
- The **+2.97e−5** offset is the *identical* systematic grid-resolution bias the
  Hejhal harness shows against the modular anchor and against G_5/G_8 (see
  `hejhal_g8_maass.json` `diff_from_TO`), i.e. it is the expected method bias,
  not a discrepancy. **The two fully independent methods agree to 5 sig figs.**
- G_7 geometry: FD corner y_corner = √(1 − (λ/2)²) ≈ 0.43388; horocycle height
  Y0 = 0.34 (below the corner); M = 18, Q = 44, dps = 30.

---

## Further G_7 odd eigenvalues (located, certify-ready)

Double-precision MMS (`code/zeta_mayer_rosen.py`, the validated odd-sector
locator) shows additional N-stable G_7 odd zeros beyond k = 1, at approximately

| k | r* | λ = ¼ + r² | status |
|---|---|---|---|
| 1 | 5.921981251 | 35.3199 | **CERTIFIED (winding=1)** |
| 2 | 7.933888770 | 63.1966 | **CERTIFIED (winding=1)** |
| 3 | 9.185710 | 84.6273 | located (N-stable), certify-ready |
| 4 | 10.229170 | 104.875 | located (N-stable), certify-ready |
| 5 | ≈10.90 | ≈119.06 | coarse-scan minimum only |
| 6 | ≈11.80 | ≈139.49 | coarse-scan minimum only |

k3/k4 are N-stable (refined values agree at N=18 and N=22 to 5 decimals); k5/k6
are coarse-scan minima only. **k3–k4 are located, not yet certified** — they are
the batch the prepared Kaggle kernel certifies (winding + dim-tail) in one job.

---

## Prepared Kaggle batch certify-sweep (NOT pushed)

`kaggle_kernels/hecke_spectrum_extend/` — a **certification** kernel (Arb
interval), distinct from the existing `hecke_highr_sweep` which is double-prec
*location* only.

- `hecke_spectrum_extend.py` — embeds the two repo certified engines
  (`zeta_cert_rosen_q5.py` + `zeta_cert_rosen.py`) as strings, writes them to
  `/kaggle/working` at runtime so the import graph resolves, `pip install
  python-flint`, then runs a **locate → winding=1 → dim-tail** certify loop over
  a candidate batch (G_7 odd k1–k4; k1/k2 already certified locally and serve as
  in-kernel regression, k3/k4 are the new targets; G_5 k1 regression anchor).
  Per-candidate incremental checkpoint to `hecke_spectrum_extend_partial.json`.
- `kernel-metadata.json` — `saarshai/hecke-spectrum-extend-certify`, CPU,
  `enable_internet: true` (needed for the python-flint pip install).
- **Embedded engines verified byte-identical to the repo sources** (ast
  literal-eval compare: Q5 match = True, CR match = True).
- **Smoke-tested locally end-to-end** (q = 5 anchor, N = 14): the kernel wrote
  both engines, imported them, self-checked (max midpoint diff 0.0), located
  r* = 6.473700 and **certified winding = 1** in 34 s. The full batch at N = 22
  is sized for the Kaggle CPU budget (G_7 k1 winding box took 197 s locally).

The main loop should push this kernel and fetch
`/kaggle/working/hecke_spectrum_extend.json`, then fold any winding=1 entries
into the published table.

---

## Retained honesty caveats (unchanged from the original package)

1. **dim-tail = validated, not a-priori-proved.** The winding enclosure rests on
   a dimension-tail (truncation-remainder) bound that is interval-self-consistent
   at every boundary sample and flagged per entry (`dim_tail_certified` /
   `dimension_certified`), but is not a closed-form a-priori proof. The q = 3
   control (recovering the Riemann ζ-zeros as `det(1−L⁺_s)=0 ⟺ ζ(2s)=0`) is the
   strong empirical support that the engine's zeros are genuine.
2. **Even-sector off-line zeros are scattering / continuous-spectrum
   resonances**, not specifically the Phillips–Sarnak *dissolved cusp forms*.
   (G_7 even resonances were certified in the original table; this extension adds
   the *odd Maass* side for G_7.)
3. **k3/k4 + any G_9 probe are LOCATED, not yet certified**: the kernel certifies
   a candidate only if its located min is deep (|det| < 1e−3) AND winding = 1;
   otherwise it records *not a zero here*. Do not claim k3/k4 (or G_9) until the
   kernel returns winding = 1 for them.

## Provenance of every number in this note

- `code/out/spectrum_extend/certified_g7_odd.json` — k=1: winding=1,
  r* = 5.921981251, |det⁻| = 5.46e−12, even |det⁺| = 1.797, dim-tail certified.
  Ran this session (`python3 code/spectrum_extend/cert_g7_odd.py`, wall 197 s).
- `code/out/spectrum_extend/certified_g7_odd_k2.json` — k=2: winding=1,
  r* = 7.933888770, |det⁻| = 1.26e−11, dim-tail certified. Ran this session
  (wall ≈ 200 s).
- `code/out/spectrum_extend/hejhal_g7_maass.json` — Hejhal r* = 5.922010656,
  σ_min = 3.83e−5, diff +2.97e−5. Ran this session (wall 136 s).
- Kernel smoke: `/private/tmp/.../out/hecke_spectrum_extend.json` (q=5 anchor,
  certified=True, winding=1). Ran this session.
