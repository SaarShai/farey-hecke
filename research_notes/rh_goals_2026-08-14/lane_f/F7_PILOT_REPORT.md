# F7 PILOT REPORT — q=7 pre-Kaggle gate

Date: 2026-08-15. Verdict: **BLOCKED**.

## 1. Staged gate measurements

- Frozen disc factors: `(2.79, 2.39, 1.90, 1.56, 1.35)`.
- Re-measured float `rho* = 0.782263813617748`; report value rounded down:
  **`0.782263813617`**. Worst block: `(2->5, n=2 tail)`. This is
  **NON-RIGOROUS FLOAT PREPARATION**, using 2,048 circle points and tail
  indices through 59. It passes the plan's proposed float re-target
  `rho* < 0.80`, but it is not an Arb TB-block certificate.
- Endpoint finite-column computation at `N=32`, dimension `160`, 384-bit
  Arb/Acb over the entire closed `1e-6` flagship box:
  `B_finite <= 18.074395571390211522643097827116...`.
- Endpoint finite-column computation at provisional `N=224`, dimension
  `1120`, 384-bit Arb/Acb over the entire closed `1e-6` flagship box:
  **`B_finite <= 1145138630.686644864111632891987682...`**.
  Matrix build wall time was `49.43017191695981 s`; build plus column norms
  was `50.04790737503208 s` (`49.72 user-s`, `0.30 sys-s`).

The production endpoint formula adds nonnegative enlarged-output corrections
and the nonnegative R2 input tail to the retained finite-column sum. Therefore
the endpoint value produced by that formula cannot improve this computed
`N=224` bound below the plan's `B approximately 30` stop threshold.

**Gate verdict: BLOCKED.** Per `F7_CERT_PLAN.md` section 3, no R3b contour
work may start when the endpoint phase returns this regime.

## 2. Staged mitigation options (not executed)

Only the options frozen by the prep plan are carried forward:

1. Re-run stage-0 optimization with a deeper grid over the five disc
   inflations to reduce `rho*`.
2. Investigate per-block radii as the other stage-0 lever to reduce `rho*`.

No new disc optimization was improvised. The plan's later contingency order
also lists an `N` re-trade only after valid R2/endpoint measurements; that was
not attempted because the explicit stage-1 stop gate fired.

## 3. CLI and local pilot status

- `--arcs i:j` CLI diff: **NOT IMPLEMENTED — mandatory stage-1 stop**.
- Seam-closure re-verification: **NOT IMPLEMENTED — mandatory stage-1 stop**.
- Local pilot chunk: **NOT RUN — mandatory stage-1 stop**.
- Pilot wall time: **NOT MEASURED (no pilot process was started)**.
- Pilot peak memory: **NOT MEASURED (no pilot process was started)**.
- Extrapolated total CPU-hours from pilot: **NOT COMPUTED**. The prep-plan
  estimate remains approximately `280 CPU-h` at `N=224`; it is not a pilot
  measurement and is not promoted here.

## 4. Frozen provisional chunk table

This is the plan's unchanged 16-way partition of the 192 base arcs. It is
ready for later kernel generation only if a new stage-1 gate passes; no kernel
was generated or started.

| chunk | `--arcs` range |
|---:|:---|
| 0 | `0:12` |
| 1 | `12:24` |
| 2 | `24:36` |
| 3 | `36:48` |
| 4 | `48:60` |
| 5 | `60:72` |
| 6 | `72:84` |
| 7 | `84:96` |
| 8 | `96:108` |
| 9 | `108:120` |
| 10 | `120:132` |
| 11 | `132:144` |
| 12 | `144:156` |
| 13 | `156:168` |
| 14 | `168:180` |
| 15 | `180:192` |

## 5. Measurement method and scope

The endpoint measurements used the existing q-generic certified builder
`.worktrees/aletheia-restore/code/zeta_cert_rosen.py`, `q=7`, `sign=+1`,
`n_head=4`, the frozen five radii, and the full complex flagship coordinate
box. Each retained matrix-column bound was the Arb upper endpoint of its
Euclidean 2-norm; the displayed `B_finite` is their Arb upper-endpoint sum.
This is sufficient for the stop decision because the production endpoint
construction only increases that quantity. It is not a completed R2/R3b
certificate.
