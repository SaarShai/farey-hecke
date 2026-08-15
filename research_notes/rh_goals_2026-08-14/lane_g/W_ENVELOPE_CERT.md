# T-b certified weight envelope

## VERDICT SUMMARY

The requested absolute tail-weight certificate does not close any flagship box. Every box has `Re(s)<1/2`, so the required deep-tail majorant `sum_n |theta'_n(z)^s|` has exponent `2 Re(s)<1` and diverges. The receipt contains the fixed-contour lower-bound witness, not only a failed upper estimate.

| box | certified W* | certified F(W*, rho*=0.697802, N=48) | comparison to TC_PREP 3.94e-6 | VERDICT | minimal certifying N |
|---|---:|---:|---|---|---:|
| g5_pin_1 | `+inf` | `+inf` | FAIL: F=+inf exceeds contour lower bound | **NOT** | none |
| g5_pin_2 | `+inf` | `+inf` | FAIL: F=+inf exceeds contour lower bound | **NOT** | none |
| g5_pin_3 | `+inf` | `+inf` | FAIL: F=+inf exceeds contour lower bound | **NOT** | none |
| g5_pin_4 | `+inf` | `+inf` | FAIL: F=+inf exceeds contour lower bound | **NOT** | none |
| g5_pin_5 | `+inf` | `+inf` | FAIL: F=+inf exceeds contour lower bound | **NOT** | none |
| g5_pin_6 | `+inf` | `+inf` | FAIL: F=+inf exceeds contour lower bound | **NOT** | none |
| g5_pin_7 | `+inf` | `+inf` | FAIL: F=+inf exceeds contour lower bound | **NOT** | none |
| g5_pin_8 | `+inf` | `+inf` | FAIL: F=+inf exceeds contour lower bound | **NOT** | none |

`W*=+inf` is the certified result for the quantity specified in TB_LEMMA_CHAIN.md L3: the maximum of per-source row sums of absolute block-weight suprema. Therefore `F=+inf`, the margin is negative infinite, and no finite N can certify the requested inequality.

## Methodology

- Backend: `python-flint Arb/Acb ball arithmetic`, precision `384` bits, arc cover `M=512`.
- The allowed blocks are parsed from the literal `BLOCKS` assignment; the receipt records its path, line, and all 11 entries.
- Each source contour is enclosed by 512 closed circular-arc Acb rectangles. The principal power is evaluated as `theta_prime ** s_ball`, where `s_ball` is the complete closed 1e-6 by 1e-6 Acb box.
- Tail families certify `n=n0..n0+15` individually. For `n>=n0+16`, the monotone majorant uses `d_n^(-p)` with `p=2*Re(s)_lower` and the requested first-term-plus-integral bound.
- For `p<=1`, the integral is divergent. At a real point on the source contour and at the box center, the receipt proves `|u_n| >= C^(-p_center)n^(-p_center)` with `p_center<1`; hence the absolute tail sum itself diverges.
- `rho*=0.697802`, `kappa=3`, and `N=48` are evaluated exactly as specified by TB_LEMMA_CHAIN.md L3. The TC_PREP comparison lower bound is its reported `3.939054358191304e-06`.

## Cross-check against the observed envelope

The observed finite coefficient envelope was `34.91457640966942`. The largest finite head-only weight interval is `[1662.83098260307214181889 +/- 2.41e-21]` at `g5_pin_8 / 3→1, +1, head`, a ratio of `[47.6256954428511780480853 +/- 1.01e-22]`. This is explicitly flagged as above the observed envelope. The requested absolute tail aggregation is `+inf`, so it exceeds the observed envelope by an unbounded amount; neither result is accepted as a certified replacement for `C_supported`.

## Per-block / per-radius detail

Each row below is one of the 11 allowed blocks at its source disc's radius from the three-radius vector (3.14, 2.27, 1.70) for one certification box. All per-n head intervals, worst arc indices, s-ball records, and deep-tail integral/witness fields are in the receipt.

| box | source radius multiplier | block | head terms | head sum upper bound | deep-tail result | W_B result |
|---|---:|---|---:|---:|---|---|
| g5_pin_1 | [3.14000000000000000000000 +/- 1e-28] | 1→2, +2, head | 1 | `[1.75421481685350033415071 +/- 1.01e-24]` | n/a | `[1.75421481685350033415071 +/- 1.01e-24]` |
| g5_pin_1 | [3.14000000000000000000000 +/- 1e-28] | 1→3, +3, tail | 16 | `[2.56920168603651225223860 +/- 4.93e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_1 | [3.14000000000000000000000 +/- 1e-28] | 1→2, −1, head | 1 | `[2.11004839616231663420603 +/- 2.44e-25]` | n/a | `[2.11004839616231663420603 +/- 2.44e-25]` |
| g5_pin_1 | [3.14000000000000000000000 +/- 1e-28] | 1→3, −2, tail | 16 | `[2.67346580172775891175091 +/- 1.26e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_1 | [2.27000000000000000000000 +/- 3e-28] | 2→3, +2, tail | 16 | `[3.56381440935278920094344 +/- 2.85e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_1 | [2.27000000000000000000000 +/- 3e-28] | 2→2, −1, head | 1 | `[2.25927312315387154059608 +/- 2.86e-25]` | n/a | `[2.25927312315387154059608 +/- 2.86e-25]` |
| g5_pin_1 | [2.27000000000000000000000 +/- 3e-28] | 2→3, −2, tail | 16 | `[2.65853280204350087075082 +/- 3.17e-25]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_1 | [1.70000000000000000000000 +/- 1e-28] | 3→1, +1, head | 1 | `[11.1615775031999819404088 +/- 7.16e-24]` | n/a | `[11.1615775031999819404088 +/- 7.16e-24]` |
| g5_pin_1 | [1.70000000000000000000000 +/- 1e-28] | 3→3, +2, tail | 16 | `[3.63011259519010540039112 +/- 6.52e-26]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_1 | [1.70000000000000000000000 +/- 1e-28] | 3→2, −1, head | 1 | `[4.93533816672268211016973 +/- 1.07e-24]` | n/a | `[4.93533816672268211016973 +/- 1.07e-24]` |
| g5_pin_1 | [1.70000000000000000000000 +/- 1e-28] | 3→3, −2, tail | 16 | `[3.19387035155401427269437 +/- 2.48e-25]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_2 | [3.14000000000000000000000 +/- 1e-28] | 1→2, +2, head | 1 | `[3.09724567217772344697545 +/- 2.43e-24]` | n/a | `[3.09724567217772344697545 +/- 2.43e-24]` |
| g5_pin_2 | [3.14000000000000000000000 +/- 1e-28] | 1→3, +3, tail | 16 | `[3.66684890014715182382726 +/- 4.81e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_2 | [3.14000000000000000000000 +/- 1e-28] | 1→2, −1, head | 1 | `[3.89402245924582911037882 +/- 4.45e-24]` | n/a | `[3.89402245924582911037882 +/- 4.45e-24]` |
| g5_pin_2 | [3.14000000000000000000000 +/- 1e-28] | 1→3, −2, tail | 16 | `[3.84250601843292161159996 +/- 2.92e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_2 | [2.27000000000000000000000 +/- 3e-28] | 2→3, +2, tail | 16 | `[5.26724744275755303429317 +/- 1.14e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_2 | [2.27000000000000000000000 +/- 3e-28] | 2→2, −1, head | 1 | `[4.07593860010577234617668 +/- 4.27e-24]` | n/a | `[4.07593860010577234617668 +/- 4.27e-24]` |
| g5_pin_2 | [2.27000000000000000000000 +/- 3e-28] | 2→3, −2, tail | 16 | `[3.75719952740454076918817 +/- 2.21e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_2 | [1.70000000000000000000000 +/- 1e-28] | 3→1, +1, head | 1 | `[29.7372015571592548863065 +/- 7.24e-24]` | n/a | `[29.7372015571592548863065 +/- 7.24e-24]` |
| g5_pin_2 | [1.70000000000000000000000 +/- 1e-28] | 3→3, +2, tail | 16 | `[5.54890590283207063740708 +/- 4.37e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_2 | [1.70000000000000000000000 +/- 1e-28] | 3→2, −1, head | 1 | `[11.0202711760493928274923 +/- 4.63e-24]` | n/a | `[11.0202711760493928274923 +/- 4.63e-24]` |
| g5_pin_2 | [1.70000000000000000000000 +/- 1e-28] | 3→3, −2, tail | 16 | `[4.77376242898886291186650 +/- 1.55e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_3 | [3.14000000000000000000000 +/- 1e-28] | 1→2, +2, head | 1 | `[8.03714779536809052311782 +/- 1.85e-24]` | n/a | `[8.03714779536809052311782 +/- 1.85e-24]` |
| g5_pin_3 | [3.14000000000000000000000 +/- 1e-28] | 1→3, +3, tail | 16 | `[5.34759526612771424392605 +/- 3.08e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_3 | [3.14000000000000000000000 +/- 1e-28] | 1→2, −1, head | 1 | `[10.8345598891361623587709 +/- 4.20e-23]` | n/a | `[10.8345598891361623587709 +/- 4.20e-23]` |
| g5_pin_3 | [3.14000000000000000000000 +/- 1e-28] | 1→3, −2, tail | 16 | `[5.72417540184523098652784 +/- 2.36e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_3 | [2.27000000000000000000000 +/- 3e-28] | 2→3, +2, tail | 16 | `[8.95454603639188786120205 +/- 8.85e-25]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_3 | [2.27000000000000000000000 +/- 3e-28] | 2→2, −1, head | 1 | `[10.9164096909350875401664 +/- 4.89e-23]` | n/a | `[10.9164096909350875401664 +/- 4.89e-23]` |
| g5_pin_3 | [2.27000000000000000000000 +/- 3e-28] | 2→3, −2, tail | 16 | `[5.45730615423201732494936 +/- 4.69e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_3 | [1.70000000000000000000000 +/- 1e-28] | 3→1, +1, head | 1 | `[179.438323720226092994515 +/- 4.44e-23]` | n/a | `[179.438323720226092994515 +/- 4.44e-23]` |
| g5_pin_3 | [1.70000000000000000000000 +/- 1e-28] | 3→3, +2, tail | 16 | `[10.0544177676177877253222 +/- 4.09e-23]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_3 | [1.70000000000000000000000 +/- 1e-28] | 3→2, −1, head | 1 | `[45.8419204473474566481245 +/- 2.89e-23]` | n/a | `[45.8419204473474566481245 +/- 2.89e-23]` |
| g5_pin_3 | [1.70000000000000000000000 +/- 1e-28] | 3→3, −2, tail | 16 | `[7.94111191664718880548844 +/- 4.87e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_4 | [3.14000000000000000000000 +/- 1e-28] | 1→2, +2, head | 1 | `[8.05836624114597280112288 +/- 1.40e-24]` | n/a | `[8.05836624114597280112288 +/- 1.40e-24]` |
| g5_pin_4 | [3.14000000000000000000000 +/- 1e-28] | 1→3, +3, tail | 16 | `[4.59325975405138279941294 +/- 7.92e-25]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_4 | [3.14000000000000000000000 +/- 1e-28] | 1→2, −1, head | 1 | `[11.0358876851947068709574 +/- 1.71e-24]` | n/a | `[11.0358876851947068709574 +/- 1.71e-24]` |
| g5_pin_4 | [3.14000000000000000000000 +/- 1e-28] | 1→3, −2, tail | 16 | `[4.93161016531141317433750 +/- 2.40e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_4 | [2.27000000000000000000000 +/- 3e-28] | 2→3, +2, tail | 16 | `[8.25941098319627615904505 +/- 4.32e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_4 | [2.27000000000000000000000 +/- 3e-28] | 2→2, −1, head | 1 | `[11.5358781725013992669944 +/- 3.60e-23]` | n/a | `[11.5358781725013992669944 +/- 3.60e-23]` |
| g5_pin_4 | [2.27000000000000000000000 +/- 3e-28] | 2→3, −2, tail | 16 | `[4.70782828714438323438537 +/- 1.49e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_4 | [1.70000000000000000000000 +/- 1e-28] | 3→1, +1, head | 1 | `[208.373552792926519676960 +/- 2.27e-22]` | n/a | `[208.373552792926519676960 +/- 2.27e-22]` |
| g5_pin_4 | [1.70000000000000000000000 +/- 1e-28] | 3→3, +2, tail | 16 | `[9.16624837319345204896932 +/- 3.44e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_4 | [1.70000000000000000000000 +/- 1e-28] | 3→2, −1, head | 1 | `[50.0000087526829045848198 +/- 3.95e-23]` | n/a | `[50.0000087526829045848198 +/- 3.95e-23]` |
| g5_pin_4 | [1.70000000000000000000000 +/- 1e-28] | 3→3, −2, tail | 16 | `[7.09959083667892757106230 +/- 4.22e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_5 | [3.14000000000000000000000 +/- 1e-28] | 1→2, +2, head | 1 | `[9.15521966947815297056675 +/- 1.31e-25]` | n/a | `[9.15521966947815297056675 +/- 1.31e-25]` |
| g5_pin_5 | [3.14000000000000000000000 +/- 1e-28] | 1→3, +3, tail | 16 | `[4.49874969791393478316031 +/- 2.74e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_5 | [3.14000000000000000000000 +/- 1e-28] | 1→2, −1, head | 1 | `[12.9317267289949454599195 +/- 4.92e-23]` | n/a | `[12.9317267289949454599195 +/- 4.92e-23]` |
| g5_pin_5 | [3.14000000000000000000000 +/- 1e-28] | 1→3, −2, tail | 16 | `[4.87319880269845514618068 +/- 1.31e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_5 | [2.27000000000000000000000 +/- 3e-28] | 2→3, +2, tail | 16 | `[8.55934727566305027893403 +/- 4.95e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_5 | [2.27000000000000000000000 +/- 3e-28] | 2→2, −1, head | 1 | `[13.1887452496366345317915 +/- 1.17e-23]` | n/a | `[13.1887452496366345317915 +/- 1.17e-23]` |
| g5_pin_5 | [2.27000000000000000000000 +/- 3e-28] | 2→3, −2, tail | 16 | `[4.63643587642602215820866 +/- 3.74e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_5 | [1.70000000000000000000000 +/- 1e-28] | 3→1, +1, head | 1 | `[292.646824484313401732556 +/- 3.73e-22]` | n/a | `[292.646824484313401732556 +/- 3.73e-22]` |
| g5_pin_5 | [1.70000000000000000000000 +/- 1e-28] | 3→3, +2, tail | 16 | `[9.58544117807509475406725 +/- 1.44e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_5 | [1.70000000000000000000000 +/- 1e-28] | 3→2, −1, head | 1 | `[63.7606274882055993183650 +/- 1.28e-23]` | n/a | `[63.7606274882055993183650 +/- 1.28e-23]` |
| g5_pin_5 | [1.70000000000000000000000 +/- 1e-28] | 3→3, −2, tail | 16 | `[7.23565603955110422153369 +/- 1.59e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_6 | [3.14000000000000000000000 +/- 1e-28] | 1→2, +2, head | 1 | `[10.7825761458742278084960 +/- 6.81e-24]` | n/a | `[10.7825761458742278084960 +/- 6.81e-24]` |
| g5_pin_6 | [3.14000000000000000000000 +/- 1e-28] | 1→3, +3, tail | 16 | `[4.56856176309361067162945 +/- 2.95e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_6 | [3.14000000000000000000000 +/- 1e-28] | 1→2, −1, head | 1 | `[15.4471284418267118355828 +/- 3.10e-23]` | n/a | `[15.4471284418267118355828 +/- 3.10e-23]` |
| g5_pin_6 | [3.14000000000000000000000 +/- 1e-28] | 1→3, −2, tail | 16 | `[4.97521473349044969172016 +/- 2.87e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_6 | [2.27000000000000000000000 +/- 3e-28] | 2→3, +2, tail | 16 | `[9.19829986151716629788532 +/- 1.57e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_6 | [2.27000000000000000000000 +/- 3e-28] | 2→2, −1, head | 1 | `[15.8565588749284353173635 +/- 4.03e-23]` | n/a | `[15.8565588749284353173635 +/- 4.03e-23]` |
| g5_pin_6 | [2.27000000000000000000000 +/- 3e-28] | 2→3, −2, tail | 16 | `[4.69920043748437923338814 +/- 3.36e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_6 | [1.70000000000000000000000 +/- 1e-28] | 3→1, +1, head | 1 | `[418.214560873053757925653 +/- 3.95e-22]` | n/a | `[418.214560873053757925653 +/- 3.95e-22]` |
| g5_pin_6 | [1.70000000000000000000000 +/- 1e-28] | 3→3, +2, tail | 16 | `[10.4473942528999837197143 +/- 5.00e-23]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_6 | [1.70000000000000000000000 +/- 1e-28] | 3→2, −1, head | 1 | `[81.9383631680676163298513 +/- 3.84e-24]` | n/a | `[81.9383631680676163298513 +/- 3.84e-24]` |
| g5_pin_6 | [1.70000000000000000000000 +/- 1e-28] | 3→3, −2, tail | 16 | `[7.66980716250207998865353 +/- 3.88e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_7 | [3.14000000000000000000000 +/- 1e-28] | 1→2, +2, head | 1 | `[18.5615580064063473409816 +/- 3.70e-23]` | n/a | `[18.5615580064063473409816 +/- 3.70e-23]` |
| g5_pin_7 | [3.14000000000000000000000 +/- 1e-28] | 1→3, +3, tail | 16 | `[7.43885099588598957839599 +/- 2.24e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_7 | [3.14000000000000000000000 +/- 1e-28] | 1→2, −1, head | 1 | `[26.5657884486983316913064 +/- 4.56e-23]` | n/a | `[26.5657884486983316913064 +/- 4.56e-23]` |
| g5_pin_7 | [3.14000000000000000000000 +/- 1e-28] | 1→3, −2, tail | 16 | `[8.09076599878669751180947 +/- 9.80e-25]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_7 | [2.27000000000000000000000 +/- 3e-28] | 2→3, +2, tail | 16 | `[14.8578154074991990652547 +/- 2.33e-23]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_7 | [2.27000000000000000000000 +/- 3e-28] | 2→2, −1, head | 1 | `[27.0849011772202826715756 +/- 3.19e-23]` | n/a | `[27.0849011772202826715756 +/- 3.19e-23]` |
| g5_pin_7 | [2.27000000000000000000000 +/- 3e-28] | 2→3, −2, tail | 16 | `[7.53692117555989444642459 +/- 3.47e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_7 | [1.70000000000000000000000 +/- 1e-28] | 3→1, +1, head | 1 | `[920.508674196419264597843 +/- 1.74e-22]` | n/a | `[920.508674196419264597843 +/- 1.74e-22]` |
| g5_pin_7 | [1.70000000000000000000000 +/- 1e-28] | 3→3, +2, tail | 16 | `[17.6272322241000408749346 +/- 3.11e-23]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_7 | [1.70000000000000000000000 +/- 1e-28] | 3→2, −1, head | 1 | `[160.952904799734926160396 +/- 3.65e-22]` | n/a | `[160.952904799734926160396 +/- 3.65e-22]` |
| g5_pin_7 | [1.70000000000000000000000 +/- 1e-28] | 3→3, −2, tail | 16 | `[12.7633328863402695248860 +/- 4.27e-23]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_8 | [3.14000000000000000000000 +/- 1e-28] | 1→2, +2, head | 1 | `[23.5925208534035266735620 +/- 4.49e-23]` | n/a | `[23.5925208534035266735620 +/- 4.49e-23]` |
| g5_pin_8 | [3.14000000000000000000000 +/- 1e-28] | 1→3, +3, tail | 16 | `[7.16658576565367567717198 +/- 3.88e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_8 | [3.14000000000000000000000 +/- 1e-28] | 1→2, −1, head | 1 | `[35.4560869119395374018553 +/- 2.71e-23]` | n/a | `[35.4560869119395374018553 +/- 2.71e-23]` |
| g5_pin_8 | [3.14000000000000000000000 +/- 1e-28] | 1→3, −2, tail | 16 | `[7.91213461002245905732984 +/- 4.07e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_8 | [2.27000000000000000000000 +/- 3e-28] | 2→3, +2, tail | 16 | `[16.0685558738663439714224 +/- 2.09e-23]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_8 | [2.27000000000000000000000 +/- 3e-28] | 2→2, −1, head | 1 | `[35.9491549187827264049682 +/- 2.90e-23]` | n/a | `[35.9491549187827264049682 +/- 2.90e-23]` |
| g5_pin_8 | [2.27000000000000000000000 +/- 3e-28] | 2→3, −2, tail | 16 | `[7.31983791279325665114155 +/- 3.83e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_8 | [1.70000000000000000000000 +/- 1e-28] | 3→1, +1, head | 1 | `[1662.83098260307214181889 +/- 2.40e-21]` | n/a | `[1662.83098260307214181889 +/- 2.40e-21]` |
| g5_pin_8 | [1.70000000000000000000000 +/- 1e-28] | 3→3, +2, tail | 16 | `[19.5492914953632376205542 +/- 3.82e-23]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |
| g5_pin_8 | [1.70000000000000000000000 +/- 1e-28] | 3→2, −1, head | 1 | `[249.682717693276146819557 +/- 3.92e-22]` | n/a | `[249.682717693276146819557 +/- 3.92e-22]` |
| g5_pin_8 | [1.70000000000000000000000 +/- 1e-28] | 3→3, −2, tail | 16 | `[13.4271453968063079105968 +/- 4.39e-24]` | DIVERGENT_ABSOLUTE_INTEGRAL (+inf) | `+inf` |

## Reproducibility

Machine-readable receipt: [W_ENVELOPE_CERT_RECEIPT.json](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/W_ENVELOPE_CERT_RECEIPT.json).

Run command:

```bash
/Users/za/.venvs/farey-rh/bin/python /Users/za/Documents/farey-hecke/code/tb_certify/certify_tb_weights.py \
  --sweep-source /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_sweep.py \
  --pins-source /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/out/resonance_geometry.json \
  --out-dir /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g --precision-bits 384 --M 512 --N 48
```

No T-c per-pin contour receipt was present at the time of this run; the comparison uses the TC_PREP lower bound only. The runner can be repeated with a later T-c receipt after that concurrent job publishes it.
