"""Function-field Farey + cluster=2 EXPLORATORY (q=2, F_2[T]).

This is a starting-point implementation — explicitly NOT the rigorous
version. The function-field Farey case differs subtly from Q:

  - F_q((1/T)) is non-archimedean (no total order in the usual sense)
  - The "cross-product" a·b' − a'·b lives in F_q^× = F_2^× = {1}, only
    one nonzero element (unlike Q where it can be ±1)
  - Stern-Brocot tree branches q-fold, not 2-fold

We use the following PRAGMATIC ordering (not canonical):
  Order a/b by the float value of the "characteristic" embedding
    a/b ↦ (a(2) / b(2))  ∈ ℚ
  where p(2) substitutes T=2 in the integer-encoded polynomial.
  This is NOT the usual function-field valuation, but it gives a total
  order and lets us extract empirical cluster statistics for diagnostic
  comparison with our q*_BCZ closed form.

If the empirical cluster=2 % is comparable to the Q case (~95% at q=0.99),
it suggests the function-field analog mirrors the Q result under this
embedding; if not, we learn something interesting either way.

Polynomial encoding: f = Σ c_i T^i with c_i ∈ {0,1} ↔ integer with bit i = c_i.
Addition over F_2 = XOR. Multiplication = "carry-less" multiplication.
"""
import math, time, json
from collections import Counter

# --- F_2[T] polynomial arithmetic ---

def deg(a):
    return a.bit_length() - 1 if a > 0 else -1

def gf2_mul(a, b):
    """Carry-less multiplication."""
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r

def gf2_divmod(a, b):
    """Return (q, r) with a = q*b + r, deg(r) < deg(b)."""
    if b == 0:
        raise ZeroDivisionError
    db = deg(b)
    q = 0
    while deg(a) >= db:
        shift = deg(a) - db
        q ^= (1 << shift)
        a ^= b << shift
    return q, a

def gf2_gcd(a, b):
    while b:
        _, r = gf2_divmod(a, b)
        a, b = b, r
    return a

def is_monic(b):
    """Monic in F_2 = leading coeff is 1, which is automatic for any nonzero b in F_2 encoding."""
    return b > 0  # all nonzero F_2 polynomials are monic

# --- Farey enumeration ---

def farey_F2T(N, monic_b_only=True):
    """Enumerate all coprime a/b with deg(a) < deg(b) ≤ N, b > 0."""
    pairs = []
    for b in range(2, 1 << (N + 1)):  # b ∈ [2, 2^{N+1})  ⇔ deg(b) ∈ [1, N]
        if deg(b) > N:
            continue
        # b is monic in F_2 (leading bit = 1)
        for a in range(1, 1 << deg(b)):  # 0 ≤ deg(a) < deg(b)
            if gf2_gcd(a, b) == 1:
                pairs.append((a, b))
    return pairs

def value_embed(a, b):
    """Map a/b → a(2)/b(2) as a rational — for total ordering."""
    return a / b  # integers; this works since a < b in int sense too (deg a < deg b)

def cluster_stats(gaps, q_list):
    """Cluster=2 diagnostic on sorted gap list."""
    n = len(gaps)
    sorted_g = sorted(gaps)
    results = {}
    for q in q_list:
        idx = min(int(q * n), n - 1)
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
        if cur > 0:
            sizes[cur] += 1
        total = sum(sizes.values())
        s2 = sizes.get(2, 0)
        s3p = sum(c for s, c in sizes.items() if s >= 3)
        results[f"{q:.4f}"] = {
            "total_clusters": total,
            "size_2": s2,
            "size_3_plus": s3p,
            "pct_size_2": s2 / total * 100 if total > 0 else 0,
            "pct_size_3_plus": s3p / total * 100 if total > 0 else 0,
            "max_size": max(sizes.keys()) if sizes else 0,
            "hist": {str(k): v for k, v in sorted(sizes.items()) if k <= 10},
        }
    return results

def run(N):
    print(f"=== F_2[T] Farey at deg N ≤ {N} ===", flush=True)
    t0 = time.time()
    pairs = farey_F2T(N)
    print(f"  enumerated {len(pairs):,} coprime pairs in {time.time()-t0:.1f}s", flush=True)
    # Sort by characteristic embedding
    pairs.sort(key=lambda ab: value_embed(*ab))
    # Gaps between consecutive embedded values
    gaps = [value_embed(*pairs[i+1]) - value_embed(*pairs[i]) for i in range(len(pairs) - 1)]
    print(f"  computed {len(gaps):,} gaps", flush=True)
    res = cluster_stats(gaps, [0.95, 0.99, 0.999])
    for qk, v in res.items():
        print(f"  q={qk}: size-2={v['pct_size_2']:.2f}%, size-3+={v['pct_size_3_plus']:.4f}%, max={v['max_size']}", flush=True)
    return {"N": N, "n_pairs": len(pairs), "elapsed_s": time.time() - t0, "results": res}

if __name__ == "__main__":
    out = {"caveat": "Uses T=2 characteristic embedding for total order, NOT the function-field valuation. Empirical diagnostic only.",
           "runs": {}}
    for N in [6, 8, 10, 12]:
        try:
            out["runs"][str(N)] = run(N)
        except Exception as e:
            print(f"N={N} failed: {e}")
            break

    with open("/Users/za/Documents/Farey NOW/projects/mimo-mini-project/function_field/farey_F2T_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nDone — see farey_F2T_results.json", flush=True)
