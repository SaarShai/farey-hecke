#!/usr/bin/env python3
"""Exhaustive d-stability certificate: remove ALL d-subsets from a known acute 24-set,
exact-repair each seeking size 25. If none reaches 25, the set is 'd-stable'.
Uses multiprocessing over subsets. Stops & writes witness if any 25 found.
"""
import sys, time, itertools, re
import multiprocessing as mp
sys.path.insert(0,'/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp')
import lns

def load_base(n):
    txt=open('/Users/za/Documents/farey-hecke/code/acute_pilot/a089676_witnesses.txt').read()
    parts=re.split(r'a\((\d+)\)\s*>=\s*(\d+):', txt); W={}
    for i in range(1,len(parts),3):
        nn=int(parts[i]); rows=re.findall(r'\(([01\s]+)\)', parts[i+2]); m=[]
        for r in rows:
            b=[c for c in r if c in '01']; v=0
            for k,c in enumerate(b):
                if c=='1': v|=1<<k
            m.append(v)
        W[nn]=m
    rec=W[n]; t=rec[0]; return [x^t for x in rec]

BASE=None; N=None; D=None
def init_worker(base,n,d):
    global BASE,N,D; BASE=base; N=n; D=d

def check(cc):
    core=[BASE[i] for i in range(len(BASE)) if i not in set(cc)]
    ext=lns.max_extension(core, N, D+1, time_limit=TL, t0=time.time())
    timed_out = lns.max_extension.last_timed_out
    if ext is not None and len(core)+len(ext)>=len(BASE)+1:
        return ("FOUND", cc, core+ext)
    if timed_out:
        return ("TIMEOUT", cc, None)   # UNSOUND for this subset
    return None

TL=30.0   # per-subset exact-search time limit (generous so searches COMPLETE = sound)
def main():
    global TL
    n=int(sys.argv[1]); d=int(sys.argv[2]); nproc=int(sys.argv[3]) if len(sys.argv)>3 else 6
    if len(sys.argv)>4: TL=float(sys.argv[4])
    # optional 5th arg: path to a custom acute witness file (else use OEIS record)
    custom = sys.argv[5] if len(sys.argv)>5 else None
    if custom:
        base=[]
        for line in open(custom):
            b=[c for c in line if c in '01']
            if len(b)==n:
                v=0
                for k,c in enumerate(b):
                    if c=='1': v|=1<<k
                base.append(v)
        t=base[0]; base=[x^t for x in base]   # translate to contain 0
        print(f"[custom witness {custom}, size {len(base)}]", flush=True)
    else:
        base=load_base(n)
    R=len(base)            # record size (24 for n=11, 32 for n=12)
    idxs=[i for i in range(len(base)) if base[i]!=0]
    combos=list(itertools.combinations(idxs,d))
    print(f"d-stability n={n} d={d}: {len(combos)} subsets, {nproc} procs, per-subset TL={TL}s", flush=True)
    t0=time.time(); timeouts=0
    with mp.Pool(nproc, initializer=init_worker, initargs=(base,n,d)) as p:
        for i,res in enumerate(p.imap_unordered(check, combos, chunksize=20)):
            if res is not None and res[0]=="FOUND":
                _,cc,witness=res
                print(f"*** FOUND {R+1}! removed {cc}, size {len(witness)} ***", flush=True)
                from core import is_acute_masks
                assert is_acute_masks(witness)
                path=f"/Users/za/Documents/farey-hecke/code/acute_pilot/exact_cp/STABILITY_FOUND_n{n}_d{d}.txt"
                with open(path,"w") as f:
                    for v in witness: f.write("".join('1' if (v>>i)&1 else '0' for i in range(n))+"\n")
                p.terminate(); return
            if res is not None and res[0]=="TIMEOUT":
                timeouts+=1
            if (i+1)%5000==0:
                print(f"  {i+1}/{len(combos)} checked, {timeouts} timeouts, {time.time()-t0:.0f}s", flush=True)
    if timeouts==0:
        print(f"d={d}-STABLE [SOUND]: no {R+1} found, ALL {len(combos)} exact searches COMPLETED ({time.time()-t0:.0f}s). Known {R}-set (n={n}) is provably {d}-stable.", flush=True)
    else:
        print(f"d={d}: no {R+1} found but {timeouts}/{len(combos)} subsets TIMED OUT (UNSOUND — raise TL and rerun those). ({time.time()-t0:.0f}s)", flush=True)

if __name__=="__main__":
    main()
