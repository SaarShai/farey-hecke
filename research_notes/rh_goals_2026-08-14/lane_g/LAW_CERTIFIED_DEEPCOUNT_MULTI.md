# LAW — CERTIFIED deep-resonance count, MULTI-`q` (`q = 7`, `q = 12`)

**Date:** 2026-08-16. **Lane G, Route B critical path.**
**Task:** the §8 next step of `LAW_CERTIFIED_DEEPCOUNT_Q9.md` — certify a
**second and third** `q`, so that "the deep count is flat in `q`" rests on more
than one certified point.

> ## Result
> **Certified deep counts, window `Re s ∈ [0.023, 0.4]`, `Im s ∈ [2, 12]`,
> both sign sectors summed:**
>
> | `q` | certified deep count | headline `N` | measured value | agree? |
> |---|---|---|---|---|
> | 7  | **6** | 20 (cross-checked at 16) | 6 (`N = 12` and `N = 16`) | **yes** |
> | 9  | 7 (prior note) | 20 | 7 | yes |
> | 12 | **5** | 24 (also closes at 20, marginally) | 5 (`N = 20`, `LAW_ROUTEB_SUBSTRATUM.md`) | **yes** |
>
> **No discrepancy.** In particular `q = 12` reads **5**, not 6 — the certificate
> reproduces the `N`-converged measured value, not the unconverged `N = 12`
> value 6 of `LAW_ROUTEB_DEEPCOUNT.md` §3.
>
> Certified deep counts across `q ∈ {7, 9, 12}` are `6, 7, 5` — **no monotone
> trend, spread 2**, at certificate grade.

Status label: **CERTIFIED (Arb ball)**, conditional on the same one named device
as the `q = 9` note — the geometric dimension-tail bound `dim_tail_from_matrix`
(§6). No existing file was modified. No git was run.

---

## 1. Method — identical to `q = 9`, one parameter changed

The ball evaluators are used **unmodified**:

| `q` parity | evaluator | used by |
|---|---|---|
| odd (`q = 7`) | `zeta_cert_rosen.cert_det` | `q = 7` |
| even (`q = 12`) | `zeta_cert_rosen_even.cert_det` | `q = 12` |

**Even `q` IS supported.** `zeta_cert_rosen_even.cert_det` has the same
signature `(s, N, sign, q, n_head=4)` and returns the same
`(det_ball, tail, info, kappa)` tuple; it implements the MMS eq.(32) even-`q`
block structure with `kappa = h_q = (q−2)/2`. This is the same builder pairing
`routeb_deepcount.py` already uses for the float measurement, so no fallback to
`q = 15` was needed. (Caveat carried forward: the even module's own header
scopes its *validation* to `q = 8`; see §7.4.)

Driver: `law_probes/certdcM_winding.py` (**new file**, `certdcM_` prefix). It is
`certdc9_winding.py` with exactly two changes — `q` read from `CERTDCM_Q`, and
the builder module selected by parity. Window, contour orientation,
criteria (a)+(b), tail safety factor 4, `n_head = 4`, bisection rule and depth
cap are byte-for-byte the same logic.

**Certification criteria** (verbatim from the `q = 9` note, both rigorous in ball
arithmetic):

- **(a) Nonvanishing.** `D(s) = cert_det(s,N,sign,q) ± 4·tail(s)` has
  `abs_lower() > 0` at every boundary sample.
- **(b) Certified argument increment.** For consecutive samples `A, B`,
  `w = D(B)·conj(D(A))` has `w.real.lower() > 0`, proving
  `Δarg ∈ (−π/2, +π/2)`; a failing pair is bisected (max depth 10).
- **Integer isolation.** See §4 — the driver's built-in flag uses the strict
  `[lo,hi] ⊂ (n−½, n+½)` test; the weaker and still-rigorous *exactly one
  integer in the ball* test is applied by hand where it matters.

**(a) and (b) PASSED at every sample and every segment of every run below** —
including the `q = 12, N = 20` run whose flag came back `null` (that was an
*isolation-width* failure, not a criterion failure).

## 2. Parameters

| parameter | `q = 7` | `q = 12` |
|---|---|---|
| `kappa` | 5 (odd, `2h+1`) | 5 (even, `h_q`) |
| matrix dimension | `5N` | `5N` |
| working precision | `PREC_BITS = 300` | `PREC_BITS = 300` |
| `N` (headline) | **20** | **24** |
| `N` (secondary) | 16 | 20 |
| `n_head` | 4 | 4 |
| tail safety factor | 4 | 4 |
| initial samples | 101 / vertical edge, 9 / horizontal | same |
| bisection | adaptive on (b), max depth 10 | same |
| interpreter | `/Users/za/.venvs/farey-rh/bin/python` | same |
| wall time | 610 s (`N=20`) + 364 s (`N=16`) | 995 s (`N=24`) + 623 s (`N=20`) |

Total wall for this note: **2592 s = 43 min**, inside the 3 h budget.

## 3. Per-`q` winding-ball tables (both sectors)

### `q = 7`, `N = 20` (headline)

| sector | edge | init samples | certified segments | bisections | max depth | `Δarg` ball (rad) | (a) | (b) | wall |
|---|---|---|---|---|---|---|---|---|---|
| `+1` | bottom `Im=2`   | 9   | 8   | 0 | 0 | `[+0.5125514384, +0.5125514388]` | PASS | PASS | 14 s |
| `+1` | right `Re=0.4`  | 101 | 103 | 3 | 3 | `[−23.4198014, −23.4171937]` | PASS | PASS | 163 s |
| `+1` | top `Im=12`     | 9   | 8   | 0 | 0 | `[+1.9425423, +1.9448389]` | PASS | PASS | 13 s |
| `+1` | left `Re=0.023` | 101 | 102 | 2 | 1 | `[+58.6577003, +58.6650349]` | PASS | PASS | 135 s |
| `−1` | bottom `Im=2`   | 9   | 8   | 0 | 0 | `[+0.9236377557, +0.9236377562]` | PASS | PASS | 11 s |
| `−1` | right `Re=0.4`  | 101 | 100 | 0 | 0 | `[−36.3021034, −36.3016001]` | PASS | PASS | 129 s |
| `−1` | top `Im=12`     | 9   | 8   | 0 | 0 | `[+0.5543409, +0.5549979]` | PASS | PASS | 11 s |
| `−1` | left `Re=0.023` | 101 | 104 | 4 | 1 | `[+34.8219812, +34.8251079]` | PASS | PASS | 136 s |

| sector | winding ball | midpoint | certified integer |
|---|---|---|---|
| `+1` | `[5.99902607500553, 6.00097400695086]` | `6.00000004097819` | **6** |
| `−1` | `[−0.00034115095536, +0.00034114097775]` | `−4.99e−9` | **0** |
| **sum** | `6 ∈ [5.99868492, 6.00131515]` | | **6** |

Isolation margin `0.4987` of a turn (`> 99.7 %` of the available `½`).
Determinant-ball evaluations: 222 (`+1`) + 221 (`−1`) = **443**.
Minimum certified `|det|` lower bound on the contour: `0.0575` (`+1`),
`0.0480` (`−1`). Maximum dimension-tail radius: `9.08e−4` (`+1`),
`1.15e−3` (`−1`), both at the deep corner `(0.023, 12)`. No `N` escalation.

### `q = 7`, `N = 16` (independent cross-check)

| sector | winding ball | integer | isolated? |
|---|---|---|---|
| `+1` | `[5.787685, 6.215862]` | 6 | yes (margin `0.284` turns) |
| `−1` | `[−0.080720, +0.079946]` | 0 | yes (margin `0.419` turns) |

Same integers, balls wider by `≈ 200×`, exactly as at `q = 9`: max tail
`0.173` / `0.234` at `N = 16` versus `9e−4` / `1.1e−3` at `N = 20`. No `N`
escalation was triggered even at `N = 16`. `q = 7` is therefore *easier* than
`q = 9`, where one point needed escalation at `N = 16`.

### `q = 12`, `N = 24` (headline)

| sector | edge | init samples | certified segments | bisections | max depth | `Δarg` ball (rad) | (a) | (b) | wall |
|---|---|---|---|---|---|---|---|---|---|
| `+1` | bottom `Im=2`   | 9   | 8   | 0 | 0 | `[−1.0452976, −1.0452843]` | PASS | PASS | 17 s |
| `+1` | right `Re=0.4`  | 101 | 107 | 7 | 1 | `[−44.4498174, −44.4031589]` | PASS | PASS | 236 s |
| `+1` | top `Im=12`     | 9   | 8   | 0 | 0 | `[−0.0659900, −0.0296184]` | PASS | PASS | 20 s |
| `+1` | left `Re=0.023` | 101 | 102 | 2 | 1 | `[+76.9004987, +76.9704632]` | PASS | PASS | 228 s |
| `−1` | bottom `Im=2`   | 9   | 8   | 0 | 0 | `[−0.5307412, −0.5307284]` | PASS | PASS | 17 s |
| `−1` | right `Re=0.4`  | 101 | 100 | 0 | 0 | `[−43.7611716, −43.7384703]` | PASS | PASS | 236 s |
| `−1` | top `Im=12`     | 9   | 8   | 0 | 0 | `[−0.2694553, −0.2278879]` | PASS | PASS | 18 s |
| `−1` | left `Re=0.023` | 101 | 101 | 1 | 1 | `[+44.5132170, +44.5451831]` | PASS | PASS | 224 s |

| sector | winding ball | midpoint | certified integer |
|---|---|---|---|
| `+1` | `[4.98781941086054, 5.01217140257359]` | `4.99999540671706` | **5** |
| `−1` | `[−0.00766348043180, +0.00765478566973]` | `−4.35e−6` | **0** |
| **sum** | `5 ∈ [4.98015593, 5.01982619]` | | **5** |

Isolation margin `0.480` of a turn. Determinant-ball evaluations:
227 (`+1`) + 226 (`−1`) = **453**. Minimum certified `|det|` lower bound:
`0.1454` (`+1`), `0.0981` (`−1`). Maximum tail: `7.52e−2` (`+1`),
`4.17e−2` (`−1`), both at `(0.023, 12)`.

**`N` escalations (all valid — every ball `det_N ± tail_N` encloses the same
infinite-dimensional determinant):** 1 point in `+1` (`(0.4, 7.1) → N = 28`);
5 points in `−1` (`(0.4, 7.3) → 28`, `(0.4, 8.2) → 32`, `(0.4, 8.3) → 32`,
`(0.4, 9.4) → 32`, `(0.023, 6.2) → 28`). Even `q = 12` is the tail-hardest of
the three surfaces certified so far.

### `q = 12`, `N = 20` — criteria pass, strict flag does not, count still certified

The `N = 20` run (the one the task pre-registered as headline) came back with
`certified_deep_count: null`. **This is not a failed certificate and not a
count discrepancy.** Every sample passed (a) and every segment passed (b); the
driver's `integer_isolated` flag uses the strict test
`[lo,hi] ⊂ (n−½, n+½)`, and the balls are wider than a half-turn:

| sector | winding ball (`N = 20`) | integers inside | strict flag | count by containment |
|---|---|---|---|---|
| `+1` | `[4.04207146, 5.91361135]` | **only 5** (`4 < 4.042`, `5.914 < 6`) | fail (width `1.87`) | **5** |
| `−1` | `[−0.50775092, +0.49244427]` | **only 0** | fail (width `1.00`) | **0** |

The argument principle makes the total winding an **exact integer** whenever (a)
holds on the contour and (b) validates the unwrap — both certified here. A ball
that encloses that integer and contains exactly one integer therefore *pins* it.
So `q = 12, N = 20` independently certifies **5**, with margins `0.042` (below 4)
and `0.086` (below 6) of a turn on the `+1` sector — thin, but rigorous.

The `N = 24` run is the headline because those margins are uncomfortable, not
because `N = 20` is invalid. The two runs agree.

**Why `q = 12` needs a larger `N` than `q = 7` or `q = 9`.** The width is
entirely the dimension tail at the deep corner `(0.023, 12)`, and the even-`q`
operator converges much more slowly there:

| `N` | tail at `(0.023,12)`, `q = 12`, `+1` | `\|det\|` there | relative |
|---|---|---|---|
| 20 | `4.53` | `209` | `2.2e−2` |
| 24 | `7.52e−2` | `209` | `3.6e−4` |
| 28 | `1.05e−3` | `209` | `5.0e−6` |

Compare `q = 7` at `N = 20`: tail `9.1e−4`. **`N = 20` is the robust truncation
for odd `q = 7, 9`; for even `q = 12` the robust truncation is `N = 24`.** This
is a new practical finding and the main methodological content of this note.

## 4. Comparison to the measured values

| `q` | measured (source) | certified (this note / `q = 9` note) | agree? |
|---|---|---|---|
| 7  | 6 — `routeb_deepcount_q7_N12.json`, `_q7_N16.json` (stratum-identical: `1,1,1,3`) | **6** (`N = 20`, `N = 16`) | **exact** |
| 9  | 7 — `LAW_ROUTEB_DEEPCOUNT.md` §3–4 | 7 (`N = 20`, `N = 16`) | exact |
| 12 | **5** — `routeb2_substratum_q12_N20_deep.json` (`0,1,4,0`), stable from `N = 16` | **5** (`N = 24`, and `N = 20`) | **exact** |
| 12 | 6 — `LAW_ROUTEB_DEEPCOUNT.md` §3 at `N = 12` (unconverged) | 5 | superseded, as expected |

**The pre-registered discrepancy check on `q = 12` is CLEAN.** The task flagged
that a certified reading of 6 would be a loud discrepancy against the
`N`-converged measured 5. The certificate reads **5**. The `N`-convergence story
of `LAW_ROUTEB_SUBSTRATUM.md` (`8 → 6 → 5 → 5` at `N = 8/12/16/20`) is confirmed
at certificate grade, and the downward drift with `N` is confirmed to have
stopped.

Sector split, at all three certified `q`:

| `q` | sign `+1` | sign `−1` |
|---|---|---|
| 7  | 6 | **0** |
| 9  | 7 | **0** |
| 12 | 5 | **0** |

**Every deep zero in this window sits in the `sign = +1` sector, at all three
certified `q`, including one even `q`.** The `−1` sector emptiness is a genuine
certified zero-count, not a null measurement (balls `±3.4e−4`, `±8.1e−4`,
`±7.7e−3`). This matches the float receipts (`sign −1` deep `= 0` in every
`routeb_deepcount_q*.json` inspected) and is now certificate-grade at three `q`.

## 5. Cumulative certified picture

Row-by-row status of the deep column of `LAW_ROUTEB_DEEPCOUNT.md` §3:

| `q` | deep count | status after this note |
|---|---|---|
| 5  | 2 | MEASURED |
| **7**  | **6** | **CERTIFIED** (this note) |
| 8  | 6 | MEASURED |
| **9**  | **7** | **CERTIFIED** (`LAW_CERTIFIED_DEEPCOUNT_Q9.md`) |
| 10 | 7 | MEASURED |
| 11 | 6 | MEASURED |
| **12** | **5** | **CERTIFIED** (this note; supersedes the `N=12` value 6) |
| 15 | 7 | MEASURED (`N = 12` only) |
| 18 | 6 | MEASURED (`N = 12` only) |
| 21 | 6 | MEASURED (`N = 12` only) |

**3 of 10 rows are now certificate-grade**, covering both parities and spanning
`q = 7` to `q = 12`. Caveat 1 of `LAW_ROUTEB_DEEPCOUNT.md` §7 ("Not certified")
is discharged for those three rows and for no other.

**What the certified subset says about the constant.** The candidate constant of
`LAW_ROUTEB_DEEPCOUNT.md` §6 is `D_q(δ₀ = 0.1) ≤ 7` in a height-10 window. Over
the certified `q ∈ {7, 9, 12}` the values are `6, 7, 5`, so:

> `D_q(0.1) ≤ 7` is **CERTIFIED for `q ∈ {7, 9, 12}`** and remains MEASURED for
> the other seven groups. Deep count per unit height over the certified subset:
> `0.5`–`0.7`.

Three certified points, non-monotone (`6, 7, 5`) and with the *largest* `q` of
the three giving the *smallest* count, is direct certificate-grade evidence
against deep growth in `q`. It is not a proof of `q`-uniformity: three points,
one window, `q ≤ 12`.

## 6. The one conditional device (unchanged)

`dim_tail_from_matrix` (odd `q`) / `dim_tail_from_matrix_signed` (even `q`)
bounds `|det_∞ − det_N|` by `g·r/(1−r)` from the observed geometric decay of the
last four dimension increments, requiring `r < 0.85`. Every certificate here is
exactly as strong as that ratio-extrapolation device — identical to the `q = 9`
note, to `R2R3_FLAGSHIP_CERT`, and to `winding_offline`. Where the ratio test
failed at a point, the driver escalated `N` rather than proceeding (§3, `q = 12`);
no run ended with an uncertified tail.

## 7. What this does and does not establish

**Does.**
1. For `q = 7` there are exactly **6**, and for `q = 12` exactly **5**, zeros of
   `det(1−L_{s,+})·det(1−L_{s,−})` with multiplicity in the open rectangle
   `Re s ∈ (0.023, 0.4)`, `Im s ∈ (2, 12)` — hence exactly that many
   Selberg-zeta resonances there, at certificate grade.
2. The **first certified deep count on an even-`q` Hecke surface**, via the
   even-`q` MMS block builder.
3. Three certified `q`, non-monotone, is the "two points at opposite ends"
   step that `LAW_CERTIFIED_DEEPCOUNT_Q9.md` §8 asked for (`q = 12` substitutes
   for `q = 21`, which remains a 4–8 h job).

**Does not.**
1. **`q`-uniformity is still not certified.** `q = 15, 18, 21` — the large-`q`
   end that Route B B5 actually needs — remain MEASURED at `N = 12` only.
   `q = 21` is untouched.
2. **No stratification.** These are deep *totals*; the `[0.2,0.3)` growth flagged
   in `LAW_ROUTEB_DEEPCOUNT.md` §7.4 is not addressed. Certifying it needs the
   shared-edge decomposition re-run in ball arithmetic on the interior verticals.
3. **Conditional on the dimension-tail device** (§6).
4. **Even-`q` builder validation scope.** `zeta_cert_rosen_even.py`'s header
   states it was cross-validated against the double-precision reference at
   `q = 8` and disclaims `q ≠ 8` claims. This certificate inherits that scope
   limit: the *winding arithmetic* is certified, and the *builder* is the same
   general even-`q` code the float measurement used, but an independent
   `q = 12` builder cross-validation was not run here. The exact agreement with
   the independently-coded float path (`routeb2_substratum_q12_N20_deep.json`,
   count and sector split) is evidence, not a validation.
5. **One height window** `Im ∈ [2,12]`; `t₀`-dependence unprobed.
6. **Boundary, not closure.** Min `|det|` lower bounds `0.048`–`0.145`; no zero
   sits on a contour, so the counts are unambiguous for the open rectangles.

## 8. Recommended next steps

1. **`q = 21` at `N = 20`** (odd, `kappa = 19`, matrix `380`) — the large-`q` end,
   the only remaining thing that would let the flatness claim be stated
   certified across the measured range. Budget separately (est. 4–8 h).
2. **`q = 15` at `N = 20`**, cheaper (`kappa = 13`), and it also closes the one
   partial cell left by `LAW_ROUTEB_SUBSTRATUM.md` §3.
3. **Even-`q` builder cross-validation at `q = 12`** against the
   `zeta_mayer_rosen` double-precision reference, to lift caveat 7.4.
4. If any further **even** `q` is certified, start at `N = 24`, not `N = 20`
   (§3).

## 9. Artifacts (receipts, `certdcM_` prefix)

- Driver (new): `law_probes/certdcM_winding.py`
- Receipts (new): `law_probes/certdcM_winding_q7_N20.json` (headline `q=7`),
  `law_probes/certdcM_winding_q7_N16.json` (cross-check),
  `law_probes/certdcM_winding_q12_N24.json` (headline `q=12`),
  `law_probes/certdcM_winding_q12_N20.json` (secondary; strict flag `null`, see §3)
- Logs (new): `law_probes/certdcM_q7_N20.log`, `certdcM_q7_N16.log`,
  `certdcM_q12_N24.log`, `certdcM_q12_N20.log`

Each JSON carries per-sector, per-edge `Δarg` **balls**, segment and bisection
counts, max bisection depth, the winding ball, the minimum certified `|det|`
lower bound, the maximum dimension-tail radius **and its location**, the list of
`N`-escalated points, and the determinant-call count.

`zeta_cert_rosen.py` and `zeta_cert_rosen_even.py` were read and used
unmodified. No existing file was modified. No git commands were run.
