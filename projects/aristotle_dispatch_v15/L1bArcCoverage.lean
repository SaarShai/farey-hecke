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

## What is left as a sorry

6. **fcorr_lb**: fcorr ≥ 1/λ³ pointwise on domain.  This is TRUE (the minimum of
   fcorr over the domain is at μc = 0), but the proof is a delicate two-regime
   argument with a razor-thin q-uniform core tied to `cos_sq_lt`; see its docstring.
7. **B1_target**: sInf ≥ 1/λ³ (follows from fcorr_lb + csInf argument; the csInf
   reduction itself is fully proved).

AXIOMS on proved results: [propext, Classical.choice, Quot.sound].

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

/-! ### B1b: fcorr ≥ 1/λ³ pointwise (SORRY) — precise residual stated below -/

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

/-- **(B1b — sorry)** For all q ≥ 18 and μc in the domain,
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

    **Status (2026-06-13, M1-verified ground truth).**
    Foundational correction bounds are now PROVED in this file (sorry-free):
    `xiq_le` (ξ ≤ θ/5), `etaq_le` (η ≤ tan θ/3), `etaq_nonneg`, `lamq_ge` (λ ≥ 1.9).
    The through-line `core_limit` (`50·cos²(33π/512) < 48`) is PROVED: it is exactly
    the q→∞ form of `RegimeACore` and equals `cos_sq_lt`.  The min of `fcorr` over the
    domain is at μc=0 (M1: argmin = 0 for every q), achieved by the central window
    index (pigeonhole offset 0 if L odd, θ if L even).

    **Remaining** (the actual sorry): assemble `RegimeACore`/`RegimeBCore` (each a
    single-variable transcendental inequality, EXACT-H, never intervalizing c=cos θ)
    + the `Finset.le_sup'` pigeonhole index selection + the regime split.  RegimeA
    margin ≥ +0.022; RegimeB margin ≥ +0.0175.  Dispatched to Aristotle (see
    `research_notes/fcorr_lb_status_2026-06-13.md`).
-/
theorem fcorr_lb (q : ℕ) (hq : 18 ≤ q) (hL : 0 < L_blk q)
    {muc : ℝ} (hmuc : muc ∈ Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q)) :
    1 / lamq q ^ 3 ≤ fcorr (L_blk q) q hL muc := by
  sorry

/-! ### B1_target: sInf bound (sorry-from-fcorr_lb + proved sInf argument) -/

/-- **(B1c)** The domain is nonempty. -/
theorem domain_nonempty (q : ℕ) (hq : 18 ≤ q) :
    (Set.Ioo (-(Real.pi / 2 - Hq (L_blk q) q)) (Real.pi / 2 - Hq (L_blk q) q)).Nonempty := by
  have hH_lt : Hq (L_blk q) q < Real.pi / 2 := H_lt_half_pi q hq
  refine ⟨0, ?_⟩
  simp only [Set.mem_Ioo]
  constructor <;> linarith

/-- **(B1_target — sorry via fcorr_lb)** For all q ≥ 18,
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


