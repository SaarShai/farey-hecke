"""
For q=7, q=8, q=11: compute c_chi for EVERY nonprincipal chi via the analytic formula
  c_chi = log(q/pi) + psi((1+a)/2) + 2 Re L'/L(1,chi),  a=parity.
(Validated above against zero-sum for the quadratic chars.)
Then form Var(D_a) = sum_chi c_chi |chi(a)-1|^2 with REAL c_chi, and rank NR.
This is the ACTUAL test: does -1 maximize variance with realistic c_chi?
"""
import mpmath as mp
mp.mp.dps = 25
import math, cmath
from sympy.ntheory.residue_ntheory import primitive_root
from sympy import totient

def Lval_general(chi_dict,q,s):
    return sum(chi_dict[r]*mp.zeta(s,mp.mpf(r)/q) for r in chi_dict)*mp.power(q,-s)

def all_chars(q):
    phi=int(totient(q)); g=primitive_root(q)
    dlog={}; x=1
    for k in range(phi):
        dlog[x%q]=k; x=(x*g)%q
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    chars=[]
    for j in range(1,phi):
        chi={a: cmath.exp(2j*math.pi*dlog[a]*j/phi) for a in units}
        chi_mp={a: mp.e**(2j*mp.pi*dlog[a]*j/phi) for a in units}
        is_odd = abs(chi[(q-1)%q]+1)<1e-9
        chars.append((chi,chi_mp,is_odd,j))
    return chars, units, phi

def c_chi_analytic(chi_mp,q,is_odd):
    a=1 if is_odd else 0
    LL=mp.diff(lambda z: mp.log(Lval_general(chi_mp,q,z)), mp.mpf(1), h=mp.mpf('1e-7'))
    return mp.re(mp.log(mp.mpf(q)/mp.pi)+mp.digamma((1+a)/mp.mpf(2))+2*mp.re(LL))

for q in [7,11,19,23]:
    chars,units,phi=all_chars(q)
    sqs=set((b*b)%q for b in units)
    cvals=[]
    for chi,chi_mp,is_odd,j in chars:
        c=c_chi_analytic(chi_mp,q,is_odd)
        cvals.append((chi,is_odd,float(c),j))
    odd_c=[c for chi,o,c,j in cvals if o]
    even_c=[c for chi,o,c,j in cvals if not o]
    print(f"\nq={q}: phi={phi}  mean c_chi(odd)={sum(odd_c)/len(odd_c):.4f} (n={len(odd_c)})  "
          f"mean c_chi(even)={ (sum(even_c)/len(even_c)) if even_c else float('nan'):.4f} (n={len(even_c)})")
    # variance per a
    res=[]
    for a in units:
        V=sum(c*abs(chi[a]-1)**2 for chi,o,c,j in cvals)
        res.append((V,a,a in sqs))
    minus1=(q-1)%q
    nrs=sorted([(V,a) for V,a,isq in res if not isq],reverse=True)
    rank=[a for V,a in nrs].index(minus1)+1
    print(f"   NR variance ranking (desc): "+", ".join(f"a={a}:{V:.3f}{'*' if a==minus1 else ''}" for V,a in nrs))
    print(f"   => -1 (a={minus1}) variance rank among NR = {rank}/{len(nrs)}   {'<<< -1 has MAX variance' if rank==1 else ''}")
