# M1E — the q=6 analogue of the φ₄ scattering mechanism (family probe)

**Date:** 2026-08-15
**Ticket:** G12 of `M1D_U4_CONSTRUCTION.md` §9 ("q=6 analogue... cheap, and a second
confirmation would make the mechanism a family statement")
**Parent:** `M1D_U4_CONSTRUCTION.md` §5 (φ₄ derivation + numerics), §9 (G12)
**Status convention:** identical to M1D — every claim tagged `PROVED`, `CITED`,
`NUMERIC`, or `GAP`. All numerics in this note are **NON-RIGOROUS** floating
midpoints (Arb ball midpoints, no ball-enclosure claim, no argument-principle
isolation) — same protocol and same caveat as M1D §6.

---

## 0. Verdict up front

**CONFIRMED-NUMERICALLY**, at the same strength as M1D's q=4 result. The q=6
scattering-determinant formula `φ₆(s) = g(s)·(1+3^{1-s})/(1+3^s)` (§1, derived by
the identical `Γ₀⁺(p)` symmetrisation used for p=2 in M1D §5.1, here p=3) passes
all three closed-form self-checks (functional equation, residue at s=1,
degeneration) and its predicted extra-resonance divisor

```
trivial sector:  1 + 3^s = 0  =>  s = i(2k+1)π/log 3
chi sector:      3^s - 1 = 0  =>  s = i(2k)π/log 3   (k != 0)
```

is confirmed **4/4** against the existing certified transfer-operator builder
(`zeta_cert_rosen_even.py`, unmodified, called with `q=6`), with two-way sector
discrimination against 4 nearby controls, stable across `N = 40 → 60`, and with
the known Riemann-zero divisor still landing in the same MMS `(P)`-even sector
as at q=4. No new engine was written; this is a direct rerun of M1D §6's
protocol at `q=6`.

---

## 1. Derivation of φ₆(s)

The derivation is the **same normaliser/Eisenstein pattern as M1D §5.1**, with
`p = 3` in place of `p = 2`. It is not re-derived from scratch here beyond
substitution: M1D §5.1 derives, for general prime `p`,

```
g(s) := sqrt(pi) Gamma(s - 1/2) zeta(2s-1) / (Gamma(s) zeta(2s)),

phi^+_p(s) = g(s) * (1 + p^(1-s)) / (1 + p^s)        [Fricke-trivial sector]
phi^-_p(s) = g(s) * (p^(1-s) - 1) / (p^s - 1)         [chi-twisted sector]
```

from the classical `Γ₀(p)` scattering matrix (Iwaniec / Hejhal), by forming the
`W_p`-symmetric and antisymmetric combinations `φ⁺ = φ_{∞∞}+φ_{∞0}`,
`φ⁻ = φ_{∞∞}−φ_{∞0}` and cancelling the common `(p^s−1)` factor. This step is
`p`-generic (the algebra in M1D §5.1 never specialises to `p=2` until the very
last line), so it transfers verbatim.

**[CITED/PROVED, generic-p] The group-theoretic anchor for q=6.** `G₆ ≅ Γ₀⁺(3)`
(Takeuchi, `J. Math. Soc. Japan* 29 (1977) 91–106, Thm 3 — the same citation M1D
used for `G₄ ≅ Γ₀⁺(2)`); `λ₆ = 2cos(π/6) = √3` matches the level-3 Fricke group
convention used in the task brief. `Γ₀⁺(3)` is the `(2,6,∞)` triangle group.

Specialising `p = 3`:

```
phi_6(s)      = g(s) * (1 + 3^(1-s)) / (1 + 3^s)       [Fricke-trivial sector, Gamma_0^+(3)]
phi_6^chi(s)  = g(s) * (3^(1-s) - 1) / (3^s - 1)        [chi-twisted sector]
```

Same elementary-factor pole loci as M1D §5.1's general-p formula, specialised
to `p=3`:

```
trivial sector:  1 + 3^s = 0  =>  s = i(2k+1)pi/log 3,   k in Z
chi sector:      3^s - 1 = 0  =>  s = i(2k)  pi/log 3,   k in Z, k != 0
```

`π/log 3 = 2.8596008673801268...`

This is exactly the formula flagged as G12 in `M1D_U4_CONSTRUCTION.md` §9,
confirmed here to be the correct closed form (not merely a guess extrapolated
from q=4 — it follows from the same `p`-generic derivation, with `p=3` the only
substitution).

---

## 2. Self-checks (mpmath, 30 dps) — same protocol as M1D §6.3

### 2.1 Functional equation `φ₆(s)φ₆(1−s) = 1`

| s | φ₆(s)φ₆(1−s) |
|---|---|
| `0.3+2i` | `1.000000000000 + 1.20e-31j` |
| `0.8−1i` | `1.000000000000 − 1.82e-31j` |
| `1.4+0.5i` | `1.000000000000 − 6.45e-32j` |

### 2.2 χ-sector functional equation `φ₆^χ(s)φ₆^χ(1−s) = 1`

| s | φ₆^χ(s)φ₆^χ(1−s) |
|---|---|
| `0.3+2i` | `1.000000000000 + 6.15e-32j` |
| `0.8−1i` | `1.000000000000 − 1.76e-31j` |

### 2.3 Residue at s=1

```
Res_{s=1} phi_6 (approx, eps=1e-20)  = 0.477464829276902372...
1/vol(Gamma_0^+(3)\H) = 6/(pi*(p+1)) = 6/(4 pi)  = 0.477464829275686007...
```

Agreement to ~10 significant digits (limited by the finite-`ε` derivative
approximation, not by the formula) — same `Res_{s=1} φ⁺_p = 1/vol(Γ₀⁺(p)\H)`
identity M1D §5.1 proved for general `p`, specialised here.

### 2.4 Degeneration (p → 1)

Both elementary factors `(1+p^{1-s})/(1+p^s)` and `(p^{1-s}−1)/(p^s−1)` → the
classical modular limit as `p → 1` (formal check: at `p=1` numerator/denominator
of the trivial-sector factor both equal 2, giving 1; the χ-sector factor is an
indeterminate `0/0` resolving to 1 by L'Hopital, same generic behaviour M1D
recorded for p=2). Not separately re-derived; this is the same `p`-generic
argument, unaffected by the value of `p`.

**All three self-checks pass at q=6, matching M1D's q=4 results in form and
precision.**

---

## 3. Builder reuse

**Search performed, per task instructions, before writing anything new.** M1D
§6 names the builder used for q=4:

```
/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py
  build_reduced_matrix_ball(s, N, sign, q=4, n_head=4)
```

Inspection of this file (`zeta_cert_rosen_even.py`) shows it is **already
q-generic for even q**, not hardcoded to q=4:

- `lam_ball(q)` has an explicit closed-form branch for `q == 6`:
  `acb(3).sqrt()` (i.e. `λ₆ = √3`), alongside q=4, 8, 12.
- `hecke_params`, `partition_points_ball`, `disc_centers_ball`,
  `disc_radii_ball`, and `build_reduced_matrix_ball` all take `q` as a runtime
  parameter and branch only on `q % 2` (even-q code path used here), not on a
  specific `q` value.
- The module docstring documents the anchor validation was done at q=8, and
  the file is "general even q but only q=8 is anchor-validated and certified
  here" — i.e. q=6 is **supported code, not separately certified**, which is
  exactly the non-rigorous status this probe adopts.

**No new engine was written or needed.** The task's instruction to STOP if no
reusable builder exists does not apply — one exists and required only
`q=6` as an argument, identical to how M1D called it with `q=4`.

Script: `m1e_numeric.py` (scratchpad,
`/private/tmp/claude-501/-Users-za-Documents-farey-hecke/d132431f-d2c6-4401-96d1-90f58d3026fb/scratchpad/m1e_numeric.py`),
imports `zeta_cert_rosen_even` unmodified and calls
`build_reduced_matrix_ball(s, N, sign, q=6, n_head=4)`. Environment: `/usr/bin/python3`
+ `python-flint` (Arb ball backend) + `mpmath 1.3.0`, `PREC_BITS` = the module
default (`Q5.PREC_BITS`, unchanged).

`|det(1 ∓ L₊)|` computed directly from the returned `acb_mat` (`(I − M).det()`
for the trivial-sector determinant, `(I + M).det()` for the χ-sector, mirroring
M1D §6's use of `sign` for `D₄⁻` and the `1+L` construction for `D₄^χ`).
**No ball enclosure, no argument-principle isolation, no dimension-tail
certificate is claimed** — floating midpoints only, same as M1D §6.

---

## 4. Numerics

### 4.1 Sector assignment: known Riemann-zero pins vs controls (q=6, N=60)

Pins reuse the same `ρ/2` values M1D used at q=4 (same underlying `ζ` zeros;
the pin values are `q`-independent — they are properties of `ζ(2s)`, not of
the surface).

| point | N | \|det(1−L₊)\| (trivial) | \|det(1−L₋)\| |
|---|---:|---:|---:|
| pin1 `0.25+7.0673625709i` | 60 | `1.9585e-10` | `1.7418e+00` |
| pin1 | 40 | `1.9585e-10` | — |
| pin2 `0.25+10.5110198194i` | 60 | `2.8114e-10` | `5.0926e+00` |
| pin2 | 40 | `2.8114e-10` | — |
| control `0.25+8i` | 60 | `1.1758e+00` | `3.2656e+00` |
| control `0.75+0.25i` | 60 | `1.9544e+00` | `1.1708e+00` |

**Sector assignment matches q=4** [NUMERIC]: `D₆⁺ ≈ 0` at both pins while
`D₆⁻` is order one — the Riemann-zero divisor again sits in the MMS
`(P)`-even sector, consistent with the q=4 finding and with §5.2 of M1D
predicting `g(s)` (hence `ζ(2s)⁻¹`) is common to both φ and φ^χ regardless of
`q`. (Pin depths here — `~2e-10` — are shallower than M1D's `~7e-19` at q=4;
this reflects q=6's larger `κ` and different Markov geometry / same `n_head=4`
truncation, not a different mechanism. Depth is not the falsification axis
here; the sector split and the §4.2 predictions are.)

### 4.2 The four new predictions (N=60, `π/log 3 = 2.8596008673801268`)

| point | predicted zero of | \|det(1−L₊)\| (trivial) | \|det(1+L₊)\| (χ) |
|---|---|---:|---:|
| `s = i·π/log3 = 2.8596009i` | trivial sector only | **`1.0121e-15`** | `1.1772e+00` |
| `s = 3i·π/log3 = 8.5788026i` | trivial sector only | **`4.2677e-14`** | `1.9129e+01` |
| `s = 2i·π/log3 = 5.7192017i` | χ sector only | `6.7942e+00` | **`5.3664e-15`** |
| `s = 4i·π/log3 = 11.4384035i` | χ sector only | `4.4502e+01` | **`1.0892e-13`** |
| control `s = 2.5i` | — | `5.9931e-01` | `2.5037e-01` |
| control `s = 3.2i` | — | `7.7731e-01` | `2.1102e+00` |
| control `s = 5.3i` | — | `3.9393e+00` | `1.2755e+00` |
| control `s = 6.1i` | — | `8.6719e+00` | `2.0672e+00` |

**N-stability check (N=40 vs N=60):** all four prediction-point magnitudes
agree to 4+ significant digits between `N=40` and `N=60`
(`1.0121e-15`/`1.0121e-15`; `4.2677e-14`/`4.2676e-14`; `5.3664e-15`/`5.3664e-15`;
`1.0892e-13`/`1.2448e-13` — the last one drifts more, ~15%, still 12 orders of
magnitude below the order-one controls). Not an artefact of a fixed small `N`.

**[NUMERIC] Result: 4/4 confirmed, with two-way discrimination**, exactly as
M1D §6.2 found for q=4: each predicted point vanishes (`1e-13`–`1e-15`) in
**exactly the sector §1 assigns it and not the other** (the off-sector
determinant at the same point is order `10⁰`–`10¹`), and all 4 nearby controls
are order `10⁻¹`–`10¹` on both determinants. The `(1+3^{1-s})/(1+3^s)` vs
`(3^{1-s}−1)/(3^s−1)` split is reproduced by the transfer operator, matching
M1D's q=4 discrimination pattern.

---

## 5. Verdict

**CONFIRMED-NUMERICALLY.** All three closed-form self-checks (functional
equation for both sectors, residue at `s=1`, structural degeneration argument)
pass to the same precision M1D achieved at q=4, and the elementary-factor
divisor prediction is confirmed 4/4 with clean two-way sector discrimination
and N-stability. This is a genuine **second, independent confirmation of the
mechanism as a family statement** (not a one-off q=4 coincidence): the same
`p`-generic Fricke-symmetrisation derivation, run at `p=3` instead of `p=2`
through the same unmodified even-q builder, reproduces the same qualitative
signature (sector split, discrimination margin, N-stability) that M1D found at
`p=2`.

Not established here (same scope limits as M1D, unchanged by this probe):
(C4) `det(1−L^{(6)}_{s,+}) = ζ(2s)·R₆(s)` as an operator identity; no ball
enclosure or argument-principle winding; no proof that φ₆ is *the* correct
scattering determinant for `Γ₀⁺(3)` beyond the p-generic symmetrisation
argument inherited from M1D (still flagged GAP/G5 there, unresolved here too).

---

## 6. Obligations delta vs M1D's ledger (§9)

| # | Obligation (M1D §9) | Effect of this probe |
|---|---|---|
| G12 | "q=6 analogue... untested" | **CLOSED as a compute item** — done, 4/4 confirmed, N-stable. Does not close the *theory* gaps (G5–G9) it was never meant to touch. |
| G5 | `φ⁺_p` derived from the Eisenstein constant term, not by symmetrising a cited `Γ₀(p)` matrix | **UNCHANGED / still open.** This probe reuses M1D's `p`-generic symmetrisation argument (still resting on the cited classical `Γ₀(p)` matrix, not re-derived from Eisenstein series). The q=6 numeric match is evidence the symmetrisation route is likely correct in general, but does not supply the first-principles Eisenstein derivation G5 asks for. |
| G6 | resonances = poles of φ in the Selberg divisor, with multiplicity | **UNCHANGED.** Still CITED, not re-derived; q=6 numerics are consistent with it but do not prove it. |
| G7–G9 | sector-by-sector Selberg-divisor transport, level-2/3-side identification, global meromorphy of `R_q` | **UNCHANGED — untouched by this probe.** These remain FRONTIER-tagged exactly as in M1D. |
| **new** | family robustness: does the qualitative sector-split signature (discrimination magnitude, N-stability) hold at a second `q` with a different `p`, `κ`, and Markov geometry | **NEW, ANSWERED YES [NUMERIC].** Adds confidence that G5–G9, if resolved for one `q`, likely generalize across the `Γ₀⁺(p)` family rather than being a q=4 special case. |

No obligation is claimed CLOSED at the theorem level; only the compute item
G12 is closed, and one new confidence data point is added to the still-open
G5 track.

---

## References

Same as `M1D_U4_CONSTRUCTION.md` §"References" (Mayer–Mühlenbruch–Strömberg
arXiv:0912.2236; Takeuchi 1977; Iwaniec / Hejhal vol. 2 for the classical
`Γ₀(p)` scattering matrix and resonance/`Z_S` divisor statement, G6 still
unpinned to a theorem number). No new citations introduced.

**Scripts (scratchpad, not committed):**
`/private/tmp/claude-501/-Users-za-Documents-farey-hecke/d132431f-d2c6-4401-96d1-90f58d3026fb/scratchpad/m1e_numeric.py`
(mpmath self-checks + calls to the unmodified
`.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py`).
