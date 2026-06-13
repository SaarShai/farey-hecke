"""
exp_diophantine_bridge.py
=========================
PROBE: does X(q) = 1/lambda_q^3 (our ergodic-optimization ground value / cluster-onset
threshold for the Taha G_q-BCZ gap-product) have a clean algebraic relation to the
HURWITZ approximation constant H(q) and/or the bottom of the LAGRANGE SPECTRUM for the
Hecke group G_q (Rosen lambda_q-continued fractions)?

LITERATURE ANCHORS (cited, used as ground truth):
- Haas & Series, "The Hurwitz constant and Diophantine approximation on Hecke groups",
  J. London Math. Soc. (2) 34 (1986) 219-234.  Hurwitz constant
      h'_q = inf_alpha M(alpha),  |alpha - k/m| < 1/(c m^2),  M(alpha)=limsup m_n(alpha):
      h'_q = 2                              if q even
      h'_q = 2*sqrt(1 + (1 - lambda_q/2)^2) if q odd
  q=3 (odd, lambda=1): h'_3 = 2*sqrt(1 + 1/4) = sqrt(5)  <-- classical Hurwitz, ANCHOR.
- Kim & Sim arXiv:2206.05441 "Markoff and Lagrange spectra on the Hecke group H4":
  Lagrange/Markoff number L_G(xi)=limsup |M^{-1}xi - M^{-1} infty| (Euclidean geodesic
  diameter). Classical L_0 starts at sqrt5. M(H4) discrete part below 2*sqrt2 is
  {sqrt(8 - 2/x^2): x in N} U {sqrt(8 - 4/y^2): y in M}; bottom (x=1) = sqrt6.
  Figure 1 geodesic max-heights sqrt5, 2sqrt2, 2sqrt3.

This file: (a) exact X(q), lambda_q, H(q); (b) test clean relations via sympy;
(c) hand off to the numeric Rosen-CF Lagrange-bottom estimator (separate file).
"""
from __future__ import annotations
import sympy as sp


def lam_exact(q):
    """lambda_q = 2 cos(pi/q) as an exact algebraic number."""
    return 2 * sp.cos(sp.pi / q)


def X_exact(q):
    """X(q) = ergodic ground value / cluster-onset.
    X(3)=2/9, X(4)=sqrt2/8 (interior optimum), X(q>=5)=1/lambda^3 (the bare cusp/global).
    Also report the 'uniform' 1/lambda^3 column separately so we can test BOTH."""
    lam = lam_exact(q)
    if q == 3:
        return sp.Rational(2, 9)
    if q == 4:
        return sp.sqrt(2) / 8
    return sp.nsimplify(1 / lam**3)


def X_uniform(q):
    """The uniform ground value 1/lambda^3 (= X for q>=5; for q=3,4 it is the cusp value,
    twice the interior X(4))."""
    return sp.nsimplify(1 / lam_exact(q)**3)


def hurwitz_HS(q):
    """Haas-Series Hurwitz constant h'_q (bottom of the Lagrange spectrum, their norm.)."""
    lam = lam_exact(q)
    if q % 2 == 0:
        return sp.Integer(2)
    return 2 * sp.sqrt(1 + (1 - lam / 2) ** 2)


def main():
    print("=" * 92)
    print("EXACT TABLE: lambda_q, X(q), 1/lambda^3, Haas-Series Hurwitz constant H(q)")
    print("=" * 92)
    rows = {}
    for q in range(3, 13):
        lam = sp.simplify(lam_exact(q))
        X = sp.simplify(X_exact(q))
        Xu = sp.simplify(X_uniform(q))
        H = sp.simplify(hurwitz_HS(q))
        lam_n = float(lam)
        X_n = float(X)
        Xu_n = float(Xu)
        H_n = float(H)
        rows[q] = dict(lam=lam, X=X, Xu=Xu, H=H,
                       lam_n=lam_n, X_n=X_n, Xu_n=Xu_n, H_n=H_n)
        print(f"\nq={q}  (parity={'even' if q%2==0 else 'odd '})")
        print(f"   lambda_q     = {lam}   = {lam_n:.10f}")
        print(f"   X(q)         = {X}   = {X_n:.10f}")
        print(f"   1/lambda^3   = {Xu}   = {Xu_n:.10f}")
        print(f"   H(q) [Haas-Series] = {H}   = {H_n:.10f}")

    # ANCHOR CHECK: q=3 Hurwitz constant must be sqrt5.
    H3 = sp.simplify(hurwitz_HS(3))
    assert sp.simplify(H3 - sp.sqrt(5)) == 0, f"ANCHOR FAIL: H(3)={H3} != sqrt5"
    print("\n[ANCHOR OK] H(3) = sqrt(5) exactly (classical Hurwitz). H-S formula validated.")

    print("\n" + "=" * 92)
    print("RELATION TESTS (exact sympy). Looking for clean closed forms.")
    print("=" * 92)

    # We test a battery of candidate identities for each q, exact where possible.
    tests = []
    for q, d in rows.items():
        lam, X, Xu, H = d['lam'], d['X'], d['Xu'], d['H']
        cand = {
            "X*H":            sp.simplify(X * H),
            "Xu*H":           sp.simplify(Xu * H),
            "Xu*H^2":         sp.simplify(Xu * H**2),
            "X*H^2":          sp.simplify(X * H**2),
            "Xu*H^3":         sp.simplify(Xu * H**3),
            "H/Xu":           sp.simplify(H / Xu),
            "H^2/Xu":         sp.simplify(H**2 / Xu),
            "H^3*Xu":         sp.simplify(H**3 * Xu),
            "1/(Xu*H)":       sp.simplify(1 / (Xu * H)),
            "H - lam":        sp.simplify(H - lam),
            "H/lam":          sp.simplify(H / lam),
            "H^2 - lam^2":    sp.simplify(H**2 - lam**2),
            "H^2/lam":        sp.simplify(H**2 / lam),
            "Xu*H^2/lam":     sp.simplify(Xu * H**2 / lam),
            "H^2*Xu^(2/3)":   sp.simplify(H**2 * Xu**sp.Rational(2, 3)),
            "lam^3*H^2":      sp.simplify(lam**3 * H**2),  # = H^2/Xu
        }
        tests.append((q, cand))

    keys = list(tests[0][1].keys())
    print(f"\n{'expr':>16} | " + " ".join(f"q={q:>2}" for q, _ in tests))
    for k in keys:
        vals = [float(c[k]) for _, c in tests]
        print(f"{k:>16} | " + " ".join(f"{v:8.4f}" for v in vals))

    # Highlight any column that is q-INDEPENDENT (clean universal constant) or
    # cleanly tracks lambda.
    print("\n--- exact forms of the most interesting combos ---")
    for q, d in rows.items():
        lam, Xu, H = d['lam'], d['Xu'], d['H']
        print(f"q={q}: H^2/lambda^? ... H^2={sp.simplify(H**2)},  "
              f"lambda^3={sp.simplify(lam**3)},  H^2/Xu = lambda^3 H^2 = {sp.simplify(lam**3*H**2)}")

    # Odd-q closed form: H^2 = 4(1 + (1-lam/2)^2) = 4 + (2-lam)^2 = lam^2 -4 lam +8.
    print("\n--- odd-q: symbolic H(q)^2 as polynomial in lambda ---")
    lam_s = sp.symbols('lam', positive=True)
    Hsq_odd = sp.expand(4 * (1 + (1 - lam_s / 2) ** 2))
    print(f"   odd q: H^2 = {Hsq_odd}   (= lam^2 - 4 lam + 8)")
    print(f"   even q: H^2 = 4 (constant)")
    # X_uniform = 1/lam^3, so H^2 * lam^3 (odd) = lam^5 -4 lam^4 +8 lam^3, not clean.
    # Test H^2 = (2-lam)^2 + 4:
    print(f"   check (2-lam)^2+4 = {sp.expand((2-lam_s)**2+4)}")


if __name__ == "__main__":
    main()
