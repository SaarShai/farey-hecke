q=3: LINE
q=4: INSUFFICIENT-DATA
q=6: INSUFFICIENT-DATA
G_5: SCATTER-CONFIRMED
G_7: SCATTER-CONFIRMED
G_8: INSUFFICIENT-DATA

# Family sweep: G_7/G_8 resonance harvest

The verdict lines above are deliberately evidence-gated. `LINE` is the expected
arithmetic outcome for q=3; a non-arithmetic surface with at least four eligible
resonances and a line outcome would falsify the stated law. `INSUFFICIENT-DATA`
means fewer than four independent eligible resonances, not a line result.

All coordinates and raw provenance are in
[`harvest_receipt.json`](./harvest_receipt.json). The statistics below are
computed from the receipt entries marked `included_in_statistics: true`, using
population standard deviation over the listed Re values. They are derived
statistics, not additional harvested measurements.

## Extended law table

| surface | arithmeticity | n | re_mean | re_std | re_min | re_max | verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| q=3 | arithmetic | 8 | 0.24999999999998349 | 6.47516930146045e-14 | 0.24999999999981787 | 0.2500000000000505 | LINE |
| q=4 | arithmetic | 3 | 0.24999999999430433 | 9.829142370588003e-12 | 0.24999999998047526 | 0.2500000000024378 | INSUFFICIENT-DATA |
| q=6 | arithmetic | 2 | 0.24999999998974964 | 1.025589335680139e-11 | 0.24999999997949376 | 0.25000000000000555 | INSUFFICIENT-DATA |
| G_5 | non-arithmetic | 8 | 0.4388239902186848 | 0.029986183641395464 | 0.3998208929499856 | 0.48527431432587564 | SCATTER-CONFIRMED |
| G_7 | non-arithmetic | 12 | 0.39320948136155115 | 0.10292157548329758 | 0.15354628004003862 | 0.4842071839738105 | SCATTER-CONFIRMED |
| G_8 | non-arithmetic | 0 | — | — | — | — | INSUFFICIENT-DATA |

The q=3, q=4, q=6, G5, and G7 rows are the exact values in
`harvest_receipt.json:derived_statistics`; each row is independently recomputed
from the corresponding coordinate entries by the receipt definition. G8 has no
eligible MMS-even coordinate entry, so no Re statistic is computed.

The observed G5 and G7 standard deviations are both well above a single-line
geometry and are consistent with the non-arithmetic scatter prediction. G7 is
therefore scatter-confirmed on twelve independent engine pins. G8 remains an
open test: the inspected G8 artifacts are explicitly MMS- / odd-sector Maass
data on `Re(s)=1/2`, not MMS-even off-line resonances. They cannot be used as
G8 even-sector geometry points.

## Per-coordinate provenance

The coordinate values in this section are copied from receipt entries; IDs are
the trace keys. `engine pin` means the transfer-operator locator output. A
`collocation cross-check` is an independent-method confirmation of an existing
engine resonance and is not counted as a second independent resonance.

### q=3 — eight engine pins

| receipt ID | coordinate `(Re, Im)` | provenance and stated precision |
|---|---|---|
| q3-01 | (0.25, 7.067362570867347) | `.worktrees/aletheia-restore/code/out/resonance_geometry.json`; 2026-08-14; engine pin from `run_resonance_geometry.py`; prec_bits=400, midpoint, `absdet=7.653303790632259e-16`. |
| q3-02 | (0.25, 10.511019819385778) | Same source/date/method; prec_bits=400, midpoint, `absdet=1.2038426631040734e-15`. |
| q3-03 | (0.25, 12.505428790072845) | Same source/date/method; prec_bits=400, midpoint, `absdet=1.5120155405459388e-15`. |
| q3-04 | (0.25, 15.212438062929756) | Same source/date/method; prec_bits=400, midpoint, `absdet=2.889047520713826e-15`. |
| q3-05 | (0.25000000000000044, 16.467530793869596) | Same source/date/method; prec_bits=400, midpoint, `absdet=3.483557711049279e-15`. |
| q3-06 | (0.24999999999999903, 18.79308907941284) | Same source/date/method; prec_bits=400, midpoint, `absdet=1.2425109911044728e-14`. |
| q3-07 | (0.2500000000000505, 20.459359506073667) | Same source/date/method; prec_bits=400, midpoint, `absdet=2.500554041126421e-14`. |
| q3-08 | (0.24999999999981787, 21.663536640457643) | Same source/date/method; prec_bits=400, midpoint, `absdet=5.587396100763513e-15`. |

### G_5 — eight engine pins used as the non-arithmetic baseline

| receipt ID | coordinate `(Re, Im)` | provenance and stated precision |
|---|---|---|
| g5-01 | (0.4538951800749447, 5.7635372417301305) | `.worktrees/aletheia-restore/code/out/resonance_geometry.json`; 2026-08-14; engine pin; prec_bits=400, `absdet=7.52642959668855e-16`, `N_stable=true`. |
| g5-02 | (0.41054373549576567, 7.819768247017059) | Same source/date/method; `absdet=9.96197617104616e-16`, `N_stable=true`. |
| g5-03 | (0.3998208929499856, 11.664755512713677) | Same source/date/method; `absdet=1.7127034611871855e-15`, `N_stable=true`. |
| g5-04 | (0.4470829807186944, 12.07971636884368) | Same source/date/method; `absdet=1.881505175616554e-15`, `N_stable=true`. |
| g5-05 | (0.46905525671927556, 12.785854147380606) | Same source/date/method; `absdet=4.313553426795327e-15`, `N_stable=true`. |
| g5-06 | (0.48527431432587564, 13.565375308892085) | Same source/date/method; `absdet=6.788018889537603e-16`, `N_stable=true`. |
| g5-07 | (0.40043857736632493, 15.14787226409561) | Same source/date/method; `absdet=1.0004806781896385e-15`, `N_stable=true`. |
| g5-08 | (0.4444809840986117, 16.487520683784943) | Same source/date/method; `absdet=9.326997285995118e-15`, `N_stable=true`. |

### q=4 and q=6 — arithmetic controls, below the four-point gate

| receipt ID | surface | coordinate `(Re, Im)` | provenance and stated precision |
|---|---|---|---|
| q4-01 | q=4 | (0.24999999999999986, 7.067362570867346) | Main-repo `Q4Q6_CONTROLS_RECEIPT.json`; 2026-08-14; N=28 engine pin after N=22 to N=28 stability; python-flint Arb midpoint, prec_bits=400, Newton tolerance 1e-12. |
| q4-02 | q=4 | (0.2500000000024378, 10.511019819386503) | Same source/date/method; N_stable=true. |
| q4-03 | q=4 | (0.24999999998047526, 12.50542878996472) | Same source/date/method; N_stable=true. |
| q6-01 | q=6 | (0.25000000000000555, 7.067362570867365) | Same source/date/method; N=28 engine pin after N=22 to N=28 stability; python-flint Arb midpoint, prec_bits=400, Newton tolerance 1e-12. |
| q6-02 | q=6 | (0.24999999997949376, 10.511019819425393) | Same source/date/method; N_stable=true. |

### G_7 — twelve engine pins plus two collocation confirmations

| receipt ID | coordinate `(Re, Im)` | provenance and stated precision |
|---|---|---|
| g7-01 | (0.4751647621098119, 4.668743786424271) | `.worktrees/aletheia-restore/code/out/resonance_g7.json`; 2026-08-14; engine pin from `run_resonance_g7.py`; prec_bits=400, N=22 to N=28 stable. |
| g7-02 | (0.23027023431785223, 6.370837585484903) | Same source/date/method; N_stable=true. |
| g7-03 | (0.4842071839738105, 7.567217676281963) | Same source/date/method; N_stable=true. |
| g7-04 | (0.15354628004003862, 8.183762967591743) | Same source/date/method; N_stable=true. |
| g7-05 | (0.3165025510952286, 9.862846594386172) | Same source/date/method; N_stable=true. |
| g7-06 | (0.39275118293967515, 11.762205068560927) | Same source/date/method; N_stable=true. |
| g7-07 | (0.40306671368607994, 12.679113036017208) | Same source/date/method; N_stable=true. |
| g7-08 | (0.47799136862002667, 12.92934750022359) | Same source/date/method; N_stable=true. |
| g7-09 | (0.4452921422130368, 14.59763251231819) | Same source/date/method; N_stable=true. |
| g7-10 | (0.46956449818341284, 15.252557431682444) | Same source/date/method; N_stable=true. |
| g7-11 | (0.39692542346031345, 16.133908467135072) | Same source/date/method; N_stable=true. |
| g7-12 | (0.47323143569932696, 16.60451004609114) | Same source/date/method; N_stable=true. |
| g7-cross-01 | (0.4842071735606393, 7.567217663577443) | `.worktrees/aletheia-restore/projects/g5-crosscheck/g7_results.json`; 2026-08-14; independent collocation/secant cross-check at M=22; mpmath_dps=15, acceptance gate abs difference <5e-4; duplicate of g7-03 group, not counted. |
| g7-cross-02 | (0.4751647677788035, 4.668743781291972) | Same source/date/method; duplicate of g7-01 group, not counted. |

### G_8 — no eligible even-sector coordinates found

The inspected G8 artifacts do not contain an MMS-even/mms+ off-line resonance
map:

- `code/out/certified_g8.json` labels its operator `mms- (sign=-1)` and calls it
  the populated odd sector for G8.
- `code/out/hejhal_g8_maass.json` is explicitly an ODD (sine) Maass-form
  collocation output and reports on-line data.
- `code/out/zeta_mayer_rosen.json` labels its q=8 zeros `sector=odd` and
  `sign=-1`.

These source checks are recorded in `harvest_receipt.json` under
`excluded_source_checks`; their eligible MMS-even coordinate count is zero.
The recorded G8 values therefore cannot be reclassified as even-sector
resonances or used in the table.

## Gap analysis

### q=4 — INSUFFICIENT-DATA

The table has three independent eligible coordinates. The missing evidence is
at least one additional independent q=4 MMS-even/mms+ resonance coordinate so
that `n >= 4`. Fill it with the locked q=4 control surface plus pinning and
finite-N stability, extending the search in the same declared Im window if the
existing candidates are exhausted. The runtime planning baseline is the recorded
G5 geometry run: 1,585.366377353668 seconds (about 26.4 minutes), from the
receipt's `runtime_references`; this is a baseline, not a measured q=4 forecast.

### q=6 — INSUFFICIENT-DATA

The table has two independent eligible coordinates. The missing evidence is at
least two additional independent q=6 MMS-even/mms+ resonance coordinates for
`n >= 4`. Fill it with the same q=6 control protocol, with the G5 1,585.366377353668
second geometry run as the only requested runtime anchor. Do not promote the
provisional line-like `re_std` to a law verdict until the four-point gate is met.

### G_8 — INSUFFICIENT-DATA

The table has zero eligible MMS-even coordinates because all inspected G8
outputs are MMS- / odd-sector on-line results. The missing evidence is at least
four independent off-line MMS-even/mms+ coordinates, not more odd-sector
collocation anchors. Fill it by running the existing even-q operator engine in
the mms+ (`sign=+1`) sector with a declared Re-Im surface, Newton localization,
and finite-N stability, then retain the first four independent candidates. Use
1,585.366377353668 seconds (about 26.4 minutes) as the G5-scale baseline for a
single geometry run; actual G8 cost is not recorded here and no G8 run was
launched in this harvest.

