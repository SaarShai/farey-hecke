#!/usr/bin/env python3
"""
Probe U1-sup -- the numeric guard for LAW obligation U1.

Question: is  sup_{s in dU} |Z_{G_q}(s)|  visibly bounded in q, where
U = D(s_inf, 1/4) and s_inf = 0.25 + 7.0673625708673465i?

Z_{G_q}(s) is NOT computable from its Euler product at Re s = 1/4 (the
product diverges).  The repo's only in-strip evaluator is the certified
Rosen/MMS transfer-operator determinant
    det(1 - L_{s,q}^{sign}),  sign = +/-1  (the two P-symmetric sectors),
whose product over the two sectors is the object identified with
Z_{G_q}(s) by the R5 chain (q=5) / U4 (general q, still a GAP).  We use it
as a PROXY and report the sector determinants separately as well as their
product.  NON-RIGOROUS: midpoint evaluation of the Arb-ball builder, no
winding certificate, no ball radii.

Also evaluated at two points with Re s > 1 where the truncated Selberg
Euler product IS available (probe_t2_shape), so the proxy's normalization
against Z can be read off rather than assumed.

Usage:  python3 probe_u1_sup.py [--N 32] [--out u1_sup.json]
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
import sys
import time
from pathlib import Path

REPO = Path("/Users/za/Documents/farey-hecke")
sys.path.insert(0, str(REPO / ".worktrees/aletheia-restore/code"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import zeta_cert_rosen_even as E  # noqa: E402
from flint import acb, arb, ctx  # noqa: E402

import probe_t2_shape as T2  # noqa: E402

S_INF = complex(0.25, 7.0673625708673465)
R_U = 0.25


def det_mid(q: int, s: complex, N: int, sign: int) -> complex:
    sb = acb(arb(s.real), arb(s.imag))
    v = E.cert_det_complex_mid(sb, N, sign, q, n_head=4)
    return complex(float(v.real), float(v.imag))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=32)
    ap.add_argument("--qs", default="12,16,22,30")
    ap.add_argument("--npts", type=int, default=8)
    ap.add_argument("--out", default="u1_sup.json")
    a = ap.parse_args()
    ctx.prec = 400

    qs = [int(x) for x in a.qs.split(",")]
    bd = [S_INF + R_U * cmath.exp(2j * math.pi * j / a.npts) for j in range(a.npts)]
    pts = [("centre", S_INF)] + [(f"dU_{j}", z) for j, z in enumerate(bd)]
    # two Euler-product-accessible control points
    pts += [("ctrl_2.0", complex(2.0, 0.0)),
            ("ctrl_1.5+7.07i", complex(1.5, 7.0673625708673465))]

    doc = {"N": a.N, "s_inf": [S_INF.real, S_INF.imag], "radius": R_U, "rows": []}
    for q in qs:
        lam = 2.0 * math.cos(math.pi / q)
        cl = T2.enumerate_classes(lam, q, 9.0)
        t0 = time.time()
        for name, s in pts:
            row = {"q": q, "point": name, "re": s.real, "im": s.imag}
            for sign in (+1, -1):
                try:
                    v = det_mid(q, s, a.N, sign)
                    row[f"det{sign:+d}"] = [v.real, v.imag]
                    row[f"abs{sign:+d}"] = abs(v)
                except Exception as exc:  # noqa: BLE001
                    row[f"det{sign:+d}"] = None
                    row[f"err{sign:+d}"] = repr(exc)[:200]
            if row.get("abs+1") is not None and row.get("abs-1") is not None:
                row["abs_product"] = row["abs+1"] * row["abs-1"]
            if s.real > 1.0:
                row["euler_abs"] = abs(T2.selberg_trunc(cl, s, 6.0))
            doc["rows"].append(row)
            print(f"q={q:3d} {name:16s} s={s.real:.6f}{s.imag:+.6f}i  "
                  f"|det+|={row.get('abs+1', float('nan')):.6e}  "
                  f"|det-|={row.get('abs-1', float('nan')):.6e}  "
                  f"prod={row.get('abs_product', float('nan')):.6e}  "
                  f"euler={row.get('euler_abs', float('nan'))}", flush=True)
        print(f"  q={q} wall={time.time()-t0:.0f}s", flush=True)

    # summary: sup over dU per q
    summ = {}
    for q in qs:
        vals_p = [r["abs+1"] for r in doc["rows"]
                  if r["q"] == q and r["point"].startswith("dU_") and r.get("abs+1")]
        vals_pr = [r["abs_product"] for r in doc["rows"]
                   if r["q"] == q and r["point"].startswith("dU_") and r.get("abs_product")]
        summ[str(q)] = dict(sup_abs_plus=max(vals_p) if vals_p else None,
                            min_abs_plus=min(vals_p) if vals_p else None,
                            sup_abs_product=max(vals_pr) if vals_pr else None,
                            min_abs_product=min(vals_pr) if vals_pr else None)
    doc["summary"] = summ
    print("\n=== sup over dU ===")
    for q in qs:
        r = summ[str(q)]
        print(f"  q={q:3d}  sup|det+|={r['sup_abs_plus']:.6e}  min|det+|={r['min_abs_plus']:.6e}  "
              f"sup|det+ det-|={r['sup_abs_product']:.6e}  min={r['min_abs_product']:.6e}")

    with open(a.out, "w") as f:
        json.dump(doc, f, indent=1, default=str)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
