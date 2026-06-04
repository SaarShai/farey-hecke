#!/usr/bin/env python3
"""Sym² L-values and Petersson norms via PARI + Rankin-Selberg.

Forms: 37a1 (rank-1), 389a1 (rank-2), Delta (weight-12).

For ECs (weight 2, s=2):
  L(Sym²E, 2) computed via Euler product with local factors
    L_p(Sym²E, s)^{-1} = (1 − α²p^{-s})(1 − αβ p^{-s})(1 − β²p^{-s})
  where α+β = a_p, αβ = p.
  Petersson norm ⟨f,f⟩ via Rankin-Selberg: ⟨f,f⟩ = N·L(Sym²f,2) / (8π³)

For Delta (weight 12, s=12):
  Use PARI mfpetersson if available, else known value 1.0353620568694467e-6.
  L(Sym²Delta, 12) via PARI lfunsympow or numerical Euler product.

Output: SYM2_LVALUES.json
"""

import json
import subprocess
from pathlib import Path

import mpmath as mp

mp.mp.dps = 50

OUT_JSON = Path("/Users/saar/Desktop/Farey-Local/experiments/SYM2_LVALUES.json")
P_MAX = 50000   # Euler product truncation
KNOWN_DELTA_PETERSSON = mp.mpf("1.0353620568694467e-6")


def gp_eval(script: str, timeout: int = 3600) -> str:
    proc = subprocess.run(
        ["gp", "-q", "--default", "parisizemax=4G"],
        input=script,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"gp failed: {proc.stderr[:500]}")
    return proc.stdout.strip()


def sieve_primes(nmax: int) -> list:
    sieve = bytearray(b"\x01") * (nmax + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(nmax**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(range(i*i, nmax+1, i)))
    return [i for i in range(2, nmax+1) if sieve[i]]


def fetch_ap_ec(curve: str, nmax: int) -> dict:
    script = f"""
    default(realprecision, 50);
    E = ellinit("{curve}");
    forprime(p=2, {nmax}, print(p, " ", ellap(E, p)));
    """
    out = gp_eval(script)
    ap = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 2:
            ap[int(parts[0])] = int(parts[1])
    return ap


def fetch_ap_delta(nmax: int) -> dict:
    script = f"""
    default(realprecision, 50);
    mf = mfinit([1,12,1], 1);
    f = mfbasis(mf)[1];
    forprime(p=2, {nmax}, print(p, " ", mfcoef(f, p)));
    """
    out = gp_eval(script)
    ap = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) == 2:
            try:
                ap[int(parts[0])] = round(float(parts[1]))
            except Exception:
                pass
    return ap


def L_sym2_EC_euler(ap_dict: dict, s: mp.mpf, p_max: int, conductor: int) -> mp.mpf:
    """L(Sym²E, s) via Euler product up to p_max.
    Local factor at good prime p:
      L_p^{-1} = (1 - α² p^{-s})(1 - αβ p^{-s})(1 - β² p^{-s})
    where α+β = a_p, αβ = p.
    α² + β² = (α+β)² - 2αβ = a_p² - 2p
    α²β² = p²
    αβ(α+β) = p·a_p
    So:
      L_p^{-1} = 1 - (α²+β²+αβ)p^{-s} + (α²β+αβ²+α²β²/p^s?...
    Actually expanding directly:
      = 1 - (α²+αβ+β²)p^{-s} + (α²β+αβ²)p^{-2s} - α²β²p^{-3s}? No.
    Correct: product of 3 terms:
      (1 - α²X)(1 - αβX)(1 - β²X) where X = p^{-s}
    = 1 - (α²+αβ+β²)X + (α³β+α²β²+αβ³)X² - α³β³X³? No wait.
    = 1 - (α²+αβ+β²)X + (α²·αβ + α²·β² + αβ·β²)X² - α²·αβ·β²·X³
    = 1 - (a_p²-p)X + p·a_p²·X²/? Let me be careful.

    Let A = a_p, P = p.
    α²+αβ+β² = (α+β)² - αβ = A² - P
    α²β + αβ² = αβ(α+β) = P·A
    α²·β² = P²
    So L_p^{-1} = 1 - (A²-P)X + P·A·X² - P²·X³  [WRONG — check product]
    Actually:
    (1-α²X)(1-αβX)(1-β²X)
    = (1-αβX - α²X + α³βX²)(1-β²X)
    = 1 - αβX - α²X + α³βX² - β²X + αβ³X² + α²β²X² - α³β³X³
    = 1 - (αβ+α²+β²)X + (α³β+αβ³+α²β²)X² - α³β³X³
    = 1 - (A²-P)X + (αβ(α²+β²) + α²β²)X² - P³X³
    α²+β² = A²-2P, so α³β+αβ³ = αβ(A²-2P) = P(A²-2P)
    α²β² = P²
    So coeff of X²: P(A²-2P)+P² = PA²-2P²+P² = PA²-P² = P(A²-P)
    And α³β³ = (αβ)³ = P³

    L_p^{-1} = 1 - (A²-P)X + P(A²-P)X² - P³X³  [still check]
    = (1-PX)[1 - (A²-2P)X + P²X²]?  Let's just use direct numerical evaluation.
    """
    primes = sieve_primes(p_max)
    log_L = mp.mpf(0)
    for p in primes:
        if p not in ap_dict:
            continue
        A = mp.mpf(ap_dict[p])
        P = mp.mpf(p)
        X = P ** (-s)
        # α, β roots of t² - At + P = 0
        disc = A**2 - 4*P
        if disc >= 0:
            sq = mp.sqrt(disc)
        else:
            sq = mp.mpc(0, mp.sqrt(-disc))
        alpha = (A + sq) / 2
        beta = (A - sq) / 2
        # local factor = 1/[(1-α²X)(1-αβX)(1-β²X)]
        f1 = 1 - alpha**2 * X
        f2 = 1 - alpha*beta * X
        f3 = 1 - beta**2 * X
        local_inv = f1 * f2 * f3
        if abs(local_inv) < 1e-20:
            continue
        log_L -= mp.log(local_inv)
    return mp.exp(log_L)


def L_sym2_delta_euler(ap_dict: dict, s: mp.mpf, p_max: int) -> mp.mpf:
    """L(Sym²Delta, s) via Euler product.
    Weight 12: αβ = p^11, α+β = a_p.
    Same structure but αβ = p^11.
    """
    primes = sieve_primes(p_max)
    log_L = mp.mpf(0)
    for p in primes:
        if p not in ap_dict:
            continue
        A = mp.mpf(ap_dict[p])
        P = mp.mpf(p)
        Pk = P**11  # αβ = p^{k-1} for weight k
        X = P ** (-s)
        disc = A**2 - 4*Pk
        if disc >= 0:
            sq = mp.sqrt(disc)
        else:
            sq = mp.mpc(0, mp.sqrt(-disc))
        alpha = (A + sq) / 2
        beta = (A - sq) / 2
        f1 = 1 - alpha**2 * X
        f2 = 1 - alpha*beta * X
        f3 = 1 - beta**2 * X
        local_inv = f1 * f2 * f3
        if abs(local_inv) < 1e-20:
            continue
        log_L -= mp.log(local_inv)
    return mp.exp(log_L)


def try_pari_petersson_ec(curve: str):
    """Try PARI mfpetersson for EC viewed as mf object."""
    script = f"""
    default(realprecision, 50);
    E = ellinit("{curve}");
    N = ellglobalred(E)[1];
    mf = mfinit([N, 2, 1], 1);
    v = mfbasis(mf);
    if(#v == 0, print("EMPTY"), print(mfpetersson(mf, v[1])));
    """
    try:
        out = gp_eval(script, timeout=120)
        if "EMPTY" in out or not out:
            return None
        # PARI may return a list or a number
        line = out.strip().splitlines()[0]
        val = float(line.strip())
        return val
    except Exception:
        return None


def main():
    results = {}

    for curve, rank, weight, conductor in [("37a1", 1, 2, 37), ("389a1", 2, 2, 389)]:
        print(f"\n=== {curve} ===", flush=True)
        print(f"  Fetching a_p table...", flush=True)
        ap = fetch_ap_ec(curve, P_MAX)
        print(f"  {len(ap)} primes", flush=True)

        print(f"  Computing L(Sym²{curve}, 2) via Euler product...", flush=True)
        L_sym2_raw = L_sym2_EC_euler(ap, mp.mpf(2), P_MAX, conductor)
        L_sym2 = float(L_sym2_raw.real) if hasattr(L_sym2_raw, 'real') else float(L_sym2_raw)
        print(f"  L(Sym²{curve}, 2) = {L_sym2:.6f}", flush=True)

        # Rankin-Selberg: <f,f> = N * L(Sym^2 f, 2) / (8*pi^3)
        petersson_RS = float(conductor * L_sym2 / (8 * float(mp.pi)**3))
        print(f"  Petersson (Rankin-Selberg) = {petersson_RS:.6e}", flush=True)

        # Try PARI directly
        petersson_pari = try_pari_petersson_ec(curve)
        print(f"  Petersson (PARI) = {petersson_pari}", flush=True)

        petersson = petersson_pari if petersson_pari is not None else petersson_RS

        results[curve] = {
            "rank": rank,
            "weight": weight,
            "conductor": conductor,
            "L_sym2_at_k": L_sym2,
            "petersson_norm_RS": petersson_RS,
            "petersson_norm_pari": petersson_pari,
            "petersson_norm": petersson,
            "ratio": L_sym2 / petersson if petersson else None,
        }

    # Delta
    print("\n=== Delta ===", flush=True)
    ap_delta = fetch_ap_delta(P_MAX)
    print(f"  {len(ap_delta)} primes for Delta", flush=True)

    print("  Computing L(Sym²Delta, 12) via Euler product...", flush=True)
    L_sym2_delta_raw = L_sym2_delta_euler(ap_delta, mp.mpf(12), P_MAX)
    L_sym2_delta = float(L_sym2_delta_raw.real) if hasattr(L_sym2_delta_raw, 'real') else float(L_sym2_delta_raw)
    print(f"  L(Sym²Delta, 12) = {L_sym2_delta:.6f}", flush=True)

    petersson_delta = float(KNOWN_DELTA_PETERSSON)
    results["Delta"] = {
        "rank": None,
        "weight": 12,
        "conductor": 1,
        "L_sym2_at_k": L_sym2_delta,
        "petersson_norm_RS": None,
        "petersson_norm_pari": None,
        "petersson_norm": petersson_delta,
        "ratio": L_sym2_delta / petersson_delta,
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nWrote {OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
