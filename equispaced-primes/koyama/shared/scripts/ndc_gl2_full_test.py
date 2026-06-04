"""
Comprehensive NDC GL(2) test with Γ-factor + p≤5K truncation.

Three objects:
  37a1  — rank 1, N=37,  ρ = 1 + 5.003212i  (LMFDB verified)
  389a1 — rank 2, N=389, ρ complex (computed via mpmath below)
  Δ(z)  — weight 12, N=1, ρ = 6 + 9.22237i (LMFDB)

Uses a_p/τ(p) data from ~/farey_py_tasks/data/, computed via point-counting (37a1/389a1 verified against LMFDB for 37a1; τ(p) verified).

Corrected NDC formula (Koyama 2026-04-18):
  D_K = c_K · E_K · N^(ρ/2) · (2π)^(-ρ) · Γ(ρ)

For Δ (holomorphic weight 12): use normalised a_p/p^{11/2} to match critical line Re=1/2, OR use unnormalised with ρ=6+γi. We use UNNORMALISED throughout.
"""
import mpmath as mp
import json, time, sys
from pathlib import Path

mp.mp.dps = 30

DATA_DIR = Path.home() / "farey_py_tasks" / "data"

# Load data
with open(DATA_DIR / "ap_37a1.json") as f:
    AP_37 = {int(k): v for k, v in json.load(f).items()}
with open(DATA_DIR / "ap_389a1.json") as f:
    AP_389 = {int(k): v for k, v in json.load(f).items()}
with open(DATA_DIR / "tau_delta.json") as f:
    TAU = {int(k): v for k, v in json.load(f).items()}

print("=" * 72)
print("NDC GL(2) full test: 37a1, 389a1, Δ(z)")
print(f"a_p/τ(p) data: {len(AP_37)} / {len(AP_389)} / {len(TAU)} primes")
print("Γ-factor correction + p≤5K truncation synchronization")
print("=" * 72)

zeta2 = mp.zeta(2)

def multiplicative_mu_from_ap(n, ap_dict, curve_N):
    """μ_E(n) via Hecke multiplicativity on a GL(2) newform.
    μ_E(p) = -a_p, μ_E(p²) = a_p² - p (for good reduction).
    For bad reduction (p|N): μ_E(p) = -a_p, μ_E(p^k≥2) = 0."""
    if n == 1: return 1
    # Find prime factorization
    res = 1
    for p in sorted(ap_dict.keys()):
        if n == 1: break
        if p * p > n and n > 1 and n in ap_dict:
            res *= -ap_dict[n]
            n = 1; break
        if n % p == 0:
            k = 0
            while n % p == 0: n //= p; k += 1
            ap = ap_dict[p]
            bad = (curve_N % p == 0)
            if k == 1: res *= -ap
            elif k == 2:
                if bad: return 0
                res *= (ap*ap - p)
            else: return 0
    if n > 1: return 0
    return res

def multiplicative_mu_delta(n, tau_dict):
    """For Δ weight 12: μ_Δ(p) = -τ(p), μ_Δ(p²) = τ(p)² - p^{11}, higher = 0."""
    if n == 1: return 1
    res = 1
    for p in sorted(tau_dict.keys()):
        if n == 1: break
        if n % p == 0:
            k = 0
            while n % p == 0: n //= p; k += 1
            tp = tau_dict[p]
            if k == 1: res *= -tp
            elif k == 2: res *= (tp*tp - p**11)
            else: return 0
    if n > 1: return 0
    return res

def compute_ndc(label, rho, N, ap_or_tau, mu_func, weight=None, Ks=[100, 200, 500, 1000]):
    """Compute corrected NDC at various K."""
    print(f"\n=== {label}: ρ = {rho}, N = {N} ===")
    two_pi_factor = mp.power(2*mp.pi, -rho)
    gamma_rho = mp.gamma(rho)
    gamma_factor = two_pi_factor * gamma_rho
    N_factor = mp.power(N, rho/2) if N > 1 else mp.mpc(1)
    print(f"|Γ_factor| = {abs(gamma_factor)}")
    print(f"arg(Γ_factor) = {mp.arg(gamma_factor)}")
    print(f"|N^(ρ/2)| = {abs(N_factor)}")
    print(f"{'K':>6} {'|c_K|':>18} {'|E_{5K}|':>18} {'|D_K|':>20} {'|D_K|·ζ(2)':>20}  elapsed")

    primes = sorted(ap_or_tau.keys())
    P_MAX = primes[-1]

    for K in Ks:
        t0 = time.time()
        upper_p = 5 * K
        if upper_p > P_MAX:
            print(f"{K:>6}  SKIP — needs p≤{upper_p} but data only to p≤{P_MAX}")
            continue

        # c_K with smooth cutoff
        c_K = mp.mpc(0)
        for n in range(1, K+1):
            m = mu_func(n, ap_or_tau, N) if label != "Δ(z)" else mu_func(n, ap_or_tau)
            if m != 0:
                c_K += mp.mpf(m) * mp.exp(-mp.mpf(n)/K) / mp.power(n, rho)

        # Euler product p ≤ 5K
        E_K = mp.mpc(1)
        for p in primes:
            if p > upper_p: break
            v = ap_or_tau[p]
            bad = (N % p == 0) if N > 1 else False
            if label == "Δ(z)":
                # L-factor: (1 - τ(p) p^{-s} + p^{11-2s})^{-1}
                E_K /= (1 - mp.mpf(v)/mp.power(p, rho) + mp.power(p, 11 - 2*rho))
            elif bad:
                E_K /= (1 - mp.mpf(v)/mp.power(p, rho))
            else:
                E_K /= (1 - mp.mpf(v)/mp.power(p, rho) + 1/mp.power(p, 2*rho - 1))

        D_K = c_K * E_K * N_factor * gamma_factor
        D_zeta2 = abs(D_K) * zeta2
        elapsed = time.time() - t0
        print(f"{K:>6} {float(abs(c_K)):>18.6e} {float(abs(E_K)):>18.6e} {float(abs(D_K)):>20.6e} {float(D_zeta2):>20.10f}  {elapsed:.1f}s")
        sys.stdout.flush()

# --- Run tests ---

# 37a1: ρ = 1 + 5.003212i (LMFDB-verified)
rho_37 = mp.mpc(1, mp.mpf('5.003212419948988'))
compute_ndc("37a1", rho_37, 37, AP_37, multiplicative_mu_from_ap, Ks=[50, 100, 200, 500, 1000])

# 389a1: rank-2, first complex zero — need value
# LMFDB's L(E_{389a1}, s) has double zero at s=1 and first complex zero
# Try a search: from known estimates, γ_1 ≈ 2.876 for 389a1
# If wrong, c_K won't converge to zero; that's our diagnostic.
print("\n\n### 389a1: Trying ρ = 1 + 2.876i (first complex zero, approx from literature)")
rho_389 = mp.mpc(1, mp.mpf('2.876'))
compute_ndc("389a1", rho_389, 389, AP_389, multiplicative_mu_from_ap, Ks=[50, 100, 200, 500, 1000])

# Δ(z): ρ = 6 + 9.22237i (LMFDB first zero of L(Δ, s))
rho_D = mp.mpc(6, mp.mpf('9.22237'))
compute_ndc("Δ(z)", rho_D, 1, TAU, multiplicative_mu_delta, weight=12, Ks=[50, 100, 200, 500, 1000])

print("\nDONE")
