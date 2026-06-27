#!/usr/bin/env python3
"""TRUSTED reference verifier for OEIS A089676 (max acute set in {0,1}^n).
Validated: PASSES on all 5 known record witnesses (n=11..15, sizes 24,32,33,64,128).
DO NOT MODIFY the core check. Every claimed record witness MUST pass this, re-run by the
main loop independently of whatever solver produced it.

Math: a set S of cube vertices is ACUTE iff every angle (over every apex) is strictly acute.
For 0/1 vectors, dot(apex Q; P,R) = (P-Q).(R-Q) = popcount((P^Q) & (R^Q)) >= 0 always, so the
ONLY forbidden case is a right angle, dot == 0, i.e. (P^Q)&(R^Q) == 0. (No obtuse angle can occur.)

CLI:
  python3 verify.py <witness_file> <n>     # rows of 0/1 (spaces optional), one vector per line
  python3 verify.py --selftest             # validate against the 5 OEIS records
Exit 0 = acute & all-distinct; prints SIZE and PASS/FAIL.
"""
import sys, os, re

def is_acute(S):
    """S: list of int bitmasks. Returns (ok:bool, witness). O(m^3) with cheap int ops."""
    if len(set(S)) != len(S):
        return (False, "DUPLICATE_POINTS")
    m = len(S)
    for j in range(m):                       # apex
        Q = S[j]
        xq = [S[a]^Q for a in range(m)]
        for a in range(m):
            if a == j: continue
            xa = xq[a]
            for b in range(a+1, m):
                if b == j: continue
                if (xa & xq[b]) == 0:        # right angle at S[j] between S[a],S[b]
                    return (False, ("right_angle_apex", j, "legs", a, b))
    return (True, None)

def rows_to_masks(rows):
    """rows: list of strings of 0/1 (spaces ok). Returns (n, [int,...])."""
    masks=[]; n=None
    for r in rows:
        bits=[c for c in r if c in '01']
        if not bits: continue
        if n is None: n=len(bits)
        if len(bits)!=n: raise ValueError(f"ragged row: {len(bits)} vs {n}")
        v=0
        for i,c in enumerate(bits):
            if c=='1': v|=(1<<i)
        masks.append(v)
    return n, masks

def parse_oeis_witnesses(path):
    """The Kamenetsky OEIS file -> {n:(claimed,[mask,...])}."""
    txt=open(path).read(); W={}
    parts=re.split(r'a\((\d+)\)\s*>=\s*(\d+):', txt)
    for i in range(1,len(parts),3):
        nn=int(parts[i]); claim=int(parts[i+1])
        rows=re.findall(r'\(([01\s]+)\)', parts[i+2])
        n,masks=rows_to_masks(rows)
        W[nn]=(claim,masks)
    return W

if __name__=="__main__":
    here=os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv)>=2 and sys.argv[1]=="--selftest":
        W=parse_oeis_witnesses(os.path.join(here,"a089676_witnesses.txt"))
        allok=True
        for nn in sorted(W):
            claim,masks=W[nn]
            ok,wit=is_acute(masks)
            good = ok and len(masks)==claim
            allok &= good
            print(f"n={nn}: size={len(masks)} claim={claim} acute={ok} {'PASS' if good else 'FAIL '+str(wit)}")
        print("SELFTEST", "PASS" if allok else "FAIL")
        sys.exit(0 if allok else 1)
    if len(sys.argv)<3:
        print("usage: verify.py <witness_file> <n>   |   verify.py --selftest"); sys.exit(2)
    path=sys.argv[1]; n_expect=int(sys.argv[2])
    rows=open(path).read().splitlines()
    n,masks=rows_to_masks(rows)
    if n!=n_expect:
        print(f"FAIL: dimension {n} != expected {n_expect}"); sys.exit(1)
    ok,wit=is_acute(masks)
    print(f"n={n} size={len(masks)} acute={ok}")
    if ok:
        print(f"PASS  (acute set of size {len(masks)} in {{0,1}}^{n})")
        sys.exit(0)
    else:
        print(f"FAIL  {wit}"); sys.exit(1)
