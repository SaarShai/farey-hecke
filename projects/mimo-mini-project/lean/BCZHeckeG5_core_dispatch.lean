import Mathlib
/-!
# Aristotle dispatch — q=5 (Hecke G₅, λ=φ) window-5 core `g5_core`  [TARGET = the lone `sorry`]

GOAL: prove `g5_core` (the lone `sorry` at the bottom): a 6-coordinate, 4-floor, real-arithmetic
lemma — **no 5 consecutive products `c_n·c_{n+1}` of a `T₅`-orbit segment are all `< 1/4`**. This is
the crux of the sharp `X(5) = 1/4` no-ground-state. Everything ABOVE `g5_core` is PROVEN (no `sorry`,
axioms `[propext, Classical.choice, Quot.sound]`) and is available as building blocks.

KEY ALGEBRAIC FACT: `λ = φ`, `φ² = φ + 1` (`phi_sq`). Use it as an `nlinarith`/`linear_combination`
HINT (not a rewrite), exactly as the q=4 proof uses `s² = 2`.

WHY q=5 IS HARD (read before attempting): q=5 is the first *connected-regime* case,
`V(5)=1/4 > 1/(4λ)=(√5−1)/8`. A SINGLE pair `(b,c)` with `bc<1/4` and region `b+φc>1` gives
`φc²−c+1/4>0`, whose discriminant `1−φ<0` is NEGATIVE → **vacuous** (no constraint). Contrast q=4:
the analog has discriminant `0` (tangent → the double root `(b−s/4)²` that closes `g4_core`). So no
fixed single/double-step `nlinarith` closes q=5; the contradiction is genuinely MULTI-STEP and uses
the conserved rotation quantity `E = c_n²+c_{n+1}²−φ·c_n c_{n+1}` (`E_conserved_floor_one`, proven
below). The numerics (`code/g5_*`): window-5 bound HOLDS (verified), max below-`1/4` run = 4, so 5
consecutive is impossible.

FLOOR CASE-SPLIT (the 4 floors `k₀,k₁,k₂,k₃ ≥ 1`; engine `kᵢ·φ·c_{mid}² = Pₙ+Pₙ₊₁ < 1/2` ⇒
`c_{mid}² < 1/(2φkᵢ) ≤ (φ−1)/2`, so large floors shrink the middle coords and break region):
  • **all-floor-1 (pure rotation):** DONE — `g5_rot3` below (margin huge, minmax ≈ 0.3945).
  • **HIGH-floor cases** (some `kᵢ ≥ 3`, or two `≥2`): margins > 0.38 (numerics) — kill via the
    `cᵢ² < 1/(2φkᵢ)` bounds + region, `g5_rot3`-style (no E needed).
  • **TIGHT defect cases (the real work, minmax → 1/4⁺):** exactly the cyclic embeddings of the
    optimizer word `(1,1,2)`:  floor words `(1,1,2,1)` [minmax 0.25042], `(2,1,1,2)` [0.25167],
    `(1,2,1,1)` [0.25179], and `(2,1,1,3)` [0.27968]. Here one step has `kᵢ=2`; use the floor-1
    recurrences on the surrounding rotation run + `E_conserved_floor_one` to pin the swept product
    max `≥ 1/4`, and the floor-`=2` upper/lower bounds (`g4_caseA′`-style: `K·φ·y ≥ 2φy > 2(1−x)`)
    on the defect step. The binding optimum is the orbit `c_n = R·sin((n+1)π/5)` at `R→R_lo`.

COMPILE (throwaway full Mathlib v4.28.0; trust the `EXIT=` line):
  `( ~/.elan/bin/lake env lean BCZHeckeG5_core_dispatch.lean 2>&1; echo EXIT=$? )`
DONE = `g5_core` sorry-free, `#print axioms g5_core` = `[propext, Classical.choice, Quot.sound]`.
-/
open Int
noncomputable section

/-! ## φ and its algebra (PROVEN) -/
noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2
lemma sqrt5_sq : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
lemma sqrt5_pos : (0:ℝ) < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
lemma phi_pos : 0 < phi := by unfold phi; have := sqrt5_pos; linarith
/-- `φ² = φ + 1` — the q=5 analog of `s² = 2`. Pass as an `nlinarith` hint. -/
lemma phi_sq : phi ^ 2 = phi + 1 := by unfold phi; nlinarith [sqrt5_sq, sqrt5_pos]
lemma phi_lt2 : phi < 2 := by
  unfold phi
  have h5 : Real.sqrt 5 < 3 := by
    have : Real.sqrt 5 < Real.sqrt 9 := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    simpa [show (9:ℝ) = 3^2 by norm_num, Real.sqrt_sq (by norm_num : (0:ℝ) ≤ 3)] using this
  linarith

/-! ## General-q building blocks (PROVEN; from `HeckeGeneralLB_VERIFIED.lean`, instantiate at `l=φ`) -/
section General
variable (l : ℝ) (hl : 0 < l)
variable (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
variable (hrec : ∀ n, c n + c (n + 2)
  = (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l * c (n + 1))

include hl hpos hrec in
lemma floor_ge_one (n : ℕ) : (1 : ℤ) ≤ ⌊(1 + c n) / (l * c (n + 1))⌋ := by
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

include hrec in
/-- Rotation invariant on a floor-1 step (the engine for the tight defect cases). -/
lemma E_conserved_floor_one (n : ℕ) (h1 : ⌊(1 + c n) / (l * c (n + 1))⌋ = 1) :
    c (n + 1) ^ 2 + c (n + 2) ^ 2 - l * (c (n + 1) * c (n + 2))
      = c n ^ 2 + c (n + 1) ^ 2 - l * (c n * c (n + 1)) := by
  have hk := hrec n
  rw [h1, Int.cast_one, one_mul] at hk
  have hz : c (n + 2) = l * c (n + 1) - c n := by linarith
  rw [hz]; ring
end General

/-! ## All-floor-1 (pure-rotation) sub-case — PROVEN (the easy quadrant of the case-split) -/

/-- Three consecutive floor-1 steps (recurrences `a+c=φb`, `b+d=φc`; floor-1 upper bound
`1+c < 2φd` at `(c,d)`; region `a+φb>1`) cannot have both `b·c < 1/4` and `c·d < 1/4`.
Proof: region at `(a,b)` ⇒ `2φb−c>1`; upper bound at `(c,d)` with `d=φc−b`, `φ²=φ+1` ⇒
`2φb < (2φ+1)c−1`; add ⇒ `φc>1`; with `φc²=bc+cd<1/2` and `φ<2` ⇒ contradiction. -/
theorem g5_rot3 (a b c d : ℝ)
    (hc : 0 < c)
    (hr0 : a + c = phi * b) (hr1 : b + d = phi * c)
    (hub2 : 1 + c < 2 * (phi * d)) (hreg0 : a + phi * b > 1)
    (hbc : b * c < 1 / 4) (hcd : c * d < 1 / 4) : False := by
  have hsq := phi_sq; have hpp := phi_pos; have hp2 := phi_lt2
  have hsumc : b * c + c * d = phi * c ^ 2 := by nlinarith [hr1]
  have hphic2 : phi * c ^ 2 < 1 / 2 := by nlinarith [hbc, hcd, hsumc]
  have hd_eq : d = phi * c - b := by linarith [hr1]
  have ha_eq : a = phi * b - c := by linarith [hr0]
  have hR0 : 2 * (phi * b) - c > 1 := by
    have : a + phi * b = 2 * (phi * b) - c := by rw [ha_eq]; ring
    linarith [hreg0, this]
  have hub2' : 1 + c < 2 * (phi + 1) * c - 2 * (phi * b) := by
    have hexp : 2 * (phi * d) = 2 * (phi + 1) * c - 2 * (phi * b) := by
      rw [hd_eq]; linear_combination (2 * c) * hsq
    linarith [hub2, hexp]
  have hphic_gt1 : phi * c > 1 := by nlinarith [hub2', hR0]
  nlinarith [hphic2, hphic_gt1, hc, hp2, mul_pos hc hpp,
    mul_pos hc (show (0:ℝ) < phi * c - 1 by linarith)]

/-! ## ⛔ TARGET: the window-5 core (the lone `sorry`) -/

/-- **q=5 window-5 core.** Six positive coordinates `a,b,c,d,e,f` of a `T₅`-orbit segment
(`λ=φ`): region above the cusp line on all 5 consecutive pairs, the BCZ floor recurrence with
floors `k₀..k₃ ≥ 1` and their floor *upper* bounds, CANNOT have all five products
`ab, bc, cd, de, ef` below `1/4`. [The 4-window analog is FALSE; 5 is the smallest correct window —
`research_notes/g5_window4_refutation_2026-06-02.md`.] Proof strategy in the file header; the
all-floor-1 quadrant is `g5_rot3`, the tight cases are the `(1,1,2)`-cyclic floor words. -/
theorem g5_core (a b c d e f : ℝ)
    (ha : 0 < a) (hb : 0 < b) (hc : 0 < c) (hd : 0 < d) (he : 0 < e) (hf : 0 < f)
    (hab1 : a + phi * b > 1) (hbc1 : b + phi * c > 1) (hcd1 : c + phi * d > 1)
    (hde1 : d + phi * e > 1) (hef1 : e + phi * f > 1)
    (k0 k1 k2 k3 : ℤ)
    (hk0 : a + c = (k0 : ℝ) * phi * b) (hk1 : b + d = (k1 : ℝ) * phi * c)
    (hk2 : c + e = (k2 : ℝ) * phi * d) (hk3 : d + f = (k3 : ℝ) * phi * e)
    (hk0ge : 1 ≤ k0) (hk1ge : 1 ≤ k1) (hk2ge : 1 ≤ k2) (hk3ge : 1 ≤ k3)
    -- floor upper bounds:  (1 + cₙ)/(φ·cₙ₊₁) < kₙ + 1
    (hk0f : 1 + a < ((k0 : ℝ) + 1) * (phi * b))
    (hk1f : 1 + b < ((k1 : ℝ) + 1) * (phi * c))
    (hk2f : 1 + c < ((k2 : ℝ) + 1) * (phi * d))
    (hk3f : 1 + d < ((k3 : ℝ) + 1) * (phi * e))
    (hAB : a * b < 1 / 4) (hBC : b * c < 1 / 4) (hCD : c * d < 1 / 4)
    (hDE : d * e < 1 / 4) (hEF : e * f < 1 / 4) :
    False := by
  sorry

#print axioms g5_rot3
