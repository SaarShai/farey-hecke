#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gq_hecke_farey_general.py  (goal #7) — DECISIVE genuine-points test for q=3,4,5,6.

Generate GENUINE G_q Hecke-Farey points (orbit of oo under G_q=<S,T_lam>, cusps a/c in Z[lam],
lam=2cos(pi/q)) using Galois-height normalization H(c)=max_emb |c| <= Q (finite by Northcott),
canonical mod-lam reduction + S-expansion. Then test the cluster/window floor at X(q) on the REAL
sorted consecutive denominator products P_n = |c_n||c_{n+1}|/Q^2.

Ring Z[lam], lam^2 = c0 + c1*lam (lam is a root of x^2 - c1 x - c0):
  q=4: lam=sqrt2,  lam^2=2      -> (c0,c1)=(2,0)
  q=5: lam=phi,    lam^2=lam+1  -> (c0,c1)=(1,1)
  q=6: lam=sqrt3,  lam^2=3      -> (c0,c1)=(3,0)
Galois conj: lam -> c1 - lam, so conj(p,r) = (p + r*c1, -r); embeddings val_+(lam), val_-(lam)=c1-val_+.
q=3 (lam=1) is ordinary Farey; handled by the integer generator elsewhere (X3_arithmetic_verify.py).

DECISION RULE:
  q=4 is PROVEN cluster<=2 -> genuine points MUST give runBelowX<=2, viol(w3)=0 (sanity).
  If q=5,6 genuine points ALSO give runBelowX<=2 & viol(w3)=0, the 3-window floor GENERALIZES
  (and the earlier random-seed T_q simulation was sampling transient, non-genuine dynamics).
  If they give runBelowX>2 / viol(w3)>0 on genuine complete points, the 3-window floor FAILS for q>=5.
"""
import math

def setup(q):
    lp = 2.0*math.cos(math.pi/q)        # val_+(lam)
    if q==4: c0,c1=2,0
    elif q==5: c0,c1=1,1
    elif q==6: c0,c1=3,0
    else: raise ValueError
    lm = c1 - lp                         # val_-(lam) (Galois conjugate embedding)
    return lp,lm,c0,c1

def make_ops(lp,lm,c0,c1):
    def valp(z): return z[0]+z[1]*lp
    def valm(z): return z[0]+z[1]*lm
    def hgt(z): return max(abs(valp(z)),abs(valm(z)))
    def add(a,b): return (a[0]+b[0],a[1]+b[1])
    def sub(a,b): return (a[0]-b[0],a[1]-b[1])
    def neg(a): return (-a[0],-a[1])
    def mul(a,b):
        p,r=a; u,v=b
        # (p+r L)(u+v L)= pu + rv L^2 + (pv+ru)L = pu+rv c0 + (pv+ru+rv c1)L
        return (p*u+r*v*c0, p*v+r*u+r*v*c1)
    return valp,valm,hgt,add,sub,neg,mul

def Xq(q):
    return {3:2/9,4:math.sqrt(2)/8,5:0.25,6:math.sqrt(3)/6}[q]

def generate(q,Q,max_nodes=4000000):
    lp,lm,c0,c1=setup(q)
    valp,valm,hgt,add,sub,neg,mul=make_ops(lp,lm,c0,c1)
    LAM=(0,1); ONE=(1,0); ZERO=(0,0)
    def canon(ac):
        a,c=ac
        if valp(c)<0: a,c=neg(a),neg(c)
        if valp(c)==0: return (a,c)
        k=math.floor((valp(a)/valp(c))/lp)
        a=sub(a, mul((0,k),c))   # a -= k*lam*c  -> value in [0,lam)
        return (a,c)
    def applyS(ac):
        a,c=ac; return (neg(c),a)
    seen=set(); out={}
    stack=[canon((ZERO,ONE)),(ONE,ZERO)]
    n=0
    nshift=max(2,int(lp)+2)
    while stack and n<max_nodes:
        ac=stack.pop(); n+=1
        a,c=ac
        key=('oo',) if valp(c)==0 else (round(valp(a)/valp(c),9),)
        if key in seen: continue
        seen.add(key)
        if valp(c)!=0 and hgt(c)<=Q+1e-9:
            v=valp(a)/valp(c)
            if -1e-9<=v<lp+1e-9:
                out[round(v,10)]=ac
        for shift in range(-nshift,nshift+1):
            t=(add(a,mul((0,shift),c)),c)
            nb=canon(applyS(t)); na,nc=nb
            if valp(nc)==0: continue
            if hgt(nc)<=Q*1.6+2:
                k2=(round(valp(na)/valp(nc),9),)
                if k2 not in seen:
                    stack.append(nb)
    return out,(valp,valm,hgt,add,sub,neg,mul)

def analyze(q,Q):
    cusps,ops=generate(q,Q)
    valp,valm,hgt,add,sub,neg,mul=ops
    items=sorted(cusps.items())
    if len(items)<6: return dict(q=q,Q=Q,n=len(items),fail=True)
    vals=[v for v,_ in items]
    dens=[abs(valp(ac[1])) for _,ac in items]
    X=Xq(q)
    P=[dens[n]*dens[n+1]/(Q*Q) for n in range(len(dens)-1)]
    # neighbor determinants (in Z[lam]) -> distinct real values
    detset=set()
    for n in range(len(items)-1):
        (_,(a0,c0)),(_,(a1,c1))=items[n],items[n+1]
        d=sub(mul(a1,c0),mul(a0,c1)); detset.add(round(valp(d),4))
    def longest_run(pred):
        b=cur=0
        for v in P:
            if pred(v): cur+=1; b=max(b,cur)
            else: cur=0
        return b
    run=longest_run(lambda v:v<X-1e-9)
    def winviol(w): return sum(1 for i in range(len(P)-w+1) if max(P[i:i+w])<X-1e-7)
    # min window-max over w=3 (sharpness probe) and the argmin denominators
    minwm3=math.inf; argd=None
    for i in range(len(P)-2):
        wm=max(P[i],P[i+1],P[i+2])
        if wm<minwm3: minwm3=wm; argd=(dens[i],dens[i+1],dens[i+2],dens[i+3] if i+3<len(dens) else None)
    return dict(q=q,Q=Q,n=len(items),X=X,minP=min(P),maxP=max(P),
                run_below_X=run,viol_w2=winviol(2),viol_w3=winviol(3),viol_w4=winviol(4),
                n_below=sum(1 for p in P if p<X-1e-9),
                dets=sorted(detset)[:8], min_winmax3=minwm3, ratio_argd=argd)

if __name__=="__main__":
    for q in [4,5,6]:
        print(f"=== q={q}  lam={2*math.cos(math.pi/q):.6f}  X(q)={Xq(q):.7f} ===")
        for Q in [20,40,80,160,320]:
            r=analyze(q,Q)
            if r.get('fail'):
                print(f"  Q={Q}: only {r['n']} cusps (incomplete)"); continue
            print(f"  Q={Q:>4} #cusps={r['n']:>6} P[{r['minP']:.4f},{r['maxP']:.4f}] "
                  f"#P<X={r['n_below']:>4} runBelowX={r['run_below_X']} "
                  f"viol(w2,w3,w4)=({r['viol_w2']},{r['viol_w3']},{r['viol_w4']}) "
                  f"minWinMax3={r['min_winmax3']:.5f} dets={r['dets']}")
        print()
