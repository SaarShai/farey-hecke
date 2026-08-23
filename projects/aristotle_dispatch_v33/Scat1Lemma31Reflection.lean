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
of order `m` at `1 − s*`. -/
theorem scat1_lemma31_reflection
    (U : Set ℂ) (hU : IsOpen U) (hUrefl : ∀ s ∈ U, (1 - s) ∈ U)
    (φ : ℂ → ℂ) (hφ : MeromorphicOn φ U)
    (hfe : ∀ s ∈ U, ∀ᶠ z in 𝓝[≠] s, φ z * φ (1 - z) = 1)
    (sstar : ℂ) (hs : sstar ∈ U)
    (m : ℕ) (hm : 1 ≤ m)
    (hpole : meromorphicOrderAt φ sstar = (-(m : ℤ) : WithTop ℤ)) :
    meromorphicOrderAt φ (1 - sstar) = ((m : ℤ) : WithTop ℤ) := by
  sorry
