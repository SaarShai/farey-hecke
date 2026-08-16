#!/usr/bin/env python3
"""Aggregate the routeb2 sub-stratum receipts (plus the routeb_ receipts that
already carry the same strata) and fit log-q slopes.  Read-only over the
originals; writes routeb2_summary.json.
"""
import json
import math
from pathlib import Path

D = Path(__file__).resolve().parent


def strata(path):
    d = json.loads(path.read_text())
    return {(c["re_lo"], c["re_hi"]): c["count"] for c in d["combined_strata"]}, d


def fit(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx if sxx else 0.0
    a = my - b * mx
    syy = sum((y - my) ** 2 for y in ys)
    r2 = (sxy ** 2 / (sxx * syy)) if sxx and syy else 0.0
    return a, b, r2


rows = {}
for p in sorted(D.glob("routeb_deepcount_q*_N*.json")) + \
        sorted(D.glob("routeb2_substratum_q*_N*.json")):
    s, d = strata(p)
    rows[(d["q"], d["N"], d.get("grid", "full"))] = {
        "s23": s.get((0.2, 0.3)), "s34": s.get((0.3, 0.4)),
        # a "sub" grid covers only [0.2,0.4], so its deep total is not the
        # Re<0.4 deep count -- report it only for the deep/full grids.
        "deep": (d.get("deep_count_re_lt_0.4")
                 if d.get("grid", "full") in ("deep", "full") else None),
        "wall": round(d["wall_seconds"]), "file": p.name,
    }

for k in sorted(rows):
    print(k, rows[k])

out = {"rows": {f"q{q}_N{N}_{g}": v for (q, N, g), v in rows.items()}, "fits": {}}
for N in (12, 16, 20):
    for key in ("s23", "s34"):
        pts = [(q, r[key]) for (q, NN, g), r in rows.items()
               if NN == N and r[key] is not None and q in (7, 9, 11, 12, 15)]
        pts = sorted(set(pts))
        if len(pts) >= 3:
            a, b, r2 = fit([math.log(q) for q, _ in pts], [y for _, y in pts])
            out["fits"][f"{key}_N{N}"] = {"pts": pts, "intercept": a,
                                          "slope_logq": b, "r2": r2}
            print(f"{key} N={N}: {a:+.3f} {b:+.3f}*log q  R2={r2:.3f}  {pts}")
(D / "routeb2_summary.json").write_text(json.dumps(out, indent=2) + "\n")
