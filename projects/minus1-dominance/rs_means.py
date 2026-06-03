"""
Rubinstein-Sarnak leading-order mean of the normalized prime-race error.

Setup. For modulus N, residue class a coprime to N, the normalized error in
the race against the principal class is

  E(x;N,a) = (phi(N) * log x / sqrt(x)) * D(x;N,a),   D = pi(x;N,a) - pi(x;N,1).

Under GRH+LI the random vector (E(x;N,a))_a converges (in log-mean) to a
limiting distribution whose MEAN vector is
  mu(a) = -1 + c_2(a),   c_2(a) = #{ b mod N : b^2 == a (mod N), gcd(b,N)=1 }.

c_2(a) is the number of square-roots of a. For a a NON-residue, c_2(a)=0 so
mu(a) = -1 for EVERY non-residue. For a a residue, c_2(a) >= 1.

(The constant -1 comes from the prime-counting bias: squares of primes p^2 = a
contribute to pi(x;N,a) iff a is a square mod N; the principal class always
gets the +1 from... actually the -1 is the contribution of the chi for which
b^2=1, i.e. comparison baseline. Standard: Rubinstein-Sarnak 1994, eq. for
the mean E[X_{N;a}] = -1 + #sqrt(a).)

This script verifies the tie at leading order for non-residues and prints the
mean vector for several moduli.
"""
import sympy
from sympy import primerange

def units(N):
    return [a for a in range(1,N) if sympy.gcd(a,N)==1]

def sqrt_count(N):
    U = units(N)
    cnt = {a:0 for a in U}
    for b in U:
        cnt[(b*b)%N]+=1
    return cnt

def residue_status(N):
    """1 if QR, 0 if NQR (among units)."""
    U=units(N); sq=set((b*b)%N for b in U)
    return {a:(1 if a in sq else 0) for a in U}

for N in [5,7,8,11,12,19,23]:
    U=units(N); sc=sqrt_count(N); rs=residue_status(N)
    print(f"\n=== N={N}  units={U} ===")
    print("  a : QR? sqrt_count mu=-1+sqrt_count")
    for a in U:
        if a==1: continue
        tag=""
        if a==(N-1): tag="  <== a=-1"
        print(f"  {a:3d}: {'QR ' if rs[a] else 'NQR'}  {sc[a]:2d}   mu={-1+sc[a]:+d}{tag}")
    nqr=[a for a in U if rs[a]==0]
    mus=set(-1+sc[a] for a in nqr)
    print(f"  non-residues: {nqr}")
    print(f"  distinct mean values among NR: {mus}  -> {'ALL TIE at -1' if mus=={-1} else 'NOT all tie'}")
