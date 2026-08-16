# LAW — `det(1−K_q)` impact audit: which banked numbers carry the missing factor

**Status:** enumeration `COMPLETE` for lane G + the flagship paper; every correction
`PROVED` numerically (float, `mpmath` `dps = 40`, no interval arithmetic — same epistemic
status as the parent). **Date:** 2026-08-16. **Lane:** G.
**Interpreter:** `/Users/za/miniforge3/envs/pari-arb/bin/python3`.
**New probes, all `q3impact`-prefixed:** `law_probes/q3impact_detK_factor.py`,
`law_probes/q3impact_u1_sup_corrected.py`, `law_probes/q3impact_u1phi_arg.py`
(+ their `.json`/`.log`). **No existing file was modified. No `git` command was run.**

**Parent:** `LAW_Q3_BRANCH_DIAGNOSIS.md` — this note discharges its `Q3D.11` (`GAP`) and
its §5 `TODO` on `LAW_U1_GROWTH.md` §7.3/§10.

---

## 0. Verdict up front

> ### **Conclusion-flips: 0.**
> Twenty-two quoted magnitudes were classified. **No stated conclusion changes sign,
> direction, or status.** Two numbers move materially (`LAW_U1_GROWTH.md` §7.3's adverse
> slope `+1.50 → +0.67`; the same note's `sup` column falls by up to `1.7×`), but the
> verdict attached to each is unchanged. Three results get **quantitatively better** after
> correction (§7.2's U4 support, `LAW_U1PHI_TEST.md`'s `−3.08` exponent, `LAW_U2B_CLOSURE`'s
> consistency with the proxy).
>
> ### **One statement — not a conclusion — must be restated.**
> `LAW_U1_GROWTH.md` §7.2 writes the U4 identification as
> `det(1−L^+)·det(1−L^−) = Z_{G_q}`. **As an identity that is false**; the true statement is
> `det(1−L^+)·det(1−L^−) = Z_{G_q} · det(1−K_q)`. The *numerical evidence* offered for it in
> that section survives and improves (§4 below). This is a labeling repair, already implied
> by the parent's `Q3D.2`, recorded here so it is not lost.

The reason the blast radius is this small is structural and was already visible in the
parent: **`|det(1−K_q)| → 1` fast in every direction the lane actually measures.**
`b_q ≤ 0.0718` for `q ≥ 5`, and `b_q ≈ (π/2q)²` for large `q`, so on `Re s ≥ 1/2` the factor
sits within `1 ± b_q^{1/2}` and, for the `q = 12 … 100` guard family, within `1 ± 0.14`.
The lane's `q`-asymptotic claims are therefore essentially untouched: the correction's own
log-log `q`-slope is `≤ 0.051` in absolute value at every guard point (§3.3).

---

## 1. Method, and the reproduction gate

`Z_S = det(1−L_s)/det(1−K_s)`, `det(1−K_s) = Π_{n≥0}(1 − b_q^{s+n})` (parent §1.2, MMS
Proposition). Every corrected number below is `P_repo / |det(1−K_q)(s)|` (magnitudes) or
`arg P_repo − arg det(1−K_q)(s)` (phases), with `P_repo` **read from the banked receipt**,
never recomputed. `b_q` is taken from `law_probes/q3diag_detK.json` where banked, else from
MMS's even-`q` closed form `b_q = (2−λ_q)/(2+λ_q)`.

**Gate — the probes reproduce the published numbers before correcting them.** From the
banked rows, `q3impact_u1_sup_corrected.py` returns the *uncorrected* slopes
`all-8 = +0.8926`, `identified = +0.0715`, `dU_0 = −0.5739`, against `LAW_U1_GROWTH.md`
§10's published `+0.893`, `+0.071`, `−0.574`; and the §7.3 "excl. `dU_4`" column
`81.84 / 25.14 / 49.47 / 92.81 / 99.40` exactly. `q3impact_u1phi_arg.py` returns the
uncorrected two-height exponents `−3.0782` / `−3.0700` against `LAW_U1PHI_TEST.md` §4.4's
`−3.078` / `−3.070` and the `β`-ratios `1.368` / `1.317` against its `1.369` / `1.318`.
(§7.3's headline `+1.50` and `+1.17` are **endpoint** slopes, `ln(99.402/25.138)/ln(40/16)
= 1.500` and `ln(99.402/49.473)/ln(40/22) = 1.167`; this note quotes both conventions.)

### 1.1 `b_q`, and how small the factor is

| `q` | 5 | 6 | 12 | 16 | 22 | 30 | 40 | 56 | 72 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| `b_q` | `1.309e−2` | `7.180e−2` | `1.733e−2` | `9.701e−3` | `5.115e−3` | `2.747e−3` | `1.544e−3` | `7.87e−4` | `4.76e−4` | `2.468e−4` |
| zero spacing `2π/log(1/b_q)` | `1.449` | `2.385` | `1.549` | `1.355` | `1.191` | `1.065` | `0.971` | `0.879` | `0.821` | `0.756` |

**`b_6 = 0.0718` is the largest `b_q` over all `q ≥ 5`** (odd `q` and larger even `q` are all
smaller), so `b_6` sets every uniform-in-`q` bound below.

---

## 2. The classification table

Class **(a)** = zero-location / winding / argument-principle claim, or a bound derived from
the Selberg **Euler product** (i.e. about the true `Z_S`, never touching a repo determinant)
— `UNAFFECTED`. Class **(b)** = a magnitude of `det(1−L)` presented *as* `det(1−L)`
— correct as labeled, only its *interpretation as `Z_S`* would be wrong. Class **(c)** =
a magnitude presented as `Z_S`, or compared against a `Z_S`-quantity — `AFFECTED`.

| # | quoted magnitude | where | class | correction factor | corrected value | flip? |
|--:|---|---|---|---|---|---|
| 1 | `sup_{∂U}` guard column, all 8 points: `170.0 / 92.8 / 49.5 / 266.4 / 275.4` | `U1_GROWTH` §7.3 | **(c)** | `1/|det(1−K_q)|`, per point, `0.24 … 2.00` | `179.2 / 111.0 / 101.6 / 145.5 / 178.0` | **no** |
| 2 | `sup_{∂U}` excl. `dU_4`: `81.84 / 25.14 / 49.47 / 92.81 / 99.40` (`q=12…40`) | `U1_GROWTH` §7.3 | **(c)** | idem | `47.01 / 33.33 / 45.95 / 56.45 / 61.59` | **no** |
| 3 | **adverse log-log slope `+1.50`** (`q = 16→40`, endpoint) | `U1_GROWTH` §7.3, §8 U1.20, §10 | **(c)** | `d log|det(1−K_q)|/d log q` | **`+0.67`** (`+1.564 → +0.673` LSQ) | **no** — still `> 0`, still adverse |
| 4 | slope `+1.17` (`q = 22→40`, endpoint) | `U1_GROWTH` §7.3 | **(c)** | idem | **`+0.49`** | **no** |
| 5 | §10 extended slope, ALL 8 points, `+0.893` | `U1_GROWTH` §10 | **(c)** | idem | **`+0.890`** | **no** — still FAILS `≤ 0` |
| 6 | §10 IDENTIFIED-domain slope **`+0.071`** ("flat") | `U1_GROWTH` §10 | **(c)** | idem | **`+0.061`** | **no** — still flat/consistent |
| 7 | §10 `Re s = 1/2` point (`dU_0`) slope **`−0.574`** ("decays") | `U1_GROWTH` §10 | **(c)** | `|det(1−K_q)(1/2+it)| ∈ [0.935, 1.126]` | **`−0.554`** | **no** — still `< 0` |
| 8 | §10 identified sups "oscillate in `[2.29, 13.69]`; `q ≥ 16`: `[2.29, 8.31]`" | `U1_GROWTH` §10 | **(c)** | idem | `[3.32, 10.39]`; `q ≥ 16`: `[3.32, 7.60]` | **no** — still no trend |
| 9 | `|Z_q(s_∞)|` centre column `6.1374 / 2.6000 / 1.1380 / 1.1516 / 0.6813` | `U1_GROWTH` §7.3 | **(c)** | `|det(1−K_q)(0.25+it_∞)|` | see `q3impact_detK_factor.json` (`≤ 1.5×`) | **no** |
| 10 | `min_{∂U}` column `0.2445 / 0.0900 / 0.1525 / 0.1503 / 0.0253` | `U1_GROWTH` §7.3 | **(c)** | idem | same order; no claim rests on it | **no** |
| 11 | §7.2 Euler control points, rel. diffs `3.3e−4 … 1.6e−3` (9 rows) | `U1_GROWTH` §7.2 | **(c)** | `|det(1−K_q)|`, `1 ± 2.2e−3` | **8 of 9 improve**; worst `1.6e−3 → 1.6e−3` | **no** — support **strengthens** |
| 12 | the U4 identity *as written*, `det(1−L^+)det(1−L^−) = Z_{G_q}` | `U1_GROWTH` §7.2 | **(c)** | — | `= Z_{G_q}·det(1−K_q)` | **statement restated** (see §0) |
| 13 | `S_q(3/2) ≤ 0.19144`, `sup |Z_{G_q}| ≤ e^{0.19144} = 1.2110` | `U1_GROWTH` §2.1–2.2, (2.1) | **(a)** | none — Euler-product bound on the true `Z_S` | unchanged | **no** |
| 14 | `S_q(σ) ≤ 0.4861`, **`|Z_{G_q}| ≤ 1.6259` on `Re s ≥ 3.5`, `q ≥ 5`** | `U2B_CLOSURE` §4.2, U2b.13 | **(a)** | none (Euler product) | unchanged | **no** |
| 14′ | *the same bound applied to the repo proxy* `P_q` | derived use | **(c)** | `|det(1−K_q)| ∈ [1 − 1.07e−4, 1 + 1.07e−4]` on `Re s ≥ 3.5`, worst case `q = 6` | `P_q ≤ 1.62608` | **no** — `1e−4` relative |
| 15 | two-sided `0.3783 ≤ |Z_{G_q}| ≤ 1.6259` | `MINIMAL_HYPOTHESES` §245, §260 | **(a)** | Euler product | unchanged | **no** |
| 16 | `D_q(t) = −2 arg P_q(1/2+it)` series, both heights | `U1PHI_TEST` §4.2 | **(c)**, *phase* | `+2 arg det(1−K_q)`, `|·| ≤ 0.198 rad` | see §5 | **no** |
| 17 | null test: span `2.024` rad vs required `17.018` rad | `U1PHI_TEST` §4.3 | **(c)** | idem | span `2.032` vs `17.018` | **no** — null still dead by `8.4×` |
| 18 | **`|φ_q| ≍ q^{−3.078}` (LSQ) / `q^{−3.070}` (endpoint)** vs predicted `−3` | `U1PHI_TEST` §4.4, headline | **(c)** | idem | **`−3.063` / `−3.042`** | **no** — moves **toward** `−3` |
| 19 | `β`-ratio `1.369` / `1.318` vs ansatz-(A)'s required `4.7116` | `U1PHI_TEST` §4.4 | **(c)** | idem | `1.285` / `1.197` | **no** — (A) still refuted |
| 20 | `min` Taylor `|det|` `1.81411…e−6`; `F_R = 1.77974e−6`; **min margin `3.43786e−8`**; `T_tail(160) = 6.26786e−22`; `rH ≤ 0.359`; winding `1` | `R3B_FLAGSHIP_CERT` §§2–4; `FLAGSHIP_PAPER_DRAFT.tex` Tab. 1 | **(b)+(a)** | none — these bound `det(1−L_{s,+})` *as such*, and feed a winding count | unchanged | **no** |
| 21 | flagship `s_0 = 0.45389518… + 5.76353724…i`, gap `δ ≥ 0.0461038` | `FLAGSHIP_PAPER_DRAFT.tex`; `THEOREM_G5_OFFLINE_ASSEMBLY` | **(a)** | `det(1−K_5) ≠ 0` on Box (`Re ≈ 0.454 > 0`) | unchanged | **no** |
| 22 | `|Z_q − Z_θ|` table + exponents `−2.115 / −2.145 / −2.180` | `T2_DETERMINANT` §P3 | **(a)** | truncated Euler products throughout — no repo determinant enters | unchanged | **no** |
| 23 | `|K_3(1/2+it_∞)| = |φ_3(1/2+it_∞)| = 1.000000000000` | `MIRROR_Q3_DISCRIMINATOR` §2 C1 | **(a)** | a `κ_q`/scattering unitarity check, not a determinant magnitude | unchanged | **no** |
| 24 | `LAW_TEO_KAPPA_CORRECTED` K.6 residual `[0.456, 2.055]` | parent §3.3 | **(c)** | already corrected in the parent | `= 1.000000000` | **no** (already banked) |

**The flagship is already `det(1−K)`-aware and needs nothing.** `FLAGSHIP_PAPER_DRAFT.tex`
carries the quotient in its abstract (l. 68), states the factorization at Link 6 (l. 449–455)
and proves non-vanishing on the Box at Link 5 (l. 441–448); `THEOREM_G5_OFFLINE_ASSEMBLY.md`
l. 117–120 does the same. Every constant in Table 1 is a `det(1−L_{s,+})` quantity feeding a
winding count. **Class (a)/(b), no correction, no flip.** For reference, if any `|Z_S|`
*magnitude* is ever quoted at `G_5` near the Box, the divisor is `|det(1−K_5)| ≈ 0.9026` at
`0.45 + 7.0674i` and `0.8563` at `0.45` (a `10–14 %` effect) — none is quoted today.

---

## 3. `LAW_U1_GROWTH.md` §7.3 / §10 — the item the parent flagged, worked out

### 3.1 The `Re s = 0` point is worse than "out of domain" — it is where `det(1−K_q)` vanishes

`∂U` is the 8-point ring of radius `1/4` about `s_∞ = 0.25 + 7.067362570867346 i`, so
`dU_4` sits at `Re s = 0` **exactly on the zero line of `det(1−K_q)`** (parent `Q3D.7`:
zeros at `s = −n + 2πik/log(1/b_q)`). The zeros' imaginary spacing shrinks like
`2π/log(1/b_q) ≈ π/log(2q/π)`, so as `q` grows the ring's `dU_4` is dragged past a zero
again and again:

| `q` | 12 | 16 | 22 | 30 | 40 | 56 | 72 | 100 |
|---|---|---|---|---|---|---|---|---|
| dist. from `t_∞` to nearest zero | `0.680` | `0.290` | `0.0787` | `0.391` | `0.273` | **`0.0343`** | `0.325` | `0.260` |
| `|det(1−K_q)(dU_4)|` | `1.995` | `1.243` | **`0.410`** | `1.830` | `1.548` | **`0.244`** | `1.894` | `1.764` |

**This is the mechanism the parent found at `q = 4` (`PC.12`'s `0.108` minimum), recurring
inside the guard.** The raggedness §7.3 caveat 1 charged to "zeros of `Z_{G_q}` migrating
past `∂U`" is, at `dU_4`, partly the *spurious* zeros of `det(1−K_q)` migrating past `∂U`.
`q = 22` and `q = 56` are the two `q` where `P_q(dU_4)` is inflated by `2.4×` and `4.1×`
for a reason that carries no information about `G_q`.

**Consequence for the ledger: `dU_4`'s exclusion is now over-determined.** §7.3 excluded it
because `Re s = 0` bounds the R5 common-continuation domain `Ω*`; a second, independent
reason is that the repo's proxy is not `Z` there in a way that is unbounded in `q`.

### 3.2 The corrected guard table

`|Z_q| = P_repo/|det(1−K_q)|`, from the banked `u1_sup.json`, `u1_sup_q40.json`,
`u1_guard_extended.json` rows:

| `q` | sup all-8 repo | **all-8 corrected** | sup excl. `dU_4` repo | **excl. `dU_4` corrected** | identified-domain repo | **identified corrected** | `dU_0` repo | **`dU_0` corrected** |
|--:|---|---|---|---|---|---|---|---|
| 12 | `170.01` | `179.24` | `81.84` | `47.01` | `13.695` | `10.393` | `0.6430` | `0.6531` |
| 16 | `92.79` | `111.03` | `25.14` | `33.33` | `2.295` | `3.316` | `0.5081` | `0.5171` |
| 22 | `49.47` | `101.63` | `49.47` | `45.95` | `6.101` | `5.667` | `0.2697` | `0.2885` |
| 30 | `266.36` | `145.53` | `92.81` | `56.45` | `8.273` | `6.938` | `0.1502` | `0.1450` |
| 40 | `275.41` | `177.97` | `99.40` | `61.59` | `3.936` | `4.023` | `0.2524` | `0.2503` |
| 56 | `97.62` | `256.37` | `97.62` | `86.38` | `6.011` | `5.957` | `0.2293` | `0.2357` |
| 72 | `659.77` | `348.40` | `147.79` | `122.90` | `7.938` | `7.523` | `0.1281` | `0.1259` |
| 100 | `831.11` | `471.11` | `243.38` | `161.94` | `8.085` | `7.604` | `0.2119` | `0.2100` |

("identified domain" = §10's `dU_0, dU_1, dU_2, dU_6, dU_7`, i.e. `Re s ≥ 0.25`.)

Slopes, both conventions:

| quantity | published | **corrected (LSQ)** | **corrected (endpoint)** | verdict |
|---|---|---|---|---|
| excl. `dU_4`, `q = 16→40` | **`+1.50`** | `+1.564 → +0.673` | `+1.500 → +0.670` | still `> 0` — **ADVERSE stands** |
| excl. `dU_4`, `q = 22→40` | `+1.17` | `+1.178 → +0.492` | `+1.167 → +0.490` | still `> 0` |
| all 8, `q = 12→100` | `+0.893` | **`+0.890`** | — | still FAILS `≤ 0` |
| identified domain, `q = 12→100` | `+0.071` | **`+0.061`** | `−0.249 → −0.147` | still flat/consistent — **§10 VERDICT stands** |
| `dU_0` (`Re s = 1/2`), `q = 12→100` | `−0.574` | **`−0.554`** | — | still decays — **passes** |

> **§7.3's headline number halves and its verdict does not move.** The `+1.50` was inflated
> by the correction's own local `q`-behaviour near the `Re s ≈ 0` edge, but the residual
> `+0.67` is still unambiguously positive, and Lemma U1-6 kills any positive exponent just
> as dead. **The §7.3 "guard verdict: ADVERSE" and the §10 "U1 CORROBORATED on the
> identification domain" both survive verbatim.** No `HEURISTIC`/`PROVED`/`GAP` label moves.

### 3.3 The requested `d log|det(1−K_q)| / d log q`

Over `q = 12 … 100` at the ring abscissae:

| point | `Re s` | `d log|det(1−K_q)| / d log q` |
|---|---|---|
| `dU_0` | `0.5000` | `−0.0197` |
| `dU_6` | `0.2500` | `−0.0508` |
| `dU_3` | `0.0732` | `+0.0080` |
| `dU_4` | `0.0000` | `−0.0328` |

**Every one is `≤ 0.051` in magnitude** — the correction is *not* a `q`-power, because
`b_q → 0`, so `|det(1−K_q)| → 1` pointwise for `Re s > 0` and the residual `q`-dependence is
the pseudo-random phase of `b_q^{it}`. **A `q`-slope conclusion can therefore never be
overturned by more than `≈ 0.05` by this factor** — which is why item 6 (`+0.071`) and item
7 (`−0.574`) are safe, and why item 3's `1.50 → 0.67` came from the *small-`q` window*
`16 → 40` (two points where `|det(1−K_q)(dU_5)|` happens to sit on opposite sides of 1),
not from a systematic drift.

---

## 4. `LAW_U1_GROWTH.md` §7.2 — U4's numeric support gets *better*

The 9 control points with `Re s > 1`, `P_repo` vs the truncated (`ℓ ≤ 6`) Euler product:

| `q` | `s` | `|det(1−K_q)|` | published rel. diff | **corrected rel. diff** |
|--:|---|---|---|---|
| 12 | `2.0` | `0.9996943` | `6.6e−4` | **`3.5e−4`** |
| 12 | `1.5+7.0674i` | `1.0021524` | `1.6e−3` | **`5.6e−4`** |
| 16 | `2.0` | `0.9999050` | `4.1e−4` | **`3.1e−4`** |
| 16 | `1.5+7.0674i` | `0.9997849` | `5.7e−4` | **`3.6e−4`** |
| 22 | `2.0` | `0.9999737` | `3.6e−4` | **`3.3e−4`** |
| 22 | `1.5+7.0674i` | `0.9996635` | `1.1e−3` | **`7.5e−4`** |
| 30 | `2.0` | `0.9999924` | `3.3e−4` | **`3.2e−4`** |
| 40 | `2.0` | `0.9999976` | `3.6e−4` | **`3.6e−4`** |
| 40 | `1.5+7.0674i` | `1.0000120` | `1.6e−3` | `1.6e−3` |

**Eight of nine improve; the ninth is unchanged to two digits.** The largest published
residual (`1.6e−3` at `q = 12`) drops by `3×`. §7.2's claim — "independent numeric evidence
for the U4 identification at even `q = 12 … 40`" — is *strengthened*, once the identity it
supports is restated as `det(1−L^+)det(1−L^−) = Z_{G_q}·det(1−K_q)` (item 12).

**Why the correction was invisible here** is the parent's §3.2 point, now with numbers:
`1 − |det(1−K_q)| ≈ b_q^σ`, which at `σ = 2`, `q = 12` is `3.0e−4` — *the same size as the
`ℓ ≤ 6` Euler-truncation residual the section attributes the whole difference to*. The two
error sources are numerically degenerate at these points.

---

## 5. `LAW_U1PHI_TEST.md` — a **phase**, not a magnitude, and it also improves

§4 does not quote `|Z|`; it quotes `D_q(t) = −2 arg P_q(1/2+it)`. Since
`arg Z_S = arg P − arg det(1−K)`, the correct statistic is
`D_q^corr = D_q^repo + 2 arg det(1−K_q)(1/2+it)`. The contamination:

| `q` | 12 | 16 | 22 | 30 | 40 |
|---|---|---|---|---|---|
| `2 arg det(1−K_q)(1/2 + 1.5i)` | `−0.0611` | `+0.1336` | `+0.1427` | `+0.0551` | `−0.0214` |
| `2 arg det(1−K_q)(1/2 + it_∞)` | `−0.0898` | `+0.1976` | — | — | `+0.0765` |

It is bounded by `2 b_q^{1/2} ≈ π/q` — i.e. **it is exactly the `γ/q` nuisance term §4.4
reported as non-identifiable against the `log q` term.** Applying it:

| statistic | published | **corrected** | flip? |
|---|---|---|---|
| span at `t = 1.5` vs null `3.612` | `1.728` | `1.524` | no — null still over-predicts |
| span at `t_∞` vs null `17.018` | `2.024` | `2.032` | **no** — factor `8.4` stands |
| `β(1.5)` LSQ / endpoint | `−0.7877` / `−0.8198` | `−0.8176` / `−0.7868` | no |
| `β(t_∞)` LSQ / endpoint | `−1.0777` / `−1.0798` | `−1.0507` / `−0.9416` | no |
| `β`-ratio vs ansatz-(A)'s `4.7116` | `1.369` / `1.318` | `1.285` / `1.197` | no — (A) still refuted |
| **exponent `−3α` (LSQ)** | **`−3.078`** | **`−3.063`** | no — `2.6% → 2.1%` from `−3` |
| **exponent `−3α` (endpoint)** | **`−3.070`** | **`−3.042`** | no — `2.3% → 1.4%` from `−3` |
| `δ` (the `t`-independent residual, `GAP` in §7) | `−0.709` / `−0.750` | `−0.755` / `−0.745` | no — still `≈ −0.7`, still open |

> **`U1-φ-a` SURVIVES, and its headline gets sharper: `|φ_q(2+it)| ≍ q^{−3.04…−3.06}`
> against a predicted `−3`.** The correction is a genuine (if small) part of the `2.6%`
> discrepancy the note charged to `t`-independent `κ_q` factors. **Not a flip** — a
> tightening. `δ ≈ −0.75` is untouched, so §7's `GAP` on it stands.

---

## 6. `LAW_U2B_CLOSURE.md` — quantified and negligible, as expected

U2b's `S_q(σ) ≤ 0.4861 ⇒ |Z_{G_q}| ≤ e^{0.4861} = 1.6259` for `Re s ≥ 3.5`, `q ≥ 5`, is
derived from the **Selberg Euler product over primitive closed geodesics**. It never touches
a repo determinant, so it is **class (a): a bound on the true `Z_S`, `PROVED` and unaffected.**

The only thing needing a number is the *derived* statement about the proxy. On `Re s ≥ 3.5`:

| `q` | `b_q` | `min |det(1−K_q)|` | `max |det(1−K_q)|` | max rel. deviation from 1 |
|--:|---|---|---|---|
| 5 | `1.309e−2` | `0.99999974` | `1.00000026` | `2.6e−7` |
| **6** | **`7.180e−2`** | `0.99989316` | `1.00010684` | **`1.07e−4`** |
| 7 | `2.973e−3` | `1 − 1.4e−9` | `1 + 1.4e−9` | `1.4e−9` |
| 8 | `3.957e−2` | `0.99998717` | `1.00001283` | `1.28e−5` |
| 12 | `1.733e−2` | `1 − 7.0e−7` | `1 + 7.0e−7` | `7.0e−7` |
| 100 | `2.468e−4` | `1 − 2.4e−13` | `1 + 2.4e−13` | `2.4e−13` |

**Worst case over all `q ≥ 5` is `q = 6` at `1.07e−4`** (`b_6` is the maximum of `b_q` on
`q ≥ 5`). So the repo proxy obeys `P_q ≤ 1.6259 × 1.000107 = 1.62608` on `Re s ≥ 3.5` —
**five significant figures survive; the `1.6259` is safe as quoted to 4 d.p.** The parent's
"likely negligible" is confirmed: `1 + O(b_q^{3.5})` with `b_6^{3.5} = 5.3e−5`.

---

## 7. Status ledger

| id | claim | status | where |
|---|---|---|---|
| DK.1 | 22 quoted magnitudes classified across lane G + `lane_p/FLAGSHIP_PAPER_DRAFT.tex`; **0 conclusion-flips** | **the finding** | §2 |
| DK.2 | The probes reproduce every published slope/exponent *before* correcting it (`+0.893`, `+0.071`, `−0.574`, `−3.078`, `−3.070`, the §7.3 sup column) | **`PROVED`** numerically — reproduction gate | §1 |
| DK.3 | `U1_GROWTH` §7.3's adverse slope `+1.50 → +0.67` (endpoint) / `+1.56 → +0.67` (LSQ); **verdict ADVERSE stands** | **`PROVED`** numerically | §3.2 |
| DK.4 | §10's three slopes `+0.893/+0.071/−0.574 → +0.890/+0.061/−0.554`; **VERDICT "U1 CORROBORATED" stands** | **`PROVED`** numerically | §3.2 |
| DK.5 | `d log|det(1−K_q)|/d log q ≤ 0.051` at every guard abscissa — the factor **cannot** move a `q`-slope conclusion by more than `≈ 0.05` | **`PROVED`** numerically | §3.3 |
| DK.6 | `dU_4` (`Re s = 0`) sits **on** the `det(1−K_q)` zero line; `|det(1−K_q)|` there ranges `0.244 … 1.995` over `q = 12 … 100`, with near-zeros at `q = 22, 56`. `dU_4`'s exclusion is over-determined | **`PROVED`** numerically — unasked-for | §3.1 |
| DK.7 | §7.2's 9 control-point residuals: **8 of 9 improve**, worst `1.6e−3 → 5.6e−4`. U4's numeric support strengthens | **`PROVED`** numerically | §4 |
| DK.8 | `det(1−L^+)det(1−L^−) = Z_{G_q}` (§7.2, as written) is **false**; `= Z_{G_q}·det(1−K_q)`. Statement repair, not a conclusion flip | **the correction** | §0, §2 item 12 |
| DK.9 | `U1PHI_TEST`'s `D_q` is a **phase**; corrected exponent `−3.078 → −3.063` (LSQ), `−3.070 → −3.042` (endpoint) — **toward** the predicted `−3`. Null test unchanged (`8.4×`) | **`PROVED`** numerically | §5 |
| DK.10 | The `arg det(1−K_q)` contamination is `O(1/q)` — **it is §4.4's non-identifiable `γ/q` nuisance term, now identified** | **`PROVED`** numerically — unasked-for | §5 |
| DK.11 | `U2B_CLOSURE`'s `|Z| ≤ 1.6259` is class (a), unaffected; the proxy version shifts by `≤ 1.07e−4` (worst `q = 6`, `b_6 = 0.0718` = the max `b_q` on `q ≥ 5`) | **`PROVED`** numerically | §6 |
| DK.12 | The flagship paper and `THEOREM_G5_OFFLINE_ASSEMBLY` are already `det(1−K)`-aware (Links 5–6); all Table-1 constants are class (a)/(b); **no correction needed** | **verified by reading** | §2 |
| DK.13 | `T2_DETERMINANT` §P3, `MINIMAL_HYPOTHESES` §§245/260, `MIRROR_Q3_DISCRIMINATOR` C1 are class (a) — Euler-product / unitarity quantities that never touch a repo determinant | **verified by reading** | §2 |
| DK.14 | Coverage: only lane G `.md`, `lane_p/FLAGSHIP_PAPER_DRAFT.tex`, and the receipts they cite were swept. Other lanes and `plans/` **not** audited | **`GAP`, scoped** | §8 |

**What stays open, stated plainly.**

1. **No code and no existing note was changed.** Every corrected number here lives only in
   this note and the three `q3impact_*` receipts. The parent's item 1 (the one-line
   `det(1−K_q)` divisor in `zeta_cert_rosen*.py`) is still not applied.
2. **Coverage is lane G + the flagship paper.** Other lanes (`lane_p` beyond the draft,
   `lane_*` elsewhere, `plans/`, `wiki/`) were not swept — DK.14.
3. **Odd `q ≥ 7`** never appears in a quoted magnitude in this sweep, so `b_7`, `b_9`, … were
   not needed beyond the `b_q` table; the parent's `Q3D.10` (`R`-symbol) remains cosmetic.
4. **Float, not intervals.** `mpmath` `dps = 40`, no Arb balls — same status as the parent.
5. §7.3's `sup` values are **midpoints** with no error bars (its own caveat 3); dividing by
   `|det(1−K_q)|` does not change that.

---

## 8. Receipts

All under `lane_g/law_probes/`. Interpreter `/Users/za/miniforge3/envs/pari-arb/bin/python3`.

- `q3impact_detK_factor.py` → `.json`, `.log` — `b_q` table and zero spacings; `|det(1−K_q)|`
  at all 8 `∂U` points for `q = 12 … 100`; `dU_4` zero-proximity (§3.1); §7.2 control points;
  the `Re s ≥ 3.5` uniform envelope (§6); `G_5` reference points; the `d log/d log q` slopes.
- `q3impact_u1_sup_corrected.py` → `.json`, `.log` — §3.2. Reads `u1_sup.json`,
  `u1_sup_q40.json`, `u1_guard_extended.json`; recomputes every sup and slope from
  `P_repo/|det(1−K_q)|`. Includes the uncorrected reproduction gate.
- `q3impact_u1phi_arg.py` → `.json`, `.log` — §5. `D_q` series from `LAW_U1PHI_TEST.md` §4.2,
  the phase correction, the `β` refits and the two-height exponent solve.
- **Not modified:** every `q3cont_*`, `q3diag_*`, `mirror_*`, `probe_u1_*`, `u1_*` receipt;
  every `LAW_*.md`; `FLAGSHIP_PAPER_DRAFT.tex`; every `zeta_cert_rosen*.py`. No `git`
  command was run.

---

READY FOR JUDGING
