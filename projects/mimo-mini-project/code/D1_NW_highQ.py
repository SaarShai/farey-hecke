"""
D1 high-Q push: extend N·W(N) computation to Q=300k and Q=1M
with very large m_factor for sharper constant identification.

Also: an analytical check on the m-truncation tail. Estimate the
remainder Σ_{m > M} A_Q(m)²/m² and report.
"""

import sys
import math
import time
sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")

from J_mikolas import sieve_mobius_totient, cumsum


def J_mikolas_optimized(Q: int, m_factor: float = 100.0) -> dict:
    """Like J_mikolas but uses numpy where helpful for speed."""
    t0 = time.time()
    mu, phi = sieve_mobius_totient(Q)
    M = cumsum(mu)
    Phi = cumsum(phi)
    sieve_t = time.time() - t0

    m_max = int(m_factor * Q)
    t0 = time.time()
    A = [0] * (m_max + 1)
    # Iterate divisor d, add d·M[Q//d] to all multiples
    for d in range(1, Q + 1):
        contribution = d * M[Q // d]
        if contribution == 0:
            continue
        for m in range(d, m_max + 1, d):
            A[m] += contribution
    # For d > Q, M[Q//d] = M[0] = 0, so no contribution. Skip.
    A_t = time.time() - t0

    t0 = time.time()
    s = 0.0
    # Also track tail behavior
    cum_running = []
    for m in range(1, m_max + 1):
        s += (A[m] / m) ** 2
        if m in [Q, 2 * Q, 5 * Q, 10 * Q, 50 * Q, 100 * Q]:
            cum_running.append((m, s))
    J = s / (2 * math.pi ** 2)
    sum_t = time.time() - t0

    Phi_N = Phi[Q]
    NW = Q * J / Phi_N
    return {
        "Q": Q,
        "m_max": m_max,
        "J": J,
        "Phi_N": Phi_N,
        "NW": NW,
        "cum_running": cum_running,
        "timings": {"sieve": sieve_t, "A": A_t, "sum": sum_t},
    }


def main():
    print(f"{'Q':>8} {'m_factor':>10} {'m_max':>10} {'J':>14} {'NW':>12} {'wall(s)':>8}")
    for Q, m_factor in [
        (100_000, 50),
        (200_000, 30),
        (500_000, 15),
    ]:
        t0 = time.time()
        res = J_mikolas_optimized(Q, m_factor=m_factor)
        wall = time.time() - t0
        print(f"{Q:>8} {m_factor:>10} {res['m_max']:>10} {res['J']:>14.6f} {res['NW']:>12.7f} {wall:>8.1f}")
        # Show running cumsum at checkpoint m values
        print(f"  Convergence: ", end="")
        prev_NW = None
        for m, cum in res["cum_running"]:
            J_so_far = cum / (2 * math.pi ** 2)
            NW_so_far = Q * J_so_far / res["Phi_N"]
            ratio = (NW_so_far / prev_NW) if prev_NW else 1.0
            print(f"  m={m}: NW={NW_so_far:.7f}", end="")
            prev_NW = NW_so_far
        print()


if __name__ == "__main__":
    main()
