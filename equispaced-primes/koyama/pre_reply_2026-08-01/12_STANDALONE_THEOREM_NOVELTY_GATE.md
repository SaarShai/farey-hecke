# Standalone boundary identity: theorem and novelty gate

Date: 2026-08-01

## Decision

The analytic theorem is now closed, but the proposed standalone paper should
**not** be presented as a new research theorem.

The strongest clean statement is unconditional: for any Dirichlet character
`chi` and any `s = 1/2 + i tau` with `tau != 0`, the ordinary prime-cutoff
limit of the `k >= 2` prime-power tail equals the corrected four-term
decomposition involving `Log_* L(2s, psi)`, `BPC_1`, `BPC_2`, and `T_{>=3}`.
Neither the assumption that `s` is a zero nor simplicity is used.

`Log_*` must be the horizontal boundary value continued from the absolutely
convergent Euler product. The earlier demand that the logarithm be independent
of arbitrary path deformation is false because logarithms have monodromy.

## Why the novelty gate fails

- [Conrad, *Canadian Journal of Mathematics* 57 (2005), Theorems 4.1,
  4.3, 4.9 and Example 4.6](https://doi.org/10.4153/CJM-2005-012-6)
  already supplies the boundary Dirichlet-series, ordering, and
  squared-character second-moment framework.
- [Akatsuka, *Kodai Mathematical Journal* 40 (2017), equations
  (2.3)--(2.5)](https://doi.org/10.2996/kmj/1490083225) directly proves the
  principal boundary prime-sum tail estimate.
- [Kaneko, *Bulletin of the Australian Mathematical Society* 106
  (2022)](https://doi.org/10.1017/S0004972721001003) treats broader partial
  Euler-product asymptotics for Dirichlet `L`-functions.
- The four-term formula is a short `k=2` isolation plus standard
  primitive/imprimitive Euler factors. The local Perron residue is standard
  Laurent algebra.

The exact four-term display was not located verbatim, but search non-detection
does not establish novelty. Structurally, the theorem is an elementary
specialization of the cited machinery.

## What remains valid and useful

- The corrected boundary identity is proved at paper level.
- The local Perron residue is proved and has a zero-`sorry` Lean certificate.
- The full partial-Moebius asymptotic remains excluded: off-target zeros
  contribute non-decaying oscillatory residues on GRH, and a global contour
  argument still needs zero-sum ordering, horizontal/left-edge bounds, and
  multiplicity control. [Inoue 2021](https://doi.org/10.5802/jtnb.1162) is the
  relevant primary explicit-formula reference.
- The material is suitable as a technical appendix or reproducibility
  certificate in a paper whose main novelty lies elsewhere.

## Artifacts

- `../../papers/boundary-euler-perron/paper.tex`
- `../../papers/boundary-euler-perron/paper.pdf`
- `../../papers/boundary-euler-perron/NOVELTY_AND_PROOF_STATUS.md`
- `../../papers/boundary-euler-perron/verify_finite_identity.py`

The compiled note is four A4 pages and was visually checked after the theorem,
branch, convergence-mode, contour, and novelty revisions.

The finite verifier passed exact rational coefficient checks through degree
100, two independent character cases (`q=4` with an imprimitive square and
`q=5` with a primitive square), and a negative control that flips the
`BPC_1` sign. It deliberately does not claim to verify boundary convergence.

Aristotle project `d84a4795-4fad-42d4-a2d4-d1003a48450d`, task
`8630cf0d-864e-4083-9edc-0e3f6f1d6678`, remained running at the last bounded
poll. No generated artifact or machine proof has been accepted.
