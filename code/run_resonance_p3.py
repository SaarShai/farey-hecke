"""
run_resonance_p3.py
===================
Focused continuation of run_resonance_v2.py: the band COUNTS, q=3 validation,
and G_5 even surface already landed in code/out/resonance_v2.json (run bx2scmyrr
crashed in localization due to a persistence bug). This reuses that data and
only runs: re-box of any inconclusive band -> localize each resonance
(bisect + Newton-pin) -> classify near-line vs near-Re=0 -> verdict.
Robust: per-step try/except, incremental atomic dumps.
"""
from __future__ import annotations
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_resonance_v2 as R2
Zr = R2.Zr
OUT_PATH = R2.OUT_PATH

t0 = time.time()
out = json.load(open(OUT_PATH))
log = out.get("log", [])
def dump():
    out["log"] = log; out["wall_seconds_p3"] = time.time() - t0
    Zr.atomic_dump(out, OUT_PATH)

g5_counts = out["g5_even_band_counts"]
surf = out["g5_even_surface"]
med5 = surf["median_absdet"]
minima = surf["minima"]                     # [{re,im,absdet}]
print("band counts:", [(b["box"][2:], b["zero_count"]) for b in g5_counts], flush=True)

# ---- re-box inconclusive bands ----
g5_rebox = []
out["g5_even_band_rebox"] = g5_rebox
for b in g5_counts:
    if b["zero_count"] is None:
        rl, rh, il, ih = b["box"]
        for (lo, hi) in [(il + 0.2, ih - 0.2), (il + 0.35, ih - 0.05)]:
            try:
                rb = R2.gbox(5, rl, rh, lo, hi, +1, 22, 52, log)
                g5_rebox.append(rb); dump()
                print(f"  rebox Im[{lo},{hi}] count={rb['zero_count']}", flush=True)
                if rb["zero_count"] is not None:
                    break
            except Exception as e:
                log.append(f"  rebox EXC {e!r}"); dump()

# ---- localize: bisect each populated band + Newton-pin surface minima ----
g5_located = []
out["g5_even_localization"] = g5_located
for b in g5_counts:
    if b["zero_count"] and b["zero_count"] > 0:
        rl, rh, il, ih = b["box"]; mid = 0.5 * (il + ih)
        for (lo, hi) in [(il, mid), (mid, ih)]:
            try:
                sub = R2.gbox(5, rl, rh, lo, hi, +1, 22, 44, log)
                g5_located.append(sub); dump()
                print(f"  subbox Im[{lo},{hi}] count={sub['zero_count']}", flush=True)
            except Exception as e:
                log.append(f"  subbox EXC {e!r}"); dump()
        for m in minima:
            re_c, im_c, dp = m["re"], m["im"], m["absdet"]
            if il <= im_c <= ih and dp < 0.5 * med5:
                try:
                    rec = R2.newton_and_winding(5, re_c, im_c, +1,
                                                f"g5even({re_c:.2f},{im_c:.2f})", log)
                    g5_located.append({"newton_pin": rec}); dump()
                    nw = rec["newton"]
                    print(f"  pin ({re_c:.2f},{im_c:.2f}) -> "
                          f"{nw['re']:.5f}+{nw['im']:.5f}i |det|={nw['absdet_mid']:.1e}",
                          flush=True)
                except Exception as e:
                    log.append(f"  pin EXC {e!r}"); dump()

# ---- classify + verdict ----
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
total_g5 = sum(b["zero_count"] for b in g5_counts if b["zero_count"] is not None)
out["verdict"] = {
    "q3_counting_validation_count": out.get("q3_counting_validation", {}).get("zero_count"),
    "g5_even_band_counts": [(b["box"], b["zero_count"]) for b in g5_counts],
    "g5_even_band_rebox": [(b["box"], b["zero_count"]) for b in g5_rebox],
    "g5_even_total_resonances_in_scan": total_g5,
    "g5_even_surface_min_absdet": surf["min_absdet"],
    "g5_even_pinned_near_line": near_line,
    "g5_even_pinned_near_zero": near_zero,
    "g5_even_n_near_line_resonances": len(near_line),
}
dump()
print("\nVERDICT:", json.dumps(out["verdict"], indent=2))
print(f"done ({time.time()-t0:.1f}s) -> {OUT_PATH}")
