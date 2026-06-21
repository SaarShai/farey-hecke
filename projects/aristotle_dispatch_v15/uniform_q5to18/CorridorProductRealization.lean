import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# `corridor_product_realization` — the product-observable orbit identity (R1 of `hbridge`).

This file proves the corridor analog of the energy-route `pgen_orbit_realization` (PROVED
axiom-clean in `hsa_realization_lean/RequestProject/Main.lean`).  Here the observable is the
*product* `P = a·b` (the genuine `product_form` on branch `q−1`) rather than `Pgen = a(a+λb)/λ`,
and the map is the `W_q`-block monodromy `M_W` whose conserved form is `Qp` (not `Eform`).

## The identity (R1, UNCONDITIONAL)

Along the `M_W`-orbit of a block-boundary point `s0 = (a,b)`, the product `P k = a_k·b_k` is the
affine sinusoid

    P k = C0 + R · cos(φ + 2kθ),    θ = π/q,

with constants (verified symbolically, `code/...derive`):

    C0 = 3λ · Qp / (4 − λ²),     R = 2√(2λ²+1) · Qp / (4 − λ²),    Qp = a² − 3λab + (2λ²+1)b²,

and `R > 0` on the corridor (`Qp > 0`).  The doubled frequency `2θ` is because `P` is degree-2 in
the rotating coordinates; `2cos(2θ) = λ² − 2` is the product-recurrence coefficient.

This is the **R1 (sinusoid-realization)** half of the `hbridge` input
`BCZHeckeGATE2_L1_skeleton.no_sustained_corridor` needs.  The remaining **R2 (sup ≥ g_corr window
pigeonhole)** half — matching this orbit's actual phase `μc` to the `windowMaxCos` grid offset and
the `fcorr` denominator `cos²(|μc|+H)` normalization — is discussed in the companion note; it is the
genuine residual.  Here we deliver R1 sorry-free and axiom-clean, plus the recurrence and the
amplitude pinning, which is the substantive new mathematics.

Sealed objects reproduced VERBATIM from `BCZHeckeGATE2_L1_skeleton.lean` / `L1bArcCoverage.lean`:
  `lamq q = 2cos(π/q)`,  `M_W (a,b) = (−λa + (2λ²+1)b, −a + 2λb)`,
  `Qp l a b = a² − 3λab + (2λ²+1)b²`,  `P = a·b`.
-/

namespace CorridorProductRealization

noncomputable section
open Real

/-! ## §0.  Verbatim sealed objects (matching the skeleton). -/

def lamq (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)
def thetaq (q : ℕ) : ℝ := Real.pi / q

/-- `M_W (a,b) = (−λa + (2λ²+1)b, −a + 2λb)` — the `W_q` block monodromy (verbatim `hblk`). -/
def MW (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ :=
  (-l * p.1 + (2 * l ^ 2 + 1) * p.2, -p.1 + 2 * l * p.2)

/-- The conserved `M_W`-ellipse `Qp` (verbatim `BCZHeckeGATE2_L1_skeleton.Qp`). -/
def Qp (l : ℝ) (a b : ℝ) : ℝ := a ^ 2 - 3 * l * (a * b) + (2 * l ^ 2 + 1) * b ^ 2

@[simp] lemma MW_fst (l : ℝ) (p : ℝ × ℝ) : (MW l p).1 = -l * p.1 + (2 * l ^ 2 + 1) * p.2 := rfl
@[simp] lemma MW_snd (l : ℝ) (p : ℝ × ℝ) : (MW l p).2 = -p.1 + 2 * l * p.2 := rfl

/-- **`M_W` preserves `Qp`** (by `ring`). -/
theorem MW_preserves_Qp (l : ℝ) (p : ℝ × ℝ) :
    Qp l (MW l p).1 (MW l p).2 = Qp l p.1 p.2 := by
  simp only [Qp, MW]; ring

/-! ## §1.  General sinusoid-from-2-step-recurrence (PROVED, self-contained).
    Identical to `hsa_realization_lean`'s `recur_closed_form` / `recur_to_Rcos`. -/

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
    have hcos2 : Real.cos (2 * ω) = 2 * Real.cos ω ^ 2 - 1 := by rw [Real.cos_two_mul]
    have hsin2 : Real.sin (2 * ω) = 2 * Real.sin ω * Real.cos ω := by rw [Real.sin_two_mul]
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

/-! ## §2.  ★ THE PRODUCT-OBSERVABLE ORBIT IDENTITY (R1, faithful, unconditional). -/

/-- Product-form constants (`l`-only times `Qp`). -/
def C0form (l Q : ℝ) : ℝ := 3 * l * Q / (4 - l ^ 2)
def Rform (l Q : ℝ) : ℝ := 2 * Real.sqrt (2 * l ^ 2 + 1) * Q / (4 - l ^ 2)

/-- **★ THE PRODUCT ORBIT IDENTITY.**  For `q = m+2 ≥ 3`, `l = lamq q`, and any block-boundary
point `s0 = (a,b)` with `Qp l a b > 0` (in particular any corridor point with `a,b > 0`), the
`M_W`-orbit product `P k = (M_W^[k] s0).1 · (M_W^[k] s0).2` is the affine sinusoid

    P k = C0 + R · cos(φ + 2kθ),    C0 = 3λQp/(4−λ²),  R = 2√(2λ²+1)Qp/(4−λ²),  θ = π/q,

with `R > 0`.  UNCONDITIONAL (no E-floor / domain gate needed for R1). -/
theorem corridor_product_realization (m : ℕ) (hm : 1 ≤ m) (l : ℝ) (hl : l = lamq (m + 2))
    (a b : ℝ) (hQpos : 0 < Qp l a b) :
    ∃ C0 R phi : ℝ, 0 < R ∧
      C0 = C0form l (Qp l a b) ∧ R = Rform l (Qp l a b) ∧
      (∀ k, ((MW l)^[k] (a, b)).1 * ((MW l)^[k] (a, b)).2
            = C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / ((m + 2 : ℕ) : ℝ)))) := by
  have hq3 : 3 ≤ m + 2 := by omega
  set q : ℕ := m + 2 with hq_def
  set θ : ℝ := Real.pi / (q : ℝ) with hθ_def
  have hqr : (0:ℝ) < (q:ℝ) := by positivity
  have hqr3 : (3:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq3
  have hθpos : 0 < θ := by rw [hθ_def]; positivity
  have hcosθ : Real.cos θ = l / 2 := by rw [hl, lamq, hq_def, ← hθ_def]; ring
  have hcospos : 0 < Real.cos θ := by
    apply Real.cos_pos_of_mem_Ioo
    constructor
    · linarith [Real.pi_pos, hθpos]
    · rw [hθ_def, div_lt_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
  have hl_pos : 0 < l := by rw [hl, lamq, hq_def, ← hθ_def]; linarith [hcospos]
  have hcos_lt1 : Real.cos θ < 1 := by
    have hθpi : θ ≤ Real.pi := by
      rw [hθ_def, div_le_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
    have := Real.cos_lt_cos_of_nonneg_of_le_pi (le_refl (0:ℝ)) hθpi hθpos
    rwa [Real.cos_zero] at this
  have hl_lt2 : l < 2 := by rw [hl, lamq, hq_def, ← hθ_def]; linarith [hcos_lt1]
  have h4 : 0 < 4 - l ^ 2 := by nlinarith [hl_pos, hl_lt2]
  have h4ne : (4 - l ^ 2) ≠ 0 := ne_of_gt h4
  have hlne : l ≠ 0 := ne_of_gt hl_pos
  -- cos(2θ) = l²/2 − 1
  have hcos2 : Real.cos (2 * θ) = l ^ 2 / 2 - 1 := by
    rw [Real.cos_two_mul, hcosθ]; ring
  have h2θpos : 0 < 2 * θ := by linarith
  have h2θlt : 2 * θ < Real.pi := by
    rw [hθ_def]; rw [show (2:ℝ) * (Real.pi / q) = 2 * Real.pi / q by ring, div_lt_iff₀ hqr]
    nlinarith [Real.pi_pos, hqr3]
  have hsin2pos : 0 < Real.sin (2 * θ) := Real.sin_pos_of_pos_of_lt_pi h2θpos h2θlt
  have hsin2ne : Real.sin (2 * θ) ≠ 0 := ne_of_gt hsin2pos
  -- abbreviations
  set Q : ℝ := Qp l a b with hQ_def
  set C0 : ℝ := C0form l Q with hC0_def
  -- the orbit and its product
  set P : ℕ → ℝ := fun k => ((MW l)^[k] (a, b)).1 * ((MW l)^[k] (a, b)).2 with hP_def
  -- Qp preserved along the orbit
  have hQorb : ∀ k, Qp l ((MW l)^[k] (a, b)).1 ((MW l)^[k] (a, b)).2 = Q := by
    intro k
    induction k with
    | zero => simp [hQ_def]
    | succ n ih =>
      rw [Function.iterate_succ_apply']
      rw [show ((MW l) ((MW l)^[n] (a, b))).1 = (MW l ((MW l)^[n] (a, b))).1 from rfl,
          show ((MW l) ((MW l)^[n] (a, b))).2 = (MW l ((MW l)^[n] (a, b))).2 from rfl]
      rw [MW_preserves_Qp l ((MW l)^[n] (a, b))]; exact ih
  -- the offset sequence and its homogeneous recurrence
  set hseq : ℕ → ℝ := fun k => P k - C0 with hseq_def
  have hrec : ∀ k, hseq (k + 2) = 2 * Real.cos (2 * θ) * hseq (k + 1) - hseq k := by
    intro k
    rw [hcos2]
    simp only [hseq_def, hP_def]
    set x := (MW l)^[k] (a, b) with hx_def
    have e1 : (MW l)^[k+1] (a, b) = MW l x := by rw [hx_def, Function.iterate_succ_apply']
    have e2 : (MW l)^[k+2] (a, b) = MW l (MW l x) := by
      rw [hx_def, show k + 2 = (k+1)+1 by ring, Function.iterate_succ_apply',
          Function.iterate_succ_apply']
    rw [e1, e2]
    -- C0 = 3λ·Qp(x)/(4−λ²) since Qp preserved
    have hCx : C0 = 3 * l * Qp l x.1 x.2 / (4 - l ^ 2) := by
      rw [hC0_def, C0form, hQ_def]
      have : Qp l x.1 x.2 = Qp l a b := by rw [hx_def]; exact hQorb k
      rw [this]
    rw [hCx]
    simp only [MW, Qp]
    field_simp
    ring
  -- get the Rcos form
  obtain ⟨R, phi, hRnn, hRiff, hform⟩ := recur_to_Rcos (2 * θ) hsin2ne hseq hrec
  -- amplitude invariant ⟹ R = Rform
  have hamp : hseq 0 ^ 2 - 2 * Real.cos (2*θ) * hseq 0 * hseq 1 + hseq 1 ^ 2
      = (Rform l Q) ^ 2 * (Real.sin (2*θ)) ^ 2 := by
    rw [hcos2]
    have hsin2sq : Real.sin (2*θ) ^ 2 = 1 - (l^2/2 - 1)^2 := by
      have := Real.sin_sq_add_cos_sq (2*θ); rw [hcos2] at this; linarith [this]
    rw [hsin2sq]
    set s := Real.sqrt (2 * l ^ 2 + 1) with hs_def
    have hssq : s ^ 2 = 2 * l ^ 2 + 1 := Real.sq_sqrt (by positivity)
    -- hseq 0 = ab − C0,  hseq 1 = (MW(a,b)).1·(MW(a,b)).2 − C0
    have hh0 : hseq 0 = a * b - C0 := by simp [hseq_def, hP_def]
    have hh1 : hseq 1 = (-l*a + (2*l^2+1)*b) * (-a + 2*l*b) - C0 := by
      simp [hseq_def, hP_def, MW]
    rw [hh0, hh1, hC0_def, C0form, Rform, hQ_def, ← hs_def]
    -- Q = a² − 3λab + (2λ²+1)b²  (unfold)
    simp only [Qp]
    field_simp
    -- the RHS is the only place `s` occurs, as `s²`; eliminate it via `hssq`, then `ring`.
    rw [hssq]
    ring
  have hampR : hseq 0 ^ 2 - 2 * Real.cos (2*θ) * hseq 0 * hseq 1 + hseq 1 ^ 2
      = R ^ 2 * (Real.sin (2*θ)) ^ 2 := by
    have e0 : hseq 0 = R * Real.cos phi := by rw [hform 0]; norm_num
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
  -- Rform > 0
  have hRform_pos : 0 < Rform l Q := by
    rw [Rform]
    apply div_pos
    · apply mul_pos (by positivity)
      exact hQpos
    · exact h4
  have hReq2 : R ^ 2 = (Rform l Q) ^ 2 := by
    have hs2 : (Real.sin (2*θ))^2 > 0 := by positivity
    have : R ^ 2 * (Real.sin (2*θ))^2 = (Rform l Q)^2 * (Real.sin (2*θ))^2 := by
      rw [← hampR, hamp]
    exact mul_right_cancel₀ (ne_of_gt hs2) this
  have hReq : R = Rform l Q := by
    nlinarith [hReq2, hRnn, le_of_lt hRform_pos, sq_nonneg (R - Rform l Q), sq_nonneg (R + Rform l Q)]
  have hRpos : 0 < R := by rw [hReq]; exact hRform_pos
  refine ⟨C0, R, phi, hRpos, rfl, hReq, ?_⟩
  intro k
  have hPk : ((MW l)^[k] (a, b)).1 * ((MW l)^[k] (a, b)).2 = hseq k + C0 := by
    rw [hseq_def]; simp only [hP_def]; ring
  rw [hPk, hform k]
  have hphase : phi + (k:ℝ) * (2*θ) = phi + 2 * (k:ℝ) * (Real.pi / ((m+2:ℕ):ℝ)) := by
    rw [hθ_def, hq_def]; ring
  rw [hphase]; ring

/-! ## §3.  ★ THE DOMAIN-OBSERVABLE ORBIT IDENTITY (R2b ingredient, faithful, unconditional).

The in-domain (lower Taha edge) observable `D = a + λb` is the SECOND sinusoid the bridge needs:
it pins the conserved radius `r²` to the `fcorr` denominator `cos²(|μc|+H)` via the window-min
forcing `Dom_n > 1 ⟹ r² ≥ 1/(Blam²cos²(...))`.  Unlike the product `P` (frequency `2θ`), `D` is
degree-1 in the rotating coordinates, so it is a single-frequency sinusoid (frequency `θ`):

    D k = (a_k + λ b_k) = Damp · cos(ψ + kθ),    Damp² = (6λ²+1)·Qp / sin²θ = r²·Blam²,

with `r² = 4(2λ²+1)Qp/(4−λ²)`, `Blam² = (12λ⁴+8λ²+1)/(2λ²+1)²` (verified symbolically).  Here we
deliver the closed form + the amplitude pinning `Damp² = (6λ²+1)Qp/sin²θ`, axiom-clean. -/

/-- **★ THE DOMAIN ORBIT IDENTITY.**  For `q = m+2 ≥ 3`, `l = lamq q`, any block-boundary point
`s0 = (a,b)`, the `M_W`-orbit domain observable `D k = (M_W^[k] s0).1 + λ·(M_W^[k] s0).2` is the
single-frequency sinusoid `Damp·cos(ψ + kθ)` with `Damp ≥ 0` and `Damp² · sin²θ = (6λ²+1)·Qp`
(the amplitude pinning; `Qp > 0 ⟹ Damp > 0`). -/
theorem corridor_domain_realization (m : ℕ) (hm : 1 ≤ m) (l : ℝ) (hl : l = lamq (m + 2))
    (a b : ℝ) :
    ∃ Damp psi : ℝ, 0 ≤ Damp ∧
      Damp ^ 2 * Real.sin (Real.pi / ((m + 2 : ℕ) : ℝ)) ^ 2 = (6 * l ^ 2 + 1) * Qp l a b ∧
      (∀ k, ((MW l)^[k] (a, b)).1 + l * ((MW l)^[k] (a, b)).2
            = Damp * Real.cos (psi + (k:ℝ) * (Real.pi / ((m + 2 : ℕ) : ℝ)))) := by
  have hq3 : 3 ≤ m + 2 := by omega
  set q : ℕ := m + 2 with hq_def
  set θ : ℝ := Real.pi / (q : ℝ) with hθ_def
  have hqr : (0:ℝ) < (q:ℝ) := by positivity
  have hqr3 : (3:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq3
  have hθpos : 0 < θ := by rw [hθ_def]; positivity
  have hθlt : θ < Real.pi := by
    rw [hθ_def, div_lt_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
  have hcosθ : Real.cos θ = l / 2 := by rw [hl, lamq, hq_def, ← hθ_def]; ring
  have hsinpos : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθpos hθlt
  have hsinne : Real.sin θ ≠ 0 := ne_of_gt hsinpos
  -- D-sequence
  set D : ℕ → ℝ := fun k => ((MW l)^[k] (a, b)).1 + l * ((MW l)^[k] (a, b)).2 with hD_def
  -- 2cos θ = l
  have hl2cos : 2 * Real.cos θ = l := by rw [hcosθ]; ring
  -- single-frequency Chebyshev recurrence D(k+2) = l·D(k+1) − D(k) = 2cosθ·D(k+1) − D(k)
  have hrec : ∀ k, D (k + 2) = 2 * Real.cos θ * D (k + 1) - D k := by
    intro k
    rw [hl2cos]
    simp only [hD_def]
    set x := (MW l)^[k] (a, b) with hx_def
    have e1 : (MW l)^[k+1] (a, b) = MW l x := by rw [hx_def, Function.iterate_succ_apply']
    have e2 : (MW l)^[k+2] (a, b) = MW l (MW l x) := by
      rw [hx_def, show k + 2 = (k+1)+1 by ring, Function.iterate_succ_apply',
          Function.iterate_succ_apply']
    rw [e1, e2]
    simp only [MW]; ring
  obtain ⟨R, psi, hRnn, hRiff, hform⟩ := recur_to_Rcos θ hsinne D hrec
  -- amplitude invariant for the θ-rotation: D0² − 2cosθ·D0·D1 + D1² = R²·sin²θ = (6λ²+1)Qp
  have hampL : D 0 ^ 2 - 2 * Real.cos θ * D 0 * D 1 + D 1 ^ 2 = (6 * l ^ 2 + 1) * Qp l a b := by
    have hD0 : D 0 = a + l * b := by simp [hD_def]
    have hD1 : D 1 = (-l*a + (2*l^2+1)*b) + l * (-a + 2*l*b) := by
      simp [hD_def, MW]
    rw [hD0, hD1, hcosθ]
    simp only [Qp]; ring
  have hampR : D 0 ^ 2 - 2 * Real.cos θ * D 0 * D 1 + D 1 ^ 2 = R ^ 2 * Real.sin θ ^ 2 := by
    have e0 : D 0 = R * Real.cos psi := by rw [hform 0]; norm_num
    have e1 : D 1 = R * (Real.cos psi * Real.cos θ - Real.sin psi * Real.sin θ) := by
      rw [hform 1]; rw [show (((1:ℕ):ℝ) * θ) = θ by norm_num, Real.cos_add]
    rw [e0, e1]
    have hpψ : Real.sin psi ^ 2 = 1 - Real.cos psi ^ 2 := by
      have := Real.sin_sq_add_cos_sq psi; linarith
    have hpyth2 : Real.cos θ ^ 2 = 1 - Real.sin θ ^ 2 := by
      have := Real.sin_sq_add_cos_sq θ; linarith
    have hexpand :
        (R * Real.cos psi) ^ 2
        - 2 * Real.cos θ * (R * Real.cos psi)
            * (R * (Real.cos psi * Real.cos θ - Real.sin psi * Real.sin θ))
        + (R * (Real.cos psi * Real.cos θ - Real.sin psi * Real.sin θ)) ^ 2
        = R ^ 2 * (Real.cos psi ^ 2 * (1 - Real.cos θ ^ 2)
                   + Real.sin psi ^ 2 * Real.sin θ ^ 2) := by ring
    rw [hexpand, hpyth2, hpψ]; ring
  refine ⟨R, psi, hRnn, ?_, ?_⟩
  · -- Damp² sin²θ = (6λ²+1)Qp : both equal the rotation invariant.  θ = π/(m+2) defeq.
    show R ^ 2 * Real.sin θ ^ 2 = (6 * l ^ 2 + 1) * Qp l a b
    rw [← hampR]; exact hampL
  · intro k
    have hk := hform k
    simp only [hD_def] at hk
    rw [hθ_def]
    exact hk

#print axioms corridor_product_realization
#print axioms corridor_domain_realization
#print axioms MW_preserves_Qp

end

end CorridorProductRealization
