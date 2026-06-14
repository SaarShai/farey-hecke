# Adversarial verification — the "biggest win" (X_Ω(q) = 1/λ_q³)

Date: 2026-06-14. Mandate: refute, not confirm. Three fronts.

Claim under attack (as handed to the auditor):
> "We proved, by a single family-uniform method, that for every Hecke triangle group
> G_q the ergodic-optimization ground value of the gap-product P on Taha's G_q-BCZ
> section is exactly X_Ω(q) = 1/λ_q³, machine-verified unconditional for q=5..21.
> Corollary: bounded-cluster ceiling B(q)=2 iff G_q arithmetic. NEW mathematics: first
> family-uniform L∞ support-edge result; local statistic detecting global arithmeticity."

---

## FRONT 1 — Independent numerics. VERDICT: PARTIAL (lower bound SURVIVES; EQUALITY unwitnessed; "unconditional q=5..21" is for the ≥ bound only).

I re-implemented Taha's scalar G_q-BCZ map from scratch (float64 + mpmath, no repo code):
  T(a,b) = (b, ⌊(1+a)/(λb)⌋·λb − a),  P(a,b)=a·b,
  λ_q = 2cos(π/q), corridor Dcorr = {0<a≤1, 0<b≤1, a+λb>1, λa+b>1}.

(a) LOWER BOUND — could NOT falsify. For q=5,7,8 I ran ~4·10⁵ corridor-edge-biased
    seeds × 3000-step orbits. EVERY orbit that STAYS in Dcorr has running-sup P strictly
    above 1/λ³:
      q=5:  inf over staying orbits of sup-P = 0.327  (ratio 1.386 × 1/λ³)
      q=7:  0.433 (ratio 2.54)
      q=8:  0.499 (ratio 3.15)
    Orbits that LEAVE Dcorr have sup-P far below 1/λ³ (ratio 0.02–0.04) — but those
    violate the theorem's hypothesis (hmem: ∀n, orbit n ∈ Dcorr), so they are NOT
    counterexamples. No staying orbit ever dipped sup-P below 1/λ³. The ≥ claim holds.

(b) TIGHTNESS / EQUALITY — NOT witnessed by any interior orbit. The minimizing orbit is
    never found (ratios stay 1.4–4.8). The reason is structural and now understood:
    1/λ_q³ is EXACTLY the cusp-tip value of the genuine observable P_gen=a(a+λb)/λ at the
    section corner (1/λ, 0) — verified to machine precision for q=5,7,8,13. The tight
    "measure" attaining 1/λ³ is the Dirac mass at the cusp tip (a degenerate / boundary,
    measure-zero object), NOT an interior orbit. So the equality X_Ω(q)=1/λ³ relies on the
    cusp-tip Dirac as the matching UPPER bound — which is NOT in the Lean footprint
    (see Front 3) and is only a recorded numerical/structural witness.

(c) The pure elliptic-rotation picture (Koyama "energy" = invariant ellipse) gives a
    corridor-inscribed ellipse whose MAX of P is BELOW 1/λ³ (ratio 0.61–0.84). The hard
    edge therefore is NOT a property of the rotation alone — it is produced by the floor
    (deep-mid/cusp ejection). This is consistent with the proof architecture (the F-window
    + ejection lemmas are load-bearing, not decorative).

(d) q=13: ZERO orbits stayed in Dcorr for ≥3000 steps out of 4·10⁵ seeds. The corridor is
    barely forward-invariant for larger q; the invariant measures supported on Dcorr are
    extremely thin. The theorem is non-vacuous (the F-window lemma is a genuine negation,
    Front 3) but the set of invariant measures it ranges over is hard to exhibit numerically.

Numeric reproduction of 1/λ³ to ≥6 digits: yes for the cusp-tip value (it is an exact
algebraic identity). The ground-value EQUALITY is not numerically reproducible as an
interior-orbit infimum because the minimizer is a boundary Dirac.

---

## FRONT 2 — Prior art / novelty. VERDICT: REFUTED as stated; SURVIVES only in a narrow rebadged form.

The claim "first family-uniform L∞ support-edge result; field previously did one surface
per paper" is FALSE as worded. The qualitative result and a family-uniform method both
predate this work by 5–13 years.

1. HARD SUPPORT EDGE (= "no small gaps") IS OLD AND QUALITATIVELY GENERAL.
   Athreya–Chaika (cited as [2] in the Veech literature): a translation surface is a
   lattice (Veech) surface IFF its renormalized slope-gap distribution has lim inf bounded
   away from 0 — i.e. lattice surfaces "never have support at zero." The positive support
   edge for Veech/Hecke surfaces is exactly this published dichotomy.

2. THE q=5 CASE IS PUBLISHED WITH AN EXACT HARD EDGE (2013).
   Athreya–Chaika–Lelièvre, "The gap distribution of slopes on the golden L"
   (arXiv:1308.4203), Remark 2 (quoted verbatim from the PDF):
     "The distribution has no support at 0, in fact f(x)=0 for 0≤x≤1. The tail … is
      quadratic …"
   The golden L = double pentagon = the Hecke G_5 surface. So the hard L∞ support edge for
   q=5 is a 2013 theorem (in their normalization the edge is at 1; the repo's 1/λ³ is the
   same phenomenon in the P-product variable).

3. THE 2n-GON / Hecke family edge is published (2021).
   Slope Gap Distribution of Saddle Connections on the 2n-gon (arXiv:2109.04495):
   Theorem 1.1 — piecewise-analytic, finitely many non-differentiability points,
   "has no support at 0," quadratic tail. The 2n-gon Veech group is a Hecke triangle group;
   the double-(2n+1)-gon Veech group is exactly H_{2n+1}.

4. A FAMILY-UNIFORM METHOD ALREADY EXISTS (2021).
   Kumanduri–Sanchez–Wang, "Slope Gap Distributions of Veech Surfaces" (arXiv:2102.10069):
   gives a UNIFORM construction via an explicit Poincaré section to the horocycle flow for
   an ARBITRARY Veech surface, proving piecewise-real-analyticity + quadratic tail for ALL
   Veech surfaces at once, with a uniform first-return finiteness result. "One surface per
   paper" was already obsolete. (2409.15660 adds effective rates, again uniformly.)

5. THE OBSERVABLE/SECTION IS TAHA'S, NOT NEW.
   Taha (arXiv:1810.10668) built the G_q-BCZ map and the G_q-Farey triangle
   Tq={(a,b)|0<a≤1, 1−λ_q a<b≤1} and computed the slope-gap distribution (Cor. 4.2). The
   repo's section, map (scalar branch), and gap-product live inside Taha's framework. The
   repo's Dcorr is a SUB-region of Taha's Tq (it adds the second lower edge λa+b>1).

6. ARITHMETICITY DICHOTOMY = TAKEUCHI 1977 (rebadged).
   The arithmetic Hecke triangle groups are exactly q∈{3,4,6} (plus q=∞); this is Takeuchi,
   "Arithmetic triangle groups," J. Math. Soc. Japan 29 (1977), and the crystallographic
   restriction. The repo's own scout memory already records this: the {3,4,6} cut is "the
   classical crystallographic restriction {2,3,4,6,∞}, older/more elementary than cluster
   algebras." The "local statistic detects global arithmeticity" framing is a repackaging
   of B(q)=2 ⟺ q∈{3,4,6}, which is Takeuchi's classification composed with the
   cluster-ceiling computation — not a new arithmeticity criterion.

WHAT IS GENUINELY NEW (the defensible residue):
   - The specific NUMBER: identifying the family-uniform support-edge value as 1/λ_q³
     (in the P-product normalization), uniform in q, with an elementary
     no-sustained⇒edge + ejection + arc-width proof that does not invoke the full
     equidistribution machinery.
   - MACHINE-VERIFICATION: a Lean-checked, axiom-clean proof of the LOWER bound for 17
     Hecke indices. To my knowledge there is no prior machine-verified slope-gap /
     ergodic-optimization edge result. This is a real, if narrow, first.
   The repo's OWN submission draft (research_notes/PAPER_uniform_onset_SUBMISSION.md) states
   this honestly (lines 30, 81, 104–106, 124–126, 154–155): it positions the result as the
   *quantitative + machine-verified* refinement of the *qualitative* Athreya–Chaika
   dichotomy, and explicitly says the equality is not in the verified footprint. The
   "biggest win" framing handed to this audit OVERCLAIMS relative to the repo's own paper.

---

## FRONT 3 — Lean cleanliness. VERDICT: SURVIVES for the LOWER BOUND on q=5..21; the "= 1/λ³ EQUALITY" and the ∀q claim are NOT verified; the top-level ∀q theorem smuggles its conclusion via hCorr.

Statements actually proved (read directly):

A. UniformOnset_q5to18.lean — Xomega_lb_q5to18 and the 13 per-q theorems. Statement:
     ∀ q∈{5,7,…,18}, ∀ μ invariant prob. measure with μ(Dcorrᶜ)=0, Pprod a.e. ≤ M,
       1/l³ ≤ essSup Pprod μ.
   This is a LOWER bound (≥), not the equality. Hypotheses are the STANDARD
   ergodic-optimization setup (invariant prob measure on the corridor, observable a.e.
   bounded) — NOT trivializing. The load-bearing combinatorial fact
   g{q}_no_window_below_genuine (e.g. g5_no_four_below_genuine, read in full) is a GENUINE
   non-vacuous negation: "no 4 consecutive gap-products all < 1/φ³" under the real
   recurrence/positivity/cap hypotheses. Not vacuous, not hidden-hypothesis-trivialized.
   Build evidence (research_notes/build_evidence_q5to18_2026-06-13.txt) shows
   #print axioms = [propext, Classical.choice, Quot.sound] for all 14 — axiom-clean, no
   sorryAx. SURVIVES.

B. GenuineMapFacts.lean — Xomega_lb_q5to21 extends to q=19,20,21 by the same 6-window
   route (g{19,20,21}_no_window_below_genuine), same axiom set claimed
   [propext, Classical.choice, Quot.sound]. Statement is again the ≥ bound with the same
   honest measure hypotheses. SURVIVES as a lower bound for 17 indices — CONDITIONAL on the
   per-q minpoly hypothesis mpolyq21 q l being the principal Hecke root (carried, true).

C. ToplevelStitch.lean — Xomega_lb_allq (the "∀q" headline). This is WEAKER than the
   q≤21 theorems and partly circular for q≥19:
   - For q∈{5,…,18}: delegates to Xomega_lb_q5to18 (real, unconditional).
   - For q≥19: the conclusion 1/l³ ≤ essSup (Pgen) μ is delivered by the HYPOTHESIS
       hCorr : 19≤q → (∀ hL, 1/λ³ ≤ g_corr …) → 1/l³ ≤ essSup (Pgen l) μ.
     i.e. hCorr is ASSUMED to map the analytic arc-width bound to the essSup conclusion.
     The proof just feeds L1b_carried into hCorr. So the q≥19 branch of Xomega_lb_allq does
     NOT prove the essSup bound — it ASSUMES the implication that yields it. The block-
     monodromy→essSup wiring is a carried hypothesis, not discharged here. (#print axioms
     lines are present in-file; the docstring's "sole sorryAx = fcorr_lb" is now STALE
     because fcorr_lb was completed 2026-06-14 — see D.)

D. L1bArcCoverage.lean — fcorr_lb (the arc-width crux) is now a CLOSED proof (no sorry in
   its body; the file header line 25 records it was sealed 2026-06-14; B1_target reduces to
   it). So the *analytic* crux is genuinely proven and axiom-clean. Good — but this seals
   only the arc-width inequality, NOT the hCorr wiring of C.

E. NO upper-bound / attaining-measure theorem exists anywhere in the directory. grep for
   essSup ≤ / Xomega_ub / equality / attain returns nothing. The EQUALITY X_Ω(q)=1/λ³ is
   therefore NOT machine-verified — only ≥ is. The matching upper bound is the cusp-tip
   Dirac (Front 1b), recorded as a witness, outside the Lean footprint.

Does hCorr/P2 "quietly assume the conclusion"? For q≥19, YES in effect: hCorr's codomain
IS the conclusion (1/l³ ≤ essSup Pgen μ). The honest reading is: q≥19 in the *top-level*
file is conditional on a carried wiring hypothesis. The genuinely UNCONDITIONAL, axiom-clean
machine-verified content is the LOWER bound for q∈{5,7,8,…,21} (17 indices) in
UniformOnset_q5to18.lean + GenuineMapFacts.lean (per the cached axiom prints; I did not run
a multi-hour build).

---

## ONE-SENTENCE DEFENSIBLE SCOPE

What actually holds, after attack: **a Lean-checked, axiom-clean LOWER bound
X_Ω(q) ≥ 1/λ_q³ for the 17 Hecke indices q∈{5,7,8,…,21} on Taha's G_q-BCZ corridor
(for any invariant probability measure on Dcorr) — a genuine first as a *machine-verified*,
*quantitative*, *family-uniform* refinement of the long-known Athreya–Chaika "no small gaps
⟺ Veech" dichotomy (golden-L/q=5 hard edge published 2013, 2n-gon family 2021, uniform Veech
method 2021) — but NOT the headline "X_Ω(q) = 1/λ³" (the matching upper bound is an
unverified cusp-tip Dirac), NOT "unconditional ∀q" (q≥19 in the top-level stitch is carried
on the hCorr wiring hypothesis whose codomain is the conclusion), and the arithmeticity
"corollary" B(q)=2 ⟺ q∈{3,4,6} is Takeuchi 1977 / the crystallographic restriction
rebadged.** The repo's own submission draft states most of these caveats; the "biggest win"
one-liner overclaims relative to it.
