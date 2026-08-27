# Computational package: Regularized Spectral Statistics for Prime Races and Low-Zero Transient Reversals

Shin-ya Koyama (Toyo University) and Saar Shai (independent researcher).

This archive is the complete data and code package for the joint manuscript.
Companion theoretical preprint: arXiv:2607.28931.

## Contents

- `numerics/source/` — ordinary prime-count race data for N in {7, 8, 11, 19, 23}
  at 438 checkpoints through 3e14 (`curve_3e14.tsv`), the independently checked
  baseline through 1.3e13, and comparison tooling.
- `numerics/spectral/` — Dirichlet L-function zero generation (PARI/GP, dual
  mesh 64/96 with agreement gate), low-zero explicit-formula reconstruction,
  transition ledger, figure source, and verifiers.
- `numerics/frontier_replication/` — independent primesieve recomputation of
  the 1.3e13 -> 3e14 frontier (three range-split runs, merge script, and the
  PASS receipt: 4896/4896 cells match `curve_3e14.tsv` exactly).
- `numerics/n19/` — independent FLINT/Arb certification of the critical-line
  zero near gamma = 0.018956399080226143 for the odd character of Conrey
  index 13 modulo 19, and the K=50/K=100 deep reconstruction.
- `lean/` — Lean 4 sources for the finite scope only: the corrected
  character-selector identity and four finite statements on the leading
  quadratic-nonresidue mean. No `sorry`/`admit`.
- `03_VERIFICATION_REPORT.md` — what was checked, how, and with what result.
- `02_TECHNICAL_CHANGELOG.md` — exact scientific changes in the joint revision.
- `SHA256SUMS.txt`, `SOURCE_PROVENANCE.md` — checksums and provenance.

## Reproduce

Each `numerics/*` directory has a local README with exact commands. The
authoritative curve file has SHA-256
`57957bdb3ce3243272c3d4b8e9ffe7dfb734b759f48b63becf7ae6f924e1caab`.

## Scope statement

The verified content is finite: exact prime-count data, certified zero
brackets, and finite Lean identities. Nothing in this package proves GRH/DRH,
zero completeness, an eventual ordering of ordinary prime counts, or the
regularized asymptotic conjectures of the manuscript.
