#!/usr/bin/env python3
"""
Cluster-size diagnostic across sequences:
  Farey/BCZ (control), Riemann zeta zeros, GUE/CUE simulations.

Convention:
  Given a sequence of consecutive normalized gaps d_1, d_2, ..., d_M,
  let Q_q = the q-quantile (P(d <= Q_q) = q).
  A gap is "extreme" if d > Q_q.    [upper tail of size 1 - q]
  A cluster is a maximal run of consecutive extreme gaps.
  cluster_size_k = number of clusters of size exactly k.
  In terms of gaps-in-runs:  gaps_in_size_k_runs = k * cluster_size_k.

  Diagnostic statistic: P_size>=3 := (sum_{k>=3} k * cluster_size_k) / total_extreme_gaps
  (fraction of extreme gaps that live in a cluster of size >= 3.)

  Also report: max_cluster_size, total_extreme, and cluster_size histogram.

Run:
  python3 cluster_diagnostic.py
"""

import numpy as np
import os
import json

RNG = np.random.default_rng(20260527)


# -------------------- core cluster statistics --------------------

def cluster_stats(gaps, q_list):
    """Return dict q -> {hist, p_size_ge_3, max_size, n_extreme, n_clusters}."""
    gaps = np.asarray(gaps, dtype=np.float64)
    out = {}
    for q in q_list:
        thr = float(np.quantile(gaps, q))
        extreme = gaps > thr
        # run-length encode the True regions
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
                          n_extreme=0, n_clusters=0, hist={})
            continue
        n_extreme = int(extreme.sum())
        max_size = int(sizes.max())
        # histogram (cluster counts by size)
        hist = {}
        for k in range(1, max_size + 1):
            c = int((sizes == k).sum())
            if c:
                hist[k] = c
        gaps_in_ge3 = int(sizes[sizes >= 3].sum())
        out[q] = dict(
            threshold=thr,
            p_size_ge_3=gaps_in_ge3 / n_extreme,
            max_size=max_size,
            n_extreme=n_extreme,
            n_clusters=int(len(sizes)),
            hist=hist,
        )
    return out


# -------------------- 1. BCZ baseline (control) --------------------

def bcz_chain_gaps(n_steps, rng):
    """Sample BCZ pair-chain: (X_i, X_{i+1}) uniform on {X+Y>1, 0<X,Y<=1}.
       Transition kernel: given X_i, X_{i+1} = Y, draw X_{i+2} via
       BCZ renewal. We use the standard MS kernel: next state given Y is
       uniform conditional on Y + X_{i+2} > 1.  This is a Markov chain on (0,1].
       Gap is the BCZ-rescaled gap proxy g_i = X_i * X_{i+1}.
    """
    # Markov chain: state s = X. Given s, draw Y uniform on (max(0,1-s), 1].
    # But the joint stationary measure on (X,Y) is 1_{X+Y>1} * 2 dX dY (uniform on triangle).
    # We sample stationary by direct (X,Y) on triangle then propagate.
    # Simpler: marginal of X under stationary is f(x) = 2x for x in (0,1] (since triangle area 1/2,
    # length of slice at X = x is x, so marginal density = 2x).
    X = np.empty(n_steps + 1, dtype=np.float64)
    # Sample X_0 from marginal 2x:  X = sqrt(U)
    X[0] = np.sqrt(rng.uniform())
    # Markov step: given X_i = x, X_{i+1} uniform on (1-x, 1].
    # Verify stationarity:  pi(y) = integral pi(x) K(y|x) dx
    #                        = integral_{1-y}^{1} 2x * (1/x) dx  = integral_{1-y}^{1} 2 dx = 2y  OK.
    for i in range(n_steps):
        x = X[i]
        X[i + 1] = 1 - x + x * rng.uniform()  # uniform on (1-x, 1]
    gaps = X[:-1] * X[1:]
    return gaps


# -------------------- 2. GUE / CUE simulations --------------------

def gue_eigenvalue_gaps(N_mat, n_matrices, rng):
    """Generate eigenvalue gaps from GUE matrices of size N_mat, n_matrices independent draws.
       Bulk-unfold each spectrum to mean spacing 1 via semicircle local density."""
    all_gaps = []
    for _ in range(n_matrices):
        # GUE: H = (A + A.conj().T)/2 with A_ij ~ CN(0,1)
        A = (rng.standard_normal((N_mat, N_mat))
             + 1j * rng.standard_normal((N_mat, N_mat))) / np.sqrt(2.0)
        H = (A + A.conj().T) / np.sqrt(2.0)
        lam = np.sort(np.linalg.eigvalsh(H))
        # unfold bulk via semicircle: rho(x) = (1/(2*pi)) sqrt(4N - x^2)  for GUE with this normalization
        # we want N_unf(x) = N * (1/2 + x*sqrt(4N - x^2)/(4*pi*N) + asin(x/(2 sqrt N))/pi)
        # Keep only bulk eigenvalues to avoid edge.
        edge = 1.6 * np.sqrt(N_mat)
        bulk_mask = np.abs(lam) < edge
        lam_b = lam[bulk_mask]
        # cumulative density for GUE Wigner semicircle:
        s = lam_b / (2.0 * np.sqrt(N_mat))
        s = np.clip(s, -1.0, 1.0)
        N_unf = N_mat * (0.5 + (s * np.sqrt(1 - s * s) + np.arcsin(s)) / np.pi)
        gaps = np.diff(N_unf)
        # gaps now have mean ~ 1 after unfolding
        all_gaps.append(gaps)
    return np.concatenate(all_gaps)


def cue_eigenvalue_gaps(N_mat, n_matrices, rng):
    """Generate eigenphase gaps from CUE (uniform unitary)."""
    all_gaps = []
    for _ in range(n_matrices):
        Z = (rng.standard_normal((N_mat, N_mat))
             + 1j * rng.standard_normal((N_mat, N_mat))) / np.sqrt(2.0)
        Q, R = np.linalg.qr(Z)
        # standardize Haar measure (Mezzadri 2007)
        d = np.diag(R)
        ph = d / np.abs(d)
        Q = Q * ph
        # eigenphases:
        evals = np.linalg.eigvals(Q)
        theta = np.sort(np.angle(evals))
        # gaps on the circle, length = N_mat
        gaps = np.diff(theta)
        # mean spacing = 2 pi / N
        gaps = gaps * N_mat / (2.0 * np.pi)
        all_gaps.append(gaps)
    return np.concatenate(all_gaps)


def poisson_gaps(n, rng):
    """Independent exponential gaps (mean 1)."""
    return rng.exponential(1.0, size=n)


# -------------------- 3. Riemann zeta zeros (Odlyzko tables) --------------------

def load_odlyzko_zeros1(path):
    """First 100k zeros of zeta (low height)."""
    vals = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                vals.append(float(line))
            except ValueError:
                continue
    return np.array(vals, dtype=np.float64)


def load_odlyzko_offset(path):
    """zeros3/4/5: offsets after several header lines. First numeric line is data."""
    vals = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                # only accept positive numbers; first few lines have prose
                v = float(line)
                if v > 0:
                    vals.append(v)
            except ValueError:
                continue
    return np.array(vals, dtype=np.float64)


def normalize_zeta_gaps_lowheight(gammas):
    """For zeros1: low height, use local mean gap = 2*pi / log(gamma_i/(2*pi))."""
    g = gammas[gammas > 7.0]  # safety
    raw_gaps = np.diff(g)
    midpoints = 0.5 * (g[:-1] + g[1:])
    local_mean = 2.0 * np.pi / np.log(midpoints / (2.0 * np.pi))
    return raw_gaps / local_mean


def normalize_zeta_gaps_offset(offsets, base_log):
    """zeros3 (offsets near 10^12), base_log = log(gamma/(2pi)) ~ constant.
       Mean gap = 2pi / base_log. Use this constant to normalize."""
    raw_gaps = np.diff(offsets)
    mean_gap = 2.0 * np.pi / base_log
    return raw_gaps / mean_gap


# -------------------- Orchestrator --------------------

def summarize(name, gaps, q_list):
    stats = cluster_stats(gaps, q_list)
    print(f"\n=== {name}  (M = {len(gaps)} gaps,  mean = {gaps.mean():.6f},  std = {gaps.std():.4f}) ===")
    print(f"{'q':>8} | {'thr':>8} | {'n_extr':>8} | {'n_clu':>6} | {'p>=3':>8} | {'maxsize':>7} | hist(top)")
    for q in q_list:
        s = stats[q]
        # truncate hist
        h = s['hist']
        keys = sorted(h.keys())[:10]
        hstr = ", ".join(f"{k}:{h[k]}" for k in keys)
        if len(h) > 10:
            hstr += ", ..."
        print(f"{q:8.4f} | {s['threshold']:8.4f} | {s['n_extreme']:8d} | "
              f"{s['n_clusters']:6d} | {s['p_size_ge_3']:8.5f} | {s['max_size']:7d} | {hstr}")
    return stats


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    q_list = [0.95, 0.99]
    summary = {}

    # ---- BCZ control ----
    print("Generating BCZ chain ...")
    bcz_g = bcz_chain_gaps(n_steps=5_000_000, rng=RNG)
    summary['BCZ_chain_5M'] = summarize("BCZ Farey-gap chain (5M)", bcz_g, q_list)

    # ---- Poisson reference ----
    print("Generating Poisson (independent exponential) ...")
    poi_g = poisson_gaps(2_000_000, RNG)
    summary['Poisson_2M'] = summarize("Poisson exponential gaps", poi_g, q_list)

    # ---- GUE ----
    print("Simulating GUE eigenvalues ...")
    gue_g = gue_eigenvalue_gaps(N_mat=300, n_matrices=400, rng=RNG)
    summary['GUE_N300_x400'] = summarize("GUE eigenvalue gaps (N=300, 400 mats)", gue_g, q_list)

    # ---- CUE ----
    print("Simulating CUE eigenvalues ...")
    cue_g = cue_eigenvalue_gaps(N_mat=400, n_matrices=400, rng=RNG)
    summary['CUE_N400_x400'] = summarize("CUE eigenphase gaps (N=400, 400 mats)", cue_g, q_list)

    # ---- Riemann zeros: zeros1 (first 100k, low height) ----
    z1 = load_odlyzko_zeros1(os.path.join(out_dir, "zeros1.txt"))
    gz1 = normalize_zeta_gaps_lowheight(z1)
    summary['zeta_first100k'] = summarize(
        f"Riemann zeta zeros 1..{len(z1)} (low height, local unfolding)", gz1, q_list)

    # ---- Riemann zeros: zeros3 (10^12 + 1..10^4) ----
    o3 = load_odlyzko_offset(os.path.join(out_dir, "zeros3.txt"))
    # base height ~ 2.67653e11; base_log = log(2.67653e11 / (2 pi))
    base_h_3 = 267653395648.0
    base_log_3 = np.log(base_h_3 / (2.0 * np.pi))
    gz3 = normalize_zeta_gaps_offset(o3, base_log_3)
    summary['zeta_at_10p12'] = summarize(
        f"Riemann zeta zeros #10^12+1..+{len(o3)} (high height ~2.7e11)", gz3, q_list)

    # ---- Riemann zeros: zeros4 (10^21 + 1..10^4) ----
    o4 = load_odlyzko_offset(os.path.join(out_dir, "zeros4.txt"))
    base_h_4 = 1.44176897509546973e20  # gamma_{10^21 + 1} approx
    base_log_4 = np.log(base_h_4 / (2.0 * np.pi))
    gz4 = normalize_zeta_gaps_offset(o4, base_log_4)
    summary['zeta_at_10p21'] = summarize(
        f"Riemann zeta zeros #10^21+1..+{len(o4)} (very high height ~1.4e20)", gz4, q_list)

    # ---- Riemann zeros: zeros5 (10^22) ----
    o5 = load_odlyzko_offset(os.path.join(out_dir, "zeros5.txt"))
    base_h_5 = 1.370919909931995308e21
    base_log_5 = np.log(base_h_5 / (2.0 * np.pi))
    gz5 = normalize_zeta_gaps_offset(o5, base_log_5)
    summary['zeta_at_10p22'] = summarize(
        f"Riemann zeta zeros #10^22+1..+{len(o5)} (~1.4e21)", gz5, q_list)

    # save JSON summary
    def jsonable(d):
        return {k: ({kk: vv for kk, vv in v.items()} if isinstance(v, dict) else v) for k, v in d.items()}
    out = {}
    for k, v in summary.items():
        out[k] = {str(q): jsonable(s) for q, s in v.items()}
    with open(os.path.join(out_dir, "cluster_diagnostic_results.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved JSON to cluster_diagnostic_results.json")


if __name__ == "__main__":
    main()
