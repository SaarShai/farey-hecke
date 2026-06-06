import Mathlib

/-
  ARC-WIDTH-PHASE route — FULL elementary INNER inequality, Lean-checkable.

  Window L = floor(q/4)+3. theta in (0, pi/7]. lam = 2 cos theta. A2 = 1 + 2 lam^2.
  H = (L-1)*theta/2 >= pi/8 + 5theta/8 (from floor(q/4) >= q/4 - 3/4).

  MAIN (this file): the binding elementary inequality
     G(theta) := lam^4 - 2 A2 cos^2(pi/8 + 5theta/8) >= 0   for theta in (0, pi/7],
  with lam = 2 cos theta, A2 = 1 + 2 lam^2.   [margin >= 0.52]

  Combined with:
   * inner_to_thr (algebra): lam^4 >= 2 A2 cos^2 H  =>  lam/(2 A2 cos^2 H) >= 1/lam^3;
   * H >= pi/8+5theta/8 (=> cos^2 H <= cos^2(pi/8+5theta/8) since both args in (0,pi/2), cos↓);
   * the INNER lower bound g_closed >= lam/(2 A2 cos^2 H) (lattice argument);
  this gives g_closed(L,q) >= 1/lam^3 for all q >= 7 with L = floor(q/4)+3.
  (q = 5, 6 handled by the existing per-q Lean window lemmas.)
-/

open Real

namespace ArcPhaseFull

/-- tangent: cos t - sin t <= 1 - t on [0, 0.57] (via Mathlib cos_bound / sin_bound). -/
theorem cos_sub_sin_le (t : ℝ) (h0 : 0 ≤ t) (h1 : t ≤ 0.57) :
    Real.cos t - Real.sin t ≤ 1 - t := by
  have ht1 : t ≤ 1 := by linarith
  have habs : |t| = t := abs_of_nonneg h0
  have h4 : |t| ^ 4 = t ^ 4 := by rw [habs]
  have hcos := Real.cos_bound (x := t) (by rw [habs]; exact ht1)
  have hsin := Real.sin_bound (x := t) (by rw [habs]; exact ht1)
  rw [abs_le] at hcos hsin
  nlinarith [hcos.2, hsin.1, h4, sq_nonneg t, h0, h1, mul_nonneg h0 h0,
             mul_nonneg (mul_nonneg h0 h0) h0]

/-- tangent bound on cos at pi/4: cos(pi/4 + s) <= (sqrt2/2)(1 - s) for s in [0, 0.57]. -/
theorem cos_tangent (s : ℝ) (h0 : 0 ≤ s) (h1 : s ≤ 0.57) :
    Real.cos (Real.pi/4 + s) ≤ (Real.sqrt 2/2) * (1 - s) := by
  rw [Real.cos_add, Real.cos_pi_div_four, Real.sin_pi_div_four]
  have hkey := cos_sub_sin_le s h0 h1
  nlinarith [hkey, Real.sqrt_nonneg 2]

/-- the degree-4 polynomial bound: P(θ) ≥ 0 on [0, π/7]. -/
noncomputable def Ppoly (θ : ℝ) : ℝ :=
  16*θ^4 - 5*Real.sqrt 2*θ^3 + (4*Real.sqrt 2 - 24)*θ^2 + (45*Real.sqrt 2/8)*θ + (7 - 9*Real.sqrt 2/2)

theorem Ppoly_nonneg (θ : ℝ) (h0 : 0 ≤ θ) (h1 : θ ≤ Real.pi/7) : Ppoly θ ≥ 0 := by
  unfold Ppoly
  have hs2hi : Real.sqrt 2 ≤ 1.41422 := by
    nlinarith [Real.sqrt_nonneg 2, Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num)]
  have hs2lo : 1.41421 ≤ Real.sqrt 2 := by
    nlinarith [Real.sqrt_nonneg 2, Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num)]
  have hub : θ ≤ 0.44880 := by
    have : Real.pi/7 ≤ 0.44880 := by linarith [Real.pi_lt_d4]
    linarith
  nlinarith [Real.sqrt_nonneg 2, h0, hub, hs2hi, hs2lo, sq_nonneg θ,
             sq_nonneg (θ - 0.3), mul_nonneg h0 (mul_nonneg h0 h0),
             mul_nonneg h0 h0, sq_nonneg (θ*θ - 0.1)]

/-- MAIN elementary inequality.
    For θ ∈ (0, π/7],  G(θ) = lam^4 - 2 A2 cos²(π/8 + 5θ/8) ≥ 0,
    where lam = 2 cos θ, A2 = 1 + 2 lam². -/
theorem G_nonneg (θ : ℝ) (h0 : 0 < θ) (h1 : θ ≤ Real.pi/7) :
    let lam := 2 * Real.cos θ
    let A2 := 1 + 2 * lam^2
    lam^4 - 2 * A2 * (Real.cos (Real.pi/8 + 5*θ/8))^2 ≥ 0 := by
  intro lam A2
  have h0' : 0 ≤ θ := le_of_lt h0
  -- step b: cos(2θ) ≥ 1 - 2θ²
  have hu : Real.cos (2*θ) ≥ 1 - 2*θ^2 := by
    have := Real.one_sub_sq_div_two_le_cos (x := 2*θ)
    nlinarith [this]
  -- lam² = 2 + 2 cos 2θ  (double angle)
  have hlam2 : lam^2 = 2 + 2 * Real.cos (2*θ) := by
    have hdc : Real.cos (2*θ) = 2 * (Real.cos θ)^2 - 1 := by
      rw [Real.cos_two_mul]
    simp only [lam]; rw [hdc]; ring
  -- cos²(π/8+5θ/8) = (1 + cos(π/4 + 5θ/4))/2
  have hhalf : (Real.cos (Real.pi/8 + 5*θ/8))^2 = (1 + Real.cos (Real.pi/4 + 5*θ/4))/2 := by
    have : Real.pi/4 + 5*θ/4 = 2*(Real.pi/8 + 5*θ/8) := by ring
    rw [this, Real.cos_two_mul]; ring
  -- step a: cos(π/4+5θ/4) ≤ (√2/2)(1 - 5θ/4)
  have hs : 5*θ/4 ≤ 0.57 := by nlinarith [Real.pi_lt_d4, h1]
  have hs0 : 0 ≤ 5*θ/4 := by linarith
  have htan : Real.cos (Real.pi/4 + 5*θ/4) ≤ (Real.sqrt 2/2)*(1 - 5*θ/4) := by
    have := cos_tangent (5*θ/4) hs0 hs
    convert this using 2
  -- A2 = 5 + 4 cos 2θ ; A2 ≥ 0
  have hA2eq : A2 = 5 + 4 * Real.cos (2*θ) := by simp only [A2]; rw [hlam2]; ring
  have hcosbd : Real.cos (2*θ) ≥ -1 := Real.neg_one_le_cos _
  have hA2pos : (0:ℝ) ≤ A2 := by rw [hA2eq]; linarith
  -- lam^4 = (lam²)² = (2 + 2 cos2θ)²
  have hlam4 : lam^4 = (2 + 2*Real.cos (2*θ))^2 := by
    have : lam^4 = (lam^2)^2 := by ring
    rw [this, hlam2]
  -- Assemble: with u := cos2θ ≥ 1-2θ², and the tangent bound,
  -- G = lam^4 - A2(1 + cos(π/4+5θ/4)) ≥ (2+2u)² - (5+4u)(1 + (√2/2)(1-5θ/4)) ≥ Ppoly(θ) ≥ 0.
  set u := Real.cos (2*θ) with hu_def
  rw [hhalf, hlam4, hA2eq]
  -- goal: (2+2u)^2 - 2*(5+4u)*((1 + cos(π/4+5θ/4))/2) ≥ 0
  -- = (2+2u)^2 - (5+4u)*(1 + cos(...)) ≥ 0
  have hub_u : u ≥ 1 - 2*θ^2 := hu
  have hPp := Ppoly_nonneg θ h0' h1
  unfold Ppoly at hPp
  set cT := Real.cos (Real.pi/4 + 5*θ/4) with hcT_def
  -- (5+4u) ≥ 0
  have h5p4u : (0:ℝ) ≤ 5 + 4*u := by linarith [hcosbd]
  -- step a (multiplied): (5+4u)·cT ≤ (5+4u)·(√2/2)(1-5θ/4)
  have hprod : (5 + 4*u) * cT ≤ (5 + 4*u) * ((Real.sqrt 2/2)*(1 - 5*θ/4)) :=
    mul_le_mul_of_nonneg_left htan h5p4u
  -- monotone-in-u step: Q(u,θ) - Ppoly(θ) = (u-u0)(4(u+u0)+b),  u0=1-2θ², coeff ≥ 0.
  set u0 : ℝ := 1 - 2*θ^2 with hu0_def
  have hdu : (0:ℝ) ≤ u - u0 := sub_nonneg.mpr hub_u
  have hth : θ ≤ 0.449 := by nlinarith [Real.pi_lt_d4, h1]
  have hs2hi : Real.sqrt 2 ≤ 1.42 := by
    nlinarith [Real.sqrt_nonneg 2, Real.sq_sqrt (show (0:ℝ) ≤ 2 by norm_num)]
  have hu0lo : (0:ℝ) ≤ u0 := by rw [hu0_def]; nlinarith [hth, h0', sq_nonneg θ]
  have hcoef : (0:ℝ) ≤ 4*(u + u0) + (5*Real.sqrt 2*θ/2 - 2*Real.sqrt 2 + 4) := by
    nlinarith [hu0lo, hub_u, hs2hi, Real.sqrt_nonneg 2, h0', hth]
  have hmono : (0:ℝ) ≤ (u - u0) * (4*(u + u0) + (5*Real.sqrt 2*θ/2 - 2*Real.sqrt 2 + 4)) :=
    mul_nonneg hdu hcoef
  -- close: G = (2+2u)²-(5+4u)(1+cT) ≥ Q (hprod) ≥ Ppoly (hmono) ≥ 0 (hPp).
  nlinarith [hprod, hPp, hmono, hu0_def, Real.sqrt_nonneg 2]

/-- cos² is monotone-decreasing on [0, π/2]. -/
theorem cos_sq_anti (a b : ℝ) (ha : 0 ≤ a) (hab : a ≤ b) (hb : b ≤ Real.pi/2) :
    (Real.cos b)^2 ≤ (Real.cos a)^2 := by
  have hcb : 0 ≤ Real.cos b := Real.cos_nonneg_of_mem_Icc ⟨by linarith [Real.pi_pos], hb⟩
  have hca : Real.cos b ≤ Real.cos a :=
    Real.cos_le_cos_of_nonneg_of_le_pi ha (by linarith [Real.pi_pos]) hab
  nlinarith [hcb, hca]

/-- algebra: lam>0, A2>0, cH2>0, lam^4 ≥ 2 A2 cH2  ⇒  lam/(2 A2 cH2) ≥ 1/lam^3. -/
theorem inner_to_thr (lam A2 cH2 : ℝ)
    (hlam : 0 < lam) (hA2 : 0 < A2) (hcH2 : 0 < cH2)
    (hkey : lam^4 ≥ 2 * A2 * cH2) :
    lam / (2 * A2 * cH2) ≥ 1 / lam^3 := by
  rw [ge_iff_le, div_le_div_iff₀ (by positivity) (by positivity)]
  nlinarith [hkey, hlam, hA2, hcH2]

/-- CAPSTONE (inner branch).  For θ ∈ (0, π/7], let lam = 2 cos θ, A2 = 1 + 2 lam².
    If the window half-angle H satisfies  π/8 + 5θ/8 ≤ H ≤ π/2,
    then the INNER lower bound clears the threshold:
        lam / (2 A2 cos² H)  ≥  1 / lam³.
    (For the uniform window L = ⌊q/4⌋+3 one has H = (L-1)θ/2 ≥ π/8+5θ/8 and H < π/2,
     and the orbit's window value g_closed(L,q) ≥ lam/(2 A2 cos² H) by the lattice argument,
     hence g_closed(L,q) ≥ 1/lam³ for all q ≥ 7.) -/
theorem inner_capstone (θ H : ℝ) (h0 : 0 < θ) (h1 : θ ≤ Real.pi/7)
    (hHlo : Real.pi/8 + 5*θ/8 ≤ H) (hHhi : H < Real.pi/2) :
    let lam := 2 * Real.cos θ
    let A2  := 1 + 2 * lam^2
    lam / (2 * A2 * (Real.cos H)^2) ≥ 1 / lam^3 := by
  intro lam A2
  -- positivity facts
  have hcosθ : 0 < Real.cos θ := by
    apply Real.cos_pos_of_mem_Ioo
    refine ⟨by linarith [Real.pi_pos], by linarith [Real.pi_pos]⟩
  have hlam : 0 < lam := by simp only [lam]; linarith
  have hA2 : 0 < A2 := by simp only [A2]; positivity
  -- cos H > 0 since 0 ≤ H < π/2
  have hHnn : 0 ≤ H := by linarith [Real.pi_pos, le_of_lt h0]
  have hcosH : 0 < Real.cos H := Real.cos_pos_of_mem_Ioo ⟨by linarith [Real.pi_pos], hHhi⟩
  have hcH2 : 0 < (Real.cos H)^2 := by positivity
  -- cos²H ≤ cos²(π/8+5θ/8)  (cos² antitone, both args in [0,π/2])
  have hlo0 : 0 ≤ Real.pi/8 + 5*θ/8 := by linarith [Real.pi_pos, le_of_lt h0]
  have hcsq : (Real.cos H)^2 ≤ (Real.cos (Real.pi/8 + 5*θ/8))^2 :=
    cos_sq_anti _ _ hlo0 hHlo (le_of_lt hHhi)
  -- the elementary inequality: lam^4 ≥ 2 A2 cos²(π/8+5θ/8)
  have hG := G_nonneg θ h0 h1
  simp only at hG
  have hkey0 : lam^4 ≥ 2 * A2 * (Real.cos (Real.pi/8 + 5*θ/8))^2 := by
    simp only [lam, A2]; linarith [hG]
  -- chain cos²H ≤ cos²(...) ⇒ lam^4 ≥ 2 A2 cos²H
  have hkey : lam^4 ≥ 2 * A2 * (Real.cos H)^2 := by
    have : 2 * A2 * (Real.cos H)^2 ≤ 2 * A2 * (Real.cos (Real.pi/8 + 5*θ/8))^2 :=
      mul_le_mul_of_nonneg_left hcsq (by positivity)
    linarith [hkey0]
  exact inner_to_thr lam A2 _ hlam hA2 hcH2 hkey

end ArcPhaseFull

#print axioms ArcPhaseFull.cos_tangent
#print axioms ArcPhaseFull.inner_to_thr
#print axioms ArcPhaseFull.cos_sq_anti
#print axioms ArcPhaseFull.inner_capstone
#print axioms ArcPhaseFull.Ppoly_nonneg
#print axioms ArcPhaseFull.G_nonneg
