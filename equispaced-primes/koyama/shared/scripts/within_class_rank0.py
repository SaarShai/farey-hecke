#!/usr/bin/env python3
"""Within-class universality test: rank-0 EC cluster.

Forms: 11a1, 14a1, 15a1, 17a1, 19a1, 20a1
200 zeros each, K=10^4, arithmetic ρ=1+iγ, μ_E(p²)=p.

Question: tight cluster (CV<20%) → within-class universality, publishable.
         spread → extra structure within rank class.

Output: RANK0_CLUSTER.json
"""

import json
import subprocess
from pathlib import Path

import mpmath as mp

mp.mp.dps = 50

EULER_GAMMA = mp.mpf("0.5772156649015328606065120900824024310421593359399235")
K = 10**4
T_MAX = 1000
N_ZEROS = 200
OUT_JSON = Path("/Users/saar/Desktop/Farey-Local/experiments/RANK0_CLUSTER.json")

RANK0_CURVES = [
    ("11a1",  11),
    ("14a1",  14),
    ("15a1",  15),
    ("17a1",  17),
    ("19a1",  19),
    ("20a1",  20),
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


def run_curve(curve: str, conductor: int) -> dict:
    print(f"\n=== {curve} (N={conductor}) ===", flush=True)

    zeros = fetch_zeros(curve, T_MAX)
    zeros = zeros[:N_ZEROS]
    print(f"  {len(zeros)} zeros", flush=True)

    if not zeros:
        return {"curve": curve, "conductor": conductor, "rank": 0,
                "E_C1": None, "E_C1_sq": None, "std_C1": None, "N_zeros": 0, "error": "no zeros"}

    ap = fetch_ap_table(curve, K)
    mu = build_mu_E(ap, K)

    lprimes = fetch_lprime_batch(curve, zeros)

    log_K = mp.log(K)
    denom = log_K + EULER_GAMMA

    C1_vals = []
    for g, Lp in zip(zeros, lprimes):
        cK = compute_cK(mu, g, K)
        C1 = float(abs(cK) * abs(Lp) / denom)
        C1_vals.append(C1)

    E_C1 = sum(C1_vals) / len(C1_vals)
    E_C1_sq = sum(v**2 for v in C1_vals) / len(C1_vals)
    variance = sum((v - E_C1)**2 for v in C1_vals) / len(C1_vals)
    std_C1 = variance**0.5
    cv = std_C1 / E_C1 if E_C1 > 0 else None

    print(f"  E[C1]={E_C1:.4f}  E[C1^2]={E_C1_sq:.4f}  std={std_C1:.4f}  CV={cv:.3f}", flush=True)

    return {
        "curve": curve,
        "conductor": conductor,
        "rank": 0,
        "E_C1": E_C1,
        "E_C1_sq": E_C1_sq,
        "std_C1": std_C1,
        "CV": cv,
        "N_zeros": len(zeros),
        "C1_vals": C1_vals,
        "error": None,
    }


def main():
    results = {}
    for curve, conductor in RANK0_CURVES:
        try:
            r = run_curve(curve, conductor)
        except Exception as e:
            print(f"ERROR on {curve}: {e}", flush=True)
            r = {"curve": curve, "conductor": conductor, "rank": 0,
                 "E_C1": None, "E_C1_sq": None, "std_C1": None, "N_zeros": 0, "error": str(e)}
        results[curve] = r

    # Summary stats
    valid = [v for v in results.values() if v["E_C1_sq"] is not None]
    if valid:
        all_E_C1_sq = [v["E_C1_sq"] for v in valid]
        mean_sq = sum(all_E_C1_sq) / len(all_E_C1_sq)
        var_sq = sum((x - mean_sq)**2 for x in all_E_C1_sq) / len(all_E_C1_sq)
        std_sq = var_sq**0.5
        cv_across = std_sq / mean_sq if mean_sq > 0 else None
        results["_summary"] = {
            "n_curves": len(valid),
            "mean_E_C1_sq": mean_sq,
            "std_E_C1_sq_across_curves": std_sq,
            "CV_across_curves": cv_across,
            "universality_holds_CV20": cv_across < 0.2 if cv_across else None,
        }
        print(f"\n=== SUMMARY ===", flush=True)
        print(f"E[C1^2] across rank-0: mean={mean_sq:.4f} std={std_sq:.4f} CV={cv_across:.3f}", flush=True)
        print(f"Within-class universality (CV<20%): {cv_across < 0.2 if cv_across else 'N/A'}", flush=True)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
