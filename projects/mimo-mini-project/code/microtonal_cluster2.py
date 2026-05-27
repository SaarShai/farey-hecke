"""
Microtonal scale-search using Stern-Brocot mediants, optionally exploiting
the cluster=2 result from our Farey-gap mini-project.

The cluster=2 result (BCZ-asymptotic, q >= 7/9; empirical q >= 0.9 for N=5000):
extreme small Farey-gap events come in clusters of size <= 2.

Question we test here: does this give a useful speedup for microtonal
scale search? Honest a-priori expectation: probably NOT, because:
  (a) the cluster=2 regime is the high-quantile extreme-gap regime,
      which is different from the convergent regime that governs best
      rational approximation;
  (b) the existing continued-fraction / Stern-Brocot algorithm for best
      rational approximation is already O(log Q) per target, so it's
      hard to beat asymptotically;
  (c) "pair refinement" is what continued fractions already do
      (consecutive convergents flank the target), so cluster=2 may
      just be re-deriving what's already standard.

We still run the experiment honestly.

Author: Farey NOW project, 2026-05-27.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from fractions import Fraction
from typing import Callable


# ---------------------------------------------------------------------------
# 1. Brute-force baseline: best rational p/q with q <= Q approximating x
# ---------------------------------------------------------------------------

def best_rational_bruteforce(x: float, max_denom: int) -> tuple[int, int, float]:
    """Enumerate all denominators 1..max_denom, find p that minimizes |p/q - x|.

    Returns (p, q, error). Cost: O(max_denom).
    """
    best_p, best_q, best_err = 0, 1, abs(x)
    for q in range(1, max_denom + 1):
        p = round(x * q)
        err = abs(p / q - x)
        if err < best_err:
            best_p, best_q, best_err = p, q, err
    return best_p, best_q, best_err


# ---------------------------------------------------------------------------
# 2. Standard Stern-Brocot mediant search (single-direction refinement)
#    This is the classical algorithm; O(log max_denom) iterations.
# ---------------------------------------------------------------------------

def best_rational_sb(x: float, max_denom: int) -> tuple[int, int, float, int]:
    """Stern-Brocot mediant search for best rational p/q <= max_denom denom.

    Returns (p, q, error, iterations).
    """
    assert x > 0
    # Bracket [a/b, c/d] with a/b < x < c/d. Start with 0/1 and 1/0
    # but for x>1 we let c/d grow with floor(x)+1.
    a, b = math.floor(x), 1
    c, d = math.floor(x) + 1, 1
    best_p, best_q, best_err = a, b, abs(a / b - x)
    if abs(c / d - x) < best_err:
        best_p, best_q, best_err = c, d, abs(c / d - x)

    iters = 0
    while True:
        iters += 1
        # Mediant
        p, q = a + c, b + d
        if q > max_denom:
            break
        val = p / q
        err = abs(val - x)
        if err < best_err:
            best_p, best_q, best_err = p, q, err
        if val < x:
            a, b = p, q
        elif val > x:
            c, d = p, q
        else:
            return p, q, 0.0, iters
    return best_p, best_q, best_err, iters


# ---------------------------------------------------------------------------
# 3. Cluster=2-aware Stern-Brocot search.
#    Hypothesis: after taking one mediant step in direction D, take the NEXT
#    mediant step in the SAME direction (paired refinement) before checking
#    the other side. Motivated by cluster=2: extreme-gap exceedances come
#    in pairs sharing a small middle denominator.
#
#    Implementation: same Stern-Brocot, but whenever we go (say) left, we
#    take a "double-step" -- the mediant of the mediant -- before re-bracketing.
#    This is equivalent to a continued-fraction-style "best rational
#    approximation from below/above" step that combines two SB moves.
# ---------------------------------------------------------------------------

def best_rational_sb_cluster2(x: float, max_denom: int) -> tuple[int, int, float, int]:
    """Stern-Brocot with paired mediant refinements (cluster=2-motivated).

    When the mediant lies on side S relative to x, we accept it AND any
    additional same-direction mediants (run-length aggregation, NOT just
    2). Cluster=2 motivates exploring "pairs" of same-side refinements
    cheaply; standard CF theory says these same-side runs have length
    equal to CF coefficients a_i, which can be > 2. To preserve
    correctness we still update the bracket by single steps internally
    (Stern-Brocot run-length acceleration is the standard CF algorithm).

    Returns (p, q, error, iterations).
    """
    assert x > 0
    a, b = math.floor(x), 1
    c, d = math.floor(x) + 1, 1
    best_p, best_q, best_err = a, b, abs(a / b - x)
    if abs(c / d - x) < best_err:
        best_p, best_q, best_err = c, d, abs(c / d - x)

    iters = 0
    while True:
        iters += 1
        # Run-length acceleration: take as many same-direction mediants as
        # possible in one batch (this is the CF coefficient a_i). Cluster=2
        # says k=2 is the typical run length at high quantile; we let k
        # grow naturally and report the empirical k each iteration.
        p, q = a + c, b + d
        if q > max_denom:
            break
        val = p / q
        if val < x:
            # Going right: keep adding (c,d) to (a,b) until we overshoot or exceed Q
            k = 1
            while True:
                p_try = a + (k + 1) * c
                q_try = b + (k + 1) * d
                if q_try > max_denom:
                    break
                v_try = p_try / q_try
                if v_try >= x:
                    break
                k += 1
            p_new, q_new = a + k * c, b + k * d
            err_new = abs(p_new / q_new - x)
            if err_new < best_err:
                best_p, best_q, best_err = p_new, q_new, err_new
            a, b = p_new, q_new
        elif val > x:
            k = 1
            while True:
                p_try = (k + 1) * a + c
                q_try = (k + 1) * b + d
                if q_try > max_denom:
                    break
                v_try = p_try / q_try
                if v_try <= x:
                    break
                k += 1
            p_new, q_new = k * a + c, k * b + d
            err_new = abs(p_new / q_new - x)
            if err_new < best_err:
                best_p, best_q, best_err = p_new, q_new, err_new
            c, d = p_new, q_new
        else:
            return p, q, 0.0, iters
    return best_p, best_q, best_err, iters


# ---------------------------------------------------------------------------
# 4. Microtonal-scale objective: given a set of target just-intonation
#    intervals, find best n-EDO (equal divisions of octave) approximation.
#
#    For n-EDO, the available pitches are k/n * log2(2) octaves = k/n octave
#    for k=0..n-1. Each target ratio r maps to log2(r) octaves; best k is
#    round(n * log2(r)). Approximation error in cents: 1200 * |log2(r) - k/n|.
#
#    The search problem we tackle: find n in [n_min, n_max] minimizing the
#    weighted max (or sum) of errors across targets.
# ---------------------------------------------------------------------------

@dataclass
class ScaleResult:
    n_tones: int
    degrees: dict          # target ratio -> (k, cents_error)
    max_error_cents: float
    sum_error_cents: float


def evaluate_edo(n: int, targets: list[Fraction]) -> ScaleResult:
    degrees = {}
    max_err, sum_err = 0.0, 0.0
    for r in targets:
        log2r = math.log2(float(r))
        k = round(log2r * n)
        cents_err = 1200.0 * abs(log2r - k / n)
        degrees[r] = (k, cents_err)
        if cents_err > max_err:
            max_err = cents_err
        sum_err += cents_err
    return ScaleResult(n_tones=n, degrees=degrees,
                       max_error_cents=max_err, sum_error_cents=sum_err)


def find_best_n_tone_scale_bruteforce(
    target_intervals: list[Fraction],
    n_min: int,
    n_max: int,
    objective: str = "max",
) -> ScaleResult:
    """Brute-force: evaluate every n in [n_min, n_max].

    Cost: O((n_max - n_min) * |targets|).
    """
    best = None
    for n in range(n_min, n_max + 1):
        res = evaluate_edo(n, target_intervals)
        score = res.max_error_cents if objective == "max" else res.sum_error_cents
        if best is None or score < (best.max_error_cents if objective == "max"
                                    else best.sum_error_cents):
            best = res
    return best


# ---------------------------------------------------------------------------
# 5. Cluster=2-aware n-EDO search.
#
#    Idea: instead of enumerating every n, jump between n-values where
#    the approximation error to a "key" target (e.g. 3/2) has small
#    Farey-style neighbours. The best n-EDO approximations to log2(3/2)
#    correspond to convergents of its continued fraction (12, 41, 53, ...),
#    so we focus search around convergents and their cluster=2 neighbours.
#
#    Cluster=2 says: at high quantile q (very small extreme gaps), the
#    exceedances come in pairs. We test whether checking n-values within
#    a small window around each convergent (the "pair") is enough.
# ---------------------------------------------------------------------------

def continued_fraction_convergents(x: float, max_denom: int) -> list[tuple[int, int]]:
    """Continued-fraction convergents p_k/q_k with q_k <= max_denom."""
    a0 = math.floor(x)
    convergents = [(a0, 1)]
    h_1, h_2 = 1, 0
    k_1, k_2 = 0, 1
    h_0, k_0 = a0, 1
    r = x - a0
    while r > 1e-15:
        x = 1.0 / r
        ai = math.floor(x)
        h_new = ai * h_0 + h_1
        k_new = ai * k_0 + k_1
        if k_new > max_denom:
            break
        convergents.append((h_new, k_new))
        h_1, h_2 = h_0, h_1
        k_1, k_2 = k_0, k_1
        h_0, k_0 = h_new, k_new
        r = x - ai
    return convergents


def find_best_n_tone_scale_cluster2(
    target_intervals: list[Fraction],
    n_min: int,
    n_max: int,
    objective: str = "max",
    window: int = 1,
) -> tuple[ScaleResult, int]:
    """Cluster=2-aware search: only evaluate n at convergent denominators
    of log2(r) for each target r, plus a small window (cluster-pair) around
    each convergent.

    Returns (best result, number of n-values evaluated).
    """
    candidate_n = set()
    # For each target, find continued-fraction convergents of log2(r) and
    # add their denominators as candidate n-values. Also add cluster=2
    # paired neighbours: denominators of mediant between consecutive
    # convergents (i.e. semi-convergents).
    for r in target_intervals:
        log2r = math.log2(float(r))
        # We want p/n ~ log2r, so denominators of CF of log2r are candidates.
        convs = continued_fraction_convergents(log2r, n_max)
        for (_, q) in convs:
            if n_min <= q <= n_max:
                candidate_n.add(q)
            # Cluster=2 window: add neighbouring n in [q-window, q+window]
            for dq in range(-window, window + 1):
                if n_min <= q + dq <= n_max and q + dq > 0:
                    candidate_n.add(q + dq)
        # Also add semi-convergents (mediant pairs)
        for i in range(len(convs) - 1):
            q1 = convs[i][1]
            q2 = convs[i + 1][1]
            for k in range(1, (q2 - q1) // max(q1, 1) + 2):
                semi_q = q1 + k * (q2 - q1) // max(1, (q2 // q1 + 1))
                if n_min <= semi_q <= n_max:
                    candidate_n.add(semi_q)

    best = None
    for n in sorted(candidate_n):
        res = evaluate_edo(n, target_intervals)
        score = res.max_error_cents if objective == "max" else res.sum_error_cents
        if best is None or score < (best.max_error_cents if objective == "max"
                                    else best.sum_error_cents):
            best = res
    return best, len(candidate_n)


# ---------------------------------------------------------------------------
# 6. Main entry: find_best_n_tone_scale(target_intervals, n_tones, max_denom)
#    Per task spec: returns the best n-tone scale approximating targets,
#    using cluster=2 refinement where helpful.
# ---------------------------------------------------------------------------

def find_best_n_tone_scale(
    target_intervals: list,
    n_tones: int | None,
    max_denom: int,
    method: str = "cluster2",
) -> dict:
    """Find best n-tone scale approximating target_intervals.

    Args:
        target_intervals: list of just-intonation ratios (e.g. [Fraction(3,2), ...])
        n_tones: if int, evaluate exactly that n-EDO. If None, search over
                 n in [5, max_denom].
        max_denom: maximum denominator (== max n-EDO to consider when n_tones is None).
        method: 'cluster2' (Stern-Brocot + cluster=2 pair window),
                'bruteforce', or 'continued-fraction'.

    Returns a dict with keys:
        n_tones, degrees (target -> (k, cents_err)),
        max_error_cents, sum_error_cents, method, evaluations.
    """
    targets = [Fraction(r) if not isinstance(r, Fraction) else r
               for r in target_intervals]
    if n_tones is not None:
        res = evaluate_edo(n_tones, targets)
        return {
            "n_tones": res.n_tones,
            "degrees": {str(t): v for t, v in res.degrees.items()},
            "max_error_cents": res.max_error_cents,
            "sum_error_cents": res.sum_error_cents,
            "method": "exact",
            "evaluations": 1,
        }
    if method == "bruteforce":
        res = find_best_n_tone_scale_bruteforce(targets, 5, max_denom)
        evals = max_denom - 5 + 1
    elif method == "cluster2":
        res, evals = find_best_n_tone_scale_cluster2(targets, 5, max_denom)
    else:
        raise ValueError(f"Unknown method: {method}")
    return {
        "n_tones": res.n_tones,
        "degrees": {str(t): v for t, v in res.degrees.items()},
        "max_error_cents": res.max_error_cents,
        "sum_error_cents": res.sum_error_cents,
        "method": method,
        "evaluations": evals,
    }


# ---------------------------------------------------------------------------
# 7. Benchmarks
# ---------------------------------------------------------------------------

def time_call(fn: Callable, *args, **kwargs):
    t0 = time.perf_counter()
    out = fn(*args, **kwargs)
    return out, time.perf_counter() - t0


def benchmark_single_rational(max_denoms=(100, 1000, 10_000, 100_000)):
    """Benchmark best_rational approximation to log2(3/2) (perfect-fifth in octaves)."""
    x = math.log2(3 / 2)  # ~0.5849625...
    rows = []
    for Q in max_denoms:
        (bf_p, bf_q, bf_err), bf_t = time_call(best_rational_bruteforce, x, Q)
        (sb_p, sb_q, sb_err, sb_iters), sb_t = time_call(best_rational_sb, x, Q)
        (c2_p, c2_q, c2_err, c2_iters), c2_t = time_call(best_rational_sb_cluster2, x, Q)
        rows.append({
            "Q": Q,
            "bruteforce": (bf_p, bf_q, bf_err, bf_t),
            "stern_brocot": (sb_p, sb_q, sb_err, sb_iters, sb_t),
            "cluster2": (c2_p, c2_q, c2_err, c2_iters, c2_t),
        })
    return rows


def benchmark_n_edo_search():
    """Find best n-EDO approximation to 5-limit JI: 3/2, 5/4, 6/5, 4/3, 5/3, 8/5."""
    targets = [Fraction(3, 2), Fraction(5, 4), Fraction(6, 5),
               Fraction(4, 3), Fraction(5, 3), Fraction(8, 5)]
    rows = []
    for Q in (50, 200, 500, 2000, 10_000):
        bf, bf_t = time_call(find_best_n_tone_scale, targets, None, Q, method="bruteforce")
        c2, c2_t = time_call(find_best_n_tone_scale, targets, None, Q, method="cluster2")
        rows.append({
            "Q": Q,
            "bruteforce": (bf["n_tones"], bf["max_error_cents"], bf["evaluations"], bf_t),
            "cluster2":   (c2["n_tones"], c2["max_error_cents"], c2["evaluations"], c2_t),
        })
    return rows, targets


def benchmark_31_edo():
    """Specific test: how well does 31-EDO approximate 5-limit JI?
    Compare against optimum 31 and nearby n found by each method."""
    targets = [Fraction(3, 2), Fraction(5, 4), Fraction(6, 5),
               Fraction(4, 3), Fraction(5, 3), Fraction(8, 5)]
    r31 = evaluate_edo(31, targets)
    return r31, targets


# ---------------------------------------------------------------------------

def main():
    print("=" * 72)
    print("Microtonal scale search using cluster=2 — benchmark")
    print("=" * 72)

    # --- Part A: single-rational best approximation ---
    print("\n[A] Best rational p/q approximating log2(3/2) = 0.58496...")
    print(f"{'Q':>8} | {'brute t (s)':>10} | {'SB t (s)':>10} | {'C2 t (s)':>10} | "
          f"{'SB iters':>9} | {'C2 iters':>9} | best p/q")
    print("-" * 100)
    for row in benchmark_single_rational():
        Q = row["Q"]
        bf_p, bf_q, bf_err, bf_t = row["bruteforce"]
        sb_p, sb_q, sb_err, sb_iters, sb_t = row["stern_brocot"]
        c2_p, c2_q, c2_err, c2_iters, c2_t = row["cluster2"]
        assert (sb_p, sb_q) == (bf_p, bf_q) == (c2_p, c2_q), \
            f"Methods disagree at Q={Q}: bf={bf_p}/{bf_q}, sb={sb_p}/{sb_q}, c2={c2_p}/{c2_q}"
        print(f"{Q:>8} | {bf_t:10.6f} | {sb_t:10.6f} | {c2_t:10.6f} | "
              f"{sb_iters:>9} | {c2_iters:>9} | {bf_p}/{bf_q}")

    # --- Part B: 31-EDO baseline for 5-limit JI ---
    print("\n[B] 31-EDO approximation to 5-limit JI (standard benchmark)")
    r31, _ = benchmark_31_edo()
    print(f"  31-EDO max error: {r31.max_error_cents:.3f} cents")
    print(f"  31-EDO sum error: {r31.sum_error_cents:.3f} cents")
    for t, (k, err) in r31.degrees.items():
        print(f"     {str(t):>6} -> {k:>3}/31 step ({1200*k/31:7.3f} c)  err {err:6.3f} c")

    # --- Part C: n-EDO search comparison ---
    print("\n[C] Searching for best n-EDO over [5, Q] for 5-limit JI")
    print(f"{'Q':>8} | {'BF best n':>10} | {'BF maxerr':>10} | {'BF t (s)':>10} | "
          f"{'C2 best n':>10} | {'C2 maxerr':>10} | {'C2 t (s)':>10} | "
          f"{'BF evals':>9} | {'C2 evals':>9} | speedup")
    print("-" * 130)
    rows, _ = benchmark_n_edo_search()
    for row in rows:
        Q = row["Q"]
        bf_n, bf_e, bf_evals, bf_t = row["bruteforce"]
        c2_n, c2_e, c2_evals, c2_t = row["cluster2"]
        speedup = bf_t / c2_t if c2_t > 0 else float("inf")
        match = "OK" if bf_n == c2_n else f"MISS bf={bf_n} c2={c2_n}"
        print(f"{Q:>8} | {bf_n:>10} | {bf_e:>10.3f} | {bf_t:10.6f} | "
              f"{c2_n:>10} | {c2_e:>10.3f} | {c2_t:10.6f} | "
              f"{bf_evals:>9} | {c2_evals:>9} | {speedup:>5.1f}x  {match}")

    # --- Part D: honesty analysis ---
    print("\n[D] Honest analysis")
    print("-" * 72)
    print("Q1: Does cluster=2 help for SINGLE best rational approximation?")
    print("    Answer: No measurable benefit. Stern-Brocot mediant already")
    print("    converges in O(log Q) steps. The cluster=2 'paired step' just")
    print("    bundles two SB mediants per loop iteration, halving iteration")
    print("    count but doing the same work. Brute force is O(Q) and only")
    print("    looks worse asymptotically; for Q <= 10^4 it's microseconds.")
    print()
    print("Q2: Does cluster=2 help for n-EDO scale search?")
    print("    Cluster=2 here is REPURPOSED as a heuristic: only evaluate n")
    print("    at continued-fraction-convergent denominators of log2(r)")
    print("    (the 'pair' is the convergent and its neighbours). This")
    print("    cuts evaluations from Q-5 to O(log Q * |targets|).")
    print()
    print("    BUT: this is just the standard continued-fraction best-")
    print("    rational-approximation theorem, NOT a new use of cluster=2.")
    print("    The cluster=2 result (BCZ, q>=7/9) governs SMALL Farey gaps")
    print("    in the bulk Farey sequence; convergents are about LARGE")
    print("    isolated good approximations. Different regimes.")
    print()
    print("Q3: Honest verdict")
    print("    cluster=2 does NOT give a real algorithmic speedup for")
    print("    microtonal scale search. The speedup we measure above")
    print("    comes from using continued-fraction convergents (classical,")
    print("    19th-century math), which we labelled 'cluster2' but")
    print("    are not actually exploiting the BCZ-asymptotic result.")
    print()
    print("    If cluster=2 has algorithmic value, it would be in problems")
    print("    where the relevant Farey gaps are at quantile >= 0.9 of a")
    print("    fixed Farey sequence F_N -- e.g. enumerating ALL pairs of")
    print("    close fractions (denominator-coprime), where knowing they")
    print("    come in pairs of size 2 lets you skip half the search.")


if __name__ == "__main__":
    main()
