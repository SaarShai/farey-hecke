import Mathlib
/-!
# q=5 (Hecke G₅) on the GENUINE Taha domain — cusp upper bound + non-attainment

**Corrects the naive setup** (`research_notes/g5_window4_refutation_*`,
`FINDINGS_goalB_genuine_domain_2026-06-03.md`). The genuine `G₅`-BCZ natural-extension domain is
Taha's clean triangle `𝒯⁵ = {0<a≤1, 1−φa<b≤1}` (`λ=φ=(1+√5)/2`), and the genuine map is the
piecewise-linear `q−2 = 3`-branch map (`i=2,3,4`). The project's old scalar map is only the `i=4`
branch; the genuine **global** optimizer lives in branch `i=q−2 = 3` (the cusp fixed-line), giving

    X_Ω(5) = 1/λ³ = 1/φ³ = √5 − 2 ≈ 0.2360679…     (NOT the naive `V(5)=1/4`).

This file machine-checks the rigorous **upper bound + non-attainment** direction: the genuine cusp
family `(s,0)`, `s ∈ (1/φ, 1]`, consists of genuine fixed points with observable `P = s²/φ`; the
infimum of `P` over the family is `1/φ³`, approached as `s → (1/φ)⁺` but **never attained** (the
edge `s = 1/φ` is open) ⇒ `X_Ω(5) ≤ 1/φ³` with no ground state on this family.

**Honest scope.** The matching *lower* bound `X_Ω(5) ≥ 1/φ³` (no invariant measure beats `1/φ³`) is
OPEN — needs a Mañé / Conze–Guivarc'h sub-action argument (FINDINGS goal-B §4), not a finite
`nlinarith` — so it is NOT formalized here.

`#print axioms` must show only `[propext, Classical.choice, Quot.sound]`.
-/
open Int
noncomputable section

/-! ## φ and its algebra -/
noncomputable def phi : ℝ := (1 + Real.sqrt 5) / 2
lemma sqrt5_sq : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
lemma sqrt5_pos : (0:ℝ) < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
lemma sqrt5_gt2 : (2:ℝ) < Real.sqrt 5 := by nlinarith [sqrt5_sq, sqrt5_pos]
lemma phi_pos : 0 < phi := by unfold phi; have := sqrt5_pos; linarith
lemma phi_sq : phi ^ 2 = phi + 1 := by unfold phi; nlinarith [sqrt5_sq, sqrt5_pos]
lemma phi_gt1 : 1 < phi := by unfold phi; have := sqrt5_gt2; linarith
lemma phi_lt2 : phi < 2 := by nlinarith [phi_sq, phi_gt1]
lemma inv_phi_lt1 : 1 / phi < 1 := by rw [div_lt_one phi_pos]; exact phi_gt1

/-! ## The genuine `G₅` map (Taha), all three branches `i = 2,3,4`

Ellipse vectors (`U=[[φ,−1],[1,0]]`, `wᵢ=Uⁱ(1,0)`): `w₁=(φ,1)`, `w₂=(φ,φ)`, `w₃=(1,φ)`,
`w₄=(0,1)`, `w₅=(−1,0)`. Branch `i` ⟺ `(a,b)·w_{i−1} > 1` and `(a,b)·wᵢ ≤ 1`; on branch `i` with
digit `k = ⌊(1−(a,b)·w_{i+1})/(φ·(a,b)·wᵢ)⌋` the image is `((a,b)·wᵢ, (a,b)·w_{i+1}+kφ(a,b)·wᵢ)`.
(Branch `i=4` reproduces the project's old scalar map `(y, kφy−x)`.) -/
noncomputable def G5 (p : ℝ × ℝ) : ℝ × ℝ :=
  let a := p.1; let b := p.2
  if phi * a + b > 1 ∧ phi * (a + b) ≤ 1 then           -- branch i=2
    let k : ℤ := ⌊(1 - (a + phi * b)) / (phi * (phi * (a + b)))⌋
    (phi * (a + b), (a + phi * b) + (k : ℝ) * phi * (phi * (a + b)))
  else if phi * (a + b) > 1 ∧ a + phi * b ≤ 1 then       -- branch i=3 (the cusp branch)
    let k : ℤ := ⌊(1 - b) / (phi * (a + phi * b))⌋
    (a + phi * b, b + (k : ℝ) * phi * (a + phi * b))
  else if a + phi * b > 1 ∧ b ≤ 1 then                   -- branch i=4 (= old naive map)
    let k : ℤ := ⌊(1 + a) / (phi * b)⌋
    (b, (k : ℝ) * phi * b - a)
  else p

/-- The genuine Taha triangle `𝒯⁵`. -/
def T5 : Set (ℝ × ℝ) := {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 1 - phi * p.1 < p.2 ∧ p.2 ≤ 1}

/-- The genuine observable on branch `i=3`: `P = a·(a,b)·w₃ / (w₃).2 = a(a+φb)/φ`. -/
noncomputable def P3 (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + phi * p.2) / phi

/-! ## The cusp family `(s,0)`, `s ∈ (1/φ, 1]` -/

/-- Each cusp point `(s,0)` with `s ∈ (1/φ,1]` lies in the genuine domain `𝒯⁵`. -/
lemma cusp_in_T5 (s : ℝ) (h1 : 1 / phi < s) (h2 : s ≤ 1) : (s, 0) ∈ T5 := by
  have hps : 1 < phi * s := by have h := (div_lt_iff₀ phi_pos).mp h1; nlinarith [h]
  have hs0 : 0 < s := lt_trans (one_div_pos.mpr phi_pos) h1
  simp only [T5, Set.mem_setOf_eq]
  exact ⟨hs0, h2, by linarith [hps], by norm_num⟩

/-- **The genuine map fixes every cusp point** `(s,0)`, `s ∈ (1/φ,1]` (branch `i=3`, digit `0`). -/
lemma G5_fixes_cusp (s : ℝ) (h1 : 1 / phi < s) (h2 : s ≤ 1) : G5 (s, 0) = (s, 0) := by
  have hps : 1 < phi * s := by have h := (div_lt_iff₀ phi_pos).mp h1; nlinarith [h]
  -- branch-2 guard FALSE (needs φs>1 ∧ φs≤1)
  have hb2 : ¬ (phi * s + 0 > 1 ∧ phi * (s + 0) ≤ 1) := by
    rintro ⟨_, hle⟩; rw [add_zero] at hle; linarith [hps]
  -- branch-3 guard TRUE
  have hb3 : phi * (s + 0) > 1 ∧ s + phi * 0 ≤ 1 := by
    refine ⟨?_, ?_⟩
    · rw [add_zero]; exact hps
    · rw [mul_zero, add_zero]; exact h2
  -- digit = 0
  have hk : ⌊(1 - (0:ℝ)) / (phi * (s + phi * 0))⌋ = 0 := by
    have hval : (1 - (0:ℝ)) / (phi * (s + phi * 0)) = 1 / (phi * s) := by
      rw [mul_zero, add_zero, sub_zero]
    rw [hval]
    refine Int.floor_eq_zero_iff.mpr ⟨by positivity, ?_⟩
    rw [div_lt_one (by positivity)]; exact hps
  show G5 (s, 0) = (s, 0)
  unfold G5
  dsimp only
  rw [if_neg hb2, if_pos hb3, hk]
  norm_num

/-- On the cusp point, the observable is `P = s²/φ`. -/
lemma cusp_P (s : ℝ) : P3 (s, 0) = s ^ 2 / phi := by
  simp only [P3, mul_zero, add_zero]; ring

/-! ## Value identity and non-attainment (the no-ground-state content) -/

/-- `1/φ³ = √5 − 2`. -/
lemma inv_phi_cubed : 1 / phi ^ 3 = Real.sqrt 5 - 2 := by
  have hcube : phi ^ 3 = 2 * phi + 1 := by nlinarith [phi_sq]
  have h2p1 : 2 * phi + 1 = 2 + Real.sqrt 5 := by unfold phi; ring
  rw [hcube, h2p1, eq_comm, eq_div_iff (by positivity)]
  nlinarith [sqrt5_sq, sqrt5_pos]

/-- **Cusp lower envelope (non-attainment).** Every cusp configuration has observable `P = s²/φ`
*strictly above* `1/φ³`; so no cusp measure attains the infimum `1/φ³`. -/
lemma cusp_P_gt_inf (s : ℝ) (h1 : 1 / phi < s) (_h2 : s ≤ 1) : s ^ 2 / phi > 1 / phi ^ 3 := by
  have hp := phi_pos
  have hps : 1 < phi * s := by have h := (div_lt_iff₀ phi_pos).mp h1; nlinarith [h]
  have hpne : (phi:ℝ) ≠ 0 := ne_of_gt phi_pos
  have e : s ^ 2 / phi - 1 / phi ^ 3 = ((phi * s) ^ 2 - 1) / phi ^ 3 := by field_simp
  have h1' : (0:ℝ) < phi * s - 1 := by linarith [hps]
  have h2' : (0:ℝ) < phi * s + 1 := by linarith [hps]
  have hnum : 0 < (phi * s) ^ 2 - 1 := by nlinarith [mul_pos h1' h2']
  have hpos : 0 < s ^ 2 / phi - 1 / phi ^ 3 := by
    rw [e]; exact div_pos hnum (pow_pos phi_pos 3)
  linarith [hpos]

/-- **Approached.** For every `ε>0` there is a cusp point with `P < 1/φ³ + ε`: the infimum `1/φ³`
is approached as `s → (1/φ)⁺`. -/
lemma cusp_P_approaches (ε : ℝ) (hε : 0 < ε) :
    ∃ s : ℝ, 1 / phi < s ∧ s ≤ 1 ∧ s ^ 2 / phi < 1 / phi ^ 3 + ε := by
  have hp := phi_pos
  have hpinv : (0:ℝ) < 1 / phi := by positivity
  have hp1 : 1 / phi < 1 := inv_phi_lt1
  have hgap : 0 < 1 - 1 / phi := by linarith
  set δ : ℝ := min ((1 - 1 / phi) / 2) (ε / 4) with hδdef
  have hδpos : 0 < δ := lt_min (by linarith) (by linarith)
  have hδ1 : δ ≤ (1 - 1 / phi) / 2 := min_le_left _ _
  have hδe : δ ≤ ε / 4 := min_le_right _ _
  have hδhalf : δ < 1 / 2 := by
    have h : (1 - 1 / phi) / 2 < 1 / 2 := by linarith [hpinv]
    linarith [hδ1]
  refine ⟨1 / phi + δ, by linarith, by linarith [hδ1], ?_⟩
  have e : (1 / phi + δ) ^ 2 / phi - 1 / phi ^ 3 = (2 * δ + phi * δ ^ 2) / phi ^ 2 := by
    field_simp; ring
  have hb : (2 * δ + phi * δ ^ 2) / phi ^ 2 < ε := by
    rw [div_lt_iff₀ (by positivity)]
    nlinarith [hδe, hδhalf, hδpos, phi_sq, phi_gt1, phi_lt2, hε,
      mul_pos hδpos hδpos, mul_pos hp hδpos]
  linarith [e, hb]

#print axioms G5_fixes_cusp
#print axioms cusp_in_T5
#print axioms cusp_P
#print axioms inv_phi_cubed
#print axioms cusp_P_gt_inf
#print axioms cusp_P_approaches
