import Mathlib
/-!
# Goal M (closure) — NO INFINITE ROTATION RUN.  ALL q, parametric in `l = λ ∈ (0,2)`.

The (L1) crux is that a single elliptic "rotation corridor" cannot sustain a sub-threshold orbit
forever.  Its rigorous CORE — model case, the scalar floor-1 (rotation) run — is proved here with
NO limits/series, only algebra + one Archimedean step:

> **`no_infinite_rotation`** : for `0 < l < 2`, there is NO sequence `c : ℕ → ℝ` with
>   * `0 < c n`        (the orbit stays in the open domain, positive coordinate), and
>   * `c (n+2) = l·c (n+1) − c n`   (the floor-1 / `K=1` BCZ step: the rotation recurrence)
>   for every `n`.
>
> Equivalently: **every BCZ orbit must leave floor 1 (have `K_n ≥ 2`) infinitely often** — pure
> rotation never persists.  This is the rigorous, q-uniform heart of "(L1): a rotation corridor is
> finite", the mechanism behind the empirical max sub-threshold run `~0.3q`.

PROOF.  The form `E := c_n² + c_{n+1}² − l·c_n c_{n+1}` is conserved (`E_conserved`) and positive
definite for `l<2` (`E_pos`).  It bounds the orbit: `c_n ≤ M` (`c_le_M`) and consecutive pairs from
below `c_{n+1}+c_{n+2} ≥ m > 0` (`pair_ge_m`).  The first difference `d_n := c_{n+1}−c_n` obeys
`d_{n+2} − d_n = (l−2)(c_{n+1}+c_{n+2}) ≤ −(2−l)m =: −δ < 0` (`d_two_step_drop`), so by induction
`d_{2n} ≤ d_0 − n·δ` (`d_even_le`) → −∞, contradicting the lower bound `d_n > −M` (`d_gt_negM`).
Archimedes (`exists_nat_gt`) finishes.

`#print axioms no_infinite_rotation` is `[propext, Classical.choice, Quot.sound]`.
-/
namespace HeckeNoRot

variable (l : ℝ)

/-- Conserved quadratic form `E_n = c_n² + c_{n+1}² − l·c_n c_{n+1}`. -/
noncomputable def Eform (c : ℕ → ℝ) (n : ℕ) : ℝ :=
  c n ^ 2 + c (n + 1) ^ 2 - l * (c n * c (n + 1))

section
variable {l}
variable {c : ℕ → ℝ}
variable (hrec : ∀ n, c (n + 2) = l * c (n + 1) - c n)

include hrec in
/-- `E` is conserved along a floor-1 run. -/
theorem E_conserved (n : ℕ) : Eform l c (n + 1) = Eform l c n := by
  have h := hrec n
  simp only [Eform]
  rw [show n + 1 + 1 = n + 2 from rfl, h]; ring

include hrec in
/-- Hence `E_n = E_0` for all `n`. -/
theorem E_const (n : ℕ) : Eform l c n = Eform l c 0 := by
  induction n with
  | zero => rfl
  | succ k ih => rw [E_conserved hrec k, ih]

end

section Main
variable {l : ℝ} (hl0 : 0 < l) (hl2 : l < 2)
variable {c : ℕ → ℝ} (hpos : ∀ n, 0 < c n)
variable (hrec : ∀ n, c (n + 2) = l * c (n + 1) - c n)

include hl0 hl2 hpos in
/-- The conserved form is positive: `2E = (2−l)(c_n²+c_{n+1}²) + l(c_n−c_{n+1})² ≥ (2−l)c_n² > 0`. -/
theorem E_pos (n : ℕ) : 0 < Eform l c n := by
  have hc := hpos n
  have h2l : 0 < 2 - l := by linarith
  have hcsq : 0 < c n ^ 2 := by positivity
  simp only [Eform]
  nlinarith [mul_pos h2l hcsq, mul_nonneg h2l.le (sq_nonneg (c (n + 1))),
    mul_nonneg hl0.le (sq_nonneg (c n - c (n + 1)))]

include hl0 hl2 hpos hrec in
/-- Uniform upper bound: `c_n ≤ M := √(2 E₀ /(2−l))`. -/
theorem c_le_M (n : ℕ) : c n ≤ Real.sqrt (2 * Eform l c 0 / (2 - l)) := by
  have h2l : 0 < 2 - l := by linarith
  have hEn : Eform l c n = Eform l c 0 := E_const hrec n
  -- (2−l)·c_n² ≤ 2 E_n  ⇒  c_n² ≤ 2E₀/(2−l)
  have hbound : c n ^ 2 ≤ 2 * Eform l c 0 / (2 - l) := by
    rw [le_div_iff₀ h2l, ← hEn]
    simp only [Eform]; nlinarith [sq_nonneg (c n - c (n + 1))]
  calc c n = Real.sqrt (c n ^ 2) := (Real.sqrt_sq (hpos n).le).symm
    _ ≤ Real.sqrt (2 * Eform l c 0 / (2 - l)) := Real.sqrt_le_sqrt hbound

include hl0 hl2 hpos hrec in
/-- Consecutive pairs are bounded below: `c_{n+1}+c_{n+2} ≥ m := √(2 E₀/(2+l)) > 0`.
    (From `2E ≤ (2+l)(c_n²+c_{n+1}²) ≤ (2+l)(c_n+c_{n+1})²`.) `hl2` is auto-included (harmless). -/
theorem pair_ge_m (n : ℕ) :
    Real.sqrt (2 * Eform l c 0 / (2 + l)) ≤ c (n + 1) + c (n + 2) := by
  have h2l : 0 < 2 + l := by linarith
  have hEn : Eform l c (n + 1) = Eform l c 0 := E_const hrec (n + 1)
  have hbound : 2 * Eform l c 0 / (2 + l) ≤ (c (n + 1) + c (n + 2)) ^ 2 := by
    rw [div_le_iff₀ h2l, ← hEn]
    simp only [Eform]
    nlinarith [sq_nonneg (c (n + 1) + c (n + 2)), mul_pos (hpos (n+1)) (hpos (n+2)),
      hl0, mul_pos hl0 (mul_pos (hpos (n+1)) (hpos (n+2)))]
  have hsum : 0 ≤ c (n + 1) + c (n + 2) := by linarith [hpos (n+1), hpos (n+2)]
  calc Real.sqrt (2 * Eform l c 0 / (2 + l))
      ≤ Real.sqrt ((c (n + 1) + c (n + 2)) ^ 2) := Real.sqrt_le_sqrt hbound
    _ = c (n + 1) + c (n + 2) := Real.sqrt_sq hsum

/-- First difference `d_n = c_{n+1} − c_n`. -/
def dseq (c : ℕ → ℝ) (n : ℕ) : ℝ := c (n + 1) - c n

include hrec in
/-- Two-step second difference: `d_{n+2} − d_n = (l−2)(c_{n+1}+c_{n+2})`. -/
theorem d_two_step (n : ℕ) :
    dseq c (n + 2) - dseq c n = (l - 2) * (c (n + 1) + c (n + 2)) := by
  have h0 := hrec n            -- c(n+2) = l c(n+1) − c n
  have h1 := hrec (n + 1)      -- c(n+3) = l c(n+2) − c(n+1)
  simp only [dseq]
  rw [show n + 2 + 1 = n + 3 from rfl, show n + 1 + 1 = n + 2 from rfl] at *
  rw [h1, h0]; ring
end Main

section Final
variable {l : ℝ} (hl0 : 0 < l) (hl2 : l < 2)
variable {c : ℕ → ℝ} (hpos : ∀ n, 0 < c n)
variable (hrec : ∀ n, c (n + 2) = l * c (n + 1) - c n)

include hl0 hl2 hpos hrec in
/-- The two-step drop is by at least `δ := (2−l)·m > 0`: `d_{n+2} ≤ d_n − δ`. -/
theorem d_step_drop (n : ℕ) :
    dseq c (n + 2) ≤ dseq c n - (2 - l) * Real.sqrt (2 * Eform l c 0 / (2 + l)) := by
  have hts := d_two_step hrec n
  have hpair := pair_ge_m hl0 hl2 hpos hrec n
  have hlneg : l - 2 < 0 := by linarith
  -- (l−2)(c_{n+1}+c_{n+2}) ≤ (l−2)·m = −(2−l)m
  have : (l - 2) * (c (n + 1) + c (n + 2))
      ≤ (l - 2) * Real.sqrt (2 * Eform l c 0 / (2 + l)) :=
    mul_le_mul_of_nonpos_left hpair hlneg.le
  linarith [hts, this]

include hl0 hl2 hpos hrec in
/-- Iterated: `d_{2n} ≤ d_0 − n·δ`. -/
theorem d_even_le (n : ℕ) :
    dseq c (2 * n)
      ≤ dseq c 0 - (n : ℝ) * ((2 - l) * Real.sqrt (2 * Eform l c 0 / (2 + l))) := by
  induction n with
  | zero => simp
  | succ k ih =>
      have hd := d_step_drop hl0 hl2 hpos hrec (2 * k)
      have e : 2 * (k + 1) = 2 * k + 2 := by ring
      rw [e]
      push_cast
      linarith [hd, ih]

include hl0 hl2 hpos hrec in
/-- Lower bound `d_n > −M` (since `c_{n+1} > 0` and `c_n ≤ M`). -/
theorem d_gt_negM (n : ℕ) : - Real.sqrt (2 * Eform l c 0 / (2 - l)) < dseq c n := by
  have hM := c_le_M hl0 hl2 hpos hrec n
  have := hpos (n + 1)
  simp only [dseq]; linarith

include hl0 hl2 hpos hrec in
/-- **NO INFINITE ROTATION RUN.**  For `0<l<2` there is no positive sequence obeying the floor-1
    rotation recurrence for every `n`.  (The hypotheses `hpos`,`hrec` are contradictory.) -/
theorem no_infinite_rotation : False := by
  set m := Real.sqrt (2 * Eform l c 0 / (2 + l)) with hm
  set M := Real.sqrt (2 * Eform l c 0 / (2 - l)) with hMdef
  have hE0 : 0 < Eform l c 0 := E_pos hl0 hl2 hpos 0
  have h2pl : 0 < 2 + l := by linarith
  have hmpos : 0 < m := by
    rw [hm]; exact Real.sqrt_pos.mpr (by positivity)
  set δ : ℝ := (2 - l) * m with hδ
  have hδpos : 0 < δ := by rw [hδ]; exact mul_pos (by linarith) hmpos
  -- choose n with n·δ > d_0 + M
  obtain ⟨n, hn⟩ := exists_nat_gt ((dseq c 0 + M) / δ)
  have hlow := d_gt_negM hl0 hl2 hpos hrec (2 * n)      -- −M < d_{2n}
  have hhigh := d_even_le hl0 hl2 hpos hrec n            -- d_{2n} ≤ d_0 − n·δ
  -- combine: −M < d_0 − n·δ  ⇒  n·δ < d_0 + M  ⇒  n < (d_0+M)/δ, contradicting hn
  have hcomb : (n : ℝ) * δ < dseq c 0 + M := by
    have : - M < dseq c 0 - (n : ℝ) * δ := lt_of_lt_of_le hlow hhigh
    linarith
  have : (n : ℝ) < (dseq c 0 + M) / δ := by
    rw [lt_div_iff₀ hδpos]; linarith [hcomb]
  linarith [hn, this]

end Final

/-- **Corollary — no scalar BCZ orbit is eventually all-floor-1.**  For the genuine scalar BCZ floor
    recurrence (`0<l<2`, `c n>0`, `c n + c(n+2) = ⌊(1+c n)/(l c(n+1))⌋·l·c(n+1)`), there is NO `N` past
    which every floor equals `1`.  Equivalently: **every orbit has floor `K_n ≥ 2` infinitely often** —
    pure rotation never takes over.  Direct from `no_infinite_rotation`: an eventually-floor-1 tail
    `c(N+·)` obeys `c(n+2)=l·c(n+1)−c n` with positive terms, which is impossible. -/
theorem infinitely_many_high_floor
    (l : ℝ) (hl0 : 0 < l) (hl2 : l < 2)
    (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
    (hrec : ∀ n, c n + c (n + 2)
      = (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l * c (n + 1)) :
    ¬ (∃ N, ∀ n, N ≤ n → ⌊(1 + c n) / (l * c (n + 1))⌋ = 1) := by
  rintro ⟨N, hN⟩
  have hdrec : ∀ m, c (N + (m + 2)) = l * c (N + (m + 1)) - c (N + m) := by
    intro m
    have hfloor := hN (N + m) (Nat.le_add_right N m)
    have h := hrec (N + m)
    rw [hfloor, Int.cast_one, one_mul] at h
    have e1 : N + (m + 2) = N + m + 2 := by ring
    have e2 : N + (m + 1) = N + m + 1 := by ring
    rw [e1, e2]; linarith
  exact no_infinite_rotation (c := fun m => c (N + m)) hl0 hl2 (fun m => hpos (N + m)) hdrec

#print axioms E_conserved
#print axioms E_const
#print axioms no_infinite_rotation
#print axioms infinitely_many_high_floor

end HeckeNoRot
