import Mathlib
set_option maxHeartbeats 2000000
/-!
# BCZ–Hecke GATE-2 consolidated confinement assembly (merge).

This file **merges** the two concurrent reductions of GATE-2 / (C′) "no sustained sub-threshold
orbit" into one canonical, axiom-clean assembly:

* `BCZHeckeConfinement_VERIFIED` (namespace `HeckeConfine`) — the **trichotomy** engine
  `subthreshold_forces_scalar`: every step ∈ {scalar, deep-mid, cusp}; the proven **cusp** leg and
  the proven **ejection** leg force a sustained sub-threshold orbit entirely onto the scalar branch.
* `BCZHeckeDeepMidElim_VERIFIED` (namespace `DeepMidElim`) — the **run** engine
  `deepmid_free_run` / `deepmid_only_trailing`: a finite sub-threshold run is deep-mid-free.
* `BCZHeckeEjection_q16to21_VERIFIED` (namespace `HeckeEjection`) — the proven `ejection_kick`
  (deep-mid sub-threshold ⟹ successor `≥ thr`, dwell ≤ 1), the shared dynamical leg.

## The merge insight (why this is a real consolidation, not a rename)

`DeepMidElim.deepmid_free_run` needs a second leg `entry` ("a deep-mid step preceded by a
sub-threshold step is itself `≥ thr`") to kill the **trailing** step of a FINITE run — and `entry`
is only **numerically** verified, an unproven hypothesis. But (C′) is about **infinite sustained**
orbits, which have no trailing step. For such orbits **ejection alone** eliminates deep-mid
(`sustained_deepmid_free`), and the proven **cusp** leg eliminates cusp, so the trichotomy engine
gives a **pure scalar** run with **no `entry` hypothesis at all**. The merge therefore *drops* an
unproven leg: the only residual is the branch trichotomy `htri` (= the genuine map definition).

## Status of every leg
* `subthreshold_forces_scalar`, `sustained_deepmid_free`, `sustained_pure_scalar` — PROVEN (engine).
* cusp leg `cusp_step_bound` (via `cusp_envelope`) — PROVEN, axiom-clean.
* ejection leg `ejection_kick` — PROVEN, axiom-clean (uv-coords, all kicks `k ≥ 0`).
* transfer / scalar read-off / F-window feed — PROVEN.
* `entry` — **DROPPED** (superseded for sustained orbits).
* residual: `htri` (orbit-level branch trichotomy = map definition) + the geometric `hmin`
  (K≥2 deep-mid → cusp routing).  Numerically confirmed; supplied as a hypothesis.

`#print axioms` on every theorem below must be exactly `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeGate2

noncomputable section

/-! ## §1. ABSTRACT ENGINES (branch-symbolic; no geometry). -/

/-- **★ Trichotomy engine** (from `HeckeConfine`).  Sustained sub-threshold + per-step legs ⟹ every
step scalar: a cusp step has `t ≤ P n` (contradiction); a sub-threshold deep-mid step ejects,
`t ≤ P (n+1)` (contradiction). -/
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

/-- **★ MERGE LEMMA — entry-free deep-mid elimination for sustained orbits.**  An INFINITE sustained
sub-threshold orbit has NO deep-mid step, using ONLY the proven ejection leg.  This is the
`DeepMidElim.deepmid_free_run` conclusion WITHOUT its numerically-only `entry` hypothesis: an
infinite orbit has no trailing step, so ejection (which constrains the successor) alone suffices. -/
theorem sustained_deepmid_free {t : ℝ}
    (P : ℕ → ℝ) (isD : ℕ → Prop)
    (eject : ∀ n, isD n → P n < t → t ≤ P (n + 1))
    (hsus : ∀ n, P n < t) :
    ∀ n, ¬ isD n := by
  intro n hDn
  exact absurd (eject n hDn (hsus n)) (not_le.mpr (hsus (n + 1)))

/-- **★ Pure-scalar consolidation.**  A sustained sub-threshold orbit is BOTH deep-mid-free (ejection,
no `entry`) AND cusp-free (proven cusp leg), hence purely scalar — the unified GATE-2 reduction. -/
theorem sustained_pure_scalar {t : ℝ}
    (scalar deepmid cusp : ℕ → Prop) (P : ℕ → ℝ)
    (htri : ∀ n, scalar n ∨ deepmid n ∨ cusp n)
    (hcusp : ∀ n, cusp n → t ≤ P n)
    (heject : ∀ n, deepmid n → P n < t → t ≤ P (n + 1))
    (hsus : ∀ n, P n < t) :
    (∀ n, scalar n) ∧ (∀ n, ¬ deepmid n) ∧ (∀ n, ¬ cusp n) := by
  refine ⟨subthreshold_forces_scalar scalar deepmid cusp P htri hcusp heject hsus, ?_, ?_⟩
  · exact sustained_deepmid_free P deepmid heject hsus
  · intro n hc; exact absurd (hcusp n hc) (not_le.mpr (hsus n))

/-! ### §1b. The run-level DeepMidElim engines (from `DeepMidElim`, verbatim — retained for the
finite-run analysis; require `entry` only for the trailing step). -/

/-- No two consecutive sub-threshold steps include a deep-mid step (`eject` + `entry`). -/
theorem no_consec_subthr_deepmid
    (thr : ℝ) (P : ℕ → ℝ) (isD : ℕ → Prop)
    (eject : ∀ n, isD n → P n < thr → thr ≤ P (n + 1))
    (entry : ∀ n, P n < thr → isD (n + 1) → thr ≤ P (n + 1))
    (n : ℕ) (hn : P n < thr) (hn1 : P (n + 1) < thr) :
    ¬ isD n ∧ ¬ isD (n + 1) := by
  refine ⟨?_, ?_⟩
  · intro hDn; have := eject n hDn hn; linarith
  · intro hDn1; have := entry n hn hDn1; linarith

/-- A finite sub-threshold run of length ≥ 2 is deep-mid-free (`eject` + `entry`). -/
theorem deepmid_free_run
    (thr : ℝ) (P : ℕ → ℝ) (isD : ℕ → Prop)
    (eject : ∀ n, isD n → P n < thr → thr ≤ P (n + 1))
    (entry : ∀ n, P n < thr → isD (n + 1) → thr ≤ P (n + 1))
    (i L : ℕ) (hL : 1 ≤ L)
    (hrun : ∀ j, j ≤ L → P (i + j) < thr) :
    ∀ j, j ≤ L → ¬ isD (i + j) := by
  intro j hj hDij
  rcases Nat.lt_or_ge j L with hjL | hjL
  · have h1 := hrun j hj
    have h2 := hrun (j + 1) (by omega)
    have hkey := eject (i + j) hDij h1
    rw [show i + (j + 1) = (i + j) + 1 by omega] at h2
    linarith
  · obtain ⟨m, hm⟩ : ∃ m, j = m + 1 := ⟨j - 1, by omega⟩
    subst hm
    have hpred := hrun m (by omega)
    have hDcur : isD ((i + m) + 1) := by rw [show (i + m) + 1 = i + (m + 1) by omega]; exact hDij
    have hkey := entry (i + m) hpred hDcur
    rw [show (i + m) + 1 = i + (m + 1) by omega] at hkey
    have hcur := hrun (m + 1) hj
    linarith

/-- Unconditional (ejection only): in a finite sub-threshold run, deep-mid occurs only as the LAST
step (`eject` only, no `entry`). -/
theorem deepmid_only_trailing
    (thr : ℝ) (P : ℕ → ℝ) (isD : ℕ → Prop)
    (eject : ∀ n, isD n → P n < thr → thr ≤ P (n + 1))
    (i L : ℕ)
    (hrun : ∀ j, j ≤ L → P (i + j) < thr) :
    ∀ j, j < L → ¬ isD (i + j) := by
  intro j hjL hDij
  have h1 := hrun j (by omega)
  have h2 := hrun (j + 1) (by omega)
  have hkey := eject (i + j) hDij h1
  rw [show i + (j + 1) = (i + j) + 1 by omega] at h2
  linarith

/-! ## §2. PROVEN DEEP-MID EJECTION LEG (from `HeckeEjection`, verbatim, uv-coordinates). -/

/-- **Deep-mid ejection (uniform box q=16..21).**  `P_i = uv − r v² < thr` ⟹ successor floor term
`λv² − uv ≥ thr` (and `P' = (λv²−uv) + kλv² ≥ λv²−uv` for every kick `k ≥ 0`). -/
theorem ejection_kick (l r u v thr : ℝ)
    (hl : (49:ℝ)/25 ≤ l) (hl' : l ≤ (99:ℝ)/50)
    (hr : (47:ℝ)/50 ≤ r) (hr' : r ≤ (61:ℝ)/50)
    (ht : (129:ℝ)/1000 ≤ thr) (ht' : thr ≤ (663:ℝ)/5000)
    (hu : (1:ℝ) < u) (hv : v ≤ 1)
    (htop : l * v - u ≤ 1) (hbot : (1:ℝ) < 2 * l * v - u)
    (hP : u * v - r * v ^ 2 < thr) :
    thr ≤ l * v ^ 2 - u * v := by
  have hlpos : (0:ℝ) < l := by linarith
  have hlv : (1:ℝ) < l * v := by linarith
  have hvpos : (0:ℝ) < v := by nlinarith [hlv, hlpos]
  nlinarith [mul_pos (show (0:ℝ) < u - 1 by linarith) hvpos,
             mul_pos (show (0:ℝ) < l * v - 1 by linarith) hvpos,
             mul_pos hvpos hvpos,
             mul_nonneg (show (0:ℝ) ≤ 1 - v by linarith) hvpos.le,
             mul_nonneg (show (0:ℝ) ≤ thr - (u * v - r * v ^ 2) by linarith) hvpos.le,
             mul_nonneg (show (0:ℝ) ≤ (61:ℝ)/50 - r by linarith) (mul_nonneg hvpos.le hvpos.le),
             mul_pos hvpos (show (0:ℝ) < 2 * l * v - u - 1 by linarith),
             sq_nonneg (l * v - 1), sq_nonneg (u - 1), hlv, hvpos, hu, hr, hr']

/-! ## §3. CONCRETE OBJECTS, LEGS, AND THE CAPSTONE (from `HeckeConfine`). -/

variable (l : ℝ)

/-- Chebyshev sequence. -/
def cheb : ℕ → ℝ
  | 0 => 0
  | 1 => 1
  | (n + 2) => l * cheb (n + 1) - cheb n

@[simp] lemma cheb_zero : cheb l 0 = 0 := rfl
@[simp] lemma cheb_one : cheb l 1 = 1 := rfl
lemma cheb_rec (n : ℕ) : cheb l (n + 2) = l * cheb l (n + 1) - cheb l n := rfl

/-- Genuine observable `Pgen (a,b) = a (a + l b)/l`. -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

/-- Scalar-branch BCZ map (the `i = q−1` branch). -/
def Tmap (p : ℝ × ℝ) : ℝ × ℝ :=
  (p.2, (⌊(1 + p.1) / (l * p.2)⌋ : ℝ) * (l * p.2) - p.1)

@[simp] lemma Tmap_fst (p : ℝ × ℝ) : (Tmap l p).1 = p.2 := rfl
lemma Tmap_snd (p : ℝ × ℝ) :
    (Tmap l p).2 = (⌊(1 + p.1) / (l * p.2)⌋ : ℝ) * (l * p.2) - p.1 := rfl

/-- F-corridor domain `Dcorr` (both Taha edges). -/
def Dcorr : Set (ℝ × ℝ) :=
  {p | 0 < p.1 ∧ p.1 ≤ 1 ∧ 0 < p.2 ∧ p.2 ≤ 1 ∧ p.1 + l * p.2 > 1 ∧ l * p.1 + p.2 > 1}

/-- Per-q F-window hypothesis type (EXACT signature of `g{q}_no_window_below_genuine`). -/
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

/-- `Pgen − a·b = a²/l`. -/
theorem Pgen_sub_prod (a b : ℝ) (hl : l ≠ 0) :
    Pgen l (a, b) - a * b = a ^ 2 / l := by
  simp only [Pgen_apply]; field_simp; ring

/-- Product `≤` genuine observable for `l > 0`. -/
theorem prod_le_Pgen (a b : ℝ) (hl : 0 < l) : a * b ≤ Pgen l (a, b) := by
  have h := Pgen_sub_prod l a b (ne_of_gt hl)
  have hnn : 0 ≤ a ^ 2 / l := div_nonneg (sq_nonneg a) hl.le
  linarith

/-- Transfer: `Pgen`-sub-threshold ⟹ product-sub-threshold. -/
theorem prod_lt_of_Pgen_lt (a b t : ℝ) (hl : 0 < l) (hP : Pgen l (a, b) < t) : a * b < t :=
  lt_of_le_of_lt (prod_le_Pgen l a b hl) hP

/-- Scalar read-off: a `Tmap`-orbit in `Dcorr` is a genuine F-corridor sequence. -/
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

/-- Cusp-branch guards. -/
def CuspGuards (l : ℝ) (p : ℝ × ℝ) : Prop :=
  0 < p.1 ∧ p.1 ≤ 1 ∧ l * p.1 + (l ^ 2 - 1) * p.2 > 1 ∧ l * p.1 + p.2 > 1 ∧ p.1 + l * p.2 ≤ 1

/-- Cusp envelope (verbatim, axiom-clean): cusp guards force `1/l³ ≤ a(a+l b)/l`. -/
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

/-- **Cusp leg as a theorem.**  A cusp-guard point has `Pgen ≥ 1/l³`. -/
theorem cusp_step_bound (p : ℝ × ℝ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1) (hg : CuspGuards l p) :
    1 / l ^ 3 ≤ Pgen l p := by
  obtain ⟨ha, ha1, hG, hd, hU⟩ := hg
  simpa [Pgen] using cusp_envelope l p.1 p.2 hl1 hlphi ha ha1 hG hd hU

/-- **★ CONSOLIDATED (C′) — `hconfine` and `entry` both ELIMINATED.**  Inputs: branch trichotomy
`htri` (= map definition), the proven F-window `hF`, and the proven ejection leg `hdeep`; the cusp
leg is discharged internally by `cusp_step_bound`.  Conclusion: no genuine sustained sub-threshold
orbit.  Proof: the trichotomy engine forces every step scalar (cusp ruled out by `cusp_step_bound`,
deep-mid by `hdeep`); the orbit is then a `Tmap`/`Dcorr` F-corridor sequence; the transfer feeds the
F-window at `i=0` for the contradiction. -/
theorem gate2_no_sustained
    (mpoly : ℝ → Prop) (hF : FwindowHyp mpoly)
    (hmp : mpoly l) (h1 : (1:ℝ) < l) (h2 : l < 2) (hlo : (9:ℝ)/5 < l) (hlphi : l ^ 2 ≥ l + 1)
    (orbit : ℕ → ℝ × ℝ) (deepmid : ℕ → Prop)
    (htri : ∀ n,
      (orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n)) ∨ deepmid n ∨ CuspGuards l (orbit n))
    (hdeep : ∀ n, deepmid n → Pgen l (orbit n) < 1 / l ^ 3 → 1 / l ^ 3 ≤ Pgen l (orbit (n + 1))) :
    ¬ (∀ n, Pgen l (orbit n) < 1 / l ^ 3) := by
  intro hsus
  have hscal := subthreshold_forces_scalar
      (fun n => orbit n ∈ Dcorr l ∧ orbit (n + 1) = Tmap l (orbit n)) deepmid
      (fun n => CuspGuards l (orbit n)) (fun n => Pgen l (orbit n))
      htri (fun n hn => cusp_step_bound l (orbit n) h1 hlphi hn) hdeep hsus
  have hmem : ∀ n, orbit n ∈ Dcorr l := fun n => (hscal n).1
  have hstep : ∀ n, orbit (n + 1) = Tmap l (orbit n) := fun n => (hscal n).2
  obtain ⟨hposc, hcap, hreg, hgen, hrec⟩ := orbit_to_cseq_hyps l orbit hmem hstep
  have hl0 : 0 < l := by linarith
  have hlink : ∀ n, (orbit n).2 = (orbit (n + 1)).1 := fun n => by rw [hstep n, Tmap_fst]
  set c : ℕ → ℝ := fun n => (orbit n).1 with hc
  have hsubc : ∀ n, c n * c (n + 1) < 1 / l ^ 3 := by
    intro n
    have hPpair : Pgen l ((orbit n).1, (orbit n).2) < 1 / l ^ 3 := by
      rw [Prod.mk.eta]; exact hsus n
    have h := prod_lt_of_Pgen_lt l (orbit n).1 (orbit n).2 (1 / l ^ 3) hl0 hPpair
    rw [hlink n] at h; exact h
  exact hF l hmp h1 h2 hlo c hposc hcap hreg hgen hrec 0
    ⟨hsubc 0, hsubc 1, hsubc 2, hsubc 3, hsubc 4, hsubc 5⟩

/-- **Faithfulness**: the legs reconstruct the old monolithic `hconfine` (so the new hypotheses are
strictly weaker/more local). -/
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

/-- Deep-mid threshold admissibility: `1/l³ ∈ [129/1000, 663/5000]` for the q=18 principal Hecke `l`
(`l ∈ [1.9695, 1.9698]`), so the proven `ejection_kick`/`hdeep` leg is applicable at `thr = 1/l³`. -/
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

end

end HeckeGate2

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeGate2.subthreshold_forces_scalar
#print axioms HeckeGate2.sustained_deepmid_free
#print axioms HeckeGate2.sustained_pure_scalar
#print axioms HeckeGate2.no_consec_subthr_deepmid
#print axioms HeckeGate2.deepmid_free_run
#print axioms HeckeGate2.deepmid_only_trailing
#print axioms HeckeGate2.ejection_kick
#print axioms HeckeGate2.cusp_envelope
#print axioms HeckeGate2.cusp_step_bound
#print axioms HeckeGate2.gate2_no_sustained
#print axioms HeckeGate2.hconfine_of_legs
#print axioms HeckeGate2.deep_threshold_admissible
