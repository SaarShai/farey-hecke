#!/usr/bin/env python3
"""q3impact_u1_sup_corrected.py -- re-derive the LAW_U1_GROWTH sec.7.3 / sec.10
guard slopes from |Z_q| = |det+ . det-| / |det(1-K_q)| instead of the bare
numerator, using ONLY banked rows (u1_sup.json, u1_sup_q40.json,
u1_guard_extended.json). Writes only its own .json/.log.
"""
import json, os, math
import mpmath as mp

mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
BANKED = json.load(open(os.path.join(HERE, "q3diag_detK.json")))["b_q"]


def b_of(q):
    if str(q) in BANKED:
        return mp.mpf(repr(BANKED[str(q)]["b_q"]))
    L = 2 * mp.cos(mp.pi / q)
    return (2 - L) / (2 + L)


def detK(q, s, nmax=300):
    b, p = b_of(q), mp.mpf(1)
    for n in range(nmax):
        t = mp.power(b, s + n)
        p *= (1 - t)
        if abs(t) < mp.mpf(10) ** -45:
            break
    return p


rows = []
for f in ["u1_sup.json", "u1_sup_q40.json", "u1_guard_extended.json"]:
    rows += json.load(open(os.path.join(HERE, f)))["rows"]

IDENT = {"dU_0", "dU_1", "dU_2", "dU_6", "dU_7"}   # Re s >= 0.25, sec.10 domain
per = {}
detail = []
for r in rows:
    if r["point"] == "centre":
        continue
    q = r["q"]
    s = mp.mpc(mp.mpf(repr(r["re"])), mp.mpf(repr(r["im"])))
    D = abs(detK(q, s))
    corr = r["abs_product"] / float(D)
    detail.append({"q": q, "point": r["point"], "re": r["re"],
                   "P_repo": r["abs_product"], "abs_detK": float(D),
                   "abs_Z_corrected": corr})
    d = per.setdefault(q, {"all": [], "ident": [], "dU0": None,
                           "all_repo": [], "ident_repo": [], "dU0_repo": None})
    d["all"].append(corr); d["all_repo"].append(r["abs_product"])
    if r["point"] in IDENT:
        d["ident"].append(corr); d["ident_repo"].append(r["abs_product"])
    if r["point"] == "dU_0":
        d["dU0"] = corr; d["dU0_repo"] = r["abs_product"]


def slope(qs, vals):
    xs = [math.log(q) for q in qs]; ys = [math.log(v) for v in vals]
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / \
           sum((x - mx) ** 2 for x in xs)


qs = sorted(per)
summary = {"per_q": {}, "slopes": {}}
for q in qs:
    d = per[q]
    summary["per_q"][q] = {
        "sup_all8_repo": max(d["all_repo"]), "sup_all8_corrected": max(d["all"]),
        "sup_ident_repo": max(d["ident_repo"]), "sup_ident_corrected": max(d["ident"]),
        "dU0_repo": d["dU0_repo"], "dU0_corrected": d["dU0"],
    }
for key, a, b in [("all8", "sup_all8_repo", "sup_all8_corrected"),
                  ("identified", "sup_ident_repo", "sup_ident_corrected"),
                  ("dU_0", "dU0_repo", "dU0_corrected")]:
    summary["slopes"][key] = {
        "repo_numerator_slope": slope(qs, [summary["per_q"][q][a] for q in qs]),
        "corrected_Z_slope": slope(qs, [summary["per_q"][q][b] for q in qs]),
    }
    # also the q=16..40 window quoted in sec.7.3
    w = [q for q in qs if 16 <= q <= 40]
    summary["slopes"][key]["repo_slope_q16_40"] = slope(w, [summary["per_q"][q][a] for q in w])
    summary["slopes"][key]["corrected_slope_q16_40"] = slope(w, [summary["per_q"][q][b] for q in w])

out = {"note": "|Z_q| = |det+ det-| / |det(1-K_q)|; banked numerators unchanged",
       "identified_points": sorted(IDENT), "summary": summary, "detail": detail}
json.dump(out, open(os.path.join(HERE, "q3impact_u1_sup_corrected.json"), "w"),
          indent=1, default=str)
print(json.dumps(summary, indent=1, default=str))
