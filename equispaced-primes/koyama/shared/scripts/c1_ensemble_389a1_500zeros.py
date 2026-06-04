"""Heavy: 389a1 at K=50K across 500 zeros."""
import mpmath as mp, json, statistics, time, subprocess
from pathlib import Path
mp.mp.dps = 25
DATA_DIR = Path.home() / "farey_py_tasks" / "data"

# Need L'(ρ) for 389a1 at 500 zeros. Fetch if needed.
lp_path = DATA_DIR / "L_prime_389a1_500.json"
if not lp_path.exists():
    print("Fetching L'(389a1) via PARI...")
    script = r'''default(parisizemax, 4*10^9);
\p 40
E389 = ellinit([0,1,1,-2,0]);
L389 = lfuninit(E389, [1, 500]);
zz = lfunzeros(L389, 500);
for(i=1, #zz, rho = 1 + I*zz[i]; lp = lfun(L389, rho, 1); print("LP389 ", zz[i], " ", abs(lp)));
quit;
'''
    r = subprocess.run(["/opt/homebrew/bin/gp", "-q"], input=script, text=True, capture_output=True, timeout=1800)
    LP = {}
    for line in r.stdout.splitlines():
        p = line.split()
        if len(p) >= 3 and p[0] == "LP389": LP[p[1]] = p[2]
    with open(lp_path, "w") as f: json.dump(LP, f)
    print(f"Got {len(LP)} L' values")
else:
    with open(lp_path) as f: LP = json.load(f)

with open(DATA_DIR / "ap_389a1_500k.json") as f: AP = {int(k):v for k,v in json.load(f).items()}

K = 50000
N_cond = 389
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
    bad = N_cond % p == 0
    # μ_E(p)=-a_p, μ_E(p²)=p (from Euler factor 1-a_p x+p x²), μ_E(p^k)=0 k≥3
    v = -a if kpow==1 else (0 if bad else (p if kpow==2 else 0))
    if kpow > 2: v = 0
    mu[n] = mp.mpf(v) * mu[m]

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
        print(f"  {idx+1}/500: {time.time()-t0:.0f}s, running E[C₁²]={statistics.mean(v*v for v in vals):.4f}")

m = statistics.mean(vals); m2 = statistics.mean(v*v for v in vals)
print(f"\n389a1 K={K} N={len(vals)}: E[C₁]={m:.4f}, E[C₁²]={m2:.4f}")
print("DONE")
