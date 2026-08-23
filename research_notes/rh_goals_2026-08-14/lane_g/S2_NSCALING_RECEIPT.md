# S2 N-scaling probe receipt (UNREFEREED)

Date: 2026-08-23. Compute-execution lane; single core, `nice 10`; d8 queue
workers untouched.

Purpose: the S2 Phase-1 gate failed at N=160 (F_R(160) ~ 1.3957e12 vs
det ~ 4.25). Measure the F_R decay at N = 192, 224, 256 and fix the smallest
N* whose per-arc margin (boundary det lower bound minus F_R upper bound)
clears 1e-8. Upper bounds rounded UP, margins rounded DOWN (arb directed
rounding, `.upper()`/`.lower()`).

Method notes:
- Endpoint certificate extended to `max_N=256, M=512` via
  `r3b_endpoint.certify_enlarged_contour_sups`.
- T_tail(N) for N not in the R2 receipt (192, 224, 256, and search N)
  recomputed from the exact decimal intervals stored in the immutable R2
  receipt block records, using the same module-level formulas
  (`certify_r2_flagship.tail_block_tail` / `single_block_tail`) as the
  receipt's own `receipt_block_tail`. Self-check: recomputation reproduces
  the stored T_tail at N=128 and N=160 to <1e-6 relative.
- One boundary det probe (bottom-edge midpoint, base arc 24, as in
  `phase1_gate.py`) re-evaluated at the largest N reached.

## Command

```
cd /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin \
  && nice -n 10 /Users/za/.venvs/farey-rh/bin/python n_scaling_probe.py
```

Driver: `.worktrees/aletheia-restore/code/second_pin/n_scaling_probe.py`
Result JSON: `research_notes/rh_goals_2026-08-14/lane_g/second_pin/N_SCALING_PROBE.json`

## Printed output

```
(pending)
```

## Findings

(pending)

## Findings (orchestrator-completed, 2026-08-23; agent detached before filling)

Source: `second_pin/N_SCALING_PROBE.json` (driver exited cleanly, wall 304.7 s;
endpoint certificate extended to max_N=256, status CERTIFIED; T_tail
recompute self-check vs stored R2 values: relative gap ≤ 3.2e-89).

| N | F_R upper bound |
|---|---|
| 192 | ≈ 1.5952e7 |
| 224 | ≈ 1.7761e2 |
| 256 | ≈ 1.9402e-3 |

Boundary det probe (bottom-edge midpoint, N=256): lower bound
**≈ 4.2493e-6** (NOTE the e-6 — earlier orchestrator MAP entries and the
Phase-1 agent's "+4.247 margin at N=256" projection misread this as 4.2493e0
by truncating the exponent; the probe's criterion and result are correct).

**Verdict: N_star = null within the certificate range — no N ≤ 256 clears
det_lower − F_R > 1e-8.** F_R(256) = 1.94e-3 is ≈ 2.66 orders above the
≈ 4.24e-6 bar.

Measured decay: ≈ 4.96 orders of magnitude per 32 columns, stable across
192→224→256. Linear projection (NOT a certificate): F_R reaches the bar at
**N ≈ 274**; the next natural block N = 288 projects F_R ≈ 2e-8, margin
≈ 4.2e-6 against the 1e-8 floor. Confirming needs the endpoint certificate
extended past 256 (max_N=288) — a minutes-scale run — before any contour
freeze.

Cost update: full contour at N=288 scales ≈ (288/256)² ≈ 1.27× over the
46 CPU-h N=256 estimate → ≈ 58 CPU-h, Kaggle-chunk territory. Owner gate on
that dispatch stands.
