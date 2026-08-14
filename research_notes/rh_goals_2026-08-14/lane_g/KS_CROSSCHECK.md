CONFIRMED — the q=5 determinant identity and q=4/q=6 trace-multiplier controls pass; the quoted q=5 ell5 decimal differs from the independently derived value only beyond 15 significant digits.

| test point s | det(1-A_s), N=50 | closed-form product, n=0..200 | relative error | verdict |
|---|---|---|---:|---|
| 0.4 + 5i | 1.17054301031324398568428 + 0.0552169411049145046539757i | 1.17054301031324398568428 + 0.0552169411049145046539757i | 5.257993060790085e-90 | CONFIRMED |
| 0.25 + 7.0674i | 0.754801698771062394599550 - 0.237932842112267242147308i | 0.754801698771062394599550 - 0.237932842112267242147308i | 1.9128506339242947e-89 | CONFIRMED |
| 0.45 + 13i | 0.858674680438141367631145 - 0.0262443094828992872331389i | 0.858674680438141367631145 - 0.0262443094828992872331389i | 1.607706451595521e-89 | CONFIRMED |
| 0.1 + 3.5i | 1.56842991825949451034219 + 0.338518622733375969692627i | 1.56842991825949451034219 + 0.338518622733375969692627i | 8.887100538582349e-90 | CONFIRMED |

These errors are 90-digit mpmath results from the N=50 dense Cauchy matrix. The moderate-Im points are Im(s)=3.5, 5, and 7.0674; the Im(s)=13 point is the high-Im test. Every point is below the 1e-10 target, including the high-Im point.

## Trace and multiplier checks

The claim source is the main-repo copy of [KS_GATE_REPORT.md](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/KS_GATE_REPORT.md:19). The requested worktree copy was absent. The source states the branch definition and weights at lines 20-21, the even/odd component words at lines 23-35, the q=5 reduction at line 37, and the q=5 matrix/trace/ell claim at lines 41-53.

For `M_n=[[0,-1],[1,n lambda_q]]`, the independently multiplied q=5 matrix is

```text
M_2 M_2 M_1 =
[[-3.23606797749978969640917, -4.23606797749978969640917],
 [ 9.47213595499957939281835, 12.0901699437494742410229 ]].
```

Its determinant is 1 and

```text
lambda5                         = 1.61803398874989484820458683
trace(M_2 M_2 M_1)               = 8.85410196624968454461376050
4 + 3*lambda5                   = 8.85410196624968454461376050
attracting fixed point           = -0.353720495719932756780750
ell5                             = 0.114420648029260201895238
attracting multiplier            = 0.0130920846954358465237842
ell5^2                           = 0.0130920846954358465237842
```

The matrix maps the attracting fixed point to itself to residual `6.14e-92`. The derivative from the Mobius formula and the eigenvalue-ratio calculation agree at `0.0130920846954358465237842`. The quoted value `0.11442064802926044` differs from the independent value by `2.381047616323521e-16` (relative difference `2.080959737017595e-15`): it agrees through 15 significant digits, but its displayed final digits are not the correctly rounded continuation of the independently derived constant.

For the even-q controls I read the source component word literally. At q=4, `h=1`, so the cycle is `L_2` and the matrix is `M_2`. At q=6, `h=2`, so the cycle is `L_1,L_2`; cyclic Fredholm determinant equivalence permits the word `L_1 L_2`, whose argument map is represented by `M_2 M_1`.

| q | matrix word | trace | computed ell | attracting multiplier | verdict |
|---:|---|---:|---:|---:|---|
| 4 | `M_2` | 2.82842712474619009760338 = `2*sqrt(2)` | 0.414213562373095048801689 = `sqrt(2)-1` | 0.171572875253809902396623 = ell4^2 | CONFIRMED |
| 5 | `M_2 M_2 M_1` | 8.85410196624968454461376 = `4+3*lambda5` | 0.114420648029260201895238 | 0.0130920846954358465237842 = ell5^2 | CONFIRMED* |
| 6 | `M_2 M_1` | 4 | 0.267949192431122706472554 = `2-sqrt(3)` | 0.0717967697244908258902146 = ell6^2 | CONFIRMED |

Here `ell` is the positive inverse expanding eigenvalue, i.e. the positive square root of the attracting derivative multiplier. This is the convention used by the source claim for ell5 and its q=4/q=6 controls; the actual composition-operator eigenvalue at Taylor level n is `ell^(2s+2n)`.

`*` q=5 is confirmed as an exact trace/multiplier identity and at the requested 15-significant-digit precision, with the quoted decimal-rounding note above.

## Methods and convergence

The fresh checker is [verify_spectral_determinant.py](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/ks_verify/verify_spectral_determinant.py). It derives each `M_n`, finds the attracting fixed point from the quadratic fixed-point equation, and evaluates `A_s=L_{1,s}L_{2,s}L_{2,s}` directly. For each Taylor basis vector `(z-p)^k`, it expands

```text
(theta_1'(z))^s * (theta_2'(theta_1(z)))^s
* (theta_2'(theta_2(theta_1(z))))^s
* (theta_2(theta_2(theta_1(z))) - p)^k
```

by a roots-of-unity Cauchy integral on `|z-p|=0.2`, using 90 decimal digits and eight samples per retained coefficient (at least 256 samples). The full finite matrix `I-A_s`, rather than a pasted diagonal or closed form, is passed to the determinant routine. The product is computed separately from the independently derived ell5 through n=200.

The convergence check used dimensions 30, 40, and 50. Relative changes from N=30 to N=50 were respectively `5.791500203248426e-58`, `1.109787311227249e-57`, `4.6627434021829095e-58`, and `2.126612851485687e-57` in the table's row order. N=40 to N=50 changes were respectively `8.567993686208894e-77`, `1.6418286008686457e-76`, `6.898101463919127e-77`, and `3.146128782715063e-76`. Thus the required moderate-s convergence gate passes by a large margin.

The relative size of the n=200 term divided by the product was `3.79922245681e-378`, `1.07797622504e-377`, `4.17237938846e-378`, and `1.01884940552e-377` in the table's row order, so n=200 is far beyond negligible here.

## Accuracy note

No tested point showed meaningful high-Im degradation at 90-digit precision and the chosen contour. In general, writing `s=sigma+i t` and `log w=u+i v` gives `|exp(s log w)|=exp(sigma*u-t*v)`, while the Cauchy sum also develops more oscillatory cancellation as `|t|` grows. Finite precision, contour proximity to a pole, and a determinant close to zero can therefore amplify truncation/conditioning error at larger Im(s). Those mechanisms are controlled in this run by the separated radius, high precision, and N=30/40/50 agreement; the Im(s)=13 result remains CONFIRMED.

## Overall component verdicts

- q=5 odd-q determinant identity at all four requested points: **CONFIRMED**.
- q=5 trace and attracting multiplier: **CONFIRMED**, with the quoted ell5 decimal corrected after its 15th significant digit.
- q=4 trace/multiplier control: **CONFIRMED**.
- q=6 trace/multiplier control: **CONFIRMED**.
