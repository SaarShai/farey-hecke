#!/usr/bin/env python3
"""Quantify super-linear cost growth on the uncapped compute endpoints.

Uses small, returning inputs so we can measure wall-clock and show the growth
curve that makes a slightly larger (still tiny) request a denial of service.
"""

from __future__ import annotations

import http.client
import json
import time

HOST, PORT = "127.0.0.1", 8765


def timed_post(path: str, payload: dict, timeout: float = 60.0) -> tuple[int | None, float]:
    conn = http.client.HTTPConnection(HOST, PORT, timeout=timeout)
    t0 = time.perf_counter()
    try:
        conn.request("POST", path, body=json.dumps(payload).encode(),
                     headers={"Content-Type": "application/json"})
        resp = conn.getresponse()
        resp.read()
        return resp.status, time.perf_counter() - t0
    finally:
        conn.close()


def sweep(name: str, path: str, sizes: list[int], build) -> None:
    print(f"\n== {name} ({path}) ==")
    prev_t = None
    for size in sizes:
        status, dt = timed_post(path, build(size))
        ratio = f"x{dt / prev_t:.1f}" if prev_t else "-"
        print(f"  n={size:<10} status={status} t={dt:.4f}s  {ratio}")
        prev_t = dt


def main() -> None:
    sweep("gaps farey_order (~0.30*order^2 fractions)", "/api/gaps",
          [200, 400, 800, 1600],
          lambda n: {"farey_order": n})
    sweep("shift p (O(p^2) exact Fraction loop)", "/api/shift",
          [251, 503, 1009, 2003],
          lambda n: {"p": n, "max_order": 6})
    sweep("optimize samples (uncapped baseline loop)", "/api/optimize",
          [10000, 40000, 160000],
          lambda n: {"candidates": [2, 3, 5, 7, 11], "layers": 3, "samples": n})
    sweep("certificate single prime (O(sqrt n) trial division)", "/api/certificate",
          [10**10 + 19, 10**12 + 39, 10**14 + 31],
          lambda n: {"denominators": [n]})
    print("\nAll four endpoints accept unbounded n; cost grows super-linearly "
          "while /api/balance is the only route with admission caps.")


if __name__ == "__main__":
    main()
