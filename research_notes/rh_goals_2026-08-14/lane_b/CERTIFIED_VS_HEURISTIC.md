# Certified vs heuristic: trust boundary of the spectral stack

Audit basis: the current source files under
`/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore`, plus their current
JSON/log outputs and the q=4/q=6 lane report.  The labels below are deliberately
attached to the claim actually emitted, not to a module's top-level docstring.

The decisive distinction is this: exact Hurwitz closure and finite-​matrix Arb
rounding are rigorous arithmetic operations, but the infinite Fredholm
determinant is only controlled here by a finite-window determinant-increment
test.  A claim depending on that test is `[CERTIFIED-MODULO-HEURISTIC]`, not a
pure `[CERTIFIED-INTERVAL]` claim.

## 1. Output-by-output classification

| Claim | Source file/function | Classification | One-line justification |
|---|---|---|---|
| Exact branch-series tail and finite-​N determinant ball | `code/zeta_cert_q3.py:142-167,175-184`; shared Rosen implementation `code/zeta_cert_rosen_q5.py:291-318,400-412` | `[CERTIFIED-INTERVAL]` | `acb_series`, Arb Hurwitz values, and `acb_mat.det` enclose the finite truncated object; the Hurwitz tail has no head-truncation error beyond its ball. This does not by itself certify the infinite determinant. |
| Six q=3 anchor enclosures: 6/6 contain the published values, 6/6 have opposite certified endpoint signs, and 6/6 pass the code's `dimension_certified` flag | `code/zeta_cert_q3.py:326-354,442-511`; current artifact `code/out/zeta_cert_q3.json:252-261` | `[CERTIFIED-MODULO-HEURISTIC]` | `ball_sign` plus bisection proves a sign change for the dimension-inflated finite determinant, but the dimension tail is inferred from four observed increment ratios rather than proved for all future dimensions. |
| q=3 resonance-line coordinates: eight points with `Re(s)` numerically at 0.25 and `|det|` about `7.7e-16` to `5.6e-15` | `code/run_resonance_geometry.py:39-55`; helper `code/zeta_resonance_g5.py:136-144,181-212`; artifact `code/out/resonance_geometry.json:1-66` | `[HIGH-PRECISION-NUMERICAL]` | These are Newton pins of `cert_det_complex_mid`, which returns midpoint floats; there is no sign bracket or winding box in this script. |
| q=3 eight-point line statistic `re_std=6.47516930146045e-14`, range `2.3264723481020155e-13` | `code/run_resonance_geometry.py:100-115`; artifact `code/out/resonance_geometry.json:119-126` | `[STATISTICAL]` | `numpy.std`, min, max, and range summarize a sample of eight numerical pins; they are not interval enclosures. |
| G₅ cloud: eight off-line pins, all marked `N_stable=True`, with listed coordinates and midpoint `|det|` values | `code/run_resonance_geometry.py:57-98`; helper `code/zeta_resonance_g5.py:136-144,181-212`; artifact `code/out/resonance_geometry.json:68-116` | `[HIGH-PRECISION-NUMERICAL]` | The surface is a midpoint scan, Newton uses a finite-difference derivative, and “stability” is only the N=22 versus N=28 coordinate/depth threshold at lines 89-92. No winding count was run. |
| G₅ cloud spread `re_std=0.029986183641395464`, range `0.08545342137589007` | `code/run_resonance_geometry.py:100-115`; artifact `code/out/resonance_geometry.json:128-142` | `[STATISTICAL]` | The spread is a `numpy.std`/range over the eight selected numerical pins. |
| G₅ band winding counts 3 and 5, unresolved third band, and the partial sum 8 in `run_resonance_p3.py` | `code/run_resonance_p3.py:25-45,47-72,74-95`; called helper `code/run_resonance_v2.py:86-107`; artifact `code/out/resonance_v2.json:2235-2315` | `[CERTIFIED-MODULO-HEURISTIC]` | `gbox` does use an Arb argument-principle winding routine, but that routine uses the finite-window dimension tail and a five-point corner/center tail estimate; the Im[14,19] band and both reboxes remain `None`, so the scan is not complete. |
| G₅ localization subbox counts `1,1,1,4`, five localized `winding=1` pins, and one near-zero pin with no winding/N-stability | `code/run_resonance_p3.py:47-72,74-95`; helper `code/run_resonance_v2.py:51-83`; artifact `code/out/resonance_v2.json:2316-2691` | `[CERTIFIED-MODULO-HEURISTIC]` | These are successful local winding computations only modulo the shared tail assumptions; the fifth/near-zero candidate has `winding=null`, and the subboxes do not repair the unresolved high-Im band. |
| G₇ cloud: twelve off-line pins, all marked N-stable | `code/run_resonance_g7.py:124-186`; helper `code/zeta_cert_rosen.py:221-235`; artifact `code/out/resonance_g7.json:45-1750` | `[HIGH-PRECISION-NUMERICAL]` | `cert_absdet_mid`/`cert_det_complex_mid` discard the tail and return midpoint floats; Newton and the N=22/N=28 test locate candidates but do not prove zeros. |
| G₇ surface minima, 41 Newton seeds, and surface wall time | `code/run_resonance_g7.py:124-161`; artifact `code/out/resonance_g7.json:31-45` | `[HIGH-PRECISION-NUMERICAL]` | The 10×141 grid is a finite midpoint landscape used to seed Newton; it is neither a zero-free cover nor a certified zero count. |
| G₇ spread `re_std=0.10292157548329758`, range `0.3306609039337719`, and “SCATTERS” call | `code/run_resonance_g7.py:188-231`; artifact `code/out/resonance_g7.json:1753-1826` | `[STATISTICAL]` | The call is a thresholded interpretation of `numpy.std`/range over twelve numerical pins, not a certified zero-set or completeness statement. |
| Prospective G₇ `winding_number`/`zero_certified` records from `certify_g7_resonances.py` | `code/certify_g7_resonances.py:33-75`; helper `code/zeta_cert_rosen.py:257-324` | `[CERTIFIED-MODULO-HEURISTIC]` | If run, it performs an Arb boundary winding calculation, but it inherits the finite-window dimension-tail and corner/center `*4` inflation; the current `resonance_g7.json` has no `g7_even_winding_certified` field, so no such result was actually reported in the audited artifact. |
| q=4 control pins: three N=28 coordinates and `LINE` verdict | `code/controls_q4q6/run_q4q6_controls.py:193-309,312-475`; report `Q4Q6_CONTROLS_REPORT.md:3,15-19` | `[HIGH-PRECISION-NUMERICAL]` | The scan calls `EVEN.cert_absdet_mid`; `pin_complex` uses finite-difference Newton; N=22 versus N=28 is a stability filter, not a zero enclosure. |
| q=4 `re_std=9.829142370588003e-12` and `LINE` threshold result | `code/controls_q4q6/run_q4q6_controls.py:428-471`; report `Q4Q6_CONTROLS_REPORT.md:3` | `[STATISTICAL]` | The code computes `numpy.std` over three pins and calls `LINE` when the sample standard deviation is below `1e-3`. |
| q=6 control pins: two N=28 coordinates and `LINE` verdict | `code/controls_q4q6/run_q4q6_controls.py:193-309,312-475`; report `Q4Q6_CONTROLS_REPORT.md:4,20-23` | `[HIGH-PRECISION-NUMERICAL]` | Same midpoint/Newton/N=22-to-28 protocol as q=4; no argument-principle box was used. |
| q=6 `re_std=1.025589335680139e-11` and `LINE` threshold result | `code/controls_q4q6/run_q4q6_controls.py:428-471`; report `Q4Q6_CONTROLS_REPORT.md:4` | `[STATISTICAL]` | The result is `numpy.std` over two pins followed by the same `re_std < 1e-3` rule. |
| q=4/q=6 report's “certified-Arb midpoint surface plus Newton pinning and finite-N stability” description | `code/controls_q4q6/run_q4q6_controls.py:482-549`; report `Q4Q6_CONTROLS_REPORT.md:24` | `[HIGH-PRECISION-NUMERICAL]` | The report itself says: “The scan is a certified-Arb midpoint surface plus Newton pinning and finite-N stability; no argument-principle winding box was used for the reported geometry.” “Certified-Arb midpoint” is not a certified zero claim. |
| q=3 two-point validation gate used before q=4/q=6 | `code/controls_q4q6/run_q4q6_controls.py:150-190,588-603`; report `Q4Q6_CONTROLS_REPORT.md:8-10` | `[HIGH-PRECISION-NUMERICAL]` | It is a Newton convergence/coordinate/finite-N gate at N=30, not the six q=3 sign-change enclosures. |
| `zeta_mayer_rosen.py` q=3 regression: 5/5 hits, maximum residual `4.7580355122534e-07` in the current JSON | `code/zeta_mayer_rosen.py:425-467,640-670`; artifact `code/out/zeta_mayer_rosen.json:22-58` | `[HIGH-PRECISION-NUMERICAL]` | The regression uses NumPy/FFT construction, eigenvalues, float sign scans, and bisection; the module explicitly says “OUT OF SCOPE: no interval certification” at lines 109-122. |
| q=5 and q=8 N-stable spectral samples in the current JSON: four and six odd-sector points | `code/zeta_mayer_rosen.py:370-380,491-510,531-575,578-637`; artifact `code/out/zeta_mayer_rosen.json:146-297,422-647` | `[HIGH-PRECISION-NUMERICAL]` | The values are minima of float `|det|` across a finite N list; N-stability and n-head stability reject some numerical instability but do not prove a complex zero or completeness. |
| q=5/q=8 Weyl rows and ratios | `code/zeta_mayer_rosen.py:517-525,616-627`; artifact `code/out/zeta_mayer_rosen.json:270-297,606-647` | `[HIGH-PRECISION-NUMERICAL]` | `N_weyl` is an exact arithmetic formula evaluated at numerically selected r-values; it is a sanity comparison, not a certified spectral count. |

No audited infinite-operator geometry claim earns pure `[CERTIFIED-INTERVAL]`. The
pure interval status applies to the finite Arb objects and exact branch-tail
closures. The q=3 sign-change output and the winding outputs are one level weaker
because their infinite-dimension control is not proved by the implementation.

The current artifact also has two provenance cautions. The G₅ geometry JSON says
`wall_seconds=1585.366...`, while its adjacent log ends with `done (1360s)`;
the JSON value is retained as the artifact's own timing, but the disagreement is
not silently resolved. Also, `code/out/zeta_mayer_rosen.json` records a staged
resume with `N_LIST=[25,35,45]` and `n_head=5000`, whereas the current
`__main__` in `zeta_mayer_rosen.py:696-699` requests `[25,35,45,55]` and
`n_head=8000`; that JSON is not a clean rerun receipt for the current source.

## 2. Dimension-tail heuristic as implemented

The q=3 implementation first states the intended mathematical condition in the
comment immediately above `dim_tail_from_matrix`:

> “If every ratio in the window is provably <= q < 1 (q the certified max), the remaining tail beyond N is bounded by the geometric series tail <= g_last * q / (1 - q) ... sound given the certified contraction q<1 of the LAST increments, i.e. the eigenvalue-decay regime of the nuclear operator.” (`code/zeta_cert_q3.py:191-205`)

The executable test is exactly this finite-window calculation:

```python
def dim_tail_from_matrix(M, which, N, step=2, window=4, q_cap=0.75):
    dims = [N - (window - m) * step for m in range(window + 1)]
    # use the FULL COMPLEX det block; abs_upper of a complex increment bounds
    # BOTH the Re and Im dimension tails simultaneously.
    Ds = {d: _det_block(M, d, which) for d in dims}
    gmag = []
    for m in range(window):
        delta = Ds[dims[m + 1]] - Ds[dims[m]]
        gmag.append(delta.abs_upper())
    ratios = []
    ok = True
    for m in range(1, window):
        if gmag[m - 1] == 0:
            ratios.append(arb(0))
            continue
        rr = gmag[m] / gmag[m - 1]
        ratios.append(rr)
        if not (rr < q_cap):
            ok = False
    info = {"dims": dims,
            "increment_mag": [float(g) for g in gmag],
            "ratios": [float(r) for r in ratios],
            "q_cap": q_cap}
    if not ok or not ratios:
        return None, info
    q = arb(0)
    for rr in ratios:
        if rr > q:
            q = rr
    if not (q < q_cap):
        return None, info
    g_last = gmag[-1]
    tail = g_last * q / (1 - q)
    info["q"] = float(q)
    info["tail_radius"] = float(tail)
    return tail, info
```

Source: `code/zeta_cert_q3.py:208-243`.  With the audited run's `N=44`, this
tests only dimensions `[36,38,40,42,44]`; the stored probe reports ratios
`0.0803124, 0.0791670, 0.0772145`, takes their maximum, and extrapolates it to
all uncomputed dimensions (`code/out/zeta_cert_q3.json:7-17`).  The code does
not prove that the next ratio, or every later ratio, is at most that maximum.
The hidden assumption is therefore:

> the observed contraction of the last four determinant increments persists
> beyond the computed truncation, in the same eigenvalue-decay regime.

The Rosen engines implement the same assumption with a different cap; the exact
implementation is `code/zeta_cert_rosen_q5.py:419-452` (re-exported by the
general odd and even builders), with `q_cap=0.85`.

```python
def dim_tail_from_matrix(M, N, kappa, step=2, window=4, q_cap=0.85):
    ds = [N - (window - m) * step for m in range(window + 1)]
    Ds = {d: _det_block(M, N, kappa, d) for d in ds}
    ...
    rr = gmag[m] / gmag[m - 1]
    if not (rr < q_cap):
        ok = False
    ...
    tail = g_last * q / (1 - q)
    return tail, info
```

Source: `code/zeta_cert_rosen_q5.py:415-452`; it is re-exported by
`code/zeta_cert_rosen.py:57-63` and `code/zeta_cert_rosen_even.py:75-82`.
`certified_det` then adds that radius to both real and imaginary components
(`code/zeta_cert_rosen_q5.py:461-476`).

The branch-series part is a different matter. In q=3,
`Ls_column_series` computes the finite head and then adds the Hurwitz-series
tail (`code/zeta_cert_q3.py:142-156`); `n_head` is therefore a conditioning
split, not an unbounded numerical sum. The same exact-Hurwitz construction is
used by the Rosen Arb builders. The heuristic enters at the *dimension/Fredholm
tail*, not at the conditionally convergent branch sum.

There is a second, spatial version of the same trust problem in winding. The
winding routines evaluate the dimension tail only at the center and four
corners, take the maximum, and multiply it by four before adding it to every
boundary ball (`code/zeta_resonance_g5.py:223-240`,
`code/zeta_cert_rosen.py:257-273`, and
`code/zeta_cert_rosen_even.py:264-284`). No analytic supremum over the whole
box is computed. Thus a reported winding count is conditional both on
truncation-persistence and on that asserted uniformization of the tail over the
box.

## 3. Upgrade ladder

The required upgrade is not “more decimal places.” It is a proven tail bound,
followed by a certified local or global zero-isolation computation.

| Present item | Computation needed for promotion | Runtime estimate grounded in audited runs |
|---|---|---|
| q=3 eight-point resonance line | Use `zeta_cert_q3.certify_zero`-style Arb sign brackets for all eight points, after replacing the finite-window tail extrapolation with a genuine trace/nuclear-norm or analytic coefficient tail bound. | The six-anchor run took `735.544 s` (`code/out/zeta_cert_q3.json:261`); linear scaling gives about `981 s` (16.3 min) for eight comparable points, before any extra precision/tail-proof overhead. |
| q=3 six anchor enclosures | Retain the existing endpoint sign/bisection proof, but make `dimension_certified` depend on a theorem-level bound valid for all discarded dimensions, not on the last four ratios. | Already 735.5 s for six; a proven bound may cost more, but no new geometric search is required. |
| G₅ eight-pin cloud | For every pin, run an off-line argument-principle box with nonzero boundary Arb balls and integer winding, using a proven dimension tail and a proven uniform box bound. To certify the cloud as a set, also split/cover the scan region and resolve the currently unresolved high-Im band. | The q=3 counting box took `80.369 s` at `N=30,K=48` (`resonance_v2.json:47-52`). The existing G₅ successful winding boxes took `182.170 s` and `183.499 s` at `N=22,K=44` (`resonance_v2.json:2235-2267`), so eight local boxes are roughly 24 min at that measured scale, plus retries and coverage boxes. |
| G₅ P3 counts 3+5 and unresolved third band | Replace the current heuristic tail/uniformization, then subdivide Im[14,19] until every boundary is certified away from zero and every subbox has an integer winding count; do not report the partial sum as a count for the full rectangle. | The two failed reboxes already cost `49.624 s` and `37.714 s`; each additional subdivision is on the order of a minute or more at the observed G₅ rate. |
| G₇ twelve-pin cloud | Extend `certify_g7_resonances.py` beyond `MAXCERT=5`, and run a winding box around each selected pin. Replace the shared dimension-tail and corner/center inflation with proven bounds first. | The q=3 K=48 box gives an 80.4 s reference. A K=24 attempt is roughly half that by boundary-sample count: a q=3-linear lower bound is about 40 s per attempt, 5 pins × 4 possible box sizes ≈13 min. Actual q=7 cost will be higher; the existing q=7 surface alone reached 832 s (`resonance_g7_run.log:1-10`). |
| q=4 three-pin control | Call `zeta_cert_rosen_even.winding_box` around each N=28 point, with a proven dimension tail and nonzero boundary balls; to support a “line” conclusion over the scan, add exhaustive zero-free coverage outside the local boxes. | The q=3 80.4 s K=48 box is the baseline. At K=24, a q=3-linear estimate is ~40 s per q=4 box, or ~2 min for three; allow retries and coverage overhead. The measured q=4 surface was 157.7 s and pinning 19.9 s (`Q4Q6_CONTROLS_REPORT.md:15-19`). |
| q=6 two-pin control | Same `winding_box` computation at both points, plus a certified cover of the scanned rectangle if the claim is about all resonances there. | The q=4/q=6 surface-time ratio was `365.1/157.7≈2.31`; applying it to the ~40 s q=4 box estimate gives ~90 s per q=6 box, or ~3 min for two before retries. Measured q=6 surface and pinning were 365.1 s and 45.1 s (`Q4Q6_CONTROLS_REPORT.md:20-23`). |
| q=5/q=8 N-stable samples from `zeta_mayer_rosen.py` | Use an Arb builder for the relevant q/sector, prove the discarded-dimensional and branch tails, then use winding boxes around each candidate; for a spectral list claim, certify a zero-free remainder or an independent count. | No valid wall time for the current source invocation is present: the only JSON is a staged resume with parameters different from `__main__`. A q=3 time-only extrapolation would be misleading because this path uses NumPy FFT/eigenvalues (`zeta_mayer_rosen.py:109-117,370-380`) rather than the q=3 Arb engine. |

## 4. Paper-ready Verification summary

The six q=3 anchor enclosures are `[CERTIFIED-MODULO-HEURISTIC]`: their Arb
branch arithmetic and endpoint sign changes are explicit, but the discarded
dimension tail is extrapolated from a finite window of observed determinant
increments and is not a proven all-​N bound. The q=3 eight-point line, the eight-point
G₅ cloud, the twelve-point G₇ cloud, and the q=4/q=6 control pins are
`[HIGH-PRECISION-NUMERICAL]` Newton/midpoint computations with finite-N stability
checks, while their reported standard deviations and ranges are `[STATISTICAL]`
sample summaries. In particular, the q=4/q=6 report states verbatim that the
geometry used “a certified-Arb midpoint surface plus Newton pinning and finite-N
stability; no argument-principle winding box was used for the reported geometry.”
Accordingly, these results do not constitute pure `[CERTIFIED-INTERVAL]` zero
enclosures or a certified completeness statement; promotion requires proven
tail bounds and argument-principle winding/zero-free coverage.
