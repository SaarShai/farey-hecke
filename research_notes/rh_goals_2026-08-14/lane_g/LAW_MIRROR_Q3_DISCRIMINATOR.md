# LAW — the `q = 3` mirror discriminator: (a) U4 or (b) the Teo assembly?

**Date:** 2026-08-16. **Lane G, compute lane.** This note executes the single named next act of
`lane_g/LAW_STRIP_AND_MIRROR.md` §5, and nothing else.

**Parent read in full:** `lane_g/LAW_STRIP_AND_MIRROR.md` (§3.1 the mirror identity, §3.3 the
measurement, §3.4 the arithmetic discriminator, §3.6 the Barnes-bracket localisation, §5 the act).
**Every number here inherits the parent's pendency**: `LAW_U1PHI_PROOF_ROUTE.md` and
`LAW_U1_GROWTH.md` §3.1's Teo transcription are both `PENDING ADVERSARIAL VERIFICATION`. All
determinants are float midpoints of the Arb builder, **no interval arithmetic, no winding
certificate**.

**No `git` command was run. Nothing was committed. `lane_f/` and every other lane are untouched.
No existing probe file was modified — the three new probes carry a `q3` name.**

---

## 0. Verdict up front

> ### **`(*)` FAILS AT `q = 3` TOO — by `9.2e4` to `5.8e6`, `N`-converged to `1e−16`. By the pre-registered rule the fault is (b), THE TEO `κ_q` ASSEMBLY. U4 is NOT refuted by the mirror test.**
>
> And the fault is localised further than the rule required: **the Barnes-bracket exponent carries
> the wrong SIGN.** Back-solving the exponent `e` that would make `(*)` hold returns
> `e ≈ −(1−2/q)/2` — the exact negative of the transcribed `(1−2/q)/2` — independently at
> `q = 3, 4, 6` and at every `σ`, to `1–4 %`. Flipping that one sign collapses a `10⁵`–`10¹⁹`
> disagreement to a residual factor of **`0.42`–`1.83`**.

---

## 1. The pre-registered rule, quoted before the numbers

From `LAW_STRIP_AND_MIRROR.md` §5, verbatim and unsoftened:

> *If `(*)` fails at `q = 3` too, the fault is the assembly **(b)** and it is a transcription bug
> the lane can fix in an afternoon. If `(*)` holds at `q = 3` and fails at `q ≥ 4`, the fault is
> **(a)** — U4 — and the guard's entire adverse-growth literature is measuring an object that is
> not `Z_{G_q}`.*

The identity under test is the parent's `(*)`, unchanged:

```
      P_q(1-s) / P_q(s)        ==        | phi_q(s) |  *  | K_q(s) |            (*)
```

`q = 3` is `PSL(2,Z)`: `φ_3(s) = √π Γ(s−½) ζ(2s−1) / (Γ(s) ζ(2s))` is **exact and classical**,
`Z_{PSL(2,Z)}` and its functional equation are classical, and the signature `(0;1;2,3)` means Teo's
formula applies verbatim. The parent could not run it because `zeta_cert_rosen_even.py` raises
`NotImplementedError`; this note imports **`zeta_cert_rosen.py`**, the odd-`q` module (eq. 33/34),
which handles `q = 3` as the scalar case (`h_q = 0`, `κ = 1`).

`|K_q|` is imported unchanged from the parent's `mirror_u4.py`. `P_3` is the parent's `P_q` with the
odd-`q` builder substituted. **Nothing else differs from the `q ≥ 4` run.**

---

## 2. The measurement — `mirror_q3.json`, `N = 32`, `prec = 400`, `t = t_∞ = 7.0673625708673465`

| `σ` | `P_3(s)` | `P_3(1−s)` | **LHS** `P(1−s)/P(s)` | `\|φ_3\|` **exact** | `\|K_3\|` | **RHS** | **LHS/RHS** |
|---|---|---|---|---|---|---|---|
| 1.25 | `8.456371e−1` | `2.449148e0` | `2.896216e0` | `4.593593e−1` | `6.852875e−5` | `3.147932e−5` | **`9.20e4`** |
| 1.40 | `8.859662e−1` | `4.961752e0` | `5.600385e0` | `5.109524e−1` | `1.005076e−5` | `5.135459e−6` | **`1.09e6`** |
| 1.50 | `9.069470e−1` | `7.832282e0` | `8.635876e0` | `5.366999e−1` | `2.793609e−6` | `1.499330e−6` | **`5.76e6`** |

**The direction matches the `q ≥ 4` failure exactly**: the transfer operator says
`|Z(1−s)| > |Z(s)|` (by `8.6×` at `σ = 1.5`), the transcribed functional equation says
`|Z(1−s)| ≪ |Z(s)|` (by `6.7e5`).

The failure is **smaller** at `q = 3` (`10⁵–10⁶`) than at `q = 12–30` (`10¹²–10¹⁹`), which is what a
wrong exponent on a `q`-independent bracket predicts: the bracket is `3.2e−20` at `σ = 1.5` for
every `q`, and `(1−2/q)/2` runs `0.167` (`q=3`) → `0.458` (`q=30`).

### Controls

**C1 — assembly / unitarity check on `Re s = 1/2`.** `|K_3(1/2 + i t_∞)| = 1.000000000000` and
`|φ_3(1/2 + i t_∞)| = 1.000000000000`. The assembly passes the parent's §3.1 check at `q = 3` as
well — and **that is precisely the check §3.6 showed to be structurally blind** to the exponent
that turns out to be wrong. This note is a direct confirmation of §3.6's blind-spot claim.

**C2 — determinant `N`-convergence.** Pre-registered before looking (the parent's rule): drift
`≤ 1e−6` ⇒ informative, `≥ 1e−2` ⇒ out of domain. At `N = 24, 32, 48, 64`:

| point | `Re s` | `P_3` | rel. drift `48 → 64` |
|---|---|---|---|
| `s`, `σ = 1.25` | `+1.2500` | `0.8456371451975448` | `3.9e−16` |
| mirror | `−0.2500` | `2.449147973853498` | `1.8e−16` |
| `s`, `σ = 1.40` | `+1.4000` | `0.885966163497939` | `0.0` |
| mirror | `−0.4000` | `4.961751673860739` | `0.0` |
| `s`, `σ = 1.50` | `+1.5000` | `0.9069470136688844` | `2.4e−16` |
| mirror | `−0.5000` | `7.832281702125336` | `0.0` |

**Every point converged to machine precision, ten orders inside the threshold.** The odd-`q` builder
is as well-behaved at `q = 3` as the even-`q` builder was at `q = 12`.

**C3 — the `φ` evaluator cannot enter.** `φ_3 = g(s)` is a closed form in `ζ` and `Γ`. No BFS, no
truncation, no continuation. The parent's suspect (c) is absent by construction, not by argument.

---

## 3. The call

> ### **`(*)` FAILS at `q = 3`. Pre-registered rule ⇒ the fault is (b), the Teo `κ_q` assembly.**
>
> **U4 is not refuted by this test.** The parent's `SM.23` ("U4-as-identification refuted OR the
> Teo assembly is wrong") resolves to the second disjunct.

**What this does and does not rehabilitate.** It removes the mirror test as evidence against U4.
It does **not** establish U4 — U4 remains a `GAP` for `q ≠ 5`, exactly as before this lane started,
and the parent's §4.1 corrections to `LAW_U1_GROWTH.md` §7.3/§10 and
`LAW_U1PHI_PROOF_ROUTE.md` §4.3 should be re-stated as *"the mirror test does not bear on these"*
rather than withdrawn. Nothing here re-validates the guard's readings at `Re s ≤ 1/2`.

---

## 4. Localisation, beyond what the brief asked — the exponent has the wrong sign

`mirror_q3_exponent.py` back-solves the exponent `e` on the Barnes bracket that would make `(*)`
hold, using the *measured* determinant ratios and the *exact* `φ_q`, at `q = 3, 4, 6`
(`q = 4, 6` ratios read from the parent's `mirror_arith.json`):

| `q` | `σ` | `\|bracket\|` | **required `e`** | transcribed `(1−2/q)/2` | `e` vs `−(1−2/q)/2` |
|---|---|---|---|---|---|
| 3 | 1.25 | `2.4077e−15` | **`−0.172892`** | `+0.166667` | `−0.0062` |
| 3 | 1.40 | `2.8617e−18` | **`−0.177488`** | `+0.166667` | `−0.0108` |
| 3 | 1.50 | `3.2083e−20` | **`−0.180132`** | `+0.166667` | `−0.0135` |
| 4 | 1.25 | `2.4077e−15` | **`−0.224002`** | `+0.250000` | `+0.0260` |
| 4 | 1.50 | `3.2083e−20` | **`−0.243444`** | `+0.250000` | `+0.0066` |
| 6 | 1.25 | `2.4077e−15` | **`−0.326001`** | `+0.333333` | `+0.0073` |
| 6 | 1.50 | `3.2083e−20` | **`−0.345811`** | `+0.333333` | `−0.0125` |

> **Seven points, three levels, three abscissae: the required exponent is `−(1−2/q)/2` to between
> `0.007` and `0.026`.** It tracks the `q`-dependence `1/6 → 1/4 → 1/3` exactly, and reverses the
> sign. This is the signature of a **transcription sign error** — the bracket inverted, i.e.
> `[ … ]^{−(1−2/q)/2}` where the lane wrote `[ … ]^{+(1−2/q)/2}` (equivalently, `s ↔ 1−s` swapped
> inside the bracket) — not of a missing factor, which would not scale with `q` this way.

**Direct confirmation (`mirror_q3_signflip.json`).** Re-evaluating the RHS with `e = −(1−2/q)/2`
and changing nothing else:

| `q` | `σ` | LHS | RHS (flipped) | ratio |
|---|---|---|---|---|
| 3 | 1.25 | `2.896216e0` | `2.348697e0` | `1.233` |
| 3 | 1.40 | `5.600385e0` | `3.617181e0` | `1.548` |
| 3 | 1.50 | `8.635876e0` | `4.718540e0` | `1.830` |
| 4 | 1.25 | `8.373042e0` | `2.008805e1` | `0.417` |
| 4 | 1.50 | `6.200982e1` | `8.322566e1` | `0.745` |
| 6 | 1.25 | `1.579028e2` | `2.021022e2` | `0.781` |
| 6 | 1.50 | `3.269361e3` | `1.867385e3` | `1.751` |

**A disagreement of `10⁵`–`10¹³` becomes a factor between `0.42` and `1.83`.** One sign accounts for
essentially the whole discrepancy.

> **Stated with its limit, and this matters.** A residual factor of `0.42`–`1.83` is **not**
> agreement, and this note does **not** claim `(*)` holds once the sign is flipped. The residual is
> `q`- and `σ`-dependent and is not identified here; candidates are the `(±1)` prefactor of Teo
> Prop. 2.5, the branch of `tan(πs/2)^{1/2}` off the critical line, and a normalisation convention
> between Teo's `Z` and the Rosen/MMS determinant. **The sign flip is a `HEURISTIC` diagnosis
> supported by seven consistent back-solves, not a corrected transcription.** The corrected formula
> must be re-derived from Teo Prop. 2.5 directly — that source was **not** opened in this lane, in
> this note or its parent — before any number is recomputed with it.
>
> Note also that the flipped-sign residual `0.42`–`1.83` is the size at which a **U4 test would
> begin to be meaningful**. Until the assembly is fixed from the source, U4 stays untested.

---

## 5. Status ledger

| # | Claim | Status | Where |
|---|---|---|---|
| Q3.1 | `(*)` fails at `q = 3` by `9.2e4` / `1.09e6` / `5.76e6` at `σ = 1.25/1.40/1.50` | **measured, clean** | §2 |
| Q3.2 | `P_3` is `N`-converged to `≤ 4e−16` at all six points, `N = 24…64` | **`PROVED`** numerically | §2 C2 |
| Q3.3 | `\|K_3(1/2+i t_∞)\| = \|φ_3(1/2+i t_∞)\| = 1.000000000000` — assembly passes the blind check | **`PROVED`** numerically | §2 C1 |
| Q3.4 | `φ_3` is exact (`g(s)`); suspect (c) absent by construction | **`PROVED`** | §2 C3 |
| Q3.5 | **Pre-registered rule ⇒ fault is (b), the Teo `κ_q` assembly. U4 not refuted by the mirror test.** | **the finding** | §3 |
| Q3.6 | Required Barnes exponent is `−(1−2/q)/2` to `≤ 0.026`, at `q = 3,4,6` and three `σ` | **measured** | §4 |
| Q3.7 | Sign flip collapses `10⁵`–`10¹³` to a factor `0.42`–`1.83` | **measured** | §4 |
| Q3.8 | The residual `0.42`–`1.83` is **unexplained**; `(*)` is **not** claimed to hold | `GAP` | §4 |
| Q3.9 | The corrected `κ_q` must be re-derived from Teo Prop. 2.5 (source never opened in this lane) | **`TODO-VERIFY`** — the next act | §4 |
| Q3.10 | The parent's §4.1 corrections stand as "the mirror test does not bear on these", not as withdrawals | `HEURISTIC` | §3 |

---

## 6. Receipts

All under `lane_g/law_probes/`. Interpreter `/Users/za/miniforge3/envs/pari-arb/bin/python3`,
`ctx.prec = 400`, `N = 32` (controls at `24, 32, 48, 64`).

- `mirror_q3.py` → `mirror_q3.json`, `mirror_q3.log`. The discriminator: C1 assembly check, the
  three `σ` rows, C2 `N`-convergence, the verdict.
- `mirror_q3_exponent.py` → `mirror_q3_exponent.json`, `.log`. The exponent back-solve at
  `q = 3, 4, 6`.
- `mirror_q3_signflip.json`, `.log`. The sign-flipped residual.
- **Not modified:** `mirror_u4.py`, `mirror_arith.py`, `mirror_nconv.py`, `strip_*.py`, every other
  probe, `lane_f/`, every file of every other lane. `mirror_q3.py` *imports* `K_q` from
  `mirror_u4.py` unchanged, so the kernel under test is byte-identical to the parent's.

---

READY FOR JUDGING
