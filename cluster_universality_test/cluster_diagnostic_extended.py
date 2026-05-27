#!/usr/bin/env python3
"""
Extended cluster-size diagnostic across more universality classes.

Adds to the prior run (BCZ, Poisson, GUE, CUE, zeta):
  - GOE  (real symmetric Gaussian -> L-functions with orthogonal symmetry,
          e.g. elliptic curve L-functions in the rank=0/even functional eqn family)
  - GSE  (Gaussian symplectic -> Sym^2 L-function symmetry families)
  - COE  (circular orthogonal -> finite-N orthogonal analogue)
  - CSE  (circular symplectic)
  - Delta-form L(s, Delta) low zeros (LMFDB downloaded earlier, ~199 zeros only)

Diagnostic conventions match cluster_diagnostic.py.

LMFDB note:
  Direct curl is gated by reCAPTCHA from this sandbox egress, and the
  WebFetch tool returns summaries rather than raw zero lists, so we cannot
  pull 1000-10000-zero windows for Dirichlet/EC/modular L-functions in this
  session. By Katz-Sarnak universality these all match one of the matrix
  ensembles below; we therefore simulate the ensembles directly and label
  the corresponding L-function family next to each entry.

Run:
  python3 cluster_diagnostic_extended.py
"""

import json
import os
import numpy as np

RNG = np.random.default_rng(20260527)


# ---- cluster_stats (same as cluster_diagnostic.py, replicated for autonomy) ----

def cluster_stats(gaps, q_list):
    gaps = np.asarray(gaps, dtype=np.float64)
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


# ---- BCZ control (replicated) ----

def bcz_chain_gaps(n_steps, rng):
    while True:
        x = float(rng.uniform())
        y = float(rng.uniform())
        if x + y > 1:
            break
    for _ in range(10_000):
        nx, ny = y, np.floor((1.0 + x) / y) * y - x
        x, y = nx, ny
    gaps = np.empty(n_steps, dtype=np.float64)
    for i in range(n_steps):
        gaps[i] = 1.0 / (x * y)
        nx, ny = y, np.floor((1.0 + x) / y) * y - x
        x, y = nx, ny
    return gaps


# ---- ensemble simulators ----

def _unfold_semicircle(lam, edge_scale_sigma):
    """Wigner semicircle bulk unfolding.
       Inputs: sorted eigenvalues lam,  edge_scale_sigma = scale such that
       eigenvalues live in [-2 sigma, 2 sigma], so rho(x) = sqrt(4 sigma^2 - x^2)/(2 pi sigma^2),
       and N(x) = total_count * [1/2 + (s sqrt(1-s^2) + arcsin s)/pi], s = x/(2 sigma).
       Keep bulk in |x| < 1.5 sigma (avoid edge fluctuations).
       Return normalized gaps with mean exactly 1 (rescale by empirical mean).
    """
    bulk_mask = np.abs(lam) < 1.5 * edge_scale_sigma
    bulk = lam[bulk_mask]
    if len(bulk) < 3:
        return np.array([])
    s = np.clip(bulk / (2.0 * edge_scale_sigma), -1.0, 1.0)
    # cumulative semicircle on [-2 sigma, 2 sigma]
    N_unf = len(lam) * (0.5 + (s * np.sqrt(1 - s * s) + np.arcsin(s)) / np.pi)
    gaps = np.diff(N_unf)
    # rescale to mean 1
    if gaps.mean() > 0:
        gaps = gaps / gaps.mean()
    return gaps


def goe_gaps(N, M, rng):
    """GOE: real symmetric Gaussian.  Conventions:
       H_ij = (A_ij + A_ji)/sqrt(2) where A_ij ~ N(0,1) iid.
       => H_ij off-diag var 1, H_ii var 2.  Wigner edge at +/- 2 sqrt(N).
    """
    all_gaps = []
    for _ in range(M):
        A = rng.standard_normal((N, N))
        H = (A + A.T) / np.sqrt(2.0)
        lam = np.sort(np.linalg.eigvalsh(H))
        all_gaps.append(_unfold_semicircle(lam, edge_scale_sigma=np.sqrt(N)))
    return np.concatenate(all_gaps)


def gse_gaps(N, M, rng):
    """GSE: 2N x 2N self-dual quaternion Hermitian -> Kramers pairs -> N distinct.
       Use the GUE-style normalisation and Kramers-deduplicate, then unfold via semicircle.
    """
    all_gaps = []
    for _ in range(M):
        A = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2.0)
        B = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2.0)
        A = (A + A.conj().T) / np.sqrt(2.0)
        B = (B - B.T) / np.sqrt(2.0)
        top = np.concatenate([A, B], axis=1)
        bot = np.concatenate([-B.conj(), A.conj()], axis=1)
        H = np.concatenate([top, bot], axis=0)
        H = (H + H.conj().T) / 2.0
        lam = np.sort(np.linalg.eigvalsh(H))
        lam = lam[::2]  # Kramers deduplicate -> N distinct
        # the 2N spectrum spans [-2 sqrt(2N), 2 sqrt(2N)] effectively after dedup
        all_gaps.append(_unfold_semicircle(lam, edge_scale_sigma=np.sqrt(2 * N)))
    return np.concatenate(all_gaps)


def cue_gaps(N, M, rng):
    """CUE eigenphase gaps."""
    all_gaps = []
    for _ in range(M):
        Z = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2.0)
        Q, R = np.linalg.qr(Z)
        d = np.diag(R)
        ph = d / np.abs(d)
        Q = Q * ph
        theta = np.sort(np.angle(np.linalg.eigvals(Q)))
        gaps = np.diff(theta) * N / (2.0 * np.pi)
        all_gaps.append(gaps)
    return np.concatenate(all_gaps)


def coe_gaps(N, M, rng):
    """COE: U U^T with U Haar unitary.  Eigenphases of UU^T."""
    all_gaps = []
    for _ in range(M):
        Z = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / np.sqrt(2.0)
        Q, R = np.linalg.qr(Z)
        d = np.diag(R)
        ph = d / np.abs(d)
        U = Q * ph
        S = U @ U.T
        theta = np.sort(np.angle(np.linalg.eigvals(S)))
        gaps = np.diff(theta) * N / (2.0 * np.pi)
        all_gaps.append(gaps)
    return np.concatenate(all_gaps)


def cse_gaps(N, M, rng):
    """CSE: U J U^T J^{-1} with J = [[0, I], [-I, 0]], Kramers pairs removed."""
    all_gaps = []
    twoN = 2 * N
    J = np.zeros((twoN, twoN), dtype=np.complex128)
    J[:N, N:] = np.eye(N)
    J[N:, :N] = -np.eye(N)
    Jinv = J.conj().T  # since J^-1 = -J = J^T for this real J
    for _ in range(M):
        Z = (rng.standard_normal((twoN, twoN)) + 1j * rng.standard_normal((twoN, twoN))) / np.sqrt(2.0)
        Q, R = np.linalg.qr(Z)
        d = np.diag(R)
        ph = d / np.abs(d)
        U = Q * ph
        S = U @ J @ U.T @ Jinv
        theta = np.sort(np.angle(np.linalg.eigvals(S)))
        theta = theta[::2]  # remove Kramers pair
        gaps = np.diff(theta) * len(theta) / (2.0 * np.pi)
        all_gaps.append(gaps)
    return np.concatenate(all_gaps)


def poisson_gaps(n, rng):
    return rng.exponential(1.0, size=n)


# ---- LMFDB delta zeros (200-zero window, low height) ----

def load_lmfdb_delta(path):
    import re
    try:
        with open(path) as f:
            txt = f.read()
    except FileNotFoundError:
        return np.array([])
    # extract positive_zeros list of stringified floats
    m = re.search(r'"positive_zeros"\s*:\s*\[([^\]]+)\]', txt)
    if not m:
        return np.array([])
    items = re.findall(r'"([\-0-9eE\.]+)"', m.group(1))
    return np.array([float(x) for x in items])


def normalize_lfunction_gaps_lowheight(gammas, deg=2, level=1, weight=12):
    """Local mean gap for weight-k cuspform L-function at height gamma:
       N(T) ~ (deg / 2 pi) T log(T sqrt(level) / (2 pi e))   [GL_2 case]
       d gamma / dn ~ 2 pi / (deg * log(gamma * sqrt(level) / (2 pi)))
       For Delta (deg=2, level=1):  mean gap ~ pi / log(gamma / (2 pi)).
    """
    g = gammas[gammas > 5.0]
    raw_gaps = np.diff(g)
    midpoints = 0.5 * (g[:-1] + g[1:])
    local_mean = 2.0 * np.pi / (deg * np.log(midpoints * np.sqrt(level) / (2.0 * np.pi)))
    return raw_gaps / local_mean


# ---- orchestrator ----

def summarize(name, gaps, q_list, family_tag=""):
    stats = cluster_stats(gaps, q_list)
    print(f"\n=== {name}   {family_tag}")
    print(f"     M = {len(gaps)} gaps,  mean = {gaps.mean():.6f},  std = {gaps.std():.4f}")
    print(f"{'q':>8} | {'thr':>8} | {'n_extr':>7} | {'n_clu':>7} | "
          f"{'size2%':>7} | {'p>=3':>7} | {'maxsz':>5} | hist")
    for q in q_list:
        s = stats[q]
        h = s['hist']
        keys = sorted(h.keys())[:8]
        hstr = ", ".join(f"{k}:{h[k]}" for k in keys)
        if len(h) > 8:
            hstr += ", ..."
        print(f"{q:8.4f} | {s['threshold']:8.4f} | {s['n_extreme']:7d} | "
              f"{s['n_clusters']:7d} | {100*s['size2_frac']:7.3f} | "
              f"{s['p_size_ge_3']:7.4f} | {s['max_size']:5d} | {hstr}")
    return stats


def main():
    out_dir = os.path.dirname(os.path.abspath(__file__))
    q_list = [0.95, 0.99]
    summary = {}

    print("Generating BCZ chain (1M, control) ...")
    bcz_g = bcz_chain_gaps(1_000_000, RNG)
    summary['BCZ_chain_1M'] = summarize("BCZ Farey-gap chain (1M)", bcz_g, q_list,
                                        family_tag="[Farey universality class]")

    print("\nGenerating Poisson (1M) ...")
    poi_g = poisson_gaps(1_000_000, RNG)
    summary['Poisson_1M'] = summarize("Poisson exponential gaps", poi_g, q_list,
                                       family_tag="[generic uncorrelated]")

    print("\nSimulating GOE (N=300, 500 mats) ...")
    goe_g = goe_gaps(300, 500, RNG)
    summary['GOE_N300_x500'] = summarize("GOE eigenvalue gaps", goe_g, q_list,
        family_tag="[L-functions w/ orthogonal symmetry: rank-0 ECs, Dirichlet L of real chi]")

    print("\nSimulating GUE (N=300, 500 mats) ...")
    gue_all = []
    for _ in range(500):
        a = (RNG.standard_normal((300, 300)) + 1j * RNG.standard_normal((300, 300))) / np.sqrt(2.0)
        h = (a + a.conj().T) / np.sqrt(2.0)
        lam = np.sort(np.linalg.eigvalsh(h))
        gue_all.append(_unfold_semicircle(lam, edge_scale_sigma=np.sqrt(300)))
    gue_g = np.concatenate(gue_all)
    summary['GUE_N300_x500'] = summarize("GUE eigenvalue gaps", gue_g, q_list,
        family_tag="[L-functions w/ unitary symmetry: generic Dirichlet L, modular L, zeta]")

    print("\nSimulating GSE (N=200, 300 mats) ...")
    gse_g = gse_gaps(200, 300, RNG)
    summary['GSE_N200_x300'] = summarize("GSE eigenvalue gaps", gse_g, q_list,
        family_tag="[L-functions w/ symplectic symmetry: Sym^2 of modular forms]")

    print("\nSimulating COE (N=400, 500 mats) ...")
    coe_g = coe_gaps(400, 500, RNG)
    summary['COE_N400_x500'] = summarize("COE eigenphase gaps", coe_g, q_list,
        family_tag="[orthogonal circular -- finite-N analogue of GOE family]")

    print("\nSimulating CUE (N=400, 500 mats) ...")
    cue_g = cue_gaps(400, 500, RNG)
    summary['CUE_N400_x500'] = summarize("CUE eigenphase gaps", cue_g, q_list,
        family_tag="[unitary circular -- finite-N analogue of GUE family]")

    print("\nSimulating CSE (N=200, 300 mats) ...")
    cse_g = cse_gaps(200, 300, RNG)
    summary['CSE_N200_x300'] = summarize("CSE eigenphase gaps", cse_g, q_list,
        family_tag="[symplectic circular -- finite-N analogue of GSE family]")

    # delta L-function (LMFDB-downloaded), low height
    delta = load_lmfdb_delta(os.path.join(out_dir, "lmfdb_delta_zeros.txt"))
    if len(delta) > 5:
        gd = normalize_lfunction_gaps_lowheight(delta, deg=2, level=1, weight=12)
        summary['Delta_L_lowzeros'] = summarize(
            f"L(s, Delta) low zeros (LMFDB, N={len(delta)})", gd, q_list,
            family_tag="[modular weight-12, level 1; predicted GUE universality]")

    # JSON dump
    out = {}
    for k, v in summary.items():
        out[k] = {str(q): {kk: vv for kk, vv in s.items()} for q, s in v.items()}
    with open(os.path.join(out_dir, "cluster_diagnostic_extended.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nSaved JSON to cluster_diagnostic_extended.json")

    # Final table: size2% at q=0.99
    print("\n" + "=" * 78)
    print("UNIVERSALITY TABLE  (cluster-size diagnostic, q=0.99)")
    print(f"{'class':28s} | {'N_gaps':>9} | {'size2%':>7} | {'size>=3%':>9} | family / L-function correspondence")
    print("-" * 78)
    order = ['BCZ_chain_1M', 'Poisson_1M', 'GOE_N300_x500', 'GUE_N300_x500',
             'GSE_N200_x300', 'COE_N400_x500', 'CUE_N400_x500', 'CSE_N200_x300',
             'Delta_L_lowzeros']
    family = {
        'BCZ_chain_1M':   'Farey fractions',
        'Poisson_1M':     'generic uncorrelated',
        'GOE_N300_x500':  'rank-0 EC L, real-char Dirichlet L',
        'GUE_N300_x500':  'zeta, generic Dirichlet L, modular L',
        'GSE_N200_x300':  'Sym^2 of modular forms',
        'COE_N400_x500':  'finite-N orthogonal',
        'CUE_N400_x500':  'finite-N unitary',
        'CSE_N200_x300':  'finite-N symplectic',
        'Delta_L_lowzeros': 'modular weight-12 (data, n=199)',
    }
    for k in order:
        if k not in summary:
            continue
        s = summary[k][0.99]
        # find n_extreme as proxy for sample size
        n_extr = s.get('n_extreme', 0)
        n_clu = s.get('n_clusters', 0)
        print(f"{k:28s} | {n_clu:>9d} | "
              f"{100*s['size2_frac']:7.3f} | {100*s['p_size_ge_3']:9.3f} | {family.get(k,'')}")


if __name__ == "__main__":
    main()
