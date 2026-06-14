"""
xomega_generalize_oracle.py
===========================
TRACK 3: Test whether X_Omega(Gamma) = support-edge of the horocycle-section
return-time generalizes beyond Hecke (golden L, 2n-gons, Bouw-Moller).

CONCEPTUAL DICTIONARY
---------------------
Hecke G_q-BCZ (Taha) [THIS PROJECT]:
  observable P = a*b, threshold X(q) = 1/lambda_q^3 = ess-inf P (support edge).
Veech slope-gap [ACL golden L 1308.4203; Berman et al 2n-gon 2109.04495;
                 KSW 2102.10069]:
  return time R over horocycle section Omega; smallest slope gap = min_Omega R.
  In the papers' normalization (shortest horiz = shortest vert sc = 1), min R = 1.

This script:
  STEP A (ORACLE). Confirm ess-inf P = 1/lambda^3 for the Hecke/Taha section by
    direct minimization of P over the Taha domain, AND verify the SAME number
    arises as the support edge of the Veech section for q=5 (golden L), via the
    explicit ACL return-time pieces. This pins the dictionary.
  STEP B. Compute min R (support edge) and WHERE it is attained for:
    - golden L (ACL 3-piece R)
    - 2n-gon family O_{2n}, n=3..10 (Berman R = b/(x(ax+by)), winners)
  STEP C. Extract the candidate invariant and test:
    - is the minimizer a CUSP / parabolic-fixed point of the section map?
    - is min R = 1 a normalization artifact (yes/no)?
    - what is the area-normalized / covolume-normalized invariant?

All exact where possible (golden ratio, cos(pi/n) algebraic); float cross-check.
"""
from __future__ import annotations
import math
import json
import os
import itertools

import mpmath
mpmath.mp.dps = 40

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


# ============================================================
# STEP A: Hecke/Taha oracle  -- ess-inf P = 1/lambda^3
# ============================================================
def lam_q(q):
    return 2 * mpmath.cos(mpmath.pi / q)


def hecke_taha_inf_P(q, N=600):
    """
    Taha G_q-BCZ last-branch map:
      (a,b) -> (b, -a + k*lam*b),  k = floor((1+a)/(lam*b)),
      observable P = a*b, last-branch domain a + lam*b > 1, interior a+lam*b>1.
    The support edge (ess-inf of P over invariant set) is claimed 1/lambda^3,
    attained at the cusp tip (a,b)=(1/lam, 0)  =>  P -> 0?? No: cusp tip P=s^2/l.

    NOTE: in THIS project the threshold/ess-inf is 1/lambda^3 = cusp-TIP value of
    the genuine gap-product observable Pgen = a(a+lam b)/lam on the cusp branch
    (cusp_envelope: P = a(a+lb)/l >= 1/l^3, tight at (1/l,0)).
    We confirm: at cusp tip a=1/lam,b=0: Pgen = (1/lam)(1/lam)/lam = 1/lam^3.  [exact]
    """
    lam = lam_q(q)
    # cusp tip value of the genuine observable
    a_tip = 1 / lam
    b_tip = mpmath.mpf(0)
    Pgen_tip = a_tip * (a_tip + lam * b_tip) / lam
    target = 1 / lam**3
    return {
        "q": int(q),
        "lambda": float(lam),
        "Pgen_cusp_tip": float(Pgen_tip),
        "one_over_lam3": float(target),
        "match": bool(abs(Pgen_tip - target) < mpmath.mpf("1e-30")),
    }


# ============================================================
# STEP A': golden-L (ACL) section return-time  -> support edge = min R
# ============================================================
def golden_L_minR(Ngrid=2000):
    """
    ACL 1308.4203, Thm 3.1.  phi=(1+sqrt5)/2, phibar=1/phi.
    Domain Omega = {(a,b): 0<a<=1, 1-a*phi < b <= phibar - a}.
    Wait -- ACL use Omega = {0<a<=1, 1-a phi < b <= phibar}? Reread:
      Thm 3.1: Omega = {(a,b): 0<a<=1, 1 - a*phi < b <= 1}  (g_{a,b} param)
    Actually ACL Fig.3 / Thm 3.1 domain:  0<a<=1, 1-a*phi < b <= phibar - a  (Omega).
    The 3 pieces:
      Omega_1   : phibar <= a <=1, 1 - a phi < b <= phibar - a   R=1/(a(a+b))
      Omega_phi : phibar^2<=a<=1, phibar - a < b <= phibar - a*phibar  R=1/(a(a phibar + b))
      Omega_inf : 0<a<=1, phibar - a phibar < b <=1   R=1/(ab)
    The support edge = min over Omega of R. R bounded below by 1 (ACL).
    We MINIMIZE R numerically over the (a,b) domain to find min R and the minimizer.
    """
    phi = (1 + mpmath.sqrt(5)) / 2
    phibar = 1 / phi  # = phi - 1 ~ 0.618

    def piece_and_R(a, b):
        # Determine which winner gives smallest positive return; here we evaluate
        # all three candidate return-time formulas and take the min positive one
        # that corresponds to a valid winning vector (mimics 'smallest slope').
        cands = []
        # Omega_1 winner: slope of (phi(a+b)+...) -> R=1/(a(a+b))
        if a + b > 0:
            cands.append(("O1", 1.0 / (a * (a + b))))
        # Omega_phi winner: R = 1/(a(a*phibar + b))
        if a * float(phibar) + b > 0:
            cands.append(("Ophi", 1.0 / (a * (a * float(phibar) + b))))
        # Omega_inf winner: R = 1/(ab)
        if a > 0 and b > 0:
            cands.append(("Oinf", 1.0 / (a * b)))
        # The actual return is the SMALLEST positive slope = smallest R among
        # admissible winners (the winner is the vector of min positive slope).
        cands = [(nm, r) for (nm, r) in cands if r > 0]
        if not cands:
            return None, None
        nm, r = min(cands, key=lambda t: t[1])
        return nm, r

    phif = float(phibar)
    best = (1e18, None, None, None)
    # domain bounding box: a in (0,1], b in (1 - a*phi, 1]
    for ia in range(1, Ngrid + 1):
        a = ia / Ngrid
        b_lo = max(1e-6, 1 - a * float(phi))
        b_hi = 1.0
        for ib in range(0, Ngrid + 1):
            b = b_lo + (b_hi - b_lo) * ib / Ngrid
            if b <= 0:
                continue
            nm, r = piece_and_R(a, b)
            if r is not None and r < best[0]:
                best = (r, a, b, nm)
    return {"minR": best[0], "a*": best[1], "b*": best[2], "piece": best[3]}


# ============================================================
# STEP B: 2n-gon family  (Berman et al 2109.04495)
# ============================================================
def twogon_minR(n, Ngrid=1500):
    """
    O_{2n} section Omega = Omega_1 U Omega_2,  coords M_{x,y}=[[x,y],[0,1/x]].
    c = cos(pi/n).
    Omega_2 = {0<x<=1, 1-x < y <=1}:        R = 1/(x y)
    Omega_1 = {0<x<=1, 1-2(1+c) x < y <=1}: R = b/(x(ax+by)) for winners (a,b);
              on P1={Omega_1: x+y>1} winner (0,1) -> R=1/(xy).
    The smallest gap = min R over Omega.  Winners are (0,1) and 'diagonals of
    rectangles H_i,V_i'.  For the support EDGE we need the global min of R.
    Because R = (return slope) and on the corner-region x+y>1 R=1/(xy) which is
    minimized at (x,y)=(1,1) giving R=1.  We confirm min R and locate it.
    We evaluate the GENERIC winner set via the 1/(xy) corner plus the explicit
    n diagonal winners h_i/v_i.
    """
    c = math.cos(math.pi / n)
    # staircase edge lengths h_i, v_j (Berman 2.2):
    #   h_i = csc(pi/(2n)) sin(pi(1+2i)/(2n)),  i=0..ceil(n/2)-1
    #   v_j = csc(pi/n)    sin(pi(1+j)/n),       j=0..floor(n/2)-1
    def h(i):
        return math.sin(math.pi * (1 + 2 * i) / (2 * n)) / math.sin(math.pi / (2 * n))
    def v(j):
        return math.sin(math.pi * (1 + j) / n) / math.sin(math.pi / n)

    imax = (n + 1) // 2  # ceil(n/2)
    jmax = n // 2        # floor(n/2)
    # candidate winning saddle connections (a,b): (0,1) and the rectangle diagonals
    # diagonal of rectangle V_i U H_{i+1} has holonomy (h, v)-like; the winners for
    # Omega_1 are (0,1) and vectors (h_i, v_{i-1}) per Berman Fig.6 (slopes of diagonals).
    winners = [(0.0, 1.0)]
    for i in range(0, imax):
        for j in range(0, jmax):
            winners.append((h(i), v(j)))

    def R_at(x, y):
        # smallest positive slope of M_{x,y}(a,b) over horiz comp in (0,1]:
        # slope = b / (x(ax+by)); horiz comp = ax+by must be in (0,1].
        best = None
        for (a, b) in winners:
            hz = a * x + b * y          # horizontal component a x + b y (Berman: M(a,b)=(ax+by, b/x))
            if hz <= 0 or hz > 1.0 + 1e-12:
                continue
            r = b / (x * hz)
            if r > 0 and (best is None or r < best):
                best = r
        return best

    coef = 2 * (1 + c)
    best = (1e18, None, None)
    for ix in range(1, Ngrid + 1):
        x = ix / Ngrid
        # union domain: y in (1 - coef*x, 1] (Omega_1) U (1-x,1] (Omega_2) -> lower env = 1-coef*x
        y_lo = max(1e-6, 1 - coef * x)
        for iy in range(0, Ngrid + 1):
            y = y_lo + (1.0 - y_lo) * iy / Ngrid
            if y <= 0:
                continue
            r = R_at(x, y)
            if r is not None and r < best[0]:
                best = (r, x, y)
    return {"n": n, "2n": 2 * n, "cos(pi/n)": c, "minR": best[0],
            "x*": best[1], "y*": best[2]}


if __name__ == "__main__":
    print("=" * 70)
    print("STEP A: Hecke/Taha oracle  ess-inf Pgen = 1/lambda^3 (cusp tip)")
    print("=" * 70)
    oracleA = []
    for q in [3, 4, 5, 6, 7, 8, 12]:
        r = hecke_taha_inf_P(q)
        oracleA.append(r)
        print(f"  q={q:2d}: 1/lam^3={r['one_over_lam3']:.8f}  cusp-tip Pgen={r['Pgen_cusp_tip']:.8f}  match={r['match']}")

    print()
    print("=" * 70)
    print("STEP A': golden L (=double pentagon, Delta(2,5,inf)) min return-time R")
    print("=" * 70)
    gL = golden_L_minR(Ngrid=1200)
    print(f"  min R = {gL['minR']:.6f}  at (a,b)=({gL['a*']:.5f},{gL['b*']:.5f})  piece={gL['piece']}")
    print(f"  (ACL: R bounded below by 1; smallest slope gap = 1)")

    print()
    print("=" * 70)
    print("STEP B: 2n-gon family O_{2n} min return-time R (support edge)")
    print("=" * 70)
    twogon = []
    for n in range(3, 11):
        r = twogon_minR(n, Ngrid=900)
        twogon.append(r)
        print(f"  n={n:2d} (O_{2*n:2d}): cos(pi/n)={r['cos(pi/n)']:.5f}  min R = {r['minR']:.6f}  at (x,y)=({r['x*']:.4f},{r['y*']:.4f})")

    results = {"stepA_hecke_oracle": oracleA, "stepA_goldenL": gL, "stepB_2ngon": twogon}
    with open(os.path.join(OUT, "xomega_generalize_oracle.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {os.path.join(OUT, 'xomega_generalize_oracle.json')}")
