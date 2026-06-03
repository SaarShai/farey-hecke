"""
Ordering check: with REALISTIC c_chi (analytic closed form), is V(q;-1,1) the LARGEST
among non-residues (=> delta smallest)?  This is the decisive discriminant claim.
c_chi = log(q/pi) + psi((1+a_chi)/2) + 2 Re L'/L(1,chi),  a_chi = (1-chi(-1))/2.
"""
import math, cmath
import mpmath as mp
from sympy.ntheory.residue_ntheory import primitive_root
from sympy import totient
mp.mp.dps = 25

def all_chars(q):
    phi=int(totient(q)); g=primitive_root(q)
    dlog={}; x=1
    for k in range(phi):
        dlog[x%q]=k; x=(x*g)%q
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    chars=[]
    for j in range(1,phi):  # nonprincipal
        chi={a: cmath.exp(2j*math.pi*dlog[a]*j/phi) for a in units}
        isodd = abs(chi[(q-1)%q]+1)<1e-9
        chars.append((j,chi,isodd))
    return chars, units, phi

def LprimeL_at_1(chi, q, Npr=200000):
    """Re L'/L(1,chi) = Re( -sum_p sum_k (log p) chi(p^k) p^{-k} ).  Truncated prime sum."""
    # sieve primes up to Npr
    sieve=bytearray([1])*(Npr+1); sieve[0]=sieve[1]=0
    for i in range(2,int(Npr**0.5)+1):
        if sieve[i]:
            sieve[i*i::i]=bytearray(len(sieve[i*i::i]))
    s=0.0
    for p in range(2,Npr+1):
        if not sieve[p]: continue
        if q % p == 0: continue
        lp=math.log(p); pk=p; k=1
        while pk<=Npr*50 and k<=40:
            s += lp * (chi[p%q].real) / pk  # Re chi(p^k)=Re(chi(p)^k); use chi[p^k mod q]
            # better: chi(p^k)=chi[(p**k)%q]
            k+=1; pk*=p
    # redo precisely with chi(p^k)
    s=0.0
    for p in range(2,Npr+1):
        if not sieve[p] or q%p==0: continue
        lp=math.log(p); k=1; pk=p
        while pk <= Npr and k<=60:
            s += lp*(chi[pk%q].real)/pk
            k+=1; pk*=p
    return -s

def c_chi_analytic(chi, isodd, q):
    a_chi = 1 if isodd else 0
    arch = math.log(q/math.pi) + float(mp.digamma((1+a_chi)/2.0))
    return arch + 2*LprimeL_at_1(chi,q)

for q in [7,11,19,23]:
    chars, units, phi = all_chars(q)
    sqs=set((b*b)%q for b in units)
    cvals={j:c_chi_analytic(chi,isodd,q) for j,chi,isodd in chars}
    def V(a):
        return sum(cvals[j]*abs(chi[a]-1)**2 for j,chi,isodd in chars)
    minus1=(q-1)%q
    nr=[a for a in units if a not in sqs]
    ranked=sorted(nr, key=lambda a:-V(a))
    rk=ranked.index(minus1)+1
    print(f"q={q:2d}: V(-1)={V(minus1):.4f}  Vmax_NR={V(ranked[0]):.4f}  "
          f"-1 rank {rk}/{len(nr)} by variance "
          f"{'(LARGEST => smallest delta => LEAST-biased NR) OK' if rk==1 else 'NOT largest!'}")
    # also delta via 2-term FM asymptotic (valid for ordering): delta=1/2+rho/sqrt(2 pi V)
    rho=sum(1 for x in units if (x*x)%q==1)
    dvals={a: 0.5+rho/math.sqrt(2*math.pi*V(a)) for a in nr}
    dmin=min(dvals,key=lambda a:dvals[a])
    print(f"       delta-min among NR at a={dmin} (-1={minus1}): "
          f"{'MATCH -1 is least-biased' if dmin==minus1 else 'mismatch'}; "
          f"delta(-1)={dvals[minus1]:.5f}")
