import Mathlib

/-!
# Renormalization F-window: the uniform INNER inequality (tail q ≥ 17), Lean-verified core.

The all-q F-window inequality `g(⌊q/4⌋+3, q) ≥ 1/λ³` (λ = 2cos(π/q)) reduces — via the lower
bound `g ≥ g_closed` (L5), the domain bound `|γ| ≤ θ/3`, and the uniformly-certified OUTER
bound — to the binding INNER inequality at the window center:

    Φ*(q) := 8 cos⁴(π/q) − cos²(H)·(1 + 8 cos²(π/q)) ≥ 0,   H = (⌊q/4⌋+2)·π/(2q).

This file proves Φ*(q) ≥ 0 OUTRIGHT for every integer q ≥ 17 (`phi_star_nonneg`, axiom-clean) —
the genuine inner inequality, not merely its relaxation. The chain is:
  * `H ≥ π/8` for q ≥ 17 (floor bound, via `Nat.div_add_mod`) ⟹ `cos²H ≤ cos²(π/8) = (2+√2)/4`
    (`cos_sq_H_le`, using `Real.cos_pi_div_eight`);
  * `cos²(π/q) ≥ 193/200` for q ≥ 17 (`cos_pi_over_q_sq_ge`);
  * the tail quadratic `Q(u) = 8u² − 2(2+√2)u − (2+√2)/4 ≥ 0` for u ≥ 193/200
    (`tail_quadratic_nonneg`, `inner_tail_quadratic`);
  * `Φ* − Q = (1+8u)·((2+√2)/4 − cos²H) ≥ 0`, so `Φ* ≥ Q ≥ 0`.

(The continuum limit q→∞ gives the exact floor value `g_∞ = 2(2−√2)/9 = 0.13017… > 1/8`,
margin `(23−16√2)/72 > 0`.) Remaining all-q gaps NOT in this file: L4 (`g_closed ≥` the
inner bound, the binding discrete min-over-μ / lattice step) and L5 (`g ≥ g_closed`, structural).
-/
namespace RenormFWindow

/-- `1.414 <= sqrt2 <= 1.415`. -/
lemma sqrt2_bounds : (1414:ℝ)/1000 ≤ Real.sqrt 2 ∧ Real.sqrt 2 ≤ (1415:ℝ)/1000 := by
  refine ⟨?_, ?_⟩
  · rw [show (1414:ℝ)/1000 = Real.sqrt ((1414/1000)^2) by rw [Real.sqrt_sq (by norm_num)]]
    apply Real.sqrt_le_sqrt; norm_num
  · rw [show (1415:ℝ)/1000 = Real.sqrt ((1415/1000)^2) by rw [Real.sqrt_sq (by norm_num)]]
    apply Real.sqrt_le_sqrt; norm_num

/-- TAIL quadratic engine: `Q(u) = 8u^2 - 2(2+sqrt2)u - (2+sqrt2)/4 >= 0` for `u >= 193/200`. -/
theorem tail_quadratic_nonneg (u : ℝ) (hu : (193:ℝ)/200 ≤ u) :
    8 * u^2 - 2 * (2 + Real.sqrt 2) * u - (2 + Real.sqrt 2)/4 ≥ 0 := by
  obtain ⟨hlo, hhi⟩ := sqrt2_bounds
  have hu0 : (0:ℝ) ≤ u := le_trans (by norm_num) hu
  have hsu : Real.sqrt 2 * u ≤ (1415/1000) * u := mul_le_mul_of_nonneg_right hhi hu0
  nlinarith [hu, hlo, hhi, hu0, hsu, sq_nonneg (u - 193/200),
             mul_nonneg (sub_nonneg.mpr hu) hu0]

lemma cos_lb (x : ℝ) : 1 - x^2/2 ≤ Real.cos x := Real.one_sub_sq_div_two_le_cos

/-- For natural `q >= 17`, `193/200 <= cos^2(pi/q)`. -/
lemma cos_pi_over_q_sq_ge (q : ℕ) (hq : 17 ≤ q) :
    (193:ℝ)/200 ≤ Real.cos (Real.pi / q)^2 := by
  have hπ : Real.pi < 3.15 := Real.pi_lt_d2
  have hπpos : (0:ℝ) < Real.pi := Real.pi_pos
  have hqR : (17:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have hqpos : (0:ℝ) < (q:ℝ) := by linarith
  have hxle : Real.pi / q ≤ Real.pi / 17 :=
    div_le_div_of_nonneg_left (le_of_lt hπpos) (by norm_num) hqR
  have hxnn : (0:ℝ) ≤ Real.pi / q := by positivity
  have h17le_pi : Real.pi / 17 ≤ Real.pi := by
    rw [div_le_iff₀ (by norm_num)]; nlinarith [hπpos]
  have hmono : Real.cos (Real.pi / 17) ≤ Real.cos (Real.pi / q) :=
    Real.cos_le_cos_of_nonneg_of_le_pi hxnn h17le_pi hxle
  have hpi17nn : (0:ℝ) ≤ Real.pi / 17 := by positivity
  have hpi17le : Real.pi / 17 ≤ 3.15/17 :=
    div_le_div_of_nonneg_right (le_of_lt hπ) (by norm_num)
  have hsq : (Real.pi/17)^2 ≤ (3.15/17)^2 := by
    apply sq_le_sq'
    · nlinarith [hpi17nn]
    · exact hpi17le
  have hclb := cos_lb (Real.pi / 17)
  have hc17 : (4912:ℝ)/5000 ≤ Real.cos (Real.pi / 17) := by nlinarith [hclb, hsq]
  have hcqnn : (0:ℝ) ≤ Real.cos (Real.pi / q) := le_trans (by norm_num) (le_trans hc17 hmono)
  have hcq : (4912:ℝ)/5000 ≤ Real.cos (Real.pi / q) := le_trans hc17 hmono
  nlinarith [hcq, hcqnn]

/-- ASSEMBLED TAIL: for `q >= 17`, the quadratic `Q(cos^2(pi/q)) >= 0`. -/
theorem inner_tail_quadratic (q : ℕ) (hq : 17 ≤ q) :
    8 * (Real.cos (Real.pi / q)^2)^2
      - 2 * (2 + Real.sqrt 2) * (Real.cos (Real.pi / q)^2)
      - (2 + Real.sqrt 2)/4 ≥ 0 :=
  tail_quadratic_nonneg _ (cos_pi_over_q_sq_ge q hq)

/-- `cos^2(pi/8) = (2 + sqrt 2)/4`. -/
lemma cos_sq_pi_div_eight : Real.cos (Real.pi / 8)^2 = (2 + Real.sqrt 2)/4 := by
  rw [Real.cos_pi_div_eight]
  rw [div_pow, Real.sq_sqrt (by positivity)]
  norm_num

/-- For `q >= 17`, the floor expression `H` satisfies `pi/8 <= H <= pi/2`. -/
lemma H_bounds (q : ℕ) (hq : 17 ≤ q) :
    Real.pi / 8 ≤ ((((q/4 + 2 : ℕ)):ℝ) * Real.pi / (2 * (q:ℝ)))
      ∧ ((((q/4 + 2 : ℕ)):ℝ) * Real.pi / (2 * (q:ℝ))) ≤ Real.pi / 2 := by
  have hπpos : (0:ℝ) < Real.pi := Real.pi_pos
  have hqR : (17:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have hqpos : (0:ℝ) < (q:ℝ) := by linarith
  -- Nat facts
  have hdiv : 4 * (q/4) + q % 4 = q := Nat.div_add_mod q 4
  have hmod : q % 4 < 4 := Nat.mod_lt q (by norm_num)
  -- Real versions
  have hd4_lo : (q:ℝ) - 3 ≤ 4 * ((q/4 : ℕ):ℝ) := by
    have : ((4 * (q/4) + q % 4 : ℕ):ℝ) = (q:ℝ) := by exact_mod_cast hdiv
    push_cast at this
    have hmodR : ((q % 4 : ℕ):ℝ) ≤ 3 := by
      have : (q % 4 : ℕ) ≤ 3 := by omega
      exact_mod_cast this
    linarith
  have hd4_hi : 4 * ((q/4 : ℕ):ℝ) ≤ (q:ℝ) := by
    have : ((4 * (q/4) + q % 4 : ℕ):ℝ) = (q:ℝ) := by exact_mod_cast hdiv
    push_cast at this
    have hmodR : (0:ℝ) ≤ ((q % 4 : ℕ):ℝ) := by positivity
    linarith
  set d : ℝ := ((q/4 : ℕ):ℝ) with hd
  have hcast : ((((q/4 + 2 : ℕ)):ℝ)) = d + 2 := by push_cast [hd]; ring
  rw [hcast]
  constructor
  · -- pi/8 <= (d+2) pi / (2q)  <=> 8(d+2) >= 2q  (using pi>0, q>0)  <=> 4(d+2) >= q
    rw [div_le_div_iff₀ (by norm_num) (by positivity)]
    -- pi * (2q) <= (d+2)*pi*8
    nlinarith [hd4_lo, hπpos, hqpos]
  · -- (d+2) pi/(2q) <= pi/2  <=>  (d+2)*pi*2 <= pi*(2q)  <=> d+2 <= q
    rw [div_le_div_iff₀ (by positivity) (by norm_num)]
    -- 4d <= q and q >= 17 so d <= q/4, d+2 <= q
    nlinarith [hd4_hi, hπpos, hqpos, hqR]

/-- For `q >= 17`, `cos^2(H) <= (2 + sqrt 2)/4`. -/
lemma cos_sq_H_le (q : ℕ) (hq : 17 ≤ q) :
    Real.cos (((((q/4 + 2 : ℕ)):ℝ) * Real.pi / (2 * (q:ℝ))))^2 ≤ (2 + Real.sqrt 2)/4 := by
  obtain ⟨hlo, hhi⟩ := H_bounds q hq
  set H : ℝ := ((((q/4 + 2 : ℕ)):ℝ) * Real.pi / (2 * (q:ℝ))) with hH
  have hπpos : (0:ℝ) < Real.pi := Real.pi_pos
  have hpi8nn : (0:ℝ) ≤ Real.pi / 8 := by positivity
  have hHnn : (0:ℝ) ≤ H := le_trans hpi8nn hlo
  have hHlepi : H ≤ Real.pi := le_trans hhi (by linarith [hπpos] : Real.pi / 2 ≤ Real.pi)
  -- cos H <= cos (pi/8)
  have hmono : Real.cos H ≤ Real.cos (Real.pi / 8) :=
    Real.cos_le_cos_of_nonneg_of_le_pi hpi8nn hHlepi hlo
  -- cos H >= 0  since 0 <= H <= pi/2
  have hcosHnn : (0:ℝ) ≤ Real.cos H := by
    apply Real.cos_nonneg_of_mem_Icc
    constructor
    · linarith [hHnn, hπpos]
    · exact hhi
  -- cos(pi/8) >= 0
  have hcos8nn : (0:ℝ) ≤ Real.cos (Real.pi / 8) := le_trans hcosHnn hmono
  -- square monotone on nonneg
  have hsq : Real.cos H ^ 2 ≤ Real.cos (Real.pi / 8) ^ 2 := by
    nlinarith [hmono, hcosHnn, hcos8nn]
  rw [cos_sq_pi_div_eight] at hsq
  exact hsq

/-- TARGET: the genuine INNER inequality, for `q >= 17`. -/
theorem phi_star_nonneg (q : ℕ) (hq : 17 ≤ q) :
    8 * Real.cos (Real.pi / (q:ℝ))^4
      - Real.cos ((((q/4 + 2 : ℕ)):ℝ) * Real.pi / (2 * (q:ℝ)))^2
        * (1 + 8 * Real.cos (Real.pi / (q:ℝ))^2) ≥ 0 := by
  set u : ℝ := Real.cos (Real.pi / (q:ℝ))^2 with hu_def
  set cH2 : ℝ := Real.cos ((((q/4 + 2 : ℕ)):ℝ) * Real.pi / (2 * (q:ℝ)))^2 with hcH2_def
  have hQ := inner_tail_quadratic q hq
  -- rewrite tail quadratic in terms of u
  have hQ' : 8 * u^2 - 2 * (2 + Real.sqrt 2) * u - (2 + Real.sqrt 2)/4 ≥ 0 := hQ
  have hcH2_le : cH2 ≤ (2 + Real.sqrt 2)/4 := cos_sq_H_le q hq
  have huge : (193:ℝ)/200 ≤ u := cos_pi_over_q_sq_ge q hq
  have h1p8u_nn : (0:ℝ) ≤ 1 + 8 * u := by nlinarith [huge]
  have hgap_nn : (0:ℝ) ≤ (2 + Real.sqrt 2)/4 - cH2 := by linarith [hcH2_le]
  have hprod : (0:ℝ) ≤ (1 + 8 * u) * ((2 + Real.sqrt 2)/4 - cH2) :=
    mul_nonneg h1p8u_nn hgap_nn
  -- cos^4 = u^2
  have hpow : Real.cos (Real.pi / (q:ℝ))^4 = u^2 := by
    rw [hu_def]; ring
  rw [hpow]
  nlinarith [hQ', hprod, hcH2_le, huge]

end RenormFWindow

#print axioms RenormFWindow.phi_star_nonneg
#print axioms RenormFWindow.cos_sq_pi_div_eight
#print axioms RenormFWindow.cos_sq_H_le
#print axioms RenormFWindow.inner_tail_quadratic
