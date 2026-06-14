import Mathlib
import ToplevelStitch
import GenuineMapFacts

set_option maxHeartbeats 4000000

/-!
# GOAL-4 (other half) — q ≤ 21-UNCONDITIONAL, (P1)-DISCHARGED top-level theorem.

Two improvements over `ToplevelStitch.Xomega_lb_allq`, both this session's GOAL-4:

1. **(P1) is DISCHARGED, not carried.**  The q ≥ 22 corridor leg is produced through
   `ToplevelStitch.perq_Xomega_lb_qge19_P1discharged`, whose genuine-map definition
   supplies only the (P2) bridge (`GenuineClassP2`) — (P1) `hScalarDcorr` is now PROVED
   by `GenuineMapFacts.scalar_implies_Dcorr` and filled in by `GenuineClassP2.toGenuineClass`.
   So the GenuineClass conditionality is reduced to (P2) alone.

2. **The unconditional half covers q ∈ {5,7,…,21}** (17 Hecke indices), via
   `GenuineMapFacts.Xomega_lb_q5to21`.  The corridor + `fcorr_lb` route is needed only
   for q ≥ 22.

This file imports the q19/20/21 window files (via `GenuineMapFacts`); kept separate
from `ToplevelStitch.lean` so that file's P1-discharge does not block on the slow
window compilations.

`#print axioms Xomega_lb_allq_q5to21_P1` = `[propext, sorryAx, Classical.choice,
Quot.sound]` with the `sorryAx` traceable ONLY to `L1bArcCoverage.fcorr_lb`.
-/

namespace ToplevelStitch

open MeasureTheory

/-- **TOP-LEVEL ∀q UNIFORM HECKE ONSET — (P1) discharged, q ≤ 21 unconditional.**

* `q ∈ {5,7,…,21}`: UNCONDITIONAL (`Xomega_lb_q5to21`), 17 Hecke indices, no `fcorr_lb`.
* `q ≥ 22`: corridor route `hCorr22`, sole open analytic input `fcorr_lb` (carried via
  `L1b_carried`).

(P1) is PROVED (`scalar_implies_Dcorr`), so the genuine-map conditionality is (P2) only.
The single `sorryAx` is traceable ONLY to `L1bArcCoverage.fcorr_lb`. -/
theorem Xomega_lb_allq_q5to21_P1
    (q : ℕ) (hq : 5 ≤ q)
    (l : ℝ) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hmp21 : q ∈ ({5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21} : Finset ℕ) →
      GenuineMapFacts.mpolyq21 q l)
    (hμD : μ (UQ.Dcorr l)ᶜ = 0) (hinv : MeasurePreserving (UQ.Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UQ.Pprod x ≤ M)
    (hCorr22 : 22 ≤ q →
        (∀ (hL : 0 < L1bArcCoverage.L_blk q),
          1 / L1bArcCoverage.lamq q ^ 3 ≤
            L1bArcCoverage.g_corr (L1bArcCoverage.L_blk q) q hL) →
        1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ) :
    (q ∈ ({5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21} : Finset ℕ) →
       1 / l ^ 3 ≤ essSup (UQ.Pprod) μ) ∧
    (22 ≤ q → 1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ) := by
  constructor
  · -- q ∈ {5,7,…,21}: UNCONDITIONAL (17 indices).
    intro hqmem
    exact GenuineMapFacts.Xomega_lb_q5to21 q hqmem l (hmp21 hqmem) h2 hlo μ hμD hinv M hPbdd
  · -- q ≥ 22: corridor route, carrying `fcorr_lb` via `L1b_carried`.
    intro hq22
    have hq18 : 18 ≤ q := by omega
    exact hCorr22 hq22 (fun hL => L1b_carried q hq18 hL)

end ToplevelStitch

-- ════════════ AXIOM AUDIT ════════════
#print axioms GenuineMapFacts.Xomega_lb_q5to21
#print axioms ToplevelStitch.Xomega_lb_allq_q5to21_P1
