# Depth-8 pre-flight at N = 262 — referee condition 3

Date: 2026-08-20 · lane_g · unrefereed

`DERIVATIVE_SEMANTICS_REFEREE.md` gave a CONDITIONAL GO for the q8 depth-8
uniform re-run. Condition 3 asks for ~4 depth-8 leaves evaluated at the full
`N = 262` on the true worst cases before the big wave is committed. This note
records that pre-flight.

## Method

Driver `kaggle_q8_subdivision/q8_leaf_shard.py`, unmodified, at
`--depth 8 --N 262 --K 1`. Leaf addressing is the driver's own big-endian
convention (`leaf_path`), so depth-7 leaf `k` refines into depth-8 leaves
`2k` and `2k+1` on the same arc:

* arc 2, depth-7 path `[1,0,0,0,1,1,1]` = leaf 71 (the true worst, depth-7
  `rH = 1.0290323`) → children 142, 143.
* arc 3, depth-7 path `[0,1,0,1,0,1,0]` = leaf 42 (referee-found failing,
  depth-7 `rH = 0.695079`) → children 84, 85.
* arc 0, mid-arc depth-7 leaf 64 → child 128; arc 1, mid-arc depth-7 leaf 63
  → child 127 (one child each, the qOp/rH peak region).

Four shards ran concurrently on 12 cores. Receipts:
`kaggle_q8_subdivision/shard_receipts/PREFLIGHT_d8_a{0,1,2,3}_*.json`.

Pass predictor: `rH < 1/(1+sqrt(2)) = 0.4142136` (the referee's a4 square-box
criterion, not `rH < 1/2`). Gate: full `arc_certificate` PASS including
`finite_taylor_excludes_zero`.

## Results (verbatim from the receipts)

| arc | d8 leaf | path | rH_upper | qOp_upper | excludes_zero | status | leaf_seconds |
|-----|---------|------|----------|-----------|---------------|--------|--------------|
| 0 | 128 | `10000000` | 0.1892125248420895230 | 0.3271992747911403256 | true | PASS | 1429.1 |
| 1 | 127 | `01111111` | 0.1886709459592556194 | 0.3271333226599129062 | true | PASS | 1427.5 |
| 2 | 142 | `10001110` | 0.1944493671754489931 | 0.3244342173806212174 | true | PASS | 1429.2 |
| 2 | 143 | `10001111` | 0.1944637027370571602 | 0.3239681184931549657 | true | PASS | 1429.3 |
| 3 | 84 | `01010100` | 0.1415497008267430356 | 0.3035516418827991532 | true | PASS | 1428.4 |
| 3 | 85 | `01010101` | 0.1422369970166416197 | 0.3043759448396981086 | true | PASS | 1427.9 |

6/6 PASS, 0 OPEN_MAX_DEPTH. `qOp_lt_1` and `rH_lt_1` true on every leaf.
Every `leaves_complete` is true; payload hashes
`8412cd87f75a4fca…` (a0), `4718219e8d9cd407…` (a1),
`6815341d87fa1b8f…` (a2), `410ce6d1f6044f01…` (a3).

## Cross-checks

* Worst observed depth-8 `rH = 0.1944637` — **2.13× below** the 0.4142136
  predictor, exactly the margin the referee computed.
* The referee's independent N = 48 probe predicted these children at
  `rH = 0.194449 / 0.194463` (arc 2) and `0.141550 / 0.142237` (arc 3). The
  N = 262 values agree to 6 significant figures. N = 48 is a faithful proxy
  for `rH` at N = 262, as claim (c) asserted.
* Per-level scaling on these leaves: arc 2 `1.0290323 → 0.1944494` = **5.29×**;
  arc 3 `0.695079 → 0.1415497` = **4.91×**. Both inside the referee's measured
  4.6–5.3× band; no leaf scaled worse than predicted.
* Cost: 1427.5–1429.3 s per leaf, tighter than the ~1900 s planning figure.
  1024 leaves ⇒ ~407 CPU-h, below the 535 CPU-h budget.

## Verdict

**FULL GO** for the 1024-leaf depth-8 wave.

All six leaves clear both the square-box predictor and the full
`arc_certificate` gate including `finite_taylor_excludes_zero`, on the true
worst depth-7 leaf of arc 2, on the referee-found failing leaf of arc 3, and
on mid-arc peak leaves of arcs 0 and 1 — covering both edge orientations.

Scope limit, stated plainly: this is 6 leaves of 1024, and the referee's
condition-4 screen remains measured-on-samples. The screen still holds — any
depth-7 leaf with `rH > 4 × 0.41421 ≈ 1.66` is not predicted to clear depth 8,
and the observed depth-7 maximum is 1.029. Arcs 0 and 1 were never fully
certified at depth 7, so a depth-7 `rH` above 1.66 there would invalidate the
prediction. Nothing in this pre-flight proves a uniform bound on `H_true`;
it confirms the predictor on the hardest cases known.
