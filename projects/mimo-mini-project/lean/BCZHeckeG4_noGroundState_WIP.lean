import Mathlib
/-!
q=4 (Hecke G₄) BCZ ergodic optimization — scalar core toward NO GROUND STATE.
s = √2, t = s/8. Orbit scalar c n > 0, region c n + s·c(n+1) > 1,
recurrence c n + c(n+2) = ⌊(1+c n)/(s·c(n+1))⌋·s·c(n+1).
Target: no orbit keeps every product P n = c n·c(n+1) ≤ s/8  (⇒ no ground state).
-/
open Int

section G4
variable (s : ℝ) (hs : s ^ 2 = 2) (hsp : 0 < s)
variable (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
variable (hreg : ∀ n, c n + s * c (n + 1) > 1)
variable (hrec : ∀ n, c n + c (n + 2)
  = (⌊(1 + c n) / (s * c (n + 1))⌋ : ℝ) * s * c (n + 1))

include hsp hpos hrec in
/-- The floor is always ≥ 1 (else the next coordinate would be ≤ 0). -/
lemma g4_floor_ge_one (n : ℕ) :
    (1 : ℤ) ≤ ⌊(1 + c n) / (s * c (n + 1))⌋ := by
  by_contra hcon
  push_neg at hcon
  have hle : ⌊(1 + c n) / (s * c (n + 1))⌋ ≤ 0 := by omega
  have hkle : (⌊(1 + c n) / (s * c (n + 1))⌋ : ℝ) ≤ 0 := by exact_mod_cast hle
  have hk := hrec n
  have hks : (⌊(1 + c n) / (s * c (n + 1))⌋ : ℝ) * s ≤ 0 :=
    mul_nonpos_iff.mpr (Or.inr ⟨hkle, hsp.le⟩)
  have hksc : (⌊(1 + c n) / (s * c (n + 1))⌋ : ℝ) * s * c (n + 1) ≤ 0 :=
    mul_nonpos_iff.mpr (Or.inr ⟨hks, (hpos (n + 1)).le⟩)
  linarith [hk, hpos n, hpos (n + 2)]

include hrec in
/-- Floor-=1 forward identity: if the floor at `n` equals 1 then `c(n+2) = s·c(n+1) − c n`. -/
lemma g4_step_floor_one (n : ℕ) (h1 : ⌊(1 + c n) / (s * c (n + 1))⌋ = 1) :
    c (n + 2) = s * c (n + 1) - c n := by
  have h := hrec n
  rw [h1, Int.cast_one, one_mul] at h
  linarith [h]

include hrec in
/-- Product identity on a floor-=1 step:
`c(n+1)·c(n+2) = s·c(n+1)² − c n·c(n+1)`. -/
lemma g4_prod_floor_one (n : ℕ) (h1 : ⌊(1 + c n) / (s * c (n + 1))⌋ = 1) :
    c (n + 1) * c (n + 2) = s * c (n + 1) ^ 2 - c n * c (n + 1) := by
  have h := g4_step_floor_one s c hrec n h1
  rw [h]; ring

include hsp hpos hrec in
/-- Case A (forward): at a t-point, if the shared coordinate `c(m+1) > 1/2` then the next
product `c(m+1)·c(m+2) > t = s/8`. Uses only floor ≥ 1 (no `s²=2`). -/
lemma g4_caseA (m : ℕ) (hPm : c m * c (m + 1) = s / 8) (hy : 1 / 2 < c (m + 1)) :
    s / 8 < c (m + 1) * c (m + 2) := by
  have hk := hrec m
  have hk1 := g4_floor_ge_one s hsp c hpos hrec m
  set K : ℝ := (⌊(1 + c m) / (s * c (m + 1))⌋ : ℝ) with hKdef
  have hK1 : (1 : ℝ) ≤ K := by rw [hKdef]; exact_mod_cast hk1
  have hc2 : c (m + 2) = K * s * c (m + 1) - c m := by linarith [hk]
  have hcpos := hpos (m + 1)
  nlinarith [hc2, hK1, hy, hPm, hsp, hcpos, mul_pos hsp hcpos,
    mul_nonneg (sub_nonneg.mpr hK1) (mul_pos hsp (mul_pos hcpos hcpos)).le,
    mul_pos hsp (mul_pos hcpos hcpos)]

include hsp hpos hrec in
/-- Case B (backward): at a t-point `c m·c(m+1) = t` with `m = j+1` and the previous
coordinate `c(j+1) > 1/2`, the t-point product itself exceeds `t` (using `P_j ≤ t`). -/
lemma g4_caseB (j : ℕ) (hPj : c j * c (j + 1) ≤ s / 8) (hx : 1 / 2 < c (j + 1)) :
    s / 8 < c (j + 1) * c (j + 2) := by
  have hk := hrec j
  have hk1 := g4_floor_ge_one s hsp c hpos hrec j
  set K : ℝ := (⌊(1 + c j) / (s * c (j + 1))⌋ : ℝ) with hKdef
  have hK1 : (1 : ℝ) ≤ K := by rw [hKdef]; exact_mod_cast hk1
  have hc2 : c (j + 2) = K * s * c (j + 1) - c j := by linarith [hk]
  have hcpos := hpos (j + 1)
  nlinarith [hc2, hK1, hx, hPj, hsp, hcpos, mul_pos hsp hcpos,
    mul_nonneg (sub_nonneg.mpr hK1) (mul_pos hsp (mul_pos hcpos hcpos)).le,
    mul_pos hsp (mul_pos hcpos hcpos)]

include hs hsp hpos hreg hrec in
/-- **t-point exclusion (q=4).** Along an orbit with every product `≤ t = s/8`, no product
equals `t` at a step `m ≥ 1`. Four cases on the t-point `(x,y) = (c m, c(m+1))`:
A `y>1/2` (forward), B `x>1/2` (backward), A′ `y∈(s/4,1/2]` with floor ≥2, Middle (floor 1
then forced floor 3). A,B done; A′,Middle staged. -/
lemma g4_not_t_at (hle : ∀ n, c n * c (n + 1) ≤ s / 8) {m : ℕ} (hm : 1 ≤ m)
    (hPm : c m * c (m + 1) = s / 8) : False := by
  obtain ⟨j, rfl⟩ : ∃ j, m = j + 1 := ⟨m - 1, by omega⟩
  -- t-point pair (x,y) = (c (j+1), c (j+2)); product = s/8
  rcases le_or_gt (c (j + 2)) (1 / 2 : ℝ) with hy | hy
  · rcases le_or_gt (c (j + 1)) (1 / 2 : ℝ) with hx | hx
    · -- Both x = c(j+1) ≤ 1/2 and y = c(j+2) ≤ 1/2.
      have hypos := hpos (j + 2)
      have hk := hrec (j + 1)
      have hk1 : (1 : ℤ) ≤ ⌊(1 + c (j + 1)) / (s * c (j + 2))⌋ :=
        g4_floor_ge_one s hsp c hpos hrec (j + 1)
      set K : ℝ := (⌊(1 + c (j + 1)) / (s * c (j + 2))⌋ : ℝ) with hKdef
      have hc3 : c (j + 3) = K * s * c (j + 2) - c (j + 1) := by linarith [hk]
      rcases le_or_gt K 1 with hK1le | hK1gt
      · -- K = 1: MIDDLE case. floor at j+1 = 1 ⟹ c(j+3) = s·y − x; this forces the next floor = 3.
        have hKeq1 : ⌊(1 + c (j + 1)) / (s * c (j + 2))⌋ = 1 := by
          have hle1 : (⌊(1 + c (j + 1)) / (s * c (j + 2))⌋ : ℝ) ≤ 1 := by rw [← hKdef]; exact hK1le
          have hle1' : ⌊(1 + c (j + 1)) / (s * c (j + 2))⌋ ≤ 1 := by exact_mod_cast hle1
          omega
        have hz : c (j + 3) = s * c (j + 2) - c (j + 1) :=
          g4_step_floor_one s c hrec (j + 1) hKeq1
        have hzpos := hpos (j + 3)
        have hsy_pos : 0 < s * c (j + 2) := mul_pos hsp (hpos (j + 2))
        have hszpos : 0 < s * c (j + 3) := mul_pos hsp hzpos
        -- s·z = 2y − s·x  (uses s² = 2)
        have hsz : s * c (j + 3) = 2 * c (j + 2) - s * c (j + 1) := by
          rw [hz]; linear_combination c (j + 2) * hs
        -- floor at j+1 = 1 ⟹ 1 + x < 2·s·y
        have hub1 : 1 + c (j + 1) < 2 * (s * c (j + 2)) := by
          have hlt := Int.lt_floor_add_one ((1 + c (j + 1)) / (s * c (j + 2)))
          rw [hKeq1] at hlt; push_cast at hlt
          rw [div_lt_iff₀ hsy_pos] at hlt; linarith [hlt]
        -- next floor = 3
        have hfloor3 : ⌊(1 + c (j + 2)) / (s * c (j + 3))⌋ = 3 := by
          rw [Int.floor_eq_iff]
          refine ⟨?_, ?_⟩
          · rw [le_div_iff₀ hszpos]; push_cast
            nlinarith [hsz, hub1, hPm, hreg (j + 1), hx, hy, hs, hsp,
              hpos (j + 1), hpos (j + 2)]
          · rw [div_lt_iff₀ hszpos]; push_cast
            nlinarith [hsz, hub1, hPm, hreg (j + 1), hx, hy, hs, hsp,
              hpos (j + 1), hpos (j + 2)]
        have hc4 : c (j + 4) = 3 * s * c (j + 3) - c (j + 2) := by
          have hr := hrec (j + 2); rw [hfloor3] at hr; push_cast at hr; linarith [hr]
        -- P_{m+2} = c(j+3)·c(j+4) = 3 s z² − (s y² − t) > t  ⟺  3 z² > y²
        have hPm2 : s / 8 < c (j + 3) * c (j + 4) := by
          nlinarith [hc4, hz, hsz, hub1, hPm, hreg (j + 1), hx, hy, hs, hsp,
            hpos (j + 1), hpos (j + 2), hzpos, mul_pos hsp hzpos]
        linarith [hle (j + 3), hPm2]
      · -- Case A′: K ≥ 2.  P_{m+1} = K·s·y² − t > t  via  K·s·y ≥ 2·s·y > 2(1−x) ≥ 2x.
        have hKge2 : (2 : ℝ) ≤ K := by
          have h1 : (1 : ℝ) < K := hK1gt
          rw [hKdef] at h1
          have h2 : (1 : ℤ) < ⌊(1 + c (j + 1)) / (s * c (j + 2))⌋ := by exact_mod_cast h1
          have h3 : (2 : ℤ) ≤ ⌊(1 + c (j + 1)) / (s * c (j + 2))⌋ := by omega
          rw [hKdef]; exact_mod_cast h3
        have hPeq : c (j + 2) * c (j + 3) = K * s * c (j + 2) ^ 2 - c (j + 1) * c (j + 2) := by
          rw [hc3]; ring
        have hPeq2 : c (j + 2) * c (j + 3) = K * s * c (j + 2) ^ 2 - s / 8 := by
          rw [hPeq, hPm]
        have hlin : 2 * c (j + 1) < K * s * c (j + 2) := by
          nlinarith [hKge2, hreg (j + 1), hx, mul_pos hsp hypos,
            mul_nonneg (by linarith [hKge2] : (0 : ℝ) ≤ K - 2) (mul_pos hsp hypos).le]
        have hgt : s / 4 < K * s * c (j + 2) ^ 2 := by nlinarith [hlin, hypos, hPm]
        linarith [hPeq2, hgt, hle (j + 2)]
    · -- Case B: x = c(j+1) > 1/2  (backward step at j)
      have hB := g4_caseB s hsp c hpos hrec j (hle j) hx
      linarith [hPm]
  · -- Case A: y = c(j+2) > 1/2  (forward step at j+1)
    have hA := g4_caseA s hsp c hpos hrec (j + 1) hPm hy
    linarith [hle (j + 2)]

end G4
