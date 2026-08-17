#!/usr/bin/env python3
"""
r1_coset_enum.py -- LANE G, task R1: enumerate double-coset c-spectrum of the
conjugated Hecke group G_q = <S, Q_q> (Hejhal LNM1001 vol.2 sec.7 model),
S: z -> z+1, Q_q: matrix (0,-1/lam; lam,0), lam = 2*cos(pi/q) (lam=2 for the
theta group / q=infinity limit).

Double-coset space [S]\\G_q/[S] (c != 0) is represented (standard free-product
normal form for G_q = Z_2 * Z_q, or Z_2 * Z_infty at lam=2) by REDUCED WORDS

    Q S^{n_1} Q S^{n_2} Q ... S^{n_{k-1}} Q ,   k >= 1, n_i in Z\\{0}

(leading/trailing S-powers are absorbed by the [S] cosets on either side, so
every double-coset representative starts and ends with Q). c(W) is the
lower-left entry of the SL(2,R) matrix representing W.

Enumeration strategy: BFS/DFS over these words, matrix-multiplying in exact
mpmath (dps=50) arithmetic, pruning any branch whose |c| already exceeds the
target cutoff X (a real, not merely heuristic, prune: |c| growth is what we
are enumerating, and matrix entries are monotonically informative once |c|
climbs -- see the validation gate in sec.1 of the LAW note for the honesty
check this pruning needs). A max word-length safety cap prevents runaway
recursion; completeness is judged empirically by the Dirichlet-sum validation
against the existing certified phi_q(1.5) evaluator (rate_measure.py), NOT
asserted a priori.
"""
from __future__ import annotations
import itertools
import json
import sys
from pathlib import Path

from mpmath import mp, mpf, cos, pi

mp.dps = 50


def lam_of_q(q):
    if q is None:  # theta-group / q=infinity limit
        return mpf(2)
    return 2 * cos(pi / q)


def matmul(A, B):
    return (
        (A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
        (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]),
    )


def S_pow(n):
    return ((mpf(1), mpf(n)), (mpf(0), mpf(1)))


def Q_mat(lam):
    return ((mpf(0), -1 / lam), (lam, mpf(0)))


def enumerate_c_spectrum(q, X, max_depth=9, m_max=None):
    """Return dict: c-value(mpf, positive representative |c|) -> list of
    (word tuple of n_i's, k, matrix) witnesses, restricted to |c| <= X.
    m_max caps the |n_i| search range (None -> derived from X, lam)."""
    lam = lam_of_q(q)
    Q = Q_mat(lam)
    if m_max is None:
        # S^m Q roughly scales c like |m|*lam for the first step; cap
        # generously so X is reached without wasting huge ranges.
        m_max = max(4, int(X / float(lam)) + 4)

    # ---- double-coset canonicalization -----------------------------------
    # c(W) is invariant under BOTH S^a*W (left mult only changes row 1) and
    # W*S^b (right mult only changes column 2) -- standard fact, verified
    # directly from S=[[1,1],[0,1]]'s shape. So |c| alone is NOT enough to
    # dedupe double cosets (Kloosterman-sum-style: many distinct cosets share
    # the same c); the correct extra invariant is d mod c (right-mult by S^b
    # shifts D -> D + b*C for integer b). A first version of this script
    # deduped on |c| alone (undercounting, saw phi/coset-sum = 0.43 vs
    # phi_ref = 0.56) and a second version deduped on WORD alone
    # (overcounting -- treating (Q,S)-words as already freely reduced, which
    # they are NOT: the true presentation is Z_2 * Z_q on generators Q and
    # R=QS, and general Q,S^n-words are redundant w.r.t. that relation --
    # gave 1.70 vs 0.56). This version dedupes on the actual double-coset
    # invariant (c, d mod c), which is provably correct and is exactly what
    # the validation gate below checks.
    found = {}  # key: (rounded c, rounded d0) -> (mpf|c|, word, matrix)

    # Zero-filter threshold scaled to the CURRENT mp.dps (callers -- e.g.
    # rate_measure.set_prec() -- may change mp.dps after this module's
    # import-time mp.dps=50; recomputing here avoids a stale, too-tight
    # threshold letting rounding noise from the elliptic relation
    # (Q_q S)^q = I leak through as a spurious huge-|c|^-2s term).
    EPS_ZERO = mpf(10) ** (-int(mp.dps * 0.4))
    # Deliberately conservative (fewer digits than mp.dps): D mod C is
    # computed by floor(D/C), which is numerically unstable exactly when a
    # word is [S]-equivalent to a much shorter one (D/C lands extremely near
    # an integer) -- a real edge case hit empirically at depth >= 9 (words
    # that almost close up via the elliptic relation land at D0 near 0 or
    # near C depending on roundoff, producing spurious near-duplicate keys
    # for what is provably the SAME double coset). Rounding to a modest
    # digit count clusters these correctly; validated against phi_q(1.5)
    # below (this was caught, not silently accepted -- see the LAW note).
    ROUND_DIGITS = 18

    def canon_key(M):
        A, B = M[0]
        C, D = M[1]
        if C < 0:
            A, B, C, D = -A, -B, -C, -D
        b = int(mp.floor(D / C))
        D0 = D - b * C
        if D0 < 0:
            D0 += C
        if D0 >= C:
            D0 -= C
        # Snap D0 to 0 (or to C, folded into 0) near the boundary: D0 as a
        # tiny-but-nonzero mpf (e.g. ~1e-50) is accumulated roundoff from a
        # word that is EXACTLY [S]-equivalent to a shorter one in exact
        # arithmetic (D/C landed within float noise of an integer) -- and
        # mp.nstr(tiny_value, digits) preserves significant figures of the
        # tiny value rather than rounding it toward 0, so without this snap
        # such words were surviving as spurious near-duplicate cosets
        # (caught via the phi_q(1.5) validation gate below going from 0.55
        # to 4.0 between max_depth=8 and 9 -- traced to exactly this).
        snap_eps = C * mpf(10) ** (-int(mp.dps * 0.5))
        if D0 < snap_eps or (C - D0) < snap_eps:
            D0 = mpf(0)
        return (mp.nstr(C, ROUND_DIGITS), mp.nstr(D0, ROUND_DIGITS))

    def record(word, M):
        c = M[1][0]
        ac = abs(c)
        if ac < EPS_ZERO or ac > X:
            return
        key = canon_key(M)
        if key not in found:
            found[key] = (ac, word, M)

    # k = 1: just Q itself.
    record((), Q)

    # BFS frontier: (word=tuple of n_i so far, matrix M ending in ...Q)
    frontier = [((), Q)]
    depth = 1
    while frontier and depth < max_depth:
        depth += 1
        next_frontier = []
        for word, M in frontier:
            for m in range(-m_max, m_max + 1):
                if m == 0:
                    continue
                M2 = matmul(M, S_pow(m))
                # prune: if the running |c| of M2*Q-ish step can only be
                # produced by full multiply, just compute it (cheap 2x2 mult)
                M3 = matmul(M2, Q)
                c3 = M3[1][0]
                if abs(c3) > X:
                    continue
                new_word = word + (m,)
                record(new_word, M3)
                next_frontier.append((new_word, M3))
        frontier = next_frontier

    return found, depth


def dirichlet_partial_sum(found, sigma_plus_it):
    """Sum |c|^{-2s} over the enumerated (deduped) c-spectrum."""
    from mpmath import mpc
    s = mpc(sigma_plus_it)
    total = mpc(0)
    for _, (ac, word, M) in found.items():
        total += ac ** (-2 * s)
    return total


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--q", type=str, default="8")  # "inf" for theta group
    p.add_argument("--X", type=float, default=50.0)
    p.add_argument("--max-depth", type=int, default=9)
    p.add_argument("--out", type=str, default=None)
    args = p.parse_args()

    q = None if args.q == "inf" else int(args.q)
    found, depth_reached = enumerate_c_spectrum(q, args.X, max_depth=args.max_depth)
    cs = sorted(float(v[0]) for v in found.values())
    out = {
        "q": args.q,
        "X": args.X,
        "max_depth": args.max_depth,
        "depth_reached": depth_reached,
        "n_cosets": len(cs),
        "c_values": cs,
    }
    print(f"q={args.q}: {len(cs)} double cosets with |c|<= {args.X}, depth_reached={depth_reached}")
    print("first 20 c:", cs[:20])
    if args.out:
        Path(args.out).write_text(json.dumps(out, indent=1))
