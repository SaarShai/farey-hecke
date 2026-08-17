"""b5j_growth.py -- B5-J probe 5: growth of det(1-L_s) in the s-plane, and the
R-optimisation of the Jensen ratio.

(a) |det(1-L_{s,+})| along Re s = x, Im s = 7, x from -2.5 to 0.5.  This tests
    the parent document's claim (LAW_ROUTEB_CONDITIONAL_THEOREM sec.6.3 item 1)
    that "the determinant is entire of order 0 in s -- no growth theorem needed".
(b) C_jensen(R) = (log max_{|s-c|=R}|det| - log|det(c)|)/log(R/1) for a range of
    R, i.e. the best the Jensen route can do with a PERFECT sup bound.
"""
import json, math, os, sys, cmath
CODE = "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code"
sys.path.insert(0, CODE)
from flint import acb, arb, ctx                                    # noqa: E402
import zeta_cert_rosen as RO, zeta_cert_rosen_even as RE           # noqa: E402
ctx.prec = 300


def det_at(q, s, N=16, sign=+1):
    M = RE if q % 2 == 0 else RO
    return M.cert_det_complex_mid(acb(arb(s.real), arb(s.imag)), N, sign, q)


out = {"N": 16, "t0": 7.0, "line": [], "Rsweep": []}
for q in (5, 7, 9):
    row = {"q": q, "x": [], "log_abs_det": []}
    x = -2.5
    while x <= 0.5001:
        v = abs(det_at(q, complex(x, 7.0)))
        row["x"].append(round(x, 3))
        row["log_abs_det"].append(math.log(v) if v > 0 else None)
        x += 0.25
    out["line"].append(row)
    print("line", json.dumps(row), flush=True)

for q in (5, 7, 9):
    c = complex(0.25, 7.0)
    m = abs(det_at(q, c))
    row = {"q": q, "log_m": math.log(m), "R": [], "log_M": [], "C_jensen": []}
    for R in (1.1, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0):
        mx = max(abs(det_at(q, c + R * cmath.exp(2j * math.pi * t / 32)))
                 for t in range(32))
        row["R"].append(R)
        row["log_M"].append(math.log(mx))
        row["C_jensen"].append((math.log(mx) - math.log(m)) / math.log(R))
    out["Rsweep"].append(row)
    print("Rsweep", json.dumps(row), flush=True)

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b5j_growth.json")
json.dump(out, open(p, "w"), indent=1)
print("wrote", p)
