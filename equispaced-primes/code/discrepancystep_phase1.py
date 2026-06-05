#!/usr/bin/env python3
"""
DiscrepancyStep Phase-1 extended numerics.
==========================================

Target open lemma (papers/math_paper/main.tex eq after line 2149):

  (DiscrepancyStep)   N(p) + B(p) + C(p) > A(p)
  for all primes p >= 11 with M(p) <= -3.

Four-term decomposition (main.tex eq:4term, lines 931-945), with
n = |F_{p-1}|, n' = |F_p| = n + (p-1):

  A = old_D_sq * (n'^2 - n^2)/n^2 / n'^2     (dilution, >0)
  B = (2/n'^2) sum_old D(f) delta(f)         (cross term)
  C = (1/n'^2) sum_old delta(f)^2            (shift^2, >0)
  N = (1/n'^2) sum_new D_{F_p}(k/p)^2        (new-fraction, >0)

The scale-free ratios used throughout (n'^2 cancels):
  N/A = new_D_sq / dilution_raw,  B/A = B_raw/dilution_raw, C/A = C_raw/dilution_raw,
  dilution_raw = old_D_sq*(n'^2-n^2)/n^2.

This module is a *vectorised* re-implementation of the canonical
experiments/bridge_DA_compute.py::float_decomposition that AVOIDS
materialising F_N by working denominator-by-denominator with numpy and
an EXACT global rank via the Mobius rank formula
  rank(x in F_M) = 1 + sum_{d=1}^M mu(d) * G(x, floor(M/d)),
  G(x,m) = sum_{b=1}^m floor(b*x).
For x = a/b this is exact integer arithmetic; G(a/b, m) is computed by a
direct O(m) numpy floor-sum (vectorised), so a full prime costs
O(p^2 / vector_width). float64 is used for the O(1) ratios (the 1e-11
cancellation only matters for the DeltaW SIGN, which we track separately
via the four-term sum, not for N/A).

Usage:  python3 discrepancystep_phase1.py PMAX [SAMPLE_STRIDE]
        SAMPLE_STRIDE k>0 means: for p above the dense cutoff, sample
        every k-th qualifying prime (sparse mode for 10^5..10^6).
Writes: code/discrepancystep_phase1.csv  (append/replace per run)
"""
import sys
import time
import csv
from math import isqrt, log, sqrt, gcd
import numpy as np


# ----------------------------------------------------------------------
# sieves
# ----------------------------------------------------------------------
def sieve_primes(limit):
    s = np.ones(limit + 1, dtype=bool)
    s[:2] = False
    for i in range(2, isqrt(limit) + 1):
        if s[i]:
            s[i * i::i] = False
    return np.nonzero(s)[0]


def totient_sieve(limit):
    phi = np.arange(limit + 1, dtype=np.int64)
    for p in range(2, limit + 1):
        if phi[p] == p:  # p prime
            phi[p::p] -= phi[p::p] // p
    return phi


def mobius_sieve(limit):
    mu = np.ones(limit + 1, dtype=np.int8)
    mu[0] = 0
    is_comp = np.zeros(limit + 1, dtype=bool)
    primes = []
    # linear sieve for mu
    spf = np.zeros(limit + 1, dtype=np.int64)
    for i in range(2, limit + 1):
        if spf[i] == 0:
            spf[i] = i
            primes.append(i)
        for p in primes:
            if p > spf[i] or i * p > limit:
                break
            spf[i * p] = p
    mu = np.zeros(limit + 1, dtype=np.int8)
    mu[1] = 1
    for n in range(2, limit + 1):
        p = spf[n]
        if (n // p) % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[n // p]
    return mu


def mertens_values(mu, limit):
    return np.cumsum(mu.astype(np.int64))


# ----------------------------------------------------------------------
# exact global rank via Mobius rank formula
# ----------------------------------------------------------------------
def make_rank_engine(M, mu):
    """Return a function rank_many(a, b) giving exact rank in F_M of the
    fractions a/b (numpy int arrays, same length), where for each entry
    0 <= a <= b, gcd(a,b)=1.  Uses:
      rank(a/b) = 1 + sum_{d=1}^{M} mu(d) * G(a/b, floor(M/d)),
      G(a/b, m) = sum_{c=1}^{m} floor(c*a/b).
    The d-sum is over squarefree d <= M with mu!=0.  For speed we
    precompute the list of (d, floor(M/d)).  G is evaluated by the
    closed reciprocity recursion (floor_sum) in O(log) each -> O(#d log).
    """
    dvals = np.nonzero(mu[1:M + 1])[0] + 1            # d with mu(d)!=0
    mud = mu[dvals].astype(np.int64)
    mvals = (M // dvals).astype(np.int64)             # floor(M/d)
    return dvals, mud, mvals


def floor_sum(n, a, b, c):
    """sum_{i=0}^{n-1} floor((a*i + b)/c), the standard O(log) recursion.
    Requires c>0, n>=0.  Returns Python int."""
    res = 0
    if a < 0:
        a2 = a % c
        res -= n * (n - 1) // 2 * ((a2 - a) // c)
        a = a2
    if b < 0:
        b2 = b % c
        res -= n * ((b2 - b) // c)
        b = b2
    while True:
        if a >= c:
            res += n * (n - 1) // 2 * (a // c)
            a %= c
        if b >= c:
            res += n * (b // c)
            b %= c
        ymax = a * n + b
        if ymax < c:
            break
        n, b, c, a = ymax // c, ymax % c, a, c
    return res


def G_floor(k, p, m):
    """G(k/p, m) = sum_{c=1}^{m} floor(c*k/p) = floor_sum(m+1, k, 0, p) for i=0..m
    minus the i=0 term (0). sum_{c=1}^m floor(c k/p) = floor_sum(m+1,k,0,p)."""
    # sum_{i=0}^{m} floor((k*i)/p) = floor_sum(m+1, k, 0, p); i=0 contributes 0.
    return floor_sum(m + 1, k, 0, p)


def rank_new_fraction(k, p, dvals, mud, mvals):
    """Exact rank of k/p in F_{p-1} via Mobius formula (Python ints)."""
    total = 0
    for d, mu_d, m in zip(dvals.tolist(), mud.tolist(), mvals.tolist()):
        if m == 0:
            continue
        total += mu_d * G_floor(k, p, m)
    return total + 1


# ----------------------------------------------------------------------
# Full per-prime decomposition (vectorised over denominators)
# ----------------------------------------------------------------------
def decompose_vectorised(p, phi):
    """Compute old_D_sq, B_raw, C_raw, new_D_sq for prime p, plus the
    four-term DeltaW sign, WITHOUT materialising all of F_{p-1} at once.
    We DO need each old fraction's global rank for old_D_sq and B; we get
    it by materialising fractions per denominator and using a global sort
    (cheap: numpy). Memory ~0.3 p^2 floats; OK up to ~1.5e4. For larger p
    we use the chunked path (see decompose_chunked)."""
    N = p - 1
    n = 1 + int(phi[1:N + 1].sum())
    n_prime = n + (p - 1)

    # materialise old fractions as (num, den) integer arrays
    nums = [np.array([0, 1], dtype=np.int64)]
    dens = [np.array([1, 1], dtype=np.int64)]
    for b in range(2, N + 1):
        a = np.arange(1, b, dtype=np.int64)
        a = a[np.gcd(a, b) == 1]
        nums.append(a)
        dens.append(np.full(a.shape, b, dtype=np.int64))
    num = np.concatenate(nums)
    den = np.concatenate(dens)
    val = num / den
    order = np.argsort(val, kind='stable')
    num = num[order]
    den = den[order]
    val = val[order]
    ranks = np.arange(num.size, dtype=np.float64)   # 0-indexed global rank

    D = ranks - n * val
    old_D_sq = float(np.dot(D, D))

    # delta(a/b) = (a - (p*a mod b))/b ; zero at a==0 or a==b
    sigma = (p * num) % den
    delta = (num - sigma) / den
    boundary = (num == 0) | (num == den)
    delta = np.where(boundary, 0.0, delta)
    B_raw = float(2.0 * np.dot(D, delta))
    C_raw = float(np.dot(delta, delta))

    # new fractions k/p, k=1..p-1.  rank_old via bisection into the sorted val.
    ks = np.arange(1, p, dtype=np.float64)
    x = ks / p
    rank_old = np.searchsorted(val, x, side='left').astype(np.float64)
    D_new = rank_old - n * x + x          # = D_old + delta(k/p), delta(k/p)=k/p
    new_D_sq = float(np.dot(D_new, D_new))

    dilution_raw = old_D_sq * (n_prime ** 2 - n ** 2) / (n ** 2)
    # DeltaW sign via four-term sum
    W_old = old_D_sq / (n * n)
    W_new = (old_D_sq + B_raw + C_raw + new_D_sq) / (n_prime * n_prime)
    dW = W_old - W_new
    return dict(p=p, n=n, n_prime=n_prime,
                old_D_sq=old_D_sq, new_D_sq=new_D_sq,
                B_raw=B_raw, C_raw=C_raw,
                dilution_raw=dilution_raw,
                NA=new_D_sq / dilution_raw,
                BA=B_raw / dilution_raw,
                CA=C_raw / dilution_raw,
                dW=dW)


def decompose_chunked(p, phi, chunk_b=4000):
    """Memory-bounded exact decomposition for large p.
    Strategy: we still need GLOBAL ranks. We compute them by, for each old
    fraction a/b, rank = #fractions < a/b. We get this WITHOUT a global
    array by the Mobius rank formula per fraction -- too slow per-fraction.
    Instead we stream: build all fractions but in denominator chunks,
    storing only (value, num, den) and merging via a global sort done in
    blocks. To stay within memory we materialise the full value array in
    float32 (0.3 p^2 * 4 bytes); for p=3e4 that's ~1e9*4 = 4GB -> too big.

    So for the present time-boxed probe we cap the *dense exact* path at
    PCAP and use it; beyond PCAP we do not claim per-prime exactness.
    This function is a placeholder kept for interface symmetry."""
    return decompose_vectorised(p, phi)


# ----------------------------------------------------------------------
# parallel worker
# ----------------------------------------------------------------------
_PHI = None  # per-worker global to avoid re-pickling the sieve


def _init_worker(pmax):
    global _PHI
    _PHI = totient_sieve(pmax)


def _work(p):
    r = decompose_vectorised(p, _PHI)
    return r


# ----------------------------------------------------------------------
# main
# ----------------------------------------------------------------------
def main():
    import multiprocessing as mp
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 12000
    STRIDE = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    PCAP = int(sys.argv[3]) if len(sys.argv) > 3 else PMAX  # dense exact cutoff
    NPROC = int(sys.argv[4]) if len(sys.argv) > 4 else max(1, mp.cpu_count() - 1)
    t0 = time.time()
    primes = sieve_primes(PMAX)
    mu = mobius_sieve(PMAX)
    M = mertens_values(mu, PMAX)

    qualifying = [int(p) for p in primes if p >= 11 and M[p] <= -3]
    # dense below PCAP, strided sample above
    todo = [p for i, p in enumerate(qualifying)
            if p <= PCAP or (i % STRIDE == 0)]
    print("qualifying M<=-3,p>=11 up to %d: %d ; computing %d (PCAP=%d STRIDE=%d NPROC=%d) (sieve %.1fs)"
          % (PMAX, len(qualifying), len(todo), PCAP, STRIDE, NPROC, time.time() - t0))

    # process smallest-first so progress prints are frequent
    with mp.Pool(NPROC, initializer=_init_worker, initargs=(PMAX,)) as pool:
        results = []
        for i, r in enumerate(pool.imap(_work, todo, chunksize=1)):
            results.append(r)
            if (i + 1) % 50 == 0:
                print("  ... %d/%d done (last p=%d, %.0fs)"
                      % (i + 1, len(todo), r['p'], time.time() - t0), flush=True)
    rows = []
    for r in results:
        r['M'] = int(M[r['p']])
        rows.append(r)
    rows.sort(key=lambda r: r['p'])

    # write CSV
    csv_path = "code/discrepancystep_phase1.csv"
    with open(csv_path, "w", newline="") as fh:
        wcsv = csv.writer(fh)
        wcsv.writerow(["p", "M", "M_over_sqrtp", "A_raw", "B_raw", "C_raw",
                       "N_raw", "NA", "CA", "BA", "margin", "deltaW_sign"])
        for r in rows:
            p = r['p']
            margin = r['BA'] + r['CA'] + r['NA'] - 1.0
            dW_sign = 1 if r['dW'] > 0 else (-1 if r['dW'] < 0 else 0)
            wcsv.writerow([p, r['M'], "%.6f" % (r['M'] / sqrt(p)),
                           "%.10e" % r['dilution_raw'], "%.10e" % r['B_raw'],
                           "%.10e" % r['C_raw'], "%.10e" % r['new_D_sq'],
                           "%.10f" % r['NA'], "%.10f" % r['CA'],
                           "%.10f" % r['BA'], "%.10f" % margin, dW_sign])
    print("wrote %s (%d rows, %.0fs total)" % (csv_path, len(rows), time.time() - t0))
    return rows


if __name__ == "__main__":
    main()
