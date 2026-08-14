#!/usr/bin/env python3
"""Compute the Farey rank-sum C_W and the fast Franel/Mertens proxy.

The requested quantity uses the endpoint-inclusive Farey sequence

    0/1 = f_0 < ... < f_{n-1} = 1/1,
    n = 1 + sum_{q<=N} phi(q),
    W = sum_j (f_j - j/n)^2, C_W = N*W.

For direct checks we stream the exact next-Farey recurrence and accumulate
with numpy.longdouble.  The fast route evaluates the exact Jordan/Mertens
identity for the centered CDF L2 quantity J:

    12 J = sum_{e<=N} (J_2(e)/e^2) T(floor(N/e))^2 + 2 T(N) + 1,
    T(x) = sum_{k<=x} M(floor(x/k))/k.

For the inclusive endpoint convention J is the integral of
    (# {f_j <= x} - n*x)^2.
The fast normalized value N*J/Phi(N), Phi=sum phi, is asymptotic to the
requested N*W and is compared against the direct rank sum in the report.
The finite-N distinction is intentional and never silently merged.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent


def totient_sum_direct(nmax: int) -> int:
    """Return 1+sum(phi(q), q<=nmax), including the 0/1 endpoint."""
    phi = np.arange(nmax + 1, dtype=np.int64)
    for p in range(2, nmax + 1):
        if phi[p] == p:
            sl = phi[p::p]
            sl -= sl // p
    return int(phi[1:].sum(dtype=np.int64)) + 1


def direct_metrics(order: int) -> dict[str, float | int]:
    """Stream F_order and return both requested and alternative conventions."""
    n = totient_sum_direct(order)
    phi = n - 1
    a, b, c, d = 0, 1, 1, order
    j = 0
    sum_w = np.longdouble(0)
    sum_alt = np.longdouble(0)
    sum_j = np.longdouble(0)

    while True:
        x = np.longdouble(a) / np.longdouble(b)
        sum_w += (x - np.longdouble(j) / np.longdouble(n)) ** 2

        if a != 0 or b != 1:
            # Positive-only convention: (0,1] with rank 0,...,phi-1.
            pos_rank = j - 1
            sum_alt += (x - np.longdouble(pos_rank) / np.longdouble(phi)) ** 2

        if a == 1 and b == 1:
            break

        x_next = np.longdouble(c) / np.longdouble(d)
        # Inclusive endpoint CDF: count is j+1 on [x, x_next].
        count = np.longdouble(j + 1)
        left = count - np.longdouble(n) * x
        right = count - np.longdouble(n) * x_next
        sum_j += -((right**3) - (left**3)) / (3 * np.longdouble(n))

        k = (order + b) // d
        a, b, c, d = c, d, k * c - a, k * d - b
        j += 1

    expected_nodes = n
    if j + 1 != expected_nodes:
        raise AssertionError((order, j + 1, expected_nodes))

    return {
        "N": order,
        "n": n,
        "Phi": phi,
        "C_W_direct": float(np.longdouble(order) * sum_w),
        "C_alt_positive": float(np.longdouble(order) * sum_alt),
        "J_direct_inclusive": float(sum_j),
        "C_Mertens_proxy_from_direct_J": float(
            np.longdouble(order) * sum_j / np.longdouble(phi)
        ),
    }


def mobius_sieve(nmax: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (mu, M, primes) through nmax using a numpy sieve."""
    is_prime = np.ones(nmax + 1, dtype=bool)
    is_prime[:2] = False
    for p in range(2, math.isqrt(nmax) + 1):
        if is_prime[p]:
            is_prime[p * p :: p] = False
    primes = np.flatnonzero(is_prime)

    mu = np.ones(nmax + 1, dtype=np.int8)
    mu[0] = 0
    for p in primes:
        mu[p::p] *= -1
        p2 = int(p) * int(p)
        if p2 <= nmax:
            mu[p2::p2] = 0
    mertens = np.cumsum(mu, dtype=np.int32)
    return mu, mertens, primes


def phi_sum_from_mu(mu: np.ndarray, order: int) -> int:
    d = np.arange(1, order + 1, dtype=np.int64)
    q = order // d
    triangular = q * (q + 1) // 2
    return int(np.dot(mu[1 : order + 1].astype(np.int64), triangular))


def quotient_values(order: int) -> list[int]:
    """All distinct values of order//e, generated in O(sqrt(order))."""
    r = math.isqrt(order)
    values = set(range(1, r + 1))
    values.update(order // e for e in range(1, r + 1))
    return sorted(values)


def build_harmonics(nmax: int) -> np.ndarray:
    h = np.empty(nmax + 1, dtype=np.float64)
    h[0] = 0.0
    h[1:] = np.cumsum(1.0 / np.arange(1, nmax + 1, dtype=np.float64))
    return h


def T_value(x: int, mertens: np.ndarray, harmonics: np.ndarray) -> float:
    """T(x)=sum_{k<=x} M(floor(x/k))/k, grouped by quotient blocks."""
    total = 0.0
    left = 1
    while left <= x:
        q = x // left
        right = x // q
        total += float(mertens[q]) * (harmonics[right] - harmonics[left - 1])
        left = right + 1
    return total


def jordan_ratio_coefficients(nmax: int, primes: np.ndarray) -> np.ndarray:
    """c[e]=J_2(e)/e^2=product_{p|e}(1-p^-2)."""
    coeff = np.ones(nmax + 1, dtype=np.float64)
    coeff[0] = 0.0
    for p in primes:
        p = int(p)
        coeff[p::p] *= 1.0 - 1.0 / float(p * p)
    return coeff


def fast_proxy_values(orders: list[int], max_order: int) -> tuple[dict[int, dict], dict]:
    """Compute the Mertens/Jordan proxy for every requested order."""
    started = time.time()
    mu, mertens, primes = mobius_sieve(max_order)
    sieve_seconds = time.time() - started
    harmonics = build_harmonics(max_order)
    coeff = jordan_ratio_coefficients(max_order, primes)

    all_queries: set[int] = set()
    for order in orders:
        all_queries.update(quotient_values(order))

    t_cache: dict[int, float] = {}
    for x in sorted(all_queries):
        t_cache[x] = T_value(x, mertens, harmonics)

    results: dict[int, dict] = {}
    for order in orders:
        phi = phi_sum_from_mu(mu, order)
        t_order = t_cache[order]
        total = 0.0
        chunk = 1_000_000
        for first in range(1, order + 1, chunk):
            last = min(order + 1, first + chunk)
            e = np.arange(first, last, dtype=np.int64)
            q = order // e
            t = np.fromiter((t_cache[int(x)] for x in q), dtype=np.float64, count=len(q))
            total += float(np.dot(coeff[first:last], t * t))
        j_value = (total + 2.0 * t_order + 1.0) / 12.0
        results[order] = {
            "N": order,
            "Phi": phi,
            "n": phi + 1,
            "J_fast_inclusive": j_value,
            "C_fast_proxy": float(order * j_value / phi),
            "T_N": t_order,
            "Jordan_sum": total,
        }

    meta = {
        "max_order": max_order,
        "prime_count": int(len(primes)),
        "sieve_seconds": sieve_seconds,
        "query_count": len(all_queries),
        "elapsed_seconds": time.time() - started,
    }
    return results, meta


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=10_000_000)
    parser.add_argument(
        "--orders",
        type=int,
        nargs="+",
        default=[100, 1_000, 2_000, 10_000, 100_000, 300_000, 1_000_000, 3_000_000, 10_000_000],
    )
    parser.add_argument("--direct-max", type=int, default=2_000)
    args = parser.parse_args()

    orders = sorted(set(args.orders))
    if max(orders) > args.max_order:
        raise SystemExit("max order exceeds --max-order")

    direct: dict[int, dict] = {}
    for order in orders:
        if order <= args.direct_max:
            print(f"direct N={order}", flush=True)
            direct[order] = direct_metrics(order)

    print(f"fast route through N={args.max_order}", flush=True)
    fast, meta = fast_proxy_values(orders, args.max_order)

    rows = []
    for order in orders:
        row = {"N": order}
        row.update(fast.get(order, {}))
        if order in direct:
            row.update(direct[order])
            row["C_W"] = direct[order]["C_W_direct"]
            row["C_W_source"] = "direct_longdouble"
            row["C_fast_minus_direct"] = (
                fast[order]["C_fast_proxy"] - direct[order]["C_W_direct"]
            )
            row["J_fast_minus_direct"] = (
                fast[order]["J_fast_inclusive"] - direct[order]["J_direct_inclusive"]
            )
        else:
            row["C_W"] = fast[order]["C_fast_proxy"]
            row["C_W_source"] = "fast_Mertens_proxy"
            row["C_fast_minus_direct"] = None
            row["J_fast_minus_direct"] = None
        rows.append(row)

    csv_path = ROOT / "cw_growth_values.csv"
    fields = [
        "N", "C_W", "C_W_source", "C_W_direct", "C_alt_positive",
        "C_fast_proxy", "C_fast_minus_direct", "J_direct_inclusive",
        "J_fast_inclusive", "J_fast_minus_direct", "Phi", "n", "T_N", "Jordan_sum",
    ]
    with csv_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fields})

    receipt = {
        "script": str(Path(__file__).relative_to(Path.cwd())) if Path.cwd() in Path(__file__).parents else str(Path(__file__)),
        "endpoint_convention": "inclusive F_N: 0/1=f_0<...<f_{n-1}=1/1; n=1+sum_{q<=N} phi(q)",
        "requested_definition": "W=sum_j(f_j-j/n)^2; C_W=N*W",
        "fast_identity": "12J=sum_{e<=N}(J2(e)/e^2)T(floor(N/e))^2+2T(N)+1",
        "fast_normalization": "C_fast_proxy=N*J/Phi(N), Phi=sum_{q<=N}phi(q)",
        "direct_max_reached": max((x for x in orders if x <= args.direct_max), default=None),
        "fast_max_reached": max(orders),
        "orders": orders,
        "meta": meta,
        "rows": rows,
    }
    (ROOT / "cw_growth_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(meta, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
