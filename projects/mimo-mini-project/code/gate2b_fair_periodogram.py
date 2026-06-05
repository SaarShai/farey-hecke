"""
Gate 2 crux: give the Fourier periodogram a FAIR fight, then sweep sample count.

If a well-tuned periodogram (Hann window, zero-padded, raw real signal) ALSO
recovers the zeros, the parametric method is "obvious" (display). If MUSIC
recovers at sample counts where the periodogram cannot, that quantifies a real
super-resolution advantage = the novelty case.

Reuses bias/sieve from gate2_clean_recovery.
"""
import math, time, sys
import numpy as np
from gate2_clean_recovery import (sieve_primes, bias_signal, make_signal,
                                  music, find_peaks, match, TRUE_GAMMA)


def fair_periodogram(xs, bias, dn, gamma_grid, pad=8):
    """Windowed, zero-padded periodogram on the RAW real (detrended) signal."""
    env = np.sqrt(xs) / np.log(xs)
    s = bias / env
    # remove low-order polynomial trend (fairer than just mean)
    t = np.arange(len(s))
    coef = np.polyfit(t, s, 3)
    s = s - np.polyval(coef, t)
    w = np.hanning(len(s))
    sw = s * w
    m = np.arange(len(sw))
    P = np.array([abs(np.sum(sw * np.exp(-1j * g * dn * m)))**2 for g in gamma_grid])
    return P


def recovered(true_g, peaks, tol_pct=2.0, max_rank=None):
    n = 0
    for tg, g, ae, pe, rk in match(true_g, peaks):
        if pe < tol_pct and (max_rank is None or rk <= max_rank):
            n += 1
    return n


def main():
    X_max = int(sys.argv[1]) if len(sys.argv) > 1 else 30_000_000
    primes = sieve_primes(X_max)
    print(f"sieved {len(primes):,} primes to {X_max:,}\n")

    # ---- Fair periodogram head-to-head at full sample count ----
    n_samples = 400
    dn = (math.log(X_max) - math.log(100)) / (n_samples - 1)
    grid = np.linspace(1.0, 22.0, 6000)
    xs, bias = bias_signal(primes, X_max, n_samples)
    Pf = fair_periodogram(xs, bias, dn, grid)
    fp = find_peaks(grid, Pf, k=8)
    print(f"[FAIR PERIODOGRAM] N={n_samples} top peaks: " +
          ", ".join(f"{g:.2f}" for g, _ in fp))
    print(f"  {'true':>8} {'got':>8} {'%err':>7} {'rank':>5}")
    for tg, g, ae, pe, rk in match(TRUE_GAMMA, fp):
        flag = "" if (pe < 2 and rk <= 5) else "  <-- weak"
        print(f"  {tg:8.3f} {g:8.3f} {pe:7.2f} {rk:5d}{flag}")
    print(f"  recovered (dominant): {recovered(TRUE_GAMMA, fp, 2.0, 5)}/5\n")

    # ---- Sample-count sweep: who recovers gamma_1..gamma_3 first? ----
    print("SWEEP: # of {g1,g2,g3} recovered (<2% err, rank<=3) vs sample count")
    print(f"  {'N':>5} {'dn':>7} {'MUSIC':>7} {'PERIODOGRAM':>12}")
    targets = TRUE_GAMMA[:3]
    for N in [40, 60, 80, 120, 160, 240, 320, 400]:
        dn = (math.log(X_max) - math.log(100)) / (N - 1)
        if math.pi / dn < 13:   # Nyquist must cover g3~13
            print(f"  {N:5d} {dn:7.4f}   (Nyquist<13, skip)")
            continue
        g = np.linspace(1.0, 13.5, 4000)
        xs, bias = bias_signal(primes, X_max, N)
        sig = make_signal(xs, bias)
        pm = find_peaks(g, music(sig, 3, dn, g), k=6)
        pf = find_peaks(g, fair_periodogram(xs, bias, dn, g), k=6)
        rm = recovered(targets, pm, 2.0, 3)
        rp = recovered(targets, pf, 2.0, 3)
        print(f"  {N:5d} {dn:7.4f} {rm:7d} {rp:12d}")


if __name__ == "__main__":
    main()
