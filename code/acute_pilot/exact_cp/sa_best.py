#!/usr/bin/env python3
"""sa_best: numpy full-candidate-scan (global best move) + incremental con update.
Each move:
  1. pick removal slot ri (worst con, with noise, never 0, tabu-aware)
  2. numpy-scan ALL pool candidates -> conflicts(w | S\{ri}); pick min (global best swap-in)
  3. commit, update con incrementally (O(K^2) bit ops)
Validated to reproduce records; designed for parallel fleet.
"""
import sys, time, random
import numpy as np

def solve(n,K,time_limit,seed,pool=None,init=None,verbose=False,
          p_random=0.03, kick_after=1200, kick_size=4, reanneal_period=0):
    rng=random.Random(seed); np.random.seed(seed&0xffffffff)
    N=1<<n; t0=time.time()
    if pool is None: pool=list(range(1,N))
    pool_arr=np.array(pool, dtype=np.int64)
    poolL=len(pool)
    # map mask->pool index for masking S members (use dict for sparse pools)
    pool_index={int(v):i for i,v in enumerate(pool)}
    def fresh(): return [0]+rng.sample(pool,K-1)
    S=init[:] if init else fresh()
    Sset=set(S)
    con=[0]*K
    def rebuild():
        for i in range(K): con[i]=0
        for i in range(K):
            a=S[i]
            for j in range(i+1,K):
                b=S[j]; ab=a^b
                for k in range(j+1,K):
                    c=S[k]
                    if ((b^a)&(c^a))==0 or (ab&(c^b))==0 or ((c^a)&(c^b))==0:
                        con[i]+=1;con[j]+=1;con[k]+=1
    rebuild()
    conf=sum(con)//3
    best_conf=conf; best_S=S[:]
    tabu={}
    it=0; no_improve=0
    while time.time()-t0<time_limit and best_conf>0:
        it+=1
        # removal slot
        ri=-1; bc=-1
        for i in range(1,K):
            if tabu.get(S[i],0)>it: continue
            if con[i]>bc: bc=con[i]; ri=i
        if ri==-1: ri=1+rng.randrange(K-1)
        if rng.random()<0.15: ri=1+rng.randrange(K-1)
        u=S[ri]; cout=con[ri]
        Stmp=S[:ri]+S[ri+1:]
        # numpy scan
        total=np.zeros(poolL, dtype=np.int32)
        W=pool_arr
        for i in range(K-1):
            a=Stmp[i]; Wa=W^a
            for j in range(i+1,K-1):
                b=Stmp[j]; Wb=W^b; ab=a^b
                total += ((Wa&Wb)==0)|((Wa&ab)==0)|((Wb&ab)==0)
        # mask members
        for s in S:
            idx=pool_index.get(s)
            if idx is not None: total[idx]=1_000_000
        mn=int(total.min())
        cands=np.flatnonzero(total==mn)
        w=int(pool_arr[cands[rng.randrange(len(cands))]])
        new_conf=conf-cout+mn
        if (new_conf<=conf) or (rng.random()<p_random):
            if w in Sset:  # safety
                no_improve+=1; continue
            # incremental update: remove u
            for i in range(K):
                if i==ri: continue
                a=S[i]; xa=a^u
                for j in range(i+1,K):
                    if j==ri: continue
                    b=S[j]; xb=b^u; ab=a^b
                    if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0:
                        con[i]-=1; con[j]-=1
            S[ri]=w; Sset.discard(u); Sset.add(w)
            cw=0
            for i in range(K):
                if i==ri: continue
                a=S[i]; xa=a^w
                for j in range(i+1,K):
                    if j==ri: continue
                    b=S[j]; xb=b^w; ab=a^b
                    if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0:
                        con[i]+=1; con[j]+=1; cw+=1
            con[ri]=cw; conf=sum(con)//3
            tabu[u]=it+12
            if conf<best_conf:
                best_conf=conf; best_S=S[:]; no_improve=0
                if verbose: print(f"  [t={time.time()-t0:.0f}s it={it}] conf={best_conf}", flush=True)
            else: no_improve+=1
        else:
            no_improve+=1
        if no_improve>kick_after:
            base=best_S[:]
            idx=rng.sample(range(1,K),min(kick_size,K-1))
            avail=[v for v in pool if v not in set(base)]
            for ii,vv in zip(idx, rng.sample(avail,len(idx))):
                base[ii]=vv
            S=base; Sset=set(S); rebuild(); conf=sum(con)//3; no_improve=0; tabu={}
    return best_S,best_conf,time.time()-t0,it

if __name__=="__main__":
    n=int(sys.argv[1]);K=int(sys.argv[2]);tl=float(sys.argv[3]) if len(sys.argv)>3 else 60
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    poolmode=sys.argv[5] if len(sys.argv)>5 else "all"
    N=1<<n; pool=None
    if poolmode=="even": pool=[v for v in range(1,N) if bin(v).count('1')%2==0]
    elif poolmode=="band3": c=n//2; pool=[v for v in range(1,N) if abs(bin(v).count('1')-c)<=3]
    elif poolmode=="band2": c=n//2; pool=[v for v in range(1,N) if abs(bin(v).count('1')-c)<=2]
    S,conf,el,it=solve(n,K,tl,seed,pool=pool,verbose=True)
    print(f"n={n} K={K} pool={poolmode}: best_conflicts={conf} in {el:.1f}s iters={it} ({it/el:.0f}/s)")
    if conf==0:
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/best_witness_n{n}_k{K}.txt"
        with open(path,"w") as f:
            for v in S: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("WITNESS:",path)
