"""
LAST PROBE: close-pair super-resolution from limited X, on REAL prime signals.

The one untested axis. For two real (quadratic) Dirichlet L-functions whose low
zeros are CLOSE, build the combined Chebyshev-bias prime signal up to bound X,
and ask: does a parametric estimator (MUSIC/ESPRIT) resolve the close pair at a
SMALLER X than a fair (Hann, zero-padded) Fourier periodogram? If yes and robust
under the real arithmetic fluctuation, a genuine niche survives. If both resolve
at ~the same X (as in Gate 2), final kill.

Ground truth zeros: direct evaluation of L(1/2+it,chi_D) via Hurwitz zeta
(mpmath) -- this is the ORACLE/competitor, not the thing tested.
"""
import math, time
import numpy as np
import mpmath as mp
from scipy.signal import hilbert
from scipy.optimize import minimize_scalar

mp.mp.dps = 25

# ---- quadratic characters: Kronecker symbol (D/n), conductor |D| ----
FUND_D = [-3, -4, 5, -7, 8, -8, -11, 12, 13, -15, 17, -19, 21, -20, 24, -23]

def kronecker(a, n):
    """Kronecker symbol (a/n)."""
    if n == 0:
        return 1 if a in (1, -1) else 0
    if n < 0:
        return kronecker(a, -1) * kronecker(a, -n)
    if n == -1 or a == -1:
        pass
    # (a/-1)
    if n == 1:
        return 1
    # factor out 2s
    res = 1
    while n % 2 == 0:
        n //= 2
        t = a % 8
        if t in (3, 5):
            res = -res
    # now n odd > 0
    a %= n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            t = n % 8
            if t in (3, 5):
                res = -res
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            res = -res
        a %= n
    return res if n == 1 else 0

def kron_neg1(a):
    """(a/-1) = sign handling: 1 if a>=0 else -1, used for negative D."""
    return 1 if a >= 0 else -1

def L_chi(D, t):
    """L(1/2+it, chi_D) via L(s,chi)=q^{-s} sum_{a=1}^{q} chi(a) zeta(s,a/q)."""
    q = abs(D); s = mp.mpf(1)/2 + 1j*t
    tot = mp.mpc(0)
    for a in range(1, q+1):
        c = kronecker(D, a)
        if c:
            tot += c * mp.zeta(s, mp.mpf(a)/q)
    return q**(-s) * tot

def low_zeros(D, t_max=20.0, coarse=0.05):
    ts = np.arange(1.0, t_max, coarse)
    mag = np.array([abs(L_chi(D, t)) for t in ts])
    zeros = []
    for i in range(1, len(mag)-1):
        if mag[i] < mag[i-1] and mag[i] < mag[i+1] and mag[i] < 0.5:
            r = minimize_scalar(lambda t: float(abs(L_chi(D, t))),
                                bracket=(ts[i-1], ts[i], ts[i+1]),
                                method="brent", options={"xtol":1e-6})
            if float(abs(L_chi(D, r.x))) < 0.05:
                zeros.append(round(float(r.x), 4))
    # dedup
    out = []
    for z in sorted(zeros):
        if not out or abs(z-out[-1]) > 0.01:
            out.append(z)
    return out

# ---- real prime bias signal for chi_D up to X ----
def sieve(N):
    s = np.ones(N+1, bool); s[:2] = False
    for i in range(2, int(math.isqrt(N))+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def combined_signal(primesD, X, n_samples):
    """Sum of Chebyshev biases of the two characters, sampled log-spaced to X."""
    log_xs = np.linspace(math.log(100), math.log(X), n_samples)
    xs = np.exp(log_xs)
    sig = np.zeros(n_samples)
    for D, pr in primesD:
        chi = np.array([kronecker(D, int(p)) for p in pr])
        cum = np.cumsum(chi.astype(float))
        idx = np.clip(np.searchsorted(pr, xs, "right")-1, 0, len(cum)-1)
        sig += cum[idx]
    env = np.sqrt(xs)/np.log(xs)
    s = sig/env
    t = np.arange(n_samples)
    s = s - np.polyval(np.polyfit(t, s, 3), t)
    return xs, s

def music_freqs(s, K, dn, grid):
    a = hilbert(s); N = len(a); M = N//2; L = N-M+1
    X = np.array([a[k:k+M] for k in range(L)]).T
    R = X @ X.conj().T / L
    w, V = np.linalg.eigh(R); En = V[:, :M-K]
    m = np.arange(M)
    P = np.array([1/(abs(En.conj().T @ np.exp(1j*g*dn*m))**2).sum() for g in grid])
    pk = [i for i in range(1,len(P)-1) if P[i]>P[i-1] and P[i]>P[i+1]]
    pk.sort(key=lambda i:-P[i]); return np.sort(grid[[pk[:K]]].ravel()) if pk else np.array([])

def fft_freqs(s, K, dn, grid, pad=16):
    w = np.hanning(len(s)); m = np.arange(len(s))
    P = np.array([abs((s*w) @ np.exp(-1j*g*dn*m))**2 for g in grid])
    pk = [i for i in range(1,len(P)-1) if P[i]>P[i-1] and P[i]>P[i+1]]
    pk.sort(key=lambda i:-P[i]); return np.sort(grid[pk[:K]]) if pk else np.array([])

def resolves(pair, freqs, tol):
    """both members of pair matched by distinct found freqs within tol."""
    if len(freqs) < 2: return False
    used=set(); ok=0
    for g in pair:
        cand=[(abs(f-g),j) for j,f in enumerate(freqs) if j not in used]
        if cand:
            d,j=min(cand)
            if d<tol: used.add(j); ok+=1
    return ok==2

def main():
    print("Finding closest cross-character low-zero pair...")
    allz=[]
    for D in FUND_D:
        z=low_zeros(D)
        for g in z: allz.append((g,D))
        print(f"  D={D:>4} zeros<20: {z}")
    allz.sort()
    zeros_by_D={D:lz for D,lz in [(D,[g for g,DD in allz if DD==D]) for D in FUND_D]}
    best=None
    for i in range(len(allz)):
        for j in range(i+1,len(allz)):
            (g1,D1),(g2,D2)=allz[i],allz[j]
            if D1!=D2:
                d=g2-g1
                # low-gamma pair: feasible Fourier threshold + strong amplitude
                if 0.35<=d<=0.55 and g2<10.5 and (best is None or d<best[0]):
                    best=(d,(g1,D1),(g2,D2))
    d,(g1,D1),(g2,D2)=best
    print(f"\nClosest cross pair in [0.35,0.55]: gamma={g1} (D={D1}) & {g2} (D={D2}), sep={d:.4f}")
    fourier_X = math.exp(2*math.pi/d)
    print(f"Fourier limit to resolve sep={d:.3f}: log X ~ {2*math.pi/d:.1f} -> X ~ {fourier_X:.2e}")
    pair=(g1,g2); tol=d/3

    Xmax=150_000_000
    print(f"Sieving to {Xmax:,} and precomputing chi cumulants...")
    t0=time.time(); primes=sieve(Xmax)
    chiA=np.array([kronecker(D1,int(p)) for p in primes],float); cumA=np.cumsum(chiA)
    chiB=np.array([kronecker(D2,int(p)) for p in primes],float); cumB=np.cumsum(chiB)
    print(f"  {len(primes):,} primes, chi precompute {time.time()-t0:.0f}s")

    def sig_at(X,n):
        log_xs=np.linspace(math.log(100),math.log(X),n); xs=np.exp(log_xs)
        idx=np.clip(np.searchsorted(primes,xs,"right")-1,0,len(cumA)-1)
        s=(cumA[idx]+cumB[idx])/(np.sqrt(xs)/np.log(xs))
        t=np.arange(n); return xs, s-np.polyval(np.polyfit(t,s,3),t)

    all_low=sorted(set([round(g,4) for g,_ in allz]))
    print(f"\nSweep X: resolve the pair? MUSIC given ORACLE source count K. (tol={tol:.3f})")
    print(f"  {'X':>13} {'n':>5} {'K':>3} {'dn':>7} {'FourierRes':>11} {'FFT':>5} {'MUSIC':>6}")
    for X in [1e6,1e7,3e7,6e7,1e8,1.5e8]:
        X=int(X)
        if X>Xmax: break
        n=max(80,int(40*math.log10(X)))
        dn=(math.log(X)-math.log(100))/(n-1); nyq=math.pi/dn
        if nyq < g2:
            print(f"  {X:13,} {n:5d}     {dn:7.4f}  (Nyquist<{g2:.1f}, skip)"); continue
        # oracle K = number of distinct zeros (either char) below Nyquist
        K=sum(1 for g in all_low if g < nyq)
        K=min(K, n//2 - 1)
        grid=np.linspace(min(g1,g2)-1.0, max(g1,g2)+1.0, 4000)
        xs,s=sig_at(X,n)
        fft_ok=resolves(pair, fft_freqs(s,2,dn,grid), tol)
        mus_ok=resolves(pair, music_freqs(s,K,dn,grid), tol)
        fres=2*math.pi/math.log(X)
        print(f"  {X:13,} {n:5d} {K:3d} {dn:7.4f} {fres:11.3f} {str(fft_ok):>5} {str(mus_ok):>6}")

if __name__=="__main__":
    main()
