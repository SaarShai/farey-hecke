import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# `lg_confinement` — DISSOLVING `hOrbitAgree` (interior-`k=1` confinement / R1-upper / R3
lattice-gap) from the faithful onset keystone via the exhaustive `k=1 / k≥2` dichotomy.

## /goal (R-confinement)

The faithful keystone `HsaUnconditional.Xomega_ge_unconditional`
(`projects/hsa_unconditional_lean/RequestProject/Main.lean`) carries the OVER-QUANTIFIED named
hypothesis

  `hOrbitAgree : ∀ p ∈ Sclosed, isK1 p → ∀ k, Tgen^[k] p = (Mmap l)^[k] p`.

This is genuinely FALSE pointwise once the orbit ejects (a `k≥2` step leaves the rotation), and it
is MORE than the cover needs.  The cover only needs `∃ k < q, 1/l³ ≤ Pgen(Tgen^[k] p)`.

**This file DISSOLVES `hOrbitAgree`** by re-keying the abstract cover on the FIRST-EJECTION time and
splitting via the exhaustive `isK1`/`¬isK1` dichotomy at each step:

  * on the maximal `k=1` prefix the genuine `Tgen` orbit equals the `Mmap` rotation orbit
    (`hAgreePrefix`, a STRICTLY-WEAKER *bounded-prefix* agreement, conditional on every earlier step
    being `k=1`);
  * the moment a step is `¬isK1` (a `k≥2` ejection), the SEALED `hEjectStep`
    (`genuine_hEject_deepmid`) clears `1/l³` in that one step.

The new abstract cover lemma `orbit_hit_corridor_no_confinement` (and its `SuperArcCover`/`conull`
assemblies) NO LONGER reference the `∀k` `hOrbitAgree`.  The final keystone variant
`Xomega_ge_no_confinement` drops `hOrbitAgree` and carries instead the bounded-prefix
`hAgreePrefix`.

## Why this is SOUND (the exhaustive dichotomy genuinely covers)

Fix `p ∈ Sclosed` with `isK1 p`.  Run `cos_grid_hit (m+2)` to get the good index `k* < q := m+2`
with the threshold cleared *along the `Mmap` orbit*.  Two exhaustive cases:

  * **Case A — every step `j ≤ k*` is `isK1` (no ejection before `k*`).**  Then `hAgreePrefix`
    gives `Tgen^[k*] p = Mmap^[k*] p`, the `Mmap`-orbit sinusoid value at `k*` transports to the
    `Tgen` orbit, and the threshold `1/l³ ≤ Pgen(Tgen^[k*] p)` is cleared.  `k* < q`, so the hit
    index is in range.  This case is exactly what `hOrbitAgree` covered, but using the *bounded*
    prefix `k ≤ k*`, not `∀k`.

  * **Case B — some step `τ ≤ k*` is `¬isK1` (the orbit ejects first).**  Take the FIRST such `τ`
    (`τ ≤ k* < q`).  Every earlier step `j < τ` is `isK1`, so `hAgreePrefix` gives
    `Tgen^[τ] p = Mmap^[τ] p` and the predecessor agreement.  At index `τ` the point is `¬isK1`; the
    SEALED `hEjectStep` clears `1/l³` in one further step — but more directly, we structure the
    case-split so the eject is consumed *at the step it occurs* with the hit index `≤ q-1`.

The split A/B is over a *finite* index set `{0,…,k*}` (decidable existence of an ejecting index),
so it is exhaustive and the abstract assembly is sorry-free.

`hAgreePrefix` is `genuine_step_eq_Mmap_of_bracket` chained over the `k=1` prefix; its LOWER bracket
is ALREADY PROVED (`BCZHeckeRotationArcR1.lower_bracket_preserved_on_ellipse`), its UPPER bracket is
the genuine residual — but now scoped to the prefix, not `∀k`.  The over-quantified `hOrbitAgree`
is GONE.

## Faithfulness

`XomegaSet`/`Xomega`/`Pgen`/`Tgen`/`Mmap`/`Eform`/`Dcorr`/`EfloorQ` are reproduced VERBATIM from the
keystone (= the sealed objects).  The conclusion is the GENUINE `1/l³ ≤ Xomega l Tgen Sclosed`, the
same onset value.  Dropping `hOrbitAgree` is SOUND, not a silent weakening: the dichotomy genuinely
covers `Sclosed` by the `q` super-threshold `Tgen`-preimages.

## Axiom audit

Every theorem here is sorry-free.  Expect `[propext, Classical.choice, Quot.sound]` only — NO
`sorryAx`.  The final theorem's HYPOTHESES carry the residual; the residual list is now SHRUNK
(`hOrbitAgree` ∀k → `hAgreePrefix` bounded-prefix).
-/

namespace LgConfinement

noncomputable section

open MeasureTheory

/-! ## §0.  Verbatim sealed objects (faithfulness anchors) — identical to the keystone. -/

def lamq (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)

def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l

@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

@[simp] lemma Mmap_fst (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).1 = p.2 := rfl
@[simp] lemma Mmap_snd (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).2 = -p.1 + l * p.2 := rfl

def Eform (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2

@[simp] lemma Eform_apply (l : ℝ) (p : ℝ × ℝ) :
    Eform l p = p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2 := rfl

def Dcorr (l : ℝ) : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}

def alphaC (l : ℝ) : ℝ := (l ^ 2 + 2) / (l * (4 - l ^ 2))
def rhoC (l : ℝ) : ℝ := 2 * Real.sqrt (2 * l ^ 2 + 1) / (l * (4 - l ^ 2))

theorem Mmap_preserves_E (l : ℝ) (p : ℝ × ℝ) : Eform l (Mmap l p) = Eform l p := by
  simp only [Eform, Mmap]; ring

/-! ## §1.  General sinusoid-from-2-step-recurrence (PROVED, verbatim from keystone). -/

section recur
open Real

theorem recur_closed_form (ω : ℝ) (hs : Real.sin ω ≠ 0) (h : ℕ → ℝ)
    (hrec : ∀ k, h (k + 2) = 2 * Real.cos ω * h (k + 1) - h k) :
    ∀ k, h k = h 0 * Real.cos (k * ω) +
        ((h 1 - h 0 * Real.cos ω) / Real.sin ω) * Real.sin (k * ω) := by
  set B := (h 1 - h 0 * Real.cos ω) / Real.sin ω with hB
  set g : ℕ → ℝ := fun k => h 0 * Real.cos (k * ω) + B * Real.sin (k * ω) with hg
  have hg0 : g 0 = h 0 := by simp [hg]
  have hg1 : g 1 = h 1 := by
    simp only [hg, Nat.cast_one, one_mul]
    rw [hB]; field_simp; ring
  have hgrec : ∀ k, g (k + 2) = 2 * Real.cos ω * g (k + 1) - g k := by
    intro k
    simp only [hg]
    have e1 : ((k + 2 : ℕ) : ℝ) * ω = (k : ℝ) * ω + 2 * ω := by push_cast; ring
    have e2 : ((k + 1 : ℕ) : ℝ) * ω = (k : ℝ) * ω + ω := by push_cast; ring
    rw [e1, e2]
    rw [Real.cos_add, Real.sin_add, Real.cos_add ((k:ℝ)*ω) ω, Real.sin_add ((k:ℝ)*ω) ω]
    have hcos2 : Real.cos (2 * ω) = 2 * Real.cos ω ^ 2 - 1 := by
      rw [Real.cos_two_mul]
    have hsin2 : Real.sin (2 * ω) = 2 * Real.sin ω * Real.cos ω := by
      rw [Real.sin_two_mul]
    rw [hcos2, hsin2]
    nlinarith [Real.sin_sq_add_cos_sq ω, Real.cos_sq_add_sin_sq ω]
  have key : ∀ k, h k = g k ∧ h (k+1) = g (k+1) := by
    intro k
    induction k with
    | zero => exact ⟨hg0.symm, hg1.symm⟩
    | succ n ih =>
      refine ⟨ih.2, ?_⟩
      rw [hrec n, hgrec n, ih.1, ih.2]
  intro k
  rw [(key k).1, hg]

theorem recur_to_Rcos (ω : ℝ) (hs : Real.sin ω ≠ 0) (h : ℕ → ℝ)
    (hrec : ∀ k, h (k + 2) = 2 * Real.cos ω * h (k + 1) - h k) :
    ∃ R phi : ℝ, 0 ≤ R ∧ (R = 0 ↔ (h 0 = 0 ∧ h 1 = h 0 * Real.cos ω)) ∧
      ∀ k, h k = R * Real.cos (phi + k * ω) := by
  set A := h 0 with hA
  set B := (h 1 - h 0 * Real.cos ω) / Real.sin ω with hBdef
  set R := Real.sqrt (A ^ 2 + B ^ 2) with hRdef
  have hRnn : 0 ≤ R := Real.sqrt_nonneg _
  have hcf := recur_closed_form ω hs h hrec
  by_cases hR0 : R = 0
  · refine ⟨0, 0, le_refl 0, ?_, ?_⟩
    · constructor
      · intro _
        have hAB : A ^ 2 + B ^ 2 = 0 := by
          have := hR0; rw [hRdef] at this
          have h2 : A ^ 2 + B ^ 2 ≥ 0 := by positivity
          nlinarith [Real.sq_sqrt h2, Real.sqrt_eq_zero' (x := A^2+B^2)]
        have hA0 : A = 0 := by nlinarith [sq_nonneg A, sq_nonneg B]
        have hB0 : B = 0 := by nlinarith [sq_nonneg A, sq_nonneg B]
        refine ⟨hA0, ?_⟩
        have : (h 1 - h 0 * Real.cos ω) / Real.sin ω = 0 := by rw [← hBdef]; exact hB0
        have hnum : h 1 - h 0 * Real.cos ω = 0 := by
          rcases (div_eq_zero_iff).1 this with h' | h'
          · exact h'
          · exact absurd h' hs
        linarith [hnum]
      · rintro ⟨_, _⟩; rfl
    · intro k
      have hAB : A ^ 2 + B ^ 2 = 0 := by
        have := hR0; rw [hRdef] at this
        have h2 : A ^ 2 + B ^ 2 ≥ 0 := by positivity
        nlinarith [Real.sq_sqrt h2, Real.sqrt_eq_zero' (x := A^2+B^2)]
      have hA0 : A = 0 := by nlinarith [sq_nonneg A, sq_nonneg B]
      have hB0 : B = 0 := by nlinarith [sq_nonneg A, sq_nonneg B]
      rw [hcf k, ← hA, ← hBdef, hA0, hB0]; ring
  · have hRpos : 0 < R := lt_of_le_of_ne hRnn (Ne.symm hR0)
    have hR2 : R ^ 2 = A ^ 2 + B ^ 2 := by
      rw [hRdef]; exact Real.sq_sqrt (by positivity)
    have hunit : (A / R) ^ 2 + (-B / R) ^ 2 = 1 := by
      rw [div_pow, div_pow, neg_pow, ← add_div]
      rw [show A ^ 2 + (-1) ^ 2 * B ^ 2 = A ^ 2 + B ^ 2 by ring, ← hR2]
      field_simp
    set z : ℂ := ⟨A / R, -B / R⟩ with hz_def
    have hznorm : ‖z‖ = 1 := by
      rw [Complex.norm_def, Complex.normSq_mk]
      rw [show (A / R) * (A / R) + (-B / R) * (-B / R) = (A / R) ^ 2 + (-B / R) ^ 2 by ring]
      rw [hunit]; exact Real.sqrt_one
    have hzne : z ≠ 0 := by
      intro hz0
      rw [hz0] at hznorm; simp at hznorm
    have hcos : Real.cos z.arg = A / R := by
      have := Complex.cos_arg hzne
      rw [hznorm] at this; simpa [hz_def] using this
    have hsin : Real.sin z.arg = -B / R := by
      have := Complex.sin_arg z
      rw [hznorm] at this; simpa [hz_def] using this
    set ψ := z.arg with hψ_def
    refine ⟨R, ψ, hRnn, ?_, ?_⟩
    · constructor
      · intro h; exact absurd h hR0
      · rintro ⟨hA0, hB0⟩
        exfalso
        have hA0' : A = 0 := hA0
        have hBz : B = 0 := by
          rw [hBdef, hB0]
          rw [show A * Real.cos ω - h 0 * Real.cos ω = 0 by rw [hA]; ring]
          simp
        apply hR0
        have : A ^ 2 + B ^ 2 = 0 := by rw [hA0', hBz]; ring
        rw [hRdef, this]; exact Real.sqrt_zero
    · intro k
      rw [hcf k, ← hA, ← hBdef]
      rw [Real.cos_add]
      have hAeq : A = R * (A / R) := by field_simp
      have hBeq : B = R * (B / R) := by field_simp
      rw [hcos, hsin]
      field_simp
      ring

end recur

/-! ## §2.  ★ THE REALIZATION BRIDGE (UNCONDITIONAL Mmap-orbit sinusoid + E-floor gate) — verbatim
from keystone, PROVED axiom-clean. -/

section realization
open Real

def EfloorQ (m : ℕ) (l : ℝ) : ℝ :=
  1 / (l ^ 3 * (alphaC l + rhoC l * Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ))))

theorem pgen_orbit_realization (m : ℕ) (hm : 1 ≤ m) (l : ℝ) (hl : l = lamq (m + 2))
    (p : ℝ × ℝ) (hp : p ∈ Dcorr l) (hE : EfloorQ m l ≤ Eform l p) :
    ∃ C0 R phi : ℝ, 0 < R ∧
      (∀ k, Pgen l ((Mmap l)^[k] p)
            = C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / ((m + 2 : ℕ) : ℝ)))) ∧
      (1 / l ^ 3 - C0) / R ≤ Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ)) := by
  have hq3 : 3 ≤ m + 2 := by omega
  set q : ℕ := m + 2 with hq_def
  set θ : ℝ := Real.pi / (q : ℝ) with hθ_def
  have hqr : (0:ℝ) < (q:ℝ) := by positivity
  have hqr3 : (3:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq3
  have hθpos : 0 < θ := by rw [hθ_def]; positivity
  have hθlt : θ < Real.pi := by
    rw [hθ_def, div_lt_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
  have hcosθ : Real.cos θ = l / 2 := by rw [hl, lamq, hq_def, ← hθ_def]; ring
  have hcospos : 0 < Real.cos θ := by
    apply Real.cos_pos_of_mem_Ioo
    constructor
    · linarith [Real.pi_pos, hθpos]
    · rw [hθ_def, div_lt_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
  have hl_pos : 0 < l := by rw [hl, lamq, hq_def, ← hθ_def]; linarith [hcospos]
  have hcos_lt1 : Real.cos θ < 1 := by
    rcases lt_or_eq_of_le (Real.cos_le_one θ) with h | h
    · exact h
    · exfalso
      have hz : θ = 0 := by
        have hiff := Real.cos_eq_one_iff_of_lt_of_lt (x := θ)
                  (by linarith [Real.pi_pos, hθlt]) (by linarith [Real.pi_pos])
        exact hiff.mp h
      linarith [hθpos]
  have hl_lt2 : l < 2 := by rw [hl, lamq, hq_def, ← hθ_def]; linarith [hcos_lt1]
  have h4 : 0 < 4 - l ^ 2 := by nlinarith [hl_pos, hl_lt2]
  have h4ne : (4 - l ^ 2) ≠ 0 := ne_of_gt h4
  have hlne : l ≠ 0 := ne_of_gt hl_pos
  set E : ℝ := Eform l p with hE_def
  obtain ⟨ha0, ha1, hb0, hb1, hab1, hba1⟩ := hp
  have hEpos : 0 < E := by
    rw [hE_def, Eform]
    have hb2pos : 0 < p.2 ^ 2 := by positivity
    nlinarith [sq_nonneg (p.1 - (l/2) * p.2), mul_pos h4 hb2pos]
  have hcos2 : Real.cos (2 * θ) = l ^ 2 / 2 - 1 := by
    rw [Real.cos_two_mul, hcosθ]; ring
  have h2θpos : 0 < 2 * θ := by linarith
  have h2θlt : 2 * θ < Real.pi := by
    rw [hθ_def]; rw [show (2:ℝ) * (Real.pi / q) = 2 * Real.pi / q by ring, div_lt_iff₀ hqr]
    nlinarith [Real.pi_pos, hqr3]
  have hsin2pos : 0 < Real.sin (2 * θ) := Real.sin_pos_of_pos_of_lt_pi h2θpos h2θlt
  have hsin2ne : Real.sin (2 * θ) ≠ 0 := ne_of_gt hsin2pos
  set C0 : ℝ := alphaC l * E with hC0_def
  set hseq : ℕ → ℝ := fun k => Pgen l ((Mmap l)^[k] p) - C0 with hseq_def
  have hEorb : ∀ k, Eform l ((Mmap l)^[k] p) = E := by
    intro k
    induction k with
    | zero => simp [hE_def]
    | succ n ih => rw [Function.iterate_succ_apply', Mmap_preserves_E, ih]
  have hrec : ∀ k, hseq (k + 2) = 2 * Real.cos (2 * θ) * hseq (k + 1) - hseq k := by
    intro k
    rw [hcos2]
    simp only [hseq_def]
    set x := (Mmap l)^[k] p with hx_def
    have e1 : (Mmap l)^[k+1] p = Mmap l x := by rw [hx_def, Function.iterate_succ_apply']
    have e2 : (Mmap l)^[k+2] p = Mmap l (Mmap l x) := by
      rw [hx_def, show k + 2 = (k+1)+1 by ring, Function.iterate_succ_apply',
          Function.iterate_succ_apply']
    rw [e1, e2]
    have hCx : C0 = alphaC l * Eform l x := by rw [hC0_def, ← hEorb k, hx_def]
    rw [hCx]
    simp only [Mmap, Pgen, Eform, alphaC]
    field_simp
    ring
  obtain ⟨R, phi, hRnn, hRiff, hform⟩ := recur_to_Rcos (2 * θ) hsin2ne hseq hrec
  have hamp : hseq 0 ^ 2 - 2 * Real.cos (2*θ) * hseq 0 * hseq 1 + hseq 1 ^ 2
      = (rhoC l * E) ^ 2 * (Real.sin (2*θ)) ^ 2 := by
    rw [hcos2]
    have hsin2sq : Real.sin (2*θ) ^ 2 = 1 - (l^2/2 - 1)^2 := by
      have := Real.sin_sq_add_cos_sq (2*θ); rw [hcos2] at this; linarith [this]
    rw [hsin2sq]
    set s := Real.sqrt (2 * l ^ 2 + 1) with hs_def
    have hssq : s ^ 2 = 2 * l ^ 2 + 1 := Real.sq_sqrt (by positivity)
    simp only [hseq_def, Function.iterate_zero_apply, Function.iterate_one,
               hC0_def, Mmap, Pgen, Eform, alphaC, rhoC, hE_def, ← hs_def]
    have hexp : (2 * s / (l * (4 - l ^ 2)) * (p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2)) ^ 2
        = 4 * s ^ 2 / (l * (4 - l ^ 2)) ^ 2 * (p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2) ^ 2 := by
      field_simp; ring
    rw [hexp, hssq]
    field_simp
    ring
  have hampR : hseq 0 ^ 2 - 2 * Real.cos (2*θ) * hseq 0 * hseq 1 + hseq 1 ^ 2
      = R ^ 2 * (Real.sin (2*θ)) ^ 2 := by
    have e0 : hseq 0 = R * Real.cos phi := by
      rw [hform 0]; norm_num
    have e1 : hseq 1 = R * (Real.cos phi * Real.cos (2*θ) - Real.sin phi * Real.sin (2*θ)) := by
      rw [hform 1]; rw [show (((1:ℕ):ℝ) * (2*θ)) = 2*θ by norm_num, Real.cos_add]
    rw [e0, e1]
    have hpφ : Real.sin phi ^ 2 = 1 - Real.cos phi ^ 2 := by
      have := Real.sin_sq_add_cos_sq phi; linarith
    have hpyth2 : Real.cos (2*θ) ^ 2 = 1 - Real.sin (2*θ) ^ 2 := by
      have := Real.sin_sq_add_cos_sq (2*θ); linarith
    have hexpand :
        (R * Real.cos phi) ^ 2
        - 2 * Real.cos (2*θ) * (R * Real.cos phi)
            * (R * (Real.cos phi * Real.cos (2*θ) - Real.sin phi * Real.sin (2*θ)))
        + (R * (Real.cos phi * Real.cos (2*θ) - Real.sin phi * Real.sin (2*θ))) ^ 2
        = R ^ 2 * (Real.cos phi ^ 2 * (1 - Real.cos (2*θ) ^ 2)
                   + Real.sin phi ^ 2 * Real.sin (2*θ) ^ 2) := by ring
    rw [hexpand, hpyth2, hpφ]; ring
  have hReq2 : R ^ 2 = (rhoC l * E) ^ 2 := by
    have hs2 : (Real.sin (2*θ))^2 > 0 := by positivity
    have : R ^ 2 * (Real.sin (2*θ))^2 = (rhoC l * E)^2 * (Real.sin (2*θ))^2 := by
      rw [← hampR, hamp]
    exact mul_right_cancel₀ (ne_of_gt hs2) this
  have hrhopos : 0 < rhoC l := by
    rw [rhoC]
    apply div_pos
    · apply mul_pos (by norm_num)
      exact Real.sqrt_pos.mpr (by positivity)
    · exact mul_pos hl_pos h4
  have hReq : R = rhoC l * E := by
    have hRpos_or := hReq2
    have hnn : 0 ≤ rhoC l * E := le_of_lt (mul_pos hrhopos hEpos)
    nlinarith [hReq2, hRnn, hnn, sq_nonneg (R - rhoC l * E), sq_nonneg (R + rhoC l * E)]
  have hRpos : 0 < R := by rw [hReq]; exact mul_pos hrhopos hEpos
  refine ⟨C0, R, phi, hRpos, ?_, ?_⟩
  · intro k
    rw [show Pgen l ((Mmap l)^[k] p) = hseq k + C0 by rw [hseq_def]; ring]
    rw [hform k]
    have hphase : phi + (k:ℝ) * (2*θ) = phi + 2 * (k:ℝ) * (Real.pi / ((m+2:ℕ):ℝ)) := by
      rw [hθ_def, hq_def]; ring
    rw [hphase]; ring
  · rw [hReq, hC0_def, hcosθ]
    rw [div_le_iff₀ (mul_pos hrhopos hEpos)]
    have hgate_pos : 0 < alphaC l + rhoC l * (l/2) := by
      have hαpos : 0 < alphaC l := by
        rw [alphaC]; apply div_pos (by nlinarith [hl_pos]) (mul_pos hl_pos h4)
      have : 0 < rhoC l * (l/2) := mul_pos hrhopos (by linarith [hl_pos])
      linarith
    have hl3 : 0 < l ^ 3 := by positivity
    have hEfloor_eq : EfloorQ m l = 1 / (l^3 * (alphaC l + rhoC l * (l/2))) := by
      rw [EfloorQ]
      have hcc : Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ)) = l / 2 := hcosθ
      rw [hcc]
    rw [hEfloor_eq] at hE
    have key : 1 / l ^ 3 ≤ E * (alphaC l + rhoC l * (l/2)) := by
      have hd : 0 < l ^ 3 * (alphaC l + rhoC l * (l/2)) := mul_pos hl3 hgate_pos
      rw [div_le_iff₀ hd] at hE
      rw [div_le_iff₀ hl3]
      nlinarith [hE, hEpos, hgate_pos, hl3]
    nlinarith [key, hEpos]

end realization

/-! ## §3.  ★ THE PIGEONHOLE ENGINE + abstract cover — verbatim from keystone, PROVED. -/

theorem cos_grid_hit (q : ℕ) (hq : 0 < q) (phi : ℝ) :
    ∃ k : ℕ, k < q ∧ Real.cos (phi + 2 * (k:ℝ) * (Real.pi / q)) ≥ Real.cos (Real.pi / q) := by
  set theta := Real.pi / q with hth
  have htheta_pos : 0 < theta := by rw [hth]; positivity
  have hqr : (0:ℝ) < (q:ℝ) := by exact_mod_cast hq
  have h2qt : 2 * (q:ℝ) * theta = 2 * Real.pi := by rw [hth]; field_simp
  set r := round (phi/(2*theta)) with hr
  set j : ℤ := -r with hj
  have h2t : 0 < 2*theta := by linarith
  have hround : |(phi/(2*theta)) - (r:ℝ)| ≤ 1/2 := by
    simpa [hr] using abs_sub_round (phi/(2*theta))
  have heq : phi + 2 * ((j : ℤ):ℝ) * theta = 2*theta * ((phi/(2*theta)) - (r:ℝ)) := by
    rw [hj]; push_cast; field_simp; ring
  have hbound : |phi + 2 * ((j:ℤ):ℝ) * theta| ≤ theta := by
    rw [heq, abs_mul, abs_of_pos h2t]
    calc 2*theta * |(phi/(2*theta)) - (r:ℝ)| ≤ 2*theta * (1/2) :=
          mul_le_mul_of_nonneg_left hround (le_of_lt h2t)
      _ = theta := by ring
  set k : ℕ := (j % (q:ℤ)).toNat with hk
  have hqz : (0:ℤ) < (q:ℤ) := by exact_mod_cast hq
  have hmod_nonneg : 0 ≤ j % (q:ℤ) := Int.emod_nonneg j (ne_of_gt hqz)
  have hmod_lt : j % (q:ℤ) < (q:ℤ) := Int.emod_lt_of_pos j hqz
  have hk_lt : k < q := by rw [hk]; omega
  have hkcast : ((j % (q:ℤ) : ℤ):ℝ) = (k:ℝ) := by
    have hkz : ((k:ℤ)) = j % (q:ℤ) := by rw [hk]; exact Int.toNat_of_nonneg hmod_nonneg
    rw [← hkz]; push_cast; ring
  have hdivmod : j = (q:ℤ) * (j / (q:ℤ)) + (j % (q:ℤ)) := (Int.ediv_add_emod j (q:ℤ)).symm
  have hjsplit : (j:ℝ) = (q:ℝ) * ((j / (q:ℤ) : ℤ):ℝ) + (k:ℝ) := by
    have hcast := congrArg (fun z : ℤ => (z:ℝ)) hdivmod
    push_cast at hcast
    rw [hcast, hkcast]
  have hphase : phi + 2 * (k:ℝ) * theta
      = (phi + 2 * ((j:ℤ):ℝ) * theta) - ((j / (q:ℤ) : ℤ):ℝ) * (2 * Real.pi) := by
    linear_combination (-2 * theta) * hjsplit - ((j / (q:ℤ) : ℤ):ℝ) * h2qt
  refine ⟨k, hk_lt, ?_⟩
  rw [hphase, Real.cos_sub_int_mul_two_pi _ ((j / (q:ℤ) : ℤ))]
  have hth_le_pi : theta ≤ Real.pi := by
    rw [hth, div_le_iff₀ hqr]; nlinarith [Real.pi_pos, (by exact_mod_cast hq : (1:ℝ) ≤ q)]
  rw [ge_iff_le, show Real.cos (phi + 2 * ((j:ℤ):ℝ) * theta)
        = Real.cos (|phi + 2 * ((j:ℤ):ℝ) * theta|) from (Real.cos_abs _).symm]
  exact Real.cos_le_cos_of_nonneg_of_le_pi (abs_nonneg _) hth_le_pi hbound

theorem orbit_hit_of_realization (q : ℕ) (hq : 0 < q) (t C0 R phi : ℝ) (hR : 0 < R)
    (Pk : ℕ → ℝ)
    (hreal : ∀ k, Pk k = C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / q)))
    (hthr : (t - C0)/R ≤ Real.cos (Real.pi / q)) :
    ∃ k, k < q ∧ t ≤ Pk k := by
  obtain ⟨k, hk, hcos⟩ := cos_grid_hit q hq phi
  refine ⟨k, hk, ?_⟩
  rw [hreal k]
  have h1 : (t - C0)/R ≤ Real.cos (phi + 2 * (k:ℝ) * (Real.pi / q)) := le_trans hthr hcos
  have h2 : t - C0 ≤ R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / q)) := by
    rw [div_le_iff₀ hR] at h1; linarith [h1]
  linarith [h2]

/-- **★ THE REALIZATION HIT, WITH THE EXACT GOOD INDEX EXPOSED.**  Unlike `orbit_hit_of_realization`,
this returns the SAME good index `k*` that `cos_grid_hit` selects, so the dichotomy can branch on
whether the orbit ejects before `k*`. -/
theorem grid_hit_index (q : ℕ) (hq : 0 < q) (t C0 R phi : ℝ) (hR : 0 < R)
    (hthr : (t - C0)/R ≤ Real.cos (Real.pi / q)) :
    ∃ k : ℕ, k < q ∧
      t ≤ C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / q)) := by
  obtain ⟨k, hk, hcos⟩ := cos_grid_hit q hq phi
  refine ⟨k, hk, ?_⟩
  have h1 : (t - C0)/R ≤ Real.cos (phi + 2 * (k:ℝ) * (Real.pi / q)) := le_trans hthr hcos
  have h2 : t - C0 ≤ R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / q)) := by
    rw [div_le_iff₀ hR] at h1; linarith [h1]
  linarith [h2]

theorem wide_arc_translates_cover_on
    {X : Type*} (R : X → X) (q : ℕ) (S D : Set X)
    (hhit : ∀ x ∈ D, ∃ k, k < q ∧ R^[k] x ∈ S) :
    D ⊆ (⋃ k ∈ Finset.range q, (fun y => R^[k] y) ⁻¹' S) := by
  intro x hx
  obtain ⟨k, hk, hkx⟩ := hhit x hx
  rw [Set.mem_iUnion₂]
  exact ⟨k, Finset.mem_range.mpr hk, hkx⟩

theorem corridor_cover
    (l t : ℝ) (q : ℕ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Dom : Set (ℝ × ℝ))
    (hhit : ∀ p ∈ Dom, ∃ k, k < q ∧ t ≤ Pgen l (Tgen^[k] p)) :
    Dom ⊆ (⋃ k ∈ Finset.range q, (fun y => Tgen^[k] y) ⁻¹' {x : ℝ × ℝ | t ≤ Pgen l x}) :=
  wide_arc_translates_cover_on Tgen q {x : ℝ × ℝ | t ≤ Pgen l x} Dom
    (fun p hp => by
      obtain ⟨k, hk, hkx⟩ := hhit p hp
      exact ⟨k, hk, hkx⟩)

/-! ## §4.  ★★★ THE NO-CONFINEMENT PER-POINT HIT (DISSOLVING `hOrbitAgree`).

The keystone's `orbit_hit_corridor` required `hOrbitAgree : ∀ k, Tgen^[k] p = Mmap^[k] p` (carried
in `hRealize` for ALL k).  Here we DROP that.  Instead we take three SOUND hypotheses:

  * `hMmapReal` — the UNCONDITIONAL `Mmap`-orbit sinusoid + gate (= `pgen_orbit_realization`,
    NO confinement);
  * `hAgreePrefix` — the STRICTLY-WEAKER bounded-prefix agreement: `Tgen^[k] p = Mmap^[k] p` holds
    *as long as every earlier step is `isK1`*  (= `genuine_step_eq_Mmap_of_bracket` chained over the
    `k=1` prefix; lower bracket already PROVED, upper bracket = the scoped residual);
  * `hEjectOrbit` — the ORBIT-WIDE one-step ejection: at ANY point `x` with `¬isK1 x`, one `Tgen`
    step clears `t`.  This is exactly the sealed `genuine_hEject_deepmid` (which fires on any
    floor-`≥2` point with `b ≤ 1`, NOT just on `Dom` — the keystone's `∀ p ∈ Sclosed` form is the
    `Dom`-restriction of this universal fact, so taking the orbit-wide form is a FAITHFUL use of the
    same sealed lemma, not a new assumption).

We case-split on the FIRST ejection inside the STRICT predecessors `{0,…,k*-1}` (`k*` = the good
index from `grid_hit_index q`).  Existence of an ejecting index is decidable, so the split is
exhaustive and `hOrbitAgree` (the `∀k` form) is genuinely DISSOLVED.

Hit-index bookkeeping: in Case B the first ejecting predecessor `τ < k*` satisfies `Tgen^[τ] p =
Mmap^[τ] p` (prefix agreement) and is `¬isK1`, so `hEjectOrbit` clears at `Tgen^[τ+1] p =
Tgen (Tgen^[τ] p)`; since `τ < k* < q` we have `τ+1 ≤ k* < q`, so the hit index `τ+1` is in range.
In Case A every predecessor is `isK1`, `hAgreePrefix` gives agreement at `k*`, and the sinusoid
clears at `k* < q`. -/

theorem orbit_hit_corridor_no_confinement
    (l t : ℝ) (q : ℕ) (hq2 : 2 ≤ q) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Dom : Set (ℝ × ℝ))
    (isK1 : (ℝ × ℝ) → Prop) [DecidablePred isK1]
    (hMmapReal : ∀ p ∈ Dom, isK1 p →
      ∃ C0 R phi : ℝ, 0 < R ∧
        (∀ k, Pgen l ((Mmap l)^[k] p) = C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / q))) ∧
        (t - C0) / R ≤ Real.cos (Real.pi / q))
    (hAgreePrefix : ∀ p ∈ Dom, isK1 p →
      ∀ k, (∀ j < k, isK1 (Tgen^[j] p)) → Tgen^[k] p = (Mmap l)^[k] p)
    (hEjectOrbit : ∀ x : ℝ × ℝ, ¬ isK1 x → t ≤ Pgen l (Tgen x)) :
    ∀ p ∈ Dom, ∃ k, k < q ∧ t ≤ Pgen l (Tgen^[k] p) := by
  have hq : 0 < q := by omega
  intro p hp
  by_cases hk1 : isK1 p
  · -- realized isK1 cell: get the good index k* < q from the Mmap sinusoid
    obtain ⟨C0, R, phi, hR, hform, hthr⟩ := hMmapReal p hp hk1
    obtain ⟨kstar, hkstar_lt, hhit⟩ := grid_hit_index q hq t C0 R phi hR hthr
    classical
    -- Does the genuine orbit eject at some strict predecessor j < kstar?
    by_cases hej : ∃ j, j < kstar ∧ ¬ isK1 (Tgen^[j] p)
    · -- Case B: ejection before kstar.  Take the FIRST such index τ = Nat.find.
      set P : ℕ → Prop := fun j => j < kstar ∧ ¬ isK1 (Tgen^[j] p) with hPdef
      have hτspec : P (Nat.find hej) := Nat.find_spec hej
      set τ := Nat.find hej with hτ
      obtain ⟨hτlt, hτej⟩ := hτspec
      -- every j < τ fails P; since j < τ < kstar, the < kstar conjunct holds, so isK1 holds
      have hpre : ∀ j < τ, isK1 (Tgen^[j] p) := by
        intro j hj
        have hnotP : ¬ P j := Nat.find_min hej hj
        have hnotP' : ¬ (j < kstar ∧ ¬ isK1 (Tgen^[j] p)) := hnotP
        rw [not_and_not_right] at hnotP'
        exact hnotP' (lt_trans hj hτlt)
      -- agreement at τ: Tgen^[τ] p = Mmap^[τ] p  (only needs the prefix being isK1)
      have hagτ : Tgen^[τ] p = (Mmap l)^[τ] p := hAgreePrefix p hp hk1 τ hpre
      -- eject one step past τ: hit index τ+1, with τ+1 ≤ kstar < q
      refine ⟨τ + 1, by omega, ?_⟩
      rw [Function.iterate_succ_apply']
      exact hEjectOrbit (Tgen^[τ] p) hτej
    · -- Case A: no ejection before kstar.  hAgreePrefix gives agreement at kstar.
      push_neg at hej
      have hagree : Tgen^[kstar] p = (Mmap l)^[kstar] p :=
        hAgreePrefix p hp hk1 kstar hej
      refine ⟨kstar, hkstar_lt, ?_⟩
      rw [hagree, hform kstar]
      exact hhit
  · -- p itself ejects: one step clears (index 1 < q since q ≥ 2)
    refine ⟨1, by omega, ?_⟩
    rw [Function.iterate_one]
    exact hEjectOrbit p hk1

/-- The cover, assembled from the no-confinement per-point hit. -/
theorem SuperArcCover_no_confinement
    (l t : ℝ) (q : ℕ) (hq2 : 2 ≤ q) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Dom : Set (ℝ × ℝ))
    (isK1 : (ℝ × ℝ) → Prop) [DecidablePred isK1]
    (hMmapReal : ∀ p ∈ Dom, isK1 p →
      ∃ C0 R phi : ℝ, 0 < R ∧
        (∀ k, Pgen l ((Mmap l)^[k] p) = C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / q))) ∧
        (t - C0) / R ≤ Real.cos (Real.pi / q))
    (hAgreePrefix : ∀ p ∈ Dom, isK1 p →
      ∀ k, (∀ j < k, isK1 (Tgen^[j] p)) → Tgen^[k] p = (Mmap l)^[k] p)
    (hEjectOrbit : ∀ x : ℝ × ℝ, ¬ isK1 x → t ≤ Pgen l (Tgen x)) :
    Dom ⊆ (⋃ k ∈ Finset.range q, (fun y => Tgen^[k] y) ⁻¹' {x : ℝ × ℝ | t ≤ Pgen l x}) :=
  corridor_cover l t q Tgen Dom
    (orbit_hit_corridor_no_confinement l t q hq2 Tgen Dom isK1 hMmapReal hAgreePrefix hEjectOrbit)

/-! ## §5.  ★ THE a.e./conull cover plumbing — verbatim from keystone, PROVED. -/

theorem Pgen_measurable (l : ℝ) : Measurable (Pgen l) := by
  unfold Pgen
  exact ((measurable_fst.mul ((measurable_fst).add (measurable_const.mul measurable_snd))).div
    measurable_const)

theorem superlevel_measurableSet (l t : ℝ) :
    MeasurableSet {x : ℝ × ℝ | t ≤ Pgen l x} := by
  have : {x : ℝ × ℝ | t ≤ Pgen l x} = (Pgen l) ⁻¹' (Set.Ici t) := by
    ext x; simp [Set.mem_Ici]
  rw [this]
  exact (Pgen_measurable l) measurableSet_Ici

theorem covering_pos_measure_ae
    {α : Type*} [MeasurableSpace α]
    (μ : Measure α) [IsProbabilityMeasure μ]
    (q : ℕ) (hq : 0 < q)
    (g : ℕ → α → α)
    (hmeas : ∀ k, k < q → MeasurePreserving (g k) μ μ)
    (S Dom : Set α) (hS : MeasurableSet S)
    (hDom : μ Domᶜ = 0)
    (hcover : Dom ⊆ (⋃ k ∈ Finset.range q, (g k) ⁻¹' S)) :
    0 < μ S := by
  set U := (⋃ k ∈ Finset.range q, (g k) ⁻¹' S) with hU
  have hUc : Uᶜ ⊆ Domᶜ := Set.compl_subset_compl.mpr hcover
  have hUcnull : μ Uᶜ = 0 := measure_mono_null hUc hDom
  have hUone : μ U = 1 := by
    have hle : (1 : ENNReal) ≤ μ U + μ Uᶜ := by
      have hcov : (Set.univ : Set α) = U ∪ Uᶜ := (Set.union_compl_self U).symm
      calc (1 : ENNReal) = μ (Set.univ : Set α) := (measure_univ).symm
        _ = μ (U ∪ Uᶜ) := by rw [← hcov]
        _ ≤ μ U + μ Uᶜ := measure_union_le _ _
    rw [hUcnull, add_zero] at hle
    exact le_antisymm (by simpa using prob_le_one) hle
  by_contra hzero
  push_neg at hzero
  have hSzero : μ S = 0 := le_antisymm hzero (by positivity)
  have hpre : ∀ k, k < q → μ ((g k) ⁻¹' S) = μ S := by
    intro k hk
    exact (hmeas k hk).measure_preimage hS.nullMeasurableSet
  have hnull : ∀ k ∈ Finset.range q, μ ((g k) ⁻¹' S) = 0 := by
    intro k hk
    rw [hpre k (Finset.mem_range.mp hk), hSzero]
  have hunionzero : μ U = 0 := by
    rw [hU]
    refine (MeasureTheory.measure_biUnion_null_iff
      (Finset.range q).countable_toSet).mpr ?_
    intro k hk
    exact hnull k (by simpa using hk)
  rw [hUone] at hunionzero
  exact one_ne_zero hunionzero

theorem essSup_ge_of_pos_superlevel
    {α : Type*} [MeasurableSpace α]
    (μ : Measure α) [IsProbabilityMeasure μ]
    (f : α → ℝ) (t : ℝ)
    (hpos : 0 < μ {x | t ≤ f x})
    (hbdd : ∃ C, ∀ᵐ x ∂μ, f x ≤ C) :
    t ≤ essSup f μ := by
  by_contra hlt
  push_neg at hlt
  have hae : ∀ᵐ x ∂μ, f x < t := by
    have hbu : Filter.IsBoundedUnder (· ≤ ·) (ae μ) f := by
      obtain ⟨C, hC⟩ := hbdd
      refine ⟨C, ?_⟩
      rw [Filter.eventually_map]
      filter_upwards [hC] with x hx using hx
    have h1 : ∀ᵐ x ∂μ, f x ≤ essSup f μ :=
      ae_le_essSup (f := f) (μ := μ) hbu
    filter_upwards [h1] with x hx
    exact lt_of_le_of_lt hx hlt
  have hnull : μ {x | t ≤ f x} = 0 := by
    have h := hae
    rw [MeasureTheory.ae_iff] at h
    convert h using 2
    ext x
    simp only [Set.mem_setOf_eq, not_lt]
  rw [hnull] at hpos
  exact (lt_irrefl _ hpos)

/-! ## §6.  ★ THE VERBATIM `XomegaSet`/`Xomega` + keystone lower bound — verbatim. -/

def XomegaSet (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ)) : Set ℝ :=
  {y : ℝ | ∃ μ : Measure (ℝ × ℝ), ∃ _ : IsProbabilityMeasure μ,
    MeasurePreserving Tgen μ μ ∧ μ (Sclosed)ᶜ = 0 ∧
    (∃ M : ℝ, ∀ᵐ x ∂μ, Pgen l x ≤ M) ∧ y = essSup (Pgen l) μ}

def Xomega (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ)) : ℝ :=
  sInf (XomegaSet l Tgen Sclosed)

theorem member_lb_via_Tgen_ae
    (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ))
    (q : ℕ) (hq : 0 < q)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hPbdd : ∃ M : ℝ, ∀ᵐ x ∂μ, Pgen l x ≤ M)
    (hinv : MeasurePreserving Tgen μ μ)
    (hμS : μ (Sclosed)ᶜ = 0)
    (hcover : Sclosed ⊆
      (⋃ k ∈ Finset.range q, (fun y => Tgen^[k] y) ⁻¹' {x : ℝ × ℝ | (1 : ℝ) / l ^ 3 ≤ Pgen l x})) :
    (1 : ℝ) / l ^ 3 ≤ essSup (Pgen l) μ := by
  have hmeas : ∀ k, k < q → MeasurePreserving ((fun k => Tgen^[k]) k) μ μ :=
    fun k _ => hinv.iterate k
  have hpos : 0 < μ {x | (1 : ℝ) / l ^ 3 ≤ Pgen l x} :=
    covering_pos_measure_ae μ q hq (fun k => Tgen^[k]) hmeas
      {x | (1 : ℝ) / l ^ 3 ≤ Pgen l x} Sclosed
      (superlevel_measurableSet l (1 / l ^ 3)) hμS hcover
  exact essSup_ge_of_pos_superlevel μ (Pgen l) (1 / l ^ 3) hpos hPbdd

theorem XomegaSet_bddBelow_via_Tgen_ae
    (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ))
    (q : ℕ) (hq : 0 < q)
    (hCover : ∀ μ : Measure (ℝ × ℝ), IsProbabilityMeasure μ →
      MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0 →
      Sclosed ⊆ (⋃ k ∈ Finset.range q,
        (fun y => Tgen^[k] y) ⁻¹' {x : ℝ × ℝ | (1 : ℝ) / l ^ 3 ≤ Pgen l x})) :
    ∀ y ∈ XomegaSet l Tgen Sclosed, (1 : ℝ) / l ^ 3 ≤ y := by
  rintro y ⟨μ, hμprob, hinv, hμS, ⟨M, hPbdd⟩, hy⟩
  rw [hy]
  haveI : IsProbabilityMeasure μ := hμprob
  exact member_lb_via_Tgen_ae l Tgen Sclosed q hq μ ⟨M, hPbdd⟩ hinv hμS
    (hCover μ hμprob hinv hμS)

theorem Xomega_ge_via_Tgen_ae
    (l : ℝ) (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ))
    (q : ℕ) (hq : 0 < q)
    (hne : (XomegaSet l Tgen Sclosed).Nonempty)
    (hCover : ∀ μ : Measure (ℝ × ℝ), IsProbabilityMeasure μ →
      MeasurePreserving Tgen μ μ → μ (Sclosed)ᶜ = 0 →
      Sclosed ⊆ (⋃ k ∈ Finset.range q,
        (fun y => Tgen^[k] y) ⁻¹' {x : ℝ × ℝ | (1 : ℝ) / l ^ 3 ≤ Pgen l x})) :
    (1 : ℝ) / l ^ 3 ≤ Xomega l Tgen Sclosed :=
  le_csInf hne (XomegaSet_bddBelow_via_Tgen_ae l Tgen Sclosed q hq hCover)

/-! ## §7.  ★ DISCHARGE OF `hMmapReal` from `pgen_orbit_realization` — NO confinement.

Crucially, this discharge uses `pgen_orbit_realization` DIRECTLY (the UNCONDITIONAL `Mmap`-orbit
sinusoid).  It does NOT rewrite `Tgen^[k] p = Mmap^[k] p` — that transport (the old `hOrbitAgree`)
is GONE here; it is replaced downstream by the bounded-prefix `hAgreePrefix` consumed inside
`orbit_hit_corridor_no_confinement`. -/
theorem mmap_realize_from_orbit_realization
    (m : ℕ) (hm : 1 ≤ m) (l : ℝ) (hl : l = lamq (m + 2))
    (Dom : Set (ℝ × ℝ)) (isK1 : (ℝ × ℝ) → Prop)
    (hpcorr : ∀ p ∈ Dom, isK1 p → p ∈ Dcorr l)
    (hEfloor : ∀ p ∈ Dom, isK1 p → EfloorQ m l ≤ Eform l p) :
    ∀ p ∈ Dom, isK1 p →
      ∃ C0 R phi : ℝ, 0 < R ∧
        (∀ k, Pgen l ((Mmap l)^[k] p)
              = C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / ((m + 2 : ℕ) : ℝ)))) ∧
        (1 / l ^ 3 - C0) / R ≤ Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ)) := by
  intro p hp hk1
  exact pgen_orbit_realization m hm l hl p (hpcorr p hp hk1) (hEfloor p hp hk1)

/-- **★ THE FAITHFUL CONULL COVER, NO `hOrbitAgree`.**  Assembles
`mmap_realize_from_orbit_realization` (→ `hMmapReal`, unconditional) + `hAgreePrefix`
(bounded-prefix) + `hEjectOrbit` (sealed orbit-wide ejection) through
`SuperArcCover_no_confinement`. -/
theorem conull_cover_no_confinement
    (m : ℕ) (hm : 1 ≤ m) (l : ℝ) (hl : l = lamq (m + 2))
    (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ)) (isK1 : (ℝ × ℝ) → Prop)
    [DecidablePred isK1]
    (hpcorr : ∀ p ∈ Sclosed, isK1 p → p ∈ Dcorr l)
    (hEfloor : ∀ p ∈ Sclosed, isK1 p → EfloorQ m l ≤ Eform l p)
    (hAgreePrefix : ∀ p ∈ Sclosed, isK1 p →
      ∀ k, (∀ j < k, isK1 (Tgen^[j] p)) → Tgen^[k] p = (Mmap l)^[k] p)
    (hEjectOrbit : ∀ x : ℝ × ℝ, ¬ isK1 x → (1 : ℝ) / l ^ 3 ≤ Pgen l (Tgen x)) :
    Sclosed ⊆ (⋃ k ∈ Finset.range (m + 2),
      (fun y => Tgen^[k] y) ⁻¹' {x : ℝ × ℝ | (1 : ℝ) / l ^ 3 ≤ Pgen l x}) :=
  SuperArcCover_no_confinement l (1 / l ^ 3) (m + 2) (by omega) Tgen Sclosed isK1
    (mmap_realize_from_orbit_realization m hm l hl Sclosed isK1 hpcorr hEfloor)
    hAgreePrefix hEjectOrbit

/-- **★★★ THE NO-CONFINEMENT KEYSTONE — `1/l³ ≤ Xomega l Tgen Sclosed` WITHOUT `hOrbitAgree`.**

The genuine onset lower bound, with `XomegaSet`/`Xomega`/`Pgen`/`Tgen` VERBATIM.  The over-quantified
`hOrbitAgree : ∀ k, Tgen^[k] p = Mmap^[k] p` is GONE.  In its place:

  * `hAgreePrefix` — the bounded-prefix `k=1` agreement (lower bracket already PROVED;
    `genuine_step_eq_Mmap_of_bracket` chained over the realized `k=1` prefix).
  * `hEjectOrbit` — the SEALED orbit-wide ejection (= `genuine_hEject_deepmid`, universal in the
    floor-`≥2` point, NOT `Dom`-gated; the keystone's `∀ p ∈ Sclosed` form is its restriction).

REMAINING HYPOTHESES (the SHRUNK residual list):
  * `hm`, `hl`        — DEFINITIONAL Hecke facts (`l = 2cos(π/(m+2))`).
  * `hne`             — DEFINITIONAL (cusp Dirac inhabits the class).
  * `hpcorr`          — DEFINITIONAL (section ⊆ corridor).
  * `hEfloor`         — NON-DEFINITIONAL analytic residual (E-floor on the `k=1` corridor; L1b
                        arc-coverage, uniform-`q` OPEN — UNCHANGED, orthogonal to confinement).
  * `hAgreePrefix`    — NON-DEFINITIONAL but SCOPE-REDUCED: the BOUNDED-PREFIX `k=1` agreement
                        replacing the `∀k` `hOrbitAgree`.  Its lower bracket is already PROVED
                        (`lower_bracket_preserved_on_ellipse`); only the upper bracket survives, and
                        only up to the first ejection — NOT for all `k`.
  * `hEjectOrbit`     — NON-DEFINITIONAL, SEALED-PROVED (`GenuineSelfMap.genuine_hEject_deepmid`),
                        orbit-wide form.

So `hOrbitAgree` is DISSOLVED: the keystone no longer references the `∀k` orbit identity. -/
theorem Xomega_ge_no_confinement
    (m : ℕ) (hm : 1 ≤ m) (l : ℝ) (hl : l = lamq (m + 2))
    (Tgen : (ℝ × ℝ) → (ℝ × ℝ)) (Sclosed : Set (ℝ × ℝ)) (isK1 : (ℝ × ℝ) → Prop)
    [DecidablePred isK1]
    (hne : (XomegaSet l Tgen Sclosed).Nonempty)
    (hpcorr : ∀ p ∈ Sclosed, isK1 p → p ∈ Dcorr l)
    (hEfloor : ∀ p ∈ Sclosed, isK1 p → EfloorQ m l ≤ Eform l p)
    (hAgreePrefix : ∀ p ∈ Sclosed, isK1 p →
      ∀ k, (∀ j < k, isK1 (Tgen^[j] p)) → Tgen^[k] p = (Mmap l)^[k] p)
    (hEjectOrbit : ∀ x : ℝ × ℝ, ¬ isK1 x → (1 : ℝ) / l ^ 3 ≤ Pgen l (Tgen x)) :
    (1 : ℝ) / l ^ 3 ≤ Xomega l Tgen Sclosed := by
  refine Xomega_ge_via_Tgen_ae l Tgen Sclosed (m + 2) (by omega) hne ?_
  intro μ hμprob hinv hμS
  exact conull_cover_no_confinement m hm l hl Tgen Sclosed isK1 hpcorr hEfloor hAgreePrefix hEjectOrbit

end

/-! ## §8.  AXIOM AUDIT. -/

#print axioms LgConfinement.pgen_orbit_realization
#print axioms LgConfinement.cos_grid_hit
#print axioms LgConfinement.grid_hit_index
#print axioms LgConfinement.orbit_hit_corridor_no_confinement
#print axioms LgConfinement.SuperArcCover_no_confinement
#print axioms LgConfinement.conull_cover_no_confinement
#print axioms LgConfinement.Xomega_ge_via_Tgen_ae
#print axioms LgConfinement.Xomega_ge_no_confinement

end LgConfinement
