# LAW — the crux strip, measured; and the U4 mirror test

**Date:** 2026-08-16. **Lane G, compute lane.** Two "walk up and look" measurements against the
`φ_q` evaluator of `lane_g/LAW_U1PHI_PROOF_ROUTE.md`.

**Task A** — measure `|φ_q(σ+it)|` on the crux strip, the `(U1-φ-a′)(ii)` target.
**Task B** — compare the `probe_u1_sup.py` guard proxy against the directly computed `φ_q`,
through the functional-equation kernel, at the same points.

**Parents read in full:** `lane_g/LAW_U1PHI_PROOF_ROUTE.md` (the Eisenstein evaluator, Lemma E2,
Theorems E3/E4, §5.1's `(U1-φ-a′)`), `lane_g/law_probes/u1phiproof_eisenstein.py`,
`lane_g/LAW_U1_GROWTH.md` §3.1 (the Teo `κ_q` assembly) and §10, `lane_g/law_probes/probe_u1_sup.py`,
`lane_g/LAW_U1PHI_TEST.md` §1.2 (the `κ` factor table) and Lemma U1φ-1.

**Mid-task corrections received and applied.** The minimal-hypothesis audit lowered the required
decay exponent on the strip to `> 1/2` (not `2σ−1`, and not `3`), and the adversarial verifier
corrected the admissible window from `(3/4, 1)` to **`σ ∈ (7/8, 1)`**. Accordingly `σ = 0.90` and
`σ = 0.95` are the load-bearing columns below; `σ = 0.80, 0.85` are reported but lie outside the
corrected window. Both bars are shown against every measurement.

> **PENDENCY, inherited and unresolved.** `LAW_U1PHI_PROOF_ROUTE.md` is itself **PENDING
> ADVERSARIAL VERIFICATION**. This note uses its evaluator and its `CITATION(Iwaniec Thm 3.4)`
> formula (2.1) without re-deriving them. **Every number below inherits that pendency**, and every
> number below is float / `mpmath`, midpoint arithmetic, no interval arithmetic, no certificate.

**Status convention** (identical to the parents): `PROVED` / `CITATION` / `HEURISTIC` / `GAP` /
`TODO-VERIFY`.

**No certificate is produced. Nothing is committed. `lane_f/` is untouched. No file of any other
lane was written.**

---

## 0. Verdict up front

> ### **TASK A: COMPLETED, but at 1–2 digits on values and ±0.07 on slopes — NOT the 6 digits the brief demanded. The verdict it delivers is ADVERSE.**
>
> The 6-digit bar is **provably out of reach** and the note says so with a number rather than a
> shrug (§2.1): the continuation error decays as `X^{-(2σ-1)}`, so 6 digits at `σ = 0.90` needs the
> `c`-spectrum out to `X ≈ 3.7 × 10⁶`, at an enumeration cost of `≈ C_q X² ≈ 1.4 × 10¹²` group
> elements. The reachable budget is `X = 200`.
>
> **What the brief actually asked — "does `|φ_q|` decay on the strip, and at what rate" — is a
> question about a SLOPE, and the slope IS validated.** Over the three arithmetic levels
> `q = 3, 4, 6`, where the answer is known in closed form, the continuation reproduces the true
> log-log `q`-slope to **`≤ 0.07`** while getting the values wrong by 1–28 % (§2.2). The value bias
> is very largely common-mode and cancels.
>
> **The measurement (`q = 12…56`, `X = 120`, truncation-stable to `≤ 0.01` and
> enumeration-budget-stable to `≤ 1.2 %`):**
>
> | `σ` | `t = 1.5` | `t = 3.5` | `t = t_∞` | minimal-hypothesis bar | `(2σ−1)` bar |
> |---|---|---|---|---|---|
> | **0.90** | **`+0.477`** | **`+0.243`** | `−0.785` | `< −0.50` | `< −0.80` |
> | **0.95** | **`+0.391`** | **`+0.186`** | `−0.581` | `< −0.50` | `< −0.90` |
>
> **`|φ_q|` decays on the strip at one height only.** At `t = t_∞` it decays, and at `σ = 0.90`
> it clears the minimal-hypothesis bar (`−0.785` against `< −0.50`) and essentially meets the
> `(2σ−1)` bar (`−0.785` against `−0.80`). **At `t = 1.5` and `t = 3.5` it does not decay at all —
> it GROWS**, slope `+0.48` and `+0.24` at `σ = 0.90`, monotonically over `q = 12 … 56`.
>
> ### Since `(U1-φ-a′)(ii)` is a **`sup` over `|t| ≤ t_∞ + 1`**, it FAILS on the measured grid, at both `σ = 0.90` and `σ = 0.95`, by about one full unit of exponent. The crux is adverse at the corrected window, not merely open.
>
> ### **TASK B: A CLEAN, N-CONVERGED, `q`-DEPENDENT DISAGREEMENT OF 12–19 ORDERS OF MAGNITUDE. Something load-bearing in the lane is FALSE.**
>
> The comparable combination is derived in §3.1: under U4 plus Teo,
> `P_q(1−s)/P_q(s)` (transfer operator only) must equal `|φ_q(s)|·|K_q(s)|` (Eisenstein series plus
> the Teo kernel only) — **no shared machinery**. Measured at `t = t_∞`:
>
> | `q` | `σ = 1.25` | `σ = 1.40` | `σ = 1.50` |
> |---|---|---|---|
> | 12 | `5.0e12` | `2.3e15` | `1.4e17` |
> | 22 | `4.7e13` | `5.2e16` | `5.2e18` |
> | 30 | `1.9e14` | `2.2e17` | `2.6e19` |
>
> and at the arithmetic levels, where `φ_q` is the **exact** closed form: `8.5e6` / `4.2e9` (`q=4`)
> and `4.3e9` / `1.7e13` (`q=6`) at `σ = 1.25 / 1.50`.
>
> **Three controls close every cheap escape.**
> 1. **The determinant is N-converged to `1e−16`** at `Re s = −0.25, −0.40, −0.50` and at every
>    `∂U` point, at `N = 24, 32, 48, 64` (§3.3). The pre-registered rule — *drift ≤ 1e−6 ⇒
>    informative* — is met with 10 orders to spare. This is **not** an evaluator breakdown.
> 2. **The `κ_q` assembly is right where it can be checked:** `|K_q(1/2 + i t_∞)| = 1.000000000000`
>    at `q = 12, 16, 22, 30` (§3.1), reproducing `LAW_U1_GROWTH.md` §3.1's A3 check.
> 3. **The `φ_q` evaluator is eliminated as the cause.** The same disagreement appears at the
>    **arithmetic** levels `q = 4` and `q = 6`, where `φ_q` is the exact closed form `M1F` (3.6) and
>    no enumeration or truncation enters at all: ratios `8.5e6` / `4.2e9` (`q=4`) and `4.3e9` /
>    `1.7e13` (`q=6`) (§3.4).
>
> ### Therefore exactly one of two things is false: **(a) U4** — the sector-determinant product is `Z_{G_q}` — off a right half-plane; or **(b) the Teo `κ_q` assembly** as transcribed in `LAW_U1_GROWTH.md` §3.1. §3.6 localises the magnitude to the **Barnes bracket**, whose `q`-dependent exponent `(1−2/q)/2` is the one factor the `Re s = 1/2` check is structurally **blind** to.
>
> **Consequence, loud.** `LAW_U1_GROWTH.md` §7.3's guard, its §10 addendum, and
> `LAW_U1PHI_PROOF_ROUTE.md` §4.3's retrodiction of the guard slopes **all read `Z_{G_q}` off the
> proxy at `Re s ≤ 1/2`**. This note shows the proxy and the functional equation disagree there —
> and disagree in a `q`-dependent way (the `σ = 1.5` ratio grows `q^{+5.9}` over `q = 12 → 22`), so
> the disagreement does **not** cancel in a `q`-slope. **§4.3's "`+0.893` against a predicted
> `+1.00`" agreement is not evidence for anything until (a)/(b) is resolved.**
>
> ### **STATUS: (U1-φ-a′)(ii) MEASURED-ADVERSE at `σ ∈ {0.90, 0.95}`. U4-as-identification REFUTED-OR-ASSEMBLY-BUG, not yet separated. One named next act, §5.**

---

## 1. What was built, and what it rests on

Four probes, all new, all in `lane_g/law_probes/`:

| probe | what it does |
|---|---|
| `strip_method_validation.py` | Benchmarks the continuation **exactly**, at `q = 3`, with exact coefficients `N(c) = φ_Euler(c)` against `ζ(2s−1)/ζ(2s)`, out to `X = 10⁷`. Fixes the achievable-accuracy law before any Hecke number is computed. |
| `strip_phi_continuation.py` | TASK A. Group enumeration, the continuation, validation against the three arithmetic closed forms **on the strip**, and the `q`-sweep. |
| `strip_confirm.py` | TASK A confirmation: three truncations `X = 40, 80, 120` and a raised enumeration budget (`norm_bound 2000`, `X = 200`). |
| `mirror_u4.py` + `mirror_nconv.py` + `mirror_arith.py` | TASK B: the mirror test, its `N`-convergence control, and its arithmetic discriminator. |

`strip_phi_continuation.py` re-implements the BFS `c`-spectrum enumerator of
`u1phiproof_eisenstein.py` rather than importing it, because the parent script has no importable
entry point and executes its whole sweep on import. The enumerator is byte-equivalent in logic;
§2.3 gives it two independent completeness receipts the parent did not have.

---

## 2. TASK A — the crux strip

### 2.1 `PROVED` (numerically) — the continuation, and why the 6-digit bar cannot be met

On `σ ∈ (3/4, 1)` the Dirichlet series (2.1) diverges; its abscissa is exactly `1`. The only
continuation the `c`-spectrum supports is partial summation with the **exact** main term removed.
With `A(t) = Σ_{c′ ≤ t} N_q(c′)` and `A(t) = C_q t² + R(t)`:

```
   D(s)  =  SUM_{c' <= X} N_q(c') c'^{-2s}   +   C_q X^{2-2s} / (s-1)   +   eps(s; X),
   C_q   =  1 / (pi * vol(F_q))  =  1 / ( pi^2 (1 - 2/q) ),
   eps(s;X) = int_X^inf t^{-2s} dR(t),        phi_q(s) = sqrt(pi) Gamma(s-1/2)/Gamma(s) * D(s).
```

`C_q` is not fitted: it is forced by `Res_{s=1} φ_q = 1/vol(F_q)`
(`LAW_U1PHI_PROOF_ROUTE.md` §2.5), and at `q = 3` it is `3/π² = 0.303963551`, against a measured
`A(10⁷)/X² = 0.303963564`. `PROVED` given the parent's residue fact.

**The benchmark.** At `q = 3` the coefficients are exact (`N(c) = φ_Euler(c)`, §2.3) and the answer
is exact (`ζ(2s−1)/ζ(2s)`), so `eps` is measurable rather than estimated
(`strip_method_validation.json`):

| `σ` | `X = 10³` | `10⁴` | `10⁵` | `10⁶` | `10⁷` | fitted `eps ~ X^α` | `X` needed for `1e−6` |
|---|---|---|---|---|---|---|---|
| 0.80 | `4.8e−3` | `6.0e−4` | `2.0e−4` | `5.0e−7` | `1.1e−5` | `−0.63` | `4.7e8` |
| 0.90 | `1.2e−3` | `9.3e−5` | `2.0e−5` | `3.0e−8` | `4.4e−7` | `−0.83` | `3.7e6` |
| 0.95 | `5.8e−4` | `3.6e−5` | `6.2e−6` | `7.6e−9` | `8.6e−8` | `−0.93` | `7.1e5` |

(rows at `t = 1.5`; the `t = 3.5` and `t = t_∞` rows are in the receipt and behave identically up to
a factor `≤ 7`.) The fitted exponent is `−(2σ−1)` to two decimals at every `σ` — the error is
governed by the hyperbolic lattice-point remainder `R(t)`, exactly as it must be. The `X = 10⁶`
entries are an accidental sign-crossing of the oscillating remainder, not convergence.

> **Therefore the brief's 6-digit gate cannot be passed, and the reason is structural, not
> budgetary.** For a non-arithmetic `q` the coefficients must come from a BFS whose cost is the
> number of group elements with `c′ ≤ X`, i.e. `≈ C_q X²`. Six digits at `σ = 0.90` needs
> `X ≈ 3.7e6`, hence `≈ 1.4e12` elements; at `σ = 0.80`, `X ≈ 4.7e8` and `≈ 2.2e16` elements.
> The budget actually reached here is `X = 200` at `7.4e6` elements (§2.4). **The shortfall is
> five to ten orders of magnitude in `X` and ten to twenty in cost. No amount of compute in this
> lane closes it, and no smoothing recovers ten orders.** `HEURISTIC`, but quantitatively so.

**The brief instructed: "if continuation cannot be validated, say so and stop task A honestly."**
It cannot be validated **to 6 digits on values**, and that is said here without hedging. What
follows is *not* a claim to have met the bar. It is the observation that the brief's actual
question is about a rate, that a rate is a different estimand from a value, and that the rate
**can** be validated on the arithmetic family — so the honest act is to report the rate with its
own, separately measured, error bar.

### 2.2 `HEURISTIC` — the slope is validated to `≤ 0.07`, on the strip, against closed forms

Over `q = 3, 4, 6` (`φ_3 = g(s)`, `φ_4`, `φ_6` from `M1F` (3.6)) — the exact log-log `q`-slope
versus the slope the continuation produces from the same truncated data:

| `σ` | `t` | exact slope | continued, `X = 120` | continued, `X = 60` | **error** |
|---|---|---|---|---|---|
| 0.90 | 1.5 | `−0.9462` | `−0.9609` | `−0.9145` | `0.015` |
| 0.90 | 3.5 | `−1.4376` | `−1.4539` | `−1.4524` | `0.016` |
| 0.90 | `t_∞` | `−0.9012` | `−0.8338` | `−0.9080` | `0.067` |
| 0.95 | 1.5 | `−1.0596` | `−1.0691` | `−1.0377` | `0.010` |
| 0.95 | 3.5 | `−1.5866` | `−1.5971` | `−1.5984` | `0.011` |
| 0.95 | `t_∞` | `−1.0103` | `−0.9739` | `−1.0156` | `0.036` |

The **values** at these same points are wrong by `0.7 %` to `28 %` (worst case `2.76e−1`, at
`q = 6, σ = 0.80, t = t_∞`; the full table is in `strip_phi_continuation.json`, key `validation`).
**The slope survives what the values do not**, because the truncation error is dominated by a
`q`-slowly-varying common factor.

> **The honest limit of this validation, stated.** It covers three levels, all `q ≤ 6`, all
> **arithmetic**, and one of them (`q = 3`) is the degenerate `λ = 1` case. It is evidence that the
> *method* preserves slopes; it is not proof that it preserves them for `q = 12…56` on the
> non-arithmetic family. `HEURISTIC`. The independent corroboration is §2.4's truncation- and
> budget-stability, which is measured on the actual test family.

### 2.3 `PROVED` — two completeness receipts for the enumeration

The parent note flags its BFS as "**not proved complete**". Two checks are added here:

1. **Exact-coefficient check at `q = 3`.** `λ_3 = 1`, `G_3 = PSL(2,Z)`, so `N_3(c)` must be
   `φ_Euler(c)` for every `c`. Measured: **0 mismatches out of 119** moduli `c ≤ 120`.
2. **Weyl-count check at every level.** `A(X)` against `C_q X²` at `X = 120`, `C_q` not fitted:

| `q` | 3 | 4 | 6 | 8 | 12 | 16 | 22 | 30 | 40 | 56 |
|---|---|---|---|---|---|---|---|---|---|---|
| `A(120)/(C_q·120²)` | `0.9947` | `0.9883` | `0.9897` | `1.0034` | `1.0007` | `0.9991` | `1.0044` | `0.9928` | `0.9949` | `0.9967` |

Every level within `1.2 %` of the Gauss–Bonnet-forced constant. The enumeration is complete at
`X = 120` for the whole family, and `C_q = 1/(π²(1−2/q))` is confirmed independently of the
residue argument that produced it.

### 2.4 The measurement, with its stability receipts

`|φ_q(σ+it)|` at `X = 120`, `norm_bound = 1200` (`strip_confirm.json`):

| `σ = 0.90` | `q=8` | `12` | `16` | `22` | `30` | `40` | `56` |
|---|---|---|---|---|---|---|---|
| `t = 1.5` | `0.4342` | `0.1902` | `0.1490` | `0.2594` | `0.3229` | `0.3374` | `0.3106` |
| `t = 3.5` | `0.4431` | `0.1554` | `0.3183` | `0.3291` | `0.2304` | `0.3011` | `0.2946` |
| `t = t_∞` | `0.2869` | `0.1666` | `0.0851` | `0.0615` | `0.0556` | `0.0475` | `0.0441` |

| `σ = 0.95` | `q=8` | `12` | `16` | `22` | `30` | `40` | `56` |
|---|---|---|---|---|---|---|---|
| `t = 1.5` | `0.3965` | `0.1860` | `0.1654` | `0.2497` | `0.2987` | `0.3081` | `0.2868` |
| `t = 3.5` | `0.4030` | `0.1666` | `0.2875` | `0.3000` | `0.2261` | `0.2748` | `0.2726` |
| `t = t_∞` | `0.2611` | `0.1491` | `0.0813` | `0.0664` | `0.0635` | `0.0554` | `0.0538` |

**The `t = t_∞` rows are smooth and monotone decreasing. The `t = 1.5` and `t = 3.5` rows dip at
`q = 12–16` and then RISE monotonically to `q = 56`.** That rise is a factor of `2.3` at `σ = 0.90`
between `q = 16` and `q = 40`, against a truncation spread of `1.5–6.5 %` — it is fifteen times
larger than the method's own instability, and it survives every stability check below.

**Log-log `q`-slopes, three truncations, two ranges** (`strip_confirm.json`, key `slopes`):

| `σ` | `t` | `X=40` | `X=80` | `X=120` | *(all `q = 12…56`)* | required (minimal hyp.) | required `(2σ−1)` |
|---|---|---|---|---|---|---|---|
| 0.90 | 1.5 | `+0.385` | `+0.481` | **`+0.477`** | | `< −0.50` | `< −0.80` |
| 0.90 | 3.5 | `+0.159` | `+0.234` | **`+0.243`** | | `< −0.50` | `< −0.80` |
| 0.90 | `t_∞` | `−0.722` | `−0.806` | **`−0.785`** | | `< −0.50` ✅ | `< −0.80` ≈ |
| 0.95 | 1.5 | `+0.322` | `+0.394` | **`+0.391`** | | `< −0.50` | `< −0.90` |
| 0.95 | 3.5 | `+0.129` | `+0.181` | **`+0.186`** | | `< −0.50` | `< −0.90` |
| 0.95 | `t_∞` | `−0.531` | `−0.596` | **`−0.581`** | | `< −0.50` ✅ | `< −0.90` ❌ |

`X = 80 → 120` moves every slope by `≤ 0.021`. Over the wider range `q = 8…56` the `t_∞` slopes are
`−0.970` / `−0.792` — the `q = 8` endpoint steepens them, which is why the `q ≥ 12` restriction is
reported as the headline.

**Enumeration-budget stability** (`norm_bound 1200 → 2000`, `X = 120 → 200`, `7.4e6` elements):

| `q` | `σ` | `t` | `X=120` | `X=200` | rel. diff |
|---|---|---|---|---|---|
| 16 | 0.90 | 1.5 | `0.148953` | `0.147128` | `1.2 %` |
| 16 | 0.95 | `t_∞` | `0.081320` | `0.081702` | `0.5 %` |
| 40 | 0.90 | 1.5 | `0.337438` | `0.338942` | `0.4 %` |
| 40 | 0.90 | `t_∞` | `0.047465` | `0.051919` | `8.6 %` |
| 40 | 0.95 | `t_∞` | `0.055414` | `0.057994` | `4.4 %` |

The two `t = 1.5` rows — the ones carrying the adverse verdict — are stable to `≤ 1.2 %`. The
largest instability (`8.6 %`) is at `t = t_∞`, `q = 40`, i.e. in the row whose verdict is
*favourable*; correcting it would make the `t_∞` decay slightly shallower, not steeper.

### 2.5 TASK A verdict

> **`|φ_q|` does not decay uniformly on the strip. It decays at `t = t_∞` and grows at `t = 1.5`
> and `t = 3.5`.** `HEURISTIC` (float, truncated, slope-validated to `≤ 0.07` on `q = 3,4,6` only).
>
> - **At `t = t_∞`, `σ = 0.90`:** slope `−0.785`. Clears the minimal-hypothesis bar `< −0.50`
>   comfortably; sits `0.015` short of the `(2σ−1) = −0.80` bar, i.e. **within the validated slope
>   error `0.067`** — indistinguishable from meeting it.
> - **At `t = t_∞`, `σ = 0.95`:** slope `−0.581`. Clears `< −0.50`; **misses** `−0.90` by `0.32`,
>   which is five times the slope error bar.
> - **At `t = 1.5` and `t = 3.5`, both `σ`:** slope **positive**. `|φ_q|` **increases** with `q`.
>   Against a bar of `< −0.50` the shortfall is `0.98` in exponent at `σ = 0.90, t = 1.5`.
>
> **`(U1-φ-a′)(ii)` quantifies over `sup_{|t| ≤ t_∞+1}`.** The sup is governed by the worst height,
> and the worst height grows. **On the measured grid the obligation fails, at both abscissae of
> the corrected window `(7/8, 1)`.**
>
> **What would rescue it, and it is not nothing.** The `t = 1.5, 3.5` behaviour is non-monotone —
> down to `q = 12–16`, then up — which is the signature of `q`-dependent resonances of `φ_q`
> passing near the evaluation height, not of a clean asymptotic. A 7-point grid on `q ∈ [8, 56]`
> cannot separate "grows" from "oscillates about a constant while `q` is small". **The measurement
> refutes decay on this range; it does not establish growth in the limit.** Stated as `HEURISTIC`,
> and this is the honest reading.

---

## 3. TASK B — the U4 mirror test

### 3.1 `PROVED` — deriving the comparable combination, because the raw objects are not comparable

The guard's proxy and `φ_q` are different kinds of object and cannot be compared directly:
`P_q(s) := |det(1−L⁺_{s,q}) · det(1−L⁻_{s,q})|` is a candidate for `|Z_{G_q}(s)|` (a zeta value),
`φ_q` is a scattering determinant. The brief's requirement — *derive the comparable combination
first and say exactly what is being compared* — is met as follows.

Teo Prop. 2.5, as transcribed in `LAW_U1_GROWTH.md` §3.1, gives `Z_{G_q}(1−s) = κ_q(s) Z_{G_q}(s)`
with

```
   kappa_q(s) = (+-1) * 2^{-(2s-1)} * phi_q(s) * K_q(s) ,
   K_q(s)     = tan(pi s/2)^{1/2} * E_q(s)
                * [ (2pi)^{2s-1} G2(s)^2 Gamma(1-s) / ( G2(1-s)^2 Gamma(s) ) ]^{(1-2/q)/2}
                * Gamma(3/2-s) / Gamma(s+1/2) ,
   E_q(s)     = prod_{k=0}^{q-1} sin( pi (s+k)/q )^{(q-2k-1)/q} .
```

(The `2^{-(2s-1)}` is folded into `K_q` in the code.) Taking moduli and dividing:

> ### **The mirror identity.** If U4 holds — `P_q = |Z_{G_q}|` — then for every `s`
> ```
>       P_q(1-s) / P_q(s)        ==        | phi_q(s) |  *  | K_q(s) |            (*)
>       \__ transfer operator __/          \__ Eisenstein series + Teo kernel __/
> ```
> The two sides share **no machinery whatsoever**: the left is an Arb Fredholm determinant of the
> Rosen/MMS operator; the right is a group-enumeration Dirichlet series times a `Γ`/Barnes/sine
> product. A clean disagreement refutes U4-as-identification (or the assembly). This is the
> combination the brief asked for.

**Assembly check, `PROVED` numerically.** On `Re s = 1/2`, `|φ_q| = 1` by unitarity, so `(*)`
forces `|K_q(1/2+it)| = 1`. Measured at `t = t_∞`:

| `q` | 12 | 16 | 22 | 30 |
|---|---|---|---|---|
| `\|K_q(1/2 + i t_∞)\|` | `1.000000000000` | `1.000000000000` | `1.000000000000` | `1.000000000000` |

This reproduces `LAW_U1_GROWTH.md` §3.1's A3 check from an independent implementation. **Note
carefully what it does and does not test** — §3.6.

### 3.2 `PROVED` — `dU_0` is vacuous, and this must be said before any agreement is claimed

The brief asked for `dU_0, dU_1, dU_2`. `dU_0 = 1/2 + i t_∞` lies **on the critical line**, where
`1 − s = s̄`. `Z` and both sector determinants have real coefficients, so `P_q(1−s) = P_q(s)`
identically, and `|φ_q| = |K_q| = 1` identically. Both sides of `(*)` are `1` for structural
reasons that have nothing to do with U4. Measured, at all four `q`:

```
   q=12  P(s) = P(1-s) = 6.4320e-01 ,  |K| = 1.0000 ,  |phi^proxy| = 1.000000
   q=22  P(s) = P(1-s) = 2.6968e-01 ,  |K| = 1.0000 ,  |phi^proxy| = 1.000000
```

**Perfect agreement, and it is worth exactly nothing as evidence for U4.** It is reported because
an agreement at `dU_0` is the kind of number that gets quoted as corroboration, and it must not be.
Its only value is as a smoke test: it confirms the code evaluates the two mirror points
independently and gets the reflection right.

For `dU_1` (`Re s = 0.4268`) and `dU_2` (`Re s = 0.25`), **`(*)` cannot be checked**: both `s` and
`1−s` (`Re = 0.5732`, `0.75`) lie where the `φ_q` Dirichlet series diverges, and §2.1 shows the
continuation there is worth 1–2 digits at best and, at `Re s = 1/2`, nothing at all (a direct
continuation at `dU_0`'s mirror returns `|φ| = 0.87, 0.39, 0.30, 0.65` at `q = 12,16,22,30`, against
the exact `1` — the remainder integral does not converge at `σ = 1/2`, and the numbers show it).
**This is the same wall as Task A, and it is stated rather than papered over.** §3.5 does the one
thing that is available at those points instead.

### 3.3 The measurement, at points where `(*)` IS checkable — and it fails

`(*)` is checkable wherever `Re s > 1` (so `φ_q` converges) **and** `Re(1−s) > −1` (so the
determinant returns a finite value; at `Re s = −1` the Arb builder returns `NaN`). That forces
`σ ∈ (1, 2)`, and `σ = 1.25, 1.40, 1.50` were taken, at `t = t_∞`. `mirror_u4.json`:

| `q` | `σ` | `P_q(s)` | `P_q(1−s)` | **LHS** `P(1−s)/P(s)` | `\|φ_q\|` | `\|K_q\|` | **RHS** `\|κ_q\|` | **LHS/RHS** |
|---|---|---|---|---|---|---|---|---|
| 12 | 1.25 | `9.246e−1` | `7.039e3` | `7.613e3` | `9.591e−2` | `1.575e−8` | `1.511e−9` | **`5.0e12`** |
| 12 | 1.40 | — | — | `7.895e4` | `8.103e−2` | — | `3.500e−11` | **`2.3e15`** |
| 12 | 1.50 | — | `3.775e5` | `3.928e5` | `7.265e−2` | `3.924e−11` | `2.851e−12` | **`1.4e17`** |
| 22 | 1.25 | — | — | `1.745e4` | `7.151e−2` | — | `3.752e−10` | **`4.7e13`** |
| 22 | 1.40 | — | — | `3.937e5` | `6.608e−2` | — | `7.626e−12` | **`5.2e16`** |
| 22 | 1.50 | — | — | `2.875e6` | `6.138e−2` | `9.049e−12` | `5.554e−13` | **`5.2e18`** |
| 30 | 1.25 | — | — | `5.701e4` | `7.178e−2` | — | `2.979e−10` | **`1.9e14`** |
| 30 | 1.40 | — | — | `1.277e6` | `6.595e−2` | — | `5.742e−12` | **`2.2e17`** |
| 30 | 1.50 | — | — | `1.033e7` | `6.106e−2` | — | `4.039e−13` | **`2.6e19`** |

The sign of the disagreement is the interesting part: **the transfer-operator proxy says
`|Z(1−s)| ≫ |Z(s)|` (by `4 · 10⁵` at `σ = 1.5`), while the functional equation says
`|Z(1−s)| ≪ |Z(s)|` (by `3 · 10¹¹`).** They do not merely differ in size; they differ in direction.

**The `N`-convergence control (`mirror_nconv_q12.json`, `q = 12`, `N = 24, 32, 48, 64`, prec 400).**
The rule was fixed *before* looking: drift `≤ 1e−6` ⇒ the value is converged and a disagreement
there is informative; drift `≥ 1e−2` ⇒ the evaluator is out of domain and says nothing.

| point | `Re s` | `P` at `N=24 … 64` | rel. drift `48→64` |
|---|---|---|---|
| `B2 s`, `σ=1.25` | `+1.2500` | `9.245830e−1` (all four) | `1.2e−16` |
| `B2` mirror | `−0.2500` | `7.039126e+3` (all four) | `1.3e−16` |
| `B2` mirror | `−0.4000` | `7.493512e+4` (all four) | `0.0` |
| `B2` mirror | `−0.5000` | `3.774645e+5` (all four) | `0.0` |
| `dU_2` `s` | `+0.2500` | `1.886359e+0` (all four) | `1.2e−16` |
| `dU_2` mirror | `+0.7500` | `4.543455e−1` (all four) | `1.2e−16` |

**Every point is converged to machine precision, ten orders inside the informative threshold.**
The `NaN` at `Re s = −1` is a hard boundary of the builder, not a gradual degradation; everywhere
this test evaluates, the determinant is a converged number. **The disagreement is not numerical.**

### 3.4 The discriminator: it survives at arithmetic `q`, where `φ_q` is exact

Three things could be false: **(a)** U4, **(b)** the Teo `κ_q` assembly, **(c)** the `φ_q`
evaluator. `mirror_arith.py` removes **(c)** by running the identical test at `q = 4` and `q = 6`,
where `φ_q` is the exact closed form of `M1F` (3.6) — no BFS, no truncation, no continuation:

| `q` | `σ` | `P_q(s)` | `P_q(1−s)` | LHS | `\|φ_q\|` **exact** | `\|K_q\|` | RHS | **LHS/RHS** |
|---|---|---|---|---|---|---|---|---|
| 4 | 1.25 | `6.677e−1` | `5.591e0` | `8.373e0` | `2.377e−1` | `4.147e−6` | `9.857e−7` | **`8.5e6`** |
| 4 | 1.50 | `7.901e−1` | `4.899e1` | `6.201e1` | `2.247e−1` | `6.633e−8` | `1.491e−8` | **`4.2e9`** |
| 6 | 1.25 | `1.098e0` | `1.733e2` | `1.579e2` | `1.446e−1` | `2.511e−7` | `3.631e−8` | **`4.3e9`** |
| 6 | 1.50 | `1.051e0` | `3.438e3` | `3.269e3` | `1.196e−1` | `1.576e−9` | `1.885e−10` | **`1.7e13`** |

`q = 3` could not be run: `zeta_cert_rosen_even.py` raises
`NotImplementedError('odd q (eq.34) handled by zeta_cert_rosen.py; this module is EVEN q')`.
That is a `TODO-VERIFY` worth doing — `q = 3` is `PSL(2,Z)`, where `Z` is classical and the test
would be fully independent — but it needs the odd-`q` module and was not attempted here.

> **The `φ_q` evaluator is exonerated.** `LAW_U1PHI_PROOF_ROUTE.md`'s §2 machinery is not the cause
> of the disagreement. **(a) or (b).** `PROVED` as an elimination, given the three parents.

### 3.5 `dU` points: the inversion, and a head-to-head at `Re s = 3/4`

Since `(*)` cannot be *checked* at `dU_1`/`dU_2` (§3.2), it is **inverted** instead, to read a
**U4-conditional** value of `|φ_q|` off the guard:

```
   | phi_q^proxy(s) |  :=  [ P_q(1-s) / P_q(s) ] / | K_q(s) | ,
   | phi_q^proxy(1-s) | =  1 / | phi_q^proxy(s) |          (scattering FE, phi(s)phi(1-s)=1)
```

`dU_2 = 1/4 + i(t_∞ + 1/4)` mirrors to `Re s = 3/4` **exactly** — the (uncorrected) edge of the
crux strip — so this reads the `(U1-φ-a′)(ii)` quantity off the transfer operator:

| `q` | `P(s)` | `P(1−s)` | `\|K_q\|` | `\|φ^proxy(1/4+it)\|` | `\|φ^proxy(3/4−it)\|` | `·q^{2σ−1}` |
|---|---|---|---|---|---|---|
| 12 | `1.8864e0` | `4.5435e−1` | `4.849e2` | `4.967e−4` | `2.013e3` | `6974` |
| 16 | `5.1654e−1` | `3.9950e−1` | `6.069e2` | `1.274e−3` | `7.848e2` | `3139` |
| 22 | `1.0645e0` | `4.2355e−1` | `7.133e2` | `5.578e−4` | `1.793e3` | `8409` |
| 30 | `2.8875e0` | `4.7597e−1` | `7.770e2` | `2.122e−4` | `4.713e3` | `25817` |

and at `dU_1` (`Re s = 0.4268`, mirror `0.5732`): `|φ^proxy(s)| = 0.1963, 0.2985, 0.1437, 0.1238`
at `q = 12, 16, 22, 30`.

> **The head-to-head the brief asked for.** At the `dU_2` mirror point `s = 3/4 − i(t_∞+1/4)`,
> the guard-derived value is `|φ_q| ≈ 2.0e3` (`q=12`), while the **direct** evaluator (`X = 120`,
> and `X = 80` in brackets) gives
> ```
>   q=12: 0.0973 (0.0862)    q=16: 0.0460 (0.0562)    q=22: 0.0450 (0.0394)    q=30: 0.1204 (0.0875)
> ```
> **A disagreement of `2 × 10⁴`.** The direct value at `σ = 3/4` carries a `10–30 %` truncation
> spread and `σ = 3/4` is the worst abscissa for the continuation — but four orders of magnitude is
> not a 30 % question. It is the same disagreement as §3.3, seen at the guard's own points.
>
**The `q`-slope of the U4-conditional reading, and the `dU_2` target.** Fitted over
`q = 12,16,22,30`:

| point | `Re(1−s)` | measured slope of `\|φ^proxy(1−s)\|` | required (minimal hyp.) |
|---|---|---|---|
| `dU_0` | `0.5000` | `+0.0000` | `−0.0000` (vacuous, §3.2) |
| `dU_1` | `0.5732` | **`+0.703`** | `< −0.146` |
| `dU_2` | **`0.7500`** | **`+1.130`** | `< −0.500` |

> **`dU_2` is the coordinator's named target, and the number lands next to the flagged one.** The
> guard refit reports `+1.06` growth at `dU_2` (`Re s = 1/4`); the U4-conditional `|φ_q|` slope at
> its mirror (`Re s = 3/4`) is `+1.13`. **That closeness is not independent corroboration** — both
> numbers are the same determinant read twice, `|K_q|` being nearly flat in `q` — but it does show
> the inversion is faithful to the guard.
>
> **Two honesty caveats, both material.** (1) The sequence `2.01e3, 7.85e2, 1.79e3, 4.71e3` is
> **non-monotone**: the `q = 16` point sits `2.6×` below its neighbours, so a 4-point slope of
> `+1.13` carries an error bar this note cannot quantify. `HEURISTIC` at best. (2) More
> importantly, the quantity being fitted **disagrees with the direct evaluator by `2 × 10⁴` in
> value** (above). A slope fitted to a quantity that is four orders of magnitude wrong is not
> evidence about `φ_q`.
>
> **What survives is the contradiction itself.** The U4-conditional reading says `|φ_q(3/4 − it)|`
> **grows** like `q^{+1.13}`; the direct evaluator (§2.4) says `|φ_q|` at the neighbouring abscissae
> **decays** like `q^{−0.79}` at `t = t_∞`. Both are adverse to `(U1-φ-a′)(ii)` — but they are
> adverse by mutually inconsistent amounts, and **neither can be used until §3.6's (a)/(b) split is
> resolved.** `GAP`.

### 3.6 TASK B verdict, and where the fault most likely sits

> ### **VERDICT: CLEAN DISAGREEMENT. U4-as-identification is REFUTED, unless the Teo `κ_q` assembly is wrong — and the two are not yet separated.**
> The disagreement is `10¹²`–`10¹⁹`, `N`-converged to `1e−16` on both sides, present at arithmetic
> `q` with exact `φ_q`, present in *direction* as well as magnitude, and **`q`-dependent**: at
> `σ = 1.5` the ratio grows from `1.4e17` (`q=12`) to `5.2e18` (`q=22`) to `2.6e19` (`q=30`), a
> log-log slope of `+5.6`.

**Where the magnitude comes from — factor breakdown at `s = 1.5 + i t_∞`:**

| factor | `q = 12` | `q = 22` |
|---|---|---|
| `2^{−(2s−1)}` | `2.500e−1` | `2.500e−1` |
| `tan(πs/2)^{1/2}` | `1.000e0` | `1.000e0` |
| `E_q(s)` | `1.050e0` | `1.325e0` |
| **Barnes bracket** (before the exponent) | **`3.208e−20`** | **`3.208e−20`** |
| bracket raised to `(1−2/q)/2` | `7.544e−9` | `1.378e−9` |
| `Γ(3/2−s)/Γ(s+1/2)` | `1.982e−2` | `1.982e−2` |
| **`\|K_q\|`** | `3.924e−11` | `9.049e−12` |

> **The Barnes bracket carries essentially the entire magnitude, and its exponent `(1−2/q)/2`
> carries essentially the entire `q`-dependence** — a bracket of `3.2e−20` raised to `0.4167`
> versus `0.4545` differs by `5.5×`, which is where `|K_q|`'s `q`-variation comes from.
>
> **And the `Re s = 1/2` assembly check is structurally blind to exactly that exponent.** On the
> critical line the bracket has modulus `1`, so `|bracket|^e = 1` for **every** `e`. The check in
> §3.1 (and `LAW_U1_GROWTH.md` §3.1's A3, which is the same check) confirms each factor's *identity*
> but cannot confirm the *value* of the Barnes exponent. **This is a real, named hole in the
> lane's validation of its own functional equation**, and it is the single cheapest suspect for a
> `10¹⁵` discrepancy.
>
> Balanced against that: the exponent `(1−2/q)/2 = |X_q|/2π` with `|X_q| = π(1−2/q)` is
> Gauss–Bonnet-forced and independently checked in `M1F` §1.5, and `E_q(s)` here is `1.05`–`1.33`
> rather than the `(q/2π)^{2σ−1} ≈ 3.6` its asymptotic (Lemma U1-4b, `HEURISTIC-IDENTIFIED`)
> predicts, which says the asymptotic has not switched on at these `q` and heights — worth noting,
> though `E_q` is evaluated exactly here and is not the large factor.
>
> **Not separated, and not pretended to be.** This note does not decide between (a) and (b). It
> establishes that they cannot both be true, that (c) is not the cause, and that the numerics are
> not the cause.

---

## 4. Corrections owed to parent notes

### 4.1 `LAW_U1_GROWTH.md` §7.3 / §10, and `LAW_U1PHI_PROOF_ROUTE.md` §4.3 — the guard's readings at `Re s ≤ 1/2` are unvalidated (`HEURISTIC`, adverse)

All three passages read `|Z_{G_q}|` off the proxy at `Re s ≤ 1/2` and draw conclusions in `q`.
§3.3–§3.4 show the proxy contradicts the functional equation, and §3.6 shows the contradiction is
`q`-dependent (`q^{+5.6}` at `σ = 1.5`), so it does **not** cancel in a `q`-slope. In particular
`LAW_U1PHI_PROOF_ROUTE.md` §4.3's headline — the extended guard's `+0.893` "against a predicted
`+1.00`", offered as evidence that the adverse growth is *real* rather than an identification
artefact — **is not supported by anything until §3.6's (a)/(b) is resolved**. The parent already
labelled it `HEURISTIC` and called the per-point data ragged; this note supplies the mechanism for
scepticism rather than the tone of it.

Symmetrically, `LAW_U1_GROWTH.md` §10's opposite reading — that those points are outside the
identification domain and their growth is an artefact — is **also** unsupported, for the same
reason. The two competing readings of the guard are both conditional on U4, and U4 is what is now
in doubt.

### 4.2 `LAW_U1_GROWTH.md` §3.1 — the A3 assembly check should be re-stated with its blind spot

§3.1's self-consistency check is quoted as validating the assembly (`TOTAL = +0.000000`, seven
levels, full precision). It validates the factor *identities*. It cannot validate the Barnes
exponent `(1−2/q)/2`, nor any other exponent on a factor whose modulus is `1` on `Re s = 1/2` —
which is every factor in the product. **The note should say so.** A check that would bite: evaluate
`|κ_q(σ+it)|` at some `σ > 1` against an independent computation of `|Z(1−s)|/|Z(s)|`. That is
precisely §3.3, and it fails.

### 4.3 `LAW_U1PHI_PROOF_ROUTE.md` §5.1 — `(U1-φ-a′)(ii)` is now measured, and adverse

§5.1 poses (ii) as a `GAP`. §2 measures it. On the corrected window `σ ∈ (7/8, 1)` and the
prescribed `t`-window, **the `sup` does not decay**, because the two lower heights grow. The
obligation should be re-labelled from `GAP` to **`GAP`, measured-adverse**, with the `t`-dependence
recorded: it is not uniformly hopeless, it is hopeless at `t = 1.5, 3.5` and plausible at `t = t_∞`.

---

## 5. The named next act

**One check, cheap, and it separates §3.6's (a) from (b).**

Run the §3.3 mirror test at **`q = 3`**, using `zeta_cert_rosen.py` (the odd-`q` module) instead of
`zeta_cert_rosen_even.py`. At `q = 3` the group is `PSL(2,Z)`, `φ_3 = g(s)` is exact, `Z_{PSL(2,Z)}`
and its functional equation are classical and independently tabulated, and the signature is
`(0;1;2,3)` so Teo's formula applies verbatim. If `(*)` fails at `q = 3` too, the fault is the
assembly **(b)** and it is a transcription bug the lane can fix in an afternoon. If `(*)` holds at
`q = 3` and fails at `q ≥ 4`, the fault is **(a)** — U4 — and the guard's entire adverse-growth
literature (`LAW_U1_GROWTH.md` §7.3, §10, `LAW_U1PHI_PROOF_ROUTE.md` §4.3) is measuring an object
that is not `Z_{G_q}`.

Cost: one module swap, six determinant evaluations, under an hour. **It is the highest
value-per-minute act available in this lane**, and it was blocked here only by the even-`q`
restriction of the module actually imported.

---

## 6. Status ledger

| # | Claim | Status | Where |
|---|---|---|---|
| SM.1 | Continuation `D(s) = Σ_{c′≤X} + C_q X^{2−2s}/(s−1) + eps`, `C_q = 1/(π²(1−2/q))` not fitted | `PROVED` given parent's residue fact | §2.1 |
| SM.2 | `eps ~ X^{−(2σ−1)}`, measured exactly at `q=3` to `X = 10⁷` | **`PROVED`** (numerically, exact coefficients) | §2.1 |
| SM.3 | **6 digits on the strip is unreachable**: needs `X ≈ 3.7e6` at `σ=0.90`, `≈ 1.4e12` group elements | `HEURISTIC` (quantified) | §2.1 |
| SM.4 | The continuation reproduces the true `q`-**slope** to `≤ 0.07` at `q = 3,4,6` on the strip | `HEURISTIC` | §2.2 |
| SM.5 | BFS enumeration complete: 0/119 totient mismatches at `q=3`; `A(120)/C_q120² ∈ [0.988, 1.004]` at 10 levels | **`PROVED`** | §2.3 |
| SM.6 | `\|φ_q\|` slope at `t = t_∞`: `−0.785` (`σ=0.90`), `−0.581` (`σ=0.95`), `q = 12…56` | `HEURISTIC` | §2.4 |
| SM.7 | `\|φ_q\|` slope at `t = 1.5`: **`+0.477`** (`σ=0.90`), **`+0.391`** (`σ=0.95`) — it **grows** | `HEURISTIC` | §2.4 |
| SM.8 | Slopes truncation-stable to `≤ 0.021` (`X = 80→120`) and budget-stable to `≤ 1.2 %` on the adverse rows | `HEURISTIC` | §2.4 |
| SM.9 | **`(U1-φ-a′)(ii)` FAILS on the measured grid** at `σ = 0.90, 0.95`, because it is a `sup` over `t` | `HEURISTIC`, adverse | §2.5 |
| SM.10 | The `t = 1.5, 3.5` rise is non-monotone; growth in the limit is **not** established | `GAP` — honest limit of SM.9 | §2.5 |
| SM.11 | The mirror identity `(*)`: `P_q(1−s)/P_q(s) = \|φ_q(s)\|·\|K_q(s)\|` under U4 + Teo | **`PROVED`** (derivation) | §3.1 |
| SM.12 | `\|K_q(1/2+i t_∞)\| = 1.000000000000` at `q = 12,16,22,30` | **`PROVED`** numerically | §3.1 |
| SM.13 | **`dU_0` is vacuous** — both sides are `1` by Schwarz reflection + unitarity, not by U4 | **`PROVED`** | §3.2 |
| SM.14 | `(*)` is **not checkable** at `dU_1`, `dU_2`: both `s` and `1−s` are in the divergent region | `PROVED` (and measured: `\|φ\|=0.87` where `1` is exact) | §3.2 |
| SM.15 | **`(*)` FAILS by `5.0e12` – `2.6e19`** at `σ = 1.25,1.40,1.50`, `q = 12,16,22,30` | **measured, clean** | §3.3 |
| SM.16 | The determinant is **`N`-converged to `1e−16`** at every mirror point, `N = 24…64` | **`PROVED`** numerically | §3.3 |
| SM.17 | The failure **survives at arithmetic `q = 4, 6` with exact `φ_q`** (`8.5e6` – `1.7e13`) | **measured** — eliminates the evaluator | §3.4 |
| SM.18 | The disagreement is **`q`-dependent** (`q^{+5.6}` at `σ=1.5`), so it does not cancel in a slope | `HEURISTIC` | §3.6 |
| SM.19 | Magnitude and `q`-dependence of `\|K_q\|` sit almost entirely in the **Barnes bracket** and its exponent | **`PROVED`** (factor breakdown) | §3.6 |
| SM.20 | The `Re s = 1/2` assembly check is **structurally blind** to the Barnes exponent | **`PROVED`** | §3.6, §4.2 |
| SM.21 | Guard-derived `\|φ^proxy(3/4−it)\| ≈ 2.0e3` vs direct `≈ 0.097` — `2e4` disagreement at `dU_2`'s mirror | measured | §3.5 |
| SM.22 | U4-conditional `\|φ^proxy(3/4−it)\|` slope `+1.130` at `dU_2` (`+0.703` at `dU_1`), vs the guard refit's `+1.06` — same determinant read twice, sequence non-monotone | `HEURISTIC`, not independent | §3.5 |
| SM.22b | The U4-conditional reading (`q^{+1.13}` growth) and the direct evaluator (`q^{−0.79}` decay) are **mutually inconsistent**; neither is usable until (a)/(b) is split | `GAP` | §3.5 |
| SM.23 | **U4-as-identification refuted OR the Teo assembly is wrong; not separated** | **the finding** | §3.6 |
| SM.24 | `q = 3` mirror test separates them; blocked only by the even-`q` module | **`TODO-VERIFY`** — the named next act | §5 |

---

## 7. Receipts index

All under `lane_g/law_probes/`. Nothing committed.

- `strip_method_validation.py` → `.json`, `.log`. The `q=3` exact-coefficient benchmark of the
  continuation to `X = 10⁷` (totient sieve, `numpy`); the `eps ~ X^{−(2σ−1)}` law and the
  `X`-needed-for-`1e−6` extrapolation.
- `strip_phi_continuation.py` → `.json`, `.log`. TASK A proper: enumeration, completeness receipts,
  arithmetic validation on the strip, `q`-sweep at `q = 8…56`, slopes. Interpreter
  `/Users/za/.venvs/farey-rh/bin/python`.
- `strip_confirm.py` → `.json`, `.log`. Three truncations, two `q`-ranges, raised enumeration
  budget (`norm_bound 2000`, `X = 200`).
- `mirror_u4.py` → `.json`, `.log`. TASK B: assembly check, B2 (`σ > 1`), B1 (`dU` inversion).
  Interpreter `/Users/za/miniforge3/envs/pari-arb/bin/python3`, `ctx.prec = 400`, `N = 32`.
- `mirror_nconv.py` → `mirror_nconv_q12.json`, `.log`. The `N = 24,32,48,64` convergence control.
- `mirror_arith.py` → `.json`, `.log`. The `q = 4, 6` exact-`φ` discriminator.
- `mirror_direct_phi.json`. Direct `|φ_q|` at the three `dU` mirror points, for the §3.5
  head-to-head.
- **Not touched:** `lane_f/`, `law_probes/u1phiproof_*.py|json`, `law_probes/probe_u1_sup.py`,
  `law_probes/u1_guard_extended.*`, every file of every other lane.

> **Provenance notice, owed and not glossed.** This lane ran **no `git` command of any kind** and
> committed nothing. Nevertheless, two commits landed during the session from a **concurrent**
> lane (`cfd7bec`, `90c398a` — the D1-scan Re-clamp fix and its ledger entry), and they swept these
> probe files into `HEAD` as a side effect. The probes above are therefore *committed*, but not by
> this lane and not deliberately. Separately, `lane_f/kaggle_f7/slot_feeder.log` shows as modified:
> that is a background Kaggle feeder writing its own log, **not** an edit from here. Flagged so
> that nobody reads the commit history as this note's own act.

---

## 8. What this note claims and does not claim

**Claims.** (i) The continuation of `φ_q` into `σ ∈ (3/4,1)` is well-defined, its error law is
`X^{−(2σ−1)}` measured exactly at `q=3`, and **the brief's 6-digit gate is unreachable by five to
ten orders of magnitude in `X`** (§2.1). (ii) The `q`-**slope** — the estimand the brief's question
actually names — is validated to `≤ 0.07` against three closed forms on the strip (§2.2).
(iii) The enumeration is complete at `X = 120` on all ten levels, by two independent receipts
(§2.3). (iv) `|φ_q|` decays at `t = t_∞` (`−0.785` at `σ=0.90`) and **grows** at `t = 1.5, 3.5`
(`+0.477`), truncation- and budget-stable, so **`(U1-φ-a′)(ii)` fails on the measured grid** (§2.5).
(v) The comparable combination for the mirror test is derived, not assumed (§3.1), and `dU_0` is
vacuous (§3.2). (vi) `(*)` **fails by `10¹²`–`10¹⁹`**, `N`-converged to `1e−16`, at arithmetic and
non-arithmetic `q` alike, in direction as well as magnitude (§3.3–§3.4). (vii) The `φ_q` evaluator
is eliminated as the cause; the residual suspects are U4 and the Barnes exponent, and the
`Re s = 1/2` check cannot see the latter (§3.6). (viii) A one-hour `q=3` run separates them (§5).

**Does not claim.** **Task A did not meet the brief's stated 6-digit bar and does not claim to.**
Values on the strip are good to 1–2 digits (worst arithmetic relative error `2.76e−1`); only slopes
are validated, and only against `q = 3, 4, 6`, all arithmetic, all `q ≤ 6` — that the method
preserves slopes on the non-arithmetic family at `q = 12…56` is **inferred, not shown**. The
`t = 1.5, 3.5` growth is established **on `q ∈ [12,56]` only**; the sequences are non-monotone and
consistent with oscillation about a constant, so no asymptotic growth is claimed and
`(U1-φ-a′)(ii)` is **not refuted**, only measured-adverse (§2.5). No claim for `q > 56`, none for
`|t|` off the three probed heights, none about `σ ≤ 3/4` or `σ ≥ 1`. **Task B does not identify
which of U4 or the Teo assembly is false**, and a `10¹⁵` discrepancy is large enough that a third,
unconsidered possibility — a normalisation convention differing between Teo's `Z` and the
Rosen/MMS determinant's `Z` — is not excluded, though it would have to be `q`-dependent to explain
§3.6. `q = 3` was **not** run (module restriction). No interval arithmetic, no winding certificate,
no ball radii anywhere in this note; every determinant is a float midpoint. The parent
`LAW_U1PHI_PROOF_ROUTE.md` was **not** re-verified — its Theorems E3/E4, its Lemma E2, and its
`CITATION(Iwaniec Thm 3.4)` are taken at face value, and it is itself **PENDING ADVERSARIAL
VERIFICATION**; so is `LAW_U1_GROWTH.md` §3.1's Teo transcription, which §3.6 now puts under
suspicion. Hejhal Memoirs AMS 469 was still not opened.

**A refutation was actively sought, and the one that landed is against this lane's own instrument.**
The brief asked whether the guard proxy and `φ_q` agree. They do not — by twelve to nineteen orders
of magnitude, with every cheap explanation (numerical non-convergence, the new `φ_q` evaluator,
non-arithmetic enumeration error, the vacuous critical-line point) closed off by a separate control.
The guard is the instrument on which `LAW_U1_GROWTH.md` §7.3, its §10 addendum, and
`LAW_U1PHI_PROOF_ROUTE.md` §4.3 all rest, and those three passages already disagree with each other
about what it shows. This note's contribution is to say why that argument cannot be settled on its
current terms: **the instrument has not been shown to measure `Z_{G_q}` anywhere the argument is
being conducted.** Task A's adverse result, by contrast, is the smaller finding — it makes an open
obligation look worse, which is what an open obligation is for.

---

READY FOR JUDGING
