#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
minus1_curve_analysis.py  --  cross-check + RS-normalized variance test on the
M2 sieve output curve_3e14.tsv.

USAGE: python3 minus1_curve_analysis.py curve_3e14.tsv [out2.tsv]

curve_3e14.tsv schema (mr1_par.c):  rows  "N<TAB>x<TAB>a<TAB>count"  giving
  count = pi(x; N, a) = #{p<=x prime : p == a (mod N)}  (a = 0..N-1, p=2 in class 2%N),
  plus  "TOTAL<TAB>N<TAB>x<TAB>pi_x"  rows.

PART A  cross-check (x <= 1.3e13): compare pi(x;N,a) for a=1..N-1 at the shared
  round checkpoints against koyama_replication_bundle/out2.tsv (raw blocks).
  Requirement: EXACT integer agreement.

PART B  RS-normalized variance test (the asymptotic prediction):
  E(x;N,a) = (log x / sqrt x)(pi(x;N,a) - pi(x;N,1))  -- the RS-normalized error of
  the race (a vs 1).  Empirical variance V_emp(N;a,1) = sample variance of E over the
  (log-uniform geometric) x-grid.  For each N in {7,11,19,23} rank the non-residues by
  V_emp and report whether a = -1 (= N-1) is the MAX (the theory prediction; conditional
  on GRH+LI).  Reported over the full grid AND the upper portion (near the onset ~3e14).
  NOTE: the log x/sqrt x weighting is the genuine RS normalization (not a free choice);
  it is identical across a, but x-dependent, so it is part of the definition.
"""
import sys, math
from collections import defaultdict

CURVE = sys.argv[1] if len(sys.argv) > 1 else "curve_3e14.tsv"
OUT2 = sys.argv[2] if len(sys.argv) > 2 else \
    "/Users/za/Documents/Farey NOW/koyama_replication_bundle/out2.tsv"
NS = [7, 8, 11, 19, 23]

def residues(N):
    sq = set((b * b) % N for b in range(1, N))
    NR = sorted(set(range(1, N)) - sq)
    return NR

# ---------------------------------------------------------------- parse curve
def parse_curve(path):
    # curve[N][x][a] = pi(x;N,a)
    curve = {N: defaultdict(dict) for N in NS}
    with open(path) as f:
        for ln in f:
            if ln.startswith('#') or ln.startswith('TOTAL'):
                continue
            p = ln.rstrip('\n').split('\t')
            if len(p) != 4:
                continue
            N, x, a, c = int(p[0]), int(p[1]), int(p[2]), int(p[3])
            curve[N][x][a] = c
    return curve

# ---------------------------------------------------------------- parse out2 (raw blocks)
def parse_out2(path):
    # out2raw[N][x][a] = pi(x;N,a), a = 1..N-1
    out2 = {N: {} for N in NS}
    curN = None
    mode = None  # 'raw' or 'diff'
    cols = None
    with open(path) as f:
        for ln in f:
            s = ln.rstrip('\n')
            if s.startswith('## N ='):
                curN = int(s.split('=')[1]); mode = None; continue
            if s.startswith('x\tcount_a='):
                mode = 'raw'
                cols = [int(c.split('=')[1]) for c in s.split('\t')[1:]]
                continue
            if s.startswith('# diffs'):
                mode = 'diff'; continue
            if s.startswith('x\tdiff_a='):
                mode = 'diff'; continue
            if not s or s.startswith('#'):
                continue
            if mode == 'raw' and curN is not None:
                p = s.split('\t')
                x = int(p[0])
                vals = [int(v) for v in p[1:]]
                out2[curN][x] = {cols[i]: vals[i] for i in range(len(cols))}
    return out2

# ---------------------------------------------------------------- PART A
def cross_check(curve, out2):
    print("=" * 70)
    print("PART A — cross-check curve_3e14.tsv vs out2.tsv (x <= 1.3e13), a=1..N-1")
    print("=" * 70)
    total_cmp = 0; mismatches = 0
    for N in NS:
        shared = sorted(set(curve[N]) & set(out2[N]))
        shared = [x for x in shared if x <= 13_000_000_000_000]
        for x in shared:
            for a in range(1, N):
                cv = curve[N][x].get(a)
                ov = out2[N][x].get(a)
                if ov is None:
                    continue
                total_cmp += 1
                if cv != ov:
                    mismatches += 1
                    print(f"  MISMATCH N={N} x={x} a={a}: curve={cv} out2={ov} (d={cv-ov})")
        print(f"  N={N}: {len(shared)} shared checkpoints <=1.3e13 compared.")
    print(f"  --> {total_cmp} comparisons, {mismatches} mismatches  "
          f"{'EXACT MATCH (PASS)' if mismatches == 0 else '*** FAIL ***'}")
    return mismatches == 0

# ---------------------------------------------------------------- PART B
def variance_test(curve):
    print("\n" + "=" * 70)
    print("PART B — RS-normalized empirical variance V_emp(N;a,1); is a=-1 the MAX?")
    print("  E(x;N,a) = (log x / sqrt x)(pi(x;N,a) - pi(x;N,1)); sample var over grid.")
    print("=" * 70)
    def sample_var(vals):
        n = len(vals)
        if n < 2: return 0.0
        m = sum(vals) / n
        return sum((v - m) ** 2 for v in vals) / (n - 1)
    results = {}
    for N in [7, 11, 19, 23]:
        xs = sorted(curve[N])
        if not xs:
            print(f"  N={N}: no data"); continue
        NR = residues(N)
        m1 = N - 1
        # define windows: full grid, and upper portion (x >= 1e13)
        windows = {
            "full": xs,
            "x>=1e13": [x for x in xs if x >= 1e13],
            "top-decade x>=3e13": [x for x in xs if x >= 3e13],
        }
        for wname, wxs in windows.items():
            if len(wxs) < 3:
                continue
            Vemp = {}
            for a in NR:
                E = []
                for x in wxs:
                    pa = curve[N][x].get(a); p1 = curve[N][x].get(1)
                    if pa is None or p1 is None:
                        continue
                    E.append((math.log(x) / math.sqrt(x)) * (pa - p1))
                Vemp[a] = sample_var(E)
            order = sorted(NR, key=lambda a: -Vemp[a])
            rank_m1 = order.index(m1) + 1
            tag = "a=-1 is MAX-var (theory-consistent)" if order[0] == m1 \
                else f"a=-1 rank {rank_m1}/{len(NR)} (argmax a={order[0]})"
            print(f"  N={N:2d} [{wname:18s}] n={len(wxs):3d}: {tag}")
            if wname == "full":
                results[N] = (rank_m1, len(NR), order[0])
    print("\n  (Theory, conditional GRH+LI: a=-1 should be the variance-MAX non-residue")
    print("   in the asymptotic regime; onset ~ e^33.4 ~ 3e14. Finite-x ranks may differ")
    print("   below onset — report honestly, do NOT force the asymptotic reading.)")
    return results

if __name__ == "__main__":
    import os
    if not os.path.exists(CURVE):
        print(f"curve file {CURVE} not present yet."); sys.exit(2)
    curve = parse_curve(CURVE)
    out2 = parse_out2(OUT2)
    ok = cross_check(curve, out2)
    variance_test(curve)
    print(f"\nCROSS-CHECK {'PASSED' if ok else 'FAILED'}.")
