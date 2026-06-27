#!/usr/bin/env python3
"""Fixed-cardinality penalty SA for OEIS A089676 acute sets in {0,1}^n.

Energy = number of ordered (apex Q; legs P,R) right-angle violations:
  (P^Q)&(R^Q)==0, over all ordered triples of the current size-k array S.
We hold k FIXED and drive energy->0 by replacing one vertex at a time
(simulated annealing). energy==0  =>  size-k acute set.

Right-angle count is symmetric in the two legs, so we count UNORDERED leg
pairs and the verifier (which counts ordered) agrees on the zero set: a set
has 0 unordered violations iff 0 ordered violations.

Usage: sa.py <n> <k> [seeds] [iters] [seedfile] [out_prefix]
Any energy-0 result is written and MUST be checked with verify.py.
"""
import sys, os, random, re

def parse_witnesses(path):
    txt=open(path).read(); W={}
    parts=re.split(r'a\((\d+)\)\s*>=\s*(\d+):', txt)
    for i in range(1,len(parts),3):
        nn=int(parts[i])
        rows=re.findall(r'\(([01\s]+)\)', parts[i+2])
        masks=[]
        for r in rows:
            bits=[c for c in r if c in '01']
            v=0
            for j,c in enumerate(bits):
                if c=='1': v|=(1<<j)
            masks.append(v)
        W[nn]=masks
    return W

def right_pair(a,b,q,pc):
    # is there a right angle at apex q between legs a,b ?  ((a^q)&(b^q))==0
    return ((a^q)&(b^q))==0

def total_energy(S):
    m=len(S); e=0
    for j in range(m):
        q=S[j]
        for a in range(m):
            if a==j: continue
            xa=S[a]^q
            for b in range(a+1,m):
                if b==j: continue
                if (xa&(S[b]^q))==0:
                    e+=1
    return e

def vertex_contrib(S, idx, val):
    """Total violations that INVOLVE position idx (with S[idx]=val), counted once each.
    Covers: idx as apex; idx as one leg (any apex, other leg). Used for delta moves."""
    m=len(S); e=0
    # idx as apex
    for a in range(m):
        if a==idx: continue
        xa=S[a]^val
        for b in range(a+1,m):
            if b==idx: continue
            if (xa&(S[b]^val))==0:
                e+=1
    # idx as a leg, apex j != idx, other leg b != idx, b>idx-as-leg handled by counting all b!=idx,j
    for j in range(m):
        if j==idx: continue
        q=S[j]
        xi=val^q
        for b in range(m):
            if b==idx or b==j: continue
            if (xi&(S[b]^q))==0:
                e+=1   # ordered leg pair (idx,b); each unordered pair counted twice over j-loop? no: apex fixed j, legs {idx,b} unordered counted once when we restrict...
    return e

# The leg-as-pair double counts: for apex j, pair {idx,b} should count once. Above loop counts
# it once per b (idx fixed as one leg, b the other) => once. Good. But the apex-block also can't
# overlap. So vertex_contrib is the exact number of violating unordered (apex,legpair) incidences
# touching idx. We use it only for relative delta of single-vertex replacement (consistent).

def replace_delta(S, idx, newval):
    old=vertex_contrib(S, idx, S[idx])
    new=vertex_contrib(S, idx, newval)
    return new-old

def run(n, k, seeds, iters, seedfile, out_prefix):
    rng=random.Random(12345)
    W=parse_witnesses(seedfile) if seedfile else {}
    seed_masks=W.get(n, [])
    full=(1<<n)
    best_global=None; best_e=10**9
    for s in range(seeds):
        rng.seed(1000*s+7)
        # init: seed from record set + random extras, or fully random
        S=list(seed_masks)
        random.Random(s).shuffle(S)
        if len(S)>k: S=S[:k]
        seen=set(S)
        while len(S)<k:
            v=rng.randrange(full)
            if v not in seen:
                seen.add(v); S.append(v)
        E=total_energy(S)
        T=2.0; cool=0.9997
        stagn=0; localbest=E
        for it in range(iters):
            if E==0: break
            # pick a vertex involved in many violations preferentially sometimes
            idx=rng.randrange(k)
            newval=rng.randrange(full)
            if newval in seen and newval!=S[idx]:
                continue
            d=replace_delta(S, idx, newval)
            if d<=0 or rng.random()<pow(2.718281828, -d/max(T,1e-9)):
                seen.discard(S[idx]); S[idx]=newval; seen.add(newval)
                E+=d
                if E<localbest:
                    localbest=E; stagn=0
                else:
                    stagn+=1
            T*=cool
            if stagn>4000:
                # kick: randomize a few vertices
                for _ in range(3):
                    i2=rng.randrange(k)
                    nv=rng.randrange(full)
                    if nv in seen: continue
                    seen.discard(S[i2]); S[i2]=nv; seen.add(nv)
                E=total_energy(S); stagn=0; T=max(T,0.8)
        E=total_energy(S)  # exact recount
        if E<best_e:
            best_e=E; best_global=list(S)
        if E==0:
            # write witness
            fn=f"{out_prefix}_n{n}_k{k}_seed{s}.txt"
            with open(fn,'w') as f:
                for v in S:
                    f.write(''.join('1' if (v>>i)&1 else '0' for i in range(n))+'\n')
            print(f"ZERO ENERGY n={n} k={k} seed={s} -> {fn}")
            return 0, fn, best_global
        print(f"  seed {s}: best E={E}", flush=True)
    # write best-so-far for record
    fn=f"{out_prefix}_n{n}_k{k}_BEST_e{best_e}.txt"
    with open(fn,'w') as f:
        for v in best_global:
            f.write(''.join('1' if (v>>i)&1 else '0' for i in range(n))+'\n')
    print(f"BEST n={n} k={k} energy={best_e} -> {fn}")
    return best_e, fn, best_global

if __name__=="__main__":
    n=int(sys.argv[1]); k=int(sys.argv[2])
    seeds=int(sys.argv[3]) if len(sys.argv)>3 else 20
    iters=int(sys.argv[4]) if len(sys.argv)>4 else 200000
    seedfile=sys.argv[5] if len(sys.argv)>5 else None
    out_prefix=sys.argv[6] if len(sys.argv)>6 else "wit"
    run(n,k,seeds,iters,seedfile,out_prefix)
