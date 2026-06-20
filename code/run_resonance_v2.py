"""
run_resonance_v2.py
===================
Faster + wider + rigorous even-sector RESONANCE hunt for non-arithmetic Hecke
G_5, with a q=3 (modular) Riemann-zero resonance VALIDATION control.

Reuses the certified off-line machinery in zeta_resonance_g5.py (cert_det,
coarse_surface, newton_locate, winding_offline).  The double-prec FFT builder
was tested and DIVERGES off the line (rel err up to 0.8) -> certified Arb engine
used throughout; N=14 for locating surfaces (<=3e-3 vs N=22, 3x faster), N=22
for the rigorous winding certification.

Protocol:
  (P1) G_5 EVEN (mms+) wide certified |det| surface, N=14, Re in [-0.1,0.49],
       Im in [1,22].  Locate minima.
  (P2) Newton-refine the deepest minima (N=22); rigorous off-line winding box
       on each -> certified zero / no-zero.
  (P3) G_5 EVEN big-box argument-principle WINDING COUNT over the core region
       [0.05,0.49] x [5,13.5] (adaptive K) -> certified number of resonances.
  (C1) q=3 (arithmetic SL(2,Z)) RESONANCE VALIDATION: scan EVEN and ODD sectors
       off-line at the predicted modular resonances s = 1/4 + i*t_n/2, where
       t_n = {14.1347, 21.0220, 25.0109, 30.4249, 32.9351} are the first Riemann
       zeta zeros (resonances of the modular surface = zeros of zeta(2s)).
       Newton + winding each -> does the transfer-op det recover the zeta zeros?
  (C2) q=3 EVEN wide surface for the landscape contrast.

Output: code/out/resonance_v2.json  (atomic, numpy-safe, incremental).
"""
from __future__ import annotations
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from flint import acb, arb, ctx

import zeta_resonance_g5 as Zr
ctx.prec = 400

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
OUT_PATH = os.path.join(OUT, "resonance_v2.json")

# First nontrivial Riemann zeta zero heights -> modular-surface resonances at
# s = 1/4 + i t_n/2  (poles of scattering phi(s) = zeros of zeta(2s)).
RIEMANN_T = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062]
RIEMANN_RESONANCES = [(0.25, t / 2.0) for t in RIEMANN_T]


def cdet(q, s, N, sign):
    return Zr.cert_det_complex_mid(q, acb(arb(s.real), arb(s.imag)), N, sign, 4)


def newton_and_winding(q, re0, im0, sign, label, log, N_loc=22):
    """Newton-refine a candidate, then certify with off-line winding boxes."""
    s0, fmin, hist = Zr.newton_locate(q, re0, im0, N_loc, sign, 4, log=log)
    rec = {"label": label, "seed": [re0, im0],
           "newton": {"re": s0.real, "im": s0.imag, "absdet_mid": fmin,
                      "in_strip": bool(0.0 < s0.real < 0.5),
                      "n_steps": len(hist) - 1},
           "winding": None}
    if 0.02 < s0.real < 0.49 and fmin < 5e-3:
        for (hx, hy) in [(0.012, 0.012), (0.02, 0.02), (0.035, 0.03), (0.05, 0.05)]:
            w, winfo = Zr.winding_offline(q, s0.real, s0.imag, hx, hy,
                                          N_loc, sign, 4, K=28, log=log)
            if w is not None:
                rec["winding"] = {"winding_number": int(w),
                                  "zero_certified": bool(w == 1), **winfo}
                break
    # N-stability check (real resonance is N-stable)
    chain = {}
    for Nc in (16, 22, 28):
        sN, fN, _ = Zr.newton_locate(q, re0, im0, Nc, sign, 4)
        chain[Nc] = {"re": sN.real, "im": sN.imag, "absdet_mid": fN}
    res_re = [chain[Nc]["re"] for Nc in (16, 22, 28)]
    res_im = [chain[Nc]["im"] for Nc in (16, 22, 28)]
    rec["N_stability"] = {
        "per_N": {int(k): v for k, v in chain.items()},
        "re_spread": max(res_re) - min(res_re),
        "im_spread": max(res_im) - min(res_im),
        "absdet_max_over_N": max(chain[Nc]["absdet_mid"] for Nc in (16, 22, 28)),
        "N_stable": bool(max(res_re) - min(res_re) < 2e-3
                         and max(res_im) - min(res_im) < 2e-3
                         and max(chain[Nc]["absdet_mid"] for Nc in (16, 22, 28)) < 1e-3),
    }
    return rec


def bigbox_winding(q, re_lo, re_hi, im_lo, im_hi, sign, N, log, Kstart=40):
    """Certified zero COUNT inside the box via argument principle, adaptive K."""
    re0 = 0.5 * (re_lo + re_hi); im0 = 0.5 * (im_lo + im_hi)
    hx = 0.5 * (re_hi - re_lo);  hy = 0.5 * (im_hi - im_lo)
    for K in (Kstart, Kstart * 2, Kstart * 4):
        w, winfo = Zr.winding_offline(q, re0, im0, hx, hy, N, sign, 4, K=K, log=log)
        if w is not None:
            return {"zero_count": int(w), "K_per_edge": K,
                    "box": [re_lo, re_hi, im_lo, im_hi], **winfo}
    return {"zero_count": None, "box": [re_lo, re_hi, im_lo, im_hi],
            "reason": "winding did not certify (half-turn/dim-tail)", **(winfo or {})}


def gbox(q, rl, rh, il, ih, sign, N, K, log):
    """Certified zero count inside the box (single fixed K, no adaptive retry)."""
    re0 = 0.5 * (rl + rh); im0 = 0.5 * (il + ih)
    hx = 0.5 * (rh - rl); hy = 0.5 * (ih - il)
    t = time.time()
    w, info = Zr.winding_offline(q, re0, im0, hx, hy, N, sign, 4, K=K, log=log)
    return {"box": [rl, rh, il, ih], "zero_count": (int(w) if w is not None else None),
            "K_per_edge": K, "N": N, "secs": time.time() - t,
            "reason": info.get("reason"), "winding_ball": info.get("winding_ball")}


def main():
    t0 = time.time()
    out = {
        "backend": Zr.Zc.BACKEND, "prec_bits": 400,
        "objective": "Even-sector resonances of non-arith Hecke G_5 via certified "
                     "argument-principle zero COUNT, with q=3 modular Riemann-zero "
                     "resonance validation. Certified Arb engine throughout "
                     "(double-prec builder diverges off-line; winding-count detects "
                     "sharp zeros a grid would step over).",
        "odd_online_spectrum_q5": Zr.ODD_R_Q5,
        "riemann_resonances_pred": [{"re": r, "im": i, "t_n": 2 * i}
                                    for (r, i) in RIEMANN_RESONANCES],
    }
    log = []
    def dump():
        out["log"] = log; out["wall_seconds"] = time.time() - t0
        Zr.atomic_dump(out, OUT_PATH)

    # ===== (V) q=3 even COUNTING-METHOD validation: box [0.10,0.45]x[6,13] =====
    # contains modular resonances at Im=gamma_n/2 for gamma in {14.13,21.02,25.01}
    # => expect winding zero_count = 3.
    log.append("=== V: q=3 even counting validation (expect 3) ===")
    vbox = gbox(3, 0.10, 0.45, 6.0, 13.0, +1, 30, 48, log)
    out["q3_counting_validation"] = vbox
    print(f"[V] q=3 even box [0.10,0.45]x[6,13] zero_count={vbox['zero_count']} "
          f"(expect 3)  [{vbox['secs']:.1f}s]", flush=True)
    dump()

    # ===== (C1) q=3 Riemann-resonance point probe + winding certification =====
    log.append("=== C1: q=3 Riemann resonance point probe ===")
    q3_probe = {"even": [], "odd": []}
    for sec_name, sec in (("even", +1), ("odd", -1)):
        for (re_r, im_r) in RIEMANN_RESONANCES:
            d = cdet(3, complex(re_r, im_r), 30, sec)
            rec = {"pred_re": re_r, "pred_im": im_r, "t_n": 2 * im_r,
                   "absdet_at_pred": abs(d)}
            q3_probe[sec_name].append(rec)
        print(f"[C1] q=3 {sec_name}: |det| at Riemann preds = "
              f"{[float('%.2e'%r['absdet_at_pred']) for r in q3_probe[sec_name]]}",
              flush=True)
        dump()
    # certify the first two even resonances as simple zeros (winding=1)
    q3_even_cert = []
    for (re_r, im_r) in RIEMANN_RESONANCES[:2]:
        s0, fmin, _ = Zr.newton_locate(3, re_r, im_r, 30, +1, 4, log=log)
        wb = gbox(3, s0.real - 0.06, s0.real + 0.06, s0.imag - 0.25, s0.imag + 0.25,
                  +1, 30, 36, log)
        q3_even_cert.append({"t_n": 2 * im_r, "located": [s0.real, s0.imag],
                             "absdet_mid": fmin, "winding": wb["zero_count"],
                             "zero_certified": bool(wb["zero_count"] == 1)})
        dump()
    out["q3_riemann_resonance_probe"] = q3_probe
    out["q3_even_resonance_certified"] = q3_even_cert
    print(f"[C1] q=3 even resonances certified (winding=1): "
          f"{[c['zero_certified'] for c in q3_even_cert]}", flush=True)

    # ===== (P1) G_5 EVEN wide surface, N=14 (landscape + locating) =====
    log.append("=== P1: G_5 even (mms+) wide surface N=14 ===")
    RE = np.linspace(0.0, 0.49, 25)        # finer in Re to catch sharp zeros
    IM = np.linspace(2.0, 20.0, 73)        # ~0.25 spacing in Im
    grid5 = Zr.coarse_surface(5, RE, IM, 14, +1, 4, log=log)
    cand5, med5 = Zr.local_minima(grid5, RE, IM, frac=0.7)
    out["g5_even_surface"] = {
        "N": 14, "scan_re": [float(RE[0]), float(RE[-1]), len(RE)],
        "scan_im": [float(IM[0]), float(IM[-1]), len(IM)],
        "median_absdet": float(med5), "min_absdet": float(grid5.min()),
        "max_absdet": float(grid5.max()), "n_minima": len(cand5),
        "minima": [{"re": c[0], "im": c[1], "absdet": c[2]} for c in cand5[:25]],
        "surface_RE": [float(x) for x in RE], "surface_IM": [float(x) for x in IM],
        "surface_absdet": [[float(v) for v in row] for row in grid5],
    }
    log.append(f"G_5 even surface: median={med5:.3e} min={grid5.min():.3e} "
               f"max={grid5.max():.3e} ; {len(cand5)} minima<0.7*med")
    print(f"[P1] G_5 even surface min|det|={grid5.min():.3e} "
          f"median={med5:.3e} minima={len(cand5)}", flush=True)
    dump()

    # ===== (P2) G_5 EVEN certified COUNT over Im-bands (the headline number) =====
    log.append("=== P2: G_5 even big-box winding COUNT over Im bands ===")
    bands = [(0.0, 0.49, 4.0, 9.0), (0.0, 0.49, 9.0, 14.0),
             (0.0, 0.49, 14.0, 19.0)]
    g5_counts = []
    for (rl, rh, il, ih) in bands:
        bc = gbox(5, rl, rh, il, ih, +1, 22, 44, log)
        g5_counts.append(bc); dump()
        print(f"[P2] G_5 even band Re[{rl},{rh}] Im[{il},{ih}] "
              f"zero_count={bc['zero_count']} [{bc['secs']:.1f}s]", flush=True)
    out["g5_even_band_counts"] = g5_counts
    total_g5 = sum(b["zero_count"] for b in g5_counts if b["zero_count"] is not None)

    # ===== (P2b) Re-box any band whose winding was inconclusive (edge clipped) =====
    g5_rebox = []
    out["g5_even_band_rebox"] = g5_rebox            # assign FIRST so dumps persist it
    for b in g5_counts:
        if b["zero_count"] is None:
            rl, rh, il, ih = b["box"]
            for (lo, hi) in [(il + 0.2, ih - 0.2), (il + 0.35, ih - 0.05)]:
                try:
                    rb = gbox(5, rl, rh, lo, hi, +1, 22, 52, log)
                    g5_rebox.append(rb); dump()
                    if rb["zero_count"] is not None:
                        break
                except Exception as e:
                    log.append(f"  rebox [{lo},{hi}] EXC {e!r}"); dump()

    # ===== (P3) Bisect to localize + Newton-pin (robust: per-step try/except) =====
    log.append("=== P3: G_5 even localization ===")
    g5_located = []
    out["g5_even_localization"] = g5_located        # assign FIRST so dumps persist it
    for b in g5_counts:
        if b["zero_count"] and b["zero_count"] > 0:
            rl, rh, il, ih = b["box"]
            mid = 0.5 * (il + ih)
            for (lo, hi) in [(il, mid), (mid, ih)]:
                try:
                    sub = gbox(5, rl, rh, lo, hi, +1, 22, 44, log)
                    g5_located.append(sub); dump()
                except Exception as e:
                    log.append(f"  subbox [{lo},{hi}] EXC {e!r}"); dump()
            for (re_c, im_c, dp) in cand5:
                if il <= im_c <= ih and dp < 0.5 * med5:
                    try:
                        rec = newton_and_winding(5, re_c, im_c, +1,
                                                 f"g5even({re_c:.2f},{im_c:.2f})", log)
                        g5_located.append({"newton_pin": rec}); dump()
                    except Exception as e:
                        log.append(f"  newton_pin ({re_c:.2f},{im_c:.2f}) EXC {e!r}")
                        dump()

    # ===== (C2) q=3 EVEN wide surface (landscape contrast) =====
    log.append("=== C2: q=3 even wide surface ===")
    try:
        RE3 = np.linspace(0.10, 0.49, 18)
        IM3 = np.linspace(4.0, 16.0, 61)
        grid3 = Zr.coarse_surface(3, RE3, IM3, 30, +1, 4, log=log)
        cand3, med3 = Zr.local_minima(grid3, RE3, IM3, frac=0.7)
        out["q3_even_surface"] = {
            "N": 30, "scan_re": [float(RE3[0]), float(RE3[-1]), len(RE3)],
            "scan_im": [float(IM3[0]), float(IM3[-1]), len(IM3)],
            "median_absdet": float(med3), "min_absdet": float(grid3.min()),
            "n_minima": len(cand3),
            "minima": [{"re": c[0], "im": c[1], "absdet": c[2]} for c in cand3[:25]],
            "surface_RE": [float(x) for x in RE3], "surface_IM": [float(x) for x in IM3],
            "surface_absdet": [[float(v) for v in row] for row in grid3],
        }
        print(f"[C2] q=3 even surface min|det|={grid3.min():.3e} "
              f"median={med3:.3e} minima={len(cand3)}", flush=True)
        dump()
    except Exception as e:
        log.append(f"C2 q3 surface EXC {e!r}"); dump()

    # ===== VERDICT =====
    # classify Newton-pinned resonances: near-line (genuine dissolved-form
    # resonances, Re in (0.1,0.49)) vs near-Re=0 (generic spectral-radius zeros).
    pinned = []
    for x in g5_located:
        if "newton_pin" in x:
            nw = x["newton_pin"].get("newton", {})
            if nw.get("absdet_mid", 9) < 1e-6:
                pinned.append({"re": nw["re"], "im": nw["im"],
                               "absdet_mid": nw["absdet_mid"],
                               "near_line": bool(0.1 < nw["re"] < 0.49)})
    near_line = [p for p in pinned if p["near_line"]]
    near_zero = [p for p in pinned if not p["near_line"]]
    out["verdict"] = {
        "q3_counting_validation_count": vbox["zero_count"],
        "q3_counting_validation_pass": bool(vbox["zero_count"] == 3),
        "q3_even_riemann_absdet": [float('%.2e' % r["absdet_at_pred"])
                                   for r in q3_probe["even"]],
        "q3_even_resonances_certified": sum(1 for c in q3_even_cert
                                            if c["zero_certified"]),
        "g5_even_band_counts": [(b["box"], b["zero_count"]) for b in g5_counts],
        "g5_even_band_rebox": [(b["box"], b["zero_count"]) for b in g5_rebox],
        "g5_even_total_resonances_in_scan": total_g5,
        "g5_even_surface_min_absdet": float(grid5.min()),
        "g5_even_surface_median_absdet": float(med5),
        "g5_even_pinned_near_line": near_line,
        "g5_even_pinned_near_zero": near_zero,
        "g5_even_n_near_line_resonances": len(near_line),
    }
    dump()
    print(f"\nwrote {OUT_PATH} ({time.time()-t0:.1f}s)")
    print("VERDICT:", json.dumps(out["verdict"], indent=2, default=Zr._san))


if __name__ == "__main__":
    main()
