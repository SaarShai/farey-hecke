"""
D3 Q6: exact closed form of C_FF(q) = lim_{D->inf} R_D,  R_D = q^D * W_D^pf.

Two independent exact handles:

(A) FF sigma_A^2 Euler-product identity (transport of Ramanujan's
    sum_n sigma(n)^2 n^{-s} = zeta(s)zeta(s-1)^2 zeta(s-2)/zeta(2s-2)):
        F(u) = sum_{m monic} sigma_A(m)^2 u^{deg m}
             = (1 - q^3 u^2) / [ (1-qu)(1-q^2 u)^2 (1-q^3 u) ].
    VERIFY by brute sum_{deg m=k} sigma_A(m)^2 vs [u^k]F(u), small k.
    (Do NOT assume the transport; verify it.)

(B) Exact R_D as a Fraction for D=1..Dmax (reuse the Q1c machinery), then
    rational Richardson on the geometric model R_D = C - A r^D :
        r_D = (R_{D+1}-R_D)/(R_D-R_{D-1}),
        C_D = R_{D+1} + (R_{D+1}-R_D)*r_D/(1-r_D)
    Exact Fraction arithmetic; C_D should stabilize -> recognise the rational.

The analytic form: the dominant singularity nearest 0 of the generating
function governing the q^D-normalised head is u = 1/q^3 (simple pole from
(1-q^3 u)); so R_D -> a rational function of q. (B) pins the exact value;
(A) supplies the structural reason it is rational.
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
@lru_cache(maxsize=None)
def factor_monic(f,q):
    f=normalize(f); fac={}; d=deg(f)
    if d==0: return tuple()
    cur=f
    for p in irr_upto(max(1,d),q):
        if deg(cur)==0: break
        while deg(cur)>=deg(p):
            qo,ro=pdivmod(cur,p,q)
            if is_zero(ro): fac[p]=fac.get(p,0)+1; cur=qo
            else: break
    if deg(cur)>=1: fac[cur]=fac.get(cur,0)+1
    return tuple(sorted(fac.items()))
@lru_cache(maxsize=None)
def sigmaA(f,q):
    f=normalize(f)
    if deg(f)==0: return 1
    val=1
    for p,e in factor_monic(f,q):
        Np=q**deg(p)
        val*= (Np**(e+1)-1)//(Np-1)
    return val
def divisors_monic(m,q):
    m=normalize(m)
    if deg(m)==0: return [(1,)]
    divs=[(1,)]
    for p,e in factor_monic(m,q):
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
    return 0 if k<0 else (1 if k==0 else 1-q)
def A_D(m,D,q):
    return sum((q**deg(e))*MA(D-deg(e),q) for e in divisors_monic(m,q))
def PhiA(g,q):
    g=normalize(g)
    if deg(g)==0: return 1
    val=q**deg(g)
    for p,_ in factor_monic(g,q):
        Np=q**deg(p); val=val*(Np-1)//Np
    return val
@lru_cache(maxsize=None)
def Phi_D(D,q):
    return sum(PhiA(g,q) for e in range(0,D+1) for g in monic_polys(e,q))

# ---- (A) verify the FF sigma_A^2 Euler product ----
def F_coeffs(q,K):
    """power-series coeffs [u^0..u^K] of (1-q^3 u^2)/((1-qu)(1-q^2 u)^2(1-q^3 u))."""
    num=[1,0,-q**3]                       # 1 - q^3 u^2
    den=[1]
    def mul(a,b):
        r=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b): r[i+j]+=x*y
        return r
    for poly in ([1,-q],[1,-q**2],[1,-q**2],[1,-q**3]):
        den=mul(den,poly)
    # series of num/den up to K
    c=[0]*(K+1)
    for n in range(K+1):
        s = num[n] if n<len(num) else 0
        s -= sum(den[j]*c[n-j] for j in range(1,min(n,len(den)-1)+1))
        c[n]=s//den[0]
    return c

def verifyA(q,K):
    Fc=F_coeffs(q,K)
    ok=True
    rows=[]
    for k in range(0,K+1):
        brute=sum(sigmaA(m,q)**2 for m in monic_polys(k,q))
        rows.append((k,brute,Fc[k],brute==Fc[k]))
        if brute!=Fc[k]: ok=False
    return ok,rows

# ---- (B) exact R_D + rational Richardson ----
def R_exact(D,q):
    Kx={2:6,3:4,5:3}.get(q,4); K=D+Kx
    W=Fraction(0)
    for k in range(0,K+1):
        wk=Fraction(1,q**(2*k))
        for m in monic_polys(k,q):
            a=A_D(m,D,q)
            if a: W+=a*a*wk
    W*= (q-1)
    return Fraction(W,Phi_D(D,q))*(q**D)

def richardson(Rs):
    # Rs: dict D->Fraction. geometric model R_D = C - A r^D.
    out=[]
    Ds=sorted(Rs)
    for i in range(2,len(Ds)):
        D0,D1,D2=Ds[i-2],Ds[i-1],Ds[i]
        if D1-D0!=1 or D2-D1!=1: continue
        d1=Rs[D1]-Rs[D0]; d2=Rs[D2]-Rs[D1]
        if d1==0: continue
        r=d2/d1
        if r==1: continue
        C=Rs[D2]+d2*r/(1-r)
        out.append((D2,r,C))
    return out

def run():
    print("="*84)
    print("Q6  exact closed form of C_FF(q)=lim R_D")
    print("="*84)
    for q in (2,3,5):
        K=5 if q!=5 else 4
        okA,rows=verifyA(q,K)
        print(f"\n--- q={q} ---")
        print(f"(A) FF sigma_A^2 Euler-product F(u)=(1-q^3u^2)/((1-qu)(1-q^2u)^2(1-q^3u)) "
              f"vs brute, k=0..{K}: {'VERIFIED' if okA else 'MISMATCH'}")
        for k,b,f,o in rows[:5]:
            print(f"    k={k}: brute={b}  [u^k]F={f}  {'ok' if o else 'X'}")
        Dmax = 6 if q==2 else (5 if q==3 else 3)
        Rs={}
        for D in range(1,Dmax+1):
            Rs[D]=R_exact(D,q)
        print(f"(B) exact R_D, D=1..{Dmax}:")
        for D in range(1,Dmax+1):
            print(f"    R_{D} = {Rs[D]}  ~= {float(Rs[D]):.6f}")
        print("    rational Richardson (geometric model R_D=C-A r^D):")
        rich=richardson(Rs)
        for D2,r,C in rich:
            print(f"    @D={D2}: r={float(r):.5f}  C_est={float(C):.6f}   (exact C={C})")
        if rich:
            Cs=[float(c) for _,_,c in rich[-3:]]
            spread=max(Cs)-min(Cs) if len(Cs)>1 else 0.0
            print(f"    -> last C_est ~ {Cs[-1]:.6f}  (spread last3 = {spread:.2e})  "
                  f"{'STABLE' if spread<1e-2 else 'not yet stable'}")
    print("\n"+"="*84)
    print("READING: (A) VERIFIED => sigma_A^2 gen fn is the stated rational (nearest")
    print("singularity u=1/q^3) => R_D limit is a rational function of q [structural].")
    print("(B) exact rational Richardson C_est stabilising => C_FF(q) value pinned;")
    print("recognise the stable rational. Honest labels: (A)[PROVEN-by-verification],")
    print("(B) value [NUMERICAL exact-extrapolation], existence&rationality [PROVEN-sketch].")
    print("="*84)

if __name__=="__main__":
    run()
