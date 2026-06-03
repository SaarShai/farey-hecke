#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_curves.py A.tsv B.tsv  --  exact integer comparison of two mr1_par curve outputs
(independent M1 vs M2 3e14 replications). Schema: "N<TAB>x<TAB>a<TAB>count" (+ TOTAL rows).
Reports any (N,x,a) where the two disagree. Gold-standard cross-check at the 3e14 frontier.
"""
import sys
from collections import defaultdict

def parse(path):
    d = {}
    with open(path) as f:
        for ln in f:
            if ln.startswith('#') or ln.startswith('TOTAL'):
                continue
            p = ln.rstrip('\n').split('\t')
            if len(p) != 4:
                continue
            N, x, a, c = int(p[0]), int(p[1]), int(p[2]), int(p[3])
            d[(N, x, a)] = c
    return d

A = parse(sys.argv[1]); B = parse(sys.argv[2])
keysA, keysB = set(A), set(B)
onlyA = keysA - keysB; onlyB = keysB - keysA
shared = keysA & keysB
mism = [(k, A[k], B[k]) for k in shared if A[k] != B[k]]
print(f"A={sys.argv[1]} ({len(A)} cells)  B={sys.argv[2]} ({len(B)} cells)")
print(f"shared cells: {len(shared)}; only-A: {len(onlyA)}; only-B: {len(onlyB)}; mismatches: {len(mism)}")
for k, va, vb in mism[:40]:
    print(f"  MISMATCH N={k[0]} x={k[1]} a={k[2]}: A={va} B={vb} (d={va-vb})")
if not mism and not onlyA and not onlyB:
    print("EXACT MATCH — two independent sieves agree to the integer at every grid point. PASS")
elif not mism:
    print("All shared cells match (grid coverage differs only by file completeness).")
else:
    print("*** DISCREPANCY — investigate ***")
