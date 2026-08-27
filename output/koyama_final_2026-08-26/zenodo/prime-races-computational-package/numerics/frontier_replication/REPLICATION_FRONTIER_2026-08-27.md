# Independent frontier replication — PASS (2026-08-27)

**Claim closed.** The `1.3e13 -> 3e14` frontier of `curve_3e14.tsv`, previously
computed only by `mr1_par` (same code on M1 and M2), is now independently
replicated by a different implementation.

## Method

- primesieve (libprimesieve, apt/Kaggle) C++ iterator, OpenMP over 256
  dynamic chunks with half-open `[lo,hi)` prime ownership; residues counted
  for N in {7, 8, 11, 19, 23} and snapshotted at mr1_par's exact 72 frontier
  grid points.
- Run as three concurrent Kaggle script kernels splitting the prime range
  (`saarshai/farey-frontier-p1/p2/p3`: `[0,1e14)`, `[1e14,2e14)`,
  `[2e14,3e14]`), each ~7.5–11.9 h wall (a single kernel hit the 12 h session
  cap on 2026-08-26 and was cancelled; version 1 of each part kernel is the
  one used). Sources: `part{1,2,3}/frontier_part.py`; outputs under `out/p{1,2,3}/`.
- Merged cell-wise by `merge_parts.py` (range counts sum to cumulative
  counts; internal TOTAL-vs-cells consistency asserted; script self-tested
  with a positive and a corrupted-cell negative case).

## Result

```
checkpoints shared: 72  cells shared: 4896  cells missing from reference: 0
PASS: 4896/4896 shared cells match exactly across 72 checkpoints; all TOTAL rows match
```

External anchors: the part range counts reproduce the published values
pi(1e14) = 3204941750802, pi(2e14) = 6270424651315, pi(3e14) = 9287441600280
exactly (p2's `[1e14,2e14)` count 3065482900513 = pi(2e14) - pi(1e14)).

## Scope

This certifies exact agreement of the two implementations at the 72 shared
grid points (all classes, all five moduli, plus TOTAL rows). It does not
certify checkpoints outside the grid or anything about zeros/GRH.
