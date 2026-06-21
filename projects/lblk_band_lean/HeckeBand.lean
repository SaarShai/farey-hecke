import Mathlib
/-!
# C-band: uniform Hecke band facts from λ_q = 2·cos(π/q)

This file proves, **uniformly for all q ≥ 7** (m = q-2 ≥ 5), the four "band facts"
about the Hecke value `λ_q = 2·cos(π/q)` that the genuine-self-map / corridor legs
of the uniform-onset proof currently carry as per-q numeric hypotheses
(`h1 : 1<λ`, `h2 : λ<2`, `hlo : 9/5<λ`, `hlphi : λ² ≥ λ+1`):

  **hecke_band**:  ∀ q ≥ 7,  with λ = 2·cos(π/q):
     1 < λ  ∧  λ < 2  ∧  9/5 < λ  ∧  λ² ≥ λ + 1.

## Threshold note (THE binding fact)

`9/5 < λ` ⟺ `cos(π/q) > 9/10`.  This holds for all q ≥ 7 because cos is increasing
in q (π/q shrinks), and at the boundary `cos(π/7) = 0.9009689…  > 0.9`.  It does
**NOT** hold at q = 5, 6: `cos(π/5) = 0.809 → λ = 1.618 < 1.8` and
`cos(π/6) = √3/2 = 0.866 → λ = 1.732 < 1.8`.  So the uniform band fact is stated
`q ≥ 7`; the q=5,6 legs of the onset proof remain on their separate 9/5-free routes.

`λ² ≥ λ + 1` ⟺ `λ ≥ φ = (1+√5)/2 = 1.618…` ⟺ `cos(π/q) ≥ φ/2 = 0.809 = cos(π/5)`,
which already holds for q ≥ 5; certainly for q ≥ 7.  Here it follows for free from
`λ ≥ 1.8` (since `1.8² - 1.8 - 1 = 0.44 > 0`).

## Proof spine

The whole thing reduces to ONE tight numeric fact: `cos(π/7) > 0.9`.  The degree-4
Taylor envelope `Real.cos_bound` is too loose at π/7 (it only gives ≳ 0.897), so we
go through the **half-angle**: `cos(π/7) = 2·cos(π/14)² − 1`, and bound `cos(π/14)`
with `cos_bound` (much tighter at the smaller angle: `cos(π/14) ≥ 0.97469`), giving
`cos(π/7) ≥ 2·0.97469² − 1 = 0.90004 > 0.9`.  Monotonicity in q
(`Real.cos_le_cos_of_nonneg_of_le_pi`) lifts this to all q ≥ 7.

AXIOMS: [propext, Classical.choice, Quot.sound] (sorryAx-free — see `#print axioms`).
-/

namespace HeckeBand

open Real

/-- The Hecke value `λ_q = 2 cos(π/q)`. -/
noncomputable def lam (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)

/-! ### Step 1 — the binding numeric core: `cos(π/7) > 0.9`, via the half-angle. -/

/-- Tight lower bound on `cos(π/14)` from the degree-4 Taylor envelope.
At the small angle π/14 ≈ 0.2244 the envelope is sharp. -/
theorem cos_pi14_ge : (0.97469 : ℝ) ≤ Real.cos (Real.pi / 14) := by
  -- π/14 bounds from π ∈ (3.141592, 3.141593)
  have hp_lo : (0.2243994 : ℝ) ≤ Real.pi / 14 := by
    have := Real.pi_gt_d6; linarith
  have hp_hi : Real.pi / 14 ≤ (0.2243996 : ℝ) := by
    have := Real.pi_lt_d6; linarith
  have hnn : (0:ℝ) ≤ Real.pi / 14 := by positivity
  have hb : |Real.pi / 14| ≤ 1 := by
    rw [abs_of_nonneg hnn]; linarith
  have hcb := Real.cos_bound hb
  rw [abs_le] at hcb
  -- |x|^4 = x^4 since x ≥ 0
  have hax : |Real.pi / 14| ^ 4 = (Real.pi / 14) ^ 4 := by
    rw [← abs_pow]; exact abs_of_nonneg (by positivity)
  rw [hax] at hcb
  -- bound x^2 and x^4 from above using the tight interval
  have hsq : (Real.pi / 14) ^ 2 ≤ (0.2243996 : ℝ) ^ 2 := by
    nlinarith [hp_lo, hp_hi, sq_nonneg (Real.pi / 14)]
  have hqt : (Real.pi / 14) ^ 4 ≤ (0.2243996 : ℝ) ^ 4 := by
    nlinarith [hsq, sq_nonneg ((Real.pi / 14) ^ 2)]
  -- lower bound: cos x ≥ 1 - x²/2 - (5/96) x⁴
  -- with x² ≤ 0.2243996², x⁴ ≤ 0.2243996⁴
  nlinarith [hcb.1, hsq, hqt]

/-- The binding core: `cos(π/7) > 0.9`, via `cos(π/7) = 2·cos(π/14)² − 1`. -/
theorem cos_pi7_gt : (0.9 : ℝ) < Real.cos (Real.pi / 7) := by
  -- double-angle: cos(2y) = 2 cos²(y) - 1, with y = π/14, so 2y = π/7
  have hdb : Real.cos (Real.pi / 7) = 2 * Real.cos (Real.pi / 14) ^ 2 - 1 := by
    have : Real.pi / 7 = 2 * (Real.pi / 14) := by ring
    rw [this, Real.cos_two_mul]
  rw [hdb]
  have h14 := cos_pi14_ge
  -- cos(π/14) ≥ 0.97469 ≥ 0 ⇒ 2·(0.97469)² - 1 = 0.90003... > 0.9
  have hpos : (0:ℝ) ≤ Real.cos (Real.pi / 14) := by linarith [h14]
  nlinarith [h14, hpos]

/-! ### Step 2 — monotonicity lift to all q ≥ 7. -/

/-- For `q ≥ 7`, `cos(π/q) ≥ cos(π/7) > 0.9`. -/
theorem cos_piq_gt (q : ℕ) (hq : 7 ≤ q) : (0.9 : ℝ) < Real.cos (Real.pi / q) := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have h7 : (7:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have hle : Real.pi / q ≤ Real.pi / 7 :=
    div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num) h7
  have hpos : 0 ≤ Real.pi / q := by positivity
  have hmono : Real.cos (Real.pi / 7) ≤ Real.cos (Real.pi / q) :=
    Real.cos_le_cos_of_nonneg_of_le_pi hpos
      (by linarith [Real.pi_le_four, Real.pi_pos]) hle
  linarith [cos_pi7_gt, hmono]

/-! ### Step 3 — assemble the four band facts. -/

/-- **C-band (uniform Hecke band facts).**
For every `q ≥ 7`, the Hecke value `λ = 2·cos(π/q)` satisfies
`1 < λ`, `λ < 2`, `9/5 < λ`, and `λ² ≥ λ + 1`. -/
theorem hecke_band (q : ℕ) (hq : 7 ≤ q) :
    1 < lam q ∧ lam q < 2 ∧ 9/5 < lam q ∧ lam q ^ 2 ≥ lam q + 1 := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  -- the binding lower bound cos(π/q) > 0.9
  have hlo_cos : (0.9 : ℝ) < Real.cos (Real.pi / q) := cos_piq_gt q hq
  -- the upper bound cos(π/q) < 1 (for the λ < 2 fact)
  have ht_pos : 0 < Real.pi / q := by positivity
  have hq7 : (7:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  -- π/q ≤ π/7 ≤ π < 2π, and -(2π) < 0 < π/q
  have ht_lt2pi : Real.pi / q < 2 * Real.pi := by
    have : Real.pi / q ≤ Real.pi := by
      rw [div_le_iff₀ hqr]; nlinarith [Real.pi_pos]
    nlinarith [Real.pi_pos]
  have ht_gt : -(2 * Real.pi) < Real.pi / q := by nlinarith [Real.pi_pos, ht_pos]
  have hne : Real.cos (Real.pi / q) ≠ 1 := by
    have hiff := (Real.cos_eq_one_iff_of_lt_of_lt ht_gt ht_lt2pi)
    intro hcos
    have := hiff.1 hcos
    linarith
  have hhi_cos : Real.cos (Real.pi / q) < 1 :=
    lt_of_le_of_ne (Real.cos_le_one _) hne
  unfold lam
  refine ⟨by linarith, by linarith, by linarith, ?_⟩
  -- λ ≥ 1.8 ⇒ λ² - λ - 1 ≥ 1.8² - 1.8 - 1 = 0.44 > 0
  have hge : (1.8 : ℝ) ≤ 2 * Real.cos (Real.pi / q) := by linarith
  nlinarith [hge]

/-! ### Consumer-facing form.

The per-q lower/equality theorems of the onset proof carry a hypothesis
`hHecke : l = 2 · cos(π/(m+2))` with `m = q-2`.  This packaged form lets a caller
discharge all four band hypotheses (`h1 h2 hlo hlphi`) from `hHecke` and `7 ≤ m+2`
(equivalently `5 ≤ m`) in one shot, replacing the per-q numeric `norm_num` discharge. -/
theorem hecke_band_of_eq {l : ℝ} (m : ℕ) (hm : 5 ≤ m)
    (hHecke : l = 2 * Real.cos (Real.pi / (m + 2))) :
    1 < l ∧ l < 2 ∧ 9/5 < l ∧ l ^ 2 ≥ l + 1 := by
  have hq : 7 ≤ m + 2 := by omega
  have hcast : ((m + 2 : ℕ) : ℝ) = (m : ℝ) + 2 := by push_cast; ring
  have hb := hecke_band (m + 2) hq
  unfold lam at hb
  rw [hcast] at hb
  rw [hHecke]
  exact hb

end HeckeBand
