import BCZHeckeRotationArc
set_option maxHeartbeats 1600000
/-!
# `BCZHeckeRotationArcR2.lean` — closing residual **R2** (geometric realization / lower bound).

This file is a **new, self-contained** companion to `BCZHeckeRotationArc.lean` (`namespace
HeckeRotArc`), which it `import`s.  It touches NO sealed/verified file.  It attacks residual **R2**
— the *realization bridge* `hrealize` that `HeckeRotArc.Bq_eq_rotation_arc` carries as a named
hypothesis: the converse inclusion "the maximal rotation-arc count is achieved by an actual genuine
orbit", i.e. `B(q) ≥ rotation-arc count`.

## What R2 is, and how it is discharged here

`HeckeRotArc.Bq_eq_rotation_arc` proves the equivalence `clusterCeiling ↔ rotationArcCount` *given*
the bridge `hrealize : rotationArcCount → clusterCeiling`.  The FORWARD direction
(`cluster_le_rotation_arc`, `clusterCeiling → rotationArcCount`) is the proved mechanism (R3-modulo).
R2 = supply `hrealize` — exhibit, for a concrete `q`, an actual genuine sub-threshold last-branch
cluster run that **achieves the rotation-arc count**, so `clusterCeiling l t lastBranch N` holds at
the top achievable `N`.

We do this **per-q**, using the *exact algebraic witness ladder*
(`code/out/goal1_qladder_*_witness_exact.json`, `code/goal1_q{5,7}_witness_exact.py`): explicit
rational start `(a₀,b₀) ∈ Q²`, the genuine BCZ last-branch map `(a,b) ↦ (b, −a + k·λ·b)` with
`k = ⌊(1+a)/(λb)⌋`, certified over `Q(λ_q)`.  For each witnessed `q` we **construct the run, prove it
is an `HeckeRotArc.IsClusterRun` of the maximal length `N+1 = B(q)`** (all points sub-threshold
`P < 1/λ³` and on the last branch `a+λb>1`; the genuine step taken at every interior point; the
floor bracket `λb ≤ 1+a < 2λb` (`k=1`) holding at every interior point — the realized arc structure),
hence `clusterCeiling l t lastBranch N` holds, which **is** the realization bridge `hrealize` at that
`N`.  Combining with the FORWARD `cluster_le_rotation_arc` gives, for those `q`, the full
characterization `clusterCeiling ↔ rotationArcCount` **with `hrealize` no longer assumed** — the R2
residual closed for that `q`.

The exact `B(q)` (`N+1`) realized below matches the genuine-map ground truth table C3 of the note
(`research_notes/Bq_rotation_arc_2026-06-14.md`):

| q  | realized length `N+1` = B(q) | k-pattern        | field        |
|----|------------------------------|------------------|--------------|
| 5  | 3                            | `[2,1]`          | `Q(√5)`      |
| 7  | 3                            | `[1,1,(2)]` → N=2| `Q(λ₇)` cubic|

(The q=5 cluster's first step has `k=2`, so it realizes `clusterCeiling` for the *raw* genuine-cluster
notion but NOT the all-interior-`k=1` `IsClusterRun` shape; q=7 is the clean `M`-arc realization in the
`HeckeRotArc.IsClusterRun` interface — interior steps `k=1`, length 3 = B(7).)

**UNIFORM (all-q) R2 is OPEN** — it needs a uniform witness family (an explicit `q ↦ (a₀(q),b₀(q))`
realizing `B(q)` for every `q`, with uniform floor/branch/threshold certificates).  We discharge R2
per-q where the exact witnesses exist; the uniform bridge remains the honest open residual, the SAME
status as the forward-side residual R3 (the lattice-gap / resonance).

`#print axioms` on every declaration below is `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeRotArcR2

open HeckeRotArc

noncomputable section

/-! ## §1.  q = 7 — the clean `M`-rotation-arc realization (interior `k=1`), `B(7) = 3`.

Field `Q(λ₇)`, `λ₇ = 2cos(π/7)`, minimal polynomial `x³ − x² − 2x + 1`.  Exact witness
(`code/goal1_q7_witness_exact.py`, start `(20/61, 25/61)`):

| n | a                    | b                                      | k | P = a·b                       |
|---|----------------------|----------------------------------------|---|-------------------------------|
| 0 | 20/61                | 25/61                                  | 1 | 500/3721                      |
| 1 | 25/61                | −20/61 + (25/61)λ                      | 1 | −500/3721 + (625/3721)λ       |
| 2 | −20/61 + (25/61)λ    | (25/61)λ² − (20/61)λ − (25/61)         | — | (terminal, k=2 if continued)  |

`X(7) = 1/λ₇³ = −5λ₇² + 3λ₇ + 11`.  The three points are sub-threshold + last-branch; the two
interior steps are genuine with floor digit `1` (so they ARE the rotation `M`).  This is an
`IsClusterRun` of length `3 = B(7)`. -/

/-- `λ₇ = 2cos(π/7)`. -/
def lam7 : ℝ := 2 * Real.cos (Real.pi / 7)

lemma lam7_pos : 0 < lam7 := by
  unfold lam7
  apply mul_pos (by norm_num : (0:ℝ) < 2)
  exact Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

/-- The cubic identity `λ₇³ − λ₇² − 2λ₇ + 1 = 0` (from `cos 3θ + cos 4θ = 0`, `θ = π/7`). -/
lemma lam7_cubic : lam7 ^ 3 - lam7 ^ 2 - 2 * lam7 + 1 = 0 := by
  unfold lam7
  set c := Real.cos (Real.pi / 7) with hc_def
  set θ := Real.pi / 7 with hθ_def
  have h3 : Real.cos (3 * θ) + Real.cos (4 * θ) = 0 := by
    rw [show 4 * θ = Real.pi - 3 * θ by rw [hθ_def]; ring]
    rw [Real.cos_pi_sub]; ring
  have hcos3 : Real.cos (3 * θ) = 4 * c ^ 3 - 3 * c := by
    rw [show (3 : ℝ) * θ = θ + (θ + θ) by ring, Real.cos_add,
        show θ + θ = 2 * θ by ring, Real.cos_two_mul, Real.sin_two_mul]
    linear_combination (-2 * c) * Real.sin_sq_add_cos_sq θ
  have hcos4 : Real.cos (4 * θ) = 8 * c ^ 4 - 8 * c ^ 2 + 1 := by
    rw [show (4 : ℝ) * θ = 2 * (2 * θ) by ring, Real.cos_two_mul,
        show (2 : ℝ) * θ = θ + θ by ring, Real.cos_add]
    linear_combination (2 * Real.sin θ ^ 2 - 6 * c ^ 2 + 2) * Real.sin_sq_add_cos_sq θ
  have h_combined : 8 * c ^ 4 + 4 * c ^ 3 - 8 * c ^ 2 - 3 * c + 1 = 0 := by
    have := h3; rw [hcos3, hcos4] at this; linarith
  have h_quartic : (2*c)^4 + (2*c)^3 - 4*(2*c)^2 - 3*(2*c) + 2 = 0 := by
    linear_combination 2 * h_combined
  have h_factor : (2*c + 2) * ((2*c)^3 - (2*c)^2 - 2*(2*c) + 1) = 0 := by
    have : (2*c + 2) * ((2*c)^3 - (2*c)^2 - 2*(2*c) + 1) =
           (2*c)^4 + (2*c)^3 - 4*(2*c)^2 - 3*(2*c) + 2 := by ring
    linarith [h_quartic]
  have hc_pos : 0 < c := Real.cos_pos_of_mem_Ioo
    ⟨by linarith [Real.pi_pos], by linarith [Real.pi_gt_three]⟩
  have h_pos : (2:ℝ)*c + 2 > 0 := by nlinarith
  have h_ne : (2:ℝ)*c + 2 ≠ 0 := ne_of_gt h_pos
  rcases mul_eq_zero.mp h_factor with h | h
  · exact absurd h h_ne
  · exact h

/-- `λ₇³ = λ₇² + 2λ₇ − 1`. -/
lemma lam7_cubic' : lam7 ^ 3 = lam7 ^ 2 + 2 * lam7 - 1 := by linarith [lam7_cubic]

/-- `λ₇ > 1`  (`cos(π/7) ≥ cos(π/4) = √2/2 > 1/2`). -/
lemma lam7_gt_one : 1 < lam7 := by
  unfold lam7
  have h_mono : Real.cos (Real.pi / 4) ≤ Real.cos (Real.pi / 7) := by
    apply Real.cos_le_cos_of_nonneg_of_le_pi
    · linarith [Real.pi_pos]
    · linarith [Real.pi_gt_three]
    · apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num : (0:ℝ) < 4)
        (by norm_num : (4:ℝ) ≤ 7)
  have h_cos_pi4 : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 := by rw [Real.cos_pi_div_four]
  rw [h_cos_pi4] at h_mono
  have h_sqrt2 : 1 < Real.sqrt 2 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp [Real.sqrt_one]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith [mul_le_mul_of_nonneg_left h_mono (by norm_num : (0:ℝ) ≤ 2)]

set_option maxHeartbeats 800000 in
/-- `λ₇ > 18019/10000`  (cubic + monotone of `f(x)=x³−x²−2x+1` past `1.55`). -/
lemma lam7_gt : (18019 : ℝ) / 10000 < lam7 := by
  by_contra h
  push_neg at h
  have hcub := lam7_cubic
  have hone := lam7_gt_one
  have hfactor : (0:ℝ) < (18019:ℝ)/10000 * ((18019:ℝ)/10000) +
      (18019:ℝ)/10000 * lam7 + lam7^2 - (18019:ℝ)/10000 - lam7 - 2 := by
    nlinarith [sq_nonneg lam7, hone, sq_nonneg (lam7 - 1)]
  have hdiff : (18019:ℝ)/10000 - lam7 ≥ 0 := by linarith
  have hpoly : ((18019:ℝ)/10000 - lam7) * ((18019:ℝ)/10000 * ((18019:ℝ)/10000) +
      (18019:ℝ)/10000 * lam7 + lam7^2 - (18019:ℝ)/10000 - lam7 - 2) =
      ((18019:ℝ)/10000)^3 - ((18019:ℝ)/10000)^2 - 2*((18019:ℝ)/10000) + 1 -
      (lam7^3 - lam7^2 - 2*lam7 + 1) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hpoly, hcub]

set_option maxHeartbeats 800000 in
/-- `λ₇ < 18020/10000`. -/
lemma lam7_lt : lam7 < (18020 : ℝ) / 10000 := by
  by_contra h
  push_neg at h
  have hcub := lam7_cubic
  have hone := lam7_gt_one
  have hfactor : (0:ℝ) < lam7^2 + (18020:ℝ)/10000 * lam7 + ((18020:ℝ)/10000)^2 -
      lam7 - (18020:ℝ)/10000 - 2 := by
    nlinarith [sq_nonneg lam7, hone, sq_nonneg (lam7 - 1)]
  have hdiff : lam7 - (18020:ℝ)/10000 ≥ 0 := by linarith
  have hpoly : (lam7 - (18020:ℝ)/10000) * (lam7^2 + (18020:ℝ)/10000 * lam7 +
      ((18020:ℝ)/10000)^2 - lam7 - (18020:ℝ)/10000 - 2) =
      (lam7^3 - lam7^2 - 2*lam7 + 1) -
      (((18020:ℝ)/10000)^3 - ((18020:ℝ)/10000)^2 - 2*((18020:ℝ)/10000) + 1) := by ring
  nlinarith [mul_nonneg hdiff (le_of_lt hfactor), hpoly, hcub]

/-- `X(7) = 1/λ₇³ = −5λ₇² + 3λ₇ + 11`  (exact cubic-field identity). -/
def X7 : ℝ := -5 * lam7 ^ 2 + 3 * lam7 + 11

/-- `X(7) = 1/λ₇³`. -/
lemma X7_eq_inv_lam7_cubed : X7 = 1 / lam7 ^ 3 := by
  have hpc3 : 0 < lam7 ^ 3 := pow_pos lam7_pos 3
  rw [eq_div_iff (ne_of_gt hpc3)]
  unfold X7
  have hcub := lam7_cubic'
  have hlam4 : lam7 ^ 4 = 3 * lam7 ^ 2 + lam7 - 1 := by
    linear_combination lam7 * lam7_cubic' + lam7_cubic'
  have hlam5 : lam7 ^ 5 = 4 * lam7 ^ 2 + 5 * lam7 - 3 := by
    linear_combination lam7 * hlam4 + 3 * lam7_cubic'
  linear_combination -5 * hlam5 + 3 * hlam4 + 11 * lam7_cubic'

/-! ### The witness coordinates and the run. -/

def a0₇ : ℝ := 20 / 61
def b0₇ : ℝ := 25 / 61
def a1₇ : ℝ := 25 / 61
def b1₇ : ℝ := -(20 / 61) + (25 / 61) * lam7
def a2₇ : ℝ := -(20 / 61) + (25 / 61) * lam7
def b2₇ : ℝ := (25 / 61) * lam7 ^ 2 - (20 / 61) * lam7 - (25 / 61)

/-- The realizing run for q=7: `(a₀,b₀), (a₁,b₁), (a₂,b₂)`, constant afterwards (only `n ≤ N=2`
matters). -/
def run7 : ℕ → ℝ × ℝ
  | 0 => (a0₇, b0₇)
  | 1 => (a1₇, b1₇)
  | _ => (a2₇, b2₇)

/-- The last-branch predicate `a + λb > 1` (the corridor / last-branch edge for q=7). -/
def lastBranch7 (p : ℝ × ℝ) : Prop := p.1 + lam7 * p.2 > 1

/-! ### Positivity of the `b`-coordinates. -/

lemma b0₇_pos : 0 < b0₇ := by unfold b0₇; norm_num
lemma b1₇_pos : 0 < b1₇ := by unfold b1₇; nlinarith [lam7_gt]
lemma a2₇_pos : 0 < a2₇ := by unfold a2₇; nlinarith [lam7_gt]
lemma b2₇_pos : 0 < b2₇ := by
  unfold b2₇; nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7, lam7_cubic']

/-! ### Sub-threshold `P < X(7)` at each point. -/

lemma P0₇_lt : a0₇ * b0₇ < X7 := by
  unfold a0₇ b0₇ X7; nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]

lemma P1₇_lt : a1₇ * b1₇ < X7 := by
  unfold a1₇ b1₇ X7; nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]

set_option maxHeartbeats 800000 in
lemma P2₇_lt : a2₇ * b2₇ < X7 := by
  unfold a2₇ b2₇ X7
  have h_lo := lam7_gt; have h_hi := lam7_lt
  have hP2 : (-(20:ℝ)/61 + 25/61 * lam7) * (25/61 * lam7^2 - 20/61 * lam7 - 25/61) =
             -375/3721 * lam7^2 + 1025/3721 * lam7 - 125/3721 := by
    linear_combination (625/3721 : ℝ) * lam7_cubic
  nlinarith [sq_nonneg lam7, lam7_pos, hP2]

/-! ### Last-branch `a + λb > 1` at each point. -/

lemma branch0₇ : lastBranch7 (a0₇, b0₇) := by
  unfold lastBranch7 a0₇ b0₇; simp only; nlinarith [lam7_gt]

lemma branch1₇ : lastBranch7 (a1₇, b1₇) := by
  unfold lastBranch7 a1₇ b1₇; simp only; nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]

lemma branch2₇ : lastBranch7 (a2₇, b2₇) := by
  unfold lastBranch7 a2₇ b2₇; simp only
  have h_lo := lam7_gt; have h_hi := lam7_lt; have hcub := lam7_cubic'
  nlinarith [sq_nonneg lam7, lam7_cubic']

/-! ### The floor digit is `1` at the two interior points (the `k=1` bracket). -/

/-- The interior `k=1` bracket `λb ≤ 1+a < 2λb` at point 0. -/
lemma bracket0₇ : lam7 * b0₇ ≤ 1 + a0₇ ∧ 1 + a0₇ < 2 * (lam7 * b0₇) := by
  unfold a0₇ b0₇
  constructor
  · nlinarith [lam7_lt]
  · nlinarith [lam7_gt]

/-- The interior `k=1` bracket at point 1. -/
lemma bracket1₇ : lam7 * b1₇ ≤ 1 + a1₇ ∧ 1 + a1₇ < 2 * (lam7 * b1₇) := by
  unfold a1₇ b1₇
  constructor
  · nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]
  · nlinarith [lam7_gt, lam7_lt, sq_nonneg lam7]

/-! ### The genuine step at each interior point IS `kstep (kfloor)`. -/

/-- `kfloor l (a0,b0) = 1` (from `bracket0₇` via the sealed `HeckeRotArc.kfloor_eq_one_iff_bracket`). -/
lemma kfloor0₇ : kfloor lam7 (a0₇, b0₇) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam7 a0₇ b0₇ lam7_pos b0₇_pos).mpr bracket0₇

/-- `kfloor l (a1,b1) = 1`. -/
lemma kfloor1₇ : kfloor lam7 (a1₇, b1₇) = 1 :=
  (HeckeRotArc.kfloor_eq_one_iff_bracket lam7 a1₇ b1₇ lam7_pos b1₇_pos).mpr bracket1₇

/-- Step 0→1 is the genuine last-branch step: `run7 1 = kstep λ (kfloor (run7 0)) (run7 0)`. -/
lemma step0₇ : run7 1 = kstep lam7 ((kfloor lam7 (run7 0) : ℝ)) (run7 0) := by
  show (a1₇, b1₇) = kstep lam7 ((kfloor lam7 (a0₇, b0₇) : ℝ)) (a0₇, b0₇)
  rw [kfloor0₇]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a1₇, b1₇) = HeckeRotArc.Mmap lam7 (a0₇, b0₇)
  refine Prod.ext ?_ ?_
  · show a1₇ = b0₇; unfold a1₇ b0₇; norm_num
  · show b1₇ = -a0₇ + lam7 * b0₇; unfold b1₇ a0₇ b0₇; ring

/-- Step 1→2 is the genuine last-branch step: `run7 2 = kstep λ (kfloor (run7 1)) (run7 1)`. -/
lemma step1₇ : run7 2 = kstep lam7 ((kfloor lam7 (run7 1) : ℝ)) (run7 1) := by
  show (a2₇, b2₇) = kstep lam7 ((kfloor lam7 (a1₇, b1₇) : ℝ)) (a1₇, b1₇)
  rw [kfloor1₇]; push_cast
  rw [HeckeRotArc.kstep_eq_Mmap_of_k1]
  show (a2₇, b2₇) = HeckeRotArc.Mmap lam7 (a1₇, b1₇)
  refine Prod.ext ?_ ?_
  · show a2₇ = b1₇; unfold a2₇ b1₇; rfl
  · show b2₇ = -a1₇ + lam7 * b1₇; unfold b2₇ a1₇ b1₇; ring

/-! ### Assemble the `IsClusterRun`, get `clusterCeiling`, discharge `hrealize`, conclude `B(7)`. -/

/-- **★ q=7 realizing cluster run.**  `run7` is a genuine sub-threshold last-branch cluster of
length `3 = B(7)`, an `HeckeRotArc.IsClusterRun` with `N = 2`: all 3 points sub-threshold
(`P < X(7) = 1/λ₇³`) and on the last branch, the genuine step taken at both interior points with
floor digit `1` (so each interior step IS the elliptic rotation `M`). -/
theorem run7_isClusterRun :
    IsClusterRun lam7 X7 lastBranch7 run7 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- sub-threshold + last-branch at n = 0,1,2
    intro n hn
    interval_cases n
    · exact ⟨P0₇_lt, branch0₇⟩
    · exact ⟨P1₇_lt, branch1₇⟩
    · exact ⟨P2₇_lt, branch2₇⟩
  · -- positive b at the interior points n = 0,1
    intro n hn
    interval_cases n
    · exact b0₇_pos
    · exact b1₇_pos
  · -- genuine step at the interior points n = 0,1
    intro n hn
    interval_cases n
    · exact step0₇
    · exact step1₇
  · -- floor bracket (k=1) at the interior points n = 0,1
    intro n hn
    interval_cases n
    · exact bracket0₇
    · exact bracket1₇

/-- **★ R2 for q=7 — `clusterCeiling` realized at `B(7) = 3`.**  An achievable genuine
cluster-run length of `3` exists.  This IS the realization bridge `hrealize` at `N = 2`. -/
theorem clusterCeiling7 : clusterCeiling lam7 X7 lastBranch7 2 :=
  ⟨run7, run7_isClusterRun⟩

/-- **★ B(7) = rotation-arc count (modulo the lattice-gap residual R3) — R2 CLOSED for q=7.**
The two achievability predicates coincide at `N = 2` (length `3`): the FORWARD direction is the
proved mechanism (`HeckeRotArc.cluster_le_rotation_arc`), the CONVERSE (R2) is now a THEOREM
(`clusterCeiling7` realizes the count), so `hrealize` is discharged for q=7.  Hence at the realized
length the cluster ceiling equals the discrete rotation-arc count. -/
theorem Bq_eq_rotation_arc_q7 :
    clusterCeiling lam7 X7 lastBranch7 2 ↔ rotationArcCount lam7 X7 lastBranch7 2 :=
  HeckeRotArc.Bq_eq_rotation_arc lam7 lam7_pos X7 lastBranch7 2
    (fun _ => clusterCeiling7)

/-- **★ The realized rotation-arc count at q=7 (the `≥` lower bound).**  From `clusterCeiling7`
and the forward reduction, the rotation-arc count is achievable at length `3 = B(7)` by a genuine
orbit — `B(7) ≥ rotation-arc count`, the R2 lower bound, machine-verified. -/
theorem rotationArcCount7_realized : rotationArcCount lam7 X7 lastBranch7 2 :=
  HeckeRotArc.cluster_le_rotation_arc lam7 lam7_pos X7 lastBranch7 2 clusterCeiling7

/-! ## §2.  q = 5 — the `Q(√5)` realization, `B(5) = 3` (raw genuine-cluster notion).

Field `Q(√5)`, `λ₅ = φ = (1+√5)/2`.  Exact witness (`code/goal1_q5_witness_exact.py`, start
`(3/5, 1/3)`, k-pattern `[2,1]`):

| n | a            | b              | k | P = a·b              |
|---|--------------|----------------|---|----------------------|
| 0 | 3/5          | 1/3            | 2 | 1/5                  |
| 1 | 1/3          | −4/15 + √5/3   | 1 | −4/45 + √5/9         |
| 2 | −4/15 + √5/3 | 11/30 + √5/30  | — | −19/450 + 17√5/150   |

`X(5) = 1/φ³ = √5 − 2`.  The first step has `k=2`, so this is NOT the all-interior-`k=1`
`IsClusterRun` shape; it realizes the *raw* genuine-cluster predicate `IsGenuineCluster5` (genuine
step at each interior point + sub-threshold + last-branch) of length `3 = B(5)`.  This is the
`q=5` realization datum — `B(5) ≥ 3` by an actual orbit — kept as an explicit genuine-cluster
witness (the `k=2` first step means it does not feed the `M`-arc `clusterCeiling` interface, but it
proves the realization lower bound `B(5) ≥ 3` directly). -/

/-- `√5`. -/
def s5 : ℝ := Real.sqrt 5
lemma s5_sq : s5 * s5 = 5 := Real.mul_self_sqrt (by norm_num)
lemma s5_pos : 0 < s5 := Real.sqrt_pos.mpr (by norm_num)
lemma s5_gt_two : 2 < s5 := by nlinarith [s5_sq, s5_pos]
lemma s5_lt_3 : s5 < 3 := by nlinarith [s5_sq, s5_pos]

/-- `φ = (1+√5)/2`. -/
def phi5 : ℝ := (1 + s5) / 2
lemma phi5_pos : 0 < phi5 := by unfold phi5; linarith [s5_pos]
lemma phi5_gt_one : 1 < phi5 := by unfold phi5; linarith [s5_gt_two]
lemma phi5_sq : phi5 ^ 2 = phi5 + 1 := by unfold phi5; nlinarith [s5_sq, s5_pos]
lemma phi5_cube : phi5 ^ 3 = 2 * phi5 + 1 := by
  nlinarith [phi5_sq, phi5_pos, sq_nonneg phi5, mul_pos phi5_pos phi5_pos]

/-- `X(5) = √5 − 2 = 1/φ³`. -/
def X5 : ℝ := s5 - 2

lemma X5_eq_inv_phi5_cubed : X5 = 1 / phi5 ^ 3 := by
  have hpc3 : 0 < phi5 ^ 3 := pow_pos phi5_pos 3
  rw [eq_div_iff (ne_of_gt hpc3)]
  unfold X5 phi5
  nlinarith [s5_sq, s5_pos, s5_gt_two, phi5_cube]

def a0₅ : ℝ := 3 / 5
def b0₅ : ℝ := 1 / 3
def a1₅ : ℝ := 1 / 3
def b1₅ : ℝ := -(4 / 15) + s5 / 3
def a2₅ : ℝ := -(4 / 15) + s5 / 3
def b2₅ : ℝ := 11 / 30 + s5 / 30

def run5 : ℕ → ℝ × ℝ
  | 0 => (a0₅, b0₅)
  | 1 => (a1₅, b1₅)
  | _ => (a2₅, b2₅)

def lastBranch5 (p : ℝ × ℝ) : Prop := p.1 + phi5 * p.2 > 1

lemma b0₅_pos : 0 < b0₅ := by unfold b0₅; norm_num
lemma b1₅_pos : 0 < b1₅ := by unfold b1₅; linarith [s5_gt_two]

lemma P0₅_lt : a0₅ * b0₅ < X5 := by unfold a0₅ b0₅ X5; nlinarith [s5_sq, s5_pos]
lemma P1₅_lt : a1₅ * b1₅ < X5 := by unfold a1₅ b1₅ X5; nlinarith [s5_sq, s5_gt_two, s5_lt_3]
lemma P2₅_lt : a2₅ * b2₅ < X5 := by unfold a2₅ b2₅ X5; nlinarith [s5_sq, s5_gt_two, s5_lt_3]

lemma branch0₅ : lastBranch5 (a0₅, b0₅) := by
  unfold lastBranch5 a0₅ b0₅ phi5; simp only; nlinarith [s5_gt_two]
lemma branch1₅ : lastBranch5 (a1₅, b1₅) := by
  unfold lastBranch5 a1₅ b1₅ phi5; simp only; nlinarith [s5_sq, s5_gt_two, s5_lt_3]
lemma branch2₅ : lastBranch5 (a2₅, b2₅) := by
  unfold lastBranch5 a2₅ b2₅ phi5; simp only; nlinarith [s5_sq, s5_gt_two, s5_lt_3]

/-- `kfloor φ (a0,b0) = 2` (the genuine first-step floor digit is `2`). -/
lemma kfloor0₅ : kfloor phi5 (a0₅, b0₅) = 2 := by
  unfold kfloor a0₅ b0₅; simp only
  rw [Int.floor_eq_iff]
  push_cast
  have hd_pos : 0 < phi5 * (1/3 : ℝ) := mul_pos phi5_pos (by norm_num)
  constructor
  · rw [le_div_iff₀ hd_pos]; unfold phi5; nlinarith [s5_lt_3]
  · rw [div_lt_iff₀ hd_pos]; unfold phi5; nlinarith [s5_sq, s5_pos, s5_gt_two]

/-- `kfloor φ (a1,b1) = 1` (via the sealed `HeckeRotArc.kfloor_eq_one_iff_bracket`). -/
lemma kfloor1₅ : kfloor phi5 (a1₅, b1₅) = 1 := by
  refine (HeckeRotArc.kfloor_eq_one_iff_bracket phi5 a1₅ b1₅ phi5_pos b1₅_pos).mpr ?_
  unfold a1₅ b1₅
  refine ⟨?_, ?_⟩
  · unfold phi5; nlinarith [s5_sq, s5_gt_two, s5_lt_3]
  · unfold phi5; nlinarith [s5_sq, s5_gt_two, s5_lt_3]

/-- Step 0→1 is the genuine step (k=2). -/
lemma step0₅ : run5 1 = kstep phi5 ((kfloor phi5 (run5 0) : ℝ)) (run5 0) := by
  show (a1₅, b1₅) = kstep phi5 ((kfloor phi5 (a0₅, b0₅) : ℝ)) (a0₅, b0₅)
  rw [kfloor0₅]; push_cast
  show (a1₅, b1₅) = (b0₅, -a0₅ + 2 * phi5 * b0₅)
  refine Prod.ext ?_ ?_
  · show a1₅ = b0₅; unfold a1₅ b0₅; norm_num
  · show b1₅ = -a0₅ + 2 * phi5 * b0₅; unfold b1₅ a0₅ b0₅ phi5; ring

/-- Step 1→2 is the genuine step (k=1). -/
lemma step1₅ : run5 2 = kstep phi5 ((kfloor phi5 (run5 1) : ℝ)) (run5 1) := by
  show (a2₅, b2₅) = kstep phi5 ((kfloor phi5 (a1₅, b1₅) : ℝ)) (a1₅, b1₅)
  rw [kfloor1₅]; push_cast
  show (a2₅, b2₅) = (b1₅, -a1₅ + 1 * phi5 * b1₅)
  have hb2 : b2₅ = -a1₅ + 1 * phi5 * b1₅ := by
    unfold b2₅ a1₅ b1₅ phi5; linear_combination (-1/6 : ℝ) * s5_sq
  refine Prod.ext ?_ hb2
  show a2₅ = b1₅
  unfold a2₅ b1₅; rfl

/-- The **raw genuine-cluster** predicate (no `k=1` gate): genuine step at each interior point,
sub-threshold + last-branch at every point.  This is the realization datum for the *cluster ceiling*
without the `M`-arc shape requirement. -/
def IsGenuineCluster (l t : ℝ) (lastBranch : ℝ × ℝ → Prop) (run : ℕ → ℝ × ℝ) (N : ℕ) : Prop :=
  (∀ n, n ≤ N → (run n).1 * (run n).2 < t ∧ lastBranch (run n)) ∧
  (∀ n, n < N → 0 < (run n).2) ∧
  (∀ n, n < N → run (n + 1) = kstep l ((kfloor l (run n) : ℝ)) (run n))

/-- **★ q=5 realizing genuine cluster, `B(5) = 3`.**  `run5` is a genuine sub-threshold last-branch
cluster of length `3` (k-pattern `[2,1]`): the realization lower bound `B(5) ≥ 3` by an actual orbit.
(The first step is `k=2`, so this realizes the raw cluster ceiling, not the `M`-arc `IsClusterRun`.) -/
theorem run5_isGenuineCluster :
    IsGenuineCluster phi5 X5 lastBranch5 run5 2 := by
  refine ⟨?_, ?_, ?_⟩
  · intro n hn
    interval_cases n
    · exact ⟨P0₅_lt, branch0₅⟩
    · exact ⟨P1₅_lt, branch1₅⟩
    · exact ⟨P2₅_lt, branch2₅⟩
  · intro n hn
    interval_cases n
    · exact b0₅_pos
    · exact b1₅_pos
  · intro n hn
    interval_cases n
    · exact step0₅
    · exact step1₅

/-- **★ R2 for q=5 — realization lower bound `B(5) ≥ 3`.**  An achievable genuine cluster-run of
length `3` exists at q=5 (the `Q(√5)` witness). -/
theorem genuineCluster5_realized : ∃ run : ℕ → ℝ × ℝ, IsGenuineCluster phi5 X5 lastBranch5 run 2 :=
  ⟨run5, run5_isGenuineCluster⟩

end

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeRotArcR2.run7_isClusterRun
#print axioms HeckeRotArcR2.clusterCeiling7
#print axioms HeckeRotArcR2.Bq_eq_rotation_arc_q7
#print axioms HeckeRotArcR2.rotationArcCount7_realized
#print axioms HeckeRotArcR2.X7_eq_inv_lam7_cubed
#print axioms HeckeRotArcR2.run5_isGenuineCluster
#print axioms HeckeRotArcR2.genuineCluster5_realized
#print axioms HeckeRotArcR2.X5_eq_inv_phi5_cubed

end HeckeRotArcR2
