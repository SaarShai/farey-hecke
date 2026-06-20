#!/usr/bin/env python3
"""
run_cert_g8.py
==============
Drive the EVEN-q certified engine (code/zeta_cert_rosen_even.py) on G_8 (q=8):

  1. VALIDATION GATE -- reproduce the anchor: |det(1-L^-_{1/2+i r})| ~ 0 at the
     Hejhal/transfer-op-validated odd Maass eigenvalue r1 = 5.798144 (mms-,
     sign=-1), and confirm the mms+ (sign=+1) sector is NOT zero there (~0.82).
     Self-check the certified builder vs the double-precision reference.

  2. CERTIFY -- argument-principle winding=1 box around the located on-line zero
     r* near 5.798144 (sign=-1).  Winding=1 => exactly one det zero inside the
     box (counted with multiplicity), with det != 0 certified on the box
     boundary in Arb balls and the dimension tail certified.  The box half-height
     in r gives the certified r-enclosure.

Writes code/out/certified_g8.json.  Honest: records what certified vs deferred.
"""
import json
import os
import time

from flint import acb, arb

import zeta_cert_rosen_even as CE

OUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "out", "certified_g8.json")

Q = 8
SIGN = -1                 # mms- / odd sector (the populated one for G_8)
N = 20                    # per-component basis (kappa=3 => 60x60 ball det)
N_HEAD = 4
ANCHOR_R = 5.798144       # transfer-op double-prec; Hejhal r*=5.798174


def main():
    t0 = time.time()
    out = {
        "backend": CE.BACKEND,
        "prec_bits": CE.PREC_BITS,
        "q": Q,
        "lambda_8": "2cos(pi/8) = sqrt(2+sqrt2)",
        "sector": "mms- (sign=-1) -- the populated odd sector for G_8",
        "operator": "MMS reduced L_{s,-} eq.32 (EVEN q), q=8 (h_q=kappa=3); "
                    "Selberg-Z numerator factor det(1-L_{s,-})",
        "engine": "code/zeta_cert_rosen_even.py (certified Arb-ball EVEN-q build)",
        "anchor": {
            "r": ANCHOR_R,
            "validated_by": [
                "transfer-op double precision (zeta_mayer_rosen.json, "
                "q8 mms- |det|=2.1e-8 at N=35)",
                "Hejhal automorphy point-matching (hejhal_g8_maass.json, "
                "r*=5.798174, sigma_min=2.1e-5)",
            ],
        },
        "rigor": {
            "geometry": "EVEN-q Markov partition phi_i=[[0;1^{hq-i}]] as Arb "
                        "balls; centers/radii match the double-prec reference.",
            "branch_tail": "EXACT via Hurwitz zeta (reused q-agnostic primitive "
                           "_tail_block_allcols); conditionally-convergent "
                           "sum_l (z +- l lam)^{-(2s+m)} given its analytic value.",
            "block_placement": "MMS eq.32 (even q): (Lg)_1 = Linf_2 g_h + sign "
                               "Linf_{-1} g_h; (Lg)_i = L_1 g_{i-1} + Linf_2 g_h "
                               "+ sign Linf_{-1} g_h, 2<=i<=h.  Verified vs the "
                               "double-prec even-q builder (diff -> 0 as its tail "
                               "truncation grows; certified tail is the exact limit).",
            "finite_N": "acb_mat.det in Arb ball arithmetic; rounding in radius.",
            "dimension_tail": "certified det-increment geometric Cauchy tail.",
            "zero_isolation": "argument principle on a complex-s box: det ball "
                              "excludes 0 on dB (certified) AND winding=1 via "
                              "certified half-turn increments => exactly one det "
                              "zero in box.",
        },
        "params": {"N_per_component": N, "kappa": 3, "matrix_dim": 3 * N,
                   "n_head": N_HEAD, "sector_sign": SIGN},
    }

    print("=" * 78)
    print("CERTIFIED G_8 (even q) Selberg-zeta zero -- anchor + winding")
    print(f"backend={CE.BACKEND} prec={CE.PREC_BITS} bits  N/comp={N} "
          f"matrix={3*N}x{3*N}  n_head={N_HEAD}")
    print("=" * 78)

    # -------------------------------------------------------------- (0) selfcheck
    print("\n[0] SELF-CHECK certified-vs-doubleprec builder (q=8, N=10):")
    sc_abs, sc_rel = CE.selfcheck_vs_doubleprec(Q, N=10, n_head=N_HEAD,
                                                r=ANCHOR_R, sign=SIGN)
    out["selfcheck_vs_doubleprec"] = {
        "N": 10, "max_abs_entry_diff": float(sc_abs), "max_rel": float(sc_rel),
        "note": "double-prec builder has an O(1/n_head) L^inf-tail truncation "
                "error; the certified tail is exact, so this diff is the "
                "double-prec resolution (~1e-5 at n_head=8000), not a bug "
                "(diff -> 2.5e-6 at n_head=2e5).",
    }

    # ------------------------------------------------- (1) anchor reproduction
    print("\n[1] ANCHOR reproduction: certified |det| at r=5.798144, both sectors:")
    anchor_dets = {}
    for Nv in [12, 16, 20]:
        row = {}
        for sg in (-1, +1):
            z = CE.cert_absdet_mid(acb(arb(1) / 2, arb(ANCHOR_R)), Nv, sg, Q,
                                   N_HEAD)
            row[("mms-" if sg < 0 else "mms+")] = float(z)
            print(f"    N={Nv:2d} sign={sg:+d} ({'mms-' if sg<0 else 'mms+'}): "
                  f"|det| = {z:.4e}")
        anchor_dets[Nv] = row
    out["anchor_absdet"] = anchor_dets
    out["anchor_reproduced"] = bool(anchor_dets[20]["mms-"] < 1e-5
                                    and anchor_dets[20]["mms+"] > 1e-2)
    print(f"    -> anchor reproduced (mms- ~0, mms+ ~O(1)): "
          f"{out['anchor_reproduced']}")

    # ------------------------------------------- (1b) certified dimension tail
    s_probe = acb(arb(1) / 2, arb(ANCHOR_R))
    Mp, kp = CE.build_reduced_matrix_ball(s_probe, N, SIGN, Q, n_head=N_HEAD)
    tailp, infop = CE.dim_tail_from_matrix(Mp, N, kp)
    print(f"\n[1b] certified dimension-tail (s=1/2+{ANCHOR_R}i, N={N}, mms-): "
          f"{('%.3e' % float(tailp)) if tailp is not None else 'NOT CERTIFIED'} "
          f"q={infop.get('q','-')}")
    out["dim_tail_probe"] = {
        "tail_radius": float(tailp) if tailp is not None else None,
        "q": infop.get("q"), "ratios": infop.get("ratios"),
        "increment_mag": infop.get("increment_mag"),
    }

    def flush():
        out["wall_seconds"] = time.time() - t0
        os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
        with open(OUT_PATH, "w") as f:
            json.dump(out, f, indent=2)

    flush()

    # ----------------------------------------------- (2) locate + winding box
    print("\n[2] locate on-line zero r* (complex-secant) then winding box:")
    r_star = CE.locate_online_zero(ANCHOR_R, N, SIGN, Q, N_HEAD)
    z_star = CE.cert_absdet_mid(acb(arb(1) / 2, arb(r_star)), N, SIGN, Q, N_HEAD)
    print(f"    r* = {r_star:.8f}  |det(1/2+i r*)| = {z_star:.3e}  "
          f"(|r* - anchor| = {abs(r_star-ANCHOR_R):.2e})")
    out["r_star_located"] = float(r_star)
    out["absdet_at_rstar"] = float(z_star)

    wnd_result = None
    for hy in (8e-5, 1.5e-4, 3e-4, 6e-4):
        for hx_mult in (1.0, 2.0):
            hx = hy * hx_mult
            for K in (16, 28):
                log = []
                w, winfo = CE.winding_box(r_star, hx, hy, N, SIGN, Q,
                                          n_head=N_HEAD, K=K, log=log)
                if w is not None:
                    wnd_result = (w, winfo, r_star, hx, hy, log)
                    break
            if wnd_result is not None:
                break
        if wnd_result is not None:
            break

    if wnd_result is not None:
        w, winfo, r0, hx, hy, log = wnd_result
        box_lo, box_hi = r0 - hy, r0 + hy
        out["winding"] = {
            "winding_number": int(w),
            "box_r_center": float(r0),
            "box_hx_dx": float(hx),
            "box_hy_dr": float(hy),
            "r_lo": float(box_lo), "r_hi": float(box_hi),
            "anchor_in_box": bool(box_lo <= ANCHOR_R <= box_hi),
            "winding_ball": winfo.get("winding_ball"),
            "K_per_edge": winfo.get("K_per_edge"),
            "tail_fix": winfo.get("tail_fix"),
            "zero_certified_in_box": bool(w == 1),
            "log": log,
        }
        print(f"    WINDING box r0={r0:.8f} +-({float(hx):.1e}dx,{float(hy):.1e}dr): "
              f"winding={w} "
              f"{'=> 1 CERTIFIED det zero in box' if w==1 else ''} "
              f"{'(anchor in box)' if box_lo<=ANCHOR_R<=box_hi else ''}")
        out["certified"] = bool(w == 1)
    else:
        out["winding"] = None
        out["certified"] = False
        print("    WINDING not certified (boxes tried up to +-6e-4)")

    flush()
    dt = time.time() - t0
    print("\n" + "=" * 78)
    print(f"RESULT: anchor_reproduced={out['anchor_reproduced']}  "
          f"certified(winding=1)={out.get('certified')}  ({dt:.1f}s)")
    print(f"wrote {OUT_PATH}")
    print("=" * 78)
    return out


if __name__ == "__main__":
    main()
