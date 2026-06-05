"""Test per-zero NDC convergence in K. This is the TRUE NDC test.
At each fixed zero ρ, compute D_K·ζ(2) for K = 1K, 2K, 5K, 10K, 20K.
If individual value → 1 as K grows, NDC confirmed for that zero."""
import mpmath as mp, json, time
from pathlib import Path
mp.mp.dps = 30

DATA_DIR = Path.home() / "farey_py_tasks" / "data"
with open(DATA_DIR / "ap_37a1_ext.json") as f: AP_37 = {int(k):v for k,v in json.load(f).items()}
with open(DATA_DIR / "ap_389a1_ext.json") as f: AP_389 = {int(k):v for k,v in json.load(f).items()}
with open(DATA_DIR / "tau_delta_ext.json") as f: TAU = {int(k):v for k,v in json.load(f).items()}

zeta2 = mp.zeta(2)

def build_mu(K, ap_dict, is_delta, curve_N=None):
    primes_list = sorted(ap_dict.keys())
    spf = list(range(K+1))
    for p in primes_list:
        if p*p > K: break
        if spf[p] == p:
            for m in range(p*p, K+1, p):
                if spf[m] == m: spf[m] = p
    mu = [mp.mpf(0)]*(K+1); mu[1] = mp.mpf(1)
    for n in range(2, K+1):
        p = spf[n]
        if p not in ap_dict: continue
        m = n; kpow = 0
        while m % p == 0: m //= p; kpow += 1
        ap = ap_dict[p]
        if is_delta:
            if kpow == 1: mupk = -ap
            elif kpow == 2: mupk = ap*ap - p**11
            else: mupk = 0
        else:
            bad = (curve_N % p == 0) if curve_N else False
            if kpow == 1: mupk = -ap
            elif kpow == 2: mupk = 0 if bad else ap*ap - p
            else: mupk = 0
        mu[n] = mp.mpf(mupk) * mu[m]
    return mu, primes_list

def ndc_at_rho(rho, K, data, is_delta, curve_N):
    """Compute |c_K · E_K|·ζ(2) at given ρ, K."""
    mu, primes_list = build_mu(K, data, is_delta, curve_N)
    c_K = mp.mpc(0)
    exp_rate = mp.mpf(1)/K
    for n in range(1, K+1):
        if mu[n] != 0:
            c_K += mu[n] * mp.exp(-mp.mpf(n)*exp_rate) / mp.power(n, rho)
    E_K = mp.mpc(1)
    for p in primes_list:
        if p > 5*K: break
        v = data[p]
        bad = (curve_N % p == 0) if (curve_N and not is_delta) else False
        if is_delta:
            E_K /= (1 - mp.mpf(v)/mp.power(p, rho) + mp.power(p, 11 - 2*rho))
        elif bad:
            E_K /= (1 - mp.mpf(v)/mp.power(p, rho))
        else:
            E_K /= (1 - mp.mpf(v)/mp.power(p, rho) + 1/mp.power(p, 2*rho - 1))
    return abs(c_K * E_K) * zeta2

# Pick specific zeros from each L-function
test_cases = [
    # (label, ρ, data, is_delta, curve_N)
    ("37a1 γ_2=5.003",  mp.mpc(1, mp.mpf('5.00317001400665869534627315571')), AP_37, False, 37),
    ("37a1 γ_7=15.60",  mp.mpc(1, mp.mpf('15.60385787320431886505786442681')), AP_37, False, 37),
    ("389a1 γ_3=2.876", mp.mpc(1, mp.mpf('2.87609907126046520176342609472')), AP_389, False, 389),
    ("389a1 γ_10=10.35",mp.mpc(1, mp.mpf('10.35143331288149667136655977862')), AP_389, False, 389),
    ("Δ γ_1=9.22",     mp.mpc(6, mp.mpf('9.22237939992110252224376719274')), TAU, True, None),
    ("Δ γ_8=28.83",    mp.mpc(6, mp.mpf('28.83168262418687544502196191298')), TAU, True, None),
]

print("="*80)
print("PER-ZERO K-CONVERGENCE — Test if individual ρ gives |D_K|·ζ(2) → 1 as K grows")
print("="*80)

Ks = [1000, 2000, 5000, 10000, 20000]
print(f"\n{'Zero':>22} | " + " | ".join(f"K={K}" for K in Ks))
print("-" * (22 + 4 + len(Ks)*14))
for label, rho, data, is_delta, N in test_cases:
    row = [f"{label:>22}"]
    for K in Ks:
        if K > 50000:
            row.append("skip")
            continue
        t0 = time.time()
        v = ndc_at_rho(rho, K, data, is_delta, N)
        row.append(f"{float(v):>10.4f}")
    print(" | ".join(row))

print("\nDONE")
