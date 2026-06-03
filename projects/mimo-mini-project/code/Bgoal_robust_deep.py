import math, itertools
from Bgoal_genuine_hunt import lam, ellipse_vecs, word_family, feasible_window, Phat
def deep(q, Pmax, Kmax):
    l=lam(q); w=ellipse_vecs(q,l); cusp=1.0/l**3
    alphabet=[(i,k) for i in range(2,q) for k in range(0,Kmax+1)]
    seen=set(); best=(cusp,"cusp[(q-2,0)]"); below=0; ex=None
    def canon(wd): return min(tuple(wd[j:]+wd[:j]) for j in range(len(wd)))
    for p in range(1,Pmax+1):
        for word in itertools.product(alphabet,repeat=p):
            c=canon(list(word))
            if c in seen: continue
            seen.add(c)
            vs=word_family(list(c),w,l)
            if vs is None: continue
            win=feasible_window(list(c),vs,w,q,l)
            if win is None: continue
            s_lo,s_hi,_=win
            mph=max(Phat(vs[n],c[n][0],w) for n in range(len(c)))
            Xc=s_lo*s_lo*mph
            if Xc<best[0]-1e-9: best=(Xc,str(list(c)))
            if Xc<cusp-1e-9:
                below+=1
                if ex is None: ex=(Xc,list(c))
    print(f"q={q} Pmax={Pmax} Kmax={Kmax}: 1/lam^3={cusp:.6f} global_best={best} #below={below} ex={ex}")
deep(5,7,2); deep(6,6,2); deep(7,6,2)
