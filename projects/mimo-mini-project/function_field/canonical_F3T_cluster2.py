"""Function-field Farey + cluster=2 — CANONICAL F_3[T] version.

Same canonical setup as canonical_F2T_cluster2.py, but for q = 3.
F_3 elements are {0, 1, 2}. Polynomials are encoded as tuples of
coefficients (low-to-high). Multiplication / division / gcd implemented
explicitly.

Mathematically: the Farey level-N coprime pairs (a, b) ∈ F_3[T] × F_3[T]
with b *monic*, deg(a) < deg(b) ≤ N, gcd(a, b) = 1. We canonicalize a
by considering all coprime a with deg < deg b (no extra scaling needed
since b is already monic).

We use lex order on the Laurent expansion (c_1, c_2, ...) with
0 < 1 < 2. The "cluster" diagnostic on consecutive gaps is the same.
"""
from __future__ import annotations
import math, time, json
from collections import Counter

Q = 3  # field size

# ----- F_3[T] polynomial arithmetic (poly = tuple of coeffs, low-to-high) -----

def poly_deg(p):
    """Degree of p; -1 if p = 0."""
    for i in range(len(p) - 1, -1, -1):
        if p[i] != 0:
            return i
    return -1

def poly_trim(p):
    """Strip trailing zeros."""
    d = poly_deg(p)
    return tuple(p[:d + 1]) if d >= 0 else ()

def poly_add(a, b):
    n = max(len(a), len(b))
    return poly_trim(tuple(((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % Q for i in range(n)))

def poly_sub(a, b):
    n = max(len(a), len(b))
    return poly_trim(tuple(((a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)) % Q for i in range(n)))

def poly_mul(a, b):
    if not a or not b:
        return ()
    r = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            r[i + j] = (r[i + j] + ai * bj) % Q
    return poly_trim(tuple(r))

def poly_scale(a, c):
    """Scalar multiply."""
    if c == 0 or not a:
        return ()
    return poly_trim(tuple((ai * c) % Q for ai in a))

def inv_mod_p(x):
    """Inverse mod p (p = Q = 3, prime)."""
    return pow(x, Q - 2, Q)

def poly_divmod(a, b):
    """Return (q, r) with a = q*b + r, deg(r) < deg(b)."""
    if not b:
        raise ZeroDivisionError
    da = poly_deg(a)
    db = poly_deg(b)
    if da < db:
        return ((), a)
    r = list(a)
    qres = [0] * (da - db + 1)
    lc_b_inv = inv_mod_p(b[db])
    while True:
        dr = poly_deg(r)
        if dr < db:
            break
        c = (r[dr] * lc_b_inv) % Q
        shift = dr - db
        qres[shift] = c
        # r := r - c * b * T^shift
        for j in range(db + 1):
            r[shift + j] = (r[shift + j] - c * b[j]) % Q
    return (poly_trim(tuple(qres)), poly_trim(tuple(r)))

def poly_gcd(a, b):
    while b:
        _, r = poly_divmod(a, b)
        a, b = b, r
    return a

def is_monic(p):
    if not p:
        return False
    return p[poly_deg(p)] == 1


# ----- Laurent expansion in F_3((1/T)) -----

def laurent_coeffs(a, b, K):
    """Return (c_1, ..., c_K) ∈ F_3^K so that a/b = Σ c_i T^{-i}.
    Assumes deg(a) < deg(b) and b monic.

    Algorithm: at each step, multiply current remainder r by T (i.e., shift
    its coefficients one to the right in our 'low-to-high' representation
    by *prepending* a zero), then check whether deg(r) == deg(b); if so
    c_i = leading_coeff(r), and we subtract c_i * b from r.
    """
    db = poly_deg(b)
    # b is monic by precondition: b[db] = 1.
    r = list(a)
    coeffs = []
    for _ in range(K):
        # r := r * T: shift to higher degree → prepend a zero in low-index storage.
        r = [0] + r
        dr = poly_deg(tuple(r))
        if dr == db:
            c = r[db]
            coeffs.append(c)
            # r := r - c * b
            for j in range(db + 1):
                r[j] = (r[j] - c * b[j]) % Q
        else:
            coeffs.append(0)
    return tuple(coeffs)


# ----- Enumeration of Farey level N over F_3[T] -----

def enumerate_polys(max_deg, monic_only=False):
    """All polys with deg ≤ max_deg (including 0, with deg = -1)."""
    out = []
    if not monic_only:
        out.append(())  # zero poly
    # For each degree d from 0 to max_deg, generate all polys of that degree.
    for d in range(0, max_deg + 1):
        # Leading coeff: 1..Q-1 (if not monic_only), else just 1.
        lead_choices = [1] if monic_only else list(range(1, Q))
        # Lower coeffs: Q^d possibilities.
        for low_idx in range(Q ** d):
            low = []
            n = low_idx
            for _ in range(d):
                low.append(n % Q)
                n //= Q
            for lc in lead_choices:
                p = tuple(low + [lc])
                out.append(p)
    return out

def farey_level(N):
    """Reduced (a, b) with b monic, deg(b) ∈ [1, N], deg(a) < deg(b), gcd(a,b)=1.
    a is any (possibly with leading coeff ≠ 1) of deg < deg(b)."""
    pairs = []
    # Enumerate b first (monic, deg in [1, N]).
    monic_bs = enumerate_polys(N, monic_only=True)
    monic_bs = [b for b in monic_bs if poly_deg(b) >= 1]

    for b in monic_bs:
        db = poly_deg(b)
        # All a of deg < db (including a = 0? — no, we exclude 0/b = 0 as a Farey fraction).
        # Actually we want a coprime to b, so a ≠ 0 automatically.
        # Enumerate a of degree from 0 to db-1.
        for da in range(0, db):
            for lead_a in range(1, Q):
                for low_idx in range(Q ** da):
                    low = []
                    n = low_idx
                    for _ in range(da):
                        low.append(n % Q)
                        n //= Q
                    a = tuple(low + [lead_a])
                    g = poly_gcd(a, b)
                    if poly_deg(g) == 0:  # gcd is a nonzero scalar = unit
                        pairs.append((a, b))
    return pairs


# ----- Gaps -----

def canonical_gap_log(a1, b1, a2, b2):
    """Return d = deg(a1*b2 - a2*b1) - deg(b1) - deg(b2). Gap = q^d."""
    cross = poly_sub(poly_mul(a1, b2), poly_mul(a2, b1))
    return poly_deg(cross) - poly_deg(b1) - poly_deg(b2)


# ----- Cluster diagnostic -----

def cluster_stats(gaps_log, q_list):
    n = len(gaps_log)
    if n == 0:
        return {f"{q:.4f}": None for q in q_list}
    sorted_g = sorted(gaps_log)
    results = {}
    for q in q_list:
        idx = min(int(q * n), n - 1)
        thr = sorted_g[idx]
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
            "threshold_log_q": thr,
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


# ----- Run -----

def run(N):
    print(f"\n=== F_3[T] canonical Farey, deg ≤ {N} ===", flush=True)
    t0 = time.time()
    pairs = farey_level(N)
    print(f"  enumerated {len(pairs):,} coprime pairs in {time.time()-t0:.2f}s", flush=True)
    K = 2 * N + 2
    t1 = time.time()
    keyed = [(laurent_coeffs(a, b, K), a, b) for (a, b) in pairs]
    keyed.sort(key=lambda x: x[0])
    print(f"  sorted by Laurent-lex in {time.time()-t1:.2f}s (K={K})", flush=True)

    t2 = time.time()
    gaps_log = []
    n_sb = 0
    for i in range(len(keyed) - 1):
        _, a1, b1 = keyed[i]
        _, a2, b2 = keyed[i + 1]
        d = canonical_gap_log(a1, b1, a2, b2)
        gaps_log.append(d)
        if d == -poly_deg(b1) - poly_deg(b2):
            n_sb += 1
    print(f"  computed {len(gaps_log):,} gaps in {time.time()-t2:.2f}s "
          f"(SB-adjacent: {n_sb/len(gaps_log)*100:.2f}%)", flush=True)

    res = cluster_stats(gaps_log, [0.95, 0.99, 0.999])
    for qk, v in res.items():
        if v is None: continue
        print(f"  q_diag={qk}: size-2={v['pct_size_2']:.2f}%, "
              f"size-3+={v['pct_size_3_plus']:.4f}%, max={v['max_size']}, "
              f"thr=3^{v['threshold_log_q']}", flush=True)
    return {
        "N": N,
        "n_pairs": len(pairs),
        "n_gaps": len(gaps_log),
        "sb_adjacent_pct": 100.0 * n_sb / len(gaps_log) if gaps_log else 0,
        "elapsed_s": time.time() - t0,
        "results": res,
    }


if __name__ == "__main__":
    # Sanity-check the inv_mod / divmod first
    assert poly_divmod((1, 1), (1, 1)) == ((1,), ()), "self-divide should give (1, 0)"
    assert poly_gcd((1, 1), (1, 1)) == (1, 1), "gcd(p,p) = p"
    assert poly_gcd((1, 1, 1), (1, 1)) == (2,) or poly_gcd((1,1,1), (1,1)) == (1,), \
        f"gcd test: got {poly_gcd((1,1,1),(1,1))}"

    out = {
        "description": "Canonical F_3[T] Farey cluster=2 diagnostic. Lex order on Laurent expansion in F_3((1/T)).",
        "comparison_Q": "At q_diag=0.99 in Q (BCZ chain): size-2 ≈ 95%, size-3+ ≈ 0%, max = 2.",
        "runs": {},
    }
    for N in [3, 4, 5]:
        try:
            out["runs"][str(N)] = run(N)
        except Exception as e:
            import traceback; traceback.print_exc()
            print(f"N={N} failed: {e}")
            break

    out_path = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/function_field/canonical_F3T_results.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nDone — see {out_path}", flush=True)
