# LAW Route B — window-2 deep-count probe (gap M3, `t₀`-uniformity)

**Date:** 2026-08-16. **Lane G, measurement lane.**
**Target:** the `t₀`-uniformity gap of `LAW_ROUTEB_CONDITIONAL_THEOREM.md` §gaps. B5/B6 are
stated *per* `t₀`; `LAW_ROUTEB_DEEPCOUNT.md` measured **one** height window, `Im s ∈ [2,12]`,
and found the deep count flat at `6–7` for `q ≥ 7`. Caveat 5 of that note says `t₀`-dependence
was never probed. This probe repeats the measurement in a **second** window.

**Verdict up front: INCONCLUSIVE — and the little signal there is points the wrong way.**
In `Im s ∈ [12,22]` the deep count is **not `N`-converged at any `q`** (it falls at every
`N`-refinement, at every `q` tested, including at `N = 20`), so the pre-registered
`INCONCLUSIVE` branch fires by its own terms. At every *fixed* `N` the window-2 deep count
carries a **large positive `log q` slope** (`+11.8` at `N=12`, `+7.3` at `N=16`, `+10.9` at
`N=20`), against `+0.63`, `R² = 0.11` for the same `q` in window 1. Route-B `t₀`-uniformity is
**not supported by this probe**; it is not refuted either, because the numbers are truncation
upper bounds that are still moving.

**Status labels:** `MEASURED`, `NON-RIGOROUS PROBE` throughout. No git was run. No existing file
was modified.

---

## 1. Pre-registration (fixed before any window-2 number was computed)

Written verbatim into the docstring of `law_probes/routeb4_window2.py` before the first run.

- **Window 2:** `Im s ∈ [12, 22]` — the adjacent decade, **same height 10** as window 1
  (`Im s ∈ [2,12]`).
- **Strata:** grid `deep` = `[0.023, 0.1, 0.2, 0.3, 0.4]`; **DEEP** = `Re s < 0.4`, i.e.
  `δ₀ = 0.1`. Identical to window 1's deep region.
- **Groups:** `q = 7, 9, 11, 12, 15` at `N = 12`; `N = 16` spot-check at `q = 9, 12`.
- **SUPPORTED** if the deep count is again `q`-flat: values in a constant band, no positive
  `log q` trend, least-squares slope statistically indistinguishable from `0` as in window 1.
- **UNDERMINED** if deep counts grow with `q` in the new window.
- **INCONCLUSIVE** otherwise, or if the counts are not `N`-stable.
- **Theory note, pre-registered:** resonance density grows with height (Weyl-type), so absolute
  window-2 counts may exceed window-1 counts. The test is `q`-flatness at fixed window, **not**
  equality with window 1. Higher `Im` may need larger `N`; if `q = 9` disagrees between `N = 12`
  and `N = 16`, escalate `N` before trusting anything.

The `N`-escalation clause fired (§4). `N = 20` was run at `q = 7, 9, 12`, and `N = 16` was added
at `q = 7, 11` beyond the pre-registered spot-checks.

---

## 2. Method and the exact diff

Machinery reused unchanged from `law_probes/routeb2_substratum.py`: shared-edge
argument-principle winding on the vertical grid lines `Re = 0.023, 0.1, 0.2, 0.3, 0.4` and the
two horizontal edges, adaptive bisection at `θ_max = π/2` to depth 6, `PREC = 128`, both sign
sectors `±1` summed, builders `zeta_cert_rosen.py` / `zeta_cert_rosen_even.py` used **unmodified**
via `cert_det_complex_mid`, interpreter `/Users/za/.venvs/farey-rh/bin/python`.

**The adapted copy is `law_probes/routeb4_window2.py`. The code diff against
`routeb2_substratum.py` is exactly two lines** (docstring replaced with this pre-registration;
everything else byte-identical, verified by `diff`):

```
21c21
< T1, T2 = 2.0, 12.0
---
> T1, T2 = 12.0, 22.0
160c160
<     path = OUTDIR / (f"routeb2_substratum_q{q}_N{N}_{grid_name}"
---
>     path = OUTDIR / (f"routeb4_window2_q{q}_N{N}_{grid_name}"
```

**Rigor label.** `NON-RIGOROUS PROBE`, identical to window 1: midpoint float evaluation of the
Arb-ball builders at reduced precision, float arg-unwrap winding with a half-turn guard, no
certified enclosure, no certified dim-tail. Not a certificate.

---

## 3. Window-2 stratified deep counts

Both sign sectors summed. `deep` grid only, so **no shallow stratum** `[0.4,0.487)` was measured
in window 2 (the brief specified grid `deep`); the shallow-vs-deep split of window 1 is therefore
**not** reproduced here — only the deep side is under test.

| `q` | `N` | `[0.023,0.1)` | `[0.1,0.2)` | `[0.2,0.3)` | `[0.3,0.4)` | **DEEP** `Re<0.4` | max residual | guard warnings | wall (s) |
|----|----|----|----|----|----|----|----|----|----|
| 7  | 12 | 1 | 2 | 2 | 3 | **8**  | 1.4e−14 | 0 | 412 |
| 7  | 16 | 1 | 2 | 1 | 3 | **7**  | 1.2e−14 | 0 | 594 |
| 7  | 20 | 0 | 0 | 1 | 2 | **3**  | 9.0e−15 | 0 | 970 |
| 9  | 12 | 3 | 4 | 2 | 8 | **17** | 1.7e−14 | 0 | 878 |
| 9  | 16 | 2 | 2 | 2 | 8 | **14** | 2.0e−14 | 0 | 1530 |
| 9  | 20 | 1 | 1 | 1 | 5 | **8**  | 9.0e−15 | 0 | 1968 |
| 11 | 12 | 2 | 2 | 4 | 8 | **16** | 1.6e−14 | 0 | 1438 |
| 11 | 16 | 4 | 3 | 4 | 3 | **14** | 1.7e−14 | 0 | 2027 |
| 12 | 12 | 2 | 1 | 3 | 6 | **12** | 9.0e−15 | 0 | 476 |
| 12 | 16 | 0 | 4 | 2 | 4 | **10** | 1.2e−14 | 0 | 975 |
| 12 | 20 | 1 | 2 | 2 | 4 | **9**  | 1.2e−14 | 0 | 1123 |
| 15 | 12 | 3 | 7 | 3 | 7 | **20** | 2.8e−14 | 0 | 2704 |

Every winding integral landed on an integer to `≤ 2.8e−14`, and **no half-turn guard fired in any
run** (window 1 had seven). The contour arithmetic is clean; the instability below is `N`-truncation,
not contour error. `min |det|` on the contours ranged `2.8e−2 … 4.5e−1`, i.e. no zero sat on a
contour.

For reference, window 1 (`Im ∈ [2,12]`, `N = 12`, same `q`): deep = `6, 7, 6, 6, 7`.

---

## 4. `N`-stability — the decisive finding

| `q` | deep at `N=12` | `N=16` | `N=20` | converged? |
|----|----|----|----|----|
| 7  | 8  | 7  | 3 | **no** — still falling, and the largest fall is the *last* step |
| 9  | 17 | 14 | 8 | **no** — the pre-registered escalation trigger; `N=20` still moves |
| 11 | 16 | 14 | SKIPPED-BUDGET | **no** |
| 12 | 12 | 10 | 9 | **no** (window 1 `q=12` was also unconverged) |
| 15 | 20 | SKIPPED-BUDGET | SKIPPED-BUDGET | unknown |

- `q = 9` at `N=12` (17) vs `N=16` (14) **disagreed**, so per the pre-registered clause `N` was
  escalated to 20: the count fell again, to 8. Two escalations, still no convergence.
- In window 1, `q = 5, 7, 9` were **stratum-by-stratum identical** at `N = 12` and `N = 16`. In
  window 2 not one `q` reproduces its count across two `N`. This is the concrete, measured
  confirmation of the pre-registered worry that **higher `Im` needs larger `N`**: the Mayer
  determinant converges worse as the imaginary part grows.
- Drift is **downward everywhere** (as in window 1), so every window-2 number is an **upper
  bound** on the true count. That direction is the safe one for a Route-B upper bound — but the
  bounds are still moving by factors of ~2, so they constrain nothing yet.

**Consequence:** the `N = 12` window-2 row is *not* the analogue of the window-1 `N = 12` row.
It is the analogue of window 1's `N = 8` row — the cautionary, under-resolved series that would
have killed Route B on an artifact. Quoting the window-2 `N = 12` counts as evidence about
`t₀`-uniformity would repeat exactly the mistake window 1 documented.

---

## 5. Fits (least squares in `log q`, deep count)

| series | fit | `R²` |
|---|---|---|
| window 2, `N = 12`, `q = 7,9,11,12,15` | `−13.05 + 11.78·log q` | 0.534 |
| window 2, `N = 16`, `q = 7,9,11,12` | `−5.27 + 7.32·log q` | 0.266 |
| window 2, `N = 20`, `q = 7,9,12` | `−17.52 + 10.95·log q` | 0.844 |
| **window 1**, `N = 12`, same `q = 7,9,11,12,15` | **`4.92 + 0.63·log q`** | **0.111** |

The contrast is the whole result. Window 1's deep slope on this `q` set is `+0.63` on counts of
size `6–7` (≈ 10 % of the level, `R² = 0.11` — noise). Window 2's slope is `+7` to `+12` on counts
of size `3–20`, i.e. of the same order as the counts themselves, at every `N` tested. If the
window-2 counts were `N`-converged this would read **UNDERMINED** without hesitation. They are
not, so it reads `INCONCLUSIVE` — but there is **no** `N` at which window 2 looks flat.

A three-point `N=20` fit is weak evidence in isolation (`q = 7, 9, 12` → `3, 8, 9`); note that its
slope survives the refinement that halved the counts, i.e. `N`-refinement removed *level*, not
*trend*.

---

## 6. Deep density per unit height, window 2 vs window 1

Window 1 candidate constant: deep count per unit height `≈ 0.6–0.7` (headline `~0.65`), giving the
Route-B B5(iii) input `#{Re s ≤ ½−δ₀, |Im s − t₀| ≤ 1} ≲ 1.4`, `q`-independent.

Window 2, height 10, deep count `/ 10`:

| `q` | `N=12` | `N=16` | `N=20` | window 1 (`N=12`) |
|----|----|----|----|----|
| 7  | 0.8 | 0.7 | **0.3** | 0.6 |
| 9  | 1.7 | 1.4 | **0.8** | 0.7 |
| 11 | 1.6 | 1.4 | — | 0.6 |
| 12 | 1.2 | 1.0 | **0.9** | 0.6 |
| 15 | 2.0 | — | — | 0.7 |

- Best-resolved window-2 densities (`N = 20`): `0.3, 0.8, 0.9` for `q = 7, 9, 12` — **overlapping
  window 1's `~0.65` in magnitude but spread by a factor of 3 across `q`**, where window 1 was
  spread by a factor of `7/6`.
- So the *level* of the window-1 constant is not contradicted at height 12–22 (no Weyl-type
  density explosion appears over one decade), but its **`q`-uniformity** — the property Route B
  actually consumes — does not reproduce.
- Reading these as upper bounds (drift is downward), the honest window-2 statement is
  `density ≤ 0.9` at `N = 20` for `q ≤ 12`, with the `q`-trend unresolved.

---

## 7. Verdict

> ### **INCONCLUSIVE** (pre-registered branch: "counts are not `N`-stable").
> Window 2 does **not** support Route-B `t₀`-uniformity. No `q` converged in `N`, so no window-2
> count can be quoted as a measurement; and at every `N` tested the deep count carries a
> `log q` slope one to two orders of magnitude larger, relative to the count, than window 1's.
> The `t₀`-uniformity gap in `LAW_ROUTEB_CONDITIONAL_THEOREM.md` §gaps remains **open, and is now
> known to be non-trivial** — the flatness at `t₀ ≈ 7` is not visibly a generic feature of the
> spectrum, and the numerics needed to decide it at `t₀ ≈ 17` are beyond `N = 20`.

What is genuinely established:

1. **The window-1 flatness has not been reproduced anywhere else.** It is, as of now, a
   one-window observation. Any Route-B write-up quoting `C(δ₀) ≈ 1.4` must say so.
2. **`N`-convergence degrades sharply with height.** Window 1 converged at `N ≥ 12` for small `q`;
   window 2 has not converged by `N = 20` for any `q`. This is a hard cost fact for the lane: a
   `t₀`-uniform measurement needs `N ≳ 24–32` and is an overnight-to-multi-day job, not a 2.5 h one.
3. **Density level is not exploding with height.** Best-`N` window-2 densities (`0.3–0.9`) sit
   in the same range as window 1's `0.65`, so the pre-registered Weyl-growth escape hatch is
   *not* what is happening — the discrepancy is in the `q`-dependence, not in the overall level.

---

## 8. Caveats and budget honesty

1. **Not certified** (see §2 rigor label). Same status as window 1.
2. **No `q` is `N`-converged.** This is the primary defect and the reason for the verdict.
3. **SKIPPED-BUDGET:** `q = 15` at `N = 16` and `N = 20`; `q = 11` at `N = 20`; `q = 15, 11` deeper
   refinements. Total wall used ≈ 3 h across 12 runs (7 concurrent at peak on a 12-performance-core
   machine), slightly over the ~2.5 h budget because the pre-registered `N`-escalation clause fired
   and was honoured. The `N = 20` series is therefore only 3 points (`q = 7, 9, 12`).
4. **No shallow stratum measured.** Grid `deep` was specified, so window 2 cannot reproduce
   window 1's "all growth sits in the shallow box" statement — only the deep side is tested.
   If the window-2 deep growth is real, that statement fails in window 2 by construction.
5. **Only two windows.** `[2,12]` and `[12,22]`. A third window (say `[22,32]`) would say whether
   window 1 or window 2 is the outlier, but at a cost that scales the wrong way (higher `Im`,
   larger `N`).
6. **`q = 15, N = 12` (deep = 20) is the least trustworthy row** — largest residual (`2.8e−14`),
   single `N`, and the largest count in the table. It contributes to the `N = 12` slope; dropping
   it leaves that slope at the same order.

---

## 9. Recommended next steps

1. **Do not promote `C(0.1) ≈ 1.4` to a `t₀`-uniform constant.** Amend
   `LAW_ROUTEB_CONDITIONAL_THEOREM.md` §gaps to record that the one probe of `t₀`-uniformity came
   back INCONCLUSIVE with an adverse trend. (Not done here — no existing file was modified.)
2. **`q = 7, 9, 12` at `N = 24` and `N = 32` in window 2.** `q = 7` is cheapest and is the row that
   moved most (`8 → 7 → 3`); if it stabilises near `6–7` the window-1 picture survives, if it
   stabilises near `2–3` the deep count is height-dependent and B5 needs restating.
3. **A cheaper proxy.** The full-window winding is quadratic-ish in cost with height; a
   `|Im s − t₀| ≤ 1` box at `t₀ = 17` (height 2, as B5 is actually stated) is ~5× cheaper per `q`
   and is the object B5 literally bounds. This lane measured height-10 windows only because
   window 1 did.

---

## 10. Artifacts

- Probe (new): `law_probes/routeb4_window2.py` (2-line code diff vs `routeb2_substratum.py`, §2)
- Receipts (new): `law_probes/routeb4_window2_q{7,9,11,12,15}_N{12,16,20}_deep.json` — 12 files
- Logs (new): `law_probes/routeb4_q{7,9,11,12,15}_N{12,16,20}_deep.log`

Each JSON carries the per-sign edge data (`dV`, `H1`, `H2`), raw non-integer windings, residuals,
guard warnings, `min |det|` on the contours with its location, det-call count, window, and the
rigor label — so every integer in §3 is re-derivable without rerunning.

Existing files were not modified. No git commands were run.
