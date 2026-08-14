# Verified numerical evidence through 300 trillion

**Internal working appendix - suitable for later manuscript adaptation after the theory is fixed.**

## Dataset and validation

- File: `projects/minus1-dominance/curve_3e14.tsv`
- SHA-256: `57957bdb3ce3243272c3d4b8e9ffe7dfb734b759f48b63becf7ae6f924e1caab`
- Range: `x <= 3 x 10^14`
- Moduli: `N in {7,8,11,19,23}`
- Grid: 438 logarithmically spaced checkpoints
- Recorded runtime: 98,498 seconds
- Current rerun of `minus1_curve_analysis.py`: **567/567 exact integer agreements, zero mismatches** against the prior independently checked baseline at nine shared checkpoints through `1.3 x 10^13`.

This proves consistency of the extended curve with the earlier baseline.  It is not a second
full independent-hardware replication of every point through `3 x 10^14`.

## Ordinary prime-count differences at `x = 3 x 10^14`

The table ranks quadratic nonresidues by
`D_N(a)=pi(x;N,a)-pi(x;N,1)`.

| N | Rank of `a=-1` | Leading class | `D_N(-1)` | Complete nonresidue order (largest first) |
|---:|---:|---:|---:|---|
| 7 | **1/3** | 6 | +324,843 | `6, 3, 5` |
| 8 | **3/3** | 5 | +505,845 | `5, 3, 7` |
| 11 | **3/5** | 7 | +137,533 | `7, 6, 10, 2, 8` |
| 19 | **6/9** | 3 | -16,802 | `3, 10, 13, 8, 2, 18, 15, 12, 14` |
| 23 | **1/11** | 22 | +294,472 | `22, 21, 5, 11, 15, 14, 7, 10, 19, 20, 17` |

Therefore `-1` strictly leads the ordinary-count race only for `N=7` and `N=23` at this
endpoint.  It is last among the three nonresidues for `N=8`, middle for `N=11`, and below
the principal class for `N=19`.

## RS-normalized empirical variance over the curve

For

```text
E(x;N,a) = (log x / sqrt(x)) (pi(x;N,a)-pi(x;N,1)),
```

the sample-variance ranks are:

| N | Full 438-point grid | `x >= 10^13` | Top decade `x >= 3 x 10^13` |
|---:|---|---|---|
| 7 | `-1` is maximum | `-1` is maximum | `-1` is maximum |
| 11 | rank 2/5; max `a=6` | rank 4/5; max `a=6` | rank 3/5; max `a=6` |
| 19 | rank 2/9; max `a=14` | rank 2/9; max `a=14` | **`-1` is maximum** |
| 23 | rank 5/11; max `a=5` | rank 11/11; max `a=11` | rank 10/11; max `a=20` |

The raw endpoint rank and the empirical-variance rank do not coincide.  At `N=19`, for
example, `-1` becomes variance-maximal in the top decade while its endpoint difference is
negative.

## Defensible interpretation

The curve is strong evidence of persistent, modulus-dependent transients around the proposed
onset scale.  It **does not** establish a universal ordinary-count dominance theorem and does
not show that spectral interference disappears at `3.18 x 10^14`.  The endpoint is near the
one-mode heuristic threshold, not demonstrably inside a stable asymptotic regime.

Safe manuscript language:

> At `x=3 x 10^14`, the unregularized races remain strongly modulus-dependent: the class
> `-1` leads for `N=7,23` but not for `N=8,11,19`.  The evolution across the log grid and the
> top-decade variance behavior for `N=19` are consistent with substantial low-zero transients,
> but do not by themselves prove an eventual ordering.

## Open numerical item

Before publication, reconcile the earlier `N=11, a=10` value at `x=1.3 x 10^13`: our
identity-reconstructing and lower-checkpoint-consistent value is `11,503`, whereas Koyama's
table gives `71,711`.  The discrepancy changes the qualitative placement of `-1` and cannot
be left as a convention difference without matching raw counts and definitions.

