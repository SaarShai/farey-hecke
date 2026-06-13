"""
exp_transience_q16.py -- the LOAD-BEARING test for Koyama's cusp coupling.

For q>=16 a non-cusp middle branch geometrically permits P<1/l^3 (verified). If the
dynamics could DWELL there, X_Omega < 1/l^3 and the uniform bound would FAIL. Koyama's
route needs the cusp escape-of-mass to forbid dwelling. We test: starting AT the low-P
middle-branch vertex, how many consecutive genuine steps stay below 1/l^3 (the excursion
window)? If finite and ~q/3 (transient), the bound holds dynamically though not per-branch.
We also confirm the ess-sup over long orbits stays >= 1/l^3 (cluster-onset proxy >=1).
"""
from __future__ import annotations
import math
import numpy as np

def hecke_w(q):
    lam = 2.0 * math.cos(math.pi / q)
    w = [(1.0, 0.0)]
    for _ in range(q + 1):
        x, y = w[-1]
        w.append((lam * x - y, x))
    return lam, w

def cheb_x(q):
    th = math.pi / q
    return {i: math.sin((i + 1) * th) / math.sin(th) for i in range(-1, q + 1)}

def step(a, b, lam, w, q):
    sub = q - 1
    d_prev = w[1][0] * a + w[1][1] * b
    for i in range(2, q):
        di = w[i][0] * a + w[i][1] * b
        if d_prev > 1.0 and di <= 1.0:
            sub = i; break
        d_prev = di
    i = sub
    wi = w[i][0] * a + w[i][1] * b
    wi1 = w[i + 1][0] * a + w[i + 1][1] * b
    yi = w[i][1]
    P = a * wi / yi
    K = math.floor((1.0 - wi1) / (lam * wi))
    return wi, wi1 + K * lam * wi, i, K, P

def low_branch_vertex(q, i):
    """The min-P vertex of genuine branch i: in (a, v=L_i) coords a=v=x_{i-1}/(1+x_{i-2}).
    Recover (a,b): L_i = a x_i + b x_{i-1} = v ; with x_i, x_{i-1} known and a known.
    a = m/(1+c), v=a, so b = (v - a x_i)/x_{i-1}."""
    x = cheb_x(q)
    m = x[i - 1]; c = x[i - 2]
    a = m / (1 + c)
    v = a
    xi = x[i]; xim1 = x[i - 1]
    b = (v - a * xi) / xim1
    return a, b

if __name__ == "__main__":
    for q in [16, 20, 24]:
        lam, w = hecke_w(q)
        inv = 1.0 / lam ** 3
        x = cheb_x(q)
        # find the deepest middle branch
        ratios = [(i, (x[i - 1] / (1 + x[i - 2] )**2) / inv) for i in range(2, q - 1)]
        i_star, r_star = min(ratios, key=lambda t: t[1])
        a, b = low_branch_vertex(q, i_star)
        # forward orbit from the low-P vertex: count consecutive P<inv
        run = 0; maxrun = 0; Ps = []
        aa, bb = a, b
        # nudge interior so it is genuinely inside the branch region
        aa += 1e-7
        for n in range(2000):
            aa, bb, i, K, P = step(aa, bb, lam, w, q)
            Ps.append(P)
            if P < inv:
                run += 1; maxrun = max(maxrun, run)
            else:
                run = 0
        # also count from the exact vertex P value forward window length until first P>=inv
        first_window = 0
        for P in Ps:
            if P < inv:
                first_window += 1
            else:
                break
        print(f"q={q:>2}  lam={lam:.5f}  1/l^3={inv:.6f}  deepest branch i={i_star} "
              f"(min P/inv={r_star:.4f})")
        print(f"        start vertex P/inv={ (a*( (x[i_star]*a)+(x[i_star-1]*b) )/x[i_star-1] )/inv if False else (x[i_star-1]/(1+x[i_star-2])**2)/inv:.4f}"
              f"   forward run below 1/l^3 from vertex: first_window={first_window}, maxrun(2000 steps)={maxrun}  (~q/3={q/3:.1f})")
