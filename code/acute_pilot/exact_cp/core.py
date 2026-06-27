#!/usr/bin/env python3
"""Core helpers for A089676 exact attack.
Right angle at apex Q between P,R  <=>  (P^Q) & (R^Q) == 0.
A set S subset {0,1}^n is ACUTE iff for NO ordered choice of apex Q and distinct
P,R in S is the angle right. Equivalently: for every unordered triple {A,B,C},
none of the 3 apex assignments yields orthogonality.
"""
import itertools

def is_acute_masks(S):
    """S: list of int bitmasks. True iff acute (matches verify.py)."""
    if len(set(S)) != len(S):
        return False
    m = len(S)
    for j in range(m):
        Q = S[j]
        xq = [s ^ Q for s in S]
        for a in range(m):
            if a == j: continue
            xa = xq[a]
            for b in range(a+1, m):
                if b == j: continue
                if (xa & xq[b]) == 0:
                    return False
    return True

def right_angle(P, Q, R):
    """True iff angle at apex Q (between P,R) is right."""
    return ((P ^ Q) & (R ^ Q)) == 0

def forbidden_triple(A, B, C):
    """For unordered {A,B,C}: True iff SOME apex gives a right angle (triple is forbidden)."""
    return right_angle(A, B, C) or right_angle(B, A, C) or right_angle(A, C, B)

if __name__ == "__main__":
    # sanity: brute force small n exact values a(2)=3,a(3)=5,a(4)=8 (known)
    # actually known: a(0..)=1,2,3,5,8,12,17,... let's confirm via exhaustive for n<=4
    import sys
    def exact_max(n):
        verts = list(range(1<<n))
        best = 0; bestS=None
        # greedy upper-ish: brute over subsets is too big; do simple branch for tiny n
        from itertools import combinations
        # only feasible n<=4 with smart bound; use incremental search
        # We'll just do a simple maximal independent-set DFS
        # build forbidden triples lazily is heavy; for n<=4 (<=16 verts) brute triples ok
        V=verts
        sys.setrecursionlimit(100000)
        bestbox=[0,None]
        def acute_add(S, cand):
            return is_acute_masks(S+[cand])
        def dfs(S, start):
            if len(S)>bestbox[0]:
                bestbox[0]=len(S); bestbox[1]=list(S)
            for i in range(start, len(V)):
                v=V[i]
                if is_acute_masks(S+[v]):
                    dfs(S+[v], i+1)
        dfs([],0)
        return bestbox[0], bestbox[1]
    for n in range(2,5):
        b,S=exact_max(n)
        print(f"n={n}: exact max found = {b}")
