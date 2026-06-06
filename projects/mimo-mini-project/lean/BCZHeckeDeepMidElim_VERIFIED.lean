import Mathlib
/-!
# Deep-mid ELIMINATION from sub-threshold runs (GATE-2 structural reduction).

Rigorous form of "the multi-branch deep-middle zoo is provably dominated"
(FINDINGS_GATE2_multibranch_2026-06-05 had this NUMERICAL only): a genuine sub-threshold run of
length ≥ 2 contains NO deep-mid step. Hence GATE-2 ("no sustained sub-threshold orbit") reduces to
F-family (C1 scalar + C2 W_q) corridor confinement — the deep-mid dimension is eliminated.

Two per-step transition facts feed it, each discharged elsewhere (named-hypothesis honesty model):
  * `eject` = the PROVEN ejection lemma (`HeckeEjection.ejection_kick`,
    `lean/BCZHeckeEjection_q16to21_VERIFIED.lean`): a deep-mid sub-threshold step's SUCCESSOR is
    ≥ thr (dwell ≤ 1).  Abstracted to its conclusion.
  * `entry` = "a deep-mid step preceded by ANY sub-threshold step is itself ≥ thr."  NUMERICALLY
    VERIFIED (genuine map, q=17..21, 40k orbits × 500 steps: 0 deep-mid-sub-threshold step has a
    sub-threshold predecessor; min deep-mid product after a sub-threshold predecessor ≈ 0.16 ≫
    thr ≈ 0.13).  This is the new ingredient; it is a per-(q, branch) algebraic inequality of the
    same kick_pure/ejection flavour (non-vanishing margin ≈ 0.03), to be discharged like the
    ejection / window lemmas.  Stated here as a hypothesis.

`#print axioms` on every theorem must be `[propext, Classical.choice, Quot.sound]`, no `sorry`.
-/
namespace DeepMidElim

/-- **No two consecutive sub-threshold steps include a deep-mid step.**
Directly from `eject` (deep-mid ⇒ successor ≥ thr) and `entry` (deep-mid ⇐ predecessor ⇒ ≥ thr). -/
theorem no_consec_subthr_deepmid
    (thr : ℝ) (P : ℕ → ℝ) (isD : ℕ → Prop)
    (eject : ∀ n, isD n → P n < thr → thr ≤ P (n + 1))
    (entry : ∀ n, P n < thr → isD (n + 1) → thr ≤ P (n + 1))
    (n : ℕ) (hn : P n < thr) (hn1 : P (n + 1) < thr) :
    ¬ isD n ∧ ¬ isD (n + 1) := by
  refine ⟨?_, ?_⟩
  · intro hDn
    have := eject n hDn hn
    linarith
  · intro hDn1
    have := entry n hn hDn1
    linarith

/-- **A sub-threshold run of length ≥ 2 is deep-mid-free.**
If `P (i+j) < thr` for all `j ≤ L` with `L ≥ 1`, then NO step in the run is deep-mid.
(Interior steps `j < L` are excluded by `eject` via their successor; the last step `j = L` by
`entry` via its predecessor.)  This eliminates the deep-mid branches from any sustained
sub-threshold orbit ⇒ GATE-2 reduces to F-family corridor confinement. -/
theorem deepmid_free_run
    (thr : ℝ) (P : ℕ → ℝ) (isD : ℕ → Prop)
    (eject : ∀ n, isD n → P n < thr → thr ≤ P (n + 1))
    (entry : ∀ n, P n < thr → isD (n + 1) → thr ≤ P (n + 1))
    (i L : ℕ) (hL : 1 ≤ L)
    (hrun : ∀ j, j ≤ L → P (i + j) < thr) :
    ∀ j, j ≤ L → ¬ isD (i + j) := by
  intro j hj hDij
  rcases Nat.lt_or_ge j L with hjL | hjL
  · -- interior step: use ejection at (i+j), successor (i+j+1) is in the run
    have h1 := hrun j hj
    have h2 := hrun (j + 1) (by omega)
    have hkey := eject (i + j) hDij h1
    rw [show i + (j + 1) = (i + j) + 1 by omega] at h2
    linarith
  · -- last step j = L ≥ 1: use entry at predecessor (i+(j-1))
    obtain ⟨m, hm⟩ : ∃ m, j = m + 1 := ⟨j - 1, by omega⟩
    subst hm
    have hpred := hrun m (by omega)
    have hcur := hrun (m + 1) hj
    have hDcur : isD ((i + m) + 1) := by rw [show (i + m) + 1 = i + (m + 1) by omega]; exact hDij
    have hkey := entry (i + m) hpred hDcur
    rw [show (i + m) + 1 = i + (m + 1) by omega] at hkey
    linarith

/-- **UNCONDITIONAL (ejection only): deep-mid can occur only as the LAST step of a sub-threshold
run.** Uses ONLY `eject` (= the PROVEN `ejection_kick`), no `entry` hypothesis. Every interior step
`j < L` of a sub-threshold run is non-deep-mid; a deep-mid is possible only at the final position
`j = L`. This is the fully-proven (no new lemma) "deep-mid dwell ≤ 1 / only-trailing" reduction. -/
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

#print axioms no_consec_subthr_deepmid
#print axioms deepmid_free_run
#print axioms deepmid_only_trailing

end DeepMidElim
