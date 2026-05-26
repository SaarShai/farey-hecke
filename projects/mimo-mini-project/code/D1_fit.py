"""
D1 asymptotic fit. Take all direct N·W(N) data and fit several models;
report best C.
"""
import math, json
from pathlib import Path

# All direct measurements we have
data = [
    # (Q, NW)
    (5000,   0.65482),
    (10000,  0.66775),
    (20000,  0.66575),
    (30000,  0.66374),
    # 50000, 100000 to be added once available
]

# Also load Q=30k/50k/100k from D1_direct_highQ.json if present
hQ_path = "/Users/za/Documents/Farey NOW/projects/mimo-mini-project/phase3_synthesis/D1_direct_highQ.json"
if Path(hQ_path).exists():
    import json as _j
    with open(hQ_path) as f:
        hQ = _j.load(f)
    existing_Qs = {q for q, _ in data}
    for r in hQ:
        if r["Q"] not in existing_Qs:
            data.append((r["Q"], float(r["NW"])))


# Models to fit (skip Q=5000 which is anomalous)
clean = [(q, nw) for q, nw in data if q >= 10000]


def fit_linear(xs, ys):
    """y = A + B x by least squares; return (A, B)."""
    n = len(xs)
    sx = sum(xs); sy = sum(ys); sxx = sum(x*x for x in xs); sxy = sum(x*y for x, y in zip(xs, ys))
    den = n * sxx - sx * sx
    B = (n * sxy - sx * sy) / den
    A = (sy - B * sx) / n
    return A, B


print("All data (clean = exclude Q=5000):")
for q, nw in data:
    flag = " [used]" if q >= 10000 else ""
    print(f"  Q={q:>6} NW={nw:.6f}{flag}")

print()
candidates = {
    "C = π²/15":      math.pi ** 2 / 15,
    "C = Laplace lim": 0.6627434193491815,
    "C = 2/3":        2 / 3,
    "C = twin-prime/2": 0.6601618158468696,
    "C = 6/π² · (5/3·6/π²)": 6/math.pi**2 * 6/math.pi**2 * 5/3,
}

print("\n=== Model: N·W(Q) = C + A/√Q ===")
xs = [1/math.sqrt(q) for q, _ in clean]
ys = [nw for _, nw in clean]
C, A = fit_linear(xs, ys)
print(f"  C = {C:.6f}, A = {A:.4f}")
print(f"  Predicted vs measured:")
for q, nw_meas in clean:
    nw_pred = C + A / math.sqrt(q)
    print(f"    Q={q:>6}: predicted {nw_pred:.6f}, measured {nw_meas:.6f}, diff {nw_meas - nw_pred:+.6f}")
print(f"  Compare C to candidates:")
for name, val in candidates.items():
    print(f"    {name:>30s} = {val:.6f}, diff from fit C = {C - val:+.6f}")

print("\n=== Model: N·W(Q) = C + A/log(Q) + B/log(Q)² ===")
if len(clean) >= 3:
    # Quadratic fit in 1/log Q
    xs = [1/math.log(q) for q, _ in clean]
    n = len(xs)
    sx1 = sum(xs); sx2 = sum(x*x for x in xs); sx3 = sum(x**3 for x in xs); sx4 = sum(x**4 for x in xs)
    sy = sum(ys); sxy = sum(x*y for x, y in zip(xs, ys)); sx2y = sum(x*x*y for x, y in zip(xs, ys))
    # Solve [[n, sx1, sx2], [sx1, sx2, sx3], [sx2, sx3, sx4]] @ [C, A, B] = [sy, sxy, sx2y]
    import numpy as np
    M = np.array([[n, sx1, sx2], [sx1, sx2, sx3], [sx2, sx3, sx4]])
    v = np.array([sy, sxy, sx2y])
    try:
        sol = np.linalg.solve(M, v)
        C, A, B = sol
        print(f"  C = {C:.6f}, A = {A:.4f}, B = {B:.4f}")
        for name, val in candidates.items():
            print(f"    {name:>30s} = {val:.6f}, diff from fit C = {C - val:+.6f}")
    except np.linalg.LinAlgError as e:
        print(f"  linear algebra error: {e}")

print("\n=== Predictions for not-yet-measured Q ===")
for q_pred in [50000, 100000, 200000, 1_000_000, 10_000_000]:
    pred_sqrt = candidates["C = π²/15"] + 0.97 / math.sqrt(q_pred)
    pred_lapl = candidates["C = Laplace lim"]
    print(f"  Q={q_pred:>9}: 1/√Q model predicts {pred_sqrt:.6f}; if C=Laplace, would converge to {pred_lapl:.6f}")
