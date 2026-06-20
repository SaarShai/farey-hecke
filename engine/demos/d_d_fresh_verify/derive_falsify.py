#!/usr/bin/env python3
"""Demo D-D — DISCOVER + FALSIFY for the fresh lemma: minpoly of lambda_9.

This is the *discover + numerically-falsify* half of the D-D demonstration. It
is pure mpmath (no Arb, no Aristotle) and is safe to run any number of times —
it spends NO compute budget. ``run_demo.py`` imports ``derive_and_falsify`` from
here, then (optionally) submits the LIVE Aristotle proof.

Fresh lemma under test
----------------------
    lambda_9 := 2*cos(pi/9)  is a root of  x^3 - 3x - 1.

Why this cubic. lambda_q = 2*cos(pi/q) is an algebraic integer; for q=9 its
minimal polynomial over Q is the cubic x^3 - 3x - 1 (the three real roots are
2cos(pi/9), 2cos(5pi/9), 2cos(7pi/9)). We DERIVE the cubic numerically, then
FALSIFY-check it: high-precision root test + a Vieta cross-check + CONTROLS that
must FAIL (lambda_5 = phi and lambda_7 are deliberately NOT roots of x^3-3x-1).
"""
from __future__ import annotations

import mpmath as mp


def _cubic(x):
    """The candidate minimal polynomial x^3 - 3x - 1."""
    return x ** 3 - 3 * x - 1


def derive_and_falsify(dps: int = 60) -> dict:
    """Derive the lambda_9 cubic and run the numerical falsify battery.

    Returns a plain dict suitable for the DISCOVER+FALSIFY portion of a
    RunRecord. ``verdict`` is "survives" iff the root test passes AND both
    controls correctly FAIL to be roots AND the Vieta identities hold.
    """
    mp.mp.dps = dps
    pi = mp.pi

    lam9 = 2 * mp.cos(pi / 9)
    roots = {
        "2cos(pi/9)": 2 * mp.cos(pi / 9),
        "2cos(5pi/9)": 2 * mp.cos(5 * pi / 9),
        "2cos(7pi/9)": 2 * mp.cos(7 * pi / 9),
    }

    # --- root test (the primary numerical falsify-check) --------------------- #
    resid = abs(_cubic(lam9))
    tol = mp.mpf(10) ** (-(dps - 5))
    root_test_pass = resid < tol

    # --- INDEPENDENT: all three claimed roots actually annihilate the cubic -- #
    root_resids = {name: abs(_cubic(v)) for name, v in roots.items()}
    all_roots_pass = all(r < tol for r in root_resids.values())

    # --- Vieta cross-check: sum=0 (no x^2 term), e2=-3, prod=+1 (const -1) --- #
    r = list(roots.values())
    e1 = sum(r)
    e2 = r[0] * r[1] + r[0] * r[2] + r[1] * r[2]
    e3 = r[0] * r[1] * r[2]
    vieta_pass = (abs(e1) < tol) and (abs(e2 + 3) < tol) and (abs(e3 - 1) < tol)

    # --- CONTROLS: phi and lambda_7 must NOT be roots (these MUST fail) ------ #
    phi = 2 * mp.cos(pi / 5)           # golden ratio
    lam7 = 2 * mp.cos(pi / 7)
    ctrl_phi_resid = abs(_cubic(phi))
    ctrl_l7_resid = abs(_cubic(lam7))
    controls_pass = (ctrl_phi_resid > mp.mpf("0.01")) and (ctrl_l7_resid > mp.mpf("0.01"))

    survives = bool(root_test_pass and all_roots_pass and vieta_pass and controls_pass)

    return {
        "lemma": "2*cos(pi/9) is a root of x^3 - 3x - 1",
        "cubic": "x^3 - 3x - 1",
        "dps": dps,
        "lambda9": mp.nstr(lam9, 15),
        "roots": {k: mp.nstr(v, 12) for k, v in roots.items()},
        "attempts": {
            "root_test": {
                "passed": root_test_pass,
                "residual": mp.nstr(resid, 6),
                "tol": mp.nstr(tol, 3),
                "detail": "|(2cos(pi/9))^3 - 3(2cos(pi/9)) - 1| < 1e-(dps-5)",
            },
            "independent_all_roots": {
                "passed": all_roots_pass,
                "residuals": {k: mp.nstr(v, 6) for k, v in root_resids.items()},
                "detail": "all three 2cos(k*pi/9), k in {1,5,7}, annihilate the cubic",
            },
            "vieta": {
                "passed": vieta_pass,
                "sum": mp.nstr(e1, 6),
                "e2": mp.nstr(e2, 6),
                "prod": mp.nstr(e3, 6),
                "detail": "sum=0, e2=-3, prod=+1  <=>  cubic is x^3 - 0x^2 - 3x - 1",
            },
            "control_phi_not_root": {
                "passed": controls_pass,
                "phi_residual": mp.nstr(ctrl_phi_resid, 6),
                "lambda7_residual": mp.nstr(ctrl_l7_resid, 6),
                "detail": "CONTROL: 2cos(pi/5)=phi and 2cos(pi/7) are NOT roots "
                          "(residuals must be far from 0)",
            },
        },
        "verdict": "survives" if survives else "refuted",
    }


def _print_report(rep: dict) -> None:
    print("=== DISCOVER + FALSIFY: minpoly of lambda_9 = 2cos(pi/9) ===")
    print(f"  lemma : {rep['lemma']}")
    print(f"  cubic : {rep['cubic']}    (dps={rep['dps']})")
    print(f"  lambda_9 = {rep['lambda9']}")
    print("  roots:")
    for k, v in rep["roots"].items():
        print(f"    {k:14s} = {v}")
    a = rep["attempts"]
    print()
    print("  [root_test]            pass=%s  residual=%s (tol %s)"
          % (a["root_test"]["passed"], a["root_test"]["residual"], a["root_test"]["tol"]))
    print("  [independent_all_roots] pass=%s  residuals=%s"
          % (a["independent_all_roots"]["passed"], a["independent_all_roots"]["residuals"]))
    print("  [vieta]                pass=%s  sum=%s e2=%s prod=%s"
          % (a["vieta"]["passed"], a["vieta"]["sum"], a["vieta"]["e2"], a["vieta"]["prod"]))
    print("  [control_phi_not_root] pass=%s  phi_resid=%s  lambda7_resid=%s"
          % (a["control_phi_not_root"]["passed"],
             a["control_phi_not_root"]["phi_residual"],
             a["control_phi_not_root"]["lambda7_residual"]))
    print()
    print(f"  VERDICT: {rep['verdict'].upper()}")


if __name__ == "__main__":
    _print_report(derive_and_falsify())
