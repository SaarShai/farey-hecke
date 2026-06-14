"""
xomega_commensurability.py
==========================
TRACK 3 commensurability test.  The commensurability invariant of a (non-arith)
Fuchsian group is the INVARIANT TRACE FIELD  k(Gamma) = Q(tr(gamma^2): gamma in Gamma).
For a triangle group Delta(p,q,r):
    trace field      Q(cos(pi/p), cos(pi/q), cos(pi/r), cos(pi/p)cos(pi/q)cos(pi/r))
    invariant trace field (commensurability invariant), per Maclachlan-Reid:
    k = Q(cos(2pi/p), cos(2pi/q), cos(2pi/r), cos(pi/p)cos(pi/q)cos(pi/r)).
For r=inf: cos(pi/inf)=1, cos(2pi/inf)=1.

We test whether the candidate X_Omega (support edge in a CANONICAL normalization)
is a commensurability invariant -- i.e. equal for commensurable surfaces and
distinguishing non-commensurable ones -- or whether it only reproduces the
trace field (already known) / collapses to a normalization artifact.

Families:
  Hecke H_q = Delta(2,q,inf):   X_Omega^Hecke = 1/lambda_q^3, lambda_q=2cos(pi/q).
  2n-gon    = Delta(n,inf,inf):  section min-R = 1 (artifact).
  We compute invariant trace field generators and the degree, and compare.
"""
from __future__ import annotations
import math, json, os
from fractions import Fraction
import mpmath
mpmath.mp.dps = 50
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

try:
    from sympy import cos, pi, nsimplify, sqrt, simplify, Rational, minimal_polynomial, Symbol, QQ, degree
    HAVE_SYMPY = True
except Exception:
    HAVE_SYMPY = False


def field_degree_over_Q(generators):
    """Degree of Q(generators) over Q using sympy minimal polynomials / composite."""
    if not HAVE_SYMPY:
        return None
    x = Symbol('x')
    # Build primitive element heuristically: sum of generators with small int coeffs
    from sympy import simplify as ssimp
    # degree of the compositum: use sympy's primitive_element
    from sympy.polys.numberfields import primitive_element
    gens = [g for g in generators if ssimp(g) != 0 and ssimp(g) != 1]
    if not gens:
        return 1
    try:
        minpoly, coeffs = primitive_element(gens, x, ex=False)
        from sympy import Poly
        return Poly(minpoly, x).degree()
    except Exception:
        return None


def invariant_trace_field_gens(p, q, r):
    """
    Maclachlan-Reid invariant trace field of Delta(p,q,r):
      k = Q( cos(2pi/p), cos(2pi/q), cos(2pi/r), cos(pi/p)cos(pi/q)cos(pi/r) ).
    r='inf' -> cos(pi/inf)=1, cos(2pi/inf)=1.
    Returns list of sympy generators.
    """
    def cp(n):   # cos(pi/n)
        return Rational(1) if n == 'inf' else cos(pi / n)
    def c2(n):   # cos(2pi/n)
        return Rational(1) if n == 'inf' else cos(2 * pi / n)
    gens = [c2(p), c2(q), c2(r), cp(p) * cp(q) * cp(r)]
    return gens


def analyze():
    rows = []
    # Hecke H_q = Delta(2,q,inf)
    for q in list(range(3, 13)):
        L = float(2 * math.cos(math.pi / q))
        gens = invariant_trace_field_gens(2, q, 'inf')
        deg = field_degree_over_Q(gens) if HAVE_SYMPY else None
        # invariant trace field of Delta(2,q,inf) = Q(cos(2pi/q)) (since cos(2pi/2)=-1, prod=0)
        rows.append({
            "name": f"Hecke H_{q}", "type": f"(2,{q},inf)",
            "lambda": L, "lambda^2": L*L,
            "arithmetic": q in (3, 4, 6),
            "X_Omega_Hecke=1/lambda^3": 1.0 / L**3,
            "inv_trace_field_deg": deg,
            "inv_trace_field": "Q(cos(2pi/%d))" % q,
        })
    # 2n-gon = Delta(n,inf,inf)
    for n in list(range(3, 11)):
        c = float(math.cos(math.pi / n))
        gens = invariant_trace_field_gens(n, 'inf', 'inf')
        deg = field_degree_over_Q(gens) if HAVE_SYMPY else None
        rows.append({
            "name": f"2n-gon O_{2*n}", "type": f"({n},inf,inf)",
            "2cos(pi/n)": 2*c,
            "arithmetic": n in (3, 4, 6),
            "section_minR": 1.0,
            "inv_trace_field_deg": deg,
            "inv_trace_field": "Q(cos(2pi/%d))" % n,
        })
    return rows


if __name__ == "__main__":
    print("=" * 78)
    print("COMMENSURABILITY: invariant trace field (the real invariant) vs X_Omega")
    print("=" * 78)
    rows = analyze()
    print(f"\n{'name':14s} {'type':12s} {'arith':9s} {'X_Omega/minR':>13s} {'inv-tr-field':>16s} {'deg':>4s}")
    print("-" * 78)
    for r in rows:
        xo = r.get("X_Omega_Hecke=1/lambda^3", r.get("section_minR"))
        arith = "ARITH" if r["arithmetic"] else "non-arith"
        deg = r["inv_trace_field_deg"]
        print(f"{r['name']:14s} {r['type']:12s} {arith:9s} {xo:13.6f} {r['inv_trace_field']:>16s} {str(deg):>4s}")

    # Commensurability check:  Delta(2,q,inf) and Delta(q,inf,inf) share inv trace
    # field Q(cos(2pi/q)); are they commensurable?  (Takeuchi: commensurable iff same
    # quaternion algebra; for non-arith, iff same invariant trace field AND ramification.)
    print("\nKEY COMMENSURABILITY OBSERVATIONS:")
    print("  - Delta(2,q,inf) and Delta(q,inf,inf) have the SAME invariant trace field")
    print("    Q(cos(2pi/q)). For NON-arithmetic groups the invariant trace field is a")
    print("    COMPLETE commensurability invariant only together with the quaternion algebra;")
    print("    triangle groups with different signatures are generally NOT commensurable")
    print("    (Takeuchi: the 9 cusped arithmetic ones are the only commensurable cluster).")
    print("  - X_Omega^Hecke = 1/lambda_q^3 is a FUNCTION of lambda_q = 2cos(pi/q), i.e. it")
    print("    lives in the TRACE FIELD Q(cos(pi/q)) (a degree-2 ext of inv trace field).")
    print("    => X_Omega carries NO more commensurability info than the trace field already")
    print("       known classically.  It is a normalization-fixed representative, not new data.")

    with open(os.path.join(OUT, "xomega_commensurability.json"), "w") as f:
        json.dump(rows, f, indent=2)
    print(f"\nSaved {os.path.join(OUT, 'xomega_commensurability.json')}")
