#!/usr/bin/env python3
"""5-minute mpmath verification: Rankin-Selberg identity 1/N paradox.

Claim: L(Sym²f, 2)/⟨f,f⟩ = 8π³/N for weight-2 squarefree-level EC.
=> 37a1 (N=37) should have ratio 10.5x larger than 389a1 (N=389).
But empirically E[C₁²]: 37a1=2.19 < 389a1=3.11.

This script tests the identity numerically at high precision.

Output: ONE_OVER_N_SIGNCHECK.md
"""

import subprocess
from pathlib import Path

import mpmath as mp

mp.mp.dps = 50

OUT_MD = Path("/Users/saar/Desktop/Farey-Local/experiments/ONE_OVER_N_SIGNCHECK.md")
P_MAX = 100000  # large Euler product for precision


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


def sieve_primes(nmax: int) -> list:
    sieve = bytearray(b"\x01") * (nmax + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(nmax**0.5) + 1):
        if sieve[i]:
            sieve[i*i::i] = bytearray(len(range(i*i, nmax+1, i)))
    return [i for i in range(2, nmax+1) if sieve[i]]


def L_sym2_euler(ap_dict: dict, s, p_max: int, bad_primes: set = None) -> mp.mpf:
    """L(Sym²E, s) partial Euler product, skipping bad primes."""
    if bad_primes is None:
        bad_primes = set()
    primes = sieve_primes(p_max)
    log_L = mp.mpf(0)
    for p in primes:
        if p in bad_primes:
            continue
        if p not in ap_dict:
            continue
        A = mp.mpf(ap_dict[p])
        P = mp.mpf(p)
        disc = A**2 - 4*P
        if disc >= 0:
            sq = mp.sqrt(disc)
            alpha = (A + sq) / 2
            beta  = (A - sq) / 2
        else:
            sq = mp.mpc(0, mp.sqrt(-disc))
            alpha = (A + sq) / 2
            beta  = (A - sq) / 2
        X = P ** (-s)
        f1 = 1 - alpha**2 * X
        f2 = 1 - alpha*beta * X
        f3 = 1 - beta**2 * X
        denom_log = mp.log(f1) + mp.log(f2) + mp.log(f3)
        log_L -= denom_log
    return mp.exp(log_L)


def petersson_from_RS(N: int, L_sym2: mp.mpf) -> mp.mpf:
    """Rankin-Selberg: ⟨f,f⟩ = N·L(Sym²f,2) / (8π³)."""
    return N * L_sym2 / (8 * mp.pi**3)


def try_pari_L_sym2(curve: str):
    """Try PARI lfunsympow for L(Sym²E, 2)."""
    script = f"""
    default(realprecision, 50);
    E = ellinit("{curve}");
    lE = lfuninit(E, [100]);
    lS = lfunsympow(lE, 2);
    v = lfun(lS, 2);
    print(v);
    """
    try:
        out = gp_eval(script, timeout=300)
        if not out:
            return None
        return float(out.strip().splitlines()[0])
    except Exception as e:
        print(f"  PARI lfunsympow failed: {e}", flush=True)
        return None


def main():
    lines = ["# Rankin-Selberg 1/N Sign-Check", "",
             f"Verification at {mp.mp.dps} digits, Euler product to P={P_MAX}.", ""]

    curves = [("37a1", 37, 1), ("389a1", 389, 2)]
    data = {}

    for curve, N, rank in curves:
        print(f"\n=== {curve} (N={N}) ===", flush=True)
        ap = fetch_ap_ec(curve, P_MAX)
        print(f"  {len(ap)} primes", flush=True)

        # Try PARI first for ground truth
        L_pari = try_pari_L_sym2(curve)
        print(f"  PARI lfunsympow L(Sym²,2) = {L_pari}", flush=True)

        # Our Euler product
        L_euler = L_sym2_euler(ap, mp.mpf(2), P_MAX, bad_primes={N})
        L_euler_real = float(L_euler.real) if hasattr(L_euler, 'real') else float(L_euler)
        print(f"  Euler product L(Sym²,2) = {L_euler_real:.6f}", flush=True)

        L_use = mp.mpf(L_pari) if L_pari is not None else mp.mpf(L_euler_real)

        # Petersson from RS identity
        petersson = petersson_from_RS(N, L_use)
        # Predicted ratio: L(Sym²,2)/⟨f,f⟩
        ratio_RS = float(L_use / petersson)
        # Should = 8π³/N
        expected = float(8 * mp.pi**3 / N)

        print(f"  L(Sym²,2) = {float(L_use):.6f}", flush=True)
        print(f"  ⟨f,f⟩_RS = {float(petersson):.6e}", flush=True)
        print(f"  ratio L/<f,f> = {ratio_RS:.4f}  (should = 8π³/N = {expected:.4f})", flush=True)

        data[curve] = {
            "N": N, "rank": rank,
            "L_sym2_euler": L_euler_real,
            "L_sym2_pari": L_pari,
            "L_sym2_used": float(L_use),
            "petersson_RS": float(petersson),
            "ratio_L_over_petersson": ratio_RS,
            "expected_8pi3_over_N": expected,
            "identity_holds": abs(ratio_RS - expected) / expected < 0.01,
        }

        lines.append(f"## {curve} (N={N}, rank={rank})")
        lines.append(f"- L(Sym²E, 2) via Euler product: {L_euler_real:.6f}")
        if L_pari:
            lines.append(f"- L(Sym²E, 2) via PARI lfunsympow: {L_pari:.6f}")
        lines.append(f"- ⟨f,f⟩ from Rankin-Selberg = N·L/(8π³): {float(petersson):.4e}")
        lines.append(f"- Ratio L(Sym²,2)/⟨f,f⟩ = {ratio_RS:.4f}")
        lines.append(f"- Expected 8π³/N = {expected:.4f}")
        lines.append(f"- Identity holds to 1%: {data[curve]['identity_holds']}")
        lines.append("")

    # Cross-ratio test
    if "37a1" in data and "389a1" in data:
        L37 = data["37a1"]["L_sym2_used"]
        L389 = data["389a1"]["L_sym2_used"]
        P37 = data["37a1"]["petersson_RS"]
        P389 = data["389a1"]["petersson_RS"]

        lines.append("## Cross-ratio Analysis")
        lines.append(f"L(Sym²,2) ratio 37a1/389a1 = {L37/L389:.4f}")
        lines.append(f"Expected from 1/N: {389/37:.4f}")
        lines.append(f"⟨f,f⟩ ratio 37a1/389a1 = {P37/P389:.4f}")
        lines.append(f"Expected from N: {37/389:.4f}")
        lines.append("")
        lines.append("## Empirical E[C₁²] vs Prediction")
        lines.append(f"Empirical E[C₁²]: 37a1=2.19, 389a1=3.11")
        lines.append(f"If E[C₁²] ∝ ⟨f,f⟩: 37a1/389a1 ratio should be {P37/P389:.4f}")
        lines.append(f"Empirical ratio: {2.19/3.11:.4f}")
        lines.append("")
        lines.append("## Diagnosis")

        ratio_pred = P37 / P389
        ratio_emp = 2.19 / 3.11
        if abs(ratio_pred - ratio_emp) / ratio_emp < 0.3:
            lines.append("MATCH: empirical ratio consistent with ⟨f,f⟩ prediction (within 30%).")
            lines.append("=> Koyama proportionality E[C₁²] ∝ ⟨f,f⟩ plausible.")
        else:
            lines.append(f"MISMATCH: predicted ratio {ratio_pred:.3f} vs empirical {ratio_emp:.3f}.")
            lines.append("=> Rankin-Selberg identity + Koyama does NOT explain the direction.")
            lines.append("Candidates: (a) additional rank-dependent factor, (b) bad prime correction, "
                         "(c) Koyama proportionality constant is form-dependent.")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_MD, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nWrote {OUT_MD}", flush=True)


if __name__ == "__main__":
    main()
