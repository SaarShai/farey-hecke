import Mathlib
/-!
# q=5 (Hecke G₅, λ=φ) window-5 core — WORK IN PROGRESS toward sharp X(5)=1/4

The sharp q=5 lower bound needs the **window-5** local lemma `g5_core` (no 5 consecutive products
`< 1/4`; the 4-window is FALSE — see `research_notes/g5_window4_refutation_2026-06-02.md`). The
floor case-split (`k₀,k₁,k₂,k₃ ≥ 1` over the window) has:

* **all-floor-1 (pure rotation):** handled HERE by `g5_rot3` — PROVEN, sorry-free, axiom-clean.
  (Margin is large: min over the floor-1 region of `max(P₀,P₁,P₂)` ≈ 0.3945 ≫ 1/4.)
* **defect cases (some `kᵢ ≥ 2`):** the tight `1/4` binding (the `(1,1,2)` entry pattern, max
  below-run 4) lives here. These are the hard residual goals — staged for Aristotle (see the
  dispatch package `research_notes/g5_aristotle_dispatch_2026-06-03.md`), NOT yet proven.

This file contains ONLY the proven `g5_rot3`; it compiles EXIT=0 with axioms
`[propext, Classical.choice, Quot.sound]`.
-/
open Int
noncomputable section

/-- `φ = (1+√5)/2 = 2cos(π/5)`. -/
noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2
lemma sqrt5_sq : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
lemma sqrt5_pos : (0:ℝ) < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
lemma phi_pos : 0 < phi := by unfold phi; have := sqrt5_pos; linarith
lemma phi_sq : phi ^ 2 = phi + 1 := by unfold phi; nlinarith [sqrt5_sq, sqrt5_pos]
lemma phi_lt2 : phi < 2 := by
  unfold phi
  have h5 : Real.sqrt 5 < 3 := by
    have : Real.sqrt 5 < Real.sqrt 9 := by
      apply Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    simpa [show (9:ℝ) = 3^2 by norm_num, Real.sqrt_sq (by norm_num : (0:ℝ) ≤ 3)] using this
  linarith

/-- **All-floor-1 (pure-rotation) sub-case of the q=5 window bound.** Three consecutive floor-1
steps (recurrences `a+c=φb`, `b+d=φc`, `c+e=φd` with the floor-1 *upper* bound `1+c < 2φd` at the
pair `(c,d)`), in region `a+φb>1`, cannot have both products `b·c` and `c·d` below `1/4`. (A
fortiori not all three of `a·b, b·c, c·d`.)

Proof: region at `(a,b)` gives `2φb − c > 1`; the floor-1 upper bound at `(c,d)` with `d = φc − b`
and `φ² = φ+1` gives `2φb < (2φ+1)c − 1`; adding ⟹ `φc > 1`. With `φc² = bc + cd < 1/2` and
`φ < 2` this is contradictory (`φc>1, c>0 ⟹ c < φc² < 1/2`, while `φc>1, φ<2 ⟹ c > 1/φ > 1/2`). -/
theorem g5_rot3 (a b c d : ℝ)
    (hc : 0 < c)
    (hr0 : a + c = phi * b)              -- floor-1 at (a,b)
    (hr1 : b + d = phi * c)              -- floor-1 at (b,c)
    (hub2 : 1 + c < 2 * (phi * d))       -- floor-1 UPPER bound at (c,d): (1+c)/(φd) < 2
    (hreg0 : a + phi * b > 1)            -- region at (a,b)
    (hbc : b * c < 1 / 4) (hcd : c * d < 1 / 4) :
    False := by
  have hsq := phi_sq
  have hpp := phi_pos
  have hp2 := phi_lt2
  -- φc² = bc + cd
  have hsumc : b * c + c * d = phi * c ^ 2 := by nlinarith [hr1]
  have hphic2 : phi * c ^ 2 < 1 / 2 := by nlinarith [hbc, hcd, hsumc]
  -- d = φc − b ; a = φb − c
  have hd_eq : d = phi * c - b := by linarith [hr1]
  have ha_eq : a = phi * b - c := by linarith [hr0]
  -- R0: 2φb − c > 1
  have hR0 : 2 * (phi * b) - c > 1 := by
    have : a + phi * b = 2 * (phi * b) - c := by rw [ha_eq]; ring
    linarith [hreg0, this]
  -- U2 expanded with φ²=φ+1:  1 + c < 2(φ+1)c − 2φb
  have hub2' : 1 + c < 2 * (phi + 1) * c - 2 * (phi * b) := by
    have hexp : 2 * (phi * d) = 2 * (phi + 1) * c - 2 * (phi * b) := by
      rw [hd_eq]; linear_combination (2 * c) * hsq
    linarith [hub2, hexp]
  -- φc > 1
  have hphic_gt1 : phi * c > 1 := by nlinarith [hub2', hR0]
  -- contradiction: φc²<1/2, φc>1, c>0, φ<2
  nlinarith [hphic2, hphic_gt1, hc, hp2, mul_pos hc hpp,
    mul_pos hc (show (0:ℝ) < phi * c - 1 by linarith)]

#print axioms g5_rot3
