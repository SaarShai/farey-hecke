#!/usr/bin/env python3
"""Route-B deep-resonance count: stratified zero counts of det(1-L_{s,sign})
for Hecke triangle groups G_q in a FIXED window, by argument-principle winding.

PRE-REGISTERED MEASUREMENT (see LAW_ROUTEB_DEEPCOUNT.md).  Window:
  Im s in [T1,T2] = [2,12],  Re s in (0.023, 0.487)  (subset of 0 < Re s < 1/2).

Method (shared-edge winding, the cost-saving device):
  * Evaluate det on a set of VERTICAL grid lines Re = c_j, j=0..J-1, tracking the
    unwrapped argument from Im=T1 to Im=T2 with adaptive bisection so that no
    consecutive pair moves the argument by more than THETA_MAX.
  * Evaluate det on the two HORIZONTAL edges Im=T1 and Im=T2 over the full Re
    span, again adaptively, storing the cumulative unwrapped argument at each
    grid abscissa c_j.
  * The winding number of the rectangle [c_j, c_{j+1}] x [T1,T2] (CCW) is then
        (1/2pi) * [ (H1[j+1]-H1[j]) + dV[j+1] + (H2[j]-H2[j+1]) - dV[j] ]
    where dV[j] is the total unwrapped arg change up the line Re=c_j.
  * Each vertical line is used twice (right edge of one cell, left edge of the
    next), so J lines + 2 horizontals give J-1 stratum counts.

Sign sectors: the transfer operator has sectors sign = +1 and sign = -1; the
resonance set of G_q is the union, so both are counted and summed.

RIGOR LABEL: NON-RIGOROUS PROBE.  Midpoint float evaluation of the Arb-ball
builders (`zeta_cert_rosen.py` odd q, `zeta_cert_rosen_even.py` even q); ctx.prec
is lowered for speed; NO certified enclosure of the boundary values and no
certified dim-tail.  The winding integers are float-unwrap integers with a
half-turn guard, not Arb winding certificates.  Adequate for a measurement /
kill-or-advance decision; NOT a proof.

Note on the determinant: raw det(1-L_s) = Z_S(s) * det(1-K)(s) with det(1-K)
zero-free on Re s > 0, so for ZERO COUNTING on 0 < Re s < 1/2 the raw
determinant counts exactly the Selberg-zeta zeros (resonances).

Usage:  routeb_deepcount.py Q [--N 8] [--tag base]
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
# vertical grid lines: strata boundaries.  0.4 is the pre-registered delta0=0.1
# shallow/deep cut.  Endpoints are pulled off 0 and 1/2 to avoid the trivial
# cusp/on-line structure.
GRID_RE = [0.023, 0.1, 0.2, 0.3, 0.4, 0.487]
SIGNS = (+1, -1)
PREC = 128
THETA_MAX = math.pi / 2.0      # max allowed |d arg| between consecutive samples
INIT_STEP_V = 0.125            # initial Im step on vertical lines
INIT_STEP_H = 0.02             # initial Re step on horizontal edges
MAX_DEPTH = 6                  # bisection depth cap


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


def _adaptive_arg_walk(f, p0, p1, n_init, warnings, label):
    """Track the unwrapped arg of f along the segment p0->p1 (both complex).

    Returns (total_delta_arg, n_points).  f takes a scalar t in [0,1] and returns
    the complex determinant value at p0 + t*(p1-p0).
    """
    ts = [i / n_init for i in range(n_init + 1)]
    vals = [f(t) for t in ts]
    total = 0.0
    npts = len(ts)
    for i in range(len(ts) - 1):
        total += _refine(f, ts[i], ts[i + 1], vals[i], vals[i + 1], 0,
                         warnings, label)
    return total, npts


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


def run_q(q, N, tag):
    ctx.prec = PREC
    t0 = time.time()
    ev = Evaluator(q, N)
    warnings = []
    per_sign = {}

    for sign in SIGNS:
        # --- vertical lines: total unwrapped arg change from T1 to T2
        dV = []
        for c in GRID_RE:
            def fv(t, c=c, sign=sign):
                return ev(sign, c, T1 + t * (T2 - T1))
            n_init = max(4, int(round((T2 - T1) / INIT_STEP_V)))
            tot, _ = _adaptive_arg_walk(fv, None, None, n_init, warnings,
                                        f"V sign={sign} Re={c}")
            dV.append(tot)

        # --- horizontal edges: cumulative unwrapped arg at each grid abscissa
        H = {}
        for T, name in ((T1, "H1"), (T2, "H2")):
            cum = [0.0]
            for j in range(len(GRID_RE) - 1):
                a, b = GRID_RE[j], GRID_RE[j + 1]

                def fh(t, a=a, b=b, T=T, sign=sign):
                    return ev(sign, a + t * (b - a), T)
                n_init = max(4, int(round((b - a) / INIT_STEP_H)))
                seg, _ = _adaptive_arg_walk(fh, None, None, n_init, warnings,
                                            f"{name} sign={sign} Re[{a},{b}]")
                cum.append(cum[-1] + seg)
            H[name] = cum

        cells = []
        for j in range(len(GRID_RE) - 1):
            loop = ((H["H1"][j + 1] - H["H1"][j]) + dV[j + 1]
                    + (H["H2"][j] - H["H2"][j + 1]) - dV[j])
            w = loop / (2 * math.pi)
            cells.append({"re_lo": GRID_RE[j], "re_hi": GRID_RE[j + 1],
                          "winding_raw": w, "count": int(round(w)),
                          "residual": abs(w - round(w))})
        per_sign[str(sign)] = {"dV": dV, "H1": H["H1"], "H2": H["H2"],
                               "cells": cells,
                               "total_count": sum(c["count"] for c in cells)}
        print(f"[q={q} N={N} sign={sign}] cells="
              f"{[c['count'] for c in cells]} calls={ev.calls} "
              f"t={time.time()-t0:.0f}s", flush=True)

    # ---- combined strata (both sign sectors summed)
    combined = []
    for j in range(len(GRID_RE) - 1):
        tot = sum(per_sign[str(s)]["cells"][j]["count"] for s in SIGNS)
        maxres = max(per_sign[str(s)]["cells"][j]["residual"] for s in SIGNS)
        combined.append({"re_lo": GRID_RE[j], "re_hi": GRID_RE[j + 1],
                         "count": tot, "max_residual": maxres})

    shallow = sum(c["count"] for c in combined if c["re_lo"] >= 0.4)
    deep = sum(c["count"] for c in combined if c["re_hi"] <= 0.4)

    out = {
        "q": q, "N": N, "n_head": 4, "prec_bits": PREC,
        "builder": ("zeta_cert_rosen_even.py" if q % 2 == 0
                    else "zeta_cert_rosen.py"),
        "rigor_label": ("NON-RIGOROUS PROBE: midpoint float eval of the Arb-ball "
                        "builder, reduced precision, float arg-unwrap winding "
                        "with half-turn guard; no Arb winding certificate"),
        "window": {"im": [T1, T2], "re_grid": GRID_RE},
        "theta_max": THETA_MAX, "max_depth": MAX_DEPTH,
        "signs": list(SIGNS),
        "per_sign": per_sign,
        "combined_strata": combined,
        "shallow_count_re_ge_0.4": shallow,
        "deep_count_re_lt_0.4": deep,
        "total_count": shallow + deep,
        "det_calls": ev.calls,
        "min_absdet_on_contours": ev.min_abs,
        "min_absdet_at": ev.min_at,
        "warnings": warnings,
        "n_warnings": len(warnings),
        "wall_seconds": time.time() - t0,
    }
    path = OUTDIR / f"routeb_deepcount_q{q}_N{N}{('_'+tag) if tag else ''}.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(f"[q={q} N={N}] DONE shallow={shallow} deep={deep} "
          f"calls={ev.calls} wall={out['wall_seconds']:.0f}s -> {path.name}",
          flush=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("q", type=int)
    ap.add_argument("--N", type=int, default=8)
    ap.add_argument("--tag", type=str, default="")
    a = ap.parse_args()
    run_q(a.q, a.N, a.tag)
