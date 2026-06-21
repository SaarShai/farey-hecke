# Lattice-gap / hOrbitAgree scope — decisive scout (2026-06-20)

/ goal: make the decisive call on `hOrbitAgree`, the interior-k=1 confinement (R1-upper =
R3 lattice-gap) residual of the faithful keystone
`HsaUnconditional.Xomega_ge_unconditional` in
`projects/hsa_unconditional_lean/RequestProject/Main.lean`.

## The two residuals (verbatim from Main.lean §6)

```
hEfloor     : ∀ p ∈ Sclosed, isK1 p → EfloorQ m l ≤ Eform l p
hOrbitAgree : ∀ p ∈ Sclosed, isK1 p → ∀ k, Tgen^[k] p = (Mmap l)^[k] p
```

`hEjectStep` (¬isK1 → one Tgen step clears 1/l³) is SEALED-PROVED
(`GenuineSelfMap.genuine_hEject_deepmid`, axiom-clean) — not a residual.

## How the cover currently USES hOrbitAgree (the load-bearing mechanism)

`orbit_hit_corridor` (Main.lean:490) splits `p ∈ Dom` by `isK1`:

* `isK1 p`  → `hRealize` produces `∃ C0 R φ, 0<R ∧ (∀k, Pgen l (Tgen^[k] p) =
  C0 + R·cos(φ+2kθ)) ∧ gate`, then `orbit_hit_of_realization` calls
  **`cos_grid_hit q`** (Main.lean:415) — a SINGLE full-period pigeonhole over
  `k ∈ {0,…,q−1}` returning the ONE `k` with `cos(φ+2kθ) ≥ cos θ`.
* `¬isK1 p` → `hEjectStep` clears in ONE step (k=1 index).

`hRealize` is discharged by `realize_from_orbit_realization` (Main.lean:680): it takes
the `Mmap`-orbit sinusoid `pgen_orbit_realization` (which gives `Pgen l ((Mmap l)^[k] p)
= C0+R·cos(...)` UNCONDITIONALLY for ALL k) and rewrites `Tgen^[k] p = (Mmap l)^[k] p`
via `hOrbitAgree` to transport it to the `Tgen` orbit. So **`hOrbitAgree` is used for
ALL k<q at once** — not for a run of length L. It is the statement "the genuine Tgen
orbit IS the pure Mmap rotation for the whole first q steps."

## Critical fact: L1b/cos_grid_hit needs the identity at the SINGLE picked k, but a FULL q-rotation to FIND it

`cos_grid_hit q` is a single-rotation pigeonhole (rotation number 1/(2q) rational, step
2θ=2π/q, so `{2kθ mod 2π}` is the equally-spaced full lattice of q points; one of them
lands within θ of the peak — `arc_coverage_ineq` family / `Real.cos_le_cos_of_…`). It
ESTABLISHES existence of a good `k*` but does not control WHERE `k*` lands. To use the
sinusoid value at `k*` we need `Tgen^[k*]p = Mmap^[k*]p`. Since `k*` can be any index in
`0..q−1`, the proof as wired demands the identity for ALL k<q — exactly `hOrbitAgree`.

`L1bArcCoverage.lean` (arc_coverage_ineq / B1_target / g_corr) is the SEPARATE
corridor-BLOCK route (block monodromy, `L_blk q = ⌈33q/256⌉+2` blocks, window-sum
sinusoid) — it is NOT the per-step Pgen-orbit pigeonhole the keystone uses. Its
`windowMaxCos` pigeonhole bounds a window of length L_blk over phase offsets; the keystone
instead uses the cleaner single-rotation `cos_grid_hit`. Neither requires "q CONSECUTIVE
k=1 steps from one phase" in the literal sense — `cos_grid_hit` sweeps the FULL period in
ONE rotation. The dependence is on the orbit identity holding across the full period.

## DECISIVE CALL: can the dichotomy ELIMINATE hOrbitAgree?

**No — not as a clean elimination, but it CAN be WEAKENED to a STOPPING-TIME (first-ejection)
confinement, which is strictly easier and removes the false "all-k<q" over-quantification.**

The over-strong `hOrbitAgree` (∀k, including AFTER ejection) is genuinely FALSE pointwise:
once the genuine orbit hits a k≥2 step it leaves the Mmap rotation (the `(k−1)λL_{q−1}`
translation kicks it off the E-ellipse, `no_infinite_k1_run` + `kfloor_ge_two_iff`), so
`Tgen^[k]p ≠ Mmap^[k]p` for k past the first increment. The note's "~40–50% random
violations" is exactly this. So `hOrbitAgree` as literally stated is only true because, on
the realized isK1 cells, the orbit happens to stay k=1 long enough — but demanding it for
ALL k is more than the cover needs.

The dichotomy gives the correct reformulation. Let `τ(p) = min{j : ¬isK1(Tgen^[j]p)}` be
the first-ejection time (well-defined and FINITE by `no_infinite_k1_run`). Two exhaustive cases:

1. **τ ≥ q** (orbit stays k=1 for the whole first period): then `Tgen^[k]p = Mmap^[k]p`
   for all k<q (genuine_step_eq_Mmap_of_bracket at each step), the sinusoid holds for all
   k<q, and `cos_grid_hit q` finds k*<q with the threshold cleared. THIS is the case
   `hOrbitAgree` was meant to cover — but with the bound `k<τ` not `∀k`.

2. **τ < q** (orbit ejects at step τ < q): then at step τ the point `Tgen^[τ]p` has floor
   ≥2, and `hEjectStep`/`genuine_hEject_deepmid` clears the threshold in ONE more step:
   `1/l³ ≤ Pgen(Tgen^[τ+1]p)` with τ+1 ≤ q. So the hit index is τ+1<q+... — needs τ+1<q,
   i.e. τ<q (holds) — actually τ+1 could equal q; the cover range is k<q so we need the
   hit at an index <q. Re-key: in case 2 take k = τ (the FIRST ejecting index is itself
   <q) and apply ejection at that step's PREDECESSOR — i.e. the hit is at index τ ≤ q−1.
   (Ejection clears Pgen at the deep-mid point itself; `genuine_hEject_deepmid` bounds
   `Pgen(genStep p)` so the cleared index is τ, the ejecting step's output, ≤ q−1.)

**The faithful reformulated cover target** (what R-confinement should prove) replaces the
single ∀k `hOrbitAgree` with the BOUNDED-TIME agreement:

```
hAgreeUpToEject : ∀ p ∈ Sclosed, isK1 p →
    ∀ k, k ≤ firstEjectTime q p → Tgen^[k] p = (Mmap l)^[k] p
```

together with case-2 handled by the already-sealed `hEjectStep`. The orbit-agreement is
then needed ONLY up to the first ejection (≤ a per-point cutoff), and the run that reaches
`cos_grid_hit`'s good index needs the rotation to survive only until that index — and IF
it ejects first, ejection clears instead. This is the genuine "per-run L1b on the k=1 run
+ ejection on k≥2" reformulation the KEY ANGLE proposed, and it is SOUND.

### Why this is strictly easier (but NOT vacuous)

`hAgreeUpToEject` is exactly `genuine_step_eq_Mmap_of_bracket` chained over the maximal
k=1 prefix — and the k=1 prefix is characterized by the floor bracket
`λb ≤ 1+a < 2λb` (kfloor_eq_one_iff_bracket). The LOWER bracket `λb≤1+a` is ALREADY A
THEOREM on the sub-threshold ellipse (`BCZHeckeRotationArcR1.lower_bracket_preserved_on_ellipse`,
axiom-clean). The remaining content is the UPPER bracket `1+a<2λb` surviving until the
ejection step — i.e. "the orbit does not eject before `cos_grid_hit`'s good index is
reached, OR if it does, ejection clears." This is the R1-upper = R3 lattice-gap, BUT
re-scoped: we no longer need it for all k, only "the rotation reaches its super-arc index
OR ejects (and ejection clears) first." Since `cos_grid_hit` guarantees a good index
within the first FULL period (q steps), and the rotation either survives to it or ejects
(clearing) first, the dichotomy DOES discharge the hard "all-k" form — but it does NOT
make confinement disappear: we still need "interior steps before the good index are k=1
(= Mmap)" so the sinusoid identity holds at the good index when reached.

**Net: the dichotomy DISSOLVES the over-quantified ∀k `hOrbitAgree` into
`hAgreeUpToEject` (bounded by first-ejection) + sealed ejection. This is a faithful
REFORMULATION of the cover (not a literal elimination): confinement is still load-bearing
but only as the bounded-prefix k=1 agreement, whose LOWER half is already proved and whose
UPPER half is the genuine residual.**

## Is the (re-scoped) confinement uniformly TRUE, or does it fail at resonances {23,61,…}?

**It is uniformly TRUE for the ONSET ≥ bound (which is all the keystone needs), even though
the EXACT B(q) value fails at resonances.** Decisive distinction:

* The resonance {23,61,…} (R3) is about the EXACT INTEGER `rotationArcCount q` exceeding
  the continuous proxy `⌊W(q)q/π⌋+1` by 1 — a question of the EXACT cluster CEILING B(q).
  The keystone does NOT need B(q); it needs only `∃ k<q, 1/l³ ≤ Pgen(Tgen^[k]p)`, i.e.
  the rotation reaches the super-arc (Pgen ≥ 1/l³) AT LEAST ONCE within q steps.

* `cos_grid_hit q` proves the super-arc is reached within ONE full period for ANY phase φ
  (the equally-spaced q-point lattice always has a point within θ of the peak, since the
  gap is exactly 2π/q < 2·θ-arc-coverage). This is parity/resonance-INDEPENDENT: it is a
  statement about a single rotation of q equally-spaced points, not about how many
  CONSECUTIVE points stay sub-threshold. The notch-straddle that creates the B(q)
  resonance affects whether an EXTRA point fits sub-threshold (B+1), never whether SOME
  point clears super-threshold.

* The `resonance_parity_gate` (R3-parity, PROVED axiom-clean in
  `BCZHeckeRotationArcR3Parity.lean`) governs the +1 GAIN in B(q); it is irrelevant to the
  onset ≥ direction. "Parity beats proximity" decides B(q)∈{B0,B0+1}, both of which are ≥
  the onset value 1/l³ at the peak.

**Conclusion on lattice_gap_nature: the lattice-gap is genuinely needed (as bounded-prefix
confinement) but is UNIFORMLY TRUE for the onset ≥ 1/l³ direction; it FAILS only for the
exact B(q) value at resonances {23,61,…}, which the keystone never invokes. The onset ≥
bound SURVIVES all resonances.**

## efloor_target + closed-form E-floor

`hEfloor` is the genuine analytic residual (E-floor on the k=1 corridor). The faithful
uniform statement to prove:

```
∀ q ≥ 5 (m ≥ 1, l = 2cos(π/(m+2))), ∀ p ∈ Sclosed l, isK1 p →
    EfloorQ m l ≤ Eform l p
```
with the CLOSED-FORM E-floor (from hsa_realization_lean §2, verbatim):
```
EfloorQ m l = 1 / (l³ · (alphaC l + rhoC l · cos(π/(m+2))))
            = 1 / (l³ · (alphaC l + rhoC l · (l/2)))           [since cos(π/(m+2)) = l/2]
alphaC l = (l²+2)/(l(4−l²))          = 1/(4c) + 3c/(4s²)   (c=cosθ, s=sinθ)
rhoC   l = 2√(2l²+1)/(l(4−l²))       = √(8c²+1)/(4s²c)
```
This is the corridor E-floor gate of `pgen_orbit_realization`; interval-certified q≤200,
uniform-q OPEN (L1b arc-coverage family). It is INDEPENDENT of the confinement residual.

## What R-confinement should target

The cleanest faithful confinement_target is the bounded-prefix agreement (NOT the
over-strong ∀k):
```
∀ p ∈ Sclosed, isK1 p → ∀ k, (∀ j < k, isK1 (Tgen^[j] p)) → Tgen^[k] p = (Mmap l)^[k] p
```
("as long as every earlier step is k=1, the orbit equals the Mmap rotation"). This is
`genuine_step_eq_Mmap_of_bracket` iterated, with the k=1 bracket = isK1 — and the cover is
re-keyed so that the FIRST non-isK1 step is handled by the sealed `hEjectStep`. This
removes the false "all-k including post-ejection" content and reduces the residual to the
already-half-proved (lower bracket DONE) per-step k=1 agreement.

## Risks

* The cover re-keying (case split on first-ejection time τ vs q) is a Lean ENGINEERING
  change in `orbit_hit_corridor`/`SuperArcCover_corridor`, not yet done; `cos_grid_hit`'s
  good index k* must be shown ≤ τ OR ejection-at-τ clears with τ ≤ q−1. The arithmetic
  "k* ≤ τ when τ ≥ (cos_grid_hit index)" needs that the super-arc is reached before
  ejection in case 1 — true because the realized isK1 cell has the full k=1 prefix to k*,
  but must be supplied (this is the residual content, not free).
* `genuine_hEject_deepmid` clears at the EJECTING step's output (index τ); confirm τ ≤ q−1
  so the hit index is in range `Finset.range q` (τ < q by case 2 hypothesis; OK).
* The bounded-prefix confinement still carries the UPPER-bracket (R1-upper) survival to k*;
  the dichotomy reduces its SCOPE (only up to k*∨τ) but does not make it vacuous.
* EfloorQ uniform-q remains separately OPEN (interval-certified q≤200); not dissolved by
  the dichotomy.
