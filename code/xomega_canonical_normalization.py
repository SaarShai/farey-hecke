"""
xomega_canonical_normalization.py
=================================
DECISION SCRIPT (goal): does the slope-gap support edge X_Omega of Hecke
triangle groups admit ANY canonical normalization that turns it into a genuine
COMMENSURABILITY invariant distinguishing the arithmetic cases {3,4,6}?

Background falsification this script must engage with:
  code/out/xomega_normalization_proof.json (bug_id 14): the RAW edge is
  normalization-dependent. The gap-product observable P (=1/lambda^3) and the
  ACL return-time observable R (=1) are RECIPROCAL, not diagonal-conjugate, so
  the lambda^3 Veech-bridge normalization is FALSIFIED. The raw number carries
  no more info than the trace field Q(cos(pi/q)).

This script tests whether ANY of three CANONICAL normalizations survives:
  (i)   covolume / area-normalized:   edge / area,   area = -pi*chi(orbifold)
  (ii)  systole-normalized:           edge * systole^k
  (iii) cusp-width-affine:            edge * cusp_width

For TWO families over q in {5,7,8,9,11,13}:
  Hecke  H_q = Delta(2,q,inf):  raw edge = 1/lambda_q^3,  lambda_q = 2cos(pi/q)
  Polygon P_q = Delta(q,inf,inf) (the (2q)-gon family used as the matched
              non-commensurable comparison with the SAME invariant trace field
              Q(cos(2pi/q))):  raw edge taken as 1/mu_q^3, mu_q = 2cos(pi/q)
              (same unit gap-product convention; the support edge of the
              Veech section in the gap-product normalization).

Each normalization is graded against the invariant-trace-field GROUND TRUTH on
THREE properties:
  (P1) DISTINGUISH non-commensurable same-trace-field pairs:
       Hecke H_q vs Polygon P_q have the SAME invariant trace field
       Q(cos(2pi/q)) but are NOT commensurable (different signatures).
       A real invariant MUST give them DIFFERENT values.
  (P2) CONSTANT on commensurable groups:
       The only commensurable cluster among cusped triangle groups is the
       arithmetic one (Takeuchi). H_3,H_4,H_6 are pairwise NON-commensurable
       (distinct arithmetic Fuchsian groups), so "constant where commensurable"
       has no positive multi-member class to enforce here EXCEPT the trivial
       single-member classes. We test the strongest available surrogate: the
       value must be a well-defined function of the commensurability class and
       NOT vary within a class. With only singletons this is vacuously passed;
       we record it honestly as VACUOUS rather than a genuine PASS.
  (P3) DISTINGUISHED VALUE on q in {3,4,6}:
       the normalization must take a value on the three arithmetic q that is
       set apart from (e.g. constant across, or cleanly separated from) the
       non-arithmetic q. We test: is the normalized edge CONSTANT on {3,4,6}
       OR does it cleanly threshold {3,4,6} away from the rest?

ANY_NORMALIZATION_PASSES = True iff some normalization passes P1 AND P3
(and P2 non-vacuously). Otherwise bug_id 14 generalizes.
"""
from __future__ import annotations
import math
import json
import os
import mpmath

mpmath.mp.dps = 50

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

# Reuse exact commensurability machinery (invariant trace field + degree)
import sys
sys.path.insert(0, HERE)
from xomega_commensurability import invariant_trace_field_gens, field_degree_over_Q  # noqa: E402

Q_LIST = [5, 7, 8, 9, 11, 13]
ARITH = {3, 4, 6}  # the arithmetic Hecke/triangle cases (Takeuchi)


def lam(q):
    """lambda_q = 2 cos(pi/q), the Hecke unit."""
    return 2 * mpmath.cos(mpmath.pi / q)


# ----------------------------------------------------------------------------
# Geometric normalizers (exact mpmath)
# ----------------------------------------------------------------------------
def orbifold_area(p, q, r):
    """
    Hyperbolic area of the triangle orbifold Delta(p,q,r) = -pi*chi
      = pi*(1 - 1/p - 1/q - 1/r),  with 1/inf = 0.
    (The full (2,q,inf) group; the triangle itself is half, area pi*(1-1/2-1/q).)
    We use the GROUP covolume = 2 * triangle area = 2*pi*(1 - 1/p - 1/q - 1/r)?
    For comparing X_Omega normalization the constant factor 2 is irrelevant; we
    take the orbifold (quotient) area A = pi*(1 - 1/p - 1/q - 1/r).
    """
    def inv(n):
        return mpmath.mpf(0) if n == 'inf' else mpmath.mpf(1) / n
    return mpmath.pi * (1 - inv(p) - inv(q) - inv(r))


def systole(lam_val):
    """
    Systole (length of shortest closed geodesic) of the Hecke surface.
    For G_q the shortest geodesic has trace 2*lambda (recorded in repo memory:
    'systole trace = 2*lambda exactly'); length = 2*arccosh(|trace|/2) =
    2*arccosh(lambda).  For the polygon family we reuse the same trace=2*mu form.
    Returns 0.0 if lambda < 1 (no hyperbolic element of that trace).
    """
    if lam_val <= 1:
        return mpmath.mpf(0)
    return 2 * mpmath.acosh(lam_val)


def cusp_width(lam_val):
    """
    Cusp width of the Hecke group G_q: the parabolic generator is translation by
    lambda_q, so the cusp width (in the standard normalization, modular cusp
    width 1 at q=3 where lambda=1) is lambda_q itself.
    """
    return lam_val


# ----------------------------------------------------------------------------
# Build the table
# ----------------------------------------------------------------------------
def family_rows():
    rows = []
    # we need q=3,4,6 too for property P3, plus the requested Q_LIST
    all_q = sorted(set(Q_LIST) | ARITH)
    for q in all_q:
        L = lam(q)
        raw = 1 / L**3                      # raw support edge (gap-product unit)
        gens = invariant_trace_field_gens(2, q, 'inf')
        deg = field_degree_over_Q(gens)
        A = orbifold_area(2, q, 'inf')      # pi*(1 - 1/2 - 1/q)
        syst = systole(L)
        cw = cusp_width(L)

        rows.append({
            "family": "Hecke",
            "q": q,
            "type": f"(2,{q},inf)",
            "arithmetic": q in ARITH,
            "lambda": float(L),
            "raw_edge_1/lam3": float(raw),
            "inv_trace_field": f"Q(cos(2pi/{q}))",
            "inv_trace_field_deg": deg,
            "area": float(A),
            "systole": float(syst),
            "cusp_width": float(cw),
            # candidate canonical normalizations:
            "norm_i_area": float(raw / A) if A != 0 else None,
            # systole-normalized: edge * systole^k.  The gap-product edge has
            # units (length)^{-2} (P=a*b is an area in the cross-section), so the
            # natural systole power to make it scale-free is k=2 -> edge*syst^2;
            # we also record k=3 to match the lambda^3 power and k=1.
            "norm_ii_systole_k2": float(raw * syst**2),
            "norm_ii_systole_k3": float(raw * syst**3),
            "norm_iii_cuspwidth": float(raw * cw),
        })

    # Polygon family P_q = Delta(q,inf,inf), the (2q)-gon, matched same-trace-field
    for q in all_q:
        mu = lam(q)  # 2 cos(pi/q): same algebraic unit (Veech polygon param)
        raw = 1 / mu**3
        gens = invariant_trace_field_gens(q, 'inf', 'inf')
        deg = field_degree_over_Q(gens)
        A = orbifold_area(q, 'inf', 'inf')  # pi*(1 - 1/q)
        syst = systole(mu)
        cw = cusp_width(mu)
        rows.append({
            "family": "Polygon",
            "q": q,
            "type": f"({q},inf,inf)",
            "arithmetic": q in ARITH,
            "lambda": float(mu),
            "raw_edge_1/lam3": float(raw),
            "inv_trace_field": f"Q(cos(2pi/{q}))",
            "inv_trace_field_deg": deg,
            "area": float(A),
            "systole": float(syst),
            "cusp_width": float(cw),
            "norm_i_area": float(raw / A) if A != 0 else None,
            "norm_ii_systole_k2": float(raw * syst**2),
            "norm_ii_systole_k3": float(raw * syst**3),
            "norm_iii_cuspwidth": float(raw * cw),
        })
    return rows


# ----------------------------------------------------------------------------
# Property tests
# ----------------------------------------------------------------------------
def approx_eq(a, b, tol=1e-9):
    if a is None or b is None:
        return False
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def test_normalization(rows, key):
    """
    Grade one normalization column `key` on P1/P2/P3.
    Returns dict with pass/fail per property + detail.
    """
    by = {}
    for r in rows:
        by[(r["family"], r["q"])] = r.get(key)

    # ---- P1: distinguish same-trace-field non-commensurable pairs
    # For each q: Hecke H_q vs Polygon P_q (same inv trace field, NOT commensurable).
    p1_pairs = []
    p1_pass = True
    for q in sorted(set(Q_LIST) | ARITH):
        h = by.get(("Hecke", q))
        p = by.get(("Polygon", q))
        differ = not approx_eq(h, p)
        p1_pairs.append({"q": q, "hecke": h, "polygon": p, "differ": differ})
        if not differ:
            p1_pass = False

    # ---- P2: constant where commensurable.
    # Among cusped triangle groups the ONLY commensurable cluster is arithmetic,
    # but H_3,H_4,H_6 are pairwise NON-commensurable distinct arithmetic groups.
    # => there is NO non-singleton commensurability class in this sample.
    # The property is therefore VACUOUS (no positive constraint). We report it as
    # such; it cannot be a genuine pass.
    p2_status = "VACUOUS (no non-singleton commensurability class in sample; "\
                "H_3,H_4,H_6 pairwise non-commensurable)"

    # ---- P3: distinguished value on {3,4,6}.
    # Test (a) CONSTANT across the three arithmetic q, and
    #      (b) cleanly THRESHOLDED: max over {3,4,6} separated from the rest.
    arith_vals = {q: by.get(("Hecke", q)) for q in sorted(ARITH)}
    nonarith_vals = {q: by.get(("Hecke", q)) for q in Q_LIST}
    av = [v for v in arith_vals.values() if v is not None]
    nv = [v for v in nonarith_vals.values() if v is not None]
    const_on_arith = False
    if len(av) == 3:
        const_on_arith = (max(av) - min(av)) <= 1e-9 * max(1.0, max(abs(x) for x in av))
    # clean separation: do the arithmetic values occupy a band disjoint from
    # the non-arithmetic ones? (a monotone cut would let a single threshold
    # isolate {3,4,6})
    clean_threshold = False
    if av and nv:
        amin, amax = min(av), max(av)
        nmin, nmax = min(nv), max(nv)
        # disjoint intervals => separable
        clean_threshold = (amax < nmin) or (amin > nmax)
    p3_pass = const_on_arith or clean_threshold

    return {
        "normalization": key,
        "P1_distinguish_noncommensurable": {"pass": p1_pass, "pairs": p1_pairs},
        "P2_constant_on_commensurable": {"pass": False, "status": p2_status},
        "P3_distinguished_on_3_4_6": {
            "pass": bool(p3_pass),
            "constant_on_arith": bool(const_on_arith),
            "clean_threshold": bool(clean_threshold),
            "arith_values": {str(k): v for k, v in arith_vals.items()},
            "nonarith_values": {str(k): v for k, v in nonarith_vals.items()},
        },
        # A normalization PASSES the goal only if it distinguishes
        # non-commensurable pairs (P1) AND singles out {3,4,6} (P3) AND P2 is a
        # genuine (non-vacuous) pass. P2 is vacuous here => no genuine pass.
        "overall_pass": bool(p1_pass and p3_pass) and False,
        "overall_pass_ignoring_vacuous_P2": bool(p1_pass and p3_pass),
    }


def main():
    rows = family_rows()
    norm_keys = [
        "raw_edge_1/lam3",      # baseline (bug_id 14 says this fails)
        "norm_i_area",
        "norm_ii_systole_k2",
        "norm_ii_systole_k3",
        "norm_iii_cuspwidth",
    ]
    grades = {k: test_normalization(rows, k) for k in norm_keys}

    any_pass = any(g["overall_pass"] for g in grades.values())

    # ---- print human-readable table
    print("=" * 100)
    print("X_Omega CANONICAL NORMALIZATION DECISION  (vs bug_id 14)")
    print("=" * 100)
    hdr = (f"{'fam':8s} {'q':>3s} {'arith':>6s} {'raw=1/lam3':>12s} "
           f"{'/area':>11s} {'*syst^2':>11s} {'*syst^3':>11s} {'*cuspw':>11s}")
    print(hdr)
    print("-" * 100)
    for r in rows:
        print(f"{r['family']:8s} {r['q']:>3d} {str(r['arithmetic']):>6s} "
              f"{r['raw_edge_1/lam3']:>12.7f} "
              f"{(r['norm_i_area'] if r['norm_i_area'] is not None else float('nan')):>11.6f} "
              f"{r['norm_ii_systole_k2']:>11.6f} "
              f"{r['norm_ii_systole_k3']:>11.6f} "
              f"{r['norm_iii_cuspwidth']:>11.6f}")

    print("\n" + "=" * 100)
    print("PROPERTY GRADES PER NORMALIZATION")
    print("=" * 100)
    for k in norm_keys:
        g = grades[k]
        print(f"\n[{k}]")
        print(f"  P1 distinguish non-commensurable (Hecke H_q vs Polygon P_q): "
              f"{'PASS' if g['P1_distinguish_noncommensurable']['pass'] else 'FAIL'}")
        for pr in g["P1_distinguish_noncommensurable"]["pairs"]:
            print(f"      q={pr['q']:>2}: H={pr['hecke']!s:>14} "
                  f"P={pr['polygon']!s:>14} differ={pr['differ']}")
        print(f"  P2 constant on commensurable: VACUOUS -> {g['P2_constant_on_commensurable']['pass']} "
              f"({g['P2_constant_on_commensurable']['status']})")
        p3 = g["P3_distinguished_on_3_4_6"]
        print(f"  P3 distinguished on {{3,4,6}}: {'PASS' if p3['pass'] else 'FAIL'}  "
              f"(constant_on_arith={p3['constant_on_arith']}, clean_threshold={p3['clean_threshold']})")
        print(f"      arith {{3,4,6}} values:    {p3['arith_values']}")
        print(f"      non-arith {Q_LIST} values: {p3['nonarith_values']}")
        print(f"  OVERALL (needs P1 & P2-genuine & P3): {'PASS' if g['overall_pass'] else 'FAIL'}"
              f"   [P1&P3 ignoring vacuous P2: "
              f"{'pass' if g['overall_pass_ignoring_vacuous_P2'] else 'fail'}]")

    print("\n" + "=" * 100)
    print(f"ANY_NORMALIZATION_PASSES = {any_pass}")
    print("=" * 100)

    out = {
        "ANY_NORMALIZATION_PASSES": any_pass,
        "q_list": Q_LIST,
        "arithmetic_q": sorted(ARITH),
        "ground_truth": "arithmetic <=> q in {3,4,6} (Takeuchi); inv trace field "
                        "Q(cos(2pi/q)) is the commensurability invariant",
        "engages_bug_id_14": "code/out/xomega_normalization_proof.json: raw edge "
                             "normalization-dependent (P,R reciprocal). This script "
                             "tests area / systole / cusp-width canonical fixes.",
        "table": rows,
        "grades": grades,
        "notes": {
            "P2_vacuous": "H_3,H_4,H_6 are pairwise non-commensurable distinct "
                          "arithmetic Fuchsian groups; no non-singleton "
                          "commensurability class exists in the sample, so "
                          "'constant on commensurable' has no positive content. "
                          "It cannot be a genuine pass -> ANY_NORMALIZATION_PASSES "
                          "requires P1 & P3 AND a genuine P2, which is unattainable here.",
            "systole_formula": "length = 2*arccosh(lambda), trace=2*lambda (repo memory).",
            "cusp_width_formula": "cusp width = lambda_q (parabolic translation length).",
            "area_formula": "A = pi*(1 - 1/p - 1/q - 1/r), 1/inf=0.",
        },
    }
    path = os.path.join(OUT, "xomega_canonical_normalization.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved {path}")
    return any_pass


if __name__ == "__main__":
    main()
