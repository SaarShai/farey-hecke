import Mathlib
set_option maxHeartbeats 4000000
noncomputable section
open Int

/-- Floor≤3 contradiction kernel (free φ). -/
lemma g5_floor_helper (phi x y : ℝ) (hps : phi^2 = phi+1) (h2 : 1 < phi)
    (hx : 0 < x) (hy : 0 < y)
    (hxs : (3*phi+2)*x^2 < 1/2) (hyU : (3*phi+2)*y^2 < 2) (hedge : 1 - phi*x < y) :
    False := by
  have hpos : 0 < phi := by linarith
  have hphix : phi * x < 1 := by nlinarith [hxs, hps, hx, mul_pos hpos hx, h2]
  have h1px : 0 < 1 - phi*x := by linarith
  have hysq : (1 - phi*x)^2 < y^2 := by
    nlinarith [mul_pos h1px (show (0:ℝ) < y + (1-phi*x) by linarith), hedge, hy]
  nlinarith [hysq, hyU, hxs, hps, hx, hphix, mul_pos hpos hx,
    sq_nonneg ((31*phi+20)*x - (10*phi+6))]


lemma case111 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 1*phi*b) (hk1 : b+d = 1*phi*c) (hk2 : c+e = 1*phi*d)
    (hk0f : 1+a < (1+1)*(phi*b)) (hk1f : 1+b < (1+1)*(phi*c)) (hk2f : 1+c < (1+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 2*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 2*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 2*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ c*d + c*e*phi - c := by
    have hr : (0:ℝ) ≤ (c)*(d + e*phi - 1) := mul_nonneg hc.le rde
    have he : (c)*(d + e*phi - 1) = c*d + c*e*phi - c := by linear_combination (0)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*c*phi + b*c - c := by
    have hr : (0:ℝ) ≤ (c)*(a*phi + b - 1) := mul_nonneg hc.le gab
    have he : (c)*(a*phi + b - 1) = a*c*phi + b*c - c := by linear_combination (0)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -3*b*c*e*phi - 2*b*c*e + e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(-2*b*c*phi - b*c + 1)) := mul_nonneg hpos.le (mul_nonneg he2.le hs1)
    have he : phi*((e)*(-2*b*c*phi - b*c + 1)) = -3*b*c*e*phi - 2*b*c*e + e*phi := by linear_combination (-2*b*c*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca rde)
    have he : phi*((1 - a)*(d + e*phi - 1)) = -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by linear_combination (-a*e + e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : phi*((1 - a)*(a*phi + b - 1)) = -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rde)
    have he : phi*((1 - e)*(d + e*phi - 1)) = -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by linear_combination (-e^2 + e)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ce gab)
    have he : phi*((1 - e)*(a*phi + b - 1)) = -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by linear_combination (-a*e + a)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*b*c*e*phi + 2*b*c*e - 3*b*c*phi - 2*b*c - e*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(-2*b*c*phi - b*c + 1)) := mul_nonneg hpos.le (mul_nonneg ce hs1)
    have he : phi*((1 - e)*(-2*b*c*phi - b*c + 1)) = 3*b*c*e*phi + 2*b*c*e - 3*b*c*phi - 2*b*c - e*phi + phi := by linear_combination (2*b*c*e - 2*b*c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ b*d*phi + b*e*phi + b*e - b*phi + c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c - d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rbc rde)
    have he : phi*((b + c*phi - 1)*(d + e*phi - 1)) = b*d*phi + b*e*phi + b*e - b*phi + c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c - d*phi - e*phi - e + phi := by linear_combination (b*e + c*d + c*e*phi + c*e - c - e)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gab)
    have he : phi*((b + c*phi - 1)*(a*phi + b - 1)) = a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by linear_combination (a*b + a*c*phi + a*c - a + b*c - c)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -a*b*phi - a*b + 4*a*c*phi + 2*a*c - a*phi - a - b^2*phi + 2*b*c*phi + 2*b*c - 2*c*phi - 2*c + phi := by
    have hr : (0:ℝ) ≤ phi*((a*phi + b - 1)*(-b + 2*c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg gab hf1)
    have he : phi*((a*phi + b - 1)*(-b + 2*c*phi - 1)) = -a*b*phi - a*b + 4*a*c*phi + 2*a*c - a*phi - a - b^2*phi + 2*b*c*phi + 2*b*c - 2*c*phi - 2*c + phi := by linear_combination (-a*b + 2*a*c*phi + 2*a*c - a + 2*b*c - 2*c)*hps
    linarith [hr, he]
  have E0 : a - b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - b*phi - b + c*phi = 0 := by linear_combination (phi)*hk0 + (b)*hps
  have E2 : a^2 - a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a^2*phi - a*b*phi - a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (a*b)*hps
  have E4 : a*b - b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E5 : a*c - b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E6 : a*c*phi - b*c*phi - b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (b*c)*hps
  have E7 : a*d*phi - b*d*phi - b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (b*d)*hps
  have E8 : a*e - b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E9 : a*e*phi - b*e*phi - b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (b*e)*hps
  have E10 : b - c*phi + d = 0 := by linear_combination (1)*hk1
  have E11 : b*phi - c*phi - c + d*phi = 0 := by linear_combination (phi)*hk1 + (c)*hps
  have E12 : a*b*phi - a*c*phi - a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (a*c)*hps
  have E13 : b^2*phi - b*c*phi - b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (b*c)*hps
  have E14 : b*c - c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E15 : b*c*phi - c^2*phi - c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (c^2)*hps
  have E16 : b*d - c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E17 : b*d*phi - c*d*phi - c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (c*d)*hps
  have E18 : b*e - c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E19 : c - d*phi + e = 0 := by linear_combination (1)*hk2
  have E20 : c*phi - d*phi - d + e*phi = 0 := by linear_combination (phi)*hk2 + (d)*hps
  have E21 : a*c - a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E22 : b*c*phi - b*d*phi - b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (b*d)*hps
  have E23 : c^2*phi - c*d*phi - c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (c*d)*hps
  have E24 : c*d - d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E25 : c*d*phi - d^2*phi - d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (d^2)*hps
  have E26 : c*e - d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E27 : c*e*phi - d*e*phi - d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, E27, h2, h3]

lemma case112 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 1*phi*b) (hk1 : b+d = 1*phi*c) (hk2 : c+e = 2*phi*d)
    (hk0f : 1+a < (1+1)*(phi*b)) (hk1f : 1+b < (1+1)*(phi*c)) (hk2f : 1+c < (2+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 2*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 2*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 3*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ b*c*phi + b*d*phi + b*d - b*phi := by
    have hr : (0:ℝ) ≤ phi*((b)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le rcd)
    have he : phi*((b)*(c + d*phi - 1)) = b*c*phi + b*d*phi + b*d - b*phi := by linear_combination (b*d)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*b*phi + a*b + b^2*phi - b*phi := by
    have hr : (0:ℝ) ≤ phi*((b)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le gab)
    have he : phi*((b)*(a*phi + b - 1)) = a*b*phi + a*b + b^2*phi - b*phi := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ a*c*phi + a*c + b*c*phi - c*phi := by
    have hr : (0:ℝ) ≤ phi*((c)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg hc.le gab)
    have he : phi*((c)*(a*phi + b - 1)) = a*c*phi + a*c + b*c*phi - c*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -3*b*c^2*phi - 2*b*c^2 + c*phi := by
    have hr : (0:ℝ) ≤ phi*((c)*(-2*b*c*phi - b*c + 1)) := mul_nonneg hpos.le (mul_nonneg hc.le hs1)
    have he : phi*((c)*(-2*b*c*phi - b*c + 1)) = -3*b*c^2*phi - 2*b*c^2 + c*phi := by linear_combination (-2*b*c^2)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ c*d*phi + d^2*phi + d^2 - d*phi := by
    have hr : (0:ℝ) ≤ phi*((d)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg hd.le rcd)
    have he : phi*((d)*(c + d*phi - 1)) = c*d*phi + d^2*phi + d^2 - d*phi := by linear_combination (d^2)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ a*e*phi + a*e + b*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gab)
    have he : phi*((e)*(a*phi + b - 1)) = a*e*phi + a*e + b*e*phi - e*phi := by linear_combination (a*e)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ d*e*phi + d*e + e^2*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(d*phi + e - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gde)
    have he : phi*((e)*(d*phi + e - 1)) = d*e*phi + d*e + e^2*phi - e*phi := by linear_combination (d*e)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -a*d*phi - a*e + a + d*phi + e - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(d*phi + e - 1) := mul_nonneg ca gde
    have he : (1 - a)*(d*phi + e - 1) = -a*d*phi - a*e + a + d*phi + e - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -b*c*phi - b*d*phi - b*d + b*phi + c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cb rcd)
    have he : phi*((1 - b)*(c + d*phi - 1)) = -b*c*phi - b*d*phi - b*d + b*phi + c*phi + d*phi + d - phi := by linear_combination (-b*d + d)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*b*c^2*phi + 2*b*c^2 - 3*b*c*phi - 2*b*c - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*b*c*phi - b*c + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs1)
    have he : phi*((1 - c)*(-2*b*c*phi - b*c + 1)) = 3*b*c^2*phi + 2*b*c^2 - 3*b*c*phi - 2*b*c - c*phi + phi := by linear_combination (2*b*c^2 - 2*b*c)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -c*d + c - d^2*phi + d*phi + d - 1 := by
    have hr : (0:ℝ) ≤ (1 - d)*(c + d*phi - 1) := mul_nonneg cdc rcd
    have he : (1 - d)*(c + d*phi - 1) = -c*d + c - d^2*phi + d*phi + d - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -a*d*phi - a*d + a*phi + a - b*d*phi + b*phi + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg cdc gab)
    have he : phi*((1 - d)*(a*phi + b - 1)) = -a*d*phi - a*d + a*phi + a - b*d*phi + b*phi + d*phi - phi := by linear_combination (-a*d + a)*hps
    linarith [hr, he]
  have E0 : a - b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - b*phi - b + c*phi = 0 := by linear_combination (phi)*hk0 + (b)*hps
  have E2 : a*b*phi - b^2*phi - b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (b^2)*hps
  have E3 : a*c - b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E4 : a*c*phi - b*c*phi - b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (b*c)*hps
  have E5 : a*d - b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E6 : a*e - b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E7 : a*e*phi - b*e*phi - b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (b*e)*hps
  have E8 : b - c*phi + d = 0 := by linear_combination (1)*hk1
  have E9 : b*phi - c*phi - c + d*phi = 0 := by linear_combination (phi)*hk1 + (c)*hps
  have E10 : a*b - a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E11 : a*b*phi - a*c*phi - a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (a*c)*hps
  have E12 : b^2 - b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E13 : b*c - c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E14 : b*c*phi - c^2*phi - c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (c^2)*hps
  have E15 : b*e - c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E16 : b*e*phi - c*e*phi - c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (c*e)*hps
  have E17 : c - 2*d*phi + e = 0 := by linear_combination (1)*hk2
  have E18 : c*phi - 2*d*phi - 2*d + e*phi = 0 := by linear_combination (phi)*hk2 + (2*d)*hps
  have E19 : a*c - 2*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E20 : b*c - 2*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E21 : b*c*phi - 2*b*d*phi - 2*b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (2*b*d)*hps
  have E22 : c^2 - 2*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E23 : c^2*phi - 2*c*d*phi - 2*c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (2*c*d)*hps
  have E24 : c*d - 2*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E25 : c*d*phi - 2*d^2*phi - 2*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (2*d^2)*hps
  have E26 : c*e*phi - 2*d*e*phi - 2*d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (2*d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, h2, h3]

lemma case113 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 1*phi*b) (hk1 : b+d = 1*phi*c) (hk2 : c+e = 3*phi*d)
    (hk0f : 1+a < (1+1)*(phi*b)) (hk1f : 1+b < (1+1)*(phi*c)) (hk2f : 1+c < (3+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 2*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 2*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 4*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ -2*b*c^2*phi - b*c^2 + c := by
    have hr : (0:ℝ) ≤ (c)*(-2*b*c*phi - b*c + 1) := mul_nonneg hc.le hs1
    have he : (c)*(-2*b*c*phi - b*c + 1) = -2*b*c^2*phi - b*c^2 + c := by linear_combination (0)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -2*c*d*e*phi - c*d*e + c := by
    have hr : (0:ℝ) ≤ (c)*(-2*d*e*phi - d*e + 1) := mul_nonneg hc.le hs3
    have he : (c)*(-2*d*e*phi - d*e + 1) = -2*c*d*e*phi - c*d*e + c := by linear_combination (0)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ c*e + d*e*phi - e := by
    have hr : (0:ℝ) ≤ (e)*(c + d*phi - 1) := mul_nonneg he2.le rcd
    have he : (e)*(c + d*phi - 1) = c*e + d*e*phi - e := by linear_combination (0)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ c*e*phi + d*e*phi + d*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rcd)
    have he : phi*((e)*(c + d*phi - 1)) = c*e*phi + d*e*phi + d*e - e*phi := by linear_combination (d*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -c*d + c - d^2*phi + d*phi + d - 1 := by
    have hr : (0:ℝ) ≤ (1 - d)*(c + d*phi - 1) := mul_nonneg cdc rcd
    have he : (1 - d)*(c + d*phi - 1) = -c*d + c - d^2*phi + d*phi + d - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -c*d*phi + c*phi - d^2*phi - d^2 + 2*d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cdc rcd)
    have he : phi*((1 - d)*(c + d*phi - 1)) = -c*d*phi + c*phi - d^2*phi - d^2 + 2*d*phi + d - phi := by linear_combination (-d^2 + d)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*b*c*d*phi + 2*b*c*d - 3*b*c*phi - 2*b*c - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*b*c*phi - b*c + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs1)
    have he : phi*((1 - d)*(-2*b*c*phi - b*c + 1)) = 3*b*c*d*phi + 2*b*c*d - 3*b*c*phi - 2*b*c - d*phi + phi := by linear_combination (2*b*c*d - 2*b*c)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 2*d^2*e*phi + d^2*e - 2*d*e*phi - d*e - d + 1 := by
    have hr : (0:ℝ) ≤ (1 - d)*(-2*d*e*phi - d*e + 1) := mul_nonneg cdc hs3
    have he : (1 - d)*(-2*d*e*phi - d*e + 1) = 2*d^2*e*phi + d^2*e - 2*d*e*phi - d*e - d + 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs3)
    have he : phi*((1 - d)*(-2*d*e*phi - d*e + 1)) = 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by linear_combination (2*d^2*e - 2*d*e)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ a*c*phi + a*d*phi + a*d - a*phi + b*c*phi + b*c + 2*b*d*phi + b*d - b*phi - b - c*phi - d*phi - d + phi := by
    have hr : (0:ℝ) ≤ phi*((a + b*phi - 1)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rab rcd)
    have he : phi*((a + b*phi - 1)*(c + d*phi - 1)) = a*c*phi + a*d*phi + a*d - a*phi + b*c*phi + b*c + 2*b*d*phi + b*d - b*phi - b - c*phi - d*phi - d + phi := by linear_combination (a*d + b*c + b*d*phi + b*d - b - d)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -3*b*d*e*phi - 2*b*d*e + b*phi - 5*c*d*e*phi - 3*c*d*e + c*phi + c + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg rbc hs3)
    have he : phi*((b + c*phi - 1)*(-2*d*e*phi - d*e + 1)) = -3*b*d*e*phi - 2*b*d*e + b*phi - 5*c*d*e*phi - 3*c*d*e + c*phi + c + 3*d*e*phi + 2*d*e - phi := by linear_combination (-2*b*d*e - 2*c*d*e*phi - 3*c*d*e + c + 2*d*e)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ b*c*phi + b*c + 2*b*d*phi + b*d - b*phi - b + c^2*phi + c*d*phi + c*d - 2*c*phi - d*phi - d + phi := by
    have hr : (0:ℝ) ≤ phi*((c + d*phi - 1)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg rcd gbc)
    have he : phi*((c + d*phi - 1)*(b*phi + c - 1)) = b*c*phi + b*c + 2*b*d*phi + b*d - b*phi - b + c^2*phi + c*d*phi + c*d - 2*c*phi - d*phi - d + phi := by linear_combination (b*c + b*d*phi + b*d - b + c*d - d)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ a^2*phi + a^2 + 2*a*b*phi - 2*a*phi + b^2 - 2*b + 1 := by
    have hr : (0:ℝ) ≤ (a*phi + b - 1)*(a*phi + b - 1) := mul_nonneg gab gab
    have he : (a*phi + b - 1)*(a*phi + b - 1) = a^2*phi + a^2 + 2*a*b*phi - 2*a*phi + b^2 - 2*b + 1 := by linear_combination (a^2)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 2*a^2*phi + a^2 + 2*a*b*phi + 2*a*b - 2*a*phi - 2*a + b^2*phi - 2*b*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((a*phi + b - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg gab gab)
    have he : phi*((a*phi + b - 1)*(a*phi + b - 1)) = 2*a^2*phi + a^2 + 2*a*b*phi + 2*a*b - 2*a*phi - 2*a + b^2*phi - 2*b*phi + phi := by linear_combination (a^2*phi + a^2 + 2*a*b - 2*a)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 10*c*d*e*phi - 6*c*d*e + 2*c*phi + 2*c + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 2*c*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs3)
    have he : phi*((-b + 2*c*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 10*c*d*e*phi - 6*c*d*e + 2*c*phi + 2*c + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*b*d*e - 4*c*d*e*phi - 6*c*d*e + 2*c + 2*d*e)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 2*b*c^2*phi + b*c^2 - 12*b*c*d*phi - 8*b*c*d + 2*b*c*phi + b*c - c + 4*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 4*d*phi - 1)*(-2*b*c*phi - b*c + 1) := mul_nonneg hf2 hs1
    have he : (-c + 4*d*phi - 1)*(-2*b*c*phi - b*c + 1) = 2*b*c^2*phi + b*c^2 - 12*b*c*d*phi - 8*b*c*d + 2*b*c*phi + b*c - c + 4*d*phi - 1 := by linear_combination (-8*b*c*d)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 2*c*d*e*phi + c*d*e - c - 12*d^2*e*phi - 8*d^2*e + 2*d*e*phi + d*e + 4*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 4*d*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf2 hs3
    have he : (-c + 4*d*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*c*d*e*phi + c*d*e - c - 12*d^2*e*phi - 8*d^2*e + 2*d*e*phi + d*e + 4*d*phi - 1 := by linear_combination (-8*d^2*e)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 20*d^2*e*phi - 12*d^2*e + 3*d*e*phi + 2*d*e + 4*d*phi + 4*d - phi := by
    have hr : (0:ℝ) ≤ phi*((-c + 4*d*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf2 hs3)
    have he : phi*((-c + 4*d*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 20*d^2*e*phi - 12*d^2*e + 3*d*e*phi + 2*d*e + 4*d*phi + 4*d - phi := by linear_combination (2*c*d*e - 8*d^2*e*phi - 12*d^2*e + 2*d*e + 4*d)*hps
    linarith [hr, he]
  have E0 : a - b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - b*phi - b + c*phi = 0 := by linear_combination (phi)*hk0 + (b)*hps
  have E2 : a^2 - a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a^2*phi - a*b*phi - a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (a*b)*hps
  have E4 : a*c - b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E5 : a*c*phi - b*c*phi - b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (b*c)*hps
  have E6 : a*d*phi - b*d*phi - b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (b*d)*hps
  have E7 : a*e - b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E8 : a*e*phi - b*e*phi - b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (b*e)*hps
  have E9 : b - c*phi + d = 0 := by linear_combination (1)*hk1
  have E10 : b*phi - c*phi - c + d*phi = 0 := by linear_combination (phi)*hk1 + (c)*hps
  have E11 : a*b - a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E12 : a*b*phi - a*c*phi - a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (a*c)*hps
  have E13 : b^2 - b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E14 : b^2*phi - b*c*phi - b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (b*c)*hps
  have E15 : b*c - c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E16 : b*c*phi - c^2*phi - c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (c^2)*hps
  have E17 : b*d - c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E18 : b*e*phi - c*e*phi - c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (c*e)*hps
  have E19 : c - 3*d*phi + e = 0 := by linear_combination (1)*hk2
  have E20 : c*phi - 3*d*phi - 3*d + e*phi = 0 := by linear_combination (phi)*hk2 + (3*d)*hps
  have E21 : a*c - 3*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E22 : a*c*phi - 3*a*d*phi - 3*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (3*a*d)*hps
  have E23 : b*c - 3*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E24 : c^2 - 3*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E25 : c^2*phi - 3*c*d*phi - 3*c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (3*c*d)*hps
  have E26 : c*d - 3*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E27 : c*d*phi - 3*d^2*phi - 3*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (3*d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, E27, h2, h3]

lemma case121 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 1*phi*b) (hk1 : b+d = 2*phi*c) (hk2 : c+e = 1*phi*d)
    (hk0f : 1+a < (1+1)*(phi*b)) (hk1f : 1+b < (2+1)*(phi*c)) (hk2f : 1+c < (1+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 2*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 2*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ b^2*phi + b*c*phi + b*c - b*phi := by
    have hr : (0:ℝ) ≤ phi*((b)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le rbc)
    have he : phi*((b)*(b + c*phi - 1)) = b^2*phi + b*c*phi + b*c - b*phi := by linear_combination (b*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*a*b^2*phi - 2*a*b^2 + b*phi := by
    have hr : (0:ℝ) ≤ phi*((b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le hs0)
    have he : phi*((b)*(-2*a*b*phi - a*b + 1)) = -3*a*b^2*phi - 2*a*b^2 + b*phi := by linear_combination (-2*a*b^2)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ c*d*phi + c*d + d^2*phi - d*phi := by
    have hr : (0:ℝ) ≤ phi*((d)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg hd.le gcd)
    have he : phi*((d)*(c*phi + d - 1)) = c*d*phi + c*d + d^2*phi - d*phi := by linear_combination (c*d)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -3*d^2*e*phi - 2*d^2*e + d*phi := by
    have hr : (0:ℝ) ≤ phi*((d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hd.le hs3)
    have he : phi*((d)*(-2*d*e*phi - d*e + 1)) = -3*d^2*e*phi - 2*d^2*e + d*phi := by linear_combination (-2*d^2*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs0)
    have he : phi*((1 - b)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by linear_combination (2*a*b^2 - 2*a*b)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -b*c + b - c^2*phi + c*phi + c - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(b + c*phi - 1) := mul_nonneg cc rbc
    have he : (1 - c)*(b + c*phi - 1) = -b*c + b - c^2*phi + c*phi + c - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -c^2*phi - c*d + c*phi + c + d - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(c*phi + d - 1) := mul_nonneg cc gcd
    have he : (1 - c)*(c*phi + d - 1) = -c^2*phi - c*d + c*phi + c + d - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs3)
    have he : phi*((1 - d)*(-2*d*e*phi - d*e + 1)) = 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by linear_combination (2*d^2*e - 2*d*e)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -b*e*phi + b*phi - c*e*phi - c*e + c*phi + c + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rbc)
    have he : phi*((1 - e)*(b + c*phi - 1)) = -b*e*phi + b*phi - c*e*phi - c*e + c*phi + c + e*phi - phi := by linear_combination (-c*e + c)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gab)
    have he : phi*((b + c*phi - 1)*(a*phi + b - 1)) = a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by linear_combination (a*b + a*c*phi + a*c - a + b*c - c)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg rde gcd)
    have he : phi*((d + e*phi - 1)*(c*phi + d - 1)) = c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by linear_combination (c*d + c*e*phi + c*e - c + d*e - e)*hps
    linarith [hr, he]
  have E0 : a - b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - b*phi - b + c*phi = 0 := by linear_combination (phi)*hk0 + (b)*hps
  have E2 : a*b - b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*c*phi - b*c*phi - b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (b*c)*hps
  have E4 : a*d - b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E5 : a*d*phi - b*d*phi - b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (b*d)*hps
  have E6 : a*e - b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E7 : b*phi - 2*c*phi - 2*c + d*phi = 0 := by linear_combination (phi)*hk1 + (2*c)*hps
  have E8 : a*b - 2*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E9 : a*b*phi - 2*a*c*phi - 2*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (2*a*c)*hps
  have E10 : b*c - 2*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E11 : b*d - 2*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E12 : b*d*phi - 2*c*d*phi - 2*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (2*c*d)*hps
  have E13 : b*e*phi - 2*c*e*phi - 2*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (2*c*e)*hps
  have E14 : c - d*phi + e = 0 := by linear_combination (1)*hk2
  have E15 : c*phi - d*phi - d + e*phi = 0 := by linear_combination (phi)*hk2 + (d)*hps
  have E16 : a*c - a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E17 : b*c*phi - b*d*phi - b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (b*d)*hps
  have E18 : c^2*phi - c*d*phi - c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (c*d)*hps
  have E19 : c*d - d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E20 : c*d*phi - d^2*phi - d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, h2, h3]

lemma case122 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 1*phi*b) (hk1 : b+d = 2*phi*c) (hk2 : c+e = 2*phi*d)
    (hk0f : 1+a < (1+1)*(phi*b)) (hk1f : 1+b < (2+1)*(phi*c)) (hk2f : 1+c < (2+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 2*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 3*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ -3*a*b^2*phi - 2*a*b^2 + b*phi := by
    have hr : (0:ℝ) ≤ phi*((b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le hs0)
    have he : phi*((b)*(-2*a*b*phi - a*b + 1)) = -3*a*b^2*phi - 2*a*b^2 + b*phi := by linear_combination (-2*a*b^2)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*b*d*e*phi - 2*b*d*e + b*phi := by
    have hr : (0:ℝ) ≤ phi*((b)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le hs3)
    have he : phi*((b)*(-2*d*e*phi - d*e + 1)) = -3*b*d*e*phi - 2*b*d*e + b*phi := by linear_combination (-2*b*d*e)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -b*e + 3*c*e*phi - e := by
    have hr : (0:ℝ) ≤ (e)*(-b + 3*c*phi - 1) := mul_nonneg he2.le hf1
    have he : (e)*(-b + 3*c*phi - 1) = -b*e + 3*c*e*phi - e := by linear_combination (0)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rcd)
    have he : phi*((1 - c)*(c + d*phi - 1)) = -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by linear_combination (-c*d + d)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -c*d*phi - c*d + c*phi + c - d^2*phi + 2*d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cdc gcd)
    have he : phi*((1 - d)*(c*phi + d - 1)) = -c*d*phi - c*d + c*phi + c - d^2*phi + 2*d*phi - phi := by linear_combination (-c*d + c)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs0)
    have he : phi*((1 - d)*(-2*a*b*phi - a*b + 1)) = 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by linear_combination (2*a*b*d - 2*a*b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs3)
    have he : phi*((1 - d)*(-2*d*e*phi - d*e + 1)) = 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by linear_combination (2*d^2*e - 2*d*e)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ce gab)
    have he : phi*((1 - e)*(a*phi + b - 1)) = -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by linear_combination (-a*e + a)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ a*b*phi + a*b + a*c*phi - a*phi + 2*b^2*phi + b^2 + b*c*phi + b*c - 2*b*phi - 2*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((a + b*phi - 1)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg rab gbc)
    have he : phi*((a + b*phi - 1)*(b*phi + c - 1)) = a*b*phi + a*b + a*c*phi - a*phi + 2*b^2*phi + b^2 + b*c*phi + b*c - 2*b*phi - 2*b - c*phi + phi := by linear_combination (a*b + b^2*phi + b^2 + b*c - 2*b)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi + b^2 + b*c*phi - 2*b - c*phi + 1 := by
    have hr : (0:ℝ) ≤ (b + c*phi - 1)*(a*phi + b - 1) := mul_nonneg rbc gab
    have he : (b + c*phi - 1)*(a*phi + b - 1) = a*b*phi + a*c*phi + a*c - a*phi + b^2 + b*c*phi - 2*b - c*phi + 1 := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gab)
    have he : phi*((b + c*phi - 1)*(a*phi + b - 1)) = a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by linear_combination (a*b + a*c*phi + a*c - a + b*c - c)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 15*a*b*c*phi - 9*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 3*c*phi + 3*c - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs0)
    have he : phi*((-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 15*a*b*c*phi - 9*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 3*c*phi + 3*c - phi := by linear_combination (2*a*b^2 - 6*a*b*c*phi - 9*a*b*c + 2*a*b + 3*c)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 15*c*d*e*phi - 9*c*d*e + 3*c*phi + 3*c + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs3)
    have he : phi*((-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 15*c*d*e*phi - 9*c*d*e + 3*c*phi + 3*c + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*b*d*e - 6*c*d*e*phi - 9*c*d*e + 3*c + 2*d*e)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 2*a*b*c*phi + a*b*c - 9*a*b*d*phi - 6*a*b*d + 2*a*b*phi + a*b - c + 3*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 3*d*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf2 hs0
    have he : (-c + 3*d*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b*c*phi + a*b*c - 9*a*b*d*phi - 6*a*b*d + 2*a*b*phi + a*b - c + 3*d*phi - 1 := by linear_combination (-6*a*b*d)*hps
    linarith [hr, he]
  have q18 : (0:ℝ) ≤ 2*c*d*e*phi + c*d*e - c - 9*d^2*e*phi - 6*d^2*e + 2*d*e*phi + d*e + 3*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 3*d*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf2 hs3
    have he : (-c + 3*d*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*c*d*e*phi + c*d*e - c - 9*d^2*e*phi - 6*d^2*e + 2*d*e*phi + d*e + 3*d*phi - 1 := by linear_combination (-6*d^2*e)*hps
    linarith [hr, he]
  have E0 : a - b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - b*phi - b + c*phi = 0 := by linear_combination (phi)*hk0 + (b)*hps
  have E2 : a*b - b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*c - b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E4 : a*e - b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E5 : a*e*phi - b*e*phi - b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (b*e)*hps
  have E6 : b - 2*c*phi + d = 0 := by linear_combination (1)*hk1
  have E7 : b*phi - 2*c*phi - 2*c + d*phi = 0 := by linear_combination (phi)*hk1 + (2*c)*hps
  have E8 : a*b - 2*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E9 : a*b*phi - 2*a*c*phi - 2*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (2*a*c)*hps
  have E10 : b^2 - 2*b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E11 : b^2*phi - 2*b*c*phi - 2*b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (2*b*c)*hps
  have E12 : b*c - 2*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*phi - 2*c^2*phi - 2*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (2*c^2)*hps
  have E14 : b*d - 2*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E15 : b*d*phi - 2*c*d*phi - 2*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (2*c*d)*hps
  have E16 : b*e - 2*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E17 : b*e*phi - 2*c*e*phi - 2*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (2*c*e)*hps
  have E18 : c - 2*d*phi + e = 0 := by linear_combination (1)*hk2
  have E19 : c*phi - 2*d*phi - 2*d + e*phi = 0 := by linear_combination (phi)*hk2 + (2*d)*hps
  have E20 : a*c - 2*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E21 : a*c*phi - 2*a*d*phi - 2*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (2*a*d)*hps
  have E22 : b*c - 2*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E23 : b*c*phi - 2*b*d*phi - 2*b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (2*b*d)*hps
  have E24 : c*d - 2*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E25 : c*d*phi - 2*d^2*phi - 2*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (2*d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, h2, h3]

lemma case123 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 1*phi*b) (hk1 : b+d = 2*phi*c) (hk2 : c+e = 3*phi*d)
    (hk0f : 1+a < (1+1)*(phi*b)) (hk1f : 1+b < (2+1)*(phi*c)) (hk2f : 1+c < (3+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 2*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 4*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ -3*a*b^2*phi - 2*a*b^2 + b*phi := by
    have hr : (0:ℝ) ≤ phi*((b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le hs0)
    have he : phi*((b)*(-2*a*b*phi - a*b + 1)) = -3*a*b^2*phi - 2*a*b^2 + b*phi := by linear_combination (-2*a*b^2)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ c*e*phi + d*e*phi + d*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rcd)
    have he : phi*((e)*(c + d*phi - 1)) = c*e*phi + d*e*phi + d*e - e*phi := by linear_combination (d*e)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -b*e + 3*c*e*phi - e := by
    have hr : (0:ℝ) ≤ (e)*(-b + 3*c*phi - 1) := mul_nonneg he2.le hf1
    have he : (e)*(-b + 3*c*phi - 1) = -b*e + 3*c*e*phi - e := by linear_combination (0)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rcd)
    have he : phi*((1 - c)*(c + d*phi - 1)) = -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by linear_combination (-c*d + d)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -c*d*phi + c*phi - d^2*phi - d^2 + 2*d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cdc rcd)
    have he : phi*((1 - d)*(c + d*phi - 1)) = -c*d*phi + c*phi - d^2*phi - d^2 + 2*d*phi + d - phi := by linear_combination (-d^2 + d)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -c*d*phi - c*d + c*phi + c - d^2*phi + 2*d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cdc gcd)
    have he : phi*((1 - d)*(c*phi + d - 1)) = -c*d*phi - c*d + c*phi + c - d^2*phi + 2*d*phi - phi := by linear_combination (-c*d + c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs0)
    have he : phi*((1 - d)*(-2*a*b*phi - a*b + 1)) = 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by linear_combination (2*a*b*d - 2*a*b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a + b*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rab)
    have he : phi*((1 - e)*(a + b*phi - 1)) = -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by linear_combination (-b*e + b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rde)
    have he : phi*((1 - e)*(d + e*phi - 1)) = -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by linear_combination (-e^2 + e)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ce gab)
    have he : phi*((1 - e)*(a*phi + b - 1)) = -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by linear_combination (-a*e + a)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ a*c*phi + a*c + a*d*phi - a*phi + 2*b*c*phi + b*c + b*d*phi + b*d - b*phi - b - c*phi - c - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((a + b*phi - 1)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg rab gcd)
    have he : phi*((a + b*phi - 1)*(c*phi + d - 1)) = a*c*phi + a*c + a*d*phi - a*phi + 2*b*c*phi + b*c + b*d*phi + b*d - b*phi - b - c*phi - c - d*phi + phi := by linear_combination (a*c + b*c*phi + b*c + b*d - b - c)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 15*a*b*c*phi - 9*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 3*c*phi + 3*c - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs0)
    have he : phi*((-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 15*a*b*c*phi - 9*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 3*c*phi + 3*c - phi := by linear_combination (2*a*b^2 - 6*a*b*c*phi - 9*a*b*c + 2*a*b + 3*c)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf2 hs0
    have he : (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by linear_combination (-8*a*b*d)*hps
    linarith [hr, he]
  have E0 : a - b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - b*phi - b + c*phi = 0 := by linear_combination (phi)*hk0 + (b)*hps
  have E2 : a*c - b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E3 : a*c*phi - b*c*phi - b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (b*c)*hps
  have E4 : a*e - b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E5 : a*e*phi - b*e*phi - b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (b*e)*hps
  have E6 : b - 2*c*phi + d = 0 := by linear_combination (1)*hk1
  have E7 : b*phi - 2*c*phi - 2*c + d*phi = 0 := by linear_combination (phi)*hk1 + (2*c)*hps
  have E8 : a*b - 2*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E9 : a*b*phi - 2*a*c*phi - 2*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (2*a*c)*hps
  have E10 : b*c - 2*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E11 : b*c*phi - 2*c^2*phi - 2*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (2*c^2)*hps
  have E12 : b*d - 2*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E13 : b*d*phi - 2*c*d*phi - 2*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (2*c*d)*hps
  have E14 : b*e - 2*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E15 : b*e*phi - 2*c*e*phi - 2*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (2*c*e)*hps
  have E16 : c - 3*d*phi + e = 0 := by linear_combination (1)*hk2
  have E17 : c*phi - 3*d*phi - 3*d + e*phi = 0 := by linear_combination (phi)*hk2 + (3*d)*hps
  have E18 : a*c - 3*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E19 : a*c*phi - 3*a*d*phi - 3*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (3*a*d)*hps
  have E20 : c^2 - 3*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E21 : c^2*phi - 3*c*d*phi - 3*c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (3*c*d)*hps
  have E22 : c*d - 3*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E23 : c*d*phi - 3*d^2*phi - 3*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (3*d^2)*hps
  have E24 : c*e - 3*d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E25 : c*e*phi - 3*d*e*phi - 3*d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (3*d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, h2, h3]

lemma case131 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 1*phi*b) (hk1 : b+d = 3*phi*c) (hk2 : c+e = 1*phi*d)
    (hk0f : 1+a < (1+1)*(phi*b)) (hk1f : 1+b < (3+1)*(phi*c)) (hk2f : 1+c < (1+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 2*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 4*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 2*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -b*c + b - c^2*phi + c*phi + c - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(b + c*phi - 1) := mul_nonneg cc rbc
    have he : (1 - c)*(b + c*phi - 1) = -b*c + b - c^2*phi + c*phi + c - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -c^2*phi - c*d + c*phi + c + d - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(c*phi + d - 1) := mul_nonneg cc gcd
    have he : (1 - c)*(c*phi + d - 1) = -c^2*phi - c*d + c*phi + c + d - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ 2*a*b*c*phi + a*b*c - 2*a*b*phi - a*b - c + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-2*a*b*phi - a*b + 1) := mul_nonneg cc hs0
    have he : (1 - c)*(-2*a*b*phi - a*b + 1) = 2*a*b*c*phi + a*b*c - 2*a*b*phi - a*b - c + 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 2*c*d*e*phi + c*d*e - c - 2*d*e*phi - d*e + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-2*d*e*phi - d*e + 1) := mul_nonneg cc hs3
    have he : (1 - c)*(-2*d*e*phi - d*e + 1) = 2*c*d*e*phi + c*d*e - c - 2*d*e*phi - d*e + 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -b*d*phi + b*phi - c*d*phi - c*d + c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cdc rbc)
    have he : phi*((1 - d)*(b + c*phi - 1)) = -b*d*phi + b*phi - c*d*phi - c*d + c*phi + c + d*phi - phi := by linear_combination (-c*d + c)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -3*a^2*b*phi - 2*a^2*b - 5*a*b^2*phi - 3*a*b^2 + 3*a*b*phi + 2*a*b + a*phi + b*phi + b - phi := by
    have hr : (0:ℝ) ≤ phi*((a + b*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg rab hs0)
    have he : phi*((a + b*phi - 1)*(-2*a*b*phi - a*b + 1)) = -3*a^2*b*phi - 2*a^2*b - 5*a*b^2*phi - 3*a*b^2 + 3*a*b*phi + 2*a*b + a*phi + b*phi + b - phi := by linear_combination (-2*a^2*b - 2*a*b^2*phi - 3*a*b^2 + 2*a*b + b)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -3*a*d*e*phi - 2*a*d*e + a*phi - 5*b*d*e*phi - 3*b*d*e + b*phi + b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((a + b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg rab hs3)
    have he : phi*((a + b*phi - 1)*(-2*d*e*phi - d*e + 1)) = -3*a*d*e*phi - 2*a*d*e + a*phi - 5*b*d*e*phi - 3*b*d*e + b*phi + b + 3*d*e*phi + 2*d*e - phi := by linear_combination (-2*a*d*e - 2*b*d*e*phi - 3*b*d*e + b + 2*d*e)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gab)
    have he : phi*((b + c*phi - 1)*(a*phi + b - 1)) = a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by linear_combination (a*b + a*c*phi + a*c - a + b*c - c)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg rde gcd)
    have he : phi*((d + e*phi - 1)*(c*phi + d - 1)) = c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by linear_combination (c*d + c*e*phi + c*e - c + d*e - e)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ -b*d - b*e*phi + b + 4*c*d*phi + 4*c*e*phi + 4*c*e - 4*c*phi - d - e*phi + 1 := by
    have hr : (0:ℝ) ≤ (d + e*phi - 1)*(-b + 4*c*phi - 1) := mul_nonneg rde hf1
    have he : (d + e*phi - 1)*(-b + 4*c*phi - 1) = -b*d - b*e*phi + b + 4*c*d*phi + 4*c*e*phi + 4*c*e - 4*c*phi - d - e*phi + 1 := by linear_combination (4*c*e)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 3*a^2*b*phi + 2*a^2*b - 10*a*b^2*phi - 6*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 2*b*phi + 2*b - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 2*b*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs0)
    have he : phi*((-a + 2*b*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a^2*b*phi + 2*a^2*b - 10*a*b^2*phi - 6*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 2*b*phi + 2*b - phi := by linear_combination (2*a^2*b - 4*a*b^2*phi - 6*a*b^2 + 2*a*b + 2*b)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 3*a*d*e*phi + 2*a*d*e - a*phi - 10*b*d*e*phi - 6*b*d*e + 2*b*phi + 2*b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 2*b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs3)
    have he : phi*((-a + 2*b*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*a*d*e*phi + 2*a*d*e - a*phi - 10*b*d*e*phi - 6*b*d*e + 2*b*phi + 2*b + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*a*d*e - 4*b*d*e*phi - 6*b*d*e + 2*b + 2*d*e)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 2*a*b^2*phi + a*b^2 - 12*a*b*c*phi - 8*a*b*c + 2*a*b*phi + a*b - b + 4*c*phi - 1 := by
    have hr : (0:ℝ) ≤ (-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf1 hs0
    have he : (-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b^2*phi + a*b^2 - 12*a*b*c*phi - 8*a*b*c + 2*a*b*phi + a*b - b + 4*c*phi - 1 := by linear_combination (-8*a*b*c)*hps
    linarith [hr, he]
  have q18 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 20*a*b*c*phi - 12*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 4*c*phi + 4*c - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs0)
    have he : phi*((-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 20*a*b*c*phi - 12*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 4*c*phi + 4*c - phi := by linear_combination (2*a*b^2 - 8*a*b*c*phi - 12*a*b*c + 2*a*b + 4*c)*hps
    linarith [hr, he]
  have q19 : (0:ℝ) ≤ 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf1 hs3
    have he : (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-8*c*d*e)*hps
    linarith [hr, he]
  have q20 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 20*c*d*e*phi - 12*c*d*e + 4*c*phi + 4*c + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs3)
    have he : phi*((-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 20*c*d*e*phi - 12*c*d*e + 4*c*phi + 4*c + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*b*d*e - 8*c*d*e*phi - 12*c*d*e + 4*c + 2*d*e)*hps
    linarith [hr, he]
  have E0 : a - b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - b*phi - b + c*phi = 0 := by linear_combination (phi)*hk0 + (b)*hps
  have E2 : a*b - b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*b*phi - b^2*phi - b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (b^2)*hps
  have E4 : a*c*phi - b*c*phi - b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (b*c)*hps
  have E5 : a*d - b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E6 : a*d*phi - b*d*phi - b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (b*d)*hps
  have E7 : a*e - b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E8 : b - 3*c*phi + d = 0 := by linear_combination (1)*hk1
  have E9 : b*phi - 3*c*phi - 3*c + d*phi = 0 := by linear_combination (phi)*hk1 + (3*c)*hps
  have E10 : a*b - 3*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E11 : b^2 - 3*b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E12 : b*c - 3*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*phi - 3*c^2*phi - 3*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (3*c^2)*hps
  have E14 : b*d - 3*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E15 : b*d*phi - 3*c*d*phi - 3*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (3*c*d)*hps
  have E16 : b*e - 3*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E17 : b*e*phi - 3*c*e*phi - 3*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (3*c*e)*hps
  have E18 : c - d*phi + e = 0 := by linear_combination (1)*hk2
  have E19 : c*phi - d*phi - d + e*phi = 0 := by linear_combination (phi)*hk2 + (d)*hps
  have E20 : a*c - a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E21 : b*c - b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E22 : b*c*phi - b*d*phi - b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (b*d)*hps
  have E23 : c*d - d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E24 : c*d*phi - d^2*phi - d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, h2, h3]

lemma case132 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 1*phi*b) (hk1 : b+d = 3*phi*c) (hk2 : c+e = 2*phi*d)
    (hk0f : 1+a < (1+1)*(phi*b)) (hk1f : 1+b < (3+1)*(phi*c)) (hk2f : 1+c < (2+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 2*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 4*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 3*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -c^2*phi - c*d + c*phi + c + d - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(c*phi + d - 1) := mul_nonneg cc gcd
    have he : (1 - c)*(c*phi + d - 1) = -c^2*phi - c*d + c*phi + c + d - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs0)
    have he : phi*((1 - d)*(-2*a*b*phi - a*b + 1)) = 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by linear_combination (2*a*b*d - 2*a*b)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs3)
    have he : phi*((1 - d)*(-2*d*e*phi - d*e + 1)) = 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by linear_combination (2*d^2*e - 2*d*e)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a + b*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rab)
    have he : phi*((1 - e)*(a + b*phi - 1)) = -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by linear_combination (-b*e + b)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi + b^2*phi + b^2 + 2*b*c*phi + b*c - 2*b*phi - b - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((a + b*phi - 1)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rab rbc)
    have he : phi*((a + b*phi - 1)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi + b^2*phi + b^2 + 2*b*c*phi + b*c - 2*b*phi - b - c*phi - c + phi := by linear_combination (a*c + b^2 + b*c*phi + b*c - b - c)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -3*a^2*b*phi - 2*a^2*b - 5*a*b^2*phi - 3*a*b^2 + 3*a*b*phi + 2*a*b + a*phi + b*phi + b - phi := by
    have hr : (0:ℝ) ≤ phi*((a + b*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg rab hs0)
    have he : phi*((a + b*phi - 1)*(-2*a*b*phi - a*b + 1)) = -3*a^2*b*phi - 2*a^2*b - 5*a*b^2*phi - 3*a*b^2 + 3*a*b*phi + 2*a*b + a*phi + b*phi + b - phi := by linear_combination (-2*a^2*b - 2*a*b^2*phi - 3*a*b^2 + 2*a*b + b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -3*a*d*e*phi - 2*a*d*e + a*phi - 5*b*d*e*phi - 3*b*d*e + b*phi + b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((a + b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg rab hs3)
    have he : phi*((a + b*phi - 1)*(-2*d*e*phi - d*e + 1)) = -3*a*d*e*phi - 2*a*d*e + a*phi - 5*b*d*e*phi - 3*b*d*e + b*phi + b + 3*d*e*phi + 2*d*e - phi := by linear_combination (-2*a*d*e - 2*b*d*e*phi - 3*b*d*e + b + 2*d*e)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi + b^2 + b*c*phi - 2*b - c*phi + 1 := by
    have hr : (0:ℝ) ≤ (b + c*phi - 1)*(a*phi + b - 1) := mul_nonneg rbc gab
    have he : (b + c*phi - 1)*(a*phi + b - 1) = a*b*phi + a*c*phi + a*c - a*phi + b^2 + b*c*phi - 2*b - c*phi + 1 := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gab)
    have he : phi*((b + c*phi - 1)*(a*phi + b - 1)) = a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by linear_combination (a*b + a*c*phi + a*c - a + b*c - c)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg rde gcd)
    have he : phi*((d + e*phi - 1)*(c*phi + d - 1)) = c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by linear_combination (c*d + c*e*phi + c*e - c + d*e - e)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ -a*b*phi + 4*a*c*phi + 4*a*c - a*phi - b^2 + 4*b*c*phi - 4*c*phi + 1 := by
    have hr : (0:ℝ) ≤ (a*phi + b - 1)*(-b + 4*c*phi - 1) := mul_nonneg gab hf1
    have he : (a*phi + b - 1)*(-b + 4*c*phi - 1) = -a*b*phi + 4*a*c*phi + 4*a*c - a*phi - b^2 + 4*b*c*phi - 4*c*phi + 1 := by linear_combination (4*a*c)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 3*a^2*b*phi + 2*a^2*b - 10*a*b^2*phi - 6*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 2*b*phi + 2*b - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 2*b*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs0)
    have he : phi*((-a + 2*b*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a^2*b*phi + 2*a^2*b - 10*a*b^2*phi - 6*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 2*b*phi + 2*b - phi := by linear_combination (2*a^2*b - 4*a*b^2*phi - 6*a*b^2 + 2*a*b + 2*b)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 3*a*d*e*phi + 2*a*d*e - a*phi - 10*b*d*e*phi - 6*b*d*e + 2*b*phi + 2*b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 2*b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs3)
    have he : phi*((-a + 2*b*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*a*d*e*phi + 2*a*d*e - a*phi - 10*b*d*e*phi - 6*b*d*e + 2*b*phi + 2*b + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*a*d*e - 4*b*d*e*phi - 6*b*d*e + 2*b + 2*d*e)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 2*a*b^2*phi + a*b^2 - 12*a*b*c*phi - 8*a*b*c + 2*a*b*phi + a*b - b + 4*c*phi - 1 := by
    have hr : (0:ℝ) ≤ (-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf1 hs0
    have he : (-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b^2*phi + a*b^2 - 12*a*b*c*phi - 8*a*b*c + 2*a*b*phi + a*b - b + 4*c*phi - 1 := by linear_combination (-8*a*b*c)*hps
    linarith [hr, he]
  have q18 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 20*a*b*c*phi - 12*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 4*c*phi + 4*c - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs0)
    have he : phi*((-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 20*a*b*c*phi - 12*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 4*c*phi + 4*c - phi := by linear_combination (2*a*b^2 - 8*a*b*c*phi - 12*a*b*c + 2*a*b + 4*c)*hps
    linarith [hr, he]
  have q19 : (0:ℝ) ≤ 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf1 hs3
    have he : (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-8*c*d*e)*hps
    linarith [hr, he]
  have q20 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 20*c*d*e*phi - 12*c*d*e + 4*c*phi + 4*c + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs3)
    have he : phi*((-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 20*c*d*e*phi - 12*c*d*e + 4*c*phi + 4*c + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*b*d*e - 8*c*d*e*phi - 12*c*d*e + 4*c + 2*d*e)*hps
    linarith [hr, he]
  have q21 : (0:ℝ) ≤ 2*a*b*c*phi + a*b*c - 9*a*b*d*phi - 6*a*b*d + 2*a*b*phi + a*b - c + 3*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 3*d*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf2 hs0
    have he : (-c + 3*d*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b*c*phi + a*b*c - 9*a*b*d*phi - 6*a*b*d + 2*a*b*phi + a*b - c + 3*d*phi - 1 := by linear_combination (-6*a*b*d)*hps
    linarith [hr, he]
  have q22 : (0:ℝ) ≤ 2*c*d*e*phi + c*d*e - c - 9*d^2*e*phi - 6*d^2*e + 2*d*e*phi + d*e + 3*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 3*d*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf2 hs3
    have he : (-c + 3*d*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*c*d*e*phi + c*d*e - c - 9*d^2*e*phi - 6*d^2*e + 2*d*e*phi + d*e + 3*d*phi - 1 := by linear_combination (-6*d^2*e)*hps
    linarith [hr, he]
  have E0 : a - b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - b*phi - b + c*phi = 0 := by linear_combination (phi)*hk0 + (b)*hps
  have E2 : a*b - b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*b*phi - b^2*phi - b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (b^2)*hps
  have E4 : a*c*phi - b*c*phi - b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (b*c)*hps
  have E5 : a*e - b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E6 : a*e*phi - b*e*phi - b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (b*e)*hps
  have E7 : b - 3*c*phi + d = 0 := by linear_combination (1)*hk1
  have E8 : b*phi - 3*c*phi - 3*c + d*phi = 0 := by linear_combination (phi)*hk1 + (3*c)*hps
  have E9 : a*b - 3*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E10 : a*b*phi - 3*a*c*phi - 3*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (3*a*c)*hps
  have E11 : b^2 - 3*b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E12 : b*c - 3*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*phi - 3*c^2*phi - 3*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (3*c^2)*hps
  have E14 : b*d*phi - 3*c*d*phi - 3*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (3*c*d)*hps
  have E15 : b*e - 3*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E16 : b*e*phi - 3*c*e*phi - 3*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (3*c*e)*hps
  have E17 : c - 2*d*phi + e = 0 := by linear_combination (1)*hk2
  have E18 : c*phi - 2*d*phi - 2*d + e*phi = 0 := by linear_combination (phi)*hk2 + (2*d)*hps
  have E19 : a*c - 2*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E20 : a*c*phi - 2*a*d*phi - 2*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (2*a*d)*hps
  have E21 : b*c - 2*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E22 : b*c*phi - 2*b*d*phi - 2*b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (2*b*d)*hps
  have E23 : c^2 - 2*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E24 : c*d - 2*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, h2, h3]

lemma case133 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 1*phi*b) (hk1 : b+d = 3*phi*c) (hk2 : c+e = 3*phi*d)
    (hk0f : 1+a < (1+1)*(phi*b)) (hk1f : 1+b < (3+1)*(phi*c)) (hk2f : 1+c < (3+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 2*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 4*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 4*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*c*phi + a*c + a*d*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gcd)
    have he : phi*((a)*(c*phi + d - 1)) = a*c*phi + a*c + a*d*phi - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*a*b^2*phi - 2*a*b^2 + b*phi := by
    have hr : (0:ℝ) ≤ phi*((b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le hs0)
    have he : phi*((b)*(-2*a*b*phi - a*b + 1)) = -3*a*b^2*phi - 2*a*b^2 + b*phi := by linear_combination (-2*a*b^2)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ c*e + d*e*phi - e := by
    have hr : (0:ℝ) ≤ (e)*(c + d*phi - 1) := mul_nonneg he2.le rcd
    have he : (e)*(c + d*phi - 1) = c*e + d*e*phi - e := by linear_combination (0)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -b*e + 4*c*e*phi - e := by
    have hr : (0:ℝ) ≤ (e)*(-b + 4*c*phi - 1) := mul_nonneg he2.le hf1
    have he : (e)*(-b + 4*c*phi - 1) = -b*e + 4*c*e*phi - e := by linear_combination (0)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rcd)
    have he : phi*((1 - c)*(c + d*phi - 1)) = -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by linear_combination (-c*d + d)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -c*d*phi - c*d + c*phi + c - d^2*phi + 2*d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cdc gcd)
    have he : phi*((1 - d)*(c*phi + d - 1)) = -c*d*phi - c*d + c*phi + c - d^2*phi + 2*d*phi - phi := by linear_combination (-c*d + c)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs0)
    have he : phi*((1 - d)*(-2*a*b*phi - a*b + 1)) = 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by linear_combination (2*a*b*d - 2*a*b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a + b*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rab)
    have he : phi*((1 - e)*(a + b*phi - 1)) = -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by linear_combination (-b*e + b)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rde)
    have he : phi*((1 - e)*(d + e*phi - 1)) = -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by linear_combination (-e^2 + e)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ce gab)
    have he : phi*((1 - e)*(a*phi + b - 1)) = -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by linear_combination (-a*e + a)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 20*a*b*c*phi - 12*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 4*c*phi + 4*c - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs0)
    have he : phi*((-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 20*a*b*c*phi - 12*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 4*c*phi + 4*c - phi := by linear_combination (2*a*b^2 - 8*a*b*c*phi - 12*a*b*c + 2*a*b + 4*c)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf2 hs0
    have he : (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by linear_combination (-8*a*b*d)*hps
    linarith [hr, he]
  have E0 : a - b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - b*phi - b + c*phi = 0 := by linear_combination (phi)*hk0 + (b)*hps
  have E2 : a*b*phi - b^2*phi - b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (b^2)*hps
  have E3 : a*c*phi - b*c*phi - b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (b*c)*hps
  have E4 : a*d*phi - b*d*phi - b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (b*d)*hps
  have E5 : a*e - b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E6 : a*e*phi - b*e*phi - b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (b*e)*hps
  have E7 : b - 3*c*phi + d = 0 := by linear_combination (1)*hk1
  have E8 : b*phi - 3*c*phi - 3*c + d*phi = 0 := by linear_combination (phi)*hk1 + (3*c)*hps
  have E9 : a*b - 3*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E10 : a*b*phi - 3*a*c*phi - 3*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (3*a*c)*hps
  have E11 : b^2 - 3*b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E12 : b^2*phi - 3*b*c*phi - 3*b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (3*b*c)*hps
  have E13 : b*c - 3*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E14 : b*c*phi - 3*c^2*phi - 3*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (3*c^2)*hps
  have E15 : b*d - 3*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E16 : b*d*phi - 3*c*d*phi - 3*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (3*c*d)*hps
  have E17 : b*e - 3*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E18 : b*e*phi - 3*c*e*phi - 3*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (3*c*e)*hps
  have E19 : c - 3*d*phi + e = 0 := by linear_combination (1)*hk2
  have E20 : c*phi - 3*d*phi - 3*d + e*phi = 0 := by linear_combination (phi)*hk2 + (3*d)*hps
  have E21 : a*c - 3*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E22 : a*c*phi - 3*a*d*phi - 3*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (3*a*d)*hps
  have E23 : b*c - 3*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E24 : c*d - 3*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E25 : c*d*phi - 3*d^2*phi - 3*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (3*d^2)*hps
  have E26 : c*e - 3*d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E27 : c*e*phi - 3*d*e*phi - 3*d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (3*d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, E27, h2, h3]

lemma case211 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 2*phi*b) (hk1 : b+d = 1*phi*c) (hk2 : c+e = 1*phi*d)
    (hk0f : 1+a < (2+1)*(phi*b)) (hk1f : 1+b < (1+1)*(phi*c)) (hk2f : 1+c < (1+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 2*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 2*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a^2*phi + a*b*phi + a*b - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(a + b*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rab)
    have he : phi*((a)*(a + b*phi - 1)) = a^2*phi + a*b*phi + a*b - a*phi := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ c*d*phi + c*e*phi + c*e - c*phi := by
    have hr : (0:ℝ) ≤ phi*((c)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg hc.le rde)
    have he : phi*((c)*(d + e*phi - 1)) = c*d*phi + c*e*phi + c*e - c*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ a*d*phi + b*d*phi + b*d - d*phi := by
    have hr : (0:ℝ) ≤ phi*((d)*(a + b*phi - 1)) := mul_nonneg hpos.le (mul_nonneg hd.le rab)
    have he : phi*((d)*(a + b*phi - 1)) = a*d*phi + b*d*phi + b*d - d*phi := by linear_combination (b*d)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ d^2*phi + d*e*phi + d*e - d*phi := by
    have hr : (0:ℝ) ≤ phi*((d)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg hd.le rde)
    have he : phi*((d)*(d + e*phi - 1)) = d^2*phi + d*e*phi + d*e - d*phi := by linear_combination (d*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -3*c*d^2*phi - 2*c*d^2 + d*phi := by
    have hr : (0:ℝ) ≤ phi*((d)*(-2*c*d*phi - c*d + 1)) := mul_nonneg hpos.le (mul_nonneg hd.le hs2)
    have he : phi*((d)*(-2*c*d*phi - c*d + 1)) = -3*c*d^2*phi - 2*c*d^2 + d*phi := by linear_combination (-2*c*d^2)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ b*e*phi + b*e + c*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gbc)
    have he : phi*((e)*(b*phi + c - 1)) = b*e*phi + b*e + c*e*phi - e*phi := by linear_combination (b*e)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -a*b*phi - a*b - a*c*phi + a*phi + b*phi + b + c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg ca gbc)
    have he : phi*((1 - a)*(b*phi + c - 1)) = -a*b*phi - a*b - a*c*phi + a*phi + b*phi + b + c*phi - phi := by linear_combination (-a*b + b)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -a*b + a - b^2*phi + b*phi + b - 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(a + b*phi - 1) := mul_nonneg cb rab
    have he : (1 - b)*(a + b*phi - 1) = -a*b + a - b^2*phi + b*phi + b - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -b*d - b*e*phi + b + d + e*phi - 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(d + e*phi - 1) := mul_nonneg cb rde
    have he : (1 - b)*(d + e*phi - 1) = -b*d - b*e*phi + b + d + e*phi - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -b*d*phi - b*e*phi - b*e + b*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cb rde)
    have he : phi*((1 - b)*(d + e*phi - 1)) = -b*d*phi - b*e*phi - b*e + b*phi + d*phi + e*phi + e - phi := by linear_combination (-b*e + e)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -c*d*phi - c*e*phi - c*e + c*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rde)
    have he : phi*((1 - c)*(d + e*phi - 1)) = -c*d*phi - c*e*phi - c*e + c*phi + d*phi + e*phi + e - phi := by linear_combination (-c*e + e)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ 3*c*d^2*phi + 2*c*d^2 - 3*c*d*phi - 2*c*d - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*c*d*phi - c*d + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs2)
    have he : phi*((1 - d)*(-2*c*d*phi - c*d + 1)) = 3*c*d^2*phi + 2*c*d^2 - 3*c*d*phi - 2*c*d - d*phi + phi := by linear_combination (2*c*d^2 - 2*c*d)*hps
    linarith [hr, he]
  have E0 : a - 2*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 2*b*phi - 2*b + c*phi = 0 := by linear_combination (phi)*hk0 + (2*b)*hps
  have E2 : a^2*phi - 2*a*b*phi - 2*a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (2*a*b)*hps
  have E3 : a*b - 2*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E4 : a*c*phi - 2*b*c*phi - 2*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (2*b*c)*hps
  have E5 : a*d*phi - 2*b*d*phi - 2*b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (2*b*d)*hps
  have E6 : a*e - 2*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E7 : a*e*phi - 2*b*e*phi - 2*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (2*b*e)*hps
  have E8 : b - c*phi + d = 0 := by linear_combination (1)*hk1
  have E9 : b*phi - c*phi - c + d*phi = 0 := by linear_combination (phi)*hk1 + (c)*hps
  have E10 : a*b - a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E11 : a*b*phi - a*c*phi - a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (a*c)*hps
  have E12 : b^2*phi - b*c*phi - b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (b*c)*hps
  have E13 : b*c - c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E14 : b*d - c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E15 : b*d*phi - c*d*phi - c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (c*d)*hps
  have E16 : b*e - c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E17 : b*e*phi - c*e*phi - c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (c*e)*hps
  have E18 : c - d*phi + e = 0 := by linear_combination (1)*hk2
  have E19 : c*phi - d*phi - d + e*phi = 0 := by linear_combination (phi)*hk2 + (d)*hps
  have E20 : a*c - a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E21 : a*c*phi - a*d*phi - a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (a*d)*hps
  have E22 : b*c*phi - b*d*phi - b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (b*d)*hps
  have E23 : c^2*phi - c*d*phi - c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (c*d)*hps
  have E24 : c*d*phi - d^2*phi - d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, h2, h3]

lemma case212 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 2*phi*b) (hk1 : b+d = 1*phi*c) (hk2 : c+e = 2*phi*d)
    (hk0f : 1+a < (2+1)*(phi*b)) (hk1f : 1+b < (1+1)*(phi*c)) (hk2f : 1+c < (2+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 2*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 3*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*b + a*c*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gbc)
    have he : phi*((a)*(b*phi + c - 1)) = a*b*phi + a*b + a*c*phi - a*phi := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*a*b*d*phi - 2*a*b*d + d*phi := by
    have hr : (0:ℝ) ≤ phi*((d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hd.le hs0)
    have he : phi*((d)*(-2*a*b*phi - a*b + 1)) = -3*a*b*d*phi - 2*a*b*d + d*phi := by linear_combination (-2*a*b*d)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -3*d^2*e*phi - 2*d^2*e + d*phi := by
    have hr : (0:ℝ) ≤ phi*((d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hd.le hs3)
    have he : phi*((d)*(-2*d*e*phi - d*e + 1)) = -3*d^2*e*phi - 2*d^2*e + d*phi := by linear_combination (-2*d^2*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ c*e*phi + d*e*phi + d*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rcd)
    have he : phi*((e)*(c + d*phi - 1)) = c*e*phi + d*e*phi + d*e - e*phi := by linear_combination (d*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -a*c - a*d*phi + a + c + d*phi - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(c + d*phi - 1) := mul_nonneg ca rcd
    have he : (1 - a)*(c + d*phi - 1) = -a*c - a*d*phi + a + c + d*phi - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -b*c*phi - b*d*phi - b*d + b*phi + c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cb rcd)
    have he : phi*((1 - b)*(c + d*phi - 1)) = -b*c*phi - b*d*phi - b*d + b*phi + c*phi + d*phi + d - phi := by linear_combination (-b*d + d)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -c^2 - c*d*phi + 2*c + d*phi - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(c + d*phi - 1) := mul_nonneg cc rcd
    have he : (1 - c)*(c + d*phi - 1) = -c^2 - c*d*phi + 2*c + d*phi - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -b*d*phi - b*d + b*phi + b - c*d*phi + c*phi + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cdc gbc)
    have he : phi*((1 - d)*(b*phi + c - 1)) = -b*d*phi - b*d + b*phi + b - c*d*phi + c*phi + d*phi - phi := by linear_combination (-b*d + b)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs0)
    have he : phi*((1 - d)*(-2*a*b*phi - a*b + 1)) = 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by linear_combination (2*a*b*d - 2*a*b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs3)
    have he : phi*((1 - d)*(-2*d*e*phi - d*e + 1)) = 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by linear_combination (2*d^2*e - 2*d*e)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -b*e*phi - b*e + b*phi + b - c*e*phi + c*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg ce gbc)
    have he : phi*((1 - e)*(b*phi + c - 1)) = -b*e*phi - b*e + b*phi + b - c*e*phi + c*phi + e*phi - phi := by linear_combination (-b*e + b)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ c*d*phi + c*e*phi + c*e - c*phi + d^2*phi + d^2 + 2*d*e*phi + d*e - 2*d*phi - d - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((c + d*phi - 1)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rcd rde)
    have he : phi*((c + d*phi - 1)*(d + e*phi - 1)) = c*d*phi + c*e*phi + c*e - c*phi + d^2*phi + d^2 + 2*d*e*phi + d*e - 2*d*phi - d - e*phi - e + phi := by linear_combination (c*e + d^2 + d*e*phi + d*e - d - e)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ 2*a*b*phi + a*b + a*c*phi + a*c - a*phi - a + b^2*phi + b^2 + b*c*phi - 2*b*phi - b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((a*phi + b - 1)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg gab gbc)
    have he : phi*((a*phi + b - 1)*(b*phi + c - 1)) = 2*a*b*phi + a*b + a*c*phi + a*c - a*phi - a + b^2*phi + b^2 + b*c*phi - 2*b*phi - b - c*phi + phi := by linear_combination (a*b*phi + a*b + a*c - a + b^2 - b)*hps
    linarith [hr, he]
  have E0 : a - 2*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 2*b*phi - 2*b + c*phi = 0 := by linear_combination (phi)*hk0 + (2*b)*hps
  have E2 : a*b - 2*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*d - 2*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E4 : a*e - 2*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E5 : a*e*phi - 2*b*e*phi - 2*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (2*b*e)*hps
  have E6 : b - c*phi + d = 0 := by linear_combination (1)*hk1
  have E7 : b*phi - c*phi - c + d*phi = 0 := by linear_combination (phi)*hk1 + (c)*hps
  have E8 : a*b - a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E9 : a*b*phi - a*c*phi - a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (a*c)*hps
  have E10 : b^2 - b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E11 : b^2*phi - b*c*phi - b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (b*c)*hps
  have E12 : b*c - c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*d - c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E14 : b*d*phi - c*d*phi - c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (c*d)*hps
  have E15 : b*e - c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E16 : b*e*phi - c*e*phi - c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (c*e)*hps
  have E17 : c - 2*d*phi + e = 0 := by linear_combination (1)*hk2
  have E18 : c*phi - 2*d*phi - 2*d + e*phi = 0 := by linear_combination (phi)*hk2 + (2*d)*hps
  have E19 : a*c - 2*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E20 : a*c*phi - 2*a*d*phi - 2*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (2*a*d)*hps
  have E21 : b*c*phi - 2*b*d*phi - 2*b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (2*b*d)*hps
  have E22 : c^2 - 2*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E23 : c^2*phi - 2*c*d*phi - 2*c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (2*c*d)*hps
  have E24 : c*d - 2*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E25 : c*d*phi - 2*d^2*phi - 2*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (2*d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, h2, h3]

lemma case213 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 2*phi*b) (hk1 : b+d = 1*phi*c) (hk2 : c+e = 3*phi*d)
    (hk0f : 1+a < (2+1)*(phi*b)) (hk1f : 1+b < (1+1)*(phi*c)) (hk2f : 1+c < (3+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 2*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 4*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*c*phi + a*d*phi + a*d - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rcd)
    have he : phi*((a)*(c + d*phi - 1)) = a*c*phi + a*d*phi + a*d - a*phi := by linear_combination (a*d)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -2*a*b*c*phi - a*b*c + c := by
    have hr : (0:ℝ) ≤ (c)*(-2*a*b*phi - a*b + 1) := mul_nonneg hc.le hs0
    have he : (c)*(-2*a*b*phi - a*b + 1) = -2*a*b*c*phi - a*b*c + c := by linear_combination (0)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -2*c*d*e*phi - c*d*e + c := by
    have hr : (0:ℝ) ≤ (c)*(-2*d*e*phi - d*e + 1) := mul_nonneg hc.le hs3
    have he : (c)*(-2*d*e*phi - d*e + 1) = -2*c*d*e*phi - c*d*e + c := by linear_combination (0)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ c*e + d*e*phi - e := by
    have hr : (0:ℝ) ≤ (e)*(c + d*phi - 1) := mul_nonneg he2.le rcd
    have he : (e)*(c + d*phi - 1) = c*e + d*e*phi - e := by linear_combination (0)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ c*e*phi + d*e*phi + d*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rcd)
    have he : phi*((e)*(c + d*phi - 1)) = c*e*phi + d*e*phi + d*e - e*phi := by linear_combination (d*e)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -c^2 - c*d*phi + 2*c + d*phi - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(c + d*phi - 1) := mul_nonneg cc rcd
    have he : (1 - c)*(c + d*phi - 1) = -c^2 - c*d*phi + 2*c + d*phi - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -c*d*phi + c*phi - d^2*phi - d^2 + 2*d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cdc rcd)
    have he : phi*((1 - d)*(c + d*phi - 1)) = -c*d*phi + c*phi - d^2*phi - d^2 + 2*d*phi + d - phi := by linear_combination (-d^2 + d)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs0)
    have he : phi*((1 - d)*(-2*a*b*phi - a*b + 1)) = 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by linear_combination (2*a*b*d - 2*a*b)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs3)
    have he : phi*((1 - d)*(-2*d*e*phi - d*e + 1)) = 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by linear_combination (2*d^2*e - 2*d*e)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a + b*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rab)
    have he : phi*((1 - e)*(a + b*phi - 1)) = -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by linear_combination (-b*e + b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -a*e*phi + a*phi - b*e + b + e - 1 := by
    have hr : (0:ℝ) ≤ (1 - e)*(a*phi + b - 1) := mul_nonneg ce gab
    have he : (1 - e)*(a*phi + b - 1) = -a*e*phi + a*phi - b*e + b + e - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ce gab)
    have he : phi*((1 - e)*(a*phi + b - 1)) = -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by linear_combination (-a*e + a)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ 2*a*b*phi + a*b + a*c*phi + a*c - a*phi - a + b^2*phi + b^2 + b*c*phi - 2*b*phi - b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((a*phi + b - 1)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg gab gbc)
    have he : phi*((a*phi + b - 1)*(b*phi + c - 1)) = 2*a*b*phi + a*b + a*c*phi + a*c - a*phi - a + b^2*phi + b^2 + b*c*phi - 2*b*phi - b - c*phi + phi := by linear_combination (a*b*phi + a*b + a*c - a + b^2 - b)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf2 hs0
    have he : (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by linear_combination (-8*a*b*d)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*c*d*e*phi + c*d*e - c - 12*d^2*e*phi - 8*d^2*e + 2*d*e*phi + d*e + 4*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 4*d*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf2 hs3
    have he : (-c + 4*d*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*c*d*e*phi + c*d*e - c - 12*d^2*e*phi - 8*d^2*e + 2*d*e*phi + d*e + 4*d*phi - 1 := by linear_combination (-8*d^2*e)*hps
    linarith [hr, he]
  have E0 : a - 2*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 2*b*phi - 2*b + c*phi = 0 := by linear_combination (phi)*hk0 + (2*b)*hps
  have E2 : a*b - 2*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*b*phi - 2*b^2*phi - 2*b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (2*b^2)*hps
  have E4 : a*c*phi - 2*b*c*phi - 2*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (2*b*c)*hps
  have E5 : a*d - 2*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E6 : a*e - 2*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E7 : a*e*phi - 2*b*e*phi - 2*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (2*b*e)*hps
  have E8 : b - c*phi + d = 0 := by linear_combination (1)*hk1
  have E9 : b*phi - c*phi - c + d*phi = 0 := by linear_combination (phi)*hk1 + (c)*hps
  have E10 : a*b*phi - a*c*phi - a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (a*c)*hps
  have E11 : b^2*phi - b*c*phi - b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (b*c)*hps
  have E12 : b*c - c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*phi - c^2*phi - c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (c^2)*hps
  have E14 : b*d*phi - c*d*phi - c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (c*d)*hps
  have E15 : b*e - c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E16 : b*e*phi - c*e*phi - c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (c*e)*hps
  have E17 : c - 3*d*phi + e = 0 := by linear_combination (1)*hk2
  have E18 : c*phi - 3*d*phi - 3*d + e*phi = 0 := by linear_combination (phi)*hk2 + (3*d)*hps
  have E19 : a*c - 3*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E20 : a*c*phi - 3*a*d*phi - 3*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (3*a*d)*hps
  have E21 : b*c - 3*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E22 : c^2 - 3*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E23 : c*d - 3*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E24 : c*d*phi - 3*d^2*phi - 3*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (3*d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, h2, h3]

lemma case221 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 2*phi*b) (hk1 : b+d = 2*phi*c) (hk2 : c+e = 1*phi*d)
    (hk0f : 1+a < (2+1)*(phi*b)) (hk1f : 1+b < (2+1)*(phi*c)) (hk2f : 1+c < (1+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 2*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b + a*c*phi - a := by
    have hr : (0:ℝ) ≤ (a)*(b + c*phi - 1) := mul_nonneg ha.le rbc
    have he : (a)*(b + c*phi - 1) = a*b + a*c*phi - a := by linear_combination (0)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -3*a^2*b*phi - 2*a^2*b + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs0)
    have he : phi*((a)*(-2*a*b*phi - a*b + 1)) = -3*a^2*b*phi - 2*a^2*b + a*phi := by linear_combination (-2*a^2*b)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -3*a*d*e*phi - 2*a*d*e + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs3)
    have he : phi*((a)*(-2*d*e*phi - d*e + 1)) = -3*a*d*e*phi - 2*a*d*e + a*phi := by linear_combination (-2*a*d*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca rde)
    have he : phi*((1 - a)*(d + e*phi - 1)) = -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by linear_combination (-a*e + e)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cb rbc)
    have he : phi*((1 - b)*(b + c*phi - 1)) = -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs0)
    have he : phi*((1 - b)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by linear_combination (2*a*b^2 - 2*a*b)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs3)
    have he : phi*((1 - b)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*b*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cc gbc)
    have he : phi*((1 - c)*(b*phi + c - 1)) = -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by linear_combination (-b*c + b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ c*d*phi + c*d + c*e*phi - c*phi + 2*d^2*phi + d^2 + d*e*phi + d*e - 2*d*phi - 2*d - e*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((c + d*phi - 1)*(d*phi + e - 1)) := mul_nonneg hpos.le (mul_nonneg rcd gde)
    have he : phi*((c + d*phi - 1)*(d*phi + e - 1)) = c*d*phi + c*d + c*e*phi - c*phi + 2*d^2*phi + d^2 + d*e*phi + d*e - 2*d*phi - 2*d - e*phi + phi := by linear_combination (c*d + d^2*phi + d^2 + d*e - 2*d)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg rde gcd)
    have he : phi*((d + e*phi - 1)*(c*phi + d - 1)) = c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by linear_combination (c*d + c*e*phi + c*e - c + d*e - e)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ -b*d - b*e*phi + b + 3*c*d*phi + 3*c*e*phi + 3*c*e - 3*c*phi - d - e*phi + 1 := by
    have hr : (0:ℝ) ≤ (d + e*phi - 1)*(-b + 3*c*phi - 1) := mul_nonneg rde hf1
    have he : (d + e*phi - 1)*(-b + 3*c*phi - 1) = -b*d - b*e*phi + b + 3*c*d*phi + 3*c*e*phi + 3*c*e - 3*c*phi - d - e*phi + 1 := by linear_combination (3*c*e)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 3*a^2*b*phi + 2*a^2*b - 15*a*b^2*phi - 9*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 3*b*phi + 3*b - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 3*b*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs0)
    have he : phi*((-a + 3*b*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a^2*b*phi + 2*a^2*b - 15*a*b^2*phi - 9*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 3*b*phi + 3*b - phi := by linear_combination (2*a^2*b - 6*a*b^2*phi - 9*a*b^2 + 2*a*b + 3*b)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 3*a*d*e*phi + 2*a*d*e - a*phi - 15*b*d*e*phi - 9*b*d*e + 3*b*phi + 3*b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 3*b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs3)
    have he : phi*((-a + 3*b*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*a*d*e*phi + 2*a*d*e - a*phi - 15*b*d*e*phi - 9*b*d*e + 3*b*phi + 3*b + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*a*d*e - 6*b*d*e*phi - 9*b*d*e + 3*b + 2*d*e)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 2*a*b^2*phi + a*b^2 - 9*a*b*c*phi - 6*a*b*c + 2*a*b*phi + a*b - b + 3*c*phi - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf1 hs0
    have he : (-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b^2*phi + a*b^2 - 9*a*b*c*phi - 6*a*b*c + 2*a*b*phi + a*b - b + 3*c*phi - 1 := by linear_combination (-6*a*b*c)*hps
    linarith [hr, he]
  have q18 : (0:ℝ) ≤ 2*b*d*e*phi + b*d*e - b - 9*c*d*e*phi - 6*c*d*e + 3*c*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf1 hs3
    have he : (-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*b*d*e*phi + b*d*e - b - 9*c*d*e*phi - 6*c*d*e + 3*c*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-6*c*d*e)*hps
    linarith [hr, he]
  have E0 : a - 2*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 2*b*phi - 2*b + c*phi = 0 := by linear_combination (phi)*hk0 + (2*b)*hps
  have E2 : a*b - 2*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*c - 2*b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E4 : a*c*phi - 2*b*c*phi - 2*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (2*b*c)*hps
  have E5 : a*d - 2*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E6 : a*d*phi - 2*b*d*phi - 2*b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (2*b*d)*hps
  have E7 : a*e - 2*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E8 : b - 2*c*phi + d = 0 := by linear_combination (1)*hk1
  have E9 : b*phi - 2*c*phi - 2*c + d*phi = 0 := by linear_combination (phi)*hk1 + (2*c)*hps
  have E10 : a*b - 2*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E11 : a*b*phi - 2*a*c*phi - 2*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (2*a*c)*hps
  have E12 : b*c - 2*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*phi - 2*c^2*phi - 2*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (2*c^2)*hps
  have E14 : b*d - 2*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E15 : b*d*phi - 2*c*d*phi - 2*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (2*c*d)*hps
  have E16 : c - d*phi + e = 0 := by linear_combination (1)*hk2
  have E17 : c*phi - d*phi - d + e*phi = 0 := by linear_combination (phi)*hk2 + (d)*hps
  have E18 : a*c - a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E19 : a*c*phi - a*d*phi - a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (a*d)*hps
  have E20 : c^2 - c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E21 : c^2*phi - c*d*phi - c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (c*d)*hps
  have E22 : c*d - d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E23 : c*d*phi - d^2*phi - d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, h2, h3]

lemma case222 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 2*phi*b) (hk1 : b+d = 2*phi*c) (hk2 : c+e = 2*phi*d)
    (hk0f : 1+a < (2+1)*(phi*b)) (hk1f : 1+b < (2+1)*(phi*c)) (hk2f : 1+c < (2+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 3*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*a^2*b*phi - 2*a^2*b + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs0)
    have he : phi*((a)*(-2*a*b*phi - a*b + 1)) = -3*a^2*b*phi - 2*a^2*b + a*phi := by linear_combination (-2*a^2*b)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -3*a*d*e*phi - 2*a*d*e + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs3)
    have he : phi*((a)*(-2*d*e*phi - d*e + 1)) = -3*a*d*e*phi - 2*a*d*e + a*phi := by linear_combination (-2*a*d*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ a*c*phi - 3*a*d*phi - 3*a*d + a*phi - c*phi + 3*d*phi + 3*d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(-c + 3*d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca hf2)
    have he : phi*((1 - a)*(-c + 3*d*phi - 1)) = a*c*phi - 3*a*d*phi - 3*a*d + a*phi - c*phi + 3*d*phi + 3*d - phi := by linear_combination (-3*a*d + 3*d)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -b*c*phi - b*c - b*d*phi + b*phi + c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cb gcd)
    have he : phi*((1 - b)*(c*phi + d - 1)) = -b*c*phi - b*c - b*d*phi + b*phi + c*phi + c + d*phi - phi := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rcd)
    have he : phi*((1 - c)*(c + d*phi - 1)) = -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by linear_combination (-c*d + d)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -b*d*phi + b*phi - c*d*phi - c*d + c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cdc rbc)
    have he : phi*((1 - d)*(b + c*phi - 1)) = -b*d*phi + b*phi - c*d*phi - c*d + c*phi + c + d*phi - phi := by linear_combination (-c*d + c)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs0)
    have he : phi*((1 - d)*(-2*a*b*phi - a*b + 1)) = 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by linear_combination (2*a*b*d - 2*a*b)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs3)
    have he : phi*((1 - d)*(-2*d*e*phi - d*e + 1)) = 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by linear_combination (2*d^2*e - 2*d*e)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gab)
    have he : phi*((b + c*phi - 1)*(a*phi + b - 1)) = a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by linear_combination (a*b + a*c*phi + a*c - a + b*c - c)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ -b*d*phi - b*e*phi - b*e + b*phi + 3*c*d*phi + 3*c*d + 6*c*e*phi + 3*c*e - 3*c*phi - 3*c - d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(-b + 3*c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rde hf1)
    have he : phi*((d + e*phi - 1)*(-b + 3*c*phi - 1)) = -b*d*phi - b*e*phi - b*e + b*phi + 3*c*d*phi + 3*c*d + 6*c*e*phi + 3*c*e - 3*c*phi - 3*c - d*phi - e*phi - e + phi := by linear_combination (-b*e + 3*c*d + 3*c*e*phi + 3*c*e - 3*c - e)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 3*a^2*b*phi + 2*a^2*b - 15*a*b^2*phi - 9*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 3*b*phi + 3*b - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 3*b*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs0)
    have he : phi*((-a + 3*b*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a^2*b*phi + 2*a^2*b - 15*a*b^2*phi - 9*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 3*b*phi + 3*b - phi := by linear_combination (2*a^2*b - 6*a*b^2*phi - 9*a*b^2 + 2*a*b + 3*b)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 3*a*d*e*phi + 2*a*d*e - a*phi - 15*b*d*e*phi - 9*b*d*e + 3*b*phi + 3*b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 3*b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs3)
    have he : phi*((-a + 3*b*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*a*d*e*phi + 2*a*d*e - a*phi - 15*b*d*e*phi - 9*b*d*e + 3*b*phi + 3*b + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*a*d*e - 6*b*d*e*phi - 9*b*d*e + 3*b + 2*d*e)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 2*a*b^2*phi + a*b^2 - 9*a*b*c*phi - 6*a*b*c + 2*a*b*phi + a*b - b + 3*c*phi - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf1 hs0
    have he : (-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b^2*phi + a*b^2 - 9*a*b*c*phi - 6*a*b*c + 2*a*b*phi + a*b - b + 3*c*phi - 1 := by linear_combination (-6*a*b*c)*hps
    linarith [hr, he]
  have q18 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 15*a*b*c*phi - 9*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 3*c*phi + 3*c - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs0)
    have he : phi*((-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 15*a*b*c*phi - 9*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 3*c*phi + 3*c - phi := by linear_combination (2*a*b^2 - 6*a*b*c*phi - 9*a*b*c + 2*a*b + 3*c)*hps
    linarith [hr, he]
  have q19 : (0:ℝ) ≤ 2*b*d*e*phi + b*d*e - b - 9*c*d*e*phi - 6*c*d*e + 3*c*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf1 hs3
    have he : (-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*b*d*e*phi + b*d*e - b - 9*c*d*e*phi - 6*c*d*e + 3*c*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-6*c*d*e)*hps
    linarith [hr, he]
  have q20 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 15*c*d*e*phi - 9*c*d*e + 3*c*phi + 3*c + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs3)
    have he : phi*((-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 15*c*d*e*phi - 9*c*d*e + 3*c*phi + 3*c + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*b*d*e - 6*c*d*e*phi - 9*c*d*e + 3*c + 2*d*e)*hps
    linarith [hr, he]
  have q21 : (0:ℝ) ≤ 2*a*b*c*phi + a*b*c - 9*a*b*d*phi - 6*a*b*d + 2*a*b*phi + a*b - c + 3*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 3*d*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf2 hs0
    have he : (-c + 3*d*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b*c*phi + a*b*c - 9*a*b*d*phi - 6*a*b*d + 2*a*b*phi + a*b - c + 3*d*phi - 1 := by linear_combination (-6*a*b*d)*hps
    linarith [hr, he]
  have q22 : (0:ℝ) ≤ 2*c*d*e*phi + c*d*e - c - 9*d^2*e*phi - 6*d^2*e + 2*d*e*phi + d*e + 3*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 3*d*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf2 hs3
    have he : (-c + 3*d*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*c*d*e*phi + c*d*e - c - 9*d^2*e*phi - 6*d^2*e + 2*d*e*phi + d*e + 3*d*phi - 1 := by linear_combination (-6*d^2*e)*hps
    linarith [hr, he]
  have E0 : a - 2*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 2*b*phi - 2*b + c*phi = 0 := by linear_combination (phi)*hk0 + (2*b)*hps
  have E2 : a*b - 2*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*b*phi - 2*b^2*phi - 2*b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (2*b^2)*hps
  have E4 : a*c - 2*b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E5 : a*c*phi - 2*b*c*phi - 2*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (2*b*c)*hps
  have E6 : a*d - 2*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E7 : a*e*phi - 2*b*e*phi - 2*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (2*b*e)*hps
  have E8 : b - 2*c*phi + d = 0 := by linear_combination (1)*hk1
  have E9 : b*phi - 2*c*phi - 2*c + d*phi = 0 := by linear_combination (phi)*hk1 + (2*c)*hps
  have E10 : a*b*phi - 2*a*c*phi - 2*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (2*a*c)*hps
  have E11 : b^2 - 2*b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E12 : b*c - 2*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*phi - 2*c^2*phi - 2*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (2*c^2)*hps
  have E14 : b*d - 2*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E15 : b*d*phi - 2*c*d*phi - 2*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (2*c*d)*hps
  have E16 : b*e - 2*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E17 : b*e*phi - 2*c*e*phi - 2*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (2*c*e)*hps
  have E18 : c - 2*d*phi + e = 0 := by linear_combination (1)*hk2
  have E19 : c*phi - 2*d*phi - 2*d + e*phi = 0 := by linear_combination (phi)*hk2 + (2*d)*hps
  have E20 : a*c*phi - 2*a*d*phi - 2*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (2*a*d)*hps
  have E21 : b*c - 2*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E22 : b*c*phi - 2*b*d*phi - 2*b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (2*b*d)*hps
  have E23 : c*d - 2*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E24 : c*d*phi - 2*d^2*phi - 2*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (2*d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, h2, h3]

lemma case223 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 2*phi*b) (hk1 : b+d = 2*phi*c) (hk2 : c+e = 3*phi*d)
    (hk0f : 1+a < (2+1)*(phi*b)) (hk1f : 1+b < (2+1)*(phi*c)) (hk2f : 1+c < (3+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 4*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*c*phi + a*c + a*d*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gcd)
    have he : phi*((a)*(c*phi + d - 1)) = a*c*phi + a*c + a*d*phi - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*a*b^2*phi - 2*a*b^2 + b*phi := by
    have hr : (0:ℝ) ≤ phi*((b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hbp.le hs0)
    have he : phi*((b)*(-2*a*b*phi - a*b + 1)) = -3*a*b^2*phi - 2*a*b^2 + b*phi := by linear_combination (-2*a*b^2)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -b*c*phi - b*c - b*d*phi + b*phi + c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cb gcd)
    have he : phi*((1 - b)*(c*phi + d - 1)) = -b*c*phi - b*c - b*d*phi + b*phi + c*phi + c + d*phi - phi := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rcd)
    have he : phi*((1 - c)*(c + d*phi - 1)) = -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by linear_combination (-c*d + d)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs0)
    have he : phi*((1 - d)*(-2*a*b*phi - a*b + 1)) = 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by linear_combination (2*a*b*d - 2*a*b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a + b*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rab)
    have he : phi*((1 - e)*(a + b*phi - 1)) = -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by linear_combination (-b*e + b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rde)
    have he : phi*((1 - e)*(d + e*phi - 1)) = -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by linear_combination (-e^2 + e)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ce gab)
    have he : phi*((1 - e)*(a*phi + b - 1)) = -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by linear_combination (-a*e + a)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ -b*d*phi - b*e*phi - b*e + b*phi + 3*c*d*phi + 3*c*d + 6*c*e*phi + 3*c*e - 3*c*phi - 3*c - d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(-b + 3*c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rde hf1)
    have he : phi*((d + e*phi - 1)*(-b + 3*c*phi - 1)) = -b*d*phi - b*e*phi - b*e + b*phi + 3*c*d*phi + 3*c*d + 6*c*e*phi + 3*c*e - 3*c*phi - 3*c - d*phi - e*phi - e + phi := by linear_combination (-b*e + 3*c*d + 3*c*e*phi + 3*c*e - 3*c - e)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 15*a*b*c*phi - 9*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 3*c*phi + 3*c - phi := by
    have hr : (0:ℝ) ≤ phi*((-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf1 hs0)
    have he : phi*((-b + 3*c*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 15*a*b*c*phi - 9*a*b*c + 3*a*b*phi + 2*a*b - b*phi + 3*c*phi + 3*c - phi := by linear_combination (2*a*b^2 - 6*a*b*c*phi - 9*a*b*c + 2*a*b + 3*c)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf2 hs0
    have he : (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by linear_combination (-8*a*b*d)*hps
    linarith [hr, he]
  have E0 : a - 2*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 2*b*phi - 2*b + c*phi = 0 := by linear_combination (phi)*hk0 + (2*b)*hps
  have E2 : a*c - 2*b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E3 : a*c*phi - 2*b*c*phi - 2*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (2*b*c)*hps
  have E4 : a*d - 2*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E5 : a*e - 2*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E6 : a*e*phi - 2*b*e*phi - 2*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (2*b*e)*hps
  have E7 : b - 2*c*phi + d = 0 := by linear_combination (1)*hk1
  have E8 : b*phi - 2*c*phi - 2*c + d*phi = 0 := by linear_combination (phi)*hk1 + (2*c)*hps
  have E9 : a*b - 2*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E10 : a*b*phi - 2*a*c*phi - 2*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (2*a*c)*hps
  have E11 : b*c - 2*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E12 : b*c*phi - 2*c^2*phi - 2*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (2*c^2)*hps
  have E13 : b*d - 2*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E14 : b*e*phi - 2*c*e*phi - 2*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (2*c*e)*hps
  have E15 : c - 3*d*phi + e = 0 := by linear_combination (1)*hk2
  have E16 : c*phi - 3*d*phi - 3*d + e*phi = 0 := by linear_combination (phi)*hk2 + (3*d)*hps
  have E17 : a*c - 3*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E18 : b*c - 3*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E19 : b*c*phi - 3*b*d*phi - 3*b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (3*b*d)*hps
  have E20 : c^2 - 3*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E21 : c^2*phi - 3*c*d*phi - 3*c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (3*c*d)*hps
  have E22 : c*d - 3*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E23 : c*d*phi - 3*d^2*phi - 3*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (3*d^2)*hps
  have E24 : c*e - 3*d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E25 : c*e*phi - 3*d*e*phi - 3*d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (3*d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, h2, h3]

lemma case231 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 2*phi*b) (hk1 : b+d = 3*phi*c) (hk2 : c+e = 1*phi*d)
    (hk0f : 1+a < (2+1)*(phi*b)) (hk1f : 1+b < (3+1)*(phi*c)) (hk2f : 1+c < (1+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 4*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 2*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*a^2*b*phi - 2*a^2*b + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs0)
    have he : phi*((a)*(-2*a*b*phi - a*b + 1)) = -3*a^2*b*phi - 2*a^2*b + a*phi := by linear_combination (-2*a^2*b)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -3*a*d*e*phi - 2*a*d*e + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs3)
    have he : phi*((a)*(-2*d*e*phi - d*e + 1)) = -3*a*d*e*phi - 2*a*d*e + a*phi := by linear_combination (-2*a*d*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d*phi + e - 1)) := mul_nonneg hpos.le (mul_nonneg ca gde)
    have he : phi*((1 - a)*(d*phi + e - 1)) = -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by linear_combination (-a*d + d)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs0)
    have he : phi*((1 - b)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by linear_combination (2*a*b^2 - 2*a*b)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs3)
    have he : phi*((1 - b)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*b*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -b*c + b - c^2*phi + c*phi + c - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(b + c*phi - 1) := mul_nonneg cc rbc
    have he : (1 - c)*(b + c*phi - 1) = -b*c + b - c^2*phi + c*phi + c - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cc gbc)
    have he : phi*((1 - c)*(b*phi + c - 1)) = -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by linear_combination (-b*c + b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ b*d + b*e*phi - b + c*d*phi + c*e*phi + c*e - c*phi - d - e*phi + 1 := by
    have hr : (0:ℝ) ≤ (b + c*phi - 1)*(d + e*phi - 1) := mul_nonneg rbc rde
    have he : (b + c*phi - 1)*(d + e*phi - 1) = b*d + b*e*phi - b + c*d*phi + c*e*phi + c*e - c*phi - d - e*phi + 1 := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gab)
    have he : phi*((b + c*phi - 1)*(a*phi + b - 1)) = a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by linear_combination (a*b + a*c*phi + a*c - a + b*c - c)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg rde gcd)
    have he : phi*((d + e*phi - 1)*(c*phi + d - 1)) = c*d*phi + c*d + 2*c*e*phi + c*e - c*phi - c + d^2*phi + d*e*phi + d*e - 2*d*phi - e*phi - e + phi := by linear_combination (c*d + c*e*phi + c*e - c + d*e - e)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ -b*d - b*e*phi + b + 4*c*d*phi + 4*c*e*phi + 4*c*e - 4*c*phi - d - e*phi + 1 := by
    have hr : (0:ℝ) ≤ (d + e*phi - 1)*(-b + 4*c*phi - 1) := mul_nonneg rde hf1
    have he : (d + e*phi - 1)*(-b + 4*c*phi - 1) = -b*d - b*e*phi + b + 4*c*d*phi + 4*c*e*phi + 4*c*e - 4*c*phi - d - e*phi + 1 := by linear_combination (4*c*e)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 3*a^2*b*phi + 2*a^2*b - 15*a*b^2*phi - 9*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 3*b*phi + 3*b - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 3*b*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs0)
    have he : phi*((-a + 3*b*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a^2*b*phi + 2*a^2*b - 15*a*b^2*phi - 9*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 3*b*phi + 3*b - phi := by linear_combination (2*a^2*b - 6*a*b^2*phi - 9*a*b^2 + 2*a*b + 3*b)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 3*a*d*e*phi + 2*a*d*e - a*phi - 15*b*d*e*phi - 9*b*d*e + 3*b*phi + 3*b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 3*b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs3)
    have he : phi*((-a + 3*b*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*a*d*e*phi + 2*a*d*e - a*phi - 15*b*d*e*phi - 9*b*d*e + 3*b*phi + 3*b + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*a*d*e - 6*b*d*e*phi - 9*b*d*e + 3*b + 2*d*e)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 2*a*b^2*phi + a*b^2 - 12*a*b*c*phi - 8*a*b*c + 2*a*b*phi + a*b - b + 4*c*phi - 1 := by
    have hr : (0:ℝ) ≤ (-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf1 hs0
    have he : (-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b^2*phi + a*b^2 - 12*a*b*c*phi - 8*a*b*c + 2*a*b*phi + a*b - b + 4*c*phi - 1 := by linear_combination (-8*a*b*c)*hps
    linarith [hr, he]
  have q18 : (0:ℝ) ≤ 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf1 hs3
    have he : (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-8*c*d*e)*hps
    linarith [hr, he]
  have E0 : a - 2*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 2*b*phi - 2*b + c*phi = 0 := by linear_combination (phi)*hk0 + (2*b)*hps
  have E2 : a*b - 2*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*b*phi - 2*b^2*phi - 2*b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (2*b^2)*hps
  have E4 : a*c*phi - 2*b*c*phi - 2*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (2*b*c)*hps
  have E5 : a*d - 2*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E6 : a*d*phi - 2*b*d*phi - 2*b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (2*b*d)*hps
  have E7 : a*e - 2*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E8 : b - 3*c*phi + d = 0 := by linear_combination (1)*hk1
  have E9 : b*phi - 3*c*phi - 3*c + d*phi = 0 := by linear_combination (phi)*hk1 + (3*c)*hps
  have E10 : a*b - 3*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E11 : a*b*phi - 3*a*c*phi - 3*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (3*a*c)*hps
  have E12 : b^2 - 3*b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E13 : b*c - 3*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E14 : b*c*phi - 3*c^2*phi - 3*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (3*c^2)*hps
  have E15 : b*d - 3*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E16 : b*d*phi - 3*c*d*phi - 3*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (3*c*d)*hps
  have E17 : b*e*phi - 3*c*e*phi - 3*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (3*c*e)*hps
  have E18 : c - d*phi + e = 0 := by linear_combination (1)*hk2
  have E19 : c*phi - d*phi - d + e*phi = 0 := by linear_combination (phi)*hk2 + (d)*hps
  have E20 : a*c - a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E21 : a*c*phi - a*d*phi - a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (a*d)*hps
  have E22 : c^2 - c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E23 : c*d - d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E24 : c*d*phi - d^2*phi - d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, h2, h3]

lemma case232 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 2*phi*b) (hk1 : b+d = 3*phi*c) (hk2 : c+e = 2*phi*d)
    (hk0f : 1+a < (2+1)*(phi*b)) (hk1f : 1+b < (3+1)*(phi*c)) (hk2f : 1+c < (2+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 4*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 3*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*c*phi + a*c + a*d*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gcd)
    have he : phi*((a)*(c*phi + d - 1)) = a*c*phi + a*c + a*d*phi - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -3*a^2*b*phi - 2*a^2*b + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs0)
    have he : phi*((a)*(-2*a*b*phi - a*b + 1)) = -3*a^2*b*phi - 2*a^2*b + a*phi := by linear_combination (-2*a^2*b)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -3*a*d*e*phi - 2*a*d*e + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs3)
    have he : phi*((a)*(-2*d*e*phi - d*e + 1)) = -3*a*d*e*phi - 2*a*d*e + a*phi := by linear_combination (-2*a*d*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d*phi + e - 1)) := mul_nonneg hpos.le (mul_nonneg ca gde)
    have he : phi*((1 - a)*(d*phi + e - 1)) = -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by linear_combination (-a*d + d)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -b*c*phi - b*c - b*d*phi + b*phi + c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cb gcd)
    have he : phi*((1 - b)*(c*phi + d - 1)) = -b*c*phi - b*c - b*d*phi + b*phi + c*phi + c + d*phi - phi := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs0)
    have he : phi*((1 - b)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by linear_combination (2*a*b^2 - 2*a*b)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs3)
    have he : phi*((1 - b)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*b*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rcd)
    have he : phi*((1 - c)*(c + d*phi - 1)) = -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by linear_combination (-c*d + d)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cc gbc)
    have he : phi*((1 - c)*(b*phi + c - 1)) = -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by linear_combination (-b*c + b)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs0)
    have he : phi*((1 - c)*(-2*a*b*phi - a*b + 1)) = 3*a*b*c*phi + 2*a*b*c - 3*a*b*phi - 2*a*b - c*phi + phi := by linear_combination (2*a*b*c - 2*a*b)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 3*a^2*b*phi + 2*a^2*b - 15*a*b^2*phi - 9*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 3*b*phi + 3*b - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 3*b*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs0)
    have he : phi*((-a + 3*b*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a^2*b*phi + 2*a^2*b - 15*a*b^2*phi - 9*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 3*b*phi + 3*b - phi := by linear_combination (2*a^2*b - 6*a*b^2*phi - 9*a*b^2 + 2*a*b + 3*b)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 3*a*d*e*phi + 2*a*d*e - a*phi - 15*b*d*e*phi - 9*b*d*e + 3*b*phi + 3*b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 3*b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs3)
    have he : phi*((-a + 3*b*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*a*d*e*phi + 2*a*d*e - a*phi - 15*b*d*e*phi - 9*b*d*e + 3*b*phi + 3*b + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*a*d*e - 6*b*d*e*phi - 9*b*d*e + 3*b + 2*d*e)*hps
    linarith [hr, he]
  have q17 : (0:ℝ) ≤ 2*a*b^2*phi + a*b^2 - 12*a*b*c*phi - 8*a*b*c + 2*a*b*phi + a*b - b + 4*c*phi - 1 := by
    have hr : (0:ℝ) ≤ (-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf1 hs0
    have he : (-b + 4*c*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b^2*phi + a*b^2 - 12*a*b*c*phi - 8*a*b*c + 2*a*b*phi + a*b - b + 4*c*phi - 1 := by linear_combination (-8*a*b*c)*hps
    linarith [hr, he]
  have q18 : (0:ℝ) ≤ 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf1 hs3
    have he : (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-8*c*d*e)*hps
    linarith [hr, he]
  have E0 : a*phi - 2*b*phi - 2*b + c*phi = 0 := by linear_combination (phi)*hk0 + (2*b)*hps
  have E1 : a*c - 2*b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E2 : a*c*phi - 2*b*c*phi - 2*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (2*b*c)*hps
  have E3 : a*d*phi - 2*b*d*phi - 2*b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (2*b*d)*hps
  have E4 : a*e*phi - 2*b*e*phi - 2*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (2*b*e)*hps
  have E5 : b - 3*c*phi + d = 0 := by linear_combination (1)*hk1
  have E6 : b*phi - 3*c*phi - 3*c + d*phi = 0 := by linear_combination (phi)*hk1 + (3*c)*hps
  have E7 : a*b - 3*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E8 : a*b*phi - 3*a*c*phi - 3*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (3*a*c)*hps
  have E9 : b*c - 3*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E10 : b*c*phi - 3*c^2*phi - 3*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (3*c^2)*hps
  have E11 : b*d - 3*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E12 : b*e*phi - 3*c*e*phi - 3*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (3*c*e)*hps
  have E13 : c*phi - 2*d*phi - 2*d + e*phi = 0 := by linear_combination (phi)*hk2 + (2*d)*hps
  have E14 : a*c*phi - 2*a*d*phi - 2*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (2*a*d)*hps
  have E15 : b*c - 2*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E16 : b*c*phi - 2*b*d*phi - 2*b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (2*b*d)*hps
  have E17 : c^2 - 2*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E18 : c^2*phi - 2*c*d*phi - 2*c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (2*c*d)*hps
  have E19 : c*d - 2*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E20 : c*d*phi - 2*d^2*phi - 2*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (2*d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, h2, h3]

lemma case233 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 2*phi*b) (hk1 : b+d = 3*phi*c) (hk2 : c+e = 3*phi*d)
    (hk0f : 1+a < (2+1)*(phi*b)) (hk1f : 1+b < (3+1)*(phi*c)) (hk2f : 1+c < (3+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 3*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 4*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 4*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*c*phi + a*c + a*d*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gcd)
    have he : phi*((a)*(c*phi + d - 1)) = a*c*phi + a*c + a*d*phi - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : phi*((1 - a)*(a*phi + b - 1)) = -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -b*c*phi - b*c - b*d*phi + b*phi + c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cb gcd)
    have he : phi*((1 - b)*(c*phi + d - 1)) = -b*c*phi - b*c - b*d*phi + b*phi + c*phi + c + d*phi - phi := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rcd)
    have he : phi*((1 - c)*(c + d*phi - 1)) = -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by linear_combination (-c*d + d)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a + b*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rab)
    have he : phi*((1 - e)*(a + b*phi - 1)) = -a*e*phi + a*phi - b*e*phi - b*e + b*phi + b + e*phi - phi := by linear_combination (-b*e + b)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rde)
    have he : phi*((1 - e)*(d + e*phi - 1)) = -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by linear_combination (-e^2 + e)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ce gab)
    have he : phi*((1 - e)*(a*phi + b - 1)) = -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by linear_combination (-a*e + a)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -b*d*phi - b*e*phi - b*e + b*phi + 4*c*d*phi + 4*c*d + 8*c*e*phi + 4*c*e - 4*c*phi - 4*c - d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(-b + 4*c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rde hf1)
    have he : phi*((d + e*phi - 1)*(-b + 4*c*phi - 1)) = -b*d*phi - b*e*phi - b*e + b*phi + 4*c*d*phi + 4*c*d + 8*c*e*phi + 4*c*e - 4*c*phi - 4*c - d*phi - e*phi - e + phi := by linear_combination (-b*e + 4*c*d + 4*c*e*phi + 4*c*e - 4*c - e)*hps
    linarith [hr, he]
  have E0 : a - 2*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 2*b*phi - 2*b + c*phi = 0 := by linear_combination (phi)*hk0 + (2*b)*hps
  have E2 : a^2 - 2*a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a^2*phi - 2*a*b*phi - 2*a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (2*a*b)*hps
  have E4 : a*c - 2*b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E5 : a*c*phi - 2*b*c*phi - 2*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (2*b*c)*hps
  have E6 : a*e - 2*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E7 : a*e*phi - 2*b*e*phi - 2*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (2*b*e)*hps
  have E8 : b - 3*c*phi + d = 0 := by linear_combination (1)*hk1
  have E9 : b*phi - 3*c*phi - 3*c + d*phi = 0 := by linear_combination (phi)*hk1 + (3*c)*hps
  have E10 : a*b - 3*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E11 : a*b*phi - 3*a*c*phi - 3*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (3*a*c)*hps
  have E12 : b*c - 3*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*phi - 3*c^2*phi - 3*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (3*c^2)*hps
  have E14 : b*d - 3*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E15 : b*d*phi - 3*c*d*phi - 3*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (3*c*d)*hps
  have E16 : b*e*phi - 3*c*e*phi - 3*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (3*c*e)*hps
  have E17 : c - 3*d*phi + e = 0 := by linear_combination (1)*hk2
  have E18 : c*phi - 3*d*phi - 3*d + e*phi = 0 := by linear_combination (phi)*hk2 + (3*d)*hps
  have E19 : a*c - 3*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E20 : a*c*phi - 3*a*d*phi - 3*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (3*a*d)*hps
  have E21 : b*c - 3*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E22 : b*c*phi - 3*b*d*phi - 3*b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (3*b*d)*hps
  have E23 : c^2 - 3*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E24 : c*d - 3*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E25 : c*d*phi - 3*d^2*phi - 3*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (3*d^2)*hps
  have E26 : c*e - 3*d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E27 : c*e*phi - 3*d*e*phi - 3*d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (3*d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, E27, h2, h3]

lemma case311 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 3*phi*b) (hk1 : b+d = 1*phi*c) (hk2 : c+e = 1*phi*d)
    (hk0f : 1+a < (3+1)*(phi*b)) (hk1f : 1+b < (1+1)*(phi*c)) (hk2f : 1+c < (1+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 4*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 2*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 2*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*c - a := by
    have hr : (0:ℝ) ≤ (a)*(b*phi + c - 1) := mul_nonneg ha.le gbc
    have he : (a)*(b*phi + c - 1) = a*b*phi + a*c - a := by linear_combination (0)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*b*phi + a*b + a*c*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gbc)
    have he : phi*((a)*(b*phi + c - 1)) = a*b*phi + a*b + a*c*phi - a*phi := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -2*a^2*b*phi - a^2*b + a := by
    have hr : (0:ℝ) ≤ (a)*(-2*a*b*phi - a*b + 1) := mul_nonneg ha.le hs0
    have he : (a)*(-2*a*b*phi - a*b + 1) = -2*a^2*b*phi - a^2*b + a := by linear_combination (0)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -3*a^2*b*phi - 2*a^2*b + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs0)
    have he : phi*((a)*(-2*a*b*phi - a*b + 1)) = -3*a^2*b*phi - 2*a^2*b + a*phi := by linear_combination (-2*a^2*b)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -2*a*c*d*phi - a*c*d + a := by
    have hr : (0:ℝ) ≤ (a)*(-2*c*d*phi - c*d + 1) := mul_nonneg ha.le hs2
    have he : (a)*(-2*c*d*phi - c*d + 1) = -2*a*c*d*phi - a*c*d + a := by linear_combination (0)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -b^2*phi - b*c + b*phi + b + c - 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(b*phi + c - 1) := mul_nonneg cb gbc
    have he : (1 - b)*(b*phi + c - 1) = -b^2*phi - b*c + b*phi + b + c - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -b^2*phi - b^2 - b*c*phi + 2*b*phi + b + c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cb gbc)
    have he : phi*((1 - b)*(b*phi + c - 1)) = -b^2*phi - b^2 - b*c*phi + 2*b*phi + b + c*phi - phi := by linear_combination (-b^2 + b)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ 2*a*b^2*phi + a*b^2 - 2*a*b*phi - a*b - b + 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(-2*a*b*phi - a*b + 1) := mul_nonneg cb hs0
    have he : (1 - b)*(-2*a*b*phi - a*b + 1) = 2*a*b^2*phi + a*b^2 - 2*a*b*phi - a*b - b + 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs0)
    have he : phi*((1 - b)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by linear_combination (2*a*b^2 - 2*a*b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*b*c*d*phi + 2*b*c*d - b*phi - 3*c*d*phi - 2*c*d + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*c*d*phi - c*d + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs2)
    have he : phi*((1 - b)*(-2*c*d*phi - c*d + 1)) = 3*b*c*d*phi + 2*b*c*d - b*phi - 3*c*d*phi - 2*c*d + phi := by linear_combination (2*b*c*d - 2*c*d)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ b*c*phi + b*c + 2*b*d*phi + b*d - b*phi - b + c^2*phi + c*d*phi + c*d - 2*c*phi - d*phi - d + phi := by
    have hr : (0:ℝ) ≤ phi*((c + d*phi - 1)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg rcd gbc)
    have he : phi*((c + d*phi - 1)*(b*phi + c - 1)) = b*c*phi + b*c + 2*b*d*phi + b*d - b*phi - b + c^2*phi + c*d*phi + c*d - 2*c*phi - d*phi - d + phi := by linear_combination (b*c + b*d*phi + b*d - b + c*d - d)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ d^2 + 2*d*e*phi - 2*d + e^2*phi + e^2 - 2*e*phi + 1 := by
    have hr : (0:ℝ) ≤ (d + e*phi - 1)*(d + e*phi - 1) := mul_nonneg rde rde
    have he : (d + e*phi - 1)*(d + e*phi - 1) = d^2 + 2*d*e*phi - 2*d + e^2*phi + e^2 - 2*e*phi + 1 := by linear_combination (e^2)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ d^2*phi + 2*d*e*phi + 2*d*e - 2*d*phi + 2*e^2*phi + e^2 - 2*e*phi - 2*e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rde rde)
    have he : phi*((d + e*phi - 1)*(d + e*phi - 1)) = d^2*phi + 2*d*e*phi + 2*d*e - 2*d*phi + 2*e^2*phi + e^2 - 2*e*phi - 2*e + phi := by linear_combination (2*d*e + e^2*phi + e^2 - 2*e)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ -b*c*phi - b*c + 4*b*d*phi + 2*b*d - b*phi - b - c^2*phi + 2*c*d*phi + 2*c*d - 2*d*phi - 2*d + phi := by
    have hr : (0:ℝ) ≤ phi*((b*phi + c - 1)*(-c + 2*d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg gbc hf2)
    have he : phi*((b*phi + c - 1)*(-c + 2*d*phi - 1)) = -b*c*phi - b*c + 4*b*d*phi + 2*b*d - b*phi - b - c^2*phi + 2*c*d*phi + 2*c*d - 2*d*phi - 2*d + phi := by linear_combination (-b*c + 2*b*d*phi + 2*b*d - b + 2*c*d - 2*d)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*a^2*b*phi + a^2*b - 12*a*b^2*phi - 8*a*b^2 + 2*a*b*phi + a*b - a + 4*b*phi - 1 := by
    have hr : (0:ℝ) ≤ (-a + 4*b*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf0 hs0
    have he : (-a + 4*b*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a^2*b*phi + a^2*b - 12*a*b^2*phi - 8*a*b^2 + 2*a*b*phi + a*b - a + 4*b*phi - 1 := by linear_combination (-8*a*b^2)*hps
    linarith [hr, he]
  have q15 : (0:ℝ) ≤ 3*a^2*b*phi + 2*a^2*b - 20*a*b^2*phi - 12*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 4*b*phi + 4*b - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 4*b*phi - 1)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs0)
    have he : phi*((-a + 4*b*phi - 1)*(-2*a*b*phi - a*b + 1)) = 3*a^2*b*phi + 2*a^2*b - 20*a*b^2*phi - 12*a*b^2 + 3*a*b*phi + 2*a*b - a*phi + 4*b*phi + 4*b - phi := by linear_combination (2*a^2*b - 8*a*b^2*phi - 12*a*b^2 + 2*a*b + 4*b)*hps
    linarith [hr, he]
  have q16 : (0:ℝ) ≤ 2*a*c*d*phi + a*c*d - a - 12*b*c*d*phi - 8*b*c*d + 4*b*phi + 2*c*d*phi + c*d - 1 := by
    have hr : (0:ℝ) ≤ (-a + 4*b*phi - 1)*(-2*c*d*phi - c*d + 1) := mul_nonneg hf0 hs2
    have he : (-a + 4*b*phi - 1)*(-2*c*d*phi - c*d + 1) = 2*a*c*d*phi + a*c*d - a - 12*b*c*d*phi - 8*b*c*d + 4*b*phi + 2*c*d*phi + c*d - 1 := by linear_combination (-8*b*c*d)*hps
    linarith [hr, he]
  have E0 : a - 3*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 3*b*phi - 3*b + c*phi = 0 := by linear_combination (phi)*hk0 + (3*b)*hps
  have E2 : a*b - 3*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E3 : a*b*phi - 3*b^2*phi - 3*b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (3*b^2)*hps
  have E4 : a*c - 3*b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E5 : a*d - 3*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E6 : a*e - 3*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E7 : b - c*phi + d = 0 := by linear_combination (1)*hk1
  have E8 : b*phi - c*phi - c + d*phi = 0 := by linear_combination (phi)*hk1 + (c)*hps
  have E9 : a*b - a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E10 : a*b*phi - a*c*phi - a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (a*c)*hps
  have E11 : b^2*phi - b*c*phi - b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (b*c)*hps
  have E12 : b*c - c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E13 : b*c*phi - c^2*phi - c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (c^2)*hps
  have E14 : b*d - c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E15 : b*d*phi - c*d*phi - c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (c*d)*hps
  have E16 : c - d*phi + e = 0 := by linear_combination (1)*hk2
  have E17 : c*phi - d*phi - d + e*phi = 0 := by linear_combination (phi)*hk2 + (d)*hps
  have E18 : a*c - a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E19 : b*c*phi - b*d*phi - b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (b*d)*hps
  have E20 : c^2 - c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E21 : c^2*phi - c*d*phi - c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (c*d)*hps
  have E22 : c*d - d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E23 : c*d*phi - d^2*phi - d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (d^2)*hps
  have E24 : c*e - d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E25 : c*e*phi - d*e*phi - d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, h2, h3]

lemma case312 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 3*phi*b) (hk1 : b+d = 1*phi*c) (hk2 : c+e = 2*phi*d)
    (hk0f : 1+a < (3+1)*(phi*b)) (hk1f : 1+b < (1+1)*(phi*c)) (hk2f : 1+c < (2+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 4*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 2*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 3*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*b + a*c*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gbc)
    have he : phi*((a)*(b*phi + c - 1)) = a*b*phi + a*b + a*c*phi - a*phi := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -a^2 + 4*a*b*phi - a := by
    have hr : (0:ℝ) ≤ (a)*(-a + 4*b*phi - 1) := mul_nonneg ha.le hf0
    have he : (a)*(-a + 4*b*phi - 1) = -a^2 + 4*a*b*phi - a := by linear_combination (0)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -2*a^2*b*phi - a^2*b + a := by
    have hr : (0:ℝ) ≤ (a)*(-2*a*b*phi - a*b + 1) := mul_nonneg ha.le hs0
    have he : (a)*(-2*a*b*phi - a*b + 1) = -2*a^2*b*phi - a^2*b + a := by linear_combination (0)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -2*a*d*e*phi - a*d*e + a := by
    have hr : (0:ℝ) ≤ (a)*(-2*d*e*phi - d*e + 1) := mul_nonneg ha.le hs3
    have he : (a)*(-2*d*e*phi - d*e + 1) = -2*a*d*e*phi - a*d*e + a := by linear_combination (0)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ b*e*phi + b*e + c*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gbc)
    have he : phi*((e)*(b*phi + c - 1)) = b*e*phi + b*e + c*e*phi - e*phi := by linear_combination (b*e)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -a*d - a*e*phi + a + d + e*phi - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(d + e*phi - 1) := mul_nonneg ca rde
    have he : (1 - a)*(d + e*phi - 1) = -a*d - a*e*phi + a + d + e*phi - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca rde)
    have he : phi*((1 - a)*(d + e*phi - 1)) = -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by linear_combination (-a*e + e)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d*phi + e - 1)) := mul_nonneg hpos.le (mul_nonneg ca gde)
    have he : phi*((1 - a)*(d*phi + e - 1)) = -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by linear_combination (-a*d + d)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -b^2*phi - b^2 - b*c*phi + 2*b*phi + b + c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cb gbc)
    have he : phi*((1 - b)*(b*phi + c - 1)) = -b^2*phi - b^2 - b*c*phi + 2*b*phi + b + c*phi - phi := by linear_combination (-b^2 + b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs0)
    have he : phi*((1 - b)*(-2*a*b*phi - a*b + 1)) = 3*a*b^2*phi + 2*a*b^2 - 3*a*b*phi - 2*a*b - b*phi + phi := by linear_combination (2*a*b^2 - 2*a*b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs3)
    have he : phi*((1 - b)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*b*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2 + 2*c - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(b*phi + c - 1) := mul_nonneg cc gbc
    have he : (1 - c)*(b*phi + c - 1) = -b*c*phi + b*phi - c^2 + 2*c - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ c*d*phi + c*e*phi + c*e - c*phi + d^2*phi + d^2 + 2*d*e*phi + d*e - 2*d*phi - d - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((c + d*phi - 1)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rcd rde)
    have he : phi*((c + d*phi - 1)*(d + e*phi - 1)) = c*d*phi + c*e*phi + c*e - c*phi + d^2*phi + d^2 + 2*d*e*phi + d*e - 2*d*phi - d - e*phi - e + phi := by linear_combination (c*e + d^2 + d*e*phi + d*e - d - e)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 2*a^2*b*phi + a^2*b - 12*a*b^2*phi - 8*a*b^2 + 2*a*b*phi + a*b - a + 4*b*phi - 1 := by
    have hr : (0:ℝ) ≤ (-a + 4*b*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf0 hs0
    have he : (-a + 4*b*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a^2*b*phi + a^2*b - 12*a*b^2*phi - 8*a*b^2 + 2*a*b*phi + a*b - a + 4*b*phi - 1 := by linear_combination (-8*a*b^2)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*a*d*e*phi + a*d*e - a - 12*b*d*e*phi - 8*b*d*e + 4*b*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-a + 4*b*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf0 hs3
    have he : (-a + 4*b*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*a*d*e*phi + a*d*e - a - 12*b*d*e*phi - 8*b*d*e + 4*b*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-8*b*d*e)*hps
    linarith [hr, he]
  have E0 : a - 3*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 3*b*phi - 3*b + c*phi = 0 := by linear_combination (phi)*hk0 + (3*b)*hps
  have E2 : a^2 - 3*a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a*b - 3*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E4 : a*b*phi - 3*b^2*phi - 3*b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (3*b^2)*hps
  have E5 : a*d - 3*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E6 : a*d*phi - 3*b*d*phi - 3*b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (3*b*d)*hps
  have E7 : a*e - 3*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E8 : a*e*phi - 3*b*e*phi - 3*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (3*b*e)*hps
  have E9 : b - c*phi + d = 0 := by linear_combination (1)*hk1
  have E10 : b*phi - c*phi - c + d*phi = 0 := by linear_combination (phi)*hk1 + (c)*hps
  have E11 : a*b - a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E12 : a*b*phi - a*c*phi - a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (a*c)*hps
  have E13 : b^2*phi - b*c*phi - b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (b*c)*hps
  have E14 : b*c - c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E15 : b*c*phi - c^2*phi - c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (c^2)*hps
  have E16 : b*d - c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E17 : b*d*phi - c*d*phi - c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (c*d)*hps
  have E18 : b*e - c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E19 : b*e*phi - c*e*phi - c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (c*e)*hps
  have E20 : c - 2*d*phi + e = 0 := by linear_combination (1)*hk2
  have E21 : c*phi - 2*d*phi - 2*d + e*phi = 0 := by linear_combination (phi)*hk2 + (2*d)*hps
  have E22 : a*c - 2*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E23 : a*c*phi - 2*a*d*phi - 2*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (2*a*d)*hps
  have E24 : c^2*phi - 2*c*d*phi - 2*c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (2*c*d)*hps
  have E25 : c*d - 2*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E26 : c*d*phi - 2*d^2*phi - 2*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (2*d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, h2, h3]

lemma case313 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 3*phi*b) (hk1 : b+d = 1*phi*c) (hk2 : c+e = 3*phi*d)
    (hk0f : 1+a < (3+1)*(phi*b)) (hk1f : 1+b < (1+1)*(phi*c)) (hk2f : 1+c < (3+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 4*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 2*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 4*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*c*phi + a*d*phi + a*d - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rcd)
    have he : phi*((a)*(c + d*phi - 1)) = a*c*phi + a*d*phi + a*d - a*phi := by linear_combination (a*d)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*b*phi + a*b + a*c*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gbc)
    have he : phi*((a)*(b*phi + c - 1)) = a*b*phi + a*b + a*c*phi - a*phi := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -2*a*b*c*phi - a*b*c + c := by
    have hr : (0:ℝ) ≤ (c)*(-2*a*b*phi - a*b + 1) := mul_nonneg hc.le hs0
    have he : (c)*(-2*a*b*phi - a*b + 1) = -2*a*b*c*phi - a*b*c + c := by linear_combination (0)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -2*c*d*e*phi - c*d*e + c := by
    have hr : (0:ℝ) ≤ (c)*(-2*d*e*phi - d*e + 1) := mul_nonneg hc.le hs3
    have he : (c)*(-2*d*e*phi - d*e + 1) = -2*c*d*e*phi - c*d*e + c := by linear_combination (0)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ c*e*phi + d*e*phi + d*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rcd)
    have he : phi*((e)*(c + d*phi - 1)) = c*e*phi + d*e*phi + d*e - e*phi := by linear_combination (d*e)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca rde)
    have he : phi*((1 - a)*(d + e*phi - 1)) = -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by linear_combination (-a*e + e)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cb rbc)
    have he : phi*((1 - b)*(b + c*phi - 1)) = -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -b*c*phi - b*d*phi - b*d + b*phi + c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cb rcd)
    have he : phi*((1 - b)*(c + d*phi - 1)) = -b*c*phi - b*d*phi - b*d + b*phi + c*phi + d*phi + d - phi := by linear_combination (-b*d + d)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -c^2 - c*d*phi + 2*c + d*phi - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(c + d*phi - 1) := mul_nonneg cc rcd
    have he : (1 - c)*(c + d*phi - 1) = -c^2 - c*d*phi + 2*c + d*phi - 1 := by linear_combination (0)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -b*d*phi - b*d + b*phi + b - c*d*phi + c*phi + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cdc gbc)
    have he : phi*((1 - d)*(b*phi + c - 1)) = -b*d*phi - b*d + b*phi + b - c*d*phi + c*phi + d*phi - phi := by linear_combination (-b*d + b)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ b*d*phi - b*phi - 2*c*d*phi - 2*c*d + 2*c*phi + 2*c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-b + 2*c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cdc hf1)
    have he : phi*((1 - d)*(-b + 2*c*phi - 1)) = b*d*phi - b*phi - 2*c*d*phi - 2*c*d + 2*c*phi + 2*c + d*phi - phi := by linear_combination (-2*c*d + 2*c)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*a*b*phi - a*b + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs0)
    have he : phi*((1 - d)*(-2*a*b*phi - a*b + 1)) = 3*a*b*d*phi + 2*a*b*d - 3*a*b*phi - 2*a*b - d*phi + phi := by linear_combination (2*a*b*d - 2*a*b)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cdc hs3)
    have he : phi*((1 - d)*(-2*d*e*phi - d*e + 1)) = 3*d^2*e*phi + 2*d^2*e - 3*d*e*phi - 2*d*e - d*phi + phi := by linear_combination (2*d^2*e - 2*d*e)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) := mul_nonneg hf2 hs0
    have he : (-c + 4*d*phi - 1)*(-2*a*b*phi - a*b + 1) = 2*a*b*c*phi + a*b*c - 12*a*b*d*phi - 8*a*b*d + 2*a*b*phi + a*b - c + 4*d*phi - 1 := by linear_combination (-8*a*b*d)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*c*d*e*phi + c*d*e - c - 12*d^2*e*phi - 8*d^2*e + 2*d*e*phi + d*e + 4*d*phi - 1 := by
    have hr : (0:ℝ) ≤ (-c + 4*d*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf2 hs3
    have he : (-c + 4*d*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*c*d*e*phi + c*d*e - c - 12*d^2*e*phi - 8*d^2*e + 2*d*e*phi + d*e + 4*d*phi - 1 := by linear_combination (-8*d^2*e)*hps
    linarith [hr, he]
  have E0 : a*phi - 3*b*phi - 3*b + c*phi = 0 := by linear_combination (phi)*hk0 + (3*b)*hps
  have E1 : a*b - 3*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E2 : a*c - 3*b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E3 : a*c*phi - 3*b*c*phi - 3*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (3*b*c)*hps
  have E4 : a*d - 3*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E5 : a*e - 3*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E6 : a*e*phi - 3*b*e*phi - 3*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (3*b*e)*hps
  have E7 : b - c*phi + d = 0 := by linear_combination (1)*hk1
  have E8 : b*phi - c*phi - c + d*phi = 0 := by linear_combination (phi)*hk1 + (c)*hps
  have E9 : a*b - a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E10 : a*b*phi - a*c*phi - a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (a*c)*hps
  have E11 : b*c - c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E12 : b*c*phi - c^2*phi - c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (c^2)*hps
  have E13 : b*d - c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E14 : b*e - c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E15 : b*e*phi - c*e*phi - c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (c*e)*hps
  have E16 : c - 3*d*phi + e = 0 := by linear_combination (1)*hk2
  have E17 : c*phi - 3*d*phi - 3*d + e*phi = 0 := by linear_combination (phi)*hk2 + (3*d)*hps
  have E18 : a*c - 3*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E19 : a*c*phi - 3*a*d*phi - 3*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (3*a*d)*hps
  have E20 : b*c - 3*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E21 : c^2 - 3*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E22 : c*d - 3*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E23 : c*d*phi - 3*d^2*phi - 3*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (3*d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, h2, h3]

lemma case321 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 3*phi*b) (hk1 : b+d = 2*phi*c) (hk2 : c+e = 1*phi*d)
    (hk0f : 1+a < (3+1)*(phi*b)) (hk1f : 1+b < (2+1)*(phi*c)) (hk2f : 1+c < (1+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 4*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 2*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b + a*c*phi - a := by
    have hr : (0:ℝ) ≤ (a)*(b + c*phi - 1) := mul_nonneg ha.le rbc
    have he : (a)*(b + c*phi - 1) = a*b + a*c*phi - a := by linear_combination (0)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ a*b*phi + a*b + a*c*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gbc)
    have he : phi*((a)*(b*phi + c - 1)) = a*b*phi + a*b + a*c*phi - a*phi := by linear_combination (a*b)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -3*a*d*e*phi - 2*a*d*e + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs3)
    have he : phi*((a)*(-2*d*e*phi - d*e + 1)) = -3*a*d*e*phi - 2*a*d*e + a*phi := by linear_combination (-2*a*d*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca rde)
    have he : phi*((1 - a)*(d + e*phi - 1)) = -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by linear_combination (-a*e + e)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : phi*((1 - a)*(a*phi + b - 1)) = -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d*phi + e - 1)) := mul_nonneg hpos.le (mul_nonneg ca gde)
    have he : phi*((1 - a)*(d*phi + e - 1)) = -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by linear_combination (-a*d + d)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cb rbc)
    have he : phi*((1 - b)*(b + c*phi - 1)) = -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -b^2*phi - b^2 - b*c*phi + 2*b*phi + b + c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cb gbc)
    have he : phi*((1 - b)*(b*phi + c - 1)) = -b^2*phi - b^2 - b*c*phi + 2*b*phi + b + c*phi - phi := by linear_combination (-b^2 + b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs3)
    have he : phi*((1 - b)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*b*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cc gbc)
    have he : phi*((1 - c)*(b*phi + c - 1)) = -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by linear_combination (-b*c + b)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ b*d*phi + b*d + b*e*phi - b*phi + 2*c*d*phi + c*d + c*e*phi + c*e - c*phi - c - d*phi - d - e*phi + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(d*phi + e - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gde)
    have he : phi*((b + c*phi - 1)*(d*phi + e - 1)) = b*d*phi + b*d + b*e*phi - b*phi + 2*c*d*phi + c*d + c*e*phi + c*e - c*phi - c - d*phi - d - e*phi + phi := by linear_combination (b*d + c*d*phi + c*d + c*e - c - d)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 3*a*d*e*phi + 2*a*d*e - a*phi - 20*b*d*e*phi - 12*b*d*e + 4*b*phi + 4*b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 4*b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs3)
    have he : phi*((-a + 4*b*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*a*d*e*phi + 2*a*d*e - a*phi - 20*b*d*e*phi - 12*b*d*e + 4*b*phi + 4*b + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*a*d*e - 8*b*d*e*phi - 12*b*d*e + 4*b + 2*d*e)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*b*d*e*phi + b*d*e - b - 9*c*d*e*phi - 6*c*d*e + 3*c*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf1 hs3
    have he : (-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*b*d*e*phi + b*d*e - b - 9*c*d*e*phi - 6*c*d*e + 3*c*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-6*c*d*e)*hps
    linarith [hr, he]
  have E0 : a - 3*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 3*b*phi - 3*b + c*phi = 0 := by linear_combination (phi)*hk0 + (3*b)*hps
  have E2 : a^2 - 3*a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a^2*phi - 3*a*b*phi - 3*a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (3*a*b)*hps
  have E4 : a*b - 3*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E5 : a*b*phi - 3*b^2*phi - 3*b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (3*b^2)*hps
  have E6 : a*d - 3*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E7 : a*d*phi - 3*b*d*phi - 3*b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (3*b*d)*hps
  have E8 : b - 2*c*phi + d = 0 := by linear_combination (1)*hk1
  have E9 : b*phi - 2*c*phi - 2*c + d*phi = 0 := by linear_combination (phi)*hk1 + (2*c)*hps
  have E10 : a*b - 2*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E11 : a*b*phi - 2*a*c*phi - 2*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (2*a*c)*hps
  have E12 : b^2 - 2*b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E13 : b^2*phi - 2*b*c*phi - 2*b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (2*b*c)*hps
  have E14 : b*c - 2*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E15 : b*c*phi - 2*c^2*phi - 2*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (2*c^2)*hps
  have E16 : b*d*phi - 2*c*d*phi - 2*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (2*c*d)*hps
  have E17 : b*e*phi - 2*c*e*phi - 2*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (2*c*e)*hps
  have E18 : c - d*phi + e = 0 := by linear_combination (1)*hk2
  have E19 : c*phi - d*phi - d + e*phi = 0 := by linear_combination (phi)*hk2 + (d)*hps
  have E20 : a*c - a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E21 : a*c*phi - a*d*phi - a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (a*d)*hps
  have E22 : b*c*phi - b*d*phi - b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (b*d)*hps
  have E23 : c^2 - c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E24 : c^2*phi - c*d*phi - c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (c*d)*hps
  have E25 : c*d - d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, h2, h3]

lemma case322 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 3*phi*b) (hk1 : b+d = 2*phi*c) (hk2 : c+e = 2*phi*d)
    (hk0f : 1+a < (3+1)*(phi*b)) (hk1f : 1+b < (2+1)*(phi*c)) (hk2f : 1+c < (2+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 4*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 3*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ -3*a*d*e*phi - 2*a*d*e + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs3)
    have he : phi*((a)*(-2*d*e*phi - d*e + 1)) = -3*a*d*e*phi - 2*a*d*e + a*phi := by linear_combination (-2*a*d*e)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ b*e*phi + c*e*phi + c*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rbc)
    have he : phi*((e)*(b + c*phi - 1)) = b*e*phi + c*e*phi + c*e - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca rde)
    have he : phi*((1 - a)*(d + e*phi - 1)) = -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by linear_combination (-a*e + e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : phi*((1 - a)*(a*phi + b - 1)) = -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ a*c*phi - 3*a*d*phi - 3*a*d + a*phi - c*phi + 3*d*phi + 3*d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(-c + 3*d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca hf2)
    have he : phi*((1 - a)*(-c + 3*d*phi - 1)) = a*c*phi - 3*a*d*phi - 3*a*d + a*phi - c*phi + 3*d*phi + 3*d - phi := by linear_combination (-3*a*d + 3*d)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs3)
    have he : phi*((1 - b)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*b*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cc gbc)
    have he : phi*((1 - c)*(b*phi + c - 1)) = -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by linear_combination (-b*c + b)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -b*d*phi + b*phi - c*d*phi - c*d + c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cdc rbc)
    have he : phi*((1 - d)*(b + c*phi - 1)) = -b*d*phi + b*phi - c*d*phi - c*d + c*phi + c + d*phi - phi := by linear_combination (-c*d + c)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rde)
    have he : phi*((1 - e)*(d + e*phi - 1)) = -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by linear_combination (-e^2 + e)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gab)
    have he : phi*((b + c*phi - 1)*(a*phi + b - 1)) = a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by linear_combination (a*b + a*c*phi + a*c - a + b*c - c)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 3*a*d*e*phi + 2*a*d*e - a*phi - 20*b*d*e*phi - 12*b*d*e + 4*b*phi + 4*b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 4*b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs3)
    have he : phi*((-a + 4*b*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*a*d*e*phi + 2*a*d*e - a*phi - 20*b*d*e*phi - 12*b*d*e + 4*b*phi + 4*b + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*a*d*e - 8*b*d*e*phi - 12*b*d*e + 4*b + 2*d*e)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*b*d*e*phi + b*d*e - b - 9*c*d*e*phi - 6*c*d*e + 3*c*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf1 hs3
    have he : (-b + 3*c*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*b*d*e*phi + b*d*e - b - 9*c*d*e*phi - 6*c*d*e + 3*c*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-6*c*d*e)*hps
    linarith [hr, he]
  have E0 : a - 3*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 3*b*phi - 3*b + c*phi = 0 := by linear_combination (phi)*hk0 + (3*b)*hps
  have E2 : a^2 - 3*a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a^2*phi - 3*a*b*phi - 3*a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (3*a*b)*hps
  have E4 : a*b - 3*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E5 : a*b*phi - 3*b^2*phi - 3*b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (3*b^2)*hps
  have E6 : a*c*phi - 3*b*c*phi - 3*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (3*b*c)*hps
  have E7 : a*d - 3*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E8 : a*d*phi - 3*b*d*phi - 3*b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (3*b*d)*hps
  have E9 : a*e - 3*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E10 : a*e*phi - 3*b*e*phi - 3*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (3*b*e)*hps
  have E11 : b - 2*c*phi + d = 0 := by linear_combination (1)*hk1
  have E12 : b*phi - 2*c*phi - 2*c + d*phi = 0 := by linear_combination (phi)*hk1 + (2*c)*hps
  have E13 : a*b - 2*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E14 : a*b*phi - 2*a*c*phi - 2*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (2*a*c)*hps
  have E15 : b^2 - 2*b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E16 : b*c - 2*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E17 : b*c*phi - 2*c^2*phi - 2*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (2*c^2)*hps
  have E18 : b*d - 2*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E19 : b*d*phi - 2*c*d*phi - 2*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (2*c*d)*hps
  have E20 : b*e - 2*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E21 : b*e*phi - 2*c*e*phi - 2*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (2*c*e)*hps
  have E22 : c - 2*d*phi + e = 0 := by linear_combination (1)*hk2
  have E23 : c*phi - 2*d*phi - 2*d + e*phi = 0 := by linear_combination (phi)*hk2 + (2*d)*hps
  have E24 : a*c - 2*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E25 : a*c*phi - 2*a*d*phi - 2*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (2*a*d)*hps
  have E26 : c*d - 2*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E27 : c*d*phi - 2*d^2*phi - 2*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (2*d^2)*hps
  have E28 : c*e - 2*d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E29 : c*e*phi - 2*d*e*phi - 2*d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (2*d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, E27, E28, E29, h2, h3]

lemma case323 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 3*phi*b) (hk1 : b+d = 2*phi*c) (hk2 : c+e = 3*phi*d)
    (hk0f : 1+a < (3+1)*(phi*b)) (hk1f : 1+b < (2+1)*(phi*c)) (hk2f : 1+c < (3+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 4*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 3*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 4*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*c*phi + a*c + a*d*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gcd)
    have he : phi*((a)*(c*phi + d - 1)) = a*c*phi + a*c + a*d*phi - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ b*e*phi + c*e*phi + c*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rbc)
    have he : phi*((e)*(b + c*phi - 1)) = b*e*phi + c*e*phi + c*e - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : phi*((1 - a)*(a*phi + b - 1)) = -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cb rbc)
    have he : phi*((1 - b)*(b + c*phi - 1)) = -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rcd)
    have he : phi*((1 - c)*(c + d*phi - 1)) = -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by linear_combination (-c*d + d)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rde)
    have he : phi*((1 - e)*(d + e*phi - 1)) = -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by linear_combination (-e^2 + e)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ce gab)
    have he : phi*((1 - e)*(a*phi + b - 1)) = -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by linear_combination (-a*e + a)*hps
    linarith [hr, he]
  have E0 : a - 3*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 3*b*phi - 3*b + c*phi = 0 := by linear_combination (phi)*hk0 + (3*b)*hps
  have E2 : a^2 - 3*a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a^2*phi - 3*a*b*phi - 3*a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (3*a*b)*hps
  have E4 : a*b - 3*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E5 : a*c - 3*b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E6 : a*c*phi - 3*b*c*phi - 3*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (3*b*c)*hps
  have E7 : a*d - 3*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E8 : a*e - 3*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E9 : a*e*phi - 3*b*e*phi - 3*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (3*b*e)*hps
  have E10 : b - 2*c*phi + d = 0 := by linear_combination (1)*hk1
  have E11 : b*phi - 2*c*phi - 2*c + d*phi = 0 := by linear_combination (phi)*hk1 + (2*c)*hps
  have E12 : a*b - 2*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E13 : a*b*phi - 2*a*c*phi - 2*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (2*a*c)*hps
  have E14 : b*c - 2*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E15 : b*c*phi - 2*c^2*phi - 2*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (2*c^2)*hps
  have E16 : b*d*phi - 2*c*d*phi - 2*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (2*c*d)*hps
  have E17 : b*e*phi - 2*c*e*phi - 2*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (2*c*e)*hps
  have E18 : c - 3*d*phi + e = 0 := by linear_combination (1)*hk2
  have E19 : c*phi - 3*d*phi - 3*d + e*phi = 0 := by linear_combination (phi)*hk2 + (3*d)*hps
  have E20 : a*c*phi - 3*a*d*phi - 3*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (3*a*d)*hps
  have E21 : b*c - 3*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E22 : c^2 - 3*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E23 : c^2*phi - 3*c*d*phi - 3*c*d + c*e*phi = 0 := by linear_combination (c*phi)*hk2 + (3*c*d)*hps
  have E24 : c*d - 3*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E25 : c*e - 3*d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E26 : c*e*phi - 3*d*e*phi - 3*d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (3*d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, h2, h3]

lemma case331 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 3*phi*b) (hk1 : b+d = 3*phi*c) (hk2 : c+e = 1*phi*d)
    (hk0f : 1+a < (3+1)*(phi*b)) (hk1f : 1+b < (3+1)*(phi*c)) (hk2f : 1+c < (1+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 4*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 4*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 2*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b + a*c*phi - a := by
    have hr : (0:ℝ) ≤ (a)*(b + c*phi - 1) := mul_nonneg ha.le rbc
    have he : (a)*(b + c*phi - 1) = a*b + a*c*phi - a := by linear_combination (0)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -a^2 + 4*a*b*phi - a := by
    have hr : (0:ℝ) ≤ (a)*(-a + 4*b*phi - 1) := mul_nonneg ha.le hf0
    have he : (a)*(-a + 4*b*phi - 1) = -a^2 + 4*a*b*phi - a := by linear_combination (0)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -3*a*d*e*phi - 2*a*d*e + a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg ha.le hs3)
    have he : phi*((a)*(-2*d*e*phi - d*e + 1)) = -3*a*d*e*phi - 2*a*d*e + a*phi := by linear_combination (-2*a*d*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ b*e*phi + c*e*phi + c*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rbc)
    have he : phi*((e)*(b + c*phi - 1)) = b*e*phi + c*e*phi + c*e - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca rde)
    have he : phi*((1 - a)*(d + e*phi - 1)) = -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by linear_combination (-a*e + e)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : phi*((1 - a)*(a*phi + b - 1)) = -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d*phi + e - 1)) := mul_nonneg hpos.le (mul_nonneg ca gde)
    have he : phi*((1 - a)*(d*phi + e - 1)) = -a*d*phi - a*d - a*e*phi + a*phi + d*phi + d + e*phi - phi := by linear_combination (-a*d + d)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cb rbc)
    have he : phi*((1 - b)*(b + c*phi - 1)) = -b^2*phi - b*c*phi - b*c + 2*b*phi + c*phi + c - phi := by linear_combination (-b*c + c)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - b)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cb hs3)
    have he : phi*((1 - b)*(-2*d*e*phi - d*e + 1)) = 3*b*d*e*phi + 2*b*d*e - b*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*b*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q11 : (0:ℝ) ≤ -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cc gbc)
    have he : phi*((1 - c)*(b*phi + c - 1)) = -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by linear_combination (-b*c + b)*hps
    linarith [hr, he]
  have q12 : (0:ℝ) ≤ 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg cc hs3)
    have he : phi*((1 - c)*(-2*d*e*phi - d*e + 1)) = 3*c*d*e*phi + 2*c*d*e - c*phi - 3*d*e*phi - 2*d*e + phi := by linear_combination (2*c*d*e - 2*d*e)*hps
    linarith [hr, he]
  have q13 : (0:ℝ) ≤ 3*a*d*e*phi + 2*a*d*e - a*phi - 20*b*d*e*phi - 12*b*d*e + 4*b*phi + 4*b + 3*d*e*phi + 2*d*e - phi := by
    have hr : (0:ℝ) ≤ phi*((-a + 4*b*phi - 1)*(-2*d*e*phi - d*e + 1)) := mul_nonneg hpos.le (mul_nonneg hf0 hs3)
    have he : phi*((-a + 4*b*phi - 1)*(-2*d*e*phi - d*e + 1)) = 3*a*d*e*phi + 2*a*d*e - a*phi - 20*b*d*e*phi - 12*b*d*e + 4*b*phi + 4*b + 3*d*e*phi + 2*d*e - phi := by linear_combination (2*a*d*e - 8*b*d*e*phi - 12*b*d*e + 4*b + 2*d*e)*hps
    linarith [hr, he]
  have q14 : (0:ℝ) ≤ 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by
    have hr : (0:ℝ) ≤ (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) := mul_nonneg hf1 hs3
    have he : (-b + 4*c*phi - 1)*(-2*d*e*phi - d*e + 1) = 2*b*d*e*phi + b*d*e - b - 12*c*d*e*phi - 8*c*d*e + 4*c*phi + 2*d*e*phi + d*e - 1 := by linear_combination (-8*c*d*e)*hps
    linarith [hr, he]
  have E0 : a - 3*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 3*b*phi - 3*b + c*phi = 0 := by linear_combination (phi)*hk0 + (3*b)*hps
  have E2 : a^2 - 3*a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a^2*phi - 3*a*b*phi - 3*a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (3*a*b)*hps
  have E4 : a*b - 3*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E5 : a*d - 3*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E6 : a*d*phi - 3*b*d*phi - 3*b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (3*b*d)*hps
  have E7 : a*e - 3*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E8 : a*e*phi - 3*b*e*phi - 3*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (3*b*e)*hps
  have E9 : b - 3*c*phi + d = 0 := by linear_combination (1)*hk1
  have E10 : b*phi - 3*c*phi - 3*c + d*phi = 0 := by linear_combination (phi)*hk1 + (3*c)*hps
  have E11 : a*b - 3*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E12 : a*b*phi - 3*a*c*phi - 3*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (3*a*c)*hps
  have E13 : b^2*phi - 3*b*c*phi - 3*b*c + b*d*phi = 0 := by linear_combination (b*phi)*hk1 + (3*b*c)*hps
  have E14 : b*c - 3*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E15 : b*c*phi - 3*c^2*phi - 3*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (3*c^2)*hps
  have E16 : b*d - 3*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E17 : b*d*phi - 3*c*d*phi - 3*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (3*c*d)*hps
  have E18 : b*e - 3*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E19 : b*e*phi - 3*c*e*phi - 3*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (3*c*e)*hps
  have E20 : c - d*phi + e = 0 := by linear_combination (1)*hk2
  have E21 : c*phi - d*phi - d + e*phi = 0 := by linear_combination (phi)*hk2 + (d)*hps
  have E22 : a*c - a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E23 : a*c*phi - a*d*phi - a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (a*d)*hps
  have E24 : b*c*phi - b*d*phi - b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (b*d)*hps
  have E25 : c*d - d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E26 : c*d*phi - d^2*phi - d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (d^2)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, h2, h3]

lemma case332 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 3*phi*b) (hk1 : b+d = 3*phi*c) (hk2 : c+e = 2*phi*d)
    (hk0f : 1+a < (3+1)*(phi*b)) (hk1f : 1+b < (3+1)*(phi*c)) (hk2f : 1+c < (2+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 4*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 4*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 3*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ b*e*phi + c*e*phi + c*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rbc)
    have he : phi*((e)*(b + c*phi - 1)) = b*e*phi + c*e*phi + c*e - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca rde)
    have he : phi*((1 - a)*(d + e*phi - 1)) = -a*d*phi - a*e*phi - a*e + a*phi + d*phi + e*phi + e - phi := by linear_combination (-a*e + e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : phi*((1 - a)*(a*phi + b - 1)) = -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ a*c*phi - 3*a*d*phi - 3*a*d + a*phi - c*phi + 3*d*phi + 3*d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(-c + 3*d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ca hf2)
    have he : phi*((1 - a)*(-c + 3*d*phi - 1)) = a*c*phi - 3*a*d*phi - 3*a*d + a*phi - c*phi + 3*d*phi + 3*d - phi := by linear_combination (-3*a*d + 3*d)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b*phi + c - 1)) := mul_nonneg hpos.le (mul_nonneg cc gbc)
    have he : phi*((1 - c)*(b*phi + c - 1)) = -b*c*phi - b*c + b*phi + b - c^2*phi + 2*c*phi - phi := by linear_combination (-b*c + b)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -b*d*phi + b*phi - c*d*phi - c*d + c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - d)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cdc rbc)
    have he : phi*((1 - d)*(b + c*phi - 1)) = -b*d*phi + b*phi - c*d*phi - c*d + c*phi + c + d*phi - phi := by linear_combination (-c*d + c)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rde)
    have he : phi*((1 - e)*(d + e*phi - 1)) = -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by linear_combination (-e^2 + e)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by
    have hr : (0:ℝ) ≤ phi*((b + c*phi - 1)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg rbc gab)
    have he : phi*((b + c*phi - 1)*(a*phi + b - 1)) = a*b*phi + a*b + 2*a*c*phi + a*c - a*phi - a + b^2*phi + b*c*phi + b*c - 2*b*phi - c*phi - c + phi := by linear_combination (a*b + a*c*phi + a*c - a + b*c - c)*hps
    linarith [hr, he]
  have E0 : a - 3*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 3*b*phi - 3*b + c*phi = 0 := by linear_combination (phi)*hk0 + (3*b)*hps
  have E2 : a^2 - 3*a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a^2*phi - 3*a*b*phi - 3*a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (3*a*b)*hps
  have E4 : a*b - 3*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E5 : a*c - 3*b*c*phi + c^2 = 0 := by linear_combination (c*1)*hk0
  have E6 : a*c*phi - 3*b*c*phi - 3*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (3*b*c)*hps
  have E7 : a*d - 3*b*d*phi + c*d = 0 := by linear_combination (d*1)*hk0
  have E8 : a*d*phi - 3*b*d*phi - 3*b*d + c*d*phi = 0 := by linear_combination (d*phi)*hk0 + (3*b*d)*hps
  have E9 : a*e*phi - 3*b*e*phi - 3*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (3*b*e)*hps
  have E10 : b - 3*c*phi + d = 0 := by linear_combination (1)*hk1
  have E11 : b*phi - 3*c*phi - 3*c + d*phi = 0 := by linear_combination (phi)*hk1 + (3*c)*hps
  have E12 : a*b - 3*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E13 : a*b*phi - 3*a*c*phi - 3*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (3*a*c)*hps
  have E14 : b*c - 3*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E15 : b*c*phi - 3*c^2*phi - 3*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (3*c^2)*hps
  have E16 : b*d - 3*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E17 : b*d*phi - 3*c*d*phi - 3*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (3*c*d)*hps
  have E18 : b*e - 3*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E19 : b*e*phi - 3*c*e*phi - 3*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (3*c*e)*hps
  have E20 : c - 2*d*phi + e = 0 := by linear_combination (1)*hk2
  have E21 : c*phi - 2*d*phi - 2*d + e*phi = 0 := by linear_combination (phi)*hk2 + (2*d)*hps
  have E22 : a*c - 2*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E23 : a*c*phi - 2*a*d*phi - 2*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (2*a*d)*hps
  have E24 : c^2 - 2*c*d*phi + c*e = 0 := by linear_combination (c*1)*hk2
  have E25 : c*d - 2*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E26 : c*d*phi - 2*d^2*phi - 2*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (2*d^2)*hps
  have E27 : c*e - 2*d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E28 : c*e*phi - 2*d*e*phi - 2*d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (2*d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, E27, E28, h2, h3]

lemma case333 (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (hk0 : a+c = 3*phi*b) (hk1 : b+d = 3*phi*c) (hk2 : c+e = 3*phi*d)
    (hk0f : 1+a < (3+1)*(phi*b)) (hk1f : 1+b < (3+1)*(phi*c)) (hk2f : 1+c < (3+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : (0:ℝ) < phi := by linarith
  have hcube : phi^3 = 2*phi+1 := by nlinarith [hps]
  have hp3 : (0:ℝ) < phi^3 := by positivity
  have gab : (0:ℝ) ≤ a*phi + b - 1 := by nlinarith [hab']
  have gbc : (0:ℝ) ≤ b*phi + c - 1 := by nlinarith [hbc']
  have gcd : (0:ℝ) ≤ c*phi + d - 1 := by nlinarith [hcd']
  have gde : (0:ℝ) ≤ d*phi + e - 1 := by nlinarith [hde']
  have rab : (0:ℝ) ≤ a + b*phi - 1 := by nlinarith [hab]
  have rbc : (0:ℝ) ≤ b + c*phi - 1 := by nlinarith [hbc]
  have rcd : (0:ℝ) ≤ c + d*phi - 1 := by nlinarith [hcd]
  have rde : (0:ℝ) ≤ d + e*phi - 1 := by nlinarith [hde]
  have ca : (0:ℝ) ≤ 1 - a := by nlinarith [ha1]
  have cb : (0:ℝ) ≤ 1 - b := by nlinarith [hb1]
  have cc : (0:ℝ) ≤ 1 - c := by nlinarith [hc1]
  have cdc : (0:ℝ) ≤ 1 - d := by nlinarith [hd1]
  have ce : (0:ℝ) ≤ 1 - e := by nlinarith [he1]
  have hf0 : (0:ℝ) ≤ -a + 4*b*phi - 1 := by nlinarith [hk0f]
  have hf1 : (0:ℝ) ≤ -b + 4*c*phi - 1 := by nlinarith [hk1f]
  have hf2 : (0:ℝ) ≤ -c + 4*d*phi - 1 := by nlinarith [hk2f]
  have hs0 : (0:ℝ) ≤ -2*a*b*phi - a*b + 1 := by
    have hh : a*b*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    have he : a*b*phi^3 = 2*a*b*phi + a*b := by rw [hcube]; ring
    linarith [hh, he]
  have hs1 : (0:ℝ) ≤ -2*b*c*phi - b*c + 1 := by
    have hh : b*c*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    have he : b*c*phi^3 = 2*b*c*phi + b*c := by rw [hcube]; ring
    linarith [hh, he]
  have hs2 : (0:ℝ) ≤ -2*c*d*phi - c*d + 1 := by
    have hh : c*d*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    have he : c*d*phi^3 = 2*c*d*phi + c*d := by rw [hcube]; ring
    linarith [hh, he]
  have hs3 : (0:ℝ) ≤ -2*d*e*phi - d*e + 1 := by
    have hh : d*e*phi^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    have he : d*e*phi^3 = 2*d*e*phi + d*e := by rw [hcube]; ring
    linarith [hh, he]
  have q0 : (0:ℝ) ≤ a*b*phi + a*c*phi + a*c - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le rbc)
    have he : phi*((a)*(b + c*phi - 1)) = a*b*phi + a*c*phi + a*c - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q1 : (0:ℝ) ≤ a*c*phi + a*c + a*d*phi - a*phi := by
    have hr : (0:ℝ) ≤ phi*((a)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg ha.le gcd)
    have he : phi*((a)*(c*phi + d - 1)) = a*c*phi + a*c + a*d*phi - a*phi := by linear_combination (a*c)*hps
    linarith [hr, he]
  have q2 : (0:ℝ) ≤ b*e*phi + c*e*phi + c*e - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le rbc)
    have he : phi*((e)*(b + c*phi - 1)) = b*e*phi + c*e*phi + c*e - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q3 : (0:ℝ) ≤ c*e*phi + c*e + d*e*phi - e*phi := by
    have hr : (0:ℝ) ≤ phi*((e)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg he2.le gcd)
    have he : phi*((e)*(c*phi + d - 1)) = c*e*phi + c*e + d*e*phi - e*phi := by linear_combination (c*e)*hps
    linarith [hr, he]
  have q4 : (0:ℝ) ≤ -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - a)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ca gab)
    have he : phi*((1 - a)*(a*phi + b - 1)) = -a^2*phi - a^2 - a*b*phi + 2*a*phi + a + b*phi - phi := by linear_combination (-a^2 + a)*hps
    linarith [hr, he]
  have q5 : (0:ℝ) ≤ -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(b + c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rbc)
    have he : phi*((1 - c)*(b + c*phi - 1)) = -b*c*phi + b*phi - c^2*phi - c^2 + 2*c*phi + c - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q6 : (0:ℝ) ≤ -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c + d*phi - 1)) := mul_nonneg hpos.le (mul_nonneg cc rcd)
    have he : phi*((1 - c)*(c + d*phi - 1)) = -c^2*phi - c*d*phi - c*d + 2*c*phi + d*phi + d - phi := by linear_combination (-c*d + d)*hps
    linarith [hr, he]
  have q7 : (0:ℝ) ≤ -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - c)*(c*phi + d - 1)) := mul_nonneg hpos.le (mul_nonneg cc gcd)
    have he : phi*((1 - c)*(c*phi + d - 1)) = -c^2*phi - c^2 - c*d*phi + 2*c*phi + c + d*phi - phi := by linear_combination (-c^2 + c)*hps
    linarith [hr, he]
  have q8 : (0:ℝ) ≤ -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(d + e*phi - 1)) := mul_nonneg hpos.le (mul_nonneg ce rde)
    have he : phi*((1 - e)*(d + e*phi - 1)) = -d*e*phi + d*phi - e^2*phi - e^2 + 2*e*phi + e - phi := by linear_combination (-e^2 + e)*hps
    linarith [hr, he]
  have q9 : (0:ℝ) ≤ -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by
    have hr : (0:ℝ) ≤ phi*((1 - e)*(a*phi + b - 1)) := mul_nonneg hpos.le (mul_nonneg ce gab)
    have he : phi*((1 - e)*(a*phi + b - 1)) = -a*e*phi - a*e + a*phi + a - b*e*phi + b*phi + e*phi - phi := by linear_combination (-a*e + a)*hps
    linarith [hr, he]
  have q10 : (0:ℝ) ≤ -b*d*phi - b*e*phi - b*e + b*phi + 4*c*d*phi + 4*c*d + 8*c*e*phi + 4*c*e - 4*c*phi - 4*c - d*phi - e*phi - e + phi := by
    have hr : (0:ℝ) ≤ phi*((d + e*phi - 1)*(-b + 4*c*phi - 1)) := mul_nonneg hpos.le (mul_nonneg rde hf1)
    have he : phi*((d + e*phi - 1)*(-b + 4*c*phi - 1)) = -b*d*phi - b*e*phi - b*e + b*phi + 4*c*d*phi + 4*c*d + 8*c*e*phi + 4*c*e - 4*c*phi - 4*c - d*phi - e*phi - e + phi := by linear_combination (-b*e + 4*c*d + 4*c*e*phi + 4*c*e - 4*c - e)*hps
    linarith [hr, he]
  have E0 : a - 3*b*phi + c = 0 := by linear_combination (1)*hk0
  have E1 : a*phi - 3*b*phi - 3*b + c*phi = 0 := by linear_combination (phi)*hk0 + (3*b)*hps
  have E2 : a^2 - 3*a*b*phi + a*c = 0 := by linear_combination (a*1)*hk0
  have E3 : a^2*phi - 3*a*b*phi - 3*a*b + a*c*phi = 0 := by linear_combination (a*phi)*hk0 + (3*a*b)*hps
  have E4 : a*b - 3*b^2*phi + b*c = 0 := by linear_combination (b*1)*hk0
  have E5 : a*b*phi - 3*b^2*phi - 3*b^2 + b*c*phi = 0 := by linear_combination (b*phi)*hk0 + (3*b^2)*hps
  have E6 : a*c*phi - 3*b*c*phi - 3*b*c + c^2*phi = 0 := by linear_combination (c*phi)*hk0 + (3*b*c)*hps
  have E7 : a*e - 3*b*e*phi + c*e = 0 := by linear_combination (e*1)*hk0
  have E8 : a*e*phi - 3*b*e*phi - 3*b*e + c*e*phi = 0 := by linear_combination (e*phi)*hk0 + (3*b*e)*hps
  have E9 : b - 3*c*phi + d = 0 := by linear_combination (1)*hk1
  have E10 : b*phi - 3*c*phi - 3*c + d*phi = 0 := by linear_combination (phi)*hk1 + (3*c)*hps
  have E11 : a*b - 3*a*c*phi + a*d = 0 := by linear_combination (a*1)*hk1
  have E12 : a*b*phi - 3*a*c*phi - 3*a*c + a*d*phi = 0 := by linear_combination (a*phi)*hk1 + (3*a*c)*hps
  have E13 : b^2 - 3*b*c*phi + b*d = 0 := by linear_combination (b*1)*hk1
  have E14 : b*c - 3*c^2*phi + c*d = 0 := by linear_combination (c*1)*hk1
  have E15 : b*c*phi - 3*c^2*phi - 3*c^2 + c*d*phi = 0 := by linear_combination (c*phi)*hk1 + (3*c^2)*hps
  have E16 : b*d - 3*c*d*phi + d^2 = 0 := by linear_combination (d*1)*hk1
  have E17 : b*d*phi - 3*c*d*phi - 3*c*d + d^2*phi = 0 := by linear_combination (d*phi)*hk1 + (3*c*d)*hps
  have E18 : b*e - 3*c*e*phi + d*e = 0 := by linear_combination (e*1)*hk1
  have E19 : b*e*phi - 3*c*e*phi - 3*c*e + d*e*phi = 0 := by linear_combination (e*phi)*hk1 + (3*c*e)*hps
  have E20 : c - 3*d*phi + e = 0 := by linear_combination (1)*hk2
  have E21 : c*phi - 3*d*phi - 3*d + e*phi = 0 := by linear_combination (phi)*hk2 + (3*d)*hps
  have E22 : a*c - 3*a*d*phi + a*e = 0 := by linear_combination (a*1)*hk2
  have E23 : a*c*phi - 3*a*d*phi - 3*a*d + a*e*phi = 0 := by linear_combination (a*phi)*hk2 + (3*a*d)*hps
  have E24 : b*c - 3*b*d*phi + b*e = 0 := by linear_combination (b*1)*hk2
  have E25 : b*c*phi - 3*b*d*phi - 3*b*d + b*e*phi = 0 := by linear_combination (b*phi)*hk2 + (3*b*d)*hps
  have E26 : c*d - 3*d^2*phi + d*e = 0 := by linear_combination (d*1)*hk2
  have E27 : c*d*phi - 3*d^2*phi - 3*d^2 + d*e*phi = 0 := by linear_combination (d*phi)*hk2 + (3*d^2)*hps
  have E28 : c*e - 3*d*e*phi + e^2 = 0 := by linear_combination (e*1)*hk2
  have E29 : c*e*phi - 3*d*e*phi - 3*d*e + e^2*phi = 0 := by linear_combination (e*phi)*hk2 + (3*d*e)*hps
  linarith [q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, E0, E1, E2, E3, E4, E5, E6, E7, E8, E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20, E21, E22, E23, E24, E25, E26, E27, E28, E29, h2, h3]


/-- **q=5 genuine window-4 core.** Five coords of a genuine branch-4 scalar orbit cannot have
all four products `< 1/φ³`. Genuine domain ⟹ BOTH edges `c_n+φc_{n+1}>1` and `φc_n+c_{n+1}>1`. -/
theorem g5_core (a b c d e phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (ha : 0 < a) (hbp : 0 < b) (hc : 0 < c) (hd : 0 < d) (he2 : 0 < e)
    (ha1 : a ≤ 1) (hb1 : b ≤ 1) (hc1 : c ≤ 1) (hd1 : d ≤ 1) (he1 : e ≤ 1)
    (hab : a+phi*b > 1) (hbc : b+phi*c > 1) (hcd : c+phi*d > 1) (hde : d+phi*e > 1)
    (hab' : phi*a+b > 1) (hbc' : phi*b+c > 1) (hcd' : phi*c+d > 1) (hde' : phi*d+e > 1)
    (K0 K1 K2 : ℤ)
    (hk0 : a+c = (K0:ℝ)*phi*b) (hk1 : b+d = (K1:ℝ)*phi*c) (hk2 : c+e = (K2:ℝ)*phi*d)
    (hk0ge : 1 ≤ K0) (hk1ge : 1 ≤ K1) (hk2ge : 1 ≤ K2)
    (hk0f : 1+a < ((K0:ℝ)+1)*(phi*b)) (hk1f : 1+b < ((K1:ℝ)+1)*(phi*c))
    (hk2f : 1+c < ((K2:ℝ)+1)*(phi*d))
    (hP0 : a*b < 1/phi^3) (hP1 : b*c < 1/phi^3) (hP2 : c*d < 1/phi^3) (hP3 : d*e < 1/phi^3) :
    False := by
  have hpos : 0 < phi := by linarith
  have hp4 : phi^4 = 3*phi+2 := by nlinarith [hps]
  have hpc3 : (0:ℝ) < phi^3 := pow_pos hpos 3
  have hp4nn : (0:ℝ) ≤ phi^4 := by positivity
  have hP0c : a*b*phi^3 < 1 := (lt_div_iff₀ hpc3).mp hP0
  have hP1c : b*c*phi^3 < 1 := (lt_div_iff₀ hpc3).mp hP1
  have hP2c : c*d*phi^3 < 1 := (lt_div_iff₀ hpc3).mp hP2
  have hP3c : d*e*phi^3 < 1 := (lt_div_iff₀ hpc3).mp hP3
  have hK0r : (1:ℝ) ≤ (K0:ℝ) := by exact_mod_cast hk0ge
  have hK1r : (1:ℝ) ≤ (K1:ℝ) := by exact_mod_cast hk1ge
  have hK2r : (1:ℝ) ≤ (K2:ℝ) := by exact_mod_cast hk2ge
  have heng0 : a*b + b*c = (K0:ℝ)*phi*b^2 := by linear_combination b*hk0
  have heng1 : b*c + c*d = (K1:ℝ)*phi*c^2 := by linear_combination c*hk1
  have heng2 : c*d + d*e = (K2:ℝ)*phi*d^2 := by linear_combination d*hk2
  have hKb : (K0:ℝ)*phi^4*b^2 < 2 := by
    have h : (a*b+b*c)*phi^3 = (K0:ℝ)*phi^4*b^2 := by linear_combination phi^3*heng0
    nlinarith [hP0c, hP1c, h]
  have hKc : (K1:ℝ)*phi^4*c^2 < 2 := by
    have h : (b*c+c*d)*phi^3 = (K1:ℝ)*phi^4*c^2 := by linear_combination phi^3*heng1
    nlinarith [hP1c, hP2c, h]
  have hKd : (K2:ℝ)*phi^4*d^2 < 2 := by
    have h : (c*d+d*e)*phi^3 = (K2:ℝ)*phi^4*d^2 := by linear_combination phi^3*heng2
    nlinarith [hP2c, hP3c, h]
  have hbU2 : (3*phi+2)*b^2 < 2 := by
    have hn : (0:ℝ) ≤ phi^4*b^2 := mul_nonneg hp4nn (sq_nonneg b)
    have h : phi^4*b^2 < 2 := by nlinarith [hKb, hK0r, mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-1) hn]
    rwa [hp4] at h
  have hcU2 : (3*phi+2)*c^2 < 2 := by
    have hn : (0:ℝ) ≤ phi^4*c^2 := mul_nonneg hp4nn (sq_nonneg c)
    have h : phi^4*c^2 < 2 := by nlinarith [hKc, hK1r, mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-1) hn]
    rwa [hp4] at h
  have hdU2 : (3*phi+2)*d^2 < 2 := by
    have hn : (0:ℝ) ≤ phi^4*d^2 := mul_nonneg hp4nn (sq_nonneg d)
    have h : phi^4*d^2 < 2 := by nlinarith [hKd, hK2r, mul_nonneg (by linarith : (0:ℝ) ≤ (K2:ℝ)-1) hn]
    rwa [hp4] at h
  have hK0le : K0 ≤ 3 := by
    by_contra hcon; push_neg at hcon
    have h4 : (4:ℝ) ≤ (K0:ℝ) := by exact_mod_cast (by omega : (4:ℤ) ≤ K0)
    have hn : (0:ℝ) ≤ phi^4*b^2 := mul_nonneg hp4nn (sq_nonneg b)
    have hbb : (3*phi+2)*b^2 < 1/2 := by
      have h : phi^4*b^2 < 1/2 := by nlinarith [hKb, h4, mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-4) hn]
      rwa [hp4] at h
    exact g5_floor_helper phi b c hps h2 hbp hc hbb hcU2 (by linarith [hbc'])
  have hK1le : K1 ≤ 3 := by
    by_contra hcon; push_neg at hcon
    have h4 : (4:ℝ) ≤ (K1:ℝ) := by exact_mod_cast (by omega : (4:ℤ) ≤ K1)
    have hn : (0:ℝ) ≤ phi^4*c^2 := mul_nonneg hp4nn (sq_nonneg c)
    have hcc : (3*phi+2)*c^2 < 1/2 := by
      have h : phi^4*c^2 < 1/2 := by nlinarith [hKc, h4, mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-4) hn]
      rwa [hp4] at h
    exact g5_floor_helper phi c d hps h2 hc hd hcc hdU2 (by linarith [hcd'])
  have hK2le : K2 ≤ 3 := by
    by_contra hcon; push_neg at hcon
    have h4 : (4:ℝ) ≤ (K2:ℝ) := by exact_mod_cast (by omega : (4:ℤ) ≤ K2)
    have hn : (0:ℝ) ≤ phi^4*d^2 := mul_nonneg hp4nn (sq_nonneg d)
    have hdd : (3*phi+2)*d^2 < 1/2 := by
      have h : phi^4*d^2 < 1/2 := by nlinarith [hKd, h4, mul_nonneg (by linarith : (0:ℝ) ≤ (K2:ℝ)-4) hn]
      rwa [hp4] at h
    exact g5_floor_helper phi d c hps h2 hd hc hdd hcU2 (by linarith [hcd])
  interval_cases K0 <;> interval_cases K1 <;> interval_cases K2 <;>
    push_cast at hk0 hk1 hk2 hk0f hk1f hk2f <;>
    first
    | exact case111 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case112 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case113 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case121 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case122 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case123 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case131 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case132 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case133 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case211 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case212 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case213 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case221 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case222 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case223 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case231 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case232 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case233 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case311 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case312 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case313 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case321 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case322 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case323 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case331 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case332 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
    | exact case333 a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3
/-- **q=5 genuine window-4, orbit form.** Along any genuine branch-4 scalar orbit (both Taha
edges + cap), no four consecutive products are all `< 1/φ³`. Plugs into the verified
`essSup_ge_of_window4` engine ⟹ `X_Ω(5) ≥ 1/φ³`. -/
theorem g5_no_four_below_genuine
    (phi : ℝ) (hps : phi^2 = phi+1) (h2 : (1:ℝ) < phi) (h3 : phi < 2)
    (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n) (hcap : ∀ n, c n ≤ 1)
    (hreg : ∀ n, c n + phi * c (n+1) > 1) (hgen : ∀ n, phi * c n + c (n+1) > 1)
    (hrec : ∀ n, c n + c (n+2) = (⌊(1 + c n)/(phi*c (n+1))⌋ : ℝ)*phi*c (n+1)) :
    ∀ i, ¬ (c i * c (i+1) < 1/phi^3 ∧ c (i+1) * c (i+2) < 1/phi^3 ∧
            c (i+2) * c (i+3) < 1/phi^3 ∧ c (i+3) * c (i+4) < 1/phi^3) := by
  have hpos' : 0 < phi := by linarith
  intro i hcon
  obtain ⟨h0, h1, h2', h3'⟩ := hcon
  have flr : ∀ n, (1:ℤ) ≤ ⌊(1 + c n)/(phi*c (n+1))⌋ := by
    intro n
    have hden : 0 < phi*c (n+1) := mul_pos hpos' (hpos (n+1))
    have hsum : 0 < (⌊(1 + c n)/(phi*c (n+1))⌋ : ℝ)*phi*c (n+1) := by
      rw [← hrec n]; linarith [hpos n, hpos (n+2)]
    have h0' : (0:ℝ) < (⌊(1 + c n)/(phi*c (n+1))⌋ : ℝ) := by nlinarith [hsum, hden]
    have : (0:ℤ) < ⌊(1 + c n)/(phi*c (n+1))⌋ := by exact_mod_cast h0'
    omega
  have flrUB : ∀ n, 1 + c n < ((⌊(1 + c n)/(phi*c (n+1))⌋ : ℝ)+1)*(phi*c (n+1)) := by
    intro n
    have hden : 0 < phi*c (n+1) := mul_pos hpos' (hpos (n+1))
    have := Int.lt_floor_add_one ((1 + c n)/(phi*c (n+1)))
    rw [div_lt_iff₀ hden] at this
    linarith [this]
  exact g5_core (c i) (c (i+1)) (c (i+2)) (c (i+3)) (c (i+4)) phi hps h2 h3
    (hpos i) (hpos (i+1)) (hpos (i+2)) (hpos (i+3)) (hpos (i+4))
    (hcap i) (hcap (i+1)) (hcap (i+2)) (hcap (i+3)) (hcap (i+4))
    (hreg i) (hreg (i+1)) (hreg (i+2)) (hreg (i+3))
    (hgen i) (hgen (i+1)) (hgen (i+2)) (hgen (i+3))
    (⌊(1 + c i)/(phi*c (i+1))⌋) (⌊(1 + c (i+1))/(phi*c (i+2))⌋) (⌊(1 + c (i+2))/(phi*c (i+3))⌋)
    (hrec i) (hrec (i+1)) (hrec (i+2)) (flr i) (flr (i+1)) (flr (i+2))
    (flrUB i) (flrUB (i+1)) (flrUB (i+2)) h0 h1 h2' h3'
