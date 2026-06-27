#!/usr/bin/env python3
"""Parallel hybrid fleet: each worker does SA->exact-repair cycles from random starts.
Stops & writes witness if any worker reaches an acute K-set."""
import sys, time
import multiprocessing as mp
sys.path.insert(0,'/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp')
import hybrid

def worker(args):
    n,K,seed,total=args
    S,el=hybrid.run(n,K,total,seed,verbose=False)
    if S is not None and len(S)>=K:
        path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/HYBRID_RECORD_n{n}_k{K}_w{seed}.txt"
        with open(path,"w") as f:
            for v in S: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
        return (seed, len(S), path)
    return (seed, 0, None)

def main():
    n=int(sys.argv[1]);K=int(sys.argv[2]);total=float(sys.argv[3]);nproc=int(sys.argv[4]) if len(sys.argv)>4 else 6
    print(f"HYBRID FLEET n={n} K={K} procs={nproc} budget={total}s", flush=True)
    args=[(n,K,1000*(i+1),total) for i in range(nproc)]
    with mp.Pool(nproc) as p:
        results=p.map(worker, args)
    sol=[r for r in results if r[1]>=K]
    if sol:
        print(f"*** SOLVED n={n} K={K} witness {sol[0][2]} ***", flush=True)
    else:
        print(f"HYBRID FLEET DONE n={n} K={K}: no {K}-set found by any worker", flush=True)

if __name__=="__main__":
    main()
