# Verdict

q4_pin_1 (q=4): **CERTIFIED** — winding=1; box=[0.249999, 0.250001, 7.067361570867346, 7.067363570867347]; min contour |det| lower bound=3.1495373271206616e-06; N=28; dimension-tail heuristic entered=True.
q4_pin_2 (q=4): **CERTIFIED** — winding=1; box=[0.249936, 0.250064, 10.510955819386503, 10.511083819386503]; min contour |det| lower bound=0.00023736408907463704; N=28; dimension-tail heuristic entered=True.
q4_pin_3 (q=4): **CERTIFIED** — winding=1; box=[0.249999, 0.250001, 12.50542778996472, 12.505429789964719]; min contour |det| lower bound=1.4729342507155297e-05; N=28; dimension-tail heuristic entered=True.
q6_pin_1 (q=6): **CERTIFIED** — winding=1; box=[0.2499995, 0.2500005, 7.0673620708673655, 7.067363070867365]; min contour |det| lower bound=2.9988288729156283e-06; N=28; dimension-tail heuristic entered=True.
q6_pin_2 (q=6): **CERTIFIED** — winding=1; box=[0.249999, 0.250001, 10.511018819425393, 10.511020819425392]; min contour |det| lower bound=1.9762950680324443e-05; N=28; dimension-tail heuristic entered=True.

# q=3 validation gate

Status: **PASS**; pin={'re': 0.25, 'im': 7.067362570867347}; winding=1; wall_seconds=35.49528958299197.
The adapted contour routine reproduced the known q=3 anchor with box=[0.249999, 0.250001, 7.067361570867347, 7.0673635708673475], K=24, N=30, winding ball=[0.9999997463048129, 1.0000002536951853], and minimum contour lower bound=1.8206726961364357e-06.

# Per-pin certificate data

## q4_pin_1 (q=4)

- target: `{'re': 0.25, 'im': 7.067362570867346}`
- status: **CERTIFIED**
- winding count: `1`
- box bounds `[Re_lo, Re_hi, Im_lo, Im_hi]`: `[0.249999, 0.250001, 7.067361570867346, 7.067363570867347]`
- half-widths: `[1e-06, 1e-06]`
- winding ball: `[0.8897964861243963, 1.1116220150142908]`
- minimum certified contour `|det|` lower bound: `3.1495373271206616e-06`
- N used: `28`; K per edge: `24`
- dimension-tail heuristic entered: **True**
- tail fix used: `9.522680587697178e-09`
- runtime: `30.747730291914195` seconds
- source receipt match: `{'matched': True, 'source_re': 0.24999999999999986, 'source_im': 7.067362570867346}`
## q4_pin_2 (q=4)

- target: `{'re': 0.25, 'im': 10.511019819386503}`
- status: **CERTIFIED**
- winding count: `1`
- box bounds `[Re_lo, Re_hi, Im_lo, Im_hi]`: `[0.249936, 0.250064, 10.510955819386503, 10.511083819386503]`
- half-widths: `[6.4e-05, 6.4e-05]`
- winding ball: `[0.5297699887305498, 1.4975150655955076]`
- minimum certified contour `|det|` lower bound: `0.00023736408907463704`
- N used: `28`; K per edge: `24`
- dimension-tail heuristic entered: **True**
- tail fix used: `3.1719887588701162e-06`
- runtime: `933.3903139161412` seconds
- source receipt match: `{'matched': True, 'source_re': 0.2500000000024378, 'source_im': 10.511019819386503}`
## q4_pin_3 (q=4)

- target: `{'re': 0.25, 'im': 12.50542878996472}`
- status: **CERTIFIED**
- winding count: `1`
- box bounds `[Re_lo, Re_hi, Im_lo, Im_hi]`: `[0.249999, 0.250001, 12.50542778996472, 12.505429789964719]`
- half-widths: `[1e-06, 1e-06]`
- winding ball: `[0.755246271379292, 1.2519861767068505]`
- minimum certified contour `|det|` lower bound: `1.4729342507155297e-05`
- N used: `28`; K per edge: `24`
- dimension-tail heuristic entered: **True**
- tail fix used: `1.0092464621147044e-07`
- runtime: `35.345560709014535` seconds
- source receipt match: `{'matched': True, 'source_re': 0.24999999998047526, 'source_im': 12.50542878996472}`
## q6_pin_1 (q=6)

- target: `{'re': 0.25, 'im': 7.067362570867365}`
- status: **CERTIFIED**
- winding count: `1`
- box bounds `[Re_lo, Re_hi, Im_lo, Im_hi]`: `[0.2499995, 0.2500005, 7.0673620708673655, 7.067363070867365]`
- half-widths: `[5e-07, 5e-07]`
- winding ball: `[0.9998549520969391, 1.0001450516283512]`
- minimum certified contour `|det|` lower bound: `2.9988288729156283e-06`
- N used: `28`; K per edge: `24`
- dimension-tail heuristic entered: **True**
- tail fix used: `1.2024345681860621e-11`
- runtime: `108.29729866585694` seconds
- source receipt match: `{'matched': True, 'source_re': 0.25000000000000555, 'source_im': 7.067362570867365}`
## q6_pin_2 (q=6)

- target: `{'re': 0.25, 'im': 10.511019819425393}`
- status: **CERTIFIED**
- winding count: `1`
- box bounds `[Re_lo, Re_hi, Im_lo, Im_hi]`: `[0.249999, 0.250001, 10.511018819425393, 10.511020819425392]`
- half-widths: `[1e-06, 1e-06]`
- winding ball: `[0.9913893286138773, 1.008619213476777]`
- minimum certified contour `|det|` lower bound: `1.9762950680324443e-05`
- N used: `28`; K per edge: `24`
- dimension-tail heuristic entered: **True**
- tail fix used: `4.628596419405895e-09`
- runtime: `100.07524308399297` seconds
- source receipt match: `{'matched': True, 'source_re': 0.24999999997949376, 'source_im': 10.511019819425393}`

# Protocol and limitations

Each contour evaluates the raw finite-N determinant in Arb balls, adds a uniform center+corner dimension-tail radius inflated by x4, then sums certified consecutive argument increments. A winding count of at least one is the reported interior zero-count certificate.
The dimension-tail component is explicitly disclosed as heuristic: it uses the existing det-increment geometric contraction test and the existing x4 center/corner-to-interior inflation. It is not silently presented as an independently proven uniform tail bound.
The q=4/q=6 operator is the existing even-q MMS eq.(32) operator with lambda=sqrt(2) and sqrt(3), respectively, and sign=+1. No source operator file was modified.
