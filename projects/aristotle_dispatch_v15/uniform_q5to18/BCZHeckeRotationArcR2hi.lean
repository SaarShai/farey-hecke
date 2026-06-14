import BCZHeckeRotationArc
set_option maxHeartbeats 1600000
/-!
# `BCZHeckeRotationArcR2hi.lean` — extending the R2 realization ladder `q = 8, 9, …` (and up).

A **new, self-contained** companion to `BCZHeckeRotationArc.lean` (`namespace HeckeRotArc`), which
it `import`s.  It touches NO sealed/verified file (`BCZHeckeRotationArc`, `…R1`, `…R2`, `…R3Parity`
are all left untouched).  It continues the per-`q` realization of residual **R2** — supplying the
`hrealize` bridge of `HeckeRotArc.Bq_eq_rotation_arc` by exhibiting an actual genuine sub-threshold
last-branch cluster run achieving the rotation-arc count — for `q` beyond the `q=7` clean `M`-arc of
`BCZHeckeRotationArcR2.lean`.

The realization body is **identical per q** to the `q=7` pattern of `…R2.lean`; the only growing
cost is the per-`q` minimal-polynomial identity for `λ_q = 2cos(π/q)`.  We DO NOT express the
threshold `X(q) = 1/λ_q³` as a field polynomial (the `q=7` file did, via the cubic) — instead we
keep `Xq := 1/λ_q³` directly and prove the sub-threshold inequalities `P < 1/λ³` by clearing the
positive denominator `λ³`, which only needs the minpoly to reduce high powers plus a tight rational
two-sided bound on `λ_q`.

Exact witnesses: `code/out/goal1_qladder_witness_exact.json` (q=8..16),
`…goal1_qladder_hi_witness_exact.json` (q=17..24), all interior `k=1`.

| q  | minpoly of `λ_q = 2cos(π/q)` | deg | start (over ℚ)  | realized `N+1 = B(q)` |
|----|------------------------------|-----|-----------------|-----------------------|
| 8  | `x⁴ − 4x² + 2`               | 4   | `(1/3, 13/33)`  | 3                     |
| 9  | `x³ − 3x − 1`                | 3   | `(1/3, 8/21)`   | 3                     |

`#print axioms` on every `Bq_eq_rotation_arc_q{q}` below is `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeRotArcR2hi

open HeckeRotArc

noncomputable section

/-! ## §1.  q = 9 — cubic field `Q(λ₉)`, `λ₉ = 2cos(π/9)`, minpoly `x³ − 3x − 1`, `B(9) = 3`.

From `cos(3·π/9) = cos(π/3) = 1/2` and the triple-angle `cos 3θ = 4cos³θ − 3cosθ`:
`4c³ − 3c = 1/2` (`c = cos π/9`) ⟹ `8c³ − 6c − 1 = 0` ⟹ `λ³ − 3λ − 1 = 0` for `λ = 2c`. -/

def lam9 : ℝ := 2 * Real.cos (Real.pi / 9)

lemma lam9_pos : 0 < lam9 := by
  unfold lam9
  apply mul_pos (by norm_num : (0:ℝ) < 2)
  exact Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

/-- The cubic identity `λ₉³ − 3λ₉ − 1 = 0`. -/
lemma lam9_cubic : lam9 ^ 3 - 3 * lam9 - 1 = 0 := by
  unfold lam9
  set c := Real.cos (Real.pi / 9) with hc_def
  set θ := Real.pi / 9 with hθ_def
  have h3θ : (3:ℝ) * θ = Real.pi / 3 := by rw [hθ_def]; ring
  have hcos3 : Real.cos (3 * θ) = 4 * c ^ 3 - 3 * c := by
    rw [show (3 : ℝ) * θ = θ + (θ + θ) by ring, Real.cos_add,
        show θ + θ = 2 * θ by ring, Real.cos_two_mul, Real.sin_two_mul]
    linear_combination (-2 * c) * Real.sin_sq_add_cos_sq θ
  have hval : Real.cos (3 * θ) = 1 / 2 := by rw [h3θ, Real.cos_pi_div_three]
  have h : 4 * c ^ 3 - 3 * c = 1 / 2 := by rw [← hcos3, hval]
  linear_combination (2 : ℝ) * h

lemma lam9_cubic' : lam9 ^ 3 = 3 * lam9 + 1 := by linarith [lam9_cubic]

lemma lam9_gt_one : 1 < lam9 := by
  unfold lam9
  have h_mono : Real.cos (Real.pi / 4) ≤ Real.cos (Real.pi / 9) := by
    apply Real.cos_le_cos_of_nonneg_of_le_pi
    · linarith [Real.pi_pos]
    · linarith [Real.pi_gt_three]
    · apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num : (0:ℝ) < 4)
        (by norm_num : (4:ℝ) ≤ 9)
  have h_cos_pi4 : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 := by rw [Real.cos_pi_div_four]
  rw [h_cos_pi4] at h_mono
  have h_sqrt2 : 1 < Real.sqrt 2 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp [Real.sqrt_one]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith [mul_le_mul_of_nonneg_left h_mono (by norm_num : (0:ℝ) ≤ 2)]

set_option maxHeartbeats 800000 in
/-- `λ₉ > 18793/10000`  (cubic + monotone of `f(x)=x³−3x−1`). -/
lemma lam9_gt : (18793 : ℝ) / 10000 < lam9 := by
  by_contra h
  push_neg at h
  have hcub := lam9_cubic
  have hone := lam9_gt_one
  have hfactor : (0:ℝ) < (18793:ℝ)/10000 * ((18793:ℝ)/10000) +
      (18793:ℝ)/10000 * lam9 + lam9^2 - 3 := by
    nlinarith [sq_nonneg lam9, hone, sq_nonneg (lam9 - 1)]
  have hdiff : (18793:ℝ)/10000 - lam9 ≥ 0 := by linarith
  have hpoly : ((18793:ℝ)/10000 - lam9) * ((18793:ℝ)/10000 * ((18793:ℝ)/10000) +
      (18793:ℝ)/10000 * lam9 + lam9^2 - 3) =
      ((18793:ℝ)/10000)^3 - 3*((18793:ℝ)/10000) - 1 -
      (lam9^3 - 3*lam9 - 1) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hpoly, hcub]

set_option maxHeartbeats 800000 in
/-- `λ₉ < 18794/10000`. -/
lemma lam9_lt : lam9 < (18794 : ℝ) / 10000 := by
  by_contra h
  push_neg at h
  have hcub := lam9_cubic
  have hone := lam9_gt_one
  have hfactor : (0:ℝ) < lam9^2 + (18794:ℝ)/10000 * lam9 + ((18794:ℝ)/10000)^2 - 3 := by
    nlinarith [sq_nonneg lam9, hone, sq_nonneg (lam9 - 1)]
  have hdiff : lam9 - (18794:ℝ)/10000 ≥ 0 := by linarith
  have hpoly : (lam9 - (18794:ℝ)/10000) * (lam9^2 + (18794:ℝ)/10000 * lam9 +
      ((18794:ℝ)/10000)^2 - 3) =
      (lam9^3 - 3*lam9 - 1) -
      (((18794:ℝ)/10000)^3 - 3*((18794:ℝ)/10000) - 1) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hpoly, hcub]

/-- `X(9) = 1/λ₉³`. -/
def X9 : ℝ := 1 / lam9 ^ 3

lemma lam9_cubed_pos : 0 < lam9 ^ 3 := pow_pos lam9_pos 3

def a0₉ : ℝ := 1 / 3
def b0₉ : ℝ := 8 / 21
def a1₉ : ℝ := 8 / 21
def b1₉ : ℝ := (8 / 21) * lam9 - 1 / 3
def a2₉ : ℝ := (8 / 21) * lam9 - 1 / 3
def b2₉ : ℝ := (8 / 21) * lam9 ^ 2 - (1 / 3) * lam9 - 8 / 21

def run9 : ℕ → ℝ × ℝ
  | 0 => (a0₉, b0₉)
  | 1 => (a1₉, b1₉)
  | _ => (a2₉, b2₉)

def lastBranch9 (p : ℝ × ℝ) : Prop := p.1 + lam9 * p.2 > 1

lemma b0₉_pos : 0 < b0₉ := by unfold b0₉; norm_num
lemma b1₉_pos : 0 < b1₉ := by unfold b1₉; nlinarith [lam9_gt]
lemma a2₉_pos : 0 < a2₉ := by unfold a2₉; nlinarith [lam9_gt]
lemma b2₉_pos : 0 < b2₉ := by
  unfold b2₉; nlinarith [lam9_gt, lam9_lt, sq_nonneg lam9]

/-- sub-threshold `P < 1/λ³`, cleared to `P·λ³ < 1`. -/
lemma P0₉_lt : a0₉ * b0₉ < X9 := by
  unfold a0₉ b0₉ X9
  rw [lt_div_iff₀ lam9_cubed_pos]
  nlinarith [lam9_gt, lam9_lt, lam9_cubic', sq_nonneg lam9, lam9_pos]

lemma P1₉_lt : a1₉ * b1₉ < X9 := by
  unfold a1₉ b1₉ X9
  rw [lt_div_iff₀ lam9_cubed_pos]
  nlinarith [lam9_gt, lam9_lt, lam9_cubic', sq_nonneg lam9, lam9_pos]

set_option maxHeartbeats 800000 in
lemma P2₉_lt : a2₉ * b2₉ < X9 := by
  unfold a2₉ b2₉ X9
  rw [lt_div_iff₀ lam9_cubed_pos]
  -- the product reduces, mod the cubic, to a degree-2 poly; supply that as a hint
  have hP2 : ((8:ℝ)/21 * lam9 - 1/3) * (8/21 * lam9^2 - 1/3*lam9 - 8/21) =
             -16/63 * lam9^2 + 59/147 * lam9 + 40/147 := by
    linear_combination (64/441 : ℝ) * lam9_cubic
  nlinarith [lam9_gt, lam9_lt, lam9_cubic', sq_nonneg lam9, lam9_pos, hP2]

lemma branch0₉ : lastBranch9 (a0₉, b0₉) := by
  unfold lastBranch9 a0₉ b0₉; simp only; nlinarith [lam9_gt]
lemma branch1₉ : lastBranch9 (a1₉, b1₉) := by
  unfold lastBranch9 a1₉ b1₉; simp only; nlinarith [lam9_gt, lam9_lt, sq_nonneg lam9]
lemma branch2₉ : lastBranch9 (a2₉, b2₉) := by
  unfold lastBranch9 a2₉ b2₉; simp only
  nlinarith [lam9_gt, lam9_lt, lam9_cubic', sq_nonneg lam9]

lemma bracket0₉ : lam9 * b0₉ ≤ 1 + a0₉ ∧ 1 + a0₉ < 2 * (lam9 * b0₉) := by
  unfold a0₉ b0₉
  exact ⟨by nlinarith [lam9_lt], by nlinarith [lam9_gt]⟩

lemma bracket1₉ : lam9 * b1₉ ≤ 1 + a1₉ ∧ 1 + a1₉ < 2 * (lam9 * b1₉) := by
  unfold a1₉ b1₉
  exact ⟨by nlinarith [lam9_gt, lam9_lt, sq_nonneg lam9],
         by nlinarith [lam9_gt, lam9_lt, sq_nonneg lam9]⟩

lemma kfloor0₉ : kfloor lam9 (a0₉, b0₉) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam9 a0₉ b0₉ lam9_pos b0₉_pos).mpr bracket0₉
lemma kfloor1₉ : kfloor lam9 (a1₉, b1₉) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam9 a1₉ b1₉ lam9_pos b1₉_pos).mpr bracket1₉

lemma step0₉ : run9 1 = kstep lam9 ((kfloor lam9 (run9 0) : ℝ)) (run9 0) := by
  show (a1₉, b1₉) = kstep lam9 ((kfloor lam9 (a0₉, b0₉) : ℝ)) (a0₉, b0₉)
  rw [kfloor0₉]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a1₉, b1₉) = HeckeRotArc.Mmap lam9 (a0₉, b0₉)
  refine Prod.ext ?_ ?_
  · show a1₉ = b0₉; unfold a1₉ b0₉; norm_num
  · show b1₉ = -a0₉ + lam9 * b0₉; unfold b1₉ a0₉ b0₉; ring

lemma step1₉ : run9 2 = kstep lam9 ((kfloor lam9 (run9 1) : ℝ)) (run9 1) := by
  show (a2₉, b2₉) = kstep lam9 ((kfloor lam9 (a1₉, b1₉) : ℝ)) (a1₉, b1₉)
  rw [kfloor1₉]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a2₉, b2₉) = HeckeRotArc.Mmap lam9 (a1₉, b1₉)
  refine Prod.ext ?_ ?_
  · show a2₉ = b1₉; unfold a2₉ b1₉; rfl
  · show b2₉ = -a1₉ + lam9 * b1₉; unfold b2₉ a1₉ b1₉; ring

theorem run9_isClusterRun : IsClusterRun lam9 X9 lastBranch9 run9 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro n hn; interval_cases n
    · exact ⟨P0₉_lt, branch0₉⟩
    · exact ⟨P1₉_lt, branch1₉⟩
    · exact ⟨P2₉_lt, branch2₉⟩
  · intro n hn; interval_cases n
    · exact b0₉_pos
    · exact b1₉_pos
  · intro n hn; interval_cases n
    · exact step0₉
    · exact step1₉
  · intro n hn; interval_cases n
    · exact bracket0₉
    · exact bracket1₉

theorem clusterCeiling9 : clusterCeiling lam9 X9 lastBranch9 2 :=
  ⟨run9, run9_isClusterRun⟩

/-- **★ B(9) = rotation-arc count — R2 closed for q=9.** -/
theorem Bq_eq_rotation_arc_q9 :
    clusterCeiling lam9 X9 lastBranch9 2 ↔ rotationArcCount lam9 X9 lastBranch9 2 :=
  HeckeRotArc.Bq_eq_rotation_arc lam9 lam9_pos X9 lastBranch9 2 (fun _ => clusterCeiling9)

theorem rotationArcCount9_realized : rotationArcCount lam9 X9 lastBranch9 2 :=
  HeckeRotArc.cluster_le_rotation_arc lam9 lam9_pos X9 lastBranch9 2 clusterCeiling9

/-! ## §2.  q = 8 — quartic field `Q(λ₈)`, `λ₈ = 2cos(π/8)`, minpoly `x⁴ − 4x² + 2`, `B(8) = 3`.

From `cos(4·π/8) = cos(π/2) = 0` and `cos 4θ = 8cos⁴θ − 8cos²θ + 1`:
`8c⁴ − 8c² + 1 = 0` ⟹ `λ⁴ − 4λ² + 2 = 0` for `λ = 2c`. -/

def lam8 : ℝ := 2 * Real.cos (Real.pi / 8)

lemma lam8_pos : 0 < lam8 := by
  unfold lam8
  apply mul_pos (by norm_num : (0:ℝ) < 2)
  exact Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

/-- The quartic identity `λ₈⁴ − 4λ₈² + 2 = 0`. -/
lemma lam8_quartic : lam8 ^ 4 - 4 * lam8 ^ 2 + 2 = 0 := by
  unfold lam8
  set c := Real.cos (Real.pi / 8) with hc_def
  set θ := Real.pi / 8 with hθ_def
  have h4θ : (4:ℝ) * θ = Real.pi / 2 := by rw [hθ_def]; ring
  have hcos4 : Real.cos (4 * θ) = 8 * c ^ 4 - 8 * c ^ 2 + 1 := by
    rw [show (4 : ℝ) * θ = 2 * (2 * θ) by ring, Real.cos_two_mul,
        show (2 : ℝ) * θ = θ + θ by ring, Real.cos_add]
    linear_combination (2 * Real.sin θ ^ 2 - 6 * c ^ 2 + 2) * Real.sin_sq_add_cos_sq θ
  have hval : Real.cos (4 * θ) = 0 := by rw [h4θ, Real.cos_pi_div_two]
  have h : 8 * c ^ 4 - 8 * c ^ 2 + 1 = 0 := by rw [← hcos4, hval]
  linear_combination (2 : ℝ) * h

lemma lam8_quartic' : lam8 ^ 4 = 4 * lam8 ^ 2 - 2 := by linarith [lam8_quartic]

lemma lam8_gt_one : 1 < lam8 := by
  unfold lam8
  have h_mono : Real.cos (Real.pi / 4) ≤ Real.cos (Real.pi / 8) := by
    apply Real.cos_le_cos_of_nonneg_of_le_pi
    · linarith [Real.pi_pos]
    · linarith [Real.pi_gt_three]
    · apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num : (0:ℝ) < 4)
        (by norm_num : (4:ℝ) ≤ 8)
  have h_cos_pi4 : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 := by rw [Real.cos_pi_div_four]
  rw [h_cos_pi4] at h_mono
  have h_sqrt2 : 1 < Real.sqrt 2 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp [Real.sqrt_one]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith [mul_le_mul_of_nonneg_left h_mono (by norm_num : (0:ℝ) ≤ 2)]

lemma lam8_lt_two : lam8 < 2 := by
  -- from the quartic `λ⁴ = 4λ² − 2` and `λ > 1`: `λ ≥ 2 ⟹ λ⁴ ≥ 16 > 14 ≥ 4λ²−2`, contradiction.
  have hq := lam8_quartic'
  have hone := lam8_gt_one
  nlinarith [hq, hone, sq_nonneg lam8, sq_nonneg (lam8 - 1), sq_nonneg (lam8^2 - 2),
    pow_pos lam8_pos 2, pow_pos lam8_pos 4]

set_option maxHeartbeats 800000 in
/-- `λ₈ > 18477/10000`. -/
lemma lam8_gt : (18477 : ℝ) / 10000 < lam8 := by
  by_contra h
  push_neg at h
  have hq := lam8_quartic
  have hone := lam8_gt_one
  have htwo := lam8_lt_two
  -- f(x) = x⁴ − 4x² + 2; f'(x) = 4x³ − 8x > 0 on (√2, 2); λ ∈ (√2,2).  Sign argument:
  have hfactor : (0:ℝ) < (lam8 + (18477:ℝ)/10000) * (lam8^2 + ((18477:ℝ)/10000)^2 - 4) := by
    nlinarith [hone, htwo, sq_nonneg lam8, sq_nonneg (lam8 - 1)]
  have hdiff : (18477:ℝ)/10000 - lam8 ≥ 0 := by linarith
  have hpoly : ((18477:ℝ)/10000 - lam8) *
      ((lam8 + (18477:ℝ)/10000) * (lam8^2 + ((18477:ℝ)/10000)^2 - 4)) =
      (((18477:ℝ)/10000)^4 - 4*((18477:ℝ)/10000)^2 + 2) - (lam8^4 - 4*lam8^2 + 2) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hpoly, hq]

set_option maxHeartbeats 800000 in
/-- `λ₈ < 18478/10000`. -/
lemma lam8_lt : lam8 < (18478 : ℝ) / 10000 := by
  by_contra h
  push_neg at h
  have hq := lam8_quartic
  have hone := lam8_gt_one
  have htwo := lam8_lt_two
  have hfactor : (0:ℝ) < (lam8 + (18478:ℝ)/10000) * (lam8^2 + ((18478:ℝ)/10000)^2 - 4) := by
    nlinarith [hone, htwo, sq_nonneg lam8, sq_nonneg (lam8 - 1)]
  have hdiff : lam8 - (18478:ℝ)/10000 ≥ 0 := by linarith
  have hpoly : (lam8 - (18478:ℝ)/10000) *
      ((lam8 + (18478:ℝ)/10000) * (lam8^2 + ((18478:ℝ)/10000)^2 - 4)) =
      (lam8^4 - 4*lam8^2 + 2) - (((18478:ℝ)/10000)^4 - 4*((18478:ℝ)/10000)^2 + 2) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hpoly, hq]

/-- `X(8) = 1/λ₈³`. -/
def X8 : ℝ := 1 / lam8 ^ 3
lemma lam8_cubed_pos : 0 < lam8 ^ 3 := pow_pos lam8_pos 3

def a0₈ : ℝ := 1 / 3
def b0₈ : ℝ := 13 / 33
def a1₈ : ℝ := 13 / 33
def b1₈ : ℝ := (13 / 33) * lam8 - 1 / 3
def a2₈ : ℝ := (13 / 33) * lam8 - 1 / 3
def b2₈ : ℝ := (13 / 33) * lam8 ^ 2 - (1 / 3) * lam8 - 13 / 33

def run8 : ℕ → ℝ × ℝ
  | 0 => (a0₈, b0₈)
  | 1 => (a1₈, b1₈)
  | _ => (a2₈, b2₈)

def lastBranch8 (p : ℝ × ℝ) : Prop := p.1 + lam8 * p.2 > 1

lemma b0₈_pos : 0 < b0₈ := by unfold b0₈; norm_num
lemma b1₈_pos : 0 < b1₈ := by unfold b1₈; nlinarith [lam8_gt]
lemma a2₈_pos : 0 < a2₈ := by unfold a2₈; nlinarith [lam8_gt]
lemma b2₈_pos : 0 < b2₈ := by
  unfold b2₈; nlinarith [lam8_gt, lam8_lt, sq_nonneg lam8]

lemma P0₈_lt : a0₈ * b0₈ < X8 := by
  unfold a0₈ b0₈ X8
  rw [lt_div_iff₀ lam8_cubed_pos]
  nlinarith [lam8_gt, lam8_lt, lam8_quartic', sq_nonneg lam8, lam8_pos]

lemma P1₈_lt : a1₈ * b1₈ < X8 := by
  unfold a1₈ b1₈ X8
  rw [lt_div_iff₀ lam8_cubed_pos]
  nlinarith [lam8_gt, lam8_lt, lam8_quartic', sq_nonneg lam8, lam8_pos]

set_option maxHeartbeats 1200000 in
lemma P2₈_lt : a2₈ * b2₈ < X8 := by
  unfold a2₈ b2₈ X8
  rw [lt_div_iff₀ lam8_cubed_pos]
  -- the product is degree-3 over the field; the reduced form is supplied to nlinarith
  have hP2 : ((13:ℝ)/33 * lam8 - 1/3) * (13/33 * lam8^2 - 1/3*lam8 - 13/33) =
             169/1089 * lam8^3 - 26/99 * lam8^2 - 16/363 * lam8 + 13/99 := by ring
  nlinarith [lam8_gt, lam8_lt, lam8_quartic', sq_nonneg lam8, lam8_pos, hP2,
    mul_pos lam8_pos lam8_pos]

lemma branch0₈ : lastBranch8 (a0₈, b0₈) := by
  unfold lastBranch8 a0₈ b0₈; simp only; nlinarith [lam8_gt]
lemma branch1₈ : lastBranch8 (a1₈, b1₈) := by
  unfold lastBranch8 a1₈ b1₈; simp only; nlinarith [lam8_gt, lam8_lt, sq_nonneg lam8]
lemma branch2₈ : lastBranch8 (a2₈, b2₈) := by
  unfold lastBranch8 a2₈ b2₈; simp only
  nlinarith [lam8_gt, lam8_lt, lam8_quartic', sq_nonneg lam8]

lemma bracket0₈ : lam8 * b0₈ ≤ 1 + a0₈ ∧ 1 + a0₈ < 2 * (lam8 * b0₈) := by
  unfold a0₈ b0₈
  exact ⟨by nlinarith [lam8_lt], by nlinarith [lam8_gt]⟩

lemma bracket1₈ : lam8 * b1₈ ≤ 1 + a1₈ ∧ 1 + a1₈ < 2 * (lam8 * b1₈) := by
  unfold a1₈ b1₈
  exact ⟨by nlinarith [lam8_gt, lam8_lt, sq_nonneg lam8],
         by nlinarith [lam8_gt, lam8_lt, sq_nonneg lam8]⟩

lemma kfloor0₈ : kfloor lam8 (a0₈, b0₈) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam8 a0₈ b0₈ lam8_pos b0₈_pos).mpr bracket0₈
lemma kfloor1₈ : kfloor lam8 (a1₈, b1₈) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam8 a1₈ b1₈ lam8_pos b1₈_pos).mpr bracket1₈

lemma step0₈ : run8 1 = kstep lam8 ((kfloor lam8 (run8 0) : ℝ)) (run8 0) := by
  show (a1₈, b1₈) = kstep lam8 ((kfloor lam8 (a0₈, b0₈) : ℝ)) (a0₈, b0₈)
  rw [kfloor0₈]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a1₈, b1₈) = HeckeRotArc.Mmap lam8 (a0₈, b0₈)
  refine Prod.ext ?_ ?_
  · show a1₈ = b0₈; unfold a1₈ b0₈; norm_num
  · show b1₈ = -a0₈ + lam8 * b0₈; unfold b1₈ a0₈ b0₈; ring

lemma step1₈ : run8 2 = kstep lam8 ((kfloor lam8 (run8 1) : ℝ)) (run8 1) := by
  show (a2₈, b2₈) = kstep lam8 ((kfloor lam8 (a1₈, b1₈) : ℝ)) (a1₈, b1₈)
  rw [kfloor1₈]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a2₈, b2₈) = HeckeRotArc.Mmap lam8 (a1₈, b1₈)
  refine Prod.ext ?_ ?_
  · show a2₈ = b1₈; unfold a2₈ b1₈; rfl
  · show b2₈ = -a1₈ + lam8 * b1₈; unfold b2₈ a1₈ b1₈; ring

theorem run8_isClusterRun : IsClusterRun lam8 X8 lastBranch8 run8 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro n hn; interval_cases n
    · exact ⟨P0₈_lt, branch0₈⟩
    · exact ⟨P1₈_lt, branch1₈⟩
    · exact ⟨P2₈_lt, branch2₈⟩
  · intro n hn; interval_cases n
    · exact b0₈_pos
    · exact b1₈_pos
  · intro n hn; interval_cases n
    · exact step0₈
    · exact step1₈
  · intro n hn; interval_cases n
    · exact bracket0₈
    · exact bracket1₈

theorem clusterCeiling8 : clusterCeiling lam8 X8 lastBranch8 2 :=
  ⟨run8, run8_isClusterRun⟩

/-- **★ B(8) = rotation-arc count — R2 closed for q=8.** -/
theorem Bq_eq_rotation_arc_q8 :
    clusterCeiling lam8 X8 lastBranch8 2 ↔ rotationArcCount lam8 X8 lastBranch8 2 :=
  HeckeRotArc.Bq_eq_rotation_arc lam8 lam8_pos X8 lastBranch8 2 (fun _ => clusterCeiling8)

theorem rotationArcCount8_realized : rotationArcCount lam8 X8 lastBranch8 2 :=
  HeckeRotArc.cluster_le_rotation_arc lam8 lam8_pos X8 lastBranch8 2 clusterCeiling8

end

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeRotArcR2hi.run9_isClusterRun
#print axioms HeckeRotArcR2hi.Bq_eq_rotation_arc_q9
#print axioms HeckeRotArcR2hi.rotationArcCount9_realized
#print axioms HeckeRotArcR2hi.run8_isClusterRun
#print axioms HeckeRotArcR2hi.Bq_eq_rotation_arc_q8
#print axioms HeckeRotArcR2hi.rotationArcCount8_realized

end HeckeRotArcR2hi
