import Mathlib
/-!
# L1b Arc-Coverage — B1 sub-obligations toward L1b_target

This file works toward proving

  **L1b_target**: ∀ q ≥ 18, 1/λ³ ≤ g_corr(L_blk q, q)

where `g_corr(L,q) = sInf_{μc ∈ (-(π/2-H), π/2-H)} fcorr(L,q,μc)` and
`fcorr(L,q,μc) = (3λ/2 + √A₂ · windowMaxCos(L,q,μc)) / (2·A₂·Blam²·cos²(|μc|+H))`.

## What is PROVED here (sorry-free)

1. **cos_sq_lt**: `cos(33π/512)² < 24/25`  (re-proved from L1bTrigCore)
2. **H_lt_half_pi**: H(L_blk q, q) < π/2 for all q ≥ 18
3. **denom_cos_pos**: cos(|μc|+H) > 0 for μc in domain
4. **arc_coverage_ineq**: `2·arccos(2√6/5)/π < 33/256`

## Corrected / removed

5. **windowMaxCos_lb** (windowMaxCos ≥ 2√6/5): **FALSE** — removed (commented out).
   windowMaxCos drops to ≈ -0.68 near the domain endpoints; the arc-coverage
   pigeonhole bound does not hold uniformly.  See the note where it stood.

## What is now PROVED (2026-06-14, sorry-free — the file has NO remaining sorry)

6. **fcorr_lb**: fcorr ≥ 1/λ³ pointwise on domain.  PROVED via the two pointwise cores
   `regimeA_all` (q≥18, the razor-thin q-uniform core tied to `cos_sq_lt`) and
   `regimeB_ondomain` (endpoint), assembled with the `pigeon_idx` window-index
   pigeonhole, `eta_ge_2xi` (2ξ≤η, for the μc<0 endpoint), and the denominator
   reduction.  See `section RegimeCores`.
7. **B1_target**: sInf ≥ 1/λ³ — PROVED (csInf reduction + fcorr_lb).

AXIOMS on all results incl. fcorr_lb / B1_target: [propext, Classical.choice, Quot.sound]
(sorryAx GONE — verified by `#print axioms`).

Helper `arg_eq_arctan` (Complex.arg → Real.arctan for positive real part) is proved
below for use in the ξ/η correction bounds.
-/

namespace L1bArcCoverage

noncomputable section

open Real

/-! ### Skeleton definitions (self-contained copy) -/

/-- `θ = π/q`. -/
def thetaq (q : ℕ) : ℝ := Real.pi / q

/-- `λ = 2 cos(π/q)`. -/
def lamq (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)

/-- `A2 = 1 + 2λ²`. -/
def A2q (q : ℕ) : ℝ := 1 + 2 * lamq q ^ 2

/-- `atan2 y x`, via `Complex.arg`. -/
def atan2' (y x : ℝ) : ℝ := Complex.arg ⟨x, y⟩

/-- `η = atan2(sin θ, 3 cos θ)`. -/
def etaq (q : ℕ) : ℝ := atan2' (Real.sin (thetaq q)) (3 * Real.cos (thetaq q))

/-- `Blam = √(12λ⁴+8λ²+1)/(2λ²+1)`. -/
def Blamq (q : ℕ) : ℝ :=
  Real.sqrt (12 * lamq q ^ 4 + 8 * lamq q ^ 2 + 1) / (2 * lamq q ^ 2 + 1)

/-- `ξ = atan2(λ sin θ, 3λ²+1+λ cos θ)`. -/
def xiq (q : ℕ) : ℝ :=
  atan2' (lamq q * Real.sin (thetaq q))
        (3 * lamq q ^ 2 + 1 + lamq q * Real.cos (thetaq q))

/-- `H = (L-1)·θ/2`. -/
def Hq (L q : ℕ) : ℝ := ((L : ℝ) - 1) * thetaq q / 2

/-- `L_blk q = ⌈33q/256⌉.toNat + 2`. -/
def L_blk (q : ℕ) : ℕ := ⌈(33 * q : ℝ) / 256⌉.toNat + 2

/-- Window-max cosine. -/
def windowMaxCos (L q : ℕ) (hL : 0 < L) (muc : ℝ) : ℝ :=
  (Finset.range L).sup' (Finset.nonempty_range_iff.mpr (by omega))
    (fun n => Real.cos (2 * (muc - xiq q) + ((2 * (n : ℝ) - ((L : ℝ) - 1)) * thetaq q) + etaq q))

/-- Pointwise functional. -/
def fcorr (L q : ℕ) (hL : 0 < L) (muc : ℝ) : ℝ :=
  (3 * lamq q / 2 + Real.sqrt (A2q q) * windowMaxCos L q hL muc)
    / (2 * A2q q * Blamq q ^ 2 * Real.cos (|muc| + Hq L q) ^ 2)

/-- g_corr = sInf of fcorr over the open domain. -/
def g_corr (L q : ℕ) (hL : 0 < L) : ℝ :=
  sInf (Set.image (fcorr L q hL)
        (Set.Ioo (-(Real.pi / 2 - Hq L q)) (Real.pi / 2 - Hq L q)))

/-! ### B0: cos²(33π/512) < 24/25 -/

/-- **PROVED (0 sorry)**: cos²(33π/512) < 24/25.
    This is a copy of `L1bTrig.cos_sq_lt` from `L1bTrigCore.lean`. -/
theorem cos_sq_lt : Real.cos (33 * Real.pi / 512) ^ 2 < 24 / 25 := by
  have hpi_lo : (3.1415 : ℝ) < Real.pi := Real.pi_gt_d4
  have hpi_hi : Real.pi < (3.1416 : ℝ) := Real.pi_lt_d4
  set x := 33 * Real.pi / 512 with hx_def
  have hx_pos : (0 : ℝ) < x := by rw [hx_def]; linarith [Real.pi_pos]
  have hx_lo : (207339 : ℝ) / 1024000 ≤ x := by rw [hx_def]; linarith
  have hx_hi : x ≤ (129591 : ℝ) / 640000 := by rw [hx_def]; linarith
  have hx_lt1 : x < 1 := by linarith
  set a := x ^ 2 with ha_def
  have ha_pos : (0 : ℝ) < a := by rw [ha_def]; positivity
  have ha_lo : (42989460921 : ℝ) / 1048576000000 ≤ a := by
    rw [ha_def]
    nlinarith [sq_nonneg x, sq_nonneg ((207339 : ℝ) / 1024000),
               mul_pos (show (0:ℝ) < 207339/1024000 by norm_num) hx_pos]
  have ha_hi : a ≤ (16793827281 : ℝ) / 409600000000 := by
    rw [ha_def]
    nlinarith [sq_nonneg ((129591:ℝ)/640000 - x), hx_hi, hx_pos.le,
               mul_pos hx_pos hx_pos]
  have habs : |x| ≤ 1 := by rw [abs_of_pos hx_pos]; linarith
  have hcb := Real.cos_bound habs
  rw [abs_le] at hcb
  have habs4 : |x| ^ 4 = a ^ 2 := by rw [ha_def, abs_of_pos hx_pos]; ring
  rw [habs4] at hcb
  have hcos_ub : Real.cos x ≤ 1 - a / 2 + a ^ 2 * (5 / 96) := by
    rw [ha_def]; linarith [hcb.2]
  have hcos_nn : (0 : ℝ) ≤ Real.cos x := by
    apply Real.cos_nonneg_of_mem_Icc
    constructor
    · linarith
    · rw [hx_def]; linarith
  have hU_nn : (0 : ℝ) ≤ 1 - a / 2 + a ^ 2 * (5 / 96) := by linarith [hcos_nn, hcos_ub]
  have hcos2_ub : Real.cos x ^ 2 ≤ (1 - a / 2 + a ^ 2 * (5 / 96)) ^ 2 := by
    apply sq_le_sq'
    · linarith [hcos_nn]
    · exact hcos_ub
  have hpoly : (24 : ℝ) / 25 - (1 - a / 2 + a ^ 2 * (5 / 96)) ^ 2 > 0 := by
    nlinarith [ha_lo, ha_hi, sq_nonneg a, sq_nonneg (a - 42989460921 / 1048576000000),
               mul_nonneg ha_pos.le ha_pos.le,
               mul_nonneg (mul_nonneg ha_pos.le ha_pos.le) ha_pos.le,
               mul_pos ha_pos ha_pos]
  linarith [hcos2_ub, hpoly]

/-! ### H_lt_half_pi -/

/-- **PROVED (0 sorry)**: For q ≥ 18, H(L_blk q, q) < π/2. -/
theorem H_lt_half_pi (q : ℕ) (hq : 18 ≤ q) : Hq (L_blk q) q < Real.pi / 2 := by
  unfold Hq thetaq L_blk
  have hpi_pos : (0 : ℝ) < Real.pi := Real.pi_pos
  have hq_pos : (0 : ℝ) < (q : ℝ) := by exact_mod_cast Nat.pos_of_ne_zero (by omega)
  -- We need: ((⌈33q/256⌉.toNat + 2 : ℝ) - 1) * (π/q) / 2 < π/2
  -- i.e. (⌈33q/256⌉.toNat + 1) * (π/q) < π
  -- i.e. ⌈33q/256⌉.toNat + 1 < q
  -- Since 33q/256 < q and ⌈33q/256⌉ ≤ q-1 for q ≥ 1, we get ⌈33q/256⌉.toNat ≤ q-1.
  -- Actually we need ⌈33q/256⌉.toNat + 1 < q, i.e. ⌈33q/256⌉.toNat ≤ q - 2.
  -- For q ≥ 18: 33q/256 ≤ 33*18/256 = 594/256 < 3, so ⌈33q/256⌉ ≤ ceil(33q/256).
  -- More carefully: ⌈33q/256⌉ ≤ ⌊33q/256⌋ + 1 ≤ 33q/256 + 1.
  -- Need: 33q/256 + 1 ≤ q - 2, i.e. 3 ≤ q(1 - 33/256) = q*223/256.
  -- For q ≥ 18: 18*223/256 = 4014/256 > 15 > 3. ✓
  have hceil_bd : ⌈(33 * (q : ℝ)) / 256⌉ ≤ (q : ℤ) - 2 := by
    apply Int.ceil_le.mpr
    push_cast
    have : (q : ℝ) ≥ 18 := by exact_mod_cast hq
    linarith
  have hceil_nn : 0 ≤ ⌈(33 * (q : ℝ)) / 256⌉ := by
    apply Int.ceil_nonneg
    positivity
  have hceil_nat_bd : ⌈(33 * (q : ℝ)) / 256⌉.toNat ≤ q - 2 := by
    omega
  -- So ⌈33q/256⌉.toNat + 1 ≤ q - 1 < q
  have hstrict : ⌈(33 * (q : ℝ)) / 256⌉.toNat + 1 < q := by omega
  -- The actual bound:
  have hLcast : ((⌈(33 * (q : ℝ)) / 256⌉.toNat + 2 : ℕ) : ℝ) - 1 =
      (⌈(33 * (q : ℝ)) / 256⌉.toNat : ℝ) + 1 := by push_cast; ring
  rw [hLcast]
  have hbound : (⌈(33 * (q : ℝ)) / 256⌉.toNat : ℝ) + 1 < (q : ℝ) := by exact_mod_cast hstrict
  -- H = (ceil.toNat + 1) * (π/q) / 2 < q * (π/q) / 2 = π/2
  calc ((⌈(33 * (q : ℝ)) / 256⌉.toNat : ℝ) + 1) * (Real.pi / ↑q) / 2
      < (q : ℝ) * (Real.pi / ↑q) / 2 := by
        apply div_lt_div_of_pos_right _ (by norm_num)
        exact mul_lt_mul_of_pos_right hbound (div_pos hpi_pos hq_pos)
    _ = Real.pi / 2 := by
        field_simp

/-! ### Denominator positivity -/

/-- **PROVED (0 sorry)**: cos(|μc|+H) > 0 for μc in the domain, H ∈ [0, π/2). -/
theorem denom_cos_pos {H : ℝ} (hH_pos : 0 ≤ H) (hH_lt : H < Real.pi / 2)
    {muc : ℝ} (hmuc : muc ∈ Set.Ioo (-(Real.pi / 2 - H)) (Real.pi / 2 - H)) :
    0 < Real.cos (|muc| + H) := by
  apply Real.cos_pos_of_mem_Ioo
  obtain ⟨hmlo, hmhi⟩ := hmuc
  have habs_lt : |muc| < Real.pi / 2 - H := by
    rw [abs_lt]; exact ⟨by linarith, hmhi⟩
  constructor
  · linarith [abs_nonneg muc]
  · linarith

/-- **PROVED (0 sorry)**: cos²(|μc|+H) > 0 for μc in the domain. -/
theorem denom_cos_sq_pos {H : ℝ} (hH_pos : 0 ≤ H) (hH_lt : H < Real.pi / 2)
    {muc : ℝ} (hmuc : muc ∈ Set.Ioo (-(Real.pi / 2 - H)) (Real.pi / 2 - H)) :
    0 < Real.cos (|muc| + H) ^ 2 :=
  sq_pos_of_pos (denom_cos_pos hH_pos hH_lt hmuc)

/-! ### Arc-coverage arithmetic inequality -/

/-- **PROVED (0 sorry)**: `2 · arccos(2√6/5) / π < 33/256`.
    Equivalently: `arccos(2√6/5) < 33π/512`.
    Proof uses `cos_sq_lt` + strict monotone decrease of arccos. -/
theorem arc_coverage_ineq : 2 * Real.arccos (2 * Real.sqrt 6 / 5) / Real.pi < 33 / 256 := by
  have hpi_pos : (0 : ℝ) < Real.pi := Real.pi_pos
  -- C_D = 2√6/5: key properties
  have h6_sq : Real.sqrt 6 ^ 2 = 6 := Real.sq_sqrt (by norm_num)
  have hCD_pos : (0 : ℝ) < 2 * Real.sqrt 6 / 5 := by positivity
  have hCD_lt1 : 2 * Real.sqrt 6 / 5 < 1 := by
    have hsqrt6_nn : 0 ≤ Real.sqrt 6 := Real.sqrt_nonneg 6
    nlinarith [h6_sq, hsqrt6_nn]
  -- cos(33π/512) is positive
  have hcos33_pos : 0 < Real.cos (33 * Real.pi / 512) := by
    apply Real.cos_pos_of_mem_Ioo
    constructor <;> linarith [Real.pi_pos]
  -- cos(33π/512) < 2√6/5, using cos_sq_lt and (2√6/5)² = 24/25
  have hcosCD_sq : (2 * Real.sqrt 6 / 5) ^ 2 = 24 / 25 := by nlinarith [h6_sq]
  have hcos33_lt_CD : Real.cos (33 * Real.pi / 512) < 2 * Real.sqrt 6 / 5 := by
    have h_sq := cos_sq_lt  -- cos²(33π/512) < 24/25 = (2√6/5)²
    -- cos²(33π/512) < (2√6/5)² and both are in (0,1); conclude cos(33π/512) < 2√6/5
    -- Proof: if a > 0 and b > 0 and a² < b² then a < b.
    -- Here a = cos(33π/512), b = 2√6/5.
    have : Real.cos (33 * Real.pi / 512) ^ 2 < (2 * Real.sqrt 6 / 5) ^ 2 := by
      rw [hcosCD_sq]; exact h_sq
    have hcos_nn : 0 ≤ Real.cos (33 * Real.pi / 512) := hcos33_pos.le
    nlinarith [sq_nonneg (2 * Real.sqrt 6 / 5 - Real.cos (33 * Real.pi / 512)),
               sq_abs (Real.cos (33 * Real.pi / 512)),
               mul_pos hcos33_pos hCD_pos]
  -- arccos is strictly decreasing: cos(33π/512) < C_D implies arccos(C_D) < arccos(cos(33π/512))
  have hcos33_mem : Real.cos (33 * Real.pi / 512) ∈ Set.Icc (-1 : ℝ) 1 :=
    ⟨neg_one_le_cos _, cos_le_one _⟩
  -- arccos(cos(33π/512)) = 33π/512
  have hangle_in_Icc : 33 * Real.pi / 512 ∈ Set.Icc 0 Real.pi := by
    constructor <;> linarith [Real.pi_pos]
  have harccos_cos : Real.arccos (Real.cos (33 * Real.pi / 512)) = 33 * Real.pi / 512 :=
    Real.arccos_cos hangle_in_Icc.1 hangle_in_Icc.2
  -- Apply arccos_lt_arccos: needs -1 ≤ cos(33π/512), cos(33π/512) < C_D, C_D ≤ 1
  have harccos_lt : Real.arccos (2 * Real.sqrt 6 / 5) < 33 * Real.pi / 512 := by
    rw [← harccos_cos]
    exact Real.arccos_lt_arccos (neg_one_le_cos _) hcos33_lt_CD hCD_lt1.le
  -- arccos(C_D) < 33π/512 implies 2·arccos(C_D)/π < 33/256
  -- harccos_lt : arccos(2√6/5) < 33π/512
  -- Want: 2·arccos(2√6/5)/π < 33/256
  have harccos_nn : 0 ≤ Real.arccos (2 * Real.sqrt 6 / 5) := Real.arccos_nonneg _
  rw [div_lt_iff₀ hpi_pos]
  -- Goal: 2 * arccos(2√6/5) < 33/256 * π
  -- From harccos_lt: arccos(2√6/5) < 33π/512, so 2*arccos < 33π/256 = (33/256)*π
  nlinarith [harccos_lt, hpi_pos]

/-! ### B1a: windowMaxCos_lb — REMOVED (the claim is FALSE). See note below. -/

/- DISPROVED — the statement below is FALSE.  Counterexample: q = 18 gives
   L_blk 18 = 5, H = π/9 ≈ 0.349, domain = (-1.222, 1.222).  At μc = 1.2 (in the
   domain) the window phases give windowMaxCos ≈ -0.14, which is far below
   2√6/5 ≈ 0.98.  Indeed near the endpoints windowMaxCos can be as low as ≈ -0.68.
   The intended downstream consumer (`fcorr_lb`) does NOT need this uniform bound:
   the minimum of `fcorr` over the domain occurs at μc = 0 where windowMaxCos ≈ 1,
   and away from μc = 0 the denominator factor cos²(|μc|+H) shrinks fast enough.
   Hence this lemma is removed (commented out) rather than left as an unprovable sorry.

   Original (false) claim: For all q ≥ 18 and μc in the domain,
    `windowMaxCos (L_blk q) q hL μc ≥ 2√6/5`.

    **Proof strategy for Aristotle/human**:

    Set L = L_blk q, θ = π/q, C_D = 2√6/5.

    The n-th cosine argument (n = 0..L-1) is:
      φ_n = 2(μc − ξ_q) + (2n − (L−1))·θ + η_q
    These are equally spaced with step 2θ, centered at n = (L−1)/2 where
      φ_center = 2(μc − ξ_q) + η_q.

    **Key input** (`arc_coverage_ineq`): 33/256 > 2·arccos(C_D)/π,
    i.e. arccos(C_D) < 33π/512 ≤ (L_blk q − 1)·θ/2 = H(L,q).

    So the window's half-span (L−1)·θ/2 = H ≥ 33π/512 > arccos(C_D).
    The window steps 2θ in total arc 2·(L−1)·θ = 4H.

    For each μc in the domain: |φ_center| = |2(μc − ξ_q) + η_q| < 2(π/2 − H) + |η_q| + 2|ξ_q|.
    For q ≥ 18: |ξ_q| ≤ arctan(2/q) ≤ 2/q ≤ 2/18 and |η_q| ≤ arctan(1/(3)) ≤ π/6 < π/3.
    (For large q these → 0, but for q = 18 one must check bounds explicitly.)

    The argument: since consecutive phases differ by 2θ = 2π/q, and the window covers
    4H ≥ 4·33π/512 > 4·arccos(C_D), the window is wide enough to contain some n with
    |φ_n| ≤ arccos(C_D), giving cos(φ_n) ≥ C_D.

    The Lean proof would use:
    - `arc_coverage_ineq` (proved above) to show 4H > 4·arccos(C_D)
    - `Real.cos_le_one`, `Finset.le_sup'` to bound from above
    - A floor/ceiling index argument to find n₀ with |φ_{n₀}| ≤ arccos(C_D)
    - `Real.cos_arccos` to get cos(arccos(C_D)) = C_D
    - `Real.cos_le_cos_of_nonneg` or similar to connect |φ_{n₀}| ≤ arccos(C_D) to
      cos(φ_{n₀}) ≥ C_D
    - `Finset.le_sup'` to promote from one index to the sup'.

    The ξ_q / η_q correction bounds for q ≥ 18 require explicit estimates from
    `Complex.arg` bounds (via `Real.arctan` bounds). This is the hardest sub-step.
-/
/-
   theorem windowMaxCos_lb (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q)
       {muc : ℝ} (hmuc : muc ∈ Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q)) :
       2 * Real.sqrt 6 / 5 ≤ windowMaxCos (L_blk q) q hL muc
-/

/-! ### Helper: Complex.arg → Real.arctan (for positive real part) -/

/-- **PROVED (0 sorry)**: For `x > 0`, `arg ⟨x, y⟩ = arctan (y / x)`.
    This reduces `atan2'`, and hence `xiq`/`etaq` (whose `x`-arguments are positive),
    to `Real.arctan`, enabling the standard `arctan_le`/`arctan_nonneg` bounds. -/
theorem arg_eq_arctan (x y : ℝ) (hx : 0 < x) :
    Complex.arg ⟨x, y⟩ = Real.arctan (y / x) := by
  have harg : |(Complex.mk x y).arg| < Real.pi / 2 := by
    rw [Complex.abs_arg_lt_pi_div_two_iff]; left; exact hx
  rw [abs_lt] at harg
  have h2 := Complex.tan_arg (⟨x, y⟩ : ℂ)
  rw [← h2, Real.arctan_tan harg.1 harg.2]

/-! ### Verified ξ/η correction bounds and λ lower bound (NEW, sorry-free)

These are the explicit correction bounds that the `fcorr_lb` regime-A pigeonhole
needs (B1_RESULT lists `0 ≤ ξ ≤ θ/5`, `0 ≤ η ≤ tan θ/3`, `λ ∈ [2cos(π/18),2)` as
required but previously unformalized).  All proved with axioms
`[propext, Classical.choice, Quot.sound]`. -/

/-- `arctan x ≤ x` for `x ≥ 0` (from `Real.lt_tan` at `arctan x`). -/
theorem arctan_le_self (x : ℝ) (hx : 0 ≤ x) : Real.arctan x ≤ x := by
  rcases eq_or_lt_of_le hx with h | h
  · simp [← h]
  · have h1 := Real.arctan_lt_pi_div_two x
    have h2 : 0 < Real.arctan x := Real.arctan_pos.mpr h
    have h3 : Real.arctan x < Real.tan (Real.arctan x) := Real.lt_tan h2 h1
    rw [Real.tan_arctan] at h3; linarith

/-- `λ = 2cos(π/q) ≥ 1.9` for `q ≥ 18` (via `cos` monotone + `cos_bound` at `π/18`). -/
theorem lamq_ge (q : ℕ) (hq : 18 ≤ q) : (1.9 : ℝ) ≤ lamq q := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have h18 : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have hle : Real.pi / q ≤ Real.pi / 18 :=
    div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num) h18
  have hpos : 0 ≤ Real.pi / q := by positivity
  have hmono : Real.cos (Real.pi/18) ≤ Real.cos (Real.pi/q) :=
    Real.cos_le_cos_of_nonneg_of_le_pi hpos (by linarith [Real.pi_le_four, Real.pi_pos]) hle
  have hb : |Real.pi/18| ≤ 1 := by rw [abs_of_nonneg (by positivity)]; nlinarith [Real.pi_lt_d4]
  have hcb := Real.cos_bound hb; rw [abs_le] at hcb
  have hax : |Real.pi/18|^4 = (Real.pi/18)^4 := by rw [← abs_pow]; exact abs_of_nonneg (by positivity)
  rw [hax] at hcb
  have hp18_lo : (0.1745:ℝ) ≤ Real.pi/18 := by nlinarith [Real.pi_gt_d4]
  have hp18_hi : Real.pi/18 ≤ (0.1746:ℝ) := by nlinarith [Real.pi_lt_d4]
  have hsq : (Real.pi/18)^2 ≤ (0.1746:ℝ)^2 := by nlinarith [hp18_lo, hp18_hi, sq_nonneg (Real.pi/18)]
  have hqt : (Real.pi/18)^4 ≤ (0.1746:ℝ)^4 := by nlinarith [hsq, sq_nonneg ((Real.pi/18)^2)]
  have hcos18 : (0.95:ℝ) ≤ Real.cos (Real.pi/18) := by nlinarith [hcb.1, hsq, hqt]
  unfold lamq; linarith [hmono, hcos18]

/-- `0 ≤ η` for `q ≥ 18` (η = arctan(tan θ/3), positive real part). -/
theorem etaq_nonneg (q : ℕ) (hq : 18 ≤ q) : 0 ≤ etaq q := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have ht_pos : 0 < thetaq q := by unfold thetaq; positivity
  have ht_lt : thetaq q < Real.pi / 2 := by
    unfold thetaq; rw [div_lt_div_iff₀ hqr (by norm_num)]
    have : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
    nlinarith [Real.pi_pos]
  have hcos_pos : 0 < 3 * Real.cos (thetaq q) := by
    have := Real.cos_pos_of_mem_Ioo (show thetaq q ∈ Set.Ioo (-(π/2)) (π/2) from ⟨by linarith, ht_lt⟩); linarith
  unfold etaq atan2'; rw [arg_eq_arctan _ _ hcos_pos]
  apply Real.arctan_nonneg.mpr
  have hsin : 0 ≤ Real.sin (thetaq q) := Real.sin_nonneg_of_nonneg_of_le_pi ht_pos.le (by linarith [Real.pi_pos])
  positivity

/-- `η ≤ tan θ / 3` for `q ≥ 18` (η = arctan(tan θ/3) ≤ tan θ/3). -/
theorem etaq_le (q : ℕ) (hq : 18 ≤ q) : etaq q ≤ Real.tan (thetaq q) / 3 := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have ht_pos : 0 < thetaq q := by unfold thetaq; positivity
  have ht_lt : thetaq q < Real.pi / 2 := by
    unfold thetaq; rw [div_lt_div_iff₀ hqr (by norm_num)]
    have : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
    nlinarith [Real.pi_pos]
  have hcos_pos : 0 < 3 * Real.cos (thetaq q) := by
    have := Real.cos_pos_of_mem_Ioo (show thetaq q ∈ Set.Ioo (-(π/2)) (π/2) from ⟨by linarith, ht_lt⟩); linarith
  have hsin : 0 ≤ Real.sin (thetaq q) := Real.sin_nonneg_of_nonneg_of_le_pi ht_pos.le (by linarith [Real.pi_pos])
  unfold etaq atan2'; rw [arg_eq_arctan _ _ hcos_pos]
  have hrw : Real.sin (thetaq q) / (3 * Real.cos (thetaq q)) = Real.tan (thetaq q) / 3 := by
    rw [Real.tan_eq_sin_div_cos]; field_simp
  rw [hrw]; apply arctan_le_self
  rw [Real.tan_eq_sin_div_cos]
  have : 0 ≤ Real.sin (thetaq q) / Real.cos (thetaq q) := div_nonneg hsin (by linarith)
  linarith

/-- `ξ ≤ θ / 5` for `q ≥ 18`.  Reduces (via `arctan_le_self`) to
    `5λ sin θ ≤ θ(3λ²+1+λ cos θ)`, then to `5λ ≤ 3λ²+1` (using `sin θ ≤ θ`,
    `λ cos θ ≥ 0`), which holds for `λ ≥ 1.9` (`lamq_ge`). -/
theorem xiq_le (q : ℕ) (hq : 18 ≤ q) : xiq q ≤ thetaq q / 5 := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have ht_pos : 0 < thetaq q := by unfold thetaq; positivity
  have ht_lt : thetaq q < Real.pi / 2 := by
    unfold thetaq; rw [div_lt_div_iff₀ hqr (by norm_num)]
    have : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
    nlinarith [Real.pi_pos]
  have hcos_pos : 0 < Real.cos (thetaq q) := Real.cos_pos_of_mem_Ioo ⟨by linarith, ht_lt⟩
  have hlam_pos : 0 < lamq q := by unfold lamq; positivity
  have hlam_ge : (1.9:ℝ) ≤ lamq q := lamq_ge q hq
  have hsin_le : Real.sin (thetaq q) ≤ thetaq q := (Real.sin_lt ht_pos).le
  have hsin_pos : 0 ≤ Real.sin (thetaq q) := Real.sin_nonneg_of_nonneg_of_le_pi ht_pos.le (by linarith [Real.pi_pos])
  have hcoslam : lamq q * Real.cos (thetaq q) ≥ 0 := mul_nonneg hlam_pos.le hcos_pos.le
  have hden_pos : 0 < 3 * lamq q ^ 2 + 1 + lamq q * Real.cos (thetaq q) := by positivity
  unfold xiq atan2'; rw [arg_eq_arctan _ _ hden_pos]
  refine le_trans (arctan_le_self _ (by positivity)) ?_
  rw [div_le_div_iff₀ hden_pos (by norm_num)]
  have hkey : 5 * lamq q ≤ 3 * lamq q ^ 2 + 1 := by nlinarith [hlam_ge]
  nlinarith [hsin_le, hsin_pos, ht_pos, hlam_pos, hcoslam, hkey,
             mul_nonneg hlam_pos.le hsin_pos,
             mul_le_mul_of_nonneg_left hsin_le (by linarith : (0:ℝ) ≤ 5 * lamq q)]

/-- **Worst-case core identity (the through-line).**  The q→∞ limit of the regime-A
    core (A) `λ³(3λ/2 + √A₂·W) ≥ 2·A₂·Blam²·cos²(H)` is, after `λ→2, A₂→9,
    Blam²→25/9, W→1, H→33π/512`, exactly `48 ≥ 50·cos²(33π/512)`, i.e. equivalent
    to `cos_sq_lt` (`cos²(33π/512) < 24/25`).  The finite-q core has strictly larger
    margin (numerically infimum ≈ 0.02215 = `48 − 50·cos²(33π/512)`, attained as
    q→∞), so this limiting form is the binding constraint of the whole theorem. -/
theorem core_limit : 50 * Real.cos (33 * Real.pi / 512) ^ 2 < 48 := by
  linarith [cos_sq_lt]

/-! ### Verified analytic building blocks toward the `fcorr_lb` regime-A core

The following lemmas (all sorry-free) are the verified components of the q-uniform
"regime A" core inequality
  (A)  λ³·(3λ/2 + √A₂·cos(θ+2ξ+η)) ≥ 2·A₂·Blam²·cos²(H)
for the large-q range (q ≥ 23, t = π/q ∈ (0, π/23], loose bound H ≥ 33π/512 + t/2).
They provide: Taylor envelopes for sin/cos, tight numeric bounds for cos/sin at
β = 33π/512, the LHS cosine upper bound `cosb_ub`, and the RHS window-cosine lower
bound `cos_arg_ge`.

**Remaining obstruction (documented).**  Combining these reduces (A) to a polynomial
inequality in `c = cos t` and `t`.  Numerically its continuous margin is only ~0.0022
(it is the limiting headroom `24/25 - cos²(33π/512) ≈ 5·10⁻⁴`, i.e. `cos_sq_lt`), and
the inequality is tight *exactly along* the curve `c = cos t`: it becomes FALSE if `c`
is relaxed to any interval `[L(t), 1]` with `L(t) < cos t` (even by 10⁻⁵).  Hence a
generic `nlinarith`/`polyrith` over a `c`-interval cannot close it; a successful proof
must keep the exact relation `c = cos t` (e.g. tight two-sided cos-power envelopes in
`t` alone, with matching signs).  This final assembly, together with the regime-A
pigeonhole index, the regime-B endpoint estimate, and the five concrete small-q cases
(q = 18..22, where `L_blk q = 5` and `H = 2θ` exactly), is what remains for `fcorr_lb`. -/

/-- Taylor lower bound for `sin` on `[0,1]` (from `Real.sin_bound`). -/
theorem sin_lower (x : ℝ) (hx0 : 0 ≤ x) (hx1 : x ≤ 1) :
    x - x^3/6 - x^4*(5/96) ≤ Real.sin x := by
  have h := Real.sin_bound (show |x| ≤ 1 by rwa [abs_of_nonneg hx0])
  rw [abs_le, abs_of_nonneg hx0] at h; nlinarith [h.1]

/-- Taylor upper bound for `cos` on `[-1,1]` (from `Real.cos_bound`). -/
theorem cos_upper (x : ℝ) (hx1 : |x| ≤ 1) :
    Real.cos x ≤ 1 - x^2/2 + x^4*(5/96) := by
  have h := Real.cos_bound hx1; rw [abs_le] at h
  have hax : |x|^4 = x^4 := by rw [← abs_pow]; exact abs_of_nonneg (by positivity)
  nlinarith [h.2, hax]

/-- Taylor lower bound for `cos` on `[-1,1]` (from `Real.cos_bound`). -/
theorem cos_lower (x : ℝ) (hx1 : |x| ≤ 1) :
    1 - x^2/2 - x^4*(5/96) ≤ Real.cos x := by
  have h := Real.cos_bound hx1; rw [abs_le] at h
  have hax : |x|^4 = x^4 := by rw [← abs_pow]; exact abs_of_nonneg (by positivity)
  nlinarith [h.1, hax]

theorem beta_lo : (0.2024854:ℝ) ≤ 33*Real.pi/512 := by nlinarith [Real.pi_gt_d6]
theorem beta_hi : 33*Real.pi/512 ≤ (0.2024855:ℝ) := by nlinarith [Real.pi_lt_d6]
theorem beta_abs : |33 * Real.pi / 512| ≤ 1 := by
  rw [abs_of_nonneg (by positivity)]; nlinarith [Real.pi_lt_d6]

/-- Tight upper bound `cos(33π/512) ≤ 0.97960`. -/
theorem cos_beta_le : Real.cos (33 * Real.pi / 512) ≤ 0.97960 := by
  have h := cos_upper (33*Real.pi/512) beta_abs
  have hs2 : (33*Real.pi/512)^2 ≥ (0.2024854:ℝ)^2 := by gcongr; exact beta_lo
  have hs4 : (33*Real.pi/512)^4 ≤ (0.2024855:ℝ)^4 := by gcongr; exact beta_hi
  nlinarith [h, hs2, hs4]

/-- Tight lower bound `sin(33π/512) ≥ 0.2010`. -/
theorem sin_beta_ge : (0.2010:ℝ) ≤ Real.sin (33 * Real.pi / 512) := by
  have h := sin_lower (33*Real.pi/512) (by linarith [Real.pi_pos]) (by nlinarith [Real.pi_lt_d6])
  have hs3 : (33*Real.pi/512)^3 ≤ (0.2024855:ℝ)^3 := by gcongr; exact beta_hi
  have hs4 : (33*Real.pi/512)^4 ≤ (0.2024855:ℝ)^4 := by gcongr; exact beta_hi
  nlinarith [h, beta_lo, hs3, hs4]

/-- `tan t ≤ 1.02 t` for `t ∈ (0, π/23]`. -/
theorem tan_le (t : ℝ) (ht0 : 0 < t) (ht : t ≤ Real.pi/23) : Real.tan t ≤ 1.02 * t := by
  have htle : t ≤ 0.1367 := by nlinarith [Real.pi_lt_d4]
  have hcos : Real.cos t ≥ 0.99 := by
    have hb : |t| ≤ 1 := by rw [abs_of_nonneg ht0.le]; linarith
    have hc := Real.cos_bound hb; rw [abs_le] at hc
    have hax : |t|^4 = t^4 := by rw [← abs_pow]; exact abs_of_nonneg (by positivity)
    have ht4 : t^4 ≤ (0.1367:ℝ)^4 := by gcongr
    nlinarith [hc.1, hax, ht4]
  have hsin : Real.sin t ≤ t := (Real.sin_lt ht0).le
  rw [Real.tan_eq_sin_div_cos, div_le_iff₀ (by linarith)]
  nlinarith [hsin, hcos, ht0.le]

/-- RHS window-cosine lower bound: `cos(t + 2(t/5) + tan t/3) ≥ 1 - 1.52 t²`,
    for `t ∈ (0, π/23]`.  (This bounds `windowMaxCos ≥ cos(θ+2ξ+η)` after the
    pigeonhole step, using `ξ ≤ θ/5`, `η ≤ tan θ/3`.) -/
theorem cos_arg_ge (t : ℝ) (ht0 : 0 < t) (ht : t ≤ Real.pi/23) :
    1 - 1.52 * t^2 ≤ Real.cos (t + 2*(t/5) + Real.tan t/3) := by
  have htle : t ≤ 0.1367 := by nlinarith [Real.pi_lt_d4]
  have htan := tan_le t ht0 ht
  have hcosnn : 0 ≤ Real.cos t := Real.cos_nonneg_of_mem_Icc ⟨by linarith [Real.pi_pos], by linarith⟩
  have htan0 : 0 ≤ Real.tan t := by
    rw [Real.tan_eq_sin_div_cos]
    exact div_nonneg (Real.sin_nonneg_of_nonneg_of_le_pi ht0.le (by linarith [Real.pi_pos])) hcosnn
  set a := t + 2*(t/5) + Real.tan t/3 with ha
  have ha_nn : 0 ≤ a := by rw [ha]; positivity
  have ha_ub : a ≤ 1.74 * t := by rw [ha]; nlinarith [htan]
  have hmono : Real.cos (1.74*t) ≤ Real.cos a :=
    Real.cos_le_cos_of_nonneg_of_le_pi ha_nn (by linarith) ha_ub
  have hcb : 1 - (1.74*t)^2/2 ≤ Real.cos (1.74*t) := by
    linarith [Real.one_sub_sq_div_two_le_cos (x := 1.74*t)]
  nlinarith [hmono, hcb]

/-- LHS cosine upper bound: `cos(33π/512 + t/2) ≤ U(t)`, the quadratic Taylor
    envelope, for `t ∈ (0, π/23]`.  (This bounds `cos²(H) ≤ cos²(33π/512 + t/2)`
    after `H ≥ 33π/512 + t/2`.) -/
theorem cosb_ub (t : ℝ) (ht0 : 0 < t) (ht : t ≤ Real.pi/23) :
    Real.cos (33 * Real.pi / 512 + t/2)
      ≤ 0.97960*(1 - (t/2)^2/2 + (t/2)^4*(5/96))
        - 0.2010*(t/2 - (t/2)^3/6 - (t/2)^4*(5/96)) := by
  have htle : t ≤ 0.1367 := by nlinarith [Real.pi_lt_d6]
  have hu0 : 0 ≤ t/2 := by linarith
  have hu1 : t/2 ≤ 1 := by linarith
  rw [Real.cos_add]
  have hcosβle := cos_beta_le
  have hsinβge := sin_beta_ge
  have hcosβpos : 0 ≤ Real.cos (33*Real.pi/512) := by
    apply Real.cos_nonneg_of_mem_Icc; constructor <;> nlinarith [Real.pi_gt_d6, Real.pi_lt_d6]
  have hcosu_ub : Real.cos (t/2) ≤ 1 - (t/2)^2/2 + (t/2)^4*(5/96) :=
    cos_upper (t/2) (by rw [abs_of_nonneg hu0]; exact hu1)
  have hcosu_pos : 0 ≤ Real.cos (t/2) := Real.cos_nonneg_of_mem_Icc ⟨by linarith [Real.pi_pos], by linarith⟩
  have hsinu_lb : t/2 - (t/2)^3/6 - (t/2)^4*(5/96) ≤ Real.sin (t/2) := sin_lower (t/2) hu0 hu1
  have hsinu_pos : 0 ≤ Real.sin (t/2) := Real.sin_nonneg_of_nonneg_of_le_pi hu0 (by linarith [Real.pi_pos])
  have hterm1 : Real.cos (33*Real.pi/512) * Real.cos (t/2)
      ≤ 0.97960*(1 - (t/2)^2/2 + (t/2)^4*(5/96)) := by
    calc Real.cos (33*Real.pi/512) * Real.cos (t/2)
        ≤ 0.97960 * Real.cos (t/2) := by nlinarith [hcosu_pos, hcosβle]
      _ ≤ 0.97960*(1 - (t/2)^2/2 + (t/2)^4*(5/96)) := by nlinarith [hcosu_ub]
  have hterm2 : 0.2010*(t/2 - (t/2)^3/6 - (t/2)^4*(5/96))
      ≤ Real.sin (33*Real.pi/512) * Real.sin (t/2) := by
    calc 0.2010*(t/2 - (t/2)^3/6 - (t/2)^4*(5/96))
        ≤ 0.2010 * Real.sin (t/2) := by nlinarith [hsinu_lb]
      _ ≤ Real.sin (33*Real.pi/512) * Real.sin (t/2) := by nlinarith [hsinu_pos, hsinβge]
  linarith [hterm1, hterm2]

/-! ### B1b: fcorr ≥ 1/λ³ pointwise (PROVED — see `section RegimeCores` + `fcorr_lb`) -/

/-- **Precise residual core (regime-A worst case), as a standalone `Prop`.**
    This is the exact single-variable inequality a human/Aristotle must close to
    discharge `fcorr_lb`'s regime A.  Stated with EXACT `H = Hq (L_blk q) q` (NOT the
    loose `33π/512 + θ/2` bound — the loose bound is FALSE for q ∈ {18,19,20,21},
    verified on M1: loose-H margin = −0.283/−0.172/−0.081/−0.005 there).  With exact
    H, the margin is comfortably positive for every q (M1 scan q=18..10⁶: infimum
    ≈ +0.02215, attained as q→∞).  The phase argument `θ + 2ξ + η` is the pigeonhole
    worst alignment at μc = 0, using `xiq_le`/`etaq_le` (`ξ ≤ θ/5`, `η ≤ tan θ/3`). -/
def RegimeACore (q : ℕ) : Prop :=
  2 * A2q q * Blamq q ^ 2 * Real.cos (Hq (L_blk q) q) ^ 2
    ≤ lamq q ^ 3 * (3 * lamq q / 2
        + Real.sqrt (A2q q) * Real.cos (thetaq q + 2 * xiq q + etaq q))

/-- **Precise residual core (regime-B endpoint), as a standalone `Prop`.**
    For the endpoint index at `|μc| > H`, with `φ = 2(μc-ξ)+η ∓ 2H`.  CORRECTION to
    B1_RESULT: the regime-B slack is NOT ≥ 0.24 — M1 shows the true minimum slack over
    `|μc| ∈ (H, π/2−H)` is only ≈ +0.0175 (q=1000), attained near the inner boundary
    `|μc| ↓ H` (continuity with regime A).  The crude bound `W ≥ −1` FAILS here
    (`3λ/2 − √A₂ ≈ −0.005 < 0`), so the endpoint phase must be tracked. -/
def RegimeBCore (q : ℕ) (muc : ℝ) : Prop :=
  Hq (L_blk q) q < |muc| →
    2 * A2q q * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q) ^ 2
      ≤ lamq q ^ 3 * (3 * lamq q / 2
          + Real.sqrt (A2q q) * Real.cos (2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q))


section RegimeCores
set_option maxHeartbeats 4000000

/-- **Algebraic identity**: `2·A₂·Blamq² = 12·λ² + 2`.
    Eliminates the sqrt/division from the LHS of RegimeACore. -/
theorem twoA2Blam_eq (q : ℕ) : 2 * A2q q * Blamq q ^ 2 = 12 * lamq q ^ 2 + 2 := by
  unfold A2q Blamq
  set lam := lamq q
  have hrad : (0:ℝ) ≤ 12 * lam ^ 4 + 8 * lam ^ 2 + 1 := by positivity
  have hsq : Real.sqrt (12 * lam ^ 4 + 8 * lam ^ 2 + 1) ^ 2
      = 12 * lam ^ 4 + 8 * lam ^ 2 + 1 := Real.sq_sqrt hrad
  have hden : (2 * lam ^ 2 + 1) ≠ 0 := by positivity
  rw [div_pow, hsq]
  field_simp
  ring

/-- For q ≥ 18, `0 ≤ θ + 2ξ + η ≤ θ + 2(θ/5) + tan θ`.  (Upper via xiq_le, etaq_le, tan θ/3 ≤ tan θ.) -/
theorem arg_bounds (q : ℕ) (hq : 18 ≤ q) :
    0 ≤ thetaq q + 2 * xiq q + etaq q ∧
    thetaq q + 2 * xiq q + etaq q ≤ thetaq q + 2 * (thetaq q / 5) + Real.tan (thetaq q) / 3 := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have ht_pos : 0 < thetaq q := by unfold thetaq; positivity
  -- xi ≥ 0
  have ht_lt : thetaq q < Real.pi / 2 := by
    unfold thetaq; rw [div_lt_div_iff₀ hqr (by norm_num)]
    have : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
    nlinarith [Real.pi_pos]
  have hcos_pos : 0 < Real.cos (thetaq q) := Real.cos_pos_of_mem_Ioo ⟨by linarith, ht_lt⟩
  have hlam_pos : 0 < lamq q := by unfold lamq; positivity
  have hsin_pos : 0 ≤ Real.sin (thetaq q) := Real.sin_nonneg_of_nonneg_of_le_pi ht_pos.le (by linarith [Real.pi_pos])
  have hden_pos : 0 < 3 * lamq q ^ 2 + 1 + lamq q * Real.cos (thetaq q) := by positivity
  have hxi_nn : 0 ≤ xiq q := by
    unfold xiq atan2'; rw [arg_eq_arctan _ _ hden_pos]
    apply Real.arctan_nonneg.mpr
    have : 0 ≤ lamq q * Real.sin (thetaq q) := mul_nonneg hlam_pos.le hsin_pos
    positivity
  have heta_nn : 0 ≤ etaq q := etaq_nonneg q hq
  refine ⟨by positivity, ?_⟩
  have hxi := xiq_le q hq
  have heta := etaq_le q hq
  -- tan θ / 3 ≤ tan θ since tan θ ≥ 0
  have htan_nn : 0 ≤ Real.tan (thetaq q) := by
    rw [Real.tan_eq_sin_div_cos]; exact div_nonneg hsin_pos hcos_pos.le
  linarith

/-- **Monotone reduction**: `cos(θ+2ξ+η) ≥ cos(θ + 2(θ/5) + tan θ/3)` for q ≥ 18,
    provided the upper argument stays in [0, π].  Uses cos decreasing on [0,π]. -/
theorem cos_arg_lower (q : ℕ) (hq : 18 ≤ q)
    (hub : thetaq q + 2 * (thetaq q / 5) + Real.tan (thetaq q) / 3 ≤ Real.pi) :
    Real.cos (thetaq q + 2 * (thetaq q / 5) + Real.tan (thetaq q) / 3)
      ≤ Real.cos (thetaq q + 2 * xiq q + etaq q) := by
  obtain ⟨hlo, hhi⟩ := arg_bounds q hq
  exact Real.cos_le_cos_of_nonneg_of_le_pi hlo hub hhi

/-- `tan t ≤ 1.02 t` for `t ∈ (0, π/18]` (wider than `tan_le`, for q ∈ {18..22}). -/
theorem tan_le18 (t : ℝ) (ht0 : 0 < t) (ht : t ≤ Real.pi/18) : Real.tan t ≤ 1.02 * t := by
  have htle : t ≤ 0.1746 := by nlinarith [Real.pi_lt_d4]
  have hcos : Real.cos t ≥ 0.981 := by
    have hb : |t| ≤ 1 := by rw [abs_of_nonneg ht0.le]; linarith
    have hc := Real.cos_bound hb; rw [abs_le] at hc
    have hax : |t|^4 = t^4 := by rw [← abs_pow]; exact abs_of_nonneg (by positivity)
    have ht4 : t^4 ≤ (0.1746:ℝ)^4 := by gcongr
    nlinarith [hc.1, hax, ht4]
  have hsin : Real.sin t ≤ t := (Real.sin_lt ht0).le
  rw [Real.tan_eq_sin_div_cos, div_le_iff₀ (by linarith)]
  nlinarith [hsin, hcos, ht0.le]

/-- RHS window-cosine lower bound on the WIDER interval `(0, π/18]`:
    `cos(t + 2(t/5) + tan t/3) ≥ 1 - 1.5138 t²`.  (arg ≤ 1.74 t, cos(1.74t) ≥ 1-(1.74t)²/2.) -/
theorem cos_arg_ge18 (t : ℝ) (ht0 : 0 < t) (ht : t ≤ Real.pi/18) :
    1 - 1.5138 * t^2 ≤ Real.cos (t + 2*(t/5) + Real.tan t/3) := by
  have htle : t ≤ 0.1746 := by nlinarith [Real.pi_lt_d4]
  have htan := tan_le18 t ht0 ht
  have hcosnn : 0 ≤ Real.cos t := Real.cos_nonneg_of_mem_Icc ⟨by linarith [Real.pi_pos], by linarith⟩
  have htan0 : 0 ≤ Real.tan t := by
    rw [Real.tan_eq_sin_div_cos]
    exact div_nonneg (Real.sin_nonneg_of_nonneg_of_le_pi ht0.le (by linarith [Real.pi_pos])) hcosnn
  set a := t + 2*(t/5) + Real.tan t/3 with ha
  have ha_nn : 0 ≤ a := by rw [ha]; positivity
  have ha_ub : a ≤ 1.74 * t := by rw [ha]; nlinarith [htan]
  have hmono : Real.cos (1.74*t) ≤ Real.cos a :=
    Real.cos_le_cos_of_nonneg_of_le_pi ha_nn (by linarith) ha_ub
  have hcb : 1 - (1.74*t)^2/2 ≤ Real.cos (1.74*t) := by
    linarith [Real.one_sub_sq_div_two_le_cos (x := 1.74*t)]
  nlinarith [hmono, hcb]

/-- **Engine (small-q regime A core), polynomial form.**
    Given `c ∈ [cl, cu]` with `cl > 0`, `s ≥ 0` with `s^2 = 8c^2+1`, `s ≥ slo ≥ 0`,
    `W ≥ Wlo ≥ 0`, and the numeric inequality
      `(48·cu²+2)·(2·cu²-1)² ≤ 8·cl³·(3·cl + slo·Wlo)`,
    conclude `(12·(2c)²+2)·(2c²-1)² ≤ (2c)³·(3·(2c)/2 + s·W)`. -/
theorem regimeA_engine (c cl cu s slo W Wlo : ℝ)
    (hcl0 : 0 < cl) (hclc : cl ≤ c) (hccu : c ≤ cu) (hcu1 : cu ≤ 1)
    (hs0 : 0 ≤ s) (hslo : slo ≤ s) (hslo0 : 0 ≤ slo)
    (hW : Wlo ≤ W) (hWlo0 : 0 ≤ Wlo)
    (hc2 : 2*c^2 - 1 ≥ 0)
    (hnum : (48*cu^2+2)*(2*cu^2-1)^2 ≤ 8*cl^3*(3*cl + slo*Wlo)) :
    (12*(2*c)^2+2)*(2*c^2-1)^2 ≤ (2*c)^3*(3*(2*c)/2 + s*W) := by
  have hc0 : 0 < c := lt_of_lt_of_le hcl0 hclc
  -- LHS upper bound: (12*(2c)^2+2)(2c^2-1)^2 = (48c^2+2)(2c^2-1)^2 ≤ (48cu^2+2)(2cu^2-1)^2
  have hLHS : (12*(2*c)^2+2)*(2*c^2-1)^2 ≤ (48*cu^2+2)*(2*cu^2-1)^2 := by
    have h1 : (48*c^2+2) ≤ (48*cu^2+2) := by nlinarith [hccu, hc0.le, hcu1]
    have h2 : (2*c^2-1)^2 ≤ (2*cu^2-1)^2 := by nlinarith [hccu, hc0.le, hcu1, hc2]
    nlinarith [h1, h2, sq_nonneg (2*c^2-1), mul_nonneg (by positivity : (0:ℝ) ≤ 48*c^2+2) (sq_nonneg (2*c^2-1))]
  -- RHS lower bound: 8c^3(3c + s W) ≥ 8cl^3(3cl + slo Wlo)
  have hRHS : 8*cl^3*(3*cl + slo*Wlo) ≤ (2*c)^3*(3*(2*c)/2 + s*W) := by
    have hcl3 : 8*cl^3 ≤ (2*c)^3 := by
      have : (2*cl)^3 ≤ (2*c)^3 := by
        apply pow_le_pow_left₀ (by linarith) (by linarith)
      nlinarith [this]
    have hin : 3*cl + slo*Wlo ≤ 3*(2*c)/2 + s*W := by
      have hsw : slo*Wlo ≤ s*W := by
        calc slo*Wlo ≤ s*Wlo := by nlinarith [hslo, hWlo0]
          _ ≤ s*W := by nlinarith [hW, hs0]
      nlinarith [hclc, hsw]
    have hpos : 0 ≤ 3*(2*c)/2 + s*W := by
      have : 0 ≤ s*W := by nlinarith [hs0, hW, hWlo0]
      nlinarith [hc0.le, this]
    have hnn1 : 0 ≤ 3*cl + slo*Wlo := by nlinarith [hcl0.le, hslo0, hWlo0]
    calc 8*cl^3*(3*cl + slo*Wlo) ≤ (2*c)^3*(3*cl+slo*Wlo) := by
            apply mul_le_mul_of_nonneg_right hcl3 hnn1
      _ ≤ (2*c)^3*(3*(2*c)/2 + s*W) := by
            apply mul_le_mul_of_nonneg_left hin (by positivity)
  linarith [hLHS, hRHS, hnum]

/-- `A2q q = 8·cos²(θ) + 1`. -/
theorem A2q_eq (q : ℕ) : A2q q = 8 * Real.cos (thetaq q)^2 + 1 := by
  unfold A2q lamq thetaq; ring

/-- `L_blk q = 5` for `q ∈ {18,…,23}`, hence `H = 2θ`. -/
theorem Lblk_eq5 (q : ℕ) (hq18 : 18 ≤ q) (hq23 : q ≤ 23) : L_blk q = 5 := by
  unfold L_blk
  have h1 : (33 * (q:ℝ))/256 ≤ 3 := by
    have : (q:ℝ) ≤ 23 := by exact_mod_cast hq23
    nlinarith
  have h2 : (2:ℝ) < (33 * (q:ℝ))/256 := by
    have : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq18
    nlinarith
  have hc1 : ⌈(33 * (q:ℝ))/256⌉ ≤ 3 := Int.ceil_le.mpr (by push_cast; linarith)
  have hc2 : (3:ℤ) ≤ ⌈(33 * (q:ℝ))/256⌉ := by
    rw [Int.le_ceil_iff]; push_cast; linarith
  have : ⌈(33 * (q:ℝ))/256⌉ = 3 := le_antisymm hc1 hc2
  rw [this]; rfl

/-- Pure-`u` s-bound: `(3 - 1.43u)² ≤ 8(1-u/2)² + 1` on `u ∈ [0, 1/30]`. -/
theorem sbound_small_u (u : ℝ) (hu0 : 0 ≤ u) (hu : u ≤ 1/30) :
    (3 - 1.43*u)^2 ≤ 8*(1 - u/2)^2 + 1 := by
  nlinarith [hu0, hu, sq_nonneg u]

/-- Pure-`u` numeric inequality (`u = t²`) backing the small-q `hnum`.
    The inequality is FALSE at `u=0` (that is the `cos_sq_lt` boundary), so the lower
    bound `u ≥ uLo := 0.0186 < (π/23)²` is essential. Proven on `u ∈ [0.0186, 0.0305]`
    (⊇ `[(π/23)², (π/18)²]`). Degree 12 in `u`, margin ≥ +0.047. -/
theorem hnum_small_u (u : ℝ) (huLo : 0.0186 ≤ u) (huHi : u ≤ 0.0305) :
    (48*(1 - u/2 + u^2*(5/96))^2+2)*(2*(1 - u/2 + u^2*(5/96))^2-1)^2
      ≤ 8*(1 - u/2)^3*(3*(1 - u/2) + (3 - 1.43*u)*(1 - 1.5138 * u)) := by
  have h1 : 0 ≤ u - 0.0186 := by linarith
  have h2 : 0 ≤ 0.0305 - u := by linarith
  have hu0 : (0:ℝ) ≤ u := by linarith
  nlinarith [h1, h2, hu0, mul_nonneg h1 h2, sq_nonneg u, mul_nonneg hu0 hu0,
             mul_nonneg (mul_nonneg h1 h2) hu0, mul_nonneg (mul_nonneg h1 h2) (mul_nonneg hu0 hu0),
             mul_nonneg h1 hu0, mul_nonneg h2 hu0, pow_nonneg hu0 3, pow_nonneg hu0 4]

/-- **RegimeACore for q ∈ {18,…,23}** (exact `H = 2θ`). -/
theorem regimeA_small (q : ℕ) (hq18 : 18 ≤ q) (hq23 : q ≤ 23) : RegimeACore q := by
  unfold RegimeACore
  rw [twoA2Blam_eq]
  -- set t = θ, c = cos θ
  set t := thetaq q with ht_def
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have ht0 : 0 < t := by rw [ht_def]; unfold thetaq; positivity
  have hq23r : (q:ℝ) ≤ 23 := by exact_mod_cast hq23
  have hq18r : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq18
  have ht_lo : Real.pi/23 ≤ t := by
    rw [ht_def]; unfold thetaq
    apply div_le_div_of_nonneg_left Real.pi_pos.le hqr hq23r
  have ht_hi : t ≤ Real.pi/18 := by
    rw [ht_def]; unfold thetaq
    apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num) hq18r
  have ht1 : t ≤ 1 := by have := Real.pi_lt_d4; nlinarith [ht_hi]
  -- H = 2θ
  have hH : Hq (L_blk q) q = 2 * t := by
    rw [Lblk_eq5 q hq18 hq23]; unfold Hq; rw [ht_def]; push_cast; ring
  rw [hH]
  -- cos(2t) = 2 cos²t - 1
  have hcos2t : Real.cos (2*t) = 2 * Real.cos t^2 - 1 := by rw [Real.cos_two_mul]
  rw [hcos2t]
  -- A2 = 8 cos²t + 1
  have hA2 : A2q q = 8 * Real.cos t^2 + 1 := by rw [A2q_eq]
  -- lam = 2 cos t
  have hlam : lamq q = 2 * Real.cos t := by unfold lamq; rw [ht_def]; rfl
  rw [hlam]
  set c := Real.cos t with hc_def
  -- u = t² with rational interval bounds [0.0186, 0.0305]
  have htabs : |t| ≤ 1 := by rw [abs_of_nonneg ht0.le]; exact ht1
  have huLo : (0.0186:ℝ) ≤ t^2 := by nlinarith [ht_lo, Real.pi_gt_d4, ht0.le]
  have huHi : t^2 ≤ (0.0305:ℝ) := by nlinarith [ht_hi, Real.pi_lt_d4, ht0.le]
  have hu0 : (0:ℝ) ≤ t^2 := sq_nonneg t
  have hu30 : t^2 ≤ 1/30 := by linarith
  -- envelopes for c = cos t : lower 1-t²/2, upper cos_upper (1-t²/2+t⁴·5/96)
  have hcL : 1 - t^2/2 ≤ c := by rw [hc_def]; exact Real.one_sub_sq_div_two_le_cos
  have hcU : c ≤ 1 - t^2/2 + t^4*(5/96) := by rw [hc_def]; exact cos_upper t htabs
  have ht4_le : t^4 ≤ t^2 := by nlinarith [huHi, sq_nonneg t, sq_nonneg (t^2)]
  have hcu1 : (1 - t^2/2 + t^4*(5/96)) ≤ 1 := by nlinarith [ht4_le, sq_nonneg t]
  have hcl0 : 0 < 1 - t^2/2 := by nlinarith [huHi]
  -- s = √A₂
  set s := Real.sqrt (A2q q) with hs_def
  have hA2nn : 0 ≤ A2q q := by rw [hA2]; positivity
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hs2 : s^2 = 8*c^2 + 1 := by rw [hs_def, Real.sq_sqrt hA2nn, hA2]
  -- W = cos(θ+2ξ+η), lower bound
  set W := Real.cos (thetaq q + 2 * xiq q + etaq q) with hW_def
  have harg_ub : t + 2*(t/5) + Real.tan t/3 ≤ Real.pi := by
    rw [ht_def]; have := tan_le18 t ht0 (by rw [ht_def] at ht_hi; exact ht_hi)
    nlinarith [ht_hi, Real.pi_gt_d4, this]
  have hWlo : 1 - 1.5138 * t^2 ≤ W := by
    rw [hW_def, ht_def]
    calc 1 - 1.5138 * t^2 ≤ Real.cos (t + 2*(t/5) + Real.tan t/3) := by
          rw [ht_def] at ht_hi; exact cos_arg_ge18 t ht0 ht_hi
      _ ≤ Real.cos (thetaq q + 2 * xiq q + etaq q) := by
          rw [← ht_def]
          have h := cos_arg_lower q hq18 (by rw [← ht_def]; exact harg_ub)
          rw [← ht_def] at h; exact h
  have hWlo0 : (0:ℝ) ≤ 1 - 1.5138 * t^2 := by nlinarith [huHi]
  -- slo = 3 - 1.43 t²
  have hslo0 : (0:ℝ) ≤ 3 - 1.43*t^2 := by nlinarith [huHi]
  have hcL_nn : 0 ≤ 1 - t^2/2 := hcl0.le
  have hc2lo : (1 - t^2/2)^2 ≤ c^2 := by
    have := mul_le_mul hcL hcL hcL_nn (le_trans hcL_nn hcL)
    nlinarith [this]
  have hslo : 3 - 1.43*t^2 ≤ s := by
    -- (3-1.43t²)² ≤ 8(1-t²/2)²+1 (sbound_small_u) ; (1-t²/2)²≤c² ⇒ ≤ 8c²+1 = s²
    have hpure := sbound_small_u (t^2) hu0 hu30
    have hsloc : (3 - 1.43*t^2)^2 ≤ 8*c^2+1 := by nlinarith [hpure, hc2lo]
    nlinarith [hsloc, hs2, hs0, hslo0, sq_nonneg (s - (3-1.43*t^2))]
  have hc2pos : 2*c^2 - 1 ≥ 0 := by nlinarith [hcL, hcl0, huHi]
  -- numeric inequality hnum (pure-u lemma, with t⁴ = (t²)², t² ∈ [0.0186,0.0305])
  have hnum : (48*(1 - t^2/2 + t^4*(5/96))^2+2)*(2*(1 - t^2/2 + t^4*(5/96))^2-1)^2
      ≤ 8*(1 - t^2/2)^3*(3*(1 - t^2/2) + (3 - 1.43*t^2)*(1 - 1.5138 * t^2)) := by
    have h := hnum_small_u (t^2) huLo huHi
    have ht4eq : t^4 = (t^2)^2 := by ring
    rw [ht4eq]; exact h
  -- apply engine
  exact regimeA_engine c (1 - t^2/2) (1 - t^2/2 + t^4*(5/96))
            s (3 - 1.43*t^2) W (1 - 1.5138 * t^2)
            hcl0 hcL hcU hcu1 hs0 hslo hslo0 hWlo hWlo0 hc2pos hnum

/-! ### q ≥ 24 route (loose H ≥ 33π/512 + θ/2) -/

/-- `H ≥ 33π/512 + θ/2` for all q ≥ 18 (`ceil(33q/256) ≥ 33q/256`). -/
theorem H_ge_loose (q : ℕ) (hq : 18 ≤ q) :
    33*Real.pi/512 + thetaq q / 2 ≤ Hq (L_blk q) q := by
  unfold Hq L_blk thetaq
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have hpi := Real.pi_pos
  have hceil : (33 * (q:ℝ))/256 ≤ (⌈(33 * (q:ℝ))/256⌉.toNat : ℝ) := by
    have h1 : (33 * (q:ℝ))/256 ≤ (⌈(33 * (q:ℝ))/256⌉ : ℝ) := Int.le_ceil _
    have h2 : (0:ℤ) ≤ ⌈(33 * (q:ℝ))/256⌉ := Int.ceil_nonneg (by positivity)
    have h3 : ((⌈(33 * (q:ℝ))/256⌉.toNat : ℤ) : ℝ) = (⌈(33 * (q:ℝ))/256⌉ : ℝ) := by
      rw [Int.toNat_of_nonneg h2]
    have h4 : ((⌈(33 * (q:ℝ))/256⌉.toNat : ℕ) : ℝ) = ((⌈(33 * (q:ℝ))/256⌉.toNat : ℤ) : ℝ) := by
      push_cast; ring
    rw [h4, h3]; exact h1
  have hLcast : ((⌈(33 * (q:ℝ))/256⌉.toNat + 2 : ℕ):ℝ) - 1
      = (⌈(33 * (q:ℝ))/256⌉.toNat : ℝ) + 1 := by push_cast; ring
  rw [hLcast]
  -- H = (N+1)·(π/q)/2 where N = ceil.toNat ≥ 33q/256.
  -- 33π/512 + π/(2q) ≤ (N+1)π/(2q)  ⟺  33π/512 ≤ N·π/(2q)  ⟺  33/256 ≤ N/q  ⟺ 33q/256 ≤ N.
  set N := (⌈(33 * (q:ℝ))/256⌉.toNat : ℝ) with hN
  have hmul : 33*Real.pi/256 ≤ N * Real.pi / q := by
    rw [le_div_iff₀ hqr]
    have : 33 * (q:ℝ)/256 * Real.pi ≤ N * Real.pi :=
      mul_le_mul_of_nonneg_right hceil hpi.le
    nlinarith [this, hpi]
  have hkey : 33*Real.pi/512 + (Real.pi/q)/2 ≤ (N + 1) * (Real.pi/q) / 2 := by
    have hexp : (N + 1) * (Real.pi/q) / 2 = N * Real.pi/q/2 + (Real.pi/q)/2 := by ring
    rw [hexp]
    have : 33*Real.pi/512 ≤ N * Real.pi/q/2 := by linarith [hmul]
    linarith [this]
  linarith [hkey]

/-- **q ≥ 24 engine**: same as `regimeA_engine` but the LHS H-cosine is bounded by `Ub ≥ 0`. -/
theorem regimeA_engine24 (c cl cu s slo W Wlo cosH Ub : ℝ)
    (hcl0 : 0 < cl) (hclc : cl ≤ c) (hccu : c ≤ cu)
    (hs0 : 0 ≤ s) (hslo : slo ≤ s) (hslo0 : 0 ≤ slo)
    (hW : Wlo ≤ W) (hWlo0 : 0 ≤ Wlo)
    (hcosH : cosH ≤ Ub) (hUb0 : 0 ≤ Ub) (hcosH0 : 0 ≤ cosH)
    (hnum : (48*cu^2+2)*Ub^2 ≤ 8*cl^3*(3*cl + slo*Wlo)) :
    (12*(2*c)^2+2)*cosH^2 ≤ (2*c)^3*(3*(2*c)/2 + s*W) := by
  have hc0 : 0 < c := lt_of_lt_of_le hcl0 hclc
  have hcu0 : 0 < cu := lt_of_lt_of_le hc0 hccu
  -- LHS: (48c^2+2)cosH^2 ≤ (48cu^2+2)Ub^2
  have hLHS : (12*(2*c)^2+2)*cosH^2 ≤ (48*cu^2+2)*Ub^2 := by
    have h1 : (48*c^2+2) ≤ (48*cu^2+2) := by nlinarith [hccu, hc0.le]
    have h2 : cosH^2 ≤ Ub^2 := by nlinarith [hcosH, hUb0, hcosH0]
    nlinarith [h1, h2, sq_nonneg cosH, mul_nonneg (by positivity : (0:ℝ) ≤ 48*c^2+2) (sq_nonneg cosH)]
  -- RHS lower bound (same as engine)
  have hRHS : 8*cl^3*(3*cl + slo*Wlo) ≤ (2*c)^3*(3*(2*c)/2 + s*W) := by
    have hcl3 : 8*cl^3 ≤ (2*c)^3 := by
      have : (2*cl)^3 ≤ (2*c)^3 := pow_le_pow_left₀ (by linarith) (by linarith) 3
      nlinarith [this]
    have hin : 3*cl + slo*Wlo ≤ 3*(2*c)/2 + s*W := by
      have hsw : slo*Wlo ≤ s*W := by
        calc slo*Wlo ≤ s*Wlo := by nlinarith [hslo, hWlo0]
          _ ≤ s*W := by nlinarith [hW, hs0]
      nlinarith [hclc, hsw]
    have hnn1 : 0 ≤ 3*cl + slo*Wlo := by nlinarith [hcl0.le, hslo0, hWlo0]
    calc 8*cl^3*(3*cl + slo*Wlo) ≤ (2*c)^3*(3*cl+slo*Wlo) := mul_le_mul_of_nonneg_right hcl3 hnn1
      _ ≤ (2*c)^3*(3*(2*c)/2 + s*W) := mul_le_mul_of_nonneg_left hin (by positivity)
  linarith [hLHS, hRHS, hnum]

/-- Pure-`t` numeric inequality (q ≥ 24 route, `t ∈ (0, π/24] ⊆ [0, 0.131]`). Degree 16. -/
theorem hnum24 (t : ℝ) (ht0 : 0 ≤ t) (ht : t ≤ 0.131) :
    (48*(1 - t^2/2 + t^4*(5/96))^2+2) *
      (0.97960*(1 - (t/2)^2/2 + (t/2)^4*(5/96)) - 0.2010*(t/2 - (t/2)^3/6 - (t/2)^4*(5/96)))^2
    ≤ 8*(1 - t^2/2)^3*(3*(1 - t^2/2) + (3 - 1.43*t^2)*(1 - 1.52 * t^2)) := by
  have h2 : 0 ≤ 0.131 - t := by linarith
  nlinarith [ht0, h2, mul_nonneg (pow_nonneg ht0 0) h2, mul_nonneg (pow_nonneg ht0 1) h2,
             mul_nonneg (pow_nonneg ht0 2) h2, mul_nonneg (pow_nonneg ht0 3) h2,
             mul_nonneg (pow_nonneg ht0 4) h2, mul_nonneg (pow_nonneg ht0 5) h2,
             mul_nonneg (pow_nonneg ht0 6) h2, mul_nonneg (pow_nonneg ht0 7) h2,
             pow_nonneg ht0 2, pow_nonneg ht0 4, pow_nonneg ht0 6, pow_nonneg ht0 8,
             pow_nonneg ht0 3, pow_nonneg ht0 5, pow_nonneg ht0 7]

/-- **RegimeACore for q ≥ 24** (loose `H ≥ 33π/512 + θ/2`). -/
theorem regimeA_large (q : ℕ) (hq : 24 ≤ q) : RegimeACore q := by
  have hq18 : 18 ≤ q := by omega
  unfold RegimeACore
  rw [twoA2Blam_eq]
  set t := thetaq q with ht_def
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have ht0 : 0 < t := by rw [ht_def]; unfold thetaq; positivity
  have hq24r : (24:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have ht_hi : t ≤ Real.pi/24 := by
    rw [ht_def]; unfold thetaq
    apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num) hq24r
  have ht_pi23 : t ≤ Real.pi/23 := by have := Real.pi_pos; nlinarith [ht_hi]
  have ht_131 : t ≤ 0.131 := by nlinarith [ht_hi, Real.pi_lt_d4]
  have ht1 : t ≤ 1 := by linarith
  -- A2 = 8 cos²t + 1, lam = 2 cos t
  have hA2 : A2q q = 8 * Real.cos t^2 + 1 := by rw [A2q_eq]
  have hlam : lamq q = 2 * Real.cos t := by unfold lamq; rw [ht_def]; rfl
  rw [hlam]
  set c := Real.cos t with hc_def
  have htabs : |t| ≤ 1 := by rw [abs_of_nonneg ht0.le]; exact ht1
  have huHi : t^2 ≤ (0.0185:ℝ) := by nlinarith [ht_hi, Real.pi_lt_d4, ht0.le]
  have hu0 : (0:ℝ) ≤ t^2 := sq_nonneg t
  -- envelopes
  have hcL : 1 - t^2/2 ≤ c := by rw [hc_def]; exact Real.one_sub_sq_div_two_le_cos
  have hcU : c ≤ 1 - t^2/2 + t^4*(5/96) := by rw [hc_def]; exact cos_upper t htabs
  have ht4_le : t^4 ≤ t^2 := by nlinarith [huHi, sq_nonneg t, sq_nonneg (t^2)]
  have hcl0 : 0 < 1 - t^2/2 := by nlinarith [huHi]
  -- s
  set s := Real.sqrt (A2q q) with hs_def
  have hA2nn : 0 ≤ A2q q := by rw [hA2]; positivity
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hs2 : s^2 = 8*c^2 + 1 := by rw [hs_def, Real.sq_sqrt hA2nn, hA2]
  -- s ≥ 3 - 1.43 t²
  have hslo0 : (0:ℝ) ≤ 3 - 1.43*t^2 := by nlinarith [huHi]
  have hcL_nn : 0 ≤ 1 - t^2/2 := hcl0.le
  have hc2lo : (1 - t^2/2)^2 ≤ c^2 := by
    have := mul_le_mul hcL hcL hcL_nn (le_trans hcL_nn hcL); nlinarith [this]
  have hslo : 3 - 1.43*t^2 ≤ s := by
    have hpure := sbound_small_u (t^2) hu0 (by linarith)
    have hsloc : (3 - 1.43*t^2)^2 ≤ 8*c^2+1 := by nlinarith [hpure, hc2lo]
    nlinarith [hsloc, hs2, hs0, hslo0, sq_nonneg (s - (3-1.43*t^2))]
  -- W = cos(θ+2ξ+η) ≥ 1 - 1.52 t²
  set W := Real.cos (thetaq q + 2 * xiq q + etaq q) with hW_def
  have harg_ub : t + 2*(t/5) + Real.tan t/3 ≤ Real.pi := by
    rw [ht_def]; have := tan_le t ht0 (by rw [ht_def] at ht_pi23; exact ht_pi23)
    nlinarith [ht_hi, Real.pi_gt_d4, this]
  have hWlo : 1 - 1.52 * t^2 ≤ W := by
    rw [hW_def, ht_def]
    calc 1 - 1.52 * t^2 ≤ Real.cos (t + 2*(t/5) + Real.tan t/3) := by
          rw [ht_def] at ht_pi23; exact cos_arg_ge t ht0 ht_pi23
      _ ≤ Real.cos (thetaq q + 2 * xiq q + etaq q) := by
          rw [← ht_def]
          have h := cos_arg_lower q hq18 (by rw [← ht_def]; exact harg_ub)
          rw [← ht_def] at h; exact h
  have hWlo0 : (0:ℝ) ≤ 1 - 1.52 * t^2 := by nlinarith [huHi]
  -- cos H bound: cos(H) ≤ U(t), via H ≥ 33π/512 + t/2 and cosb_ub
  set cosH := Real.cos (Hq (L_blk q) q) with hcosH_def
  set Ub := 0.97960*(1 - (t/2)^2/2 + (t/2)^4*(5/96)) - 0.2010*(t/2 - (t/2)^3/6 - (t/2)^4*(5/96)) with hUb_def
  have hHge : 33*Real.pi/512 + t/2 ≤ Hq (L_blk q) q := by
    rw [ht_def]; exact H_ge_loose q hq18
  have hHlt : Hq (L_blk q) q < Real.pi/2 := H_lt_half_pi q hq18
  have hH33pos : 0 ≤ 33*Real.pi/512 + t/2 := by positivity
  have hcosH_le_cosUH : cosH ≤ Real.cos (33*Real.pi/512 + t/2) := by
    rw [hcosH_def]
    exact Real.cos_le_cos_of_nonneg_of_le_pi hH33pos (by linarith [Real.pi_pos]) hHge
  have hcosUH_le_Ub : Real.cos (33*Real.pi/512 + t/2) ≤ Ub := by
    rw [hUb_def, ht_def]; exact cosb_ub t ht0 (by rw [ht_def] at ht_pi23; exact ht_pi23)
  have hcosH_le_Ub : cosH ≤ Ub := le_trans hcosH_le_cosUH hcosUH_le_Ub
  have hH0 : 0 ≤ Hq (L_blk q) q := le_trans hH33pos hHge
  have hcosH0 : 0 ≤ cosH := by
    rw [hcosH_def]
    exact Real.cos_nonneg_of_mem_Icc ⟨by linarith [Real.pi_pos], by linarith [hHlt]⟩
  have hUb0 : 0 ≤ Ub := le_trans hcosH0 hcosH_le_Ub
  -- numeric inequality
  have hnum : (48*(1 - t^2/2 + t^4*(5/96))^2+2)*Ub^2
      ≤ 8*(1 - t^2/2)^3*(3*(1 - t^2/2) + (3 - 1.43*t^2)*(1 - 1.52 * t^2)) := by
    rw [hUb_def]; exact hnum24 t ht0.le ht_131
  -- apply engine24
  exact regimeA_engine24 c (1 - t^2/2) (1 - t^2/2 + t^4*(5/96)) s (3 - 1.43*t^2)
          W (1 - 1.52 * t^2) cosH Ub
          hcl0 hcL hcU hs0 hslo hslo0 hWlo hWlo0 hcosH_le_Ub hUb0 hcosH0 hnum

/-- **RegimeACore for all q ≥ 18.** -/
theorem regimeA_all (q : ℕ) (hq : 18 ≤ q) : RegimeACore q := by
  by_cases h : q ≤ 23
  · exact regimeA_small q hq h
  · exact regimeA_large q (by omega)

/-! ### RegimeBCore (endpoint, |μc| > H) — comfortable (margin ≥ +5.85) -/

/-- δ = 4H − 2θ/5 ≤ 1.3265 (so cos δ ≥ 0.24). Split q ≤ 23 (δ=7.6θ) / q ≥ 24. -/
theorem delta_le (q : ℕ) (hq : 18 ≤ q) :
    4 * Hq (L_blk q) q - 2 * thetaq q / 5 ≤ 1.3265 := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have ht0 : 0 < thetaq q := by unfold thetaq; positivity
  by_cases hq23 : q ≤ 23
  · rw [show Hq (L_blk q) q = 2 * thetaq q from by rw [Lblk_eq5 q hq hq23]; unfold Hq; push_cast; ring]
    have htle : thetaq q ≤ Real.pi/18 := by
      unfold thetaq; apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num)
        (by exact_mod_cast hq : (18:ℝ) ≤ (q:ℝ))
    nlinarith [htle, Real.pi_lt_d4, ht0]
  · have hq24 : 24 ≤ q := by omega
    have hq24r : (24:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq24
    have hLle : ((L_blk q : ℝ)) ≤ 33*(q:ℝ)/256 + 3 := by
      unfold L_blk
      have h1 : (⌈(33 * (q:ℝ))/256⌉ : ℝ) ≤ 33*(q:ℝ)/256 + 1 := by
        have := Int.ceil_lt_add_one ((33 * (q:ℝ))/256); linarith
      have h2 : (0:ℤ) ≤ ⌈(33 * (q:ℝ))/256⌉ := Int.ceil_nonneg (by positivity)
      have h3 : ((⌈(33 * (q:ℝ))/256⌉.toNat : ℤ) : ℝ) = (⌈(33 * (q:ℝ))/256⌉ : ℝ) := by
        rw [Int.toNat_of_nonneg h2]
      have h4 : ((⌈(33 * (q:ℝ))/256⌉.toNat : ℕ) : ℝ) = ((⌈(33 * (q:ℝ))/256⌉.toNat : ℤ) : ℝ) := by
        push_cast; ring
      push_cast; rw [h4, h3]; linarith
    have hpi := Real.pi_pos
    have hHform : Hq (L_blk q) q = ((L_blk q : ℝ) - 1) * (Real.pi/q) / 2 := by unfold Hq thetaq; ring
    have htheq : thetaq q = Real.pi/q := by unfold thetaq; rfl
    rw [hHform, htheq]
    have hLm1 : ((L_blk q : ℝ) - 1) ≤ 33*(q:ℝ)/256 + 2 := by linarith [hLle]
    rw [show 4 * (((L_blk q : ℝ) - 1) * (Real.pi/q) / 2) - 2 * (Real.pi/q)/5
          = (2*((L_blk q : ℝ) - 1) - 2/5) * (Real.pi/q) from by ring]
    have hbound : (2*((L_blk q : ℝ) - 1) - 2/5) * (Real.pi/q)
        ≤ (2*(33*(q:ℝ)/256 + 2) - 2/5) * (Real.pi/q) :=
      mul_le_mul_of_nonneg_right (by linarith [hLm1]) (by positivity)
    have hsimp : (2*(33*(q:ℝ)/256 + 2) - 2/5) * (Real.pi/q) = 33*Real.pi/128 + 3.6*Real.pi/q := by
      field_simp; ring
    rw [hsimp] at hbound
    have h36 : (3.6:ℝ)*Real.pi/q ≤ 3.6*Real.pi/24 :=
      div_le_div_of_nonneg_left (by positivity) (by norm_num) hq24r
    have hfin : 33*Real.pi/128 + 3.6*Real.pi/q ≤ 1.3265 := by nlinarith [h36, Real.pi_lt_d4]
    linarith [hbound, hfin]

/-- **Arc engine (regime B core).** The reduced linear-on-the-unit-circle inequality
    `25(1 + cosψ·cosδ − sinψ·sinδ) ≤ 24c⁴ + 8c³·s·cosψ`, given `c ∈ [0.9848,1]`,
    `s = √(8c²+1)`, the two Pythagorean relations, `sinψ,sinδ ≥ 0`, `cosψ ≥ −cosδ`,
    and `cosδ ∈ [0.24, 0.69]`.  Margin ≥ +2.9 (closed by nlinarith, split on sign of cosψ). -/
theorem arc_trig (c s cp sp cd sd : ℝ)
    (hc_lo : 0.9846 ≤ c) (hc_hi : c ≤ 1) (hs0 : 0 ≤ s) (hs2 : s^2 = 8*c^2+1)
    (hcsp : cp^2 + sp^2 = 1) (hsp : 0 ≤ sp) (hcp_lo : -cd ≤ cp) (hcp_hi : cp ≤ 1)
    (hcd : cd^2 + sd^2 = 1) (hcd_lo : 0.24 ≤ cd) (hcd_hi : cd ≤ 0.695) (hsd0 : 0 ≤ sd) :
    25*(1 + cp*cd - sp*sd) ≤ 24*c^4 + 8*c^3*s*cp := by
  have hcm : (0:ℝ) ≤ c - 0.9846 := by linarith
  have hc0 : (0:ℝ) ≤ c := by linarith
  have hs_lo : 2.95 ≤ s := by nlinarith [hs2, hs0, hc_lo, hc_hi]
  have hs_hi : s ≤ 3 := by nlinarith [hs2, hs0, hc_lo, hc_hi]
  have hc3_lo : (0.9544:ℝ) ≤ c^3 := by nlinarith [hcm, hc0, sq_nonneg (c-0.9846)]
  have hc3_hi : c^3 ≤ 1 := by nlinarith [hc_lo, hc_hi]
  have hc4eq : c^4 = c^3 * c := by ring
  have hc34 : (0.9544:ℝ) * 0.9846 ≤ c^3 * c :=
    mul_le_mul hc3_lo hc_lo (by norm_num) (by linarith [hc3_lo])
  have hprodeq : (0.9544:ℝ) * 0.9846 = 0.93970224 := by norm_num
  have hc34' : (0.93970224:ℝ) ≤ c^3 * c := hprodeq ▸ hc34
  have hc4 : (22.55:ℝ) ≤ 24*c^4 := by
    have : 24 * (c^3 * c) = 24 * c^4 := by ring
    linarith [hc34', this]
  have h8c3s_lo : (22.5:ℝ) ≤ 8*c^3*s := by nlinarith [hc3_lo, hs_lo, hc3_hi, hs_hi]
  have h8c3s_hi : 8*c^3*s ≤ 24 := by nlinarith [hc3_lo, hs_lo, hc3_hi, hs_hi]
  rcases le_or_gt 0 cp with hcp0 | hcp0
  · have hterm : 22.5*cp ≤ 8*c^3*s*cp := by nlinarith [h8c3s_lo, hcp0]
    nlinarith [hc4, hterm, hcsp, hsp, hcp_lo, hcp_hi, hcd, hcd_lo, hcd_hi, hsd0, hcp0,
               mul_nonneg hsp hsd0, mul_nonneg (by linarith : (0:ℝ) ≤ cp+cd) hsp,
               sq_nonneg (sp-sd), mul_nonneg hcp0 (by linarith : (0:ℝ) ≤ 0.695-cd)]
  · have hterm : 24*cp ≤ 8*c^3*s*cp := by nlinarith [h8c3s_hi, hcp0]
    nlinarith [hc4, hterm, hcsp, hsp, hcp_lo, hcp_hi, hcd, hcd_lo, hcd_hi, hsd0,
               mul_nonneg hsp hsd0, mul_nonneg (by linarith : (0:ℝ) ≤ cp+cd) hsp,
               sq_nonneg (sp-sd), mul_nonneg (by linarith : (0:ℝ) ≤ cp+cd) hsd0]

/-- `tan θ ≤ 1.2 θ` for q ≥ 18 (θ ≤ π/18); gives `η ≤ tanθ/3 ≤ 0.4θ = 2θ/5`. -/
theorem tan_le12 (q : ℕ) (hq : 18 ≤ q) : Real.tan (thetaq q) ≤ 1.2 * thetaq q := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have ht0 : 0 < thetaq q := by unfold thetaq; positivity
  have hq18r : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have ht_hi : thetaq q ≤ Real.pi/18 := by
    unfold thetaq; apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num) hq18r
  exact le_trans (tan_le18 (thetaq q) ht0 ht_hi) (by nlinarith [ht0])

/-- **Corrected regime-B core, ON-DOMAIN** (the file's `RegimeBCore` omits the upper
    bound `|μc| < π/2−H` and is FALSE without it; this is the version `fcorr_lb` needs).
    Margin ≥ +5.85. -/
theorem regimeB_ondomain (q : ℕ) (hq : 18 ≤ q) {muc : ℝ}
    (hmlo : Hq (L_blk q) q < |muc|) (hmhi : |muc| < Real.pi/2 - Hq (L_blk q) q) :
    2 * A2q q * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q) ^ 2
      ≤ lamq q ^ 3 * (3 * lamq q / 2
          + Real.sqrt (A2q q) * Real.cos (2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q)) := by
  rw [twoA2Blam_eq]
  set t := thetaq q with ht_def
  set H := Hq (L_blk q) q with hH_def
  set m := |muc| with hm_def
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have ht0 : 0 < t := by rw [ht_def]; unfold thetaq; positivity
  have ht_lt : t < Real.pi/2 := by
    rw [ht_def]; unfold thetaq; rw [div_lt_div_iff₀ hqr (by norm_num)]
    have h18 : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
    nlinarith [Real.pi_pos]
  have hH0 : 0 ≤ H := by rw [hH_def]; exact le_trans (by positivity) (H_ge_loose q hq)
  have hHlt : H < Real.pi/2 := by rw [hH_def]; exact H_lt_half_pi q hq
  -- set c = cos t, lam = 2c, A2 = 8c²+1
  have hlam : lamq q = 2 * Real.cos t := by unfold lamq; rw [ht_def]; rfl
  rw [hlam]
  set c := Real.cos t with hc_def
  have hcpos : 0 < c := by rw [hc_def]; exact Real.cos_pos_of_mem_Ioo ⟨by linarith, ht_lt⟩
  have hA2 : A2q q = 8 * c^2 + 1 := by rw [hc_def, ht_def]; exact A2q_eq q
  set s := Real.sqrt (A2q q) with hs_def
  have hA2nn : 0 ≤ A2q q := by rw [hA2]; positivity
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hs2 : s^2 = 8*c^2 + 1 := by rw [hs_def, Real.sq_sqrt hA2nn, hA2]
  -- ξ, η bounds
  have hxi_nn : 0 ≤ xiq q := by
    have hsin_pos : 0 ≤ Real.sin t := Real.sin_nonneg_of_nonneg_of_le_pi ht0.le (by linarith [Real.pi_pos])
    have hden_pos : 0 < 3 * lamq q ^ 2 + 1 + lamq q * Real.cos t := by
      have : 0 < lamq q := by unfold lamq; rw [← hc_def, ht_def] at *; positivity
      positivity
    unfold xiq atan2'; rw [ht_def] at *; rw [arg_eq_arctan _ _ (by rw [← ht_def]; exact hden_pos)]
    apply Real.arctan_nonneg.mpr
    have hlampos : 0 < lamq q := by unfold lamq; positivity
    have : 0 ≤ lamq q * Real.sin (thetaq q) := mul_nonneg hlampos.le (by rw [← ht_def] at hsin_pos; rw [ht_def]; exact Real.sin_nonneg_of_nonneg_of_le_pi (by positivity) (by rw [← ht_def]; linarith [Real.pi_pos]))
    positivity
  have hxi_le : xiq q ≤ t/5 := by rw [ht_def]; exact xiq_le q hq
  have heta_nn : 0 ≤ etaq q := etaq_nonneg q hq
  have heta_le : etaq q ≤ Real.tan t / 3 := by rw [ht_def]; exact etaq_le q hq
  have htan_le : Real.tan t ≤ 1.2 * t := by rw [ht_def]; exact tan_le12 q hq
  -- window arg = 2(m-ξ)+η-2H = 2(m-H) + (η - 2ξ); set r = m - H ≥ 0
  set r := m - H with hr_def
  have hr0 : 0 < r := by rw [hr_def]; linarith [hmlo]
  have hr_hi : r < Real.pi/2 - 2*H := by rw [hr_def]; linarith [hmhi]
  -- |η - 2ξ| ≤ 2t/5
  have hd_hi : etaq q - 2 * xiq q ≤ 2*t/5 := by
    have : Real.tan t / 3 ≤ 2*t/5 := by nlinarith [htan_le, ht0]
    linarith [heta_le, hxi_nn, this]
  have hd_lo : -(2*t/5) ≤ etaq q - 2 * xiq q := by linarith [heta_nn, hxi_le]
  -- ψ = 2r + 2t/5 ; the window arg φ = 2r + (η-2ξ) satisfies |φ| ≤ ψ ≤ π
  set phi := 2 * (m - xiq q) + etaq q - 2 * H with hphi_def
  have hphi_eq : phi = 2*r + (etaq q - 2 * xiq q) := by rw [hphi_def, hr_def]; ring
  set psi := 2*r + 2*t/5 with hpsi_def
  have hpsi_nn : 0 ≤ psi := by rw [hpsi_def]; positivity
  -- ψ ≤ π : 2r < π - 4H, and 2t/5 ≤ 4H (since H ≥ 33π/512 ≥ ... and t small)
  have hHge : 33*Real.pi/512 + t/2 ≤ H := by rw [hH_def, ht_def]; exact H_ge_loose q hq
  have ht_small : t ≤ Real.pi/18 := by
    rw [ht_def]; unfold thetaq
    apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num) (by exact_mod_cast hq : (18:ℝ) ≤ (q:ℝ))
  have hpsi_pi : psi ≤ Real.pi := by
    rw [hpsi_def]
    have h4H : 2*t/5 ≤ 4*H := by nlinarith [hHge, ht0, Real.pi_pos, ht_small]
    linarith [hr_hi, h4H]
  -- cos(φ) ≥ cos(ψ): |φ| ≤ ψ ≤ π
  have hphi_abs : |phi| ≤ psi := by
    rw [hphi_eq, hpsi_def, abs_le]; constructor <;> linarith [hd_hi, hd_lo, hr0]
  have hcos_phi : Real.cos psi ≤ Real.cos phi := by
    rw [← Real.cos_abs phi]
    exact Real.cos_le_cos_of_nonneg_of_le_pi (abs_nonneg phi) hpsi_pi hphi_abs
  -- cos²(m+H) = (1 + cos(2(m+H)))/2 = (1 + cos(ψ+δ))/2, δ = 4H - 2t/5
  -- 2(m+H) = 2m+2H = 2(r+H)+2H = 2r+4H = ψ + (4H - 2t/5)
  set delta := 4*H - 2*t/5 with hdelta_def
  have h2mH : 2*(m+H) = psi + delta := by rw [hpsi_def, hdelta_def, hr_def]; ring
  have hcos2 : Real.cos (m+H)^2 = (1 + Real.cos (psi + delta))/2 := by
    have := Real.cos_sq (m+H)
    rw [this]; rw [← h2mH]; ring
  rw [hcos2]
  -- now prove: (12(2c)²+2)·(1+cos(ψ+δ))/2 ≤ (2c)³(3·(2c)/2 + s·cosφ)
  have hsin_psi : 0 ≤ Real.sin psi := Real.sin_nonneg_of_nonneg_of_le_pi hpsi_nn hpsi_pi
  have hexp : Real.cos (psi + delta) = Real.cos psi * Real.cos delta - Real.sin psi * Real.sin delta :=
    Real.cos_add psi delta
  rw [hexp]
  -- δ bounds: 33π/128 ≤ δ ≤ δ_max, giving cosδ ∈ [0.24, 0.69]
  have hdelta_lo : 33*Real.pi/128 ≤ delta := by rw [hdelta_def]; nlinarith [hHge]
  have hdelta_nn : 0 ≤ delta := by linarith [hdelta_lo, Real.pi_pos]
  -- δ ≤ 1.3265 (from delta_le)
  have hdelta_hi : delta ≤ 1.3265 := by rw [hdelta_def, hH_def, ht_def]; exact delta_le q hq
  -- cosδ ∈ [0.24, 0.69]
  have hcd_hi : Real.cos delta ≤ 0.695 := by
    have hmono : Real.cos delta ≤ Real.cos (33*Real.pi/128) :=
      Real.cos_le_cos_of_nonneg_of_le_pi (by positivity) (by linarith [hdelta_lo, Real.pi_pos]) hdelta_lo
    have hnum : Real.cos (33*Real.pi/128) ≤ 0.695 := by
      have hb : |33*Real.pi/128| ≤ 1 := by rw [abs_of_nonneg (by positivity)]; nlinarith [Real.pi_lt_d4]
      have hcb := Real.cos_bound hb; rw [abs_le] at hcb
      have hax : |33*Real.pi/128|^4 = (33*Real.pi/128)^4 := by rw [← abs_pow]; exact abs_of_nonneg (by positivity)
      rw [hax] at hcb
      have hx_lo : (0.80991:ℝ) ≤ 33*Real.pi/128 := by nlinarith [Real.pi_gt_d4]
      have hx_hi : 33*Real.pi/128 ≤ (0.80995:ℝ) := by nlinarith [Real.pi_lt_d4]
      have hx2 : (0.80991:ℝ)^2 ≤ (33*Real.pi/128)^2 := by
        have : (0:ℝ) ≤ 33*Real.pi/128 := by positivity
        nlinarith [hx_lo, this]
      have hx4 : (33*Real.pi/128)^4 ≤ (0.80995:ℝ)^4 := by
        have h2 : (33*Real.pi/128)^2 ≤ (0.80995:ℝ)^2 := by
          have : (0:ℝ) ≤ 33*Real.pi/128 := by positivity
          nlinarith [hx_hi, this]
        nlinarith [h2, sq_nonneg ((33*Real.pi/128)^2)]
      nlinarith [hcb.2, hx2, hx4]
    linarith [hmono, hnum]
  have hcd_lo : 0.24 ≤ Real.cos delta := by
    have hmono : Real.cos (1.3265:ℝ) ≤ Real.cos delta :=
      Real.cos_le_cos_of_nonneg_of_le_pi hdelta_nn (by linarith [Real.pi_gt_three]) hdelta_hi
    have hnum : (0.24:ℝ) ≤ Real.cos (1.3265:ℝ) := by
      -- bound via cos(1.3265) = sin(π/2 − 1.3265), π/2−1.3265 ≈ 0.2443 ∈ (0,1]
      have hshift : Real.cos (1.3265:ℝ) = Real.sin (Real.pi/2 - 1.3265) := by
        rw [Real.sin_pi_div_two_sub]
      rw [hshift]
      have harg_pos : 0 < Real.pi/2 - 1.3265 := by nlinarith [Real.pi_gt_d4]
      have harg_le : Real.pi/2 - 1.3265 ≤ 1 := by nlinarith [Real.pi_lt_d4]
      have hsl := sin_lower (Real.pi/2 - 1.3265) harg_pos.le harg_le
      have ha_lo : (0.2442:ℝ) ≤ Real.pi/2 - 1.3265 := by nlinarith [Real.pi_gt_d4]
      have ha_hi : Real.pi/2 - 1.3265 ≤ (0.2443:ℝ) := by nlinarith [Real.pi_lt_d4]
      set a := Real.pi/2 - 1.3265 with ha_def
      have ha3 : a^3 ≤ (0.2443:ℝ)^3 := by nlinarith [ha_lo, ha_hi, sq_nonneg a, harg_pos.le]
      have ha4 : a^4 ≤ (0.2443:ℝ)^4 := by nlinarith [ha3, ha_hi, harg_pos.le, sq_nonneg a]
      nlinarith [hsl, ha_lo, ha3, ha4]
    linarith [hmono, hnum]
  -- Pythagorean for δ
  have hpyth_d : Real.cos delta^2 + Real.sin delta^2 = 1 := by rw [add_comm]; exact Real.sin_sq_add_cos_sq delta
  have hsd_nn : 0 ≤ Real.sin delta := Real.sin_nonneg_of_nonneg_of_le_pi hdelta_nn (by linarith [hdelta_hi, Real.pi_gt_three])
  -- cosψ ≥ −cosδ:  ψ ≤ π − δ, cos decreasing on [0,π], cos(π−δ) = −cosδ
  have hpsi_le_pimd : psi ≤ Real.pi - delta := by
    rw [hpsi_def, hdelta_def, hr_def]; linarith [hmhi, hH_def]
  have hcp_lo : -Real.cos delta ≤ Real.cos psi := by
    have h1 : Real.cos (Real.pi - delta) ≤ Real.cos psi :=
      Real.cos_le_cos_of_nonneg_of_le_pi hpsi_nn (by linarith [hdelta_nn]) hpsi_le_pimd
    rwa [Real.cos_pi_sub] at h1
  have hpyth_p : Real.cos psi^2 + Real.sin psi^2 = 1 := by rw [add_comm]; exact Real.sin_sq_add_cos_sq psi
  have hcp_hi : Real.cos psi ≤ 1 := Real.cos_le_one psi
  -- c bounds: c = cos t ≥ cos(π/18) ≥ 0.9848, c ≤ 1
  have hc_lo : (0.9846:ℝ) ≤ c := by
    rw [hc_def]
    have ht18 : t ≤ Real.pi/18 := ht_small
    have hmono : Real.cos (Real.pi/18) ≤ Real.cos t :=
      Real.cos_le_cos_of_nonneg_of_le_pi ht0.le (by linarith [Real.pi_le_four, Real.pi_pos]) ht18
    have hnum : (0.9846:ℝ) ≤ Real.cos (Real.pi/18) := by
      have hb : |Real.pi/18| ≤ 1 := by rw [abs_of_nonneg (by positivity)]; nlinarith [Real.pi_lt_d4]
      have hcl := cos_lower (Real.pi/18) hb
      have hy_lo : (0.17452:ℝ) ≤ Real.pi/18 := by nlinarith [Real.pi_gt_d4]
      have hy_hi : Real.pi/18 ≤ (0.17454:ℝ) := by nlinarith [Real.pi_lt_d4]
      have hy2 : (Real.pi/18)^2 ≤ (0.17454:ℝ)^2 := by nlinarith [hy_lo, hy_hi, sq_nonneg (Real.pi/18)]
      have hy4 : (Real.pi/18)^4 ≤ (0.17454:ℝ)^4 := by nlinarith [hy2, sq_nonneg ((Real.pi/18)^2)]
      nlinarith [hcl, hy2, hy4]
    linarith [hmono, hnum]
  have hc_hi : c ≤ 1 := Real.cos_le_one t
  -- reduce RHS using cosφ ≥ cosψ, s ≥ 0
  have hsphi : s * Real.cos psi ≤ s * Real.cos phi := mul_le_mul_of_nonneg_left hcos_phi hs0
  -- apply arc_trig
  have harc := arc_trig c s (Real.cos psi) (Real.sin psi) (Real.cos delta) (Real.sin delta)
    hc_lo hc_hi hs0 hs2 hpyth_p hsin_psi hcp_lo hcp_hi hpyth_d hcd_lo hcd_hi hsd_nn
  -- final: goal is (12(2c)²+2)(1+(cosψcosδ−sinψsinδ))/2 ≤ (2c)³(3(2c)/2 + s cosφ)
  -- LHS = (48c²+2)/2·(1+...) ≤ 25·(1+...) [c≤1, bracket≥0]; RHS ≥ 24c⁴+8c³ s cosψ [via hsphi]
  have hbracket_nn : 0 ≤ 1 + (Real.cos psi*Real.cos delta - Real.sin psi*Real.sin delta) := by
    have : Real.cos psi*Real.cos delta - Real.sin psi*Real.sin delta = Real.cos (psi+delta) := hexp.symm
    rw [this]; linarith [Real.neg_one_le_cos (psi+delta)]
  nlinarith [harc, hsphi, hbracket_nn, hc_lo, hc_hi, sq_nonneg c, hs0,
             mul_nonneg (by linarith [hc_hi] : (0:ℝ) ≤ 1 - c) hbracket_nn,
             mul_nonneg (by positivity : (0:ℝ) ≤ (2*c)^3) (sub_nonneg.mpr hcos_phi)]

/-- **Regime-A pigeonhole index.**  For `L ≥ 1`, `θ > 0`, `|2μc| ≤ (L−1)θ`, there is a
    window index `n ∈ range L` whose offset `(2n−(L−1))θ` cancels `2μc` to within `θ`. -/
theorem pigeon_idx (L : ℕ) (hL : 1 ≤ L) (θ μc : ℝ) (hθ : 0 < θ)
    (hbd : |2*μc| ≤ ((L:ℝ)-1)*θ) :
    ∃ n ∈ Finset.range L, |2*μc + (2*(n:ℝ)-((L:ℝ)-1))*θ| ≤ θ := by
  set y := ((L:ℝ)-1) - 2*μc/θ with hy
  have hθ' : θ ≠ 0 := ne_of_gt hθ
  have hybd : 0 ≤ y ∧ y ≤ 2*((L:ℝ)-1) := by
    rw [abs_le] at hbd
    refine ⟨?_, ?_⟩
    · rw [hy]; have : 2*μc/θ ≤ (L:ℝ)-1 := by rw [div_le_iff₀ hθ]; nlinarith [hbd.2]
      linarith
    · rw [hy]; have : -(((L:ℝ)-1)) ≤ 2*μc/θ := by rw [le_div_iff₀ hθ]; nlinarith [hbd.1]
      linarith
  set n0 : ℤ := ⌊y/2 + 1/2⌋ with hn0
  have hn0_bd : |2*(n0:ℝ) - y| ≤ 1 := by
    have h1 := Int.floor_le (y/2+1/2); have h2 := Int.lt_floor_add_one (y/2+1/2)
    rw [abs_le]; constructor <;> [nlinarith [h2]; nlinarith [h1]]
  have hn0_nn : 0 ≤ n0 := by rw [hn0]; apply Int.floor_nonneg.mpr; nlinarith [hybd.1]
  have hn0_lt : n0 < L := by
    rw [hn0]; rw [Int.floor_lt]; push_cast; nlinarith [hybd.2]
  refine ⟨n0.toNat, Finset.mem_range.mpr (by omega), ?_⟩
  have hcast : ((n0.toNat : ℕ):ℝ) = (n0:ℝ) := by
    have : ((n0.toNat : ℤ):ℝ) = (n0:ℝ) := by rw [Int.toNat_of_nonneg hn0_nn]
    push_cast at this ⊢; linarith [this]
  have hmuc_eq : 2*μc = (((L:ℝ)-1) - y)*θ := by rw [hy]; field_simp; ring
  rw [hcast, hmuc_eq]
  have hrw : ((((L:ℝ)-1) - y)*θ + (2*(n0:ℝ)-((L:ℝ)-1))*θ) = (2*(n0:ℝ) - y)*θ := by ring
  rw [hrw, abs_mul, abs_of_pos hθ]
  calc |2*(n0:ℝ) - y| * θ ≤ 1 * θ := mul_le_mul_of_nonneg_right hn0_bd hθ.le
    _ = θ := by ring

/-- `2ξ ≤ η` for q ≥ 18.  Reduces (arctan double-angle `arctan u + arctan u =
    arctan(2u/(1−u²))` + monotonicity) to the algebraic `tanθ/3 ≥ 2ND/(D²−N²)`
    (`N=λsinθ`, `D=3λ²+1+λcosθ`), which after clearing denominators is `32c⁴+12c²+1 ≥ 0`. -/
theorem eta_ge_2xi (q : ℕ) (hq : 18 ≤ q) : 2 * xiq q ≤ etaq q := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  set θ := thetaq q with hθdef
  have ht0 : 0 < θ := by rw [hθdef]; unfold thetaq; positivity
  have htlt : θ < Real.pi/2 := by
    rw [hθdef]; unfold thetaq; rw [div_lt_div_iff₀ hqr (by norm_num)]
    have h18 : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
    nlinarith [Real.pi_pos]
  have hc : 0 < Real.cos θ := Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], htlt⟩
  have hs : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi ht0 (by linarith [Real.pi_pos])
  set lam := lamq q with hlamdef
  have hlam : lam = 2 * Real.cos θ := by rw [hlamdef, hθdef]; rfl
  set N := lam * Real.sin θ with hN
  set D := 3*lam^2 + 1 + lam * Real.cos θ with hD
  have hD_pos : 0 < D := by rw [hD, hlam]; positivity
  have hN_nn : 0 ≤ N := by rw [hN, hlam]; positivity
  set u := N / D with hu
  have hu_nn : 0 ≤ u := div_nonneg hN_nn hD_pos.le
  have hxi_eq : xiq q = Real.arctan u := by
    unfold xiq atan2'; rw [hθdef] at hD; rw [hu, hN, hD]
    rw [arg_eq_arctan _ _ (by rw [hlam] at *; rw [← hθdef]; positivity)]
  have heta_eq : etaq q = Real.arctan (Real.tan θ / 3) := by
    unfold etaq atan2'; rw [hθdef]
    rw [arg_eq_arctan _ _ (by positivity)]
    congr 1; rw [Real.tan_eq_sin_div_cos]; field_simp
  have hu_lt1 : u < 1 := by
    rw [hu, div_lt_one hD_pos, hN, hD, hlam]
    nlinarith [hc, hs, Real.sin_sq_add_cos_sq θ, mul_pos hc hc]
  have huu_lt1 : u * u < 1 := by nlinarith [hu_nn, hu_lt1]
  have h2xi : 2 * Real.arctan u = Real.arctan ((u + u)/(1 - u*u)) := by
    rw [← Real.arctan_add huu_lt1]; ring
  rw [hxi_eq, heta_eq, h2xi]
  apply Real.arctan_mono
  have h1mu : 0 < 1 - u*u := by linarith [huu_lt1]
  have hkey : (u + u)/(1 - u*u) = (2*N*D)/(D^2 - N^2) := by rw [hu]; field_simp; ring
  rw [hkey, Real.tan_eq_sin_div_cos]
  have hDN_pos : 0 < D^2 - N^2 := by
    have : N < D := by rw [hu] at hu_lt1; exact (div_lt_one hD_pos).mp hu_lt1
    nlinarith [this, hN_nn, hD_pos]
  rw [div_div, div_le_div_iff₀ hDN_pos (by positivity)]
  rw [hN, hD, hlam]
  nlinarith [hc, hs, Real.sin_sq_add_cos_sq θ, mul_pos hc hc, mul_pos hs hs,
             sq_nonneg (Real.cos θ), sq_nonneg (Real.sin θ),
             mul_pos (mul_pos hc hc) (mul_pos hc hc)]

-- helper: cos θ > 0, sin θ ≥ 0, tan bounds for q ≥ 18 (consolidated)
theorem theta_facts (q : ℕ) (hq : 18 ≤ q) :
    0 < thetaq q ∧ thetaq q ≤ Real.pi/18 ∧ 0 < Real.cos (thetaq q) ∧ 0 ≤ Real.sin (thetaq q) := by
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have hq18r : (18:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have ht0 : 0 < thetaq q := by unfold thetaq; positivity
  have hthi : thetaq q ≤ Real.pi/18 := by
    unfold thetaq; apply div_le_div_of_nonneg_left Real.pi_pos.le (by norm_num) hq18r
  have htlt : thetaq q < Real.pi/2 := by
    have := Real.pi_pos; unfold thetaq; rw [div_lt_div_iff₀ hqr (by norm_num)]; nlinarith
  have hcos : 0 < Real.cos (thetaq q) := Real.cos_pos_of_mem_Ioo ⟨by linarith, htlt⟩
  have hsin : 0 ≤ Real.sin (thetaq q) :=
    Real.sin_nonneg_of_nonneg_of_le_pi ht0.le (by linarith [Real.pi_pos])
  exact ⟨ht0, hthi, hcos, hsin⟩

end RegimeCores

set_option maxHeartbeats 1000000 in
/-- **(B1b — PROVED)** For all q ≥ 18 and μc in the domain,
    `fcorr (L_blk q) q hL μc ≥ 1 / lamq q ^ 3`.

    **Corrected proof architecture** (the old `windowMaxCos_lb` route is invalid:
    windowMaxCos is NOT ≥ 2√6/5 — it can be ≈ -0.68 near the endpoints).

    Write L = L_blk q, θ = π/q, λ = 2cosθ, A₂ = 1+2λ², H = (L-1)θ/2, ξ = xiq q, η = etaq q.
    The denominator `2·A₂·Blam²·cos²(|μc|+H)` is positive (`denom_cos_sq_pos`,
    `H_lt_half_pi`), so `1/λ³ ≤ fcorr` is equivalent to the pointwise inequality
      (P)  2·A₂·Blam²·cos²(|μc|+H) ≤ λ³·(3λ/2 + √A₂ · W),   W := windowMaxCos … μc.
    Lower-bound W by ONE window index n* (via `Finset.le_sup'`), chosen so that the
    phase φ_{n*} = 2(μc-ξ) + (2n*-(L-1))θ + η is as close to 0 as possible:
      • Regime A (|μc| ≤ H):  some n* gives |2μc + (2n*-(L-1))θ| ≤ θ (the offsets
        (2n*-(L-1))θ are 2θ-spaced and cover [-2H,2H] ∋ -2μc), hence
        |φ_{n*}| ≤ θ + 2ξ + η and W ≥ cos(θ+2ξ+η).  Since cos²(|μc|+H) ≤ cos²(H),
        (P) reduces to `RegimeACore q` (above).
      • Regime B (H < |μc| < π/2-H):  the endpoint index gives `RegimeBCore q muc`.

    **Status (2026-06-14).  BOTH POINTWISE CORES ARE NOW PROVED (sorry-free,
    axioms = [propext, Classical.choice, Quot.sound]).**  See `section RegimeCores`:
    • `regimeA_all q : RegimeACore q` — for ALL q ≥ 18, via `regimeA_small`
      (q ∈ {18..23}, exact H = 2θ) + `regimeA_large` (q ≥ 24, loose H), built on the
      key algebraic identity `twoA2Blam_eq : 2·A₂·Blam² = 12λ²+2` and the Taylor
      envelopes; the binding case is `cos_sq_lt`.
    • `regimeB_ondomain q (hmlo : H<|μc|) (hmhi : |μc|<π/2−H) : <regimeB inequality>`
      — the CORRECTED regime-B core (the file's `RegimeBCore` def OMITS the upper bound
      `|μc| < π/2−H` and is FALSE without it; the on-domain version is what fcorr_lb
      needs). Reduced to the unit-circle `arc_trig` lemma (margin ≥ +2.8; NOT +0.0175 —
      regime B is comfortable, not the bottleneck). Uses `delta_le`, `tan_le12`.

    **Remaining (the ONLY residual): the windowMaxCos `Finset.le_sup'` index selection
    + denominator reduction + regime split** — combinatorial wiring, NO new mathematics:
      (a) denom>0 ⇒ reduce `1/λ³ ≤ fcorr` to (P) via `denom_cos_sq_pos`/`H_lt_half_pi`;
      (b) regime A (|μc|≤H): pigeonhole integer n* = round(((L−1)−2μc/θ)/2) ∈ range L
          giving `|2μc+(2n*−(L−1))θ| ≤ θ`, hence `windowMaxCos ≥ cos(θ+2ξ+η)` by
          `Finset.le_sup'`; then `cos²(|μc|+H) ≤ cos²(H)` and apply `regimeA_all`;
      (c) regime B (H<|μc|): endpoint index n*=L−1 gives the `regimeB_ondomain` arg;
          apply `regimeB_ondomain`.
    All the analytic inequalities are discharged; only (a)/(b)/(c) bookkeeping is left.
    Full report: `research_notes/fcorr_lb_attempt_2026-06-13.md`.
-/
theorem fcorr_lb (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q)
    {muc : ℝ} (hmuc : muc ∈ Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q)) :
    1 / lamq q ^ 3 ≤ fcorr (L_blk q) q hL muc := by
  obtain ⟨hmlo0, hmhi0⟩ := hmuc
  obtain ⟨hθ0, hθ18, hcosθ, hsinθ⟩ := theta_facts q hq
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast (by omega : 0 < q)
  have hH0 : 0 ≤ Hq (L_blk q) q := le_trans (by positivity) (H_ge_loose q hq)
  have hHlt : Hq (L_blk q) q < Real.pi/2 := H_lt_half_pi q hq
  have hlam_pos : 0 < lamq q := by unfold lamq; positivity
  have hA2_pos : 0 < A2q q := by unfold A2q; positivity
  have hBlam_pos : 0 < Blamq q := by
    unfold Blamq; apply div_pos (Real.sqrt_pos.mpr (by positivity)) (by positivity)
  have hcosH_pos : 0 < Real.cos (|muc| + Hq (L_blk q) q) := denom_cos_pos hH0 hHlt ⟨hmlo0, hmhi0⟩
  have hdenom_pos : 0 < 2 * A2q q * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q) ^ 2 := by
    have := sq_pos_of_pos hcosH_pos; positivity
  have habs_lt : |muc| < Real.pi/2 - Hq (L_blk q) q := by rw [abs_lt]; exact ⟨by linarith, hmhi0⟩
  -- ξ, η bounds
  have hxi_nn : 0 ≤ xiq q := by
    have hden_pos : 0 < 3 * lamq q ^ 2 + 1 + lamq q * Real.cos (thetaq q) := by positivity
    unfold xiq atan2'; rw [arg_eq_arctan _ _ hden_pos]
    exact Real.arctan_nonneg.mpr (by positivity)
  have heta_nn : 0 ≤ etaq q := etaq_nonneg q hq
  have hxi_le : xiq q ≤ thetaq q/5 := xiq_le q hq
  have heta_le : etaq q ≤ Real.tan (thetaq q)/3 := etaq_le q hq
  have htan_nn : 0 ≤ Real.tan (thetaq q) := by
    rw [Real.tan_eq_sin_div_cos]; exact div_nonneg hsinθ hcosθ.le
  have htan_le : Real.tan (thetaq q) ≤ 1.2*thetaq q := tan_le12 q hq
  have hargpi : thetaq q + 2*xiq q + etaq q ≤ Real.pi := by
    nlinarith [hxi_le, heta_le, htan_le, hθ18, Real.pi_gt_d4, hθ0]
  -- reduce 1/λ³ ≤ fcorr to (P): 1/λ³ ≤ N/D  ⟺  D ≤ N·λ³  (D,λ³>0)
  rw [fcorr, div_le_div_iff₀ (by positivity) hdenom_pos, one_mul]
  -- goal: 2A2Blam²cos²(|μc|+H) ≤ (3λ/2 + √A₂ W) * λ³
  -- It suffices to show  (P') 2A2Blam²cos²(|μc|+H) ≤ λ³(3λ/2 + √A₂ W). reorder:
  rw [show (3 * lamq q / 2 + Real.sqrt (A2q q) * windowMaxCos (L_blk q) q hL muc) * lamq q ^ 3
        = lamq q ^ 3 * (3 * lamq q / 2 + Real.sqrt (A2q q) * windowMaxCos (L_blk q) q hL muc) from by ring]
  -- W lower bound depends on regime
  by_cases hregA : |muc| ≤ Hq (L_blk q) q
  · -- REGIME A
    have hLθ : ((L_blk q:ℝ)-1)*thetaq q = 2*Hq (L_blk q) q := by unfold Hq; ring
    have h2bd : |2*muc| ≤ ((L_blk q:ℝ)-1)*thetaq q := by
      rw [hLθ, show (2:ℝ)*muc = 2*muc from rfl, abs_mul, abs_two]
      have : |muc| ≤ Hq (L_blk q) q := hregA; linarith
    obtain ⟨n, hn_mem, hn_bd⟩ := pigeon_idx (L_blk q) (by omega) (thetaq q) muc hθ0 h2bd
    have hwin_ge : Real.cos (2 * (muc - xiq q) + ((2*(n:ℝ)-((L_blk q:ℝ)-1))*thetaq q) + etaq q)
        ≤ windowMaxCos (L_blk q) q hL muc := by
      apply Finset.le_sup' (s := Finset.range (L_blk q))
        (f := fun n => Real.cos (2 * (muc - xiq q) + ((2 * (n : ℝ) - ((L_blk q : ℝ) - 1)) * thetaq q) + etaq q))
      exact hn_mem
    set φ := 2 * (muc - xiq q) + ((2*(n:ℝ)-((L_blk q:ℝ)-1))*thetaq q) + etaq q with hφdef
    have hφ_abs : |φ| ≤ thetaq q + 2*xiq q + etaq q := by
      have hrw : φ = (2*muc + (2*(n:ℝ)-((L_blk q:ℝ)-1))*thetaq q) + (etaq q - 2*xiq q) := by
        rw [hφdef]; ring
      rw [hrw]
      calc |(2*muc + (2*(n:ℝ)-((L_blk q:ℝ)-1))*thetaq q) + (etaq q - 2*xiq q)|
          ≤ |2*muc + (2*(n:ℝ)-((L_blk q:ℝ)-1))*thetaq q| + |etaq q - 2*xiq q| := abs_add_le _ _
        _ ≤ thetaq q + (2*xiq q + etaq q) := by
            apply add_le_add hn_bd; rw [abs_le]; constructor <;> linarith [hxi_nn, heta_nn]
        _ = thetaq q + 2*xiq q + etaq q := by ring
    have hcos_ge : Real.cos (thetaq q + 2*xiq q + etaq q) ≤ Real.cos φ := by
      rw [← Real.cos_abs φ]
      exact Real.cos_le_cos_of_nonneg_of_le_pi (abs_nonneg φ) hargpi hφ_abs
    have hW_ge : Real.cos (thetaq q + 2*xiq q + etaq q) ≤ windowMaxCos (L_blk q) q hL muc :=
      le_trans hcos_ge hwin_ge
    -- RegimeACore
    have hcore := regimeA_all q hq
    unfold RegimeACore at hcore
    -- cos²(|μc|+H) ≤ cos²(H)
    have hcosH2_le : Real.cos (|muc| + Hq (L_blk q) q)^2 ≤ Real.cos (Hq (L_blk q) q) ^ 2 := by
      have h1 : Real.cos (|muc| + Hq (L_blk q) q) ≤ Real.cos (Hq (L_blk q) q) :=
        Real.cos_le_cos_of_nonneg_of_le_pi hH0 (by linarith [habs_lt]) (by linarith [abs_nonneg muc])
      have h2 : 0 ≤ Real.cos (Hq (L_blk q) q) :=
        Real.cos_nonneg_of_mem_Icc ⟨by linarith [Real.pi_pos], by linarith⟩
      nlinarith [h1, h2, hcosH_pos]
    have hWfull : 3 * lamq q / 2 + Real.sqrt (A2q q) * Real.cos (thetaq q + 2 * xiq q + etaq q)
        ≤ 3 * lamq q / 2 + Real.sqrt (A2q q) * windowMaxCos (L_blk q) q hL muc := by
      have := mul_le_mul_of_nonneg_left hW_ge (Real.sqrt_nonneg (A2q q)); linarith [this]
    have hLHS : 2 * A2q q * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q)^2
        ≤ 2 * A2q q * Blamq q ^ 2 * Real.cos (Hq (L_blk q) q) ^ 2 :=
      mul_le_mul_of_nonneg_left hcosH2_le (by positivity)
    calc 2 * A2q q * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q) ^ 2
        ≤ 2 * A2q q * Blamq q ^ 2 * Real.cos (Hq (L_blk q) q) ^ 2 := hLHS
      _ ≤ lamq q ^ 3 * (3 * lamq q / 2 + Real.sqrt (A2q q) * Real.cos (thetaq q + 2 * xiq q + etaq q)) := hcore
      _ ≤ lamq q ^ 3 * (3 * lamq q / 2 + Real.sqrt (A2q q) * windowMaxCos (L_blk q) q hL muc) :=
          mul_le_mul_of_nonneg_left hWfull (by positivity)
  · -- REGIME B (endpoint), |muc| > H
    push_neg at hregA
    have hHθ : ((L_blk q:ℝ)-1)*thetaq q = 2*Hq (L_blk q) q := by unfold Hq; ring
    -- regimeB_ondomain gives the core inequality with cos(2(|μc|−ξ)+η−2H)
    have hcore := regimeB_ondomain q hq hregA habs_lt
    -- need windowMaxCos ≥ cos(2(|μc|−ξ)+η−2H)
    have hmem0 : (0:ℕ) ∈ Finset.range (L_blk q) := Finset.mem_range.mpr (by omega)
    have hmemL : (L_blk q - 1) ∈ Finset.range (L_blk q) := Finset.mem_range.mpr (by omega)
    have hW_ge : Real.cos (2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q)
        ≤ windowMaxCos (L_blk q) q hL muc := by
      rcases le_or_gt 0 muc with hmuc0 | hmuc0
      · -- μc ≥ 0: |μc| = μc, n=0 phase = 2(μc−ξ)−(L−1)θ+η = regimeB arg exactly
        have habseq : |muc| = muc := abs_of_nonneg hmuc0
        have hwin0 : Real.cos (2 * (muc - xiq q) + ((2*(0:ℕ)-((L_blk q:ℝ)-1))*thetaq q) + etaq q)
            ≤ windowMaxCos (L_blk q) q hL muc := by
          apply Finset.le_sup' (s := Finset.range (L_blk q))
            (f := fun n => Real.cos (2 * (muc - xiq q) + ((2 * (n : ℝ) - ((L_blk q : ℝ) - 1)) * thetaq q) + etaq q))
          exact hmem0
        have hphaseeq : 2 * (muc - xiq q) + ((2*(0:ℕ)-((L_blk q:ℝ)-1))*thetaq q) + etaq q
            = 2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q := by
          rw [habseq]; push_cast; rw [show (2*(0:ℝ)-((L_blk q:ℝ)-1)) = -(((L_blk q:ℝ)-1)) from by ring]
          have : -(((L_blk q:ℝ)-1)) * thetaq q = -2*Hq (L_blk q) q := by rw [show -(((L_blk q:ℝ)-1)) * thetaq q = -((((L_blk q:ℝ)-1))*thetaq q) from by ring, hHθ]; ring
          rw [this]; ring
        rwa [hphaseeq] at hwin0
      · -- μc < 0: |μc| = −μc, n=L−1 phase; use cos evenness + eta_ge_2xi
        have habseq : |muc| = -muc := abs_of_neg hmuc0
        have hwinL : Real.cos (2 * (muc - xiq q) + ((2*((L_blk q - 1:ℕ):ℝ)-((L_blk q:ℝ)-1))*thetaq q) + etaq q)
            ≤ windowMaxCos (L_blk q) q hL muc := by
          apply Finset.le_sup' (s := Finset.range (L_blk q))
            (f := fun n => Real.cos (2 * (muc - xiq q) + ((2 * (n : ℝ) - ((L_blk q : ℝ) - 1)) * thetaq q) + etaq q))
          exact hmemL
        -- phase_{L-1} = 2(μc-ξ)+(L-1)θ+η.  By cos even, = cos(2(|μc|+ξ)−2H−η).
        have hLcast : ((L_blk q - 1 : ℕ):ℝ) = (L_blk q:ℝ) - 1 := by
          have : 1 ≤ L_blk q := hL; push_cast [Nat.cast_sub this]; ring
        set ψL := 2 * (muc - xiq q) + ((2*((L_blk q - 1:ℕ):ℝ)-((L_blk q:ℝ)-1))*thetaq q) + etaq q with hψL
        -- ψL = 2(μc-ξ)+(L-1)θ+η = -(2|μc|+2ξ-2H-η)  (μc<0)
        have hψL_eq : ψL = -(2*|muc| + 2*xiq q - 2*Hq (L_blk q) q - etaq q) := by
          rw [hψL, hLcast, habseq]
          rw [show (2*((L_blk q:ℝ)-1)-((L_blk q:ℝ)-1)) = ((L_blk q:ℝ)-1) from by ring]
          have hh : ((L_blk q:ℝ)-1)*thetaq q = 2*Hq (L_blk q) q := hHθ
          nlinarith [hh] -- linear identity
        -- target arg A = 2(|μc|−ξ)+η−2H. |−ψL| = 2|μc|+2ξ−2H−η, |A| = 2|μc|−2ξ+η−2H.
        -- |−ψL| − |A| = 4ξ − 2η = −2(η−2ξ) ≤ 0 by eta_ge_2xi. So |ψL| ≤ |A| ⟹ cos(ψL) ≥ cos(A).
        have heta2xi := eta_ge_2xi q hq
        -- A = 2|μc|−2ξ+η−2H ≥ 0;  set B = 2|μc|+2ξ−2H−η (= −ψL).  |B| ≤ A ≤ π.
        have hxile : xiq q ≤ thetaq q/5 := xiq_le q hq
        have hregA' : Hq (L_blk q) q < |muc| := hregA
        have hA_lo : 0 ≤ 2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q := by
          nlinarith [hregA', hxile, hxi_nn, heta_nn, hθ0]
        have hHge : 33*Real.pi/512 + thetaq q/2 ≤ Hq (L_blk q) q := H_ge_loose q hq
        have hA_pi : 2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q ≤ Real.pi := by
          nlinarith [habs_lt, hxi_nn, heta_le, htan_le, hθ0, hθ18, Real.pi_gt_d4, hxile, hHge]
        -- |B| ≤ A:  B ≤ A  (4ξ−2η ≤ 0 by eta_ge_2xi)  and  −B ≤ A  (−B = η+2H−2|μc|−2ξ ≤ A near boundary)
        have hB_le_A : 2*|muc| + 2*xiq q - 2*Hq (L_blk q) q - etaq q
            ≤ 2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q := by nlinarith [heta2xi]
        have hnegB_le_A : -(2*|muc| + 2*xiq q - 2*Hq (L_blk q) q - etaq q)
            ≤ 2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q := by
          nlinarith [hregA', hxi_nn, heta_nn]
        have hcos_ge : Real.cos (2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q) ≤ Real.cos ψL := by
          rw [hψL_eq]
          rw [Real.cos_neg, ← Real.cos_abs (2*|muc| + 2*xiq q - 2*Hq (L_blk q) q - etaq q)]
          apply Real.cos_le_cos_of_nonneg_of_le_pi (abs_nonneg _) hA_pi
          rw [abs_le]; exact ⟨by linarith [hnegB_le_A], hB_le_A⟩
        exact le_trans hcos_ge hwinL
    -- apply regimeB core (rewrite twoA2Blam in hcore)
    have hcore2 : 2 * A2q q * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q) ^ 2
        ≤ lamq q ^ 3 * (3 * lamq q / 2 + Real.sqrt (A2q q) * windowMaxCos (L_blk q) q hL muc) := by
      have hWfull : 3 * lamq q / 2 + Real.sqrt (A2q q) * Real.cos (2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q)
          ≤ 3 * lamq q / 2 + Real.sqrt (A2q q) * windowMaxCos (L_blk q) q hL muc := by
        have := mul_le_mul_of_nonneg_left hW_ge (Real.sqrt_nonneg (A2q q)); linarith [this]
      calc 2 * A2q q * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q) ^ 2
          ≤ lamq q ^ 3 * (3 * lamq q / 2 + Real.sqrt (A2q q) * Real.cos (2 * (|muc| - xiq q) + etaq q - 2 * Hq (L_blk q) q)) := hcore
        _ ≤ lamq q ^ 3 * (3 * lamq q / 2 + Real.sqrt (A2q q) * windowMaxCos (L_blk q) q hL muc) :=
            mul_le_mul_of_nonneg_left hWfull (by positivity)
    exact hcore2


/-! ### B1_target: sInf bound (sorry-from-fcorr_lb + proved sInf argument) -/

/-- **(B1c)** The domain is nonempty. -/
theorem domain_nonempty (q : ℕ) (hq : 18 ≤ q) :
    (Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q)).Nonempty := by
  have hH_lt : Hq (L_blk q) q < Real.pi / 2 := H_lt_half_pi q hq
  refine ⟨0, ?_⟩
  simp only [Set.mem_Ioo]
  constructor <;> linarith

/-- **(B1_target — PROVED via fcorr_lb)** For all q ≥ 18,
    `1/λ³ ≤ g_corr (L_blk q) q hL`.

    **Proof structure (proved except for `fcorr_lb`)**: Since the domain is nonempty
    and `fcorr ≥ 1/λ³` pointwise (from `fcorr_lb`), `sInf (image fcorr D) ≥ 1/λ³`
    by `le_csInf` + pointwise bound.
-/
theorem B1_target (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q) :
    1 / lamq q ^ 3 ≤ g_corr (L_blk q) q hL := by
  unfold g_corr
  have hH_lt : Hq (L_blk q) q < Real.pi / 2 := H_lt_half_pi q hq
  have hdom_nonempty := domain_nonempty q hq
  have himage_nonempty : (Set.image (fcorr (L_blk q) q hL)
        (Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q))).Nonempty :=
    hdom_nonempty.image _
  apply le_csInf himage_nonempty
  rintro y ⟨muc, hmuc, rfl⟩
  exact fcorr_lb q hq hL hmuc

end

/-! ### Axiom checks -/


end L1bArcCoverage



#print axioms L1bArcCoverage.fcorr_lb
#print axioms L1bArcCoverage.B1_target
