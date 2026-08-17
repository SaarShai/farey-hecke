# F8 CERT PLAN — q=8 off-line resonance certificate (run plan)

Lane F, 2026-08-17. EVEN-q analogue of `F7_CERT_PLAN.md`. This pass covers
**Stage 0–2 ONLY** (source builder port, TB block certification, N-convergence
probe) — local, no Kaggle, no R2 envelope, no R3b winding, no bundling. R2 /
R3b / `kaggle_f8/` / canary are gated on judging this pass, per coordinator
scope confirmation (this session, following commit 1f2b578 which banked
`make_bundles.py` and the box-selection work).

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
