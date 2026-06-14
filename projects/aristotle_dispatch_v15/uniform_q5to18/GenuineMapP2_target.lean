import Mathlib
import BCZHeckeS1_trichotomy
import GenuineMapP2

set_option maxHeartbeats 4000000

/-!
# `target_of_corridor` — the SOS-identity discharge of `PgenEjectTarget` (the analytic
half of the genuine-map P2 deep-mid ejection bridge).

This file proves the single named analytic inequality `GenuineMapP2.PgenEjectTarget`
from the two index-free corridor facts
  * `hu  : 1 < L l a b (i-1)`   (entry / minimality bound)
  * `hs  : 0 ≤ L l a b (i+1)`   (corridor-length positivity)
via the exact SOS identity
  `G(λ,u,v) = λ⁴v² − λ³uv + λ²v² − 1 = (u²−1) + (λv−u)(λ³v+λv+u)`.

It imports the SEALED `GenuineMapP2.lean` (read-only) and adds the new theorem
beside it (in a fresh namespace so no sealed declaration is touched).

`#print axioms GenuineMapP2_target.target_of_corridor` = `[propext, Classical.choice, Quot.sound]`.
-/

namespace GenuineMapP2_target

open HeckeS1

noncomputable section
variable (l : ℝ)

/-- **`PgenEjectTarget` from the two index-free corridor facts.**  At a deep-mid active
branch, with `u = L_{i-1}`, `v = L_i`, `s = L_{i+1}`: the entry bound `1 < u`, the corridor
positivity `0 ≤ s = L_{i+1}` (given the recurrence `L_{i+1} = λL_i − L_{i-1}`), and `0 < l`
give the target.  Proof: multiply by `l^3 > 0`; the exact identity
`l⁴v² − l³uv + l²v² − 1 = (u²−1) + (lv−u)(l³v + lv + u)` with `s = lv−u ≥ 0`,
`u² − 1 > 0`, cofactor `> 0`, closes it. -/
theorem target_of_corridor (a b : ℝ) (i : ℕ) (hl : 0 < l)
    (hu  : 1 < L l a b (i - 1))
    (hrec : L l a b (i + 1) = l * L l a b i - L l a b (i - 1))
    (hs  : 0 ≤ L l a b (i + 1)) :
    GenuineMapP2.PgenEjectTarget l a b i := by
  unfold GenuineMapP2.PgenEjectTarget
  set u := L l a b (i - 1) with hudef
  set v := L l a b i with hvdef
  -- s = l*v − u ≥ 0  (rewrite the recurrence)
  have hs' : 0 ≤ l * v - u := by rw [← hrec]; exact hs
  -- v > 0 : l*v ≥ u > 1 > 0 and l > 0
  have hv : 0 < v := by nlinarith [hs', hu, hl]
  -- the cofactor l³v + lv + u is positive
  have hcof : (0:ℝ) ≤ l ^ 3 * v + l * v + u := by
    have h1 : 0 ≤ l ^ 3 * v := by positivity
    have h2 : 0 ≤ l * v := by positivity
    linarith [hu]
  -- u² − 1 > 0  via (u−1)(u+1) > 0
  have husq : (0:ℝ) < (u - 1) * (u + 1) :=
    mul_pos (by linarith : (0:ℝ) < u - 1) (by linarith : (0:ℝ) < u + 1)
  -- The RHS in cleared form: `l*v² − u*v + v²/l = (l²*v² − l*u*v + v²)/l`.
  have hrhs : l * v ^ 2 - u * v + v ^ 2 / l
      = (l ^ 2 * v ^ 2 - l * u * v + v ^ 2) / l := by
    field_simp
  rw [hrhs]
  -- reduce `1/l³ ≤ X/l` (both denominators positive) to a polynomial inequality
  rw [div_le_div_iff₀ (by positivity : (0:ℝ) < l ^ 3) hl]
  -- goal: `1 * l ≤ (l²v² − luv + v²) * l³`, i.e. (after the SOS identity) `G ≥ 0`.
  -- SOS:  l⁴v² − l³uv + l²v² − 1 = (u²−1) + (lv−u)(l³v + lv + u).
  nlinarith [mul_nonneg hs' hcof, husq, sq_nonneg (l * v - u), hl, hv, hs',
             mul_pos hl hv]

end

end GenuineMapP2_target

-- ════════════ AXIOM AUDIT ════════════
#print axioms GenuineMapP2_target.target_of_corridor
