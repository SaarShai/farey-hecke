#!/usr/bin/env python3
"""
GOAL F (B) — general-q per-branch envelope P_i >= 1/lam^3 on branches i=2..q-2.

Tools:
 - x_i = sin((i+1)pi/q)/sin(pi/q) = Chebyshev U_i(cos th); recurrence x_{i+1}=lam x_i - x_{i-1};
   x_{-1}=0, x_0=1, x_{q-2}=1, x_{q-3}=lam, x_{q-1}=0.
 - L_i(a,b) = a x_i + b x_{i-1}.   Branch i  <=>  L_{i-1}>1 and L_i<=1  (i=2..q-1).
 - Observable P_i = a*L_i / x_{i-1}  (= a*b on scalar branch i=q-1; = a(a+lam b)/lam on cusp i=q-2).
 - Exact identity (det x_{i-1}^2 - x_i x_{i-2} = 1):
     a = x_{i-1} L_{i-1} - x_{i-2} L_i ,   b = x_{i-1} L_i - x_i L_{i-1},
     P_i = L_i (L_{i-1} - rho L_i),  rho = x_{i-2}/x_{i-1}.

This script:
 (1) finds the min of P_i over each branch polygon (vertex enumeration) and its location;
 (2) confirms cusp branch min = 1/lam^3, others > 1/lam^3;
 (3) tests the candidate vertex V_i = {L_{i-1}=1} ∩ {b=1-lam a}, a=(x_{i-2}-1)/x_{i-3}.
"""
import numpy as np
from itertools import combinations
import math

def build(q):
    th = math.pi/q
    lam = 2*math.cos(th)
    # x_i for i=-1..q   (index shift: x[k] = x_{k-1}), store dict
    x = {-1:0.0, 0:1.0}
    for i in range(1, q+2):
        x[i] = lam*x[i-1] - x[i-2]
    return lam, x

def Pobs(a,b,i,x):
    Li = a*x[i] + b*x[i-1]
    return a*Li/x[i-1]

def constraints(i, lam, x):
    # each constraint as (f, name) where feasible region is f(a,b) >= -tol  (>=0)
    # branch: L_{i-1}>1, L_i<=1 ; domain: 0<a<=1, b>1-lam a, b<=1
    return {
        'Lim1_ge1': lambda a,b: (a*x[i-1]+b*x[i-2]) - 1.0,      # L_{i-1}-1 >= 0
        'Li_le1'  : lambda a,b: 1.0 - (a*x[i]+b*x[i-1]),       # 1 - L_i >= 0
        'a_ge0'   : lambda a,b: a,
        'a_le1'   : lambda a,b: 1.0 - a,
        'bdom'    : lambda a,b: b - (1.0 - lam*a),             # b - (1-lam a) >= 0
        'b_le1'   : lambda a,b: 1.0 - b,
    }

def lines(i, lam, x):
    # boundary lines as (A,B,C) meaning A*a+B*b=C
    return {
        'Lim1=1': (x[i-1], x[i-2], 1.0),
        'Li=1'  : (x[i],   x[i-1], 1.0),
        'a=0'   : (1.0, 0.0, 0.0),
        'a=1'   : (1.0, 0.0, 1.0),
        'bdom'  : (lam, 1.0, 1.0),     # lam a + b = 1
        'b=1'   : (0.0, 1.0, 1.0),
        'b=0'   : (0.0, 1.0, 0.0),
    }

def solve2(l1, l2):
    A = np.array([[l1[0],l1[1]],[l2[0],l2[1]]])
    C = np.array([l1[2],l2[2]])
    if abs(np.linalg.det(A))<1e-12: return None
    return np.linalg.solve(A,C)

def explore(q, verbose=True):
    lam, x = build(q)
    thr = 1.0/lam**3
    out = {}
    for i in range(2, q-1):     # i=2..q-2 (exclude scalar q-1)
        cons = constraints(i, lam, x)
        lns = lines(i, lam, x)
        verts = []
        names = list(lns.keys())
        for n1,n2 in combinations(names,2):
            p = solve2(lns[n1], lns[n2])
            if p is None: continue
            a,b = p
            if not np.all(np.isfinite(p)): continue
            ok = all(f(a,b) >= -1e-9 for f in cons.values())
            if ok:
                verts.append((a,b,Pobs(a,b,i,x),(n1,n2)))
        if not verts:
            out[i]=None; continue
        vmin = min(verts, key=lambda t:t[2])
        out[i]=(vmin, lam, thr)
        if verbose:
            tag = " <CUSP q-2>" if i==q-2 else ""
            print(f"  q={q} branch i={i}{tag}: minP={vmin[2]:.8f}  thr=1/lam^3={thr:.8f}  "
                  f"ratio={vmin[2]/thr:.6f}  at a={vmin[0]:.5f},b={vmin[1]:.5f} via {vmin[3]}")
    return out, lam, x, thr

def grid_check(q, N=600):
    """dense grid over Tq, classify by branch, find min P per branch, count P<thr off-scalar."""
    lam, x = build(q); thr=1.0/lam**3
    minP = {i:1e9 for i in range(2,q)}
    below_off = 0
    for ia in range(1,N):
        a = ia/N
        for ib in range(0,N+1):
            b = -1 + 2*ib/N
            if not (0<a<=1 and 1-lam*a < b <= 1): continue
            # branch
            br=None
            for i in range(2,q):
                if a*x[i-1]+b*x[i-2] > 1-1e-12 and a*x[i]+b*x[i-1] <= 1+1e-12:
                    br=i; break
            if br is None: continue
            P = Pobs(a,b,br,x)
            minP[br]=min(minP[br],P)
            if br <= q-2 and P < thr-1e-9:
                below_off += 1
    return minP, thr, below_off

if __name__=="__main__":
    print("=== Vertex-enumeration min of P_i per branch (i=2..q-2) ===")
    for q in range(5,14):
        explore(q)
    print("\n=== Candidate vertex V_i = {L_{i-1}=1} ∩ {b=1-lam a}: a=(x_{i-2}-1)/x_{i-3} ===")
    for q in [5,6,7,8,10,13]:
        lam,x = build(q); thr=1/lam**3
        for i in range(2,q-1):
            a = (x[i-2]-1)/x[i-3] if abs(x[i-3])>1e-12 else float('nan')
            b = 1-lam*a
            P = Pobs(a,b,i,x)
            tag=" <CUSP>" if i==q-2 else ""
            print(f"  q={q} i={i}{tag}: a={a:.5f} b={b:.5f} P={P:.8f} (thr={thr:.8f}, P-thr={P-thr:+.2e})")
    print("\n=== Dense-grid reduction check (P<thr off scalar branch count should be 0) ===")
    for q in [5,6,7,8]:
        minP,thr,below_off = grid_check(q, N=500)
        s = "  ".join(f"i={i}:{minP[i]:.5f}" for i in range(2,q))
        print(f"  q={q} thr={thr:.6f}  minP[{s}]  below_off={below_off}")
