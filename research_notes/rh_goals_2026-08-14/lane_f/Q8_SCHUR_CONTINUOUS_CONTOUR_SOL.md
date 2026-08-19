# q=8 Schur-reduced continuous-contour lane

Status: **OPEN; AWAITING COLD REFEREE.** This note records a theorem-oriented
implementation and a bounded edge certificate. It does **not** claim the q=8
law or an unconditional full proof. E1, exact q=8 MMS/Hilbert binding, `K_s`,
common continuation, and Selberg factorization remain **OPEN**.

## Exact reduction and domains

The production evaluator is `q8_schur_contour.py`. It consumes the direct q=8
block dictionaries exposed by `q8_r3b_engine.py`; the new production path does
not allocate the legacy `3*N` matrix. The five nonzero q=8 MMS-(32) blocks are
typed as

```text
A2 : H1 -> H2       A3 : H2 -> H3
B1 : H3 -> H1       B2 : H3 -> H2       B3 : H3 -> H3.
```

Thus the eliminated return map on `H3` is exactly

```text
C_N = B3 + A3*B2 + A3*A2*B1,
C_N' = B3'
      + A3'*B2 + A3*B2'
      + A3'*A2*B1 + A3*A2'*B1 + A3*A2*B1'.
```

The finite block determinant identity is `det(I-L_N)=det(I-C_N)`. The direct
evaluator was checked against the compatibility 3-block assembly:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... build_q8_block_matrices_and_s_derivative; build_reduced_matrix_and_s_derivative ...
PY
N 2 abs_upper [9.33818479707285358085109e-87 +/- 4.84e-111]
N 4 abs_upper [1.12757903328632728496784e-84 +/- 4.88e-108]
N 8 abs_upper [5.18392836627278901446578e-84 +/- 4.13e-108]
```

These are finite Arb identity radii only; no theorem status is upgraded by
this check.

## Continuous closed-subarc enclosure

For a closed horizontal/vertical segment with midpoint `s0`, radius `r`, and
complex unit direction `v`, the checker evaluates the derivative on the Acb
rectangle and uses the line-integral enclosure

```text
|C_N(s)-C_N(s0)| <= r * sup_arc |C_N'(s)|.
```

This avoids the refuted endpoint-only predicate and the severe dependency
inflation of directly subtracting two broad Acb evaluations. With
`A0=I-C_N(s0)`, it forms the interval `delta` from that derivative bound and
uses only Frobenius/Hilbert bounds:

```text
qF       = || A0^(-1) delta ||_F,
inv_arc  <= ||A0^(-1)||_F / (1-qF),
```

requiring `qF<1`. No matrix infinity norm is substituted for this gate.

The finite determinant box is the Jacobi/Taylor box

```text
H  = |tr((I-A0^(-1)delta)^(-1) A0^(-1) (-v C_N'))|,
rH = r*H,
|det(I-C_N(s))-det(I-C_N(s0))|
    <= r*H*|det(I-C_N(s0))|/(1-rH).
```

Strict `rH<1` and positive lower modulus are required. Ordered boxes then go
to the adjacent-overlap/half-plane winding checker. Any failed strict gate is
recursively bisected; an unresolved leaf leaves the run `OPEN`.

## Fredholm trace-norm homotopy bound

The pinned R2 receipt is loaded with local tracked TB/W receipts and their
source hashes are checked. For a tail family, with selected column bounds
`b_k`, `K` the first omitted index, and R2 parameters `A,C,q,rho`, the checker
uses the Arb upper bound

```text
HS <= sqrt(sum_{k<K} b_k^2
           + 2*A^2*q^(2K)/(1-q^2)
           + 2*C^2*sum_{k>=K} k^2*rho^(2k-2)).
```

The last sum is evaluated by the exact closed form

```text
sum_{k>=K} k^2*x^k
 = x^K*(K^2 + (-2*K^2+2*K+1)*x + (K-1)^2*x^2)/(1-x)^3,
```

with `x=rho^2` and the additional factor `rho^-2`. A single branch uses
`w/sqrt(1-rho^2)`. The signed `-1` family is included in each `B_j` bound by
the triangle inequality.

With `a2,a3,b1,b2,b3` the resulting HS bounds, the operator bound is

```text
Xop = b3 + a3*b2 + a3*a2*b1.
```

The domain chain is `H3 -> H1 -> H2 -> H3` for `A3*A2*B1`, and the finite
return map is `X_N P3`. The trace-norm decomposition used by the checker is
`C - X_N P3`, with telescoping bound

```text
tau = tb3 + a3*tb2 + a3*a2*tb1
    + ta3*b2 + ta3*a2*b1 + a3*ta2*b1.
```

For each arc, the Woodbury-style finite inverse bound and homotopy gate are

```text
||(I-X_N P3)^(-1)|| <= 1 + Xop*inv_arc,
tail_homotopy = tau*(1 + Xop*inv_arc) < 1.
```

This is a trace-class/Fredholm comparison gate, not the missing MMS/Hilbert
identification or Selberg factorization.

Receipt for the pinned parameters and recomputed R2 tails:

```text
PYTHONDONTWRITEBYTECODE=1 /Users/za/.venvs/farey-rh/bin/python - <<'PY'
... load_operator_bounds(..., 104) ...
PY
A2 A3 B1 B2 B3 [37.190070676935277472 +/- 1.57e-19] [22.743685837096234236 +/- 1.02e-20] [13.387099102591173655 +/- 2.26e-19] [4.0764068877755438397 +/- 2.67e-20] [11.334579588543742426 +/- 4.08e-21]
Xop [11427.381413421776648 +/- 3.43e-17] tau104 [1.2647466890578745041e-12 +/- 4.50e-32]
256 source [3.4499945503265230464527639567213577262548803647375061 recomputed [3.4499945503265230464527639616863099255625617512283535 True
320 source [3.0481340275887105508444872207199434529464104721998028 recomputed [3.0481340275887105508444872262383532961899005733383455 True
```

The displayed source/recomputed prefixes are a compact receipt; the checker
compares the complete Arb intervals and prints `True` for both rows.

## Bounded q=8 edge result

The first unsplit `N=104` bottom edge fails the continuous Frobenius radius
gate at the requested initial width:

```text
python3 - <<'PY'  # reads /tmp/q8_schur_104.json from the exact runner command
...
PY
status OPEN runtime_seconds 67.31261908399756 arc_status OPEN_MAX_DEPTH qF [2.6890663136436820935 +/- 6.51e-17] arc_count 1
```

The targeted depth-2 adaptive run for that same bottom edge produced four
strictly passing leaves. Its output is **a shard**, so winding remains `null`
and the overall status remains `OPEN`:

```text
python3 - <<'PY'  # reads /tmp/q8_schur_n104_edge0_d2.json
...
PY
status OPEN finite_arc_count 4 runtime_seconds 473.2811248329963
path [0, 0] status PASS qF [0.53756911537515361665 +/- 2.15e-17] tail [0.054882770307790165742 +/- 1.33e-18] rH [0.20867394620966853158 +/- 9.49e-18] lower [2.4443623893264283819e-6 +/- 2.04e-22]
path [0, 1] status PASS qF [0.65189710970098169174 +/- 5.32e-17] tail [0.088413874889147037184 +/- 3.81e-18] rH [0.24722721234097563836 +/- 1.09e-17] lower [2.0632692022230975622e-6 +/- 1.84e-22]
path [1, 0] status PASS qF [0.65189591800013735323 +/- 3.91e-17] tail [0.088413501635079161378 +/- 3.56e-18] rH [0.23759983110657900696 +/- 1.04e-17] lower [1.9053528178819682385e-6 +/- 7.31e-23]
path [1, 1] status PASS qF [0.53756615765659410133 +/- 5.08e-17] tail [0.054882287844598129367 +/- 1.42e-18] rH [0.19233211447125186933 +/- 8.45e-19] lower [2.4880136644858425931e-6 +/- 1.68e-24]
```

The shard status is conservative: the edge passed, but no closed four-edge
winding was run in this bounded receipt.

## Deterministic sharding/checkpointing

`q8_schur_contour.py` accepts `--arc-start`, `--arc-end`, `--checkpoint`, and
`--resume`. Initial arcs are ordered bottom, right, top, left. Checkpoint
records include exact run parameters and subdivision paths, and are intended
for deterministic local/Kaggle sharding. Kaggle was **not launched** in this
lane. No generated checkpoint or cache is part of this commit.

## Remaining gates

1. Run/harvest the full `N=104`, `K=1`, depth-2 four-edge contour and obtain a
   certified ordered winding. Until that result exists, the q=8 continuous
   contour is **OPEN**.
2. Obtain a separate adversarial cold referee for this implementation before
   any status upgrade; current proof-oriented claims are **AWAITING COLD
   REFEREE**.
3. Prove E1 on the enlarged disc, exact q=8 MMS-to-Hilbert/operator binding,
   nonvanishing `K_s`, common continuation, and Selberg factorization. These
   are independent **OPEN** gates and are not implied by the finite contour or
   the trace-norm homotopy computation.
