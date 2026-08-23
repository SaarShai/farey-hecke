# S2 second-pin N=288 contour campaign — build + dispatch receipt

- Date: 2026-08-23. Compute-engineering lane, OWNER-APPROVED (~58 CPU-h
  escalation signed off). **Status: UNREFEREED.**
- Goal: certify the second G_5 winding box (center
  `0.41054373549473627 + 7.81976824701551188 i`, half-width `1e-6`,
  sign=+1 P-symmetric/mms+, n_head=4); on success NOGO-OPEN-1 closes at
  assembly (referee-gated).
- Interpreter: `/Users/za/.venvs/farey-rh/bin/python` (python-flint 0.9.0,
  384-bit balls). Directed rounding throughout: upper bounds UP, margins DOWN.
- Nothing was committed. The q8 d8 campaign files were not touched; no Kaggle
  kernel was cancelled or deleted.

## A. Boundary det FREEZE at N=288 — verdict: PASS (subsample + per-arc-in-campaign)

Which of the task's two options holds: **the subsample-plus-campaign option.**
Full per-arc dets at N=288 locally ARE the 46–58 CPU-h campaign, so the freeze
is a 12-probe per-edge subsample, and the caveat is explicitly carried into
the campaign design — **confirmed from the orchestrator** that every campaign
chunk recomputes and certifies its own per-arc determinants: each arc
evaluation (`certify_r3b_flagship._jacobi_taylor_arc`) builds the midpoint
det, the certified Taylor box, and requires BOTH the finite Taylor box and the
F-inflated box to exclude zero, per arc, in ball arithmetic. The freeze below
is dispatch-gate evidence, not the certificate; the campaign itself is the
per-arc certificate.

Driver: `.worktrees/aletheia-restore/code/second_pin/freeze_boundary_dets_n288.py`
(single core, nice 19, wall 2777.5 s). Receipt JSON:
`lane_g/second_pin/S2_BOUNDARY_DET_FREEZE_N288.json`; log
`lane_g/second_pin/FREEZE_N288.log`.

Command:
```
( cd /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin \
  && nice -n 19 /Users/za/.venvs/farey-rh/bin/python freeze_boundary_dets_n288.py )
```

Contents (all certified Arb bounds, directed rounding):
- Endpoint certificate re-derived at max_N=288, M=512: **CERTIFIED**
  (Kimi 1-C3 guard active).
- T_tail(288) recomputed from the immutable R2 receipt block records
  (self-check vs stored 128/160 rows passed): `1.4251150358948e-41` scale.
- **F_R(288) = 2.0894484155448082e-8 (upper)** — reproduces
  `F288_PROBE.json` exactly (determinism check).
- 12 boundary det probes at N=288, 3 per edge (base arcs edge·48+{12,24,36}):

| edge | min det lower bound | probes (det lower / margin lower) |
|---|---|---|
| bottom | 4.249324e-6 | 4.7109e-6/4.6901e-6 · 4.2493e-6/4.2284e-6 · 4.7901e-6/4.7692e-6 |
| right  | 4.249316e-6 | 4.7109e-6/4.6900e-6 · 4.2493e-6/4.2284e-6 · 4.7901e-6/4.7692e-6 |
| top    | 4.249328e-6 | 4.7109e-6/4.6900e-6 · 4.2493e-6/4.2284e-6 · 4.7901e-6/4.7692e-6 |
| left   | 4.249337e-6 | 4.7110e-6/4.6901e-6 · 4.2493e-6/4.2284e-6 · 4.7901e-6/4.7692e-6 |

- **Worst probe margin (lower bound): 4.2284212773e-6 — POSITIVE, clears the
  1e-8 floor by ~2.6 orders. GATE PASS.** The midpoint-proxy caveat of
  `F288_PROBE.json` (single N=256 bottom-edge probe) is REPLACED by this
  N=288 four-edge freeze; the residual per-arc caveat (Taylor-radius erosion
  on closed arcs) is carried by design into the campaign's per-arc gates.
- N* note: N=274 is the measured floor (S2_NSCALING_RECEIPT.md); the campaign
  stays at the frozen N=288 (margin headroom ~2e3× in F_R).

## B. Code tasks (B3–B6 per plan §6 / SECOND_PIN_PREP §5)

All edits inside `.worktrees/aletheia-restore/code/second_pin/` and the NEW
campaign dir `lane_g/kaggle_s2_contour/`. Flagship originals byte-identical.

1. **B3 — seam-aware merge (DONE + TESTED).**
   `certify_r3b_flagship.merge_chunks_and_verify_closure` rewritten: instead
   of rejecting subdivided chunks (old `count==192` check), it verifies that
   the accepted leaves of every base arc tile the arc's dyadic parameter
   interval exactly once, contiguously, in lineage order (Fraction
   arithmetic, exact), then runs the adjacent-box overlap-polygon winding
   over ALL merged leaves. Synthetic tests: subdivided 8-arc cover merges to
   winding 1; a dropped leaf and a duplicated leaf are both refused
   (transcript: "B3 MERGE TESTS PASS").
2. **B4 — bundle generator (DONE + REHEARSED).**
   `lane_g/kaggle_s2_contour/build_bundle.py` (q8-pattern: flat dataset +
   manifest sha256 + in-kernel tree reconstruction). Dependency closure
   derived by `sys.modules` trace: 8 python files + 8 data inputs + 2
   import-time data files the trace missed and the REHEARSAL caught
   (`lane_g/tb_disc_opt.json`, `code/out/resonance_geometry.json` — the
   lane_f "3 failed pushes" failure mode, caught locally instead). Rehearsal:
   dataset → staged tree in scratchpad → orchestrator `--self-test` PASS →
   `verify_immutable_inputs` + `load_and_validate_r2` + `ensure_tail_bound(288)`
   PASS ("REHEARSAL PASS" in transcript).
3. **B5 — constant/sha plumbing (DONE).**
   - `N_PRIMARY 160 → 288` in the orchestrator copy.
   - In-memory `ensure_tail_bound`: T_tail(288) recomputed from the immutable
     R2 receipt block records with a mandatory self-check against the stored
     128/160 rows (receipt file untouched; `R2_EXPECTED_SHA256` pin
     `6410dff3…` still binds it).
   - Report text de-flagshipped (S2 center, N from constants).
   - **DEVIATION (loud): latent crash fixed in `certify_r3_flagship.py`
     copy.** Its `load_and_validate_r2` still checked the FLAGSHIP W receipt
     (`W_ENVELOPE_CERT_V2_RECEIPT.json`) and a nonexistent
     `second_pin/certify_tb_blocks.py` for the R2 source bindings; the S2 R2
     receipt binds `second_pin/W_ENVELOPE_CERT_S2_RECEIPT.json` and
     `tb_certify/certify_tb_blocks.py`. Phase 1 never hit this (phase1_gate
     bypassed `load_and_validate_r2`); every campaign kernel would have
     crashed. Both paths corrected; `load_and_validate_r2` now verified
     passing (B_total 203.1038… reproduced).
   - **DEVIATION (design, loud): new `--skip-comparison` flag.** The
     orchestrator otherwise runs the N=128 control arm inside EVERY chunk
     kernel (16× waste; the plan puts the control arm in Phase 5 assembly).
     Chunk kernels pass the flag; the control arm must be run ONCE locally at
     assembly (see resume instructions).
4. **B6 — Kimi guards: already installed by Phase 1** (1-C3 in
   `r3b_endpoint.py`, 1-C4 + re-derived 1-C5 gate literals in the
   orchestrator) — verified present and exercised (endpoint cert CERTIFIED at
   this box; self-test passes at the S2 pin, derivative sanity 15 digits).

## C. Kaggle dispatch — LIVE

- Private dataset `saarshai/s2-contour-n288-inputs` (18 files, every file
  sha256-manifested; kernel aborts on any mismatch; the orchestrator then
  re-verifies its own R2/TB sha pins in-kernel). Status: "ready".
- 16 PRIVATE script kernels `s2-contour-n288-s00 … -s15`, chunk k =
  `--arcs 12k:12k+12`, `--workers 4 --skip-comparison`, receipts to
  `/kaggle/working/S2_CHUNK_a{lo}-{hi}.json` (+ .ckpt.json + .md). Soft
  in-kernel deadline 39600 s → SIGTERM (orchestrator checkpoints, exits
  cleanly, kernel exits 0 so partial artifacts are preserved).
- Slot poller `lane_g/kaggle_s2_contour/push_s2_kaggle.sh` running in the
  background (log `PUSHER_S2.log`), modeled exactly on
  `push_d8_kaggle.sh` including the `KernelWorkerStatus.` literal-enum
  status check; NON-DESTRUCTIVE — the d8 wave-2 kernels were never touched.
- State at receipt time (2026-08-23 ~09:5x UTC): **5 kernels pushed and
  `KernelWorkerStatus.RUNNING` (s00–s04)** — s00–s02 took free slots at
  08:23–08:25 UTC, s03–s04 took slots as d8 kernels completed on their own;
  s05–s15 queued in the poller (5-slot waves, 300 s poll).
- In-kernel log verification: `kaggle kernels logs` returns nothing while a
  script kernel is RUNNING (CLI 2.2.1 behavior, same as the q8 campaign), so
  the first in-kernel staging log check falls to harvest time; the local
  full-tree rehearsal (§B.2) is the pre-dispatch evidence that the kernel
  code path works end-to-end.
- Cost projection: ~1240 s CPU/arc local ⇒ 12 arcs/4 workers ≈ 1–2 h/chunk
  Kaggle wall (+overhead, ×2 subdivision buffer ⇒ well under the 12 h cap);
  full campaign ≈ 3–4 slot-waves ≈ 12–24 h calendar depending on d8 slot
  handover.

## D. Local queueing — NOT done (deliberate)

`ps aux | grep '[s]pawn_main' | wc -l` → **12**; load avg 15.57 on 16 cores —
the d8 local queue (workers 12) saturates the box. Per the task rule:
**Kaggle-only** for S2 chunks. Only the single-core nice-19 freeze driver ran
locally (the Phase-1 precedent). If the d8 local queue drains before Kaggle
finishes, chunks can be run locally with the same orchestrator command (see
below) — receipts are interchangeable with kernel receipts.

## Resume / harvest instructions (future session)

1. **Poller**: if dead, re-run
   `( cd …/lane_g/kaggle_s2_contour && ./push_s2_kaggle.sh >> PUSHER_S2.log 2>&1 & )`
   — idempotent via `.pushed_*` markers in `chunk_receipts/`.
2. **Harvest**: `( cd …/lane_g/kaggle_s2_contour && ./harvest_s2_kaggle.sh )`
   repeatedly; it pulls COMPLETE kernels into `chunk_receipts/` (idempotent,
   never cancels anything). All 16 in → it tells you to merge.
3. **Merge + winding (Phase 4)**:
   `/Users/za/.venvs/farey-rh/bin/python …/kaggle_s2_contour/merge_s2_chunks.py`
   → `chunk_receipts/S2_MERGED_CONTOUR_RECEIPT.json`. Requires all 16 chunks
   `CHUNK_ARCS_CLEAR`, identical F_R(288), contiguous ranges, dyadic leaf
   tiling; then the overlap-polygon winding must pin an integer ≥ 1.
4. **Chunk failure**: a `CHUNK_NOT_CLEAR` receipt names the failing lineage;
   re-run that chunk locally (after d8 drains) with
   `( cd …/code/second_pin && python certify_r3b_flagship.py --arcs LO:HI
   --workers 2 --skip-comparison --receipt …S2_CHUNK_aLO-HI.json … )`.
5. **Phase 5 assembly (separate session)**: run the N=128 control arm ONCE
   (orchestrator WITHOUT `--skip-comparison` and without `--arcs`, or a
   targeted control run; expected NOT_CERTIFIED), then the second-pin cert
   doc mirroring `THEOREM_G5_OFFLINE_ASSEMBLY.md`, THEN (referee-gated) the
   `NO_VERTICAL_LINE_COROLLARY.md` upgrade closing NOGO-OPEN-1. Do NOT edit
   the corollary before a cold referee passes the S2 chain (plan §5).
6. **Expected timeline**: first wave (s00–s04) lands ~4–6 h from 08:25 UTC
   2026-08-23; all 16 chunks in ~12–24 h; merge is minutes.

## Deviations from the frozen plan (complete list, none silent)

1. N escalated 160 → 288 (owner-approved; S2_PHASE1 gate FAIL at 160,
   N*=288 from F288_PROBE).
2. `load_and_validate_r2` W-binding + arc_helper paths fixed in the r3 copy
   (§B.3 — would otherwise crash every kernel).
3. `--skip-comparison` added; control arm moved to assembly time (§B.3).
4. Plan §6 said "budget ≤1 h" for Phase 1 — the N=288 freeze took 46 min
   (within budget).
5. The det freeze is a 12-probe subsample, not full per-arc (46+ CPU-h);
   per-arc certification is delivered by the campaign chunks themselves
   (§A — this is the flagship design's own structure, confirmed in code).

STATUS: UNREFEREED. Every number is reproducible from
`lane_g/second_pin/S2_BOUNDARY_DET_FREEZE_N288.json`, the bundle
`manifest.json`, `PUSHER_S2.log`, and the commands quoted inline.
