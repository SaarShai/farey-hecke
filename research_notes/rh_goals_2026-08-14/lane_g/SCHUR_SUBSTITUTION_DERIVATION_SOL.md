# Schur substitution — derivation of residual R1

**Date** 2026-08-20 · **Lane** lane_g (derivation lane, cold on the L-OUT
compute lane and on the adjudication lane) · **Branch**
`codex/prime-step-review-economic-validation` · **Mode** read-only on the work
product. This file is the only new artifact. No existing file was edited,
nothing was committed, nothing was pushed.

**Interpreter** `/Users/za/.venvs/farey-rh/bin/python` (python-flint / Arb,
`ctx.prec = 384–400`; mpmath 25–50 dps for the singular-value arm). All scripts
written for this derivation live in the session scratchpad, not in the repo.

**Task.** `L_OUT_CONDITION4_ADJUDICATION.md` §5 R1: *"condition 5's
factor-by-factor Schur substitution is asserted, not re-derived — the largest
remaining soundness risk inside L-OUT."* Prove or refute it.

---

## 0. Verdict, up front

| item | verdict |
|---|---|
| The six-term telescoped substitution as implemented at `q8_schur_contour.py:350-358` | **PROVED** — it is an exact operator telescoping, not a first-order truncation; no cross term is dropped |
| Direction (upper bound on the true defect) | **PROVED** conservative |
| Hypothesis (iv): which operator the `hs[.]` coefficients must bound | **the TRUE untruncated blocks**, and the code does supply that. Hypothesis identified, audited, and confirmed. It is **load-bearing** — §5.3 exhibits an explicit counterexample if the truncated-block norms are used instead |
| Inherited open hypothesis H0 (orthonormal basis / Hardy-Hilbert binding) | **CONJECTURAL** — not created by this substitution, but the substitution is conditional on it, exactly as everything else in L-OUT is |
| Secondary finding on `Xop` | **GAP (latent, not currently live)** — see §6.2 |

Net: **R1 is discharged.** The substitution is sound. Its soundness rests on a
hypothesis that no lane_g document had previously stated, that hypothesis is
true of the code as written, and the derivation below records why.

---

## 1. Objects, and the exact statement to be proved

### 1.1 The Schur combination

The q=8 even MMS-(32) operator has block form
`L = [[0,0,B1],[A2,0,B2],[0,A3,B3]]`, and exact block elimination gives
`det(I-L) = det(I-C)` with

```text
C  =  B3 + A3 B2 + A3 A2 B1 .                                            (1.1)
```

The checker never forms `C`. It forms, at `q8_schur_contour.py:190`
(`schur_value_and_derivative`),

```text
C_N  =  B3_N + A3_N B2_N + A3_N A2_N B1_N ,        X_N := P_N X P_N ,    (1.2)
```

i.e. **products of truncated blocks**, not the truncation of the product. That
distinction is the whole content of the problem: `(A3 B2)_N != A3_N B2_N`.

`X_N` is literally the top-left `N x N` corner of the block in the `e_{j,k}`
basis; verified numerically to be exact (§5.1, `corner = 0.0`).

### 1.2 The per-block defect

Write `Delta_X := X - X_N`. From `Q8_OUTPUT_TAIL_SOL.md:147` (2.1) and
`:215-221` (2.6),

```text
X - P_N X P_N  =  X (I - P_N)  +  (I - P_N) X P_N                        (1.3)
|| X - X_N ||_1  <=  tau_in(X; N)  +  tau_out(X; N, theta)  =:  d_X      (1.4)
```

with `tau_in` = `tail_trace_tail`/`single_trace_tail`
(`q8_schur_contour.py:216-221`) and `tau_out = theta^{-N} sum_{k<N} M_k(theta)`.
Both are **trace-norm** (`||.||_1`) bounds. (1.4) is the object the L-OUT lane
certifies; this note takes it as given and does not re-derive it — the
adjudication already re-derived (2.1)–(2.6) and the referee independently
confirmed the HS→trace step.

### 1.3 The coefficient bounds

`q8_schur_contour.py:332` (single blocks) and `:224-239`
(`block_hilbert_tail_bound`, tail-family blocks) produce, for
`h_X := hs[X]`:

```text
h_A2 = w / sqrt(1 - rho^2)                    = sqrt( sum_{k>=0} (w rho^k)^2 )
h_B  = sqrt( sum_{k<K} b_k^2 + 2A^2 q^{2K}/(1-q^2) + 2C^2 sum_{k>=K} k^2 rho^{2k-2} )
```

Both are **complete `k`-sums over the whole infinite column index set**, with no
`k < N` cut. This is the load-bearing observation of the whole note and is
argued in §4.

### 1.4 The statement

> **Theorem S (the substitution).** Let `A2, A3, B1, B2, B3` be bounded
> operators on a Hilbert space `H`, let `P_N` be an **orthogonal** projection,
> `X_N := P_N X P_N`, and let `C`, `C_N` be as in (1.1)–(1.2). Suppose real
> numbers `d_X, h_X >= 0` satisfy
>
> ```text
> (H1)   h_X  >=  || X ||_op          for X in {A2, A3, B1, B2}
> (H2)   d_X  >=  || X - X_N ||_1     for X in {A2, A3, B1, B2, B3}
> ```
>
> Then
>
> ```text
> || C - C_N ||_1
>     <=  d_B3
>       + h_A3 d_B2  +  d_A3 h_B2
>       + h_A3 h_A2 d_B1  +  h_A3 d_A2 h_B1  +  d_A3 h_A2 h_B1 .          (S)
> ```
>
> The right-hand side of (S) is **exactly** `input_tail_only` at
> `q8_schur_contour.py:351-358` with `trace[X] -> d_X` and `hs[X] -> h_X`.

Note what (H1) does **not** say: it does not require `h_X >= ||X_N||_op`
separately — that follows (Lemma 2.2), but only because `P_N` is an orthogonal
projection. And note that (H1) is a hypothesis on the **true** operator. That is
the classic hole the task asks about, and it is where the whole derivation
turns; see §4 and the counterexample in §5.3.

---

## 2. Norm inequalities used, named

All are standard facts about the Schatten ideals; each is named at the point of
use so that no step is silent.

* **(N1) Trace-ideal / Hölder property.** For bounded `A, B` and trace-class `T`,
  `A T B` is trace class and `|| A T B ||_1 <= ||A||_op ||T||_1 ||B||_op`.
  (Reed–Simon XI / Simon, *Trace Ideals*, Thm 2.8: the Schatten classes are
  two-sided ideals, and `||.||_1` is unitarily invariant with this Hölder
  bound.) Specializations used: `||AT||_1 <= ||A||_op ||T||_1` and
  `||TB||_1 <= ||T||_1 ||B||_op`.
* **(N2) Triangle inequality** for `||.||_1`.
* **(N3) Norm domination.** `||X||_op <= ||X||_HS ( = ||X||_2 )` and
  `||X||_2 <= ||X||_1`. Used only in the direction `op <= HS`, when a recorded
  Hilbert–Schmidt bound is consumed as an operator-norm bound (§4.1). This is
  the conservative direction.
* **(N4) Projection contraction.** For an orthogonal projection `P`,
  `||P||_op = 1`, hence by (N1) `||P X P||_op <= ||X||_op` and
  `||P X P||_1 <= ||X||_1`.
* **(N5) Rank-one column decomposition.** `X (I - P_N) = sum_{k >= N} (X e_k) e_k^*`
  is a sum of rank-one operators of trace norm `||X e_k||_2`, so
  `||X(I-P_N)||_1 <= sum_{k >= N} ||X e_k||_2`. (This is (2.2) of
  `Q8_OUTPUT_TAIL_SOL.md`; used here only to identify what `d_X` is, not in the
  telescoping itself.)

**Lemma 2.2.** Under (H1) and `P_N` an orthogonal projection,
`h_X >= ||X_N||_op` as well.
*Proof.* (N4) with `P = P_N`. ∎

This lemma is why a **single** number `h_X` may stand in front of both a
truncated and an untruncated factor in (S). The reverse is false — a bound on
`||X_N||_op` says nothing about `||X||_op` — which is the asymmetry §5.3
exploits.

---

## 3. The derivation

### 3.1 The two- and three-factor telescoping identities

These are **algebraic identities**, valid in any ring. No approximation, no
expansion in a small parameter, no discarded remainder.

```text
A B  -  A_N B_N   =   (A - A_N) B  +  A_N (B - B_N)
                  =   Delta_A B  +  A_N Delta_B                          (3.1)

A B C  -  A_N B_N C_N
     =  (A - A_N) B C  +  A_N (B - B_N) C  +  A_N B_N (C - C_N)
     =  Delta_A B C  +  A_N Delta_B C  +  A_N B_N Delta_C                (3.2)
```

*Verification of (3.2), term by term:*
`Delta_A B C = ABC - A_N BC`;
`A_N Delta_B C = A_N BC - A_N B_N C`;
`A_N B_N Delta_C = A_N B_N C - A_N B_N C_N`.
The sum telescopes: `ABC - A_N B_N C_N`. ∎

**This settles requirement (ii) of the task — "no cross term is dropped" —
definitively, and it settles it in a stronger form than the task anticipates.**
The task frames the risk as "second-order terms must be dominated explicitly,
not ignored". There are no second-order terms to dominate. The naive route

```text
(A_N + Delta_A)(B_N + Delta_B) = A_N B_N + Delta_A B_N + A_N Delta_B
                                 + Delta_A Delta_B                       (3.3)
```

does produce a quadratic remainder `Delta_A Delta_B`, and a bound built from
(3.3) that kept only the linear terms would be **unsound**. But (3.1) is not
(3.3). In (3.1) the *first* term carries the **untruncated** `B`, not `B_N`;
`Delta_A B = Delta_A B_N + Delta_A Delta_B` absorbs the quadratic remainder
exactly. Likewise in (3.2) the first term carries untruncated `B C` and the
second untruncated `C`, absorbing all quadratic and the single cubic remainder.
The graded structure is: **one factor untruncated on the right of each `Delta`,
truncated on the left.** That is the entire mechanism, and it is precisely why
(H1) must be a hypothesis about the **true** operator (§4).

### 3.2 Assembling (S)

Apply (N2) to (1.1)–(1.2):

```text
C - C_N  =  Delta_B3  +  ( A3 B2 - A3_N B2_N )  +  ( A3 A2 B1 - A3_N A2_N B1_N )
```

*Term 1.* `|| Delta_B3 ||_1 <= d_B3` by (H2).

*Term 2.* By (3.1),
`A3 B2 - A3_N B2_N = Delta_A3 B2 + A3_N Delta_B2`. By (N2) then (N1):

```text
|| Delta_A3 B2 ||_1   <=  || Delta_A3 ||_1 || B2 ||_op   <=  d_A3 h_B2     [(H2),(H1)]
|| A3_N Delta_B2 ||_1 <=  || A3_N ||_op || Delta_B2 ||_1 <=  h_A3 d_B2     [Lemma 2.2,(H2)]
```

*Term 3.* By (3.2) with `(A,B,C) = (A3, A2, B1)`,
`A3 A2 B1 - A3_N A2_N B1_N = Delta_A3 A2 B1 + A3_N Delta_A2 B1 + A3_N A2_N Delta_B1`.
By (N2) then (N1):

```text
|| Delta_A3 A2 B1 ||_1      <= ||Delta_A3||_1 ||A2||_op ||B1||_op   <= d_A3 h_A2 h_B1
|| A3_N Delta_A2 B1 ||_1    <= ||A3_N||_op ||Delta_A2||_1 ||B1||_op <= h_A3 d_A2 h_B1
|| A3_N A2_N Delta_B1 ||_1  <= ||A3_N||_op ||A2_N||_op ||Delta_B1||_1
                                                                    <= h_A3 h_A2 d_B1
```

using (H1) for the untruncated `||A2||_op, ||B1||_op` and Lemma 2.2 for the
truncated `||A3_N||_op, ||A2_N||_op`. Summing the six bounds gives (S). ∎

**Term-for-term correspondence with the code** (`q8_schur_contour.py:351-358`):

| derivation term | bound | code line | code expression |
|---|---|---|---|
| `Delta_B3` | `d_B3` | 352 | `trace["B3"]` |
| `A3_N Delta_B2` | `h_A3 d_B2` | 353 | `a3 * trace["B2"]` |
| `A3_N A2_N Delta_B1` | `h_A3 h_A2 d_B1` | 354 | `a3 * a2 * trace["B1"]` |
| `Delta_A3 B2` | `d_A3 h_B2` | 355 | `trace["A3"] * b2` |
| `Delta_A3 A2 B1` | `d_A3 h_A2 h_B1` | 356 | `trace["A3"] * a2 * b1` |
| `A3_N Delta_A2 B1` | `h_A3 d_A2 h_B1` | 357 | `a3 * trace["A2"] * b1` |

Six terms, six slots, bijective. `hs[.]` unchanged, `trace[.]` carrying the
defect — exactly referee condition 5, and exactly the rule correction block 6
asserts. **The rule the three lane_g documents state is the correct rule; what
was missing was this derivation, and it goes through.**

### 3.3 Requirement (iii) — direction

Every quantity in (S) is a nonnegative real. The code takes `.upper()` on each
`hs[.]` and each `trace[.]` before combining (`:332`, `:345`, `:346`, `:216-221`,
`:239`) and `.upper()` on the total (`:358`). Arb's `.upper()` returns an upper
bound of the enclosure, and `+`/`*` on nonnegative arb enclosures are monotone
increasing in each argument. Therefore the recorded `input_tail_only` (and,
after the L-OUT substitution `trace[X] -> trace[X] + tau_out[X]`, `full_tau`) is
an **upper** bound of the RHS of (S), hence of `||C - C_N||_1`. Direction is
conservative at every step. ✓

There is a second, independent conservatism: (S) bounds the **trace** norm,
while the downstream consumer (§6.1) needs only an **operator**-norm bound, and
`||.||_op <= ||.||_1` by (N3). The pipeline therefore over-delivers.

### 3.4 Substituting `tau_out` into each slot

L-OUT sets `d_X = tau_in(X) + tau_out(X)` in each of the six slots. By (1.4)
this is exactly the hypothesis (H2) of Theorem S. No further argument is needed:
(S) is stated for an arbitrary `d_X` dominating `||X - X_N||_1`, and (1.4) says
`tau_in + tau_out` is such a `d_X`. The "category slip" the referee flagged in
GAP 5 (adding two block-level totals rather than substituting per slot) is
avoided precisely by this reading — (2.6) is consumed as the *input* to (H2),
never as a substitute for the telescoping. ✓

---

## 4. Hypothesis audit against the actual code

This is task requirement (iv): do the recorded `hs[.]` bound the **true**
operator or only the **perturbed/truncated** one, and which is required?

**Required: the true one.** (H1) is used three times on untruncated factors —
`||B2||_op`, `||A2||_op`, `||B1||_op` in terms 2 and 3 of §3.2. Lemma 2.2
recovers the truncated cases for free, but not conversely.

### 4.1 What the code actually records

* **Tail-family blocks `B1, B2, B3`** (`block_hilbert_tail_bound`, `:224-239`).
  Computes `sqrt( sum_{k<K} sel_k^2 + 2A^2 q^{2K}/(1-q^2) + 2C^2 sum_{k>=K} k^2 rho^{2k-2} )`.
  The `k`-sum runs over the **entire** column index set (`k < K` explicitly,
  `k >= K` by the closed-form envelope tail) with no reference to `N`. Each
  `sel_k >= M_k(1) >= ||X e_k||_2` — the last step by
  `Q8_OUTPUT_TAIL_SOL.md:186` (2.3) at `theta = 1`, whose row sum
  `sum_{m>=0} |X[m,k]|^2` covers **all** rows `m`, omitted output rows included.
  Hence `hs[B_j] >= sqrt( sum_k ||X e_k||_2^2 ) = ||X||_HS >= ||X||_op` by (N3),
  for the **true, untruncated, un-row-truncated** block. **(H1) holds.** ✓
* **Single blocks `A2, A3`** (`:332`). `weight / sqrt(1 - rho^2)
  = sqrt( sum_{k>=0} (w rho^k)^2 )`, again a complete `k`-sum, on the TB/W
  receipt precondition `||X e_k||_2 <= w rho^k`. Same conclusion. **(H1) holds.** ✓
* **The two-family sum** (`:345`). `hs[B_j]` is the sum over the `+2` and `-1`
  sub-blocks; since `B_j` is their sum, (N2) gives
  `||B_j||_op <= sum of parts`. ✓ The same triangle step covers
  `trace[B_j]` at `:346` for (H2). ✓

**Conclusion of the audit: the classic hole is not present.** The `hs[.]`
coefficients bound the true infinite blocks, which is the side (H1) demands.
This was never stated in `Q8_OUTPUT_TAIL_SOL.md`, `Q8_OUTPUT_TAIL_REFEREE.md`,
or `L_OUT_RECEIPT_SOL.md` (searched; no doc asserts either side). It is true of
the code as written, but it is an **implicit invariant**: any future re-pin of
`hs[.]` to a finite-section norm — a natural-looking "tightening", since
`||X_N|| <= ||X||` — would silently break (S). See §7 R1-a.

### 4.2 Hypotheses inherited, not established here

* **H0 — orthonormality of `{e_{j,k}}`.** Everything above uses (N4)
  (`P_N` an orthogonal projection) and the identification
  `sum_m |X[m,k]|^2 = ||X e_k||_2^2`. Both hold iff the `e_{j,k}` basis is
  orthonormal for the Hilbert structure in which `||.||_1`, `||.||_HS` are
  taken. `Q8_OUTPUT_TAIL_SOL.md:100-101` declares this ("Hardy/Hilbert norm in
  the gate means precisely this"), and the adjudication records that the
  **"Exact q=8 MMS-to-Hardy/Hilbert operator, basis and norm binding" remains
  separately OPEN** (`L_OUT_CONDITION4_ADJUDICATION.md:361-367`).
  Status: **CONJECTURAL, inherited.** Theorem S neither needs more than the rest
  of L-OUT already assumes nor repairs it. If H0 fails, `P_N` need not be a
  contraction, Lemma 2.2 fails, and (S) fails with it — but so does (2.2)–(2.6)
  and every norm in the receipt chain. R1 is not the place this is decided.
* **The TB/W column preconditions** `||A2 e_k||_2 <= w rho^k`. Taken from the
  pinned TB/W receipts; the adjudication §3.3 independently re-verified the
  boundary-sup preconditions of the same objects. Not re-derived here.

---

## 5. Numeric receipts

Scripts: `schur_subst_test.py` (mpmath singular-value arm) and
`schur_subst_arb.py` (Arb interval arm + counterexample search), both in the
session scratchpad. "True" is modelled by the dimension-`M` truncation with
`M = 3N`; blocks come from the **unmodified** `lane_f/q8_r3b_engine.py`
(`build_q8_block_matrices_and_s_derivative`, factors `("10","4","2")`,
`sign = 1`, `n_head = 4`) and the Schur combination is formed exactly as
`schur_value_and_derivative` does it.

### 5.1 Structural precondition: `X_N` is the corner of `X_M`

`max over the 5 blocks and i,j < N of |X_M[i,j] - X_N[i,j]| = 0.0` at every
tested `(s, N, M)`. So the engine's dimension-`N` block **is** `P_N X P_N` with
`P_N` the coordinate projection, as (1.2) assumes. No embedding mismatch.

### 5.2 Main arm — mpmath, 50 dps, exact singular values

`LHS = ||C_M - C_N||_1` (sum of singular values); `RHS_true` = (S) with
`d_X = ||X_M - X_N||_1`, `h_X = ||X_M||_op`.

| `s` | `N`/`M` | LHS | RHS (S) | ratio | pass |
|---|---|---|---|---|---|
| `0.42523104+4.34576079i` (the pin) | 6/18 | 17.35979 | 278.66569 | 16.05 | ✓ |
| `0.42523104+4.34576079i` | 8/24 | 10.512898 | 112.05261 | 10.66 | ✓ |
| `0.42523104+4.34576079i` | 10/30 | 5.4987797 | 45.691119 | 8.309 | ✓ |
| `0.42523104+0.5i` | 6/18 | 0.11400894 | 0.92121539 | 8.080 | ✓ |
| `0.42523104+0.5i` | 10/30 | 0.012609652 | 0.29802142 | 23.63 | ✓ |
| `0.1+1.0i` | 6/18 | 0.16124124 | 1.0580744 | **6.562** | ✓ |
| `0.1+1.0i` | 10/30 | 0.018137156 | 0.31045662 | 17.12 | ✓ |
| `0.9+0.2i` | 6/18 | 0.068070297 | 0.4680277 | 6.876 | ✓ |
| `0.9+0.2i` | 10/30 | 0.0093038547 | 0.16007874 | 17.21 | ✓ |
| `0.05+8.0i` (adverse, large blocks) | 6/18 | 7591.0628 | 2204995.3 | 290.5 | ✓ |
| `0.05+8.0i` | 10/30 | 5978.633 | 596144.61 | 99.71 | ✓ |
| `0.75+12.5i` (adverse) | 6/18 | 110479.43 | 2.9761293e9 | 26938 | ✓ |
| `0.75+12.5i` | 10/30 | 155760.45 | 1.930651e9 | 12395 | ✓ |

**18 configurations (6 `s`-points x 3 `(N,M)` pairs), 0 violations, min ratio
6.562.** The bound is loose by roughly one order at the pin and much more at
adverse points, as an operator-norm-coefficient bound should be — looseness is
the conservative direction.

### 5.3 The test has power, and hypothesis (iv) is load-bearing

Two negative controls, both run on the same data:

* **Strawman A — drop the two `Delta_A`-side terms** (keep only
  `d_B3 + h_A3 d_B2 + h_A3 h_A2 d_B1`, the shape a reader might guess from
  "substitute into each `trace[.]` slot" if the `A`-slots were overlooked).
  Minimum ratio over the 18 configurations: **0.3115 < 1 — VIOLATED** at
  10 of 18 points. So the six-term shape is not decorative; the numeric test
  would have caught a wrong shape.
* **Strawman B — use truncated-block coefficients** `h_X = ||P X P||_op`
  instead of `||X||_op`, i.e. deny hypothesis (H1) and keep only Lemma 2.2's
  half. On the q=8 blocks this happens not to fail (min ratio 6.561, because the
  q=8 blocks are strongly diagonally concentrated so `||X_N||_op ~ ||X||_op`).
  A randomized search over `3 x 3` complex Gaussian block quintuples with
  `rank(P) = 1` finds a counterexample: **RHS/LHS = 0.91097 < 1**.

  So (S) is **false** under the weakened hypothesis, and the q=8 numerics alone
  could not have distinguished the two. Hypothesis (H1) has to be verified by
  reading the code (§4.1), which is what makes §4 the substantive part of this
  note rather than a formality.

### 5.4 Rigorous Arb interval arm

To remove any dependence on floating singular values, the direction was
re-verified with Arb enclosures only, with both sides deliberately biased
*against* the claim: LHS **over**-estimated by the rank-one column bound
`||Y||_1 <= sum_j ||Y e_j||_2` (N5), RHS **under**-estimated by
`d_X -> ||Delta_X||_F <= ||Delta_X||_1` and
`h_X -> max_j ||X e_j||_2 <= ||X||_op`. Passing this stricter test implies the
true inequality.

| `s` | `N`/`M` | `LHS_upper` | `RHS_lower` | rigorous pass |
|---|---|---|---|---|
| `0.42523104+4.34576079i` | 6/18 | `[20.53692067 +/- 3.95e-9]` | `[194.2264990 +/- 9.82e-9]` | **True** |
| `0.42523104+4.34576079i` | 8/24 | `[12.48355850 +/- 3.11e-9]` | `[76.27954930 +/- 6.13e-10]` | **True** |
| `0.42523104+0.5i` | 6/18 | `[0.1632644485 +/- 2.76e-11]` | `[0.5205803147 +/- 2.86e-12]` | **True** |
| `0.42523104+0.5i` | 8/24 | `[0.05529972734 +/- 2.90e-12]` | `[0.2923510088 +/- 9.48e-13]` | **True** |
| `0.1+1.0i` | 6/18 | `[0.2307870971 +/- 3.93e-11]` | `[0.5892499985 +/- 1.53e-11]` | **True** |
| `0.1+1.0i` | 8/24 | `[0.07821965076 +/- 3.32e-12]` | `[0.3122063661 +/- 4.53e-11]` | **True** |
| `0.9+0.2i` | 6/18 | `[0.1013909548 +/- 1.92e-11]` | `[0.2946505137 +/- 1.41e-11]` | **True** |
| `0.9+0.2i` | 8/24 | `[0.03967717208 +/- 2.59e-12]` | `[0.1723266210 +/- 4.29e-11]` | **True** |

**8/8, no floating-point step anywhere in the comparison.**

---

## 6. What (S) is consumed by, and one latent gap

### 6.1 The consumer is an operator-norm homotopy gate

`q8_schur_contour.py:486-495`:

```text
inv_arc       = ||A0^{-1}||_F / (1 - qF)                  A0 = I - C_N(s_mid)
inv_tilde     = 1 + Xop * inv_arc
tail_homotopy = full_tau * inv_tilde                      gate: < 1
```

`inv_tilde` is the resolvent identity `(I-C)^{-1} = I + C (I-C)^{-1}`, so
`inv_tilde >= ||(I - C_N)^{-1}||` provided `Xop >= ||C_N||_op` and
`inv_arc >= ||(I-C_N)^{-1}||` on the arc. The gate `full_tau * inv_tilde < 1`
is then the Neumann condition `||(I-C_N)^{-1}|| * ||C - C_N|| < 1`, which makes
`I - (C_N + t(C - C_N))` invertible for all `t` in `[0,1]` and so licenses the
finite-section winding count as the winding count of `det(I - C)`.

(S) delivers `||C - C_N||_1 >= ||C - C_N||_op`, so it over-delivers for this
consumer (N3). ✓ Direction correct. Note that `full_tail_certified` is
hard-coded `False` at `:395`, so this gate is currently inert; the derivation
is prospective, which is the right posture.

### 6.2 Latent gap — `Xop` is an HS bound used where a trace bound might later
be wanted

`xop = b3 + a3*b2 + a3*a2*b1` (`:350`). As an **operator**-norm bound of `C_N`
this is sound: `||B3||_op <= b3` by (N3), `||A3 B2||_op <= a3 b2`, etc.

But if any future consumer reads `Xop` as a bound on `||C_N||_1` — e.g. a
Fredholm determinant-difference estimate of the Simon type
`|det(I-C) - det(I-C_N)| <= ||C - C_N||_1 exp(1 + ||C||_1 + ||C_N||_1)`, which
is the natural next tool once `full_tau` goes live — the first term is
**unsound**: `b3` bounds `||B3||_HS`, and `||B3||_1` is *not* dominated by
`||B3||_HS`. (The product terms would survive, since
`||A3 B2||_1 <= ||A3||_HS ||B2||_HS = a3 b2` by Hölder; only the bare `b3`
fails.) Flagged as **CONJECTURAL / do not reuse** — see §7 R1-b. This is
outside R1's scope and does not affect the ruling above.

---

## 7. Verdict and repairs

### VERDICT: **PROVED.**

The factor-by-factor Schur substitution as implemented at
`q8_schur_contour.py:350-358`, with `trace[X] -> tau_in(X) + tau_out(X)` and
`hs[.]` unchanged, is a valid upper bound on `||C - C_N||_1`. It is not a
first-order approximation: (3.1)–(3.2) are exact ring identities, and the
quadratic and cubic remainders are absorbed by the untruncated factors, not
dropped. The direction is conservative at every step. The bound is verified
numerically at 18 configurations including adverse ones (min slack 6.56x), and
rigorously with Arb enclosures at 8 configurations with both sides biased
against the claim.

**Residual R1 of `L_OUT_CONDITION4_ADJUDICATION.md` is discharged**, subject
only to inherited hypothesis H0 (§4.2), which is the already-recorded, already-
open Hardy/Hilbert basis binding and is not created by this substitution.

### Repairs / recommendations (none block the verdict)

* **R1-a (invariant, should be recorded in code).** (H1) requires `hs[.]` to
  bound the **true untruncated** blocks. The code satisfies this (§4.1) but
  nowhere says so, and the "obvious tightening" `hs[X] -> ||X_N||` is unsound
  (§5.3 strawman B, ratio 0.911). Recommend a one-line comment at
  `q8_schur_contour.py:224` and `:332` — *"complete k-sum: must bound the
  untruncated block; the telescoping at :351-358 depends on it"* — and a
  sentence in any future L-OUT receipt schema. **Not applied: this note edits
  no existing file.**
* **R1-b (latent).** Do not reuse `Xop` as a trace-norm bound; `b3` is an HS
  bound and the bare `B3` term would be unsound in a Simon-type determinant
  difference (§6.2). If that route is taken, `B3` needs its own `||.||_1`
  certificate (`sum_k M_k` for the `B3` families, which the receipts already
  contain as `trace["B3"]`-shaped data at `N = 0`).
* **R1-c (documentation).** `Q8_OUTPUT_TAIL_SOL.md` correction block 6,
  `Q8_OUTPUT_TAIL_REFEREE.md` GAP 5 / condition 5, and
  `L_OUT_RECEIPT_SOL.md` §3 all state the substitution rule correctly and all
  assert rather than derive it. This file is the derivation; if any of those is
  ever revised, point it here rather than restating the assertion.

### Scope statement

Nothing above upgrades any claim outside R1. `full_tail_certified` remains
`False`; the `N = 104` pin still misses the `1e-15` target (adjudication §5,
condition 7); and the q=8 MMS-to-Hardy/Hilbert operator/basis/norm binding, E1
on the enlarged disc, `K_s` nonvanishing, the Selberg factorization, the
four-edge winding, and `recorded_tail_checks_pass` all remain OPEN. Theorem S
is conditional on all of them exactly as the rest of L-OUT is.

---

**READY FOR JUDGING.**

---

## Dated correction block (2026-08-20, referee M1–M6, append-only)

Applied per SCHUR_SUBSTITUTION_REFEREE.md (final verdict CONFIRMED; six
minor defects, none soundness-affecting):

- **M1**: strawman A is violated at 11 of 18 points, not 10 as stated
  (min 0.3115 correct) — the note under-stated its own test power.
- **M2**: reproducibility — the numeric tables used
  factors=("10","4","2") = RECEIPT_FACTORS, NOT the engine default
  EXACT_FACTORS=('3.4','2.2','1.4'); reruns must pass the receipt
  factors explicitly or they will get a different (still passing)
  table.
- **M3**: §0 row 1 "as implemented ... PROVED" is to be read as the
  body states three times: the live input_tail_only is tau_in only and
  is NOT itself a bound on ||C−C_N||_1; the PROVED claim is the
  telescoping substitution identity and its norm bookkeeping.
- **M4**: the §4.1 citation for the full-column Parseval step should be
  Q8_OUTPUT_TAIL_SOL.md §1.3 (direct support), not :186 (2.3) at
  theta=1.
- **M5**: the counterexample is stronger than reported: 200,000 random
  rank-one quintuples give 0 violations under (H1) but 27,840 (13.9%)
  violations with truncated coefficients, worst ratio 0.217 (referee
  receipt) — hypothesis (iv) is load-bearing with positive measure.
- **M6**: the closing "nothing was committed" is stale; the note is
  committed as a5d9adc by the orchestrating session (true at authoring
  time).
