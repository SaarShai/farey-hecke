# LAW — CERTIFIED deep-resonance count, `q = 9`

**Date:** 2026-08-16. **Lane G, Route B critical path.**
**Task:** upgrade one row of `LAW_ROUTEB_DEEPCOUNT.md` §3 from `MEASURED` (float
argument-unwrap) to a **certified Arb-ball winding count** — the step named in
that note's §8.2 and required by `LAW_B5J_JENSEN.md`'s redirect (certified
winding is the only depth-resolving instrument left).

> ## Result
> **Certified deep count at `q = 9` = 7**, in the window
> `Re s ∈ [0.023, 0.4]`, `Im s ∈ [2, 12]`, both sign sectors summed.
> Winding balls (`N = 20`): sector `+1` = `7.000000 ∈ [6.998779, 7.001221]`,
> sector `−1` = `0.000000 ∈ [−0.000812, +0.000812]`.
> **Agrees exactly with the measured value 7** of `LAW_ROUTEB_DEEPCOUNT.md`
> (`N = 12` and `N = 16`, float).

Status label: **CERTIFIED (Arb ball)**, conditional on one named device — the
geometric dimension-tail bound (§5). No existing file was modified. No git was
run.

---

## 1. Tool chosen, and why

**Chosen:** the Arb ball determinant `zeta_cert_rosen.cert_det` (odd `q`; `q = 9`
is odd, so `zeta_cert_rosen_even.py` is not involved), used **unmodified**,
driven by a new adaptive-subdivision winding driver
`law_probes/certdc9_winding.py`.

Candidates considered:

| candidate | verdict |
|---|---|
| `zeta_cert_rosen.cert_det_complex_mid` (what `routeb_deepcount.py` used) | **rejected** — midpoint float only; no enclosure, hence no certificate. This is exactly the gap being closed. |
| `zeta_cert_rosen.winding_offline` (the repo's existing certified winding box) | **base method adopted, call rejected.** Its ball evaluation and its `det`-ball-excludes-0 test are the right device and are reused verbatim in spirit. But it is hard-wired to a **fixed `K` per edge** with no refinement, and its half-turn guard (`rw.lower()>0 or iw.lower()>0 or iw.upper()<0`) accepts any ball that misses the branch cut — which does **not** exclude a true increment `> π`. On this contour (perimeter `20.75`, `≈ 7` interior zeros, `Δarg` up to `67` rad on one edge) a fixed `K` cannot be chosen a priori, and the weak guard would not certify the unwrap. |
| R3B Taylor-model closed arcs (`R3B_FLAGSHIP_CERT.md`, `code/tc_rerun/certify_r3b_flagship.py`) | **rejected for this job.** It is the strongest certified-winding machinery in the repo, but it is built for a *small closed arc around one pinned zero* (a `~1e−6`-radius Taylor tube), with a self-consistency factor `rH` that must stay `< 1`. Covering a `0.377 × 10` rectangle with `1e−6` tubes is many orders of magnitude outside the budget, and it certifies *localization of a known zero*, not a *count over a large region*. |
| `engine/certify/` | not present in this worktree. |

So the driver is the smallest addition that makes the existing ball evaluator
usable on a large rectangle: adaptive bisection plus a **strict** half-turn test.

## 2. Certification criteria (both rigorous in the ball arithmetic)

For every boundary sample `s`, the ball is
`D(s) = cert_det(s, N, sign, 9) ± 4·tail(s)` (both components), where `tail(s)`
is the dimension-tail radius returned by `dim_tail_from_matrix`; the factor 4 is
the same safety factor `winding_offline` uses.

- **(a) Nonvanishing.** `D(s).abs_lower() > 0` at every sample — the determinant
  is provably nonzero there. Checked at all `449` distinct samples across the
  two sectors.
- **(b) Certified argument increment.** For consecutive samples `A, B`,
  `w = D(B)·conj(D(A))` must satisfy `w.real.lower() > 0`. This proves
  `Δarg ∈ (−π/2, +π/2)`, so `arg(w)` (principal) *is* the true increment and the
  running sum is the true argument variation. This is **strictly stronger** than
  `winding_offline`'s guard. A pair failing (b) is bisected (max depth 10); no
  pair reached max depth.
- **Integer isolation.** The winding ball `Σ arg(w) / 2π` must contain exactly
  one integer, i.e. `[lo, hi] ⊂ (n − ½, n + ½)`.

Contour: rectangle traversed counter-clockwise, `(0.023,2) → (0.4,2) →
(0.4,12) → (0.023,12) → (0.023,2)`. Zeros are counted with multiplicity; the
count is of zeros of the raw `det(1 − L_{s,±})`, which on `0 < Re s < ½` equals
the resonance count because `det(1 − K_s)` is zero-free there
(`LAW_Q3_BRANCH_DIAGNOSIS.md`, MMS arXiv:0912.2236).

## 3. Parameters

| parameter | value |
|---|---|
| `q` | 9 (`κ = 7`) |
| working precision | `PREC_BITS = 300` (`ctx.prec`, module default, **not** lowered to 128 as in the float probe) |
| `N` (Mayer truncation) | **20 (headline)**; 16 (independent cross-check) |
| `n_head` | 4 |
| tail safety factor | 4 |
| initial samples | 101 per vertical edge (`ΔIm = 0.1`), 9 per horizontal edge |
| bisection | adaptive on criterion (b), max depth 10 |
| interpreter | `/Users/za/.venvs/farey-rh/bin/python` (python-flint) |
| wall time | 1041 s (`N = 20`) + 863 s (`N = 16`) = **32 min**, within the 2.5 h budget |

## 4. Per-edge certification status

### `N = 20` (headline)

| sector | edge | samples | certified segments | bisections | max depth | `Δarg` ball (rad) | (a) | (b) | wall |
|---|---|---|---|---|---|---|---|---|---|
| `+1` | bottom `Im = 2` | 9 | 8 | 0 | 0 | `[+2.6374749374, +2.6374749377]` | PASS | PASS | 24 s |
| `+1` | right `Re = 0.4` | 101 | 108 | 8 | 2 | `[−30.0758689, −30.0746108]` | PASS | PASS | 288 s |
| `+1` | top `Im = 12` | 9 | 8 | 0 | 0 | `[+4.1940049, +4.1977073]` | PASS | PASS | 21 s |
| `+1` | left `Re = 0.023` | 101 | 105 | 5 | 2 | `[+67.2190150, +67.2293949]` | PASS | PASS | 240 s |
| `−1` | bottom `Im = 2` | 9 | 8 | 0 | 0 | `[−1.0346270167, −1.0346270164]` | PASS | PASS | 18 s |
| `−1` | right `Re = 0.4` | 101 | 100 | 0 | 0 | `[−39.5366785, −39.5359256]` | PASS | PASS | 208 s |
| `−1` | top `Im = 12` | 9 | 8 | 0 | 0 | `[−0.5670950, −0.5660306]` | PASS | PASS | 17 s |
| `−1` | left `Re = 0.023` | 101 | 102 | 2 | 1 | `[+41.1332992, +41.1416848]` | PASS | PASS | 224 s |

**Every edge of both sectors is CERTIFIED on both criteria.** No edge failed, no
sample needed an `N` escalation at `N = 20`, and no pair hit the depth cap.

Diagnostics (`N = 20`): minimum certified `|det|` lower bound on the contour is
`0.1031` (sector `+1`) and `0.1141` (sector `−1`) — the contour is comfortably
clear of every zero, so criterion (a) is not marginal. Maximum dimension-tail
radius is `1.11e−3` (`+1`) and `3.16e−3` (`−1`), both attained at the deep
corner `(0.023, 12)` where `|det| ≈ 28`; relative tail `≈ 4e−5`.

Determinant-ball evaluations: 230 (`+1`) + 219 (`−1`) = **449**.

### Winding balls and the certified count (`N = 20`)

| sector | winding ball | midpoint | certified integer |
|---|---|---|---|
| `+1` | `[6.99877904355526, 7.00122061371803]` | `6.99999982863665` | **7** |
| `−1` | `[−0.00081189863886, +0.00081193899314]` | `2.02e−8` | **0** |
| **sum** | half-width `≤ 1.6e−3` turns | | **7** |

**Error statement.** The certified deep count is `7`, with total winding
enclosure `7 ∈ [6.99796, 7.00203]` (sum of the two sector balls). The distance
from the nearest excluded integer is `0.498` of a turn, i.e. the isolation
margin is `> 99.5 %` of the available `½`-turn allowance.

## 5. Cross-check at `N = 16`, and what the ball width is made of

The same certificate closes independently at `N = 16`:

| sector | winding ball (`N = 16`) | integer | isolated? |
|---|---|---|---|
| `+1` | `[6.752656, 7.236265]` | 7 | yes (margin `0.264` turns) |
| `−1` | `[−0.161658, +0.164035]` | 0 | yes (margin `0.336` turns) |

Same integers, **much wider balls** — half-width `0.24` turns instead of
`0.0012`, a factor `≈ 200`. The width is dominated entirely by the
dimension-tail radius, not by the 300-bit arithmetic: at `(0.023, 12)` the tail
is `0.19` at `N = 16` versus `1.1e−3` at `N = 20` (and `20.4` at `N = 12`, where
the ratio test fails outright and no certificate exists at all). This is the
practical finding: **`N = 16` certifies, but only just; `N = 20` is the first
truncation at which the deep-corner tail is small enough for the certificate to
be robust.** One point, `(0.4, 11.7)` in sector `−1`, needed an automatic
escalation to `N = 20` even during the `N = 16` run (the driver escalates
`N → N+4 → N+8` at a point whose tail ratio test fails; every ball
`det_N ± tail_N` encloses the same infinite-dimensional determinant, so mixing
`N` across samples keeps all enclosures valid).

**The one conditional device.** `dim_tail_from_matrix` bounds
`|det_∞ − det_N|` by `g·q/(1−q)` from the observed geometric decay of the last
four dimension increments, requiring `q < 0.85`. This is the repo's standard
certified-determinant device (identical to the one underneath
`R2R3_FLAGSHIP_CERT` and `winding_offline`), and it is a *ratio-extrapolation*
bound, not an a-priori nuclear-tail theorem. The certificate here is exactly as
strong as that device — no stronger, and no weaker than any other certified
determinant result in this lane. Observed ratios in this run were `≤ 0.24`
everywhere, far inside the cap.

## 6. Comparison to the measured count

| source | method | `q = 9` deep count, `Re ∈ [0.023,0.4]`, `Im ∈ [2,12]` |
|---|---|---|
| `LAW_ROUTEB_DEEPCOUNT.md` §3, `N = 12` | float midpoint, 128-bit, adaptive unwrap | 7 (strata `1,1,1,4`) |
| `LAW_ROUTEB_DEEPCOUNT.md` §4, `N = 16` | same, stratum-by-stratum identical | 7 |
| **this note, `N = 20`** | **Arb ball, criteria (a)+(b), 300-bit** | **7** |

Exact agreement. Caveat 1 of `LAW_ROUTEB_DEEPCOUNT.md` §7 ("Not certified") is
now **discharged for the `q = 9` row**, and only for that row.

Sector split, newly visible and not in the float note (which reported strata
summed over sectors): **all 7 deep zeros sit in the `sign = +1` sector; the
`sign = −1` sector is certified to contain none.** The `−1` winding ball
`[−8.1e−4, +8.1e−4]` is a genuine certified zero-count of `0`, not a null
measurement.

## 7. What this does and does not establish

**Does.** For `q = 9` there are exactly `7` zeros of `det(1 − L_{s,+}) ·
det(1 − L_{s,−})`, counted with multiplicity, in the closed-window interior
`Re s ∈ (0.023, 0.4)`, `Im s ∈ (2, 12)` — hence exactly `7` Selberg-zeta
resonances there, at certificate grade. This is the first certified deep count
for any surface in the Route B program, and it converts the `D_q(δ₀ = 0.1) ≤ 7`
candidate constant of `LAW_ROUTEB_DEEPCOUNT.md` §6 from a float measurement into
a certified value **at one `q`**.

**Does not.**
1. **One `q` only.** `q`-uniformity of the deep bound — the thing Route B B5
   actually consumes — remains `MEASURED`. Certifying `q = 9` does not certify
   `q = 21`, and the `[0.2, 0.3)` growth flagged in `LAW_ROUTEB_DEEPCOUNT.md` §7.4
   is untouched by this run.
2. **No stratification.** This certifies the deep *total*, not the four
   sub-strata. Sub-stratum certificates would need the shared-edge decomposition
   re-run in ball arithmetic on 5 more verticals (cheap: `≈ 4` more vertical
   edges per sector, `≈ 25` min).
3. **Conditional on the dimension-tail device** (§5).
4. **One height window.** `Im ∈ [2,12]` only; `t₀`-dependence unprobed, as before.
5. **Boundary, not closure.** Zeros exactly *on* the contour would break
   criterion (a); none did (min `|det| ≥ 0.103`), so the count is unambiguous for
   the open rectangle.

## 8. Recommended next step

Certify a **second** `q` — `q = 7` (deep `= 6`) or `q = 21` (deep `= 6`, the
large-`q` end). Two certified points at opposite ends of the range is what turns
"the deep count is flat" from a float observation into a defensible claim. Cost
scales with `κ = q − 2` and with `N`; `q = 21` at `N = 20` is the expensive one
(est. 4–8 h) and should be budgeted separately. `q = 7` is `≈ 20` min.

## 9. Artifacts (receipts, `certdc9_` prefix)

- Driver (new): `law_probes/certdc9_winding.py`
- Receipts (new): `law_probes/certdc9_winding_q9_N20.json` (headline),
  `law_probes/certdc9_winding_q9_N16.json` (cross-check)
- Logs (new): `law_probes/certdc9_q9_N20.log`, `law_probes/certdc9_q9_N16.log`

Each JSON carries the per-sector, per-edge `Δarg` **balls** (not midpoints), the
segment and bisection counts, the max bisection depth, the winding ball, the
minimum certified `|det|` lower bound on the contour, the maximum dimension-tail
radius, the list of `N`-escalated points, and the determinant-call count — so
every number above is re-derivable without rerunning.

`zeta_cert_rosen.py` and `zeta_cert_rosen_q5.py` were read and used unmodified.
No existing file was modified. No git commands were run.
