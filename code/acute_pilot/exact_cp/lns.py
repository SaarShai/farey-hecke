#!/usr/bin/env python3
"""Large-Neighborhood Search (destroy + EXACT repair) for A089676.

Take a current acute set S (size K-1 or a near-miss size K). To reach size K:
  - Keep a subset 'core' of S of size K-1-d (remove d vertices).
  - EXACTLY search for the maximum number of vertices that can be added to 'core'
    (via backtracking restricted to candidates compatible with core), seeking core_size+? >= K.
If we find an extension reaching size K -> acute K-set found.

This explores a large neighborhood (all ways to optimally re-fill d+1 slots) exactly,
far stronger than single-vertex swaps. d is the 'destroy size' (3..7 tractable).
"""
import sys, time, random
sys.path.insert(0,'/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp')

def forb3(A,B,C):
    return ((B^A)&(C^A))==0 or ((A^B)&(C^B))==0 or ((A^C)&(B^C))==0

def compat(v, core):
    for i in range(len(core)):
        a=core[i]; xa=a^v
        for j in range(i+1,len(core)):
            b=core[j]; xb=b^v; ab=a^b
            if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0:
                return False
    return True

def max_extension(core, n, need, time_limit, t0):
    """Exact: can we add >=need vertices to 'core' keeping acute? Return an extension list of size>=need or None.
    Backtracking over candidate vertices (those compatible with core), MIS-style index order."""
    N=1<<n
    cand=[v for v in range(N) if v not in set(core) and compat(v, core)]
    # order candidates by popcount-mid then value for better early hits
    c=n/2
    cand.sort(key=lambda v:(abs(bin(v).count('1')-c), v))
    best=[0]; bestext=[None]
    found=[None]; timed_out=[False]
    def bt(added, C, start):
        if found[0] is not None: return
        if time.time()-t0>time_limit: timed_out[0]=True; return
        if len(added)>=need:
            found[0]=added[:]; return
        # bound: added + remaining candidates < need -> prune
        if len(added)+(len(C)-start)<need: return
        for idx in range(start, len(C)):
            if found[0] is not None: return
            if time.time()-t0>time_limit: timed_out[0]=True; return
            if len(added)+(len(C)-idx)<need: return
            v=C[idx]
            # v compatible with core (precomputed) and must be compatible with current 'added'
            ok=True
            for u in added:
                xu=v^u
                for s in core:
                    xs=v^s; us=u^s
                    if (xu&xs)==0 or (xu&us)==0 or (xs&us)==0:
                        ok=False; break
                if not ok: break
                # also triple within added+v among themselves+core handled by pairwise w/ core;
                # need triples (v,u,u2) for u,u2 in added:
            if ok:
                for a_i in range(len(added)):
                    for a_j in range(a_i+1,len(added)):
                        if forb3(v, added[a_i], added[a_j]):
                            ok=False; break
                    if not ok: break
            if not ok: continue
            added.append(v)
            bt(added, C, idx+1)
            added.pop()
    bt([], cand, 0)
    # expose completion status for rigorous certificates: complete == search exhausted
    max_extension.last_timed_out = timed_out[0] and found[0] is None
    return found[0]
max_extension.last_timed_out = False

def lns(n, K, time_limit, seed, init=None, d=4, verbose=False):
    rng=random.Random(seed); t0=time.time()
    N=1<<n
    # get a starting acute set of size K-1 (use SA or record-translate or greedy)
    import sa_best
    if init is None:
        S,conf,el,it=sa_best.solve(n, K-1, min(60,time_limit), seed, verbose=False)
        if conf!=0:
            # fall back: greedy
            pass
        cur=S
    else:
        cur=init[:]
    # ensure cur is acute of size K-1
    # LNS loop: destroy d, exact-repair seeking d+1 (to grow by 1)
    best_size=len(cur)
    best_set=cur[:]
    while time.time()-t0<time_limit:
        if len(cur)>=K:
            return cur, time.time()-t0
        # pick core: remove d random (keep 0)
        nonzero_idx=[i for i in range(len(cur)) if cur[i]!=0]
        rem=set(rng.sample(nonzero_idx, min(d,len(nonzero_idx))))
        core=[cur[i] for i in range(len(cur)) if i not in rem]
        need=(len(cur)-len(core))+1   # to grow by 1 overall
        ext=max_extension(core, n, need, time_limit, t0)
        if ext is not None and len(core)+len(ext)>len(cur):
            cur=core+ext
            if len(cur)>best_size:
                best_size=len(cur); best_set=cur[:]
                if verbose: print(f"  [t={time.time()-t0:.0f}s] grew to size {len(cur)}", flush=True)
                if len(cur)>=K: return cur, time.time()-t0
        else:
            # no growth this core; occasionally perturb cur via a random valid swap to diversify
            # try a different core next iter (loop). Add light randomization: re-fill core to same size.
            ext2=max_extension(core, n, len(cur)-len(core), time_limit, t0)
            if ext2 is not None and rng.random()<0.5:
                cur=core+ext2  # lateral move (same size, different set)
    return best_set, time.time()-t0

if __name__=="__main__":
    n=int(sys.argv[1]);K=int(sys.argv[2]);tl=float(sys.argv[3]) if len(sys.argv)>3 else 120
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    d=int(sys.argv[5]) if len(sys.argv)>5 else 4
    cur,el=lns(n,K,tl,seed,d=d,verbose=True)
    print(f"n={n} K={K} d={d}: best_size={len(cur)} in {el:.1f}s")
    if len(cur)>=K:
        from core import is_acute_masks
        assert is_acute_masks(cur), "BUG not acute"
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/lns_witness_n{n}_k{K}.txt"
        with open(path,"w") as f:
            for v in cur: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("WITNESS:",path)
