#!/usr/bin/env python3
"""
chi4_packing.py -- compute chi_2 and chi_4 on an actual Apollonian packing via the
tangency structure, following arXiv:2307.02749 Sec 4-5.

chi_2 (Def 4.3 simplest form, Thm 1.6 / Prop 4.4):
   For tangent coprime curvatures a,b: rho = a+b, chi_2(C)=Kronecker(rho, n) appropriately.
   We use the propagation form: pick a base circle, define chi_2 via a coprime tangent neighbor.

chi_4 (Def 5.6 + Prop 5.8/5.9): for tangent circles C1,C2 of coprime curvatures n1,n2
   there exists beta in Z[i] with N(beta)=n1+n2 valid for BOTH; then
       chi_4(C) = (Def 5.6 formula in beta and n).
   Prop 5.9: chi_4(C1)=chi_4(C2).  Defined only for type (6,1)/(6,17) (n==0,1,4 mod 8).

We compute chi_4(A) by:
  1. find a tangent coprime pair (n1,n2) in the packing with n1,n2 ODD and == 1 mod 8 (cleanest case),
  2. beta = a Gaussian integer with a^2+b^2 = n1+n2 (sum of two squares), primary,
  3. apply Def 5.6 (n==1 mod 8 branch: chi_4 = [beta/n]),
  4. verify chi_4 is CONSTANT by recomputing on several distinct tangent pairs.
"""
import sys
from collections import deque
from math import gcd
sys.path.insert(0, '/Users/za/Documents/farey-hecke/code')
from chi4_oracle import (
    gnorm, gmul, ggcd, is_odd, is_primary, make_primary, quartic_symbol_int_denom,
    UNITS, kronecker,
)

def sum_of_two_squares(m):
    """Return list of (a,b) with a^2+b^2=m, a,b integers, gcd-various reps.
    Returns ALL primitive-ish reps with a>=0,b>=0 then we adjust signs/associates."""
    import math
    reps = []
    r = math.isqrt(m)
    for a in range(0, r + 1):
        b2 = m - a * a
        b = math.isqrt(b2)
        if b * b == b2:
            reps.append((a, b))
    return reps

def beta_for_sum(n1, n2):
    """Find a primary Gaussian integer beta with N(beta)=n1+n2.
    Returns the primary associate. Requires n1+n2 expressible as sum of two squares
    with the resulting beta ODD (N odd) -- true when n1,n2 odd => n1+n2 even =2*odd,
    so beta=(1+i)*beta' ; we then use beta' (odd) for the odd-curvature formula as in Prop 5.9.
    For the cleanest n1==n2==1 mod 8 case we instead seek a DIRECT odd beta is impossible
    (N even); we follow Prop 5.9: beta=(1+i)beta', and chi_4(C1)=[beta'/n1] up to the i^((n1-1)/4) factor.

    To keep the oracle simple and rigorous we instead compute chi_4 via Def 5.6 directly using
    a beta with N(beta)=n where n is the curvature and beta in the lattice Lambda_C.  But the
    lattice is only available through tangency.  The robust, paper-faithful route used here:
    compute chi_4 for an ODD curvature n1 using a tangent EVEN coprime curvature n2 so that
    N(beta)=n1+n2 is ODD => beta itself is odd, primary, and Def 5.6 (n1==1 mod8) gives
    chi_4(C1)=[beta/n1] directly (no (1+i) factor).  This is exactly the n2-even branch of Prop 5.9.
    """
    s = n1 + n2
    for (a, b) in sum_of_two_squares(s):
        for (sa, sb) in [(a, b), (a, -b), (b, a), (b, -a)]:
            beta = (sa, sb)
            if gnorm(beta) == s and is_odd(beta):
                bp, _ = make_primary(beta)
                return bp
    return None

def apollonian_quadruples(root, B, max_nodes=2_000_000):
    """BFS Descartes quadruples; yield quadruples with all |curv|<=B-ish.
    Returns list of quadruples (tuples) reachable."""
    root = tuple(root)
    seen = set()
    out = []
    dq = deque([root])
    seen.add(tuple(sorted(root)))
    nodes = 0
    while dq and nodes < max_nodes:
        q = dq.popleft()
        nodes += 1
        out.append(q)
        a, b, c, d = q
        for nq in (
            (2 * (b + c + d) - a, b, c, d),
            (a, 2 * (a + c + d) - b, c, d),
            (a, b, 2 * (a + b + d) - c, d),
            (a, b, c, 2 * (a + b + c) - d),
        ):
            if min(nq) < -B:
                continue
            pos = [v for v in nq if v > 0]
            if pos and min(pos) <= B and max(nq) <= 3 * B:
                key = tuple(sorted(nq))
                if key not in seen:
                    seen.add(key)
                    dq.append(nq)
    return out

def find_tangent_coprime_pairs(root, B, want=30, parity=None):
    """Find tangent coprime curvature pairs (n1,n2) in the packing.
    In a Descartes quadruple all 4 circles are mutually tangent, so any two entries
    of a quadruple are tangent.  parity: optional filter ('oe'=one odd one even, etc.)."""
    quads = apollonian_quadruples(root, B)
    pairs = set()
    for q in quads:
        for i in range(4):
            for j in range(i + 1, 4):
                a, b = q[i], q[j]
                if a > 0 and b > 0 and gcd(a, b) == 1 and a <= B and b <= B:
                    n1, n2 = sorted((a, b))
                    if parity == 'oe':
                        if (n1 % 2) + (n2 % 2) != 1:
                            continue
                    pairs.add((n1, n2))
                    if len(pairs) >= want * 5:
                        break
    return sorted(pairs)

def chi4_of_odd_circle(n1, n2):
    """chi_4 of the circle of ODD curvature n1, using tangent coprime EVEN curvature n2.
    Def 5.6 (n1 == 1 mod 8): chi_4 = [beta / n1], beta primary, N(beta)=n1+n2.
    Returns exponent k mod 4 (value i^k), or None."""
    assert n1 % 2 == 1
    assert n2 % 2 == 0
    assert gcd(n1, n2) == 1
    if n1 % 8 != 1:
        return ('SKIP', f"n1={n1} not 1 mod 8")
    s = n1 + n2  # odd
    beta = beta_for_sum(n1, n2)
    if beta is None:
        return ('NOBETA', s)
    k = quartic_symbol_int_denom(beta, n1)
    return k

def chi2_of_circle(n1, n2):
    """chi_2 via Def 4.3-style: rho = n1+n2 (a properly-represented value), chi_2=Kronecker form.
    For n==1 mod 4: chi_2=(rho|n)."""
    rho = n1 + n2
    r = n1 % 4
    if r in (0, 1):
        return kronecker(rho, n1)
    elif r == 2:
        return kronecker(-rho, n1 // 2)
    else:
        return kronecker(2 * rho, n1)

def compute_packing_chi4(root, B=4000, label=""):
    """Compute chi_4(A) for a type-(6,1)/(6,17) packing; verify constancy."""
    pairs_oe = find_tangent_coprime_pairs(root, B, parity='oe')
    # restrict to ones where the odd one is 1 mod 8 (type (6,1) all odd are 1 mod 8)
    results = {}
    chi2results = {}
    for (a, b) in pairs_oe:
        if a % 2 == 1:
            nodd, neven = a, b
        else:
            nodd, neven = b, a
        if nodd % 8 != 1:
            continue
        k = chi4_of_odd_circle(nodd, neven)
        if isinstance(k, tuple):
            continue
        results[(nodd, neven)] = k
        chi2results[(nodd, neven)] = chi2_of_circle(nodd, neven)
        if len(results) >= 60:
            break
    vals = set(results.values())
    chi2vals = set(chi2results.values())
    print(f"=== {label}  root={root} ===")
    print(f"  tangent odd(==1mod8)/even coprime pairs tested: {len(results)}")
    print(f"  chi_4 values observed (exponent k, value i^k): {sorted(vals)} -> {[UNITS[v] for v in sorted(vals)]}")
    print(f"  chi_2 values observed: {sorted(chi2vals)}")
    # constancy
    const4 = (len(vals) == 1)
    const2 = (len(chi2vals) == 1)
    print(f"  chi_4 CONSTANT across packing: {const4}")
    print(f"  chi_2 CONSTANT across packing: {const2}")
    if const4:
        k = next(iter(vals))
        print(f"  chi_4(A) = i^{k} = {UNITS[k]}  (1=+1, (0,1)=i, (-1,0)=-1, (0,-1)=-i)")
        # chi_4^2 == chi_2 ?
        chi4sq = (-1) ** k
        if const2:
            chi2 = next(iter(chi2vals))
            print(f"  CHECK Prop 5.12: chi_4^2 = {chi4sq}, chi_2 = {chi2}, match={chi4sq==chi2}")
    # sample table
    print("  sample (nodd, neven) -> chi_4 exp, chi_2:")
    for kp in list(results.keys())[:8]:
        print(f"     {kp} -> i^{results[kp]} , chi2={chi2results[kp]}")
    print()
    return vals, chi2vals


if __name__ == "__main__":
    # strip packing = type (6,1,1,1), chi_4 IS defined here
    compute_packing_chi4((0, 0, 1, 1), B=6000, label="STRIP (6,1,1,1) OPEN")

    # sanity controls: type (6,1) packings with KNOWN chi_4 obstructions from Prop 5.11.
    # (6,1,1,-1) packing (-8,12,25,25): table says n^4,4n^4,9n^4,36n^4 quartic obstruction
    #   => chi_4(A) in {-1,i,-i} (NOT +1). Use as a POSITIVE control (chi_4 != 1).
    compute_packing_chi4((-8, 12, 25, 25), B=6000, label="CONTROL (6,1,1,-1) has quartic obstr")
