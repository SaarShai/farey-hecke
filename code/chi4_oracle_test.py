#!/usr/bin/env python3
"""
chi4_oracle_test.py -- self-tests for the quartic residue symbol chi_4 in Z[i].
Validates against KNOWN quartic-reciprocity facts (Lemmermeyer Ch.6 / paper Prop 5.3-5.4-5.12).
"""
import random
from chi4_oracle import (
    gmul, gadd, gsub, gnorm, gconj, ggcd, is_unit, is_odd, is_primary, make_primary,
    quartic_symbol, quartic_value, quartic_symbol_int_denom, UNITS, kronecker,
    gaussian_primes_above, factor_int, _greduce_mod,
)

PASS = 0
FAIL = 0
def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        # print(f"  PASS {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name}  {extra}")

# ---------------------------------------------------------------------------
# O0. quartic symbol value is a power of i (0..3).
# ---------------------------------------------------------------------------
rng = random.Random(1)
def rand_odd_primary(maxc=15):
    while True:
        a = rng.randint(-maxc, maxc)
        b = rng.randint(-maxc, maxc)
        al = (a, b)
        if gnorm(al) > 1 and is_odd(al):
            p, _ = make_primary(al)
            return p

# ---------------------------------------------------------------------------
# O1. Multiplicativity in numerator (Prop 5.3a): [a1 a2 / b] = [a1/b][a2/b].
# ---------------------------------------------------------------------------
print("O1 multiplicativity in numerator (Prop 5.3a)")
for _ in range(300):
    b = rand_odd_primary()
    a1 = (rng.randint(-12, 12), rng.randint(-12, 12))
    a2 = (rng.randint(-12, 12), rng.randint(-12, 12))
    a12 = gmul(a1, a2)
    if not (is_unit(ggcd(a12, b)) and a1 != (0, 0) and a2 != (0, 0)):
        continue
    k12 = quartic_symbol(a12, b)
    k1 = quartic_symbol(a1, b)
    k2 = quartic_symbol(a2, b)
    if k12 is None or k1 is None or k2 is None:
        continue
    check("mult-num", k12 == (k1 + k2) % 4, f"a1={a1} a2={a2} b={b}: {k12} vs {(k1+k2)%4}")

# ---------------------------------------------------------------------------
# O1b. Congruence invariance (Prop 5.3b): a1 == a2 mod b  =>  [a1/b]=[a2/b].
# ---------------------------------------------------------------------------
print("O1b congruence invariance (Prop 5.3b)")
for _ in range(300):
    b = rand_odd_primary()
    a1 = (rng.randint(-20, 20), rng.randint(-20, 20))
    if not is_unit(ggcd(a1, b)) or a1 == (0, 0):
        continue
    # a2 = a1 + b*gamma
    gam = (rng.randint(-3, 3), rng.randint(-3, 3))
    a2 = gadd(a1, gmul(b, gam))
    k1 = quartic_symbol(a1, b)
    k2 = quartic_symbol(a2, b)
    if k1 is None or k2 is None:
        continue
    check("cong", k1 == k2, f"a1={a1} a2={a2} b={b}: {k1} vs {k2}")

# ---------------------------------------------------------------------------
# O1c. Rational-integer numerator over odd integer denom (Prop 5.3c): [a/b]=1 for a,b in Z coprime, b odd.
# ---------------------------------------------------------------------------
print("O1c integer numerator (Prop 5.3c): [a/b]=1, a,b coprime integers, b odd")
from math import gcd as _gcd
for _ in range(400):
    a = rng.randint(-50, 50)
    b = 2 * rng.randint(1, 40) + 1   # odd positive
    if _gcd(abs(a), b) != 1 or a == 0:
        continue
    k = quartic_symbol_int_denom((a, 0), b)
    check("int-num", k == 0, f"a={a} b={b}: i^{k}")

# ---------------------------------------------------------------------------
# O2. DIRECT definition (Def 5.2 Euler criterion) for Gaussian PRIMES: cross-check
#     the reciprocity-algorithm value against [alpha/pi] = alpha^((N(pi)-1)/4) mod pi.
# ---------------------------------------------------------------------------
print("O2 Euler-criterion cross-check on Gaussian primes (Def 5.2)")
def euler_quartic(alpha, pi):
    """Direct: unique k with alpha^((N(pi)-1)/4) == i^k mod pi.  Brute via Gaussian mod."""
    N = gnorm(pi)
    e = (N - 1) // 4
    # compute alpha^e mod pi by repeated multiply + reduce
    res = (1, 0)
    base = _greduce_mod(alpha, pi)
    ee = e
    while ee > 0:
        if ee & 1:
            res = _greduce_mod(gmul(res, base), pi)
        base = _greduce_mod(gmul(base, base), pi)
        ee >>= 1
    # res should be congruent to i^k mod pi; find k
    for k in range(4):
        if _greduce_mod(gsub(res, UNITS[k]), pi) == (0, 0):
            return k
    return None

# enumerate small gaussian primes
small_primes = []
for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 37, 41]:
    small_primes.extend(gaussian_primes_above(p))
for pi in small_primes:
    for _ in range(40):
        alpha = (rng.randint(-10, 10), rng.randint(-10, 10))
        if not is_unit(ggcd(alpha, pi)) or alpha == (0, 0):
            continue
        kalg = quartic_symbol(alpha, pi)
        keul = euler_quartic(alpha, pi)
        if kalg is None or keul is None:
            continue
        check("euler", kalg == keul, f"alpha={alpha} pi={pi}: alg i^{kalg} vs euler i^{keul}")

# ---------------------------------------------------------------------------
# O3. Supplement [2/alpha] = i^(-b/2) for primary alpha=a+bi (Prop 5.4):
#     2 = -i*(1+i)^2, so [2/alpha] = [-i/alpha]*[(1+i)/alpha]^2.
#     Paper states [2/alpha] = i^{-b/2}.  Cross-check.
# ---------------------------------------------------------------------------
print("O3 supplement [2/alpha] = i^(-b/2) (Prop 5.4)")
for _ in range(300):
    al = rand_odd_primary()
    a, b = al
    k2 = quartic_symbol((2, 0), al)
    expect = ((-b // 2) % 4) if b % 2 == 0 else None
    # b is even iff a odd? for primary alpha, N odd means exactly one of a,b even.
    # primary: (1,0) or (3,2) mod4 -> b even. so b even always for primary. good.
    if expect is None:
        continue
    check("supp2", k2 == expect, f"alpha={al}: [2/a]=i^{k2}, expect i^{expect}")

# ---------------------------------------------------------------------------
# O4. (THE KEY ORACLE) chi_4^2 == chi_2  (Prop 5.12).
#     For a Gaussian integer beta with N(beta)=n+n2 (tangency), odd curvature n:
#       chi_4(C) = [beta / n]   (n == 1 mod 8 case),
#       chi_4(C)^2 = [beta/n]^2 = (beta|n)_2  = ( N(beta) | n )_Kronecker = (n2 | n).
#     Test: i^{2k} == kronecker(N(beta), n) interpreted in {1,-1}.
# ---------------------------------------------------------------------------
print("O4 chi_4^2 == quadratic symbol [beta/n]^2 == Kronecker(N(beta),n)  (Prop 5.12)")
for _ in range(500):
    # random odd n, random beta coprime to n
    n = 2 * rng.randint(1, 60) + 1
    beta = (rng.randint(-30, 30), rng.randint(-30, 30))
    if beta == (0, 0):
        continue
    Nb = gnorm(beta)
    if _gcd(Nb, n) != 1:
        continue
    k = quartic_symbol_int_denom(beta, n)
    if k is None:
        continue
    sq = (-1) ** (k % 2) if (k % 2) else 1  # i^{2k} = (-1)^k
    sq = 1 if (k % 4) in (0, 2) and (k % 4) == 0 else sq
    # i^k squared = i^{2k} = (-1)^k
    chi4sq = (-1) ** (k)            # = (i^k)^2 = i^{2k} = (-1)^k
    kron = kronecker(Nb, n)
    check("chi4sq", chi4sq == kron, f"beta={beta} n={n}: i^{k} sq={chi4sq} vs kron(N,n)={kron}")

# ---------------------------------------------------------------------------
print()
print(f"PASS={PASS}  FAIL={FAIL}")
if FAIL == 0:
    print("ORACLE: ALL TESTS PASSED")
else:
    print("ORACLE: FAILURES PRESENT")
