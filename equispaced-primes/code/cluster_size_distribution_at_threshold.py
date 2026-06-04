"""Cluster-size distribution of the BCZ chain at the exact threshold t* = 2/9.

Goal: high-precision empirical Pr(L=1), Pr(L=2) at t = 2/9 to test closed-form
candidates like P_BCZ(XY < 2/9) = (8 ln(3/2) - 2)/9.

Convention:
  - State (x, y) ∈ T = {(x,y): 0<x<1, 0<y<1, x+y>1}; stationary density f = 2.
  - Map T_BCZ(x, y) = (y, ky - x) with k = floor((1+x)/y).
  - Cluster-member condition at step i: X_i X_{i+1} < t*, where t* = 2/9.
  - A *cluster* is a maximal run of consecutive cluster-members.
  - cluster_size_le_two theorem (Lean v8) ⇒ no run of length ≥ 3 at t = 2/9.

We accumulate empirical Pr(L=k | a cluster starts here) = N_k / sum_j N_j and also
the "rates" Pr(cluster of size k starts at step i=0), which sum to P(start) = ?

This script runs ~10^9 BCZ chain steps split across multiple independent seeds
and reports the cluster-size distribution with bootstrap-style error bars.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import numpy as np
from numba import njit

T_STAR = 2.0 / 9.0  # exact threshold, NOT a quantile
Q_STAR_BCZ = (11.0 - 8.0 * math.log(3.0 / 2.0)) / 9.0
P_BCZ_XY_LT_2_9 = (8.0 * math.log(3.0 / 2.0) - 2.0) / 9.0  # P(X*Y < 2/9) on (T, f=2)


@njit(cache=True, fastmath=False)
def _sample_initial_TwoNbhd(seed: int):
    """Uniform sample from T = {x+y>1} ∩ (0,1)^2 by rejection."""
    np.random.seed(seed)
    while True:
        x = np.random.random()
        y = np.random.random()
        if x + y > 1.0:
            return x, y


@njit(cache=True, fastmath=False)
def _burn(x: float, y: float, n_burn: int):
    for _ in range(n_burn):
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x
    return x, y


@njit(cache=True, fastmath=False)
def run_chain_at_threshold(seed: int, n_burn: int, n_steps: int, hist_max: int):
    """Stream `n_steps` BCZ iterates after `n_burn` burn-in.

    At each step we test the *member condition* X_i X_{i+1} < t* (t* = 2/9 exact).
    Returns (hist, n_steps_actual) where
      hist[k] = number of clusters of size k (1 <= k <= hist_max), hist[hist_max+1] = overflow.

    Note: a transient at the start (where we don't yet know whether the previous
    pair was a member) introduces ±1 bias of order O(1) — negligible vs N≈1e9.
    """
    x, y = _sample_initial_TwoNbhd(seed)
    x, y = _burn(x, y, n_burn)

    hist = np.zeros(hist_max + 2, dtype=np.int64)
    cur_run = 0  # length of the current cluster (consecutive members)

    # Track previous member-bit so we know when a cluster begins/ends.
    # For step i=0 we don't have prev info — treat as non-member (drop first cluster if any).
    first_cluster_dropped = False

    for _ in range(n_steps):
        prod = x * y
        member = (prod < T_STAR)
        if member:
            cur_run += 1
        else:
            if cur_run > 0:
                if not first_cluster_dropped:
                    # discard the very first cluster — its size may be truncated
                    first_cluster_dropped = True
                else:
                    if cur_run <= hist_max:
                        hist[cur_run] += 1
                    else:
                        hist[hist_max + 1] += 1
                cur_run = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k * y - x

    # We DO NOT flush the trailing run — it may be truncated too. Drop it.

    return hist, n_steps


def _summarize(hist: np.ndarray, hist_max: int) -> dict:
    sizes = {int(k): int(hist[k]) for k in range(1, hist_max + 1) if hist[k] > 0}
    overflow = int(hist[hist_max + 1])
    if overflow > 0:
        sizes[f">{hist_max}"] = overflow
    total = sum(int(v) for v in sizes.values())
    out = {
        "total_clusters": total,
        "size_1": int(hist[1]),
        "size_2": int(hist[2]),
        "size_3_plus_observed": sum(int(hist[k]) for k in range(3, hist_max + 2)),
        "hist": sizes,
    }
    if total > 0:
        out["pr_L_eq_1"] = int(hist[1]) / total
        out["pr_L_eq_2"] = int(hist[2]) / total
        out["pr_L_ge_3"] = sum(int(hist[k]) for k in range(3, hist_max + 2)) / total
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-steps", type=int, default=200_000_000,
                        help="Steps per seed (default 2e8).")
    parser.add_argument("--n-seeds", type=int, default=5,
                        help="Number of independent seeds (default 5 → 1e9 total).")
    parser.add_argument("--n-burn", type=int, default=200_000,
                        help="Burn-in steps per seed (default 2e5).")
    parser.add_argument("--hist-max", type=int, default=10)
    parser.add_argument("--out", type=str,
                        default="/Users/za/Documents/Farey NOW/code/cluster_size_distribution_results.json")
    parser.add_argument("--seed-base", type=int, default=20260527)
    parser.add_argument("--smoke", action="store_true",
                        help="Quick smoke test: 5e6 steps × 2 seeds (~1 min).")
    args = parser.parse_args()

    if args.smoke:
        args.n_steps = 5_000_000
        args.n_seeds = 2

    print(f"BCZ cluster-size distribution at EXACT t* = 2/9", flush=True)
    print(f"  n_seeds   = {args.n_seeds}")
    print(f"  n_steps   = {args.n_steps:,}   (total: {args.n_seeds * args.n_steps:,})")
    print(f"  n_burn    = {args.n_burn:,}")
    print(f"  q*_BCZ    = {Q_STAR_BCZ:.12f}")
    print(f"  P(XY<2/9) = {P_BCZ_XY_LT_2_9:.12f}   [closed form]", flush=True)

    t0 = time.time()
    # JIT warmup
    print("\nJIT warmup...", flush=True)
    _ = run_chain_at_threshold(1, 1000, 1000, args.hist_max)
    print(f"  warmup done in {time.time() - t0:.1f}s", flush=True)

    per_seed = []
    total_hist = np.zeros(args.hist_max + 2, dtype=np.int64)
    for s in range(args.n_seeds):
        seed = args.seed_base + 7919 * s
        t1 = time.time()
        hist, n_done = run_chain_at_threshold(seed, args.n_burn, args.n_steps, args.hist_max)
        dt = time.time() - t1
        rate = n_done / dt / 1e6
        summ = _summarize(hist, args.hist_max)
        summ["seed"] = seed
        summ["n_steps"] = n_done
        summ["elapsed_s"] = dt
        per_seed.append(summ)
        total_hist += hist
        pr1 = summ.get("pr_L_eq_1", float("nan"))
        pr2 = summ.get("pr_L_eq_2", float("nan"))
        pr3 = summ.get("pr_L_ge_3", float("nan"))
        print(f"  seed {seed}: {n_done/1e6:.0f} M steps in {dt:.0f}s ({rate:.0f} M/s), "
              f"total_clusters={summ['total_clusters']:,}, "
              f"Pr(L=1)={pr1:.6f}, Pr(L=2)={pr2:.6f}, Pr(L≥3)={pr3:.2e}", flush=True)

    pooled = _summarize(total_hist, args.hist_max)
    pooled["n_seeds"] = args.n_seeds
    pooled["total_steps"] = args.n_seeds * args.n_steps
    pooled["elapsed_total_s"] = time.time() - t0

    # Inter-seed std (Bootstrap-style)
    pr1_vals = [s["pr_L_eq_1"] for s in per_seed if "pr_L_eq_1" in s]
    pr2_vals = [s["pr_L_eq_2"] for s in per_seed if "pr_L_eq_2" in s]
    if len(pr1_vals) >= 2:
        pooled["pr_L_eq_1_std_interseed"] = float(np.std(pr1_vals, ddof=1) / math.sqrt(len(pr1_vals)))
        pooled["pr_L_eq_2_std_interseed"] = float(np.std(pr2_vals, ddof=1) / math.sqrt(len(pr2_vals)))

    # Closed-form CANDIDATES to test:
    log32 = math.log(1.5)
    candidates = {
        "Pr(L=1) = (2 - 4 ln(3/2)) / 9":        (2.0 - 4.0 * log32) / 9.0,
        "Pr(L=1) = (3 - 4 ln(3/2)) / 9":        (3.0 - 4.0 * log32) / 9.0,
        "Pr(L=1) = 9 (Pr(L=1)_predicted)":       None,
        "Pr(L=1) = 1 - 8/(8 ln(3/2) - 2 + ...)": None,
        "Pr(L=2)/Pr(L=1) = (1 + 4 ln(3/2))/(1 - 4 ln(3/2))": None,
        "Pr(L=2)/Pr(L=1) = 17/5 (ratio test)": None,
        "(8 ln(3/2) - 2)/9 = P(XY<2/9)":         P_BCZ_XY_LT_2_9,
        "1 - q*_BCZ = (8 ln(3/2) - 2)/9":        1.0 - Q_STAR_BCZ,
    }
    pooled["closed_form_candidates"] = {k: v for k, v in candidates.items() if v is not None}
    # Distance of each candidate to pooled Pr(L=1)
    if "pr_L_eq_1" in pooled:
        pr1 = pooled["pr_L_eq_1"]
        pooled["candidate_residuals_for_PrL1"] = {
            k: abs(pr1 - v) for k, v in candidates.items() if v is not None
        }

    pooled["per_seed"] = per_seed
    pooled["meta"] = {
        "t_star": T_STAR,
        "q_star_BCZ": Q_STAR_BCZ,
        "P_BCZ_XY_lt_2_9": P_BCZ_XY_LT_2_9,
        "convention": "member iff X_i*X_{i+1} < 2/9; cluster = maximal run",
    }

    with open(args.out, "w") as f:
        json.dump(pooled, f, indent=2)

    print(f"\n=== POOLED (over {args.n_seeds} seeds) ===")
    print(f"  total clusters     = {pooled['total_clusters']:,}")
    print(f"  Pr(L=1)            = {pooled.get('pr_L_eq_1', float('nan')):.8f}")
    print(f"  Pr(L=2)            = {pooled.get('pr_L_eq_2', float('nan')):.8f}")
    print(f"  Pr(L>=3) observed  = {pooled.get('pr_L_ge_3', float('nan')):.3e}")
    if "pr_L_eq_1_std_interseed" in pooled:
        print(f"  Pr(L=1) inter-seed SE = {pooled['pr_L_eq_1_std_interseed']:.2e}")
        print(f"  Pr(L=2) inter-seed SE = {pooled['pr_L_eq_2_std_interseed']:.2e}")
    print(f"  elapsed            = {pooled['elapsed_total_s']:.0f}s")
    print(f"  output             = {args.out}")


if __name__ == "__main__":
    main()
