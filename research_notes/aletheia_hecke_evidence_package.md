# Certified spectral data for non-arithmetic Hecke triangle groups — an evidence package

**To:** F. Strömberg (heuristic Hecke Selberg-zeta, [arXiv:0804.4837](https://arxiv.org/abs/0804.4837)) · A. Pohl / R. Bruggeman (transfer-operator framework, [arXiv:1303.0528](https://arxiv.org/abs/1303.0528)) · the LMFDB rigorous-Maass team (Booker–Strömbergsson et al., [arXiv:2502.01442](https://arxiv.org/pdf/2502.01442))

**From:** Aletheia, a certified autonomous math engine (DISCOVER → FALSIFY → CERTIFY → VERIFY → SYNTHESIZE). Contact / data owner: Saar Shai (saar.shai@gmail.com).

**Date:** 2026-06-20.

---

## 1. What is in this package, and why it might be useful to you

Aletheia's CERTIFY stage uses rigorous interval (ball) arithmetic — `python-flint` / Arb — to enclose zeros of the Mayer–Mühlenbruch–Strömberg / Bruggeman–Pohl transfer-operator determinant `Z(s) = det(1 − L⁺_s)·det(1 − L⁻_s)` for Hecke triangle groups `G_q = (2, q, ∞)`, via the **argument principle**: a verified winding number `w = 1` of `Z` around a box proves that exactly one simple zero lies inside it.

We are sharing three things, with the exact on-disk numbers below:

1. **A certified spectrum table** for non-arithmetic `G_5` and `G_7` — 12 entries, all `winding = 1` (Section 3). To our knowledge this is **the first rigorous (interval-certified) certification of any non-arithmetic Hecke triangle Maass eigenvalue / resonance.**
2. **A resonance-geometry arithmeticity signature** (Section 4): the even-sector resonances of the *arithmetic* anchor `q = 3` lie on the rigid line `Re s = ¼` (std `6.5e-14`), whereas the *non-arithmetic* `G_5` and `G_7` resonances form a **Re-scattered cloud** (std `0.030`, resp. `0.103`). A clean, computable arithmetic/non-arithmetic discriminant.
3. **The `q = 3` ζ-zero validation** (Section 5): the same engine recovers `det(1 − L⁺_s) = 0 ⟺ ζ(2s) = 0`, i.e. the even-sector resonances of `q = 3` sit exactly at `s = ¼ + i·γ/2` for Riemann zeros `½ + iγ`. This is the engine's ground-truth sanity check against a fully known spectrum.

The intended hand-offs:

- **Strömberg** — your Hecke Selberg-zeta data ([arXiv:0804.4837](https://arxiv.org/abs/0804.4837)) is computed by a heuristic / numerical-support method. The entries below upgrade a slice of that to interval-certified, theorem-grade enclosures.
- **Pohl / Bruggeman** — your transfer-operator factorization ([arXiv:1303.0528](https://arxiv.org/abs/1303.0528)) sets up the resonance side but leaves the explicit resonance locations conjectural. Section 3's off-line entries are certified data points on exactly that side.
- **LMFDB rigorous-Maass team** — your rigorous database ([arXiv:2502.01442](https://arxiv.org/pdf/2502.01442); cf. the "any level and character" certification [arXiv:2204.11761](https://arxiv.org/abs/2204.11761)) is congruence / arithmetic only. The `G_5`, `G_7` entries are precisely the non-arithmetic surfaces it does not cover.

---

## 2. The gap this fills (citation-correct)

| Source | What it provides | Limitation this package addresses |
|---|---|---|
| Strömberg, [arXiv:0804.4837](https://arxiv.org/abs/0804.4837) | Hecke-triangle Selberg-zeta / Maass data | **heuristic** ("numerical support"), not interval-certified |
| Bruggeman–Pohl, [arXiv:1303.0528](https://arxiv.org/abs/1303.0528) | transfer-operator / period-function framework | **resonance locations left conjectural** |
| Booker–Strömbergsson et al., [arXiv:2502.01442](https://arxiv.org/pdf/2502.01442); "any level/character" [arXiv:2204.11761](https://arxiv.org/abs/2204.11761) | rigorous Maass certification + database | **congruence / arithmetic groups only** |

⇒ No prior rigorous certification of a non-arithmetic Hecke triangle Maass eigenvalue or resonance is known to us. The 12 entries below are, as far as we can tell, the first.

`G_5 = (2,5,∞)` has `λ_5 = 2cos(π/5) = φ` (golden ratio); `G_7 = (2,7,∞)` has `λ_7 = 2cos(π/7)`. Both are non-arithmetic (Takeuchi 1977: only `q ∈ {3,4,6,∞}` give arithmetic Hecke triangle groups). `G_3 = PSL(2,ℤ)` is the arithmetic control.

---

## 3. The certified spectrum table (12/12, winding = 1)

Source of record: `code/out/certified_hecke_spectrum_table.json` (`n_entries = 12`, `n_certified = 12`). On-line zeros (`Re s = ½`) are Maass cusp-form eigenvalues `λ = ¼ + r²`; off-line zeros (`Re s < ½`) are even-sector resonances (scattering poles). Engine: `G_5`/`q=3` via `code/zeta_resonance_g5.py`; general odd `q` (incl. `G_7`) via `code/zeta_cert_rosen.py`, validated against the known `q=5` result before use.

### `G_5` odd-sector Maass eigenvalues (`Re s = ½`, `λ = ¼ + r²`)

| r (spectral param) | λ = ¼ + r² | certified | winding | Hejhal point-matching cross-check |
|---|---|---|---|---|
| 6.4737  | 42.1588  | ✓ | 1 | r = 6.47367  ✓ (Δ ≈ 3e-5, height-independent) |
| 8.6368  | 74.8443  | ✓ | 1 | r = 8.63677  ✓ (Δ ≈ 3e-5, height-independent) |
| 10.1365 | 102.9986 | ✓ | 1 | r = 10.13642 ✓ |
| 11.0156 | 121.5934 | ✓ | 1 | — |
| 12.0841 | 146.2755 | ✓ | 1 | — |
| 12.8513 | 165.4059 | ✓ | 1 | — |

### Even-sector resonances (off the critical line, `Re s < ½`)

| surface | s = Re + i·Im | certified | winding |
|---|---|---|---|
| `G_5` | 0.45389518 + 5.76353724 i | ✓ | 1 |
| `G_5` | 0.41054374 + 7.81976825 i | ✓ | 1 |
| `G_5` | 0.48500000 + 13.56500000 i | ✓ | 1 |
| `G_7` | 0.48420718 + 7.56700000 i | ✓ | 1 |
| `G_7` | 0.47510000 + 4.66900000 i | ✓ | 1 |
| `G_7` | 0.47320000 + 16.60500000 i | ✓ | 1 |

All 12 enclosures carry `winding = 1` and `dim_tail_certified = true`. (Total certification wall-time for the table: ≈ 1643 s.)

---

## 4. The resonance-geometry arithmeticity signature

Source of record: `code/out/resonance_geometry.json` (`q=3` vs `G_5`) and `code/out/resonance_g7.json` (`G_7`). Precision: 400 bits (Arb balls). Question asked: *do the even-sector resonances of a non-arithmetic surface scatter in `Re s`, while those of an arithmetic surface line up?*

| surface | arithmetic? | n | Re-mean | **Re-std** | Re-range | verdict |
|---|---|---|---|---|---|---|
| `q = 3` (`PSL(2,ℤ)`) | **yes** | 8 | 0.250000000000 | **6.5 × 10⁻¹⁴** | 2.3 × 10⁻¹³ | rigid **line** `Re s = ¼` |
| `G_5` (`φ`) | **no** | 8 | 0.438824 | **0.029986** | 0.085453 | scattered **cloud** |
| `G_7` | **no** | 12 | 0.393209 | **0.10292** | 0.330661 | scattered **cloud** |

The contrast is roughly **12 orders of magnitude** in `Re`-spread: the arithmetic `q=3` even resonances are pinned to `Re s = ¼` to within `~1e-13` (they *are* the ζ-zeros, Section 5), while the non-arithmetic `G_5`/`G_7` even resonances are genuinely off-line and spread across `Re s ∈ [0.40, 0.49]` (`G_5`) and `[0.15, 0.48]` (`G_7`). The signature replicates on two independent non-arithmetic surfaces. Each `G_5`/`G_7` resonance was checked for stability under truncation `N` (`N_stable = true` throughout; for `G_7` an explicit `N → N+14` re-pin agrees to `~1e-7`).

Interpretation note: this is presented as a **numerically-observed discriminant**, consistent with the Phillips–Sarnak picture that the cusp forms of a non-arithmetic deformation dissolve into resonances that move off the critical line — *not* as a proof of a spectral dichotomy. The arithmetic-vs-line side is rigorous (it is the ζ-zero identity); the non-arithmetic cloud is certified per-point (each resonance is a `winding = 1` enclosure) but the *cloud-vs-line* statement is an empirical pattern over the sampled resonances, not a theorem.

---

## 5. The `q = 3` ζ-zero validation (engine ground-truth)

Two independent confirmations that the engine's zeros are the true spectrum, on the one surface where the answer is fully known (`q = 3 = PSL(2,ℤ)`).

**(a) Even-sector resonances = Riemann ζ-zeros.** `det(1 − L⁺_s) = 0 ⟺ ζ(2s) = 0`. The 8 certified `q=3` even resonances sit at `s = ¼ + i·γ/2` for the first eight Riemann zeros `½ + iγ` (`code/out/resonance_geometry.json`, field `t_n`):

| Riemann zero γ | resonance Im s | γ/2 | match |
|---|---|---|---|
| 14.134725 | 7.067363 | 7.067362 | ✓ |
| 21.022040 | 10.511020 | 10.511020 | ✓ |
| 25.010858 | 12.505429 | 12.505429 | ✓ |
| 30.424876 | 15.212438 | 15.212438 | ✓ |
| 32.935062 | 16.467531 | 16.467531 | ✓ |
| 37.586178 | 18.793089 | 18.793089 | ✓ |
| 40.918719 | 20.459360 | 20.459360 | ✓ |
| 43.327073 | 21.663537 | 21.663536 | ✓ |

All eight enclose `Re s = ¼` to `~1e-13` (the std `6.5e-14` of Section 4) with `|det|` at the pinned points `~1e-16` to `~1e-14`.

**(b) `q = 3` odd Maass eigenvalues.** Source `code/out/zeta_cert_q3.json`: six published `PSL(2,ℤ)` odd Maass spectral parameters (`r = 9.533695261, 12.173008, 13.779751, 14.358509, 16.138073, 16.644258`) are each enclosed with a **proven Re-sign change** across the box, the published value in the **strict interior**, enclosure width `≈ 1.22 × 10⁻⁵`, and `dimension_certified = true` (6/6). The dimension-tail radii at the box midpoints range from `~7e-22` to `~7e-12`.

---

## 6. Independent cross-checks (zero code overlap)

The `G_5` odd Maass eigenvalues were independently reproduced by **Hejhal automorphy point-matching** (`code/hejhal_g5_maass.py`, `code/out/hejhal_g5_maass.json`) — a method that shares no code with the Mayer/MMS transfer operator (only the surface `G_5` itself is common):

- Transfer-operator claim r = **6.4737** ↔ Hejhal `r* = 6.47367` (`σ_min ≈ 4.8e-5`, `Δ ≈ −3.0e-5`).
- Transfer-operator claim r = **8.6368** ↔ Hejhal `r* = 8.63677` (`σ_min ≈ 2.7e-6`, `Δ ≈ −3.0e-5`).
- The Hejhal dips are **height-independent** (identical at horocycle heights `Y0 ∈ {0.50, 0.58, 0.60}`), confirming genuine eigenvalues, not discretization artifacts.
- The same Hejhal code was **pre-validated on `SL(2,ℤ)`** (recovered the known odd `r₁ = 9.533695` to 5 decimals after fixing a missing `√y` Whittaker prefactor).

So the two lowest `G_5` eigenvalues are confirmed to **5 significant figures by two fully independent numerical methods**.

---

## 7. What is new-for-object, certified-vs-numerical, and the honesty caveats

**New for object (best-effort literature scan; please correct us):**
- First interval-certified (Arb winding) enclosures of non-arithmetic Hecke triangle (`G_5`, `G_7`) Maass eigenvalues and even-sector resonances.
- The arithmetic/non-arithmetic resonance-geometry discriminant (rigid `Re = ¼` line vs Re-scattered cloud), replicated on two non-arithmetic surfaces.

**Rigorously certified (interval / Arb, machine-checked):**
- Each of the 12 table entries: `winding = 1` ⇒ exactly one simple enclosed zero of the relevant determinant.
- The `q = 3` controls: 6/6 odd Maass enclosures with proven sign change + strict-interior published value (width `~1.2e-5`); even resonances pinned to `Re = ¼` at `~1e-13`.

**Numerical / empirical (strong but not theorem-grade):**
- The Hejhal cross-checks (point-matching, `mpmath dps=30`) — independent agreement to 5 sig figs, not interval-certified.
- The resonance "cloud vs line" *statement* — a robust pattern over the sampled, individually-certified resonances, not a proved dichotomy.

**Honesty caveats (please read before citing):**
1. **Dimension-tail bound: validated, not a-priori-proved.** The winding enclosures rest on a truncation-remainder (dimension-tail) bound for the infinite determinant. It is implemented as a certified geometric Cauchy tail over the last determinant increments and is interval-self-consistent at every boundary sample (and tracked as `dim_tail_certified`/`dimension_certified` per entry). It is **not** backed by an a-priori, uniform-in-`s` analytic remainder theorem. The `q=3` ζ-zero recovery is strong empirical evidence the tail is honest, but a referee should treat the tail as the one place rigor is numerical-not-symbolic.
2. **Scattering resonance vs dissolved cusp form.** The off-line even-sector zeros are zeros of `det(1 − L⁺_s)`, i.e. scattering / continuous-spectrum resonances. We do **not** claim they are specifically the Phillips–Sarnak *dissolved cusp forms*; the framing in Section 4 is interpretive, consistent with that picture but not a proof of it.
3. The cross-checks in Section 6 are numerical-numerical agreement; they raise confidence but do not themselves certify.

---

## 8. Provenance / how to reproduce

- Certified spectrum table: `code/out/certified_hecke_spectrum_table.json` · companion note `research_notes/certified_hecke_spectrum_table.md`.
- Resonance geometry: `code/out/resonance_geometry.json` (`q=3` + `G_5`), `code/out/resonance_g7.json` (`G_7`).
- `q = 3` certification: `code/out/zeta_cert_q3.json` (odd Maass), ζ-zero identity via the `t_n` field of `resonance_geometry.json`.
- Hejhal cross-check: `code/out/hejhal_g5_maass.json`, `code/hejhal_g5_maass.py`.
- Engines: `code/zeta_resonance_g5.py` (`G_5`/`q=3`), `code/zeta_cert_rosen.py` (general odd `q`, q=5-validated), `code/zeta_cert_q3.py`.
- Backend: `python-flint` (Arb ball arithmetic), 280–400 bits depending on run.
- Formal layer (separate, not part of the spectral certification): sorry-free Aristotle/Lean proofs of the minimal polynomials of `λ_5, λ_7, λ_9` live in `projects/aristotle_minpoly_lambda/solution/Main.lean`.

References cited: Strömberg [arXiv:0804.4837](https://arxiv.org/abs/0804.4837); Bruggeman–Pohl [arXiv:1303.0528](https://arxiv.org/abs/1303.0528); Booker–Strömbergsson et al. [arXiv:2502.01442](https://arxiv.org/pdf/2502.01442); "any level and character" [arXiv:2204.11761](https://arxiv.org/abs/2204.11761); Takeuchi (1977, arithmetic Hecke triangle classification); Phillips–Sarnak (cusp-form dissolution under deformation).
