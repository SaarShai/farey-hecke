import mpmath as mp
import math
mp.mp.dps = 30

# Dirichlet characters mod q via primitive root, compute L(1/2,chi) and check vanishing.
# We use mpmath's built-in via Hurwitz zeta: L(s,chi)=q^{-s} sum_{a=1}^{q} chi(a) zeta(s, a/q)
def chars_mod(q):
    # build all Dirichlet characters mod q as functions, using group (Z/q)^*
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    n=len(units)
    # find generators via brute force decomposition is overkill; use sympy
    import sympy
    G = sympy.ntheory.residue_ntheory  # not directly chars
    # Build characters by discrete log on the abelian group structure using sympy's nthroot? 
    # Simpler: use the fact (Z/q)* for q in {7,8,11,5,3,13} is cyclic or known.
    return units

def Lchi(s, q, chi):
    # chi: dict a-> complex value on units, 0 else
    tot = mp.mpc(0)
    for a in range(1,q+1):
        ca = chi.get(a%q,0)
        if ca!=0:
            tot += ca*mp.zeta(s, mp.mpf(a)/q)
    return q**(-s)*tot

def cyclic_chars(q,g):
    # (Z/q)* cyclic with generator g, order n=phi
    units=[a for a in range(1,q) if math.gcd(a,q)==1]
    n=len(units)
    # discrete log table
    dlog={}
    cur=1
    for k in range(n):
        dlog[cur]=k
        cur=(cur*g)%q
    chars=[]
    for j in range(n):  # character index
        chi={}
        for a in units:
            chi[a]=mp.e**(2j*mp.pi*j*dlog[a]/n)
        chars.append(chi)
    return chars,n

# q=7 cyclic, generator 3 ; q=11 cyclic gen 2 ; q=5 gen 2 ; q=13 gen 2 ; q=3 gen 2
for q,g in [(3,2),(5,2),(7,3),(11,2),(13,2),(23,5)]:
    chars,n=cyclic_chars(q,g)
    print(f"--- q={q} phi={n} ---")
    for j,chi in enumerate(chars):
        if j==0: 
            continue  # principal
        val=Lchi(mp.mpf(0.5),q,chi)
        # quadratic char is j=n/2
        tag=""
        if n%2==0 and j==n//2: tag=" (quadratic/Legendre)"
        print(f"  chi_{j}: L(1/2)= {mp.nstr(val,8)}  |L|={mp.nstr(abs(val),6)}{tag}")
