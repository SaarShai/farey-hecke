#!/usr/bin/env python3
"""Targeted (-r,+s) swap search from structured 32-point 13-subcube slices of the records.
For each slice, try removing r points and greedily/exhaustively re-adding to exceed 33.
This explores a DIFFERENT neighborhood than the random-kick C searcher, anchored on structure."""
import sys, itertools, random, time
sys.path.insert(0,'.'); sys.path.insert(0,'structure')
from verify import parse_oeis_witnesses
from acute_core import is_acute_fast, can_add
W=parse_oeis_witnesses('a089676_witnesses.txt')
n=13
# rebuild all 32-slices
slices=set()
for nn in (15,14):
    c,M=W[nn]
    combos=itertools.combinations(range(nn),2) if nn==15 else [(i,) for i in range(nn)]
    for cc in combos:
        for vv in itertools.product([0,1],repeat=len(cc)):
            sub=[m for m in M if all(((m>>cc[k])&1)==vv[k] for k in range(len(cc)))]
            keep=[i for i in range(nn) if i not in cc]
            proj=tuple(sorted(sum(((m>>old)&1)<<newi for newi,old in enumerate(keep)) for m in sub))
            if len(set(proj))==len(proj) and len(proj)>=32: slices.add(proj)
slices=[list(s) for s in slices]
print(f'{len(slices)} structured 32-slices', flush=True)

def addable(S):
    Sset=set(S)
    return [p for p in range(1<<n) if p not in Sset and can_add(S,p)]

best=33; bestset=None; t0=time.time(); TL=float(sys.argv[1]) if len(sys.argv)>1 else 240
random.seed(0)
# Strategy: from each slice, do randomized (-r,+greedy) restarts. r in 1..6.
trials=0
while time.time()-t0<TL:
    S=list(random.choice(slices)); 
    r=random.randint(1,6)
    for _ in range(r):
        if S: S.pop(random.randrange(len(S)))
    # greedy add (random order)
    cand_order=list(range(1<<n)); random.shuffle(cand_order)
    Sset=set(S)
    for p in cand_order:
        if p in Sset: continue
        if can_add(S,p): S.append(p); Sset.add(p)
    trials+=1
    if len(S)>best:
        ok,_=is_acute_fast(S)
        if ok:
            best=len(S); bestset=S[:]
            print(f'*** NEW BEST {best} (trial {trials}, t={time.time()-t0:.0f}s)', flush=True)
print(f'done trials={trials} best={best}', flush=True)
if bestset and best>=34:
    with open('structure/cand_n13_deepen.txt','w') as f:
        for v in bestset: f.write(' '.join(str((v>>i)&1) for i in range(n))+'\n')
    print('WROTE cand_n13_deepen.txt', flush=True)
