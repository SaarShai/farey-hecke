"""
analyze_qv.py — clean + analyze the G_5/q3 quantum-variance kernel output.
Filters spurious forms (the relaxed N-stability let dips through), recomputes
the variance on genuine forms, checks the |M|^2 vs r decay (QUE rate), and
states honestly what the data can/can't say about universal-vs-arithmetic.
"""
import json, glob
import numpy as np

d = json.load(open("code/out/qv_g5_v2.json"))
VALID_G5_ODD = [6.4737, 8.6368, 10.1365, 11.0156, 12.0841, 12.8513]   # certified low-r
# SL(2,Z) odd Maass r (q3 anchor)
VALID_Q3 = [9.5337, 12.1730, 14.3585, 16.1381, 16.6443, 18.1809]

def forms(q): return d["runs"][q]["forms"]

def summarize(label, fs, valid):
    r   = np.array([f["r"] for f in fs])
    M   = np.array([f["matrix_element"] for f in fs])
    shp = np.array([f["N_stability_shift"] for f in fs])
    sg  = np.array([f["sigma_min"] for f in fs])
    print(f"\n===== {label}: {len(fs)} raw forms =====")
    print(f"  N_stability_shift: min={shp.min():.1e} med={np.median(shp):.1e} max={shp.max():.1e}")
    print(f"  sigma_min:         min={sg.min():.1e} med={np.median(sg):.1e} max={sg.max():.1e}")
    # low-r cross-check vs validated spectrum
    lowr = [f for f in fs if f["r"] < 13.0]
    hits = sum(any(abs(f["r"]-v) < 0.03 for v in valid) for f in lowr)
    print(f"  low-r (<13): {len(lowr)} forms, {hits} match validated spectrum (±0.03)")
    # tight filters
    for name, mask in [("raw", np.ones(len(fs), bool)),
                       ("tight shift<5e-5", shp < 5e-5),
                       ("tight shift<2e-5 & sig<1e-4", (shp < 2e-5) & (sg < 1e-4))]:
        rr, MM = r[mask], M[mask]
        V = float(np.mean(MM**2)) if len(MM) else float("nan")
        print(f"  [{name:28s}] n={mask.sum():2d}  V=mean|M|^2={V:.5f}")
    return r, M, shp, sg

def decay_fit(label, fs, shp_thresh=5e-5):
    fs = [f for f in fs if f["N_stability_shift"] < shp_thresh and f["r"] > 5]
    r = np.array([f["r"] for f in fs]); M2 = np.array([f["matrix_element"] for f in fs])**2
    if len(r) < 5:
        print(f"  {label}: too few clean forms ({len(r)}) to fit decay"); return
    # window-average |M|^2 and fit log-log slope (QUE => |M|^2 ~ C/r, slope ~ -1)
    sl, b = np.polyfit(np.log(r), np.log(M2 + 1e-12), 1)
    # V*r per form: if ~const, that's the 1/r rate
    Vr = M2 * r
    print(f"  {label}: n={len(r)} clean, log-log slope(|M|^2 vs r)={sl:.2f} "
          f"(QUE/CdV ~ -1), mean(|M|^2 * r)={np.mean(Vr):.4f} +- {np.std(Vr):.4f}")

g5 = forms("G_5"); q3 = forms("q3")
print("STORED V:", d.get("quantum_variance_V_by_q"))
summarize("G_5 (non-arith)", g5, VALID_G5_ODD)
summarize("q3 (arith)", q3, VALID_Q3)
print("\n--- |M|^2 vs r decay (QUE rate; clean forms shift<5e-5) ---")
decay_fit("G_5", g5)
decay_fit("q3 ", q3)
print("""
HONEST VERDICT (universal vs arithmetic):
- Both surfaces' matrix elements decay with r -> consistent with QUE (mass equidistributes).
- The clean universal-vs-arithmetic discrimination needs (i) the CLASSICAL variance
  C(f) of each surface's geodesic flow (the Luo-Sarnak/Eckhardt normalizer) and
  (ii) many more spectrally-clean high-r forms than the conditioning at Y0=0.5
  yields. Raw V_G5 vs V_q3 are NOT directly comparable (different surfaces => different
  C(f) and different spectral windows). => DATA-LIMITED: we have the matrix-element
  data + a QUE-consistent decay, NOT the universal-vs-arithmetic verdict.
""")
