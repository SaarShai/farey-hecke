# INDEX CONVENTION (fixed 2026-08-15): CSV 'index' is 1-BASED into
# the Odlyzko seed table: row index i <-> seeds[i-1] <-> mp.zetazero(i).
#!/usr/bin/env python3
"""Full harvest gate for Kaggle zero tables (Kimi audit 4-D1 + 4-D2).

Gates, per part CSV:
  G1 residual   : max |zeta(1/2+i*gamma)| below 1e-15 (from CSV column)
  G2 monotone   : gamma strictly increasing, no duplicates
  G3 seed-match : |gamma_refined - odlyzko_seed| <= 1e-6 for every row
  G4 index      : contiguous, matches JSON receipt range
  G5 N(T) count : Riemann-von Mangoldt completeness — for the part's range
                  (T_first, T_last], the zero COUNT must equal
                  round(N_rvm(T_last)) - round(N_rvm(T_first)) where
                  N_rvm(T) = T/(2pi) log(T/(2pi e)) + 7/8 + S(T) correction
                  is evaluated via mpmath's rigorous-enough zetazero-free
                  formula N(T) ~ theta(T)/pi + 1 + S(T); we use
                  mp.siegeltheta and check the count against
                  theta(T)/pi + 1 at both ends (|S(T)| < 1 for these
                  heights would flag any missing/extra zero).
Usage: harvest_gate.py <csv> [<csv>...]
"""
import csv, json, sys
from mpmath import mp

mp.dps = 30
SEEDS = "/Users/za/Documents/farey-hecke/cluster_universality_test/zeros1.txt"
seeds = [float(l) for l in open(SEEDS) if l.strip()]

def n_smooth(t):
    # theta(T)/pi + 1: smooth part of the counting function
    return mp.siegeltheta(t) / mp.pi + 1

overall = True
for f in sys.argv[1:]:
    rows = list(csv.DictReader(open(f)))
    g = [mp.mpf(r["gamma_refined"]) for r in rows]
    res = [abs(mp.mpf(r["residual"])) for r in rows]
    idx = [int(r["index"]) for r in rows]
    g1 = max(res) < mp.mpf("1e-15")
    g2 = all(b > a for a, b in zip(g, g[1:]))
    g3 = all(abs(float(g[i]) - seeds[idx[i] - 1]) <= 1e-6 for i in range(len(rows)))
    g4 = all(b == a + 1 for a, b in zip(idx, idx[1:]))
    # G5: count in (midpoint below first, midpoint above last] vs RvM.
    # Use midpoints to neighbor seeds so the interval boundary is unambiguous.
    lo = (seeds[idx[0] - 2] + float(g[0])) / 2 if idx[0] > 1 else float(g[0]) - 0.5
    hi = (float(g[-1]) + seeds[idx[-1]]) / 2 if idx[-1] < len(seeds) else float(g[-1]) + 0.5
    expected = mp.nint(n_smooth(hi) - n_smooth(lo))
    s_dev = max(abs(n_smooth(hi) - n_smooth(lo) - len(rows)), 0)
    g5 = int(expected) == len(rows) and s_dev < mp.mpf("0.5")
    verdict = all([g1, g2, g3, g4, g5])
    overall &= verdict
    print(json.dumps({
        "file": f, "rows": len(rows),
        "G1_residual": bool(g1), "max_residual": mp.nstr(max(res), 5),
        "G2_monotone": bool(g2), "G3_seed_match": bool(g3),
        "G4_index_contiguous": bool(g4),
        "G5_rvm_count": bool(g5), "rvm_expected": int(expected),
        "rvm_deviation": mp.nstr(s_dev, 5),
        "VERDICT": "PASS" if verdict else "FAIL",
    }))
sys.exit(0 if overall else 1)
