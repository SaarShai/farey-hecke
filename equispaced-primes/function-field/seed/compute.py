"""
Unconditional finite-data verification of Aoki–Koyama (JNT 2023) Theorem 3.4
(cyclotomic function fields).

For chosen (q, M) we:
  (a) Sieve all monic irreducible P in F_q[T] of degree <= N.
  (b) Reduce P mod M, getting class A in (F_q[T]/M)^*.
  (c) Accumulate pi_{1/2}(q^n; M, A) = sum over P irr, deg P <= n, P=A (mod M),
      of 1 / q^{deg(P)/2}.
  (d) Compute LHS_n(A) := pi_{1/2,K}(q^n) - Phi(M) * pi_{1/2}(q^n; M, A).
  (e) Compare to AK Theorem 3.4 RHS = ((2^t - 1)/2 + m(sigma_A)) log n + c + o(1)
      when A is a QR mod M, and (-1/2 + m(sigma_A)) log n + c + o(1) otherwise.

We assume m(sigma_A) = 0 (we will check this numerically a posteriori).

Output: tables and a function-field Rubinstein-Sarnak-style log-density estimate.

Unconditional in char(K) > 0 by Kaneko-Koyama-Kurokawa, "Toward the Deep Riemann
Hypothesis for GL_n", AK ref [18], cited in AK p.238 line 361.
"""

import math
import json
import time
import sys
from fq_poly import (
    f2_monic_polys_of_degree, f2_is_irreducible, f2_mod, f2_deg, f2_mul,
    fq_monic_polys_of_degree, fq_is_irreducible, fq_mod, fq_deg, fq_mul,
)


def f2_class_mod_M(P, M, modM_table=None):
    return f2_mod(P, M)


def f2_sieve_irreducibles_by_degree(N):
    """Return list `irr_by_deg` of length N+1 where irr_by_deg[d] is list of monic
    irreducible polys (packed ints) of degree d, for d = 1..N."""
    irr_by_deg = [[] for _ in range(N + 1)]
    # Degree 1: T, T+1
    for p in f2_monic_polys_of_degree(1):
        irr_by_deg[1].append(p)
    # Higher degrees: sieve with smaller primes
    for n in range(2, N + 1):
        half = n // 2
        smalls = []
        for d in range(1, half + 1):
            smalls.extend(irr_by_deg[d])
        cur = []
        for p in f2_monic_polys_of_degree(n):
            ok = True
            for r in smalls:
                if f2_mod(p, r) == 0:
                    ok = False
                    break
            if ok:
                cur.append(p)
        irr_by_deg[n] = cur
        print(f"  F_2 deg {n}: {len(cur)} irreducibles", flush=True)
    return irr_by_deg


def fq_sieve_irreducibles_by_degree(N, q):
    irr_by_deg = [[] for _ in range(N + 1)]
    for p in fq_monic_polys_of_degree(1, q):
        irr_by_deg[1].append(p)
    for n in range(2, N + 1):
        half = n // 2
        smalls = []
        for d in range(1, half + 1):
            smalls.extend(irr_by_deg[d])
        cur = []
        for p in fq_monic_polys_of_degree(n, q):
            ok = True
            for r in smalls:
                if (len(fq_mod(p, r, q)) == 1 and fq_mod(p, r, q)[0] == 0):
                    ok = False
                    break
            if ok:
                cur.append(p)
        irr_by_deg[n] = cur
        print(f"  F_{q} deg {n}: {len(cur)} irreducibles", flush=True)
    return irr_by_deg


# ---------- Unit group of (F_q[T]/M)^* by enumeration ----------

def f2_units_mod_M(M):
    """Return list of all units in F_2[T]/(M), as packed ints (representatives)."""
    dM = f2_deg(M)
    units = []
    for r in range(1 << dM):
        # gcd(r, M) == 1?
        from fq_poly import f2_gcd
        if f2_deg(f2_gcd(r, M)) == 0 and r != 0:
            units.append(r)
    return units


def fq_units_mod_M(M, q):
    dM = fq_deg(M)
    from fq_poly import fq_gcd
    units = []
    if dM == 0:
        return []
    iterator = range(q ** dM)
    for k in iterator:
        digits = []
        kk = k
        for _ in range(dM):
            digits.append(kk % q)
            kk //= q
        if all(d == 0 for d in digits):
            continue
        t = tuple(digits)
        # normalize
        while len(t) > 1 and t[-1] == 0:
            t = t[:-1]
        g = fq_gcd(M, t, q)
        if fq_deg(g) == 0:
            units.append(t)
    return units


def f2_squares_mod_M(M):
    units = f2_units_mod_M(M)
    sqs = set()
    for u in units:
        sq = f2_mod(f2_mul(u, u), M)
        sqs.add(sq)
    return sqs


def fq_squares_mod_M(M, q):
    units = fq_units_mod_M(M, q)
    sqs = set()
    for u in units:
        sq = fq_mod(fq_mul(u, u, q), M, q)
        sqs.add(sq)
    return sqs


# ---------- Main accumulation ----------

def run_f2(M, N, label):
    print(f"=== {label}: q=2, M=packed {bin(M)}, N={N} ===", flush=True)
    units = f2_units_mod_M(M)
    Phi = len(units)
    squares = f2_squares_mod_M(M)
    print(f"Phi(M) = {Phi}, units = {units}, squares = {sorted(squares)}", flush=True)

    print(f"Sieving irreducibles up to degree {N}...", flush=True)
    t0 = time.time()
    irr_by_deg = f2_sieve_irreducibles_by_degree(N)
    print(f"Sieve done in {time.time()-t0:.1f}s", flush=True)

    # For each n: pi_{1/2,K}(q^n) = sum over P irr, deg P<=n of 1/sqrt(2^{deg P})
    # pi_{1/2}(q^n; M, A) = same but restricted to P = A (mod M)
    # We exclude primes dividing M (ramified primes) from the residue-class sums
    # (they don't contribute to (F_q[T]/M)^*). The full pi_{1/2,K} normally
    # includes them, BUT AK's theorem in cyclotomic setting tracks all primes;
    # the residue-class one only sums unramified P. The difference is a finite
    # bounded constant absorbed in c. We will report results with the
    # standard convention: pi_{1/2,K} sums all P, pi_{1/2}(...; M, A) sums P with
    # gcd(P, M) = 1 and P = A (mod M). This is exactly AK's setup.

    pi_K_partial = [0.0] * (N + 1)
    pi_class = {u: [0.0] * (N + 1) for u in units}

    for d in range(1, N + 1):
        w = 1.0 / (2.0 ** (d / 2.0))
        d_count_all = 0
        d_count_unit = 0
        for P in irr_by_deg[d]:
            d_count_all += 1
            pi_K_partial[d] += w
            # P mod M; if P | M then it's not coprime, skip from class sum
            r = f2_mod(P, M)
            if r in pi_class:
                pi_class[r][d] += w
                d_count_unit += 1
        # cumulate
        pi_K_partial[d] += pi_K_partial[d - 1]
        for u in units:
            pi_class[u][d] += pi_class[u][d - 1]

    results = {
        "q": 2, "M_packed": M, "Phi": Phi, "N": N,
        "units": [int(u) for u in units],
        "squares": [int(s) for s in squares],
        "pi_K": pi_K_partial,
        "pi_class": {int(u): pi_class[u] for u in units},
    }
    return results


def run_fq(M, N, q, label):
    print(f"=== {label}: q={q}, M={M}, N={N} ===", flush=True)
    units = fq_units_mod_M(M, q)
    Phi = len(units)
    squares = fq_squares_mod_M(M, q)
    print(f"Phi(M) = {Phi}, |units|={len(units)}, |squares|={len(squares)}", flush=True)
    print(f"squares = {sorted(squares)}", flush=True)
    print(f"units   = {sorted(units)}", flush=True)

    print(f"Sieving irreducibles up to degree {N}...", flush=True)
    t0 = time.time()
    irr_by_deg = fq_sieve_irreducibles_by_degree(N, q)
    print(f"Sieve done in {time.time()-t0:.1f}s", flush=True)

    pi_K_partial = [0.0] * (N + 1)
    pi_class = {u: [0.0] * (N + 1) for u in units}

    for d in range(1, N + 1):
        w = 1.0 / (q ** (d / 2.0))
        for P in irr_by_deg[d]:
            pi_K_partial[d] += w
            r = fq_mod(P, M, q)
            if r in pi_class:
                pi_class[r][d] += w
        pi_K_partial[d] += pi_K_partial[d - 1]
        for u in units:
            pi_class[u][d] += pi_class[u][d - 1]

    results = {
        "q": q, "M": list(M), "Phi": Phi, "N": N,
        "units": [list(u) for u in units],
        "squares": [list(s) for s in squares],
        "pi_K": pi_K_partial,
        "pi_class": {str(u): pi_class[u] for u in units},
    }
    return results


def analyze_f2(res, label):
    Phi = res["Phi"]
    pi_K = res["pi_K"]
    units = [int(u) for u in res["units"]]
    sqs = set(res["squares"])
    N = res["N"]
    print(f"\n--- Analysis: {label} ---")
    print(f"Phi={Phi}, units={units}, squares mod M = {sorted(sqs)}")
    # t = dim F_2 G/G^2
    # G has order Phi; squares group order |G^2|. |G/G^2| = Phi / |G^2|.
    t = round(math.log2(Phi / len(sqs)))
    print(f"|G/G^2| = {Phi // len(sqs)} ; t = log_2 = {t}")
    QR_coef = (2 ** t - 1) / 2.0
    NR_coef = -1 / 2.0
    print(f"Predicted log-n coefficients (assuming m(sigma_A)=0):")
    print(f"   QR (A in G^2): (2^t - 1)/2 = {QR_coef}")
    print(f"   non-QR (A not in G^2): -1/2 = {NR_coef}")
    # Print table of LHS_n(A)
    header = ["n"] + [f"LHS(A={u})" for u in units] + ["log n"]
    print("\n" + "  ".join(f"{h:>12}" for h in header))
    rows = []
    for n in range(1, N + 1):
        row = [n]
        for u in units:
            lhs = pi_K[n] - Phi * res["pi_class"][u][n]
            row.append(lhs)
        row.append(math.log(n) if n > 0 else float("nan"))
        rows.append(row)
        print("  ".join(f"{x:12.6f}" if isinstance(x, float) else f"{x:>12d}" for x in row))

    # Fit LHS(A) = C * log n + c by least squares on n in [n_min, N]
    n_min_fit = max(5, N // 3)
    xs = [math.log(n) for n in range(n_min_fit, N + 1)]
    print(f"\nLeast-squares fit C, c for LHS = C*log n + c on n in [{n_min_fit},{N}]:")
    fits = {}
    for u in units:
        ys = [pi_K[n] - Phi * res["pi_class"][u][n] for n in range(n_min_fit, N + 1)]
        # least squares
        n_pts = len(xs)
        sx = sum(xs); sy = sum(ys); sxx = sum(x*x for x in xs); sxy = sum(x*y for x,y in zip(xs,ys))
        denom = n_pts * sxx - sx * sx
        C = (n_pts * sxy - sx * sy) / denom
        c = (sy - C * sx) / n_pts
        # residual
        resid = math.sqrt(sum((y - C*x - c)**2 for x,y in zip(xs,ys)) / n_pts)
        fits[u] = (C, c, resid)
        kind = "QR" if u in sqs else "non-QR"
        pred = QR_coef if u in sqs else NR_coef
        print(f"  A={u} ({kind}): C={C:.6f} (pred {pred:+.4f}, diff {C-pred:+.4f}), c={c:.4f}, resid={resid:.4f}")
    return fits


def analyze_fq(res, label, q):
    Phi = res["Phi"]
    pi_K = res["pi_K"]
    units = [tuple(u) for u in res["units"]]
    sqs = set(tuple(s) for s in res["squares"])
    N = res["N"]
    print(f"\n--- Analysis: {label} ---")
    print(f"Phi={Phi}, |squares mod M| = {len(sqs)}")
    t = round(math.log2(Phi / len(sqs)))
    print(f"|G/G^2| = {Phi // len(sqs)} ; t = log_2 = {t}")
    QR_coef = (2 ** t - 1) / 2.0
    NR_coef = -1 / 2.0
    print(f"Predicted log-n coefficients (assuming m(sigma_A)=0):")
    print(f"   QR (A in G^2): (2^t - 1)/2 = {QR_coef}")
    print(f"   non-QR (A not in G^2): -1/2 = {NR_coef}")

    print(f"\n{'n':>3} {'pi_K':>10} " + " ".join(f"LHS{u}".rjust(14) for u in units[:6]) + (" ..." if len(units) > 6 else ""))
    for n in range(1, N + 1):
        line = f"{n:>3} {pi_K[n]:>10.5f} "
        for u in units[:6]:
            lhs = pi_K[n] - Phi * res["pi_class"][str(u)][n]
            line += f"{lhs:>14.6f} "
        print(line)

    n_min_fit = max(4, N // 3)
    xs = [math.log(n) for n in range(n_min_fit, N + 1)]
    print(f"\nLeast-squares fit C, c for LHS = C*log n + c on n in [{n_min_fit},{N}]:")
    fits = {}
    for u in units:
        ys = [pi_K[n] - Phi * res["pi_class"][str(u)][n] for n in range(n_min_fit, N + 1)]
        n_pts = len(xs)
        sx = sum(xs); sy = sum(ys); sxx = sum(x*x for x in xs); sxy = sum(x*y for x,y in zip(xs,ys))
        denom = n_pts * sxx - sx * sx
        C = (n_pts * sxy - sx * sy) / denom
        c = (sy - C * sx) / n_pts
        resid = math.sqrt(sum((y - C*x - c)**2 for x,y in zip(xs,ys)) / n_pts)
        fits[u] = (C, c, resid)
        kind = "QR" if u in sqs else "non-QR"
        pred = QR_coef if u in sqs else NR_coef
        print(f"  A={u} ({kind}): C={C:+.6f} (pred {pred:+.4f}, diff {C-pred:+.4f}), c={c:+.4f}, resid={resid:.4f}")
    return fits


def log_density_pairwise(res, n_min=2, store=True):
    """Function-field analog of Rubinstein-Sarnak density.

    For each pair (b, a) of units with b non-QR and a QR (assuming m(sigma)=0),
    AK predicts pi_{1/2}(q^n; M, b) - pi_{1/2}(q^n; M, a) > 0 eventually.

    Define delta(b, a) := #{n in [n_min, N] : pi_{1/2}(q^n;M,b) > pi_{1/2}(q^n;M,a)}
                        / (N - n_min + 1).

    This is the function-field log-density analog (sum over n of indicator,
    weighted uniformly; cf. R-S who weight by 1/log T for log-density).
    """
    pass


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"

    if cmd in ("all", "ex36"):
        # Example 3.6: q=2, M = T^2 = 0b100 = 4
        res = run_f2(4, 22, "Example 3.6 (q=2, M=T^2)")
        fits = analyze_f2(res, "Example 3.6")
        with open("/tmp/ak_d2/out_ex36.json", "w") as f:
            json.dump(res, f)

    if cmd in ("all", "t1_T3"):
        # q=2, M = T^3 = 0b1000 = 8
        res = run_f2(8, 22, "q=2, M=T^3 (t=1)")
        fits = analyze_f2(res, "q=2, M=T^3")
        with open("/tmp/ak_d2/out_T3.json", "w") as f:
            json.dump(res, f)

    if cmd in ("all", "f3_split"):
        # q=3, M = T*(T+1)*(T+2) = T^3 - T = T*(T^2-1). t should be 3.
        # T*(T+1)*(T+2) over F_3: (T)*(T+1) = T^2+T; (T^2+T)*(T+2) = T^3+2T^2+T^2+2T = T^3+3T^2+2T = T^3+2T.
        # Wait: (T^2+T)(T+2) = T^3 + 2T^2 + T^2 + 2T = T^3 + 3T^2 + 2T = T^3 + 2T (mod 3).
        # So M = (0, 2, 0, 1) (i.e., 2T + T^3).
        M = (0, 2, 0, 1)
        res = run_fq(M, 14, 3, "q=3, M=T(T+1)(T+2) (t=3)")
        fits = analyze_fq(res, "q=3, M=T(T+1)(T+2)", 3)
        with open("/tmp/ak_d2/out_f3_split.json", "w") as f:
            json.dump(res, f)

    if cmd in ("all", "f3_t2"):
        # q=3, M = T^2 - 1 = (T-1)(T+1) = (T+2)(T+1). t=2.
        # M = T^2 + 2 = (2, 0, 1).
        M = (2, 0, 1)
        res = run_fq(M, 14, 3, "q=3, M=T^2-1 (t=2)")
        fits = analyze_fq(res, "q=3, M=T^2-1", 3)
        with open("/tmp/ak_d2/out_f3_t2.json", "w") as f:
            json.dump(res, f)
