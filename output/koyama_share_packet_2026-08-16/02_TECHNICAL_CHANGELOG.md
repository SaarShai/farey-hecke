# Technical change log

This records the changes from the supplied `nontriv2607.tex` to the joint
revision. The line-level unified diff is `support/manuscript_changes.diff`.

## Analytic status and definitions

- Corrected the character selector from `1-chi(a)` to
  `1-conjugate(chi(a))`; without the conjugate, the negative term selects
  `a^{-1}`.
- Made the logarithm-branch pairing explicit so the proposed special-value
  combination is real.
- Replaced the unsupported fixed-`T` theorem by a two-parameter conjectural
  target with `T=T(x)`.
- Retained the diagonal factor `T/(4 sqrt(pi))` inside the coefficient unless
  a genuine cancellation is proved.
- Identified the missing global work: a summed off-diagonal estimate, justified
  order interchanges, prime-power tails, Archimedean/conductor/imprimitive
  factors, and strict inequalities for any universal ordering.
- Recast the universal `-1` apex and `1` nadir statements as a conjectural
  regularized hierarchy, not a theorem about ordinary prime counts.
- Removed the earlier Fejer-kernel “independent proof,” whose uniform prime-tail
  bound was not established.

## Numerical section

- Added the 438-checkpoint ordinary-count dataset for
  `N in {7,8,11,19,23}` through `3 x 10^14`.
- Recorded exact agreement in all 567 shared baseline cells through
  `1.3 x 10^13`; the extension above that height remains one run.
- Rebuilt Table 3 from raw class counts, correcting eight cells at
  `1.3 x 10^13`, correcting the sign for `N=19, a=10` at `1.3 x 10^11`, and
  restoring `a=20` modulo 23.
- Added the endpoint ranks of `-1`: `1/3, 3/3, 3/5, 6/9, 1/11` for
  `N=7,8,11,19,23`.
- Added the low-zero explicit-formula reconstruction using 25 positive zeros
  per nonprincipal character, together with fit metrics and rank-transition
  counts.
- Added the independently certified modulus-19 zero near
  `0.018956399080226143` for the odd character of Conrey index 13.
- Removed the former `gamma approximately 1.74` lowest-mode claim and the
  associated `exp(33.4)` settling estimate.
- Added the modulus-19 100-zero stability run, which raises the `-1`
  correlation from 0.9715 to 0.9925 while leaving rank changes active.

## Reproducibility and declarations

- Added data/code provenance, the authoritative curve digest, executable
  verifiers, test suites, and manifests.
- Limited the Lean claim to one corrected character-selector project and four
  finite quadratic-nonresidue statements; no analytic theorem is claimed to be
  formalized.
- Added author contributions and computational/AI-assistance disclosures.
- Added the requirement for a permanent public data/code archive identifier
  before submission.

## Intentionally pending

- No finite-`x` plot of the proposed mollified statistic is supplied because
  the statistic, normalization, logarithm branch, and admissible `T(x)` regime
  are not yet fixed.
- No transfer theorem from the regularized hierarchy to eventual ordinary
  prime-count dominance is asserted.
- The title, author order, affiliations, contribution statement, public archive
  DOI, and final submission venue/version remain subject to both authors'
  approval.
