# μ-bridge reformulation — global-Mmap vs Tgen-on-corridor (2026-06-20)

## Verdict (one line)

`hMmap` as literally stated in the B3 keystone (global `Mmap` preserves any
`Tgen`-invariant `μ` carried by `Sclosed`) is **NOT provable / generically FALSE**.
The faithful fix is to **drop `hMmap` entirely** and feed the wrapper the carried
map `Tgen` (definitionally `μ`-preserving) instead of the global `Mmap`, running the
covering on `Tgen`-iterates. This still concludes the genuine `1/l³ ≤ Xomega l Tgen Sclosed`,
and it ALIGNS the keystone with the project's own genuine no-sustained-sub-threshold engine.

## Why `hMmap` (as stated) is false off-corridor

Sealed facts (`GenuineSelfMap.lean`, `BCZHeckeRotationArc.lean`):

- `Tgen` on the scalar branch is `(a,b) ↦ (b, −a + kλb)` with the **genuine floor**
  `k = ⌊(1+a)/(λb)⌋` (`genStep_scalar_eq`, `genFloor`).
- `Mmap l (a,b) = (b, −a + λb)` is the **k = 1 special case**.
- `genuine_step_eq_Mmap_of_bracket`: `Tgen = Mmap` **only** on the interior k=1 bracket
  `λb ≤ 1+a < 2λb`.
- `kfloor_ge_two_iff`: on `2λb ≤ 1+a` the floor is `k ≥ 2`, where `Tgen ≠ Mmap`.

The BCZ return dynamics **requires** k ≥ 2 floor increments (the cusp-excursion / ejection
events; cf. `Bq_rotation_arc_2026-06-14.md`: "the genuine orbit must hit k ≥ 2 eventually").
So the set `{k ≥ 2}` carries positive `μ`-mass for the genuine invariant `μ`. On that set the
map fed to `μ`'s invariance (which is `Tgen`) is NOT `Mmap`. Therefore:

> `MeasurePreserving Tgen μ μ`  does NOT imply  `MeasurePreserving (Mmap l) μ μ`.

The B1 file already concedes this in prose ("`(†) ⇒ hMmap` globally: **FALSE**", B1 §3) and its
attempted discharge `hMmap_via_arclength` proves `MeasurePreserving M μ μ` from a `True`
placeholder — i.e. it is **vacuous/unsound as written** (would prove every map preserves every
measure). That is the worst-failure pattern the honesty rule warns about; it must not be relied on.

Note `Mmap` IS linear with `det = 1` (`hmeas_lean.block_iterate_volume_preserving`), so it preserves
**Lebesgue volume** unconditionally — but the `XomegaSet` member `μ` is a *probability* measure
supported on `Sclosed` (closure of the bounded Taha triangle), NOT Lebesgue. Volume-preservation of
`Mmap` does not transfer to the singular/compactly-supported invariant `μ`. So even the cleanest true
fact about `Mmap` does not rescue global `hMmap` for the relevant `μ`.

## The correct formulation

Replace the global-`Mmap` dynamics by `Tgen` itself in BOTH wrapper inputs:

- The wrapper's `hmeas` slot becomes `∀ k < q, MeasurePreserving (Tgen^[k]) μ μ`, discharged
  for FREE from the carried `hinv : MeasurePreserving Tgen μ μ` via `MeasurePreserving.iterate`.
  No new hypothesis — it is definitional class membership data. `hMmap` is **eliminated**.
- The covering slot becomes the `Tgen`-iterate covering (one residual; see `hSuperArc_target`).

This is faithful because (i) `XomegaSet` is unchanged (verbatim), (ii) the conclusion is the
genuine `1/l³ ≤ Xomega l Tgen Sclosed`, (iii) the dynamics actually fed in is the SAME `Tgen` the
membership datum is about — no silent redefinition. On the k=1 corridor `Tgen = Mmap`, so this
*specializes to* the intended rotation picture exactly where that picture is valid; off-corridor it
uses the honest genuine map rather than an unprovable global-rotation claim.

## hMmap_target (the provable, faithful replacement)

There is NO separate measure-input target. The measure side is discharged definitionally:

```
hmeas_Tgen : ∀ k, k < q → MeasurePreserving (Tgen^[k]) μ μ
           := fun k _ => hinv.iterate k          -- hinv carried by XomegaSet membership
```

i.e. the faithful "measure target" is the trivial `hinv.iterate` step. `hMmap` is deleted.

## hSuperArc_target (the provable, faithful covering)

```
hSuperArc_Tgen :
  ∀ μ, IsProbabilityMeasure μ → MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0 →
    (⋃ k ∈ Finset.range q, (Tgen^[k]) ⁻¹' {x | 1/l^3 ≤ Pgen l x}) = Set.univ
```

(or, weakened to a μ-a.e. cover on `Sclosed` if one prefers to match the engine exactly —
either suffices, since `covering_pos_measure` only needs positive measure of the super-level set).

This is the **genuine no-sustained-sub-threshold fact** the project already owns:
`essSup_ge_of_no_sustained_strict` / `no_sustained_corridor` /
`genuine_no_sustained_cusp_discharged` ("the genuine orbit cannot sustain sub-threshold `Pgen`
for q consecutive steps", `BCZHeckeUniformOnset.lean:204`). On the k=1 corridor it reduces, via
`genuine_step_eq_Mmap_of_bracket`, to the sealed L1b rotation-arc width bound (`arc_coverage_ineq`,
`B1_target`); the k≥2 ejection steps land **above** threshold by the deep-mid ejection lemma
(`GenuineSelfMap.genuine_hEject_deepmid`: `1/l³ ≤ Pgen(genStep)` at k≥2 branches), so they only
HELP the cover. This is why the covering is genuinely true on `Tgen`-iterates whereas the
`Mmap`-iterate covering (B2 `super_arc_hit_within_q`, asserted on ALL of `ℝ×ℝ` incl. off-ellipse /
b≤0 junk) was itself an over-strong proxy.

## Reformulation needed? YES (keystone instantiation edit)

Minimal faithful change to `projects/mu_bridge_B3_lean/RequestProject/Main.lean`:

- DELETE the `hMmap : … → MeasurePreserving (Mmap l) μ μ` hypothesis from
  `XomegaSet_bddBelow_via_energy` and `Xomega_ge_via_energy`.
- In `member_lb_via_energy`, replace `g := fun k => (Mmap l)^[k]` by `g := fun k => Tgen^[k]`,
  and replace `hmeas_of_invariant μ (Mmap l) hMmap q` by `fun k _ => hinv.iterate k`
  (the carried `hinv` from membership; pass it down).
- Re-key `hSuperArc` from `((Mmap l)^[k])⁻¹' …` to `(Tgen^[k])⁻¹' …` (the `hSuperArc_target` above).
- The `superlevel_measurableSet`, `hbdd_of_member`, `le_csInf` steps are unchanged.

Conclusion `1/l³ ≤ Xomega l Tgen Sclosed` is **retained intact** — verified below.

`Mmap` / `BCZHeckeRotationArc` are NOT discarded: they remain the corridor-local computation that
PROVES `hSuperArc_Tgen` on the k=1 arc (`genuine_step_eq_Mmap_of_bracket` + L1b). They move from
being a (false) global measure hypothesis to being the right tool inside the (true) covering proof.

## Elaboration evidence

File: `projects/mu_bridge_reformulation_scratch/Reform.lean` (verbatim wrapper cores + the
reformulated `member_lb_via_Tgen` / `XomegaSet_bddBelow_via_Tgen` / `Xomega_ge_via_Tgen`).

Command:
```
cd projects/aristotle_dispatch_v15 && lake env lean .../Reform.lean
```
Output:
```
'Reform.Xomega_ge_via_Tgen' depends on axioms: [propext, Classical.choice, Quot.sound]
```
EXIT 0. **No `sorryAx`.** The reformulated keystone elaborates axiom-clean and still delivers
`1/l^3 ≤ Xomega l Tgen Sclosed` from the SINGLE residual `hSuperArc_Tgen` (no `hMmap`).

## Residual after reformulation

Exactly ONE open input remains for fully-unconditional all-q `X_Ω(q) ≥ 1/λ³`:
`hSuperArc_Tgen` (the genuine no-sustained-sub-threshold covering on `Tgen`-iterates), which is the
project's own already-scoped L1b / no-sustained engine — NOT a new gap, and NOT the false global
measure claim. The measure side is now definitional.

## Risks / caveats

- `hSuperArc_Tgen` must be stated on `Tgen` orbits restricted to (or a.e. on) `Sclosed`/Taha; a
  literal `= Set.univ` over all of `ℝ×ℝ` (off-ellipse junk where `Tgen` is the identity for b>1)
  would be FALSE. Use either the a.e.-on-`Sclosed` cover (sufficient via `covering_pos_measure`
  applied after intersecting with the conull `Sclosed`) or restrict the union to `Sclosed`. This is
  a strict improvement in honesty over B2's all-of-`ℝ×ℝ` `Mmap` claim, which had the same defect
  hidden.
- The deep-mid ejection lemma `genuine_hEject_deepmid` needs corridor positivity `0 ≤ L_{i+1}` as a
  named genuine-corridor input; that is the same genuine data the assembly already carries, not new.
- This reformulation does not, by itself, close `hSuperArc_Tgen`; it removes the unprovable `hMmap`
  and points the remaining work at the genuine engine.
