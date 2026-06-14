#!/usr/bin/env python3
"""
reciprocity_oracle.py  --  EXACT-arithmetic chi_2 reciprocity oracle.

Two reciprocity-obstruction primitives, both in exact integer arithmetic:

A. SL(2,Z)-semigroup chi_2  (Rickards-Stange, arXiv:2401.01860 / Duke 2025).
   The "chi_2 invariant" is the Kronecker symbol (x|y) on the orbit vector [x,y].
   A semigroup <G_1,...,G_k>^+  subset SL(2,Z)^{>=0} PRESERVES this symbol iff every
   generator G=[a,b;c,d] satisfies the kron_action triviality condition
   (Prop 3.2 of the paper, transcribed verbatim from the authors' PARI/GP code
   paper.gp:70-87, function kronaction).  If preserved AND (x|y)=-1 on a starting
   vector whose orbit congruences still ADMIT squares (no congruence explanation),
   the orbit has a RECIPROCITY OBSTRUCTION: it contains no squares.  (Def 2.4, Thm 2.5.)

B. Apollonian-curvature chi_2  (Haag-Kertzer-Rickards-Stange, arXiv:2307.02749, Def 4.3).
   For a curvature n with associated quadratic-form residue rho (the properly-
   represented invertible residue of the circle's form mod n, up to squares):
       chi_2 = (rho | n)        if n = 0,1 (mod 4)
             = (-rho | n/2)     if n = 2 (mod 4)
             = (2 rho | n)      if n = 3 (mod 4)      [Kronecker symbols]
   chi_2 is constant on the whole packing; chi_2 = -1 forces a missing square-class
   family {n^2, 2n^2, 3n^2, 6n^2}-type set (Prop 4.10).

Exact arithmetic throughout: Kronecker symbol implemented from scratch on Python ints.

This file: oracle definitions + self-tests.  Scan harness is reciprocity_scan.py.
"""

# ----------------------------------------------------------------------------
# Exact Kronecker / Jacobi symbol on arbitrary Python ints.
# ----------------------------------------------------------------------------

def kronecker(a, n):
    """Kronecker symbol (a|n), exact, for arbitrary integers a,n.
    Matches PARI/GP kronecker(a,n).  Returns -1,0,+1."""
    a = int(a); n = int(n)
    if n == 0:
        return 1 if (a == 1 or a == -1) else 0
    # sign of n
    result = 1
    if n < 0:
        n = -n
        if a < 0:
            result = -result
    # factor out powers of 2 from n
    if n % 2 == 0:
        if a % 2 == 0:
            return 0
        # (a|2): 0 if a even, 1 if a=+-1 mod 8, -1 if a=+-3 mod 8
        while n % 2 == 0:
            n //= 2
            am8 = a % 8
            if am8 == 3 or am8 == 5:
                result = -result
    if n == 1:
        return result
    # now n is odd, >=3.  Jacobi symbol (a|n) via reciprocity.
    a = a % n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            nm8 = n % 8
            if nm8 == 3 or nm8 == 5:
                result = -result
        # swap (quadratic reciprocity)
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    if n == 1:
        return result
    return 0


# ----------------------------------------------------------------------------
# A.  SL(2,Z)-semigroup chi_2  (Kronecker symbol on orbit vector).
# ----------------------------------------------------------------------------

def oddpart(m):
    m = abs(int(m))
    if m == 0:
        return 0
    while m % 2 == 0:
        m //= 2
    return m

def valuation2(m):
    m = abs(int(m))
    if m == 0:
        return 10**9
    v = 0
    while m % 2 == 0:
        m //= 2
        v += 1
    return v

def kron_action(M, x, y):
    """Verbatim transcription of paper.gp kronaction(M,[x,y]) (Prop 3.2).
    Returns the ratio  ( (ax+by | cx+dy) ) / ( (x|y) )  predicted by the action,
    i.e. the value v such that  kronecker(ax+by, cx+dy) == v * kronecker(x,y).
    The semigroup PRESERVES the symbol iff this returns +1 for the generator
    on all valid (x,y).  Mirrors the authors' code exactly (returns 1 for the
    'ignore' cases that violate the hypotheses)."""
    a, b = M[0]
    c, d = M[1]
    x = int(x); y = int(y)
    from math import gcd
    if gcd(x, d) > 1 or gcd(x, y) > 1 or a < 0 or b < 0 or c < 0 or d < 0:
        return 1  # ignore this case (same as paper.gp)
    A = ((oddpart(x) - 1) >> 1) % 2
    B = ((oddpart(d) - 1) >> 1) % 2
    cxpdy = c * x + d * y
    C = ((oddpart(cxpdy) - 1) >> 1) % 2
    D = ((oddpart(y) - 1) >> 1) % 2
    alpha = (A * B + A * C + B * C + A * D) % 2
    if valuation2(x) == 1 or valuation2(d) == 1:
        mu = kronecker(c * x * d * y + 1, 2)
    else:
        mu = 1
    if valuation2(cxpdy) == 1:
        mu = mu * kronecker(b * x * cxpdy + 1, 2)
    return (kronecker(a * x + b * y, cxpdy) * ((-1) ** alpha) * mu
            * kronecker(c, d) * kronecker(x, y))


def kron_action_verify(M, n_test=400, B=4000, seed=0):
    """Verify the Prop 3.2 IDENTITY holds for matrix M: kron_action(M,x,y)==+1 for all
    valid (x,y).  This is a theorem for every M in SL(2,Z)^{>=0}; we use it only to
    cross-check that our transcription of the formula is correct, NOT to test Psi
    membership.  Returns (True/False, witness)."""
    import random
    from math import gcd
    rng = random.Random(seed)
    pairs = [(x, y) for x in range(1, 40) for y in range(1, 40)]
    for _ in range(n_test):
        pairs.append((rng.randint(1, B), rng.randint(1, B)))
    d = M[1][1]
    for (x, y) in pairs:
        if gcd(x, d) != 1 or gcd(x, y) != 1 or y % 2 == 0:
            continue
        if kron_action(M, x, y) != 1:
            return (False, (M, x, y, kron_action(M, x, y)))
    return (True, None)


def preserves_symbol(gens, n_test=600, B=6000, seed=0):
    """Test whether the semigroup <gens>^+ PRESERVES the Kronecker symbol on orbit
    vectors -- i.e. whether each generator lies in the symbol-preserving semigroup
    Psi (Definition 2.1, Rickards-Stange).  Uses the DIRECT definition:
        (a x + b y | c x + d y) == (x | y)
    for every coprime (x,y) with y odd (and the image coprime).  This is exactly
    membership in Psi.  Returns (True/False, witness-or-None)."""
    import random
    from math import gcd
    rng = random.Random(seed)
    for M in gens:
        (a, b), (c, d) = M
        pairs = [(x, y) for x in range(1, 60) for y in range(1, 60)]
        for _ in range(n_test):
            pairs.append((rng.randint(1, B), rng.randint(1, B)))
        for (x, y) in pairs:
            if gcd(x, y) != 1 or y % 2 == 0:
                continue
            top = a * x + b * y
            bot = c * x + d * y
            if top <= 0 or bot <= 0 or gcd(top, bot) != 1:
                continue
            if kronecker(top, bot) != kronecker(x, y):
                return (False, (M, x, y, kronecker(top, bot), kronecker(x, y)))
    return (True, None)


def matvec(M, v):
    (a, b), (c, d) = M
    return (a * v[0] + b * v[1], c * v[0] + d * v[1])

def orbit_entries(gens, start, B, entry, max_nodes=4_000_000):
    """BFS the semigroup orbit <gens>^+ * start, collecting the `entry`-th coordinate
    (0=numerator/top, 1=denominator/bottom) of every orbit vector with that entry <= B.
    Returns the SET of values of that entry observed (exact ints)."""
    from collections import deque
    seen_vec = set()
    vals = set()
    dq = deque()
    dq.append(tuple(start))
    seen_vec.add(tuple(start))
    nodes = 0
    while dq:
        v = dq.popleft()
        nodes += 1
        if nodes > max_nodes:
            break
        if v[entry] <= B and v[entry] > 0:
            vals.add(v[entry])
        for M in gens:
            w = matvec(M, v)
            # prune: only expand if the tracked entry still within bound (entries are
            # nondecreasing under nonneg generators of det 1 acting on nonneg vectors,
            # so once both entries exceed B no descendant returns below B).
            if w[0] <= B and w[1] <= B and w not in seen_vec:
                seen_vec.add(w)
                dq.append(w)
    return vals

def has_square(vals):
    import math
    for v in vals:
        r = math.isqrt(v)
        if r * r == v:
            return True
    return False


# ----------------------------------------------------------------------------
# B.  Apollonian-curvature chi_2  (Def 4.3 of arXiv:2307.02749).
# ----------------------------------------------------------------------------

def apollonian_chi2(rho, n):
    """chi_2 for an Apollonian curvature n with quadratic-form residue rho (Def 4.3).
    rho = properly-represented invertible residue of the circle's quadratic form mod n,
    taken up to squares.  Exact Kronecker symbols."""
    n = int(n); rho = int(rho)
    r = n % 4
    if r == 0 or r == 1:
        return kronecker(rho, n)
    elif r == 2:
        return kronecker(-rho, n // 2)
    else:  # r == 3
        return kronecker(2 * rho, n)


def apollonian_curvatures(root, B):
    """Generate all curvatures <= B in the integral Apollonian packing with the given
    Descartes root quadruple `root` (a 4-tuple of ints).  Uses the Apollonian group
    (the four 'swap' generators S_i: replace curvature i via Descartes:
    a' = 2(b+c+d) - a ).  BFS over quadruples; collect all curvatures <= B."""
    from collections import deque
    root = tuple(sorted(root))
    seen = set()
    curv = set()
    dq = deque([root])
    seen.add(root)
    while dq:
        q = dq.popleft()
        for x in q:
            if 0 < x <= B:
                curv.add(x)
        a, b, c, d = q
        # four Descartes reflections
        for nq in (
            (2 * (b + c + d) - a, b, c, d),
            (a, 2 * (a + c + d) - b, c, d),
            (a, b, 2 * (a + b + d) - c, d),
            (a, b, c, 2 * (a + b + c) - d),
        ):
            # only keep growing within bound: expand if min positive curvature <= B
            pos = [v for v in nq if v > 0]
            if not pos:
                continue
            if min(v for v in nq if v > 0) <= B:
                t = tuple(sorted(nq))
                if t not in seen and max(nq) <= 4 * B:  # loose growth cap
                    seen.add(t)
                    dq.append(t)
    return curv


if __name__ == "__main__":
    print("self-tests: see reciprocity_oracle_test.py")
