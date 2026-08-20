# q=8 omitted-output (row / projection) coefficient tail

Date: 2026-08-20.
Lane: G5 (q=8 omitted-output projection tail).
Repo: `/Users/za/Documents/farey-hecke`, branch
`codex/prime-step-review-economic-validation`.

## Status

**CONJECTURAL. NOT CERTIFIED. PENDING A COLD REFEREE.**

This note derives the missing omitted-output tail in the same Hardy/Hilbert
norm the input-column tail already uses, gives the explicit constants and the
closed forms, records the numerical receipts that the bound survives adverse
comparison against brute-force tail sums, and names exactly what remains
uncertified. No file in `lane_f/` was modified. No checker was changed. No
q=8 determinant, Fredholm, Selberg, resonance, or LAW claim is made or
advanced here. Nothing below is confirmed.

**Source-location correction.** The task brief located the q=8 Schur sources
in `research_notes/rh_goals_2026-08-14/lane_g/`. They are in fact in
`research_notes/rh_goals_2026-08-14/lane_f/`. Every file cited below is under
`lane_f/`. This note is written to the requested `lane_g/` path.

---

## 1. Setup and the exact gate

### 1.1 The gate, quoted

`lane_f/Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_SOL.md`, "Remaining OPEN gates":

> The first remaining mathematical gap is a certified omitted-output
> row/projection coefficient tail, combined with the input-column tail in the
> same explicitly bound Hardy/Hilbert norm.

`lane_f/Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_REFEREE.md`, verdict section
(**GAPS NOT REFUTED**):

> The first remaining mathematical gap is a certified omitted-output-row /
> projection tail combined with the input-column tail in one explicitly bound
> Hardy/Hilbert (and propagated trace) norm.

and §4:

> there is no certified omitted-output-row/projection coefficient tail
> compatible with the input-column tail, and therefore no full trace-norm
> bound for the finite-section-to-Fredholm comparison.

The checker states the same refusal in code, `lane_f/q8_schur_contour.py:381`:

> "The immutable q8 F1024 receipts bound omitted input columns only; no
> compatible omitted-output-row/projection coefficient tail is present."

and names the required shape at `q8_schur_contour.py:397`:

> "tau_full requires full block tails ||T-P_i T P_j||_1, combining omitted
> input columns and omitted output rows before Schur telescoping"

### 1.2 Operator, basis, norm

From `lane_f/q8_r3b_engine.py` and `lane_f/f8_certify_tb_blocks.py`. The q=8
even MMS eq.(32) transfer operator acts on functions holomorphic on three
discs `D(c_i, r_i)`, `i = 1,2,3`, where `c_i`, `r_i` come from the Markov
partition of `[-lambda/2, 0]` with `lambda = lambda_8 = 2 cos(pi/8) =
sqrt(2 + sqrt(2))` and the pinned F1024 inflation factors `("10","4","2")`.
Pinned values (`f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json`):

```text
lambda   [1.84775906502257351225637 +/- 3.63e-24]
c_1 -0.844623198620733149792552   r_1 0.792563338905536063356316
c_2 -0.653281482438188263928322   r_2 0.448341529167965118114394
c_3 -0.270598050073098492199862   r_3 0.541196100146196984399723
```

Define the Hilbert space

```text
H  =  H^2(D(c_1,r_1)) (+) H^2(D(c_2,r_2)) (+) H^2(D(c_3,r_3)),
```

each summand the Hardy space of the disc with orthonormal basis

```text
e_{i,m}(z) = ((z - c_i)/r_i)^m ,    m = 0, 1, 2, ...
```

This is exactly the basis the engine uses. In
`_single_block_allcols_with_s_derivative` (`q8_r3b_engine.py:24-46`) the series
variable is `u` with `z = c_i + rho_i*u` — the normalized **output**-disc
coordinate, so the series index `m` is the **row** index — and column `k` is
`weight * base^k` with `base = (argument - c_j)/rho_j` — the normalized
**input**-disc coordinate, so `k` is the **column** index. Hence for one block
`T = T^{(i,j)}`:

```text
T[m,k]  =  m-th Taylor coefficient in u  of  f_k(u) := (T e_{j,k})(c_i + r_i u).
```

The relevant norms are the Hilbert-Schmidt norm of `H` in this basis and the
trace norm; "Hardy/Hilbert norm" in the gate means precisely this.

### 1.3 What the R2 receipt actually certifies

This is the load-bearing observation, and it is stronger than the SOL text
suggests. `lane_f/q8_r2_local.py:186-208` computes, for each block and each
`k <= K_head`,

```text
direct_sups[k] = sup over the arc cover of  d D(c_i, r_i)  of  |(T e_{j,k})(z)|
```

(`exact_tail_columns_on_arc` evaluates the Hurwitz-closed column *function* at
points `z` on the boundary circle of the **output** disc; the arc cover is
`arcs[i-1] = tb.arc_ball(centers[i], radii[i], ., M)` with `M = 512`). It then
records the envelope

```text
selected_column_bounds[k] = b_k <= min( direct_sups[k],  A q^k + C k rho^(k-1) )
```

with `A = direct_sups[0]`, `q = |c_j| / r_j`, `rho = TB ratio_upper_bound`, and
`C` the summed weighted first moment (heads plus certified deep tail).

So `b_k` is a **sup-norm bound on the boundary circle of the output disc**, not
an l2 column norm. By Parseval in `u` on `|u| = 1`,

```text
sum_{m >= 0} |T[m,k]|^2  =  ||f_k||^2_{L^2(|u|=1)}  <=  ( sup_{|u|=1} |f_k| )^2  =  b_k^2 ,
```

which retroactively justifies `block_hilbert_tail_bound`
(`q8_schur_contour.py:224-239`) treating `b_k` as a column l2 bound. It also
supplies, for free, the mechanism the output side needs: **the same
computation on an enlarged circle gives geometric row decay.**

---

## 2. Derivation

Let `P_N` be the orthogonal projection onto `span{e_{i,m} : m < N}` in every
disc summand.

### 2.1 The two-term splitting

```text
T - P_N T P_N  =  T (I - P_N)  +  (I - P_N) T P_N .                       (2.1)
```

(Check: `T(I-P_N) + (I-P_N)T P_N = T - T P_N + T P_N - P_N T P_N`.) This split
is chosen over the equivalent `(I-P_N)T + P_N T (I-P_N)` deliberately: its
second term involves only the **finite** column range `k < N`, so no
convergence hypothesis on the full column sum is needed. That matters in §3.3.

The first term is the input-column tail, already certified:

```text
|| T (I-P_N) ||_HS^2 = sum_{k >= N} ||T e_k||^2 ,
|| T (I-P_N) ||_1   <= sum_{k >= N} ||T e_k||_2 ,                          (2.2)
```

the second inequality because `T(I-P_N) = sum_{k>=N} (T e_k) e_k^*` is a sum of
rank-one operators of trace norm `||T e_k||_2`. The right-hand side of (2.2) is
exactly `tail_trace_tail` / `single_trace_tail` in `q8_schur_contour.py:216-221`.
This is `input_tail_only`.

The second term of (2.1) is the missing object.

### 2.2 Enlarged-contour Parseval — the output tail

Fix an inflation factor `theta > 1` for output disc `i` and suppose (gate G1,
§3.1) every branch image `f_k` is holomorphic on the closed disc
`|u| <= theta`. Set

```text
M_k^{(i,j)}(theta) := sup_{|u| = theta} | (T^{(i,j)} e_{j,k})(c_i + r_i u) | .
```

Parseval on the circle `|u| = theta`:

```text
sum_{m >= 0} theta^(2m) |T[m,k]|^2  =  || f_k ||^2_{L^2(|u|=theta)}
                                    <=  M_k(theta)^2 .
```

Drop all terms with `m < N` and use `theta^(2m) >= theta^(2N)` on the rest:

```text
sum_{m >= N} |T[m,k]|^2  <=  theta^(-2N) M_k(theta)^2 .                    (2.3)
```

That is the omitted-output row tail for a single column, geometric in `N`, in
the same Hardy/Hilbert norm. Summing over the retained columns:

```text
|| (I - P_N) T P_N ||_HS  <=  theta^(-N) * sqrt( sum_{k < N} M_k(theta)^2 ) .  (2.4)
```

### 2.3 Trace-norm propagation

Let `D_theta` be the diagonal operator `D_theta e_{i,m} = theta^m e_{i,m}`.
Then `(I-P_N) = (I-P_N) D_theta^{-1} D_theta` and
`|| (I-P_N) D_theta^{-1} ||_op = sup_{m>=N} theta^(-m) = theta^(-N)` for
`theta > 1`, so

```text
|| (I-P_N) T P_N ||_1  <=  theta^(-N) * || D_theta T P_N ||_1
                       <=  theta^(-N) * sum_{k < N} || D_theta T e_k ||_2
                       <=  theta^(-N) * sum_{k < N} M_k(theta) ,             (2.5)
```

the last step by the same Parseval identity as (2.3). Combining (2.1), (2.2),
(2.5):

```text
|| T - P_N T P_N ||_1  <=  tau_in(N) + tau_out(N; theta)                     (2.6)

tau_in(N)          =  sum_{k >= N} ( A q^k + C k rho^(k-1) )
                   =  A q^N/(1-q) + C * rho^(N-1)(N - (N-1) rho)/(1-rho)^2
tau_out(N; theta)  =  theta^(-N) * sum_{k < N} M_k(theta)
```

with `tau_in` **exactly** the checker's existing `tail_trace_tail`. Both terms
are in the same norm, both are explicit, both round UP.

### 2.4 Closed form for the output prefactor

The enlarged-contour sups obey the same envelope shape as the R2 receipt, with
`theta`-dependent constants (`A_theta`, `C_theta`, `rho_theta`) and a
`theta`-**independent** `q = |c_j|/r_j` (q depends only on the input disc):

```text
M_k(theta)  <=  A_theta q^k  +  C_theta k rho_theta^(k-1) ,                 (2.7)
```

so, using `(x+y)^2 <= 2x^2 + 2y^2`,

```text
sum_{k<N} M_k(theta)^2  <=  2 A_theta^2 * G_2(N,q)  +  2 C_theta^2 * S_2(N,rho_theta)
sum_{k<N} M_k(theta)    <=  A_theta * G_1(N,q)      +  C_theta * S_1(N,rho_theta)
```

with the elementary finite closed forms (all valid for any positive ratio, `< 1`
or not — this is why the split (2.1) was chosen):

```text
G_1(N,x) = sum_{k<N} x^k        = (1 - x^N)/(1 - x)                (x != 1; = N at x=1)
G_2(N,x) = sum_{k<N} x^(2k)     = (1 - x^(2N))/(1 - x^2)           (x != 1; = N at x=1)
S_1(N,x) = sum_{k<N} k x^(k-1)  = (1 - N x^(N-1) + (N-1) x^N)/(1-x)^2
                                                                    (x != 1; = N(N-1)/2 at x=1)
S_2(N,x) = sum_{k<N} k^2 x^(2k-2)                                   (= (N-1)N(2N-1)/6 at x=1;
                                otherwise the standard rational closed form in x^2)
```

At the optimal `theta` (§3.2) the binding `rho_theta` sits at 1, where
`S_2(N,1) = (N-1)N(2N-1)/6`, giving the clean asymptotic shape

```text
tau_out(N; theta*)  ~  theta*^(-N) * O(N^(3/2))    (HS)
                    ~  theta*^(-N) * O(N^2)        (trace) .
```

So the certified output tail is **geometric times polynomial**, with base
`1/theta*`.

---

## 3. Gates, the optimal theta, and what is still missing

### 3.1 G1 — holomorphy on the enlarged closed disc

`M_k(theta)` exists only if every branch image is holomorphic on
`|z - c_i| <= theta r_i`. Two sub-conditions, both already checked at
`theta = 1` by `f8_certify_tb_blocks.py` (`pole_clearance`,
`branch_cut_clearance`):

* **Pole.** The branch denominator `z -/+ n lambda` must not vanish on the
  closed disc: `theta < |c_i -/+ n lambda| / r_i`.
* **Branch cut.** The weight `(denominator^2)^(-s)` needs `denominator^2` off
  `(-inf, 0]`, i.e. `Re(denominator) != 0`. The discs are real-centred, so this
  is the *same* condition as pole clearance here.

Computed limits (Arb, 256 bits, from the pinned TB receipt):

```text
block (i,j,n,neg,tail)        theta <
(1,3,2,False,True)             3.597056274847714
(1,3,1,True, True)             3.397056274847714
(2,1,1,False,False)            2.664213562373095
(2,3,2,False,True)             6.785533905932738
(2,3,1,True, True)             5.578427124746190
(3,2,1,False,False)            2.914213562373095
(3,3,2,False,True)             6.328427124746190
(3,3,1,True, True)             3.914213562373095
```

G1 is therefore **not** the binding constraint. A third sub-condition applies
to the six Hurwitz-closed tail families: the deep-tail bound in
`q8_r2_local.deep_first_moment_bound` needs
`d = first_n*lambda -/+ c_i - theta*r_i > 0`, and the Hurwitz Taylor expansion
in `_tail_block_allcols_with_s_derivative` expands in the slope
`+/- theta r_i / lambda` about `a_0 = n_0 + n_head -/+ c_i/lambda`. With
`n_0 + n_head >= 5` and `theta r_i/lambda <= 0.53` at the theta of §3.2, both
have wide margin. Neither is binding either.

### 3.2 G2 — the decay rate, and the optimal theta

The effective decay rate of (2.4) is

```text
rate_i(theta)  =  max(1, rho_i(theta)) / theta ,
rho_i(theta)   =  max over blocks with output disc i of
                  sup_{|z-c_i| <= theta r_i} |(psi_n(z) - c_j)/r_j| ,
```

because `M_k ~ rho^k` makes `sqrt(sum_{k<N} M_k^2)` either `O(1)` (if
`rho < 1`) or `O(rho^N)` (if `rho > 1`). Each `psi_n` is a Mobius map, so
`rho_i(theta)` is exact in interval arithmetic: `psi_n(D(c_i, theta r_i))` is
the disc with centre `-/+ a/(a^2 - R^2)` and radius `R/(a^2 - R^2)`, with
`a = c_i -/+ n lambda`, `R = theta r_i`.

Computed (Arb, 256 bits; blocks with output disc `i`, `n` swept to 400 for the
tail families):

```text
per-output-disc optimum of max(1, rho_i(theta))/theta

  disc 1:  theta* = 1.845   rho_1 = 1.002117   rate = 0.543153
  disc 2:  theta* = 1.300   rho_2 = 0.997198   rate = 0.769231
  disc 3:  theta* = 1.235   rho_3 = 0.997209   rate = 0.809717
```

The optimum sits at `rho_i(theta) = 1` in every case, i.e. inflate the output
disc until the branch images just fill the input disc. A **uniform** theta is
capped by disc 3:

```text
theta_max (all 8 blocks, rho < 1)   = 1.2369074008682055
theta_max (all 8 blocks, rho < 0.99) = 1.230053
theta_max (all 8 blocks, rho < 0.95) = 1.202067
rho* at theta = 1 (TB receipt)       = 0.696590428020637535884545
```

**The binding block is `(3,2,1,False,False)` = `A3`**, the single-branch head
map disc 3 -> disc 2. It alone forces `theta <= 1.2369`.

Consequence, and it is the practically important one: the omitted-output tail
decays at rate `~0.8097^N`, whereas the certified input-column tail decays at
`~0.6966^N`. **The output side dominates by many orders of magnitude.** At the
checker's pinned `DEFAULT_N = 104` (`q8_schur_contour.py:50`):

```text
tau_in(104)  upper = 5.56204863545e-15     (recomputed from the pinned receipts)
tau_in(256)  upper = 3.44999455033e-39     (matches receipt tail_bounds "256")
tau_in(320)  upper = 3.04813402759e-49     (matches receipt tail_bounds "320")
theta^(-104) at theta = 1.2  = 5.82304854958e-9
```

so `tau_out(104)` is roughly `1e-6`, eight orders **worse** than `tau_in(104)`.
A larger `N` is required. Extrapolating the measured per-step rate 0.809866
from the validated `N = 16` quadrature total 1.19138 (§4):

```text
target 1e-12:  N >= 148 (HS),  N >= 161 (trace)
target 1e-15:  N >= 181 (HS),  N >= 194 (trace)     <- DIAGNOSTIC extrapolation
target 1e-18:  N >= 214 (HS),  N >= 226 (trace)
```

**CONJECTURAL, DIAGNOSTIC.** These are extrapolations from finite-`N`
measurements at the pin, not certified bounds. But the conclusion they point at
is robust and should be taken seriously: **`N = 104` is very likely too small
once the output tail is included; roughly `N >= 200` is needed.** This is a
real cost finding, not an incidental remark.

### 3.3 Why the finite-`k` split matters

At the optimum `rho_theta = 1`, so `sum_{k >= 0} M_k(theta)^2` **diverges**.
The splitting (2.1) is what makes the optimum usable: only `sum_{k < N}` ever
appears on the output side. A note using the other splitting
`(I-P_N)T + P_N T(I-P_N)` would need `rho_theta < 1` strictly and would be
forced to a strictly worse rate. This is not cosmetic.

### 3.4 What is actually missing — named

The derivation of §2 is complete as mathematics, **relative to** the
Hardy/Hilbert binding that the SOL and referee both already list as separately
OPEN ("Exact q=8 MMS-to-Hardy/Hilbert operator, basis, and norm binding"). It
is not a substitute for that binding and does not close it.

Given that binding, what remains is **one certification run, not one theorem**:

> **MISSING RECEIPT (L-OUT), CONJECTURAL.** An immutable Arb receipt asserting,
> for each of the eight eq.(32) blocks, a chosen admissible `theta_i > 1`, and
> each `k < K_head`:
>
> ```text
> M_k^{(i,j)}(theta_i)  <=  b_k^theta ,
> M_k^{(i,j)}(theta_i)  <=  A_theta q^k + C_theta k rho_theta^(k-1)  for k >= K_head,
> ```
>
> together with certified G1 holomorphy of the branch weight and of the
> Hurwitz-closed deep tail on the **closed** disc `|z - c_i| <= theta_i r_i`,
> and `rho_theta` from the enlarged Mobius image.

This is the *same* computation `q8_r2_local.py` already performs, with the arc
cover built at radius `theta_i * r_i` instead of `r_i`. It requires no new
analytic machinery. That is the honest, and I think the strongest, statement:
the gate is a computation that has not been run, not a lemma that is unknown.

Two hazards that a referee should attack, and that must be handled in L-OUT:

1. **Do not rescale the input basis.** For the blocks with `i == j` — `B3` =
   `(3,3)` — inflating output disc 3 by editing the geometry factors would also
   change the input disc 3 normalization `r_j`, silently changing the operator.
   The enlargement must apply to the **evaluation contour only**. The existing
   `exact_tail_columns_on_arc(s, z, c_j, r_j, lam, n0, neg, k_head)` already
   takes `c_j, r_j` as arguments independent of the arc points `z`, so building
   `arcs[i-1]` at radius `theta_i * r_i` while leaving `centers[j-1]`,
   `radii[j-1]` untouched is exactly right. A naive
   "multiply factor `i` by theta" rebuild is **wrong** for `B3`, and the probe
   in §4 reproduces the discrepancy.
2. **`rho_theta` must be swept over all `n >= n_0`,** not just `n = n_0`. The
   sup over `n` moves with `theta`: at `theta = 1` the worst `n` for the
   `(1,3,1,True)` family is deep in the tail, at `theta = 1.2` it is `n = 1`.

### 3.5 Gates NOT addressed here

Unchanged and still OPEN, verbatim from the SOL: E1 on the enlarged disc and
branch/pole holomorphy region; the exact q=8 MMS-to-Hardy/Hilbert operator,
basis and norm binding; nonvanishing and word/lattice identification of `K_s`;
common meromorphic continuation and the Selberg determinant/zeta/scattering
factorization; a complete corrected four-edge winding and a new independent
cold referee. Also unchanged: `recorded_tail_checks_pass` is false against the
pinned N=256/N=320 rows, an independent false gate this note does not touch.

---

## 4. Numerical receipts

Adverse test: compare the candidate bound against **brute-force** omitted-output
tail sums computed from the pinned engine at the pinned pin
`s = 0.4252310423737965 + 4.345760788321986 i`, factors `("10","4","2")`,
`sign = 1`, `n_head = 4`, `ctx.prec = 384`. The engine is imported unmodified;
no `lane_f/` file was edited. Probe:
`<scratchpad>/outtail_probe.py`.

The tested inequality is (2.3)+(2.4) in the form actually certifiable:

```text
brute  :=  || (I - P_N) T P_N ||_HS  =  sqrt( sum_{k<N} sum_{N<=m<MBIG} |T[m,k]|^2 )
bound  :=  theta^(-N) * sqrt( sum_{k<N} G_k(theta)^2 ),
           G_k(theta)^2 = sum_{m<MBIG} theta^(2m) |T[m,k]|^2   ( <= M_k(theta)^2 )
```

### 4.1 theta = 1.2 (rho < 1 regime), N = 10, MBIG = 90

```text
block   brute                 bound                 bound/brute   holds
  A2    6.518769e-01          4.006989e+00          6.147         True
  A3    4.894527e-01          2.481296e+00          5.07          True
  B1    2.038971e-02          9.038963e-01          44.33         True
  B2    1.207337e-04          2.810194e-01          2328          True
  B3    1.021735e-02          6.959273e-01          68.11         True
```

Same test at N = 6, MBIG = 34: holds for all five blocks (ratios 2.02, 2.11,
3.53, 30.7, 6.16). The prefactor `sqrt(sum_k M_k^2)` is stable in `N`
(A2: 24.757 at N=6, 24.810 at N=10), confirming the `k`-sum has converged.

### 4.2 theta = 1.2 and theta = 1.235 (rho >= 1 regime), MBIG = 70

Thirty cases, all hold; `theta = 1.235` is uniformly tighter, as §3.2 predicts:

```text
              theta = 1.2                      theta = 1.235
block  N     brute        bound         holds  bound         holds
  A2   8   1.69018e+00  5.76746e+00     True   5.31153e+00    True
  A2  12   2.58740e-01  2.78303e+00     True   2.28611e+00    True
  A2  16   4.92245e-02  1.34221e+00     True   9.82935e-01    True
  A3   8   1.07919e+00  3.56052e+00     True   3.28738e+00    True
  A3  12   2.35903e-01  1.72606e+00     True   1.42812e+00    True
  A3  16   6.41910e-02  8.33598e-01     True   6.16562e-01    True
  B1   8   1.13686e-01  1.30161e+00     True   1.13426e+00    True
  B1  12   3.44172e-03  6.27706e-01     True   4.87577e-01    True
  B1  16   1.11944e-04  3.02713e-01     True   2.09592e-01    True
  B2   8   1.61913e-03  4.04668e-01     True   3.37075e-01    True
  B2  12   8.91466e-06  1.95152e-01     True   1.44897e-01    True
  B2  16   6.23905e-08  9.41128e-02     True   6.22860e-02    True
  B3   8   4.85354e-02  1.00199e+00     True   8.60028e-01    True
  B3  12   2.47764e-03  4.83299e-01     True   3.69781e-01    True
  B3  16   2.07127e-04  2.33075e-01     True   1.58959e-01    True
```

**Rate check.** A2 at `theta = 1.235`: 5.31153 (N=8) -> 0.982935 (N=16), a
per-step factor `(0.982935/5.31153)^(1/8) = 0.809866`. The predicted rate from
the independent Mobius computation of §3.2 is `0.809717`. Agreement to
2e-4 — the geometry prediction and the measured decay are the same number. This
is the strongest single receipt in this note.

### 4.3 Naive-rebuild discrepancy (hazard 3.4.1, reproduced)

Recomputing the prefactor by scaling geometry factor `i` by `theta` agrees with
the direct `G_k` computation for A2, A3, B1, B2 (identical to 6 s.f.) and
**disagrees for B3** (`6.637150e-01` vs `6.959273e-01` at N=10), because B3 has
`i == j == 3` and the rebuild rescales the input basis too. Both values happen
to exceed `brute` here, so the error is not visible as a gate failure — which is
exactly why it must be excluded by construction rather than by testing.

### 4.4 Tooling

`/Users/za/.venvs/farey-rh/bin/python` (python-flint / Arb), `ctx.prec = 384`
for the engine probes and 256 for the Mobius/geometry sweeps. All reported
upper bounds use `arb.upper()`, i.e. rounded UP. Comparisons use
`bound.lower() >= brute.upper()`, the adverse direction.

---

## 5. How the existing checker would consume this — interface only

**No code change is proposed here and none was made.** The following is the
interface a future L-OUT receipt would present to
`lane_f/q8_schur_contour.py` so that its existing structure absorbs it.

### 5.1 New immutable receipt

A fourth pinned receipt, alongside R2 / TB / W, say
`f8_receipts/Q8_R2OUT_F1024_THETA_RECEIPT.json`, schema `q8-r2out-local/v1`,
produced by the enlarged-contour re-run of `q8_r2_local.py` described in §3.4.
Per block it carries the same keys the checker already parses, plus theta:

```json
{ "block": [3,2,1,false,false],
  "theta_exact_string": "1.2",
  "A_theta_upper_bound": "...",
  "C_theta_upper_bound": "...",
  "q_upper_bound": "...",
  "rho_theta_upper_bound": "...",
  "selected_column_bounds_theta": ["...", "..."],
  "holomorphy_gate": { "pole_clearance_pass": true,
                       "branch_cut_clearance_pass": true,
                       "deep_tail_d_lower_bound": "..." } }
```

It must bind `TB_sha256` and `W_sha256` exactly as the R2 receipt does, and its
`geometry` block must carry the **unscaled** `centers` / `source_radii` so the
checker's existing overlap test at `q8_schur_contour.py:295-318` still applies
unchanged, with `theta` recorded separately.

### 5.2 Consumption points in `load_operator_bounds`

Three sites, all already scaffolded by the repair:

1. `q8_schur_contour.py:393` — `"output_projection_tail": None` becomes the
   value of the closed form of §2.4:
   ```text
   output_projection_tail(N)  =  theta^(-N) * ( A_theta * G_1(N,q)
                                              + C_theta * S_1(N,rho_theta) )
   ```
   summed over blocks with the same Schur telescoping the input side already
   uses at `q8_schur_contour.py:351-358` (`trace[.]` replaced by the
   corresponding output tail, `hs[.]` factors unchanged).
2. `q8_schur_contour.py:394` — `"full_tau": None` becomes
   `input_tail_only + output_projection_tail`, i.e. (2.6). Both summands are
   trace-norm quantities in the same basis, so the sum is meaningful; this is
   the "propagated trace norm" the referee asks for.
3. `q8_schur_contour.py:395` — `"full_tail_certified": False` becomes true
   **only if** every new gate passes: the L-OUT receipt hash verifies, its
   `holomorphy_gate` fields are all true, `theta > 1` strictly, `rho_theta`
   from the receipt is reproduced by the checker's own Mobius computation, and
   `full_tau` is finite. Otherwise it stays false and the existing fail-closed
   path at `q8_schur_contour.py:717-721` and `746-790` is unchanged.

The per-arc gate `"full_output_projection_tail_available"`
(`q8_schur_contour.py:465`) then becomes satisfiable without any change to its
own logic. `recorded_tail_checks_pass` is a **separate** false gate and is not
addressed by any of this.

### 5.3 The N consequence

If §3.2's extrapolation survives certification, `DEFAULT_N = 104`
(`q8_schur_contour.py:50`) is insufficient once `output_projection_tail` is
live, and the production contour would need `N` near 200. That changes the
runtime class of the N=104 contour that "was not run", and should be planned
for rather than discovered.

---

## 6. Summary

* The gate asks for an omitted-output row/projection tail in the same
  Hardy/Hilbert norm as the input-column tail. §2 derives one:
  `||(I-P_N) T P_N||_HS <= theta^(-N) sqrt(sum_{k<N} M_k(theta)^2)` and its
  trace-norm counterpart, via Parseval on an enlarged contour.
* The mechanism is available because the R2 receipt's column bounds are
  boundary **sup-norms on the output disc**, not l2 column norms (§1.3). The
  identical computation on a circle of radius `theta r_i` yields the row decay.
* All constants are explicit and computable by the **existing** R2/TB/W
  pipeline re-run at the enlarged contour. No new analytic machinery is
  required, given the separately-OPEN Hardy/Hilbert binding.
* An admissible `theta > 1` demonstrably exists: `theta_max = 1.2369` uniform,
  binding block `(3,2,1,False,False)`; per-disc optima give rates 0.543 /
  0.769 / 0.810.
* The bound survives 45 adverse numerical comparisons against brute-force tail
  sums in both regimes, and its predicted decay rate matches the measured one
  to 2e-4.
* The output side decays much slower than the input side. `N = 104` is very
  likely too small; roughly `N >= 200`. DIAGNOSTIC.
* What is missing is named: receipt **L-OUT** (§3.4) — a certification run, not
  an unknown lemma — plus the pre-existing Hardy/Hilbert binding, on which all
  of the above is conditional.

Every claim above that is not a direct quotation, a recorded receipt value, or
an elementary identity is **CONJECTURAL**. Nothing here is confirmed. No file
was committed, pushed, or edited; one new file was written.

**READY FOR JUDGING.**

---

## Corrections (2026-08-20, per cold referee `Q8_OUTPUT_TAIL_REFEREE.md`, verdict GAPS NOT REFUTED)

### Correction (2026-08-20, referee defect 1):

Defective sentence, quoted verbatim from §4.2:

> Agreement to 2e-4 — the geometry prediction and the measured decay are the
> same number. This is the strongest single receipt in this note.

Corrected statement (referee §1(d), GAP 2): `5.31153` and `0.982935` are
values of the *bound*, not of the operator. The bound is defined as
`theta^{-N} * sqrt(sum_{k<N} G_k^2)` with an `N`-independent-to-first-order
prefactor, so its per-step factor is `1/theta = 1/1.235 = 0.809717` **by
construction**; the `2e-4` residual is merely the prefactor's drift. Nothing
about the Möbius geometry is tested by this check. The true measured decay of
the omitted-output tail, taken from this note's own §4.2 brute column, is
materially different per family: `~0.6427` (A2), `~0.7027` (A3), `~0.4208`
(B1), `~0.2807` (B2), `~0.5057` (B3) per step. The bound itself remains valid;
only the "strongest single receipt in this note" billing is withdrawn — it is
an overstatement of a self-check, not a corroboration of the geometry.

### Correction (2026-08-20, referee defect 2):

Defective sentence, quoted verbatim from §6:

> The bound survives 45 adverse numerical comparisons against brute-force tail
> sums in both regimes, and its predicted decay rate matches the measured one
> to 2e-4.

Corrected statement (referee §1(d), GAP 1): the count is **40**, not 45: §4.1
contains `5 + 5 = 10` and §4.2 contains `15 x 2 = 30`. The remaining 5 are
§4.3's naive-rebuild prefactor comparisons, which are not bound-vs-brute
comparisons at all — and one of them (`i == j == 3`, block B3) disagrees with
the direct computation *by construction*, since it exercises a rejected
geometry-rebuild route rather than the certified one.

### Correction (2026-08-20, referee defect 3):

Defective sentence, quoted verbatim from §3.2:

> so `tau_out(104)` is roughly `1e-6`, eight orders **worse** than
> `tau_in(104)`.

Corrected statement (referee §1(e), GAP 3): the same extrapolation at
`theta = 1.235` gives `1.19138 * 0.809866^88 = 1.04e-8` (HS), and `~1.6e-7`
after the note's own trace inflation. Neither figure is `1e-6`; "eight orders
worse" should read about **6.3 orders (HS) / 7.5 orders (trace)** worse than
`tau_in(104)`. The error is in the conservative direction and does not change
the qualitative conclusion — the `N >~ 200` headline is unaffected, since it
rests on the rate `0.809866`, which is correct, not on this figure.

### Correction (2026-08-20, referee defect 4):

Defective JSON schema, quoted verbatim from §5.1:

> ```json
> { "block": [3,2,1,false,false],
>   "theta_exact_string": "1.2",
>   "A_theta_upper_bound": "...",
>   "C_theta_upper_bound": "...",
>   "q_upper_bound": "...",
>   "rho_theta_upper_bound": "...",
>   "selected_column_bounds_theta": ["...", "..."],
>   "holomorphy_gate": { "pole_clearance_pass": true,
>                        "branch_cut_clearance_pass": true,
>                        "deep_tail_d_lower_bound": "..." } }
> ```

Corrected statement (referee §1(f), GAP 4, corrected form transcribed from
referee §3.3): `[3,2,1,false,false]` (`A3`) is a **single-branch head** block,
not a Hurwitz-closed tail family — `q8_r2_local.py:181-184` emits
`weight_sup_upper_bound` + `center_included_image_ratio_upper_bound` for
`tail == False`, and `A`/`C`/`q`/`rho` only for `tail == True`. Since `A3` is
precisely the **binding** block (§3.2), the schema above does not cover the
case that drives the rate. The corrected per-family split is:

* `tail == True` (the six Hurwitz families, all with `j == 3`, `q = 0.5`):
  `A_theta_upper_bound`, `C_theta_upper_bound`, `q_upper_bound`,
  `rho_theta_upper_bound`, `selected_column_bounds_theta` (`K_head + 1`
  entries), each an Arb `.upper()` string.
* `tail == False` (`A2 = (2,1,1,F,F)`, `A3 = (3,2,1,F,F)` — **including the
  binding block**): `weight_theta_sup_upper_bound`, `rho_theta_upper_bound`,
  `selected_column_bounds_theta`. The consumption formula for these is
  `theta^{-N} * W_theta * G_1(N, rho_theta)` (trace) and
  `theta^{-N} * W_theta * sqrt(G_2(N, rho_theta))` (HS) — **not** the
  `A q^k + C k rho^{k-1}` form used by the tail families.

### Correction (2026-08-20, referee defect 5):

Defective sentence, quoted verbatim from §6:

> An admissible `theta > 1` demonstrably exists: `theta_max = 1.2369` uniform,
> binding block `(3,2,1,False,False)`; per-disc optima give rates 0.543 /
> 0.769 / 0.810.

Corrected statement (referee §1(c), mislabelling GAP): `theta_max = 1.2369`
(`rho_theta < 1` uniform) is the *rate-optimal* `theta`, not the maximal
admissible one — `rho_theta >= 1` is fine per this note's own §3.3, so
`rho_theta < 1` is not an admissibility condition. The actual G1 admissibility
ceiling is **2.664** (the `(2,1,1,False,False)` pole-clearance limit). The
referee independently verified admissibility beyond `1.2369`, directly, at
`theta = 2.4` and `theta = 2.60` (both near the `2.664` pole ceiling; bound
still holds, though constants blow up as the pole is approached).

### Correction (2026-08-20, referee defect 6):

Defective sentence, quoted verbatim from §5.2:

> `"full_tau": None` becomes `input_tail_only + output_projection_tail`, i.e.
> (2.6). Both summands are trace-norm quantities in the same basis, so the sum
> is meaningful; this is the "propagated trace norm" the referee asks for.

Corrected statement (referee §1(f), GAP 5): the substitution is sound, but
"i.e. (2.6)" is a category slip. (2.6) is a single-operator inequality;
`input_tail_only` (`q8_schur_contour.py:351-358`) is the **telescoped** Schur
combination `trace[B3] + a3 trace[B2] + a3 a2 trace[B1] + trace[A3] b2 +
trace[A3] a2 b1 + a3 trace[A2] b1`. The licensing step, which must be stated
explicitly rather than left implicit in "i.e. (2.6)", is: telescoping
`X - X~` factor by factor requires substituting the **full** per-block defect
`tau_in + tau_out` into **each** `trace[.]` slot of that combination, with the
`hs[.]` factors unchanged — this is what §5.2.1 already prescribes elsewhere
in this note but does not connect to the "i.e. (2.6)" sentence, which a later
reader could otherwise take as licence to add the two totals in the wrong
order.

### Correction (2026-08-20, referee defect 7 — reproducibility):

Defective citations, quoted verbatim: from §4.4, "Probe:
`` `<scratchpad>/outtail_probe.py` ``."; from §3.2, "Computed (Arb, 256 bits;
blocks with output disc `i`, `n` swept to 400 for the tail families):".

Corrected statement (referee §1(g), reproducibility defect): `<scratchpad>/
outtail_probe.py` is a literal placeholder pointing into an ephemeral,
git-ignored session directory, and the §3.2 "Computed (Arb, 256 bits)"
geometry sweep (and the earlier pole/branch-cut sweep of §3.1) emits no
receipt file at all. Every §3.2/§4 number in this note is independently
reproduced by the referee (`Q8_OUTPUT_TAIL_REFEREE.md` §1(a)–(e)), but none of
them is repo-auditable as things stand. These numbers should be treated as
**reproduced-by-referee** (cite `Q8_OUTPUT_TAIL_REFEREE.md` §1(a)–(e) and §2),
not as repo-auditable receipts. Any future L-OUT lane must ship the sweep as a
tracked script plus a JSON receipt, not a scratchpad path.

### Correction (2026-08-20, referee defect 8 — stale sentence):

Defective sentence, quoted verbatim:

> No file was committed, pushed, or edited; one new file was written.

Corrected statement (referee §1(g)): this note is now tracked, added by
commit `b701cee`. The sentence above was accurate at the moment of writing but
is now stale.
