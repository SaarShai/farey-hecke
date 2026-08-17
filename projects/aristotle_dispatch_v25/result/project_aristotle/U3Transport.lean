import Mathlib

/-!
# U3 transport — the divisor-bookkeeping core (v25 dispatch)

Source obligation: `U3` of
`research_notes/rh_goals_2026-08-14/lane_g/LAW_T2_DETERMINANT.md` §5.2
(= `C14` of `LAW_ANCHOR_T1_THETA.md`, = `G6`/`N2` of `M1F_EISENSTEIN_DERIVATION.md`),
worked out in `lane_g/LAW_U3_TRANSPORT.md`, and named as recommended lane #2
("`U3` (Aristotle-able finite piece) … textbook-shaped") in
`lane_g/LAW_SH_EFFECTIVIZATION_SKELETON.md` §7.

**What is formalized here.** Only the *algebraic implication chain* of the
transport: order-of-vanishing arithmetic for meromorphic germs, run against the
Selberg functional equation `Z(1-s) = κ(s) Z(s)` (Teo, LMP 110 (2020),
Prop. 2.5) in the shape

```
    ord_{s₀} Z(1 - ·)  =  ord_{s₀} κ  +  ord_{s₀} Z
```

with **every analytic input carried as an explicit hypothesis**:

* `Z` holomorphic and non-vanishing at the reflected point `1 - s₀`
  (Lemma U3-A of the source note) — hypothesis `hZfree`;
* every factor of `κ` other than `φ = det Φ` finite and non-zero at `s₀`
  (Lemma U3-B, the Barnes/`Γ`/`sin`-power factors, all of whose divisors are
  real) — hypotheses `hunit`, `hc`, `hc0`;
* the functional equation itself — hypothesis `hFE`, as an eventual equality on
  a punctured neighbourhood (faithful: `κ` carries fractional powers with a
  branch choice, and the identity is used only off the real axis).

Nothing about `ζ`, `Λ`, Eisenstein series, Barnes `Γ₂`, the trace formula, or
the actual meromorphic continuation of `Z_Γ` is asserted. See `SKIPPED.md`.

**The `Γ_θ` specialization** (§3 of the source note) is included in the same
algebraic style: `det Φ_θ = g² E` with `g = Λ(2s-1)/Λ(2s)`, so the divisor of
`det Φ_θ` at `s₀` is `2·(ord Λ at 2s₀-1) - 2·(ord Λ at 2s₀)` whenever `E` is a
unit there. The two instances the note uses are stated separately: the order-`2m`
**pole** at `s = ρ/2` (denominator vanishes) and the order-`2m` **zero** at the
conjugate point `1 - conj(ρ/2) = (1+ρ)/2` (numerator vanishes).

All statements are hypothesis-complete, and all proofs are now supplied: the
file contains no `sorry`.
-/

open Filter Topology

namespace U3

/-! ### Private helpers -/

/-- Coercion helper: doubling in `WithTop ℤ` is the coercion of doubling in `ℤ`. -/
private lemma withTop_two_mul (a : ℤ) :
    ((2 : ℕ) : WithTop ℤ) * ((a : ℤ) : WithTop ℤ) = ((2 * a : ℤ) : WithTop ℤ) := by
  rw [show ((2 : ℕ) : WithTop ℤ) = ((2 : ℤ) : WithTop ℤ) by norm_cast, ← WithTop.coe_mul]

/-- Order arithmetic under precomposition with an affine map (auxiliary form,
used before `meromorphicOrderAt_affine` is available). -/
private lemma meromorphicOrderAt_affine_aux (F : ℂ → ℂ) (a b s₀ : ℂ) (ha : a ≠ 0) :
    meromorphicOrderAt (fun s => F (a * s + b)) s₀ = meromorphicOrderAt F (a * s₀ + b) := by
  have hg : AnalyticAt ℂ (fun s : ℂ => a * s + b) s₀ := by fun_prop
  have hd : deriv (fun s : ℂ => a * s + b) s₀ = a :=
    (((hasDerivAt_id s₀).const_mul a).add_const b).deriv.trans (by simp)
  have := meromorphicOrderAt_comp_of_deriv_ne_zero (f := F) hg (by rw [hd]; exact ha)
  simpa [Function.comp_def] using this

/-- Meromorphy is preserved by precomposition with an affine map. -/
private lemma meromorphicAt_affine_comp (F : ℂ → ℂ) (a b s₀ : ℂ)
    (hF : MeromorphicAt F (a * s₀ + b)) : MeromorphicAt (fun s => F (a * s + b)) s₀ := by
  have hg : AnalyticAt ℂ (fun s : ℂ => a * s + b) s₀ := by fun_prop
  have := MeromorphicAt.comp_analyticAt (f := F) (g := fun s : ℂ => a * s + b) (x := s₀) hF hg
  simpa [Function.comp_def] using this

/-- An analytic function that does not vanish has order `0`. -/
private lemma meromorphicOrderAt_eq_zero_of_analytic_of_ne_zero {F : ℂ → ℂ} {x : ℂ}
    (hF : AnalyticAt ℂ F x) (hF0 : F x ≠ 0) : meromorphicOrderAt F x = 0 := by
  rw [hF.meromorphicOrderAt_eq, analyticOrderAt_eq_zero.mpr (Or.inr hF0)]
  simp

/-! ## 1. Order arithmetic for meromorphic germs -/

/-- **Reflection.** Precomposition with `s ↦ 1 - s` (an affine map of nonzero
derivative) moves the order to the reflected point. This is the step that turns
`ord_{s₀} Z(1-·)` into `ord_{1-s₀} Z`. -/
theorem meromorphicOrderAt_reflect (Z : ℂ → ℂ) (s₀ : ℂ) :
    meromorphicOrderAt (fun s => Z (1 - s)) s₀ = meromorphicOrderAt Z (1 - s₀) := by
  have := meromorphicOrderAt_affine_aux Z (-1) 1 s₀ (by norm_num)
  simpa [neg_mul, sub_eq_neg_add, add_comm] using this

/-- **Affine precomposition**, the general form used for `Λ(2s-1)` and `Λ(2s)`. -/
theorem meromorphicOrderAt_affine (F : ℂ → ℂ) (a b s₀ : ℂ) (ha : a ≠ 0) :
    meromorphicOrderAt (fun s => F (a * s + b)) s₀ = meromorphicOrderAt F (a * s₀ + b) :=
  meromorphicOrderAt_affine_aux F a b s₀ ha

/-- **Lemma U3-B, abstracted.** A factor that is analytic and non-vanishing at
`s₀` does not move the order. Here `κ` is the functional-equation factor and `c`
collects the Barnes, elliptic-`sin`-power and parabolic-`Γ` factors, all of whose
divisors are real, hence units at any non-real `s₀`. -/
theorem meromorphicOrderAt_eq_of_unit_factor (c φ κ : ℂ → ℂ) (s₀ : ℂ)
    (hc : AnalyticAt ℂ c s₀) (hc0 : c s₀ ≠ 0)
    (hunit : κ =ᶠ[𝓝[≠] s₀] fun s => c s * φ s) :
    meromorphicOrderAt κ s₀ = meromorphicOrderAt φ s₀ := by
  rw [meromorphicOrderAt_congr hunit]
  exact meromorphicOrderAt_mul_of_ne_zero hc hc0

/-- **Quotient order.** `ord (F/G) = ord F - ord G`, in the form needed for
`g(s) = Λ(2s-1)/Λ(2s)`; both orders are assumed finite (neither germ vanishes
identically). -/
theorem meromorphicOrderAt_div (F G : ℂ → ℂ) (s₀ : ℂ)
    (hF : MeromorphicAt F s₀) (hG : MeromorphicAt G s₀)
    (hFt : meromorphicOrderAt F s₀ ≠ ⊤) (hGt : meromorphicOrderAt G s₀ ≠ ⊤) :
    meromorphicOrderAt (fun s => F s / G s) s₀ =
      meromorphicOrderAt F s₀ + -meromorphicOrderAt G s₀ := by
  have h : (fun s => F s / G s) = F * G⁻¹ := by funext s; simp [div_eq_mul_inv]
  rw [h, meromorphicOrderAt_mul hF hG.inv, meromorphicOrderAt_inv]

/-- A positive order at a point where the function is analytic forces a zero
there. (Used to convert "order `2m`" into the statement "`Z_{Γ_θ}` has a zero at
`s_∞`" that the Hurwitz step of `(T2′)` consumes.) -/
theorem zero_of_meromorphicOrderAt_pos (Z : ℂ → ℂ) (s₀ : ℂ)
    (hZ : AnalyticAt ℂ Z s₀) (h : 0 < meromorphicOrderAt Z s₀) :
    Z s₀ = 0 := by
  have h1 := tendsto_zero_of_meromorphicOrderAt_pos h
  have h2 : Filter.Tendsto Z (𝓝[≠] s₀) (𝓝 (Z s₀)) :=
    hZ.continuousAt.continuousWithinAt.tendsto
  exact tendsto_nhds_unique h2 h1

/-! ## 2. The transport, as an algebraic implication chain

This is Theorem U3 of `LAW_U3_TRANSPORT.md` §2.6, with its two analytic inputs
(Lemma U3-A: `Z` is a unit at the reflected point; Lemma U3-B: `κ/φ` is a unit)
demoted to hypotheses. -/

/-- **THEOREM U3 (algebraic core).** Given the Selberg functional equation
`Z(1-s) = κ(s) Z(s)` near `s₀`, a factorization `κ = c · φ` with `c` a unit at
`s₀`, a pole of `φ` of order `m ≥ 1` at `s₀`, and `Z` a unit at the reflected
point `1 - s₀`, the germ of `Z` at `s₀` has order exactly `m`. -/
theorem transport_order (Z κ φ c : ℂ → ℂ) (s₀ : ℂ) (m : ℕ) (hm : 1 ≤ m)
    (hZ : MeromorphicAt Z s₀)
    (hZne : meromorphicOrderAt Z s₀ ≠ ⊤)
    (hκ : MeromorphicAt κ s₀)
    (hFE : (fun s => Z (1 - s)) =ᶠ[𝓝[≠] s₀] fun s => κ s * Z s)
    (hunit : κ =ᶠ[𝓝[≠] s₀] fun s => c s * φ s)
    (hc : AnalyticAt ℂ c s₀) (hc0 : c s₀ ≠ 0)
    (hpole : meromorphicOrderAt φ s₀ = ((-(m : ℤ) : ℤ) : WithTop ℤ))
    (hZfree : meromorphicOrderAt Z (1 - s₀) = 0) :
    meromorphicOrderAt Z s₀ = ((m : ℤ) : WithTop ℤ) := by
  have hkord : meromorphicOrderAt κ s₀ = ((-(m : ℤ) : ℤ) : WithTop ℤ) := by
    rw [meromorphicOrderAt_eq_of_unit_factor c φ κ s₀ hc hc0 hunit, hpole]
  have key : meromorphicOrderAt (fun s => Z (1 - s)) s₀
      = meromorphicOrderAt κ s₀ + meromorphicOrderAt Z s₀ := by
    rw [meromorphicOrderAt_congr hFE]
    exact meromorphicOrderAt_mul hκ hZ
  rw [meromorphicOrderAt_reflect, hZfree, hkord] at key
  lift meromorphicOrderAt Z s₀ to ℤ using hZne with n hn
  rw [← WithTop.coe_add, ← WithTop.coe_zero, WithTop.coe_inj] at key
  rw [WithTop.coe_inj]
  omega

/-- **No-cancellation corollary.** Under the hypotheses of `transport_order`
with `m ≥ 2`, the order of `Z` at `s₀` is at least `2` — the exact input the
Hurwitz step of `(T2′)` (`LAW_T2_DETERMINANT.md` §3.2) consumes. -/
theorem transport_order_ge_two (Z κ φ c : ℂ → ℂ) (s₀ : ℂ) (m : ℕ) (hm : 2 ≤ m)
    (hZ : MeromorphicAt Z s₀)
    (hZne : meromorphicOrderAt Z s₀ ≠ ⊤)
    (hκ : MeromorphicAt κ s₀)
    (hFE : (fun s => Z (1 - s)) =ᶠ[𝓝[≠] s₀] fun s => κ s * Z s)
    (hunit : κ =ᶠ[𝓝[≠] s₀] fun s => c s * φ s)
    (hc : AnalyticAt ℂ c s₀) (hc0 : c s₀ ≠ 0)
    (hpole : meromorphicOrderAt φ s₀ = ((-(m : ℤ) : ℤ) : WithTop ℤ))
    (hZfree : meromorphicOrderAt Z (1 - s₀) = 0) :
    ((2 : ℤ) : WithTop ℤ) ≤ meromorphicOrderAt Z s₀ := by
  have h := transport_order Z κ φ c s₀ m (le_trans (by norm_num) hm) hZ hZne hκ hFE hunit hc hc0
    hpole hZfree
  rw [h, WithTop.coe_le_coe]
  exact_mod_cast hm

/-! ## 3. The `Γ_θ` divisor bookkeeping

`LAW_ANCHOR_T1_THETA.md` (DET), `PROVED`:
`det Φ_θ(s) = g(s)² E(s)` with `g(s) = Λ(2s-1)/Λ(2s)` and `E` a rational
function of `2^s` whose zeros lie on `Re s = 1` and whose poles lie on
`Re s = 0`. Both instances below take "`E` is a unit at the point" as a
hypothesis rather than re-deriving it. -/

/-- **Order of `det Φ_θ = g² E`** in terms of the orders of `Λ` at the two
argument points. -/
theorem order_detPhi (Lam E : ℂ → ℂ) (s₀ : ℂ)
    (hnum : MeromorphicAt Lam (2 * s₀ - 1)) (hden : MeromorphicAt Lam (2 * s₀))
    (hnumt : meromorphicOrderAt Lam (2 * s₀ - 1) ≠ ⊤)
    (hdent : meromorphicOrderAt Lam (2 * s₀) ≠ ⊤)
    (hE : AnalyticAt ℂ E s₀) (hE0 : E s₀ ≠ 0) :
    meromorphicOrderAt (fun s => (Lam (2 * s - 1) / Lam (2 * s)) ^ 2 * E s) s₀ =
      (2 : ℕ) * (meromorphicOrderAt Lam (2 * s₀ - 1) + -meromorphicOrderAt Lam (2 * s₀)) := by
  have hA : MeromorphicAt (fun s => Lam (2 * s - 1)) s₀ := by
    have := meromorphicAt_affine_comp Lam 2 (-1) s₀ (by simpa [sub_eq_add_neg] using hnum)
    simpa [sub_eq_add_neg] using this
  have hB : MeromorphicAt (fun s => Lam (2 * s)) s₀ := by
    simpa using meromorphicAt_affine_comp Lam 2 0 s₀ (by simpa using hden)
  have hordA : meromorphicOrderAt (fun s => Lam (2 * s - 1)) s₀
      = meromorphicOrderAt Lam (2 * s₀ - 1) := by
    have := meromorphicOrderAt_affine Lam 2 (-1) s₀ (by norm_num)
    simpa [sub_eq_add_neg] using this
  have hordB : meromorphicOrderAt (fun s => Lam (2 * s)) s₀
      = meromorphicOrderAt Lam (2 * s₀) := by
    simpa using meromorphicOrderAt_affine Lam 2 0 s₀ (by norm_num)
  have hAB : MeromorphicAt (fun s => Lam (2 * s - 1) / Lam (2 * s)) s₀ := hA.div hB
  have hdiv : meromorphicOrderAt (fun s => Lam (2 * s - 1) / Lam (2 * s)) s₀
      = meromorphicOrderAt Lam (2 * s₀ - 1) + -meromorphicOrderAt Lam (2 * s₀) := by
    rw [meromorphicOrderAt_div _ _ _ hA hB (by rwa [hordA]) (by rwa [hordB]), hordA, hordB]
  have hcomm : (fun s => (Lam (2 * s - 1) / Lam (2 * s)) ^ 2 * E s)
      = E * (fun s => Lam (2 * s - 1) / Lam (2 * s)) ^ 2 := by
    funext s; simp [mul_comm]
  rw [hcomm, meromorphicOrderAt_mul_of_ne_zero hE hE0, meromorphicOrderAt_pow hAB, hdiv]

/-- **The anchor pole (T1).** At `s₀ = ρ/2` the denominator `Λ(2s)` vanishes to
order `m` and the numerator `Λ(2s-1)` is a unit, so `det Φ_θ` has a pole of
order exactly `2m`. -/
theorem order_detPhi_at_pole (Lam E : ℂ → ℂ) (s₀ : ℂ) (m : ℕ) (hm : 1 ≤ m)
    (hnum : AnalyticAt ℂ Lam (2 * s₀ - 1)) (hnum0 : Lam (2 * s₀ - 1) ≠ 0)
    (hden : MeromorphicAt Lam (2 * s₀))
    (hden_ord : meromorphicOrderAt Lam (2 * s₀) = ((m : ℤ) : WithTop ℤ))
    (hE : AnalyticAt ℂ E s₀) (hE0 : E s₀ ≠ 0) :
    meromorphicOrderAt (fun s => (Lam (2 * s - 1) / Lam (2 * s)) ^ 2 * E s) s₀ =
      ((-(2 * (m : ℤ)) : ℤ) : WithTop ℤ) := by
  have hnumord : meromorphicOrderAt Lam (2 * s₀ - 1) = 0 :=
    meromorphicOrderAt_eq_zero_of_analytic_of_ne_zero hnum hnum0
  rw [order_detPhi Lam E s₀ hnum.meromorphicAt hden (by rw [hnumord]; exact WithTop.zero_ne_top)
      (by rw [hden_ord]; exact WithTop.natCast_ne_top m) hE hE0, hnumord, hden_ord,
    zero_add, show -((m : ℤ) : WithTop ℤ) = ((-(m : ℤ) : ℤ) : WithTop ℤ) by norm_cast,
    withTop_two_mul]
  norm_num

/-- **The conjugate point (§3.3).** At `w = (1+ρ)/2` the numerator `Λ(2s-1)`
vanishes to order `m` and the denominator `Λ(2s)` is a unit, so `det Φ_θ` has a
zero of order exactly `2m`. This is the form in which the literature states the
transport ("zero of `φ` at `1 - β̄`"), so it is proved separately rather than
converted with a reality hypothesis on `φ`. -/
theorem order_detPhi_at_conjugate (Lam E : ℂ → ℂ) (w : ℂ) (m : ℕ) (hm : 1 ≤ m)
    (hnum : MeromorphicAt Lam (2 * w - 1))
    (hnum_ord : meromorphicOrderAt Lam (2 * w - 1) = ((m : ℤ) : WithTop ℤ))
    (hden : AnalyticAt ℂ Lam (2 * w)) (hden0 : Lam (2 * w) ≠ 0)
    (hE : AnalyticAt ℂ E w) (hE0 : E w ≠ 0) :
    meromorphicOrderAt (fun s => (Lam (2 * s - 1) / Lam (2 * s)) ^ 2 * E s) w =
      ((2 * (m : ℤ) : ℤ) : WithTop ℤ) := by
  have hdenord : meromorphicOrderAt Lam (2 * w) = 0 :=
    meromorphicOrderAt_eq_zero_of_analytic_of_ne_zero hden hden0
  rw [order_detPhi Lam E w hnum hden.meromorphicAt
      (by rw [hnum_ord]; exact WithTop.natCast_ne_top m) (by rw [hdenord]; exact WithTop.zero_ne_top)
      hE hE0, hnum_ord, hdenord,
    show -(0 : WithTop ℤ) = ((0 : ℤ) : WithTop ℤ) by norm_num, ← WithTop.coe_add,
    withTop_two_mul]
  norm_num

/-- **(3.1), pure arithmetic.** If `Re ρ = 1/2` then the conjugate-reflected
anchor point is `1 - conj(ρ/2) = (1+ρ)/2`. This is the identity that lets the
transport be applied in the form in which it is stated, using `Re ρ₁ = 1/2` and
nothing else. -/
theorem conj_reflect_of_re_half (ρ : ℂ) (hρ : ρ.re = 1 / 2) :
    1 - (starRingEnd ℂ) (ρ / 2) = (1 + ρ) / 2 := by
  apply Complex.ext <;> simp [Complex.div_re, Complex.div_im, Complex.normSq, hρ] <;> ring

/-! ## 4. The assembled anchor statement

Everything above, chained at `s₀ = ρ/2` with `φ = det Φ_θ = g² E`. -/

/-- **(U3-θ), algebraic form.** With the Selberg functional equation, the
`Γ_θ` scattering determinant in the form `g² E`, `Λ` vanishing to order `m ≥ 1`
at `2s₀`, and `Z` a unit at the reflected point, the Selberg zeta germ has order
exactly `2m` at `s₀`; in particular at least `2`. -/
theorem anchor_order (Z κ c Lam E : ℂ → ℂ) (s₀ : ℂ) (m : ℕ) (hm : 1 ≤ m)
    (hZ : MeromorphicAt Z s₀)
    (hZne : meromorphicOrderAt Z s₀ ≠ ⊤)
    (hκ : MeromorphicAt κ s₀)
    (hFE : (fun s => Z (1 - s)) =ᶠ[𝓝[≠] s₀] fun s => κ s * Z s)
    (hunit : κ =ᶠ[𝓝[≠] s₀] fun s =>
      c s * ((Lam (2 * s - 1) / Lam (2 * s)) ^ 2 * E s))
    (hc : AnalyticAt ℂ c s₀) (hc0 : c s₀ ≠ 0)
    (hnum : AnalyticAt ℂ Lam (2 * s₀ - 1)) (hnum0 : Lam (2 * s₀ - 1) ≠ 0)
    (hden : MeromorphicAt Lam (2 * s₀))
    (hden_ord : meromorphicOrderAt Lam (2 * s₀) = ((m : ℤ) : WithTop ℤ))
    (hE : AnalyticAt ℂ E s₀) (hE0 : E s₀ ≠ 0)
    (hZfree : meromorphicOrderAt Z (1 - s₀) = 0) :
    meromorphicOrderAt Z s₀ = ((2 * (m : ℤ) : ℤ) : WithTop ℤ) := by
  have hpole : meromorphicOrderAt
      (fun s => (Lam (2 * s - 1) / Lam (2 * s)) ^ 2 * E s) s₀
      = ((-((2 * m : ℕ) : ℤ) : ℤ) : WithTop ℤ) := by
    rw [order_detPhi_at_pole Lam E s₀ m hm hnum hnum0 hden hden_ord hE hE0]
    norm_cast
  have := transport_order Z κ (fun s => (Lam (2 * s - 1) / Lam (2 * s)) ^ 2 * E s) c s₀
    (2 * m) (by omega) hZ hZne hκ hFE hunit hc hc0 hpole hZfree
  rw [this]
  norm_cast

/-- The Hurwitz-consumable consequence: order at least `2`, hence (where `Z` is
analytic) an actual zero. -/
theorem anchor_zero (Z κ c Lam E : ℂ → ℂ) (s₀ : ℂ) (m : ℕ) (hm : 1 ≤ m)
    (hZan : AnalyticAt ℂ Z s₀)
    (hZne : meromorphicOrderAt Z s₀ ≠ ⊤)
    (hκ : MeromorphicAt κ s₀)
    (hFE : (fun s => Z (1 - s)) =ᶠ[𝓝[≠] s₀] fun s => κ s * Z s)
    (hunit : κ =ᶠ[𝓝[≠] s₀] fun s =>
      c s * ((Lam (2 * s - 1) / Lam (2 * s)) ^ 2 * E s))
    (hc : AnalyticAt ℂ c s₀) (hc0 : c s₀ ≠ 0)
    (hnum : AnalyticAt ℂ Lam (2 * s₀ - 1)) (hnum0 : Lam (2 * s₀ - 1) ≠ 0)
    (hden : MeromorphicAt Lam (2 * s₀))
    (hden_ord : meromorphicOrderAt Lam (2 * s₀) = ((m : ℤ) : WithTop ℤ))
    (hE : AnalyticAt ℂ E s₀) (hE0 : E s₀ ≠ 0)
    (hZfree : meromorphicOrderAt Z (1 - s₀) = 0) :
    Z s₀ = 0 ∧ ((2 : ℤ) : WithTop ℤ) ≤ meromorphicOrderAt Z s₀ := by
  have h := anchor_order Z κ c Lam E s₀ m hm hZan.meromorphicAt hZne hκ hFE hunit hc hc0
    hnum hnum0 hden hden_ord hE hE0 hZfree
  have h2 : ((2 : ℤ) : WithTop ℤ) ≤ meromorphicOrderAt Z s₀ := by
    rw [h, WithTop.coe_le_coe]
    omega
  have h0 : (0 : WithTop ℤ) < ((2 : ℤ) : WithTop ℤ) := by
    rw [← WithTop.coe_zero, WithTop.coe_lt_coe]; norm_num
  exact ⟨zero_of_meromorphicOrderAt_pos Z s₀ hZan (lt_of_lt_of_le h0 h2), h2⟩

end U3
