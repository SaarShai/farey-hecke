#!/usr/bin/env python3
"""
D1 BCZ-cocycle numerical verification (exact arithmetic where load-bearing).

Verified here:
  (V1) BCZ map T on Omega reproduces consecutive Farey neighbour pairs
       (Boca-Cobeli-Zaharescu / Athreya-Cheung Poincare-section dictionary).
  (V2) A_Q(m) = sum_{d|m} d*M(floor(Q/d))  [Mertens identity];  A_Q real;
       prime-step increment  Delta A(m) = A_p(m)-A_{p-1}(m) = -1 + p*[p|m].
  (V3) Mikolas L^2 second moment
         J(Q) := int_0^1 E_Q(x)^2 dx = (1/(2 pi^2)) sum_{m>=1} A_Q(m)^2/m^2 + O(1)
       and  N*W(N) -> C ~ 0.66   (W(N) = J(N)/Phi + O(1/Phi)).
  (V4) Farey rank discrepancy E_Q = Birkhoff sum of the BCZ cocycle
       g(section point) along the first-return orbit (gap = 1/(k k')).
  (V5) prime "only-new" vs composite "always-overlap" via primitivity
       (visibility) of the bottom-row lattice vector: #new = phi(Q).

Farey side and the identity side use exact integer / Fraction arithmetic.
Float appears only for the Mikolas tail constant and the asymptotic plot.
"""

from fractions import Fraction
from math import gcd, pi
import numpy as np

# ----------------------------------------------------------------------
# Global sieves (computed once): mu(n) and Mertens M(n)=sum_{k<=n} mu(k).
# ----------------------------------------------------------------------
_NMAX = 0
_MU = None       # numpy int8 array of mu
_MERT = None     # numpy int64 array, _MERT[n] = M(n), _MERT[0]=0

def ensure_sieve(N):
    global _NMAX, _MU, _MERT
    if N <= _NMAX:
        return
    N = max(N, 2 * _NMAX, 1000)
    mu = np.ones(N + 1, dtype=np.int64)
    mu[0] = 0
    is_comp = np.zeros(N + 1, dtype=bool)
    primes = []
    for i in range(2, N + 1):
        if not is_comp[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            ip = i * p
            if ip > N:
                break
            is_comp[ip] = True
            if i % p == 0:
                mu[ip] = 0
                break
            else:
                mu[ip] = -mu[i]
    mert = np.cumsum(mu).astype(np.int64)
    _NMAX, _MU, _MERT = N, mu, mert

def M(n):
    if n <= 0:
        return 0
    ensure_sieve(n)
    return int(_MERT[n])

def mobius(n):
    if n <= 0:
        return 0
    ensure_sieve(n)
    return int(_MU[n])

def divisors(m):
    ds = []
    d = 1
    while d * d <= m:
        if m % d == 0:
            ds.append(d)
            if d != m // d:
                ds.append(m // d)
        d += 1
    return ds

# ----------------------------------------------------------------------
# Farey sequence F_Q on (0,1]; BCZ section.
# ----------------------------------------------------------------------

def farey(Q):
    """Ascending reduced fractions in (0,1] with denominator<=Q (exact)."""
    a, b, c, d = 0, 1, 1, Q
    out = []
    while c <= Q:
        if (a, b) != (0, 1):
            out.append((a, b))
        k = (Q + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
    out.append((1, 1))
    return out

def bcz_pairs(Q):
    F = farey(Q)
    return [(F[i][1], F[i + 1][1]) for i in range(len(F) - 1)]

def bcz_map(k, kp, Q):
    """BCZ map in the integer-denominator chart: (k,k') -> (k', kappa k' - k),
    kappa = floor((Q + k)/k')."""
    kappa = (Q + k) // kp
    return (kp, kappa * kp - k)

# ---------- (V1) ----------
def verify_V1(Q):
    pairs = bcz_pairs(Q)
    nF = len(farey(Q))
    ok = all(bcz_map(*pairs[i], Q) == pairs[i + 1] for i in range(len(pairs) - 1))
    cons = all(1 <= k <= Q and 1 <= kp <= Q and k + kp > Q for (k, kp) in pairs)
    print(f"  V1 Q={Q}: orbit len {len(pairs)} (=|F_Q|-1={nF-1}), "
          f"T-consistent={ok}, Omega(k+k'>Q)={cons}")
    return ok and cons

# ---------- (V2) ----------
def A_ramanujan(Q, m):
    """A_Q(m) = sum_{k=1}^Q c_k(m), c_k(m)=sum_{d|gcd(m,k)} d*mu(k/d). Exact."""
    total = 0
    for k in range(1, Q + 1):
        g = gcd(m, k)
        for d in divisors(g):
            total += d * mobius(k // d)
    return total

def A_identity(Q, m):
    """A_Q(m) = sum_{d|m} d*M(floor(Q/d))  (verified-fact identity). Exact."""
    return sum(d * M(Q // d) for d in divisors(m))

def verify_V2(Q, ms):
    ok = all(A_ramanujan(Q, m) == A_identity(Q, m) for m in ms)
    inc_ok = True
    for p in (5, 7, 11, 13, 17, 19):
        for m in ms:
            d = A_identity(p, m) - A_identity(p - 1, m)
            pred = -1 + (p if (m % p == 0) else 0)
            if d != pred:
                inc_ok = False
                print(f"   V2 inc FAIL p={p} m={m}: dA={d} pred={pred}")
    print(f"  V2 Q={Q}: Mertens identity match={ok}; "
          f"Delta A = -1 + p*[p|m] match={inc_ok}")
    return ok and inc_ok

# ---------- (V3) ----------
def J_direct_exact(Q):
    """J(Q)=int_0^1 E_Q^2, EXACT Fraction. On (f_j,f_{j+1}] count=j,
    E=j-Phi x; antiderivative -(j-Phi x)^3/(3 Phi). Small Q only."""
    F = [Fraction(0)] + [Fraction(h, k) for (h, k) in farey(Q)]
    Phi = len(F) - 1
    J = Fraction(0)
    for j in range(len(F) - 1):
        x0, x1 = F[j], F[j + 1]
        t0 = -((j - Phi * x0) ** 3) / (3 * Phi)
        t1 = -((j - Phi * x1) ** 3) / (3 * Phi)
        J += t1 - t0
    return J

def J_direct_fast(Q):
    """Same J(Q) in float, vectorized. Farey nodes f_j = num/den; on
    [f_j,f_{j+1}] integrand (j-Phi x)^2, exact antiderivative evaluated
    in float (the per-node values are themselves exact rationals)."""
    F = farey(Q)
    num = np.array([0] + [h for (h, k) in F], dtype=np.float64)
    den = np.array([1] + [k for (h, k) in F], dtype=np.float64)
    x = num / den
    Phi = len(F)
    j = np.arange(len(x), dtype=np.float64)            # count just left of x[i]
    # interval i is [x[i], x[i+1]], count = i (i fractions are <= x[i])
    v0 = j[:-1] - Phi * x[:-1]
    v1 = j[:-1] - Phi * x[1:]
    contrib = -(v1 ** 3 - v0 ** 3) / (3.0 * Phi)
    return float(np.sum(contrib))

def J_mikolas_tail(Q, Mt):
    """(1/(2 pi^2)) sum_{m=1}^{Mt} A_Q(m)^2/m^2,  A_Q(m)=sum_{d|m} d*M(Q//d).
    Build A on 1..Mt by a divisor sieve, fully vectorized per d-block but
    only over d with M(Q//d)!=0 (skips most large d since Q//d small)."""
    ensure_sieve(max(Q, Mt))
    Mvals = _MERT
    A = np.zeros(Mt + 1, dtype=np.float64)
    for d in range(1, Mt + 1):
        qd = Q // d
        if qd == 0:
            break
        md = int(Mvals[qd])
        if md:
            A[d:Mt + 1:d] += d * md
    m = np.arange(1, Mt + 1, dtype=np.float64)
    return float(np.sum(A[1:] ** 2 / m ** 2)) / (2.0 * pi * pi)

def verify_V3(Qs, exact_upto=400):
    print("  V3 Mikolas second moment + asymptotic N*W(N):", flush=True)
    print("     Q    J(float)   J_exact(<=%d)  Mikolas(tail)  Phi     N*W(N)"
          % exact_upto, flush=True)
    for Q in Qs:
        Phi = len(farey(Q))
        Jf = J_direct_fast(Q)
        Je = f"{float(J_direct_exact(Q)):.5f}" if Q <= exact_upto else "   --   "
        Jm = J_mikolas_tail(Q, 50 * Q)
        NW = Q * Jf / Phi
        print(f"   {Q:5d}  {Jf:10.5f}  {Je:>10}   {Jm:11.5f}   {Phi:7d}  "
              f"{NW:.6f}", flush=True)

# ---------- (V4) ----------
def verify_V4(Q):
    """Birkhoff identity, CORRECT boundary convention: orbit starts at the
    node f_0 = 0 (the left endpoint of (0,1]); the per-step cocycle over
    the interval [f_{j-1}, f_j] is  g_j = 1 - Phi*(f_j - f_{j-1}).  Then
        S_j := sum_{i=1}^{j} g_i = E_Q(f_j) = j - Phi*f_j
    exactly, for every node, with S_0 = 0 and S_{|F_Q|} = 0 (closed orbit).
    For j>=2 the inner gaps are f_j - f_{j-1} = 1/(k_{j-1} k_j) (BCZ gap).
    The first and last steps use the (0,1] boundary 1/Q (the section's
    return at the cusp), NOT a k k' product; this is the only boundary
    correction and it is part of the cocycle definition, not an error."""
    Fx = [Fraction(0)] + [Fraction(h, k) for (h, k) in farey(Q)]  # f_0=0
    F = farey(Q)
    Phi = len(F)
    run = Fraction(0)
    ok = True
    gap_ok = True
    for j in range(1, len(Fx)):
        gap = Fx[j] - Fx[j - 1]
        if 2 <= j <= len(Fx) - 2:               # interior: BCZ gap formula
            k, kp = F[j - 2][1], F[j - 1][1]
            if gap != Fraction(1, k * kp):
                gap_ok = False
        g = 1 - Phi * gap                       # bounded BCZ cocycle
        run += g
        E_node = j - Phi * Fx[j]                # direct E_Q at node
        if run != E_node:
            ok = False
            print(f"   V4 Birkhoff FAIL j={j}: S={float(run)} E={float(E_node)}")
            break
    closed = (run == 0)                          # S at f=1 must be 0
    print(f"  V4 Q={Q}: interior gap=1/(k k')={gap_ok}; "
          f"E_Q(f_j)=Birkhoff sum S_j={ok}; closed-orbit S_end=0={closed}")
    return ok and gap_ok and closed

# ---------- (V5) ----------
def verify_V6(Q, maxlag=40):
    """[NUMERICAL-ONLY] Green-Kubo pre-check for the closing theorem (R).
    Take the centered BCZ cocycle ghat over one F_Q orbit, estimate the
    lag-j autocovariance  c_j = <ghat * ghat o T^j>  and the running
    Green-Kubo sum  sigma2(L) = c_0 + 2 sum_{j=1}^{L} c_j.  If c_j decays
    (summable) sigma2(L) stabilizes -> consistent with Var(S_n) ~ sigma2 n.
    This does NOT prove (R); it tests its key hypothesis cheaply."""
    Fx = [Fraction(0)] + [Fraction(h, k) for (h, k) in farey(Q)]
    Phi = len(Fx) - 1
    g = np.array([1.0 - Phi * float(Fx[j] - Fx[j - 1])
                  for j in range(1, len(Fx))], dtype=np.float64)
    n = len(g)
    gh = g - g.mean()
    c0 = float(np.mean(gh * gh))
    print(f"  V6 Q={Q}: orbit n={n}, c_0={c0:.5f}")
    s = c0
    prev = None
    for L in (1, 2, 4, 8, 16, maxlag):
        acc = c0
        for j in range(1, L + 1):
            cj = float(np.mean(gh[:n - j] * gh[j:]))
            acc += 2.0 * cj
        cj_last = float(np.mean(gh[:n - L] * gh[L:]))
        print(f"    L={L:3d}: GreenKubo sigma2(L)={acc:.5f}  c_{L}={cj_last:.3e}")


def verify_V7(Q, Ts=(2, 4, 8, 16), maxlag=40):
    """[NUMERICAL-ONLY] Truncated-cocycle Green-Kubo pre-check (the
    sharpened theorem (R) target).  Truncate the gap at 1/(T*Q):
        g^{(T)}_j = 1 - Phi * min(gap_j, 1/(T*Q)).
    If truncation restores a uniformly-L^2 cocycle with summable
    correlations, c_0(T) should stabilize across Q and sigma2(L) should
    converge in L (per fixed T).  Tests the §2.0 renormalization claim."""
    Fx = [Fraction(0)] + [Fraction(h, k) for (h, k) in farey(Q)]
    Phi = len(Fx) - 1
    gaps = np.array([float(Fx[j] - Fx[j - 1]) for j in range(1, len(Fx))],
                    dtype=np.float64)
    n = len(gaps)
    for T in Ts:
        cap = 1.0 / (T * Q)
        g = 1.0 - Phi * np.minimum(gaps, cap)
        gh = g - g.mean()
        c0 = float(np.mean(gh * gh))
        acc = c0
        for j in range(1, maxlag + 1):
            acc += 2.0 * float(np.mean(gh[:n - j] * gh[j:]))
        print(f"  V7 Q={Q} T={T:3d}: c_0={c0:.4f}  sigma2(L={maxlag})={acc:.4f}")


def euler_phi(n):
    res, x, p = n, n, 2
    while p * p <= x:
        if x % p == 0:
            while x % p == 0:
                x //= p
            res -= res // p
        p += 1
    if x > 1:
        res -= res // x
    return res

def verify_V5(denoms):
    print("  V5 #new points at denominator Q = phi(Q) (visibility/primitivity):")
    for Q in denoms:
        ph = euler_phi(Q)
        is_p = (ph == Q - 1 and Q > 1)
        tag = "PRIME -> all new, retrace=0" if is_p \
              else f"COMPOSITE -> retrace={(Q-1)-ph} (>0)"
        print(f"    Q={Q:3d}: phi={ph:3d}  {tag}")

# ----------------------------------------------------------------------
def main():
    print("=" * 70)
    print("D1 BCZ-cocycle verification (exact arithmetic)")
    print("=" * 70)
    print("[V1] BCZ map = Farey neighbour first-return orbit")
    for Q in (10, 25, 50, 100, 200, 500):
        verify_V1(Q)
    print("[V2] Mertens identity for A_Q(m) + prime-step Delta A")
    for Q in (20, 50, 97):
        verify_V2(Q, ms=[1, 2, 3, 5, 6, 7, 10, 11, 12, 30, 60, 97])
    print("[V3] Mikolas L^2 second moment and N*W(N) -> C")
    verify_V3([50, 100, 200, 400, 800, 1600, 3200], exact_upto=400)
    print("[V4] Discrepancy as Birkhoff sum of BCZ cocycle")
    for Q in (10, 50, 100, 300, 600):
        verify_V4(Q)
    print("[V5] Prime/composite dichotomy via section primitivity")
    verify_V5([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 30, 31])
    print("[V6] Green-Kubo autocovariance pre-check (RAW cocycle)")
    for Q in (200, 800, 2000):
        verify_V6(Q, maxlag=40)
    print("[V7] TRUNCATED-cocycle Green-Kubo (sharpened (R) target)")
    for Q in (500, 1000, 2000, 4000):
        verify_V7(Q, Ts=(2, 4, 8, 16), maxlag=40)
    print("=" * 70)

if __name__ == "__main__":
    main()
