"""
TASK 5b PROOF SCHEMA verification.
Establish the EXACT inequality controlling whether a=-1 density-dominates all
other non-residues in the delta(q;a,1) hierarchy, and verify it numerically.

All CONDITIONAL on GRH+LI (FM Thm 1.1 / Thm 1.10 framework).
We RUN every number; nothing fabricated.
"""
import mpmath as mp
mp.mp.dps = 30

from sympy import primerange, isprime
from sympy.ntheory.residue_ntheory import primitive_root

GAMMA0 = mp.euler  # Euler-Mascheroni
LOG2 = mp.log(2)

def vonmangoldt(n):
    # Lambda(n): log p if n=p^k, else 0
    n = int(n)
    if n < 2:
        return mp.mpf(0)
    f = {}
    m = n
    d = 2
    while d*d <= m:
        while m % d == 0:
            f[d] = f.get(d,0)+1
            m//=d
        d+=1
    if m>1:
        f[m]=f.get(m,0)+1
    if len(f)==1:
        p = list(f.keys())[0]
        return mp.log(p)
    return mp.mpf(0)

def inv_mod(a,q):
    return pow(a, -1, q)

def Lambda_q_prime(q):
    # FM Def 1.5 for prime q: L(q) = log( q / (2 pi e^{gamma0}) )
    return mp.log(q) - mp.log(2*mp.pi) - GAMMA0

def D_prime(q, a):
    """FM Cor 1.9 explicit D(q;a,1) for PRIME q (FM_text.txt ~line 4043):
       D(q;a,1) = i_q(-a) log2 + Lambda(a)/a + Lambda(a^{-1})/a^{-1} + 2 log q /(q(q-1))
       i_q(-a)=1 iff -a == 1 mod q iff a == -1 mod q.
       a^{-1} taken as least positive residue.
    """
    ainv = inv_mod(a % q, q)
    iq = LOG2 if (a % q) == (q-1) else mp.mpf(0)
    t_a   = vonmangoldt(a % q)/(a % q)
    t_ai  = vonmangoldt(ainv)/ainv
    tail  = 2*mp.log(q)/(q*(q-1))
    return iq + t_a + t_ai + tail

def is_nonsquare(a,q):
    a%=q
    if a==0: return False
    qrs = set((x*x)%q for x in range(1,q))
    return a not in qrs

# ---------------------------------------------------------------------------
# CORE CLAIM: for prime q, delta(q;a,1) ordering is REVERSE of D(q;a,1) ordering
# (FM Cor 1.9: larger D => smaller delta), to leading two-term order.
# "-1 dominates (tops delta)"  <=>  D(q;-1,1) is the MINIMUM over nonsquares a.
# We test the OPPOSITE: is D(q;-1,1) the MAXIMUM?  (=> -1 is delta-MINIMUM)
# ---------------------------------------------------------------------------

print("="*78)
print("EXACT INEQUALITY:  delta(q;a,1) ranks as the REVERSE of D(q;a,1).")
print("  D(q;a,1) = i_q(-a)log2 + L(a)/a + L(a^{-1})/a^{-1} + 2 log q/(q(q-1)).")
print("  i_q(-a)log2 = log2  IFF  a == -1 (mod q); = 0 otherwise.")
print("  -1 tops delta  <=>  D(q;-1,1) is the MINIMUM over nonsquares a.")
print("="*78)

for q in [7,11,19,23,43,67,79,83,103,127,163,167,199,211,223,227,239,251,263,271,283]:
    if not isprime(q):
        continue
    if q % 4 != 3:
        continue  # need -1 a nonsquare
    NRs = [a for a in range(2,q) if is_nonsquare(a,q)]
    Ds = [(a, D_prime(q,a)) for a in NRs]
    Ds.sort(key=lambda t: -t[1])  # descending D
    m1 = q-1
    Dm1 = D_prime(q,m1)
    # rank of -1 by D (1 = largest D)
    rankD = 1 + sum(1 for (a,d) in Ds if d > Dm1 + mp.mpf('1e-25'))
    is_maxD = (Ds[0][0]==m1)
    # the gap to the next-largest D among OTHER nonsquares
    others = [d for (a,d) in Ds if a!=m1]
    gap = Dm1 - max(others)
    print(f"q={q:4d}  phi={q-1:4d}  #NR={len(NRs):3d}  "
          f"D(-1)={float(Dm1):.6f}  rank_by_D={rankD} "
          f"(1=max)  -1 is D-max:{is_maxD}  gap_to_next={float(gap):+.6f}")

print()
print("INTERPRETATION: rank_by_D == 1 (always) => -1 has the LARGEST D")
print("  => -1 has the SMALLEST delta(q;a,1)  => -1 is the LEAST-biased NR,")
print("  the EXACT OPPOSITE of '-1 dominates'. (FM Thm 1.10, GRH+LI.)")
