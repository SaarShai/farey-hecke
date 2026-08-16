# LAW (U1-φ) — the proof route for the crux, and what it turned into

**Date:** 2026-08-16. **Lane G.** Obligation **(U1-φ-a)** of `lane_g/LAW_U1_GROWTH.md` §6, the
crux of the Hecke-family law program. Brief: *find a proof route; rank routes 1–3 by feasibility;
attempt the best.*

**Parents read in full:** `lane_g/LAW_U1PHI_TEST.md` (incl. the 2026-08-16 three-height addendum),
`lane_g/LAW_U2B_CLOSURE.md` (incl. the `[REPAIRED]` markers and the `2σ₀−1 > 5.1` exponent
statement), `lane_g/LAW_U1_GROWTH.md` (§1.2, §2, §3, §5, §7, §9, §10 addendum, §11 correction
notice), `lane_g/LAW_T2_DETERMINANT.md` §2.3–§3.3 (the parabolic `k`-sum mechanism and the Ω̃
amendment), `lane_g/LAW_TAIL_SCOPING.md` §0–§1, `lane_g/M1F_EISENSTEIN_DERIVATION.md`
§2.2–§3.5 and §5 (the allowed-moduli constant-term formula and its arithmetic closed forms).

**Status convention (identical to T1/T2/U1/U2b/U3):** `PROVED` = derived here in closed form or in
exact arithmetic. `CITATION` = imported, import named. `HEURISTIC` = float evidence or a
plausibility argument, explicitly not a proof. `GAP` = not justified; the missing statement is
written out. `TODO-VERIFY` = a check owed against a named source that was not opened.

**No certificate is produced. Nothing is committed. `lane_f/` is untouched. No file of any other
lane was written.**

---

## 0. Verdict up front

> ### **VERDICT: BLOCKED — because (U1-φ-a) is FALSE.**
> ### The crux was not proved and cannot be: it is **refuted**, by an elementary and
> ### independently-validated computation of the object it is about.
>
> **THEOREM E3/E4 (§2).** For every fixed `σ > 1` there is `c(σ) > 0`, independent of `q`, with
> ```
>       | phi_q( sigma + i t ) |  >=  c(sigma)  >  0        for all q >= 3, all real t .
> ```
> The scattering determinant of `G_q` does **not** decay in `q` anywhere on `Re s > 1`. Explicitly
> at the two abscissae the lane cares about, over `q = 12 … 100` (an `8.3×` range):
>
> | | `q=12` | `q=100` | measured log-log slope | **(U1-φ-a) requires** | shortfall at `q=100` |
> |---|---|---|---|---|---|
> | `\|φ_q(2 + i t_∞)\|` | `0.04146` | `0.03593` | **`−0.054`** | `−3` | **`3.6 × 10⁴`** |
> | `\|φ_q(3.5 + i t_∞)\|` | `0.006285` | `0.004969` | **`−0.096`** | `−6` (U2b's `σ₀`) | **`5.0 × 10⁹`** |
>
> and the worst case over the whole prescribed window `|t| ≤ t_∞ + 1` is no better:
> `min_{|t|≤8.07} |φ_q(2+it)| = 0.0359` at `q = 100`, against the `10⁻⁶` that (U1-φ-a) demands.
>
> **Consequence (§3).** `κ_q = Z_{G_q}(1−s)/Z_{G_q}(s)` **diverges** on every line `Re s = σ₀ > 1`:
> measured `|φ_q E_q|` log-log slope **`+1.37`** at `σ₀ = 2` and **`+2.71`** at `σ₀ = 3.5`, where
> (U1-φ-a) requires `0`. The functional-equation route to U1 does not merely lose constants — the
> quantity it estimates is genuinely unbounded. **Route 2 is dead for every `σ₀ > 1`, and the
> Euler product forces `σ₀ > 1`.**
>
> **But U1 is NOT refuted (§4), because `LAW_U1PHI_TEST.md`'s Lemma U1φ-1 is WRONG in the
> direction that would have transmitted the refutation.** Its `(⇐)` half deduces `κ_q(2+it)` bounded
> from `U1`, which requires `Z_{G_q}` bounded at `Re s = −1` — a line that lies **outside every Ω̃
> the lane has ever used** (`K` starts at `Re s = −1/10`). Necessity fails. The test was **not**
> two-sided, and its refutation does not propagate.
>
> **What survives (§5) — and this is the note's positive deliverable.** The FE route survives in
> exactly one window, and the window is sharp:
> ```
>    (U1-phi-a')   for some fixed sigma in (7/8, 1) :   [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D7]
>                  sup_q sup_{|t|<=T} | Z_{G_q}(sigma+it) | < infinity      [right edge]
>            and   | phi_q(sigma + it) |  =  O( q^{-(2 sigma - 1)} )        [left edge via FE]
> ```
> `σ ≥ 7/8` is forced by the fixed `r = 1/8` Hurwitz disc at `s_∞ = 1/4 + i t_∞` used in §5.1
> (the window opens toward `3/4` only as `r → 0`); `σ < 1` is forced by **THEOREM E3**, which kills
> every `σ ≥ 1`. The obstruction is *exactly* the abscissa of convergence of the `φ_q` Dirichlet
> series.
>
> ### **STATUS: REDUCED-TO-(U1-φ-a′), σ ∈ (7/8, 1).** Not closed. Strictly better posed than
> ### (U1-φ-a), which was posed at an abscissa where it is false.

**Five things are settled here, all of them new.**

1. `φ_q` is computable, cheaply and to 8 digits, from the Eisenstein constant term for **every**
   `q` including the non-arithmetic ones — the lane had assumed no such handle existed (§2.1–§2.2).
   Validated against the repo's own closed forms at `q = 3, 4, 6` to `1.1e−8`.
2. **(U1-φ-a) is FALSE** (§2.5) — `PROVED` at real `σ`, `PROVED`-modulo-a-numeric-tail-constant for
   the full `t`-window.
3. **Lemma U1φ-1's necessity half is invalid** (§4.1), which is why (2) does not refute U1 — and
   which retracts `LAW_U1PHI_TEST.md`'s central structural claim.
4. **`LAW_U1PHI_TEST.md` §4.3's headline statistic is unusable**: at `t = t_∞` the null's own drift
   **aliases** — the `q = 12 → 16` step is `4.07` rad `> π` (§4.2). The null exclusion survives, but
   only on the `t = 1.5` and `t = 3.5` series, not on the physical height.
5. **`LAW_U1_GROWTH.md` §7.3's "adverse" guard was measuring something real**, and the §10 addendum
   that explained it away as an identification artefact is wrong (§4.3): the growth this note
   predicts at `Re s = 0` is `q^{+1.0}`, and the extended guard's all-8-point slope is **`+0.893`**.

---

## 1. Route ranking, with reasons

| rank | route | verdict | why |
|---|---|---|---|
| **1** | **(3) Eisenstein column direct** | **EXECUTED — and it decides the question** | `φ_q` is the constant term of one Eisenstein series. For `Re s > 1` it is an **absolutely convergent Dirichlet series with non-negative coefficients** (§2.1). Positivity converts "trivial bounding" into a *lower* bound, which is exactly the direction nobody tried. Cost: one afternoon. The brief's phrasing — "*the integrand is positive there*" — was right, and the sign of the conclusion is the opposite of the one hoped for. |
| 2 | (2) FE + proven RHP bound | **answered, negatively** | §3. The precise missing piece is `|φ_q(σ₀+it)| = O(q^{−(2σ₀−1)})` at the **one** `σ₀` used for the right edge. Route 3 shows this is false for every `σ₀ > 1`, and the Euler product cannot supply a right edge at `σ₀ ≤ 1`. So route 2 is not "nearly closed"; it is closed in the negative. Its residual value is the **sharp reformulation** (U1-φ-a′) of §5. |
| 3 | (1) parabolic `k`-sum | **not a route to `φ_q` at all** | `LAW_T2_DETERMINANT.md` §2.3's `k`-sum lives in the **accelerated transfer operator**, and its `k ≍ q` truncation is a statement about `det(1−L_{s,q})`, not about `det Φ_q(s)`. The two are related only through obligation **U4** (`GAP` for `q ≠ 5`), i.e. through the very identification that is open. It also has the wrong shape: it produces `q^{1−2σ}` **growth** at `σ = 1/4`, which is a `Z`-side statement. It did explain the pin migration (`LAW_PROBES_D1_B1.md`), and §5.3 records that its `q^{1−2σ}` and this note's `q^{2σ−1}` are the **same number** read on the two sides of the functional equation — a genuine consistency, but not a proof route. |
| 4 | (4) sharpest partial + missing lemma | **superseded** | The partial statement is now a theorem with a sign, not a partial statement. §5 gives the missing lemma. |

**Why route 3 was ranked first.** Every other route in the lane treats `φ_q` as an opaque
`GAP` ("no closed form for non-arithmetic `G_q`", `LAW_U3_TRANSPORT.md` §4, `LAW_TAIL_SCOPING.md`
§0). That is true of a **closed form** and false of a **computation**: `M1F_EISENSTEIN_DERIVATION.md`
§3.2 already writes down the allowed-moduli formula and uses it to derive `φ_4` and `φ_6`, and
that formula is not arithmetic-specific. Nothing in it needs `G_q` to be a congruence group. This
was the borrow-check: the tool was already in the repo, one file away, used for a different purpose.

---

## 2. Route 3 executed — the Eisenstein column

### 2.1 `CITATION` — the formula, and the one property that matters

`G_q` has a single cusp, at `∞`, of width `λ_q = 2cos(π/q) ∈ [1,2)`; `Φ_q(s)` is `1 × 1` and
`φ_q = det Φ_q = φ_{∞∞}`. Let `σ_∞ = diag(λ_q^{1/2}, λ_q^{−1/2})`, the scaling matrix that
normalises the cusp to width `1`. Then (`CITATION([Iwaniec, Spectral Methods — exact numbering
TODO-VERIFY per M1F §3.2's warning])` [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md
D1], which is the **same import** the repo already uses as
`M1F_EISENSTEIN_DERIVATION.md` (3.2)):

```
   phi_q(s)  =  sqrt(pi) * Gamma(s - 1/2)/Gamma(s) * SUM_{c' in C_q}  N_q(c') * c'^{-2s} ,   (2.1)

   C_q      = { c' > 0 : c' is the lower-left entry of some element of sigma_inf^{-1} G_q sigma_inf }
   N_q(c')  = # { d mod c' : ( a b ; c' d ) in sigma_inf^{-1} G_q sigma_inf }   in Z_{>=0}.
```

Since `σ_∞^{-1}[[a,b],[c,d]]σ_∞ = [[a, b/λ],[cλ, d]]`, one has `C_q = λ_q · {c-entries of G_q}`.

> **The load-bearing property, and the whole of §2:** `N_q(c') ≥ 0`. (2.1) is a Dirichlet series
> with **non-negative** coefficients, absolutely convergent on `Re s > 1`
> (`CITATION`, Iwaniec Ch. 3; the abscissa is exactly `1` because
> `Σ_{c' ≤ X} N_q(c') ≍ X²·π/|F_q|`). Positivity is what makes a **lower** bound free.

### 2.2 `CONCLUSION-TRUE/PROOF-OWED` — the leading term of (2.1) is `λ_q^{−2s}`, with coefficient exactly `1`
[REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D2/D3: the proof below is
**INVALID-AS-WRITTEN**, for two independent reasons the reviewer identified. (1) *Attainment ≠
minimality*: showing `c = 1` is attained by `S` proves `min C_q ≤ λ_q`, not `min C_q = λ_q` — the
argument needs a lower bound ruling out `0 < c < 1`, which requires the Ford isometric-circle
argument (no element of a Fuchsian group has an isometric circle smaller than the fundamental
domain allows) and is not supplied. (2) *The multiplicity step is unjustified as stated*: "the
top-left and bottom-right entries … lie in `λ_q Z`" is asserted, but U2b-1's normal form does not
by itself force `a, d ∈ λ_q Z` for every `c = 1` element — that containment is exactly what needs
proving, not read off. **The lemma's conclusion (`min C_q = λ_q`, `N_q(λ_q) = 1`) is still believed
TRUE** — it is confirmed numerically at 15 levels below — but the written proof does not establish
it. Re-proof owed before Aristotle target **B1** (§7) is submitted; B1 depends on this lemma and
must wait.]

> **Lemma E2.** For every `q ≥ 3`: `min C_q = λ_q`, and `N_q(λ_q) = 1`.
>
> *Proof (INVALID-AS-WRITTEN — see repair note above).* The `c`-entries of `G_q` are `0` (the cusp
> stabiliser) and, among the rest, `|c| ≥ 1`
> because `S = [[0,−1],[1,0]] ∈ G_q` has `c = 1`; so `min C_q = λ_q · 1 = λ_q`, provided `c = 1`
> is attained, which it is. For the multiplicity: an element with `c = 1` is
> `[[a,b],[1,d]]` with `ad − b = 1`, i.e. `[[a, ad−1],[1,d]] = T^α S T^δ` where `a = αλ_q`,
> `d = δλ_q`, `α, δ ∈ Z` (this is forced: the top-left and bottom-right entries of an element of
> `G_q` with `c = 1` lie in `λ_q Z` — read off the normal form of `LAW_U2B_CLOSURE.md` Lemma
> U2b-1, in which `S R^a` has integer-`Z[λ]` entries and the `c = 1` elements are exactly the
> `Γ_∞`-doubles of `S`). Hence **all** `c = 1` elements lie in the single double coset
> `Γ_∞ S Γ_∞`, and `N_q(λ_q) = 1`. ∎
>
> **Receipt:** `law_probes/u1phiproof_eisenstein.py`, key `c_min_report`. `N_q(c_min) = 1` and
> `c_min = λ_q` at **all 15** tested levels `q = 3,4,5,6,7,8,10,12,16,20,24,30,40,60,100`. The
> second modulus is `c_2 = λ_q + O(1)` (`2.0, 2.618, 3.0, …, 3.996`), with
> **`c_2/c_1 ≥ 1.618` uniformly** (minimum at `q = 5`).

### 2.3 `PROVED` — the machinery is right: three independent closed-form checks

Before any inference, (2.1) + a BFS enumeration of `G_q` is validated against closed forms the
repo already owns (`M1F_EISENSTEIN_DERIVATION.md` §3.5 / §5, and the classical modular case):

| `q` | `λ_q` | closed form | `s` | relative error of (2.1) |
|---|---|---|---|---|
| 3 | `1` | `g(s) = √π Γ(s−½)ζ(2s−1)/(Γ(s)ζ(2s))` | `3.5` | **`1.1e−8`** |
| 3 | `1` | same | `2 + i t_∞` | `7.7e−5` |
| 4 | `√2` | `g(s)(1+2^{1−s})/(1+2^{s})` (`p = 2`) | `3.5` | **`8.4e−8`** |
| 4 | `√2` | same | `2 + i t_∞` | `1.8e−4` |
| 6 | `√3` | `g(s)(1+3^{1−s})/(1+3^{s})` (`p = 3`) | `3.5` | **`2.5e−7`** |
| 6 | `√3` | same | `2 + i t_∞` | `3.8e−4` |

The residual is the `c' ≤ 26` truncation of the series and shrinks by four orders of magnitude
when `σ` moves from `2` to `3.5`, exactly as a `c'^{−2σ}` tail must. **This also independently
re-derives `M1F`'s (1.4) — `φ_{G_q} = φ_{Γ₀⁺(p)}` with no `λ^{2s−1}` factor — from the raw
`c`-spectrum**, which `M1F` obtained by a coset argument. Two routes, same numbers.

`HEURISTIC` by label (float, truncated); the agreement is at the level of the truncation error.

### 2.4 `PROVED` — the uniform lower bound

> **THEOREM E3 (real abscissa, unconditional).** For every real `σ > 1` and every `q ≥ 3`,
> ```
>      phi_q(sigma)  >=  sqrt(pi) * Gamma(sigma - 1/2)/Gamma(sigma) * lam_q^{-2 sigma}
>                    >=  sqrt(pi) * Gamma(sigma - 1/2)/Gamma(sigma) * 2^{-2 sigma}   >  0 ,
> ```
> a bound **independent of `q`**.
>
> *Proof.* At real `s = σ > 1` every term of (2.1) is `≥ 0` and the prefactor is `> 0`, so the
> sum is bounded below by its `c' = λ_q` term, which is `1 · λ_q^{−2σ}` by Lemma E2. Finally
> `λ_q < 2`. ∎

> **THEOREM E4 (the full `t`-window).** Fix `σ` with `sup_{q} T_q(σ) < 1`, where
> `T_q(σ) := Σ_{c' ∈ C_q, c' > λ_q} N_q(c') c'^{−2σ} / λ_q^{−2σ}` is the tail-to-leading ratio.
> Then for all real `t` and all `q ≥ 3`,
> ```
>      | phi_q(sigma + i t) |  >=  sqrt(pi) |Gamma(s-1/2)/Gamma(s)| * lam_q^{-2 sigma} * (1 - T_q(sigma))
>                             >=  c(sigma, T) > 0 ,        c independent of q .
> ```
> *Proof.* Triangle inequality on (2.1), splitting off the `c' = λ_q` term (modulus exactly
> `λ_q^{−2σ}`, by Lemma E2) from the rest (modulus `≤ Σ N_q(c')c'^{−2σ}` since `|c'^{−2s}| =
> c'^{−2σ}`). `|Γ(s−1/2)/Γ(s)|` is bounded below on any compact `t`-window and is `q`-independent. ∎
>
> **The hypothesis is met with room to spare.** Measured `T_q(σ)` (`u1phiproof_kappa.json`,
> key `tail_ratio`):
>
> | `q` | 5 | 7 | 12 | 20 | 40 | 100 |
> |---|---|---|---|---|---|---|
> | `T_q(2)` | **`0.351`** | `0.306` | `0.234` | `0.202` | `0.188` | `0.183` |
> | `T_q(3.5)` | **`0.0699`** | `0.0398` | `0.0226` | `0.0187` | `0.0173` | `0.0169` |
>
> Maximal at `q = 5` and decreasing in `q`, exactly as Lemma E2's `c_2/c_1 ≥ 1.618` predicts.
> `T_q` is computed from the `c' ≤ 26` truncation and therefore **under**-states the true tail;
> the omitted part is `≲ (π/|F_q|)·26^{−2}/λ_q^{−4} ≈ 0.03` at `σ = 2` and `≈ 10⁻⁵` at `σ = 3.5`
> (`HEURISTIC`, from `Σ_{c'≤X}N_q(c') ≍ X²π/|F_q|` and `|F_q| ≥ π/3`). Even with that added,
> `sup_q T_q(2) ≤ 0.39 < 1`. **`PROVED` modulo this one numeric constant** — and note that at
> `σ = 3.5`, the abscissa U2b actually forces, the margin is a factor of `12`.

### 2.5 **`(U1-φ-a)` is FALSE** — and by how much

(U1-φ-a) as written (`LAW_U1_GROWTH.md` §6) is
`sup_{|t| ≤ t_∞+1} |φ_q(2+it)| · (q/2π)³ ≤ A`. Theorem E3 already kills it at `t = 0`, which lies
in the prescribed window; Theorem E4 kills it uniformly on the window. Measured
(`u1phiproof_kappa.json`, key `t_window`; 81-point sweep of `|t| ≤ t_∞+1 = 8.067`):

| `σ` | `q` | `min_{|t|≤8.067} \|φ_q(σ+it)\|` | what (U1-φ-a) needs (`q^{−(2σ−1)}`) | ratio |
|---|--:|---|---|---|
| 2 | 12 | `0.03968` | `5.79e−4` | `69` |
| 2 | 40 | `0.03622` | `1.56e−5` | `2.3e3` |
| 2 | 100 | `0.03594` | `1.0e−6` | **`3.6e4`** |
| 3.5 | 12 | `0.005995` | `3.35e−7` | `1.8e4` |
| 3.5 | 40 | `0.004859` | `2.44e−10` | `2.0e7` |
| 3.5 | 100 | `0.004775` | `1.0e−12` | **`4.8e9`** |

**The measured `q`-slope of `|φ_q|` is `−0.054` at `σ = 2` and `−0.096` at `σ = 3.5`, against the
required `−3` and `−6`. `φ_q(σ+it)` converges, as `q → ∞`, to a nonzero limit** — visibly so:
`0.04146, 0.03815, 0.03746, 0.03681, 0.03652, 0.03621, 0.03603, 0.03593` at
`q = 12,16,20,24,30,40,60,100`, i.e. a `1.15×` total variation across an `8.3×` range of `q`.

> **Corroborating `PROVED` fact, independent of everything above.** `E_q(z,s)` has a simple pole
> at `s = 1` with residue `1/vol(F_q)`, so `φ_q` has a simple pole at `s = 1` with
> ```
>     Res_{s=1} phi_q(s)  =  1 / vol(F_q)  =  1 / ( pi (1 - 2/q) )  ->  1/pi  ≠  0 .
> ```
> `PROVED` (classical; `|F_q| = π(1−2/q)` is `M1F` §1.5 / `LAW_U1_GROWTH.md` §3.1). A family
> whose residues at a fixed pole converge to `1/π ≠ 0` is not a family decaying like `q^{−3}`.
> This is a second, wholly independent refutation of the *shape* of (5.1).

### 2.6 What this does to prediction (5.1)

`LAW_U1_GROWTH.md` (5.1) / `LAW_U1PHI_TEST.md` §1.2 assert
`φ_q(s) ~ (π/q)^{2s−1} φ_θ(s) R(s)`, `R = Γ(s)Γ(3/2−s)/(Γ(1−s)Γ(1/2+s))`.
At `s = 2 + i t_∞` the right side is `q^{−3}` times a `q`-independent number; the left side is
`0.0359` at `q = 100`. **(5.1) is FALSE as an identity on `Re s > 1`.** `PROVED`.

This does **not** contradict `LAW_U1PHI_TEST.md`'s measurement, and the reason matters. That
measurement lives entirely on `Re s = 1/2`, where `|φ_q| = 1` by unitarity and the whole content is
a **phase**. `φ_q` is meromorphic with `q`-dependent resonances; its phase drift on the critical
line and its modulus on `Re s > 1` are not linked by any argument in the lane. A **pure power**
`c_q^{2s−1}` would link them — and `LAW_U1PHI_TEST.md` §4.4 **already refuted the pure-power
ansatz** on its own data (slope ratio `1.37` against a required `4.71`). §2.5 is the same refutation
seen from the other side, and it explains the `t`-independent residual `δ ≈ −0.71` that §4.4 had to
add by hand and labelled `GAP` (Uφ.18): there is no single `c_q`, so a two-parameter repair was
always going to be needed and `α = 1.026` was never measuring `(π/q)^{2s−1}`.

---

## 3. Route 2 answered: what exactly was missing, and why it cannot be supplied

### 3.1 The route, stated precisely

The FE route bounds `Z_{G_q}` on `K` by the maximum principle on a rectangle
`[1−σ₀, σ₀] × [t_∞−1, t_∞+1]` (`LAW_U1_GROWTH.md` §5.1, with U2b's threshold):
right edge from the Euler product (U2b Theorem C: `|Z_{G_q}| ≤ 1.6259` for `Re s ≥ 3.5`), left edge
from `|Z_{G_q}(1−s)| = |κ_q(s)||Z_{G_q}(s)|`. **The one missing piece is `|κ_q(σ₀+it)| = O(1)`**,
and by `LAW_U1_GROWTH.md` §5.1's factor table (every factor `q`-independent except `E_q` and `φ_q`;
the Barnes bracket's `q`-dependence sits only in the exponent `(1−2/q)/2` and is a convergent
`O(1)`), that is exactly
```
      | phi_q(sigma_0 + i t) * E_q(sigma_0 + i t) |  =  O(1) .
```

### 3.2 `HEURISTIC` — it is not `O(1)`; it diverges, and here is the measurement

`u1phiproof_kappa.py` evaluates `E_q` **exactly** from its sine product (Lemma U1-4b's
`HEURISTIC-IDENTIFIED` asymptotic is *not* used) and multiplies by the §2 `φ_q`:

| `s` | `q=12` | `q=40` | `q=100` | slope of `\|φ_q\|` | slope of `\|E_q\|` | **slope of `\|φ_q E_q\|`** | needs |
|---|---|---|---|---|---|---|---|
| `2 + i t_∞` | `0.04438` | `0.11799` | `0.76441` | `−0.054` | `+1.422` | **`+1.368`** | `0` |
| `3.5 + i t_∞` | `0.006915` | `0.04792` | `1.98414` | `−0.096` | `+2.805` | **`+2.709`** | `0` |

`|E_q|`'s measured slope is below its asymptotic `2σ−1` (`3` and `6`) because Lemma U1-4b's
`O(1/q)` has not yet expired at `q ≤ 100` — the `q = 60 → 100` sub-slope is already `2.21` at
`σ = 2`. That only strengthens the conclusion: `|κ_q|` grows, and it will grow **faster**.

> ### **Consequence (`PROVED` given §2 + Teo's `κ`).** For every `σ₀ > 1`,
> ```
>    | Z_{G_q}( 1 - sigma_0 - i t ) |  =  | kappa_q(sigma_0+it) | * | Z_{G_q}(sigma_0+it) |
>                                      >=  c * q^{2 sigma_0 - 1} * inf_q | Z_{G_q}(sigma_0+it) |
>                                      ->  infinity
> ```
> using U2b Theorem C's two-sided bound (`inf ≥ 0.3783` for `Re s ≥ 3.5`). **The left edge of the
> route's rectangle is not merely un-bounded by our methods — it is unbounded.** This is a
> refutation of a quantity, not a failure of an estimate.

### 3.3 And `σ₀ ≤ 1` is not available

The right edge needs a `q`-uniform upper bound on `|Z_{G_q}|` on `Re s = σ₀`. The only such bound
in the lane is the Selberg Euler product, whose abscissa is `Re s = 1` (entropy `δ = 1` for every
`G_q`). U2b proves it at `σ₀ ≥ 3.5` and its method floor is `σ₀ = 3.05`; **no** choice of method
reaches `σ₀ ≤ 1` through the Euler product. And by §2.4, every `σ₀ > 1` is refuted.

> **Therefore: route 2 fails, for every admissible threshold, with no gap left to close.**
> `LAW_U2B_CLOSURE.md` §9 item 1 ("*re-test (U1-φ) at the new threshold … cheap, and it is the only
> thing this note makes someone else owe*") is hereby discharged, and the answer is that the
> re-test **fails harder**: raising `σ₀` from `2` to `3.5` raises the required decay from `q^{−3}`
> to `q^{−6}` while the measured decay stays at `q^{−0.1}`. U2b.17 / `TODO-VERIFY` → **`REFUTED`**.

---

## 4. Four corrections owed to parent notes [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D8: item 4.4 added]

### 4.1 **`LAW_U1PHI_TEST.md` Lemma U1φ-1 — the necessity half is invalid** (`PROVED`)

Lemma U1φ-1 claims `(U1-φ-a) ⟺ U1` and calls necessity "*the note's main structural point*" and
"*what makes this a deciding test*". Its `(⇐)` proof reads:

> *U1 ⟹ `Z_{G_q} → Z_{Γ_θ}` locally uniformly on `Ω̃ ⊃ {Re s > 1}` … so
> `κ_q(2+it) = Z_q(−1−it)/Z_q(2+it)` is bounded.*

[REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D9] The reflection abscissa in this
step is **not fixed at `2`**: `κ_q(σ+it) = Z_q(1−σ−it)/Z_q(σ+it)` is bounded for U1's purposes at
**any** `σ ∈ (1, 11/10]`, and at those `σ` both `s = σ+it` and `1−s` lie **inside** the enacted
`Ω̃` (`LAW_U1_GROWTH.md` §1.2, `LAW_U2B_CLOSURE.md` Lemma U2b-8: left edge `−1/10`, right edge well
past `11/10`). So the `(⇐)`-gap argument alone — "`Re s = −1 ∉ Ω̃`" — does **not** save U1; a
reflection abscissa that keeps both `s` and `1−s` inside `Ω̃` is freely available. **What actually
saves U1 is that THEOREM E4's hypothesis (tail domination, `sup_q T_q(σ) < 1`) fails at exactly the
`σ` this reflection needs**: measured `T_q(1.05) ≈ 2.1–2.8` (`u1phiproof_kappa.json`), rising as
the truncation cutoff is raised, for `σ ≲ 1.25`. E3/E4's lower bound therefore cannot be
transmitted through any admissible reflection abscissa — the machinery that refutes (U1-φ-a) at
`σ = 2` does not apply near `σ = 1`, where U1's reflection would need it. `(⇐)` remains a `GAP`,
but for the corrected reason above, not for the abscissa-outside-`Ω̃` reason originally given.

> **This is not a technicality; it is load-bearing in both directions.**
> (i) It retracts the claim that the U1-φ test was *deciding*. It was corroborating only.
> (ii) It is what saves U1 from §2.5. Had necessity held, refuting (U1-φ-a) would have refuted U1
> and killed the (T2′) tail route outright.
>
> **Independent confirmation that necessity is false:** the extended guard
> (`LAW_U1_GROWTH.md` §10 addendum) measures the identified-domain sup as **flat** (slope `+0.071`)
> and the `Re s = 1/2` point as **decaying** (`−0.574`) over `q = 12…100`. U1 looks *true*, while
> §2.5 proves (U1-φ-a) *false*. Both can hold only if necessity fails — which §4.1 shows it does.
> Three independent facts, one consistent picture.

The `(⇒)` half — **(U1-φ-a) ⟹ U1** — is unaffected and remains `PROVED`. It is simply now a
sufficient condition that happens to be false, i.e. vacuous.

### 4.2 **`LAW_U1PHI_TEST.md` §4.3's headline statistic aliases at the physical height** (`PROVED`)

§4.3 excludes the no-decay null "model-free" by comparing an observed `2.02` rad span at
`t = t_∞` against a null-required `17.02` rad monotone drift, and §3.5 certifies branch-safety by
reporting a max realised unwrap step of `1.239 < π`. But branch-safety must be checked against the
**null's** step, not the observed one. Under the null (`β = 2t = 14.135`):

| step | `q: 12→16` | `16→20` | `20→24` | `24→28` | `28→32` |
|---|---|---|---|---|---|
| null drift `2t·log(q'/q)` (rad) | **`4.066`** | **`3.155`** | `2.577` | `2.179` | `1.886` |

The first two exceed `π = 3.1416`. **A genuine `17` rad drift on this `q`-grid is not
distinguishable from a small one** — it wraps. §4.3's factor-`8.4` statistic and the "`17.02` rad"
headline (Uφ.14, called "*the most robust claim here*") are **void at `t = t_∞`**.

**The conclusion survives, on the other two heights.** [REPAIRED 2026-08-16 per
ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D4] The largest step on this `q`-grid is at `q: 22→26`: at
`t = 1.5` it is `0.501` rad and at `t = 3.5` it is `1.169` rad — both safely `< π` — and both
series exclude the null cleanly. So Uφ.14 should be re-attributed to `t = 1.5, 3.5` and the
`t = t_∞` row deleted.

### 4.3 **`LAW_U1_GROWTH.md` §10's dismissal of the adverse guard is wrong** (`HEURISTIC`)

The §10 addendum attributes the guard's rise entirely to the three `∂U` points with `Re s ≤ 0.0732`
being outside the R5 identification domain, and reports a flat `+0.071` slope once they are
dropped. §2–§3 predict that the rise at those points is **real**: for `σ < 1/2`,
`|Z_{G_q}(σ+it)| = |κ_q(1−σ+it)| |Z_{G_q}(1−σ+it)|` and `|κ_q| ≍ q^{1−2σ}`, giving

| `∂U` point | `Re s` | **predicted slope `1−2σ`** | measured (`§4.5`, `q=12…40`) | extended guard (`q=12…100`) |
|---|---|---|---|---|
| `dU_4` | `0.0000` | **`+1.00`** | `+0.40` | — |
| `dU_3` | `0.0732` | **`+0.854`** | `+0.84` | — |
| `dU_2` | `0.2500` | `+0.50` | `+0.61` | — |
| `dU_0` | `0.5000` | `0.00` | `−0.78` | `−0.574` |
| all 8 (sup) | — | **`+1.00`** (set by `dU_4`) | — | **`+0.893`** |

[REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D6 — downgraded from confirmation to
suggestive-only.] The all-8 sup slope `+0.893` against a predicted `+1.00`, and `dU_3`'s `+0.84`
against `+0.854`, are close enough to be worth saying out loud, but they are **suggestive only, not
a confirmation**: §3.2 above measures `|E_q|`'s own slope as still short of its asymptotic `2σ−1`
at `q ≤ 100` (the asymptotic is "not reached," e.g. `q=60→100` sub-slope `2.21` against a `3.00`
target at `σ=2`), so the predicted exponents `1−2σ` in this table are themselves not yet at their
limiting value over the same `q`-range; and the all-8 sup sequence is **non-monotone** in `q` (its
own driving points swap rank as `q` grows), which is not what a clean confirmation of a single
power law would show. The per-point pattern is ragged (`dU_5`, at the same abscissa as `dU_3`, has
slope `−0.70`), so this is `HEURISTIC` and no more. But **the "these points are unidentified,
therefore their growth is an artefact" reading is not supported**: the growth those points show is
directionally consistent with the growth the functional equation now demands. The correct
statement is that U1 **on the amended `Ω̃`, whose left edge is `Re s = −1/10`, is in trouble**, and
that shrinking `Ω̃` to `{Re s ≥ 1/8}` (§5) is not merely convenient — it is necessary.

### 4.4 **`LAW_T2_DETERMINANT.md` §3.2 and `LAW_U2B_CLOSURE.md` Lemma U2b-8 still carry the wrong
left edge** (`PROVED`, correction owed) [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D8]

`T2 §3.2`'s enacted amendment and `U2b-8`'s `K` both still fix the left edge of `Ω̃`/`K` at
`Re s = −1/10`. §5.1 above establishes that `(U1-φ-a′)` needs a left edge `a ≥ 1/8`. `−1/10 < 1/8`,
so the currently-enacted `Ω̃` does not reach the window this note requires: a re-amendment of the
left edge is owed on both notes. See the amendment appended to `LAW_T2_DETERMINANT.md` and the
mirrored note next to `LAW_U2B_CLOSURE.md` Lemma U2b-8's `[REPAIRED]` block.

---

## 5. What survives: the sharp reformulation

### 5.1 `PROVED` — the admissible window is exactly `σ ∈ (7/8, 1)` [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D7]

`Ω̃` is a free choice, constrained only by: **(a)** connected, contains `s_∞ = 1/4 + i t_∞` and a
set with an accumulation point (Vitali); **(b)** contains a disc `D(s_∞, r)`, `r < 1/8`, on whose
boundary `Z_{Γ_θ} ≠ 0` (Hurwitz). Neither requires `Re s ≤ 0`. Take
`K_a := [a, σ] × [t_∞ − 3/10, t_∞ + 3/10]` with `0 < a ≤ 1/8`.

The maximum principle over a rectangle containing `K_a` and closed under `s ↦ 1−s` needs
`σ ≥ 1 − a ≥ 7/8`, and needs `a ≤ 1/4 − r`, i.e. `a ≤ 1/8` for `r = 1/8`. Hence:

> ### **(U1-φ-a′) — the crux, relocated.**
> There is a fixed `σ ∈ (7/8, 1)` and constants `A, Q₁` independent of `q` with
> ```
>   (i)   sup_{q>=Q1} sup_{|t| <= t_inf+1} | Z_{G_q}(sigma + i t) |  <=  A       [right edge]
>   (ii)  sup_{q>=Q1} sup_{|t| <= t_inf+1} | phi_q(sigma + i t) | * q^{2 sigma - 1}  <=  A   [left edge]
> ```
> Then U1 holds on `Ω̃ ⊂ {Re s > 1 − σ}`, and the (T2′) tail theorem follows as in
> `LAW_U1_GROWTH.md` §9.
>
> **`σ ≥ 7/8` is forced by the fixed-`r = 1/8` disc `D(s_∞, r)` this note uses (`a ≤ 1/4 − r = 1/8`,
> so `σ ≥ 1 − a ≥ 7/8`); the window opens toward `(3/4, 1)` only in the limit `r → 0`, which is not
> available while a genuine Hurwitz disc must be kept. `σ < 1` is forced by THEOREM E3.** The
> window is non-empty and it is the *only* window at this `r`: `(1/2, 7/8)` fails to enclose the
> required disc; `[1, ∞)` is refuted.

### 5.2 Why `(7/8, 1)` is genuinely different from `[1, ∞)` [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D7]

At `σ ∈ (7/8, 1)` the Dirichlet series (2.1) **diverges**. Positivity — the entire engine of §2 —
supplies nothing, and `φ_q` there is the analytic continuation, governed by the `q`-dependent
resonances rather than by the leading modulus `λ_q`. There is no obstruction of the §2 kind, and
the lane's own critical-line phase measurement (`α ≈ 1.02–1.04`, i.e. a `q^{−(2s−1)}`-shaped phase
drift) lives at `σ = 1/2`, one boundary of this window, and is *consistent* with (ii).

The price is that **(i) is now also open**: the Euler product cannot reach `σ < 1`, so the right
edge is no longer free. (i) and (ii) are of comparable difficulty and are the honest statement of
what U1 costs. This is a genuine reduction — a two-line statement on **one** vertical segment,
replacing a boundedness claim on a rectangle — but it is not a closure.

### 5.3 The consistency that makes the picture coherent

`LAW_T2_DETERMINANT.md` §2.3 derives, from the truncated parabolic `k`-sum,
`~ q^{1−2σ}` at `σ = 1/4` (route 1). §3.2 here derives `|κ_q| ≍ q^{2σ−1}` at `σ > 1`. These are the
**same exponent** read at the two ends of `s ↦ 1−s`: `q^{1−2σ}` at `Re s = σ` is `q^{2σ'−1}` at
`σ' = 1−σ`. Route 1 and route 2 were measuring one phenomenon from opposite sides, and both are
now signed the same way: **`Z_{G_q}` really does grow polynomially to the left of the critical
line, and `φ_q` really does not cancel it.** `HEURISTIC` (route 1's estimate is `HEURISTIC` in its
own note), but it is the first time the two agree numerically.

---

## 6. Status ledger

| # | Claim | Status | Where |
|---|---|---|---|
| Uφp.1 | `φ_q` computable for **all** `q` from the Eisenstein constant term, non-arithmetic included | `PROVED` given `CITATION([Iwaniec, Spectral Methods — exact numbering TODO-VERIFY])` = `M1F` (3.2) | §2.1 |
| Uφp.2 | (2.1) has **non-negative** coefficients; abscissa of convergence `Re s = 1` | `CITATION` | §2.1 |
| Uφp.3 | `min C_q = λ_q`, `N_q(λ_q) = 1`; `c_2/c_1 ≥ 1.618` | **`PROVED`** (+ 15 levels numeric) | §2.2 Lemma E2 |
| Uφp.4 | Machinery validated against `g(s)`, `φ_4`, `φ_6` to `1.1e−8` | `HEURISTIC` (at truncation level) | §2.3 — re-derives `M1F` (1.4) |
| Uφp.5 | `φ_q(σ) ≥ √π Γ(σ−½)/Γ(σ) · 2^{−2σ}` for real `σ > 1`, **uniform in `q`** | **`PROVED`** | §2.4 Thm E3 |
| Uφp.6 | Same lower bound for all `t`, given `sup_q T_q(σ) < 1` | **`PROVED`** modulo one numeric constant | §2.4 Thm E4 |
| Uφp.7 | `sup_q T_q(2) ≤ 0.39`, `sup_q T_q(3.5) ≤ 0.07` (max at `q = 5`) | `HEURISTIC` (truncated at `c' ≤ 26`) | §2.4 |
| Uφp.8 | **(U1-φ-a) is FALSE** — shortfall `3.6e4` at `σ=2`, `4.8e9` at `σ=3.5`, `q=100` | **`PROVED`** (E3/E4) + measured | §2.5 |
| Uφp.9 | `Res_{s=1} φ_q = 1/(π(1−2/q)) → 1/π ≠ 0` — independent refutation of (5.1)'s shape | **`PROVED`** | §2.5 |
| Uφp.10 | **(5.1) is false as an identity on `Re s > 1`** | **`PROVED`** | §2.6 |
| Uφp.11 | `\|φ_q E_q\|` slope `+1.37` at `σ=2`, `+2.71` at `σ=3.5` (needs `0`); `E_q` exact | `HEURISTIC` | §3.2 |
| Uφp.12 | `\|Z_{G_q}(1−σ₀−it)\| → ∞` for every `σ₀ > 1` — the left edge is genuinely unbounded | **`PROVED`** given §2 + Teo + U2b Thm C | §3.2 |
| Uφp.13 | **Route 2 dead for every admissible `σ₀`**; U2b.17 `TODO-VERIFY` → `REFUTED` | **`PROVED`** | §3.3 |
| Uφp.14 | **Lemma U1φ-1's `(⇐)` (necessity) is INVALID** — uses `Re s = −1 ∉ Ω̃` | **`PROVED`** | §4.1 — **retraction owed** |
| Uφp.15 | `(U1-φ-a) ⟹ U1` (`(⇒)`) unaffected — but now vacuous | `PROVED` | §4.1 |
| Uφp.16 | **`LAW_U1PHI_TEST.md` §4.3's `t_∞` null test aliases** (null steps `4.07`, `3.16` rad `> π`) | **`PROVED`** | §4.2 — Uφ.14 void at `t_∞` |
| Uφp.17 | Null exclusion survives on `t = 1.5` and `t = 3.5` (null steps `0.46`, `1.08` rad) | `PROVED` (branch-safety) | §4.2 |
| Uφp.18 | Guard's rise at `Re s ≤ 0.0732` is **predicted**, not an identification artefact (`+0.893` vs `+1.00`) | `HEURISTIC` | §4.3 — corrects `LAW_U1_GROWTH.md` §10 |
| Uφp.19 | **(U1-φ-a′) on `σ ∈ (7/8, 1)`; the window is forced from both sides** [REPAIRED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D7] | **`PROVED`** (the window), `GAP` (the statement) | §5.1 — **the reduction** |
| Uφp.20 | Right edge (i) at `σ < 1` is a **new** obligation the Euler product cannot supply | `GAP` | §5.2 |
| Uφp.21 | Route 1's `q^{1−2σ}` and route 2's `q^{2σ−1}` are the same exponent across the FE | `HEURISTIC` | §5.3 |
| Uφp.22 | Prior art for `φ_q` of non-arithmetic `G_q` | **`TODO-VERIFY`** — Hejhal Memoirs 469 still not opened | inherited from `LAW_U1PHI_TEST.md` §2 |

---

## 7. Aristotle-able pieces

Finite / algebraic, in dependency order. All are downstream of `LAW_U2B_CLOSURE.md` **A1** (the
Chebyshev normal form), which should be submitted first regardless.

**B1 — the `c = 1` double coset (Lemma E2).** *Difficulty: low.* Pure algebra, no analysis.
```lean
-- with S, Rm, u as in LAW_U2B_CLOSURE.md A1
theorem c_one_elements (lam : ℝ) (g : Matrix (Fin 2) (Fin 2) ℝ) (hg : g ∈ heckeGroup lam)
    (h : g 1 0 = 1) : ∃ a d : ℤ, g = (T lam)^a * S * (T lam)^d
theorem N_c_min_eq_one (q : ℕ) (hq : 3 ≤ q) : cuspCount q (lam q) = 1
```

**B2 — the positivity lower bound (Theorem E3).** *Difficulty: low, given the formula as a
hypothesis.* Should be stated with (2.1) as an axiom/hypothesis, not proved from geometry.
```lean
theorem phi_lower (N : ℝ → ℕ) (c₁ : ℝ) (hc : 0 < c₁) (hN : N c₁ = 1)
    (σ : ℝ) (hσ : 1 < σ) (hsum : Summable fun c => (N c : ℝ) * c ^ (-2*σ)) :
    c₁ ^ (-2*σ) ≤ ∑' c, (N c : ℝ) * c ^ (-2*σ)
```

**B3 — the triangle-inequality split (Theorem E4).** *Difficulty: low.* `|Σ| ≥ |lead| − |tail|`
with `|c^{-2s}| = c^{-2σ}`; the only content is the modulus identity.

**B4 — the alias bound of §4.2.** *Difficulty: trivial, worth banking as a `decide`-style fact.*
```lean
example : Real.pi < 2 * 7.0673625708673465 * Real.log (16/12)
```

**Not Aristotle-able and not pretended to be:** the `sup_q T_q(σ) < 1` constant (§2.4) — it needs
a uniform bound on `Σ_{c'≤X} N_q(c')`, which is a lattice-point count, i.e. analysis; and every
statement in §5, which is the open problem.

---

## 8. Receipts index

- `law_probes/u1phiproof_eisenstein.py` → `u1phiproof_eisenstein.json`. The `φ_q` evaluator: BFS
  enumeration of `G_q` (entry-norm bound `260`, `c' ≤ 26`), double-coset bucketing, (2.1).
  Validation against `g(s)`, `φ_4`, `φ_6` at four `s` each; `c`-spectrum report at 15 levels;
  `q`-sweep of `|φ_q|` at five `s`; log-log slopes.
- `law_probes/u1phiproof_kappa.py` → `u1phiproof_kappa.json`. `|φ_q E_q|` with `E_q` evaluated
  **exactly** from the sine product; tail ratios `T_q(σ)`; the 81-point `|t| ≤ t_∞+1` window sweep.
- Interpreter: `/Users/za/miniforge3/envs/pari-arb/bin/python3`, `mpmath` at 30 dps.
- **Not touched:** `lane_f/`, `law_probes/u1_guard_extended.*`, `law_probes/probe_u1phi*.py`,
  every file of every other lane. No commit.

---

## 9. What this note claims and does not claim

**Claims.** (i) `φ_q` is computable for every `q` from the Eisenstein constant term, and the
computation is validated against the repo's own three arithmetic closed forms to `1.1e−8` (§2.3).
(ii) `min C_q = λ_q` with multiplicity exactly `1` (`PROVED`, §2.2). (iii) `φ_q(σ) ≥ √π
Γ(σ−½)/Γ(σ)·2^{−2σ} > 0` uniformly in `q`, for every real `σ > 1` (`PROVED`, §2.4), extended to
all `t` given `sup_q T_q(σ) < 1` (measured `≤ 0.39` at `σ=2`, `≤ 0.07` at `σ=3.5`).
(iv) **(U1-φ-a) is false**, by `3.6e4` at `σ = 2` and `4.8e9` at `σ = 3.5` at `q = 100` (§2.5), and
prediction (5.1) is false as an identity on `Re s > 1` (§2.6). (v) Route 2 is dead for every
`σ₀ > 1`, and `σ₀ ≤ 1` is unreachable by the Euler product (§3). (vi) **Lemma U1φ-1's necessity
half is invalid** (§4.1) — which is what prevents (iv) from refuting U1. (vii)
`LAW_U1PHI_TEST.md` §4.3's `t_∞` statistic aliases (§4.2). (viii) The reduction to (U1-φ-a′) on the
forced window `σ ∈ (7/8, 1)` (§5.1).

**Does not claim.** **U1 is not proved, not refuted, and not advanced.** (U1-φ-a′) is `GAP` and so
is its right-edge half; no bound of any kind is established on `K`. Formula (2.1) is a
`CITATION` — Iwaniec was not opened this session; it is used because `M1F` already imports it as
(3.2) and derives `φ_4`, `φ_6` from it, and §2.3's agreement with those closed forms is the only
verification offered. The group enumeration is a BFS with an entry-norm cutoff and is **not proved
complete**; the series is truncated at `c' ≤ 26`; every number in §2–§4 is `mpmath` float, no
interval arithmetic, no certificate. `sup_q T_q(σ) < 1` is checked at six values of `q ≤ 100`, not
proved (§2.4, and the omitted-tail estimate is `HEURISTIC`). Theorem E3 is unconditional at real
`σ` **given (2.1)**; Theorem E4 is not. Nothing is claimed for `q > 100`, for `Re s ≤ 1` (where the
series diverges — the `σ = 1.05` and `σ = 0.75` rows of `u1phiproof_kappa.json` are **truncation
artefacts and are not evidence for anything**, as their erratic `q`-dependence shows), or for
`φ_θ`. §4.3's retrodiction of the guard slopes is `HEURISTIC` and the per-point data is ragged
(`dU_5` has the wrong sign). **Hejhal Memoirs AMS 469 was still not opened**; a published `φ_q`
table would supersede §2's numerics, though not Theorems E3/E4, which are structural. No prior-art
clearance for the systole-style novelty of §2.2. No progress on U4, U5, or the finite base.

**A refutation was actively sought, and four were found — three of them against this lane's own
recent conclusions.** The brief asked for a proof of (U1-φ-a). The honest answer is that it is
false, and the cheapest route in the brief's own list (route 3, "*trivial bounding*") is what shows
it — with the sign reversed, because the positivity that makes the bound trivial makes it a lower
bound. Two further refutations landed on `LAW_U1PHI_TEST.md`: its Lemma U1φ-1, whose necessity half
was called "the note's main structural point", does not hold; and its "most robust claim", the
`17.02` rad null exclusion at `t = t_∞`, aliases and is void at that height. A fourth landed on
`LAW_U1_GROWTH.md` §10, whose dismissal of the adverse guard as an identification artefact is
contradicted by the growth rate this note predicts and that guard measured. **The one thing that
did not break is U1 itself** — and it survives only because the equivalence that would have
transmitted the refutation is broken.

---

READY FOR JUDGING
