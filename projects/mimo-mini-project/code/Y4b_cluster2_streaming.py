"""Y4b: Streaming cluster=2 for large N (memory-safe).

Y4 stored all gaps in memory → OOM at N=300k.

Y4b uses two passes:
  Pass 1: scan gaps, compute threshold via sampling (no full storage).
  Pass 2: scan again, count clusters above threshold streaming.

Threshold via "running quantile" — at quantile q, threshold is the
(1-q)-th largest gap. We use a min-heap of size k = round((1-q)*Φ(N))
to track top-k gaps. Memory: O(k) which for q=0.9999 at N=10⁶ is ~10⁵.
"""
import sys
import time
import heapq

def stream_gaps(N):
    a, b, c, d = 0, 1, 1, N
    prev_val = 0.0
    while c <= N:
        k = (N + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        cur_val = a / b
        yield cur_val - prev_val
        prev_val = cur_val

def cluster_stream(N, q):
    """Streaming compute: returns (n_gaps, threshold, size_distribution)."""
    t0 = time.time()
    # Pass 1: estimate Phi(N) and find top-k gaps via min-heap
    # Phi(N) ~ 3N²/pi² roughly; allocate heap conservatively
    import math
    Phi_est = int(3 * N * N / (math.pi ** 2)) + 10000
    k = int((1 - q) * Phi_est) + 1
    heap = []  # min-heap of top-k gaps
    n_gaps = 0
    for g in stream_gaps(N):
        n_gaps += 1
        if len(heap) < k:
            heapq.heappush(heap, g)
        elif g > heap[0]:
            heapq.heapreplace(heap, g)
    threshold = heap[0]  # smallest of top-k
    t1 = time.time()
    print(f"  Pass 1: n_gaps={n_gaps}, top-{k} threshold={threshold:.6e}, {t1-t0:.1f}s", flush=True)

    # Pass 2: stream gaps again, count clusters (consecutive runs above threshold)
    size_dist = {}
    current_run = 0
    n_exceed = 0
    for g in stream_gaps(N):
        if g > threshold:
            current_run += 1
            n_exceed += 1
        else:
            if current_run > 0:
                size_dist[current_run] = size_dist.get(current_run, 0) + 1
                current_run = 0
    if current_run > 0:
        size_dist[current_run] = size_dist.get(current_run, 0) + 1
    t2 = time.time()
    print(f"  Pass 2: n_exceed={n_exceed}, clusters={sum(size_dist.values())}, {t2-t1:.1f}s", flush=True)

    return n_gaps, threshold, size_dist

def main():
    if len(sys.argv) < 2:
        print("Usage: Y4b_cluster2_streaming.py N [q] [q2 q3 ...]")
        sys.exit(1)
    N = int(sys.argv[1])
    qs = [float(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else [0.99, 0.999, 0.9999]

    print(f"=== N={N} ===", flush=True)
    for q in qs:
        print(f"q={q}:", flush=True)
        n_gaps, threshold, size_dist = cluster_stream(N, q)
        n_clusters = sum(size_dist.values())
        total_size = sum(s * c for s, c in size_dist.items())
        mean_size = total_size / n_clusters if n_clusters > 0 else 0
        theta = 1 / mean_size if mean_size > 0 else 0
        pct = {s: size_dist.get(s, 0) / n_clusters * 100 if n_clusters > 0 else 0 for s in [1, 2, 3, 4, 5]}
        dist_str = " ".join(f"{s}:{size_dist.get(s, 0)}" for s in sorted(size_dist) if size_dist.get(s, 0) > 0)
        print(f"  n_gaps={n_gaps} clusters={n_clusters} theta={theta:.4f} mean_size={mean_size:.3f}", flush=True)
        print(f"  %size=1:{pct[1]:5.1f} %=2:{pct[2]:5.1f} %=3:{pct[3]:5.2f} %=4:{pct[4]:5.2f} %=5:{pct[5]:5.2f}", flush=True)
        print(f"  dist: {dist_str}", flush=True)

if __name__ == "__main__":
    main()
