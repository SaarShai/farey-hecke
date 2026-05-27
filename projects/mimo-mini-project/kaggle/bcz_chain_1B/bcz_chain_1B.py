"""BCZ chain 1 billion MC steps — pin down q*_BCZ to 6 decimals.

Tests the closed-form q*_BCZ = (11 - 8 ln(3/2))/9 ≈ 0.86180879
with extreme precision (1B samples → ~10^-9 statistical resolution).
"""
import time
import math
import json
import random
from collections import Counter

random.seed(12345)

def sample_init():
    while True:
        x, y = random.random(), random.random()
        if x + y > 1: return x, y

def bcz_step(x, y):
    k = math.floor((1 + x) / y)
    return y, k * y - x

def run_chain(N_steps, q_list):
    print(f"BCZ chain MC: {N_steps:,} steps")
    print(f"Closed-form q*_BCZ = {(11 - 8 * math.log(3/2)) / 9:.10f}")
    print()
    
    t0 = time.time()
    x, y = sample_init()
    # Burn-in
    for _ in range(50000): x, y = bcz_step(x, y)
    
    print(f"Generating {N_steps:,} pairs...", flush=True)
    pairs = [(x, y)]
    gaps = []
    for i in range(N_steps):
        x, y = bcz_step(x, y)
        gaps.append(1.0 / (pairs[-1][0] * pairs[-1][1]))
        pairs.append((x, y))
        if (i + 1) % 100_000_000 == 0:
            print(f"  {i+1:,} pairs in {time.time()-t0:.0f}s", flush=True)
    print(f"  total: {time.time()-t0:.0f}s, {len(gaps):,} gaps")
    
    # Sort once
    print("Sorting gaps...", flush=True)
    t1 = time.time()
    sorted_g = sorted(gaps)
    print(f"  sort done in {time.time()-t1:.0f}s")
    
    # For each q, threshold + cluster sizes
    print("\nResults:", flush=True)
    results = {}
    for q in q_list:
        thr_idx = min(int(q * len(gaps)), len(gaps) - 1)
        thr = sorted_g[thr_idx]
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
        s2 = sizes.get(2, 0) / total * 100 if total > 0 else 0
        s3p = sum(c for s, c in sizes.items() if s >= 3) / total * 100 if total > 0 else 0
        max_size = max(sizes.keys()) if sizes else 0
        
        # Top cluster sizes hist (capped)
        hist = {str(k): v for k, v in sorted(sizes.items()) if k <= 10}
        
        results[q] = {
            "threshold": thr,
            "total_clusters": total,
            "pct_size_2": s2,
            "pct_size_3_plus": s3p,
            "max_size": max_size,
            "hist_truncated": hist,
        }
        marker = ""
        if q >= 0.86181: marker = " ← above q*_BCZ closed form"
        elif q <= 0.86180: marker = " ← below q*_BCZ"
        print(f"  q={q:.5f}: clusters={total:,}, size-2={s2:.3f}%, size-3+={s3p:.5f}%, max={max_size}{marker}", flush=True)
    
    return results

# Run 1B steps at fine q resolution around closed form
N_steps = 1_000_000_000
results = run_chain(N_steps, [0.95, 0.99, 0.85, 0.86, 0.8615, 0.8618, 0.8619, 0.862, 0.865, 0.87, 0.9, 0.99])

with open("/kaggle/working/bcz_chain_1B_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nDone. Results saved to /kaggle/working/bcz_chain_1B_results.json")
