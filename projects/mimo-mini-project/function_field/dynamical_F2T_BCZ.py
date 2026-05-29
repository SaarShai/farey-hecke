"""Dynamical function-field BCZ analog over F_2[T] (and F_3[T]).

This script investigates whether the DYNAMICAL recurrence analog of the
BCZ map over function fields exhibits the "cluster <= 2" universality that
holds in the rational case.

Two recurrences are explored:

(A) Hall recurrence (direct port of the rational BCZ chain):
    b_{i+2} = k_{i+1} * b_{i+1} + b_i   (char-2 addition)
    where k_{i+1} = (T^N + b_i) // b_{i+1}   in F_q[T].
    EMPIRICAL FINDING: every orbit collapses to a 2-cycle within ~4 steps.
    The dynamics is NOT ergodic on the Farey set. This is documented as a
    structural obstruction (see Section A below).

(B) Function-field Gauss map (continued-fraction shift):
    For x = a/b in m_inf = (1/T) F_q[[1/T]], the next iterate is
        T_Gauss(a/b) = r/a   where  b = q(T) * a + r  with deg r < deg a.
    The partial quotients k_i = q(T) have geometric distribution
    P(deg k = d) = (q-1)/q^d (a known clean fact - Berthe-Nakada).
    This IS an ergodic dynamics on m_inf and the natural function-field
    analog of the BCZ first-return map (modulo a different choice of
    Poincare section than Athreya-Cheung's).

For (B), we compute the cluster diagnostic on the "gap product"
    g_i = |x_i| * |x_{i+1}| = q^{xlog_i + xlog_{i+1}}
where xlog_i = deg(num x_i) - deg(denom x_i) < 0. This is the
function-field analog of X_i = x_i * x_{i+1} on the BCZ triangle, where
EXTREME = small g_i (analogous to extreme = small X_i = large gap = top
quantile in the BCZ chain).

KEY EMPIRICAL FINDING (this script):
- Over F_2(T): cluster <= 2 holds for the most extreme ~0.3% tail of gaps
  (thr log_2 g < -12); cluster jumps to >2 at thr -11.
- Over F_3(T): cluster <= 2 holds for the most extreme ~0.3% tail (thr log_3
  g < -8); cluster jumps to >2 at thr -7.
- This is QUALITATIVELY weaker than the rational case (where cluster <= 2
  holds on a *much larger* upper-quantile range, ~13.8% of gaps).
- The phenomenon over F_q(T) is more like "the few most-extreme gaps are
  isolated" rather than "a structural cluster bound".

USAGE: python3 dynamical_F2T_BCZ.py
       Outputs: dynamical_F2T_BCZ_results.json with full data.
"""
from __future__ import annotations
import json
import random
import time
from collections import Counter
from typing import Dict, List, Tuple

# Reuse F_2[T] poly arithmetic from canonical_F2T_cluster2.
from canonical_F2T_cluster2 import (
    deg, gf2_mul, gf2_divmod, gf2_gcd, farey_level,
)
# Reuse F_3[T] poly arithmetic from canonical_F3T_cluster2.
from canonical_F3T_cluster2 import (
    poly_deg, poly_add, poly_mul, poly_divmod, poly_sub,
)


# =====================================================================
# PART A: Hall recurrence over F_2[T]  (direct port -- collapses to 2-cycles)
# =====================================================================

def hall_step_F2(a_prev: int, b_prev: int, a_cur: int, b_cur: int,
                 T_N: int) -> Tuple[int, int]:
    """One step of the Hall recurrence over F_2[T]:
        k = (T^N + b_prev) // b_cur   (polynomial quotient in F_2[T])
        b_next = k * b_cur + b_prev   (char-2 addition = XOR)
        a_next = k * a_cur + a_prev
    Returns (a_next, b_next).
    """
    num = T_N ^ b_prev
    k, _ = gf2_divmod(num, b_cur)
    a_next = gf2_mul(k, a_cur) ^ a_prev
    b_next = gf2_mul(k, b_cur) ^ b_prev
    return a_next, b_next, k


def hall_trajectory_F2(seed: Tuple[int, int, int, int], N: int, max_steps: int = 200):
    """Iterate the Hall recurrence from seed (a_prev, b_prev, a_cur, b_cur) and
    return the full trajectory (until 2-cycle or max_steps reached).
    """
    T_N = 1 << N
    a_prev, b_prev, a_cur, b_cur = seed
    trajectory = [(a_prev, b_prev), (a_cur, b_cur)]
    seen = {(a_prev, b_prev, a_cur, b_cur): 0}
    for step in range(max_steps):
        a_next, b_next, k = hall_step_F2(a_prev, b_prev, a_cur, b_cur, T_N)
        trajectory.append((a_next, b_next))
        state = (a_prev, b_prev, a_cur, b_cur, a_next, b_next)
        a_prev, b_prev = a_cur, b_cur
        a_cur, b_cur = a_next, b_next
        cur_state = (a_prev, b_prev, a_cur, b_cur)
        if cur_state in seen:
            cycle_start = seen[cur_state]
            cycle_len = step + 1 - cycle_start
            return trajectory, cycle_start, cycle_len
        seen[cur_state] = step + 1
    return trajectory, None, None


def part_A_collapse_demo(N_list: List[int]) -> Dict:
    """Demonstrate that the Hall chain collapses to a 2-cycle in F_2(T)
    from MANY Farey-adjacent seeds, for several values of N."""
    out = {"N_list": N_list, "per_N": {}}
    for N in N_list:
        pairs_F = farey_level(N)
        # Find all Farey-adjacent ordered pairs (cross-product = 1 in F_2)
        sb_pairs = []
        for (a, b) in pairs_F:
            for (a2, b2) in pairs_F:
                if (a, b) == (a2, b2):
                    continue
                if (gf2_mul(a, b2) ^ gf2_mul(a2, b)) == 1:
                    sb_pairs.append((a, b, a2, b2))

        cycle_lens = Counter()
        cycle_starts = Counter()
        distinct_visited = []
        for seed in sb_pairs:
            traj, cs, cl = hall_trajectory_F2(seed, N, max_steps=80)
            if cl is None:
                continue
            cycle_lens[cl] += 1
            cycle_starts[cs] += 1
            distinct_visited.append(len(set(traj)))
        info = {
            "n_farey_pairs": len(pairs_F),
            "n_sb_adjacent_pairs": len(sb_pairs),
            "cycle_length_distribution": dict(cycle_lens),
            "transient_start_distribution": dict(cycle_starts),
            "distinct_visited_mean": (sum(distinct_visited) / len(distinct_visited)
                                       if distinct_visited else None),
            "distinct_visited_max": max(distinct_visited) if distinct_visited else None,
        }
        out["per_N"][str(N)] = info
        print(f"  Hall on F_2(T) N={N}: {len(sb_pairs)} SB seeds, cycle lens = {dict(cycle_lens)}, "
              f"avg distinct visited = {info['distinct_visited_mean']:.2f}")
    return out


# =====================================================================
# PART B: Function-field Gauss map (the ergodic chain)
# =====================================================================

def gauss_orbit_F2(a: int, b: int, max_steps: int):
    """Iterate T_Gauss(a/b) = r/a where b = q*a + r in F_2[T].
    Returns (partial_quotients_degs, xlog_sequence)
    where xlog_i = deg(num x_i) - deg(denom x_i) (negative, = log_2 |x_i|).
    """
    pqs = []
    xlogs = []
    for _ in range(max_steps):
        if a == 0:
            break
        xlogs.append(deg(a) - deg(b))
        q, r = gf2_divmod(b, a)
        pqs.append(deg(q))
        a, b = r, a
    return pqs, xlogs


def gauss_orbit_F3(a: tuple, b: tuple, max_steps: int):
    """Iterate the F_3 Gauss map."""
    pqs = []
    xlogs = []
    for _ in range(max_steps):
        if not a or poly_deg(a) < 0:
            break
        xlogs.append(poly_deg(a) - poly_deg(b))
        q, r = poly_divmod(b, a)
        pqs.append(poly_deg(q))
        a, b = r, a
    return pqs, xlogs


def cluster_diagnostic_by_threshold(gap_logs: List[int],
                                     thr_min: int = -25,
                                     thr_max: int = 0) -> List[Dict]:
    """For each integer threshold value, compute (n_extreme, n_clusters, hist, max_size).
    'Extreme' means gap_log STRICTLY BELOW threshold (= small gap = small product
    |x_i x_{i+1}|, the function-field analog of the BCZ extreme tail).
    """
    results = []
    for t in range(thr_min, thr_max + 1):
        sizes = Counter()
        cur = 0
        for g in gap_logs:
            if g < t:
                cur += 1
            else:
                if cur > 0:
                    sizes[cur] += 1
                    cur = 0
        if cur > 0:
            sizes[cur] += 1
        n_ext = sum(1 for g in gap_logs if g < t)
        total = sum(sizes.values())
        max_size = max(sizes.keys()) if sizes else 0
        s1 = sizes.get(1, 0)
        s2 = sizes.get(2, 0)
        s3p = sum(c for s, c in sizes.items() if s >= 3)
        results.append({
            "threshold": t,
            "n_extreme": n_ext,
            "n_clusters": total,
            "max_size": max_size,
            "n_size_1": s1,
            "n_size_2": s2,
            "n_size_3_plus": s3p,
            "hist": {str(k): v for k, v in sorted(sizes.items()) if k <= 10},
        })
    return results


def find_cluster_boundary(thr_results: List[Dict]) -> Dict:
    """Find the largest threshold value at which cluster_max <= 2 holds."""
    boundary = None
    for r in thr_results:
        if r["max_size"] <= 2 and r["max_size"] > 0:
            boundary = r["threshold"]
    return {"largest_thr_cluster_le_2": boundary}


def part_B_gauss_F2(precision: int, n_orbits: int, seed: int = 2026) -> Dict:
    """Run F_2 Gauss-map experiment."""
    random.seed(seed)
    all_gap_logs = []
    all_pq_degs = []
    orbit_lengths = []
    for orb in range(n_orbits):
        # Random Laurent series at given precision: b monic, deg b = precision; a random, deg a < precision.
        b = (1 << precision) | random.randint(0, (1 << precision) - 1)
        a = random.randint(1, (1 << precision) - 1)
        pqs, xlogs = gauss_orbit_F2(a, b, max_steps=4 * precision)
        all_pq_degs.extend(pqs)
        gaps = [xlogs[i] + xlogs[i + 1] for i in range(len(xlogs) - 1)]
        all_gap_logs.extend(gaps)
        orbit_lengths.append(len(xlogs))
    print(f"  F_2 Gauss: {n_orbits} orbits, total {sum(orbit_lengths):,} CF steps, "
          f"{len(all_gap_logs):,} gaps. Mean deg(k) = {sum(all_pq_degs)/len(all_pq_degs):.3f} "
          f"(theory: 2.0)")

    pq_hist = Counter(all_pq_degs)
    gap_hist = Counter(all_gap_logs)
    thr_results = cluster_diagnostic_by_threshold(all_gap_logs, thr_min=-25, thr_max=0)
    boundary = find_cluster_boundary(thr_results)

    return {
        "field": "F_2(T)",
        "precision": precision,
        "n_orbits": n_orbits,
        "orbit_lengths": orbit_lengths,
        "n_partial_quotients_total": len(all_pq_degs),
        "n_gaps_total": len(all_gap_logs),
        "mean_deg_k": sum(all_pq_degs) / len(all_pq_degs),
        "theory_mean_deg_k_q_over_q_minus_1": 2.0,  # 2/(2-1)
        "partial_quotient_deg_distribution": {str(k): v for k, v in sorted(pq_hist.items())[:15]},
        "gap_log_distribution_smallest_15": {str(k): v for k, v in sorted(gap_hist.items())[:15]},
        "gap_log_distribution_largest_5": {str(k): v for k, v in sorted(gap_hist.items())[-5:]},
        "threshold_sweep": thr_results,
        "cluster_le_2_boundary": boundary,
    }


def part_B_gauss_F3(precision: int, n_orbits: int, seed: int = 2026) -> Dict:
    """Run F_3 Gauss-map experiment."""
    random.seed(seed)
    all_gap_logs = []
    all_pq_degs = []
    orbit_lengths = []
    for orb in range(n_orbits):
        # Random F_3 polys: b monic of degree precision; a of degree precision - 1.
        b = tuple([random.randint(0, 2) for _ in range(precision)] + [1])
        a_deg = random.randint(precision - 2, precision - 1)
        a = tuple([random.randint(0, 2) for _ in range(a_deg)] + [random.choice([1, 2])])
        pqs, xlogs = gauss_orbit_F3(a, b, max_steps=4 * precision)
        all_pq_degs.extend(pqs)
        gaps = [xlogs[i] + xlogs[i + 1] for i in range(len(xlogs) - 1)]
        all_gap_logs.extend(gaps)
        orbit_lengths.append(len(xlogs))
    print(f"  F_3 Gauss: {n_orbits} orbits, total {sum(orbit_lengths):,} CF steps, "
          f"{len(all_gap_logs):,} gaps. Mean deg(k) = {sum(all_pq_degs)/len(all_pq_degs):.3f} "
          f"(theory: 1.5)")

    pq_hist = Counter(all_pq_degs)
    gap_hist = Counter(all_gap_logs)
    thr_results = cluster_diagnostic_by_threshold(all_gap_logs, thr_min=-20, thr_max=0)
    boundary = find_cluster_boundary(thr_results)

    return {
        "field": "F_3(T)",
        "precision": precision,
        "n_orbits": n_orbits,
        "orbit_lengths": orbit_lengths,
        "n_partial_quotients_total": len(all_pq_degs),
        "n_gaps_total": len(all_gap_logs),
        "mean_deg_k": sum(all_pq_degs) / len(all_pq_degs),
        "theory_mean_deg_k_q_over_q_minus_1": 1.5,  # 3/(3-1)
        "partial_quotient_deg_distribution": {str(k): v for k, v in sorted(pq_hist.items())[:15]},
        "gap_log_distribution_smallest_15": {str(k): v for k, v in sorted(gap_hist.items())[:15]},
        "gap_log_distribution_largest_5": {str(k): v for k, v in sorted(gap_hist.items())[-5:]},
        "threshold_sweep": thr_results,
        "cluster_le_2_boundary": boundary,
    }


# =====================================================================
# Main
# =====================================================================

def main() -> Dict:
    out = {
        "description": (
            "Dynamical function-field BCZ analog (F_2(T) and F_3(T)). "
            "Part A: Hall recurrence (direct port) -- collapses to 2-cycles, "
            "NOT ergodic. Part B: function-field Gauss map (continued-fraction "
            "shift) -- ergodic; cluster<=2 holds in the extreme tail only "
            "(top ~0.3% of gaps), unlike Q where cluster<=2 holds on top ~13.8%."
        ),
        "comparison_Q_BCZ": {
            "q_star_BCZ": "(11 - 8 * ln(3/2))/9 ≈ 0.86181",
            "threshold_t_star": "2/9",
            "cluster_size_at_q_star": "max = 2, size-2 ≈ 95%",
            "extreme_quantile_at_threshold": "≈ 0.138 (P(X < 2/9) under BCZ density)",
        },
        "parts": {},
    }
    t0 = time.time()

    print("=== PART A: Hall recurrence over F_2(T) (collapse-to-2-cycle demo) ===")
    out["parts"]["A_hall_F2T"] = part_A_collapse_demo([4, 5, 6])

    print("\n=== PART B: Gauss-map dynamics over F_2(T) (the ergodic chain) ===")
    out["parts"]["B_gauss_F2T"] = part_B_gauss_F2(precision=30000, n_orbits=8)

    print("\n=== PART B': Gauss-map dynamics over F_3(T) ===")
    out["parts"]["B_gauss_F3T"] = part_B_gauss_F3(precision=12000, n_orbits=6)

    out["elapsed_s"] = time.time() - t0
    return out


if __name__ == "__main__":
    result = main()
    out_path = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/function_field/dynamical_F2T_BCZ_results.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nDone in {result['elapsed_s']:.1f}s -- see {out_path}")
    # Print top-line summary
    bdy_F2 = result["parts"]["B_gauss_F2T"]["cluster_le_2_boundary"]["largest_thr_cluster_le_2"]
    bdy_F3 = result["parts"]["B_gauss_F3T"]["cluster_le_2_boundary"]["largest_thr_cluster_le_2"]
    print(f"\n=== SUMMARY ===")
    print(f"F_2(T) cluster<=2 boundary: log_2 g < {bdy_F2}")
    print(f"F_3(T) cluster<=2 boundary: log_3 g < {bdy_F3}")
    print(f"Q reference: cluster<=2 on TOP ~13.8% of gaps (q* ≈ 0.862, t* = 2/9).")
