#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sweep_variance.py -- Option-3 large-q variance-ordering sweep.

QUESTION (conditional GRH+LI; this is the RS/Fiorilli-Martin framework):
  For each prime q == 3 (mod 4) [so that -1 is a nonsquare], is a = -1 the
  variance-MAXIMAL nonsquare, i.e. argmax_{a nonsquare} V(q;a,1)?
  V max  <=>  delta(q;a,1) MIN  <=>  a is the LEAST-biased nonsquare.
  Fiorilli-Martin Crelle 676 (2013) Thm 1.10 (GRH+LI): for any fixed a != -1,
  delta(q;-1,1) < delta(q;a,1) for all but FINITELY many q with -1,a nonsquares.
  This sweep is the empirical per-q complement: it reports every prime q == 3 mod 4
  where -1 is NOT the variance-max nonsquare.

VARIANCE (FM Thm 1.4, GRH only; here specialized to prime q where every
  nonprincipal chi is primitive):
    V(q;a,1) = sum_{chi != chi0} c_chi |chi(a)-1|^2,
    c_chi = log(q/pi) + psi((1+a_chi)/2) + 2 Re L'/L(1,chi),  a_chi = (1-chi(-1))/2.
  FAST L'/L via shared Hurwitz-zeta Laurent (sum_r chi(r)=0 kills the pole):
    L(s,chi) = q^{-s} sum_{r=1}^{q-1} chi(r) zeta(s,r/q),
    zeta(s,a) = 1/(s-1) + gamma_0(a) - gamma_1(a)(s-1) + ...,  gamma_0(a) = -psi(a),
    A0(chi)=sum_r chi(r) gamma_0(r/q),  A1(chi)=sum_r chi(r) gamma_1(r/q),
    L'/L(1,chi) = -log q - A1/A0.
  gamma_1(a) by central difference of f(s)=zeta(s,a)-1/(s-1) (err ~1e-9 at dps15).
  All chi handled at once by FFT over discrete-log-ordered residues -> O(q log q)/modulus.

  c_chi & V validated to ~1e-14 vs compute_delta.py's slow mp.diff route (_test_fast_lpl.py);
  this script additionally SELF-TESTS q in {7,11,19,23} against a direct (slow) V at startup
  and refuses to run the sweep unless they reproduce the established ranks (1/3,1/5,1/9,1/11).

STATUS: CONDITIONAL on GRH + LI. c_chi NUMERICAL (validated closed form). Nothing unconditional.
"""
import sys, os, time, math
import mpmath as mp
import numpy as np

mp.mp.dps = 15
LOG2 = math.log(2.0)

# ---------------------------------------------------------------- number theory
def primitive_root(q):
    # q prime: find generator of (Z/qZ)*
    phi = q - 1
    # factor phi
    fac = {}
    n = phi
    d = 2
    while d * d <= n:
        while n % d == 0:
            fac[d] = 1; n //= d
        d += 1
    if n > 1: fac[n] = 1
    for g in range(2, q):
        ok = True
        for p in fac:
            if pow(g, phi // p, q) == 1:
                ok = False; break
        if ok:
            return g
    raise RuntimeError(f"no primitive root mod {q}")

def gamma1_array(q):
    """gamma_1(r/q) for r=1..q-1 via central diff of zeta(s,r/q)-1/(s-1) at s=1."""
    h = mp.mpf('1e-5')
    one = mp.mpf(1)
    out = np.empty(q - 1, dtype=np.float64)
    for r in range(1, q):
        a = mp.mpf(r) / q
        # f(1+h) = zeta(1+h,a) - 1/h ;  f(1-h) = zeta(1-h,a) + 1/h
        fp = mp.zeta(one + h, a) - 1 / h
        fm = mp.zeta(one - h, a) + 1 / h
        out[r - 1] = float(-(fp - fm) / (2 * h))
    return out

def psi_array(q):
    out = np.empty(q - 1, dtype=np.float64)
    for r in range(1, q):
        out[r - 1] = float(mp.psi(0, mp.mpf(r) / q))
    return out

# ---------------------------------------------------------------- core analysis
def analyze(q, want_full=False):
    """Return dict with -1's variance rank among nonsquares for prime q==3 mod 4."""
    phi = q - 1
    g = primitive_root(q)
    # res[j] = g^j mod q ; dlog used implicitly via ordering
    res = np.empty(phi, dtype=np.int64)
    x = 1
    for j in range(phi):
        res[j] = x
        x = (x * g) % q
    # gamma_0(r/q) = -psi(r/q), gamma_1(r/q) indexed by residue value
    psi_by_res = psi_array(q)      # index r-1 -> psi(r/q)
    g1_by_res = gamma1_array(q)    # index r-1 -> gamma_1(r/q)
    # reorder by discrete log: b0[j] = gamma_0(res[j]/q) = -psi(res[j]/q)
    b0 = -psi_by_res[res - 1]
    b1 = g1_by_res[res - 1]
    # A0(k) = sum_j b0[j] exp(+2pi i k j/phi) = conj(fft(b0))[k]  (b0 real)
    A0 = np.conj(np.fft.fft(b0))
    A1 = np.conj(np.fft.fft(b1))
    logq = math.log(q)
    LpL = -logq - A1 / A0          # complex, per character k=0..phi-1 (k=0 principal)
    # parity: chi_k(-1) = (-1)^k  -> a_chi = k mod 2
    k = np.arange(phi)
    psi_par = np.where(k % 2 == 1, float(mp.psi(0, 1)), float(mp.psi(0, mp.mpf(1) / 2)))
    c = (logq - math.log(math.pi)) + psi_par + 2.0 * LpL.real   # c_chi for each k
    c[0] = 0.0                      # drop principal (k=0)
    # V(g^m) = 2*S - 2*Re( sum_k c[k] exp(2pi i k m/phi) ),  S = sum_k c[k]
    S = c.sum()
    T = np.conj(np.fft.fft(c))      # T[m] = sum_k c[k] exp(+2pi i k m/phi)
    V = 2.0 * S - 2.0 * T.real      # V indexed by m = dlog(a)
    # nonsquares <=> m odd ; a=-1 is g^{phi/2}, m_{-1}=phi/2 (odd since q==3 mod4)
    m_minus1 = phi // 2
    odd_m = np.arange(1, phi, 2)
    Vodd = V[odd_m]
    order = odd_m[np.argsort(-Vodd)]            # m's of nonsquares, descending V
    rank_minus1 = int(np.where(order == m_minus1)[0][0]) + 1
    argmax_m = int(order[0])
    n_nr = len(odd_m)
    # margin of -1 vs the best OTHER nonsquare (negative if -1 not max)
    others = [mm for mm in order if mm != m_minus1]
    if others:                                  # q==3: only one nonsquare (-1 itself)
        best_other = others[0]
        margin = float(V[m_minus1] - V[best_other])
    else:
        best_other = m_minus1
        margin = float('inf')
    out = dict(q=q, phi=phi, n_nr=n_nr, rank_minus1=rank_minus1,
               is_max=(rank_minus1 == 1), V_minus1=float(V[m_minus1]),
               argmax_m=argmax_m, V_argmax=float(V[order[0]]),
               best_other_m=best_other, margin=margin)
    if want_full:
        out['V_by_m'] = V
        out['res'] = res
    return out

# ---------------------------------------------------------------- slow direct (self-test)
def analyze_direct(q):
    """O(phi^2) exact-ish direct V via the same c_chi closed form (mpmath). Self-test only."""
    phi = q - 1
    g = primitive_root(q)
    res = []
    x = 1
    for j in range(phi):
        res.append(x); x = (x * g) % q
    dlog = {res[j]: j for j in range(phi)}
    g0 = {r: -mp.psi(0, mp.mpf(r) / q) for r in range(1, q)}
    h = mp.mpf('1e-5'); one = mp.mpf(1)
    g1 = {}
    for r in range(1, q):
        a = mp.mpf(r) / q
        g1[r] = -((mp.zeta(one + h, a) - 1 / h) - (mp.zeta(one - h, a) + 1 / h)) / (2 * h)
    cc = []
    for kk in range(1, phi):
        A0 = mp.fsum(mp.e ** (2j * mp.pi * kk * dlog[r] / phi) * g0[r] for r in range(1, q))
        A1 = mp.fsum(mp.e ** (2j * mp.pi * kk * dlog[r] / phi) * g1[r] for r in range(1, q))
        lpl = -mp.log(q) - A1 / A0
        achi = kk % 2
        cc.append((kk, mp.log(mp.mpf(q) / mp.pi) + mp.psi(0, (1 + achi) / mp.mpf(2)) + 2 * lpl.real))
    sq = set((b * b) % q for b in range(1, q))
    NR = sorted(set(range(1, q)) - sq)
    V = {}
    for a in NR:
        V[a] = float(mp.fsum(c * abs(mp.e ** (2j * mp.pi * kk * dlog[a] / phi) - 1) ** 2 for kk, c in cc))
    order = sorted(NR, key=lambda a: -V[a])
    return order, V

def self_test():
    print("SELF-TEST: fast FFT V vs slow direct V; assert -1 = unique variance-max")
    expect_rank = {7: (1, 3), 11: (1, 5), 19: (1, 9), 23: (1, 11)}  # (rank, n_nr) from RECONCILE
    ok = True
    for q in [7, 11, 19, 23]:
        fast = analyze(q)
        order, Vdir = analyze_direct(q)
        m1 = q - 1
        rank_dir = order.index(m1) + 1
        # compare fast V(-1) to direct
        err = abs(fast['V_minus1'] - Vdir[m1])
        exp_rank, exp_n = expect_rank[q]
        good = (fast['rank_minus1'] == rank_dir == exp_rank and fast['n_nr'] == exp_n and err < 1e-6)
        ok = ok and good
        print(f"  q={q}: fast rank(-1)={fast['rank_minus1']} dir rank={rank_dir} "
              f"(expect {exp_rank}/{exp_n}), |V_fast-V_dir|={err:.2e}  {'PASS' if good else 'FAIL'}")
    print(f"  SELF-TEST {'PASSED' if ok else 'FAILED'}\n")
    return ok

# ---------------------------------------------------------------- sweep driver
def primes_3mod4_upto(N):
    sieve = bytearray([1]) * (N + 1)
    sieve[0:2] = b'\x00\x00'
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
    return [p for p in range(3, N + 1) if sieve[p] and p % 4 == 3]

def worker(q):
    try:
        return analyze(q)
    except Exception as e:
        return dict(q=q, error=str(e))

def main():
    QMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    NPROC = int(sys.argv[2]) if len(sys.argv) > 2 else max(1, os.cpu_count() - 2)
    OUT = sys.argv[3] if len(sys.argv) > 3 else "sweep_results.tsv"
    if not self_test():
        print("*** SELF-TEST FAILED -- aborting sweep ***"); sys.exit(1)
    qs = primes_3mod4_upto(QMAX)
    print(f"Sweeping {len(qs)} primes q==3 mod4 in [3,{QMAX}] on {NPROC} procs -> {OUT}")
    t0 = time.time()
    done = 0
    exceptions = []
    # resume: skip q already in OUT
    seen = set()
    if os.path.exists(OUT):
        with open(OUT) as f:
            for ln in f:
                if ln and not ln.startswith('q\t'):
                    try: seen.add(int(ln.split('\t')[0]))
                    except: pass
    todo = [q for q in qs if q not in seen]
    print(f"  resume: {len(seen)} already done, {len(todo)} to do")
    write_header = not os.path.exists(OUT)
    from multiprocessing import Pool
    with open(OUT, 'a', buffering=1) as f:
        if write_header:
            f.write("q\tphi\tn_nr\trank_minus1\tis_max\tV_minus1\targmax_m\tV_argmax\tmargin\n")
        with Pool(NPROC) as pool:
            for r in pool.imap_unordered(worker, todo, chunksize=1):
                done += 1
                if 'error' in r:
                    print(f"  q={r['q']} ERROR {r['error']}"); continue
                f.write(f"{r['q']}\t{r['phi']}\t{r['n_nr']}\t{r['rank_minus1']}\t"
                        f"{int(r['is_max'])}\t{r['V_minus1']:.6f}\t{r['argmax_m']}\t"
                        f"{r['V_argmax']:.6f}\t{r['margin']:.6f}\n")
                if not r['is_max']:
                    exceptions.append(r)
                    print(f"  *** EXCEPTION q={r['q']}: -1 rank {r['rank_minus1']}/{r['n_nr']} "
                          f"argmax m={r['argmax_m']} margin={r['margin']:.4f}")
                if done % 200 == 0:
                    el = time.time() - t0
                    print(f"  ... {done}/{len(todo)} done in {el:.0f}s "
                          f"({el/done:.2f}s/modulus), exceptions so far: {len(exceptions)}")
    el = time.time() - t0
    print(f"\nDONE: {done} moduli in {el:.0f}s. Exceptions (-1 NOT variance-max): {len(exceptions)}")
    for r in exceptions:
        print(f"  q={r['q']}: rank {r['rank_minus1']}/{r['n_nr']} margin {r['margin']:.4f}")

if __name__ == "__main__":
    main()
