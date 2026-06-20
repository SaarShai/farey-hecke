"""
run_resonance_g7.py
===================
G_7 even-sector (mms+) resonance map -- the q=7 analogue of run_resonance_geometry.py
(which mapped G_5).  TEST: does the non-arithmetic Hecke surface G_7 ALSO produce
a SCATTERED even-resonance cloud (like G_5: Re-std ~0.030), or do its resonances
line up (like arithmetic q=3: Re=1/4, std ~1e-14)?  If G_7 scatters too, the
"cloud vs line" arithmeticity signature holds across TWO non-arith surfaces.

Engine: generalized certified Arb engine zeta_cert_rosen.py (q parameter).
VALIDATED on q=5 first (selfcheck_q5 + reproduces the q=5 even resonance
s=0.453895+5.763537i |det|=7.5e-16).  q=7 odd sanity anchor confirmed: on-line
odd Maass zeros at r=5.922, 9.186, 10.229 (|det(1-L-)| ~ 1e-8).

PIPELINE (per resonance):
  (A) certified |det(1-L+_s)| surface over Re in [0.1,0.49], Im in [3,17]
      (coarse N for the surface, then refine);
  (B) Newton-pin each coarse minimum (single complex var, det holomorphic off-line);
  (C) N-stability: keep s with |det| < 1e-5 AND (re,im) stable from N=22 to N=28;
  (D) Re-spread (std, range) of the kept set; compare to G_5 (0.030) / q=3 (1e-14).

Output: code/out/resonance_g7.json (numpy/flint-safe).
"""
from __future__ import annotations
import json
import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from flint import acb, arb, ctx

import zeta_cert_rosen as Z

ctx.prec = 400
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out",
                   "resonance_g7.json")

# q=7 odd on-line Maass anchors (confirmed this run, for interleaving reference).
ODD_R_Q7 = [5.92198, 9.18571, 10.22917]
# G_5 even resonance reference (from code/out/resonance_geometry.json).
G5_RE_STD = 0.029986
G5_RE_RANGE = 0.085453


def _san(o):
    if isinstance(o, dict):
        return {k: _san(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_san(v) for v in o]
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.complexfloating, complex)):
        return {"re": float(o.real), "im": float(o.imag)}
    return o


def atomic_dump(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(_san(obj), f, indent=2)
    os.replace(tmp, path)


def absmid(q, re, im, N, sign):
    return Z.cert_absdet_mid(acb(arb(float(re)), arb(float(im))), N, sign, q, 4)


def newton_locate(q, re0, im0, N, sign, iters=40, hfd=1e-6):
    """2D complex Newton on certified midpoint det (holomorphic off-line)."""
    s = complex(re0, im0)
    f = lambda z: Z.cert_det_complex_mid(
        acb(arb(z.real), arb(z.imag)), N, sign, q, 4)
    fs = f(s)
    for it in range(iters):
        fp = (f(s + hfd) - f(s - hfd)) / (2 * hfd)
        if fp == 0:
            break
        snew = s - fs / fp
        if snew.real >= 0.5:
            snew = complex(0.49, snew.imag)
        if snew.real <= 0.0:
            snew = complex(0.01, snew.imag)
        fnew = f(snew)
        if abs(snew - s) < 1e-13 or abs(fnew) < 1e-18:
            s, fs = snew, fnew
            break
        s, fs = snew, fnew
    return s.real, s.imag, abs(fs)


def main():
    t0 = time.time()
    out = {
        "objective": "G_7 even-sector (mms+) resonance map: does non-arith G_7 "
                     "scatter in Re like G_5, or line up like arith q=3?",
        "backend": Z.BACKEND, "prec_bits": 400, "q": 7,
        "engine": "generalized certified Arb engine zeta_cert_rosen.py "
                  "(validated on q=5: selfcheck_q5 max-diff 0, reproduces q=5 "
                  "even resonance s=0.453895+5.763537i |det|=7.5e-16).",
        "q7_odd_online_anchor": {
            "note": "on-line odd Maass zeros confirm operator correctness",
            "zeros_r": ODD_R_Q7,
            "absdet_at_zeros": [1.91e-08, 5.42e-09, 3.63e-08],
        },
        "g5_reference": {"re_std": G5_RE_STD, "re_range": G5_RE_RANGE,
                         "n": 8, "verdict": "scattered cloud"},
        "q3_reference": {"re": 0.25, "re_std": 6.5e-14,
                         "verdict": "rigid line Re=1/4 (zeta zeros)"},
    }
    log = []

    def dump():
        out["log"] = log
        out["wall_seconds"] = time.time() - t0
        atomic_dump(out, OUT)

    # ---- (A) certified |det(1-L+)| surface, coarse N for the surface ----
    # Re band: off-line strip; Im band: q=7 even resonance window (a bit above
    # the odd band since lambda=1/4+r^2 grows; cover [3,17] like G_5).
    N_SURF = 14
    RE = np.linspace(0.12, 0.48, 10)        # off-line Re band
    IM = np.linspace(3.0, 17.0, 141)        # 0.1 spacing in Im to catch dips
    log.append(f"q7 even surface: N={N_SURF} dim={5*N_SURF} grid "
               f"{len(RE)}x{len(IM)} Re[{RE[0]:.2f},{RE[-1]:.2f}] "
               f"Im[{IM[0]:.1f},{IM[-1]:.1f}]")
    grid = np.empty((len(RE), len(IM)))
    for a, re in enumerate(RE):
        for b, im in enumerate(IM):
            try:
                grid[a, b] = absmid(7, re, im, N_SURF, +1)
            except Exception:
                grid[a, b] = 9.99
        print(f"[g7 surf] Re={re:.3f} min|det|={grid[a].min():.3e} "
              f"({time.time()-t0:.0f}s)", flush=True)
        log.append(f"surf Re={re:.3f} min={grid[a].min():.3e}")
        dump()
    med = float(np.median(grid))
    out["surface"] = {
        "N_surf": N_SURF, "RE": [float(x) for x in RE],
        "IM": [float(x) for x in IM], "median": med,
        "min": float(grid.min()), "max": float(grid.max()),
        "absdet": [[float(v) for v in row] for row in grid],
    }
    dump()

    # ---- (B) seed Newton from grid points below a generous threshold ----
    thr = min(0.5 * med, 0.45)
    seeds = []
    for a in range(len(RE)):
        for b in range(len(IM)):
            if grid[a, b] < thr:
                seeds.append((float(RE[a]), float(IM[b])))
    log.append(f"surface median={med:.3e}; {len(seeds)} seeds below {thr:.3f}")
    print(f"[g7] median|det|={med:.3e}; {len(seeds)} Newton seeds", flush=True)

    # ---- (B/C) Newton-pin + N-stability (N=22 then N=28) ----
    g7 = []
    for (re0, im0) in seeds:
        try:
            re, im, fm = newton_locate(7, re0, im0, 22, +1)
            if not (fm < 1e-5 and 0.05 < re < 0.49 and 3.0 < im < 17.0):
                continue
            # dedup against already-found
            if any(abs(re - z["re"]) < 0.01 and abs(im - z["im"]) < 0.03
                   for z in g7):
                continue
            re2, im2, fm2 = newton_locate(7, re0, im0, 28, +1)
            stable = bool(abs(re - re2) < 2e-3 and abs(im - im2) < 2e-3
                          and fm2 < 1e-4)
            g7.append({"re": re, "im": im, "absdet": fm,
                       "re_N28": re2, "im_N28": im2, "absdet_N28": fm2,
                       "N_stable": stable})
            print(f"[g7] s={re:.5f}+{im:.5f}i |det|={fm:.1e} "
                  f"N28:|det|={fm2:.1e} Nstable={stable}", flush=True)
            dump()
        except Exception as e:
            log.append(f"g7 pin ({re0:.3f},{im0:.3f}) EXC {e!r}")
    g7.sort(key=lambda z: z["im"])
    out["g7_even_resonances"] = g7

    # ---- (D) Re-spread statistics ----
    def stats(zs):
        res = [z["re"] for z in zs]
        if not res:
            return {"n": 0}
        return {"n": len(res), "re_mean": float(np.mean(res)),
                "re_std": float(np.std(res)), "re_min": float(min(res)),
                "re_max": float(max(res)), "re_range": float(max(res) - min(res)),
                "im_list": [float(z["im"]) for z in zs],
                "re_list": [float(z["re"]) for z in zs]}

    g7_stable = [z for z in g7 if z["N_stable"]]
    st_all = stats(g7)
    st_stable = stats(g7_stable)
    out["verdict"] = {
        "g7_all_geometry": st_all,
        "g7_stable_geometry": st_stable,
        "g5_reference_re_std": G5_RE_STD,
        "g5_reference_re_range": G5_RE_RANGE,
        "q3_reference_re_std": 6.5e-14,
        "interpretation": (
            "If g7 re_std is O(0.01-0.05) (comparable to G_5 0.030) and re_range "
            "is wide, then G_7 ALSO SCATTERS -> arithmeticity signature (cloud "
            "for non-arith vs line for arith) holds across TWO non-arith surfaces."
        ),
    }
    # explicit comparison verdict
    n_st = st_stable.get("n", 0)
    if n_st >= 3:
        std = st_stable["re_std"]
        rng = st_stable["re_range"]
        if std > 1e-3:
            out["verdict"]["call"] = (
                f"G_7 SCATTERS (re_std={std:.4f}, re_range={rng:.4f}); "
                f"NOT a line (q3 std ~1e-14). Signature CONFIRMED on 2nd "
                f"non-arith surface.")
        else:
            out["verdict"]["call"] = (
                f"G_7 resonances LINE UP (re_std={std:.2e}); surprising -- "
                f"behaves like arithmetic. Signature does NOT generalize.")
    else:
        out["verdict"]["call"] = (
            f"INCONCLUSIVE: only {n_st} N-stable even resonances found; "
            f"not enough for a spread statistic.")

    dump()
    print("\n=== VERDICT ===")
    print(json.dumps(_san(out["verdict"]), indent=2))
    print(f"\ndone ({time.time()-t0:.0f}s) -> {OUT}")
    return out


if __name__ == "__main__":
    main()
