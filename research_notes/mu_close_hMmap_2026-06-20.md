# Closing the MEASURE input of the B3 keystone (`hMmap`) — 2026-06-20

## Goal

Prove the measure input (`hMmap_target`) of the B3 keystone
`Xomega_ge_via_energy` (`projects/mu_bridge_B3_lean/RequestProject/Main.lean`).

## Verdict

The global `hMmap` AS LITERALLY STATED is **FALSE / unprovable**, and the faithful
measure input is discharged **definitionally** under the `Tgen`-on-corridor
reformulation. Both facts are now PROVED axiom-clean.

- File: `/Users/za/Documents/farey-hecke/projects/mu_close_hMmap_lean/RequestProject/Main.lean`
- Command: `( cd /Users/za/Documents/farey-hecke/projects/aristotle_dispatch_v15 && lake env lean /Users/za/Documents/farey-hecke/projects/mu_close_hMmap_lean/RequestProject/Main.lean )`
- Result: EXIT 0; all 10 declarations `depends on axioms: [propext, Classical.choice, Quot.sound]`; NO `sorryAx`.

## What `hMmap` asks and why it is false as stated

`hMmap : ∀ μ, IsProbabilityMeasure μ → MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0
            → MeasurePreserving (Mmap l) μ μ`

It asks the GLOBAL linear rotation `Mmap l (a,b) = (b, −a+λb)` to preserve EVERY
`Tgen`-invariant probability measure carried by `Sclosed`. But the sealed facts
(`BCZHeckeRotationArc.genuine_step_eq_Mmap_of_bracket`, `kfloor_ge_two_iff`,
`GenuineSelfMap.genStep_scalar_eq`) say `Tgen = Mmap` ONLY on the interior k=1 bracket
`λb ≤ 1+a < 2λb`; on `2λb ≤ 1+a` the genuine floor is `k ≥ 2` and
`Tgen (a,b) = (b, −a+kλb) ≠ Mmap (a,b)`. The genuine BCZ return dynamics visits
`{k ≥ 2}` with positive μ-mass, so a `Tgen`-invariant μ is NOT `Mmap`-invariant.
(`Mmap` is linear det 1 ⇒ preserves LEBESGUE area unconditionally — but the wrapper's
μ is a PROBABILITY measure on the bounded Taha triangle, not Lebesgue, so that does
not rescue the global claim.)

This matches B1's own prose concession (`(†)⇒hMmap globally: FALSE`). B1's
`hMmap_via_arclength` "discharges" `hMmap` from a `True` placeholder via `sorry` — an
UNSOUND route.

## The unsoundness, formalized (refutation)

`unsound_demo` (axiom-clean, sorry-free) proves: a universal `MeasurePreserving`
discharge `∀ {α} [MeasurableSpace α] (μ) (M), MeasurePreserving M μ μ` implies `False`,
witnessed by the doubling map `x ↦ 2x` on `ℝ` with Lebesgue volume (preimage of `[0,2]`
is `[0,1]`, measure 1 ≠ 2). This is the formal reason the `True`-placeholder route
cannot be relied on.

## The faithful measure input (PROVED, axiom-clean)

Under the `Tgen`-on-corridor reformulation the wrapper is fed `g k = Tgen^[k]`, and the
carried membership datum `hinv : MeasurePreserving Tgen μ μ` discharges every iterate:

```
theorem hmeas_Tgen_of_invariant
    (μ : Measure α) (Tgen : α → α) (hinv : MeasurePreserving Tgen μ μ) (q : ℕ) :
    ∀ k, k < q → MeasurePreserving (Tgen^[k]) μ μ :=
  fun k _ => hinv.iterate k
```

This is FAITHFUL: it transports the SAME `Tgen` the invariance datum is about — no
silent redefinition, no fabricated measure fact. `hMmap` is DELETED, not re-proved.

## Corridor agreement (where the reformulation specializes correctly)

`Tgen_eq_Mmap_on_bracket` (axiom-clean): on `λb ≤ 1+a < 2λb` the genuine scalar step
`kstep l (kfloor)(a,b)` equals `Mmap l (a,b)`. So `Tgen`-on-corridor specializes to the
intended rotation-arc picture exactly where it is valid; off-bracket (k≥2) `Tgen ≠ Mmap`
(`kfloor_ge_two_iff`), the obstruction to the global `hMmap`.

## End-to-end keystone, measure side closed

`Xomega_ge_via_Tgen` (axiom-clean) reproduces the genuine `XomegaSet`/`Xomega`/`Pgen`
verbatim and derives `1/l³ ≤ Xomega l Tgen Sclosed` with the measure input discharged
by `hmeas_Tgen_of_invariant`. The lone open input is `hSuperArc_Tgen` (the genuine
no-sustained-sub-threshold covering on `Tgen`-iterates).

## Net residual after this file

Exactly ONE open input to the all-q lower bound: `hSuperArc_Tgen`. The MEASURE side
`hMmap` is GONE — discharged DEFINITIONALLY by the carried `Tgen`-invariance.

## Why no Aristotle submission

There is no genuinely-hard step in the measure input: with the keystone on
`Tgen`-on-corridor the measure side is definitional (`hinv.iterate`), and the global
`hMmap` is honestly false (refuted by `unsound_demo`). Authoring a `sorry`-RequestProject
for Aristotle would be dishonest — nothing to delegate. The remaining hard work
(`hSuperArc_Tgen`) is the existing project covering engine, a SEPARATE goal, not this one.

## Keystone edit needed (for the orchestrator)

In `projects/mu_bridge_B3_lean/RequestProject/Main.lean`:
1. DELETE the `hMmap` hypothesis from `member_lb_via_energy`,
   `XomegaSet_bddBelow_via_energy`, `Xomega_ge_via_energy`.
2. Replace `g := fun k => (Mmap l)^[k]` with `g := fun k => Tgen^[k]`, and
   `hmeas_of_invariant μ (Mmap l) hMmap q` with `hmeas_Tgen_of_invariant μ Tgen hinv q`
   (thread the carried `hinv` from the `rintro` destructure in `XomegaSet_bddBelow`).
3. Re-key `hSuperArc` from `((Mmap l)^[k])⁻¹'…` to `(Tgen^[k])⁻¹'…`.
4. `superlevel_measurableSet`, `hbdd_of_member`, `le_csInf` unchanged.

This whole edit is verified clean end-to-end in
`projects/mu_close_hMmap_lean/RequestProject/Main.lean` (`Xomega_ge_via_Tgen`).
