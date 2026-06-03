"""
Verify the Rubinstein-Sarnak mean formula for the normalized error vector.

RS (Experimental Math 3 (1994), 173-197) study, for fixed modulus q and
residue classes a_1,...,a_r coprime to q, the vector-valued function

  E(x; q, a) = (log x / sqrt(x)) * ( phi(q) * pi(x;q,a) - pi(x) )     [their normalization]

Equivalently using psi or theta. Under GRH the limiting logarithmic distribution
of E exists. Its MEAN is

  mean of E(.;q,a) = -1 + 2 * #{ b mod q : b^2 = a (mod q) }      ... (RS eq, "c_a")

Wait: RS write the mean of the a-component as  -c(q,a) where
  c(q,a) = -1 + #{ solutions b of b^2 = a mod q }.
The constant comes from the contribution of PRIME POWERS (squares of primes):
pi(x;q,a) counts p; but psi/theta vs pi correction and the p^2 = a condition.

Let me just verify the COUNT N(q,a) = #{b in (Z/q)^* : b^2 = a} and confirm:
  - a is a QR  => N(q,a) = #square roots > 0
  - a is a non-residue => N(q,a) = 0
  - so mean(a) = -1 + N(q,a); for ALL non-residues mean = -1 (TIE).
"""
from sympy import totient

def sqrt_count(q, a):
    """#{ b in (Z/q)^* : b^2 = a mod q }."""
    cnt = 0
    for b in range(q):
        if __import__('math').gcd(b, q) == 1 and (b*b - a) % q == 0:
            cnt += 1
    return cnt

def units(q):
    import math
    return [a for a in range(1, q) if math.gcd(a, q) == 1]

for q in [7, 8, 11, 19, 23, 5, 13, 3, 4, 12, 15, 24]:
    U = units(q)
    sqs = set((b*b) % q for b in U)  # quadratic residues
    print(f"\n=== q = {q}  (phi={totient(q)}, |QR|={len(sqs)}) ===")
    minus1 = (-1) % q
    nr_means = {}
    for a in U:
        N = sqrt_count(q, a)
        mean = -1 + N
        kind = "QR " if a in sqs else "NR "
        star = " <== a=-1" if a == minus1 else ""
        if a not in sqs:
            nr_means[a] = mean
        print(f"  a={a:3d} {kind} sqrt_count={N}  mean=-1+N = {mean:+d}{star}")
    if nr_means:
        vals = set(nr_means.values())
        print(f"  --> all NR means: {sorted(set(nr_means.values()))}  (TIE among NR: {len(vals)==1})")
