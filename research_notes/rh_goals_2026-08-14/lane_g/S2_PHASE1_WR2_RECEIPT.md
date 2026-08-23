# S2 Phase-1 — W/R2 re-run at the second winding box: receipts and GATE verdict

- Date: 2026-08-23. Lane S2 continuation (owner-approved), executing the FROZEN
  plan `S2_SECOND_WINDING_BOX_SOL.md` §6, Phase 1 only. **Status: UNREFEREED.**
- Interpreter: `/Users/za/.venvs/farey-rh/bin/python` (python-flint/Arb, 384-bit
  balls throughout). All runs single-threaded, `nice -n 10`, ≤ 2 cores total;
  the live d8 shard queue was not touched (load stayed d8-dominated throughout).
- Box under test (frozen §6 Phase 0): center `0.41054373549473627 +
  7.81976824701551188 i`, per-coordinate half-width `1e-6`, box name
  `g5_pin_s2`, operator sign=+1 (P-symmetric / mms+), n_head=4.
- Directed rounding: quoted upper bounds are truncated UP, lower bounds and
  margins DOWN (conservative direction), from the full receipt strings.

## 0. GATE VERDICT, up front

**Phase-1 GATE: FAIL at N = 160 — STOP, per the plan's own criterion.**
F_R(new box, N=160) = `1.3958e12` (certified upper bound) against a boundary
determinant level of ≈ `4.2493`; every probed per-arc margin is ≈ `−1.396e12`,
i.e. astronomically below the ~1e-8 gate floor. No contour arc was run, no
Kaggle spend was made (both per the gate rule).

**Cause (diagnosed, not a bug):** T_tail(160) at the new box is fine
(`9.519e-22`, vs flagship `6.268e-22`), but the endpoint trace bound B_same
jumps `17.2912 → 37.6841`, and F_R = T_tail·exp(1+2·B_same) pays
exp(2·ΔB) ≈ 5e17 for it. This is the SECOND_PIN_PREP §2 degradation warning
(|t| 5.76 → 7.82 inflating the matrix column norms) landing exactly as
flagged: "whether the final margin closes at N=160 CANNOT be inferred" — it
does not close.

**Re-plan (projection, NON-BINDING):** the same certified R2 block-tail
formulas project the first positive per-arc margin at **N = 240**
(margin ≈ +3.66) and a comfortable one at **N = 256** (margin ≈ +4.247, F_R
≈ 1.94e-3 vs det level 4.2493). Recommended Phase-3 first attempt: **N = 256**
(see §5 caveats). Phase 2 is NOT ready to dispatch at N = 160.

## 1. What was executed (frozen-plan step by step)

New code dir `.worktrees/aletheia-restore/code/second_pin/` (copies, never
in-place; originals byte-identical — flagship sha pins unaffected):

| copy | source | edits |
|---|---|---|
| `certify_w_second_pin.py` | `tb_certify/certify_tb_weights_v2.py` | frozen single pin `g5_pin_s2` (load_pins hard-coded), output names `W_ENVELOPE_CERT_S2*`, out-dir `lane_g/second_pin/`, count check 8→1 |
| `certify_r2_flagship.py` | `tb_certify/certify_r2_flagship.py` | PIN_NAME/PIN_RE/PIN_IM → S2; W path → S2 receipt; output paths → `lane_g/second_pin/`; TB helper path → `tb_certify/` |
| `certify_r3_flagship.py` | `tc_rerun/certify_r3_flagship.py` | PIN_RE/PIN_IM → S2; R2/receipt/report paths → second_pin; sys.path add `tc_rerun` |
| `r3b_endpoint.py` | `tb_certify/r3b_endpoint.py` | `flagship_s_box()` + `s_region` → S2 box; **Kimi 1-C3 guard added** (raise unless center_ratio.upper() ≤ rho.lower()); path fixes |
| `certify_r3b_flagship.py` | `tc_rerun/certify_r3b_flagship.py` | all input/output paths → second_pin copies; `R2_EXPECTED_SHA256` → `6410dff3…` (S2 R2, full sha in §2); **Kimi 1-C4 guard added** (raise unless FTC direction horizontal XOR vertical); **1-C5 gate literals re-derived** (`Neumann_q_strictly_below_one` / `rH_strictly_below_one` now recomputed via `definitely_less`, not hard-coded True) |
| `phase1_gate.py` | new (95 lines) | GATE driver: immutable-input check, endpoint certificate (M=512, max_N=160), `compute_endpoint_trace_bound` at N=128/160, 4 boundary det probes at N=160 |

37 string edits applied by a strict apply-script (each pattern required
exactly once); TB_V2, E1, K_s receipts reused verbatim per prep §2.

## 2. W envelope (S2 box) — receipt

Command: `( cd …/code/second_pin && nice -n 10 python certify_w_second_pin.py
--pins-source …/lane_g/S2_SECOND_WINDING_BOX_SOL.md )` (provenance-only path;
pin constants are frozen in-code). Runtime 1.3 s. Output:

```
{"F": "[1.41515213333341829837719e+188 +/- …]", "W0": "[45.9375141993582343954994 +/- …]",
 "W_ge1": "[44.6658811851825879737774 +/- …]", "box": "g5_pin_s2",
 "margin_lower": "[-1.415…e+188 …]", "minimal_N": 1287, "verdict": "NOT"}
```

- W^(≥1) = `44.66589` (upper, trunc up) vs flagship pin's `18.63581`.
- The crude L3′ W-level verdict "NOT / minimal_N 1287" mirrors the flagship
  pattern (flagship: NOT / minimal_N 567 at this level) — the operative bound
  is the R2/R3b chain, exactly as at the flagship. Not itself a gate.
- Receipt: `lane_g/second_pin/W_ENVELOPE_CERT_S2_RECEIPT.json`
  sha256 `dc95c5112342517d…` (report `W_ENVELOPE_CERT_S2.md` beside it).

## 3. R2 column envelope (S2 box) — receipt

Command: `( cd …/code/second_pin && nice -n 10 python certify_r2_flagship.py )`
(production defaults: M=512, K_head=16, 384 bits). Runtime 13.0 s.
**Status CERTIFIED, verdict `R2_COLUMN_ENVELOPE_CERTIFIED_R3_PENDING`.**

| quantity | S2 box | flagship |
|---|---|---|
| B_total | 203.10388 (up) | 97.76665 |
| T_tail(128) | 8.0134e-17 (up) | 5.2716e-17 |
| T_tail(160) | 9.5186e-22 (up) | 6.2679e-22 |
| T_tail(160) < T_tail(128) | True | True |

- Receipt: `lane_g/second_pin/R2_SECONDPIN_ENVELOPE_RECEIPT.json`
  sha256 `6410dff31e503176dbf03a1b181568c99f5bc386287b109ced371f08d7eee83d`
  (this sha is pinned into the orchestrator copy's `R2_EXPECTED_SHA256`).
- Strict `g5_pin_s2` box selection against the S2 W receipt passed; TB V2
  geometry cross-checks passed; negative control 2σ<1 passed (2σ ≈ 0.8211).

## 4. GATE computation — endpoint bound, F_R, boundary det probes

Command: `( cd …/code/second_pin && nice -n 10 python phase1_gate.py )`,
264 s wall. Result JSON: `lane_g/second_pin/PHASE1_GATE_RESULT.json`
(sha256 `7795f15c611b6429…`). Immutable-input sha check (S2 R2 + TB V2)
passed; endpoint certificate (11 blocks, M=512 enlarged arcs, 1-C3 guard
active) CERTIFIED in 1.0 s.

Endpoint trace bounds (`compute_endpoint_trace_bound`, full closed S2 box):

| N | B_retained | B_same | F_R = T_tail·exp(1+2·B_same) | flagship F_R |
|---|---|---|---|---|
| 128 | 37.68597 (up) | 37.68597 | 1.1796e17 (up) | 0.14978 |
| 160 | 37.68404 (up) | 37.68404 | **1.3958e12** (up) | **1.7798e-6** |

Boundary determinant probes (edge-midpoint base arcs, point evaluations of
the certified per-disc builder + `_det_block` at N=160):

| base arc | edge | \|det\| lower bound | margin = det_lower − F_R(160) |
|---|---|---|---|
| 24 | bottom | 4.249324 (down) | −1.3958e12 |
| 72 | right | 4.249315 (down) | −1.3958e12 |
| 120 | top | 4.249328 (down) | −1.3958e12 |
| 168 | left | 4.249336 (down) | −1.3958e12 |

**GATE (plan §6: projected per-arc margin at N=160 below ~1e-8 → STOP): FAIL.**

Zero-location sanity (rules out a probe/pin artifact): center |det| by the
same per-disc builder is `7.8943e-12` at N=22 and `3.6072e-16` at N=44
(flagship center for calibration: `8.1084e-16` / `9.5895e-14`) — the S2 zero
is genuinely inside the box, and the near-constant boundary modulus 4.2493
across all four equidistant edge midpoints is exactly the simple-zero
prediction |det| ≈ |det′|·1e-6 (so |det′| ≈ 4.25e6 at N=160 — the det scale
at |t|=7.82 is ~2e6× the flagship's, which is also why the margin target is
4.25 rather than 1.8e-6).

## 5. Re-plan projection for N (NON-BINDING, [ARB-derived projection])

Recomputing T_tail(N) from the S2 R2 receipt's certified per-block tail
parameters (the receipt's own `receipt_block_tail` formulas) and holding
B_same at the N=160 value 37.68404 (it moved only −0.002 from 128→160, but
its value at higher N is UNVERIFIED — recompute during the re-run):

| N | T_tail(N) | projected F_R | projected margin vs 4.2493 |
|---|---|---|---|
| 192 | 1.088e-26 | 1.595e7 | −1.60e7 |
| 224 | 1.211e-31 | 1.776e2 | −173.4 |
| 232 | 6.975e-33 | 1.023e1 | −5.98 |
| 240 | 4.012e-34 | 5.883e-1 | **+3.6610** (down) |
| 256 | 1.323e-36 | 1.940e-3 | **+4.2474** (down) |
| 288 | 1.425e-41 | 2.090e-8 | +4.2493 |

Recommendation: **first Phase-3 attempt at N = 256** (N=240 leaves margin
3.66 against a 4.25 level before Taylor-radius inflation and subdivision
erosion; N=256's 4.2474 has ~2e3× headroom in F_R). Caveats: (a) B_same(256)
must be recomputed, (b) per-arc Taylor radii shrink the finite det lower
bound below the point-probe 4.2493, (c) |det′| ≈ 4.25e6 means the same
1e-6 box — no widening needed. Cost projection (flagship calibration 212 s
CPU/arc at N=160, ~N³ det/inverse scaling): ≈ 870 s CPU/arc at N=256 →
192 base arcs ≈ 46 CPU-h before subdivision — Kaggle 16-chunk territory
(~12·870/4 s ≈ 44 min/chunk + overhead, ×2 subdivision buffer ≈ 1.5 h/chunk,
under the session cap), NOT overnight-local while the d8 queue owns the box.

## 6. Deviations from the frozen plan (flagged, none silent)

1. §6 says the four certifier copies come from `code/tb_certify/`; in the
   repo `certify_r3_flagship.py` / `certify_r3b_flagship.py` actually live in
   `code/tc_rerun/` — copied from there. Same files the flagship receipts pin.
2. Path plumbing edits beyond the three PIN sites were required in the copies
   (sys.path inserts for `tc_rerun`/`tb_certify`, output paths to
   `lane_g/second_pin/`) — all listed in §1, applied by strict-match script.
3. The GATE quantity F_R required the endpoint certificate + trace bound,
   which §6 lists under the orchestrator; computed via the new 95-line
   `phase1_gate.py` driver (no contour arcs run) rather than by launching the
   orchestrator, so the gate could be evaluated without any arc spend.
4. The W copy's `--pins-source` records the S2 SOL note (provenance sha) —
   the flagship's scan-JSON pin loader is bypassed by frozen in-code
   constants, honestly recorded (`exact_count_check: len(pins)==1`).
5. The plan's "budget ≤ 1 h" held (W 1.3 s + R2 13 s + gate 264 s + probes);
   no checkpoint/resume was needed.

## 7. What Phase 2+ needs before dispatch (unchanged blockers + new)

- N must be re-frozen (recommend 256) and the projection's B_same(256)
  verified by one `compute_endpoint_trace_bound(256, …)` run (needs the
  endpoint certificate re-run with `max_N=256` — minutes).
- B3 (merge seam handling), B4 (bundle generator rewrite), B5 (sha plumbing
  for the new N), B6 remainder — unchanged code tasks from
  `SECOND_PIN_PREP.md` §5. The two Kimi guards + re-derived gate literals are
  now IN the copies (this session).
- Owner sign-off on the N escalation (≈2.7× the planned Phase-3 compute).

STATUS: UNREFEREED. Every number above is reproducible from the four JSON
receipts in `lane_g/second_pin/` and the commands quoted inline.

## ERRATA (2026-08-23, append-only)

§0/§4/§5 print the boundary det level as ~4.2493 due to a truncated-string exponent misread; the correct level is ~4.2493e-6 (see `S2_NSCALING_RECEIPT.md` correction and `S2_BOUNDARY_DET_FREEZE_N288.json`). All margin statements in those sections must be read at the e-6 scale.
