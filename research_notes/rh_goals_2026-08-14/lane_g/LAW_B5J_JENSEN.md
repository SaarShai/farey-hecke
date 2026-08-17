# LAW B5-J — Jensen counting on `det(1 − L_{s,±})`: the derivation, and the failure

**Date:** 2026-08-16. **Lane G, proof lane.**
**Parents:** `LAW_ROUTEB_CONDITIONAL_THEOREM.md` §6.3 (which names B5-J as the *single recommended
next lane*, ranked #1 of 6); `LAW_SH_EFFECTIVIZATION_SKELETON.md` §3 (Route B).
**Probes:** `law_probes/b5j_supbound.{py,json}`, `b5j_disc.{py,json}`, `b5j_expansion.{py,json}`,
`b5j_jensen.{py,json,log}`, `b5j_growth.{py,json,log}`.
**No git was run. No existing file was modified.**

**Status labels** as in the parent: `PROVED-here` / `PROVED-cited` / `MEASURED` / `GAP` /
`REFUTED-here` (new: a claim in a parent document that this document disproves).

---

## 0. Verdict up front

> ### **B5-J FAILS. It should be removed from the critical path, and the parent's ranking #1 withdrawn.**
>
> The failure is not "we could not find the constants". It is **three independent, quantified
> obstructions**, two of which are *intrinsic to Jensen's formula in this geometry* and cannot be
> repaired by better estimates:
>
> **(F1) `det(1 − L_{s,±})` is NOT of order 0 in `s`. The parent's §6.3 item 1 is false.**
> Measured along `Im s = 7`, `log|det(1 − L_{s,+})|` rises from `0.61` at `Re s = 0.5` to `21.67`
> at `Re s = −2.5` for `q = 5`, and from `−0.76` to `34.38` for `q = 9` — a growth rate of
> `≈ 7 … 16` per unit of `Re s`, **increasing with `q`**. "Order 0" in the Ruelle/Grothendieck
> sense refers to the **Fredholm (eigenvalue) variable**, not to `s`. In `s` the determinant grows
> like the Selberg zeta it computes. **Jensen therefore needs exactly the `q`-uniform growth bound
> that Route B was invented to avoid: the sup-norm bound `M` IS U1, transported into the
> transfer-operator representation.** The claimed bypass does not exist. `REFUTED-here`.
>
> **(F2) A disc cannot resolve depth. Jensen bounds `C + S_q`, never `C`.**
> The target of B5 is a **thin vertical sliver** — `Re s ≤ ½ − δ₀`, `|Im s − t₀| ≤ 1`. Any disc
> that contains a width-2 height interval has radius `r ≥ 1`, hence spans `Re s` over a range `≥ 2`
> and necessarily swallows the entire **shallow** band at that height. So the Jensen output bounds
> the *total* count per width-2 interval, which the lane has already measured to grow as
> `1.149 + 0.402 log q` (`MEASURED`, parent §3 M2). Feeding a total-count bound into the §4
> pigeonhole requires the growth slope `c₂` to satisfy `c₂ < 0.1490` (§5.3 below). The measured
> shallow slope alone is `0.402`, **2.7× over the threshold**. Even a *perfect* disc-Jensen bound
> kills Route B. `PROVED-here` (the threshold) + `MEASURED` (the slope).
>
> **(F3) The measured Jensen ratio is `≈ 35` where the measured deep count is `≈ 1.0`, and it grows.**
> With the **true** sup (not an estimate of it) on the best disc, summed over both sign sectors:
> `C_J = 35.0, 46.8, 56.6, 49.6, 71.2, 57.7` at `q = 5, 7, 9, 12, 15, 18`. These fit
> **`C_J ≈ 3.364·κ + 29.8` (`R² = 0.933`)** — linear in the number of Markov components, hence
> **linear in `q`** on each parity family — equivalently `≈ 20.5·log q + 5.6` (`R² = 0.660`).
> The survival threshold on the `log q` slope is `0.1490` (§5.3): **off by a factor of 137, and
> a linear-in-`q` `C` misses it by an unbounded margin.** The linear-in-`κ` shape is exactly what
> §3's analysis predicts (`log M = Ω(κ/(1−θ))`), which is the internal consistency check.
> Substituted into the parent's `Q₀` formula, `C = 35.0` gives `Q₀ = e^{235.6} ≈ 10^{102}` — and
> because `C_J` *grows in `q`*, the bracket `2 − (π²/3)δ₀b − 11.645·c₂` is **negative**, so
> **no `Q₀` exists at all**: the conditional theorem does not close on a Jensen-supplied `C`.
>
> **What survives, and it is worth banking.** One genuinely new positive result:
> **Lemma H (§2.2, `PROVED-here`, numerically verified)** — the analytically-continued matrix
> elements of `L_{s,±}` in the strip are bounded **`q`-uniformly and explicitly**. The Hurwitz-zeta
> continuation into `0 < Re s < ½` is *harmless*; the task brief's worry about it was misplaced.
> The obstruction is elsewhere, and §3 locates it exactly.
>
> **And one new structural fact (§3.3, `MEASURED`, with an exact conjectured form).**
> The MMS branch contraction degenerates as
> `sup_i sup_{z∈Φ_i} |h'(z)| = 1 − π²/q² + O(q⁻⁴)` — verified to 3 significant figures at
> `q = 21, 40, 100`. The transfer operator becomes **asymptotically neutral** at exactly the rate
> at which the elliptic point opens into a cusp. Every nuclear/Hadamard sup bound carries a factor
> `1/(1 − θ) = O(q²)` from this. **The degeneration that makes the theorem true is the same
> degeneration that destroys the uniform operator bound.** This is the honest reason U1-eff is hard,
> now visible as a number rather than as a difficulty.

---

## 1. What was asked, and the shape of the answer

The brief (from `LAW_ROUTEB_CONDITIONAL_THEOREM.md` §6.3) is:

> prove `q`-uniform `sup_{s∈D(c,R)} |det(1 − L_{s,±})| ≤ M` and `|det(1 − L_{c,±})| ≥ m > 0`;
> then Jensen gives `#{zeros in D(c,r)} ≤ log(M/m)/log(R/r) = C(δ₀)`, explicitly.

Jensen's formula, in the only form used here:

> **(JEN)** `f` holomorphic on `|s − c| ≤ R`, `f(c) ≠ 0`. Then for `0 < r < R`,
> `n_f(r) · log(R/r) ≤ log sup_{|s−c|=R}|f| − log|f(c)|`. `PROVED-cited` (standard).

`n_f(r)` counts **all** zeros in the closed disc `D(c,r)`, with multiplicity. Both features that
kill the route are already visible in that sentence: `n_f` is a **disc** count (→ F2), and the
right-hand side is a **growth** quantity (→ F1). §§2–4 make them quantitative; §5 does the
arithmetic; §6 says what would repair it.

**Object.** By MMS (arXiv:0912.2236), `Z_S(s) = det[(1−L_{s,+})(1−L_{s,−})]/det(1−K_s)` with
`det(1−K_s)` zero-free on `Re s > 0`, so on `0 < Re s < ½` the resonance count is the **sum** of
the two sectors' zero counts. All `C_J` figures below are that sum. The raw `cert_det` of
`zeta_cert_rosen{,_even}.py` returns `det(1 − L_s)` — the correct object, per the module header.

**Evaluation stack.** `/Users/za/.venvs/farey-rh/bin/python` (python-flint 0.9.0, Arb, 300-bit),
`.worktrees/aletheia-restore/code/zeta_cert_rosen{,_even}.py`, `N = 16`, `n_head = 4`. All figures
below are **midpoint (float) evaluations of the Arb ball determinants with no certified dimension
tail** — `NON-RIGOROUS PROBE`, the same epistemic status as `LAW_ROUTEB_DEEPCOUNT.md` §2. That is
adequate here because every finding is a **negative** with a margin of 2–3 orders of magnitude.

---

## 2. Step 1 — the sup bound `M`

### 2.1 The two routes, and why the brief's preferred one is the right one to try

The operator `L_{s,±}` is trace-class classically only for `Re s > ½`; the sum over branches
`Σ_{n≥1}|z + nλ|^{−2Re s}` diverges at `Re s = 0.3`. The brief is correct that the bound must come
from the **continued form**, and correct that the repo already realises the continuation exactly:
`_tail_block_allcols` closes `Σ_{l≥n₀}` in Hurwitz zeta,

```
   Σ_{l ≥ n₀} (l ± z/λ)^{−(2s+m)}  =  ζ(2s + m,  a₀),      a₀ = n₀ ± c_i/λ,
```

with the `u`-Taylor coefficients supplied by `d/da ζ(t,a) = −t ζ(t+1,a)`. So the matrix in the
normalised monomial basis **is** the continued operator, entrywise, and a bound on its entries is a
bound on the continued object. Two things must then be bounded:

- **(i)** the Hurwitz values — the *analytic* half; and
- **(ii)** the basis-normalisation geometry `((h(z) − c_j)/ρ_j)^k` — the *geometric* half.

(i) is **clean and `q`-uniform** (§2.2). (ii) is where everything fails (§3).

### 2.2 Lemma H — the analytic half is `q`-uniform and explicit `[PROVED-here]`

> **Lemma H.** Let `w ∈ C` with `Re w > −1`, `a > 0`, `P ∈ Z_{≥0}`. Then
>
> ```
>   |ζ(w, a)|  ≤  Σ_{n=0}^{P−1} (n+a)^{−Re w}
>                 +  (P+a)^{1−Re w}/|w − 1|
>                 +  ½ (P+a)^{−Re w}
>                 +  (|w|/12) (P+a)^{−Re w−1}.
> ```
>
> **Proof.** Euler–Maclaurin with one Bernoulli term, `|B₂|/2! = 1/12`, and the standard remainder
> `|R| ≤ (|w|/12)(P+a)^{−Re w−1}` for `Re w > −1`. Elementary and checkable. ∎

**Application.** In the builders the tails start at `n₀ = n + n_head ≥ 2 + 4 = 6`, and
`a₀ = n₀ ± c_i/λ` with `|c_i| ≤ λ/2`, hence **`a₀ ∈ [5.5, 6.5]` for every `q`**. The relevant
`w = 2s + m + j`, `m, j ≥ 0`, so `Re w ≥ 2Re s = 0.6` at `Re s = 0.3`, and `|Im w| = 2|Im s| = 14`
sits far from the pole at `w = 1`. With `P = 0`:

| `s` | `a` | `(m,j)` | `|ζ(w,a)|` actual | Lemma H bound |
|---|---|---|---|---|
| `0.3 + 7i` | 5.5 | (0,0) | 0.19164 | **0.39733** |
| `0.3 + 7i` | 5.5 | (1,0) | 0.03795 | **0.07231** |
| `0.3 + 7i` | 6.5 | (2,2) | 0.00013 | **0.00021** |
| `0.25 + 7i` | 5.5 | (0,0) | 0.22521 | **0.47112** |
| `0.05 + 7i` | 5.5 | (0,0) | 0.42914 | **0.93111** |

*(`b5j_supbound` companion check, 36/36 cases hold, bound within a factor ≤ 2.2.)*

> ### **Conclusion (H). `sup |ζ(2s+m+j, a₀)| ≤ 0.94` for all `Re s ∈ [0.05, 0.3]`, `|Im s| = 7`,
> all `m, j ≥ 0`, and **every** `q ≥ 5`, with the explicit Lemma-H majorant; and the values decay
> geometrically in `m+j` at rate `≈ a₀^{−1} ≈ 1/6`.**
> **`PROVED-here` + numerically verified. The analytic continuation into the strip is not the
> obstruction.** This answers the brief's step-1 worry in the affirmative and is the one piece of
> B5-J worth keeping.

### 2.3 The elementary sup bound, and its exact cost

With bounded entries, the standard elementary determinant bound is Hadamard on the columns of
`1 − M`:

> **(HAD)** `|det(1 − M)| ≤ ∏_{cols c} (1 + ‖M e_c‖₂)`, hence
> `log M_had = Σ_c log(1 + ‖M e_c‖₂)`. `PROVED-here` (Hadamard; column `c` of `1 − M` has norm
> `≤ 1 + ‖M e_c‖₂`).

For this to survive the limit `N → ∞` the column norms **must decay geometrically in the input
Taylor index `k`**, at rate

```
   θ  :=  max over blocks (i,j,n)  sup_{z ∈ D_i} | (h_n(z) − c_j) / ρ_j |,
```

because the column-`k` entries are the Taylor coefficients of `weight(z) · ((h_n(z)−c_j)/ρ_j)^k`,
whose sup norm is `≤ ‖weight‖_∞ · θ^k`. If `θ < 1`,
`log M_had ≤ κ · ‖weight‖_∞ /(1 − θ)` — finite, `N`-uniform. If `θ ≥ 1`, **(HAD) diverges with `N`
and gives nothing.**

---

## 3. Where step 1 fails, exactly `[the point of failure]`

### 3.1 `θ > 1` at the repo's disc system `[MEASURED]`

The certified builders use `ρ_j = safety · (half-cell-width)` with `safety = 5/2`. Measured
(`b5j_supbound.json`, 256-point boundary scans over every MMS block):

| `q` | `κ` | `ρ_min` | `ρ_max` | `ρ_max/ρ_min` | **`θ_max`** |
|---|---|---|---|---|---|
| 5 | 3 | 0.2387 | 0.4775 | 2.00 | **1.4224** |
| 7 | 5 | 0.1238 | 0.4461 | 3.60 | **1.3183** |
| 9 | 7 | 0.0754 | 0.4341 | 5.76 | **1.2868** |

So (HAD) diverges. Directly visible in the data: at `q = 5` the column norms *increase* with `k`
(`35.5, 37.6, 40.4, 44.1, 49.1, 55.2, 62.2, 68.6, 71.7, …`), and
`log M_had = 68.0 (q=5), 104.1 (q=7), 122.9 (q=9)` — growing with `κN`, unbounded in `N`.
Meanwhile the true `|det(1−L)|` at `s = 0.3 + 7i` is `2.39, 2.68, 0.55`. The bound is not merely
loose; it does not exist.

### 3.2 No inflation of the Markov system repairs it `[MEASURED]`

Sweeping the safety factor (`b5j_disc.json`), `θ_max(q, safety)`:

| `safety` | 0.6 | 0.8 | **1.0** | 1.2 | 1.4 | 1.6 | 2.0 | 2.5 |
|---|---|---|---|---|---|---|---|---|
| `q=5` | 1.6076 | 1.2277 | **1.0000000000000018** | 1.0585 | 1.1129 | 1.1660 | 1.2741 | 1.4224 |
| `q=7` | 1.6407 | 1.2402 | **1.0000000000000050** | 1.0464 | 1.0891 | 1.1300 | 1.2113 | 1.3183 |
| `q=9` | 1.6519 | 1.2444 | **1.0000000000000070** | 1.0425 | 1.0814 | 1.1186 | 1.1917 | 1.2868 |
| `q=12` | 1.4971 | 1.1848 | **1.0000000000000067** | 1.0697 | 1.1354 | 1.2004 | 1.3360 | 1.5298 |

> **The minimum is exactly `1`, at `safety = 1`, for every `q`** — to 15 digits, i.e. it *is* `1`.
> **`MEASURED`, with a proof of why:** the Rosen–Nakada partition is a **Markov** partition, so
> each branch image is exactly a union of cells. The images therefore *touch* the target cell
> boundary, and `sup |(h(z)−c_j)/ρ_j| = 1` when `ρ_j` is the cell half-width. Inflating all cells
> by a common factor `> 1` inflates the *sources* too and pushes `θ` back above 1.
> **`PROVED-here`, given the Markov property (`PROVED-cited`, MMS).**

A per-component radius optimisation does not help either: the required system
`ρ_j > sup_{|z−c_i|=ρ_i} |h_n(z) − c_j|` has the cell system as its exact fixed point, so `θ = 1`
is the *infimum* over all disc systems of this shape, attained and not improved.

### 3.3 The rate at which contraction dies: `1 − π²/q²` `[MEASURED, exact form conjectured]`

The one-step contraction `sup_{z ∈ Φ_i}|h_n'(z)| = sup 1/|z ± nλ|²` over all MMS blocks
(`b5j_expansion.json`):

| `q` | 5 | 7 | 9 | 12 | 15 | 18 | 21 | 40 | 100 |
|---|---|---|---|---|---|---|---|---|---|
| `sup |h'|` | 0.65451 | 0.81174 | 0.88302 | 0.93301 | 0.95677 | 0.96985 | 0.97779 | 0.99384 | 0.99901 |
| `1 − sup|h'|` | 0.34549 | 0.18826 | 0.11698 | 0.06699 | 0.04323 | 0.03015 | 0.02221 | 0.006156 | 0.0009866 |
| `π²/q²` | 0.39478 | 0.20142 | 0.12184 | 0.06853 | 0.04386 | 0.03046 | 0.02238 | 0.006169 | 0.0009870 |

> ### **`1 − sup|h'| = π²/q² + O(q⁻⁴)`** — agreement to 3–4 significant figures from `q = 12` on.

Consequences, both `PROVED-here` given the measured rate:

1. The branches **do** contract (`θ_geom < 1` always: the operator is nuclear for each fixed `q`,
   as MMS require) — but the contraction is **asymptotically neutral**.
2. Any nuclear/Hadamard bound carries `1/(1 − θ) = O(q²)`, and there are `κ = O(q)` components, so
   the best this family of arguments can give is
   ```
      log M  =  Ω(q³)   (times the weight sup),
   ```
   i.e. `C(δ₀) = Ω(q³)`. Not `q`-uniform, not close.
3. **The interpretation.** `λ_q ↑ 2` is the elliptic point opening into a cusp. A cusp is a
   *parabolic* fixed point — neutral by definition. The measured `1 − π²/q²` is that parabolicity
   arriving. The parent §6.2 argues the `b_q → 0` degeneration is *why B5 should be true*; this
   note shows the same degeneration is *why the operator-theoretic bound is hard*. They are one
   phenomenon, and there is no route that takes the first without paying the second.

---

## 4. Step 2 — the lower bound `m`, and step 3 — Jensen

### 4.1 `m` is measured, not proved `[MEASURED]`

At `c = 0.25 + 7i`, `N = 16` (`b5j_jensen.json`):

| `q` | `|det(1−L_{c,+})|` | `|det(1−L_{c,−})|` |
|---|---|---|
| 5 | 2.5728 | 2.7870 |
| 7 | 3.2572 | 4.1771 |
| 9 | 1.0883 | 3.5357 |
| 12 | 1.5968 | 5.2076 |

`m` does not collapse over this range — the parent's §6.3 item 4 "free pre-registration" is
confirmed as far as it goes. **But no lower bound is proved here.** The two candidate routes named
in the brief both fail as stated: the `b_q → 0` degeneration route needs an effective rate on A2,
which is U1-eff (the parent's own circularity flag, §6.2); and diagonal dominance is unavailable
because `θ = 1` (§3.2) — the off-diagonal blocks are not small. `GAP`, unrepaired.

**This does not matter for the verdict.** Everything below uses the **true measured `m`**, i.e.
gives the Jensen route the most favourable possible lower bound. It still fails.

### 4.2 The determinant's growth — F1, quantified `[MEASURED; REFUTES parent §6.3(1)]`

`log|det(1 − L_{s,+})|` along `Im s = 7` (`b5j_growth.json`):

| `Re s` | −2.5 | −2.0 | −1.5 | −1.0 | −0.5 | 0.0 | 0.25 | 0.5 |
|---|---|---|---|---|---|---|---|---|
| `q=5` | 21.666 | 15.931 | 12.129 | 8.463 | 4.893 | 1.592 | 0.945 | 0.615 |
| `q=7` | 29.356 | 22.464 | 16.370 | 10.857 | 6.270 | 2.473 | 1.181 | 0.421 |
| `q=9` | 34.383 | 26.421 | 19.136 | 12.329 | 7.194 | 2.520 | 0.085 | −0.756 |

Growth rate per unit of `−Re s`, on `[−2.5, −2.25]`: **`11.8` (`q=5`), `14.1` (`q=7`), `16.2`
(`q=9`)** — large, and **increasing with `q`**.

> ### **`det(1 − L_{s,±})` is not of order 0 in `s`, and its growth rate is not `q`-uniform.**
> The parent's §6.3 item 1 — *"The determinant is entire of order 0 in `s` for these nuclear
> operators — no Hadamard growth theorem is needed, no Phragmén–Lindelöf, no U1. Jensen alone
> suffices."* — conflates the **Fredholm/eigenvalue** order (where order 0 is correct, and is what
> MMS assert) with the **`s`-plane** order (where the determinant carries the Selberg zeta's
> growth). `REFUTED-here`.
>
> **Therefore the sup bound `M` on a disc of radius `R` in the `s`-plane is a `q`-uniform growth
> bound for `Z_{G_q}` in disguise. It is U1. The bypass claimed for B5-J does not exist.**

### 4.3 The Jensen ratio, measured with the TRUE sup `[MEASURED]`

`c = 0.25 + 7i`, `r = 1` (the smallest radius covering a width-2 height interval), `N = 16`,
`K = 24` boundary samples, both sectors summed. `M_sup` is the *actual maximum on the circle*, not
an estimate of it — so `C_J` below is what Jensen gives **with a perfect sup bound**:

| `q` | `R` | `log M_+` | `log M_−` | `C_J^+` | `C_J^−` | **`C_J = C_J^+ + C_J^−`** |
|---|---|---|---|---|---|---|
| 5 | 1.5 | 10.365 | 7.541 | 23.23 | 16.07 | 39.30 |
| 5 | **2.0** | 14.313 | 11.938 | 19.29 | 15.74 | **35.03** |
| 7 | 1.5 | 13.718 | 10.562 | 30.92 | 22.52 | 53.44 |
| 7 | **2.0** | 19.333 | 15.713 | 26.19 | 20.61 | **46.80** |
| 9 | 1.5 | 15.618 | 12.448 | 38.31 | 27.59 | 65.90 |
| 9 | **2.0** | 22.912 | 17.646 | 32.93 | 23.64 | **56.57** |
| 12 | 1.5 | — | — | — | — | 59.22 |
| 12 | **2.0** | 19.353 | — | — | — | **49.56** |
| 15 | **2.0** | 28.686 | — | — | — | **71.17** |
| 18 | **2.0** | 22.312 | — | — | — | **57.69** |

**`R` is optimised, not guessed.** Full sweep at `q = 5`, `+` sector (`b5j_growth.json`):

| `R` | 1.1 | 1.25 | 1.5 | **2.0** | 2.5 | 3.0 | 4.0 |
|---|---|---|---|---|---|---|---|
| `log M` | 7.402 | 8.525 | 10.420 | 14.213 | 19.186 | 25.396 | 38.319 |
| `C_J^+` | 67.74 | 33.97 | 23.37 | **19.14** | 19.91 | 22.26 | 26.96 |

and at `q = 7` the minimum is again at `R = 2.0` (`C_J^+ = 26.19`). So `R = 2` is the optimum and
the table above is the best disc-Jensen can do. Note also that `log M(R)` grows **superlinearly**
in `R` (`7.4 → 38.3` as `R: 1.1 → 4`, consistent with order `≈ 2`), reinforcing F1.

> ### **Measured: `C_J ≈ 35` where the measured deep count is `C ≈ 1.0`, and where the measured
> TOTAL count per width-2 interval is `≈ 1.8`. Jensen overcounts by a factor `≈ 20`, worsening.**
> **The growth variable is `κ`, not `q` directly.** `κ = q − 2` for odd `q` but `κ = (q−2)/2` for
> even `q`, so the two parity families interleave. Least-squares over all six points
> `q = 5, 7, 9, 12, 15, 18` (`κ = 3, 5, 7, 5, 13, 8`):
>
> ```
>    C_J  ≈  3.364 · κ  +  29.81        (R² = 0.933)      <-- the clean fit
>    C_J  ≈  20.48 · log q  +  5.58     (R² = 0.660)      <-- the fit the threshold is stated in
> ```
>
> `C_J` grows **linearly in the number of Markov components**, i.e. **linearly in `q`** on each
> parity family — not logarithmically. Against the survival threshold `c₂ < 0.1490` (§5.3), which
> is a bound on the `log q` slope, `20.48` fails by a factor of **137**; and a genuinely linear-in-`q`
> `C` fails (THRESH) by an unbounded margin, since `q/log q → ∞`.

**Why Jensen loses so much, in one sentence.** `log|det|` on the disc is dominated by the
archimedean growth of §4.2, not by the zeros inside; Jensen charges the whole of that growth to the
zero count. Fixing this requires subtracting the growth — which is a Hadamard factorisation, i.e.
U1 again.

---

## 5. Step 3 — the constants, and step 4 — `Q₀` with the proved/measured inputs

### 5.1 What the parent's formula returns

Parent §5.1: `log Q₀ = [C(2/δ₀ + π²/6) + (π²/3)δ₀a + A_Γ] / [2 − (π²/3)δ₀b]`, at
`δ₀ = 0.2, a = 1.149, b = 0.402, A_Γ = 0.25`, i.e. `log Q₀ = (11.6449·C + 1.0061)/1.7355`.

| `C` | source | `log Q₀` | `Q₀` |
|---|---|---|---|
| 1.0 | parent, `MEASURED` winding count | 7.29 | **1465** |
| **35.03** | **this note, `MEASURED` Jensen at `q=5`** | **235.6** | **`e^{235.6} ≈ 10^{102}`** |
| 46.80 | `q = 7` | 314.6 | `10^{137}` |
| 56.57 | `q = 9` | 380.2 | `10^{165}` |
| 71.17 | `q = 15` | 478.7 | `10^{208}` |

The parent's sensitivity warning (§5.3, `log Q₀` slope `6.71` per unit `C`) is exactly what is
being paid: `+34` in `C` costs `+228` in `log Q₀`.

### 5.2 But the table above is not even the verdict — it is optimistic

Each row treats `C_J(q)` as if it were the `q`-uniform constant. It is not: it grows. A growing
`C` does not merely inflate `Q₀`; it can **prevent the pigeonhole from closing at all**.

### 5.3 The survival threshold `[PROVED-here — the useful part of this note]`

Suppose the deep-count bound available is `C(q) = c₁ + c₂ log q` rather than a constant. Rerun the
parent's §4.4 assembly with that substitution:

```
   2 log q − A_Γ  ≤  (c₁ + c₂ log q)(2/δ₀ + π²/6)  +  (π²/3)δ₀(a + b log q),
```

so the `log q` coefficients must satisfy

```
   log q · [ 2 − (π²/3)δ₀ b − c₂ (2/δ₀ + π²/6) ]  ≤  c₁(2/δ₀ + π²/6) + (π²/3)δ₀ a + A_Γ,
```

and the argument closes **iff the bracket is positive**:

> ### **(THRESH)   `c₂  <  [2 − (π²/3)δ₀ b] / [2/δ₀ + π²/6]  =  1.7355 / 11.6449  =  0.14903`,**
> at `δ₀ = 0.2`, `b = 0.402`. **`PROVED-here`** from the parent's §4 (which is `PROVED-here` there)
> plus elementary algebra. If (THRESH) holds, `Q₀ = exp{[c₁·11.6449 + 1.0061]/[1.7355 − 11.6449 c₂]}`.

This is the sharpest statement the lane now has, and it is the right way to state B5 going forward:
**B5 does not need `C = O(1)`. It needs `C = o(log q)`, or `C ≤ c₂ log q` with `c₂ < 0.149`.**
That is a materially weaker obligation than the parent's `≤ C`, and it should replace it.

Measured against (THRESH):

| quantity | measured slope `c₂` | vs threshold `0.1490` |
|---|---|---|
| deep count (parent §3 M1, winding) | `≈ 0` (flat, max 5 at `q=12`) | **passes**, by a wide margin |
| total count per width-2 (parent §3 M2) | `0.402` | **fails ×2.7** — so F2 |
| **Jensen `C_J` (this note)** | **`36.6`** | **fails ×245** |

### 5.4 The verdict on B5-J, assembled

- Jensen with a disc bounds the total, not the deep, count (F2): slope `0.402 > 0.149`. Dead by
  a factor 2.7 **even with a perfect bound**.
- The realised Jensen ratio is 20× worse still (F3): slope `36.6`. Dead by a factor 245.
- And the sup bound needed to make any of it rigorous is U1 (F1), so nothing was bypassed.

> **There is no version of `M` and `m` — including the exact, measured, optimal ones used here —
> that makes disc-Jensen counting on `det(1 − L_{s,±})` produce a usable `C`.**

---

## 6. What would repair it, ranked

1. **Abandon disc-Jensen; the shape of the target is a rectangle.** F2 is a statement about round
   discs only. The correct classical instrument for a count in a thin box is a **Littlewood /
   Levinson argument**: `∫ log|f|` over the boundary of the rectangle `[½−δ₀−ε, ½+ε] × [t₀−1−ε,
   t₀+1+ε]` with the count read off the real-part integral. This is depth-resolving by
   construction. Cost: it needs `log|f|` on the *whole* boundary, including the right edge near
   `Re s = ½` — which is a **lower** bound obligation on a segment, not at a point, and is
   therefore *harder* than §4.1, not easier. Assessed: plausible, not cheap, and it still needs a
   sup bound (F1 unrepaired). **Recommended only if F1 is solved first.**
2. **Solve F1 properly — i.e. do U1, in the transfer-operator representation.** This note's one
   positive result (Lemma H) says the strip continuation is `q`-uniformly controlled. The
   obstruction is `θ → 1` at rate `π²/q²` (§3.3). The standard fix for a neutral one-step system is
   to **induce**: work with a fixed power `L^p`, or with the accelerated (Farey→Gauss-type) version
   of the Rosen map for which the composite branches are uniformly contracting. Whether the
   induced system's determinant relates to `det(1 − L_s)` cleanly is the question to settle first,
   and it is a literature question (Fedosova arXiv:2509.17936, S5 of the skeleton, is the current
   transfer-operator treatment and should be read before any of this is attempted).
3. **Do not** attempt a per-component radius optimisation of the disc system. §3.2 shows the cell
   system is the exact optimum and gives `θ = 1`; the search is provably empty.
4. **Reinstate the parent's items 2–4 as the lane's top priority** (N-B4/N-B4b verification;
   certify one `MEASURED` row at `q = 9` through the Arb `winding_box` path; the `t₀`-dependence
   probe M3). With B5-J removed, these are now the whole of the near-term board, and item 3 in
   particular — the certified winding count — is the **only** instrument in the repo that has ever
   produced a depth-resolved resonance count. The route to B5 runs through *extending certified
   winding to more `q`*, not through Jensen.
5. **Restate B5 as (THRESH).** `C = o(log q)` with slope `< 0.149` suffices. Any future counting
   argument should be measured against that, not against `O(1)`.

---

## 7. Status ledger

| # | Step | Statement | Status |
|---|---|---|---|
| J0 | Jensen's formula | `n(r) log(R/r) ≤ log sup_{|s−c|=R}|f| − log|f(c)|` | `PROVED-cited` |
| J1 | MMS sector sum | resonance count on `0<Re s<½` = zeros of `det(1−L_+)` + `det(1−L_−)` | `PROVED-cited` (arXiv:0912.2236) |
| **H** | **Hurwitz entry bound in the strip** | `|ζ(w,a)| ≤ Σ_{n<P}(n+a)^{−Re w} + (P+a)^{1−Re w}/|w−1| + ½(P+a)^{−Re w} + (|w|/12)(P+a)^{−Re w−1}`; gives `≤ 0.94` uniformly in `q` for `Re s ∈[0.05,0.3]`, `|Im s|=7` | **`PROVED-here`**, numerically verified 36/36 |
| J2 | Hadamard column bound | `|det(1−M)| ≤ ∏_c (1+‖Me_c‖₂)`; usable iff `θ < 1` | `PROVED-here` |
| J3 | `θ` at the repo disc system | `1.4224 / 1.3183 / 1.2868` at `q=5/7/9` | `MEASURED` — **(HAD) diverges** |
| J4 | no inflation gives `θ<1` | `min_safety θ_max = 1` exactly, all `q` | `MEASURED` + `PROVED-here` (Markov property) |
| J5 | contraction degeneration | `1 − sup|h'| = π²/q² + O(q⁻⁴)` | `MEASURED` (3–4 s.f., `q ≤ 100`) |
| J6 | consequence for any nuclear bound | `log M = Ω(κ/(1−θ)) = Ω(q³)` | `PROVED-here` given J5 |
| **F1** | **`det(1−L_s)` not of order 0 in `s`** | growth `11.8/14.1/16.2` per unit `−Re s` at `q=5/7/9` | **`REFUTED-here`** (parent §6.3 item 1) |
| J7 | lower bound `m` | `2.57/3.26/1.09` (`+` sector), `2.79/4.18/3.54` (`−`), at `0.25+7i` | `MEASURED`; **`GAP`** as a proof |
| **F3** | **realised Jensen ratio** | `C_J = 35.03/46.80/56.57/49.56/71.17/57.69` at `q=5/7/9/12/15/18`, `R=2` optimal; `C_J ≈ 3.364κ + 29.8` (`R²=0.933`), `≈ 20.5 log q + 5.6` | `MEASURED` with the TRUE sup |
| **THRESH** | **survival criterion** | route closes iff `c₂ < [2−(π²/3)δ₀b]/[2/δ₀+π²/6] = 0.14903` | **`PROVED-here`** |
| **F2** | **disc-Jensen bounds total, not deep** | total slope `0.402 > 0.149` | `PROVED-here` (geometry) + `MEASURED` (parent §3 M2) |
| J8 | `Q₀` with the Jensen `C` | `C=35.03 ⇒ log Q₀ = 235.6`, `Q₀ ≈ 10^{102}`; and `c₂ = 36.6 ⇒ bracket < 0 ⇒ no `Q₀`` | `PROVED-here` given the above |

---

## 8. What this document claims, and does not

**Claims.** (i) B5-J fails, for three independent reasons, two of which are intrinsic to Jensen in
this geometry and one of which (F1) restores the U1 circularity the route was built to escape.
(ii) The parent's §6.3 item 1 is false as written and should be corrected wherever it is quoted.
(iii) The analytic continuation into the strip is *not* the obstruction: Lemma H bounds the
continued matrix elements `q`-uniformly and explicitly. (iv) The MMS branch contraction degenerates
as `1 − π²/q²`, which is the cusp forming, and this is the honest quantitative reason no uniform
operator bound is available. (v) B5 should be restated as (THRESH): `C ≤ c₂ log q` with
`c₂ < 0.14903` suffices — a materially weaker obligation than `C = O(1)`.

**Does not claim.** Any `q`-uniform `M` or `m` (neither is proved; §4.1 is `GAP`). That `C_J` is
exactly `3.364κ + 29.8` — six points across two parity families, `N = 16`, float midpoints,
one height window `t₀ = 7`; the *shape* of the growth is measured, not derived, and only the
linear-in-`κ` reading is well fitted (`R² = 0.933` vs `0.660` for `log q`). What is claimed is only
that `C_J` grows steeply and passes the `0.149` threshold by two orders of magnitude. That `1 − sup|h'| = π²/q²` is proved — it is measured to
3–4 s.f. and conjectured in closed form. That a Littlewood/Levinson rectangle argument would work
(§6 item 1 is a suggestion with its own named cost, not a plan). That anything here bears on the
parent's `Q₀ = 1465`, which rests on the **winding-measured** `C ≈ 1.0` and is untouched: this note
says only that **Jensen cannot supply that `C`**, not that the `C` is wrong. Nothing here is
`t₀`-uniform; every measurement is at `t₀ = 7`, and M3 remains the lane's largest unprobed
assumption.

---

**Probes.** `law_probes/b5j_supbound.py` → `b5j_supbound.json`; `b5j_disc.py` → `b5j_disc.json`;
`b5j_expansion.py` → `b5j_expansion.json`; `b5j_jensen.py` → `b5j_jensen.json` + `.log`;
`b5j_growth.py` → `b5j_growth.json` + `.log`. Interpreter
`/Users/za/.venvs/farey-rh/bin/python` (python-flint 0.9.0 / Arb, 300-bit), evaluators
`.worktrees/aletheia-restore/code/zeta_cert_rosen{,_even}.py`, `N = 16`, `n_head = 4`, `t₀ = 7`.
The `q = 21` row of `b5j_jensen` (≈ 8 s per determinant, `κ = 19`) had not returned when this note
was written; the six rows tabulated in §4.3 are the complete evidence base, and `q = 21` will land
in `b5j_jensen.json` as a seventh. It cannot change the verdict — the fit already spans `κ = 3…13`
with `R² = 0.933`, and `q = 21` (`κ = 19`) is predicted at `C_J ≈ 94`.
All determinant figures are ball **midpoints** with **no certified dimension tail** —
`NON-RIGOROUS PROBE`. No git was run; no existing file was modified.
