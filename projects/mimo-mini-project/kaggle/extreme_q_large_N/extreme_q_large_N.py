"""Extreme-q BCZ + large-N RMT — experiments 1 & 2.

EXPERIMENT 1 — Push BCZ cluster=2 % beyond q=0.99:
  Run BCZ chain at 1B MC steps and evaluate at q ∈ {0.99, 0.999, 0.9999, 0.99999}.
  Goal: confirm size-2 % → 100% as q → 1.

EXPERIMENT 2 — Large-N RMT: does cluster=2 % shift with sample size?
  β-Hermite β=1,2,4 at N ∈ {10000, 30000, 100000} with 3 reps each.
  Goal: confirm RMT stays at ~0% at q=0.99 even at large N.

Time budget: ~10 min on Kaggle CPU.
"""
import time, math, json
import numpy as np
from numba import njit
from collections import Counter

Q_STAR = (11.0 - 8.0 * math.log(3.0/2.0)) / 9.0
print(f"q*_BCZ = {Q_STAR:.12f}", flush=True)

# -------- EXPERIMENT 1: BCZ chain extreme-q --------

@njit(cache=True)
def burn_and_sample_gaps(N_burn, N_sample, seed):
    np.random.seed(seed)
    while True:
        x = np.random.random(); y = np.random.random()
        if x + y > 1.0: break
    for _ in range(N_burn):
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    out = np.empty(N_sample, dtype=np.float32)
    for i in range(N_sample):
        out[i] = np.float32(1.0 / (x * y))
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    return out, x, y

@njit(cache=True)
def count_clusters_streaming(x_in, y_in, N_steps, thresholds, cluster_hist_max):
    n_t = len(thresholds)
    hist = np.zeros((n_t, cluster_hist_max + 2), dtype=np.int64)
    cur = np.zeros(n_t, dtype=np.int64)
    x, y = x_in, y_in
    for i in range(N_steps):
        gap = 1.0 / (x * y)
        for t_idx in range(n_t):
            if gap > thresholds[t_idx]:
                cur[t_idx] += 1
            else:
                if cur[t_idx] > 0:
                    if cur[t_idx] <= cluster_hist_max:
                        hist[t_idx, cur[t_idx]] += 1
                    else:
                        hist[t_idx, cluster_hist_max + 1] += 1
                    cur[t_idx] = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    for t_idx in range(n_t):
        if cur[t_idx] > 0:
            if cur[t_idx] <= cluster_hist_max:
                hist[t_idx, cur[t_idx]] += 1
            else:
                hist[t_idx, cluster_hist_max + 1] += 1
    return hist, x, y

def bcz_extreme_q():
    print("\n=== EXPERIMENT 1: BCZ chain extreme-q ===", flush=True)
    t0 = time.time()
    Q_LIST = [0.99, 0.999, 0.9999, 0.99999]
    HIST_MAX = 10

    # Pass 1: sample 100M gaps for thresholds at extreme q
    SAMPLE_N = 100_000_000
    print(f"Pass 1: sampling {SAMPLE_N:,} gaps...", flush=True)
    gaps_sample, x, y = burn_and_sample_gaps(200_000, SAMPLE_N, 12345)
    gaps_sample.sort()
    thresholds_arr = np.array([gaps_sample[min(int(q * SAMPLE_N), SAMPLE_N - 1)] for q in Q_LIST], dtype=np.float64)
    print(f"  Thresholds: {dict(zip(Q_LIST, thresholds_arr))}", flush=True)
    del gaps_sample

    # Pass 2: stream 1B steps counting clusters
    STREAM_N = 1_000_000_000
    print(f"Pass 2: streaming {STREAM_N:,} steps...", flush=True)
    hist, _, _ = count_clusters_streaming(x, y, STREAM_N, thresholds_arr, HIST_MAX)

    results = {}
    for i, q in enumerate(Q_LIST):
        total = int(hist[i, 1:].sum())
        s2 = int(hist[i, 2])
        s3p = total - int(hist[i, 1]) - s2
        results[f"{q:.5f}"] = {
            "threshold": float(thresholds_arr[i]),
            "total_clusters": total,
            "size_1": int(hist[i, 1]),
            "size_2": s2,
            "size_3_plus": s3p,
            "pct_size_2": s2 / total * 100 if total > 0 else 0,
            "pct_size_3_plus": s3p / total * 100 if total > 0 else 0,
            "hist": {str(k): int(hist[i, k]) for k in range(1, HIST_MAX + 1) if hist[i, k] > 0},
        }
        marker = "← above q*_BCZ" if q > Q_STAR else ""
        print(f"  q={q:.5f}: clusters={total:,}, size-2={results[f'{q:.5f}']['pct_size_2']:.4f}%, size-3+={results[f'{q:.5f}']['pct_size_3_plus']:.6f}% {marker}", flush=True)

    print(f"  EXP 1 done in {time.time() - t0:.0f}s", flush=True)
    return results

# -------- EXPERIMENT 2: Large-N RMT --------

def beta_ensemble_spacings(beta, N, rng):
    """Tridiagonal Hermite β-ensemble, bulk spacings normalised to mean 1."""
    d = rng.standard_normal(N) * math.sqrt(2.0)
    sub = np.sqrt(rng.chisquare(beta * np.arange(N - 1, 0, -1)))
    T = np.diag(d) + np.diag(sub, k=1) + np.diag(sub, k=-1)
    eig = np.linalg.eigvalsh(T)
    e0 = int(0.2 * N); e1 = int(0.8 * N)
    bulk = eig[e0:e1]
    sp = np.diff(bulk)
    return sp / np.mean(sp)

def cluster_diagnostic(gaps, q_list):
    sorted_g = np.sort(gaps)
    results = {}
    for q in q_list:
        idx = min(int(q * len(gaps)), len(gaps) - 1)
        thr = sorted_g[idx]
        sizes = Counter()
        cur = 0
        for g in gaps:
            if g > thr:
                cur += 1
            else:
                if cur > 0:
                    sizes[cur] += 1
                    cur = 0
        if cur > 0: sizes[cur] += 1
        total = sum(sizes.values())
        s2 = sizes.get(2, 0)
        s3p = sum(c for s, c in sizes.items() if s >= 3)
        results[f"{q:.4f}"] = {
            "total_clusters": total,
            "size_2": s2,
            "size_3_plus": s3p,
            "pct_size_2": s2/total*100 if total > 0 else 0,
            "pct_size_3_plus": s3p/total*100 if total > 0 else 0,
            "max_size": max(sizes.keys()) if sizes else 0,
        }
    return results

def rmt_large_N():
    print("\n=== EXPERIMENT 2: Large-N RMT ===", flush=True)
    Q_LIST = [0.95, 0.99, 0.999]
    REPEATS = 3
    rng = np.random.default_rng(20260527)
    results = {}

    for beta in [1, 2, 4]:
        for N in [10_000, 30_000, 100_000]:
            label = f"beta_{beta}_N_{N}"
            print(f"\n  {label} ({REPEATS} reps)...", flush=True)
            t0 = time.time()
            per_q = {f"{q:.4f}": {"pct_size_2": [], "pct_size_3_plus": []} for q in Q_LIST}
            for r in range(REPEATS):
                gaps = beta_ensemble_spacings(beta, N, rng)
                res = cluster_diagnostic(gaps, Q_LIST)
                for qk, sv in res.items():
                    per_q[qk]["pct_size_2"].append(sv["pct_size_2"])
                    per_q[qk]["pct_size_3_plus"].append(sv["pct_size_3_plus"])
            summary = {"elapsed_s": time.time() - t0}
            for qk, vals in per_q.items():
                summary[qk] = {
                    "pct_size_2_mean": float(np.mean(vals["pct_size_2"])),
                    "pct_size_2_std": float(np.std(vals["pct_size_2"])),
                    "pct_size_3_plus_mean": float(np.mean(vals["pct_size_3_plus"])),
                    "pct_size_3_plus_std": float(np.std(vals["pct_size_3_plus"])),
                }
                print(f"    q={qk}: s2={summary[qk]['pct_size_2_mean']:.4f}±{summary[qk]['pct_size_2_std']:.4f}%, "
                      f"s3+={summary[qk]['pct_size_3_plus_mean']:.5f}%", flush=True)
            results[label] = summary
    return results

# -------- Run both --------

t_total = time.time()
out = {
    "q_star_BCZ": Q_STAR,
    "experiment_1_BCZ_extreme_q": bcz_extreme_q(),
    "experiment_2_RMT_large_N": rmt_large_N(),
    "total_elapsed_s": time.time() - t_total,
}

with open("/kaggle/working/extreme_q_large_N_results.json", "w") as f:
    json.dump(out, f, indent=2)
print(f"\nDone in {time.time() - t_total:.0f}s. Results saved.", flush=True)
