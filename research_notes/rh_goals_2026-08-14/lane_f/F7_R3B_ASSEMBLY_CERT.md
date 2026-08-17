# VERDICT: THEOREM-GRADE closed-contour YES at N=256 (q=7, assembled from 16 chunks)

Run status: `complete`. All seven assembly gates PASS.

Assembly of the 16 banked Kaggle chunk receipts into one closed-contour
verdict for the 192-arc boundary of the q=7 pin box. The chunked runs deferred
the winding to merge ("chunked run: not a closed cycle, winding deferred to
merge"); this document supplies the merge, the seam-closure re-verification the
cert plan flags as REQUIRED, and the global gate.

Producer: `kaggle_f7/assemble_f7.py` — sha256
`8e52840ecd6974d9e4ec079cddbed5b1505f619acff116ac8f4d2d8a957d4b0f` (recorded
live in `F7_R3B_ASSEMBLY_RECEIPT.json:/assembly_script_sha256`). The winding and
adjacent-box closure test are NOT re-implemented here: the script imports and
calls `f7_certify_r3b_flagship.merge_chunks_and_verify_closure` and
`certified_winding_via_overlap_polygon` — the pinned orchestrator's own
routines, the same code the 16 chunks were certified with. Machine-readable
receipt: `F7_R3B_ASSEMBLY_RECEIPT.json`.

## 1. Constants and provenance

- Arithmetic: python-flint Arb/Acb at `384` bits (identical in all 16 chunks).
- Flagship s-box: center `0.4751647621098225 + 4.668743786424289 i`
  (`g7_pin_1`, mms+), coordinate half-width `1e-6`.
- Operator: q=7, sign `+1`, κ=5, 19-block eq.(34) assembly, engine head split
  `4`; exact radius strings `3.522`, `2.622`, `2.372`, `1.79`, `1.6`.
- Closed cover: `4*48=192` base arcs; primary `N=256` (matrix `1280×1280`),
  arithmetic/failure comparison `N=224` (`1120×1120`).
- Chunking: `16` chunks × `12` base arcs, `--workers 4`, max subdivision depth
  `8`, max arc evaluations `1536` per chunk.
- Immutable R2 receipt required sha256
  `4e5f0105e80f6f4fc0e173750abc628534bbc944928f759b1cf3e12bb9202efc`; consumed
  unchanged in all 16 chunks: `True`; equals the orchestrator's
  `R2_EXPECTED_SHA256` pin: `True`.
- Immutable TB V2 receipt required sha256
  `93baddf565b2dca6e94da441a9d7e906ab81576c4acf3506ab334bcf1251f4f6`; consumed
  unchanged in all 16 chunks: `True`; equals the orchestrator's
  `TB_V2_EXPECTED_SHA256` pin: `True`.
- R2_receipt: `lane_f/f7_receipts/F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json` — sha256
  `4e5f0105e80f6f4fc0e173750abc628534bbc944928f759b1cf3e12bb9202efc`.
- TB_V2_receipt: `lane_f/f7_receipts/F7_TB_BLOCK_CERTIFICATES_RECEIPT.json` —
  sha256 `93baddf565b2dca6e94da441a9d7e906ab81576c4acf3506ab334bcf1251f4f6`.
- attempt1_report: `lane_f/F7_PILOT2_REPORT.md` — sha256
  `2bbebd689de07814ed888aab0998c24d70539b12712dcfd50615c4f1dda24e30`.
- R1_restatement: `lane_f/F7_TB_R2_RECEIPTS.md` — sha256
  `02230ad94f4480659d2b5b0ffbdaaa99a01a7b6c0557a907c752c59c51e20ba7`.
- engine: `.worktrees/aletheia-restore/code/zeta_cert_rosen.py` — sha256
  `b6ee87fd8f35f0b704323a1f4c0f7d1c510b5ac6c79a0d6dbf58c95d70e28a0f`.
- R2_code: `lane_f/f7_certify_r2_flagship.py` — sha256
  `56d30d4771a832998c790096fba8026b7ecbd6257d443d29733c1db12fbb296f`.
- R3b_orchestrator: `lane_f/f7_certify_r3b_flagship.py` — sha256
  `df9873d9f1e47c47f2e846d38d906f8f77619a17871e6d7c6da8c225bb63f687`.
- R3b_derivative: `lane_f/f7_r3b_engine.py` — sha256
  `661a4d2b132d1821d18499a302f58805bf7565e560d8f1520379dde156bc7d1a`.
- R3b_endpoint: `lane_f/f7_r3b_endpoint.py` — sha256
  `3d397de0091229668cd73be2f353e19b67cd4e710bc2e552685123f111cb8c9d`.
- R2 B_total (comparison only):
  `[119.06285559909506923733105505540038073444204661321639737225436126041286995631480026545596 +/- 4.39e-87]`.
- R2 T_tail(224):
  `[1.4792058281325539748603802619554165552377648576548274999569040540025817664661217849158409e-23 +/- 7.80e-113]`;
  T_tail(256):
  `[2.4114870765008821786740995136173071286026016793840098027676886638887413159663541053986189e-27 +/- 8.08e-117]`.
- Enlarged-contour cover: `512` closed Acb arcs per block, `19` blocks, status
  `CERTIFIED`; max `eta = R/R_enlarged` across blocks `<= 0.86956522 < 1`.
- M' central-difference sanity at arc 0, N=6: matrix agreement `15` digits;
  Jacobi determinant derivative agreement `15` digits (step `1e-8`);
  labelled non-proof.

### Provenance flag — one primary path drifted AFTER the run (honest note)

All 16 chunks record the SAME engine sha256
`b6ee87fd…e28a0f`, so every chunk ran identical code — the cross-chunk
identity the plan requires holds. But the primary path
`.worktrees/aletheia-restore/code/zeta_cert_rosen.py` now hashes to
`965c2e5f65ae88b458d79bc425375e31589dcbf50703173664ef0e30901dceac` (mtime
2026-08-16, after the chunk runs). The certified bytes are still present in the
repository at
`.worktrees/aletheia-restore/code/out/kaggle_top4/hecke-gap-sweep/zeta_cert_rosen.py`,
verified to hash `b6ee87fd…e28a0f`. This is a provenance/reproducibility note,
not a gate failure and not a cross-chunk mismatch: no certified quantity in
this verdict depends on the current content of the drifted path. Any re-run
must restore the pinned bytes first. The other eight bindings still match their
live files byte-for-byte.

## 2. Coverage and hash pinning

- 16 chunk arc ranges: `[0,12) [12,24) [24,36) [36,48) [48,60) [60,72) [72,84)
  [84,96) [96,108) [108,120) [120,132) [132,144) [144,156) [156,168) [168,180)
  [180,192)` — contiguous, no gap, no overlap, tiling `[0,192)` exactly once.
- Merged accepted-record count `192`; merged `base_arc_index` sequence equals
  `0,1,…,191` in contour order.
- All nine source bindings carry a single sha256 across all 16 receipts
  (no chunk ran different code); `R2_constants` block canonical sha256
  `afe91fa35d1604853d8eec699e936f774ea3ba569a16cca54fc39c9af70a1d6b`, identical
  in all 16; `precision_bits` `384` in all 16;
  `immutable_hashes_verified` `True` in all 16.
- Per-chunk receipt sha256s are recorded in the assembly receipt.

## 3. Per-chunk table (N=256)

| Chunk | Arcs | Status | Gate | Cover | Accepted | Splits | min(finite lower − F), rounded DOWN | Wall s |
|---|---|---|---|---|---|---|---|---|
| chunk-00 | [0,12) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000281662514926721232928678 | 15253 |
| chunk-01 | [12,24) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000243478101506489600523288 | 27539 |
| chunk-02 | [24,36) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000241285307347605238320287 | 29655 |
| chunk-03 | [36,48) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000272360662199040605120561 | 29456 |
| chunk-04 | [48,60) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000281662323786929766696360 | 24467 |
| chunk-05 | [60,72) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000243478102572880428669938 | 15346 |
| chunk-06 | [72,84) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | **0.00000241285276269068356797445** | 26215 |
| chunk-07 | [84,96) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000272360607581385377254603 | 26224 |
| chunk-08 | [96,108) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000281662137054547307075060 | 15169 |
| chunk-09 | [108,120) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000243478064552118595669220 | 29169 |
| chunk-10 | [120,132) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000241285380530118956012129 | 25408 |
| chunk-11 | [132,144) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000272360764157905368024681 | 29245 |
| chunk-12 | [144,156) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000281662281806238277401688 | 26454 |
| chunk-13 | [156,168) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000243478010465359930660943 | 15102 |
| chunk-14 | [168,180) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000241285353703405127403857 | 26393 |
| chunk-15 | [180,192) | CHUNK_ARCS_CLEAR | True | True | 12 | 0 | 0.00000272360762402099572694119 | 26814 |

Every chunk: `all_finite_Taylor_enclosures_exclude_zero` `True`,
`all_F_inflated_closed_arc_enclosures_exclude_zero` `True`,
`complete_closed_cover` `True`, `adaptive_subdivision_count` `0` (every base
arc was accepted whole, so the merged cover is exactly the 192 base arcs).

Totals: base closed arcs `192`; accepted closed subarcs `192`; arc evaluations
`192`; adaptive splits `0`; chunk contour wall time `387 909 s` (≈107.8 h);
total chunk runtime including endpoint phases `441 267 s` (≈122.6 h).

## 4. Seam closure re-verification (REQUIRED by the cert plan)

Checked at all `192` arc junctions of the closed cycle, including the wrap
junction 191→0, and reported explicitly at the `16` chunk seams
(junction base-arc indices `0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132,
144, 156, 168, 180`):

- Contour endpoints chain at every junction (`s_end` of arc `i−1` and `s_start`
  of arc `i` are Arb balls that overlap and each contains the other's
  midpoint): `True` at all 192, `True` at all 16 seams.
- Adjacent finite-Taylor determinant boxes overlap at every junction
  (`box_intersection` non-empty — the audit's contour-closure check, now run
  ACROSS chunk boundaries and not only in-process): `True` at all 192,
  `True` at all 16 seams.
- Seam failures: none.

## 5. Closed-arc exclusions and winding

### N=256 (merged, primary)

- Complete closed cover over all 192 base arcs: `True`; accepted subarcs `192`;
  adaptive splits `0`.
- Every finite Taylor enclosure excludes 0: `True` (192/192).
- Every F-inflated closed-arc enclosure excludes 0: `True` (192/192).
- Certified finite-cover argument winding: **`1`**; winding ball
  `[0.999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999998426476 +/- 5.17e-114]`;
  integer pinned: `True`; method `convex overlap-midpoint polygon homotopic
  inside nonzero arc boxes`.
- Full determinant winding by the nonvanishing straight-line homotopy inside
  the F-inflated tubes: `1`.
- Minimum finite Taylor |det| lower bound (rounded DOWN):
  `0.00000241501898715557778515214`; ball
  `[2.41501898715557778515214258163664391994473503416052364421993308291284075137637738574532416360765571715625700752559054653e-6 +/- 3.86e-124]`.
- Minimum certified `finite lower − F` margin (rounded DOWN):
  **`0.00000241285276269068356797445`** (attained in chunk-06); ball
  `[2.41285276269068356797445899436723923863302307932658329703015428728494464067638054863561310108346294229247140664058485876e-6 +/- 1.90e-124]`.
  The same value is re-derived independently from the 192 raw per-arc
  `finite_lower_minus_F_margin` records — the per-arc and per-chunk minima
  agree (this is the 1-C5 re-derivation discipline).
- Maximum Taylor radius `rG` (rounded UP): `8.88500440571987887571864e-7`.
- Maximum self-consistency factor `rH` (rounded UP):
  `0.211064737207127407537372` — strictly below 1.

### N=224 (designed control arm — must and does FAIL)

- Status `NOT_CERTIFIED` in all 16 chunks; `closed_contour_gate_pass` `False`
  in all 16; accepted subarcs `0`; complete closed cover `False`.
- Winding: `None`; winding ball `unavailable`.
- First failure, base arc `0`: F-inflated Taylor enclosure contains zero;
  `finite lower − F` =
  `[-9.44306558608178031101452325736845754625867430555853709397…e-6]`,
  finite Taylor lower = `[3.84454864854494568510975196996557973391749745721…e-6]`,
  `rH` = `[0.1078881193012207508261966991922423444…]`;
  subdivision budget exhausted: `False`.
- Per plan §6 this arm is the fail-safe: it FAILED as designed, so the N=256
  pass is not an artefact of a too-loose tail bound.

## 6. Theorem-valid endpoint trace norm (N=256, identical in all 16 chunks)

- Matrix dimension `1280`; status `CERTIFIED`.
- Computed-row column 2-norm sum:
  `[20.1696369233844355095351318663678808976454087505001476309706301840016652295612162340827558268021086857807780463560229727 +/- 3.07e-119]`.
- Sum of enlarged-disc output-tail corrections:
  `[7.706042496573776902616531098546786270709958158012581816423…e-13]`.
- Retained full-column sum B_ret:
  `[20.1696369233852061137847892440581425507552634291272186267864314421833075403261104783308624199419464677594341335142295184 +/- 4.10e-119]`.
- Immutable input tail T_tail(256):
  `[2.41148707650088217867409951361730712860260167938400980276768866388874131596635410539861890808000003354449905512392399933e-27 +/- 3.48e-147]`.
- Same valid bound for both endpoints `||L||_1, ||LP_N||_1`:
  `[20.1696369233852061137847892464696296272561456078013181404037385707859092197101202810985510838306877837257882389128489895 +/- 3.44e-119]`.
- `F_R = T_tail*exp(1+2*B_same)`:
  `[2.16622446489421717768358726940468131171195483394034718977879562789611069999683710971106252419277486378560088500548535025e-9 +/- 3.52e-129]`.
- N=224 comparison arm (both rounded UP): `B_same <= 20.1696367902697082`,
  `F_R <= 1.3287614234626725996124275228e-5` — three orders of magnitude
  larger than the boundary minimum, which is why that arm fails.

Margin quality: `min(finite lower − F) / F_R = [1113.8517 +/- 1.9e-5]`, i.e. the
N=256 boundary margin is ~1.1e3 × F_R (contrast q=5 at N=160, where the margin was 2% of
F_R). The q=7 certificate is not thin.

## 7. Mathematical validity and scope

For a closed straight subarc A with midpoint s0 and radius r, Acb inversion of
`A(s)=I-M(s)` over the whole subarc certifies `H >= sup |tr(A(s)^(-1) M'(s))|`.
Jacobi gives `|d'(s)| <= H |d(s)|`. If `D=sup_A |d'|`, the segment mean-value
integral gives `sup_A |d| <= |d(s0)|+rD`, hence `D <= H(|d(s0)|+rD)`. The
certified inequality `rH<1` therefore yields `D <= G := H|d(s0)|/(1-rH)`, and
`d(s0)+ball(0,rG)` contains `det(I-M(s))` for every s in the closed subarc.

For each retained column, Cauchy's coefficient estimate on the certified
enlarged output disc gives `|a_m| <= U eta^m`; summing `m>=N` gives
`U eta^N/(1-eta)`, which dominates the omitted-output H2 norm. Adding this to
the computed-row 2-norm gives a full retained-column bound. Adding immutable
R2 `T_tail(N)` bounds `||L||_1`; the same sum also bounds `||LP_N||_1`.

The finite Taylor cover supplies the certified argument increments. Because
every F-inflated tube excludes 0, the straight-line perturbation from the
finite determinant to the Fredholm determinant stays nonzero on the boundary,
so winding is preserved.

Chunk-merge validity: each chunk certified a contiguous base-arc range with the
same pinned code, same precision, same immutable inputs, and accepted every
base arc whole. The 16 ranges tile `[0,192)` exactly once, so their ordered
concatenation IS the closed 192-arc cycle; the adjacent-box overlap test then
runs over that cycle, including all 16 chunk seams and the wrap. Nothing about
the winding count depends on the chunk decomposition — the argument accumulates
over one cycle of nonzero boxes.

### What this YES does and does not prove

Does prove: at `N=256`, with 384-bit ball arithmetic and the pinned immutable
R2/TB inputs, the finite determinant `det(I - L P_N)` and — through the
F-inflated homotopy — the Fredholm determinant `det(I - L_s)` have winding
number exactly `1` on the boundary of the `1e-6` coordinate box around
`s0 = 0.4751647621098225 + 4.668743786424289 i`. Exactly one zero of the
Fredholm determinant lies in that closed box, counted with multiplicity.

Does NOT prove (same scope caveats as the q=5 flagship cert):

- This is the R2/R3 closed-contour computation only. The MMS
  sector/factorization argument and the separate closed
  `det(1-K_s) != 0` identification remain OUTSIDE this verdict, exactly as in
  the mandatory attempt-1 report. Until link 4 (K_s gate, box margin
  ≈ 0.5895480) and link 4b (E1 enlarged-disc contraction) are banked at q=7,
  the enclosed zero is a zero of the certified Fredholm determinant, NOT yet
  identified as a resonance of `G_7`.
- No claim of `delta = 1/2 - Re(s*) >= 0.0248342` or `Re(s*) <= 0.4751648`
  follows from this document alone. That conclusion needs the full seven-link
  chain (R5 determinant identification included); this is link 3.
- Sector honesty: `sign = +1` (mms+) only. No geometric parity claim.
- No statement about any other zero, about the completeness of the q=7
  resonance list, or about the nearest sibling zero (1.70 away at float level
  — isolation was never in doubt; the winding count is what is certified).
- The central-difference derivative check is a labelled non-proof sanity check;
  production bounds use Acb analytic derivatives.

### Carried-forward known-latent code notes

The q=7 orchestrator is a port of the q=5 runner, so the three latent hazards
recorded in `lane_g/R3B_FLAGSHIP_CERT.md` (Kimi K3 audit 2026-08-15) apply to
this run too and are re-stated, not re-litigated:

- (1-C3) `f7_r3b_endpoint.py` takes `rho = max(head_base_sups, deep_rho)`,
  omitting `center_ratio`. Any re-run or parameter change must add an explicit
  `assert rho >= center_ratio`.
- (1-C4) the FTC direction ball is selected by endpoint-ball overlap with no
  assertion; unreachable at 384 bits but unguarded.
- (1-C5) two gate literals are written as hard-coded `True`. This assembly
  therefore re-derives the global margin from the 192 raw per-arc records and
  confirms it equals the per-chunk minimum, rather than trusting the summary
  fields.
