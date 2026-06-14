"""
xomega_invariance_test.py
=========================
TRACK 3 (decisive test).  Is the support edge X_Omega(Gamma) := ess-inf of the
horocycle-section return time a GENUINE invariant of the lattice Gamma (or the
commensurability class), or a normalization artifact?

THREE normalization conventions, computed for each surface:
  (1) section-coordinate min R  (the papers' convention: shortest horiz = shortest
      vert sc = 1).  -> EXPECTED universally 1 (artifact).
  (2) Hecke/Taha convention (parabolic generator [[1,lambda],[0,1]], lambda=cusp
      translation length).  -> my project's 1/lambda^3.
  (3) UNIT-AREA convention: rescale the surface to area 1, then the smallest
      *un-renormalized* slope gap has an intrinsic value; equivalently
      (min R) x (geometric normalization).  Test commensurability invariance here.

DICTIONARY (derived):
  Hecke G_q-BCZ threshold  1/lambda_q^3  =  (cusp-tip value of gap-product P)
  ACL/Berman section min R  =  1  (cusp corner (1,1))
  The two sections differ by the SL2 conjugation that sends the parabolic
  [[1,lambda],[0,1]] (Hecke) to [[1,1],[0,1]] (ACL): a diagonal scaling
  diag(sqrt(lambda), 1/sqrt(lambda)) scales slopes by lambda, hence gaps by
  lambda^2, and the area element accordingly.  So
        (min R)_Hecke-normalized  =  lambda * (min R)_ACL  ... to be checked.

We compute, for the triangle-group Veech surfaces:
  - Hecke H_q  (=Delta(2,q,inf)),  q=5,7,8,...  [my family]
  - 2n-gon O_{2n} (=Delta(n,inf,inf)),  n=3..10
  - check the cusp-width ratio (commensurability signature) per Takeuchi/Maclachlan.
"""
from __future__ import annotations
import math, json, os
import mpmath
mpmath.mp.dps = 40
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)


def lam(q):
    return 2 * mpmath.cos(mpmath.pi / q)


# ---------------------------------------------------------------------------
# Golden L done RIGHT: minimize R over the ACL section with the correct
# 3-piece return-time (Thm 3.1 of 1308.4203), parabolic = [[1,1],[0,1]].
# ACL Thm 3.1: Omega = {(a,b): 0<a<=1, 1 - a*phi < b <= phibar - a}
#   Omega_1   : phibar <= a <=1,        1-a*phi < b <= phibar - a       R=1/(a(a+b))
#   Omega_phi : phibar^2 <= a <=1,      phibar-a < b <= phibar - a*phibar R=1/(a(a*phibar+b))
#   Omega_inf : 0<a<=1,                 phibar - a*phibar < b <= 1?      R=1/(ab)
# The actual return time is the value of the listed piece on its subdomain.
# ---------------------------------------------------------------------------
def golden_L_minR_exact():
    phi = (1 + math.sqrt(5)) / 2
    phibar = 1 / phi
    best = (1e18, None, None, None)
    N = 3000
    for ia in range(1, N + 1):
        a = ia / N
        b_lo = max(1e-7, 1 - a * phi)
        b_hi = phibar  # right edge phibar - a is < phibar; use phibar as box top
        for ib in range(0, N + 1):
            b = b_lo + (b_hi - b_lo) * ib / N
            if b <= 0:
                continue
            # assign piece by ACL subdomain boundaries:
            R = None
            if phibar - 1e-12 <= a <= 1 and 1 - a * phi < b <= phibar - a + 1e-12:
                R = 1.0 / (a * (a + b))
            elif phibar**2 - 1e-12 <= a <= 1 and phibar - a < b <= phibar - a * phibar + 1e-12:
                R = 1.0 / (a * (a * phibar + b))
            elif 0 < a <= 1 and phibar - a * phibar < b <= 1 + 1e-12:
                R = 1.0 / (a * b)
            if R is not None and 0 < R < best[0]:
                best = (R, a, b, "auto")
    return {"minR": best[0], "a*": best[1], "b*": best[2]}


# ---------------------------------------------------------------------------
# Hecke H_q Taha-BCZ:  the genuine gap-product P over the section.
# The support edge (ess-inf) = 1/lambda^3.  We ALSO compute the *return-time*
# analogue and its min, to compare with the Veech R.  In the Taha section the
# minimum gap (return time) is governed by the parabolic translation length
# lambda; the natural "min R" in Hecke coords is 1/lambda (cusp width^-1)
# scaled.  We report the canonical numbers.
# ---------------------------------------------------------------------------
def hecke_numbers(q):
    L = lam(q)
    return {
        "q": int(q),
        "lambda": float(L),
        "1/lambda^3": float(1 / L**3),
        "1/lambda": float(1 / L),
        "lambda^2": float(L**2),  # arithmeticity: lambda^2 in Z iff q in {3,4,6}
        "lambda^2_int_dist": float(abs(L**2 - round(float(L**2)))),
    }


# ---------------------------------------------------------------------------
# Commensurability / arithmeticity signatures of the triangle groups.
# Takeuchi 1977: arithmetic triangle groups are a finite list.
#   Hecke Delta(2,q,inf) arithmetic  <=>  q in {3,4,6,inf}  (lambda^2 in Z).
#   2n-gon Delta(n,inf,inf) arithmetic <=> n in {?}  (Takeuchi list for (n,inf,inf)).
#   Delta(n,inf,inf) is arithmetic for n=3,4,6,inf (same crystallographic n).
# Commensurability of triangle groups: Takeuchi's commensurability classes.
# ---------------------------------------------------------------------------
def triangle_arith_signature():
    # arithmetic (p,q,inf) triangle groups (Takeuchi 1977, table of arithmetic
    # triangle groups). (2,q,inf): q=3,4,6,inf.  (n,inf,inf): n=3,4,6,inf.
    sig = {}
    for q in range(3, 13):
        L = float(lam(q))
        # Delta(2,q,inf) = Hecke H_q arithmetic iff q in {3,4,6}
        sig[f"Hecke H_{q} = D(2,{q},inf)"] = {
            "lambda": L, "lambda^2": L*L,
            "lambda^2_is_int": abs(L*L - round(L*L)) < 1e-9,
            "arithmetic": q in (3, 4, 6),
            "type": "(2,%d,inf)" % q,
        }
    for n in range(3, 11):
        c = math.cos(math.pi / n)
        sig[f"2n-gon O_{2*n} = D({n},inf,inf)"] = {
            "cos(pi/n)": c, "2cos(pi/n)": 2*c,
            "arithmetic": n in (3, 4, 6),  # Delta(n,inf,inf) arithmetic <=> n in {3,4,6,inf}
            "type": "(%d,inf,inf)" % n,
        }
    return sig


if __name__ == "__main__":
    print("=" * 72)
    print("DECISIVE TEST: is the support edge an invariant or a normalization artifact?")
    print("=" * 72)

    print("\n[1] golden L (=double pentagon = Hecke H_5 = Delta(2,5,inf)) min R in ACL coords")
    gL = golden_L_minR_exact()
    print(f"    min R = {gL['minR']:.6f}  at (a,b)=({gL['a*']:.5f},{gL['b*']:.5f})")
    print(f"    ACL paper states min R = 1 (smallest slope gap). artifact-of-normalization check.")

    print("\n[2] Hecke H_q canonical numbers (Taha normalization: parabolic [[1,lambda],[0,1]])")
    hk = []
    for q in [5, 7, 8, 9, 10, 11, 12]:
        r = hecke_numbers(q)
        hk.append(r)
        print(f"    q={q:2d}: lambda={r['lambda']:.5f}  1/lambda^3={r['1/lambda^3']:.6f}  "
              f"1/lambda={r['1/lambda']:.6f}  lambda^2={r['lambda^2']:.5f} "
              f"(int-dist {r['lambda^2_int_dist']:.4f})")

    print("\n[3] arithmeticity signatures of the triangle-group Veech surfaces")
    sig = triangle_arith_signature()
    for name, d in sig.items():
        arith = "ARITH" if d["arithmetic"] else "non-arith"
        extra = (f"lambda^2={d['lambda^2']:.4f}" if "lambda^2" in d
                 else f"2cos={d['2cos(pi/n)']:.4f}")
        print(f"    {name:30s} {d['type']:14s} {arith:9s} {extra}")

    results = {"goldenL": gL, "hecke": hk, "signatures": sig}
    with open(os.path.join(OUT, "xomega_invariance_test.json"), "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved {os.path.join(OUT, 'xomega_invariance_test.json')}")
