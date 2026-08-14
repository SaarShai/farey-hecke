"""T-a recon: measure worst-case branch-image contraction for G_5 discs.
Empirical (float) — guides the proof; the proven version uses Arb."""
import math, sys, json
sys.path.insert(0, "/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
from zeta_mayer_rosen import hecke_params, partition_points, disc_centers, disc_radii
import numpy as np

q = 5
lam, hq, kappa = hecke_params(q)
pts = partition_points(q)
cs = disc_centers(q)
rs = disc_radii(q)          # safety 2.5 (default)
print("lambda=%.6f kappa=%d" % (lam, kappa))
print("partition:", [round(p,6) for p in pts])
print("centers  :", [round(c,6) for c in cs])
print("radii    :", [round(r,6) for r in rs])

theta = np.exp(2j*np.pi*np.arange(4096)/4096)
worst = 0.0; rows = []
NHEAD = 60
for i in range(kappa):            # source disc (operator input contour)
    z = cs[i] + rs[i]*theta
    for n in range(1, NHEAD+1):
        for sgn in (+1, -1):
            img = -1.0/(z + n*lam) if sgn>0 else 1.0/(z - n*lam)
            # nearest target disc: min over j of normalized distance
            best = min((np.max(np.abs(img - cs[j]))/rs[j], j) for j in range(kappa))
            rho, j = best
            rows.append((i, sgn*n, j, float(rho)))
            worst = max(worst, rho) if rho < 10 else worst
# report worst head contraction that is actually < 1 (branches mapping into domain)
inside = [r for r in rows if r[3] < 1.0]
outside = [r for r in rows if r[3] >= 1.0]
w = max(r[3] for r in inside)
print("head branches landing strictly inside some disc: %d/%d" % (len(inside), len(rows)))
print("worst contraction ratio among inside-landing head branches: rho_hat = %.6f" % w)
if outside:
    print("branches NOT inside any disc (first 6):", [(r[0], r[1], round(r[3],3)) for r in outside[:6]])
# tail bound at n0: |theta_n(z)| <= 1/(n*lam - lam/2 - max rad)
n0 = 8
tail = 1.0/(n0*lam - lam/2 - max(rs))
print("explicit tail bound at n0=%d: |image| <= %.6f (vs min disc reach %.6f)" % (n0, tail, min(abs(c)-r for c,r in zip(cs,rs))))
json.dump({"rho_hat_inside": w, "n_inside": len(inside), "n_total": len(rows),
           "outside_sample": outside[:10], "centers": cs, "radii": rs},
          open("/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/ta_recon.json","w"), indent=1)
