#!/usr/bin/env python3
"""Bounded probe: Farey-order priority allocation vs dyadic vs WFQ.

Tests the ONE unrefuted lead from the silent-coordination corpus:
heterogeneous slot sizes with nested, non-disruptive growth.

Question: among ZERO-COMMUNICATION, NON-POSITION-DISRUPTIVE schemes,
does the Farey/Stern-Brocot palette approximate a priority-proportional
bandwidth target better than dyadic bisection? WFQ is the proportionality
ceiling (exact) but is disruptive (repartitions on every change).

Channel = circle [0,1), single shared TDMA frame. Each placed point owns
the arc to its next neighbor (its bandwidth share). Sum of arcs = 1.

Two sub-experiments:
  EXP1 (proportionality): static population of N weighted agents. Place by
    weight-rank into each scheme's deterministic enumeration; assign largest
    weight -> largest available arc (sorted, fair, identical procedure for
    all schemes). Measure how close actual shares are to ideal w_i/W.
  EXP2 (disruption): agents arrive 1..N; count how many existing points
    must MOVE (recompute position => needs comms) per join.

Honest design notes:
  - WFQ TV-error is 0 by construction (it IS the ideal). It is included to
    show the gap both approximators leave on the table, and to contrast on
    disruption (where it loses).
  - Min-arc is the drift proxy: smaller min gap => tighter clock-sync need.
"""
import numpy as np
from collections import deque

# ----------------------------------------------------------------------
# Deterministic enumerations (both BFS subdivision of [0,1), zero-comm)
# ----------------------------------------------------------------------

def stern_brocot_enum(K):
    """First K Farey/Stern-Brocot mediants in BFS order, as floats in (0,1).
    BFS over intervals starting (0/1, 1/1); yields 1/2, 1/3, 2/3, 1/4, ...
    Increasing denominators ~ decreasing gap sizes => natural priority order."""
    out = []
    q = deque()
    q.append(((0, 1), (1, 1)))
    while len(out) < K:
        (a, b), (c, d) = q.popleft()
        m_num, m_den = a + c, b + d  # mediant
        out.append(m_num / m_den)
        q.append(((a, b), (m_num, m_den)))
        q.append(((m_num, m_den), (c, d)))
    return np.array(out[:K])


def dyadic_enum(K):
    """First K dyadic rationals in van der Corput (BFS bisection) order:
    1/2, 1/4, 3/4, 1/8, 3/8, 5/8, 7/8, ...  Slot sizes are powers of 2."""
    out = []
    level = 1
    while len(out) < K:
        denom = 2 ** level
        for num in range(1, denom, 2):  # odd numerators are new at this level
            out.append(num / denom)
            if len(out) >= K:
                break
        level += 1
    return np.array(out[:K])


def arcs_of(points):
    """Circular arc lengths owned by each point (gap to next neighbor)."""
    p = np.sort(np.asarray(points))
    nxt = np.append(p[1:], p[0] + 1.0)
    return nxt - p  # sums to 1


# ----------------------------------------------------------------------
# Weight distributions
# ----------------------------------------------------------------------

def weights(dist, N, rng):
    if dist == "uniform":
        return np.ones(N)
    if dist == "two_class":          # 20% high (x10), 80% low (x1)
        w = np.ones(N)
        hi = max(1, N // 5)
        w[:hi] = 10.0
        return w
    if dist == "zipf":               # heavy tail, w_k ~ 1/rank
        return 1.0 / np.arange(1, N + 1)
    if dist == "lognormal":
        return rng.lognormal(mean=0.0, sigma=1.0, size=N)
    raise ValueError(dist)


# ----------------------------------------------------------------------
# EXP1: proportionality
# ----------------------------------------------------------------------

def exp1(schemes, dists, Ns, trials=40, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for dist in dists:
        for N in Ns:
            agg = {s: {"tv": [], "maxrel": [], "mingap": []} for s in schemes}
            for _ in range(trials):
                w = np.sort(weights(dist, N, rng))[::-1]      # desc
                ideal = w / w.sum()                            # target shares
                for s, enum in schemes.items():
                    arcs = np.sort(arcs_of(enum(N)))[::-1]     # desc
                    # fair assignment: largest weight -> largest arc
                    actual = arcs                              # already aligned desc
                    tv = 0.5 * np.abs(actual - ideal).sum()
                    maxrel = np.max(np.abs(actual - ideal) / ideal)
                    agg[s]["tv"].append(tv)
                    agg[s]["maxrel"].append(maxrel)
                    agg[s]["mingap"].append(arcs.min())
            for s in schemes:
                rows.append({
                    "dist": dist, "N": N, "scheme": s,
                    "tv": np.mean(agg[s]["tv"]),
                    "maxrel": np.mean(agg[s]["maxrel"]),
                    "mingap_x_uniform": np.mean(agg[s]["mingap"]) * N,  # vs 1/N
                })
    return rows


# ----------------------------------------------------------------------
# EXP2: position disruption on incremental join
# ----------------------------------------------------------------------

def exp2(Ns):
    """Count cumulative position MOVES as agents arrive 1..N.
    Farey/dyadic: newcomer takes next enumeration slot; existing points never
    move => 0 moves. WFQ: repartition into equal-or-weighted intervals every
    join => all t existing points shift => sum_{t} t moves."""
    rows = []
    for N in Ns:
        sb = stern_brocot_enum(N)
        dy = dyadic_enum(N)
        moves = {"farey": 0, "dyadic": 0, "wfq": 0}
        for t in range(1, N + 1):
            # nested schemes: prefix of length t-1 is unchanged subset of length t
            moves["farey"] += int(np.any(~np.isin(np.round(sb[:t-1], 12),
                                                  np.round(sb[:t], 12)))) * (t - 1)
            moves["dyadic"] += int(np.any(~np.isin(np.round(dy[:t-1], 12),
                                                   np.round(dy[:t], 12)))) * (t - 1)
            moves["wfq"] += (t - 1)  # every existing interval boundary moves
        rows.append({"N": N, **moves})
    return rows


def main():
    schemes = {"farey": stern_brocot_enum, "dyadic": dyadic_enum}
    dists = ["uniform", "two_class", "zipf", "lognormal"]
    Ns = [16, 50, 100, 200]

    print("=" * 78)
    print("EXP1: proportional-allocation error  (TV: lower=better; WFQ=0 ideal)")
    print("      mingap_x_uniform = min arc / (1/N)  (drift proxy; higher=better)")
    print("=" * 78)
    rows = exp1(schemes, dists, Ns)
    print(f"{'dist':<10}{'N':>5}{'scheme':>9}{'TV_err':>10}{'maxrel':>10}{'mingap_xU':>11}")
    for r in rows:
        print(f"{r['dist']:<10}{r['N']:>5}{r['scheme']:>9}"
              f"{r['tv']:>10.4f}{r['maxrel']:>10.2f}{r['mingap_x_uniform']:>11.3f}")

    # head-to-head summary: Farey TV / dyadic TV per (dist,N)
    print("\n" + "=" * 78)
    print("HEAD-TO-HEAD: TV_farey / TV_dyadic  (<1 => Farey better, >1 => dyadic better)")
    print("=" * 78)
    by = {}
    for r in rows:
        by[(r["dist"], r["N"], r["scheme"])] = r
    print(f"{'dist':<10}{'N':>5}{'TVf/TVd':>10}{'mingap_f':>10}{'mingap_d':>10}")
    for dist in dists:
        for N in Ns:
            f = by[(dist, N, "farey")]
            d = by[(dist, N, "dyadic")]
            ratio = f["tv"] / d["tv"] if d["tv"] > 1e-12 else float("inf")
            print(f"{dist:<10}{N:>5}{ratio:>10.3f}"
                  f"{f['mingap_x_uniform']:>10.3f}{d['mingap_x_uniform']:>10.3f}")

    print("\n" + "=" * 78)
    print("EXP2: cumulative position MOVES (recompute => needs comms). Lower=better")
    print("=" * 78)
    d2 = exp2(Ns)
    print(f"{'N':>5}{'farey':>10}{'dyadic':>10}{'wfq':>12}")
    for r in d2:
        print(f"{r['N']:>5}{r['farey']:>10}{r['dyadic']:>10}{r['wfq']:>12}")


if __name__ == "__main__":
    main()
