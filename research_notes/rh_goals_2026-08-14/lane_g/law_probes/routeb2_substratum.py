#!/usr/bin/env python3
"""Route-B FOLLOW-UP: is the [0.2,0.3) sub-stratum growth real or a truncation
artifact?  Adapted copy of `routeb_deepcount.py` (originals untouched); only the
vertical grid is made selectable, so a sub-stratum re-measurement at high N costs
half (or less) of a full-grid run.

=====================================================================
PRE-REGISTRATION -- written before any N=16/N=20 number was computed.
=====================================================================
Everything is inherited unchanged from `routeb_deepcount.py`: window
Im s in [2,12]; strata boundaries drawn from the SAME list
[0.023, 0.1, 0.2, 0.3, 0.4, 0.487]; same shared-edge argument-principle winding;
same THETA_MAX = pi/2 adaptive bisection to depth 6; same PREC = 128; both sign
sectors summed; same builders `zeta_cert_rosen(.py|_even.py)` used unmodified via
`cert_det_complex_mid`; same interpreter /Users/za/.venvs/farey-rh/bin/python.

THREAD 1 -- [0.2,0.3) and [0.3,0.4) at N=16 (and N=20 where affordable),
            q in {7, 9, 11, 12, 15}.
  REAL     if the [0.2,0.3) count at N=16 EQUALS the N=12 count for every tested
           q, AND the log-q slope of [0.2,0.3) over the tested q stays positive.
  ARTIFACT if counts DROP at higher N and the log-q slope collapses toward 0
           (|slope| small / sign lost), as happened to the whole deep count
           between N=8 and N=12.
  MIXED    if some q move and others do not, or the slope stays positive but the
           counts are not N-stable.

THREAD 2 -- q=12 deep count at N=20 (deep grid, Re in [0.023,0.4]).
  Deep was 8 -> 6 -> 5 at N = 8/12/16.  STABILISED if N=20 reads 5; STILL
  DRIFTING if it reads <= 4 (or moves up).

CONSEQUENCE (pre-registered, so the reading is not chosen after the fact):
  If REAL, the delta0 = 0.1 cut is load-bearing: the deep bound candidate
  ~1.4 per unit height holds only at delta0 = 0.1, and at delta0 = 0.2 (cut at
  Re < 0.3) the surviving count is what must be quoted -- report the delta0=0.2
  count and its log-q slope as the revised candidate.
  If ARTIFACT, the deep total stays flat for the right reason and the ~1.4
  candidate is unchanged, with delta0 = 0.2 giving a SMALLER constant.

BUDGET: any single (q, N) cell over ~25 min wall is killed and recorded as
SKIPPED-BUDGET.

RIGOR LABEL: NON-RIGOROUS PROBE (identical caveats to routeb_deepcount.py):
midpoint float evaluation of the Arb-ball builders at reduced precision, float
arg-unwrap winding with a half-turn guard, no certified enclosure and no
certified dim-tail.  Measurement only; not a proof.

Usage:  routeb2_substratum.py Q --N 16 [--grid sub|deep|full]
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
T1, T2 = 2.0, 12.0
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
    path = OUTDIR / (f"routeb2_substratum_q{q}_N{N}_{grid_name}"
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
