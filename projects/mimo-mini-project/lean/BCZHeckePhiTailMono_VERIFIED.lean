import Mathlib
set_option maxHeartbeats 40000000
noncomputable section
open Real

/-- THE TAIL POLYNOMIAL INEQUALITY (q-uniform, q ≥ 9), monotonicity-reduction route.
For `θ ∈ (0, π/9]` (i.e. `q ≥ 9`) the polynomial lower bound on the Hecke F-window INNER
margin `Psi = λ⁴ - 2(1+2λ²)cos²H` is strictly positive:
`(2 - θ²)⁴ - 18·(1 - x²/4 + x⁴/48) > 0`, `x = π/4 + 5θ/4`.
Proof: explicit `π`-power brackets + Bernstein-positivity products `θ^j(a-θ)^{8-j} ≥ 0`,
`a = 3.1416/9`, the certificate whose 9 Bernstein coefficients are all `> 0`. -/
theorem psi_lb_pos
    (theta : ℝ) (hlo : 0 < theta) (hhi : theta ≤ Real.pi/9) :
    0 < (2 - theta^2)^4 - 18 * (1 - (Real.pi/4 + 5*theta/4)^2/4 + (Real.pi/4 + 5*theta/4)^4/48) := by
  have hpi_lo : (3.1415 : ℝ) < Real.pi := Real.pi_gt_d4
  have hpi_hi : Real.pi < 3.1416 := Real.pi_lt_d4
  have hth0 : 0 ≤ theta := le_of_lt hlo
  have hthU : theta ≤ 1309/3750 := by
    have h1 : Real.pi/9 ≤ 3.1416/9 := by linarith
    have h2 : (3.1416:ℝ)/9 = 1309/3750 := by norm_num
    linarith [hhi, h1]
  have hath : (0:ℝ) ≤ 1309/3750 - theta := by linarith
  -- explicit π-power brackets
  have hpi2lo : (9.8690 : ℝ) < Real.pi^2 := by nlinarith [hpi_lo, Real.pi_pos]
  have hpi2hi : Real.pi^2 < 9.8697 := by nlinarith [hpi_hi, Real.pi_pos]
  have hpi3hi : Real.pi^3 < 31.007 := by nlinarith [hpi_hi, hpi2hi, Real.pi_pos, sq_nonneg Real.pi]
  have hpi3lo : (31.003 : ℝ) < Real.pi^3 := by nlinarith [hpi_lo, hpi2lo, Real.pi_pos]
  have hpi4hi : Real.pi^4 < 97.412 := by nlinarith [hpi2hi, sq_nonneg (Real.pi^2)]
  have hpi2pos : (0:ℝ) < Real.pi^2 := by positivity
  have hpi4lo : (97.397 : ℝ) < Real.pi^4 := by nlinarith [hpi2lo, hpi2pos]
  -- Bernstein nonneg products (degree-8 partition of unity on [0, a], a=1309/3750)
  nlinarith [hpi_lo, hpi_hi, hpi2lo, hpi2hi, hpi3lo, hpi3hi, hpi4lo, hpi4hi, hth0, hthU,
             mul_nonneg (pow_nonneg hth0 0) (pow_nonneg hath 8),
             mul_nonneg (pow_nonneg hth0 1) (pow_nonneg hath 7),
             mul_nonneg (pow_nonneg hth0 2) (pow_nonneg hath 6),
             mul_nonneg (pow_nonneg hth0 3) (pow_nonneg hath 5),
             mul_nonneg (pow_nonneg hth0 4) (pow_nonneg hath 4),
             mul_nonneg (pow_nonneg hth0 5) (pow_nonneg hath 3),
             mul_nonneg (pow_nonneg hth0 6) (pow_nonneg hath 2),
             mul_nonneg (pow_nonneg hth0 7) (pow_nonneg hath 1),
             mul_nonneg (pow_nonneg hth0 8) (pow_nonneg hath 0),
             mul_nonneg hth0 (mul_nonneg hth0 hth0)]

#print axioms psi_lb_pos
