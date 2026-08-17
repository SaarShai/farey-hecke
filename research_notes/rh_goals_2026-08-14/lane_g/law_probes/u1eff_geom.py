"""u1eff_geom.py -- U1-eff entry-wise probe, step 0: does a theta-LIMIT MATRIX exist?

The entry-wise hypothesis presupposes a fixed-dimension limit object M_infty
(the Gamma_theta transfer matrix) that M_q converges to entrywise.  This probe
measures the MMS Markov geometry as q grows:

  kappa(q)              = number of Markov components (= matrix block count)
  cell widths           = phi_i - phi_{i-1}
  rho_min, rho_max      = smallest / largest disc radius (safety 5/2)

If kappa grows and rho_min collapses, no fixed M_infty exists and the
hypothesis is structurally ill-posed BEFORE any determinant is computed.

Read-only probe; writes only its own JSON next to itself.
"""
import json, os, sys

CODE = "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code"
sys.path.insert(0, CODE)
from flint import acb, arb, ctx                                    # noqa: E402
import zeta_cert_rosen as RO                                       # noqa: E402

ctx.prec = 300


def cx(z):
    return complex(float(z.real.mid()), float(z.imag.mid()))


def run():
    out = []
    for q in [5, 7, 9, 11, 15, 21, 41, 81, 161, 321]:
        lam = RO.lam_ball(q)
        hq, kappa = RO.hecke_params(q)
        pts = [cx(p).real for p in RO.partition_points_ball(q, lam)]
        widths = [pts[i] - pts[i - 1] for i in range(1, len(pts))]
        rho = [abs(cx(x)) for x in RO.disc_radii_ball(q, lam)]
        lamf = float(lam.real.mid())
        out.append(dict(
            q=q, lam=lamf, two_minus_lam=2.0 - lamf, pi2_over_q2=(3.141592653589793 ** 2) / q ** 2,
            kappa=kappa, dim_N16=kappa * 16,
            width_min=min(widths), width_max=max(widths),
            rho_min=min(rho), rho_max=max(rho),
            rho_ratio=max(rho) / min(rho),
            # cell nearest the collapsing endpoint -lambda/2 and nearest 0
            width_first=widths[0], width_last=widths[-1],
            pts_head=pts[:4], pts_tail=pts[-4:],
        ))
        print(out[-1], flush=True)
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "u1eff_geom.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=1)
    print("wrote", p)


if __name__ == "__main__":
    run()
