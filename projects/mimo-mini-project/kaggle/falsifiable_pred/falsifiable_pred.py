"""Test the falsifiable prediction Pr(L≥3) ≈ (324/143)·ε² at small ε.

Subagent #5 derived the EXACT rational prefactor 324/143 ≈ 2.2657 for the
size-3+ entry probability in the BCZ chain at t = 2/9 + ε.

Predicted values:
  ε = 10⁻³: Pr(L≥3) ≈ 2.27 × 10⁻⁶  (per-step rate ≈ 0.138 × prob_per_cluster)
  ε = 10⁻⁴: Pr(L≥3) ≈ 2.27 × 10⁻⁸
  ε = 10⁻⁵: Pr(L≥3) ≈ 2.27 × 10⁻¹⁰  ← target

To detect Pr per-step at 10⁻¹⁰ rate, need ~10¹¹ steps to get O(10) events.
At numba speed ~50M steps/sec on Kaggle, 10¹¹ steps = 2000 sec ≈ 33 min.
Marginal but doable within Kaggle's 9-hour limit.

Strategy: run multiple ε values with progressively more steps.
"""
import time, math, json
import numpy as np
from numba import njit

T_STAR = 2.0/9.0
THEORY_PREFACTOR = 324.0/143.0   # ≈ 2.2657

@njit(cache=True)
def burn_in(N_burn, seed_val):
    np.random.seed(seed_val)
    while True:
        x = np.random.random(); y = np.random.random()
        if x + y > 1.0: break
    for _ in range(N_burn):
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    return x, y

@njit(cache=True)
def count_size_3plus_events(x0, y0, N_steps, t_thr):
    """Streaming: count clusters of size ≥ 3 (frequency-per-cluster diagnostic)."""
    x, y = x0, y0
    current_run = 0
    n_clusters = 0
    n_3plus = 0
    n_steps_total = 0
    for i in range(N_steps):
        n_steps_total += 1
        if x * y < t_thr:
            current_run += 1
        else:
            if current_run > 0:
                n_clusters += 1
                if current_run >= 3:
                    n_3plus += 1
                current_run = 0
        k = math.floor((1.0 + x) / y)
        x, y = y, k*y - x
    if current_run > 0:
        n_clusters += 1
        if current_run >= 3:
            n_3plus += 1
    return n_clusters, n_3plus, n_steps_total

def run():
    print(f"q*_BCZ = {(11 - 8*math.log(3/2))/9:.6f}", flush=True)
    print(f"Theory: Pr(L≥3 | cluster) = (324/143)·ε² = {THEORY_PREFACTOR:.5f}·ε²", flush=True)

    # Calibrate numba
    x0, y0 = burn_in(50_000, 42)
    _ = count_size_3plus_events(x0, y0, 10_000, T_STAR + 0.1)

    configs = [
        (1e-3, 2_000_000_000),   # ~3.4M expected size-3+ events
        (1e-4, 20_000_000_000),  # ~340K expected, need ~10x more steps
        (1e-5, 100_000_000_000), # ~17K expected, need a LOT more steps
    ]
    results = {"theory_prefactor": THEORY_PREFACTOR, "t_star": T_STAR, "data": []}
    t_total = time.time()

    for eps, n_steps in configs:
        t_thr = T_STAR + eps
        print(f"\n=== ε = {eps:.0e}, n_steps = {n_steps:,} ===", flush=True)
        x0, y0 = burn_in(50_000, int(eps * 1e8) + 7)
        t0 = time.time()
        n_clust, n_3plus, n_steps_actual = count_size_3plus_events(x0, y0, n_steps, t_thr)
        elapsed = time.time() - t0
        ratio = (n_3plus / n_clust) / (eps * eps) if n_clust > 0 and n_3plus > 0 else 0.0
        print(f"  clusters: {n_clust:,}", flush=True)
        print(f"  size-3+ events: {n_3plus:,}", flush=True)
        print(f"  Pr(L≥3 | cluster): {n_3plus/n_clust if n_clust > 0 else 0:.4e}", flush=True)
        print(f"  Pr(L≥3 | cluster) / ε² = {ratio:.4f}  (theory: {THEORY_PREFACTOR:.4f})", flush=True)
        print(f"  deviation: {(ratio - THEORY_PREFACTOR) * 100:.2f}% (relative to theory)", flush=True)
        print(f"  elapsed: {elapsed:.0f}s", flush=True)
        results["data"].append({
            "eps": eps, "n_steps": n_steps, "n_clusters": n_clust,
            "n_size_3plus": n_3plus,
            "pr_3_given_cluster": n_3plus/n_clust if n_clust > 0 else 0,
            "ratio_to_theory": ratio,
            "relative_deviation_percent": (ratio - THEORY_PREFACTOR) * 100 if ratio > 0 else None,
            "elapsed_s": elapsed,
        })

    print(f"\nTotal elapsed: {time.time() - t_total:.0f}s", flush=True)

    with open("/kaggle/working/falsifiable_pred_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run()
