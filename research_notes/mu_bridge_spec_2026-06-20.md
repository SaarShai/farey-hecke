# μ-bridge instantiation spec (q ≥ 22) — 2026-06-20

Scout output: exact wrapper signature + how to discharge `XomegaSet_bddBelow` for an
ARBITRARY `μ ∈ XomegaSet` (q ≥ 22) via `hCorr_uniform_via_energy`. READ-ONLY scout.

## 0. Wrapper signature (VERBATIM, namespace `UniformQge22Energy`, mirrored in `HmeasDischarge`)

```
theorem hCorr_uniform_via_energy
    {α : Type*} [MeasurableSpace α]
    (μ : MeasureTheory.Measure α) [MeasureTheory.IsProbabilityMeasure μ]
    (q : ℕ) (hq : 0 < q)
    (P : α → ℝ) (t : ℝ)
    (g : ℕ → α → α)
    (hmeas : ∀ k, k < q → MeasureTheory.MeasurePreserving (g k) μ μ)
    (hSmeas : MeasurableSet {x | t ≤ P x})
    (hbdd : ∃ C, ∀ᵐ x ∂μ, P x ≤ C)
    (hSuperArc :
      (⋃ k ∈ Finset.range q, (g k) ⁻¹' {x | t ≤ P x}) = Set.univ) :
    t ≤ essSup P μ
```
Conclusion delivered: `t ≤ essSup P μ`. Internally = `covering_pos_measure` (μS>0 from
joint covering + hmeas) then `essSup_ge_of_pos_superlevel` (μ{t≤P}>0 + hbdd ⇒ t ≤ essSup).
Both consumed halves are sorry-free/axiom-clean. ONLY open content = `hSuperArc` (L1b).

Convenience variant (hmeas pre-discharged from ONE base map): `HmeasDischarge.hCorr_uniform_block_rotation`
takes a single `M : α → α`, `hM : MeasurePreserving M μ μ`, sets `g k = M^[k]`.

## 1. Target / instantiation for `XomegaSet_bddBelow` (q ≥ 22)

`XomegaSet l m B = {y | ∃ μ, ∃ _:IsProbabilityMeasure μ, MeasurePreserving (Tgen l m B) μ μ
  ∧ μ (Sclosed l)ᶜ = 0 ∧ (∃ M, ∀ᵐ x ∂μ, Pgen l x ≤ M) ∧ y = essSup (Pgen l) μ}`.

Goal: `∀ y ∈ XomegaSet, 1/l^3 ≤ y`. Destructure `y = essSup (Pgen l) μ`, then must show
`1/l^3 ≤ essSup (Pgen l) μ`. This is EXACTLY `hCorr_uniform_via_energy` with the
instantiation:

- `α := ℝ × ℝ`
- `μ := μ` (the arbitrary XomegaSet witness; carries `IsProbabilityMeasure`)
- `q := m+2` (Hecke index), `hq : 0 < q` trivial
- `P := UniformOnset.Pgen l` (def `p.1*(p.1+l*p.2)/l`)  ← P=Pgen, B3
- `t := 1/l^3`                                          ← t=1/l³, B3
- `g := fun k => (Mmap l)^[k]` (block-rotation iterates; `Mmap l p = (p.2, -p.1+l*p.2)`) ← B1
- `hmeas` ← from `MeasurePreserving (Mmap l) μ μ` via `hmeas_of_invariant` / `.iterate`  ← B1
- `hSmeas : MeasurableSet {x | 1/l^3 ≤ Pgen l x}` (Pgen continuous/measurable)            ← B3
- `hbdd`  ← the XomegaSet member's own `(∃ M, ∀ᵐ x ∂μ, Pgen l x ≤ M)`                       ← B3
- `hSuperArc` ← sealed L1b super-arc covering                                              ← B2

## 2. Per-bridge obligations

### B1 — measure bridge (Tgen-invariance ⇒ hmeas), incl. the partial-map subtlety
What XomegaSet gives: `hinv : MeasurePreserving (Tgen l m B) μ μ`.
What wrapper wants: `∀ k<q, MeasurePreserving (g k) μ μ` with `g k = (Mmap l)^[k]`.
Path: supply `MeasurePreserving (Mmap l) μ μ`, then `hmeas_of_invariant μ (Mmap l) hM q`
(= `hM.iterate k`) gives all iterates.

SHARP RISK (the partial-map subtlety): `Tgen ≠ Mmap` pointwise. `Tgen` is the genuine
self-map (branch select + `genStep` at floor `k = ⌊(1+a)/(λb)⌋`), identity for `b>1`.
`Mmap` is the elliptic rotation, and `genuine_step_eq_Mmap_of_bracket` shows
`kstep (kfloor) (a,b) = Mmap (a,b)` ONLY on the interior bracket `λb ≤ 1+a < 2λb`
(floor digit 1). So `Tgen = Mmap` holds only on the k=1 (interior, sub-threshold) part
of the corridor — a PARTIAL agreement, not global. To get `MeasurePreserving (Mmap l) μ μ`
from `MeasurePreserving (Tgen l m B) μ μ` you need μ supported where the two agree, OR a
separate proof that μ (the corridor invariant measure) is `Mmap`-invariant. Available clean
facts: `Mmap_preserves_E` (E conserved), `Mmat_conj_eq_rot` (M whitens to rotation R(−θ),
which preserves arc-length). The honest reduction (recorded in hmeas_lean §5) is:
μ-bridge = "pushforward of arc-length under the whitening conjugacy is M-invariant",
a measure-assembly step. The cleanest faithful B1 statement therefore introduces
`hMmap : MeasurePreserving (Mmap l) μ μ` as a NAMED input (the same class as `hinv`), NOT
a derivation from `hinv` — because globally `Tgen ≠ Mmap`. Do NOT claim `hinv ⇒ hMmap`
without restricting μ to the k=1 corridor; that would be a faithfulness violation.

### B2 — covering bridge (sealed L1b ⇒ hSuperArc)
What wrapper wants: `(⋃ k ∈ Finset.range q, (g k) ⁻¹' {x | t ≤ Pgen l x}) = Set.univ`,
i.e. the q rotation-translates of the super-threshold arc `{Pgen ≥ 1/l³}` cover ℝ×ℝ.
Sealed content: `L1bArcCoverage.fcorr_lb (q) (hq:18≤q) (hL)` PROVED-modulo-its-own-sorry,
`B1_target` (= `1/lamq^3 ≤ g_corr (L_blk q) q hL`), `arc_coverage_ineq`
(`2·arccos(2√6/5)/π < 33/256` PROVED). Numerically super-arc occupies ≈0.872 of the
period (uniform), and rotation step `2π/q < width` for all q, so q translates cover.

SHARP RISK: L1b is phrased on the SINUSOID phase `ψ` (Fobs = offset + amp·cos ψ on the
conserved ellipse / sinusoid window), with `g_corr`/`fcorr` a window-min functional over
the phase domain — NOT directly as a set-cover `⋃ preimage = univ` on ℝ×ℝ. The bridge must
(i) realize Pgen as `(r²/2A₂)·Fobs` along the corridor orbit (the realization/`hbridge`
step the energy-route note flags as un-assembled), and (ii) convert the arc-width fraction
`(1−C)/2 ≈ 0.436 > 1/q` into the literal `⋃ k<q (Mmap^[k])⁻¹ {Pgen≥t} = univ`. The
half-width-≥π/q ⇒ q-translates-cover step is `arc_translates_cover` in spirit but must be
proved against the genuine `Mmap` rotation (θ=π/q) and the genuine observable, not the
abstract sinusoid. This is where the genuine-observable realization gap lives.

### B3 — observable identification (P=Pgen, t=1/l³) + measurability/boundedness + assembly
- `P := UniformOnset.Pgen l`, `t := 1/l^3` — direct, no bridge (definitional match to
  XomegaSet's `Pgen` and `closed_section_lb`'s threshold).
- `hbdd`: take VERBATIM from the XomegaSet member: `⟨M, hPbdd⟩` where
  `hPbdd : ∀ᵐ x ∂μ, Pgen l x ≤ M`. (XomegaSet stores exactly `∃ M, ∀ᵐ ... ≤ M`.) Zero risk.
- `hSmeas`: `MeasurableSet {x | 1/l^3 ≤ Pgen l x}`. Pgen is a polynomial/rational in
  coordinates (measurable; `measurable_genuine_orbitdata`-style measurability already in
  OnsetEquality.lean), so superlevel set is measurable. Mild.
- Assembly skeleton: replace the body of `XomegaSet_bddBelow` (currently
  `exact closed_section_lb ...`) by, after `rintro y ⟨μ,hμprob,hinv,hμS,⟨M,hPbdd⟩,hy⟩; rw[hy]`:
  `exact hCorr_uniform_via_energy μ (m+2) (by omega) (Pgen l) (1/l^3)
     (fun k => (Mmap l)^[k]) (hmeas_of_invariant μ (Mmap l) hMmap (m+2)) hSmeas ⟨M,hPbdd⟩ hSuperArc`
  where `hMmap` (B1) and `hSuperArc` (B2) are the two genuine inputs to supply.
  NOTE: this swaps the q≤21 `closed_section_lb` route for the q≥22 energy route; the
  assembled `Xomega_lb_allq` already routes q≥19 through `hCorr` (ToplevelStitch §6), so the
  natural home is the q≥22 branch of that hCorr, NOT XomegaSet_bddBelow directly — see risks.

## 3. xomega obligations (the wrapper inputs to supply for q ≥ 22, arbitrary μ ∈ XomegaSet)

1. `hMmap : MeasurePreserving (Mmap l) μ μ`  — NEW named input (B1; cannot derive from
   `hinv : MeasurePreserving (Tgen l m B) μ μ` globally since Tgen=Mmap only on k=1 bracket).
2. `hSuperArc : (⋃ k ∈ range (m+2), ((Mmap l)^[k])⁻¹' {x|1/l^3 ≤ Pgen l x}) = univ`
   — the sealed L1b covering, realized on genuine `Mmap`/`Pgen` (B2; the one HARD input).
3. `hSmeas : MeasurableSet {x | 1/l^3 ≤ Pgen l x}`  — mild (Pgen measurable).
4. `hbdd := ⟨M, hPbdd⟩`  — taken verbatim from the XomegaSet member (free).
Plus `IsProbabilityMeasure μ` (carried by the member) and `hq : 0 < m+2` (trivial).
hmeas is then `hmeas_of_invariant μ (Mmap l) hMmap (m+2)`.

## 4. Available named facts each bridge can cite
- `hmeas_of_invariant`, `block_iterate_volume_preserving`, `block_volume_preserving`,
  `det_Mmat`/`det_Mlin` (=1), `hCorr_uniform_block_rotation` — HmeasDischarge (B1).
- `Mmap_preserves_E`, `Mmat_conj_eq_rot`, `genuine_step_eq_Mmap_of_bracket`,
  `kfloor_eq_one_iff_bracket`, `kfloor_ge_two_iff`, `kstep_eq_Mmap_of_k1` — BCZHeckeRotationArc (B1/B2).
- `covering_pos_measure`, `essSup_ge_of_pos_superlevel`, `hCorr_uniform_via_energy` — wrapper.
- `L1bArcCoverage.fcorr_lb`, `B1_target`, `arc_coverage_ineq`, `g_corr`, `L_blk`,
  `H_lt_half_pi`, `cos_sq_lt` — L1b sealed (B2).
- `XomegaSet`, `XomegaSet_bddBelow`, `Xomega_ge`, `cusp_val_mem`, `cusp_dirac_admissible`
  (nonemptiness), `Pgen`, `Sclosed`, `closed_section_lb` — OnsetEquality (B3).

## 5. Sharp risks (faithfulness)
- B1 partial-map: must NOT claim `MeasurePreserving Tgen μ μ ⇒ MeasurePreserving Mmap μ μ`.
  Tgen=Mmap only on the interior-k=1 sub-threshold corridor; global μ-invariance under Mmap
  is a SEPARATE named hypothesis (= the realization/μ-bridge residual). State it as input.
- B2 realization: L1b lives on sinusoid phase ψ with a window-min functional; converting to
  literal `⋃ preimage {Pgen≥t} = univ` on ℝ×ℝ requires the genuine-observable realization
  (Pgen = positive-scale·Fobs along orbit) + arc-width⇒cover. This is the genuine HARD step.
- B3 measure subtlety: XomegaSet uses `μ (Sclosed l)ᶜ = 0` (carried on Sclosed); the wrapper
  covering is on all of ℝ×ℝ. The cover `=univ` is the strong form; alternatively prove cover
  a.e. on Sclosed (μ-conull) — faithful and may be easier, but then `covering_pos_measure`
  needs `hcover` only μ-a.e., NOT `=Set.univ`. The wrapper as written demands `=univ`; a
  faithful weaker variant `(⋃ ...) =ᵐ[μ] univ` would need a wrapper tweak (covering_pos via
  measure_biUnion on a conull cover). Flag for B2 author.
- Boundary q≥22 vs q≥19: `Xomega_lb_allq` already routes q≥19 through `hCorr`. The energy
  route is needed for q≥22 (fixed-window certs die there). q∈{19,20,21} are window-certified
  unconditional. So the hCorr instantiation should target the q≥22 sub-branch; do not
  re-prove q≤21 via the energy route.
- Nonemptiness: `Xomega_ge` needs `(XomegaSet).Nonempty`; `cusp_val_mem`/`cusp_dirac_admissible`
  supply a cusp-tip Dirac witness. Independent of the bddBelow bridge but required for the
  final `Xomega ≥ 1/l³`.
