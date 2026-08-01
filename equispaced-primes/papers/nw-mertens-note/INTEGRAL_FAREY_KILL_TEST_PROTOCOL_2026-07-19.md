# Integral Farey discrepancy kill-test protocol

Date frozen: 2026-07-19, before the conditioned scan was run.

## Observable

This test uses exactly the observable in
`function-field/formal_conjectures_submission/FareyDiscrepancySign.lean`:

\[
D_N(x)=\#\{f\in F_N:f\le x\}-|F_N|x,\qquad
W(N)=\int_0^1D_N(x)^2\,dx,
\]

where (F_N) contains reduced fractions in ((0,1]), including (1), and

\[
\Delta W(p)=W(p-1)-W(p).
\]

It does **not** use the normalized discrete Franel--Landau wobble in older
project files.

Writing

\[
a(n)=\frac1n\prod_{q\mid n}(1-q),\qquad A(x)=\sum_{n\le x}a(n),
\]

the exact primitive-layer kernel gives

\[
\Delta W(p)=\frac{p-1}{6p}\bigl(A(p-1)-1\bigr)
\]

for prime (p).  The `-1` is load-bearing: the endpoint (1\in F_N)
contributes the extra cross-term that is absent from an interior-only Farey
portfolio.

## Population and event

- Limit: every prime (p\le100000).
- Qualifier: (M(p)\le-3), using an integer Möbius sieve and cumulative
  Mertens sum.
- Agreement event: `sign(DeltaW(p)) = sign(-M(p))`.  On the qualifying
  population this is exactly `DeltaW(p) > 0`.
- Arithmetic: `Fraction` exact rational accumulation.  A sign is certified by
  integer numerator comparison; floating point is display-only.

## Predeclared verdict gates

1. **Pointwise claim:** `FAIL` on the first qualifying prime with
   `DeltaW <= 0`; otherwise `PASS_TO_LIMIT`.  This is only a finite verdict.
2. **Density-one numerical support:** evaluate cumulative cutoffs 10000,
   30000, and 100000 and the terminal band `(30000,100000]`.
   `SUPPORTED_TO_LIMIT` requires all of:
   - at least 30 qualifying primes at every cumulative cutoff;
   - cumulative agreement proportions are nondecreasing;
   - the two-sided 95% Wilson lower bound at 100000 is at least 0.90;
   - terminal-band agreement is at least 0.90.
   Any failed gate is `NO_SUPPORT_TO_LIMIT`; missing data or an execution
   failure is `INCOMPLETE`.

No finite computation proves or disproves a density-one statement.  The
second verdict is deliberately labeled numerical support, not a theorem.

## Verification requirements

- Compare the closed formula with direct exact piecewise integration for every
  prime through 31.
- Independently compare Möbius and (a(n)) values with trial-division oracles
  through 200.
- Save all qualifying rows, cutoff and band summaries, source/protocol SHA-256
  hashes, and the exact first pointwise failure witness.
- Re-run from a clean command entry point and require byte-identical CSV and
  JSON outputs.

