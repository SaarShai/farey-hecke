#!/usr/bin/env python3
"""Aggregate routeb_deepcount_q*_N*.json: stratified table, log-q fits, N-stability."""
from __future__ import annotations
import json, math, sys
from pathlib import Path

D = Path(__file__).resolve().parent
QS = [5, 7, 8, 9, 10, 11, 12, 15, 18, 21]
LABELS = ['[0.023,0.1)', '[0.1,0.2)', '[0.2,0.3)', '[0.3,0.4)', '[0.4,0.487)']


def load(q, N):
    p = D / f"routeb_deepcount_q{q}_N{N}.json"
    return json.loads(p.read_text()) if p.exists() else None


def lsq(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = my - b * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    return a, b, (1 - ss_res / ss_tot if ss_tot else float("nan"))


def table(N):
    rows = []
    for q in QS:
        d = load(q, N)
        if d is None:
            continue
        rows.append({
            "q": q, "N": N,
            "strata": [c["count"] for c in d["combined_strata"]],
            "shallow": d["shallow_count_re_ge_0.4"],
            "deep": d["deep_count_re_lt_0.4"],
            "total": d["total_count"],
            "maxres": max(c["max_residual"] for c in d["combined_strata"]),
            "warn": d["n_warnings"], "mindet": d["min_absdet_on_contours"],
            "calls": d["det_calls"], "wall": d["wall_seconds"],
        })
    return rows


def report(rows, N):
    if not rows:
        print(f"\n=== N={N}: no data ===")
        return
    print(f"\n=== N={N} ===   strata = {LABELS}")
    print(f"{'q':>3} {'strata (deep -> shallow)':>26} {'deep':>5} {'shal':>5} "
          f"{'tot':>4} {'maxres':>8} {'wn':>3} {'min|det|':>9} {'wall':>6}")
    for r in rows:
        print(f"{r['q']:>3} {str(r['strata']):>26} {r['deep']:>5} {r['shallow']:>5} "
              f"{r['total']:>4} {r['maxres']:>8.1e} {r['warn']:>3} "
              f"{r['mindet']:>9.2e} {r['wall']:>6.0f}")
    lq = [math.log(r["q"]) for r in rows]
    qs = [r["q"] for r in rows]
    for key in ("shallow", "deep", "total"):
        ys = [r[key] for r in rows]
        a, b, r2 = lsq(lq, ys)
        a2, b2, r22 = lsq(qs, ys)
        print(f"  {key:>8}: {a:+7.3f} {b:+.3f}*log q  R2={r2:.3f}   | "
              f"linear-in-q {a2:+7.3f} {b2:+.4f}*q  R2={r22:.3f}  | vals={ys}")
    print("  per-sub-stratum log-q slope:")
    for j, lab in enumerate(LABELS):
        ys = [r["strata"][j] for r in rows]
        a, b, r2 = lsq(lq, ys)
        print(f"    {lab:>13}: {b:+.3f}*log q  R2={r2:.3f}  vals={ys}")


allrows = {}
for N in (8, 12, 16):
    allrows[N] = table(N)
    report(allrows[N], N)

print("\n=== N-STABILITY (per q, strata / deep / shallow) ===")
for q in QS:
    parts = []
    for N in (8, 12, 16):
        d = load(q, N)
        if d:
            parts.append(f"N{N}={[c['count'] for c in d['combined_strata']]}"
                         f" d={d['deep_count_re_lt_0.4']} s={d['shallow_count_re_ge_0.4']}")
    if parts:
        print(f"  q={q:>2}: " + "  ||  ".join(parts))

json.dump({str(k): v for k, v in allrows.items()},
          open(D / "routeb_summary.json", "w"), indent=2)
print("\nwrote routeb_summary.json")
