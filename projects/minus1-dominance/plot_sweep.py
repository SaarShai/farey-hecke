#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_sweep.py -- visualize the option-3 variance-ordering sweep.

Reads sweep_results.tsv (cols: q phi n_nr rank_minus1 is_max V_minus1 argmax_m
V_argmax margin) and produces sweep_plot.png:
  (top)    V(q;-1,1) vs q (the maximal RS variance), with the parity-gap scale 2*phi*log2;
  (bottom) the margin V(-1) - max_{a != -1} V(a) vs q -- positive everywhere means -1 is the
           unique variance-MAX non-residue; exceptions (margin <= 0) are marked in red.
"""
import sys, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PATH = sys.argv[1] if len(sys.argv) > 1 else "sweep_results.tsv"
rows = []
with open(PATH) as f:
    for ln in f:
        if ln.startswith('q\t') or not ln.strip():
            continue
        p = ln.split('\t')
        q = int(p[0]); phi = int(p[1]); ismax = int(p[4])
        Vm1 = float(p[5]); margin = float(p[8])
        rows.append((q, phi, ismax, Vm1, margin))
rows.sort()
qs = [r[0] for r in rows]
phis = [r[1] for r in rows]
Vm1 = [r[3] for r in rows]
margins = [r[4] if math.isfinite(r[4]) else float('nan') for r in rows]
exc = [(r[0], r[4]) for r in rows if r[2] == 0]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax1.plot(qs, Vm1, '.', ms=2, color='C0', label=r'$V(q;-1,1)$ (max RS variance)')
ax1.plot(qs, [2 * ph * math.log(2) for ph in phis], '-', lw=0.8, color='C3',
         label=r'parity-gap scale $2\varphi(q)\log 2$')
ax1.set_ylabel('limiting RS variance')
ax1.set_title(r'Option-3 sweep: $a=-1$ is the variance-MAX (least-biased) non-residue, '
              r'primes $q\equiv 3\,(4)$ (GRH+LI)')
ax1.legend(fontsize=8); ax1.grid(alpha=0.3)

good_q = [q for q, _, im, _, _ in rows if im == 1]
good_m = [m for q, _, im, _, m in rows if im == 1 and math.isfinite(m)]
gq = [q for q, m in zip(good_q, good_m)]
ax2.plot(gq, good_m, '.', ms=2, color='C2',
         label=r'margin $V(-1)-\max_{a\neq -1}V(a)>0$  ($-1$ is unique max)')
ax2.axhline(0, color='k', lw=0.6)
if exc:
    ax2.plot([e[0] for e in exc], [e[1] for e in exc], 'rx', ms=8,
             label=f'EXCEPTIONS ({len(exc)})')
ax2.set_xlabel('q'); ax2.set_ylabel('variance margin')
ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("sweep_plot.png", dpi=130)
print(f"wrote sweep_plot.png  ({len(rows)} primes, {len(exc)} exceptions)")
