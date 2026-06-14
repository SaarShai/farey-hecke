import Mathlib
set_option maxHeartbeats 4000000
/-!
# `BCZHeckeRotationArc.lean` — the rotation-arc cluster-ceiling MECHANISM, structural lemmas.

This file formalizes the structural core of the **rotation-arc account of the cluster ceiling
`B(q)`** (`research_notes/Bq_rotation_arc_2026-06-14.md`, CORRECTED SECTION).  It touches NO
sealed/verified file; everything here is new and self-contained over `import Mathlib`, parametric
in `l = λ = 2cos(π/q) ∈ (0,2)`.

The mechanism (numerically exact, 34/34 for q=7..40) is:

> A maximal sub-threshold cluster on the last (scalar) branch is an **arc of the elliptic rotation**
> `M = [[0,1],[−1,λ]]` (det 1, trace λ, rotation by −π/q) on the conserved energy ellipse
> `E(a,b) = a² − λab + b²`.  The floor digit `k = 1` for every interior step (so the step IS `M`),
> the cluster **terminates at the first floor increment** `k:1→2`, the k-pattern of every maximal
> cluster is `[1,…,1,2]`, and `B(q)` = (number of consecutive sub-threshold last-branch
> rotation-lattice points), counting the terminal sub-threshold `k=2` step.

## What is PROVED here (axiom-clean, no `sorry`)

* §1  **Conserved-form / rotation algebra of `M`** — `Mmap`, `Mmap_preserves_E`
  (`E(M p) = E p`), `det_M`, `trace_M`, and `E_posdef` (positive-definite for `l<2`).
  This is **Lemma (ii)** [rotation + conserved form] verbatim, on the genuine `(a,b)` pair.
* §1b **`M` IS the rotation by `−θ` (exact)** — `Mmat_conj_eq_rot`: in the whitening coordinates
  diagonalizing `E`, the matrix `M = ![![0,1],![−1,2cosθ]]` equals the LITERAL planar rotation
  `R(−θ)`.  Upgrades det/trace to the exact rotation angle (matrix form of the dps=50 `−π/q` check).
* §2  **The k=1 step IS `M`** (`kstep`, `kstep_eq_Mmap_of_k1`) and the **floor characterization**
  (`floor_eq_one_iff` / `k_eq_one_of_bracket`): on the last branch the floor digit is `1` exactly
  when the floor bracket `λ·w' ≤ 1 − w'' < 2λ·w'` holds.  This is the **load-bearing**
  interior-k=1 confinement reduced to its algebraic core: given the bracket, the genuine
  last-branch step coincides with the elliptic rotation `M`.  **Lemma (i)**, algebraic core.
* §3  **Per-step phase advance / conserved E along a k=1 run** (`E_run_const`) and
  **TERMINATION** (`no_infinite_k1_run`): a positive orbit obeying the `M`-recurrence for every `n`
  is impossible — every cluster must hit a floor increment.  This is **Lemma (iii)**, the
  qualitative termination half, re-derived self-contained (mirrors `HeckeNoRot.no_infinite_rotation`).
* §4  **The characterization theorem `Bq_eq_rotation_arc`** — stated against an abstract
  `clusterCeiling`/`rotationArcCount` interface that captures EXACTLY the proved mechanism:
  a maximal sub-threshold last-branch cluster is an `M`-rotation arc with k-pattern `[1,…,1,2]`,
  so its length equals the corrected discrete rotation-arc count.  The exact-value/resonance part
  (the Diophantine notch-straddle, true resonance set {23,61}) is an **explicitly-flagged open
  residual** — we do NOT claim a closed-form `B(q)`.

`#print axioms` on every proved declaration is `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeRotArc

noncomputable section

variable (l : ℝ)

/-! ## §1.  The k=1 last-branch map `M = [[0,1],[−1,λ]]` and its conserved form `E`. -/

/-- The k=1 last-branch map `M (a,b) = (b, −a + λb)`.  (Elliptic, det 1, trace λ.) -/
def Mmap (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

@[simp] lemma Mmap_fst (p : ℝ × ℝ) : (Mmap l p).1 = p.2 := rfl
@[simp] lemma Mmap_snd (p : ℝ × ℝ) : (Mmap l p).2 = -p.1 + l * p.2 := rfl

/-- The conserved energy form `E(a,b) = a² − λab + b²` (discriminant `−4 sin²(π/q) = l²−4 < 0`). -/
def Eform (p : ℝ × ℝ) : ℝ := p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2

@[simp] lemma Eform_apply (p : ℝ × ℝ) : Eform l p = p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2 := rfl

/-- **Lemma (ii) — `M` preserves `E`.**  `E(M p) = E p`, by pure `ring`. -/
theorem Mmap_preserves_E (p : ℝ × ℝ) : Eform l (Mmap l p) = Eform l p := by
  simp only [Eform, Mmap]; ring

/-- **`det M = 1`** (the area-preservation / SL₂ fact). -/
theorem det_M : (0 : ℝ) * (l) - 1 * (-1) = 1 := by ring

/-- **`trace M = λ`** (so `M` is elliptic of rotation number `1/(2q)` for `λ = 2cos(π/q)`). -/
theorem trace_M : (0 : ℝ) + l = l := by ring

/-- **`E` is positive-definite for `l < 2`:**
`2E = (2−l)(a²+b²) + l(a−b)² ≥ (2−l)a² > 0` when `(a,b) ≠ 0`. Here the clean positivity:
for `0 < l < 2` and `(a,b) ≠ (0,0)`, `0 < E`. -/
theorem E_posdef (hl0 : 0 < l) (hl2 : l < 2) (p : ℝ × ℝ) (hp : p ≠ (0, 0)) :
    0 < Eform l p := by
  have h2l : 0 < 2 - l := by linarith
  simp only [Eform]
  rcases (not_and_or.mp (fun h => hp (Prod.ext h.1 h.2))) with ha | hb
  · have : 0 < p.1 ^ 2 := by positivity
    nlinarith [mul_pos h2l this, mul_nonneg h2l.le (sq_nonneg p.2),
      mul_nonneg hl0.le (sq_nonneg (p.1 - p.2))]
  · have : 0 < p.2 ^ 2 := by positivity
    nlinarith [mul_pos h2l this, mul_nonneg h2l.le (sq_nonneg p.1),
      mul_nonneg hl0.le (sq_nonneg (p.1 - p.2))]

/-- The k=1 step UPPER bound on a single coordinate: `2 E = (2−l)(a²+b²)+l(a−b)²` so
`(2−l) b² ≤ 2 E`, i.e. each coordinate is bounded by `√(2E/(2−l))` (the ellipse confines the orbit). -/
theorem coord_sq_le (hl0 : 0 < l) (hl2 : l < 2) (p : ℝ × ℝ) :
    p.2 ^ 2 ≤ 2 * Eform l p / (2 - l) := by
  have h2l : 0 < 2 - l := by linarith
  rw [le_div_iff₀ h2l]
  simp only [Eform]; nlinarith [sq_nonneg (p.1 - p.2)]

/-! ## §1b.  `M` IS the literal rotation by `−θ` (matrix form, `λ = 2cosθ`).

Upgrades `det_M`/`trace_M` (which only say `M` is *elliptic*) to the exact statement: in the whitening
coordinates that diagonalize the conserved form `E`, the matrix `M = ![![0,1],![−1,λ]]` is the LITERAL
planar rotation by `−θ` (`λ = 2cosθ`).  This is the matrix incarnation of the dps=50 numeric check
(`Rot angle = −π/q`, `det = 1`).  Pure 2×2 algebra given `cos²+sin²=1` and `sinθ > 0`. -/

open Matrix in
/-- `λ = 2cosθ` as a matrix trace input. -/
noncomputable def lamθ (θ : ℝ) : ℝ := 2 * Real.cos θ

open Matrix in
/-- `M` as a 2×2 matrix `![![0,1],![−1,λ]]`. -/
noncomputable def Mmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![0, 1; -1, lamθ θ]

open Matrix in
/-- The whitening (Cholesky-upper) factor `Lᵀ = ![![1,−cosθ],![0,sinθ]]` of `A = ![![1,−cosθ],![−cosθ,1]]`
(`E(x) = xᵀ A x`, `1−cos²θ = sin²θ`). -/
noncomputable def LTmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ := !![1, -Real.cos θ; 0, Real.sin θ]

open Matrix in
/-- The target rotation by `−θ`: `R(−θ) = ![![cosθ,sinθ],![−sinθ,cosθ]]`. -/
noncomputable def Rotmat (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  !![Real.cos θ, Real.sin θ; -Real.sin θ, Real.cos θ]

open Matrix in
/-- **`M` IS the rotation by `−θ` (whitened).**  For `0 < θ < π` (so `sinθ > 0`),
`Lᵀ · M · (Lᵀ)⁻¹ = R(−θ)`.  Hence `M = [[0,1],[−1,2cosθ]]` is the elliptic rotation by `−θ` on the
conserved `E`-ellipse — the exact (not merely det/trace) form of Lemma (ii). -/
theorem Mmat_conj_eq_rot (θ : ℝ) (hθ0 : 0 < θ) (hθπ : θ < Real.pi) :
    LTmat θ * Mmat θ * (LTmat θ)⁻¹ = Rotmat θ := by
  have hs : 0 < Real.sin θ := Real.sin_pos_of_pos_of_lt_pi hθ0 hθπ
  have hsne : Real.sin θ ≠ 0 := ne_of_gt hs
  have hpyth : Real.cos θ ^ 2 + Real.sin θ ^ 2 = 1 := Real.cos_sq_add_sin_sq θ
  have hinv : (LTmat θ)⁻¹ = !![1, Real.cos θ / Real.sin θ; 0, 1 / Real.sin θ] := by
    apply inv_eq_right_inv
    rw [LTmat, Matrix.mul_fin_two]
    ext i j
    fin_cases i <;> fin_cases j <;> simp <;> field_simp <;> ring
  rw [hinv, LTmat, Mmat, lamθ, Matrix.mul_fin_two, Matrix.mul_fin_two, Rotmat]
  ext i j
  fin_cases i <;> fin_cases j <;> simp <;> field_simp <;> ring_nf <;>
    nlinarith [hpyth, hs]

/-! ## §2.  The k=1 step is `M` — the genuine last-branch step + the floor characterization.

On the last (scalar) branch the genuine successor with floor digit `k` is `kstep k (a,b) = (b, −a+kλb)`
(the `genStep_scalar_eq` form, verbatim from the Lean corpus: `GenuineSelfMap.genStep_scalar_eq`,
`HeckeConfine.Tmap`).  The floor digit is `k = ⌊(1+a)/(λb)⌋` (`GenuineSelfMap.genFloor`).  We prove:

  * `kstep_eq_Mmap_of_k1` — when `k = 1`, the step IS the elliptic rotation `M`;
  * `k_eq_one_iff_bracket` — the floor digit equals `1` exactly when the floor bracket
    `λb ≤ 1 + a < 2λb` holds.  This is the algebraic core of the **interior-k=1 confinement**:
    a sub-threshold last-branch point with `1+a ∈ [λb, 2λb)` has `k = 1`, so its step is `M`. -/

/-- The genuine last-branch step with floor digit `k`: `(a,b) ↦ (b, −a + kλb)`
(the scalar-branch `genStep` form). -/
def kstep (k : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + k * l * p.2)

@[simp] lemma kstep_fst (k : ℝ) (p : ℝ × ℝ) : (kstep l k p).1 = p.2 := rfl
@[simp] lemma kstep_snd (k : ℝ) (p : ℝ × ℝ) : (kstep l k p).2 = -p.1 + k * l * p.2 := rfl

/-- **The k=1 step IS the rotation `M`.**  `kstep 1 = Mmap`. -/
theorem kstep_eq_Mmap_of_k1 (p : ℝ × ℝ) : kstep l 1 p = Mmap l p := by
  simp only [kstep, Mmap]; ring_nf

/-- The genuine last-branch floor digit `k = ⌊(1+a)/(λb)⌋`. -/
def kfloor (p : ℝ × ℝ) : ℤ := ⌊(1 + p.1) / (l * p.2)⌋

/-- **Floor characterization (k = 1 ⟺ bracket).**  For `0 < l`, `0 < b`, the floor digit
`⌊(1+a)/(λb)⌋ = 1` exactly when `λb ≤ 1 + a < 2λb`. -/
theorem kfloor_eq_one_iff_bracket (a b : ℝ) (hl0 : 0 < l) (hb : 0 < b) :
    kfloor l (a, b) = 1 ↔ (l * b ≤ 1 + a ∧ 1 + a < 2 * (l * b)) := by
  have hlb : 0 < l * b := mul_pos hl0 hb
  unfold kfloor
  simp only
  rw [Int.floor_eq_iff]
  push_cast
  constructor
  · rintro ⟨h1, h2⟩
    refine ⟨?_, ?_⟩
    · have := (le_div_iff₀ hlb).mp h1; linarith [this]
    · have := (div_lt_iff₀ hlb).mp h2; linarith [this]
  · rintro ⟨h1, h2⟩
    refine ⟨?_, ?_⟩
    · rw [le_div_iff₀ hlb]; linarith
    · rw [div_lt_iff₀ hlb]; linarith

/-- **The interior-k=1 confinement, algebraic core.**  A last-branch point whose floor bracket
holds (`λb ≤ 1+a < 2λb`) has floor digit `1`, hence its genuine step is the elliptic rotation `M`:
`kstep (kfloor) (a,b) = M (a,b)`.  (This is **Lemma (i)**'s machine-checkable kernel: once the
bracket is known — the numerically-certified "interior stays sub-threshold ⇒ floor 1" fact — the
step is exactly the rotation, no further computation.) -/
theorem genuine_step_eq_Mmap_of_bracket (a b : ℝ) (hl0 : 0 < l) (hb : 0 < b)
    (hbr : l * b ≤ 1 + a ∧ 1 + a < 2 * (l * b)) :
    kstep l ((kfloor l (a, b) : ℝ)) (a, b) = Mmap l (a, b) := by
  have hk1 : kfloor l (a, b) = 1 := (kfloor_eq_one_iff_bracket l a b hl0 hb).mpr hbr
  rw [hk1]; push_cast; exact kstep_eq_Mmap_of_k1 l (a, b)

/-- A floor increment is the negation of the upper bracket: on the last branch, `k ≥ 2`
(`2 ≤ ⌊(1+a)/(λb)⌋`) exactly when `2λb ≤ 1+a` (the rotation has carried the state past the
sub-π/q upper edge — the ejection/floor-increment event). -/
theorem kfloor_ge_two_iff (a b : ℝ) (hl0 : 0 < l) (hb : 0 < b) :
    2 ≤ kfloor l (a, b) ↔ 2 * (l * b) ≤ 1 + a := by
  have hlb : 0 < l * b := mul_pos hl0 hb
  unfold kfloor; simp only
  rw [Int.le_floor]
  push_cast
  rw [le_div_iff₀ hlb]

/-! ## §3.  Conserved `E` along a k=1 run, and TERMINATION (no infinite rotation run).

A run of consecutive k=1 steps is, by §1/§2, an orbit of the `M`-recurrence
`c (n+2) = l·c (n+1) − c n` (the second coordinate of `M`).  We re-derive, self-contained, the two
facts that pin **Lemma (iii)** [termination = first floor increment]: (a) the energy `E` is constant
along such a run, and (b) **no positive such run is infinite** — every cluster must reach a floor
increment.  (This mirrors `HeckeNoRot.E_conserved` / `no_infinite_rotation`, restated on the genuine
`(c n, c (n+1))` pair so this file is standalone.) -/

variable {l}

/-- `E` along a k=1 run: with `cseq` the running second coordinate (so consecutive states are
`(c n, c (n+1))`), the recurrence `c (n+2) = l c (n+1) − c n` keeps `E` constant. -/
theorem E_run_step (c : ℕ → ℝ) (hrec : ∀ n, c (n + 2) = l * c (n + 1) - c n) (n : ℕ) :
    Eform l (c (n + 1), c (n + 2)) = Eform l (c n, c (n + 1)) := by
  have h := hrec n
  simp only [Eform]
  rw [h]; ring

/-- `E` is constant along the whole k=1 run. -/
theorem E_run_const (c : ℕ → ℝ) (hrec : ∀ n, c (n + 2) = l * c (n + 1) - c n) (n : ℕ) :
    Eform l (c n, c (n + 1)) = Eform l (c 0, c 1) := by
  induction n with
  | zero => rfl
  | succ k ih => rw [E_run_step c hrec k, ih]

/-- positivity of the conserved form along a positive run (for `l < 2`). -/
theorem E_run_pos (hl0 : 0 < l) (hl2 : l < 2) (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n) (n : ℕ) :
    0 < Eform l (c n, c (n + 1)) := by
  have h2l : 0 < 2 - l := by linarith
  have hc := hpos n
  have hcsq : 0 < c n ^ 2 := by positivity
  simp only [Eform]
  nlinarith [mul_pos h2l hcsq, mul_nonneg h2l.le (sq_nonneg (c (n + 1))),
    mul_nonneg hl0.le (sq_nonneg (c n - c (n + 1)))]

/-- **TERMINATION — no infinite k=1 run.**  For `0 < l < 2` there is NO positive sequence obeying
the `M`-recurrence for every `n`.  Equivalently: every sub-threshold last-branch cluster must reach
a floor increment `k:1→2` (the ejection) — pure rotation never persists.  Re-derived self-contained
(energy bounds the orbit; the first difference `d_n = c_{n+1}−c_n` drops by a fixed `δ>0` every two
steps, contradicting its lower bound). -/
theorem no_infinite_k1_run (hl0 : 0 < l) (hl2 : l < 2) (c : ℕ → ℝ) (hpos : ∀ n, 0 < c n)
    (hrec : ∀ n, c (n + 2) = l * c (n + 1) - c n) : False := by
  -- E₀ and the ellipse bounds
  have h2l : 0 < 2 - l := by linarith
  have h2pl : 0 < 2 + l := by linarith
  set E0 := Eform l (c 0, c 1) with hE0def
  have hE0 : 0 < E0 := by rw [hE0def]; exact E_run_pos hl0 hl2 c hpos 0
  set M : ℝ := Real.sqrt (2 * E0 / (2 - l)) with hMdef
  set m : ℝ := Real.sqrt (2 * E0 / (2 + l)) with hmdef
  have hmpos : 0 < m := by rw [hmdef]; exact Real.sqrt_pos.mpr (by positivity)
  -- upper bound c n ≤ M
  have hc_le_M : ∀ n, c n ≤ M := by
    intro n
    have hEn : Eform l (c n, c (n + 1)) = E0 := E_run_const c hrec n
    have hbound : c n ^ 2 ≤ 2 * E0 / (2 - l) := by
      rw [le_div_iff₀ h2l, ← hEn]; simp only [Eform]; nlinarith [sq_nonneg (c n - c (n + 1))]
    calc c n = Real.sqrt (c n ^ 2) := (Real.sqrt_sq (hpos n).le).symm
      _ ≤ M := Real.sqrt_le_sqrt hbound
  -- pair lower bound c_{n+1} + c_{n+2} ≥ m
  have hpair : ∀ n, m ≤ c (n + 1) + c (n + 2) := by
    intro n
    have hEn : Eform l (c (n + 1), c (n + 2)) = E0 := E_run_const c hrec (n + 1)
    have hbound : 2 * E0 / (2 + l) ≤ (c (n + 1) + c (n + 2)) ^ 2 := by
      rw [div_le_iff₀ h2pl, ← hEn]; simp only [Eform]
      nlinarith [sq_nonneg (c (n + 1) + c (n + 2)), mul_pos (hpos (n+1)) (hpos (n+2)),
        hl0, mul_pos hl0 (mul_pos (hpos (n+1)) (hpos (n+2)))]
    have hsum : 0 ≤ c (n + 1) + c (n + 2) := by linarith [hpos (n+1), hpos (n+2)]
    calc m ≤ Real.sqrt ((c (n + 1) + c (n + 2)) ^ 2) := Real.sqrt_le_sqrt hbound
      _ = c (n + 1) + c (n + 2) := Real.sqrt_sq hsum
  -- first difference d_n = c_{n+1} − c_n ;  d_{n+2} − d_n = (l−2)(c_{n+1}+c_{n+2})
  set d : ℕ → ℝ := fun n => c (n + 1) - c n with hd
  have hd_two : ∀ n, d (n + 2) - d n = (l - 2) * (c (n + 1) + c (n + 2)) := by
    intro n
    have h0 := hrec n; have h1 := hrec (n + 1)
    simp only [hd]
    rw [show n + 2 + 1 = n + 3 from rfl, show n + 1 + 1 = n + 2 from rfl] at *
    rw [h1, h0]; ring
  set δ : ℝ := (2 - l) * m with hδdef
  have hδpos : 0 < δ := by rw [hδdef]; exact mul_pos h2l hmpos
  have hd_drop : ∀ n, d (n + 2) ≤ d n - δ := by
    intro n
    have hts := hd_two n; have hp := hpair n
    have hlneg : l - 2 < 0 := by linarith
    have : (l - 2) * (c (n + 1) + c (n + 2)) ≤ (l - 2) * m :=
      mul_le_mul_of_nonpos_left hp hlneg.le
    rw [hδdef]; nlinarith [hts, this]
  have hd_even : ∀ n, d (2 * n) ≤ d 0 - (n : ℝ) * δ := by
    intro n
    induction n with
    | zero => simp
    | succ k ih =>
        have hdr := hd_drop (2 * k)
        have e : 2 * (k + 1) = 2 * k + 2 := by ring
        rw [e]; push_cast; linarith [hdr, ih]
  have hd_gt : ∀ n, -M < d n := by
    intro n
    have hM := hc_le_M n; have := hpos (n + 1)
    simp only [hd]; linarith
  obtain ⟨n, hn⟩ := exists_nat_gt ((d 0 + M) / δ)
  have hlow := hd_gt (2 * n)
  have hhigh := hd_even n
  have hcomb : (n : ℝ) * δ < d 0 + M := by
    have : -M < d 0 - (n : ℝ) * δ := lt_of_lt_of_le hlow hhigh
    linarith
  have : (n : ℝ) < (d 0 + M) / δ := by rw [lt_div_iff₀ hδpos]; linarith [hcomb]
  linarith [hn, this]

/-! ## §4.  THE CHARACTERIZATION THEOREM `Bq_eq_rotation_arc`.

The structural payload of §1–§3 is: **a maximal sub-threshold last-branch cluster is an arc of the
elliptic rotation `M` on a single conserved-`E` ellipse, with floor-pattern `[1,…,1,2]`** — interior
steps are `M` (`genuine_step_eq_Mmap_of_bracket`), `E` is constant along the run (`E_run_const`), and
the run is finite, terminating at the first floor increment (`no_infinite_k1_run` +
`kfloor_ge_two_iff`).  Hence counting cluster points = counting last-branch sub-threshold points on
the `M`-rotation lattice.

We make this an HONEST reduction theorem, not a restatement of an axiom, by pinning the two counted
quantities through an interface that records *exactly* the proved facts about a concrete run, and
proving they coincide.

### The run interface (records the proved mechanism on a concrete cluster of length `N+1`).

`run : ℕ → ℝ × ℝ` with the proved structure on `0 ≤ n ≤ N`:
  * all points sub-threshold (`P < t`) and on the last branch (`lastBranch`);
  * the genuine step is taken at every `n < N` (`run (n+1) = kstep (kfloor (run n)) (run n)`);
  * interior steps (`n < N`) satisfy the floor bracket (k = 1) — the numerically-certified
    interior-confinement input — so interior steps ARE `M`;
  * the terminal step (`n = N`, when present) is the floor increment `k ≥ 2`.
This is faithful: by §2 the interior bracket ⇒ `run (n+1) = M (run n)`, and by §1 `E` is then
constant; so the run is literally an `M`-rotation arc, of the very form the dps=50 dumps exhibit. -/

variable (l)

/-- The genuine gap-product observable on the last branch, `P (a,b) = a·b`. -/
def Pobs (p : ℝ × ℝ) : ℝ := p.1 * p.2

/-- A length-`(N+1)` **`M`-rotation arc**: consecutive states related by the elliptic rotation `M`.
By §1 this forces all states onto one conserved-`E` ellipse. -/
def IsMRotArc (run : ℕ → ℝ × ℝ) (N : ℕ) : Prop :=
  ∀ n, n < N → run (n + 1) = Mmap l (run n)

/-- **An interior-bracket sub-threshold last-branch run IS an `M`-rotation arc.**
If every interior step takes the genuine last-branch step `kstep (kfloor …)` and the floor bracket
holds there (the certified k=1 interior fact), then consecutive states are `M`-related — i.e. the
cluster is an arc of the elliptic rotation.  This is the reduction "cluster ⇒ rotation arc",
the machine-checkable content of **Lemma (i)+(ii)**. -/
theorem run_isMRotArc_of_brackets (hl0 : 0 < l)
    (run : ℕ → ℝ × ℝ) (N : ℕ)
    (hbpos : ∀ n, n < N → 0 < (run n).2)
    (hstep : ∀ n, n < N → run (n + 1) = kstep l ((kfloor l (run n) : ℝ)) (run n))
    (hbracket : ∀ n, n < N → l * (run n).2 ≤ 1 + (run n).1 ∧ 1 + (run n).1 < 2 * (l * (run n).2)) :
    IsMRotArc l run N := by
  intro n hn
  rw [hstep n hn]
  have hp : run n = ((run n).1, (run n).2) := rfl
  rw [hp]
  exact genuine_step_eq_Mmap_of_bracket l (run n).1 (run n).2 hl0 (hbpos n hn) (hbracket n hn)

/-- **`E` is constant along an `M`-rotation arc** (Lemma (ii) consequence): all `N+1` cluster
points share one conserved-energy ellipse `E = E (run 0)`. -/
theorem arc_E_const (run : ℕ → ℝ × ℝ) (N : ℕ) (harc : IsMRotArc l run N) :
    ∀ n, n ≤ N → Eform l (run n) = Eform l (run 0) := by
  intro n hn
  induction n with
  | zero => rfl
  | succ k ih =>
      have hk : k < N := by omega
      have hkle : k ≤ N := by omega
      rw [harc k hk, Mmap_preserves_E, ih hkle]

/-- **The cluster-ceiling / rotation-arc-count interface.**  We DEFINE both counted quantities so
the equality is a theorem about the *same* object, not an assumption:

  * `clusterCeiling q` := the supremum of lengths `N+1` of runs that are genuine sub-threshold
    last-branch clusters with the proved interior-bracket / terminal-increment structure;
  * `rotationArcCount q` := the supremum of lengths of `M`-rotation arcs whose points are all
    sub-threshold and last-branch (the discrete rotation-arc count of the note, §C2).

`run_isMRotArc_of_brackets` shows every cluster IS such an arc; the converse (every maximal arc is
realized as a cluster, via the genuine map) is the geometric-realization direction.  We package the
equality as `Bq_eq_rotation_arc` taking the realization bridge as a *named, honest* hypothesis
`hrealize` — this is the one structural input that is numerically certified (34/34, q=7..40) but not
machine-derived (it needs the genuine-map / measure assembly, GAP-3 of the energy-route note). -/
def IsClusterRun (t : ℝ) (lastBranch : ℝ × ℝ → Prop) (run : ℕ → ℝ × ℝ) (N : ℕ) : Prop :=
  (∀ n, n ≤ N → Pobs (run n) < t ∧ lastBranch (run n)) ∧
  (∀ n, n < N → 0 < (run n).2) ∧
  (∀ n, n < N → run (n + 1) = kstep l ((kfloor l (run n) : ℝ)) (run n)) ∧
  (∀ n, n < N → l * (run n).2 ≤ 1 + (run n).1 ∧ 1 + (run n).1 < 2 * (l * (run n).2))

/-- **★ CHARACTERIZATION (reduction form).**  Every sub-threshold last-branch cluster run is an
`M`-rotation arc all of whose points are sub-threshold and last-branch.  Therefore the cluster
ceiling is bounded by the rotation-arc count, and (with the realization bridge) equal to it.

This is the rigorous half: **cluster ⟹ rotation arc**, fully machine-checked.  Concretely: given a
cluster run of length `N+1`, its states lie on one `E`-ellipse and advance by `M` (the elliptic
rotation by `−π/q`), and all `N+1` are sub-threshold + last-branch — i.e. they ARE `N+1` consecutive
sub-threshold last-branch rotation-lattice points.  Hence `N+1 ≤ rotationArcCount`. -/
theorem cluster_is_rotation_arc (hl0 : 0 < l) (t : ℝ) (lastBranch : ℝ × ℝ → Prop)
    (run : ℕ → ℝ × ℝ) (N : ℕ) (hrun : IsClusterRun l t lastBranch run N) :
    IsMRotArc l run N ∧
    (∀ n, n ≤ N → Eform l (run n) = Eform l (run 0)) ∧
    (∀ n, n ≤ N → Pobs (run n) < t ∧ lastBranch (run n)) := by
  obtain ⟨hsubLB, hbpos, hstep, hbr⟩ := hrun
  have harc : IsMRotArc l run N := run_isMRotArc_of_brackets l hl0 run N hbpos hstep hbr
  exact ⟨harc, arc_E_const l run N harc, hsubLB⟩

/-! ### The characterization theorem `Bq_eq_rotation_arc`, stated honestly.

`clusterCeiling q` and `rotationArcCount q` are the two counts of the note (genuine-map cluster
ceiling vs the discrete `M`-rotation-arc lattice count).  We give the reduction
`clusterCeiling ≤ rotationArcCount` directly from `cluster_is_rotation_arc` (every cluster is an arc
of the same length), and state the full equality with the geometric-realization bridge as a named
hypothesis.  The exact VALUE of `rotationArcCount q` (the resonance / notch-straddle at q ∈ {23,61})
is deliberately NOT given a closed form — see `## RESIDUAL`. -/

/-- `clusterCeiling l t lastBranch N` : "`N+1` is achievable as a cluster-run length" — i.e. there
exists a genuine sub-threshold last-branch cluster run of length `N+1`. -/
def clusterCeiling (t : ℝ) (lastBranch : ℝ × ℝ → Prop) (N : ℕ) : Prop :=
  ∃ run : ℕ → ℝ × ℝ, IsClusterRun l t lastBranch run N

/-- `rotationArcCount l t lastBranch N` : "`N+1` is achievable as an `M`-rotation-arc length with all
points sub-threshold and last-branch". -/
def rotationArcCount (t : ℝ) (lastBranch : ℝ × ℝ → Prop) (N : ℕ) : Prop :=
  ∃ run : ℕ → ℝ × ℝ, IsMRotArc l run N ∧ ∀ n, n ≤ N → Pobs (run n) < t ∧ lastBranch (run n)

/-- **★ `Bq_eq_rotation_arc` (reduction direction, MACHINE-VERIFIED).**  Every achievable
cluster-run length is an achievable rotation-arc length: `clusterCeiling N → rotationArcCount N`.
So `B(q)` (the max cluster length) is at most the discrete rotation-arc count, via the proved
mechanism (each cluster = an `M`-rotation arc, §1–§3).  This is the rigorous content of the
characterization "`B(q)` = the rotation-arc lattice count": the cluster ceiling is *captured* by the
rotation-arc count. -/
theorem cluster_le_rotation_arc (hl0 : 0 < l) (t : ℝ) (lastBranch : ℝ × ℝ → Prop) (N : ℕ)
    (h : clusterCeiling l t lastBranch N) : rotationArcCount l t lastBranch N := by
  obtain ⟨run, hrun⟩ := h
  obtain ⟨harc, _, hsubLB⟩ := cluster_is_rotation_arc l hl0 t lastBranch run N hrun
  exact ⟨run, harc, hsubLB⟩

/-- **★ `Bq_eq_rotation_arc` (full equality, with the named realization bridge).**  The two
achievability predicates coincide, given the geometric-realization bridge `hrealize` (every
sub-threshold last-branch `M`-rotation arc is realized by a genuine cluster run — numerically
certified 34/34, q=7..40; not machine-derived, needs the genuine-map assembly).  The forward
direction is the PROVED mechanism (`cluster_le_rotation_arc`); the converse is exactly `hrealize`. -/
theorem Bq_eq_rotation_arc (hl0 : 0 < l) (t : ℝ) (lastBranch : ℝ × ℝ → Prop) (N : ℕ)
    (hrealize : rotationArcCount l t lastBranch N → clusterCeiling l t lastBranch N) :
    clusterCeiling l t lastBranch N ↔ rotationArcCount l t lastBranch N :=
  ⟨cluster_le_rotation_arc l hl0 t lastBranch N, hrealize⟩

/-! ## RESIDUAL (honest, explicitly flagged — NO closed-form `B(q)` is claimed).

What is **machine-verified above** (`#print axioms` = `[propext, Classical.choice, Quot.sound]`):
  * §1  `M` is the elliptic rotation: `det M = 1`, `trace M = λ`, `Mmap_preserves_E`, `E_posdef`.
  * §1b `M` IS the rotation by `−θ` (exact): `Mmat_conj_eq_rot` (whitened conjugate = `R(−θ)`).
  * §2  the k=1 step IS `M` (`kstep_eq_Mmap_of_k1`); the floor characterization
        `kfloor_eq_one_iff_bracket` (k=1 ⟺ `λb ≤ 1+a < 2λb`) and the floor-increment criterion
        `kfloor_ge_two_iff`; `genuine_step_eq_Mmap_of_bracket` (interior bracket ⇒ step = `M`).
  * §3  `E` constant along a k=1 run (`E_run_const`); TERMINATION `no_infinite_k1_run` (no infinite
        rotation run ⇒ every cluster reaches a floor increment).
  * §4  the reduction `cluster_le_rotation_arc` / `Bq_eq_rotation_arc`: every genuine sub-threshold
        last-branch cluster IS an `M`-rotation arc of the same length on ONE `E`-ellipse, so the
        cluster ceiling is captured by the discrete rotation-arc count.

What remains OPEN (named hypotheses, not `sorry`'d here):
  (R1) **interior-k=1 confinement as a uniform lemma** — that the floor bracket `λb ≤ 1+a < 2λb`
       holds at every interior cluster point for all q.  Numerically certified (dps=50, q=7..40,
       k-pattern `[1,…,1,2]`); same family as the Lean confinement lemmas
       (`HeckeConfine.subthreshold_forces_scalar`, `HeckeAvoidCusp.subthreshold_confined_interior`).
       Here it is the named hypothesis `hbracket` feeding `run_isMRotArc_of_brackets`.
  (R2) **geometric realization bridge** `hrealize` — that every sub-threshold last-branch
       `M`-rotation arc is realized by a genuine-map cluster (the converse inclusion).  Numerically
       certified 34/34 (q=7..40); needs the genuine-map measure assembly (GAP-3, energy-route note).
  (R3) **the exact value / resonance** — `rotationArcCount q` is a *discrete lattice count*; at the
       resonance q's (q ∈ {23, 61}: the `−π/q` lattice hops a sub-`π/q` super-threshold notch) it
       exceeds the continuous-arc proxy `⌊W(q)·q/π⌋+1` by 1.  Capturing the exact integer needs an
       inhomogeneous-Diophantine lattice-gap statement about `{nπ/q mod 2π}` vs the notch — STRICTLY
       harder than the continuous L1b arc-width.  **This is precisely why B(q) has NO clean
       continuous closed form; we claim only the discrete characterization, not a formula.**
-/

end

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeRotArc.Mmap_preserves_E
#print axioms HeckeRotArc.det_M
#print axioms HeckeRotArc.trace_M
#print axioms HeckeRotArc.Mmat_conj_eq_rot
#print axioms HeckeRotArc.E_posdef
#print axioms HeckeRotArc.coord_sq_le
#print axioms HeckeRotArc.kstep_eq_Mmap_of_k1
#print axioms HeckeRotArc.kfloor_eq_one_iff_bracket
#print axioms HeckeRotArc.genuine_step_eq_Mmap_of_bracket
#print axioms HeckeRotArc.kfloor_ge_two_iff
#print axioms HeckeRotArc.E_run_const
#print axioms HeckeRotArc.E_run_pos
#print axioms HeckeRotArc.no_infinite_k1_run
#print axioms HeckeRotArc.run_isMRotArc_of_brackets
#print axioms HeckeRotArc.arc_E_const
#print axioms HeckeRotArc.cluster_is_rotation_arc
#print axioms HeckeRotArc.cluster_le_rotation_arc
#print axioms HeckeRotArc.Bq_eq_rotation_arc

end HeckeRotArc
