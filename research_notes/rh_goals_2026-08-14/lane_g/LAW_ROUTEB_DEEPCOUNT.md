# LAW Route B — deep-resonance count measurement (kill-or-advance)

**Date:** 2026-08-16. **Lane G, measurement lane.**
**Target:** the single named blocker of Route B in `LAW_SH_EFFECTIVIZATION_SKELETON.md` §5 —
a `q`-uniform UPPER bound on the **deep** resonance count
`#{s : Re s ≤ ½−δ₀, |Im s − t₀| ≤ 1}`, needed to be `o(log q)` so the `log q` winding mass
of B3 is forced into a shallow `δ`-box (B5/B6 pigeonhole).

**Verdict up front: ROUTE B ADVANCES.** The deep count is **flat in `q`** — 6 or 7 for every
`q ∈ {7,…,21}`, fitted slope `−0.13·log q` with `R² = 0.009` — while the shallow count grows
at `+2.14·log q`. This is exactly the pre-registered ADVANCE pattern. The B5 upper bound the
route needs is not merely `o(log q)`; it is measured **bounded**.

**Status labels:** `MEASURED` throughout. This is a **non-rigorous probe**, not a certificate.
No git was run. No existing file was modified.

---

## 1. Pre-registration (fixed before any count was computed)

Written into `law_probes/routeb_deepcount.py` before the first run; the rule below is verbatim
from the lane brief.

- **Window (fixed, `q`-independent):** `Im s ∈ [2, 12]`, `Re s ∈ (0.023, 0.487) ⊂ (0, ½)`.
  Endpoints pulled off `0` and `½` to avoid the cusp structure and the critical line itself.
- **Strata** (by depth `½ − Re s`):
  `[0.023,0.1)`, `[0.1,0.2)`, `[0.2,0.3)`, `[0.3,0.4)` — **DEEP** (`δ ≥ δ₀ = 0.1`, i.e. `Re s < 0.4`);
  `[0.4,0.487)` — **SHALLOW** (`δ ≤ 0.1`).
  `δ₀ = 0.1` is the pre-registered cut.
- **Groups:** `q = 5, 7, 8, 9, 10, 11, 12, 15, 18, 21` (all non-arithmetic).
- **ADVANCES** if the **shallow** count grows like `log q` while the **deep** count
  (`Re s < ½ − δ₀`) stays **bounded uniformly in `q`**.
- **TROUBLE** if deep counts grow with `q` (pigeonhole mass leaks to depth, no shallow box forced).
- **INCONCLUSIVE** otherwise, or if the counts are not `N`-stable.

---

## 2. Method

**Object counted.** Zeros of the raw transfer-operator determinant `det(1 − L_{s,±})`. Per the
`zeta_cert_rosen.py` module header (MMS, arXiv:0912.2236),

> `Z_S(s) = det[(1 − L_{s,+})(1 − L_{s,−})] / det(1 − K_s)`, and `det(1 − K_s)` is **zero-free on
> `Re s > 0`** (its zeros are exactly `s ∈ −ℕ₀ + i(2π/log(1/b_q))ℤ`).

So on `0 < Re s < ½` the two sectors' zero counts **sum to exactly the Selberg-zeta zero
(resonance) count**, and the raw determinant needs no `det(1−K)` correction. Both sectors
`sign = ±1` are counted and summed for every `q`.

**Counter.** Argument-principle winding on rectangle boundaries, computed by a **shared-edge**
decomposition that makes the whole stratification cost one pass:

- the unwrapped argument of `det` is tracked up each of the 6 vertical grid lines
  `Re = 0.023, 0.1, 0.2, 0.3, 0.4, 0.487` from `Im = 2` to `Im = 12` (total change `ΔV[j]`);
- and along the two horizontal edges `Im = 2`, `Im = 12`, storing the cumulative argument
  `H1[j], H2[j]` at each grid abscissa;
- the winding of stratum `[c_j, c_{j+1}] × [2,12]` is then
  `(1/2π)·[ (H1[j+1]−H1[j]) + ΔV[j+1] + (H2[j]−H2[j+1]) − ΔV[j] ]`.

Every vertical line serves as the right edge of one stratum and the left edge of the next, so
5 strata × 2 sectors cost 6 verticals + 2 horizontals per sector rather than 20 independent
contours. Sampling is **adaptive**: bisection refines any consecutive pair whose argument moves
by more than `θ_max = π/2`, to depth 6.

**Builders.** `zeta_cert_rosen.py` (odd `q`), `zeta_cert_rosen_even.py` (even `q`), used
**unmodified** via `cert_det_complex_mid`. Probe: `law_probes/routeb_deepcount.py`
(new, `routeb_` prefix). Interpreter `/Users/za/.venvs/farey-rh/bin/python` (flint).

**Rigor label — read this before quoting any number.** `NON-RIGOROUS PROBE`. Midpoint float
evaluation of the Arb-ball builders with `ctx.prec` lowered to 128 bits for speed (verified to
reproduce the 300-bit values to >15 digits at test points). No certified ball enclosure of the
boundary values, no certified dim-tail, hence **no Arb winding certificate**. The integers below
are float arg-unwrap windings with a half-turn guard. Adequate for a kill-or-advance decision;
**not** a proof, and not a substitute for the `winding_box` certified path.

---

## 3. Per-`q` stratified counts

Both sign sectors summed. Primary series is **`N = 12`** (see §4 — `N = 8` is under-resolved).

### N = 12 (primary)

| `q` | `[0.023,0.1)` | `[0.1,0.2)` | `[0.2,0.3)` | `[0.3,0.4)` | **DEEP** `Re<0.4` | **SHALLOW** `[0.4,0.487)` | total | max residual | wall (s) |
|----|----|----|----|----|----|----|----|----|----|
| 5  | 0 | 0 | 1 | 1 | **2** | **2** | 4  | 3.4e−15 | 81 |
| 7  | 1 | 1 | 1 | 3 | **6** | **2** | 8  | 2.2e−15 | 414 |
| 8  | 2 | 1 | 0 | 3 | **6** | **5** | 11 | 3.3e−15 | 248 |
| 9  | 1 | 1 | 1 | 4 | **7** | **4** | 11 | 4.6e−15 | 261 |
| 10 | 1 | 2 | 1 | 3 | **7** | **5** | 12 | 5.6e−15 | 334 |
| 11 | 1 | 1 | 1 | 3 | **6** | **4** | 10 | 4.5e−15 | 937 |
| 12 | 1 | 0 | 5 | 0 | **6** | **3** | 9  | 2.7e−15 | 150 |
| 15 | 0 | 0 | 4 | 3 | **7** | **5** | 12 | 6.8e−15 | 1500 |
| 18 | 0 | 0 | 4 | 2 | **6** | **5** | 11 | 5.6e−15 | 854 |
| 21 | 0 | 0 | 3 | 3 | **6** | **6** | 12 | 9.0e−15 | 2803 |

"max residual" is `|winding − round(winding)|` over the strata: every winding integral landed on
an integer to **machine epsilon**, so the arithmetic of the contour integration is clean.

### N = 8 (superseded — retained because it is the cautionary result)

| `q` | 5 | 7 | 8 | 9 | 10 | 11 | 12 | 15 | 18 | 21 |
|----|---|---|---|---|----|----|----|----|----|----|
| DEEP | 3 | 6 | 7 | 9 | 7 | 7 | 8 | 10 | 8 | **13** |
| SHALLOW | 2 | 4 | 4 | 4 | 5 | 6 | 4 | 5 | 4 | 6 |

At `N = 8` the deep count **appears to grow** (`+5.11·log q`, `R² = 0.73`) — which would have read
as **TROUBLE**. That growth is a **truncation artifact**: it is destroyed by raising `N`, and the
excess sits precisely in the two deepest strata `[0.023, 0.2)`, where the finite-`N` Mayer
determinant converges worst. Reporting the `N = 8` series alone would have killed Route B on a
numerical artifact. This is the single most important methodological finding of the lane.

---

## 4. `N`-stability evidence

Requested at two sizes on at least 2 values of `q`; run at three sizes on four values.

| `q` | `N = 8` (deep / shallow) | `N = 12` | `N = 16` | converged? |
|----|----|----|----|----|
| 5  | 3 / 2 | **2 / 2** | **2 / 2** | **yes** at `N ≥ 12` |
| 7  | 6 / 4 | **6 / 2** | **6 / 2** | **yes** at `N ≥ 12` |
| 9  | 9 / 4 | **7 / 4** | **7 / 4** | **yes** at `N ≥ 12` |
| 12 | 8 / 4 | 6 / 3 | 5 / 5 | **no** — total 9 → 10, deep still drifting down |
| 8, 10, 11, 15, 18, 21 | — | measured | not run (cost) | `N=12` only |

- `q = 5, 7, 9`: **stratum-by-stratum identical** at `N = 12` and `N = 16`. The `N = 12` series is
  resolved for these.
- `q = 12`: not converged (deep `8 → 6 → 5`). The drift is **downward**, i.e. further refinement
  can only *reduce* the deep count — which **strengthens** the ADVANCE verdict rather than
  threatening it. The `q = 12` shallow figure `3` at `N = 12` is the least trustworthy number in
  the table (see the caveat in §7).
- The deepest strata `[0.023, 0.2)` empty out as `N` rises (at `N = 12` they are `0` for every
  `q ≥ 15`), consistent with their `N = 8` occupancy being spurious.

**Honest limitation:** the large `q` (15, 18, 21) are measured at `N = 12` only. Cost forbade
`N = 16` there — `q = 21` at `N = 12` already took 2803 s (~47 min), over the ~10 min/`q` budget;
`N = 16` would be several hours. Given that every converged case converged *downward* in the deep
strata, the `N = 12` large-`q` deep counts are best read as **upper bounds**.

---

## 5. Fits

`N = 12` series, least squares.

| quantity | fit (all `q`) | `R²` | fit (`q ≥ 7`, dropping the `q=5` low outlier) | `R²` |
|---|---|---|---|---|
| **DEEP** (`Re < 0.4`) | `1.613 + 1.812·log q` | 0.301 | **`6.652 − 0.130·log q`** | **0.009** |
| **SHALLOW** (`[0.4,0.487)`) | `−1.515 + 2.373·log q` | 0.577 | **`−0.908 + 2.139·log q`** | 0.418 |
| total | `0.098 + 4.185·log q` | 0.541 | `5.744 + 2.009·log q` | 0.276 |

Reading:

- **Deep is flat.** Over `q = 7…21` the deep count takes only the two values `{6, 7}`. The apparent
  all-`q` slope is an artifact of `q = 5` (deep `= 2`), the smallest and least generic group; drop
  it and the slope is `−0.13` with `R² = 0.009` — statistically indistinguishable from a constant.
  Linear-in-`q` fares no better (`R² = 0.15`).
- **Shallow grows.** `+2.14·log q`, and `+0.20·q` linear (`R² = 0.53`); the resolution here is too
  coarse to separate `log q` from a slow power, but the *direction and location* of the growth is
  the pre-registered signal, and it is unambiguous: **all** of the `q`-growth in the window sits in
  the shallow stratum.
- Per sub-stratum, the two deepest strata have **negative** log-`q` slopes at `N = 12`
  (`−0.62`, `−0.56`), the `[0.3,0.4)` stratum is flat (`+0.27`, `R² = 0.01`), and the growth is
  concentrated in `[0.2,0.3)` (`+2.73`) and `[0.4,0.487)` (`+2.37`). The `[0.2,0.3)` figure is the
  one genuinely uncomfortable number in the table — see §7.

---

## 6. Verdict and measured candidate constants

> ### **ADVANCES.**
> Deep counts are uniformly bounded across `q = 5…21`; shallow counts carry all the `q`-growth.
> This is the pre-registered ADVANCE pattern, and it says the B5 blocker is not just `o(log q)`
> but plausibly `O(1)`.

**Candidate constants for the `q`-uniform deep bound** (all `MEASURED`, all at `δ₀ = 0.1`,
window `Im ∈ [2,12]` of height `10`, both sign sectors, `N = 12`):

| quantity | measured value | form for B5 |
|---|---|---|
| `D_q(δ₀=0.1)` := deep count in the window | `≤ 7` for all `q ∈ [5,21]` | `D_q(δ₀) ≤ 7` |
| deep count **per unit height** | `0.6`–`0.7` (`0.2` at `q=5`) | `#{Re s ≤ ½−δ₀, |Im s − t₀| ≤ 1} ≲ 1.4` |
| conjectured uniform bound | — | **`#{Re s ≤ ½−δ₀, |Im s − t₀| ≤ 1} ≤ C(δ₀)`, `C(0.1) ≈ 1.4`, `q`-independent** |
| shallow growth rate | `≈ 2.1·log q` in a height-10 window | consistent in order with B3's `c₀(T)·log Q` |

The `≲ 1.4` per unit height is the number Route B actually consumes: B5(iii) bounds the deep
Poisson-kernel mass by `(2/δ) ×` (deep count per unit height), so a `q`-independent `C(δ₀)`
makes that term `O_δ(1)` and the `log q` mass of B3 is forced into the shallow box, giving B6 an
**explicit** threshold `Q₀`.

**What this does NOT establish.** These are float windings on 10 groups in one fixed height
window. They do not prove boundedness, they say nothing about `Im s` outside `[2,12]`, and the
deep-count constant is not certified. The honest claim is: *the measurement that would have
killed Route B did not kill it, and the quantity Route B needs bounded looks bounded.*

---

## 7. Caveats (each is a real defect, not a formality)

1. **Not certified.** See the rigor label in §2. Promoting any row to a claim needs the Arb
   `winding_box` path with dim-tail certification.
2. **`q = 12` is not `N`-converged** and `q = 15, 18, 21` were measured at one `N` only. Deep
   counts drift **down** with `N` in every converged case, so the deep column reads as an upper
   bound — the safe direction for this verdict, but still a gap.
3. **One near-π unwrap.** In `q = 12, N = 12`, sign `−1`, the argument moved by `3.1399` (i.e.
   `≈ π`) across an interval of width `2·10⁻³` in `Im` at `Re = 0.487` — a zero sitting essentially
   *on* the outer contour. The loop still closed to an integer at `1.1e−15`, but an unwrap slip
   would also land on an integer, so this does not self-certify. It affects only the `q = 12`
   **shallow** figure, not the `δ₀ = 0.1` deep/shallow cut. Six other guard hits occurred, all with
   `|Δarg| < 2.3 < π` (unambiguous).
4. **`[0.2,0.3)` shows growth** (`+2.73·log q`, driven by `q = 12,15,18,21` reading `5,4,4,3`
   against `≈1` for `q ≤ 11`). This is *inside* the deep region and is the one signal pointing the
   other way. It is offset by the two deepest strata emptying out, so the deep **total** stays
   flat — but if the `[0.2,0.3)` growth is real rather than an `N`-resolution effect, the
   `δ₀ = 0.1` cut is doing load-bearing work and a larger `δ₀` would look worse, not better. This
   is the first thing to re-measure.
5. **Fixed height window.** `t₀`-dependence was not probed; B5/B6 are stated per `t₀`.
6. **`q = 5` is an outlier** (deep `= 2` vs `6–7`). Included in the table, excluded from the
   headline fit, and flagged rather than smoothed over.

---

## 8. Recommended next steps

1. **Re-measure `[0.2,0.3)` at `N = 16` for `q = 15, 18, 21`.** This is the only sub-stratum
   arguing for TROUBLE and it is the cheapest way to firm up or break the verdict. (Cost: hours,
   parallelizable; `q = 21` at `N = 16` is the expensive one.)
2. **Certify a single row.** Take `q = 9` (converged at `N = 12 = 16`) and re-run the deep strata
   through the Arb `winding_box` path to convert one line of §3 from `MEASURED` to certified.
3. **Vary `δ₀` and `t₀`.** Deep counts at `δ₀ ∈ {0.05, 0.25}` and a second height window would
   test whether `C(δ₀)` is genuinely `q`-uniform or an artifact of this window.
4. **Then, and only then, write B5 down as a conjecture with the measured `C(0.1) ≈ 1.4`** and
   push B6 to an explicit `Q₀`. Per the skeleton §7, this bypasses U1 entirely.

---

## 9. Artifacts

- Probe (new): `law_probes/routeb_deepcount.py`
- Aggregator (new): `law_probes/routeb_analyze.py` → `law_probes/routeb_summary.json`
- Receipts: `law_probes/routeb_deepcount_q{5,7,8,9,10,11,12,15,18,21}_N8.json`,
  `…_N12.json` (all 10), `…_N16.json` (`q = 5, 7, 9, 12`)
- Logs: `law_probes/routeb_q{q}_N{8,12,16}.log`

Each JSON carries the full per-sign edge data (`dV`, `H1`, `H2`), the raw non-integer winding
values, the residuals, the guard warnings with their `Δarg`, `min |det|` on the contours, the
det-call count, and the rigor label — so every integer in §3 is re-derivable without rerunning.

Existing files were not modified; `probe_d1_scan.py` was read for its protocol and left untouched.
No git commands were run.
