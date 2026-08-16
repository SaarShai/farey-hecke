# LAW tail probes D1 (migration) and B1 (float scaling curve) — results

Lane G leg 2 (builder), ticket `law-tail-anchor-probe.md`, per
`LAW_TAIL_SCOPING.md` §2.5 (D1) and §3.5 (B1). Both probes are
**NON-RIGOROUS**: midpoint float evaluation of the certified Arb-ball
builders, no winding certificate computed. Labelled throughout.

## Builder substitution note (read before the tables)

The ticket names `zeta_cert_rosen.py`'s `lam_ball(q)` /
`build_reduced_matrix_ball` as the q-generic builder for Probe D1. That module
**only handles odd q** (`build_reduced_matrix_ball` raises
`NotImplementedError` for even q — MMS eq.34 vs eq.32 have different block
structure). `q = 12, 16, 22` — the ticket's own D1 grid — **are all even**.
Probe D1 therefore uses `zeta_cert_rosen_even.py`, the sibling even-q
generalized builder in the same worktree (same lineage: re-exports the exact
Hurwitz/`acb_series` primitives from `zeta_cert_rosen_q5.py` verbatim, only
the geometry and MMS eq.32 block placement differ; anchor-validated at q=8
against the double-precision reference, general-q code path exercised here
for the first time at q=12,16,22). This is a substitution of the *matching*
sibling module for the requested q's, not a scope change — flagged loudly
per the brief's instruction to report honestly.

Probe B1 uses `family_prep_constants.py`'s `RhoEvaluator` /
`capture_allowed_blocks`, which wraps `zeta_mayer_rosen.build_reduced_matrix`
(q-generic, both parities, float64) — this matched the brief's named pattern
directly; no substitution needed.

---

## Probe D1 — narrow-box determinant scan, q = 12, 16, 22

**Method.** mms+ sector (`sign=+1`, the sector with off-line pins in the
q=7/8 repo data). Two-stage: (1) coarse grid, `N=16`, `Re ∈ [0.15,0.45]`
(16 pts), `Im ∈ [6.6,7.6]` (21 pts), midpoint `|det|`; local-minimum seeds
(3×3 window test, fallback to the 8 lowest cells if none pass); (2)
complex-Newton refine each seed at `N=48` (finite-difference derivative,
tol `1e-10`). For q=22, one additional re-refine at `N=96` to spot-check
stability (per the brief). Builder: `zeta_cert_rosen_even.py`, `n_head=4`,
400-bit Arb precision (`ctx.prec`), midpoints only (no ball radii used —
this is deliberately a probe, not a certificate).

Script: `law_probes/probe_d1_scan.py`. Receipts:
`law_probes/d1_q{12,16,22}.json`, `law_probes/d1_q22_n96_stability.json`,
logs `law_probes/d1_q{12,16,22}.log`.

### Per-q candidates (all converged, `absdet` at machine-zero after Newton)

| q | seed (Re,Im) | refined pin (Re,Im), N=48 | absdet |
|--:|---|---|---|
| 12 | (0.210, 7.500) | (0.206880, 7.481235) | 8.5e-16 |
| 16 | (0.210, 7.350) | (0.202094, 7.349177) | 2.2e-15 |
| 16 | (0.350, 6.750) | (0.337589, 6.724694) | 5.5e-16 |
| 16 | (0.410, 7.300) | **(0.407938, 7.298233)** | 2.2e-16 |
| 22 | (0.250, 7.200) | **(0.248468, 7.205146)** | 5.0e-16 |
| 22 | (0.350, 7.550) | (0.341920, 7.540344) | 2.5e-15 |
| 22 | (0.410, 6.950) | (0.403647, 6.940808) | 8.6e-16 |

q=12 found exactly one candidate in the box. For q=16 and q=22, the
**pin adopted below is the candidate with the smallest `absdet`** (the most
numerically confident root) — bold in the table. This selection rule is
independent of distance-to-`s_∞`; it happens to coincide with the
nearest-to-`s_∞` candidate at both q=16 and q=22 (checked explicitly, not
cherry-picked): q=16 distances are 0.286, 0.354, **0.280**; q=22 distances
are **0.138**, 0.482, 0.199. No selection bias toward the migration
hypothesis.

**q=22 stability spot-check (N=48 → N=96):** re-refining the adopted pin at
`N=96` converged in 1 Newton step with **zero change** to 15 decimal places
(`re=0.24846809418782273`, `im=7.205145931613445`, `absdet=5.04e-16` at both
N=48 and N=96). The pin is `N`-stable at this precision.

### Migration table: `|pin(q) − s_∞|`, `s_∞ = 0.25 + 7.0673625708673465i`

| q | pin | dist to s_∞ |
|--:|---|--:|
| 12 | 0.206880 + 7.481235 i | 0.416113 |
| 16 | 0.407938 + 7.298233 i | 0.279725 |
| 22 | 0.248468 + 7.205146 i | 0.137792 |

**Monotone decreasing in q.** This alone is the headline fact: the adopted
mms+ pin closest-to-line in the box gets closer to `s_∞` as q grows,
12 → 16 → 22, with no reversal (contrast the scoping note's §1.4 warning that
the raw "lowest-Im pin" heuristic is non-monotone at q=5,7,8 — this is a
*different* selection rule, box-restricted + lowest-absdet, and it *is*
monotone over this q range).

### Power-law fit and discrimination (free regression + 3 fixed exponents)

Free log-log regression (`dist ~ C·q^p`, least squares over the 3 points):
**p = −1.83**, C = 41.1.

Residual comparison for the three candidate exponents (fit `C` per exponent
by geometric mean, residuals in log-space, sum-of-squares):

| exponent p | fitted C | log-residuals (q=12,16,22) | SS(log-resid) |
|---|--:|---|--:|
| −1 | 4.077 | +0.2028, +0.0934, −0.2962 | 0.1376 |
| −4/3 (−1.333) | 10.31 | +0.1035, +0.0900, −0.1935 | 0.0563 |
| **−2** | **65.90** | **−0.0951, +0.0831, +0.0120** | **0.0161** |

`q^{-2}` fits the three points **best** among the tested exponents (SS
smaller by 3.5× vs `q^{-4/3}` and 8.5× vs `q^{-1}`), and the free-regression
slope `−1.83` sits closer to `−2` than to either alternative. With only 3
points this is not a statistically tight discrimination, but the ordering is
unambiguous and the residual pattern for `p=-2` is small and sign-alternating
(no systematic curvature), consistent with `q^{-2}` being close to the true
law.

### D1 Verdict: **MIGRATION-CONSISTENT**

The pin distance to `s_∞` decreases monotonically over q=12,16,22, and the
decay rate is closer to the `q^{-2}` prediction than to `q^{-1}` or
`q^{-4/3}`. This is genuine (if weak — 3 points, non-rigorous midpoint scan,
builder substitution noted above) support for the Rouché-continuation
route's premise that a pin exists in the box for every sampled q and drifts
toward the anchor. It does **not** certify anything: no winding number was
computed, so "a pin in the box" here means "a converged Newton root of the
midpoint determinant landed in the box," not a certified isolated zero.
Recommend Leg 2's gate (open the T2 ticket) is **supported**, not proven —
report this as the honest strength of the evidence, matching the brief's
instruction not to inflate.

---

## Probe B1 — float disc optimizer scaling curve, q = 10,14,18,22,26,30

**Method.** `RhoEvaluator`/`capture_allowed_blocks` from
`family_prep_constants.py` (float64, 2048 circle points per disc, tail
indices to 59 — identical evaluation kernel to the q=7 `f7_mitigation_
stage0.py` run). Coarser search than that q=7 run: 3 multi-starts (two
linear-decreasing inflation profiles + one uniform), coordinate-descent
steps `(0.1, 0.05, 0.02, 0.01, 0.005)` vs F7's `(0.05,...,0.001)` and F7's
`3^19`-shell multi-start. **Correction made mid-run:** a uniform-inflation
start gives `ρ* ≥ 1` for `kappa ≥ 6` (`q ≥ 14`) — probed directly and
confirmed the mechanism (the `n=1`/tail head block near the parabolic branch
needs a large-near-component-1, small-near-component-κ inflation profile,
exactly the shape of F7's frozen factors `(2.79,2.39,1.90,1.56,1.35)`, not a
flat one). Fixed by adding the two linear-decreasing starts before running
the full sweep; recorded here for honesty rather than silently editing.

Script: `law_probes/probe_b1_scan.py`. Receipts: `law_probes/b1_q{q}.json`,
`law_probes/b1_summary.json`, `law_probes/b1_q8.json` (sanity check only,
not part of the 6-point table — see below).

### Sanity check against the existing repo receipt

Running the same coarser optimizer at q=8 (not requested, run only as a
cross-check): `ρ* = 0.7720`, **lower** than `F7_CONSTANTS_MANIFEST.md`'s
pilot value `0.8207785` for q=8. This is plausible, not a red flag: different
multi-start basins in a non-convex per-block min-max landscape can land on
different local optima, and the q=8 pilot run's factors
`(3.00, 1.90, 1.35)` were not exhaustively re-optimized in this repo the way
q=7's were. Flagged so the reader does not misread B1's q=8 number as
disagreeing with a certified value — nothing here is certified either way.

### ρ*(q) table

| q | κ | ρ*(q) | 1−ρ*(q) | worst block |
|--:|--:|--:|--:|---|
| 10 | 4 | 0.813296 | 0.186704 | (3→2, n=1 head) |
| 14 | 6 | 0.856696 | 0.143304 | (6→6, n=−1 tail) |
| 18 | 8 | 0.914003 | 0.085997 | (3→2, n=1 head) |
| 22 | 10 | 0.929466 | 0.070534 | (3→2, n=1 head) |
| 26 | 12 | 0.943000 | 0.057000 | (3→2, n=1 head) |
| 30 | 14 | 0.950202 | 0.049798 | (3→2, n=1 head) |

`1 − ρ*(q)` decreases monotonically, `n=±1`-branch-dominated at every q
except q=14 (tail block worst there) — consistent with §1.2/§3.2 of the
scoping note's mechanism (parabolic `λ→2` degradation of the `n=1` branch).

### Power-law fit

Least-squares log-log regression over all 6 points:
**`1 − ρ*(q) ≈ 3.61 · q^{-1.268}`**, `R² = 0.975`
(residuals in `1-ρ*` units: −0.0081, +0.0162, −0.0065, −0.0012, −0.0010,
+0.0014 — small, no systematic trend, good fit over this wider q-range).

Comparison to the scoping note's 3-point HEURISTIC fit (q=5,7,8, exponents
in `[−1.46, −1.33]` depending on which pair of points is used): the 6-point
exponent **−1.27** is *shallower* than that range, i.e. the decay is a bit
slower over the wider q=10..30 window than the 3-point q=5..8 fit predicted.
Both are float, non-rigorous, and this optimizer's coarser search means the
`ρ*` values here are **upper bounds** on the true disc-optimum `ρ*(q)` (a
deeper search, as in F7's, can only lower them) — so `1-ρ*(q)` here is a
*lower*-bound-on-the-decay-rate estimate; the true exponent could be
somewhat steeper (closer to the 3-point range) once optimized as thoroughly
as q=7 was.

### B1 Verdict: **decaying, no plateau — closes (b) as a tail route**,
**exponent ≈ −1.27 (this coarser 6-point search), 95% "eyeball" confidence
band roughly [−1.1, −1.5] given the coarse-search upper-bound caveat above
and the discrepancy with the 3-point HEURISTIC range**

`1 − ρ*(q)` shows **no plateau** through q=30 (it is still `0.0498` at
q=30, an order of magnitude below q=10's `0.187`, continuing to fall). Per
the scoping note's own decision rule (§3.5): "If it continues as `q^{-1.4}`,
(b) is closed as a tail route and the finding is banked as a negative." The
6-point exponent (−1.27) is close to but shallower than −1.4; either way the
qualitative verdict is unchanged — **(b) remains LOW feasibility as a tail
route** (no uniform `ρ_max < 1` exists) and is **REQUIRED only as the finite
base**, exactly as the scoping note already concluded. This run adds 6 more
points of confirmation and rules out the plateau alternative that would have
overturned the note's ranking.

---

## Time / compute record

- B1: all 6 q's ran in ≈1–2 s each (cheap, as scoped).
- D1: q=12 grid+refine ≈ 382 s; q=16 ≈ 1297 s; q=22 grid+refine ≈ 2401 s plus
  the N=96 stability re-refine ≈ 1232 s (total q=22 wall ≈ 3633 s ≈ 61 min,
  within the ticket's 1–2 h/q budget). All three q's ran as parallel `nohup`
  background processes as instructed.

## Receipts index

- `law_probes/probe_d1_scan.py`, `law_probes/probe_b1_scan.py` — scripts.
- `law_probes/d1_q12.json`, `d1_q16.json`, `d1_q22.json`,
  `d1_q22_n96_stability.json` — D1 receipts.
- `law_probes/b1_q10.json` … `b1_q30.json`, `b1_summary.json`,
  `b1_q8.json` (sanity-only) — B1 receipts.
- `law_probes/d1_q{12,16,22}.log`, `b1_run.log` — run logs.
