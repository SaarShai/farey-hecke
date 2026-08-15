# M1C — q=4 / level-2 modular containment kill-test

**Date:** 2026-08-14  
**Scope:** numerical falsification probe for the candidate q=4 intertwiner `(I_4)` in `M1B_Q4_INTERTWINER.md`. This is finite-dimensional evidence only; it is not a proof of divisor containment or of `(I_4)`.

## Verdict

**CONTAINMENT SUPPORTED (finite numerical probe; not proved).**

At the real q=4 pin `s=1` and at all three q=4 `mms+` pins carried by the lane-b receipt, the level-2 vector-valued modular determinant is below `1e-8` at both `N=40` and `N=60`. The least-small modular value is `1.27e-17`. Two off-zero controls give determinants of order one on both sides, so the result is not explained by a trivially vanishing implementation.

The q=4 pin at `0.25 + 12.50542878996472 i` is the shallowest q=4 zero in this run (`|D_4| = 1.6121e-9`), but it is stable between `N=40` and `N=60` to about `3e-13`; its modular determinant is `1.27e-17`–`1.56e-17`.

## Operators and source authority

### Build A: MMS q=4

Build A was called from the existing even-q builder, without copying or modifying it:

`/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py`

The called path was `cert_det_complex_mid(s, N, sign=+1, q=4, n_head=4)`, implementing the MMS even-q eq. (32) `mms+` block. For q=4 this is

```text
D4(s) = det(1 - L^(4)_{s,+})
     = det(1 - L^infinity_{2,s} - L^infinity_{-1,s}).
```

The q=4 builder uses its own normalized Taylor geometry (`kappa=h_4=1`); the two basis sizes were `N=40,60`.

### Build B: Fraczek–Mayer level 2

The implementation follows [Fraczek–Mayer, arXiv:1011.4441](https://arxiv.org/abs/1011.4441), §2, equations (2.0.2)–(2.0.3): the standard Mayer disc `D={|z-1|<3/2}`, with

```text
M_{2,s} = [[0, M^+_{2,s}], [M^-_{2,s}, 0]],
(M^+/-_{2,s} f)(z) = sum_{m>=1} (z+m)^(-2s)
    rho_2(S T^(+/-m)) f(1/(z+m)).
```

The vector basis was the normalized Taylor basis

```text
z0 = (sqrt(5)-1)/2 = 0.6180339887498948...
u  = (z-z0)/0.30,
e_k(z) = u^k,  k=0,...,N-1.
```

The finite head was `m=1,...,4`; the two parity tails were evaluated by the exact Hurwitz-zeta continuation used by the existing `zeta_cert_rosen_q5.py` primitive. The level-2 `T` action has order two, so `rho_2(ST^{-m})=rho_2(ST^{m})`; consequently `M^+_{2,s}=M^-_{2,s}` in this representation and `det(1-M_{2,s})` and `det(1+M_{2,s})` agree.

The existing q=4 pin source is [lane_b/Q4Q6_CONTROLS_RECEIPT.json](../lane_b/Q4Q6_CONTROLS_RECEIPT.json).

## Explicit level-2 coset representation

Using right-coset representatives `R_1=I`, `R_2=S`, `R_3=ST` and the convention `R_i g in Gamma_0(2) R_j`, the permutation matrices are

```text
rho_2(S) = [[0,1,0],
            [1,0,0],
            [0,0,1]]

rho_2(T) = [[1,0,0],
            [0,0,1],
            [0,1,0]].
```

Fresh exact integer checks returned:

```text
rho_2(S)^2       = I_3       PASS
rho_2(ST)^3      = I_3       PASS
rho_2(T)^2       = I_3       PASS
rho_2(ST^m)      = rho_2(ST^(-m)), 1 <= m <= 12   PASS
```

### Fricke-action attempt

The projective integer representative of `W_2` is `[[0,-1],[2,0]]`. Modulo 2 it is singular, so it does not define a permutation of `P^1(F_2)`, the three-point model underlying the `rho_2` coset action. Independently, an exhaustive search over the six `3 x 3` permutation matrices found only the identity satisfying

```text
P rho_2(S) = rho_2(S) P,
P rho_2(T) = rho_2(T^(-1)) P.
```

Therefore no nontrivial, honest `3 x 3` Fricke permutation action was used, and no Fricke-plus subdeterminants are claimed. This is an unresolved structural limitation of the probe, not a reason to silently identify the congruence determinant with the q=4 Fricke-plus block.

## Numerical table

All entries are midpoint values of the finite `N` determinant. `D_4` is Build A. The two modular columns are Build B. The controls are deliberately away from the listed q=4 pins.

| point | `N` | `|D_4(s)|` | `|det(1-M_{2,s})|` | `|det(1+M_{2,s})|` |
|---|---:|---:|---:|---:|
| `s=1` real pin | 40 | `8.0571062500e-26` | `9.8415611738e-19` | `9.8415611738e-19` |
| `s=1` real pin | 60 | `1.1849377704e-37` | `2.9040501692e-27` | `2.9040501692e-27` |
| q4 pin 1: `0.25+7.067362570867346i` | 40 | `2.8293558613e-15` | `1.5419890403e-29` | `1.5419890403e-29` |
| q4 pin 1 | 60 | `2.8293443737e-15` | `1.5437606688e-29` | `1.5437606688e-29` |
| q4 pin 2: `0.25+10.511019819386503i` | 40 | `2.7425503022e-12` | `2.4662138651e-22` | `2.4662138651e-22` |
| q4 pin 2 | 60 | `2.7427305139e-12` | `1.8786274590e-22` | `1.8786274590e-22` |
| q4 pin 3: `0.25+12.50542878996472i` | 40 | `1.6121261085e-9` | `1.5573479154e-17` | `1.5573479154e-17` |
| q4 pin 3 | 60 | `1.6123846574e-9` | `1.2697331287e-17` | `1.2697331287e-17` |
| control: `0.25+8i` | 40 | `2.9768170606` | `21.7782014000` | `21.7782014000` |
| control: `0.25+8i` | 60 | `2.9768351787` | `21.7782014000` | `21.7782014000` |
| control: `0.75+0.25i` | 40 | `1.5965451300` | `3.5835861245` | `3.5835861245` |
| control: `0.75+0.25i` | 60 | `1.5965182336` | `3.5835861245` | `3.5835861245` |

## Convergence and interpretation

- The real `s=1` pin and all three complex q=4 pins remain zeros under `N=40 -> 60`; the modular determinant values are much smaller than the requested `1e-8` threshold.
- The two controls remain order one: the smallest q=4 control magnitude is `1.5965`, and the smallest modular control magnitude is `3.5836`.
- The modular `+` and `-` determinants agree because the explicit level-2 representation makes the `+m` and `-m` branch matrices equal. This agreement is an algebraic control, not an extra Fricke factorization.
- No argument-principle isolation, multiplicity calculation, global zero scan, or determinant-preserving MMS-to-Fraczek–Mayer intertwiner was attempted.

The evidence supports the narrow prediction that the level-2 congruence determinant vanishes at the tested q=4 divisor points under this finite truncation and convention. It does **not** prove `Z_{Gamma_0(2)} superset Z_{Gamma_0^+(2)}` globally, does not prove `(I_4)`, and does not settle the missing Fricke-plus restriction or the MMS `K_s` divisor.

The machine-readable receipt is [M1C_Q4_KILLTEST_RECEIPT.json](M1C_Q4_KILLTEST_RECEIPT.json). The computation requested `nice -n 15`; the host emitted `nice: setpriority: Operation not permitted`, so the priority reduction was not granted. The run nevertheless used only `N=40,60`, two controls, three existing lane-b pins, and the real `s=1` pin, and completed in about 52 seconds. No source, builder, lane-b file, or unrelated worktree file was written.
