STATUS: UNREFEREED

# FIG-1 data sources — resonance-cloud figure (arith q=3 vs non-arith G_5)

## Files used

1. **`resonance_geometry_source.json`** (this dir) — byte-identical cached
   copy of
   `.worktrees/aletheia-restore/code/out/resonance_geometry.json`
   (git-tracked in that worktree, commit `659932c` "Aletheia stack session
   artifacts 2026-08-14: controls, gates, certifications").
   - sha256 (both copies, verified identical):
     `dcdd71196521b170fff9f8e494668c838595bc4a07060d38b23053ec9c8372ac`
   - Fields plotted: `q3_even_resonances[].{re,im}` (8 points, left panel),
     `g5_even_resonances[].{re,im}` (8 points, right panel).
   - Provenance: memory note `g5-even-resonances-arithmeticity.md`
     (2026-06-20 run `bcpwjju41`), Arb Hurwitz-exact transfer-operator engine
     (`code/zeta_resonance_g5.py`, `code/zeta_cert_rosen_q5.py`), 400-bit
     precision, argument-principle winding as the interior-zero detector.
   - q=3 points: `absdet` ~ 1e-15 to 1e-16, `re_std` = 6.475e-14 across 8
     points (rigid Re=1/4 line) — cross-checked against Riemann zeta zeros
     via `t_n` (det(1-L+_s)=0 ⟺ ζ(2s)=0). **Interval-certified in the
     documented sense**: not a formal Arb ball-arithmetic certificate on
     this specific JSON's floats, but validated by the ζ(2s)=0 recovery
     cross-check to ~1e-13 vs Odlyzko zeros (see memory note).
   - G_5 points: `absdet` ~ 1e-15, `N_stable: true` (stable under precision
     bump). **Numerically validated, NOT interval-certified** — these are
     Newton-pinned double/arb roots with no rigorous enclosure. Labelled as
     such in the figure legend.

2. **Two off-line certified Selberg zero pins** (G_5 panel, black stars):
   - Pin 1: `0.4538951800749447 + 5.7635372417301305i`
   - Pin 2 (S2): `0.41054373549473627 + 7.81976824701551188i`
   - Source: `research_notes/rh_goals_2026-08-14/lane_g/S2_CONTOUR_CAMPAIGN_RECEIPT.md`
     (half-width `1e-6` box, argument-principle winding certificate,
     `W_ENVELOPE_CERT_S2_RECEIPT.json` chain). **These ARE interval-certified**
     — the strongest tier of evidence in this figure.
   - Note: pin 2's coordinates match `g5_even_resonances` point 2
     (`0.41054373549576567 + 7.819768247017059i`) to ~1e-6 — same physical
     resonance, located first by the numerical sweep and later upgraded to
     a certified box via the S2 contour campaign. They are plotted
     separately (star overlay on top of the cloud point) since they carry
     different evidence tiers.

## Gaps / caveats

- No machine-readable Q8 (depth-8, q=8) dataset was used in this figure —
  the brief asked only for arith (q=3) vs non-arith (G_5); the q8
  subdivision campaign (`Q8_D8_MERGED_CHECKPOINT.json`) is a separate
  object (Q8 boundary/winding certification, not an even-resonance list)
  and was not plotted.
- Only 8 resonance points per panel exist in the source dataset (the
  certified/validated run stopped there); the figure does not extrapolate
  or fabricate additional points.
- Legend text in `make_fig1.py` explicitly distinguishes "interval-certified"
  (q=3, and the two star pins) from "numerically validated" (G_5 cloud) —
  do not read the G_5 cloud points as certified.
