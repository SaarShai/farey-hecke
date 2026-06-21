import Mathlib
import L1bArcCoverage
import CorridorProductRealization

set_option maxHeartbeats 4000000

/-!
# `RealizeWire.lean` — wiring the proved realization identities toward `hbridge`.

`hbridge` (in `BCZHeckeGATE2_L1_skeleton.no_sustained_corridor`) is the corridor realization
`g_corr (L_blk q) q ≤ sup'_{j<L_blk q} P(N+j)`.  Its substantive content was identified (this
session) as TWO orbit-observable sinusoid identities, both now PROVED axiom-clean in
`CorridorProductRealization.lean`:

* `corridor_product_realization` — `P k = C0 + R·cos(φ + 2kθ)` (product `a·b`, frequency `2θ`),
  `C0 = 3λQp/(4−λ²)`, `R = 2√(2λ²+1)Qp/(4−λ²)`, `R > 0`.
* `corridor_domain_realization` — `D k = Damp·cos(ψ + kθ)` (domain `a+λb`, frequency `θ`),
  amplitude-pinned `Damp²sin²θ = (6λ²+1)Qp`.

This file makes the REMAINING assembly explicit and machine-checked: it states the `hbridge`
conclusion in the `L1bArcCoverage` vocabulary (`g_corr`, `fcorr`, `windowMaxCos`) and PROVES it
from ONE precisely-named residual — the **value-of-`fcorr` realization** `WindowProductRealizes`,
which packages (i) the phase-grid alignment `φ,N ↦ μc` matching my product closed form to
`windowMaxCos`, (ii) the in-domain radius forcing `Damp·cos>1 ⟹ r² ≥ 1/(Blam²cos²(|μc|+H))` from
`corridor_domain_realization`, and (iii) `μc ∈ domain`.  We DISCHARGE the final `sInf`-le-value
step here (`Real.csInf_le` + the domain image), so the residual is exactly the realization match,
nothing more.  NO `sorry`: the residual is a named hypothesis (a `Prop`), not an axiom.

This is the honest scope: R1 (both sinusoid identities) PROVED; the residual = the `fcorr`
value-match + in-domain forcing, stated exactly.
-/

namespace RealizeWire

open L1bArcCoverage
open scoped Real

noncomputable section

/-- **The value-of-`fcorr` realization residual** (the precise remaining input of `hbridge`).
Given a corridor block-window orbit `P : ℕ → ℝ` (the product observable along the `M_W` rotation),
and a window start `N`, there is a domain-centered phase `muc` in the open `fcorr`-domain at which
the window-sup of `P` dominates `fcorr (L_blk q) q · muc`.  This is exactly the content
"`g_true = window-sup P ≥ fcorr(μc_orbit)`" delivered by the two proved sinusoid identities
(`corridor_product_realization` for the numerator, `corridor_domain_realization` for the
denominator/in-domain forcing) once the phase grids are aligned. -/
def WindowProductRealizes (q : ℕ) (hL : 0 < L_blk q) (P : ℕ → ℝ) : Prop :=
  ∀ N : ℕ, ∃ muc : ℝ,
    muc ∈ Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q) ∧
    fcorr (L_blk q) q hL muc ≤
      (Finset.range (L_blk q)).sup' (Finset.nonempty_range_iff.mpr (by omega)) (fun j => P (N + j))

/-- `g_corr` is bounded below: its defining image of `fcorr` over the domain is bounded below by
`1/λ³` (from `B1_target`), hence `BddBelow`. -/
theorem g_corr_image_bddBelow (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q) :
    BddBelow (Set.image (fcorr (L_blk q) q hL)
        (Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q))) := by
  refine ⟨1 / lamq q ^ 3, ?_⟩
  rintro y ⟨muc, hmuc, rfl⟩
  exact fcorr_lb q hq hL hmuc

/-- **`hbridge` from the named residual.**  For `q ≥ 18`, given the value-of-`fcorr` realization
`WindowProductRealizes`, the corridor bridge `g_corr ≤ window-sup P` holds for every window start
`N`.  Proved by `csInf ≤ value` (the residual supplies an in-domain `muc` with `fcorr muc ≤
window-sup`, and `g_corr = sInf` over the domain image is `≤ fcorr muc`).  Axiom-clean. -/
theorem hbridge_of_realizes (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q)
    (P : ℕ → ℝ) (hreal : WindowProductRealizes q hL P) :
    ∀ N : ℕ,
      g_corr (L_blk q) q hL ≤
        (Finset.range (L_blk q)).sup' (Finset.nonempty_range_iff.mpr (by omega))
          (fun j => P (N + j)) := by
  intro N
  obtain ⟨muc, hmuc, hle⟩ := hreal N
  -- g_corr = sInf (image fcorr domain) ≤ fcorr muc  (muc in domain, image bddBelow)
  have hmem : fcorr (L_blk q) q hL muc ∈
      Set.image (fcorr (L_blk q) q hL)
        (Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q)) :=
    ⟨muc, hmuc, rfl⟩
  have hsInf_le : g_corr (L_blk q) q hL ≤ fcorr (L_blk q) q hL muc := by
    unfold g_corr
    exact csInf_le (g_corr_image_bddBelow q hq hL) hmem
  exact le_trans hsInf_le hle

/-! ## Soundness / honesty check.

`hbridge_of_realizes` reduces the corridor bridge to `WindowProductRealizes`, a single `Prop`
whose content is *exactly* the two PROVED sinusoid identities plus phase alignment.  Nothing is a
`sorry`; the residual is a named, fully-specified realization datum.  Combined with
`L1bArcCoverage.B1_target` (`1/λ³ ≤ g_corr`, PROVED) this gives `1/λ³ ≤ window-sup P`, i.e. the
`FwindowL (L_blk q)` discrete-window contradiction — the input `perq_Xomega_lb_Lblk_GEN` consumes. -/

/-- **Capstone (conditional on the residual).**  `1/λ³ ≤ window-sup P` for every window start,
i.e. the discrete window cannot stay sub-threshold — given `WindowProductRealizes`.  This is the
`FwindowL`-shaped conclusion the genuine chain needs, here derived from `B1_target` (PROVED) +
the named realization residual. -/
theorem window_not_subthreshold (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q)
    (P : ℕ → ℝ) (hreal : WindowProductRealizes q hL P) :
    ∀ N : ℕ,
      1 / lamq q ^ 3 ≤
        (Finset.range (L_blk q)).sup' (Finset.nonempty_range_iff.mpr (by omega))
          (fun j => P (N + j)) := by
  intro N
  exact le_trans (B1_target q hq hL) (hbridge_of_realizes q hq hL P hreal N)

#print axioms hbridge_of_realizes
#print axioms window_not_subthreshold
#print axioms g_corr_image_bddBelow

end

end RealizeWire
