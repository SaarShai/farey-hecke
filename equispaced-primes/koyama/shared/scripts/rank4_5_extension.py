#!/usr/bin/env python3
"""Rank-4 and rank-5 EC extension — arithmetic normalization.

Modeled on phase1_ec_recompute.py helpers.
Tries several rank-4 candidates from LMFDB rank tables:
  - 234446a1 (rank 4)
  - 214850b1 (rank 4)
  - 19747a1  (rank 4)
  - 5765760a1 (rank 4, large conductor — try last)
Rank-5 candidate: skip unless pari confirms it quickly.

Uses ellinit("label") — pari-elldata must be installed.
For each valid curve: 200 zeros at K=10^4, arithmetic rho=1+i*gamma, correct mu_E.
Output: /Users/saar/Desktop/Farey-Local/experiments/RANK_EXTENSION.json
Schema: {label: {rank, conductor, E_C1, E_C1_sq, N_zeros, C1_list}}
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
T_MAX = 2000          # need ~200 zeros; rank-4 zeros may be spaced
TARGET_N = 200
SANITY_N = 5
OUT_PATH = Path("/Users/saar/Desktop/Farey-Local/experiments/RANK_EXTENSION.json")

# Rank-4 candidates (label, expected_rank)
RANK4_CANDIDATES = [
    "234446a1",
    "214850b1",
    "19747a1",
]
# Rank-5: known difficult; try known LMFDB rank-5 smallest conductor
RANK5_CANDIDATES = [
    "19047851a1",  # one of smallest rank-5 conductors from LMFDB
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


def verify_curve(label: str) -> tuple[bool, int, int]:
    """Return (valid, rank, conductor) or (False, 0, 0) if label unknown."""
    script = f"""
    default(realprecision, 50);
    E = ellinit("{label}");
    if(#E == 0, print("INVALID"); quit());
    N = ellglobalred(E)[1];
    r = ellanalyticrank(E)[1];
    print("VALID ", r, " ", N);
    """
    try:
        out = gp_eval(script, timeout=300)
    except Exception as e:
        print(f"  [{label}] verify failed: {e}", flush=True)
        return False, 0, 0
    for line in out.strip().splitlines():
        if line.startswith("VALID"):
            parts = line.split()
            return True, int(parts[1]), int(parts[2])
        if line.strip() == "INVALID":
            return False, 0, 0
    return False, 0, 0


def fetch_zeros(label: str, tmax: int) -> list:
    script = f"""
    default(realprecision, 50);
    E = ellinit("{label}");
    Z = lfunzeros(E, [1e-6, {tmax}]);
    for(i=1, #Z, print(Z[i]));
    """
    out = gp_eval(script, timeout=3600)
    zeros = []
    for line in out.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            zeros.append(mp.mpf(line))
        except Exception:
            pass
    return zeros


def fetch_ap_table(label: str, nmax: int) -> dict:
    script = f"""
    default(realprecision, 50);
    E = ellinit("{label}");
    forprime(p=2, {nmax}, print(p, " ", ellap(E, p)));
    """
    out = gp_eval(script, timeout=600)
    ap = {}
    for line in out.strip().splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        try:
            ap[int(parts[0])] = int(parts[1])
        except Exception:
            pass
    return ap


def fetch_lprime_batch(label: str, gammas: list) -> list:
    gamma_str = ", ".join(mp.nstr(g, 40) for g in gammas)
    script = f"""
    default(realprecision, 50);
    E = ellinit("{label}");
    gs = [{gamma_str}];
    for(i=1, #gs, v = lfun(E, 1 + I*gs[i], 1); print(real(v), " ", imag(v)));
    """
    out = gp_eval(script, timeout=3600)
    vals = []
    for line in out.strip().splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        try:
            vals.append(mp.mpc(mp.mpf(parts[0]), mp.mpf(parts[1])))
        except Exception:
            pass
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
    """mu_E(p)=-a_p, mu_E(p^2)=p, mu_E(p^k>=3)=0, mu_E(1)=1."""
    mu = [mp.mpf(0)] * (nmax + 1)
    mu[1] = mp.mpf(1)
    primes = sieve_primes(nmax)
    for p in primes:
        pk = p
        k = 1
        while pk <= nmax:
            if k == 1:
                val = mp.mpf(-ap.get(p, 0))
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


def run_curve(label: str, rank: int, conductor: int) -> dict:
    print(f"\n=== {label} (rank {rank}, N={conductor}) ===", flush=True)

    print(f"  fetching zeros up to T={T_MAX}...", flush=True)
    zeros = fetch_zeros(label, T_MAX)
    print(f"  fetched {len(zeros)} zeros", flush=True)
    if len(zeros) < 10:
        # try larger T
        print(f"  too few zeros, retrying with T=5000...", flush=True)
        zeros = fetch_zeros(label, 5000)
        print(f"  fetched {len(zeros)} zeros at T=5000", flush=True)

    zeros = zeros[:TARGET_N]
    print(f"  using {len(zeros)} zeros", flush=True)
    if len(zeros) == 0:
        return {"error": "no zeros found", "rank": rank, "conductor": conductor}

    print(f"  fetching a_p table...", flush=True)
    ap = fetch_ap_table(label, K)
    print(f"  got {len(ap)} primes", flush=True)

    print(f"  building mu_E...", flush=True)
    mu = build_mu_E(ap, K)

    print(f"  fetching L' batch ({len(zeros)} zeros)...", flush=True)
    lprimes = fetch_lprime_batch(label, zeros)

    log_K = mp.log(K)
    denom = log_K + EULER_GAMMA

    C1_list = []
    for idx, (g, Lp) in enumerate(zip(zeros, lprimes)):
        cK = compute_cK(mu, g, K)
        C1 = float(abs(cK) * abs(Lp) / denom)
        C1_list.append(C1)
        if idx < SANITY_N:
            print(f"  gamma={float(g):.6f}  |c_K|={float(abs(cK)):.4e}  |L'|={float(abs(Lp)):.4e}  C1={C1:.4e}", flush=True)

    n = len(C1_list)
    mean_c1 = sum(C1_list) / n
    mean_c1_sq = sum(x**2 for x in C1_list) / n
    print(f"  E[C1]={mean_c1:.4f}  E[C1^2]={mean_c1_sq:.4f}  N={n}", flush=True)

    return {
        "rank": rank,
        "conductor": conductor,
        "N_zeros": n,
        "E_C1": mean_c1,
        "E_C1_sq": mean_c1_sq,
        "C1_list": C1_list,
    }


def main():
    results = {}

    # Load existing results if any
    if OUT_PATH.exists():
        with open(OUT_PATH) as f:
            results = json.load(f)
        print(f"Loaded {len(results)} existing results", flush=True)

    all_candidates = [(label, 4) for label in RANK4_CANDIDATES] + \
                     [(label, 5) for label in RANK5_CANDIDATES]

    for label, expected_rank in all_candidates:
        if label in results:
            print(f"Skipping {label} (already done)", flush=True)
            continue

        print(f"\nVerifying {label}...", flush=True)
        valid, rank, conductor = verify_curve(label)
        if not valid:
            print(f"  SKIPPED: label {label} not found in pari-elldata", flush=True)
            results[label] = {"error": "label not found", "expected_rank": expected_rank}
            with open(OUT_PATH, "w") as f:
                json.dump(results, f, indent=2)
            continue

        print(f"  confirmed: rank={rank}, conductor={conductor}", flush=True)
        if rank != expected_rank:
            print(f"  WARNING: expected rank {expected_rank}, got {rank}", flush=True)

        try:
            res = run_curve(label, rank, conductor)
            results[label] = res
        except Exception as e:
            print(f"  ERROR on {label}: {e}", flush=True)
            results[label] = {"error": str(e), "rank": rank, "conductor": conductor}

        # Save after each curve
        with open(OUT_PATH, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Saved results to {OUT_PATH}", flush=True)

    print(f"\n=== DONE. {len(results)} entries in {OUT_PATH} ===", flush=True)


if __name__ == "__main__":
    main()
