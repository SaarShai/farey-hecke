"""
D3 Q1c (DECISIVE, exact): closed-form FF Mikolas second moment via Parseval +
the G0 exact identity. No floats in the Farey order; pure exact rationals.

E_D = (counting measure of Farey set F_D) - Phi_D * Haar on the K_inf circle.
Fourier coeffs: hatE_D(0)=0 ; hatE_D(m)=A_D(m) for m!=0.
G0 (exact): A_D(m) = sum_{e|m monic} q^{deg e} * M_A(D-deg e),
            M_A(0)=1, M_A(k>=1)=1-q, M_A(k<0)=0.
Unit grouping: |A_D(c m)|=|A_D(m)|, deg(cm)=deg m for c in F_q^*  =>  sum over
nonzero m = (q-1) * sum over monic m.

Mikolas / ball-discrepancy L^2 second moment (canonical |m|^{-2} Parseval weight,
the FF analogue of the sawtooth 1/(2 pi i m)^2):
    Wtot_D := (q-1) * sum_{m monic} A_D(m)^2 * q^{-2 deg m}        (converges per D:
              tail A_D(m) is capped at ~ d_A(m) q^D, killed by q^{-2deg m})
    W_D^pf := Wtot_D / Phi_D            (per-fraction; FF analogue of Mikolas W(N))
    R_D    := q^D * W_D^pf              (FF analogue of N*W(N) -> C)

Phi_D = sum_{g monic, deg g<=D} Phi_A(g),  Phi_A(g)=|g| prod_{P|g}(1-1/|P|).

DECISION:
  R_D -> finite constant  => FF normalized 2nd moment converges EXACTLY and
     UNCONDITIONALLY (no RH); this is the FF Mikolas/Good-Churchhouse analogue.
     By G2(b) character-orthogonality it is the Keating-Rudnick object =>
     CONFIRMS dictionary-tier verdict (exact unconditional collapse, NOT a new
     statistic; the char-0 RH-depth is absent because M_A is exactly constant).
  R_D grows  => FF reproduces a genuine char-0-like growth (would be surprising;
     re-examine).
Cross-check: R_D limit must be consistent with the Q1a radix simulation
(q=2: ~0.98,1.09,1.11,1.24 ; q=3: ~1.33,1.48,1.54,1.64 ; rising/slow).
"""
from itertools import product
from functools import lru_cache
from fractions import Fraction

def normalize(p):
    p=list(p)
    while len(p)>1 and p[-1]==0: p.pop()
    return tuple(p)
def deg(p):
    p=normalize(p)
    return -1 if (len(p)==1 and p[0]==0) else len(p)-1
def is_zero(p): return deg(p)==-1
def pmul(a,b,q):
    if is_zero(a) or is_zero(b): return (0,)
    r=[0]*(len(a)+len(b)-1)
    for i,ai in enumerate(a):
        if ai:
            for j,bj in enumerate(b): r[i+j]=(r[i+j]+ai*bj)%q
    return normalize(tuple(r))
def pdivmod(a,b,q):
    a=list(normalize(a)); b=normalize(b); db=deg(b)
    inv=pow(b[-1],q-2,q); quot=[0]
    while deg(tuple(a))>=db and not is_zero(tuple(a)):
        da=deg(tuple(a)); sh=da-db; f=(a[da]*inv)%q
        if sh>=len(quot): quot+=[0]*(sh+1-len(quot))
        quot[sh]=f
        for i,bi in enumerate(b): a[i+sh]=(a[i+sh]-f*bi)%q
        a=list(normalize(tuple(a)))
        if is_zero(tuple(a)) and sh==0: break
    return normalize(tuple(quot)),normalize(tuple(a))
def pmod(a,b,q): return pdivmod(a,b,q)[1]
def monic_polys(d,q):
    if d==0: yield (1,); return
    for lo in product(range(q),repeat=d): yield tuple(lo)+(1,)
@lru_cache(maxsize=None)
def irr_upto(md,q):
    irr=[]
    for d in range(1,md+1):
        for f in monic_polys(d,q):
            ok=True
            for g in irr:
                if deg(g)>d//2: break
                if is_zero(pmod(f,g,q)): ok=False;break
            if ok: irr.append(f)
    return tuple(irr)
def factor_monic(f,q):
    f=normalize(f); fac={}; d=deg(f)
    if d==0: return fac
    cur=f
    for p in irr_upto(max(1,d),q):
        if deg(cur)==0: break
        while deg(cur)>=deg(p):
            qo,ro=pdivmod(cur,p,q)
            if is_zero(ro): fac[p]=fac.get(p,0)+1; cur=qo
            else: break
    if deg(cur)>=1: fac[cur]=fac.get(cur,0)+1
    return fac
def divisors_monic(m,q):
    m=normalize(m)
    if deg(m)==0: return [(1,)]
    fac=factor_monic(m,q); divs=[(1,)]
    for p,e in fac.items():
        new=[]; pe=(1,)
        for _ in range(e+1):
            for dd in divs: new.append(pmul(dd,pe,q))
            pe=pmul(pe,p,q)
        divs=new
    seen=set();out=[]
    for dd in divs:
        dd=normalize(dd)
        if dd not in seen: seen.add(dd);out.append(dd)
    return out
def MA(k,q):
    if k<0: return 0
    if k==0: return 1
    return 1-q
def A_D(m,D,q):
    s=0
    for e in divisors_monic(m,q):
        s += (q**deg(e))*MA(D-deg(e),q)
    return s
def PhiA(g,q):
    g=normalize(g)
    if deg(g)==0: return 1
    val=q**deg(g)
    for p in factor_monic(g,q):
        val = val*(q**deg(p)-1)//(q**deg(p))
    return val
@lru_cache(maxsize=None)
def Phi_D(D,q):
    tot=0
    for e in range(0,D+1):
        for g in monic_polys(e,q):
            tot+=PhiA(g,q)
    return tot

def R_of_D(D,q,Kextra=6):
    # tail term per degree-k slice ~ q^{2D} q^{-k}; cumulative tail from k=D+Kextra
    # ~ q^{D-Kextra} vs Wtot~q^D  => relative tail ~ q^{-Kextra}. Kextra by q:
    Kx = {2:6, 3:4, 5:3}.get(q, 4)
    K=D+Kx
    Wtot=Fraction(0)
    for k in range(0,K+1):
        wk=Fraction(1,q**(2*k))
        for m in monic_polys(k,q):
            a=A_D(m,D,q)
            if a!=0:
                Wtot += a*a*wk
    Wtot *= (q-1)
    phi=Phi_D(D,q)
    Wpf=Fraction(Wtot,phi)
    R=Wpf*(q**D)
    return float(R), float(Wpf), phi, float(Wtot)

def run():
    print("="*84)
    print("Q1c EXACT: R_D = q^D * (Wtot_D/Phi_D),  Wtot_D=(q-1) sum_{m monic} A_D(m)^2 q^{-2deg m}")
    print("A_D(m) exact via G0. Pure Fraction arithmetic. Decisive: does R_D converge?")
    print("="*84)
    for q in (2,3,5):
        Dmax = 7 if q==2 else (5 if q==3 else 3)
        print(f"\n--- q={q} ---")
        print(f"{'D':>2} {'Phi_D':>10} {'Wtot_D':>14} {'W_D^pf':>12} {'R_D=q^D W^pf':>14} {'dR':>9}")
        prev=None
        for D in range(1,Dmax+1):
            R,Wpf,phi,Wtot=R_of_D(D,q)
            dR = "" if prev is None else f"{R-prev:+.5f}"
            print(f"{D:>2} {phi:>10} {Wtot:>14.4f} {Wpf:>12.6e} {R:>14.6f} {dR:>9}")
            prev=R
    print("\n"+"="*84)
    print("READING: R_D rising & dR shrinking (geometric) => converges to finite C_FF(q),")
    print("EXACT and UNCONDITIONAL (M_A constant; no RH). Consistent w/ Q1a radix sim.")
    print("By G2(b) orthogonality this is the Keating-Rudnick/Mikolas object =>")
    print("CONFIRMS dictionary-tier: exact unconditional collapse, NOT a new statistic.")
    print("If dR not shrinking / R_D ~ q^D => growth, re-examine (would be surprising).")
    print("="*84)

if __name__=="__main__":
    run()
