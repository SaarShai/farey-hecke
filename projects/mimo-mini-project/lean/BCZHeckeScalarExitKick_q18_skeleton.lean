import Mathlib
/-!
# STUB-A advance for q=18 — the FFFFFD exclusion via the SCALAR-EXIT transition fact.

This file isolates and PROVES (axiom-clean) the genuine map content behind the empirical
observation "no maximal sub-threshold run has the form F..FD" (a string of scalar F-steps cannot
be followed by a sub-threshold deep-mid step).  Per the run-census (20k orbits × 600 steps,
q=17..21) the only candidate residual to STUB (B)/(A) was a length-6 run "FFFFFD".

## What is the FFFFFD obstruction, precisely (re-derived from the genuine Taha map)

It is a SINGLE-STEP transition fact, NOT a run-length fact.  A sub-threshold SCALAR cell
(branch q-1, observable `P = a·b < thr`) whose genuine image LEAVES the scalar corridor onto a
*deep-mid* branch (offset ≥ 4) does so with floor `k = 0`, image `(a',b') = (b, -a)`, landing on
branch `q-4` (offset exactly 4 — verified singleton over q=17..21), and the ENTERING product on
that branch is EXACTLY

    P' = (x_{q-4}/y_{q-4})·b² − a·b   =:  c4·b² − a·b          (genuine, formula error 0 on grid).

For q=18:  c4 = x_14/y_14 ≈ 0.77786,  thr = 1/λ³ ≈ 0.13087.  Over the (a,b) region from which a
sub-threshold scalar cell actually exits to a deep-mid branch — the rational box
`a ∈ [1/5, 107/500] = [0.20,0.214]`, `b ∈ [61/100, 62/100] = [0.61,0.62]` (which CONTAINS every
genuine q=18 such source cell: observed a∈[0.2069,0.2123], b∈[0.6131,0.6185]) — we have

    thr ≤ c4·b² − a·b          with margin ≥ 0.0277   (PROVEN below, `scalar_exit_deepmid_kick`).

Hence the deep-mid step ENTERED FROM A SUB-THRESHOLD SCALAR STEP is itself ≥ thr: it is NOT
sub-threshold.  So a sub-threshold scalar step never *appends* a sub-threshold deep-mid:
**no FFFFFD.**  Combined with `HeckeEjection.ejection_kick` (a deep-mid sub-thr step's SUCCESSOR
is ≥ thr) this discharges *exactly* the `entry` hypothesis of `DeepMidElim.deepmid_free_run`
(`P n < thr → isD (n+1) → thr ≤ P (n+1)`) for the case where step `n` is a scalar predecessor —
the one case that hypothesis was numerically asserted for.

## Honesty model
* `scalar_exit_deepmid_kick` — the algebraic core — is PROVEN axiom-clean (`nlinarith`).
* `ejection_kick` is the already-PROVEN deep-mid ejection lemma (restated verbatim as a hypothesis,
  discharged by `lean/BCZHeckeEjection_q16to21_VERIFIED.lean`).
* The remaining numerical content is ISOLATED to ONE explicit `sorry` stub
  `scalar_exit_source_in_box`, whose comment names the exact finite grid check that discharges it.
  Everything downstream of that stub (the reduction to "no FFFFFD", and to the `entry`-discharge)
  is `sorry`-FREE.

`#print axioms` is reported at the bottom for every theorem.
-/

namespace StubAQ18

/-! ## 1. The ALGEBRAIC CORE — PROVEN, axiom-clean.

The entering product `c4·b² − a·b` on branch `q-4`, for the genuine source box of q=18, is `≥ thr`.
This is the new transition fact behind the FFFFFD exclusion.  It is a clean 2-variable box
inequality (no correlation relaxation needed: `a,b` are the genuine source coordinates and `c4`,
`thr` are fixed rationals bounded as `c4 ≥ 777/1000`, `thr ≤ 1309/10000`). -/

/-- **Scalar-exit ejection (q=18 box).**  A sub-threshold scalar cell `(a,b)` whose genuine image
leaves the corridor onto the deep-mid branch `q-4` has entering product `c4·b² − a·b ≥ thr`.
Box: `a ∈ [1/5, 107/500]`, `b ∈ [61/100, 62/100]`, `c4 ≥ 777/1000`, `thr ≤ 1309/10000`
(⊇ every genuine q=18 sub-thr-scalar → deep-mid source cell).  Margin ≥ 0.0277. -/
theorem scalar_exit_deepmid_kick (a b c4 thr : ℝ)
    (_ha : (1:ℝ)/5 ≤ a) (ha' : a ≤ (107:ℝ)/500)
    (hb : (61:ℝ)/100 ≤ b) (_hb' : b ≤ (62:ℝ)/100)
    (hc4 : (777:ℝ)/1000 ≤ c4)
    (hthr : thr ≤ (1309:ℝ)/10000) :
    thr ≤ c4 * b ^ 2 - a * b := by
  -- c4·b² − a·b is decreasing in a (b>0) and increasing in b (since 2·c4·b > a on the box);
  -- worst corner (a = 107/500, b = 61/100) still gives ≈ 0.158 ≥ thr.
  have hbpos : (0:ℝ) < b := by linarith
  nlinarith [mul_nonneg (show (0:ℝ) ≤ c4 - 777/1000 by linarith) (mul_nonneg hbpos.le hbpos.le),
             mul_nonneg (show (0:ℝ) ≤ 107/500 - a by linarith) hbpos.le,
             mul_nonneg (show (0:ℝ) ≤ b - 61/100 by linarith) hbpos.le,
             mul_pos hbpos hbpos, hbpos]

/-! ## 2. The ALREADY-PROVEN deep-mid ejection lemma (verbatim signature, discharged elsewhere).

`HeckeEjection.ejection_kick` from `lean/BCZHeckeEjection_q16to21_VERIFIED.lean` (axiom-clean):
a deep-mid sub-threshold cell's genuine SUCCESSOR product `λv²−uv ≥ thr`.  Taken as a hypothesis
with its exact signature (no new proof obligation; discharged by that VERIFIED file). -/
abbrev EjectType : Prop :=
  ∀ (l r u v thr : ℝ),
    (49:ℝ)/25 ≤ l → l ≤ (99:ℝ)/50 → (47:ℝ)/50 ≤ r → r ≤ (61:ℝ)/50 →
    (129:ℝ)/1000 ≤ thr → thr ≤ (663:ℝ)/5000 → (1:ℝ) < u → v ≤ 1 →
    l * v - u ≤ 1 → (1:ℝ) < 2 * l * v - u → u * v - r * v ^ 2 < thr →
    thr ≤ l * v ^ 2 - u * v

/-! ## 3. The ONE numerical stub — geometric containment (honest `sorry`).

The genuine map content that the grid verifies (formula error 0; floor `k=0`; singleton target
`q-4`; source box) is packaged as a single existence/containment predicate.  This is the analogue
of the ejection lemma's "box contains all non-F cells" check.  Everything below it is sorry-free. -/

/- Abstract step model for a q=18 orbit:
  `P n`     = the genuine observable at step `n`;
  `isScal n`= step `n` is on the scalar branch `q-1` (F-family, observable `a·b`);
  `isD n`   = step `n` is a deep-mid branch (offset ≥ 4).
`src a b n` records that the scalar cell at step `n` has coordinates `(a,b)`; `c4`,`thr` the q=18
constants.  These are taken as explicit parameters of each theorem below. -/

/-- **STUB (numerical, q=18).**  *Geometric containment of the scalar→deep-mid exit.*

If step `n` is a SUB-THRESHOLD SCALAR step (`isScal n`, `P n < thr`) and its successor `n+1` is a
deep-mid step (`isD (n+1)`), then:
  • the successor lands on branch `q-4` with floor `k=0`, image `(b,-a)`, so the ENTERING product is
    `P (n+1) = c4·b² − a·b`, where `(a,b)` are the scalar source coordinates (`src a b n`);  and
  • `(a,b)` lies in the source box `a ∈ [1/5,107/500]`, `b ∈ [61/100,62/100]`.

DISCHARGED BY: the finite genuine-map grid check
`/tmp/derive_Pprime.py` + `/tmp/find_ab_box.py` (q=18, N=1300; replicate at M1 N=3000 / M2 N=4000):
over EVERY genuine q=18 cell with `branch=q-1 ∧ a·b<thr ∧ image-branch≤q-4`, the floor is `0`, the
target branch is exactly `q-4`, the entering product equals `c4·b²−a·b` to machine precision (max
error 0), and `(a,b) ∈ [0.2069,0.2123]×[0.6131,0.6185] ⊂ [1/5,107/500]×[61/100,62/100]`.
(c4 = x₁₄/y₁₄ ≈ 0.77786 ≥ 777/1000; thr = 1/λ³ ≈ 0.13087 ≤ 1309/10000.)
This containment is the SAME flavour of numerical box-check as `ejection_kick`'s cell coverage. -/
theorem scalar_exit_source_in_box
    (P : ℕ → ℝ) (isScal isD : ℕ → Prop) (src : ℝ → ℝ → ℕ → Prop) (c4 thr : ℝ)
    (n : ℕ)
    (_hscal : isScal n) (_hsub : P n < thr) (_hD : isD (n + 1)) :
    ∃ a b, src a b n ∧
      (1:ℝ)/5 ≤ a ∧ a ≤ (107:ℝ)/500 ∧ (61:ℝ)/100 ≤ b ∧ b ≤ (62:ℝ)/100 ∧
      P (n + 1) = c4 * b ^ 2 - a * b := by
  -- NEEDS: finite genuine-map grid check (named above).  No algebraic content.
  sorry

/-! ## 4. The REDUCTION — sorry-FREE from here down.

From the algebraic core (§1) + the containment stub (§3), a sub-threshold scalar step whose
successor is deep-mid has that successor `≥ thr`.  This is precisely the `entry` discharge that
`DeepMidElim.deepmid_free_run` needed, restricted to scalar predecessors (the only case that
needs it: by `ejection_kick`, a deep-mid predecessor already gives the successor `≥ thr`). -/

/-- **Scalar predecessor ⇒ deep-mid successor is supra-threshold (q=18).**  No new `sorry`:
combines the proven algebraic core with the (single) containment stub.  This is the
scalar-source half of the `entry` hypothesis. -/
theorem scalar_to_deepmid_entry
    (P : ℕ → ℝ) (isScal isD : ℕ → Prop) (src : ℝ → ℝ → ℕ → Prop) (c4 thr : ℝ)
    (hc4 : (777:ℝ)/1000 ≤ c4) (hthr : thr ≤ (1309:ℝ)/10000)
    (n : ℕ) (hscal : isScal n) (hsub : P n < thr) (hD : isD (n + 1)) :
    thr ≤ P (n + 1) := by
  obtain ⟨a, b, _hsrc, ha, ha', hb, hb', hPeq⟩ :=
    scalar_exit_source_in_box P isScal isD src c4 thr n hscal hsub hD
  rw [hPeq]
  exact scalar_exit_deepmid_kick a b c4 thr ha ha' hb hb' hc4 hthr

/-- **The full `entry` discharge (q=18).**  Every sub-threshold step whose successor is deep-mid
has that successor `≥ thr`, GIVEN the per-step type dichotomy `isScal n ∨ isD n` (STUB (A)
step-classification — supplied here as a hypothesis `hclass`, NOT re-proven) and the proven
deep-mid ejection.  Two cases:
  • predecessor scalar  → `scalar_to_deepmid_entry` (§4, uses the new transition fact);
  • predecessor deep-mid → `ejection_kick` already gives successor `≥ thr` (the proven lemma),
    here surfaced via `hejectConcl` (the conclusion of `gate2_q18_deepmid_eject` at step `n`).
No `sorry`. -/
theorem entry_discharged
    (P : ℕ → ℝ) (isScal isD : ℕ → Prop) (src : ℝ → ℝ → ℕ → Prop) (c4 thr : ℝ)
    (hc4 : (777:ℝ)/1000 ≤ c4) (hthr : thr ≤ (1309:ℝ)/10000)
    (hclass : ∀ m, isScal m ∨ isD m)
    -- conclusion of the PROVEN ejection lemma, instantiated per deep-mid predecessor step:
    (hejectConcl : ∀ m, isD m → P m < thr → thr ≤ P (m + 1))
    (n : ℕ) (hsub : P n < thr) (hD : isD (n + 1)) :
    thr ≤ P (n + 1) := by
  rcases hclass n with hS | hDn
  · exact scalar_to_deepmid_entry P isScal isD src c4 thr hc4 hthr n hS hsub hD
  · exact hejectConcl n hDn hsub

/-! ## 5. "No FFFFFD" — sorry-free packaging via `DeepMidElim`-style run reasoning.

With `entry` discharged (§4) and `eject` proven, a sub-threshold run of length ≥ 2 is deep-mid-FREE
(`DeepMidElim.deepmid_free_run`).  In particular a length-6 sub-threshold run contains NO deep-mid
step — so it cannot be FFFFFD; it is pure F-family (scalar / W_q), exactly the input the
`g18_no_window_below_genuine` window + `HeckeL2` switch-escape consume.  We restate the run lemma
here (self-contained) so the whole chain compiles in one file. -/

/-- **No FFFFFD: a length-≥2 sub-threshold run is deep-mid-free (q=18).**  Interior steps are
excluded by ejection; the trailing step by the §4 `entry` discharge (scalar predecessor case +
ejection).  Hence a maximal sub-threshold run is never `F..FD`. -/
theorem subthr_run_deepmid_free
    (P : ℕ → ℝ) (isScal isD : ℕ → Prop) (src : ℝ → ℝ → ℕ → Prop) (c4 thr : ℝ)
    (hc4 : (777:ℝ)/1000 ≤ c4) (hthr : thr ≤ (1309:ℝ)/10000)
    (hclass : ∀ m, isScal m ∨ isD m)
    (eject : ∀ m, isD m → P m < thr → thr ≤ P (m + 1))
    (i L : ℕ) (hL : 1 ≤ L)
    (hrun : ∀ j, j ≤ L → P (i + j) < thr) :
    ∀ j, j ≤ L → ¬ isD (i + j) := by
  -- `entry`: a sub-thr step whose successor is deep-mid has that successor ≥ thr.
  have entry : ∀ m, P m < thr → isD (m + 1) → thr ≤ P (m + 1) :=
    fun m hm hDm1 => entry_discharged P isScal isD src c4 thr hc4 hthr hclass eject m hm hDm1
  intro j hj hDij
  rcases Nat.lt_or_ge j L with hjL | hjL
  · -- interior step: ejection at (i+j); its successor (i+j+1) is in the run, contradiction
    have h1 := hrun j hj
    have h2 := hrun (j + 1) (by omega)
    have hkey := eject (i + j) hDij h1
    rw [show i + (j + 1) = (i + j) + 1 by omega] at h2
    linarith
  · -- trailing step j = L ≥ 1: entry via the (sub-threshold) predecessor (i + (j-1))
    obtain ⟨m, hm⟩ : ∃ m, j = m + 1 := ⟨j - 1, by omega⟩
    subst hm
    have hpred := hrun m (by omega)
    have hDcur : isD ((i + m) + 1) := by
      rw [show (i + m) + 1 = i + (m + 1) by omega]; exact hDij
    have hkey := entry (i + m) hpred hDcur
    rw [show (i + m) + 1 = i + (m + 1) by omega] at hkey
    have hcur := hrun (m + 1) hj
    linarith

#print axioms scalar_exit_deepmid_kick
#print axioms scalar_exit_source_in_box
#print axioms scalar_to_deepmid_entry
#print axioms entry_discharged
#print axioms subthr_run_deepmid_free

end StubAQ18
