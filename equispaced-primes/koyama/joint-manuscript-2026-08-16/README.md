# Joint manuscript revision - 2026-08-16

This directory is an isolated revision of Koyama's supplied
`nontriv2607.tex` (SHA-256
`d6acb7680e4225d1e0d51237a1aacfa14e073ed9edf9a6010f9f9fb93fbb875c`).
The supplied file in `/Users/za/Downloads` was not modified.

## Files

- `manuscript.tex`: joint, evidence-bounded revision.
- `manuscript.pdf`: clean Tectonic build.
- `figures/spectral_reconstruction.pdf`: verified five-modulus reconstruction.
- `integrate_revision.py`: reproducible transformation from the supplied source.

## Build

From this directory:

```sh
tectonic -X compile manuscript.tex --keep-logs -r 2
```

The final build has 8 letter-size pages and no TeX warnings, overfull boxes,
underfull boxes, undefined references, or oversized floats.

## Scope decisions

- The corrected character selector is a lemma.
- The Gaussian limit is a two-parameter conjectural target, not a fixed-`T`
  theorem.
- Universal apex/nadir language is conjectural.
- Ordinary-count evidence is explicitly separated from the proposed
  regularized statistic.
- The requested finite-`x` regularized comparison plot is not fabricated;
  it remains pending a fixed statistic, normalization, branch convention,
  and proved `T(x)` regime.
- The former Table 3 is rebuilt from raw class counts, including all modulus-23
  quadratic nonresidues.

## Fresh verification

- Baseline counts: 567/567 exact matches, zero mismatches.
- Spectral package: 55/55 zero checks pass; 13,578 reconstruction rows.
- Independent modulus-19 gate: Arb sign bracket passes; 17/17 deep zero
  checks pass; 7 adversarial tests pass.
- Lean: the character-selector project builds; the four finite
  quadratic-nonresidue theorems compile against Mathlib v4.28.0.

