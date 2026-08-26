# T-b certified weight envelope — iteration 2

## VERDICT SUMMARY

The repaired L3′ weight envelope is finite under the prescribed k=1 image-radius tail majorant. The single frozen second-pin box is evaluated with a complete closed 1e-6 Acb s-box; `W^(0)` is reported only as a conditioning sanity value and is not used in `F`.

| box | W^(≥1) entering F | W^(0) sanity | F at N=48 | contour lower bound | margin | VERDICT | minimal certifying N |
|---|---:|---:|---:|---:|---:|---|---:|
| g5_pin_s3 | `[232.202534303779445519856 +/- 3.77e-22]` | `[231.298043266853013382345 +/- 4.81e-22]` | `[2.53597999827675389830628e+997 +/- 9.50e+976]` | `[3.93905435819130400000000e-6 +/- 1e-34]` | `[-2.53597999827675389830628e+997 +/- 9.50e+976]` | **NOT** | 6466 |

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
| g5_pin_s3 | 1 | `[22.1356560477097983673000 +/- 5.37e-23]` | `[24.0269090321622253716086 +/- 8.78e-23]` |
| g5_pin_s3 | 2 | `[16.9184146985859292952888 +/- 5.94e-23]` | `[18.3742050271159982176587 +/- 8.68e-23]` |
| g5_pin_s3 | 3 | `[232.202534303779445519856 +/- 3.76e-22]` | `[231.298043266853013382345 +/- 4.80e-22]` |

## Tail-family records

The receipt contains every V2 head term, weight sup, product, deep first term, integral, and closed `Phi_0` sup. The compact table below gives the block-level constants.

| box | block | head weighted sum | deep k=1 tail | W^(≥1) block | W^(0) block |
|---|---|---:|---:|---:|---:|
| g5_pin_s3 | 1→2, +2, head | `[4.37024421578157860453479 +/- 5.94e-24]` | n/a | `[8.03714779536809052311782 +/- 1.85e-24]` | `[8.03714779536809052311782 +/- 1.85e-24]` |
| g5_pin_s3 | 1→3, +3, tail | `[1.32871085376218296408397 +/- 5.04e-24]` | `[0.221666623310580112757219 +/- 3.62e-25]` (p+1=[1.79963978589996203865987 +/- 9.59e-25]) | `[1.55037747707276307684119 +/- 5.98e-24]` | `[2.57008466604834045427399 +/- 1.87e-24]` |
| g5_pin_s3 | 1→2, −1, head | `[4.85158342507194463674487 +/- 5.73e-24]` | n/a | `[10.8345598891361623587709 +/- 4.20e-23]` | `[10.8345598891361623587709 +/- 4.20e-23]` |
| g5_pin_s3 | 1→3, −2, tail | `[1.50350327981727392206602 +/- 3.96e-24]` | `[0.210067606315508486504070 +/- 3.39e-25]` (p+1=[1.79963978589996203865987 +/- 9.59e-25]) | `[1.71357088613278240857009 +/- 3.83e-24]` | `[2.58511668160963203544593 +/- 2.06e-24]` |
| g5_pin_s3 | 2→3, +2, tail | `[4.09265642731134044964433 +/- 7.54e-24]` | `[0.213885730084543301242731 +/- 5.65e-25]` (p+1=[1.79963978589996203865987 +/- 9.59e-25]) | `[4.30654215739588375088707 +/- 7.17e-24]` | `[5.42099919256891283848661 +/- 3.74e-24]` |
| g5_pin_s3 | 2→2, −1, head | `[3.29598769082571296991574 +/- 9.35e-24]` | n/a | `[10.9164096909350875401664 +/- 4.89e-23]` | `[10.9164096909350875401664 +/- 4.89e-23]` |
| g5_pin_s3 | 2→3, −2, tail | `[1.48928634923415156011072 +/- 3.66e-24]` | `[0.206176501020806444124606 +/- 2.06e-25]` (p+1=[1.79963978589996203865987 +/- 9.59e-25]) | `[1.69546285025495800423533 +/- 3.24e-24]` | `[2.03679614361199783900566 +/- 4.09e-24]` |
| g5_pin_s3 | 3→1, +1, head | `[115.986822805185177632962 +/- 1.46e-22]` | n/a | `[179.438323720226092994515 +/- 4.44e-23]` | `[179.438323720226092994515 +/- 4.44e-23]` |
| g5_pin_s3 | 3→3, +2, tail | `[3.98889166301234167175105 +/- 1.12e-23]` | `[0.221914008782907583755349 +/- 5.81e-25]` (p+1=[1.79963978589996203865987 +/- 9.59e-25]) | `[4.21080567179524925550639 +/- 6.00e-24]` | `[3.79565459528721082319677 +/- 2.44e-24]` |
| g5_pin_s3 | 3→2, −1, head | `[29.7223772265535815172060 +/- 6.20e-23]` | n/a | `[45.8419204473474566481245 +/- 2.89e-23]` | `[45.8419204473474566481245 +/- 2.89e-23]` |
| g5_pin_s3 | 3→3, −2, tail | `[2.49280077876066583474415 +/- 3.35e-24]` | `[0.218683685649980786966255 +/- 5.44e-25]` (p+1=[1.79963978589996203865987 +/- 9.59e-25]) | `[2.71148446441064662171040 +/- 6.54e-24]` | `[2.22214450399225291650913 +/- 3.96e-24]` |

## Reproducibility

Receipt: [W_ENVELOPE_CERT_S2_RECEIPT.json](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/third_pin/W_ENVELOPE_CERT_S2_RECEIPT.json).

```bash
/Users/za/.venvs/farey-rh/bin/python /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/third_pin/certify_w_second_pin.py \
  --blocks-receipt /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json \
  --sweep-source /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_sweep.py \
  --pins-source /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/out/resonance_geometry.json \
  --tc-dir /Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun \
  --out-dir /Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/third_pin --precision-bits 384 --M 512 --N 48
```

T-c source status: `per_pin_output`. The run used the per-pin output when available; this receipt records whether the fallback `3.939054358191304e-06` was required.
