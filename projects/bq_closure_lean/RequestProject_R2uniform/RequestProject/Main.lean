import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# R2 UNIFORM realization witness family for the B(q) rotation-arc theorem.

This file targets the single OPEN residual that would advance the `B(q)` rotation-arc
theorem toward closure: the **uniform-all-q realization witness family** (residual R2).

## Background

The `B(q)` theorem (sealed repo files `BCZHeckeRotationArc*.lean`) reduces the cluster
ceiling `B(q)` for the Rosen continued-fraction / Hecke `G_q` last-branch observable to the
length of an `M`-rotation arc on the conserved ellipse, where
`M (a,b) = (b, -a + λ b)` is the elliptic rotation by `-π/q` (`λ = 2cos(π/q)`). The forward
direction `cluster ⟹ rotation arc` (`cluster_le_rotation_arc`) is machine-verified. The
remaining **R2** residual is the *realization bridge* `hrealize`: exhibit an actual genuine
sub-threshold last-branch cluster run of the claimed length.

R2 has been discharged **per-q** (sealed, axiom-clean) for `q ∈ {7,8,9,10,11,12,13}` (and a
lower bound `B(5) ≥ 3`) — each via a hand-picked rational start `(a₀,b₀) ∈ Q(λ_q)²` with NO
closed form in `q`. The genuinely OPEN piece is a SINGLE uniform construction
`λ ↦ (a₀(λ), b₀(λ))` that realizes a genuine length-3 cluster for ALL `q` in a range. This
file supplies exactly that.

## The uniform witness family (this file's contribution)

For the conserved-ellipse rotation `M`, a length-3 arc that is **symmetric** about its middle
point is, taking the middle on the diagonal `r₁ = (s,s)`:

  r₀ = M⁻¹ r₁ = (s·(λ−1), s),   r₁ = (s, s),   r₂ = M r₁ = (s, s·(λ−1)).

(These three identities are exact `ring` facts under `M`.) The single SCALE function

  **s(λ) = (1104 − 385·λ)/1000**

makes all of the following hold UNIFORMLY for every real `λ ∈ [9/5, 199/100] = [1.8, 1.99]`
(verified continuously at dps=40, worst margin ≈ 2.5e−3):

  * sub-threshold:        `P(rᵢ) < 1/λ³`   (`P(r₀)=P(r₂)=s²(λ−1)`, `P(r₁)=s²`);
  * last-branch:          `aᵢ + λ·bᵢ > 1`;
  * cross-section domain: `0 < aᵢ ≤ 1`, `1 − λ·aᵢ < bᵢ ≤ 1`;
  * interior floor `k=1`: `λ·bᵢ ≤ 1+aᵢ < 2λ·bᵢ` at `r₀, r₁`;
  * genuine cluster start: predecessor `(λa₀−b₀, a₀)` is NOT last-branch.

The interval `[1.8, 1.99]` contains `λ_q = 2cos(π/q)` for **q = 7 .. 31** (since
`λ₇ = 1.80194 > 1.8` and `λ₃₁ = 1.98904 < 1.99`), so the SAME explicit construction realizes
a genuine length-3 sub-threshold last-branch `k=1` cluster for every one of those Hecke groups
at once. In particular it reproduces the per-q proved `clusterCeiling7 .. clusterCeiling13`
(the entire proved block) from ONE formula — this is the uniform lower bound `B(q) ≥ 3`.

## What this file proves (target)

`uniform_clusterCeiling`:
  for every real `l` with `9/5 ≤ l ≤ 199/100`,
  `clusterCeiling l (1/l^3) (lastBranch l) 2` holds,
i.e. there is a genuine sub-threshold last-branch cluster run of length `3` (interior `k=1`).
This is the realization residual (R2) discharged UNIFORMLY over the whole `λ`-interval, hence
for all the Hecke values `λ_q`, `q = 7..31`, simultaneously — strictly stronger than any
per-q fact.

SCOPE: this is the LOWER bound `B(q) ≥ 3` (a length-3 cluster EXISTS, uniformly). It does NOT
prove maximality. It does NOT cover the resonance q's (`q ≥ 23` resonances `{23,61,…}` where
`B(q)` exceeds the continuous count) — there length-3 is still a valid lower bound, just not
tight. The interval is closed in `λ`; the construction is the same continuous family for all
`λ` in it, so specializing to any `λ_q` in range is immediate.

The `HeckeRotArc` skeleton (`Mmap`, `kstep`, `kfloor`, `kfloor_eq_one_iff_bracket`, `Pobs`,
`IsClusterRun`, `clusterCeiling`) is inlined VERBATIM from `BCZHeckeRotationArc.lean`, so the
realization datum produced here is exactly the input the sealed `Bq_eq_rotation_arc` consumes.
-/

namespace HeckeRotArcR2Uniform

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

/-! ## §1.  The uniform witness family.

Scale function `s(l) = (1104 − 385·l)/1000`.  Run points (symmetric `M`-arc):
`r₀ = (s·(l−1), s)`, `r₁ = (s, s)`, `r₂ = (s, s·(l−1))`.
`lastBranch l p := p.1 + l·p.2 > 1`, threshold `t = 1/l³`. -/

noncomputable section

/-- The uniform scale function `s(l) = (1104 − 385 l)/1000`. -/
def swit (l : ℝ) : ℝ := (1104 - 385 * l) / 1000

/-- The genuine BCZ last-branch predicate `a + l·b > 1`. -/
def lastBranch (l : ℝ) (p : ℝ × ℝ) : Prop := p.1 + l * p.2 > 1

/-- The three explicit witness points as functions of `l`. -/
def r0w (l : ℝ) : ℝ × ℝ := (swit l * (l - 1), swit l)
def r1w (l : ℝ) : ℝ × ℝ := (swit l, swit l)
def r2w (l : ℝ) : ℝ × ℝ := (swit l, swit l * (l - 1))

/-- The realizing run: `r₀, r₁, r₂`, constant afterwards (only `n ≤ N = 2` matters). -/
def runw (l : ℝ) : ℕ → ℝ × ℝ
  | 0 => r0w l
  | 1 => r1w l
  | _ => r2w l

/-! ### §1a.  Interval hypotheses and basic bounds on `s(l)`. -/

variable {l : ℝ}

/-- On `[9/5, 199/100]`, `1 < l`. -/
lemma l_gt_one (hlo : 9/5 ≤ l) : 1 < l := by linarith

/-- On `[9/5, 199/100]`, `s(l) > 0`. -/
lemma swit_pos (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : 0 < swit l := by
  unfold swit; rw [lt_div_iff₀ (by norm_num : (0:ℝ) < 1000)]; nlinarith

/-- `s(l) < 1` on the interval (so the `b`-coordinates are `≤ 1`). -/
lemma swit_lt_one (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : swit l < 1 := by
  unfold swit; rw [div_lt_iff₀ (by norm_num : (0:ℝ) < 1000)]; nlinarith

end

/-! ## §2.  Uniform certificates for the 9 cluster conditions.

Each is a polynomial inequality in `l` (and the rational `s(l)`) that holds for all
`l ∈ [9/5, 199/100]`.  These are the genuinely-uniform facts — proven once for the whole
interval, not per-q. -/

noncomputable section
variable {l : ℝ}

/-- `b`-coordinate of `r₀`, `r₁` is `s(l) > 0`. -/
lemma b0_pos (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : 0 < (r0w l).2 := by
  show 0 < swit l; exact swit_pos hlo hhi
lemma b1_pos (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : 0 < (r1w l).2 := by
  show 0 < swit l; exact swit_pos hlo hhi

/-! ### Sub-threshold `P(rᵢ) < 1/l³`.  `P(r₀)=P(r₂)=s²(l−1)`, `P(r₁)=s²`. -/

/-- The two interval-bound nonneg factors and their product — the standard `nlinarith`
witnesses for a polynomial positive on `[9/5, 199/100]`. -/
lemma hL (hlo : 9/5 ≤ l) : (0:ℝ) ≤ l - 9/5 := by linarith
lemma hU (hhi : l ≤ 199/100) : (0:ℝ) ≤ 199/100 - l := by linarith

set_option maxHeartbeats 1600000 in
lemma sub0 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : Pobs (r0w l) < 1 / l ^ 3 := by
  have hl3 : 0 < l ^ 3 := by positivity
  have hl1 : (1:ℝ) < l := by linarith
  show swit l * (l - 1) * swit l < 1 / l ^ 3
  rw [lt_div_iff₀ hl3]; unfold swit
  nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l, sq_nonneg (l-1),
    mul_nonneg (mul_nonneg (hL hlo) (hU hhi)) (le_of_lt hl3),
    mul_nonneg (hL hlo) (le_of_lt hl3), mul_nonneg (hU hhi) (le_of_lt hl3),
    mul_pos hl3 hl3, hl1.le]

set_option maxHeartbeats 1600000 in
lemma sub1 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : Pobs (r1w l) < 1 / l ^ 3 := by
  have hl3 : 0 < l ^ 3 := by positivity
  show swit l * swit l < 1 / l ^ 3
  rw [lt_div_iff₀ hl3]; unfold swit
  nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l, sq_nonneg (l-1),
    mul_nonneg (mul_nonneg (hL hlo) (hU hhi)) (le_of_lt hl3),
    mul_nonneg (hL hlo) (le_of_lt hl3), mul_nonneg (hU hhi) (le_of_lt hl3), hl3.le]

set_option maxHeartbeats 1600000 in
lemma sub2 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : Pobs (r2w l) < 1 / l ^ 3 := by
  have hl3 : 0 < l ^ 3 := by positivity
  have hl1 : (1:ℝ) < l := by linarith
  show swit l * (swit l * (l - 1)) < 1 / l ^ 3
  rw [lt_div_iff₀ hl3]; unfold swit
  nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l, sq_nonneg (l-1),
    mul_nonneg (mul_nonneg (hL hlo) (hU hhi)) (le_of_lt hl3),
    mul_nonneg (hL hlo) (le_of_lt hl3), mul_nonneg (hU hhi) (le_of_lt hl3),
    mul_pos hl3 hl3, hl1.le]

/-! ### Last-branch `aᵢ + l·bᵢ > 1`. -/

lemma br0 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : lastBranch l (r0w l) := by
  show swit l * (l - 1) + l * swit l > 1
  unfold swit; rw [gt_iff_lt]
  nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l]
lemma br1 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : lastBranch l (r1w l) := by
  show swit l + l * swit l > 1
  unfold swit; rw [gt_iff_lt]
  nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l]
lemma br2 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : lastBranch l (r2w l) := by
  show swit l + l * (swit l * (l - 1)) > 1
  unfold swit; rw [gt_iff_lt]
  nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l, sq_nonneg (l-1),
    mul_nonneg (mul_nonneg (hL hlo) (hU hhi)) (hL hlo)]

/-! ### Interior `k=1` bracket `l·bᵢ ≤ 1+aᵢ < 2 l bᵢ` at `r₀, r₁`. -/

lemma bracket0 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) :
    l * (r0w l).2 ≤ 1 + (r0w l).1 ∧ 1 + (r0w l).1 < 2 * (l * (r0w l).2) := by
  show l * swit l ≤ 1 + swit l * (l - 1) ∧ 1 + swit l * (l - 1) < 2 * (l * swit l)
  unfold swit
  refine ⟨?_, ?_⟩
  · nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l]
  · nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l]

lemma bracket1 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) :
    l * (r1w l).2 ≤ 1 + (r1w l).1 ∧ 1 + (r1w l).1 < 2 * (l * (r1w l).2) := by
  show l * swit l ≤ 1 + swit l ∧ 1 + swit l < 2 * (l * swit l)
  unfold swit
  refine ⟨?_, ?_⟩
  · nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l]
  · nlinarith [hL hlo, hU hhi, mul_nonneg (hL hlo) (hU hhi), sq_nonneg l]

/-! ### The genuine steps are the rotation `M` (k = 1).  Exact `ring` identities. -/

lemma kfloor0 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : kfloor l (r0w l) = 1 :=
  (kfloor_eq_one_iff_bracket l (r0w l).1 (r0w l).2 (by linarith [l_gt_one hlo])
    (b0_pos hlo hhi)).mpr (bracket0 hlo hhi)

lemma kfloor1 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) : kfloor l (r1w l) = 1 :=
  (kfloor_eq_one_iff_bracket l (r1w l).1 (r1w l).2 (by linarith [l_gt_one hlo])
    (b1_pos hlo hhi)).mpr (bracket1 hlo hhi)

lemma step0 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) :
    runw l 1 = kstep l ((kfloor l (runw l 0) : ℝ)) (runw l 0) := by
  show r1w l = kstep l ((kfloor l (r0w l) : ℝ)) (r0w l)
  rw [kfloor0 hlo hhi]; push_cast
  rw [kstep_eq_Mmap_of_k1]
  show r1w l = Mmap l (r0w l)
  refine Prod.ext ?_ ?_
  · show swit l = swit l; rfl
  · show swit l = -(swit l * (l - 1)) + l * swit l; ring

lemma step1 (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) :
    runw l 2 = kstep l ((kfloor l (runw l 1) : ℝ)) (runw l 1) := by
  show r2w l = kstep l ((kfloor l (r1w l) : ℝ)) (r1w l)
  rw [kfloor1 hlo hhi]; push_cast
  rw [kstep_eq_Mmap_of_k1]
  show r2w l = Mmap l (r1w l)
  refine Prod.ext ?_ ?_
  · show swit l = swit l; rfl
  · show swit l * (l - 1) = -swit l + l * swit l; ring

/-! ## §3.  Assemble the uniform `IsClusterRun` and `clusterCeiling`. -/

set_option maxHeartbeats 2000000 in
/-- **★ The uniform run is a genuine length-3 sub-threshold last-branch cluster (`k=1` interior)
for EVERY `l ∈ [9/5, 199/100]`.** -/
theorem runw_isClusterRun (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) :
    IsClusterRun l (1 / l ^ 3) (lastBranch l) (runw l) 2 := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro n hn; interval_cases n
    · exact ⟨sub0 hlo hhi, br0 hlo hhi⟩
    · exact ⟨sub1 hlo hhi, br1 hlo hhi⟩
    · exact ⟨sub2 hlo hhi, br2 hlo hhi⟩
  · intro n hn; interval_cases n
    · exact b0_pos hlo hhi
    · exact b1_pos hlo hhi
  · intro n hn; interval_cases n
    · exact step0 hlo hhi
    · exact step1 hlo hhi
  · intro n hn; interval_cases n
    · exact bracket0 hlo hhi
    · exact bracket1 hlo hhi

/-- **★ THE R2 UNIFORM REALIZATION DATUM.**  For EVERY real `l ∈ [9/5, 199/100]` there is a
genuine sub-threshold last-branch cluster run of length `3`.  This is the realization residual
(R2) discharged UNIFORMLY: ONE explicit family `l ↦ (s(l)(l−1), s(l))` works for the whole
`λ`-interval, hence for every Hecke value `λ_q = 2cos(π/q)` with `q = 7..31` simultaneously.
It is exactly the `hrealize` input the sealed `Bq_eq_rotation_arc` consumes, now supplied by
a single closed form rather than per-q. -/
theorem uniform_clusterCeiling (hlo : 9/5 ≤ l) (hhi : l ≤ 199/100) :
    clusterCeiling l (1 / l ^ 3) (lastBranch l) 2 :=
  ⟨runw l, runw_isClusterRun hlo hhi⟩

end

/-! ## §4.  Hecke specialization — the genuine point of the uniform family.

For any `q` whose `λ_q = 2cos(π/q)` lands in `[9/5, 199/100]`, the uniform family gives the
realization datum.  We give the generic specialization and the q=11 anchor (which must match
the separately-proved `clusterCeiling11`). -/

noncomputable section

/-- **★ Hecke specialization.**  If `λ = 2cos(π/q)` lies in `[9/5, 199/100]` (equivalently
`q = 7..31`), the uniform family realizes a genuine length-3 cluster for that Hecke group:
`clusterCeiling λ (1/λ³) (lastBranch λ) 2`.  This recovers the per-q proved
`clusterCeiling7 .. clusterCeiling13` (and q=14..31) from ONE formula. -/
theorem hecke_clusterCeiling (lq : ℝ) (hlo : 9/5 ≤ lq) (hhi : lq ≤ 199/100) :
    clusterCeiling lq (1 / lq ^ 3) (lastBranch lq) 2 :=
  uniform_clusterCeiling hlo hhi

/-! ### λ₁₁ = 2cos(π/11) lands in the interval — minpoly bracket (ported from the proved
q=11 realization file, so the anchor is itself `sorry`-free). -/

/-- `λ₁₁ = 2cos(π/11)`. -/
def lam11 : ℝ := 2 * Real.cos (Real.pi / 11)

lemma lam11_pos : 0 < lam11 := by
  unfold lam11
  apply mul_pos (by norm_num : (0:ℝ) < 2)
  exact Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩

open Polynomial Polynomial.Chebyshev in
/-- `T`-recurrence specialized to real evaluation. -/
theorem T_real_rec (c : ℝ) (n : ℕ) :
    (T ℝ ((n:ℤ)+2)).eval c = 2*c*(T ℝ ((n:ℤ)+1)).eval c - (T ℝ (n:ℤ)).eval c := by
  rw [Polynomial.Chebyshev.T_add_two ℝ (n : ℤ)]
  simp only [eval_mul, eval_sub, eval_X, eval_ofNat]

open Polynomial Polynomial.Chebyshev in
/-- `T₁₁` at a real `c`. -/
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

set_option maxHeartbeats 800000 in
/-- Degree-5 minpoly identity for `λ₁₁`. -/
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

/-- `√2 ≤ λ₁₁` (from `cos(π/4) ≤ cos(π/11)`). -/
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

lemma lam11_lt_two : lam11 < 2 := by
  unfold lam11
  have hcos : Real.cos (Real.pi / 11) < 1 := by
    have h := Real.cos_lt_cos_of_nonneg_of_le_pi (le_refl (0:ℝ))
      (by linarith [Real.pi_pos] : Real.pi / 11 ≤ Real.pi)
      (by positivity : (0:ℝ) < Real.pi / 11)
    rwa [Real.cos_zero] at h
  linarith

lemma lam11_ge_crude : (1414 : ℝ) / 1000 ≤ lam11 := by
  have h := lam11_ge_sqrt2
  have hs : (1414 : ℝ) / 1000 ≤ Real.sqrt 2 := by
    rw [show (1414 : ℝ) / 1000 = Real.sqrt ((1414/1000)^2) by
      rw [Real.sqrt_sq (by norm_num)]]
    apply Real.sqrt_le_sqrt; norm_num
  linarith

set_option maxHeartbeats 1600000 in
/-- `λ₁₁ > 191898/100000` — so `9/5 = 1.8 ≤ λ₁₁`. -/
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
/-- `λ₁₁ < 191899/100000` — so `λ₁₁ ≤ 199/100 = 1.99`. -/
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

/-- **★ q=11 ANCHOR (faithfulness check, `sorry`-free).**  `λ₁₁ = 2cos(π/11) ∈ [9/5, 199/100]`
(`λ₁₁ ≈ 1.91899`), so the uniform family produces the q=11 realization datum — the SAME
conclusion shape as the independently-proved `clusterCeiling11` (length-3, `B(11) ≥ 3`),
now from the uniform construction.  This is the instantiation that confirms the uniform
statement is non-vacuous and matches the proven per-q fact. -/
theorem clusterCeiling11_uniform :
    clusterCeiling lam11 (1 / lam11 ^ 3) (lastBranch lam11) 2 := by
  apply hecke_clusterCeiling
  · -- 9/5 ≤ λ₁₁ :  λ₁₁ > 191898/100000 = 1.91898 > 1.8 = 9/5
    have := lam11_gt; norm_num; linarith
  · -- λ₁₁ ≤ 199/100 :  λ₁₁ < 191899/100000 = 1.91899 < 1.99 = 199/100
    have := lam11_lt; norm_num; linarith

end

end HeckeRotArcR2Uniform

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeRotArcR2Uniform.runw_isClusterRun
#print axioms HeckeRotArcR2Uniform.uniform_clusterCeiling
#print axioms HeckeRotArcR2Uniform.hecke_clusterCeiling
#print axioms HeckeRotArcR2Uniform.clusterCeiling11_uniform
