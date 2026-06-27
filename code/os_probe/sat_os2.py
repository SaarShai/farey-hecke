#!/usr/bin/env python3
"""
SAT encoding v2 for OS(n) period-L existence, with SYMMETRY BREAKING.

Same core constraints as sat_os.py (validated against ground truth), plus
rotation symmetry breaking via a lex-leader constraint: the chosen bit string
b[0..L-1] must be lexicographically <= every cyclic rotation of itself.
This is SOUND for an existence/UNSAT decision because the OS(n) property is
invariant under cyclic rotation, so a solution exists iff a rotation-canonical
solution exists. (We do NOT add complement/reversal breaking by default since
those change the witness class subtly; rotation alone is the safe big win.)

Lex-leader (b <= rot^k(b) for all k) encoded with the standard chain of
"equal-so-far" auxiliary variables.
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


def add_lex_le(cnf, pool, xs, ys, tag):
    """Add clauses enforcing the bit-vector xs <= ys lexicographically.
    xs, ys are lists of literals (variables) of equal length, MSB first.
    Standard encoding with 'eq prefix' aux vars e_k = (xs[0..k-1]==ys[0..k-1]).
    Constraint at position k (given equal prefix): xs[k]=0 or ys[k]=1, i.e.
    (NOT eq_k) OR (NOT xs[k]) OR ys[k).
    eq_0 = True. eq_{k+1} = eq_k AND (xs[k]==ys[k]).
    """
    L = len(xs)
    # eq_k = "prefix positions 0..k-1 are all equal". eq_0 = True.
    eq = [pool.id((tag, 'eq', k)) for k in range(L + 1)]
    cnf.append([eq[0]])  # eq_0 = True
    for k in range(L):
        x, y, e, en = xs[k], ys[k], eq[k], eq[k + 1]
        # If prefix equal so far, require x <= y at this position:
        #   (NOT e) OR (NOT x) OR y
        cnf.append([-e, -x, y])
        # Define en = e AND (x == y).
        # (1) en -> e
        cnf.append([-en, e])
        # (2) en -> (x -> y)   and   en -> (y -> x)   [i.e. x==y]
        cnf.append([-en, -x, y])
        cnf.append([-en, x, -y])
        # (3) (e AND x AND y) -> en
        cnf.append([-e, -x, -y, en])
        # (4) (e AND ~x AND ~y) -> en
        cnf.append([-e, x, y, en])


def build(L, n, symbreak=True, verbose=False):
    pool = IDPool()
    cnf = CNF()

    def B(i):
        return pool.id(('b', i % L))

    def M(i, p):
        return pool.id(('m', i, p))

    def Y(p):
        return pool.id(('y', p))

    P = 1 << n
    patterns = range(P)

    for i in range(L):
        bits = [B(i + t) for t in range(n)]
        for p in patterns:
            m = M(i, p)
            lits = []
            for t in range(n):
                want1 = (p >> t) & 1
                lits.append(bits[t] if want1 else -bits[t])
            for lit in lits:
                cnf.append([-m, lit])
            cnf.append([m] + [-lit for lit in lits])

    for p in patterns:
        occ = [M(i, p) for i in range(L)]
        amo = CardEnc.atmost(lits=occ, bound=1, vpool=pool, encoding=EncType.seqcounter)
        cnf.extend(amo.clauses)
        y = Y(p)
        cnf.append([-y] + occ)
        for m in occ:
            cnf.append([-m, y])

    for p in patterns:
        r = reverse_pattern(p, n)
        if r == p:
            for i in range(L):
                cnf.append([-M(i, p)])
        elif p < r:
            cnf.append([-Y(p), -Y(r)])

    if symbreak:
        # rotation lex-leader: b <= rotation-by-k of b, for k=1..L-1
        base = [B(i) for i in range(L)]
        for k in range(1, L):
            rot = [B((i + k) % L) for i in range(L)]
            add_lex_le(cnf, pool, base, rot, tag=('rot', k))

    if verbose:
        print(f"  v2 L={L} n={n}: vars={pool.top}, clauses={len(cnf.clauses)}", file=sys.stderr)
    return cnf, pool, B


def solve(L, n, symbreak=True, verbose=True):
    cnf, pool, B = build(L, n, symbreak=symbreak, verbose=verbose)
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
    import argparse, time
    ap = argparse.ArgumentParser()
    ap.add_argument("L", type=int)
    ap.add_argument("-n", type=int, default=8)
    ap.add_argument("--nosym", action="store_true")
    args = ap.parse_args()
    t = time.time()
    sat, s = solve(args.L, args.n, symbreak=not args.nosym)
    dt = time.time() - t
    if sat:
        print(f"SAT  L={args.L}: {s}  ({dt:.1f}s)")
    else:
        print(f"UNSAT L={args.L}: no OS({args.n}) of period {args.L} ({dt:.1f}s)")
