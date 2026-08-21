# q=8 mid-arc zero-exclusion failure — diagnosis

Date: 2026-08-20
Lane: G (diagnosis), branch `codex/prime-step-review-economic-validation`
Author: sol (diagnosis lane)
Scope: MAP entry "NEW FINDING: MID-ARC LEAVES CLEAR qOp BUT FAIL ZERO-EXCLUSION"

Status of every claim below is marked. CERTIFIED = read from an Arb
receipt. MEASURED = float point evaluation, NON-CERTIFIED. CONJECTURAL =
unproved model or projection.

## 0. Headline

The failure is **not** a determinant dip, **not** a nearby zero on the
contour, and **not** an N=262 tail floor. `|det|` has no dip anywhere on
the pin-box boundary: its minimum is `3.0011e-6` at each edge midpoint,
and it rises monotonically toward the corners.

The failure is **enclosure inflation in one scalar**, `H_trace_abs_upper`
(`q8_schur_contour.py:979`). `H` over-estimates the true logarithmic
derivative `|det'/det|` by a factor of **73x to 133x** (measured). That
single factor is what pushes `rH = radius * H` from a true `~0.008` up to
`~1.0` at depth 7, and `rH` near 1 is what blows the Taylor radius up by
`rH/(1-rH) ~ 281`.

Recommended action: **tighten `H`**, not deepen, not raise N, not re-pin.
Arithmetic in section 5.

## 1. Decomposition of `finite_taylor_box`

### 1.1 Exact formula from the code

`arc_certificate` (`research_notes/rh_goals_2026-08-14/lane_f/q8_schur_contour.py:885`):

- `radius = |end - start| / 2` (line 890) — half the leaf length.
- `A0 = I - C(midpoint)` (line 901); `midpoint_det = A0.det()` (line 982).
- `cprime_arc` = `C'` built on the **box** `s_arc` (lines 895-899).
- `cprime_t = direction * cprime_arc` (line 974).
- `normalized_delta = A0^-1 * delta`, `delta[i][j] = disc(radius * |cprime_arc[i][j]|_upper)`
  (lines 908-914).
- `correction = I - normalized_delta`; `J = correction^-1 * A0^-1 * (-cprime_t)` (lines 975-978).
- `H = |trace(J)|_upper` (line 979).
- `rH = radius * H` (line 980), gate `rH < 1` (line 981).
- **`taylor_radius = rho = radius * H * |midpoint_det|_upper / (1 - rH)`** (line 984),
  and `rho := 0` if the `rH < 1` gate fails (line 986).
- `finite_box = inflate(midpoint_det, rho)` (line 987), and `inflate`
  (line 870) adds `rho` to the real **and** imaginary radius — the box is
  a **square of half-side `rho`** centred on the `midpoint_det` ball.
- `finite_taylor_excludes_zero = abs_lower(finite_box) > 0` (lines 988-989).

Writing `rho = rH/(1-rH) * |det|`, the gate is scale-free in `|det|`:

> **excludes_zero  <=>  rho < max(|Re det|, |Im det|)  <=>  rH/(1-rH) < mu,
> where mu = max(|Re det|,|Im det|)/|det| in [1/sqrt(2), 1].**
>
> Equivalently **`rH < mu/(1+mu)`**, a threshold in `[0.4142, 0.5]`.

CERTIFIED verification of this criterion on the shard boundary
(`SHARD_a2_l64-128.ckpt.json`):

| leaf | rH | mu/(1+mu) | rho | max(&#124;Re&#124;,&#124;Im&#124;) | excludes_zero |
|---:|---:|---:|---:|---:|:--:|
| 118 | 0.44908 | 0.4300 | 3.2131e-6 | 2.9732e-6 | N |
| 119 | 0.43750 | 0.4319 | 3.0895e-6 | 3.0196e-6 | N |
| 120 | 0.42624 | 0.4337 | 2.9739e-6 | 3.0659e-6 | **Y** |
| 127 | 0.35802 | 0.4451 | 2.3577e-6 | 3.3905e-6 | **Y** |

The PASS/FAIL flip happens exactly where `rH` crosses `mu/(1+mu)`.

### 1.2 Radius-dependent vs radius-independent terms

**Radius-dependent:** `radius` (linear), and `H` weakly (its box-sup
component shrinks with the leaf).

**Radius-independent floor:** the only strictly radius-free quantity in
the box is the Arb enclosure error carried on `midpoint_det` itself —
`+/- 2.57e-87` (real) and `+/- 4.14e-86` (imag) at 384 bits on leaf 64.
That is **80 orders of magnitude** below `|det| ~ 3e-6`.

> **There is no meaningful floor.** `rho -> 0` linearly as `radius -> 0`.
> The MAP framing ("`midpoint_det ~ -4.69e-7` vs `finite_taylor_box` radius
> `8.44e-4`") compared `Re(det)` against `rho`; but `rho` is not a floor,
> it is `281 x |det|`, because `rH = 0.99645` makes `rH/(1-rH) = 280.7`.

There is however a **radius-independent structural constant**. CERTIFIED
across all 64 shard leaves:

> `|midpoint_det| * ||A0^-1||_F = 29.101` — **constant to 5 significant
> figures on every leaf** (`||A0^-1||_F = inv_arc_upper * (1 - qOp_upper)`,
> lines 956/915).

This is the near-singular structure `A0^-1 = adj(A0)/det(A0)` with
`||adj(A0)||_F ~ 29.101` essentially constant along the contour.
Consequently

> `H = 29.101 * kappa_F / |det|`, with `kappa_F = H*|det|/29.101` measured
> at **7.51 to 13.70** across the shard (an effective `||C'||_F`-type factor).

So the certificate condition becomes, in radius-independent form:

> **`radius < mu/(1+mu) * |det| / Lambda`, where `Lambda = 29.101 * kappa_F`
> in [218, 399].**

`Lambda` is the radius-independent floor constant the MAP was reaching for.

### 1.3 Evaluated on a failing and a passing leaf (CERTIFIED inputs)

| quantity | failing leaf 64 | passing leaf 120 |
|---|---:|---:|
| `radius` | 7.8125e-9 | 7.8125e-9 |
| `midpoint_det` | -4.6919e-7 + 2.9642e-6 i | -3.0659e-6 + 2.5740e-6 i |
| `\|det\|` | 3.0011e-6 | 4.0032e-6 |
| `H` | 1.2755e8 | 5.4558e7 |
| `\|\|A0^-1\|\|_F` | 9.6967e6 | 7.2695e6 |
| `\|det\| * \|\|A0^-1\|\|_F` | 29.101 | 29.101 |
| `kappa_F` | 13.15 | 7.51 |
| `Lambda = 29.101*kappa_F` | 382.7 | 218.5 |
| `rH` | 0.99645 | 0.42624 |
| `rH/(1-rH)` | 280.7 | 0.7429 |
| `rho` | 8.4322e-4 | 2.9739e-6 |
| `mu` | 0.9877 | 0.7659 |
| `mu/(1+mu)` threshold | 0.4969 | 0.4337 |
| verdict | FAIL (rH is 2.005x threshold) | PASS (margin 1.8%) |

Reproduces `rho` exactly: `0.99645/0.00355 * 3.0011e-6 = 8.424e-4` vs
recorded `8.4322e-4`.

## 2. Leaf profile from the checkpoint

The shard `SHARD_a2_l64-128.ckpt.json` is now **complete**: 64 leaves,
`PASS: 8`, `OPEN_MAX_DEPTH: 56`, `leaves_complete: true`, wall 11113 s.
(It held 60 records when the MAP entry was written; leaves 124-127 have
since landed and all four PASS.)

### 2.1 Correction to the MAP entry

The MAP says the failing leaves "fail only `finite_taylor_excludes_zero`".
CERTIFIED: that is true for leaf 64 and leaves 79-119, but **leaves 65-78
fail a different gate, `rH_lt_1`** (`rH` in [1.00090, 1.02903]). For those
leaves `taylor_radius` is forced to 0 (line 986), so their box degenerates
to the bare `midpoint_det` and `finite_taylor_excludes_zero` reports **true**
spuriously. Reading that flag without the `rH_lt_1` gate is misleading.

### 2.2 Full 64-leaf table

`s0` = pin centre `0.4252310423737965 + 4.345760788321986 i`;
`dist = |s_leafmid - s0|`; leaves run right-to-left along the top edge.

| leaf | Re(s) | dist(s,s0) | \|det\| | arg det | H | rH | mu/(1+mu) | rho | excl.0 | failing gate |
|---:|---|---:|---:|---:|---:|---:|---:|---:|:--:|---|
| 64 | 0.4252310423737965 | 1.0000e-06 | 3.0011e-06 | +1.7278 | 1.2755e+08 | 0.99645 | 0.4969 | 8.432e-04 | N | finite_lower_positive |
| 65 | 0.4252310267487965 | 1.0003e-06 | 3.0019e-06 | +1.7434 | 1.2842e+08 | 1.00326 | 0.4963 | 0.000e+00 | Y | rH_lt_1 |
| 66 | 0.4252310111237965 | 1.0008e-06 | 3.0033e-06 | +1.7590 | 1.2939e+08 | 1.01083 | 0.4955 | 0.000e+00 | Y | rH_lt_1 |
| 67 | 0.4252309954987965 | 1.0015e-06 | 3.0055e-06 | +1.7746 | 1.3019e+08 | 1.01710 | 0.4948 | 0.000e+00 | Y | rH_lt_1 |
| 68 | 0.4252309798737965 | 1.0025e-06 | 3.0084e-06 | +1.7902 | 1.3083e+08 | 1.02207 | 0.4939 | 0.000e+00 | Y | rH_lt_1 |
| 69 | 0.4252309642487965 | 1.0037e-06 | 3.0121e-06 | +1.8057 | 1.3129e+08 | 1.02572 | 0.4930 | 0.000e+00 | Y | rH_lt_1 |
| 70 | 0.4252309486237965 | 1.0051e-06 | 3.0165e-06 | +1.8212 | 1.3159e+08 | 1.02804 | 0.4921 | 0.000e+00 | Y | rH_lt_1 |
| 71 | 0.4252309329987965 | 1.0068e-06 | 3.0216e-06 | +1.8366 | 1.3172e+08 | 1.02903 | 0.4911 | 0.000e+00 | Y | rH_lt_1 |
| 72 | 0.4252309173737965 | 1.0088e-06 | 3.0274e-06 | +1.8520 | 1.3167e+08 | 1.02870 | 0.4900 | 0.000e+00 | Y | rH_lt_1 |
| 73 | 0.4252309017487965 | 1.0110e-06 | 3.0339e-06 | +1.8673 | 1.3147e+08 | 1.02707 | 0.4888 | 0.000e+00 | Y | rH_lt_1 |
| 74 | 0.4252308861237965 | 1.0134e-06 | 3.0412e-06 | +1.8826 | 1.3109e+08 | 1.02417 | 0.4876 | 0.000e+00 | Y | rH_lt_1 |
| 75 | 0.4252308704987965 | 1.0160e-06 | 3.0491e-06 | +1.8978 | 1.3056e+08 | 1.02001 | 0.4864 | 0.000e+00 | Y | rH_lt_1 |
| 76 | 0.4252308548737965 | 1.0189e-06 | 3.0577e-06 | +1.9128 | 1.2988e+08 | 1.01465 | 0.4851 | 0.000e+00 | Y | rH_lt_1 |
| 77 | 0.4252308392487965 | 1.0220e-06 | 3.0671e-06 | +1.9279 | 1.2904e+08 | 1.00815 | 0.4837 | 0.000e+00 | Y | rH_lt_1 |
| 78 | 0.4252308236237965 | 1.0253e-06 | 3.0771e-06 | +1.9428 | 1.2812e+08 | 1.00090 | 0.4823 | 0.000e+00 | Y | rH_lt_1 |
| 79 | 0.4252308079987965 | 1.0289e-06 | 3.0878e-06 | +1.9576 | 1.2707e+08 | 0.99271 | 0.4808 | 4.205e-04 | N | finite_lower_positive |
| 80 | 0.4252307923737965 | 1.0327e-06 | 3.0992e-06 | +1.9723 | 1.2592e+08 | 0.98374 | 0.4793 | 1.875e-04 | N | finite_lower_positive |
| 81 | 0.4252307767487965 | 1.0367e-06 | 3.1112e-06 | +1.9869 | 1.2466e+08 | 0.97390 | 0.4777 | 1.161e-04 | N | finite_lower_positive |
| 82 | 0.4252307611237965 | 1.0409e-06 | 3.1239e-06 | +2.0014 | 1.2329e+08 | 0.96323 | 0.4761 | 8.183e-05 | N | finite_lower_positive |
| 83 | 0.4252307454987965 | 1.0454e-06 | 3.1372e-06 | +2.0157 | 1.2186e+08 | 0.95206 | 0.4744 | 6.230e-05 | N | finite_lower_positive |
| 84 | 0.4252307298737965 | 1.0500e-06 | 3.1512e-06 | +2.0300 | 1.2033e+08 | 0.94008 | 0.4727 | 4.944e-05 | N | finite_lower_positive |
| 85 | 0.4252307142487965 | 1.0549e-06 | 3.1658e-06 | +2.0441 | 1.1871e+08 | 0.92742 | 0.4709 | 4.046e-05 | N | finite_lower_positive |
| 86 | 0.4252306986237965 | 1.0600e-06 | 3.1811e-06 | +2.0580 | 1.1700e+08 | 0.91410 | 0.4691 | 3.385e-05 | N | finite_lower_positive |
| 87 | 0.4252306829987965 | 1.0653e-06 | 3.1970e-06 | +2.0719 | 1.1522e+08 | 0.90016 | 0.4673 | 2.882e-05 | N | finite_lower_positive |
| 88 | 0.4252306673737965 | 1.0708e-06 | 3.2134e-06 | +2.0856 | 1.1337e+08 | 0.88567 | 0.4654 | 2.489e-05 | N | finite_lower_positive |
| 89 | 0.4252306517487965 | 1.0765e-06 | 3.2305e-06 | +2.0991 | 1.1145e+08 | 0.87071 | 0.4634 | 2.176e-05 | N | finite_lower_positive |
| 90 | 0.4252306361237965 | 1.0823e-06 | 3.2481e-06 | +2.1125 | 1.0948e+08 | 0.85533 | 0.4614 | 1.920e-05 | N | finite_lower_positive |
| 91 | 0.4252306204987965 | 1.0884e-06 | 3.2664e-06 | +2.1258 | 1.0750e+08 | 0.83988 | 0.4594 | 1.713e-05 | N | finite_lower_positive |
| 92 | 0.4252306048737965 | 1.0947e-06 | 3.2851e-06 | +2.1389 | 1.0550e+08 | 0.82425 | 0.4574 | 1.541e-05 | N | finite_lower_positive |
| 93 | 0.4252305892487965 | 1.1011e-06 | 3.3045e-06 | +2.1519 | 1.0347e+08 | 0.80839 | 0.4553 | 1.394e-05 | N | finite_lower_positive |
| 94 | 0.4252305736237965 | 1.1078e-06 | 3.3244e-06 | +2.1647 | 1.0142e+08 | 0.79232 | 0.4532 | 1.268e-05 | N | finite_lower_positive |
| 95 | 0.4252305579987965 | 1.1146e-06 | 3.3448e-06 | +2.1773 | 9.9358e+07 | 0.77623 | 0.4510 | 1.160e-05 | N | finite_lower_positive |
| 96 | 0.4252305423737965 | 1.1215e-06 | 3.3658e-06 | +2.1898 | 9.7301e+07 | 0.76016 | 0.4489 | 1.067e-05 | N | finite_lower_positive |
| 97 | 0.4252305267487965 | 1.1287e-06 | 3.3873e-06 | +2.2022 | 9.5331e+07 | 0.74478 | 0.4467 | 9.885e-06 | N | finite_lower_positive |
| 98 | 0.4252305111237965 | 1.1360e-06 | 3.4093e-06 | +2.2144 | 9.3370e+07 | 0.72945 | 0.4444 | 9.192e-06 | N | finite_lower_positive |
| 99 | 0.4252304954987965 | 1.1435e-06 | 3.4318e-06 | +2.2264 | 9.1406e+07 | 0.71411 | 0.4422 | 8.572e-06 | N | finite_lower_positive |
| 100 | 0.4252304798737965 | 1.1512e-06 | 3.4548e-06 | +2.2383 | 8.9444e+07 | 0.69878 | 0.4399 | 8.015e-06 | N | finite_lower_positive |
| 101 | 0.4252304642487965 | 1.1590e-06 | 3.4783e-06 | +2.2500 | 8.7485e+07 | 0.68348 | 0.4376 | 7.511e-06 | N | finite_lower_positive |
| 102 | 0.4252304486237965 | 1.1670e-06 | 3.5022e-06 | +2.2615 | 8.5534e+07 | 0.66823 | 0.4353 | 7.054e-06 | N | finite_lower_positive |
| 103 | 0.4252304329987965 | 1.1751e-06 | 3.5266e-06 | +2.2729 | 8.3593e+07 | 0.65307 | 0.4329 | 6.638e-06 | N | finite_lower_positive |
| 104 | 0.4252304173737965 | 1.1834e-06 | 3.5514e-06 | +2.2842 | 8.1665e+07 | 0.63801 | 0.4306 | 6.259e-06 | N | finite_lower_positive |
| 105 | 0.4252304017487965 | 1.1918e-06 | 3.5767e-06 | +2.2952 | 7.9755e+07 | 0.62309 | 0.4282 | 5.913e-06 | N | finite_lower_positive |
| 106 | 0.4252303861237965 | 1.2004e-06 | 3.6025e-06 | +2.3062 | 7.7868e+07 | 0.60834 | 0.4258 | 5.596e-06 | N | finite_lower_positive |
| 107 | 0.4252303704987965 | 1.2091e-06 | 3.6286e-06 | +2.3169 | 7.6007e+07 | 0.59380 | 0.4234 | 5.305e-06 | N | finite_lower_positive |
| 108 | 0.4252303548737965 | 1.2180e-06 | 3.6552e-06 | +2.3275 | 7.4171e+07 | 0.57946 | 0.4210 | 5.036e-06 | N | finite_lower_positive |
| 109 | 0.4252303392487965 | 1.2270e-06 | 3.6822e-06 | +2.3380 | 7.2361e+07 | 0.56532 | 0.4186 | 4.789e-06 | N | finite_lower_positive |
| 110 | 0.4252303236237965 | 1.2361e-06 | 3.7095e-06 | +2.3483 | 7.0581e+07 | 0.55141 | 0.4161 | 4.560e-06 | N | finite_lower_positive |
| 111 | 0.4252303079987965 | 1.2453e-06 | 3.7373e-06 | +2.3584 | 6.8830e+07 | 0.53773 | 0.4148 | 4.347e-06 | N | finite_lower_positive |
| 112 | 0.4252302923737965 | 1.2547e-06 | 3.7654e-06 | +2.3684 | 6.7109e+07 | 0.52429 | 0.4172 | 4.150e-06 | N | finite_lower_positive |
| 113 | 0.4252302767487965 | 1.2642e-06 | 3.7939e-06 | +2.3783 | 6.5421e+07 | 0.51110 | 0.4195 | 3.966e-06 | N | finite_lower_positive |
| 114 | 0.4252302611237965 | 1.2738e-06 | 3.8228e-06 | +2.3880 | 6.3765e+07 | 0.49816 | 0.4217 | 3.795e-06 | N | finite_lower_positive |
| 115 | 0.4252302454987965 | 1.2836e-06 | 3.8520e-06 | +2.3976 | 6.2143e+07 | 0.48549 | 0.4239 | 3.635e-06 | N | finite_lower_positive |
| 116 | 0.4252302298737965 | 1.2934e-06 | 3.8816e-06 | +2.4070 | 6.0554e+07 | 0.47308 | 0.4260 | 3.485e-06 | N | finite_lower_positive |
| 117 | 0.4252302142487965 | 1.3034e-06 | 3.9115e-06 | +2.4162 | 5.9001e+07 | 0.46095 | 0.4280 | 3.345e-06 | N | finite_lower_positive |
| 118 | 0.4252301986237965 | 1.3135e-06 | 3.9417e-06 | +2.4254 | 5.7483e+07 | 0.44908 | 0.4300 | 3.213e-06 | N | finite_lower_positive |
| 119 | 0.4252301829987965 | 1.3236e-06 | 3.9723e-06 | +2.4344 | 5.6000e+07 | 0.43750 | 0.4319 | 3.090e-06 | N | finite_lower_positive |
| 120 | 0.4252301673737965 | 1.3339e-06 | 4.0032e-06 | +2.4432 | 5.4558e+07 | 0.42624 | 0.4337 | 2.974e-06 | Y | - |
| 121 | 0.4252301517487965 | 1.3443e-06 | 4.0343e-06 | +2.4519 | 5.3210e+07 | 0.41570 | 0.4355 | 2.870e-06 | Y | - |
| 122 | 0.4252301361237965 | 1.3548e-06 | 4.0658e-06 | +2.4605 | 5.1893e+07 | 0.40541 | 0.4372 | 2.772e-06 | Y | - |
| 123 | 0.4252301204987965 | 1.3654e-06 | 4.0976e-06 | +2.4689 | 5.0606e+07 | 0.39536 | 0.4389 | 2.679e-06 | Y | - |
| 124 | 0.4252301048737965 | 1.3761e-06 | 4.1297e-06 | +2.4773 | 4.9350e+07 | 0.38555 | 0.4405 | 2.591e-06 | Y | - |
| 125 | 0.4252300892487965 | 1.3869e-06 | 4.1620e-06 | +2.4854 | 4.8147e+07 | 0.37615 | 0.4421 | 2.509e-06 | Y | - |
| 126 | 0.4252300736237965 | 1.3977e-06 | 4.1947e-06 | +2.4935 | 4.6973e+07 | 0.36698 | 0.4436 | 2.432e-06 | Y | - |
| 127 | 0.4252300579987965 | 1.4087e-06 | 4.2276e-06 | +2.5014 | 4.5827e+07 | 0.35802 | 0.4451 | 2.358e-06 | Y | - |

### 2.3 Is there a dip, a sign change, or a phase rotation?

CERTIFIED, from the table:

- **No dip.** `|det|` rises **monotonically** from `3.0011e-6` (leaf 64) to
  `4.2276e-6` (leaf 127). Leaf 64 is the midpoint of the top edge — the
  closest point of that edge to the box centre — so the shard already
  contains the arc minimum, and it is `3.0e-6`, four orders above any
  numerical floor.
- **No sign change.** `Re(det)` is negative on every leaf
  (`-4.69e-7 -> -3.39e-6`); `Im(det)` is positive on every leaf
  (`+2.96e-6 -> +2.53e-6`). `det` stays in the second quadrant throughout.
- **Smooth phase rotation, no jump.** `arg(det)` advances monotonically
  from `+1.7278` to `+2.5014` rad, total `+0.7736` rad over the half-edge,
  in steps of `~0.0124` rad/leaf with no discontinuity. A zero on or
  crossing the contour would show a rapid rotation or a `|det|` collapse;
  neither occurs.
- **`H` peaks where `|det|` is smallest**, `H = 1.3172e8` at leaf 71,
  falling to `4.5827e7` at leaf 127 — exactly the `H ~ 29.101*kappa_F/|det|`
  law of section 1.2, not a zero-proximity signature.

### 2.4 The determinant model (from CERTIFIED data, model CONJECTURAL)

Finite-differencing the 64 CERTIFIED `midpoint_det` values (spacing
`1.5625e-8`) gives the **true** logarithmic derivative:

| leaf | dist(s,s0) | true &#124;det'/det&#124; (fd) | 1/&#124;det'/det&#124; | certified H | inflation H/true |
|---:|---:|---:|---:|---:|---:|
| 65 | 1.0003e-6 | 9.9973e5 | 1.0003e-6 | 1.2842e8 | 128.5 |
| 74 | 1.0134e-6 | 9.8681e5 | 1.0134e-6 | 1.3109e8 | 132.8 |
| 89 | 1.0765e-6 | 9.2898e5 | 1.0765e-6 | 1.1145e8 | 120.0 |
| 104 | 1.1834e-6 | 8.4502e5 | 1.1834e-6 | 8.1665e7 | 96.6 |
| 119 | 1.3236e-6 | 7.5550e5 | 1.3236e-6 | 5.6000e7 | 74.1 |

`1/|det'/det|` **equals `dist(s, s0)` to 4 significant figures at every
leaf.** That is the signature of a **single simple zero of
`det(I - C_262)` located at the pin centre `s0` itself**, with

> `det(s) ~ A * (s - s0)`, `A = 2.9642 + 0.46919 i`, `|A| = 3.0011`.

Cross-check at leaf 127 (CERTIFIED): model predicts
`-3.4103e-6 + 2.4987e-6 i`; recorded `-3.3905e-6 + 2.5252e-6 i` — agreement
to 0.6% / 1.1% across the whole half-edge.

Independent MEASURED (NON-CERTIFIED) cross-check far outside the box, at
`s0 + 1e-3 i`, `N=96`, 96-bit: `det = -4.4129e-4 + 2.9692e-3 i`, vs model
`-4.6919e-4 + 2.9642e-3 i`. The linear model survives 1000x the box radius,
so the zero is isolated with no competitor nearby.

**Consequence (CONJECTURAL, model-based):** the zero is at the **exact
centre** of the pin box, `1e-6` from all four edges. `min |det|` on the
boundary is therefore `|A| * 1e-6 = 3.0011e-6`, attained at all four edge
midpoints, rising to `|A|*sqrt(2)*1e-6 = 4.2442e-6` at the corners. The
CERTIFIED arc-0 leaves 0-3 (`LOCAL_VALIDATION_a0_l0-4.json`,
`|det| = 4.2276e-6` at the bottom-left corner, `H = 4.5525e7`) match the
top-edge corner values (`4.2276e-6`, `4.5827e7`) to 0.7%, confirming the
model's four-fold prediction.

## 3. Float pre-scan of the four arcs

**NON-CERTIFIED.** Point evaluations of `det(I - C_N)` at `N = 96`,
96-bit precision, 48 samples per arc (192 points on the closed contour),
using `q8_r3b_engine.build_q8_block_matrices_and_s_derivative` and the
same Schur assembly `C = B3 + A3*B2 + A3*A2*B1`. Reduced `N` and reduced
precision: this locates dips and measures winding, it **certifies nothing**.
Script: scratchpad `scan2.py`; raw output `SCAN_N96.json`.

<!--SCAN-->

## 4. Verdict per arc

The governing inequality (section 1.1) is `rH = radius * H < mu/(1+mu)`,
with the worst-case threshold `mu = 1/sqrt(2)` giving `rH < 0.4142`.

**(a) The dips stay far above any floor — deeper subdivision suffices.**
There is no `|det|` value anywhere on the contour below `3.0e-6`; the
smallest CERTIFIED `finite_taylor_abs_lower` obstruction is a `rho` of
`8.4e-4`, which is `281x |det|` purely because `rH -> 1`. Option (b) of the
brief — "`|det|` below the floor, uncertifiable at N=262 at any depth" —
is **refuted**: `rho` is proportional to `radius`, so every leaf certifies
at sufficient depth.

**Required depth, per region (CERTIFIED `H`, extrapolation CONJECTURAL).**
Assume `H` does not grow under subdivision (conservative: `H`'s box-sup
component can only shrink). `radius(d) = 1e-6 * 2^(1-d)`, i.e. `7.8125e-9`
at depth 7.

| region of a half-edge (by dist to s0) | certified rH at depth 7 | depth needed |
|---|---:|---:|
| leaves 120-127 (dist >= 1.334e-6) | 0.358 - 0.426 | **7** (already PASS) |
| leaves 90-119 (dist 1.086e-6 - 1.327e-6) | 0.437 - 0.855 | **8** |
| leaves 64-89 (dist 1.000e-6 - 1.077e-6) | 0.867 - 1.029 | **9** |

Worst leaf 71: `H = 1.3172e8`, `rH(9) = 1.02903/4 = 0.2573 < 0.4911` — passes
with a 1.9x margin. Depth 8 gives `0.5145 > 0.4911` — fails. So **depth 9**
is the requirement for the middle ~40% of each edge.

**Per-arc verdicts.**

- **Arc 2 (top).** CERTIFIED complete for leaves 64-127: 8 PASS, 56 OPEN.
  All 56 fail for the `rH` reason, none for a `|det|` reason. Needs depth 8
  for leaves 90-119, depth 9 for leaves 64-89. By the section-2.4 model the
  mirror half (leaves 0-63) behaves identically.
- **Arcs 0, 1, 3.** No zero-exclusion failure has been *observed* yet
  because only the corner leaves have been run (`arc 0` leaves 0-3, all
  PASS at `rH ~ 0.36`). The model and the measured symmetry predict the
  **same** profile: the outer ~12% of each edge passes at depth 7, the rest
  does not. The arc-3 shard now running will, on this prediction, return
  **~8 PASS and ~56 OPEN**.

**Is the dip a zero near the boundary (bad placement) or inside the box
(the winding target)?** CERTIFIED phase profile (section 2.3) plus the
`1/|det'/det| = dist(s,s0)` identity (section 2.4) place the zero at the
box **centre**, `1e-6` from every edge — the maximum possible clearance for
this box. Placement is not merely acceptable, it is **optimal**. It is the
winding target, not a boundary intruder. **No re-pin is indicated.**

**Would raising N help?** No, and it is strictly harmful. The tail gates
are nowhere near binding at N=262 (CERTIFIED, leaf 64):
`tail_homotopy_upper = 1.92e-6` against a threshold of 1;
`full_tau_upper = 5.995e-18`; `input_tail_only_upper = 1.956e-37`. Five to
thirty orders of margin. `N` does not appear in the `rho` formula except
through `A0`, and raising `N` **increases** `||adj(A0)||_F` and the
262-term interval trace, so it would if anything **raise** `H`. Cost scales
as `N^3`. Verdict: **do not raise N.**

## 5. Economy call and the single recommendation

### 5.1 Measured unit cost

`SHARD_a2_l64-128`: 64 leaves, 11113 s wall, 12 workers
=> **174 s wall per leaf-node** (CERTIFIED from the checkpoint `timing`
block and `LOCAL_QUEUE.log`). Cost is dominated by the two `N=262` block
builds and is **independent of leaf size**, so a depth-9 node costs the
same as a depth-7 node.

Machine state at time of writing: load average 17.8, the `a3_l0-64` shard
running with 12 workers (`LOCAL_QUEUE.log`: `QUEUE START a3_l0-64`).

### 5.2 Are the running kernel's remaining leaves worth their CPU?

**Mostly no, at depth 7.** Prediction (CONJECTURAL, from the validated
model): of 512 depth-7 leaves on the full contour, only those with
`dist >= 1.330e-6`, i.e. `|x| >= 8.78e-7` of a 1e-6 half-edge, pass —
**16 per edge, 64 of 512 = 12.5%**. The running `a3` shard will spend
~3.1 h to bank ~8 PASS and ~56 OPEN_MAX_DEPTH.

Worse, the OPEN records are **not reusable**. `load_checkpoint`
(`q8_leaf_shard.py:213`) hard-fails on any `params` mismatch, and `params`
carries both `max_depth` and `checker_sha256`
(`q8_schur_contour.py:1035-1055`). So **any** change to `max_depth` or to
the checker source discards the entire checkpoint — all 68 leaf
evaluations banked so far (64 on a2 + 4 on a0), about **3.3 h of wall**.
That blast radius is identical for every option below, which is what makes
the comparison clean.

### 5.3 Cost of the three options in the brief

**(i) Continue and deepen locally, to depth 9.** Applying the per-leaf
criterion `rH(d) = rH(7) * 2^(7-d) < mu/(1+mu)` to all 64 CERTIFIED shard
leaves: **8 pass at depth 7, 36 at depth 8, 20 at depth 9, and none needs
depth 10** — so depth 9 is provably sufficient for the whole half-edge on
the conservative "H does not shrink" assumption. Adaptive node count
(1 node at depth 7, +2 at depth 8, +4 at depth 9):

    8*1 + 36*3 + 20*7 = 8 + 108 + 140 = 256 nodes per half-edge
    256 * 8 half-edges = 2048 nodes
    2048 * 174 s = 356,352 s = 99.0 h = 4.1 days

versus 512 nodes = 24.7 h for a depth-7-only sweep that would certify only
64/512 = 12.5% of the contour. **Route (i) works but costs 4.1 days.**

**(ii) Increase N.** Refuted in section 4: the tail has 5+ orders of
margin, `N` does not enter `rho`, and raising it raises `H` and costs
`O(N^3)`. **Estimated N that shrinks the tail floor below min|det|: already
satisfied at N=262 by 12 orders of magnitude.** No action.

**(iii) Re-pin.** The zero sits at the box centre, equidistant from all
four edges. Shifting the box **reduces** the minimum clearance and so
**tightens** the gate. Enlarging the box is first-order neutral: doubling
the half-width doubles `dist` (halving true `|det'/det|`) but also doubles
the arc length and therefore `radius` at fixed depth, leaving `rH`
unchanged, while adding leaves. Blast radius if done anyway: all 12 banked
PASS leaves, the pinned `pin` block in every checkpoint `params`, and the
L-OUT repin receipt binding
(`lane_g/l_out/Q8_R2OUT_F1024_REPIN_THETA1p230_RECEIPT.json`, pinned by
sha `15f1603a...` at `q8_schur_contour.py:67`). **Strictly harmful. Do not.**

### 5.4 The recommendation: option (iv), tighten `H`

None of (i)-(iii) addresses the cause. The cause is that `H` is a
**73x-133x over-estimate** of the quantity it bounds (section 2.4,
MEASURED against CERTIFIED finite differences).

Mechanism (diagnosed, CERTIFIED support): `H = |trace(J)|_upper` where `J`
is a product of three 262x262 **interval** matrices. The interval trace is
a sum of `262^2 = 68,644` terms whose radii add, destroying the near-total
cancellation present in the true trace. The observed ratio
`H / ||A0^-1||_F = 7.5 - 13.7` is exactly a Cauchy-Schwarz-style
`|tr(PQ)| <= ||P||_F ||Q||_F` loss, and `||A0^-1||_F = 29.101/|det|` blows
up near the zero — so `H` inherits the `1/|det|` singularity that the true
`det'/det` also has, but multiplied by a factor of ~100.

**Concrete tightening** (targets lines 973-981 only). Split

    tr(J) = tr(A0^-1 * (-C'_mid,t))  +  [ tr(J) - tr(A0^-1 * (-C'_mid,t)) ]

- First term at the **midpoint**, a point not a box. `midpoint_derivatives`
  is **already computed** at line 892 and currently unused for `H`, so this
  costs one extra 262-term trace and **no new `N=262` build**. Its magnitude
  is the true `|det'/det| ~ 1e6`.
- Second term is `O(radius)`: bound by
  `||A0^-1||_F * ||C'_arc - C'_mid||_F + ||(correction^-1 - I) A0^-1 C'_t||_F`.
  Both vanish with the leaf, unlike the current `O(1)` Frobenius bound.

**Projected effect (CONJECTURAL — the `||C''||_F` scale is not measured).**
If the tightened `H` lands within 10x of truth, `H ~ 1e7`:

Each arc has length `2e-6`, so a depth-`d` leaf has
`radius(d) = 1e-6 * 2^-d` (check: `d=7` gives `7.8125e-9`, as recorded).
Hence `rH(d) = 1e-6 * 2^-d * H`. With `H ~ 1e7`:

    rH(d) = 10 * 2^-d  <  0.4142   =>   2^d > 24.1   =>   d = 5
    depth 5: rH = 10/32 = 0.3125, margin 1.33x
    adaptive nodes 4 arcs * (1+2+4+8+16+32) = 4*63 = 252
    252 * 174 s = 43,848 s = 12.2 h

If it lands within 2x of truth, `H ~ 2e6`, then `rH(d) = 2 * 2^-d < 0.4142`
needs `d = 3`: `4*(1+2+4+8) = 60` nodes = `10,440 s` = **2.9 h**.

Even the pessimistic 10x case is **12.2 h against 99 h** — an **8.1x
saving**. The optimistic case is 34x. And the blast radius is the *same*
68 leaf evaluations (~3.3 h) that a `max_depth` bump would also cost, since
both invalidate the checkpoint `params`.

**Recommendation, one action:**

> **Stop the `a3` kernel after the current leaf, and open an engine lane to
> tighten `H` in `arc_certificate` (lines 973-981) using the already-computed
> midpoint derivative, before spending any more CPU at depth 7.**

Supporting arithmetic, side by side:

| route | wall to certify the closed contour | receipts destroyed | verdict |
|---|---:|---:|---|
| continue at depth 7 | 24.7 h, certifies 12.5% | 0 | incomplete, not a route |
| (i) deepen to depth 9 | **99 h** | 68 leaves (3.3 h) | works, expensive |
| (ii) raise N | > 99 h, no benefit | 68 leaves | harmful |
| (iii) re-pin | >= 99 h, tighter gate | 68 leaves + L-OUT binding | harmful |
| **(iv) tighten H** | **2.9 - 12.2 h** (CONJECTURAL) | 68 leaves (3.3 h) | **recommended** |

Fallback if (iv) does not reach 10x of truth: (i) remains available and
unaffected — the depth-9 route is a proven-sufficient backstop, and nothing
in (iv) forecloses it.

### 5.5 What is NOT claimed

- The location of the determinant zero at the pin centre is CONJECTURAL: it
  rests on a linear model fitted to CERTIFIED midpoint determinants and on
  NON-CERTIFIED float evaluation. It is not a certified zero-localisation.
- The winding number reported in section 3 is NON-CERTIFIED float.
- The projected `H` after tightening is CONJECTURAL; the `O(radius)`
  perturbation term has not been measured, only argued to be `O(radius)`.
- No file was edited, nothing was committed or pushed. The engine change in
  5.4 is a proposal, not an applied patch.

READY FOR JUDGING

---

## Dated correction block (2026-08-20, self-refutation + dtest verdict, append-only)

**The H-tightening recommendation of §2.4/§5.4 is WITHDRAWN — refuted by
this lane's own validation probe.**  Probe trace_test.py (Arb 384-bit,
N = 262, leaf-64 midpoint of SHARD_a2_l64-128):

```text
tr(A0^-1 * C'_mid) = 1.28000000605e8 + 10.14 i    (radius 7.1e-94, TIGHT)
certified H (box)  = 1.2755e8   -> box overhead 0.35%, not 73-133x
```

H is a faithful evaluation of |tr(A0^-1 C'_mid)|; the earlier "73-133x
inflation" was the ratio H / (finite-difference |det'/det|), wrongly
attributed to enclosure loss.  Do NOT tighten H; there is nothing loose
to tighten.

**dtest verdict (orchestrator, post-restore): C' EXONERATED.**
Entrywise central finite differences of C vs the engine's derivative
blocks at N = 96, 8 entries including deep ones: ratio = 1 to ~1e-17
relative on every entry (dtest.py, quoted in the session ledger).
build_q8_block_matrices_and_s_derivative DOES return dC/ds.

**The real open question (now the headline):** the engine's two outputs
for d/ds log det at the leaf-64 midpoint are mutually inconsistent —
finite differences of 64 CERTIFIED midpoint_det values give magnitude
~1.0e6 essentially pure imaginary; -tr(A0^-1 C'_mid) gives 1.28e8
essentially pure real — 128x apart in magnitude and 90 degrees in
phase.  With C' verified correct, suspicion moves to WHICH inverse the
trace/Taylor bound should carry: the anchor A0^-1 versus the true
(I - C(s))^-1, and/or the directional-derivative convention along the
arc.  Note 1/dist(s_mid, box centre) ~ 1e6 matches the finite-difference
magnitude — consistent with d/ds log det being dominated by the simple
zero at the centre, as §4's scan found.  If the engine's A0^-1-based H
is a legitimately conservative surrogate, the 12 banked PASS leaves
remain sound and the failing leaves may unlock under the correct
quantity; if the Taylor bound REQUIRES the true log-derivative, the
gate derivation must be re-audited.  DERIVATIVE-SEMANTICS LANE assigned;
everything in §2.4/§5.4 that consumed the refuted diagnosis is
superseded by this block.

## Dated correction block (2026-08-21 #2, supersedes correction block #1 — append-only)

**The "128x / 90-degree" inconsistency DOES NOT EXIST.**  Independently
re-measured (referee lane, N = 64, arc 3 leaf path 0101010, and N = 48,
arc 2 leaf 64): `-tr(A0^-1 C'_mid)` equals an end-to-end central finite
difference of `det(I - C(s))` to 1.9e-22 (h = 1e-11) and 1.9e-24
(h = 1e-12) relative, with magnitude ~1.0e6 — matching the finite
differences of the certified `midpoint_det` values.  The
`1.28000000605e8` of correction block #1 came from a probe
(`trace_test.py`, not present in the repo) whose value agrees with
`1/radius = 1/7.8125e-9 = 1.28e8` to 8 significant figures.  It was not a
trace.  **The which-inverse question is CLOSED:** lines 973-979 of
`q8_schur_contour.py` carry the true arc inverse via the exact anchored
factorization `A(s)^-1 = (I - A0^-1 dC)^-1 A0^-1`; `tr(A0^-1 C')` is
never used as the gate quantity.  The directional convention is also
correct on all four edges.

**Correction to correction block #1's stated reason for withdrawing
H-tightening.**  The claim "box overhead 0.35%, not 73-133x" is FALSE.
Measured at the leaf-64 midpoint, N = 48: `|tr(A0^-1 C'_mid)| = 9.99970e5`,
arc-box `|tr(A0^-1 C'_arcbox)| = 1.000008e6` (1.0000381x), production
`H = 1.2754593e8` (**127.55x**).  100% of the slack is the
`correction_inverse` factor.  The withdrawal of §2.4/§5.4 STANDS, but for
the correct reason: the slack is a structural limit of norm-type bounds on
a near-cancelling trace, and closing it needs a rigorous nuclear-norm
bound on `A0^-1 C'` that the codebase does not have.

**§5.2's threshold `rH < mu/(1+mu)`, `mu in [1/sqrt(2), 1]`, is CONFIRMED
and takes priority** over any later "rH < 1/2" statement: `inflate()`
builds a square box, and six leaves of `SHARD_a2_l64-128` with
`rH` in (0.4375, 0.4982) — all below 1/2 — have
`finite_taylor_excludes_zero = false`.  The safe per-leaf predictor is
`rH < 1/(1+sqrt(2)) = 0.41421`.
