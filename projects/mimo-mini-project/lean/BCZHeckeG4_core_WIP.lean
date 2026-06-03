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

end G4
