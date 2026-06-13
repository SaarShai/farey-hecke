import Mathlib
set_option maxHeartbeats 1600000
noncomputable section
open Int

/-- `9/5 < lam_7` via synthetic division of the minpoly by `(t-9/5)`. -/
lemma g7_lam_lo (lam : ℝ) (hps : lam^3 = lam^2 + 2*lam - 1) (h2 : (1:ℝ) < lam) (h3 : lam < 2) :
    (9:ℝ)/5 < lam := by
  have hg : (0:ℝ) < lam^2 + 4*lam/5 - 14/25 := by nlinarith [h2, h3, sq_nonneg (lam-1), sq_nonneg (lam-2), sq_nonneg lam, pow_pos (show (0:ℝ)<lam by linarith) 3, pow_pos (show (0:ℝ)<lam by linarith) 5, pow_pos (show (0:ℝ)<lam by linarith) 7]
  have key : (lam - 9/5) * (lam^2 + 4*lam/5 - 14/25) = 1/125 := by linear_combination hps
  nlinarith [key, hg]

/-- Interior-floor contradiction (K>=2 impossible inside a sub-threshold window): if a
middle coord `m` has `lam^4 m^2 < 1` (= the K>=2 bound) and a neighbour `n` with `lam^4 n^2
< 2` and edge `1 - lam m < n`, then False.  Uses only `9/5 < lam < 2` via `(lam^2-lam)^2
>= 2` — field-independent. -/
lemma g7_floor_helper (lam m n : ℝ) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hlo : (9:ℝ)/5 < lam) (hm : 0 < m) (hn : 0 < n)
    (hms : lam^4 * m^2 < 1) (hns : lam^4 * n^2 < 2) (hedge : 1 - lam*m < n) : False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hl2 : (1:ℝ) < lam^2 := by nlinarith [h2]
  have hlm : lam^2 * m < 1 := by nlinarith [hms, mul_pos (mul_pos hpos hpos) hm, sq_nonneg (lam^2*m)]
  have hlm1 : lam*m < 1 := by nlinarith [hlm, hl2, hm, mul_pos hpos hm]
  have h1lm : (0:ℝ) < 1 - lam*m := by linarith
  have hnsq : (1 - lam*m)^2 < n^2 := by nlinarith [hedge, h1lm, hn]
  have hml : (36:ℝ)/25 ≤ lam^2 - lam := by nlinarith [mul_pos (show (0:ℝ)<lam-9/5 by linarith) (show (0:ℝ)<lam+4/5 by linarith)]
  have hKey : (2:ℝ) ≤ lam^4 - 2*lam^3 + lam^2 := by nlinarith [hml, sq_nonneg (lam^2-lam), mul_pos hpos (show (0:ℝ)<lam-1 by linarith)]
  have hA : lam^4 * (1 - lam*m)^2 < 2 := by nlinarith [hnsq, hns, mul_pos (mul_pos (mul_pos hpos hpos) hpos) hpos]
  nlinarith [hA, hKey, h1lm, hlm, hpos, hl2, mul_pos hpos h1lm, sq_nonneg (lam - lam^2*m), sq_nonneg (lam*(1-lam*m))]

lemma case_q7 (a b c d e lam : ℝ) (hps : lam^3 = lam^2 + 2*lam - 1) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hpa : 0 < a) (hpb : 0 < b) (hpc : 0 < c) (hpd : 0 < d) (hpe : 0 < e)
    (hca : a ≤ 1) (hcb : b ≤ 1) (hcc : c ≤ 1) (hcd : d ≤ 1) (hce : e ≤ 1)
    (hr0 : a+lam*b > 1) (hr1 : b+lam*c > 1) (hr2 : c+lam*d > 1) (hr3 : d+lam*e > 1)
    (hg0 : lam*a+b > 1) (hg1 : lam*b+c > 1) (hg2 : lam*c+d > 1) (hg3 : lam*d+e > 1)
    (hk0 : a+c = 1*lam*b) (hk1 : b+d = 1*lam*c) (hk2 : c+e = 1*lam*d)
    (hf0 : 1+a < (1+1)*(lam*b)) (hf1 : 1+b < (1+1)*(lam*c)) (hf2 : 1+c < (1+1)*(lam*d))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) (hP3 : d*e < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have pos0 : (0:ℝ) ≤ a := le_of_lt hpa
  have pos1 : (0:ℝ) ≤ b := le_of_lt hpb
  have pos2 : (0:ℝ) ≤ c := le_of_lt hpc
  have pos3 : (0:ℝ) ≤ d := le_of_lt hpd
  have pos4 : (0:ℝ) ≤ e := le_of_lt hpe
  have cap0 : (0:ℝ) ≤ 1 - a := by nlinarith [hca]
  have cap1 : (0:ℝ) ≤ 1 - b := by nlinarith [hcb]
  have cap2 : (0:ℝ) ≤ 1 - c := by nlinarith [hcc]
  have cap3 : (0:ℝ) ≤ 1 - d := by nlinarith [hcd]
  have cap4 : (0:ℝ) ≤ 1 - e := by nlinarith [hce]
  have reg0 : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hr0]
  have reg1 : (0:ℝ) ≤ b + c*lam - 1 := by nlinarith [hr1]
  have reg2 : (0:ℝ) ≤ c + d*lam - 1 := by nlinarith [hr2]
  have reg3 : (0:ℝ) ≤ d + e*lam - 1 := by nlinarith [hr3]
  have gen0 : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hg0]
  have gen1 : (0:ℝ) ≤ b*lam + c - 1 := by nlinarith [hg1]
  have gen2 : (0:ℝ) ≤ c*lam + d - 1 := by nlinarith [hg2]
  have gen3 : (0:ℝ) ≤ d*lam + e - 1 := by nlinarith [hg3]
  have slk0 : (0:ℝ) ≤ -a*b*lam^3 + 1 := by
    have hh : (a*b)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
    nlinarith [hh]
  have slk1 : (0:ℝ) ≤ -b*c*lam^3 + 1 := by
    have hh : (b*c)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP1
    nlinarith [hh]
  have slk2 : (0:ℝ) ≤ -c*d*lam^3 + 1 := by
    have hh : (c*d)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
    nlinarith [hh]
  have slk3 : (0:ℝ) ≤ -d*e*lam^3 + 1 := by
    have hh : (d*e)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP3
    nlinarith [hh]
  have flu0 : (0:ℝ) ≤ -a + 2*b*lam - 1 := by nlinarith [hf0]
  have flu1 : (0:ℝ) ≤ -b + 2*c*lam - 1 := by nlinarith [hf1]
  have flu2 : (0:ℝ) ≤ -c + 2*d*lam - 1 := by nlinarith [hf2]
  have qq0 : (0:ℝ) ≤ -4*a^2*b*lam^2 - 5*a^2*b*lam + 3*a^2*b + 15*a*b^2*lam^2 + 9*a*b^2*lam - 7*a*b^2 - 10*b^3*lam^2 - 9*b^3*lam + 6*b^3 + b*lam := by
    have hr : (0:ℝ) ≤ lam*((b)*(-c*d*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg pos1 slk2)
    have he : lam*((b)*(-c*d*lam^3 + 1)) = -4*a^2*b*lam^2 - 5*a^2*b*lam + 3*a^2*b + 15*a*b^2*lam^2 + 9*a*b^2*lam - 7*a*b^2 - 10*b^3*lam^2 - 9*b^3*lam + 6*b^3 + b*lam := by linear_combination (a*b*lam^5 - b^2*lam^6 - b*d*lam^4)*hk0 + (a*b*lam^4 - b^2*lam^5)*hk1 + (-a^2*b*lam^2 - a^2*b*lam - 3*a^2*b + 2*a*b^2*lam^3 + 2*a*b^2*lam^2 + 5*a*b^2*lam + 7*a*b^2 - b^3*lam^4 - b^3*lam^3 - 2*b^3*lam^2 - 3*b^3*lam - 6*b^3)*hps
    linarith [hr, he]
  have qq1 : (0:ℝ) ≤ 3*a^2*lam^2 + a^2*lam - a^2 - 3*a*b*lam^2 - 2*a*b*lam + 2*a*b - 3*a*lam^2 + a + 3*b*lam^2 + 2*b*lam - 2*b - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(d + e*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap0 reg3)
    have he : lam*((1 - a)*(d + e*lam - 1)) = 3*a^2*lam^2 + a^2*lam - a^2 - 3*a*b*lam^2 - 2*a*b*lam + 2*a*b - 3*a*lam^2 + a + 3*b*lam^2 + 2*b*lam - 2*b - lam := by linear_combination (-a*lam^4 + lam^4)*hk0 + (-a*lam^3 - a*lam + lam^3 + lam)*hk1 + (-a*lam^2 + lam^2)*hk2 + (a^2*lam + a^2 - a*b*lam^2 - a*b*lam - 2*a*b - a*lam - a + b*lam^2 + b*lam + 2*b)*hps
    linarith [hr, he]
  have qq2 : (0:ℝ) ≤ -a^2*lam^2 - a*b*lam + a*lam^2 + a*lam + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap0 gen0)
    have he : lam*((1 - a)*(a*lam + b - 1)) = -a^2*lam^2 - a*b*lam + a*lam^2 + a*lam + b*lam - lam := by linear_combination 0
    linarith [hr, he]
  have qq3 : (0:ℝ) ≤ -3*a^2*b*lam^2 - a^2*b*lam + a^2*b + 4*a*b^2*lam^2 + 5*a*b^2*lam - 3*a*b^2 + 3*a*b*lam^2 + a*b*lam - a*b - a*lam - 4*b^2*lam^2 - 5*b^2*lam + 3*b^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(-b*c*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap0 slk1)
    have he : lam*((1 - a)*(-b*c*lam^3 + 1)) = -3*a^2*b*lam^2 - a^2*b*lam + a^2*b + 4*a*b^2*lam^2 + 5*a*b^2*lam - 3*a*b^2 + 3*a*b*lam^2 + a*b*lam - a*b - a*lam - 4*b^2*lam^2 - 5*b^2*lam + 3*b^2 + lam := by linear_combination (a*b*lam^4 - b*lam^4)*hk0 + (-a^2*b*lam - a^2*b + a*b^2*lam^2 + a*b^2*lam + 3*a*b^2 + a*b*lam + a*b - b^2*lam^2 - b^2*lam - 3*b^2)*hps
    linarith [hr, he]
  have qq4 : (0:ℝ) ≤ 4*a^3*lam^2 + 5*a^3*lam - 3*a^3 - 15*a^2*b*lam^2 - 9*a^2*b*lam + 7*a^2*b - 4*a^2*lam^2 - 5*a^2*lam + 3*a^2 + 10*a*b^2*lam^2 + 9*a*b^2*lam - 6*a*b^2 + 15*a*b*lam^2 + 9*a*b*lam - 7*a*b - a*lam - 10*b^2*lam^2 - 9*b^2*lam + 6*b^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(-c*d*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap0 slk2)
    have he : lam*((1 - a)*(-c*d*lam^3 + 1)) = 4*a^3*lam^2 + 5*a^3*lam - 3*a^3 - 15*a^2*b*lam^2 - 9*a^2*b*lam + 7*a^2*b - 4*a^2*lam^2 - 5*a^2*lam + 3*a^2 + 10*a*b^2*lam^2 + 9*a*b^2*lam - 6*a*b^2 + 15*a*b*lam^2 + 9*a*b*lam - 7*a*b - a*lam - 10*b^2*lam^2 - 9*b^2*lam + 6*b^2 + lam := by linear_combination (-a^2*lam^5 + a*b*lam^6 + a*d*lam^4 + a*lam^5 - b*lam^6 - d*lam^4)*hk0 + (-a^2*lam^4 + a*b*lam^5 + a*lam^4 - b*lam^5)*hk1 + (a^3*lam^2 + a^3*lam + 3*a^3 - 2*a^2*b*lam^3 - 2*a^2*b*lam^2 - 5*a^2*b*lam - 7*a^2*b - a^2*lam^2 - a^2*lam - 3*a^2 + a*b^2*lam^4 + a*b^2*lam^3 + 2*a*b^2*lam^2 + 3*a*b^2*lam + 6*a*b^2 + 2*a*b*lam^3 + 2*a*b*lam^2 + 5*a*b*lam + 7*a*b - b^2*lam^4 - b^2*lam^3 - 2*b^2*lam^2 - 3*b^2*lam - 6*b^2)*hps
    linarith [hr, he]
  have qq5 : (0:ℝ) ≤ -a^2*lam^2 - 2*a^2*lam + a^2 + 5*a*b*lam^2 + 2*a*b*lam - 3*a*b - a*lam^2 - 2*a*lam - 3*b^2*lam^2 - 2*b^2*lam + 2*b^2 + 2*b*lam^2 + 2*b*lam - 2*b - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(d + e*lam - 1) := mul_nonneg cap2 reg3
    have he : (1 - c)*(d + e*lam - 1) = -a^2*lam^2 - 2*a^2*lam + a^2 + 5*a*b*lam^2 + 2*a*b*lam - 3*a*b - a*lam^2 - 2*a*lam - 3*b^2*lam^2 - 2*b^2*lam + 2*b^2 + 2*b*lam^2 + 2*b*lam - 2*b - 1 := by linear_combination (a*lam^3 - b*lam^4 - d - e*lam + lam^3 + 1)*hk0 + (a*lam^2 + a - b*lam^3 - b*lam + lam^2 + 1)*hk1 + (a*lam - b*lam^2 + lam)*hk2 + (-a^2 + 2*a*b*lam + 2*a*b - a - b^2*lam^2 - b^2*lam - 2*b^2 + b*lam + b)*hps
    linarith [hr, he]
  have qq6 : (0:ℝ) ≤ -3*a^2*lam^2 - a^2*lam + a^2 + 7*a*b*lam^2 + 7*a*b*lam - 5*a*b - 3*a*lam^2 - 2*a*lam + a - 5*b^2*lam^2 - 4*b^2*lam + 3*b^2 + 4*b*lam^2 + 2*b*lam - 2*b - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(d + e*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap2 reg3)
    have he : lam*((1 - c)*(d + e*lam - 1)) = -3*a^2*lam^2 - a^2*lam + a^2 + 7*a*b*lam^2 + 7*a*b*lam - 5*a*b - 3*a*lam^2 - 2*a*lam + a - 5*b^2*lam^2 - 4*b^2*lam + 3*b^2 + 4*b*lam^2 + 2*b*lam - 2*b - lam := by linear_combination (a*lam^4 - b*lam^5 - d*lam - e*lam^2 + lam^4 + lam)*hk0 + (a*lam^3 + a*lam - b*lam^4 - b*lam^2 + lam^3 + lam)*hk1 + (a*lam^2 - b*lam^3 + lam^2)*hk2 + (-a^2*lam - a^2 + 2*a*b*lam^2 + 2*a*b*lam + 5*a*b - a*lam - a - b^2*lam^3 - b^2*lam^2 - 2*b^2*lam - 3*b^2 + b*lam^2 + b*lam + 2*b)*hps
    linarith [hr, he]
  have qq7 : (0:ℝ) ≤ a^2*lam - a*b*lam^2 + a*b + a*lam - a - b^2*lam + b*lam + b - 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(a*lam + b - 1) := mul_nonneg cap2 gen0
    have he : (1 - c)*(a*lam + b - 1) = a^2*lam - a*b*lam^2 + a*b + a*lam - a - b^2*lam + b*lam + b - 1 := by linear_combination (-a*lam - b + 1)*hk0
    linarith [hr, he]
  have qq8 : (0:ℝ) ≤ a^2*lam^2 - a*b*lam^2 - a*b*lam + a*b + a*lam^2 - a*lam - b^2*lam^2 + b*lam^2 + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap2 gen0)
    have he : lam*((1 - c)*(a*lam + b - 1)) = a^2*lam^2 - a*b*lam^2 - a*b*lam + a*b + a*lam^2 - a*lam - b^2*lam^2 + b*lam^2 + b*lam - lam := by linear_combination (-a*lam^2 - b*lam + lam)*hk0 + (-a*b)*hps
    linarith [hr, he]
  have qq9 : (0:ℝ) ≤ a^2*b*lam^2 + 2*a^2*b*lam - a^2*b - 6*a*b^2*lam^2 - 2*a*b^2*lam + 2*a*b^2 + a*b*lam^2 + 2*a*b*lam - a*b + a + 4*b^3*lam^2 + 5*b^3*lam - 3*b^3 - 3*b^2*lam^2 - b^2*lam + b^2 - b*lam + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-b*c*lam^3 + 1) := mul_nonneg cap2 slk1
    have he : (1 - c)*(-b*c*lam^3 + 1) = a^2*b*lam^2 + 2*a^2*b*lam - a^2*b - 6*a*b^2*lam^2 - 2*a*b^2*lam + 2*a*b^2 + a*b*lam^2 + 2*a*b*lam - a*b + a + 4*b^3*lam^2 + 5*b^3*lam - 3*b^3 - 3*b^2*lam^2 - b^2*lam + b^2 - b*lam + 1 := by linear_combination (-a*b*lam^3 + b^2*lam^4 + b*c*lam^3 - b*lam^3 - 1)*hk0 + (a^2*b - 2*a*b^2*lam - 2*a*b^2 + a*b + b^3*lam^2 + b^3*lam + 3*b^3 - b^2*lam - b^2)*hps
    linarith [hr, he]
  have qq10 : (0:ℝ) ≤ 3*a^2*b*lam^2 + a^2*b*lam - a^2*b - 8*a*b^2*lam^2 - 10*a*b^2*lam + 6*a*b^2 + 3*a*b*lam^2 + a*b*lam - a*b + a*lam + 9*b^3*lam^2 + 5*b^3*lam - 4*b^3 - 4*b^2*lam^2 - 5*b^2*lam + 3*b^2 - b*lam^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(-b*c*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap2 slk1)
    have he : lam*((1 - c)*(-b*c*lam^3 + 1)) = 3*a^2*b*lam^2 + a^2*b*lam - a^2*b - 8*a*b^2*lam^2 - 10*a*b^2*lam + 6*a*b^2 + 3*a*b*lam^2 + a*b*lam - a*b + a*lam + 9*b^3*lam^2 + 5*b^3*lam - 4*b^3 - 4*b^2*lam^2 - 5*b^2*lam + 3*b^2 - b*lam^2 + lam := by linear_combination (-a*b*lam^4 + b^2*lam^5 + b*c*lam^4 - b*lam^4 - lam)*hk0 + (a^2*b*lam + a^2*b - 2*a*b^2*lam^2 - 2*a*b^2*lam - 6*a*b^2 + a*b*lam + a*b + b^3*lam^3 + b^3*lam^2 + 3*b^3*lam + 4*b^3 - b^2*lam^2 - b^2*lam - 3*b^2)*hps
    linarith [hr, he]
  have qq11 : (0:ℝ) ≤ -6*a^2*lam^2 - 4*a^2*lam + 3*a^2 + 12*a*b*lam^2 + 9*a*b*lam - 6*a*b - 4*a*lam^2 - 2*a*lam + 2*a - 6*b^2*lam^2 - 5*b^2*lam + 3*b^2 + 4*b*lam^2 + 3*b*lam - 3*b - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - e)*(d + e*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap4 reg3)
    have he : lam*((1 - e)*(d + e*lam - 1)) = -6*a^2*lam^2 - 4*a^2*lam + 3*a^2 + 12*a*b*lam^2 + 9*a*b*lam - 6*a*b - 4*a*lam^2 - 2*a*lam + 2*a - 6*b^2*lam^2 - 5*b^2*lam + 3*b^2 + 4*b*lam^2 + 3*b*lam - 3*b - lam := by linear_combination (a*lam^6 - a*lam^4 - b*lam^7 + 2*b*lam^5 - b*lam - e*lam^4 + lam^4 + lam^3 - lam)*hk0 + (a*lam^5 - b*lam^6 + b*lam^4 + b*lam^2 - e*lam^3 - e*lam + lam^3 + lam^2 + lam)*hk1 + (a*lam^4 - b*lam^5 + b*lam^3 + b*lam - e*lam^2 + lam^2 + lam)*hk2 + (-a^2*lam^3 - a^2*lam^2 - 2*a^2*lam - 3*a^2 + 2*a*b*lam^4 + 2*a*b*lam^3 + 2*a*b*lam^2 + 4*a*b*lam + 6*a*b - a*lam - 2*a - b^2*lam^5 - b^2*lam^4 - b^2*lam^2 - b^2*lam - 3*b^2 + b*lam^2 + 2*b*lam + 3*b)*hps
    linarith [hr, he]
  have qq12 : (0:ℝ) ≤ 2*a^2*lam^2 + a^2*lam - a^2 - a*b*lam^2 - a*lam + a - b^2*lam^2 - b^2*lam + b^2 + b*lam^2 + 2*b*lam - b - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - e)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap4 gen0)
    have he : lam*((1 - e)*(a*lam + b - 1)) = 2*a^2*lam^2 + a^2*lam - a^2 - a*b*lam^2 - a*lam + a - b^2*lam^2 - b^2*lam + b^2 + b*lam^2 + 2*b*lam - b - lam := by linear_combination (-a*lam^4 + a*lam^2 - b*lam^3 + b*lam + lam^3 - lam)*hk0 + (-a*lam^3 - b*lam^2 + lam^2)*hk1 + (-a*lam^2 - b*lam + lam)*hk2 + (a^2*lam + a^2 - a*b*lam^2 - a*b*lam - a - b^2*lam - b^2 + b*lam + b)*hps
    linarith [hr, he]
  have qq13 : (0:ℝ) ≤ 6*a^2*b*lam^2 + 4*a^2*b*lam - 3*a^2*b - 16*a*b^2*lam^2 - 13*a*b^2*lam + 9*a*b^2 + 3*a*b*lam^2 + a*b*lam - a*b + a*lam^2 + a*lam - a + 10*b^3*lam^2 + 9*b^3*lam - 6*b^3 - 4*b^2*lam^2 - 5*b^2*lam + 3*b^2 - b*lam^2 - b*lam + b + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - e)*(-b*c*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap4 slk1)
    have he : lam*((1 - e)*(-b*c*lam^3 + 1)) = 6*a^2*b*lam^2 + 4*a^2*b*lam - 3*a^2*b - 16*a*b^2*lam^2 - 13*a*b^2*lam + 9*a*b^2 + 3*a*b*lam^2 + a*b*lam - a*b + a*lam^2 + a*lam - a + 10*b^3*lam^2 + 9*b^3*lam - 6*b^3 - 4*b^2*lam^2 - 5*b^2*lam + 3*b^2 - b*lam^2 - b*lam + b + lam := by linear_combination (-a*b*lam^6 + a*b*lam^4 + b^2*lam^7 - b^2*lam^5 + b*e*lam^4 - b*lam^4 - lam^3 + lam)*hk0 + (-a*b*lam^5 + b^2*lam^6 - lam^2)*hk1 + (-a*b*lam^4 + b^2*lam^5 - lam)*hk2 + (a^2*b*lam^3 + a^2*b*lam^2 + 2*a^2*b*lam + 3*a^2*b - 2*a*b^2*lam^4 - 2*a*b^2*lam^3 - 3*a*b^2*lam^2 - 5*a*b^2*lam - 9*a*b^2 + a*b*lam + a*b + a + b^3*lam^5 + b^3*lam^4 + b^3*lam^3 + 2*b^3*lam^2 + 3*b^3*lam + 6*b^3 - b^2*lam^2 - b^2*lam - 3*b^2 - b*lam - b)*hps
    linarith [hr, he]
  have qq14 : (0:ℝ) ≤ -10*a^3*lam^2 - 9*a^3*lam + 6*a^3 + 42*a^2*b*lam^2 + 33*a^2*b*lam - 23*a^2*b - 4*a^2*lam^2 - 5*a^2*lam + 3*a^2 - 55*a*b^2*lam^2 - 43*a*b^2*lam + 30*a*b^2 + 15*a*b*lam^2 + 9*a*b*lam - 7*a*b + a*lam^2 + a*lam - a + 23*b^3*lam^2 + 19*b^3*lam - 13*b^3 - 10*b^2*lam^2 - 9*b^2*lam + 6*b^2 - b*lam^2 - b*lam + b + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - e)*(-c*d*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap4 slk2)
    have he : lam*((1 - e)*(-c*d*lam^3 + 1)) = -10*a^3*lam^2 - 9*a^3*lam + 6*a^3 + 42*a^2*b*lam^2 + 33*a^2*b*lam - 23*a^2*b - 4*a^2*lam^2 - 5*a^2*lam + 3*a^2 - 55*a*b^2*lam^2 - 43*a*b^2*lam + 30*a*b^2 + 15*a*b*lam^2 + 9*a*b*lam - 7*a*b + a*lam^2 + a*lam - a + 23*b^3*lam^2 + 19*b^3*lam - 13*b^3 - 10*b^2*lam^2 - 9*b^2*lam + 6*b^2 - b*lam^2 - b*lam + b + lam := by linear_combination (a^2*lam^7 - a^2*lam^5 - 2*a*b*lam^8 + 3*a*b*lam^6 - a*b*lam^4 - a*e*lam^5 + a*lam^5 + b^2*lam^9 - 2*b^2*lam^7 + b^2*lam^5 + b*e*lam^6 - b*lam^6 + d*e*lam^4 - d*lam^4 - lam^3 + lam)*hk0 + (a^2*lam^6 - 2*a*b*lam^7 + a*b*lam^5 - a*e*lam^4 + a*lam^4 + b^2*lam^8 - b^2*lam^6 + b*e*lam^5 - b*lam^5 - lam^2)*hk1 + (a^2*lam^5 - 2*a*b*lam^6 + a*b*lam^4 + b^2*lam^7 - b^2*lam^5 - lam)*hk2 + (-a^3*lam^4 - a^3*lam^3 - 2*a^3*lam^2 - 3*a^3*lam - 6*a^3 + 3*a^2*b*lam^5 + 3*a^2*b*lam^4 + 4*a^2*b*lam^3 + 7*a^2*b*lam^2 + 13*a^2*b*lam + 23*a^2*b - a^2*lam^2 - a^2*lam - 3*a^2 - 3*a*b^2*lam^6 - 3*a*b^2*lam^5 - 2*a*b^2*lam^4 - 5*a*b^2*lam^3 - 9*a*b^2*lam^2 - 17*a*b^2*lam - 30*a*b^2 + 2*a*b*lam^3 + 2*a*b*lam^2 + 5*a*b*lam + 7*a*b + a + b^3*lam^7 + b^3*lam^6 + b^3*lam^4 + 2*b^3*lam^3 + 4*b^3*lam^2 + 7*b^3*lam + 13*b^3 - b^2*lam^4 - b^2*lam^3 - 2*b^2*lam^2 - 3*b^2*lam - 6*b^2 - b*lam - b)*hps
    linarith [hr, he]
  have qq15 : (0:ℝ) ≤ a^2*lam + 2*a*b*lam^2 - 2*a*lam + b^2*lam^2 + 2*b^2*lam - b^2 - 2*b*lam^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((a + b*lam - 1)*(a + b*lam - 1)) := mul_nonneg hpos.le (mul_nonneg reg0 reg0)
    have he : lam*((a + b*lam - 1)*(a + b*lam - 1)) = a^2*lam + 2*a*b*lam^2 - 2*a*lam + b^2*lam^2 + 2*b^2*lam - b^2 - 2*b*lam^2 + lam := by linear_combination (b^2)*hps
    linarith [hr, he]
  have qq16 : (0:ℝ) ≤ -2*a^2*lam^2 - 3*a^2*lam + 2*a^2 - 2*a*b*lam^2 + 2*a*lam^2 + 2*a*lam - 2*a + 5*b^2*lam^2 + 4*b^2*lam - 3*b^2 - 4*b*lam^2 - 2*b*lam + 2*b + lam := by
    have hr : (0:ℝ) ≤ lam*((a + b*lam - 1)*(d*lam + e - 1)) := mul_nonneg hpos.le (mul_nonneg reg0 gen3)
    have he : lam*((a + b*lam - 1)*(d*lam + e - 1)) = -2*a^2*lam^2 - 3*a^2*lam + 2*a^2 - 2*a*b*lam^2 + 2*a*lam^2 + 2*a*lam - 2*a + 5*b^2*lam^2 + 4*b^2*lam - 3*b^2 - 4*b*lam^2 - 2*b*lam + 2*b + lam := by linear_combination (2*a*lam^3 - a*lam + 2*b*lam^4 - b*lam^2 - 2*lam^3 + lam)*hk0 + (2*a*lam^2 + 2*b*lam^3 - 2*lam^2)*hk1 + (a*lam + b*lam^2 - lam)*hk2 + (-2*a^2 + 2*a + 2*b^2*lam^2 + 2*b^2*lam + 3*b^2 - 2*b*lam - 2*b)*hps
    linarith [hr, he]
  have qq17 : (0:ℝ) ≤ 4*a^2*lam^2 + 5*a^2*lam - 3*a^2 - 17*a*b*lam^2 - 10*a*b*lam + 8*a*b + 4*a*lam^2 + a*lam - a + 12*b^2*lam^2 + 9*b^2*lam - 7*b^2 - 4*b*lam^2 - 5*b*lam + 3*b + lam := by
    have hr : (0:ℝ) ≤ lam*((b + c*lam - 1)*(d + e*lam - 1)) := mul_nonneg hpos.le (mul_nonneg reg1 reg3)
    have he : lam*((b + c*lam - 1)*(d + e*lam - 1)) = 4*a^2*lam^2 + 5*a^2*lam - 3*a^2 - 17*a*b*lam^2 - 10*a*b*lam + 8*a*b + 4*a*lam^2 + a*lam - a + 12*b^2*lam^2 + 9*b^2*lam - 7*b^2 - 4*b*lam^2 - 5*b*lam + 3*b + lam := by linear_combination (-a*lam^5 + b*lam^6 + b*lam^4 + d*lam^2 + e*lam^3 - lam^4 - lam^2)*hk0 + (-a*lam^4 - a*lam^2 + b*lam^5 + 2*b*lam^3 + b*lam - lam^3 - lam)*hk1 + (-a*lam^3 + b*lam^4 + b*lam^2 - lam^2)*hk2 + (a^2*lam^2 + a^2*lam + 3*a^2 - 2*a*b*lam^3 - 2*a*b*lam^2 - 6*a*b*lam - 8*a*b + a*lam + a + b^2*lam^4 + b^2*lam^3 + 3*b^2*lam^2 + 4*b^2*lam + 7*b^2 - b*lam^2 - b*lam - 3*b)*hps
    linarith [hr, he]
  have qq18 : (0:ℝ) ≤ -a^2*lam^2 - 2*a^2*lam + a^2 + 3*a*b*lam^2 + a*b*lam - a*b + b^2*lam^2 + 3*b^2*lam - b^2 - b*lam^2 - 4*b*lam + b + lam := by
    have hr : (0:ℝ) ≤ lam*((b + c*lam - 1)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg reg1 gen0)
    have he : lam*((b + c*lam - 1)*(a*lam + b - 1)) = -a^2*lam^2 - 2*a^2*lam + a^2 + 3*a*b*lam^2 + a*b*lam - a*b + b^2*lam^2 + 3*b^2*lam - b^2 - b*lam^2 - 4*b*lam + b + lam := by linear_combination (a*lam^3 + b*lam^2 - lam^2)*hk0 + (-a^2 + a*b*lam + a*b + b^2 - b)*hps
    linarith [hr, he]
  have qq19 : (0:ℝ) ≤ 5*a^2*b*lam^2 + 7*a^2*b*lam - 4*a^2*b - 9*a*b^2*lam^2 - 5*a*b^2*lam + 4*a*b^2 + a*b*lam^2 + 2*a*b*lam - a*b - a*lam^2 - a + b*lam^2 + 2*b*lam - b - 1 := by
    have hr : (0:ℝ) ≤ (c + d*lam - 1)*(-a*b*lam^3 + 1) := mul_nonneg reg2 slk0
    have he : (c + d*lam - 1)*(-a*b*lam^3 + 1) = 5*a^2*b*lam^2 + 7*a^2*b*lam - 4*a^2*b - 9*a*b^2*lam^2 - 5*a*b^2*lam + 4*a*b^2 + a*b*lam^2 + 2*a*b*lam - a*b - a*lam^2 - a + b*lam^2 + 2*b*lam - b - 1 := by linear_combination (-a*b*lam^5 - a*b*lam^3 + lam^2 + 1)*hk0 + (-a*b*lam^4 + lam)*hk1 + (a^2*b*lam^2 + a^2*b*lam + 4*a^2*b - a*b^2*lam^3 - a*b^2*lam^2 - 3*a*b^2*lam - 4*a*b^2 + a*b + b)*hps
    linarith [hr, he]
  have qq20 : (0:ℝ) ≤ 8*a^2*lam^2 + 10*a^2*lam - 6*a^2 - 25*a*b*lam^2 - 17*a*b*lam + 13*a*b + 5*a*lam^2 + a*lam - a + 15*b^2*lam^2 + 12*b^2*lam - 8*b^2 - 5*b*lam^2 - 5*b*lam + 4*b + lam := by
    have hr : (0:ℝ) ≤ lam*((d + e*lam - 1)*(c*lam + d - 1)) := mul_nonneg hpos.le (mul_nonneg reg3 gen2)
    have he : lam*((d + e*lam - 1)*(c*lam + d - 1)) = 8*a^2*lam^2 + 10*a^2*lam - 6*a^2 - 25*a*b*lam^2 - 17*a*b*lam + 13*a*b + 5*a*lam^2 + a*lam - a + 15*b^2*lam^2 + 12*b^2*lam - 8*b^2 - 5*b*lam^2 - 5*b*lam + 4*b + lam := by linear_combination (-2*a*lam^5 + 2*b*lam^6 - b*lam^4 + 2*d*lam^2 + 2*e*lam^3 - lam^4 - 2*lam^2)*hk0 + (-2*a*lam^4 - 2*a*lam^2 + 2*b*lam^5 + b*lam^3 - b*lam + d*lam + e*lam^2 - lam^3 - 2*lam)*hk1 + (-2*a*lam^3 + 2*b*lam^4 - b*lam^2 - lam^2)*hk2 + (2*a^2*lam^2 + 2*a^2*lam + 6*a^2 - 4*a*b*lam^3 - 4*a*b*lam^2 - 9*a*b*lam - 13*a*b + a*lam + a + 2*b^2*lam^4 + 2*b^2*lam^3 + 3*b^2*lam^2 + 5*b^2*lam + 8*b^2 - b*lam^2 - b*lam - 4*b)*hps
    linarith [hr, he]
  have qq21 : (0:ℝ) ≤ -2*a^2*lam^2 - 4*a^2*lam + 2*a^2 + 3*a*b*lam^2 + 2*a*b*lam - 2*a*b + a*lam^2 + 2*b^2*lam^2 + 3*b^2*lam - 2*b^2 - 2*b*lam^2 - 4*b*lam + 2*b + lam := by
    have hr : (0:ℝ) ≤ lam*((a*lam + b - 1)*(c*lam + d - 1)) := mul_nonneg hpos.le (mul_nonneg gen0 gen2)
    have he : lam*((a*lam + b - 1)*(c*lam + d - 1)) = -2*a^2*lam^2 - 4*a^2*lam + 2*a^2 + 3*a*b*lam^2 + 2*a*b*lam - 2*a*b + a*lam^2 + 2*b^2*lam^2 + 3*b^2*lam - 2*b^2 - 2*b*lam^2 - 4*b*lam + 2*b + lam := by linear_combination (2*a*lam^3 + 2*b*lam^2 - 2*lam^2)*hk0 + (a*lam^2 + b*lam - lam)*hk1 + (-2*a^2 + 2*a*b*lam + 2*a*b + 2*b^2 - 2*b)*hps
    linarith [hr, he]
  have qq22 : (0:ℝ) ≤ 2*a^2*lam^2 + 3*a^2*lam - 2*a^2 - 13*a*b*lam^2 - 6*a*b*lam + 6*a*b + 2*a*lam^2 + 4*a*lam - 2*a + 10*b^2*lam^2 + 8*b^2*lam - 6*b^2 - 5*b*lam^2 - 2*b*lam + 2*b + lam := by
    have hr : (0:ℝ) ≤ lam*((b*lam + c - 1)*(d*lam + e - 1)) := mul_nonneg hpos.le (mul_nonneg gen1 gen3)
    have he : lam*((b*lam + c - 1)*(d*lam + e - 1)) = 2*a^2*lam^2 + 3*a^2*lam - 2*a^2 - 13*a*b*lam^2 - 6*a*b*lam + 6*a*b + 2*a*lam^2 + 4*a*lam - 2*a + 10*b^2*lam^2 + 8*b^2*lam - 6*b^2 - 5*b*lam^2 - 2*b*lam + 2*b + lam := by linear_combination (-2*a*lam^3 + a*lam + 4*b*lam^4 - 2*b*lam^2 + d*lam^2 + e*lam - 2*lam^3)*hk0 + (-2*a*lam^2 + 4*b*lam^3 - 2*lam^2)*hk1 + (-a*lam + 2*b*lam^2 - lam)*hk2 + (2*a^2 - 6*a*b*lam - 6*a*b + 2*a + 4*b^2*lam^2 + 4*b^2*lam + 6*b^2 - 2*b*lam - 2*b)*hps
    linarith [hr, he]
  have qq23 : (0:ℝ) ≤ a^2*b*lam^2 + 2*a^2*b*lam - a^2*b - 6*a*b^2*lam^2 - 2*a*b^2*lam + 2*a*b^2 + a*b*lam^2 + 2*a*b*lam - a*b - a + 2*b*lam - 1 := by
    have hr : (0:ℝ) ≤ (b*lam + c - 1)*(-a*b*lam^3 + 1) := mul_nonneg gen1 slk0
    have he : (b*lam + c - 1)*(-a*b*lam^3 + 1) = a^2*b*lam^2 + 2*a^2*b*lam - a^2*b - 6*a*b^2*lam^2 - 2*a*b^2*lam + 2*a*b^2 + a*b*lam^2 + 2*a*b*lam - a*b - a + 2*b*lam - 1 := by linear_combination (-a*b*lam^3 + 1)*hk0 + (a^2*b - 2*a*b^2*lam - 2*a*b^2 + a*b)*hps
    linarith [hr, he]
  have qq24 : (0:ℝ) ≤ 6*a^3*lam^2 + 4*a^3*lam - 3*a^3 - 33*a^2*b*lam^2 - 28*a^2*b*lam + 19*a^2*b + 6*a^2*lam^2 + 4*a^2*lam - 3*a^2 + 53*a*b^2*lam^2 + 44*a*b^2*lam - 30*a*b^2 - 13*a*b*lam^2 - 10*a*b*lam + 7*a*b - a - 26*b^3*lam^2 - 20*b^3*lam + 14*b^3 + 7*b^2*lam^2 + 6*b^2*lam - 4*b^2 + 2*b*lam - 1 := by
    have hr : (0:ℝ) ≤ (b*lam + c - 1)*(-d*e*lam^3 + 1) := mul_nonneg gen1 slk3
    have he : (b*lam + c - 1)*(-d*e*lam^3 + 1) = 6*a^3*lam^2 + 4*a^3*lam - 3*a^3 - 33*a^2*b*lam^2 - 28*a^2*b*lam + 19*a^2*b + 6*a^2*lam^2 + 4*a^2*lam - 3*a^2 + 53*a*b^2*lam^2 + 44*a*b^2*lam - 30*a*b^2 - 13*a*b*lam^2 - 10*a*b*lam + 7*a*b - a - 26*b^3*lam^2 - 20*b^3*lam + 14*b^3 + 7*b^2*lam^2 + 6*b^2*lam - 4*b^2 + 2*b*lam - 1 := by linear_combination (-a^2*lam^6 + a^2*lam^4 + 3*a*b*lam^7 - 4*a*b*lam^5 + a*b*lam^3 + a*e*lam^4 - a*lam^6 + a*lam^4 - 2*b^2*lam^8 + 4*b^2*lam^6 - 2*b^2*lam^4 - 2*b*e*lam^5 + b*lam^7 - 2*b*lam^5 + b*lam^3 - d*e*lam^3 + e*lam^4 + 1)*hk0 + (-a^2*lam^5 + 3*a*b*lam^6 - a*b*lam^4 + a*e*lam^3 - a*lam^5 - 2*b^2*lam^7 + 2*b^2*lam^5 - 2*b*e*lam^4 + b*lam^6 - b*lam^4 + e*lam^3)*hk1 + (-a^2*lam^4 + 3*a*b*lam^5 - a*b*lam^3 - a*lam^4 - 2*b^2*lam^6 + 2*b^2*lam^4 + b*lam^5 - b*lam^3)*hk2 + (a^3*lam^3 + a^3*lam^2 + 2*a^3*lam + 3*a^3 - 4*a^2*b*lam^4 - 4*a^2*b*lam^3 - 6*a^2*b*lam^2 - 10*a^2*b*lam - 19*a^2*b + a^2*lam^3 + a^2*lam^2 + 2*a^2*lam + 3*a^2 + 5*a*b^2*lam^5 + 5*a*b^2*lam^4 + 4*a*b^2*lam^3 + 9*a*b^2*lam^2 + 16*a*b^2*lam + 30*a*b^2 - 2*a*b*lam^4 - 2*a*b*lam^3 - 2*a*b*lam^2 - 4*a*b*lam - 7*a*b - 2*b^3*lam^6 - 2*b^3*lam^5 - 2*b^3*lam^3 - 4*b^3*lam^2 - 8*b^3*lam - 14*b^3 + b^2*lam^5 + b^2*lam^4 + b^2*lam^2 + 2*b^2*lam + 4*b^2)*hps
    linarith [hr, he]
  have qq25 : (0:ℝ) ≤ -8*a^2*b*lam^2 - 10*a^2*b*lam + 6*a^2*b + 33*a*b^2*lam^2 + 19*a*b^2*lam - 15*a*b^2 - 3*a*b*lam^2 - a*b*lam + a*b - 2*a*lam^2 - 24*b^3*lam^2 - 23*b^3*lam + 15*b^3 + 4*b^2*lam^2 + 5*b^2*lam - 3*b^2 + 2*b*lam^2 + 3*b*lam - 2*b - lam := by
    have hr : (0:ℝ) ≤ lam*((c*lam + d - 1)*(-b*c*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg gen2 slk1)
    have he : lam*((c*lam + d - 1)*(-b*c*lam^3 + 1)) = -8*a^2*b*lam^2 - 10*a^2*b*lam + 6*a^2*b + 33*a*b^2*lam^2 + 19*a*b^2*lam - 15*a*b^2 - 3*a*b*lam^2 - a*b*lam + a*b - 2*a*lam^2 - 24*b^3*lam^2 - 23*b^3*lam + 15*b^3 + 4*b^2*lam^2 + 5*b^2*lam - 3*b^2 + 2*b*lam^2 + 3*b*lam - 2*b - lam := by linear_combination (2*a*b*lam^5 - 2*b^2*lam^6 - b*c*lam^5 - b*d*lam^4 + b*lam^4 + 2*lam^2)*hk0 + (a*b*lam^4 - b^2*lam^5 + lam)*hk1 + (-2*a^2*b*lam^2 - 2*a^2*b*lam - 6*a^2*b + 4*a*b^2*lam^3 + 4*a*b^2*lam^2 + 11*a*b^2*lam + 15*a*b^2 - a*b*lam - a*b - 2*b^3*lam^4 - 2*b^3*lam^3 - 5*b^3*lam^2 - 7*b^3*lam - 15*b^3 + b^2*lam^2 + b^2*lam + 3*b^2 + 2*b)*hps
    linarith [hr, he]
  linarith [qq0, qq1, qq2, qq3, qq4, qq5, qq6, qq7, qq8, qq9, qq10, qq11, qq12, qq13, qq14, qq15, qq16, qq17, qq18, qq19, qq20, qq21, qq22, qq23, qq24, qq25, h2, h3]

/-- **q=7 window-4 core.** 5 coords of a genuine scalar orbit (both Taha edges + cap
+ 3 integer floors K_i>=1 with recurrence and floor-upper) cannot have all 4 products
`< 1/lam^3`.  Each interior floor is forced to 1 (floor-helper), reducing to the single
Chebyshev case `case_q7`. -/
theorem g7_core (a b c d e lam : ℝ) (hps : lam^3 = lam^2 + 2*lam - 1) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hpa : 0 < a) (hpb : 0 < b) (hpc : 0 < c) (hpd : 0 < d) (hpe : 0 < e)
    (hca : a ≤ 1) (hcb : b ≤ 1) (hcc : c ≤ 1) (hcd : d ≤ 1) (hce : e ≤ 1)
    (hr0 : a+lam*b > 1) (hr1 : b+lam*c > 1) (hr2 : c+lam*d > 1) (hr3 : d+lam*e > 1)
    (hg0 : lam*a+b > 1) (hg1 : lam*b+c > 1) (hg2 : lam*c+d > 1) (hg3 : lam*d+e > 1)
    (K0 K1 K2 : ℤ)
    (hk0 : a+c = (K0:ℝ)*lam*b) (hk1 : b+d = (K1:ℝ)*lam*c) (hk2 : c+e = (K2:ℝ)*lam*d)
    (hKge0 : 1 ≤ K0) (hKge1 : 1 ≤ K1) (hKge2 : 1 ≤ K2)
    (hf0 : 1+a < ((K0:ℝ)+1)*(lam*b)) (hf1 : 1+b < ((K1:ℝ)+1)*(lam*c)) (hf2 : 1+c < ((K2:ℝ)+1)*(lam*d))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) (hP3 : d*e < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hlo : (9:ℝ)/5 < lam := g7_lam_lo lam hps h2 h3
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have hp4nn : (0:ℝ) ≤ lam^4 := by positivity
  have hP0c : a*b*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
  have hP1c : b*c*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP1
  have hP2c : c*d*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
  have hP3c : d*e*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP3
  have hKr0 : (1:ℝ) ≤ (K0:ℝ) := by exact_mod_cast hKge0
  have heng0 : a*b + b*c = (K0:ℝ)*lam*b^2 := by linear_combination b*hk0
  have hK0b : (K0:ℝ)*lam^4*b^2 < 2 := by
    have h : (a*b+b*c)*lam^3 = (K0:ℝ)*lam^4*b^2 := by linear_combination lam^3*heng0
    nlinarith [hP0c, hP1c, h]
  have hbU0 : lam^4*b^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*b^2 := mul_nonneg hp4nn (sq_nonneg _)
    nlinarith [hK0b, hKr0, mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-1) hn]
  have hKr1 : (1:ℝ) ≤ (K1:ℝ) := by exact_mod_cast hKge1
  have heng1 : b*c + c*d = (K1:ℝ)*lam*c^2 := by linear_combination c*hk1
  have hK1b : (K1:ℝ)*lam^4*c^2 < 2 := by
    have h : (b*c+c*d)*lam^3 = (K1:ℝ)*lam^4*c^2 := by linear_combination lam^3*heng1
    nlinarith [hP1c, hP2c, h]
  have hbU1 : lam^4*c^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*c^2 := mul_nonneg hp4nn (sq_nonneg _)
    nlinarith [hK1b, hKr1, mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-1) hn]
  have hKr2 : (1:ℝ) ≤ (K2:ℝ) := by exact_mod_cast hKge2
  have heng2 : c*d + d*e = (K2:ℝ)*lam*d^2 := by linear_combination d*hk2
  have hK2b : (K2:ℝ)*lam^4*d^2 < 2 := by
    have h : (c*d+d*e)*lam^3 = (K2:ℝ)*lam^4*d^2 := by linear_combination lam^3*heng2
    nlinarith [hP2c, hP3c, h]
  have hbU2 : lam^4*d^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*d^2 := mul_nonneg hp4nn (sq_nonneg _)
    nlinarith [hK2b, hKr2, mul_nonneg (by linarith : (0:ℝ) ≤ (K2:ℝ)-1) hn]
  have hKle0 : K0 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K0:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K0)
    have hn : (0:ℝ) ≤ lam^4*b^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*b^2 < 1 := by nlinarith [hK0b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-2) hn]
    exact g7_floor_helper lam b c h2 h3 hlo hpb hpc hms hbU1 (by linarith [hg1])
  have hKle1 : K1 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K1:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K1)
    have hn : (0:ℝ) ≤ lam^4*c^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*c^2 < 1 := by nlinarith [hK1b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-2) hn]
    exact g7_floor_helper lam c d h2 h3 hlo hpc hpd hms hbU2 (by linarith [hg2])
  have hKle2 : K2 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K2:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K2)
    have hn : (0:ℝ) ≤ lam^4*d^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*d^2 < 1 := by nlinarith [hK2b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K2:ℝ)-2) hn]
    exact g7_floor_helper lam d c h2 h3 hlo hpd hpc hms hbU1 (by linarith [hr2])
  interval_cases K0 <;> interval_cases K1 <;> interval_cases K2 <;>
    push_cast at hk0 hf0 hk1 hf1 hk2 hf2 <;>
    exact case_q7 a b c d e lam hps h2 h3 hpa hpb hpc hpd hpe hca hcb hcc hcd hce hr0 hr1 hr2 hr3 hg0 hg1 hg2 hg3 hk0 hk1 hk2 hf0 hf1 hf2 hP0 hP1 hP2 hP3

/-- **q=7 window-4, orbit form.** Along any genuine scalar orbit (both Taha edges + cap +
genuine floor recurrence), no 4 consecutive products are all `< 1/lam^3`. -/
theorem g7_no_window_below_genuine
    (lam : ℝ) (hps : lam^3 = lam^2 + 2*lam - 1) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (c : ℕ → ℝ) (hposc : ∀ n, 0 < c n) (hcap : ∀ n, c n ≤ 1)
    (hreg : ∀ n, c n + lam * c (n+1) > 1) (hgen : ∀ n, lam * c n + c (n+1) > 1)
    (hrec : ∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) :
    ∀ i, ¬ (c (i+0) * c (i+1) < 1/lam^3 ∧
            c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3 ∧
            c (i+3) * c (i+4) < 1/lam^3) := by
  have hpos' : 0 < lam := by linarith
  intro i hcon
  obtain ⟨hh0, hh1, hh2, hh3⟩ := hcon
  have flr : ∀ n, (1:ℤ) ≤ ⌊(1 + c n)/(lam*c (n+1))⌋ := by
    intro n
    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hposc (n+1))
    have hsum : 0 < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1) := by
      rw [← hrec n]; linarith [hposc n, hposc (n+2)]
    have h0' : (0:ℝ) < (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ) := by nlinarith [hsum, hden]
    have : (0:ℤ) < ⌊(1 + c n)/(lam*c (n+1))⌋ := by exact_mod_cast h0'
    omega
  have flrUB : ∀ n, 1 + c n < ((⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)+1)*(lam*c (n+1)) := by
    intro n
    have hden : 0 < lam*c (n+1) := mul_pos hpos' (hposc (n+1))
    have := Int.lt_floor_add_one ((1 + c n)/(lam*c (n+1)))
    rw [div_lt_iff₀ hden] at this
    linarith [this]
  exact g7_core (c (i+0)) (c (i+1)) (c (i+2)) (c (i+3)) (c (i+4)) lam hps h2 h3
    (hposc (i+0)) (hposc (i+1)) (hposc (i+2)) (hposc (i+3)) (hposc (i+4))
    (hcap (i+0)) (hcap (i+1)) (hcap (i+2)) (hcap (i+3)) (hcap (i+4))
    (hreg (i+0)) (hreg (i+1)) (hreg (i+2)) (hreg (i+3))
    (hgen (i+0)) (hgen (i+1)) (hgen (i+2)) (hgen (i+3))
    (⌊(1 + c (i+0))/(lam*c (i+1))⌋) (⌊(1 + c (i+1))/(lam*c (i+2))⌋) (⌊(1 + c (i+2))/(lam*c (i+3))⌋)
    (hrec (i+0)) (hrec (i+1)) (hrec (i+2))
    (flr (i+0)) (flr (i+1)) (flr (i+2))
    (flrUB (i+0)) (flrUB (i+1)) (flrUB (i+2))
    hh0 hh1 hh2 hh3

#print axioms g7_floor_helper
#print axioms case_q7
#print axioms g7_core
#print axioms g7_no_window_below_genuine
#print axioms g7_lam_lo