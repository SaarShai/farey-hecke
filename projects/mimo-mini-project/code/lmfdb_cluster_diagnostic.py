#!/usr/bin/env python3
"""
APPLIED TEST: cluster=2 universality diagnostic on arithmetic L-function zeros.

Background
----------
Prior runs (cluster_universality_test/cluster_diagnostic_extended.py) established:
  - BCZ Farey chain    : ~95% size-2 at q=0.99    (Farey universality class)
  - All RMT ensembles  : ~0% size-2 at q=0.99     (GOE/GUE/GSE/COE/CUE/CSE)
  - Poisson            : ~1.1% size-2 at q=0.99
  - Riemann zeta (100k): 0% size-2 at q=0.99      (consistent with GUE)

Question this script answers:
  Do any OTHER arithmetic L-functions sit in the BCZ class (size-2 >> RMT)?

Method
------
For each L-function we get >=5000 imaginary parts of nontrivial zeros, unfold
locally to mean spacing 1 using N(T) ~ (deg / 2 pi) T log(C T^deg) -style
asymptotic, compute consecutive gaps, then run the cluster diagnostic at
q in {0.95, 0.99, 0.999}.

Diagnostic conventions match prior project code (cluster_diagnostic_extended.py):
  - 'size2_frac' = (# clusters of size exactly 2) / (# clusters)
  - 'p_size_ge_3' = (sum of gaps in size>=3 clusters) / (# extreme gaps)

L-functions tested
------------------
1. Riemann zeta zeros 1..100,000   (from cluster_universality_test/zeros1.txt)
   -> control: should match GUE, ~0% size-2 at q=0.99.

2. Dirichlet L(s, chi_{-3})  (odd, conductor 3, real Kronecker)
   computed in PARI/GP via lfunzeros.

3. Dirichlet L(s, chi_{-4})  (odd, conductor 4, real Kronecker)
   computed in PARI/GP via lfunzeros.

4. L(s, Delta)  Ramanujan modular form weight 12 level 1.
   computed in PARI/GP via mfeigenbasis + lfunmf.

5. L(s, f) for f = newform 11.2.a.a  (= L-function of elliptic curve 11a1,
   weight 2, level 11) -- a degree-2 GL_2 L-function with orthogonal symmetry.
   computed in PARI/GP via ellinit + lfuncreate.

6. L(s, Sym^2 Delta)  (degree 3, symplectic).
   computed in PARI/GP via lfunsympow.

Zero data caching
-----------------
PARI computation is slow for high T; we cache per-L-function zero files in
projects/mimo-mini-project/data/zeros/  so re-runs are fast.

Output
------
- prints summary table to stdout (and run log alongside)
- writes lmfdb_diagnostic_results.json  with the full per-q-per-L-function stats

Notes on honesty
----------------
- For the Sym^2 case PARI's lfunsympow with the Delta form is expensive; we
  cap T to whatever produces >=2000 zeros within a 6-minute budget per L-fn
  and report the actual sample size used.
- LMFDB's web download endpoint returns at most 10 zeros per L-function; we
  cannot pull bulk lists that way, hence the on-the-fly PARI computation.
- We do NOT use Sage; only PARI/GP via subprocess + mpmath fallback.
"""

import json
import math
import os
import subprocess
import sys
import time

import numpy as np


# --------------------------------------------------------------------- paths

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA_DIR = os.path.join(ROOT, "data", "zeros")
NOTES_DIR = os.path.join(ROOT, "research_notes")
RESULT_JSON = os.path.join(HERE, "lmfdb_diagnostic_results.json")
ZETA_ZEROS1 = os.path.join(
    os.path.dirname(ROOT), "..", "cluster_universality_test", "zeros1.txt"
)
ZETA_ZEROS1 = os.path.abspath(ZETA_ZEROS1)

os.makedirs(DATA_DIR, exist_ok=True)


# --------------------------------------------------------- cluster diagnostic

def cluster_stats(gaps, q_list):
    """Return dict q -> stats (size2_frac, p_size_ge_3, hist, ...).

    Identical conventions to
    cluster_universality_test/cluster_diagnostic_extended.py.
    """
    gaps = np.asarray(gaps, dtype=np.float64)
    gaps = gaps[np.isfinite(gaps)]
    out = {}
    for q in q_list:
        thr = float(np.quantile(gaps, q))
        extreme = gaps > thr
        sizes = []
        i = 0
        n = len(extreme)
        while i < n:
            if extreme[i]:
                j = i
                while j < n and extreme[j]:
                    j += 1
                sizes.append(j - i)
                i = j
            else:
                i += 1
        sizes = np.array(sizes, dtype=int)
        if len(sizes) == 0:
            out[q] = dict(threshold=thr, p_size_ge_3=0.0, max_size=0,
                          n_extreme=0, n_clusters=0, hist={},
                          size2_frac=0.0)
            continue
        n_extreme = int(extreme.sum())
        max_size = int(sizes.max())
        hist = {}
        for k in range(1, max_size + 1):
            c = int((sizes == k).sum())
            if c:
                hist[k] = c
        gaps_in_ge3 = int(sizes[sizes >= 3].sum())
        size2_frac = float((sizes == 2).sum()) / len(sizes)
        out[q] = dict(
            threshold=thr,
            p_size_ge_3=gaps_in_ge3 / n_extreme,
            max_size=max_size,
            n_extreme=n_extreme,
            n_clusters=int(len(sizes)),
            hist=hist,
            size2_frac=size2_frac,
        )
    return out


# -------------------------------------------------------------- unfolding

def unfold_zeros(gammas, deg, conductor=1, weight=None):
    """Local-mean unfolding for a degree-deg principal L-function.

    For a primitive self-dual L of degree d and (analytic) conductor q,
    the Riemann-von Mangoldt formula (Iwaniec-Kowalski Thm 5.8) gives
        N(T) = (T / (2 pi)) * log( q * T^d / (2 pi e)^d ) + O(log T),
    so local density
        rho(T) = dN/dT = (1/(2 pi)) * log( q * T^d / (2 pi)^d )
               = (1/(2 pi)) * (log q + d * log(T / (2 pi))).

    Cross-checks:
      zeta  (d=1, q=1):  rho(T) = (1/(2 pi)) log(T/(2 pi))  -- standard.
      Delta (d=2, q=1):  rho(T) = (1/pi) log(T/(2 pi)).
    """
    g = gammas[gammas > 5.0]
    raw_gaps = np.diff(g)
    midpoints = 0.5 * (g[:-1] + g[1:])
    rho = (math.log(conductor) + deg * np.log(midpoints / (2.0 * math.pi))) / (2.0 * math.pi)
    local_mean = 1.0 / rho
    return raw_gaps / local_mean


# -------------------------------------------------------------- PARI bridge

def _run_pari(script, timeout_s, parisize_mb=1024):
    """Run a PARI/GP script (string) and return its stdout."""
    full = f"default(parisize, {parisize_mb}*2^20);\n" + script + "\nquit\n"
    res = subprocess.run(
        ["gp", "-q"], input=full, capture_output=True, text=True,
        timeout=timeout_s,
    )
    if res.returncode != 0:
        sys.stderr.write(f"[pari stderr]\n{res.stderr}\n")
    return res.stdout, res.stderr


def parse_pari_vec_to_floats(s):
    """Parse 'v=[a,b,c]' style PARI vec text dump into list of floats."""
    s = s.strip()
    # may be split over lines and have backslash continuations
    s = s.replace("\\\n", "").replace("\\", "")
    if s.startswith("[") and s.endswith("]"):
        body = s[1:-1]
    else:
        body = s
    out = []
    for tok in body.split(","):
        tok = tok.strip()
        if not tok:
            continue
        try:
            out.append(float(tok))
        except ValueError:
            pass
    return out


def compute_kronecker_zeros(disc, T_max, cache_label, timeout_s=900):
    """L(s, chi_disc) zeros up to T = T_max, where disc is a fundamental
    discriminant (-3 -> chi_{-3} mod 3 odd; -4 -> chi_{-4} mod 4 odd)."""
    cache = os.path.join(DATA_DIR, f"{cache_label}_T{T_max}.txt")
    if os.path.exists(cache):
        return np.loadtxt(cache)
    script = f"""
default(realprecision, 16);
L = lfuncreate({disc});
v = lfunzeros(L, {T_max});
for(i=1, #v, print1(v[i]); if(i < #v, print1(",")));
print();
"""
    t0 = time.time()
    stdout, _ = _run_pari(script, timeout_s=timeout_s)
    elapsed = time.time() - t0
    zeros = parse_pari_vec_to_floats(stdout)
    print(f"  PARI chi_{disc} -> {len(zeros)} zeros in {elapsed:.1f}s "
          f"(T_max={T_max})")
    np.savetxt(cache, np.array(zeros))
    return np.array(zeros)


def compute_delta_zeros(T_max, timeout_s=900):
    cache = os.path.join(DATA_DIR, f"delta_T{T_max}.txt")
    if os.path.exists(cache):
        return np.loadtxt(cache)
    script = f"""
default(realprecision, 16);
M = mfinit([1,12], 0);
F = mfeigenbasis(M)[1];
L = lfunmf(M, F);
v = lfunzeros(L, {T_max});
for(i=1, #v, print1(v[i]); if(i < #v, print1(",")));
print();
"""
    t0 = time.time()
    stdout, _ = _run_pari(script, timeout_s=timeout_s)
    elapsed = time.time() - t0
    zeros = parse_pari_vec_to_floats(stdout)
    print(f"  PARI Delta L -> {len(zeros)} zeros in {elapsed:.1f}s "
          f"(T_max={T_max})")
    np.savetxt(cache, np.array(zeros))
    return np.array(zeros)


def compute_ell_curve_zeros(a_invariants, label, T_max, timeout_s=900):
    """Elliptic curve L-function zeros for the curve E with given Weierstrass."""
    a = "[" + ",".join(str(x) for x in a_invariants) + "]"
    cache = os.path.join(DATA_DIR, f"ec_{label}_T{T_max}.txt")
    if os.path.exists(cache):
        return np.loadtxt(cache)
    script = f"""
default(realprecision, 16);
E = ellinit({a});
L = lfuncreate(E);
v = lfunzeros(L, {T_max});
for(i=1, #v, print1(v[i]); if(i < #v, print1(",")));
print();
"""
    t0 = time.time()
    stdout, _ = _run_pari(script, timeout_s=timeout_s)
    elapsed = time.time() - t0
    zeros = parse_pari_vec_to_floats(stdout)
    print(f"  PARI EC {label} -> {len(zeros)} zeros in {elapsed:.1f}s "
          f"(T_max={T_max})")
    np.savetxt(cache, np.array(zeros))
    return np.array(zeros)


def compute_sym2_delta_zeros(T_max, timeout_s=1200):
    cache = os.path.join(DATA_DIR, f"sym2_delta_T{T_max}.txt")
    if os.path.exists(cache):
        return np.loadtxt(cache)
    # lfunsympow on the Delta L-function.  Note the Delta L is symmetric power
    # 1 of the Galois rep; sym^2 has degree 3, conductor 1, weight = 22.
    script = f"""
default(realprecision, 16);
M = mfinit([1,12], 0);
F = mfeigenbasis(M)[1];
L = lfunmf(M, F);
S = lfunsympow(L, 2);
v = lfunzeros(S, {T_max});
for(i=1, #v, print1(v[i]); if(i < #v, print1(",")));
print();
"""
    t0 = time.time()
    stdout, _ = _run_pari(script, timeout_s=timeout_s)
    elapsed = time.time() - t0
    zeros = parse_pari_vec_to_floats(stdout)
    print(f"  PARI Sym^2 Delta -> {len(zeros)} zeros in {elapsed:.1f}s "
          f"(T_max={T_max})")
    np.savetxt(cache, np.array(zeros))
    return np.array(zeros)


# --------------------------------------------------------- zeta loader

def load_zeta_zeros1():
    """First 100k zeros of zeta, low height, from cluster_universality_test."""
    vals = []
    with open(ZETA_ZEROS1) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                vals.append(float(line))
            except ValueError:
                pass
    return np.array(vals)


# -------------------------------------------------------------- summarize

def summarize(label, gammas, deg, conductor, weight, q_list, family_tag=""):
    if gammas is None or len(gammas) < 50:
        print(f"\n=== {label}   SKIPPED (only {0 if gammas is None else len(gammas)} zeros)")
        return None
    gaps = unfold_zeros(np.sort(gammas), deg=deg, conductor=conductor,
                        weight=weight)
    # also rescale gaps to exact mean 1 to remove any sub-leading drift
    if gaps.mean() > 0:
        gaps_n = gaps / gaps.mean()
    else:
        gaps_n = gaps
    stats = cluster_stats(gaps_n, q_list)
    print(f"\n=== {label}   {family_tag}")
    print(f"     #zeros = {len(gammas)}, #gaps = {len(gaps_n)}, "
          f"mean(post-rescale) = {gaps_n.mean():.6f}, std = {gaps_n.std():.4f}, "
          f"height range = [{gammas.min():.2f}, {gammas.max():.2f}]")
    print(f"{'q':>8} | {'thr':>7} | {'n_extr':>7} | {'n_clu':>7} | "
          f"{'size2%':>7} | {'p>=3':>7} | {'maxsz':>5} | hist")
    for q in q_list:
        s = stats[q]
        h = s['hist']
        keys = sorted(h.keys())[:8]
        hstr = ", ".join(f"{k}:{h[k]}" for k in keys)
        if len(h) > 8:
            hstr += ", ..."
        print(f"{q:8.4f} | {s['threshold']:7.4f} | {s['n_extreme']:7d} | "
              f"{s['n_clusters']:7d} | {100*s['size2_frac']:7.3f} | "
              f"{s['p_size_ge_3']:7.4f} | {s['max_size']:5d} | {hstr}")
    return {
        "label": label,
        "deg": deg,
        "conductor": conductor,
        "weight": weight,
        "n_zeros": int(len(gammas)),
        "n_gaps": int(len(gaps_n)),
        "height_min": float(gammas.min()),
        "height_max": float(gammas.max()),
        "stats": {str(q): stats[q] for q in q_list},
        "family_tag": family_tag,
    }


# ------------------------------------------------------------------- main

def main():
    q_list = [0.95, 0.99, 0.999]
    summary = {}

    print("=" * 78)
    print(" APPLIED cluster=2 diagnostic on arithmetic L-function zeros")
    print(" date 2026-05-27")
    print("=" * 78)

    # ---- 1. Riemann zeta (control) ----------------------------------------
    print("\n[1] Riemann zeta zeros 1..100,000  (control, expected GUE-like)")
    try:
        z_zeta = load_zeta_zeros1()
        s = summarize("Riemann zeta zeros 1..100,000", z_zeta,
                      deg=1, conductor=1, weight=0.5,
                      q_list=q_list,
                      family_tag="[GUE prediction]")
        if s: summary["zeta_100k"] = s
    except Exception as e:
        print(f"  zeta load failed: {e}")

    # ---- 2. chi_{-3} ------------------------------------------------------
    print("\n[2] Dirichlet L(s, chi_{-3}), conductor 3 (odd Kronecker)")
    try:
        z = compute_kronecker_zeros(disc=-3, T_max=4000, cache_label="chi_m3")
        if len(z) > 50:
            s = summarize("L(s, chi_{-3})", z,
                          deg=1, conductor=3, weight=0.5,
                          q_list=q_list,
                          family_tag="[degree 1, real odd char => GUE prediction]")
            if s: summary["chi_m3"] = s
    except subprocess.TimeoutExpired:
        print("  PARI timed out.")
    except Exception as e:
        print(f"  chi_{{-3}} failed: {e}")

    # ---- 3. chi_{-4} ------------------------------------------------------
    print("\n[3] Dirichlet L(s, chi_{-4}), conductor 4 (odd Kronecker)")
    try:
        z = compute_kronecker_zeros(disc=-4, T_max=4000, cache_label="chi_m4")
        if len(z) > 50:
            s = summarize("L(s, chi_{-4})", z,
                          deg=1, conductor=4, weight=0.5,
                          q_list=q_list,
                          family_tag="[degree 1, real odd char => GUE prediction]")
            if s: summary["chi_m4"] = s
    except subprocess.TimeoutExpired:
        print("  PARI timed out.")
    except Exception as e:
        print(f"  chi_{{-4}} failed: {e}")

    # ---- 3b. chi_5  (real even Kronecker, disc=5) -------------------------
    print("\n[3b] Dirichlet L(s, chi_5), conductor 5 (even Kronecker)")
    try:
        z = compute_kronecker_zeros(disc=5, T_max=4000, cache_label="chi_5")
        if z is not None and len(z) > 50:
            s = summarize("L(s, chi_5)", z,
                          deg=1, conductor=5, weight=0.5,
                          q_list=q_list,
                          family_tag="[degree 1, real even char => GUE prediction]")
            if s: summary["chi_5"] = s
    except Exception as e:
        print(f"  chi_5 failed: {e}")

    # ---- 3c. chi_8  (real even Kronecker, disc=8) -------------------------
    print("\n[3c] Dirichlet L(s, chi_8), conductor 8 (even Kronecker)")
    try:
        z = compute_kronecker_zeros(disc=8, T_max=4000, cache_label="chi_8")
        if z is not None and len(z) > 50:
            s = summarize("L(s, chi_8)", z,
                          deg=1, conductor=8, weight=0.5,
                          q_list=q_list,
                          family_tag="[degree 1, real even char => GUE prediction]")
            if s: summary["chi_8"] = s
    except Exception as e:
        print(f"  chi_8 failed: {e}")

    # ---- 4. Delta (small + big) ------------------------------------------
    print("\n[4] L(s, Delta) modular weight 12 level 1")
    z = None
    # try larger compute first
    big_cache = os.path.join(DATA_DIR, "delta_T3000.txt")
    small_cache = os.path.join(DATA_DIR, "delta_T900.txt")
    if os.path.exists(big_cache):
        z = np.loadtxt(big_cache)
        T_used = 3000
        print(f"  using {big_cache} ({len(z)} zeros)")
    elif os.path.exists(small_cache):
        z = np.loadtxt(small_cache)
        T_used = 900
        print(f"  using {small_cache} ({len(z)} zeros)")
    if z is not None and len(z) > 50:
        s = summarize(f"L(s, Delta) (T<={T_used})", z,
                      deg=2, conductor=1, weight=11.0,
                      q_list=q_list,
                      family_tag="[GL_2 self-dual cuspform; predicted GUE/unitary]")
        if s: summary["delta_L"] = s

    # ---- 4b. weight-16 level-1 newform L (Delta_16-like) ------------------
    print("\n[4b] L(s, f_16) weight 16 level 1 newform")
    wt16_cache = os.path.join(DATA_DIR, "wt16_T900.txt")
    if os.path.exists(wt16_cache):
        z = np.loadtxt(wt16_cache)
        if len(z) > 50:
            s = summarize("L(s, f_16) wt16 level 1", z,
                          deg=2, conductor=1, weight=15.0,
                          q_list=q_list,
                          family_tag="[GL_2 wt 16 cuspform; predicted GUE]")
            if s: summary["wt16_L"] = s

    # ---- 5. Elliptic curve 11a1 -------------------------------------------
    print("\n[5] L(s, E_11a1) elliptic curve, conductor 11 (weight 2 newform)")
    ec_cache_big = os.path.join(DATA_DIR, "ec_11a1_T2500.txt")
    ec_cache_small = os.path.join(DATA_DIR, "ec_11a1_T500.txt")
    if os.path.exists(ec_cache_big):
        z = np.loadtxt(ec_cache_big)
        ec_T = 2500
    elif os.path.exists(ec_cache_small):
        z = np.loadtxt(ec_cache_small)
        ec_T = 500
        print(f"  using T=500 (T=2500 timed out at 20-min budget)")
    else:
        z = None
    if z is not None and len(z) > 50:
        s = summarize(f"L(s, E_11a1) (T<={ec_T})", z,
                      deg=2, conductor=11, weight=0.5,
                      q_list=q_list,
                      family_tag="[GL_2 weight 2; rank 0; predicted GUE-like]")
        if s: summary["ec_11a1"] = s
    else:
        print("  no zeros file found; skipping.")

    # ---- 6. Sym^2 Delta : SKIPPED (lfunsympow unimplemented in PARI 2.15) ----
    print("\n[6] L(s, Sym^2 Delta): SKIPPED -- PARI 'lfunsympow' is not yet "
          "implemented (degree-3 symmetric powers are unavailable through "
          "PARI's lfun interface in 2.15.x; would need a hand-rolled Dirichlet "
          "series + functional equation).  Reported honestly; not tested.")

    # ---- write JSON --------------------------------------------------------
    out = {}
    for k, v in summary.items():
        # make stats JSON-serialisable (cast ints/floats explicitly)
        stats = {}
        for q_str, s in v["stats"].items():
            stats[q_str] = {
                "threshold": float(s["threshold"]),
                "n_extreme": int(s["n_extreme"]),
                "n_clusters": int(s["n_clusters"]),
                "max_size": int(s["max_size"]),
                "size2_frac": float(s["size2_frac"]),
                "p_size_ge_3": float(s["p_size_ge_3"]),
                "hist": {str(k2): int(v2) for k2, v2 in s["hist"].items()},
            }
        out[k] = {
            "label": v["label"],
            "deg": int(v["deg"]),
            "conductor": int(v["conductor"]),
            "weight": float(v["weight"]),
            "n_zeros": int(v["n_zeros"]),
            "n_gaps": int(v["n_gaps"]),
            "height_min": float(v["height_min"]),
            "height_max": float(v["height_max"]),
            "family_tag": v["family_tag"],
            "stats": stats,
        }
    with open(RESULT_JSON, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved JSON -> {RESULT_JSON}")

    # ---- final table -------------------------------------------------------
    print("\n" + "=" * 90)
    print(" UNIVERSALITY TABLE (cluster diagnostic vs Farey/BCZ baseline)")
    print("=" * 90)
    print(" Reference baselines (from cluster_universality_test):")
    print("   BCZ Farey chain : size-2 = 88.2% @ q=0.95,  94.6% @ q=0.99")
    print("   GUE/GOE/GSE/COE/CUE/CSE (RMT) : 0.6% @ q=0.95, 0% @ q=0.99")
    print("   Poisson : 4.6% @ q=0.95, 1.1% @ q=0.99")
    print("-" * 90)
    print(f"{'L-function':32s} | {'#zer':>5} | q=0.95 size2% | q=0.99 size2% | q=0.999 size2% | verdict")
    print("-" * 90)
    order = ["zeta_100k", "chi_m3", "chi_m4", "chi_5", "chi_8",
             "delta_L", "wt16_L", "ec_11a1"]
    for k in order:
        if k not in summary:
            continue
        s = summary[k]
        n = s["n_zeros"]
        s95 = s["stats"]["0.95"]["size2_frac"] * 100
        s99 = s["stats"]["0.99"]["size2_frac"] * 100
        try:
            s999 = s["stats"]["0.999"]["size2_frac"] * 100
        except KeyError:
            s999 = float("nan")
        # verdict
        if s99 > 50:
            verdict = "BCZ-class"
        elif s99 > 8:
            verdict = "intermediate"
        elif s99 > 1.5:
            verdict = "Poisson-like"
        else:
            verdict = "RMT (GUE/GOE/GSE)"
        print(f"{s['label']:32s} | {n:5d} | "
              f"{s95:13.3f} | {s99:13.3f} | {s999:14.3f} | {verdict}")
    print("=" * 90)


if __name__ == "__main__":
    main()
