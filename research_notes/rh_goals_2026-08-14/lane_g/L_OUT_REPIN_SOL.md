# L-OUT re-pin — q=8 enlarged contour at theta = 1.230 uniform, N = 262

**Date** 2026-08-20 · **Lane** lane_g / l_out (compute) · **Branch**
`codex/prime-step-review-economic-validation` · **Status** receipts produced;
**no gate flipped**, no commit, no push.

This note re-pins the L-OUT enlarged-contour computation at the pin
`L_OUT_CONDITION4_ADJUDICATION.md` R5 recommends (`theta = 1.230` uniform),
evaluates the adjudication's **corrected** conditions 4a'/4b' alongside the
original ones, and evaluates the certified output-tail target
`full_tau <= 1e-15` honestly at `N = 262`.

**What is NOT claimed.** The separately-**OPEN** "Exact q=8 MMS-to-Hardy/Hilbert
operator, basis and norm binding" is not claimed, not addressed, and every
number below is conditional on it. No theorem-grade closure is created.
`lane_f/q8_schur_contour.py` still reads `"full_tail_certified": False` at line
395 and **no lane_f file was modified** (`git status --porcelain
research_notes/rh_goals_2026-08-14/lane_f` returns empty). Also untouched and
still open: E1 on the enlarged disc, `K_s` nonvanishing and word/lattice
identification, the Selberg determinant/zeta/scattering factorization, the
four-edge winding, and the independently-false `recorded_tail_checks_pass`
gate.

Interpreters: `/Users/za/.venvs/farey-rh/bin/python` (python-flint / Arb,
`ctx.prec = 384`) for everything certified;
`/Users/za/miniforge3/envs/pari-arb/bin/python3` (mpmath, 60 dps) for the
non-Arb cross-check only. Upper bounds are rounded UP, witnesses and margins
DOWN.

---

## 1. What changed since `L_OUT_RECEIPT_SOL.md`

| item | before | now |
|---|---|---|
| production `theta` | uniform `1.2` | **uniform `1.230`** (adjudication R5) |
| truncation `N` evaluated | 104 / 181 / 200 / 214 | 104 / 214 / 237 / **238** / **245** / 256 / 260 / **262** / 263 / 300 |
| `runtime_seconds` in hashed payload | yes — receipt not pinnable | **removed** (adjudication R4); hash now reproducible |
| condition 4 | original 4a/4b only, **FAIL** | originals **retained and still reported**, plus corrected **4a'/4b'** |
| condition 7 target | asserted, not evaluated per N | evaluated per `N` with a conservative interval test |
| adverse regression rows | 60, `N in {6,10,14}` | **120**, `N in {6,8,10,12,14,16}` (adjudication R2) |

`N = 262` was used as asked, a margin of **+24 steps** above the `N >= 238`
minimum that `theta = 1.230` requires. Runtime never became an issue (whole
programme under 90 s), so the fallback `N = 245` was not needed.

### 1.1 The R4 fix, and proof that it worked

`q8_r2out_local.py` now computes the runtime but keeps it **out** of the
receipt dict, reporting it on stdout only, and records
`"hashed_payload_excludes_wall_clock": true`. Two independent runs of the
generator produce a **byte-identical** receipt:

```
$ /Users/za/.venvs/farey-rh/bin/python q8_r2out_local.py --theta 1.230 \
    --M 512 --K-head 16 --n-sweep 400 \
    --out Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json
...
{
  "receipt": ".../l_out/Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json",
  "theta": ["1.230","1.230","1.230"],
  "sha256": "15f1603af9319ccef1ae7deb942e5cd946835472ef507dbe0bd8b0d2372054d5",
  "runtime_seconds_not_in_payload": 8.523861500001658
}

$ # second run, into a scratch path
{ ... "sha256": "15f1603af9319ccef1ae7deb942e5cd946835472ef507dbe0bd8b0d2372054d5",
      "runtime_seconds_not_in_payload": 8.527684582997608 }

$ diff <(json canonicalize repin) <(json canonicalize repeat) ; DIFF_EXIT=0
15f1603af9319ccef1ae7deb942e5cd946835472ef507dbe0bd8b0d2372054d5  Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json
15f1603af9319ccef1ae7deb942e5cd946835472ef507dbe0bd8b0d2372054d5  .../scratchpad/repeat.json
```

The receipt is now hash-pinnable. The four pre-existing L-OUT receipts were
left on disk untouched; the re-pin is a new file, so nothing was overwritten.

---

## 2. The re-pinned receipt (theta = 1.230 uniform)

```
$ cd research_notes/rh_goals_2026-08-14/lane_g/l_out
$ /Users/za/.venvs/farey-rh/bin/python q8_r2out_local.py --theta 1.230 \
    --M 512 --K-head 16 --n-sweep 400 --out Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json
L_OUT block=1→3, +2, tail A=[9.2880561896843944015 +/- 8.08e-21] C=[8.4853962039881394598 +/- 4.08e-20] rho_theta=[0.50249990433723938566 +/- 4.95e-21]
L_OUT block=1→3, −1, tail A=[12.249865202314346699 +/- 4.74e-19] C=[11.124401106861390700 +/- 2.14e-19] rho_theta=[0.57594670685159255475 +/- 4.18e-21]
L_OUT block=2→1, +1, head W_theta=[71.317529246890155407 +/- 9.39e-20] rho_theta=[0.89738296770057045638 +/- 1.89e-21]
L_OUT block=2→3, +2, tail A=[1.8014653605081847426 +/- 4.53e-20] C=[1.9313393189994449508 +/- 2.19e-20] rho_theta=[0.50249782689956301757 +/- 2.06e-21]
L_OUT block=2→3, −1, tail A=[3.4725855592666046369 +/- 4.84e-20] C=[3.4800683422704988954 +/- 4.80e-20] rho_theta=[0.50249782689956301757 +/- 2.06e-21]
L_OUT block=3→2, +1, head W_theta=[36.292994297299257603 +/- 1.76e-19] rho_theta=[0.99091814948302953778 +/- 1.31e-21]
L_OUT block=3→3, +2, tail A=[1.7151988045278146286 +/- 1.09e-20] C=[1.8326468519443317954 +/- 3.91e-20] rho_theta=[0.50249692070542789298 +/- 3.33e-21]
L_OUT block=3→3, −1, tail A=[10.133194647264454741 +/- 9.04e-20] C=[10.485676456213718092 +/- 2.94e-19] rho_theta=[0.77202897045583805912 +/- 1.76e-21]
```

Geometry is unchanged and unscaled (`c_j`, `r_j` from the pinned TB receipt);
only the arc cover moves, to radius `theta_i r_i`. Enlarged arc radii
`(0.97485290785, 0.55145808088, 0.66567120318)`.

**The one number the referee should look at twice.** The binding block `A3`
(`3→2, +1`) carries `rho_theta = 0.99091814948` at `theta = 1.230` (arc cover;
exact Möbius `0.98992276164`). It is strictly below 1, so condition 3 passes,
but the margin is **0.0091** — about a fifth of the margin at `theta = 1.2`
(`rho_theta(A3) = 0.94804`). This is the price of the 24-step saving in `N`,
and it is a real trade, not a free lunch. It is also why the per-disc option
stays rejected: it drives the disc-1 tail families to `0.99795`.

---

## 3. Per-condition table at the new pin — ORIGINAL conditions

```
$ /Users/za/.venvs/farey-rh/bin/python q8_lout_check.py \
    --lout Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json \
    --witness-points 512 --precondition-points 256 --precondition-nmax 2000 \
    --N-targets 104 214 237 238 245 256 260 262 263 300 \
    --out Q8_LOUT_CHECK_REPIN_THETA1p230.json
```

| # | Original condition | Verdict at the new pin |
|---|---|---|
| 1 | `theta_i > 1` strictly, recorded exactly | **PASS** — `theta_exact_strings = ["1.230","1.230","1.230"]`, `theta_uniform: true` |
| 2 | G1 holomorphy at `theta_i r_i`, pole clearance strictly positive | **PASS** — 8/8 recomputed by the checker; worst pole margin **0.6430175017** (`A2`), worst Hurwitz slope **0.5275865914** < `a_0 = 5` |
| 3 | `rho_theta` reproduced by the checker's own Möbius, `n` swept to 400 | **PASS** — 8/8 covered, agree to <= 0.101%, all `< 1`; tightest margin `A3` 0.0091 |
| 4 | Self-consistency (4a) and monotonicity in theta (4b) | **FAIL** — unchanged in character from the previous run; see below |
| 5 | `output_projection_tail(N)` finite; `full_tau` by substitution into each `trace[.]` slot, `hs[.]` unchanged | **PASS** — finite at all ten `N`; `input_tail_only` reproduced by the same telescoping |
| 6 | `N = 104` red-flag regression (`full_tau <= 1e-14` is a red flag) | **PASS** — `full_tau(104) = 6.96410381592e-4`, red flag NOT triggered, output term 5.5e8x the input term |
| 7 | Flip `full_tail_certified` only if 1–6 hold | **NOT SATISFIED** — because original 4 is FAIL |

Original condition 4 detail at the new pin (the originals are **retained in
the checker, not overwritten**; the primed variants were added alongside):

| block | 4a holds | first `k` sel<dir | 4b holds | `min_k` sel_theta/sel_R2 | like-for-like 4b | l4l min |
|---|---|---|---|---|---|---|
| `1→3, +2` | no | 6 | no | 0.272115495 | yes | 1.80595121 |
| `1→3, −1` | no | 6 | yes | 1.871916739 | yes | 1.89986621 |
| `2→1, +1` **A2** | yes | — | yes | 2.437298621 | yes | 2.43729862 |
| `2→3, +2` | no | 8 | no | 0.201080125 | yes | 1.28874064 |
| `2→3, −1` | no | 6 | no | 0.191468408 | yes | 1.40250955 |
| `3→2, +1` **A3** | yes | — | yes | 2.224123033 | yes | 2.22412303 |
| `3→3, +2` | no | 8 | no | 0.209125762 | yes | 1.31564491 |
| `3→3, −1` | no | 8 | yes | 1.726175694 | yes | 1.72617569 |

`baseline_control_pinned_R2_satisfies_4a: false` — the pinned, certified R2
receipt fails the identical test, exactly as before. The originals are reported
so the referee can see that nothing was quietly relaxed: **original condition 4
still FAILS at the new pin, and original condition 7 is still NOT SATISFIED.**

---

## 4. Per-condition table at the new pin — CORRECTED conditions 4a'/4b'

The corrected texts were transcribed from
`L_OUT_CONDITION4_ADJUDICATION.md` §"The corrected condition 4" into two **new**
checker sections, `condition_4a_prime_witness` and
`condition_4b_prime_max_modulus`, backed by a new module
`l_out/q8_lout_witness.py`. The original `condition_4_self_consistency` section
is byte-for-byte the same logic it was.

### 4a' — witness domination + envelope preconditions — **PASS**

`W_k := max over 512 boundary points z of |u| = theta of |f_k(z)|.lower()`,
evaluated at a **point** `z` (zero radius) and the **point**
`s = 0.4252310423737965 + 4.345760788321986 i` (box centre). Since
`W_k = |f_k(z_p)|.lower() <= |f_k(z_p)| <= sup_{|u|=theta}|f_k| = M_k(theta)`,
`W_k` is a rigorous lower-bound witness. The path does not reuse the receipt's
arc-cover enclosure: `z` is a point, so the `r_j^{-k}` binomial sum is
evaluated on points rather than on balls.

| block | `min_k` selected/`W_k` | `max_k` direct/`W_k` | violations | `A >= W_0` | `C >= sampled sum` | `rho >= sampled sup|u|` | `rho >= q` |
|---|---|---|---|---|---|---|---|
| `1→3, +2` | 1.04841217049 | 1.13e7 | none | yes | yes | yes | yes |
| `1→3, −1` | 1.05711350063 | 2.09e6 | none | yes | yes | yes | yes |
| `2→1, +1` **A2** | 1.13184294980 | 2.503 | none | yes | n/a | yes | n/a |
| `2→3, +2` | 1.03229230424 | 8.01e9 | none | yes | yes | yes | yes |
| `2→3, −1` | 1.03460687942 | 1.40e7 | none | yes | yes | yes | yes |
| `3→2, +1` **A3** | 1.09337322036 | 2.362 | none | yes | n/a | yes | n/a |
| `3→3, +2` | 1.04298578693 | 5.13e9 | none | yes | yes | yes | yes |
| `3→3, −1` | 1.04498573657 | 9.81e4 | none | yes | yes | yes | yes |

8 blocks x 17 `k` = **136 comparisons, zero violations**, every element
checked. The `min_k` column reproduces the adjudication's own `THETA1p230` row
(1.0484 / 1.0572 / 1.1318 / 1.0324 / 1.0347 / 1.0934 / 1.0430 / 1.0450) to four
digits from an independently written evaluator. The `max direct/W_k` column
re-confirms the interval-wrapping diagnosis: the direct arc-cover sup overshoots
a point witness by up to **8.0e9**, so `min(direct, envelope)` is picking the
envelope for good reason.

Precondition figures (`C_theta` recorded vs sampled sum; `rho_theta` recorded
vs sampled `sup|u|`), 256 boundary points, branch sum truncated at `n = 2000`:

| block | `C_theta` | sampled `sum_n |w_n psi_n|/r_j` | `rho_theta` | sampled `sup_{n,z}|u_n|` |
|---|---|---|---|---|
| `1→3, +2` | 8.48539620399 | 7.92907426060 | 0.502499904337 | 0.499500017619 |
| `1→3, −1` | 11.1244011069 | 10.4892867398 | 0.575946706852 | 0.575823861594 |
| `2→1, +1` | — | — | 0.897382967701 | 0.896514373048 |
| `2→3, +2` | 1.93133931900 | 1.89264384947 | 0.502497826900 | 0.499499986223 |
| `2→3, −1` | 3.48006834227 | 3.38639610945 | 0.502497826900 | 0.499500162947 |
| `3→2, +1` | — | — | 0.990918149483 | 0.989922761642 |
| `3→3, +2` | 1.83264685194 | 1.77854617109 | 0.502496920705 | 0.499500053447 |
| `3→3, −1` | 10.4856764562 | 9.90326436417 | 0.772028970456 | 0.771960476705 |

**Honest label, recorded in the JSON itself.** The `C` and `sup|u|` figures are
maxima over **sampled** boundary points with the branch sum **truncated** at
`n = 2000`, so each is a lower estimate of the true sup. `C_theta >= ...` and
`rho_theta >= ...` against them are **necessary conditions, not proofs of the
preconditions**. Only the `A >= W_0` leg and the witness domination itself are
element-complete.

### 4b' — max-modulus monotonicity of the DIRECT sups — **PASS**

`direct_column_sups_theta[k] >= direct_column_sups[k]` (pinned R2), every block,
every `k`. On the two single-branch blocks the pinned receipt records no direct
sups, so the pinned envelope `W rho^k` is the `theta = 1` baseline (the
adjudication's own convention).

| block | `min_k` direct_theta / direct_R2 | violations |
|---|---|---|
| `1→3, +2` | 1.86499900459 | none |
| `1→3, −1` | 1.95660901790 | none |
| `2→1, +1` | 2.43729862103 | none |
| `2→3, +2` | 1.37982127999 | none |
| `2→3, −1` | 1.46105382218 | none |
| `3→2, +1` | 2.22412303273 | none |
| `3→3, +2` | 1.42360407899 | none |
| `3→3, −1` | 1.72617569424 | none |

8/8, minimum ratio **1.3798**. Reproduces the adjudication's `THETA1p230` row
exactly. The contour was genuinely enlarged.

### Corrected conditions 1–6 at the new pin

`[true, true, true, true, true, true]` — `condition_4_prime_overall.pass = true`.

### Negative control — the corrected conditions still bite

Re-running the same corrected checker on the `theta_max = 1.2369074008682055`
control receipt gives corrected `[true, true, FALSE, true, true, true]` and
`c7' = false`: condition 3 refuses it because `rho_theta(A3) > 1`. So relaxing
4a to 4a' did **not** make the gate vacuous — the rate optimum is still
mechanically rejected. Report:
`Q8_LOUT_CHECK_REPIN_THETAMAX_CONTROL.json`.

---

## 5. Condition 7 evaluated honestly at N = 262

The checker now tests the target conservatively: the certified **upper
endpoint** of `full_tau` must sit strictly below the **lower endpoint** of the
`arb` representation of `1e-15` (1e-15 is not a binary dyadic, so it is itself
a ball).

```
L_OUT_CHECK N=104 input=[1.2647467e-12 +/- 2.13e-24] output=[0.00069641038 +/- 3.89e-16] full=[0.00069641038 +/- 3.58e-16]
L_OUT_CHECK N=214 input=[6.7377297e-30 +/- 4.96e-42] output=[1.1813511e-13 +/- 2.07e-25] full=[1.1813511e-13 +/- 2.07e-25]
L_OUT_CHECK N=237 input=[1.6480715e-33 +/- 9.55e-46] output=[1.0371039e-15 +/- 3.68e-27] full=[1.0371039e-15 +/- 3.68e-27]
L_OUT_CHECK N=238 input=[1.1480293e-33 +/- 4.65e-45] output=[8.4401336e-16 +/- 3.51e-28] full=[8.4401336e-16 +/- 3.51e-28]
L_OUT_CHECK N=245 input=[9.1367529e-35 +/- 1.17e-47] output=[1.9948934e-16 +/- 1.89e-28] full=[1.9948934e-16 +/- 1.89e-28]
L_OUT_CHECK N=256 input=[1.7121434e-36 +/- 8.89e-50] output=[2.0660326e-17 +/- 2.12e-29] full=[2.0660326e-17 +/- 2.12e-29]
L_OUT_CHECK N=260 input=[4.0313354e-37 +/- 1.30e-49] output=[9.0557508e-18 +/- 2.74e-30] full=[9.0557508e-18 +/- 2.74e-30]
L_OUT_CHECK N=262 input=[1.9561556e-37 +/- 4.02e-49] output=[5.9951138e-18 +/- 2.62e-30] full=[5.9951138e-18 +/- 2.62e-30]
L_OUT_CHECK N=263 input=[1.3626384e-37 +/- 2.25e-49] output=[4.8778549e-18 +/- 4.23e-30] full=[4.8778549e-18 +/- 4.23e-30]
L_OUT_CHECK N=300 input=[2.1112646e-43 +/- 4.46e-55] output=[2.3557588e-21 +/- 2.43e-33] full=[2.3557588e-21 +/- 2.43e-33]
```

| `N` | `input_tail_only` | `output_projection_tail` | `full_tau` | `full_tau <= 1e-15` |
|---|---|---|---|---|
| 104 | 1.26474668906e-12 | 6.96410380328e-4 | 6.96410381592e-4 | no |
| 214 | 6.73772969788e-30 | 1.18135107078e-13 | 1.18135107078e-13 | no |
| 237 | 1.64807151524e-33 | 1.03710385983e-15 | 1.03710385983e-15 | **no** |
| **238** | 1.14802929669e-33 | 8.44013360170e-16 | 8.44013360170e-16 | **yes** |
| 245 | 9.13675286237e-35 | 1.99489339788e-16 | 1.99489339788e-16 | yes |
| 256 | 1.71214340816e-36 | 2.06603255985e-17 | 2.06603255985e-17 | yes |
| 260 | 4.03133541887e-37 | 9.05575075254e-18 | 9.05575075254e-18 | yes |
| **262** | **1.95615556072e-37** | **5.99511380254e-18** | **5.99511380254e-18** | **yes** |
| 263 | 1.36263841652e-37 | 4.87785487612e-18 | 4.87785487612e-18 | yes |
| 300 | 2.11126459713e-43 | 2.35575878746e-21 | 2.35575878746e-21 | yes |

### The answer to the question asked

**At `N = 262`, `theta = 1.230` uniform, `full_tau <= 1e-15` HOLDS with the
interval upper bound.** The exact certified value, upper endpoint:

```
full_tau(262) = [5.99511380253738705057330e-18 +/- 2.18e-42]
```

i.e. `full_tau(262) <= 5.99511380253738705057331e-18`, which is
**1.67e2 times below** the `1e-15` target. The test
`full_tau.upper() < arb("1e-15").lower()` returns `true`.

The threshold itself is reproduced exactly: `N = 237` gives
`1.03710385983e-15` (above target), `N = 238` gives `8.44013360170e-16` (below).
That is the adjudication's `N >= 238` figure for `theta = 1.230`, digit for
digit, and `N = 262` carries **24 steps of margin** above it.

The **matched input-side pin** is like-for-like: `input_tail_only` at each `N`
comes from the **unmodified** `lane_f.q8_schur_contour.load_operator_bounds`
called at that same `N`, off the pinned R2/TB/W receipts with their pinned
sha256 checks intact. At `N = 262` it is `1.95615556072e-37`, i.e. **19 orders
below** the output term — the telescoped total is entirely output-dominated, as
expected.

**Condition 7 itself is still NOT flipped.** The checker's
`condition_7_full_tail_certified_corrected` block records
`conditions_1_to_6_corrected = [true,true,true,true,true,true]` and
`N_meeting_target = [238, 245, 256, 260, 262, 263, 300]`, and is explicitly
labelled `EVALUATION ONLY`. `lane_f` was not written to.

---

## 6. Adverse regression at the new pin — 30/30 hold, 120 rows

```
$ /Users/za/.venvs/farey-rh/bin/python q8_lout_adverse.py \
    --lout Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json \
    --N 6 8 10 12 14 16 --rows 120 --out Q8_LOUT_ADVERSE_REPIN_THETA1p230.json
ADVERSE N=6 A2 lhs=[26.814118 +/- 3.34e-7] rhs=[4.1012154 +/- 2.86e-8] holds=True
ADVERSE N=6 A3 lhs=[15.859124 +/- 2.92e-7] rhs=[2.4134113 +/- 2.93e-8] holds=True
ADVERSE N=6 B1 lhs=[7.4026790 +/- 2.22e-8] rhs=[0.53116841 +/- 3.57e-10] holds=True
ADVERSE N=6 B2 lhs=[1.6404850 +/- 9.45e-9] rhs=[0.018959274 +/- 4.95e-10] holds=True
ADVERSE N=6 B3 lhs=[4.5702222 +/- 5.62e-9] rhs=[0.23392027 +/- 3.12e-9] holds=True
ADVERSE N=8 A2 lhs=[17.847258 +/- 2.66e-8] rhs=[1.6901788 +/- 2.01e-8] holds=True
ADVERSE N=8 A3 lhs=[10.798606 +/- 1.48e-7] rhs=[1.0791937 +/- 3.61e-8] holds=True
ADVERSE N=8 B1 lhs=[5.7380946 +/- 4.27e-8] rhs=[0.11368642 +/- 1.23e-9] holds=True
ADVERSE N=8 B2 lhs=[1.1281274 +/- 3.01e-8] rhs=[0.0016191333 +/- 3.33e-11] holds=True
ADVERSE N=8 B3 lhs=[4.4518127 +/- 3.57e-8] rhs=[0.048535435 +/- 3.73e-10] holds=True
ADVERSE N=10 A2 lhs=[11.829885 +/- 3.72e-7] rhs=[0.65187694 +/- 2.95e-10] holds=True
ADVERSE N=10 A3 lhs=[7.2693549 +/- 1.28e-8] rhs=[0.48945274 +/- 4.24e-9] holds=True
ADVERSE N=10 B1 lhs=[5.6274291 +/- 5.96e-9] rhs=[0.020389705 +/- 2.07e-10] holds=True
ADVERSE N=10 B2 lhs=[0.84392876 +/- 4.56e-9] rhs=[0.00012073374 +/- 1.53e-12] holds=True
ADVERSE N=10 B3 lhs=[6.7493226 +/- 1.37e-8] rhs=[0.010217349 +/- 2.99e-10] holds=True
ADVERSE N=12 A2 lhs=[7.8319881 +/- 4.22e-8] rhs=[0.25874042 +/- 5.64e-10] holds=True
ADVERSE N=12 A3 lhs=[4.8760387 +/- 4.56e-8] rhs=[0.23590266 +/- 1.95e-9] holds=True
ADVERSE N=12 B1 lhs=[7.0587743 +/- 1.68e-8] rhs=[0.0034417228 +/- 2.43e-11] holds=True
ADVERSE N=12 B2 lhs=[0.75888748 +/- 1.51e-9] rhs=[8.9146612e-6 +/- 2.82e-14] holds=True
ADVERSE N=12 B3 lhs=[12.519226 +/- 3.04e-7] rhs=[0.0024776354 +/- 2.19e-11] holds=True
ADVERSE N=14 A2 lhs=[5.1813416 +/- 2.85e-8] rhs=[0.10945012 +/- 1.84e-9] holds=True
ADVERSE N=14 A3 lhs=[3.2581611 +/- 2.29e-8] rhs=[0.12037621 +/- 3.65e-9] holds=True
ADVERSE N=14 B1 lhs=[10.019958 +/- 1.46e-7] rhs=[0.00059629039 +/- 1.63e-12] holds=True
ADVERSE N=14 B2 lhs=[0.84631003 +/- 1.08e-9] rhs=[7.0911288e-7 +/- 3.81e-15] holds=True
ADVERSE N=14 B3 lhs=[24.460385 +/- 4.39e-7] rhs=[0.00068666094 +/- 2.28e-12] holds=True
ADVERSE N=16 A2 lhs=[3.4264645 +/- 4.54e-8] rhs=[0.049224464 +/- 1.31e-10] holds=True
ADVERSE N=16 A3 lhs=[2.1763209 +/- 2.52e-8] rhs=[0.064191013 +/- 3.74e-11] holds=True
ADVERSE N=16 B1 lhs=[14.917043 +/- 2.68e-7] rhs=[0.00011194419 +/- 3.28e-12] holds=True
ADVERSE N=16 B2 lhs=[1.0724472 +/- 4.54e-8] rhs=[6.2390509e-8 +/- 2.54e-16] holds=True
ADVERSE N=16 B3 lhs=[48.719355 +/- 4.41e-8] rhs=[0.00020712712 +/- 1.78e-12] holds=True
{"passed": 30, "total": 30, ...}
```

`T` is built by the **unmodified** `lane_f/q8_r3b_engine`
(`build_q8_block_matrices_and_s_derivative`, `sign = 1`, `n_head = 4`,
factors `("10","4","2")`) at the pin centre. Row count doubled from 60 to 120
per adjudication R2, and the `N` grid extended from 3 to 6 values (the ceiling
is `K_head + 1 = 17`). Margins run from **6.538x** (`N = 6`, `A2`) to
**1.719e7x** (`N = 16`, `B2`).

**The R2 caveat still stands and is still recorded in the JSON.** The RHS sums
rows `m` in `[N, 120)` only, so it is a lower bound on the true omitted-row mass
and a pass is a **necessary condition, not a proof of the bound**. One new
observation: the RHS values at 120 rows are identical to the 60-row values at
printed precision (e.g. `N = 6`, `A2`: 4.1012154 both times), so the row sum has
numerically saturated — the truncation is no longer where the slack is. That is
evidence, not a proof; the caveat's status is unchanged.

---

## 7. mpmath cross-check at the new pin

```
$ /Users/za/miniforge3/envs/pari-arb/bin/python3 q8_lout_crosscheck_mpmath.py \
    --lout Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json \
    --check Q8_LOUT_CHECK_REPIN_THETA1p230.json
rho_theta cross-check (mpmath exact Moebius vs Arb receipt):
  1→3, +2, tail      receipt=0.502499904337   mpmath=0.502499904337   rel_diff=1.85e-24
  1→3, −1, tail      receipt=0.575946706852   mpmath=0.575823861594   rel_diff=0.000213
  2→1, +1, head      receipt=0.897382967701   mpmath=0.896514373048   rel_diff=0.000969
  2→3, +2, tail      receipt=0.5024978269     mpmath=0.5024978269     rel_diff=1.85e-24
  2→3, −1, tail      receipt=0.5024978269     mpmath=0.5024978269     rel_diff=1.85e-24
  3→2, +1, head      receipt=0.990918149483   mpmath=0.989922761642   rel_diff=0.00101
  3→3, +2, tail      receipt=0.502496920705   mpmath=0.502496920705   rel_diff=1.85e-24
  3→3, −1, tail      receipt=0.772028970456   mpmath=0.771960476705   rel_diff=8.87e-5
  worst relative difference: 0.00101
full_tau cross-check (mpmath vs Arb checker):
  N=104  mpmath=0.0006964103816  arb=0.0006964103816  rel_diff=3.47e-13
  N=214  mpmath=1.181351071e-13  arb=1.181351071e-13  rel_diff=1.55e-12
  N=237  mpmath=1.03710386e-15   arb=1.03710386e-15   rel_diff=3.74e-12
  N=238  mpmath=8.440133602e-16  arb=8.440133602e-16  rel_diff=6.1e-13
  N=245  mpmath=1.994893398e-16  arb=1.994893398e-16  rel_diff=1.14e-12
  N=256  mpmath=2.06603256e-17   arb=2.06603256e-17   rel_diff=1.22e-12
  N=260  mpmath=9.055750753e-18  arb=9.055750753e-18  rel_diff=1.05e-13
  N=262  mpmath=5.995113803e-18  arb=5.995113803e-18  rel_diff=6.33e-13
  N=263  mpmath=4.877854876e-18  arb=4.877854876e-18  rel_diff=6.7e-13
  N=300  mpmath=2.355758787e-21  arb=2.355758787e-21  rel_diff=8.3e-13
smallest N with full_tau <= 1e-15 (mpmath, input tail bounded by 2.111e-43): 238
```

`full_tau` agrees to **1e-12 relative** at every `N`, and the crossing
`N = 238` is reproduced independently in a non-Arb arm. The `rho` differences
(<= 0.101%) are the arc-cover outer bound vs the exact Möbius image; the receipt
value is the larger, i.e. conservative, one in every case.

**One inherited imprecision, stated.** The crossing search in
`q8_lout_crosscheck_mpmath.py` adds `input_by_n[max(input_by_n)]` — the input
tail at the **largest** `N` in the grid (2.111e-43 at `N = 300`), which is the
smallest of them — rather than the input at the `N` being tested. It is
therefore slightly optimistic. It changes nothing here: at `N = 238` the true
input term is 1.148e-33, still **17 orders** below the output term
8.440e-16, so the crossing is unaffected. The Arb checker does not have this
imprecision — it uses the input at the matching `N`.

---

## 8. What a flip of `full_tail_certified` would STILL require

The gate is **not** flipped, and this lane does not recommend flipping it on
this receipt alone. Three things stand between these numbers and a flip:

1. **A referee pass on this receipt.** The corrected conditions 4a'/4b' come
   from `L_OUT_CONDITION4_ADJUDICATION.md`, which is itself awaiting judgment.
   This lane transcribed and evaluated them; it did not ratify them. The
   original conditions 4 and 7 still read FAIL / NOT SATISFIED at this pin, and
   that is reported above rather than suppressed.
2. **The R1 Schur-substitution derivation.** The adjudication's R1 flags the
   largest remaining soundness risk *inside* L-OUT: condition 5's per-slot
   substitution `trace[X] -> trace[X] + tau_out[X]` into the
   `q8_schur_contour.py:351-358` telescoping is **asserted, not derived**.
   Telescoping a Schur complement factor-by-factor with per-block defects
   `tau_in + tau_out` needs a proof that (2.6), a single-operator inequality,
   does not supply. This note reproduces the arithmetic; it does not close that
   gap. Until it is derived, every `full_tau` figure above is a computation
   under an unproven substitution.
3. **The separately-OPEN Hardy/Hilbert binding.** "Exact q=8 MMS-to-Hardy/Hilbert
   operator, basis and norm binding" remains OPEN and is **not claimed here**.
   Every number in this note is conditional on it.

Additionally, an actual flip means re-pinning `N` from 104 to at least 238 (262
on this receipt) inside `lane_f/q8_schur_contour.py`, which changes the pinned
configuration and its downstream cost. That is a **lane_f authority decision**
and out of scope for this compute lane.

Also unchanged and still open: E1 on the enlarged disc, `K_s` nonvanishing and
word/lattice identification, the Selberg determinant/zeta/scattering
factorization, the four-edge winding, and the independently-false
`recorded_tail_checks_pass` gate. L-OUT closes at most one gate of six, and it
closes none today.

### Residual notes from this lane

* **R3 is unfixed and inherited.** On the two single-branch blocks
  `selected_column_bounds_theta` equals the direct sups while `tau_out` consumes
  the envelope `W_theta rho^k`. Conservative, hence sound, but the array named
  "selected" is still not the consumed object there. A schema fix, not a
  soundness one; not attempted here.
* **The `A3` margin is the new pin's weak point.** `rho_theta(A3) = 0.99092`
  (0.98992 exact Möbius). Condition 3 passes with margin 0.0091. If any future
  revision moves the geometry, this is the first thing that breaks.
* **The precondition checks are sampled**, per §4a' above. Element-complete
  verification of `C_theta` and `rho_theta` as sups would need an arc-cover
  argument on those two quantities, which this lane did not build.

---

## 9. Artifacts

All under `research_notes/rh_goals_2026-08-14/lane_g/l_out/`. Nothing was
committed or pushed; the four pre-existing L-OUT receipts were not overwritten.

| file | sha256 | role |
|---|---|---|
| `Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json` | `15f1603af9319ccef1ae7deb942e5cd946835472ef507dbe0bd8b0d2372054d5` | **re-pinned receipt**, theta = 1.230 uniform, hash-reproducible |
| `Q8_LOUT_CHECK_REPIN_THETA1p230.json` | `08722fdd60348a2278eb4bd71df41a4705c08cad4967b2b41effd4da27aab319` | checker report: original 1–7 + corrected 4a'/4b'/7 |
| `Q8_LOUT_ADVERSE_REPIN_THETA1p230.json` | `422e5d1c3d7245f955b166f2e9060f00d8bd0495e1f44007a02384953a59d099` | adverse regression, 120 rows, 30/30 |
| `Q8_LOUT_CHECK_REPIN_THETAMAX_CONTROL.json` | `163bf7d5096ea1a68e5a14f128251c40f8f7a84adeae23b226670375c65f4b4f` | negative control, corrected conditions still FAIL |
| `q8_lout_witness.py` | `fa0ef8f2819500009d7c54598f6a1371f81515dbbd546fad86d2909c5bd96262` | **new** — witness + precondition evaluator for 4a' |

Modified (lane_g only): `q8_r2out_local.py` (R4 fix — wall clock out of the
hashed payload), `q8_lout_check.py` (corrected 4a'/4b' **added** alongside the
originals, per-`N` target test, corrected condition 7 section).

`git status --porcelain research_notes/rh_goals_2026-08-14/lane_f` → empty.
`q8_schur_contour.py:395` → `"full_tail_certified": False`.

---

**READY FOR JUDGING.**
