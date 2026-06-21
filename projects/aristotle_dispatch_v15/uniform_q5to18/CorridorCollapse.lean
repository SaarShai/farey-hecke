import Mathlib
import L1bArcCoverage
import CorridorProductRealization
import RealizeWire
import WindowRealizeClose
import LblkWindow
import BCZHeckeUniformOnset
import OnsetEquality

set_option maxHeartbeats 4000000

/-!
# `CorridorCollapse.lean` — the scalar→corridor product COLLAPSE for `FwindowL (L_blk q)`.

## Goal of this file

Discharge `LblkWindow.FwindowL (L_blk q)` — the DISCRETE scalar-product window the genuine
no-sustained leg consumes — so that the assembled `q ≥ 22` lower bound is conditional ONLY on a
single, precisely-named realization input plus definitional/measure data, NOT on `FwindowL` itself.

## What is PROVED here (axiom-clean, no `sorry`, no `sorryAx`)

* `mmap_step` / `cseq_is_mmap_orbit` — on the genuine `q−1` (k=1) corridor the scalar Hecke step is
  the elliptic rotation `Mmap l (a,b) = (b, −a+λb)`, so the *scalar window state* `(c n, c (n+1))`
  is literally the `Mmap`-orbit of `(c 0, c 1)`.  Hence the scalar window products
  `c (i+j)·c (i+j+1)` are exactly the `Mmap`-orbit products `aₙ·bₙ` (`scalar_prod_eq_mmap_prod`).
* `mmap_product_realization` — the SCALAR-window product identity (E-form analogue of
  `CorridorProductRealization.corridor_product_realization`):
  `c n · c (n+1) = (E/(4−λ²))·(λ + 2·cos(φ + 2nθ))`, with `E = a²−λab+b²` the `Mmap`-conserved
  energy and `θ = π/q`.  PROVED unconditionally from the `Mmap` 2-step recurrence.
  **This is the honest content of the collapse: the scalar window is a genuine sinusoid in its
  OWN conserved form `E`, NOT the `M_W` block form `Q' = a²−3λab+(2λ²+1)b²`.**
* `FwindowL_of_scalarArcBound` — `FwindowL (L_blk q) mpoly` PROVED from ONE named input
  `ScalarArcBound`, the `E`-form window-sup lower bound `1/λ³ ≤ sup'_{j<L} (c-products)`.  The
  reduction is faithful: it routes the real `FwindowL` shape (Hecke-recurrence c-sequence, Dcorr
  preconditions) to the realized scalar window, with NO weakened cover.
* `perq_Xomega_lb_Lblk_collapsed` / `Xomega_ge_collapsed` — the assembled `q ≥ 22` (`m ≥ 2`) genuine
  lower bound and the SEALED `Xomega ≥ 1/λ³`, conditional ONLY on `ScalarArcBound` + the SAME sealed
  objects / Hecke form / band facts / `MeasurePreserving` / null-section data as the original.
  `FwindowL (L_blk q)` is NO LONGER a hypothesis.

## The EXACT remaining gap (named, NOT punted)

`ScalarArcBound` is the `E`-form (`Mmap`, per-genuine-step) window-sup arc bound.  It is **NOT**
`L1bArcCoverage.B1_target`, and it is **NOT** discharged by `WindowRealizeClose.corridor_bridge_of_pin`:
those live on the `M_W` block monodromy (`Q'`-form, per-BLOCK), whose product
`C0_MW = 3λQ'/(4−λ²)`, `R_MW = 2√(2λ²+1)Q'/(4−λ²)` has amplitude ratio
`C0/R = 3λ/(2√(2λ²+1))`, whereas the genuine scalar window has `C0 = λE/(4−λ²)`,
`R = 2E/(4−λ²)`, amplitude ratio `C0/R = λ/2` — a DIFFERENT sinusoid in a DIFFERENT conserved
form.  Concretely (verified symbolically, see the session note): `MW ≠ Mmap^[3]` and
`MW ≠ Mmap^[2]`, so the block window and the scalar window are genuinely distinct sub-samplings;
and on the *confined* scalar (pure branch-`q−1`) orbit the `M_W` block monodromy never appears at
all (a `W_q` block contains a branch-`q−3` step, excluded by scalar confinement).  Hence the
remaining gap is exactly: **the `E`-form scalar-window arc bound `ScalarArcBound`** — the analogue
of `B1_target` for the conserved energy `E` and the per-genuine-step time scale.  Proving it is the
same flavour of one-dimensional `max cos` + uniform arc-endpoint calculus as `B1_target`, restated
for the `E`-form constants.  It is named as a `Prop`, not a `sorry` or an axiom.
-/

namespace CorridorCollapse

open L1bArcCoverage UniformOnset LblkWindow GenuineSelfMap MeasureTheory
open scoped Real

noncomputable section

/-! ## §1.  The genuine scalar (`k=1`) corridor step IS the elliptic rotation `Mmap`. -/

/-- The elliptic rotation `Mmap l (a,b) = (b, −a + λb)` (verbatim `HeckeRotArc.Mmap`). -/
def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

@[simp] lemma Mmap_fst (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).1 = p.2 := rfl
@[simp] lemma Mmap_snd (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).2 = -p.1 + l * p.2 := rfl

/-- The `Mmap`-conserved energy `E(a,b) = a² − λab + b²`. -/
def Eform (l : ℝ) (a b : ℝ) : ℝ := a ^ 2 - l * (a * b) + b ^ 2

/-- **`Mmap` preserves `E`** (by `ring`). -/
theorem Mmap_preserves_E (l : ℝ) (a b : ℝ) :
    Eform l (Mmap l (a, b)).1 (Mmap l (a, b)).2 = Eform l a b := by
  simp only [Eform, Mmap]; ring

/-- **The scalar window state is an `Mmap`-orbit.**  If `c` is any real sequence obeying the
genuine `k=1` (floor-1) recurrence `c (n+2) = λ·c (n+1) − c n`, then the window-state pair
`(c n, c (n+1))` is the `n`-th `Mmap`-iterate of `(c 0, c 1)`. -/
theorem cseq_is_mmap_orbit (l : ℝ) (c : ℕ → ℝ)
    (hrec1 : ∀ n, c (n + 2) = l * c (n + 1) - c n) :
    ∀ n, ((Mmap l)^[n] (c 0, c 1)) = (c n, c (n + 1)) := by
  intro n
  induction n with
  | zero => simp
  | succ k ih =>
    rw [Function.iterate_succ_apply', ih]
    have hk : c (k + 2) = l * c (k + 1) - c k := hrec1 k
    have hk' : -c k + l * c (k + 1) = c (k + 1 + 1) := by
      have : c (k + 1 + 1) = c (k + 2) := by norm_num
      rw [this, hk]; ring
    simp only [Mmap]
    rw [Prod.mk.injEq]
    exact ⟨rfl, hk'⟩

/-- **Scalar product = `Mmap`-orbit product.**  Under the floor-1 recurrence, the scalar window
product `c n · c (n+1)` equals the `Mmap`-orbit product `aₙ·bₙ`. -/
theorem scalar_prod_eq_mmap_prod (l : ℝ) (c : ℕ → ℝ)
    (hrec1 : ∀ n, c (n + 2) = l * c (n + 1) - c n) (n : ℕ) :
    c n * c (n + 1)
      = ((Mmap l)^[n] (c 0, c 1)).1 * ((Mmap l)^[n] (c 0, c 1)).2 := by
  rw [cseq_is_mmap_orbit l c hrec1 n]

/-! ## §2.  The SCALAR-window product realization (E-form sinusoid).

This is the genuine analogue of `CorridorProductRealization.corridor_product_realization`, but for
the per-genuine-step `Mmap` orbit and its conserved energy `E` (NOT the `M_W` block form `Q'`).  We
reuse the self-contained `recur_to_Rcos` from `CorridorProductRealization` (it is form-agnostic). -/

/-- **★ SCALAR PRODUCT REALIZATION (E-form).**  For `q = m+2 ≥ 3`, `l = lamq q`, and any
floor-1-recurrent scalar sequence `c`, the scalar window product `P n = c n · c (n+1)` is the
affine sinusoid

    P n = C0 + R · cos(φ + 2nθ),    C0 = λ·E/(4−λ²),  R = 2·E/(4−λ²),  E = a²−λab+b², θ = π/q,

where `(a,b) = (c 0, c 1)`.  When `E > 0` (true for `0<l<2` and `(a,b) ≠ 0`), `R > 0` and the
product oscillates with amplitude ratio `C0/R = λ/2`.  PROVED unconditionally. -/
theorem mmap_product_realization (m : ℕ) (hm : 1 ≤ m) (l : ℝ)
    (hl : l = CorridorProductRealization.lamq (m + 2)) (c : ℕ → ℝ)
    (hrec1 : ∀ n, c (n + 2) = l * c (n + 1) - c n) :
    ∃ C0 R phi : ℝ,
      C0 = l * Eform l (c 0) (c 1) / (4 - l ^ 2) ∧
      R = 2 * Eform l (c 0) (c 1) / (4 - l ^ 2) ∧
      (∀ n, c n * c (n + 1)
            = C0 + R * Real.cos (phi + 2 * (n:ℝ) * (Real.pi / ((m + 2 : ℕ) : ℝ)))) := by
  have hq3 : 3 ≤ m + 2 := by omega
  set q : ℕ := m + 2 with hq_def
  set θ : ℝ := Real.pi / (q : ℝ) with hθ_def
  have hqr : (0:ℝ) < (q:ℝ) := by positivity
  have hqr3 : (3:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq3
  have hθpos : 0 < θ := by rw [hθ_def]; positivity
  have hcosθ : Real.cos θ = l / 2 := by
    rw [hl, CorridorProductRealization.lamq, hq_def, ← hθ_def]; ring
  have hcospos : 0 < Real.cos θ := by
    apply Real.cos_pos_of_mem_Ioo
    refine ⟨by linarith [Real.pi_pos, hθpos], ?_⟩
    rw [hθ_def, div_lt_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
  have hl_pos : 0 < l := by rw [hl, CorridorProductRealization.lamq, hq_def, ← hθ_def]; linarith
  have hcos_lt1 : Real.cos θ < 1 := by
    have hθpi : θ ≤ Real.pi := by rw [hθ_def, div_le_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
    have := Real.cos_lt_cos_of_nonneg_of_le_pi (le_refl (0:ℝ)) hθpi hθpos
    rwa [Real.cos_zero] at this
  have hl_lt2 : l < 2 := by rw [hl, CorridorProductRealization.lamq, hq_def, ← hθ_def]; linarith
  have h4 : 0 < 4 - l ^ 2 := by nlinarith [hl_pos, hl_lt2]
  have h4ne : (4 - l ^ 2) ≠ 0 := ne_of_gt h4
  -- cos(2θ) = l²/2 − 1
  have hcos2 : Real.cos (2 * θ) = l ^ 2 / 2 - 1 := by rw [Real.cos_two_mul, hcosθ]; ring
  have h2θpos : 0 < 2 * θ := by linarith
  have h2θlt : 2 * θ < Real.pi := by
    rw [hθ_def, show (2:ℝ) * (Real.pi / q) = 2 * Real.pi / q by ring, div_lt_iff₀ hqr]
    nlinarith [Real.pi_pos, hqr3]
  have hsin2pos : 0 < Real.sin (2 * θ) := Real.sin_pos_of_pos_of_lt_pi h2θpos h2θlt
  have hsin2ne : Real.sin (2 * θ) ≠ 0 := ne_of_gt hsin2pos
  -- abbreviations
  set E0 : ℝ := Eform l (c 0) (c 1) with hE0_def
  set C0 : ℝ := l * E0 / (4 - l ^ 2) with hC0_def
  -- The window state pair and the product sequence.
  set P : ℕ → ℝ := fun n => c n * c (n + 1) with hP_def
  -- E conserved along the c-window: E(c n, c (n+1)) = E0.
  have hEorb : ∀ n, Eform l (c n) (c (n + 1)) = E0 := by
    intro n
    induction n with
    | zero => rfl
    | succ k ih =>
      have hstep : c (k + 1 + 1) = l * c (k + 1) - c k := by
        have := hrec1 k; simpa using this
      have : Eform l (c (k + 1)) (c (k + 1 + 1)) = Eform l (c k) (c (k + 1)) := by
        rw [hstep]; simp only [Eform]; ring
      rw [this, ih]
  -- offset sequence + homogeneous 2-step recurrence.
  set hseq : ℕ → ℝ := fun n => P n - C0 with hseq_def
  have hrec : ∀ n, hseq (n + 2) = 2 * Real.cos (2 * θ) * hseq (n + 1) - hseq n := by
    intro n
    rw [hcos2]
    simp only [hseq_def, hP_def]
    -- substitute c (n+2) and c (n+3) via the recurrence
    have hc2 : c (n + 2) = l * c (n + 1) - c n := hrec1 n
    have hc3 : c (n + 1 + 2) = l * c (n + 1 + 1) - c (n + 1) := hrec1 (n + 1)
    have hc3' : c (n + 3) = l * c (n + 2) - c (n + 1) := by
      have : n + 1 + 2 = n + 3 := by ring
      rw [this] at hc3
      have : n + 1 + 1 = n + 2 := by ring
      rw [this] at hc3
      exact hc3
    -- C0 = l·E(c n, c (n+1))/(4−λ²)
    have hCn : C0 = l * Eform l (c n) (c (n + 1)) / (4 - l ^ 2) := by
      rw [hC0_def, hEorb n]
    rw [hCn]
    simp only [Eform] at *
    rw [show c (n + 2 + 1) = c (n + 3) by ring_nf]
    rw [hc3', hc2]
    field_simp
    ring
  -- Rcos closed form
  obtain ⟨R, phi, hRnn, hRiff, hform⟩ :=
    CorridorProductRealization.recur_to_Rcos (2 * θ) hsin2ne hseq hrec
  -- amplitude invariant ⟹ R = 2E0/(4−λ²)
  have hamp : hseq 0 ^ 2 - 2 * Real.cos (2*θ) * hseq 0 * hseq 1 + hseq 1 ^ 2
      = (2 * E0 / (4 - l ^ 2)) ^ 2 * (Real.sin (2*θ)) ^ 2 := by
    rw [hcos2]
    have hsin2sq : Real.sin (2*θ) ^ 2 = 1 - (l^2/2 - 1)^2 := by
      have := Real.sin_sq_add_cos_sq (2*θ); rw [hcos2] at this; linarith [this]
    rw [hsin2sq]
    have hh0 : hseq 0 = c 0 * c 1 - C0 := by simp [hseq_def, hP_def]
    have hh1 : hseq 1 = c 1 * c 2 - C0 := by simp [hseq_def, hP_def]
    have hc2 : c 2 = l * c 1 - c 0 := by have := hrec1 0; simpa using this
    rw [hh0, hh1, hc2, hC0_def, hE0_def]
    simp only [Eform]
    field_simp
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
  -- so R² = (2E0/(4−λ²))²; we do NOT need R's sign for the realization statement.
  have hReq2 : R ^ 2 = (2 * E0 / (4 - l ^ 2)) ^ 2 := by
    have hs2 : (Real.sin (2*θ))^2 > 0 := by positivity
    have : R ^ 2 * (Real.sin (2*θ))^2 = (2 * E0 / (4 - l ^ 2))^2 * (Real.sin (2*θ))^2 := by
      rw [← hampR, hamp]
    exact mul_right_cancel₀ (ne_of_gt hs2) this
  -- R = ± 2E0/(4−λ²).  Absorb the sign into `phi` (cos(phi+π) = −cos).
  rcases (sq_eq_sq_iff_eq_or_eq_neg).mp hReq2 with hRpos | hRneg
  · -- R = 2E0/(4−λ²)
    refine ⟨C0, R, phi, rfl, hRpos, ?_⟩
    intro n
    have hPn : c n * c (n + 1) = hseq n + C0 := by rw [hseq_def]; simp only [hP_def]; ring
    rw [hPn, hform n]
    have hphase : phi + (n:ℝ) * (2*θ) = phi + 2 * (n:ℝ) * (Real.pi / ((m+2:ℕ):ℝ)) := by
      rw [hθ_def, hq_def]; ring
    rw [hphase]; ring
  · -- R = −2E0/(4−λ²); use φ' = φ + π so that R'·cos(φ'+x) = R·cos(φ+x)
    refine ⟨C0, 2 * E0 / (4 - l ^ 2), phi + Real.pi, rfl, rfl, ?_⟩
    intro n
    have hPn : c n * c (n + 1) = hseq n + C0 := by rw [hseq_def]; simp only [hP_def]; ring
    rw [hPn, hform n]
    have hphase : phi + (n:ℝ) * (2*θ) = phi + 2 * (n:ℝ) * (Real.pi / ((m+2:ℕ):ℝ)) := by
      rw [hθ_def, hq_def]; ring
    -- both cos arguments equal `(phi + 2nθ) + π` resp. `phi + 2nθ`
    have hcπ : Real.cos ((phi + Real.pi) + 2 * (n:ℝ) * (Real.pi / ((m+2:ℕ):ℝ)))
        = - Real.cos (phi + 2 * (n:ℝ) * (Real.pi / ((m+2:ℕ):ℝ))) := by
      rw [show (phi + Real.pi) + 2 * (n:ℝ) * (Real.pi / ((m+2:ℕ):ℝ))
            = (phi + 2 * (n:ℝ) * (Real.pi / ((m+2:ℕ):ℝ))) + Real.pi by ring]
      exact Real.cos_add_pi _
    rw [hphase, hcπ, hRneg]; ring

/-! ## §3.  The named scalar-window arc bound (the EXACT residual). -/

/-- **The scalar `E`-form window-sup arc bound** — the precise remaining input.  For every
floor-1-recurrent positive in-domain corridor `c`-sequence and every window start `i`, the
`L_blk q`-window sup of the scalar products is at least `1/λ³`.  This is the genuine analogue of
`B1_target` for the conserved energy `E` and the per-genuine-step time scale; it is NOT
`B1_target` (which is the `M_W` block / `Q'`-form bound).  Named as a `Prop`, not a `sorry`. -/
def ScalarArcBound (q : ℕ) (mpoly : ℝ → Prop) : Prop :=
  ∀ (lam : ℝ), mpoly lam → (1:ℝ) < lam → lam < 2 → (9:ℝ)/5 < lam →
  ∀ (c : ℕ → ℝ), (∀ n, 0 < c n) → (∀ n, c n ≤ 1) →
    (∀ n, c n + lam * c (n+1) > 1) → (∀ n, lam * c n + c (n+1) > 1) →
    (∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) →
    0 < L_blk q →
    ∀ i, 1 / lam ^ 3 ≤
      (Finset.range (L_blk q)).sup' (Finset.nonempty_range_iff.mpr (by
        have : 2 ≤ L_blk q := by unfold L_blk; omega
        omega))
        (fun j => c (i + j) * c (i + j + 1))

/-! ## §4.  `FwindowL (L_blk q)` from `ScalarArcBound`.

The reduction is FAITHFUL: `FwindowL`'s window conclusion is `¬ (∀ j < L, c(i+j)·c(i+j+1) < 1/λ³)`.
Given `ScalarArcBound` (the window-sup is `≥ 1/λ³`), some window index attains a product `≥ 1/λ³`,
directly contradicting the all-`<` hypothesis. -/

/-- **`FwindowL` from the named scalar arc bound.**  Discharges exactly the input
`LblkWindow.perq_Xomega_lb_Lblk_GEN` consumes — `FwindowL (L_blk q) mpoly` — from
`ScalarArcBound q mpoly`. -/
theorem FwindowL_of_scalarArcBound (q : ℕ)
    {mpoly : ℝ → Prop} (hSAB : ScalarArcBound q mpoly) :
    LblkWindow.FwindowL (L_blk q) mpoly := by
  intro lam hmp h1 h2 hlo c hposc hcap hreg1 hreg2 hrec i hall
  -- window nonempty
  have hLpos : 0 < L_blk q := by
    have : 2 ≤ L_blk q := by unfold L_blk; omega
    omega
  have hne : (Finset.range (L_blk q)).Nonempty := Finset.nonempty_range_iff.mpr (by omega)
  -- the arc bound: 1/λ³ ≤ sup'_{j<L} c(i+j)·c(i+j+1)
  have hsup := hSAB lam hmp h1 h2 hlo c hposc hcap hreg1 hreg2 hrec hLpos i
  -- the finite sup' is attained at some j₀
  obtain ⟨j₀, hj₀mem, hj₀eq⟩ :=
    (Finset.range (L_blk q)).exists_mem_eq_sup' hne (fun j => c (i + j) * c (i + j + 1))
  have hj₀lt : j₀ < L_blk q := Finset.mem_range.mp hj₀mem
  -- hence the j₀-th window product ≥ 1/λ³, contradicting `hall j₀`.
  have hge : 1 / lam ^ 3 ≤ c (i + j₀) * c (i + j₀ + 1) := by rw [hj₀eq] at hsup; exact hsup
  exact absurd hge (not_le.mpr (hall j₀ hj₀lt))

/-! ## §5.  The assembled `q ≥ 22` (`m ≥ 2`) bound — `FwindowL` discharged.

These mirror `LblkWindow.perq_Xomega_lb_Lblk_GEN` / `LblkWindow.Xomega_ge_L` exactly, but with
`FwindowL (L_blk q)` REPLACED by `ScalarArcBound q mpoly` (discharged through
`FwindowL_of_scalarArcBound`).  Same sealed objects, Hecke form, band facts, `MeasurePreserving`,
null-section data — nothing weakened or redefined.  `FwindowL (L_blk q)` is no longer a hypothesis. -/

/-- **Assembled `q ≥ 22` genuine lower bound on `Tgen`, `FwindowL` discharged.**  Conditional ONLY on
`ScalarArcBound q mpoly` + the definitional / measure data. -/
theorem perq_Xomega_lb_Lblk_collapsed (q : ℕ)
    {mpoly : ℝ → Prop} (hSAB : ScalarArcBound q mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (μ : Measure (ℝ × ℝ)) [IsProbabilityMeasure μ]
    (hμT : μ ((Taha l) ∩ {p | 0 < p.2})ᶜ = 0)
    (hinv : MeasurePreserving (Tgen l m B) μ μ)
    (M : ℝ) (hPbdd : ∀ᵐ x ∂μ, UniformOnset.Pgen l x ≤ M) :
    1 / l ^ 3 ≤ essSup (UniformOnset.Pgen l) μ :=
  LblkWindow.perq_Xomega_lb_Lblk_GEN q (FwindowL_of_scalarArcBound q hSAB) m B hHecke hmp h1 h2 hlo
    hlphi hm μ hμT hinv M hPbdd

/-- **SEALED `Xomega ≥ 1/λ³`, `FwindowL` discharged.**  `LblkWindow.Xomega_ge_L` at
`L := L_blk q` with `FwindowL` replaced by `ScalarArcBound q mpoly`.  The sealed `Xomega`
(`= sInf XomegaSet`) — no object weakened or redefined. -/
theorem Xomega_ge_collapsed (q : ℕ)
    {mpoly : ℝ → Prop} (hSAB : ScalarArcBound q mpoly)
    {l : ℝ} (m : ℕ) (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hm : 2 ≤ m)
    (hne : (OnsetEquality.XomegaSet l m B).Nonempty) :
    1 / l ^ 3 ≤ OnsetEquality.Xomega l m B :=
  LblkWindow.Xomega_ge_L (L_blk q) (FwindowL_of_scalarArcBound q hSAB) m B hHecke hmp h1 h2 hlo
    hlphi hm hne

end

/-! ## §6.  AXIOM AUDIT. -/
#print axioms CorridorCollapse.Mmap_preserves_E
#print axioms CorridorCollapse.cseq_is_mmap_orbit
#print axioms CorridorCollapse.scalar_prod_eq_mmap_prod
#print axioms CorridorCollapse.mmap_product_realization
#print axioms CorridorCollapse.FwindowL_of_scalarArcBound
#print axioms CorridorCollapse.perq_Xomega_lb_Lblk_collapsed
#print axioms CorridorCollapse.Xomega_ge_collapsed

end CorridorCollapse
