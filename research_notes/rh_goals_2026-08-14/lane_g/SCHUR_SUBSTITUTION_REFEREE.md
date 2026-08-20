# Referee — Schur substitution derivation (residual R1)

**Date** 2026-08-20 · **Target**
`lane_g/SCHUR_SUBSTITUTION_DERIVATION_SOL.md` (commit `a5d9adc`, 514 lines,
1 file, 0 other files touched) · **Referee mode** cold: no shared context with
the author lane, no file edited, no commit, no push. This file is the only new
artifact. `lane_g/l_out/` was not read as a work product and is not graded.

**Interpreter** `/Users/za/.venvs/farey-rh/bin/python` (python-flint 0.9.0 /
Arb, `ctx.prec = 400`; mpmath 1.4.1 at 40–50 dps). Referee scripts live in the
session scratchpad, not in the repo.

---

## 0. House verdict

### **CONFIRMED**

Every load-bearing claim of the target note reproduced independently. The
telescoping identity is exact (residual `1.4e-40` at working precision, not a
truncation); the six code slots are in correct, order-sensitive bijection with
the six telescoping terms; each slot's norm bookkeeping is individually valid,
not merely valid in the sum; hypothesis (iv) is confirmed against the code and
is confirmed load-bearing far more strongly than the note claims; the full
`5.2` and `5.4` numeric tables reproduce to every displayed digit from a script
written from scratch.

Six minor defects (M1–M6) are recorded in §8. **None** touches soundness; all
are documentation or receipt-hygiene items. No defect refutes the verdict
`PROVED`, and the note's scope statement holds.

| attack | verdict |
|---|---|
| 1 — re-derive the identity; resolvent-shape hole | **NO HOLE.** `C` is a plain polynomial; the suspected `(I-K)^{-1}` shape is absent |
| 2 — per-slot op/trace bookkeeping | **CORRECT.** All six slots verified individually on real q8 data |
| 3 — `hs[.]` complete `k`-sums, no hidden `N` | **CONFIRMED.** `hs` bit-identical across `N = 6…1000` |
| 4 — independent numerics | **REPRODUCED.** 18/18 configs, 8/8 Arb, counterexample confirmed and strengthened |
| 5 — latent `Xop`/`b3` gap | **CORRECTLY CLASSIFIED.** No live path commits the unsoundness |
| 6 — scope / LEDGER RULE | **COMPLIANT**, with one stale self-description (M6) |

---

## 1. Attack 1 — the identity, re-derived from the code's actual object

### 1.1 The suspected hole is not there

The attack brief's leading hypothesis was that the checker's object is
resolvent-shaped, so plain telescoping would not apply. It is not.
`q8_r3b_engine.py:143-158` returns **exactly five** nonzero blocks, keyed
`(output_disc, input_disc)`:

```text
(2,1)=A2, (3,2)=A3, (1,3)=B1, (2,3)=B2, (3,3)=B3
```

so `L = [[0,0,B1],[A2,0,B2],[0,A3,B3]]`. Re-deriving the elimination myself
(not reading the note's version): with `M = [[I,0],[-A2,I]]`, `det M = 1`,
`M^{-1} = [[I,0],[A2,I]]`, the Schur complement of the leading `2x2` block of
`I - L` is

```text
(I - B3) - [0,-A3] M^{-1} [-B1; -B2] = I - (B3 + A3 B2 + A3 A2 B1) .
```

The nilpotent `A`-corner is what makes this a **polynomial**, not a Neumann
series: no `(I-K)^{-1}` appears, so plain ring telescoping is licensed.
`schur_value_and_derivative` (`q8_schur_contour.py:190-194`) forms exactly
`b3 + a3*b2 + (a3*a2)*b1`.

**Receipt** (`ref_id.py`, 500 random `4x4` block quintuples):

```text
max |det(I-L) - det(I-C)|  over 500 quintuples          = 1.12e-15   (= 0, fp noise)
min |det(I-L) - det(I-Cbad)|, Cbad = B3+A3B2+A2A3B1     = 3.27e-3    (genuinely wrong)
```

The `A2 A3` control is the point: the identity is **order-sensitive**, so the
six-slot bijection is a real constraint and not an accidental symmetry.

### 1.2 The telescoping is exact, verified on the live blocks

Not the idealised `ABC`: the actual q8 blocks at production factors
`("10","4","2")`, `sign = 1`, `n_head = 4`.

```text
max_{i,j} | sum(6 slots) - (C - C_N) |
  s = 0.42523104+4.34576079i, N=6/M=18 : 1.37e-40
  s = 0.42523104+4.34576079i, N=8/M=24 : 1.66e-40
  s = 0.05+8.0i,              N=6/M=18 : 6.74e-39
  s = 0.05+8.0i,              N=8/M=24 : 3.98e-38
```

at 40 dps. Exact to working precision. **PASS.** No cross term is dropped, and
no second-order remainder is present to drop — the note's §3.1 reading (the
untruncated right factors absorb `Delta_A Delta_B` and the cubic term) is
correct.

### 1.3 The 6-slot bijection, line by line

`q8_schur_contour.py:351-358` re-read directly:

| line | code | telescoping term | referee verdict |
|---|---|---|---|
| 352 | `trace["B3"]` | `Delta_B3` | ✓ |
| 353 | `a3 * trace["B2"]` | `A3_N Delta_B2` | ✓ |
| 354 | `a3 * a2 * trace["B1"]` | `A3_N A2_N Delta_B1` | ✓ |
| 355 | `trace["A3"] * b2` | `Delta_A3 B2` | ✓ |
| 356 | `trace["A3"] * a2 * b1` | `Delta_A3 A2 B1` | ✓ |
| 357 | `a3 * trace["A2"] * b1` | `A3_N Delta_A2 B1` | ✓ |

Six slots, six terms, bijective, correctly ordered. `b3` appears **only** in
`xop` (`:350`) and never in `input_tail_only` — correct, since `B3` enters the
telescoping only through `Delta_B3` and needs no operator-norm coefficient.
The note's Theorem S correctly lists (H1) over `{A2,A3,B1,B2}` only.

---

## 2. Attack 2 — norm bookkeeping, slot by slot

The summed inequality can pass while an individual slot is mis-normed (a
loose slot masking a tight wrong one). I therefore tested **each slot
separately**, computing the true trace norm of the operator in that slot
against the coefficient the code assigns it.

`ref_id.py`, exact singular values at 40 dps, `d_X = ||X_M - X_N||_1`,
`h_X = ||X_M||_op`:

```text
s = 0.42523104+4.34576079i, N = 6 / M = 18
   Delta_B3           ||T||_1 = 0.31701358     bound = 0.31701358     ok
   A3N.Delta_B2       ||T||_1 = 0.00044293337  bound = 0.1492237      ok
   A3N.A2N.Delta_B1   ||T||_1 = 0.00031086458  bound = 43.387641      ok
   Delta_A3.B2        ||T||_1 = 1.4339767      bound = 4.2263893      ok
   Delta_A3.A2.B1     ||T||_1 = 16.343181      bound = 117.59997      ok
   A3N.Delta_A2.B1    ||T||_1 = 5.0625743e-6   bound = 112.98546      ok
```

Same, all six ok, at `(s,N) = (0.42523104+4.34576079i, 8)`,
`(0.05+8.0i, 6)`, `(0.05+8.0i, 8)` — 24 individual slot checks, 0 failures.
Note `Delta_B3` is **tight** (equality), which is the correct signature: that
slot carries no operator-norm coefficient at all.

**Audit of which norm sits where.** Each slot has the shape `X (Delta) Y` with
the `Delta` in `||.||_1` and the outer factors in `||.||_op` via
`||X T Y||_1 <= ||X||_op ||T||_1 ||Y||_op`. No slot uses an operator norm on a
`Delta` or a trace norm on an outer factor; no pair is swapped. The one place
a swap would be invisible in the sum — slot 355 (`d_A3 * h_B2`, `Delta` on the
**left**) vs slot 353 (`h_A3 * d_B2`, `Delta` on the **right**) — is exactly
the asymmetry the strawman-A control detects (§4.2). **PASS.**

The `op <= HS` consumption of `hs[.]` (N3) is the conservative direction.
`||C-C_N||_1 >= ||C-C_N||_op` for the operator-norm consumer at `:488` is also
conservative. **Direction PASS.**

---

## 3. Attack 3 — hypothesis (iv) against the code

Two questions: (a) are the `hs[.]` formulas complete `k`-sums, and (b) is there
hidden `N` dependence, including through cached arrays sized by `N`?

### 3.1 Static read

* `block_hilbert_tail_bound(row)` (`:224-239`) — **takes no `N` argument.**
  Sums `sel_k^2` for `k < K` plus the closed-form envelope tail
  `2A^2 q^{2K}/(1-q^2) + 2C^2 sum_{k>=K} k^2 rho^{2k-2}` over **all** `k >= K`.
  I verified the envelope algebra: `(A q^k + C k rho^{k-1})^2 <= 2A^2 q^{2k} +
  2C^2 k^2 rho^{2k-2}`, and `sum_{k>=K} 2A^2 q^{2k} = 2A^2 q^{2K}/(1-q^2)`,
  matching `sum_k2_rho_tail` for the second piece. Complete infinite sum. ✓
* `hs[name]` for single blocks (`:332`) — `weight / sqrt(1 - rho^2)`
  `= sqrt(sum_{k>=0} (w rho^k)^2)`. No `N`. ✓
* `K = len(row["selected_column_bounds"])` comes from the **hash-pinned** R2
  receipt (`PINNED_RECEIPT_SHA256["R2"]`), not from `N`. Measured `K = 17` for
  every tail block, against a production `DEFAULT_N = 104`. No coupling. ✓

### 3.2 Dynamic receipt — the decisive test

I called `load_operator_bounds` on the real pinned receipts at five widely
separated `N` and compared the outputs bit for bit:

```text
hs  identical across N in {6, 40, 104, 262, 1000}:  True
Xop identical across N in {6, 40, 104, 262, 1000}:  True

hs @ N=6    = {A2: [37.19007067693527747215676 +/- 1.22e-24],
               A3: [22.74368583709623423601011 +/- 9.88e-25],
               B1: [13.38709910259117365477485 +/- 4.05e-25],
               B2: [4.076406887775543839726626 +/- 3.57e-25],
               B3: [11.33457958854374242599595 +/- 3.21e-24]}
hs @ N=1000 = identical, to the last recorded digit and radius

trace @ N=6    B3 = [21.9108940138 +/- 2.57e-11]      (varies with N, as it must)
trace @ N=104  B3 = [3.04840229158e-15 +/- 3.84e-27]
trace @ N=1000 B3 = [3.57565327488e-169 +/- 3.48e-181]
```

`hs` is **`N`-invariant**; `trace` is not. **The claim in §4.1 of the note is
confirmed, and by a stronger method than the note used.** No cached array,
no receipt field, no code path introduces an `N`-cut into `hs`.

### 3.3 Does `hs[.]` bound the TRUE block, including omitted OUTPUT rows?

This is the substantive half of (iv), and the note leans on
`Q8_OUTPUT_TAIL_SOL.md` §1.3 for it. I re-verified the generator rather than
the doc:

* **Tail families** (`q8_r2_local.py:186-206`). `direct_sups[k]` is the sup of
  the column **function** `(T e_{j,k})(z)` over the arc cover `arcs[i-1]` of
  the boundary of the **output** disc `i`, and `selected_column_bounds[k] =
  min(direct_sups[k], tail_envelope(A,C,q,rho,k))`. Being a boundary sup on
  the output disc, Parseval in the output coordinate gives
  `sum_{m>=0} |T[m,k]|^2 <= sel_k^2` — the sum over **all** rows `m`, omitted
  rows included. ✓
* **Single branches** (`q8_r2_local.py:180-183`, `q8_weight_support.py:127`).
  `plain_weight_sup_upper_bound = weight_sup(arcs[i-1], ...)` — again a sup on
  the **output**-disc arc cover — and `low_bounds = weight * rho^k` with `rho`
  the TB image-ratio sup. Same Parseval conclusion. ✓

So `hs[X] >= ||X||_HS >= ||X||_op` for the **true, untruncated,
un-row-truncated** block, which is the side (H1) demands. **PASS.**

*Inherited caveat, correctly declared by the note:* Parseval on the boundary
needs the column function holomorphic on a neighbourhood of the closed output
disc — gate G1, adjudication condition 2 (**PASS**). And the arc cover is a
ball-arithmetic cover, sound but inherited from the pinned receipts. The note
declares both as inherited and does not re-derive them; that is the correct
posture and I did not re-derive them either.

---

## 4. Attack 4 — independent numerics

Written from scratch (`ref_num.py`, `ref_arb.py`, `ref_cex.py`, `ref_id.py`);
the author's scripts were never read.

### 4.1 Main arm — 18 configurations, exact singular values, 50 dps

`LHS = ||C_M - C_N||_1`, `RHS` = (S) with `d_X = ||X_M - X_N||_1`,
`h_X = ||X_M||_op`, `M = 3N`, blocks from unmodified
`lane_f/q8_r3b_engine.py`.

```text
s                          N/M    corner  LHS           RHS           ratio    strawA   strawB
0.42523104+4.34576079i     6/18   0.0     17.359791     278.6657      16.052   2.5262   15.018
0.42523104+4.34576079i     8/24   0.0     10.512898     112.05262     10.659   0.89528  10.591
0.42523104+4.34576079i     10/30  0.0     5.4987797     45.691119      8.3093  0.31151   8.3055
0.42523104+0.5i            6/18   0.0     0.11400894    0.9212154      8.0802  0.86631   8.0794
0.42523104+0.5i            8/24   0.0     0.036615496   0.51418102    14.043   0.87721  14.043
0.42523104+0.5i           10/30   0.0     0.012609652   0.29802142    23.634   0.88732  23.634
0.1+1.0i                   6/18   0.0     0.16124124    1.0580744      6.5621  0.89814   6.5614
0.1+1.0i                   8/24   0.0     0.052437731   0.55669556    10.616   0.89602  10.616
0.1+1.0i                  10/30   0.0     0.018137156   0.31045662    17.117   0.90107  17.117
0.9+0.2i                   6/18   0.0     0.068070297   0.4680277      6.8757  0.58412   6.8731
0.9+0.2i                   8/24   0.0     0.024825687   0.27093344    10.913   0.59475  10.913
0.9+0.2i                  10/30   0.0     0.0093038547  0.16007874    17.206   0.62069  17.206
0.05+8.0i (adverse)        6/18   0.0     7591.0628     2204995.3    290.47   71.106   141.24
0.05+8.0i                  8/24   0.0     7146.2819     1271966.6    177.99   32.051   148.7
0.05+8.0i                 10/30   0.0     5978.633      596144.61     99.713  11.803    96.516
0.75+12.5i (adverse)       6/18   0.0     110479.43     2.9761293e9 26938.0  7997.4   1509.1
0.75+12.5i                 8/24   0.0     150949.98     2.5998308e9 17223.0  4423.8   4542.5
0.75+12.5i                10/30   0.0     155760.45     1.930651e9  12395.0  2516.6   7290.4
```

**18/18 pass, 0 violations, min ratio 6.5621.** This reproduces **every**
number in the note's §5.2 table to every displayed digit (`17.359791` /
`278.66569` / `16.05`; `5.4987797` / `45.691119` / `8.309`; `0.16124124` /
`1.0580744` / `6.562`; `155760.45` / `1.930651e9` / `12395`; …). Includes
two adverse `s`-points as required.

`corner = 0.0` at all 18 — `X_N` is literally the top-left corner of `X_M`,
confirming §5.1 and the `X_N = P_N X P_N` reading of (1.2). Independently
confirmed.

*Reproducibility trap the note steps into (M2):* §5.2 states factors
`("10","4","2")` but does not say these are `RECEIPT_FACTORS`, not the engine
default `EXACT_FACTORS = ('3.4','2.2','1.4')`. My first run used the default
and produced a completely different table (pin 6/18: LHS `1.764`, RHS `8.66`,
ratio `4.91`; min ratio over 18 = `3.85`). **All 18 still passed** and the
strawman still failed at exactly 10 points, so the verdict is robust to the
geometry — but a reader following the note literally will not reproduce the
table. Worth one clause.

### 4.2 Test power — strawman A (3-term)

Dropping the two `Delta_A`-side terms: **min ratio 0.31151**, matching the
note's `0.3115` exactly.

**Discrepancy (M1):** I count **11 of 18** violated points, not the note's
"10 of 18". Violating rows: 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 (the note
appears to have missed row 10, ratio `0.99869` in the default-factor run /
`0.58412` here). The note **under**-states its own test power; direction is
harmless, but the receipt is off by one.

### 4.3 The counterexample — hypothesis (iv) is load-bearing

Independent randomized search (`ref_cex.py`, `3x3` complex Gaussian block
quintuples, `rank(P) = 1`, seed 20260820, **200 000 trials**):

```text
true-coefficient (H1) violations       : 0        / 200000
truncated-coefficient violations       : 27840    / 200000   (13.9%)
min truncated-coefficient ratio        : 0.21708
```

The note reports a single counterexample at ratio `0.91097`. I find the
failure set has **positive measure** — 13.9% of random draws — with a worst
ratio of `0.217`, i.e. the bound can be violated by a factor of **4.6x**, not
`1.1x`. **Hypothesis (iv) is confirmed load-bearing, and materially more so
than the note claims.** Correspondingly, 0/200 000 violations under (H1) is
strong independent support for Theorem S itself.

On the actual q8 blocks, strawman B does not fail (my min ratio `6.5614` vs
the note's `6.561` — reproduced): the q8 blocks are too diagonally
concentrated for the numerics to detect the difference. The note's conclusion
— that (iv) can only be settled by reading the code, which is why §4 is the
substantive section — is correct, and §3 above is my independent discharge of
it.

### 4.4 Rigorous Arb arm — 8/8

Both sides deliberately biased against the claim: `LHS` over-estimated by the
rank-one column bound `||Y||_1 <= sum_j ||Y e_j||_2`; `RHS` under-estimated by
`d_X -> ||Delta_X||_F` and `h_X -> max_j ||X e_j||_2`. Both biases verified in
the correct direction before use. Arb enclosures only, no float step:

```text
s                        N/M    LHS_upper                       RHS_lower                     pass
0.42523104+4.34576079i   6/18   [20.53692086 +/- 1.36e-9]       [194.2265009 +/- 4.90e-8]     True
0.42523104+4.34576079i   8/24   [12.48355861 +/- 4.68e-9]       [76.27955004 +/- 1.38e-9]     True
0.42523104+0.5i          6/18   [0.1632644494 +/- 1.79e-11]     [0.5205803163 +/- 2.02e-11]   True
0.42523104+0.5i          8/24   [0.05529972754 +/- 3.96e-12]    [0.2923510095 +/- 3.53e-11]   True
0.1+1.0i                 6/18   [0.2307870971 +/- 3.93e-11]     [0.5892499985 +/- 1.53e-11]   True
0.1+1.0i                 8/24   [0.07821965076 +/- 3.32e-12]    [0.3122063661 +/- 4.53e-11]   True
0.9+0.2i                 6/18   [0.1013909548 +/- 1.92e-11]     [0.2946505137 +/- 1.41e-11]   True
0.9+0.2i                 8/24   [0.03967717208 +/- 2.59e-12]    [0.1723266210 +/- 4.29e-11]   True
```

**8/8**, midpoints matching the note's §5.4 table to every displayed digit.
The stricter-test-implies-true-inequality logic is valid.

---

## 5. Attack 5 — the `Xop` / `b3` flag: is any live path already unsound?

`Xop` is read at exactly two places (full grep of `q8_schur_contour.py`):

```text
:488   inv_tilde = (arb(1) + bounds["Xop"] * inv_arc).upper()
:478   record["Xop_upper"] = arb_text(bounds["Xop"])          # reporting only
```

At `:488` `Xop` is consumed as an **operator**-norm bound of `C_N`, which is
what `b3 + a3*b2 + a3*a2*b1` legitimately is: `||B3_N||_op <= ||B3||_op <=
||B3||_HS <= b3` by (N3) and Lemma 2.2, and likewise for the products. The
resolvent identity `(I-C_N)^{-1} = I + C_N (I-C_N)^{-1}` then gives
`inv_tilde >= ||(I-C_N)^{-1}||` given `inv_arc >= ||(I-C_N)^{-1}||`. **Sound.**

The only trace-norm-flavoured consumer is gated:

```text
:490   if bounds["full_tail_certified"] and bounds["full_tau"] is not None:
:491       tail_homotopy = (bounds["full_tau"] * inv_tilde).upper()
:395   "full_tail_certified": False,           # hard-coded
:394   "full_tau": None,
```

I confirmed at runtime on the real pinned receipts, at all five `N` tested:
`full_tail_certified = False`, `full_tau = None`. And `:785-788` folds
`not full_tail_certified` into `unresolved`, so no run can report a resolved
status while the gate is inert.

**Verdict: the flag is correctly classified as LATENT. No live code path
commits the flagged unsoundness.** The note's §6.2 analysis is also correct on
the mathematics — `||B3||_1` is genuinely not dominated by `||B3||_HS`, while
the product terms `||A3 B2||_1 <= ||A3||_HS ||B2||_HS` survive by Hölder. R1-b
is a real, correctly-scoped warning for the Simon-type determinant-difference
route.

---

## 6. Attack 6 — scope and LEDGER RULE

| requirement | evidence | verdict |
|---|---|---|
| remains conditional on the OPEN Hardy/Hilbert binding | §0 row 4 and §4.2 mark H0 **CONJECTURAL, inherited**; §7 repeats it. Matches `L_OUT_CONDITION4_ADJUDICATION.md:361-367` verbatim in substance | ✓ |
| claims no theorem-grade q8 closure | §7 scope statement enumerates `full_tail_certified = False`, the `N = 104` / `1e-15` miss, E1, `K_s`, Selberg factorization, four-edge winding, `recorded_tail_checks_pass` — I cross-checked this list against the adjudication's own OPEN list; it is complete and nothing is softened | ✓ |
| no restatement stronger than the most-caveated source | the `PROVED` verdict is scoped to *the substitution*, never to the gate or to q8 | ✓ |
| read-only on the work product | `git status --porcelain` shows **0** modified tracked files; `git show --stat a5d9adc` = 1 file changed, 514 insertions, 0 deletions | ✓ |
| no out-of-scope diff | same receipt: the commit touches only `SCHUR_SUBSTITUTION_DERIVATION_SOL.md`. No drive-by edits, nothing deleted | ✓ |
| `lane_g/l_out/` untouched by the author | not modified in `a5d9adc`; not read or graded by this referee | ✓ |

The note's claim that no prior lane_g document states which side of the
truncation `hs[.]` must bound: **verified.** `grep -n "untruncated\|true
block\|infinite block"` over `Q8_OUTPUT_TAIL_SOL.md`,
`Q8_OUTPUT_TAIL_REFEREE.md`, `L_OUT_RECEIPT_SOL.md` returns nothing. R1-a is a
genuine undocumented invariant and the recommendation is sound.

---

## 7. One clarification the note earns but does not quite state (M3)

`input_tail_only` as computed **today** substitutes `trace[X] = tau_in(X)`
only — a bound on `||X (I - P_N)||_1`, not on `||X - P_N X P_N||_1`. Under
hypothesis (H2) it is therefore **not** a bound on `||C - C_N||_1`; only the
prospective `full_tau` (with `tau_in + tau_out`) is. The note is technically
correct throughout (§1.4 states (S) "with `trace[X] -> d_X`", §3.4 handles the
substitution, §6.1 notes the gate is inert), but the §0 verdict table row 1
reads "the six-term telescoped substitution **as implemented** … PROVED",
which a §0-only reader can over-read as certifying the live number. What is
proved is the **shape**; the live inputs are known-insufficient by design and
the gate is correctly held shut. One clause in §0 row 1 would close this.

Grading strict, this is an ambiguity in the verdict-table wording, **not** a
false claim — the body disambiguates it three times. It does not move the
house verdict.

---

## 8. Defect list

| # | defect | where | severity | why the author likely missed it |
|---|---|---|---|---|
| M1 | strawman A is violated at **11** of 18 points, not 10 (min `0.3115` correct) | §5.3 bullet 1 | cosmetic; under-states own test power | off-by-one in a hand count of a printed table |
| M2 | `factors = ("10","4","2")` is `RECEIPT_FACTORS`, **not** the engine default `EXACT_FACTORS = ('3.4','2.2','1.4')`; a reader using the default reproduces a different table | §5 preamble | reproducibility | author had the constant in context and did not notice the default differs |
| M3 | §0 row 1 "as implemented … PROVED" can be over-read as certifying the live `input_tail_only`, which is `tau_in` only | §0 | wording | body disambiguates it, so the summary line was not re-read against a cold reader |
| M4 | §4.1 cites `Q8_OUTPUT_TAIL_SOL.md:186` (2.3) "at `theta = 1`" for the full-column Parseval step; the direct statement is §1.3, and (2.3) is derived by *dropping* `m < N` terms — sound either way, but the cited line is not the cleanest support | §4.1 | citation | (2.3) at `theta=1` does imply it, so the slip is invisible from inside |
| M5 | the counterexample is reported as a single find at ratio `0.91097`; the failure set has positive measure (13.9% of random draws, worst ratio `0.217`) | §5.3 bullet 2 | under-claim | search stopped at first witness |
| M6 | "nothing was committed, nothing was pushed" is now stale — the note is committed as `a5d9adc` | §front matter | stale self-description | commit made after the note was written; not pushed (no remote ref), so half the sentence still holds |

None of M1–M6 is a soundness defect. None requires a change to Theorem S, to
the code, or to the verdict. **Nothing was fixed by this referee; all six are
reported for the owning lane.**

---

## 9. Ruling

The target note's central claim — that
`q8_schur_contour.py:351-358` is the **exact** operator telescoping
`ABC - A_N B_N C_N = Delta_A BC + A_N Delta_B C + A_N B_N Delta_C`, in
correct six-slot bijection, with correct per-slot op/trace bookkeeping,
conservative direction, and with `hs[.]` correctly supplying the **true
untruncated** operator norms that hypothesis (H1) demands — is **upheld on
independent evidence**. Its two flagged items (the undocumented invariant
R1-a, the latent `Xop`/`b3` gap R1-b) are correctly identified and correctly
scoped, and no live path commits the latent unsoundness. The scope statement
is complete and LEDGER-RULE compliant.

### **CONFIRMED**

Residual R1 of `L_OUT_CONDITION4_ADJUDICATION.md` is discharged, conditional
on inherited hypothesis H0 (the still-OPEN q=8 MMS-to-Hardy/Hilbert
operator/basis/norm binding) and on the pinned TB/W/R2 receipt preconditions,
exactly as the note states. No theorem-grade q=8 claim is created or
strengthened by this referee.

---

**READY FOR JUDGING.**
