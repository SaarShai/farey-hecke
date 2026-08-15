# M1g upgrade: theorem-grade winding certificates for the 8 predicted resonances

- status: open
- kind: research (certification engineering)
- mode: AFK (builder/codex) + frontier gate
- created: 2026-08-15 (overnight run, from M1g honest 0/8)
- blocked by: none
- claimed by: none

## Goal
Promote the 8 predicted scattering resonances (q=4: iπ/log2, 3iπ/log2 trivial;
2iπ/log2, 4iπ/log2 χ. q=6: same with log3) from sampled-winding evidence
(M1G_PREDICTION_WINDING_CERTS.md: winding balls ~1 ± 1e-4..1e-10, but tail
heuristic) to rigorous Fredholm-determinant zero certificates.

## Work items
1. Replace the even-q `dimension_tail_heuristic` (4×max(center,corners)
   inflation) with a proven uniform boundary tail bound, following the R3b
   pattern (T_tail from ‖L‖₁-type envelope; round margins DOWN).
2. Add a `det(1+L₊)` (χ-sector) winding entry point to the even-q contour
   routine — currently absent (TypeError on determinant_sector kwarg).
3. Re-run all 8 boxes; then also winding=0 checks in the opposite sector.
4. Frontier gate: verify the tail bound derivation before any CERTIFIED label.

## Why it matters
Certified extra resonances at p^s = ±1 are the checkable prediction of the
M1f scattering identification (G5 closed); certification upgrades the
mechanism's confirmation from numerics to theorem-grade at 8 points.

## Receipts
lane_g/M1G_PREDICTION_WINDING_CERTS.md + m1g_receipts/ (honest 0/8 baseline).
