"""Exotic universality classes diagnostic — experiment 3.

Hunting for anything in the 3-90% middle bin (between Wigner-Dyson ~0% and BCZ ~95%).

Candidates tested:
  1. Bogomolny semi-Poisson: P(s) = 4s·exp(-2s) — known intermediate statistic
  2. Berry-Robnik Wigner+Poisson mixtures: α ∈ {0.1, 0.3, 0.5, 0.7, 0.9}
  3. Laguerre β=2 ensemble (Wishart bulk) — non-Hermite RMT
  4. Jacobi β=2 ensemble — finite-interval RMT
  5. Tracy-Widom edge: extremes from N independent β=2 ensembles
  6. "Anti-BCZ" density: f(x,y) = 2·𝟙_{x+y<1} (mirror of BCZ) — does this also give cluster=2?
  7. Quarter-disk indicator: f(x,y) = 4/π · 𝟙_{x²+y²<1, x>0, y>0} — different geometry
  8. Hexagonal indicator: f(x,y) ∝ 𝟙_{hexagon} — different region

The "indicator-region" experiments test whether cluster=2 comes from indicator-type
densities GENERICALLY, or only from the BCZ triangle specifically.
"""
import time, math, json
import numpy as np
from collections import Counter

Q_STAR = (11.0 - 8.0 * math.log(3.0/2.0)) / 9.0
Q_LIST = [0.95, 0.99, 0.999]
REPEATS = 5
N_LARGE = 100_000

def cluster_diagnostic(gaps, q_list):
    sorted_g = np.sort(gaps)
    results = {}
    for q in q_list:
        idx = min(int(q * len(gaps)), len(gaps) - 1)
        thr = sorted_g[idx]
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
        s3p = sum(c for s, c in sizes.items() if s >= 3)
        results[f"{q:.4f}"] = {
            "total_clusters": total,
            "size_2": s2,
            "size_3_plus": s3p,
            "pct_size_2": s2/total*100 if total > 0 else 0,
            "pct_size_3_plus": s3p/total*100 if total > 0 else 0,
            "max_size": max(sizes.keys()) if sizes else 0,
        }
    return results

def avg(label, generator, reps=REPEATS):
    print(f"\n=== {label} (×{reps}) ===", flush=True)
    t0 = time.time()
    per_q = {f"{q:.4f}": {"pct_size_2": [], "pct_size_3_plus": []} for q in Q_LIST}
    for _ in range(reps):
        gaps = generator()
        res = cluster_diagnostic(gaps, Q_LIST)
        for qk, sv in res.items():
            per_q[qk]["pct_size_2"].append(sv["pct_size_2"])
            per_q[qk]["pct_size_3_plus"].append(sv["pct_size_3_plus"])
    summary = {"elapsed_s": time.time() - t0}
    for qk, vals in per_q.items():
        summary[qk] = {
            "pct_size_2_mean": float(np.mean(vals["pct_size_2"])),
            "pct_size_2_std": float(np.std(vals["pct_size_2"])),
            "pct_size_3_plus_mean": float(np.mean(vals["pct_size_3_plus"])),
        }
        print(f"  q={qk}: s2={summary[qk]['pct_size_2_mean']:.3f}±{summary[qk]['pct_size_2_std']:.3f}%, s3+={summary[qk]['pct_size_3_plus_mean']:.5f}%", flush=True)
    return summary

# -------- Generators --------

rng = np.random.default_rng(20260527)

def semi_poisson(N, rng):
    """Bogomolny semi-Poisson: P(s) = 4s·exp(-2s). Sample via inverse-CDF."""
    u = rng.random(N)
    # CDF F(s) = 1 - (1 + 2s)·exp(-2s); invert via Newton from initial guess s = sqrt(-ln(1-u)/2)
    s = np.sqrt(-np.log(1 - u + 1e-15))
    for _ in range(20):
        F = 1 - (1 + 2*s) * np.exp(-2*s)
        Fp = 4*s * np.exp(-2*s)
        s = s - (F - u) / (Fp + 1e-15)
        s = np.clip(s, 1e-10, 100)
    return s / np.mean(s)  # normalise to mean 1

def berry_robnik(alpha, N, rng):
    """Wigner-Poisson mixture: α GUE + (1-α) Poisson by superposition."""
    n_gue = int(alpha * N)
    n_poi = N - n_gue
    # GUE part: tridiagonal β=2
    if n_gue > 100:
        d = rng.standard_normal(n_gue) * math.sqrt(2.0)
        sub = np.sqrt(rng.chisquare(2 * np.arange(n_gue - 1, 0, -1)))
        T = np.diag(d) + np.diag(sub, k=1) + np.diag(sub, k=-1)
        eig_gue = np.sort(np.linalg.eigvalsh(T))
        # Map to unit interval via rank
        ranks = np.arange(len(eig_gue)) / len(eig_gue)
    else:
        ranks = np.array([])
    # Poisson part: uniform random on (0,1)
    poi = np.sort(rng.random(n_poi))
    # Combine and sort
    combined = np.sort(np.concatenate([ranks, poi]))
    sp = np.diff(combined)
    sp = sp[sp > 0]
    return sp / np.mean(sp)

def laguerre_beta2(N, rng):
    """Eigenvalues of W = G·G^T where G is N x N standard complex Gaussian (β=2 Wishart)."""
    G = (rng.standard_normal((N, N)) + 1j * rng.standard_normal((N, N))) / math.sqrt(2)
    W = G @ G.conj().T
    eig = np.sort(np.linalg.eigvalsh(W))
    # Bulk spacings (drop edges)
    e0 = int(0.2 * N); e1 = int(0.8 * N)
    sp = np.diff(eig[e0:e1])
    return sp / np.mean(sp)

def anti_bcz_chain(N_steps, rng):
    """Use the BCZ chain but with the mirror density f(x,y) = 2·𝟙_{x+y<1}.
    Sample directly from the lower triangle and compute pair-product gaps.
    """
    # Sample N independent pairs from the lower triangle
    samples = []
    while len(samples) < N_steps:
        x = rng.random(); y = rng.random()
        if x + y < 1.0:
            samples.append((x, y))
    samples = np.array(samples)
    # Gap statistic: 1/(x*y) for each pair (same as BCZ)
    gaps = 1.0 / (samples[:, 0] * samples[:, 1])
    return gaps

def upper_triangle_independent(N_steps, rng):
    """BCZ-density independent samples (not the chain): is cluster=2 due to dynamics or density?"""
    samples = []
    while len(samples) < N_steps:
        x = rng.random(); y = rng.random()
        if x + y > 1.0:
            samples.append((x, y))
    samples = np.array(samples)
    gaps = 1.0 / (samples[:, 0] * samples[:, 1])
    return gaps

def quarter_disk(N_steps, rng):
    """f(x,y) = 4/π · 𝟙_{x²+y²<1, x>0, y>0}. Sample, compute 1/(xy) gaps."""
    samples = []
    while len(samples) < N_steps:
        x = rng.random(); y = rng.random()
        if x*x + y*y < 1.0:
            samples.append((x, y))
    samples = np.array(samples)
    gaps = 1.0 / (samples[:, 0] * samples[:, 1])
    return gaps

# -------- Run --------

results = {"q_star_BCZ": Q_STAR, "configs": {}}

results["configs"]["semi_poisson_Bogomolny"] = avg(
    "Semi-Poisson (Bogomolny)", lambda: semi_poisson(N_LARGE, rng), reps=5
)

for alpha in [0.1, 0.3, 0.5, 0.7, 0.9]:
    label = f"Berry-Robnik alpha={alpha:.1f}"
    results["configs"][f"berry_robnik_{alpha:.1f}"] = avg(
        label, lambda a=alpha: berry_robnik(a, 10_000, rng), reps=3
    )

results["configs"]["laguerre_beta2"] = avg(
    "Laguerre β=2 (Wishart bulk)", lambda: laguerre_beta2(2_000, rng), reps=3
)

results["configs"]["anti_bcz"] = avg(
    "Anti-BCZ density 2·𝟙_{x+y<1}", lambda: anti_bcz_chain(N_LARGE, rng), reps=3
)

results["configs"]["upper_triangle_independent"] = avg(
    "Upper triangle independent sampling (test: is cluster=2 from density or from DYNAMICS?)",
    lambda: upper_triangle_independent(N_LARGE, rng), reps=3
)

results["configs"]["quarter_disk"] = avg(
    "Quarter-disk indicator density", lambda: quarter_disk(N_LARGE, rng), reps=3
)

with open("/kaggle/working/exotic_classes_results.json", "w") as f:
    json.dump(results, f, indent=2)
print("\nDone — exotic classes results saved.", flush=True)
