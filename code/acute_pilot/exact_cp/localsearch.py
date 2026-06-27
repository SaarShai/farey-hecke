#!/usr/bin/env python3
"""Fast incremental local search for A089676 acute sets.

Key incremental test: given current acute set S (list of masks) and candidate v,
v can be ADDED iff no forbidden triple is created. New triples all involve v.
A new forbidden triple uses v as one of {apex, leg, leg}. Check:
 For each pair (a,b) in S: is {v,a,b} forbidden? -> apex v: (a^v)&(b^v)==0;
   apex a: (v^a)&(b^a)==0; apex b: (v^b)&(a^b)==0.
 Plus pairs where v is apex with the other two... covered above (v,a,b symmetric set).
So adding v: for all unordered pairs (a,b) in S, check forb3(v,a,b). O(|S|^2).
That's the cost. To make additions O(|S|): precompute, but triple is inherently pair-based.

We use: a 'conflict' when adding v = exists pair a,b in S with forb3(v,a,b).
Local search: maintain S acute. Try to grow; when stuck, remove k random, re-grow with
randomized candidate order + tabu. Restart from translates/permutations of records.
"""
import sys, time, random

def forb3(A,B,C):
    return ((B^A)&(C^A))==0 or ((A^B)&(C^B))==0 or ((A^C)&(B^C))==0

def can_add(S, v):
    # check all pairs in S
    L=len(S)
    for i in range(L):
        a=S[i]
        for j in range(i+1,L):
            b=S[j]
            if forb3(v,a,b):
                return False
    return True

def can_add_fast(S, v):
    """Slightly faster: precompute v^s for all s, but triple needs pairwise apex tests."""
    L=len(S)
    xv=[s^v for s in S]
    for i in range(L):
        a=S[i]; xva=xv[i]   # a^v
        # apex v between a,b: (a^v)&(b^v)==0  => xva & xv[j]==0
        # apex a between v,b: (v^a)&(b^a)==0  => xva & (b^a)==0
        # apex b between v,a: (v^b)&(a^b)==0  => xv[j] & (a^b)==0
        for j in range(i+1,L):
            b=S[j]; xvb=xv[j]
            if (xva & xvb)==0: return False
            ab=a^b
            if (xva & ab)==0: return False
            if (xvb & ab)==0: return False
    return True

def grow(S, cands, rng):
    """Greedily add candidates (in given order) that keep S acute."""
    for v in cands:
        if v in S_set_of(S): continue
        if can_add_fast(S, v):
            S.append(v)
    return S

def S_set_of(S): return set(S)

def build_random(n, target, time_limit, seed):
    rng=random.Random(seed)
    mask=(1<<n)-1
    allv=list(range(1<<n))
    t0=time.time()
    best=[]
    # start with 0 always
    while time.time()-t0 < time_limit:
        S=[0]
        order=allv[:]; rng.shuffle(order)
        Sset={0}
        for v in order:
            if v==0: continue
            if can_add_fast(S, v):
                S.append(v); Sset.add(v)
        if len(S)>len(best):
            best=S[:]
            if len(best)>=target:
                return best, time.time()-t0
    return best, time.time()-t0

if __name__=="__main__":
    n=int(sys.argv[1]); target=int(sys.argv[2]); tl=float(sys.argv[3]) if len(sys.argv)>3 else 30
    best, el=build_random(n,target,tl,seed=0)
    print(f"n={n} random-greedy best={len(best)} in {el:.1f}s")
