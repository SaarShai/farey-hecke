#!/usr/bin/env python3
"""Merge the 3 range-split Kaggle part curves into one cumulative curve and
diff it cell-for-cell against the frontier rows of the project curve.

Each part file holds, at every checkpoint x, the count of primes p <= x with
p in that part's range [RLO, RHI). Cell-wise summation over parts therefore
gives the full cumulative counts. Usage:

    python3 merge_parts.py out/p1/curve_kaggle_indep.tsv out/p2/... out/p3/... \
            ../curve_3e14.tsv
"""
import sys
from collections import defaultdict

def load(path):
    cells, totals = {}, {}
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            t = line.split()
            if t[0] == "TOTAL":
                totals[(int(t[1]), int(t[2]))] = int(t[3])
            else:
                cells[(int(t[0]), int(t[1]), int(t[2]))] = int(t[3])
    return cells, totals

def main():
    parts = sys.argv[1:4]
    ref_path = sys.argv[4]
    merged = defaultdict(int)
    merged_tot = defaultdict(int)
    keysets = []
    for p in parts:
        c, t = load(p)
        keysets.append(set(c))
        for k, v in c.items():
            merged[k] += v
        for k, v in t.items():
            merged_tot[k] += v
    assert keysets[0] == keysets[1] == keysets[2], "part grids differ"
    # internal consistency: TOTAL == sum of class cells at every (N, x)
    for (N, x), tot in merged_tot.items():
        s = sum(v for (n, xx, a), v in merged.items() if n == N and xx == x)
        assert s == tot, f"TOTAL mismatch N={N} x={x}: {s} != {tot}"

    ref_cells, ref_tot = load(ref_path)
    shared = [k for k in merged if k in ref_cells]
    miss = [k for k in merged if k not in ref_cells]
    bad = [(k, merged[k], ref_cells[k]) for k in shared if merged[k] != ref_cells[k]]
    xs = sorted({x for (_, x, _) in shared})
    print(f"checkpoints shared: {len(xs)}  cells shared: {len(shared)}  "
          f"cells missing from reference: {len(miss)}")
    if bad:
        print(f"FAIL: {len(bad)} mismatching cells")
        for k, m, r in bad[:20]:
            print("  N=%d x=%d a=%d  kaggle=%d  mr1_par=%d" % (*k, m, r))
        sys.exit(1)
    tb = [(k, merged_tot[k], ref_tot[k]) for k in merged_tot if k in ref_tot
          and merged_tot[k] != ref_tot[k]]
    if tb:
        print(f"FAIL: {len(tb)} mismatching TOTAL rows"); sys.exit(1)
    print(f"PASS: {len(shared)}/{len(shared)} shared cells match exactly "
          f"across {len(xs)} checkpoints; all TOTAL rows match")

if __name__ == "__main__":
    main()
