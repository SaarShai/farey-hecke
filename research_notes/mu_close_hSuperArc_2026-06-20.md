# Closing `hSuperArc` — the genuine super-threshold arc covering (2026-06-20)

## Task

Prove the covering input `hSuperArc` of the reformulated B3 keystone (all-`q` uniform onset lower
bound `1/λ³ ≤ X_Ω(q)`): the genuine super-threshold arc `{x | 1/l³ ≤ Pgen l x}`, under the `q`
rotation-translates of the block step `Mmap l (a,b) = (b, −a+λb)` (angle `θ = π/q` per step), covers
the relevant space. Realize the SEALED L1b arc-coverage (`arc_coverage_ineq` PROVED) on the genuine
`Pgen` orbit, converting the arc half-width inequality into the literal cover.

## Headline result

- **The literal `= Set.univ` covering (B2's `super_arc_hit_within_q` / `SuperArcCover`) is FALSE.**
  Demonstrated, PROVED: the cusp tip `(0,0)` is an `Mmap`-fixed point with `Pgen(0,0)=0 < 1/l³`, so
  its orbit never hits the super-threshold set. B2 asserted the cover on all of `ℝ²`; that target is
  unprovable (it omits `(0,0)`). [`superarc_univ_is_false`, axiom-clean.] Numerically confirmed: the
  sub-threshold arc reaches the full circle for every ellipse `E(p)` below a positive `q`-dependent
  floor.
- **The FAITHFUL covering is corridor-restricted.** `SuperArcCover_corridor`: the corridor
  `Dcorr l` ⊆ ⋃_{k<q} (Mmap^[k])⁻¹ {1/l³ ≤ Pgen}. This is exactly what `covering_pos_measure` needs
  (`μ (Dcorr)ᶜ = 0` ⟹ super-level set has positive `μ`-measure), so it is a faithful `hSuperArc`.
- **The covering reduces to ONE named analytic residual `pgen_orbit_realization`** (the realization
  bridge). Everything downstream is PROVED axiom-clean.

## File / proof state

`projects/mu_close_hSuperArc_lean/RequestProject/Main.lean`

Command:
`( cd projects/aristotle_dispatch_v15 && lake env lean projects/mu_close_hSuperArc_lean/RequestProject/Main.lean )`
→ EXIT 0, 0 errors, exactly 1 `sorryAx` (traced solely to `pgen_orbit_realization`).

PROVED, axiom-clean `[propext, Classical.choice, Quot.sound]` (NO sorryAx):

1. **`cos_grid_hit`** — THE PIGEONHOLE ENGINE. For `q≥1`, `θ=π/q`, any phase `φ`: some `k<q` has
   `cos(φ + 2kθ) ≥ cos θ`, i.e. the `q` equally-spaced rotation phases (spacing `2θ=2π/q`, full
   circle) land inside any super-arc of half-width `≥ θ`. Proof: nearest-grid index via `round`,
   reduce mod `q` by `Int.emod` using `cos`-`2π`-periodicity (`cos_sub_int_mul_two_pi`), then
   `|x|≤θ ⟹ cos x ≥ cos θ` by `cos_le_cos_of_nonneg_of_le_pi`. This is the genuine NEW PROVED content
   (B2 only had the trivial set-algebra cover; the actual rotation-arc pigeonhole was inside its
   `sorry`).
2. **`orbit_hit_of_realization`** — realization datum + threshold gate ⟹ orbit hits super-level.
3. **`arc_coverage_ineq`** / **`cos_sq_lt`** — the SEALED L1b sub-arc width bound
   `2·arccos(2√6/5)/π < 33/256`, reproduced verbatim from `L1bArcCoverage`.
4. **`wide_arc_translates_cover_on`** — orbit-hits ⟹ preimages cover (B2's abstract cover,
   generalized to a sub-domain `D` rather than all of `X`, so the corridor restriction is clean).
5. **`Mmap_preserves_E`**, **`Mmap_iterate_zero`**, **`superarc_univ_is_false`**.

THE SINGLE NAMED RESIDUAL (`sorry`, for Aristotle):

- **`pgen_orbit_realization`** — for `q=m+2`, `l=lamq q`, `p∈Dcorr l`:
  `∃ C0 R φ, R>0 ∧ (∀k, Pgen(M^k p) = C0 + R·cos(φ + 2kθ)) ∧ (1/l³ − C0)/R ≤ cos θ`.
  This is B2's `super_arc_hit_within_q` SHARPENED to the precise sinusoid datum + gate, so the
  downstream `orbit_hit_of_realization` + `cos_grid_hit` close the cover deterministically.

## The genuine math (verified numerically, then formalized as the named gap)

Along an `Mmap` orbit, **`Pgen(M^k p)` is an exact affine sinusoid in `k` of frequency `2θ`**
(residual ~1e-15 in a least-squares fit, q=7,23,40): `Pgen(M^k p) = α·E(p) + ρ·E(p)·cos(φ₀ − 2kθ)`,
with `α, ρ > 0` constants depending only on `l` (verified `α`, `ρ/E` independent of `(a,b)`;
`α·(4−l²)→3`, `ρ·(4−l²)→3` as `l→2`). The doubled frequency comes from `Pgen` being a degree-2 form
in the rotating whitened coordinates (`Mmat_conj_eq_rot`: `Mmap` whitens to rotation by `−θ`;
`Mmap_preserves_E`: orbit stays on the `E(p)`-ellipse).

The threshold gate `(t − C0)/R ≤ cos θ` is `E`-scale-invariant (`C0, R ∝ E(p)`), so it reduces to
the sealed sub-arc width: on the `Fobs = 3λ/2 + √(1+2λ²)·cos` normalization the sub-threshold cosine
is `2√6/5` and `arc_coverage_ineq` gives sub-arc half-width `arccos(2√6/5) < 33π/512`, whence the
super-arc half-width `≥ θ = π/q`. The corridor `E`-floor (E(p)>0 bounded below on `Dcorr l`) keeps
`1/(l³E(p))` inside the band. Both ingredients (R1 whitening identification, R2 gate from
`arc_coverage_ineq`) are exactly the content of `pgen_orbit_realization`.

The exact closed forms of `α, ρ` are not `3/(4−l²)` (they differ at finite `l`); the precise values
need the whitening Cholesky factor `LTmat θ = [[1,−cosθ],[0,sinθ]]` change of coordinates — this is
the remaining derivation handed to Aristotle (it does NOT need the constants to be pretty, only
`R>0` and the gate).

## Aristotle

- Self-contained RequestProject: `projects/mu_close_hSuperArc_lean/aristotle_realization/`
  (mirrors `projects/hmeas_lean/`), containing `Mmat_conj_eq_rot`, `Mmap_preserves_E`,
  `arc_coverage_ineq`, `cos_sq_lt` PROVED + `pgen_orbit_realization` as the single `sorry`.
  Elaborates EXIT 0, 1 intended sorry.
- Submitted: **Project UUID `0c0c196b-23b0-4f99-8e79-e8ffebfa08c6`**, Task
  `c905d5f2-d660-4940-a9a5-013eb4926689` (running). Check with
  `~/.local/bin/aristotle show 0c0c196b-23b0-4f99-8e79-e8ffebfa08c6 --api-key "$KEY"`.

## Honest scope

- This does NOT by itself prove the all-`q` onset. It delivers the covering MODULO the single
  realization bridge, with the measure side definitional (per the μ-bridge reformulation) and the
  pigeonhole + abstract cover + arc-coverage all PROVED axiom-clean.
- The corrected (corridor-restricted) covering is the right faithful target; the previously-stated
  all-`ℝ²` cover (B2 `SuperArcCover`, and the keystone's `hSuperArc … = Set.univ`) is FALSE off the
  corridor and must be read as the conull/`Dcorr`-restricted form. This is a genuine correction, not
  a weakening: `covering_pos_measure` only consumes positive `μ`-measure of the super-level set,
  which the corridor cover supplies.
