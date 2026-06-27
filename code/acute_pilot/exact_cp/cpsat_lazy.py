#!/usr/bin/env python3
"""CP-SAT feasibility for A089676 with LAZY triple constraints.

Decision version: does an acute set of size >= K exist in {0,1}^n (containing 0 WLOG)?
We model binary x_v for each candidate vertex. Symmetry: fix x_0 = 1.
Pairwise '0-compatible' constraints are added eagerly as edges (clique requirement on S\{0}).
All-nonzero triple constraints are added LAZILY: solve, extract S, run exact checker,
add any violated triple as clause (not all three) repeat.

We also prune the candidate vertex set: a vertex P can only be in S (with 0) if it's
0-compatible with enough others; we keep all nonzero verts but rely on pairwise edges.

Usage: python3 cpsat_lazy.py <n> <K> [time_limit_s] [seed]
"""
import sys, time
from ortools.sat.python import cp_model

def popcount(x): return bin(x).count('1')

def solve(n, K, time_limit=600, seed=0, verbose=True):
    mask=(1<<n)-1
    V=list(range(1<<n))          # all vertices incl 0
    nz=[v for v in V if v!=0]
    t0=time.time()

    def compat0(P,R):
        return (P&R)!=0 and (P&~R&mask)!=0 and (R&~P&mask)!=0

    # Build model
    m=cp_model.CpModel()
    x={v: m.NewBoolVar(f"x{v}") for v in V}
    m.Add(x[0]==1)                       # fix 0
    m.Add(sum(x.values()) >= K)

    # Pairwise 0-compatibility: for every pair of nonzero P,R, if NOT compat0 then
    # they can't both be chosen WITH 0. Since 0 is forced in, forbid x[P]+x[R] <= 1.
    # This is O(nz^2) ~ 2M for n=11, 8M for n=12 -- add only the FORBIDDEN pairs.
    pair_count=0
    nzl=nz
    L=len(nzl)
    for i in range(L):
        P=nzl[i]
        # precompute
        for j in range(i+1,L):
            R=nzl[j]
            if not ((P&R)!=0 and (P&~R&mask)!=0 and (R&~P&mask)!=0):
                m.AddBoolOr([x[P].Not(), x[R].Not()])
                pair_count+=1
    if verbose: print(f"[setup] forbidden 0-pairs added: {pair_count}  ({time.time()-t0:.1f}s)")

    # Lazy triple loop via solution callback is complex; use iterative solve.
    # Build solver
    def ra(P,Q,R): return ((P^Q)&(R^Q))==0
    def violated_triples(S):
        """Return list of (A,B,C) unordered triples in S that are forbidden (any apex right angle)."""
        out=[]
        Sl=list(S)
        msk=[s for s in Sl]
        ln=len(Sl)
        for ai in range(ln):
            A=Sl[ai]
            for bi in range(ai+1,ln):
                B=Sl[bi]
                for ci in range(bi+1,ln):
                    C=Sl[ci]
                    if ra(B,A,C) or ra(A,B,C) or ra(A,C,B):
                        out.append((A,B,C))
        return out

    added_triples=set()
    it=0
    while True:
        it+=1
        solver=cp_model.CpSolver()
        solver.parameters.max_time_in_seconds=max(1.0, time_limit-(time.time()-t0))
        solver.parameters.random_seed=seed
        solver.parameters.num_search_workers=8
        st=solver.Solve(m)
        if st==cp_model.INFEASIBLE:
            if verbose: print(f"[it{it}] INFEASIBLE -> no acute set of size {K} (given added clauses). ({time.time()-t0:.1f}s)")
            return ("INFEASIBLE", None)
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            if verbose: print(f"[it{it}] status={solver.StatusName(st)} (timeout/unknown). ({time.time()-t0:.1f}s)")
            return ("TIMEOUT", None)
        S=[v for v in V if solver.Value(x[v])==1]
        viol=violated_triples(S)
        if not viol:
            if verbose: print(f"[it{it}] FEASIBLE acute set size {len(S)} found! ({time.time()-t0:.1f}s)")
            return ("FEASIBLE", S)
        # add violated triples as clauses
        for (A,B,C) in viol:
            key=(A,B,C)
            if key in added_triples: continue
            added_triples.add(key)
            m.AddBoolOr([x[A].Not(), x[B].Not(), x[C].Not()])
        if verbose and it%1==0:
            print(f"[it{it}] size={len(S)} violated_triples={len(viol)} total_lazy={len(added_triples)} ({time.time()-t0:.1f}s)")
        if time.time()-t0>time_limit:
            return ("TIMEOUT", None)

if __name__=="__main__":
    n=int(sys.argv[1]); K=int(sys.argv[2])
    tl=int(sys.argv[3]) if len(sys.argv)>3 else 600
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    res,S=solve(n,K,tl,seed)
    print("RESULT:",res, "size" if S else "", len(S) if S else "")
    if S is not None:
        with open(f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/witness_n{n}_k{K}.txt","w") as f:
            for v in S:
                f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("witness written")
