"""
goal1_q6_certs.py — verify the ACTUAL inequalities a q=6 proof needs, on dense
samples of the feasible regions (not orbit), with margins. lam=sqrt3, X=sqrt3/9.

Branches (d_i=w_i.(a,b)):  d1=sqrt3 a+b, d2=2a+sqrt3 b, d3=sqrt3 a+2b, d4=a+sqrt3 b, d5=b.
T_i = {d_{i-1}>1, d_i<=1}; T5 last. domain = T^6 = {0<a<=1, 1-sqrt3 a<b<=1} = {d1>1,b<=1}.
P on T_i = a*d_i/y_i; y2=sqrt3,y3=2,y4=sqrt3,y5=1.

(1) intermediate non-extreme: P_{Ti}>=X for i=2,3,4. report min margin + candidate certs.
(2) T5 cluster: x_i=(a,b),x_{i+1}=(b,c) both T5 & extreme (ab<X,bc<X), a+c=k*sqrt3*b.
    third x_{i+2}=(c,d), d=-b+l*sqrt3*c. If (c,d) in T5: need cd>=X. report min margin,
    and the (c,l) structure of that subcase.
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(66)
L = math.sqrt(3.0)
X = L / 9.0          # 1/lam^3 = sqrt3/9
W = [(1.0, 0.0)]
for _ in range(6):
    x, y = W[-1]; W.append((L*x - y, x))
def d(i, a, b): return W[i][0]*a + W[i][1]*b
def branch(a, b):
    for i in range(2, 6):
        if d(i-1, a, b) > 1.0 and d(i, a, b) <= 1.0:
            return i
    return 5

# ---------- (1) intermediate branches on dense samples ----------
def intermediate(n=30_000_000):
    res = {2: [1e9, None], 3: [1e9, None], 4: [1e9, None]}
    # certificate candidates (should be >=0 on T_i): margin of P - X
    for _ in range(n):
        a = rng.random()
        lo = 1 - L*a
        b = lo + rng.random()*(1-lo)
        if not (0 < a <= 1 and lo < b <= 1):
            continue
        i = branch(a, b)
        if i in (2, 3, 4):
            P = a*d(i, a, b)/W[i][1]
            if P - X < res[i][0]:
                res[i][0] = P - X; res[i][1] = (a, b)
    return res

# ---------- (2) T5 cluster chain (feasible enumeration) ----------
def t5_cluster(n=60_000_000):
    a = rng.random(size=n)
    b = (1 - L*a) + rng.random(size=n)*(1-(1-L*a))
    dom = (a > 0) & (a <= 1) & (1 - L*a < b) & (b <= 1)
    inT5_i = (a + L*b > 1)               # T5: d4>1
    ab = a*b
    m = dom & inT5_i & (ab < X)
    a, b = a[m], b[m]
    k = np.floor((1 + a)/(L*b))
    c = -a + k*L*b
    # x_{i+1}=(b,c) in T5 & extreme
    inT4dom = (1 - L*b < c) & (c <= 1)   # domain of (b,c)
    inT5_1 = (b + L*c > 1)               # T5 cond
    bc = b*c
    cl = inT4dom & inT5_1 & (bc < X)
    a, b, c, k = a[cl], b[cl], c[cl], k[cl]
    out = dict(n=int(cl.sum()),
               kb2_max=float((k*b*b).max()) if cl.sum() else None,
               k_min=float(k.min()) if cl.sum() else None,
               b_max=float(b.max()) if cl.sum() else None,
               c_min=float(c.min()) if cl.sum() else None)
    if cl.sum() == 0:
        return out
    l = np.floor((1 + b)/(L*c))
    dd = -b + l*L*c
    inT5_2 = (c + L*dd > 1)               # third point in T5 ?
    cd = c*dd
    # third in T5: must have cd>=X (non-extreme)
    out["third_T5_count"] = int(inT5_2.sum())
    out["third_nonT5_count"] = int((~inT5_2).sum())
    if inT5_2.any():
        out["min_cd_minus_X_T5"] = float((cd[inT5_2] - X).min())
        out["c_range_when_T5"] = (float(c[inT5_2].min()), float(c[inT5_2].max()))
        out["l_when_T5"] = {int(v): int((l[inT5_2] == v).sum()) for v in np.unique(l[inT5_2])}
        # also: among third-in-T5, is cd<X EVER (would be a 3rd extreme = cluster>=3)?
        out["third_extreme_in_T5"] = int((cd[inT5_2] < X).sum())
    return out


if __name__ == "__main__":
    print(f"q=6  X=sqrt3/9={X:.8f}  1/3={1/3:.6f}")
    print("\n(1) intermediate non-extreme  min(P-X) over dense T_i samples (must be >=0):")
    r = intermediate()
    for i in (2, 3, 4):
        print(f"   T_{i}: min(P-X)={r[i][0]:+.6f} at (a,b)={tuple(round(v,5) for v in r[i][1])}")
    print("   (T_4 tight: P=a(a+sqrt3 b)/sqrt3 >= X  <=>  a(a+sqrt3 b) >= 1/3)")

    print("\n(2) T5 double-extreme cluster chain:")
    t = t5_cluster()
    for k_, v in t.items():
        print(f"   {k_} = {v}")
    if t.get("third_extreme_in_T5", 0) == 0 and t.get("min_cd_minus_X_T5", -1) >= 0:
        print("   => 3rd point in T5 is ALWAYS non-extreme (cd>=X). cluster<=2 closes.")
