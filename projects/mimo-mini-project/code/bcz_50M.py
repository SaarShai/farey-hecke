"""High-precision BCZ chain MC at q just above and below the closed-form 0.86181."""
import random, math, sys
from collections import Counter

random.seed(789)
def sample_init():
    while True:
        x, y = random.random(), random.random()
        if x+y > 1: return x, y

def bcz_step(x, y):
    return y, math.floor((1+x)/y)*y - x

def sim(N_steps, q):
    x, y = sample_init()
    for _ in range(10000): x, y = bcz_step(x, y)
    pairs = [(x, y)]; gaps = []
    for _ in range(N_steps):
        x, y = bcz_step(x, y)
        gaps.append(1.0/(pairs[-1][0]*pairs[-1][1]))
        pairs.append((x, y))
    sorted_g = sorted(gaps)
    thr = sorted_g[int(q*len(gaps))]
    sizes = Counter(); cur = 0
    for g in gaps:
        if g > thr: cur += 1
        else:
            if cur > 0: sizes[cur] += 1; cur = 0
    if cur > 0: sizes[cur] += 1
    total = sum(sizes.values())
    s3 = sum(c for s,c in sizes.items() if s >= 3)
    return total, s3, max(sizes.keys()) if sizes else 0

N = 50_000_000
print(f'Ultra-high-precision BCZ MC ({N} steps) near q*_BCZ = (11-8 ln(3/2))/9 = 0.86181', flush=True)
print(f'q         total       size3+    fraction       max_size')
sys.stdout.flush()
for q in [0.8600, 0.8610, 0.8615, 0.8617, 0.8618, 0.8619, 0.8620, 0.8625]:
    import time
    t0 = time.time()
    total, s3, ms = sim(N, q)
    frac = s3/total if total > 0 else 0
    closed_form_marker = ' ← (11-8 ln(3/2))/9' if abs(q - 0.86181) < 0.0001 else ''
    print(f'{q:.4f}    {total:>8}    {s3:>6}    {frac:.7f}    {ms}    ({time.time()-t0:.0f}s){closed_form_marker}', flush=True)
