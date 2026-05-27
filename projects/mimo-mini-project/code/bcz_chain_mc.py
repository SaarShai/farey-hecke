"""BCZ Markov chain Monte Carlo: simulate the chain directly (not finite Farey)
to find the BCZ-density limit P(cluster ≥ 3 at quantile q) for various q.

The BCZ map: given (x_i, x_{i+1}) ∈ T = {x+y > 1, 0 < x,y < 1}, the next state is
  (x_{i+1}, k · x_{i+1} - x_i)
where k = ⌊(1 + x_i) / x_{i+1}⌋, modulo the triangle constraint.

The gap d_i = 1/(b_i · b_{i+1}) corresponds to 1/(X_i · X_{i+1}) in normalized units.
"""
import random
import math
from collections import Counter
import sys

random.seed(42)

def sample_initial():
    """Sample (X_0, X_1) from BCZ density 2 on T."""
    while True:
        x = random.random()
        y = random.random()
        if x + y > 1:
            return x, y

def bcz_step(x, y):
    """Apply BCZ map: (x, y) → (y, k·y - x) where k = floor((1+x)/y)."""
    k = math.floor((1 + x) / y)
    return y, k*y - x

def simulate(N_steps, q_list):
    """Run BCZ chain N_steps. For each q in q_list, compute fraction of size-3+ clusters."""
    # Phase 1: collect gaps
    x, y = sample_initial()
    # Burn-in
    for _ in range(1000):
        x, y = bcz_step(x, y)
    
    gaps = []
    pairs = [(x, y)]
    for _ in range(N_steps):
        x, y = bcz_step(x, y)
        gaps.append(1.0 / (pairs[-1][0] * pairs[-1][1]))  # gap from prev pair
        pairs.append((x, y))
    # Note: gap_i corresponds to pair (X_i, X_{i+1})
    
    sorted_g = sorted(gaps)
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
        size3p = sum(c for s, c in sizes.items() if s >= 3)
        results[q] = (total, size3p, sizes, thr)
    return results

# Test at various q
N_steps = 1_000_000
q_list = [0.50, 0.60, 0.70, 0.78, 0.807, 0.85, 0.86, 0.87, 0.88, 0.90, 0.95, 0.99]
print(f"BCZ chain MC, {N_steps} steps", flush=True)
print(f"q       total_clusters  size3+  fraction  max_size  threshold")
results = simulate(N_steps, q_list)
for q in q_list:
    total, size3p, sizes, thr = results[q]
    max_size = max(sizes.keys()) if sizes else 0
    frac = size3p / total if total > 0 else 0
    marker = ""
    if abs(q - 0.807) < 0.001: marker = " ← median-run cutoff"
    if abs(q - 7/9) < 0.001: marker = " ← 7/9"
    print(f"{q:.4f}  {total:>13}  {size3p:>6}  {frac:.5f}  {max_size:>8}  {thr:.4e}{marker}", flush=True)
