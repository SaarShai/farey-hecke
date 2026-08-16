# F7 PILOT2 REPORT — q=7 stage-1 gate re-check, `--arcs` CLI, chunk pilot attempt

Date: 2026-08-15. Scope: stages 2-3 of `F7_CERT_PLAN.md` under the option-2
radii adopted in `F7_MITIGATION_REPORT.md` (`GO` verdict, `(3.522, 2.622,
2.372, 1.790, 1.600)`, float `rho* = 0.762251293807`, `B_finite(N=224) <=
20.1696367902`). Nothing beyond the CLI diff, the seam-closure helper, and
the pilot attempt was touched; no Kaggle kernels started; no commit made.

**Prior-attempt check (per instructions).** `git status` on the base repo and
on `.worktrees/aletheia-restore` showed no partial edits to
`certify_r3b_flagship.py` or any other cert runner before this session's
edits began — the worktree's untracked files are all pre-existing
`tb_certify`/`tc_rerun` scaffolding unrelated to this ticket (`family_prep/`,
`render_fill_report.py`, `certify_tb_blocks*.py`, `run_tc*.py`,
`tc_rerun.py`, a stray `tc_run_receipt_certifiedrho.json`). No prior codex
work on this lane's runner was found or lost.

## 1. N* recomputation — explicit arithmetic

The plan's decision rule (`F7_CERT_PLAN.md` §3):

```
F_R(N) = T_tail(N) * exp(1 + 2*B(N))  <  0.1 * m0
```

where `m0` is the float pre-scan estimate of `min_{∂Box}|det(I - L P_N)|` at
`N=32` (stage 2b) and `T_tail(N)` is the R2-envelope tail bound (stage 2). **Neither
`m0` nor a q=7 `T_tail(N)` exists yet** — both require the Arb R2 envelope
computation (`certify_r2_flagship.py`), which is gated behind stage-1 TB
block certification, which itself requires a q=7 port of `certify_tb_blocks_v2.py`
(itemized in `F7_CERT_PLAN.md` §2, not executed — see §3 below for why this
is out of this ticket's reachable scope). So `N*` cannot be *measured* here;
what follows is the plan's own scaling consistency check, made explicit and
verified numerically (all NON-RIGOROUS, float-level):

- Option-2 radii, `B_finite(N=224) = 20.1696367902`, `rho* = 0.762251293807`.
- `exp(1 + 2*B(224)) = exp(41.3392735804) = 8.982937992848e+17`.
- q=5 reference chain (certified): `B = 17.2912`, `T_tail(160) = 6.27e-22`,
  reported `F_R = 1.78e-6`. Reproduced here:
  `T_tail(160) * exp(1+2*17.2912) = 6.27e-22 * 2.839487576516e15 =
  1.78036e-06` — matches the plan's stated `1.78e-6` to 3 sig figs. Confirms
  the rule is being applied identically.
- `exp(1+2*B(224))_{q=7} / exp(1+2*B)_{q=5} = 8.98294e17 / 2.83949e15 =
  316.36`. So q=7's exponential-tail penalty at N=224 is ~316x q=5's at
  N=160 — this is the cost the larger `rho*` and `B` must be offset by a
  smaller `T_tail`.
- `rho*^N` at the option-2 value: `rho*^160 = 1.3668e-19`, `rho*^192 =
  2.3059e-23`, `rho*^224 = 3.8904e-27`, `rho*^256 = 6.5634e-31`. The plan's
  downstream note claims `rho*^224 ≈ 4e-27 "matches" q=5's rho*^160 ≈
  1e-25` — verified: `3.89e-27` is in fact *smaller* than `1e-25` by ~26x
  (i.e. even more favorable, not merely "matching").
- If `T_tail(N)` scales with the same order-of-magnitude prefactor as q=5's
  (`T_tail(160)/rho*^160 = 6.27e-22 / 1.3668e-19 = 4.59e-3`, i.e. `T_tail(N)
  ≈ C·rho*^N` with `C` order `1e-2`–`1e-3`), then at q=7 `N=224`:
  `F_R(224) ≈ C · 3.8904e-27 · 8.9829e17 ≈ C · 3.495e-9`, i.e.
  `F_R(224) ≈ 1.6e-11` for `C ≈ 4.6e-3`. This is ~5 orders of magnitude
  *smaller* than q=5's certified `F_R(160) = 1.78e-6`, so under this
  extrapolation the rule's margin condition (`F_R < 0.1·m0`) is easily
  satisfiable at `N* = 224` provided `m0` (q=7, `∂Box`, `N=32`) is not itself
  many orders smaller than q=5's implied `m0 ≈ F_R+margin ≈ 1.81e-6`.

**Verdict on N\*: `N* = 224` remains the consistent provisional freeze** —
this is a scaling-argument confirmation of the plan's own downstream note,
not a new measurement. It is explicitly NOT a stage-2b/R2 certificate; both
of those require Arb computation this ticket did not execute (see §3). If a
different `N*` is ever wanted, `N_COMPARISON = 192` is already provisioned
(`rho*^192 = 2.306e-23`, `exp` factor exponent unaffected — `B` was measured
flat in `N` up through 224 in the mitigation report, so `B(192) ≈ B(224) ≈
20.17` is a reasonable float-level estimate, not separately measured here).

## 2. `--arcs i:j` CLI addition (implemented, unit-verified)

File: `.worktrees/aletheia-restore/code/tc_rerun/certify_r3b_flagship.py`
(122 insertions / 4 deletions, `git diff --stat`).

- `evaluate_closed_cover_parallel(...)` gained an `arc_range: tuple[int,int]
  | None = None` parameter. When set, the base closed cover (192 arcs for
  the current q=5 geometry; the plan's q=7 chunk table assumes the same 192)
  is sliced `base[i:j]` before the adaptive-subdivision queue is built, and
  the full-cycle winding computation (`certified_winding_via_overlap_polygon`,
  which requires `boxes[index-1]` adjacency around the *entire* closed
  cycle) is skipped for a chunk — a slice is not a closed cycle. The
  returned dict now carries `chunk_arc_range`, `chunk_gate_pass` (local
  per-arc non-vanishing only), and `status ∈
  {CHUNK_ARCS_CLEAR, CHUNK_NOT_CLEAR}` instead of the whole-cover
  `{CERTIFIED, NOT_CERTIFIED}` labels, so a chunk receipt cannot be
  mistaken for a full certificate.
- `parse_args()` gained `--arcs i:j` (`_parse_arc_range`, validates `0 <= i
  < j`); `run()` threads `args.arcs` into the `N_PRIMARY` branch's call to
  `evaluate_closed_cover_parallel` (the `N_COMPARISON` designed-fail control
  arm is intentionally left unchunked — chunking a control that must FAIL is
  not meaningful).
- New standalone function `merge_chunks_and_verify_closure(chunk_receipts,
  expected_base_closed_arc_count)`: sorts chunk receipts by
  `chunk_arc_range`, checks the ranges tile `[0, N)` contiguously with no
  gap or overlap (**the seam-closure re-verification the plan requires**),
  checks every chunk cleared locally, concatenates the accepted per-arc
  records in base-arc order, and re-runs
  `certified_winding_via_overlap_polygon` over the *full* ordered box
  sequence — this is the actual seam check (adjacent-box overlap across a
  chunk boundary is exercised exactly like an in-chunk adjacency, since the
  boxes are concatenated before the winding polygon is built).

**Verification performed** (venv `~/.venvs/farey-rh`, `python-flint` 0.9.0
present there — the base env lacks `flint`):

- `python3 -m py_compile certify_r3b_flagship.py` — passes.
- `_parse_arc_range("0:12") == (0, 12)`; rejects `"5:2"` (inverted) and
  `"abc"` (malformed) with `argparse.ArgumentTypeError`.
- `merge_chunks_and_verify_closure` unit-tested against three synthetic
  chunk-receipt sets: (a) ranges `[0,12),[12,24)` against
  `expected=192` → correctly rejected, "do not tile the full base cover";
  (b) ranges `[0,12),[13,24)` (seam gap) → correctly rejected, "chunk arc
  ranges are not contiguous (seam gap or overlap)"; (c) tiling ranges but
  empty `records` lists vs `expected=24` → correctly rejected, "merged
  accepted-record count does not match the base cover size". All three
  failure modes fire as designed.
- Loaded the real (q=5) `closed_boundary_segments(...)` geometry via
  `certify_r3_flagship` and confirmed the base closed cover is exactly 192
  arcs (matches the plan's chunk-table assumption) and that an
  out-of-bounds `--arcs 190:200` request is caught by the same bounds check
  used inside `evaluate_closed_cover_parallel`.

No end-to-end chunked run of the full pipeline was executed (that requires
the q=7 port described in §3, not present).

## 3. Pilot chunk 0 (arcs 0:12) — NO-GO, structural blocker (not a timing NO-GO)

**Not run.** Before any wall-time/memory measurement is meaningful, the
runner must be able to build a q=7, `N=224`, option-2-radii matrix and
evaluate a Jacobi-Taylor arc determinant on it. Checked directly against the
live file:

- `ENGINE_PATH = WORKTREE_ROOT / "code" / "zeta_cert_rosen_q5.py"` (:41) —
  q=5 only.
- `EXACT_FACTORS = ("3.14", "2.27", "1.70")` (:60) — q=5's 3-factor radii,
  not q=7's 5-factor option-2 radii.
- `N_PRIMARY = 160`, `N_COMPARISON = 128` (:55-56) — q=5 values, not 224/192.
- `PIN_RE/PIN_IM/HALF_WIDTH` sourced from `r3_attempt1` (`certify_r3_flagship.py`)
  — q=5's pin box, not the q=7 flagship box
  `0.4751647621098225 + 4.668743786424289i`.
- `verify_immutable_inputs()` hash-pins `R2_PATH`/`TB_V2_PATH` against
  `R2_EXPECTED_SHA256`/`TB_V2_EXPECTED_SHA256` (:50-51), and those paths
  point at `lane_g/R2_FLAGSHIP_ENVELOPE_RECEIPT.json` and
  `lane_g/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json` — **confirmed present on
  disk, but these are the q=5 (lane_g) receipts.** No q=7 (lane_f) analogs
  exist anywhere in the repo (`find ... -iname "*R2_FLAGSHIP*" -o -iname
  "*TB_BLOCK_CERT*"` returns only the lane_g files).

Every one of these is a named, itemized change in `F7_CERT_PLAN.md` §2
("R3b winding cert" row) that was explicitly scoped as future work, not part
of this ticket. Producing them requires: (a) stage-1 TB block certification
for q=7 (κ=5, 19 blocks, 5 radii — a new Arb script derived from
`certify_tb_blocks_v2.py`), and (b) stage-2 R2 envelope certification for
q=7 (`certify_r2_flagship.py` re-run at the q=7 pin/geometry, producing the
q=7 `T_tail(N)` this report's §1 could only extrapolate). Neither exists.
Attempting to run the pilot against the current runner would either (i)
raise `FileNotFoundError`/hash-mismatch in `verify_immutable_inputs()`
immediately, or (ii) silently certify the *wrong* problem (q=5's box, at
q=5's radii) if the hash checks were bypassed — neither is an honest q=7
measurement, so no reduced pilot was attempted at any arc count.

This is a **structural** blocker (missing prerequisite artifacts + a
q=5-hardcoded engine binding), not a wall-time budget problem. Rule 5 of the
governing instructions (stop after two failed attempts at the same
criterion) does not apply cleanly here since no attempt was made that could
fail twice on the same diagnosis — the blocker was identified by direct
inspection before any run, and re-attempting without the stage-1/2 q=7
artifacts would just reproduce the same `FileNotFoundError`/hash-mismatch.

## 4. Timing / extrapolation

**No new measurement.** The plan's own unmeasured upper-bound estimate
stands unchanged: `~280 CPU-h` at `N=224` (1120×1120), `~175 CPU-h` at
`N=192`, from the q=5 cost-per-evaluation scaling
(`F7_CERT_PLAN.md` §5) — not promoted to a pilot figure, exactly as the
first pilot (`F7_PILOT_REPORT.md` §3) also declined to promote it. The
16-chunk table (≈18 CPU-h/chunk at N=224, ≈11 CPU-h/chunk at N=192) fits a
12h/4-vCPU (≤48 CPU-h) Kaggle session with 2-3x headroom *by this estimate
only*; it has not been checked against a measured per-arc-evaluation cost at
q=7 geometry, because no q=7 arc evaluation has run.

## 5. GO/NO-GO verdict

**NO-GO on stage 3 (pilot execution).** Structural: the q=7 TB block
certificate (stage 1) and R2 envelope (stage 2, including the `m0`/stage-2b
float pre-scan needed to close §1's `N*` decision rule) do not exist, and
the R3b runner is hardcoded to q=5 inputs (engine path, factors, N values,
pin box, and hash-pinned q=5 receipts). No pilot — full or reduced — can
honestly execute against q=7 without first producing those artifacts, which
`F7_CERT_PLAN.md` §2 itemizes as separate, larger stage-1/stage-2 work, not
part of this ticket's "stage 2 = `--arcs` CLI, stage 3 = pilot chunk" scope.

**GO on stage 2 (CLI + seam-closure) in isolation.** The `--arcs i:j` CLI
addition and the `merge_chunks_and_verify_closure` seam-closure helper are
implemented as a surgical diff to the existing runner, are q-independent
(they operate on the runner's own `closed_boundary_segments` output and
`chunk_arc_range` bookkeeping, not on the q-specific engine/factor
constants), and are unit-verified against synthetic chunk data and the live
192-arc q=5 base cover. They are ready to use once a q=7-ported runner
exists; they required no changes to `ENGINE_PATH`, `EXACT_FACTORS`, or the
hash-pinned receipts, so they carry no risk of having silently baked in q=5
assumptions.

**Chunk table.** Unchanged from `F7_PILOT_REPORT.md` §4 (16 chunks of 12
base arcs each, `0:12` through `180:192`) — still valid once a q=7 runner
exists, since the base cover size (192) matches the current runner's
geometry and the `--arcs` slicing added here is index-based, not
q-specific.

## 6. Recommended next step (frontier's call)

Port the q=7 TB block certification (stage 1) and R2 envelope (stage 2,
including the `m0` stage-2b float pre-scan) per the itemized changes in
`F7_CERT_PLAN.md` §2, producing real `lane_f/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json`
and `lane_f/R2_FLAGSHIP_ENVELOPE_RECEIPT.json` analogs. Only then can
`certify_r3b_flagship.py` be forked/re-pointed at q=7 constants (`ENGINE_PATH`,
`EXACT_FACTORS`, `N_PRIMARY/N_COMPARISON`, the flagship pin, and fresh
`R2_EXPECTED_SHA256`/`TB_V2_EXPECTED_SHA256`) and a real pilot chunk run —
at that point the `--arcs`/`merge_chunks_and_verify_closure` machinery added
here needs no further changes.
