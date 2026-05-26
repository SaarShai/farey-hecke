"""
Memory-efficient streaming J(Q) computation.

The Farey sequence F_Q can be generated one fraction at a time via Stern-Brocot
recurrence. We process each interval [x_j, x_{j+1}] as it appears, accumulating
J(Q) = ∫ E_Q² without ever holding the full sequence.

For each new fraction x_{j+1} (with j = count of fractions ≤ x_{j+1} including itself,
in the convention used by verify_bcz_cocycle.J_direct_fast):
   contribution = -((j - Φ·x_{j+1})^3 - (j - Φ·x_j)^3) / (3·Φ)

But we don't know Φ = |F_Q| upfront! Stern-Brocot gives us the count as we go.

WORKAROUND: do two passes.
  Pass 1: Count |F_Q| (Φ).
  Pass 2: Stream the fractions, accumulate J(Q).

Each pass is O(|F_Q|) time, O(1) memory.

For Q=100k, |F_Q| ≈ 3·10^9; each pass at ~10M fractions/sec is ~5 min. Total ~10min.

Stern-Brocot recurrence (matches verify_bcz_cocycle.farey()):
  a, b, c, d = 0, 1, 1, Q
  yield (a, b)  # 0/1
  while c <= Q:
      k = (Q + b) // d
      a, b, c, d = c, d, k*c - a, k*d - b
      yield (a, b)
"""

import time
import argparse
import json
from pathlib import Path


def count_farey(Q):
    """Count |F_Q| = 1 + Σ_{q≤Q} φ(q) by streaming Stern-Brocot."""
    a, b, c, d = 0, 1, 1, Q
    n = 1
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        n += 1
    return n


def J_stream(Q):
    """Streaming J(Q). Two passes. Returns J(Q) as float."""
    # Pass 1: count
    Phi = float(count_farey(Q))
    inv3Phi = 1.0 / (3.0 * Phi)

    # Pass 2: integrate
    # State: prev_fraction = x_j (numerator a, denominator b)
    a, b, c, d = 0, 1, 1, Q
    j_count = 1  # number of fractions <= x_j (just x_0 = 0/1)
    prev_v = (j_count - Phi * (a / b)) ** 3  # at x_j = 0/1
    J_sum = 0.0
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        # new fraction is x_{j+1} = a/b
        x_new = a / b
        # For interval [x_j, x_{j+1}], count = j_count (j_count fractions are <= x_j).
        # E_Q(x) = j_count - Φ·x on this interval.
        # ∫_{x_j}^{x_{j+1}} (j_count - Φ·x)^2 dx
        # = -[(j_count - Φ·x)^3 / (3Φ)]_{x_j}^{x_{j+1}}
        # = (prev_v - new_v) / (3Φ)  where prev_v = (j_count - Φ·x_j)^3, new_v = (j_count - Φ·x_{j+1})^3
        new_v_low = (j_count - Phi * x_new) ** 3   # j_count is still j_count, x = x_{j+1}
        J_sum += (prev_v - new_v_low) * inv3Phi
        j_count += 1
        # For the next interval [x_{j+1}, x_{j+2}], the count becomes j_count+1.
        # But we're done with interval [x_j, x_{j+1}].
        prev_v = (j_count - Phi * x_new) ** 3   # E(x_{j+1}+) starts at j_count - Φ·x_{j+1}
    return J_sum, int(Phi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--Q", type=int, action="append", required=True, help="Q value (can be repeated)")
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    results = []
    for Q in args.Q:
        t0 = time.time()
        J, Phi = J_stream(Q)
        wall = time.time() - t0
        NW = Q * J / Phi
        results.append({"Q": Q, "Phi": Phi, "J": J, "NW": NW, "wall_s": wall})
        print(f"Q={Q:>7} Phi={Phi:>13} J={J:>14.6f} NW={NW:>11.8f} wall={wall:.1f}s", flush=True)

    if args.out:
        with open(args.out, "w") as f:
            json.dump(results, f, indent=2)
        print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
