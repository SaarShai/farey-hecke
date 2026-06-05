"""
Gate 3: the ONLY regime where parametric methods can beat a periodogram by
construction -- sample-starved super-resolution. Recover K closely-spaced
frequencies from N ~ 2K samples (below the Fourier/Rayleigh limit 2*pi/N).

This models the finite-degree (function-field) L-function case: the explicit
formula is an EXACT finite sum of K exponentials, so we can simulate it cleanly
with known ordinates and controlled noise.

Question: is there a (separation, SNR) regime where Prony/matrix-pencil cleanly
resolves both zeros but a windowed zero-padded periodogram cannot? And does it
survive realistic noise? If the advantage evaporates under any noise, the
finite-d niche is fragile too.
"""
import numpy as np

def matrix_pencil(sig, K):
    N = len(sig); L = N // 2
    L = max(L, K + 1); L = min(L, N - K - 1)
    Y = np.array([sig[i:i+L+1] for i in range(N - L)])
    Y0, Y1 = Y[:, :-1], Y[:, 1:]
    z = np.linalg.eigvals(np.linalg.pinv(Y0) @ Y1)
    z = z[np.argsort(-np.abs(z))][:K]
    return np.angle(z)

def periodogram_freqs(sig, K, dn=1.0, pad=64):
    w = np.hanning(len(sig))
    S = np.abs(np.fft.rfft(sig * w, n=pad*len(sig)))**2
    f = 2*np.pi*np.fft.rfftfreq(pad*len(sig))
    pk = [i for i in range(1, len(S)-1) if S[i] > S[i-1] and S[i] > S[i+1]]
    pk.sort(key=lambda i: -S[i])
    return np.sort(f[pk[:K]])

from scipy.signal import hilbert

def trial(gammas, N, snr_db, rng, kind):
    # all gammas must be in (0, pi) rad/sample to avoid aliasing
    n = np.arange(1, N+1)
    s = sum(np.cos(g*n + rng.uniform(0, 2*np.pi)) for g in gammas)
    if snr_db is not None:
        p = np.mean(s**2); ns = np.sqrt(p/10**(snr_db/10))
        s = s + rng.normal(0, ns, N)
    K = len(gammas)
    if kind == "prony":
        a = hilbert(s)                      # analytic signal (already complex)
        est = np.sort(np.abs(matrix_pencil(a, K)))
    else:
        est = periodogram_freqs(s, K)
    if len(est) < K: return False
    err = np.abs(np.sort(est) - np.sort(gammas))
    return bool(np.all(err < 0.25 * min(np.diff(sorted(gammas)))))

def main():
    rng = np.random.default_rng(0)
    base = 1.0
    print("RESOLUTION (noiseless), N=6 samples, K=2 zeros at {1.0, 1.0+sep} rad/sample")
    print("  Rayleigh/Fourier limit at N=6 ~ 2pi/6 = 1.047 rad")
    print(f"  {'sep':>6} {'prony':>7} {'periodogram':>12}")
    for sep in [1.5, 1.0, 0.6, 0.4, 0.25, 0.15, 0.08]:
        g = [base, base+sep]
        pr = np.mean([trial(g, 6, None, rng, "prony") for _ in range(40)])
        pp = np.mean([trial(g, 6, None, rng, "peri") for _ in range(40)])
        print(f"  {sep:6.2f} {pr:7.2f} {pp:12.2f}")

    print("\nNOISE robustness, N=12 samples, K=2 zeros sep=0.5 (sub-Rayleigh for periodogram)")
    print(f"  {'SNR_dB':>7} {'prony':>7} {'periodogram':>12}")
    for snr in [60, 40, 30, 20, 10, 0]:
        g = [base, base+0.5]
        pr = np.mean([trial(g, 12, snr, rng, "prony") for _ in range(60)])
        pp = np.mean([trial(g, 12, snr, rng, "peri") for _ in range(60)])
        print(f"  {snr:7d} {pr:7.2f} {pp:12.2f}")

if __name__ == "__main__":
    main()
