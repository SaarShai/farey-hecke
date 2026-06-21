import Mathlib

open scoped BigOperators
open scoped Real

set_option maxHeartbeats 4000000

/-!
# Closing `hSuperArc` — the genuine super-threshold arc covering (the B2 HARD residual)

## Goal (the `hSuperArc_target` of the μ-bridge reformulation)

The B3 keystone (`projects/mu_bridge_B3_lean/RequestProject/Main.lean`,
`Xomega_ge_via_energy`) reduces the all-`q` uniform onset lower bound
`1/λ³ ≤ X_Ω(q)` to ONE genuinely analytic input, the **covering**

> `hSuperArc : (⋃ k ∈ range q, (g k)⁻¹' {x | 1/l³ ≤ Pgen l x}) = …`

with `g k = (Mmap l)^[k]` the block-rotation iterates (`Mmap (a,b) = (b,−a+λb)`), the
genuine observable `Pgen (a,b) = a(a+λb)/λ`, and `q = m+2`, `l = 2cos(π/q)`.

This file realizes that covering on the genuine `Mmap`/`Pgen`, consuming the SEALED L1b
arc-coverage fact `L1bArcCoverage.arc_coverage_ineq` (reproduced verbatim) and the rotation
algebra of `Mmap`.

## ★ FAITHFULNESS / HONESTY: the literal `= Set.univ` covering is FALSE.

B2 (`projects/mu_bridge_B2_lean`) states `super_arc_hit_within_q` and `SuperArcCover` on **all**
of `ℝ × ℝ` (`= Set.univ`).  **That target is FALSE**, and we demonstrate the counterexample
in `superarc_univ_is_false` below:

  * take `p = (0,0)`.  `Mmap l (0,0) = (0,0)` (a fixed point), so the whole orbit is `(0,0)`,
    and `Pgen l (0,0) = 0 < 1/l³`.  Hence NO iterate `k` lands `(0,0)` in the super-threshold
    set; the orbit of `(0,0)` never hits `{1/l³ ≤ Pgen}`.  So `super_arc_hit_within_q` is false
    for `p = (0,0)`, and the union of preimages is NOT `Set.univ` (it misses `(0,0)`).

(More generally every ellipse `E(p) = a²−λab+b²` below a positive `q`-dependent threshold keeps
the entire `Mmap`-orbit sub-threshold — verified numerically: the sub-threshold arc reaches the
full circle for small `E`.)

The FAITHFUL covering — the one the reformulated keystone actually needs — is the covering
**restricted to the conull corridor `Sclosed`** on which the invariant measure `μ` lives
(`μ (Sclosed)ᶜ = 0`).  `covering_pos_measure` only needs the super-level set to have positive
`μ`-measure, and a covering valid `μ`-a.e. (equivalently: on the corridor `D` with `μ Dᶜ = 0`)
suffices.  We therefore deliver:

  * `orbit_hit_in_corridor` — every point of the corridor region whose ellipse clears the
    `E`-floor has its `Mmap`-orbit hit the super-threshold set within `q` steps;
  * `SuperArcCover_corridor` — the corridor-restricted covering, the faithful `hSuperArc`.

## What is PROVED here (sorry-free, axiom-clean `[propext, Classical.choice, Quot.sound]`)

1. **`cos_grid_hit`** — THE PIGEONHOLE ENGINE.  For `q ≥ 1`, `θ = π/q`, and any phase `φ`, the
   `q` equally-spaced rotation phases `φ + 2kθ` (`k < q`, spacing `2θ = 2π/q`, sweeping the full
   circle) include one with `cos(φ + 2kθ) ≥ cos θ` — i.e. the grid lands inside any super-arc of
   half-width `≥ θ`.  This is the discrete-rotation-arc covering core, fully formal (uses
   `round`-nearest + `Int.emod` reduction + `cos_sub_int_mul_two_pi` periodicity).

2. **`orbit_hit_of_realization`** — the bridge consumer: GIVEN the sinusoid realization
   `Pgen(M^k p) = C0 + R·cos(φ + 2kθ)` with `R > 0` and the threshold gate
   `(t − C0)/R ≤ cos θ`, some `k < q` has `t ≤ Pgen(M^k p)`.  PROVED from `cos_grid_hit`.

3. **`wide_arc_translates_cover`** — orbit-hits ⟹ preimages cover (verbatim from B2, q-independent
   set algebra).  PROVED.

4. **`arc_coverage_ineq`** — the SEALED L1b fact `2·arccos(2√6/5)/π < 33/256`, reproduced verbatim
   from `L1bArcCoverage.lean` (the sub-arc width bound that, on the genuine normalization, forces
   the super-arc half-width `≥ θ = π/q`).  PROVED.

5. **`superarc_univ_is_false`** — the honest negative: the all-`ℝ²` covering FAILS (the `(0,0)`
   fixed point witnesses it).  PROVED.

## The single NAMED residual (the genuine HARD analytic step, `sorry` for Aristotle)

**`pgen_orbit_realization`** — the un-assembled **realization bridge**: along an `Mmap`-orbit
started at a corridor point `p` whose ellipse clears the `E`-floor, the genuine observable is the
affine sinusoid

  `Pgen(M^k p) = C0(p) + R(p)·cos(φ(p) + 2kθ)`,    `R(p) > 0`,

AND the threshold gate `(1/l³ − C0(p))/R(p) ≤ cos θ` holds (this last is where the corridor
`E`-floor and the sealed `arc_coverage_ineq` / `B1_target` are consumed: `C0, R` are positive
multiples of `E(p)`, so the gate is `E`-scale-invariant and reduces to the sealed sub-arc width
`< π/q`).  This is EXACTLY the step B2 marked `sorry` (`super_arc_hit_within_q`), here sharpened
to the precise sinusoid datum `(C0, R, φ)` + gate, isolating the missing content to: (i) the
whitening identification `Pgen = α·E + ρ·E·cos(…)` (the `Mmat_conj_eq_rot` change of coordinates),
and (ii) the gate `(t−αE)/(ρE) ≤ cos θ` from `arc_coverage_ineq` at the corridor `E`-floor.

Everything DOWNSTREAM of `pgen_orbit_realization` is PROVED here; the covering is delivered
modulo this single named hypothesis.
-/

namespace MuCloseHSuperArc

noncomputable section

open MeasureTheory

/-! ## §0.  Verbatim sealed objects (faithfulness anchors). -/

/-- `λ_q = 2 cos(π/q)` — verbatim `L1bArcCoverage.lamq` / `UniformQge22Energy.lamq`. -/
def lamq (q : ℕ) : ℝ := 2 * Real.cos (Real.pi / q)

/-- `θ = π/q` — the per-block rotation step. -/
def thetaq (q : ℕ) : ℝ := Real.pi / q

/-- The genuine block step `Mmap (a,b) = (b, −a + λb)` — verbatim `BCZHeckeRotationArc.Mmap`
(elliptic rotation by `−θ`, `det = 1`, `trace = λ`). -/
def Mmap (l : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.2, -p.1 + l * p.2)

@[simp] lemma Mmap_fst (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).1 = p.2 := rfl
@[simp] lemma Mmap_snd (l : ℝ) (p : ℝ × ℝ) : (Mmap l p).2 = -p.1 + l * p.2 := rfl

/-- The genuine observable `Pgen (a,b) = a(a+λb)/λ` — verbatim `UniformOnset.Pgen`. -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l

@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-- The conserved energy form `E(a,b) = a² − λab + b²` — verbatim `BCZHeckeRotationArc.Eform`. -/
def Eform (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2

@[simp] lemma Eform_apply (l : ℝ) (p : ℝ × ℝ) :
    Eform l p = p.1 ^ 2 - l * (p.1 * p.2) + p.2 ^ 2 := rfl

/-- `Mmap` preserves `E` (verbatim `Mmap_preserves_E`, by `ring`). -/
theorem Mmap_preserves_E (l : ℝ) (p : ℝ × ℝ) : Eform l (Mmap l p) = Eform l p := by
  simp only [Eform, Mmap]; ring

/-- **The corridor region** `Dcorr` on which `μ` lives — verbatim `UniformOnset.Dcorr`.  Every
point here is bounded away from the cusp tip `(0,0)`, so its ellipse clears the `E`-floor. -/
def Dcorr (l : ℝ) : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}

/-! ## §1.  ★ THE PIGEONHOLE ENGINE (q-independent, PROVED).

For `q ≥ 1`, `θ = π/q`, the `q` rotation phases `φ + 2kθ` (`k < q`) are equally spaced by
`2θ = 2π/q` and sweep the full circle.  Hence they cannot all avoid any super-arc of cosine-radius
`≥ θ`: some `k < q` has `cos(φ + 2kθ) ≥ cos θ`.  This is the discrete-rotation form of "a grid of
spacing `2π/q` hits every arc of width `≥ 2π/q`".  Proof: take the nearest grid index to `−φ` via
`round`, reduce mod `q` by `Int.emod` (using `2qθ = 2π`-periodicity of `cos`), then
`|φ + 2kθ| ≤ θ ⟹ cos(φ+2kθ) ≥ cos θ` from monotonicity of `cos` on `[0,π]`. -/

/-- **★ PIGEONHOLE / GRID-HITS-SUPER-ARC (PROVED, axiom-clean).** -/
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

/-! ## §2.  ★ THE REALIZATION CONSUMER (PROVED).

The realization datum (supplied by `pgen_orbit_realization`, §4) is: along the `Mmap`-orbit of a
corridor point, `Pgen(M^k p) = C0 + R·cos(φ + 2kθ)` with `R > 0`, AND the threshold gate
`(t − C0)/R ≤ cos θ`.  Given that datum, the pigeonhole `cos_grid_hit` immediately produces a `k`
with `t ≤ Pgen(M^k p)`.  PROVED. -/

/-- **★ REALIZATION ⟹ ORBIT HITS (PROVED).**  If the orbit observable is the affine sinusoid
`Pk k = C0 + R·cos(φ + 2kθ)` with `R > 0`, and the threshold gate `(t − C0)/R ≤ cos θ` holds, then
some `k < q` clears the threshold `t ≤ Pk k`. -/
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

/-! ## §3.  ★ THE SEALED L1b ARC-COVERAGE FACT (verbatim, PROVED).

`arc_coverage_ineq : 2·arccos(2√6/5)/π < 33/256`, reproduced byte-for-byte from
`L1bArcCoverage.arc_coverage_ineq` (which is proved sorry-free there, axioms
`[propext, Classical.choice, Quot.sound]`).  This is the sub-arc width bound: on the genuine
normalization `Pgen = (E/2A₂)·Fobs`, `Fobs = 3λ/2 + √(1+2λ²)·cos`, the sub-threshold cosine value
is `2√6/5` and the sub-arc half-width `arccos(2√6/5) < 33π/512 ≤ H = (L−1)θ/2`, so the
complementary super-arc has half-width `≥ θ = π/q` — exactly the input `cos_grid_hit` needs.  We
reproduce the proof verbatim so this file is self-contained for Aristotle. -/

/-- **`cos²(33π/512) < 24/25`** — verbatim `L1bArcCoverage.cos_sq_lt`. -/
theorem cos_sq_lt : Real.cos (33 * Real.pi / 512) ^ 2 < 24 / 25 := by
  have hpi_lo : (3.1415 : ℝ) < Real.pi := Real.pi_gt_d4
  have hpi_hi : Real.pi < (3.1416 : ℝ) := Real.pi_lt_d4
  set x := 33 * Real.pi / 512 with hx_def
  have hx_pos : (0 : ℝ) < x := by rw [hx_def]; linarith [Real.pi_pos]
  have hx_lo : (207339 : ℝ) / 1024000 ≤ x := by rw [hx_def]; linarith
  have hx_hi : x ≤ (129591 : ℝ) / 640000 := by rw [hx_def]; linarith
  have hx_lt1 : x < 1 := by linarith
  set a := x ^ 2 with ha_def
  have ha_pos : (0 : ℝ) < a := by rw [ha_def]; positivity
  have ha_lo : (42989460921 : ℝ) / 1048576000000 ≤ a := by
    rw [ha_def]
    nlinarith [sq_nonneg x, sq_nonneg ((207339 : ℝ) / 1024000),
               mul_pos (show (0:ℝ) < 207339/1024000 by norm_num) hx_pos]
  have ha_hi : a ≤ (16793827281 : ℝ) / 409600000000 := by
    rw [ha_def]
    nlinarith [sq_nonneg ((129591:ℝ)/640000 - x), hx_hi, hx_pos.le,
               mul_pos hx_pos hx_pos]
  have habs : |x| ≤ 1 := by rw [abs_of_pos hx_pos]; linarith
  have hcb := Real.cos_bound habs
  rw [abs_le] at hcb
  have habs4 : |x| ^ 4 = a ^ 2 := by rw [ha_def, abs_of_pos hx_pos]; ring
  rw [habs4] at hcb
  have hcos_ub : Real.cos x ≤ 1 - a / 2 + a ^ 2 * (5 / 96) := by
    rw [ha_def]; linarith [hcb.2]
  have hcos_nn : (0 : ℝ) ≤ Real.cos x := by
    apply Real.cos_nonneg_of_mem_Icc
    constructor
    · linarith
    · rw [hx_def]; linarith
  have hU_nn : (0 : ℝ) ≤ 1 - a / 2 + a ^ 2 * (5 / 96) := by linarith [hcos_nn, hcos_ub]
  have hcos2_ub : Real.cos x ^ 2 ≤ (1 - a / 2 + a ^ 2 * (5 / 96)) ^ 2 := by
    apply sq_le_sq'
    · linarith [hcos_nn]
    · exact hcos_ub
  have hpoly : (24 : ℝ) / 25 - (1 - a / 2 + a ^ 2 * (5 / 96)) ^ 2 > 0 := by
    nlinarith [ha_lo, ha_hi, sq_nonneg a, sq_nonneg (a - 42989460921 / 1048576000000),
               mul_nonneg ha_pos.le ha_pos.le,
               mul_nonneg (mul_nonneg ha_pos.le ha_pos.le) ha_pos.le,
               mul_pos ha_pos ha_pos]
  linarith [hcos2_ub, hpoly]

/-- **★ SEALED L1b ARC-COVERAGE** `2·arccos(2√6/5)/π < 33/256` — verbatim
`L1bArcCoverage.arc_coverage_ineq`. -/
theorem arc_coverage_ineq : 2 * Real.arccos (2 * Real.sqrt 6 / 5) / Real.pi < 33 / 256 := by
  have hpi_pos : (0 : ℝ) < Real.pi := Real.pi_pos
  have h6_sq : Real.sqrt 6 ^ 2 = 6 := Real.sq_sqrt (by norm_num)
  have hCD_pos : (0 : ℝ) < 2 * Real.sqrt 6 / 5 := by positivity
  have hCD_lt1 : 2 * Real.sqrt 6 / 5 < 1 := by
    have hsqrt6_nn : 0 ≤ Real.sqrt 6 := Real.sqrt_nonneg 6
    nlinarith [h6_sq, hsqrt6_nn]
  have hcos33_pos : 0 < Real.cos (33 * Real.pi / 512) := by
    apply Real.cos_pos_of_mem_Ioo
    constructor <;> linarith [Real.pi_pos]
  have hcosCD_sq : (2 * Real.sqrt 6 / 5) ^ 2 = 24 / 25 := by nlinarith [h6_sq]
  have hcos33_lt_CD : Real.cos (33 * Real.pi / 512) < 2 * Real.sqrt 6 / 5 := by
    have h_sq := cos_sq_lt
    have hlt2 : Real.cos (33 * Real.pi / 512) ^ 2 < (2 * Real.sqrt 6 / 5) ^ 2 := by
      rw [hcosCD_sq]; exact h_sq
    have hcos_nn : 0 ≤ Real.cos (33 * Real.pi / 512) := hcos33_pos.le
    nlinarith [sq_nonneg (2 * Real.sqrt 6 / 5 - Real.cos (33 * Real.pi / 512)),
               sq_abs (Real.cos (33 * Real.pi / 512)),
               mul_pos hcos33_pos hCD_pos]
  have hangle_in_Icc : 33 * Real.pi / 512 ∈ Set.Icc 0 Real.pi := by
    constructor <;> linarith [Real.pi_pos]
  have harccos_cos : Real.arccos (Real.cos (33 * Real.pi / 512)) = 33 * Real.pi / 512 :=
    Real.arccos_cos hangle_in_Icc.1 hangle_in_Icc.2
  have harccos_lt : Real.arccos (2 * Real.sqrt 6 / 5) < 33 * Real.pi / 512 := by
    rw [← harccos_cos]
    exact Real.arccos_lt_arccos (Real.neg_one_le_cos _) hcos33_lt_CD hCD_lt1.le
  rw [div_lt_iff₀ hpi_pos]
  nlinarith [harccos_lt, hpi_pos]

/-! ## §4.  ★ THE GENUINE HARD RESIDUAL — the realization bridge (single NAMED `sorry`).

This is the ONLY open content of this file.  It is exactly the step B2's `super_arc_hit_within_q`
marked `sorry`, here sharpened to the precise sinusoid datum + threshold gate so the downstream
`orbit_hit_of_realization` + `cos_grid_hit` close the covering deterministically.

CONTENT to supply (Aristotle):
  Let `q = m+2 ≥ 3`, `l = lamq q = 2cos(π/q)` (so `0 < l < 2`), `θ = π/q`, `t = 1/l³`.
  For a corridor point `p ∈ Dcorr l` (so `E(p) > 0`, bounded away from the cusp tip):

  (R1)  **Whitening / sinusoid identification.**  There are `C0, R, φ` with `R > 0` and
        `Pgen(M^k p) = C0 + R·cos(φ + 2kθ)` for all `k`.  PROOF: by `Mmap_preserves_E` the orbit
        lies on the fixed ellipse `E(p)`; by `Mmat_conj_eq_rot` (`BCZHeckeRotationArc`) `Mmap` is
        the planar rotation by `−θ` in whitening coordinates; `Pgen` is a quadratic form, so along
        the orbit it is `α·E(p) + ρ·E(p)·cos(φ₀ − 2kθ)` for `l`-only constants `α, ρ > 0`
        (numerically `α·(4−l²) → 3`, `ρ·(4−l²) → 3` as `l → 2`).  Set `C0 = α E(p)`, `R = ρ E(p)`.

  (R2)  **Threshold gate.**  `(t − C0)/R ≤ cos θ`.  PROOF: this is `E`-scale-invariant — divide by
        `E(p)`: `(t/E(p) − α)/ρ ≤ cos θ`.  On the genuine `Fobs = 3λ/2 + √(1+2λ²)·cos`
        normalization the sub-threshold cosine value is `2√6/5`, and `arc_coverage_ineq`
        (`2·arccos(2√6/5)/π < 33/256`) gives the sub-arc half-width `arccos(2√6/5) < 33π/512`,
        whence the complementary super-arc half-width `≥ θ = π/q` and the gate `(t−C0)/R ≤ cos θ`.
        This is where the corridor `E`-floor (`E(p)` bounded below on `Dcorr`) and the sealed
        `arc_coverage_ineq` / `L1bArcCoverage.B1_target` enter.

We package (R1)+(R2) as the existence of `(C0, R, φ)` with `R > 0`, the orbit identity, and the
gate — the precise datum `orbit_hit_of_realization` consumes. -/

/-- **★ THE GENUINE HARD RESIDUAL (realization bridge) — NAMED `sorry` for Aristotle.**
For `q = m+2`, `l = lamq q`, and a corridor point `p ∈ Dcorr l`, the `Mmap`-orbit observable is an
affine sinusoid `C0 + R·cos(φ + 2kθ)` with `R > 0` whose threshold gate `(1/l³ − C0)/R ≤ cos θ`
holds.  (The two analytic ingredients: the whitening identification `Pgen = αE + ρE·cos(…)` and
the gate from `arc_coverage_ineq` at the corridor `E`-floor.) -/
theorem pgen_orbit_realization (m : ℕ) (l : ℝ) (hl : l = lamq (m + 2))
    (p : ℝ × ℝ) (hp : p ∈ Dcorr l) :
    ∃ C0 R phi : ℝ, 0 < R ∧
      (∀ k, Pgen l ((Mmap l)^[k] p)
            = C0 + R * Real.cos (phi + 2 * (k:ℝ) * (Real.pi / ((m + 2 : ℕ) : ℝ)))) ∧
      (1 / l ^ 3 - C0) / R ≤ Real.cos (Real.pi / ((m + 2 : ℕ) : ℝ)) := by
  -- ★ THE GENUINELY HARD STEP.  Reduces to:
  --   (R1) the whitening sinusoid identification `Pgen(M^k p) = αE + ρE·cos(φ − 2kθ)`
  --        (via `BCZHeckeRotationArc.Mmat_conj_eq_rot` + `Mmap_preserves_E`), and
  --   (R2) the threshold gate `(t − C0)/R ≤ cos θ` from `arc_coverage_ineq` (proved above,
  --        SEALED) at the corridor `E`-floor on `Dcorr l`.
  sorry

/-! ## §5.  ★ THE FAITHFUL COVERING (PROVED modulo §4).

We assemble: `pgen_orbit_realization` (§4) ⟶ `orbit_hit_of_realization` (§2) gives orbit-hits on
the corridor; `wide_arc_translates_cover` (§6) turns orbit-hits into the preimage covering, here
RESTRICTED to the corridor `Dcorr l` (the conull set `μ` lives on).  This is the faithful
`hSuperArc` — NOT the false all-`ℝ²` form. -/

/-- **★ ORBIT HITS SUPER-THRESHOLD WITHIN `q` (on the corridor) — PROVED modulo §4.**
For `q = m+2`, `l = lamq q`, every corridor point `p ∈ Dcorr l` has its `Mmap`-orbit hit the
super-threshold set `{1/l³ ≤ Pgen}` within `q` steps. -/
theorem orbit_hit_in_corridor (m : ℕ) (l : ℝ) (hl : l = lamq (m + 2))
    (p : ℝ × ℝ) (hp : p ∈ Dcorr l) :
    ∃ k, k < m + 2 ∧ (Mmap l)^[k] p ∈ {x : ℝ × ℝ | 1 / l ^ 3 ≤ Pgen l x} := by
  obtain ⟨C0, R, phi, hR, hreal, hthr⟩ := pgen_orbit_realization m l hl p hp
  obtain ⟨k, hk, hhit⟩ :=
    orbit_hit_of_realization (m + 2) (by omega) (1 / l ^ 3) C0 R phi hR
      (fun k => Pgen l ((Mmap l)^[k] p)) hreal hthr
  exact ⟨k, hk, hhit⟩

/-! ## §6.  ★ THE ABSTRACT COVER (verbatim from B2, PROVED). -/

/-- **★ ORBIT-HITS ⟹ PREIMAGES COVER (q-independent, measure-free) — verbatim B2.**
If for the map `R : X → X` every point of `D ⊆ X` hits `S` within `q` steps, then `D` is contained
in the union of the `q` preimages `⋃ k<q, R^[k]⁻¹ S`. -/
theorem wide_arc_translates_cover_on
    {X : Type*} (R : X → X) (q : ℕ) (S D : Set X)
    (hhit : ∀ x ∈ D, ∃ k, k < q ∧ R^[k] x ∈ S) :
    D ⊆ (⋃ k ∈ Finset.range q, (fun y => R^[k] y) ⁻¹' S) := by
  intro x hx
  obtain ⟨k, hk, hkx⟩ := hhit x hx
  rw [Set.mem_iUnion₂]
  exact ⟨k, Finset.mem_range.mpr hk, hkx⟩

/-- **★ THE FAITHFUL `hSuperArc` (corridor-restricted) — PROVED modulo §4.**
For `q = m+2`, `l = lamq q`, the corridor `Dcorr l` is COVERED by the `q` rotation-translates of
the genuine super-threshold set under `Mmap l`.  This is the faithful covering input to the
reformulated keystone: with `μ (Dcorr l)ᶜ = 0`, the super-level set has positive `μ`-measure (via
`covering_pos_measure`), which is all `hCorr_uniform_via_energy` needs.  The literal all-`ℝ²`
`= Set.univ` form is FALSE (see `superarc_univ_is_false`). -/
theorem SuperArcCover_corridor (m : ℕ) (l : ℝ) (hl : l = lamq (m + 2)) :
    Dcorr l ⊆ (⋃ k ∈ Finset.range (m + 2),
        (fun y => (Mmap l)^[k] y) ⁻¹' {x : ℝ × ℝ | 1 / l ^ 3 ≤ Pgen l x}) :=
  wide_arc_translates_cover_on (Mmap l) (m + 2) {x : ℝ × ℝ | 1 / l ^ 3 ≤ Pgen l x} (Dcorr l)
    (fun p hp => orbit_hit_in_corridor m l hl p hp)

/-! ## §7.  ★ THE HONEST NEGATIVE — the all-`ℝ²` covering is FALSE.

The cusp tip `(0,0)` is an `Mmap`-fixed point whose orbit is constant `(0,0)` with
`Pgen l (0,0) = 0 < 1/l³`.  So the orbit of `(0,0)` NEVER hits the super-threshold set; hence
`super_arc_hit_within_q` (B2's all-`ℝ²` form) is false at `(0,0)`, and the union of preimages omits
`(0,0)`, so it is NOT `Set.univ`.  This is why the faithful covering must be corridor-restricted. -/

/-- `(0,0)` is an `Mmap`-fixed point. -/
theorem Mmap_fix_zero (l : ℝ) : Mmap l (0, 0) = (0, 0) := by simp [Mmap]

/-- `Mmap`-orbit of `(0,0)` is constant `(0,0)`. -/
theorem Mmap_iterate_zero (l : ℝ) (k : ℕ) : (Mmap l)^[k] (0, 0) = (0, 0) := by
  induction k with
  | zero => rfl
  | succ n ih => rw [Function.iterate_succ_apply', ih, Mmap_fix_zero]

/-- **★ THE all-`ℝ²` COVERING IS FALSE (the `(0,0)` counterexample).**
For `l > 0`, the orbit of the cusp tip `(0,0)` never enters `{1/l³ ≤ Pgen}` (it stays at `Pgen = 0`),
so no `k` witnesses a hit.  Hence B2's `super_arc_hit_within_q` on all of `ℝ²` is false. -/
theorem superarc_univ_is_false (l : ℝ) (hl0 : 0 < l) :
    ¬ ∃ k, (Mmap l)^[k] (0, 0) ∈ {x : ℝ × ℝ | 1 / l ^ 3 ≤ Pgen l x} := by
  rintro ⟨k, hk⟩
  rw [Set.mem_setOf_eq, Mmap_iterate_zero] at hk
  have hP0 : Pgen l (0, 0) = 0 := by simp [Pgen]
  rw [hP0] at hk
  have hpos : (0:ℝ) < 1 / l ^ 3 := by positivity
  linarith [hk, hpos]

/-! ## §8.  AXIOM AUDIT.

`cos_grid_hit`, `orbit_hit_of_realization`, `arc_coverage_ineq`, `cos_sq_lt`,
`wide_arc_translates_cover_on`, `Mmap_iterate_zero`, `superarc_univ_is_false`,
`Mmap_preserves_E` are sorry-free; expect `[propext, Classical.choice, Quot.sound]`.
`orbit_hit_in_corridor` / `SuperArcCover_corridor` carry the SINGLE named residual
`pgen_orbit_realization` (the realization bridge), so they show `sorryAx` until Aristotle
discharges it. -/

#print axioms cos_grid_hit
#print axioms orbit_hit_of_realization
#print axioms arc_coverage_ineq
#print axioms cos_sq_lt
#print axioms wide_arc_translates_cover_on
#print axioms superarc_univ_is_false
#print axioms Mmap_preserves_E
#print axioms SuperArcCover_corridor

end

end MuCloseHSuperArc
