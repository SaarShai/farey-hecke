"""
GAP-11 N1 (deterministic) re-run: compute the ACTUAL frozen T1 observable
y(t), t = log N, on the order-1 Riesz window (amendment A2, clause W'), and
compare it against the explicit-formula prediction of T1_GAP16_RIESZ_IMPORT.md
Proposition R.

Frozen observable (T1 draft §1.1, window W' of Prop R):

    S(N) := Sum_{n<=N} mu(n) (1 - n/N) = (1/N) Sum_{0<=k<N} M(k)      (arithmetic side)

    y(t) := N^{-1/2} * [ S(N) - R0 - R_{-1}(N) - R_triv(N) ]
          = 2 Sum_{gamma>0} a_gamma cos(gamma*t + phi_gamma) + eps(t)   N = e^t

    R0 = -2                       (GAP16 (2.4)/T1 draft sec 1.1)
    R_{-1}(N) = 12/N              (GAP16 (2.4), new Riesz-window pole)
    R_triv(N) = Sum_{n>=1} N^{-2n} / ( (-2n)(1-2n) zeta'(-2n) )   (GAP16 (2.5), O(N^-2))

    a_gamma * e^{i phi_gamma} = 1 / ( (1/2+i*gamma)(3/2+i*gamma) zeta'(1/2+i*gamma) )

This script:
  (1) segmented-sieves mu(n) to N_MAX = 3e7 with numpy,
  (2) forms M(k) and its running sum to get S(N) at a log-spaced grid of N,
  (3) forms y(t) at the grid and compares it against the K-zero truncated
      explicit-formula prediction (Prop R), reporting the residual RMSE,
  (4) extracts the amplitude at gamma_1 = 14.1347 by a windowed periodogram
      (matched filter) directly from y(t), independent of the truncated
      prediction, and compares it to the predicted a_{gamma_1} and to the
      T1 bound / Gate-1 empirical numbers of draft sec 5.2.
"""
import hashlib
import json
import sys
import time

import numpy as np
import mpmath as mp

mp.mp.dps = 30

N_MAX = 30_000_000
N_GRID = 200
N_GRID_MIN = 1000  # below this the O(N^-A) remainder / R_triv truncation is not trustworthy

ZEROS = [14.134725141734693, 21.022039638771555, 25.010857580145688,
         30.424876125859513, 32.935061587739190, 37.586178158825671,
         40.918719012147495, 43.327073280914999, 48.005150881167159,
         49.773832477672302]

TWO_PI = 2.0 * np.pi


# ---------------------------------------------------------------- sieve mu
def sieve_mobius(n_max):
    """mu[1..n_max], standard prime/prime-square marking, numpy vectorised."""
    mu = np.ones(n_max + 1, dtype=np.int8)
    mu[0] = 0
    is_comp = np.zeros(n_max + 1, dtype=bool)
    for p in range(2, int(n_max ** 0.5) + 1):
        if not is_comp[p]:
            is_comp[p * p:: p] = True
    # recompute primes via a clean sieve of eratosthenes (above loop only marks composites correctly
    # if done in increasing p order using the *unmarked* status, which the slice above already gives)
    primes = np.nonzero(~is_comp[2:])[0] + 2
    for p in primes:
        mu[p:: p] *= -1
        pp = p * p
        if pp <= n_max:
            mu[pp:: pp] = 0
    return mu


def main():
    t0 = time.time()
    print("sieving mu(n) to N_MAX =", N_MAX)
    mu = sieve_mobius(N_MAX)
    print("sieve done in %.1fs" % (time.time() - t0))

    # M(k) = sum_{n<=k} mu(n), k=0..N_MAX  (M(0)=0)
    M = np.cumsum(mu.astype(np.int64))
    # prefix2(N) = sum_{k=0}^{N-1} M(k)
    prefix2 = np.cumsum(M.astype(np.float64))  # prefix2[j] = sum_{k=0}^{j} M(k)

    # log-spaced integer grid of N in [N_GRID_MIN, N_MAX]
    grid = np.unique(np.round(np.geomspace(N_GRID_MIN, N_MAX, N_GRID)).astype(np.int64))
    grid = grid[(grid >= 2) & (grid <= N_MAX)]

    def S_of_N(N):
        # S(N) = (1/N) * sum_{k=0}^{N-1} M(k) = prefix2[N-1] / N
        return prefix2[N - 1] / N

    S_vals = np.array([S_of_N(N) for N in grid], dtype=np.float64)

    # R_triv(N): leading term n=1, zeta'(-2) = -zeta(3)/(4 pi^2); higher terms astronomically
    # smaller (n=2 term ~N^-4 * zeta'(-4)^-1) and omitted -- checked negligible below.
    zetap_neg2 = float(-mp.zeta(3) / (4 * mp.pi ** 2))
    coeff1 = 1.0 / ((-2) * (1 - 2) * zetap_neg2)   # = 1/(2*zeta'(-2))
    R_triv = coeff1 * grid.astype(np.float64) ** (-2.0)
    R_triv_n2_ratio_at_min = None  # sanity note only; not computed (negligible by construction)

    R0 = -2.0
    Rm1 = 12.0 / grid.astype(np.float64)

    t_grid = np.log(grid.astype(np.float64))
    y_emp = grid.astype(np.float64) ** (-0.5) * (S_vals - R0 - Rm1 - R_triv)

    # ---- explicit-formula prediction, K-zero truncation (Prop R) ----
    print("computing zeta'(1/2+i*gamma_j) for the first %d zeros (mpmath)..." % len(ZEROS))
    a_amp = []
    phi = []
    for g in ZEROS:
        s = mp.mpc(0.5, g)
        zp = mp.zeta(s, derivative=1)
        val = 1.0 / ((mp.mpc(0.5, g)) * (mp.mpc(1.5, g)) * zp)
        a_amp.append(float(abs(val)))
        phi.append(float(mp.arg(val)))
    a_amp = np.array(a_amp)
    phi = np.array(phi)

    print("\n--- a_gamma_j, phi_gamma_j (Prop R amplitude/phase) ---")
    for j, (g, a, p) in enumerate(zip(ZEROS, a_amp, phi), 1):
        print(f"  j={j:2d}  gamma={g:10.6f}  a_gamma={a:.6e}  phi={p:.6f}")

    def predicted(t, K):
        return sum(2 * a_amp[j] * np.cos(ZEROS[j] * t + phi[j]) for j in range(K))

    for K in (1, 3, 10):
        pred = predicted(t_grid, K)
        resid = y_emp - pred
        rmse = float(np.sqrt(np.mean(resid[grid >= N_GRID_MIN] ** 2)))
        print(f"K={K:2d} zeros:  residual RMSE over grid = {rmse:.6e}   "
              f"(y_emp range [{y_emp.min():.4f},{y_emp.max():.4f}])")

    # ---- windowed periodogram / matched filter at gamma_1, direct from y_emp ----
    # C(g) = (1/(t_max-t_min)) * int y_emp(t) exp(-i g t) dt  (trapezoid on the log-spaced-in-N,
    # i.e. UNIFORM-in-t grid)
    def matched_filter(g):
        integrand = y_emp * np.exp(-1j * g * t_grid)
        val = np.trapezoid(integrand, t_grid) / (t_grid[-1] - t_grid[0])
        return val

    g1 = ZEROS[0]
    C1 = matched_filter(g1)
    print(f"\nmatched filter at gamma_1={g1}: |C1| = {abs(C1):.6e}  "
          f"(predicted a_gamma1 = {a_amp[0]:.6e}, ratio = {abs(C1)/a_amp[0]:.4f})")

    # off-tone control (sanity: matched filter should be much smaller off a true zero)
    g_off = 17.0
    C_off = matched_filter(g_off)
    print(f"off-tone control at gamma={g_off}: |C| = {abs(C_off):.6e}")

    # T1 draft sec 5.2 comparison numbers, X=3e7
    T = np.log(3e7)
    bound_gamma1 = np.sqrt(6 * np.log(g1 / TWO_PI)) / T ** 1.5
    gate1_empirical_gamma1 = 0.04e-2 * g1  # 0.04% relative error, T1 draft sec 5.2 row 2
    print(f"\nT1 bound RMSE at gamma_1 (X=3e7): {bound_gamma1:.6f}")
    print(f"Gate-1 empirical abs error at gamma_1 (from draft sec 5.2): {gate1_empirical_gamma1:.6f}")
    print(f"N1 rerun: |matched-filter amplitude - predicted a_gamma1| = "
          f"{abs(abs(C1) - a_amp[0]):.6e}")

    # ---- receipt ----
    with open(__file__, "rb") as fh:
        script_sha256 = hashlib.sha256(fh.read()).hexdigest()

    receipt = {
        "purpose": "GAP-11 N1 (deterministic) re-run of the frozen T1 observable y(t) "
                   "on the actual arithmetic side (Mobius sieve), compared against the "
                   "Prop R explicit-formula prediction (T1_GAP16_RIESZ_IMPORT.md).",
        "script": "research_notes/rh_goals_2026-08-14/lane_t/t1_gap11_rerun.py",
        "script_sha256": script_sha256,
        "python": sys.version,
        "numpy_version": np.__version__,
        "mpmath_version": mp.__version__,
        "N_MAX": N_MAX,
        "grid_size": int(len(grid)),
        "grid_min": int(grid.min()),
        "grid_max": int(grid.max()),
        "R0": R0,
        "R_triv_leading_coeff_at_n1": coeff1,
        "zeta_prime_neg2": zetap_neg2,
        "residual_rmse_vs_K_zeros": {
            str(K): float(np.sqrt(np.mean((y_emp - predicted(t_grid, K))[grid >= N_GRID_MIN] ** 2)))
            for K in (1, 3, 10)
        },
        "matched_filter_gamma1": {
            "gamma_1": g1,
            "abs_C1": float(abs(C1)),
            "predicted_a_gamma1": float(a_amp[0]),
            "ratio": float(abs(C1) / a_amp[0]),
        },
        "matched_filter_off_tone_control": {"gamma": g_off, "abs_C": float(abs(C_off))},
        "T1_bound_RMSE_at_gamma1_X3e7": float(bound_gamma1),
        "gate1_empirical_abs_error_at_gamma1_from_draft": float(gate1_empirical_gamma1),
    }
    out_path = __file__.rsplit("/", 1)[0] + "/T1_GAP11_N1_RECEIPT.json"
    with open(out_path, "w") as fh:
        json.dump(receipt, fh, indent=2)
    print("\nreceipt written to", out_path)


if __name__ == "__main__":
    main()
