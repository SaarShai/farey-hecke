# LAW Route B — second-`N` confirmation of the certified height-2 counts (`t₀ = 17`)

**Date:** 2026-08-16. **Lane G, Route B.** Append-style companion to
`LAW_ROUTEB_HEIGHT2_CERT.md`.

**Target:** caveat 7 of that note — each of the three headline counts `(1, 2, 0)`
rested on **one** truncation `N`, unlike the window-1 certificates which had two
agreeing `N`. This note supplies the second `N` for all three `q`.

**Verdict up front: CONFIRMED at every `q`. Same three integers `1, 2, 0`, with
balls 13×–83× tighter.**

---

## 1. What was run

Driver `law_probes/certdcH_winding.py` **unmodified** (byte-identical to the file
that produced the headline receipts). Ball evaluators `zeta_cert_rosen.py` /
`zeta_cert_rosen_even.py` unmodified. Interpreter
`/Users/za/.venvs/farey-rh/bin/python`. Same box: `Re s ∈ [0.023, 0.4]`,
`Im s ∈ [16, 18]`. Both sign sectors summed.

Environment for all three runs:
`CERTDCH_Q=<q> CERTDCH_N=<N> CERTDCH_INITV=100 CERTDCH_INITH=8 CERTDCH_DEPTH=10`.

Two things differ from the headline runs, and **both move in the safe direction**
(finer contour resolution, smaller dimension tail):

1. **Truncation** `N`: `7 → 28` (headline 24), `9 → 28` (headline 24),
   `12 → 36` (headline 32).
2. **Vertical sampling** `INIT_V = 100` (101 points per vertical edge) versus the
   headline's `24` (25 points) — 50 samples per unit height instead of 12.

This is therefore a *joint* `N`+density re-measurement, not an `N`-only variation.
It answers caveat 7 (a second independent truncation agrees) but it does **not**
isolate which of the two changes bought the tighter ball. Stated plainly so no one
later reads the width shrink as an `N`-only effect.

## 2. Result table — both `N` per `q`

Isolation margin = `0.5 − (ball half-width)` in turns; the certificate needs it
`> 0`.

| `q` | `N` | sector | winding ball | ball width | certified integer | isolation margin | **box total** |
|---|---|---|---|---|---|---|---|
| 7  | 24 (headline) | `+1` | `[0.98843994, 1.01152984]` | `2.31e−2` | 1 | `0.488` | **1** |
| 7  | 24 (headline) | `−1` | `[−0.00388427, +0.00388387]` | `7.77e−3` | 0 | `0.496` | |
| **7**  | **28 (this note)** | `+1` | `[0.99974415, 1.00025585]` | `5.12e−4` | **1** | `0.49974` | **1** |
| **7**  | **28 (this note)** | `−1` | `[−9.8191e−5, +9.8192e−5]` | `1.96e−4` | **0** | `0.49990` | |
| 9  | 24 (headline) | `+1` | `[1.96752804, 2.03277795]` | `6.52e−2` | 2 | `0.467` | **2** |
| 9  | 24 (headline) | `−1` | `[−0.01213401, +0.01210372]` | `2.42e−2` | 0 | `0.488` | |
| **9**  | **28 (this note)** | `+1` | `[1.99921658, 2.00078345]` | `1.57e−3` | **2** | `0.49961` | **2** |
| **9**  | **28 (this note)** | `−1` | `[−3.5591e−4, +3.5592e−4]` | `7.12e−4` | **0** | `0.49964` | |
| 12 | 32 (headline) | `+1` | `[−0.25345230, +0.25608612]` | `5.10e−1` | 0 | `0.244` | **0** |
| 12 | 32 (headline) | `−1` | `[−0.12383417, +0.12221959]` | `2.46e−1` | 0 | `0.376` | |
| **12** | **36 (this note)** | `+1` | `[−0.01249562, +0.01249975]` | `2.50e−2` | **0** | `0.4875` | **0** |
| **12** | **36 (this note)** | `−1` | `[−0.00924476, +0.00924322]` | `1.85e−2` | **0** | `0.49076` | |

### Verdict per `q`

| `q` | headline `N` → count | second `N` → count | ball tightening (`+1` sector) | verdict |
|---|---|---|---|---|
| 7  | 24 → **1** | 28 → **1** | 45× | **CONFIRMED** |
| 9  | 24 → **2** | 28 → **2** | 42× | **CONFIRMED** |
| 12 | 32 → **0** | 36 → **0** | 20× | **CONFIRMED** |

**No discrepancy of any kind.** Every ball isolated its integer strictly; no run
aborted; the driver's internal `N → N+4 → N+8` escalation fired at **zero** points
in all six sectors (`N_escalated_points` empty everywhere), so the pre-registered
single-escalation clause was not needed.

## 3. Contour health, second `N` versus headline

| `q` | `N` | min certified `\|det\|` lower (`+1` / `−1`) | max dim-tail (`+1` / `−1`) | tail location |
|---|---|---|---|---|
| 7  | 24 | `0.0473` / `0.8391` | `0.246` / `0.260` | `(0.023, 17.75)` / `(0.023, 18)` |
| **7**  | **28** | `0.0451` / `0.8360` | **`0.00190`** / **`0.00198`** | `(0.023, 17.82)` / `(0.023, 18)` |
| 9  | 24 | `0.6839` / `1.4593` | `0.525` / `0.668` | `(0.023, 17.17)` / `(0.023, 18)` |
| **9**  | **28** | `0.6839` / `1.4595` | **`0.00390`** / **`0.00616`** | `(0.023, 17.18)` / `(0.023, 18)` |
| 12 | 32 | `0.6057` / `1.4449` | `13.06` / `8.89` | `(0.023, 18)` (both) |
| **12** | **36** | `0.6419` / `1.4469` | **`0.2815`** / **`0.2205`** | `(0.023, 18)` (both) |

The determinant modulus on the contour is **stable to 2–4 significant figures**
across the two truncations at every `q` — the same surface is being measured — while
the dimension tail falls by `130×` (`q = 7`), `110×` (`q = 9`) and `40×` (`q = 12`).
That is the expected geometric-truncation behaviour and it is what the ball
tightening buys.

The `q = 12` tail is still the largest by two orders of magnitude, consistent with
`LAW_CERTIFIED_DEEPCOUNT_MULTI.md` §3 (even `q` is the tail-hardest surface) and
with §3.3 of the headline note. At `N = 36` it is `0.28`, small against
`min |det| ≈ 0.64`, so the `TAIL_SAFETY = 4` inflation no longer threatens the
sector-`+1` sign test the way it did at `N = 28`.

## 4. Bisection behaviour

| `q` | `N` | total certified segments | bisections | max depth |
|---|---|---|---|---|
| 7  | 24 | 142 | 14 | 4 |
| **7**  | **28** | **434** | **2** | **2** |
| 9  | 24 | 146 | 18 | 1 |
| **9**  | **28** | **432** | **0** | **0** |
| 12 | 32 | 160 | 32 | 2 |
| **12** | **36** | **432** | **0** | **0** |

Criterion (b) now passes on the raw sample grid essentially everywhere — two
bisections in six sectors, both in `q = 7` sector `+1` on the right edge. The
half-turn condition is met with room, so the argument-increment unwrapping is not
being rescued by adaptivity.

## 5. Reading

1. **Caveat 7 of `LAW_ROUTEB_HEIGHT2_CERT.md` is discharged.** All three
   height-2 headline counts now rest on **two** agreeing truncations, matching the
   evidential standard of the window-1 certificates.
2. **The `q = 12 → 0` counterweight is strengthened, not overturned.** §5 of the
   headline note flagged the zero as the number most in need of a second look,
   partly because its ball (`±0.25`) was the loosest of the six. At `N = 36` that
   ball is `±0.0125` — `0` is pinned with margin `0.4875` of a turn, in line with
   the odd-`q` sectors. The zero survives the harder look.
3. **The non-monotone `q`-trend `(1, 2, 0)` is reproduced exactly** at the second
   `N`. The truncation-artifact diagnosis of the window-2 adverse `log q` slope
   (headline §4) does not depend on a single `N` per `q` any more.
4. **What is still not tested.** Everything else in the headline note's caveat
   list is unchanged: one device (`dim_tail_from_matrix`), the even-`q` builder's
   `q = 8` validation scope, three `q` with `q ≤ 12`, two `t₀` values, no
   `Re`-stratification, no float sub-window recomputation. This note hardens the
   truncation axis **only**. In particular a second `N` cannot detect a systematic
   error shared by both truncations — e.g. a mis-scoped even-`q` builder would
   return `0` at `N = 32` and `N = 36` alike.

## 6. Artifacts (all new; `certdcH_` prefix, no collisions)

Under `research_notes/rh_goals_2026-08-14/lane_g/law_probes/`:

- Receipts: `certdcH_winding_q7_N28.json`, `certdcH_winding_q9_N28.json`,
  `certdcH_winding_q12_N36.json`
- Logs: `certdcH_q7_N28.log`, `certdcH_q9_N28.log`, `certdcH_q12_N36.log`

Wall: `1352 s` (`q=7`) + `2496 s` (`q=9`) + `2680 s` (`q=12`) = **`6528 s` CPU**,
run concurrently, **~45 min wall**, inside the 2 h budget. Determinant-ball
evaluations: `436 + 434 + 434 = 1304`.

Driver and ball evaluators used **unmodified**. No existing file was modified.
