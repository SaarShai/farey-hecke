# Zeta-zero reciprocal-derivative sum: result

## Verdict

Using the natural two-sided convention

`S = Σ_{gamma in R} 1 / ((1/4 + gamma^2) |zeta'(1/2+i gamma)|^2)`,

the computation gives

**S = 0.02903 ± 0.00016**, with a conservative interval
`[0.02898, 0.02914]`.

The error bar is a numerical tail envelope, not a theorem-level bound. The
finite sum and root residuals are much more accurate than the infinite-tail
claim; the defensible precision here is about three significant digits.

**S = 2/pi^2 = 0.2026423673 is DEAD.** Its residual from the central estimate
is `0.1736074433`, roughly 6.0 times the estimate itself and far outside the
tail interval.

The computation uses positive ordinates from `zeros1.txt` and doubles the sum.
The negative ordinates give identical terms by conjugation. The E5 convention
is positive ordinates only, so it is one-half of the natural two-sided sum.

## Partial sums

| N | positive-ordinate sum | two-sided sum |
|---:|---:|---:|
| 100 | 0.014143636055307528 | 0.028287272110615056 |
| 300 | 0.014349494265830053 | 0.028698988531660105 |
| 1,000 | 0.014453988690945204 | 0.028907977381890409 |
| 3,000 | 0.014489912328235117 | 0.028979824656470234 |
| 10,000 | not completed | not reported |

The `N=3000` value is the exact sum of three independently computed chunks:
`N=1..1000`, `1001..2000`, and `2001..3000`. The attempted `N=10000`
extension was stopped after repeated bounded PARI/GP runs did not finish; no
unobserved value is inferred. This is recorded in `zero_sum_receipt.json`.

## Root refinement and sanity checks

`zeros1.txt` contains 100,000 positive ordinates with about nine decimal digits
in the seed table. Each of the 3,000 used seeds was refined by one real Newton
update applied to `zeta(1/2+i*t)` using PARI/GP's arbitrary-precision
`lfuninit` evaluator, then the residual and derivative were evaluated at the
refined ordinate.

The maximum residual over all 3,000 used zeros was
`5.2370020942838978552e-17`, versus the required strict threshold `1e-15`.
Failure count: `0`. The per-chunk maxima were `2.0877261576520969455e-18`,
`2.4389167939889694249e-18`, and `5.2370020942838978552e-17`.

The supplied Python environment had no importable `mpmath`, and package
installation was blocked by the network/DNS sandbox. The production fallback
used PARI/GP 2.17.3 at 20-digit real precision. A separate 30-digit PARI run
through `N=1000` gave the same displayed partial sums and maximum residual
`5.51057192390154456003139059199e-35`. The report does not claim mpmath was
run.

## Tail estimate

For a one-sided tail beginning at ordinate `T`, use the zero density

`dN/dt ~= log(t/(2*pi))/(2*pi)`

and hold the observed block mean `B = average(1/|zeta'(rho)|^2)` fixed. Since
the summand is approximately `B/t^2`,

`Tail_+(T) ~= B * (log(T/(2*pi)) + 1) / (2*pi*T)`.

The observed average `|zeta'(rho)|^2` grows across the computed blocks, while
the observed average inverse square falls:

| block | average `|zeta'(rho)|^2` | average `1/|zeta'(rho)|^2` |
|---:|---:|---:|
| 1–100 | 7.42485614 | 0.24098168 |
| 101–300 | 14.27673809 | 0.13525052 |
| 301–1,000 | 22.94594755 | 0.11955532 |
| 1,001–2,000 | 31.28689863 | 0.09610023 |
| 2,001–3,000 | 37.18530831 | 0.08341624 |

At `N=3000`, `T ~= 3533.328243396`. Using the final-block mean gives a
central one-sided tail estimate `2.7549660e-5`. For a conservative envelope,
take twice the largest inverse-square mean among the high blocks, namely
`2*0.1195553203`; this gives a one-sided tail bound `7.8970434e-5`, or
`1.5794087e-4` after restoring both signs. Adding the central tail to the
two-sided `N=3000` partial gives `0.02903492398`.

The numerical consistency check available without the unfinished `N=10000`
run is the observed one-sided increment

`S_3000^+ - S_1000^+ = 3.5923637e-5`,

versus the same density model's `N=1000` one-sided tail estimate
`8.6063909e-5`; their ratio is `0.4174`. The observed finite increment is
below the conservative extrapolation and of the same scale. This supports the
chosen error envelope but does not prove it.

## E5 convention reconciliation

The source anchors are `E5_zeta_zero_sum.py:4-17, 23, 26-40, 60-63`.

- E5 sets `mp.dps = 30` at line 23.
- Lines 26–36 sum `n=1..N` using one `mp.zetazero(n)` per positive zero. No
  conjugate-zero term is added.
- E5 uses `|rho|^2 = 1/4 + gamma^2`, exactly the convention used here.
- E5 actually runs `N=100` at lines 60–63.

Independent reproduction of that one-sided convention gives

`S_100^+ = 0.01414363605530752816632330319...`,

which displays as `0.0141436361`, exactly matching the E5 number to its stated
10 decimal places. The corresponding two-sided value is
`0.028287272110615056...`. Thus the only convention factor here is `2` from
including both signs; replacing `|rho|^2` by `gamma^2` is not what caused the
discrepancy.

## The Mikolás / `2/pi^2` normalization error

The exact conjecture location is `log.md:13`. It says that the empirical
Mikolás quantity `N·W(N)` tends to `2/3` and calls the displayed zero-sum value
`2/pi^2` a conjectured equivalent. The linked longer derivation is
`projects/mimo-mini-project/phase3_synthesis/FIVE_DISCOVERIES.md:25-49`; its
line 49 is where the `C = (pi^2/3) * S` bridge is invoked.

The algebra `C=2/3 => S=2/pi^2` is correct if the preceding normalization is
correct. The suspect step is the bridge recorded in the E5 handoff at
`E5_zeta_zero_sum.py:4-8`: `C = (pi^2/3) * S`. The local record presents this
as conjectural; it does not derive the normalization. With the computed
two-sided sum, that bridge would give

`(pi^2/3) * S ~= 0.09552107`,

not `2/3`. Equivalently, the asserted `2/pi^2` is larger than the measured
two-sided sum by a factor `6.9793`. The positive-versus-two-sided factor of two
has already been reconciled and cannot repair a factor `6.98` mismatch.

Therefore the precise local failure is the unverified normalization bridge
between the Farey/Mikolás constant and this zero sum, not the final algebraic
division by `pi^2`. The inspected `log.md` line does not contain enough
derivation to identify a more granular hidden factor; it should not be treated
as a settled equivalence.

The imported note `research_notes/imported_farey_now/SELBERG_INPUT_DISPROVED.md:27-31`
states the related RH-conditional limit as approximately `0.03`. The present
estimate rounds to `0.03` and differs from the literal comparison value by
`0.0009651`, so the imported note is consistent at its stated precision.

## Simple-form checks

Residuals below are absolute residuals from the central estimate
`0.029034923976884106`; all values and residuals are also in the JSON receipt.

| candidate | value | absolute residual |
|---|---:|---:|
| `3/pi^4` | 0.03079794676405301 | 0.001763022787168906 |
| `1/pi^3 = (2/pi^2)/(2*pi)` | 0.03225153443319950 | 0.003216610456315390 |
| `2/pi^4` | 0.02053196450936868 | 0.008502959467515430 |
| `1/(2*pi^3)` | 0.01612576721659975 | 0.012909156760284358 |
| `1/(2*pi^2)` | 0.05066059182116889 | 0.021625667844284782 |
| `(2/pi^2)/(2*pi)^2 = 1/(2*pi^4)` | 0.005132991127342169 | 0.023901932849541938 |
| `6/pi^4` | 0.06159589352810602 | 0.03256096955122192 |
| `2/pi^2` | 0.20264236728467555 | 0.17360744330779143 |

Among this small, preselected list, `3/pi^4` is closest, but its 0.00176
residual is much larger than the finite-sum numerical error and comparable to
the uncertainty in trying to infer any closed form from only three significant
digits. This is not evidence for `3/pi^4`; no closed form is claimed.

## Reproduction files and evidence

- `zero_sum_pari_driver.py`: reusable PARI/GP-backed computation driver.
- `assemble_zero_sum_receipt.py`: assembles the independently verified chunks
  and writes the numeric receipt.
- `zero_sum_receipt.json`: all numeric results, conventions, residual checks,
  tail values, E5 reconciliation, and candidate residuals.
