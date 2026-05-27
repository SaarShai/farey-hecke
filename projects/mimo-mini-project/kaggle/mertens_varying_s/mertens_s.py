"""Σ M(n)² / n^s for varying s — find any closed forms.

Compute at N=10^8 for s = 2.1, 2.5, 3, 3.5, 4, 5, 6.
"""
import time, math, json

def sieve(N):
    mu = [1]*(N+1); mu[0]=0
    is_p = bytearray(N+1)
    is_p[0]=is_p[1]=1
    for p in range(2, N+1):
        if is_p[p] == 0:
            for j in range(p, N+1, p):
                if j > p: is_p[j] = 1
                mu[j] = -mu[j]
            for j in range(p*p, N+1, p*p):
                mu[j] = 0
    return mu

N = 100_000_000
print(f"Sieving N={N}...", flush=True)
t0 = time.time()
mu = sieve(N)
print(f"  sieve done in {time.time()-t0:.0f}s")

t1 = time.time()
print("Computing partial sums for multiple s simultaneously...", flush=True)
s_list = [2.1, 2.25, 2.5, 2.75, 3.0, 3.5, 4.0, 5.0, 6.0]
sums = {s: 0.0 for s in s_list}
M_acc = 0
results = {str(s): {} for s in s_list}
checkpoints = [10**k for k in range(4, 9)] + [N]
for n in range(1, N+1):
    M_acc += mu[n]
    M_sq = M_acc * M_acc
    for s in s_list:
        sums[s] += M_sq / (n**s)
    if n in checkpoints:
        for s in s_list:
            results[str(s)][str(n)] = sums[s]
        print(f"  N={n:>10}: s=2.5={sums[2.5]:.10f}, s=3={sums[3.0]:.10f}, s=4={sums[4.0]:.10f}  t={time.time()-t1:.0f}s", flush=True)

print()
print("FINAL Σ M(n)²/n^s at N=10⁸:")
for s in s_list:
    print(f"  s = {s}: {sums[s]:.14f}")

# Test candidate closed forms
print()
print("Closed form candidates:")
import math
candidates_at_s = {
    3.0: {
        'ζ(3)/2': 1.20206/2,
        '12/π²': 12/math.pi**2,
        '1 + 1/π² + 1/12': 1 + 1/math.pi**2 + 1/12,
        '36·C·ζ(3)/(4·π²) — Tauberian guess': 36*0.66989*1.20206/(4*math.pi**2),
    },
    4.0: {
        'ζ(4)·ζ(2)/ζ(8)': (math.pi**4/90)*(math.pi**2/6)/(math.pi**8/9450),
        '6/π² · ζ(3)': 6/math.pi**2 * 1.20206,
    },
}
for s, candidates in candidates_at_s.items():
    print(f"  s={s} (value {sums[s]:.6f}):")
    for name, val in candidates.items():
        print(f"    {name} = {val:.6f}  (diff {val-sums[s]:+.6f})")

with open("/kaggle/working/mertens_varying_s.json", "w") as f:
    json.dump({
        "N": N,
        "sums_at_N": {str(s): v for s, v in sums.items()},
        "partial_sums": results,
        "elapsed_s": time.time() - t0,
    }, f, indent=2)
