#!/usr/bin/env python3
"""Is beta_min (min ergodic AVERAGE of P) = 1/lam^3, or < it? Decides sub-action feasibility.
Enumerate feasible parabolic words; for each, min average over the s-family is at s->s_lo:
   avg = s_lo^2 * mean_n(Phat_n).  Compare to 1/lam^3.  Also scan hyperbolic fixed orbits.
If min word-average >= 1/lam^3 (approached only by cusp word) => beta_min=1/lam^3 (sub-action alive).
If some word-average < 1/lam^3 => sub-action at level 1/lam^3 is DEAD; window route only."""
import itertools, math
import numpy as np
import importlib.util
spec=importlib.util.spec_from_file_location("gh","Bgoal_genuine_hunt.py")
gh=importlib.util.module_from_spec(spec); spec.loader.exec_module(gh)

def analyze(q, Pmax, Kmax):
    l=gh.lam(q); w=gh.ellipse_vecs(q,l); thr=1.0/l**3
    branches=list(range(2,q))
    alphabet=[(i,k) for i in branches for k in range(0,Kmax+1)]
    seen=set()
    min_avg=1e9; min_avg_word=None; min_max=1e9
    n_feas=0
    def canon(word):
        return min(tuple(word[j:]+word[:j]) for j in range(len(word)))
    for p in range(1,Pmax+1):
        for word in itertools.product(alphabet,repeat=p):
            c=canon(list(word))
            if c in seen: continue
            seen.add(c)
            vs=gh.word_family(list(c),w,l)
            if vs is None: continue
            win=gh.feasible_window(list(c),vs,w,q,l)
            if win is None: continue
            s_lo,s_hi,_=win
            n_feas+=1
            phats=[gh.Phat(vs[n],c[n][0],w) for n in range(len(c))]
            avg=s_lo*s_lo*sum(phats)/len(phats)   # min average over family (s->s_lo)
            mx =s_lo*s_lo*max(phats)
            if avg<min_avg: min_avg=avg; min_avg_word=list(c)
            if mx<min_max: min_max=mx
    return thr,min_avg,min_avg_word,min_max,n_feas

for q,(Pm,Km) in [(5,(6,3)),(6,(6,2)),(7,(6,2)),(8,(6,2))]:
    thr,ma,maw,mm,nf=analyze(q,Pm,Km)
    print(f"q={q}: 1/lam^3={thr:.6f}  min_word_AVG={ma:.6f} (ratio {ma/thr:.4f}) word={maw}  "
          f"min_word_MAX={mm:.6f} (ratio {mm/thr:.4f})  [{nf} feasible words]")
print()
print("min_word_MAX ratio ~1.000 (>=1) confirms window/esssup lower bound 1/lam^3.")
print("min_word_AVG ratio: if >=1.000 => beta_min=1/lam^3 (sub-action alive); if <1 => sub-action dead.")
