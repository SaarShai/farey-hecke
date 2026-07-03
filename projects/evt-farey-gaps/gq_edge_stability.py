"""
gq_edge_stability.py
====================
Numeric probe: EVT extremal index and local stability at P_max for G_q BCZ maps.

For q ∈ {3, 5, 7}, run long orbits (10^7 steps), locate argmax of P, compute
Jacobian at maximizer, classify stability (parabolic/elliptic/hyperbolic), and
empirically check exceedance clustering at deep threshold.
"""
from __future__ import annotations
import math
import json
import numpy as np
from typing import Tuple

rng = np.random.default_rng(20260703)

# ============================================================================
# Hecke BCZ map (from goal1_bcz_hecke_cluster.py, inlined for clarity)
# ============================================================================

def hecke_vectors(q: int):
    """w_i = U_q^i (1,0)^T for i = 0..q,  U_q = [[lam,-1],[1,0]]."""
    lam = 2.0 * math.cos(math.pi / q)
    U = np.array([[lam, -1.0], [1.0, 0.0]])
    w = [np.array([1.0, 0.0])]
    for _ in range(q):
        w.append(U @ w[-1])
    return lam, w


def in_domain(a, b, lam, tol=1e-12):
    return (0 < a <= 1 + tol) and (1 - lam * a - tol < b <= 1 + tol)


def bcz_q_step(a, b, lam, w, q):
    """One step of the Taha G_q-BCZ map. Returns (a',b',i,k,P)."""
    d = [float(w[i] @ np.array([a, b])) for i in range(q + 1)]
    sub = None
    for i in range(2, q):
        if d[i - 1] > 1.0 and d[i] <= 1.0:
            sub = i
            break
    if sub is None:
        for i in range(2, q):
            if d[i] <= 1.0:
                sub = i
                break
        if sub is None:
            sub = q - 1
    i = sub
    wi = d[i]
    wi1 = d[i + 1]
    yi = float(w[i][1])
    P = a * wi / yi
    k = math.floor((1.0 - wi1) / (lam * wi))
    a2 = wi
    b2 = wi1 + k * lam * wi
    return a2, b2, i, k, P


def X_of_q(q: int) -> float:
    lam = 2.0 * math.cos(math.pi / q)
    if q == 3:
        return 2.0 / 9.0
    if q == 4:
        return math.sqrt(2.0) / 8.0
    return 1.0 / (lam ** 3)


def random_start(lam):
    while True:
        a = rng.random()
        b = rng.random()
        if 0 < a <= 1 and (1 - lam * a) < b <= 1:
            return a, b


# ============================================================================
# Jacobian computation at (a, b) on branch i
# ============================================================================

def jacobian_branch_i(a, b, i, lam, w, q, h=1e-8):
    """
    Compute 2x2 Jacobian of the map (a, b) -> (a', b') on branch i,
    using finite differences.

    Returns J = [[da'/da, da'/db], [db'/da, db'/db]].
    """
    def get_a_b_on_branch(a_in, b_in):
        a_out, b_out, i_out, k_out, P_out = bcz_q_step(a_in, b_in, lam, w, q)
        return a_out, b_out, i_out

    a2, b2, i_check = get_a_b_on_branch(a, b)
    if i_check != i:
        # Point is not on branch i; fall back to numerical gradient at the point
        # (the map is multi-valued, so this is the local linear part)
        pass

    # Finite differences
    da_da = ((get_a_b_on_branch(a + h, b)[0]) - a2) / h
    da_db = ((get_a_b_on_branch(a, b + h)[0]) - a2) / h
    db_da = ((get_a_b_on_branch(a + h, b)[1]) - b2) / h
    db_db = ((get_a_b_on_branch(a, b + h)[1]) - b2) / h

    J = np.array([[da_da, da_db], [db_da, db_db]], dtype=float)
    return J


def classify_stability(J):
    """
    Classify stability of a 2x2 Jacobian:
    - parabolic: |trace| = 2 (or ~2 numerically)
    - elliptic: |trace| < 2, rotation angle from eigenvalues
    - hyperbolic: |trace| > 2, multipliers from eigenvalues

    Returns: dict with trace, eigenvalues, type, and angle/multipliers if applicable.
    """
    tr = np.trace(J)
    deter = np.linalg.det(J)
    eigvals = np.linalg.eigvals(J)

    abs_tr = abs(tr)

    result = {
        "trace": float(tr),
        "determinant": float(deter),
        "eigenvalues": [complex(ev) for ev in eigvals],
        "abs_trace": float(abs_tr),
    }

    tol = 0.02
    if abs_tr < 2 - tol:
        # Elliptic
        result["type"] = "elliptic"
        if abs(eigvals[0]) > 1e-10:
            angle = np.angle(eigvals[0])
            result["rotation_angle_radians"] = float(angle)
            result["rotation_angle_degrees"] = float(np.degrees(angle))
    elif abs_tr > 2 + tol:
        # Hyperbolic
        result["type"] = "hyperbolic"
        result["multipliers"] = [float(abs(ev)) for ev in eigvals]
    else:
        # Parabolic (or borderline)
        result["type"] = "parabolic"

    return result


# ============================================================================
# Long orbit analysis with clustering
# ============================================================================

def run_long_orbit(q, n_steps, burn=500):
    """
    Run a single long orbit for q, returning:
    - P_max and argmax point (a*, b*, i, k)
    - branch/k info at maximizer
    - Jacobian trace/eigenvalues at maximizer
    - empirical cluster stats at deep threshold (99.99th percentile)
    """
    lam, w = hecke_vectors(q)
    X = X_of_q(q)

    # Pick random initial point
    a, b = random_start(lam)
    for _ in range(burn):
        a, b, i, k, P = bcz_q_step(a, b, lam, w, q)

    # Collect orbit data
    products = []
    coords = []
    P_max = -np.inf
    argmax_coord = None

    for step in range(n_steps):
        a, b, i, k, P = bcz_q_step(a, b, lam, w, q)
        products.append(P)
        coords.append((a, b, i, k))

        if P > P_max:
            P_max = P
            # Store the *previous* point which generated this P
            argmax_coord = coords[-2] if len(coords) > 1 else (a, b, i, k)

    # More precisely: the product P corresponds to (a, b) before the step.
    # Re-trace to get the exact maximizer coordinates.
    products_array = np.array(products)
    max_idx = np.argmax(products_array)
    if max_idx < len(coords):
        a_max, b_max, i_max, k_max = coords[max_idx]
    else:
        a_max, b_max, i_max, k_max = argmax_coord if argmax_coord else (a, b, i, k)

    # Compute Jacobian at maximizer
    J = jacobian_branch_i(a_max, b_max, i_max, lam, w, q)
    stability = classify_stability(J)

    # Clustering at deep threshold (99.99th percentile)
    deep_thresh = np.percentile(products_array, 99.99)
    exceedances = products_array > deep_thresh
    cluster_sizes = []
    cur_size = 0
    for exc in exceedances:
        if exc:
            cur_size += 1
        else:
            if cur_size > 0:
                cluster_sizes.append(cur_size)
            cur_size = 0
    if cur_size > 0:
        cluster_sizes.append(cur_size)

    mean_cluster_size = float(np.mean(cluster_sizes)) if cluster_sizes else 0.0
    cluster_hist = {}
    for sz in cluster_sizes:
        cluster_hist[sz] = cluster_hist.get(sz, 0) + 1

    # Also check runs below X (the theoretical threshold)
    below_X = products_array < X
    below_runs = []
    cur_run = 0
    for bx in below_X:
        if bx:
            cur_run += 1
        else:
            if cur_run > 0:
                below_runs.append(cur_run)
            cur_run = 0
    if cur_run > 0:
        below_runs.append(cur_run)

    max_run_below_X = max(below_runs) if below_runs else 0
    mean_run_below_X = float(np.mean(below_runs)) if below_runs else 0.0

    return {
        "q": q,
        "lam": float(lam),
        "X_q": float(X),
        "n_steps": n_steps,
        "P_max": float(P_max),
        "argmax_coords": {
            "a": float(a_max),
            "b": float(b_max),
            "branch_i": int(i_max),
            "k": int(k_max),
        },
        "stability": stability,
        "deep_threshold_99p99": float(deep_thresh),
        "empirical_cluster_stats": {
            "mean_cluster_size": mean_cluster_size,
            "histogram": cluster_hist,
            "num_clusters": len(cluster_sizes),
        },
        "runs_below_X": {
            "max_run": int(max_run_below_X),
            "mean_run": mean_run_below_X,
            "num_runs": len(below_runs),
        },
    }


def main():
    print("=" * 80)
    print("EVT Extremal Index & Local Stability Probe: Hecke G_q BCZ Maps")
    print("=" * 80)

    results = {}

    for q in [3, 5, 7]:
        print(f"\n[q={q}] Running 10^7-step orbit...")
        result = run_long_orbit(q, n_steps=10_000_000, burn=500)
        results[q] = result

        print(f"  λ_q = {result['lam']:.6f}")
        print(f"  X(q) = {result['X_q']:.8f}")
        print(f"  P_max = {result['P_max']:.8f}")
        print(f"  argmax: a*={result['argmax_coords']['a']:.8f}, "
              f"b*={result['argmax_coords']['b']:.8f}")
        print(f"  branch i={result['argmax_coords']['branch_i']}, "
              f"k={result['argmax_coords']['k']}")
        stab = result['stability']
        print(f"  Jacobian trace={stab['trace']:.6f}, "
              f"type={stab['type']}")
        if stab['type'] == 'parabolic':
            print(f"    (parabolic confirmed: |trace|={stab['abs_trace']:.6f})")
        elif stab['type'] == 'elliptic':
            print(f"    rotation angle: {stab.get('rotation_angle_degrees', 'N/A')}°")
        elif stab['type'] == 'hyperbolic':
            print(f"    multipliers: {stab.get('multipliers', 'N/A')}")

        empi = result['empirical_cluster_stats']
        print(f"  99.99-percentile exceedances:")
        print(f"    mean cluster size: {empi['mean_cluster_size']:.3f}")
        print(f"    num clusters: {empi['num_clusters']}")
        print(f"    histogram (top 5): {dict(sorted(empi['histogram'].items(), key=lambda x: x[1], reverse=True)[:5])}")

        runs = result['runs_below_X']
        print(f"  Runs below X(q):")
        print(f"    max run: {runs['max_run']}")
        print(f"    mean run: {runs['mean_run']:.3f}")
        print(f"    num runs: {runs['num_runs']}")

    # Write results to JSON
    output_path = "/Users/za/Documents/farey-hecke/projects/evt-farey-gaps/gq_edge_results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n\nResults written to: {output_path}")

    # Summary report
    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'q':>3} {'P_max':>12} {'trace':>10} {'type':>12} {'mean_cluster':>14}")
    print("-" * 55)
    for q in [3, 5, 7]:
        r = results[q]
        print(f"{q:>3} {r['P_max']:>12.8f} {r['stability']['trace']:>10.6f} "
              f"{r['stability']['type']:>12} {r['empirical_cluster_stats']['mean_cluster_size']:>14.3f}")

    print("\n" + "=" * 80)
    print("READY FOR JUDGING")
    print("=" * 80)


if __name__ == "__main__":
    main()
