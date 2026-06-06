import Mathlib
set_option maxHeartbeats 4000000
/-!
# WF5 avoid_cusp — the clean "sub-threshold ⟹ not on the cusp branch ⟹ interior" lemma.

A genuine orbit on Taha with EVERY genuine observable `Pgen < 1/l³` CANNOT sit on the cusp
(parabolic) branch `i = q−2`: on that branch the proven cusp envelope forces `Pgen ≥ 1/l³`
(the cusp observable is `s²/l > 1/l³` at the cusp tip, strictly super-threshold).  Hence a
sub-threshold orbit AVOIDS the cusp branch and is confined to the interior of the genuine
branch fan (the F-corridor + deep-mid branches).

CONTENT (additions only; all foundations inlined verbatim, axiom-clean):
* §A  inlined `cheb`, `L`, `Pgen`, the cusp boundary `L`-identities, `cusp_envelope`,
      `kick_bound_of_cusp`, `cusp_guards_of_branch`, `kick_bound_of_branch`
      (verbatim from BCZHeckeGenuineMap_allq_WIP / BCZHeckeCusp_envelope_allq_VERIFIED).
* §B  THE NEW RESULTS:
  - `subthreshold_not_cusp_guards`     : Pgen<1/l³ ⟹ the cusp-guard BUNDLE fails (¬ all five guards).
  - `subthreshold_not_cusp_branch`     : Pgen<1/l³ ⟹ the cusp-BRANCH predicate fails
                                          (¬ (entry ∧ active ∧ Taha-edge)) — the branch is not q−2.
  - `subthreshold_branchIdx_ne_cusp`   : Pgen<1/l³ ⟹ `branchIdx ≠ q−2` (selector lands off the cusp).
  - `subthreshold_confined_interior`   : the packaged statement — a sub-threshold Taha orbit is on a
                                          NON-cusp (interior) branch: its active index is ≠ q−2, and
                                          equivalently the cusp active form `a+l b ≤ 1` is RULED OUT,
                                          i.e. it lies strictly in the F-corridor / deep-mid region
                                          `a + l b > 1` (interior of the genuine fan).
  - `cusp_tip_super_threshold`         : non-vacuity — the cusp tip `(s,0)` HAS `Pgen = s²/l > 1/l³`,
                                          so the cusp branch is genuinely super-threshold (the orbit
                                          we exclude is real, and the exclusion is non-trivial).

`#print axioms` on every new theorem must be `[propext, Classical.choice, Quot.sound]`.
-/

namespace HeckeAvoidCusp

noncomputable section
variable (l : ℝ)

/-! ## §A. Inlined foundations (verbatim, axiom-clean). -/

/-- Chebyshev sequence `cheb l 0 = 0`, `cheb l 1 = 1`, `cheb l (n+2) = l·cheb(n+1) − cheb n`. -/
def cheb : ℕ → ℝ
  | 0 => 0
  | 1 => 1
  | (n + 2) => l * cheb (n + 1) - cheb n

@[simp] lemma cheb_zero : cheb l 0 = 0 := rfl
@[simp] lemma cheb_one : cheb l 1 = 1 := rfl
lemma cheb_rec (n : ℕ) : cheb l (n + 2) = l * cheb l (n + 1) - cheb l n := rfl

/-- Branch linear form `L_i(a,b) = a·cheb(i+1) + b·cheb(i)`. -/
def L (a b : ℝ) (i : ℕ) : ℝ := a * cheb l (i + 1) + b * cheb l i

/-- Genuine observable `P = a (a + l b)/l` (the assembly's `Pgen`). -/
def Pgen (l : ℝ) (p : ℝ × ℝ) : ℝ := p.1 * (p.1 + l * p.2) / l
@[simp] lemma Pgen_apply (l : ℝ) (p : ℝ × ℝ) : Pgen l p = p.1 * (p.1 + l * p.2) / l := rfl

open Classical in
/-- The active genuine branch index: the least `i` with `1 ≤ i ∧ L_i ≤ 1`. -/
noncomputable def branchIdx (a b : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) : ℕ :=
  Nat.find h

open Classical in
theorem branchIdx_spec (a b : ℝ) (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1) :
    1 ≤ branchIdx l a b h ∧ L l a b (branchIdx l a b h) ≤ 1 ∧
      ∀ j, j < branchIdx l a b h → ¬ (1 ≤ j ∧ L l a b j ≤ 1) := by
  refine ⟨(Nat.find_spec h).1, (Nat.find_spec h).2, ?_⟩
  intro j hj; exact Nat.find_min h hj

/-- **Cusp-branch envelope, all q** (verbatim, axiom-clean). -/
theorem cusp_envelope (l a b : ℝ)
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

/-- **Kick bound from `cusp_envelope`** (verbatim). -/
theorem kick_bound_of_cusp
    {l a b : ℝ} (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hcuspGuards : 0 < a ∧ a ≤ 1 ∧ l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1) :
    1 / l ^ 3 ≤ Pgen l (a, b) := by
  obtain ⟨ha, ha1, hG, hd, hU⟩ := hcuspGuards
  simpa [Pgen] using cusp_envelope l a b hl1 hlphi ha ha1 hG hd hU

theorem cheb_cusp_m2 (m : ℕ) (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1) :
    cheb l (m + 2) = l := by
  have hrec : cheb l (m + 4) = l * cheb l (m + 3) - cheb l (m + 2) := cheb_rec l (m + 2)
  rw [hq0, hq1] at hrec; linarith

theorem cheb_cusp_m1 (m : ℕ) (hq1 : cheb l (m + 3) = 1) (hm2 : cheb l (m + 2) = l) :
    cheb l (m + 1) = l ^ 2 - 1 := by
  have hrec : cheb l (m + 3) = l * cheb l (m + 2) - cheb l (m + 1) := cheb_rec l (m + 1)
  rw [hq1, hm2] at hrec; nlinarith [hrec]

theorem L_cusp_active (a b : ℝ) (m : ℕ)
    (hq1 : cheb l (m + 3) = 1) (hm2 : cheb l (m + 2) = l) :
    L l a b (m + 2) = a + l * b := by
  simp only [L, show m + 2 + 1 = m + 3 from rfl, hq1, hm2]; ring

theorem L_cusp_entry (a b : ℝ) (m : ℕ)
    (hm2 : cheb l (m + 2) = l) (hm1 : cheb l (m + 1) = l ^ 2 - 1) :
    L l a b (m + 1) = l * a + (l ^ 2 - 1) * b := by
  simp only [L, show m + 1 + 1 = m + 2 from rfl, hm2, hm1]; ring

/-- **CUSP-GUARD MEMBERSHIP** (verbatim). -/
theorem cusp_guards_of_branch (a b : ℝ) (m : ℕ)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1)) (hactive : L l a b (m + 2) ≤ 1)
    (htaha : 1 - l * a < b) :
    l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1 := by
  have hm2 : cheb l (m + 2) = l := cheb_cusp_m2 l m hq0 hq1
  have hm1 : cheb l (m + 1) = l ^ 2 - 1 := cheb_cusp_m1 l m hq1 hm2
  have hLa : L l a b (m + 2) = a + l * b := L_cusp_active l a b m hq1 hm2
  have hLe : L l a b (m + 1) = l * a + (l ^ 2 - 1) * b := L_cusp_entry l a b m hm2 hm1
  refine ⟨?_, ?_, ?_⟩
  · rw [hLe] at hentry; linarith
  · linarith [htaha]
  · rw [hLa] at hactive; linarith

/-- **CUSP BRANCH ⟹ KICK BOUND** (verbatim). -/
theorem kick_bound_of_branch (a b : ℝ) (m : ℕ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1)) (hactive : L l a b (m + 2) ≤ 1)
    (htaha : 1 - l * a < b) :
    1 / l ^ 3 ≤ Pgen l (a, b) := by
  obtain ⟨hG1, hG2, hG3⟩ := cusp_guards_of_branch l a b m hq0 hq1 hentry hactive htaha
  exact kick_bound_of_cusp hl1 hlphi ⟨ha, ha1, hG1, hG2, hG3⟩

/-! ## §B. THE NEW RESULTS — the sub-threshold ⟹ not-cusp ⟹ interior chain.

These are the clean contrapositive of `cusp_envelope` / `kick_bound_of_cusp` /
`kick_bound_of_branch`: if the genuine observable is STRICTLY below `1/l³`, the orbit point cannot
satisfy the cusp-branch guards, hence cannot be the active cusp branch `i = q−2`, hence is confined
to the interior (`a + l b > 1`, the F-corridor / deep-mid region). -/

/-- **Sub-threshold ⟹ the cusp-guard bundle FAILS.**  Pure contrapositive of `kick_bound_of_cusp`:
if `Pgen (a,b) < 1/l³` then the five cusp guards `(0<a, a≤1, G1, G2, G3)` cannot all hold (else the
cusp envelope would force `Pgen ≥ 1/l³`).  This is the atomic obstruction. -/
theorem subthreshold_not_cusp_guards {l a b : ℝ}
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (hsub : Pgen l (a, b) < 1 / l ^ 3) :
    ¬ (0 < a ∧ a ≤ 1 ∧ l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1) := by
  intro hguards
  exact absurd (kick_bound_of_cusp hl1 hlphi hguards) (not_le.mpr hsub)

/-- **Sub-threshold ⟹ NOT on the cusp branch (branch-predicate form).**  On the cusp branch
`i = q−2 = m+2` the active predicate is `L_{m+2} ≤ 1`, the entry predicate `1 < L_{m+1}`, and the
Taha lower edge `1 − l a < b`; together with `0 < a ≤ 1` these ARE the cusp guards.  So if
`Pgen < 1/l³`, the orbit point CANNOT simultaneously be in the cusp `a`-domain and satisfy the
cusp branch's entry/active predicates and the Taha edge: it is not the `q−2` branch. -/
theorem subthreshold_not_cusp_branch {l a b : ℝ} (m : ℕ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hsub : Pgen l (a, b) < 1 / l ^ 3) :
    ¬ (1 < L l a b (m + 1) ∧ L l a b (m + 2) ≤ 1 ∧ 1 - l * a < b) := by
  rintro ⟨hentry, hactive, htaha⟩
  exact absurd (kick_bound_of_branch l a b m hl1 hlphi ha ha1 hq0 hq1 hentry hactive htaha)
    (not_le.mpr hsub)

/-- **Sub-threshold + Taha edge ⟹ the cusp ACTIVE form is ruled out: `a + l b > 1` (interior).**
The cusp active predicate is `L_{m+2} = a + l b ≤ 1`.  Under the Taha lower edge (always available
on the genuine domain) and the cusp `a`-domain `0 < a ≤ 1`, sub-threshold FORCES `a + l b > 1`,
i.e. the point lies strictly INSIDE the F-corridor / deep-mid region — the interior of the genuine
branch fan, off the cusp face.  (This is the geometric content: the cusp branch is the face
`a + l b ≤ 1`; sub-threshold pushes you off it into `a + l b > 1`.) -/
theorem subthreshold_interior {l a b : ℝ} (m : ℕ)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1))
    (htaha : 1 - l * a < b)
    (hsub : Pgen l (a, b) < 1 / l ^ 3) :
    1 < a + l * b := by
  -- boundary cheb values to rewrite the active branch into `a + l b`
  have hm2 : cheb l (m + 2) = l := cheb_cusp_m2 l m hq0 hq1
  have hLa : L l a b (m + 2) = a + l * b := L_cusp_active l a b m hq1 hm2
  by_contra hcon
  push_neg at hcon  -- a + l b ≤ 1
  -- then the cusp active predicate holds, contradicting sub-threshold
  have hactive : L l a b (m + 2) ≤ 1 := by rw [hLa]; exact hcon
  exact subthreshold_not_cusp_branch m hl1 hlphi ha ha1 hq0 hq1 hsub ⟨hentry, hactive, htaha⟩

/-- **Sub-threshold ⟹ the SELECTOR avoids the cusp index: `branchIdx ≠ q−2`.**  The genuine active
branch is `i = branchIdx l a b h` (least `i≥1` with `L_i ≤ 1`).  If it equalled the cusp index
`m+2`, then `branchIdx_spec` would certify the cusp active predicate `L_{m+2} ≤ 1`; together with the
cusp `a`-domain, the entry predicate, and the Taha edge this is the cusp branch — excluded by
sub-threshold.  Hence the selected branch is strictly off the cusp: `branchIdx ≠ m+2`. -/
theorem subthreshold_branchIdx_ne_cusp {l a b : ℝ} (m : ℕ)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1))
    (htaha : 1 - l * a < b)
    (hsub : Pgen l (a, b) < 1 / l ^ 3) :
    branchIdx l a b h ≠ m + 2 := by
  intro heq
  -- the selector certifies L at the selected (= cusp) index is ≤ 1
  have hact_sel : L l a b (branchIdx l a b h) ≤ 1 := (branchIdx_spec l a b h).2.1
  rw [heq] at hact_sel  -- L l a b (m+2) ≤ 1  (the cusp active predicate)
  exact subthreshold_not_cusp_branch m hl1 hlphi ha ha1 hq0 hq1 hsub ⟨hentry, hact_sel, htaha⟩

/-- **PACKAGED CAPSTONE — sub-threshold ⟹ confined to the interior (off the cusp branch).**
A genuine orbit point `(a,b)` on the cusp `a`-domain `0<a≤1`, satisfying the Taha lower edge and the
cusp entry predicate, whose genuine observable is sub-threshold `Pgen (a,b) < 1/l³`, simultaneously:
  (i)   FAILS the full cusp-guard bundle (`subthreshold_not_cusp_guards`),
  (ii)  is NOT on the cusp branch (`subthreshold_not_cusp_branch`: ¬ entry∧active∧edge),
  (iii) lies in the INTERIOR `a + l b > 1` (off the cusp face `a + l b ≤ 1`), and
  (iv)  the SELECTOR avoids the cusp index `branchIdx ≠ q−2`.
This is the clean "sub-threshold ⟹ not cusp branch ⟹ interior" lemma: a sub-threshold orbit is
confined to the F-corridor + deep-mid branches, never the cusp/parabolic branch. -/
theorem subthreshold_confined_interior {l a b : ℝ} (m : ℕ)
    (h : ∃ i, 1 ≤ i ∧ L l a b i ≤ 1)
    (hl1 : 1 < l) (hlphi : l ^ 2 ≥ l + 1)
    (ha : 0 < a) (ha1 : a ≤ 1)
    (hq0 : cheb l (m + 4) = 0) (hq1 : cheb l (m + 3) = 1)
    (hentry : 1 < L l a b (m + 1))
    (htaha : 1 - l * a < b)
    (hsub : Pgen l (a, b) < 1 / l ^ 3) :
    (¬ (0 < a ∧ a ≤ 1 ∧ l * a + (l ^ 2 - 1) * b > 1 ∧ l * a + b > 1 ∧ a + l * b ≤ 1))
      ∧ (¬ (1 < L l a b (m + 1) ∧ L l a b (m + 2) ≤ 1 ∧ 1 - l * a < b))
      ∧ (1 < a + l * b)
      ∧ (branchIdx l a b h ≠ m + 2) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact subthreshold_not_cusp_guards hl1 hlphi hsub
  · exact subthreshold_not_cusp_branch m hl1 hlphi ha ha1 hq0 hq1 hsub
  · exact subthreshold_interior m hl1 hlphi ha ha1 hq0 hq1 hentry htaha hsub
  · exact subthreshold_branchIdx_ne_cusp m h hl1 hlphi ha ha1 hq0 hq1 hentry htaha hsub

/-! ## §C. NON-VACUITY — the cusp branch is genuinely super-threshold (the excluded orbit is real). -/

/-- On the cusp tip `(s,0)` the genuine observable is `Pgen l (s,0) = s²/l`. -/
theorem cusp_Pgen (s : ℝ) : Pgen l (s, 0) = s ^ 2 / l := by
  simp only [Pgen, mul_zero, add_zero]; ring

/-- **NON-VACUITY: the cusp branch is STRICTLY super-threshold.**  At the cusp tip `(s,0)` with
`s ∈ (1/l, 1]` the genuine observable is `Pgen = s²/l > 1/l³`.  So the cusp branch is NOT
sub-threshold — confirming the exclusion `subthreshold_confined_interior` is non-trivial: there
genuinely IS mass on the cusp branch, and it sits ABOVE the threshold, which is precisely why a
sub-threshold orbit must avoid it.  (Witness for the non-emptiness law: the cusp tip realizes the
super-threshold value the envelope guarantees.) -/
theorem cusp_tip_super_threshold {l s : ℝ} (hl : 0 < l) (h1 : 1 / l < s) :
    1 / l ^ 3 < Pgen l (s, 0) := by
  rw [cusp_Pgen l s]
  -- 1/l³ < s²/l  from  1/l < s  (both positive)
  set t := 1 / l with ht
  have htpos : 0 < t := by rw [ht]; positivity
  have hts : t < s := h1
  have h1l : 1 / l ^ 3 = t ^ 3 := by rw [ht]; ring
  have h2l : s ^ 2 / l = s ^ 2 * t := by rw [ht]; ring
  rw [h1l, h2l]
  nlinarith [mul_pos htpos (mul_pos (show (0:ℝ) < s - t by linarith)
                                    (show (0:ℝ) < s + t by linarith))]

end

end HeckeAvoidCusp

-- ════════════ AXIOM AUDIT ════════════
#print axioms HeckeAvoidCusp.subthreshold_not_cusp_guards
#print axioms HeckeAvoidCusp.subthreshold_not_cusp_branch
#print axioms HeckeAvoidCusp.subthreshold_interior
#print axioms HeckeAvoidCusp.subthreshold_branchIdx_ne_cusp
#print axioms HeckeAvoidCusp.subthreshold_confined_interior
#print axioms HeckeAvoidCusp.cusp_tip_super_threshold
