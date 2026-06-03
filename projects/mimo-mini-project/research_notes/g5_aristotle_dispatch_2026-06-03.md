# Aristotle dispatch — q=5 window-5 core `g5_core` (USER submits; not self-submitted)

**Status:** STAGED, not submitted. Submit to Aristotle yourself when ready. The all-floor-1 quadrant
(`g5_rot3`) is already PROVEN locally and shipped in the package; this dispatch is for the remaining
(harder) cases that complete `g5_core`.

## File to submit
`lean/BCZHeckeG5_core_dispatch.lean` (self-contained; compiles EXIT=0 with one `sorry` = `g5_core`).
Everything above `g5_core` is proven, axioms `[propext, Classical.choice, Quot.sound]`:
`phi/phi_sq/phi_lt2`, `floor_ge_one`, `E_conserved_floor_one`, and **`g5_rot3`** (the all-floor-1
sub-case). Aristotle's job: discharge the single `sorry` in `g5_core`.

## PROMPT (paste to Aristotle)

> Prove the theorem `g5_core` in the attached Lean 4 file (Mathlib v4.28.0), replacing its `sorry`.
> Do not modify any other declaration; all lemmas above `g5_core` are already proven and are yours to
> use. The result must be sorry-free with `#print axioms g5_core` = `[propext, Classical.choice,
> Quot.sound]`. Compile with `( ~/.elan/bin/lake env lean BCZHeckeG5_core_dispatch.lean 2>&1; echo
> EXIT=$? )` and report the `EXIT=` line.
>
> `g5_core` asserts: six positive reals `a,b,c,d,e,f` (a `T₅`-orbit segment, `λ=φ=(1+√5)/2`,
> `φ²=φ+1`) that lie above the cusp line on all five consecutive pairs (`a+φb>1`, …, `e+φf>1`),
> satisfy the BCZ floor recurrence `cₙ+cₙ₊₂ = kₙ·φ·cₙ₊₁` with integer floors `k₀..k₃ ≥ 1` and their
> floor upper bounds `1+cₙ < (kₙ+1)·φ·cₙ₊₁`, CANNOT have all five products `ab,bc,cd,de,ef` below
> `1/4`. (This is the sharp q=5 cluster bound; the 4-window version is false, 5 is the minimum.)
>
> CRITICAL: use `phi_sq : φ²=φ+1` only as an `nlinarith`/`linear_combination` hint, never a rewrite.
> q=5 is the *connected* regime: any SINGLE-pair argument is vacuous (the relevant discriminant
> `1−φ<0`), so the contradiction is genuinely multi-step. Recommended route:
>   1. Engine: `bc+cd = k1·φ·c²` etc. (multiply each recurrence by the middle coord), so each
>      `kᵢ·φ·c_{mid}² < 1/2`, giving `c_{mid}² < 1/(2φkᵢ) ≤ (φ−1)/2`. Large floors break region.
>   2. `interval_cases` the four floors over the feasible band (each `kᵢ ∈ {1,2,3}`; the engine +
>      region prune the rest). ~tens of cases; most close by `nlinarith` with the `cᵢ²` bounds.
>   3. all-floor-1 sub-block: reuse `g5_rot3` (already proven).
>   4. the only TIGHT cases are the cyclic `(1,1,2)` words — floor words `(1,1,2,1)`,`(2,1,1,2)`,
>      `(1,2,1,1)` (and `(2,1,1,3)`); there `min max(5 products) → 1/4⁺`. For these use
>      `E_conserved_floor_one` on the surrounding floor-1 (rotation) run to lower-bound the swept
>      product peak, and the floor-`=2` step bound `K·φ·y ≥ 2φy > 2(1−x) ≥ 2x` (the `g4_caseA′`
>      trick from the q=4 proof). The binding optimum is `cₙ = R·sin((n+1)π/5)` at `R→R_lo`, where
>      the products are `R²·{sin36·sin72, sin72², sin72·sin36} = {0.1545, 0.25, 0.1545}·(R/R_lo)²`.
>
> Numerics confirming the statement is TRUE (so a proof exists): max run of consecutive sub-`1/4`
> products on real `T₅` orbits is 4 (window-5 holds; verified three independent ways); the per-floor
> word `min max(5 products)` table has its global minimum `0.25042` at word `(1,1,2,1)` — i.e. the
> bound is tight but never violated.

## Provenance / honesty
- The window-4 form (`g5_no_four_below`) is REFUTED — do NOT ask Aristotle to prove it.
- `g5_rot3` margin ≈ 0.3945; tight cases listed above from `code/g5_window_precheck.py` (per-floor
  table) and the window-5 word scan. `X(5)=1/4` lower bound has no paper proof; this would be the
  first rigorous one if `g5_core` lands.
- After `g5_core`: assemble `g5_no_five_below` (orbit form, mechanical bridge as in
  `g4_no_three_below`), a window-5 `essSup` engine (generalize `essSup_ge_of_window` to a 5-`max`),
  a `1/4`-point exclusion lemma (analog of `g4_not_t_at`), then `g5_no_ground_state`.
