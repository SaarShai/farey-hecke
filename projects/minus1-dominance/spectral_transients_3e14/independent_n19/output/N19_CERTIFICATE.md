# Independent q=19 low-zero certificate

## Result

Python FLINT/Arb, without using PARI for the root search, evaluates the real Hardy
Z-function with sign-definite interval endpoints.  Continuity therefore proves that
at least one critical-line zero lies in the displayed bracket.  The computation does
not establish uniqueness, zero completeness below the bracket, or GRH.

| field | certified/computed value |
|---|---:|
| modulus / Conrey index | 19 / 13 |
| conductor / order | 19 / 18 |
| parity / chi(-1) | 1 / -1 |
| left endpoint | `0.01895639908022614299416416142284675655219221399702004258153398046224672068102271928157962443842821018` |
| right endpoint | `0.0189563990802261429941641614228467565521922139970200425815339804622467206810227192875143542795280844` |
| bracket width | `5.93472984109987421717077641848e-84` |
| Hardy Z endpoint signs | 1, -1 |
| midpoint | `0.01895639908022614299416416142284675655219221399702004258153398046224672068102271928454698935897814729` |
| Arb upper bound for abs L(midpoint) | `[3.540616796861935390428592865383403317380e-85 +/- 1.51e-125]` |
| top-decade one-mode RMS | 6.71932703334982214826479580548 |
| correlation with centered observed E_19(x;18,1) | 0.727600207814534860894972408247 |
| phase excursion over sampled top decade | 0.0436339043030932417144031228043 radians |
| later comparison with PARI ordinate | `0.018956399080226142994164161422846756552` |
| absolute FLINT-PARI difference | `1.922139970200425815339804622467206810227e-40` |

## Interpretation

This independently contradicts the manuscript's description of approximately
1.74 as the lowest complex q=19 ordinate: a critical-line zero exists near
0.018956399080226143.  Its very long log-x period and large top-decade RMS make it
an active slow mode at the 300-trillion scale.  The calculation alone does not
identify this zero as the globally lowest zero without an independent completeness
argument; the safe claim is existence far below 1.74.
