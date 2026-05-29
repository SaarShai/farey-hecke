"""cluster2_pruning_demo.py — does cluster=2 universality buy us an algorithmic speedup?

Problem (extreme-gap Farey enumeration):
    Given N, threshold quantile q with q > q*_BCZ = (11 - 8 ln(3/2))/9 ≈ 0.86181,
    enumerate every maximal RUN of consecutive Farey gaps g_i = a_{i+1}/b_{i+1} - a_i/b_i
    that exceed the q-quantile threshold τ. Report each run's (start, length, gaps).

cluster=2 universality:
    Above q*_BCZ, no maximal run can have length ≥ 3 — every cluster has size 1 or 2.
    => after detecting 2 consecutive extreme gaps, the next gap CANNOT be extreme,
       so we can skip the comparison and the bookkeeping that would have followed.

Two algorithms here:

  baseline:
    stream gaps; maintain a running extreme-counter `cur`. On gap > τ, cur += 1;
    on gap ≤ τ, close the run (if any) and reset.

  pruned (uses cluster=2):
    same stream, but the moment `cur == 2`, declare the next gap implicitly
    non-extreme, close the run, and SKIP the threshold-comparison on the next
    gap. The next gap is still computed (Stern-Brocot recurrence is unavoidable),
    but its branch is forced.

Honesty check:
  The threshold comparison is a single float compare — possibly the saving is
  not measurable against the recurrence cost. We measure to find out.

Correctness check:
  Both algorithms must produce IDENTICAL run lists.
"""

from __future__ import annotations
import math
import sys
import time
import statistics
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


def _p(*args, **kwargs):
    """Print + flush so progress is visible during long runs."""
    kwargs.setdefault("flush", True)
    print(*args, **kwargs)

Q_STAR_BCZ = (11.0 - 8.0 * math.log(3.0 / 2.0)) / 9.0  # ≈ 0.8618087927927428


# ----------------------------------------------------------------------
# Farey gap streaming via Stern-Brocot recurrence.
# Generates b_i (denominators) in order. Gap_i = 1 / (b_i * b_{i+1}).
# ----------------------------------------------------------------------

def stream_denominators(N: int):
    """Yield denominators b_0, b_1, b_2, ... of F_N in order."""
    a, b, c, d = 0, 1, 1, N
    yield b  # b_0 = 1 (fraction 0/1)
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        yield b


def stream_gaps_np(N: int) -> np.ndarray:
    """Materialize all gaps of F_N as float64 array. Memory O(|F_N|)."""
    bs = np.fromiter(stream_denominators(N), dtype=np.int64)
    # gap_i = 1 / (b_i * b_{i+1})
    return 1.0 / (bs[:-1].astype(np.float64) * bs[1:].astype(np.float64))


# ----------------------------------------------------------------------
# Threshold from quantile (vectorised).
# ----------------------------------------------------------------------

def threshold_for_q(gaps: np.ndarray, q: float) -> float:
    """Return τ s.t. fraction of gaps > τ is approx (1-q)."""
    n = len(gaps)
    idx = min(int(q * n), n - 1)
    # Use partition rather than full sort — faster, same threshold.
    return float(np.partition(gaps, idx)[idx])


# ----------------------------------------------------------------------
# Algorithm A (baseline): scan every gap.
# Returns list of (start, length) tuples.
# ----------------------------------------------------------------------

def enumerate_runs_baseline(gaps: np.ndarray, tau: float) -> List[Tuple[int, int]]:
    runs: List[Tuple[int, int]] = []
    n = len(gaps)
    i = 0
    while i < n:
        if gaps[i] > tau:
            j = i
            while j < n and gaps[j] > tau:
                j += 1
            runs.append((i, j - i))
            i = j
        else:
            i += 1
    return runs


# ----------------------------------------------------------------------
# Algorithm B (pruned, uses cluster=2):
# After exactly 2 consecutive extreme gaps, skip the comparison on the next
# gap — by cluster=2, it MUST be ≤ τ.
# ----------------------------------------------------------------------

def enumerate_runs_pruned(gaps: np.ndarray, tau: float) -> List[Tuple[int, int]]:
    runs: List[Tuple[int, int]] = []
    n = len(gaps)
    i = 0
    while i < n:
        if gaps[i] > tau:
            # First extreme gap of a potential run.
            if i + 1 < n and gaps[i + 1] > tau:
                # Second extreme gap confirmed — cluster=2 says i+2 CANNOT be extreme.
                # Skip the comparison on i+2 entirely; advance i to i+3.
                runs.append((i, 2))
                i += 3  # ← the prune: skip one threshold comparison + bookkeeping
            else:
                runs.append((i, 1))
                i += 2  # gap i+1 known ≤ τ, no need to re-check
        else:
            i += 1
    return runs


# ----------------------------------------------------------------------
# Algorithm C (vectorised baseline): NumPy comparison + run-length encode.
# This is the strongest realistic baseline — it's what one would actually
# write in Python for this problem. cluster=2 can't help here since the
# comparison is fully vectorised.
# ----------------------------------------------------------------------

def enumerate_runs_vectorised(gaps: np.ndarray, tau: float) -> List[Tuple[int, int]]:
    mask = gaps > tau
    if not mask.any():
        return []
    # Find run starts and ends.
    padded = np.r_[False, mask, False]
    diff = np.diff(padded.astype(np.int8))
    starts = np.where(diff == 1)[0]
    ends = np.where(diff == -1)[0]
    lengths = ends - starts
    return list(zip(starts.tolist(), lengths.tolist()))


# ----------------------------------------------------------------------
# Streaming-mode algorithms: do not materialise all gaps.
# Useful at larger N where memory is the bottleneck.
# These do TWO passes over the Stern-Brocot recurrence:
#   pass 1: sample gaps to estimate τ (reservoir of fixed size).
#   pass 2: stream gaps and enumerate runs.
# The pruning saves the comparison on the gap immediately after a size-2 cluster.
# The Stern-Brocot integer step is unavoidable.
# ----------------------------------------------------------------------

def estimate_tau_streaming(N: int, q: float, sample_size: int = 200_000) -> float:
    """One-pass estimate of τ from a sub-sampled stream."""
    rng = np.random.default_rng(0)
    samples = []
    bs_iter = stream_denominators(N)
    prev = next(bs_iter)
    # Reservoir-style: take first `sample_size`, then random subsequent swaps.
    i = 0
    for b in bs_iter:
        g = 1.0 / (prev * b)
        if len(samples) < sample_size:
            samples.append(g)
        else:
            j = rng.integers(0, i + 1)
            if j < sample_size:
                samples[j] = g
        prev = b
        i += 1
    arr = np.asarray(samples, dtype=np.float64)
    idx = min(int(q * len(arr)), len(arr) - 1)
    return float(np.partition(arr, idx)[idx])


def enumerate_runs_streaming_baseline(N: int, tau: float) -> List[Tuple[int, int]]:
    runs: List[Tuple[int, int]] = []
    bs_iter = stream_denominators(N)
    prev = next(bs_iter)
    cur_start = -1
    cur_len = 0
    i = 0
    for b in bs_iter:
        g = 1.0 / (prev * b)
        if g > tau:
            if cur_len == 0:
                cur_start = i
            cur_len += 1
        else:
            if cur_len > 0:
                runs.append((cur_start, cur_len))
                cur_len = 0
        prev = b
        i += 1
    if cur_len > 0:
        runs.append((cur_start, cur_len))
    return runs


def enumerate_runs_streaming_pruned(N: int, tau: float) -> List[Tuple[int, int]]:
    """Streaming + cluster=2: after 2 consecutive extreme gaps, skip the next
    threshold comparison entirely (the comparison is *forced* non-extreme,
    by cluster=2 universality)."""
    runs: List[Tuple[int, int]] = []
    bs_iter = stream_denominators(N)
    prev = next(bs_iter)
    cur_start = -1
    cur_len = 0
    skip_next_compare = False
    i = 0
    for b in bs_iter:
        if skip_next_compare:
            # Forced non-extreme by cluster=2. Skip the comparison.
            # No gap computation needed for the threshold check, but we still
            # need to advance `prev`.
            skip_next_compare = False
            prev = b
            i += 1
            continue
        g = 1.0 / (prev * b)
        if g > tau:
            if cur_len == 0:
                cur_start = i
            cur_len += 1
            if cur_len == 2:
                # Cluster of size 2 confirmed — flush, and SKIP next comparison.
                runs.append((cur_start, 2))
                cur_len = 0
                skip_next_compare = True
        else:
            if cur_len > 0:
                runs.append((cur_start, cur_len))
                cur_len = 0
        prev = b
        i += 1
    if cur_len > 0:
        runs.append((cur_start, cur_len))
    return runs


# ----------------------------------------------------------------------
# Benchmark harness.
# ----------------------------------------------------------------------

@dataclass
class BenchResult:
    N: int
    q: float
    n_gaps: int
    tau: float
    n_runs: int
    n_size2: int
    n_size_ge3: int
    baseline_secs: float
    pruned_secs: float
    vectorised_secs: float
    same_output: bool


def time_fn(fn, *args, repeats: int = 5):
    """Median over `repeats` runs."""
    samples = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        out = fn(*args)
        samples.append(time.perf_counter() - t0)
    return statistics.median(samples), out


def benchmark_one(N: int, q: float, repeats: int = 5) -> BenchResult:
    gaps = stream_gaps_np(N)
    tau = threshold_for_q(gaps, q)

    # Warm-up call (discarded) to avoid cold-cache bias on the first algorithm.
    _ = enumerate_runs_baseline(gaps, tau)

    # Interleave base / prune / vec across repeats so order-effects average out.
    base_times, prune_times, vec_times = [], [], []
    runs_base = runs_prune = runs_vec = None
    for _ in range(repeats):
        t0 = time.perf_counter(); runs_base = enumerate_runs_baseline(gaps, tau)
        base_times.append(time.perf_counter() - t0)
        t0 = time.perf_counter(); runs_prune = enumerate_runs_pruned(gaps, tau)
        prune_times.append(time.perf_counter() - t0)
        t0 = time.perf_counter(); runs_vec = enumerate_runs_vectorised(gaps, tau)
        vec_times.append(time.perf_counter() - t0)
    t_base = statistics.median(base_times)
    t_prune = statistics.median(prune_times)
    t_vec = statistics.median(vec_times)

    same_bp = runs_base == runs_prune
    same_bv = runs_base == runs_vec
    same_all = same_bp and same_bv

    # Count cluster-size distribution from baseline (truth).
    size2 = sum(1 for _, ln in runs_base if ln == 2)
    sizege3 = sum(1 for _, ln in runs_base if ln >= 3)

    return BenchResult(
        N=N, q=q, n_gaps=len(gaps), tau=tau, n_runs=len(runs_base),
        n_size2=size2, n_size_ge3=sizege3,
        baseline_secs=t_base, pruned_secs=t_prune, vectorised_secs=t_vec,
        same_output=same_all,
    )


def main():
    _p(f"cluster=2 pruning demo — q*_BCZ = {Q_STAR_BCZ:.10f}")
    _p()
    _p("Pick q comfortably ABOVE q*_BCZ so cluster=2 universality applies.")
    _p("If q < q*_BCZ the pruned algorithm is INCORRECT (size-3+ runs exist).")
    _p()

    # Show universality empirically by also running q below q*_BCZ.
    # NOTE: |F_N| ≈ 3·N²/π², so N=10^4 already gives ~3·10^7 gaps (~240 MB float64).
    # Anything beyond N≈15k is impractical to materialise in memory.
    grid = [
        # (N, q)
        ( 1_000, 0.99),
        ( 3_000, 0.99),
        (10_000, 0.99),
        ( 1_000, 0.90),   # still above q*_BCZ
        ( 3_000, 0.90),
        ( 5_000, 0.90),
        ( 1_000, 0.87),   # just above q*_BCZ
        ( 3_000, 0.87),
        ( 5_000, 0.87),
    ]

    header = (
        f"{'N':>10} {'q':>6} {'|gaps|':>10} {'#runs':>8} "
        f"{'#sz=2':>7} {'#sz≥3':>7} {'base(ms)':>10} {'prune(ms)':>10} "
        f"{'vec(ms)':>9} {'prune/base':>11} {'same?':>6}"
    )
    _p(header)
    _p("-" * len(header))

    for N, q in grid:
        _p(f"  ... running N={N}, q={q}", end="\r")
        reps = 3 if N >= 10_000 else 5
        t_start = time.perf_counter()
        r = benchmark_one(N, q, repeats=reps)
        _p(f"  [done N={N:>10} q={q:.3f}  wall={time.perf_counter()-t_start:.1f}s]", end="")
        _p()
        ratio = r.pruned_secs / r.baseline_secs if r.baseline_secs > 0 else float("nan")
        _p(
            f"{r.N:>10} {r.q:>6.3f} {r.n_gaps:>10} {r.n_runs:>8} "
            f"{r.n_size2:>7} {r.n_size_ge3:>7} "
            f"{r.baseline_secs*1e3:>10.3f} {r.pruned_secs*1e3:>10.3f} "
            f"{r.vectorised_secs*1e3:>9.3f} {ratio:>11.3f} "
            f"{'OK' if r.same_output else 'FAIL':>6}"
        )

    _p()
    _p("Sanity check: try q = 0.50 (well below q*_BCZ). cluster=2 should NOT hold,")
    _p("the pruned algorithm should produce WRONG output (size-3+ runs missed).")
    r = benchmark_one(3_000, 0.50, repeats=3)
    _p(
        f"{r.N:>10} {r.q:>6.3f} {r.n_gaps:>10} {r.n_runs:>8} "
        f"{r.n_size2:>7} {r.n_size_ge3:>7} "
        f"{r.baseline_secs*1e3:>10.3f} {r.pruned_secs*1e3:>10.3f} "
        f"{r.vectorised_secs*1e3:>9.3f} "
        f"{(r.pruned_secs/r.baseline_secs):>11.3f} "
        f"{'OK' if r.same_output else 'FAIL':>6}"
    )
    _p("(FAIL at q=0.5 is EXPECTED — the prune is unsound below q*_BCZ.)")
    _p(f"(At q=0.5 there are {r.n_size_ge3} clusters of size ≥ 3 that the prune misses.)")

    # ------------------------------------------------------------------
    # Streaming benchmark — for larger N where memory matters.
    # ------------------------------------------------------------------
    _p()
    _p("=" * 80)
    _p("Streaming-mode benchmark (no gap array materialised)")
    _p("Used at larger N where |F_N|·8 bytes does not fit in RAM.")
    _p("=" * 80)

    stream_header = (
        f"{'N':>10} {'q':>6} {'#runs':>8} {'#sz=2':>8} {'#sz≥3':>7} "
        f"{'base(s)':>9} {'prune(s)':>9} {'prune/base':>11} {'same?':>6}"
    )
    _p(stream_header)
    _p("-" * len(stream_header))

    stream_grid = [
        (3_000,  0.90),
        (5_000,  0.90),
        (3_000,  0.87),
        (5_000,  0.87),
    ]
    # Interleave runs (base, prune, base, prune, ...) to avoid order-effects /
    # cache warm-up bias. Single-shot timings are noisy; interleaved + median
    # is honest.
    for N, q in stream_grid:
        _p(f"  ... streaming N={N}, q={q}", end="\r")
        tau = estimate_tau_streaming(N, q, sample_size=100_000)

        # Warm-up run (discarded), then 3 interleaved measurements each.
        _ = enumerate_runs_streaming_baseline(N, tau)
        base_times, prune_times = [], []
        runs_base = runs_prune = None
        for _ in range(3):
            t0 = time.perf_counter()
            runs_base = enumerate_runs_streaming_baseline(N, tau)
            base_times.append(time.perf_counter() - t0)
            t0 = time.perf_counter()
            runs_prune = enumerate_runs_streaming_pruned(N, tau)
            prune_times.append(time.perf_counter() - t0)
        t_base = statistics.median(base_times)
        t_prune = statistics.median(prune_times)
        same = runs_base == runs_prune
        size2 = sum(1 for _, ln in runs_base if ln == 2)
        sizege3 = sum(1 for _, ln in runs_base if ln >= 3)
        ratio = t_prune / t_base if t_base > 0 else float("nan")
        _p(
            f"{N:>10} {q:>6.3f} {len(runs_base):>8} {size2:>8} {sizege3:>7} "
            f"{t_base:>9.2f} {t_prune:>9.2f} {ratio:>11.3f} "
            f"{'OK' if same else 'FAIL':>6}"
        )

    _p()
    _p("Notes:")
    _p(f"  q*_BCZ = (11 − 8·ln(3/2))/9 = {Q_STAR_BCZ:.10f}")
    _p("  Baseline & Pruned: Python while-loops; vectorised: NumPy whole-array.")
    _p("  All algorithms operate on the same pre-computed gap array.")


if __name__ == "__main__":
    main()
