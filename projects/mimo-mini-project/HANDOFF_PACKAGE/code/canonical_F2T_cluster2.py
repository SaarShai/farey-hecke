"""Function-field Farey + cluster=2 — CANONICAL F_2[T] version.

Replaces the earlier `farey_F2T_cluster2.py` (T=2 embedding) with the
correct, canonical, **valuation-based** ordering on F_2((1/T)).

Setup
-----
- Field: F_2(T), local completion F_2((1/T)) with valuation |f| = 2^{deg f}.
- Farey of level N: reduced (a, b), b monic, deg(b) ≤ N, 0 ≤ deg(a) < deg(b),
  gcd(a, b) = 1 in F_2[T]. (Over F_2 every nonzero polynomial is monic.)
- Each a/b ∈ F_2((1/T)) has |a/b| < 1, so it equals a Laurent tail
    a/b = c_1·T^{-1} + c_2·T^{-2} + c_3·T^{-3} + ...
  with c_i ∈ F_2. We use lexicographic order on (c_1, c_2, ...) as the
  canonical total order on the unit ball — this is the non-archimedean
  analog of the usual real order on (0, 1).
- Two reduced fractions a/b, a'/b' are Stern-Brocot adjacent
  ⟺ a·b' - a'·b ∈ F_2^× = {1}. In that case
    |a/b - a'/b'| = 2^{-(deg b + deg b')}      (canonical gap)
  Otherwise the canonical gap has the same form but with the numerator
  degree d = deg(a·b' - a'·b) > 0:
    |a/b - a'/b'| = 2^{d - deg b - deg b'}.

What we measure
---------------
We sort all level-N Farey pairs by their Laurent-lex value, then take
consecutive pair gaps (the multiset of |a/b - a'/b'| above). On this gap
sequence we compute the standard "cluster=k" diagnostic for the rational
case: for a quantile q_diag ∈ {0.95, 0.99, 0.999}, the cluster threshold
is the q_diag-quantile gap value, and a "cluster of size s" is a maximal
run of consecutive positions whose gap exceeds the threshold. We then
report (% size 2, % size 3+, max cluster) for each q_diag.

Honest caveats
--------------
- F_2 is the smallest possible (q + 1) = 3 branching at the SB tree, so
  finite-N effects are largest here. q = 3, 4, 5 would be more telling but
  the code can be ported easily.
- "Lex on Laurent coefficients" is one canonical choice; others (different
  fundamental domain, reverse lex) would give the same gap multiset but
  potentially a different *consecutive* pattern. Cluster sizes can shift
  by O(1).
- N ≤ 12 is brute-force only — no asymptotic claim is made.
"""
from __future__ import annotations
import math, time, json
from collections import Counter

# ----- F_2[T] arithmetic (polynomials encoded as integers, bit i = coeff of T^i) -----

def deg(a: int) -> int:
    return a.bit_length() - 1 if a > 0 else -1

def gf2_mul(a: int, b: int) -> int:
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r

def gf2_divmod(a: int, b: int):
    if b == 0:
        raise ZeroDivisionError
    db = deg(b)
    q = 0
    while a and deg(a) >= db:
        shift = deg(a) - db
        q ^= (1 << shift)
        a ^= b << shift
    return q, a

def gf2_gcd(a: int, b: int) -> int:
    while b:
        _, r = gf2_divmod(a, b)
        a, b = b, r
    return a


# ----- Laurent expansion of a/b in F_2((1/T)) -----

def laurent_coeffs(a: int, b: int, K: int) -> tuple:
    """Return (c_1, c_2, ..., c_K) ∈ F_2^K, the first K coefficients of
    a/b = c_1 T^{-1} + c_2 T^{-2} + ...   (requires deg a < deg b).

    Algorithm: long-division of a by b "from the top". At each step:
      shift a one place toward higher precision (multiply by T → bit-shift left),
      take c_i = (leading bit of a relative to deg b),
      subtract c_i · b · T^{?} from a so the leading bit drops.

    More concretely: we maintain a "remainder" r, starting r = a. Then for
    each i=1,2,…,K:
      r = r * T  (shift left by 1)
      if deg(r) == deg(b):          # then c_i = 1
        c_i = 1; r ^= b
      else:                          # deg(r) < deg(b) → c_i = 0
        c_i = 0
    """
    coeffs = []
    db = deg(b)
    r = a
    for _ in range(K):
        r <<= 1  # r := r * T
        if deg(r) == db:
            coeffs.append(1)
            r ^= b
        else:
            # deg(r) must be < db here (cannot exceed because deg(a) < deg(b) initially
            # and we only ever subtract b when deg(r) == deg(b))
            coeffs.append(0)
    return tuple(coeffs)


# ----- Enumeration of Farey level N -----

def farey_level(N: int):
    """All (a, b) with deg(a) < deg(b) ≤ N, gcd(a,b) = 1 over F_2.
    b ranges over nonzero polynomials (all monic in F_2). Returns list."""
    pairs = []
    for b in range(2, 1 << (N + 1)):
        db = deg(b)
        if db > N:
            continue
        for a in range(1, 1 << db):
            if gf2_gcd(a, b) == 1:
                pairs.append((a, b))
    return pairs


# ----- Canonical gaps -----

def canonical_gap_log(a1: int, b1: int, a2: int, b2: int) -> int:
    """Return d = deg(a1·b2 - a2·b1) - deg(b1) - deg(b2).
    The actual valuation gap is 2^d. We return d (an int, ≤ -2 for SB-adjacent).
    For SB-adjacent pairs d = -deg(b1) - deg(b2)."""
    cross = gf2_mul(a1, b2) ^ gf2_mul(a2, b1)
    return deg(cross) - deg(b1) - deg(b2)


# ----- Cluster diagnostic -----

def cluster_stats(gaps_log: list, q_list):
    """gaps_log[i] = log_2 of the i-th consecutive gap (integer).
    Threshold at quantile q is the q-th element of the sorted gaps."""
    n = len(gaps_log)
    if n == 0:
        return {f"{q:.4f}": None for q in q_list}
    sorted_g = sorted(gaps_log)
    results = {}
    for q in q_list:
        idx = min(int(q * n), n - 1)
        thr = sorted_g[idx]
        # A "cluster" = maximal run of gaps > threshold (strictly greater).
        sizes = Counter()
        cur = 0
        for g in gaps_log:
            if g > thr:
                cur += 1
            else:
                if cur > 0:
                    sizes[cur] += 1
                    cur = 0
        if cur > 0:
            sizes[cur] += 1
        total = sum(sizes.values())
        s2 = sizes.get(2, 0)
        s3p = sum(c for s, c in sizes.items() if s >= 3)
        results[f"{q:.4f}"] = {
            "threshold_log2": thr,
            "total_clusters": total,
            "size_1": sizes.get(1, 0),
            "size_2": s2,
            "size_3_plus": s3p,
            "pct_size_2": s2 / total * 100 if total > 0 else 0.0,
            "pct_size_3_plus": s3p / total * 100 if total > 0 else 0.0,
            "max_size": max(sizes.keys()) if sizes else 0,
            "hist": {str(k): v for k, v in sorted(sizes.items()) if k <= 10},
        }
    return results


# ----- Main run -----

def run(N: int, K_extra: int = 2):
    """For level N: enumerate, sort by Laurent-lex, compute consecutive gaps,
    run cluster diagnostic. K_extra = extra Laurent coeffs past 2N for tie-break."""
    print(f"\n=== F_2[T] canonical Farey, deg ≤ {N} ===", flush=True)
    t0 = time.time()
    pairs = farey_level(N)
    print(f"  enumerated {len(pairs):,} coprime pairs in {time.time()-t0:.2f}s", flush=True)

    # Precision needed: two distinct Farey fractions a/b, a'/b' of level ≤ N
    # differ by at least 2^{-2N} (since |a/b - a'/b'| ≥ 2^{0 - 2N} = 2^{-2N} when
    # the cross-product is nonzero and has degree ≥ 0). So K = 2N + 1 is sufficient
    # to distinguish any two pairs by lex order.
    K = 2 * N + K_extra
    t1 = time.time()
    keyed = [(laurent_coeffs(a, b, K), a, b) for (a, b) in pairs]
    keyed.sort(key=lambda x: x[0])
    print(f"  sorted by Laurent-lex in {time.time()-t1:.2f}s (K={K})", flush=True)

    # Sanity check: all keys distinct.
    keys_only = [k for (k, _, _) in keyed]
    distinct = len(set(keys_only))
    if distinct != len(keys_only):
        print(f"  WARNING: only {distinct}/{len(keys_only)} distinct keys (collisions!)", flush=True)

    t2 = time.time()
    gaps_log = []
    n_sb = 0  # number of consecutive pairs that are SB-adjacent
    for i in range(len(keyed) - 1):
        _, a1, b1 = keyed[i]
        _, a2, b2 = keyed[i + 1]
        d = canonical_gap_log(a1, b1, a2, b2)
        gaps_log.append(d)
        if d == -deg(b1) - deg(b2):
            n_sb += 1
    print(f"  computed {len(gaps_log):,} gaps in {time.time()-t2:.2f}s "
          f"(SB-adjacent fraction: {n_sb/len(gaps_log)*100:.2f}%)", flush=True)

    res = cluster_stats(gaps_log, [0.95, 0.99, 0.999])
    for qk, v in res.items():
        if v is None:
            continue
        print(f"  q_diag={qk}: size-2={v['pct_size_2']:.2f}%, "
              f"size-3+={v['pct_size_3_plus']:.4f}%, max={v['max_size']}, "
              f"thr=2^{v['threshold_log2']}", flush=True)
    return {
        "N": N,
        "n_pairs": len(pairs),
        "n_gaps": len(gaps_log),
        "sb_adjacent_pct": 100.0 * n_sb / len(gaps_log) if gaps_log else 0,
        "elapsed_s": time.time() - t0,
        "results": res,
    }


if __name__ == "__main__":
    out = {
        "description": "Canonical F_2[T] Farey cluster=2 diagnostic. "
                       "Ordering = lex on Laurent expansion in F_2((1/T)). "
                       "Gap = valuation |a/b - a'/b'| = 2^{deg(ab'-a'b) - deg b - deg b'}.",
        "comparison_Q": "At q_diag=0.99 in Q (BCZ chain): size-2 ≈ 95%, size-3+ ≈ 0%, max = 2.",
        "runs": {},
    }
    for N in [5, 6, 7, 8]:
        try:
            out["runs"][str(N)] = run(N)
        except Exception as e:
            print(f"N={N} failed: {e}")
            break

    out_path = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/function_field/canonical_F2T_results.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nDone — see {out_path}", flush=True)
