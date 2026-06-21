# RequestProject — Discharging `hmeas` (block-iterate measure preservation) for the q ≥ 22 energy route

## Goal

The machine-verified uniform wrapper `hCorr_uniform_via_energy`
(`projects/uniform_qge22_energy_lean/RequestProject/Main.lean`) delivers the `hCorr` shape
`t ≤ ess-sup_μ P` for every `q` from three inputs, of which the only "measure" input is

> `hmeas : ∀ k, k < q → MeasurePreserving (g k) μ μ`

with `g k = M^[k]` the iterates of the genuine corridor block step `M`. This project discharges
`hmeas`.

## The block step

The genuine block step is the linear map with matrix `M = ![![0,1],[−1,λ]]` (the `Mmat` of
`projects/aristotle_dispatch_v15/uniform_q5to18/BCZHeckeRotationArc.lean`), which is proved there to
have `det M = 1`, `trace M = λ`, and to be the elliptic rotation by `θ = π/q` on the conserved
ellipse `E = a² − λab + b²` (`Mmat_conj_eq_rot`, `Mmap_preserves_E`).

## What is PROVED (sorry-free, axiom-clean `[propext, Classical.choice, Quot.sound]`)

1. `det_Mmat` / `det_Mlin` — `det M = 1`.
2. `block_volume_preserving` — `M` preserves the additive-Haar (Lebesgue/volume) measure on
   `ℝ² = Fin 2 → ℝ`, from `det M = 1` via `Measure.map_linearMap_addHaar_eq_smul_addHaar`
   (Haar rescales by `|det|⁻¹ = 1`).
3. **`block_iterate_volume_preserving`** — `∀ k, MeasurePreserving (M^[k]) volume volume`.
   **This is `hmeas` for the natural Haar/Lebesgue measure, PROVED UNCONDITIONALLY.**
4. `hmeas_of_invariant` — for ANY measure `μ` preserved by `M`, every iterate preserves `μ`
   (`MeasurePreserving.iterate`); i.e. `hmeas` reduces to the SINGLE base `MeasurePreserving M μ μ`.
5. **`hCorr_uniform_block_rotation`** — instantiates the verbatim-reproduced wrapper
   `hCorr_uniform_via_energy` with `g k = M^[k]`, discharging the `hmeas` slot from the single
   standard input `hM : MeasurePreserving M μ μ`. Delivers `t ≤ essSup P μ` (the hard `hSuperArc`
   passed through unchanged).
6. `Mmat_conj_eq_rot` — verbatim `BCZHeckeRotationArc.Mmat_conj_eq_rot`: `Lᵀ M (Lᵀ)⁻¹ = R(−θ)`,
   recording that `M` preserves the arc-length (rotation-invariant) measure on the ellipse — the
   μ-bridge ingredient.

## Honesty (which measure)

- For the natural Haar/Lebesgue **volume** measure, `hmeas` is **PROVED unconditionally** (#3,
  det = 1).
- The wrapper requires a **probability** measure `μ` (volume on ℝ² is infinite, not a probability
  measure). For the genuine invariant probability measure of the section dynamics, `hmeas` is
  **reduced to exactly** the standard input `MeasurePreserving M μ μ` (#4, #5) — the SAME
  `hinv : MeasurePreserving (Tgen l m B) μ μ` already carried by
  `GenuineClassDischarge.perq_Xomega_lb_qge19_GEN'` for q ≤ 21. So q ≥ 22 gains NO NEW gap.
- The remaining μ-bridge (identifying `μ` with the arc-length measure on the ellipse and pushing it
  through the whitening conjugacy `Mmat_conj_eq_rot`) is measure-assembly, NOT a new analytic crux.

## Build

```
( cd <repo>/projects/aristotle_dispatch_v15 && \
  lake env lean <repo>/projects/hmeas_lean/RequestProject/Main.lean )
```
Elaborates clean (only unused-variable / `<;>`-style linter warnings); the `#print axioms` block at
the end shows all 7 results axiom-clean.
