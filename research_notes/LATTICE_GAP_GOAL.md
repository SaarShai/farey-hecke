# GOAL — attack the lattice-gap residual (hOrbitAgree) + the E-floor (hEfloor)

Date 2026-06-20. The two non-definitional residuals of the faithful, sorryAx-free
`Xomega_ge_unconditional` (projects/hsa_unconditional_lean, commit 0b93aef). Closing them →
fully unconditional all-q X_Ω(q) ≥ 1/λ³; hOrbitAgree is shared with the B(q) exact-value theorem.

## The key angle to test FIRST (may dissolve the lattice-gap)
hOrbitAgree as stated = uniform interior-k=1 confinement `Tgen^[k]=Mmap^[k]` (the R1-upper /
inhomogeneous-Diophantine / parity-resonance residual). BUT the cover only needs
"1/λ³ ≤ Pgen reached within q steps." Every orbit step is EITHER:
  (a) k=1  → Tgen=Mmap (genuine_step_eq_Mmap_of_bracket); the rotation sweeps the super-arc
            within q steps by sealed L1b (arc_coverage_ineq / B1_target), OR
  (b) k≥2  → genuine_hEject_deepmid clears the threshold in ONE step.
This dichotomy is EXHAUSTIVE (kfloor is 1 or ≥2). So uniform confinement may be UNNECESSARY:
the threshold is cleared within q steps either way. If the per-run L1b coverage applies to a
k=1 run of length L≤q (not requiring a full-q run), hOrbitAgree dissolves WITHOUT the lattice-gap.
Risk: L1b arc-coverage may assume q consecutive k=1 steps from one phase; a short run that ejects
early must then be covered by the ejection step — verify that composition holds.

## Pieces (parallel)
- **R-confinement** — resolve hOrbitAgree. FIRST try the exhaustive-dichotomy reformulation
  (cover from per-run L1b on the k=1 run + ejection on k≥2, eliminating uniform confinement).
  If genuinely needed, attack the equal-spacing/parity lattice-gap directly (rotation number
  1/(2q) RATIONAL → equally-spaced lattice; resonance_parity_gate PROVED). Lean + Aristotle.
- **R-efloor** — prove the uniform corridor E-floor hEfloor (E bounded below on Dcorr away from
  the cusp tip), via the closed-form conserved-ellipse geometry. Kaggle to verify uniformity
  across q; Lean + Aristotle for the bound.

## Integration (main loop)
Substitute the closed residual(s) into Xomega_ge_unconditional; re-elaborate (no sorryAx) +
faithfulness; commit. HONEST: this is the program's central hard residual — an honest "dissolved
via dichotomy" OR "reduced to a finite per-q check" OR "precise obstruction identified" are all
valuable outcomes. Do NOT claim unconditional unless the assembled theorem carries no
non-definitional hypothesis and depends on no sorryAx.

## Rules (every agent; hooks don't fire in subagents)
READY FOR JUDGING not "done"; attempts+assumptions; quote lake EXIT+axioms. Write ONLY assigned
disjoint paths; no git; no key echo. Reuse sealed defs VERBATIM — a vacuous/weakened statement
that elaborates is the worst failure. Distinguish PROVED / reduced / OPEN.
