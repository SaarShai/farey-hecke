#!/usr/bin/env python3
"""
DiscrepancyStep numerical feasibility probe.
============================================

Target open lemma (papers/math_paper/main.tex eq after line 2149):

  (DiscrepancyStep)   N(p) + B(p) + C(p) > A(p)
  for all primes p >= 11 with M(p) <= -3.

Four-term decomposition (main.tex eq:4term, lines 931-945), with
n=|F_{p-1}|, n'=|F_p|=n+(p-1):

  A = sum_old D_{F_{p-1}}(f)^2 * (1/n^2 - 1/n'^2)        (dilution, >0)
  B = (2/n'^2) sum D_{F_{p-1}}(f) * delta(f)             (cross term)
  C = (1/n'^2) sum delta(f)^2                            (shift^2, >0)
  N = (1/n'^2) sum_new D_{F_p}(k/p)^2                    (new-fraction, >0)

  D(f_j) = j - n*f_j          (rank discrepancy, main.tex:300-301)
  delta(f) = f - {p f}        (shift, main.tex:304-307)

Ratios are scale-free: dividing A,B,C,N by the common pieces,
  N/A = new_D_sq / dilution_raw,  B/A = B_raw/dilution_raw,  C/A = C_raw/dilution_raw
where dilution_raw = old_D_sq*(n'^2-n^2)/n^2, new_D_sq = sum_new D_{F_p}(k/p)^2
(raw, undivided), B_raw = 2 sum D*delta, C_raw = sum delta^2.

This reuses the canonical float algorithm of
experiments/bridge_DA_compute.py::float_decomposition (re-implemented
here standalone) and adds the tabulation/fit the scoping doc needs.

Usage:  python3 discrepancystep_probe.py [PMAX]   (default 20000)
Writes: code/discrepancystep_probe_out.txt
"""
import sys
import time
from math import gcd, isqrt, log
import bisect


def sieve_primes(limit):
    s = [True] * (limit + 1)
    s[0] = s[1] = False
    for i in range(2, isqrt(limit) + 1):
        if s[i]:
            for j in range(i * i, limit + 1, i):
                s[j] = False
    return [i for i in range(2, limit + 1) if s[i]]


def totient_sieve(limit):
    phi = list(range(limit + 1))
    for p in range(2, limit + 1):
        if phi[p] == p:  # p prime
            for k in range(p, limit + 1, p):
                phi[k] -= phi[k] // p
    return phi


def mobius_sieve(limit):
    spf = [0] * (limit + 1)
    for i in range(2, limit + 1):
        if spf[i] == 0:
            for j in range(i, limit + 1, i):
                if spf[j] == 0:
                    spf[j] = i
    mu = [0] * (limit + 1)
    mu[1] = 1
    for n in range(2, limit + 1):
        p = spf[n]
        if (n // p) % p == 0:
            mu[n] = 0
        else:
            mu[n] = -mu[n // p]
    return mu


def mertens_values(mu, limit):
    M = [0] * (limit + 1)
    acc = 0
    for n in range(1, limit + 1):
        acc += mu[n]
        M[n] = acc
    return M


def farey_generator(N):
    """Yield (a,b) of F_N in ascending order via the standard recurrence."""
    a, b, c, d = 0, 1, 1, N
    yield (a, b)
    while c <= N:
        yield (c, d)
        k = (N + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b


def farey_size(N, phi):
    return 1 + sum(phi[k] for k in range(1, N + 1))


def decompose(p, phi):
    """Float four-term decomposition; returns ratios N/A, B/A, C/A and delta_W."""
    N = p - 1
    n = farey_size(N, phi)
    n_prime = n + p - 1

    old = list(farey_generator(N))
    fvals = [a / b for (a, b) in old]

    old_D_sq = 0.0
    B_raw = 0.0
    C_raw = 0.0
    for idx, (a, b) in enumerate(old):
        f = a / b
        D = idx - n * f
        old_D_sq += D * D
        if a == 0 or a == b:
            delta = 0.0
        else:
            sigma = (p * a) % b
            delta = (a - sigma) / b
        B_raw += 2.0 * D * delta
        C_raw += delta * delta

    sum_Dold_sq = 0.0
    sum_kp_Dold = 0.0
    sum_kp_sq = 0.0
    for k in range(1, p):
        x = k / p
        rank_old = bisect.bisect_left(fvals, x)
        D_old_x = rank_old - n * x
        sum_Dold_sq += D_old_x * D_old_x
        sum_kp_Dold += x * D_old_x
        sum_kp_sq += x * x
    # D_{F_p}(k/p) = D_{F_{p-1}}(k/p) + delta(k/p) and delta(k/p)=k/p (since {p*k/p}=0)
    new_D_sq = sum_Dold_sq + 2.0 * sum_kp_Dold + sum_kp_sq

    dilution_raw = old_D_sq * (n_prime ** 2 - n ** 2) / (n ** 2)
    NA = new_D_sq / dilution_raw
    BA = B_raw / dilution_raw
    CA = C_raw / dilution_raw

    W_old = old_D_sq / (n * n)
    W_new = (old_D_sq + B_raw + C_raw + new_D_sq) / (n_prime * n_prime)
    dW = W_old - W_new  # ΔW; <0 means wobble worsens
    return dict(p=p, n=n, n_prime=n_prime, NA=NA, BA=BA, CA=CA, dW=dW)


def main():
    PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    t0 = time.time()
    primes = sieve_primes(PMAX)
    phi = totient_sieve(PMAX)
    mu = mobius_sieve(PMAX)
    M = mertens_values(mu, PMAX)

    rows = []
    for p in primes:
        if p < 11:
            continue
        if M[p] > -3:
            continue
        r = decompose(p, phi)
        r['M'] = M[p]
        rows.append(r)

    out = []

    def w(line=""):
        out.append(line)

    w("DiscrepancyStep probe  PMAX=%d  primes(M<=-3,p>=11)=%d  elapsed=%.1fs"
      % (PMAX, len(rows), time.time() - t0))
    w("")
    # margins / extremes
    margins = [(r['BA'] + r['CA'] + r['NA'] - 1.0, r) for r in rows]
    worst = min(margins, key=lambda t: t[0])
    NA_list = [r['NA'] for r in rows]
    CA_list = [r['CA'] for r in rows]
    BA_list = [r['BA'] for r in rows]
    n_Bpos = sum(1 for r in rows if r['BA'] > 0)
    n_Bneg = sum(1 for r in rows if r['BA'] <= 0)
    dW_pos = sum(1 for r in rows if r['dW'] >= 0)

    w("=== EXTREMES (over M<=-3 primes) ===")
    w("N/A:           min=%.6f  max=%.6f" % (min(NA_list), max(NA_list)))
    w("C/A:           min=%.6f  max=%.6f" % (min(CA_list), max(CA_list)))
    w("B/A:           min=%.6f  max=%.6f" % (min(BA_list), max(BA_list)))
    w("(B+C+N)/A - 1: min(worst margin)=%.6f at p=%d (M=%d)"
      % (worst[0], worst[1]['p'], worst[1]['M']))
    w("B>0 fraction:  %d/%d positive, %d non-positive" % (n_Bpos, len(rows), n_Bneg))
    if n_Bneg:
        w("  B<=0 at primes: " + ", ".join(
            "p=%d(M=%d,B/A=%.2e)" % (r['p'], r['M'], r['BA'])
            for r in rows if r['BA'] <= 0)[:400])
    w("DeltaW>=0 (FAILS sign) count: %d  (should be 0 for theorem)" % dW_pos)
    if dW_pos:
        w("  DeltaW>=0 at: " + ", ".join(
            "p=%d(M=%d)" % (r['p'], r['M']) for r in rows if r['dW'] >= 0))
    w("")

    # Fit N/A = 1 + c/p by least squares on x=1/p, y=N/A-1
    xs = [1.0 / r['p'] for r in rows]
    ys = [r['NA'] - 1.0 for r in rows]
    n = len(xs)
    sx = sum(xs); sy = sum(ys)
    sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    # model y = c*x  (no intercept): c = sxy/sxx
    c_noint = sxy / sxx
    res_noint = sum((y - c_noint * x) ** 2 for x, y in zip(xs, ys))
    # model y = a + c*x (with intercept) to check a~0
    denom = n * sxx - sx * sx
    c_int = (n * sxy - sx * sy) / denom
    a_int = (sy - c_int * sx) / n
    res_int = sum((y - (a_int + c_int * x)) ** 2 for x, y in zip(xs, ys))
    w("=== FIT  N/A - 1  vs 1/p ===")
    w("no-intercept  N/A = 1 + c/p : c=%.4f   SSres=%.3e  RMS=%.3e"
      % (c_noint, res_noint, (res_noint / n) ** 0.5))
    w("with-intercept N/A = 1 + a + c/p : a=%.3e  c=%.4f  SSres=%.3e RMS=%.3e"
      % (a_int, c_int, res_int, (res_int / n) ** 0.5))
    w("  (a~0 would support a clean 1+O(1/p); large |a| => offset/messy)")
    w("")

    # tail behaviour: largest 8 primes
    w("=== SAMPLE ROWS (largest 12 M<=-3 primes) ===")
    w("%9s %5s %9s %9s %9s %11s" % ("p", "M", "N/A", "B/A", "C/A", "(B+C+N)/A"))
    for r in rows[-12:]:
        w("%9d %5d %9.5f %9.5f %9.5f %11.5f"
          % (r['p'], r['M'], r['NA'], r['BA'], r['CA'],
             r['BA'] + r['CA'] + r['NA']))
    w("")
    # by |M| bucket: mean (B+C+N)/A
    w("=== (B+C+N)/A by Mertens depth ===")
    buckets = {}
    for r in rows:
        key = r['M']
        buckets.setdefault(key, []).append(r['BA'] + r['CA'] + r['NA'])
    for mval in sorted(buckets)[:6] + sorted(buckets)[-6:]:
        vals = buckets[mval]
        w("M=%4d  n=%4d  mean(B+C+N)/A=%.4f  min=%.4f"
          % (mval, len(vals), sum(vals) / len(vals), min(vals)))

    text = "\n".join(out)
    print(text)
    with open("code/discrepancystep_probe_out.txt", "w") as fh:
        fh.write(text + "\n")


if __name__ == "__main__":
    main()
