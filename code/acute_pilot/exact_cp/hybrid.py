#!/usr/bin/env python3
"""Hybrid: SA to a near-miss K-set (few conflicts), then EXACT-repair.
1. Run sa_best at size K -> get S with c conflicts (c small).
2. Identify the vertices involved in conflicts; remove them (the 'conflict core' is kept).
3. Exact max_extension on the conflict-free core seeking to reach K again WITHOUT conflicts.
Repeat with fresh SA starts. If exact-repair reaches K with 0 conflicts -> acute K-set.
"""
import sys, time, random
sys.path.insert(0,'/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp')
import sa_best, lns
from core import is_acute_masks

def conflict_vertices(S):
    """return indices of vertices in >=1 forbidden triple."""
    K=len(S); bad=set()
    for i in range(K):
        for j in range(i+1,K):
            ab=S[i]^S[j]
            for k in range(j+1,K):
                a,b,c=S[i],S[j],S[k]
                if ((b^a)&(c^a))==0 or (ab&(c^b))==0 or ((c^a)&(c^b))==0:
                    bad.add(i);bad.add(j);bad.add(k)
    return bad

def run(n,K,time_limit,seed,verbose=False):
    rng=random.Random(seed); t0=time.time()
    best_overall=10**9
    while time.time()-t0<time_limit:
        # SA phase (short) to get a low-conflict K-set
        S,conf,el,it=sa_best.solve(n,K,min(45,time_limit-(time.time()-t0)),seed,verbose=False)
        if conf==0:
            return S, time.time()-t0
        if conf<best_overall:
            best_overall=conf
            if verbose: print(f"  [t={time.time()-t0:.0f}s] SA conflicts={conf}", flush=True)
        # exact-repair: remove conflict vertices, refill
        bad=conflict_vertices(S)
        bad.discard(S.index(0) if 0 in S else -1)
        core=[S[i] for i in range(K) if i not in bad and S[i]!=0]
        if 0 in S: core=[0]+core
        need=K-len(core)
        if need>0 and len(core)>=K-12:  # only if removal is modest enough for exact
            ext=lns.max_extension(core, n, need, time_limit=min(20,time_limit-(time.time()-t0)), t0=time.time())
            if ext is not None and len(core)+len(ext)>=K:
                cand=core+ext[:K-len(core)]
                if is_acute_masks(cand) and len(cand)>=K:
                    return cand, time.time()-t0
        seed+=1
    return None, time.time()-t0

if __name__=="__main__":
    n=int(sys.argv[1]);K=int(sys.argv[2]);tl=float(sys.argv[3]) if len(sys.argv)>3 else 120
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    S,el=run(n,K,tl,seed,verbose=True)
    if S:
        print(f"*** FOUND size {len(S)} acute in {{0,1}}^{n} ({el:.0f}s) ***")
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/hybrid_witness_n{n}_k{K}.txt"
        with open(path,"w") as f:
            for v in S: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("WITNESS:",path)
    else:
        print(f"n={n} K={K}: no acute {K}-set found in {el:.0f}s")
