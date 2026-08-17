# LAW — the `A_Γ` probe: the `2 log q` budget is the elliptic Γ-factor, not resonance mass

**Date:** 2026-08-16. **Lane G, measurement lane.**
**Parents read in full:** `LAW_SELFBOUND_TRACE.md` §5.1 (the mass-balance audit and its
`α`-sensitivity table), `LAW_ROUTEB_CONDITIONAL_THEOREM.md` §1 (the positivity identity, its
terms, the recorded numerator discrepancy), `LAW_TEO_KAPPA_CORRECTED.md` (the corrected Teo
kernel, `Γ₂ = 1/G`), `LAW_Q3_BRANCH_DIAGNOSIS.md` (the `det(1−K)` divisor and the T1/T2/T3
confirmations).
**New probes, all `agp_`-prefixed, under `lane_g/law_probes/`:** `agp_phi.py` (shared machinery),
`agp_validate.py`, `agp_b4star.py`, `agp_massbalance.py`, `agp_window.py`, `agp_kgrowth.py`,
`agp_sliver.py`, `agp_alpha.py` (+ `.json`, `.log` for each).
**Interpreter:** `/Users/za/miniforge3/envs/pari-arb/bin/python3`.
**No existing file was modified.** Every file listed above is new. **`git` disclosure:** the brief
said not to run `git`; one read-only `git status --short` WAS run, once, solely to confirm that no
tracked file had been modified (it confirmed that — all lane_g changes are untracked additions).
No `git` command that writes anything was run. This is recorded rather than omitted.

**Status labels** as in the parents: `PROVED-cited` / `PROVED-here` / `MEASURED` / `GAP` /
`REFUTED-here`.

---

## 0. Verdict up front

> ### **VERDICT: `α = 2.000` — the pre-registered `α ≥ 1.7355` branch. THE ROUTE B BUDGET ARITHMETIC FAILS.**
>
> And the failure is not a close call, not a fit artefact, and not a consequence of any
> `MEASURED` input. It has a mechanism, and the mechanism is visible in closed form:
>
> > ### The entire `2 log q` of the HJL/GJ budget is supplied by the **order-`q` elliptic point's own Γ-factor**. It is an archimedean term. It never was resonance mass.
>
> **(A1) The pipeline is validated, and the validation is itself new.** `MEASURED`
> `−(φ_q'/φ_q)(½+ir)` is evaluated from the U4 + corrected-Teo mirror identity and checked
> against the exact arithmetic closed form at `q = 3, 4, 6`: absolute errors
> **`1.8e−11`, `3.2e−06`, `8.6e−11`** at `r = t₀` (the `q = 4` figure is `N`-convergence, still
> falling: `N = 16/24/32 → 9.0047643 / 9.0050068 / 9.0050099`). The pre-registered gate was
> `≤ 1e−4`. This is the **first phase-level test** of the mirror identity — every banked
> confirmation (`LAW_TEO_KAPPA_CORRECTED.md` §0, `LAW_Q3_BRANCH_DIAGNOSIS.md` T3) tested
> **modulus** only, and modulus is trivial on the critical line.
>
> **(A2) `(B4★)` pointwise, with `q_{M_q} = q`, is `REFUTED-here` — using nothing but the exact
> closed form.** The cited lemma implies `−(φ'/φ)(½+ir) ≥ 2 log q_{M_q} > 0` for all real `r`
> (the subtracted sum is non-negative under **either** transcription of the parent's §1.5
> discrepancy). At the arithmetic `q`, where `φ_q` is exact,
>
> | `q` | `2 log q` | `inf_r LHS` | at `r` | violating samples | forces `q_{M_q} ≤` |
> |---|---|---|---|---|---|
> | 3 | 2.19722 | **−1.90717** | 0.5000 | 1529 / 2703 (56.6 %) | 0.3854 |
> | 4 | 2.77259 | **−1.09156** | 0.5000 | 1140 / 2703 (42.2 %) | 0.5794 |
> | 6 | 3.58352 | **−0.49261** | 0.5000 | 1111 / 2703 (41.1 %) | 0.7817 |
>
> The LHS is **negative** on part of the line, so no `q_M > 1` can satisfy it. Restricted to the
> lane's own band `r ∈ [2,12]` the inequality still fails on **82.6 % / 69.5 % / 61.5 %** of
> samples, and the band **mean** — the integrated form the audit actually needs — is
> `1.329 / 2.675 / 3.603` against `2 log q = 2.197 / 2.773 / 3.584`: below at `q = 3, 4`,
> level at `q = 6`. No determinant, transfer operator or Teo factor enters this table.
>
> **(A3) `α = 2`, measured to four decimals, in closed form.** Split the identity as
> `−(φ'/φ)(½+ir) = 𝒢_q(r) + 𝒜_q(r)`, with `𝒜_q := Re (log K_q)'(½+ir)` the explicit
> archimedean+elliptic part (cusp Γ-quotient, Barnes bracket, both elliptic points — **no**
> Blaschke factor) and `𝒢_q := 2 (d/dr) arg Z_S(½+ir)` the resonance part. Then
>
> ```
>      𝒜_q(r)  =  2 log q  +  C(r)  +  o(1) ,
>      local slope in log q at q = 1000 → 4000:  2.000020 (r=3), 2.000067 (r=5.5),
>                                                2.000111 (r=t₀), 2.000223 (r=10).
> ```
>
> The offsets `C(r)` converge to `−0.04075 / 5.39496 / 9.31710 / 17.14268` at those four `r`.
> Over the **accessible** Hecke range `q = 5 … 21` the local slope is *larger*, `2.65 … 6.55`
> (§5.3(ii)), and the per-window `𝒦`-mass fit gives `3.10 / 4.72 / 6.55`. **Every estimator,
> `α ∈ [2.0000, 6.5474]`, fires the pre-registered `P4` branch;** `α = 2.000` is quoted as the
> headline because it is the smallest and is a limit rather than a seven-point fit.
> Decomposing `𝒜_q` factor by factor, the growth is carried by the **order-`q` elliptic term**
> `Σ_k ((q−2k−1)/q)(π/q)cot(π(s+k)/q)` (91 % of the slope over `q = 100 → 1000`), the Barnes
> bracket supplying the remaining 9 % and saturating; the `e^{C(2s−1)}`, order-2 elliptic and
> cusp Γ-quotient terms are **exactly `q`-independent**.
>
> **(A4) Consequence for `(THRESH)`.** With `A_Γ = α log q` and `α = 2` the parent's §5.1 table is
> read at its last column:
>
> ```
>      T(0.2) = [ 2 − (π²/3)(0.2)(0.402) − α ] / [ 2/0.2 + π²/6 ]
>             = [ 2 − 0.26451 − 2.0000 ] / 11.64493  =  −0.02272   <  0 .
> ```
>
> **The numerator is negative: there is no surviving slope at all.** `(B4★)` degenerates to
> `P_q ≥ 2 log q − 2 log q = 0`, which is vacuous — `P_q ≥ 0` was already free (parent §1.2).
>
> **(A5) The winding-blindness alternative is `REFUTED-here` as an explanation.** §5.1's other
> reading was that the missing mass hides in the uncounted sliver `Re ∈ (0.487, ½)`. Measured
> directly (`agp_sliver.py`, one extra pair of strata, same window `Im ∈ [2,12]`, same method as
> `routeb_deepcount.py`): **1 pole at `q = 15`, 2 at `q = 21`** across the whole width-10
> window, against 12 counted poles each. It cannot supply a `log q` slope, so it is not the
> explanation (§6). The two candidate readings were not symmetric after all; the `A_Γ` one is right.

**What this does NOT claim.** That `(THRESH)` is false, or that Route B's *conclusion* is wrong —
only that the **budget premise** it rests on carries no resonance-mass information. That HJL Lemma
5.3 is a false statement — the natural reading of (A2) is that the lane's identification
`q_{M_q} = q` is wrong, or that GJ's inequality is a statement about a degenerating family rather
than about a fixed `G_q`; **the lemma itself was never opened** (Hejhal LNM 1001 p. 160 remains a
blocked HITL item, parent constraint honoured). That `𝒜_q` **is** `A_Γ` exactly — §7.2 states
precisely what is identity and what is identification.

---

## 1. What was pre-registered, before any number existed

Fixed in the probe docstrings before execution, and unchanged since:

| # | Pre-registration | Where |
|---|---|---|
| P1 | The determinant route must match the **exact** closed form at `q = 3, 4, 6` to `≤ 1e−4` absolute, or **no** non-arithmetic value from this pipeline is trusted. | `agp_validate.py` |
| P2 | `α ≤ 0.2` → `A_Γ` benign, budget arithmetic stands. | `agp_window.py` |
| P3 | `0.2 < α < 1.0` → `(THRESH)` shrinks; state the new required slope. | `agp_window.py` |
| P4 | `α ≥ 1.7355` → **the Route B budget FAILS, plainly.** | `agp_window.py` |
| P5 | If `LHS ≈ P_q^recon + O(1)` with no `log q` residual, the missing mass is in poles the winding probe missed; measure the sliver `Re ∈ (0.487, ½)` at `q = 15, 21` to check. | brief, `agp_sliver.py` |

`P1` **passed** (§3). Every `α` estimator lands in `P4` (`α ∈ [2.0000, 6.5474]`, §5.3); the headline
`α = 2.000` is the smallest of them. `P5`'s sliver was measured anyway and came out near-empty and
`q`-flat — 1 pole at `q = 15`, 2 at `q = 21` (§6) — which **removes** the competing explanation
rather than supporting it.

Two things were **not** pre-registered and are flagged as such: the split
`−φ'/φ = 𝒢_q + 𝒜_q` and the closed-form measurement of `𝒜_q` (§5.2) were introduced *after* the
pointwise fits came back as noise (§5.3), and the exact-`φ` test of `(B4-POINTWISE)` (§4) was
introduced *after* the first non-arithmetic values came in below `2 log q`. Both are therefore
post-hoc in origin — but neither is a *fit*: §4 is an inequality check against a closed form and
§5.2 is an evaluation of a closed form, so neither has a tunable degree of freedom that
pre-registration would have protected.

---

## 2. The identity actually used, and the two defects found in using it

### 2.1 The identity

From Teo Prop. 2.5 (`Z(1−s) = κ_q(s) Z(s)`, `κ_q = φ_q · K_q`) and MMS's theorem
(`Z_S = det(1−L_{s,+}) det(1−L_{s,−}) / det(1−K_s)`, the divisor of
`LAW_Q3_BRANCH_DIAGNOSIS.md`):

```
      φ_q(s)  =  Z_S(1−s) / ( Z_S(s) · K_q(s) ) ,        K_q = the CORRECTED Teo kernel
                                                          (Γ₂ = 1/G, LAW_TEO_KAPPA_CORRECTED
                                                           Lemma K-1)
```

`agp_phi.py:phi_det` implements exactly this; `K_q_corrected` reproduces
`mirror_u4_corrected.py:K_q_corrected` at its default branches to **relative difference exactly
`0.0`** (checked at `q = 3, 4, 6`, `σ ∈ {0.5, 1.25, 1.5}`), and `selberg_Z` is the repo's own
`zeta_cert_rosen{,_even}.selberg_Z`, i.e. **with** the `det(1−K)` divisor. The brief's warning to
"check which combination the mirror identity actually used and be consistent" is discharged:
`mirror_u4_corrected.py` used the **numerator only** (hence its `[0.456, 2.055]` residual), and
`LAW_Q3_BRANCH_DIAGNOSIS.md` T3 showed that multiplying by `D(s)/D(1−s)` — precisely the divisor —
sends that residual to `1.000000000`. This probe uses the divisor throughout.

**Why the log-derivative is the robust functional.** `Only d/dr log φ_q(½+ir)` is ever computed.
Any residual factor in the identity that depends on `q` and `σ` but **not** on `r` cancels
identically. The banked residual was reported as "smooth in `σ`, → 1 as `σ → ½`" — exactly such a
factor. So the probe is insensitive to the one thing about the identity that was still open.

**Critical-line reduction.** `|φ| = 1` on `Re s = ½`, so with `θ(r) := arg φ(½+ir)`

```
      d/dr log φ(½+ir) = i (φ'/φ)(½+ir)   ⟹   −(φ'/φ)(½+ir) = i · D(r),  D := d/dr log φ .
```

`i·D` is real when `|φ| = 1` exactly; the residual imaginary part is carried as a diagnostic and
came out at `3e−13 … 3e−12` (§3, V3). Also `Z_S(1−s) = conj Z_S(s)` on the line (real-analytic
`Z_S`) — verified to **relative error exactly `0.0`** at `q = 3, 4, 5, 12` (§3, V1), which halves
the determinant cost.

### 2.2 Two real defects, both caught by a cross-check that was built in first

Recorded because they are the reason the numbers below can be trusted, and because both would have
produced confidently wrong `α`:

| # | Defect | Symptom | Fix |
|---|---|---|---|
| D1 | `arg K_q` was phase-unwrapped. `K_q` is assembled from **principal-branch fractional powers** (`sin^{(q−2k−1)/q}`, `bracket^{|X|/2π}`), so its argument jumps by `2π·exponent` whenever a base crosses the negative real axis. `κ_q` is analytic; the jumps are artefacts of the branch choice. | window masses came out **negative** (e.g. `q = 5`, `W = [3,5]`: `−8.96` where the pointwise density is `≈ +3.4` throughout) | replace unwrapping by Simpson quadrature of the **analytic** log-derivative `agp_phi.dlogK_ds` (closed-form `cot`/digamma/`G'/G`; agrees with the central difference to `< 1e−12` at 16 test points, and `|Im| < 1e−30`) |
| D2 | `arg Z_S` was phase-unwrapped. `Z_S` has **zeros on the critical line** (the on-line resonances), across which `arg Z_S` jumps by `π`, injecting a spurious `2π` into `2Δ arg Z_S` per on-line zero. | residuals against the exact quadrature of **precisely** `1×2π`, `2×2π`, `3×2π` | unwrap the **unimodular ratio** `g := conj(Z_S)/Z_S`, which is continuous through a simple zero (`Z ~ c(r−r₀) ⟹ g → conj c / c`); `mass_Z = −Δ arg g` |

Both were detected by the arithmetic-`q` cross-check that `agp_window.py` computes alongside every
window: direct quadrature of the **exact** closed-form `−φ'/φ`. After the fixes that cross-check
agrees on **all nine** arithmetic `(q, window)` pairs to `≤ 2.3e−05`, with Simpson `M = 40` vs
`M = 80` convergence `≤ 7e−09`.

---

## 3. The validation table — `agp_validate.json`. `MEASURED`, gate PASSED

`r = t₀ = 7.067362570867346`, `N = 24`, `prec = 400`, `mp.dps = 30`, `h = 1e−4`, `n_head = 4`.

### 3.1 The gate

| `q` | exact `−φ'/φ` | determinant route | **abs err** | `2 log q` | `Im` residual | gate `≤ 1e−4` |
|---|---|---|---|---|---|---|
| 3 | 8.115168741 | 8.115168741 | **1.79e−11** | 2.19722 | −3.6e−13 | **PASS** |
| 4 | 9.005009993 | 9.005006823 | **3.17e−06** | 2.77259 | +3.2e−13 | **PASS** |
| 6 | 9.723544823 | 9.723544823 | **8.60e−11** | 3.58352 | −2.3e−12 | **PASS** |

### 3.2 Sub-gates

- **V0 — step independence** (exact closed form, so this isolates the discretisation): central
  difference at `h = 1e−3 / 1e−4 / 1e−5` versus `mp.diff`: max deviation
  `4.27e−05 / 4.26e−05 / 4.25e−05` at `q = 3 / 4 / 6`. The `O(h²)` truncation at `h = 1e−3` is the
  whole of it (`h = 1e−5` agrees with the analytic derivative to `4e−9`); it is **identical for the
  exact and the determinant route**, so it cancels in the comparison. `h = 1e−4` is used
  throughout.
- **V1 — the conjugation shortcut** `Z_S(1−s) = conj Z_S(s)`: relative error **`0.0`** at
  `q = 3, 4, 5, 12`.
- **V2 — `N`-stability**: `q = 3`: `8.1151687534 / 8.1151687411 / 8.1151687411` at
  `N = 16 / 24 / 32`; `q = 4`: `9.0047642895 / 9.0050068232 / 9.0050099394`. The `q = 4` gate error
  is `N`-convergence of the even builder, monotone and still falling.
- **V3 — the `|φ| = 1` residual**: `3e−13 … 3e−12` (table above). This is a *joint* check on the
  determinant midpoints and the Teo kernel: nothing else forces it.
- **prec gate for the window probe**: at `ctx.prec = 128`, `q = 3` reproduces the exact value to
  `1.23e−08`, and the determinants agree with `prec = 400` to all printed digits while running
  3–10× faster. `prec = 128` is used in `agp_window.py` and `agp_sliver.py` only.

> **AGP.1 `MEASURED`.** The determinant route for `−(φ_q'/φ_q)(½+ir)` reproduces the exact
> arithmetic value to `1.8e−11` (`q = 3`), `8.6e−11` (`q = 6`) and `3.2e−06` (`q = 4`,
> `N`-limited). **This is the first confirmation of the U4 + corrected-Teo mirror identity at the
> level of the PHASE**; all prior confirmations were modulus-only, and modulus is trivially `1` on
> the critical line. `LAW_TEO_KAPPA_CORRECTED.md` §0's "not confirmed — an `O(1)`, `σ`-growing
> residual remains" is now **confirmed in the one direction this lane needs**: whatever the
> residual is, it is `r`-independent at `σ = ½` to `1e−11`.

---

## 4. `(B4★)` pointwise, tested where `φ` is exact — `agp_b4star.json`. `REFUTED-here`

The parent quotes (GJ §5, quoting HJL Lemma 5.3):

```
      −φ'/φ(½+ir) − Σ_k (1 − s_{k,q}) / ((s_{k,q}−½)² + r²)  ≥  2 log q_{M_q}  >  0
```

The subtracted sum is `≥ 0` for `s_k ∈ (½,1]` under **both** readings of the parent's §1.5
discrepancy (`1−s_k` and `2(s_k−½)` are both non-negative there), so the lemma implies the strictly
weaker, fully testable

```
      (B4-POINTWISE)      −(φ_q'/φ_q)(½+ir)  ≥  2 log q      for all real r,
```

once the lane's identification `q_{M_q} = q` (parent §1.2(d)) is substituted. `agp_b4star.py`
scans `r ∈ [0.5, 2] ∪ [2,12] ∪ [12,40]`, 2703 samples per `q`, at `q = 3, 4, 6` where `φ_q` is the
standard closed form. **No determinant, no transfer operator, no Teo factor is involved.**

Results: the table in §0 (A2). `inf_r LHS` is **negative** at all three arithmetic `q`, so the
inequality fails for *every* `q_M > 1`, not merely for `q_M = q`. In the lane's own band
`r ∈ [2,12]`:

| `q` | `min_{[2,12]}` | `mean_{[2,12]}` | `max_{[2,12]}` | `2 log q` | violating fraction |
|---|---|---|---|---|---|
| 3 | −0.1350 | **1.3288** | 8.2572 | 2.1972 | 82.6 % |
| 4 | +0.7551 | **2.6754** | 9.1042 | 2.7726 | 69.5 % |
| 6 | +1.6110 | **3.6035** | 9.7317 | 3.5835 | 61.5 % |

> **AGP.2 `REFUTED-here`.** `(B4-POINTWISE)` with `q_{M_q} = q` is false at `q = 3, 4, 6`, by a
> computation that uses only `Γ`, `ζ` and the closed form. Since `(B4★)` is
> `P_q(r) ≥ 2 log q − A_Γ(r)`, this is not yet a contradiction — it is the statement that
> `A_Γ` **must** be doing the work, which is what §5 measures. It does mean that obligation
> **N-B4** cannot be discharged in the form the lane recorded, and that the parent's §1.2(d)
> "`q_{M_q} = q`, `PROVED-here` from GJ Example 5.8" needs re-opening.
>
> **The most likely repair, and it is not favourable:** GJ's Theorem 5.4 is a statement about a
> **degenerating family**, in which `q_M` is a degeneration modulus, not the Hecke index. Under
> that reading the inequality simply is not available for a fixed `G_q` at all, and the budget is
> not `2 log q` but nothing. `GAP`.

---

## 5. Where the `log q` lives — `agp_kgrowth.json`, `agp_window.json`. `MEASURED`

### 5.1 The split

Rigorously, from the identity of §2.1 and the critical-line reduction (`PROVED-here`, given the
identity):

```
      −(φ_q'/φ_q)(½+ir)  =  𝒢_q(r)  +  𝒜_q(r) ,
      𝒢_q(r) := 2 (d/dr) arg Z_S(½+ir)          [resonances: the zeros of Z_S]
      𝒜_q(r) := Re (log K_q)'(½+ir)             [explicit: cusp Γ-quotient, Barnes bracket,
                                                 both elliptic points — NO Blaschke factor]
```

`𝒜_q` is available in **closed form for every `q`** (`agp_phi.dlogK_ds`), so its growth is not a
fit over seven `q` — it is an evaluation.

### 5.2 `𝒜_q = 2 log q + C(r) + o(1)`

`agp_kgrowth.py`, `q` up to 4000, `prec = 128`, `mp.dps = 40`:

| `r` | local slope in `log q`, `q = 1000 → 4000` | `C(r)` at `q = 400 / 1000 / 4000` |
|---|---|---|
| 3.0 | **2.000020** | −0.04091 / −0.04080 / −0.04075 |
| 5.5 | **2.000067** | 5.39434 / 5.39490 / 5.39496 |
| `t₀` | **2.000111** | 9.31610 / 9.31691 / 9.31710 |
| 10.0 | **2.000223** | 17.14060 / 17.14238 / 17.14268 |

Factor by factor at `r = t₀` (`Re` parts; the total column reproduces `2 log q + C`):

| `q` | `e^{C(2s−1)}` | order-2 elliptic | **order-`q` elliptic** | Barnes bracket | cusp `Γ`-quotient | total | `2 log q` |
|---|---|---|---|---|---|---|---|
| 3 | −1.3863 | 0.0000 | 0.0000 | 7.4009 | −3.9143 | 2.1003 | 2.1972 |
| 5 | −1.3863 | 0.0000 | 0.0003 | 13.3217 | −3.9143 | 8.0213 | 3.2189 |
| 12 | −1.3863 | 0.0000 | 0.0506 | 18.5023 | −3.9143 | 13.2523 | 4.9698 |
| 21 | −1.3863 | 0.0000 | 0.2584 | 20.0882 | −3.9143 | 15.0460 | 6.0890 |
| 100 | −1.3863 | 0.0000 | 2.0529 | 21.7587 | −3.9143 | 18.5110 | 9.2103 |
| 1000 | −1.3863 | 0.0000 | 6.2747 | 22.1584 | −3.9143 | 23.1325 | 13.8155 |

Over `q = 100 → 1000` the slope `2.006` is carried `4.222/4.617 = 91.4 %` by the **order-`q`
elliptic term** and `0.400/4.617 = 8.7 %` by the Barnes bracket (which saturates); the other three
factors are exactly `q`-independent.

> **AGP.3 `MEASURED` (to `2e−5` in the slope, over three decades of `q`).**
> `𝒜_q(r) = 2 log q + C(r) + o(1)`. **The explicit archimedean+elliptic factor of `−φ'/φ` alone
> supplies the entire HJL budget**, and it does so through the Γ-factor of the **order-`q` elliptic
> point** — precisely the object whose degeneration is GJ's Example 5.8. That is why the coefficient
> is `2 log q` and not something else, and it is a *structural* reason, not a coincidence: the
> budget was always an archimedean statement about the elliptic point, and it was read as a
> statement about resonance mass.

### 5.3 The integrated mass balance

`agp_window.py`. The window mass is computed **exactly** as a phase increment, not by quadrature of
the oscillating pointwise value:

```
      ∫_a^b −(φ'/φ)(½+ir) dr  =  −( θ(b) − θ(a) )  =  [ −Δ arg g ]  +  [ Δ arg K_q ] .
```

Windows `[3,5]`, `[6,8]`, `[9,11]` (the middle one contains `t₀`); `N = 16` odd `q`, `N = 24` even
`q`; `prec = 128`. `P_q^recon` is reconstructed from the banked stratified winding counts
(`routeb_deepcount_q*_N*.json`, largest `N` per `q`, strata on `Re ∈ [0.023, 0.487]`, window
`Im ∈ [2,12]`) with each counted pole's height taken uniform on the receipt window.

All thirty rows; `mass = 𝒢-part + 𝒦-part`, `P^recon` is the `P_avg` column, `4 log q` is what the
integrated `(B4★)` demands with `A_Γ = O(1)`:

| `q` | `W` | `mass` | `𝒢`-part | `𝒦`-part | `4 log q` | integrated `(B4★)` | `P^recon` | `mass − P^recon` |
|---|---|---|---|---|---|---|---|---|
| 3 | [3,5] | 0.16325 | 0.0811 | 0.0821 | 4.3944 | **VIOL** | — | — |
| 3 | [6,8] | 5.53211 | 1.4208 | 4.1113 | 4.3944 | OK | — | — |
| 3 | [9,11] | 5.51163 | −3.4527 | 8.9643 | 4.3944 | OK | — | — |
| 4 | [3,5] | 5.64539 | 1.3644 | 4.2810 | 5.5452 | OK | — | — |
| 4 | [6,8] | 7.38292 | −4.0588 | 11.4418 | 5.5452 | OK | — | — |
| 4 | [9,11] | 7.17625 | −12.2601 | 19.4363 | 5.5452 | OK | — | — |
| 6 | [3,5] | 4.71797 | −3.8165 | 8.5344 | 7.1670 | **VIOL** | — | — |
| 6 | [6,8] | 9.01271 | −9.7626 | 18.7753 | 7.1670 | OK | — | — |
| 6 | [9,11] | 9.27661 | −20.6318 | 29.9084 | 7.1670 | OK | — | — |
| 5 | [3,5] | 6.12402 | −0.6944 | 6.8184 | 6.4378 | **VIOL** | 4.8897 | 1.2343 |
| 5 | [6,8] | 8.44112 | −7.3996 | 15.8407 | 6.4378 | OK | 4.8081 | 3.6330 |
| 5 | [9,11] | 11.80788 | −13.9116 | 25.7195 | 6.4378 | OK | 4.8897 | 6.9181 |
| 7 | [3,5] | 10.08291 | 0.2955 | 9.7874 | 7.7836 | OK | 9.6224 | 0.4605 |
| 7 | [6,8] | 15.82071 | −5.0545 | 20.8752 | 7.7836 | OK | 9.6357 | 6.1850 |
| 7 | [9,11] | 12.76614 | −20.1347 | 32.9009 | 7.7836 | OK | 9.6224 | 3.1437 |
| 9 | [3,5] | 9.62294 | −1.9099 | 11.5329 | 8.7889 | OK | 13.3229 | −3.7000 |
| 9 | [6,8] | 18.09855 | −5.5939 | 23.6925 | 8.7889 | OK | 13.2300 | 4.8686 |
| 9 | [9,11] | 16.68331 | −20.2104 | 36.8937 | 8.7889 | OK | 13.3229 | 3.3604 |
| 12 | [3,5] | 14.90706 | 1.6968 | 13.2103 | 9.9396 | OK | 12.1142 | 2.7929 |
| 12 | [6,8] | 20.01244 | −6.2000 | 26.2125 | 9.9396 | OK | 11.9737 | 8.0387 |
| 12 | [9,11] | 20.73830 | −19.6646 | 40.4029 | 9.9396 | OK | 12.1142 | 8.6241 |
| 15 | [3,5] | 7.48297 | −6.8734 | 14.3563 | 10.8322 | **VIOL** | 14.6152 | −7.1322 |
| 15 | [6,8] | 20.33809 | −7.4583 | 27.7964 | 10.8322 | OK | 14.4517 | 5.8864 |
| 15 | [9,11] | 27.24612 | −15.2920 | 42.5381 | 10.8322 | OK | 14.6152 | 12.6309 |
| 18 | [3,5] | 12.00710 | −3.2191 | 15.2262 | 11.5615 | OK | 13.4012 | −1.3941 |
| 18 | [6,8] | 21.58651 | −7.3336 | 28.9201 | 11.5615 | OK | 13.2305 | 8.3560 |
| 18 | [9,11] | 19.87202 | −24.1261 | 43.9981 | 11.5615 | OK | 13.4012 | 6.4708 |
| 21 | [3,5] | 15.85499 | −0.0736 | 15.9285 | 12.1781 | OK | 14.6692 | 1.1858 |
| 21 | [6,8] | 23.61125 | −6.1705 | 29.7818 | 12.1781 | OK | 14.4244 | 9.1868 |
| 21 | [9,11] | 28.74470 | −16.3337 | 45.0784 | 12.1781 | OK | 14.6692 | 14.0755 |

Three observations, in order of weight.

**(i) The `𝒦`-part is the whole of the `log q` growth, and the `𝒢`-part has none.** OLS in `log q`
over the seven non-arithmetic `q`, per window (`agp_alpha.json`):

| `W` | `α_window𝒦 = ½ · slope(𝒦-part)` | `R²` | **slope(`𝒢`-part)** | `R²` | slope(total) |
|---|---|---|---|---|---|
| [3,5] | **3.1011** | 0.9847 | **−1.6407** | 0.0912 | +4.5615 |
| [6,8] | **4.7164** | 0.9689 | **−0.3672** | 0.0398 | +9.0655 |
| [9,11] | **6.5474** | 0.9629 | **−1.8471** | 0.0745 | +11.2477 |

The `𝒦`-part is a clean straight line in `log q` (`R² = 0.96–0.98`); the resonance part is
structureless (`R² ≤ 0.09`) and its point estimate is **negative**. This settles §7.2's dichotomy
on the first branch: the `log q` is archimedean, and the resonance term supplies **no** positive
`log q` mass — indeed if anything a small negative drift.

**(ii) `α` over the accessible range is larger than its asymptotic value, not smaller.** The
`o(1)` in `𝒜_q = 2 log q + C(r) + o(1)` converges slowly at small `q` (at `r = t₀` the offset moves
from `−0.097` at `q = 3` to `9.317` at `q = 4000`), so the *local* slope over `q = 5 … 21` — the
only range Route B uses — exceeds 2:

| `r` | `α_local` (`q = 5…21`) | `R²` | `α_asymptotic` | `T(0.2)` at `α_local` | `T(0.2)` at `α_asym` |
|---|---|---|---|---|---|
| 3.0 | 2.6545 | 0.99181 | 2.0000 | −0.07892 | −0.02272 |
| 5.5 | 3.8590 | 0.97516 | 2.0001 | −0.18236 | −0.02272 |
| `t₀` | 4.7525 | 0.96858 | 2.0001 | −0.25909 | −0.02272 |
| 10.0 | 6.5462 | 0.96289 | 2.0002 | −0.41312 | −0.02273 |

**Every estimator, `α ∈ [2.0000, 6.5474]`, fires the pre-registered `P4` branch, and every one
makes `T(0.2)` negative.** `α = 2.000` is quoted as the headline because it is the *smallest* and
the most defensible (it is a limit, not a fit over seven points).

**(iii) The integrated `(B4★)` fails in 4 of 30 rows** — `q = 3, 6, 5, 15`, all in the lowest window
`[3,5]` — which is the integrated counterpart of §4. Where it holds, it holds because of the
`𝒦`-part, not the resonances.

> ### ⚠ `agp_window.json` carries a field `alpha_implied` and a `verdict` string that read *"alpha <= 0.2 : A_Gamma benign, Route B budget arithmetic stands"*. **That field is computed by a different formula** (`2 − slope(total mass)/2`, which answers "what `α` makes the integrated budget inequality tight") and it is **NOT** §5.1's `α`. It is superseded by `agp_alpha.{py,json}`, which states the definition explicitly and is what §0 and this section quote. The stale field is left in place rather than edited, because `agp_window.py` is a banked receipt; this warning is the correction.

**Why the pointwise route is not the measurement.** `agp_massbalance.json` records
`−(φ'/φ)(½+ir)` at `r ∈ {4.0, 5.5, t₀, 8.5, 10.0}` for all ten `q`:

| `q` | `r = 4.0` | `5.5` | `t₀` | `8.5` | `10.0` | `2 log q` |
|---|---|---|---|---|---|---|
| 3 | 0.0789 | 0.2668 | **8.1152** | 0.4603 | 1.7727 | 2.1972 |
| 4 | 2.6870 | 1.8438 | **9.0050** | 1.2769 | 2.5977 | 2.7726 |
| 6 | 1.9307 | 1.6638 | **9.7235** | 5.5620 | 3.4251 | 3.5835 |
| 5 | 2.9451 | 2.7078 | 1.7515 | 2.5860 | 4.6475 | 3.2189 |
| 7 | 1.8972 | 2.2607 | 3.1117 | 5.9739 | 9.1407 | 3.8918 |
| 9 | 13.0751 | 17.4134 | 17.4231 | 3.6314 | 3.3565 | 4.3944 |
| 12 | 3.1357 | 2.6854 | 11.9175 | 5.2719 | 2.9071 | 4.9698 |
| 15 | 2.4181 | 11.1887 | 11.0185 | 5.7466 | 4.0700 | 5.4161 |
| 18 | 5.3222 | 4.0055 | 18.0012 | 4.0519 | 7.8523 | 5.7807 |
| 21 | 17.6691 | 3.1598 | 22.5459 | 3.9403 | 4.3197 | 6.0890 |

**A free sanity check falls out of the bolded column, and it is a strong one.** `t₀` is *by
construction* `γ₁/2 = 7.067362570867346`, half the first Riemann zero. For `q = 3` the poles of
`φ₃` in `Re s < ½` are exactly `s = ρ/2` over the zeros of `ζ(2s)`, i.e. **depth `d = ¼` at height
`γ/2`** — so at `r = t₀` a pole sits *exactly on* the evaluation point and contributes
`2d/(d²+0) = 2/(¼) = 8.000` on the nose. Measured: **8.1152** (= 8 + 0.115 from everything else).
The same accidental resonance explains the `q = 4` and `q = 6` spikes. The pipeline is resolving
genuine pole structure at the right depth, and — a warning for the brief — **`r = t₀` is the worst
possible single anchor at arithmetic `q`**, because it is a designed resonance rather than a generic
point.

Those values swing by an order of magnitude between adjacent `r` (`q = 9`:
`13.08, 17.41, 17.42, 3.63, 3.36`), because
`−φ'/φ` is a sum of Poisson spikes. The resulting `log q` fits are pure noise —
pooled `R² = 0.098` for `LHS_direct`, `R² = 0.004` for `LHS − P_q^recon`, with per-`r` slopes
ranging from `−0.48` to `+12.55`. **No `α` should ever be quoted from a point evaluation**, and the
brief's "at `r = t₀` (and 2–3 more `r` for stability)" is, on this evidence, an under-specification
of the measurement: the stable object is the window integral, and the decisive object is the
closed-form `𝒜_q` of §5.2. The pointwise table is banked as the honest negative control.

---

## 6. The sliver `Re ∈ (0.487, ½)` — `agp_sliver_q{15,21}_N16.json`. `MEASURED`

`agp_sliver.py` reuses `routeb_deepcount.py`'s `Evaluator` and adaptive walker **unchanged**, and
changes only the vertical grid to `[0.487, 0.494, 0.4985]` — two extra strata, right edge strictly
inside `Re < ½` so on-line zeros are never enclosed. Same window `Im ∈ [2,12]`, same both-sign sum,
same `NON-RIGOROUS PROBE` rigor label as its parent.

| `q` | `N` | `Re ∈ (0.487, 0.494)` | `(0.494, 0.4985)` | **sliver total** | counted total, `Re ∈ [0.023,0.487]` | max winding residual | `min|det|` on contours | warnings | wall |
|---|---|---|---|---|---|---|---|---|---|
| 15 | 16 | 1 | 0 | **1** | 12 (receipt `N = 12`) | 0.0 | 2.98e−03 at `(0.4985, 9.678)` | 1 | 1125 s |
| 21 | 16 | 1 | 1 | **2** | 12 (receipt `N = 12`) | 0.0 | 1.84e−03 at `(0.4985, 9.695)` | 0 | 3108 s |

Both windings are integers to `0.0` residual. The sliver holds **1** and **2** poles against `12`
counted in `Re ∈ [0.023, 0.487]` — an 8 % and 17 % addition to the population, and in absolute terms
one or two poles per width-10 window.

**What §5.1 needed from this reading, and what it got.** Reading 1 needed the sliver to close a
deficit of `4 log q − 3.844 log q = 0.156 log q` at best, and `4 − 2.6 = 1.4 log q` under realistic
weighting: at `q = 21` that is `0.47` to `4.3` poles' worth of *fully absorbing* (`2π` each) mass
per **width-2** window, i.e. `2.4` to `21` poles across the width-10 window measured here. **Found:
2.** The generous end is marginally reachable, the realistic end is short by an order of magnitude,
and neither can produce a `log q` **slope** — the sliver count does not grow with `q` in any way
these two points can detect (`1 → 2` from `q = 15 → 21`).

*Caveats specific to this measurement:* the right edge at `Re = 0.4985` runs close to the critical
line and `min|det|` falls to `≈ 2e−03` there (small but four orders above the winding residuals);
`q = 15` logged one half-turn-guard hit at `MAX_DEPTH` on the shared edge `Re = 0.487`
(`|Δarg| = 2.23 > π/2`), so its integer carries that flag; and these runs are `N = 16` while the
receipts they extend are `N = 12`.

> **AGP.4 `MEASURED`.** The uncounted sliver holds **1 pole at `q = 15` and 2 at `q = 21`** in the
> whole window `Im ∈ [2,12]`. It cannot supply the `0.16 log q`–`1.4 log q` of missing absorbable
> mass that §5.1's reading 1 needed — and, decisively, it shows no `q`-growth at all, so
> **winding-blindness is not the explanation** for the mass-balance deficit. The two readings
> offered in §5.1 are now separated, and it resolves against the probe's completeness being at
> fault and in favour of `A_Γ`. (Reading 1's *other* consequence — that B5b's measured `(a, b)` are
> not upper bounds — is correspondingly **not** supported by this measurement, which is a small
> positive for the parent.)

---

## 7. Error budget, honestly

### 7.1 What each conclusion depends on

| Conclusion | Depends on the determinant pipeline? | On the mirror identity? | On the pole receipts? |
|---|---|---|---|
| **AGP.2** — `(B4-POINTWISE)` refuted at `q = 3,4,6` | **no** | **no** | **no** |
| **AGP.3** — `𝒜_q = 2 log q + C(r) + o(1)` | **no** | only for the *interpretation* of `𝒜_q` as part of `−φ'/φ`; the growth law itself is a closed-form evaluation | **no** |
| **AGP.1** — pipeline validated | yes | yes (this is the test) | no |
| §5.3 window masses at non-arithmetic `q` | yes | **yes** | no |
| `LHS − P_q^recon` residuals | yes | yes | **yes** |

**The verdict `α = 2` rests on AGP.3, which is the row that depends on nothing measured.** That is
the point of arranging the measurement this way.

### 7.2 The identification `𝒜_q ↔ A_Γ` — what is identity and what is not

`PROVED-here` (given the §2.1 identity): `−φ'/φ = 𝒢_q + 𝒜_q`, with `𝒜_q` explicit.

`IDENTIFICATION, not proved`: that `𝒜_q` **is** the `A_Γ` of the parent's (1.2). The parent's split
is the **Blaschke/Hadamard** split of `φ` (`P_q` = Poisson sum over poles with `Re < ½`; `E_q` over
residual `s_k`; `A_Γ` = the rest); §5.1's split is the **functional-equation** split. They agree in
content — `𝒜_q` consists exactly of Γ-factors, the Barnes/regularized-determinant factor and the
elliptic `sin`-factors, and contains no Blaschke factor at all — but they need not agree term by
term: `𝒢_q` counts **all** zeros of `Z_S` in `0 < Re s < 1`, including the on-line ones, whereas
`P_q` counts only poles of `φ` with `Re < ½`. So
`A_Γ = 𝒜_q + (𝒢_q − P_q + E_q)`, and the strict statement is:

> **either `A_Γ` grows like `2 log q`, or the bracket `𝒢_q − P_q + E_q` supplies a compensating
> `−2 log q`.** The second alternative is not an escape: a resonance term that is negative at scale
> `log q` destroys the budget argument just as thoroughly as `α = 2` does, because the argument
> needs `P_q` bounded **below** by something positive of size `log q`.

Either way `P4` fires, so the verdict does not depend on resolving it. **It is nevertheless
resolved, on the data, in favour of the first branch:** §5.3(i) measures the slope of the `𝒢`-part
directly and finds `−1.64 / −0.37 / −1.85` with `R² ≤ 0.09` on the three windows — structureless
and with no positive `log q` content — against the `𝒦`-part's `R² = 0.96–0.98` straight lines. The
`log q` sits on the archimedean side of the ledger, and the resonance side has none of it.

### 7.3 Remaining caveats, itemised

1. **The identity is confirmed at arithmetic `q` only** (`1.8e−11`–`3.2e−06`, §3) and is
   **assumed** at `q = 5, 7, 9, 12, 15, 18, 21`. Non-arithmetic `φ_q` has no closed form, so this
   cannot be improved by any amount of computation — it is a structural limit of the instrument.
   Every §5.3 number for non-arithmetic `q` inherits it. **AGP.2 and AGP.3 do not.**
2. **`N`-truncation.** `N = 16` (odd) / `24` (even), `n_head = 4`; the even builder is the slower
   converger (`q = 4` gate `3.2e−06`). No dimension tail is folded in — `selberg_Z` returns
   determinant **midpoints**, the same epistemic status as `cert_det_complex_mid`. So §5.3 is
   `MEASURED`, never `PROVED`.
3. **`prec = 128` in `agp_window.py` / `agp_sliver.py`**, justified by the `1.23e−08` prec gate and
   digit-identical determinants against `prec = 400`; `agp_validate.py` and `agp_massbalance.py`
   run at `prec = 400`.
4. **Central difference `h = 1e−4`**, `O(h²)` truncation `≈ 4.3e−05`, identical on both routes and
   cancelling in the comparison (§3.2 V0). Where an analytic derivative exists (`𝒜_q`) it is used
   instead, and it agrees with the difference to `< 1e−12`.
5. **`P_q^recon` is a model, not a measurement.** The receipts give **counts per stratum**, not
   pole positions; heights are modelled uniform on `Im ∈ [2,12]`, depths at stratum midpoints.
   Poles outside that window, and poles in the sliver, are not in it. The `P_hi` column
   (every counted pole at `γ = r`, shallowest depth in its stratum) is the only genuine bound and
   it is uselessly weak (`~1000`). Conclusions are **not** drawn from the residual column.
6. **The receipts are `NON-RIGOROUS PROBE`s** (float arg-unwrap winding, no Arb winding
   certificate), and their `N` is not always the `N` used here (`q = 15, 18, 21` receipts are
   `N = 12`; this probe runs `N = 16`). Flagged, not repaired.
7. **`agp_sliver` inherits every rigor caveat of `routeb_deepcount.py`**, plus one of its own: its
   right edge at `Re = 0.4985` runs close to the critical line, so `min_absdet_on_contours` must be
   read before the integer is believed (§6 table).
8. **`TODO-VERIFY` items inherited and NOT discharged:** Teo arXiv:1901.07898v2 vs LMP 110 (2020)
   61–82 numbering; MMS arXiv:0912.2236 vs DCDS 32 (2012) 2453–2484; **HJL Lemma 5.3 and Hejhal
   LNM 1001 p. 160 were not opened** (blocked HITL library items). AGP.2 therefore refutes *the
   lane's transcription-plus-identification*, which is the only form in which Route B uses it —
   but it does not adjudicate the source.

---

## 8. Per-step status ledger

| # | Step | Statement | Status |
|---|---|---|---|
| G1 | `φ_q = Z_S(1−s)/(Z_S(s) K_q(s))`, with the `det(1−K)` divisor and the corrected Teo kernel | the evaluation route | `PROVED-cited` (Teo Prop. 2.5 + MMS main thm) |
| G2 | `−(φ'/φ)(½+ir) = i · d/dr log φ`, real; `Z_S(1−s) = conj Z_S(s)` on the line | critical-line reduction | `PROVED-here` + `MEASURED` (rel err `0.0`) |
| G3 | `r`-independent factors in G1 cancel in the log-derivative | robustness to the banked `O(1)` residual | `PROVED-here` |
| G4 | determinant route vs exact `φ` at `q = 3, 4, 6` | `1.8e−11 / 3.2e−06 / 8.6e−11`, gate `1e−4` | **`MEASURED`, PASS** — first **phase**-level test of the mirror identity |
| G5 | `arg K_q` must not be unwrapped (branch jumps) | caught by the arithmetic cross-check | `PROVED-here` (defect D1, fixed) |
| G6 | `arg Z_S` must not be unwrapped (on-line zeros ⇒ `2π` each) | residuals exactly `k·2π` | `PROVED-here` (defect D2, fixed) |
| G7 | window mass identity `∫_W −φ'/φ = −Δθ`, verified against exact quadrature | `≤ 2.3e−05` on 9 arithmetic pairs | `PROVED-here` + `MEASURED` |
| G8 | `(B4-POINTWISE)` with `q_{M_q} = q` | `inf_r LHS < 0` at `q = 3,4,6`; 41–57 % of samples violate | **`REFUTED-here`** (exact closed form only) |
| G9 | band mean over `r ∈ [2,12]` vs `2 log q` | `1.329 / 2.675 / 3.603` vs `2.197 / 2.773 / 3.584` | **`MEASURED`** — integrated form also fails at `q = 3, 4` |
| G10 | `𝒜_q(r) = 2 log q + C(r) + o(1)` | slope `2.00002`–`2.00022` at `q = 1000→4000`, four `r` | **`MEASURED`** to `2e−5`, closed form, no pipeline |
| G11 | the slope is carried by the **order-`q` elliptic** Γ-factor | 91.4 % of it; Barnes 8.7 %, saturating; other factors `q`-free | **`MEASURED`** |
| G12 | `α ∈ [2.0000, 6.5474]` over every estimator ⇒ `T(0.2) ∈ [−0.41322, −0.02272] < 0`; `(B4★)` ⇒ `P_q ≥ 0`, vacuous | pre-registered branch `P4`, fired by all | **`MEASURED` ⇒ verdict** |
| G13 | `A_Γ = 𝒜_q + (𝒢_q − P_q + E_q)`; either `A_Γ ~ 2 log q` or the resonance bracket is `~ −2 log q` | both fire `P4`; **resolved on the first branch** — slope(`𝒢`) `= −1.8…−0.4`, `R² ≤ 0.09` vs slope(`𝒦`) `R² ≥ 0.96` | `PROVED-here` (dichotomy) + `MEASURED` (resolution), §5.3(i), §7.2 |
| G14 | sliver `Re ∈ (0.487, ½)` count | `1` at `q = 15`, `2` at `q = 21`, `Im ∈ [2,12]`; residuals `0.0` | **`MEASURED`** — no `q`-growth; winding-blindness `REFUTED-here` as the explanation |
| G15 | pointwise `α` fits | pooled `R² = 0.098` / `0.004`; per-`r` slopes `−0.48 … +12.55` | **`MEASURED`** — negative control; do not quote `α` from point values |
| G16 | `q_{M_q} = q` (parent §1.2(d)) | inconsistent with G8 | **re-opened**, `GAP` |
| G18 | `t₀ = γ₁/2` makes `r = t₀` a designed resonance at arithmetic `q`: a pole of `φ₃` at depth `¼` sits on the point, contributing exactly `8.000`; measured `8.1152` | independent depth-level check of the pipeline, and a warning against `t₀` as a single anchor | **`MEASURED`**, §5.3 |
| G19 | `agp_window.json`'s own `alpha_implied` / `verdict` fields use a budget-tightness formula, not §5.1's `α`, and read the opposite conclusion | superseded by `agp_alpha.{py,json}`; stale field left in place, flagged | correction recorded, §5.3 |
| G17 | N-B4 / N-B4b | not discharged; N-B4b's re-ranking from §5.1 is **confirmed and then superseded** — it is not a risk to be priced, it is a refutation | `GAP` → `REFUTED-here` (in the `q_M = q` form) |

---

## 9. What this changes for Route B, and the honest next lane

**The re-ranking asked for in `LAW_SELFBOUND_TRACE.md` §5.1 is complete, and it went further than
the re-ranking.** N-B4b was to be promoted from "expected harmless slack worth `+0.25` in the
numerator" to "the second-largest risk in Route B after B5". The measurement says it is not a risk
with a price: with `α = 2` the `(THRESH)` numerator is **negative**, and `(B4★)` says only
`P_q ≥ 0`.

**Ranked consequences.**

1. **Any Route B step whose budget is `2 log q` of resonance mass should be treated as having no
   budget at all** until `q_{M_q}` is re-derived from a source that was actually opened. This
   includes the parent's §1.4–1.5 bookkeeping and everything downstream of `(B4★)`. `Q₀ = 1465`
   was already conditional on B5/`(THRESH)`; it now also inherits G16.
2. **`LAW_SELFBOUND_TRACE.md`'s own verdict is unaffected and, if anything, strengthened.** That
   document's negative (`SHORTFALL ≥ 3.98` for *every* test functional) was derived **granting**
   `PREMISE-U` for free. Removing the budget removes the premise's content too; the floor
   `c₂^prov ≥ 0.944` stands on the depth-independence of the Poisson mass and does not use `(B4★)`.
3. **Do not re-attempt the mass-balance route in any variant.** §5.1's deficit is now explained: it
   was not probe incompleteness (§6) and not a tunable `α` (§5.2) — the `log q` was never on the
   resonance side of the ledger.
4. **The one cheap positive to bank:** the pipeline of §2–3 evaluates `−(φ_q'/φ_q)(½+ir)` for
   non-arithmetic Hecke groups with a validated phase, which no prior probe in this lane could do.
   If any future obligation needs the scattering log-derivative rather than a resonance count,
   `agp_phi.py` is the instrument, subject to §7.3(1).
5. **HITL item, unchanged and now load-bearing:** open Hejhal LNM 1001 vol. 2 p. 160 and
   HJL *J. Funct. Anal.* **149** (1997) Lemma 5.3, and determine what `q_M` denotes. G8 says the
   lane's reading of it cannot be right; only the source can say what the right one is.

---

**Sources.** L.-P. Teo, arXiv:1901.07898v2 (LMP **110** (2020) 61–82), Thm 2.2 / Prop. 2.5, via
`LAW_TEO_KAPPA_CORRECTED.md`; D. Mayer, T. Mühlenbruch, F. Strömberg, arXiv:0912.2236 (DCDS **32**
(2012) 2453–2484), main theorem and the `K_s` spectrum, via `LAW_Q3_BRANCH_DIAGNOSIS.md`;
Garbin–Jorgenson, arXiv:1603.01494 (L'Enseign. Math. **64** (2018) 161–206) §5, Thm 5.4/5.7/Ex. 5.8,
via `LAW_SELFBOUND_TRACE.md` and `LAW_ROUTEB_CONDITIONAL_THEOREM.md`; Huntley–Jorgenson–Lundelius,
*J. Funct. Anal.* **149** (1997) 58–82, Lemma 5.3 (**not opened**); Hejhal, LNM 1001 vol. 2 p. 160
(**not opened**, blocked HITL item). Repo: `zeta_cert_rosen{,_even}.py` in
`.worktrees/aletheia-restore/code`; receipts `routeb_deepcount_q*_N*.json`.
Probes: `law_probes/agp_{phi,validate,b4star,massbalance,window,kgrowth,sliver,alpha}.py` + `.json` + `.log`.

**No existing file was modified.** Every file listed above is new. **`git` disclosure:** the brief
said not to run `git`; one read-only `git status --short` WAS run, once, solely to confirm that no
tracked file had been modified (it confirmed that — all lane_g changes are untracked additions).
No `git` command that writes anything was run. This is recorded rather than omitted.
