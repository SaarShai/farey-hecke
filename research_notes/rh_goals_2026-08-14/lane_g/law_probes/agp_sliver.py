#!/usr/bin/env python3
"""
agp_sliver.py -- LANE G: count the UNCOUNTED sliver Re in (0.487, 1/2).

LAW_SELFBOUND_TRACE.md sec.5.1 offers two explanations for the mass-balance
deficit; the WINDING-BLINDNESS alternative says the missing Poisson mass sits in
poles the routeb winding probe never looked at, namely the sliver
Re in (0.487, 1/2) (its poles are the shallowest, so each absorbs close to the
full 2*pi).  This probe measures that stratum's count directly.

METHOD.  Exactly routeb_deepcount.py's shared-edge argument-principle winding,
reusing that module's Evaluator and adaptive argument walker unchanged, with the
ONLY change being the vertical grid:

        GRID_RE = [0.487, 0.494, 0.4985]      (two extra strata)

instead of [0.023, ..., 0.487].  The right edge stops at 0.4985, strictly inside
Re < 1/2, so on-line zeros (Re = 1/2 exactly) are never enclosed and never sat on.
Same window Im in [2,12], same both-sign-sector sum, same N convention.

RIGOR LABEL: identical to routeb_deepcount.py -- NON-RIGOROUS PROBE (midpoint
float evaluation, float arg-unwrap winding with half-turn guard).  Watch
min_absdet_on_contours: a small value next to the critical line means the
contour ran close to an on-line zero and the integer is not to be trusted.

No existing file is modified; output goes to agp_sliver_q{q}_N{N}.json.

Run: /Users/za/miniforge3/envs/pari-arb/bin/python3 agp_sliver.py Q [--N 16]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import routeb_deepcount as RB                                        # noqa: E402
from flint import ctx                                                # noqa: E402

GRID_RE = [0.487, 0.494, 0.4985]


def run(q, N):
    ctx.prec = RB.PREC
    t0 = time.time()
    ev = RB.Evaluator(q, N)
    warnings = []
    per_sign = {}
    T1, T2 = RB.T1, RB.T2

    for sign in RB.SIGNS:
        dV = []
        for c in GRID_RE:
            def fv(t, c=c, sign=sign):
                return ev(sign, c, T1 + t * (T2 - T1))
            n_init = max(4, int(round((T2 - T1) / RB.INIT_STEP_V)))
            tot, _ = RB._adaptive_arg_walk(fv, None, None, n_init, warnings,
                                           f"V sign={sign} Re={c}")
            dV.append(tot)

        H = {}
        for T, name in ((T1, "H1"), (T2, "H2")):
            cum = [0.0]
            for j in range(len(GRID_RE) - 1):
                a, b = GRID_RE[j], GRID_RE[j + 1]

                def fh(t, a=a, b=b, T=T, sign=sign):
                    return ev(sign, a + t * (b - a), T)
                n_init = max(4, int(round((b - a) / RB.INIT_STEP_H)))
                seg, _ = RB._adaptive_arg_walk(fh, None, None, n_init, warnings,
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
        print(f"[q={q} N={N} sign={sign}] sliver cells="
              f"{[c['count'] for c in cells]} raw="
              f"{[round(c['winding_raw'],4) for c in cells]} "
              f"calls={ev.calls} t={time.time()-t0:.0f}s", flush=True)

    combined = []
    for j in range(len(GRID_RE) - 1):
        tot = sum(per_sign[str(s)]["cells"][j]["count"] for s in RB.SIGNS)
        maxres = max(per_sign[str(s)]["cells"][j]["residual"] for s in RB.SIGNS)
        combined.append({"re_lo": GRID_RE[j], "re_hi": GRID_RE[j + 1],
                         "count": tot, "max_residual": maxres})

    out = {"probe": "agp_sliver", "q": q, "N": N, "n_head": 4,
           "prec_bits": RB.PREC,
           "builder": ("zeta_cert_rosen_even.py" if q % 2 == 0
                       else "zeta_cert_rosen.py"),
           "rigor_label": RB.__doc__.split("RIGOR LABEL:")[1].split("Usage")[0].strip(),
           "window": {"im": [T1, T2], "re_grid": GRID_RE},
           "signs": list(RB.SIGNS), "per_sign": per_sign,
           "combined_strata": combined,
           "sliver_count_re_in_0487_0498": sum(c["count"] for c in combined),
           "det_calls": ev.calls,
           "min_absdet_on_contours": ev.min_abs,
           "min_absdet_at": ev.min_at,
           "warnings": warnings, "n_warnings": len(warnings),
           "wall_seconds": time.time() - t0}
    p = HERE / f"agp_sliver_q{q}_N{N}.json"
    p.write_text(json.dumps(out, indent=2) + "\n")
    print(f"[q={q} N={N}] DONE sliver_total={out['sliver_count_re_in_0487_0498']} "
          f"min|det|={ev.min_abs:.3e} wall={out['wall_seconds']:.0f}s -> {p.name}",
          flush=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("q", type=int)
    ap.add_argument("--N", type=int, default=16)
    a = ap.parse_args()
    run(a.q, a.N)
