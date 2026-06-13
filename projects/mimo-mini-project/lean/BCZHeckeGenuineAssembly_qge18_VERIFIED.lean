import Mathlib
/-!
# Genuine assembly `(C′) ⟹ X_Ω(q) ≥ 1/λ³` for `q ≥ 18` — wiring the proven pieces.

**λ = l = 2cos(π/q) ∈ (1,2)** (here `q ≥ 18`, so `9/5 < l < 2`).  The genuine Hecke‑BCZ ergodic
optimization value is `X_Ω(q) = inf_μ ess‑sup_μ P = 1/l³`.  This file assembles the GENUINE LOWER
bound `X_Ω(q) ≥ 1/l³` by feeding the genuine condition

> **(C′)**  no `BCZ_q`‑orbit on the Taha triangle `𝒯^q` keeps every gap‑product `P < 1/l³`

to the proven abstract engine `essSup_ge_of_no_sustained`, and DERIVING (C′) from the proven
mechanism pieces:

* **(L1)** `infinitely_many_high_floor` — every scalar BCZ orbit has floor `K_n ≥ 2` infinitely
  often (a pure rotation never persists; proved via the conserved form, all `0<l<2`);
* **the kick bound** — at a high‑floor step the genuine observable is `≥ 1/l³` (this is exactly the
  (L2) switch‑is‑parabolic + `cusp_envelope` content), here DERIVED from the proven all‑q
  `cusp_envelope` under the explicit cusp‑branch guards.

## Strict honesty about scope (READ THIS).
The fully unconditional genuine lower bound for `q ≥ 18` does **not** follow from the scalar pieces
alone: the scalar‑branch reduction (`P < 1/l³ ⟹ on the scalar branch q−1`) is FALSE for `q ≥ 16`
(middle branches carry sub‑threshold points — `FINDINGS_goalF/M`).  So this file proves a **clean
CONDITIONAL theorem**: it hypothesizes exactly the genuine‑map orbit facts that the (not‑yet‑Lean)
piecewise `q−2`‑branch map would supply — the domain edges, the scalar floor recurrence along the
orbit, and that a floor‑change/high‑floor step lands on the cusp(parabolic) branch — and derives
(C′) and hence the bound from the proven pieces.  Section 6 states PRECISELY what genuine‑map
infrastructure would discharge each hypothesis to make it unconditional.

Everything proven here is parametric in `l` with `9/5 < l < 2` (covers every `q ≥ 18`).

`#print axioms` on every theorem below must show only `[propext, Classical.choice, Quot.sound]`.
All inlined lemmas are verbatim from the cross‑checked VERIFIED files
(`BCZHeckeG5_lowerbound_VERIFIED`, `BCZHeckeNoInfiniteRotation_allq_VERIFIED`,
`BCZHeckeCusp_envelope_allq_VERIFIED`).
-/
open Int Real Set MeasureTheory Filter
open scoped Classical ENNReal Topology
noncomputable section

/-! ## §1. The abstract `(C′)` engine.

`essSup_ge_of_no_sustained` is verbatim from `BCZHeckeG5_lowerbound_VERIFIED.lean`: given a map
`T`, observable `P`, set `D`, reals `t,M`, an invariant prob. measure `μ` with `μ(Dᶜ)=0`,
`P` a.e. `≤ M`, and `hNS` = "no forward `T`‑orbit in `D` keeps every `P ≤ t`", it concludes
`t ≤ ess‑sup P μ`.

`essSup_ge_of_no_sustained_strict` is the STRICT variant — `hNS` need only refute every orbit
keeping `P < t` (the genuinely natural form of (C′): "no orbit keeps every gap‑product strictly
below `1/l³`").  Identical proof; `ae_lt_of_essSup_lt` already gives the strict a.e. bound, so this
form is *more general* (weaker hypothesis) and matches exactly what the mechanism pieces deliver.
Supplying `hNS = (C′)` and `t = 1/l³` gives `X_Ω(q) ≥ 1/l³`. -/
theorem essSup_ge_of_no_sustained
    {X : Type*} [MeasurableSpace X]
    (T : X → X) (P : X → ℝ) (D : Set X) (t M : ℝ)
    (μ : Measure X) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hNS : ∀ (orbit : ℕ → X),
      (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
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
    have hDn : ∀ᵐ x ∂μ, T^[n] x ∈ D := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null hμD
    have hPn : ∀ᵐ x ∂μ, P (T^[n] x) ≤ t := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_le)
    filter_upwards [hDn, hPn] with x h1 h2; exact ⟨h1, h2⟩
  have hall : ∀ᵐ x ∂μ, ∀ n, (T^[n] x ∈ D ∧ P (T^[n] x) ≤ t) := ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  set orbit : ℕ → X := fun n => T^[n] x with horbit
  have hmem : ∀ n, orbit n ∈ D := fun n => (hx n).1
  have hstep : ∀ n, orbit (n + 1) = T (orbit n) :=
    fun n => Function.iterate_succ_apply' (f := T) n x
  exact hNS orbit hmem hstep (fun n => (hx n).2)

/-- **Strict `(C′)` engine.**  Same as `essSup_ge_of_no_sustained` but the no‑sustained hypothesis
need only refute orbits keeping `P < t` (strict).  This is the exact match for the strict
sub‑threshold condition the mechanism proves. -/
theorem essSup_ge_of_no_sustained_strict
    {X : Type*} [MeasurableSpace X]
    (T : X → X) (P : X → ℝ) (D : Set X) (t M : ℝ)
    (μ : Measure X) [IsProbabilityMeasure μ]
    (hμD : μ Dᶜ = 0)
    (hinv : MeasurePreserving T μ μ)
    (hPbdd : ∀ᵐ x ∂μ, P x ≤ M)
    (hNS : ∀ (orbit : ℕ → X),
      (∀ n, orbit n ∈ D) → (∀ n, orbit (n + 1) = T (orbit n)) →
      ¬ (∀ n, P (orbit n) < t)) :
    t ≤ essSup P μ := by
  have hbdd : IsBoundedUnder (· ≤ ·) (ae μ) P := ⟨M, hPbdd⟩
  by_contra hlt
  push_neg at hlt
  have hae_lt : ∀ᵐ x ∂μ, P x < t := ae_lt_of_essSup_lt hlt hbdd
  have key : ∀ n, ∀ᵐ x ∂μ, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := by
    intro n
    have hDn : ∀ᵐ x ∂μ, T^[n] x ∈ D := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null hμD
    have hPn : ∀ᵐ x ∂μ, P (T^[n] x) < t := by
      rw [ae_iff]; exact (hinv.iterate n).preimage_null (ae_iff.mp hae_lt)
    filter_upwards [hDn, hPn] with x h1 h2; exact ⟨h1, h2⟩
  have hall : ∀ᵐ x ∂μ, ∀ n, (T^[n] x ∈ D ∧ P (T^[n] x) < t) := ae_all_iff.mpr key
  obtain ⟨x, hx⟩ := hall.exists
  set orbit : ℕ → X := fun n => T^[n] x with horbit
  have hmem : ∀ n, orbit n ∈ D := fun n => (hx n).1
  have hstep : ∀ n, orbit (n + 1) = T (orbit n) :=
    fun n => Function.iterate_succ_apply' (f := T) n x
  exact hNS orbit hmem hstep (fun n => (hx n).2)

/-! ## §2. (L1): no infinite rotation ⟹ floor `≥ 2` infinitely often.

Verbatim from `BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`.  Namespaced to avoid clashes. -/
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
theorem E_conserved (n : ℕ) : Eform l c (n + 1) = Eform l c n := by
  have h := hrec n
  simp only [Eform]
  rw [show n + 1 + 1 = n + 2 from rfl, h]; ring

include hrec in
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
theorem E_pos (n : ℕ) : 0 < Eform l c n := by
  have hc := hpos n
  have h2l : 0 < 2 - l := by linarith
  have hcsq : 0 < c n ^ 2 := by positivity
  simp only [Eform]
  nlinarith [mul_pos h2l hcsq, mul_nonneg h2l.le (sq_nonneg (c (n + 1))),
    mul_nonneg hl0.le (sq_nonneg (c n - c (n + 1)))]

include hl0 hl2 hpos hrec in
theorem c_le_M (n : ℕ) : c n ≤ Real.sqrt (2 * Eform l c 0 / (2 - l)) := by
  have h2l : 0 < 2 - l := by linarith
  have hEn : Eform l c n = Eform l c 0 := E_const hrec n
  have hbound : c n ^ 2 ≤ 2 * Eform l c 0 / (2 - l) := by
    rw [le_div_iff₀ h2l, ← hEn]
    simp only [Eform]; nlinarith [sq_nonneg (c n - c (n + 1))]
  calc c n = Real.sqrt (c n ^ 2) := (Real.sqrt_sq (hpos n).le).symm
    _ ≤ Real.sqrt (2 * Eform l c 0 / (2 - l)) := Real.sqrt_le_sqrt hbound

include hl0 hl2 hpos hrec in
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

def dseq (c : ℕ → ℝ) (n : ℕ) : ℝ := c (n + 1) - c n

include hrec in
theorem d_two_step (n : ℕ) :
    dseq c (n + 2) - dseq c n = (l - 2) * (c (n + 1) + c (n + 2)) := by
  have h0 := hrec n
  have h1 := hrec (n + 1)
  simp only [dseq]
  rw [show n + 2 + 1 = n + 3 from rfl, show n + 1 + 1 = n + 2 from rfl] at *
  rw [h1, h0]; ring
end Main

section Final
variable {l : ℝ} (hl0 : 0 < l) (hl2 : l < 2)
variable {c : ℕ → ℝ} (hpos : ∀ n, 0 < c n)
variable (hrec : ∀ n, c (n + 2) = l * c (n + 1) - c n)

include hl0 hl2 hpos hrec in
theorem d_step_drop (n : ℕ) :
    dseq c (n + 2) ≤ dseq c n - (2 - l) * Real.sqrt (2 * Eform l c 0 / (2 + l)) := by
  have hts := d_two_step hrec n
  have hpair := pair_ge_m hl0 hl2 hpos hrec n
  have hlneg : l - 2 < 0 := by linarith
  have : (l - 2) * (c (n + 1) + c (n + 2))
      ≤ (l - 2) * Real.sqrt (2 * Eform l c 0 / (2 + l)) :=
    mul_le_mul_of_nonpos_left hpair hlneg.le
  linarith [hts, this]

include hl0 hl2 hpos hrec in
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
theorem d_gt_negM (n : ℕ) : - Real.sqrt (2 * Eform l c 0 / (2 - l)) < dseq c n := by
  have hM := c_le_M hl0 hl2 hpos hrec n
  have := hpos (n + 1)
  simp only [dseq]; linarith

include hl0 hl2 hpos hrec in
/-- **NO INFINITE ROTATION RUN.**  For `0<l<2` no positive sequence obeys the floor‑1 rotation
    recurrence `c(n+2)=l c(n+1)−c n` for every `n`. -/
theorem no_infinite_rotation : False := by
  set m := Real.sqrt (2 * Eform l c 0 / (2 + l)) with hm
  set M := Real.sqrt (2 * Eform l c 0 / (2 - l)) with hMdef
  have hE0 : 0 < Eform l c 0 := E_pos hl0 hl2 hpos 0
  have h2pl : 0 < 2 + l := by linarith
  have hmpos : 0 < m := by
    rw [hm]; exact Real.sqrt_pos.mpr (by positivity)
  set δ : ℝ := (2 - l) * m with hδ
  have hδpos : 0 < δ := by rw [hδ]; exact mul_pos (by linarith) hmpos
  obtain ⟨n, hn⟩ := exists_nat_gt ((dseq c 0 + M) / δ)
  have hlow := d_gt_negM hl0 hl2 hpos hrec (2 * n)
  have hhigh := d_even_le hl0 hl2 hpos hrec n
  have hcomb : (n : ℝ) * δ < dseq c 0 + M := by
    have : - M < dseq c 0 - (n : ℝ) * δ := lt_of_lt_of_le hlow hhigh
    linarith
  have : (n : ℝ) < (dseq c 0 + M) / δ := by
    rw [lt_div_iff₀ hδpos]; linarith [hcomb]
  linarith [hn, this]

end Final

/-- **(L1) — every scalar BCZ orbit has floor `≥ 2` infinitely often.**  Verbatim from
    `BCZHeckeNoInfiniteRotation_allq_VERIFIED.lean`.  For `0<l<2`, a positive sequence with the
    genuine scalar floor recurrence has NO tail on which every floor is `1`. -/
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

end HeckeNoRot

/-! ## §3. The cusp‑branch envelope (all q).

Verbatim from `BCZHeckeCusp_envelope_allq_VERIFIED.lean`.  On the genuine cusp(parabolic) branch
`i = q−2` the observable `P = a(a + l b)/l ≥ 1/l³` for every `l ≥ φ`.  This is the bound that the
"kick" enjoys (the floor‑change step is parabolic, lands on this branch). -/
theorem cusp_envelope (l a b : ℝ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hG : l * a + (l ^ 2 - 1) * b > 1)
    (hd : l * a + b > 1)
    (hU : a + l * b ≤ 1) :
    1 / l ^ 3 ≤ a * (a + l * b) / l := by
  have hl : 0 < l := by linarith
  have hl2 : l ^ 2 - 2 > 0 := by nlinarith [hlphi, hl1]
  have hc1 : l ^ 3 - l - 1 ≥ 0 := by nlinarith [hlphi, hl1]
  have hc2 : l ^ 2 - l - 1 ≥ 0 := by linarith [hlphi]
  have hkey : 1 ≤ l ^ 2 * (a * (a + l * b)) := by
    rcases le_or_gt a (1 / l) with hca | hca
    · have hfa : l * a ≤ 1 := by rw [mul_comm]; exact (le_div_iff₀ hl).mp hca
      have hage : a * (l + 1) ≥ 1 := by nlinarith [hU, hd, hl]
      have hlo : 1 ≤ l ^ 2 * a := by nlinarith [hage, hlphi, ha, hl]
      nlinarith [hl2, hl,
        mul_nonneg hc1 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + b - 1 by linarith)),
        mul_nonneg hl2.le (mul_nonneg (show (0:ℝ) ≤ l ^ 2 * a - 1 by linarith)
                                      (show (0:ℝ) ≤ 1 - l * a by linarith)),
        mul_nonneg hc2 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + (l ^ 2 - 1) * b - 1 by linarith))]
    · have hfa : 1 ≤ l * a := by
        have h := (div_lt_iff₀ hl).mp hca; rw [mul_comm] at h; linarith
      nlinarith [hl2, hl,
        mul_nonneg hc1 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + (l ^ 2 - 1) * b - 1 by linarith)),
        mul_nonneg hl2.le (mul_nonneg (show (0:ℝ) ≤ l * a - 1 by linarith)
                                      (show (0:ℝ) ≤ 1 - a by linarith)),
        mul_nonneg hc2 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + b - 1 by linarith))]
  have e : a * (a + l * b) / l - 1 / l ^ 3
      = (l ^ 2 * (a * (a + l * b)) - 1) / l ^ 3 := by
    rw [div_sub_div _ _ (by positivity : (l:ℝ) ≠ 0) (by positivity : (l:ℝ) ^ 3 ≠ 0)]
    rw [div_eq_div_iff (by positivity) (by positivity)]; ring
  have hnn : 0 ≤ a * (a + l * b) / l - 1 / l ^ 3 := by
    rw [e]; exact div_nonneg (by linarith [hkey]) (by positivity)
  linarith

/-! ## §4. The genuine observable, the Taha triangle, and the scalar branch map.

We work with the genuine observable `Pgen (a,b) = a (a + l b)/l` (matching `cusp_envelope` and the
q=5 `P3`), and the scalar/Taha domain.  On the scalar branch `i = q−1` the genuine map is the
project's scalar map `Tmap (a,b) = (b, ⌊(1+a)/(l b)⌋·l·b − a)` (verbatim the q=5 `i=4` branch). -/

variable (l : ℝ)

/-- Genuine observable `P = a (a + l b)/l`. -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-- The scalar‑branch BCZ map (`i = q−1`): `(a,b) ↦ (b, ⌊(1+a)/(l b)⌋·l·b − a)`. -/
noncomputable def Tmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  let k : ℤ := ⌊(1 + p.1) / (l * p.2)⌋
  (p.2, (k : ℝ) * (l * p.2) - p.1)

@[simp] lemma Tmap_fst (l : ℝ) (p : ℝ × ℝ) : (Tmap l p).1 = p.2 := rfl
lemma Tmap_snd (l : ℝ) (p : ℝ × ℝ) :
    (Tmap l p).2 = (⌊(1 + p.1) / (l * p.2)⌋ : ℝ) * (l * p.2) - p.1 := rfl

/-- The Taha triangle `𝒯^q = {0 < a ≤ 1, 1 − l a < b ≤ 1}` (the genuine domain). -/
def Taha (l : ℝ) : Set (ℝ × ℝ) := {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 1 - l * p.1 < p.2 ∧ p.2 ≤ 1}

/-! ## §5. THE ASSEMBLY.

### §5a. The kick bound DERIVED from `cusp_envelope`.

At a high‑floor step the orbit point lands on the cusp(parabolic) branch (the (L2) content: the
switch element is parabolic, `BCZHeckeL2_*`).  *Given* the cusp‑branch guards there,
`cusp_envelope` delivers `P ≥ 1/l³` — so the kick bound is a genuine CONSEQUENCE of a proven
all‑q lemma, not an assertion. -/
theorem kick_bound_of_cusp
    {l a b : ℝ} (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hcuspGuards : 0 < a ∧ a ≤ 1 ∧ l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1) :
    1 / l ^ 3 ≤ Pgen l (a, b) := by
  obtain ⟨ha, ha1, hG, hd, hU⟩ := hcuspGuards
  simpa [Pgen] using cusp_envelope l a b hl1 hlphi ha ha1 hG hd hU

/-! ### §5b. The scalar `(C′)` core: (L1) + kick bound ⟹ no sustained sub‑threshold orbit.

This is the heart of the architecture.  Hypotheses (all genuine‑map facts):
* `hpos` — the orbit's first coordinate stays positive (Taha domain);
* `hrec` — the scalar floor recurrence holds along the orbit;
* `hkick` — at any high‑floor step the genuine observable `c_n(c_n + l c_{n+1})/l ≥ 1/l³`
  (the (L2)+cusp content; via `kick_bound_of_cusp` it follows from the cusp‑branch guards).

Conclusion: the orbit cannot keep the genuine observable `< 1/l³` forever.  Mechanism:
sub‑threshold + the recurrence ⇒ (else the kick bound fires) every floor is exactly `1`
⇒ contradicts `infinitely_many_high_floor`. -/
theorem genuine_no_sustained_scalar
    {l : ℝ} (hl0 : 0 < l) (hl2 : l < 2)
    (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
    (hrec : ∀ n, c n + c (n + 2)
      = (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l * c (n + 1))
    (hkick : ∀ n, 2 ≤ ⌊(1 + c n) / (l * c (n + 1))⌋ →
        1 / l ^ 3 ≤ c n * (c n + l * c (n + 1)) / l) :
    ¬ (∀ n, c n * (c n + l * c (n + 1)) / l < 1 / l ^ 3) := by
  intro hsub
  have hnotf1 := HeckeNoRot.infinitely_many_high_floor l hl0 hl2 c hpos hrec
  have hfloor1 : ∀ n, ⌊(1 + c n) / (l * c (n + 1))⌋ = 1 := by
    intro n
    have hge1 : (1 : ℤ) ≤ ⌊(1 + c n) / (l * c (n + 1))⌋ := by
      by_contra hcon
      push_neg at hcon
      have hle : ⌊(1 + c n) / (l * c (n + 1))⌋ ≤ 0 := by omega
      have hkle : (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) ≤ 0 := by exact_mod_cast hle
      have hk := hrec n
      have hks : (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l ≤ 0 :=
        mul_nonpos_iff.mpr (Or.inr ⟨hkle, hl0.le⟩)
      have hksc : (⌊(1 + c n) / (l * c (n + 1))⌋ : ℝ) * l * c (n + 1) ≤ 0 :=
        mul_nonpos_iff.mpr (Or.inr ⟨hks, (hpos (n + 1)).le⟩)
      linarith [hk, hpos n, hpos (n + 2)]
    have hle1 : ⌊(1 + c n) / (l * c (n + 1))⌋ ≤ 1 := by
      by_contra hcon
      push_neg at hcon
      have h2 : (2 : ℤ) ≤ ⌊(1 + c n) / (l * c (n + 1))⌋ := by omega
      exact absurd (hkick n h2) (not_le.mpr (hsub n))
    omega
  exact hnotf1 ⟨0, fun n _ => hfloor1 n⟩

/-! ### §5c. Bridge: scalar `(C′)` core ⟹ `(C′)` for `Tmap`‑orbits on the Taha triangle.

Transports `genuine_no_sustained_scalar` to forward `Tmap`‑orbits, exactly as the verified
`g5_no_sustained_orbit`.  The observable is the genuine `Pgen`; the orbit's coordinates satisfy
`(orbit n).2 = (orbit (n+1)).1` (shift, true on the scalar branch — `Tmap_fst`). -/
theorem genuine_no_sustained_orbit
    {l : ℝ} (hl0 : 0 < l) (hl2 : l < 2)
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Taha l)
    (hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n))
    -- KICK BOUND along the orbit (the genuine‑map (L2)+cusp content):
    (hkick : ∀ n, 2 ≤ ⌊(1 + (orbit n).1) / (l * (orbit (n+1)).1)⌋ →
        1 / l ^ 3 ≤ Pgen l (orbit n)) :
    ¬ (∀ n, Pgen l (orbit n) < 1 / l ^ 3) := by
  intro hsub
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, Tmap_fst]
  have hpos : ∀ n, 0 < (orbit n).1 := by
    intro n; have hm := hmem n; simp only [Taha, Set.mem_setOf_eq] at hm; exact hm.1
  -- scalar floor recurrence from the map step
  have hrec : ∀ n, (orbit n).1 + (orbit (n + 2)).1
      = (⌊(1 + (orbit n).1) / (l * (orbit (n + 1)).1)⌋ : ℝ)
          * l * (orbit (n + 1)).1 := by
    intro n
    have h22 : (orbit (n + 2)).1 = (orbit (n + 1)).2 := (hlink (n + 1)).symm
    have hval : (orbit (n + 1)).2
        = (⌊(1 + (orbit n).1) / (l * (orbit n).2)⌋ : ℝ)
            * (l * (orbit n).2) - (orbit n).1 := by rw [hstep n, Tmap_snd]
    rw [h22, hval, hlink n]; ring
  -- the genuine observable, written via the scalar coordinate `c n := (orbit n).1`
  have hPval : ∀ n, Pgen l (orbit n)
      = (orbit n).1 * ((orbit n).1 + l * (orbit (n + 1)).1) / l := by
    intro n; rw [Pgen_apply, hlink n]
  -- the kick bound restated on `c`
  have hkick' : ∀ n, 2 ≤ ⌊(1 + (orbit n).1) / (l * (orbit (n + 1)).1)⌋ →
      1 / l ^ 3 ≤ (orbit n).1 * ((orbit n).1 + l * (orbit (n + 1)).1) / l := by
    intro n hn; rw [← hPval n]; exact hkick n hn
  -- sub‑threshold restated on `c`
  have hsub' : ∀ n, (orbit n).1 * ((orbit n).1 + l * (orbit (n + 1)).1) / l < 1 / l ^ 3 := by
    intro n; rw [← hPval n]; exact hsub n
  exact genuine_no_sustained_scalar hl0 hl2 (fun n => (orbit n).1) hpos hrec hkick' hsub'

/-! ### §5d. THE BOUND — feed `(C′)` to the engine.

Final assembly: any `Tmap`‑invariant probability measure on the Taha triangle, with `Pgen` a.e.
bounded and the kick bound holding along every orbit, has `ess‑sup Pgen ≥ 1/l³`.  I.e.
`X_Ω(q) ≥ 1/l³`.  This is the genuine lower bound, conditional on the kick bound. -/
theorem essSup_genuine_ge
    {l : ℝ} (hl0 : 0 < l) (hl2 : l < 2)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ (Taha l)ᶜ = 0)
    (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pgen l x ≤ M)
    (hkick : ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ Taha l) → (∀ n, orbit (n + 1) = Tmap l (orbit n)) →
      ∀ n, 2 ≤ ⌊(1 + (orbit n).1) / (l * (orbit (n+1)).1)⌋ →
        1 / l ^ 3 ≤ Pgen l (orbit n)) :
    1 / l ^ 3 ≤ essSup (Pgen l) μ :=
  essSup_ge_of_no_sustained_strict (Tmap l) (Pgen l) (Taha l) (1 / l ^ 3) M μ hμT hinv hPbdd
    (fun orbit hmem hstep =>
      genuine_no_sustained_orbit hl0 hl2 orbit hmem hstep (hkick orbit hmem hstep))

/-! ### §5e. The fully assembled conditional theorem, with the kick discharged by `cusp_envelope`.

Replacing the abstract kick bound by the proven `cusp_envelope`: if at every high‑floor step the
orbit point satisfies the genuine cusp‑branch guards (the remaining genuine‑map fact — see §6),
then the lower bound holds.  This is the cleanest CONDITIONAL theorem: every analytic inequality is
proven; the only hypotheses are the genuine‑map combinatorial facts (domain, scalar recurrence
along the orbit, and "a high‑floor step lands on the cusp branch"). -/
theorem essSup_genuine_ge_via_cusp
    {l : ℝ} (hl1 : 1 < l) (hl2 : l < 2) (hlphi : l ^ 2 ≥ l + 1)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ (Taha l)ᶜ = 0)
    (hinv : MeasurePreserving (Tmap l) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, Pgen l x ≤ M)
    -- the remaining genuine‑map fact: a high‑floor step lands on the cusp(parabolic) branch
    (hcuspAtKick : ∀ (orbit : ℕ → ℝ × ℝ),
      (∀ n, orbit n ∈ Taha l) → (∀ n, orbit (n + 1) = Tmap l (orbit n)) →
      ∀ n, 2 ≤ ⌊(1 + (orbit n).1) / (l * (orbit (n+1)).1)⌋ →
        (0 < (orbit n).1 ∧ (orbit n).1 ≤ 1 ∧
         l * (orbit n).1 + (l ^ 2 - 1) * (orbit n).2 > 1 ∧
         l * (orbit n).1 + (orbit n).2 > 1 ∧ (orbit n).1 + l * (orbit n).2 ≤ 1)) :
    1 / l ^ 3 ≤ essSup (Pgen l) μ := by
  have hl0 : 0 < l := by linarith
  refine essSup_genuine_ge hl0 hl2 μ hμT hinv M hPbdd ?_
  intro orbit hmem hstep n hn
  exact kick_bound_of_cusp hl1 hlphi (hcuspAtKick orbit hmem hstep n hn)

/-! ### §5f. Non‑vacuity: the cusp‑branch guards are satisfiable (the assembly is not empty).

The cusp vertices `(s,0)` with `s ∈ (1/l, 1]` lie in the Taha triangle AND satisfy every
cusp‑branch guard used by `kick_bound_of_cusp` — so the kick hypotheses are genuinely realizable
(they are the parabolic fixed points where the infimum `1/l³` is approached).  Hence the
conditional theorems are non‑vacuous: there exist points discharging the cusp guards, and the
bound there is exactly attained‑from‑above (`Pgen (s,0) = s²/l ≥ 1/l³`). -/
theorem cusp_guards_satisfiable {l : ℝ} (hl1 : 1 < l) {s : ℝ} (hs1 : 1 / l < s) (hs2 : s ≤ 1) :
    (s, (0:ℝ)) ∈ Taha l ∧
    (0 < (s,(0:ℝ)).1 ∧ (s,(0:ℝ)).1 ≤ 1 ∧
     l * (s,(0:ℝ)).1 + (l ^ 2 - 1) * (s,(0:ℝ)).2 > 1 ∧
     l * (s,(0:ℝ)).1 + (s,(0:ℝ)).2 > 1 ∧ (s,(0:ℝ)).1 + l * (s,(0:ℝ)).2 ≤ 1) := by
  have hl0 : 0 < l := by linarith
  have hps : 1 < l * s := by have h := (div_lt_iff₀ hl0).mp hs1; nlinarith [h]
  have hs0 : 0 < s := lt_trans (one_div_pos.mpr hl0) hs1
  refine ⟨?_, ?_⟩
  · simp only [Taha, Set.mem_setOf_eq]; exact ⟨hs0, hs2, by nlinarith [hps], by norm_num⟩
  · refine ⟨hs0, hs2, ?_, ?_, ?_⟩ <;> simp only [] <;> nlinarith [hps, hs2]

/-! ## §6. What remains to make this UNCONDITIONAL (precise genuine‑map infrastructure).

The engine is fed, and (C′) is derived from the proven mechanism pieces.  Every *analytic*
inequality in the chain is machine‑checked here (the engine, (L1) `infinitely_many_high_floor`, and
the cusp bound `cusp_envelope`).  The hypotheses of `essSup_genuine_ge` / `essSup_genuine_ge_via_cusp`
are exactly the genuine‑map combinatorial/geometric facts that are **not yet formalized in Lean**.
To discharge them and obtain an unconditional `X_Ω(q) ≥ 1/l³` for `q ≥ 18`, one needs:

1.  **The genuine piecewise map `BCZ_q` in Lean (the `q−2` branch matrices `M_{i,k}`).**  Currently
    only the q=5 instance exists (`BCZHeckeG5_genuine_VERIFIED.G5`, three branches).  Needed: the
    all‑q definition of the branch generators `M_{i,k}` (`i = 2..q−1`) on `𝒯^q` from the universal
    Chebyshev boundary data `x_{q-1}=0, x_{q-2}=1, x_{q-3}=l, x_{q-4}=l²−1`, and the piecewise map.
    This replaces our scalar `Tmap` (the `i=q−1` branch) by the genuine multi‑branch map, and is the
    object the invariant measure `μ` actually lives on.

2.  **`hstep` / `hrec` (scalar recurrence along the orbit).**  In §5 we hypothesize the orbit obeys
    the scalar floor recurrence.  Genuinely this is the **2‑branch reduction** (`FINDINGS_goalM` §4b,
    `projects/mimo-mini-project/code/Mgoal_subthr_branches.py`): every *sustained* sub‑threshold run uses only branches
    `{q−1, q−3}` (the F‑family), and on the dominant scalar branch the recurrence is exactly `hrec`.
    Formalizing this needs: the branch‑membership predicate and the proof that a sub‑threshold run
    stays on the `{q−1,q−3}` alphabet (the *confinement lemma*, numerically robust q≤30/40, OPEN in
    Lean).  [For q=16,17 the stronger "runs are scalar" is reduced to the proven `two_step_kick`.]

3.  **`hcuspAtKick` / `hkick` (a high‑floor step lands on the cusp/parabolic branch).**  This is the
    (L2) content: at a floor change the switch element is parabolic (`adjF_switch_parabolic`,
    `switch_forces_nonelliptic` — already Lean, all q), so the step sits on the cusp branch where
    `cusp_envelope` (Lean, all q) gives `P ≥ 1/l³`.  Making it unconditional needs the bridge
    "floor `K_n ≥ 2` ⟹ the orbit point `(a,b)` satisfies the cusp‑branch guards
    `l a+(l²−1)b>1, l a+b>1, a+l b≤1`" for the genuine map — i.e. identifying the high‑floor branch
    geometrically.  We *derive* the bound from the guards (`kick_bound_of_cusp`); the missing link is
    the guard‑membership itself, which is a property of the genuine branch decomposition (1).

4.  **`hinv` (existence/invariance of `μ`) and `hPbdd` (a.e. boundedness of `Pgen`).**  Standard once
    (1) is in place: `μ` is the BCZ/Haar natural‑extension measure on `𝒯^q`; `Pgen` is bounded on the
    triangle.

In short: items (2)–(3) are the genuine‑map combinatorics (branch confinement + high‑floor⟹cusp
guard); item (1) is the genuine‑map *definition*; item (4) is routine.  The ANALYTIC heart — engine,
no‑infinite‑rotation, cusp envelope, and the glue deriving (C′) — is fully proven above.
The single hardest genuinely‑open analytic residual (orthogonal to formalization) is the
(L1)‑quantitative `O(1/q²)` margin on the 2‑branch alphabet (`FINDINGS_goalN`); the qualitative
core of it (`no_infinite_rotation`) is what powers `genuine_no_sustained_scalar` here. -/

#print axioms essSup_ge_of_no_sustained
#print axioms essSup_ge_of_no_sustained_strict
#print axioms HeckeNoRot.no_infinite_rotation
#print axioms HeckeNoRot.infinitely_many_high_floor
#print axioms cusp_envelope
#print axioms kick_bound_of_cusp
#print axioms genuine_no_sustained_scalar
#print axioms genuine_no_sustained_orbit
#print axioms essSup_genuine_ge
#print axioms essSup_genuine_ge_via_cusp
#print axioms cusp_guards_satisfiable
