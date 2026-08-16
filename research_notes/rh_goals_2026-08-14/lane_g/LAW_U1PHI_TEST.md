# LAW (U1-φ) — the prediction test for the scattering determinant

**Date:** 2026-08-16. **Lane G.** Obligation **(U1-φ-a)** of `lane_g/LAW_U1_GROWTH.md` §6,
i.e. the falsifiable prediction (5.1) of that note. This is the **second deciding test** for the
LAW tail, independent of the running sup-guard extension.

**Parents read in full:** `lane_g/LAW_U1_GROWTH.md` (§3.1 the `κ_q` assembly, §3.3 Lemma U1-4b,
§5.1 the prediction (5.1), §6 the obligation, §7 the guard), `lane_g/LAW_U3_TRANSPORT.md`
(§2.5 Teo's functional equation verbatim, §2.6 the divisor argument),
`lane_g/LAW_ANCHOR_T1_THETA.md` (the `det Φ_θ = g² E` closed form).

**Status convention (identical to T1 / T2 / U1 / U3):** `PROVED` = derived here in closed form or
verified in exact/symbolic arithmetic. `CITATION` = imported, import named and read.
`TODO-VERIFY` = a specific check owed against a named source that was **not opened**.
`HEURISTIC` = float evidence or a plausibility argument, explicitly not a proof.
`GAP` = not justified; the missing statement is written out.

**No certificate is produced. Nothing is committed. `lane_f` is untouched.
`law_probes/u1_guard_extended.*` was not read or written.**

---

## 0. Verdict up front

> ### **VERDICT: PREDICTION-CONSISTENT.** The fitted exponent is **`−3.08`** against the
> ### prediction **`−3`** and the no-decay null **`0`**. `|φ_q(2+it)| ≍ q^{−3}` survives its
> ### first real test.
>
> | estimator | `α` | **exponent `−3α`** | prediction | null |
> |---|---|---|---|---|
> | two-height decomposition, LSQ slopes | `1.0261` | **`−3.078`** | `−3` | `0` |
> | two-height decomposition, endpoint slopes | `1.0234` | **`−3.070`** | `−3` | `0` |
>
> Two independent estimators agree to `0.008`. **The null is excluded model-free**: at the physical
> height it demands a **monotone `17.02` rad** drift of the scattering phase over `q = 12 → 40`;
> the measured total span is **`2.02` rad and non-monotone** — a factor `8.4` too small, with the
> wrong shape.

Five things are settled here, four of them new.

1. **(5.1) is re-derived independently and confirmed exactly**, `π` and all, by comparing Teo's
   `κ` for signature `(0;1;2,q)` against `(0;2;2)` (§1.2, `PROVED` given Teo + Lemma U1-4b). The
   parent note's formula carries no transcription error.
2. **`(U1-φ-a) ⟺ U1` — the implication runs BOTH ways** (Lemma U1φ-1, §1.4, `PROVED`).
   `LAW_U1_GROWTH.md` §6 recorded only sufficiency. Necessity is new, and it is what makes this a
   *deciding* test rather than a corroborating one: a refutation would have killed U1 outright.
3. **The Γ-skeleton of (5.1) is exactly unitarity-compatible** — `R(s)R(1−s) = 1` identically
   (§1.3, `PROVED`, verified to `1.1e−42`). This is the provable-today half of the prediction, and
   it was assembled from two independent bookkeeping sources that had no reason to agree.
4. **The pure-power ansatz alone is REFUTED, and its repair is what yields `−3.08`.** (5.1) taken
   literally demands `β(t) ∝ t`, i.e. a slope ratio `4.7116` between the two heights; the measured
   ratio is `1.37`. The slopes are instead **nearly equal** (`−0.788`, `−1.078`), the signature of
   a **`t`-independent** additive drift `δ ≈ −0.71` sitting on top of the `(2s−1)`-power. Fitting
   `β(t) = 2t(1−α) + δ` — two heights, two unknowns — returns `α = 1.026`, i.e. the `(π/q)^{2s−1}`
   scaling is right to `2.6%` and the leftover is a nuisance phase that (5.1) simply does not
   model. §4.3.
5. **The guard's adverse rise is localized, and this note locates it.** Re-reading
   `u1_sup.json`/`u1_sup_q40.json` **per point** (§4.5, not done before): of the eight `∂U` points,
   **five decrease** in `q` and the rise is confined to `Re s ≤ 0.0732` — i.e. to exactly the two
   points sitting on or beside `∂Ω*`, where the determinant has no identification guarantee. At
   `Re s = 1/2`, inside the safe domain, `|Z_q|` **falls** with log-log slope `−0.78`.
   `LAW_U1_GROWTH.md` §7.3's `+1.50` is a statement about the *maximum over a set two of whose
   members are out-of-domain*, not about a quantity that is uniformly trustworthy.

**Headline: U1-φ-a SURVIVES; the exponent is `−3.08` against a predicted `−3`; and the guard's
adverse reading is materially weakened. The (T2′) tail route is no longer "at risk" on the
evidence available — but it is not corroborated either, because §4.4's fits are model-dependent
and everything here is float on an unidentified proxy.**

---

## 1. What is being tested, and why it is worth a session

### 1.1 The prediction

`LAW_U1_GROWTH.md` (5.1):

```
   phi_q(s)  ~  (pi/q)^{2s-1} · phi_theta(s) · Gamma(s) Gamma(3/2-s)
                                             / ( Gamma(1-s) Gamma(1/2+s) )      (5.1)
```

whose modulus consequence at `Re s = 2` is the obligation **(U1-φ-a)**:
`|φ_q(2+it)| = O(q^{−3})`.

### 1.2 `PROVED` — (5.1) is not a guess: it is the *unique* consequence of `κ_q → κ_θ`

Re-derived here independently of the parent note, from Teo's Prop. 2.5
(`CITATION(Teo, arXiv:1901.07898v2, Prop. 2.5)`, quoted verbatim in `LAW_U3_TRANSPORT.md` §2.5)
applied to **both** signatures:

| | `G_q` | `Γ_θ` |
|---|---|---|
| type `(g; n; m_1,…,m_v)` | `(0; 1; 2, q)` | `(0; 2; 2)` |
| `e^{C(2s−1)}`, `C = −n log 2` | `2^{−(2s−1)}` | `2^{−2(2s−1)}` |
| elliptic `∏_j∏_k sin(π(s+k)/m_j)^{(m_j−2k−1)/m_j}` | `tan(πs/2)^{1/2} · E_q(s)` | `tan(πs/2)^{1/2}` |
| Barnes bracket exponent `|X|/2π` | `(1 − 2/q)/2` | `1/2` |
| parabolic `[Γ(3/2−s)/Γ(s+1/2)]^n` | `n = 1` | `n = 2` |

Write `P(s) := Γ(3/2−s)/Γ(s+1/2)` and `B(s)` for the Barnes bracket. Then

```
   kappa_q = ± · 2^{-(2s-1)} · phi_q · tan(pi s/2)^{1/2} · E_q · B^{(1-2/q)/2} · P
   kappa_θ = ± · 2^{-2(2s-1)} · phi_θ · tan(pi s/2)^{1/2} ·        B^{1/2}     · P^2
```

The `tan` factors are identical and cancel; `B^{(1−2/q)/2} → B^{1/2}`. Imposing
`κ_q → κ_θ` and solving for `φ_q`:

```
   phi_q(s) · E_q(s)  ->  phi_theta(s) · 2^{-(2s-1)} · P(s) .                    (1.1)
```

Substituting Lemma U1-4b, `E_q(s) = (q/2π)^{2s−1} · Γ(1−s)/Γ(s) · (1 + O(1/q))`:

```
   phi_q(s) ~ (2pi/q)^{2s-1} · 2^{-(2s-1)} · phi_theta · Gamma(s)/Gamma(1-s) · Gamma(3/2-s)/Gamma(s+1/2)
            = (pi/q)^{2s-1} · phi_theta(s) · Gamma(s)Gamma(3/2-s) / ( Gamma(1-s)Gamma(1/2+s) ) .
```

**This reproduces (5.1) exactly, including the `π` (which is `2π/2`: the `2π` from `E_q`'s
asymptotic, the `2` from the cusp-count difference `C = −n log 2`, `n = 1` vs `n = 2`).**
`PROVED` given `CITATION(Teo Prop. 2.5)` + Lemma U1-4b (`HEURISTIC-IDENTIFIED`).
The parent note's formula is independently confirmed; no transcription error.

### 1.3 `PROVED` — the Γ-skeleton is exactly unitarity-compatible

Put `R(s) := Γ(s)Γ(3/2−s)/(Γ(1−s)Γ(1/2+s))`, the skeleton of (5.1). Any prediction of the form
`φ_q = c_q^{2s−1} φ_θ(s) R(s)` must respect `φ(s)φ(1−s) = 1` (`CITATION(FJS (2.6))`, and `PROVED`
for `Γ_θ` as T1 C8). Since `c_q^{2s−1} c_q^{1−2s} = 1` and `φ_θ(s)φ_θ(1−s) = 1`, this forces
`R(s)R(1−s) = 1`. **It holds identically:**

```
   R(s) R(1-s) = [Gamma(s)Gamma(3/2-s)] / [Gamma(1-s)Gamma(1/2+s)]
               · [Gamma(1-s)Gamma(1/2+s)] / [Gamma(s)Gamma(3/2-s)]  =  1 .
```

`PROVED` (the two brackets are literally exchanged under `s ↦ 1−s`), and verified numerically to
`≤ 1.1e−42` at `s = 0.3+2.1i, 0.5+1.5i, 0.5+7.0674i, 2+3i` (mpmath, 40 dps).
Consequently `|R(1/2+it)| = 1` (verified to full precision), as unitarity demands.

**Why this matters.** The Γ-skeleton was assembled from two independent bookkeeping sources — the
`Γ(1−s)/Γ(s)` of the collapsing order-`q` cone point (Lemma U1-4b) and the parabolic count going
`n = 1 → n = 2` — and it lands on exactly the unique shape compatible with the scattering
functional equation. That is a real check on the assembly, and it is the **provable-today** half of
the prediction.

### 1.4 Which piece is provable today, and which is not

| piece of (5.1) | status |
|---|---|
| the **Γ-factor skeleton** `Γ(s)Γ(3/2−s)/(Γ(1−s)Γ(1/2+s))` | `PROVED` given Teo + U1-4b (§1.2), **and** independently forced by unitarity (§1.3). Modulo the Euler–Maclaurin remainder of U1-4b — small, Aristotle-able, already logged as U1.12. |
| the **`(π/q)^{2s−1}` scaling** | **NOT independently provable.** §1.2 derives it *from* `κ_q → κ_θ`, which is U1's own conclusion. |
| **`|φ_q(2+it)| = O(q^{−3})`** | `GAP`. This is (U1-φ-a). |

> ### **Lemma U1φ-1 (`PROVED`, and it is the note's main structural point).**
> Given Teo Prop. 2.5 and Lemma U1-4b, **(U1-φ-a) ⟺ U1**, on the fixed height range
> `|t| ≤ t_∞ + 1`. Not merely sufficient — **necessary**.
>
> *Proof.* (⇐) U1 ⟹ (by Vitali, `LAW_U1_GROWTH.md` §9) `Z_{G_q} → Z_{Γ_θ}` locally uniformly on
> `Ω̃ ⊃ {Re s > 1}`, and `Z_{Γ_θ} ≠ 0` there, so `κ_q(2+it) = Z_q(−1−it)/Z_q(2+it)` is bounded;
> every factor of `κ_q` other than `φ_q E_q` is `O(1)` (`LAW_U1_GROWTH.md` §5.1 table, `PROVED`
> row by row), so `|φ_q E_q| = O(1)`, and `|E_q(2+it)| ≍ (q/2π)³` gives `|φ_q(2+it)| = O(q^{−3})`.
> (⇒) (U1-φ-a) ⟹ `|κ_q(2+it)| = O(1)` by the same table ⟹
> `sup_{Re s = −1}|Z_{G_q}| ≤ sup|κ_q| · sup_{Re s = 2}|Z_{G_q}| = O(1)`, using
> `LAW_U1_GROWTH.md` (2.1) on the right edge. Two bounded vertical edges plus the bounded
> horizontal edges of the rectangle `[−1,2] × [t_∞−1, t_∞+1]` give, by the maximum principle,
> `sup_K |Z_{G_q}| = O(1)`, which with §2's half-plane bound is Lemma U1-0, i.e. **U1**. ∎
>
> **Consequence, and it is the reason this test was worth running:** a refutation of (5.1) is a
> refutation of **U1 itself**, not merely of one route to it. `LAW_U1_GROWTH.md` §6 stated only the
> (⇐) direction ("either one … closes U1"); the (⇒) direction is new here and it is what makes the
> test two-sided.

### 1.5 `HEURISTIC` — an a-priori reason for scepticism, and one against it

**Against (5.1).** The `q`-scaling cannot come from the cusp. `G_q` has one cusp, of width
`λ_q = 2cos(π/q) ∈ [1, 2)`, which is **bounded and bounded away from `0`** — the usual
`h^{1−2s}`-type normalisation factor of a width-`h` cusp is therefore `O(1)` in `q` and cannot
produce `q^{−3}`. The only available source is the **degeneration of the order-`q` cone point into
`Γ_θ`'s second cusp** (the reading already recorded in `LAW_U1_GROWTH.md` §3.3). But `φ_q` is a
`1×1` determinant of a one-cusp group and `φ_θ` is the `2×2` determinant of a two-cusp group;
there is no continuity principle that makes the former converge to the latter up to an explicit
power. A new cusp opening generically **creates** resonances rather than preserving their count.

**For (5.1).** The degeneration is *not* a pinching one: `|X_q| = π(1−2/q) → π` is continuous, no
geodesic collapses, and the systole is uniformly bounded below (`LAW_U1_GROWTH.md` §2.2). So the
violence of a pinching degeneration is absent. Moreover the elliptic mass
`M(q) = (1/π)log(2e^γ q/π)` of Lemma U1-5, which enters the *winding* term of the Weyl law, is of
exactly the size that a `(q/2π)^{2s−1}`-type factor in `E_q` produces — so §5.2's `log q` is **not**
by itself evidence against (5.1). Both readings are `HEURISTIC`; the measurement below decides.

---

## 2. Literature — the honest result: **the intended source could not be opened**

A dedicated retrieval pass was run against the sources `LAW_U1_GROWTH.md` §9 item 2 named.

| target | outcome |
|---|---|
| **Hejhal, *Eigenvalues of the Laplacian for Hecke triangle groups*, Memoirs AMS 469 (1992)** | **NOT READ.** Existence confirmed (AMS listing `bookstore.ams.org/memo-97-469`, Memoirs vol. 97 no. 469, 165 pp.; `pubs.ams.org/ebooks/memo/0469`). Full text behind AMS/MathSciNet paywall; no accessible excerpt, review text, or third-party quotation of its `φ_q` content was retrieved. `TODO-VERIFY(Hejhal Memoirs AMS 469 — obtain via institutional access; extract the normalisation of `E_q(z,s)` for the width-`λ_q` cusp, any closed form or table for `φ_q`, and any `q`-asymptotic.)` |
| **Hejhal, *On eigenvalues of the Laplacian for Hecke triangle groups*, Adv. Stud. Pure Math. 21 (1992) 359–…** | **NOT READ.** Project Euclid PDF located (`10.2969/aspm/02110359`); text not extractable in this session. `TODO-VERIFY`. |
| **Winkler, *Cusp forms and Hecke groups*, J. reine angew. Math. 386 (1988) 187–204** | **NOT READ.** Existence confirmed only. `TODO-VERIFY`. |
| **Phillips–Sarnak**, Invent. Math. 80 (1985) 339–364 and JAMS 5 (1992) 1–32 | **NOT READ** this session. Carried unchanged from `LAW_U3_TRANSPORT.md` §4 as the reason to expect no closed form for `φ_q` at non-arithmetic `q`. |
| **Fedosova, arXiv:2509.17936** (transfer-operator approximation of `Z_Γ` for Hecke triangle groups) | **READ** (HTML). Relevant only negatively: it computes `Z_{Γ_w}` via **finite-dimensional determinants with explicit exponentially decaying error**, i.e. it takes exactly the route this repo takes and **does not** introduce or tabulate `φ_q`. |
| explicit `φ_q` / Eisenstein constant term for `G_q`, non-arithmetic `q` | **NONE FOUND.** No closed form, no table, no `q`-asymptotic, and no explicit statement of a cusp-width normalisation factor for Hecke groups was retrieved. |
| degeneration asymptotics for scattering matrices (Judge, Wolpert, Jorgenson–Lundelius) | **NOT READ.** Titles located; nothing specific to `G_q → Γ_θ` retrieved. `TODO-VERIFY`. |

> **Conclusion of §2.** `LAW_U1_GROWTH.md` §9's plan — "*a literature lookup plus one plot*" — is
> **not executable** at this access level. The Memoir was not opened, so **nothing is imported from
> it, and no number in this note is attributed to it.** Absence of a retrieved source is **not**
> clearance: a `φ_q` table may well exist in Memoirs 469 and would supersede §4.
> **This is why the test below was redesigned to use the repo's own machinery instead.**

---

## 3. The test design — the critical line carries the whole answer

### 3.1 `PROVED` — on `Re s = 1/2`, `κ_q` is one determinant evaluation

`Z_{G_q}` has real Dirichlet coefficients (an Euler product over real norms `N(P) > 1`), so
`Z_{G_q}(s̄) = conj Z_{G_q}(s)`. On `Re s = 1/2` one has `1 − s = s̄`, hence

```
   kappa_q(1/2 + it)  =  Z_q(1-s)/Z_q(s)  =  conj Z_q(1/2+it) / Z_q(1/2+it)
                      =  exp( -2 i · arg Z_q(1/2+it) ) .                        (3.1)
```

`PROVED`. **One** evaluation of `Z_q` per `(q, t)` gives `κ_q` completely — no evaluation at
`Re s = −1` is needed, which matters because the determinant proxy has no identification there.

Every factor of `κ_q` has modulus `1` on `Re s = 1/2` (`LAW_U1_GROWTH.md` §3.1, verified there to
`1e−17` factor by factor), so on the critical line **the entire content of (5.1) is a statement
about phase** — precisely the information the sup-guard, which measures `|Z_q|` only, is
structurally blind to. The two tests are independent in the strongest sense: they read disjoint
components of the same object.

### 3.2 `PROVED` — the ansatz, the slope, and the decisive exponent

Suppose the `q`-dependence of `φ_q` is a pure power in the Teo variable `2s−1`:

```
   phi_q(s)  =  (c_q)^{2s-1} · psi(s) · (1 + o(1)) ,     c_q = C · q^{-alpha} .   (A)
```

(5.1) is exactly `α = 1`, `c_q = π/q`. Under (A), on `s = 1/2 + it`:

- `arg φ_q` gains `2t log c_q = −2αt log q + const`;
- `arg E_q` gains `+2t log q + const` (Lemma U1-4b);
- every other factor of `κ_q` is `q`-independent **except** the Barnes exponent `(1−2/q)/2`, whose
  `q`-dependence is `O(1/q)`.

Therefore

```
   D_q(t) := arg kappa_q(1/2+it) = -2 arg Z_q(1/2+it)
           = const(t)  +  beta · log q  +  O(1/q) ,     beta = 2 t (1 - alpha) .  (3.2)

   alpha = 1 - beta/(2t) ,        |phi_q(2+it)| ~ q^{-3 alpha} .                  (3.3)
```

> **The decisive number is `−3α = −3 + 3β/(2t)`.**
> `β = 0` ⟺ `α = 1` ⟺ exponent `−3` ⟺ **PREDICTION CONSISTENT**.
> `β = 2t` ⟺ `α = 0` ⟺ exponent `0` ⟺ `φ_q` has no `q`-decay ⟺ **PREDICTION REFUTED**.

**The ansatz (A) is itself tested**, not assumed: (3.2) says `β` must be **proportional to `t`**.
The probe runs at two heights, `t = 1.5` and `t = t_∞ = 7.0673625708673465`, and the ratio
`β(t_∞)/β(1.5)` must come out `4.7116` if (A) holds.

### 3.3 Why this simultaneously tests **both** prongs of (U1-φ)

`D_q(t)` is (twice) the scattering phase, and the winding term of the Weyl law is
`M_q(T) = (1/4π)∫_{−T}^{T}(−φ_q'/φ_q)(1/2+it)dt` — the integral of the same phase. A `log q` drift
in `D_q` **is** growth of the winding, i.e. resonance accumulation in the fixed disc. So a nonzero
`β` bears on **(U1-φ-b)** (uniform resonance count) as well as on **(U1-φ-a)**. `HEURISTIC` as a
quantitative link; `PROVED` that the two quantities are the same phase.

### 3.4 What is actually evaluated, and its two honest caveats

`Z_{G_q}(1/2+it)` is replaced by the repo's only in-strip evaluator, the Rosen/MMS
transfer-operator determinant product over the two `P`-symmetric sectors,

```
   P_q(s) := det(1 - L_{s,q}^{+}) · det(1 - L_{s,q}^{-}) ,
```

built by `.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py` (even `q`), midpoint
evaluation at `N = 32` collocation points, 400-bit Arb precision, `n_head = 4`.

1. **Identification (U4).** `P_q = Z_{G_q}` is R5 at `q = 5` and obligation **U4** in general
   (`GAP`). `LAW_U1_GROWTH.md` §7.2 gives it `3e−4 … 2e−3` support at `q = 12,16,22,30,40` on
   `Re s > 1`; §4.1 below adds a **phase** check that the earlier work never made.
2. **Domain.** Both heights satisfy `Im s > 1`, so `1/2 + it` lies **inside** the R5 common
   continuation domain `Ω* = {Re s > 1/2} ∪ {Re s > 0, Im s > 1}`
   (`TB_R5_DETERMINANT_IDENTIFICATION.md`). This is strictly better than the guard, whose largest
   values sat on `Re s = 0`, i.e. on `∂Ω*`, and had to be discarded.

**NON-RIGOROUS:** midpoint arithmetic, no ball radii, no winding certificate. Float evidence only.

### 3.5 The branch hazard, and how it is handled

`D_q` is recovered from `arg P_q` only **mod `2π`**. The probe reduces each `D_q` to `(−π, π]` and
then unwraps along **increasing `q`**, which is valid iff every consecutive step is `< π`. The
predicted-if-refuted swing is `β log(q_max/q_min) = 2t · log(40/12)`, i.e. `3.6` rad at `t = 1.5`
and `17.0` rad at `t = t_∞` — hence the deliberately **fine `q`-grid**, and hence the low height
`t = 1.5`, whose swing is unwrappable with no ambiguity at all. The maximum realised step is
reported with the fit and must be `< π = 3.1416`.

This hazard is not hypothetical. Assembling `E_q(1/2+it)` from principal logarithms and comparing
its argument against Lemma U1-4b's closed form gives a residual `× q` that is **stable** at
`t = 1.5` (`6.47, 6.60, 6.67, 6.70` at `q = 12, 20, 30, 40` — clean `O(1/q)`, confirming U1-4b on
the imaginary part as the parent note confirmed it on the real part) but **divergent** at
`t = t_∞` (`−24.6, −113.7, −233.2, −355.7`), which is a pure `2π`-bookkeeping artefact of the
`2t log(q/2π)` term, not a failure of U1-4b. `HEURISTIC`. **This is exactly why the probe measures
`arg κ_q` directly and unwraps it, rather than assembling `κ_q` factor by factor.** The modulus
identity `|E_q(1/2+it)| = 1` (Lemma U1-4a) was re-verified to full precision at all these points.

---

## 4. The measurement

### 4.1 The phase control — `PROVED`-grade, and it is new

Before any inference: at real `s = 2`, `Z_{G_q}(2) > 0`, so a correct identification must give
`arg P_q(2) = 0`. Measured, **`q = 12, 14, …, 40` (14 values):**

```
   arg P_q(2.0)  =  +0.000e+00   exactly, for every q .
```

and `|P_q(2)| = 0.9757547, 0.9772822, …, 0.9808582` reproduces `u1_sup.log`'s control column to
**all printed digits**. **So the proxy carries no spurious `q`-dependent phase**, which is the one
failure mode that would have invalidated a phase measurement. Earlier probes used `|P_q|` only and
never checked this. `HEURISTIC` by label; exact to working precision in fact.

Cross-validation: `|P_12(0.5 + 7.0674i)| = 6.432000e−01` here, against `dU_0` of `u1_sup.json` at
`q = 12`, `6.432000e−01` — identical, on a different interpreter
(`miniforge3/envs/pari-arb`, python-flint 0.8.0) from the one the guard used.

### 4.2 The two series — **NON-RIGOROUS**

`D_q(t) = −2 arg P_q(1/2 + it)`, reduced to `(−π, π]` then unwrapped in increasing `q`.
Full per-point data in `law_probes/u1phi.json`, log `u1phi.log`.

**`t = 1.5`** (10 values of `q`; max unwrap step `0.543` rad `< π` ✓):

| `q` | 12 | 14 | 16 | 18 | 20 | 22 | 26 | 30 | 34 | 40 |
|---|---|---|---|---|---|---|---|---|---|---|
| `D_q` | `+1.384` | `+0.918` | `+0.374` | `−0.044` | `−0.267` | `−0.344` | `−0.275` | `−0.096` | `+0.107` | `+0.397` |

**`t = t_∞ = 7.0673625708673465`** (8 values; max unwrap step `1.239` rad `< π` ✓):

| `q` | 12 | 16 | 20 | 24 | 28 | 32 | 36 | 40 |
|---|---|---|---|---|---|---|---|---|
| `D_q` | `+4.061` | `+2.860` | `+2.602` | `+2.472` | `+3.276` | `+2.037` | `+2.117` | `+2.761` |

### 4.3 The model-free statistic — **the null dies here**

A `log q` drift is **monotone** and of size `β · log(40/12) = 1.204 β`. The null `β = 2t`:

| `t` | `n` | observed span of `D_q` | **null-required swing `2t·log(40/12)`** | ratio | monotone? |
|---|--:|---|---|---|---|
| `1.5` | 10 | `1.728` rad | `3.612` rad | `0.478` | **no** (turns at `q ≈ 22`) |
| `7.0674` | 8 | `2.024` rad | **`17.018` rad** | **`0.119`** | **no** (turns at `q ≈ 32`) |

**At the physical height the null over-predicts the observed variation by a factor `8.4`, and
predicts a monotone drift where the data turns around twice.** This conclusion uses no fitted
model at all: it compares a total variation against a required monotone swing.
`HEURISTIC` by label (float, proxy), but it is the most robust statement in the note.

> **Corollary.** `|φ_q(2+it)| ≍ 1` — the "no decay" scenario `LAW_U1_GROWTH.md` §5.1 called the
> *trivial bound*, and the scenario the guard was read as supporting — is **excluded** by this
> measurement. `HEURISTIC`.

### 4.4 The exponent — and the honest fact that single-height fits do not determine it

Naive single-height inversion of (3.3), `α = 1 − β/(2t)`:

| `t` | `β` (LSQ) | `α` | exponent `−3α` | max resid |
|---|---|---|---|---|
| `1.5` | `−0.7875` | `1.2625` | `−3.788` | `0.704` |
| `7.0674` | `−1.0780` | `1.0763` | `−3.229` | `0.658` |

Both bracket `−3` from below, but **they disagree with each other**, and the residuals are `~40%`
of the signal. Adding a `γ/q` nuisance term (`u1phi_fit.py`) makes it worse, not better: at
`t = 1.5` the 3-parameter fit flips the slope to `β = +5.99` (`exponent +2.99`) while cutting the
residual to `0.177`. **Over `q = 12 … 40` a `log q` term and a `1/q` term are not separately
identifiable.** Reported as a defect of the parametric route, not hidden.

**The resolution, and it is the note's quantitative deliverable.** (3.2) predicts
`β(t) = 2t(1−α)`, so `β(t_∞)/β(1.5)` must be `t_∞/1.5 = 4.7116`. Measured: **`1.369`** (LSQ),
**`1.318`** (endpoint). **The pure-power ansatz (A) alone is refuted.** But the two slopes are
*nearly equal*, which is the signature of an additive, **`t`-independent** `log q` term — exactly
what a mis-modelled `q`-dependent *constant* in `κ_q` produces (the Barnes exponent `(1−2/q)/2`,
the sign `(−1)^{A_q/2}`, and the branch conventions of the fractional powers are all
`t`-independent). So refine the model to

```
   beta(t)  =  2 t (1 - alpha)  +  delta ,        delta  independent of t .        (4.1)
```

Two heights, two unknowns, solved exactly:

| slopes used | `1 − α` | `α` | `δ` | **exponent `−3α`** |
|---|---|---|---|---|
| LSQ (`−0.7875`, `−1.0780`) | `−0.0261` | `1.0261` | `−0.709` | **`−3.078`** |
| endpoint (`−0.8198`, `−1.0801`) | `−0.0234` | `1.0234` | `−0.750` | **`−3.070`** |

> ### **The decisive number: `|φ_q(2+it)| ≍ q^{−3.08}`, against the prediction `q^{−3}`.**
> The `(π/q)^{2s−1}` scaling is recovered to **`2.6%` in the exponent `α`**, and the two
> estimators — a 10-and-8-point least squares, and a bare endpoint difference — agree to `0.008`.
> `HEURISTIC`. The residual `δ ≈ −0.7` is `t`-independent and is **not** part of (5.1)'s shape;
> it is charged to the `t`-independent factors of `κ_q` (§7 records it as an open item, `GAP`).

### 4.5 Unasked-for: the guard's rise is confined to the out-of-domain edge

`LAW_U1_GROWTH.md` §7.3 reports `sup_{∂U}` rising with log-log slope `+1.50`. That note never
broke the sup down by point. Doing so, from `u1_sup.json` + `u1_sup_q40.json`
(`|det⁺·det⁻|`, `q = 12, 16, 22, 30, 40`):

[CORRECTED 2026-08-16 per ADVERSARIAL_REVIEW_U1PHI_ROUTE.md D5: the slope column below is
recomputed at source — the original column did not follow from its own tabulated `q=12…40` data
(the `dU_5` entry, in particular, had the wrong sign).]

| point | `Re s` | `q=12` | `16` | `22` | `30` | `40` | **log-log slope `12→40`** |
|---|---|---|---|---|---|---|---|
| `dU_0` | `0.5000` | `0.643` | `0.508` | `0.270` | `0.150` | `0.252` | **`−1.028`** |
| `dU_1` | `0.4268` | `0.245` | `0.090` | `0.153` | `0.158` | `0.025` | **`−1.88`** |
| `dU_7` | `0.4268` | `2.952` | `0.953` | `0.348` | `1.054` | `0.630` | **`−1.28`** |
| `dU_6` | `0.2500` | `13.69` | `2.295` | `6.101` | `8.273` | `3.236` | **`−1.20`** |
| `dU_2` | `0.2500` | `1.886` | `0.517` | `1.065` | `2.888` | `3.936` | **`+1.064`** |
| `dU_5` | `0.0732` | `81.84` | `17.38` | `49.47` | `92.81` | `35.30` | **`+0.022`** |
| `dU_3` | `0.0732` | `36.11` | `25.14` | `13.71` | `48.18` | `99.40` | **`+0.878`** |
| `dU_4` | `0.0000` | `170.0` | `92.79` | `41.69` | `266.4` | `275.4` | **`+0.669`** |

**Five of eight points decrease in `q`; the three that rise all have `Re s ≤ 0.25`, and the two
largest in magnitude — the ones that *set* the sup — are `dU_3` and `dU_4` at `Re s = 0.0732` and
`Re s = 0`.** `dU_4` was already excluded by the parent note for lying on `∂Ω*`; `dU_3` sits
`0.073` away from it and its mirror `dU_5`, at the *same* abscissa, has slope `−0.70`. The `+1.50`
sup slope is therefore driven by the region where the R5 identification is weakest, and the
per-point behaviour at the same abscissa is inconsistent in sign. `HEURISTIC`.

**This does not vindicate U1** — `sup` is what U1 is about, and a sup over a set including a
badly-behaved point is still a sup. It does mean the parent note's "**the quantity U1 asserts to
be bounded is growing**" over-reads the data: on the half of `∂U` where the proxy is trustworthy,
it is **shrinking**.

---

## 5. What it means for the tail

### 5.1 If the reading is right (exponent `−3`)

By **Lemma U1φ-1** (§1.4), (U1-φ-a) is not merely sufficient for U1 — it is equivalent to it. So
`|φ_q(2+it)| ≍ q^{−3}` means `κ_q(2+it) = O(1)`, hence `sup_{Re s = −1}|Z_{G_q}| = O(1)`, hence
(with `LAW_U1_GROWTH.md` (2.1) on the right edge and the maximum principle on
`[−1,2] × [t_∞−1, t_∞+1]`) **U1 holds**, and the §9 tail theorem of `LAW_U1_GROWTH.md` becomes
unconditional except for **U2b** and **U4**. The route's remaining obligations would then be, in
order: U2b (cheap, near-closed), U4 (needed only for the certified finite base), U5 effectivity.

**The lane's priority order should invert.** `LAW_U1_GROWTH.md` §9 recommended
*"extend the guard before funding anything else … if the `+1.5` slope persists to `q = 100`,
(T2′) is dead"*. On the evidence here the guard's slope is not measuring what that
recommendation assumed (§4.5), and the independent phase test points the other way. **The
extended guard remains worth finishing** — it is running — **but its verdict should now be read
against §4.5's per-point breakdown, and a rise confined to `Re s ≤ 0.073` should no longer be
treated as fatal.**

### 5.2 If the reading is wrong

Three ways it could be, and each is a concrete next check rather than a shrug.

1. **The proxy is not `Z_{G_q}` (U4).** Everything here is `P_q = det(1−L⁺)det(1−L⁻)`. §4.1's
   phase control is real evidence that the identification is phase-clean, and it is new, but it is
   evidence at `Re s > 1` only. If `P_q` and `Z_{G_q}` differ by a `q`-dependent factor that is
   trivial on `Re s > 1` and non-trivial on `Re s = 1/2`, §4 measures that factor instead.
   **U4 is now load-bearing for this note in a way it was not for the sup guard**, because a phase
   is more delicate than a modulus. `GAP`.
2. **Model (4.1) is a two-point fit of a two-parameter model.** It has zero degrees of freedom:
   it *cannot* fail. Its credibility rests entirely on (i) `α` coming out at `1.02` rather than at
   some unrelated value, and (ii) the two slope estimators agreeing to `0.008`. **A third height
   would give it a degree of freedom and is the single cheapest strengthening available** (§5.3).
3. **`q ≤ 40`.** The prediction is asymptotic. `log 40 − log 12 = 1.204` is barely one `e`-fold;
   a slowly-varying correction can masquerade as a shifted `α` over that range.

### 5.3 Recommended next, in cost order

1. **A third height.** Re-run `probe_u1phi.py` at `t = 3.5` on the same `q` grid (≈ 25 min). It
   turns (4.1) from an interpolation into a testable overdetermined fit and directly checks the
   `t`-independence of `δ` — the one modelling assumption doing real work. **This is the highest
   value-per-minute item in the lane right now.**
2. **Pin `δ`.** Compute the `t`-independent factors of `κ_q` in closed form at `Re s = 1/2` —
   `(−1)^{A_q/2}`, `2^{−(2s−1)}`, and the Barnes bracket at exponent `(1−2/q)/2` — and check
   whether their combined `q`-drift is the measured `δ ≈ −0.71`. If it is, (5.1) is confirmed with
   no residual at all, and `α` should be re-fitted with `δ` **known** rather than free, which
   restores a degree of freedom at each height. Needs Teo's `Γ₂` convention pinned (`V3` of
   `LAW_U3_TRANSPORT.md` §6).
3. **Extend the `q` grid to `q = 56, 72` at `t = t_∞`** — reuses the same machinery as the
   running guard extension and doubles the `log q` lever.
4. **Hejhal Memoirs AMS 469** (§2) remains owed to a human with library access. It could supersede
   all of §4 with an actual `φ_q` table.

---

## 6. Status ledger

| # | Step | Status | Note |
|---|---|---|---|
| Uφ.1 | (5.1) re-derived from Teo `κ` for `(0;1;2,q)` vs `(0;2;2)` | `PROVED` given `CITATION(Teo Prop. 2.5)` + U1-4b | §1.2 — exact match, `π = 2π/2` explained |
| Uφ.2 | `R(s)R(1−s) = 1` for the Γ-skeleton | `PROVED` (closed form) + numeric `≤1.1e−42` | §1.3 — unitarity-forced |
| Uφ.3 | `\|R(1/2+it)\| = 1` | `PROVED` | §1.3 |
| Uφ.4 | **`(U1-φ-a) ⟺ U1`** — necessity as well as sufficiency | `PROVED` | §1.4 Lemma U1φ-1 — **new**; makes the test deciding |
| Uφ.5 | The `(π/q)^{2s−1}` factor is not independently provable; it *is* `κ_q → κ_θ` | `PROVED` (logical) | §1.4 |
| Uφ.6 | Cusp width `λ_q ∈ [1,2)` cannot source the `q`-scaling | `PROVED` | §1.5 — the scaling must come from the cone-point degeneration |
| Uφ.7 | Hejhal Memoirs AMS 469 content | **`TODO-VERIFY` — NOT OPENED** | §2; existence confirmed, text paywalled. **Nothing imported.** |
| Uφ.8 | No explicit `φ_q` for non-arithmetic `G_q` retrieved anywhere | negative literature result | §2 — absence is **not** clearance |
| Uφ.9 | `κ_q(1/2+it) = exp(−2i·arg Z_q(1/2+it))` | `PROVED` | §3.1 — one evaluation per point; avoids `Re s = −1` |
| Uφ.10 | On `Re s = 1/2` the whole of (5.1) is a phase statement | `PROVED` | §3.1 — disjoint from what the sup-guard reads |
| Uφ.11 | `arg P_q(2.0) = 0` exactly, `q = 12…40` (14 values) | `HEURISTIC` (exact to working precision) | §4.1 — **new**; the proxy is phase-clean |
| Uφ.12 | `\|P_q\|` control column reproduces `u1_sup.log` to all digits, different interpreter | `HEURISTIC` | §4.1 |
| Uφ.13 | `\|E_q(1/2+it)\| = 1` re-verified; U1-4b `O(1/q)` confirmed on the imaginary part at `t=1.5` | `HEURISTIC` | §3.5 — residual `×q` = `6.47…6.70` |
| Uφ.14 | **Null (`\|φ_q\| ≍ 1`) excluded model-free: span `2.02` rad vs required monotone `17.02` rad** | `HEURISTIC` | §4.3 — the most robust claim here |
| Uφ.15 | Single-height fits do not determine the exponent (`−3.79` vs `−3.23`; `γ/q` flips the sign) | `HEURISTIC` — **a reported defect** | §4.4 |
| Uφ.16 | Pure-power ansatz (A) alone **refuted**: slope ratio `1.37` vs required `4.71` | `HEURISTIC` | §4.4 |
| Uφ.17 | **Two-height fit `β(t)=2t(1−α)+δ`: `α = 1.026`, exponent `−3.078`** (endpoint: `1.023`, `−3.070`) | `HEURISTIC` | §4.4 — **the deliverable number** |
| Uφ.18 | Residual `t`-independent drift `δ ≈ −0.71` unexplained | `GAP` | §4.4; §5.3 item 2 is the check |
| Uφ.19 | (4.1) is a zero-degree-of-freedom fit | **stated limitation** | §5.2 — a third height fixes it |
| Uφ.20 | **Guard's `+1.50` rise is confined to `Re s ≤ 0.0732`; 5 of 8 `∂U` points decrease; `Re s = 1/2` slope is `−0.78`** | `HEURISTIC` | §4.5 — **new, unasked-for**; weakens `LAW_U1_GROWTH.md` §7.3 |
| Uφ.21 | U4 (`P_q = Z_{G_q}`) is now load-bearing for a **phase**, not just a modulus | `GAP` — **promoted** | §5.2 item 1 |

---

## 7. What this note claims and does not claim

**Claims.**
(i) (5.1) is re-derived independently and matches the parent note exactly (§1.2, `PROVED` given
Teo + U1-4b).
(ii) `R(s)R(1−s) = 1` identically for the Γ-skeleton (§1.3, `PROVED`) — the prediction is exactly
unitarity-compatible, which is the provable-today half of it.
(iii) **Lemma U1φ-1: `(U1-φ-a) ⟺ U1`** (§1.4, `PROVED`) — necessity is new and makes the test
two-sided.
(iv) The proxy is **phase-clean**: `arg P_q(2.0) = 0` exactly at 14 values of `q` (§4.1).
(v) **Model-free, the no-decay null is excluded**: the observed span of the scattering phase is
`2.02` rad at `t = t_∞` against a required monotone `17.02` rad, and the data is non-monotone
(§4.3, `HEURISTIC`).
(vi) **The fitted exponent is `−3.08`** (two-height decomposition, LSQ) / `−3.07` (endpoint),
against the predicted `−3` (§4.4, `HEURISTIC`).
(vii) The pure-power ansatz alone is refuted (slope ratio `1.37` vs `4.71`); it is repaired by a
`t`-independent additive drift `δ ≈ −0.71`, and the repair is what yields `α = 1.026` (§4.4).
(viii) **The guard's adverse rise is confined to `Re s ≤ 0.0732`**; five of eight `∂U` points
decrease in `q`, and at `Re s = 1/2` the slope is `−0.78` (§4.5, `HEURISTIC`, unasked-for).

**Does not claim.**
**U1 is not proved, and (U1-φ-a) is not proved.** Every number in §3.5 and §4 is float / `mpmath`
midpoint arithmetic on an Arb determinant — no interval arithmetic, no ball radii, no winding
certificate. The object measured is `P_q`, not `Z_{G_q}`: obligation **U4** is `GAP` for `q ≠ 5`
and this note *raises* its stakes (Uφ.21). **Hejhal Memoirs AMS 469 was not opened**, nor was any
other source that might contain an actual `φ_q`; no number here is attributed to any of them, and
absence of a retrieved source is not clearance. The exponent `−3.08` comes from a
**zero-degree-of-freedom** two-height fit whose `t`-independence assumption is untested (a third
height is §5.3 item 1); single-height fits alone do **not** determine the exponent, and adding a
`1/q` term flips the sign of the slope at `t = 1.5` (Uφ.15 — reported, not hidden). The residual
`δ ≈ −0.71` is unexplained (`GAP`). Nothing is claimed for `q > 40`, for `t` outside
`{1.5, 7.0674}`, or for odd `q` (the builder is even-`q`). No progress on U2b, U4, U5. No
certificate. No prior-art clearance.

**A refutation was actively sought — and one was found, though not the expected one.** The test
was designed so that (5.1) *could* die: the null predicts a `17` rad monotone drift that would have
been unmissable. It did not die. What **was** refuted is (5.1)'s own *pure-power form*: the two
heights give nearly equal slopes where proportionality to `t` was required (`1.37` vs `4.71`), so
(5.1) as literally written is incomplete and needs the `t`-independent term `δ`. Two further
adverse findings are recorded against this note's own conclusion rather than buried: the
single-height fits disagree with each other and with the two-height answer, and the `γ/q`
robustness fit inverts the sign of the slope at the low height. And one adverse finding was
recorded against a **parent** note: `LAW_U1_GROWTH.md` §7.3's headline over-reads its own data,
because the sup it reports is set by the two points where the identification is weakest (§4.5).

---

## 8. Receipts index

- `law_probes/probe_u1phi.py` — the test. Receipt `law_probes/u1phi.json`, log `law_probes/u1phi.log`.
- `law_probes/u1phi_fit.py` — post-hoc robustness fits (`2`-param vs `3`-param with a `γ/q`
  nuisance term; tail-only refit). Receipt `law_probes/u1phi_fit.json`.
- Reused unchanged: `.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py` (even-`q` Arb
  determinant builder).
- **Not touched:** `law_probes/u1_guard_extended.*` (a concurrent probe owns it), `lane_f`.
- Interpreter: `/Users/za/miniforge3/envs/pari-arb/bin/python3` (python-flint 0.8.0). Its control
  values reproduce `law_probes/u1_sup.log` to all printed digits, so it is interchangeable with the
  `.venvs/farey-rh` interpreter the earlier probes used.

---

## Addendum 2026-08-16: third height t = 3.5 — the fit is now overdetermined

Per §5.2 recommendation 1. Runner: `law_probes/probe_u1phi_t35.py` (reuses
`probe_u1phi.py`'s proxy verbatim; N = 32, same q grid 12–40). Receipts:
`law_probes/u1phi_t35.json`, `u1phi_t35.log`, `u1phi_threeheight.json`.

- **t = 3.5 standalone**: β = +0.0931 → α = 0.9867 → **exponent −2.9601**
  (max unwrap step 1.3845 rad, branch-safe).
- **Joint three-height fit** β(t) = a + m·t over t ∈ {1.5, 3.5, 7.0674}:
  m = −0.0845, a = −0.2507 (max resid 0.6397 rad) →
  **α_joint = 1.0423 → exponent −3.1268**.
- **Null killed with dof to spare**: the no-decay null demands m = 2
  (β = 2t); measured m = −0.08. The single-height disagreement flagged in
  §5.2 (−3.79 at t=1.5 vs −3.23 at t_phys) resolves as the t-independent
  drift δ absorbing the low-t distortion: the t=3.5 point falls between
  them at −2.96, monotone toward −3 as t grows.
- Caveat unchanged: all three heights float on the U4-unidentified proxy.

**VERDICT (upgraded): PREDICTION-CONSISTENT, overdetermined. The zero-dof
limitation of the original fit is discharged; the exponent brackets −3
from both sides (−2.96 / −3.13).**
