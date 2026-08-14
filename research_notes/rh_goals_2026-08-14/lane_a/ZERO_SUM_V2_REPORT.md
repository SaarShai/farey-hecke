# Zero-sum V2 report

## Verdict

**S = 0.029032731101 +/- 1.79e-05; digits claimed: 3 significant digits; 4 significant digits are not certified by the tail bar.**

The N=10,000 positive partial sum is `0.014507394686525`. The fitted central one-sided tail is `8.97086399804e-06` and the max-block envelope is `1.28359904688e-05`. The requested absolute 1e-5 bar is **not achieved**: the remaining uncertainty is dominated by the non-rigorous tail envelope at T=9877.78265401, not backend precision.

The five displayed decimal places are not all claimed as significant digits; the conservative tail model supports the stated digit count only.

## Partial sum and tail

The natural convention is two-sided over conjugate zeros; all computed positive-ordinate terms are doubled in S.

| N | gamma_N | positive partial sum | two-sided partial sum |
|---:|---:|---:|---:|
| 100 | 236.524229666 | 0.014143636055308 | 0.028287272110615 |
| 300 | 541.847437121 | 0.014349494265830 | 0.028698988531660 |
| 1000 | 1419.42248095 | 0.014453988690945 | 0.028907977381890 |
| 3000 | 3533.3282434 | 0.014489912328235 | 0.028979824656470 |
| 3500 | 4023.9051514 | 0.014492932126721 | 0.028985864253442 |
| 4000 | 4506.31149673 | 0.014495875642118 | 0.028991751284236 |
| 4500 | 4980.11876253 | 0.014497884953134 | 0.028995769906268 |
| 5000 | 5447.8619983 | 0.014500060455490 | 0.029000120910980 |
| 5500 | 5909.432316 | 0.014501254044013 | 0.029002508088025 |
| 6000 | 6365.85232102 | 0.014502447556514 | 0.029004895113027 |
| 6500 | 6817.95747832 | 0.014503310096632 | 0.029006620193263 |
| 7000 | 7264.74824809 | 0.014504274121121 | 0.029008548242241 |
| 7500 | 7708.22097263 | 0.014504987209119 | 0.029009974418239 |
| 8000 | 8148.1884058 | 0.014505585650601 | 0.029011171301201 |
| 8500 | 8585.65146315 | 0.014506084504022 | 0.029012169008043 |
| 9000 | 9018.42447561 | 0.014506541477924 | 0.029013082955848 |
| 9500 | 9449.60972539 | 0.014506932876633 | 0.029013865753265 |
| 10000 | 9877.78265401 | 0.014507394686525 | 0.029014789373050 |

For the Gonek comparison, the empirical block mean is B(t)=mean(1/|zeta'(rho)|^2), while the asymptotic prediction is B_G(t)=(6/pi^2)/log(t/(2*pi)). A through-origin fit B=alpha B_G is made on the 500-zero blocks whose lower endpoint has N>=5001.

Fit slope alpha = `0.915845260536`; B/B_G mean = `0.915202150596`, range = [`0.799502643139`, `1.10063480746`], block-mean RMSE = `0.00832365`.

The density-weighted integrand is B(t) log(t/(2*pi))/(2*pi*(t^2+1/4)). Under the fitted Gonek form the logarithms cancel, giving central one-sided tail alpha*(3/pi^3)*2*atan(1/(2T)). The conservative envelope holds B at the maximum selected block mean and uses the corresponding density integral.

T = `9877.7826540055011428`; central one-sided tail = `8.97086399804113e-06`; envelope one-sided tail = `1.2835990468773e-05`; selected max block mean = `0.0952914215049`.

The envelope is a numerical extrapolation, not a theorem-level bound against an unseen unusually small zeta derivative.

## Error budget

- Tail-model symmetric contribution to the two-sided bar: `1.79417e-05` (interval is from the positive partial sum to the envelope).
- Backend cross-check contribution: `4.90891e-25` from realprecision 20 versus 30 over every A4 chunk; maximum single-chunk difference `4.74178e-26`.
- A4 seed/root first-order propagation: `2.12783e-21` two-sided, from residual/|zeta'| root displacement and the local derivative of the complete weighted term; maximum A4 root displacement `4.99361e-17`.
- Inherited N<=3000 seed sensitivity: `not fully per-zero propagated; reused N<=3000 receipt has residual gate and N<=1000 realprecision-30 displayed-sum cross-check`. The inherited receipt supplies residual maxima and a realprecision-30 N<=1000 displayed-sum cross-check, but not per-zero zeta'' values, so an independent per-zero propagation for that already-computed range was intentionally not repeated.

The tail term is orders of magnitude larger than the measured numerical budgets. The seed statement is therefore explicit about the one residual limitation that remains in the reused legacy aggregate; it is not silently promoted to a rigorous bound.

## Candidate closed forms

Residuals are measured against the central estimate in units of the final conservative one-sigma-style bar. Every candidate remains excluded by more than 5 sigma.

| candidate | value | absolute residual | sigma units | verdict |
|---|---:|---:|---:|---|
| `3/pi^4` | 0.0307979467641 | 0.00176522 | 98.386 | EXCLUDED |
| `1/pi^3 = (2/pi^2)/(2*pi)` | 0.0322515344332 | 0.0032188 | 179.403 | EXCLUDED |
| `2/pi^4` | 0.0205319645094 | 0.00850077 | 473.799 | EXCLUDED |
| `1/(2*pi^3)` | 0.0161257672166 | 0.012907 | 719.382 | EXCLUDED |
| `1/(2*pi^2)` | 0.0506605918212 | 0.0216279 | 1205.45 | EXCLUDED |
| `(2/pi^2)/(2*pi)^2 = 1/(2*pi^4)` | 0.00513299112734 | 0.0238997 | 1332.08 | EXCLUDED |
| `6/pi^4` | 0.0615958935281 | 0.0325632 | 1814.94 | EXCLUDED |
| `2/pi^2` | 0.202642367285 | 0.17361 | 9676.31 | EXCLUDED |

## Residual and source checks

A3/A4 source SHA-256: `3436c916a7878261ac183fd7b9448c9a4736b8bbccf1356874a6ce1788541632`. Refined zeros used: 10000; maximum residual: `1.32504e-16`; strict threshold: `1e-15`; failures: 0.

The A4 weighted chunk sums reproduce A3's J_-1 chunks on the overlapping range with maximum absolute difference `0` in the reciprocal-derivative sum and matching boundary ordinates.

Reproduction:

```bash
python3 research_notes/rh_goals_2026-08-14/lane_a/zero_sum_v2_driver.py --nmax 10000
python3 research_notes/rh_goals_2026-08-14/lane_a/zero_sum_v2_backend_crosscheck.py --nmax 10000
python3 research_notes/rh_goals_2026-08-14/lane_a/analyze_zero_sum_v2.py
```
