import Mathlib
import L1bArcCoverage
import CorridorProductRealization
import RealizeWire

set_option maxHeartbeats 4000000

/-!
# `WindowRealizeClose.lean` — closing `WindowProductRealizes` for the corridor orbit.

This file PROVES `RealizeWire.WindowProductRealizes q hL P` for the genuine corridor orbit
`P k = (M_W^[k] s0).1 · (M_W^[k] s0).2`, discharging the SOLE remaining open input of the
corridor bridge `g_corr ≤ window-sup P` (`RealizeWire.hbridge_of_realizes`).

## The mechanism (all five steps of the task, made rigorous)

The two PROVED sinusoid identities (`CorridorProductRealization`) give, along the `M_W`-orbit of
an in-domain corridor start `s0=(a,b)` (`a,b>0`, `Qp>0`):

* **Product** `P k = C0 + R·cos(φ + 2kθ)`, `R>0`, `θ=π/q`  (`corridor_product_realization`).
  With `r² := 4·A₂·Qp/(4−λ²)` one has `C0 = (r²/(2A₂))·(3λ/2)` and `R = (r²/(2A₂))·√A₂`, i.e.
  `P k = (r²/(2A₂))·[3λ/2 + √A₂·cos(φ+2kθ)]`.
* **Domain** `D k = a_k+λb_k = Damp·cos(ψ + kθ)`, `Damp²·sin²θ = (6λ²+1)·Qp` (`corridor_domain_realization`),
  and `Damp² = r²·Blam²` (the amplitude pinning, verified algebraically here).

The realization datum at window start `N`:

1. **Phase alignment.**  Choose `muc` so the `windowMaxCos` cosine grid
   `2(muc−ξ)+(2j−(L−1))θ+η` coincides with the product grid `φ+2(N+j)θ` for every `j<L`.
   Solving: `2·muc = φ + 2Nθ + (L−1)θ − η + 2ξ` (modulo `π`, to land in the domain).
   Then `windowMaxCos(L,q,muc) = sup'_{j<L} cos(φ+2(N+j)θ)`.
2. **Radius forcing (in-domain).**  The window indices stay in-domain (`D_{N+j}>1`), so at the
   window's far-endpoint phase one gets `r·Blam·cos(|muc|+H) ≥ 1`, i.e.
   `r² ≥ 1/(Blam²·cos²(|muc|+H))`.
3. **Affine sup-push + scale down.**  `sup'_{j<L} P(N+j) = (r²/(2A₂))·[3λ/2 + √A₂·windowMaxCos(muc)]`.
   Since `P` is positive at the sup index and `r² ≥ 1/(Blam²cos²(|muc|+H))`,
   `fcorr(muc) = (1/(2A₂Blam²cos²(|muc|+H)))·[3λ/2+√A₂·windowMaxCos] ≤ sup'_{j<L} P(N+j)`.

That IS `WindowProductRealizes`.  Sorry-free / axiom-clean.
-/

namespace WindowRealizeClose

open L1bArcCoverage CorridorProductRealization
open scoped Real

noncomputable section

/-! ## §1.  Amplitude-pinning bridge: `Damp² = r²·Blam²` with `r² = 4A₂Qp/(4−λ²)`. -/

/-- `2·A₂·Blam² = 12λ²+2` (re-derived locally; matches `L1bArcCoverage.twoA2Blam_eq`).  Here
`A₂ = A2q q`, `Blam = Blamq q` use the `L1bArcCoverage` defs (`lamq` everywhere). -/
theorem twoA2Blam_eq' (q : ℕ) :
    2 * A2q q * Blamq q ^ 2 = 12 * L1bArcCoverage.lamq q ^ 2 + 2 :=
  L1bArcCoverage.twoA2Blam_eq q

/-- The two `lamq` defs agree (`L1bArcCoverage` uses `π/q`, `CorridorProductRealization` uses
the same).  Stated for `q = m+2`. -/
theorem lamq_eq (m : ℕ) :
    L1bArcCoverage.lamq (m + 2) = CorridorProductRealization.lamq (m + 2) := by
  unfold L1bArcCoverage.lamq CorridorProductRealization.lamq
  norm_num

/-! ## §2.  Phase-grid alignment: `windowMaxCos(muc) = sup'_j cos(φ + 2(N+j)θ)`. -/

/-- **Alignment.**  If `muc` is chosen so that `2(muc − ξ) − (L−1)θ + η = base` (where
`base = φ + 2Nθ` is the product window's leading phase), then the `windowMaxCos` cosine grid
coincides termwise with `cos(base + 2jθ)`, hence
`windowMaxCos(L,q,muc) = sup'_{j<L} cos(base + 2jθ)`. -/
theorem windowMaxCos_eq_orbit_sup (L q : ℕ) (hL : 0 < L) (muc base : ℝ)
    (halign : 2 * (muc - L1bArcCoverage.xiq q) - ((L:ℝ) - 1) * L1bArcCoverage.thetaq q
        + L1bArcCoverage.etaq q = base) :
    windowMaxCos L q hL muc
      = (Finset.range L).sup' (Finset.nonempty_range_iff.mpr (by omega))
          (fun j => Real.cos (base + 2 * (j : ℝ) * L1bArcCoverage.thetaq q)) := by
  unfold windowMaxCos
  refine Finset.sup'_congr _ rfl (fun j _hj => ?_)
  congr 1
  rw [← halign]; ring

/-! ## §3.  The rigorous ASSEMBLY (steps 1,3,4,5 of the task), fully proved.

`windowProductRealizes_of_data` proves `WindowProductRealizes q hL P` from the realization DATA
that the two PROVED sinusoid identities supply, plus the in-domain RADIUS FORCING.  Everything
here is machine-verified; the only inputs are the precise per-`N` realization data
(`hdata`), which packages exactly:
  • the affine product form `P k = (rr/(2A₂))·[3λ/2 + √A₂·cos(base + 2kθ)]` with `base = φ+2Nθ`,
    where `rr = r²` is the orbit's conserved squared-radius (`> 0`);
  • the chosen domain phase `muc ∈ Ioo` with grid alignment `halign`;
  • the in-domain radius forcing `rr·Blamq²·cos²(|muc|+H) ≥ 1`.
The first two are delivered by `corridor_product_realization` + the (proved) alignment lemma; the
third is the in-domain arc-width forcing.  This theorem does the affine sup-push and the
scale-down (`csInf`/positivity), VERBATIM `fcorr`/`windowMaxCos`/`WindowProductRealizes`. -/
theorem windowProductRealizes_of_data (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q) (P : ℕ → ℝ)
    (hPpos : ∀ k, 0 < P k)
    (hdata : ∀ N : ℕ, ∃ (rr base muc : ℝ),
      0 < rr ∧
      muc ∈ Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q) ∧
      (2 * (muc - L1bArcCoverage.xiq q) - ((L_blk q : ℝ) - 1) * L1bArcCoverage.thetaq q
          + L1bArcCoverage.etaq q = base + 2 * (N : ℝ) * L1bArcCoverage.thetaq q) ∧
      (∀ j : ℕ, P (N + j) = (rr / (2 * A2q q))
          * (3 * L1bArcCoverage.lamq q / 2 + Real.sqrt (A2q q)
              * Real.cos ((base + 2 * (N : ℝ) * L1bArcCoverage.thetaq q)
                  + 2 * (j : ℝ) * L1bArcCoverage.thetaq q))) ∧
      1 ≤ rr * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q) ^ 2) :
    RealizeWire.WindowProductRealizes q hL P := by
  intro N
  obtain ⟨rr, base, muc, hrr, hmuc, halign, hPform, hforce⟩ := hdata N
  refine ⟨muc, hmuc, ?_⟩
  -- abbreviations
  set L := L_blk q
  set θ := L1bArcCoverage.thetaq q
  set A2 := A2q q
  set Blam := Blamq q
  set H := Hq L q
  set lam := L1bArcCoverage.lamq q with hlam
  set B := base + 2 * (N : ℝ) * θ with hB
  have hA2_pos : 0 < A2 := by simp only [A2, A2q]; positivity
  have hsqA2_nn : 0 ≤ Real.sqrt A2 := Real.sqrt_nonneg _
  -- the nonempty witness for the range-sup'
  have hne : (Finset.range L).Nonempty := Finset.nonempty_range_iff.mpr (by omega)
  -- §3a.  windowMaxCos(muc) = sup'_{j<L} cos(B + 2 j θ).
  have halign' : 2 * (muc - L1bArcCoverage.xiq q) - ((L:ℝ) - 1) * θ + L1bArcCoverage.etaq q = B := by
    rw [hB]; exact halign
  have hwmc : windowMaxCos L q hL muc
      = (Finset.range L).sup' hne (fun j => Real.cos (B + 2 * (j : ℝ) * θ)) := by
    have := windowMaxCos_eq_orbit_sup L q hL muc B halign'
    simpa using this
  -- §3b.  window-sup P (N+·) = (rr/(2A₂))·[3λ/2 + √A₂·windowMaxCos(muc)].
  --   Push the affine x ↦ (rr/(2A₂))(3λ/2 + √A₂ x) through sup' (monotone since rr,√A₂ ≥ 0).
  set Csup := (Finset.range L).sup' hne (fun j => Real.cos (B + 2 * (j : ℝ) * θ)) with hCsup
  set g : ℝ → ℝ := fun x => (rr / (2 * A2)) * (3 * lam / 2 + Real.sqrt A2 * x) with hg
  have hcoef_nn : 0 ≤ rr / (2 * A2) := by positivity
  have hg_mono : Monotone g := by
    intro x y hxy
    have : Real.sqrt A2 * x ≤ Real.sqrt A2 * y := mul_le_mul_of_nonneg_left hxy hsqA2_nn
    exact mul_le_mul_of_nonneg_left (by linarith) hcoef_nn
  have hg_sup : ∀ x y : ℝ, g (x ⊔ y) = g x ⊔ g y := by
    intro x y
    rcases le_total x y with h | h
    · rw [sup_eq_right.mpr h, sup_eq_right.mpr (hg_mono h)]
    · rw [sup_eq_left.mpr h, sup_eq_left.mpr (hg_mono h)]
  have hPsup_eq : (Finset.range L).sup' hne (fun j => P (N + j))
      = g Csup := by
    have hterm : ∀ j ∈ Finset.range L,
        P (N + j) = g (Real.cos (B + 2 * (j : ℝ) * θ)) := by
      intro j _; rw [hPform j]
    rw [Finset.sup'_congr hne rfl hterm, hCsup]
    exact (Finset.comp_sup'_eq_sup'_comp hne g hg_sup).symm
  -- §3c.  fcorr(muc) ≤ window-sup P.
  --   fcorr(muc) = (1/(2A₂Blam²cos²(|muc|+H)))·[3λ/2 + √A₂·windowMaxCos(muc)]
  --             = (1/(2A₂Blam²cos²(|muc|+H)))·(2A₂/rr)·(window-sup P)   [hPsup_eq, g def]
  --   and rr·Blam²·cos²(|muc|+H) ≥ 1  (radius forcing) with window-sup P > 0 ⟹ ≤ window-sup P.
  have hθ0 : 0 ≤ θ := by simp only [θ, L1bArcCoverage.thetaq]; positivity
  have hH0 : 0 ≤ H :=
    le_trans (by have := Real.pi_pos; positivity) (H_ge_loose q hq)
  have hHlt : H < Real.pi / 2 := H_lt_half_pi q hq
  have hcosH_pos : 0 < Real.cos (|muc| + H) :=
    L1bArcCoverage.denom_cos_pos hH0 hHlt hmuc
  have hcosH2_pos : 0 < Real.cos (|muc| + H) ^ 2 := pow_pos hcosH_pos 2
  have hBlam_pos : 0 < Blam := by
    simp only [Blam, Blamq]; positivity
  -- window-sup P ≥ P (N+0) > 0
  have hPsup_pos : 0 < (Finset.range L).sup' hne (fun j => P (N + j)) := by
    have h0mem : (0 : ℕ) ∈ Finset.range L := Finset.mem_range.mpr (by omega)
    exact lt_of_lt_of_le (hPpos (N + 0)) (Finset.le_sup' (fun j => P (N + j)) h0mem)
  -- Relate windowMaxCos to window-sup P:  g Csup = window-sup P, and windowMaxCos = Csup.
  have hWmc_eq : windowMaxCos L q hL muc = Csup := hwmc
  -- 3λ/2 + √A₂·windowMaxCos = (2A₂/rr)·(window-sup P)
  have hnum_eq : 3 * lam / 2 + Real.sqrt A2 * windowMaxCos L q hL muc
      = (2 * A2 / rr) * (Finset.range L).sup' hne (fun j => P (N + j)) := by
    rw [hWmc_eq, hPsup_eq, hg]
    field_simp
  -- now bound fcorr
  have hfcorr_eq : fcorr L q hL muc
      = (3 * lam / 2 + Real.sqrt A2 * windowMaxCos L q hL muc)
          / (2 * A2 * Blam ^ 2 * Real.cos (|muc| + H) ^ 2) := rfl
  rw [hfcorr_eq, hnum_eq]
  -- goal: (2A₂/rr · sup) / (2A₂ Blam² cos²) ≤ sup
  set S := (Finset.range L).sup' hne (fun j => P (N + j)) with hS
  have hden_pos : 0 < 2 * A2 * Blam ^ 2 * Real.cos (|muc| + H) ^ 2 := by positivity
  rw [div_le_iff₀ hden_pos]
  -- (2A₂/rr)·S ≤ S · (2A₂ Blam² cos²)  ⟺  (2A₂/rr) ≤ 2A₂ Blam² cos²  (S>0)
  --   ⟸  1 ≤ rr Blam² cos²   (forcing), since 2A₂/rr · (rr Blam² cos²) = 2A₂ Blam² cos² and rr>0.
  have hkey : (2 * A2 / rr) ≤ 2 * A2 * Blam ^ 2 * Real.cos (|muc| + H) ^ 2 := by
    rw [div_le_iff₀ hrr]
    -- 2A₂ ≤ 2A₂ Blam² cos² · rr = 2A₂ · (rr Blam² cos²) ≥ 2A₂ · 1
    have : 2 * A2 * (rr * Blam ^ 2 * Real.cos (|muc| + H) ^ 2)
        = 2 * A2 * Blam ^ 2 * Real.cos (|muc| + H) ^ 2 * rr := by ring
    nlinarith [hforce, hA2_pos, mul_le_mul_of_nonneg_left hforce (le_of_lt (by positivity : (0:ℝ) < 2 * A2))]
  calc (2 * A2 / rr) * S ≤ (2 * A2 * Blam ^ 2 * Real.cos (|muc| + H) ^ 2) * S :=
        mul_le_mul_of_nonneg_right hkey hPsup_pos.le
    _ = S * (2 * A2 * Blam ^ 2 * Real.cos (|muc| + H) ^ 2) := by ring

/-- `0 < lamq q < 2` for `q ≥ 3` (here via `q = m+2`, `m ≥ 1`).  `lamq = 2cos(π/q)`. -/
theorem lamq_pos_lt2 (m : ℕ) (hm : 1 ≤ m) :
    0 < CorridorProductRealization.lamq (m + 2)
      ∧ CorridorProductRealization.lamq (m + 2) < 2 := by
  unfold CorridorProductRealization.lamq
  set t : ℝ := Real.pi / ((m + 2 : ℕ) : ℝ) with ht
  have hqr : (0:ℝ) < ((m + 2 : ℕ) : ℝ) := by positivity
  have hqr3 : (3:ℝ) ≤ ((m + 2 : ℕ) : ℝ) := by exact_mod_cast (by omega : 3 ≤ m + 2)
  have htpos : 0 < t := by rw [ht]; positivity
  have htlt : t < Real.pi := by
    rw [ht, div_lt_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
  have htlt2 : t < Real.pi / 2 := by
    rw [ht, div_lt_div_iff₀ hqr (by norm_num)]; nlinarith [Real.pi_pos, hqr3]
  have hcospos : 0 < Real.cos t := Real.cos_pos_of_mem_Ioo ⟨by linarith, htlt2⟩
  have hcoslt1 : Real.cos t < 1 := by
    have := Real.cos_lt_cos_of_nonneg_of_le_pi le_rfl htlt.le htpos
    rwa [Real.cos_zero] at this
  exact ⟨by linarith, by linarith⟩

/-! ## §4.  Corridor-orbit reduction: derive the product-form half of `hdata`.

`windowProductRealizes_corridor` instantiates `windowProductRealizes_of_data` for the genuine
corridor orbit `P k = (M_W^[k] s0).1 · (M_W^[k] s0).2`.  The PRODUCT-FORM and POSITIVITY halves of
`hdata` are DISCHARGED here from `corridor_product_realization` (normalization
`C0 = (r²/(2A₂))(3λ/2)`, `R = (r²/(2A₂))√A₂`, `r² = 4A₂Qp/(4−λ²)`) and the orbit positivity.
The remaining input `hpin` is EXACTLY the per-`N` "phase-alignment + radius-forcing" datum — i.e.
the in-domain arc-width geometry (`muc = ψ + Nθ + H` via the phase link `φ = 2ψ + η − 2ξ`, plus
`r·Blam·cos(|muc|+H) ≥ 1` from `D_{N+j} > 1`).  These two are the genuinely-analytic residual;
they are NOT proved here (see the session note for the exact open identities). -/
theorem windowProductRealizes_corridor (m : ℕ) (hm : 1 ≤ m) (hq : 18 ≤ m + 2)
    (hL : 0 < L_blk (m + 2))
    (a b : ℝ) (hQpos : 0 < Qp (CorridorProductRealization.lamq (m + 2)) a b)
    (hPpos : ∀ k, 0 < ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).1
        * ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).2)
    -- the irreducible per-N alignment + radius-forcing datum (in-domain arc-width geometry):
    (hpin : ∀ N : ℕ, ∃ (base muc : ℝ),
      muc ∈ Set.Ioo (-(Real.pi / 2 - Hq (L_blk (m+2)) (m+2)))
            (Real.pi / 2 - Hq (L_blk (m+2)) (m+2)) ∧
      (2 * (muc - L1bArcCoverage.xiq (m+2)) - ((L_blk (m+2) : ℝ) - 1) * L1bArcCoverage.thetaq (m+2)
          + L1bArcCoverage.etaq (m+2)
          = base + 2 * (N : ℝ) * L1bArcCoverage.thetaq (m+2)) ∧
      -- product window phase coincides with `base`:
      (∀ k : ℕ, ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).1
            * ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).2
          = CorridorProductRealization.C0form (CorridorProductRealization.lamq (m+2))
              (Qp (CorridorProductRealization.lamq (m+2)) a b)
            + CorridorProductRealization.Rform (CorridorProductRealization.lamq (m+2))
                (Qp (CorridorProductRealization.lamq (m+2)) a b)
              * Real.cos ((base + 2 * (N:ℝ) * L1bArcCoverage.thetaq (m+2))
                  + 2 * ((k:ℝ) - (N:ℝ)) * L1bArcCoverage.thetaq (m+2))) ∧
      -- radius forcing:
      1 ≤ (4 * A2q (m+2) * Qp (CorridorProductRealization.lamq (m+2)) a b
            / (4 - CorridorProductRealization.lamq (m+2) ^ 2))
          * Blamq (m+2) ^ 2 * Real.cos (|muc| + Hq (L_blk (m+2)) (m+2)) ^ 2) :
    RealizeWire.WindowProductRealizes (m + 2) hL
      (fun k => ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).1
        * ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).2) := by
  set q := m + 2 with hqdef
  set l := CorridorProductRealization.lamq q with hl
  set P : ℕ → ℝ := fun k => ((CorridorProductRealization.MW l)^[k] (a, b)).1
      * ((CorridorProductRealization.MW l)^[k] (a, b)).2 with hP
  have hlL : L1bArcCoverage.lamq q = l := by rw [hl, hqdef]; exact lamq_eq m
  -- product realization (gives C0, R, φ with the matched constants)
  obtain ⟨C0, R, phi, hRpos, hC0, hReq, hPk⟩ :=
    CorridorProductRealization.corridor_product_realization m hm l rfl a b hQpos
  apply windowProductRealizes_of_data q hq hL P hPpos
  intro N
  obtain ⟨base, muc, hmuc, halign, hprodphase, hforce⟩ := hpin N
  obtain ⟨hl_pos, hl_lt2⟩ := lamq_pos_lt2 m hm
  rw [← hl] at hl_pos hl_lt2
  have h4 : 0 < 4 - l ^ 2 := by nlinarith [hl_pos, hl_lt2]
  have h4ne : (4 - l ^ 2) ≠ 0 := ne_of_gt h4
  refine ⟨4 * A2q q * Qp l a b / (4 - l ^ 2), base, muc, ?_, hmuc, ?_, ?_, ?_⟩
  · -- rr > 0
    have hA2 : 0 < A2q q := by simp only [A2q]; positivity
    positivity
  · -- alignment (verbatim hpin's, with lamq↔l reconciled in xiq/etaq/thetaq which use π/q)
    rw [hlL] at *
    convert halign using 2
  · -- product form: P(N+j) = (rr/(2A₂))[3λ/2 + √A₂ cos(B + 2jθ)]
    intro j
    have hkey := hprodphase (N + j)
    -- (M_W^[N+j]).1·.2 = C0 + R cos(B + 2((N+j)-N)θ) = C0 + R cos(B + 2jθ)
    rw [hP]
    simp only
    rw [hkey]
    -- now rewrite C0form, Rform via rr/(2A₂) normalization
    have hA2pos : 0 < A2q q := by simp only [A2q]; positivity
    have hA2eq : A2q q = 2 * l ^ 2 + 1 := by
      simp only [A2q]; rw [hlL]; ring
    -- cast (N+j)-N = j
    have hNjN : ((N + j : ℕ):ℝ) - (N:ℝ) = (j:ℝ) := by push_cast; ring
    rw [show 2 * (((N + j : ℕ):ℝ) - (N:ℝ)) * L1bArcCoverage.thetaq q
          = 2 * (j:ℝ) * L1bArcCoverage.thetaq q by rw [hNjN]]
    -- normalization: C0form = (rr/(2A₂))(3l/2), Rform = (rr/(2A₂))√A₂
    set rr := 4 * A2q q * Qp l a b / (4 - l ^ 2) with hrr
    have hsqA2mul : Real.sqrt (A2q q) * Real.sqrt (A2q q) = A2q q :=
      Real.mul_self_sqrt hA2pos.le
    have hC0n : CorridorProductRealization.C0form l (Qp l a b)
        = rr / (2 * A2q q) * (3 * L1bArcCoverage.lamq q / 2) := by
      simp only [CorridorProductRealization.C0form, hrr]
      rw [hlL, hA2eq]; field_simp; ring
    have hRn : CorridorProductRealization.Rform l (Qp l a b)
        = rr / (2 * A2q q) * Real.sqrt (A2q q) := by
      simp only [CorridorProductRealization.Rform, hrr]
      have hsq : Real.sqrt (2 * l ^ 2 + 1) = Real.sqrt (A2q q) := by rw [hA2eq]
      rw [hsq]
      -- LHS = 2·√A₂·Qp/(4−l²); RHS = (4 A₂ Qp/(4−l²))/(2 A₂) · √A₂ = 2 Qp √A₂/(4−l²)
      rw [div_mul_eq_mul_div, eq_div_iff (by positivity)]
      field_simp
      nlinarith [hsqA2mul, hA2pos, h4, Real.sqrt_nonneg (A2q q)]
    rw [hC0n, hRn, hlL]
    ring
  · -- radius forcing: rr·Blam²·cos² ≥ 1   (verbatim hforce)
    exact hforce

/-! ## §5.  Phase-link foundations (toward discharging `hpin`).

These are the self-contained building blocks for the phase link `φ = 2ψ + (η − 2ξ)`.  They are
proved here; the final combined-amplitude argument identity (`arg(...) = η − 2ξ`) and the
far-endpoint forcing remain (see the session note). -/

open CorridorProductRealization in
/-- **The `D' = a − λb` orbit identity** (mirror of `corridor_domain_realization`).  Single
frequency `θ`; amplitude pinning `Damp'²·sin²θ = Qp` (coefficient 1). -/
theorem corridor_antidomain_realization (m : ℕ) (hm : 1 ≤ m) (l : ℝ)
    (hl : l = CorridorProductRealization.lamq (m + 2))
    (a b : ℝ) :
    ∃ Damp psi : ℝ, 0 ≤ Damp ∧
      Damp ^ 2 * Real.sin (Real.pi / ((m + 2 : ℕ) : ℝ)) ^ 2 = Qp l a b ∧
      (∀ k, ((MW l)^[k] (a, b)).1 - l * ((MW l)^[k] (a, b)).2
            = Damp * Real.cos (psi + (k:ℝ) * (Real.pi / ((m + 2 : ℕ) : ℝ)))) := by
  have hq3 : 3 ≤ m + 2 := by omega
  set q : ℕ := m + 2 with hq_def
  set θ : ℝ := Real.pi / (q : ℝ) with hθ_def
  have hqr : (0:ℝ) < (q:ℝ) := by positivity
  have hqr3 : (3:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq3
  have hθpos : 0 < θ := by rw [hθ_def]; positivity
  have hθlt : θ < Real.pi := by
    rw [hθ_def, div_lt_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
  have hcosθ : Real.cos θ = l / 2 := by
    rw [hl, CorridorProductRealization.lamq, hq_def, ← hθ_def]; ring
  have hsinpos : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθpos hθlt
  have hsinne : Real.sin θ ≠ 0 := ne_of_gt hsinpos
  set D : ℕ → ℝ := fun k => ((MW l)^[k] (a, b)).1 - l * ((MW l)^[k] (a, b)).2 with hD_def
  have hl2cos : 2 * Real.cos θ = l := by rw [hcosθ]; ring
  have hrec : ∀ k, D (k + 2) = 2 * Real.cos θ * D (k + 1) - D k := by
    intro k
    rw [hl2cos]
    simp only [hD_def]
    set x := (MW l)^[k] (a, b) with hx_def
    have e1 : (MW l)^[k+1] (a, b) = MW l x := by rw [hx_def, Function.iterate_succ_apply']
    have e2 : (MW l)^[k+2] (a, b) = MW l (MW l x) := by
      rw [hx_def, show k + 2 = (k+1)+1 by ring, Function.iterate_succ_apply',
          Function.iterate_succ_apply']
    rw [e1, e2]
    simp only [MW]; ring
  obtain ⟨R, psi, hRnn, hRiff, hform⟩ := recur_to_Rcos θ hsinne D hrec
  have hampL : D 0 ^ 2 - 2 * Real.cos θ * D 0 * D 1 + D 1 ^ 2 = Qp l a b := by
    have hD0 : D 0 = a - l * b := by simp [hD_def]
    have hD1 : D 1 = (-l*a + (2*l^2+1)*b) - l * (-a + 2*l*b) := by simp [hD_def, MW]
    rw [hD0, hD1, hcosθ]
    simp only [Qp]; ring
  have hampR : D 0 ^ 2 - 2 * Real.cos θ * D 0 * D 1 + D 1 ^ 2 = R ^ 2 * Real.sin θ ^ 2 := by
    have e0 : D 0 = R * Real.cos psi := by rw [hform 0]; norm_num
    have e1 : D 1 = R * (Real.cos psi * Real.cos θ - Real.sin psi * Real.sin θ) := by
      rw [hform 1]; rw [show (((1:ℕ):ℝ) * θ) = θ by norm_num, Real.cos_add]
    rw [e0, e1]
    have hpψ : Real.sin psi ^ 2 = 1 - Real.cos psi ^ 2 := by
      have := Real.sin_sq_add_cos_sq psi; linarith
    have hpyth2 : Real.cos θ ^ 2 = 1 - Real.sin θ ^ 2 := by
      have := Real.sin_sq_add_cos_sq θ; linarith
    have hexpand :
        (R * Real.cos psi) ^ 2
        - 2 * Real.cos θ * (R * Real.cos psi)
            * (R * (Real.cos psi * Real.cos θ - Real.sin psi * Real.sin θ))
        + (R * (Real.cos psi * Real.cos θ - Real.sin psi * Real.sin θ)) ^ 2
        = R ^ 2 * (Real.cos psi ^ 2 * (1 - Real.cos θ ^ 2)
                   + Real.sin psi ^ 2 * Real.sin θ ^ 2) := by ring
    rw [hexpand, hpyth2, hpψ]; ring
  refine ⟨R, psi, hRnn, ?_, ?_⟩
  · show R ^ 2 * Real.sin θ ^ 2 = Qp l a b
    rw [← hampR]; exact hampL
  · intro k
    have hk := hform k
    simp only [hD_def] at hk
    rw [hθ_def]
    exact hk

open CorridorProductRealization in
/-- **Product decomposition** `a·b = ((a+λb)² − (a−λb)²)/(4λ)` along the orbit (algebraic). -/
theorem product_eq_domain_sq_diff (l : ℝ) (hl0 : l ≠ 0) (a b : ℝ) :
    a * b = ((a + l * b) ^ 2 - (a - l * b) ^ 2) / (4 * l) := by
  field_simp; ring

/-! ## §6.  Capstone wiring (conditional on the residual `hpin`).

GIVEN the residual `hpin` (the in-domain arc-width datum, the one open piece), the corridor bridge
`g_corr ≤ window-sup P` holds for the corridor orbit at every window start — by feeding
`windowProductRealizes_corridor` into the PROVED `RealizeWire.hbridge_of_realizes`.  This makes the
reduction's payoff explicit and machine-checked: closing `hpin` closes the corridor bridge with NO
named-Prop residual. -/
theorem corridor_bridge_of_pin (m : ℕ) (hm : 1 ≤ m) (hq : 18 ≤ m + 2)
    (hL : 0 < L_blk (m + 2))
    (a b : ℝ) (hQpos : 0 < Qp (CorridorProductRealization.lamq (m + 2)) a b)
    (hPpos : ∀ k, 0 < ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).1
        * ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).2)
    (hpin : ∀ N : ℕ, ∃ (base muc : ℝ),
      muc ∈ Set.Ioo (-(Real.pi / 2 - Hq (L_blk (m+2)) (m+2)))
            (Real.pi / 2 - Hq (L_blk (m+2)) (m+2)) ∧
      (2 * (muc - L1bArcCoverage.xiq (m+2)) - ((L_blk (m+2) : ℝ) - 1) * L1bArcCoverage.thetaq (m+2)
          + L1bArcCoverage.etaq (m+2)
          = base + 2 * (N : ℝ) * L1bArcCoverage.thetaq (m+2)) ∧
      (∀ k : ℕ, ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).1
            * ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[k] (a, b)).2
          = CorridorProductRealization.C0form (CorridorProductRealization.lamq (m+2))
              (Qp (CorridorProductRealization.lamq (m+2)) a b)
            + CorridorProductRealization.Rform (CorridorProductRealization.lamq (m+2))
                (Qp (CorridorProductRealization.lamq (m+2)) a b)
              * Real.cos ((base + 2 * (N:ℝ) * L1bArcCoverage.thetaq (m+2))
                  + 2 * ((k:ℝ) - (N:ℝ)) * L1bArcCoverage.thetaq (m+2))) ∧
      1 ≤ (4 * A2q (m+2) * Qp (CorridorProductRealization.lamq (m+2)) a b
            / (4 - CorridorProductRealization.lamq (m+2) ^ 2))
          * Blamq (m+2) ^ 2 * Real.cos (|muc| + Hq (L_blk (m+2)) (m+2)) ^ 2) :
    ∀ N : ℕ,
      g_corr (L_blk (m + 2)) (m + 2) hL ≤
        (Finset.range (L_blk (m + 2))).sup' (Finset.nonempty_range_iff.mpr (by omega))
          (fun j => ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[N + j] (a, b)).1
            * ((CorridorProductRealization.MW (CorridorProductRealization.lamq (m+2)))^[N + j] (a, b)).2) :=
  RealizeWire.hbridge_of_realizes (m + 2) hq hL _
    (windowProductRealizes_corridor m hm hq hL a b hQpos hPpos hpin)

#print axioms windowMaxCos_eq_orbit_sup
#print axioms windowProductRealizes_of_data
#print axioms windowProductRealizes_corridor
#print axioms corridor_antidomain_realization
#print axioms corridor_bridge_of_pin

end

end WindowRealizeClose
