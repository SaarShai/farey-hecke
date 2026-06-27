#!/usr/bin/env python3
"""Classic Metropolis SA (slow geometric cooling) for A089676 fixed-size K.
Different dynamics from sa_best's greedy best-swap: accepts worse moves by exp(-dE/T),
long cooling schedule, reheats. Move = single random swap (remove random nonzero, add random
non-member). Incremental conflict via per-vertex con array. This explores barriers greedy can't.
"""
import sys, time, random

def solve(n,K,time_limit,seed,init=None,verbose=False,T0=4.0,Tmin=0.05,alpha=0.99995):
    rng=random.Random(seed)
    N=1<<n; t0=time.time()
    pool=list(range(1,N))
    S=init[:] if init else [0]+rng.sample(pool,K-1)
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
    best=conf; bestS=S[:]
    T=T0; it=0
    def cw(w, ri):
        c=0
        for i in range(K):
            if i==ri: continue
            a=S[i]; xa=a^w
            for j in range(i+1,K):
                if j==ri: continue
                b=S[j]; xb=b^w; ab=a^b
                if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0: c+=1
        return c
    while time.time()-t0<time_limit and best>0:
        it+=1
        T=max(Tmin, T*alpha)
        if T<=Tmin: T=T0  # reheat
        ri=1+rng.randrange(K-1)
        u=S[ri]
        w=pool[rng.randrange(len(pool))]
        if w in Sset: continue
        cout=con[ri]
        cin=cw(w, ri)
        dE=cin-cout
        if dE<=0 or rng.random()<pow(2.718281828, -dE/T):
            # commit incremental
            for i in range(K):
                if i==ri: continue
                a=S[i]; xa=a^u
                for j in range(i+1,K):
                    if j==ri: continue
                    b=S[j]; xb=b^u; ab=a^b
                    if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0:
                        con[i]-=1; con[j]-=1
            S[ri]=w; Sset.discard(u); Sset.add(w)
            cwn=0
            for i in range(K):
                if i==ri: continue
                a=S[i]; xa=a^w
                for j in range(i+1,K):
                    if j==ri: continue
                    b=S[j]; xb=b^w; ab=a^b
                    if (xa&xb)==0 or (xa&ab)==0 or (xb&ab)==0:
                        con[i]+=1;con[j]+=1; cwn+=1
            con[ri]=cwn; conf=sum(con)//3
            if conf<best:
                best=conf; bestS=S[:]
                if verbose: print(f"  [t={time.time()-t0:.0f}s it={it} T={T:.2f}] conf={best}", flush=True)
    return bestS,best,time.time()-t0,it

if __name__=="__main__":
    n=int(sys.argv[1]);K=int(sys.argv[2]);tl=float(sys.argv[3]) if len(sys.argv)>3 else 120
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    S,conf,el,it=solve(n,K,tl,seed,verbose=True)
    print(f"classic-SA n={n} K={K}: best_conf={conf} in {el:.0f}s iters={it} ({it/el:.0f}/s)")
    if conf==0:
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/classic_witness_n{n}_k{K}.txt"
        with open(path,"w") as f:
            for v in S: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("WITNESS:",path)
