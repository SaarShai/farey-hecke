# L-OUT condition 4 — cold adjudication

**Date** 2026-08-20 · **Lane** lane_g (adjudication, independent of the L-OUT
compute lane) · **Branch** `codex/prime-step-review-economic-validation` ·
**Mode** read-only on the work product. This file is the only new artifact. No
existing file was edited, nothing was committed, nothing was pushed.

**Interpreters used.** `/Users/za/.venvs/farey-rh/bin/python` (python-flint /
Arb, `ctx.prec = 384`) for every certified number;
`/Users/za/miniforge3/envs/pari-arb/bin/python3` (mpmath, 30–50 dps) for the
independent non-Arb arm. All scripts written for this adjudication live in the
session scratchpad, not in the repo.

---

## 1. The dispute, restated

`Q8_OUTPUT_TAIL_REFEREE.md` §3.4 sets seven pass/fail conditions for receipt
L-OUT. `L_OUT_RECEIPT_SOL.md` reports 5 of 7 met, condition 4 **FAIL**, and the
lane OPEN. The executor's position:

* **4a** (`selected_column_bounds_theta[k] >= the direct enlarged-arc sup for
  every k <= K_head`) is **mis-specified**, not violated:
  `lane_f/q8_r2_local.py:206` deliberately sets
  `selected[k] = min(direct_sup[k], envelope[k])`, so `selected < direct`
  wherever the envelope is tighter. The pinned R2 receipt — the certified
  baseline the condition exists to validate — fails the identical test at
  `k = 7–10`. The cause given: interval wrapping in the `r_j^{-k}` binomial sum
  of `exact_tail_columns_on_arc` inflates the direct sup geometrically in `k`.
* **4b** (`selected_column_bounds_theta[k] >= selected_column_bounds[k]` from
  the pinned R2 receipt) fails on 4 of 8 blocks in the production arm, but the
  confound is the spec's own mandated `n`-sweep to 400, which yields a tighter
  `rho_theta` than the pinned R2's deep-tail cut at `first_n = 14/15`. The
  like-for-like arm passes 8/8, min ratio 1.246.

Two spec errata are also claimed: `rho_theta(A3)` at `theta = 1.2` is 0.948,
not `<= 0.87`; and the certified `N` for `full_tau <= 1e-15` is 262, not
`~200`, because the Schur telescoping multiplies the output tail by `hs`
factors as large as `a2 * b1 = 497.9`.

Everything below is re-derived or re-run by this lane. Nothing is taken from
the executor's report or from the referee's report as fact.

---

## 2. What soundness actually requires

### 2.1 The chain

From `Q8_OUTPUT_TAIL_SOL.md` §2 (as amended by its eight appended correction
blocks), the omitted-output term enters only through

```text
M_k^{(i,j)}(theta) := sup_{|u| = theta} | (T^{(i,j)} e_{j,k})(c_i + r_i u) |     (defn)

sum_{m >= N} |T[m,k]|^2      <=  theta^(-2N) M_k(theta)^2                        (2.3)
|| (I-P_N) T P_N ||_HS       <=  theta^(-N) sqrt( sum_{k<N} M_k(theta)^2 )       (2.4)
|| (I-P_N) T P_N ||_1        <=  theta^(-N) sum_{k<N} M_k(theta)                 (2.5)
```

(2.3)–(2.5) are monotone increasing in each `M_k`. Therefore the chain stays
valid when `M_k` is replaced by **any** quantity `b_k^theta >= M_k(theta)`.
Nothing in the derivation refers to how `b_k^theta` was produced, and nothing
refers to a second, coarser upper bound of the same object.

**Consequence.** Soundness requires

```text
selected_column_bounds_theta[k]  >=  M_k(theta)          (the TRUE boundary sup)
```

and **not** `selected >= direct_sup[k]`. If `D_k` and `E_k` are each proven
upper bounds of `M_k`, then `min(D_k, E_k) >= M_k` as well. The `min` at
`q8_r2_local.py:206` is therefore sound by construction, and requiring
`selected >= D_k` is requiring the receipt to discard the tighter of two valid
certificates.

### 2.2 Both arms are genuine upper bounds of the same object

* **Direct arm `D_k`.** `exact_tail_columns_on_arc` evaluates the exact column
  function on an Arb ball that covers one arc of the boundary circle;
  `abs_upper()` over the 512-arc cover is a rigorous upper bound of
  `sup_{|u|=theta} |f_k|`. It is an upper bound only. It is **not** a witness
  and it is **not** a lower bound of `M_k`.
* **Envelope arm `E_k`.** The `A q^k + C k rho^(k-1)` form is the center-split
  mean-value majorant. Re-derived here from scratch. With
  `u_n(z) = (psi_n(z) - c_j)/r_j`, `psi_n(z) = ±1/(z ∓ n lambda)`, and
  `f_k(z) = sum_n w_n(z) u_n(z)^k`:

  ```text
  u_n = (-c_j/r_j) + psi_n/r_j ,  so by the mean value theorem for t -> t^k
  | u_n^k - (-c_j/r_j)^k |  <=  k * max(|u_n|, |c_j|/r_j)^(k-1) * |psi_n|/r_j

  |f_k(z)|  <=  q^k |sum_n w_n(z)|  +  k rho^(k-1) sum_n |w_n(z) psi_n(z)|/r_j
            <=  A q^k  +  C k rho^(k-1)
  ```

  with `q = |c_j|/r_j`, `A >= sup_z |f_0(z)|` (and `f_0 = sum_n w_n` exactly,
  because `e_{j,0} = 1` — this is why `A = direct_sups[0]` is legitimate),
  `C >= sup_z sum_n |w_n psi_n|/r_j`, and `rho >= max(sup_{n,z}|u_n|, q)`.

  The derivation is independent of the interval evaluation of `f_k`. Its three
  preconditions are checkable per receipt, and are checked in §3.3 below.

### 2.3 The direct arm is the loose one, by a factor up to 7.5e7

Because `columns[k] = sum_{m<=k} C(k,m) (-c_j)^(k-m) r_j^(-k) z_terms[m]` is an
alternating binomial sum with a `r_j^(-k)` scale (`r_j < 1`), an Arb ball input
loses the cancellation and the enclosure width grows geometrically in `k`.
§3.1 measures this: at `k = 16` the pinned baseline's direct sup exceeds a
point-evaluated witness of the true sup by up to **7.47e7**, while `selected`
exceeds the same witness by 5.3e4 at most. The `min` is the correct engineering
choice and the one the tail bound consumes.

### 2.4 The direct sups are not even load-bearing

`tau_out` is assembled in `l_out/q8_r2out_local.py` and in the checker from the
**closed forms** only:

```text
tail family    theta^-N * ( A_theta*G1(N,q) + C_theta*S1(N,rho_theta) )     (trace)
single branch  theta^-N * W_theta * G1(N,rho_theta)                          (trace)
```

i.e. from `sum_{k<N} E_k`. Neither `direct_column_sups_theta` nor
`selected_column_bounds_theta` enters `tau_out` at any `N`. Verified by
re-implementing the consumption from the receipt fields alone and reproducing
the executor's `tau_out` table to all printed digits (§4.2). So condition 4a as
written grades a diagnostic array against another diagnostic array, and grades
it in the direction that forbids the tighter certificate.

### 2.5 Internal evidence that the referee itself ran the witness test

`Q8_OUTPUT_TAIL_REFEREE.md:382` records the referee's own criterion (a) check:
"8/8 blocks x 17 k values, `min(b_k/sup_k) ∈ [1.026, 1.098]`, zero
violations". No violations are possible against the interval direct sups — the
pinned receipt fails that comparison at `k = 7` on three blocks (§3.2). The
value **1.026** is reproduced exactly in §3.1 as `min_k selected/witness` on
block `2→3, +2` of the pinned receipt, and 1.098 sits in the single-branch
range. The referee's executed test was therefore witness-domination; only the
prose of condition 4a diverged from it.

### VERDICT ON 4a: **MIS-SPECIFIED.** Not a soundness hole.

The property "selected >= direct sup" was never guaranteed by the engine, is
not required by (2.3)–(2.5), is not satisfied by the certified pinned baseline,
and governs an array that no consumed quantity reads.

---

## 3. The corrected condition 4, and its evaluation

### Corrected 4a (soundness-preserving form)

> **4a'.** For every block and every `k <= K_head`, the recorded column bound
> must dominate a rigorous lower-bound **witness** of the true boundary sup:
>
> ```text
> selected_column_bounds_theta[k]  >=  W_k ,
> W_k := max over >= 256 boundary points z of |u| = theta of  |f_k(z)|.lower()
> ```
>
> evaluated with a point `z` and a point `s` inside the pinned `s`-box (so
> `W_k <= M_k(theta)` rigorously), by an evaluation path that does not reuse
> the receipt's own arc-cover enclosure. In addition the envelope's three
> preconditions must be recorded and checked:
> `A_theta >= W_0`, `C_theta >= sup_z sum_n |w_n psi_n|/r_j`, and
> `rho_theta >= max(sup_{n,z} |u_n(z)|, q)`.
>
> No relation between `selected` and `direct_column_sups_theta` is required in
> either direction; `min(direct, envelope)` is the sound and preferred choice.

### Corrected 4b (theorem-backed monotonicity form)

> **4b'.** The **direct arc-cover sups** must be monotone in `theta`:
> `direct_column_sups_theta[k] >= direct_column_sups[k]` (pinned R2) for every
> block and `k`. This is the maximum-modulus statement — `|f_k|` is holomorphic
> on the closed enlarged disc by gate G1, so its boundary sup on `|u| = theta`
> dominates the sup on `|u| = 1` — and it is the property "a violation means the
> contour was not actually enlarged" was written to detect. It is invariant
> under the `rho`-sweep depth, so it is not confounded by the spec's own
> mandated `n`-sweep to 400. The like-for-like `selected` comparison (same
> deep-tail cutoff) is retained as a secondary diagnostic.

### 3.1 Evaluation of 4a' — PASS everywhere

Witness computed at 256 boundary points (512 for single-branch blocks), point
`s = 0.4252310423737965 + 4.345760788321986 i` (box centre, no half-width),
`abs_lower()` per point, `ctx.prec = 384`. `min_k selected/W_k` per receipt:

| receipt | 1→3,+2 | 1→3,−1 | 2→1 A2 | 2→3,+2 | 2→3,−1 | 3→2 A3 | 3→3,+2 | 3→3,−1 | violations |
|---|---|---|---|---|---|---|---|---|---|
| pinned R2 (`theta = 1`, baseline) | 1.0418 | 1.0377 | — | 1.0263 | 1.0275 | — | 1.0372 | 1.0330 | **0** |
| `THETA` (uniform 1.2) | 1.0467 | 1.0545 | 1.1291 | 1.0316 | 1.0337 | 1.0839 | 1.0424 | 1.0433 | **0** |
| `THETA1p230` (uniform 1.230) | 1.0484 | 1.0572 | 1.1318 | 1.0324 | 1.0347 | 1.0934 | 1.0430 | 1.0450 | **0** |
| `PERDISC` (1.84/1.30/1.23) | 1.0999 | 1.0925 | 1.1349 | 1.0342 | 1.0368 | 1.0934 | 1.0430 | 1.0450 | **0** |
| `THETAMAX_CONTROL` (1.2369074) | 1.0488 | 1.0578 | 1.1323 | 1.0326 | 1.0349 | 1.0957 | 1.0432 | 1.0454 | **0** |

That is 8 blocks x 17 `k` x 5 receipts = **680 comparisons, zero violations**.
Every element checked; none sampled.

The same run measures the direct arm's inflation, `direct/W_k` (pinned R2
baseline, `k = 0, 6, 10, 16`):

| block | k=0 | k=6 | k=10 | k=16 |
|---|---|---|---|---|
| `1→3, +2` | 1.042 | 195.2 | 3.51e4 | **7.47e7** |
| `1→3, −1` | 1.038 | 109.8 | 1.17e4 | 1.17e7 |
| `2→3, +2` | 1.026 | 1587 | 1.59e6 | 5.63e9 |
| `2→3, −1` | 1.028 | 104.3 | 1.77e4 | 3.64e7 |
| `3→3, +2` | 1.037 | 1.08e4 | 4.05e6 | 2.34e9 |
| `3→3, −1` | 1.033 | 22.3 | 969.5 | 2.59e5 |

`direct == selected` for every `k` below the wrapping knee and diverges from it
after; the wrapping diagnosis in `L_OUT_RECEIPT_SOL.md` §4.4 is **confirmed**.

### 3.2 Independent reproduction of the executor's baseline control

Pure JSON test against `lane_f/f8_receipts/Q8_R2_F1024_LOCAL_RECEIPT.json`,
comparing its own `selected_column_bounds` with its own `direct_column_sups`:

```text
1→3, +2, tail  first k with selected < direct: 7   sel/dir at k=10: 0.0882, k=16: 0.00071
1→3, −1, tail  first k: 7                          k=10: 0.0565,       k=16: 0.00037
2→3, +2, tail  first k: 9                          k=10: 0.5034,       k=16: 0.00850
2→3, −1, tail  first k: 8                          k=10: 0.1204,       k=16: 0.00092
3→3, +2, tail  first k: 10                         k=10: 0.8174,       k=16: 0.01957
3→3, −1, tail  first k: 7                          k=10: 0.0762,       k=16: 0.00055
```

First failing `k` = **7, 7, 9, 8, 10, 7** — exactly the executor's claim. The
pinned, certified R2 receipt fails condition 4a as written. **Claim CONFIRMED.**

### 3.3 Envelope preconditions (part of 4a')

Independent mpmath arm, 128 boundary points, branch sum to `n = 3000`:

| block | `C_theta` (1.2) | sampled `sup_z sum_n |w_n psi_n|/r_j` | `C >= sum` | `rho_theta` | `q` | `rho >= q` |
|---|---|---|---|---|---|---|
| `1→3, +2` | 7.844118469 | 7.343857623 | yes | 0.50249982 | 0.5 | yes |
| `1→3, −1` | 10.20060376 | 9.647342178 | yes | 0.56124661 | 0.5 | yes |
| `2→3, +2` | 1.868256749 | 1.831455607 | yes | 0.50249778 | 0.5 | yes |
| `2→3, −1` | 3.327872803 | 3.242136904 | yes | 0.50249778 | 0.5 | yes |
| `3→3, +2` | 1.768038552 | 1.717656903 | yes | 0.50249687 | 0.5 | yes |
| `3→3, −1` | 9.739242945 | 9.225993535 | yes | 0.75796407 | 0.5 | yes |

Same check on the per-disc receipt: `C >= sum` and `rho >= q` on all six tail
blocks. `A_theta >= W_0` is the `k = 0` column of §3.1 (ratios 1.026–1.135).
Independent `sup_{n,z} |u_n|` sampling (2048 points, `n` to 400) returns
0.4975 / 0.5611 / 0.8563 / 0.4975 / 0.4975 / **0.9470979422** / 0.4975 / 0.7579,
each covered by the corresponding recorded `rho_theta`. The mean-value
envelope's preconditions hold on every receipt.

### 3.4 Evaluation of 4b' — PASS everywhere

`min_k direct_column_sups_theta[k] / direct_column_sups[k]` (for the two
single-branch blocks the pinned receipt records no direct sups, so the pinned
envelope `W rho^k` is used as the baseline):

| receipt | 1→3,+2 | 1→3,−1 | A2 | 2→3,+2 | 2→3,−1 | A3 | 3→3,+2 | 3→3,−1 |
|---|---|---|---|---|---|---|---|---|
| `THETA` 1.2 | 1.7162 | 1.7900 | 2.0710 | 1.3229 | 1.3901 | 1.9881 | 1.3594 | 1.6058 |
| `THETA1p230` | 1.8650 | 1.9566 | 2.4373 | 1.3798 | 1.4611 | 2.2241 | 1.4236 | 1.7262 |
| `PERDISC` | 11.1619 | 13.0271 | 3.2450 | 1.5227 | 1.6416 | 2.2241 | 1.4236 | 1.7262 |
| `THETAMAX_CONTROL` | 1.9011 | 1.9972 | 2.5267 | 1.3933 | 1.4779 | 2.2827 | 1.4388 | 1.7552 |

All 8 blocks, all four receipts, minimum 1.3229. The contour was genuinely
enlarged, by the maximum-modulus-backed test.

The executor's two 4b arms are also reproduced exactly: production arm
`min_k selected_theta/selected_R2` = 0.2515 / 1.1669 / 2.0710 / 0.1945 /
**0.1831** / 1.9881 / 0.2017 / 1.6058 — 4 of 8 blocks below 1, min 0.183;
like-for-like (`selected_column_bounds_theta_tb_cutoff`) = 1.6681 / 1.7406 /
2.0710 / **1.2458** / 1.3404 / 1.9881 / 1.2682 / 1.6058 — 8/8 above 1, min
1.246. Both claims **CONFIRMED**, digit for digit.

### VERDICT ON 4b: the executor's diagnosis is **CORRECT**; the production arm
failure is an artifact of the spec's mandated `n`-sweep, not of the contour.
Under the corrected 4b' the receipts **PASS**.

### 3.5 Corrected condition 4 — overall **PASS** on all four L-OUT receipts.

---

## 4. Audit of the two spec-errata claims

### 4.1 `rho_theta(A3; theta = 1.2)` — executor CONFIRMED, referee REFUTED

Independent mpmath computation of `sup_{|z-c_3| = 1.2 r_3} |−1/(z+lambda) − c_2| / r_2`
over 2048 boundary points:

```text
block 3->2, n0=1, neg=False:  rho_sample = 0.9470979422
```

The receipt's arc-cover value 0.948043829806 covers it; both are far above the
referee's `rho_theta <= 0.87` claim at `theta = 1.2`
(`Q8_OUTPUT_TAIL_REFEREE.md:446-447`). The same sweep reproduces
`rho(A2) = 0.856311225466`. **Erratum CONFIRMED.** The referee's `0.87` is
wrong by roughly the entire margin to 1; the recommendation to pin `theta = 1.2`
survives on `rho < 1` (margin 0.052), but the quoted figure must not be relied
on.

Also reproduced independently, from geometry only: every G1 pole/branch-cut
margin in `L_OUT_RECEIPT_SOL.md` §4.2 (1.899818925, 1.741306257, 0.6564677476,
2.504226813, 1.963030712, 0.9277256948, 2.77548476, 1.468921795) and the worst
Hurwitz slope 0.51471863 at `theta = 1.2`. Condition 2 stands on my own numbers.

### 4.2 Certified `N = 262` and `a2 * b1 = 497.9` — CONFIRMED

Re-implemented the `hs` factors and the telescoping from the pinned R2 / TB / W
receipts using the **unmodified** `q8_schur_contour` formulas, and the
`tau_out` consumption from the L-OUT receipt fields, then substituted
`trace[X] -> trace[X] + tau_out[X]` in each of the six `trace[.]` slots at
`q8_schur_contour.py:351-358`:

```text
hs = {A2: 37.19007067693528, A3: 22.743685837096233, B1: 13.387099102591174,
      B2: 4.076406887775544, B3: 11.334579588543743}
a2*b1 = 497.86716178450257

theta = 1.2      full_tau(104) = 3.2208458e-3    first N with full_tau <= 1e-15: 262
                 (N=261 -> 1.19528308683e-15 ; N=262 -> 9.96069265240e-16)
theta = 1.230    first N: 238   (N=237 -> 1.03710385983e-15)
per-disc         first N: 237   (N=236 -> 1.07435791862e-15)

tau_out(104) trace, theta=1.2:  A2 2.5813720827e-6  A3 3.6218437100e-6
                                B1 7.2316058614e-7  B2 1.8083950460e-7
                                B3 1.1385445670e-6
dominant term  tau_out[A3]*a2*b1 = 1.8031970496e-3  of total 3.2208457514e-3
```

Every figure in `L_OUT_RECEIPT_SOL.md` §3, §3.1 and §4.5 is reproduced to all
printed digits. **Both errata CONFIRMED.** The `~N >= 200` figure in
`Q8_OUTPUT_TAIL_SOL.md` §3.2/§5.3 is a block-level estimate and understates the
telescoped requirement by ~3 orders / ~+37 steps.

---

## 5. Resulting L-OUT status

| # | Condition (corrected where noted) | Status | Evidence produced by this lane |
|---|---|---|---|
| 1 | `theta_i > 1` strictly, recorded exactly | **PASS** | `theta_exact_strings` read from all four receipts; `1.2 / 1.230 / (1.84,1.30,1.23) / 1.2369074` |
| 2 | G1 holomorphy at `theta_i r_i`, strictly positive pole clearance | **PASS** | §4.1: all 8 pole/branch margins and the worst slope 0.5147 < `a_0` recomputed from geometry |
| 3 | `rho_theta` reproduced by an independent Möbius/boundary computation, `n` swept to 400 | **PASS** | §3.3: independent 2048-point sweep, every receipt value covers it, all `< 1` at `theta = 1.2 / 1.230`; the `theta_max` control correctly gives `rho(A3) > 1` |
| 4a' | `selected_column_bounds_theta[k] >= witness`, envelope preconditions recorded | **PASS** | §3.1, §3.3: 680/680 comparisons, min ratio 1.026; `A`, `C`, `rho >= max(sup|u|, q)` all verified |
| 4b' | `direct_column_sups_theta[k] >= direct_column_sups[k]` (max modulus) | **PASS** | §3.4: 8/8 blocks x 4 receipts, min ratio 1.3229 |
| 5 | `output_projection_tail(N)` finite; `full_tau` by substitution into each `trace[.]` slot, `hs[.]` unchanged | **PASS as computed** (see caveat R1) | §4.2: telescoping re-implemented from the unmodified formulas; `input_tail_only` reproduced exactly |
| 6 | `N = 104` red-flag regression | **PASS** | §4.2: `full_tau(104) = 3.2208458e-3`, 2.5e9x the input tail; red flag not triggered |
| 7 | flip `full_tail_certified` only if 1–6 hold | **NOT SATISFIED AT THE CURRENT PIN** | 1–6 hold, but only at `N >= 262` (`theta = 1.2`) / `N >= 238` (`1.230`); the pinned `N = 104` misses the `1e-15` target by ~12 orders |

**Overall.** Condition 4 was the only thing standing between L-OUT and 7/7. On
the corrected reading it **passes**, so the computation delivered by the L-OUT
lane is sound and complete for what it set out to certify: with `theta = 1.2`
uniform and `N >= 262` (or `theta = 1.230` and `N >= 238`), the omitted-output
projection tail is bounded, certified, and telescopes to
`full_tau <= 1e-15`. The executor was right to refuse to waive the condition
itself and to route the ruling here.

**What does NOT follow.** L-OUT closes one gate of six. The **"Exact q=8
MMS-to-Hardy/Hilbert operator, basis and norm binding" remains separately
OPEN**, and every number above is conditional on it. Also still open: E1 on the
enlarged disc, `K_s` nonvanishing and word/lattice identification, the Selberg
determinant/zeta/scattering factorization, the four-edge winding, and the
independently-false `recorded_tail_checks_pass` gate. No theorem-grade claim is
created or strengthened by this adjudication.

**What a gate flip would additionally require** (out of scope for both the
compute lane and this one): re-pinning `N` from 104 to at least 262 in
`lane_f/q8_schur_contour.py`, which changes the pinned configuration and its
downstream cost, and is a lane_f authority decision.

### Residual items this lane flags (none affect the condition-4 ruling)

* **R1 — condition 5's substitution is asserted, not derived.** The referee's
  GAP 5 (the "i.e. (2.6)" level slip) is answered in `L_OUT_RECEIPT_SOL.md` §3
  by stating the per-slot substitution explicitly, which is what the spec asked
  for. This lane reproduced the arithmetic but did **not** re-derive that
  telescoping a Schur complement factor-by-factor with per-block defects
  `tau_in + tau_out` is valid. That derivation is the largest remaining
  soundness risk inside L-OUT, and it is not a condition-4 issue.
* **R2 — the adverse regression is a necessary condition only.** Its RHS sums
  rows `m` in `[N, 60)`. The report says so; keep it labelled that way.
* **R3 — shape inconsistency in the single-branch records.**
  `selected_column_bounds_theta` for A2/A3 equals the direct sups (the tighter
  arm), but `tau_out` consumes `W_theta * rho^k` (the envelope, the looser
  arm). Conservative, hence sound, but the array named "selected" is not the
  consumed object on those two blocks. Worth a one-line note in any future
  receipt schema.
* **R4 — the receipt is not hash-pinnable as emitted** (`runtime_seconds` in
  the hashed payload). Confirmed by inspection of the receipt keys. Drop that
  field before any `PINNED_RECEIPT_SHA256` entry.
* **R5 — `theta = 1.230` uniform is the better production pin** (N = 238 vs
  262) at a safer `rho` profile than per-disc, which drives the disc-1 tail
  family to `rho_theta = 0.99795` and A2 to 0.99824 (both reproduced here).
* **R6 — spec hygiene.** `Q8_OUTPUT_TAIL_REFEREE.md` §3.2's `rho <= 0.87` and
  §3.4 condition 4a should be corrected in place if that file is ever revised;
  as of this file, both are known-wrong and only this adjudication records it.

### State of the tree at adjudication time

`git status --porcelain research_notes/rh_goals_2026-08-14/lane_f
research_notes/rh_goals_2026-08-14/lane_g` returns empty (lane_f and lane_g
clean); `q8_schur_contour.py` still carries `"full_tail_certified": False`. The
L-OUT lane's "no lane_f edit" claim is confirmed.

---

**READY FOR JUDGING.**
