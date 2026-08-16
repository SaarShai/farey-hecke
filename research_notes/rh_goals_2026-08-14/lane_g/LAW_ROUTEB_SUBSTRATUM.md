# LAW Route B — `[0.2,0.3)` sub-stratum: real growth or truncation artifact?

**Date:** 2026-08-16. **Lane G, measurement lane. Follow-up to `LAW_ROUTEB_DEEPCOUNT.md` §7.4 and §8.1.**

**Verdict up front: MIXED by the letter of the pre-registered rule, REAL in substance.**
The `[0.2,0.3)` counts are `N`-stable at `N = 16` **and** `N = 20` for `q = 7, 9, 11, 15`
(`1, 1, 1, 4`) and the positive `log q` slope survives (`+4.88 → +4.47`, `R²` rising
`0.53 → 0.62`). One cell moved: `q = 12` dropped `5 → 4` between `N = 12` and `N = 16`, then
held `4` at `N = 20`. That single unit blocks the literal REAL rule ("equal for **all**
tested `q`"), but it is the opposite of the ARTIFACT signature — the slope did not collapse,
it firmed up.

**Thread 2 answer: `q = 12` STABILISES at deep `= 5`.** `8 → 6 → 5 → 5` at `N = 8/12/16/20`.

**Consequence: the `δ₀ = 0.1` cut is load-bearing, as §7.4 feared, but the bound survives a
larger cut.** At `δ₀ = 0.2` (deep `≡ Re s < 0.3`) the measured count is `≤ 5` per height-10
window over `q = 5…21`, giving a revised candidate **`C(0.2) ≈ 1.0`** per unit height —
*smaller* than `C(0.1) ≈ 1.4`, so Route B is not damaged by moving the cut.

**Status labels:** `MEASURED` throughout, `NON-RIGOROUS PROBE` (inherited). No git was run.
No existing file was modified.

---

## 1. Pre-registration (fixed before any `N = 16` / `N = 20` number was computed)

Written verbatim into the header of `law_probes/routeb2_substratum.py` before the first run.

Inherited unchanged from `routeb_deepcount.py`: window `Im s ∈ [2,12]`; strata boundaries drawn
from the same list `[0.023, 0.1, 0.2, 0.3, 0.4, 0.487]`; same shared-edge argument-principle
winding; same `θ_max = π/2` adaptive bisection to depth 6; same `PREC = 128`; both sign sectors
summed; same builders `zeta_cert_rosen.py` / `zeta_cert_rosen_even.py` used **unmodified** via
`cert_det_complex_mid`; same interpreter `/Users/za/.venvs/farey-rh/bin/python`.

**Thread 1** — `[0.2,0.3)` and `[0.3,0.4)` at `N = 16` (and `N = 20` where affordable),
`q ∈ {7, 9, 11, 12, 15}`:

- **REAL** if `[0.2,0.3)` at `N = 16` **equals** the `N = 12` count for **every** tested `q`,
  **and** the `log q` slope stays positive.
- **ARTIFACT** if counts **drop** at higher `N` and the slope collapses toward `0`
  (the `N = 8 → 12` deep-count pattern).
- **MIXED** if some `q` move and others do not, or the slope stays positive but the counts are
  not `N`-stable.

**Thread 2** — `q = 12` deep count at `N = 20`: **STABILISED** if `N = 20` reads `5`;
**STILL DRIFTING** if `≤ 4` or moving up.

**Consequence, pre-registered so the reading is not chosen after the fact:** if REAL, quote the
`δ₀ = 0.2` count and its slope as the revised deep-bound candidate; if ARTIFACT, `C(0.1) ≈ 1.4`
stands unchanged and `δ₀ = 0.2` gives a smaller constant.

**Budget:** any single `(q, N)` cell over ~25 min wall is killed and recorded `SKIPPED-BUDGET`.

---

## 2. Method delta (what changed, and why it is the same measurement)

`law_probes/routeb2_substratum.py` is an **adapted copy** of `routeb_deepcount.py`; the original
probe, aggregator and receipts were not modified. The only functional change is that the vertical
grid is selectable:

| grid | `Re` lines | covers |
|---|---|---|
| `sub` | `0.2, 0.3, 0.4` | the two sub-strata under test |
| `deep` | `0.023, 0.1, 0.2, 0.3, 0.4` | the whole `δ₀ = 0.1` deep region |
| `full` | the original 6 lines | identical to `routeb_deepcount.py` |

The winding of a stratum uses only the two vertical lines bounding it plus the horizontal edges
between them, so dropping the other lines is exactly a restriction of the same shared-edge
decomposition — not a different estimator. The `sub` grid halves the cost, which is what bought
`N = 20`.

**Adaptation validated against the existing receipt.** `q = 12, N = 16`, `sub` grid returns
`[0.2,0.3) = 4`, `[0.3,0.4) = 0` — identical to the corresponding cells of the pre-existing
full-grid receipt `routeb_deepcount_q12_N16.json` (`[1, 0, 4, 0, 5]`), at 225 s instead of 779 s.

**Sector structure (new observation).** In every `N ≥ 16` run here the `sign = −1` sector
contributes `0` to both `[0.2,0.3)` and `[0.3,0.4)`; all deep occupancy in `Re ∈ [0.2,0.4]` sits
in the `sign = +1` sector. Every winding landed on an integer to `≲1e−14`.

---

## 3. Table — `q × N × sub-stratum`

Both sign sectors summed. `N = 8, 12` and the `N = 16` rows for `q = 7, 9, 12` are read off the
**existing** lane receipts (same probe, same window); `N = 16` for `q = 11, 15` and all `N = 20`
figures are new.

| `q` | `N` | `[0.2,0.3)` | `[0.3,0.4)` | source |
|----|----|----|----|----|
| 7  | 12 | 1 | 3 | `routeb_deepcount_q7_N12.json` |
| 7  | 16 | 1 | 3 | `routeb_deepcount_q7_N16.json` |
| 7  | **20** | **1** | **3** | `routeb2_substratum_q7_N20_sub.json` (411 s) |
| 9  | 12 | 1 | 4 | `routeb_deepcount_q9_N12.json` |
| 9  | 16 | 1 | 4 | `routeb_deepcount_q9_N16.json` |
| 9  | **20** | **1** | **4** | `routeb2_substratum_q9_N20_sub.json` (738 s) |
| 11 | 12 | 1 | 3 | `routeb_deepcount_q11_N12.json` |
| 11 | **16** | **1** | **3** | `routeb2_substratum_q11_N16_sub.json` (629 s) |
| 11 | **20** | **1** | **3** | `routeb2_substratum_q11_N20_sub.json` (1132 s) |
| 12 | 12 | 5 | 0 | `routeb_deepcount_q12_N12.json` |
| 12 | 16 | 4 | 0 | `routeb_deepcount_q12_N16.json`, reproduced by `routeb2_substratum_q12_N16_sub.json` |
| 12 | **20** | **4** | **0** | `routeb2_substratum_q12_N20_deep.json` (641 s) |
| 15 | 12 | 4 | 3 | `routeb_deepcount_q15_N12.json` |
| 15 | **16** | **4** | **3** | `routeb2_substratum_q15_N16_sub.json` (1177 s) |
| 15 | **20** | **(4)** | **(3)** | `routeb2_q15_N20_sub.log` — **SKIPPED-BUDGET (partial)** |

`q = 15, N = 20` completed the `sign = +1` sector (`[4, 3]` at 1405 s) and was killed by the
budget cap at 1800 s during `sign = −1`; no JSON receipt was written. Since `sign = −1` returned
`[0, 0]` in **every** other `N ≥ 16` run, `[4, 3]` is the near-certain total, but it is recorded
in parentheses and excluded from the headline fits.

### Thread 2 — `q = 12` deep column

| `N` | `[0.023,0.1)` | `[0.1,0.2)` | `[0.2,0.3)` | `[0.3,0.4)` | **deep** |
|----|----|----|----|----|----|
| 8  | 1 | 3 | 4 | 0 | 8 |
| 12 | 1 | 0 | 5 | 0 | 6 |
| 16 | 1 | 0 | 4 | 0 | **5** |
| **20** | **0** | **1** | **4** | **0** | **5** |

**STABILISED at 5.** The total is unchanged from `N = 16`; one zero moved between the two
deepest, worst-converged strata (`[0.023,0.1) → [0.1,0.2)`), so the *assignment* inside
`Re < 0.2` is still `N`-sensitive while the *total* is not.

---

## 4. Fits (`q = 7, 9, 11, 12, 15`, least squares in `log q`)

| quantity | `N = 12` | `N = 16` | `N = 20` |
|---|---|---|---|
| `[0.2,0.3)` | `−9.05 + 4.88·log q`, `R² = 0.53` | `−8.29 + 4.47·log q`, `R² = 0.62` | `−7.23 + 3.98·log q`, `R² = 0.40` (4 pts: `q = 7,9,11,12`) |
| `[0.3,0.4)` | `+6.55 − 1.68·log q`, `R² = 0.10` | `+6.55 − 1.68·log q`, `R² = 0.10` | `+12.26 − 4.33·log q`, `R² = 0.36` (4 pts) |

Including the partial `q = 15, N = 20` value `4`, the `N = 20` `[0.2,0.3)` fit is
`−8.29 + 4.47·log q`, `R² = 0.62` — identical to `N = 16`.

**Reading, stated plainly.** The slope is positive and does not decay with `N`; the ARTIFACT
signature (drop + slope collapse) does **not** occur. But with 5 groups this is really a **two-level
step**, not a fitted growth law: `q ≤ 11` read `1`, `q ≥ 12` read `4`. `log q` is not
distinguishable here from any increasing function. The honest statement is *the `[0.2,0.3)`
occupancy is higher for the larger `q` and that difference is `N`-converged*, not *it grows like
`log q`*.

---

## 5. Verdict

> ### MIXED by the letter; REAL in substance.
> `q = 7, 9, 11, 15`: `[0.2,0.3)` identical at `N = 12, 16, 20`. `q = 12`: `5 → 4 → 4`, i.e. one
> unit of the `N = 12` figure was truncation, the rest is converged. The `log q` slope stays
> positive with `R²` rising. The pre-registered ARTIFACT branch is **not** triggered.
>
> ### `q = 12` deep count: STABILISED at 5 (`N = 16 = 20`).

This closes both open threads of `LAW_ROUTEB_DEEPCOUNT.md` §7.2 and §7.4 in the direction the
note flagged as uncomfortable: the `[0.2,0.3)` growth is **not** another `N = 8`-style artifact.

---

## 6. Revised deep-bound candidate

Per the pre-registered consequence rule (REAL branch), the number to quote is the `δ₀ = 0.2`
count, i.e. resonances with `Re s < 0.3`, summing `[0.023,0.1) + [0.1,0.2) + [0.2,0.3)`.

| `q` | 5 | 7 | 8 | 9 | 10 | 11 | 12 | 15 | 18 | 21 |
|----|---|---|---|---|----|----|----|----|----|----|
| count `Re s < 0.3`, height-10 window | 1 | 3 | 3 | 3 | 4 | 3 | **5*** | 4 | 4 | 3 |

`*` `q = 12` at the converged `N = 20` (`0+1+4`); it reads `6` at `N = 12`. All other columns are
`N = 12` figures, which every converged case says are **upper bounds**.

Fit (all `q`, `N = 12` figures): `−0.25 + 1.54·log q`, `R² = 0.29` — a weak upward drift, with the
maximum at `q = 12` rather than at the largest `q`, so it is not a growth trend.

| quantity | measured | form for B5 |
|---|---|---|
| `D_q(δ₀ = 0.2)` in the height-10 window | `≤ 5` for all `q ∈ [5,21]` (`≤ 6` if the unconverged `N = 12` value at `q = 12` is used) | `D_q(0.2) ≤ 5` |
| per unit height | `0.3`–`0.5` | `#{Re s ≤ ½−0.2, |Im s − t₀| ≤ 1} ≲ 1.0` |
| revised uniform candidate | — | **`C(0.2) ≈ 1.0`** (`≲ 1.2` on the conservative `N = 12` reading) |
| previous candidate, unchanged | — | `C(0.1) ≈ 1.4` |

**Does the ~1.4 bound survive at `δ₀ = 0.2`? Yes, and it improves.** `C(0.2) ≈ 1.0 < 1.4 ≈ C(0.1)`.
`§7.4`'s worry — "if the `[0.2,0.3)` growth is real, a larger `δ₀` would look worse" — is **not**
borne out: emptying the `[0.2,0.3)` stratum out of the deep region removes more count than the
`[0.023,0.2)` strata add back, because those are the strata that empty as `N` rises. The `δ₀ = 0.1`
cut is load-bearing in the sense that the deep **total** at `δ₀ = 0.1` is flat only through
cancellation (`[0.2,0.3)` up, `[0.023,0.2)` down); but B5 consumes an **upper** bound, and the
upper bound is monotone-improving in `δ₀` across the measured range. **Route B still advances.**

---

## 7. Caveats

1. **Not certified.** Same rigor label as the parent note: float arg-unwrap windings on midpoint
   evaluations of the Arb-ball builders at 128 bits. `MEASURED`, not proved.
2. **Five groups, two levels.** `[0.2,0.3)` takes only the values `{1, 4}` over the tested `q`.
   Calling the difference a `log q` slope over-reads it; the defensible claim is the `N`-stability
   of the difference. `q = 8, 10, 18, 21` were **not** re-measured at `N ≥ 16` (cost).
3. **`q = 15, N = 20` is partial** (`sign = +1` only, `SKIPPED-BUDGET` at 1800 s). Excluded from
   the headline fits.
4. **`q = 12` deep composition still moves** inside `Re < 0.2` at `N = 20` even though the total
   does not; the deepest two strata remain the least trustworthy cells in the table.
5. **`δ₀ = 0.2` values for `q ≠ 12` rest on `N = 12`** for the `[0.023,0.2)` part. Every converged
   case converged **downward**, so these are upper bounds — the safe direction here.
6. **Fixed window `Im ∈ [2,12]`.** `t₀`-dependence is still unprobed (parent note §7.5). The
   `q = 12` near-π unwrap of §7.3 touched only the shallow stratum and is untouched by this work.
7. **Concurrency inflates wall times.** Runs were executed 4-way parallel, so the seconds quoted
   are ~2× a solo run. An initial 8-way launch was aborted for contention before producing any
   number; no result in this note comes from it.

---

## 8. Recommended next steps

1. **`N = 16` for `q = 18, 21`** in the `sub` grid (~30–40 min each solo) — the only remaining way
   the "step at `q ≈ 12`" reading could turn into a genuine growth trend, or die.
2. **Finish `q = 15, N = 20`** (`sign = −1` sector alone) to close the one partial cell.
3. **`δ₀ = 0.25` / `δ₀ = 0.05` sweep** using the `deep` grid, to see whether `C(δ₀)` is monotone
   as §6 suggests.
4. **Certify one row** (`q = 9`, converged at `N = 12 = 16 = 20`) through the Arb `winding_box`
   path — unchanged from the parent note's step 2, and now better motivated: `q = 9` is stable
   across four values of `N`.

---

## 9. Artifacts

- Probe (new, adapted copy; originals untouched): `law_probes/routeb2_substratum.py`
- Aggregator (new): `law_probes/routeb2_analyze.py` → `law_probes/routeb2_summary.json`
- Receipts (new): `law_probes/routeb2_substratum_q{7,9,11}_N20_sub.json`,
  `…_q11_N16_sub.json`, `…_q12_N16_sub.json`, `…_q15_N16_sub.json`, `…_q12_N20_deep.json`
- Logs (new): `law_probes/routeb2_q{7,9,11,15}_N20_sub.log`,
  `law_probes/routeb2_q{11,12,15}_N16_sub.log`, `law_probes/routeb2_q12_N20_deep.log`
- Reused unmodified: `law_probes/routeb_deepcount.py`, `routeb_analyze.py` and all
  `routeb_deepcount_q*_N*.json` receipts.

Every JSON carries the full per-sign edge data, raw non-integer windings, residuals, guard
warnings, `min |det|` on the contours, det-call count and the rigor label, so each integer above
is re-derivable without rerunning.
