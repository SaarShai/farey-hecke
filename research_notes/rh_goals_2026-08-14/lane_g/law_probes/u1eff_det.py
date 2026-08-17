"""u1eff_det.py -- U1-eff entry-wise probe, step 2: does det(1 - L_{s,+}) converge in q?

The entry-wise hypothesis claims that q^{-2} entry convergence transports to a
q^{-2} DETERMINANT difference on a fixed contour.  That transport step is only
legitimate if the matrices share a dimension.  Here kappa(q) = q-2, so the
determinant is taken over a GROWING matrix.  This probe measures the actual
det(1 - L_{s,+}) at fixed strip points for a ladder of q and asks whether it
converges at all, and if so at what rate.

d = per-component truncation (matrix side kappa*d).  Two d values are run so a
dimension-truncation artefact can be separated from the q trend.

Read-only probe; writes only its own JSON next to itself.
"""
import json, math, os, sys, time

CODE = "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code"
sys.path.insert(0, CODE)
from flint import acb, arb, ctx                                    # noqa: E402
import zeta_cert_rosen as RO                                       # noqa: E402

ctx.prec = 300

N = 12
NHEAD = 4
DS = [int(x) for x in (os.environ.get("DS") or "8,12").split(",")]
SPTS = [("s1", 0.25, 7.0674), ("s2", 0.35, 17.0)]
QS = [int(x) for x in (os.environ.get("QS") or "11,21,41,81").split(",")]


def cx(z):
    return complex(float(z.real.mid()), float(z.imag.mid()))


def run():
    out = {"N": N, "n_head": NHEAD, "ds": DS, "qs": QS, "points": {}}
    for name, sr, si in SPTS:
        s = acb(sr, si)
        rows = {}
        for q in QS:
            t0 = time.time()
            M, kappa = RO.build_reduced_matrix_ball(s, N, +1, q, n_head=NHEAD)
            tb = time.time() - t0
            rec = {"q": q, "kappa": kappa, "build_s": round(tb, 2), "det": {}}
            for d in DS:
                t1 = time.time()
                det = RO._det_block(M, N, kappa, d)
                z = cx(det)
                rec["det"][str(d)] = {"dim": kappa * d, "re": z.real, "im": z.imag,
                                      "abs": abs(z), "logabs": math.log(abs(z)) if abs(z) > 0 else None,
                                      "sec": round(time.time() - t1, 1)}
                print(f"  {name} q={q} d={d} dim={kappa*d} det={z:.8g} "
                      f"|det|={abs(z):.8g} ({time.time()-t1:.1f}s)", flush=True)
            rows[q] = rec
        out["points"][name] = rows
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "u1eff_det.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", p)


if __name__ == "__main__":
    run()
