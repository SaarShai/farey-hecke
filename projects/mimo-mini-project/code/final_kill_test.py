#!/usr/bin/env python3
"""Final kill-test for the priority-nesting lead.

Probe 1 showed Farey beats vanilla base-2 dyadic on heavy-tailed priority
allocation. Two ways that result could still collapse:

Q1 (universal frontier): is the Farey STRUCTURE special, or does any finer
    universal nested palette (higher-radix van der Corput) match it? If some
    design-free radix matches Farey's TV with a larger min-gap, Farey is not
    special -- "just use a fine nested palette."

Q2 (target-matched oracle): if you KNOW the priority distribution at design
    time, a fixed partition at the cumulative target shares gives TV=0 and
    min-gap = exactly the smallest target share (>= what any proportional
    scheme needs). That dominates Farey ON ACCURACY AND DRIFT -- *if* the
    final population/target is known. Its cost: it is a fixed partition for
    the final size, so when underpopulated it wastes bandwidth (the not-yet-
    arrived agents' slots sit idle). Farey, being full-subdivision, uses 100%
    of bandwidth at every population size. We quantify that cost.

Model identical to probe 1: circle [0,1), point owns arc to next neighbor.
"""
import numpy as np
from collections import deque


def stern_brocot_enum(K):
    out, q = [], deque([((0, 1), (1, 1))])
    while len(out) < K:
        (a, b), (c, d) = q.popleft()
        mn, md = a + c, b + d
        out.append(mn / md)
        q.append(((a, b), (mn, md)))
        q.append(((mn, md), (c, d)))
    return np.array(out[:K])


def vdc_enum(K, base):
    """van der Corput base-`base`, graded order (level by level)."""
    out, n = [], 1
    while len(out) < K:
        # radical inverse of n in `base`
        x, b, i = 0.0, 1.0 / base, n
        while i > 0:
            x += (i % base) * b
            i //= base
            b /= base
        out.append(x)
        n += 1
    return np.array(out[:K])


def arcs_of(points):
    p = np.sort(np.asarray(points))
    nxt = np.append(p[1:], p[0] + 1.0)
    return nxt - p


def weights(dist, N, rng):
    if dist == "uniform":
        return np.ones(N)
    if dist == "two_class":
        w = np.ones(N); w[:max(1, N // 5)] = 10.0; return w
    if dist == "zipf":
        return 1.0 / np.arange(1, N + 1)
    if dist == "lognormal":
        return rng.lognormal(0.0, 1.0, N)
    raise ValueError(dist)


# ----------------------------------------------------------------------
# Q1: universal design-free frontier  (Farey vs radix-2/3/5 vdC)
# ----------------------------------------------------------------------

def q1(dists, Ns, trials=40, seed=1):
    rng = np.random.default_rng(seed)
    schemes = {
        "farey":   lambda K: stern_brocot_enum(K),
        "dyadic2": lambda K: vdc_enum(K, 2),
        "vdc3":    lambda K: vdc_enum(K, 3),
        "vdc5":    lambda K: vdc_enum(K, 5),
    }
    print("=" * 84)
    print("Q1: universal nested palettes (design-free). TV lower=better; mingap_xU higher=better")
    print("=" * 84)
    print(f"{'dist':<10}{'N':>5}{'scheme':>9}{'TV':>9}{'maxrel':>9}{'mingap_xU':>11}")
    for dist in dists:
        for N in Ns:
            for s, enum in schemes.items():
                tv, mr, mg = [], [], []
                for _ in range(trials):
                    w = np.sort(weights(dist, N, rng))[::-1]
                    ideal = w / w.sum()
                    arcs = np.sort(arcs_of(enum(N)))[::-1]
                    tv.append(0.5 * np.abs(arcs - ideal).sum())
                    mr.append(np.max(np.abs(arcs - ideal) / ideal))
                    mg.append(arcs.min() * N)
                print(f"{dist:<10}{N:>5}{s:>9}{np.mean(tv):>9.4f}"
                      f"{np.mean(mr):>9.2f}{np.mean(mg):>11.3f}")
            print()


# ----------------------------------------------------------------------
# Q2: target-matched oracle  -- dominance when size known, cost when not
# ----------------------------------------------------------------------

def q2(dists, N=100, trials=40, seed=2):
    rng = np.random.default_rng(seed)
    print("=" * 84)
    print(f"Q2: target-matched fixed partition vs Farey  (N={N})")
    print("    'final' = at full population; util curve = bandwidth used when underpopulated")
    print("=" * 84)
    for dist in dists:
        tv_tm, mg_tm, tv_fa, mg_fa = [], [], [], []
        util_tm = {q: [] for q in (0.25, 0.5, 0.75, 1.0)}
        util_fa = 1.0  # full-subdivision always uses all bandwidth
        for _ in range(trials):
            w = np.sort(weights(dist, N, rng))[::-1]
            ideal = w / w.sum()
            # target-matched fixed partition: arcs == ideal (TV=0 at full pop)
            tv_tm.append(0.0)
            mg_tm.append(ideal.min() * N)
            # farey at full pop
            fa = np.sort(arcs_of(stern_brocot_enum(N)))[::-1]
            tv_fa.append(0.5 * np.abs(fa - ideal).sum())
            mg_fa.append(fa.min() * N)
            # target-matched utilization when only fraction q of agents present
            # present = random subset; they own their FIXED final slots => util = sum of their shares
            order = rng.permutation(N)
            for q in util_tm:
                t = max(1, int(q * N))
                present = order[:t]
                util_tm[q].append(ideal[present].sum())  # fixed slots, rest idle
        print(f"-- {dist} --")
        print(f"   final TV:      farey={np.mean(tv_fa):.4f}   target-matched={np.mean(tv_tm):.4f}")
        print(f"   final mingap:  farey={np.mean(mg_fa):.3f}xU  target-matched={np.mean(mg_tm):.3f}xU")
        print(f"   utilization (farey=1.00 at all sizes):")
        for q in (0.25, 0.5, 0.75, 1.0):
            print(f"      at {int(q*100):>3}% pop:  target-matched={np.mean(util_tm[q]):.3f}   farey=1.000")
        print()


if __name__ == "__main__":
    dists = ["uniform", "two_class", "zipf", "lognormal"]
    q1(dists, [50, 100, 200])
    q2(dists, N=100)
