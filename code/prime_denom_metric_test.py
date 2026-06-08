"""
prime_denom_metric_test.py
==========================

Decisive test of experiment (3): is the prime-denominator approximation behavior
of a target alpha a NEW phenomenon, or fully explained by the classical metric
baseline (Harman's Khintchine analogue)?

Baseline (metric, almost-all alpha):
  Harman's prime-denominator Khintchine theorem: for psi decreasing, for a.a.
  alpha,  #{q prime <= Q : ||q*alpha|| < psi(q)}  ~  2 * sum_{q prime <= Q} psi(q)
  provided sum diverges. With psi(q)=c/q:  sum_{q<=Q} c/q ~ c*loglog Q (Mertens),
  and since this DIVERGES, |alpha - p/q| < c/q^2 holds infinitely often for a.a.
  alpha even with q restricted to primes. => EXPONENT 2, same as full Farey.

So the prediction is: the shallow prime log-log slope seen at small N in
E6/exp3 is a FINITE-SIZE artifact; as N grows the prime best-approx slope -> -2,
and the counting function matches 2*sum 1/q exactly. If true, there is NO new
metric result -- the only open frontier is the UNIFORM exponent (nu<1/3,
Matomaki), which is analytic NT, not visible to Monte Carlo.

This script tests that prediction with EXACT big-integer arithmetic (alpha given
to D=40 decimal digits, so ||q*alpha|| is computed exactly for q up to ~10^7,
no float swamping of the ~1e-12 signal).

Reproduce:  python3 code/prime_denom_metric_test.py
"""

from __future__ import annotations
import math, json, os, random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False

D = 40
SCALE = 10 ** D
# fractional parts to 40 decimal digits (exact integers A, alpha = A/10^40)
NAMED = {
    "phi-1":  6180339887498948482045868343656381177203,
    "sqrt2-1":4142135623730950488016887242096980785696,
    "e-2":    7182818284590452353602874713526624977572,
    "pi-3":   1415926535897932384626433832795028841971,
}


def sieve(N):
    s = bytearray([1]) * (N + 1)
    s[0] = s[1] = 0
    for i in range(2, int(math.isqrt(N)) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return s


def norm_int(q, A):
    """Exact ||q*alpha|| * SCALE  as an integer in [0, SCALE/2]."""
    r = (q * A) % SCALE
    return min(r, SCALE - r)


# ---- TEST A: exponent convergence (best-approx error vs N) -------------------
def test_A(Nmax=1_000_000, checkpoints=24):
    print(f"\n===== TEST A: exponent convergence (Nmax={Nmax}) =====")
    s = sieve(Nmax)
    cps = sorted(set(int(round(10 ** x)) for x in
                     [3 + (math.log10(Nmax) - 3) * i / (checkpoints - 1)
                      for i in range(checkpoints)]))
    report = {}
    for name, A in NAMED.items():
        best_full = None
        best_prime = None
        rows = []
        ci = 0
        for q in range(1, Nmax + 1):
            n = norm_int(q, A)          # ||q a|| * SCALE
            err = n / (q * SCALE)       # |a - p/q|
            if best_full is None or err < best_full[1]:
                best_full = (q, err)
            if s[q] and (best_prime is None or err < best_prime[1]):
                best_prime = (q, err)
            if ci < len(cps) and q == cps[ci]:
                rows.append((q, best_full[1], best_prime[1] if best_prime else None))
                ci += 1
        # local slope over the top half of the checkpoints
        def slope(idx):
            pts = [(math.log10(r[0]), math.log10(r[idx])) for r in rows
                   if r[idx] and r[idx] > 0]
            pts = pts[len(pts) // 2:]
            n = len(pts); mx = sum(p[0] for p in pts) / n; my = sum(p[1] for p in pts) / n
            den = sum((p[0] - mx) ** 2 for p in pts)
            return sum((p[0] - mx) * (p[1] - my) for p in pts) / den
        sf, sp = slope(1), slope(2)
        report[name] = {"rows": rows, "slope_full": sf, "slope_prime": sp}
        print(f"  {name:8s}  upper-decade slope  full={sf:+.3f}  prime={sp:+.3f}"
              f"   (both -> -2 if classical)")
    json.dump(report, open(os.path.join(OUT, "primemetric_A.json"), "w"))
    if HAVE_MPL:
        fig, ax = plt.subplots(figsize=(8, 5))
        for name in NAMED:
            rows = report[name]["rows"]
            ax.loglog([r[0] for r in rows], [r[1] for r in rows], "-o", ms=3,
                      label=f"{name} full")
            ax.loglog([r[0] for r in rows], [r[2] for r in rows], "--s", ms=3,
                      label=f"{name} prime")
        xs = [rows[0][0], rows[-1][0]]
        ax.loglog(xs, [xs[0] ** -2 * 3, xs[1] ** -2 * 3], "k:", lw=1, label="slope -2 ref")
        ax.set_xlabel("N"); ax.set_ylabel("best |a-p/q|, q<=N")
        ax.set_title("TEST A: prime-denom best-approx slope -> -2 (classical exponent)")
        ax.legend(fontsize=6, ncol=2); fig.tight_layout()
        p = os.path.join(OUT, "primemetric_A.png"); fig.savefig(p, dpi=120); plt.close(fig)
        print(f"  [plot] {p}")
    return report


# ---- TEST B: counting function vs Harman/Mertens baseline -------------------
def mertens_prime_sum(Q, s):
    """sum_{q prime <= Q} 1/q  (exact float)."""
    tot = 0.0
    for q in range(2, Q + 1):
        if s[q]:
            tot += 1.0 / q
    return tot


def test_B(Q=200_000, n_alpha=400, c=1.0, seed=12345):
    """Vectorized with numpy int64. Uses Db=13 digit precision (exact for this Q:
    ||qa|| threshold ~ c/Q ~ 5e-6 >> 1e-13). q*A and nrm*q both stay < 9.2e18."""
    import numpy as np
    Db = 13
    SC = 10 ** Db
    print(f"\n===== TEST B: counting #{{q prime<=Q: ||qa||<c/q}} vs 2c*sum 1/q "
          f"(Q={Q}, {n_alpha} random a, c={c}, prec={Db}d) =====")
    s = sieve(Q)
    P = np.array([q for q in range(2, Q + 1) if s[q]], dtype=np.int64)
    rng = random.Random(seed)
    thresh = int(c * SC)
    cps = sorted(set(int(round(10 ** x)) for x in
                     [2 + (math.log10(Q) - 2) * i / 14 for i in range(15)]))
    # map each checkpoint to a prime-array index (# primes <= Q_)
    cidx = [(Q_, int(np.searchsorted(P, Q_, side="right"))) for Q_ in cps]
    acc = {Q_: 0.0 for Q_ in cps}
    for _ in range(n_alpha):
        A = rng.randrange(10 ** (Db - 1), SC)
        r = (P * A) % SC                       # ||qa||*SC  (int64, no overflow)
        nrm = np.minimum(r, SC - r)
        hit = (nrm * P < thresh)               # ||qa|| < c/q
        cum = np.cumsum(hit)
        for Q_, k in cidx:
            acc[Q_] += int(cum[k - 1]) if k > 0 else 0
    baseline = {Q_: 2 * c * mertens_prime_sum(Q_, s) for Q_ in cps}
    print("    Q          mean_count    2c*sum1/q    ratio")
    rows = []
    for Q_ in cps:
        m = acc[Q_] / n_alpha
        b = baseline[Q_]
        rows.append((Q_, m, b, m / b if b else float("nan")))
        print(f"    {Q_:>9d}   {m:9.3f}    {b:9.3f}    {m/b if b else 0:.3f}")
    json.dump({"rows": rows, "c": c, "n_alpha": n_alpha},
              open(os.path.join(OUT, "primemetric_B.json"), "w"))
    if HAVE_MPL:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.semilogx([r[0] for r in rows], [r[1] for r in rows], "-o", label="mean count (200 random a)")
        ax.semilogx([r[0] for r in rows], [r[2] for r in rows], "--", label="Harman/Mertens 2c*sum 1/q")
        ax.set_xlabel("Q"); ax.set_ylabel("count")
        ax.set_title("TEST B: prime-denom counting vs classical metric baseline")
        ax.legend(fontsize=8); fig.tight_layout()
        p = os.path.join(OUT, "primemetric_B.png"); fig.savefig(p, dpi=120); plt.close(fig)
        print(f"  [plot] {p}")
    return rows


if __name__ == "__main__":
    test_A()
    test_B()
    print(f"\noutputs in {OUT}")
