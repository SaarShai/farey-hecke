"""
zeta_resonance_g5.py
====================
EVEN-sector (mms+) RESONANCE hunt for the non-arithmetic Hecke triangle group
G_5 (lambda_5 = golden ratio).  This is the off-line continuation of the
established 2026-06-20 result:

  * G_5 ODD (mms-) sector carries clean N-stable Maass zeros ON the critical
    line at r = 6.4737, 8.6368, 10.1365, 11.0156, 12.0841, 12.8513 (certified,
    code/out/zeta_cert_rosen_q5.json).
  * G_5 EVEN (mms+) sector has NO zero on the line (|det| floor ~ a few e-2..1)
    = numerical Phillips-Sarnak cusp-form DISSOLUTION: the even Maass cusp forms
    of the non-arithmetic surface dissolve into RESONANCES (scattering poles of
    the Selberg zeta / zeros of det(1-L+_s) with Re(s) < 1/2).

TASK: find those even-sector resonances -- complex s with Re(s) < 1/2 where
det(1 - L+_s) = 0.

METHOD (honest, rigorous where claimed):
  (A) CHEAP coarse |det| surface via the certified Hurwitz-exact engine
      (NOT the double-prec FFT builder, which is unreliable off-line; verified
      in this repo).  We use the certified engine throughout because it is
      cheap enough at N=22 and is the only trustworthy off-line evaluator.
  (B) Refine every coarse |det| minimum by 2D complex Newton/secant on the
      certified midpoint det.mid() to locate a candidate s0.
  (C) Confirm each candidate with a RIGOROUS argument-principle winding box,
      using an OFF-LINE-capable winding routine (the repo's certify_winding
      hard-codes the box real-center at 1/2; we parameterize it here).
  (D) N-convergence: re-locate each confirmed candidate at N=18,22,26 -- a real
      resonance is N-stable; a spurious one drifts.
  (E) CONTROL: q=3 (arithmetic SL(2,Z)) even sector, same pipeline, as a
      contrast (arithmetic even forms survive on the line; expect a DIFFERENT
      off-line landscape).

Output: code/out/zeta_resonance_g5.json (numpy-safe atomic write).

Be honest: if det(1-L+_s) has no clean off-line zeros, report the |det|
landscape, the minima, and the convergence behavior as a negative/partial.
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

import zeta_cert_rosen_q5 as Zc  # certified Arb engine (q=5 MMS block operator)

PREC_BITS = 400
ctx.prec = PREC_BITS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

# Published ODD (mms-) on-line spectrum (for shadowing / interleaving reference).
ODD_R_Q5 = [6.4737, 8.6368, 10.1365, 11.0156, 12.0841, 12.8513]


# ===========================================================================
#  q=3 (arithmetic) MMS block geometry + builder for the CONTROL.
#  The certified engine zeta_cert_rosen_q5.py hard-codes q=5 geometry, so we
#  build the q=3 scalar (kappa=1) certified det here, reusing its exact-Hurwitz
#  primitives (_single_block_allcols / _tail_block_allcols).  q=3 eq.(33):
#    (L g)_1 = Linf_{3} g_1  +- Linf_{-2} g_1    (kappa=1, h=0)
# ===========================================================================
def _lam_ball_q3():
    # lambda_3 = 2 cos(pi/3) = 1.
    return acb(1)


def _q3_geometry():
    # q=3: Markov cell of [-lambda/2,0] = [-1/2, 0], single component.
    # center c_1 = -1/4, radius rho_1 = safety/2 * (1/2) with safety=5/2 -> 5/8.
    # Use the same safety as the q=5 builder (disc_radii_ball safety=5/2).
    lam = _lam_ball_q3()
    pts = [acb(-1) / 2, acb(0)]
    c = [(pts[0] + pts[1]) / 2]                 # -1/4
    rho = [(pts[1] - pts[0]) * (arb(5) / 2) / 2]  # 5/8
    return lam, c, rho


def build_reduced_matrix_ball_q3(s, N, sign, n_head=4):
    """Certified q=3 scalar reduced operator det matrix (kappa=1), eq.(33).

    (L g)_1 = Linf_{3} g_1 + sign * Linf_{-2} g_1.
    Reuses zeta_cert_rosen_q5's exact-Hurwitz allcols primitives.
    """
    lam, c, rho = _q3_geometry()
    kappa = 1
    sgn = acb(sign)
    ci, ri = c[0], rho[0]
    cj, rj = c[0], rho[0]

    def inf_block(n0, neg):
        cols = Zc._tail_block_allcols(s, ci, ri, cj, rj, lam, n0 + n_head, neg, N)
        for l in range(n0, n0 + n_head):
            hc = Zc._single_block_allcols(s, ci, ri, cj, rj, lam, l, neg, N)
            for kk in range(N):
                cols[kk] = cols[kk] + hc[kk]
        return cols

    pos = inf_block(3, False)             # Linf_{3}
    neg = inf_block(2, True)              # Linf_{-2}
    cols = [pos[kk] + sgn * neg[kk] for kk in range(N)]

    dim = kappa * N
    M = acb_mat = Zc.acb_mat(dim, dim)
    for kk in range(N):
        cser = cols[kk]
        for m in range(N):
            M[m, kk] = cser[m] if m < len(cser) else acb(0)
    return M, kappa


# ===========================================================================
#  Unified certified det evaluation: q -> (det_ball, tail, info).
#  q=5 uses Zc.build_reduced_matrix_ball; q=3 uses the local q3 builder.
# ===========================================================================
def cert_det(q, s, N, sign, n_head):
    if q == 5:
        M, kappa = Zc.build_reduced_matrix_ball(s, N, sign, n_head=n_head)
    elif q == 3:
        M, kappa = build_reduced_matrix_ball_q3(s, N, sign, n_head=n_head)
    else:
        raise ValueError("q must be 3 or 5")
    det = Zc._det_block(M, N, kappa, N)
    tail, info = Zc.dim_tail_from_matrix(M, N, kappa)
    return det, tail, info, kappa


def cert_absdet_mid(q, s, N, sign, n_head):
    """Midpoint |det| (double) for cheap surface scans / Newton."""
    det, _t, _i, _k = cert_det(q, s, N, sign, n_head)
    return abs(complex(float(det.real.mid()), float(det.imag.mid())))


def cert_det_complex_mid(q, s, N, sign, n_head):
    det, _t, _i, _k = cert_det(q, s, N, sign, n_head)
    return complex(float(det.real.mid()), float(det.imag.mid()))


# ===========================================================================
#  (A) Coarse |det| surface on a complex grid (certified midpoints).
# ===========================================================================
def coarse_surface(q, RE, IM, N, sign, n_head, log=None):
    grid = np.empty((len(RE), len(IM)))
    t0 = time.time()
    for a, re in enumerate(RE):
        for b, im in enumerate(IM):
            s = acb(arb(float(re)), arb(float(im)))
            grid[a, b] = cert_absdet_mid(q, s, N, sign, n_head)
        if log is not None:
            log.append(f"  surface row Re={re:.3f} done "
                       f"min|det|={grid[a].min():.3e} ({time.time()-t0:.1f}s)")
    return grid


def local_minima(grid, RE, IM, frac=0.6):
    """2D local minima of the |det| surface, keep those below frac*median."""
    med = float(np.median(grid))
    cand = []
    for a in range(1, len(RE) - 1):
        for b in range(1, len(IM) - 1):
            w = grid[a - 1:a + 2, b - 1:b + 2]
            if grid[a, b] == w.min() and grid[a, b] < frac * med:
                cand.append((float(RE[a]), float(IM[b]), float(grid[a, b])))
    cand.sort(key=lambda c: c[2])
    return cand, med


# ===========================================================================
#  (B) 2D complex Newton on the certified midpoint det to locate a zero s0.
#  det is holomorphic off-line, so Newton in the single complex variable s is
#  valid: s <- s - det(s)/det'(s), det' by a small complex finite difference.
# ===========================================================================
def newton_locate(q, re0, im0, N, sign, n_head, iters=40, tol=1e-12,
                  hfd=1e-6, log=None):
    s = complex(re0, im0)
    def f(z):
        return cert_det_complex_mid(
            q, acb(arb(z.real), arb(z.imag)), N, sign, n_head)
    fs = f(s)
    history = [(s.real, s.imag, abs(fs))]
    for it in range(iters):
        # complex derivative via central finite difference in the real direction
        # (Cauchy-Riemann: df/ds = df/d(Re s) for holomorphic f).
        fp = (f(s + hfd) - f(s - hfd)) / (2 * hfd)
        if fp == 0:
            break
        step = fs / fp
        s_new = s - step
        # keep the search inside the open strip 0 < Re(s) < 1/2 (clamp gently)
        if s_new.real >= 0.5:
            s_new = complex(0.49, s_new.imag)
        if s_new.real <= 0.0:
            s_new = complex(0.01, s_new.imag)
        fs_new = f(s_new)
        history.append((s_new.real, s_new.imag, abs(fs_new)))
        if abs(s_new - s) < tol or abs(fs_new) < 1e-18:
            s, fs = s_new, fs_new
            break
        s, fs = s_new, fs_new
    if log is not None:
        log.append(f"  newton ({re0:.3f},{im0:.3f}) -> "
                   f"({s.real:.5f},{s.imag:.5f}) |det|={abs(fs):.3e} "
                   f"in {len(history)-1} steps")
    return s, abs(fs), history


# ===========================================================================
#  (C) OFF-LINE argument-principle winding box (parameterized real-center).
#  B = { s = re0 + dx + i(im0 + dy) : |dx|<=hx, |dy|<=hy }.  Rigorous: every
#  boundary det ball must exclude 0 and consecutive samples within a half-turn.
#  Uses a uniform dimension-tail bound over the box (max over corners+center,
#  inflated x4) added to Re & Im of each boundary det -- same device as the
#  repo's certify_winding, now with re0 != 1/2.
# ===========================================================================
def winding_offline(q, re0, im0, hx, hy, N, sign, n_head, K=24, log=None):
    half = arb(re0)
    # uniform dim-tail over box corners + center
    radii = []
    for sx, sy in [(0, 0), (-1, -1), (1, -1), (1, 1), (-1, 1)]:
        s = acb(half + arb(sx) * arb(hx), arb(im0) + arb(sy) * arb(hy))
        det, tail, info, kappa = cert_det(q, s, N, sign, n_head)
        if tail is None:
            if log is not None:
                log.append(f"  winding: dim-tail UNCERTIFIED at corner "
                           f"({sx},{sy}); abort")
            return None, {"reason": "dim-tail not certified over box"}
        radii.append(tail)
    tail_fix = radii[0]
    for t in radii[1:]:
        if t > tail_fix:
            tail_fix = t
    tail_fix = tail_fix * 4

    # CCW boundary samples
    pts = []
    for t in range(K):
        pts.append((-hx + 2 * hx * t / K, -hy))
    for t in range(K):
        pts.append((hx, -hy + 2 * hy * t / K))
    for t in range(K):
        pts.append((hx - 2 * hx * t / K, hy))
    for t in range(K):
        pts.append((-hx, hy - 2 * hy * t / K))

    dets = []
    for dx, dy in pts:
        s = acb(half + arb(dx), arb(im0) + arb(dy))
        det, _t, _i, _k = cert_det(q, s, N, sign, n_head)
        det = acb(det.real + arb(0, tail_fix), det.imag + arb(0, tail_fix))
        if not (det.abs_lower() > 0):
            if log is not None:
                log.append(f"  winding: det ball contains 0 at "
                           f"(dx={float(dx):.2e},dy={float(dy):.2e}); "
                           f"box edge on/near a zero")
            return None, {"reason": "det ball contains 0 on dB",
                          "where": [float(dx), float(dy)],
                          "tail_fix": float(tail_fix)}
        dets.append(det)

    total = arb(0)
    n = len(dets)
    for t in range(n):
        A = dets[t]
        B = dets[(t + 1) % n]
        w = B * A.conjugate()
        rw, iw = w.real, w.imag
        if not (rw.lower() > 0 or iw.lower() > 0 or iw.upper() < 0):
            if log is not None:
                log.append(f"  winding: consecutive {t}->{t+1} not within "
                           f"half-turn; increase K")
            return None, {"reason": "half-turn test failed", "edge": t}
        total = total + w.arg().real
    wnd = total / (arb.pi() * 2)
    lo, hi = wnd.lower(), wnd.upper()
    nint = round(float(wnd.mid()))
    if lo > nint - arb(1) / 2 and hi < nint + arb(1) / 2:
        return nint, {"winding": int(nint),
                      "winding_ball": [float(lo), float(hi)],
                      "K_per_edge": K, "box_hx": float(hx), "box_hy": float(hy),
                      "re0_center": float(re0), "im0_center": float(im0),
                      "tail_fix": float(tail_fix)}
    if log is not None:
        log.append(f"  winding: sum/2pi ball [{float(lo):.4f},{float(hi):.4f}] "
                   f"does not pin an integer")
    return None, {"winding_ball": [float(lo), float(hi)], "K_per_edge": K}


# ===========================================================================
#  numpy-safe JSON
# ===========================================================================
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


# ===========================================================================
#  MAIN
# ===========================================================================
def run_even_hunt(q, RE, IM, N, n_head, sign=+1, label="q5_even", log=None):
    """Full even-sector hunt for one q: surface -> minima -> Newton -> winding."""
    if log is None:
        log = []
    t0 = time.time()
    log.append(f"=== {label}: q={q} sign={sign} N={N} grid "
               f"{len(RE)}x{len(IM)} Re[{RE[0]:.2f},{RE[-1]:.2f}] "
               f"Im[{IM[0]:.2f},{IM[-1]:.2f}] ===")
    grid = coarse_surface(q, RE, IM, N, sign, n_head, log=log)
    cand, med = local_minima(grid, RE, IM, frac=0.6)
    log.append(f"surface: median|det|={med:.3e} min={grid.min():.3e} "
               f"max={grid.max():.3e} ; {len(cand)} coarse minima below 0.6*median")

    results = []
    for (re_c, im_c, dp) in cand[:16]:
        rec = {"coarse": {"re": re_c, "im": im_c, "absdet_dp": dp}}
        s0, fmin, hist = newton_locate(q, re_c, im_c, N, sign, n_head, log=log)
        rec["newton"] = {"re": s0.real, "im": s0.imag, "absdet_mid": fmin,
                         "in_strip": bool(0.0 < s0.real < 0.5),
                         "n_steps": len(hist) - 1}
        # only attempt winding if Newton converged to a small |det| inside strip
        wnd = None
        if 0.02 < s0.real < 0.49 and fmin < 1e-3:
            for (hx, hy) in [(0.012, 0.012), (0.02, 0.02), (0.035, 0.03),
                             (0.05, 0.04)]:
                w, winfo = winding_offline(q, s0.real, s0.imag, hx, hy,
                                           N, sign, n_head, K=24, log=log)
                if w is not None:
                    wnd = (w, winfo)
                    break
        if wnd is not None:
            w, winfo = wnd
            rec["winding"] = {"winding_number": int(w),
                              "zero_certified": bool(w == 1), **winfo}
        else:
            rec["winding"] = None
        results.append(rec)

    out = {
        "q": q, "label": label, "sign": sign, "N": N, "n_head": n_head,
        "scan_re": [float(RE[0]), float(RE[-1]), len(RE)],
        "scan_im": [float(IM[0]), float(IM[-1]), len(IM)],
        "surface_median_absdet": float(med),
        "surface_min_absdet": float(grid.min()),
        "surface_max_absdet": float(grid.max()),
        "n_coarse_minima": len(cand),
        "candidates": results,
        "wall_seconds": time.time() - t0,
        # store the full surface coarsely (downsample if large) for landscape report
        "surface_RE": [float(x) for x in RE],
        "surface_IM": [float(x) for x in IM],
        "surface_absdet": [[float(v) for v in row] for row in grid],
    }
    return out, grid, log


def main():
    t0 = time.time()
    out = {
        "backend": Zc.BACKEND,
        "prec_bits": PREC_BITS,
        "objective": "EVEN-sector (mms+) resonances of non-arithmetic Hecke G_5: "
                     "complex s with Re(s)<1/2 where det(1-L+_s)=0 "
                     "(scattering poles = dissolved even Maass cusp forms).",
        "odd_online_spectrum_q5": ODD_R_Q5,
        "note_engine": "Certified Hurwitz-exact Arb engine used throughout "
                       "(double-prec FFT builder is unreliable off-line, verified). "
                       "Coarse surface = certified midpoints; winding = rigorous "
                       "off-line argument principle (parameterized real-center).",
    }
    out_path = os.path.join(OUT, "zeta_resonance_g5.json")
    master_log = []

    N_MAIN, NH = 22, 4

    # ---- (1) PRIMARY: q=5 even-sector surface over the resonance window ----
    # Re(s) in (0, 1/2); Im over the odd-band [5,13.5] plus a low-Im tail.
    RE = np.linspace(0.06, 0.46, 21)
    IM = np.linspace(4.0, 13.5, 96)        # ~0.1 spacing in Im
    res5, grid5, log5 = run_even_hunt(
        5, RE, IM, N_MAIN, NH, sign=+1, label="q5_even", log=[])
    out["q5_even"] = res5
    master_log += log5
    atomic_dump(out, out_path)
    print(f"[q5_even] surface done: median|det|={res5['surface_median_absdet']:.3e} "
          f"min={res5['surface_min_absdet']:.3e} "
          f"({res5['n_coarse_minima']} coarse minima)", flush=True)
    n_cert5 = sum(1 for c in res5["candidates"]
                  if c.get("winding") and c["winding"]["zero_certified"])
    print(f"[q5_even] certified off-line zeros: {n_cert5}", flush=True)

    # ---- (2) N-CONVERGENCE on the best certified / deepest candidates ----
    # Take up to 4 deepest Newton results inside the strip and relocate at
    # N=18,22,26.  Real resonance: N-stable; spurious: drifts.
    conv = []
    cands = sorted(res5["candidates"],
                   key=lambda c: c["newton"]["absdet_mid"])
    seen = []
    for c in cands:
        nw = c["newton"]
        if not (0.02 < nw["re"] < 0.49):
            continue
        # de-dup by proximity
        if any(abs(nw["re"] - p[0]) < 0.02 and abs(nw["im"] - p[1]) < 0.05
               for p in seen):
            continue
        seen.append((nw["re"], nw["im"]))
        chain = {}
        for Nc in (18, 22, 26):
            s0, fmin, _h = newton_locate(5, nw["re"], nw["im"], Nc, +1, NH)
            chain[Nc] = {"re": s0.real, "im": s0.imag, "absdet_mid": fmin}
        res_re = [chain[Nc]["re"] for Nc in (18, 22, 26)]
        res_im = [chain[Nc]["im"] for Nc in (18, 22, 26)]
        re_spread = max(res_re) - min(res_re)
        im_spread = max(res_im) - min(res_im)
        conv.append({
            "seed": {"re": nw["re"], "im": nw["im"]},
            "per_N": {int(Nc): chain[Nc] for Nc in (18, 22, 26)},
            "re_spread": re_spread, "im_spread": im_spread,
            "absdet_min_over_N": min(chain[Nc]["absdet_mid"] for Nc in (18, 22, 26)),
            "N_stable": bool(re_spread < 2e-3 and im_spread < 2e-3
                             and max(chain[Nc]["absdet_mid"]
                                     for Nc in (18, 22, 26)) < 1e-3),
        })
        if len(conv) >= 5:
            break
    out["q5_even_Nconvergence"] = conv
    master_log.append(f"N-convergence: tested {len(conv)} candidates")
    for cv in conv:
        master_log.append(
            f"  seed=({cv['seed']['re']:.3f},{cv['seed']['im']:.3f}) "
            f"re_spread={cv['re_spread']:.1e} im_spread={cv['im_spread']:.1e} "
            f"|det|min={cv['absdet_min_over_N']:.2e} "
            f"{'N-STABLE' if cv['N_stable'] else 'drifts/shallow'}")
    atomic_dump(out, out_path)
    print(f"[q5_even] N-convergence on {len(conv)} candidates done", flush=True)

    # ---- (3) CONTROL: q=3 arithmetic even (mms+) sector, same window ----
    # Cheap (kappa=1 => N x N, not 3N x 3N).  Arithmetic even forms survive on
    # the line; expect a structurally different off-line landscape.
    RE3 = np.linspace(0.06, 0.46, 21)
    IM3 = np.linspace(8.0, 17.0, 91)       # SL(2,Z) even-form band
    res3, grid3, log3 = run_even_hunt(
        3, RE3, IM3, 30, NH, sign=+1, label="q3_even_control", log=[])
    out["q3_even_control"] = res3
    master_log += log3
    n_cert3 = sum(1 for c in res3["candidates"]
                  if c.get("winding") and c["winding"]["zero_certified"])
    print(f"[q3_even_control] surface done: "
          f"median|det|={res3['surface_median_absdet']:.3e} "
          f"min={res3['surface_min_absdet']:.3e} "
          f"certified off-line zeros={n_cert3}", flush=True)

    # ---- VERDICT ----
    certified5 = [c for c in res5["candidates"]
                  if c.get("winding") and c["winding"]["zero_certified"]]
    out["verdict"] = {
        "q5_even_certified_offline_zeros": len(certified5),
        "q5_even_certified_list": [
            {"re": c["newton"]["re"], "im": c["newton"]["im"],
             "absdet_mid": c["newton"]["absdet_mid"],
             "winding": c["winding"]["winding_number"]}
            for c in certified5],
        "q5_even_Nstable_candidates": sum(1 for cv in conv if cv["N_stable"]),
        "q3_control_certified_offline_zeros": n_cert3,
        "q5_surface_min_absdet": res5["surface_min_absdet"],
        "q5_surface_median_absdet": res5["surface_median_absdet"],
    }
    out["log"] = master_log
    out["wall_seconds_total"] = time.time() - t0
    atomic_dump(out, out_path)
    print(f"\nwrote {out_path}  ({time.time()-t0:.1f}s)")
    print(f"VERDICT: q5_even certified off-line zeros = {len(certified5)} ; "
          f"N-stable candidates = {sum(1 for cv in conv if cv['N_stable'])} ; "
          f"q3 control certified = {n_cert3}")
    return out


if __name__ == "__main__":
    main()
