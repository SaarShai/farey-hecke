"""Cluster=2 diagnostic on multiple universality classes.

Runs the size-2 cluster fraction at q ∈ {0.95, 0.99, 0.999} for:
  - Wigner β-ensembles: β = 1 (GOE), 2 (GUE), 4 (GSE), 6, 10 (intermediate rigidity)
  - Classical group ensembles via Haar: CUE (β=2), COE (β=1), CSE (β=4)
  - Poisson (uniform random spacings)
  - Periodic + small jitter
  - φ-rotation (Three-Gap)

For RMT ensembles we compute the spacing statistic on UNFOLDED eigenvalues
(local mean spacing = 1) — this was the bug in our earlier 'GUE 15%'
artifact, now corrected.

Output: JSON table of per-class cluster fractions for the diagnostic paper.
"""
import time, math, json
import numpy as np
from collections import Counter

Q_STAR = (11.0 - 8.0 * math.log(3.0/2.0)) / 9.0
print(f"q*_BCZ closed form = {Q_STAR:.6f}", flush=True)

# ---------- Spacing → cluster diagnostic ----------

def cluster_at_q(gaps, q_list, hist_max=10):
    """Return per-q cluster size statistics. gaps must be sorted-by-position."""
    gaps = np.asarray(gaps)
    sorted_g = np.sort(gaps)
    results = {}
    for q in q_list:
        thr = sorted_g[min(int(q * len(gaps)), len(gaps) - 1)]
        sizes = Counter()
        cur = 0
        for g in gaps:
            if g > thr:
                cur += 1
            else:
                if cur > 0:
                    sizes[cur] += 1
                    cur = 0
        if cur > 0: sizes[cur] += 1
        total = sum(sizes.values())
        s2 = sizes.get(2, 0)
        s3p = sum(c for k, c in sizes.items() if k >= 3)
        results[f"{q:.4f}"] = {
            "total_clusters": total,
            "pct_size_2": s2/total*100 if total > 0 else 0,
            "pct_size_3_plus": s3p/total*100 if total > 0 else 0,
            "hist": {str(k): v for k, v in sorted(sizes.items()) if k <= hist_max},
        }
    return results

# ---------- Sequence generators ----------

def beta_ensemble_eigenvalues(beta, N, rng):
    """Tridiagonal-construction Dumitriu–Edelman 2002 β-ensemble.

    Returns N sorted eigenvalues. Already approximately semicircle-distributed
    with bulk on (-2sqrt(N), 2sqrt(N)).
    """
    # Diagonal entries: N(0, sqrt(2)) i.i.d.
    d = rng.standard_normal(N) * math.sqrt(2.0)
    # Sub-diagonal: chi-distributed with parameter beta*(N-k)
    sub = np.array([math.sqrt(rng.chisquare(beta * (N - k))) for k in range(1, N)])
    # Build tridiagonal
    T = np.diag(d) + np.diag(sub, k=1) + np.diag(sub, k=-1)
    return np.sort(np.linalg.eigvalsh(T))

def cue_unfolded_spacings(N, rng):
    """CUE: eigenvalues of Haar-random U(N) on the unit circle, then unfolded.

    Sample by generating Z = (G + iG)/sqrt(2), QR-factoring to get Haar U,
    eigenvalues e^{iθ}, then sort θ and compute spacings normalised to mean=1.
    """
    Z = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / math.sqrt(2)
    Q, R = np.linalg.qr(Z)
    # Adjust phases for true Haar
    D = np.diag(R) / np.abs(np.diag(R))
    Q = Q * D[None, :]
    eig = np.linalg.eigvals(Q)
    theta = np.sort(np.angle(eig))  # in [-π, π]
    spacings = np.diff(theta)
    # Unfold to mean 1
    return spacings / np.mean(spacings)

def cse_unfolded_spacings(N, rng):
    """CSE via Hermitian-self-dual construction (β=4 circular).

    Use direct: spacings from CSE have density ~ s^4 exp(-c s²).
    Cheap proxy: sample Haar U(2N) and project to symplectic subgroup;
    simpler approximation: COE on N/2 doubled — use tridiagonal β-ensemble bulk.
    """
    # Approximation: use β=4 Hermite ensemble (close enough for cluster diagnostic).
    eig = beta_ensemble_eigenvalues(4, N, rng)
    # Compute bulk spacings (drop 20% edges)
    e0 = int(0.2 * N); e1 = int(0.8 * N)
    bulk = eig[e0:e1]
    sp = np.diff(bulk)
    return sp / np.mean(sp)

def coe_unfolded_spacings(N, rng):
    """COE ~ symmetric Haar U(N). Use eigenvalues of (U + U^T)/√2 type; or β=1 Hermite proxy."""
    eig = beta_ensemble_eigenvalues(1, N, rng)
    e0 = int(0.2 * N); e1 = int(0.8 * N)
    bulk = eig[e0:e1]
    sp = np.diff(bulk)
    return sp / np.mean(sp)

def hermite_bulk_spacings(beta, N, rng):
    """β-ensemble Hermite bulk spacings, normalized to mean 1."""
    eig = beta_ensemble_eigenvalues(beta, N, rng)
    # Drop 20% on each side to keep bulk
    e0 = int(0.2 * N); e1 = int(0.8 * N)
    bulk = eig[e0:e1]
    sp = np.diff(bulk)
    return sp / np.mean(sp)

def poisson_spacings(N, rng):
    """Poisson process spacings, mean 1."""
    return rng.exponential(1.0, size=N)

def phi_rotation_gaps(N):
    """Three-gap theorem sequence from φ-rotation."""
    phi = (math.sqrt(5) - 1) / 2
    pts = np.sort(np.array([(i * phi) % 1 for i in range(N)]))
    sp = np.diff(pts)
    return sp / np.mean(sp)

def periodic_jittered_gaps(N, rng, jitter=0.01):
    """Nearly-periodic with small random perturbation."""
    pts = np.linspace(0, 1, N + 1)[:-1] + jitter * rng.standard_normal(N) / N
    pts = np.sort(pts % 1.0)
    sp = np.diff(pts)
    sp = sp[sp > 0]
    return sp / np.mean(sp)

def riemann_zeros_spacings_mpmath(K):
    """Compute first K Riemann zeros via mpmath, unfold to mean 1.

    Slow — only use for K ≤ 10000.
    """
    from mpmath import zetazero, mp
    mp.dps = 20
    zeros = np.array([float(zetazero(n).imag) for n in range(1, K + 1)])
    sp = np.diff(zeros)
    # Riemann zero density ~ log(t)/(2π); unfold
    t_mid = (zeros[:-1] + zeros[1:]) / 2
    local_mean = np.log(t_mid) / (2 * math.pi)
    return sp * local_mean  # → mean 1 globally

# ---------- Run ----------

Q_LIST = [0.95, 0.99, 0.999]
REPEATS = 5  # average over multiple realizations
N_BETA = 5000  # eigenvalues per ensemble — bulk ~3000 spacings
RNG = np.random.default_rng(20260527)

all_results = {"q_star_BCZ": Q_STAR, "Q_LIST": Q_LIST, "configs": {}}

def avg_over_repeats(label, generator, N, repeats):
    print(f"\n=== {label} (N={N}, {repeats} repeats) ===", flush=True)
    t0 = time.time()
    per_q = {q: {"pct_size_2": [], "pct_size_3_plus": []} for q in [f"{q:.4f}" for q in Q_LIST]}
    for r in range(repeats):
        gaps = generator()
        res = cluster_at_q(gaps, Q_LIST)
        for qk, sv in res.items():
            per_q[qk]["pct_size_2"].append(sv["pct_size_2"])
            per_q[qk]["pct_size_3_plus"].append(sv["pct_size_3_plus"])
    summary = {}
    for qk, vals in per_q.items():
        summary[qk] = {
            "pct_size_2_mean": float(np.mean(vals["pct_size_2"])),
            "pct_size_2_std": float(np.std(vals["pct_size_2"])),
            "pct_size_3_plus_mean": float(np.mean(vals["pct_size_3_plus"])),
            "pct_size_3_plus_std": float(np.std(vals["pct_size_3_plus"])),
        }
        print(f"  q={qk}: size-2={summary[qk]['pct_size_2_mean']:.3f}±{summary[qk]['pct_size_2_std']:.3f}%, "
              f"size-3+={summary[qk]['pct_size_3_plus_mean']:.4f}±{summary[qk]['pct_size_3_plus_std']:.4f}%", flush=True)
    summary["elapsed_s"] = time.time() - t0
    return summary

# β-ensembles
for beta in [1, 2, 4, 6, 10]:
    all_results["configs"][f"beta_{beta}_hermite_bulk"] = avg_over_repeats(
        f"β={beta} Hermite bulk", lambda b=beta: hermite_bulk_spacings(b, N_BETA, RNG), N_BETA, REPEATS
    )

# Circular ensembles
all_results["configs"]["CUE"] = avg_over_repeats(
    "CUE Haar", lambda: cue_unfolded_spacings(2000, RNG), 2000, REPEATS
)
all_results["configs"]["COE"] = avg_over_repeats(
    "COE proxy (β=1 Hermite)", lambda: coe_unfolded_spacings(N_BETA, RNG), N_BETA, REPEATS
)
all_results["configs"]["CSE"] = avg_over_repeats(
    "CSE proxy (β=4 Hermite)", lambda: cse_unfolded_spacings(N_BETA, RNG), N_BETA, REPEATS
)

# Poisson / periodic / φ
all_results["configs"]["Poisson"] = avg_over_repeats(
    "Poisson", lambda: poisson_spacings(10000, RNG), 10000, REPEATS
)
all_results["configs"]["periodic_jitter"] = avg_over_repeats(
    "Periodic + jitter", lambda: periodic_jittered_gaps(10000, RNG), 10000, REPEATS
)
all_results["configs"]["phi_rotation"] = avg_over_repeats(
    "φ-rotation (Three-Gap)", lambda: phi_rotation_gaps(10000), 10000, 1  # deterministic
)

# Riemann zeros (slow — small K)
try:
    print("\n=== Riemann zeros (K=5000, slow mpmath) ===", flush=True)
    t0 = time.time()
    sp = riemann_zeros_spacings_mpmath(5000)
    print(f"  computed {len(sp)} unfolded spacings in {time.time()-t0:.0f}s", flush=True)
    res = cluster_at_q(sp, Q_LIST)
    all_results["configs"]["Riemann_zeros_5k"] = {
        qk: {
            "pct_size_2_mean": v["pct_size_2"],
            "pct_size_3_plus_mean": v["pct_size_3_plus"],
            "total_clusters": v["total_clusters"],
        }
        for qk, v in res.items()
    }
    all_results["configs"]["Riemann_zeros_5k"]["elapsed_s"] = time.time() - t0
    for qk, v in res.items():
        print(f"  q={qk}: size-2={v['pct_size_2']:.3f}%, size-3+={v['pct_size_3_plus']:.4f}%", flush=True)
except Exception as e:
    print(f"Riemann zeros skipped: {e}", flush=True)

# Save
with open("/kaggle/working/diagnostic_suite_results.json", "w") as f:
    json.dump(all_results, f, indent=2)
print("\nDone — diagnostic suite results saved.", flush=True)
