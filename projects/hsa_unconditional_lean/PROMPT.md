# RequestProject — FINAL INTEGRATION of the all-`q` onset lower bound `1/λ³ ≤ X_Ω`

## Goal

Assemble the already-proved, axiom-clean pieces (realization bridge + covering engine + deep-mid
ejection) into a single keystone

> `Xomega_ge_unconditional : 1/l³ ≤ Xomega l Tgen Sclosed`

with `XomegaSet`/`Xomega`/`Pgen`/`Tgen` spelled VERBATIM (the conclusion is the GENUINE onset
value, no redefinition), re-keyed from the FALSE `= Set.univ` covering to the TRUE
a.e.-on-`Sclosed` (conull) covering.

## What is PROVED here (sorry-free, axiom-clean `[propext, Classical.choice, Quot.sound]`)

* `pgen_orbit_realization` — orbit sinusoid identity + E-floor gate on the `Mmap` orbit (verbatim
  reproduction of `hsa_realization_lean`, with its `recur_closed_form`/`recur_to_Rcos` helpers).
* the covering engine `cos_grid_hit`, `orbit_hit_of_realization`, `wide_arc_translates_cover_on`,
  `corridor_cover`, `orbit_hit_corridor`, `SuperArcCover_corridor`, `covering_pos_measure_ae`,
  `essSup_ge_of_pos_superlevel`, `member_lb_via_Tgen_ae`, `XomegaSet_bddBelow_via_Tgen_ae`,
  `Xomega_ge_via_Tgen_ae` (verbatim reproduction of `hsa_covering_lean`).
* `realize_from_orbit_realization` — **the integration lemma**: discharges the abstract `hRealize`
  datum from `pgen_orbit_realization`, transporting the `Mmap` orbit to the `Tgen` orbit via the
  carried orbit-agreement hypothesis and supplying the E-floor.
* `conull_cover_assembled` — the FAITHFUL conull cover from `pgen_orbit_realization` + the named
  deep-mid ejection through `SuperArcCover_corridor`.
* `Xomega_ge_unconditional` — **the final integrated keystone**, the genuine `1/l³ ≤ Xomega`.

## HONEST residual list of `Xomega_ge_unconditional` (NOT yet unconditional)

DEFINITIONAL Hecke facts: `hm` (`1 ≤ m`), `hl` (`l = lamq (m+2)`), `hne` (cusp Dirac inhabits the
class), `hpcorr` (section ⊆ corridor).

NON-DEFINITIONAL residuals (the genuine open content):
* `hEfloor` — corridor E-floor `EfloorQ ≤ Eform` on the `k=1` part (L1b arc-coverage; interval-
  certified `q≤200`, uniform-`q` OPEN).
* `hOrbitAgree` — interior-`k=1` confinement `Tgen^[k] p = (Mmap l)^[k] p` (R1-upper residual).
* `hEjectStep` — deep-mid one-step ejection (= sealed `GenuineSelfMap.genuine_hEject_deepmid`,
  axiom-clean over the sealed infrastructure; named here because this file is self-contained).

So the theorem is FAITHFUL and `sorryAx`-free, but carries `hEfloor`, `hOrbitAgree`, `hEjectStep`.

## Build

```
( cd <repo>/projects/aristotle_dispatch_v15 && \
  lake env lean <repo>/projects/hsa_unconditional_lean/RequestProject/Main.lean )
```
Elaborates clean (EXIT 0; two benign linter warnings — a deprecation alias and one unused
hypothesis carried for signature fidelity). The `#print axioms` block at the end shows all 10
results `[propext, Classical.choice, Quot.sound]`, NO `sorryAx`.
