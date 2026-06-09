/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ cluster ≤ 2 for the Hecke group G_6 (Taha BCZ map analogue), v12

## Goal

Prove `cluster_size_le_two_q6`: along the Taha G_6-BCZ orbit, three consecutive
points cannot all have the ergodic-opt observable `P < X(6) = √3/9 = 1/λ³` (λ=√3).
This is the third **arithmetic** Hecke case (q ∈ {3,4,6}); q=3 (v8) and q=4 (v11)
are already machine-proved.

## Geometry (Taha, arXiv:1810.10668, Thm 2.2; q=6, λ₆ = 2cos(π/6) = √3)

Special vectors `wᵢ = U₆ⁱ(1,0)ᵀ`, U₆=[[√3,−1],[1,0]]:
  `w₁=(√3,1)`, `w₂=(2,√3)`, `w₃=(√3,2)`, `w₄=(1,√3)`, `w₅=(0,1)`, `w₆=(−1,0)`.
Write `dᵢ = wᵢ·(a,b)`:  d₁=√3a+b, d₂=2a+√3b, d₃=√3a+2b, d₄=a+√3b, d₅=b.
* Domain `T⁶ = {0<a≤1, 1−√3a<b≤1}` (= {d₁>1, b≤1}).
* Partition `Tᵢ={d_{i-1}>1, dᵢ≤1}`, i=2..5; T₅ last.  Disjointness ⇒ the FIRST dᵢ to
  drop ≤1 (scanning i=2,3,4,5) names the branch, and on each Tᵢ all later d are ≤1.
* Observable `P = a·dᵢ/yᵢ` (yᵢ = wᵢ second coord: y₂=√3,y₃=2,y₄=√3,y₅=1).
  On the last branch T₅ (w₅=(0,1)): `P = a·b`.
* BCZ map on Tᵢ: `(a,b) ↦ (dᵢ, d_{i+1} + k·√3·dᵢ)`, `k=⌊(1−d_{i+1})/(√3 dᵢ)⌋`.
  On T₅: `(b, −a + k√3 b)`, `k=⌊(1+a)/(√3 b)⌋`.

## Proof outline (every step verified numerically; code/goal1_q6_{mechanism,certs}.py)

Extremes are confined to T₅ (intermediate branches have `P ≥ X`):
* `lemA2` (T₂): `a·d₂ ≥ 1/3`.  Clean: `a+d₂ = √3·d₁ > √3`, `(1−a)(1−d₂)≥0`.
* `lemA3` (T₃): `a·d₃ ≥ 2√3/9`. Clean: `a+d₃ = (√3−1)(d₁+d₂) > 2(√3−1)`.
* `lemA4` (T₄): `a·d₄ ≥ 1/3` (TIGHT, = at corner (1/√3,0)).  Exact identity
  `a·d₄ − 1/3 = ⅓(d₁−1)+⅓(d₃−1)+(a−√3/3)(d₄−√3/3)`; needs a Positivstellensatz
  certificate (the last term can be negative; the d₁−1 term dominates).
Then `xᵢ,xᵢ₊₁ ∈ T₅`, `P(xᵢ)=ab`, `P(xᵢ₊₁)=bc`, `a+c=k√3b`, `xᵢ₊₂=(c,d)`, `d=−b+ℓ√3c`.
Third point: if `xᵢ₊₂ ∉ T₅` it is non-extreme (lemA2/3/4); if `xᵢ₊₂ ∈ T₅`, need `cd≥X`:
* `k≥3`: `kb²<2/9` ⇒ `b<√(2/27)` ⇒ `c>1−√3b>√2/3` ⇒ `cd ≥ √3c²−bc > 2X−X = X`.  Clean.
* `k∈{1,2}`: the hard coupled certificate (uses ab<X, bc<X, T₅ conds, ℓ≥1).
-/

open Real Set
open Classical

noncomputable section

-- `λ₆ = 2cos(π/6) = √3`.
noncomputable def s3 : ℝ := Real.sqrt 3

lemma s3_mul : s3 * s3 = 3 := Real.mul_self_sqrt (by norm_num)
lemma s3_pos : 0 < s3 := Real.sqrt_pos.mpr (by norm_num)
lemma s3_gt_one : 1 < s3 := by nlinarith [s3_mul, s3_pos]
lemma s3_lt_two : s3 < 2 := by nlinarith [s3_mul, s3_pos]

-- `X(6) = 1/λ³ = √3/9`.  We use `s3 / 9` directly.

/-- Domain `T⁶ = {0<a≤1, 1−√3a<b≤1}`. -/
def T6 : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 1 - s3 * p.1 < p.2 ∧ p.2 ≤ 1}

/-- Last branch `T₅`: `d₄ = a+√3b > 1`. -/
def InT5 (p : ℝ × ℝ) : Prop := p.1 + s3 * p.2 > 1

/-- Observable.  Branch by the first `dᵢ` to drop `≤1` (T₅ if d₄>1, else T₄ if d₃>1,
else T₃ if d₂>1, else T₂). -/
noncomputable def Pobs (p : ℝ × ℝ) : ℝ :=
  if p.1 + s3 * p.2 > 1 then p.1 * p.2                          -- T₅ : a·b
  else if s3 * p.1 + 2 * p.2 > 1 then p.1 * (p.1 + s3 * p.2) / s3   -- T₄ : a·d₄/√3
  else if 2 * p.1 + s3 * p.2 > 1 then p.1 * (s3 * p.1 + 2 * p.2) / 2 -- T₃ : a·d₃/2
  else p.1 * (2 * p.1 + s3 * p.2) / s3                          -- T₂ : a·d₂/√3

/-- Taha G_6-BCZ map (four branches). -/
noncomputable def bczMap6 (p : ℝ × ℝ) : ℝ × ℝ :=
  if p.1 + s3 * p.2 > 1 then                                    -- T₅
    (p.2, -p.1 + ((⌊(1 + p.1) / (s3 * p.2)⌋ : ℤ) : ℝ) * s3 * p.2)
  else if s3 * p.1 + 2 * p.2 > 1 then                           -- T₄ : a'=d₄, b'=d₅+k√3d₄
    (p.1 + s3 * p.2,
      p.2 + ((⌊(1 - p.2) / (s3 * (p.1 + s3 * p.2))⌋ : ℤ) : ℝ) * s3 * (p.1 + s3 * p.2))
  else if 2 * p.1 + s3 * p.2 > 1 then                           -- T₃ : a'=d₃, b'=d₄+k√3d₃
    (s3 * p.1 + 2 * p.2,
      (p.1 + s3 * p.2)
        + ((⌊(1 - (p.1 + s3 * p.2)) / (s3 * (s3 * p.1 + 2 * p.2))⌋ : ℤ) : ℝ)
          * s3 * (s3 * p.1 + 2 * p.2))
  else                                                          -- T₂ : a'=d₂, b'=d₃+k√3d₂
    (2 * p.1 + s3 * p.2,
      (s3 * p.1 + 2 * p.2)
        + ((⌊(1 - (s3 * p.1 + 2 * p.2)) / (s3 * (2 * p.1 + s3 * p.2))⌋ : ℤ) : ℝ)
          * s3 * (2 * p.1 + s3 * p.2))

lemma Pobs_T5 {p : ℝ × ℝ} (h : InT5 p) : Pobs p = p.1 * p.2 := by
  unfold Pobs; rw [if_pos (show p.1 + s3 * p.2 > 1 from h)]

lemma bczMap6_T5 {p : ℝ × ℝ} (h : InT5 p) :
    bczMap6 p = (p.2, -p.1 + ((⌊(1 + p.1) / (s3 * p.2)⌋ : ℤ) : ℝ) * s3 * p.2) := by
  unfold bczMap6; rw [if_pos (show p.1 + s3 * p.2 > 1 from h)]

/-- `s3/9 = (1/3)/s3`, converting the threshold between forms. -/
lemma X_lt_third_over_s3 : s3 / 9 = (1 / 3) / s3 := by
  rw [div_div, div_eq_div_iff (by norm_num : (9:ℝ) ≠ 0)
    (ne_of_gt (mul_pos (by norm_num : (0:ℝ) < 3) s3_pos))]
  nlinarith [s3_mul]

/-- **T₂ non-extreme** (clean): on `T₂`, `a·d₂ ≥ 1/3`. -/
lemma lemA2 {a b : ℝ}
    (ha_pos : 0 < a) (ha_le : a ≤ 1)
    (hdom : 1 - s3 * a < b)
    (hd2 : 2 * a + s3 * b ≤ 1) :
    a * (2 * a + s3 * b) ≥ 1 / 3 := by
  have h3 : s3 * s3 = 3 := s3_mul
  have hpos : 0 < s3 := s3_pos
  have hd1 : s3 * a + b > 1 := by nlinarith [hdom, hpos]
  have hfac : (1 - a) * (1 - (2 * a + s3 * b)) ≥ 0 := mul_nonneg (by linarith) (by linarith)
  have hident : a + (2 * a + s3 * b) = s3 * (s3 * a + b) := by nlinarith [h3]
  nlinarith [hfac, hident, hd1, h3]

/-- **T₃ non-extreme** (clean): on `T₃`, `a·d₃ ≥ 2√3/9`. -/
lemma lemA3 {a b : ℝ}
    (ha_pos : 0 < a) (ha_le : a ≤ 1)
    (hdom : 1 - s3 * a < b)
    (hd2 : 2 * a + s3 * b > 1)
    (hd3 : s3 * a + 2 * b ≤ 1) :
    a * (s3 * a + 2 * b) ≥ 2 * s3 / 9 := by
  have h3 : s3 * s3 = 3 := s3_mul
  have hpos : 0 < s3 := s3_pos
  have hd1 : s3 * a + b > 1 := by nlinarith [hdom, hpos]
  have hfac : (1 - a) * (1 - (s3 * a + 2 * b)) ≥ 0 := mul_nonneg (by linarith) (by linarith)
  nlinarith [hfac, hd1, hd2, h3, hpos, s3_gt_one,
             mul_pos hpos (by linarith : 0 < s3 * a + b - 1)]

/-
**T₄ non-extreme** (TIGHT — the hard certificate): on `T₄`, `a·d₄ ≥ 1/3`.
Exact identity: `a·d₄ − 1/3 = ⅓(d₁−1) + ⅓(d₃−1) + (a−√3/3)(d₄−√3/3)`.
-/
lemma lemA4 {a b : ℝ}
    (ha_pos : 0 < a) (ha_le : a ≤ 1)
    (hdom : 1 - s3 * a < b)
    (hd3 : s3 * a + 2 * b > 1)
    (hd4 : a + s3 * b ≤ 1) :
    a * (a + s3 * b) ≥ 1 / 3 := by
  have h3 : s3 * s3 = 3 := s3_mul
  have hpos : 0 < s3 := s3_pos
  have hd1 : s3 * a + b > 1 := by nlinarith [hdom, hpos]
  have hid : a * (a + s3 * b) - 1 / 3
      = (1 / 3) * (s3 * a + b - 1) + (1 / 3) * (s3 * a + 2 * b - 1)
        + (a - s3 / 3) * (a + s3 * b - s3 / 3) := by
    linear_combination ((3 * b - 1) / 9) * s3_mul
  by_contra h_contra;
  nlinarith only [ ha_pos, ha_le, hdom, hd3, hd4, h3, hpos, hd1, h_contra, hid, mul_le_mul_of_nonneg_left hd1.le ha_pos.le, mul_le_mul_of_nonneg_left hd3.le ha_pos.le, mul_le_mul_of_nonneg_left hd4 ha_pos.le, mul_le_mul_of_nonneg_left hd1.le hpos.le, mul_le_mul_of_nonneg_left hd3.le hpos.le, mul_le_mul_of_nonneg_left hd4 hpos.le ]

/-- Off the last branch, the observable is `≥ X = √3/9`. -/
lemma nonextreme_off_T5 {p : ℝ × ℝ} (hp : p ∈ T6) (hn : ¬ InT5 p) :
    Pobs p ≥ s3 / 9 := by
  obtain ⟨ha, hale, hdom, _hble⟩ := hp
  have hpos : 0 < s3 := s3_pos
  have hXeq : s3 / 9 = (1 / 3) / s3 := X_lt_third_over_s3
  have hd4 : ¬ (p.1 + s3 * p.2 > 1) := hn
  unfold Pobs
  rw [if_neg hd4]
  by_cases hd3 : s3 * p.1 + 2 * p.2 > 1
  · rw [if_pos hd3]
    -- T₄ : a·d₄/√3 ≥ X ⇔ a·d₄ ≥ 1/3
    have h4 := lemA4 ha hale hdom hd3 (le_of_not_gt hd4)
    rw [ge_iff_le, hXeq]
    exact div_le_div_of_nonneg_right h4 hpos.le
  · rw [if_neg hd3]
    by_cases hd2 : 2 * p.1 + s3 * p.2 > 1
    · rw [if_pos hd2]
      -- T₃ : a·d₃/2 ≥ X ⇔ a·d₃ ≥ 2√3/9
      have h3 := lemA3 ha hale hdom hd2 (le_of_not_gt hd3)
      rw [ge_iff_le, le_div_iff₀ (by norm_num : (0:ℝ) < 2)]
      linarith
    · rw [if_neg hd2]
      -- T₂ : a·d₂/√3 ≥ X ⇔ a·d₂ ≥ 1/3
      have h2 := lemA2 ha hale hdom (le_of_not_gt hd2)
      rw [ge_iff_le, hXeq]
      exact div_le_div_of_nonneg_right h2 hpos.le

/-- Extreme (`P < X`) ⇒ in the last branch `T₅`. -/
lemma extreme_imp_T5 {p : ℝ × ℝ} (hp : p ∈ T6) (hext : Pobs p < s3 / 9) : InT5 p := by
  by_contra hn
  have := nonextreme_off_T5 hp hn
  linarith

/-
For k=1, l=1 is impossible: it forces bc ≥ s3/9.
-/
lemma closing_k1_l_ge_2 {a b c d : ℝ} {l : ℤ}
    (h3 : s3 * s3 = 3) (hpos : 0 < s3)
    (hbc : b * c < s3 / 9)
    (hsum : a + c = 1 * s3 * b)
    (_hT5_1 : b + s3 * c > 1)
    (hT5_2 : c + s3 * d > 1)
    (hc_pos : 0 < c) (hb_pos : 0 < b)
    (hlR1 : (1 : ℤ) ≤ l)
    (hcd_eq : c * d = (l : ℝ) * s3 * c ^ 2 - b * c)
    (ha_dom : 1 - s3 * a < b) :
    (2 : ℤ) ≤ l := by
  rcases l with ⟨ _ | _ | l ⟩ <;> norm_num at *;
  · -- From hT5_2, we have $4c - s3b > 1$.
    have h4c_s3b : 4 * c - s3 * b > 1 := by
      nlinarith;
    -- From hT5_1, we have $4b - s3c > 1$.
    have h4b_s3c : 4 * b - s3 * c > 1 := by
      nlinarith [ mul_pos hpos hb_pos, mul_pos hpos hc_pos ];
    nlinarith only [ h3, hpos, hbc, hc_pos, hb_pos, h4c_s3b, h4b_s3c, mul_pos hc_pos hb_pos, mul_pos hc_pos hpos, mul_pos hb_pos hpos, sq_nonneg ( c - b ), sq_nonneg ( c - s3 / 3 ), sq_nonneg ( b - s3 / 3 ) ];
  · linarith;
  · tauto

/-
For k=1 with l≥2, cd ≥ s3/9.
-/
lemma closing_k1_from_l2 {a b c d : ℝ} {l : ℤ}
    (h3 : s3 * s3 = 3) (hpos : 0 < s3)
    (hab : a * b < s3 / 9)
    (hbc : b * c < s3 / 9)
    (hsum : a + c = 1 * s3 * b)
    (_hT5_i : a + s3 * b > 1)
    (hT5_1 : b + s3 * c > 1)
    (_hT5_2 : c + s3 * d > 1)
    (hc_pos : 0 < c) (hb_pos : 0 < b)
    (_hc_le : c ≤ 1) (hdom1 : 1 - s3 * b < c)
    (hL2 : (1 : ℝ) * b ^ 2 < 2 / 9)
    (hlR2 : (2 : ℝ) ≤ (l : ℝ))
    (hcd_eq : c * d = (l : ℝ) * s3 * c ^ 2 - b * c)
    (_ha_dom : 1 - s3 * a < b) :
    c * d ≥ s3 / 9 := by
  -- From hcd_eq: cd = l*s3*c^2 - bc. Since l ≥ 2, cd ≥ 2*s3*c^2 - bc.
  have hcd_ge : c * d ≥ 2 * s3 * c^2 - b * c := by
    exact hcd_eq.symm ▸ by gcongr;
  contrapose! hbc;
  norm_num [ show a = 1 * s3 * b - c by linarith ] at *;
  by_cases h_case : b ≤ 1 / 3;
  · nlinarith only [ h_case, hT5_1, _hT5_2, hL2, hdom1, hcd_ge, hbc, h3, hpos, mul_le_mul_of_nonneg_left h_case <| show 0 ≤ s3 by positivity ];
  · by_cases h_case2 : b ≤ 2 / 5;
    · nlinarith only [ h_case, h_case2, hT5_1, _hT5_2, hcd_ge, hbc, hab, hL2, h3, hpos, mul_le_mul_of_nonneg_left h_case2 hpos.le ];
    · nlinarith only [ hab, hbc, h_case, h_case2, hL2, hT5_1, _hT5_2, hcd_ge, hpos, h3, mul_pos hpos hc_pos, mul_pos hpos hb_pos, mul_pos hc_pos hb_pos, sq_nonneg ( b - 2 / 5 ), sq_nonneg ( c - 1 / 3 ), sq_nonneg ( s3 - 1 ) ]

/-- Helper for the k=1 case of the third-point closing. -/
lemma closing_k1 {a b c d : ℝ} {l : ℤ}
    (h3 : s3 * s3 = 3) (hpos : 0 < s3)
    (hab : a * b < s3 / 9)
    (hbc : b * c < s3 / 9)
    (hsum : a + c = 1 * s3 * b)
    (hT5_i : a + s3 * b > 1)
    (hT5_1 : b + s3 * c > 1)
    (hT5_2 : c + s3 * d > 1)
    (hc_pos : 0 < c) (hb_pos : 0 < b)
    (hc_le : c ≤ 1) (hdom1 : 1 - s3 * b < c)
    (hL2 : (1 : ℝ) * b ^ 2 < 2 / 9)
    (hlR1 : (1 : ℝ) ≤ (l : ℝ))
    (hcd_eq : c * d = (l : ℝ) * s3 * c ^ 2 - b * c)
    (_ha_pos : 0 < a) (_ha_le : a ≤ 1)
    (ha_dom : 1 - s3 * a < b) (_hb_le : b ≤ 1) :
    c * d ≥ s3 / 9 := by
  have hl2 : (2 : ℤ) ≤ l :=
    closing_k1_l_ge_2 h3 hpos hbc hsum hT5_1 hT5_2 hc_pos hb_pos
      (by exact_mod_cast (show (1:ℝ) ≤ (l:ℝ) from hlR1)) hcd_eq ha_dom
  have hlR2 : (2 : ℝ) ≤ (l : ℝ) := by exact_mod_cast hl2
  exact closing_k1_from_l2 h3 hpos hab hbc hsum hT5_i hT5_1 hT5_2
    hc_pos hb_pos hc_le hdom1 hL2 hlR2 hcd_eq ha_dom

/-
Helper for the k=2 case of the third-point closing.
-/
lemma closing_k2 {a b c d : ℝ} {l : ℤ}
    (h3 : s3 * s3 = 3) (hpos : 0 < s3)
    (hab : a * b < s3 / 9)
    (hbc : b * c < s3 / 9)
    (hsum : a + c = 2 * s3 * b)
    (_hT5_i : a + s3 * b > 1)
    (hT5_1 : b + s3 * c > 1)
    (_hT5_2 : c + s3 * d > 1)
    (hc_pos : 0 < c) (hb_pos : 0 < b)
    (_hc_le : c ≤ 1) (hdom1 : 1 - s3 * b < c)
    (hL2 : (2 : ℝ) * b ^ 2 < 2 / 9)
    (hlR1 : (1 : ℝ) ≤ (l : ℝ))
    (hcd_eq : c * d = (l : ℝ) * s3 * c ^ 2 - b * c) :
    c * d ≥ s3 / 9 := by
  by_contra! h_contra;
  have hb_lt_third : b < 1 / 3 := by
    nlinarith only [ hb_pos, hL2 ];
  have hc_gt_0_42 : c > 1 - s3 / 3 := by
    nlinarith only [ hdom1, hb_lt_third, hpos, h3 ];
  have hcd_ge : c * d ≥ s3 * c ^ 2 - b * c := by
    nlinarith [ mul_le_mul_of_nonneg_left hlR1 ( show 0 ≤ s3 * c ^ 2 by positivity ) ];
  nlinarith only [ h3, hpos, hb_lt_third, hc_gt_0_42, hcd_ge, h_contra, hL2, hT5_1, _hT5_2, hdom1, hsum, hab, hbc, mul_pos hb_pos hc_pos, mul_pos hb_pos ( sub_pos.mpr hc_gt_0_42 ), mul_pos hc_pos ( sub_pos.mpr hc_gt_0_42 ) ]

set_option maxHeartbeats 1600000 in
/-- **Main theorem**: in any Taha G_6-BCZ orbit, three consecutive points cannot all
have observable `< √3/9 = X(6)`. -/
theorem cluster_size_le_two_q6 :
    ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ T6) →
      (∀ n, orbit (n + 1) = bczMap6 (orbit n)) →
      ∀ i,
        Pobs (orbit i) < s3 / 9 →
        Pobs (orbit (i + 1)) < s3 / 9 →
        Pobs (orbit (i + 2)) ≥ s3 / 9 := by
  intro orbit hmem hstep i hext0 hext1
  have h3 : s3 * s3 = 3 := s3_mul
  have hpos : 0 < s3 := s3_pos
  have hiT5 : InT5 (orbit i) := extreme_imp_T5 (hmem i) hext0
  have hi1T5 : InT5 (orbit (i + 1)) := extreme_imp_T5 (hmem (i + 1)) hext1
  -- map equations
  have hmapi : orbit (i + 1) =
      ((orbit i).2, -(orbit i).1 + ((⌊(1 + (orbit i).1) / (s3 * (orbit i).2)⌋ : ℤ) : ℝ) * s3 * (orbit i).2) := by
    rw [hstep i]; exact bczMap6_T5 hiT5
  have hmapi1 : orbit (i + 2) =
      ((orbit (i + 1)).2,
        -(orbit (i + 1)).1 + ((⌊(1 + (orbit (i + 1)).1) / (s3 * (orbit (i + 1)).2)⌋ : ℤ) : ℝ) * s3 * (orbit (i + 1)).2) := by
    rw [show i + 2 = (i + 1) + 1 from rfl, hstep (i + 1)]; exact bczMap6_T5 hi1T5
  obtain ⟨ha_pos, ha_le, ha_dom, hb_le⟩ := hmem i
  set a := (orbit i).1 with ha_def
  set b := (orbit i).2 with hb_def
  -- projection: (orbit (i+1)).1 = b
  have hb_eq1 : (orbit (i + 1)).1 = b := by rw [hmapi]
  set c := (orbit (i + 1)).2 with hc_def
  have hc_eq : c = -a + ((⌊(1 + a) / (s3 * b)⌋ : ℤ) : ℝ) * s3 * b := by
    rw [hc_def, hmapi]
  set k : ℤ := ⌊(1 + a) / (s3 * b)⌋ with hk_def
  have hsum : a + c = (k : ℝ) * s3 * b := by rw [hc_eq]; ring
  have hab : a * b < s3 / 9 := by
    have hPi := Pobs_T5 hiT5; rw [← ha_def, ← hb_def] at hPi; rw [hPi] at hext0; exact hext0
  have hbc : b * c < s3 / 9 := by
    have hP1 := Pobs_T5 hi1T5; rw [hb_eq1, ← hc_def] at hP1; rw [hP1] at hext1; exact hext1
  obtain ⟨hb_pos, hb_le1, hdom1, hc_le⟩ := hmem (i + 1)
  rw [hb_eq1] at hb_pos hb_le1 hdom1
  rw [← hc_def] at hdom1 hc_le
  -- T₅ membership facts
  have hT5_i : a + s3 * b > 1 := hiT5
  have hT5_1 : b + s3 * c > 1 := by
    have h : (orbit (i + 1)).1 + s3 * (orbit (i + 1)).2 > 1 := hi1T5
    rw [hb_eq1, ← hc_def] at h; exact h
  have hc_pos : 0 < c := by nlinarith [hT5_1, hb_le1, hpos]
  -- k ≥ 1
  have hk1 : (1 : ℤ) ≤ k := by
    have hsb : 0 < s3 * b := mul_pos hpos hb_pos
    have : (0 : ℝ) < (k : ℝ) := by nlinarith [hsum, ha_pos, hc_pos, hsb]
    have : 0 < k := by exact_mod_cast this
    omega
  -- ab + bc = k√3 b² < 2X  ⇒  k b² < 2/9
  have hprod : a * b + b * c = (k : ℝ) * s3 * b ^ 2 := by
    have h : a * b + b * c = b * (a + c) := by ring
    rw [h, hsum]; ring
  have hL2 : (k : ℝ) * b ^ 2 < 2 / 9 := by
    have hstep_l2 : (k : ℝ) * s3 * b ^ 2 < 2 * s3 / 9 := by rw [← hprod]; linarith [hab, hbc]
    have h' : s3 * ((k : ℝ) * b ^ 2) < s3 * (2 / 9) := by nlinarith [hstep_l2]
    exact lt_of_mul_lt_mul_left h' (le_of_lt hpos)
  -- x_{i+2} = (c, d)
  have hc_eq2 : (orbit (i + 2)).1 = c := by rw [hmapi1]
  set l : ℤ := ⌊(1 + b) / (s3 * c)⌋ with hl_def
  have hd_eq : (orbit (i + 2)).2 = -b + (l : ℝ) * s3 * c := by
    simp only [hmapi1, hb_eq1, hl_def]
  set d := (orbit (i + 2)).2 with hd_def
  -- membership of x_{i+2}
  obtain ⟨hc_pos2, hc_le2, hdom_2, hd_le2⟩ := hmem (i + 2)
  rw [hc_eq2] at hc_pos2 hc_le2 hdom_2
  rw [← hd_def] at hdom_2 hd_le2
  -- split on whether x_{i+2} is in the last branch
  by_cases hbranch : InT5 (orbit (i + 2))
  · -- x_{i+2} ∈ T₅ : Pobs = c·d ; need c·d ≥ X
    have hPeq : Pobs (orbit (i + 2)) = c * d := by
      have := Pobs_T5 hbranch; rw [hc_eq2, ← hd_def] at this; exact this
    have hT5_2 : c + s3 * d > 1 := by
      have h : (orbit (i + 2)).1 + s3 * (orbit (i + 2)).2 > 1 := hbranch
      rw [hc_eq2, ← hd_def] at h; exact h
    -- ℓ ≥ 1
    have hl0 : 0 ≤ l := by
      rw [hl_def]; apply Int.floor_nonneg.mpr
      exact div_nonneg (by linarith [hb_pos]) (le_of_lt (mul_pos hpos hc_pos))
    have hl1 : (1 : ℤ) ≤ l := by
      rcases eq_or_lt_of_le hl0 with h0 | h1
      · exfalso
        have hlR0 : (l : ℝ) = 0 := by rw [← h0]; norm_num
        have hd0 : d = -b := by rw [hd_eq, hlR0]; ring
        rw [hd0] at hT5_2
        nlinarith [hT5_2, hc_le2, mul_pos hpos hb_pos]
      · omega
    have hlR1 : (1 : ℝ) ≤ (l : ℝ) := by exact_mod_cast hl1
    have hcd_eq : c * d = (l : ℝ) * s3 * c ^ 2 - b * c := by rw [hd_eq]; ring
    rw [hPeq]
    -- case on k : k≥3 is clean; k∈{1,2} is the hard coupled certificate.
    rcases lt_or_ge k 3 with hk_lo | hk_hi
    · -- k ∈ {1, 2}
      interval_cases k
      · -- k = 1
        have hsum1 : a + c = 1 * s3 * b := by push_cast at hsum ⊢; linarith
        have hL2_1 : (1 : ℝ) * b ^ 2 < 2 / 9 := by push_cast at hL2 ⊢; linarith
        exact closing_k1 h3 hpos hab hbc hsum1 hT5_i hT5_1 hT5_2
          hc_pos hb_pos hc_le2 hdom1 hL2_1 hlR1 hcd_eq ha_pos ha_le ha_dom hb_le
      · -- k = 2
        have hsum2 : a + c = 2 * s3 * b := by push_cast at hsum ⊢; linarith
        have hL2_2 : (2 : ℝ) * b ^ 2 < 2 / 9 := by push_cast at hL2 ⊢; linarith
        exact closing_k2 h3 hpos hab hbc hsum2 hT5_i hT5_1 hT5_2
          hc_pos hb_pos hc_le2 hdom1 hL2_2 hlR1 hcd_eq
    · -- k ≥ 3 : clean.
      have hkR3 : (3 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk_hi
      have hb2 : b ^ 2 < 2 / 27 := by nlinarith [hL2, hkR3, sq_nonneg b]
      have hc_big : c > 1 - s3 * b := hdom1
      have hsb2 : (s3 * b) ^ 2 < 2 / 9 := by nlinarith [hb2, h3]
      have hc2 : c ^ 2 > 2 / 9 := by nlinarith [hc_big, hsb2, hb_pos, hpos, h3]
      nlinarith [hcd_eq, hlR1, hbc, hc2, h3, hpos,
                 mul_nonneg (sub_nonneg.mpr hlR1) (mul_nonneg hpos.le (sq_nonneg c))]
  · -- x_{i+2} ∉ T₅ : non-extreme by nonextreme_off_T5
    exact nonextreme_off_T5 (hmem (i + 2)) hbranch

end