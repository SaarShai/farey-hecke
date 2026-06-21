import Mathlib

open scoped BigOperators
open scoped Real
open scoped Nat

set_option maxHeartbeats 4000000

/-!
# `pgen_orbit_realization` — the realization wiring lemma for `hSuperArc`.

Along the `Mmap`-orbit of a corridor point, the genuine observable `Pgen` is an affine sinusoid
`C0 + R·cos(φ + 2kθ)` on the conserved energy ellipse `E`, and (under the corridor `E`-floor) its
threshold gate `(1/l³ − C0)/R ≤ cos θ` holds.

The orbit identity (R1) is UNCONDITIONAL; the gate (R2) is gated by an explicit `E`-floor
hypothesis `hE : Efloor l ≤ Eform l p`.  The current too-strong `Main.lean:326-337` statement
(gate for ALL `p ∈ Dcorr`) is FALSE for small `q` (numerically `q=5` has corridor points with
`E < Efloor`); the faithful statement carries `hE`.

Sealed defs reproduced VERBATIM:
  `lamq q = 2 cos(π/q)`,  `Mmap l (a,b) = (b, −a+l b)`,  `Pgen l (a,b) = a(a+l b)/l`,
  `Eform l (a,b) = a² − l a b + b²`,
  `Dcorr l = {0<a≤1, 0<b≤1, a+lb>1, la+b>1}`.

Constants (Kaggle `saarshai/hsa-constants`, verified to 50+ dps; symbolic `sympy`):
  `alpha l = (l²+2)/(l(4−l²)) = 1/(4c)+3c/(4s²)`   (c=cos θ, s=sin θ)
  `rho   l = 2√(2l²+1)/(l(4−l²)) = √(8c²+1)/(4s²c)`
  `Efloor l = 1/(l³(alpha l + rho l · c))`.
-/

noncomputable section
open MeasureTheory

/-! ## §0.  Verbatim sealed objects. -/

def lamq (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)
def thetaq (q : ℕ) : ℝ := Real.pi / q
def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
def Eform (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2
def Dcorr (l : ℝ) : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}

@[simp] lemma Mmap_fst (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).1 = p.2 := rfl
@[simp] lemma Mmap_snd (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).2 = -p.1 + l * p.2 := rfl
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl
@[simp] lemma Eform_apply (l : ℝ) (p : ℝ × ℝ) :
    Eform l p = p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2 := rfl

theorem Mmap_preserves_E (l : ℝ) (p : ℝ × ℝ) : Eform l (Mmap l p) = Eform l p := by
  simp only [Eform, Mmap]; ring

/-- The realization constants (l-only). -/
def alphaC (l : ℝ) : ℝ := (l ^ 2 + 2) / (l * (4 - l ^ 2))
def rhoC (l : ℝ) : ℝ := 2 * Real.sqrt (2 * l ^ 2 + 1) / (l * (4 - l ^ 2))

end

/-! ## §1.  General sinusoid-from-2-step-recurrence (PROVED, self-contained).

A real sequence `h : ℕ → ℝ` with `h (k+2) = 2β·h(k+1) − h k` (where `β = cos ω`, `0 ≤ ω`,
i.e. `β = cos ω` from a `ω`) is `h k = A·cos(k ω) + B·sin(k ω)` for `A = h 0` and the unique `B`
with `A cos ω + B sin ω = h 1` (when `sin ω ≠ 0`).  Packaged as the `R·cos(φ + kω)` form. -/

noncomputable section
open Real

/-- A two-step recurrence `h(k+2) = 2 cos ω · h(k+1) − h k` forces the closed form
`h k = h 0 · cos(k ω) + B · sin(k ω)` where `B = (h 1 − h 0 · cos ω)/ sin ω`, provided `sin ω ≠ 0`. -/
theorem recur_closed_form (ω : ℝ) (hs : Real.sin ω ≠ 0) (h : ℕ → ℝ)
    (hrec : ∀ k, h (k + 2) = 2 * Real.cos ω * h (k + 1) - h k) :
    ∀ k, h k = h 0 * Real.cos (k * ω) +
        ((h 1 - h 0 * Real.cos ω) / Real.sin ω) * Real.sin (k * ω) := by
  set B := (h 1 - h 0 * Real.cos ω) / Real.sin ω with hB
  -- the candidate closed form
  set g : ℕ → ℝ := fun k => h 0 * Real.cos (k * ω) + B * Real.sin (k * ω) with hg
  have hg0 : g 0 = h 0 := by simp [hg]
  have hg1 : g 1 = h 1 := by
    simp only [hg, Nat.cast_one, one_mul]
    rw [hB]; field_simp; ring
  -- g satisfies the same recurrence
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
  -- induction: h k = g k for all k
  have key : ∀ k, h k = g k ∧ h (k+1) = g (k+1) := by
    intro k
    induction k with
    | zero => exact ⟨hg0.symm, hg1.symm⟩
    | succ n ih =>
      refine ⟨ih.2, ?_⟩
      rw [hrec n, hgrec n, ih.1, ih.2]
  intro k
  rw [(key k).1, hg]

/-- Packaged `R·cos(φ + kω)` form: any solution of the two-step recurrence with `sin ω ≠ 0`
equals `R cos(φ + kω)` with `R = √(A² + B²)`, `A = h 0`, `B = (h1 − A cos ω)/sin ω`. -/
theorem recur_to_Rcos (ω : ℝ) (hs : Real.sin ω ≠ 0) (h : ℕ → ℝ)
    (hrec : ∀ k, h (k + 2) = 2 * Real.cos ω * h (k + 1) - h k) :
    ∃ R phi : ℝ, 0 ≤ R ∧ (R = 0 ↔ (h 0 = 0 ∧ h 1 = h 0 * Real.cos ω)) ∧
      ∀ k, h k = R * Real.cos (phi + k * ω) := by
  set A := h 0 with hA
  set B := (h 1 - h 0 * Real.cos ω) / Real.sin ω with hBdef
  set R := Real.sqrt (A ^ 2 + B ^ 2) with hRdef
  have hRnn : 0 ≤ R := Real.sqrt_nonneg _
  have hcf := recur_closed_form ω hs h hrec
  -- choose φ with cos φ = A/R, sin φ = -B/R when R>0
  by_cases hR0 : R = 0
  · -- degenerate: A=B=0 ⟹ h ≡ 0
    refine ⟨0, 0, le_refl 0, ?_, ?_⟩
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
    -- build phi via Complex.arg: cos phi = A/R, sin phi = -B/R since (A/R)²+(-B/R)²=1.
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
      -- target: A cos(kω) + B sin(kω) = R(cos ψ cos(kω) - sin ψ sin(kω))
      --                                = R((A/R) cos(kω) - (-B/R) sin(kω)) = A cos + B sin
      field_simp
      ring

end

/-! ## §2.  ★ THE FAITHFUL `pgen_orbit_realization` (orbit identity + E-floor gate). -/

noncomputable section
open Real

/-- Corridor `E`-floor: `Efloor l = 1/(l³ (alpha l + rho l · cos(π/q)))`.  Restated cleanly. -/
def EfloorQ (m : ℕ) (l : ℝ) : ℝ :=
  1 / (l ^ 3 * (alphaC l + rhoC l * Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ))))

/-- **★ THE REALIZATION BRIDGE (FAITHFUL, Form A with E-floor).**
For `q = m+2 ≥ 3`, `l = lamq q`, a corridor point `p ∈ Dcorr l` whose ellipse clears the
`E`-floor (`EfloorQ ≤ Eform l p`), the `Mmap`-orbit observable is the affine sinusoid
`C0 + R·cos(φ + 2kθ)` with `R > 0`, and the threshold gate `(1/l³ − C0)/R ≤ cos θ` holds.

`C0 = alphaC l · E`, `R = rhoC l · E`, `E = Eform l p`, `θ = π/q`.

The orbit identity is UNCONDITIONAL (the `E`-floor is used ONLY for the gate). -/
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
  -- π/q ∈ (0, π/3]
  have hθpos : 0 < θ := by rw [hθ_def]; positivity
  have hθlt : θ < Real.pi := by
    rw [hθ_def, div_lt_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
  -- l = 2 cos θ, with cos θ ∈ (0,1)
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
  -- E > 0 on the corridor
  set E : ℝ := Eform l p with hE_def
  obtain ⟨ha0, ha1, hb0, hb1, hab1, hba1⟩ := hp
  have hEpos : 0 < E := by
    rw [hE_def, Eform]
    -- a² - l a b + b² = (a - (l/2) b)² + ((4-l²)/4) b² > 0  for b>0
    have hb2pos : 0 < p.2 ^ 2 := by positivity
    nlinarith [sq_nonneg (p.1 - (l/2) * p.2), mul_pos h4 hb2pos]
  -- cos(2θ) = l²/2 - 1
  have hcos2 : Real.cos (2 * θ) = l ^ 2 / 2 - 1 := by
    rw [Real.cos_two_mul, hcosθ]; ring
  -- sin(2θ) > 0  since 0 < 2θ < π (q ≥ 3 ⟹ 2θ = 2π/q ≤ 2π/3 < π)
  have h2θpos : 0 < 2 * θ := by linarith
  have h2θlt : 2 * θ < Real.pi := by
    rw [hθ_def]; rw [show (2:ℝ) * (Real.pi / q) = 2 * Real.pi / q by ring, div_lt_iff₀ hqr]
    nlinarith [Real.pi_pos, hqr3]
  have hsin2pos : 0 < Real.sin (2 * θ) := Real.sin_pos_of_pos_of_lt_pi h2θpos h2θlt
  have hsin2ne : Real.sin (2 * θ) ≠ 0 := ne_of_gt hsin2pos
  -- C0 = αE
  set C0 : ℝ := alphaC l * E with hC0_def
  -- the orbit-offset sequence
  set hseq : ℕ → ℝ := fun k => Pgen l ((Mmap l)^[k] p) - C0 with hseq_def
  -- E is preserved along the orbit
  have hEorb : ∀ k, Eform l ((Mmap l)^[k] p) = E := by
    intro k
    induction k with
    | zero => simp [hE_def]
    | succ n ih => rw [Function.iterate_succ_apply', Mmap_preserves_E, ih]
  -- the recurrence  hseq(k+2) = 2 cos(2θ) hseq(k+1) - hseq k
  have hrec : ∀ k, hseq (k + 2) = 2 * Real.cos (2 * θ) * hseq (k + 1) - hseq k := by
    intro k
    rw [hcos2]
    simp only [hseq_def]
    -- write the (k+1),(k+2) iterates as Mmap applied to the k-th iterate
    set x := (Mmap l)^[k] p with hx_def
    have e1 : (Mmap l)^[k+1] p = Mmap l x := by rw [hx_def, Function.iterate_succ_apply']
    have e2 : (Mmap l)^[k+2] p = Mmap l (Mmap l x) := by
      rw [hx_def, show k + 2 = (k+1)+1 by ring, Function.iterate_succ_apply',
          Function.iterate_succ_apply']
    rw [e1, e2]
    -- C0 = αE = α·Eform l x  (since Eform preserved)
    have hCx : C0 = alphaC l * Eform l x := by rw [hC0_def, ← hEorb k, hx_def]
    rw [hCx]
    simp only [Mmap, Pgen, Eform, alphaC]
    field_simp
    ring
  -- get the cos form from recur_to_Rcos
  obtain ⟨R, phi, hRnn, hRiff, hform⟩ := recur_to_Rcos (2 * θ) hsin2ne hseq hrec
  -- amplitude invariant ⟹ R = rhoC l * E
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
  -- but also  hseq0²-2cos2 h0 h1+h1² = R² sin²(2θ)  by the cos form
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
  -- assemble: orbit identity with phase  phi + k·(2θ),  i.e.  phi + 2kθ
  refine ⟨C0, R, phi, hRpos, ?_, ?_⟩
  · intro k
    rw [show Pgen l ((Mmap l)^[k] p) = hseq k + C0 by rw [hseq_def]; ring]
    rw [hform k]
    -- match phase:  phi + k·(2θ)  =  phi + 2·k·(π/q)
    have hphase : phi + (k:ℝ) * (2*θ) = phi + 2 * (k:ℝ) * (Real.pi / ((m+2:ℕ):ℝ)) := by
      rw [hθ_def, hq_def]; ring
    rw [hphase]; ring
  · -- gate: (1/l³ − C0)/R ≤ cos θ.  With C0=αE, R=ρE, equivalent to E ≥ Efloor.
    rw [hReq, hC0_def, hcosθ]
    rw [div_le_iff₀ (mul_pos hrhopos hEpos)]
    -- 1/l³ − αE ≤ (l/2)·ρE   ⟺   1/l³ ≤ E(α + ρ·l/2) = E(α + ρ cos θ)
    -- and  E ≥ Efloor = 1/(l³(α+ρ cos θ))  gives exactly this.
    have hgate_pos : 0 < alphaC l + rhoC l * (l/2) := by
      have hαpos : 0 < alphaC l := by
        rw [alphaC]; apply div_pos (by nlinarith [hl_pos]) (mul_pos hl_pos h4)
      have : 0 < rhoC l * (l/2) := mul_pos hrhopos (by linarith [hl_pos])
      linarith
    have hl3 : 0 < l ^ 3 := by positivity
    -- Efloor (with cos(π/q) = l/2)
    have hEfloor_eq : EfloorQ m l = 1 / (l^3 * (alphaC l + rhoC l * (l/2))) := by
      rw [EfloorQ]
      have hcc : Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ)) = l / 2 := hcosθ
      rw [hcc]
    rw [hEfloor_eq] at hE
    -- from E ≥ 1/(l³ g) (g>0,l³>0)  ⟹  1/l³ ≤ E·g
    have key : 1 / l ^ 3 ≤ E * (alphaC l + rhoC l * (l/2)) := by
      have hd : 0 < l ^ 3 * (alphaC l + rhoC l * (l/2)) := mul_pos hl3 hgate_pos
      rw [div_le_iff₀ hd] at hE
      -- hE : 1 ≤ E * (l³ g)
      rw [div_le_iff₀ hl3]
      nlinarith [hE, hEpos, hgate_pos, hl3]
    nlinarith [key, hEpos]

end
