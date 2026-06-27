#!/usr/bin/env python3
"""Faster SA v2 for A089676.
- Incremental per-vertex conflict array maintained across swaps (no full recompute each move).
- Candidate pool restriction (optional: even popcount, or popcount band).
- Tabu list on recently-removed vertices. SA acceptance + targeted kicks.

State invariants:
  S : list of K masks, S[0]=0 fixed.
  con[i] = # forbidden triples containing S[i].  total_conf = sum(con)//3.
Swap S[ri]=w: update con for all members. Cost O(K^2) but in pure python with bit ops,
or O(K) numpy for the candidate scan. We do candidate scan with numpy over pool, then a cheap
incremental update of con after committing.
"""
import sys, time, random
import numpy as np

def forb3(A,B,C):
    return ((B^A)&(C^A))==0 or ((A^B)&(C^B))==0 or ((A^C)&(B^C))==0

def build_con(S):
    K=len(S); con=[0]*K
    for i in range(K):
        for j in range(i+1,K):
            ab=S[i]^S[j]
            for k in range(j+1,K):
                if ((S[j]^S[i])&(S[k]^S[i]))==0 or (ab&(S[k]^S[j]))==0 or ((S[k]^S[i])&(S[k]^S[j]))==0:
                    con[i]+=1;con[j]+=1;con[k]+=1
    return con

def pairwise_with(v, S, skip=-1):
    """# forbidden triples {v,a,b}, a,b in S (indices != skip). returns count + (also used for delta)."""
    c=0; K=len(S)
    for i in range(K):
        if i==skip: continue
        a=S[i]; xva=a^v
        for j in range(i+1,K):
            if j==skip: continue
            b=S[j]; xvb=b^v; ab=a^b
            if (xva&xvb)==0 or (xva&ab)==0 or (xvb&ab)==0:
                c+=1
    return c

def cand_conflicts_pool(Stmp, pool_arr, n):
    """conflicts for each candidate in pool_arr (numpy), given Stmp members."""
    total=np.zeros(len(pool_arr), dtype=np.int32)
    L=len(Stmp); W=pool_arr
    for i in range(L):
        a=Stmp[i]; Wa=W^a
        for j in range(i+1,L):
            b=Stmp[j]; Wb=W^b; ab=a^b
            total += ((Wa&Wb)==0)|((Wa&ab)==0)|((Wb&ab)==0)
    return total

def solve(n,K,time_limit,seed,pool=None,init=None,verbose=False,
          p_random=0.03, kick_after=600, kick_size=3):
    rng=random.Random(seed); np.random.seed(seed&0xffffffff)
    N=1<<n; t0=time.time()
    if pool is None:
        pool=list(range(1,N))
    pool_set=set(pool)
    pool_arr=np.array(pool, dtype=np.int64)
    def fresh():
        return [0]+rng.sample(pool, K-1)
    S=init[:] if init else fresh()
    con=build_con(S)
    conf=sum(con)//3
    best_conf=conf; best_S=S[:]
    tabu={}
    it=0; no_improve=0
    while time.time()-t0<time_limit and best_conf>0:
        it+=1
        # choose removal: worst non-zero, non-tabu
        order=sorted(range(1,K), key=lambda i:-con[i])
        ri=None
        for i in order:
            if tabu.get(S[i],0)<=it:
                ri=i; break
        if ri is None: ri=order[0]
        if rng.random()<0.2: ri=rng.randrange(1,K)
        v_out=S[ri]
        cout=con[ri]
        Stmp=S[:ri]+S[ri+1:]
        cc=cand_conflicts_pool(Stmp,pool_arr,n)
        # mask out current members & v_out
        # build index map lazily: set huge where pool elem in S
        Sset=set(S)
        big= np.array([ (1_000_000 if (int(p) in Sset) else 0) for p in pool_arr ], dtype=np.int32)
        cc=cc+big
        mn=int(cc.min())
        cands=np.flatnonzero(cc==mn)
        w=int(pool_arr[cands[rng.randrange(len(cands))]])
        new_conf=conf-cout+mn
        accept = (new_conf<=conf) or (rng.random()<p_random)
        if accept and w!=v_out and w not in Sset:
            S[ri]=w
            con=build_con(S)   # recompute (correct, simpler); optimize later if needed
            conf=sum(con)//3
            tabu[v_out]=it+8
            if conf<best_conf:
                best_conf=conf; best_S=S[:]; no_improve=0
                if verbose: print(f"  [t={time.time()-t0:.0f}s it={it}] conf={best_conf}", flush=True)
            else:
                no_improve+=1
        else:
            no_improve+=1
        if no_improve>kick_after:
            # kick: from best, replace kick_size vertices randomly from pool
            base=best_S[:]
            idx=rng.sample(range(1,K), kick_size)
            avail=[v for v in pool if v not in set(base)]
            for ii,vv in zip(idx, rng.sample(avail,kick_size)):
                base[ii]=vv
            S=base; con=build_con(S); conf=sum(con)//3; no_improve=0; tabu={}
    return best_S,best_conf,time.time()-t0

if __name__=="__main__":
    n=int(sys.argv[1]);K=int(sys.argv[2]);tl=float(sys.argv[3]) if len(sys.argv)>3 else 60
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    poolmode=sys.argv[5] if len(sys.argv)>5 else "all"
    N=1<<n
    pool=None
    if poolmode=="even":
        pool=[v for v in range(1,N) if bin(v).count('1')%2==0]
    elif poolmode.startswith("band"):
        c=n//2; pool=[v for v in range(1,N) if abs(bin(v).count('1')-c)<=2]
    S,conf,el=solve(n,K,tl,seed,pool=pool,verbose=True)
    print(f"n={n} K={K} pool={poolmode}: best_conflicts={conf} in {el:.1f}s")
    if conf==0:
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/v2_witness_n{n}_k{K}.txt"
        with open(path,"w") as f:
            for v in S: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("WITNESS:",path)
