#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
G4_hecke_farey_points.py  (goal #7)

Generate GENUINE G_4 Hecke-Farey points (lam=sqrt2): the orbit of the cusp oo under the Hecke
group G_4 = <S, T_lam>, S(z)=-1/z, T_lam(z)=z+lam, with cusps a/c, a,c in Z[sqrt2].

DENSE-DENOMINATOR SUBTLETY: Z[sqrt2] is DENSE in R, so {|c|<=Q} is INFINITE. The correct finite
"level" for an arithmetic Hecke group uses the GALOIS HEIGHT  H(c)=max(|c|,|c'|), c'=conjugate
(p-r*sqrt2 for c=p+r*sqrt2). H(c)<=Q is finite (Northcott). We generate all cusps in [0,lam] with
H(c)<=Q, sort, and inspect consecutive denominator products.

GOAL: see whether the BCZ recurrence and the X(4)=sqrt2/8 floor appear on REAL points, and
honestly report which normalization (real |c| vs height) the dynamics uses.
"""
import math, heapq
S2 = math.sqrt(2.0)

# Z[sqrt2] element as (p,r) = p + r*sqrt2
def val(z):  return z[0] + z[1]*S2          # real embedding
def conj(z): return (z[0], -z[1])
def hgt(z):  return max(abs(val(z)), abs(val(conj(z))))   # Galois height
def add(a,b): return (a[0]+b[0], a[1]+b[1])
def sub(a,b): return (a[0]-b[0], a[1]-b[1])
def neg(a):   return (-a[0], -a[1])
def mul(a,b):
    # (p+r√2)(u+v√2) = pu+2rv + (pv+ru)√2
    return (a[0]*b[0]+2*a[1]*b[1], a[0]*b[1]+a[1]*b[0])
LAM=(0,1)           # sqrt2
ONE=(1,0); ZERO=(0,0)

# Moebius action on a cusp represented as (a,c) meaning a/c (a,c in Z[sqrt2]).
def applyS(ac):   # z -> -1/z : a/c -> -c/a
    a,c=ac; return (neg(c), a)
def applyT(ac,sgn):  # z -> z + sgn*lam : a/c -> (a + sgn*lam*c)/c
    a,c=ac; return (add(a, mul((0,sgn), c)), c)

def normalize_cusp(ac):
    """Return a canonical (a,c) with c 'positive-ish' for dedup; key by real value."""
    return ac

def generate(Q, max_nodes=400000):
    """BFS over cusps reachable from oo=(1,0), keeping those with height<=Q, value in [0,lam]."""
    start=(ONE, ZERO)   # oo
    seen={}             # key: rounded real value -> (a,c)
    frontier=[start]
    cusps={}
    steps=0
    # We expand by S and T^{+-1}; keep nodes whose cusp value is finite and height<=Q (or is oo).
    visited=set()
    def key(ac):
        a,c=ac
        if c==ZERO: return ('oo',)
        return (round(val(a)/val(c) if val(c)!=0 else 0, 9),)
    while frontier and steps<max_nodes:
        ac=frontier.pop()
        steps+=1
        a,c=ac
        kc = ('oo',) if c==ZERO else (round(val(a)/val(c),10),)
        if kc in visited: continue
        visited.add(kc)
        if c!=ZERO:
            v=val(a)/val(c)
            if 0<=v<=val(LAM)+1e-9 and hgt(c)<=Q+1e-9:
                cusps[round(v,10)]=(a,c)
        # expand
        for nb in (applyS(ac), applyT(ac,1), applyT(ac,-1)):
            a2,c2=nb
            # prune: if denominator height already > Q AND value outside a margin, still allow S to reduce;
            # keep exploration if height(c2)<= Q*4 (slack so neighbors of in-range cusps are found)
            if c2!=ZERO and hgt(c2) > Q*3+5:
                # only keep if value in window (might still be a needed neighbor); else prune
                v2=val(a2)/val(c2)
                if not (-0.1<=v2<=val(LAM)+0.1):
                    continue
            k2=('oo',) if c2==ZERO else (round(val(a2)/val(c2),10),)
            if k2 not in visited:
                frontier.append(nb)
    return cusps

def analyze(Q):
    cusps=generate(Q)
    items=sorted(cusps.items())            # (value, (a,c)) sorted by value
    vals=[v for v,_ in items]
    dens=[abs(val(ac[1])) for _,ac in items]     # |c| real embedding
    # consecutive denominator products normalized by Q^2 (real-embedding normalization)
    P=[dens[n]*dens[n+1]/(Q*Q) for n in range(len(dens)-1)]
    X4=S2/8
    # gaps
    gaps=[vals[n+1]-vals[n] for n in range(len(vals)-1)]
    # check Farey-neighbor determinant a_{n+1} c_n - a_n c_{n+1} for consecutive
    dets=[]
    for n in range(len(items)-1):
        (_,(a0,c0)),(_,(a1,c1))=items[n],items[n+1]
        d=sub(mul(a1,c0),mul(a0,c1))    # in Z[sqrt2]
        dets.append(d)
    # check recurrence d_{n+1} ?= floor((Q+d_{n-1})/(lam d_n)) lam d_n - d_{n-1}  (real)
    rec_ok=0; rec_bad=0
    for n in range(1,len(dens)-1):
        k=math.floor((Q+dens[n-1])/(S2*dens[n]))
        pred=k*S2*dens[n]-dens[n-1]
        if abs(pred-dens[n+1])<1e-6: rec_ok+=1
        else: rec_bad+=1
    return dict(Q=Q,n_cusps=len(items),X4=X4,
                min_gap=min(gaps) if gaps else None,
                max_gap=max(gaps) if gaps else None,
                min_P=min(P) if P else None, max_P=max(P) if P else None,
                rec_ok=rec_ok, rec_bad=rec_bad,
                sample_dets=[ (round(val(d),4), d) for d in dets[:8] ],
                n_below_X=sum(1 for p in P if p<X4-1e-9))

if __name__=="__main__":
    for Q in [8, 12, 20, 30]:
        r=analyze(Q)
        print(f"Q(height)={Q:>3}  #cusps in [0,lam]={r['n_cusps']:>5}  X4=sqrt2/8={r['X4']:.6f}")
        print(f"   gaps in [{r['min_gap']:.5f},{r['max_gap']:.5f}]  P in [{r['min_P']:.5f},{r['max_P']:.5f}]  "
              f"#P<X4={r['n_below_X']}")
        print(f"   BCZ-recurrence on real |c|: ok={r['rec_ok']} bad={r['rec_bad']}  "
              f"(if bad>>0, real-|c| is NOT the right BCZ normalization for q=4)")
        print(f"   first consecutive determinants a'c-ac' (val): {[d[0] for d in r['sample_dets']]}")
        print()
