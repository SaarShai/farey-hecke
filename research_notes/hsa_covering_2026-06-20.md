# hSuperArc covering — FAITHFUL corridor cover PROVED axiom-clean (from named realization hyp)

Date: 2026-06-21
Files: `projects/hsa_covering_lean/RequestProject/Main.lean` (deliverable, axiom-clean),
`projects/hsa_covering_lean/aristotle_covering/` (single-`sorry` Aristotle package).

## Result

The covering target `hSuperArc_Tgen` that the reformulated keystone
`MuCloseHMmap.Xomega_ge_via_Tgen` (`projects/mu_close_hMmap_lean`) consumes is DISCHARGED, in its
FAITHFUL form, axiom-clean `[propext, Classical.choice, Quot.sound]` (NO `sorryAx`), from two NAMED
inputs (the realization bridge `pgen_orbit_realization` + the genuine deep-mid one-step ejection,
both carried as explicit lemma hypotheses).

`lake env lean` EXIT 0; all 12 theorems `depends on axioms: [propext, Classical.choice, Quot.sound]`.

## The load-bearing honesty finding: the keystone's literal `= Set.univ` is FALSE

`Xomega_ge_via_Tgen` (and B3's `covering_pos_measure`) demand
`(⋃ k<q, (Tgen^[k])⁻¹' {1/l³ ≤ Pgen}) = Set.univ`. That literal target is **FALSE**:
`superarc_univ_is_false` (PROVED here) exhibits the cusp tip `(0,0)`, an `Mmap`/`Tgen` fixed point
with `Pgen(0,0)=0 < 1/l³`, whose orbit never hits the super-threshold set.

The FAITHFUL covering is the one valid on the conull corridor section `Sclosed` (the keystone's
`μ (Sclosed)ᶜ = 0`): `covering_pos_measure` needs only POSITIVE `μ`-mass of the super-level set, and
a conull cover delivers exactly that. Note `(0,0) ∉ Sclosed` (since `Sclosed ⊆ Taha` requires
`0 < a`), so the conull cover is NOT contradicted by the `(0,0)` counterexample.

## What is PROVED (axiom-clean)

- `cos_grid_hit` — discrete rotation-arc pigeonhole (the `q` phases `φ+2kθ`, spacing `2π/q`, hit any
  super-arc of half-width `≥ θ`). [reproduced verbatim from the hSuperArc attempt]
- `orbit_hit_of_realization` — realization datum `Pgen(orbit_k)=C0+R·cos(φ+2kθ)`, `R>0`, gate
  `(t−C0)/R ≤ cos θ` ⟹ some `k<q` clears `t`.
- `wide_arc_translates_cover_on`, `corridor_cover` — per-point hit ⟹ preimage inclusion.
- `orbit_hit_corridor` — **the assembly**: split `Dom` by `isK1`; on `isK1` (k₀=1 rotation-arc)
  points use the realization hyp + pigeonhole; on `¬isK1` (k₀≥2 deep-mid) points use the one-step
  ejection. Conclusion: every corridor point hits within `q` `Tgen`-steps.
- `SuperArcCover_corridor` — the FAITHFUL `hSuperArc` inclusion `Dom ⊆ ⋃ k<q, (Tgen^[k])⁻¹' {t≤Pgen}`
  from the two named inputs.
- `covering_pos_measure_ae` — conull cover (`μ Domᶜ=0`) + measure-preservation ⟹ `0 < μ {t≤Pgen}`
  (the honest replacement of B3's `= Set.univ` `covering_pos_measure`).
- `member_lb_via_Tgen_ae`, `XomegaSet_bddBelow_via_Tgen_ae`, `Xomega_ge_via_Tgen_ae` — the keystone
  lower bound `1/l³ ≤ Xomega` REWIRED to consume the conull cover (faithful replacement of
  `Xomega_ge_via_Tgen`, whose literal `= Set.univ` hypothesis can never be supplied).
- `essSup_ge_of_pos_superlevel`, `superlevel_measurableSet`, `Pgen_measurable` — wrapper plumbing
  (verbatim from B3).
- `superarc_univ_is_false` — the honest negative.

## The single residual: `pgen_orbit_realization` (P-realization's job, not this /goal)

The covering's only open content is the realization bridge — supplied by the P-realization agent and
substituted by the main loop. It is carried here as the explicit `hRealize` hypothesis of
`orbit_hit_corridor`/`SuperArcCover_corridor`, so the covering is PROVED from it. The Aristotle
package `aristotle_covering/` states it concretely (scout's Form A, with the load-bearing
`hE : Efloor ≤ Eform l p`) as a single `sorry` and `covering_from_realization` wires it through the
proved `SuperArcCover_corridor` (sole `sorryAx` traces to that one `sorry`).

## Faithfulness to the keystone

`member_lb_via_Tgen_ae` reuses the sealed `Pgen`, `XomegaSet`, `Xomega`, threshold `1/l³`, the
`Tgen`-iterate dynamics, and the measure-side `hinv.iterate` discharge VERBATIM from
`mu_close_hMmap`'s `member_lb_via_Tgen`; the ONLY change is the covering hypothesis (conull inclusion
instead of `= Set.univ`). This is the honest, true statement; the `= Set.univ` form is false and
documented as such.

## Aristotle submission status — BLOCKED (environment)

Submission of `aristotle_covering/` could not complete: the Aristotle API key in `~/.farey_api_keys`
is rejected ("Invalid API key") — confirmed independently by `aristotle list` also failing. This is
an environmental/key-expiry issue, NOT a defect in the project. The package is authored, elaborates
with exactly one `sorry` (`pgen_orbit_realization`, line 472), and is ready to resubmit once a valid
key is available. See `aristotle_covering/submit.log`, `aristotle_covering/PROMPT.md`.

## Verify command

```
cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15 && \
  lake env lean /Users/za/Documents/farey-hecke/projects/hsa_covering_lean/RequestProject/Main.lean
```
EXIT 0; 12 theorems `[propext, Classical.choice, Quot.sound]`, no `sorryAx`.
