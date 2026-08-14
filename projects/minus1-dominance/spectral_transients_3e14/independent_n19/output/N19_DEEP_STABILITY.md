# N=19 deep spectral stability

Every one of the 17 nonprincipal characters has at least 100 positive
critical-line ordinates in the PARI dual-mesh list.  K is the number of
positive zeros retained per character.

## The -1 race

| K | top-decade correlation | RMSE | endpoint error |
|---:|---:|---:|---:|
| 25 | 0.971455692158 | 1.74492038408 | -1.72982518312 |
| 50 | 0.986558843853 | 1.41248982296 | -0.526978147898 |
| 100 | 0.992474652817 | 1.2521546704 | -0.531556489463 |

## Rank dynamics over all nine nonsquare classes

| source | K | rank changes | leader changes | rank agreement with observed | leader agreement with observed |
|---|---:|---:|---:|---:|---:|
| observed | NA | 17 | 8 | 1 | 1 |
| spectral | 25 | 12 | 5 | 0.77358490566 | 0.905660377358 |
| spectral | 50 | 11 | 5 | 0.849056603774 | 0.905660377358 |
| spectral | 100 | 14 | 7 | 0.905660377358 | 0.981132075472 |

K=100 improves the -1 curve correlation to more than 0.99 and reproduces
14 rank changes and seven leader changes across the 53 top-decade points.
The reconstructed rank and leader agreement with the observed data rise to
more than 0.90 and 0.98, respectively.  Thus the transient-rank conclusion
persists and strengthens at K=100; the sampled 300-trillion regime does not
look rank-stable.
