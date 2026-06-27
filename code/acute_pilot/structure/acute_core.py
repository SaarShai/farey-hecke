#!/usr/bin/env python3
"""Core acute-set primitives (bitmask). Mirrors verify.py exactly.
Right angle at apex Q between distinct legs P,R  <=>  (P^Q)&(R^Q)==0.
S acute <=> NO such ordered triple. (Equivalently no apex has two distinct legs with disjoint diff-supports.)
"""
def is_acute_fast(S):
    """S list of ints. Return (ok, witness). Early-exit O(m^3)."""
    if len(set(S))!=len(S): return (False,"DUP")
    m=len(S); Sl=list(S)
    for j in range(m):
        Q=Sl[j]
        xq=[s^Q for s in Sl]
        for a in range(m):
            if a==j: continue
            xa=xq[a]
            for b in range(a+1,m):
                if b==j: continue
                if (xa & xq[b])==0:
                    return (False,(j,a,b))
    return (True,None)

def can_add(S, p, masks=None):
    """Is S+{p} still acute, given S already acute? Check only triples involving p."""
    m=len(S)
    # p as apex: any two distinct legs in S with disjoint (s^p)?
    xq=[s^p for s in S]
    for a in range(m):
        xa=xq[a]
        if xa==0: return False  # p duplicates an element
        for b in range(a+1,m):
            if (xa & xq[b])==0: return False
    # p as a leg: apex Q in S, other leg R in S, (p^Q)&(R^Q)==0
    for j in range(m):
        Q=S[j]; pq=p^Q
        if pq==0: return False
        for r in range(m):
            if r==j: continue
            if (pq & (S[r]^Q))==0: return False
    return True
