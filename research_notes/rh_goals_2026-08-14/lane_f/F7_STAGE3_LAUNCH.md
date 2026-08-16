# F7 STAGE-3 LAUNCH — q=7 R3b closed-cover, 16-way Kaggle chunk launch

Date: 2026-08-15/16. Follows `F7_4B_REOPT_REPORT.md` (stage 4b enlarged-contour
fix, GO). Scope: sha-pin sanity, one-arc smoke, 16 self-contained private
Kaggle bundles, push, and slug/queue record. No commit, no other lanes'
files.

## 1. sha256 pins

`f7_certify_r3b_flagship.py` hardcodes exactly two expected hashes,
`R2_EXPECTED_SHA256` and `TB_V2_EXPECTED_SHA256`, checked live in
`verify_immutable_inputs()`. Both still match the on-disk receipts
byte-for-byte:

```
R2_EXPECTED_SHA256  = 4e5f0105e80f6f4fc0e173750abc628534bbc944928f759b1cf3e12bb9202efc
  live sha256(F7_R2_FLAGSHIP_ENVELOPE_RECEIPT.json) = 4e5f0105e80f6f4fc0e173750abc628534bbc944928f759b1cf3e12bb9202efc  -- MATCH
TB_V2_EXPECTED_SHA256 = 93baddf565b2dca6e94da441a9d7e906ab81576c4acf3506ab334bcf1251f4f6
  live sha256(F7_TB_BLOCK_CERTIFICATES_RECEIPT.json) = 93baddf565b2dca6e94da441a9d7e906ab81576c4acf3506ab334bcf1251f4f6  -- MATCH
```

`f7_r3b_endpoint.py`'s sha256 is **not** hardcoded anywhere in
`f7_certify_r3b_flagship.py`; it is computed live
(`sha256(ENDPOINT_CODE_PATH)`) and recorded in every receipt's
`source_bindings.R3b_endpoint` field, not compared against a stored pin.
Same for the three V2 receipts from `F7_4B_REOPT_REPORT.md`
(`F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`,
`F7_R3B_ENDPOINT_V2_RECEIPT.json`, `F7_STAGE2_FR_V2_RECEIPT.json`) — the
flagship cert script does not currently consume or pin them at all (that
integration is out of scope here; the script's own theorem-grade closed-cover
computation re-derives the endpoint/enlarged-contour bounds independently at
runtime, as the smoke run below shows). **Verdict: no pin edit was needed or
made** — the file was already correct for the fixed `f7_r3b_endpoint.py`; the
old-hash note in `F7_4B_REOPT_REPORT.md` referred only to the historical
`f7_receipts/smoke/` receipts, which the report explicitly leaves untouched.

Live current endpoint hash for the record:
`sha256(f7_r3b_endpoint.py) = 3d397de0091229668cd73be2f353e19b67cd4e710bc2e552685123f111cb8c9d`
(matches the "fixed" value quoted in `F7_4B_REOPT_REPORT.md` §5).

## 2. Smoke: one arc, `--arcs 0:1`, N=256/224, 4 workers

Command:

```bash
/Users/za/.venvs/farey-rh/bin/python f7_certify_r3b_flagship.py \
  --arcs 0:1 --workers 4 \
  --receipt f7_receipts/smoke_v2/F7_R3B_SMOKE_V2_RECEIPT.json \
  --checkpoint f7_receipts/smoke_v2/F7_R3B_SMOKE_V2_CHECKPOINT.json \
  --report f7_receipts/smoke_v2/F7_R3B_SMOKE_V2_CERT.md
```

**Wall time: 2622.9 s (43.7 min), under the 45-min ceiling** (script's own
`runtime_seconds` field; `verify_immutable_inputs`/setup/enlarged-sups/matrix
builds ≈ 121 s, N=256 closed-contour phase 1513.7 s, N=224 control-arm phase
988.1 s).

Result — **base arc 0 is FINITE and gate-passing at N=256**:

- `closed_contour["256"].status = "CHUNK_ARCS_CLEAR"`, `chunk_gate_pass = True`,
  `accepted_closed_subarc_count = 1`, `adaptive_subdivision_count = 0`
  (accepted at depth 0, no subdivision needed).
- `all_finite_Taylor_enclosures_exclude_zero = True`,
  `all_F_inflated_closed_arc_enclosures_exclude_zero = True`.
- `minimum_finite_Taylor_abs_lower_bound ≈ 3.844e-6`, finite and well above
  the `F_R` margin (`finite_lower_minus_F_margin ≈ 3.842e-6 > 0`).
- `immutable_hashes_verified = True`.

N=224 is the **designed control arm** (`stop_after_first_failure=True`,
NOT_CERTIFIED by construction below the m₀ threshold, per
`F7_4B_REOPT_REPORT.md` §3): it fails on base arc 0 exactly as expected —
`F_R_upper_bound ≈ 1.32876e-5` (reproduces the stage-4b report's N=224 table
value to every printed digit), `status = "NOT_CERTIFIED"`. This is not a
launch blocker; it is the intended NOT_CERTIFIED control result.

**Verdict: SMOKE PASS.** Both the finite-F_R check and the wall-time ceiling
clear.

## 3. Sixteen self-contained Kaggle bundles

Generator: `/private/tmp/.../scratchpad/make_bundles.py` (session-scoped,
not committed). Layout: `lane_f/kaggle_f7/f7-r3b-chunk-NN/` for
`NN = 00..15`, each with `kernel-metadata.json`
(`is_private: true`, `enable_gpu: false`) and one runner script
`f7_r3b_chunk_NN.py`.

Each runner embeds, as zlib-compressed + base64-encoded blobs (raw base64
alone exceeded Kaggle's 1 MB script-source cap; compressed the bundle is
≈ 275–285 KB), every file `f7_certify_r3b_flagship.py`'s import graph and
`sha256`-pin checks touch at their **exact hardcoded absolute paths**
(the script and its whole dependency tree use fixed paths under
`/Users/za/Documents/farey-hecke/...`, not paths relative to the kernel
working directory — confirmed by three failed pushes that iteratively
surfaced `ModuleNotFoundError`/`FileNotFoundError` for missing transitive
deps, fixed by tracing `sys.modules` after a local `--self-test` run and by
reading the two Kaggle error logs):

- `.worktrees/aletheia-restore/code/tc_rerun/{certify_r3_flagship,tc_rerun,r3b_engine}.py`
- `.worktrees/aletheia-restore/code/tb_certify/{certify_tb_blocks,certify_tb_blocks_v2}.py`
- `.worktrees/aletheia-restore/code/{zeta_cert_rosen,zeta_cert_rosen_q5}.py`
- `.worktrees/aletheia-restore/code/out/resonance_geometry.json`
- `lane_f/{f7_certify_r3b_flagship,f7_certify_r2_flagship,f7_certify_tb_blocks,f7_r3b_engine,f7_source_builder,f7_r3b_endpoint}.py`
- `lane_f/{F7_PILOT2_REPORT.md,F7_TB_R2_RECEIPTS.md}`
- `lane_f/f7_receipts/{F7_R2_FLAGSHIP_ENVELOPE_RECEIPT,F7_TB_BLOCK_CERTIFICATES_RECEIPT,F7_W_ENVELOPE_CERT_RECEIPT}.json`
- `lane_g/tb_disc_opt.json`

The runner `pip install -q python-flint` if needed, writes the 15 files to
their scaffold paths, then runs the **unmodified**
`f7_certify_r3b_flagship.py` with `--arcs {lo}:{hi} --workers 4`, output to
`/kaggle/working/`. Chunk table (frozen 16-way partition of the 192 base arcs,
`F7_PILOT_REPORT.md` §4):

| chunk | `--arcs` |
|---:|:---|
| 00 | 0:12 | 01 | 12:24 | 02 | 24:36 | 03 | 36:48 |
| 04 | 48:60 | 05 | 60:72 | 06 | 72:84 | 07 | 84:96 |
| 08 | 96:108 | 09 | 108:120 | 10 | 120:132 | 11 | 132:144 |
| 12 | 144:156 | 13 | 156:168 | 14 | 168:180 | 15 | 180:192 |

Verification before push: decompress round-trip of all 15 embedded files
against the live originals (byte-identical, checked), `ast.parse` syntax
check of each runner, and a local `--self-test` re-run to enumerate the true
import graph.

## 4. CPU-h extrapolation

From the one-arc smoke (best case: `adaptive_subdivision_count = 0`, no
subdivision needed):

- N=256 primary phase, per arc: 1513.7 s.
- N=224 control-arm phase: **fixed cost per kernel, not per arc**
  (`stop_after_first_failure=True`, always fails on base arc 0 of the full
  192-arc cover): 988.1 s.
- Setup (verify/enlarged-sups/TB+R2+endpoint matrix rebuild): ≈121 s.

Per 12-arc chunk, optimistic (uniform per-arc cost, 4 parallel workers):

- N=256: 12 × 1513.7 s = 18,164 s CPU ≈ **5.05 CPU-h**; wall with 4 workers
  ≈ ceil(12/4) × 1513.7 s ≈ 4541 s ≈ 1.26 h.
- N=224 control: 988 s ≈ 0.27 CPU-h, serial, once per kernel.
- Setup: ≈121 s ≈ 0.03 CPU-h.
- **Optimistic total ≈ 5.36 CPU-h/chunk, ≈ 1.6 h wall/chunk.**

Applying a 2× buffer for arcs that need subdivision (the smoke arc needed
none — `max_subdivision_depth=8` exists precisely because harder arcs can):
**≈ 10.7 CPU-h/chunk, ≈ 3.1 h wall/chunk**, still far under Kaggle's ~9–12 h
per-session cap and the task's ~40 CPU-h split threshold — **no chunk needs
splitting** on current evidence. 16 chunks total: **≈ 86–171 CPU-h**,
consistent with the prep-plan's ~280 CPU-h order-of-magnitude estimate (this
extrapolation is from a single easy arc and should be treated as a
lower/plausible-range estimate, not a hard bound).

## 5. Push results

`kaggle kernels push -p f7-r3b-chunk-NN` for all 16, iterating through three
dependency-completeness failures (see §3) before the import/hash-pin chain
was fully self-contained; confirmed by chunk 00 sustaining `RUNNING` past 9.5
minutes wall (real arc-evaluation work, not an import crash) before the
remaining four accepted slots were pushed.

**Accepted and RUNNING (5/16 — Kaggle's "Maximum batch CPU session count of
5" cap):**

| chunk | ref | arcs | status at last check (2026-08-16 04:50 UTC) |
|---:|:---|:---|:---|
| 00 | `saarshai/f7-r3b-chunk-00` | 0:12 | RUNNING |
| 01 | `saarshai/f7-r3b-chunk-01` | 12:24 | RUNNING |
| 02 | `saarshai/f7-r3b-chunk-02` | 24:36 | RUNNING |
| 03 | `saarshai/f7-r3b-chunk-03` | 36:48 | RUNNING |
| 04 | `saarshai/f7-r3b-chunk-04` | 48:60 | RUNNING |

**Queued (11/16 — rejected with `Kernel push error: Maximum batch CPU
session count of 5 reached.`; bundles are built, verified, and ready; push
each as a slot frees, in this order):**

| order | chunk | ref | arcs |
|---:|---:|:---|:---|
| 1 | 05 | `saarshai/f7-r3b-chunk-05` | 60:72 |
| 2 | 06 | `saarshai/f7-r3b-chunk-06` | 72:84 |
| 3 | 07 | `saarshai/f7-r3b-chunk-07` | 84:96 |
| 4 | 08 | `saarshai/f7-r3b-chunk-08` | 96:108 |
| 5 | 09 | `saarshai/f7-r3b-chunk-09` | 108:120 |
| 6 | 10 | `saarshai/f7-r3b-chunk-10` | 120:132 |
| 7 | 11 | `saarshai/f7-r3b-chunk-11` | 132:144 |
| 8 | 12 | `saarshai/f7-r3b-chunk-12` | 144:156 |
| 9 | 13 | `saarshai/f7-r3b-chunk-13` | 156:168 |
| 10 | 14 | `saarshai/f7-r3b-chunk-14` | 168:180 |
| 11 | 15 | `saarshai/f7-r3b-chunk-15` | 180:192 |

Re-run `cd lane_f/kaggle_f7/f7-r3b-chunk-NN && kaggle kernels push` for each
queued chunk as running kernels finish and free a slot (poll with
`kaggle kernels status saarshai/f7-r3b-chunk-NN`).

## 6. Honest scope and caveats

- The CPU-h extrapolation is from **one** arc that needed zero subdivision;
  harder arcs elsewhere in the 192-arc cover could cost substantially more.
  No chunk has finished; §4's per-chunk estimate is not yet a measured pilot.
- N=224's control-arm failure is by design (NOT_CERTIFIED below the m₀
  threshold) and should not be read as a launch defect in the pushed
  kernels' eventual output.
- The sha256-pin task (§1) required no file edit: both hardcoded pins were
  already correct, and the endpoint/V2-receipt hashes are computed live, not
  pinned, in the current script.
- Bundle dependency completeness was established empirically (three failed
  Kaggle pushes, each fixed from its traceback) rather than from a single
  static analysis pass; a fourth hidden dependency cannot be ruled out for
  chunks that reach code paths the smoke arc did not exercise (e.g. deeper
  subdivision, `evaluate_closed_cover_parallel`'s worker-error branches).
- `make_bundles.py` lives in the session scratchpad, not the repo; the
  generated `kaggle_f7/` bundles themselves are on-repo artifacts checked
  above but the generator was not committed anywhere (task said not to
  commit).

## 7. Artifacts

- `f7_receipts/smoke_v2/F7_R3B_SMOKE_V2_{RECEIPT,CHECKPOINT}.json`,
  `F7_R3B_SMOKE_V2_CERT.md`, `run.log` — the one-arc smoke.
- `kaggle_f7/f7-r3b-chunk-00 .. -15/` — 16 push-verified bundle directories.
