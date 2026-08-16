#!/usr/bin/env python3
"""
strip_confirm.py -- LANE G, TASK A confirmation.

strip_phi_continuation.py measures |phi_q| on the crux strip with two
truncations (X = 60, 120) at enumeration budget norm_bound = 1200.  Two
findings need a harder look before they are reported:

  (a) at t = t_inf the q-sequence decays monotonically (slope ~ -0.97 at
      sigma = 0.90), but at t = 1.5 and t = 3.5 it does NOT -- it dips and
      then RISES over q = 12..56.  Artefact or real?
  (b) the whole-range slope is dominated by the q = 8 endpoint.

This script re-measures with THREE truncations (X = 40, 80, 120) at the same
budget and, for two q, at the larger budget norm_bound = 2000 / cmax = 200 with
X = 200.  If the value is stable across truncation AND across enumeration
budget, the non-decay at t = 1.5, 3.5 is a property of phi_q, not of the method.
Slopes are reported both over q = 8..56 and over q = 12..56.
"""
import json, math, sys, time
from mpmath import mp, mpf, mpc, fabs
from strip_phi_continuation import enumerate_c_spectrum, phi_cont

mp.dps = 30
TINF = mpf('7.0673625708673465')


def slope(qs, vals):
    xs = [math.log(q) for q in qs]
    ys = [math.log(v) for v in vals]
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    return (sum((a-mx)*(b-my) for a, b in zip(xs, ys))
            / sum((a-mx)**2 for a in xs))


def main():
    qs = [8, 12, 16, 22, 30, 40, 56]
    sigmas = [mpf('0.90'), mpf('0.95')]
    ts = [mpf('1.5'), mpf('3.5'), TINF]
    Xs = [40.0, 80.0, 120.0]
    out = {"description": "TASK A confirmation: truncation- and budget-stability "
                          "of |phi_q| on the crux strip",
           "params": {"norm_bound": 1200.0, "cmax": 120.0, "Xs": Xs},
           "vals": {}, "hi_budget": [], "slopes": {}}

    for q in qs:
        t0 = time.time()
        lam, cls, ne = enumerate_c_spectrum(q, 1200.0, 120.0)
        for sg in sigmas:
            for t in ts:
                s = mpc(sg, t)
                k = f"sigma={float(sg)},t={float(t):.4f}"
                rec = {"q": q}
                for X in Xs:
                    rec[f"X{int(X)}"] = float(fabs(phi_cont(cls, s, q, X)))
                sp = max(rec[f"X{int(X)}"] for X in Xs) - min(rec[f"X{int(X)}"] for X in Xs)
                rec["trunc_spread_rel"] = sp / rec["X120"]
                out["vals"].setdefault(k, []).append(rec)
        print(f"q={q} done {time.time()-t0:.0f}s", flush=True)

    # higher enumeration budget on two q, to separate truncation from budget
    for q in (16, 40):
        t0 = time.time()
        lam, cls, ne = enumerate_c_spectrum(q, 2000.0, 200.0)
        for sg in sigmas:
            for t in ts:
                s = mpc(sg, t)
                out["hi_budget"].append(
                    {"q": q, "sigma": float(sg), "t": float(t),
                     "X120": float(fabs(phi_cont(cls, s, q, 120.0))),
                     "X200": float(fabs(phi_cont(cls, s, q, 200.0))),
                     "n_elts": ne})
        print(f"hi-budget q={q} n_elts={ne} {time.time()-t0:.0f}s", flush=True)

    for k, rows in out["vals"].items():
        e = {}
        for X in Xs:
            e[f"slope_q8_56_X{int(X)}"] = slope([r["q"] for r in rows],
                                                [r[f"X{int(X)}"] for r in rows])
            sub = [r for r in rows if r["q"] >= 12]
            e[f"slope_q12_56_X{int(X)}"] = slope([r["q"] for r in sub],
                                                 [r[f"X{int(X)}"] for r in sub])
        sg = float(k.split(',')[0].split('=')[1])
        e["required_minimal_hypothesis"] = -0.5
        e["required_2sigma_minus_1"] = -(2*sg - 1)
        out["slopes"][k] = e

    print("\n=== slopes (q=8..56 | q=12..56), three truncations ===")
    for k, e in out["slopes"].items():
        print(f"  {k}")
        for X in Xs:
            print(f"     X={int(X):3d}:  q8-56 {e[f'slope_q8_56_X{int(X)}']:+.4f}"
                  f"   q12-56 {e[f'slope_q12_56_X{int(X)}']:+.4f}")
        print(f"     bars: minimal-hypothesis < -0.50 ; (2sigma-1) < "
              f"{e['required_2sigma_minus_1']:+.2f}")

    print("\n=== higher enumeration budget (norm_bound 2000, cmax 200) ===")
    for r in out["hi_budget"]:
        print(f"  q={r['q']} sigma={r['sigma']} t={r['t']:.4f}: "
              f"X120={r['X120']:.6f}  X200={r['X200']:.6f}  "
              f"rel_diff={abs(r['X200']-r['X120'])/r['X200']:.3f}")

    with open(__file__.replace('.py', '.json'), 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("\nwrote", __file__.replace('.py', '.json'))


if __name__ == "__main__":
    main()
