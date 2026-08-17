"""b5j_expansion.py -- B5-J probe 4: why no invariant disc system exists.

For each MMS block (i,j,branch n) of G_q, the inverse branch is
h_n(z) = -1/(z+n lam) (pos) or +1/(z - n lam) (neg).  A disc system with
h_n(D_i) subset D_j and ratio theta < 1 exists only if the branches contract.
We report sup_{z in cell_i} |h_n'(z)| = sup 1/|z +- n lam|^2 per block, the
global max over blocks, and the prediction sec^2(pi/q) for the n=1 pos branch
at the left endpoint z = -lam/2 (where |z+lam| = lam/2 = cos(pi/q) < 1).
"""
import json, math, os, sys
CODE = "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code"
sys.path.insert(0, CODE)
from flint import ctx                                              # noqa: E402
import zeta_cert_rosen as RO, zeta_cert_rosen_even as RE           # noqa: E402
from b5j_disc import blocks, cx                                    # noqa: E402
ctx.prec = 300

out = []
for q in [5, 7, 8, 9, 10, 11, 12, 15, 18, 21, 40, 100]:
    M = RE if q % 2 == 0 else RO
    lamb = M.lam_ball(q); lam = float(lamb.real.mid())
    hq, kappa = M.hecke_params(q)
    pts = sorted(cx(p).real for p in M.partition_points_ball(q, lamb))
    worst, arg = 0.0, None
    for (i, j, kind, n, neg) in blocks(q, kappa, hq):
        ns = [n] if kind == "sgl" else list(range(n, n + 6))
        a, b = pts[i - 1], pts[i]
        for nn in ns:
            for z in (a, b, (a + b) / 2):
                d = (z + nn * lam) if not neg else (z - nn * lam)
                v = 1.0 / (d * d)
                if abs(v) > worst:
                    worst, arg = abs(v), (i, j, kind, nn, neg, z)
    out.append({"q": q, "lam": lam, "kappa": kappa,
                "sup_|h'|": worst, "argmax": list(map(str, arg)),
                "sec2_pi_over_q": 1.0 / math.cos(math.pi / q) ** 2,
                "cell_width_min": min(pts[i] - pts[i-1] for i in range(1, len(pts))),
                "cell_width_max": max(pts[i] - pts[i-1] for i in range(1, len(pts)))})
    print(json.dumps(out[-1]), flush=True)
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "b5j_expansion.json")
json.dump(out, open(p, "w"), indent=1)
print("wrote", p)
