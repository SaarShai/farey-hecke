"""
GATE 1+2 (honest): does MUSIC/Prony RECOVER L(s,chi_4) zeros from Chebyshev
bias, NON-circularly, beating the Fourier periodogram (obviousness baseline)
and a null control?

Fixes the committed script's flaws:
  - gamma axis is determined A PRIORI: steering vector uses e^{i*gamma*dn*m},
    so peaks are read directly in true gamma units. NO post-hoc "divide by dn
    or not" choice (the circular fit).
  - Ground truth fixed BEFORE running (LMFDB L(s,chi_4) ordinates).
  - Adds Fourier periodogram baseline: if the periodogram already peaks at the
    same gammas, the parametric method is "obvious" (display, not recovery).
  - Adds NULL: shuffle prime residue classes -> signal with same envelope but
    no zero structure. True-gamma peaks must VANISH under null.
  - Reports, per true zero: nearest recovered peak, error, and its RANK among
    all peaks (are true zeros DOMINANT, or cherry-picked?).

KILL criteria (decide before looking):
  K1: true zeros are not dominant peaks (rank > #zeros sought) -> recovery is
      cherry-picking, not detection.
  K2: parametric method no better than periodogram (same peaks, same accuracy)
      -> obviousness loss; it's just the known spectral display.
  K3: null produces peaks at the true gammas of comparable height -> the
      "recovery" is an artifact of the envelope, not the zeros.
"""
import math, time, sys
import numpy as np

# LMFDB ground truth: low zeros of L(s, chi_4) (Dirichlet beta), fixed a priori
TRUE_GAMMA = np.array([6.0209489, 10.2437703, 12.9888600, 16.3425751, 18.2919922])


def sieve_primes(N):
    s = np.ones(N + 1, dtype=bool)
    s[:2] = False
    for i in range(2, int(math.isqrt(N)) + 1):
        if s[i]:
            s[i*i::i] = False
    return np.nonzero(s)[0]


def bias_signal(primes, X_max, n_samples, shuffle=False, rng=None):
    """Chebyshev bias pi(x;4,3)-pi(x;4,1) at n_samples log-spaced x in [100,X_max].
    shuffle=True randomly permutes the +/-1 residue labels (NULL: same count
    envelope, destroys zero structure)."""
    odd = primes[primes > 2]
    res = np.where(odd % 4 == 3, 1, -1).astype(np.int64)
    if shuffle:
        res = rng.permutation(res)
    cum = np.cumsum(res)                      # bias up to each prime
    log_xs = np.linspace(math.log(100), math.log(X_max), n_samples)
    xs = np.exp(log_xs)
    idx = np.searchsorted(odd, xs, side="right") - 1
    idx = np.clip(idx, 0, len(cum) - 1)
    bias = cum[idx].astype(float)
    return xs, bias


def make_signal(xs, bias):
    """Normalize by sqrt(x)/log(x) envelope, detrend, return complex analytic."""
    env = np.sqrt(xs) / np.log(xs)
    s = bias / env
    s = s - np.mean(s)
    # analytic signal (Hilbert) -> complex, one-sided spectrum
    from numpy.fft import fft, ifft
    N = len(s)
    S = fft(s)
    h = np.zeros(N)
    h[0] = 1;
    if N % 2 == 0:
        h[N//2] = 1; h[1:N//2] = 2
    else:
        h[1:(N+1)//2] = 2
    return ifft(S * h)


def music(signal, n_sources, dn, gamma_grid):
    N = len(signal); M = N // 2
    L = N - M + 1
    X = np.empty((M, L), dtype=complex)
    for k in range(L):
        X[:, k] = signal[k:k+M]
    R = (X @ X.conj().T) / L
    w, V = np.linalg.eigh(R)
    En = V[:, :M - n_sources]                 # noise subspace (smallest eigs)
    m = np.arange(M)
    P = np.empty(len(gamma_grid))
    for i, g in enumerate(gamma_grid):
        a = np.exp(1j * g * dn * m)
        proj = En.conj().T @ a
        P[i] = 1.0 / (np.vdot(proj, proj).real + 1e-15)
    return P


def periodogram(signal, dn, gamma_grid):
    m = np.arange(len(signal))
    P = np.empty(len(gamma_grid))
    for i, g in enumerate(gamma_grid):
        a = np.exp(-1j * g * dn * m)
        P[i] = np.abs(np.vdot(a, signal))**2
    return P


def find_peaks(gamma_grid, P, k=8):
    pk = [(gamma_grid[i], P[i]) for i in range(1, len(P)-1)
          if P[i] > P[i-1] and P[i] > P[i+1]]
    pk.sort(key=lambda t: -t[1])
    return pk[:k]


def match(true_g, peaks):
    """For each true gamma: nearest peak, abs error, % error, rank."""
    out = []
    for tg in true_g:
        best = min(range(len(peaks)), key=lambda j: abs(peaks[j][0] - tg))
        g, _ = peaks[best]
        out.append((tg, g, abs(g-tg), 100*abs(g-tg)/tg, best+1))
    return out


def report(name, true_g, peaks):
    print(f"\n[{name}] top peaks (gamma): " +
          ", ".join(f"{g:.2f}" for g, _ in peaks))
    print(f"  {'true':>8} {'got':>8} {'abserr':>8} {'%err':>7} {'rank':>5}")
    for tg, g, ae, pe, rk in match(true_g, peaks):
        flag = "" if (pe < 2 and rk <= len(true_g)) else "  <-- weak"
        print(f"  {tg:8.3f} {g:8.3f} {ae:8.3f} {pe:7.2f} {rk:5d}{flag}")


def main():
    X_max = int(sys.argv[1]) if len(sys.argv) > 1 else 30_000_000
    n_samples = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    n_sources = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    print(f"=== Gate1+2 clean recovery: X={X_max:,} samples={n_samples} d={n_sources} ===")
    t0 = time.time()
    primes = sieve_primes(X_max)
    print(f"  sieved {len(primes):,} primes in {time.time()-t0:.1f}s")
    dn = (math.log(X_max) - math.log(100)) / (n_samples - 1)
    nyq = math.pi / dn
    print(f"  dn={dn:.4f}  Nyquist gamma={nyq:.1f}  freq-res~{2*math.pi/(n_samples*dn):.3f}")
    grid = np.linspace(1.0, min(22.0, nyq*0.95), 4000)

    xs, bias = bias_signal(primes, X_max, n_samples)
    sig = make_signal(xs, bias)
    Pm = music(sig, n_sources, dn, grid)
    Pp = periodogram(sig, dn, grid)
    report("MUSIC", TRUE_GAMMA, find_peaks(grid, Pm))
    report("PERIODOGRAM (baseline)", TRUE_GAMMA, find_peaks(grid, Pp))

    rng = np.random.default_rng(0)
    xs0, bias0 = bias_signal(primes, X_max, n_samples, shuffle=True, rng=rng)
    sig0 = make_signal(xs0, bias0)
    Pm0 = music(sig0, n_sources, dn, grid)
    report("NULL (shuffled residues) MUSIC", TRUE_GAMMA, find_peaks(grid, Pm0))

    # honest scorecard
    m = match(TRUE_GAMMA, find_peaks(grid, Pm))
    good = [r for r in m if r[3] < 2 and r[4] <= n_sources]
    print(f"\nSCORECARD: {len(good)}/{len(TRUE_GAMMA)} true zeros recovered "
          f"as dominant (<2% err, rank<={n_sources})")


if __name__ == "__main__":
    main()
