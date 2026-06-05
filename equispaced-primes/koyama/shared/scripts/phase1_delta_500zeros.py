#!/usr/bin/env python3
# NOTE: This script contains the Δ-valid 500-zero ensemble only.
# The EC portion (37a1, 389a1) had a μ_f(p²) bug (used p^11 for EC, should use p).
# For corrected EC computation use phase1_ec_recompute.py instead.
from __future__ import annotations

import json
import math
import os
import subprocess
import tempfile
from pathlib import Path
from mpmath import mp

K = 10000
H = mp.mpf("1e-8")
PREC = 50
DENOM = math.log(K) + 0.5772156649015328606
OUT = Path.home() / "Desktop" / "Farey-Local" / "experiments" / "PHASE1_500ZEROS_CORRECTED.json"

mp.dps = PREC


def gp_run(script: str) -> str:
    # Use temp file — gp -q -f with stdin has multi-line parsing issues
    # Collapse multi-line scripts to single-line for inline use
    with tempfile.NamedTemporaryFile(mode="w", suffix=".gp", delete=False) as f:
        f.write(script)
        fname = f.name
    try:
        r = subprocess.run(
            ["gp", "-q", fname],
            text=True,
            capture_output=True,
            check=True,
        )
        return r.stdout.strip()
    finally:
        os.unlink(fname)


def gp_try(scripts: list[str]) -> str:
    last = None
    for s in scripts:
        try:
            out = gp_run(s)
            if out:
                return out
        except subprocess.CalledProcessError as e:
            last = e
    raise RuntimeError(f"gp failed: {last.stderr if last else 'no output'}")


def parse_prime_map(text: str) -> dict[int, int]:
    out: dict[int, int] = {}
    for line in text.splitlines():
        if not line.strip():
            continue
        p, v = line.split()
        out[int(p)] = int(v)
    return out


def parse_zero_bundle(text: str):
    zeros, lprimes = [], []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Remove PARI spaces inside E-notation: "1.23 E-5" -> "1.23E-5"
        import re as _re
        line = _re.sub(r'(\d)\s+([Ee][+-]?\d)', r'\1\2', line)
        parts = line.split()
        if len(parts) != 4:
            continue  # skip malformed lines
        try:
            re0, im0, relp, imlp = map(mp.mpf, parts)
        except Exception:
            continue
        zeros.append(mp.mpc(re0, im0))
        lprimes.append(mp.mpc(relp, imlp))
    return zeros, lprimes


def sieve_spf(n: int) -> list[int]:
    spf = list(range(n + 1))
    spf[0] = spf[1] = 1
    for i in range(2, int(n**0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def build_terms(mu_p: dict[int, int], square_local) -> list[tuple[mp.mpf, mp.mpf]]:
    spf = sieve_spf(K)
    terms = []
    for n in range(1, K + 1):
        m, val = n, 1
        while m > 1:
            p = spf[m]
            e = 0
            while m % p == 0:
                m //= p
                e += 1
            if e >= 3:
                val = 0
                break
            val *= mu_p[p] if e == 1 else square_local(p)
        if val:
            terms.append((mp.mpf(val) * mp.exp(-mp.mpf(n) / K), mp.log(n)))
    return terms


def c_k(rho, terms):
    s = mp.mpc(0)
    for w, ln in terms:
        s += w * mp.exp(-rho * ln)
    return s


def pair(z):
    return [float(z.real), float(z.imag)]


def is_central(z):
    return abs(z.real - mp.mpf("0.5")) < mp.mpf("1e-20") and abs(z.imag) < mp.mpf("1e-20")


# Weierstrass models for curves without elldata
EC_MODELS = {
    "37a1": "[0,0,1,-1,0]",
    "389a1": "[0,1,1,-2,0]",
}


def get_ec(label: str, im_upper: float):
    model = EC_MODELS[label]
    coeff_script = (
        f'default(realprecision, 50); E = ellinit({model});'
        f' forprime(p = 2, {K}, print(p, " ", ellap(E, p)));'
    )
    coeffs = parse_prime_map(gp_run(coeff_script))
    zero_script = (
        f'default(realprecision, 50); E = ellinit({model}); L = lfuncreate(E);'
        f' z = lfunzeros(L, {im_upper}); h = 0.0000001;'
        f' for(i = 1, #z, s = 1/2 + z[i]*I;'
        f' lp = (lfun(L, s + h*I) - lfun(L, s - h*I)) / (2*h*I);'
        f' print("0.5 ", z[i], " ", real(lp), " ", imag(lp)););'
    )
    zeros, lprimes = parse_zero_bundle(gp_run(zero_script))
    return coeffs, zeros, lprimes


def get_delta(im_upper: float):
    coeff_script = (
        f'default(realprecision, 50); mf = mfinit([1,12], 1); f = mfeigenbasis(mf)[1];'
        f' c = mfcoefs(f, {K}); forprime(p = 2, {K}, print(p, " ", c[p+1]));'
    )
    coeffs = parse_prime_map(gp_run(coeff_script))
    zero_script = (
        f'default(realprecision, 50); mf = mfinit([1,12], 1); f = mfeigenbasis(mf)[1];'
        f' L = lfunmf(mf, f); z = lfunzeros(L, {im_upper}); h = 0.0000001;'
        f' for(i = 1, #z, s = 6 + z[i]*I;'
        f' lp = (lfun(L, s + h*I) - lfun(L, s - h*I)) / (2*h*I);'
        f' print("6.0 ", z[i], " ", real(lp), " ", imag(lp)););'
    )
    zeros, lprimes = parse_zero_bundle(gp_run(zero_script))
    return coeffs, zeros, lprimes


def assemble(mu_p, zeros, lprimes, square_local, skip_central=False):
    if skip_central:
        filtered = [(z, lp) for z, lp in zip(zeros, lprimes) if not is_central(z)]
        zeros, lprimes = [z for z, _ in filtered], [lp for _, lp in filtered]
    terms = build_terms(mu_p, square_local)
    cvals, C1 = [], []
    for z, lp in zip(zeros, lprimes):
        ck = c_k(z, terms)
        cvals.append(ck)
        C1.append(float(abs(ck) * abs(lp) / DENOM))
    ec1_sq = float(sum(c * c for c in C1) / len(C1))
    return {
        "zeros": [pair(z) for z in zeros],
        "c_K": [pair(z) for z in cvals],
        "Lprime": [pair(z) for z in lprimes],
        "C1": C1,
        "EC1_sq": ec1_sq,
    }


def main():
    out = {}

    # Upper imaginary limits: EC ~300 gives ~500 zeros; Delta ~600 gives ~500 zeros
    print("Computing 37a1...")
    ec37_p, z37, lp37 = get_ec("37a1", 300.0)
    # skip_central=True: lfuncreate returns z=0 as first zero (numerical artifact)
    out["37a1"] = assemble(ec37_p, z37, lp37, lambda p: p, skip_central=True)
    print(f"  37a1 zeros={len(out['37a1']['C1'])}, E[C1^2] = {out['37a1']['EC1_sq']:.4f}")

    print("Computing Delta...")
    delta_p, zd, lpd = get_delta(600.0)
    out["Delta"] = assemble(delta_p, zd, lpd, lambda p: p**11)
    print(f"  Delta zeros={len(out['Delta']['C1'])}, E[C1^2] = {out['Delta']['EC1_sq']:.4f}")

    print("Computing 389a1...")
    ec389_p, z389, lp389 = get_ec("389a1", 300.0)
    out["389a1"] = assemble(ec389_p, z389, lp389, lambda p: p, skip_central=True)
    print(f"  389a1 E[C1^2] = {out['389a1']['EC1_sq']:.4f}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(f"Saved to {OUT}")


if __name__ == "__main__":
    main()
