# Exact integral Farey discrepancy kill-test report

## Verdict

- Pointwise sign claim: **FAIL**.
- Predeclared density-one numerical-support gate: **NO_SUPPORT_TO_LIMIT**.
- Scope: this is a decisive finite refutation of the pointwise claim and
  strong finite counterevidence, not a proof that a density-one asymptotic is
  false.

Among all 4,617 primes (p\le100000) with (M(p)\le-3), the exact integral
observable agreed with `sign(-M(p))` **zero times**.

The first qualifying prime already fails:

\[
p=13,\qquad M(13)=-3,\qquad
A(12)-1=-\frac{95083}{27720},
\]

and therefore

\[
\Delta W(13)=W(12)-W(13)
=-\frac{95083}{180180}<0,
\]

whereas `sign(-M(13))=+1`.

## Matched observable and exact reduction

For the formal Lean definition, (F_N\subset(0,1]) includes the endpoint
(1), and

\[
D_N(x)=\#\{f\in F_N:f\le x\}-|F_N|x,
\qquad W(N)=\int_0^1D_N(x)^2\,dx.
\]

The primitive denominator-layer kernel gives, for prime (p),

\[
\Delta W(p)=\frac{p-1}{6p}\left(A(p-1)-1\right),
\quad
A(x)=\sum_{n\le x}\frac1n\prod_{q\mid n}(1-q).
\]

An interior-only Farey portfolio instead has driver (2-A(p-1)).  The
endpoint (1) contributes

\[
2\langle h_1,h_p\rangle=-\frac{p-1}{6p},
\]

which changes the load-bearing constant from 2 to 1.  This is why the older
discrete-wobble and interior-layer computations did not answer the formal
question.

## Frozen gates and results

The protocol was written before the conditioned scan:
[`INTEGRAL_FAREY_KILL_TEST_PROTOCOL_2026-07-19.md`](INTEGRAL_FAREY_KILL_TEST_PROTOCOL_2026-07-19.md).

| cutoff | qualifying | agreements | proportion | Wilson 95% upper |
|---:|---:|---:|---:|---:|
| 10,000 | 598 | 0 | 0 | 0.006383 |
| 30,000 | 1,732 | 0 | 0 | 0.002213 |
| 100,000 | 4,617 | 0 | 0 | 0.000831 |

The terminal band `(30000,100000]` contains 2,885 qualifying primes and zero
agreements.  Both load-bearing density-support thresholds fail.

## Reproduction and verification

From this directory:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_integral_farey_kill_test.py
PYTHONDONTWRITEBYTECODE=1 python3 integral_farey_kill_test.py
```

The tests compare the closed formula to direct exact piecewise integration at
every prime through 31 and independently check the Möbius sieve and arithmetic
coefficient through 200.  The scan uses Python `Fraction`; signs are integer
comparisons, while decimal columns are display-only.

Artifacts:

- [`integral_farey_kill_test.py`](integral_farey_kill_test.py)
- [`test_integral_farey_kill_test.py`](test_integral_farey_kill_test.py)
- [`integral_farey_kill_test_p100000.csv`](integral_farey_kill_test_p100000.csv)
- [`integral_farey_kill_test_p100000.json`](integral_farey_kill_test_p100000.json)

Recorded hashes:

- script: `dad8b73ff0e26529fd1eb5fce016504ef48b5b7319b554364c73bc087feaca02`
- frozen protocol: `25e5a1dfff4833d4110b1b8182c8f25a88b46eddd542b0b0aace143e4b263111`
- CSV: `b398c923f53823fa4dc26e3f31f7e1f155051a22054f16c56a11a2ee715fb0e2`

## Research consequence

The proposed `FareyDiscrepancySign` submission should be withdrawn, not
defended with the old numerical records.  A sign-reversed conjecture would fit
this finite range, but proposing it now would be post hoc.  The next legitimate
step is to study the exact driver (A(x)-1) on its own and derive any relation
to Mertens values before stating a replacement conjecture.

