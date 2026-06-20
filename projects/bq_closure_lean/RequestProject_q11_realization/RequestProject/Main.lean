import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# q = 11 realization for the B(q) rotation-arc theorem (residual R2).

This file is a **self-contained** RequestProject targeting the smallest open per-`q`
realization gap in the B(q) rotation-arc theorem: the `q = 11` realization datum.

The B(q) theorem (in the sealed repo files `BCZHeckeRotationArc*.lean`) reduces the
cluster ceiling `B(q)` for the Rosen continued-fraction last-branch observable to the
count of lattice points on an `M`-rotation arc on the conserved ellipse, where
`M (a,b) = (b, -a + λ b)` is the elliptic rotation by `-π/q` (`λ = 2cos(π/q)`).

The forward direction (`cluster ⟹ rotation arc`, `cluster_le_rotation_arc`) is already
machine-verified. The remaining **R2** residual is the per-`q` *realization*: exhibit an
actual genuine sub-threshold last-branch cluster run of the claimed length, which
discharges the realization bridge `hrealize` for that `q`. Realizations already exist
(sealed, axiom-clean) for `q = 7, 8, 9, 10, 12, 13` (and a lower bound `B(5) ≥ 3`).
`q = 11` is the smallest gap inside that ladder.

## What this file proves (target)

`B(11) ≥ 3` is realized (lower bound): there is a genuine sub-threshold last-branch
cluster run of length `3` (interior floor `k = 1`) for `λ₁₁ = 2cos(π/11)`.
Concretely we prove

  `clusterCeiling11 : clusterCeiling lam11 X11 lastBranch11 2`

(`N = 2`, run length `N+1 = 3`). This discharges the realization residual (R2) for
q=11: it is exactly the `hrealize` input the sealed `Bq_eq_rotation_arc` consumes.

SCOPE: this is the LOWER bound `B(11) ≥ 3` only — a length-3 cluster EXISTS. It does
NOT prove maximality `B(11) ≤ 3`; that rests on numeric ground truth (dps≥40 grid scan).

The witness orbit is the EXACT rational start `(34/101, 37/101)` (a genuine BCZ
cross-section domain point), iterated by `M`: verified at dps=60
(`projects/bq_closure_lean/q11_witness_v2.py`) to have all three points in the last
branch (`a + λb > 1`), all sub-threshold (`a·b < 1/λ³`), and interior floor `k = 1`
(bracket `λb ≤ 1+a < 2λb`) at the first two points. (An earlier length-4 candidate
from start `(19/61, 22/61)` was REJECTED — see §2 — so no `B(11)=4` claim is made.)

The degree-5 minimal polynomial `λ₁₁⁵ − λ₁₁⁴ − 4λ₁₁³ + 3λ₁₁² + 3λ₁₁ − 1 = 0`
(Aristotle-verified separately) is reproved here via Chebyshev `T₁₁(c) = −1`.

This file inlines the minimal `HeckeRotArc` definitions so it is standalone (it does NOT
import the sealed repo files); the realization datum it produces is exactly the input the
sealed `Bq_eq_rotation_arc` consumes for `q = 11`.
-/

namespace HeckeRotArcQ11

noncomputable section

/-! ## §0.  The inlined `HeckeRotArc` skeleton (verbatim from `BCZHeckeRotationArc.lean`). -/

variable (l : ℝ)

/-- The k=1 last-branch map `M (a,b) = (b, −a + λb)`. -/
def Mmap (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

/-- The genuine last-branch step with floor digit `k`: `(a,b) ↦ (b, −a + kλb)`. -/
def kstep (k : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + k * l * p.2)

/-- The k=1 step IS the rotation `M`. -/
theorem kstep_eq_Mmap_of_k1 (p : ℝ × ℝ) : kstep l 1 p = Mmap l p := by
  simp only [kstep, Mmap]; ring_nf

/-- The genuine last-branch floor digit `k = ⌊(1+a)/(λb)⌋`. -/
def kfloor (p : ℝ × ℝ) : ℤ := ⌊(1 + p.1) / (l * p.2)⌋

/-- Floor characterization (`k = 1 ⟺ bracket`). -/
theorem kfloor_eq_one_iff_bracket (a b : ℝ) (hl0 : 0 < l) (hb : 0 < b) :
    kfloor l (a, b) = 1 ↔ (l * b ≤ 1 + a ∧ 1 + a < 2 * (l * b)) := by
  have hlb : 0 < l * b := mul_pos hl0 hb
  unfold kfloor
  simp only
  rw [Int.floor_eq_iff]
  push_cast
  constructor
  · rintro ⟨h1, h2⟩
    refine ⟨?_, ?_⟩
    · have := (le_div_iff₀ hlb).mp h1; linarith [this]
    · have := (div_lt_iff₀ hlb).mp h2; linarith [this]
  · rintro ⟨h1, h2⟩
    refine ⟨?_, ?_⟩
    · rw [le_div_iff₀ hlb]; linarith
    · rw [div_lt_iff₀ hlb]; linarith

/-- The last-branch observable `P(a,b) = a·b`. -/
def Pobs (p : ℝ × ℝ) : ℝ := p.1 * p.2

/-- A genuine sub-threshold last-branch cluster run of length `N+1`. -/
def IsClusterRun (t : ℝ) (lastBranch : ℝ × ℝ → Prop) (run : ℕ → ℝ × ℝ) (N : ℕ) : Prop :=
  (∀ n, n ≤ N → Pobs (run n) < t ∧ lastBranch (run n)) ∧
  (∀ n, n < N → 0 < (run n).2) ∧
  (∀ n, n < N → run (n + 1) = kstep l ((kfloor l (run n) : ℝ)) (run n)) ∧
  (∀ n, n < N → l * (run n).2 ≤ 1 + (run n).1 ∧ 1 + (run n).1 < 2 * (l * (run n).2))

/-- `clusterCeiling l t lastBranch N` : "`N+1` is achievable as a cluster-run length". -/
def clusterCeiling (t : ℝ) (lastBranch : ℝ × ℝ → Prop) (N : ℕ) : Prop :=
  ∃ run : ℕ → ℝ × ℝ, IsClusterRun l t lastBranch run N

end

/-! ## §1.  `λ₁₁ = 2cos(π/11)`, its degree-5 minimal polynomial, and tight rational bounds. -/

noncomputable section

open Polynomial Polynomial.Chebyshev in
/-- `T`-recurrence specialized to real evaluation. -/
theorem T_real_rec (c : ℝ) (n : ℕ) :
    (T ℝ ((n:ℤ)+2)).eval c = 2*c*(T ℝ ((n:ℤ)+1)).eval c - (T ℝ (n:ℤ)).eval c := by
  rw [Polynomial.Chebyshev.T_add_two ℝ (n : ℤ)]
  simp only [eval_mul, eval_sub, eval_X, eval_ofNat]

open Polynomial Polynomial.Chebyshev in
/-- The explicit degree-11 Chebyshev polynomial `T₁₁` evaluated at a real `c`. -/
theorem T11_eval (c : ℝ) : (T ℝ 11).eval c =
    1024*c^11 - 2816*c^9 + 2816*c^7 - 1232*c^5 + 220*c^3 - 11*c := by
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
  have e11 : (T ℝ (11:ℤ)).eval c =
      1024*c^11 - 2816*c^9 + 2816*c^7 - 1232*c^5 + 220*c^3 - 11*c := by
    have := T_real_rec c 9; norm_num at this; rw [this, e9, e10]; ring
  exact e11

def lam11 : ℝ := 2 * Real.cos (Real.pi / 11)

lemma lam11_pos : 0 < lam11 := by
  unfold lam11
  apply mul_pos (by norm_num : (0:ℝ) < 2)
  exact Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

set_option maxHeartbeats 800000 in
/-- The degree-5 minimal-polynomial identity for `λ₁₁ = 2cos(π/11)`, via `T₁₁(c) = −1`
and the factorization `(λ+2)·minpoly² = 2·(T₁₁(λ/2)+1)`. -/
lemma lam11_minpoly :
    lam11^5 - lam11^4 - 4*lam11^3 + 3*lam11^2 + 3*lam11 - 1 = 0 := by
  set c := Real.cos (Real.pi / 11) with hc
  have hT : (Polynomial.Chebyshev.T ℝ 11).eval c = -1 := by
    rw [hc, Polynomial.Chebyshev.T_real_cos]
    rw [show (11:ℤ) * (Real.pi/11) = Real.pi by push_cast; ring]
    exact Real.cos_pi
  rw [T11_eval] at hT
  have hlam : lam11 = 2 * c := by rw [hc]; rfl
  have hpos : (0:ℝ) < lam11 + 2 := by have := lam11_pos; linarith
  have hfactored : (lam11 + 2) *
      (lam11^5 - lam11^4 - 4*lam11^3 + 3*lam11^2 + 3*lam11 - 1)^2 = 0 := by
    rw [hlam]; linear_combination 2 * hT
  have hsq : (lam11^5 - lam11^4 - 4*lam11^3 + 3*lam11^2 + 3*lam11 - 1)^2 = 0 := by
    rcases mul_eq_zero.mp hfactored with h | h
    · linarith
    · exact h
  exact pow_eq_zero_iff (by norm_num) |>.mp hsq

/-- Power-reduction normal form `λ₁₁⁵ = λ₁₁⁴ + 4λ₁₁³ − 3λ₁₁² − 3λ₁₁ + 1`. -/
lemma lam11_minpoly' :
    lam11^5 = lam11^4 + 4*lam11^3 - 3*lam11^2 - 3*lam11 + 1 := by
  linarith [lam11_minpoly]

/-- `√2 ≤ λ₁₁`, from `cos(π/4) ≤ cos(π/11)`. -/
lemma lam11_ge_sqrt2 : Real.sqrt 2 ≤ lam11 := by
  unfold lam11
  have h_mono : Real.cos (Real.pi / 4) ≤ Real.cos (Real.pi / 11) := by
    apply Real.cos_le_cos_of_nonneg_of_le_pi
    · linarith [Real.pi_pos]
    · linarith [Real.pi_gt_three]
    · apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num : (0:ℝ) < 4)
        (by norm_num : (4:ℝ) ≤ 11)
  have h_cos_pi4 : Real.cos (Real.pi / 4) = Real.sqrt 2 / 2 := by rw [Real.cos_pi_div_four]
  rw [h_cos_pi4] at h_mono
  linarith [mul_le_mul_of_nonneg_left h_mono (by norm_num : (0:ℝ) ≤ 2)]

lemma lam11_gt_one : 1 < lam11 := by
  have h := lam11_ge_sqrt2
  have h1 : 1 < Real.sqrt 2 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp [Real.sqrt_one]]
    exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  linarith

lemma lam11_lt_two : lam11 < 2 := by
  unfold lam11
  have hcos : Real.cos (Real.pi / 11) < 1 := by
    have h := Real.cos_lt_cos_of_nonneg_of_le_pi (le_refl (0:ℝ))
      (by linarith [Real.pi_pos] : Real.pi / 11 ≤ Real.pi)
      (by positivity : (0:ℝ) < Real.pi / 11)
    rwa [Real.cos_zero] at h
  linarith

/-- Crude lower bound `λ₁₁ ≥ 1.414`, i.e. `√2 ≤ λ₁₁`.  This is the ONLY crude lower bound the
minpoly pins below need: among the 5 roots `2cos(kπ/11)`, `k = 1,3,5,7,9` (numerically
`1.91899, 1.30972, 0.28463, −0.83083, −1.68251`), `λ₁₁ = 2cos(π/11)` is the UNIQUE root in the
interval `(√2, 2)` — `√2 ≈ 1.41421` already excludes the next-largest root `1.30972`.  So
`√2 ≤ λ₁₁ < 2` isolates `λ₁₁` and the minpoly pins below succeed from this crude bracket alone. -/
lemma lam11_ge_crude : (1414 : ℝ) / 1000 ≤ lam11 := by
  have h := lam11_ge_sqrt2
  have hs : (1414 : ℝ) / 1000 ≤ Real.sqrt 2 := by
    rw [show (1414 : ℝ) / 1000 = Real.sqrt ((1414/1000)^2) by
      rw [Real.sqrt_sq (by norm_num)]]
    apply Real.sqrt_le_sqrt; norm_num
  linarith

set_option maxHeartbeats 1600000 in
/-- `λ₁₁ > 191898/100000`  (degree-5 minpoly + the larger-root pin `λ₁₁ ≥ 1.91`). -/
lemma lam11_gt : (191898 : ℝ) / 100000 < lam11 := by
  by_contra h
  push_neg at h
  have hmp := lam11_minpoly
  have hge := lam11_ge_crude
  have htwo := lam11_lt_two
  nlinarith [hmp, hge, htwo, h, sq_nonneg lam11, pow_pos lam11_pos 2, pow_pos lam11_pos 3,
    pow_pos lam11_pos 4,
    mul_nonneg (by linarith : (0:ℝ) ≤ lam11 - (1414:ℝ)/1000)
      (by linarith : (0:ℝ) ≤ (191898:ℝ)/100000 - lam11)]

set_option maxHeartbeats 1600000 in
/-- `λ₁₁ < 191899/100000`. -/
lemma lam11_lt : lam11 < (191899 : ℝ) / 100000 := by
  by_contra h
  push_neg at h
  have hmp := lam11_minpoly
  have hge := lam11_ge_crude
  have htwo := lam11_lt_two
  nlinarith [hmp, hge, htwo, h, sq_nonneg lam11, pow_pos lam11_pos 2, pow_pos lam11_pos 3,
    pow_pos lam11_pos 4,
    mul_nonneg (by linarith : (0:ℝ) ≤ lam11 - (191899:ℝ)/100000)
      (by linarith : (0:ℝ) ≤ (2:ℝ) - lam11),
    mul_nonneg (by linarith : (0:ℝ) ≤ lam11 - (191899:ℝ)/100000)
      (by linarith : (0:ℝ) ≤ lam11 - (1414:ℝ)/1000)]

/-! ## §2.  The q=11 witness orbit:  exact rational start `(34/101, 37/101)`, iterated by `M`.

**B(11) = 3** (genuine ground truth, k-pattern `[1,1,2]`): the cluster ceiling for `q = 11` is a
length-3 run, the continuous (no-resonance) count `B₀(11) = ⌊W(11)·11/π⌋ + 1 = 3`.  `q = 11` is
NOT a resonance (scalar gate `R(11) = 0`: `ρ_min ≈ 1.0451 > ρ_max ≈ 1.0211`).

The witness start `(34/101, 37/101)` is a genuine BCZ cross-section domain point (`0 < a ≤ 1`,
`1 − λa < b ≤ 1`), its predecessor `(λa₀−b₀, a₀)` is NOT on the last branch (so `r0` is a genuine
*cluster start*), and the three points `r0, r1 = M r0, r2 = M r1` are all in the last branch,
sub-threshold, with interior floor `k = 1` at `r0, r1`.  Verified at dps=60
(`projects/bq_closure_lean/q11_witness_v2.py`): min last-branch margin ≈ 1.25e−2, min
threshold gap ≈ 7.30e−3, all three valid-domain.

(An earlier length-4 candidate from start `(19/61, 22/61)` was REJECTED: that start fails the
domain condition `b > 1 − λa` and its `M`-orbit leaves the genuine cross-section — a transient,
not a genuine cluster.  This is exactly the check that distinguishes `B(11) = 3` from an
over-count.) -/

/-- `X(11) = 1/λ₁₁³` (the threshold `t = 1/λ³`). -/
def X11 : ℝ := 1 / lam11 ^ 3
lemma lam11_cubed_pos : 0 < lam11 ^ 3 := pow_pos lam11_pos 3

def a0₁₁ : ℝ := 34 / 101
def b0₁₁ : ℝ := 37 / 101
def a1₁₁ : ℝ := 37 / 101
def b1₁₁ : ℝ := (37 / 101) * lam11 - 34 / 101
def a2₁₁ : ℝ := (37 / 101) * lam11 - 34 / 101
def b2₁₁ : ℝ := (37 / 101) * lam11 ^ 2 - (34 / 101) * lam11 - 37 / 101

def run11 : ℕ → ℝ × ℝ
  | 0 => (a0₁₁, b0₁₁)
  | 1 => (a1₁₁, b1₁₁)
  | _ => (a2₁₁, b2₁₁)

def lastBranch11 (p : ℝ × ℝ) : Prop := p.1 + lam11 * p.2 > 1

lemma b0₁₁_pos : 0 < b0₁₁ := by unfold b0₁₁; norm_num
lemma b1₁₁_pos : 0 < b1₁₁ := by unfold b1₁₁; nlinarith [lam11_gt]
lemma b2₁₁_pos : 0 < b2₁₁ := by unfold b2₁₁; nlinarith [lam11_gt, lam11_lt, sq_nonneg lam11]

set_option maxHeartbeats 800000 in
lemma P0₁₁_lt : a0₁₁ * b0₁₁ < X11 := by
  unfold a0₁₁ b0₁₁ X11
  rw [lt_div_iff₀ lam11_cubed_pos]
  -- a0*b0*λ³ = (1258/10201)·λ³
  nlinarith [lam11_gt, lam11_lt, lam11_minpoly', sq_nonneg lam11, lam11_pos,
    pow_pos lam11_pos 2, pow_pos lam11_pos 3]

set_option maxHeartbeats 1200000 in
lemma P1₁₁_lt : a1₁₁ * b1₁₁ < X11 := by
  unfold a1₁₁ b1₁₁ X11
  rw [lt_div_iff₀ lam11_cubed_pos]
  -- a1*b1*λ³ = (1369/10201)·λ⁴ − (1258/10201)·λ³
  have hP1 : ((37:ℝ)/101) * ((37:ℝ)/101 * lam11 - 34/101) * lam11 ^ 3 =
             1369/10201 * lam11^4 - 1258/10201 * lam11^3 := by ring
  rw [hP1]
  nlinarith [lam11_gt, lam11_lt, lam11_minpoly', sq_nonneg lam11, lam11_pos,
    pow_pos lam11_pos 2, pow_pos lam11_pos 3, pow_pos lam11_pos 4]

set_option maxHeartbeats 2000000 in
lemma P2₁₁_lt : a2₁₁ * b2₁₁ < X11 := by
  unfold a2₁₁ b2₁₁ X11
  rw [lt_div_iff₀ lam11_cubed_pos]
  -- reduce (a2*b2)*λ³ mod minpoly to degree ≤ 4
  have hP2 : ((37:ℝ)/101 * lam11 - 34/101) *
      ((37:ℝ)/101 * lam11^2 - 34/101 * lam11 - 37/101) * lam11 ^ 3 =
      (4116/10201 * lam11^4 - 7437/10201 * lam11^3 - 666/10201 * lam11^2
        + 4810/10201 * lam11 - 1147/10201)
      + (1369/10201 * lam11 - 1147/10201) *
        (lam11^5 - lam11^4 - 4*lam11^3 + 3*lam11^2 + 3*lam11 - 1) := by
    ring
  rw [hP2, lam11_minpoly]
  nlinarith [lam11_gt, lam11_lt, lam11_minpoly', sq_nonneg lam11, lam11_pos,
    pow_pos lam11_pos 2, pow_pos lam11_pos 3, pow_pos lam11_pos 4,
    mul_pos lam11_pos lam11_pos]

lemma branch0₁₁ : lastBranch11 (a0₁₁, b0₁₁) := by
  unfold lastBranch11 a0₁₁ b0₁₁; simp only; nlinarith [lam11_gt]
lemma branch1₁₁ : lastBranch11 (a1₁₁, b1₁₁) := by
  unfold lastBranch11 a1₁₁ b1₁₁; simp only; nlinarith [lam11_gt, lam11_lt, sq_nonneg lam11]
lemma branch2₁₁ : lastBranch11 (a2₁₁, b2₁₁) := by
  unfold lastBranch11 a2₁₁ b2₁₁; simp only
  nlinarith [lam11_gt, lam11_lt, lam11_minpoly', sq_nonneg lam11, pow_pos lam11_pos 2]

lemma bracket0₁₁ : lam11 * b0₁₁ ≤ 1 + a0₁₁ ∧ 1 + a0₁₁ < 2 * (lam11 * b0₁₁) := by
  unfold a0₁₁ b0₁₁
  exact ⟨by nlinarith [lam11_lt], by nlinarith [lam11_gt]⟩

lemma bracket1₁₁ : lam11 * b1₁₁ ≤ 1 + a1₁₁ ∧ 1 + a1₁₁ < 2 * (lam11 * b1₁₁) := by
  unfold a1₁₁ b1₁₁
  exact ⟨by nlinarith [lam11_gt, lam11_lt, sq_nonneg lam11],
         by nlinarith [lam11_gt, lam11_lt, sq_nonneg lam11]⟩

lemma kfloor0₁₁ : kfloor lam11 (a0₁₁, b0₁₁) = 1 :=
  (kfloor_eq_one_iff_bracket lam11 a0₁₁ b0₁₁ lam11_pos b0₁₁_pos).mpr bracket0₁₁
lemma kfloor1₁₁ : kfloor lam11 (a1₁₁, b1₁₁) = 1 :=
  (kfloor_eq_one_iff_bracket lam11 a1₁₁ b1₁₁ lam11_pos b1₁₁_pos).mpr bracket1₁₁

lemma step0₁₁ : run11 1 = kstep lam11 ((kfloor lam11 (run11 0) : ℝ)) (run11 0) := by
  show (a1₁₁, b1₁₁) = kstep lam11 ((kfloor lam11 (a0₁₁, b0₁₁) : ℝ)) (a0₁₁, b0₁₁)
  rw [kfloor0₁₁]; push_cast
  rw [kstep_eq_Mmap_of_k1]
  show (a1₁₁, b1₁₁) = Mmap lam11 (a0₁₁, b0₁₁)
  refine Prod.ext ?_ ?_
  · show a1₁₁ = b0₁₁; unfold a1₁₁ b0₁₁; norm_num
  · show b1₁₁ = -a0₁₁ + lam11 * b0₁₁; unfold b1₁₁ a0₁₁ b0₁₁; ring

lemma step1₁₁ : run11 2 = kstep lam11 ((kfloor lam11 (run11 1) : ℝ)) (run11 1) := by
  show (a2₁₁, b2₁₁) = kstep lam11 ((kfloor lam11 (a1₁₁, b1₁₁) : ℝ)) (a1₁₁, b1₁₁)
  rw [kfloor1₁₁]; push_cast
  rw [kstep_eq_Mmap_of_k1]
  show (a2₁₁, b2₁₁) = Mmap lam11 (a1₁₁, b1₁₁)
  refine Prod.ext ?_ ?_
  · show a2₁₁ = b1₁₁; unfold a2₁₁ b1₁₁; rfl
  · show b2₁₁ = -a1₁₁ + lam11 * b1₁₁; unfold b2₁₁ a1₁₁ b1₁₁; ring

/-- **★ The q=11 cluster run is a genuine length-3 sub-threshold last-branch cluster (k=1 interior).** -/
theorem run11_isClusterRun : IsClusterRun lam11 X11 lastBranch11 run11 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro n hn; interval_cases n
    · exact ⟨P0₁₁_lt, branch0₁₁⟩
    · exact ⟨P1₁₁_lt, branch1₁₁⟩
    · exact ⟨P2₁₁_lt, branch2₁₁⟩
  · intro n hn; interval_cases n
    · exact b0₁₁_pos
    · exact b1₁₁_pos
  · intro n hn; interval_cases n
    · exact step0₁₁
    · exact step1₁₁
  · intro n hn; interval_cases n
    · exact bracket0₁₁
    · exact bracket1₁₁

/-- **★ THE q=11 REALIZATION DATUM — discharges `hrealize` for q=11 (residual R2).**
A genuine sub-threshold last-branch cluster run of length `3` exists; this realizes
`B(11) = 3` and is exactly the input the sealed `Bq_eq_rotation_arc` consumes. -/
theorem clusterCeiling11 : clusterCeiling lam11 X11 lastBranch11 2 :=
  ⟨run11, run11_isClusterRun⟩

end

end HeckeRotArcQ11

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeRotArcQ11.lam11_minpoly
#print axioms HeckeRotArcQ11.run11_isClusterRun
#print axioms HeckeRotArcQ11.clusterCeiling11
