#!/usr/bin/env python3
"""Simulated-annealing / tabu engine for A089676 fixed-size acute sets.

Formulation: fix target size K. Maintain a multiset-free set S of K distinct vertices.
Objective = number of forbidden (ordered-collapsed) triples in S = "conflicts".
Acute set <=> conflicts==0. SA over swaps (replace one vertex by an outside vertex).

Incremental conflict delta on swap is the engine's hot loop, done with bit ops.
A triple {A,B,C} forbidden iff forb3. conflicts(S)=sum over triples.
On removing v: subtract triples containing v. On adding w: add triples containing w.
We maintain per-vertex conflict contribution to pick worst vertices.
"""
import sys, time, random

def forb3(A,B,C):
    return ((B^A)&(C^A))==0 or ((A^B)&(C^B))==0 or ((A^C)&(B^C))==0

def pair_conflicts_with(v, S):
    """number of forbidden triples {v,a,b} with a,b in S (v not in S)."""
    c=0; L=len(S)
    xv=[s^v for s in S]
    for i in range(L):
        a=S[i]; xva=xv[i]
        for j in range(i+1,L):
            b=S[j]; xvb=xv[j]
            ab=a^b
            if (xva&xvb)==0 or (xva&ab)==0 or (xvb&ab)==0:
                c+=1
    return c

def total_conflicts(S):
    c=0; L=len(S)
    for i in range(L):
        a=S[i]
        for j in range(i+1,L):
            b=S[j]; ab=a^b; xa=a^a # noop
            for k in range(j+1,L):
                cc=S[k]
                if forb3(a,b,cc): c+=1
    return c

def per_vertex_conflicts(S):
    """contribution of each vertex = #forbidden triples containing it."""
    L=len(S)
    contrib=[0]*L
    for i in range(L):
        for j in range(i+1,L):
            for k in range(j+1,L):
                if forb3(S[i],S[j],S[k]):
                    contrib[i]+=1; contrib[j]+=1; contrib[k]+=1
    return contrib

def sa(n, K, time_limit, seed, init=None, restarts=True, T0=2.0, cool=0.9995, verbose=True):
    rng=random.Random(seed)
    allv=list(range(1<<n))
    t0=time.time()
    best_conf=10**9; best_S=None
    def fresh_init():
        # WLOG include 0
        S=[0]+rng.sample([v for v in allv if v!=0], K-1)
        return S
    S = init[:] if init else fresh_init()
    conf=total_conflicts(S)
    Sset=set(S)
    T=T0
    iters=0
    last_improve=0
    while time.time()-t0 < time_limit:
        iters+=1
        T*=cool
        if T<0.01: T=T0  # reheat
        # pick a vertex to remove: bias toward high-conflict vertices
        # compute per-vertex occasionally; here pick the most-conflicting with prob, else random
        # cheap: pick random index, but weight by recomputing contribution of a few
        ri = rng.randrange(K)
        # ensure we don't always remove 0 (keep 0 fixed for symmetry) -> skip index of 0
        if S[ri]==0:
            ri=(ri+1)%K
        v_out=S[ri]
        # pick candidate in
        # try several candidates, choose best delta
        cand=None; best_delta=None
        Stmp=S[:ri]+S[ri+1:]
        # current conflicts contributed by v_out:
        cout = pair_conflicts_with(v_out, Stmp)
        for _ in range(8):
            w=rng.randrange(1<<n)
            if w in Sset and w!=v_out: continue
            cin = pair_conflicts_with(w, Stmp)
            delta = cin - cout
            if best_delta is None or delta<best_delta:
                best_delta=delta; cand=w; cand_cin=cin
        if cand is None: continue
        # SA accept
        if best_delta<=0 or rng.random() < pow(2.718281828, -best_delta/max(T,1e-6)):
            Sset.discard(v_out); 
            if cand in Sset: 
                continue
            S[ri]=cand; Sset.add(cand)
            conf += best_delta
            if conf<best_conf:
                best_conf=conf; best_S=S[:]; last_improve=iters
                if verbose and best_conf<=5:
                    print(f"  [t={time.time()-t0:.0f}s it={iters}] conflicts={best_conf}")
                if best_conf==0:
                    return best_S, 0, time.time()-t0
        # restart if stuck
        if restarts and iters-last_improve > 20000:
            S=fresh_init(); conf=total_conflicts(S); Sset=set(S); T=T0; last_improve=iters
    return best_S, best_conf, time.time()-t0

if __name__=="__main__":
    n=int(sys.argv[1]); K=int(sys.argv[2]); tl=float(sys.argv[3]) if len(sys.argv)>3 else 60
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    S,conf,el=sa(n,K,tl,seed)
    print(f"n={n} K={K}: best_conflicts={conf} in {el:.1f}s")
    if conf==0:
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/sa_witness_n{n}_k{K}.txt"
        with open(path,"w") as f:
            for v in S:
                f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("WITNESS:",path)
