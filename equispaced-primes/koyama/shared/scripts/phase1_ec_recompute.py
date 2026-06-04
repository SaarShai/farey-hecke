#!/usr/bin/env python3
"""Phase 1 EC rerun — arithmetic normalization for 37a1 and 389a1.

Fixes prior bug where analytic ρ=0.5+iγ was combined with arithmetic μ_E
coefficients, producing garbage (E[C₁²]~10⁸). This script uses ρ=1+iγ with
arithmetic μ_E throughout.

Output: /Users/saar/Desktop/Farey-Local/experiments/PHASE1_EC_RECOMPUTE.json
"""

import json
import math
import subprocess
import sys
from pathlib import Path

import mpmath as mp

mp.mp.dps = 50

EULER_GAMMA = mp.mpf("0.5772156649015328606065120900824024310421593359399235")
K = 10**4
T_MAX = 1000
SANITY_N = 10
TARGET_N = 500
CURVES = ["37a1", "389a1"]
OUT_PATH = Path("/Users/saar/Desktop/Farey-Local/experiments/PHASE1_EC_RECOMPUTE.json")


def gp_eval(script: str) -> str:
    """Run a PARI/GP script and return stdout."""
    proc = subprocess.run(
        ["gp", "-q", "--default", "parisizemax=4G"],
        input=script,
        capture_output=True,
        text=True,
        timeout=3600,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gp failed: {proc.stderr}")
    return proc.stdout


def fetch_zeros(curve: str, tmax: int) -> list:
    """Return imaginary parts of nontrivial zeros with 0 < Im(ρ) <= tmax."""
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
        if not line:
            continue
        zeros.append(mp.mpf(line))
    return zeros


def fetch_ap_table(curve: str, nmax: int) -> dict:
    """Return dict {p: a_p} for primes p <= nmax using ellap."""
    script = f"""
    default(realprecision, 50);
    E = ellinit("{curve}");
    forprime(p=2, {nmax}, print(p, " ", ellap(E, p)));
    """
    out = gp_eval(script)
    ap = {}
    for line in out.strip().splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        ap[int(parts[0])] = int(parts[1])
    return ap


def fetch_lprime_batch(curve: str, gammas: list) -> list:
    """Return L'(1+i*gamma, E) as list of (re, im) mpc for each gamma."""
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
        if len(parts) != 2:
            continue
        vals.append(mp.mpc(mp.mpf(parts[0]), mp.mpf(parts[1])))
    if len(vals) != len(gammas):
        raise RuntimeError(f"Lprime count mismatch: got {len(vals)} expected {len(gammas)}")
    return vals


def sieve_primes(nmax: int) -> list:
    sieve = bytearray(b"\x01") * (nmax + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(nmax**0.5) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:nmax + 1:step] = bytearray(len(range(start, nmax + 1, step)))
    return [i for i in range(2, nmax + 1) if sieve[i]]


def build_mu_E(ap: dict, nmax: int) -> list:
    """Build μ_E(n) for n=1..nmax via multiplicativity.
    μ_E(p)=−a_p, μ_E(p²)=p, μ_E(p^k≥3)=0, μ_E(1)=1.
    """
    mu = [mp.mpf(0)] * (nmax + 1)
    mu[1] = mp.mpf(1)
    primes = sieve_primes(nmax)
    for p in primes:
        pk = p
        k = 1
        while pk <= nmax:
            if k == 1:
                val = mp.mpf(-ap[p])
            elif k == 2:
                val = mp.mpf(p)
            else:
                val = mp.mpf(0)
            if val != 0:
                limit = nmax // pk
                for m in range(1, limit + 1):
                    if m % p == 0:
                        continue
                    mm = mu[m]
                    if mm == 0:
                        continue
                    mu[m * pk] = mm * val
            pk *= p
            k += 1
    return mu


def compute_cK(mu: list, gamma, K_val: int):
    """c_K(ρ,E) = Σ_{n≤K} μ_E(n) exp(−n/K) n^{−(1+iγ)}."""
    K_mpf = mp.mpf(K_val)
    s = mp.mpc(0)
    neg_s = mp.mpc(-1, -gamma)
    for n in range(1, K_val + 1):
        m = mu[n]
        if m == 0:
            continue
        weight = mp.e ** (-mp.mpf(n) / K_mpf)
        term = m * weight * mp.e ** (neg_s * mp.log(n))
        s += term
    return s


def run_curve(curve: str, n_zeros_target: int) -> dict:
    print(f"\n=== {curve} ===", flush=True)
    zeros = fetch_zeros(curve, T_MAX)
    print(f"fetched {len(zeros)} zeros up to T={T_MAX}", flush=True)
    zeros = zeros[:n_zeros_target]
    print(f"using first {len(zeros)} zeros", flush=True)

    print(f"fetching a_p table up to {K}...", flush=True)
    ap = fetch_ap_table(curve, K)
    print(f"got {len(ap)} primes", flush=True)

    print("building μ_E(n) table...", flush=True)
    mu = build_mu_E(ap, K)

    print("fetching L'(1+iγ) batch...", flush=True)
    lprimes = fetch_lprime_batch(curve, zeros)

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
        zero_list.append([float(mp.mpf(1)), float(g)])
        if idx < SANITY_N:
            print(f"  γ={float(g):.6f}  |c_K|={float(abs(cK)):.4e}  |L'|={float(abs(Lp)):.4e}  C1={float(C1):.4e}", flush=True)

    return {
        "C1": C1_list,
        "Lprime": Lp_list,
        "c_K": cK_list,
        "zeros": zero_list,
    }


def main():
    results = {}

    print("\n### SANITY GATE: 37a1 first 10 zeros ###", flush=True)
    sanity = run_curve("37a1", SANITY_N)
    mean_C1 = sum(sanity["C1"]) / len(sanity["C1"])
    print(f"\nMean C1 over first {SANITY_N} zeros: {mean_C1:.4f}", flush=True)
    if not (0.3 <= mean_C1 <= 3.0):
        print("FAIL: normalization likely still wrong", flush=True)
        sys.exit(1)
    print("PASS: proceeding to full 500 zeros", flush=True)

    for curve in CURVES:
        results[curve] = run_curve(curve, TARGET_N)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nwrote {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
