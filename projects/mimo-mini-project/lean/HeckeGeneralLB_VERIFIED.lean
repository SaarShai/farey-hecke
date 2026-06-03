import Mathlib
/-!
Hecke BCZ ergodic optimization — GENERAL-q positive lower bound (all q at once).

Setup (any λ > 0; for Hecke take λ = 2cos(π/q)). A positive orbit `c : ℕ → ℝ` of the BCZ-type
return map on `D = {x>0, y>0, x+λy>1}`:
  * `hpos`  : `0 < c n`,
  * `hreg`  : `c n + λ·c (n+1) > 1`           (the open domain / cusp triangle),
  * `hrec`  : `c n + c (n+2) = K_n · λ · c (n+1)`, where `K_n = ⌊(1+c n)/(λ c (n+1))⌋`.
Engine identity: `P n + P (n+1) = K_n · λ · c (n+1)^2` with `P n = c n · c (n+1)` and `K_n ≥ 1`.

THEOREM `hecke_ground_value_pos`: no orbit keeps every product `P n ≤ λ/(2(1+λ)^2)`.
⇒ for every Hecke group the ergodic-optimization infimum `X(q) ≥ λ/(2(1+λ)^2) > 0`
   (uniform positive ground value — never collapses to 0; valid for ALL q at once).
Sharp value is larger (q=3: 2/9, q=4: √2/8, …); this is the clean uniform lower bound.
-/
open Int

section General
variable (l : ℝ) (hl : 0 < l)
variable (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
variable (hreg : ∀ n, c n + l * c (n + 1) > 1)
variable (hrec : ∀ n, c n + c (n + 2)
  = (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l * c (n + 1))

include hl hpos hrec in
/-- The BCZ floor is always ≥ 1 (otherwise the next coordinate would be ≤ 0). -/
lemma floor_ge_one (n : ℕ) :
    (1 : ℤ) ≤ ⌊(1 + c n) / (l * c (n + 1))⌋ := by
  by_contra hcon
  push_neg at hcon
  have hle : ⌊(1 + c n) / (l * c (n + 1))⌋ ≤ 0 := by omega
  have hkle : (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) ≤ 0 := by exact_mod_cast hle
  have hk := hrec n
  have hks : (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l ≤ 0 :=
    mul_nonpos_iff.mpr (Or.inr ⟨hkle, hl.le⟩)
  have hksc : (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l * c (n + 1) ≤ 0 :=
    mul_nonpos_iff.mpr (Or.inr ⟨hks, (hpos (n + 1)).le⟩)
  linarith [hk, hpos n, hpos (n + 2)]

include hl hpos hrec in
/-- Engine: `P n + P (n+1) = K_n · l · c(n+1)^2 ≥ l · c(n+1)^2` (since `K_n ≥ 1`). -/
lemma engine_le (n : ℕ) :
    l * c (n + 1) ^ 2 ≤ c n * c (n + 1) + c (n + 1) * c (n + 2) := by
  have hk := hrec n
  have hk1 := floor_ge_one l hl c hpos hrec n
  set K : ℝ := (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) with hKdef
  have hK1 : (1 : ℝ) ≤ K := by rw [hKdef]; exact_mod_cast hk1
  have hcpos := hpos (n + 1)
  have h2 : c n + c (n + 2) = K * l * c (n + 1) := hk
  have hsum : c n * c (n + 1) + c (n + 1) * c (n + 2) = K * l * c (n + 1) ^ 2 := by
    linear_combination c (n + 1) * h2
  rw [hsum]
  nlinarith [hK1, hl, sq_nonneg (c (n + 1)),
    mul_nonneg (sub_nonneg.mpr hK1) (by positivity : (0:ℝ) ≤ l * c (n + 1) ^ 2)]

include hl hpos hreg hrec in
/-- **General-q positive ground value.** No orbit keeps every product `≤ l/(2(1+l)^2)`.
Hence the ergodic-optimization infimum satisfies `X ≥ l/(2(1+l)^2) > 0` for every `l > 0`
(in particular every Hecke `l = 2cos(π/q)`): the ground value never collapses to 0. -/
theorem hecke_ground_value_pos :
    ¬ (∀ n, c n * c (n + 1) ≤ l / (2 * (1 + l) ^ 2)) := by
  intro hle
  have h1l : 0 < 1 + l := by linarith
  -- Step 1: for every n, c(n+1) ≤ 1/(1+l).
  have key : ∀ n, c (n + 1) ≤ 1 / (1 + l) := by
    intro n
    have he := engine_le l hl c hpos hrec n
    have hPn := hle n
    have hPn1 := hle (n + 1)
    have hcpos := hpos (n + 1)
    -- l·c(n+1)^2 ≤ 2·(l/(2(1+l)^2)) = l/(1+l)^2
    have h2B : (2 : ℝ) * (l / (2 * (1 + l) ^ 2)) = l / (1 + l) ^ 2 := by
      field_simp
    have hsq : l * c (n + 1) ^ 2 ≤ l / (1 + l) ^ 2 := by nlinarith [he, hPn, hPn1, h2B]
    -- divide by l: c(n+1)^2 ≤ 1/(1+l)^2
    have hsq2 : c (n + 1) ^ 2 ≤ 1 / (1 + l) ^ 2 := by
      have hrw : l / (1 + l) ^ 2 = l * (1 / (1 + l) ^ 2) := by ring
      rw [hrw] at hsq
      exact le_of_mul_le_mul_left hsq hl
    -- conclude c(n+1) ≤ 1/(1+l) using nonnegativity
    have hb : (0 : ℝ) < 1 / (1 + l) := by positivity
    have hbsq : (1 / (1 + l)) ^ 2 = 1 / (1 + l) ^ 2 := by rw [div_pow, one_pow]
    nlinarith [hsq2, hcpos, hb, hbsq, mul_pos hb hb, sq_nonneg (c (n + 1) - 1 / (1 + l))]
  -- Step 2: domain at n=1 gives c 1 + l·c 2 ≤ 1, contradicting hreg 1 (> 1).
  have e : 1 / (1 + l) + l * (1 / (1 + l)) = 1 := by field_simp
  have hub : c 1 + l * c 2 ≤ 1 := by
    nlinarith [key 0, key 1, hl, e, mul_nonneg hl.le (sub_nonneg.mpr (key 1))]
  linarith [hreg 1, hub]

include hrec in
/-- Conserved quantity on a floor-1 (rotation) step: `E = c_n² + c_{n+1}² − l·c_n c_{n+1}` is
preserved (the rotation invariant; on the optimizer family `E = R² sin²(π/q)`). -/
lemma E_conserved_floor_one (n : ℕ)
    (h1 : ⌊(1 + c n) / (l * c (n + 1))⌋ = 1) :
    c (n + 1) ^ 2 + c (n + 2) ^ 2 - l * (c (n + 1) * c (n + 2))
      = c n ^ 2 + c (n + 1) ^ 2 - l * (c n * c (n + 1)) := by
  have hk := hrec n
  rw [h1, Int.cast_one, one_mul] at hk
  have hz : c (n + 2) = l * c (n + 1) - c n := by linarith
  rw [hz]; ring

end General

#print axioms hecke_ground_value_pos
#print axioms E_conserved_floor_one
