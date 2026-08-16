# LAW Route B — the decisive step-vs-trend test: `q = 18` and `q = 21` at `N = 16`

**Date:** 2026-08-16. **Lane G, measurement lane. Closes step 1 of
`LAW_ROUTEB_SUBSTRATUM.md` §8 (recommended next steps).**

**Verdict up front: STEP-CONFIRMED.** At `N = 16` the `[0.2,0.3)` occupancy reads
`3` for both `q = 18` and `q = 21` — at or below the `q = 12` maximum of `4`, and
*at or below* their own `N = 12` values (`4` and `3`). The deep total `Re s < 0.4`
is `6` for both, unchanged from `N = 12`. Occupancy does **not** grow with `q`
past the step at `q ≈ 12`; it plateaus. **The deep-bound candidate
`C(0.2) ≈ 1.0` stands unchanged**, and the step sits inside it. **Route B advances
cleanly.**

**Status labels:** `MEASURED`, `NON-RIGOROUS PROBE` (inherited unchanged). No git
was run. No existing file was modified. No existing receipt was overwritten.

---

## 1. Baseline verification — the brief's pre-registered numbers were wrong

The task brief pre-registered the `N = 12` baselines as `q = 18: [0.2,0.3) = 1`
and `q = 21: [0.2,0.3) = 2`. **Both are wrong.** Read directly from the receipts
before any new number was computed:

| receipt | `[0.023,0.1)` | `[0.1,0.2)` | `[0.2,0.3)` | `[0.3,0.4)` | deep `Re<0.4` |
|---|---|---|---|---|---|
| `routeb_deepcount_q18_N12.json` | 0 | 0 | **4** | 2 | **6** |
| `routeb_deepcount_q21_N12.json` | 0 | 0 | **3** | 3 | **6** |

The deep totals `(6, 6)` quoted in the brief are **correct**. The `[0.2,0.3)`
figures `4` and `3` also match `LAW_ROUTEB_SUBSTRATUM.md` §6, whose `Re s < 0.3`
row reads `4` at `q = 18` and `3` at `q = 21` (`= 0 + 0 + 4` and `0 + 0 + 3`).
The brief's `1` and `2` appear in no receipt.

**Consequence for the verdict rule.** The brief's thresholds
(`STEP-CONFIRMED if ≤ 2`, `TREND-TROUBLE if ≥ 4`) were built on those wrong
baselines and are unusable: `q = 18` and `q = 21` already sat at `4` and `3` at
`N = 12`, i.e. already at the post-step (`q ≥ 12`) level, never at the low-`q`
level of `1`. A rule demanding `≤ 2` would have declared TREND-TROUBLE before the
run started.

---

## 2. Re-registered rule (fixed in writing before any `N = 16` number existed)

Recorded at launch; reproduced verbatim in substance.

- **STEP-CONFIRMED (plateau)** — `[0.2,0.3)` at `N = 16` for **both** `q` lands in
  `{3, 4, 5}`, i.e. at or below the `q = 12` maximum and not above its own
  `N = 12` value. Reading: the occupancy is a two-level **step** (low for
  `q ≤ 11`, `≈ 3–4` for `q ≥ 12`) that plateaus; `C(0.2) ≈ 1.0` holds with the
  step inside it; Route B advances.
- **TREND-TROUBLE** — `[0.2,0.3)` at `N = 16` for either `q` reads `≥ 6`, i.e.
  strictly above every value measured at any `q`. Reading: occupancy grows with
  `q` past the step; the deep-bound candidate needs re-examination.
- **`N`-TRUNCATION (third branch, added because every converged cell so far moved
  down with `N`)** — either `q` drops below `3`. Reading: same direction as
  `q = 12`'s `5 → 4`; the upper bound improves.

Deep totals `Re s < 0.4` recorded against the `N = 12` value `6` for both `q`.
The bound-relevant quantity for `C(0.2)` is `Re s < 0.3`.

**Method, unmodified.** `law_probes/routeb2_substratum.py` run as shipped
(`--grid deep`, which reports all four strata under `Re = 0.4` plus the total in
one pass), `--N 16`, window `Im s ∈ [2,12]`, both sign sectors, `PREC = 128`,
`θ_max = π/2`, depth 6, builders `zeta_cert_rosen(.py|_even.py)` untouched,
interpreter `/Users/za/.venvs/farey-rh/bin/python`. Runs were **sequential and
solo** — unlike the parent note's 4-way parallel runs, so the wall times below are
true solo times.

---

## 3. Results

| `q` | `N` | `[0.023,0.1)` | `[0.1,0.2)` | `[0.2,0.3)` | `[0.3,0.4)` | `Re<0.3` | **deep `Re<0.4`** | source |
|----|----|----|----|----|----|----|----|----|
| 18 | 8  | 2 | 1 | 5 | 0 | 8 | 8 | `routeb_deepcount_q18_N8.json` |
| 18 | 12 | 0 | 0 | 4 | 2 | 4 | 6 | `routeb_deepcount_q18_N12.json` |
| 18 | **16** | **0** | **1** | **3** | **2** | **4** | **6** | `routeb2_substratum_q18_N16_deep_routeb3.json` (642 s) |
| 21 | 8  | 3 | 1 | 6 | 3 | 10 | 13 | `routeb_deepcount_q21_N8.json` |
| 21 | 12 | 0 | 0 | 3 | 3 | 3 | 6 | `routeb_deepcount_q21_N12.json` |
| 21 | **16** | **0** | **0** | **3** | **3** | **3** | **6** | `routeb2_substratum_q21_N16_deep_routeb3.json` (4991 s) |

Both cells completed **both** sign sectors — no partial, no budget kill. Wall
times `642 s` (`q = 18`) and `4991 s` (`q = 21`, ≈ 83 min), well inside the 3.5 h
cap.

**Quality of the two new cells.** Zero guard warnings. Every winding landed on an
integer to `≤ 6.8e−15` (`q = 18`) and `≤ 5.8e−15` (`q = 21`). `min |det|` on the
contours `0.0627` and `0.0408` — no near-zero contour crossing. Det calls `971`
and `1002`.

**Sector structure holds.** The `sign = −1` sector returned `[0,0,0,0]` in both
runs — the same observation as every other `N ≥ 16` run in the parent note. All
deep occupancy sits in `sign = +1`.

---

## 4. Verdict against the re-registered rule

> ### STEP-CONFIRMED.
> `q = 18`: `[0.2,0.3)` `4 → 3` from `N = 12` to `N = 16` (moved **down**, into the
> `N`-truncation direction). `q = 21`: `3 → 3`, exactly stable.
> Both land in `{3,4,5}`; neither reaches the TREND-TROUBLE floor of `6`; the
> `q = 12` value `4` remains the maximum over all measured `q`.
>
> ### Deep totals: unchanged at 6 for both `q` (`N = 12 = 16`).

The `[0.2,0.3)` occupancy over all measured `q` now reads

| `q` | 5 | 7 | 9 | 11 | 12 | 15 | 18 | 21 |
|----|---|---|---|----|----|----|----|----|
| `[0.2,0.3)`, best available `N` | 1 | 1 | 1 | 1 | 4 | 4 | **3** | **3** |

— `1` for `q ≤ 11`, then `4, 4, 3, 3` for `q ≥ 12`. This is a **step, not a
growth trend**: the largest two `q` read *below* the mid-`q` cells. A least-squares
`log q` fit still returns a positive slope (`−2.71 + 2.06·log q`, `R² = 0.51`),
but that slope is now an artifact of the step's position and is **not** evidence
of growth — the two new points move it down (`4.47 → 2.06`) rather than extending
it. **Do not quote the slope.** The defensible statement is: *`[0.2,0.3)`
occupancy is `1` for `q ≤ 11` and `3–4` for `q ≥ 12`, and that difference is
`N`-converged.*

This is exactly the outcome the parent note's §8.1 named as "the only remaining way
the step reading could turn into a genuine growth trend, or die." **It died.**

---

## 5. Confirmed deep-bound constant

`δ₀ = 0.2` (deep `≡ Re s < 0.3`), height-10 window `Im s ∈ [2,12]`:

| `q` | 5 | 7 | 8 | 9 | 10 | 11 | 12 | 15 | 18 | 21 |
|----|---|---|---|---|----|----|----|----|----|----|
| count `Re s < 0.3` | 1 | 3 | 3 | 3 | 4 | 3 | **5*** | 4 | **4** | **3** |

`*` `q = 12` at the converged `N = 20`. `q = 18, 21` are the **new `N = 16`**
figures (`0+1+3` and `0+0+3`); `q = 18` is unchanged from `N = 12` and `q = 21` is
unchanged from `N = 12`. `q = 5,7,8,9,10,11,15` remain `N = 12` figures, which every
converged case says are **upper bounds**.

| quantity | measured | form for B5 |
|---|---|---|
| `D_q(δ₀ = 0.2)` in the height-10 window | `≤ 5` for all `q ∈ [5,21]` | `D_q(0.2) ≤ 5` |
| per unit height | `0.1`–`0.5` | `#{Re s ≤ ½−0.2, |Im s − t₀| ≤ 1} ≲ 1.0` |
| **uniform candidate** | — | **`C(0.2) ≈ 1.0` — CONFIRMED, unchanged** |
| previous candidate at `δ₀ = 0.1` | — | `C(0.1) ≈ 1.4`, unchanged |

Fit over all `q` of the `Re < 0.3` count: `−0.19 + 1.48·log q`, `R² = 0.37` — the
maximum sits at `q = 12`, not at the largest `q`, so this is a weak drift with an
interior maximum, not a growth law. The two largest `q` read `4` and `3`, below the
`q = 12` value `5`.

**`C(0.2) ≈ 1.0` is not revised. It is confirmed on the two most expensive cells
in the lane.**

---

## 6. Caveats

1. **Not certified.** Same rigor label as both parent notes: float arg-unwrap
   windings on midpoint evaluations of the Arb-ball builders at 128 bits.
   `MEASURED`, not proved. (Residuals `≤ 7e−15` and zero warnings make a
   mis-rounded winding unlikely, but that is not a certificate.)
2. **`N = 16`, not `N = 20`, for `q = 18, 21`.** `q = 21` cost 83 min solo at
   `N = 16`; `N = 20` was not attempted. Every converged cell in the lane moved
   **down** with `N`, so these are upper bounds — the safe direction for B5.
3. **`q = 8, 10` were never re-measured above `N = 12`** (unchanged from the
   parent note).
4. **The `q = 18` composition moved inside `Re < 0.2`** (`[0.1,0.2)`: `0 → 1`)
   while the `Re < 0.3` total held at `4` — the same "assignment moves, total does
   not" behaviour seen at `q = 12`. The deepest strata remain the least
   trustworthy cells.
5. **Fixed window `Im ∈ [2,12]`.** `t₀`-dependence remains unprobed.
6. **The brief's pre-registered baselines were wrong** (§1). The verdict here is
   against the corrected rule of §2, fixed in writing before any number was
   computed. A reader who wants the brief's literal rule should note that it
   would have read TREND-TROUBLE off the *`N = 12`* data alone, before this work.

---

## 7. Artifacts

Receipts and logs carry a `routeb3` tag. **Filename collision note:** the probe
hard-codes its own `routeb2_substratum_*` naming and only the `--tag` suffix is
settable, so the new JSONs are named `routeb2_substratum_q{18,21}_N16_deep_routeb3.json`
— a `routeb2_` prefix with a `routeb3` tag. No pre-existing file has that name;
nothing was overwritten. The logs use a clean `routeb3_` prefix.

- New receipts: `law_probes/routeb2_substratum_q18_N16_deep_routeb3.json`,
  `law_probes/routeb2_substratum_q21_N16_deep_routeb3.json`
- New logs: `law_probes/routeb3_q18_N16_deep.log`, `law_probes/routeb3_q21_N16_deep.log`
- Reused **unmodified**: `law_probes/routeb2_substratum.py`,
  `law_probes/routeb_deepcount_q{18,21}_N{8,12}.json`, both builders.

Exact commands (run from `law_probes/`):

```
/Users/za/.venvs/farey-rh/bin/python routeb2_substratum.py 18 --N 16 --grid deep --tag routeb3
/Users/za/.venvs/farey-rh/bin/python routeb2_substratum.py 21 --N 16 --grid deep --tag routeb3
```

## 8. Remaining next steps (unchanged from the parent note, minus step 1)

1. Finish `q = 15, N = 20` (`sign = −1` sector alone) to close the one partial cell.
2. `δ₀ = 0.25` / `δ₀ = 0.05` sweep on the `deep` grid, to test monotonicity of `C(δ₀)`.
3. Certify one row (`q = 9`) through the Arb `winding_box` path.
4. `t₀`-dependence: repeat one `q` in a second height window.
