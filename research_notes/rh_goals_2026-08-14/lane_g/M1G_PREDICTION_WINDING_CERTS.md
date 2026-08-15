# M1G predicted-resonance winding certificates

**Verdict: 0/8 rigorously certified.** Four trivial-sector runs produced interval-arithmetic sampled windings equal to 1, but the existing even-q contour routine explicitly uses a heuristic `4 * max(center,corners)` dimension-tail inflation, not the theorem-grade uniform endpoint/tail bound used by R3b. The four chi-sector determinants have no existing winding entry point. No result below is promoted to a rigorous Fredholm-determinant zero certificate.

| point | sector | box | N | winding number | minimum margin (rounded DOWN) | wall time |
|---|---|---|---:|---|---:|---:|
| `i*pi/log(2)` | trivial, `det(1-L_+)` | `Re=[-0.001,0.001]`, `Im=[4.531360141827194,4.5333601418271945]` | 60 | `1` sampled; **FAILED-TO-CERTIFY** | `0.0016990536247013` sampled lower bound; not a proven full-det margin | `152.872254042 s` |
| `3i*pi/log(2)` | trivial, `det(1-L_+)` | `Re=[-0.001,0.001]`, `Im=[13.596080425481581,13.59808042548158]` | 60 | `1` sampled; **FAILED-TO-CERTIFY** | `0.0215748480253992` sampled lower bound; not a proven full-det margin | `158.785455333 s` |
| `2i*pi/log(2)` | chi, `det(1+L_+)` | center `9.064720283654388i`, half-width `0.001` requested | 60 requested | **BLOCKED** | unavailable | `0 s` |
| `4i*pi/log(2)` | chi, `det(1+L_+)` | center `18.129440567308777i`, half-width `0.001` requested | 60 requested | **BLOCKED** | unavailable | `0 s` |
| `i*pi/log(3)` | trivial, `det(1-L_+)` | `Re=[-0.001,0.001]`, `Im=[2.858600867380127,2.8606008673801266]` | 60 | `1` sampled; **FAILED-TO-CERTIFY** | `0.0019615618597260` sampled lower bound; not a proven full-det margin | `1287.826152542 s` |
| `3i*pi/log(3)` | trivial, `det(1-L_+)` | `Re=[-0.001,0.001]`, `Im=[8.577802602140382,8.579802602140381]` | 60 | `1` sampled; **FAILED-TO-CERTIFY** | `0.0213275427876490` sampled lower bound; not a proven full-det margin | `1547.985767792 s` |
| `2i*pi/log(3)` | chi, `det(1+L_+)` | center `5.7192017347602535i`, half-width `0.001` requested | 60 requested | **BLOCKED** | unavailable | `0 s` |
| `4i*pi/log(3)` | chi, `det(1+L_+)` | center `11.438403469520507i`, half-width `0.001` requested | 60 requested | **BLOCKED** | unavailable | `0 s` |

## Parameters and margin audit

- Arithmetic: python-flint Arb/Acb, 400 bits.
- Trivial-sector calls: existing `controls_q4q6.certify_q4q6_winding.contour_winding`, importing unmodified `zeta_cert_rosen_even.py`; `N=60`, `n_head=4`, `K=24` per edge, 96 contour points, `hx=hy=1e-3`, `sign=+1`.
- Pure-imaginary evaluation succeeded: `Re(s)=0` did not trigger a domain error.
- Winding balls: `[0.999896727502346,1.000103274360299]`, `[0.9994978392496705,1.0005021905526519]`, `[0.9999999998777231,1.0000000001222769]`, `[0.9999999997549546,1.0000000002450455]`.
- Added tail radii: `4.811675893631446e-09`, `2.970563523093208e-07`, `6.536241684694031e-15`, `1.4291344112896005e-13`.
- Every displayed lower bound was rounded downward. They remain sampled-contour bounds after a heuristic tail inflation; therefore their positive sign does not prove full-determinant boundary exclusion.
- R3b is hard-bound to the q=5 per-disc builder, q=5 derivative implementation, immutable q=5 R2/T-b receipts, and `I-M`; it cannot evaluate q=4/q=6 or `I+M` unchanged.

## Blockers

1. Existing q4/q6 code records `dimension_tail_heuristic: true`: `det-increment geometric contraction over last dimensions, max(center+corners) x4 for box interior`. This is not a proven uniform boundary enclosure.
2. Exact chi-sector call error: `TypeError: winding_box() got an unexpected keyword argument 'determinant_sector'`. Adding `det(1+L_+)` support would be a new/modified evaluator, forbidden by the task.
3. Other-sector winding-zero checks were not run: the chi-sector winding path is absent and the available path is not theorem-grade.

Per-point receipts: `m1g_receipts/`.
