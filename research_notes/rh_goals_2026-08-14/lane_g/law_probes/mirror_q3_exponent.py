#!/usr/bin/env python3
"""
mirror_q3_exponent.py -- follow-up localiser for mirror_q3.py.

mirror_q3.py shows (*) fails at q=3 by 9.2e4 - 5.8e6, so by the pre-registered
rule the fault is (b), the Teo kappa assembly.  LAW_STRIP_AND_MIRROR.md Sec 3.6
names ONE suspect factor inside the assembly: the Barnes bracket raised to
(1-2/q)/2, the only exponent the Re s = 1/2 check is structurally blind to.

This script back-solves the exponent e that WOULD make (*) hold, at q = 3,4,6,
using the determinant ratios already measured (mirror_q3.json, mirror_arith.json)
and the exact phi_q.  If a single, q-consistent, "nice" e appears, the bug is
localised to the exponent.  If the required e is q-dependent and unstructured,
the bracket is not the whole story.

Diagnostic only.  No new hypothesis is adopted.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mpmath import (mp, mpf, mpc, gamma, sqrt, pi, sin, tan, barnesg, fabs,
                    power, zeta, log)
mp.dps = 30
TINF = mpf('7.0673625708673465')
HERE = Path(__file__).resolve().parent


def g_of_s(s):
    return sqrt(pi)*gamma(s-mpf(1)/2)*zeta(2*s-1)/(gamma(s)*zeta(2*s))


def phi_exact(q, s):
    if q == 3:
        return g_of_s(s)
    p = {4: 2, 6: 3}[q]
    return g_of_s(s)*(1+mpf(p)**(1-s))/(1+mpf(p)**s)


def E_q(s, q):
    v = mpc(1)
    for k in range(q):
        v *= power(sin(pi*(s+k)/q), mpf(q-2*k-1)/q)
    return v


def bracket(s):
    return (power(2*pi, 2*s-1)*barnesg(s)**2*gamma(1-s)
            / (barnesg(1-s)**2*gamma(s)))


def K_no_bracket(s, q):
    return (power(2, -(2*s-1)) * sqrt(tan(pi*s/2)) * E_q(s, q)
            * gamma(mpf(3)/2-s)/gamma(s+mpf(1)/2))


def rows():
    d = json.loads((HERE/"mirror_q3.json").read_text())
    for r in d["rows"]:
        if "LHS_ratio" in r:
            yield 3, mpf(repr(r["sigma"])), mpf(repr(r["LHS_ratio"]))
    d = json.loads((HERE/"mirror_arith.json").read_text())
    for r in d["rows"]:
        if "LHS_ratio" in r and r["q"] in (4, 6):
            yield r["q"], mpf(repr(r["sigma"])), mpf(repr(r["LHS_ratio"]))


def main():
    out = {"description": "back-solve the Barnes-bracket exponent e that would "
                          "make P_q(1-s)/P_q(s) = |phi_q(s)||K_q(s)| hold",
           "nominal_exponent": "(1-2/q)/2", "rows": []}
    for q, sg, lhs in rows():
        s = mpc(sg, TINF)
        nominal = (1 - mpf(2)/q)/2
        # required |bracket|^e = LHS / (|phi| |K_no_bracket|)
        need = lhs / (fabs(phi_exact(q, s)) * fabs(K_no_bracket(s, q)))
        b = fabs(bracket(s))
        e = log(need)/log(b)
        r = {"q": q, "sigma": float(sg), "LHS_ratio": float(lhs),
             "abs_bracket": float(b), "required_bracket_power": float(need),
             "required_exponent_e": float(e), "nominal_exponent": float(nominal),
             "e_minus_nominal": float(e - nominal)}
        out["rows"].append(r)
        print(f"q={q} sigma={float(sg):.2f}: |bracket|={float(b):.4e}  "
              f"required e={float(e):+.6f}   nominal (1-2/q)/2={float(nominal):.6f}  "
              f"diff={float(e-nominal):+.6f}", flush=True)
    (HERE/"mirror_q3_exponent.json").write_text(json.dumps(out, indent=1))
    print("wrote mirror_q3_exponent.json")


if __name__ == "__main__":
    main()
