import Mathlib
/-!
# q=5 (Hecke G₅, λ=φ) — SHARP value V(5)=1/4: the t-point exclusion lemma (NEW, 2026-06-03).

The "1/4-point exclusion" left CONJECTURAL by goal C is machine-checked here. At an exact t-point
P_m = c_m·c_{m+1} = 1/4 inside an in-D orbit with all products ≤1/4, a forward product is forced
> 1/4 within ≤3 steps. With a window-5 bound (the remaining gap) this gives sharp X(5)=1/4 + no GS.

Cases at t-point (x,y)=(c_m,c_{m+1}), x,y∈[a,b], b²=1/(2φ), a²=φ/8, ab=1/4, floor Km≥1:
 (I)   Km≥2 ⟹ P_{m+1}=Km φ y²−1/4 ≥ 2φy²−1/4 ≥ φ/4 > 1/4   (uses y²≥φ/8).
 (k=1) hreg forces y>1/2  (4(φ+2)y²−4y−φ=(2y−1)(2(φ+2)y+φ)).
 (III) k=1, y∈(½,b]: K_{m+1}=2; then 2z²>y² ⟹ P_{m+2}>1/4 (IIIa), else K_{m+2}=1 and
       P_{m+3}=φw²−P_{m+2}>1/4 (IIIb).  z=φy−x, w=2φz−y.
-/
open Int
set_option maxHeartbeats 1600000
noncomputable section

def phi : ℝ := (1 + Real.sqrt 5) / 2
lemma sqrt5_sq : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
lemma sqrt5_pos : (0:ℝ) < Real.sqrt 5 := Real.sqrt_pos.mpr (by norm_num)
lemma phi_pos : 0 < phi := by unfold phi; have := sqrt5_pos; linarith
lemma phi_sq : phi ^ 2 = phi + 1 := by unfold phi; nlinarith [sqrt5_sq, sqrt5_pos]
lemma phi_gt_one : 1 < phi := by
  have h2 : (2:ℝ) < Real.sqrt 5 := by nlinarith [sqrt5_sq, sqrt5_pos]
  unfold phi; linarith
lemma phi_lt_two : phi < 2 := by
  have h3 : Real.sqrt 5 < 3 := by nlinarith [sqrt5_sq, sqrt5_pos]
  unfold phi; linarith

section Orbit
variable (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
variable (hreg : ∀ n, c n + phi * c (n + 1) > 1)
variable (hrec : ∀ n, c n + c (n + 2)
  = (⌊(1 + c n) / (phi * c (n + 1))⌋ : ℝ) * phi * c (n + 1))

include hpos hrec in
lemma floor_ge_one (n : ℕ) : (1 : ℤ) ≤ ⌊(1 + c n) / (phi * c (n + 1))⌋ := by
  by_contra hcon
  push_neg at hcon
  have hle : ⌊(1 + c n) / (phi * c (n + 1))⌋ ≤ 0 := by omega
  have hkle : (⌊(1 + c n) / (phi * c (n + 1))⌋ : ℝ) ≤ 0 := by exact_mod_cast hle
  have hk := hrec n
  have hks : (⌊(1 + c n) / (phi * c (n + 1))⌋ : ℝ) * phi ≤ 0 :=
    mul_nonpos_iff.mpr (Or.inr ⟨hkle, phi_pos.le⟩)
  have hksc : (⌊(1 + c n) / (phi * c (n + 1))⌋ : ℝ) * phi * c (n + 1) ≤ 0 :=
    mul_nonpos_iff.mpr (Or.inr ⟨hks, (hpos (n + 1)).le⟩)
  linarith [hk, hpos n, hpos (n + 2)]

include hpos hrec in
lemma engine_le (n : ℕ) :
    phi * c (n + 1) ^ 2 ≤ c n * c (n + 1) + c (n + 1) * c (n + 2) := by
  have hk := hrec n
  have hk1 := floor_ge_one c hpos hrec n
  set K : ℝ := (⌊(1 + c n) / (phi * c (n + 1))⌋ : ℝ) with hKdef
  have hK1 : (1 : ℝ) ≤ K := by rw [hKdef]; exact_mod_cast hk1
  have hcpos := hpos (n + 1)
  have h2 : c n + c (n + 2) = K * phi * c (n + 1) := hk
  have hsum : c n * c (n + 1) + c (n + 1) * c (n + 2) = K * phi * c (n + 1) ^ 2 := by
    linear_combination c (n + 1) * h2
  rw [hsum]
  nlinarith [hK1, phi_pos, sq_nonneg (c (n + 1)),
    mul_nonneg (sub_nonneg.mpr hK1) (mul_nonneg phi_pos.le (sq_nonneg (c (n + 1))))]

include hpos hreg hrec in
/-- **q=5 t-point exclusion.** In an in-D orbit with all products ≤ 1/4, no exact t-point
`c_m c_{m+1} = 1/4` (m≥1) can be sustained: a forward product exceeds 1/4. -/
theorem g5_tpoint_excl (hle : ∀ n, c n * c (n + 1) ≤ 1 / 4)
    {m : ℕ} (hm : 1 ≤ m) (hP : c m * c (m + 1) = 1 / 4) : False := by
  obtain ⟨j, rfl⟩ : ∃ j, m = j + 1 := ⟨m - 1, by omega⟩
  -- name the relevant coordinates
  set x := c (j + 1) with hxdef
  set y := c (j + 2) with hydef
  set z := c (j + 3) with hzdef
  set w := c (j + 4) with hwdef
  have hx0 : 0 < x := hpos (j + 1)
  have hy0 : 0 < y := hpos (j + 2)
  have hxy : x * y = 1 / 4 := hP
  -- coordinate bounds 2φx²≤1, 2φy²≤1
  have hy2 : 2 * phi * y ^ 2 ≤ 1 := by
    have he : phi * y ^ 2 ≤ x * y + y * z := engine_le c hpos hrec (j + 1)
    have h1 : x * y ≤ 1 / 4 := hle (j + 1)
    have h2 : y * z ≤ 1 / 4 := hle (j + 2)
    nlinarith [he, h1, h2]
  have hx2 : 2 * phi * x ^ 2 ≤ 1 := by
    have he : phi * x ^ 2 ≤ c j * x + x * y := engine_le c hpos hrec j
    have h0 : c j * x ≤ 1 / 4 := hle j
    have h1 : x * y ≤ 1 / 4 := hle (j + 1)
    nlinarith [he, h0, h1]
  -- y² ≥ φ/8
  have hxy2 : (x * y) ^ 2 = 1 / 16 := by rw [hxy]; norm_num
  have hyge : 8 * y ^ 2 ≥ phi := by
    nlinarith [hxy2, phi_pos,
      mul_nonneg (sq_nonneg y) (by linarith [hx2] : (0:ℝ) ≤ 1 - 2 * phi * x ^ 2)]
  -- floor at j+1
  have hKm1 : (1 : ℤ) ≤ ⌊(1 + x) / (phi * y)⌋ := floor_ge_one c hpos hrec (j + 1)
  have hrecm : x + z = (⌊(1 + x) / (phi * y)⌋ : ℝ) * phi * y := hrec (j + 1)
  rcases lt_or_ge ⌊(1 + x) / (phi * y)⌋ 2 with hKlt | hKge
  · -- Km = 1
    have hKeq : ⌊(1 + x) / (phi * y)⌋ = 1 := by omega
    rw [hKeq] at hrecm; push_cast at hrecm
    have hzval : z = phi * y - x := by linarith [hrecm]
    -- hreg at j+2 forces y > 1/2
    have hregm : y + phi * z > 1 := hreg (j + 2)
    have hreg2 : (phi + 2) * y - phi * x > 1 := by
      have : y + phi * (phi * y - x) > 1 := by rw [← hzval]; exact hregm
      nlinarith [this, phi_sq, hy0]
    have hpxy : phi * x * y = phi / 4 := by
      have : phi * (x * y) = phi * (1 / 4) := by rw [hxy]
      nlinarith [this]
    have hprod : ((phi + 2) * y - phi * x - 1) * y > 0 := mul_pos (by linarith [hreg2]) hy0
    have hH : 4 * (phi + 2) * y ^ 2 - 4 * y - phi > 0 := by nlinarith [hprod, hpxy]
    have hpf : 0 < 2 * (phi + 2) * y + phi := by nlinarith [phi_pos, hy0]
    have hfac : 4 * (phi + 2) * y ^ 2 - 4 * y - phi
        = (2 * y - 1) * (2 * (phi + 2) * y + phi) := by ring
    have hygt : 1 / 2 < y := by
      rcases le_or_gt y (1 / 2) with h | h
      · exfalso
        have hle0 : (2 * y - 1) * (2 * (phi + 2) * y + phi) ≤ 0 :=
          mul_nonpos_of_nonpos_of_nonneg (by linarith) hpf.le
        rw [← hfac] at hle0; linarith [hH]
      · exact h
    -- ===== Case III: k=1, y∈(½,b]. Forward ≤3 steps. =====
    -- z > 0
    have h4 : 4 * y * z = 4 * phi * y ^ 2 - 1 := by rw [hzval]; linear_combination (-4) * hxy
    have hz0 : 0 < z := by nlinarith [h4, hygt, phi_gt_one, hy0]
    have hphz : 0 < phi * z := mul_pos phi_pos hz0
    -- floor K_{m+1} = 2 via explicit polynomial certificates
    have h8 : 4 * y * (2 * (phi * z)) = (8 * phi + 8) * y ^ 2 - 2 * phi := by
      rw [hzval]; linear_combination (8 * y ^ 2) * phi_sq + (-8 * phi) * hxy
    have hidA : (8 * phi + 4) * y ^ 2 - 4 * y - 2 * phi
        = (2 * phi + 2) * (2 * phi * y ^ 2 - 1) - 2 * (2 * y - 1) := by
      linear_combination (-4 * y ^ 2) * phi_sq
    have hcertA : (8 * phi + 4) * y ^ 2 - 4 * y - 2 * phi ≤ 0 := by
      rw [hidA]; nlinarith [hy2, hygt, phi_pos]
    have hbnd_lo : 2 * (phi * z) ≤ 1 + y := by nlinarith [h8, hcertA, hy0]
    have hphzy : 4 * y * (phi * z) = (4 * phi + 4) * y ^ 2 - phi := by
      rw [hzval]; linear_combination (4 * y ^ 2) * phi_sq + (-4 * phi) * hxy
    have hidB : (12 * phi + 8) * y ^ 2 - 4 * y - 3 * phi
        = (2 * y - 1) * ((6 * phi + 4) * y + 3 * phi) := by ring
    have hcertB : (12 * phi + 8) * y ^ 2 - 4 * y - 3 * phi > 0 := by
      rw [hidB]
      exact mul_pos (by linarith [hygt]) (by nlinarith [phi_pos, hy0])
    have hbnd_hi : 1 + y < 3 * (phi * z) := by nlinarith [hphzy, hcertB, hy0]
    have hK1floor : ⌊(1 + y) / (phi * z)⌋ = (2 : ℤ) := by
      rw [Int.floor_eq_iff]
      refine ⟨?_, ?_⟩
      · rw [le_div_iff₀ hphz]; push_cast; linarith [hbnd_lo]
      · rw [div_lt_iff₀ hphz]; push_cast; nlinarith [hbnd_hi]
    -- w = 2φz − y
    have hrecm1 : y + w = (⌊(1 + y) / (phi * z)⌋ : ℝ) * phi * z := hrec (j + 2)
    rw [hK1floor] at hrecm1; push_cast at hrecm1
    have hwval : w = 2 * phi * z - y := by linarith [hrecm1]
    -- key inequality (10φ+6)y² + (6φ+4)x² > 4φ+5/2  (SOS cert, needs y²>1/4)
    have hu14 : (1 : ℝ) / 4 < y ^ 2 := by nlinarith [hygt, hy0]
    have hQ : ((10 * phi + 6) * y ^ 2 + (6 * phi + 4) * x ^ 2 - (4 * phi + 5 / 2)) * y ^ 2
        = (10 * phi + 6) * (y ^ 2 - 1 / 4) ^ 2 + ((2 * phi + 1) / 2) * (y ^ 2 - 1 / 4) := by
      linear_combination (6 * phi + 4) * hxy2
    have hQpos : ((10 * phi + 6) * y ^ 2 + (6 * phi + 4) * x ^ 2 - (4 * phi + 5 / 2)) * y ^ 2 > 0 := by
      rw [hQ]
      have h1 : (0:ℝ) ≤ (10 * phi + 6) * (y ^ 2 - 1 / 4) ^ 2 :=
        mul_nonneg (by nlinarith [phi_pos]) (sq_nonneg _)
      have h2 : (0:ℝ) < ((2 * phi + 1) / 2) * (y ^ 2 - 1 / 4) :=
        mul_pos (by nlinarith [phi_pos]) (by linarith [hu14])
      linarith
    have hbig : (10 * phi + 6) * y ^ 2 + (6 * phi + 4) * x ^ 2 > 4 * phi + 5 / 2 := by
      nlinarith [hQpos, mul_pos hy0 hy0]
    -- φw² − wz − 1/4 = (10φ+6)y²+(6φ+4)x²−(4φ+5/2)  (identity), so > 0 by hbig
    have hid : phi * w ^ 2 - w * z - 1 / 4
        = (10 * phi + 6) * y ^ 2 + (6 * phi + 4) * x ^ 2 - (4 * phi + 5 / 2) := by
      rw [hwval, hzval]
      linear_combination (4 * phi ^ 3 * y ^ 2 - 8 * phi ^ 2 * x * y + 4 * phi ^ 2 * y ^ 2
          + 4 * phi * x ^ 2 - 8 * phi * x * y + 2 * phi * y ^ 2 + 4 * x ^ 2 - 8 * x * y
          + 6 * y ^ 2) * phi_sq + (-16 * phi - 9) * hxy
    have hfinal : phi * w ^ 2 - w * z > 1 / 4 := by linarith [hid, hbig]
    -- step 3: K_{m+2} ≥ 1 ⟹ P_{m+3} = K·φw² − wz ≥ φw² − wz > 1/4, contradicting hle(j+4)
    have hK2 : (1 : ℤ) ≤ ⌊(1 + z) / (phi * w)⌋ := floor_ge_one c hpos hrec (j + 3)
    have hK2r : (1 : ℝ) ≤ (⌊(1 + z) / (phi * w)⌋ : ℝ) := by exact_mod_cast hK2
    have hrecm2 : z + c (j + 5) = (⌊(1 + z) / (phi * w)⌋ : ℝ) * phi * w := hrec (j + 3)
    have hc5 : c (j + 5) = (⌊(1 + z) / (phi * w)⌋ : ℝ) * phi * w - z := by linarith [hrecm2]
    have hwc5 : w * c (j + 5) ≤ 1 / 4 := hle (j + 4)
    rw [hc5] at hwc5
    have hPm3 : phi * w ^ 2 - w * z ≤ 1 / 4 := by
      nlinarith [hwc5, mul_nonneg (by linarith [hK2r] : (0:ℝ) ≤ (⌊(1 + z) / (phi * w)⌋ : ℝ) - 1)
        (mul_nonneg phi_pos.le (sq_nonneg w))]
    linarith [hPm3, hfinal]
  · -- Km ≥ 2 : Case I
    have hKreal : (2 : ℝ) ≤ (⌊(1 + x) / (phi * y)⌋ : ℝ) := by exact_mod_cast hKge
    have hzval : z = (⌊(1 + x) / (phi * y)⌋ : ℝ) * phi * y - x := by linarith [hrecm]
    have hP1 : y * z ≤ 1 / 4 := hle (j + 2)
    rw [hzval] at hP1
    have hP1' : (⌊(1 + x) / (phi * y)⌋ : ℝ) * phi * y ^ 2 ≤ 1 / 2 := by nlinarith [hP1, hxy]
    have hkey : 2 * phi * y ^ 2 ≤ (⌊(1 + x) / (phi * y)⌋ : ℝ) * phi * y ^ 2 := by
      nlinarith [hKreal, mul_pos phi_pos (mul_pos hy0 hy0)]
    nlinarith [hP1', hkey, hyge, phi_sq, phi_gt_one, phi_pos,
      mul_nonneg phi_pos.le (by linarith [hyge] : (0:ℝ) ≤ 8 * y ^ 2 - phi)]

end Orbit
#print axioms g5_tpoint_excl

/-! ## Sharp X(5)=1/4 + no ground state, conditional on the window-5 bound.

The ONE remaining gap is the window-5 bound `Q5Window`: along every in-D orbit, every window of
5 consecutive products contains one `≥ 1/4` (equivalently no 5 consecutive products are `< 1/4`).
This is the lower bound `X(5) ≥ 1/4` itself; it is NUMERICALLY CERTIFIED (longest sub-1/4 run = 4,
three independent methods + hill-climb) but its hand/Lean proof — the connected-regime multi-step
dynamics — is the analog of q=3's machine-checked v8 cluster bound and is not yet discharged.
Everything BELOW is machine-checked CONDITIONAL on `Q5Window`. -/

/-- **Window-5 bound** (hypothesis; numerically certified, Lean proof pending). Along any in-D
orbit, every length-5 window of consecutive products contains one `≥ 1/4`. -/
def Q5Window : Prop :=
  ∀ (c : ℕ → ℝ), (∀ n, 0 < c n) → (∀ n, c n + phi * c (n + 1) > 1) →
    (∀ n, c n + c (n + 2) = (⌊(1 + c n) / (phi * c (n + 1))⌋ : ℝ) * phi * c (n + 1)) →
    ∀ n, ∃ i, i ≤ 4 ∧ 1 / 4 ≤ c (n + i) * c (n + i + 1)

/-- **Sharp scalar bound (conditional).** No in-D orbit keeps every product `≤ 1/4`. -/
theorem g5_no_sustained_sharp (hWin : Q5Window) (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
    (hreg : ∀ n, c n + phi * c (n + 1) > 1)
    (hrec : ∀ n, c n + c (n + 2) = (⌊(1 + c n) / (phi * c (n + 1))⌋ : ℝ) * phi * c (n + 1)) :
    ¬ (∀ n, c n * c (n + 1) ≤ 1 / 4) := by
  intro hle
  obtain ⟨i, _, hge⟩ := hWin c hpos hreg hrec 1
  have hP : c (1 + i) * c (1 + i + 1) = 1 / 4 := le_antisymm (hle (1 + i)) hge
  exact g5_tpoint_excl c hpos hreg hrec hle (by omega) hP

/-! ### Measure form (mirrors `G5lb.lean`, threshold 1/4). -/

open MeasureTheory Filter

def bczProduct (p : ℝ × ℝ) : ℝ := p.1 * p.2
@[simp] lemma bczProduct_apply (p : ℝ × ℝ) : bczProduct p = p.1 * p.2 := rfl

noncomputable def g5Map (p : ℝ × ℝ) : ℝ × ℝ :=
  (p.2, (⌊(1 + p.1) / (phi * p.2)⌋ : ℝ) * (phi * p.2) - p.1)
@[simp] lemma g5Map_fst (p : ℝ × ℝ) : (g5Map p).1 = p.2 := rfl
lemma g5Map_snd (p : ℝ × ℝ) :
    (g5Map p).2 = (⌊(1 + p.1) / (phi * p.2)⌋ : ℝ) * (phi * p.2) - p.1 := rfl

def g5Triangle : Set (ℝ × ℝ) := {p | 0 < p.1 ∧ 0 < p.2 ∧ p.1 + phi * p.2 > 1}

/-- Abstract: no in-D orbit sustains `P ≤ t` ⟹ `essSup ≥ t`. (Verbatim engine from `G5lb.lean`.) -/
theorem essSup_ge_of_no_sustained
    {X : Type*} [MeasurableSpace X]
    (T : X → X) (P : X → ℝ) (D : Set X) (t M : ℝ)
    (μ : Measure X) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0) (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hNS : ∀ (orbit : ℕ → X), (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ¬ (∀ n, P (orbit n) ≤ t)) :
    t ≤ essSup P μ := by
  have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) P := ⟨M, hPbdd⟩
  by_contra hlt
  push_neg at hlt
  have hae_le : ∀ᵐ x ∂μ, P x ≤ t := by
    have h : ∀ᵐ x ∂μ, P x < t := ae_lt_of_essSup_lt hlt hbdd
    filter_upwards [h] with x hx; exact hx.le
  have key : ∀ n, ∀ᵐ x ∂μ, (T^[n] x ∈ D ∧ P (T^[n] x) ≤ t) := by
    intro n
    have hDn : ∀ᵐ x ∂μ, T^[n] x ∈ D := by rw [ae_iff]; exact (hinv.iterate n).preimage_null hμD
    have hPn : ∀ᵐ x ∂μ, P (T^[n] x) ≤ t := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_le)
    filter_upwards [hDn, hPn] with x h1 h2; exact ⟨h1, h2⟩
  have hall : ∀ᵐ x ∂μ, ∀ n, (T^[n] x ∈ D ∧ P (T^[n] x) ≤ t) := ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  exact hNS (fun n => T^[n] x) (fun n => (hx n).1)
    (fun n => Function.iterate_succ_apply' (f := T) n x) (fun n => (hx n).2)

/-- Bridge: the sharp scalar bound transports to `g5Map`-orbits in `g5Triangle`. -/
theorem g5_no_sustained_orbit_sharp (hWin : Q5Window) (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ g5Triangle) (hstep : ∀ n, orbit (n + 1) = g5Map (orbit n)) :
    ¬ (∀ n, bczProduct (orbit n) ≤ 1 / 4) := by
  intro hle
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, g5Map_fst]
  have hpos : ∀ n, 0 < (orbit n).1 := fun n => (hmem n).1
  have hreg : ∀ n, (orbit n).1 + phi * (orbit (n + 1)).1 > 1 := by
    intro n; have hm := hmem n; rw [← hlink n]; exact hm.2.2
  have hrec : ∀ n, (orbit n).1 + (orbit (n + 2)).1
      = (⌊(1 + (orbit n).1) / (phi * (orbit (n + 1)).1)⌋ : ℝ) * phi * (orbit (n + 1)).1 := by
    intro n
    have h22 : (orbit (n + 2)).1 = (orbit (n + 1)).2 := (hlink (n + 1)).symm
    have hval : (orbit (n + 1)).2
        = (⌊(1 + (orbit n).1) / (phi * (orbit n).2)⌋ : ℝ) * (phi * (orbit n).2) - (orbit n).1 := by
      rw [hstep n, g5Map_snd]
    rw [h22, hval, hlink n]; ring
  have hsc : ∀ n, (orbit n).1 * (orbit (n + 1)).1 ≤ 1 / 4 := by
    intro n; have hh := hle n; rw [bczProduct_apply, hlink n] at hh; exact hh
  exact g5_no_sustained_sharp hWin (fun n => (orbit n).1) hpos hreg hrec hsc

/-- **q=5 SHARP measure lower bound (conditional on `Q5Window`):** `ess-sup P ≥ 1/4`. -/
theorem essSup_g5Product_ge_sharp (hWin : Q5Window)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ g5Triangleᶜ = 0) (hinv : MeasurePreserving g5Map μ μ)
    (hPbdd : ∀ᵐ x ∂μ, bczProduct x ≤ 1) :
    (1 : ℝ) / 4 ≤ essSup bczProduct μ :=
  essSup_ge_of_no_sustained g5Map bczProduct g5Triangle (1 / 4) 1 μ hμT hinv hPbdd
    (g5_no_sustained_orbit_sharp hWin)

/-- **q=5 NO GROUND STATE (conditional on `Q5Window`):** no `g5Map`-invariant probability measure
on `g5Triangle` attains `ess-sup P = 1/4`. With the upper bound (the optimizer family → 1/4⁺), the
ergodic-optimization infimum `X(5)=1/4` is approached but never realized. -/
theorem g5_no_ground_state (hWin : Q5Window)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ g5Triangleᶜ = 0) (hinv : MeasurePreserving g5Map μ μ)
    (hPbdd : ∀ᵐ x ∂μ, bczProduct x ≤ 1) :
    essSup bczProduct μ ≠ 1 / 4 := by
  intro hES
  have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) bczProduct := ⟨1, hPbdd⟩
  have hae_le : ∀ᵐ x ∂μ, bczProduct x ≤ 1 / 4 := by
    have h := ae_le_essSup (μ := μ) (f := bczProduct) hbdd; rw [hES] at h; exact h
  have key : ∀ n, ∀ᵐ x ∂μ, (g5Map^[n] x ∈ g5Triangle ∧ bczProduct (g5Map^[n] x) ≤ 1 / 4) := by
    intro n
    have hDn : ∀ᵐ x ∂μ, g5Map^[n] x ∈ g5Triangle := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null hμT
    have hPn : ∀ᵐ x ∂μ, bczProduct (g5Map^[n] x) ≤ 1 / 4 := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_le)
    filter_upwards [hDn, hPn] with x h1 h2; exact ⟨h1, h2⟩
  have hall : ∀ᵐ x ∂μ, ∀ n, (g5Map^[n] x ∈ g5Triangle ∧ bczProduct (g5Map^[n] x) ≤ 1 / 4) :=
    ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  exact g5_no_sustained_orbit_sharp hWin (fun n => g5Map^[n] x) (fun n => (hx n).1)
    (fun n => Function.iterate_succ_apply' (f := g5Map) n x) (fun n => (hx n).2)

#print axioms g5_no_sustained_sharp
#print axioms essSup_g5Product_ge_sharp
#print axioms g5_no_ground_state
