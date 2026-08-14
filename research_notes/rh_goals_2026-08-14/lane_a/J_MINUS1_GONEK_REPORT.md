# Gonek's J_-1 slope: numerical test

## Verdict

**TOO EARLY** — completed through N=10000 (T=9877.78265401).

The through-origin top-half fit is `J_-1(T) = a T` with `a = 0.0927819176946`; the 500-zero incremental-slope scatter is `±0.01455` (sample standard deviation, not a confidence interval). The Gonek target is `3/pi^3 = 0.096754603300`. The first-versus-last top-half chunk-slope means are `0.10208146` and `0.086675125`, respectively, so the run is classified as `TOO EARLY` when that drift diagnostic fires. This is a finite-height diagnostic, not a confirmation or refutation of the asymptotic.

The classification is intentionally conservative: at these heights the observed slope/rate is still subject to substantial finite-T correction and chunk-to-chunk fluctuation.

## Requested and extended partial sums

Here `J_-1(T)` is the positive-ordinate sum over the first N refined zeros, with T = gamma_N. The ratio column compares `J_-1(T)/T` with `3/pi^3`.

| N | T = gamma_N | J_-1(T) | J_-1(T)/T | ratio to 3/pi^3 | max residual in chunk |
|---:|---:|---:|---:|---:|---:|
| 500 | 811.184358847 | 75.4356028893 | 0.0929944001836 | 0.9611367 | 1.26e-18 |
| 1000 | 1419.42248095 | 134.836996647 | 0.0949942659476 | 0.98180616 | 2.09e-18 |
| 1500 | 1980.91004309 | 184.610267815 | 0.093194675073 | 0.96320663 | 2.44e-18 |
| 2000 | 2515.28648292 | 230.937227096 | 0.0918134887074 | 0.94893148 | 2.44e-18 |
| 2500 | 3031.28921747 | 275.138444137 | 0.09076614747 | 0.93810676 | 5.24e-17 |
| 3000 | 3533.3282434 | 314.353470079 | 0.0889680913926 | 0.91952309 | 4.7e-17 |
| 3500 | 4023.9051514 | 357.433305088 | 0.0888274677556 | 0.91806968 | 1.03e-16 |
| 4000 | 4506.31149673 | 411.292517136 | 0.0912703255055 | 0.94331766 | 5.64e-17 |
| 4500 | 4980.11876253 | 455.928377791 | 0.0915496998226 | 0.94620511 | 1.02e-16 |
| 5000 | 5447.8619983 | 514.499284474 | 0.0944405869009 | 0.97608366 | 7.15e-17 |
| 5500 | 5909.432316 | 552.829026169 | 0.0935502763391 | 0.96688192 | 7.06e-17 |
| 6000 | 6365.85232102 | 597.550024543 | 0.0938680312407 | 0.97016605 | 7.21e-17 |
| 6500 | 6817.95747832 | 635.023653726 | 0.0931398671443 | 0.96264016 | 9.52e-17 |
| 7000 | 7264.74824809 | 682.669364479 | 0.0939701337425 | 0.97122132 | 9.63e-17 |
| 7500 | 7708.22097263 | 722.628449124 | 0.0937477599163 | 0.96892299 | 1.18e-16 |
| 8000 | 8148.1884058 | 760.079667045 | 0.0932820437122 | 0.96410962 | 7.6e-17 |
| 8500 | 8585.65146315 | 794.94166177 | 0.0925895565621 | 0.95695247 | 1.15e-16 |
| 9000 | 9018.42447561 | 830.361136161 | 0.0920738581785 | 0.95162251 | 8.81e-17 |
| 9500 | 9449.60972539 | 863.684493786 | 0.0913989592041 | 0.94464714 | 1.33e-16 |
| 10000 | 9877.78265401 | 906.886774848 | 0.0918107642792 | 0.94890332 | 1.3e-16 |

## Top-half linear fit and residual diagnostics

Fit window: completed checkpoints with N >= ceil(10000/2) = 5000. The reported slope is through the origin, matching the asymptotic form. `RMSE(J_-1) = 7.4399748`, `max |residual| = 13.068418`, `max relative residual = 0.017563097`, and through-origin `R^2 = 0.99989477`.

| N | J_-1(T) | fitted aT | residual | relative residual |
|---:|---:|---:|---:|---:|
| 5000 | 514.499284474 | 505.463083538 | 9.0362 | 0.0175631 |
| 5500 | 552.829026169 | 548.288462765 | 4.54056 | 0.00821332 |
| 6000 | 597.550024543 | 590.635986105 | 6.91404 | 0.0115706 |
| 6500 | 635.023653726 | 632.583169599 | 2.44048 | 0.00384314 |
| 7000 | 682.669364479 | 674.037274026 | 8.63209 | 0.0126446 |
| 7500 | 722.628449124 | 715.183523855 | 7.44493 | 0.0103026 |
| 8000 | 760.079667045 | 756.004546028 | 4.07512 | 0.00536144 |
| 8500 | 794.94166177 | 796.593207409 | -1.65155 | -0.00207757 |
| 9000 | 830.361136161 | 836.746717431 | -6.38558 | -0.00769013 |
| 9500 | 863.684493786 | 876.752911787 | -13.0684 | -0.015131 |
| 10000 | 906.886774848 | 916.479617209 | -9.59284 | -0.0105778 |

### Incremental-slope scatter

The uncertainty below is the sample standard deviation of the 500-zero slopes `Delta J_-1 / Delta T` in the top-half window. It is reported as scatter because adjacent blocks are not justified as independent random draws, and because drift is part of the finite-T effect.

| block | Delta T | Delta J_-1 | incremental slope |
|---:|---:|---:|---:|
| 4501–5000 | 467.743235772 | 58.5709066839 | 0.125220211014 |
| 5001–5500 | 461.570317703 | 38.3297416947 | 0.0830420419697 |
| 5501–6000 | 456.420005016 | 44.7209983743 | 0.0979821170912 |
| 6001–6500 | 452.105157301 | 37.4736291828 | 0.0828869756906 |
| 6501–7000 | 446.790769768 | 47.6457107524 | 0.106639872568 |
| 7001–7500 | 443.472724542 | 39.9590846457 | 0.0901049431778 |
| 7501–8000 | 439.967433173 | 37.4512179207 | 0.0851227047662 |
| 8001–8500 | 437.463057346 | 34.861994725 | 0.0796912885319 |
| 8501–9000 | 432.77301246 | 35.4194743905 | 0.0818430756325 |
| 9001–9500 | 431.185249779 | 33.3233576253 | 0.0772831576276 |
| 9501–10000 | 428.172928616 | 43.2022810621 | 0.100899141853 |

Chunk-slope scatter: `0.014553942`; nominal standard error of the mean (shown for reference only): `0.0043881787`.

## Numerical method and checkpoints

- PARI/GP 2.17.3 with `realprecision=20` and a reused `lfuninit` evaluator per chunk.
- Each seed from `cluster_universality_test/zeros1.txt` receives one real Newton update; the residual gate is `|zeta(1/2+i gamma)| < 1e-15`.
- Computation is chunked into 500-zero jobs. Completed chunks are stored under `research_notes/rh_goals_2026-08-14/lane_a/j_minus1_checkpoints/` and reused only when the source checksum and computation configuration match.
- The JSON receipt includes raw GP decimal strings, cumulative sums, all per-chunk maxima/failure counts, fit diagnostics, and the source checksum.

## Caveats

Finite-T corrections to Gonek's asymptotic are expected to be large at these heights. Even a run reaching T approximately 10^4 is far too short to support a definitive asymptotic claim; the verdict should be read as a numerical consistency/drift classification only. The derivative reciprocal weights can fluctuate strongly, so chunk scatter is informative but is not a rigorous uncertainty bound.

The literature context and the stated target `3/pi^3` are recorded in [`lane_c/S1_ZERO_SUM_LIT.md`](../lane_c/S1_ZERO_SUM_LIT.md).

## Reproduction

```bash
python3 research_notes/rh_goals_2026-08-14/lane_a/zero_sum_pari_driver.py --mode jminus1 --nmax 10000
```
