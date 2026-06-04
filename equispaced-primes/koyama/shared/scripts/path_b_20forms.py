#!/usr/bin/env python3
"""Path B: 20-form E[C₁²] regression across rank/weight/conductor.

Forms:
  rank-0 ECs: 11a1, 14a1, 15a1, 17a1, 19a1, 20a1, 21a1, 24a1
  rank-1 ECs: 37a1, 43a1, 53a1, 57a1, 58a1, 61a1
  rank-2 ECs: 389a1, 433a1, 446d1, 571b1
  rank-3 EC:  5077a1
  Weight-12:  Delta (modular discriminant)

Output: PATH_B_20FORMS.csv
"""

import csv
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
N_ZEROS = 200
OUT_CSV = Path("/Users/saar/Desktop/Farey-Local/experiments/PATH_B_20FORMS.csv")

# (label, rank, weight, conductor)
FORMS = [
    ("11a1",   0, 2,  11),
    ("14a1",   0, 2,  14),
    ("15a1",   0, 2,  15),
    ("17a1",   0, 2,  17),
    ("19a1",   0, 2,  19),
    ("20a1",   0, 2,  20),
    ("21a1",   0, 2,  21),
    ("24a1",   0, 2,  24),
    ("37a1",   1, 2,  37),
    ("43a1",   1, 2,  43),
    ("53a1",   1, 2,  53),
    ("57a1",   1, 2,  57),
    ("58a1",   1, 2,  58),
    ("61a1",   1, 2,  61),
    ("389a1",  2, 2, 389),
    ("433a1",  2, 2, 433),
    ("446d1",  2, 2, 446),
    ("571b1",  2, 2, 571),
    ("5077a1", 3, 2, 5077),
    ("Delta", -1, 12, 1),   # rank=-1 means weight-12
]


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


def fetch_zeros_ec(curve: str, tmax: int) -> list:
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


def fetch_zeros_delta(tmax: int) -> list:
    """Zeros of L(Delta, s) — imaginary parts of nontrivial zeros."""
    script = f"""
    default(realprecision, 50);
    mf = mfinit([1,12,1], 1);
    f = mfbasis(mf)[1];
    lf = lfuninit(mflfun(mf, f), [{tmax}]);
    Z = lfunzeros(lf, [1e-6, {tmax}]);
    for(i=1, #Z, print(Z[i]));
    """
    out = gp_eval(script)
    zeros = []
    for line in out.strip().splitlines():
        line = line.strip()
        if line:
            try:
                zeros.append(mp.mpf(line))
            except Exception:
                pass
    return zeros


def fetch_ap_ec(curve: str, nmax: int) -> dict:
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


def fetch_af_delta(nmax: int) -> dict:
    """Return a_p for Delta (weight-12 cusp form) for primes p <= nmax."""
    script = f"""
    default(realprecision, 50);
    mf = mfinit([1,12,1], 1);
    f = mfbasis(mf)[1];
    forprime(p=2, {nmax}, print(p, " ", mfcoef(f, p)));
    """
    out = gp_eval(script)
    ap = {}
    for line in out.strip().splitlines():
        parts = line.split()
        if len(parts) == 2:
            try:
                ap[int(parts[0])] = round(float(parts[1]))
            except Exception:
                pass
    return ap


def sieve_primes(nmax: int) -> list:
    sieve = bytearray(b"\x01") * (nmax + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(nmax**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(range(i*i, nmax+1, i)))
    return [i for i in range(2, nmax+1) if sieve[i]]


def build_mu_EC(ap: dict, nmax: int) -> list:
    """μ_E: μ(p)=−a_p, μ(p²)=p, μ(p^k≥3)=0."""
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


def build_mu_delta(ap: dict, nmax: int) -> list:
    """μ_Delta: μ(p)=−a_p, μ(p²)=p^11, μ(p^k≥3)=0."""
    mu = [mp.mpf(0)] * (nmax + 1)
    mu[1] = mp.mpf(1)
    primes = sieve_primes(nmax)
    for p in primes:
        if p not in ap:
            continue
        pk, k = p, 1
        while pk <= nmax:
            val = mp.mpf(-ap[p]) if k == 1 else (mp.mpf(p**11) if k == 2 else mp.mpf(0))
            if val != 0:
                for m in range(1, nmax // pk + 1):
                    if m % p == 0:
                        continue
                    if mu[m] != 0:
                        mu[m * pk] = mu[m] * val
            pk *= p
            k += 1
    return mu


def compute_cK(mu: list, gamma, K_val: int, rho_real: float):
    """c_K(ρ) = Σ_{n≤K} μ(n) exp(−n/K) n^{−ρ}, ρ = rho_real + iγ."""
    K_mpf = mp.mpf(K_val)
    s = mp.mpc(0)
    neg_re = mp.mpf(-rho_real)
    for n in range(1, K_val + 1):
        m = mu[n]
        if m == 0:
            continue
        ln_n = mp.log(n)
        weight = mp.exp(-mp.mpf(n) / K_mpf)
        n_pow = mp.exp((neg_re - mp.mpc(0, gamma)) * ln_n)
        s += m * weight * n_pow
    return s


def fetch_lprime_ec(curve: str, gammas: list) -> list:
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


def fetch_lprime_delta(gammas: list) -> list:
    """L'(6+iγ, Delta) for each gamma."""
    gamma_str = ", ".join(mp.nstr(g, 40) for g in gammas)
    script = f"""
    default(realprecision, 50);
    mf = mfinit([1,12,1], 1);
    f = mfbasis(mf)[1];
    lf = lfuninit(mflfun(mf, f), [1000]);
    gs = [{gamma_str}];
    for(i=1, #gs, v = lfun(lf, 6 + I*gs[i], 1); print(real(v), " ", imag(v)));
    """
    out = gp_eval(script)
    vals = []
    for line in out.strip().splitlines():
        parts = line.split()
        if len(parts) == 2:
            vals.append(mp.mpc(mp.mpf(parts[0]), mp.mpf(parts[1])))
    return vals


def run_form(label: str, rank: int, weight: int, conductor: int) -> dict:
    print(f"\n=== {label} (rank={rank}, wt={weight}, N={conductor}) ===", flush=True)

    is_delta = (label == "Delta")
    rho_real = 6.0 if is_delta else 1.0

    # Fetch zeros
    if is_delta:
        zeros = fetch_zeros_delta(T_MAX)
    else:
        zeros = fetch_zeros_ec(label, T_MAX)

    zeros = zeros[:N_ZEROS]
    print(f"  using {len(zeros)} zeros", flush=True)
    if len(zeros) == 0:
        return {"label": label, "rank": rank, "weight": weight, "conductor": conductor,
                "E_C1": None, "E_C1_sq": None, "N_zeros": 0, "error": "no zeros"}

    # Fetch ap table
    if is_delta:
        ap = fetch_af_delta(K)
        mu = build_mu_delta(ap, K)
    else:
        ap = fetch_ap_ec(label, K)
        mu = build_mu_EC(ap, K)

    print(f"  built mu table, {len(ap)} primes", flush=True)

    # Fetch L'
    if is_delta:
        lprimes = fetch_lprime_delta(zeros)
    else:
        lprimes = fetch_lprime_ec(label, zeros)

    print(f"  fetched {len(lprimes)} L' values", flush=True)

    log_K = mp.log(K)
    denom = log_K + EULER_GAMMA

    C1_vals = []
    for idx, (g, Lp) in enumerate(zip(zeros, lprimes)):
        cK = compute_cK(mu, g, K, rho_real)
        C1 = float(abs(cK) * abs(Lp) / denom)
        C1_vals.append(C1)
        if idx < 3:
            print(f"    γ={float(g):.4f} C1={C1:.4e}", flush=True)

    E_C1 = sum(C1_vals) / len(C1_vals)
    E_C1_sq = sum(v**2 for v in C1_vals) / len(C1_vals)
    print(f"  E[C1]={E_C1:.4f}  E[C1^2]={E_C1_sq:.4f}", flush=True)

    return {
        "label": label,
        "rank": rank,
        "weight": weight,
        "conductor": conductor,
        "E_C1": E_C1,
        "E_C1_sq": E_C1_sq,
        "N_zeros": len(zeros),
        "error": None,
    }


def main():
    rows = []
    for label, rank, weight, conductor in FORMS:
        try:
            row = run_form(label, rank, weight, conductor)
        except Exception as e:
            print(f"  ERROR on {label}: {e}", flush=True)
            row = {"label": label, "rank": rank, "weight": weight, "conductor": conductor,
                   "E_C1": None, "E_C1_sq": None, "N_zeros": 0, "error": str(e)}
        rows.append(row)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["label", "rank", "weight", "conductor",
                                                "E_C1", "E_C1_sq", "N_zeros", "error"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {OUT_CSV}", flush=True)


if __name__ == "__main__":
    main()
