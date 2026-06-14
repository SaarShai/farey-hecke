import BCZHeckeRotationArc
set_option maxHeartbeats 1600000
/-!
# `BCZHeckeRotationArcR2hi2.lean` — extending the R2 realization ladder to `q = 10, 12, 13`.

A **new, self-contained** companion to `BCZHeckeRotationArc.lean` (`namespace HeckeRotArc`), which
it `import`s.  It touches NO sealed/verified file (`BCZHeckeRotationArc`, `…R1`, `…R2`, `…R2hi`,
`…R3Parity` are all left untouched).  It continues the per-`q` realization of residual **R2** —
supplying the `hrealize` bridge of `HeckeRotArc.Bq_eq_rotation_arc` by exhibiting an actual genuine
sub-threshold last-branch cluster run achieving the rotation-arc count — for the next `q` beyond the
`q = 8, 9` arcs of `BCZHeckeRotationArcR2hi.lean`.

The realization body is **identical per q** to the `q = 7, 8, 9` pattern (keep `Xq := 1/λ_q³`
directly, prove `P < 1/λ³` by clearing the positive denominator `λ³`, which needs only the per-`q`
minpoly to reduce high powers plus a tight rational two-sided bound on `λ_q`).  The only growing cost
is the per-`q` minimal-polynomial identity for `λ_q = 2cos(π/q)`.

Exact witnesses: `code/out/goal1_qladder_witness_exact.json` (q=8..16), all interior `k=1`.

| q  | minpoly of `λ_q = 2cos(π/q)` | deg | start (over ℚ) | realized `N+1 = B(q)` |
|----|------------------------------|-----|----------------|-----------------------|
| 10 | `x⁴ − 5x² + 5`              | 4   | `(1/3, 3/8)`   | 3                     |
| 12 | `x⁴ − 4x² + 1`              | 4   | `(1/3, 11/30)` | 3                     |
| 13 | `x⁶ − x⁵ − 5x⁴ + 4x³ + 6x² − 3x − 1` | 6 | `(31/94, 17/47)` | **4** (first length-4 arc) |

`#print axioms` on every `Bq_eq_rotation_arc_q{q}` below is `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeRotArcR2hi2

open HeckeRotArc

noncomputable section

/-! ## §1.  q = 10 — quartic field `Q(λ₁₀)`, `λ₁₀ = 2cos(π/10)`, minpoly `x⁴ − 5x² + 5`, `B(10) = 3`.

From the double-angle `λ₁₀² = 2 + 2cos(π/5) = (5+√5)/2` and `cos(π/5) = (1+√5)/4`:
`2λ₁₀² − 5 = √5` ⟹ `(2λ₁₀² − 5)² = 5` ⟹ `λ₁₀⁴ − 5λ₁₀² + 5 = 0`. -/

def lam10 : ℝ := 2 * Real.cos (Real.pi / 10)

lemma lam10_pos : 0 < lam10 := by
  unfold lam10
  apply mul_pos (by norm_num : (0:ℝ) < 2)
  exact Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

/-- `λ₁₀² = (5 + √5)/2`, from `2cos²(π/10) = 1 + cos(π/5)` and `cos(π/5) = (1+√5)/4`. -/
lemma lam10_sq : lam10 ^ 2 = (5 + Real.sqrt 5) / 2 := by
  unfold lam10
  have hdouble : Real.cos (2 * (Real.pi / 10)) = 2 * Real.cos (Real.pi / 10) ^ 2 - 1 :=
    Real.cos_two_mul _
  have h25 : (2:ℝ) * (Real.pi / 10) = Real.pi / 5 := by ring
  rw [h25, Real.cos_pi_div_five] at hdouble
  nlinarith [hdouble]

/-- The quartic identity `λ₁₀⁴ − 5λ₁₀² + 5 = 0`. -/
lemma lam10_quartic : lam10 ^ 4 - 5 * lam10 ^ 2 + 5 = 0 := by
  have hsq := lam10_sq
  have hr5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  -- (2λ²−5) = √5, square both sides
  have h : (2 * lam10 ^ 2 - 5) = Real.sqrt 5 := by rw [hsq]; ring
  have h2 : (2 * lam10 ^ 2 - 5) ^ 2 = 5 := by rw [h]; exact hr5
  nlinarith [h2]

lemma lam10_quartic' : lam10 ^ 4 = 5 * lam10 ^ 2 - 5 := by linarith [lam10_quartic]

/-- `√2 ≤ λ₁₀` (so `λ₁₀² ≥ 2`), from `cos(π/4) ≤ cos(π/10)`. -/
lemma lam10_ge_sqrt2 : Real.sqrt 2 ≤ lam10 := by
  unfold lam10
  have h_mono : Real.cos (Real.pi / 4) ≤ Real.cos (Real.pi / 10) := by
    apply Real.cos_le_cos_of_nonneg_of_le_pi
    · linarith [Real.pi_pos]
    · linarith [Real.pi_gt_three]
    · apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num : (0:ℝ) < 4)
        (by norm_num : (4:ℝ) ≤ 10)
  have h_cos_pi4 : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 := by rw [Real.cos_pi_div_four]
  rw [h_cos_pi4] at h_mono
  linarith [mul_le_mul_of_nonneg_left h_mono (by norm_num : (0:ℝ) ≤ 2)]

lemma lam10_sq_ge_two : (2:ℝ) ≤ lam10 ^ 2 := by
  have h := lam10_ge_sqrt2
  have hr2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  nlinarith [h, hr2, Real.sqrt_nonneg 2, lam10_pos]

lemma lam10_gt_one : 1 < lam10 := by
  have h := lam10_ge_sqrt2
  have h1 : 1 < Real.sqrt 2 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp [Real.sqrt_one]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith

lemma lam10_sq_lt_four : lam10 ^ 2 < 4 := by
  -- u = λ²; u² − 5u + 5 = 0 and u ≥ 2 ⟹ u < 4 (since the poly is >0 for u ≥ 4)
  have hq := lam10_quartic
  have hge := lam10_sq_ge_two
  nlinarith [hq, hge, sq_nonneg (lam10 ^ 2 - 4), pow_pos lam10_pos 2]

lemma lam10_lt_two : lam10 < 2 := by
  nlinarith [lam10_sq_lt_four, lam10_pos, sq_nonneg (lam10 - 2)]

set_option maxHeartbeats 800000 in
/-- `λ₁₀ > 19021/10000`. -/
lemma lam10_gt : (19021 : ℝ) / 10000 < lam10 := by
  by_contra h
  push_neg at h
  have hq := lam10_quartic
  have hone := lam10_gt_one
  have htwo := lam10_lt_two
  have hfactor : (0:ℝ) < (lam10 + (19021:ℝ)/10000) * (lam10^2 + ((19021:ℝ)/10000)^2 - 5) := by
    nlinarith [hone, htwo, lam10_sq_ge_two, sq_nonneg lam10, sq_nonneg (lam10 - 1)]
  have hdiff : (19021:ℝ)/10000 - lam10 ≥ 0 := by linarith
  have hpoly : ((19021:ℝ)/10000 - lam10) *
      ((lam10 + (19021:ℝ)/10000) * (lam10^2 + ((19021:ℝ)/10000)^2 - 5)) =
      (((19021:ℝ)/10000)^4 - 5*((19021:ℝ)/10000)^2 + 5) - (lam10^4 - 5*lam10^2 + 5) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hpoly, hq]

set_option maxHeartbeats 800000 in
/-- `λ₁₀ < 19022/10000`. -/
lemma lam10_lt : lam10 < (19022 : ℝ) / 10000 := by
  by_contra h
  push_neg at h
  have hq := lam10_quartic
  have hone := lam10_gt_one
  have htwo := lam10_lt_two
  have hfactor : (0:ℝ) < (lam10 + (19022:ℝ)/10000) * (lam10^2 + ((19022:ℝ)/10000)^2 - 5) := by
    nlinarith [hone, htwo, lam10_sq_ge_two, sq_nonneg lam10, sq_nonneg (lam10 - 1)]
  have hdiff : lam10 - (19022:ℝ)/10000 ≥ 0 := by linarith
  have hpoly : (lam10 - (19022:ℝ)/10000) *
      ((lam10 + (19022:ℝ)/10000) * (lam10^2 + ((19022:ℝ)/10000)^2 - 5)) =
      (lam10^4 - 5*lam10^2 + 5) - (((19022:ℝ)/10000)^4 - 5*((19022:ℝ)/10000)^2 + 5) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hq, hpoly]

/-- `X(10) = 1/λ₁₀³`. -/
def X10 : ℝ := 1 / lam10 ^ 3
lemma lam10_cubed_pos : 0 < lam10 ^ 3 := pow_pos lam10_pos 3

def a0₁₀ : ℝ := 1 / 3
def b0₁₀ : ℝ := 3 / 8
def a1₁₀ : ℝ := 3 / 8
def b1₁₀ : ℝ := (3 / 8) * lam10 - 1 / 3
def a2₁₀ : ℝ := (3 / 8) * lam10 - 1 / 3
def b2₁₀ : ℝ := (3 / 8) * lam10 ^ 2 - (1 / 3) * lam10 - 3 / 8

def run10 : ℕ → ℝ × ℝ
  | 0 => (a0₁₀, b0₁₀)
  | 1 => (a1₁₀, b1₁₀)
  | _ => (a2₁₀, b2₁₀)

def lastBranch10 (p : ℝ × ℝ) : Prop := p.1 + lam10 * p.2 > 1

lemma b0₁₀_pos : 0 < b0₁₀ := by unfold b0₁₀; norm_num
lemma b1₁₀_pos : 0 < b1₁₀ := by unfold b1₁₀; nlinarith [lam10_gt]
lemma a2₁₀_pos : 0 < a2₁₀ := by unfold a2₁₀; nlinarith [lam10_gt]
lemma b2₁₀_pos : 0 < b2₁₀ := by unfold b2₁₀; nlinarith [lam10_gt, lam10_lt, sq_nonneg lam10]

lemma P0₁₀_lt : a0₁₀ * b0₁₀ < X10 := by
  unfold a0₁₀ b0₁₀ X10
  rw [lt_div_iff₀ lam10_cubed_pos]
  nlinarith [lam10_gt, lam10_lt, lam10_quartic', sq_nonneg lam10, lam10_pos]

lemma P1₁₀_lt : a1₁₀ * b1₁₀ < X10 := by
  unfold a1₁₀ b1₁₀ X10
  rw [lt_div_iff₀ lam10_cubed_pos]
  nlinarith [lam10_gt, lam10_lt, lam10_quartic', sq_nonneg lam10, lam10_pos]

set_option maxHeartbeats 1200000 in
lemma P2₁₀_lt : a2₁₀ * b2₁₀ < X10 := by
  unfold a2₁₀ b2₁₀ X10
  rw [lt_div_iff₀ lam10_cubed_pos]
  have hP2 : ((3:ℝ)/8 * lam10 - 1/3) * (3/8 * lam10^2 - 1/3*lam10 - 3/8) =
             9/64 * lam10^3 - 1/4 * lam10^2 - 17/576 * lam10 + 1/8 := by ring
  nlinarith [lam10_gt, lam10_lt, lam10_quartic', sq_nonneg lam10, lam10_pos, hP2,
    mul_pos lam10_pos lam10_pos]

lemma branch0₁₀ : lastBranch10 (a0₁₀, b0₁₀) := by
  unfold lastBranch10 a0₁₀ b0₁₀; simp only; nlinarith [lam10_gt]
lemma branch1₁₀ : lastBranch10 (a1₁₀, b1₁₀) := by
  unfold lastBranch10 a1₁₀ b1₁₀; simp only; nlinarith [lam10_gt, lam10_lt, sq_nonneg lam10]
lemma branch2₁₀ : lastBranch10 (a2₁₀, b2₁₀) := by
  unfold lastBranch10 a2₁₀ b2₁₀; simp only
  nlinarith [lam10_gt, lam10_lt, lam10_quartic', sq_nonneg lam10]

lemma bracket0₁₀ : lam10 * b0₁₀ ≤ 1 + a0₁₀ ∧ 1 + a0₁₀ < 2 * (lam10 * b0₁₀) := by
  unfold a0₁₀ b0₁₀
  exact ⟨by nlinarith [lam10_lt], by nlinarith [lam10_gt]⟩

lemma bracket1₁₀ : lam10 * b1₁₀ ≤ 1 + a1₁₀ ∧ 1 + a1₁₀ < 2 * (lam10 * b1₁₀) := by
  unfold a1₁₀ b1₁₀
  exact ⟨by nlinarith [lam10_gt, lam10_lt, sq_nonneg lam10],
         by nlinarith [lam10_gt, lam10_lt, sq_nonneg lam10]⟩

lemma kfloor0₁₀ : kfloor lam10 (a0₁₀, b0₁₀) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam10 a0₁₀ b0₁₀ lam10_pos b0₁₀_pos).mpr bracket0₁₀
lemma kfloor1₁₀ : kfloor lam10 (a1₁₀, b1₁₀) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam10 a1₁₀ b1₁₀ lam10_pos b1₁₀_pos).mpr bracket1₁₀

lemma step0₁₀ : run10 1 = kstep lam10 ((kfloor lam10 (run10 0) : ℝ)) (run10 0) := by
  show (a1₁₀, b1₁₀) = kstep lam10 ((kfloor lam10 (a0₁₀, b0₁₀) : ℝ)) (a0₁₀, b0₁₀)
  rw [kfloor0₁₀]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a1₁₀, b1₁₀) = HeckeRotArc.Mmap lam10 (a0₁₀, b0₁₀)
  refine Prod.ext ?_ ?_
  · show a1₁₀ = b0₁₀; unfold a1₁₀ b0₁₀; norm_num
  · show b1₁₀ = -a0₁₀ + lam10 * b0₁₀; unfold b1₁₀ a0₁₀ b0₁₀; ring

lemma step1₁₀ : run10 2 = kstep lam10 ((kfloor lam10 (run10 1) : ℝ)) (run10 1) := by
  show (a2₁₀, b2₁₀) = kstep lam10 ((kfloor lam10 (a1₁₀, b1₁₀) : ℝ)) (a1₁₀, b1₁₀)
  rw [kfloor1₁₀]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a2₁₀, b2₁₀) = HeckeRotArc.Mmap lam10 (a1₁₀, b1₁₀)
  refine Prod.ext ?_ ?_
  · show a2₁₀ = b1₁₀; unfold a2₁₀ b1₁₀; rfl
  · show b2₁₀ = -a1₁₀ + lam10 * b1₁₀; unfold b2₁₀ a1₁₀ b1₁₀; ring

theorem run10_isClusterRun : IsClusterRun lam10 X10 lastBranch10 run10 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro n hn; interval_cases n
    · exact ⟨P0₁₀_lt, branch0₁₀⟩
    · exact ⟨P1₁₀_lt, branch1₁₀⟩
    · exact ⟨P2₁₀_lt, branch2₁₀⟩
  · intro n hn; interval_cases n
    · exact b0₁₀_pos
    · exact b1₁₀_pos
  · intro n hn; interval_cases n
    · exact step0₁₀
    · exact step1₁₀
  · intro n hn; interval_cases n
    · exact bracket0₁₀
    · exact bracket1₁₀

theorem clusterCeiling10 : clusterCeiling lam10 X10 lastBranch10 2 :=
  ⟨run10, run10_isClusterRun⟩

/-- **★ B(10) = rotation-arc count — R2 closed for q=10.** -/
theorem Bq_eq_rotation_arc_q10 :
    clusterCeiling lam10 X10 lastBranch10 2 ↔ rotationArcCount lam10 X10 lastBranch10 2 :=
  HeckeRotArc.Bq_eq_rotation_arc lam10 lam10_pos X10 lastBranch10 2 (fun _ => clusterCeiling10)

theorem rotationArcCount10_realized : rotationArcCount lam10 X10 lastBranch10 2 :=
  HeckeRotArc.cluster_le_rotation_arc lam10 lam10_pos X10 lastBranch10 2 clusterCeiling10

/-! ## §2.  q = 12 — quartic field `Q(λ₁₂)`, `λ₁₂ = 2cos(π/12)`, minpoly `x⁴ − 4x² + 1`, `B(12) = 3`.

From the double-angle `λ₁₂² = 2 + 2cos(π/6) = 2 + √3` and `cos(π/6) = √3/2`:
`λ₁₂² − 2 = √3` ⟹ `(λ₁₂² − 2)² = 3` ⟹ `λ₁₂⁴ − 4λ₁₂² + 1 = 0`. -/

def lam12 : ℝ := 2 * Real.cos (Real.pi / 12)

lemma lam12_pos : 0 < lam12 := by
  unfold lam12
  apply mul_pos (by norm_num : (0:ℝ) < 2)
  exact Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

/-- `λ₁₂² = 2 + √3`, from `2cos²(π/12) = 1 + cos(π/6)` and `cos(π/6) = √3/2`. -/
lemma lam12_sq : lam12 ^ 2 = 2 + Real.sqrt 3 := by
  unfold lam12
  have hdouble : Real.cos (2 * (Real.pi / 12)) = 2 * Real.cos (Real.pi / 12) ^ 2 - 1 :=
    Real.cos_two_mul _
  have h26 : (2:ℝ) * (Real.pi / 12) = Real.pi / 6 := by ring
  rw [h26, Real.cos_pi_div_six] at hdouble
  nlinarith [hdouble]

/-- The quartic identity `λ₁₂⁴ − 4λ₁₂² + 1 = 0`. -/
lemma lam12_quartic : lam12 ^ 4 - 4 * lam12 ^ 2 + 1 = 0 := by
  have hsq := lam12_sq
  have hr3 : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  have h : (lam12 ^ 2 - 2) = Real.sqrt 3 := by rw [hsq]; ring
  have h2 : (lam12 ^ 2 - 2) ^ 2 = 3 := by rw [h]; exact hr3
  nlinarith [h2]

lemma lam12_quartic' : lam12 ^ 4 = 4 * lam12 ^ 2 - 1 := by linarith [lam12_quartic]

/-- `√2 ≤ λ₁₂` (so `λ₁₂² ≥ 2`), from `cos(π/4) ≤ cos(π/12)`. -/
lemma lam12_ge_sqrt2 : Real.sqrt 2 ≤ lam12 := by
  unfold lam12
  have h_mono : Real.cos (Real.pi / 4) ≤ Real.cos (Real.pi / 12) := by
    apply Real.cos_le_cos_of_nonneg_of_le_pi
    · linarith [Real.pi_pos]
    · linarith [Real.pi_gt_three]
    · apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num : (0:ℝ) < 4)
        (by norm_num : (4:ℝ) ≤ 12)
  have h_cos_pi4 : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 := by rw [Real.cos_pi_div_four]
  rw [h_cos_pi4] at h_mono
  linarith [mul_le_mul_of_nonneg_left h_mono (by norm_num : (0:ℝ) ≤ 2)]

lemma lam12_sq_ge_two : (2:ℝ) ≤ lam12 ^ 2 := by
  have h := lam12_ge_sqrt2
  have hr2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  nlinarith [h, hr2, Real.sqrt_nonneg 2, lam12_pos]

lemma lam12_gt_one : 1 < lam12 := by
  have h := lam12_ge_sqrt2
  have h1 : 1 < Real.sqrt 2 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp [Real.sqrt_one]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith

lemma lam12_sq_lt_four : lam12 ^ 2 < 4 := by
  -- u = λ²; u² − 4u + 1 = 0 and u ≥ 2 ⟹ u < 4 (poly >0 for u ≥ 4)
  have hq := lam12_quartic
  have hge := lam12_sq_ge_two
  nlinarith [hq, hge, sq_nonneg (lam12 ^ 2 - 4), pow_pos lam12_pos 2]

lemma lam12_lt_two : lam12 < 2 := by
  nlinarith [lam12_sq_lt_four, lam12_pos, sq_nonneg (lam12 - 2)]

set_option maxHeartbeats 800000 in
/-- `λ₁₂ > 19318/10000`. -/
lemma lam12_gt : (19318 : ℝ) / 10000 < lam12 := by
  by_contra h
  push_neg at h
  have hq := lam12_quartic
  have hone := lam12_gt_one
  have htwo := lam12_lt_two
  have hfactor : (0:ℝ) < (lam12 + (19318:ℝ)/10000) * (lam12^2 + ((19318:ℝ)/10000)^2 - 4) := by
    nlinarith [hone, htwo, lam12_sq_ge_two, sq_nonneg lam12, sq_nonneg (lam12 - 1)]
  have hdiff : (19318:ℝ)/10000 - lam12 ≥ 0 := by linarith
  have hpoly : ((19318:ℝ)/10000 - lam12) *
      ((lam12 + (19318:ℝ)/10000) * (lam12^2 + ((19318:ℝ)/10000)^2 - 4)) =
      (((19318:ℝ)/10000)^4 - 4*((19318:ℝ)/10000)^2 + 1) - (lam12^4 - 4*lam12^2 + 1) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hq, hpoly]

set_option maxHeartbeats 800000 in
/-- `λ₁₂ < 19319/10000`. -/
lemma lam12_lt : lam12 < (19319 : ℝ) / 10000 := by
  by_contra h
  push_neg at h
  have hq := lam12_quartic
  have hone := lam12_gt_one
  have htwo := lam12_lt_two
  have hfactor : (0:ℝ) < (lam12 + (19319:ℝ)/10000) * (lam12^2 + ((19319:ℝ)/10000)^2 - 4) := by
    nlinarith [hone, htwo, lam12_sq_ge_two, sq_nonneg lam12, sq_nonneg (lam12 - 1)]
  have hdiff : lam12 - (19319:ℝ)/10000 ≥ 0 := by linarith
  have hpoly : (lam12 - (19319:ℝ)/10000) *
      ((lam12 + (19319:ℝ)/10000) * (lam12^2 + ((19319:ℝ)/10000)^2 - 4)) =
      (lam12^4 - 4*lam12^2 + 1) - (((19319:ℝ)/10000)^4 - 4*((19319:ℝ)/10000)^2 + 1) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hq, hpoly]

/-- `X(12) = 1/λ₁₂³`. -/
def X12 : ℝ := 1 / lam12 ^ 3
lemma lam12_cubed_pos : 0 < lam12 ^ 3 := pow_pos lam12_pos 3

def a0₁₂ : ℝ := 1 / 3
def b0₁₂ : ℝ := 11 / 30
def a1₁₂ : ℝ := 11 / 30
def b1₁₂ : ℝ := (11 / 30) * lam12 - 1 / 3
def a2₁₂ : ℝ := (11 / 30) * lam12 - 1 / 3
def b2₁₂ : ℝ := (11 / 30) * lam12 ^ 2 - (1 / 3) * lam12 - 11 / 30

def run12 : ℕ → ℝ × ℝ
  | 0 => (a0₁₂, b0₁₂)
  | 1 => (a1₁₂, b1₁₂)
  | _ => (a2₁₂, b2₁₂)

def lastBranch12 (p : ℝ × ℝ) : Prop := p.1 + lam12 * p.2 > 1

lemma b0₁₂_pos : 0 < b0₁₂ := by unfold b0₁₂; norm_num
lemma b1₁₂_pos : 0 < b1₁₂ := by unfold b1₁₂; nlinarith [lam12_gt]
lemma a2₁₂_pos : 0 < a2₁₂ := by unfold a2₁₂; nlinarith [lam12_gt]
lemma b2₁₂_pos : 0 < b2₁₂ := by unfold b2₁₂; nlinarith [lam12_gt, lam12_lt, sq_nonneg lam12]

lemma P0₁₂_lt : a0₁₂ * b0₁₂ < X12 := by
  unfold a0₁₂ b0₁₂ X12
  rw [lt_div_iff₀ lam12_cubed_pos]
  nlinarith [lam12_gt, lam12_lt, lam12_quartic', sq_nonneg lam12, lam12_pos]

lemma P1₁₂_lt : a1₁₂ * b1₁₂ < X12 := by
  unfold a1₁₂ b1₁₂ X12
  rw [lt_div_iff₀ lam12_cubed_pos]
  nlinarith [lam12_gt, lam12_lt, lam12_quartic', sq_nonneg lam12, lam12_pos]

set_option maxHeartbeats 1200000 in
lemma P2₁₂_lt : a2₁₂ * b2₁₂ < X12 := by
  unfold a2₁₂ b2₁₂ X12
  rw [lt_div_iff₀ lam12_cubed_pos]
  have hP2 : ((11:ℝ)/30 * lam12 - 1/3) * (11/30 * lam12^2 - 1/3*lam12 - 11/30) =
             121/900 * lam12^3 - 11/45 * lam12^2 - 7/300 * lam12 + 11/90 := by ring
  nlinarith [lam12_gt, lam12_lt, lam12_quartic', sq_nonneg lam12, lam12_pos, hP2,
    mul_pos lam12_pos lam12_pos]

lemma branch0₁₂ : lastBranch12 (a0₁₂, b0₁₂) := by
  unfold lastBranch12 a0₁₂ b0₁₂; simp only; nlinarith [lam12_gt]
lemma branch1₁₂ : lastBranch12 (a1₁₂, b1₁₂) := by
  unfold lastBranch12 a1₁₂ b1₁₂; simp only; nlinarith [lam12_gt, lam12_lt, sq_nonneg lam12]
lemma branch2₁₂ : lastBranch12 (a2₁₂, b2₁₂) := by
  unfold lastBranch12 a2₁₂ b2₁₂; simp only
  nlinarith [lam12_gt, lam12_lt, lam12_quartic', sq_nonneg lam12]

lemma bracket0₁₂ : lam12 * b0₁₂ ≤ 1 + a0₁₂ ∧ 1 + a0₁₂ < 2 * (lam12 * b0₁₂) := by
  unfold a0₁₂ b0₁₂
  exact ⟨by nlinarith [lam12_lt], by nlinarith [lam12_gt]⟩

lemma bracket1₁₂ : lam12 * b1₁₂ ≤ 1 + a1₁₂ ∧ 1 + a1₁₂ < 2 * (lam12 * b1₁₂) := by
  unfold a1₁₂ b1₁₂
  exact ⟨by nlinarith [lam12_gt, lam12_lt, sq_nonneg lam12],
         by nlinarith [lam12_gt, lam12_lt, sq_nonneg lam12]⟩

lemma kfloor0₁₂ : kfloor lam12 (a0₁₂, b0₁₂) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam12 a0₁₂ b0₁₂ lam12_pos b0₁₂_pos).mpr bracket0₁₂
lemma kfloor1₁₂ : kfloor lam12 (a1₁₂, b1₁₂) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam12 a1₁₂ b1₁₂ lam12_pos b1₁₂_pos).mpr bracket1₁₂

lemma step0₁₂ : run12 1 = kstep lam12 ((kfloor lam12 (run12 0) : ℝ)) (run12 0) := by
  show (a1₁₂, b1₁₂) = kstep lam12 ((kfloor lam12 (a0₁₂, b0₁₂) : ℝ)) (a0₁₂, b0₁₂)
  rw [kfloor0₁₂]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a1₁₂, b1₁₂) = HeckeRotArc.Mmap lam12 (a0₁₂, b0₁₂)
  refine Prod.ext ?_ ?_
  · show a1₁₂ = b0₁₂; unfold a1₁₂ b0₁₂; norm_num
  · show b1₁₂ = -a0₁₂ + lam12 * b0₁₂; unfold b1₁₂ a0₁₂ b0₁₂; ring

lemma step1₁₂ : run12 2 = kstep lam12 ((kfloor lam12 (run12 1) : ℝ)) (run12 1) := by
  show (a2₁₂, b2₁₂) = kstep lam12 ((kfloor lam12 (a1₁₂, b1₁₂) : ℝ)) (a1₁₂, b1₁₂)
  rw [kfloor1₁₂]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a2₁₂, b2₁₂) = HeckeRotArc.Mmap lam12 (a1₁₂, b1₁₂)
  refine Prod.ext ?_ ?_
  · show a2₁₂ = b1₁₂; unfold a2₁₂ b1₁₂; rfl
  · show b2₁₂ = -a1₁₂ + lam12 * b1₁₂; unfold b2₁₂ a1₁₂ b1₁₂; ring

theorem run12_isClusterRun : IsClusterRun lam12 X12 lastBranch12 run12 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro n hn; interval_cases n
    · exact ⟨P0₁₂_lt, branch0₁₂⟩
    · exact ⟨P1₁₂_lt, branch1₁₂⟩
    · exact ⟨P2₁₂_lt, branch2₁₂⟩
  · intro n hn; interval_cases n
    · exact b0₁₂_pos
    · exact b1₁₂_pos
  · intro n hn; interval_cases n
    · exact step0₁₂
    · exact step1₁₂
  · intro n hn; interval_cases n
    · exact bracket0₁₂
    · exact bracket1₁₂

theorem clusterCeiling12 : clusterCeiling lam12 X12 lastBranch12 2 :=
  ⟨run12, run12_isClusterRun⟩

/-- **★ B(12) = rotation-arc count — R2 closed for q=12.** -/
theorem Bq_eq_rotation_arc_q12 :
    clusterCeiling lam12 X12 lastBranch12 2 ↔ rotationArcCount lam12 X12 lastBranch12 2 :=
  HeckeRotArc.Bq_eq_rotation_arc lam12 lam12_pos X12 lastBranch12 2 (fun _ => clusterCeiling12)

theorem rotationArcCount12_realized : rotationArcCount lam12 X12 lastBranch12 2 :=
  HeckeRotArc.cluster_le_rotation_arc lam12 lam12_pos X12 lastBranch12 2 clusterCeiling12

/-! ## §3.  q = 13 — degree-6 field `Q(λ₁₃)`, `λ₁₃ = 2cos(π/13)`, **`B(13) = 4` — the FIRST length-4
rotation arc** (the `3 → 4` cluster-ceiling transition).

`minpoly(λ₁₃) = x⁶ − x⁵ − 5x⁴ + 4x³ + 6x² − 3x − 1` (degree `φ(26)/2 = 6`).  We obtain it from the
Chebyshev identity `T₁₃(cos θ) = cos(13θ)`: at `θ = π/13`, `cos(13·π/13) = cos π = −1`, so
`T₁₃(c) = −1` with `c = cos(π/13)`.  Substituting `λ = 2c` into the explicit degree-13 expansion of
`T₁₃` gives the exact factorization `(λ+2)·minpoly(λ)² = 2·(T₁₃(λ/2)+1) = 0`; since `λ+2 > 0`, the
minimal polynomial vanishes.

The realization arc has length `N+1 = 4` (start `(31/94, 17/47)`, interior `k = 1`), exhibiting the
first non-`{8,9,10,11,12}` ceiling value `B(13) = 4` of the ladder. -/

open Polynomial Polynomial.Chebyshev in
/-- Chebyshev `T`-recurrence specialized to real evaluation: `T_{n+2}(c) = 2c·T_{n+1}(c) − T_n(c)`. -/
theorem T_real_rec (c : ℝ) (n : ℕ) :
    (T ℝ ((n:ℤ)+2)).eval c = 2*c*(T ℝ ((n:ℤ)+1)).eval c - (T ℝ (n:ℤ)).eval c := by
  rw [Polynomial.Chebyshev.T_add_two ℝ (n : ℤ)]
  simp only [eval_mul, eval_sub, eval_X, eval_ofNat]

open Polynomial Polynomial.Chebyshev in
/-- The explicit degree-13 Chebyshev polynomial `T₁₃` evaluated at a real `c`. -/
theorem T13_eval (c : ℝ) : (T ℝ 13).eval c =
    4096*c^13 - 13312*c^11 + 16640*c^9 - 9984*c^7 + 2912*c^5 - 364*c^3 + 13*c := by
  have e2 : (T ℝ (2:ℤ)).eval c = 2*c^2 - 1 := by
    have := T_real_rec c 0; norm_num at this; rw [this]; ring
  have e3 : (T ℝ (3:ℤ)).eval c = 4*c^3 - 3*c := by
    have := T_real_rec c 1; norm_num at this; rw [this, e2]; ring
  have e4 : (T ℝ (4:ℤ)).eval c = 8*c^4 - 8*c^2 + 1 := by
    have := T_real_rec c 2; norm_num at this; rw [this, e2, e3]; ring
  have e5 : (T ℝ (5:ℤ)).eval c = 16*c^5 - 20*c^3 + 5*c := by
    have := T_real_rec c 3; norm_num at this; rw [this, e3, e4]; ring
  have e6 : (T ℝ (6:ℤ)).eval c = 32*c^6 - 48*c^4 + 18*c^2 - 1 := by
    have := T_real_rec c 4; norm_num at this; rw [this, e4, e5]; ring
  have e7 : (T ℝ (7:ℤ)).eval c = 64*c^7 - 112*c^5 + 56*c^3 - 7*c := by
    have := T_real_rec c 5; norm_num at this; rw [this, e5, e6]; ring
  have e8 : (T ℝ (8:ℤ)).eval c = 128*c^8 - 256*c^6 + 160*c^4 - 32*c^2 + 1 := by
    have := T_real_rec c 6; norm_num at this; rw [this, e6, e7]; ring
  have e9 : (T ℝ (9:ℤ)).eval c = 256*c^9 - 576*c^7 + 432*c^5 - 120*c^3 + 9*c := by
    have := T_real_rec c 7; norm_num at this; rw [this, e7, e8]; ring
  have e10 : (T ℝ (10:ℤ)).eval c = 512*c^10 - 1280*c^8 + 1120*c^6 - 400*c^4 + 50*c^2 - 1 := by
    have := T_real_rec c 8; norm_num at this; rw [this, e8, e9]; ring
  have e11 : (T ℝ (11:ℤ)).eval c = 1024*c^11 - 2816*c^9 + 2816*c^7 - 1232*c^5 + 220*c^3 - 11*c := by
    have := T_real_rec c 9; norm_num at this; rw [this, e9, e10]; ring
  have e12 : (T ℝ (12:ℤ)).eval c =
      2048*c^12 - 6144*c^10 + 6912*c^8 - 3584*c^6 + 840*c^4 - 72*c^2 + 1 := by
    have := T_real_rec c 10; norm_num at this; rw [this, e10, e11]; ring
  have e13 : (T ℝ (13:ℤ)).eval c =
      4096*c^13 - 13312*c^11 + 16640*c^9 - 9984*c^7 + 2912*c^5 - 364*c^3 + 13*c := by
    have := T_real_rec c 11; norm_num at this; rw [this, e11, e12]; ring
  exact e13

def lam13 : ℝ := 2 * Real.cos (Real.pi / 13)

lemma lam13_pos : 0 < lam13 := by
  unfold lam13
  apply mul_pos (by norm_num : (0:ℝ) < 2)
  exact Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

set_option maxHeartbeats 800000 in
/-- The degree-6 minimal-polynomial identity for `λ₁₃ = 2cos(π/13)`, via Chebyshev `T₁₃(c) = −1`
and the factorization `(λ+2)·minpoly² = 2·(T₁₃(λ/2)+1)`. -/
lemma lam13_minpoly :
    lam13^6 - lam13^5 - 5*lam13^4 + 4*lam13^3 + 6*lam13^2 - 3*lam13 - 1 = 0 := by
  set c := Real.cos (Real.pi / 13) with hc
  have hT : (Polynomial.Chebyshev.T ℝ 13).eval c = -1 := by
    rw [hc, Polynomial.Chebyshev.T_real_cos]
    rw [show (13:ℤ) * (Real.pi/13) = Real.pi by push_cast; ring]
    exact Real.cos_pi
  rw [T13_eval] at hT
  have hlam : lam13 = 2 * c := by rw [hc]; rfl
  have hpos : (0:ℝ) < lam13 + 2 := by have := lam13_pos; linarith
  have hfactored : (lam13 + 2) *
      (lam13^6 - lam13^5 - 5*lam13^4 + 4*lam13^3 + 6*lam13^2 - 3*lam13 - 1)^2 = 0 := by
    rw [hlam]; linear_combination 2 * hT
  have hsq : (lam13^6 - lam13^5 - 5*lam13^4 + 4*lam13^3 + 6*lam13^2 - 3*lam13 - 1)^2 = 0 := by
    rcases mul_eq_zero.mp hfactored with h | h
    · linarith
    · exact h
  exact pow_eq_zero_iff (by norm_num) |>.mp hsq

/-- Power-reduction normal form `λ₁₃⁶ = λ₁₃⁵ + 5λ₁₃⁴ − 4λ₁₃³ − 6λ₁₃² + 3λ₁₃ + 1`. -/
lemma lam13_minpoly' :
    lam13^6 = lam13^5 + 5*lam13^4 - 4*lam13^3 - 6*lam13^2 + 3*lam13 + 1 := by
  linarith [lam13_minpoly]

/-- `√2 ≤ λ₁₃`, from `cos(π/4) ≤ cos(π/13)`. -/
lemma lam13_ge_sqrt2 : Real.sqrt 2 ≤ lam13 := by
  unfold lam13
  have h_mono : Real.cos (Real.pi / 4) ≤ Real.cos (Real.pi / 13) := by
    apply Real.cos_le_cos_of_nonneg_of_le_pi
    · linarith [Real.pi_pos]
    · linarith [Real.pi_gt_three]
    · apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num : (0:ℝ) < 4)
        (by norm_num : (4:ℝ) ≤ 13)
  have h_cos_pi4 : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 := by rw [Real.cos_pi_div_four]
  rw [h_cos_pi4] at h_mono
  linarith [mul_le_mul_of_nonneg_left h_mono (by norm_num : (0:ℝ) ≤ 2)]

lemma lam13_gt_one : 1 < lam13 := by
  have h := lam13_ge_sqrt2
  have h1 : 1 < Real.sqrt 2 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp [Real.sqrt_one]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith

lemma lam13_lt_two : lam13 < 2 := by
  unfold lam13
  have hcos : Real.cos (Real.pi / 13) < 1 := by
    have h := Real.cos_lt_cos_of_nonneg_of_le_pi (le_refl (0:ℝ))
      (by linarith [Real.pi_pos] : Real.pi / 13 ≤ Real.pi)
      (by positivity : (0:ℝ) < Real.pi / 13)
    rwa [Real.cos_zero] at h
  linarith

/-- Crude lower bound `λ₁₃ ≥ λ₁₀ > 1.9`, from `cos(π/13) ≥ cos(π/10)` (π/13 < π/10).  Used to pin
the larger minpoly root for the tight rational bounds below. -/
lemma lam13_ge_lam10 : lam10 ≤ lam13 := by
  unfold lam10 lam13
  have h_mono : Real.cos (Real.pi / 10) ≤ Real.cos (Real.pi / 13) := by
    apply Real.cos_le_cos_of_nonneg_of_le_pi
    · positivity
    · linarith [Real.pi_pos]
    · apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num : (0:ℝ) < 10)
        (by norm_num : (10:ℝ) ≤ 13)
  linarith [mul_le_mul_of_nonneg_left h_mono (by norm_num : (0:ℝ) ≤ 2)]

lemma lam13_ge_crude : (1897 : ℝ) / 1000 ≤ lam13 :=
  le_trans (by linarith [lam10_gt]) lam13_ge_lam10

set_option maxHeartbeats 1600000 in
/-- `λ₁₃ > 19418/10000`  (degree-6 minpoly + the larger-root pin `λ₁₃ ≥ 1.897`). -/
lemma lam13_gt : (19418 : ℝ) / 10000 < lam13 := by
  by_contra h
  push_neg at h
  have hmp := lam13_minpoly
  have hge := lam13_ge_crude
  have htwo := lam13_lt_two
  nlinarith [hmp, hge, htwo, h, sq_nonneg lam13, pow_pos lam13_pos 2, pow_pos lam13_pos 3,
    pow_pos lam13_pos 4, pow_pos lam13_pos 5,
    mul_nonneg (by linarith : (0:ℝ) ≤ lam13 - (1897:ℝ)/1000)
      (by linarith : (0:ℝ) ≤ (19418:ℝ)/10000 - lam13)]

set_option maxHeartbeats 1600000 in
/-- `λ₁₃ < 19419/10000`. -/
lemma lam13_lt : lam13 < (19419 : ℝ) / 10000 := by
  by_contra h
  push_neg at h
  have hmp := lam13_minpoly
  have hge := lam13_ge_crude
  have htwo := lam13_lt_two
  nlinarith [hmp, hge, htwo, h, sq_nonneg lam13, pow_pos lam13_pos 2, pow_pos lam13_pos 3,
    pow_pos lam13_pos 4, pow_pos lam13_pos 5,
    mul_nonneg (by linarith : (0:ℝ) ≤ lam13 - (19419:ℝ)/10000)
      (by linarith : (0:ℝ) ≤ (2:ℝ) - lam13),
    mul_nonneg (by linarith : (0:ℝ) ≤ lam13 - (19419:ℝ)/10000)
      (by linarith : (0:ℝ) ≤ lam13 - (1897:ℝ)/1000)]

/-- `X(13) = 1/λ₁₃³`. -/
def X13 : ℝ := 1 / lam13 ^ 3
lemma lam13_cubed_pos : 0 < lam13 ^ 3 := pow_pos lam13_pos 3

def a0₁₃ : ℝ := 31 / 94
def b0₁₃ : ℝ := 17 / 47
def a1₁₃ : ℝ := 17 / 47
def b1₁₃ : ℝ := (17 / 47) * lam13 - 31 / 94
def a2₁₃ : ℝ := (17 / 47) * lam13 - 31 / 94
def b2₁₃ : ℝ := (17 / 47) * lam13 ^ 2 - (31 / 94) * lam13 - 17 / 47
def a3₁₃ : ℝ := (17 / 47) * lam13 ^ 2 - (31 / 94) * lam13 - 17 / 47
def b3₁₃ : ℝ := (17 / 47) * lam13 ^ 3 - (31 / 94) * lam13 ^ 2 - (34 / 47) * lam13 + 31 / 94

def run13 : ℕ → ℝ × ℝ
  | 0 => (a0₁₃, b0₁₃)
  | 1 => (a1₁₃, b1₁₃)
  | 2 => (a2₁₃, b2₁₃)
  | _ => (a3₁₃, b3₁₃)

def lastBranch13 (p : ℝ × ℝ) : Prop := p.1 + lam13 * p.2 > 1

lemma b0₁₃_pos : 0 < b0₁₃ := by unfold b0₁₃; norm_num
lemma b1₁₃_pos : 0 < b1₁₃ := by unfold b1₁₃; nlinarith [lam13_gt]
lemma b2₁₃_pos : 0 < b2₁₃ := by unfold b2₁₃; nlinarith [lam13_gt, lam13_lt, sq_nonneg lam13]
lemma b3₁₃_pos : 0 < b3₁₃ := by
  unfold b3₁₃
  nlinarith [lam13_gt, lam13_lt, sq_nonneg lam13, pow_pos lam13_pos 2, pow_pos lam13_pos 3,
    mul_pos lam13_pos lam13_pos]

set_option maxHeartbeats 800000 in
lemma P0₁₃_lt : a0₁₃ * b0₁₃ < X13 := by
  unfold a0₁₃ b0₁₃ X13
  rw [lt_div_iff₀ lam13_cubed_pos]
  nlinarith [lam13_gt, lam13_lt, lam13_minpoly', sq_nonneg lam13, lam13_pos,
    pow_pos lam13_pos 2, pow_pos lam13_pos 3]

set_option maxHeartbeats 1200000 in
lemma P1₁₃_lt : a1₁₃ * b1₁₃ < X13 := by
  unfold a1₁₃ b1₁₃ X13
  rw [lt_div_iff₀ lam13_cubed_pos]
  -- a1*b1*λ³ is degree 4: = 289/2209·λ⁴ − 527/4418·λ³
  have hP1 : ((17:ℝ)/47) * ((17:ℝ)/47 * lam13 - 31/94) * lam13 ^ 3 =
             289/2209 * lam13^4 - 527/4418 * lam13^3 := by ring
  rw [hP1]
  nlinarith [lam13_gt, lam13_lt, lam13_minpoly', sq_nonneg lam13, lam13_pos,
    pow_pos lam13_pos 2, pow_pos lam13_pos 3, pow_pos lam13_pos 4]

set_option maxHeartbeats 2000000 in
lemma P2₁₃_lt : a2₁₃ * b2₁₃ < X13 := by
  unfold a2₁₃ b2₁₃ X13
  rw [lt_div_iff₀ lam13_cubed_pos]
  -- reduce (a2*b2)*λ³ mod minpoly to degree ≤ 5
  have hP2 : ((17:ℝ)/47 * lam13 - 31/94) *
      ((17:ℝ)/47 * lam13^2 - 31/94 * lam13 - 17/47) * lam13 ^ 3 =
      (-238/2209 * lam13^5 + 5585/8836 * lam13^4 - 1785/4418 * lam13^3
        - 1734/2209 * lam13^2 + 867/2209 * lam13 + 289/2209)
      + (289/2209) * (lam13^6 - lam13^5 - 5*lam13^4 + 4*lam13^3 + 6*lam13^2 - 3*lam13 - 1) := by
    ring
  rw [hP2, lam13_minpoly]
  nlinarith [lam13_gt, lam13_lt, lam13_minpoly', sq_nonneg lam13, lam13_pos,
    pow_pos lam13_pos 2, pow_pos lam13_pos 3, pow_pos lam13_pos 4, pow_pos lam13_pos 5,
    mul_pos lam13_pos lam13_pos]

set_option maxHeartbeats 2000000 in
lemma P3₁₃_lt : a3₁₃ * b3₁₃ < X13 := by
  unfold a3₁₃ b3₁₃ X13
  rw [lt_div_iff₀ lam13_cubed_pos]
  have hP3 : ((17:ℝ)/47 * lam13^2 - 31/94 * lam13 - 17/47) *
      ((17:ℝ)/47 * lam13^3 - 31/94 * lam13^2 - 34/47 * lam13 + 31/94) * lam13 ^ 3 =
      (-2847/8836 * lam13^5 + 2457/2209 * lam13^4 - 579/4418 * lam13^3
        - 7813/4418 * lam13^2 + 6011/8836 * lam13 + 2321/8836)
      + (289/2209 * lam13^2 - 238/2209 * lam13 + 2321/8836) *
        (lam13^6 - lam13^5 - 5*lam13^4 + 4*lam13^3 + 6*lam13^2 - 3*lam13 - 1) := by
    ring
  rw [hP3, lam13_minpoly]
  nlinarith [lam13_gt, lam13_lt, lam13_minpoly', sq_nonneg lam13, lam13_pos,
    pow_pos lam13_pos 2, pow_pos lam13_pos 3, pow_pos lam13_pos 4, pow_pos lam13_pos 5,
    mul_pos lam13_pos lam13_pos]

lemma branch0₁₃ : lastBranch13 (a0₁₃, b0₁₃) := by
  unfold lastBranch13 a0₁₃ b0₁₃; simp only; nlinarith [lam13_gt]
lemma branch1₁₃ : lastBranch13 (a1₁₃, b1₁₃) := by
  unfold lastBranch13 a1₁₃ b1₁₃; simp only; nlinarith [lam13_gt, lam13_lt, sq_nonneg lam13]
lemma branch2₁₃ : lastBranch13 (a2₁₃, b2₁₃) := by
  unfold lastBranch13 a2₁₃ b2₁₃; simp only
  nlinarith [lam13_gt, lam13_lt, lam13_minpoly', sq_nonneg lam13]
lemma branch3₁₃ : lastBranch13 (a3₁₃, b3₁₃) := by
  unfold lastBranch13 a3₁₃ b3₁₃; simp only
  nlinarith [lam13_gt, lam13_lt, lam13_minpoly', sq_nonneg lam13, pow_pos lam13_pos 2,
    pow_pos lam13_pos 3]

lemma bracket0₁₃ : lam13 * b0₁₃ ≤ 1 + a0₁₃ ∧ 1 + a0₁₃ < 2 * (lam13 * b0₁₃) := by
  unfold a0₁₃ b0₁₃
  exact ⟨by nlinarith [lam13_lt], by nlinarith [lam13_gt]⟩

lemma bracket1₁₃ : lam13 * b1₁₃ ≤ 1 + a1₁₃ ∧ 1 + a1₁₃ < 2 * (lam13 * b1₁₃) := by
  unfold a1₁₃ b1₁₃
  exact ⟨by nlinarith [lam13_gt, lam13_lt, sq_nonneg lam13],
         by nlinarith [lam13_gt, lam13_lt, sq_nonneg lam13]⟩

lemma bracket2₁₃ : lam13 * b2₁₃ ≤ 1 + a2₁₃ ∧ 1 + a2₁₃ < 2 * (lam13 * b2₁₃) := by
  unfold a2₁₃ b2₁₃
  exact ⟨by nlinarith [lam13_gt, lam13_lt, lam13_minpoly', sq_nonneg lam13, pow_pos lam13_pos 2,
              pow_pos lam13_pos 3],
         by nlinarith [lam13_gt, lam13_lt, lam13_minpoly', sq_nonneg lam13, pow_pos lam13_pos 2,
              pow_pos lam13_pos 3]⟩

lemma kfloor0₁₃ : kfloor lam13 (a0₁₃, b0₁₃) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam13 a0₁₃ b0₁₃ lam13_pos b0₁₃_pos).mpr bracket0₁₃
lemma kfloor1₁₃ : kfloor lam13 (a1₁₃, b1₁₃) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam13 a1₁₃ b1₁₃ lam13_pos b1₁₃_pos).mpr bracket1₁₃
lemma kfloor2₁₃ : kfloor lam13 (a2₁₃, b2₁₃) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam13 a2₁₃ b2₁₃ lam13_pos b2₁₃_pos).mpr bracket2₁₃

lemma step0₁₃ : run13 1 = kstep lam13 ((kfloor lam13 (run13 0) : ℝ)) (run13 0) := by
  show (a1₁₃, b1₁₃) = kstep lam13 ((kfloor lam13 (a0₁₃, b0₁₃) : ℝ)) (a0₁₃, b0₁₃)
  rw [kfloor0₁₃]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a1₁₃, b1₁₃) = HeckeRotArc.Mmap lam13 (a0₁₃, b0₁₃)
  refine Prod.ext ?_ ?_
  · show a1₁₃ = b0₁₃; unfold a1₁₃ b0₁₃; norm_num
  · show b1₁₃ = -a0₁₃ + lam13 * b0₁₃; unfold b1₁₃ a0₁₃ b0₁₃; ring

lemma step1₁₃ : run13 2 = kstep lam13 ((kfloor lam13 (run13 1) : ℝ)) (run13 1) := by
  show (a2₁₃, b2₁₃) = kstep lam13 ((kfloor lam13 (a1₁₃, b1₁₃) : ℝ)) (a1₁₃, b1₁₃)
  rw [kfloor1₁₃]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a2₁₃, b2₁₃) = HeckeRotArc.Mmap lam13 (a1₁₃, b1₁₃)
  refine Prod.ext ?_ ?_
  · show a2₁₃ = b1₁₃; unfold a2₁₃ b1₁₃; rfl
  · show b2₁₃ = -a1₁₃ + lam13 * b1₁₃; unfold b2₁₃ a1₁₃ b1₁₃; ring

lemma step2₁₃ : run13 3 = kstep lam13 ((kfloor lam13 (run13 2) : ℝ)) (run13 2) := by
  show (a3₁₃, b3₁₃) = kstep lam13 ((kfloor lam13 (a2₁₃, b2₁₃) : ℝ)) (a2₁₃, b2₁₃)
  rw [kfloor2₁₃]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a3₁₃, b3₁₃) = HeckeRotArc.Mmap lam13 (a2₁₃, b2₁₃)
  refine Prod.ext ?_ ?_
  · show a3₁₃ = b2₁₃; unfold a3₁₃ b2₁₃; rfl
  · show b3₁₃ = -a2₁₃ + lam13 * b2₁₃; unfold b3₁₃ a2₁₃ b2₁₃; ring

theorem run13_isClusterRun : IsClusterRun lam13 X13 lastBranch13 run13 3 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro n hn; interval_cases n
    · exact ⟨P0₁₃_lt, branch0₁₃⟩
    · exact ⟨P1₁₃_lt, branch1₁₃⟩
    · exact ⟨P2₁₃_lt, branch2₁₃⟩
    · exact ⟨P3₁₃_lt, branch3₁₃⟩
  · intro n hn; interval_cases n
    · exact b0₁₃_pos
    · exact b1₁₃_pos
    · exact b2₁₃_pos
  · intro n hn; interval_cases n
    · exact step0₁₃
    · exact step1₁₃
    · exact step2₁₃
  · intro n hn; interval_cases n
    · exact bracket0₁₃
    · exact bracket1₁₃
    · exact bracket2₁₃

theorem clusterCeiling13 : clusterCeiling lam13 X13 lastBranch13 3 :=
  ⟨run13, run13_isClusterRun⟩

/-- **★ B(13) = rotation-arc count — R2 closed for q=13, the FIRST length-4 arc.** -/
theorem Bq_eq_rotation_arc_q13 :
    clusterCeiling lam13 X13 lastBranch13 3 ↔ rotationArcCount lam13 X13 lastBranch13 3 :=
  HeckeRotArc.Bq_eq_rotation_arc lam13 lam13_pos X13 lastBranch13 3 (fun _ => clusterCeiling13)

theorem rotationArcCount13_realized : rotationArcCount lam13 X13 lastBranch13 3 :=
  HeckeRotArc.cluster_le_rotation_arc lam13 lam13_pos X13 lastBranch13 3 clusterCeiling13

end

-- ════════════ AXIOM AUDIT (q=10, q=12, q=13) ════════════
#print axioms HeckeRotArcR2hi2.run10_isClusterRun
#print axioms HeckeRotArcR2hi2.Bq_eq_rotation_arc_q10
#print axioms HeckeRotArcR2hi2.rotationArcCount10_realized
#print axioms HeckeRotArcR2hi2.run12_isClusterRun
#print axioms HeckeRotArcR2hi2.Bq_eq_rotation_arc_q12
#print axioms HeckeRotArcR2hi2.rotationArcCount12_realized
#print axioms HeckeRotArcR2hi2.lam13_minpoly
#print axioms HeckeRotArcR2hi2.run13_isClusterRun
#print axioms HeckeRotArcR2hi2.Bq_eq_rotation_arc_q13
#print axioms HeckeRotArcR2hi2.rotationArcCount13_realized

end HeckeRotArcR2hi2
