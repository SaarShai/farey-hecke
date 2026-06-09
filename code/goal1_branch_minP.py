"""
goal1_branch_minP.py — per-branch min of the observable P over T^q, vs X(q).

Hypothesis: for q=3,4 every NON-last branch has min P > X(q) (extremes confined to
the last branch T_{q-1} where the map is the clean (b,-a+k*lam*b) form => cluster<=2).
For q>=5 some intermediate branch dips below X(q)=1/lam^3, so extremes are NOT
confined => size-3 clusters become possible.  This explains the q=4 vs q>=5 split.
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(11)


def hecke_w(q):
    lam = 2 * math.cos(math.pi / q)
    w = [(1.0, 0.0)]
    for _ in range(q + 1):
        x, y = w[-1]
        w.append((lam * x - y, x))
    return lam, w


def Xq(q):
    lam = 2 * math.cos(math.pi / q)
    if q == 3: return 2 / 9
    if q == 4: return math.sqrt(2) / 8
    return 1.0 / lam ** 3


def branch_of(a, b, w, q):
    sub = q - 1
    d_prev = w[1][0] * a + w[1][1] * b
    for i in range(2, q):
        di = w[i][0] * a + w[i][1] * b
        if d_prev > 1.0 and di <= 1.0:
            return i
        d_prev = di
    return sub


def scan(q, n=8_000_000):
    lam, w = hecke_w(q)
    X = Xq(q)
    minP = {i: math.inf for i in range(2, q)}
    extreme_in = {i: 0 for i in range(2, q)}
    for _ in range(n):
        a = rng.random()
        lo = 1 - lam * a
        b = lo + rng.random() * (1 - lo)
        if not (0 < a <= 1 and lo < b <= 1):
            continue
        i = branch_of(a, b, w, q)
        wi = w[i][0] * a + w[i][1] * b
        P = a * wi / w[i][1]
        if P < minP[i]:
            minP[i] = P
        if P < X:
            extreme_in[i] += 1
    return lam, X, minP, extreme_in


if __name__ == "__main__":
    for q in range(3, 9):
        lam, X, minP, ext = scan(q)
        print(f"\nq={q}  lam={lam:.5f}  X(q)={X:.6f}   (last branch = T_{q-1})")
        for i in range(2, q):
            tag = "LAST" if i == q - 1 else "intermediate"
            below = "  <-- DIPS BELOW X (extremes here!)" if minP[i] < X else ""
            print(f"   T_{i} ({tag:12s}): minP={minP[i]:.6f}  extreme_count={ext[i]:>8d}{below}")
