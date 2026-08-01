# A-driver characterization protocol

Frozen: 2026-07-19, before this protocol's discovery or holdout scans.

## Question and scope

The refuted Farey observable has prime-step sign equal to that of
`A(p-1)-1`, where

\[
a(n)=\frac{1}{n}\prod_{q\mid n}(1-q),\qquad
A(x)=\sum_{n\le x}a(n).
\]

This is an observational characterization of the driver.  It does not test,
state, or select a replacement asymptotic conjecture.

The exact identity used as an independent arithmetic check is

\[
a(n)=\sum_{d\mid n}\frac{\mu(d)}{n/d},\qquad
A(x)=\sum_{d\le x}\mu(d)H_{\lfloor x/d\rfloor}.
\]

## Frozen data split

- Discovery: every integer `1 <= x <= 1,000,000`, and every prime
  `p <= 1,000,000` (using `A(p-1)-1` and `M(p)`).
- Holdout: every integer `1,000,000 < x <= 2,000,000`, and every prime in
  that interval.  No metric, bin boundary, conditioning rule, or qualitative
  label may be altered after discovery results are seen.

## Frozen metrics

For each split, calculate:

1. Sign inventory of `A(x)-1` (negative, zero, positive) at every integer;
   retain the first nonnegative integer if one occurs.
2. Fixed decade-style blocks `[1,10^k]` truncated at the split boundary:
   count, mean, minimum, maximum, and mean of
   `abs(A(x)-1)/sqrt(x)`.  These are descriptive only; no fitted exponent is
   selected from them.
3. Pearson correlation of `A(x)-1` with `M(x)` over all integers in the
   split, and sign agreement over integers for which `M(x) != 0`.
4. At primes: counts and agreement rates for the *reversed* finite pattern
   `sign(A(p-1)-1) = sign(M(p))`, separately for `M(p)<=-3`, `M(p)>=3`, and
   all `M(p)!=0`.  The original, refuted orientation is recorded only as its
   complementary rate when both signs are nonzero.

The holdout is classified only against the following predeclared descriptive
labels: `CONSISTENT` when its sign inventory and the direction (positive,
negative, or zero) of each nonempty prime-conditioned rate match discovery;
otherwise `DIFFERS`.  This label is not evidence for an asymptotic theorem.

## Arithmetic and certification

- `mu`, `M`, prime flags, and the integer numerator
  `prod_(q|n)(1-q)` are computed by an integer smallest-prime-factor sieve.
- The production accumulation uses compensated IEEE-754 binary64 summation.
  Its numerical status is cross-checked at fixed endpoints `10^k` and every
  `10,000`th point by an independent `Decimal` 80-significant-digit
  accumulation from the same exact coefficients.
- A reported nonzero sign is certified only when binary64 and Decimal signs
  agree and the Decimal absolute value exceeds `1e-60`; otherwise it is
  labeled `UNRESOLVED` rather than forced.
- Direct `Fraction` summation validates both coefficient formulas and signs
  for every `x<=200`; this is the exact oracle.  Decimal values are serialized
  only for audit checkpoints, not presented as exact rational values.

## Acceptance criteria

1. New, dependency-light code reproduces the frozen split without editing
   prior artifacts.
2. CSV/JSON retain all prime rows, fixed checkpoints, and provenance hashes.
3. Exact small-range and independent Decimal checks pass before results are
   interpreted.
4. Report separates discovery from holdout and makes no replacement
   conjecture.
