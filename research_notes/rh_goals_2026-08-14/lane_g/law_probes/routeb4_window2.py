#!/usr/bin/env python3
"""Route-B GAP M3 (t0-uniformity): repeat the deep/shallow stratified resonance
count in a SECOND spectral window.  Adapted copy of `routeb2_substratum.py`
(originals untouched).  DIFF vs routeb2_substratum.py, in full:
  (1) T1, T2 = 2.0, 12.0   ->   T1, T2 = 12.0, 22.0
  (2) receipt filename stem `routeb2_substratum_q...` -> `routeb4_window2_q...`
Nothing else changed: same GRIDS, same SIGNS, same PREC = 128, same
THETA_MAX = pi/2 adaptive bisection to depth 6, same INIT_STEP_V/H, same
shared-edge argument-principle winding, same builders
`zeta_cert_rosen(.py|_even.py)` used unmodified via `cert_det_complex_mid`,
same interpreter /Users/za/.venvs/farey-rh/bin/python.

=====================================================================
PRE-REGISTRATION -- written before any window-2 number was computed.
=====================================================================
WINDOW 2 = Im s in [12, 22]: the adjacent decade, same height 10 as window 1
(Im s in [2,12], LAW_ROUTEB_DEEPCOUNT.md).  Deep = Re s < 0.4 (delta0 = 0.1),
grid `deep` = [0.023, 0.1, 0.2, 0.3, 0.4].  Groups q = 7, 9, 11, 12, 15 at
N = 12; N = 16 spot-check at q = 9 and q = 12.

Window 1 result under test: deep count FLAT at 6-7 for q >= 7, fitted
6.652 - 0.130*log q, R^2 = 0.009.

  SUPPORTED   if the window-2 deep stratum count is again q-flat: the values lie
              in a constant band with no positive log-q trend, and the least
              squares log-q slope is statistically indistinguishable from 0 as
              in window 1 (R^2 small, |slope| small relative to the band).
  UNDERMINED  if deep counts GROW with q in window 2 (clear positive log-q slope
              carried by the deep stratum).
  INCONCLUSIVE otherwise, or if the counts are not N-stable.

THEORY NOTE (pre-registered so it is not an after-the-fact excuse): resonance
density grows with height (Weyl-type), so ABSOLUTE window-2 counts may exceed
window-1 counts.  The test is q-FLATNESS at fixed window, not equality with
window 1.  Higher Im may also need larger N for convergence: if q=9 disagrees
between N=12 and N=16, N is escalated before any number is trusted.

BUDGET: ~2.5 h total.  Any cell that would blow the budget is killed and
recorded as SKIPPED-BUDGET in the write-up.

RIGOR LABEL: NON-RIGOROUS PROBE (identical caveats to routeb_deepcount.py):
midpoint float evaluation of the Arb-ball builders at reduced precision, float
arg-unwrap winding with a half-turn guard, no certified enclosure and no
certified dim-tail.  Measurement only; not a proof.

Usage:  routeb4_window2.py Q --N 12 [--grid sub|deep|full]
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

from flint import acb, arb, ctx  # noqa: E402
import zeta_cert_rosen as ODD  # noqa: E402
import zeta_cert_rosen_even as EVEN  # noqa: E402

OUTDIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------- pre-registered
T1, T2 = 12.0, 22.0
GRIDS = {
    # sub-stratum re-measurement: [0.2,0.3) and [0.3,0.4) only
    "sub": [0.2, 0.3, 0.4],
    # full deep region (delta >= delta0 = 0.1)
    "deep": [0.023, 0.1, 0.2, 0.3, 0.4],
    # the original probe's grid
    "full": [0.023, 0.1, 0.2, 0.3, 0.4, 0.487],
}
SIGNS = (+1, -1)
PREC = 128
THETA_MAX = math.pi / 2.0
INIT_STEP_V = 0.125
INIT_STEP_H = 0.02
MAX_DEPTH = 6


def module_for(q):
    return EVEN if q % 2 == 0 else ODD


class Evaluator:
    def __init__(self, q, N, n_head=4):
        self.q, self.N, self.n_head = q, N, n_head
        self.mod = module_for(q)
        self.calls = 0
        self.min_abs = float("inf")
        self.min_at = None

    def __call__(self, sign, re, im):
        self.calls += 1
        s = acb(arb(re), arb(im))
        z = self.mod.cert_det_complex_mid(s, self.N, sign, self.q, n_head=self.n_head)
        a = abs(z)
        if a < self.min_abs:
            self.min_abs = a
            self.min_at = (re, im)
        return z


def _adaptive_arg_walk(f, n_init, warnings, label):
    ts = [i / n_init for i in range(n_init + 1)]
    vals = [f(t) for t in ts]
    total = 0.0
    for i in range(len(ts) - 1):
        total += _refine(f, ts[i], ts[i + 1], vals[i], vals[i + 1], 0,
                         warnings, label)
    return total, len(ts)


def _refine(f, ta, tb, va, vb, depth, warnings, label):
    d = cmath.phase(vb / va) if va != 0 else 0.0
    if abs(d) <= THETA_MAX or depth >= MAX_DEPTH:
        if abs(d) > THETA_MAX:
            warnings.append({"label": label, "t": [ta, tb], "darg": d,
                             "reason": "half-turn guard hit at MAX_DEPTH"})
        return d
    tm = 0.5 * (ta + tb)
    vm = f(tm)
    return (_refine(f, ta, tm, va, vm, depth + 1, warnings, label)
            + _refine(f, tm, tb, vm, vb, depth + 1, warnings, label))


def run_q(q, N, grid_name, tag):
    grid_re = GRIDS[grid_name]
    ctx.prec = PREC
    t0 = time.time()
    ev = Evaluator(q, N)
    warnings = []
    per_sign = {}

    for sign in SIGNS:
        dV = []
        for c in grid_re:
            def fv(t, c=c, sign=sign):
                return ev(sign, c, T1 + t * (T2 - T1))
            n_init = max(4, int(round((T2 - T1) / INIT_STEP_V)))
            tot, _ = _adaptive_arg_walk(fv, n_init, warnings,
                                        f"V sign={sign} Re={c}")
            dV.append(tot)

        H = {}
        for T, name in ((T1, "H1"), (T2, "H2")):
            cum = [0.0]
            for j in range(len(grid_re) - 1):
                a, b = grid_re[j], grid_re[j + 1]

                def fh(t, a=a, b=b, T=T, sign=sign):
                    return ev(sign, a + t * (b - a), T)
                n_init = max(4, int(round((b - a) / INIT_STEP_H)))
                seg, _ = _adaptive_arg_walk(fh, n_init, warnings,
                                            f"{name} sign={sign} Re[{a},{b}]")
                cum.append(cum[-1] + seg)
            H[name] = cum

        cells = []
        for j in range(len(grid_re) - 1):
            loop = ((H["H1"][j + 1] - H["H1"][j]) + dV[j + 1]
                    + (H["H2"][j] - H["H2"][j + 1]) - dV[j])
            w = loop / (2 * math.pi)
            cells.append({"re_lo": grid_re[j], "re_hi": grid_re[j + 1],
                          "winding_raw": w, "count": int(round(w)),
                          "residual": abs(w - round(w))})
        per_sign[str(sign)] = {"dV": dV, "H1": H["H1"], "H2": H["H2"],
                               "cells": cells,
                               "total_count": sum(c["count"] for c in cells)}
        print(f"[q={q} N={N} grid={grid_name} sign={sign}] cells="
              f"{[c['count'] for c in cells]} calls={ev.calls} "
              f"t={time.time()-t0:.0f}s", flush=True)

    combined = []
    for j in range(len(grid_re) - 1):
        tot = sum(per_sign[str(s)]["cells"][j]["count"] for s in SIGNS)
        maxres = max(per_sign[str(s)]["cells"][j]["residual"] for s in SIGNS)
        combined.append({"re_lo": grid_re[j], "re_hi": grid_re[j + 1],
                         "count": tot, "max_residual": maxres})

    out = {
        "q": q, "N": N, "grid": grid_name, "grid_re": grid_re,
        "n_head": 4, "prec_bits": PREC,
        "builder": ("zeta_cert_rosen_even.py" if q % 2 == 0
                    else "zeta_cert_rosen.py"),
        "rigor_label": ("NON-RIGOROUS PROBE: midpoint float eval of the Arb-ball "
                        "builder, reduced precision, float arg-unwrap winding "
                        "with half-turn guard; no Arb winding certificate"),
        "window": {"im": [T1, T2], "re_grid": grid_re},
        "theta_max": THETA_MAX, "max_depth": MAX_DEPTH,
        "signs": list(SIGNS),
        "per_sign": per_sign,
        "combined_strata": combined,
        "deep_count_re_lt_0.4": sum(c["count"] for c in combined
                                    if c["re_hi"] <= 0.4),
        "det_calls": ev.calls,
        "min_absdet_on_contours": ev.min_abs,
        "min_absdet_at": ev.min_at,
        "warnings": warnings,
        "n_warnings": len(warnings),
        "wall_seconds": time.time() - t0,
    }
    path = OUTDIR / (f"routeb4_window2_q{q}_N{N}_{grid_name}"
                     f"{('_'+tag) if tag else ''}.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"[q={q} N={N} grid={grid_name}] DONE cells="
          f"{[c['count'] for c in combined]} calls={ev.calls} "
          f"wall={out['wall_seconds']:.0f}s -> {path.name}", flush=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("q", type=int)
    ap.add_argument("--N", type=int, default=16)
    ap.add_argument("--grid", type=str, default="sub", choices=list(GRIDS))
    ap.add_argument("--tag", type=str, default="")
    a = ap.parse_args()
    run_q(a.q, a.N, a.grid, a.tag)
