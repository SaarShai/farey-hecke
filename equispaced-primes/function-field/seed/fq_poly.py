"""
Polynomial arithmetic over F_q for tiny q (specifically q=2 packed as Python int,
and general q stored as tuple of coefficients).

Convention for F_2 packed-int representation:
    A polynomial sum_i a_i T^i with a_i in {0,1} is stored as the integer
    sum_i a_i * 2^i. Multiplication is carry-less (XOR for add, schoolbook for mul).
    Degree is bit_length - 1 (for nonzero).

For general q (we use q=3), polynomial is a tuple of ints in [0,q) with index = T-power.
"""

# ---------- F_2 (packed int) ----------

def f2_deg(a):
    return a.bit_length() - 1  # -1 for the zero polynomial


def f2_mul(a, b):
    # Carry-less multiplication
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def f2_divmod(a, b):
    # Returns (q, r) with a = b*q + r, deg(r) < deg(b).
    if b == 0:
        raise ZeroDivisionError
    db = f2_deg(b)
    q = 0
    while True:
        da = f2_deg(a)
        if da < db:
            break
        shift = da - db
        q ^= 1 << shift
        a ^= b << shift
    return q, a


def f2_mod(a, b):
    if b == 0:
        raise ZeroDivisionError
    db = f2_deg(b)
    while True:
        da = f2_deg(a)
        if da < db:
            return a
        a ^= b << (da - db)


def f2_gcd(a, b):
    while b:
        a, b = b, f2_mod(a, b)
    return a


def f2_pow_mod(base, exp, mod):
    # base^exp mod (mod), all over F_2.
    result = 1
    base = f2_mod(base, mod)
    while exp:
        if exp & 1:
            result = f2_mod(f2_mul(result, base), mod)
        base = f2_mod(f2_mul(base, base), mod)
        exp >>= 1
    return result


def f2_is_irreducible(p):
    """Rabin's test in F_2[T]. p > 1 monic (highest bit set)."""
    n = f2_deg(p)
    if n <= 0:
        return False
    if n == 1:
        return True
    # Distinct prime divisors of n
    primes = []
    m = n
    d = 2
    while d * d <= m:
        if m % d == 0:
            primes.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        primes.append(m)
    # T mod p
    Tmod = 2 % p if p != 2 else 0  # T = 0b10 = 2
    Tmod = 2
    if p == 2:
        return False  # deg 1, but p=2 = T itself; deg(T) = 1, so the n==1 branch caught it
    # 1) T^(2^n) == T mod p
    e = 2 ** n
    if f2_pow_mod(Tmod, e, p) != Tmod % p if False else None:
        pass  # placeholder
    # Compute T^(2^n) mod p by repeated squaring n times
    cur = Tmod % p
    # We want T^(2^n) mod p; compute by squaring n times starting from T.
    for _ in range(n):
        cur = f2_mod(f2_mul(cur, cur), p)
    if cur != Tmod % p:
        return False
    # 2) For each prime divisor q of n, gcd(T^(2^(n/q)) - T, p) == 1
    for qp in primes:
        cur = Tmod % p
        for _ in range(n // qp):
            cur = f2_mod(f2_mul(cur, cur), p)
        diff = cur ^ (Tmod % p)
        if diff == 0:
            return False
        g = f2_gcd(p, diff)
        if f2_deg(g) > 0:
            return False
    return True


def f2_monic_polys_of_degree(n):
    """Yield all monic polynomials of degree n in F_2[T], packed as ints."""
    if n == 0:
        yield 1
        return
    top = 1 << n
    for low in range(1 << n):
        yield top | low


# ---------- F_q (general; coefficient tuple) ----------

def fq_normalize(a, q):
    # Strip leading zeros
    while len(a) > 1 and a[-1] == 0:
        a = a[:-1]
    return a


def fq_deg(a):
    if len(a) == 1 and a[0] == 0:
        return -1
    return len(a) - 1


def fq_add(a, b, q):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        x = a[i] if i < len(a) else 0
        y = b[i] if i < len(b) else 0
        out[i] = (x + y) % q
    return tuple(fq_normalize(tuple(out), q))


def fq_sub(a, b, q):
    n = max(len(a), len(b))
    out = [0] * n
    for i in range(n):
        x = a[i] if i < len(a) else 0
        y = b[i] if i < len(b) else 0
        out[i] = (x - y) % q
    return tuple(fq_normalize(tuple(out), q))


def fq_mul(a, b, q):
    if (len(a) == 1 and a[0] == 0) or (len(b) == 1 and b[0] == 0):
        return (0,)
    out = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0:
                continue
            out[i + j] = (out[i + j] + ai * bj) % q
    return tuple(fq_normalize(tuple(out), q))


def fq_scalar_mul(a, c, q):
    if c == 0:
        return (0,)
    return tuple((x * c) % q for x in a)


def fq_inv(c, q):
    # c in F_q^*, q prime. Use Fermat.
    return pow(c, q - 2, q)


def fq_divmod(a, b, q):
    if fq_deg(b) < 0:
        raise ZeroDivisionError
    a = list(a)
    qr = [0] * max(0, fq_deg(a) - fq_deg(b) + 1) if fq_deg(a) >= fq_deg(b) else [0]
    while fq_deg(tuple(fq_normalize(tuple(a), q))) >= fq_deg(b):
        a = list(fq_normalize(tuple(a), q))
        da = len(a) - 1
        db = len(b) - 1
        shift = da - db
        lead_a = a[-1]
        lead_b = b[-1]
        coef = (lead_a * fq_inv(lead_b, q)) % q
        # qr[shift] += coef
        while len(qr) <= shift:
            qr.append(0)
        qr[shift] = (qr[shift] + coef) % q
        # a -= coef * b shifted by `shift`
        for j, bj in enumerate(b):
            a[shift + j] = (a[shift + j] - coef * bj) % q
        # drop the leading zero
        a = list(fq_normalize(tuple(a), q))
        if len(a) == 1 and a[0] == 0:
            break
    return tuple(fq_normalize(tuple(qr), q)), tuple(fq_normalize(tuple(a), q))


def fq_mod(a, b, q):
    _, r = fq_divmod(a, b, q)
    return r


def fq_gcd(a, b, q):
    while not (len(b) == 1 and b[0] == 0):
        a, b = b, fq_mod(a, b, q)
    # Make monic
    if len(a) == 1 and a[0] == 0:
        return a
    lead = a[-1]
    if lead != 1:
        inv = fq_inv(lead, q)
        a = tuple((x * inv) % q for x in a)
    return a


def fq_pow_mod(base, exp, mod, q):
    result = (1,)
    base = fq_mod(base, mod, q)
    while exp:
        if exp & 1:
            result = fq_mod(fq_mul(result, base, q), mod, q)
        base = fq_mod(fq_mul(base, base, q), mod, q)
        exp >>= 1
    return result


def fq_is_irreducible(p, q):
    """Rabin's test on monic p of degree n in F_q[T]."""
    n = fq_deg(p)
    if n <= 0:
        return False
    if n == 1:
        return True
    primes = []
    m = n
    d = 2
    while d * d <= m:
        if m % d == 0:
            primes.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        primes.append(m)
    T = (0, 1)
    # T^(q^n) mod p
    cur = T
    for _ in range(n):
        # Raise to qth power: cur = cur^q mod p
        cur = fq_pow_mod(cur, q, p, q)
    if cur != T:
        return False
    for qp in primes:
        cur = T
        for _ in range(n // qp):
            cur = fq_pow_mod(cur, q, p, q)
        diff = fq_sub(cur, T, q)
        if len(diff) == 1 and diff[0] == 0:
            return False
        g = fq_gcd(p, diff, q)
        if fq_deg(g) > 0:
            return False
    return True


def fq_monic_polys_of_degree(n, q):
    """Iterate monic polys of degree n over F_q as coefficient tuples."""
    if n == 0:
        yield (1,)
        return
    # coefficients[0..n-1] arbitrary in F_q, coefficients[n] = 1
    digits = [0] * n
    total = q ** n
    for k in range(total):
        kk = k
        for i in range(n):
            digits[i] = kk % q
            kk //= q
        yield tuple(digits) + (1,)


if __name__ == "__main__":
    # Sanity tests
    # F_2 irreducibles of degree <= 4
    for n in range(1, 5):
        count = sum(1 for p in f2_monic_polys_of_degree(n) if f2_is_irreducible(p))
        # Expected: deg1: 2, deg2: 1, deg3: 2, deg4: 3
        print(f"F_2 deg {n}: {count} irreducibles")
    # F_3
    for n in range(1, 5):
        count = sum(1 for p in fq_monic_polys_of_degree(n, 3) if fq_is_irreducible(p, 3))
        # Expected: deg1: 3, deg2: 3, deg3: 8, deg4: 18
        print(f"F_3 deg {n}: {count} irreducibles")
