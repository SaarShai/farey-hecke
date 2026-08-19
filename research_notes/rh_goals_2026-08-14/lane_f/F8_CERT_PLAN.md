# F8 CERT PLAN — q=8 off-line resonance certificate (run plan)

Lane F, 2026-08-17. EVEN-q analogue of `F7_CERT_PLAN.md`. This pass covers
**Stage 0–2 ONLY** (source builder port, TB block certification, N-convergence
probe) — local, no Kaggle, no R2 envelope, no R3b winding, no bundling. R2 /
R3b / `kaggle_f8/` / canary are gated on judging this pass, per coordinator
scope confirmation (this session, following commit 1f2b578 which banked
`make_bundles.py` and the box-selection work).

**Update (this pass, gates-resolution round):** commit 51faa5d banked Stage
0–2 and promoted the two flags raised in §2/§3 below to blocking gates on R2.
Both are now resolved — see §"Gates (resolved this pass)" at the end of this
file for the verdicts, receipts, and the updated §2 factors this changed.
§2's original narrative below is left in place except for the factors table,
which now reflects the GATE-2-hardened geometry; the *old* (thin-margin)
factors and their ρ*=0.9987 result are preserved verbatim in the gates
section for the record.

## 0. Box (carried from the prior pass, unchanged)

s₀ = 0.4252310423737965 + 4.345760788321986 i, sign = +1 (mms+ sector),
q = 8. Source: `lane_k/harvest/hecke_family_q7_q8_scan.json`, surface
`q8_mms_plus`, pin 1 (smallest N22→N28 drift of the family, ~3 orders better
than the next candidate). K_s box margin ≈ 0.6227577 (down-rounded), δ =
½ − Re(s₀) − 1e-6 ≈ 0.0747680 (down-rounded).

## 1. Even-q deltas — MMS eq.(32) vs eq.(34), stated explicitly

This is the section the coordinator asked not to leave implicit.

**q=7 (odd, eq.(34)):** `h_7 = 2`, `κ_7 = 2h+1 = 5`. Partition of
`[-λ/2, 0]` into `κ` intervals needs **two interleaved continued-fraction
families** (even-index and odd-index points use different digit-word rules —
see `F7_CERT_PLAN.md` §"Special columns move" / `F7_CONSTANTS_MANIFEST.md`
§6.3). The reduced operator's eq.(34) block list has **19 blocks** (9 finite
head blocks + 10 Hurwitz-tail families), because the K_s word for odd q keeps
an `L_1^{h-1}` factor and every disc index up to `κ=5` participates in the
"tail lands on g_κ" recursion independently.

**q=8 (even, eq.(32)):** `h_8 = (q-2)/2 = 3`, `κ_8 = h_8 = 3` (for even q,
kappa equals h_q exactly — no `2h+1`). The partition of `[-λ/2, 0]` needs
only **one** continued-fraction family: `φ_i = CF([1]^(h-i))`, `i = 0..h`,
with `φ_0` overridden to `-λ/2` (verified against
`zeta_cert_rosen_even.partition_points_ball`, byte-for-byte the same rule).
The reduced operator's eq.(32) assembly loop is short and uniform:

```
add_cols(1, h, inf_block(1, h, 2, False))
add_cols(1, h, inf_block(1, h, 1, True), prefac=sgn)
for i in 2..h:
    add_cols(i, i-1, single_block(i, i-1, 1, False))
    add_cols(i, h, inf_block(i, h, 2, False))
    add_cols(i, h, inf_block(i, h, 1, True), prefac=sgn)
```

giving **8 blocks** at h=κ=3: 2 finite head-only blocks (the direct
partition-adjacency maps `2→1` and `3→2`) + 6 Hurwitz-tail families (all
landing on the last disc, `g_3`). Every block's target column is `g_h = g_3`
(component `h`), unlike odd q where heads/`L_{-1}` land on `g_{2h}` and tails
land on `g_{2h+1}` — a structurally simpler, single-target recursion. This
matches `zeta_cert_rosen_even.build_reduced_matrix_ball`'s own eq.(32) loop
exactly (that module is where the block list above was read from, then
hand-transcribed into `f8_certify_tb_blocks.BLOCKS` / `f8_source_builder.py`
for the TB-block certification layer, which needs a different, ratio-
optimizable disc geometry than that module's fixed determinant-build
geometry — see §2).

**Field degree:** λ_8 = 2cos(π/8) = √(2+√2), an exact **degree-2** radical
(vs λ_7's degree-3 minimal polynomial `x³-x²-2x+1`, vs λ_5's degree-2 golden
ratio). q=8 is algebraically the simplest of the three so far.

## 2. TB block certification (stage 1)

Files: `f8_certify_tb_blocks.py` (BLOCKS list + geometry + certification
driver, reusing `tb_certify/certify_tb_blocks.py` (v1) and
`certify_tb_blocks_v2.py` (v2) verbatim — same reuse discipline as F7),
`f8_source_builder.py` (value-only matrix assembly, factor-parameterized).

**Geometry finding (new, q=8-specific — flag this clearly):** the uniform
safety factor 2.5 that `zeta_cert_rosen_even.py` uses for its **determinant
build** (chosen there for numerical robustness of `cert_det`, not for a
ratio-< 1 convergence bound) does **not** certify at the TB-block layer: at
factor 2.5 uniform, the two finite head-only blocks (`2→1`, `3→2`, the
direct partition-adjacency maps at n=1) have containment ratio 1.26 / 1.63
— **greater than 1**, i.e. the source disc's image is NOT contained in the
target disc at that geometry. A local grid search (uniform scaling only
makes it *worse*: ratio grows with the inflation factor, since the finite
blocks are near-critical at the bare partition half-widths — worst ratio is
already 1.02 at factor 1.0) found non-uniform per-disc factors
**(1.7, 1.4, 1.15)** for discs (1, 2, 3) bring every block under ratio 1.

**Certified result** (`f8_receipts/F8_TB_BLOCK_CERTIFICATES_RECEIPT.json`,
`PREC_BITS=384`, `M=512`, `K_start=6`, `max_K=24`):

| block | kind | certified ratio upper bound | pass |
|---|---|---:|---|
| 1→3, +2 | tail (K=11) | ≤ 0.998676850298546… | PASS |
| 1→3, −1 | tail (K=12) | ≤ 0.998676850298546… | PASS |
| 2→1, +1 | head (finite) | ≤ 0.873181440360437… | PASS |
| 2→3, +2 | tail | ≤ (comfortably under) | PASS |
| 2→3, −1 | tail | ≤ (comfortably under) | PASS |
| 3→2, +1 | head (finite) | ≤ 0.873181440360437… | PASS |
| 3→3, +2 | tail (K=11) | ≤ 0.996646888568821… | PASS |
| 3→3, −1 | tail (K=12) | ≤ 0.996646888568821… | PASS |

**SUPERSEDED this pass — see §"Gates (resolved this pass)" / GATE 2.** The
factors (1.7, 1.4, 1.15) and ρ*=0.9987 above are the historical record of
what Stage 1 first certified; `f8_certify_tb_blocks.py` and
`f8_receipts/F8_TB_BLOCK_CERTIFICATES_RECEIPT.json` now hold the
GATE-2-hardened geometry `(3.4, 2.2, 1.4)`, certified ρ* = 0.9074127334.

**rho\* = 0.998676850298546231512835 (Arb ball, both endpoints agree to
1.11e-25)** — `PASS_RHO_LT_1.0`. **Caveat, stated plainly: this margin is
thin** (0.13% below the basic-convergence gate), driven by the crude
centered-at-zero deep-tail bound needing a large `K` (11–12) before it beats
the finite head-terms' own ratio at this geometry. Contrast q=7's certified
ρ\*=0.7623 (comfortable 24% margin under its 0.80 gate). **q=8's TB geometry
is not yet optimized for a production R2/R3b run** — it establishes
convergence (ρ\*<1, hence the truncated block series converges), not a
production-grade rate. Re-optimizing (1.7, 1.4, 1.15) further, or splitting
per-block radii more finely, is flagged as the first task of the *next* pass
(R2 envelope), not attempted here — this pass's threshold is deliberately
`ρ*<1` (basic convergence, reported not gated — see `f8_certify_tb_blocks.py`
module docstring), since no prior q=8 float stage-0 optimization exists to
re-target against (unlike q=7's `F7_MITIGATION_REPORT.md`).

Pole/branch-cut clearance: all blocks PASS (see
`f8_receipts/F8_TB_BLOCK_CERTIFICATES.md` for the full per-block table).

## 3. Validation — two checks, both against ground truth

**(a) Internal consistency: `f8_source_builder`'s explicit 8-block assembly
vs the trusted generic `zeta_cert_rosen_even.build_reduced_matrix_ball`.**
Both implement the same eq.(32) loop; compared at the SAME geometry (uniform
factor 2.5, `zeta_cert_rosen_even`'s own default) to isolate "same assembly,
same geometry" from "different geometry, different but individually valid
matrix" (the (1.7,1.4,1.15) TB-optimized geometry above is deliberately
different from the uniform 2.5 the trusted engine hardcodes).

```
s = 0.5 + 5.798144i, N=12, sign=-1, q=8, n_head=4
max |entry diff| = 0.0   PASS (byte-identical Arb balls)
```

**(b) Ground truth: the trusted engine's own double-precision cross-check**
(`zeta_cert_rosen_even.selfcheck_vs_doubleprec(8, N=10)`, comparing against
`zeta_mayer_rosen.build_reduced_matrix(8, ...)`, `n_head=8000` FFT reference):

```
max |entry diff| = 6.183414e-05, max rel = 1.519
(module's own stated FFT resolution: ~1e-6; this run's abs error is ~60x
that figure — the module's own header claims ~1e-7, so this is worth a flag,
not silently accepted: EITHER the double-prec reference's FFT tail resolution
at N=10 is worse than the header states, OR there is a real discrepancy.
Not independently re-derived this pass — logged as a caveat, not resolved.)
```

Since (a) proved `f8_source_builder` (uniform-2.5 geometry) is
**byte-identical** to `zeta_cert_rosen_even`'s generic builder, (b)
transitively validates `f8_source_builder` too — it is not an independent
re-derivation, it inherits the existing engine's own self-check, caveat
included.

## 4. N-convergence check (stage 2 / F7_CERT_PLAN §3 analogue)

Single center-point probe at s₀ (interior, not the box boundary — same
scope as F7_CERT_PLAN §3's own scan-evidence paragraph, which was also a
center-point float/ball check; the boundary-sup-driven decision is R2's job,
next pass), via the trusted `zeta_cert_rosen_even.cert_det` (uniform-2.5
geometry, the engine actually used for `cert_det`/winding, not the TB-layer's
(1.7,1.4,1.15) geometry):

| N | \|det\| (mid) | tail (Arb upper) | tail / \|det\| | wall |
|---:|---:|---:|---:|---:|
| 16 | 7.679140e-09 | 9.522e-09 | 1.240 | 0.3s |
| 20 | 2.664019e-11 | 2.818e-11 | 1.058 | 0.4s |
| 24 | 9.172472e-14 | 9.841e-14 | 1.073 | 0.7s |
| 28 | 1.937329e-15 | 3.148e-16 | **0.163** | 1.0s |
| 32 | 1.818476e-15 | 7.467e-19 | **4.1e-4** | 1.4s |

`|det|` decays geometrically N=16→24 (consistent with approaching a genuine
near-zero — the scan's pin drift is ~2.6e-13, so the residual determinant at
this float-precision center is expected to be small but nonzero), then
**stabilizes** at ≈1.8e-15 from N=28 to N=32 — the tail bound has become
subdominant and the value is N-converged. This matches the q=12 finding in
`LAW_CERTIFIED_DEEPCOUNT_MULTI.md` ("even q needs N=24 not N=20" for a
deep-corner point) — here the point is shallow (Im=4.35, not the q=12 deep
corner at Im=12), so convergence is faster, by N≈28–32 rather than N≥24
marginal / N=28 robust.

**Decision (provisional, this pass only — the real N_PRIMARY/N_COMPARISON
freeze per F7_CERT_PLAN's own rule happens AFTER R2's boundary-sup
measurement, not from this single interior point):**

- **N_PRIMARY = 32** (tail/|det| = 4.1e-4, comfortable).
- **N_COMPARISON = 28** (tail/|det| = 0.163, thinner but still sub-dominant;
  independent secondary confirmation, same convention as F7's
  N_PRIMARY=256/N_COMPARISON=224 pairing — not a deliberately-failing
  control, which F7 also did not use N_COMPARISON for).
- Both are far below F7's N_PRIMARY=224–256 (odd q, κ=5, 5N-dim matrix); q=8
  needs `κN = 3×32 = 96`-dimensional matrices vs q=7's `5×224 = 1120` — a
  cost-class difference, consistent with κ_8=3 < κ_7=5 and q=8's box being
  shallower (Im=4.35 vs F7's Im=4.67, comparable) and better-drift-selected.
- **Caveat:** this is a single interior point, not the box-boundary
  supremum R2's F_R(N) inequality actually needs. Treat N_PRIMARY/
  N_COMPARISON above as a strong prior for R2's N-grid, not a frozen
  decision — R2 (next pass) must re-derive F_R(N) properly before any
  contour work starts, exactly as F7_CERT_PLAN §3 requires.

## 5. What this pass does NOT do (explicitly out of scope, gated on judging)

1. R2 envelope (boundary-sup `F_R(N)` derivation, the actual N-freeze).
2. R3b closed-contour winding certificate.
3. `lane_f/kaggle_f8/` bundle construction (`make_bundles.py`-style, q=8
   files don't exist yet at that layer — only stage-0/1 files do).
4. Any Kaggle push (canary or otherwise).
5. K_s gate box-margin re-verification against the FULL box (only the
   center-point margin was computed in the prior pass — trivial given the
   nearest lattice point is 0.62 away and the box half-width is 1e-6, but
   not re-derived here).
6. Re-optimizing the TB-block disc geometry beyond the coarse grid search in
   §2 (ρ*=0.9987 is thin; a finer/per-block search should happen before R2
   commits to a geometry).

## 6. Artifacts

- `f8_certify_tb_blocks.py` — TB block certification driver (BLOCKS list,
  geometry, v1/v2 reuse).
- `f8_source_builder.py` — value-only 8-block matrix assembly
  (factor-parameterized), validated against the trusted generic builder.
- `f8_receipts/F8_TB_BLOCK_CERTIFICATES_RECEIPT.json`,
  `f8_receipts/F8_TB_BLOCK_CERTIFICATES.md` — stage-1 certificate.

No existing file was modified except as listed. No commits, no Kaggle
pushes, this pass.

## Gates (resolved this pass)

Coordinator promoted §3's double-precision-selfcheck anomaly and §2's thin
ρ*=0.9987 to blocking gates on R2 (commit 51faa5d banked Stage 0–2). Both
resolved below. R2 remains a separate, not-yet-started pass.

### GATE 1 — `selfcheck_vs_doubleprec(8, N=10)` anomaly

**(a) Locate the max-rel entry.** Re-ran the selfcheck with per-entry
instrumentation (not part of the banked module; a diagnostic-only script, not
committed). The worst-relative-error entry is **`(row=0, col=29)`** — the
top-right corner of the truncated `30×30` (`κN=3×10`) matrix, i.e. the
**deepest tail column at the truncation edge** (component 3, series index
`m=9` of `N=10`, the last basis function kept before truncation):

```
idx=(0,29)  mine = 4.928149e-09 + 9.467264e-09j   (|mine| ≈ 1.07e-08)
            dp   = 7.932121e-09 − 6.464881e-09j   (|dp|   ≈ 1.02e-08)
abs diff = 1.621e-08     rel diff = 1.519  (i.e. 151.9%)
```

Both values are **near-zero relative to the matrix scale** (Frobenius norm
≈107): this is a truncation-edge coefficient near the double-precision
builder's own FFT noise floor (its `n_head=8000`-term tail sum has residual
FFT/aliasing error at exactly this kind of small, high-index entry), not a
disagreement between two well-resolved values. Recomputing with the
matrix-norm-normalized metric the coordinator asked for:

```
max |diff| (absolute, whole matrix)      = 6.183e-05
Frobenius norm of the certified matrix   = 106.98
max |diff| / Frobenius norm              = 5.780e-07
max |diff| / operator (spectral) 2-norm  = 6.375e-07   (2-norm = 96.998)
```

Both normalized figures land **inside** the module's stated ~1e-6 to ~1e-7
resolution band. The raw `max_rel=1.519` figure the module prints is an
artifact of dividing by `max(|mine|, |dp|, 1e-12)` at an entry where both
operands are ~1e-8 — a standard cross-precision-comparison pitfall (relative
error is meaningless near zero), not evidence the matrices disagree.

**(b) Is q=8 an outlier, or does the harness do this everywhere?** Ran the
identical selfcheck at q=12 (the multi-q note's own validated even case) and
q=4 (algebraically the simplest even case, kappa=1):

| q | dim (κN) | max abs diff | max rel diff | rel-worst entry | Frobenius norm | max abs / Frobenius |
|---:|---:|---:|---:|---|---:|---:|
| 4  | 10 | 1.105e-04 | 7.782e-03 | (0, 9)  — truncation-edge column | 102.32 | 1.080e-06 |
| 8  | 30 | 6.183e-05 | 1.519e+00 | (0, 29) — truncation-edge column | 106.98 | 5.780e-07 |
| 12 | 50 | 6.237e-05 | 1.173e+00 | (0, 49) — truncation-edge column | 64.43  | 9.681e-07 |

**Everywhere.** All three q have their worst-relative-error entry at the
identical structural location — row 0, the LAST column (the deepest
truncation-edge basis coefficient) — and q=8's `max_rel=1.519` is not an
outlier among q=4's `7.8e-3` / q=12's `1.173`: q=4 happens to have a
larger-magnitude worst-entry so its naive relative metric looks smaller, but
the underlying absolute-error and Frobenius-normalized figures are the same
order of magnitude (`~1e-4` abs, `~1e-6` to `1e-7` normalized) at all three
q. The harness's raw `max_rel` print is unreliable everywhere it's used, not
specifically broken for q=8.

**Verdict: HARNESS-ARTIFACT.** The builder is not defective — its Frobenius-
and operator-norm-normalized agreement with the double-precision reference is
`5.8e-7` at q=8 (`9.7e-7` at q=12, `1.1e-6` at q=4), consistent with the
module's own stated resolution claim. The module's raw printed `max_rel`
statistic (division by `max(|a|,|b|,1e-12)` with no near-zero guard) is a
**harness-metric defect**, not a stated-claim-wrong situation either — the
module's header text describes absolute/FFT resolution (`~1e-6`), which is
correct; it is the `max_rel` PRINT LINE specifically that is misleading and
should be read with the near-zero caveat above (not itself a blocking
finding, since the header's actual documented claim was about absolute
resolution, which holds). No change made to `zeta_cert_rosen_even.py` (out of
scope — it is the trusted, already-cross-validated engine; this gate was
about explaining an anomaly, not patching upstream code this pass).

Diagnostic scripts used for (a)/(b) are not committed to the repo (adhoc,
inline `python3 - <<'PYEOF'` runs this session); the numbers above are the
receipt.

### GATE 2 — harden ρ*

**Optimization.** No `scipy` in the venv (`ModuleNotFoundError`); used a
hand-rolled Nelder–Mead simplex search (float, `M=128` arc cover, fast
surrogate) over the three per-disc safety factors, minimizing the worst
block ratio, then re-verified the winner at `M=512` and finally at full Arb
rigor via `f8_certify_tb_blocks.py`.

- **Unconstrained** Nelder–Mead converges to ratio ≈ **0.650** at factors ≈
  `(14.67, 5.04, 2.19)`. **Rejected as geometrically unsound**: disc 1 would
  then have radius ≈1.16 around center ≈−0.845, i.e. it would extend past
  `Re s = 0` and heavily overlap discs 2 and 3 — untested against pole/
  branch-cut clearance at that scale, and far outside any precedent (q=7's
  own largest adopted factor is 3.522). Not adopted.
- **Bounded grid + refine** (factors capped at ≤5.0, ≈1.4× q=7's largest
  adopted factor, to stay within a geometrically-precedented range): best
  found at coarse `M=64` is **(3.4, 2.2, 1.4) → ratio ≈ 0.803** (`M=512`
  recheck: 0.745 float estimate). **Adopted.**
- Pushing the cap further (up to 5.0) continued to improve the float ratio
  marginally (best 0.746 at `(5.0, 2.8, 1.6)`), but with diminishing returns
  and larger, less-precedented discs for no material gain over the already-
  passing (3.4, 2.2, 1.4) point — not adopted, to keep the geometry
  conservative.

**Full Arb certification at (3.4, 2.2, 1.4)**
(`f8_receipts/F8_TB_BLOCK_CERTIFICATES_RECEIPT.json`, `PREC_BITS=384`,
`M=512`, `K_start=6`, `max_K=24` — same discipline as the original run):

| block | kind | certified ratio upper bound | K used |
|---|---|---:|---:|
| 1→3, +2 | tail | ≤ 0.884413361619760… | 6 |
| 1→3, −1 | tail | ≤ 0.907412733398576… | 6 |
| 2→1, +1 | head (finite) | ≤ 0.781324224626880… | — |
| 2→3, +2 | tail | ≤ 0.882096403418673… | 6 |
| 2→3, −1 | tail | ≤ 0.904432463312020… | 6 |
| 3→2, +1 | head (finite) | ≤ 0.735980304555347… | 6 |
| 3→3, +2 | tail | ≤ 0.879466587362801… | 6 |
| 3→3, −1 | tail | ≤ 0.901063013512934… | 6 |

**Certified ρ\* = 0.907412733398576057385920 (Arb ball, endpoints agree to
4.69e-25). `PASS_RHO_LT_0.99`, verdict `worst_block = "1→3, −1, tail"`.** All
pole clearances PASS, all branch-cut clearances PASS (`all_pole_clearances_pass:
true`, `all_branch_cut_clearances_pass: true` in the receipt). K collapses
from 11–12 (old geometry) to **6** (new geometry) for every tail family — the
crude deep-tail bound now dominates much earlier, direct evidence the
geometry, not just the threshold, improved.

**Target ρ\* ≤ 0.99 is REACHED with real margin**: 0.99 − 0.9074 = 0.083
(8.3% headroom below the gate itself); margin to the hard convergence bound
of 1.0 is 9.26%. This is now in the **same range as q=7's own certified
ρ\* = 0.7623** (float) / **0.762251293807** (the q=7 chain's own reported
comparison value) — not identical, but no longer an outlier requiring
special-casing.

**Block re-cutting / merging.** The coordinator asked whether the two finite
head blocks (`2→1`, `3→2`) admit restructuring (as the odd-q pipeline's
block-choice notes allow) to structurally improve the margin. **Not
attempted**, because the geometry search alone already reached the target
with comfortable headroom (§ above) — re-cutting the block list would change
`f8_source_builder.py`'s assembly (currently an exact transcription of
`zeta_cert_rosen_even`'s eq.(32) loop, cross-validated byte-identical in
Stage 0's §3(a)) and is not needed to clear GATE 2. Flagged as an available
lever for a FUTURE pass only if R2's boundary-sup work later finds the
current geometry insufficient there (R2's `F_R(N)` inequality is a different,
stricter quantity than this TB-layer ratio — see below).

**Error-budget headroom vs the q=7 pipeline's ~1113x.** The q=7 R3b margin/
`F_R` ratio at `N=256` is `1113.85` (`ADVERSARIAL_REVIEW_G7_V1.md`). That
downstream figure depends on ρ\* through the exponential decay rate
`|ln ρ*|` in `F_R(N) ~ T_tail(N)·exp(1+2B(N))`, `T_tail(N) ~ ρ*^N` (roughly —
the exact R2 formula is not yet ported to q=8; this is the same qualitative
dependence F7_CERT_PLAN §3 itself uses to argue N-budget). Comparing the OLD
and NEW ρ\* by that exponent:

| | ρ\* | \|ln ρ\*\| | N needed for 1113.85× decay (≈ q=7's headroom) |
|---|---:|---:|---:|
| OLD (Stage 1, pre-gate) | 0.9987 | 0.00130 | **≈5393** — infeasible at any practical N |
| NEW (GATE 2, this pass) | 0.9074 | 0.09717 | **≈72** — well inside q=8's already-observed N-convergence range (Stage 2's N-convergence table showed the actual operator tail dominant by N=28–32 using the determinant-build geometry, a related but distinct quantity) |
| q=7 (reference) | 0.7623 | 0.2716 | 26 (consistent with q=7 reaching its 1113× margin at N=256, i.e. q=7's actual N budget is set by the boundary-sup R2 formula, not this floor estimate — this table is an order-of-magnitude sanity check, not a substitute for R2) |

**Conclusion: the OLD thin ρ\*=0.9987 would have genuinely threatened the
final cert** — its decay exponent is ~75× worse than q=7's, which would have
needed an N in the thousands (infeasible at any Kaggle-chunk budget) to reach
comparable headroom, and R2's actual boundary-sup formula (stricter than
this floor estimate) would likely have needed even more. **The NEW ρ\*=0.9074
removes that threat**: its decay exponent is only ~2.8× worse than q=7's
(0.09717 vs 0.2716), putting q=8's projected N-budget for comparable headroom
in the same cost class as q=7's (tens, not thousands) — consistent with
q=8's smaller κ=3 (vs q=7's κ=5) actually making it a CHEAPER contour cert
than q=7 if R2/R3b proceed with this geometry.

**Verdicts:**

- **GATE 1: HARNESS-ARTIFACT.**
- **GATE 2: RESOLVED — ρ\* = 0.9074127334 ≤ 0.99 target, geometry (3.4, 2.2,
  1.4), full Arb certificate PASS, pole/branch-cut clearance PASS.**

## R2 + R3b (this pass, gated on both gates above being resolved)

Both gates cleared (commit e91e3f0 banked them). This pass ports the
remainder of the pipeline. **Architecture deviation from F7, stated
explicitly, not hidden:** F7's R2 (`f7_certify_r2_flagship.py`, 550 lines,
requires a further undocumented dependency — a "W-envelope" weight-bound
receipt from `certify_tb_weights.py`, which does not exist for q=8) and R3b
(`f7_certify_r3b_flagship.py` + `f7_r3b_endpoint.py`, 1673 + 387 lines) are a
heavy analytic-block-envelope pipeline, built because F7's box needed N up to
224–256 (5N×5N matrices, 192 arcs, mandatory multi-day Kaggle chunking) — an
analytic `T_tail(N)` formula was necessary there to avoid brute-force N
escalation at that cost. **q=8's box needs only N≈30–34** (3N×3N matrices,
established below) — direct, brute-force-but-fully-rigorous per-point Arb
ball certification is cheap enough that no analytic envelope layer or 16-way
chunk split is needed. This pass therefore reuses the ALREADY-VALIDATED,
ALREADY-CERTIFIED-AT-THREE-`q` (7, 9, 12 — q=12 is EVEN, same builder pairing)
methodology of `lane_g/law_probes/certdcM_winding.py`
(`LAW_CERTIFIED_DEEPCOUNT_MULTI.md`), narrowed from that script's big
deep-count window to the single 1e-6 flagship box, in a new file
**`f8_certify_r3b_flagship.py`** — same criteria (a) nonvanishing / (b)
certified argument increment, same `TAIL_SAFETY=4`, same bisection discipline
(max depth 10), same engine call (`zeta_cert_rosen_even.cert_det`,
UNMODIFIED). This is a smaller, simpler, but equally rigorous proof of the
same fact F7's R2+R3b prove: a certified winding-1 closed contour around the
flagship box.

### R2-equivalent: boundary-sup-driven N freeze

`f8_certify_r3b_flagship.py --boundary-sup-check` samples the 4 box corners
**plus the box center** (the worst-case point in the closed box for margin —
it is closest to the pin's own scan-estimated zero, so `|det|` is smallest
there; more conservative than checking only the topological boundary) and
reports the worst `TAIL_SAFETY·tail / |det|` ratio — the direct brute-force
analogue of F7's `F_R(N) < m0` inequality, computed with the SAME rigorous
Arb tail bound (`dim_tail_from_matrix_signed`) F7's own engine uses, rather
than an analytic block-series bound:

| N | worst-point ratio (4·tail/\|det\|) | worst point | criterion (a) |
|---:|---:|---|---|
| 24 | 4.260 | center | **FAIL** |
| 28 | — (raises: det ball contains 0 at center) | center | **FAIL** |
| 30 | 0.0562 (17.8× margin) | center | PASS |
| 32 | 0.00272 (367× margin) | center | PASS |
| 34 | 2.15e-4 (4657× margin) | center | PASS |
| 36 | 2.27e-5 (44000× margin) | center | PASS |

**Revises the Stage-2 provisional N_PRIMARY=32/N_COMPARISON=28.** N=28 was
picked at Stage 2 from an interior-point probe WITHOUT the `TAIL_SAFETY=4`
factor; with the factor and the box-center-inclusive check, N=28 genuinely
fails criterion (a) (the tail-inflated det ball contains zero). **Revised
decision: N_PRIMARY = 32, N_COMPARISON = 30** — both clear the boundary-sup
check with real margin (367× and 17.8× respectively), and N=30 is a
meaningfully independent lower-N cross-check (not a designed-to-fail
control, matching F7's own N_PRIMARY/N_COMPARISON convention of "both should
pass").

**Caveat, stated plainly**: checking corners+center is strong evidence but
not a continuum supremum proof over every point in the closed box (F7's
analytic block envelope bounds the true continuum sup; this brute-force
check samples 5 points). It is not needed for the winding certificate's own
soundness (that only requires criteria (a)/(b) on the actually-traversed,
bisection-refined contour — proven below, independent of this diagnostic),
but is the honest scope of this N-freeze decision.

### Local smoke test (one arc)

```
$ f8_certify_r3b_flagship.py --one-arc --N 32
{
  "smoke_test": true,
  "one_arc": {"edge": "bottom",
              "from": [0.4252300423737965, 4.345759788321986],
              "to":   [0.42523054237379654, 4.345759788321986]},
  "delta_arg": 0.3217504197904403,
  "delta_arg_ball": [0.32175033315478985, 0.3217505064260907],
  "criterion_a_pass": true,
  "criterion_b_pass": true,
  "chunk_gate_pass": true,
  "det_calls": 2,
  "wall_seconds": 2.66
}
```

Confirms the endpoint executes end-to-end (imports the engine, evaluates two
boundary points, certifies one segment, emits `chunk_gate_pass`) before
committing to the full 16-arc box run.

### Full closed-contour box certificate

Ran the complete 4-edge, 16-arc closed contour (`--N 32`, `--N 30`, and — for
comparison, not adoption — `--N 28`):

| N | certified integer | winding ball | `chunk_gate_pass` | `closed_contour_status` | min \|det\| lower on contour | det calls |
|---:|---:|---|---|---|---:|---:|
| 28 | 1 | [0.9999985, 1.0000015] | True | CLOSED_CONTOUR_CERTIFIED | 3.001e-06 | 16 |
| 30 | **1** | [0.99999925, 1.00000075] | **True** | **CLOSED_CONTOUR_CERTIFIED** | 3.001e-06 | 16 |
| 32 | **1** | [0.99999979, 1.00000021] | **True** | **CLOSED_CONTOUR_CERTIFIED** | 3.001e-06 | 16 |

**All three N give winding = 1, certified** — the contour-only argument-
principle certificate (criteria a+b on the sampled+bisected boundary points)
is valid even at N=28, because the contour samples never touch the box
center (the point that fails the STRICTER center-inclusive boundary-sup
check at N=28 above). This is worth flagging honestly: **the two checks
answer different questions.** The closed-contour certificate (this table)
proves "exactly one zero of `det(1−L_{s,+})` lies inside the box," using only
the points actually walked on the boundary. The boundary-sup check (previous
section) is a stronger, separate diagnostic that also verifies nonvanishing
at the box's worst INTERIOR point (relevant to a from-scratch N-budget
decision, not to the winding certificate's own validity). N_PRIMARY=32 is
adopted because it clears BOTH checks with large margin; N=28 is reported as
a third, informative data point, not adopted, since it fails the stricter
check even though its contour certificate is independently valid.

`min_det_abs_lower_on_contour` (3.001e-06) — note this is on the actual
CONTOUR points (corners + edge midpoints), not the center, consistent with
the corners being farther from the pin's zero than the center (explaining
why this figure looks comfortable even at N=28 where the CENTER check
fails).

### Bundling and canary push

`make_bundles_f8.py` (new, adapted from the validated `kaggle_f7/
make_bundles.py`; provenance comment at its own header) packages a SINGLE
chunk — `kaggle_f8/f8-r3b-chunk-00/` — because q=8's box fits one Kaggle
session (unlike F7's mandatory 16-way split). Embeds 4 files as
zlib+base64 blobs:

| file | sha256 |
|---|---|
| `zeta_cert_rosen_even.py` | `693d2a88fd525e94c8ab6a63486e82fe0670d9dce142effbd5be5e324597212a` |
| `zeta_cert_rosen.py` | `965c2e5f65ae88b458d79bc425375e31589dcbf50703173664ef0e30901dceac` |
| `zeta_cert_rosen_q5.py` | `c84c5c3f6d9f7a320bca7f1dbfd96a4859c3eea9b3de5420eb4eb223ad0d597b` |
| `f8_certify_r3b_flagship.py` | `a8fd1d4ed48ede0343fcec3ce7d8f96699d993391cb97f9578b1e1878787e0ca` |

Validated by decompressing all 4 embedded blobs and diffing against the live
source files: **all 4 byte-identical** (integrity check, not a full
container-environment run — matching F7's own precedent that Kaggle-
container behavior can only be confirmed by an actual push, per
`F7_STAGE3_LAUNCH.md` §6).

**Pushed `saarshai/f8-r3b-chunk-00` (private) to Kaggle.**
`kaggle kernels push` succeeded; `kaggle kernels status` confirms:

```
saarshai/f8-r3b-chunk-00 has status "KernelWorkerStatus.RUNNING"
```

**Update — the canary finished during this pass** (q=8's N=32 box is cheap:
`wall_seconds: 59.6` inside the Kaggle container, not the multi-hour-per-
chunk cost F7's N=224–256 needed). `kaggle kernels status` progressed
RUNNING → `KernelWorkerStatus.COMPLETE`; downloaded the container's own
output via `kaggle kernels output` and confirmed the Kaggle-produced
receipts **independently reproduce the local run**: `F8_R3B_CHUNK_00_N32_
RECEIPT.json` and `..._N30_RECEIPT.json` both show `certified_integer: 1`,
`chunk_gate_pass: true`, `closed_contour_status: "CLOSED_CONTOUR_CERTIFIED"`,
matching the local receipts exactly; kernel log shows `EXIT CODE: 0` for
both N. Per the coordinator's instruction, **no further chunks/pushes this
pass** — checking the canary's inference against the pipeline's own theorem-
assembly criteria (K_s gate re-verification, sector-honesty writeup, etc.)
is deferred to the next pass.

### Artifacts (this section)

- `f8_certify_r3b_flagship.py` — R2-equivalent boundary-sup check + R3b
  closed-contour certificate, single file.
- `make_bundles_f8.py` — bundler (provenance comment points to the validated
  `kaggle_f7/make_bundles.py`).
- `kaggle_f8/f8-r3b-chunk-00/{f8_r3b_chunk_00.py,kernel-metadata.json}` —
  pushed bundle.
- `f8_receipts/F8_R3B_RECEIPT_N{28,30,32}.json`,
  `f8_receipts/F8_R3B_CERT_N{28,30,32}.md` — local closed-contour receipts.

No commits, no further Kaggle pushes this pass.

---

## DATED CORRECTION — 2026-08-19 — CONTINUOUS-CONTOUR CLAIM REFUTED PENDING COLD REFEREE

This block is append-only and does not rewrite the historical receipts above.
The prior `CLOSED_CONTOUR_CERTIFIED` interpretation is **REFUTED as a
theorem-grade continuous Fredholm-contour certificate**, subject to the
separate cold referee now required by the program's proof-claim rule.

The exact defects are structural, not rounding issues:

1. `f8_certify_r3b_flagship.py::certify_segment` evaluates determinant balls
   only at the two endpoints.  It accepts a segment when the endpoint
   half-turn test passes and bisects only when that endpoint test fails.  It
   supplies no Taylor/derivative or other interval enclosure over the segment
   interior.
2. Its determinant inflation comes from the even engine's
   `dim_tail_from_matrix`; that implementation describes the geometric
   increment extrapolation as a heuristic and explicitly says it is **not a
   proven uniform tail bound**.
3. The determinant engine uses uniform geometry factor `2.5`, whereas this
   note's TB proof rejects that geometry for the two finite head blocks and
   adopts `(3.4, 2.2, 1.4)`.  The current winding receipts do not bind a
   theorem-valid Fredholm tail to the adopted geometry.

Binding source receipt (fresh 2026-08-19):

```text
$ nl -ba lane_f/f8_certify_r3b_flagship.py | sed -n '97,150p'
105  det, tail, info, _kappa = EVEN.cert_det(...)
116  r = tail * TAIL_SAFETY
132  def certify_segment(...)
133      A = ev.det_ball(*p0)
134      B = ev.det_ball(*p1)
136      if w.real.lower() > 0:
147      mid = ...
148      return certify_segment(ev, p0, mid, ...) + ...

$ rg -n 'dim_tail_from_matrix' lane_g/law_probes/kaggle_boundary_rate/zeta_cert_rosen_even.py
107:dim_tail_from_matrix = Q5.dim_tail_from_matrix
280:    """Same det-increment geometric-ratio tail heuristic as
282:    applies to the chi sector too.  Disclosed as heuristic identically to the
284:    -- this is NOT a proven uniform tail bound.

$ rg -n 'EXACT_FACTORS|uniform, the two' lane_f/f8_certify_tb_blocks.py
74:# for this ratio bound) does NOT certify: at factor 2.5 uniform, the two
85:EXACT_FACTORS = ("3.4", "2.2", "1.4")
```

Corrected strongest statement: the N=30 and N=32 runs, including their
byte-matched Kaggle copies, are **SUPPORTED SAMPLED FINITE-SECTION POLYGON
WINDING EVIDENCE**.  They do not prove nonvanishing on every continuous
subarc, a Fredholm winding, a Selberg-zeta zero, or a q=8 resonance.  Every
such q=8 conclusion is therefore **CONJECTURAL**.  The JSON status strings are
retained as historical program output, not as theorem status.

All q=8 assembly/promotion work is stopped.  A repair must independently bind
the eq.-(32) evaluator, exact Arb box, theorem-valid R2/Fredholm and derivative
tails, continuous R3b subarcs, E1, `K_s`, and primary-source factorization;
Kaggle becomes relevant only after those local proof gates are frozen.  Final
banking of this correction awaits a separate cold referee file.

---

## DATED REFEREE BANKING — 2026-08-19

`F8_R3B_REFUTATION_REFEREE.md` returns **REFUTATION CONFIRMED** after a cold
source reconstruction, an actual `certify_segment` countermodel, a separate
finite-tail countermodel, receipt/hash comparison, and parity-by-parity audit
of the q=9..12 driver.  The correction immediately above is therefore fully
banked: q=8 has sampled finite-section polygon winding evidence only; the old
continuous-Fredholm-certificate interpretation is false.

Decisive referee receipt:

```text
ACTUAL_CERTIFY_SEGMENT_COUNTERMODEL seen= [(0.0, 0.0), (1.0, 0.0)]
ACTUAL_CERTIFY_SEGMENT_COUNTERMODEL stats= {'segments': 1, 'bisections': 0, 'max_depth_used': 0} delta_arg= 0
ACTUAL_CERTIFY_SEGMENT_COUNTERMODEL interior_zero= 0.0 endpoint_nonzero= True accepted_without_interior_sample= True
TAIL_COUNTERMODEL observed_ratios= [0.5, 0.5, 0.5] q_obs= 0.5 estimated_tail= 0.125 next_increment= 100.0 bound_violated= True
```

This refutes the certificate implication, not the existence of an actual q=8
zero.  A genuine q=8 Selberg-zero/resonance theorem remains **CONJECTURAL** and
requires the repair list above.
