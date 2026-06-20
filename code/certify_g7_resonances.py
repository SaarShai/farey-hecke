"""
certify_g7_resonances.py
========================
RIGOROUS upgrade for the G_7 even resonances found by run_resonance_g7.py:
apply the certified off-line argument-principle winding box (winding_offline)
around each N-stable pinned resonance.  A winding number = 1 PROVES a genuine
complex zero of det(1-L+_s) inside the box (a true scattering pole / dissolved
even Maass form), strictly stronger than the N-stability + deep-|det| locator.

This makes the G_7 result MORE rigorous than the G_5 geometry baseline
(run_resonance_geometry.py did NOT run winding boxes).

Reads code/out/resonance_g7.json, certifies up to MAXCERT deepest resonances,
writes the winding records back into the JSON.
"""
from __future__ import annotations
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import ctx
import zeta_cert_rosen as Z
from run_resonance_g7 import atomic_dump, _san

ctx.prec = 400
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out",
                   "resonance_g7.json")
MAXCERT = 5


def main():
    t0 = time.time()
    d = json.load(open(OUT))
    res = [z for z in d.get("g7_even_resonances", []) if z.get("N_stable")]
    res.sort(key=lambda z: z["absdet"])
    res = res[:MAXCERT]
    print(f"certifying {len(res)} deepest N-stable G_7 even resonances "
          f"via winding box", flush=True)
    certs = []
    for z in res:
        re0, im0 = z["re"], z["im"]
        log = []
        wnd = None
        # try a few box sizes (small first; widen if det ball touches 0)
        for (hx, hy) in [(0.008, 0.008), (0.015, 0.015), (0.025, 0.02),
                         (0.04, 0.03)]:
            w, info = Z.winding_offline(re0, im0, hx, hy, 22, +1, 7, 4,
                                        K=24, log=log)
            if w is not None:
                wnd = (w, info)
                break
        rec = {"re": re0, "im": im0, "absdet": z["absdet"]}
        if wnd is not None:
            w, info = wnd
            rec["winding_number"] = int(w)
            rec["zero_certified"] = bool(w == 1)
            rec["winding_info"] = info
            print(f"  s={re0:.5f}+{im0:.5f}i: winding={w} "
                  f"{'=> 1 CERTIFIED off-line zero in box' if w == 1 else ''}",
                  flush=True)
        else:
            rec["winding_number"] = None
            rec["zero_certified"] = False
            rec["winding_log"] = log
            print(f"  s={re0:.5f}+{im0:.5f}i: winding NOT certified "
                  f"(boxes up to 0.04)", flush=True)
        certs.append(rec)
    d["g7_even_winding_certified"] = certs
    n_cert = sum(1 for c in certs if c["zero_certified"])
    d.setdefault("verdict", {})["n_winding_certified"] = n_cert
    atomic_dump(d, OUT)
    print(f"\n{n_cert}/{len(certs)} winding-certified off-line zeros "
          f"({time.time()-t0:.0f}s) -> {OUT}")


if __name__ == "__main__":
    main()
