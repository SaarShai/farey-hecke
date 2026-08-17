#!/usr/bin/env python3
"""
agp_alpha.py -- LANE G: extract alpha and apply the PRE-REGISTERED verdict rule.

Reads only banked receipts (agp_kgrowth.json, agp_window.json); recomputes no
determinant and writes no file except its own .json.

THE DEFINITION OF alpha, AND A CORRECTION TO agp_window.py's FIELD NAME.
LAW_SELFBOUND_TRACE.md sec.5.1 defines alpha by  A_Gamma(r) = alpha * log q,  and
its sensitivity table substitutes that alpha into

    T(delta0) = [ 2 - (pi^2/3) delta0 b - alpha ] / [ 2/delta0 + pi^2/6 ],  b = 0.402.

So alpha is the COEFFICIENT OF log q IN THE ARCHIMEDEAN TERM -- it is read off the
archimedean term directly, and NOT from the total window mass.  agp_window.py
also emits a field named "alpha_implied" computed as 2 - slope(total mass)/2;
that quantity answers a different question (what alpha would make the integrated
budget inequality TIGHT), it is not sec.5.1's alpha, and it is NOT used here or in
LAW_AGAMMA_PROBE.md.  This script supersedes that field.

WHAT IS COMPUTED.
  alpha_asym(r)   : asymptotic slope of A_q(r) := Re dlogK_ds(1/2+ir, q) in log q,
                    from the largest q pair in agp_kgrowth.json (q = 1000 -> 4000).
  alpha_local(r)  : OLS slope of A_q(r) in log q over the ACCESSIBLE Hecke range
                    q in {5,7,9,12,15,18,21} -- the range Route B actually uses.
  alpha_windowK   : (1/2) * OLS slope of the per-width-2-window K-mass in log q,
                    per window, from agp_window.json.  Equals alpha_local up to the
                    r-averaging over the window.
  slope_G         : OLS slope of the RESONANCE part (mass_Z) in log q, per window.
                    Reported because sec.7.2's dichotomy turns on whether this
                    supplies a compensating -2 log q.  A non-negative value here
                    means the archimedean reading is the operative one.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 agp_alpha.py
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QS = [5, 7, 9, 12, 15, 18, 21]
B = 0.402
DELTA0 = 0.2


def ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    a = sxy / sxx
    b = my - a * mx
    ss = sum((y - (a * x + b)) ** 2 for x, y in zip(xs, ys))
    st = sum((y - my) ** 2 for y in ys)
    return a, b, (1 - ss / st if st else float("nan"))


def T_of(alpha, delta0=DELTA0):
    return ((2.0 - (math.pi ** 2 / 3) * delta0 * B - alpha)
            / (2.0 / delta0 + math.pi ** 2 / 6))


def verdict(alpha):
    if alpha <= 0.2:
        return "P2: alpha <= 0.2 -- A_Gamma benign, Route B budget arithmetic stands"
    if alpha < 1.0:
        return "P3: 0.2 < alpha < 1.0 -- THRESH shrinks; new required slope stated"
    if alpha < 1.7355:
        return "P3+: 1.0 <= alpha < 1.7355 -- THRESH shrinks severely"
    return "P4: alpha >= 1.7355 -- THE ROUTE B BUDGET FAILS"


def main():
    kg = json.load(open(HERE / "agp_kgrowth.json"))
    out = {"probe": "agp_alpha",
           "reads": ["agp_kgrowth.json", "agp_window.json"],
           "alpha_definition": "A_Gamma(r) = alpha * log q (LAW_SELFBOUND_TRACE sec.5.1)",
           "supersedes": "agp_window.json field 'alpha_implied' (different quantity)",
           "per_r": {}, "per_window": {}, "verdicts": {}}

    print("=== alpha from the archimedean term A_q(r) = Re (log K_q)'(1/2+ir) ===")
    for r, series in kg["series"].items():
        by_q = {v["q"]: v["kdens"] for v in series}
        xs = [math.log(q) for q in QS if q in by_q]
        ys = [by_q[q] for q in QS if q in by_q]
        a_loc, _, r2 = ols(xs, ys)
        a_asy = kg["asymptotics"][r]["local_slope_last"]
        out["per_r"][r] = {"alpha_local_q5_21": a_loc, "R2_local": r2,
                           "alpha_asymptotic": a_asy,
                           "T_0.2_at_alpha_local": T_of(a_loc),
                           "T_0.2_at_alpha_asymptotic": T_of(a_asy),
                           "verdict_local": verdict(a_loc),
                           "verdict_asymptotic": verdict(a_asy)}
        print(f"  r={float(r):8.5f}: alpha_local(q=5..21) = {a_loc:7.4f} (R2={r2:.5f}), "
              f"alpha_asymptotic = {a_asy:7.4f}   "
              f"T(0.2) = {T_of(a_loc):+8.5f} / {T_of(a_asy):+8.5f}")

    try:
        wd = json.load(open(HERE / "agp_window.json"))
    except FileNotFoundError:
        wd = None

    if wd:
        print("\n=== per-window: (1/2) slope of K-mass, and slope of the resonance part ===")
        for w in wd["params"]["windows"]:
            key = f"{w[0]}-{w[1]}"
            rows = [x for x in wd["rows"]
                    if x["q"] in QS and list(x["window"]) == list(w)]
            if len(rows) < 3:
                continue
            xs = [math.log(x["q"]) for x in rows]
            aK, _, r2K = ols(xs, [x["mass_K"] for x in rows])
            aZ, _, r2Z = ols(xs, [x["mass_Z"] for x in rows])
            aM, _, r2M = ols(xs, [x["mass"] for x in rows])
            out["per_window"][key] = {
                "n_q": len(rows),
                "slope_massK": aK, "R2_massK": r2K, "alpha_windowK": aK / 2.0,
                "slope_massZ_resonance_part": aZ, "R2_massZ": r2Z,
                "slope_total_mass": aM, "R2_total": r2M,
                "T_0.2_at_alpha_windowK": T_of(aK / 2.0),
                "verdict_windowK": verdict(aK / 2.0)}
            print(f"  W={key}: alpha_windowK = {aK/2.0:7.4f} (R2={r2K:.4f})   "
                  f"slope_G(resonance) = {aZ:+8.4f} (R2={r2Z:.4f})   "
                  f"slope_total = {aM:+8.4f}   T(0.2) = {T_of(aK/2.0):+8.5f}")

    alphas = ([v["alpha_local_q5_21"] for v in out["per_r"].values()]
              + [v["alpha_asymptotic"] for v in out["per_r"].values()]
              + [v["alpha_windowK"] for v in out["per_window"].values()])
    amin, amax = min(alphas), max(alphas)
    out["verdicts"] = {
        "alpha_range_over_all_estimators": [amin, amax],
        "alpha_headline_asymptotic": out["per_r"][list(out["per_r"])[0]]["alpha_asymptotic"],
        "all_estimators_fire_P4": all(a >= 1.7355 for a in alphas),
        "T_0.2_range": [T_of(amax), T_of(amin)],
        "pre_registered_verdict": verdict(amin)}
    print(f"\nALPHA over all estimators: [{amin:.4f}, {amax:.4f}]")
    print(f"T(0.2) over that range:    [{T_of(amax):+.5f}, {T_of(amin):+.5f}]  "
          f"(0.14903 at alpha=0)")
    print(f"PRE-REGISTERED VERDICT (worst-case, smallest alpha): {verdict(amin)}")
    print(f"all estimators fire P4: {out['verdicts']['all_estimators_fire_P4']}")

    p = __file__.replace('.py', '.json')
    with open(p, 'w') as f:
        json.dump(out, f, indent=1, default=str)
    print("wrote", p)


if __name__ == "__main__":
    main()
