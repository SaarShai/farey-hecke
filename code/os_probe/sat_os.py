#!/usr/bin/env python3
"""
SAT encoding for: does a cyclic binary ORIENTABLE sequence OS(n) of period L exist?

Cyclic sequence b_0..b_{L-1} (indices mod L). Window_i = b_i b_{i+1} ... b_{i+n-1}.
OS(n) constraint: the 2L strings { window_i, reverse(window_i) : i } are all distinct.

Equivalent "pattern-occupancy" encoding (the clean one):
For each 8-bit pattern p in {0..2^n-1}, position i "realizes" p iff window_i == p.
Constraints:
  (A) at each position exactly one pattern is realized (defining clauses linking
      window bits to pattern indicator). We use the bit variables directly and
      derive pattern-match indicators.
  (B) Each pattern p is realized by AT MOST ONE position (forward distinct).
  (C) For each pattern p, NOT (p realized somewhere AND reverse(p) realized
      somewhere)  -- unless p == reverse(p) (palindrome), which must be realized
      by NO position at all.

We implement via pattern indicator vars y_{p} = "pattern p occurs at least once"
plus per-position-pattern match vars. Simpler & tight: use occurrence-count
encoding.

Variables:
  bit b_i           (i in 0..L-1)
  match m_{i,p}     = window at i equals pattern p   (i in 0..L-1, p in patterns)
Clauses:
  m_{i,p} <-> AND_{t} (b_{i+t} == bit t of p)        (channeling)
  for each p:  at-most-one over { m_{i,p} : i }        (forward distinct, B)
  pair (p, rev(p)) with p < rev(p):
        not ( (OR_i m_{i,p}) and (OR_i m_{i,rev(p)}) )  (C)
  p palindrome (p==rev(p)):  all m_{i,p} = 0           (no palindromic window)

To keep clause count manageable we only instantiate m_{i,p} for p that *could*
match (all p). L up to ~96, patterns 256, so ~96*256 ~ 24k match vars. Fine.

Optionally fix a symmetry-breaking prefix.
"""
import sys
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195


def reverse_pattern(p, n):
    r = 0
    for t in range(n):
        if (p >> t) & 1:
            r |= 1 << (n - 1 - t)
    return r


def build(L, n, fix_prefix=None, verbose=False):
    pool = IDPool()
    cnf = CNF()

    def B(i):
        return pool.id(('b', i % L))

    def M(i, p):
        return pool.id(('m', i, p))

    P = 1 << n
    patterns = range(P)

    # channeling: m_{i,p} <-> AND_t lit(b_{i+t}, bit_t(p))
    # We need m vars only where useful: all p.
    # m -> each literal ; and (all literals) -> m
    for i in range(L):
        bits = [B(i + t) for t in range(n)]
        for p in patterns:
            m = M(i, p)
            lits = []
            for t in range(n):
                want1 = (p >> t) & 1
                lits.append(bits[t] if want1 else -bits[t])
            # m -> lits
            for lit in lits:
                cnf.append([-m, lit])
            # lits -> m   :  (NOT all lits) OR m  == clause [m, -lit1, -lit2, ...] with negated lits
            cnf.append([m] + [-lit for lit in lits])

    # (B) forward distinct: at most one position per pattern p
    for p in patterns:
        occ = [M(i, p) for i in range(L)]
        # at-most-one
        amo = CardEnc.atmost(lits=occ, bound=1, vpool=pool, encoding=EncType.seqcounter)
        cnf.extend(amo.clauses)

    # occurrence indicator y_p = OR_i m_{i,p}
    def Y(p):
        return pool.id(('y', p))
    for p in patterns:
        y = Y(p)
        occ = [M(i, p) for i in range(L)]
        # y -> OR occ
        cnf.append([-y] + occ)
        # each occ -> y
        for m in occ:
            cnf.append([-m, y])

    # (C) reverse / palindrome
    for p in patterns:
        r = reverse_pattern(p, n)
        if r == p:
            # palindrome: forbid entirely
            for i in range(L):
                cnf.append([-M(i, p)])
        elif p < r:
            # not (y_p and y_r)
            cnf.append([-Y(p), -Y(r)])

    # symmetry breaking: optional prefix fix
    if fix_prefix:
        for i, ch in enumerate(fix_prefix):
            cnf.append([B(i) if ch == '1' else -B(i)])

    if verbose:
        print(f"  L={L} n={n}: vars={pool.top}, clauses={len(cnf.clauses)}", file=sys.stderr)
    return cnf, pool, B


def solve(L, n, fix_prefix=None, timeout=None, verbose=True):
    cnf, pool, B = build(L, n, fix_prefix=fix_prefix, verbose=verbose)
    solver = Cadical195(bootstrap_with=cnf.clauses)
    sat = solver.solve()
    if sat:
        model = set(l for l in solver.get_model() if l > 0)
        s = ''.join('1' if pool.id(('b', i)) in model else '0' for i in range(L))
        solver.delete()
        return True, s
    solver.delete()
    return False, None


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("L", type=int)
    ap.add_argument("-n", type=int, default=8)
    ap.add_argument("--prefix", default=None)
    args = ap.parse_args()
    sat, s = solve(args.L, args.n, fix_prefix=args.prefix)
    if sat:
        print(f"SAT  L={args.L}: {s}")
    else:
        print(f"UNSAT L={args.L}: no OS({args.n}) of period {args.L} exists")
