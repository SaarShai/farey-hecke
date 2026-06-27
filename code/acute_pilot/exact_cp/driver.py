#!/usr/bin/env python3
"""Multi-seed driver for sa_fast. Runs seeds sequentially within a wall budget,
tracks best conflict count, writes witness on conflicts==0, logs progress.
Also supports 'extend' mode: seed from a known acute set of size K-1 + 1 random vertex.
"""
import sys, time, random, re
sys.path.insert(0,'/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp')
import sa_fast

def load_records():
    txt=open('/Users/za/Documents/farey-hecke/code/acute_pilot/a089676_witnesses.txt').read()
    parts=re.split(r'a\((\d+)\)\s*>=\s*(\d+):', txt); W={}
    for i in range(1,len(parts),3):
        nn=int(parts[i]); rows=re.findall(r'\(([01\s]+)\)', parts[i+2]); masks=[]
        for r in rows:
            bits=[c for c in r if c in '01']; v=0
            for k,c in enumerate(bits):
                if c=='1': v|=1<<k
            masks.append(v)
        W[nn]=masks
    return W

def run(n,K,total_budget,base_seed=0,mode="scratch",per_seed=None):
    t0=time.time()
    W=load_records()
    best_overall=10**9; best_S=None; seed=base_seed
    if per_seed is None: per_seed=min(120, total_budget)
    while time.time()-t0 < total_budget:
        rng=random.Random(seed*999+1)
        init=None
        if mode=="extend" and (K-1) in [len(W.get(n,[]))] :
            pass
        if mode=="extend":
            rec=W[n]; t=rec[0]; base=[m^t for m in rec]  # contains 0, size = a(n)
            # extend to K: add (K-len(base)) random new vertices
            pool=[v for v in range(1,1<<n) if v not in set(base)]
            extra=rng.sample(pool, K-len(base))
            init=base+extra
        elif mode=="perturb_extend":
            rec=W[n]; t=rec[0]; base=[m^t for m in rec]
            # drop a few from base, add fresh to reach K
            keep=[0]+rng.sample([v for v in base if v!=0], len(base)-1-2)
            pool=[v for v in range(1,1<<n) if v not in set(keep)]
            init=keep+rng.sample(pool, K-len(keep))
        rem=total_budget-(time.time()-t0)
        budget=min(per_seed, rem)
        S,conf,el=sa_fast.solve(n,K,budget,seed,init=init,verbose=False)
        if conf<best_overall:
            best_overall=conf; best_S=S[:]
            print(f"[seed {seed} mode={mode}] conf={conf} (best={best_overall}) t={time.time()-t0:.0f}s", flush=True)
        if conf==0:
            path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/RECORD_n{n}_k{K}.txt"
            with open(path,"w") as f:
                for v in S: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
            print(f"*** SOLVED n={n} K={K}! witness {path} ***", flush=True)
            return best_S,0
        seed+=1
    print(f"[done] n={n} K={K} best_conflicts={best_overall} after {time.time()-t0:.0f}s", flush=True)
    return best_S,best_overall

if __name__=="__main__":
    n=int(sys.argv[1]);K=int(sys.argv[2]);budget=float(sys.argv[3])
    mode=sys.argv[4] if len(sys.argv)>4 else "scratch"
    base_seed=int(sys.argv[5]) if len(sys.argv)>5 else 0
    per_seed=float(sys.argv[6]) if len(sys.argv)>6 else None
    run(n,K,budget,base_seed,mode,per_seed)
