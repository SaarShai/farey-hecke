# LAW Route B — CERTIFIED deep count in the HEIGHT-2 box at `t₀ = 17`

**Date:** 2026-08-16. **Lane G, Route B critical path.**
**Target:** the `t₀`-uniformity gap that `LAW_ROUTEB_WINDOW2.md` left open with an
adverse signal. This note certifies the object **B5 literally bounds** —
`#{resonances : Re s ≤ ½ − δ₀, |Im s − t₀| ≤ 1}` at `t₀ = 17` — instead of a
height-10 decade window.

**Status:** PRE-REGISTRATION SECTION (§1) WRITTEN BEFORE ANY NUMBER WAS COMPUTED.
Results follow in §3 onward.

---

## 1. Pre-registration (fixed before the first run)

- **Box:** `Re s ∈ [0.023, 0.4]`, `Im s ∈ [16, 18]` — i.e. `δ₀ = 0.1`, `t₀ = 17`,
  height 2, exactly the B5(iii) object.
- **Groups / truncation:** `q = 7, 9` at `N = 24`; `q = 12` at `N = 28`
  (window 2 needs deeper `N` than window 1; `LAW_CERTIFIED_DEEPCOUNT_MULTI.md` §3
  found even `q` is the tail-hardest surface).
- **Grade:** CERTIFIED (Arb ball), criteria (a) nonvanishing + (b) certified
  argument increment, conditional on the `dim_tail_from_matrix` device, exactly as
  in `LAW_CERTIFIED_DEEPCOUNT_MULTI.md`. If a winding ball fails to isolate an
  integer, **escalate `N` once more and report the ball width honestly** rather
  than quoting a midpoint.

**Decision rule.**

- **SURVIVES** — B5's `t₀`-uniformity assumption survives at `t₀ = 17` — if the
  certified height-2 deep count is **≤ 3 for all three `q`**.
  (Window-1 density `0.65`/unit ⇒ expected `≈ 1.3` per height-2 box;
  the Route-B constant `C(0.1) · 2 ≈ 2.8`.)
- **ADVERSE-CONFIRMED** if **any `q` reads ≥ 5**, or if the counts grow
  `q`-monotonically.
- **INTERMEDIATE** — report as-is, no verdict word — otherwise (e.g. a `4`
  with no monotone trend, or an unisolated ball).

---

## 2. Method and the exact diff

Driver: `law_probes/certdcH_winding.py` (**new file**, `certdcH_` prefix). It is
`certdcM_winding.py` with **only the window constants, the edge labels, the
receipt name and the env prefix changed**. The certificate logic — criteria (a)
and (b), tail safety factor 4, `n_head = 4`, `PREC_BITS = 300`, adaptive
bisection to depth 10, both sign sectors, parity-selected builder — is
byte-identical. Ball evaluators `zeta_cert_rosen.py` / `zeta_cert_rosen_even.py`
used **unmodified**. Interpreter `/Users/za/.venvs/farey-rh/bin/python`.

The full `diff certdcM_winding.py certdcH_winding.py`:

```
1c1    docstring title: "MULTI-q" -> "HEIGHT-2 BOX"
14,15c14,15  docstring window: "[2, 12]" -> "[16, 18]", t0 = 17
27c27  docstring env line: CERTDCM_* -> CERTDCH_*
41c41  Q = int(os.environ.get("CERTDCH_Q", os.environ.get("CERTDCM_Q", "7")))
46c46  IM_LO, IM_HI = 2.0, 12.0        ->  IM_LO, IM_HI = 16.0, 18.0
47c47  N   env var CERTDCM_N     -> CERTDCH_N
49c49  MAX_DEPTH env var         -> CERTDCH_DEPTH
51,52c51,52  INIT_V / INIT_H env vars  -> CERTDCH_INITV / CERTDCH_INITH
134c134 edge labels "bottom Im=2"/"top Im=12" -> "bottom Im=16"/"top Im=18"
202c202 receipt path certdcM_winding_q{Q}_N{N}.json -> certdcH_...
```

**Sampling density.** `CERTDCH_INITV = 24` samples per vertical edge over height 2
= **12 samples per unit height**, *higher* than the window-1 certificates'
`100 / 10 = 10` per unit. `CERTDCH_INITH = 8` per horizontal edge over the same
`Re`-width as before. So the box is resolved no more coarsely than the certified
window-1 runs, and is cheaper only because the contour is shorter.

---

## 3. Result

> ### **SURVIVES** (pre-registered branch: certified height-2 deep count `≤ 3` at every `q`).
>
> **Certified deep counts, `Re s ∈ [0.023, 0.4]`, `Im s ∈ [16, 18]` (`t₀ = 17`,
> `δ₀ = 0.1`), both sign sectors summed:**
>
> | `q` | headline `N` | certified count | per unit height | `≤ 3`? |
> |---|---|---|---|---|
> | 7  | 24 | **1** | 0.5 | yes |
> | 9  | 24 | **2** | 1.0 | yes |
> | 12 | 32 | **0** | 0.0 | yes |
>
> Every ball isolated an integer strictly. The counts are **non-monotone in `q`**,
> and the **largest `q` gives the smallest count** — the opposite of the
> `log q` growth the float window-2 probe showed.

Pre-registered expectation was `≈ 1.3` per height-2 box from the window-1 density
`0.65`/unit, and the Route-B budget `C(0.1)·2 ≈ 2.8`. Observed: `1, 2, 0`, mean
`1.0`. **The measurement lands on the pre-registered expectation and inside the
Route-B budget at all three `q`.**

### 3.1 Winding balls

| `q` | `N` | sector | winding ball | midpoint | certified integer | isolation margin (turns) |
|---|---|---|---|---|---|---|
| 7  | 24 | `+1` | `[0.98843994, 1.01152984]` | `0.99998489` | **1** | `0.488` |
| 7  | 24 | `−1` | `[−0.00388427, +0.00388387]` | `−1.99e−7` | **0** | `0.496` |
| 9  | 24 | `+1` | `[1.96752804, 2.03277795]` | `2.00015299` | **2** | `0.467` |
| 9  | 24 | `−1` | `[−0.01213401, +0.01210372]` | `−1.51e−5` | **0** | `0.488` |
| 12 | 32 | `+1` | `[−0.25345230, +0.25608612]` | `+1.3e−3` | **0** | `0.244` |
| 12 | 32 | `−1` | `[−0.12383417, +0.12221959]` | `−8.1e−4` | **0** | `0.376` |

`certified_deep_count` in the receipt equals the sector sum: `1`, `2`, `0`.

### 3.2 Per-edge certified argument variation

`q = 7`, `N = 24` (wall 269 s, 144 determinant-ball evaluations):

| sector | edge | init samples | certified segments | bisections | max depth | `Δarg` ball (rad) | (a) | (b) | wall |
|---|---|---|---|---|---|---|---|---|---|
| `+1` | bottom `Im=16`  | 9  | 8  | 0  | 0 | `[+1.359378, +1.362177]` | PASS | PASS | 18 s |
| `+1` | right `Re=0.4`  | 25 | 35 | 11 | 4 | `[−24.826796, −24.798280]` | PASS | PASS | 70 s |
| `+1` | top `Im=18`     | 9  | 8  | 0  | 0 | `[−0.695599, −0.656297]` | PASS | PASS | 16 s |
| `+1` | left `Re=0.023` | 25 | 24 | 0  | 0 | `[+30.373569, +30.448030]` | PASS | PASS | 46 s |
| `−1` | bottom `Im=16`  | 9  | 8  | 0  | 0 | `[−1.045344, −1.043844]` | PASS | PASS | 16 s |
| `−1` | right `Re=0.4`  | 25 | 27 | 3  | 1 | `[−26.963739, −26.954646]` | PASS | PASS | 47 s |
| `−1` | top `Im=18`     | 9  | 8  | 0  | 0 | `[+0.559068, +0.571287]` | PASS | PASS | 14 s |
| `−1` | left `Re=0.023` | 25 | 24 | 0  | 0 | `[+27.425609, +27.451606]` | PASS | PASS | 42 s |

`q = 9`, `N = 24` (wall 500 s, 148 evaluations):

| sector | edge | init | segs | bisect | depth | `Δarg` ball (rad) | (a) | (b) | wall |
|---|---|---|---|---|---|---|---|---|---|
| `+1` | bottom `Im=16`  | 9  | 8  | 0  | 0 | `[+1.740820, +1.743625]` | PASS | PASS | 35 s |
| `+1` | right `Re=0.4`  | 25 | 26 | 2  | 1 | `[−25.665337, −25.635675]` | PASS | PASS | 101 s |
| `+1` | top `Im=18`     | 9  | 8  | 0  | 0 | `[−0.055295, −0.044810]` | PASS | PASS | 28 s |
| `+1` | left `Re=0.023` | 25 | 34 | 10 | 1 | `[+36.342155, +36.709181]` | PASS | PASS | 115 s |
| `−1` | bottom `Im=16`  | 9  | 8  | 0  | 0 | `[+0.831754, +0.832759]` | PASS | PASS | 28 s |
| `−1` | right `Re=0.4`  | 25 | 30 | 6  | 1 | `[−31.493456, −31.471207]` | PASS | PASS | 93 s |
| `−1` | top `Im=18`     | 9  | 8  | 0  | 0 | `[−0.398034, −0.383428]` | PASS | PASS | 25 s |
| `−1` | left `Re=0.023` | 25 | 24 | 0  | 0 | `[+30.983496, +31.097926]` | PASS | PASS | 75 s |

`q = 12`, `N = 32` (wall 658 s, 162 evaluations; even-`q` builder):

| sector | edge | init | segs | bisect | depth | `Δarg` ball (rad) | (a) | (b) | wall |
|---|---|---|---|---|---|---|---|---|---|
| `+1` | bottom `Im=16`  | 9  | 8  | 0  | 0 | `[+0.421015, +0.444556]` | PASS | PASS | 44 s |
| `+1` | right `Re=0.4`  | 25 | 34 | 10 | 2 | `[−34.395051, −32.872196]` | PASS | PASS | 157 s |
| `+1` | top `Im=18`     | 9  | 8  | 0  | 0 | `[−0.896248, −0.646556]` | PASS | PASS | 30 s |
| `+1` | left `Re=0.023` | 25 | 32 | 8  | 1 | `[+33.277796, +34.683232]` | PASS | PASS | 123 s |
| `−1` | bottom `Im=16`  | 9  | 8  | 0  | 0 | `[−0.612191, −0.607908]` | PASS | PASS | 35 s |
| `−1` | right `Re=0.4`  | 25 | 33 | 9  | 1 | `[−34.211983, −33.621191]` | PASS | PASS | 127 s |
| `−1` | top `Im=18`     | 9  | 8  | 0  | 0 | `[+0.504274, +0.593256]` | PASS | PASS | 31 s |
| `−1` | left `Re=0.023` | 25 | 29 | 5  | 1 | `[+33.541827, +34.403772]` | PASS | PASS | 111 s |

**Criteria (a) and (b) passed at every sample and every segment of all three
headline runs.** No point needed the driver's internal `N → N+4 → N+8`
escalation. Contour health:

| `q` | `N` | min certified `\|det\|` lower bound (`+1` / `−1`) | max dim-tail (`+1` / `−1`) | tail location |
|---|---|---|---|---|
| 7  | 24 | `0.0473` / `0.8391` | `0.246` / `0.260` | `(0.023, 17.75)` / `(0.023, 18)` |
| 9  | 24 | `0.6839` / `1.4593` | `0.525` / `0.668` | `(0.023, 17.17)` / `(0.023, 18)` |
| 12 | 32 | `0.6057` / `1.4449` | `13.06` / `8.89` | `(0.023, 18)` (both) |

No zero sits on any contour, so all six counts are unambiguous for the **open**
rectangle `Re s ∈ (0.023, 0.4)`, `Im s ∈ (16, 18)`.

### 3.3 The `N`-escalation clause fired once, as pre-registered

`q = 12` at the pre-registered `N = 28` **aborted**: criterion (b) failed at
maximum bisection depth on the right edge, between `Im = 17.28125` and
`Im = 17.2813314` (segment length `8e−5`).

The cause was diagnosed before escalating, and it is **not** a zero on the
contour. Direct ball evaluation at that point, `q = 12`, sector `+1`:

| `N` | `det` midpoint | `\|det\|` lower | dim tail |
|---|---|---|---|
| 28 | `−1.4504 − 1.5025 i` | `2.088` | `1.55e−1` |
| 32 | `−1.4051 − 1.4327 i` | `2.007` | `4.19e−3` |
| 36 | `−1.4061 − 1.4351 i` | `2.009` | `9.34e−5` |

`|det| ≈ 2.0` and stable; the tail alone, inflated by the safety factor 4, was
`0.62` — a third of the determinant modulus — so the pair product `w` straddled
the imaginary axis. `N = 32` shrinks the tail by `37×` and the run completed
cleanly. Per the pre-registration this is a single escalation with the width
reported, not a silent midpoint quote.

**Practical truncation finding (extends `LAW_CERTIFIED_DEEPCOUNT_MULTI.md` §3).**
At `Im ≈ 7` the robust truncations were `N = 20` (odd) and `N = 24` (even). At
`Im ≈ 17` they are **`N = 24` (odd `q = 7, 9`) and `N = 32` (even `q = 12`)`**.

### 3.4 Failed lower-`N` cross-checks — reported, not hidden

Two independent `N = 20` runs were attempted at the height-2 box:

| run | outcome | detail |
|---|---|---|
| `q = 7`, `N = 20` | **NOT CERTIFIED** | sector `−1` pins `0` (ball `[−0.4188, +0.4127]`); sector `+1` ball is `[−0.5995, +2.5911]` — width `3.19` turns, contains `0, 1, 2`. Max dim tail `23.3`. |
| `q = 9`, `N = 20` | **ABORTED** | criterion (b) unmet at max depth on the left edge near `(0.023, 17.526)`; tail-driven, same mechanism as `q = 12` at `N = 28`. |

Neither contradicts the headline: a `N = 20` ball is a *valid but too wide*
enclosure of the same integer (`1 ∈ [−0.5995, 2.5911]`). They are recorded
because they are the honest cost statement — **`N = 20`, the truncation that
carried the entire window-2 float table, cannot certify anything at `t₀ = 17`.**

---

## 4. Comparison with the float window-2 numbers

**The float receipts do not contain per-zero positions.** Each
`routeb4_window2_q*_N*_deep.json` stores per-sign vertical-edge argument
variations `dV`, the two horizontal-edge variations `H1`/`H2`, and `cells` keyed
**only by `Re`-stratum** (`re_lo`, `re_hi`, `winding_raw`, `count`), each an
argument-principle count over the **whole** `Im ∈ [12,22]` window. There is no
`Im`-resolution inside the window and no zero-localization list. **A float count
restricted to `Im ∈ [16,18]` therefore cannot be recomputed from the existing
receipts** — it would require a fresh run of `routeb4_window2.py` on the
sub-window. That was not done (budget went to the certificates).

What can be compared is the **density**:

| `q` | float window-2 `N=20` deep count, `Im ∈ [12,22]` | implied density /unit | **certified height-2 count** `Im ∈ [16,18]` | certified density /unit |
|---|---|---|---|---|
| 7  | 3 (upper bound, unconverged) | 0.3 | **1** | **0.5** |
| 9  | 8 (upper bound, unconverged) | 0.8 | **2** | **1.0** |
| 12 | 9 (upper bound, unconverged) | 0.9 | **0** | **0.0** |

Two things follow.

1. **The float `N = 20` values were still too large**, as `LAW_ROUTEB_WINDOW2.md`
   §4 predicted (drift is downward, so those are upper bounds). The certified box
   at `q = 12` reads `0` where the float density predicted `≈ 1.8` zeros in that
   box.
2. **The `q`-trend reverses under certification.** The float `N = 20` triple
   `(3, 8, 9)` for `q = (7, 9, 12)` is monotone increasing — the adverse signal.
   The certified triple `(1, 2, 0)` is not monotone, and its largest `q` is its
   smallest count. A `log q` least-squares slope on the certified triple is
   **`−1.98`** (`R² = 0.28`) — negative, and small enough on counts of this size
   to be indistinguishable from flat — against `+10.95`
   at `R² = 0.84` for the float `N = 20` decade series.

**Diagnosis of the window-2 adverse signal: it is a truncation artifact.** The
`log q` slope tracked how badly each surface was under-resolved at `N = 20`
(`q = 12` was the worst, and it carried the largest count), not a real growth in
deep resonances. This is the same failure mode `LAW_ROUTEB_WINDOW2.md` §4 warned
about ("the analogue of window 1's `N = 8` row") — now demonstrated rather than
suspected.

---

## 5. Verdict and implications

> ### **SURVIVES.** B5's `t₀`-uniformity assumption is **not** contradicted at `t₀ = 17`.
> Certified deep counts in the height-2 box are `1, 2, 0` for `q = 7, 9, 12` —
> all `≤ 3`, all inside the Route-B budget `C(0.1)·2 ≈ 2.8`, non-monotone in `q`,
> at certificate grade.

**For the `t₀`-uniformity gap.**

1. The window-2 `INCONCLUSIVE`-with-adverse-trend verdict is now **explained**:
   the adverse `log q` slope was truncation, and it disappears when the same
   `q` set is certified at adequate `N`. `LAW_ROUTEB_WINDOW2.md` §7 said the
   numbers "constrain nothing yet"; that remains correct, and this note supplies
   numbers that do constrain.
2. The window-1 flatness is **no longer a one-window observation.** It now has a
   second, independent height (`t₀ = 17` versus `t₀ ≈ 7`) at certificate grade,
   on the same three `q`, with the deep density in the same range
   (`0.0–1.0`/unit here, `0.5–0.7`/unit certified in window 1).
3. Recommendation 1 of `LAW_ROUTEB_WINDOW2.md` §9 ("do not promote `C(0.1) ≈ 1.4`
   to a `t₀`-uniform constant") should be **revised, not executed as written**:
   the one probe that came back adverse has been superseded by a certified probe
   of the actual B5 object that came back consistent. `C(0.1) ≈ 1.4` per unit
   height still should not be *asserted* `t₀`-uniform — but the recorded evidence
   against it is now withdrawn.

**For the conditional theorem** (`LAW_ROUTEB_CONDITIONAL_THEOREM.md` §gaps). The
`t₀`-uniformity gap **stays open** — three `q`, two `t₀` values, `q ≤ 12` is not a
uniformity proof. What changes is its status: it was, after window 2, a gap with
*evidence pointing against the assumption*; it is now a gap with *certified
evidence consistent with the assumption at two separated heights*. B5 remains an
assumption; it is no longer a suspected-false assumption.

**Honest counterweight.** The single strongest number here, `q = 12 → 0`, is also
the one that most needs a second look: a count of zero in a height-2 box is
exactly what an over-tight contour or a mis-scoped even-`q` builder would also
produce. The `−1` sector is certified empty at all three `q` here, matching
window 1, which is reassuring; and the `q = 12` `+1` ball `[−0.253, +0.256]`
excludes `±1` with margin `0.24` of a turn, so `0` is pinned rigorously given the
tail device. Caveat 7.4 of `LAW_CERTIFIED_DEEPCOUNT_MULTI.md` (the even-`q`
builder's own validation scope is `q = 8`) is inherited unchanged.

---

## 6. Caveats

1. **Conditional on one device.** `dim_tail_from_matrix` /
   `dim_tail_from_matrix_signed` — the geometric ratio-extrapolation tail bound.
   Every certificate here is exactly as strong as that device, identical to the
   window-1 certified notes.
2. **Even-`q` builder validation scope** is `q = 8` per its own header; the
   `q = 12` certificate inherits that limit (§5 counterweight).
3. **Three `q`, `q ≤ 12`.** `q = 15, 18, 21` — the large-`q` end B5 actually needs
   — are untouched at `t₀ = 17`.
4. **Two heights.** `t₀ ≈ 7` (window 1) and `t₀ = 17`. Two points do not establish
   uniformity in `t₀` any more than three `q` establish uniformity in `q`.
5. **No stratification.** Deep totals only; no `Re`-stratum breakdown inside the
   box.
6. **No float sub-window recomputation** (§4) — the existing receipts lack
   `Im`-resolution, and a fresh float run in `[16,18]` was not budgeted.
7. **`N = 20` cross-checks failed** (§3.4). Each headline count therefore rests on
   **one** `N`, unlike the window-1 certificates which had two agreeing `N`. A
   second agreeing `N` (e.g. `q = 7` at `N = 28`) is the cheapest remaining
   hardening.

---

## 7. Recommended next steps

1. **`q = 7` at `N = 28` and `q = 9` at `N = 28`** in the same box — supplies the
   second agreeing `N` that caveat 7 asks for. ~10 min and ~20 min respectively.
2. **`q = 15` and `q = 21` at `t₀ = 17`**, `N = 24`/`N = 28` — the large-`q` end.
   This is now the single highest-value measurement in the lane: with `q = 21`
   certified at both `t₀`, the flatness claim would span the measured `q` range at
   two heights.
3. **A third `t₀`** (say `t₀ = 27`) in the same cheap height-2 form. The height-2
   box is `~4–5×` cheaper than a decade window per `q`, so `t₀`-scans are now
   affordable in a way the window probes were not — this is the methodological
   payoff of the note.
4. **Fresh float run of `routeb4_window2.py` restricted to `Im ∈ [16,18]`** at
   `N = 20` and `N = 24`, purely to quantify the float/certified gap that §4 could
   only bound indirectly.

---

## 8. Artifacts

- Driver (new): `law_probes/certdcH_winding.py` (§2 diff vs `certdcM_winding.py`)
- Receipts (new): `law_probes/certdcH_winding_q7_N24.json` (headline `q=7`),
  `certdcH_winding_q9_N24.json` (headline `q=9`),
  `certdcH_winding_q12_N32.json` (headline `q=12`),
  `certdcH_winding_q7_N20.json` (failed cross-check, ball not isolated)
- Logs (new): `law_probes/certdcH_q7_N24.log`, `certdcH_q9_N24.log`,
  `certdcH_q12_N32.log`, `certdcH_q12_N28.log` (aborted run, §3.3),
  `certdcH_q7_N20.log`, `certdcH_q9_N20.log` (aborted, §3.4)

Total wall: 269 + 500 + 658 s for the headlines, plus ~700 s of the aborted and
failed cross-check runs = **~36 min**, well inside the 3 h budget (three runs
concurrent).

Each JSON carries per-sector, per-edge `Δarg` **balls**, segment/bisection counts,
max bisection depth, the winding ball and its isolated integer, the minimum
certified `|det|` lower bound on the contour, the maximum dimension-tail radius
with its location, the `N`-escalated point list, and the determinant-call count.

`zeta_cert_rosen.py` and `zeta_cert_rosen_even.py` were used **unmodified**.
No existing file was modified. No git commands were run.
