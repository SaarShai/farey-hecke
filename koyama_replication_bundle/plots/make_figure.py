#!/usr/bin/env python3
"""Generate the headline replication figure for the CREST grant artefact bundle.

Figure 1 (top): pi(x; N, -1) - pi(x; N, 1) for N in {7,8,11,19,23} as a function
of x in {10^9, 10^10, 1.3e10, 10^11, 1.3e11, 10^12, 1.3e12, 10^13, 1.3e13}.
Shows that -1 is consistently strongly positive (Conjecture 2 dominance signal)
across the grid, with Littlewood sign-flips for some N.

Figure 2 (bottom): rank of -1 (mod N) among non-residues at x = 1.3e13 (and
at x = 10^12 for comparison), one bar per modulus.  Smaller rank = closer to
the top.  Rank 1 = -1 is the largest non-residue diff.
"""
import re, pathlib, sys
from math import gcd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DIR = pathlib.Path(__file__).resolve().parent.parent
text = (DIR / "out2.tsv").read_text()

blocks = {}
cur_N = None
state = None
for line in text.splitlines():
    m = re.match(r"^## N = (\d+)", line)
    if m:
        cur_N = int(m.group(1))
        blocks[cur_N] = {"counts": {}, "diffs": {}}
        state = None
        continue
    if line.startswith("# diffs"):
        state = "diffs"; continue
    if line.startswith("x\tcount_a"):
        state = "counts"; continue
    if line.startswith("x\tdiff_a"):
        state = "diffs"; continue
    if state and line and line[0].isdigit():
        parts = line.split("\t")
        x = int(parts[0])
        vals = list(map(int, parts[1:]))
        if state == "counts":
            blocks[cur_N]["counts"][x] = vals
        else:
            blocks[cur_N]["diffs"][x] = vals

Ns = sorted(blocks.keys())
checkpoints = sorted(blocks[7]["diffs"].keys())

# ----- Figure 1: dominance trajectory -----
fig, axes = plt.subplots(2, 1, figsize=(8.5, 9.0), gridspec_kw={"height_ratios": [3, 2]})
ax1 = axes[0]
colors = {7: "#1b9e77", 8: "#d95f02", 11: "#7570b3", 19: "#e7298a", 23: "#66a61e"}
markers = {7: "o", 8: "s", 11: "^", 19: "D", 23: "v"}

for N in Ns:
    minus1 = N - 1
    ys = []
    for x in checkpoints:
        diffs = blocks[N]["diffs"][x]   # cols a=2..N-1
        ys.append(diffs[minus1 - 2])
    ax1.plot(checkpoints, ys, marker=markers[N], color=colors[N],
             label=fr"$N={N}$ ($-1\equiv{minus1}$)", linewidth=1.3, markersize=6)

ax1.set_xscale("log")
ax1.axhline(0, color="black", linewidth=0.6, linestyle="--", alpha=0.6)
ax1.set_xlabel(r"$x$")
ax1.set_ylabel(r"$\pi(x;\,N,-1)\;-\;\pi(x;\,N,1)$")
ax1.set_title("Replication of Koyama (2026): dominance of $-1\\,(\\mathrm{mod}\\,N)$ vs $x$")
ax1.legend(loc="upper left", framealpha=0.9, fontsize=9)
ax1.grid(True, which="both", linestyle=":", alpha=0.3)

# ----- Figure 2: rank of -1 at headline checkpoints -----
ax2 = axes[1]
def rank_of_minus_one(N, x):
    """Return rank of -1 mod N among non-residues at x (1 = largest diff)."""
    coprimes = [a for a in range(2, N) if gcd(a, N) == 1]
    diffs = blocks[N]["diffs"][x]
    pairs = [(a, diffs[a - 2]) for a in coprimes]
    # Determine quadratic non-residues: a is QNR iff a is not a square mod N.
    squares = {(a*a) % N for a in range(1, N)}
    nonres = [(a, d) for a, d in pairs if a not in squares]
    nonres.sort(key=lambda t: -t[1])
    for r, (a, _) in enumerate(nonres, 1):
        if a == N - 1:
            return r, len(nonres)
    return None, len(nonres)

bar_w = 0.35
xpos = list(range(len(Ns)))
ranks_13e13 = []
ranks_1e12 = []
labels_13 = []
labels_12 = []
totals = []
for N in Ns:
    r13, t = rank_of_minus_one(N, 13_000_000_000_000)
    r12, _ = rank_of_minus_one(N, 1_000_000_000_000)
    ranks_13e13.append(r13)
    ranks_1e12.append(r12)
    totals.append(t)
    labels_13.append(f"{r13}/{t}")
    labels_12.append(f"{r12}/{t}")

bars1 = ax2.bar([p - bar_w/2 for p in xpos], ranks_13e13, bar_w,
                label=r"$x=1.3\!\cdot\!10^{13}$", color="#377eb8", edgecolor="black", linewidth=0.6)
bars2 = ax2.bar([p + bar_w/2 for p in xpos], ranks_1e12, bar_w,
                label=r"$x=10^{12}$", color="#ff7f00", edgecolor="black", linewidth=0.6)

for p, lbl in zip(xpos, labels_13):
    ax2.text(p - bar_w/2, ranks_13e13[xpos.index(p)] + 0.1, lbl, ha="center", fontsize=8)
for p, lbl in zip(xpos, labels_12):
    ax2.text(p + bar_w/2, ranks_1e12[xpos.index(p)] + 0.1, lbl, ha="center", fontsize=8)

ax2.set_xticks(xpos)
ax2.set_xticklabels([f"$N={N}$" for N in Ns])
ax2.set_ylabel("rank of $-1$ among non-residues\n(1 = largest)")
ax2.set_title("Rank of $-1\\,(\\mathrm{mod}\\,N)$ among non-residues (smaller = stronger dominance)")
ax2.invert_yaxis()
ax2.legend(loc="upper right", framealpha=0.9, fontsize=9)
ax2.grid(True, axis="y", linestyle=":", alpha=0.3)
ax2.set_ylim(max(max(ranks_13e13), max(ranks_1e12)) + 0.5, 0.5)

plt.tight_layout()
out_pdf = pathlib.Path(__file__).parent / "dominance_figure.pdf"
out_png = pathlib.Path(__file__).parent / "dominance_figure.png"
plt.savefig(out_pdf, dpi=200)
plt.savefig(out_png, dpi=200)
print("Wrote", out_pdf)
print("Wrote", out_png)
