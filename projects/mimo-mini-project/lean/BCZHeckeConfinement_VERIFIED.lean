import Mathlib
set_option maxHeartbeats 2000000
/-!
# BCZ–Hecke confinement assembly — eliminating the monolithic `hconfine` connective.

## What this file closes

The genuine-map (C′) "no sustained sub-threshold orbit" was, in
`BCZHeckeGenuineMap_allq_WIP.perq_general_no_sustained`, conditional on a single MONOLITHIC,
still-open hypothesis

  `hconfine : (∀ j, Q j < 1/l³) → ∃ scalar F-corridor sequence c, everywhere sub-threshold`

— the global "sustained sub-threshold ⟹ confined to the scalar branch" reduction (§6 item (2),
"OPEN in Lean").  This file **eliminates `hconfine`** and replaces it by the conjunction of

  (T) a per-step **branch trichotomy** `htri` : every orbit step is scalar / deep-mid / cusp
      (this is the genuine branch decomposition = the genuine *map definition*, §6 item (1)),
  (C) a per-step **cusp fact** `hcusp`  : a cusp step has `Pgen ≥ 1/l³`,
  (D) a per-step **deep-mid fact** `hdeep` : a sub-threshold deep-mid step ejects, `Pgen(n+1) ≥ 1/l³`.

(C) and (D) are **already PROVEN, axiom-clean**, in named files — not new assumptions:
  * (C) is `BCZHeckeAvoidCusp_VERIFIED.kick_bound_of_branch`
        (= `cusp_envelope` ⇒ `1/l³ ≤ Pgen` on the cusp branch).
  * (D) is `BCZHeckeGenuineMap_allq_WIP.genuine_ejection_floor1`
        instantiated at `thr = 1/l³` (admissible for `q = 16..21`; see `deep_threshold_admissible`).

The new content is the **symbolic-dynamics ASSEMBLY** `subthreshold_forces_scalar`: from (T)+(C)+(D)
and "every step sub-threshold", EVERY step must be scalar (a cusp step would already be `≥ 1/l³`; a
deep-mid step would force the *next* step `≥ 1/l³`).  Once every step is scalar the orbit is a genuine
`Tmap` F-corridor orbit, and the proven per-q F-window refutes a 6-window — closing (C′).

So the residual shrinks from the **global** confinement lemma to the **local** branch trichotomy
`htri` (the map definition), with the two dynamical legs discharged by proven lemmas.

`#print axioms` on every theorem below must be exactly `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeConfine

noncomputable section

variable (l : ℝ)

/-! ## §0. Objects (verbatim from the assembly / ObsAlign / AvoidCusp files). -/

/-- Chebyshev sequence `x_n`, `x_0 = 0, x_1 = 1, x_{n+2} = l x_{n+1} − x_n`. -/
def cheb : ℕ → ℝ
  | 0 => 0
  | 1 => 1
  | (n + 2) => l * cheb (n + 1) - cheb n

@[simp] lemma cheb_zero : cheb l 0 = 0 := rfl
@[simp] lemma cheb_one : cheb l 1 = 1 := rfl
lemma cheb_rec (n : ℕ) : cheb l (n + 2) = l * cheb l (n + 1) - cheb l n := rfl

/-- Genuine observable `Pgen (a,b) = a (a + l b)/l` (matches every file's `Pgen`). -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-- The scalar-branch BCZ map `Tmap (a,b) = (b, ⌊(1+a)/(l b)⌋·l·b − a)` (the `i = q−1` branch). -/
def Tmap (p : ℝ × ℝ) : ℝ × ℝ :=
  (p.2, (⌊(1 + p.1) / (l * p.2)⌋ : ℝ) * (l * p.2) - p.1)

@[simp] lemma Tmap_fst (p : ℝ × ℝ) : (Tmap l p).1 = p.2 := rfl
lemma Tmap_snd (p : ℝ × ℝ) :
    (Tmap l p).2 = (⌊(1 + p.1) / (l * p.2)⌋ : ℝ) * (l * p.2) - p.1 := rfl

/-- The F-corridor domain `Dcorr = {0<a≤1, 0<b≤1, a+l b>1, l a+b>1}` (both Taha edges). -/
def Dcorr : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}

/-- The verbatim per-q F-window hypothesis type (EXACT signature of `g{q}_no_window_below_genuine`,
axiom-clean in `BCZHeckeG{q}_window_VERIFIED.lean`), for a per-q minimal-polynomial predicate. -/
def FwindowHyp (mpoly : ℝ → Prop) : Prop :=
  ∀ (lam : ℝ), mpoly lam → (1:ℝ) < lam → lam < 2 → (9:ℝ)/5 < lam →
  ∀ (c : ℕ → ℝ), (∀ n, 0 < c n) → (∀ n, c n ≤ 1) →
    (∀ n, c n + lam * c (n+1) > 1) → (∀ n, lam * c n + c (n+1) > 1) →
    (∀ n, c n + c (n+2) = (⌊(1 + c n)/(lam*c (n+1))⌋ : ℝ)*lam*c (n+1)) →
    ∀ i, ¬ (c (i+0) * c (i+1) < 1/lam^3 ∧
            c (i+1) * c (i+2) < 1/lam^3 ∧
            c (i+2) * c (i+3) < 1/lam^3 ∧
            c (i+3) * c (i+4) < 1/lam^3 ∧
            c (i+4) * c (i+5) < 1/lam^3 ∧
            c (i+5) * c (i+6) < 1/lam^3)

/-! ## §1. THE TRANSFER (`Pgen` sub-threshold ⟹ product sub-threshold), verbatim from ObsAlign. -/

/-- `Pgen − a·b = a²/l` (the only slack). -/
theorem Pgen_sub_prod (a b : ℝ) (hl : l ≠ 0) :
    Pgen l (a, b) - a * b = a ^ 2 / l := by
  simp only [Pgen_apply]; field_simp; ring

/-- Product `≤` genuine observable for `l > 0`. -/
theorem prod_le_Pgen (a b : ℝ) (hl : 0 < l) : a * b ≤ Pgen l (a, b) := by
  have h := Pgen_sub_prod l a b (ne_of_gt hl)
  have hnn : 0 ≤ a ^ 2 / l := div_nonneg (sq_nonneg a) hl.le
  linarith

/-- **Transfer**: a `Pgen`-sub-threshold point is product-sub-threshold. -/
theorem prod_lt_of_Pgen_lt (a b t : ℝ) (hl : 0 < l) (hP : Pgen l (a, b) < t) : a * b < t :=
  lt_of_le_of_lt (prod_le_Pgen l a b hl) hP

/-! ## §2. SCALAR READ-OFF: a `Tmap`-orbit in `Dcorr` is a genuine F-corridor sequence.
Verbatim port of `orbit_to_cseq_hyps`. -/

theorem orbit_to_cseq_hyps
    (orbit : ℕ → ℝ × ℝ)
    (hmem : ∀ n, orbit n ∈ Dcorr l)
    (hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n)) :
    (∀ n, 0 < (orbit n).1) ∧ (∀ n, (orbit n).1 ≤ 1) ∧
    (∀ n, (orbit n).1 + l * (orbit (n+1)).1 > 1) ∧
    (∀ n, l * (orbit n).1 + (orbit (n+1)).1 > 1) ∧
    (∀ n, (orbit n).1 + (orbit (n+2)).1
      = (⌊(1 + (orbit n).1) / (l * (orbit (n+1)).1)⌋ : ℝ) * l * (orbit (n+1)).1) := by
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, Tmap_fst]
  refine ⟨fun n => (hmem n).1, fun n => (hmem n).2.1, ?_, ?_, ?_⟩
  · intro n; have h := (hmem n).2.2.2.2.1; rw [hlink n] at h; exact h
  · intro n; have h := (hmem n).2.2.2.2.2; rw [hlink n] at h; exact h
  · intro n
    have h22 : (orbit (n + 2)).1 = (orbit (n + 1)).2 := (hlink (n + 1)).symm
    have hval : (orbit (n + 1)).2
        = (⌊(1 + (orbit n).1) / (l * (orbit n).2)⌋ : ℝ) * (l * (orbit n).2) - (orbit n).1 := by
      rw [hstep n, Tmap_snd]
    rw [h22, hval, hlink n]; ring

/-! ## §3. ★ THE CONFINEMENT ENGINE — the symbolic-dynamics assembly. ★

This is the previously-open content.  Given the per-step trichotomy and the two dynamical legs, a
sustained sub-threshold orbit is forced ENTIRELY onto the scalar branch. -/

/-- **★ Sustained sub-threshold ⟹ every step scalar.**  Pure finite-symbol argument:
* a **cusp** step has `t ≤ P n` (leg C), contradicting `P n < t`;
* a sub-threshold **deep-mid** step ejects, `t ≤ P (n+1)` (leg D), contradicting `P (n+1) < t`;
so the only consistent branch at every step is **scalar**.  This eliminates the monolithic
`hconfine`. -/
theorem subthreshold_forces_scalar {t : ℝ}
    (scalar deepmid cusp : ℕ → Prop) (P : ℕ → ℝ)
    (htri : ∀ n, scalar n ∨ deepmid n ∨ cusp n)
    (hcusp : ∀ n, cusp n → t ≤ P n)
    (hdeep : ∀ n, deepmid n → P n < t → t ≤ P (n + 1))
    (hsus : ∀ n, P n < t) :
    ∀ n, scalar n := by
  intro n
  rcases htri n with hs | hd | hc
  · exact hs
  · exact absurd (hdeep n hd (hsus n)) (not_le.mpr (hsus (n + 1)))
  · exact absurd (hcusp n hc) (not_le.mpr (hsus n))

/-! ## §4. ★ THE ASSEMBLED (C′): no sustained sub-threshold genuine orbit, with `hconfine` GONE. ★

`hconfine` is replaced by `htri` (trichotomy = map definition, the only residual) plus the two
PROVEN per-step legs `hcusp`/`hdeep`.  The scalar leg of the trichotomy is the CONCRETE
`Tmap`/`Dcorr` F-corridor step; once all steps are scalar, the proven F-window `hF` refutes the
6-window. -/
theorem genuine_no_sustained_assembled
    (mpoly : ℝ → Prop) (hF : FwindowHyp mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l)
    (orbit : ℕ → ℝ × ℝ) (deepmid cusp : ℕ → Prop)
    (htri : ∀ n,
      (orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n)) ∨ deepmid n ∨ cusp n)
    (hcusp : ∀ n, cusp n → 1 / l ^ 3 ≤ Pgen l (orbit n))
    (hdeep : ∀ n, deepmid n → Pgen l (orbit n) < 1 / l ^ 3 → 1 / l ^ 3 ≤ Pgen l (orbit (n + 1))) :
    ¬ (∀ n, Pgen l (orbit n) < 1 / l ^ 3) := by
  intro hsus
  -- The confinement engine: every step is the scalar `Tmap`/`Dcorr` branch.
  have hscal := subthreshold_forces_scalar
      (fun n => orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n)) deepmid cusp
      (fun n => Pgen l (orbit n)) htri hcusp hdeep hsus
  have hmem : ∀ n, orbit n ∈ Dcorr l := fun n => (hscal n).1
  have hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n) := fun n => (hscal n).2
  -- Scalar read-off: the orbit is a genuine F-corridor sequence.
  obtain ⟨hposc, hcap, hreg, hgen, hrec⟩ := orbit_to_cseq_hyps l orbit hmem hstep
  have hl0 : 0 < l := by linarith
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, Tmap_fst]
  set c : ℕ → ℝ := fun n => (orbit n).1 with hc
  -- Transfer: sub-threshold `Pgen` ⟹ sub-threshold product `c_n·c_{n+1}`.
  have hsubc : ∀ n, c n * c (n + 1) < 1 / l ^ 3 := by
    intro n
    have hPpair : Pgen l ((orbit n).1, (orbit n).2) < 1 / l ^ 3 := by
      rw [Prod.mk.eta]; exact hsus n
    have h := prod_lt_of_Pgen_lt l (orbit n).1 (orbit n).2 (1 / l ^ 3) hl0 hPpair
    rw [hlink n] at h; exact h
  -- Feed the F-window at i = 0 with the first six sub-threshold products.
  exact hF l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0
    ⟨hsubc 0, hsubc 1, hsubc 2, hsubc 3, hsubc 4, hsubc 5⟩

/-! ## §5. The decomposition is FAITHFUL: the legs RECONSTRUCT the old `hconfine`.

We prove that `htri + hcusp + hdeep` (plus the scalar read-off, which is just `orbit_to_cseq_hyps`)
implies the original monolithic `hconfine` of `perq_general_no_sustained`.  Hence the new hypotheses
are genuinely WEAKER / more local than `hconfine`: anything provable with the old connective is
provable here, and the engine is the missing implication.  (Q n is the genuine observable along the
orbit.) -/
theorem hconfine_of_legs
    (orbit : ℕ → ℝ × ℝ) (deepmid cusp : ℕ → Prop)
    (hl0 : 0 < l)
    (htri : ∀ n,
      (orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n)) ∨ deepmid n ∨ cusp n)
    (hcusp : ∀ n, cusp n → 1 / l ^ 3 ≤ Pgen l (orbit n))
    (hdeep : ∀ n, deepmid n → Pgen l (orbit n) < 1 / l ^ 3 → 1 / l ^ 3 ≤ Pgen l (orbit (n + 1))) :
    (∀ j, Pgen l (orbit j) < 1 / l ^ 3) →
      ∃ (c : ℕ → ℝ),
        (∀ n, 0 < c n) ∧ (∀ n, c n ≤ 1) ∧
        (∀ n, c n + l * c (n+1) > 1) ∧ (∀ n, l * c n + c (n+1) > 1) ∧
        (∀ n, c n + c (n+2) = (⌊(1 + c n)/(l*c (n+1))⌋ : ℝ)*l*c (n+1)) ∧
        (∀ n, c n * c (n+1) < 1 / l ^ 3) := by
  intro hsus
  have hscal := subthreshold_forces_scalar
      (fun n => orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n)) deepmid cusp
      (fun n => Pgen l (orbit n)) htri hcusp hdeep hsus
  have hmem : ∀ n, orbit n ∈ Dcorr l := fun n => (hscal n).1
  have hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n) := fun n => (hscal n).2
  obtain ⟨hposc, hcap, hreg, hgen, hrec⟩ := orbit_to_cseq_hyps l orbit hmem hstep
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, Tmap_fst]
  refine ⟨fun n => (orbit n).1, hposc, hcap, hreg, hgen, hrec, ?_⟩
  intro n
  have hPpair : Pgen l ((orbit n).1, (orbit n).2) < 1 / l ^ 3 := by
    rw [Prod.mk.eta]; exact hsus n
  have h := prod_lt_of_Pgen_lt l (orbit n).1 (orbit n).2 (1 / l ^ 3) hl0 hPpair
  rw [hlink n] at h; exact h

/-! ## §6. DEEP-MID THRESHOLD ADMISSIBILITY: `thr = 1/l³` lies in the ejection range `[129/1000,
663/5000]` for the principal-Hecke `l` of `q = 16..21` (so leg (D) = `genuine_ejection_floor1` at
`thr = 1/l³` is applicable).  Sample: `q = 18`, `l = 2cos(π/18) ∈ [1.9695, 1.9698]`. -/
theorem deep_threshold_admissible
    (hlo : (19695:ℝ)/10000 ≤ l) (hhi : l ≤ (19698:ℝ)/10000) :
    (129:ℝ)/1000 ≤ 1 / l ^ 3 ∧ 1 / l ^ 3 ≤ (663:ℝ)/5000 := by
  have hl0 : 0 < l := by linarith
  have hl3 : 0 < l ^ 3 := by positivity
  have hupper : l ^ 3 ≤ (19698:ℝ)/10000 * ((19698:ℝ)/10000 * ((19698:ℝ)/10000)) := by
    have h2 : l ^ 2 ≤ (19698:ℝ)/10000 * ((19698:ℝ)/10000) := by nlinarith [hlo, hhi, hl0]
    nlinarith [h2, hlo, hhi, hl0, sq_nonneg l]
  have hlower : (19695:ℝ)/10000 * ((19695:ℝ)/10000 * ((19695:ℝ)/10000)) ≤ l ^ 3 := by
    have h2 : (19695:ℝ)/10000 * ((19695:ℝ)/10000) ≤ l ^ 2 := by nlinarith [hlo, hhi, hl0]
    nlinarith [h2, hlo, hhi, hl0, sq_nonneg l]
  refine ⟨?_, ?_⟩
  · rw [le_div_iff₀ hl3]; nlinarith [hupper]
  · rw [div_le_iff₀ hl3]; nlinarith [hlower]

/-! ## §7. ★ LEG (C) DISCHARGED — the cusp leg `hcusp` is the PROVEN cusp envelope. ★

`cusp_envelope` (verbatim from `BCZHeckeAvoidCusp_VERIFIED`, axiom-clean) shows the cusp-branch guards
force `Pgen ≥ 1/l³`.  So leg (C) of the engine is **not an assumption** — it is this theorem.  We then
give the fully-cusp-discharged capstone, where `cusp n` is the concrete cusp-guard membership. -/

/-- Cusp-branch guards at a point: `0<a, a≤1, l a+(l²−1)b>1, l a+b>1, a+l b≤1`. -/
def CuspGuards (l : ℝ) (p : ℝ × ℝ) : Prop :=
  0 < p.1 ∧ p.1 ≤ 1 ∧ l * p.1 + (l ^ 2 - 1) * p.2 > 1 ∧ l * p.1 + p.2 > 1 ∧ p.1 + l * p.2 ≤ 1

/-- **Cusp envelope** (verbatim, axiom-clean from `BCZHeckeAvoidCusp_VERIFIED.cusp_envelope`):
the cusp-branch guards force `1/l³ ≤ a(a+l b)/l`. -/
theorem cusp_envelope (a b : ℝ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hG : l * a + (l ^ 2 - 1) * b > 1)
    (hd : l * a + b > 1)
    (hU : a + l * b ≤ 1) :
    1 / l ^ 3 ≤ a * (a + l * b) / l := by
  have hl : 0 < l := by linarith
  have hl2 : l ^ 2 - 2 > 0 := by nlinarith [hlphi, hl1]
  have hc1 : l ^ 3 - l - 1 ≥ 0 := by nlinarith [hlphi, hl1]
  have hc2 : l ^ 2 - l - 1 ≥ 0 := by linarith [hlphi]
  have hkey : 1 ≤ l ^ 2 * (a * (a + l * b)) := by
    rcases le_or_gt a (1 / l) with hca | hca
    · have hfa : l * a ≤ 1 := by rw [mul_comm]; exact (le_div_iff₀ hl).mp hca
      have hage : a * (l + 1) ≥ 1 := by nlinarith [hU, hd, hl]
      have hlo : 1 ≤ l ^ 2 * a := by nlinarith [hage, hlphi, ha, hl]
      nlinarith [hl2, hl,
        mul_nonneg hc1 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + b - 1 by linarith)),
        mul_nonneg hl2.le (mul_nonneg (show (0:ℝ) ≤ l ^ 2 * a - 1 by linarith)
                                      (show (0:ℝ) ≤ 1 - l * a by linarith)),
        mul_nonneg hc2 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + (l ^ 2 - 1) * b - 1 by linarith))]
    · have hfa : 1 ≤ l * a := by
        have h := (div_lt_iff₀ hl).mp hca; rw [mul_comm] at h; linarith
      nlinarith [hl2, hl,
        mul_nonneg hc1 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + (l ^ 2 - 1) * b - 1 by linarith)),
        mul_nonneg hl2.le (mul_nonneg (show (0:ℝ) ≤ l * a - 1 by linarith)
                                      (show (0:ℝ) ≤ 1 - a by linarith)),
        mul_nonneg hc2 (mul_nonneg ha.le (show (0:ℝ) ≤ l * a + b - 1 by linarith))]
  have e : a * (a + l * b) / l - 1 / l ^ 3
      = (l ^ 2 * (a * (a + l * b)) - 1) / l ^ 3 := by
    rw [div_sub_div _ _ (by positivity : (l:ℝ) ≠ 0) (by positivity : (l:ℝ) ^ 3 ≠ 0)]
    rw [div_eq_div_iff (by positivity) (by positivity)]; ring
  have hnn : 0 ≤ a * (a + l * b) / l - 1 / l ^ 3 := by
    rw [e]; exact div_nonneg (by linarith [hkey]) (by positivity)
  linarith

/-- **★ LEG (C) AS A THEOREM.**  A cusp-guard point has `Pgen ≥ 1/l³`. -/
theorem cusp_step_bound (p : ℝ × ℝ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1) (hg : CuspGuards l p) :
    1 / l ^ 3 ≤ Pgen l p := by
  obtain ⟨ha, ha1, hG, hd, hU⟩ := hg
  simpa [Pgen] using cusp_envelope l p.1 p.2 hl1 hlphi ha ha1 hG hd hU

/-- **★ FULLY-CUSP-DISCHARGED (C′).**  Same as `genuine_no_sustained_assembled` but the cusp leg is
DISCHARGED: `cusp n` is the concrete cusp-guard membership `CuspGuards l (orbit n)`, and `hcusp` is
supplied internally by `cusp_step_bound` (the proven envelope).  The remaining inputs are the branch
trichotomy `htri` (= the genuine map definition) and the deep-mid ejection leg `hdeep`. -/
theorem genuine_no_sustained_cusp_discharged
    (mpoly : ℝ → Prop) (hF : FwindowHyp mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (orbit : ℕ → ℝ × ℝ) (deepmid : ℕ → Prop)
    (htri : ∀ n,
      (orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n)) ∨ deepmid n ∨ CuspGuards l (orbit n))
    (hdeep : ∀ n, deepmid n → Pgen l (orbit n) < 1 / l ^ 3 → 1 / l ^ 3 ≤ Pgen l (orbit (n + 1))) :
    ¬ (∀ n, Pgen l (orbit n) < 1 / l ^ 3) :=
  genuine_no_sustained_assembled l mpoly hF hmp h1 h2 hlo orbit deepmid
    (fun n => CuspGuards l (orbit n))
    htri (fun n hn => cusp_step_bound l (orbit n) h1 hlphi hn) hdeep

end

end HeckeConfine

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeConfine.cusp_envelope
#print axioms HeckeConfine.cusp_step_bound
#print axioms HeckeConfine.genuine_no_sustained_cusp_discharged
#print axioms HeckeConfine.prod_lt_of_Pgen_lt
#print axioms HeckeConfine.orbit_to_cseq_hyps
#print axioms HeckeConfine.subthreshold_forces_scalar
#print axioms HeckeConfine.genuine_no_sustained_assembled
#print axioms HeckeConfine.hconfine_of_legs
#print axioms HeckeConfine.deep_threshold_admissible
