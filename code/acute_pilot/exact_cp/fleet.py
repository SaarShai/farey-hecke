#!/usr/bin/env python3
"""Parallel fleet: run many SA workers (multiprocessing) for a target (n,K).
Each worker runs sa_best with its own seed/params; on conflicts==0 it writes RECORD file
and the fleet stops. Logs best-so-far across workers periodically.
"""
import sys, time, os, random
import multiprocessing as mp
sys.path.insert(0,'/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp')
import sa_best

OUT='/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp'

def worker(args):
    n,K,seed,per_run,total,poolmode = args
    N=1<<n; pool=None
    if poolmode=="even": pool=[v for v in range(1,N) if bin(v).count('1')%2==0]
    elif poolmode=="band2": c=n//2; pool=[v for v in range(1,N) if abs(bin(v).count('1')-c)<=2]
    elif poolmode=="band3": c=n//2; pool=[v for v in range(1,N) if abs(bin(v).count('1')-c)<=3]
    t0=time.time(); best=10**9; bestS=None; s=seed
    while time.time()-t0 < total:
        # vary params per restart
        rng=random.Random(s)
        pr=rng.choice([0.02,0.03,0.05,0.08])
        ka=rng.choice([800,1200,2000,3000])
        ks=rng.choice([3,4,5,6])
        S,conf,el,it=sa_best.solve(n,K,min(per_run,total-(time.time()-t0)),s,pool=pool,
                                    p_random=pr,kick_after=ka,kick_size=ks,verbose=False)
        if conf<best:
            best=conf; bestS=S[:]
        if conf==0:
            path=f"{OUT}/RECORD_n{n}_k{K}_w{seed}.txt"
            with open(path,"w") as f:
                for v in S: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
            return (seed,0,path)
        s+=1000
    return (seed,best,None)

def main():
    n=int(sys.argv[1]);K=int(sys.argv[2]);total=float(sys.argv[3])
    nproc=int(sys.argv[4]) if len(sys.argv)>4 else 14
    poolmode=sys.argv[5] if len(sys.argv)>5 else "all"
    per_run=float(sys.argv[6]) if len(sys.argv)>6 else 90
    print(f"FLEET n={n} K={K} procs={nproc} pool={poolmode} budget={total}s per_run={per_run}s", flush=True)
    args=[(n,K,1+i,per_run,total,poolmode) for i in range(nproc)]
    with mp.Pool(nproc) as p:
        results=p.map(worker, args)
    solved=[r for r in results if r[1]==0]
    bests=sorted(r[1] for r in results)
    print(f"FLEET DONE n={n} K={K}: best_conflicts across workers = {bests[0]}  (distribution: {bests})", flush=True)
    if solved:
        print(f"*** SOLVED *** witness: {solved[0][2]}", flush=True)
    else:
        print(f"No 0-conflict found. min conflicts = {bests[0]}", flush=True)

if __name__=="__main__":
    main()
