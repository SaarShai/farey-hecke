"""
goal1_q6_mechanism.py — pin the q=6 (lambda=sqrt3) cluster<=2 mechanism before
formalizing cluster_size_le_two_q6.  X(6)=1/lam^3=sqrt3/9.

q=6 vectors (lam=sqrt3): w1=(sqrt3,1) w2=(2,sqrt3) w3=(sqrt3,2) w4=(1,sqrt3) w5=(0,1).
Branches T_i={d_{i-1}>1, d_i<=1}, d_i=w_i.(a,b), i=2..5; T5 last.
Observable P = a*d_i / y_i (y_i = w_i[1]); on T5 (w5=(0,1)) P=a*b.
Last-branch map: (a,b)->(b, -a+k*lam*b), k=floor((1+a)/(lam*b)).

Checks:
 (A) intermediate branches T2,T3,T4 are non-extreme (P>X), AND whether the
     (1-a)(1-d_i)>=0 lower bound  P>=(a+d_i-1)/y_i  already exceeds X (tells us if
     that clean trick suffices per branch for the Lean proof).
 (B) clusters live in T5; tabulate k (1st step), ell (2nd step), b/c ranges,
     and the 3rd-point outcome.  Confirm max-run = 2 and (if possible) min k.
"""
from __future__ import annotations
import math
import numpy as np

rng = np.random.default_rng(6)
LAM = math.sqrt(3.0)
X = 1.0 / LAM**3            # = sqrt3/9
# vectors w0..w6
W = [(1.0, 0.0)]
for _ in range(6):
    x, y = W[-1]
    W.append((LAM*x - y, x))
# W[2]=(2,sqrt3) W[3]=(sqrt3,2) W[4]=(1,sqrt3) W[5]=(0,1)


def dot(i, a, b):
    return W[i][0]*a + W[i][1]*b


def branch(a, b):
    for i in range(2, 6):
        if dot(i-1, a, b) > 1.0 and dot(i, a, b) <= 1.0:
            return i
    return 5


def P_obs(a, b):
    i = branch(a, b)
    return a * dot(i, a, b) / W[i][1]


def step(a, b):
    i = branch(a, b)
    if i == 5:                       # last branch: (b, -a + k*lam*b)
        k = math.floor((1.0 + a) / (LAM * b))
        return b, -a + k*LAM*b, 5, k
    di = dot(i, a, b); di1 = dot(i+1, a, b)
    k = math.floor((1.0 - di1) / (LAM * di))
    return di, di1 + k*LAM*di, i, k


def in_dom(a, b, tol=1e-9):
    return (0 < a <= 1+tol) and (1 - LAM*a - tol < b <= 1+tol)


# ---- (A) intermediate-branch lower bounds ----
def check_intermediate(n=12_000_000):
    minP = {2: 9., 3: 9., 4: 9.}
    minBound = {2: 9., 3: 9., 4: 9.}   # (a+d_i-1)/y_i
    cnt = {2: 0, 3: 0, 4: 0}
    for _ in range(n):
        a = rng.random()
        lo = 1 - LAM*a
        b = lo + rng.random()*(1-lo)
        if not in_dom(a, b):
            continue
        i = branch(a, b)
        if i in (2, 3, 4):
            di = dot(i, a, b); yi = W[i][1]
            P = a*di/yi
            bound = (a + di - 1)/yi
            cnt[i] += 1
            minP[i] = min(minP[i], P)
            minBound[i] = min(minBound[i], bound)
    return minP, minBound, cnt


# ---- (B) cluster structure ----
def clusters(n_steps=3_000_000, n_starts=20, burn=400):
    recs = []
    max_run = 0
    extreme_nonlast = 0
    for _ in range(n_starts):
        while True:
            a = rng.random(); b = rng.random()
            if in_dom(a, b):
                break
        for _ in range(burn):
            a, b, _, _ = step(a, b)
        buf = []
        for _ in range(n_steps):
            i = branch(a, b); P = P_obs(a, b)
            an, bn, ii, k = step(a, b)
            buf.append((a, b, i, P, k))
            if P < X and i != 5:
                extreme_nonlast += 1
            a, b = an, bn
        j = 0; nn = len(buf)
        while j < nn:
            if buf[j][3] < X:
                s = j
                while j < nn and buf[j][3] < X:
                    j += 1
                max_run = max(max_run, j - s)
                if j - s == 2 and j < nn:
                    recs.append((buf[s], buf[s+1], buf[j]))
            else:
                j += 1
    return recs, max_run, extreme_nonlast


if __name__ == "__main__":
    print(f"q=6 lam=sqrt3={LAM:.6f}  X=1/lam^3=sqrt3/9={X:.6f}")
    print(f"W2={tuple(round(v,4) for v in W[2])} W3={tuple(round(v,4) for v in W[3])} "
          f"W4={tuple(round(v,4) for v in W[4])} W5={tuple(round(v,4) for v in W[5])}")

    print("\n[A] intermediate branches (P>X ? and does (a+d_i-1)/y_i bound exceed X ?)")
    minP, minBound, cnt = check_intermediate()
    for i in (2, 3, 4):
        print(f"  T_{i}: n={cnt[i]:>8d}  minP={minP[i]:.6f}  min[(a+d-1)/y]={minBound[i]:.6f}  "
              f"P>X:{minP[i]>X}  bound>X:{minBound[i]>X}")

    print("\n[B] cluster structure")
    recs, max_run, ext_nl = clusters()
    print(f"  max_run={max_run}   extreme-but-not-last-branch count={ext_nl}   #size2={len(recs)}")
    from collections import Counter
    kc = Counter(); ellc = Counter(); pat = Counter(); tb = Counter()
    bs = []; cs = []
    for (p0, p1, p2) in recs:
        a0,b0,i0,P0,k0 = p0; a1,b1,i1,P1,k1 = p1; a2,b2,i2,P2,k2 = p2
        pat[(i0,i1)] += 1; tb[i2] += 1; kc[k0] += 1; ellc[k1] += 1
        bs.append(b0); cs.append(b1)
    bs = np.array(bs); cs = np.array(cs)
    print(f"  branch pattern (x_i,x_i+1): {dict(pat)}")
    print(f"  3rd-point branch: {dict(tb)}")
    print(f"  k(1st step) min={min(kc) if kc else None} dist(head)={dict(sorted(kc.items())[:6])}")
    print(f"  ell(2nd step) dist={dict(sorted(ellc.items()))}")
    print(f"  shared b: min={bs.min():.5f} max={bs.max():.5f}   "
          f"sqrt(2/9)={math.sqrt(2/9):.5f} 1/lam={1/LAM:.5f} lam/4-ish")
    print(f"  large c: min={cs.min():.5f} max={cs.max():.5f}   (need c>1/2 for 3rd>=X?)")
    # candidate b-threshold: kb^2<2/9 (from ab+bc<2X=2sqrt3/9 => k*sqrt3*b^2<2sqrt3/9)
    print(f"  check k*b^2<2/9 over clusters: max={max((k0*b0*b0) for (p0,_,_) in recs for (a0,b0,i0,P0,k0) in [p0]):.5f} (=2/9={2/9:.5f})")
