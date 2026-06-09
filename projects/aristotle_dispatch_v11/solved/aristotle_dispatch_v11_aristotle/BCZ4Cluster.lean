/-
Copyright 2026 Saar Shai. All rights reserved.
Released under Apache 2.0 license as described in the LICENSE file.
Authors: Saar Shai
-/

import Mathlib

/-!
# BCZ cluster ≤ 2 for the Hecke group G_4 (Taha BCZ map analogue), v11

## Goal

Prove `cluster_size_le_two_q4`: along the Taha G_4-BCZ orbit, three consecutive
points cannot all have the ergodic-optimization observable `P < X(4) = √2/8`.
This is the q=4 analogue of the proven q=3 theorem `cluster_size_le_two_clean`
(Aristotle v8).  Together with q=3 it supports the headline conjecture
`X(q) = cluster-onset threshold`.

## Geometry (Taha, arXiv:1810.10668, Thm 2.2; q=4, λ₄ = 2cos(π/4) = √2)

* `G_4`-Farey triangle (domain):  `T⁴ = {(a,b) | 0 < a ≤ 1, 1 − √2·a < b ≤ 1}`.
* Special vectors `wᵢ = U₄ⁱ(1,0)ᵀ`, `U₄ = [[√2,−1],[1,0]]`:
  `w₀=(1,0)`, `w₁=(√2,1)`, `w₂=(1,√2)`, `w₃=(0,1)`, `w₄=(−1,0)`.
* Partition (note `√2·a+b>1` holds throughout `T⁴`, and `b≤1`):
  `T₂ = {a+√2b ≤ 1}`,  `T₃ = {a+√2b > 1}`.
* BCZ map (two branches):
  - On `T₃`:  `(a,b) ↦ (b, −a + k·√2·b)`,  `k = ⌊(1+a)/(√2 b)⌋`.
  - On `T₂`:  `(a,b) ↦ (a+√2b, b + k·√2·(a+√2b))`, `k = ⌊(1−b)/(√2(a+√2b))⌋`.
* Observable `P = 1/R_q` (reciprocal of Taha's roof; small `P` ⇔ large gap):
  `P = a·b` on `T₃`,  `P = a·(a+√2b)/√2` on `T₂`.  (Reduces to `a·b` for q=3.)

## Proof outline (every inequality verified numerically; code/goal1_q4_proof_verify.py)

Let `xᵢ=(a,b)`, `xᵢ₊₁=(b,c)`, `xᵢ₊₂=(c,d)`, with `P(xᵢ),P(xᵢ₊₁) < √2/8`.

**Lemma A** (`lemA`): on `T₂`, `P = a(a+√2b)/√2 ≥ 1−√2/2 > √2/8`.
  Key: with `s=a+√2b`, the domain gives `a+s>√2`, and `(1−a)(1−s)≥0` ⇒
  `a·s ≥ a+s−1 > √2−1`, so `P ≥ (√2−1)/√2 = 1−√2/2`.
  ⇒ (`extreme_imp_T3`) any extreme point is in `T₃`. So `xᵢ,xᵢ₊₁ ∈ T₃`.

On `T₃`: `c = −a + k√2b` (so `a+c = k√2b`), and `P(xᵢ)=ab`, `P(xᵢ₊₁)=bc`.
* `k ≥ 1`: `c>0` (from `b+√2c>1`, `b≤1`) and `a>0` ⇒ `k√2b=a+c>0` ⇒ `k≥1`.
* `k·b² < 1/4`: `ab+bc = b(a+c) = k√2b² < 2·(√2/8) = √2/4` ⇒ `k b² < 1/4`.
* `k ≥ 2`: if `k=1` then `a+c=√2b`; domain `√2a+b>1` ⇒ `a>(1−b)/√2`, and
  `T₃` for `(b,c)` (`b+√2c>1`) ⇒ `c>(1−b)/√2`; so `√2b=a+c>√2(1−b)` ⇒ `b>1/2`,
  contradicting `b²<1/4` (from `k=1`) ⇒ `b<1/2`.
* `c > 1/2`: `k≥2` ⇒ `b²<1/8` ⇒ `√2b<1/2`; domain `1−√2b<c` ⇒ `c>1/2`.

Third point `xᵢ₊₂=(c,d)`, `d=−b+ℓ√2c`, `ℓ=⌊(1+b)/(√2c)⌋`:
* if `xᵢ₊₂∈T₂`: `P ≥ 1−√2/2 > √2/8` by Lemma A.
* if `xᵢ₊₂∈T₃`: then `ℓ≥1` (else `d=−b`, `c+√2d=c−√2b<1`, not `T₃`); so
  `P = cd = ℓ√2c² − bc ≥ √2c² − bc > √2c² − √2/8 > √2/4 − √2/8 = √2/8`  (uses `c>1/2`).

In both cases `P(xᵢ₊₂) ≥ √2/8`.  ∎

## Constraints (project ethos; same as v8)
* NO broad `aesop` / `grind` / `simp_all +decide`.  Acceptable: `linarith`,
  `nlinarith`, `norm_num`, `ring`, `rw`, `simp only [named]`, `by_contra`,
  `rcases`, `omega`, `Int.floor_nonneg`, `Int.cast_*`, named lemma applications.
* Final: 0 sorries, only standard axioms (`propext`, `Classical.choice`, `Quot.sound`).
* The mathematics is verified.  Fix only Lean mechanics (rewrite plumbing,
  `nlinarith` hint sets, lemma-name drift for v4.28.0).  Do NOT change the math.
-/

open Real Set
open Classical

noncomputable section

/-- `λ₄ = 2cos(π/4) = √2`. -/
noncomputable def s2 : ℝ := Real.sqrt 2

lemma s2_mul : s2 * s2 = 2 := Real.mul_self_sqrt (by norm_num)

lemma s2_pos : 0 < s2 := Real.sqrt_pos.mpr (by norm_num)

lemma s2_gt_one : 1 < s2 := by nlinarith [s2_mul, s2_pos]

lemma s2_lt_32 : s2 < 3 / 2 := by nlinarith [s2_mul, s2_pos]

/-- The `G_4`-Farey triangle `T⁴ = {0 < a ≤ 1, 1 − √2·a < b ≤ 1}`. -/
def T4 : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 1 - s2 * p.1 < p.2 ∧ p.2 ≤ 1}

/-- `T₃` half: `a + √2·b > 1` (its complement in `T⁴` is `T₂`). -/
def InT3 (p : ℝ × ℝ) : Prop := p.1 + s2 * p.2 > 1

/-- Observable `P = 1/R_q`:  `a·b` on `T₃`, `a(a+√2b)/√2` on `T₂`. -/
noncomputable def Pobs (p : ℝ × ℝ) : ℝ :=
  if p.1 + s2 * p.2 > 1 then p.1 * p.2 else p.1 * (p.1 + s2 * p.2) / s2

/-- Taha G_4-BCZ map (two branches). -/
noncomputable def bczMap4 (p : ℝ × ℝ) : ℝ × ℝ :=
  if p.1 + s2 * p.2 > 1 then
    (p.2, -p.1 + ((⌊(1 + p.1) / (s2 * p.2)⌋ : ℤ) : ℝ) * s2 * p.2)
  else
    (p.1 + s2 * p.2,
      p.2 + ((⌊(1 - p.2) / (s2 * (p.1 + s2 * p.2))⌋ : ℤ) : ℝ) * s2 * (p.1 + s2 * p.2))

/-- `Pobs` on the `T₃` branch. -/
lemma Pobs_T3 {p : ℝ × ℝ} (h : InT3 p) : Pobs p = p.1 * p.2 := by
  unfold Pobs; rw [if_pos (show p.1 + s2 * p.2 > 1 from h)]

/-- `Pobs` on the `T₂` branch. -/
lemma Pobs_T2 {p : ℝ × ℝ} (h : ¬ InT3 p) : Pobs p = p.1 * (p.1 + s2 * p.2) / s2 := by
  unfold Pobs; rw [if_neg (show ¬ (p.1 + s2 * p.2 > 1) from h)]

/-- `bczMap4` on the `T₃` branch. -/
lemma bczMap4_T3 {p : ℝ × ℝ} (h : InT3 p) :
    bczMap4 p = (p.2, -p.1 + ((⌊(1 + p.1) / (s2 * p.2)⌋ : ℤ) : ℝ) * s2 * p.2) := by
  unfold bczMap4; rw [if_pos (show p.1 + s2 * p.2 > 1 from h)]

/-- **Lemma A**: on `T₂` (i.e. `a + √2·b ≤ 1`) inside `T⁴`, the observable
`a(a+√2b)/√2 ≥ 1 − √2/2`. -/
lemma lemA {a b : ℝ}
    (_ha_pos : 0 < a) (ha_le : a ≤ 1)
    (ha_dom : 1 - s2 * a < b) (_hb_le : b ≤ 1)
    (hT2 : ¬ (a + s2 * b > 1)) :
    a * (a + s2 * b) / s2 ≥ 1 - s2 / 2 := by
  have h2 : s2 * s2 = 2 := s2_mul
  have hpos : 0 < s2 := s2_pos
  set s := a + s2 * b with hs_def
  have hs_le : s ≤ 1 := le_of_not_gt hT2
  -- domain `1 − √2a < b` ⇒ `√2a + b > 1`
  have hdom' : s2 * a + b > 1 := by linarith [ha_dom]
  -- `a + s = 2a + √2 b > √2`   (multiply the domain inequality by √2)
  have hexp : s2 * (s2 * a + b) = 2 * a + s2 * b := by
    have h : s2 * (s2 * a + b) = s2 * s2 * a + s2 * b := by ring
    rw [h, h2]
  have haps : a + s > s2 := by
    have hmul : s2 * 1 < s2 * (s2 * a + b) := mul_lt_mul_of_pos_left hdom' hpos
    rw [mul_one, hexp] at hmul
    rw [hs_def]; linarith [hmul]
  -- `(1−a)(1−s) ≥ 0` ⇒ `a·s ≥ a+s−1 > √2−1`
  have hfac : (1 - a) * (1 - s) ≥ 0 := mul_nonneg (by linarith) (by linarith)
  have has : a * s > s2 - 1 := by nlinarith [hfac, haps]
  -- `P = a·s/√2 ≥ (√2−1)/√2 = 1 − √2/2`
  rw [ge_iff_le, le_div_iff₀ hpos]
  nlinarith [has, h2, hpos]

/-- `1 − √2/2 > √2/8`. -/
lemma half_gap : (1 : ℝ) - s2 / 2 > s2 / 8 := by nlinarith [s2_lt_32, s2_pos]

/-- An extreme point (`P < √2/8`) of `T⁴` lies in `T₃`. -/
lemma extreme_imp_T3 {p : ℝ × ℝ} (hp : p ∈ T4) (hext : Pobs p < s2 / 8) : InT3 p := by
  by_contra hn
  obtain ⟨ha, hale, hdom, hble⟩ := hp
  have hval : Pobs p = p.1 * (p.1 + s2 * p.2) / s2 := Pobs_T2 hn
  have hA := lemA ha hale hdom hble hn
  rw [hval] at hext
  linarith [hA, half_gap, hext]

private lemma sqrt2_mul_lt_half {b : ℝ} (_hb_pos : 0 < b) (hb2 : b ^ 2 < 1 / 8) :
    s2 * b < 1 / 2 := by
  have h2 : s2 * s2 = 2 := s2_mul
  have hbb : b * b < 1 / 8 := by nlinarith [hb2]
  have hsbsq : s2 * b * (s2 * b) < 1 / 4 := by nlinarith [h2]
  by_contra hge; push_neg at hge
  nlinarith [hge]

set_option maxHeartbeats 800000 in
/-- **Main theorem**: in any Taha G_4-BCZ orbit, three consecutive points cannot
all have observable `< √2/8 = X(4)`. -/
theorem cluster_size_le_two_q4 :
    ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ T4) →
      (∀ n, orbit (n + 1) = bczMap4 (orbit n)) →
      ∀ i,
        Pobs (orbit i) < s2 / 8 →
        Pobs (orbit (i + 1)) < s2 / 8 →
        Pobs (orbit (i + 2)) ≥ s2 / 8 := by
  intro orbit hmem hstep i hext0 hext1
  have h2 : s2 * s2 = 2 := s2_mul
  have hpos : 0 < s2 := s2_pos
  -- branch facts (extreme ⇒ T₃), established before `set` so `set` folds the maps
  have hiT3 : InT3 (orbit i) := extreme_imp_T3 (hmem i) hext0
  have hi1T3 : InT3 (orbit (i + 1)) := extreme_imp_T3 (hmem (i + 1)) hext1
  -- map equations in literal coordinates (match `bczMap4_T3` exactly)
  have hmapi : orbit (i + 1) =
      ((orbit i).2,
        -(orbit i).1 + ((⌊(1 + (orbit i).1) / (s2 * (orbit i).2)⌋ : ℤ) : ℝ) * s2 * (orbit i).2) := by
    rw [hstep i]; exact bczMap4_T3 hiT3
  have hmapi1 : orbit (i + 2) =
      ((orbit (i + 1)).2,
        -(orbit (i + 1)).1
          + ((⌊(1 + (orbit (i + 1)).1) / (s2 * (orbit (i + 1)).2)⌋ : ℤ) : ℝ) * s2 * (orbit (i + 1)).2) := by
    rw [show i + 2 = (i + 1) + 1 from rfl, hstep (i + 1)]; exact bczMap4_T3 hi1T3
  -- x_i membership (obtained before `set` so projections fold to a,b)
  obtain ⟨ha_pos, ha_le, ha_dom, hb_le⟩ := hmem i
  -- ===== name coordinates =====
  set a := (orbit i).1 with ha_def
  set b := (orbit i).2 with hb_def
  -- now: ha_pos:0<a, ha_le:a≤1, ha_dom:1-s2*a<b, hb_le:b≤1,
  --      hmapi: orbit (i+1) = (b, -a + ↑⌊(1+a)/(s2*b)⌋ * s2 * b)
  have hb_eq1 : (orbit (i + 1)).1 = b := by rw [hmapi]
  set c := (orbit (i + 1)).2 with hc_def
  -- hmapi1 now has (orbit (i+1)).2 folded to c
  have hc_eq : c = -a + ((⌊(1 + a) / (s2 * b)⌋ : ℤ) : ℝ) * s2 * b := by rw [hc_def, hmapi]
  set k : ℤ := ⌊(1 + a) / (s2 * b)⌋ with hk_def
  -- hc_eq : c = -a + ↑k * s2 * b
  have hsum : a + c = (k : ℝ) * s2 * b := by rw [hc_eq]; ring
  -- P(x_i) = a*b ;  P(x_{i+1}) = b*c
  have hab : a * b < s2 / 8 := by
    have hPi := Pobs_T3 hiT3
    rw [← ha_def, ← hb_def] at hPi
    rw [hPi] at hext0; exact hext0
  have hbc : b * c < s2 / 8 := by
    have hP1 := Pobs_T3 hi1T3
    rw [hb_eq1, ← hc_def] at hP1
    rw [hP1] at hext1; exact hext1
  -- x_{i+1} membership, folded to b,c
  obtain ⟨hb_pos, hb_le1, hdom1, hc_le⟩ := hmem (i + 1)
  rw [hb_eq1] at hb_pos hb_le1 hdom1
  rw [← hc_def] at hdom1 hc_le
  -- T₃ for x_{i+1}:  b + √2 c > 1
  have hT3_1 : b + s2 * c > 1 := by
    have h : (orbit (i + 1)).1 + s2 * (orbit (i + 1)).2 > 1 := hi1T3
    rw [hb_eq1, ← hc_def] at h; exact h
  -- c > 0
  have hc_pos : 0 < c := by nlinarith [hT3_1, hb_le1, hpos]
  -- ===== k ≥ 1 =====
  have hk1 : (1 : ℤ) ≤ k := by
    have hsb : 0 < s2 * b := mul_pos hpos hb_pos
    have hkR_pos : (0 : ℝ) < (k : ℝ) := by nlinarith [hsum, ha_pos, hc_pos, hsb]
    have : 0 < k := by exact_mod_cast hkR_pos
    omega
  -- ===== k·b² < 1/4 =====
  have hprod : a * b + b * c = (k : ℝ) * s2 * b ^ 2 := by
    have h : a * b + b * c = b * (a + c) := by ring
    rw [h, hsum]; ring
  have hstep_l2 : (k : ℝ) * s2 * b ^ 2 < s2 / 4 := by rw [← hprod]; linarith [hab, hbc]
  have hL2 : (k : ℝ) * b ^ 2 < 1 / 4 := by
    have h' : s2 * ((k : ℝ) * b ^ 2) < s2 * (1 / 4) := by nlinarith [hstep_l2]
    exact lt_of_mul_lt_mul_left h' (le_of_lt hpos)
  -- ===== k ≥ 2 (rule out k = 1) =====
  have hk2 : (2 : ℤ) ≤ k := by
    by_contra hcon
    push_neg at hcon
    have hk_eq : k = 1 := le_antisymm (by omega) hk1
    have hkR1 : (k : ℝ) = 1 := by rw [hk_eq]; norm_num
    have hsum1 : a + c = s2 * b := by rw [hsum, hkR1]; ring
    have hda : s2 * a > 1 - b := by linarith [ha_dom]
    have hdc : s2 * c > 1 - b := by linarith [hT3_1]
    have hexp2 : s2 * (a + c) = 2 * b := by
      rw [hsum1, show s2 * (s2 * b) = s2 * s2 * b from by ring, h2]
    have hbgt : b > 1 / 2 := by nlinarith [hda, hdc, hexp2]
    have hblt : b < 1 / 2 := by nlinarith [hL2, hkR1, hb_pos]
    linarith [hbgt, hblt]
  -- ===== c > 1/2 =====
  have hkR2 : (2 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk2
  have hb2 : b ^ 2 < 1 / 8 := by nlinarith [hL2, hkR2, sq_nonneg b]
  have hsb_half : s2 * b < 1 / 2 := sqrt2_mul_lt_half hb_pos hb2
  have hc_half : c > 1 / 2 := by linarith [hdom1, hsb_half]
  -- ===== x_{i+2} = (c, d) =====
  have hc_eq2 : (orbit (i + 2)).1 = c := by rw [hmapi1, hc_def]
  have hd_raw : (orbit (i + 2)).2 = -b + ((⌊(1 + b) / (s2 * c)⌋ : ℤ) : ℝ) * s2 * c := by
    rw [hmapi1, hb_eq1]
  set l : ℤ := ⌊(1 + b) / (s2 * c)⌋ with hl_def
  set d := (orbit (i + 2)).2 with hd_def
  have hd_eq : d = -b + (l : ℝ) * s2 * c := hd_raw
  -- x_{i+2} membership, folded to c,d
  obtain ⟨hc_pos2, hc_le2, hdom_2, hd_le2⟩ := hmem (i + 2)
  rw [hc_eq2] at hc_pos2 hc_le2 hdom_2
  rw [← hd_def] at hdom_2 hd_le2
  -- ===== conclude: split on the branch of x_{i+2} =====
  by_cases hbranch : c + s2 * d > 1
  · -- x_{i+2} ∈ T₃ : P = c·d, ℓ ≥ 1, c·d > √2/8
    have hi2T3 : InT3 (orbit (i + 2)) := by
      show (orbit (i + 2)).1 + s2 * (orbit (i + 2)).2 > 1
      rw [hc_eq2, ← hd_def]; exact hbranch
    have hPeq : Pobs (orbit (i + 2)) = c * d := by
      have hP2 := Pobs_T3 hi2T3
      rw [hc_eq2, ← hd_def] at hP2; exact hP2
    -- ℓ ≥ 0
    have hl0 : 0 ≤ l := by
      rw [hl_def]; apply Int.floor_nonneg.mpr
      apply div_nonneg (by linarith [hb_pos]) (le_of_lt (mul_pos hpos hc_pos))
    -- ℓ ≥ 1 (ℓ = 0 ⇒ d = −b ⇒ c + √2 d = c − √2 b < 1, not T₃)
    have hl1 : (1 : ℤ) ≤ l := by
      rcases eq_or_lt_of_le hl0 with h0 | h1
      · exfalso
        have hlR0 : (l : ℝ) = 0 := by rw [← h0]; norm_num
        have hd0 : d = -b := by rw [hd_eq, hlR0]; ring
        rw [hd0] at hbranch
        nlinarith [hbranch, hc_le2, mul_pos hpos hb_pos]
      · omega
    have hlR1 : (1 : ℝ) ≤ (l : ℝ) := by exact_mod_cast hl1
    have hcd_eq : c * d = (l : ℝ) * s2 * c ^ 2 - b * c := by rw [hd_eq]; ring
    have hsc2 : 0 ≤ s2 * c ^ 2 := mul_nonneg (le_of_lt hpos) (sq_nonneg c)
    have hc2 : c ^ 2 > 1 / 4 := by nlinarith [hc_half, hc_pos]
    have hsc2_gt : s2 * c ^ 2 > s2 / 4 := by nlinarith [hc2, hpos]
    have hcd : c * d > s2 / 8 := by
      nlinarith [hcd_eq, hsc2_gt, hbc, mul_nonneg (sub_nonneg.mpr hlR1) hsc2]
    rw [hPeq]; linarith [hcd]
  · -- x_{i+2} ∈ T₂ : P ≥ 1 − √2/2 > √2/8 (Lemma A)
    have hn : ¬ InT3 (orbit (i + 2)) := by
      show ¬ ((orbit (i + 2)).1 + s2 * (orbit (i + 2)).2 > 1)
      rw [hc_eq2, ← hd_def]; exact hbranch
    have hP2 : Pobs (orbit (i + 2)) = c * (c + s2 * d) / s2 := by
      have h := Pobs_T2 hn
      rw [hc_eq2, ← hd_def] at h; exact h
    have hA := lemA hc_pos2 hc_le2 hdom_2 hd_le2 hbranch
    rw [hP2]; linarith [hA, half_gap]

end
