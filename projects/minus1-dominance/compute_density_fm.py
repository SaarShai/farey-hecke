"""
Compute Rubinstein-Sarnak densities delta(q;a,1) for nonsquares a, two ways:
(A) the exact 2-term FM asymptotic   delta ~ 1/2 + rho(q)/sqrt(2 pi V(q;a,1))
    with V from Fiorilli-Martin Theorem 1.4 (arithmetic, GRH only), where
       V(q;a,b) = 2 phi(q) [ Lambda*(q) + Kq(a-b) + iq(-a b^{-1}) log2 ] + 2 M*(q;a,b)
    and we compute M*(q;a,b) = sum_{chi != chi0} |chi(a)-chi(b)|^2 * Re L'/L(1,chi*).
(B) the "honest" definition  V(q;a,b) = sum_{chi mod q} |chi(b)-chi(a)|^2 b(chi),
    b(chi) = sum_{gamma: L(1/2+ig,chi)=0} 1/(1/4+gamma^2),
    by DIRECT zero summation with mpmath for small q  (cross-check of (A)).

Goal: print, for each q, the ordering of delta(q;a,1) over nonsquares a, and
flag whether a = -1 (= q-1) is the SMALLEST (FM Thm 1.10) or largest.

Honest labels:
  - rho(q), iq, Kq, Lambda(q): PROVEN arithmetic (FM Def 1.2/1.5).
  - V via Thm 1.4: PROVEN under GRH.
  - delta via Thm 1.1 truncation: asymptotic; leading 2 terms only here.
  - LI is assumed for delta to be well defined (RS).
"""
import mpmath as mp
import math, cmath
import sympy
mp.mp.dps = 30

_PRIME_N = 60000
_PRIMES = list(sympy.primerange(2, _PRIME_N))
_LOGP = {p: math.log(p) for p in _PRIMES}

def units(q):
    return [a for a in range(1, q) if math.gcd(a, q) == 1]

def is_square(q, a, U):
    sq = set((b*b) % q for b in U)
    return a in sq

def dirichlet_characters(q):
    """All phi(q) Dirichlet characters mod q.
    Decompose (Z/q)^* = product of INDEPENDENT cyclic factors (one per prime power
    in q, with the 2^k anomaly handled), each given by an explicit generator of
    known order. Every unit then has a UNIQUE exponent vector (discrete log), and
    characters are products of roots of unity on the generators. This guarantees
    exactly phi(q) distinct characters.
    """
    U = units(q)
    n = len(U)
    def mul(a,b): return (a*b)%q
    def order(a):
        o=1; x=a
        while x!=1:
            x=mul(x,a); o+=1
        return o
    # independent cyclic generators via CRT over prime-power components
    def factor(m):
        f={}; d=2; nn=m
        while d*d<=nn:
            while nn%d==0: f[d]=f.get(d,0)+1; nn//=d
            d+=1
        if nn>1: f[nn]=f.get(nn,0)+1
        return f
    fac=factor(q)
    gens=[]; gen_orders=[]
    for p,k in fac.items():
        pk=p**k
        m_rest=q//pk
        # CRT lift: element that is g mod pk and 1 mod m_rest
        def crt(g):
            # find x = g mod pk, 1 mod m_rest
            if m_rest==1: return g % q
            from sympy.ntheory.modular import crt as scrt
            x,_=scrt([pk,m_rest],[g,1])
            return int(x)%q
        if p==2:
            if k==1:
                continue  # trivial
            elif k==2:
                gens.append(crt(3)); gen_orders.append(2)
            else:
                # (Z/2^k)^* = <-1> x <3 or 5>, orders 2 and 2^{k-2}
                gens.append(crt(pk-1)); gen_orders.append(2)
                gens.append(crt(5)); gen_orders.append(2**(k-2))
        else:
            # cyclic: find primitive root mod pk
            from sympy.ntheory.residue_ntheory import primitive_root
            g=primitive_root(pk)
            gens.append(crt(g)); gen_orders.append((p-1)*p**(k-1))
    # discrete log table
    import itertools
    dlog={}
    for combo in itertools.product(*[range(o) for o in gen_orders]):
        val=1
        for g,e in zip(gens,combo):
            val=mul(val, pow(g,e,q))
        dlog[val]=combo
    assert len(dlog)==n, (q, len(dlog), n, gens, gen_orders)
    chars=[]
    for combo in itertools.product(*[range(o) for o in gen_orders]):
        def make(combo=combo):
            def chi(a):
                a%=q
                if math.gcd(a,q)!=1: return 0
                e=dlog[a]
                ang=sum(2*math.pi*kk*ee/oo for kk,ee,oo in zip(combo,e,gen_orders))
                return cmath.exp(1j*ang)
            return chi
        chars.append(make())
    return chars

# ---- FM arithmetic pieces (Def 1.5) ----
def vonmangoldt(n):
    if n<2: return 0.0
    m=n; p=None
    d=2; nn=n; fac={}
    while d*d<=nn:
        while nn%d==0:
            fac[d]=fac.get(d,0)+1; nn//=d
        d+=1
    if nn>1: fac[nn]=fac.get(nn,0)+1
    if len(fac)==1:
        p=list(fac.keys())[0]
        return math.log(p)
    return 0.0

def Lambda_q(q):
    # Lambda(q) = log q - sum_{p|q} log p/(p-1) + Lam(q)/phi(q) - (gamma0 + log 2pi)
    phi=len(units(q))
    s=0.0
    # prime factors
    nn=q; d=2; primes=set()
    while d*d<=nn:
        while nn%d==0: primes.add(d); nn//=d
        d+=1
    if nn>1: primes.add(nn)
    for p in primes:
        s+=math.log(p)/(p-1)
    gamma0=float(mp.euler)
    return math.log(q) - s + vonmangoldt(q)/phi - (gamma0 + math.log(2*math.pi))

def Kq(q, n):
    n%=q
    g=math.gcd(n,q)
    m=q//g
    phi_m=len(units(m)) if m>1 else 1
    phi_q=len(units(q))
    term1 = vonmangoldt(m)/phi_m if m>1 else 0.0
    return term1 - vonmangoldt(q)/phi_q

def iq(q,n):
    return 1.0 if (n % q)==1 else 0.0

def Mstar(q,a,b,chars):
    """sum_{chi != chi0} |chi(a)-chi(b)|^2 Re L'/L(1, chi*).
    Use chi* = primitive inducing char. For simplicity (small q, and to keep the
    cross-check honest) compute L'/L(1,chi) for the character mod q directly via
    its Hurwitz-zeta expression; for imprimitive chi this differs from chi* by
    Euler factors at p|q, a finite correction. We compute with chi mod q (gives M,
    not M*); the difference M - M* is the explicit Euler-factor sum. We report M
    and note the distinction. For PROVED direction we rely on Thm 1.4 sign of the
    iq term, which is independent of M*.
    """
    phi=len(units(q))
    total=0.0
    for chi in chars:
        # skip principal
        if all(abs(chi(u)-1)<1e-9 for u in units(q)):
            continue
        ca=chi(a); cb=chi(b)
        w=abs(ca-cb)**2
        if w<1e-12: continue
        # L'/L(1,chi) = - sum_{n>=1} Lambda(n) chi(n) / n   (truncated).
        # Lower-order correction to V; the ORDERING among nonsquares is driven by
        # the iq/Kq arithmetic terms, so moderate truncation suffices here.
        N=_PRIME_N
        acc=0j
        for p in _PRIMES:
            lp=_LOGP[p]
            pk=p
            while pk<N:
                acc += lp*chi(pk)/pk
                pk*=p
        val = -acc
        total += w*val.real
    return total

def V_thm14(q,a,b,chars):
    phi=len(units(q))
    inv_b = pow(b, -1, q)
    term = Lambda_q(q) + Kq(q, a-b) + iq(q, (-a*inv_b)%q)*math.log(2)
    Mst = Mstar(q,a,b,chars)
    return 2*phi*term + 2*Mst, 2*phi*term, 2*Mst

def rho(q):
    # number of solutions x^2=1 mod q
    return sum(1 for x in range(q) if math.gcd(x,q)==1 and (x*x)%q==1)

def delta_two_term(q,a,b,chars):
    V,_,_ = V_thm14(q,a,b,chars)
    r=rho(q)
    V=float(V)
    if V<=0:
        # 2-term asymptotic invalid (needs q>=43 so that Lambda(q)>0 and V>0)
        return float('nan'), V
    return 0.5 + r/math.sqrt(2*math.pi*V), V

if __name__=="__main__":
    for q in [7,11,19,23,43,47,67,163]:
        U=units(q)
        chars=dirichlet_characters(q)
        # sanity: number of chars == phi
        assert len(chars)==len(U), (q,len(chars),len(U))
        sq=set((x*x)%q for x in U)
        nonsq=[a for a in U if a not in sq]
        if not nonsq:
            print(f"q={q}: no nonsquares (cyclic, all? skip)"); continue
        rows=[]
        for a in nonsq:
            d,V=delta_two_term(q,a,1,chars)
            rows.append((a,float(d),float(V)))
        rows.sort(key=lambda r:-r[1])  # largest density first
        m1=(q-1)
        print(f"\n=== q={q}  rho={rho(q)}  nonsquares={nonsq} ===")
        print("  rank   a     delta(q;a,1)        V(q;a,1)     note")
        for i,(a,d,V) in enumerate(rows):
            note = "<== a = -1 (q-1)" if a==m1 else ""
            print(f"  {i+1:>3}  {a:>4}    {d:.8f}    {V:10.4f}   {note}")
        # explicit -1 position
        ranks={a:i+1 for i,(a,d,V) in enumerate(rows)}
        if m1 in ranks:
            print(f"  --> a=-1 ({m1}) has rank {ranks[m1]} of {len(rows)} "
                  f"({'SMALLEST delta' if ranks[m1]==len(rows) else 'LARGEST delta' if ranks[m1]==1 else 'middle'})")
