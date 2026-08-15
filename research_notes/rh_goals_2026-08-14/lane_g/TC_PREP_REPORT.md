# T-c preparation report — 2026-08-14

## Validation gate verdict: PASS

The requested numerical gate was evaluated at
`s = 0.45390 + 5.76354i`, `N=28`, `sign=+1`, `n_head=4`.

| determinant | midpoint value |
|---|---:|
| old uniform radii (`safety=2.5`) | `1.502416589955056e-05 + 1.589912189596303e-05 i` |
| new per-disc radii (`a=(3.14,2.27,1.70)`) | `1.502416589955056e-05 + 1.589912189596303e-05 i` |

Measured relative discrepancy, `abs(new-old)/abs(old)`: **`0.00000000000000000e+00`**.
Both determinants were computed independently from the source builder and the
new parameterized builder in Arb ball arithmetic; the displayed equality is
not an estimate.

## N=48 timing box

One full four-edge box was evaluated at the full-precision flagship center
`s = 0.4538951800749447 + 5.7635372417301305 i`, with half-widths
`(1e-6,1e-6)`, `K=24` points per edge, `N=48`, `sign=+1`, and `n_head=4`.
This was the pure finite-`N` contour: no dimension-tail inflation was applied.

- Contour points: `96`
- Wall time: **`269.89283824991435 s`**
- Minimum Arb contour `|det|` lower bound: **`3.939054358191304e-06`**
- Pure finite-`N` winding result: **`1`**, winding interval `[1.0,1.0]`

## Margin budget

The coefficient scan used the normalized output-row mode `m` and recorded
`max |B[m,k]| / rho^m` over every matrix coefficient and all 96 contour
points. The observed data support:

- `rho = 0.6596888264417232` (the lane-g optimization value, displayed as
  `0.6597`)
- `C_supported = 34.91457640966942`
- `F(N=48) = C*rho^(N+1)/(1-rho) = 1.4412783134630447e-07`
- Finite contour lower bound minus `F`: **`3.7949265268449994e-06`**

Therefore **N=48 suffices for this measured box under the stated F budget**:
the margin remains strictly positive after subtracting the tail radius. Using
the same observed `C` and the measured finite-contour lower bound, the first
integer N for which this scalar margin is positive is `N=41` (`F=2.6507816429059507e-06`,
margin `1.2882727152853534e-06`). This is a budget calculation, not an
additional N=41 contour run.

The reported `C` is the envelope supported by the observed normalized
coefficients; the separate analytic proof of that envelope remains the
load-bearing T-b mathematical obligation.

## File manifest

New source files written under `code/tc_rerun/`:

- `code/tc_rerun/tc_rerun.py` — imports the certified source machinery and
  parameterizes the q=5 matrix builder by independent disc radii; provides
  finite contour, coefficient-envelope, tail-budget, and winding helpers.
- `code/tc_rerun/run_tc.py` — full T-c driver containing all eight G_5 pins and
  the named essential-gap box; exits without computation unless `--go` is
  supplied. The essential-gap box repeats the rightmost pin (`g5_pin_6`), whose
  observed gap is `0.5 - 0.48527431432587564 = 0.01472568567412436`.

Generated validation bytecode also exists under `code/tc_rerun/__pycache__/`:
`tc_rerun.cpython-313.pyc` and `run_tc.cpython-313.pyc`.

The original `code/zeta_cert_rosen_q5.py` and all source receipts were left
unchanged. The full 8-pin T-c run was not launched.
