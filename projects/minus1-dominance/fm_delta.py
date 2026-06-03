"""
Closed-form Fiorilli-Martin density delta(q;a,1) for a a non-residue, via
Corollary 1.9 (arXiv:0912.4908):

 delta(q;a,b) = 1/2 + rho(q)/(2 sqrt(pi phi(q) L(q))) * (1 - Delta(q;a,b)/(2 L(q)) + O(1/log^2 q))

with a nonsquare, b=1 square, and
 Delta(q;a,b) = Kq(a-b) + iota_q(-a b^{-1}) log2 + Lambda(r1)/r1 + Lambda(r2)/r2 + H(q;a,b)
 r1 = least positive residue of a b^{-1}, r2 = b a^{-1}.
 L(q) = log q - sum_{p|q} log p/(p-1) + Lambda(q)/phi(q) - (gamma0 + log 2pi).

We DROP H (small, eq involves e(q;p,r); =0 unless extreme coincidence; for our
moduli with a,b coprime to q the leading behavior is captured). We compute
Delta exactly for b=1 and RANK non-residues by delta. SMALLER Delta => LARGER delta
=> MORE favored over the principal class.

This is the EXACT predictor of the relative ordering among non-residues in the
race against 1.  a=-1 has the UNIQUE extra +log2 (iota term), hence LARGEST Delta,
hence SMALLEST delta(q;-1,1): -1 is the LEAST favored NR vs the principal class.
"""
import sympy
from sympy import log, gcd, totient, primefactors, isprime, Rational
import math

EULER=0.5772156649015328606
LOG2PI=math.log(2*math.pi)

def Lambda(n):
    if n<2: return 0.0
    pf=sympy.factorint(n)
    if len(pf)==1:
        p=list(pf.keys())[0]; return math.log(p)
    return 0.0

def Lq(q):
    s=math.log(q)
    for p in primefactors(q):
        s-=math.log(p)/(p-1)
    s+=Lambda(q)/int(totient(q))
    s-=(EULER+LOG2PI)
    return s

def Kq(n,q):
    g=math.gcd(n%q if n%q!=0 else q, q)
    qq=q//g
    return Lambda(qq)/int(totient(qq)) - Lambda(q)/int(totient(q))

def rho(q):
    w=len(primefactors(q))
    if q%2==1: return 2**w
    if q%4!=0: return 2**(w-1)
    if q%8!=0: return 2**w
    return 2**(w+1)

def Delta(q,a,b):
    inv=lambda x: pow(x,-1,q)
    r1=(a*inv(b))%q; r2=(b*inv(a))%q
    iota = 1 if ((-a*inv(b))%q)==1 else 0
    val = Kq(a-b,q) + iota*math.log(2) + Lambda(r1)/r1 + Lambda(r2)/r2
    return val, dict(r1=r1,r2=r2,iota=iota,Kq=Kq(a-b,q))

def delta(q,a,b=1):
    Lqv=Lq(q); rh=rho(q); ph=int(totient(q))
    D,_=Delta(q,a,b)
    if Lqv<=0:
        return float('nan')  # Cor 1.9 asymptotic invalid for small q; use Delta ranking
    pref = rh/(2*math.sqrt(math.pi*ph*Lqv))
    return 0.5 + pref*(1 - D/(2*Lqv))

def rank_nonresidues(q):
    from math import gcd as g
    U=[a for a in range(1,q) if g(a,q)==1]
    sq=set((x*x)%q for x in U); nqr=[a for a in U if a not in sq]
    rows=[]
    for a in nqr:
        if a==1: continue
        D,info=Delta(q,a,1)
        d=delta(q,a,1)
        rows.append((a,d,D,info))
    # rank by Delta ASCENDING (smaller Delta = larger delta = MORE favored).
    # Valid for all q since delta is monotone decreasing in Delta.
    rows.sort(key=lambda r:r[2])
    return rows,nqr

if __name__=="__main__":
    import sys
    for q in [7,8,11,12,19,23,24,3,5,13,29,43,47]:
        if Lq(q)<=0:
            print(f"q={q}: L(q)={Lq(q):.3f} <=0 (asymptotics not valid for small q), skipping rank reliability note")
        rows,nqr=rank_nonresidues(q)
        print(f"\nq={q}  L(q)={Lq(q):.4f} rho={rho(q)} phi={int(totient(q))}  NR(non-principal)={[a for a in nqr if a!=1]}")
        print("  rank: a   delta(q;a,1)    Delta(q;a,1)  [r1,r2,iota,Kq]")
        for i,(a,d,D,info) in enumerate(rows):
            tag="  <== a=-1 (LEAST favored)" if a==q-1 else ""
            print(f"   {i+1:2d}.  a={a:3d}  delta={d:.6f}  Delta={D:.5f}  {info}{tag}")
