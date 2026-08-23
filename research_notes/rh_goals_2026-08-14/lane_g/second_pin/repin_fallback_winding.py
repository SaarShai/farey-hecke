#!/usr/bin/env python3
"""repin_fallback_winding.py — re-derive the fallback pin's scan-level
winding ball (referee C3: the ball [0.99999949, 1.00000051] was quoted in
S2_SECOND_WINDING_BOX_SOL.md §4 without a reachable artifact).

Provenance note: the original ball DOES exist at full precision in
`.worktrees/aletheia-restore/code/out/resonance_v2.json`
(newton_pin label "g5even(0.43,7.75)": winding_ball
[0.9999999492931789, 1.000000050706821], K_per_edge=28, hx=hy=0.012,
center (0.41054373549576567, 7.819768247017059), tail_fix 6.078e-11) —
the referee's grep for the 8-digit rounded string could not hit it.
This script INDEPENDENTLY re-runs the same computation
(`zeta_resonance_g5.winding_offline`, prec 400 bits, sign=+1, n_head=4,
K=28, hx=hy=0.012) at a caller-chosen truncation N and records the actual
ball with directed rounding (arb .lower()/.upper() printed via arb.str
with more=True, i.e. guaranteed enclosures).

Usage: repin_fallback_winding.py [--N 16]
Writes REPIN_FALLBACK_WINDING_N{N}_RECEIPT.json next to itself and logs
to stdout (tee'd by the caller into repin_fallback.log).
"""
import argparse
import json
import time
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
CODE = Path("/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code")
sys.path.insert(0, str(CODE))

from flint import arb, ctx  # noqa: E402
import zeta_resonance_g5 as Zr  # noqa: E402

RE0 = "0.41054373549576567"   # newton-pinned center from resonance_v2.json
IM0 = "7.819768247017059"
HX = HY = 0.012
K = 28
SIGN = +1
N_HEAD = 4
PREC = 400


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, default=16)
    args = ap.parse_args()
    ctx.prec = PREC
    log = []
    t0 = time.time()
    # winding_offline takes float-ish re0/im0; keep full-precision strings in
    # the receipt, floats round-trip exactly here (both are 17-digit doubles).
    w, info = Zr.winding_offline(5, float(RE0), float(IM0), HX, HY,
                                 args.N, SIGN, N_HEAD, K=K, log=log)
    wall = time.time() - t0
    print(f"# repin_fallback_winding  N={args.N} prec={PREC} sign={SIGN:+d} "
          f"n_head={N_HEAD} K={K} hx=hy={HX}")
    print(f"center = ({RE0}, {IM0})")
    for line in log:
        print("log:", line)
    print("winding =", w)
    print("info =", json.dumps(info, indent=1))
    # Directed (outward) rounding guard: winding_offline converts the arb
    # ball endpoints (already rigorous .lower()/.upper() enclosure endpoints)
    # to Python floats, which may round to nearest.  Outward-round by 1 ulp
    # so the recorded ball is a guaranteed superset.
    import math
    ball = info.get("winding_ball")
    ball_outward = None
    if ball is not None:
        ball_outward = [math.nextafter(ball[0], -math.inf),
                        math.nextafter(ball[1], math.inf)]
        print("winding_ball outward-rounded (1 ulp):", ball_outward)
    receipt = {
        "script": "repin_fallback_winding.py",
        "engine": str(CODE / "zeta_resonance_g5.py"),
        "provenance_of_original_ball":
            str(CODE / "out" / "resonance_v2.json") +
            " (newton_pin g5even(0.43,7.75), winding_ball "
            "[0.9999999492931789, 1.000000050706821])",
        "center": [RE0, IM0], "hx": HX, "hy": HY, "K_per_edge": K,
        "N": args.N, "sign": SIGN, "n_head": N_HEAD, "prec_bits": PREC,
        "winding": w, "info": info,
        "winding_ball_outward_1ulp": ball_outward,
        "wall_seconds": wall,
    }
    out = HERE / f"REPIN_FALLBACK_WINDING_N{args.N}_RECEIPT.json"
    out.write_text(json.dumps(receipt, indent=1))
    print("receipt:", out)


if __name__ == "__main__":
    main()
