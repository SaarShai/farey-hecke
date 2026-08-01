# A-driver discovery/holdout report

## Verdict

The frozen two-way characterization is **DIFFERS** across its discovery range
`[1, 1,000,000]` and holdout range `(1,000,000, 2,000,000]`.  It does not
support a replacement conjecture.

The driver is emphatically not sign-fixed: after the exact zero at `x=1`, it
has both signs in each split and changes sign 2,739 times in discovery and
1,355 times in holdout.  The first recorded nonzero sign change is at
`x=3293` in discovery and `x=1,019,861` in holdout.

## Frozen observable

\[
a(n)=\frac1n\prod_{q\mid n}(1-q),\qquad A(x)=\sum_{n\le x}a(n),
\]

and the Farey prime-step sign is the sign of `A(p-1)-1`.  The protocol,
including the discovery/holdout split and all metrics, was frozen before the
scan: [`A_DRIVER_PROTOCOL_2026-07-19.md`](A_DRIVER_PROTOCOL_2026-07-19.md).

The exact second form used for validation is

\[
a(n)=\sum_{d\mid n}\frac{\mu(d)}{n/d},qquad
A(x)=\sum_{d\le x}\mu(d)H_{\lfloor x/d\rfloor}.
\]

## Integer-level behavior

| split | negative | zero | positive | sign changes | corr(`A(x)-1`,`M(x)`) | mean `abs(A(x)-1)/sqrt(x)` |
|---|---:|---:|---:|---:|---:|---:|
| discovery | 683,715 | 1 | 316,284 | 2,739 | 0.970578 | 0.098630 |
| holdout | 532,168 | 0 | 467,832 | 1,355 | 0.960649 | 0.084549 |

The required fixed cumulative decade blocks `[1,10^k]`, intersected with each
split and truncated at its boundary, are below.  The normalization is
descriptive, not an estimated power law.

| split | global block | split intersection | count | mean | min | max |
|---|---|---|---:|---:|---:|---:|
| discovery | `[1,1]` | `[1,1]` | 1 | 0 | 0 | 0 |
| discovery | `[1,10]` | `[1,10]` | 10 | 0.742371 | 0 | 1.035803 |
| discovery | `[1,100]` | `[1,100]` | 100 | 0.864136 | 0 | 1.207360 |
| discovery | `[1,1,000]` | `[1,1,000]` | 1,000 | 0.530962 | 0 | 1.207360 |
| discovery | `[1,10,000]` | `[1,10,000]` | 10,000 | 0.260766 | 0 | 1.207360 |
| discovery | `[1,100,000]` | `[1,100,000]` | 100,000 | 0.132470 | 0 | 1.207360 |
| discovery | `[1,1,000,000]` | `[1,1,000,000]` | 1,000,000 | 0.098630 | 0 | 1.207360 |
| holdout | `[1,10,000,000]` | `[1,000,001,2,000,000]` | 1,000,000 | 0.084549 | 1.85e-7 | 0.256571 |

Over integers with nonzero Mertens value, the reversed-sign agreement
`sign(A(x)-1)=sign(M(x))` is 0.835556 in discovery and 0.878357 in holdout.
This is a strong finite association, not a deterministic identity: the many
driver sign changes and the non-unit agreement rates are load-bearing
counterexamples to that interpretation.

## Prime-conditioned behavior

The table uses the predeclared reversed orientation
`sign(A(p-1)-1)=sign(M(p))`; the final column is the complementary orientation
used by the refuted Farey claim.

| condition | discovery n | reversed rate | original rate | holdout n | reversed rate | original rate |
|---|---:|---:|---:|---:|---:|---:|
| `M(p)<=-3` | 40,155 | 0.994222 | 0.005778 | 32,845 | 0.937890 | 0.062110 |
| `M(p)>=3` | 36,029 | 0.674429 | 0.325571 | 36,888 | 0.833360 | 0.166640 |
| `M(p)!=0` | 78,014 | 0.835581 | 0.164419 | 70,259 | 0.879802 | 0.120198 |

Every nonempty conditioned rate stayed on the same side of 1/2 in holdout.
Nevertheless, the protocol literally requires the *sign inventory* to match:
discovery contains `{negative, zero, positive}` because `A(1)-1=0`, while
holdout contains `{negative, positive}`.  The required mechanical verdict is
therefore `DIFFERS`; it is not legitimate to coarsen both inventories to
"mixed".  No sign-reversed conjecture is proposed: no candidate passed the
frozen holdout gate, and a finite directional pattern cannot establish a
density or asymptotic law.

## Arithmetic status and reproducibility

The coefficient sieve, Möbius values, Mertens values, and numerator products
are integer computations.  Direct `Fraction` computation verifies the two
driver formulas for every `x<=200` and reproduces

\[
A(12)-1=-95083/27720.
\]

The full scan uses compensated binary64 accumulation alongside a Decimal
80-significant-digit accumulation.  At all 2,000,000 scan points the two
non-tiny signs agreed; the conflict count is zero.  This is a strong
reproducibility check, but it is not a formal interval-arithmetic proof for
the large range.

Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v A_DRIVER_TEST_2026-07-19.py
PYTHONDONTWRITEBYTECODE=1 python3 A_DRIVER_ANALYSIS.py
```

The second clean run produced byte-identical artifacts.  SHA-256:

- `A_DRIVER_PRIMES_2026-07-19.csv`: `48bdd0ce9f210fb0f52cdcf146090d1804d26753564dade3ce18f179efd7f1a4`
- `A_DRIVER_CHECKPOINTS_2026-07-19.csv`: `1a0ffce2255350ba0fea4792a1161a6baac4550f14a59cb1ca4cb6ac0eb2b7cf`
- `A_DRIVER_RESULTS_2026-07-19.json`: `e67a7a5890badf1f9b62497895729132bf33b08f858e0da7d231b7c7c67ef9ed`

Artifacts:

- [`A_DRIVER_ANALYSIS.py`](A_DRIVER_ANALYSIS.py)
- [`A_DRIVER_TEST_2026-07-19.py`](A_DRIVER_TEST_2026-07-19.py)
- [`A_DRIVER_PRIMES_2026-07-19.csv`](A_DRIVER_PRIMES_2026-07-19.csv)
- [`A_DRIVER_CHECKPOINTS_2026-07-19.csv`](A_DRIVER_CHECKPOINTS_2026-07-19.csv)
- [`A_DRIVER_RESULTS_2026-07-19.json`](A_DRIVER_RESULTS_2026-07-19.json)

## Limitation and next theorem-shaped question

The evidence identifies a useful exact reduction and a high finite
association with the Mertens function.  The next legitimate step is analytic:
derive a summation-by-parts or Dirichlet-series relation that gives effective
control of `A(x)-1` from information about `M(x)`, then state only a theorem
whose hypotheses and conclusion are independently justified.
