"""
run_resonance_geometry.py
=========================
EXPANSION: map the even-sector resonance GEOMETRY of G_5 (non-arith) and
contrast with q=3 (arithmetic). The sharp question:

  q=3 (arithmetic modular surface): even resonances = zeros of zeta(2s), all on
    the vertical line Re(s)=1/4 (a RIGID line).
  G_5 (non-arithmetic): the two already-located even resonances sit at Re=0.454
    and Re=0.411 -- DIFFERENT Re -> NOT on a single vertical line.

Hypothesis under test: the resonance Re-distribution detects arithmeticity --
arithmetic = resonances on a line; non-arithmetic = scattered. We locate MANY
G_5 even resonances, measure the Re-spread, and compare to q=3's Re=1/4 line.

Certified Arb engine throughout (double-prec diverges off-line).
Output: code/out/resonance_geometry.json
"""
from __future__ import annotations
import json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from flint import acb, arb, ctx
import zeta_resonance_g5 as Zr
ctx.prec = 400
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "resonance_geometry.json")
RIEMANN_T = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062, 37.586178,
             40.918719, 43.327073]

t0 = time.time()
out = {"objective": "even-sector resonance geometry: G_5 (non-arith) cloud vs "
                    "q=3 (arith) Re=1/4 line; arithmeticity signature.",
       "prec_bits": 400}
log = []
def dump():
    out["log"] = log; out["wall_seconds"] = time.time() - t0
    Zr.atomic_dump(out, OUT)

def pin(q, re0, im0, sign, N=22):
    s0, fmin, hist = Zr.newton_locate(q, re0, im0, N, sign, 4)
    return s0.real, s0.imag, fmin

# ---- q=3 even: confirm resonances lie on Re=1/4 (Newton from zeta-zero seeds) ----
log.append("q3 even: pin resonances from s=1/4+i*gamma/2 seeds")
q3 = []
for g in RIEMANN_T:
    try:
        re, im, fm = pin(3, 0.25, g / 2.0, +1, N=30)
        if fm < 1e-6:
            q3.append({"re": re, "im": im, "absdet": fm, "t_n": g})
            print(f"[q3] gamma={g:.4f} -> s={re:.5f}+{im:.5f}i |det|={fm:.1e}", flush=True)
    except Exception as e:
        log.append(f"q3 pin gamma={g} EXC {e!r}")
out["q3_even_resonances"] = q3
dump()

# ---- G_5 even: fine near-line surface -> Newton-pin -> dedup ----
log.append("G_5 even: fine near-line surface + Newton-pin")
RE = np.linspace(0.30, 0.49, 8)        # near-line band (dissolved/scattering)
IM = np.linspace(3.0, 17.0, 141)       # 0.1 spacing -> catch sharp dips
grid = np.empty((len(RE), len(IM)))
for a, re in enumerate(RE):
    for b, im in enumerate(IM):
        try:
            grid[a, b] = abs(Zr.cert_det_complex_mid(5, acb(arb(float(re)), arb(float(im))), 14, +1, 4))
        except Exception:
            grid[a, b] = 9.99
    print(f"[G5 surf] Re={re:.3f} min|det|={grid[a].min():.3e} ({time.time()-t0:.0f}s)", flush=True)
    log.append(f"surf Re={re:.3f} min={grid[a].min():.3e}")
    dump()
med = float(np.median(grid))

# seed Newton from every grid point below a generous threshold
seeds = []
thr = min(0.5 * med, 0.40)
for a in range(len(RE)):
    for b in range(len(IM)):
        if grid[a, b] < thr:
            seeds.append((float(RE[a]), float(IM[b])))
log.append(f"G_5 surface median={med:.3e}; {len(seeds)} seeds below {thr:.3f}")

g5 = []
for (re0, im0) in seeds:
    try:
        re, im, fm = pin(5, re0, im0, +1, N=22)
        if fm < 1e-5 and 0.05 < re < 0.49 and 3.0 < im < 17.0:
            # dedup
            if not any(abs(re - z["re"]) < 0.01 and abs(im - z["im"]) < 0.03 for z in g5):
                # N-stability confirm (N=28)
                re2, im2, fm2 = pin(5, re0, im0, +1, N=28)
                stable = bool(abs(re - re2) < 2e-3 and abs(im - im2) < 2e-3 and fm2 < 1e-4)
                g5.append({"re": re, "im": im, "absdet": fm, "N_stable": stable})
                print(f"[G5] pinned s={re:.5f}+{im:.5f}i |det|={fm:.1e} Nstable={stable}", flush=True)
                dump()
    except Exception as e:
        log.append(f"G5 pin ({re0},{im0}) EXC {e!r}")
g5.sort(key=lambda z: z["im"])
out["g5_even_resonances"] = g5

# ---- characterize: Re-spread (line vs scatter) ----
g5_stable = [z for z in g5 if z["N_stable"]]
def stats(zs):
    res = [z["re"] for z in zs]
    if not res:
        return {"n": 0}
    return {"n": len(res), "re_mean": float(np.mean(res)),
            "re_std": float(np.std(res)), "re_min": float(min(res)),
            "re_max": float(max(res)), "re_range": float(max(res) - min(res))}
out["verdict"] = {
    "q3_geometry": {**stats(q3), "expected": "Re=0.25 line (zeta zeros)"},
    "g5_all_geometry": stats(g5),
    "g5_stable_geometry": stats(g5_stable),
    "interpretation": "if g5 re_std >> q3 re_std (~0) and g5 re_range is wide, "
                      "non-arith resonances SCATTER in Re vs arith resonances on a line.",
}
dump()
print("\nVERDICT:", json.dumps(out["verdict"], indent=2))
print(f"done ({time.time()-t0:.0f}s) -> {OUT}")
