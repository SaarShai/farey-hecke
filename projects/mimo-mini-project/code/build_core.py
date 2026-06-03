#!/usr/bin/env python3
"""Assemble the full g5_core file: preamble + floor helper + 27 case lemmas + g5_core dispatch."""
import emit5, itertools, sys

PRE = r"""import Mathlib
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
"""

CORE_HEAD = r"""
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
"""

def dispatch():
    lines=["    first"]
    for K in itertools.product([1,2,3],repeat=3):
        nm=f"case{K[0]}{K[1]}{K[2]}"
        lines.append(f"    | exact {nm} a b c d e phi hps h2 h3 ha hbp hc hd he2 ha1 hb1 hc1 hd1 he1 "
                     f"hab hbc hcd hde hab' hbc' hcd' hde' hk0 hk1 hk2 hk0f hk1f hk2f hP0 hP1 hP2 hP3")
    return "\n".join(lines)

if __name__=='__main__':
    out=[PRE]
    for K in itertools.product([1,2,3],repeat=3):
        nm=f"case{K[0]}{K[1]}{K[2]}"
        out.append(emit5.emit(K,nm))
    out.append(CORE_HEAD + dispatch())
    open('/tmp/lean-minus1/G5CORE.lean','w').write("\n\n".join(out))
    print("written", sum(len(x.split(chr(10))) for x in out), "lines")
