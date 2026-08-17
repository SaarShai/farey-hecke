# Verification report

**Verification date:** 16 August 2026

## Manuscript artifact

- Tectonic build: **PASS**.
- Output: eight US-letter pages.
- Undefined references/citations: none.
- Overfull/underfull boxes and oversized floats: none reported.
- Rendered-page visual inspection: all eight pages checked; no clipping,
  overlap, missing figure, or float-order defect found.

## Ordinary-count data

- Authoritative extended curve SHA-256:
  `57957bdb3ce3243272c3d4b8e9ffe7dfb734b759f48b63becf7ae6f924e1caab`.
- Shared baseline comparison: **567/567 exact integer matches**, zero
  mismatches, through `1.3 x 10^13`.
- Scope: the extension from `1.3 x 10^13` to `3 x 10^14` is a single full run,
  not an independent replication.

## Base low-zero reconstruction

- Zero cross-checks: **55/55 pass**.
- Reconstruction rows: **13,578**.
- Ordinates: two PARI/GP mesh runs, with direct residual checks below
  `1e-28` for used zeros.
- Important limitation: these checks do not prove zero completeness or GRH.

## Independent modulus-19 gate

- Arb sign-definite endpoint bracket: **PASS**.
- Deep-zero checks: **17/17 pass**.
- Adversarial verifier tests: **7/7 pass**.
- Certified conclusion: existence of a critical-line zero in the reported
  bracket. Uniqueness, completeness, and GRH are not claimed.

## Lean scope

- Corrected character-selector project: **build passes**.
- Four finite leading-mean/nonresidue theorems: **compile** against Lean 4 and
  Mathlib 4.28.0.
- Source scan: no `sorry` or `admit` in the claimed files.
- Not formalized: the regularized-limit conjecture, explicit-formula analysis,
  numerical pipeline, DRH/GRH, or the manuscript as a whole.

## Scientific claim gate

- Corrected selector: proved finite character algebra.
- Ordinary-count and low-zero claims: verified finite computations at the
  stated dataset scope.
- Two-parameter regularized limit: conjecture/open analytic program.
- Universal apex/nadir hierarchy: conjecture conditional on that program and
  strict inequalities.
- Eventual ordinary-count ordering: not claimed.
- Requested mollified finite-`x` plot: not produced pending a fixed analytic
  definition and normalization.

## Integrity

`support/SHA256SUMS.txt` covers every other packet file. The outer archive is
also tested after creation. These checks establish file integrity and
reproducibility of the included checks; they do not replace mathematical peer
review.
