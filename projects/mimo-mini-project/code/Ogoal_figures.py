#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ogoal_figures.py (goal O) — figures for the zero-temperature / cusp-escape demonstration.
Consumes Ogoal_{value_seq,transfer,escape}_*.json/npz produced by the other scripts.
Outputs PNGs to ../figures/.

(i)  cusp escape: min-MAX family value V(s)->1/lam^3 as base pt -> cusp vertex (ESCAPE), and
     the Birkhoff mu_beta cusp-mass -> 0 (does NOT escape) -- the two objectives side by side.
(ii) two zero-temperature values: 1/lam^3 (ess-sup, min-MAX) vs beta_min (Birkhoff, min-AVG) vs q.
(iii) freezing curve: free energy -ln rho(beta)/beta vs beta (q=5,7,12), with 1/lam^3 levels.
(iv) escape rate / margin: (2-lam) q^2 -> pi^2 and (1/lam^3-1/8) q^2 -> (3/16)pi^2 vs q.
(v)  mu_beta heatmaps over Tq at increasing beta (q=5): interior concentration, NOT cusp.
"""
import json, os, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "..", "figures")
def load(name): return json.load(open(os.path.join(HERE, name)))

vseq = load("Ogoal_value_seq_results.json")
tran = load("Ogoal_transfer_summary.json")
esc  = load("Ogoal_escape_results.json")

# ---------- (i) escape: value->1/lam^3, and divergent parabolic residence (no ground state) ----------
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
# left: min-MAX family value vs dist-to-cusp (q=5,7,12) -> 1/lam^3
for q in ["5","7","12"]:
    tbl = vseq["value_sequence"][q]
    d = [r["dist"] for r in tbl]; v = [r["val"] for r in tbl]
    l, = ax[0].plot(d, v, 'o-', label=f"q={q}")
    thr = [r for r in esc["margin"] if r["q"]==int(q)][0]["inv_lam3"]
    ax[0].axhline(thr, ls=':', color=l.get_color(), lw=0.9)
ax[0].set_xscale('log'); ax[0].invert_xaxis()
ax[0].set_xlabel("distance of optimizing orbit to cusp vertex (1/λ,0)")
ax[0].set_ylabel("ess-sup P  along min-MAX family")
ax[0].set_title("min-MAX (ess-sup): optimizer ESCAPES to cusp,\nvalue → 1/λ³  (dotted) from above")
ax[0].legend()
# right: parabolic residence diverges ~ 1/delta (marginal -> no ground state)
for q, rows in esc["residence"].items():
    dl = [r["delta"] for r in rows]; st = [r["steps_in"] for r in rows]
    ax[1].plot(dl, st, 'o-', label=f"q={q}")
dref = [r["delta"] for r in esc["residence"]["5"]]
ax[1].plot(dref, [0.15/d for d in dref], 'k--', lw=0.9, label="∝ 1/δ (parabolic)")
ax[1].set_xscale('log'); ax[1].set_yscale('log'); ax[1].invert_xaxis()
ax[1].set_xlabel("seed distance δ to cusp vertex")
ax[1].set_ylabel("steps spent in cusp neighbourhood")
ax[1].set_title("Residence DIVERGES ∝ 1/δ as δ→0 (parabolic / marginal):\nthe optimizer never settles — NO ground state")
ax[1].legend()
fig.suptitle("Cusp escape on the Hecke BCZ map: ess-sup → 1/λ³ with divergent residence (no ground state)",
             fontweight='bold')
fig.tight_layout(); fig.savefig(os.path.join(FIG, "Ogoal_escape_vs_noescape.png"), dpi=140)
plt.close(fig)

# ---------- (ii) two values vs q ----------
fig, ax = plt.subplots(figsize=(7.5, 5))
rows = esc["margin"]
qs = [r["q"] for r in rows]
# 1/lam^3 = X_Omega only for q>=5; q=3,4 are special (interior minimizer, GS exists)
q5 = [r["q"] for r in rows if r["q"] >= 5]; inv5 = [r["inv_lam3"] for r in rows if r["q"] >= 5]
ax.plot(q5, inv5, 's-', color='C3', label="1/λ³ = X_Ω(q)  (q≥5, min-MAX ess-sup, PROVEN; ESCAPE)")
ax.plot([3, 4], [2/9, math.sqrt(2)/8], 'P', color='C1', ms=11,
        label="X_Ω(3)=2/9, X_Ω(4)=√2/8  (interior minimizer, GS EXISTS)")
# q=5 proven Birkhoff beta_min (word search, period-3 interior orbit): 0.18634 < 1/lam^3
ax.plot([5], [0.186339], 'D', color='C0', ms=10,
        label="β_min(q=5)=0.1863 (min-AVG, PROVEN interior orbit)")
ax.annotate("min-AVG < min-MAX\n(gap: 0.236 vs 0.186)", xy=(5,0.186339),
            xytext=(7,0.165), arrowprops=dict(arrowstyle='->', color='C0'), color='C0')
# transfer free-energy zero-temp estimate at max reliable beta (grid; caveat)
for q, d in tran.items():
    res = [r for r in d["results"] if "error" not in r and r["free_energy"] is not None]
    fmin = min(r["free_energy"] for r in res)
    ax.plot(int(q), fmin, 'o', color='C2', ms=6, mfc='none',
            label="Birkhoff transfer estimate (grid)" if q==list(tran)[0] else None)
ax.axhline(0.125, ls=':', color='gray'); ax.text(qs[-4], 0.128, "1/8 (q→∞)", color='gray')
ax.set_xlabel("q"); ax.set_ylabel("value")
ax.set_title("Two zero-temperature values: ess-sup 1/λ³  vs  Birkhoff β_min  (β_min < 1/λ³)")
ax.legend(); fig.tight_layout()
fig.savefig(os.path.join(FIG, "Ogoal_two_values.png"), dpi=140); plt.close(fig)

# ---------- (iii) freezing curve ----------
fig, ax = plt.subplots(figsize=(7.5, 5))
for q, d in tran.items():
    res = [r for r in d["results"] if "error" not in r and r["free_energy"] is not None]
    bb = [r["beta"] for r in res]; fe = [r["free_energy"] for r in res]
    l, = ax.plot(bb, fe, 'o-', label=f"q={q}: free energy -lnρ/β")
    ax.axhline(d["meta"]["inv_lam3"], ls=':', color=l.get_color(), lw=0.8)
ax.set_xscale('log'); ax.set_xlabel("β"); ax.set_ylabel("free energy  f(β) = -ln ρ(β)/β")
ax.set_title("Freezing / zero-temperature transition\n(free energy → β_min as β→∞; dotted = 1/λ³ ess-sup level)")
ax.legend(); fig.tight_layout()
fig.savefig(os.path.join(FIG, "Ogoal_freezing.png"), dpi=140); plt.close(fig)

# ---------- (iv) escape-rate / margin O(1/q^2) ----------
fig, ax = plt.subplots(1, 2, figsize=(12, 4.6))
qs = [r["q"] for r in rows]
mq2 = [r["margin_q2"] for r in rows]; gq2 = [r["gap_q2"] for r in rows]
ax[0].plot(qs, mq2, 'o-', label="(2−λ)·q²")
ax[0].axhline(math.pi**2, ls='--', color='r', label="π² = 9.8696")
ax[0].set_xlabel("q"); ax[0].set_ylabel("(2−λ)·q²")
ax[0].set_title("cusp-corridor margin 2−λ ~ π²/q²  (O(1/q²))"); ax[0].legend()
ax[1].plot(qs, gq2, 's-', color='C3', label="(1/λ³ − 1/8)·q²")
ax[1].axhline(3/16*math.pi**2, ls='--', color='r', label="(3/16)π² = 1.8506")
ax[1].set_xlabel("q"); ax[1].set_ylabel("(1/λ³ − 1/8)·q²")
ax[1].set_title("value approach to asymptote 1/8  (O(1/q²))"); ax[1].legend()
fig.tight_layout(); fig.savefig(os.path.join(FIG, "Ogoal_escape_rate.png"), dpi=140); plt.close(fig)

# NOTE: a mu_beta(a,b) heatmap was deliberately NOT produced -- the grid-Ulam eigenvector
# location is unstable at large beta (ARPACK a-edge spurious modes; q-dependent onset), so any
# such heatmap would misrepresent where mu_beta concentrates. The robust transfer results are the
# beta=0 flat-density validation and the freezing curve (Ogoal_freezing.png).

print("wrote figures:",
      "Ogoal_escape_vs_noescape.png, Ogoal_two_values.png, Ogoal_freezing.png,",
      "Ogoal_escape_rate.png")
