/-
SCAT-1 Lemma 3.1, abstract reflection core (step (ii) only).

Source: research_notes/rh_goals_2026-08-14/lane_g/SCAT1_PHIQ_ZERO_CERTIFIER_SOL.md,
Lemma 3.1 step (ii): if `φ(s) · φ(1 − s) = 1` as meromorphic functions and
`φ` has a pole of order `m` at `s*`, then `φ` has a zero of order `m` at
`1 − s*`.  NOTE the reflection is `s ↦ 1 − s` (NOT `1 − conj s`); no
conjugation appears anywhere.

Formalization choices:
* "meromorphic on an open set `U` stable under `s ↦ 1 − s`" is carried as
  `MeromorphicOn φ U`, `IsOpen U`, and `∀ s ∈ U, (1 - s) ∈ U`.
* "`φ(s)·φ(1−s) = 1` as meromorphic functions / away from poles" is carried
  as the identity holding on `U` off a discrete exceptional set; concretely we
  assume it frequently near every point:
  `∀ s ∈ U, ∀ᶠ z in 𝓝[≠] s, φ z * φ (1 - z) = 1`.
  (This is the honest local content of the meromorphic identity and is what
  the order computation consumes.)
* "pole of order `m`" / "zero of order `m`" use the mathlib meromorphic
  order: `meromorphicOrderAt φ s = (n : WithTop ℤ)` with `n = -m` for the
  pole and `n = m` for the zero.  If the ambient mathlib still uses the older
  spelling `(hφ.meromorphicAt).order`, adapt accordingly — the mathematical
  statement must stay exactly this one.
-/
import Mathlib

open Filter Topology

/-- **SCAT-1 Lemma 3.1, abstract reflection core.**
Let `φ` be meromorphic on an open set `U ⊆ ℂ` stable under `s ↦ 1 − s`,
satisfying `φ(s) · φ(1 − s) = 1` away from poles (frequently near every point
of `U`).  If `φ` has a pole of order `m ≥ 1` at `s* ∈ U`, then `φ` has a zero
of order `m` at `1 − s*`.

Note: the hypotheses `IsOpen U` and `1 ≤ m` are kept as stated, but the proof
does not need them (the argument is purely local at `s*` and works for any
integer order). -/
theorem scat1_lemma31_reflection
    (U : Set ℂ) (hU : IsOpen U) (hUrefl : ∀ s ∈ U, (1 - s) ∈ U)
    (φ : ℂ → ℂ) (hφ : MeromorphicOn φ U)
    (hfe : ∀ s ∈ U, ∀ᶠ z in 𝓝[≠] s, φ z * φ (1 - z) = 1)
    (sstar : ℂ) (hs : sstar ∈ U)
    (m : ℕ) (hm : 1 ≤ m)
    (hpole : meromorphicOrderAt φ sstar = (-(m : ℤ) : WithTop ℤ)) :
    meromorphicOrderAt φ (1 - sstar) = ((m : ℤ) : WithTop ℤ) := by
  set g : ℂ → ℂ := fun z => φ (1 - z) with hgdef
  have hanal : AnalyticAt ℂ (fun z : ℂ => 1 - z) sstar := by fun_prop
  have hderiv : HasDerivAt (fun z : ℂ => 1 - z) (-1) sstar := by
    simpa using (hasDerivAt_id sstar).const_sub (1 : ℂ)
  have hd : deriv (fun z : ℂ => 1 - z) sstar ≠ 0 := by
    rw [hderiv.deriv]; norm_num
  -- order of `g` at `sstar` equals order of `φ` at `1 - sstar`
  have horder : meromorphicOrderAt g sstar = meromorphicOrderAt φ (1 - sstar) := by
    simpa [hgdef, Function.comp_def] using
      meromorphicOrderAt_comp_of_deriv_ne_zero (f := φ) hanal hd
  -- meromorphy
  have hφs : MeromorphicAt φ sstar := hφ sstar hs
  have hφr : MeromorphicAt φ (1 - sstar) := hφ (1 - sstar) (hUrefl sstar hs)
  have hgm : MeromorphicAt g sstar := by
    have := (meromorphicAt_comp_iff_of_deriv_ne_zero (f := φ) hanal hd).mpr hφr
    simpa [hgdef, Function.comp_def] using this
  -- the functional equation gives order 0 for the product
  have hprod : meromorphicOrderAt (φ * g) sstar = 0 := by
    have h1 : (φ * g) =ᶠ[𝓝[≠] sstar] (fun _ => (1 : ℂ)) := by
      filter_upwards [hfe sstar hs] with z hz using hz
    rw [meromorphicOrderAt_congr h1]
    simp [meromorphicOrderAt_const]
  rw [meromorphicOrderAt_mul hφs hgm, hpole, horder] at hprod
  -- solve for the order
  rcases eq_or_ne (meromorphicOrderAt φ (1 - sstar)) ⊤ with h | h
  · rw [h] at hprod; simp at hprod
  · obtain ⟨n, hn⟩ := WithTop.ne_top_iff_exists.mp h
    rw [← hn] at hprod ⊢
    norm_cast at hprod ⊢
    omega
