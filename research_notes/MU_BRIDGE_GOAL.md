# GOAL — μ-bridge: fully unconditional all-q  X_Ω(q) ≥ 1/λ³

Date 2026-06-20. Target: wire the MACHINE-VERIFIED energy/no-dwell wrapper
`hCorr_uniform_via_energy` (projects/hmeas_lean, projects/uniform_qge22_energy_lean) into
the genuine ergodic-optimization class `XomegaSet` (OnsetEquality.lean:352) so the corridor
confinement is discharged for ALL q (esp. q≥22), yielding `Xomega_ge` unconditionally for
every Hecke q — the keystone of the Koyama joint paper.

KEY FACTS (already proved/sealed — no open math remains, only the bridge):
- `MeasurePreserving(Tgen) μ μ` is DEFINITIONAL (inside XomegaSet); not a gap.
- The real q≥22 blocker = the confinement input `hFW`/`hCorr` (F-window caps at 21).
- Energy wrapper proved: covering + measure-preservation ⇒ essSup ≥ t (axiom-clean).
- `hmeas` measure-half proved (det M=1 volume; iterate lemma); reduces to Tgen-invariance.
- L1b arc-coverage SEALED (`L1bArcCoverage.fcorr_lb`/`.B1_target`/`arc_coverage_ineq`).
- `Mmat_conj_eq_rot`, `Mmap_preserves_E`, `genuine_step_eq_Mmap` (M = Tgen on k=1 block).

## Bridge pieces (parallel)
- **B1 measure-bridge** — from definitional `MeasurePreserving(Tgen) μ μ` derive the block-iterate
  `hmeas : ∀k<q, MeasurePreserving (g k) μ μ` the wrapper consumes (g k = block step iterate;
  block step = Tgen on the k=1 cluster region). The subtle partial-map piece.
- **B2 covering-bridge** — from sealed L1b arc-coverage derive the wrapper's covering / `hSuperArc`
  (the q π/q-translates of the super-threshold arc cover the circle).
- **B3 observable+assembly-prep** — identify wrapper `P=Pgen`, `t=1/λ³`; super-level set
  measurability + a.e.-boundedness (from XomegaSet); draft `Xomega_ge_allq` skeleton consuming B1+B2.

## Integration (main loop)
Assemble B1+B2+B3 → unconditional `Xomega_ge_allq` (∀ Hecke q); re-elaborate (lake env lean,
0 sorry, axiom-clean) + FAITHFULNESS (statement = the real XomegaSet_bddBelow / Xomega_ge, not
weakened); submit to Aristotle; commit. HONEST: hard formalization; partial (bridges discharged,
hard step scoped) is an acceptable, theorem-advancing outcome. No overclaim.

## Rules (every agent; hooks don't fire in subagents)
READY FOR JUDGING not "done"; attempts+assumptions; quote smoke. Write ONLY assigned disjoint
paths; no git; no key echo. Reuse sealed definitions verbatim — a vacuous/weakened statement that
elaborates is the worst failure. Distinguish PROVED / reduced-to-named-hyp / open.
