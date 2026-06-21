# RequestProject — Uniform `hCorr` for `q ≥ 22` via the energy / escape-of-mass route

## Goal

Replace the per-`q` fixed-window confinement (which provably caps at `q ≤ 21`, since
the cluster ceiling `B(q) ∼ 0.216 q` outgrows any fixed window length) with ONE
`q`-independent measure-theoretic argument that discharges the named hypothesis `hCorr`
of `ToplevelStitch.Xomega_lb_allq`:

> `hCorr :  1/λ³ ≤ ess-sup_μ P_gen`   — no genuine invariant probability measure is
> supported entirely in the sub-threshold sector `{P_gen < 1/λ³}`.

## What is already PROVED in this file (`RequestProject/Main.lean`, sorry-free, axiom-clean)

All four declarations print axioms `[propext, Classical.choice, Quot.sound]`:

1. `covering_pos_measure` — **the measure-theoretic no-dwell core.** If `μ` is a
   probability measure, `g 0,…,g (q-1)` are `μ`-measure-preserving, `S` measurable, and
   the preimages `g k ⁻¹' S` (`k < q`) COVER the space, then `μ S > 0`. Pure measure
   theory, q-independent.
2. `essSup_ge_of_pos_superlevel` — `μ {x | t ≤ P x} > 0 ⇒ t ≤ ess-sup_μ P`.
3. `hCorr_uniform_via_energy` — **the assembly.** Chains 1+2: given the block-rotation
   iterates are measure-preserving and the super-threshold set's `q` translates cover the
   space (`hSuperArc`), delivers `t ≤ ess-sup_μ P` — the exact `hCorr` conclusion — for
   every `q ≥ 1`, with NO per-`q` window.
4. `ampq_pos` — the block amplitude `√(1+2λ²) > 0`.

## The ONE genuinely hard input (named hypothesis `hSuperArc`, NOT a sorry)

`hSuperArc : (⋃ k ∈ Finset.range q, g k ⁻¹' {x | t ≤ P x}) = Set.univ`

This is the **L1b super-arc covering**: the `q` rotation-translates (by `2π/q`) of the
super-threshold arc cover the circle. It holds because the super arc occupies a UNIFORM
fraction `≈ 0.872` of the period (super-arc half-width fraction `(1−C)/2 ≈ 0.436`,
`C = 2arccos(2√6/5)/π ≈ 0.1282`), so a wide arc's `q` equally-spaced translates always
tile the circle (`2·0.436π ≫ 2π/q` for every `q`; numerically validated
`code/uniform_qge22/covering_lemma.py`).

The super-arc NON-emptiness with that uniform fraction is exactly the sealed
`L1bArcCoverage.fcorr_lb` (PROVED) and `arc_coverage_ineq : 2·arccos(2√6/5)/π < 33/256`
(PROVED). What is NOT yet assembled — and is the residual the next agent should target —
is:

- the **realization bridge**: that the GENUINE block observable's super-threshold set is
  (a.e.) this wide arc on the block ellipse (the `hbridge` / `g_corr ≤ g_true` link of the
  energy-route note), AND
- the **block-rotation = `q` measure-preserving iterates** structure (the genuine
  corridor block map's measure-preserving assembly, GAP-3).

These are the two un-assembled measure steps. The pure analytic super-arc width inequality
is sealed; the pure measure-theoretic wrapper is now proved here.

## Honest residual (the exact open inequality)

The single open analytic inequality of the WHOLE route remains the sealed **L1b**:
for all `q ≥ 18`, `1/λ³ ≤ g_corr(L_blk q, q)` with `L_blk q = ⌈33q/256⌉+2`, whose
`q`-independent geometric heart `2·arccos(2√6/5)/π < 33/256` is already proved. This file
adds nothing to L1b; it proves the measure-theoretic wrapper that L1b feeds into, which was
previously only heuristic. The remaining un-formalized step is the dynamical realization
(`hSuperArc` from L1b on the genuine block ellipse) — routine-but-substantial measure
assembly, NOT a new analytic crux.

## Build

```
( cd <repo>/projects/aristotle_dispatch_v15 && \
  lake env lean <repo>/projects/uniform_qge22_energy_lean/RequestProject/Main.lean )
```
Elaborates clean (only unused-variable warnings); `#print axioms` block at the end shows
all four results axiom-clean.
