#!/usr/bin/env python3
"""SA v3: incremental conflict updates, fast inner loop, parallel-friendly.
con[i] = #forbidden triples containing S[i]. On swapping out S[ri]=u, in w:
  - remove all triples containing u: for each pair (a,b) in S\{u}, if forb3(u,a,b): con[a]-=1,con[b]-=1; con[u] reset.
  - add all triples containing w: symmetric.
This is O(K^2) per move in pure python with bit ops (~K^2=600 ops). ~50k+ moves/sec.
Candidate choice: evaluate a sampled subset of pool with pairwise count, pick best (avoids 2^n numpy scan).
"""
import sys, time, random

def solve(n,K,time_limit,seed,pool=None,init=None,verbose=False,
          n_cand=64, p_random=0.02, kick_after=4000, kick_size=4, reanneal=True):
    rng=random.Random(seed)
    N=1<<n; mask=N-1; t0=time.time()
    if pool is None: pool=list(range(1,N))
    poolL=len(pool)
    def fresh():
        return [0]+rng.sample(pool,K-1)
    S=init[:] if init else fresh()
    Sset=set(S)
    # con array
    con=[0]*K
    def rebuild_con():
        for i in range(K): con[i]=0
        for i in range(K):
            a=S[i]
            for j in range(i+1,K):
                b=S[j]; ab=a^b
                for k in range(j+1,K):
                    c=S[k]
                    if ((b^a)&(c^a))==0 or (ab&(c^b))==0 or ((c^a)&(c^b))==0:
                        con[i]+=1;con[j]+=1;con[k]+=1
    rebuild_con()
    conf=sum(con)//3
    best_conf=conf; best_S=S[:]
    # index lookup
    pos={v:i for i,v in enumerate(S)}
    it=0; no_improve=0
    def pair_count(v, skip_idx):
        """#forbidden triples {v,a,b}, a,b=S members idx != skip_idx."""
        c=0
        for i in range(K):
            if i==skip_idx: continue
            a=S[i]; xa=a^v
            for j in range(i+1,K):
                if j==skip_idx: continue
                b=S[j]; xb=b^v; ab=a^b
                if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0:
                    c+=1
        return c
    tabu={}
    while time.time()-t0<time_limit and best_conf>0:
        it+=1
        # pick removal slot: worst con, non-tabu, not 0
        ri=-1; bestcon=-1
        for i in range(1,K):
            if tabu.get(S[i],0)>it: continue
            if con[i]>bestcon: bestcon=con[i]; ri=i
        if ri==-1:
            ri=1+rng.randrange(K-1)
        if rng.random()<0.15: ri=1+rng.randrange(K-1)
        u=S[ri]; cout=con[ri]
        # sample candidates
        best_w=None; best_cin=None
        tries=0
        for _ in range(n_cand):
            w=pool[rng.randrange(poolL)]
            if w in Sset: continue
            cin=pair_count(w, ri)
            if best_cin is None or cin<best_cin:
                best_cin=cin; best_w=w
                if cin==0: break
        if best_w is None: continue
        new_conf=conf-cout+best_cin
        if new_conf<=conf or rng.random()<p_random:
            # commit swap: incremental con update
            # remove u: subtract triples containing u
            for i in range(K):
                if i==ri: continue
                a=S[i]; xa=a^u
                for j in range(i+1,K):
                    if j==ri: continue
                    b=S[j]; xb=b^u; ab=a^b
                    if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0:
                        con[i]-=1; con[j]-=1
            # place w
            S[ri]=w; Sset.discard(u); Sset.add(w)
            # add w triples
            cw=0
            for i in range(K):
                if i==ri: continue
                a=S[i]; xa=a^w
                for j in range(i+1,K):
                    if j==ri: continue
                    b=S[j]; xb=b^w; ab=a^b
                    if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0:
                        con[i]+=1; con[j]+=1; cw+=1
            con[ri]=cw
            conf=sum(con)//3
            tabu[u]=it+10
            if conf<best_conf:
                best_conf=conf; best_S=S[:]; no_improve=0
                if verbose: print(f"  [t={time.time()-t0:.0f}s it={it}] conf={best_conf}", flush=True)
            else:
                no_improve+=1
        else:
            no_improve+=1
        if no_improve>kick_after:
            base=best_S[:]
            idx=rng.sample(range(1,K),kick_size)
            avail=[v for v in pool if v not in set(base)]
            for ii,vv in zip(idx, rng.sample(avail,kick_size)):
                base[ii]=vv
            S=base; Sset=set(S); rebuild_con(); conf=sum(con)//3; no_improve=0; tabu={}
    return best_S,best_conf,time.time()-t0, it

if __name__=="__main__":
    n=int(sys.argv[1]);K=int(sys.argv[2]);tl=float(sys.argv[3]) if len(sys.argv)>3 else 60
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    poolmode=sys.argv[5] if len(sys.argv)>5 else "all"
    N=1<<n; pool=None
    if poolmode=="even": pool=[v for v in range(1,N) if bin(v).count('1')%2==0]
    elif poolmode=="band3": c=n//2; pool=[v for v in range(1,N) if abs(bin(v).count('1')-c)<=3]
    S,conf,el,it=solve(n,K,tl,seed,pool=pool,verbose=True)
    print(f"n={n} K={K} pool={poolmode}: best_conflicts={conf} in {el:.1f}s iters={it} ({it/el:.0f}/s)")
    if conf==0:
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/v3_witness_n{n}_k{K}.txt"
        with open(path,"w") as f:
            for v in S: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("WITNESS:",path)
