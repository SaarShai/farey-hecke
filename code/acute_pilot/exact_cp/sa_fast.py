#!/usr/bin/env python3
"""Fully numpy-vectorized SA for A089676. Both per-vertex contrib AND candidate eval vectorized.

State: set S (list of K masks, S[0]=0 fixed). conflicts = total forbidden triples.
Per move: vectorize conflicts(w) over all 2^n candidates for the chosen removed slot.
Per-vertex contributions computed by one O(K^2) numpy pass (vector over the K members).
"""
import sys, time, random
import numpy as np

def member_contribs(S, n):
    """contrib[i] = # forbidden triples in S that contain S[i]. Vectorized over members."""
    A=np.array(S, dtype=np.int64)
    K=len(S)
    contrib=np.zeros(K, dtype=np.int64)
    # For each ordered pair (i,j) i<j compute, for all k, forb3(S[i],S[j],S[k]) ... that's O(K^3).
    # Instead: for each pair (i,j), the # of k making {i,j,k} forbidden contributes to i,j,k.
    # We need per-pair vector over k. Loop pairs O(K^2), each does numpy over K. Total O(K^3) but in numpy.
    for i in range(K):
        a=S[i]; Aa=A^a
        for j in range(i+1,K):
            b=S[j]; ab=a^b; Ab=A^b
            # forb3(a,b,S[k]) for all k: with c=S[k]
            # (b^a)&(c^a)==0  -> ab & Aa ... wait need (S[k]^a). Aa=A^a is (S[k]^a). 
            # cond1: (b^a)&(c^a)==0 = ab & (c^a)==0 -> ab & Aa ==0
            # cond2: (a^b)&(c^b)==0 = ab & (c^b)==0 -> ab & Ab ==0
            # cond3: (a^c)&(b^c)==0 = (c^a)&(c^b)==0 -> Aa & Ab ==0
            m = ((ab & Aa)==0) | ((ab & Ab)==0) | ((Aa & Ab)==0)
            m[i]=False; m[j]=False
            cnt=int(m.sum())
            # each true k => triple {i,j,k} forbidden
            contrib[i]+=cnt; contrib[j]+=cnt
            contrib[np.flatnonzero(m)] += 1
    # Every forbidden triple is enumerated by all 3 of its pairs, each enumeration adds
    # 1 to all 3 members -> contrib is uniformly 3x the true per-vertex triple count.
    return contrib // 3

def cand_conflicts(Stmp, n):
    N=1<<n
    W=np.arange(N, dtype=np.int64)
    total=np.zeros(N, dtype=np.int32)
    L=len(Stmp)
    for i in range(L):
        a=Stmp[i]; Wa=W^a
        for j in range(i+1,L):
            b=Stmp[j]; Wb=W^b; ab=a^b
            total += ((Wa&Wb)==0)|((Wa&ab)==0)|((Wb&ab)==0)
    return total

def total_conf(S):
    c=0; L=len(S)
    for i in range(L):
        a=S[i]
        for j in range(i+1,L):
            b=S[j]; ab=a^b
            for k in range(j+1,L):
                cc=S[k]
                if ((b^a)&(cc^a))==0 or (ab&(cc^b))==0 or ((cc^a)&(cc^b))==0:
                    c+=1
    return c

def solve(n,K,time_limit,seed,init=None,verbose=True, p_random=0.04, perturb_after=2000):
    rng=random.Random(seed); np.random.seed(seed&0xffffffff)
    N=1<<n; t0=time.time()
    def fresh():
        return [0]+rng.sample(range(1,N),K-1)
    S=init[:] if init else fresh()
    conf=total_conf(S)
    best_conf=conf; best_S=S[:]
    no_improve=0; it=0
    while time.time()-t0<time_limit and best_conf>0:
        it+=1
        contrib=member_contribs(S,n)
        contrib[0]=-1  # never remove 0
        # pick removal: worst vertex w.p. 1-p, else random nonzero
        if rng.random()<0.75:
            ri=int(np.argmax(contrib))
        else:
            ri=rng.randrange(1,K)
        if S[ri]==0: ri=1
        cout=int(contrib[ri])
        Stmp=S[:ri]+S[ri+1:]
        cc=cand_conflicts(Stmp,n)
        for s in Stmp: cc[s]=10**6
        cc[S[ri]]=10**6
        mn=int(cc.min())
        bestw=np.flatnonzero(cc==mn)
        w=int(bestw[rng.randrange(len(bestw))])
        new_conf=conf-cout+mn
        if new_conf<=conf or rng.random()<p_random:
            S[ri]=w; conf=new_conf
            if conf<best_conf:
                best_conf=conf; best_S=S[:]; no_improve=0
                if verbose: print(f"  [t={time.time()-t0:.0f}s it={it}] conflicts={best_conf}")
            else:
                no_improve+=1
        else:
            no_improve+=1
        if no_improve>perturb_after:
            base=best_S
            keep=[0]+rng.sample([v for v in base if v!=0], (K-1)*2//3)
            pool=[v for v in range(1,N) if v not in set(keep)]
            S=keep+rng.sample(pool, K-len(keep))
            conf=total_conf(S); no_improve=0
    return best_S,best_conf,time.time()-t0

if __name__=="__main__":
    n=int(sys.argv[1]);K=int(sys.argv[2]);tl=float(sys.argv[3]) if len(sys.argv)>3 else 60
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    S,conf,el=solve(n,K,tl,seed)
    print(f"n={n} K={K}: best_conflicts={conf} in {el:.1f}s")
    if conf==0:
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/fast_witness_n{n}_k{K}.txt"
        with open(path,"w") as f:
            for v in S: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("WITNESS:",path)
