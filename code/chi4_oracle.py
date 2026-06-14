#!/usr/bin/env python3
"""
chi4_oracle.py -- EXACT-arithmetic QUARTIC reciprocity symbol chi_4 in Z[i],
following Haag-Kertzer-Rickards-Stange, arXiv:2307.02749, Section 5.

Implements:
  - Gaussian-integer arithmetic (exact, Python ints).
  - The quartic residue symbol [alpha/beta] in Z[i] (Definition 5.2 / Prop 5.3-5.4),
    computed by the standard reciprocity algorithm (analogue of the Jacobi-symbol
    binary-GCD reduction, using quartic reciprocity for Z[i]).
  - chi_4(C) for a circle of curvature n in an Apollonian packing of type (6,1)/(6,17)
    via the tangency structure (Prop 5.8 / Def 5.6): for tangent coprime curvatures
    n1, n2 there is beta in Z[i] with N(beta) = n1 + n2 valid for both circles, and
    chi_4(C1) = chi_4(C2) propagates (Prop 5.9).

ORACLE checks (must pass before trusting any chi_4 value):
  O1. quartic symbol multiplicativity (Prop 5.3a), congruence (5.3b), integer case (5.3c).
  O2. supplementary laws (Prop 5.4) for primary alpha: [i/alpha], [-1/alpha], [(1+i)/alpha], [2/alpha].
  O3. quartic reciprocity (Prop 5.4) on random primary coprime pairs.
  O4. chi_4^2 == chi_2  (Prop 5.12) on the standard gasket / type-(6,1) packing.
  O5. [alpha/beta] is a power of i, and [alpha/beta]^2 == Kronecker(N(alpha), N(beta))-type
      consistency  (Prop 5.12 ingredient: [N(beta)/n] over Z relation).

All Gaussian integers represented as (re, im) tuples of Python ints.
"""

from math import gcd

# ---------------------------------------------------------------------------
# Gaussian integer arithmetic  (exact).
# ---------------------------------------------------------------------------

def gmul(a, b):
    (ar, ai), (br, bi) = a, b
    return (ar * br - ai * bi, ar * bi + ai * br)

def gadd(a, b):
    return (a[0] + b[0], a[1] + b[1])

def gsub(a, b):
    return (a[0] - b[0], a[1] - b[1])

def gnorm(a):
    return a[0] * a[0] + a[1] * a[1]

def gconj(a):
    return (a[0], -a[1])

def gdivmod(a, b):
    """Exact Euclidean division in Z[i]: a = q*b + r with N(r) < N(b).
    q = round(a / b) componentwise (nearest Gaussian integer)."""
    nb = gnorm(b)
    # a * conj(b) / N(b)
    num = gmul(a, gconj(b))
    qr = _nint(num[0], nb)
    qi = _nint(num[1], nb)
    q = (qr, qi)
    r = gsub(a, gmul(q, b))
    return q, r

def _nint(p, q):
    """Nearest integer to p/q (round half away from zero), exact integer arithmetic."""
    # round(p/q): floor(p/q + 1/2) for the standard nearest; ties handled consistently.
    if q < 0:
        p, q = -p, -q
    # nearest integer
    twice = 2 * p
    fl = twice // (2 * q)        # floor(p/q)
    rem = p - fl * q
    if 2 * rem > q:
        return fl + 1
    elif 2 * rem == q:
        return fl + 1            # round half up (any consistent rule is fine for gcd)
    else:
        return fl

def ggcd(a, b):
    while b != (0, 0):
        _, r = gdivmod(a, b)
        a, b = b, r
    return a

UNITS = [(1, 0), (0, 1), (-1, 0), (0, -1)]   # 1, i, -1, -i  (i^0..i^3)

def is_unit(a):
    return gnorm(a) == 1

def is_odd(a):
    return gnorm(a) % 2 == 1

def make_primary(alpha):
    """Return the unique primary associate of an ODD alpha (alpha = 1 mod (2+2i)),
    plus the unit u such that primary = u * alpha (u in UNITS as power of i).
    Primary: (a,b) = (1,0) or (3,2) mod 4  (Definition 5.1)."""
    assert is_odd(alpha), f"alpha must be odd, got {alpha} norm {gnorm(alpha)}"
    cur = alpha
    for k in range(4):
        a, b = cur[0] % 4, cur[1] % 4
        if (a, b) in ((1, 0), (3, 2)):
            return cur, k          # cur = i^k * alpha
        cur = gmul((0, 1), cur)    # multiply by i
    raise RuntimeError(f"no primary associate for {alpha}")

def is_primary(alpha):
    if not is_odd(alpha):
        return False
    a, b = alpha[0] % 4, alpha[1] % 4
    return (a, b) in ((1, 0), (3, 2))

# ---------------------------------------------------------------------------
# Quartic residue symbol  [alpha / beta]  in Z[i]   (Definition 5.2).
# Returns the exponent k in {0,1,2,3} meaning the value i^k.
# Computed by the reciprocity algorithm (Lemmermeyer Ch.6; Prop 5.3, 5.4).
# ---------------------------------------------------------------------------

def _quartic_supp_i(alpha):
    """[i/alpha] = i^((1-a)/2)  for primary alpha=a+bi  (Prop 5.4).  Returns exponent mod 4."""
    a = alpha[0]
    return ((1 - a) // 2) % 4

def _quartic_supp_1pi(alpha):
    """[(1+i)/alpha] = i^((a-b-b^2-1)/4) for primary alpha=a+bi (Prop 5.4). Returns exponent."""
    a, b = alpha
    num = (a - b - b * b - 1)
    assert num % 4 == 0, f"(1+i) supplement exponent not integral for {alpha}: {num}"
    return (num // 4) % 4

def quartic_symbol(alpha, beta):
    """Quartic residue symbol [alpha/beta], beta ODD (N(beta) odd), gcd(alpha,beta)=1 (unit gcd).
    Returns exponent k in {0,1,2,3}: the symbol value is i^k.
    Algorithm: reduce via (a) factoring out the unit and (1+i) part of the numerator,
    using supplements; (b) flip via quartic reciprocity when both primary; recurse.
    """
    a = alpha
    b = beta
    assert is_odd(b), f"denominator must be odd: {b} norm {gnorm(b)}"
    # gcd check (non-unit gcd => symbol 0; should not occur in our use)
    g = ggcd(a, b)
    if not is_unit(g):
        return None  # not coprime; symbol = 0 (handle by caller)

    result = 0  # exponent of i, mod 4

    # make denominator primary
    bp, ub = make_primary(b)        # bp = i^ub * b ; but symbol depends only on residue class:
    # [alpha/beta]: extend multiplicatively in denominator; for a unit u, [alpha/u]=1.
    # beta and its associate i^k*beta: [alpha/(i^k beta)] = [alpha/i^k]*[alpha/beta]
    # and [alpha/unit]=1.  So associates of beta give the SAME symbol value.  Use primary bp.
    b = bp

    a = _greduce_mod(a, b)          # reduce numerator mod beta (Prop 5.3b)
    while True:
        if a == (0, 0):
            return None  # gcd nontrivial
        # factor out unit and (1+i) powers from a
        # remove (1+i) factors
        cnt1pi = 0
        while gnorm(a) % 2 == 0:
            q, r = gdivmod(a, (1, 1))
            assert r == (0, 0)
            a = q
            cnt1pi += 1
        if cnt1pi:
            result = (result + cnt1pi * _quartic_supp_1pi(b)) % 4
        # now a is odd. factor out unit -> primary
        ap, ua = make_primary(a)
        # a = i^{-ua} * ap  => [a/b] = [i^{-ua}/b]*[ap/b] = [i/b]^{-ua} * [ap/b]
        result = (result + ((-ua) % 4) * _quartic_supp_i(b)) % 4
        a = ap
        if a == (1, 0):
            return result % 4
        # quartic reciprocity: [a/b] = [b/a] * (-1)^{(N(a)-1)/4 * (N(b)-1)/4}
        ea = (gnorm(a) - 1) // 4
        eb = (gnorm(b) - 1) // 4
        if (ea % 2) * (eb % 2) == 1:
            # multiply by (-1) = i^2
            result = (result + 2) % 4
        # flip
        a, b = b, a
        a = _greduce_mod(a, b)

def _greduce_mod(a, b):
    """a mod b in Z[i] (representative of smallest norm), exact."""
    _, r = gdivmod(a, b)
    return r

def quartic_value(alpha, beta):
    """Return the symbol value as a unit tuple (i^k), or None if not coprime."""
    k = quartic_symbol(alpha, beta)
    if k is None:
        return None
    return UNITS[k % 4]

# ---------------------------------------------------------------------------
# Quartic symbol with denominator an ODD POSITIVE INTEGER n  (the chi_4 use-case,
# Def 5.6: [beta/n'] with n' odd positive integer; Prop 5.3c, 5.4 last line).
# When the denominator is a rational odd prime p, factor it in Z[i]:
#   p == 1 mod 4: p = pi * conj(pi);  p == 3 mod 4: p inert (prime in Z[i]).
# We compute [beta/n] for n odd positive integer by factoring n over Z then over Z[i].
# ---------------------------------------------------------------------------

def factor_int(n):
    n = int(abs(n))
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def gaussian_primes_above(p):
    """Return Gaussian prime(s) above rational prime p (p odd).
    p==3 mod4: [(p,0)] inert.  p==1 mod4: [pi, conj(pi)] with N(pi)=p."""
    if p % 4 == 3:
        return [(p, 0)]
    # p == 1 mod 4: find a,b with a^2+b^2=p
    # solve x^2 = -1 mod p, then gcd
    x = _sqrt_mod_neg1(p)
    pi = ggcd((p, 0), (x, 1))
    return [pi, gconj(pi)]

def _sqrt_mod_neg1(p):
    """Find x with x^2 == -1 mod p (p == 1 mod 4)."""
    # use a quadratic nonresidue: x = g^((p-1)/4)
    for g in range(2, p):
        # is g a QNR? Euler
        if pow(g, (p - 1) // 2, p) == p - 1:
            return pow(g, (p - 1) // 4, p)
    raise RuntimeError("no QNR found")

def quartic_symbol_int_denom(beta, n):
    """[beta / n] for n an ODD POSITIVE INTEGER, beta in Z[i], gcd(N(beta),n)=1.
    Multiplicative over the Gaussian-prime factorization of n.  Returns exponent k mod 4."""
    assert n % 2 == 1 and n > 0
    if n == 1:
        return 0
    f = factor_int(n)
    total = 0
    for p, e in f.items():
        for pi in gaussian_primes_above(p):
            mult = e
            # for inert p (3 mod4), gaussian_primes_above returns single (p,0) with that prime;
            # n contains p^e so the Gaussian valuation is e.
            k = quartic_symbol(beta, pi)
            if k is None:
                return None
            total = (total + mult * k) % 4
    return total % 4

# ---------------------------------------------------------------------------
# Kronecker symbol over Z  (for chi_2 comparison; reuse exact impl).
# ---------------------------------------------------------------------------

def kronecker(a, n):
    a = int(a); n = int(n)
    if n == 0:
        return 1 if (a == 1 or a == -1) else 0
    result = 1
    if n < 0:
        n = -n
        if a < 0:
            result = -result
    if n % 2 == 0:
        if a % 2 == 0:
            return 0
        while n % 2 == 0:
            n //= 2
            am8 = a % 8
            if am8 == 3 or am8 == 5:
                result = -result
    if n == 1:
        return result
    a = a % n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            nm8 = n % 8
            if nm8 == 3 or nm8 == 5:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    if n == 1:
        return result
    return 0


if __name__ == "__main__":
    print("chi4_oracle module: run chi4_oracle_test.py for self-tests")
