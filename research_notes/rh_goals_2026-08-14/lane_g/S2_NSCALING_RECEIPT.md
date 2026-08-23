# S2 N-scaling probe receipt (UNREFEREED)

Date: 2026-08-23. Compute-execution lane; single core, `nice 10`; d8 queue
workers untouched.

Purpose: the S2 Phase-1 gate failed at N=160 (F_R(160) ~ 1.3957e12 vs the
boundary det probes). Measure the F_R decay at N = 192, 224, 256 and fix the
smallest N* whose per-arc margin (boundary det lower bound minus F_R upper
bound) clears 1e-8. Upper bounds rounded UP, margins rounded DOWN (arb
directed rounding, `.upper()`/`.lower()`).

IMPORTANT CORRECTION uncovered en route: the Phase-1 boundary det lower
bounds are ~4.2493e-6, NOT ~4.25 — earlier truncated string prints hid the
`e-6` exponent (full strings in PHASE1_GATE_RESULT.json end `...e-6`). The
margin criterion is therefore F_R(N) < 4.2493e-6 - 1e-8, far harder than the
misread ~4.25 target.

Method:
- Endpoint certificate extended via
  `r3b_endpoint.certify_enlarged_contour_sups(tb_v2, max_N, M=512)`
  (max_N=256 for the scan, max_N=288 for the N* refinement; ~1s each,
  status CERTIFIED both times).
- T_tail(N) for N absent from the R2 receipt recomputed from the exact
  decimal intervals stored in the immutable R2 receipt block records, using
  the same module-level formulas (`certify_r2_flagship.tail_block_tail` /
  `single_block_tail`) as the receipt's own `receipt_block_tail`.
  Self-check: recomputation reproduces the stored T_tail at N=128 and N=160
  to <1e-6 relative (passed).
- F_R(N) from `certify_r3b_flagship.compute_endpoint_trace_bound` (second_pin
  copy), formula `T_tail(N) * exp(1 + 2*B_same(N))`.
- Boundary det probe = bottom-edge midpoint, base arc 24, as in
  `phase1_gate.py`, re-evaluated at N=256 and again at N*=274.

## Commands

```
cd /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin \
  && nice -n 10 /Users/za/.venvs/farey-rh/bin/python n_scaling_probe.py
cd /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin \
  && nice -n 10 /Users/za/.venvs/farey-rh/bin/python n_star_fix.py
```

Drivers: `.worktrees/aletheia-restore/code/second_pin/n_scaling_probe.py`,
`.worktrees/aletheia-restore/code/second_pin/n_star_fix.py`
Result JSON: `research_notes/rh_goals_2026-08-14/lane_g/second_pin/N_SCALING_PROBE.json`
(incremental writes after each N; `n_star_extension` block appended by the
second driver).

## Printed output (n_scaling_probe.py)

```
immutable inputs verified
T_tail receipt-formula self-check passed (N=128,160)
endpoint certificate (max_N=256) done in 1.1s
{"N": 192, "B_same": "[37.68397952568881114857664835", "T_tail": "[1.088004350342916535988276854", "F_R": "[15951952.29164935939203394534", "wall_s": 41.9}
{"N": 224, "B_same": "[37.68397787302944094256938122", "T_tail": "[1.211348022084295367202729773", "F_R": "[177.6031684156818715867254398", "wall_s": 55.3}
{"N": 256, "B_same": "[37.68397782468172400442012909", "T_tail": "[1.323297340107374965580321235", "F_R": "[0.001940167262825029820219850", "wall_s": 61.4}
{"det_probe_N": 256, "edge": "bottom", "det_lower": "[4.24932405437646406369185", "margin": "[-0.0019359179387706533561", "wall_s": 144.9}
{"N_star": null, ... "total_s": 304.7}
```

(det_lower full value is 4.2493240543764640636918...e-6; the negative margin
at N=256 is det_lower(4.2493e-6) - F_R(1.9402e-3) = -1.9359e-3, rounded down.)

## Printed output (n_star_fix.py)

```
endpoint certificate (max_N=288) done in 0.9s status=CERTIFIED
{"N": 274, "F_R": "[3.119668197224968962165834255", "margin": "[1.129655857151495101526023469", "clears": true, "wall_s": 69.9}
{"N": 265, "F_R": "[7.783940398289250274861769960", "margin": "[-7.35900799285160386849258418", "clears": false, "wall_s": 65.5}
{"N": 269, "F_R": "[1.863476452755973550334428571", "margin": "[-1.43854404731832714396524279", "clears": false, "wall_s": 64.3}
{"N": 271, "F_R": "[9.117034208328838946455273146", "margin": "[-4.86771015395237488276341542", "clears": false, "wall_s": 65.6}
{"N": 272, "F_R": "[6.376912256619015891563029819", "margin": "[-2.12758820224255182787117209", "clears": false, "wall_s": 67.7}
{"N": 273, "F_R": "[4.460279091291776039515994980", "margin": "[-2.10955036915311975824137255", "clears": false, "wall_s": 74.2}
{"N_star": 274, "det_lower_at_N_star": "[4.249324054376464063691857724", "margin": "[1.129655857151495101526023469", "total_s": 595.2}
```

Full exponents (from the JSON): F_R(274)=3.1197e-6,
F_R(273)=4.4603e-6 (fails, margin -2.1096e-7), F_R(272)=6.3769e-6,
F_R(271)=9.1170e-6, F_R(269)=1.8635e-5, F_R(265)=7.7839e-5.
det probe at N=274: |det| >= 4.2493240543764640636918...e-6 (wall 187.1s);
margin lower bound 1.1296558571514951e-6 > 1e-8. CLEARS.

## Findings

| N   | F_R upper bound | wall (s) |
|-----|-----------------|----------|
| 128 | 1.1796e17 (prior) | — |
| 160 | 1.3957e12 (prior) | — |
| 192 | 1.5952e7  | 41.9 |
| 224 | 1.7760e2  | 55.3 |
| 256 | 1.9402e-3 | 61.4 |
| 273 | 4.4603e-6 | 74.2 |
| 274 | 3.1197e-6 | 69.9 |

- Measured decay: F_R ~ exp(-0.357 N) — per-32 ratio 8.98e4 (192->224),
  9.15e4 (224->256), rate 0.3574/N over 256->274. One decade per ~6.45 in N.
  Extremely regular; B_same is flat (~37.684) so the decay is pure T_tail.
- **N* = 274** (smallest N with det_lower - F_R(N) >= 1e-8): margin lower
  bound 1.1297e-6 at the bottom-edge midpoint det probe evaluated at the
  same N=274. N=273 fails (margin -2.11e-7).
- Caveat: N* is fixed against ONE boundary point (bottom-edge midpoint,
  base arc 24). Phase-1 showed the four edge-midpoint dets agree to ~5
  digits (4.24932e-6 to 4.24934e-6, spread ~2e-11 absolute), so the
  edge-to-edge variation does not move N*; but full arcs use interval
  s-boxes whose det lower bounds dip below the midpoint value, so arcs may
  need subdivision where |det| dips toward F_R(274)=3.12e-6.
- Runtime at N*=274 (single core, measured): endpoint certificate ~1s,
  trace bound ~70s, point det probe 187s. A full-contour Jacobi-Taylor arc
  adds a matrix inverse and a derivative-matrix build on top of the det
  probe — estimate ~3-5x the det probe, i.e. ~10-16 min/arc. 192 base arcs
  => ~32-50 h single-core before subdivision. Verdict: does NOT fit a
  single-core local overnight; fits a local overnight with ~6-8 parallel
  workers (~5-8 h wall) provided the d8 queue is idle by then, otherwise
  route to Kaggle.
