"""Arithmeticity-signature law figure: line vs cloud across 5 Hecke surfaces."""
import json, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

d = json.load(open('/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_b/harvest_receipt.json'))
pts, stats = {}, d['derived_statistics']
for e in d['coordinate_entries']:
    if e.get('included_in_statistics'):
        pts.setdefault(e['surface'], []).append((e['value']['re'], e['value']['im']))

BLUE, ORANGE = "#2a78d6", "#d97706"
INK, MUT = "#333333", "#8a8a8a"
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11.5, 6.2), width_ratios=[2.1, 1.0])
fig.patch.set_facecolor("white")

# Panel A: the s-plane
ax.axvline(0.25, color=MUT, lw=1.2, ls=(0, (5, 4)), zorder=1)
ax.text(0.25, 23.35, "Re = 1/4 — critical line (ζ(2s) zeros)", fontsize=9, color=INK, ha="center", va="bottom")
mk = {"q=3": ("o", 62), "q=4": ("s", 58), "q=6": ("D", 50)}
for s, (m, sz) in mk.items():
    xs, ys = zip(*pts[s]); ax.scatter(xs, ys, marker=m, s=sz, facecolors="none",
        edgecolors=BLUE, linewidths=2.0, zorder=3, label=f"{s}  (arithmetic)")
for s, m in (("G_5", "o"), ("G_7", "^")):
    xs, ys = zip(*pts[s]); ax.scatter(xs, ys, marker=m, s=54, color=ORANGE,
        alpha=0.9, zorder=3, label=("G₅" if s=="G_5" else "G₇") + "  (non-arithmetic)")
zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271]
for g in zeros:
    ax.plot([0.115, 0.128], [g/2, g/2], color=MUT, lw=1.0, zorder=2)
ax.text(0.108, zeros[0]/2 - 1.15, "γ/2 of the\nRiemann zeros", fontsize=8, color=MUT, ha="left")
ax.set_xlim(0.10, 0.53); ax.set_ylim(3.4, 24.6)
ax.set_xlabel("Re(s)", fontsize=10, color=INK); ax.set_ylabel("Im(s)", fontsize=10, color=INK)
ax.set_title("Transfer-operator resonances across the Hecke family", fontsize=11.5, color=INK, pad=10)
ax.legend(loc="lower right", fontsize=8.5, frameon=False)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
ax.tick_params(colors=MUT, labelsize=8.5)

# Panel B: rigidity gap (log scale)
order = ["q=3", "q=4", "q=6", "G_5", "G_7"]
labels = ["q=3", "q=4", "q=6", "G₅", "G₇"]
vals = [max(stats[s]["re_std"], 1e-15) for s in order]
cols = [BLUE]*3 + [ORANGE]*2
y = range(len(order))
ax2.hlines(y, 1e-15, vals, color=cols, lw=2, alpha=0.55)
ax2.scatter(vals, y, s=64, color=cols, zorder=3)
for i, v in enumerate(vals):
    ax2.annotate(f"{v:.0e}", (v, i), textcoords="offset points", xytext=(0, 9),
                 fontsize=8, color=INK, ha="center")
ax2.set_xscale("log"); ax2.set_xlim(1e-15, 1.0)
ax2.set_yticks(list(y), labels, fontsize=9.5); ax2.invert_yaxis()
ax2.set_xlabel("std of Re(s) across resonances  (log scale)", fontsize=9.5, color=INK)
ax2.set_title("The rigidity gap: ~11 orders of magnitude", fontsize=11.5, color=INK, pad=10)
ax2.axvspan(1e-15, 1e-9, color=BLUE, alpha=0.05)
ax2.axvspan(1e-3, 1.0, color=ORANGE, alpha=0.05)
ax2.text(3e-13, -0.55, "pinned to the line", fontsize=8.5, color=BLUE, ha="center")
ax2.text(5e-2, -0.55, "scattered", fontsize=8.5, color=ORANGE, ha="center")
for sp in ("top", "right"): ax2.spines[sp].set_visible(False)
ax2.tick_params(colors=MUT, labelsize=8.5)

fig.suptitle("Arithmetic Hecke groups pin their resonances to the critical line — non-arithmetic groups scatter",
             fontsize=12.5, color=INK, y=0.985)
fig.text(0.01, 0.012, "Certified/high-precision pins, 2026-08-14 receipts; q=3,4,6 arithmetic (Takeuchi), G₅, G₇ non-arithmetic. Newton-pinned |det|≈1e-15; q=3 line std 6.5e-14.",
         fontsize=7, color=MUT)
plt.tight_layout(rect=(0, 0.03, 1, 0.95))
out = "/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_b/arithmeticity_law_figure.png"
fig.savefig(out, dpi=180)
print("wrote", out)
