#!/usr/bin/env python3
"""Rank-3 anchor: 5077a1, 500 zeros at K=10^4, arithmetic ρ=1+iγ.

Output: RANK3_5077A1.json — same schema as PHASE1_EC_RECOMPUTE.json
"""

import json
import math
import subprocess
from pathlib import Path

import mpmath as mp

mp.mp.dps = 50

EULER_GAMMA = mp.mpf("0.5772156649015328606065120900824024310421593359399235")
K = 10**4
T_MAX = 2000   # need more T for 500 zeros of rank-3
N_ZEROS = 500
CURVE = "5077a1"
OUT_JSON = Path("/Users/saar/Desktop/Farey-Local/experiments/RANK3_5077A1.json")


def gp_eval(script: str, timeout: int = 7200) -> str:
    proc = subprocess.run(
        ["gp", "-q", "--default", "parisizemax=4G"],
        input=script,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gp failed: {proc.stderr[:500]}")
    return proc.stdout


def fetch_zeros(curve: str, tmax: int) -> list:
    script = f"""
    default(realprecision, 50);
    E = ellinit("{curve}");
    Z = lfunzeros(E, [1e-6, {tmax}]);
    for(i=1, #Z, print(Z[i]));
    """
    out = gp_eval(script)
    zeros = []
    for line in out.strip().splitlines():
        line = line.strip()
        if line:
            zeros.append(mp.mpf(line))
    return zeros


def fetch_ap_table(curve: str, nmax: int) -> dict:
    script = f"""
    default(realprecision, 50);
    E = ellinit("{curve}");
    forprime(p=2, {nmax}, print(p, " ", ellap(E, p)));
    """
    out = gp_eval(script)
    ap = {}
    for line in out.strip().splitlines():
        parts = line.split()
        if len(parts) == 2:
            ap[int(parts[0])] = int(parts[1])
    return ap


def sieve_primes(nmax: int) -> list:
    sieve = bytearray(b"\x01") * (nmax + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(nmax**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(range(i*i, nmax+1, i)))
    return [i for i in range(2, nmax+1) if sieve[i]]


def build_mu_E(ap: dict, nmax: int) -> list:
    """μ_E(p)=−a_p, μ_E(p²)=p, μ_E(p^k≥3)=0."""
    mu = [mp.mpf(0)] * (nmax + 1)
    mu[1] = mp.mpf(1)
    primes = sieve_primes(nmax)
    for p in primes:
        if p not in ap:
            continue
        pk, k = p, 1
        while pk <= nmax:
            val = mp.mpf(-ap[p]) if k == 1 else (mp.mpf(p) if k == 2 else mp.mpf(0))
            if val != 0:
                for m in range(1, nmax // pk + 1):
                    if m % p == 0:
                        continue
                    if mu[m] != 0:
                        mu[m * pk] = mu[m] * val
            pk *= p
            k += 1
    return mu


def compute_cK(mu: list, gamma, K_val: int):
    """c_K(1+iγ) = Σ_{n≤K} μ_E(n) exp(−n/K) n^{−(1+iγ)}."""
    K_mpf = mp.mpf(K_val)
    s = mp.mpc(0)
    for n in range(1, K_val + 1):
        m = mu[n]
        if m == 0:
            continue
        weight = mp.exp(-mp.mpf(n) / K_mpf)
        n_pow = mp.exp(mp.mpc(-1, -gamma) * mp.log(n))
        s += m * weight * n_pow
    return s


def fetch_lprime_batch(curve: str, gammas: list) -> list:
    gamma_str = ", ".join(mp.nstr(g, 40) for g in gammas)
    script = f"""
    default(realprecision, 50);
    E = ellinit("{curve}");
    gs = [{gamma_str}];
    for(i=1, #gs, v = lfun(E, 1 + I*gs[i], 1); print(real(v), " ", imag(v)));
    """
    out = gp_eval(script)
    vals = []
    for line in out.strip().splitlines():
        parts = line.split()
        if len(parts) == 2:
            vals.append(mp.mpc(mp.mpf(parts[0]), mp.mpf(parts[1])))
    return vals


def main():
    print(f"=== {CURVE} ===", flush=True)

    print("Fetching zeros...", flush=True)
    zeros = fetch_zeros(CURVE, T_MAX)
    print(f"  got {len(zeros)} zeros up to T={T_MAX}", flush=True)
    zeros = zeros[:N_ZEROS]
    print(f"  using {len(zeros)} zeros", flush=True)

    print(f"Fetching a_p table up to {K}...", flush=True)
    ap = fetch_ap_table(CURVE, K)
    print(f"  got {len(ap)} primes", flush=True)

    print("Building μ_E table...", flush=True)
    mu = build_mu_E(ap, K)

    print("Fetching L'(1+iγ) batch...", flush=True)
    lprimes = fetch_lprime_batch(CURVE, zeros)
    print(f"  got {len(lprimes)} L' values", flush=True)

    log_K = mp.log(K)
    denom = log_K + EULER_GAMMA

    C1_list = []
    cK_list = []
    Lp_list = []
    zero_list = []

    for idx, (g, Lp) in enumerate(zip(zeros, lprimes)):
        cK = compute_cK(mu, g, K)
        C1 = abs(cK) * abs(Lp) / denom
        C1_list.append(float(C1))
        cK_list.append([float(cK.real), float(cK.imag)])
        Lp_list.append([float(Lp.real), float(Lp.imag)])
        zero_list.append([1.0, float(g)])
        if idx < 5:
            print(f"  γ={float(g):.6f}  C1={float(C1):.4e}", flush=True)

    E_C1 = sum(C1_list) / len(C1_list)
    E_C1_sq = sum(v**2 for v in C1_list) / len(C1_list)
    print(f"\nE[C1] = {E_C1:.4f}", flush=True)
    print(f"E[C1^2] = {E_C1_sq:.4f}", flush=True)

    result = {
        CURVE: {
            "C1": C1_list,
            "Lprime": Lp_list,
            "c_K": cK_list,
            "zeros": zero_list,
            "E_C1": E_C1,
            "E_C1_sq": E_C1_sq,
            "N_zeros": len(zeros),
            "rank": 3,
            "conductor": 5077,
        }
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote {OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
