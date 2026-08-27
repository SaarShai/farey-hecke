# Joint manuscript review packet

**Prepared for:** Shin-ya Koyama  
**Prepared by:** Saar Shai  
**Version date:** 16 August 2026

This is the complete review and reproducibility packet for the joint revision
of *Regularized Spectral Statistics for Prime Races and Low-Zero Transient
Reversals*. Start with `manuscript/manuscript.pdf`, then read
`02_TECHNICAL_CHANGELOG.md` and `03_VERIFICATION_REPORT.md`.

## Contents

- `02_TRANSMITTAL_MEMO.pdf` — concise review map, results, and open decisions.
- `02_TECHNICAL_CHANGELOG.md` — exact scientific and editorial changes.
- `03_VERIFICATION_REPORT.md` — what was checked, how, and with what result.
- `manuscript/` — submission-shaped TeX, compiled PDF, and figure.
- `numerics/` — authoritative ordinary-count curve, independent baseline,
  zero data, derived outputs, plots, generators, and verifiers.
- `lean/` — compact Lean source projects for the claimed finite scope only.
- `support/` — source provenance, a unified source diff, and checksums.

## Important status boundary

This version does **not** claim the earlier fixed-`T` asymptotic as a theorem.
It states a two-parameter regularized limit as a conjectural analytic target.
The summed off-diagonal estimate, justified order interchanges, logarithm
branch convention, and an admissible `T(x)` regime remain open obligations.

The finite-`x` mollified comparison plot is consequently not included. It
would not be mathematically interpretable until the statistic, normalization,
branch convention, and `T(x)` regime are fixed. The included numerical figure
instead reconstructs the observed **ordinary** prime-count transients from
low zeros, with the distinction stated throughout the manuscript.

## Suggested review sequence

1. Confirm the theorem/conjecture boundary and the open analytic obligations.
2. Check the corrected selector and the raw-count replacement for Table 3.
3. Review the ordinary-count and low-zero numerical section and Figure 1.
4. Confirm title, author order, affiliations, contribution statement, and
   computational-assistance disclosure.
5. Agree on a permanent public archive for data/code and insert its DOI.
6. Both authors approve one final compiled version before any arXiv replacement
   or journal submission.

## Build

From `manuscript/`:

```sh
tectonic -X compile manuscript.tex --keep-logs -r 2
```

The verified build has eight US-letter pages and no TeX layout or reference
warnings. Reproduction commands for the numerical packages are in their local
README files. Checksums for every packet file are in
`support/SHA256SUMS.txt`.
