# Kaggle frontier independent cross-check — push instructions

**Status: STAGED, push-blocked on Kaggle auth (token returns 401).**

## What this is
`frontier_indep.py` = a Kaggle *script* kernel that recomputes `pi(x;N,a)` for
`N∈{7,8,11,19,23}` with **primesieve** (a different implementation from the project's
`mr1_par.c`), multithreaded by range, snapshotting at mr1_par's **exact** 72 frontier grid
points `1.3e13 → 3e14`. Output `/kaggle/working/curve_kaggle_indep.tsv` is in mr1_par schema,
so it diffs cell-for-cell via `compare_curves.py`.

## Why the frontier specifically
At `x ≤ 1.3e13` the curve is already corroborated by two independent methods in the Koyama
bundle (primesieve `replicate.cpp` == hand-rolled `independent_sieve.c`, certified exact in
`REPLICATION_REPORT.md`). The region `1.3e13 → 3e14` (the RS-variance onset) is computed ONLY
by `mr1_par` (M1 and M2 run the **same** code), so a large-x logic bug would pass both. This
kernel closes that gap with an independent implementation.

## Blocker
`~/.kaggle/kaggle.json` (user `saarshai`) returns **401 Unauthorized** — the API token is
expired/revoked. To unblock: Kaggle → Settings → API → **Create New Token**, save the
downloaded `kaggle.json` to `~/.kaggle/kaggle.json` (chmod 600).

## Push (once token is valid)
```bash
KG=~/Library/Python/3.9/bin/kaggle
cd "projects/minus1-dominance/kaggle_frontier"
"$KG" kernels push -p .
# watch:
"$KG" kernels status saarshai/farey-frontier-indep
# when complete, pull the output:
"$KG" kernels output saarshai/farey-frontier-indep -p ./out
# cross-check vs the project sieve (once curve_3e14.tsv has landed from M2):
python3 ../compare_curves.py ./out/curve_kaggle_indep.tsv ../curve_3e14.tsv
```
Expected runtime on Kaggle's 4 vCPU: ~3–5 h (π(3e14) ≈ 8.7e12 primes via primesieve
iterator, 4 threads). Kaggle CPU session limit is 12 h — comfortable.

## Sanity baked in
Kernel prints `pi(x)` at 3 checkpoints; cross-check vs known `π(1e14)=3204941750802`.
`compare_curves.py` requires EXACT integer agreement on every shared `(N,x,a)` cell.
