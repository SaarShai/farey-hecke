# Family sweep fill

New sequential certified-midpoint surface scans for the arithmeticity-law table and blind-test pool. Each surface had its validation gate run before new-territory evaluation.

## G_8 even

Verdict: **SCATTER**

Evidence status: **SCATTER**; the four-independent-pin gate is met.

Supporting stats:

- N-stable pinned count: `8`.
- Re mean/std/range: `0.369890394361` / `0.112496581253` / `0.345740817327`.
- Re min/max: `0.121428898693` / `0.46716971602`.
- Surface coverage: Re `[0.1, 0.49, 16]`, Im `[3.0, 17.0, 141]`; 2256/2256 cells evaluated; evaluation errors `0`.
- Wall time: `683.261496583` seconds.

Validation gate:

- Gate: **PASS**.
- Known pin: `s=0.5+5.798144i`.
- Reproduced value: `|det|=2.57933248921e-07` at the known G8 odd-sector anchor; opposite-sector value `0.824213033787`.
- Match tolerance: known-sector `|det| < 1e-05`; opposite-sector `|det| > 0.01`.

Pinned coordinates and N-stability:

| coordinate `(Re, Im)` | `|det|` N=22 | `|det|` N=28 | `ΔRe` | `ΔIm` | stable |
|---:|---:|---:|---:|---:|:---:|
| `(0.425231042374, 4.34576078832)` | `2.07882393991e-16` | `1.20796736129e-15` | `2.57405208259e-13` | `4.67181848762e-13` | `True` |
| `(0.301268784887, 5.84679320246)` | `2.39201493008e-15` | `5.46717549506e-16` | `5.19012610667e-11` | `3.22240012451e-11` | `True` |
| `(0.437608560357, 7.27867174399)` | `1.29120026553e-15` | `7.62076891188e-16` | `5.32451915891e-10` | `2.07628580995e-10` | `True` |
| `(0.30377859726, 7.95881180906)` | `7.27444748494e-16` | `2.62362176493e-17` | `1.14770709048e-08` | `4.18198808916e-09` | `True` |
| `(0.121428898693, 8.31733177778)` | `6.51177744076e-15` | `1.00856016595e-15` | `2.85285935847e-08` | `4.33058975347e-08` | `True` |
| `(0.44592111356, 9.55726809847)` | `6.14499913326e-15` | `6.40995211516e-15` | `5.33560596816e-08` | `7.50291029306e-08` | `True` |
| `(0.456716441739, 11.4163897099)` | `4.23687761481e-15` | `5.56739517001e-15` | `7.90838321385e-07` | `2.80079149029e-06` | `True` |
| `(0.46716971602, 12.2621403083)` | `4.71276281621e-15` | `2.55537150988e-15` | `4.82917829336e-07` | `2.86700427949e-05` | `True` |

## extended q=4

Verdict: **LINE**

Evidence status: **INSUFFICIENT-DATA**; the four-independent-pin gate is not met.

Supporting stats:

- N-stable pinned count: `3`.
- Re mean/std/range: `0.249999999994` / `9.82914237059e-12` / `2.1962570651e-11`.
- Re min/max: `0.24999999998` / `0.250000000002`.
- Surface coverage: Re `[0.1, 0.49, 16]`, Im `[3.0, 30.0, 271]`; 4336/4336 cells evaluated; evaluation errors `0`.
- Wall time: `384.63688425` seconds.

Validation gate:

- Gate: **PASS**.
- Known pin: `s=0.24999999998+12.50542879i`.
- Reproduced N=22/N=28 values: `s22=0.250000232265+12.5054286855i`, `s28=0.24999999998+12.50542879i`.
- Match tolerance: `|ΔRe|,|ΔIm| < 0.002`; known-to-N=28 delta `(0, 0)`.

Pinned coordinates and N-stability:

| coordinate `(Re, Im)` | `|det|` N=22 | `|det|` N=28 | `ΔRe` | `ΔIm` | stable |
|---:|---:|---:|---:|---:|:---:|
| `(0.25, 7.06736257087)` | `3.12766866915e-16` | `1.74159933736e-16` | `4.25739998811e-12` | `1.19371179608e-12` | `True` |
| `(0.250000000002, 10.5110198194)` | `5.05984966074e-16` | `1.98140767303e-15` | `1.31386099222e-09` | `9.73396474535e-09` | `True` |
| `(0.24999999998, 12.50542879)` | `4.21426971137e-15` | `1.19154886797e-14` | `2.32284167817e-07` | `1.04454127126e-07` | `True` |

## extended q=6

Verdict: **LINE**

Evidence status: **INSUFFICIENT-DATA**; the four-independent-pin gate is not met.

Supporting stats:

- N-stable pinned count: `2`.
- Re mean/std/range: `0.24999999999` / `1.02558933568e-11` / `2.05117867136e-11`.
- Re min/max: `0.249999999979` / `0.25`.
- Surface coverage: Re `[0.1, 0.49, 16]`, Im `[3.0, 30.0, 271]`; 4336/4336 cells evaluated; evaluation errors `0`.
- Wall time: `820.887542416` seconds.

Validation gate:

- Gate: **PASS**.
- Known pin: `s=0.249999999979+10.5110198194i`.
- Reproduced N=22/N=28 values: `s22=0.24999993378+10.5110197285i`, `s28=0.249999999979+10.5110198194i`.
- Match tolerance: `|ΔRe|,|ΔIm| < 0.002`; known-to-N=28 delta `(0, 0)`.

Pinned coordinates and N-stability:

| coordinate `(Re, Im)` | `|det|` N=22 | `|det|` N=28 | `ΔRe` | `ΔIm` | stable |
|---:|---:|---:|---:|---:|:---:|
| `(0.25, 7.06736257087)` | `1.44416110824e-15` | `1.04973227919e-15` | `7.81473497025e-11` | `7.03765934418e-11` | `True` |
| `(0.249999999979, 10.5110198194)` | `1.27529100886e-14` | `1.04034891833e-14` | `6.61998266482e-08` | `9.09398689686e-08` | `True` |

## Caveats

- G8 coverage is Re `[0.1,0.49]` on 16 grid values and Im `[3,17]` on 141 values. q4 and q6 coverage is the same Re grid and Im `[3,30]` on 271 values. These are finite scans, not completeness proofs.
- The surface is a midpoint determinant locator followed by Newton pinning and an N=22 to N=28 stability comparison. Reported coordinates are not interval enclosures.
- No winding certificates exist yet for any new result. In particular, the G8 validation pin is the existing odd-sector anchor and does not certify any new even-sector off-line zero.
- The q4 and q6 extended scans did not reach the four-independent-pin evidence threshold: q4 produced three stable line pins and q6 produced two. Their displayed `LINE` verdicts are law predictions consistent with the observed coordinates, not promoted four-point confirmations.
- The G8 even result reaches eight stable pins with a wide Re spread and is reported as `SCATTER` under the preregistered non-arithmetic prediction.

Receipt: `FAMILY_SWEEP_FILL_RECEIPT.json`.
