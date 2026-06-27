#!/usr/bin/env python3
"""Numpy-vectorized min-conflicts SA for A089676.

We vectorize the cost of ADDING a candidate w to a fixed support set Stmp (size K-1):
conflicts(w) = #{ unordered pairs (a,b) in Stmp : forb3(w,a,b) }.
forb3(w,a,b) = [ (w^a)&(w^b)==0 ] or [ (w^a)&(a^b)==0 ] or [ (w^b)&(a^b)==0 ].

For a FIXED pair (a,b) we can vectorize over all w in 0..2^n-1 using numpy uint arrays.
But that's 2^n * K^2 work. Instead: for the swap step we only need conflicts(w) for all w,
given Stmp. Loop over the C(K-1,2) pairs (~300), each pair contributes a boolean mask over
all 2^n candidates computed with numpy bitops. Sum masks -> conflict count per candidate.
Cost per full evaluation: ~300 * 2^n numpy ops. For n=11 (2048): 300*2048=600k ops -> ~ms.
Then pick argmin among non-S candidates (+ the removed vertex's slot). This is a strong
'best swap' local search; add SA noise + restarts.
"""
import sys, time, random
import numpy as np

def conflicts_per_candidate(Stmp, n):
    """Return int array len 2^n: conflicts(w) = # forbidden triples {w,a,b}, a,b in Stmp."""
    N=1<<n
    W=np.arange(N, dtype=np.int64)
    total=np.zeros(N, dtype=np.int32)
    L=len(Stmp)
    A=Stmp
    for i in range(L):
        a=A[i]
        Wa = W ^ a          # w^a
        for j in range(i+1,L):
            b=A[j]
            Wb = W ^ b
            ab = a^b
            # forbidden if any of the three ==0
            m = ((Wa & Wb)==0) | ((Wa & ab)==0) | ((Wb & ab)==0)
            total += m
    return total

def solve(n, K, time_limit, seed, verbose=True, init=None):
    rng=random.Random(seed)
    np.random.seed(seed)
    N=1<<n
    t0=time.time()
    best_conf=10**9; best_S=None
    def fresh():
        return [0]+rng.sample(range(1,N), K-1)
    S = init[:] if init else fresh()
    Sset=set(S)
    no_improve=0
    reheat=0
    # current total conflicts
    def total_conf(S):
        # via per-candidate trick: sum over vertices of conflicts(v|S\{v}) / 3
        c=0; L=len(S)
        for i in range(L):
            for j in range(i+1,L):
                for k in range(j+1,L):
                    a,b,cc=S[i],S[j],S[k]
                    if ((b^a)&(cc^a))==0 or ((a^b)&(cc^b))==0 or ((a^cc)&(b^cc))==0:
                        c+=1
        return c
    conf=total_conf(S)
    best_conf=conf; best_S=S[:]
    it=0
    while time.time()-t0<time_limit and best_conf>0:
        it+=1
        # choose a vertex to remove (not 0). Prefer high-conflict: compute per-vertex contrib cheaply
        # contrib(v) = conflicts(v | S\{v})
        # pick the worst among a random sample of positions, or full scan occasionally
        idxs=[i for i in range(K) if S[i]!=0]
        # compute contrib for all -> pick worst with noise
        contribs=[]
        for i in idxs:
            Stmp=S[:i]+S[i+1:]
            # contrib = conflicts of S[i] vs Stmp  (cheap pairwise)
            v=S[i]; c=0
            xv=[s^v for s in Stmp]
            Lt=len(Stmp)
            for p in range(Lt):
                xvp=xv[p]; ap=Stmp[p]
                for q in range(p+1,Lt):
                    xvq=xv[q]; abq=ap^Stmp[q]
                    if (xvp&xvq)==0 or (xvp&abq)==0 or (xvq&abq)==0:
                        c+=1
            contribs.append((c,i))
        contribs.sort(reverse=True)
        # pick among top with randomness (SA-ish): mostly worst, sometimes random
        if rng.random()<0.7:
            _,ri = contribs[0]
        else:
            _,ri = rng.choice(contribs)
        v_out=S[ri]
        Stmp=S[:ri]+S[ri+1:]
        cc = conflicts_per_candidate(Stmp, n)   # numpy array over all candidates
        # forbid current members
        for s in Stmp: cc[s]=10**6
        cc[0]=10**6  # 0 stays via Stmp anyway; don't re-add 0
        cout = contribs[[i for _,i in contribs].index(ri)][0] if False else None
        # find best candidate(s): min conflicts
        mn=cc.min()
        bestw=np.flatnonzero(cc==mn)
        w=int(bestw[rng.randrange(len(bestw))])
        # accept (this is greedy best-improvement; add occasional random worse move)
        new_conf = conf - (sum(c for c,i in contribs if i==ri)) + int(mn)
        # the removed-vertex contribution:
        cout_val = dict((i,c) for c,i in contribs)[ri]
        new_conf = conf - cout_val + int(mn)
        if new_conf <= conf or rng.random()<0.05:
            S[ri]=w; Sset.discard(v_out); Sset.add(w)
            conf=new_conf
            if conf<best_conf:
                best_conf=conf; best_S=S[:]; no_improve=0
                if verbose: print(f"  [t={time.time()-t0:.0f}s it={it}] conflicts={best_conf}")
                if best_conf==0: break
            else:
                no_improve+=1
        else:
            no_improve+=1
        if no_improve>1500:
            # perturb: random restart keeping best half
            keep=best_S[:1] + rng.sample(best_S[1:], K//2)
            rest=rng.sample([v for v in range(1,N) if v not in set(keep)], K-len(keep))
            S=keep+rest; Sset=set(S); conf=total_conf(S); no_improve=0
    return best_S, best_conf, time.time()-t0

if __name__=="__main__":
    n=int(sys.argv[1]); K=int(sys.argv[2]); tl=float(sys.argv[3]) if len(sys.argv)>3 else 60
    seed=int(sys.argv[4]) if len(sys.argv)>4 else 0
    S,conf,el=solve(n,K,tl,seed)
    print(f"n={n} K={K}: best_conflicts={conf} in {el:.1f}s  iters_done")
    if conf==0:
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/sanp_witness_n{n}_k{K}.txt"
        with open(path,"w") as f:
            for v in S:
                f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        print("WITNESS:",path)
