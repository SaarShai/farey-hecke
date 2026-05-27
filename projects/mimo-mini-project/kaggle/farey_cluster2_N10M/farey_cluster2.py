"""Cluster=2 universality at N=10^7 — streaming.

Tests our closed-form q*_BCZ = (11 - 8 ln(3/2))/9 ≈ 0.86181 empirically
at the largest N feasible on Kaggle's 9-hour CPU.
"""
import time
import math
import json
import heapq
from collections import Counter

def stream_pairs(N):
    """Yield consecutive Farey denominators via Stern-Brocot enumeration."""
    a, b, c, d = 0, 1, 1, N
    yield b
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        yield b

def streaming_cluster(N, q_list):
    """Two-pass: top-k heap for threshold, then count clusters."""
    print(f"\n=== N={N} ===", flush=True)
    t0 = time.time()
    
    # Pass 1: count total + find top-k thresholds
    print("Pass 1: enumerating + collecting top-k gaps...", flush=True)
    Phi_est = int(3 * N * N / (math.pi**2)) + 10000
    
    # We need top-k for each q. Use single largest k = (1-min_q)·Phi
    max_1mq = max(1 - q for q in q_list)
    k_max = int(max_1mq * Phi_est) + 100
    
    heap = []  # min-heap of top-k gaps (gap value = 1/(prev_b · b))
    n_gaps = 0
    prev_b = None
    for b in stream_pairs(N):
        if prev_b is not None:
            gap = 1.0 / (prev_b * b)
            if len(heap) < k_max:
                heapq.heappush(heap, gap)
            elif gap > heap[0]:
                heapq.heapreplace(heap, gap)
            n_gaps += 1
            if n_gaps % 100_000_000 == 0:
                print(f"  pass 1: {n_gaps:,} gaps in {time.time()-t0:.0f}s", flush=True)
        prev_b = b
    print(f"  pass 1 done: {n_gaps:,} gaps in {time.time()-t0:.0f}s", flush=True)
    
    # Sort heap to get thresholds
    sorted_heap = sorted(heap)  # ascending
    print(f"  heap size: {len(sorted_heap):,}")
    
    thresholds = {}
    for q in q_list:
        n_extreme = int((1 - q) * n_gaps)
        # threshold = (n_extreme)-th from TOP in our heap = len(heap) - n_extreme
        if n_extreme < len(sorted_heap):
            thresholds[q] = sorted_heap[len(sorted_heap) - n_extreme]
        else:
            thresholds[q] = sorted_heap[0]
    print(f"  thresholds: { {q: f'{t:.4e}' for q, t in thresholds.items()} }")
    
    # Pass 2: stream gaps again, count clusters per q
    print("Pass 2: counting clusters...", flush=True)
    t1 = time.time()
    results = {}
    for q, thr in thresholds.items():
        sizes = Counter()
        cur = 0
        prev_b = None
        for b in stream_pairs(N):
            if prev_b is not None:
                gap = 1.0 / (prev_b * b)
                if gap > thr:
                    cur += 1
                else:
                    if cur > 0:
                        sizes[cur] += 1
                        cur = 0
            prev_b = b
        if cur > 0:
            sizes[cur] += 1
        total = sum(sizes.values())
        s3p = sum(c for s, c in sizes.items() if s >= 3)
        results[q] = {
            "total_clusters": total,
            "size_3_plus": s3p,
            "fraction_3_plus": s3p / total if total > 0 else 0,
            "max_size": max(sizes.keys()) if sizes else 0,
            "hist": dict(sizes),
        }
    print(f"  pass 2 done in {time.time()-t1:.0f}s", flush=True)
    print(f"  total: {time.time()-t0:.0f}s")
    
    return results

# Run at multiple N
all_results = {}
for N in [1_000_000, 3_000_000, 10_000_000]:
    res = streaming_cluster(N, [0.95, 0.99, 0.999, 0.9999])
    all_results[N] = res
    # Print summary
    for q, r in res.items():
        pct_size_2 = r["hist"].get(2, 0) / r["total_clusters"] * 100 if r["total_clusters"] > 0 else 0
        print(f"  N={N} q={q}: size-2={pct_size_2:.2f}%, size-3+={r['fraction_3_plus']*100:.4f}%, max={r['max_size']}")

# Write results
with open("/kaggle/working/farey_cluster2_results.json", "w") as f:
    json.dump(all_results, f, indent=2, default=str)
print("\nResults saved to /kaggle/working/farey_cluster2_results.json")
print("\nClosed-form q*_BCZ = (11 - 8 ln(3/2))/9 =", (11 - 8 * math.log(3/2)) / 9)
