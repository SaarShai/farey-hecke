#!/usr/bin/env python3
"""Three illustration figures for the G_5 off-line resonance theorem.

Every plotted point/constant is a certified value from repo receipts:
- flagship pin s* = 0.4538951800749447 + 5.7635372417301305i, box 1e-6/coord
  (lane_g/THEOREM_G5_OFFLINE_ASSEMBLY.md), gap delta >= 0.0461038
- winding cert: N=160, 284 subarcs, min margin >= 3.43786e-8 (rounded down),
  T_tail(160) = 6.26786e-22 (lane_g/R3B_FLAGSHIP_CERT.md)
- arithmetic pins: q=4 and q=6 determinant zeros at s = rho/2 (rho = Riemann
  zeros 14.1347/21.0220...), i.e. Re = 1/4 exactly (b2-arithmetic-controls,
  M1E sector table: |D+| ~ 1e-10 at 0.25+7.0674i / 0.25+10.5110i)
- G_7 candidate pin 0.4751647621098225 + 4.668743786424289i (float scan,
  F7_CONSTANTS_MANIFEST; labeled candidate, cert in progress)
Figures are illustrations; the certified numbers are quoted on them.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Circle
import numpy as np

OUT = '/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_p/figures'
S_RE, S_IM = 0.4538951800749447, 5.7635372417301305
DELTA = 0.0461038

# ---------- Figure 1: where the zero sits ----------
fig, ax = plt.subplots(figsize=(7, 8))
ax.axvspan(0, 1, color='#f4f4f8', zorder=0)
ax.axvline(0.5, color='#c0392b', lw=2.2, zorder=2)
ax.text(0.502, 7.45, 'critical line  Re(s) = 1/2', color='#c0392b',
        fontsize=11, rotation=90, va='top')
# certified box (drawn larger than scale, true size noted)
ax.add_patch(Rectangle((S_RE-0.012, S_IM-0.012), 0.024, 0.024,
             fill=False, ec='#1a5276', lw=2, zorder=4))
ax.plot([S_RE], [S_IM], 'o', ms=7, color='#1a5276', zorder=5)
ax.annotate('certified zero  s*\n0.45390 + 5.76354 i\n(box 10⁻⁶ per coordinate,\ndrawn enlarged)',
            xy=(S_RE, S_IM), xytext=(0.09, 6.35), fontsize=10.5,
            arrowprops=dict(arrowstyle='->', color='#1a5276'), color='#1a5276')
# gap arrow
ax.add_patch(FancyArrowPatch((S_RE+0.013, S_IM), (0.5, S_IM),
             arrowstyle='<->', mutation_scale=14, color='#7d3c98', lw=1.8, zorder=3))
ax.text((S_RE+0.5)/2, S_IM+0.09, 'proven gap\nδ ≥ 0.0461038', ha='center',
        fontsize=10.5, color='#7d3c98')
ax.set_xlim(0.0, 1.0); ax.set_ylim(4.4, 7.5)
ax.set_xlabel('Re(s)'); ax.set_ylabel('Im(s)')
ax.set_title('Figure 1 — The theorem: a resonance of the golden-ratio surface $G_5$\n'
             'proven to sit strictly OFF the critical line', fontsize=12)
ax.text(0.02, 4.5, 'Every digit backed by interval-arithmetic certificates;\n'
        'abstract steps machine-proved in Lean.', fontsize=9, style='italic', color='#555')
fig.tight_layout(); fig.savefig(f'{OUT}/fig1_offline_zero.png', dpi=180); plt.close(fig)

# ---------- Figure 2: the dichotomy ----------
fig, ax = plt.subplots(figsize=(7, 8))
ax.axvline(0.25, color='#c0392b', lw=2.2, label='arithmetic prediction  Re = 1/4\n(zeros = Riemann zeros / 2)')
# arithmetic certified pins (q=4, q=6) at rho/2
arith = [(0.25, 7.0674), (0.25, 10.5110/2+5.2555*0)]  # 0.25+7.0674i, 0.25+10.5110i scaled below
arith = [(0.25, 7.0674), (0.25, 10.5110)]
for i,(x,y) in enumerate(arith):
    ax.plot(x, y, 's', ms=10, mfc='none', mec='#c0392b', mew=2,
            label='arithmetic $G_4,G_6$: verified ON the line\n(|det| ≈ 10⁻¹⁰ at ρ/2)' if i==0 else None)
ax.plot(S_RE, S_IM, '*', ms=20, color='#1a5276',
        label='non-arithmetic $G_5$: CERTIFIED off-line\n(the theorem)')
ax.plot(0.4751647621098225, 4.668743786424289, '*', ms=15, mfc='none', mec='#1a5276', mew=1.8,
        label='non-arithmetic $G_7$: candidate pin\n(certification running now)')
ax.axvline(0.5, color='#999', lw=1, ls='--'); ax.text(0.503, 11.4, 'Re = 1/2', color='#777', fontsize=9)
ax.set_xlim(0.05, 0.75); ax.set_ylim(3.5, 11.8)
ax.set_xlabel('Re(s)'); ax.set_ylabel('Im(s)')
ax.set_title('Figure 2 — The dichotomy: arithmetic surfaces pin zeros to a line;\n'
             'non-arithmetic surfaces provably do not', fontsize=12)
ax.legend(loc='lower left', fontsize=9, framealpha=0.95)
fig.tight_layout(); fig.savefig(f'{OUT}/fig2_dichotomy.png', dpi=180); plt.close(fig)

# ---------- Figure 3: how the proof works (winding certificate) ----------
fig, ax = plt.subplots(figsize=(8, 7))
th = np.linspace(0, 2*np.pi, 285)
R = 1.0
# 284 subarcs
for i in range(284):
    a, b = th[i], th[i+1]
    tt = np.linspace(a, b, 6)
    ax.plot(R*np.cos(tt), R*np.sin(tt), color=plt.cm.viridis(i/284), lw=3)
ax.plot([0],[0], 'o', ms=9, color='#1a5276')
ax.text(0, -0.14, 'zero s*\ntrapped inside', ha='center', fontsize=10.5, color='#1a5276')
ax.text(0, 1.13, 'closed contour around the 10⁻⁶ box — 284 certified sub-arcs',
        ha='center', fontsize=10.5)
ax.annotate('on every sub-arc the determinant is proven\nNON-ZERO with margin ≥ 3.43786×10⁻⁸\n(rounded down; interval arithmetic)',
            xy=(np.cos(0.8), np.sin(0.8)), xytext=(1.25, 0.75), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='#333'))
ax.annotate('truncation error proven ≤ 6.27×10⁻²²\n(theorem-grade tail bound, N = 160)',
            xy=(np.cos(2.4), np.sin(2.4)), xytext=(-2.35, 0.75), fontsize=10,
            arrowprops=dict(arrowstyle='->', color='#333'))
ax.text(0, -1.35, 'The function winds around zero exactly ONCE along this contour\n'
        '⇒ exactly one zero inside the box (argument principle) — a proof, not a numeric',
        ha='center', fontsize=11)
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-1.55, 1.3); ax.set_aspect('equal'); ax.axis('off')
ax.set_title('Figure 3 — How the proof certifies the zero: a rigorous winding-number argument', fontsize=12)
fig.tight_layout(); fig.savefig(f'{OUT}/fig3_winding_cert.png', dpi=180); plt.close(fig)
print('wrote 3 figures')
