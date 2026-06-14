import Mathlib
import BCZHeckeS1_trichotomy
import BCZHeckeUniformOnset
import UniformOnset_q5to18
import GenuineSelfMap
import GenuineClassDischarge
import GenuineMapFacts
import OnsetEquality

set_option maxHeartbeats 1600000

/-!
# Uniform discharge of the onset EQUALITY `X_Ω(q) = 1/λ³`

This file UNIFORMLY discharges the one remaining q-concrete input of the general onset
equality `OnsetEquality.Xomega_eq` — the cusp-tip active-branch identity
`hbranch_all : ∀ s ∈ (1/λ,1], branchIdx l s 0 (…) = m` — for EVERY Hecke index, not just
`q = 5`.

## The uniform crux (research note `onset_equality_resolution_2026-06-14.md §8`)

For the cusp tip `(s,0)` with `1/λ < s ≤ 1`, `L l s 0 i = s · cheb l (i+1)`.  The active
branch is the least `i ≥ 1` with `L_i ≤ 1`.  Two facts pin `branchIdx = m`:

* **`i = m` is active**: `L_m = s · cheb l (m+1) = s · 1 = s ≤ 1`  (from `Boundary.hq1`).
* **`1 ≤ i ≤ m−1` is NOT active**: `L_i = s · cheb l (i+1)` with `2 ≤ i+1 ≤ m`.  The
  uniform **sine-arc bound** `cheb l k ≥ λ` for `2 ≤ k ≤ m` then gives
  `L_i ≥ s · λ > 1` (since `s > 1/λ`).

The sine-arc bound `cheb (2cos θ) k ≥ 2cos θ = sin 2θ / sin θ` for `2 ≤ k ≤ m`,
`θ = π/(m+2)`, is exactly `sin(kθ) ≥ sin(2θ)` on the arc `kθ ∈ [2θ, π−2θ]`
(`mθ = π − 2θ`), by symmetry of `sin` about `π/2`.  It is proved here from the verified
`GenuineClassDischarge.cheb_sin` + `GenuineClassDischarge.sin_ge_sin_theta`.

## What is established

* `chebGeLambda_of_hecke` — the uniform sine-arc bound `λ ≤ cheb l k`, `2 ≤ k ≤ m`.
* `branchIdx_cusp_uniform` — `branchIdx l s 0 (…) = m` for ALL `m ≥ 2` at the Hecke λ
  (discharges `hbranch_all` uniformly).
* `Xomega_eq_uniform` — `X_Ω(q) = 1/λ³` for EVERY Hecke `q = m+2` given only the
  per-q window fact `Fwindow6 mpoly` + the standard band/minpoly inputs.  The
  cusp-branch identity is GONE (discharged uniformly above).
* Per-q corollaries `Xomega_eq_q7 … Xomega_eq_q21` — the window fact `hF{q}` is the
  verified `g{q}_no_window_below_genuine`; the only carried inputs are the
  minimal-polynomial `mpoly{q} l` and the band facts (the same inputs every
  per-q lower bound carries).

## Honesty note on q = 5

The genuine-map lower-bound engine (`perq_Xomega_lb_qge19_GEN'`) carries `hlo : 9/5 < l`.
For `q = 5`, `λ₅ = φ = 2cos(π/5) ≈ 1.618 < 9/5`, so that hypothesis is FALSE at the real
golden ratio: `OnsetEquality.Xomega_eq_q5` (and the uniform theorem instantiated at `m=3`)
is **vacuous** at the true `λ₅`.  The first index at which the band hypothesis `9/5 < λ_q`
genuinely holds is `q = 7` (`λ₇ ≈ 1.8019`).  Hence the honestly non-vacuous machine-verified
range of the EQUALITY is **q ∈ {7,8,…,21}** (15 Hecke indices).  The cusp-branch identity
`branchIdx_cusp_uniform` itself holds for every `m ≥ 2` (all `q ≥ 4`); the `9/5` floor is a
lower-bound-engine constraint, not a defect of the upper-bound / branch discharge.
-/

namespace OnsetEqualityUniform

open MeasureTheory Filter Set
open scoped ENNReal Topology
open HeckeS1 GenuineSelfMap UniformOnset OnsetEquality

noncomputable section

/-! ## §1.  The uniform sine-arc bound `λ ≤ cheb l k`, `2 ≤ k ≤ m`. -/

/-- **Uniform sine-arc bound.**  For `l = 2cos(π/(m+2))`, `m ≥ 2`, and `2 ≤ k ≤ m`, the
Chebyshev value `cheb l k ≥ l`.  Equivalent to `sin(kθ) ≥ sin(2θ)` for `kθ ∈ [2θ, π−2θ]`,
`θ = π/(m+2)`.  Proved from `cheb_sin` + `sin_ge_sin_theta` (both axiom-clean). -/
theorem chebGeLambda_of_hecke (m k : ℕ) (hm : 2 ≤ m) (hk : 2 ≤ k) (hkm : k ≤ m) :
    2 * Real.cos (Real.pi / ((m:ℝ) + 2)) ≤ cheb (2 * Real.cos (Real.pi / ((m:ℝ) + 2))) k := by
  set θ : ℝ := Real.pi / ((m:ℝ) + 2) with hθdef
  set l : ℝ := 2 * Real.cos θ with hldef
  have hmr : (0:ℝ) < (m : ℝ) + 2 := by positivity
  have hpi := Real.pi_pos
  -- 0 < θ ≤ π/2, and 2θ ≤ π/2 (needs m ≥ 2).
  have hθpos : 0 < θ := by rw [hθdef]; positivity
  have hmcast : (2:ℝ) ≤ (m:ℝ) := by exact_mod_cast hm
  have h2θle : 2 * θ ≤ Real.pi / 2 := by
    have hθle : θ ≤ Real.pi / (2 * 2) := by
      rw [hθdef]
      apply div_le_div_of_nonneg_left hpi.le (by norm_num) (by nlinarith [hmcast])
    have : Real.pi / (2 * 2) = (Real.pi / 2) / 2 := by ring
    rw [this] at hθle; linarith
  have h2θpos : 0 < 2 * θ := by linarith
  -- sin θ > 0.
  have hsinθ : 0 < Real.sin θ := by
    apply Real.sin_pos_of_pos_of_lt_pi hθpos
    rw [hθdef]; rw [div_lt_iff₀ hmr]; nlinarith [hpi, hmcast]
  -- The two sin closed forms.
  have hcsk : cheb l k * Real.sin θ = Real.sin ((k:ℝ) * θ) := by
    rw [hldef]; exact GenuineClassDischarge.cheb_sin θ k
  have hcs2 : cheb l 2 * Real.sin θ = Real.sin ((2:ℝ) * θ) := by
    have := GenuineClassDischarge.cheb_sin θ 2
    rw [hldef]; push_cast at this ⊢; convert this using 2
  -- cheb l 2 = l = 2 cos θ.
  have hcheb2 : cheb l 2 = l := by
    have : cheb l 2 = l * cheb l 1 - cheb l 0 := cheb_rec l 0
    rw [this]; simp [cheb_one, cheb_zero]
  -- kθ ∈ [2θ, π − 2θ].
  have hklo : 2 * θ ≤ (k : ℝ) * θ := by
    have : (2:ℝ) ≤ (k:ℝ) := by exact_mod_cast hk
    nlinarith [hθpos]
  have hkhi : (k : ℝ) * θ ≤ Real.pi - 2 * θ := by
    -- (k)θ ≤ mθ = mπ/(m+2) = π − 2π/(m+2) = π − 2θ
    have hkle : (k:ℝ) ≤ (m:ℝ) := by exact_mod_cast hkm
    have hmθ : (m:ℝ) * θ = Real.pi - 2 * θ := by
      rw [hθdef]; field_simp; ring
    nlinarith [hθpos, hkle, hmθ]
  -- sin(kθ) ≥ sin(2θ).
  have hge : Real.sin (2 * θ) ≤ Real.sin ((k : ℝ) * θ) :=
    GenuineClassDischarge.sin_ge_sin_theta (2 * θ) ((k:ℝ)*θ) h2θpos h2θle hklo hkhi
  -- transfer to cheb: cheb k · sinθ = sin(kθ) ≥ sin(2θ) = cheb 2 · sinθ = l · sinθ
  have hchain : l * Real.sin θ ≤ cheb l k * Real.sin θ := by
    rw [hcsk]
    calc l * Real.sin θ = cheb l 2 * Real.sin θ := by rw [hcheb2]
      _ = Real.sin ((2:ℝ) * θ) := hcs2
      _ ≤ Real.sin ((k:ℝ) * θ) := hge
  -- divide by sinθ > 0
  have := le_of_mul_le_mul_right (by linarith [hchain] : l * Real.sin θ ≤ cheb l k * Real.sin θ) hsinθ
  rwa [hldef] at this

/-! ## §2.  The uniform cusp active-branch identity (`hbranch_all` discharged). -/

/-- **Uniform cusp active-branch identity.**  For `l = 2cos(π/(m+2))`, `m ≥ 2`, and any cusp
tip `s ∈ (1/l,1]`, the active branch at `(s,0)` is `i = m`.  This discharges the
`hbranch_all` hypothesis of `OnsetEquality.Xomega_eq` for EVERY Hecke `q = m+2`.

Proof: `L l s 0 m = s·cheb l (m+1) = s ≤ 1` (active witness via `Boundary.hq1`), while for
`1 ≤ i ≤ m−1`, `L l s 0 i = s·cheb l (i+1) ≥ s·λ > 1` by the sine-arc bound
(`chebGeLambda_of_hecke`, `2 ≤ i+1 ≤ m`) — so no smaller index is active, pinning
`branchIdx = m` by minimality. -/
theorem branchIdx_cusp_uniform (m : ℕ) (hm : 2 ≤ m)
    {l : ℝ} (hl1 : 1 < l)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (B : Boundary l m) (s : ℝ) (hs_gt : 1 / l < s) (hs_le1 : s ≤ 1) :
    branchIdx l s 0 (branch_exists l s 0 m B.hq0 B.hq1 (by norm_num)) = m := by
  have hl0 : 0 < l := by linarith
  have hls : 1 < l * s := by have h := (div_lt_iff₀ hl0).mp hs_gt; nlinarith [h]
  -- L l s 0 i = s · cheb l (i+1).
  have hLval : ∀ i : ℕ, L l s 0 i = s * cheb l (i + 1) := by
    intro i; simp only [L]; ring
  -- cusp witness: L_m = s ≤ 1.
  have hLm : L l s 0 m = s := by rw [hLval, B.hq1]; ring
  -- sub-cusp indices 1 ≤ i ≤ m−1 are not active: L_i ≥ s·l > 1.
  set h := branch_exists l s 0 m B.hq0 B.hq1 (by norm_num) with hh
  have hspec := branchIdx_spec l s 0 h
  set i := branchIdx l s 0 h with hi
  obtain ⟨hi1, hiactive, himin⟩ := hspec
  -- m is an active witness ⇒ i ≤ m.
  have hle_m : i ≤ m := Nat.find_min' h ⟨by omega, by rw [hLm]; exact hs_le1⟩
  -- Each 1 ≤ j ≤ m−1 fails to be active.
  have hsubcusp : ∀ j : ℕ, 1 ≤ j → j ≤ m - 1 → ¬ (L l s 0 j ≤ 1) := by
    intro j hj1 hjm
    have hk2 : 2 ≤ j + 1 := by omega
    have hkm : j + 1 ≤ m := by omega
    have hcheb := chebGeLambda_of_hecke m (j + 1) hm hk2 hkm
    rw [← hHecke] at hcheb
    -- L_j = s · cheb l (j+1) ≥ s · l > 1
    have hLj : L l s 0 j = s * cheb l (j + 1) := hLval j
    have hspos : 0 < s := lt_trans (by positivity) hs_gt
    have : s * l ≤ L l s 0 j := by rw [hLj]; nlinarith [hcheb, hspos]
    have hgt1 : 1 < L l s 0 j := by nlinarith [this, hls]
    linarith
  -- i ≥ 1 active and ≤ m; but no 1 ≤ j ≤ m-1 active ⇒ i = m.
  by_contra hne
  have hilt : i < m := lt_of_le_of_ne hle_m hne
  have hile : i ≤ m - 1 := by omega
  exact hsubcusp i hi1 hile hiactive

/-! ## §3.  The uniform equality theorem.

`X_Ω(q) = 1/λ³` for EVERY Hecke `q = m+2`, with the cusp-branch identity discharged
uniformly.  The only carried inputs are the per-q window fact `Fwindow6 mpoly`, the
minimal polynomial `mpoly l`, and the standard band facts. -/

/-- **UNIFORM ONSET EQUALITY.**  `X_Ω(q) = 1/λ³` for every Hecke index `q = m+2` (`m ≥ 2`),
GIVEN the per-q window fact `hFW : Fwindow6 mpoly` (`hmp : mpoly l`) and the band facts.
The cusp active-branch identity is discharged INTERNALLY by `branchIdx_cusp_uniform` — there
is NO remaining q-concrete hypothesis beyond the window fact every lower bound already needs.

A non-attained infimum: every cusp Dirac `δ_{(s,0)}` has `essSup = s²/λ > 1/λ³` strictly. -/
theorem Xomega_eq_uniform
    {mpoly : ℝ → Prop} (hFW : Fwindow6 mpoly)
    (m : ℕ) (hm : 2 ≤ m) {l : ℝ} (B : Boundary l m)
    (hHecke : l = 2 * Real.cos (Real.pi / ((m:ℝ) + 2)))
    (hmp : mpoly l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l) (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l m B = 1 / l ^ 3 := by
  have hbranch_all : ∀ s : ℝ, 1 / l < s → s ≤ 1 →
      branchIdx l s 0 (branch_exists l s 0 m B.hq0 B.hq1 (by norm_num)) = m :=
    fun s hsg hsl => branchIdx_cusp_uniform m hm h1 hHecke B s hsg hsl
  exact Xomega_eq l m hFW B hHecke hmp h1 h2 hlo hlphi hm hbranch_all

/-! ## §4.  Per-q corollaries (q = 7 … 21).

Each supplies the verified per-q window fact `g{q}_no_window_below_genuine` (typed
`FwindowHyp{4,5,6}`, definitionally the `Fwindow6` shape after the `Fwindow6_of_*` lifts)
and the per-q minimal polynomial.  The band facts `1<l, l<2, 9/5<l, l²≥l+1` are carried
(the same inputs every per-q lower bound carries), and `B := boundary_of_hecke …`
is constructed from the Hecke form.  q = 5 is OMITTED: `9/5 < λ₅` is false (see header). -/

/-- 4-window → 6-window lift (a 4-window violation embeds in a 6-window one). -/
theorem Fwindow6_of_Fwindow4 {mpoly : ℝ → Prop} (h : Fwindow4 mpoly) : Fwindow6 mpoly :=
  fun lam hmp hl1 hl2 hlo c hpos hle hg1 hg2 hstep i ⟨h0, h1, h2, h3, _h4, _h5⟩ =>
    h lam hmp hl1 hl2 hlo c hpos hle hg1 hg2 hstep i ⟨h0, h1, h2, h3⟩

/-- 5-window → 6-window lift (a 5-window violation embeds in a 6-window one). -/
theorem Fwindow6_of_Fwindow5 {mpoly : ℝ → Prop} (h : Fwindow5 mpoly) : Fwindow6 mpoly :=
  fun lam hmp hl1 hl2 hlo c hpos hle hg1 hg2 hstep i ⟨h0, h1, h2, h3, h4, _h5⟩ =>
    h lam hmp hl1 hl2 hlo c hpos hle hg1 hg2 hstep i ⟨h0, h1, h2, h3, h4⟩

section PerQ
variable {l : ℝ}

/-- **q = 7 EQUALITY.**  `X_Ω(7) = 1/λ₇³`, `λ₇ = 2cos(π/7)`, `m = 5`. -/
theorem Xomega_eq_q7 (hHecke : l = 2 * Real.cos (Real.pi / ((5:ℝ) + 2)))
    (hmp : UniformOnset.mpoly7 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 5 (GenuineClassDischarge.boundary_of_hecke 5 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow4 _root_.hF7) 5 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 8 EQUALITY.**  `X_Ω(8) = 1/λ₈³`, `m = 6`. -/
theorem Xomega_eq_q8 (hHecke : l = 2 * Real.cos (Real.pi / ((6:ℝ) + 2)))
    (hmp : UniformOnset.mpoly8 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 6 (GenuineClassDischarge.boundary_of_hecke 6 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow4 _root_.hF8) 6 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 9 EQUALITY.**  `m = 7`. -/
theorem Xomega_eq_q9 (hHecke : l = 2 * Real.cos (Real.pi / ((7:ℝ) + 2)))
    (hmp : UniformOnset.mpoly9 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 7 (GenuineClassDischarge.boundary_of_hecke 7 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow4 _root_.hF9) 7 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 10 EQUALITY.**  `m = 8`. -/
theorem Xomega_eq_q10 (hHecke : l = 2 * Real.cos (Real.pi / ((8:ℝ) + 2)))
    (hmp : UniformOnset.mpoly10 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 8 (GenuineClassDischarge.boundary_of_hecke 8 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow4 _root_.hF10) 8 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 11 EQUALITY.**  `m = 9`. -/
theorem Xomega_eq_q11 (hHecke : l = 2 * Real.cos (Real.pi / ((9:ℝ) + 2)))
    (hmp : UniformOnset.mpoly11 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 9 (GenuineClassDischarge.boundary_of_hecke 9 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow4 _root_.hF11) 9 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 12 EQUALITY.**  `m = 10`. -/
theorem Xomega_eq_q12 (hHecke : l = 2 * Real.cos (Real.pi / ((10:ℝ) + 2)))
    (hmp : UniformOnset.mpoly12 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 10 (GenuineClassDischarge.boundary_of_hecke 10 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow5 _root_.hF12) 10 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 13 EQUALITY.**  `m = 11`. -/
theorem Xomega_eq_q13 (hHecke : l = 2 * Real.cos (Real.pi / ((11:ℝ) + 2)))
    (hmp : UniformOnset.mpoly13 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 11 (GenuineClassDischarge.boundary_of_hecke 11 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow5 _root_.hF13) 11 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 14 EQUALITY.**  `m = 12`. -/
theorem Xomega_eq_q14 (hHecke : l = 2 * Real.cos (Real.pi / ((12:ℝ) + 2)))
    (hmp : UniformOnset.mpoly14 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 12 (GenuineClassDischarge.boundary_of_hecke 12 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow5 _root_.hF14) 12 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 15 EQUALITY.**  `m = 13`. -/
theorem Xomega_eq_q15 (hHecke : l = 2 * Real.cos (Real.pi / ((13:ℝ) + 2)))
    (hmp : UniformOnset.mpoly15 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 13 (GenuineClassDischarge.boundary_of_hecke 13 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow5 _root_.hF15) 13 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 16 EQUALITY.**  `m = 14`. -/
theorem Xomega_eq_q16 (hHecke : l = 2 * Real.cos (Real.pi / ((14:ℝ) + 2)))
    (hmp : UniformOnset.mpoly16 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 14 (GenuineClassDischarge.boundary_of_hecke 14 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform (Fwindow6_of_Fwindow5 _root_.hF16) 14 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 17 EQUALITY.**  `m = 15`.  Native 6-window. -/
theorem Xomega_eq_q17 (hHecke : l = 2 * Real.cos (Real.pi / ((15:ℝ) + 2)))
    (hmp : UniformOnset.mpoly17 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 15 (GenuineClassDischarge.boundary_of_hecke 15 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform _root_.hF17 15 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 18 EQUALITY.**  `m = 16`.  Native 6-window. -/
theorem Xomega_eq_q18 (hHecke : l = 2 * Real.cos (Real.pi / ((16:ℝ) + 2)))
    (hmp : UniformOnset.mpoly18 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 16 (GenuineClassDischarge.boundary_of_hecke 16 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform _root_.hF18 16 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 19 EQUALITY.**  `m = 17`.  Native 6-window (`GenuineMapFacts.hF19`). -/
theorem Xomega_eq_q19 (hHecke : l = 2 * Real.cos (Real.pi / ((17:ℝ) + 2)))
    (hmp : GenuineMapFacts.mpoly19 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 17 (GenuineClassDischarge.boundary_of_hecke 17 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform GenuineMapFacts.hF19 17 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 20 EQUALITY.**  `m = 18`.  Native 6-window (`GenuineMapFacts.hF20`). -/
theorem Xomega_eq_q20 (hHecke : l = 2 * Real.cos (Real.pi / ((18:ℝ) + 2)))
    (hmp : GenuineMapFacts.mpoly20 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 18 (GenuineClassDischarge.boundary_of_hecke 18 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform GenuineMapFacts.hF20 18 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

/-- **q = 21 EQUALITY.**  `m = 19`.  Native 6-window (`GenuineMapFacts.hF21`). -/
theorem Xomega_eq_q21 (hHecke : l = 2 * Real.cos (Real.pi / ((19:ℝ) + 2)))
    (hmp : GenuineMapFacts.mpoly21 l) (h1 : 1 < l) (h2 : l < 2) (hlo : 9/5 < l)
    (hlphi : l ^ 2 ≥ l + 1) :
    Xomega l 19 (GenuineClassDischarge.boundary_of_hecke 19 (by norm_num) l hHecke) = 1 / l ^ 3 :=
  Xomega_eq_uniform GenuineMapFacts.hF21 19 (by norm_num) _ hHecke hmp h1 h2 hlo hlphi

end PerQ

end

end OnsetEqualityUniform

-- ════════════ AXIOM AUDIT ════════════
#print axioms OnsetEqualityUniform.chebGeLambda_of_hecke
#print axioms OnsetEqualityUniform.branchIdx_cusp_uniform
#print axioms OnsetEqualityUniform.Xomega_eq_uniform
#print axioms OnsetEqualityUniform.Xomega_eq_q7
#print axioms OnsetEqualityUniform.Xomega_eq_q12
#print axioms OnsetEqualityUniform.Xomega_eq_q17
#print axioms OnsetEqualityUniform.Xomega_eq_q18
#print axioms OnsetEqualityUniform.Xomega_eq_q19
#print axioms OnsetEqualityUniform.Xomega_eq_q21
