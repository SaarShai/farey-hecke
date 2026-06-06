# Bridge robustness gate — the slowest-torsion claim was tuning; a cusp/torsion-free dichotomy survives

**Date:** 2026-06-05 (supersedes the strong claims of `FINDINGS_bridge_crossgroup_2026-06-05.md`).
Source: workflow `bridge-robustness` (wf_341f4995-1c2, 6 agents, M1/M2 exact periodic-word enumeration).
The prior cross-group round used a DIFFERENT, partly hand-tuned observable per group. This round FROZE one
canonical observable (blind to outcomes) and re-tested. Structural trace facts independently re-checked;
the per-group enumeration minima are subagent numerics (M1/M2), NOT re-run by me.

## The frozen observable (forced, not tuned)
`ψ(x) := 1/R(x)`, R = first-return (suspension) roof of the geodesic flow over the group's standard
boundary coding. Orbit-sum `Σ R = ℓ(γ) = 2 arccosh(|tr M|/2)` (translation length). On the Hecke coding
`R = R_q` exactly, so **`ψ = 1/R_q = P` identically** (equality, not monotone-equivalence) — the Hecke
min-ess-sup is literally unchanged. Two natural variants were tested and REJECTED as negative controls:
bare mean-roof `ℓ/L` (selects the wrong q=3 element) and single-step `log‖Mv‖` (direction-dependent). So
the L∞/ess-sup aggregation of the reciprocal roof is forced.

## Retest results (frozen observable, exact word enumeration)
| group | structure | extremizer under ψ=1/R | attained | systole rejected | vs prior |
|---|---|---|---|---|---|
| **Γ(2)** | torsion-free, 3 cusps | **parabolic cusp**, 2/9 | no | **yes, 1.86×** | **AGREES** |
| **octagon** | cocompact, torsion-free | **hyperbolic systole** | yes | no (ratio 1.0) | agrees (coarse) |
| **(2,4,6)** | cocompact, elliptic | **hyperbolic** (cocycle cancellation) | no (degenerate→0) | no (artifact ∞) | **DISAGREES** |
| **(2,3,7)** | cocompact, elliptic | **hyperbolic systole** (ratio 1.0) | yes | no | **DISAGREES** (refutes prediction) |

## What this decides
- **The strong "slowest-torsion selection + ~1.7× systole rejection in cocompact-torsion groups" claim is
  an ARTIFACT of per-group observable tuning.** The two load-bearing cases — (2,4,6) (prior "decisive
  positive") and (2,3,7) (the designed confirmation) — BOTH collapse under the freeze.
- **The recurring ~1.7× ratio is downgraded** from "suggestive possible law" to a cusp-group coincidence
  (Γ(2)/Hecke 1.72–1.86×) that EVAPORATES in cocompact-torsion groups (degenerate in (2,4,6); 1.0 in
  (2,3,7)).
- **What SURVIVES (observable-independent, both anchors reproduce under the freeze):** a **cusp /
  torsion-free dichotomy** — cusped groups (Γ(2), Hecke) escape to a NON-ATTAINED parabolic extremizer;
  torsion-free cuspless groups (octagon) ATTAIN the hyperbolic systole. This is the honest surviving result.

## Honest status tags
- **PROVEN-structural (certain, observable-independent, re-verified):** Γ(2) torsion-free ⇒ non-hyperbolic
  = parabolic-cusp only; (2,4,6) elliptic top `2cos(π/6)=√3 < 2 < √6` systole; (2,3,7) elliptic spectrum
  `{0,1,1.80194} < 2 < 2.24698` systole; octagon cocompact torsion-free ⇒ all non-identity hyperbolic,
  `R=log|f'| ≤ ℓ_sys` ⇒ `X=1/ℓ_sys` attained at systole.
- **NUMERICAL (subagent M1/M2, NOT re-run by me):** all exact-enumeration minima; the cocycle-cancellation
  diagnosis for (2,4,6); the (2,3,7) per-length floor (min-stable from L=4, robust to horizon); octagon SFT
  counts.
- **ROOT-CAUSE diagnosis (the valuable finding):** elliptic-generator CORNER-ROTATION codings have no
  canonically POSITIVE roof — `1/R` is then governed by sign-crossings/cancellation, not cone-dwell — so the
  frozen observable cannot select an elliptic element on that coding. This is WHY (2,4,6)/(2,3,7) fail.

## The open door — RESOLVED (2026-06-05, same day): OUTCOME B
The discriminator was RUN (workflow `bowenseries-246-discriminator`, M1 exact periodic-word enumeration).
A genuine positive-roof Bowen-Series SIDE-PAIRING coding for (2,4,6) was built — `R = log|f'| > 0` verified
canonically positive on all of S¹ (the premise the corner-rotation coding violated), orbit-sum identity
`Σ R = ℓ(γ) = 2 arccosh(|tr|/2)` confirmed to residual ~1e-40. Same frozen `ψ=1/R` applied mechanically.
**RESULT = OUTCOME B (the slowest-torsion law does NOT survive):**
- min-ess-sup is ATTAINED at the hyperbolic SYSTOLE `bC` (|tr|=√6, X≈1.56898), NOT the slowest (order-6)
  elliptic and NOT a non-attained cone-hugging limit. Strict global floor over 193 admissible classes to L=11.
- The order-6 CONE-HUGGING hyperbolic family does NOT drift below the systole: winding ever-tighter pushes
  |tr| DOWN toward the order-6 elliptic value √3 < 2, so the family EXITS the hyperbolic set (hits the
  "elliptic wall") before it can compete. 0/13 cone-hugging words (|tr| up to 36.8) below the systole floor.
- Robust across all 13 tested valid (positive-roof) centers z0 (the qualitative outcome is z0-invariant;
  only the numeric value of X depends on z0). Honest caveat: a fully coordinate-free symmetry-canonical
  center was not singled out, but "attained short hyperbolic minimizer, no cone-hug drift" holds at every
  valid center.
**Conclusion:** the prior (2,4,6) failure was NOT corner-rotation coding degeneracy. The slowest-torsion
selection law genuinely FAILS for cocompact-torsion groups under a positive-roof canonical observable. The
ONLY surviving cross-group result is the **cusp / torsion-free dichotomy** — now established, not pending.

## Realistic ceiling (unchanged, now better-supported)
Novelty-of-formulation for the **cusp / torsion-free dichotomy** (min-ess-sup over the BCZ/Bowen-Series
cocycle escapes to a non-attained cusp extremizer iff the group is cusped), distinct from Lagrange–Markov.
NOT a slowest-torsion selection law. The cocompact-torsion case is OPEN pending the Bowen-Series discriminator.
