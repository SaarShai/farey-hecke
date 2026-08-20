# Receipt L-OUT — q=8 omitted-output projection tail on the enlarged contour

**Date** 2026-08-20 · **Lane** lane_g / l_out · **Branch**
`codex/prime-step-review-economic-validation` · **Status** the lane stays
**OPEN**: pass/fail condition 4 is not met as written, so
`full_tail_certified` is **not** flipped.

Everything below is a computation on the pinned q=8 F1024 receipts. The
separately-OPEN **"Exact q=8 MMS-to-Hardy/Hilbert operator, basis and norm
binding"** is *not* claimed, not addressed, and every number here is
conditional on it. E1 on the enlarged disc, `K_s` nonvanishing, the Selberg
determinant/zeta/scattering factorization, the four-edge winding and the
independently-false `recorded_tail_checks_pass` gate are also untouched.

No `lane_f/` file was modified. `git status` at the end of the run reports
`lane_f` clean; `q8_schur_contour.py:395` still reads
`"full_tail_certified": False`. Nothing was committed or pushed.

---

## 0. The spec, restated

From `Q8_OUTPUT_TAIL_REFEREE.md` §3 (verdict **GAPS NOT REFUTED**, line 396),
which corrects `Q8_OUTPUT_TAIL_SOL.md` §5.1 for GAP 4 (wrong envelope family)
and §5.2 for GAP 5 (level slip on "(2.6)").

**What to run.** The `q8_r2_local.py` computation with **one** structural
change: the arc cover on output disc `i` is built at radius `theta_i * r_i`,
while `centers[j-1]` / `radii[j-1]` passed to `exact_tail_columns_on_arc` and
`direct_head_first_moment_sup` stay **unscaled**. Rebuilding geometry by
scaling `factors[i-1]` is rejected. Plus: per block a certified G1 record and a
certified `rho_theta` from the exact Möbius image, `n` swept to at least 400.

**Parameters.** pin `s = 0.4252310423737965 + 4.345760788321986 i`,
half-width `1e-6`; factors `("10","4","2")`; sign 1; `n_head 4`;
`ctx.prec 384`; `M 512`; `K_head 16`; `theta` uniform `1.2` recommended
(`1.2369074008682055` is the rate optimum but sits at `rho_theta = 1` — do NOT
pin it; `1.230` if the extra rate is wanted; per-disc `(1.84, 1.30, 1.23)`
permitted, RECORD which was used); `N` targets `104, 181, 200, 214`.

**Receipt.** `Q8_R2OUT_F1024_THETA_RECEIPT.json`, schema `q8-r2out-local/v1`,
split by family exactly as `q8_r2_local.py` does: `tail == True` emits
`A_theta / C_theta / q / rho_theta / selected_column_bounds_theta`;
`tail == False` (`A2`, `A3` — **including the binding block** `A3`) emits
`weight_theta_sup / rho_theta / selected_column_bounds_theta` and consumes as
`theta^-N * W_theta * G_1(N, rho_theta)` (trace), **not** the
`A q^k + C k rho^{k-1}` form. Plus `theta_exact_string`, unscaled `geometry`,
`holomorphy_gate`, Möbius `rho_theta` provenance, `TB_sha256` / `W_sha256`.

**Seven pass/fail conditions** — §4 below evaluates each one.

**Adverse regression** (referee §3.4, closing paragraph): for the five
assembled blocks and `N in {6, 10, 14}`,
`theta^-N sqrt(sum_{k<N} M_k(theta)^2) >= sqrt(sum_{k<N} sum_{m>=N} |T[m,k]|^2)`
with `T` from the **unmodified** `q8_r3b_engine`.

---

## 1. What was run

New tracked scripts, all under
`research_notes/rh_goals_2026-08-14/lane_g/l_out/` (a NEW directory; no
`lane_f` file was touched, and `q8_r2_local` / `q8_tb_support` /
`q8_weight_support` / `q8_schur_contour` / `q8_r3b_engine` are imported
read-only):

| file | role |
|---|---|
| `q8_r2out_local.py` | receipt generator (the enlarged-contour re-run) |
| `q8_lout_check.py` | independent checker; evaluates conditions 1–7 |
| `q8_lout_adverse.py` | adverse regression vs the unmodified engine |
| `q8_lout_crosscheck_mpmath.py` | non-Arb mpmath cross-check |

Interpreters: `/Users/za/.venvs/farey-rh/bin/python` (python-flint 0.9.0 / Arb,
384 bits) for everything certified; `/Users/za/miniforge3/envs/pari-arb/bin/python3`
(mpmath, 60 dps) for the cross-check only.

**Runtime.** The whole programme is cheap: the production receipt takes
**8.56 s**, each checker pass **~0.1 s**, the adverse regression **6.5 s**.
The `~2 h` contingency in the brief was not needed — **every pass/fail
condition was evaluated at every N target**, and the `N` sweep was extended
well past 214 (to 320) at no cost. Nothing here is a partial run.

### 1.1 Commands, verbatim

```
$ cd research_notes/rh_goals_2026-08-14/lane_g/l_out
$ /Users/za/.venvs/farey-rh/bin/python q8_r2out_local.py --theta 1.2 \
    --M 512 --K-head 16 --n-sweep 400 --out Q8_R2OUT_F1024_THETA_RECEIPT.json
L_OUT block=1→3, +2, tail A=[8.5468889594095025342 +/- 4.84e-20] C=[7.8441184685665044486 +/- 2.49e-20] rho_theta=[0.50249982392119579649 +/- 1.51e-21]
L_OUT block=1→3, −1, tail A=[11.207041231978590615 +/- 4.83e-19] C=[10.200603763048093955 +/- 5.8e-22] rho_theta=[0.56124660625839629148 +/- 3.95e-21]
L_OUT block=2→1, +1, head W_theta=[63.340810575798769335 +/- 3.46e-19] rho_theta=[0.85711607499837192641 +/- 2.43e-21]
L_OUT block=2→3, +2, tail A=[1.7271454213382189547 +/- 1.29e-20] C=[1.8682567491567902932 +/- 3.82e-21] rho_theta=[0.50249778148431794561 +/- 3.13e-21]
L_OUT block=2→3, −1, tail A=[3.3038881600809401573 +/- 4.46e-20] C=[3.3278728030451464319 +/- 1.27e-20] rho_theta=[0.50249778148431794561 +/- 3.13e-21]
L_OUT block=3→2, +1, head W_theta=[32.442172466071799524 +/- 2.55e-20] rho_theta=[0.94804382980635864415 +/- 3.89e-21]
L_OUT block=3→3, +2, tail A=[1.6377953181026412302 +/- 2.93e-20] C=[1.7680385524567662782 +/- 2.94e-20] rho_theta=[0.50249686592435361658 +/- 3.78e-21]
L_OUT block=3→3, −1, tail A=[9.4267069982550466719 +/- 1.45e-20] C=[9.7392429453410402753 +/- 3.51e-20] rho_theta=[0.75796406616858429986 +/- 4.45e-23]
{
  "receipt": ".../lane_g/l_out/Q8_R2OUT_F1024_THETA_RECEIPT.json",
  "theta": ["1.2","1.2","1.2"],
  "runtime_seconds": 8.562645958001667
}
```

`sha256(Q8_R2OUT_F1024_THETA_RECEIPT.json) =`
`c2055cb817c84b912d7ec4c92cbb867c61a1dd9971c25b007b828a19ac801734`
— **caveat**: the receipt carries a `runtime_seconds` field (inherited from
`q8_r2_local.py`'s receipt shape), so its hash is **not** reproducible across
runs. Every mathematical field is; the hash is not a pin. A future pinned
L-OUT receipt should drop `runtime_seconds` from the hashed payload.

Receipts produced (all tracked in `l_out/`):

| receipt | theta | purpose |
|---|---|---|
| `Q8_R2OUT_F1024_THETA_RECEIPT.json` | uniform `1.2` | **production** |
| `Q8_R2OUT_F1024_THETA1p230_RECEIPT.json` | uniform `1.230` | recorded variant |
| `Q8_R2OUT_F1024_PERDISC_RECEIPT.json` | `(1.84, 1.30, 1.23)` | recorded variant |
| `Q8_R2OUT_F1024_THETAMAX_CONTROL_RECEIPT.json` | uniform `1.2369074008682055` | **negative control** |

with checker reports `Q8_LOUT_CHECK_THETA1p2.json`,
`Q8_LOUT_CHECK_THETA1p230.json`, `Q8_LOUT_CHECK_PERDISC.json`,
`Q8_LOUT_CHECK_THETAMAX_CONTROL.json`, an N-scan
`Q8_LOUT_NSCAN_THETA1p2.json`, and the adverse report
`Q8_LOUT_ADVERSE_THETA1p2.json`.

---

## 2. The production receipt (theta = 1.2 uniform)

Geometry (unscaled, from the pinned TB receipt):
`lambda = 1.84775906502257351226`,
`centers = (-0.84462319862073, -0.65328148243819, -0.27059805007310)`,
`source_radii = (0.79256333890554, 0.44834152916797, 0.54119610014620)`.
Enlarged **arc** radii `theta_i r_i = (0.95107600668663, 0.53800983500156,
0.64943532017544)`; the target-side `c_j`, `r_j` are untouched.

| block | family | `A_theta` / `W_theta` | `C_theta` | `q` | `rho_theta` | worst `n` |
|---|---|---|---|---|---|---|
| `1→3, +2` | Hurwitz tail | 8.54688895940951 | 7.84411846856651 | 0.5 | 0.50249982392120 | 401 (deep) |
| `1→3, −1` | Hurwitz tail | 11.2070412319786 | 10.2006037630481 | 0.5 | 0.56124660625840 | 1 |
| `2→1, +1` **A2** | single branch | 63.3408105757988 | — | 1.06568542494924 | 0.85711607499837 | 1 |
| `2→3, +2` | Hurwitz tail | 1.72714542133822 | 1.86825674915679 | 0.5 | 0.50249778148432 | 401 (deep) |
| `2→3, −1` | Hurwitz tail | 3.30388816008094 | 3.32787280304515 | 0.5 | 0.50249778148432 | 401 (deep) |
| `3→2, +1` **A3** | single branch | 32.4421724660718 | — | 1.45710678118655 | **0.94804382980636** | 1 |
| `3→3, +2` | Hurwitz tail | 1.63779531810264 | 1.76803855245677 | 0.5 | 0.50249686592435 | 401 (deep) |
| `3→3, −1` | Hurwitz tail | 9.42670699825505 | 9.73924294534104 | 0.5 | 0.75796406616858 | 1 |

All values are Arb `.upper()` strings (rounded UP). The referee's §3.3
prediction that the six tail families carry `q = 0.5` exactly is confirmed;
`A3 = (3,2,1,False,False)` is the binding block, in the **single-branch**
family, consumed with `theta^-N W_theta G_1(N, rho_theta)` — the corrected
form, not `A q^k + C k rho^{k-1}`.

**One spec number is not reproduced.** Referee §3.2 states that
`theta = 1.2` "gives `rho_theta <= 0.87` on every block". It does not: the
binding block `A3` has `rho_theta = 0.94804` (arc cover) / `0.94710` (exact
Möbius). The referee's own `theta_max = 1.2369074008682055` *is* confirmed as
the `rho_theta(A3) = 1` point (exact Möbius gives 0.99997 there), and
`theta = 1.230` giving `rho < 0.99` is confirmed (0.99092 arc cover /
0.98991 exact). So the recommendation to pin `1.2` survives — `rho_theta < 1`
strictly on every block, margin 0.052 — but the quoted `0.87` is wrong by
roughly the whole margin and should not be relied on.

---

## 3. The output tail and `full_tau`

Per block, `tau_out(N) = theta_i^{-N} * sum_{k<N} M_k(theta)` with `M_k` the
closed-form majorant (2.7) of the block's own family. The block totals are
then substituted into **each** `trace[.]` slot of the existing telescoping at
`q8_schur_contour.py:351-358`,

```
input_tail_only = trace[B3] + a3*trace[B2] + a3*a2*trace[B1]
                + trace[A3]*b2 + trace[A3]*a2*b1 + a3*trace[A2]*b1
```

with the `hs[.]` factors `a2, a3, b1, b2` **unchanged**, exactly as referee
condition 5 prescribes. This is the step that "(2.6)" alone does not license
(GAP 5): (2.6) is a single-operator inequality, whereas telescoping
`X - X~` factor by factor needs the full per-block defect `tau_in + tau_out`
in every `trace[.]` slot. The substitution is stated here explicitly, and the
checker performs it that way.

`hs` factors at the pin (from the **unmodified**
`q8_schur_contour.load_operator_bounds`):
`a2 = 37.1900706769`, `a3 = 22.7436858371`, `b1 = 13.3870991026`,
`b2 = 4.07640688778`, `b3 = 11.3345795885`.

Per-block `tau_out(104)`, theta = 1.2 (trace / HS):

| block | trace | HS |
|---|---|---|
| A2 | 2.58137208273e-6 | 7.16016148771e-7 |
| A3 | 3.62184370999e-6 | 5.93798537141e-7 |
| B1 | 7.23160586135e-7 | 2.82822110755e-7 |
| B2 | 1.80839504597e-7 | 7.39691184015e-8 |
| B3 | 1.13854456702e-6 | 3.03763017105e-7 |

Telescoped totals (theta = 1.2 uniform):

```
$ /Users/za/.venvs/farey-rh/bin/python q8_lout_check.py \
    --lout Q8_R2OUT_F1024_THETA_RECEIPT.json \
    --out Q8_LOUT_CHECK_THETA1p2.json --N-targets 104 181 200 214 240 256 260 261 262 263
L_OUT_CHECK N=104 input=[1.2647467e-12 +/- 1.10e-20] output=[0.0032208457 +/- 4.93e-11] full=[0.0032208458 +/- 4.96e-11]
L_OUT_CHECK N=181 input=[1.0240621e-24 +/- 8.76e-33] output=[2.5819925e-9 +/- 3.11e-17] full=[2.5819925e-9 +/- 3.11e-17]
L_OUT_CHECK N=200 input=[1.0637757e-27 +/- 2.67e-36] output=[8.0820457e-11 +/- 3.58e-19] full=[8.0820457e-11 +/- 3.58e-19]
L_OUT_CHECK N=214 input=[6.7377297e-30 +/- 2.14e-39] output=[6.2948713e-12 +/- 4.02e-20] full=[6.2948713e-12 +/- 4.02e-20]
L_OUT_CHECK N=240 input=[5.5706627e-34 +/- 2.64e-42] output=[5.4989084e-14 +/- 1.74e-22] full=[5.4989084e-14 +/- 1.74e-22]
L_OUT_CHECK N=256 input=[1.7121434e-36 +/- 8.17e-45] output=[2.9742463e-15 +/- 4.93e-23] full=[2.9742463e-15 +/- 4.93e-23]
L_OUT_CHECK N=260 input=[4.0313354e-37 +/- 1.89e-45] output=[1.4343397e-15 +/- 3.61e-23] full=[1.4343397e-15 +/- 3.61e-23]
L_OUT_CHECK N=261 input=[2.8081879e-37 +/- 4.39e-45] output=[1.1952831e-15 +/- 1.36e-23] full=[1.1952831e-15 +/- 1.36e-23]
L_OUT_CHECK N=262 input=[1.9561556e-37 +/- 3.93e-45] output=[9.9606926e-16 +/- 4.97e-24] full=[9.9606926e-16 +/- 4.97e-24]
L_OUT_CHECK N=263 input=[1.3626384e-37 +/- 1.66e-45] output=[8.3005774e-16 +/- 1.52e-24] full=[8.3005774e-16 +/- 1.52e-24]
```

### 3.1 The N consequence is worse than the note predicted — DIAGNOSTIC

`Q8_OUTPUT_TAIL_SOL.md` §3.2/§5.3 predicts "roughly `N >= 200`". The certified
telescoped figure, for `full_tau <= 1e-15`:

| theta | first N with `full_tau <= 1e-15` | `full_tau` there |
|---|---|---|
| uniform `1.2` | **262** | 9.96069265240e-16 |
| uniform `1.230` | **238** | 8.44013360000e-16 |
| per-disc `(1.84, 1.30, 1.23)` | **237** | 8.74503470000e-16 |

Root cause of the gap to "`N >= 200`": the note compares a **block-level**
`tau_out` against a **block-level** `tau_in`. Once both are pushed through the
Schur telescoping, the output term is multiplied by `hs` factors as large as
`a2 * b1 = 497.9`, and the dominant term is `tau_out[A3] * a2 * b1`
(1.803e-3 of the 3.221e-3 total at `N = 104`). That is a fixed ~3-order
inflation, i.e. ~+37 steps at rate 0.833 and ~+22 at rate 0.813. The
qualitative headline ("`N = 104` is far too small; the production contour
needs `N` in the low hundreds") stands; the number is 262 not 200 at the
recommended theta.

Per-disc theta buys almost nothing over uniform `1.230` (237 vs 238) because
the telescoping is dominated by the disc-3 terms, where the permitted theta is
capped near 1.23 by `rho_theta(A3) -> 1`. It also pushes `rho_theta` on the
disc-1 tail families to 0.99795, which is far less comfortable. **Uniform
`theta = 1.230` is the better production choice on this evidence**; the
production run recorded here nevertheless uses the referee-recommended `1.2`.

### 3.2 Independent mpmath cross-check

```
$ /Users/za/miniforge3/envs/pari-arb/bin/python3 q8_lout_crosscheck_mpmath.py \
    --lout Q8_R2OUT_F1024_THETA_RECEIPT.json --check Q8_LOUT_CHECK_THETA1p2.json
rho_theta cross-check (mpmath exact Moebius vs Arb receipt):
  1→3, +2, tail      receipt=0.502499823921   mpmath=0.502499823921   rel_diff=1.85e-24
  1→3, −1, tail      receipt=0.561246606258   mpmath=0.561133880178   rel_diff=0.000201
  2→1, +1, head      receipt=0.857116074998   mpmath=0.856311225466   rel_diff=0.00094
  2→3, +2, tail      receipt=0.502497781484   mpmath=0.502497781484   rel_diff=1.85e-24
  2→3, −1, tail      receipt=0.502497781484   mpmath=0.502497781484   rel_diff=1.85e-24
  3→2, +1, head      receipt=0.948043829806   mpmath=0.947097942205   rel_diff=0.000999
  3→3, +2, tail      receipt=0.502496865924   mpmath=0.502496865924   rel_diff=1.85e-24
  3→3, −1, tail      receipt=0.757964066169   mpmath=0.757901592455   rel_diff=8.24e-5
  worst relative difference: 0.000999
full_tau cross-check (mpmath vs Arb checker):
  N=104  mpmath=0.003220845751   arb=0.003220845751   rel_diff=1.08e-12
  N=181  mpmath=2.58199247e-9    arb=2.58199247e-9    rel_diff=1.38e-12
  N=200  mpmath=8.082045738e-11  arb=8.082045738e-11  rel_diff=4.59e-13
  N=214  mpmath=6.294871342e-12  arb=6.294871342e-12  rel_diff=1.18e-13
  N=240  mpmath=5.498908419e-14  arb=5.498908419e-14  rel_diff=6.33e-13
  N=256  mpmath=2.97424635e-15   arb=2.97424635e-15   rel_diff=4.82e-13
  N=260  mpmath=1.434339664e-15  arb=1.434339664e-15  rel_diff=2.42e-12
  N=261  mpmath=1.195283087e-15  arb=1.195283087e-15  rel_diff=2.73e-12
  N=262  mpmath=9.960692652e-16  arb=9.960692652e-16  rel_diff=6.0e-13
  N=263  mpmath=8.300577417e-16  arb=8.300577417e-16  rel_diff=2.88e-14
smallest N with full_tau <= 1e-15 (mpmath, input tail bounded by 1.363e-37): 262
```

The `rho` differences (<= 0.1%) are the arc-cover outer bound vs the exact
Möbius image; the receipt value is the larger, i.e. conservative, one in every
case. `full_tau` agrees to 1e-12 relative and the crossing `N = 262` is
reproduced independently.

---

## 4. The seven pass/fail conditions

### 4.1 Condition 1 — `theta_i > 1` strictly, recorded exactly — **PASS**

Receipt field `theta_exact_strings = ["1.2","1.2","1.2"]`,
`theta_uniform = true`. Checker: `strictly_greater_than_one: true` for discs
1, 2, 3 (`theta.lower() > 1` in Arb). `Q8_LOUT_CHECK_THETA1p2.json`
→ `condition_1_theta_gt_1.pass = true`.

### 4.2 Condition 2 — holomorphy gate at the enlarged radius — **PASS**

All eight blocks, every field true, recomputed by the checker (not read from
the receipt), with strictly positive pole clearance:

| block | pole margin (lower) | branch-cut margin (lower) | deep-tail `d` (lower) | Hurwitz slope | `a_0` |
|---|---|---|---|---|---|
| `1→3, +2` | 1.899818924 | 1.899818924 | 25.92068677 | 0.5147186 | 6 |
| `1→3, −1` | 1.741306256 | 1.741306256 | 25.76217410 | 0.5147186 | 5 |
| `2→1, +1` | 0.656467747 | 0.656467747 | 0.656467747 | 0.2911688 | 5 |
| `2→3, +2` | 2.504226812 | 2.504226812 | 26.52509465 | 0.2911688 | 6 |
| `2→3, −1` | 1.963030712 | 1.963030712 | 25.98389855 | 0.2911688 | 5 |
| `3→2, +1` | 0.927725694 | 0.927725694 | 0.927725694 | 0.3514718 | 5 |
| `3→3, +2` | 2.775484759 | 2.775484759 | 26.79635260 | 0.3514718 | 6 |
| `3→3, −1` | 1.468921794 | 1.468921794 | 25.48978964 | 0.3514718 | 5 |

Margins are lower bounds (rounded DOWN); the slope is an upper bound (rounded
UP). Worst pole clearance 0.6565 at the enlarged radius; worst Hurwitz slope
`theta_1 r_1 / lambda = 0.51472 < a_0 = 5`. This also settles referee GAP 6:
the `0.53` slope figure is the uniform-`theta = 1.2369` value; at
`theta = 1.2` it is 0.5147, and the margin to `a_0` is wide either way.

### 4.3 Condition 3 — `rho_theta` reproduced by the checker's own Möbius — **PASS**

The checker never reads `rho_theta` as fact: it recomputes it from
`centre = ∓a/(a^2 - R^2)`, `radius = R/(a^2 - R^2)`, `a = c_i ∓ n lambda`,
`R = theta_i r_i`, sweeping `n = n_0 .. 400` plus a crude deep-tail bound for
`n >= 401`, with the geometry taken from the **pinned TB receipt** (the
L-OUT geometry echo is separately verified to overlap it —
`geometry_echo_overlaps_pinned_TB: true`).

| block | receipt `rho_theta` | checker Möbius `rho_theta` | receipt worst `n` | checker worst `n` | `< 1` |
|---|---|---|---|---|---|
| `1→3, +2` | 0.502499823921 | 0.502499823921 | 401 | 401 | yes |
| `1→3, −1` | 0.561246606258 | 0.561133880178 | 1 | 1 | yes |
| `2→1, +1` | 0.857116074998 | 0.856311225466 | 1 | 1 | yes |
| `2→3, +2` | 0.502497781484 | 0.502497781484 | 401 | 401 | yes |
| `2→3, −1` | 0.502497781484 | 0.502497781484 | 401 | 401 | yes |
| `3→2, +1` | 0.948043829806 | 0.947097942205 | 1 | 1 | yes |
| `3→3, +2` | 0.502496865924 | 0.502496865924 | 401 | 401 | yes |
| `3→3, −1` | 0.757964066169 | 0.757901592455 | 1 | 1 | yes |

Every receipt value covers the checker's value and agrees within 0.1%
(threshold 1%), and every `rho_theta < 1` strictly. Coverage is tested at
`1e-20` relative tolerance, because the receipt value is an 80-digit decimal
round trip of an Arb ball and can land ~1e-24 relative below a freshly
computed upper endpoint; the raw ratio is recorded per block so the margin is
auditable.

The `n`-sweep requirement bites exactly as the referee warned: for four of the
six tail families the worst `n` is the deep-tail cutoff (401), **not** `n_0`.
Sweeping only `n = n_0` would have under-reported `rho_theta` for those blocks.

**Negative control.** The same pipeline at the referee's rate optimum
`theta = 1.2369074008682055` yields `rho_theta(A3) = 1.0010071438982470307`
(arc cover; exact Möbius 0.99997), and condition 3 **FAILS** there
(`rho_theta_below_one: false`) — `Q8_LOUT_CHECK_THETAMAX_CONTROL.json`,
conditions `[true, true, false, false, true, true, false]`. The gate bites,
and the referee's "do NOT pin the optimum" is confirmed mechanically.

### 4.4 Condition 4 — self-consistency and monotonicity in theta — **FAIL**

This condition has two sub-tests. It is reported FAIL because sub-test 4a is
not met. The lane therefore stays OPEN. The diagnosis follows.

**4a — `selected_column_bounds_theta[k] >= direct enlarged-arc sup` — FAIL
(and the pinned baseline fails the same test).**

| block | 4a holds | first `k` where selected < direct |
|---|---|---|
| `1→3, +2` | no | 6 |
| `1→3, −1` | no | 6 |
| `2→1, +1` **A2** | **yes** | — |
| `2→3, +2` | no | 8 |
| `2→3, −1` | no | 6 |
| `3→2, +1` **A3** | **yes** | — |
| `3→3, +2` | no | 8 |
| `3→3, −1` | no | 8 |

The checker also runs a **baseline control** on the PINNED
`Q8_R2_F1024_LOCAL_RECEIPT.json` itself:
`baseline_control_pinned_R2_satisfies_4a: false`, with the first failing `k` at
7, 7, 9, 8, 10, 7 for the six tail families. Independent reproduction:

```
$ /Users/za/.venvs/farey-rh/bin/python -c "... Q8_R2_F1024_LOCAL_RECEIPT.json ..."
1→3, +2, tail k where selected<direct: [7, 8, 9, 10, 11] ratios k=6,10,16: ['1.00000', '[0.0881904 +/- 2.26e-8]', '[0.000705742 +/- 2.29e-10]']
1→3, −1, tail k where selected<direct: [7, 8, 9, 10, 11] ratios k=6,10,16: ['1.00000', '[0.0564902 +/- 4.50e-8]', '[0.000367164 +/- 1.97e-10]']
2→3, +2, tail k where selected<direct: [9, 10, 11, 12, 13] ratios k=6,10,16: ['1.00000', '[0.503411 +/- 2.39e-7]', '[0.00849628 +/- 3.76e-9]']
2→3, −1, tail k where selected<direct: [8, 9, 10, 11, 12] ratios k=6,10,16: ['1.00000', '[0.120425 +/- 2.81e-7]', '[0.000916651 +/- 2.07e-10]']
3→3, +2, tail k where selected<direct: [10, 11, 12, 13, 14] ratios k=6,10,16: ['1.00000', '[0.817391 +/- 2.48e-7]', '[0.0195718 +/- 1.66e-8]']
3→3, −1, tail k where selected<direct: [7, 8, 9, 10, 11] ratios k=6,10,16: ['1.00000', '[0.0761552 +/- 1.47e-8]', '[0.000552099 +/- 4.03e-10]']
```

**Reading.** `q8_r2_local.py:206` *deliberately* sets
`selected[k] = min(direct_sup[k], envelope[k])`. Both are certified upper
bounds on the true column sup, and the `min` is the tighter one. The direct
arc-cover sup is computed through the `r_j^{-k}` binomial sum of
`exact_tail_columns_on_arc`, so interval wrapping inflates it geometrically in
`k`; past `k ≈ 7` it is the looser of the two and the `min` correctly picks
the envelope. Condition 4a as literally written ("the receipt's own envelope
must not undercut its own direct sups") therefore **cannot** be satisfied by
this pipeline — the certified baseline it is meant to validate fails it too.
It is a mis-specified condition, not a defect in the L-OUT run. The enlarged
contour makes the wrapping bite one to two columns earlier (first failure at
`k = 6–8` vs `7–10`), which is the expected direction.

**This is reported as FAIL, not waived.** Ruling on whether to respecify 4a
(e.g. "`max(selected, envelope)[k] >= direct[k]`", or "the envelope dominates
the direct sup for all `k` below the wrapping knee") belongs to the referee,
not to this compute lane.

One artifact *was* found and fixed rather than argued away: on the two
single-branch blocks 4a initially failed at `k = 0` with ratio
`1.0000000 ± 3.3e-10`, because two Arb routes compute the same `k = 0`
boundary sup (`weight_sup`'s argmax selector vs the `max_arb` hull) and differ
in the last bits. `q8_r2out_local.py` now rounds `W_theta` UP to the larger of
the two. Both single-branch blocks then pass 4a at every `k` (envelope/direct
ratio 1.0, 4.44, 5.90, 7.18 at `k = 0, 6, 10, 16` for A2; 1.0, 3.35, 4.48,
5.68 for A3), so the binding block is clean.

**4b — `selected_column_bounds_theta[k] >= selected_column_bounds[k]` from the
pinned R2 receipt (monotonicity in theta) — FAIL as run, PASS like-for-like.**

The production arm fails on 4 of 8 blocks (min ratio 0.183). The cause is not
the contour: it is that the referee's own mandated `n`-sweep to 400 produces a
**tighter** `rho_theta` than the pinned R2 receipt, whose deep tail was cut at
`first_n = 14/15` (TB `ratio_upper_bound` for `1→3,+2` is 0.5709, dominated by
that crude cutoff; swept to 401 the same quantity is 0.5025). Two changes are
confounded in the comparison.

The checker therefore also computes a **like-for-like** arm: the same enlarged
contour with the deep-tail cutoff put back at TB's `first_n`, so `theta` is
the only difference. That arm **passes on all 8 blocks**:

| block | like-for-like `min_k selected_theta[k] / selected_R2[k]` |
|---|---|
| `1→3, +2` | 1.66810076299 |
| `1→3, −1` | 1.74063838638 |
| `2→1, +1` | 2.07097611977 |
| `2→3, +2` | 1.24584114460 |
| `2→3, −1` | 1.34036568554 |
| `3→2, +1` | 1.98813529748 |
| `3→3, +2` | 1.26824889511 |
| `3→3, −1` | 1.60582650029 |

Every ratio exceeds 1 with margin 0.246 or better, so **the contour was
genuinely enlarged** — which is what 4b exists to detect. Recorded as a
diagnostic; it does not convert 4b's production arm into a pass.

### 4.5 Condition 5 — `output_projection_tail(N)` finite, `full_tau` by the stated substitution — **PASS**

`full_tau_finite: true` at every `N` target. The substitution is the one
prescribed: the block output tails go into **each** `trace[.]` slot of the
`q8_schur_contour.py:351-358` telescoping, `hs[.]` factors unchanged (§3
above). As a self-check the checker re-runs the same telescoping on the
unmodified `trace[.]` dictionary and reproduces `input_tail_only` exactly.

| `N` | `input_tail_only` | `output_projection_tail` | `full_tau` |
|---|---|---|---|
| 104 | 1.26474668906e-12 | 3.22084575010e-3 | **3.22084575137e-3** |
| 181 | 1.02406210875e-24 | 2.58199246964e-9 | 2.58199246964e-9 |
| 200 | 1.06377569733e-27 | 8.08204573802e-11 | 8.08204573802e-11 |
| 214 | 6.73772969788e-30 | 6.29487134185e-12 | 6.29487134185e-12 |

(All upper bounds, rounded UP.)

### 4.6 Condition 6 — `N = 104` regression / red flag — **PASS**

`full_tau(104) = [0.00322084575137 +/- 3.15e-15]`,
`input_tail_only(104) = [1.26474668906e-12 +/- 2.13e-24]`.
`red_flag_full_tau_le_1e-14: false`. The output term dominates the input term
by a factor 2.5e9, so it was demonstrably neither dropped nor mis-scaled — the
failure mode the red flag exists to catch did not occur.

Honest note on magnitude: the referee expected "`full_tau ~ 1e-7`" at
`N = 104`; the computed value is 3.22e-3, i.e. **4.5 orders larger**. The
referee's figure is a block-level `tau_out`; the telescoped quantity carries
the `hs` factors (§3.1). The pass/fail test as written (`> 1e-14`) is met
either way, and the discrepancy is in the conservative direction.

### 4.7 Condition 7 — flip `full_tail_certified` — **NOT SATISFIED**

Conditions 1–6 evaluate to `[true, true, true, false, true, true]`.
Condition 4 is not met, so `full_tail_certified` is **not** flipped. The
fail-closed path at `q8_schur_contour.py:717-721` / `746-790` stands
unchanged; `q8_schur_contour.py:395` still reads `False`. No lane_f file was
edited, so nothing downstream can have been loosened.

### 4.8 Adverse regression (referee §3.4, closing paragraph) — 15/15 hold

```
$ /Users/za/.venvs/farey-rh/bin/python q8_lout_adverse.py \
    --lout Q8_R2OUT_F1024_THETA_RECEIPT.json --N 6 10 14 --rows 60 \
    --out Q8_LOUT_ADVERSE_THETA1p2.json
ADVERSE N=6 A2 lhs=[26.884711 +/- 4.42e-7] rhs=[4.1012154 +/- 2.86e-8] holds=True
ADVERSE N=6 A3 lhs=[15.822838 +/- 2.90e-7] rhs=[2.4134113 +/- 2.93e-8] holds=True
ADVERSE N=6 B1 lhs=[7.7944408 +/- 1.75e-8] rhs=[0.53116841 +/- 3.57e-10] holds=True
ADVERSE N=6 B2 lhs=[1.8102796 +/- 2.42e-8] rhs=[0.018959274 +/- 4.95e-10] holds=True
ADVERSE N=6 B3 lhs=[4.8718850 +/- 9.93e-9] rhs=[0.23392027 +/- 3.12e-9] holds=True
ADVERSE N=10 A2 lhs=[13.041155 +/- 1.69e-7] rhs=[0.65187694 +/- 2.95e-10] holds=True
ADVERSE N=10 A3 lhs=[7.8698114 +/- 2.21e-8] rhs=[0.48945274 +/- 4.24e-9] holds=True
ADVERSE N=10 B1 lhs=[6.2669266 +/- 1.32e-8] rhs=[0.020389705 +/- 2.07e-10] holds=True
ADVERSE N=10 B2 lhs=[1.0152866 +/- 1.70e-8] rhs=[0.00012073374 +/- 1.53e-12] holds=True
ADVERSE N=10 B3 lhs=[7.5332891 +/- 4.49e-8] rhs=[0.010217349 +/- 2.99e-10] holds=True
ADVERSE N=14 A2 lhs=[6.2959675 +/- 3.18e-8] rhs=[0.10945012 +/- 1.84e-9] holds=True
ADVERSE N=14 A3 lhs=[3.8426869 +/- 2.79e-9] rhs=[0.12037621 +/- 3.65e-9] holds=True
ADVERSE N=14 B1 lhs=[11.738175 +/- 2.26e-7] rhs=[0.00059629039 +/- 1.63e-12] holds=True
ADVERSE N=14 B2 lhs=[1.0815468 +/- 1.07e-8] rhs=[7.0911288e-7 +/- 3.81e-15] holds=True
ADVERSE N=14 B3 lhs=[29.223425 +/- 3.22e-7] rhs=[0.00068666094 +/- 2.28e-12] holds=True
{"passed": 15, "total": 15, ...}
```

`T` is built by the **unmodified** `q8_r3b_engine`
(`build_q8_block_matrices_and_s_derivative`, `sign = 1`, `n_head = 4`,
factors `("10","4","2")`) at the pin centre. **Caveat, stated in the report
itself**: the right-hand side sums rows `m` in `[N, 60)` only, so it is a
*lower* bound on the true omitted-row mass. A pass is a necessary condition,
not a proof of the bound. The margins are large (LHS/RHS from 6.6x to 1.7e6x),
and the referee reports 60/60 of the analogous checks holding at other thetas.

---

## 5. Verdict table

| # | Condition | Verdict | Receipt |
|---|---|---|---|
| 1 | `theta_i > 1` strictly, recorded exactly | **PASS** | `theta_exact_strings = ["1.2","1.2","1.2"]`; `condition_1_theta_gt_1.pass = true` |
| 2 | Holomorphy gate true, pole clearance strictly positive at `theta_i r_i` | **PASS** | 8/8 blocks; worst pole margin 0.6565; worst slope 0.5147 < `a_0` = 5 |
| 3 | `rho_theta` reproduced by the checker's own Möbius, `n` swept to 400 | **PASS** | 8/8 covered, agree to <= 0.1%, all `< 1`; worst `n` = 401 on 4 blocks; negative control at `theta_max` correctly FAILS |
| 4 | Self-consistency (4a) and monotonicity in theta (4b) | **FAIL** | 4a: 2/8 blocks pass — and the **pinned R2 receipt fails the same test** (`baseline_control_pinned_R2_satisfies_4a: false`), so the condition is mis-specified. 4b: production arm confounded by the mandated deeper `n`-sweep; like-for-like arm passes 8/8, min ratio 1.246 |
| 5 | `output_projection_tail(N)` finite; `full_tau` by substitution into each `trace[.]` slot | **PASS** | `full_tau_finite: true` at N = 104/181/200/214; substitution stated in §3 and implemented that way |
| 6 | `N = 104` red-flag regression (`full_tau <= 1e-14` is a red flag) | **PASS** | `full_tau(104) = 3.22084575137e-3`; red flag NOT triggered; output term 2.5e9x the input term |
| 7 | Flip `full_tail_certified` only if 1–6 hold | **NOT SATISFIED** | 1–6 = `[true, true, true, false, true, true]`; `q8_schur_contour.py:395` still `False`; fail-closed path stands |
| — | Adverse regression vs unmodified engine | **15/15 hold** | rows truncated at 60 — necessary, not sufficient |

**Overall: the lane stays OPEN.** L-OUT is not certified. Condition 4 is
unmet, and the honest reason is a defect in the condition rather than in the
computation — but that is the referee's call to make, not this lane's, and no
pass is forced.

---

## 6. Findings the referee should rule on

1. **Condition 4a is unsatisfiable by the R2 pipeline as designed.**
   `q8_r2_local.py:206` takes `min(direct_sup, envelope)`; the pinned R2
   receipt fails 4a at `k = 7–10`. Respecify or drop.
2. **`theta = 1.2` does not give `rho_theta <= 0.87`** (referee §3.2). The
   binding block A3 has `rho_theta = 0.94804`. The recommendation survives
   (`rho < 1`, margin 0.052); the quoted bound does not.
3. **`theta_max = 1.2369074008682055` is confirmed as the `rho_theta(A3) = 1`
   point**, and the certification correctly refuses it (arc cover gives
   1.00101 > 1). "Do NOT pin the optimum" is now mechanically enforced.
4. **The `n`-sweep to 400 is load-bearing and also confounds 4b.** On 4 of 6
   tail families the worst `n` is the sweep cutoff, not `n_0` — but the same
   sweep makes `rho_theta` tighter than the pinned R2's, so 4b needs the
   like-for-like arm to mean what it was written to mean.
5. **`N >~ 200` is optimistic.** The telescoped requirement for
   `full_tau <= 1e-15` is `N = 262` at `theta = 1.2`, `238` at `1.230`,
   `237` per-disc. The `hs` factors (`a2 b1 = 497.9`) cost ~3 orders that the
   note's block-level comparison omits.
6. **The L-OUT receipt is not hash-pinnable as emitted.** It inherits
   `runtime_seconds` from the `q8_r2_local.py` receipt shape, so its sha256
   changes on every run. Drop that field from the payload before any
   `PINNED_RECEIPT_SHA256` entry is added.
7. **Uniform `theta = 1.230` beats the per-disc option** (238 vs 237, a
   one-step difference) at a much safer `rho_theta` profile: per-disc pushes
   the disc-1 tail families to 0.99795. Recommend `1.230` uniform for
   production if L-OUT is ever re-specified and re-run.

## 7. What L-OUT still does NOT close

Unchanged from referee §3.5. The Hardy/Hilbert operator/basis/norm binding
(**separately OPEN — not claimed here**), E1 on the enlarged disc, `K_s`
nonvanishing and word/lattice identification, the Selberg
determinant/zeta/scattering factorization, the four-edge winding, and the
independently-false `recorded_tail_checks_pass` gate. L-OUT would have closed
one gate of six; on this run it closes none, because condition 4 is unmet.

---

**READY FOR JUDGING.**
