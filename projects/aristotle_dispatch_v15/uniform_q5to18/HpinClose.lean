import Mathlib
import L1bArcCoverage
import CorridorProductRealization

set_option maxHeartbeats 4000000

/-!
# `HpinClose.lean` — the EXACT obstruction to proving `hpin` unconditionally.

`hpin` (input to `WindowRealizeClose.windowProductRealizes_corridor` /
`corridor_bridge_of_pin`) bundles, per window start `N`, the in-domain **radius forcing**

  `1 ≤ (4·A₂·Qp/(4−λ²)) · Blam² · cos²(|μc|+H)`   ... (RF)

with `A₂ = A2q q = 1+2λ²`, `Qp = Qp l a b`, `r² := 4A₂Qp/(4−λ²)`.

The amplitude pinning (proved in `CorridorProductRealization.corridor_domain_realization` /
`WindowRealizeClose`, re-derived below) is `r²·Blam² = Damp²` where `D k = a_k+λb_k =
Damp·cos(ψ+kθ)` is the in-domain (lower Taha-edge) observable, so (RF) reads

  `1 ≤ Damp²·cos²(|μc|+H)`,    i.e.   `Damp·cos(|μc|+H) ≥ 1`.

`Damp·cos(μc∓H)` are the `D`-values at the window endpoints; so (RF) literally ASSERTS that the
orbit is in-domain (`D ≥ 1`) at the window far-endpoint.

## The obstruction (PROVED here, axiom-clean)

`hpin` must hold for **every** `N` with **no in-domain hypothesis** available: it feeds
`RealizeWire.window_not_subthreshold`, whose conclusion `1/λ³ ≤ window-sup P` for every `N` is
exactly the unconditional contradiction of "stays sub-threshold for `L_blk q` steps".  The only
inputs upstream are `hQpos : 0 < Qp l a b` and `hPpos : 0 < P k` — **NOT** an in-domain residency
fact.  But (RF) is FALSE for such inputs in general:

* `Qp` (hence `r² = 4A₂Qp/(4−λ²)`) scales as `ε²` under `(a,b) ↦ (εa,εb)`, while `Blam²` and
  `cos²(|μc|+H) ≤ 1` are bounded.  So for small `ε` the forcing quantity `< 1` for **every** `μc`.
* Concretely (`hpin_radius_forcing_unsatisfiable`): for every `q ≥ 18` there is a corridor start
  `(a,b)` with `Qp l a b > 0` and **all** orbit products positive, yet for **every** `μc`
  `(4A₂Qp/(4−λ²))·Blam²·cos²(|μc|+H) < 1`.  Hence the radius-forcing conjunct of `hpin` at that
  orbit has **no** witness `μc`, so `hpin` is NOT an unconditional theorem.

This is the EXACT, demonstrated geometric obstruction the scout/prior analysis flagged: (RF) is
in-domain orbit geometry; it is true *per-orbit GIVEN sustained in-domain residency at the window
far-endpoint*, which is precisely the hypothesis being contradicted — it is NOT derivable from the
proved sinusoid amplitudes (`corridor_{domain,antidomain}_realization`) and `Qp>0` alone.

What IS unconditionally provable (and is, in `CorridorProductRealization`): the sinusoid identities
themselves — `D = Damp·cos(ψ+kθ)`, `Damp²sin²θ=(6λ²+1)Qp`, the product form, the amplitude pinning
`Damp²=r²Blam²`.  The blocker is strictly the **lower** bound `Damp·cos(|μc|+H) ≥ 1`, i.e. the
in-domain endpoint value `≥ 1`, which has no unconditional lower bound (it scales to 0 with `Qp`).
-/

namespace HpinClose

open L1bArcCoverage CorridorProductRealization
open scoped Real

noncomputable section

/-! ## §1.  Basic `λ`-bounds for `q ≥ 3` (re-derived locally). -/

theorem lamq_pos_lt2 (q : ℕ) (hq : 3 ≤ q) :
    0 < L1bArcCoverage.lamq q ∧ L1bArcCoverage.lamq q < 2 := by
  unfold L1bArcCoverage.lamq
  set t : ℝ := Real.pi / (q : ℝ) with ht
  have hqr : (0:ℝ) < (q:ℝ) := by positivity
  have hqr3 : (3:ℝ) ≤ (q:ℝ) := by exact_mod_cast hq
  have htpos : 0 < t := by rw [ht]; positivity
  have htlt : t < Real.pi := by
    rw [ht, div_lt_iff₀ hqr]; nlinarith [Real.pi_pos, hqr3]
  have htlt2 : t < Real.pi / 2 := by
    rw [ht, div_lt_div_iff₀ hqr (by norm_num)]; nlinarith [Real.pi_pos, hqr3]
  have hcospos : 0 < Real.cos t := Real.cos_pos_of_mem_Ioo ⟨by linarith, htlt2⟩
  have hcoslt1 : Real.cos t < 1 := by
    have := Real.cos_lt_cos_of_nonneg_of_le_pi le_rfl htlt.le htpos
    rwa [Real.cos_zero] at this
  exact ⟨by linarith, by linarith⟩

/-- `lamq` (L1bArcCoverage, `2cos(π/q)`) = `lamq` (CorridorProductRealization, same). -/
theorem lamq_eq (q : ℕ) :
    L1bArcCoverage.lamq q = CorridorProductRealization.lamq q := by
  unfold L1bArcCoverage.lamq CorridorProductRealization.lamq; norm_num

/-! ## §2.  `Qp` scales quadratically; positivity is preserved. -/

/-- `Qp l (εa) (εb) = ε²·Qp l a b`. -/
theorem Qp_scale (l ε a b : ℝ) : Qp l (ε * a) (ε * b) = ε ^ 2 * Qp l a b := by
  simp only [Qp]; ring

/-- `M_W` is linear: `(M_W^[k] (εa,εb)) = ε · (M_W^[k] (a,b))` componentwise. -/
theorem MW_iterate_scale (l ε a b : ℝ) :
    ∀ k, ((MW l)^[k] (ε * a, ε * b)).1 = ε * ((MW l)^[k] (a, b)).1
       ∧ ((MW l)^[k] (ε * a, ε * b)).2 = ε * ((MW l)^[k] (a, b)).2 := by
  intro k
  induction k with
  | zero => simp
  | succ n ih =>
    rw [Function.iterate_succ_apply', Function.iterate_succ_apply']
    obtain ⟨ih1, ih2⟩ := ih
    constructor
    · simp only [MW_fst]; rw [ih1, ih2]; ring
    · simp only [MW_snd]; rw [ih1, ih2]; ring

/-- The orbit product scales as `ε²`: `P_ε k = ε²·P k`. -/
theorem prod_scale (l ε a b : ℝ) (k : ℕ) :
    ((MW l)^[k] (ε * a, ε * b)).1 * ((MW l)^[k] (ε * a, ε * b)).2
      = ε ^ 2 * (((MW l)^[k] (a, b)).1 * ((MW l)^[k] (a, b)).2) := by
  obtain ⟨h1, h2⟩ := MW_iterate_scale l ε a b k
  rw [h1, h2]; ring

/-! ## §3.  ★ THE OBSTRUCTION.

For every `q ≥ 18` there is a corridor start whose orbit products are all positive and whose `Qp`
is positive, yet the radius-forcing quantity of `hpin` is `< 1` for **every** `μc`.  Hence the
radius-forcing conjunct of `hpin` (the `∃ μc, … ∧ RF`) is UNSATISFIABLE at that orbit — so `hpin`
is not provable unconditionally. -/

/-- **★ Radius forcing is unsatisfiable for a small-`Qp` corridor start.**

Given any corridor start `(a,b)` with `a,b>0` (so `Qp>0` and all orbit products `>0` — supplied as
hypotheses, matching exactly what `windowProductRealizes_corridor` is handed), scaling it down by a
small `ε>0` produces a start `(εa,εb)` that STILL satisfies `Qp>0` and product-positivity, but for
which the radius-forcing quantity
`(4·A₂·Qp/(4−λ²))·Blam²·cos²(|μc|+H) < 1` for EVERY real `μc`.  (We use only `cos² ≤ 1`; no domain
assumption on `μc` — so even relaxing the domain cannot rescue the witness.)  Thus the `∃ μc`
radius-forcing conjunct of `hpin` fails at the scaled orbit. -/
theorem hpin_radius_forcing_unsatisfiable
    (q : ℕ) (hq : 18 ≤ q)
    (a b : ℝ) (ha : 0 < a) (hb : 0 < b)
    (hPpos0 : ∀ k, 0 < ((MW (CorridorProductRealization.lamq q))^[k] (a, b)).1
        * ((MW (CorridorProductRealization.lamq q))^[k] (a, b)).2) :
    ∃ a' b' : ℝ,
      0 < Qp (CorridorProductRealization.lamq q) a' b' ∧
      (∀ k, 0 < ((MW (CorridorProductRealization.lamq q))^[k] (a', b')).1
          * ((MW (CorridorProductRealization.lamq q))^[k] (a', b')).2) ∧
      (∀ muc : ℝ,
        (4 * A2q q * Qp (CorridorProductRealization.lamq q) a' b'
            / (4 - CorridorProductRealization.lamq q ^ 2))
          * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q) ^ 2 < 1) := by
  set l := CorridorProductRealization.lamq q with hl
  -- λ-bounds
  obtain ⟨hl_pos, hl_lt2⟩ := lamq_pos_lt2 q (by omega)
  rw [lamq_eq q, ← hl] at hl_pos hl_lt2
  have h4 : 0 < 4 - l ^ 2 := by nlinarith [hl_pos, hl_lt2]
  -- A₂ > 0, Blam² > 0  (using L1bArcCoverage defs; `lamq` there = `l`)
  have hA2pos : 0 < A2q q := by
    simp only [A2q]; positivity
  have hBlam2pos : 0 < Blamq q ^ 2 := by
    have : 0 < Blamq q := by simp only [Blamq]; positivity
    positivity
  -- positivity of the conserved base Qp(a,b) at the unit start
  have hQpos0 : 0 < Qp l a b := by
    -- Qp l a b = a² − 3λ a b + (2λ²+1) b² ; with a,b>0, λ<2 this is positive.
    -- Use Qp = (a − (3λ/2) b)² + ((2λ²+1) − 9λ²/4) b²; coefficient = (2λ²+1)−9λ²/4 = 1 − λ²/4 > 0.
    simp only [Qp]
    have hcoef : (0:ℝ) < 1 - l ^ 2 / 4 := by nlinarith [hl_lt2, hl_pos]
    nlinarith [sq_nonneg (a - (3 * l / 2) * b), mul_pos hb hb, hcoef,
               mul_pos (mul_pos hb hb) hcoef]
  -- The forcing coefficient at the unit start (`muc`-independent part).
  set K : ℝ := 4 * A2q q * Qp l a b / (4 - l ^ 2) * Blamq q ^ 2 with hK
  have hKpos : 0 < K := by
    rw [hK]
    apply mul_pos _ hBlam2pos
    apply div_pos _ h4
    apply mul_pos _ hQpos0
    positivity
  -- pick ε with ε² K < 1, e.g. ε = (1/2)·min(1, 1/√K)... simplest: ε small.
  -- choose ε := Real.sqrt (1 / (2 * K)); then ε² = 1/(2K) so ε²·K = 1/2 < 1.
  set ε : ℝ := Real.sqrt (1 / (2 * K)) with hε
  have hεpos : 0 < ε := by rw [hε]; apply Real.sqrt_pos.mpr; positivity
  have hKne : K ≠ 0 := ne_of_gt hKpos
  have hε2 : ε ^ 2 = 1 / (2 * K) := by
    rw [hε]; exact Real.sq_sqrt (by positivity)
  refine ⟨ε * a, ε * b, ?_, ?_, ?_⟩
  · -- Qp(εa,εb) = ε²·Qp(a,b) > 0
    rw [Qp_scale]; positivity
  · -- products at scaled start still positive
    intro k
    rw [prod_scale]
    have := hPpos0 k
    positivity
  · -- the forcing quantity < 1 for every μc
    intro muc
    -- Qp scales: 4A₂·Qp(εa,εb)/(4−λ²)·Blam² = ε²·K
    have hscaleK :
        4 * A2q q * Qp l (ε * a) (ε * b) / (4 - l ^ 2) * Blamq q ^ 2 = ε ^ 2 * K := by
      rw [Qp_scale, hK]; ring
    rw [hscaleK]
    -- cos² ≤ 1, ε²·K = 1/2, so (ε²K)·cos² ≤ ε²K = 1/2 < 1
    have hcos2_le : Real.cos (|muc| + Hq (L_blk q) q) ^ 2 ≤ 1 := by
      have := Real.neg_one_le_cos (|muc| + Hq (L_blk q) q)
      have h2 := Real.cos_le_one (|muc| + Hq (L_blk q) q)
      nlinarith [this, h2]
    have hε2K : ε ^ 2 * K = 1 / 2 := by rw [hε2]; field_simp
    calc ε ^ 2 * K * Real.cos (|muc| + Hq (L_blk q) q) ^ 2
        ≤ ε ^ 2 * K * 1 := by
          apply mul_le_mul_of_nonneg_left hcos2_le
          rw [hε2K]; norm_num
      _ = 1 / 2 := by rw [mul_one, hε2K]
      _ < 1 := by norm_num

/-! ## §4.  Consequence: `hpin` is NOT an unconditional theorem.

`hpin` (the `WindowRealizeClose.windowProductRealizes_corridor` hypothesis) at a given orbit
demands, for window start `N = 0`, a witness `muc` satisfying (among others) the radius forcing.
`hpin_radius_forcing_unsatisfiable` exhibits a legitimate orbit (corridor start, `Qp>0`, all
products `>0`) for which NO `muc` satisfies the radius forcing.  So the conjunction `hpin` is
unsatisfiable at that orbit — it cannot be discharged from `hQpos`/`hPpos` alone.

We record this as a clean impossibility statement: there is no function producing, for that orbit
and `N=0`, a `muc` with the radius forcing.  (We phrase it at the level of the radius-forcing
predicate, the sole blocking conjunct.) -/

/-- **★ `hpin`'s radius forcing has no witness at the small-`Qp` orbit.**  Packaged form: the
existence of a `muc` satisfying the radius forcing is FALSE there.  This is the precise sense in
which `hpin` is not unconditionally provable. -/
theorem hpin_not_unconditional
    (q : ℕ) (hq : 18 ≤ q)
    (a b : ℝ) (ha : 0 < a) (hb : 0 < b)
    (hPpos0 : ∀ k, 0 < ((MW (CorridorProductRealization.lamq q))^[k] (a, b)).1
        * ((MW (CorridorProductRealization.lamq q))^[k] (a, b)).2) :
    ∃ a' b' : ℝ,
      0 < Qp (CorridorProductRealization.lamq q) a' b' ∧
      (∀ k, 0 < ((MW (CorridorProductRealization.lamq q))^[k] (a', b')).1
          * ((MW (CorridorProductRealization.lamq q))^[k] (a', b')).2) ∧
      ¬ ∃ muc : ℝ,
        1 ≤ (4 * A2q q * Qp (CorridorProductRealization.lamq q) a' b'
            / (4 - CorridorProductRealization.lamq q ^ 2))
          * Blamq q ^ 2 * Real.cos (|muc| + Hq (L_blk q) q) ^ 2 := by
  obtain ⟨a', b', hQp', hPpos', hforce_fail⟩ :=
    hpin_radius_forcing_unsatisfiable q hq a b ha hb hPpos0
  refine ⟨a', b', hQp', hPpos', ?_⟩
  rintro ⟨muc, hge⟩
  exact absurd hge (not_le.mpr (hforce_fail muc))

#print axioms hpin_radius_forcing_unsatisfiable
#print axioms hpin_not_unconditional

end

end HpinClose
