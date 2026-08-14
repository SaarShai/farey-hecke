# Spectral transient atlas through 300 trillion

**Internal manuscript-facing result.  The computation is verified; the explicit-formula
interpretation remains conditional and finite-scale.**

## Result in one paragraph

The ordinary prime-count curves through `3 x 10^14` are quantitatively reconstructed by the
low zeros of all nonprincipal Dirichlet `L`-functions modulo `N in {7,8,11,19,23}`.  On the
53-point top-decade window `x >= 3 x 10^13`, using the first 25 positive zeros of every
character gives correlations `0.965, 0.931, 0.939, 0.971, 0.826` with the observed `-1`
curves, respectively.  The same window still contains `17, 23, 30, 17, 39` changes in the
rank of `-1` across its 52 consecutive intervals.  Low-zero interference is therefore real
and strongly explanatory, but it has not disappeared near `3.18 x 10^14`.

## Reproducible package

Package: `projects/minus1-dominance/spectral_transients_3e14/`

Primary figure:
`projects/minus1-dominance/spectral_transients_3e14/output/spectral_reconstruction.pdf`

The package contains:

- a PARI/GP generator covering all 55 nonprincipal characters;
- two `lfunzeros` mesh checks, with subdivisions 64 and 96, through height 80;
- direct residual checks `abs(L(1/2+i*gamma,chi)) < 1e-28` for every returned zero;
- an independent match of all three modulo-8 first-zero anchors against the pre-existing
  mpmath data to `1e-12`;
- the explicit-formula reconstruction, fit metrics, transition ledger, per-mode attribution,
  figure source, verifier, and SHA-256 manifest.

The two PARI meshes use the same underlying implementation and are a robustness check, not
an independent zero-completeness proof.  The prior mpmath match is independent but covers
only three anchors.

## Normalization and truncation

For a unit class `a`, the observed curve is

```text
E_N(x;a,1) = phi(N) log(x)/sqrt(x) * (pi(x;N,a) - pi(x;N,1)).
```

The reconstruction uses the GRH explicit-formula truncation

```text
C_N(1) - C_N(a)
  - sum_(chi != chi0) sum_(gamma_chi > 0)
      2 Re((conj(chi(a))-1) exp(i gamma log x)/(1/2+i gamma)),
```

where `C_N(a)` is the number of unit square roots of `a`.  Truncation level `K` means the
first `K` positive zeros of **each** nonprincipal character, not the first `K` modes globally.

## Top-decade reconstruction of the `-1` curve

| N | correlation, 1 zero/character | correlation, 25 zeros/character | RMSE at 25 | endpoint reconstruction error at 25 |
|---:|---:|---:|---:|---:|
| 7  | 0.731 | **0.965** | 0.515 | -0.056 |
| 8  | 0.616 | **0.931** | 0.626 | -0.597 |
| 11 | 0.806 | **0.939** | 0.919 | +0.183 |
| 19 | 0.751 | **0.971** | 1.745 | -1.730 |
| 23 | 0.038 | **0.826** | 1.728 | -2.322 |

The low modes already explain much of the slowly varying structure for `N=7,11,19`.  For
`N=23`, one zero per character is insufficient: many modes interfere materially, and the
correlation becomes useful only after a deeper truncation.  This directly warns against a
one-mode onset argument.

## Observed instability in the top decade

| N | rank changes in 52 intervals | leader changes | fraction of points where `-1` leads | endpoint rank | endpoint leader |
|---:|---:|---:|---:|---:|---:|
| 7  | 17 | 13 | 0.358 | 1/3 | 6 |
| 8  | 23 | 15 | 0.358 | 3/3 | 5 |
| 11 | 30 | 26 | 0.377 | 3/5 | 7 |
| 19 | 17 | 8  | 0.415 | 6/9 | 3 |
| 23 | 39 | 23 | 0.132 | 1/11 | 22 |

Every modulus visits rank 1 during the top decade, and every modulus also leaves it.  The
endpoint is therefore not evidence of a settled ranking.

## Load-bearing correction to the manuscript's `N=19` narrative

The manuscript calls `gamma approximately 1.74` the lowest zero of the complex characters
modulo 19.  PARI instead returns

```text
q = 19, Conrey index = 13, character order = 18,
gamma = 0.0189563990802261, chi(-1) = -1.
```

Both meshes return this ordinate, and direct evaluation gives
`abs(L(1/2+i*gamma,chi))` far below `1e-28`.  This mode is active in the `-1` race, has
top-decade RMS contribution `6.719`, and alone correlates `0.728` with the centered observed
curve.  Thus the printed `318`-trillion calculation omits a much lower, much slower mode and
cannot be described as the scale where complex-character interference subsides.

## Safe manuscript conclusion

> The unregularized races remain spectrally coherent but dynamically unsettled through
> `3 x 10^14`.  Low-zero explicit-formula truncations reproduce the observed trajectories
> with high correlation, while frequent rank and leader changes persist throughout the top
> decade.  These data support a low-zero transient mechanism, not a universal stabilization
> threshold or an eventual ordinary-count ordering.

## Limits

- The reconstruction assumes the standard GRH critical-line form of the explicit formula.
- A finite zero list does not prove zero completeness or GRH.
- High correlation is explanatory numerical evidence, not a theorem.
- This analysis concerns ordinary counts.  It does not validate the manuscript's separate
  Gaussian-regularized statistic or transfer a result between the two statistics.

