#!/usr/bin/env python3
"""FIG-1: resonance-cloud figure, arithmetic (q=3) vs non-arithmetic (G_5) Hecke groups.

Data source: a byte-identical cached copy of
.worktrees/aletheia-restore/code/out/resonance_geometry.json, checked in
alongside this script as resonance_geometry_source.json (sha256 verified
equal; see FIG1_DATA_SOURCES.md for provenance). All plotted points are
Newton-pinned to machine precision (|det| ~ 1e-15); the q=3 sector is
additionally interval-certified against Riemann zeta zeros. The two off-line
certified Selberg zero pins (S2 contour campaign, argument-principle winding
certificates) are highlighted separately on the G_5 panel.
"""
import json
import pathlib

import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).parent
DATA = json.loads((HERE / "resonance_geometry_source.json").read_text())

q3 = DATA["q3_even_resonances"]
g5 = DATA["g5_even_resonances"]

# Certified off-line pins (argument-principle winding certificates, S2 campaign),
# half-width 1e-6 boxes. These are the two flagship theorem points.
CERT_PINS = [
    (0.4538951800749447, 5.7635372417301305, "pin 1"),
    (0.41054373549473627, 7.81976824701551188, "pin 2 (S2)"),
]
PIN_HALFWIDTH = 1e-6

fig, (axL, axR) = plt.subplots(1, 2, figsize=(8, 5.5), sharey=True)

# Left panel: q=3 (arithmetic)
q3_re = [p["re"] for p in q3]
q3_im = [p["im"] for p in q3]
axL.scatter(q3_re, q3_im, marker="o", s=28, color="tab:blue",
            label="q=3 even resonances (interval-certified)")
axL.axvline(0.25, ls="--", lw=1, color="grey")
axL.axvline(0.5, ls="--", lw=1, color="grey")
axL.set_title("Arithmetic (q=3)")
axL.set_xlabel("Re(s)")
axL.set_ylabel("Im(s)")
axL.set_xlim(0.0, 0.6)
axL.legend(loc="lower right", fontsize=7)

# Right panel: G_5 (non-arithmetic)
g5_re = [p["re"] for p in g5]
g5_im = [p["im"] for p in g5]
axR.scatter(g5_re, g5_im, marker="o", s=28, color="tab:red",
            label="G_5 even resonances (numerically validated,\nN-stable, |det|~1e-15)")
for re, im, _ in CERT_PINS:
    axR.scatter([re], [im], marker="*", s=160, color="black", zorder=5,
                label="certified off-line pin\n(winding cert, box halfwidth 1e-6)"
                if re == CERT_PINS[0][0] else None)
axR.axvline(0.25, ls="--", lw=1, color="grey")
axR.axvline(0.5, ls="--", lw=1, color="grey")
axR.set_title("Non-arithmetic (G_5)")
axR.set_xlabel("Re(s)")
axR.set_xlim(0.0, 0.6)
axR.legend(loc="upper left", fontsize=7)

fig.text(0.5, 0.01,
          "Dashed lines: Re=1/4, Re=1/2. Stars mark the two argument-principle-certified\n"
          "off-line zeros (box halfwidth 1e-6, not visible at this scale).",
          ha="center", fontsize=8)

fig.tight_layout(rect=(0, 0.06, 1, 1))
fig.savefig(HERE / "fig1_resonance_cloud.pdf")
fig.savefig(HERE / "fig1_resonance_cloud.png", dpi=200)

# ponytail self-check: data sanity before declaring done
assert len(q3) == 8 and len(g5) == 8, "unexpected point counts"
assert max(abs(p["re"] - 0.25) for p in q3) < 1e-10, "q3 line assumption broken"
print(f"OK: q3 n={len(q3)}, g5 n={len(g5)}, saved to {HERE}")
