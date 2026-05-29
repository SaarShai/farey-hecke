/-
G_4 Hecke BCZ cluster rigidity — CORE real-arithmetic lemma (machine-checked).
Mirrors the v8 cluster_size_le_two structure but for the Hecke group G_4 (λ = √2),
ground-state constant t = √2/8.

Pure lemma: four consecutive T_3-orbit coordinates a,b,c,d (with the BCZ recurrence
a+c = k0·√2·b, b+d = k1·√2·c, floor word k0,k1 ≥ 1, triangle sums > 1) cannot have
all three gap-products a·b, b·c, c·d below √2/8.

This is the heart of §3 / §3b of T8_hecke_verdict.md.  No `sorry`, no heavy automation.
`s` plays the role of √2 (only `s^2 = 2`, `s > 0` are used).
-/
import Mathlib.Tactic

set_option maxHeartbeats 1000000

/-- The core: no three consecutive G_4 gap-products are all < √2/8. -/
theorem g4_core (s a b c d : ℝ)
    (hs : s ^ 2 = 2) (hsp : 0 < s)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d)
    (hab1 : a + s * b > 1) (hbc1 : b + s * c > 1) (hcd1 : c + s * d > 1)
    (k0 k1 : ℤ)
    (hk0 : a + c = (k0 : ℝ) * s * b)
    (hk1 : b + d = (k1 : ℝ) * s * c)
    (hk0ge : 1 ≤ k0) (hk1ge : 1 ≤ k1)
    -- floor upper bound for k0: (1+a)/(s·b) < k0 + 1, i.e. 1 + a < (k0+1)·s·b
    (hk0f : 1 + a < ((k0 : ℝ) + 1) * (s * b))
    (hABt : a * b < s / 8) (hBCt : b * c < s / 8) (hCDt : c * d < s / 8) :
    False := by
  have hk0ge' : (1 : ℝ) ≤ (k0 : ℝ) := by exact_mod_cast hk0ge
  have hk1ge' : (1 : ℝ) ≤ (k1 : ℝ) := by exact_mod_cast hk1ge
  -- Pure facts about s = √2 (hoisted while the context is still small).
  have hs_lt2 : s < 2 := by nlinarith [hs, hsp]
  have hs_hi : s < 17 / 12 := by nlinarith [hs, hsp]
  have h32s_pos : 0 < 3 / 2 - s := by nlinarith [hs, hsp]
  have hs_pos_half : 0 < 1 - s / 2 := by linarith [hs_lt2]
  -- Recurrence sum identities:  a·b + b·c = k0·s·b² ,  b·c + c·d = k1·s·c².
  have e1 : a * b + b * c = (k0 : ℝ) * s * b ^ 2 := by linear_combination b * hk0
  have e2 : b * c + c * d = (k1 : ℝ) * s * c ^ 2 := by linear_combination c * hk1
  -- Hence k0·s·b² < s/4 and k1·s·c² < s/4.
  have hS1 : (k0 : ℝ) * s * b ^ 2 < s / 4 := by rw [← e1]; linarith [hABt, hBCt]
  have hS2 : (k1 : ℝ) * s * c ^ 2 < s / 4 := by rw [← e2]; linarith [hBCt, hCDt]
  -- Step (iii): b² < 1/4.  s·b² ≤ k0·s·b² < s/4, then divide by s>0.
  have hb2 : b ^ 2 < 1 / 4 := by
    nlinarith [hS1, hsp,
      mul_nonneg (mul_nonneg (sub_nonneg.mpr hk0ge') hsp.le) (sq_nonneg b)]
  have hb_half : b < 1 / 2 := by nlinarith [hb2, hb]
  -- Step (iv): c² > 1/8, via s·c > 1 − b > 1/2 then (s·c)² = 2c² > 1/4.
  have hsc : s * c > 1 / 2 := by linarith [hbc1, hb_half]
  have hsc2 : (s * c) ^ 2 = 2 * c ^ 2 := by rw [mul_pow, hs]
  have hc2 : c ^ 2 > 1 / 8 := by nlinarith [hsc, mul_pos hsp hc, hsc2]
  -- Step (v): k1 = 1.  From k1·c² < 1/4 (divide hS2 by s) and c² > 1/8.
  have hk1c : (k1 : ℝ) * c ^ 2 < 1 / 4 := by nlinarith [hS2, hsp]
  have hk1_lt2 : (k1 : ℝ) < 2 := by
    nlinarith [hk1c, hc2,
      mul_pos (show (0:ℝ) < (k1:ℝ) by linarith) (show (0:ℝ) < c ^ 2 - 1/8 by linarith)]
  have hk1eq : k1 = 1 := by
    have : k1 < 2 := by exact_mod_cast hk1_lt2
    omega
  have hk1r : (k1 : ℝ) = 1 := by exact_mod_cast hk1eq
  -- Step (vi): c < 1/2.  From hS2 with k1 = 1: c² < 1/4.
  have hc_half : c < 1 / 2 := by
    have hcsq : c ^ 2 < 1 / 4 := by
      have h := hk1c; rw [hk1r] at h; linarith [h]
    nlinarith [hcsq, hc]
  -- Step (vii): b > 1 − s/2 and hence b² > 3/2 − s.
  have hb_lo : b > 1 - s / 2 := by
    have hsc_lt : s * c < s / 2 := by nlinarith [hc_half, hsp]
    linarith [hbc1, hsc_lt]
  have hb_lo2 : b ^ 2 > 3 / 2 - s := by
    nlinarith [mul_pos (show (0:ℝ) < b - (1 - s/2) by linarith)
                       (show (0:ℝ) < b + (1 - s/2) by linarith), hs]
  -- Step (viii): k0 ≤ 2.  k0·b² < 1/4 and b² > 3/2 − s with s < 17/12.
  have hk0_lt3 : (k0 : ℝ) < 3 := by
    have hk0b2 : (k0 : ℝ) * b ^ 2 < 1 / 4 := by nlinarith [hS1, hsp]
    nlinarith [hk0b2, hs_hi, h32s_pos,
      mul_pos (show (0:ℝ) < (k0:ℝ) by linarith)
              (show (0:ℝ) < b ^ 2 - (3/2 - s) by linarith)]
  have hk0_le2 : k0 ≤ 2 := by
    have : k0 < 3 := by exact_mod_cast hk0_lt3
    omega
  -- Case split on k0 ∈ {1, 2}.
  interval_cases k0
  · -- k0 = 1.  a + c = s·b, so a = s·b − c.
    have hac : a + c = s * b := by push_cast at hk0; linear_combination hk0
    have ha_eq : a = s * b - c := by linear_combination hac
    -- R_0: a + s·b > 1 ⟹ 2 s·b − c > 1 ⟹ (c>0) s·b > 1/2.
    have hb_gt : s * b > 1 / 2 := by nlinarith [hab1, ha_eq, hc]
    -- d = s·c − b (k1 = 1).  Then c + s·d > 1 ⟹ 3c − s·b > 1.
    have hd_eq : d = s * c - b := by rw [hk1r] at hk1; linear_combination hk1
    have hR2 : 3 * c - s * b > 1 := by
      have hsd : s * d = 2 * c - s * b := by rw [hd_eq]; linear_combination c * hs
      linarith [hcd1, hsd]
    -- c > (1 + s·b)/3 ; so b·c > b·(1+s·b)/3.
    have hbc_lo : b * c > b * (1 + s * b) / 3 := by
      have h3c : c > (1 + s * b) / 3 := by linarith [hR2]
      nlinarith [h3c, hb]
    -- s·b > 1/2 ⟹ b > 1/(2s) = s/4.
    have hb_gt_s4 : b > s / 4 := by nlinarith [hb_gt, hs, hsp]
    -- b·(1 + s·b)/3 ≥ s/8 using b > s/4, s² = 2 (equality holds exactly at b = s/4).
    have hkey : b * (1 + s * b) / 3 ≥ s / 8 := by
      nlinarith [hb_gt_s4, hs, hsp, hb,
        mul_nonneg hsp.le (sq_nonneg (b - s/4)),
        mul_pos hsp (show (0:ℝ) < b - s/4 by linarith)]
    linarith [hBCt, hbc_lo, hkey]
  · -- k0 = 2.  a + c = 2 s·b.  Floor: 1 + a < 3·s·b.
    have hac : a + c = 2 * (s * b) := by push_cast at hk0; linear_combination hk0
    have ha_eq : a = 2 * (s * b) - c := by linear_combination hac
    have hfloor : 1 + a < 3 * (s * b) := by push_cast at hk0f; linarith [hk0f]
    -- ⟹ 1 − c < s·b.
    have h1c : 1 - c < s * b := by linarith [hfloor, ha_eq]
    -- b² < 1/8 (from k0 = 2 in hS1), hence b < s/4.
    have hb2' : b ^ 2 < 1 / 8 := by
      have hS1' : (2:ℝ) * s * b ^ 2 < s / 4 := by push_cast at hS1; linarith [hS1]
      nlinarith [hS1', hsp]
    have hb_lt_s4 : b < s / 4 := by nlinarith [hb2', hs, hsp, hb]
    -- s·b < s·(s/4) = 1/2 ⟹ 1 − c < 1/2 ⟹ c > 1/2.  Contradicts c < 1/2.
    have hsb_lt : s * b < 1 / 2 := by nlinarith [hb_lt_s4, hs, hsp]
    have hc_gt : c > 1 / 2 := by linarith [h1c, hsb_lt]
    linarith [hc_gt, hc_half]

/-- Orbit form (mirrors v8 `cluster_size_le_two_clean`).  For a region-(q−1)
    BCZ orbit of the Hecke group G_4 (λ = √2 played by `s`) — a positive sequence
    lying above the line `c n + s·c (n+1) > 1` and evolving by the floor recurrence
    `c (n+2) = ⌊(1 + c n)/(s·c (n+1))⌋ · s · c (n+1) − c n` — no three consecutive
    gap-products `c n · c (n+1)` are all below the ground-state value `s/8 = √2/8`.
    Equivalently: every window of three consecutive products has its max ≥ √2/8,
    i.e. the cluster of sub-√2/8 products has size ≤ 2. -/
theorem g4_no_three_below
    (s : ℝ) (hs : s ^ 2 = 2) (hsp : 0 < s)
    (c : ℕ → ℝ)
    (hpos : ∀ n, 0 < c n)
    (hreg : ∀ n, c n + s * c (n + 1) > 1)
    (hrec : ∀ n, c n + c (n + 2)
              = (⌊(1 + c n) / (s * c (n + 1))⌋ : ℝ) * s * c (n + 1)) :
    ∀ i, ¬ (c i * c (i + 1) < s / 8 ∧
            c (i + 1) * c (i + 2) < s / 8 ∧
            c (i + 2) * c (i + 3) < s / 8) := by
  intro i hcon
  obtain ⟨hAB, hBC, hCD⟩ := hcon
  have hsb_pos : 0 < s * c (i + 1) := mul_pos hsp (hpos (i + 1))
  have hsc_pos : 0 < s * c (i + 2) := mul_pos hsp (hpos (i + 2))
  -- the two floor words of the BCZ recurrence at steps i and i+1
  have hk0 : c i + c (i + 2)
      = (⌊(1 + c i) / (s * c (i + 1))⌋ : ℝ) * s * c (i + 1) := hrec i
  have hk1 : c (i + 1) + c (i + 3)
      = (⌊(1 + c (i + 1)) / (s * c (i + 2))⌋ : ℝ) * s * c (i + 2) := hrec (i + 1)
  -- k0 ≥ 1: the recurrence sum k0·s·c(i+1) = c i + c(i+2) > 0, and s·c(i+1) > 0.
  have hk0ge : 1 ≤ ⌊(1 + c i) / (s * c (i + 1))⌋ := by
    have hsum : 0 < (⌊(1 + c i) / (s * c (i + 1))⌋ : ℝ) * s * c (i + 1) := by
      rw [← hk0]; linarith [hpos i, hpos (i + 2)]
    have h0 : (0 : ℝ) < (⌊(1 + c i) / (s * c (i + 1))⌋ : ℝ) := by nlinarith [hsum, hsb_pos]
    have : (0 : ℤ) < ⌊(1 + c i) / (s * c (i + 1))⌋ := by exact_mod_cast h0
    omega
  have hk1ge : 1 ≤ ⌊(1 + c (i + 1)) / (s * c (i + 2))⌋ := by
    have hsum : 0 < (⌊(1 + c (i + 1)) / (s * c (i + 2))⌋ : ℝ) * s * c (i + 2) := by
      rw [← hk1]; linarith [hpos (i + 1), hpos (i + 3)]
    have h0 : (0 : ℝ) < (⌊(1 + c (i + 1)) / (s * c (i + 2))⌋ : ℝ) := by nlinarith [hsum, hsc_pos]
    have : (0 : ℤ) < ⌊(1 + c (i + 1)) / (s * c (i + 2))⌋ := by exact_mod_cast h0
    omega
  -- floor upper bound: (1 + c i)/(s·c(i+1)) < k0 + 1, cleared of the denominator.
  have hk0f : 1 + c i
      < ((⌊(1 + c i) / (s * c (i + 1))⌋ : ℝ) + 1) * (s * c (i + 1)) :=
    (div_lt_iff₀ hsb_pos).mp (Int.lt_floor_add_one _)
  exact g4_core s (c i) (c (i + 1)) (c (i + 2)) (c (i + 3)) hs hsp
    (hpos i) (hpos (i + 1)) (hpos (i + 2)) (hpos (i + 3))
    (hreg i) (hreg (i + 1)) (hreg (i + 2))
    (⌊(1 + c i) / (s * c (i + 1))⌋) (⌊(1 + c (i + 1)) / (s * c (i + 2))⌋)
    hk0 hk1 hk0ge hk1ge hk0f hAB hBC hCD
