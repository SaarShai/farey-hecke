# T-b certified weight envelope — iteration 2

## VERDICT SUMMARY

The repaired L3′ weight envelope is finite under the prescribed k=1 image-radius tail majorant. The single frozen second-pin box is evaluated with a complete closed 1e-6 Acb s-box; `W^(0)` is reported only as a conditioning sanity value and is not used in `F`.

| box | W^(≥1) entering F | W^(0) sanity | F at N=48 | contour lower bound | margin | VERDICT | minimal certifying N |
|---|---:|---:|---:|---:|---:|---|---:|
| g5_pin_s2 | `[44.6658811851825879737774 +/- 9.40e-23]` | `[45.9375141993582343954994 +/- 7.28e-23]` | `[1.41515213333341829837719e+188 +/- 1.33e+167]` | `[3.93905435819130400000000e-6 +/- 1e-34]` | `[-1.41515213333341829837719e+188 +/- 1.33e+167]` | **NOT** | 1287 |

The verdict is `PASS` only when the certified lower endpoint of `contour lower bound − F` is positive. `W^(0)` does not enter the displayed `F` calculation.

## Method

- Backend: `python-flint Arb/Acb ball arithmetic`, precision `384` bits, closed-arc cover `M=512`.
- The 11 allowed blocks and every finite tail head ratio are read from `TB_BLOCK_CERTIFICATES_V2_RECEIPT.json`; no tail branch is re-summed term by term.
- For each tail family, the deep image factor is `|theta_n|/R_j ≤ 1/(R_j*d_n)` and the weight majorant is `A*d_n^(-p)`, so the product integral has exponent `1+p`, `p=2*sigma_lower`.
- `W^(0)` is the direct `k=0` Hurwitz-closed value `((lambda^2)^(-s))*zeta(2s, n0 ± z/lambda)` on the same Acb contour cover, routed through `zeta_cert_rosen_q5.hurwitz_series_in_a(..., Nser=1)`.
- `F(W^(≥1), rho*=0.697802, N) = exp(1 + 3W/(1-rho*)) * 3W*rho*^N/(1-rho*)`; `N=48` is the requested evaluation.

## Per-box aggregation

| box | source row | W^(≥1) row sum | W^(0) row sum |
|---|---:|---:|---:|
| g5_pin_s2 | 1 | `[9.36307350563266641663437 +/- 9.58e-24]` | `[9.39265055602668145735889 +/- 6.80e-24]` |
| g5_pin_s2 | 2 | `[7.69406908291246389286936 +/- 1.35e-23]` | `[8.22028666550757779837900 +/- 8.26e-24]` |
| g5_pin_s2 | 3 | `[44.6658811851825879737774 +/- 9.39e-23]` | `[45.9375141993582343954994 +/- 7.27e-23]` |

## Tail-family records

The receipt contains every V2 head term, weight sup, product, deep first term, integral, and closed `Phi_0` sup. The compact table below gives the block-level constants.

| box | block | head weighted sum | deep k=1 tail | W^(≥1) block | W^(0) block |
|---|---|---:|---:|---:|---:|
| g5_pin_s2 | 1→2, +2, head | `[1.68414471505544726083819 +/- 4.19e-24]` | n/a | `[3.09724567217760575743782 +/- 4.94e-24]` | `[3.09724567217760575743782 +/- 4.94e-24]` |
| g5_pin_s2 | 1→3, +3, tail | `[0.955332679609391790871109 +/- 2.16e-24]` | `[0.185363926647689104703081 +/- 1.81e-25]` (p+1=[1.82108547098946337865987 +/- 9.59e-25]) | `[1.14069660625708089557419 +/- 1.89e-24]` | `[1.10957169722816775986844 +/- 1.27e-24]` |
| g5_pin_s2 | 1→2, −1, head | `[1.74369563816595824418180 +/- 4.74e-24]` | n/a | `[3.89402245924575034952126 +/- 1.97e-26]` | `[3.89402245924575034952126 +/- 1.97e-26]` |
| g5_pin_s2 | 1→3, −2, tail | `[1.05494365278433298586977 +/- 2.10e-24]` | `[0.176165115167896428231331 +/- 3.46e-25]` (p+1=[1.82108547098946337865987 +/- 9.59e-25]) | `[1.23110876795222941410110 +/- 2.72e-24]` | `[1.29181072737515759053137 +/- 5.66e-25]` |
| g5_pin_s2 | 2→3, +2, tail | `[2.20872148746426669951386 +/- 9.25e-24]` | `[0.180504148295506556041489 +/- 4.93e-25]` (p+1=[1.82108547098946337865987 +/- 9.59e-25]) | `[2.38922563575977325555536 +/- 5.01e-24]` | `[2.80124791530026319992192 +/- 1.69e-24]` |
| g5_pin_s2 | 2→2, −1, head | `[1.23064669015359019833262 +/- 4.89e-24]` | n/a | `[4.07593860010572025194351 +/- 4.28e-24]` | `[4.07593860010572025194351 +/- 4.28e-24]` |
| g5_pin_s2 | 2→3, −2, tail | `[1.05461181527156707448344 +/- 5.03e-24]` | `[0.174293031775403310887050 +/- 3.71e-25]` (p+1=[1.82108547098946337865987 +/- 9.59e-25]) | `[1.22890484704697038537049 +/- 4.20e-24]` | `[1.34310015010159434651357 +/- 2.28e-24]` |
| g5_pin_s2 | 3→1, +1, head | `[19.2217774677273737238992 +/- 2.28e-23]` | n/a | `[29.7372015571584358962280 +/- 3.01e-24]` | `[29.7372015571584358962280 +/- 3.01e-24]` |
| g5_pin_s2 | 3→3, +2, tail | `[2.05967775082085849248549 +/- 4.31e-24]` | `[0.184526756299304214377937 +/- 1.57e-25]` (p+1=[1.82108547098946337865987 +/- 9.59e-25]) | `[2.24420450712016270686343 +/- 5.91e-24]` | `[2.99158901481462586982113 +/- 4.87e-24]` |
| g5_pin_s2 | 3→2, −1, head | `[7.14517746719785525182936 +/- 9.89e-24]` | n/a | `[11.0202711760496735389470 +/- 5.00e-23]` | `[11.0202711760496735389470 +/- 5.00e-23]` |
| g5_pin_s2 | 3→3, −2, tail | `[1.48220853557379585410888 +/- 4.10e-24]` | `[0.181995409280519977630122 +/- 1.92e-25]` (p+1=[1.82108547098946337865987 +/- 9.59e-25]) | `[1.66420394485431583173900 +/- 4.93e-24]` | `[2.18845245133549909050326 +/- 4.78e-24]` |

## Reproducibility

Receipt: [W_ENVELOPE_CERT_S2_RECEIPT.json](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/second_pin/W_ENVELOPE_CERT_S2_RECEIPT.json).

```bash
/Users/za/.venvs/farey-rh/bin/python /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/second_pin/certify_w_second_pin.py \
  --blocks-receipt /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json \
  --sweep-source /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_sweep.py \
  --pins-source /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/S2_SECOND_WINDING_BOX_SOL.md \
  --tc-dir /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun \
  --out-dir /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/second_pin --precision-bits 384 --M 512 --N 48
```

T-c source status: `per_pin_output`. The run used the per-pin output when available; this receipt records whether the fallback `3.939054358191304e-06` was required.
