import Mathlib
/-!
# q=5 genuine per-branch envelope (goal D, the lower-bound reduction's key static input)

The genuine `G₅`-BCZ map has branches `i = 2,3,4`.  Numerically (`projects/mimo-mini-project/code/Dgoal_perbranch.py`) the
observable `P` is `< 1/φ³` ONLY on the scalar branch `i = q−1 = 4`; on the non-scalar branches
`i = 2,3` one has `P ≥ 1/φ³` pointwise.  This file machine-checks that **per-branch envelope** for
`i = 2,3`:

* `branch3_envelope` : on branch `i=3` (the cusp branch), `P₃ = a(a+φb)/φ ≥ 1/φ³`  (tight at the
  cusp vertex `(1/φ,0)`);
* `branch2_envelope` : on branch `i=2`, `P₂ = a(a+b) ≥ 1/φ³`  (in fact `≥ 1/φ² > 1/φ³`).

Consequence (the reduction): any genuine orbit step with `P < 1/φ³` is necessarily on the scalar
branch `i=4`.  Hence a run of consecutive `P < 1/φ³` is a run of consecutive **scalar-map** steps,
and the genuine no-sustained/lower-bound problem collapses to the purely scalar one (3-term
recurrence with `a ≤ 1`), whose ergodic-optimisation value `V(5)=1/4 > 1/φ³`.

Key algebraic identities (both verified by `nlinarith` via `φ²=φ+1`, `φ³=2φ+1`):
* `φ²a(a+φb) − 1 = φ²a·(φ(a+b)−1) + (φa−1)(1−a)`              (used when `a > 1/φ`),
* `φ²a(a+φb) − 1 = φ³·a·(b−1+φa) + (φ²a−1)(1−φa)`            (used when `a ≤ 1/φ`).

`#print axioms` shows only `[propext, Classical.choice, Quot.sound]`.
-/
open Int
noncomputable section

/-- `φ = (1+√5)/2 = 2cos(π/5) = λ₅`. -/
noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2
lemma sqrt5_sq : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
lemma sqrt5_pos : (0:ℝ) < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
lemma sqrt5_gt2 : (2:ℝ) < Real.sqrt 5 := by nlinarith [sqrt5_sq, sqrt5_pos]
lemma phi_pos : 0 < phi := by unfold phi; have := sqrt5_pos; linarith
lemma phi_sq : phi ^ 2 = phi + 1 := by unfold phi; nlinarith [sqrt5_sq, sqrt5_pos]
lemma phi_gt1 : 1 < phi := by unfold phi; have := sqrt5_gt2; linarith
lemma phi_lt2 : phi < 2 := by nlinarith [phi_sq, phi_gt1]
lemma phi_cube : phi ^ 3 = 2 * phi + 1 := by nlinarith [phi_sq]

/-- `1/φ³ = √5 − 2` (the genuine cusp value `X_Ω(5)`). -/
lemma inv_phi_cubed : 1 / phi ^ 3 = Real.sqrt 5 - 2 := by
  have h2p1 : 2 * phi + 1 = 2 + Real.sqrt 5 := by unfold phi; ring
  rw [phi_cube, h2p1, eq_comm, eq_div_iff (by positivity)]
  nlinarith [sqrt5_sq, sqrt5_pos]

/-- **Branch `i=3` (cusp branch) envelope.** Genuine branch-3 guards `φ(a+b)>1`, `a+φb≤1`; domain
`0<a≤1`, `1−φa<b`.  Then `P₃ = a(a+φb)/φ ≥ 1/φ³`. -/
theorem branch3_envelope (a b : ℝ)
    (ha : 0 < a) (ha1 : a ≤ 1) (hdb : 1 - phi * a < b)
    (hg1 : phi * (a + b) > 1) (hg2 : a + phi * b ≤ 1) :
    1 / phi ^ 3 ≤ a * (a + phi * b) / phi := by
  have hp := phi_pos
  have hp1 := phi_gt1
  have hd : 0 < b - 1 + phi * a := by linarith
  have hkey : 1 ≤ phi ^ 2 * (a * (a + phi * b)) := by
    rcases le_or_gt a (1 / phi) with hca | hca
    · -- a ≤ 1/φ:  φ²a(a+φb)−1 = φ³·a·d + (φ²a−1)(1−φa)  with d = b−1+φa.
      have hfa : phi * a ≤ 1 := by rw [mul_comm]; exact (le_div_iff₀ hp).mp hca
      have hlo : 1 ≤ phi ^ 2 * a := by nlinarith [phi_sq, hp, hp1, mul_pos hp hd, hg2]
      nlinarith [phi_sq, phi_cube, hp,
        mul_pos (mul_pos (show (0:ℝ) < phi ^ 3 by positivity) ha) hd,
        mul_nonneg (show (0:ℝ) ≤ phi ^ 2 * a - 1 by linarith)
                   (show (0:ℝ) ≤ 1 - phi * a by linarith)]
    · -- a > 1/φ:  φ²a(a+φb)−1 = φ²a·(φ(a+b)−1) + (φa−1)(1−a).
      have hfa : 1 ≤ phi * a := by
        have h := (div_lt_iff₀ hp).mp hca; rw [mul_comm] at h; linarith
      have hg1' : 0 < phi * (a + b) - 1 := by linarith
      nlinarith [phi_sq, phi_cube, hp,
        mul_pos (show (0:ℝ) < phi ^ 2 * a by positivity) hg1',
        mul_nonneg (show (0:ℝ) ≤ phi * a - 1 by linarith)
                   (show (0:ℝ) ≤ 1 - a by linarith)]
  have e : a * (a + phi * b) / phi - 1 / phi ^ 3
      = (phi ^ 2 * (a * (a + phi * b)) - 1) / phi ^ 3 := by field_simp
  have hnn : 0 ≤ a * (a + phi * b) / phi - 1 / phi ^ 3 := by
    rw [e]; exact div_nonneg (by linarith [hkey]) (by positivity)
  linarith

/-- **Branch `i=2` envelope.** Genuine branch-2 guards `φa+b>1`, `φ(a+b)≤1`; domain `0<a≤1`,
`1−φa<b`.  Then `P₂ = a(a+b) ≥ 1/φ³` (indeed `≥ 1/φ²`). -/
theorem branch2_envelope (a b : ℝ)
    (ha : 0 < a) (ha1 : a ≤ 1) (hdb : 1 - phi * a < b)
    (hg1 : phi * a + b > 1) (hg2 : phi * (a + b) ≤ 1) :
    1 / phi ^ 3 ≤ a * (a + b) := by
  have hp := phi_pos
  have hp1 := phi_gt1
  have hge2 : 1 / phi ^ 2 ≤ a * (a + b) := by
    have hkey : 1 ≤ phi ^ 2 * (a * (a + b)) := by
      nlinarith [phi_sq, hp, hp1, ha, ha1, hdb, hg1, hg2,
        mul_pos ha (show (0:ℝ) < phi * a + b - 1 by linarith),
        mul_nonneg ha.le (show (0:ℝ) ≤ 1 - phi * (a + b) by linarith),
        mul_nonneg ha.le (sub_nonneg.mpr ha1), sq_nonneg (phi * a - 1)]
    have e : a * (a + b) - 1 / phi ^ 2 = (phi ^ 2 * (a * (a + b)) - 1) / phi ^ 2 := by field_simp
    have hnn : 0 ≤ a * (a + b) - 1 / phi ^ 2 := by
      rw [e]; exact div_nonneg (by linarith [hkey]) (by positivity)
    linarith
  have hcube : 1 / phi ^ 3 ≤ 1 / phi ^ 2 := by
    apply div_le_div_of_nonneg_left (by norm_num) (by positivity)
    nlinarith [hp, hp1]
  linarith

#print axioms inv_phi_cubed
#print axioms branch3_envelope
#print axioms branch2_envelope
