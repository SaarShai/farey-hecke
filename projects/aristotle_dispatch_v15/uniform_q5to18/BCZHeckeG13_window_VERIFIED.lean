import Mathlib
set_option maxHeartbeats 20000000
noncomputable section
open Int

/-- Interior-floor contradiction (K>=2 impossible inside a sub-threshold window): if a
middle coord `m` has `lam^4 m^2 < 1` (= the K>=2 bound) and a neighbour `n` with `lam^4 n^2
< 2` and edge `1 - lam m < n`, then False.  Uses only `9/5 < lam < 2` via `(lam^2-lam)^2
>= 2` — field-independent. -/
lemma g13_floor_helper (lam m n : ℝ) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
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

lemma case_q13 (a b c d e f lam : ℝ) (hps : lam^6 = lam^5 + 5*lam^4 - 4*lam^3 - 6*lam^2 + 3*lam + 1) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hpa : 0 < a) (hpb : 0 < b) (hpc : 0 < c) (hpd : 0 < d) (hpe : 0 < e) (hpf : 0 < f)
    (hca : a ≤ 1) (hcb : b ≤ 1) (hcc : c ≤ 1) (hcd : d ≤ 1) (hce : e ≤ 1) (hcf : f ≤ 1)
    (hr0 : a+lam*b > 1) (hr1 : b+lam*c > 1) (hr2 : c+lam*d > 1) (hr3 : d+lam*e > 1) (hr4 : e+lam*f > 1)
    (hg0 : lam*a+b > 1) (hg1 : lam*b+c > 1) (hg2 : lam*c+d > 1) (hg3 : lam*d+e > 1) (hg4 : lam*e+f > 1)
    (hk0 : a+c = 1*lam*b) (hk1 : b+d = 1*lam*c) (hk2 : c+e = 1*lam*d) (hk3 : d+f = 1*lam*e)
    (hf0 : 1+a < (1+1)*(lam*b)) (hf1 : 1+b < (1+1)*(lam*c)) (hf2 : 1+c < (1+1)*(lam*d)) (hf3 : 1+d < (1+1)*(lam*e))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) (hP3 : d*e < 1/lam^3) (hP4 : e*f < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have pos0 : (0:ℝ) ≤ a := le_of_lt hpa
  have pos1 : (0:ℝ) ≤ b := le_of_lt hpb
  have pos2 : (0:ℝ) ≤ c := le_of_lt hpc
  have pos3 : (0:ℝ) ≤ d := le_of_lt hpd
  have pos4 : (0:ℝ) ≤ e := le_of_lt hpe
  have pos5 : (0:ℝ) ≤ f := le_of_lt hpf
  have cap0 : (0:ℝ) ≤ 1 - a := by nlinarith [hca]
  have cap1 : (0:ℝ) ≤ 1 - b := by nlinarith [hcb]
  have cap2 : (0:ℝ) ≤ 1 - c := by nlinarith [hcc]
  have cap3 : (0:ℝ) ≤ 1 - d := by nlinarith [hcd]
  have cap4 : (0:ℝ) ≤ 1 - e := by nlinarith [hce]
  have cap5 : (0:ℝ) ≤ 1 - f := by nlinarith [hcf]
  have reg0 : (0:ℝ) ≤ a + b*lam - 1 := by nlinarith [hr0]
  have reg1 : (0:ℝ) ≤ b + c*lam - 1 := by nlinarith [hr1]
  have reg2 : (0:ℝ) ≤ c + d*lam - 1 := by nlinarith [hr2]
  have reg3 : (0:ℝ) ≤ d + e*lam - 1 := by nlinarith [hr3]
  have reg4 : (0:ℝ) ≤ e + f*lam - 1 := by nlinarith [hr4]
  have gen0 : (0:ℝ) ≤ a*lam + b - 1 := by nlinarith [hg0]
  have gen1 : (0:ℝ) ≤ b*lam + c - 1 := by nlinarith [hg1]
  have gen2 : (0:ℝ) ≤ c*lam + d - 1 := by nlinarith [hg2]
  have gen3 : (0:ℝ) ≤ d*lam + e - 1 := by nlinarith [hg3]
  have gen4 : (0:ℝ) ≤ e*lam + f - 1 := by nlinarith [hg4]
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
  have slk4 : (0:ℝ) ≤ -e*f*lam^3 + 1 := by
    have hh : (e*f)*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP4
    nlinarith [hh]
  have flu0 : (0:ℝ) ≤ -a + 2*b*lam - 1 := by nlinarith [hf0]
  have flu1 : (0:ℝ) ≤ -b + 2*c*lam - 1 := by nlinarith [hf1]
  have flu2 : (0:ℝ) ≤ -c + 2*d*lam - 1 := by nlinarith [hf2]
  have flu3 : (0:ℝ) ≤ -d + 2*e*lam - 1 := by nlinarith [hf3]
  have qq0 : (0:ℝ) ≤ -a^2*lam^5 + a^2*lam^3 + a^2*lam + a*b*lam^5 + 3*a*b*lam^4 - 4*a*b*lam^3 - 7*a*b*lam^2 + 3*a*b*lam + a*b - a*lam := by
    have hr : (0:ℝ) ≤ lam*((a)*(e + f*lam - 1)) := mul_nonneg hpos.le (mul_nonneg pos0 reg4)
    have he : lam*((a)*(e + f*lam - 1)) = -a^2*lam^5 + a^2*lam^3 + a^2*lam + a*b*lam^5 + 3*a*b*lam^4 - 4*a*b*lam^3 - 7*a*b*lam^2 + 3*a*b*lam + a*b - a*lam := by linear_combination (a*lam^5 - a*lam^3 - a*lam)*hk0 + (a*lam^4)*hk1 + (a*lam^3 + a*lam)*hk2 + (a*lam^2)*hk3 + (a*b)*hps
    linarith [hr, he]
  have qq1 : (0:ℝ) ≤ -a^2 - a*b*lam + 2*a + b*lam - 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(a + b*lam - 1) := mul_nonneg cap0 reg0
    have he : (1 - a)*(a + b*lam - 1) = -a^2 - a*b*lam + 2*a + b*lam - 1 := by linear_combination 0
    linarith [hr, he]
  have qq2 : (0:ℝ) ≤ -a^2*b*lam^3 + a*b^2*lam^4 + a*b*lam^3 - a - b^2*lam^4 + 1 := by
    have hr : (0:ℝ) ≤ (1 - a)*(-b*c*lam^3 + 1) := mul_nonneg cap0 slk1
    have he : (1 - a)*(-b*c*lam^3 + 1) = -a^2*b*lam^3 + a*b^2*lam^4 + a*b*lam^3 - a - b^2*lam^4 + 1 := by linear_combination (a*b*lam^3 - b*lam^3)*hk0
    linarith [hr, he]
  have qq3 : (0:ℝ) ≤ -a^2*b*lam^4 + a*b^2*lam^5 + a*b*lam^4 - a*lam - b^2*lam^5 + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(-b*c*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap0 slk1)
    have he : lam*((1 - a)*(-b*c*lam^3 + 1)) = -a^2*b*lam^4 + a*b^2*lam^5 + a*b*lam^4 - a*lam - b^2*lam^5 + lam := by linear_combination (a*b*lam^4 - b*lam^4)*hk0
    linarith [hr, he]
  have qq4 : (0:ℝ) ≤ 5*a^3*lam^5 + a^3*lam^4 - 10*a^3*lam^3 - 3*a^3*lam^2 + 4*a^3*lam + a^3 - 10*a^2*b*lam^5 - 21*a^2*b*lam^4 + 38*a^2*b*lam^3 + 40*a^2*b*lam^2 - 26*a^2*b*lam - 8*a^2*b - 5*a^2*lam^5 - a^2*lam^4 + 10*a^2*lam^3 + 3*a^2*lam^2 - 4*a^2*lam - a^2 + 11*a*b^2*lam^5 + 5*a*b^2*lam^4 - 30*a*b^2*lam^3 - 14*a*b^2*lam^2 + 15*a*b^2*lam + 4*a*b^2 + 10*a*b*lam^5 + 21*a*b*lam^4 - 38*a*b*lam^3 - 40*a*b*lam^2 + 26*a*b*lam + 8*a*b - a*lam - 11*b^2*lam^5 - 5*b^2*lam^4 + 30*b^2*lam^3 + 14*b^2*lam^2 - 15*b^2*lam - 4*b^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - a)*(-d*e*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap0 slk3)
    have he : lam*((1 - a)*(-d*e*lam^3 + 1)) = 5*a^3*lam^5 + a^3*lam^4 - 10*a^3*lam^3 - 3*a^3*lam^2 + 4*a^3*lam + a^3 - 10*a^2*b*lam^5 - 21*a^2*b*lam^4 + 38*a^2*b*lam^3 + 40*a^2*b*lam^2 - 26*a^2*b*lam - 8*a^2*b - 5*a^2*lam^5 - a^2*lam^4 + 10*a^2*lam^3 + 3*a^2*lam^2 - 4*a^2*lam - a^2 + 11*a*b^2*lam^5 + 5*a*b^2*lam^4 - 30*a*b^2*lam^3 - 14*a*b^2*lam^2 + 15*a*b^2*lam + 4*a*b^2 + 10*a*b*lam^5 + 21*a*b*lam^4 - 38*a*b*lam^3 - 40*a*b*lam^2 + 26*a*b*lam + 8*a*b - a*lam - 11*b^2*lam^5 - 5*b^2*lam^4 + 30*b^2*lam^3 + 14*b^2*lam^2 - 15*b^2*lam - 4*b^2 + lam := by linear_combination (-a^2*lam^7 + a^2*lam^5 + a*b*lam^8 - 2*a*b*lam^6 + a*b*lam^4 + a*e*lam^5 + a*lam^7 - a*lam^5 - b*lam^8 + 2*b*lam^6 - b*lam^4 - e*lam^5)*hk0 + (-a^2*lam^6 + a*b*lam^7 - a*b*lam^5 + a*e*lam^4 + a*lam^6 - b*lam^7 + b*lam^5 - e*lam^4)*hk1 + (-a^2*lam^5 + a*b*lam^6 - a*b*lam^4 + a*lam^5 - b*lam^6 + b*lam^4)*hk2 + (a^3*lam + a^3 - 2*a^2*b*lam^2 - 2*a^2*b*lam - 8*a^2*b - a^2*lam - a^2 + a*b^2*lam^3 + a*b^2*lam^2 + 3*a*b^2*lam + 4*a*b^2 + 2*a*b*lam^2 + 2*a*b*lam + 8*a*b - b^2*lam^3 - b^2*lam^2 - 3*b^2*lam - 4*b^2)*hps
    linarith [hr, he]
  have qq5 : (0:ℝ) ≤ a*b*lam^4 - a*b*lam^2 - a*b - a*lam^4 + a*lam^2 + a - b^2*lam^5 + 2*b^2*lam^3 + b^2*lam + b*lam^5 - 2*b*lam^3 - b*lam + b - 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(e + f*lam - 1) := mul_nonneg cap1 reg4
    have he : (1 - b)*(e + f*lam - 1) = a*b*lam^4 - a*b*lam^2 - a*b - a*lam^4 + a*lam^2 + a - b^2*lam^5 + 2*b^2*lam^3 + b^2*lam + b*lam^5 - 2*b*lam^3 - b*lam + b - 1 := by linear_combination (-b*lam^4 + b*lam^2 + b + lam^4 - lam^2 - 1)*hk0 + (-b*lam^3 + lam^3)*hk1 + (-b*lam^2 - b + lam^2 + 1)*hk2 + (-b*lam + lam)*hk3
    linarith [hr, he]
  have qq6 : (0:ℝ) ≤ a*b*lam^5 - a*b*lam^3 - a*b*lam - a*lam^5 + a*lam^3 + a*lam - b^2*lam^5 - 3*b^2*lam^4 + 4*b^2*lam^3 + 7*b^2*lam^2 - 3*b^2*lam - b^2 + b*lam^5 + 3*b*lam^4 - 4*b*lam^3 - 7*b*lam^2 + 4*b*lam + b - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(e + f*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap1 reg4)
    have he : lam*((1 - b)*(e + f*lam - 1)) = a*b*lam^5 - a*b*lam^3 - a*b*lam - a*lam^5 + a*lam^3 + a*lam - b^2*lam^5 - 3*b^2*lam^4 + 4*b^2*lam^3 + 7*b^2*lam^2 - 3*b^2*lam - b^2 + b*lam^5 + 3*b*lam^4 - 4*b*lam^3 - 7*b*lam^2 + 4*b*lam + b - lam := by linear_combination (-b*lam^5 + b*lam^3 + b*lam + lam^5 - lam^3 - lam)*hk0 + (-b*lam^4 + lam^4)*hk1 + (-b*lam^3 - b*lam + lam^3 + lam)*hk2 + (-b*lam^2 + lam^2)*hk3 + (-b^2 + b)*hps
    linarith [hr, he]
  have qq7 : (0:ℝ) ≤ -a*b*lam + a*lam - b^2 + 2*b - 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(a*lam + b - 1) := mul_nonneg cap1 gen0
    have he : (1 - b)*(a*lam + b - 1) = -a*b*lam + a*lam - b^2 + 2*b - 1 := by linear_combination 0
    linarith [hr, he]
  have qq8 : (0:ℝ) ≤ -a*b^2*lam^3 + a*b*lam^3 + b^3*lam^4 - b^2*lam^4 - b + 1 := by
    have hr : (0:ℝ) ≤ (1 - b)*(-b*c*lam^3 + 1) := mul_nonneg cap1 slk1
    have he : (1 - b)*(-b*c*lam^3 + 1) = -a*b^2*lam^3 + a*b*lam^3 + b^3*lam^4 - b^2*lam^4 - b + 1 := by linear_combination (b^2*lam^3 - b*lam^3)*hk0
    linarith [hr, he]
  have qq9 : (0:ℝ) ≤ -a*b^2*lam^4 + a*b*lam^4 + b^3*lam^5 - b^2*lam^5 - b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - b)*(-b*c*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap1 slk1)
    have he : lam*((1 - b)*(-b*c*lam^3 + 1)) = -a*b^2*lam^4 + a*b*lam^4 + b^3*lam^5 - b^2*lam^5 - b*lam + lam := by linear_combination (b^2*lam^4 - b*lam^4)*hk0
    linarith [hr, he]
  have qq10 : (0:ℝ) ≤ -a^2*lam^5 + a^2*lam^3 + a^2*lam + 2*a*b*lam^5 + 7*a*b*lam^4 - 8*a*b*lam^3 - 14*a*b*lam^2 + 6*a*b*lam + 2*a*b - a*lam^5 + a*lam^3 - 4*b^2*lam^5 - b^2*lam^4 + 11*b^2*lam^3 + 3*b^2*lam^2 - 4*b^2*lam - b^2 + b*lam^5 + 3*b*lam^4 - 4*b*lam^3 - 6*b*lam^2 + 3*b*lam + b - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(e + f*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap2 reg4)
    have he : lam*((1 - c)*(e + f*lam - 1)) = -a^2*lam^5 + a^2*lam^3 + a^2*lam + 2*a*b*lam^5 + 7*a*b*lam^4 - 8*a*b*lam^3 - 14*a*b*lam^2 + 6*a*b*lam + 2*a*b - a*lam^5 + a*lam^3 - 4*b^2*lam^5 - b^2*lam^4 + 11*b^2*lam^3 + 3*b^2*lam^2 - 4*b^2*lam - b^2 + b*lam^5 + 3*b*lam^4 - 4*b*lam^3 - 6*b*lam^2 + 3*b*lam + b - lam := by linear_combination (a*lam^5 - a*lam^3 - a*lam - b*lam^6 + b*lam^4 + b*lam^2 - e*lam - f*lam^2 + lam^5 - lam^3)*hk0 + (a*lam^4 - b*lam^5 + lam^4)*hk1 + (a*lam^3 + a*lam - b*lam^4 - b*lam^2 + lam^3 + lam)*hk2 + (a*lam^2 - b*lam^3 + lam^2)*hk3 + (2*a*b - b^2*lam - b^2 + b)*hps
    linarith [hr, he]
  have qq11 : (0:ℝ) ≤ a^2*b*lam^3 - 2*a*b^2*lam^4 + a*b*lam^3 + a + b^3*lam^5 - b^2*lam^4 - b*lam + 1 := by
    have hr : (0:ℝ) ≤ (1 - c)*(-b*c*lam^3 + 1) := mul_nonneg cap2 slk1
    have he : (1 - c)*(-b*c*lam^3 + 1) = a^2*b*lam^3 - 2*a*b^2*lam^4 + a*b*lam^3 + a + b^3*lam^5 - b^2*lam^4 - b*lam + 1 := by linear_combination (-a*b*lam^3 + b^2*lam^4 + b*c*lam^3 - b*lam^3 - 1)*hk0
    linarith [hr, he]
  have qq12 : (0:ℝ) ≤ -a^3*lam^5 + 3*a^2*b*lam^5 + 14*a^2*b*lam^4 - 12*a^2*b*lam^3 - 18*a^2*b*lam^2 + 9*a^2*b*lam + 3*a^2*b - a^2*lam^5 - 16*a*b^2*lam^5 - 3*a*b^2*lam^4 + 30*a*b^2*lam^3 + 9*a*b^2*lam^2 - 12*a*b^2*lam - 3*a*b^2 + 2*a*b*lam^5 + 9*a*b*lam^4 - 8*a*b*lam^3 - 12*a*b*lam^2 + 6*a*b*lam + 2*a*b + a*lam + 6*b^3*lam^5 + 15*b^3*lam^4 - 23*b^3*lam^3 - 26*b^3*lam^2 + 16*b^3*lam + 5*b^3 - 5*b^2*lam^5 - b^2*lam^4 + 10*b^2*lam^3 + 3*b^2*lam^2 - 4*b^2*lam - b^2 - b*lam^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - c)*(-c*d*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap2 slk2)
    have he : lam*((1 - c)*(-c*d*lam^3 + 1)) = -a^3*lam^5 + 3*a^2*b*lam^5 + 14*a^2*b*lam^4 - 12*a^2*b*lam^3 - 18*a^2*b*lam^2 + 9*a^2*b*lam + 3*a^2*b - a^2*lam^5 - 16*a*b^2*lam^5 - 3*a*b^2*lam^4 + 30*a*b^2*lam^3 + 9*a*b^2*lam^2 - 12*a*b^2*lam - 3*a*b^2 + 2*a*b*lam^5 + 9*a*b*lam^4 - 8*a*b*lam^3 - 12*a*b*lam^2 + 6*a*b*lam + 2*a*b + a*lam + 6*b^3*lam^5 + 15*b^3*lam^4 - 23*b^3*lam^3 - 26*b^3*lam^2 + 16*b^3*lam + 5*b^3 - 5*b^2*lam^5 - b^2*lam^4 + 10*b^2*lam^3 + 3*b^2*lam^2 - 4*b^2*lam - b^2 - b*lam^2 + lam := by linear_combination (a^2*lam^5 - 2*a*b*lam^6 - a*d*lam^4 + a*lam^5 + b^2*lam^7 + b*d*lam^5 - b*lam^6 + c*d*lam^4 - d*lam^4 - lam)*hk0 + (a^2*lam^4 - 2*a*b*lam^5 + a*lam^4 + b^2*lam^6 - b*lam^5)*hk1 + (3*a^2*b - 3*a*b^2*lam - 3*a*b^2 + 2*a*b + b^3*lam^2 + b^3*lam + 5*b^3 - b^2*lam - b^2)*hps
    linarith [hr, he]
  have qq13 : (0:ℝ) ≤ -a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 7*a^2*lam^2 - 3*a^2*lam - a^2 + 8*a*b*lam^5 + 2*a*b*lam^4 - 21*a*b*lam^3 - 6*a*b*lam^2 + 9*a*b*lam + 2*a*b - a*lam^5 + a*lam^3 - a*lam^2 + a*lam - 4*b^2*lam^5 - 6*b^2*lam^4 + 15*b^2*lam^3 + 13*b^2*lam^2 - 10*b^2*lam - 3*b^2 + b*lam^5 + 3*b*lam^4 - 3*b*lam^3 - 7*b*lam^2 + 2*b*lam + b - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - d)*(e + f*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap3 reg4)
    have he : lam*((1 - d)*(e + f*lam - 1)) = -a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 7*a^2*lam^2 - 3*a^2*lam - a^2 + 8*a*b*lam^5 + 2*a*b*lam^4 - 21*a*b*lam^3 - 6*a*b*lam^2 + 9*a*b*lam + 2*a*b - a*lam^5 + a*lam^3 - a*lam^2 + a*lam - 4*b^2*lam^5 - 6*b^2*lam^4 + 15*b^2*lam^3 + 13*b^2*lam^2 - 10*b^2*lam - 3*b^2 + b*lam^5 + 3*b*lam^4 - 3*b*lam^3 - 7*b*lam^2 + 2*b*lam + b - lam := by linear_combination (a*lam^6 - a*lam^4 - a*lam^2 - b*lam^7 + 2*b*lam^5 - b*lam - e*lam^2 - f*lam^3 + lam^5 - lam^3 + lam^2 - lam)*hk0 + (a*lam^5 - b*lam^6 + b*lam^4 - e*lam - f*lam^2 + lam^4 + lam)*hk1 + (a*lam^4 + a*lam^2 - b*lam^5 + b*lam + lam^3 + lam)*hk2 + (a*lam^3 - b*lam^4 + b*lam^2 + lam^2)*hk3 + (-a^2 + 2*a*b*lam + 2*a*b - b^2*lam^2 - b^2*lam - 3*b^2 + b)*hps
    linarith [hr, he]
  have qq14 : (0:ℝ) ≤ a^2*lam^3 - a*b*lam^4 + 2*a*b*lam^2 - b^2*lam^3 + b^2*lam + b*lam^3 - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - d)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap3 gen0)
    have he : lam*((1 - d)*(a*lam + b - 1)) = a^2*lam^3 - a*b*lam^4 + 2*a*b*lam^2 - b^2*lam^3 + b^2*lam + b*lam^3 - lam := by linear_combination (-a*lam^3 - b*lam^2 + lam^2)*hk0 + (-a*lam^2 - b*lam + lam)*hk1
    linarith [hr, he]
  have qq15 : (0:ℝ) ≤ -5*a^3*lam^5 - a^3*lam^4 + 10*a^3*lam^3 + 3*a^3*lam^2 - 4*a^3*lam - a^3 + 15*a^2*b*lam^5 + 32*a^2*b*lam^4 - 57*a^2*b*lam^3 - 60*a^2*b*lam^2 + 39*a^2*b*lam + 12*a^2*b - a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 6*a^2*lam^2 - 3*a^2*lam - a^2 - 34*a*b^2*lam^5 - 15*a*b^2*lam^4 + 91*a*b^2*lam^3 + 42*a*b^2*lam^2 - 45*a*b^2*lam - 12*a*b^2 + 8*a*b*lam^5 + 2*a*b*lam^4 - 19*a*b*lam^3 - 6*a*b*lam^2 + 8*a*b*lam + 2*a*b + a*lam + 12*b^3*lam^5 + 18*b^3*lam^4 - 43*b^3*lam^3 - 37*b^3*lam^2 + 27*b^3*lam + 8*b^3 - 4*b^2*lam^5 - 7*b^2*lam^4 + 15*b^2*lam^3 + 14*b^2*lam^2 - 10*b^2*lam - 3*b^2 - b*lam^2 + b + 1 := by
    have hr : (0:ℝ) ≤ (1 - d)*(-d*e*lam^3 + 1) := mul_nonneg cap3 slk3
    have he : (1 - d)*(-d*e*lam^3 + 1) = -5*a^3*lam^5 - a^3*lam^4 + 10*a^3*lam^3 + 3*a^3*lam^2 - 4*a^3*lam - a^3 + 15*a^2*b*lam^5 + 32*a^2*b*lam^4 - 57*a^2*b*lam^3 - 60*a^2*b*lam^2 + 39*a^2*b*lam + 12*a^2*b - a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 6*a^2*lam^2 - 3*a^2*lam - a^2 - 34*a*b^2*lam^5 - 15*a*b^2*lam^4 + 91*a*b^2*lam^3 + 42*a*b^2*lam^2 - 45*a*b^2*lam - 12*a*b^2 + 8*a*b*lam^5 + 2*a*b*lam^4 - 19*a*b*lam^3 - 6*a*b*lam^2 + 8*a*b*lam + 2*a*b + a*lam + 12*b^3*lam^5 + 18*b^3*lam^4 - 43*b^3*lam^3 - 37*b^3*lam^2 + 27*b^3*lam + 8*b^3 - 4*b^2*lam^5 - 7*b^2*lam^4 + 15*b^2*lam^3 + 14*b^2*lam^2 - 10*b^2*lam - 3*b^2 - b*lam^2 + b + 1 := by linear_combination (a^2*lam^7 - a^2*lam^5 - 2*a*b*lam^8 + 4*a*b*lam^6 - 2*a*b*lam^4 - a*e*lam^5 + a*lam^6 - a*lam^4 + b^2*lam^9 - 3*b^2*lam^7 + 3*b^2*lam^5 - b^2*lam^3 + b*e*lam^6 - b*e*lam^4 - b*lam^7 + 2*b*lam^5 - b*lam^3 + d*e*lam^4 - e*lam^4 - lam)*hk0 + (a^2*lam^6 - 2*a*b*lam^7 + 2*a*b*lam^5 - a*e*lam^4 + a*lam^5 + b^2*lam^8 - 2*b^2*lam^6 + b^2*lam^4 + b*e*lam^5 - b*e*lam^3 - b*lam^6 + b*lam^4 + d*e*lam^3 - e*lam^3 - 1)*hk1 + (a^2*lam^5 - 2*a*b*lam^6 + 2*a*b*lam^4 + a*lam^4 + b^2*lam^7 - 2*b^2*lam^5 + b^2*lam^3 - b*lam^5 + b*lam^3)*hk2 + (-a^3*lam - a^3 + 3*a^2*b*lam^2 + 3*a^2*b*lam + 12*a^2*b - a^2 - 3*a*b^2*lam^3 - 3*a*b^2*lam^2 - 9*a*b^2*lam - 12*a*b^2 + 2*a*b*lam + 2*a*b + b^3*lam^4 + b^3*lam^3 + 2*b^3*lam^2 + 3*b^3*lam + 8*b^3 - b^2*lam^2 - b^2*lam - 3*b^2)*hps
    linarith [hr, he]
  have qq16 : (0:ℝ) ≤ -a^2*lam^5 - 3*a^2*lam^4 + 4*a^2*lam^3 + 6*a^2*lam^2 - 3*a^2*lam - 2*a^2 + 6*a*b*lam^5 + 2*a*b*lam^4 - 18*a*b*lam^3 - 6*a*b*lam^2 + 11*a*b*lam + 2*a*b - a*lam^4 + 2*a - 3*b^2*lam^5 - 3*b^2*lam^4 + 11*b^2*lam^3 + 6*b^2*lam^2 - 7*b^2*lam - 2*b^2 + b*lam^5 - b*lam^3 - 3*b*lam - 1 := by
    have hr : (0:ℝ) ≤ (1 - e)*(e + f*lam - 1) := mul_nonneg cap4 reg4
    have he : (1 - e)*(e + f*lam - 1) = -a^2*lam^5 - 3*a^2*lam^4 + 4*a^2*lam^3 + 6*a^2*lam^2 - 3*a^2*lam - 2*a^2 + 6*a*b*lam^5 + 2*a*b*lam^4 - 18*a*b*lam^3 - 6*a*b*lam^2 + 11*a*b*lam + 2*a*b - a*lam^4 + 2*a - 3*b^2*lam^5 - 3*b^2*lam^4 + 11*b^2*lam^3 + 6*b^2*lam^2 - 7*b^2*lam - 2*b^2 + b*lam^5 - b*lam^3 - 3*b*lam - 1 := by linear_combination (a*lam^6 - 2*a*lam^4 + a - b*lam^7 + 3*b*lam^5 - b*lam^3 - 2*b*lam - e*lam^2 + e - f*lam^3 + f*lam + lam^4 - 2)*hk0 + (a*lam^5 - a*lam^3 - b*lam^6 + 2*b*lam^4 - e*lam - f*lam^2 + lam^3 + lam)*hk1 + (a*lam^4 - a - b*lam^5 + b*lam^3 + 2*b*lam - e - f*lam + lam^2 + 2)*hk2 + (a*lam^3 - a*lam - b*lam^4 + 2*b*lam^2 + lam)*hk3 + (-a^2 + 2*a*b*lam + 2*a*b - b^2*lam^2 - b^2*lam - 2*b^2)*hps
    linarith [hr, he]
  have qq17 : (0:ℝ) ≤ a^2*lam^3 - a^2*lam - a*b*lam^4 + 3*a*b*lam^2 - a*b - a*lam^2 + a*lam + a - b^2*lam^3 + 2*b^2*lam + b*lam^3 - 2*b*lam + b - 1 := by
    have hr : (0:ℝ) ≤ (1 - e)*(a*lam + b - 1) := mul_nonneg cap4 gen0
    have he : (1 - e)*(a*lam + b - 1) = a^2*lam^3 - a^2*lam - a*b*lam^4 + 3*a*b*lam^2 - a*b - a*lam^2 + a*lam + a - b^2*lam^3 + 2*b^2*lam + b*lam^3 - 2*b*lam + b - 1 := by linear_combination (-a*lam^3 + a*lam - b*lam^2 + b + lam^2 - 1)*hk0 + (-a*lam^2 - b*lam + lam)*hk1 + (-a*lam - b + 1)*hk2
    linarith [hr, he]
  have qq18 : (0:ℝ) ≤ a^2*lam^4 - a^2*lam^2 - a*b*lam^5 + 3*a*b*lam^3 - a*b*lam - a*lam^3 + a*lam^2 + a*lam - b^2*lam^4 + 2*b^2*lam^2 + b*lam^4 - 2*b*lam^2 + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - e)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg cap4 gen0)
    have he : lam*((1 - e)*(a*lam + b - 1)) = a^2*lam^4 - a^2*lam^2 - a*b*lam^5 + 3*a*b*lam^3 - a*b*lam - a*lam^3 + a*lam^2 + a*lam - b^2*lam^4 + 2*b^2*lam^2 + b*lam^4 - 2*b*lam^2 + b*lam - lam := by linear_combination (-a*lam^4 + a*lam^2 - b*lam^3 + b*lam + lam^3 - lam)*hk0 + (-a*lam^3 - b*lam^2 + lam^2)*hk1 + (-a*lam^2 - b*lam + lam)*hk2
    linarith [hr, he]
  have qq19 : (0:ℝ) ≤ -5*a^3*lam^5 - a^3*lam^4 + 10*a^3*lam^3 + 3*a^3*lam^2 - 4*a^3*lam - a^3 + 16*a^2*b*lam^5 + 36*a^2*b*lam^4 - 61*a^2*b*lam^3 - 66*a^2*b*lam^2 + 42*a^2*b*lam + 13*a^2*b - a^2*lam^5 - 42*a*b^2*lam^5 - 17*a*b^2*lam^4 + 110*a*b^2*lam^3 + 48*a*b^2*lam^2 - 53*a*b^2*lam - 14*a*b^2 + 2*a*b*lam^5 + 9*a*b*lam^4 - 8*a*b*lam^3 - 12*a*b*lam^2 + 6*a*b*lam + 2*a*b + a*lam^3 - a*lam + 16*b^3*lam^5 + 25*b^3*lam^4 - 58*b^3*lam^3 - 51*b^3*lam^2 + 37*b^3*lam + 11*b^3 - 5*b^2*lam^5 - b^2*lam^4 + 10*b^2*lam^3 + 3*b^2*lam^2 - 4*b^2*lam - b^2 - b*lam^4 + 2*b*lam^2 + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - e)*(-c*d*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap4 slk2)
    have he : lam*((1 - e)*(-c*d*lam^3 + 1)) = -5*a^3*lam^5 - a^3*lam^4 + 10*a^3*lam^3 + 3*a^3*lam^2 - 4*a^3*lam - a^3 + 16*a^2*b*lam^5 + 36*a^2*b*lam^4 - 61*a^2*b*lam^3 - 66*a^2*b*lam^2 + 42*a^2*b*lam + 13*a^2*b - a^2*lam^5 - 42*a*b^2*lam^5 - 17*a*b^2*lam^4 + 110*a*b^2*lam^3 + 48*a*b^2*lam^2 - 53*a*b^2*lam - 14*a*b^2 + 2*a*b*lam^5 + 9*a*b*lam^4 - 8*a*b*lam^3 - 12*a*b*lam^2 + 6*a*b*lam + 2*a*b + a*lam^3 - a*lam + 16*b^3*lam^5 + 25*b^3*lam^4 - 58*b^3*lam^3 - 51*b^3*lam^2 + 37*b^3*lam + 11*b^3 - 5*b^2*lam^5 - b^2*lam^4 + 10*b^2*lam^3 + 3*b^2*lam^2 - 4*b^2*lam - b^2 - b*lam^4 + 2*b*lam^2 + lam := by linear_combination (a^2*lam^7 - a^2*lam^5 - 2*a*b*lam^8 + 3*a*b*lam^6 - a*b*lam^4 - a*e*lam^5 + a*lam^5 + b^2*lam^9 - 2*b^2*lam^7 + b^2*lam^5 + b*e*lam^6 - b*lam^6 + d*e*lam^4 - d*lam^4 - lam^3 + lam)*hk0 + (a^2*lam^6 - 2*a*b*lam^7 + a*b*lam^5 - a*e*lam^4 + a*lam^4 + b^2*lam^8 - b^2*lam^6 + b*e*lam^5 - b*lam^5 - lam^2)*hk1 + (a^2*lam^5 - 2*a*b*lam^6 + a*b*lam^4 + b^2*lam^7 - b^2*lam^5 - lam)*hk2 + (-a^3*lam - a^3 + 3*a^2*b*lam^2 + 3*a^2*b*lam + 13*a^2*b - 3*a*b^2*lam^3 - 3*a*b^2*lam^2 - 11*a*b^2*lam - 14*a*b^2 + 2*a*b + b^3*lam^4 + b^3*lam^3 + 3*b^3*lam^2 + 4*b^3*lam + 11*b^3 - b^2*lam - b^2)*hps
    linarith [hr, he]
  have qq20 : (0:ℝ) ≤ -5*a^3*lam^5 - 11*a^3*lam^4 + 19*a^3*lam^3 + 20*a^3*lam^2 - 13*a^3*lam - 4*a^3 + 34*a^2*b*lam^5 + 15*a^2*b*lam^4 - 91*a^2*b*lam^3 - 42*a^2*b*lam^2 + 45*a^2*b*lam + 12*a^2*b - a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 6*a^2*lam^2 - 3*a^2*lam - a^2 - 35*a*b^2*lam^5 - 51*a*b^2*lam^4 + 125*a*b^2*lam^3 + 105*a*b^2*lam^2 - 78*a*b^2*lam - 23*a*b^2 + 8*a*b*lam^5 + 2*a*b*lam^4 - 19*a*b*lam^3 - 6*a*b*lam^2 + 8*a*b*lam + 2*a*b + a*lam^2 - a + 19*b^3*lam^5 + 12*b^3*lam^4 - 55*b^3*lam^3 - 31*b^3*lam^2 + 29*b^3*lam + 8*b^3 - 4*b^2*lam^5 - 7*b^2*lam^4 + 15*b^2*lam^3 + 14*b^2*lam^2 - 10*b^2*lam - 3*b^2 - b*lam^3 + 2*b*lam + 1 := by
    have hr : (0:ℝ) ≤ (1 - e)*(-d*e*lam^3 + 1) := mul_nonneg cap4 slk3
    have he : (1 - e)*(-d*e*lam^3 + 1) = -5*a^3*lam^5 - 11*a^3*lam^4 + 19*a^3*lam^3 + 20*a^3*lam^2 - 13*a^3*lam - 4*a^3 + 34*a^2*b*lam^5 + 15*a^2*b*lam^4 - 91*a^2*b*lam^3 - 42*a^2*b*lam^2 + 45*a^2*b*lam + 12*a^2*b - a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 6*a^2*lam^2 - 3*a^2*lam - a^2 - 35*a*b^2*lam^5 - 51*a*b^2*lam^4 + 125*a*b^2*lam^3 + 105*a*b^2*lam^2 - 78*a*b^2*lam - 23*a*b^2 + 8*a*b*lam^5 + 2*a*b*lam^4 - 19*a*b*lam^3 - 6*a*b*lam^2 + 8*a*b*lam + 2*a*b + a*lam^2 - a + 19*b^3*lam^5 + 12*b^3*lam^4 - 55*b^3*lam^3 - 31*b^3*lam^2 + 29*b^3*lam + 8*b^3 - 4*b^2*lam^5 - 7*b^2*lam^4 + 15*b^2*lam^3 + 14*b^2*lam^2 - 10*b^2*lam - 3*b^2 - b*lam^3 + 2*b*lam + 1 := by linear_combination (a^2*lam^8 - 2*a^2*lam^6 + a^2*lam^4 - 2*a*b*lam^9 + 6*a*b*lam^7 - 5*a*b*lam^5 + a*b*lam^3 - a*e*lam^6 + a*e*lam^4 + a*lam^6 - a*lam^4 + b^2*lam^10 - 4*b^2*lam^8 + 5*b^2*lam^6 - 2*b^2*lam^4 + b*e*lam^7 - 2*b*e*lam^5 + b*e*lam^3 - b*lam^7 + 2*b*lam^5 - b*lam^3 + e^2*lam^4 - e*lam^4 - lam^2 + 1)*hk0 + (a^2*lam^7 - a^2*lam^5 - 2*a*b*lam^8 + 4*a*b*lam^6 - a*b*lam^4 - a*e*lam^5 + a*lam^5 + b^2*lam^9 - 3*b^2*lam^7 + 2*b^2*lam^5 + b*e*lam^6 - b*e*lam^4 - b*lam^6 + b*lam^4 + e^2*lam^3 - e*lam^3 - lam)*hk1 + (a^2*lam^6 - a^2*lam^4 - 2*a*b*lam^7 + 4*a*b*lam^5 - a*b*lam^3 - a*e*lam^4 + a*lam^4 + b^2*lam^8 - 3*b^2*lam^6 + 2*b^2*lam^4 + b*e*lam^5 - b*e*lam^3 - b*lam^5 + b*lam^3 - 1)*hk2 + (-a^3*lam^2 - a^3*lam - 4*a^3 + 3*a^2*b*lam^3 + 3*a^2*b*lam^2 + 9*a^2*b*lam + 12*a^2*b - a^2 - 3*a*b^2*lam^4 - 3*a*b^2*lam^3 - 6*a*b^2*lam^2 - 9*a*b^2*lam - 23*a*b^2 + 2*a*b*lam + 2*a*b + b^3*lam^5 + b^3*lam^4 + b^3*lam^3 + 2*b^3*lam^2 + 5*b^3*lam + 8*b^3 - b^2*lam^2 - b^2*lam - 3*b^2)*hps
    linarith [hr, he]
  have qq21 : (0:ℝ) ≤ a^2*lam^4 - 2*a^2*lam^2 + a*b*lam^3 - a*b*lam - a*lam^4 + 2*a*lam^2 + a*lam - b^2*lam^5 - 2*b^2*lam^4 + 4*b^2*lam^3 + 5*b^2*lam^2 - 3*b^2*lam - b^2 + b*lam^5 - 3*b*lam^3 + b*lam^2 + b*lam - lam := by
    have hr : (0:ℝ) ≤ lam*((1 - f)*(a + b*lam - 1)) := mul_nonneg hpos.le (mul_nonneg cap5 reg0)
    have he : lam*((1 - f)*(a + b*lam - 1)) = a^2*lam^4 - 2*a^2*lam^2 + a*b*lam^3 - a*b*lam - a*lam^4 + 2*a*lam^2 + a*lam - b^2*lam^5 - 2*b^2*lam^4 + 4*b^2*lam^3 + 5*b^2*lam^2 - 3*b^2*lam - b^2 + b*lam^5 - 3*b*lam^3 + b*lam^2 + b*lam - lam := by linear_combination (-a*lam^4 + 2*a*lam^2 - b*lam^5 + 2*b*lam^3 + lam^4 - 2*lam^2)*hk0 + (-a*lam^3 + a*lam - b*lam^4 + b*lam^2 + lam^3 - lam)*hk1 + (-a*lam^2 - b*lam^3 + lam^2)*hk2 + (-a*lam - b*lam^2 + lam)*hk3 + (-b^2)*hps
    linarith [hr, he]
  have qq22 : (0:ℝ) ≤ 4*a^2*b*lam^5 + a^2*b*lam^4 - 10*a^2*b*lam^3 - 3*a^2*b*lam^2 + 4*a^2*b*lam + a^2*b - 9*a*b^2*lam^5 - 16*a*b^2*lam^4 + 34*a*b^2*lam^3 + 34*a*b^2*lam^2 - 23*a*b^2*lam - 7*a*b^2 + a*b*lam^4 + a*lam^4 - 2*a*lam^2 + 10*b^3*lam^5 + 5*b^3*lam^4 - 30*b^3*lam^3 - 14*b^3*lam^2 + 15*b^3*lam + 4*b^3 - b^2*lam^5 - b*lam^5 + 3*b*lam^3 - b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - f)*(-b*c*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap5 slk1)
    have he : lam*((1 - f)*(-b*c*lam^3 + 1)) = 4*a^2*b*lam^5 + a^2*b*lam^4 - 10*a^2*b*lam^3 - 3*a^2*b*lam^2 + 4*a^2*b*lam + a^2*b - 9*a*b^2*lam^5 - 16*a*b^2*lam^4 + 34*a*b^2*lam^3 + 34*a*b^2*lam^2 - 23*a*b^2*lam - 7*a*b^2 + a*b*lam^4 + a*lam^4 - 2*a*lam^2 + 10*b^3*lam^5 + 5*b^3*lam^4 - 30*b^3*lam^3 - 14*b^3*lam^2 + 15*b^3*lam + 4*b^3 - b^2*lam^5 - b*lam^5 + 3*b*lam^3 - b*lam + lam := by linear_combination (-a*b*lam^7 + 2*a*b*lam^5 + b^2*lam^8 - 2*b^2*lam^6 + b*f*lam^4 - b*lam^4 - lam^4 + 2*lam^2)*hk0 + (-a*b*lam^6 + a*b*lam^4 + b^2*lam^7 - b^2*lam^5 - lam^3 + lam)*hk1 + (-a*b*lam^5 + b^2*lam^6 - lam^2)*hk2 + (-a*b*lam^4 + b^2*lam^5 - lam)*hk3 + (a^2*b*lam + a^2*b - 2*a*b^2*lam^2 - 2*a*b^2*lam - 7*a*b^2 + b^3*lam^3 + b^3*lam^2 + 3*b^3*lam + 4*b^3)*hps
    linarith [hr, he]
  have qq23 : (0:ℝ) ≤ -11*a^3*lam^5 - 5*a^3*lam^4 + 30*a^3*lam^3 + 14*a^3*lam^2 - 15*a^3*lam - 4*a^3 + 34*a^2*b*lam^5 + 47*a^2*b*lam^4 - 121*a^2*b*lam^3 - 99*a^2*b*lam^2 + 75*a^2*b*lam + 22*a^2*b - a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 6*a^2*lam^2 - 3*a^2*lam - a^2 - 52*a*b^2*lam^5 - 35*a*b^2*lam^4 + 154*a*b^2*lam^3 + 90*a*b^2*lam^2 - 83*a*b^2*lam - 23*a*b^2 + 8*a*b*lam^5 + 2*a*b*lam^4 - 19*a*b*lam^3 - 6*a*b*lam^2 + 8*a*b*lam + 2*a*b + a*lam^3 - 2*a*lam + 19*b^3*lam^5 + 22*b^3*lam^4 - 64*b^3*lam^3 - 48*b^3*lam^2 + 38*b^3*lam + 11*b^3 - 4*b^2*lam^5 - 7*b^2*lam^4 + 15*b^2*lam^3 + 14*b^2*lam^2 - 10*b^2*lam - 3*b^2 - b*lam^4 + 3*b*lam^2 - b + 1 := by
    have hr : (0:ℝ) ≤ (1 - f)*(-d*e*lam^3 + 1) := mul_nonneg cap5 slk3
    have he : (1 - f)*(-d*e*lam^3 + 1) = -11*a^3*lam^5 - 5*a^3*lam^4 + 30*a^3*lam^3 + 14*a^3*lam^2 - 15*a^3*lam - 4*a^3 + 34*a^2*b*lam^5 + 47*a^2*b*lam^4 - 121*a^2*b*lam^3 - 99*a^2*b*lam^2 + 75*a^2*b*lam + 22*a^2*b - a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 6*a^2*lam^2 - 3*a^2*lam - a^2 - 52*a*b^2*lam^5 - 35*a*b^2*lam^4 + 154*a*b^2*lam^3 + 90*a*b^2*lam^2 - 83*a*b^2*lam - 23*a*b^2 + 8*a*b*lam^5 + 2*a*b*lam^4 - 19*a*b*lam^3 - 6*a*b*lam^2 + 8*a*b*lam + 2*a*b + a*lam^3 - 2*a*lam + 19*b^3*lam^5 + 22*b^3*lam^4 - 64*b^3*lam^3 - 48*b^3*lam^2 + 38*b^3*lam + 11*b^3 - 4*b^2*lam^5 - 7*b^2*lam^4 + 15*b^2*lam^3 + 14*b^2*lam^2 - 10*b^2*lam - 3*b^2 - b*lam^4 + 3*b*lam^2 - b + 1 := by linear_combination (a^2*lam^9 - 3*a^2*lam^7 + 2*a^2*lam^5 - 2*a*b*lam^10 + 8*a*b*lam^8 - 9*a*b*lam^6 + 2*a*b*lam^4 - a*f*lam^6 + a*f*lam^4 + a*lam^6 - a*lam^4 + b^2*lam^11 - 5*b^2*lam^9 + 8*b^2*lam^7 - 4*b^2*lam^5 + b*f*lam^7 - 2*b*f*lam^5 + b*f*lam^3 - b*lam^7 + 2*b*lam^5 - b*lam^3 + e*f*lam^4 - e*lam^4 - lam^3 + 2*lam)*hk0 + (a^2*lam^8 - 2*a^2*lam^6 + a^2*lam^4 - 2*a*b*lam^9 + 6*a*b*lam^7 - 5*a*b*lam^5 + a*b*lam^3 - a*f*lam^5 + a*lam^5 + b^2*lam^10 - 4*b^2*lam^8 + 5*b^2*lam^6 - 2*b^2*lam^4 + b*f*lam^6 - b*f*lam^4 - b*lam^6 + b*lam^4 + e*f*lam^3 - e*lam^3 - lam^2 + 1)*hk1 + (a^2*lam^7 - a^2*lam^5 - 2*a*b*lam^8 + 4*a*b*lam^6 - a*b*lam^4 - a*f*lam^4 + a*lam^4 + b^2*lam^9 - 3*b^2*lam^7 + 2*b^2*lam^5 + b*f*lam^5 - b*f*lam^3 - b*lam^5 + b*lam^3 - lam)*hk2 + (a^2*lam^6 - a^2*lam^4 - 2*a*b*lam^7 + 4*a*b*lam^5 - a*b*lam^3 + b^2*lam^8 - 3*b^2*lam^6 + 2*b^2*lam^4 - 1)*hk3 + (-a^3*lam^3 - a^3*lam^2 - 3*a^3*lam - 4*a^3 + 3*a^2*b*lam^4 + 3*a^2*b*lam^3 + 6*a^2*b*lam^2 + 9*a^2*b*lam + 22*a^2*b - a^2 - 3*a*b^2*lam^5 - 3*a*b^2*lam^4 - 3*a*b^2*lam^3 - 6*a*b^2*lam^2 - 14*a*b^2*lam - 23*a*b^2 + 2*a*b*lam + 2*a*b + b^3*lam^6 + b^3*lam^5 + b^3*lam^3 + 3*b^3*lam^2 + 5*b^3*lam + 11*b^3 - b^2*lam^2 - b^2*lam - 3*b^2)*hps
    linarith [hr, he]
  have qq24 : (0:ℝ) ≤ -16*a^3*lam^5 - 25*a^3*lam^4 + 58*a^3*lam^3 + 51*a^3*lam^2 - 37*a^3*lam - 11*a^3 + 81*a^2*b*lam^5 + 49*a^2*b*lam^4 - 235*a^2*b*lam^3 - 129*a^2*b*lam^2 + 124*a^2*b*lam + 34*a^2*b - 5*a^2*lam^5 - a^2*lam^4 + 10*a^2*lam^3 + 3*a^2*lam^2 - 4*a^2*lam - a^2 - 87*a*b^2*lam^5 - 106*a*b^2*lam^4 + 298*a*b^2*lam^3 + 229*a*b^2*lam^2 - 179*a*b^2*lam - 52*a*b^2 + 10*a*b*lam^5 + 21*a*b*lam^4 - 38*a*b*lam^3 - 40*a*b*lam^2 + 26*a*b*lam + 8*a*b + a*lam^4 - 2*a*lam^2 + 41*b^3*lam^5 + 31*b^3*lam^4 - 124*b^3*lam^3 - 76*b^3*lam^2 + 68*b^3*lam + 19*b^3 - 11*b^2*lam^5 - 5*b^2*lam^4 + 30*b^2*lam^3 + 14*b^2*lam^2 - 15*b^2*lam - 4*b^2 - b*lam^5 + 3*b*lam^3 - b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((1 - f)*(-d*e*lam^3 + 1)) := mul_nonneg hpos.le (mul_nonneg cap5 slk3)
    have he : lam*((1 - f)*(-d*e*lam^3 + 1)) = -16*a^3*lam^5 - 25*a^3*lam^4 + 58*a^3*lam^3 + 51*a^3*lam^2 - 37*a^3*lam - 11*a^3 + 81*a^2*b*lam^5 + 49*a^2*b*lam^4 - 235*a^2*b*lam^3 - 129*a^2*b*lam^2 + 124*a^2*b*lam + 34*a^2*b - 5*a^2*lam^5 - a^2*lam^4 + 10*a^2*lam^3 + 3*a^2*lam^2 - 4*a^2*lam - a^2 - 87*a*b^2*lam^5 - 106*a*b^2*lam^4 + 298*a*b^2*lam^3 + 229*a*b^2*lam^2 - 179*a*b^2*lam - 52*a*b^2 + 10*a*b*lam^5 + 21*a*b*lam^4 - 38*a*b*lam^3 - 40*a*b*lam^2 + 26*a*b*lam + 8*a*b + a*lam^4 - 2*a*lam^2 + 41*b^3*lam^5 + 31*b^3*lam^4 - 124*b^3*lam^3 - 76*b^3*lam^2 + 68*b^3*lam + 19*b^3 - 11*b^2*lam^5 - 5*b^2*lam^4 + 30*b^2*lam^3 + 14*b^2*lam^2 - 15*b^2*lam - 4*b^2 - b*lam^5 + 3*b*lam^3 - b*lam + lam := by linear_combination (a^2*lam^10 - 3*a^2*lam^8 + 2*a^2*lam^6 - 2*a*b*lam^11 + 8*a*b*lam^9 - 9*a*b*lam^7 + 2*a*b*lam^5 - a*f*lam^7 + a*f*lam^5 + a*lam^7 - a*lam^5 + b^2*lam^12 - 5*b^2*lam^10 + 8*b^2*lam^8 - 4*b^2*lam^6 + b*f*lam^8 - 2*b*f*lam^6 + b*f*lam^4 - b*lam^8 + 2*b*lam^6 - b*lam^4 + e*f*lam^5 - e*lam^5 - lam^4 + 2*lam^2)*hk0 + (a^2*lam^9 - 2*a^2*lam^7 + a^2*lam^5 - 2*a*b*lam^10 + 6*a*b*lam^8 - 5*a*b*lam^6 + a*b*lam^4 - a*f*lam^6 + a*lam^6 + b^2*lam^11 - 4*b^2*lam^9 + 5*b^2*lam^7 - 2*b^2*lam^5 + b*f*lam^7 - b*f*lam^5 - b*lam^7 + b*lam^5 + e*f*lam^4 - e*lam^4 - lam^3 + lam)*hk1 + (a^2*lam^8 - a^2*lam^6 - 2*a*b*lam^9 + 4*a*b*lam^7 - a*b*lam^5 - a*f*lam^5 + a*lam^5 + b^2*lam^10 - 3*b^2*lam^8 + 2*b^2*lam^6 + b*f*lam^6 - b*f*lam^4 - b*lam^6 + b*lam^4 - lam^2)*hk2 + (a^2*lam^7 - a^2*lam^5 - 2*a*b*lam^8 + 4*a*b*lam^6 - a*b*lam^4 + b^2*lam^9 - 3*b^2*lam^7 + 2*b^2*lam^5 - lam)*hk3 + (-a^3*lam^4 - a^3*lam^3 - 3*a^3*lam^2 - 4*a^3*lam - 11*a^3 + 3*a^2*b*lam^5 + 3*a^2*b*lam^4 + 6*a^2*b*lam^3 + 9*a^2*b*lam^2 + 22*a^2*b*lam + 34*a^2*b - a^2*lam - a^2 - 3*a*b^2*lam^6 - 3*a*b^2*lam^5 - 3*a*b^2*lam^4 - 6*a*b^2*lam^3 - 14*a*b^2*lam^2 - 23*a*b^2*lam - 52*a*b^2 + 2*a*b*lam^2 + 2*a*b*lam + 8*a*b + b^3*lam^7 + b^3*lam^6 + b^3*lam^4 + 3*b^3*lam^3 + 5*b^3*lam^2 + 11*b^3*lam + 19*b^3 - b^2*lam^3 - b^2*lam^2 - 3*b^2*lam - 4*b^2)*hps
    linarith [hr, he]
  have qq25 : (0:ℝ) ≤ -a^2*lam + a*b + a*lam - a + b^2*lam^3 + b^2*lam - b*lam^2 - b*lam - b + 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(b + c*lam - 1) := mul_nonneg reg0 reg1
    have he : (a + b*lam - 1)*(b + c*lam - 1) = -a^2*lam + a*b + a*lam - a + b^2*lam^3 + b^2*lam - b*lam^2 - b*lam - b + 1 := by linear_combination (a*lam + b*lam^2 - lam)*hk0
    linarith [hr, he]
  have qq26 : (0:ℝ) ≤ -a^2*lam^2 - a^2 - a*b*lam + a*lam^2 + b^2*lam^4 - b*lam^3 - b*lam + 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(c + d*lam - 1) := mul_nonneg reg0 reg2
    have he : (a + b*lam - 1)*(c + d*lam - 1) = -a^2*lam^2 - a^2 - a*b*lam + a*lam^2 + b^2*lam^4 - b*lam^3 - b*lam + 1 := by linear_combination (a*lam^2 + a + b*lam^3 + b*lam - lam^2 - 1)*hk0 + (a*lam + b*lam^2 - lam)*hk1
    linarith [hr, he]
  have qq27 : (0:ℝ) ≤ -2*a^2*lam - a*b + 2*a*lam - a + 2*b^2*lam^3 - b^2*lam - 2*b*lam^2 - b*lam + b + 1 := by
    have hr : (0:ℝ) ≤ (a + b*lam - 1)*(c*lam + d - 1) := mul_nonneg reg0 gen2
    have he : (a + b*lam - 1)*(c*lam + d - 1) = -2*a^2*lam - a*b + 2*a*lam - a + 2*b^2*lam^3 - b^2*lam - 2*b*lam^2 - b*lam + b + 1 := by linear_combination (2*a*lam + 2*b*lam^2 - 2*lam)*hk0 + (a + b*lam - 1)*hk1
    linarith [hr, he]
  have qq28 : (0:ℝ) ≤ a^2*lam^2 - 2*a*b*lam^3 - 2*a*b*lam + 2*a*lam + b^2*lam^4 + 2*b^2*lam^2 + b^2 - 2*b*lam^2 - 2*b + 1 := by
    have hr : (0:ℝ) ≤ (b + c*lam - 1)*(b + c*lam - 1) := mul_nonneg reg1 reg1
    have he : (b + c*lam - 1)*(b + c*lam - 1) = a^2*lam^2 - 2*a*b*lam^3 - 2*a*b*lam + 2*a*lam + b^2*lam^4 + 2*b^2*lam^2 + b^2 - 2*b*lam^2 - 2*b + 1 := by linear_combination (-a*lam^2 + b*lam^3 + 2*b*lam + c*lam^2 - 2*lam)*hk0
    linarith [hr, he]
  have qq29 : (0:ℝ) ≤ 2*a^2*lam^3 - a^2*lam - 4*a*b*lam^4 + 2*a*b*lam^2 + a*b + 2*a*lam^2 + a*lam - a + 2*b^2*lam^5 - b^2*lam^3 - 3*b^2*lam - 2*b*lam^3 - b*lam^2 + 3*b*lam - b + 1 := by
    have hr : (0:ℝ) ≤ (b + c*lam - 1)*(d*lam + e - 1) := mul_nonneg reg1 gen3
    have he : (b + c*lam - 1)*(d*lam + e - 1) = 2*a^2*lam^3 - a^2*lam - 4*a*b*lam^4 + 2*a*b*lam^2 + a*b + 2*a*lam^2 + a*lam - a + 2*b^2*lam^5 - b^2*lam^3 - 3*b^2*lam - 2*b*lam^3 - b*lam^2 + 3*b*lam - b + 1 := by linear_combination (-2*a*lam^3 + a*lam + 2*b*lam^4 + b*lam^2 - b + d*lam^2 + e*lam - 2*lam^2 - lam + 1)*hk0 + (-2*a*lam^2 + 2*b*lam^3 + 2*b*lam - 2*lam)*hk1 + (-a*lam + b*lam^2 + b - 1)*hk2
    linarith [hr, he]
  have qq30 : (0:ℝ) ≤ a^2*b*lam^4 - a*b^2*lam^5 - a*b^2*lam^3 + a*b*lam^3 - a*lam + b*lam^2 + b - 1 := by
    have hr : (0:ℝ) ≤ (b + c*lam - 1)*(-a*b*lam^3 + 1) := mul_nonneg reg1 slk0
    have he : (b + c*lam - 1)*(-a*b*lam^3 + 1) = a^2*b*lam^4 - a*b^2*lam^5 - a*b^2*lam^3 + a*b*lam^3 - a*lam + b*lam^2 + b - 1 := by linear_combination (-a*b*lam^4 + lam)*hk0
    linarith [hr, he]
  have qq31 : (0:ℝ) ≤ 2*a^2*lam^5 - a^2*lam^3 - 3*a^2*lam - 4*a*b*lam^5 - 14*a*b*lam^4 + 16*a*b*lam^3 + 28*a*b*lam^2 - 12*a*b*lam - 5*a*b + 2*a*lam^3 + a*lam^2 - 3*a*lam + a + 7*b^2*lam^5 + 2*b^2*lam^4 - 19*b^2*lam^3 - 6*b^2*lam^2 + 8*b^2*lam + 2*b^2 - 2*b*lam^4 - b*lam^3 + 5*b*lam^2 - b + 1 := by
    have hr : (0:ℝ) ≤ (c + d*lam - 1)*(e*lam + f - 1) := mul_nonneg reg2 gen4
    have he : (c + d*lam - 1)*(e*lam + f - 1) = 2*a^2*lam^5 - a^2*lam^3 - 3*a^2*lam - 4*a*b*lam^5 - 14*a*b*lam^4 + 16*a*b*lam^3 + 28*a*b*lam^2 - 12*a*b*lam - 5*a*b + 2*a*lam^3 + a*lam^2 - 3*a*lam + a + 7*b^2*lam^5 + 2*b^2*lam^4 - 19*b^2*lam^3 - 6*b^2*lam^2 + 8*b^2*lam + 2*b^2 - 2*b*lam^4 - b*lam^3 + 5*b*lam^2 - b + 1 := by linear_combination (-2*a*lam^5 + a*lam^3 + 3*a*lam + 2*b*lam^6 - 3*b*lam^4 + e*lam^3 + e*lam + f*lam^2 + f - 2*lam^3 - lam^2 + 3*lam - 1)*hk0 + (-2*a*lam^4 - a*lam^2 + a + 2*b*lam^5 - b*lam^3 + e*lam^2 + f*lam - 2*lam^2 - lam + 1)*hk1 + (-2*a*lam^3 - 2*a*lam + 2*b*lam^4 - 2*lam)*hk2 + (-a*lam^2 - a + b*lam^3 - 1)*hk3 + (-4*a*b + 2*b^2*lam + 2*b^2)*hps
    linarith [hr, he]
  have qq32 : (0:ℝ) ≤ a^2*b*lam^5 + a^2*b*lam^3 - a*b^2*lam^5 - 5*a*b^2*lam^4 + 4*a*b^2*lam^3 + 6*a*b^2*lam^2 - 3*a*b^2*lam - a*b^2 + a*b*lam^3 - a*lam^2 - a + b*lam^3 - 1 := by
    have hr : (0:ℝ) ≤ (c + d*lam - 1)*(-a*b*lam^3 + 1) := mul_nonneg reg2 slk0
    have he : (c + d*lam - 1)*(-a*b*lam^3 + 1) = a^2*b*lam^5 + a^2*b*lam^3 - a*b^2*lam^5 - 5*a*b^2*lam^4 + 4*a*b^2*lam^3 + 6*a*b^2*lam^2 - 3*a*b^2*lam - a*b^2 + a*b*lam^3 - a*lam^2 - a + b*lam^3 - 1 := by linear_combination (-a*b*lam^5 - a*b*lam^3 + lam^2 + 1)*hk0 + (-a*b*lam^4 + lam)*hk1 + (-a*b^2)*hps
    linarith [hr, he]
  have qq33 : (0:ℝ) ≤ 20*a^3*lam^5 + 32*a^3*lam^4 - 73*a^3*lam^3 - 65*a^3*lam^2 + 47*a^3*lam + 14*a^3 - 106*a^2*b*lam^5 - 62*a^2*b*lam^4 + 306*a^2*b*lam^3 + 165*a^2*b*lam^2 - 161*a^2*b*lam - 44*a^2*b + 4*a^2*lam^5 + 7*a^2*lam^4 - 15*a^2*lam^3 - 14*a^2*lam^2 + 10*a^2*lam + 3*a^2 + 116*a*b^2*lam^5 + 143*a*b^2*lam^4 - 400*a*b^2*lam^3 - 308*a*b^2*lam^2 + 241*a*b^2*lam + 70*a*b^2 - 14*a*b*lam^5 - 8*a*b*lam^4 + 41*a*b*lam^3 + 22*a*b*lam^2 - 22*a*b*lam - 6*a*b - a*lam^2 - a - 56*b^3*lam^5 - 42*b^3*lam^4 + 169*b^3*lam^3 + 104*b^3*lam^2 - 93*b^3*lam - 26*b^3 + 7*b^2*lam^5 + 8*b^2*lam^4 - 24*b^2*lam^3 - 17*b^2*lam^2 + 14*b^2*lam + 4*b^2 + b*lam^3 - 1 := by
    have hr : (0:ℝ) ≤ (c + d*lam - 1)*(-e*f*lam^3 + 1) := mul_nonneg reg2 slk4
    have he : (c + d*lam - 1)*(-e*f*lam^3 + 1) = 20*a^3*lam^5 + 32*a^3*lam^4 - 73*a^3*lam^3 - 65*a^3*lam^2 + 47*a^3*lam + 14*a^3 - 106*a^2*b*lam^5 - 62*a^2*b*lam^4 + 306*a^2*b*lam^3 + 165*a^2*b*lam^2 - 161*a^2*b*lam - 44*a^2*b + 4*a^2*lam^5 + 7*a^2*lam^4 - 15*a^2*lam^3 - 14*a^2*lam^2 + 10*a^2*lam + 3*a^2 + 116*a*b^2*lam^5 + 143*a*b^2*lam^4 - 400*a*b^2*lam^3 - 308*a*b^2*lam^2 + 241*a*b^2*lam + 70*a*b^2 - 14*a*b*lam^5 - 8*a*b*lam^4 + 41*a*b*lam^3 + 22*a*b*lam^2 - 22*a*b*lam - 6*a*b - a*lam^2 - a - 56*b^3*lam^5 - 42*b^3*lam^4 + 169*b^3*lam^3 + 104*b^3*lam^2 - 93*b^3*lam - 26*b^3 + 7*b^2*lam^5 + 8*b^2*lam^4 - 24*b^2*lam^3 - 17*b^2*lam^2 + 14*b^2*lam + 4*b^2 + b*lam^3 - 1 := by linear_combination (-a^2*lam^10 + 2*a^2*lam^8 + a^2*lam^6 - 2*a^2*lam^4 + 2*a*b*lam^11 - 6*a*b*lam^9 + 2*a*b*lam^7 + 4*a*b*lam^5 + a*f*lam^7 - a*f*lam^3 - a*lam^8 + 3*a*lam^6 - 2*a*lam^4 - b^2*lam^12 + 4*b^2*lam^10 - 4*b^2*lam^8 - b*f*lam^8 + b*f*lam^6 + b*lam^9 - 4*b*lam^7 + 4*b*lam^5 - e*f*lam^5 - e*f*lam^3 + f*lam^5 - f*lam^3 + lam^2 + 1)*hk0 + (-a^2*lam^9 + a^2*lam^7 + a^2*lam^5 - a^2*lam^3 + 2*a*b*lam^10 - 4*a*b*lam^8 + 2*a*b*lam^4 + a*f*lam^6 + a*f*lam^4 - a*lam^7 + 2*a*lam^5 - a*lam^3 - b^2*lam^11 + 3*b^2*lam^9 - 2*b^2*lam^7 - b*f*lam^7 + b*lam^8 - 3*b*lam^6 + 2*b*lam^4 - e*f*lam^4 + f*lam^4 + lam)*hk1 + (-a^2*lam^8 + a^2*lam^4 + 2*a*b*lam^9 - 2*a*b*lam^7 - 2*a*b*lam^5 + a*f*lam^5 + a*f*lam^3 - a*lam^6 + a*lam^4 - b^2*lam^10 + 2*b^2*lam^8 - b*f*lam^6 + b*lam^7 - 2*b*lam^5 + f*lam^3)*hk2 + (-a^2*lam^7 + a^2*lam^3 + 2*a*b*lam^8 - 2*a*b*lam^6 - 2*a*b*lam^4 - a*lam^5 + a*lam^3 - b^2*lam^9 + 2*b^2*lam^7 + b*lam^6 - 2*b*lam^4)*hk3 + (a^3*lam^4 + a^3*lam^3 + 4*a^3*lam^2 + 5*a^3*lam + 14*a^3 - 3*a^2*b*lam^5 - 3*a^2*b*lam^4 - 9*a^2*b*lam^3 - 12*a^2*b*lam^2 - 29*a^2*b*lam - 44*a^2*b + a^2*lam^2 + a^2*lam + 3*a^2 + 3*a*b^2*lam^6 + 3*a*b^2*lam^5 + 6*a*b^2*lam^4 + 9*a*b^2*lam^3 + 19*a*b^2*lam^2 + 31*a*b^2*lam + 70*a*b^2 - 2*a*b*lam^3 - 2*a*b*lam^2 - 4*a*b*lam - 6*a*b - b^3*lam^7 - b^3*lam^6 - b^3*lam^5 - 2*b^3*lam^4 - 4*b^3*lam^3 - 7*b^3*lam^2 - 15*b^3*lam - 26*b^3 + b^2*lam^4 + b^2*lam^3 + b^2*lam^2 + 2*b^2*lam + 4*b^2)*hps
    linarith [hr, he]
  have qq34 : (0:ℝ) ≤ 6*a^3*lam^5 + a^3*lam^4 - 10*a^3*lam^3 - 3*a^3*lam^2 + 4*a^3*lam + a^3 - 19*a^2*b*lam^5 - 49*a^2*b*lam^4 + 73*a^2*b*lam^3 + 84*a^2*b*lam^2 - 51*a^2*b*lam - 16*a^2*b + a^2*lam^4 + 56*a*b^2*lam^5 + 20*a*b^2*lam^4 - 139*a*b^2*lam^3 - 57*a*b^2*lam^2 + 65*a*b^2*lam + 17*a*b^2 - 2*a*b*lam^5 + a*b*lam^3 - a*lam^3 - 21*b^3*lam^5 - 36*b^3*lam^4 + 77*b^3*lam^3 + 71*b^3*lam^2 - 50*b^3*lam - 15*b^3 + b^2*lam^5 + 4*b^2*lam^4 - 4*b^2*lam^3 - 6*b^2*lam^2 + 3*b^2*lam + b^2 + b*lam^4 - b*lam^2 - b - 1 := by
    have hr : (0:ℝ) ≤ (d + e*lam - 1)*(-c*d*lam^3 + 1) := mul_nonneg reg3 slk2
    have he : (d + e*lam - 1)*(-c*d*lam^3 + 1) = 6*a^3*lam^5 + a^3*lam^4 - 10*a^3*lam^3 - 3*a^3*lam^2 + 4*a^3*lam + a^3 - 19*a^2*b*lam^5 - 49*a^2*b*lam^4 + 73*a^2*b*lam^3 + 84*a^2*b*lam^2 - 51*a^2*b*lam - 16*a^2*b + a^2*lam^4 + 56*a*b^2*lam^5 + 20*a*b^2*lam^4 - 139*a*b^2*lam^3 - 57*a*b^2*lam^2 + 65*a*b^2*lam + 17*a*b^2 - 2*a*b*lam^5 + a*b*lam^3 - a*lam^3 - 21*b^3*lam^5 - 36*b^3*lam^4 + 77*b^3*lam^3 + 71*b^3*lam^2 - 50*b^3*lam - 15*b^3 + b^2*lam^5 + 4*b^2*lam^4 - 4*b^2*lam^3 - 6*b^2*lam^2 + 3*b^2*lam + b^2 + b*lam^4 - b*lam^2 - b - 1 := by linear_combination (-a^2*lam^7 + 2*a*b*lam^8 - a*b*lam^6 + a*d*lam^4 + a*e*lam^5 - a*lam^4 - b^2*lam^9 + b^2*lam^7 - b*d*lam^5 - b*e*lam^6 + b*lam^5 - d^2*lam^3 - d*e*lam^4 + d*lam^3 + lam^3)*hk0 + (-a^2*lam^6 - a^2*lam^4 + 2*a*b*lam^7 + a*b*lam^5 - a*b*lam^3 + a*d*lam^3 + a*e*lam^4 - a*lam^3 - b^2*lam^8 + b^2*lam^4 - b*d*lam^4 - b*e*lam^5 + b*lam^4 + lam^2 + 1)*hk1 + (-a^2*lam^5 + 2*a*b*lam^6 - a*b*lam^4 - b^2*lam^7 + b^2*lam^5 + lam)*hk2 + (a^3*lam + a^3 - 3*a^2*b*lam^2 - 3*a^2*b*lam - 16*a^2*b + 3*a*b^2*lam^3 + 3*a*b^2*lam^2 + 14*a*b^2*lam + 17*a*b^2 - b^3*lam^4 - b^3*lam^3 - 4*b^3*lam^2 - 5*b^3*lam - 15*b^3 + b^2)*hps
    linarith [hr, he]
  have qq35 : (0:ℝ) ≤ 14*a^2*lam^5 + 6*a^2*lam^4 - 38*a^2*lam^3 - 17*a^2*lam^2 + 20*a^2*lam + 5*a^2 - 28*a*b*lam^5 - 36*a*b*lam^4 + 100*a*b*lam^3 + 76*a*b*lam^2 - 62*a*b*lam - 18*a*b + 2*a*lam^5 - 2*a*lam^3 - 2*a*lam + 18*b^2*lam^5 + 14*b^2*lam^4 - 54*b^2*lam^3 - 36*b^2*lam^2 + 32*b^2*lam + 9*b^2 - 2*b*lam^5 - 6*b*lam^4 + 8*b*lam^3 + 14*b*lam^2 - 6*b*lam - 2*b + lam := by
    have hr : (0:ℝ) ≤ lam*((e + f*lam - 1)*(e + f*lam - 1)) := mul_nonneg hpos.le (mul_nonneg reg4 reg4)
    have he : lam*((e + f*lam - 1)*(e + f*lam - 1)) = 14*a^2*lam^5 + 6*a^2*lam^4 - 38*a^2*lam^3 - 17*a^2*lam^2 + 20*a^2*lam + 5*a^2 - 28*a*b*lam^5 - 36*a*b*lam^4 + 100*a*b*lam^3 + 76*a*b*lam^2 - 62*a*b*lam - 18*a*b + 2*a*lam^5 - 2*a*lam^3 - 2*a*lam + 18*b^2*lam^5 + 14*b^2*lam^4 - 54*b^2*lam^3 - 36*b^2*lam^2 + 32*b^2*lam + 9*b^2 - 2*b*lam^5 - 6*b*lam^4 + 8*b*lam^3 + 14*b*lam^2 - 6*b*lam - 2*b + lam := by linear_combination (-a*lam^9 + 2*a*lam^7 + a*lam^5 - 2*a*lam^3 - a*lam + b*lam^10 - 3*b*lam^8 + 3*b*lam^4 + 2*b*lam^2 + e*lam^3 - e*lam + f*lam^6 - 2*f*lam^2 - 2*lam^5 + 2*lam^3 + 2*lam)*hk0 + (-a*lam^8 + a*lam^6 + a*lam^4 - a*lam^2 + b*lam^9 - 2*b*lam^7 - b*lam^5 + b*lam^3 + e*lam^2 + f*lam^5 + f*lam^3 - 2*lam^4)*hk1 + (-a*lam^7 + a*lam^3 + a*lam + b*lam^8 - b*lam^6 - 2*b*lam^4 - 2*b*lam^2 + e*lam + f*lam^4 + 2*f*lam^2 - 2*lam^3 - 2*lam)*hk2 + (-a*lam^6 + 2*a*lam^2 + b*lam^7 - b*lam^5 - 3*b*lam^3 + f*lam^3 - 2*lam^2)*hk3 + (a^2*lam^3 + a^2*lam^2 + 4*a^2*lam + 5*a^2 - 2*a*b*lam^4 - 2*a*b*lam^3 - 6*a*b*lam^2 - 8*a*b*lam - 18*a*b + b^2*lam^5 + b^2*lam^4 + 2*b^2*lam^3 + 3*b^2*lam^2 + 5*b^2*lam + 9*b^2 - 2*b)*hps
    linarith [hr, he]
  have qq36 : (0:ℝ) ≤ -a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 7*a^2*lam^2 - 3*a^2*lam - a^2 + 3*a*b*lam^5 + a*b*lam^4 - 10*a*b*lam^3 - 3*a*b*lam^2 + 5*a*b*lam + a*b + a*lam^5 - a*lam^3 - a*lam^2 - a*lam + b^2*lam^5 + 3*b^2*lam^4 - 4*b^2*lam^3 - 7*b^2*lam^2 + 3*b^2*lam + b^2 - b*lam^5 - 3*b*lam^4 + 4*b*lam^3 + 7*b*lam^2 - 4*b*lam - b + lam := by
    have hr : (0:ℝ) ≤ lam*((e + f*lam - 1)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg reg4 gen0)
    have he : lam*((e + f*lam - 1)*(a*lam + b - 1)) = -a^2*lam^5 - 4*a^2*lam^4 + 4*a^2*lam^3 + 7*a^2*lam^2 - 3*a^2*lam - a^2 + 3*a*b*lam^5 + a*b*lam^4 - 10*a*b*lam^3 - 3*a*b*lam^2 + 5*a*b*lam + a*b + a*lam^5 - a*lam^3 - a*lam^2 - a*lam + b^2*lam^5 + 3*b^2*lam^4 - 4*b^2*lam^3 - 7*b^2*lam^2 + 3*b^2*lam + b^2 - b*lam^5 - 3*b*lam^4 + 4*b*lam^3 + 7*b*lam^2 - 4*b*lam - b + lam := by linear_combination (a*lam^6 - a*lam^4 - a*lam^2 + b*lam^5 - b*lam^3 - b*lam - lam^5 + lam^3 + lam)*hk0 + (a*lam^5 + b*lam^4 - lam^4)*hk1 + (a*lam^4 + a*lam^2 + b*lam^3 + b*lam - lam^3 - lam)*hk2 + (a*lam^3 + b*lam^2 - lam^2)*hk3 + (-a^2 + a*b*lam + a*b + b^2 - b)*hps
    linarith [hr, he]
  have qq37 : (0:ℝ) ≤ 6*a^3*lam^5 + 14*a^3*lam^4 - 23*a^3*lam^3 - 26*a^3*lam^2 + 16*a^3*lam + 5*a^3 - 49*a^2*b*lam^5 - 19*a^2*b*lam^4 + 129*a^2*b*lam^3 + 54*a^2*b*lam^2 - 61*a^2*b*lam - 16*a^2*b + a^2*lam^4 + 56*a*b^2*lam^5 + 87*a*b^2*lam^4 - 204*a*b^2*lam^3 - 181*a*b^2*lam^2 + 131*a*b^2*lam + 39*a*b^2 - 2*a*b*lam^5 + a*b*lam^3 - a*lam^4 + a*lam^2 + a - 36*b^3*lam^5 - 21*b^3*lam^4 + 105*b^3*lam^3 + 56*b^3*lam^2 - 55*b^3*lam - 15*b^3 + b^2*lam^5 + 4*b^2*lam^4 - 4*b^2*lam^3 - 6*b^2*lam^2 + 3*b^2*lam + b^2 + b*lam^5 - 2*b*lam^3 - b*lam - 1 := by
    have hr : (0:ℝ) ≤ (e + f*lam - 1)*(-c*d*lam^3 + 1) := mul_nonneg reg4 slk2
    have he : (e + f*lam - 1)*(-c*d*lam^3 + 1) = 6*a^3*lam^5 + 14*a^3*lam^4 - 23*a^3*lam^3 - 26*a^3*lam^2 + 16*a^3*lam + 5*a^3 - 49*a^2*b*lam^5 - 19*a^2*b*lam^4 + 129*a^2*b*lam^3 + 54*a^2*b*lam^2 - 61*a^2*b*lam - 16*a^2*b + a^2*lam^4 + 56*a*b^2*lam^5 + 87*a*b^2*lam^4 - 204*a*b^2*lam^3 - 181*a*b^2*lam^2 + 131*a*b^2*lam + 39*a*b^2 - 2*a*b*lam^5 + a*b*lam^3 - a*lam^4 + a*lam^2 + a - 36*b^3*lam^5 - 21*b^3*lam^4 + 105*b^3*lam^3 + 56*b^3*lam^2 - 55*b^3*lam - 15*b^3 + b^2*lam^5 + 4*b^2*lam^4 - 4*b^2*lam^3 - 6*b^2*lam^2 + 3*b^2*lam + b^2 + b*lam^5 - 2*b*lam^3 - b*lam - 1 := by linear_combination (-a^2*lam^8 + a^2*lam^6 + a^2*lam^4 + 2*a*b*lam^9 - 3*a*b*lam^7 - a*b*lam^5 + a*b*lam^3 + a*e*lam^4 + a*f*lam^5 - a*lam^4 - b^2*lam^10 + 2*b^2*lam^8 - b^2*lam^4 - b*e*lam^5 - b*f*lam^6 + b*lam^5 - d*e*lam^3 - d*f*lam^4 + d*lam^3 + lam^4 - lam^2 - 1)*hk0 + (-a^2*lam^7 + 2*a*b*lam^8 - a*b*lam^6 + a*e*lam^3 + a*f*lam^4 - a*lam^3 - b^2*lam^9 + b^2*lam^7 - b*e*lam^4 - b*f*lam^5 + b*lam^4 + lam^3)*hk1 + (-a^2*lam^6 - a^2*lam^4 + 2*a*b*lam^7 + a*b*lam^5 - a*b*lam^3 - b^2*lam^8 + b^2*lam^4 + lam^2 + 1)*hk2 + (-a^2*lam^5 + 2*a*b*lam^6 - a*b*lam^4 - b^2*lam^7 + b^2*lam^5 + lam)*hk3 + (a^3*lam^2 + a^3*lam + 5*a^3 - 3*a^2*b*lam^3 - 3*a^2*b*lam^2 - 13*a^2*b*lam - 16*a^2*b + 3*a*b^2*lam^4 + 3*a*b^2*lam^3 + 11*a*b^2*lam^2 + 14*a*b^2*lam + 39*a*b^2 - b^3*lam^5 - b^3*lam^4 - 3*b^3*lam^3 - 4*b^3*lam^2 - 10*b^3*lam - 15*b^3 + b^2)*hps
    linarith [hr, he]
  have qq38 : (0:ℝ) ≤ a^2*lam^3 + 2*a*b*lam^2 - 2*a*lam^2 + b^2*lam - 2*b*lam + lam := by
    have hr : (0:ℝ) ≤ lam*((a*lam + b - 1)*(a*lam + b - 1)) := mul_nonneg hpos.le (mul_nonneg gen0 gen0)
    have he : lam*((a*lam + b - 1)*(a*lam + b - 1)) = a^2*lam^3 + 2*a*b*lam^2 - 2*a*lam^2 + b^2*lam - 2*b*lam + lam := by linear_combination 0
    linarith [hr, he]
  have qq39 : (0:ℝ) ≤ -a^3*lam^5 + 2*a^2*b*lam^5 + 8*a^2*b*lam^4 - 8*a^2*b*lam^3 - 12*a^2*b*lam^2 + 6*a^2*b*lam + 2*a^2*b + a^2*lam^4 - 3*a*b^2*lam^5 - a*b^2*lam^4 + 9*a*b^2*lam^3 + 3*a*b^2*lam^2 - 4*a*b^2*lam - a*b^2 - 2*a*b*lam^5 + a*b*lam^3 + a*lam - b^3*lam^5 - 4*b^3*lam^4 + 4*b^3*lam^3 + 6*b^3*lam^2 - 3*b^3*lam - b^3 + b^2*lam^5 + 4*b^2*lam^4 - 4*b^2*lam^3 - 6*b^2*lam^2 + 3*b^2*lam + b^2 + b - 1 := by
    have hr : (0:ℝ) ≤ (a*lam + b - 1)*(-c*d*lam^3 + 1) := mul_nonneg gen0 slk2
    have he : (a*lam + b - 1)*(-c*d*lam^3 + 1) = -a^3*lam^5 + 2*a^2*b*lam^5 + 8*a^2*b*lam^4 - 8*a^2*b*lam^3 - 12*a^2*b*lam^2 + 6*a^2*b*lam + 2*a^2*b + a^2*lam^4 - 3*a*b^2*lam^5 - a*b^2*lam^4 + 9*a*b^2*lam^3 + 3*a*b^2*lam^2 - 4*a*b^2*lam - a*b^2 - 2*a*b*lam^5 + a*b*lam^3 + a*lam - b^3*lam^5 - 4*b^3*lam^4 + 4*b^3*lam^3 + 6*b^3*lam^2 - 3*b^3*lam - b^3 + b^2*lam^5 + 4*b^2*lam^4 - 4*b^2*lam^3 - 6*b^2*lam^2 + 3*b^2*lam + b^2 + b - 1 := by linear_combination (a^2*lam^5 - a*b*lam^6 + a*b*lam^4 - a*d*lam^4 - a*lam^4 - b^2*lam^5 - b*d*lam^3 + b*lam^5 + d*lam^3)*hk0 + (a^2*lam^4 - a*b*lam^5 + a*b*lam^3 - a*lam^3 - b^2*lam^4 + b*lam^4)*hk1 + (2*a^2*b - a*b^2*lam - a*b^2 - b^3 + b^2)*hps
    linarith [hr, he]
  have qq40 : (0:ℝ) ≤ a^3*lam^4 - 4*a^2*b*lam^5 + a^2*b*lam^3 + a^2*lam^4 + 5*a*b^2*lam^5 + 22*a*b^2*lam^4 - 20*a*b^2*lam^3 - 30*a*b^2*lam^2 + 15*a*b^2*lam + 5*a*b^2 - 2*a*b*lam^5 + a*b*lam^3 - a - 10*b^3*lam^5 - 2*b^3*lam^4 + 20*b^3*lam^3 + 6*b^3*lam^2 - 8*b^3*lam - 2*b^3 + b^2*lam^5 + 4*b^2*lam^4 - 4*b^2*lam^3 - 6*b^2*lam^2 + 3*b^2*lam + b^2 + 2*b*lam - 1 := by
    have hr : (0:ℝ) ≤ (b*lam + c - 1)*(-c*d*lam^3 + 1) := mul_nonneg gen1 slk2
    have he : (b*lam + c - 1)*(-c*d*lam^3 + 1) = a^3*lam^4 - 4*a^2*b*lam^5 + a^2*b*lam^3 + a^2*lam^4 + 5*a*b^2*lam^5 + 22*a*b^2*lam^4 - 20*a*b^2*lam^3 - 30*a*b^2*lam^2 + 15*a*b^2*lam + 5*a*b^2 - 2*a*b*lam^5 + a*b*lam^3 - a - 10*b^3*lam^5 - 2*b^3*lam^4 + 20*b^3*lam^3 + 6*b^3*lam^2 - 8*b^3*lam - 2*b^3 + b^2*lam^5 + 4*b^2*lam^4 - 4*b^2*lam^3 - 6*b^2*lam^2 + 3*b^2*lam + b^2 + 2*b*lam - 1 := by linear_combination (-a^2*lam^4 + 3*a*b*lam^5 + a*d*lam^3 - a*lam^4 - 2*b^2*lam^6 - 2*b*d*lam^4 + b*lam^5 - c*d*lam^3 + d*lam^3 + 1)*hk0 + (-a^2*lam^3 + 3*a*b*lam^4 - a*lam^3 - 2*b^2*lam^5 + b*lam^4)*hk1 + (5*a*b^2 - 2*b^3*lam - 2*b^3 + b^2)*hps
    linarith [hr, he]
  have qq41 : (0:ℝ) ≤ 4*a^2*lam^4 - 6*a^2*lam^2 - 8*a*b*lam^5 + 18*a*b*lam^3 - 5*a*b*lam + 2*a*lam^3 - a*lam + 4*b^2*lam^5 + 8*b^2*lam^4 - 16*b^2*lam^3 - 17*b^2*lam^2 + 12*b^2*lam + 3*b^2 - 2*b*lam^4 + 3*b*lam^2 + 1 := by
    have hr : (0:ℝ) ≤ (c*lam + d - 1)*(e*lam + f - 1) := mul_nonneg gen2 gen4
    have he : (c*lam + d - 1)*(e*lam + f - 1) = 4*a^2*lam^4 - 6*a^2*lam^2 - 8*a*b*lam^5 + 18*a*b*lam^3 - 5*a*b*lam + 2*a*lam^3 - a*lam + 4*b^2*lam^5 + 8*b^2*lam^4 - 16*b^2*lam^3 - 17*b^2*lam^2 + 12*b^2*lam + 3*b^2 - 2*b*lam^4 + 3*b*lam^2 + 1 := by linear_combination (-4*a*lam^4 + 6*a*lam^2 + 4*b*lam^5 - 8*b*lam^3 + 3*b*lam + 2*e*lam^2 + 2*f*lam - 2*lam^3 + lam)*hk0 + (-4*a*lam^3 + 2*a*lam + 4*b*lam^4 - 4*b*lam^2 + b + e*lam + f - 2*lam^2)*hk1 + (-4*a*lam^2 + 4*b*lam^3 - 2*b*lam - 2*lam)*hk2 + (-2*a*lam + 2*b*lam^2 - b - 1)*hk3 + (4*b^2)*hps
    linarith [hr, he]
  have qq42 : (0:ℝ) ≤ 2*a^2*b*lam^4 - 2*a*b^2*lam^5 + a*b^2*lam^3 + a*b*lam^3 - 2*a*lam + 2*b*lam^2 - b - 1 := by
    have hr : (0:ℝ) ≤ (c*lam + d - 1)*(-a*b*lam^3 + 1) := mul_nonneg gen2 slk0
    have he : (c*lam + d - 1)*(-a*b*lam^3 + 1) = 2*a^2*b*lam^4 - 2*a*b^2*lam^5 + a*b^2*lam^3 + a*b*lam^3 - 2*a*lam + 2*b*lam^2 - b - 1 := by linear_combination (-2*a*b*lam^4 + 2*lam)*hk0 + (-a*b*lam^3 + 1)*hk1
    linarith [hr, he]
  have qq43 : (0:ℝ) ≤ 22*a^3*lam^5 + 10*a^3*lam^4 - 60*a^3*lam^3 - 28*a^3*lam^2 + 30*a^3*lam + 8*a^3 - 72*a^2*b*lam^5 - 101*a^2*b*lam^4 + 257*a^2*b*lam^3 + 212*a^2*b*lam^2 - 160*a^2*b*lam - 47*a^2*b + 4*a^2*lam^5 + 7*a^2*lam^4 - 15*a^2*lam^3 - 14*a^2*lam^2 + 10*a^2*lam + 3*a^2 + 118*a*b^2*lam^5 + 78*a*b^2*lam^4 - 349*a*b^2*lam^3 - 202*a*b^2*lam^2 + 188*a*b^2*lam + 52*a*b^2 - 14*a*b*lam^5 - 8*a*b*lam^4 + 41*a*b*lam^3 + 22*a*b*lam^2 - 22*a*b*lam - 6*a*b - 2*a*lam - 45*b^3*lam^5 - 52*b^3*lam^4 + 152*b^3*lam^3 + 113*b^3*lam^2 - 90*b^3*lam - 26*b^3 + 7*b^2*lam^5 + 8*b^2*lam^4 - 24*b^2*lam^3 - 17*b^2*lam^2 + 14*b^2*lam + 4*b^2 + 2*b*lam^2 - b - 1 := by
    have hr : (0:ℝ) ≤ (c*lam + d - 1)*(-e*f*lam^3 + 1) := mul_nonneg gen2 slk4
    have he : (c*lam + d - 1)*(-e*f*lam^3 + 1) = 22*a^3*lam^5 + 10*a^3*lam^4 - 60*a^3*lam^3 - 28*a^3*lam^2 + 30*a^3*lam + 8*a^3 - 72*a^2*b*lam^5 - 101*a^2*b*lam^4 + 257*a^2*b*lam^3 + 212*a^2*b*lam^2 - 160*a^2*b*lam - 47*a^2*b + 4*a^2*lam^5 + 7*a^2*lam^4 - 15*a^2*lam^3 - 14*a^2*lam^2 + 10*a^2*lam + 3*a^2 + 118*a*b^2*lam^5 + 78*a*b^2*lam^4 - 349*a*b^2*lam^3 - 202*a*b^2*lam^2 + 188*a*b^2*lam + 52*a*b^2 - 14*a*b*lam^5 - 8*a*b*lam^4 + 41*a*b*lam^3 + 22*a*b*lam^2 - 22*a*b*lam - 6*a*b - 2*a*lam - 45*b^3*lam^5 - 52*b^3*lam^4 + 152*b^3*lam^3 + 113*b^3*lam^2 - 90*b^3*lam - 26*b^3 + 7*b^2*lam^5 + 8*b^2*lam^4 - 24*b^2*lam^3 - 17*b^2*lam^2 + 14*b^2*lam + 4*b^2 + 2*b*lam^2 - b - 1 := by linear_combination (-2*a^2*lam^9 + 6*a^2*lam^7 - 4*a^2*lam^5 + 4*a*b*lam^10 - 15*a*b*lam^8 + 15*a*b*lam^6 - 2*a*b*lam^4 + 2*a*f*lam^6 - 2*a*f*lam^4 - a*lam^8 + 3*a*lam^6 - 2*a*lam^4 - 2*b^2*lam^11 + 9*b^2*lam^9 - 12*b^2*lam^7 + 4*b^2*lam^5 - 2*b*f*lam^7 + 3*b*f*lam^5 - b*f*lam^3 + b*lam^9 - 4*b*lam^7 + 4*b*lam^5 - 2*e*f*lam^4 + f*lam^5 - f*lam^3 + 2*lam)*hk0 + (-2*a^2*lam^8 + 4*a^2*lam^6 - 2*a^2*lam^4 + 4*a*b*lam^9 - 11*a*b*lam^7 + 8*a*b*lam^5 - a*b*lam^3 + 2*a*f*lam^5 - a*lam^7 + 2*a*lam^5 - a*lam^3 - 2*b^2*lam^10 + 7*b^2*lam^8 - 7*b^2*lam^6 + 2*b^2*lam^4 - 2*b*f*lam^6 + b*f*lam^4 + b*lam^8 - 3*b*lam^6 + 2*b*lam^4 - e*f*lam^3 + f*lam^4 + 1)*hk1 + (-2*a^2*lam^7 + 2*a^2*lam^5 + 4*a*b*lam^8 - 7*a*b*lam^6 + a*b*lam^4 + 2*a*f*lam^4 - a*lam^6 + a*lam^4 - 2*b^2*lam^9 + 5*b^2*lam^7 - 2*b^2*lam^5 - 2*b*f*lam^5 + b*f*lam^3 + b*lam^7 - 2*b*lam^5 + f*lam^3)*hk2 + (-2*a^2*lam^6 + 2*a^2*lam^4 + 4*a*b*lam^7 - 7*a*b*lam^5 + a*b*lam^3 - a*lam^5 + a*lam^3 - 2*b^2*lam^8 + 5*b^2*lam^6 - 2*b^2*lam^4 + b*lam^6 - 2*b*lam^4)*hk3 + (2*a^3*lam^3 + 2*a^3*lam^2 + 6*a^3*lam + 8*a^3 - 6*a^2*b*lam^4 - 6*a^2*b*lam^3 - 13*a^2*b*lam^2 - 19*a^2*b*lam - 47*a^2*b + a^2*lam^2 + a^2*lam + 3*a^2 + 6*a*b^2*lam^5 + 6*a*b^2*lam^4 + 8*a*b^2*lam^3 + 14*a*b^2*lam^2 + 32*a*b^2*lam + 52*a*b^2 - 2*a*b*lam^3 - 2*a*b*lam^2 - 4*a*b*lam - 6*a*b - 2*b^3*lam^6 - 2*b^3*lam^5 - b^3*lam^4 - 3*b^3*lam^3 - 7*b^3*lam^2 - 12*b^3*lam - 26*b^3 + b^2*lam^4 + b^2*lam^3 + b^2*lam^2 + 2*b^2*lam + 4*b^2)*hps
    linarith [hr, he]
  have qq44 : (0:ℝ) ≤ 4*a^2*lam^4 - 4*a^2*lam^2 + a^2 - 8*a*b*lam^5 + 16*a*b*lam^3 - 6*a*b*lam + 4*a*lam^2 - 2*a + 4*b^2*lam^5 + 8*b^2*lam^4 - 16*b^2*lam^3 - 15*b^2*lam^2 + 12*b^2*lam + 4*b^2 - 4*b*lam^3 + 6*b*lam + 1 := by
    have hr : (0:ℝ) ≤ (d*lam + e - 1)*(d*lam + e - 1) := mul_nonneg gen3 gen3
    have he : (d*lam + e - 1)*(d*lam + e - 1) = 4*a^2*lam^4 - 4*a^2*lam^2 + a^2 - 8*a*b*lam^5 + 16*a*b*lam^3 - 6*a*b*lam + 4*a*lam^2 - 2*a + 4*b^2*lam^5 + 8*b^2*lam^4 - 16*b^2*lam^3 - 15*b^2*lam^2 + 12*b^2*lam + 4*b^2 - 4*b*lam^3 + 6*b*lam + 1 := by linear_combination (-4*a*lam^4 + 4*a*lam^2 - a + 4*b*lam^5 - 8*b*lam^3 + 4*b*lam + d*lam^3 + 3*e*lam^2 - e - 4*lam^2 + 2)*hk0 + (-4*a*lam^3 + a*lam + 4*b*lam^4 - 5*b*lam^2 + d*lam^2 + 3*e*lam - 4*lam)*hk1 + (-3*a*lam^2 + a + 3*b*lam^3 - 4*b*lam + e - 2)*hk2 + (4*b^2)*hps
    linarith [hr, he]
  have qq45 : (0:ℝ) ≤ 4*a^2*lam^5 - 8*a^2*lam^3 + 3*a^2*lam - 8*a*b*lam^5 - 16*a*b*lam^4 + 32*a*b*lam^3 + 32*a*b*lam^2 - 24*a*b*lam - 7*a*b + 2*a*lam^3 + 2*a*lam^2 - 3*a*lam - a + 8*b^2*lam^5 + 4*b^2*lam^4 - 23*b^2*lam^3 - 12*b^2*lam^2 + 13*b^2*lam + 4*b^2 - 2*b*lam^4 - 2*b*lam^3 + 5*b*lam^2 + 3*b*lam - b + 1 := by
    have hr : (0:ℝ) ≤ (d*lam + e - 1)*(e*lam + f - 1) := mul_nonneg gen3 gen4
    have he : (d*lam + e - 1)*(e*lam + f - 1) = 4*a^2*lam^5 - 8*a^2*lam^3 + 3*a^2*lam - 8*a*b*lam^5 - 16*a*b*lam^4 + 32*a*b*lam^3 + 32*a*b*lam^2 - 24*a*b*lam - 7*a*b + 2*a*lam^3 + 2*a*lam^2 - 3*a*lam - a + 8*b^2*lam^5 + 4*b^2*lam^4 - 23*b^2*lam^3 - 12*b^2*lam^2 + 13*b^2*lam + 4*b^2 - 2*b*lam^4 - 2*b*lam^3 + 5*b*lam^2 + 3*b*lam - b + 1 := by linear_combination (-4*a*lam^5 + 8*a*lam^3 - 3*a*lam + 4*b*lam^6 - 12*b*lam^4 + 9*b*lam^2 + 2*e*lam^3 - e*lam + 2*f*lam^2 - f - 2*lam^3 - 2*lam^2 + 3*lam + 1)*hk0 + (-4*a*lam^4 + 4*a*lam^2 - a + 4*b*lam^5 - 8*b*lam^3 + 3*b*lam + 2*e*lam^2 + 2*f*lam - 2*lam^2 - 2*lam + 1)*hk1 + (-4*a*lam^3 + 2*a*lam + 4*b*lam^4 - 6*b*lam^2 + e*lam + f - 2*lam - 1)*hk2 + (-2*a*lam^2 + a + 2*b*lam^3 - 3*b*lam - 1)*hk3 + (-8*a*b + 4*b^2*lam + 4*b^2)*hps
    linarith [hr, he]
  have qq46 : (0:ℝ) ≤ 28*a^3*lam^5 + 43*a^3*lam^4 - 101*a^3*lam^3 - 88*a^3*lam^2 + 64*a^3*lam + 19*a^3 - 137*a^2*b*lam^5 - 85*a^2*b*lam^4 + 399*a^2*b*lam^3 + 222*a^2*b*lam^2 - 211*a^2*b*lam - 58*a^2*b + 4*a^2*lam^5 + 7*a^2*lam^4 - 15*a^2*lam^3 - 14*a^2*lam^2 + 10*a^2*lam + 3*a^2 + 145*a*b^2*lam^5 + 175*a*b^2*lam^4 - 494*a*b^2*lam^3 - 379*a*b^2*lam^2 + 296*a*b^2*lam + 86*a*b^2 - 14*a*b*lam^5 - 8*a*b*lam^4 + 41*a*b*lam^3 + 22*a*b*lam^2 - 22*a*b*lam - 6*a*b - 2*a*lam^2 + a - 67*b^3*lam^5 - 51*b^3*lam^4 + 203*b^3*lam^3 + 124*b^3*lam^2 - 111*b^3*lam - 31*b^3 + 7*b^2*lam^5 + 8*b^2*lam^4 - 24*b^2*lam^3 - 17*b^2*lam^2 + 14*b^2*lam + 4*b^2 + 2*b*lam^3 - 3*b*lam - 1 := by
    have hr : (0:ℝ) ≤ (d*lam + e - 1)*(-e*f*lam^3 + 1) := mul_nonneg gen3 slk4
    have he : (d*lam + e - 1)*(-e*f*lam^3 + 1) = 28*a^3*lam^5 + 43*a^3*lam^4 - 101*a^3*lam^3 - 88*a^3*lam^2 + 64*a^3*lam + 19*a^3 - 137*a^2*b*lam^5 - 85*a^2*b*lam^4 + 399*a^2*b*lam^3 + 222*a^2*b*lam^2 - 211*a^2*b*lam - 58*a^2*b + 4*a^2*lam^5 + 7*a^2*lam^4 - 15*a^2*lam^3 - 14*a^2*lam^2 + 10*a^2*lam + 3*a^2 + 145*a*b^2*lam^5 + 175*a*b^2*lam^4 - 494*a*b^2*lam^3 - 379*a*b^2*lam^2 + 296*a*b^2*lam + 86*a*b^2 - 14*a*b*lam^5 - 8*a*b*lam^4 + 41*a*b*lam^3 + 22*a*b*lam^2 - 22*a*b*lam - 6*a*b - 2*a*lam^2 + a - 67*b^3*lam^5 - 51*b^3*lam^4 + 203*b^3*lam^3 + 124*b^3*lam^2 - 111*b^3*lam - 31*b^3 + 7*b^2*lam^5 + 8*b^2*lam^4 - 24*b^2*lam^3 - 17*b^2*lam^2 + 14*b^2*lam + 4*b^2 + 2*b*lam^3 - 3*b*lam - 1 := by linear_combination (-2*a^2*lam^10 + 7*a^2*lam^8 - 7*a^2*lam^6 + 2*a^2*lam^4 + 4*a*b*lam^11 - 18*a*b*lam^9 + 25*a*b*lam^7 - 10*a*b*lam^5 + 2*a*f*lam^7 - 3*a*f*lam^5 + a*f*lam^3 - a*lam^8 + 3*a*lam^6 - 2*a*lam^4 - 2*b^2*lam^12 + 11*b^2*lam^10 - 20*b^2*lam^8 + 12*b^2*lam^6 - 2*b*f*lam^8 + 5*b*f*lam^6 - 3*b*f*lam^4 + b*lam^9 - 4*b*lam^7 + 4*b*lam^5 - 2*e*f*lam^5 + e*f*lam^3 + f*lam^5 - f*lam^3 + 2*lam^2 - 1)*hk0 + (-2*a^2*lam^9 + 5*a^2*lam^7 - 4*a^2*lam^5 + a^2*lam^3 + 4*a*b*lam^10 - 14*a*b*lam^8 + 15*a*b*lam^6 - 5*a*b*lam^4 + 2*a*f*lam^6 - a*f*lam^4 - a*lam^7 + 2*a*lam^5 - a*lam^3 - 2*b^2*lam^11 + 9*b^2*lam^9 - 13*b^2*lam^7 + 6*b^2*lam^5 - 2*b*f*lam^7 + 3*b*f*lam^5 + b*lam^8 - 3*b*lam^6 + 2*b*lam^4 - 2*e*f*lam^4 + f*lam^4 + 2*lam)*hk1 + (-2*a^2*lam^8 + 3*a^2*lam^6 - a^2*lam^4 + 4*a*b*lam^9 - 10*a*b*lam^7 + 5*a*b*lam^5 + 2*a*f*lam^5 - a*f*lam^3 - a*lam^6 + a*lam^4 - 2*b^2*lam^10 + 7*b^2*lam^8 - 6*b^2*lam^6 - 2*b*f*lam^6 + 3*b*f*lam^4 + b*lam^7 - 2*b*lam^5 - e*f*lam^3 + f*lam^3 + 1)*hk2 + (-2*a^2*lam^7 + 3*a^2*lam^5 - a^2*lam^3 + 4*a*b*lam^8 - 10*a*b*lam^6 + 5*a*b*lam^4 - a*lam^5 + a*lam^3 - 2*b^2*lam^9 + 7*b^2*lam^7 - 6*b^2*lam^5 + b*lam^6 - 2*b*lam^4)*hk3 + (2*a^3*lam^4 + 2*a^3*lam^3 + 5*a^3*lam^2 + 7*a^3*lam + 19*a^3 - 6*a^2*b*lam^5 - 6*a^2*b*lam^4 - 9*a^2*b*lam^3 - 15*a^2*b*lam^2 - 37*a^2*b*lam - 58*a^2*b + a^2*lam^2 + a^2*lam + 3*a^2 + 6*a*b^2*lam^6 + 6*a*b^2*lam^5 + 3*a*b^2*lam^4 + 9*a*b^2*lam^3 + 23*a*b^2*lam^2 + 38*a*b^2*lam + 86*a*b^2 - 2*a*b*lam^3 - 2*a*b*lam^2 - 4*a*b*lam - 6*a*b - 2*b^3*lam^7 - 2*b^3*lam^6 + b^3*lam^5 - b^3*lam^4 - 5*b^3*lam^3 - 8*b^3*lam^2 - 18*b^3*lam - 31*b^3 + b^2*lam^4 + b^2*lam^3 + b^2*lam^2 + 2*b^2*lam + 4*b^2)*hps
    linarith [hr, he]
  linarith [qq0, qq1, qq2, qq3, qq4, qq5, qq6, qq7, qq8, qq9, qq10, qq11, qq12, qq13, qq14, qq15, qq16, qq17, qq18, qq19, qq20, qq21, qq22, qq23, qq24, qq25, qq26, qq27, qq28, qq29, qq30, qq31, qq32, qq33, qq34, qq35, qq36, qq37, qq38, qq39, qq40, qq41, qq42, qq43, qq44, qq45, qq46, h2, h3]

/-- **q=13 window-5 core.** 6 coords of a genuine scalar orbit (both Taha edges + cap
+ 4 integer floors K_i>=1 with recurrence and floor-upper) cannot have all 5 products
`< 1/lam^3`.  Each interior floor is forced to 1 (floor-helper), reducing to the single
Chebyshev case `case_q13`. -/
theorem g13_core (a b c d e f lam : ℝ) (hps : lam^6 = lam^5 + 5*lam^4 - 4*lam^3 - 6*lam^2 + 3*lam + 1) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hlo : (9:ℝ)/5 < lam)
    (hpa : 0 < a) (hpb : 0 < b) (hpc : 0 < c) (hpd : 0 < d) (hpe : 0 < e) (hpf : 0 < f)
    (hca : a ≤ 1) (hcb : b ≤ 1) (hcc : c ≤ 1) (hcd : d ≤ 1) (hce : e ≤ 1) (hcf : f ≤ 1)
    (hr0 : a+lam*b > 1) (hr1 : b+lam*c > 1) (hr2 : c+lam*d > 1) (hr3 : d+lam*e > 1) (hr4 : e+lam*f > 1)
    (hg0 : lam*a+b > 1) (hg1 : lam*b+c > 1) (hg2 : lam*c+d > 1) (hg3 : lam*d+e > 1) (hg4 : lam*e+f > 1)
    (K0 K1 K2 K3 : ℤ)
    (hk0 : a+c = (K0:ℝ)*lam*b) (hk1 : b+d = (K1:ℝ)*lam*c) (hk2 : c+e = (K2:ℝ)*lam*d) (hk3 : d+f = (K3:ℝ)*lam*e)
    (hKge0 : 1 ≤ K0) (hKge1 : 1 ≤ K1) (hKge2 : 1 ≤ K2) (hKge3 : 1 ≤ K3)
    (hf0 : 1+a < ((K0:ℝ)+1)*(lam*b)) (hf1 : 1+b < ((K1:ℝ)+1)*(lam*c)) (hf2 : 1+c < ((K2:ℝ)+1)*(lam*d)) (hf3 : 1+d < ((K3:ℝ)+1)*(lam*e))
    (hP0 : a*b < 1/lam^3) (hP1 : b*c < 1/lam^3) (hP2 : c*d < 1/lam^3) (hP3 : d*e < 1/lam^3) (hP4 : e*f < 1/lam^3) :
    False := by
  have hpos : (0:ℝ) < lam := by linarith
  have hp3 : (0:ℝ) < lam^3 := by positivity
  have hp4nn : (0:ℝ) ≤ lam^4 := by positivity
  have hP0c : a*b*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP0
  have hP1c : b*c*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP1
  have hP2c : c*d*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP2
  have hP3c : d*e*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP3
  have hP4c : e*f*lam^3 < 1 := (lt_div_iff₀ hp3).mp hP4
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
  have hKr3 : (1:ℝ) ≤ (K3:ℝ) := by exact_mod_cast hKge3
  have heng3 : d*e + e*f = (K3:ℝ)*lam*e^2 := by linear_combination e*hk3
  have hK3b : (K3:ℝ)*lam^4*e^2 < 2 := by
    have h : (d*e+e*f)*lam^3 = (K3:ℝ)*lam^4*e^2 := by linear_combination lam^3*heng3
    nlinarith [hP3c, hP4c, h]
  have hbU3 : lam^4*e^2 < 2 := by
    have hn : (0:ℝ) ≤ lam^4*e^2 := mul_nonneg hp4nn (sq_nonneg _)
    nlinarith [hK3b, hKr3, mul_nonneg (by linarith : (0:ℝ) ≤ (K3:ℝ)-1) hn]
  have hKle0 : K0 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K0:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K0)
    have hn : (0:ℝ) ≤ lam^4*b^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*b^2 < 1 := by nlinarith [hK0b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K0:ℝ)-2) hn]
    exact g13_floor_helper lam b c h2 h3 hlo hpb hpc hms hbU1 (by linarith [hg1])
  have hKle1 : K1 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K1:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K1)
    have hn : (0:ℝ) ≤ lam^4*c^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*c^2 < 1 := by nlinarith [hK1b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K1:ℝ)-2) hn]
    exact g13_floor_helper lam c d h2 h3 hlo hpc hpd hms hbU2 (by linarith [hg2])
  have hKle2 : K2 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K2:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K2)
    have hn : (0:ℝ) ≤ lam^4*d^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*d^2 < 1 := by nlinarith [hK2b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K2:ℝ)-2) hn]
    exact g13_floor_helper lam d e h2 h3 hlo hpd hpe hms hbU3 (by linarith [hg3])
  have hKle3 : K3 ≤ 1 := by
    by_contra hcon; push_neg at hcon
    have h2K : (2:ℝ) ≤ (K3:ℝ) := by exact_mod_cast (by omega : (2:ℤ) ≤ K3)
    have hn : (0:ℝ) ≤ lam^4*e^2 := mul_nonneg hp4nn (sq_nonneg _)
    have hms : lam^4*e^2 < 1 := by nlinarith [hK3b, h2K, mul_nonneg (by linarith : (0:ℝ) ≤ (K3:ℝ)-2) hn]
    exact g13_floor_helper lam e d h2 h3 hlo hpe hpd hms hbU2 (by linarith [hr3])
  interval_cases K0 <;> interval_cases K1 <;> interval_cases K2 <;> interval_cases K3 <;>
    push_cast at hk0 hf0 hk1 hf1 hk2 hf2 hk3 hf3 <;>
    exact case_q13 a b c d e f lam hps h2 h3 hpa hpb hpc hpd hpe hpf hca hcb hcc hcd hce hcf hr0 hr1 hr2 hr3 hr4 hg0 hg1 hg2 hg3 hg4 hk0 hk1 hk2 hk3 hf0 hf1 hf2 hf3 hP0 hP1 hP2 hP3 hP4

/-- **q=13 window-5, orbit form.** Along any genuine scalar orbit (both Taha edges + cap +
genuine floor recurrence), no 5 consecutive products are all `< 1/lam^3`. -/
theorem g13_no_window_below_genuine
    (lam : ℝ) (hps : lam^6 = lam^5 + 5*lam^4 - 4*lam^3 - 6*lam^2 + 3*lam + 1) (h2 : (1:ℝ) < lam) (h3 : lam < 2)
    (hlo : (9:ℝ)/5 < lam)
    (c : ℕ → ℝ) (hposc : ∀ n, 0 < c n) (hcap : ∀ n, c n ≤ 1)
    (hreg : ∀ n, c n + lam * c (n+1) > 1) (hgen : ∀ n, lam * c n + c (n+1) > 1)
    (hrec : ∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) :
    ∀ i, ¬ (c (i+0) * c (i+1) < 1/lam^3 ∧
            c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3 ∧
            c (i+3) * c (i+4) < 1/lam^3 ∧
            c (i+4) * c (i+5) < 1/lam^3) := by
  have hpos' : 0 < lam := by linarith
  intro i hcon
  obtain ⟨hh0, hh1, hh2, hh3, hh4⟩ := hcon
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
  exact g13_core (c (i+0)) (c (i+1)) (c (i+2)) (c (i+3)) (c (i+4)) (c (i+5)) lam hps h2 h3 hlo
    (hposc (i+0)) (hposc (i+1)) (hposc (i+2)) (hposc (i+3)) (hposc (i+4)) (hposc (i+5))
    (hcap (i+0)) (hcap (i+1)) (hcap (i+2)) (hcap (i+3)) (hcap (i+4)) (hcap (i+5))
    (hreg (i+0)) (hreg (i+1)) (hreg (i+2)) (hreg (i+3)) (hreg (i+4))
    (hgen (i+0)) (hgen (i+1)) (hgen (i+2)) (hgen (i+3)) (hgen (i+4))
    (⌊(1 + c (i+0))/(lam*c (i+1))⌋) (⌊(1 + c (i+1))/(lam*c (i+2))⌋) (⌊(1 + c (i+2))/(lam*c (i+3))⌋) (⌊(1 + c (i+3))/(lam*c (i+4))⌋)
    (hrec (i+0)) (hrec (i+1)) (hrec (i+2)) (hrec (i+3))
    (flr (i+0)) (flr (i+1)) (flr (i+2)) (flr (i+3))
    (flrUB (i+0)) (flrUB (i+1)) (flrUB (i+2)) (flrUB (i+3))
    hh0 hh1 hh2 hh3 hh4

#print axioms g13_floor_helper
#print axioms case_q13
#print axioms g13_core
#print axioms g13_no_window_below_genuine