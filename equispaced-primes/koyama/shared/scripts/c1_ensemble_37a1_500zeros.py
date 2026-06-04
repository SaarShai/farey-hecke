"""Heavy: C₁ at 1000 zeros of 37a1 at K=50,000. Takes ~30+ min.
BUGFIX 2026-04-20: μ_E(p²) corrected to p (Euler factor coeff), was wrongly a_p²-p=a_{p²}.
"""
import mpmath as mp, json, statistics, time
from pathlib import Path
mp.mp.dps = 25
DATA_DIR = Path.home() / "farey_py_tasks" / "data"
with open(DATA_DIR / "ap_37a1_500k.json") as f: AP = {int(k):v for k,v in json.load(f).items()}
with open(DATA_DIR / "L_prime_500.json") as f: LP = json.load(f)["37a1"]

K = 50000
primes_list = sorted(AP.keys())
spf = list(range(K+1))
for p in primes_list:
    if p*p > K: break
    if spf[p] == p:
        for m in range(p*p, K+1, p):
            if spf[m] == m: spf[m] = p
mu = [mp.mpf(0)]*(K+1); mu[1]=mp.mpf(1)
for n in range(2, K+1):
    p = spf[n]
    if p not in AP: continue
    m = n; kpow = 0
    while m % p == 0: m //= p; kpow += 1
    a = AP[p]
    bad = 37 % p == 0
    # μ_E(p)=-a_p, μ_E(p²)=p (from Euler factor 1-a_p x+p x²), μ_E(p^k)=0 k≥3
    v = -a if kpow==1 else (0 if bad else (p if kpow==2 else 0))
    if kpow > 2: v = 0
    mu[n] = mp.mpf(v) * mu[m]
print(f"μ table built for K={K}")

vals = []
exp_rate = mp.mpf(1)/K
t0 = time.time()
for idx, (g_str, lp_str) in enumerate(LP.items()):
    if idx >= 500: break
    g = mp.mpf(g_str); lp = mp.mpf(lp_str)
    rho = mp.mpc(1, g)
    c_K = mp.mpc(0)
    for n in range(1, K+1):
        if mu[n] != 0:
            c_K += mu[n] * mp.exp(-mp.mpf(n)*exp_rate) / mp.power(n, rho)
    C1 = abs(c_K) * lp / (mp.log(K) + mp.euler)
    vals.append(float(C1))
    if (idx+1) % 50 == 0:
        print(f"  {idx+1}/500: {time.time()-t0:.0f}s, running mean C₁²={statistics.mean(v*v for v in vals):.4f}")
m = statistics.mean(vals); m2 = statistics.mean(v*v for v in vals)
print(f"\nK={K}, N={len(vals)}: E[C₁]={m:.4f}, E[C₁²]={m2:.4f}")
print("DONE")
