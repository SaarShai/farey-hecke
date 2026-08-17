"""b5j_jensen.py -- B5-J probe 3: the Jensen ratio itself.

For the MMS reduced determinant det(1 - L_{s,sign}) of G_q, on a disc
D(c,R) with c inside the strip 0 < Re s < 1/2 at height t0:

    M  := max_{|s-c|=R} |det(1-L_s)|      (sup bound, MEASURED)
    m  := |det(1-L_c)|                    (one-point lower bound, MEASURED)
    C_J := log(M/m) / log(R/r)            (Jensen bound on #zeros in D(c,r))

Jensen's formula:  n(r) log(R/r) <= log M - log|f(c)|  for f entire, f(c)!=0.

This measures what the Jensen route WOULD give even with perfect constants,
and how it scales in q.  Non-rigorous probe: midpoint (float) evaluation of the
Arb ball determinants, no certified dimension tail.
"""
import json, math, os, sys, cmath

CODE = "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code"
sys.path.insert(0, CODE)
from flint import acb, arb, ctx                                    # noqa: E402
import zeta_cert_rosen as RO                                       # noqa: E402
import zeta_cert_rosen_even as RE                                  # noqa: E402

ctx.prec = 300


def det_at(q, s, N, sign, n_head=4):
    M = RE if q % 2 == 0 else RO
    return M.cert_det_complex_mid(acb(arb(s.real), arb(s.imag)), N, sign, q,
                                  n_head=n_head)


def scan(q, c, R, N, sign, K=64):
    vals = []
    for t in range(K):
        s = c + R * cmath.exp(2j * math.pi * t / K)
        vals.append((t, abs(det_at(q, s, N, sign))))
    mx = max(v for _, v in vals)
    mn = min(v for _, v in vals)
    return mx, mn, vals


def run(qs, N=16, t0=7.0, cre=0.25, Rs=(1.5, 2.0), r=1.0, K=24):
    out = {"N": N, "t0": t0, "c_re": cre, "r_count": r, "rows": []}
    for q in qs:
        c = complex(cre, t0)
        row = {"q": q}
        for sign in (+1, -1):
            m = abs(det_at(q, c, N, sign))
            e = {"m_center": m, "log_m": math.log(m) if m > 0 else None,
                 "discs": []}
            for R in Rs:
                mx, mn, _ = scan(q, c, R, N, sign, K=K)
                d = {"R": R, "M_sup": mx, "min_on_circle": mn,
                     "log_M": math.log(mx)}
                if m > 0 and R > r:
                    d["C_jensen"] = (math.log(mx) - math.log(m)) / math.log(R / r)
                e["discs"].append(d)
            row[f"sign{sign:+d}"] = e
        out["rows"].append(row)
        print(json.dumps(row), flush=True)
    return out


if __name__ == "__main__":
    qs = [int(x) for x in (sys.argv[1:] or ["5", "12", "21"])]
    res = run(qs)
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "b5j_jensen.json")
    with open(p, "w") as f:
        json.dump(res, f, indent=1)
    print("wrote", p)
