"""
D1: Push N·W(N) precision to test candidate identifications for C.

Candidates (from MiMo B2 brainstorm):
  - Laplace limit L = 0.6627434193491815...
    (root of x*exp(sqrt(1+x²))/(1+sqrt(1+x²)) = 1; arises in Kepler's equation)
  - Twin-prime constant Π_2 / 2 = 0.6601618158...
  - 2/π · something
  - ζ(2)·something

Approach: Mikolás formula J(Q) = (1/(2π²)) Σ A_Q(m)² / m² with very large m_max,
extrapolate as Q → ∞.

Method: For each Q, compute J(Q) with m_max = 50·Q. Compute N·W(N) = N·J(N)/Φ(N).
Plot vs N (log-log) to extrapolate asymptote.
"""

import math
import sys

sys.path.insert(0, "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/code")
from J_mikolas import J_mikolas


def main():
    # Run at several Q with large m_factor for asymptote estimation
    cases = []
    for Q, m_factor in [
        (1_000, 50.0),
        (2_000, 50.0),
        (5_000, 30.0),
        (10_000, 30.0),
        (20_000, 20.0),
        (50_000, 15.0),
        (100_000, 10.0),
    ]:
        res = J_mikolas(Q, m_factor=m_factor)
        cases.append(res)
        print(f"Q={Q:>7}  m_max={res['m_max']:>9}  J={res['J']:>14.6f}  NW={res['NW']:>10.7f}")

    print()
    print("Candidate constants vs Q-extrapolated NW:")
    candidates = {
        "Laplace limit": 0.6627434193491815,
        "Twin-prime / 2": 0.6601618158468696,
        "2 - 4/π": 2 - 4 / math.pi,         # = 0.7268
        "1 - 1/3 + 1/(π²)": 1 - 1/3 + 1/math.pi**2,  # = 0.7680
        "ζ(2)·6/π² · 1/something": None,
        "(π² - 6)/6": (math.pi ** 2 - 6) / 6,        # = 0.6449 — ζ(2) - 1
        "6/π² · (something close to π²/6)": 6/math.pi**2,
        "π²/(3·5) = π²/15": math.pi ** 2 / 15,        # = 0.658 ← VERY CLOSE
        "0.66": 0.66,
        "2/3": 2/3,
    }
    # Use the largest Q as our best estimate
    best_NW = cases[-1]["NW"]
    print(f"Best Q={cases[-1]['Q']}: N·W = {best_NW:.7f}")
    print()
    for name, val in candidates.items():
        if val is None: continue
        diff = best_NW - val
        print(f"  {name:>35s} = {val:.7f}  (diff {diff:+.6f})")


if __name__ == "__main__":
    main()
