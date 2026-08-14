# Lean contribution inventory and gates before replying

**Internal decision brief - no email or material has been sent.**

## What the Lean work actually proves

### Directly relevant, fully certified

`equispaced-primes/lean/formal-conjectures/Minus1Core.lean` proves four unconditional,
finite-combinatorial statements:

1. a nonsquare in `ZMod N` has zero square roots;
2. every quadratic nonresidue has leading mean `-1` under the stated Rubinstein-Sarnak mean formula;
3. any two nonresidues tie at that leading-mean level;
4. consequently `-1`, when a nonresidue, is not singled out by the leading mean.

Recorded clean-build evidence: Lean 4 / Mathlib v4.28.0, exit 0, zero warnings, and only
`[propext, Quot.sound]` in the axiom printout.  This is a useful corrective/combinatorial
lemma.  It is **not** a formalization of Theorem 1.4 in the attached manuscript.

### New focused certificate

The independently returned Aristotle task in `02_CHARACTER_ORTHOGONALITY_CERTIFICATE.md`
certifies the exact algebraic error in Definition 1.3.  Its scope is finite character algebra
plus the concrete modulus-7 witness.  It does not certify the explicit formula, DRH input,
limiting argument, or universal dominance claim.

### Broader formal-conjectures inventory

The older ten-module project contains eight zero-`sorry` modules and two occurrences of
`sorry`, both representing the same general-`K` Dirichlet Polynomial Avoidance Conjecture:

- `DPAC_full.lean:338`
- `DirichletPolynomialAvoidance.lean:54`

Several zero-`sorry` theorems are explicitly conditional on named analytic or numerical
hypotheses.  None matches the statement of the attached manuscript's Theorem 1.4.  The reply
must therefore say **"Lean formalization of selected finite/algebraic components"**, never
"Lean verification of the paper" or "formal proof of the main theorem."

## Collaboration and submission gates

Do not consent to submission, transfer raw data/code, or allow a broad Lean-verification claim
until all of the following are satisfied:

1. **Identity check:** continue the conversation through a fresh institutional channel obtained
   from Toyo University's public profile, not solely by replying to the existing consumer-domain
   thread.
2. **Public preprint record:** obtain the public arXiv identifier and version.  As checked on
   1 August 2026 UTC, exact-title arXiv search returned no public result; the attached PDF shows
   only an arXiv submission watermark.
3. **Full joint source:** receive the complete proposed joint TeX, bibliography, figures, tables,
   code/data citations, and contribution statement.
4. **Distinct joint advance:** identify exactly what theorem and proof are new beyond Koyama's
   single-author preprint.  Data alone should not be used to make an unsupported theorem look
   submission-ready.
5. **Authorship fixed before submission:** both authors approve the complete version, names/order,
   contribution statement, cover letter, venue, and every later revision.  Inventiones' current
   policy requires explicit coauthor consent and accountability.
6. **Technical repair:** close every priority item in `01_THEOREM_AUDIT.md` and obtain independent
   analytic review.
7. **Numerical repair:** reconcile `N=11, a=10`; state precisely which computations were independently
   replicated; keep the 300-trillion conclusion finite-scale and non-universal.
8. **IP and provenance:** retain dated hashes, authorship of code/Lean/data, a data-availability plan,
   and explicit permission boundaries before transfer.

## Recommended reply posture

Be warm about continuing the collaboration, but do **not** endorse an Inventiones submission
timeline yet.  The reply should say:

- the 300-trillion appendix and a precise Lean inventory are ready;
- the attached draft contains a correctable inverse-class inconsistency and major missing analytic
  estimates that must be resolved first;
- we need the public arXiv identifier and complete joint TeX;
- we will approve neither authorship claims nor submission until both authors review the full version;
- the separate elliptic-curve/Decision-Audit work remains single-author unless Koyama later makes a
  substantial, documentable contribution.

## External policy anchors checked 1 August 2026 UTC

- Toyo University researcher profile: <https://ris.toyo.ac.jp/profile/en.09d82e3d424baf429c5613ee8954ad37.html>
- Exact-title arXiv search: <https://arxiv.org/search/?query=%22The+Fine-Structure+Hierarchy+of+Prime+Biases%22&searchtype=all>
- Inventiones submission/authorship guidance: <https://link.springer.com/journal/222/submission-guidelines>
