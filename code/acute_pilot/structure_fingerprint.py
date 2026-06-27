#!/usr/bin/env python3
"""Cheap structural fingerprint of the A089676 record witnesses.
Signals of HIDDEN STRUCTURE in the (non-linear) optima a(11..15):
  - period subgroup P = {v : S^v == S}  (|P| = maximal subspace S is a union of cosets of; >1 = structure)
  - pairwise XOR-distance distribution (few distinct values = code-like; spread = heuristic)
  - per-coordinate column balance (|S|/2 = code-like)
  - weight distribution
Run from repo root: python3 code/acute_pilot/structure_fingerprint.py
"""
import os, re
from collections import Counter

def popc(x): return bin(x).count('1')

def load(path):
    txt=open(path).read(); W={}
    parts=re.split(r'a\((\d+)\)\s*>=\s*(\d+):', txt)
    for i in range(1,len(parts),3):
        n=int(parts[i]); rows=re.findall(r'\(([01\s]+)\)', parts[i+2])
        vecs=[]
        for r in rows:
            bits=[int(b) for b in r.split()]; v=0
            for j,b in enumerate(bits):
                if b: v|=(1<<j)
            vecs.append(v)
        W[n]=(len(bits) if rows else 0, vecs)
    return W

def period_subgroup(S, n):
    Sset=set(S)
    P=[v for v in range(1<<n) if all((s^v) in Sset for s in S)]
    return P  # includes 0; |P| is a power of 2

def fingerprint(n, S):
    Sset=set(S); m=len(S)
    # pairwise distances
    dists=Counter()
    for i in range(m):
        for j in range(i+1,m):
            dists[popc(S[i]^S[j])]+=1
    # column balance
    cols=[sum((s>>c)&1 for s in S) for c in range(n)]
    # weights
    wts=Counter(popc(s) for s in S)
    P=period_subgroup(S,n)
    print(f"\n== n={n}, |S|={m} ==")
    print(f"  period subgroup |P| = {len(P)}  (dim {len(P).bit_length()-1})  -> {'STRUCTURE (coset union)' if len(P)>1 else 'trivial (no translational structure)'}")
    print(f"  distinct pairwise distances = {len(dists)}  range [{min(dists)},{max(dists)}]  -> {'code-like (few)' if len(dists)<=6 else 'spread (heuristic-like)'}")
    print(f"    distance histogram: {dict(sorted(dists.items()))}")
    print(f"  column 1-counts (ideal balance={m/2:.1f}): min={min(cols)} max={max(cols)} -> {'balanced' if max(cols)-min(cols)<=2 else 'uneven'}")
    print(f"  weight distribution: {dict(sorted(wts.items()))}")

if __name__=="__main__":
    here=os.path.dirname(os.path.abspath(__file__))
    W=load(os.path.join(here,"a089676_witnesses.txt"))
    for n in (11,12,13,14,15):
        nn,S=W[n]; fingerprint(nn,S)
