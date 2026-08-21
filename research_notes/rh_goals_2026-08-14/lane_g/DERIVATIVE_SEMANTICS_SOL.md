# Derivative semantics of the q8 Taylor-box gate — SOL

Lane: derivative-semantics (lane_g). Date: 2026-08-20.
Branch: `codex/prime-step-review-economic-validation`.
Interpreter: `/Users/za/.venvs/farey-rh/bin/python` (python-flint / Arb, prec 384).
Files audited (READ-ONLY, nothing edited, nothing committed):
`research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py`,
`research_notes/rh_goals_2026-08-14/lane_f/q8_r3b_engine.py`,
`research_notes/rh_goals_2026-08-14/lane_g/kaggle_q8_subdivision/shard_receipts/SHARD_a2_l64-128.ckpt.json`.

**Headline verdict: (a) SOUND-CONSERVATIVE.** The gate bounds exactly the
quantity it mathematically requires — the true logarithmic derivative
`d/du log det(I - C(s))` along the arc, carrying the *arc* inverse
`A(s)^{-1}`, not the anchor `A0^{-1}`. The 12 banked PASS leaves stand.
The measured conservatism is **127.55x**, and it is localised entirely to
one factor (`correction_inverse`, line 976). The 128x/90-degree anomaly of
the previous lane is **not a property of the gate at all** — it was a
broken probe. And the conservatism is **super-quadratic in the leaf
radius**, which makes **depth 8**, not depth 9, the sufficient re-shard.

---

## 1. The bound the checker mathematically requires

Fix a closed leaf `[start, end]`, midpoint `s0`, half-length `r`, unit
direction `e = ds/du` (`segment_direction`, `|e| = 1`). Put

```
A(s) = I - C(s),   A0 = A(s0),   D(s) = det A(s),   phi(u) = D(s0 + u e).
```

`C` is analytic on a neighbourhood of the leaf, so `phi` is analytic on
`|u| <= r`. Jacobi's formula gives

```
phi'(u) = phi(u) * tr( A(s)^{-1} dA/du ) = -phi(u) * e * tr( A(s)^{-1} C'(s) ).      (1)
```

So the derivative the checker needs is the **logarithmic derivative of the
determinant carrying the true inverse `A(s)^{-1}`**, evaluated (or
enclosed) over the whole leaf. It is *not* `tr(A0^{-1} C'(s0))`, which is
only the value of (1) at the single point `u = 0`.

Let `H` be any bound with

```
|tr( A(s)^{-1} dA/du )| <= H   for all s on the leaf.                               (2)
```

Set `M = sup_{|u|<=r} |phi(u)|`. From (1), for any `u`,
`|phi(u) - phi(0)| = |int_0^u phi'| <= r H M`, hence `M <= |phi(0)| + r H M`, so
provided `rH < 1`,

```
M <= |phi(0)| / (1 - rH),   and   |phi(u) - phi(0)| <= r H |phi(0)| / (1 - rH).      (3)
```

(3) is the **first-order-with-remainder inequality the checker needs**: a
Gronwall-closed mean-value bound, valid for every `u` on the leaf. The
enclosure is `det(I-C(s)) in phi(0) + disc( rH|phi(0)|/(1-rH) )`, and the
leaf certifies (zero excluded) iff that disc misses 0, i.e. iff

```
rH / (1 - rH) < 1    <=>    rH < 1/2.                                               (4)
```

### Does the implementation use the anchored factorization wrongly?

No — and this is the crux the correction block flagged. The anchored
factorization is exact:

```
A(s) = A0 - (C(s) - C(s0)) = A0 ( I - A0^{-1} dC(s) ),   dC(s) = C(s) - C(s0),
=>  A(s)^{-1} = ( I - A0^{-1} dC(s) )^{-1} A0^{-1}.                                 (5)
```

Substituting (5) into (2) gives precisely

```
tr( A(s)^{-1} dA/du ) = tr( (I - A0^{-1} dC)^{-1} A0^{-1} (-e C'(s)) ),             (6)
```

which is what lines 973-979 assemble. **`tr(A0^{-1} C')` is not used as the
gate quantity.** It is the `correction_inverse = 0` truncation of (6); the
implementation composes it correctly with the missing factor.

---

## 2. Line-by-line audit of `arc_certificate` (lines 885-1005)

| line | expression | role in (2)-(4) | verdict |
|---|---|---|---|
| 890 | `radius = |end-start|/2` | `r` | correct |
| 891/895-899 | `cprime_arc` on `segment_box(start,end)` | interval enclosure of `C'(s)` over the leaf | sound (box contains the segment) |
| 901-902 | `A0 = I - c_mid`, `A0_inverse` | anchor of (5) | sound |
| 908-913 | `delta[i,j] = disc(radius * |cprime_arc[i,j]|)` | entrywise enclosure of `dC(s)`; `|dC_ij| <= r sup|C'_ij|` by the segment integral | sound; the disc (not `acb(0,B)`) is the correct 2-D inflation, as the comment states |
| 914-916 | `normalized_delta = A0^{-1} delta`, `qOp` | `||A0^{-1} dC||_2` bound | sound |
| 918 | gate `qOp < 1` | invertibility in (5) via Neumann | sound |
| 975-976 | `correction = I - normalized_delta`, `.inv()` | the `(I - A0^{-1}dC)^{-1}` factor of (5)/(6) | sound: Arb's verified LU encloses the inverse of **every** matrix in the interval box, or fails loudly (it returned "matrix is singular" in probe R1, so it is not silently over-trusting) |
| 973-974, 977-978 | `direction`, `-e C'`, `A0^{-1}(-eC')`, `corr^{-1} * (...)` | assembles (6) in the correct order `corr^{-1} A0^{-1} (dA/du)` | **correct composition** |
| 979 | `H = |sum of diagonal|` | `H` of (2) | sound (trace of an enclosure encloses the trace) |
| 980-981 | `rH`, gate `rH < 1` | hypothesis of (3) | sound |
| 984 | `radius*H*|det_mid|/(1-rH)` | remainder of (3) | **exactly (3)** |
| 987-989 | `inflate(midpoint_det, taylor_radius)`, `abs_lower > 0` | the enclosure and criterion (4) | sound |

**The assembled inequality is VALID.** No missing division by `det` (the
`|det_mid|` factor in line 984 is exactly the `phi(0)` of (3)); no missing
direction factor (line 973 supplies `e`, and since `|e| = 1` it cannot
change `H` at all — so the **90-degree phase clue is a red herring for the
gate**: `H` is a modulus and is direction-blind).

---

## 3. Numeric receipts

Probes: `dsem.py`, `dsem2.py`, `dsem3.py`, `dsem4.py` (scratchpad;
Arb prec 384). Target: leaf 64 of arc 2 = record 0 of
`SHARD_a2_l64-128.ckpt.json`, `s_mid = 0.42523103456129652 + 4.3457617883219859 i`,
`radius = 7.8125e-9`.

### 3.1 The previous lane's "1.28e8 pure real" is REFUTED

At `N = 48`, through the production code path
(`build_q8_block_matrices_and_s_derivative` -> `schur_value_and_derivative`):

```
det(I-C(s_mid))         = -4.6918866299e-7 + 2.9642223862e-6 i
-tr(A0^-1 C'_mid)       = -7813.6510392 - 999939.2373226 i   (|.| = 999969.765)
FD dlogdet/ds, h=1e-11  = -7813.6510392 - 999939.2373226 i
FD dlogdet/ds, h=1e-12  = -7813.6510392 - 999939.2373226 i
```

The analytic trace and the end-to-end finite difference of
`det(I-C(s))` agree to **~1e-19 relative**. Entrywise FD of the **Schur**
`C'` (not just the blocks) against `cp`, entries (0,0),(1,3),(5,5),(20,7),(47,47):
ratio `= 1` to `~1e-24` relative, imaginary part `~1e-25`. So
`schur_value_and_derivative`'s product rule is correct too, and
`tr(A0^{-1}C'_mid)` is `~1.0e6`, **matching** the finite differences of the
64 certified `midpoint_det` values (recomputed independently in true `s`
units, not per-leaf-index: leaf 1 gives `-23426 - 999451 i`, `|.| = 9.997e5`;
leaf 31 `8.97e5`; leaf 62 `7.15e5`).

There is therefore **no 128x and no 90-degree discrepancy in the
mathematics**. The prior probe's `1.28000000605e8` is an artifact:
`1/radius = 1/7.8125e-9 = 1.28e8` exactly. Its "essentially pure real"
character matches the real part of the true trace being `-7813.65` while
the imaginary part carries the magnitude — i.e. the probe reported a
radius-scaled quantity, not a trace. The det value it was compared against
is independently confirmed: `N = 48` reproduces the `N = 262` receipt's
`midpoint_det` to 10 significant figures.

### 3.2 Where the conservatism actually lives (attribution)

Same leaf, `N = 48`, reproducing the production assembly step by step:

| quantity | value | ratio to true `|tr_mid|` |
|---|---:|---:|
| A. `|tr(A0^-1 C'_mid)|` (truth at midpoint) | 9.99970e5 | 1.000000 |
| B. `|tr(A0^-1 C'_arcbox)|` (arc-box `C'` only) | 1.000008e6 | **1.0000381** |
| C. production `H` (adds `correction^-1`) | 1.2754593e8 | **127.5498** |
| receipt `H` at `N = 262` | 1.2754605e8 | — |

Two consequences, both receipted:

1. The `N = 48` reconstruction reproduces the `N = 262` production `H` to
   **6 significant figures** (1.2754593e8 vs 1.27546049e8), plus `qOp`
   0.6544379 vs receipt 0.6544379. The small-`N` probe is a faithful proxy.
2. The arc-box enclosure of `C'` costs **0.0038%**. **100% of the 127.55x
   is the `correction_inverse` factor** (line 976) — i.e. the enclosure of
   the `(I - A0^{-1}dC)^{-1}` term of (5), whose *true* contribution at the
   midpoint is exactly zero.

Mechanism (CONJECTURAL as an explanation, but consistent with the numbers):
the true trace `~1e6` is a near-total cancellation across 262 diagonal
entries of `A0^{-1}C'`, whose individual magnitudes are orders larger. The
interval product with `corr^{-1}` destroys that cancellation, and the
resulting bound sits at roughly the Frobenius-product level
`||corr^{-1}A0^{-1}dC||_F * ||A0^{-1}C'||_F`. This is a **structural
limit of norm-type bounds on a cancelling trace**, not a calibration
constant and not a code defect.

### 3.3 The conservatism is super-quadratic in the radius — depth 8 suffices

The `correction^{-1} - I` term carries `dC`, which is itself `O(radius)`.
So `H ~ H_true + c*radius`, hence `rH ~ r*H_true + c*r^2`: halving the
leaf should cut `rH` by ~4x, not 2x. Measured, same leaf, `N = 48`, full
production gate including the zero-exclusion test of (4):

```
depth 7 (leaf 0)  r=7.8125e-09  qOp=0.6544  H=1.275459e8  rH=0.996453  EXCLUDES_ZERO=False
depth 8 left half r=3.9063e-09  qOp=0.3272  H=4.843844e7  rH=0.189213  EXCLUDES_ZERO=True
depth 8 right half r=3.9063e-09 qOp=0.3272  H=4.857887e7  rH=0.189761  EXCLUDES_ZERO=True
rH ratio depth7/depth8 = 5.266 / 5.251     (4.0 = quadratic; measured is better)
```

The observed 5.26x beats the quadratic prediction because `1/(1-qOp)`
also relaxes (0.654 -> 0.327). **The worst open leaf of the shard passes at
depth 8 with `rH = 0.189`, a 2.6x margin below the `rH < 1/2` threshold
of (4).**

---

## 4. Verdict and its consequences

**(a) SOUND-CONSERVATIVE.** Proofs: section 1 (derivation), section 2
(line-by-line correspondence), section 3.2 (attribution). Specifically:

- The 12 banked PASS leaves **stand**. Their certificates use a valid
  enclosure of the required quantity; being conservative can only make a
  PASS harder, never spurious. No shard receipt is invalidated, no
  re-run is forced for soundness reasons.
- The `ZERO_EXCLUSION_DIAGNOSIS_SOL.md` correction block's open question
  is **answered in favour of the gate**: it carries the true arc inverse,
  not the anchor. Its premise ("the engine's two outputs ... are mutually
  inconsistent") is withdrawn — one of the two outputs was a broken probe.
- The `H`-tightening recommendation of that document's section 2.4/5.4,
  already withdrawn, stays withdrawn *for its original reason but not
  its stated one*: `H` is a faithful evaluation of the correct formula,
  and there is a real 127.55x of enclosure slack in it, but that slack is
  a structural norm-bound limit, not a loose constant.

**Cost of the unlock (CONJECTURAL — measured at `N = 48`, not yet at
`N = 262`).** Since `certify_adaptive` only splits leaves that fail, the
route is a `max_depth` bump 7 -> 8, not a re-shard: banked PASS leaves are
untouched by the recursion, and only the OPEN leaves take one extra split
(2 evaluations each). Against `ZERO_EXCLUSION_DIAGNOSIS_SOL.md`'s table,
where depth 9 was costed at 99 h and depth 7 at 24.7 h, depth 8 is the
midpoint of that geometric ladder, `~50 h` for the closed contour, i.e.
**about half the depth-9 backstop** — and unlike the withdrawn
`H`-tightening route it requires **no engine change at all**. The
`params` field of the checkpoints still changes with `max_depth`, so the
68-leaf (~3.3 h) receipt invalidation noted there still applies.

Not claimed: that every leaf of every arc passes at depth 8. Only the
worst-`rH` leaf of `SHARD_a2_l64-128` was tested, and only at `N = 48`.
Leaves nearer the pin centre have larger `H_true`. The `rH ~ a*r + b*r^2`
model plus the recorded per-leaf `rH` gives a per-leaf prediction, but it
is a model, not a certificate.

---

## 5. Repair spec (SPEC ONLY — `lane_f` NOT edited)

Two independent items. Item A is the cheap, no-code route and is
**recommended**; item B is the engine change and is optional.

### A. `max_depth` 7 -> 8, no engine change

- Change: the `--max-depth` argument of the shard driver only.
- Justification: section 3.3, criterion (4).
- Gate to watch: `rH_upper < 0.5` per leaf (the *real* pass threshold;
  the code's `rH < 1` gate at line 981 is only the hypothesis of (3), and
  a leaf with `0.5 <= rH < 1` will pass that gate and still fail
  `finite_taylor_excludes_zero`). Recording `rH` is already done, so the
  existing receipts are enough to predict the next depth.
- Pre-flight (cheap, recommended before spending 50 h): rerun the
  `dsem4.py` half-split probe at `N = 262` on the two or three
  largest-`rH` OPEN leaves across all arcs. That converts the CONJECTURAL
  cost estimate into a measured one for ~3 leaf evaluations.

### B. Optional tightening of `H` — recover the cancelling trace

Target: replace `H` by a bound closer to `|tr(A0^{-1}C'_arc)|` (test B
above, only 1.0000381x above truth) plus an explicitly-bounded correction,
instead of enclosing the whole product. Using (5),

```
tr(A(s)^{-1} dA/du) = -e * [ tr(A0^{-1} C'(s)) + tr( (corr^{-1} - I) A0^{-1} C'(s) ) ]
                    = -e * [ T1(s) + T2(s) ],   corr^{-1} - I = corr^{-1} A0^{-1} dC.
```

- `T1` is already computed tightly on the arc box (test B). Keep it as an
  interval scalar; do **not** route it through `corr^{-1}`.
- `T2` needs a bound that does not multiply two Frobenius norms of
  non-cancelling matrices — that product is what currently costs 127x.
  Candidate: `|tr(XY)| <= ||X||_2 * ||Y||_*` with `X = corr^{-1}A0^{-1}dC`
  (`||X||_2 <= qOp/(1-qOp) = 1.894` from the existing `inv_arc`/Neumann
  machinery, no new certification needed) and `Y = A0^{-1}C'`, whose
  **nuclear** norm must then be certified. This is the open piece: a
  rigorous nuclear-norm bound on `A0^{-1}C'` is not currently available in
  the codebase, and if it is estimated by `sqrt(N)*||.||_F` the result is
  *worse* than the present bound. **Do not implement B on the
  `sqrt(N)*Frobenius` route.**
- Certifying `(I-C(s))^{-1}` directly on the arc box (the obvious
  alternative) is **REFUTED for this leaf**: probe R1 built
  `A_arc = I - C(s_arc)` and called `.inv()`; Arb returned *"matrix is
  singular"*. The arc-box entries carry `~5e-6` dependency inflation
  (`A_arc[0,0] = [0.16182 +/- 4.4e-6] + [0.06020 +/- 5.0e-6] i` against the
  midpoint's `0.161816356... + 0.060195774... i`, exact to 1e-110), which
  is far too wide to verify invertibility. This vindicates the anchored
  split of lines 901-914 and closes the "just use the true inverse"
  suggestion of the correction block: the true inverse is **not
  rigorously enclosable** at this leaf width, which is precisely why the
  anchored form exists.

Conclusion on B: it is a research task with an unresolved sub-problem
(rigorous nuclear-norm bound), whereas A is a one-flag change with a
measured 2.6x margin. **Ship A; leave B parked.**

---

## 6. What is NOT claimed

- The depth-8 sufficiency is measured at `N = 48` on one leaf and is
  CONJECTURAL at `N = 262` and across all arcs.
- The `~50 h` figure is interpolated from `ZERO_EXCLUSION_DIAGNOSIS_SOL.md`'s
  own cost ladder, not re-measured here.
- The cancellation mechanism of section 3.2 is an explanation consistent
  with the numbers, not a proof.
- No claim about the location of the determinant zero is made or used; the
  soundness verdict does not depend on it.
- No file under `lane_f` was edited. Nothing was committed or pushed.

READY FOR JUDGING

---

## Dated correction block (2026-08-21, referee defects 1–6, append-only)

Applied per DERIVATIVE_SEMANTICS_REFEREE.md (verdict GAPS NOT REFUTED;
CONDITIONAL GO; the load-bearing mathematics (a1-a3), (b), (c), (e) and
the depth-8 measurements reproduced exactly, (d2) strengthened to the
true worst leaf):

- **D1 (threshold REFUTED)**: eqn (4)'s / §4 / §5A's "real pass
  threshold rH < 1/2" is WRONG — inflate() builds a SQUARE box, so
  zero-exclusion is guaranteed only for rH < 1/(1+sqrt(2)) =
  0.41421...; six OPEN leaves of SHARD_a2_l64-128 with rH in
  (0.4375, 0.4982) — all below 1/2 — have excludes_zero = False
  (referee's square-box predictor matched the receipt 10/10 on
  straddling leaves).  ZERO_EXCLUSION_DIAGNOSIS_SOL.md:56's
  mu/(1+mu) ∈ [0.4142, 0.5] was right and takes priority.
- **D2 (worst leaf)**: §3's "worst failing leaf rH = 0.9965" audited
  record 0 = the LOWEST-rH failing leaf; the shard maximum is
  rH = 1.0290323 at path [1,0,0,0,1,1,1] (record 7).  Harmless in
  outcome: the referee verified the true worst also clears depth 8
  (children rH = 0.194449 / 0.194463, EXCLUDES_ZERO = True).
- **D3 (margin)**: the depth-8 margin against the CORRECT threshold is
  2.13x (0.41421 / 0.19446), not 2.6x.
- **D4 (cost mechanism REFUTED)**: the production driver
  q8_leaf_shard.py is uniform-depth by construction and params-bound to
  --depth — no depth-7 checkpoint resume, no per-open-leaf splitting.
  Correct restart scope: 1024 fresh uniform depth-8 leaves ≈ 535 CPU-h
  ≈ 45-50 wall-h at 12 workers; all banked depth-7 PASS receipts
  unusable for resume.
- **D5 (headline)**: line 19 / §3.3's flat "depth 8 sufficient" is
  demoted to §6's correct hedge: MEASURED-ON-SAMPLES (2 of 512 depth-7
  leaves' children measured by the author, +2 by the referee incl. the
  true worst; arcs 0/1 largely unmeasured; a further failing leaf found
  at a3 path [0,1,0,1,0,1,0], rH = 0.695).  Screen rule: depth-7
  rH > 4 x 0.41421 ≈ 1.66 predicts failure to clear depth 8 (none
  observed; max 1.029).
- **D6 (minor)**: §1's "disc |u| <= r" — only the real interval is
  enclosed (sound as used); §3.1's "1/radius exactly" is 8 s.f. with an
  unexplained residue and the probe source absent from the repo; "12
  banked PASS" was stale (36 exist: a0 4/4, a2 8/64, a3 12/12-partial).
