"""
Function-field Rubinstein-Sarnak-style density.

For (q, M) and a pair (b, a) of units, define:

  delta(b, a; N) := #{n in {1,...,N} : pi(q^n; M, b) > pi(q^n; M, a)} / N

where pi(q^n; M, A) = #{P monic irreducible, deg P <= n, P = A (mod M)}.

We compute this UNWEIGHTED count (closer to R-S who use the prime-counting
function, not pi_{1/2}); and also the pi_{1/2} version for comparison.

Also: log-density on x = q^n: the natural change-of-variables makes dx/x =
log(q) * dn, so density on n-axis IS the log-density on x-axis up to a
constant factor (which is 1 if we sum over integers n; for a continuous
analog one'd integrate). We report density on n.
"""

import json
import math
import sys

from fq_poly import (
    f2_monic_polys_of_degree, f2_mod, f2_deg,
    fq_monic_polys_of_degree, fq_mod, fq_deg,
)


def recompute_unweighted_f2(M_packed, N, irr_by_deg, units):
    """Given precomputed list-of-list irr_by_deg, compute UNWEIGHTED pi(q^n;M,A)."""
    pi_class = {u: [0] * (N + 1) for u in units}
    for d in range(1, N + 1):
        for P in irr_by_deg[d]:
            r = f2_mod(P, M_packed)
            if r in pi_class:
                pi_class[r][d] += 1
        for u in units:
            pi_class[u][d] += pi_class[u][d - 1]
    return pi_class


def rs_density(pi_class, units, sqs, N, n_start=1):
    """Compute pairwise RS density on n in [n_start, N]."""
    sqs = set(sqs)
    result = []
    for b in units:
        for a in units:
            if a == b: continue
            denom = N - n_start + 1
            wins = 0
            ties = 0
            for n in range(n_start, N + 1):
                if pi_class[b][n] > pi_class[a][n]:
                    wins += 1
                elif pi_class[b][n] == pi_class[a][n]:
                    ties += 1
            delta = wins / denom
            tag = ""
            if a in sqs and b not in sqs:
                tag = "non-QR vs QR (bias-predicted)"
            elif b in sqs and a not in sqs:
                tag = "QR vs non-QR"
            result.append((b, a, delta, wins, ties, denom, tag))
    return result


# --- Use cached sieve from compute.py outputs (which only store pi_{1/2}, not the prime lists)
# --- For RS density we need raw counts; we recompute from scratch.

def main_ex36():
    from compute import f2_sieve_irreducibles_by_degree, f2_units_mod_M, f2_squares_mod_M
    N = 22
    M = 4  # T^2
    units = f2_units_mod_M(M)
    sqs = f2_squares_mod_M(M)
    print(f"q=2, M=T^2, units={units}, squares={sqs}")
    print("Sieving (cached)...", flush=True)
    irr_by_deg = f2_sieve_irreducibles_by_degree(N)
    pi_class = recompute_unweighted_f2(M, N, irr_by_deg, units)

    print("\nUnweighted pi(q^n; M, A) by n:")
    print("n   pi(.;M,1)  pi(.;M,T+1)   diff   sign")
    for n in range(1, N + 1):
        c1 = pi_class[1][n]
        c3 = pi_class[3][n]
        sign = "+" if c3 > c1 else ("0" if c3 == c1 else "-")
        print(f"{n:2d}  {c1:8d}   {c3:8d}   {c3-c1:+5d}   {sign}")

    res = rs_density(pi_class, units, sqs, N, n_start=1)
    print("\nRubinstein-Sarnak density delta(b, a) = #{n: pi(q^n;M,b) > pi(q^n;M,a)} / N")
    for b, a, delta, wins, ties, denom, tag in res:
        print(f"  delta(b={b}, a={a}) = {delta:.4f}  ({wins}/{denom}, ties={ties})  {tag}")

    # Also report log-density: ∑_{n=1}^N (log q) / (log(q^n)) * 1_{...} normalized
    # Standard R-S uses ∫ dx/(x log x) -> for x = q^n, dx/x = log(q) dn,
    # so dx/(x log x) = dn/n. That's a "harmonic mean" weighting.
    print("\nHarmonic-weighted density delta_log(b, a) = sum_{n: pi(b) > pi(a)} (1/n) / sum_{n=1..N} (1/n):")
    H = sum(1/n for n in range(1, N+1))
    for b in units:
        for a in units:
            if a == b: continue
            num = sum(1/n for n in range(1, N+1) if pi_class[b][n] > pi_class[a][n])
            print(f"  delta_log(b={b}, a={a}) = {num/H:.4f}  (numer/H = {num:.4f}/{H:.4f})")


if __name__ == "__main__":
    main_ex36()
