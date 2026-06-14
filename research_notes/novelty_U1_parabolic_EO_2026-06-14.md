# Novelty audit — U1 "Cusp Ground-State Theorem for parabolic ergodic optimization"

**Date:** 2026-06-14. **Mode:** citation-grade prior-art audit (default = "likely known",
weigh near-misses). **Scope:** the abstract statement only (NOT the Hecke-specific 1/λ³ value,
which is audited elsewhere). Web-searched; PDFs fetched where extractable.

---

## THE STATEMENT (U1)
> Let T be a piecewise-smooth measure-preserving cross-section map with a **parabolic/neutral
> fixed point p** (cusp return map of a horocycle/geodesic flow on a finite-volume hyperbolic
> surface, or the SL(2,ℝ) cross-section of a Veech surface). Let P be a bounded "gap-type"
> observable attaining its relevant extreme value at p. Then the **L∞ / essential-supremum**
> ergodic-optimization ground value
>   inf_{μ ∈ M(T)} ( ess-sup_μ P ) = P(p),
> attained by the Dirac measure δ_p at the parabolic fixed point ("cusp ground state").

---

## VERDICT: **PARTIAL-with-scope** (the *named functional* + the *parabolic-localization-of-
## the-inf-ess-sup* combination is essentially absent from the literature; but each of the three
## ingredients has strong adjacent prior art, and the abstract identity alone is a near-triviality.)

Breakdown by the three distinctions the task flagged:

| Distinction | Status | Why |
|---|---|---|
| (1) ess-sup vs Birkhoff-average EO | **NOVEL framing** — inf-ess-sup over invariant measures is not a studied object in EO | The entire EO field (Jenkinson, Bochi, Contreras, Garibaldi) optimizes ∫φ dμ. "L∞ ergodic maximization" papers exist but mean something else (sup-norm of a *trig polynomial* via a maximizing measure), not inf-ess-sup. |
| (2) parabolic/neutral ground state | **KNOWN as a phenomenon, different vehicle** | Dirac-at-parabolic-point as a limiting/ground-state measure is established for Manneville–Pomeau / intermittent maps — but via stochastic stability and zero-temperature thermodynamic formalism, NOT via inf-ess-sup. |
| (3) cusp/slope-gap incarnation | **KNOWN object, never optimization-framed** | Slope-gap / horocycle-section people prove the "no small gaps / hard edge" and gap *distributions*; nobody frames the minimal/extreme gap as an EO ground value `inf_μ ess-sup`. |

Net: the *combination* (call the inf-ess-sup an EO ground value AND localize it at a parabolic
cusp point AND realize it as a slope-gap/horocycle-section statement) appears **not previously
stated**. But see the honest sentence in (d): once correctly stated the abstract identity is
shallow; the value is in the realization, not the principle.

---

## (b) The 3–6 closest papers

1. **Riquelme & Velozo, "Ergodic optimization and zero temperature limits in negative curvature"
   — arXiv:2001.01694.** *Closest non-compact-EO paper.* Geodesic flow on non-compact
   negatively-curved manifolds; proves the ONLY obstruction to existence of an average-maximizing
   measure is full **escape of mass**, and studies zero-temperature limits. **Does NOT cover U1:**
   (i) it maximizes the **Birkhoff average** ∫φ dμ, not inf-ess-sup; (ii) escape-of-mass *destroys*
   the maximizer there, whereas U1 *uses* a parabolic/cusp point as the *minimizer* of ess-sup —
   opposite role of the cusp; (iii) no L∞ object, no localization-at-parabolic-point conclusion.
   **Near-miss, not a kill** — it is the right setting (cusp escape on non-compact hyperbolic
   geometry) but the wrong functional and the cusp plays the antagonist, not the ground state.

2. **Motonaga, "Minimax aspects of optimizations in ergodic theory" — arXiv:2411.17615.**
   The word "minimax" is a false friend: this is **inf-sup Fenchel–Rockafellar duality of the
   usual average-maximization** (variational principle for generalized pressure), NOT minimizing
   an essential supremum over measures. **Does NOT cover U1.** (Kills the "minimax EO" lead.)

3. **Kucherenko & Wolf, "Ground States and Zero-Temperature Measures at the Boundary of Rotation
   Sets" — arXiv:1604.06512.** "Ground state" = zero-temperature accumulation point of
   equilibrium states; maximizes **entropy on a face of the rotation set** (a Birkhoff-average /
   thermodynamic object). **Does NOT cover U1:** no ess-sup functional, no parabolic-point
   localization. (Settles that "ground state" in the literature ≠ our inf-ess-sup ground value.)

4. **Shen / "On stochastic stability of expanding circle maps with neutral fixed points" —
   arXiv:1212.5671** (and the Manneville–Pomeau / Pomeau–Manneville thermodynamic-phase-transition
   line, e.g. arXiv:1208.5252). *Closest "Dirac-at-parabolic-point" prior art.* For x↦x+x^{1+α},
   α≥1, the small-noise / zero-temperature limiting measure **IS the Dirac at the neutral fixed
   point**. **Does NOT cover U1:** that selection is via stochastic stability / freezing of Gibbs
   measures (a thermodynamic, average-side mechanism), and the localization is of an
   *equilibrium/zero-temperature* measure, not of the minimizer of an essential supremum. It
   establishes that "mass concentrates at the parabolic point in a low-temperature limit" — the
   morally-same phenomenon U1 names, but reached through an unrelated functional. **Strong
   conceptual near-miss for distinction (2).**

5. **Kumanduri–Sanchez–Wang, "Slope Gap Distributions of Veech Surfaces" — arXiv:2102.10069;
   + Athreya–Chaika–Lelièvre / Uyanik–Work "golden L" 1308.4203, octagon 1409.0830; effective
   2409.15660.** *Closest cusp/horocycle-section prior art.* Parameterize the horocycle Poincaré
   section, prove the slope-gap distribution is piecewise real-analytic, and characterize Veech
   surfaces by **"no small gaps" (a hard edge at 0)** — the support edge of the *gap distribution*.
   **Does NOT cover U1:** they study the **distribution** (and its support edge under the *unique*
   ergodic section measure), never the *optimization* `inf over invariant measures of ess-sup`;
   the hard edge there is a property of one canonical measure, not a min-over-all-invariant-measures
   ground value attained by a Dirac at the cusp. **Near-miss** — same geometric object (gap on a
   cusp section), absent the EO framing.

6. **Jenkinson, "Ergodic optimization in dynamical systems" — arXiv:1712.02307** (the field
   survey). Defines EO entirely as β(φ)=sup_μ ∫φ dμ; "Contreras: generic ground states are a
   single periodic orbit" is the **hyperbolic/expanding** baseline U1 deliberately departs from.
   No section treats inf-ess-sup over measures, nor parabolic supports as the rule. **Confirms
   the gap** rather than filling it. (The "L∞ ergodic maximization" papers e.g. arXiv:1903.09425
   are about L∞-estimating Thue–Morse trigonometric polynomials — a different use of "L∞".)

---

## (c) Narrowest genuinely-new version worth proving

The abstract identity is too cheap (see (d)). The defensible new content is the *realization*,
stated at exactly the level the Hecke work supplies:

> **(U1′ — narrow):** For the Taha G_q-BCZ cross-section map T_q of the horocycle flow (a
> piecewise-smooth, area-preserving section with a single parabolic cusp fixed point p_q), and
> the genuine gap-product observable P, the L∞ ergodic ground value
>   X_Ω(q) := inf_{μ ∈ M(T_q)} ess-sup_μ P  =  P(p_q) = 1/λ_q³,   λ_q = 2cos(π/q),
> the inf being **attained uniquely by the cusp Dirac δ_{p_q}**, and this value being a
> family-uniform invariant that **detects arithmeticity** of G_q (the {3,4,6} interior-value
> exceptions). The genuinely new mathematics is (i) that the inf-ess-sup is attained at the
> *parabolic* point rather than a hyperbolic periodic orbit (contra Contreras), and (ii) the
> **uniform-in-q lower bound** `ess-sup_μ P ≥ 1/λ_q³` for every non-cusp invariant μ — i.e. that
> no invariant measure can keep P essentially below the cusp value. (i)+(ii) are the content;
> the abstract `inf=P(p)` framing is the wrapper.

Even narrower honest core: **"a transient/no-dwell mechanism forces ess-sup_μ P ≥ P(p) for all
invariant μ on a parabolic cross-section, with equality only at the cusp Dirac"** — this is the
one statement with real proof-content (it is precisely the q≥16 multi-branch transience gap that
`exp_energy_cusp_numeric_2026-06-12.md` and `energy_route_2026-06-12.md` flag as the open lemma).

A *general* "Cusp Ground-State Theorem" abstracting U1 to all parabolic section maps is the
follow-on-roadmap Path 2 — and is **only worth stating if the hypotheses are non-vacuous and the
conclusion is non-trivial**, which requires the transience input, not just the geometry.

---

## (d) One honest sentence: real unifying theorem, or near-triviality?

**As an abstract identity it is a near-triviality dressed in new vocabulary** — for any fixed
invariant μ, ess-sup_μ P ≥ value of P on the support's relevant extreme, so `inf_μ ess-sup_μ P`
trivially collapses to "the smallest closed-invariant-set value of P," and if a Dirac δ_p is
admissible and P(p) is that smallest value the equation `=P(p)` is immediate; **the entire
mathematical weight lives in the two non-trivial facts the wrapper hides — that the parabolic
cusp point is where P's relevant extreme sits AND that no other invariant measure can essentially
undercut it (the uniform no-dwell/transience lower bound)** — so U1 is a genuine theorem only in
its realized form (U1′), where those two facts are real and, for the Hecke family, still partly
open (the q≥16 uniform transience lemma).

---

## Bottom line for the workflow
- Do **not** market U1 as "L∞ ergodic optimization" without immediately stating that the
  inf-ess-sup framing, while apparently un-named in EO, is shallow on its own.
- The citable novelty is **(U1′)**: parabolic (non-periodic-orbit) localization of an EO ground
  value + uniform lower bound + arithmeticity detection, on the horocycle/Veech cusp section.
- Mandatory citations to position honestly: Riquelme–Velozo 2001.01694 (escape of mass),
  Jenkinson 1712.02307 + Contreras (hyperbolic baseline U1 departs from), Manneville–Pomeau /
  Shen 1212.5671 (Dirac-at-parabolic-point precedent, different vehicle), KSW 2102.10069 +
  golden-L 1308.4203 (slope-gap hard edge = the same object, un-optimized).
- The proof-bearing gap is **not** the abstract principle; it is the uniform no-dwell lower
  bound (open for q≥16), already tracked in the energy-route notes.
