# LAW Route B — the CONDITIONAL THEOREM

> **[AMENDMENT RB-A3, 2026-08-16 — COLD REVIEW RULING: MIS-INSTANTIATED, AND
> THE CORRECTED INSTANTIATION IS O(1) ⇒ ROUTE B VIA (B4★) IS DEAD; Q₀ = 1465
> IS WITHDRAWN AS UNSUPPORTED.]** COLD_REVIEW_ROUTEB_FATE.md: q_{M_q} appears
> ONCE in GJ and is never defined; it is NOT the elliptic order q — three
> independent lines identify it as λ_q = 2cos(π/q) (σ→∞ limits measured to
> 1/(2σ) residuals: 0, log 2, log 3 = 2 log λ_q exactly; Herglotz structure;
> q_M>1 excludes exactly q=3). Budget is 2 log λ_q ≤ 2 log 2 — BOUNDED. The
> pigeonhole has bounded LHS vs growing RHS: no contradiction for any C, δ₀.
> REVERSALS: correctly instantiated lemma HOLDS at q=3,4,6 with positive
> margin (the "refutation" came from GJ's misprinted numerator, which §1.5
> wrongly ruled non-load-bearing); the A_Γ log-q fear is UNFOUNDED (true
> A_Γ = O(1), |A_Γ| ≤ 1.64 for r ≥ 2 — the probe's 𝒜_q was the FE kernel,
> not A_Γ); B3 (averaged log q counts, constants from unpublished Hejhal)
> RESTORED to critical path as the only genuine log q growth in GJ. Hejhal
> p.160 / HJL primary text now decides the only open question (HITL). LAW_AGAMMA_PROBE.md: α = 2.000 (closed-form, q to
> 4000, not determinant-dependent) — the ENTIRE 2 log q positivity budget is
> supplied by the order-q elliptic point's own Γ-factor (91%), not resonance
> mass; the resonance part 𝒢_q has NO positive log q content (slope −1.8…−0.4,
> R² ≤ 0.09). T(0.2) → −0.023: (B4★) degenerates to P_q ≥ 0 and the pigeonhole
> forces nothing. Also: (B4★) pointwise with q_M = q REFUTED at arithmetic
> q=3,4,6 (inf_r LHS negative) — this note's §1.2(d) identification needs
> re-opening; the winding-blindness alternative is dead (sliver: 1–2 poles,
> no growth). A cold frontier review must rule DEAD vs MIS-INSTANTIATED
> before any further Route-B work.

> **[AMENDMENT RB-A1, 2026-08-16 — B5-J FAILED; B5 RESTATED AS (THRESH).]**
> LAW_B5J_JENSEN.md: §6.3(1)'s "entire of order 0 in s, no U1 needed" is
> REFUTED — order 0 holds for the Fredholm/eigenvalue expansion, not the
> s-plane; measured s-plane growth 11.8–16.2 per unit Re s, increasing in q.
> The Jensen sup bound IS U1 in disguise; a disc cannot resolve depth (any
> covering disc swallows the shallow band), realised C_J ≈ 35–71 growing
> linearly in q ⇒ no Q₀ from that route. B5 is hereby RESTATED as (THRESH):
> deep-count slope c₂ < 0.14903 at δ₀=0.2 suffices (materially weaker than
> O(1)); the winding-measured deep count (flat, {5,6,7}) passes comfortably.
> Banked positives: Lemma H (continuation into the strip is NOT the
> obstruction; uniform |ζ(2s+m+j,a₀)| ≤ 0.94 bound, 36/36 verified) and the
> mechanism statement "the degeneration making the theorem true destroys the
> uniform operator bound" (1−sup|h'| = π²/q²; Markov partition forces
> κ/(1−θ) = Ω(q³)). Critical path now: certified winding counts (the only
> depth-resolving instrument) + N-B4/N-B4b + t₀-uniformity probe.

**Date:** 2026-08-16. **Lane G, drafting lane.**
**Parents:** `LAW_SH_EFFECTIVIZATION_SKELETON.md` §3 (Route B, steps B1–B6);
`LAW_ROUTEB_DEEPCOUNT.md`, `LAW_ROUTEB_SUBSTRATUM.md`, `LAW_ROUTEB_Q18Q21.md` (the measurements);
`LAW_ANCHOR_T1_THETA.md` (T1, the `Γ_θ` limit object).

**What this document is.** The complete logical chain from the trace-formula positivity input to a
localization statement for `G_q`, with **every step status-labelled** and **every constant either
written down or named as an obligation**. It is a proof-strategy document, not a paper. Nothing
here is claimed as proved that is not proved.

**Status labels, used on every numbered step:**

| label | meaning |
|---|---|
| `PROVED-cited` | proved in a named source; the statement is quoted or precisely referenced |
| `PROVED-here` | derived in this document from labelled inputs, elementary and checkable |
| `MEASURED` | a repo measurement, non-rigorous probe; the obligation is to prove it |
| `GAP` | not proved anywhere known to this lane; an explicit obligation |
| `TODO-VERIFY` | reconstructed or read through a secondary channel; needs a primary-source check |

---

## 0. Verdict up front

> **The chain closes, conditionally, with an explicit `Q₀`.**
>
> **CONDITIONAL THEOREM (§5).** Fix `δ₀ = 0.2` and `t₀ ≥ 2`. **IF** the deep-resonance bound
> **(B5-bound)** holds — `#{s : φ_q(s) = ∞, Re s ≤ ½ − δ₀, |Im s − t₀| ≤ 1} ≤ C` for all
> non-arithmetic `q` and all `t₀` — **and** the shallow density bound **(B5b-bound)** holds with
> the measured affine constants, **THEN** for every `q ≥ Q₀(C)` the scattering determinant `φ_q`
> has a pole in the box
> `[½ − 0.2, ½) × [t₀ − 1, t₀ + 1]`,
> with
> **`Q₀(C) = exp[ (11.645·C + 1.006) / 1.7355 ]`**, and at the **measured** value `C = C(0.2) ≈ 1.0`:
>
> ### **Q₀ ≈ 1.5 × 10³   (explicitly, `Q₀ = 1465`).**
>
> Under the narrower reading of the shallow stratum (§5.4) the same chain gives `Q₀ = 877`.
> `Q₀` is **violently sensitive to `C`**: `C = 1.4 → Q₀ ≈ 2.1 × 10⁴`; `C = 2 → Q₀ ≈ 1.2 × 10⁶`.
>
> **The honest caveat, stated once and not softened.** `C` is `MEASURED` on ten groups in one
> fixed height window by a non-certified float winding probe. It is **not proved**, and the
> theorem is worthless as an unconditional statement until it is. Everything in §6 is about that.
>
> **Two findings that were not in the skeleton, and that change the route's shape:**
>
> 1. **The positivity input is far stronger than B3.** Skeleton §3 routed the `log q` mass through
>    B3 (`G_{M_q,0}(T) = (2C√(T−¼)/π)·log Q + O(1)`, with `C` and the `O(1)` both `UNKNOWN`).
>    That is unnecessary. HJL Lemma 5.3 is a **pointwise** lower bound valid at every `r`, with
>    **no unknown constant at all** (§1). Route B should be re-based on it and B3 dropped from the
>    critical path. This removes two `UNKNOWN`s from the constants table.
> 2. **B5 as written in the skeleton is incomplete.** Bounding the *deep* stratum is necessary but
>    not sufficient: the **far-field mass of the shallow stratum** also grows with `q` and must be
>    bounded, because shallow poles are numerous (`≈ 2.1 log q` per height-10 window). This is a
>    second obligation, **B5b**, that the measurement lane did *not* answer and that the skeleton
>    did not name. It is bounded here by the factor `δ₀` in the Poisson tail (§4.3) — the tail is
>    `O(δ₀ log q)`, small **only because `δ₀` is small**, which is exactly why the denominator
>    `2 − 0.265` in `Q₀` is not `2`. The route survives it, but it is load-bearing and it is a
>    `GAP` on the shallow side too.

---

## 1. The positivity input (B4), precisely

### 1.1 The statement

**[`PROVED-cited`, `TODO-VERIFY` on the transcription channel]**

Garbin–Jorgenson, *Spectral asymptotics on sequences of elliptically degenerating Riemann
surfaces*, arXiv:1603.01494 = L'Enseign. Math. **64** (2018) 161–206, §5 (proof of their
Thm 5.4), quoting **Huntley–Jorgenson–Lundelius, J. Funct. Anal. 149 (1997) 58–82, Lemma 5.3**,
itself from **Hejhal, LNM 1001 vol. 2 (1983), p. 160**:

> ```
>      φ'                N        1 − s_{k,q}
>   − ─── (½ + i r)  −   Σ    ───────────────────────   ≥   2 log q_{M_q}  >  0.
>      φ               k=1   (s_{k,q} − ½)² + r²
> ```

**Transcription provenance, stated because it matters.** This was read from the ar5iv HTML
rendering of arXiv:1603.01494 via an automated fetch, not from the journal PDF and not from
Hejhal p. 160 (a blocked HITL library item — the constraint of the parent skeleton is honoured
here too). The arXiv abstract page alone did **not** contain it; the full-text rendering did, and
returned it in the mangled-Unicode form
`−ϕ′ϕ(1/2+ir)−∑_{k=1}^{N} (1−s_{k,q})/((s_{k,q}−1/2)²+r²) ≥ 2 log q_{M_q} > 0`, located in
"Section 5, Proof of Theorem 5.4". The de-mangling above is mine. **Obligation N-B4: check this
against the journal PDF or the arXiv source before any of it is published.** In particular the
numerator `1 − s_k` is the single character most likely to be a transcription artifact; §1.4
records an independent derivation that disagrees with it, and §1.5 explains why the disagreement
does not matter.

### 1.2 What the symbols are

**[`PROVED-cited` for (a)–(c), `PROVED-here` for (d)]**

- **(a)** `φ = φ_{M_q}` is the scattering determinant. For a **one-cusp** group — and `G_q` has
  exactly one cusp — this is the scalar `1 × 1` scattering matrix, so `φ_q` *is* `det Φ_q`.
- **(b)** `s_{k,q}`, `k = 1 … N`, are the parameters of the **small (exceptional) eigenvalues**
  `λ_k = s_k(1 − s_k) < ¼` of the Laplacian on `M_q = G_q\H`, so `s_k ∈ (½, 1]`, real, finitely
  many. The `k = 1` term is the constant eigenfunction, `s_1 = 1`.
- **(c)** `q_{M_q}` is the **degeneration parameter**: per Garbin–Jorgenson, "*the positive
  integer `q_γ` is the order of the centralizer subgroup of the elliptic element `γ`*", and
  `Q = ∏_{γ ∈ DE(Γ)} q_γ` over the degenerating elliptic elements.
- **(d) For the Hecke family this is exactly the Hecke index.** `PROVED-here` from (c) plus
  Garbin–Jorgenson Example 5.8: `G_N\H` has "*genus zero with one cusp and three elliptic points
  of order 2, 3, and N*". Only the order-`N` point degenerates as `N → ∞` (the orders `2` and `3`
  are fixed), so the degenerating set is the single element of order `q`, and

  ```
     q_{M_q}  =  q,        Q  =  q.
  ```

  **This is the step that makes the whole route quantitative for `G_q`**, and it is clean: no
  unknown constant relates `log q_M` to `log q`; they are equal.

### 1.3 The bookkeeping question, answered

The parent brief flags this as the place a sign error kills the route. The answer:

> **`−(φ'/φ)(½ + ir)` counts POLES OF `φ`, and nothing else.**
> It does **not** count cusp-form eigenvalues. Embedded eigenvalues of the discrete spectrum do
> not appear in `φ` at all — in the trace-formula identity (B1) they sit in the **`N_{M,w}(T)`**
> term, on the *other* side of the scattering term. The `Σ_k` correction in Lemma 5.3 involves
> only the finitely many **exceptional** `s_k ∈ (½, 1]`, which are precisely the poles of `φ` on
> the real segment `(½, 1]` — i.e. still poles of `φ`, just the *residual*, non-resonance ones.

So the three objects are: (i) poles of `φ` with `Re < ½` — the **resonances**, what the theorem is
about; (ii) poles of `φ` in `(½, 1]` — the **residual/exceptional** poles, finitely many, real,
which the `Σ_k` term removes; (iii) cusp eigenvalues — **absent from `φ`**, irrelevant to this
inequality. Confusing (iii) with (i) is the error the brief warns about; it is not made here.

### 1.4 The Poisson-kernel structure

**[`PROVED-here`, modulo obligation N-B4b]**

`φ_q` is meromorphic in `C`, of finite order, satisfies `φ(s)φ(1−s) = 1`, and `|φ(½+ir)| = 1` for
real `r` (unitarity of the scattering matrix on the critical line). Hence its zeros are the
reflections `1 − ρ` of its poles `ρ`, and it admits a Blaschke/Hadamard factorization whose
non-elementary part is a product of factors `(s − (1−ρ))/(s − ρ)`.

Compute one such factor's contribution to `−(φ'/φ)` at `s = ½ + ir`. Write `ρ = β + iγ` and
`d := ½ − β` (the **depth**). Then

```
   − d/ds log [ (s − (1−ρ))/(s − ρ) ]  at  s = ½+ir
     = − [ 1/((½−β) + i(r−γ)) − 1/((β−½) + i(r−γ)) ]        ... for a pole at ρ
     = + 2d / ( d² + (r − γ)² ).
```

- A pole with `Re ρ < ½` has `d > 0` and contributes **`+2d/(d² + (r−γ)²) ≥ 0`** — a Poisson
  kernel of width `d` centred at height `γ`, with total mass `∫_R = 2π` independent of `d`.
- A pole with `Re ρ = s_k ∈ (½, 1]` (real, so `γ = 0`) has `d = ½ − s_k < 0` and contributes
  **`−2(s_k − ½)/((s_k − ½)² + r²) ≤ 0`**.

Therefore, defining the **resonance Poisson mass**

```
   P_q(r)  :=   Σ_{ρ : φ_q(ρ)=∞,  Re ρ < ½ }   2 d_ρ / ( d_ρ² + (r − γ_ρ)² )     ≥ 0,
```

we have the identity

```
   − (φ'_q/φ_q)(½ + ir)  =  P_q(r)  −  Σ_k 2(s_k−½)/((s_k−½)² + r²)  +  A_Γ(r).       (1.4)
```

**`A_Γ(r)` is the archimedean/elementary factor** — the part of `−φ'/φ` coming from the
non-Blaschke factors of the Hadamard product. For a one-cusp weight-0 group the Eisenstein
constant term carries a factor `√π Γ(s−½)/Γ(s)` (cf. `LAW_ANCHOR_T1_THETA.md` §2, M1F (3.2)),
whose logarithmic derivative at `s = ½+ir` is `−[ψ(ir) − ψ(½+ir)] = O(1/|r|)`; the remaining
factor is a Dirichlet series whose entire growth is carried by its zeros, i.e. already inside
`P_q`. So:

> **`|A_Γ(t₀)| ≤ 1/(2|t₀|) + o(1/|t₀|)`, hence `≤ 0.25` for `t₀ ≥ 2`.** — **`GAP`**, obligation
> **N-B4b**: this is the one place a `q`-dependent unbounded term could hide. The Γ-factor is
> manifestly `q`-independent (one cusp, weight 0, same gamma factor for every `q`), which is why
> this is expected to be harmless; but "expected" is not "proved". §5 carries `A_Γ` explicitly as
> a named slack so the reader can see exactly what it costs (`+0.25` in the numerator of `log Q₀`,
> i.e. `Q₀: 1268 → 1465`).

### 1.5 Why the coefficient discrepancy does not matter

Lemma 5.3 subtracts `(1 − s_k)/((s_k−½)² + r²)`; identity (1.4) produces `2(s_k − ½)/(⋯)`. These
agree only at `s_k = 2/3`, so **one of them is not what I think it is** (most likely a
transcription artifact per N-B4, or a different normalization of `s_k`). **This is recorded as a
live discrepancy, not smoothed over.**

**It is nonetheless non-load-bearing, for a reason that is worth stating explicitly.** For
`s_k ∈ (½, 1]`, both candidate numerators are `≥ 0`:
`1 − s_k ∈ [0, ½)` and `2(s_k − ½) ∈ (0, 1]`. And in both readings the exceptional term is
**subtracted from the left-hand side**. So in either case, combining Lemma 5.3 with (1.4) and
discarding a non-negative quantity gives the same consequence:

> ### **(B4★)   `P_q(r)  ≥  2 log q  −  A_Γ(r)`   for every real `r` and every `q`.**
>
> **[`PROVED-here` from `PROVED-cited` Lemma 5.3 + `PROVED-here` (1.4) + `GAP` N-B4b]**

This is the **only** input Route B needs from the trace formula. Note what it is not:

- It is **not** an average over a window; it holds **pointwise in `r`**.
- It has **no unknown constant**. `2 log q` is exact, with `q` the Hecke index (§1.2(d)).
- It does **not** require B1, B2, or B3. **Route B should be re-based on (B4★) and B3 dropped.**
  B3's `0 < C < 1` mean-value point and its `O(1)` / `O((log Q)^{3/4})` remainders — three
  `UNKNOWN` entries in the skeleton's constants table — leave the critical path entirely.

---

## 2. The target statement

Fix a **depth cut** `δ₀ ∈ (0, ½)` and a height `t₀`. Define the target box

```
   B(δ₀, t₀)  :=  [ ½ − δ₀ ,  ½ )  ×  [ t₀ − 1 ,  t₀ + 1 ].
```

**LAW-B(`δ₀`, `t₀`, `q`):** *`φ_q` has a pole in `B(δ₀, t₀)`.*

**Relation to Hejhal Thm 7.11.** Hejhal's conclusion (quoted verbatim in the skeleton §0(a), and
re-fetched here from the same source: "*Given `t₀ ∈ R` and `0 < δ < 1`, the rectangle
`[1/2, 1/2+δ] × [t₀−δ, t₀+δ]` must contain zeros of `φ_N(s)` and the rectangle
`[1/2−δ, 1/2] × [t₀−δ, t₀+δ]` must contain poles of `φ_N(s)` when `N` is sufficiently large*") is
**LAW-B with the height half-width tied to `δ₀` and both sent to `0`**. What is proved below is
weaker in shape — the height half-width is pinned at `1`, not `δ`, and the depth cut is pinned at
the measured `δ₀ = 0.2`, not arbitrary — and **stronger in kind**, because `Q₀` is a number.

**Do not overstate the conclusion.** For a *fixed* cofinite group, every pole of `φ` off the real
axis already lies in `Re s < ½` (unitarity + `φ(s)φ(1−s) = 1`). The content is **localization in
height and depth, uniformly in `q`, with an effective threshold** — not the bare existence of an
off-line pole. The skeleton §6 makes this point; it is repeated here because it is the single
easiest place for the programme to inflate its own result.

---

## 3. The measured inputs

**[`MEASURED` throughout — `NON-RIGOROUS PROBE`, float argument-principle windings on midpoint
evaluations of the Arb-ball transfer-operator builders at 128-bit precision; no certified ball
enclosure, no certified dimension tail. See `LAW_ROUTEB_DEEPCOUNT.md` §2.]**

Window `Im s ∈ [2, 12]` (height 10), both sign sectors summed, best available `N` per cell.

### M1 — deep count, `δ₀ = 0.2` (i.e. `Re s < 0.3`)

| `q` | 5 | 7 | 8 | 9 | 10 | 11 | 12 | 15 | 18 | 21 |
|----|---|---|---|---|----|----|----|----|----|----|
| count `Re s < 0.3`, height-10 window | 1 | 3 | 3 | 3 | 4 | 3 | **5** | 4 | 4 | 3 |

Maximum `5`, attained at `q = 12`, **not** at the largest `q`. The two largest `q` read `4` and
`3` at `N = 16` (`LAW_ROUTEB_Q18Q21.md` §5, STEP-CONFIRMED). Converted to the form the argument
consumes — a count in a **width-2** interval `|Im s − t₀| ≤ 1`:

> ### **`C(δ₀ = 0.2) ≈ 1.0`.**   `MEASURED`. Obligation: **prove it** (§6).

### M2 — shallow count

Shallow stratum `[0.4, 0.487)` in the height-10 window, fit over `q ≥ 7`:
`−0.908 + 2.139·log q`, `R² = 0.418`.
Total count in the window, fit over `q ≥ 7`: `5.744 + 2.009·log q`, `R² = 0.276`.

**The conservative reading is used below**, because the measurement's shallow stratum
`[0.4, 0.487)` is *narrower* than the argument's shallow band `Re ∈ (0.3, 0.5)` — it omits both
`[0.3, 0.4)` and the uncounted sliver `Re > 0.487`. Bounding the shallow band by the **total**
count and converting to a width-2 interval (divide the height-10 figure by 5):

> ### **`S_q ≤ a + b·log q` per width-2 interval, with `a = 1.149`, `b = 0.402`.**
> `MEASURED`, and **an upper bound only in the measured window** — the sliver `Re ∈ (0.487, 0.5)`
> was never counted, so even this is not a true upper bound. Named as **`GAP` B5b-sliver** in §6.

### M3 — what is measured about `t₀`-dependence

**Nothing.** Every count above is in the single window `Im s ∈ [2, 12]`. `t₀`-uniformity — which
the theorem asserts for all `t₀` — is **unprobed** in the entire lane. `GAP`.

---

## 4. The pigeonhole, derived

**[`PROVED-here` throughout §4, from (B4★) and the labelled counting hypotheses.]**

Assume, for contradiction, that **`B(δ₀, t₀)` is empty**: no pole of `φ_q` has both `d_ρ < δ₀` and
`|γ_ρ − t₀| ≤ 1`. Evaluate (B4★) at the single point `r = t₀` and split `P_q(t₀)` by the two
criteria. Every pole falls into exactly one of three classes.

Shells: for `n ≥ 1` let `Sh_n := {ρ : n ≤ |γ_ρ − t₀| < n+1}`, and `Sh_0 := {|γ_ρ − t₀| < 1}`. Each
shell is an interval of total height `2`, so each contains at most one width-2 interval's worth of
poles — this is why the counting hypotheses are stated per width-2 interval.

### 4.1 Class I — deep poles, near (`d_ρ ≥ δ₀`, `ρ ∈ Sh_0`)

Kernel bound: `2d/(d² + (γ−t₀)²) ≤ 2d/d² = 2/d ≤ 2/δ₀`.
Count: `≤ C` by hypothesis (B5-bound).

```
   Class I  ≤  2C/δ₀.
```

### 4.2 Class II — deep poles, far (`d_ρ ≥ δ₀`, `ρ ∈ Sh_n`, `n ≥ 1`)

Kernel bound: `2d/(d² + (γ−t₀)²) ≤ 2d/n² ≤ 1/n²`, using `d ≤ ½` (a pole with `Re ρ < 0` is
excluded by the standard resonance geometry; if one wished to allow `Re ρ < 0`, replace `½` by the
relevant bound and the constant `π²/6` scales linearly).
Count per shell: `≤ C`.

```
   Class II  ≤  C · Σ_{n≥1} 1/n²  =  C · π²/6  =  1.6449 C.
```

### 4.3 Class III — shallow poles, far (`d_ρ < δ₀`, `ρ ∈ Sh_n`, `n ≥ 1`)

*(By the contradiction hypothesis, shallow-and-near is empty; this class is what the skeleton's
B5 omitted.)*

Kernel bound: `2d/(d² + (γ−t₀)²) ≤ 2d/n² < 2δ₀/n²`. **The factor `δ₀` is the whole reason this
class is controllable**: shallow poles are numerous (their count grows like `log q`) but each one
is *shallow*, and the far field of a Poisson kernel is proportional to its width.
Count per shell: `≤ S_q = a + b log q`.

```
   Class III  ≤  2δ₀ (a + b log q) · Σ_{n≥1} 1/n²  =  (π²/3) δ₀ (a + b log q)
                                                    =  3.2899 δ₀ (a + b log q).
```

### 4.4 Assembling

By (B4★) and `P_q(t₀) = I + II + III` under the emptiness hypothesis:

```
   2 log q − A_Γ  ≤  2C/δ₀  +  (π²/6) C  +  (π²/3) δ₀ a  +  (π²/3) δ₀ b · log q,
```

i.e.

```
   log q · [ 2 − (π²/3) δ₀ b ]   ≤   C (2/δ₀ + π²/6)  +  (π²/3) δ₀ a  +  A_Γ.     (4.4)
```

**If the bracket on the left is positive**, (4.4) fails for all sufficiently large `q`, and the
emptiness hypothesis is contradicted. That gives the theorem.

> **The positivity of the bracket is a real condition, not a formality.** It requires
> `δ₀ b < 6/π² = 0.6079`. With `b = 0.402` this caps `δ₀ < 1.51` — no constraint in practice. But
> if the shallow density per width-2 interval were `≳ 1.5 log q` rather than `0.4 log q`, the
> bracket would close and **Route B would fail outright at `δ₀ = 0.2`**. The route is alive
> because the shallow poles are sparse *per unit height*, not merely because they are shallow.

---

## 5. The conditional theorem, with `Q₀`

### 5.1 Statement

> ### **THEOREM (Route B, conditional).**
>
> Let `δ₀ ∈ (0, ½)` and `t₀ ≥ 2`. Suppose:
>
> - **(B4★)** `P_q(r) ≥ 2 log q − A_Γ(r)` for all real `r` — **`PROVED-here`** from HJL Lemma 5.3
>   (`PROVED-cited`, `TODO-VERIFY` N-B4) and identity (1.4), **given** obligation N-B4b bounding
>   `|A_Γ(t₀)| ≤ 0.25` for `t₀ ≥ 2`;
> - **(B5-bound)** `#{ρ : φ_q(ρ) = ∞, Re ρ ≤ ½ − δ₀, |Im ρ − t₀| ≤ 1} ≤ C`, uniformly in `q` and
>   `t₀` — **`GAP`**, `MEASURED` at `C(0.2) ≈ 1.0`;
> - **(B5b-bound)** `#{ρ : φ_q(ρ) = ∞, ½ − δ₀ < Re ρ < ½, |Im ρ − t₀| ≤ 1} ≤ a + b log q`,
>   uniformly in `t₀` — **`GAP`**, `MEASURED` at `a = 1.149`, `b = 0.402`;
> - **(bracket)** `(π²/3) δ₀ b < 2`.
>
> **Then** for every `q ≥ Q₀`, `φ_q` has a pole in `[½ − δ₀, ½) × [t₀ − 1, t₀ + 1]`, where
>
> ```
>                    ⎡  C (2/δ₀ + π²/6)  +  (π²/3) δ₀ a  +  A_Γ  ⎤
>      Q₀  =  exp    ⎢ ───────────────────────────────────────── ⎥ .
>                    ⎣            2  −  (π²/3) δ₀ b              ⎦
> ```

### 5.2 The number

At the measured values `δ₀ = 0.2`, `C = 1.0`, `a = 1.149`, `b = 0.402`, `A_Γ = 0.25`:

| term | value |
|---|---|
| `C (2/δ₀ + π²/6)` = `1.0 × (10 + 1.6449)` | `11.6449` |
| `(π²/3) δ₀ a` = `3.28987 × 0.2 × 1.149` | `0.7561` |
| `A_Γ` | `0.2500` |
| **numerator** | **`12.6511`** |
| `(π²/3) δ₀ b` = `3.28987 × 0.2 × 0.402` | `0.2645` |
| **denominator** = `2 − 0.2645` | **`1.7355`** |
| `log Q₀` | **`7.2896`** |

> ### **`Q₀ = 1465`.  Round figure: `Q₀ ≈ 1.5 × 10³`.**

### 5.3 Sensitivity — read this before quoting `Q₀`

`log Q₀` is **linear in `C` with slope `2/δ₀ + π²/6` divided by the bracket**, i.e. `6.71` at
`δ₀ = 0.2`. So `Q₀` moves by a factor of `e^{6.71}` ≈ 820 per unit of `C`:

| `C` | `Q₀` | comment |
|---|---|---|
| 0.5 | 51 | if the true deep count is half the measured value |
| **1.0** | **1465** | **the measured value** |
| 1.4 | `2.1 × 10⁴` | the `δ₀ = 0.1` measured constant, for comparison |
| 2.0 | `1.2 × 10⁶` | |
| 5.0 | `6.6 × 10¹⁴` | |

**`Q₀` is a number, but it is a number about `C`, and `C` is measured, not proved.** A factor-of-2
error in `C` costs six orders of magnitude in `Q₀`. Any statement of the form "the law holds for
`q ≥ 1465`" is **conditional on an unproved counting bound** and must be written that way.

### 5.4 Choice of `δ₀`, and the alternative reading

Varying `δ₀` against the lane's two measured `C` values:

| `δ₀` | `C(δ₀)` | source | `log Q₀` | `Q₀` |
|---|---|---|---|---|
| 0.1 | 1.4 | `LAW_ROUTEB_DEEPCOUNT.md` §6, `MEASURED` | 16.56 | `1.6 × 10⁷` |
| **0.2** | **1.0** | `LAW_ROUTEB_SUBSTRATUM.md` §6 / `Q18Q21.md` §5, `MEASURED` | **7.29** | **1465** |
| 0.3 | ~1.0 | **not measured** — extrapolation only | 6.05 | 423 |

`δ₀ = 0.2` is the right cut and it is the *measured* one: `C(0.2) = 1.0 < 1.4 = C(0.1)`, so moving
the cut deeper improves both `C` and the `2/δ₀` factor. Extending to `δ₀ = 0.25`/`0.3` is
recommended (`LAW_ROUTEB_Q18Q21.md` §8.2) and would likely buy another order of magnitude — but
`C(0.3)` is **not measured** and the row above is extrapolation, labelled as such.

**Narrow-shallow reading.** If one uses the literal measured shallow stratum `[0.4, 0.487)`
(`2.139 log q` per height-10 window, so `a = 0`, `b = 0.428`) instead of the conservative
total-count bound, the numerator drops to `11.6449 + 0.2500 = 11.895` and the denominator rises to
`2 − 0.2816 = 1.7184`, giving `log Q₀ = 6.9221`, **`Q₀ = 1014`**; dropping `A_Γ` as well gives
**`Q₀ = 877`**. These are the optimistic figures. **`Q₀ = 1465` is the one to quote**, because the
conservative reading is the only one that does not silently assume the uncounted band
`Re ∈ (0.3, 0.4) ∪ (0.487, 0.5)` is empty.

### 5.5 What the theorem does not give

1. **Not `t₀`-uniform in evidence.** The statement asserts uniformity in `t₀`; the measurements
   cover `Im s ∈ [2, 12]` only. Both (B5-bound) and (B5b-bound) are stated `t₀`-uniformly and
   **neither is measured that way**. `GAP` (M3).
2. **Height half-width pinned at `1`, not `δ`.** Hejhal's box shrinks in both directions. Shrinking
   the height half-width to `δ < 1` is possible — Class II/III shell sums then start at `n ≈ 1/δ`
   and *improve* — but Class I's count hypothesis must then be restated per width-`2δ` interval,
   where the measured `C` gives no information below width 2. Doing this properly needs a density
   measurement at finer height resolution. Not attempted here.
3. **Poles of `φ_q`, not zeros of `Z_{G_q}`.** The transport pole-of-`φ` ⇒ zero-of-`Z` is the
   repo's obligation **U3** / M1F N2-G6, still `GAP` (`LAW_ANCHOR_T1_THETA.md` C14). Route B's
   conclusion is a **scattering** statement. That is what Hejhal 7.11 also is, so no ground is
   lost — but the flagship's Selberg-zero framing needs U3 regardless of which route supplies it.
4. **Nothing at all below `Q₀`.** For `q = 5 … 21` — the entire certified range of the repo — this
   theorem says nothing. Those `q` are covered, if at all, by direct Aletheia certification, not
   by this argument. The two are complementary, not redundant (§6.4).

---

## 6. What would prove B5, and the recommended lane

The route now rests on two counting bounds, **B5** (deep, `q`-uniform, `O(1)`) and **B5b**
(shallow, `O(log q)`). B5 is the hard one. Candidates, assessed:

### 6.1 Repo tooling — what it can and cannot do

- **U2b counting theorems** (`LAW_U2B_CLOSURE.md`: `sys(G_q) = 2 arccosh λ_q ≥ 2.1226`;
  `sup_{q≥5} Σ e^{−σℓ}/(1−e^{−ℓ}) ≤ 0.4861` for `σ ≥ 3.5`; `|Z| ≤ 1.6259`). **These bound the
  LENGTH side** — the geodesic/Euler-product half of the Selberg zeta function, in `Re s > 1`.
  They are exactly the wrong side of the functional equation for a resonance count in
  `0 < Re s < ½`, and they do not transfer without the growth bound U1 that Route B exists to
  avoid. **Cannot prove B5.** They are, however, the right *template* — see §6.3.
- **Aletheia winding certificates** (`engine/certify/`, argument-principle Arb enclosures,
  validated at `q = 3, 5, 7`). **These can CERTIFY a per-`q` count for a finite range**, turning
  the `MEASURED` rows of §3 into theorems for those specific `q`. They are the correct instrument
  for the base case and for promoting `LAW_ROUTEB_DEEPCOUNT.md` §3 out of `NON-RIGOROUS PROBE`.
  **They cannot say anything about all `q`** — every certificate is one group.
- **Weyl law via area.** `|F_q| = π(1 − 2/q) ≤ π` is `PROVED`, giving `N_q(T) + M_q(T) ~
  (|F_q|/4π)T²` with a `q`-uniform leading constant. This bounds the **total** count in a height
  window, `q`-uniformly. It is genuinely useful for **B5b** — a `q`-uniform Weyl upper bound
  would replace the `MEASURED` `(a, b)` with proved constants — but it is far too crude for **B5**,
  since it does not see depth at all: it would bound the deep count by the total, which grows.

### 6.2 The degeneration route (`b_q → 0`, T1) — why it recovers Hejhal but not `Q₀`

The most conceptually satisfying candidate, and the one the brief names:
as `λ_q ↑ 2` the elliptic point opens into a cusp, `G_q → Γ_θ`, and `φ_q → φ_θ` locally uniformly
(skeleton A2). By **T1** (`LAW_ANCHOR_T1_THETA.md`, `PROVED`), the limit's poles are exactly
`{ρ/2 : ζ(ρ) = 0}` together with the simple poles at `ikπ/log 2` on `Re s = 0` (per the 2026-08-16
erratum), and the `ρ/2` family carries **order `2·m(ρ)`**, the order-2 structure the brief
recalls. By Riemann–von Mangoldt the set `{ρ/2}` has density `(1/π) log(2t)` per unit height at
height `t` — **finite, `q`-independent, and in the fixed window `Im ∈ [2, 12]` it is a bounded
number**. Locally uniform convergence plus Hurwitz then gives:

> for each `δ₀` and each compact height window, `D_q(δ₀) ≤ D_θ(δ₀) + ε` for all `q ≥ q₁(δ₀, t₀)`.

**This is a genuine proof of B5 in shape** — and it is why the measured flatness of the deep count
is not a coincidence: the deep poles are converging to `Γ_θ`'s fixed lattice. But:

1. `q₁(δ₀, t₀)` is **ineffective** without a rate on A2 — which is exactly **U1-eff**, the blocker
   Route B was built to bypass. Feeding an ineffective `q₁` into §5 yields an ineffective `Q₀`,
   i.e. **Hejhal's theorem again, with extra steps**. Circular for the effective goal.
2. The convergence `φ_q → φ_θ` at `Re s ≈ 0.3` is precisely the regime where nothing is proved
   (U2a covers `Re s > 1` only).

**Verdict: the right explanation, the wrong proof.** It should be written into the programme as
the *reason to believe* B5, and it makes B5 a credible conjecture rather than a hopeful one. It
must not be presented as a route to an effective `Q₀`.

### 6.3 Resolvent / Fadeev–Pavlov, and the recommended lane

Classical resonance-counting technology (Fadeev–Pavlov; Guillopé–Zworski; Selberg's own
`N + M ~ cT²`) delivers **upper bounds on total resonance counts in discs**, via a Jensen-type
argument applied to an entire function whose zeros are the resonances. The obstruction to using it
here has always been that the natural such function is `Z_{G_q}`, and the required `q`-uniform
growth bound is U1.

**But Route B does not have to use `Z_{G_q}`.** The measurement lane already counts deep
resonances as zeros of the **Mayer transfer-operator determinant** `det(1 − L_{s,±})`, using the
MMS identity (arXiv:0912.2236)

```
   Z_S(s) = det[(1 − L_{s,+})(1 − L_{s,−})] / det(1 − K_s),     det(1 − K_s) zero-free on Re s > 0,
```

so on `0 < Re s < ½` the two sectors' zero counts **sum exactly to the resonance count**
(`LAW_ROUTEB_DEEPCOUNT.md` §2, and the sector observation that all deep occupancy sits in
`sign = +1`). This changes the problem completely:

> ### **Recommended single next lane — B5-J: Jensen counting on the transfer-operator determinant.**
>
> Prove `q`-uniform bounds
>
> - **(upper)** `sup_{s ∈ D} |det(1 − L_{s,±})| ≤ M`, on a fixed disc `D ⊂ {0 < Re s < ½}`
>   covering the deep region and the height window;
> - **(lower)** `|det(1 − L_{s*,±})| ≥ m > 0` at one interior point `s*`;
>
> both `q`-uniform. **Jensen's formula then bounds the zero count in a smaller concentric disc by
> `log(M/m)/log(R/r)` — which is exactly `C(δ₀)`, and it is explicit.**

Why this is the right lane, and not another restatement of U1:

1. **The determinant is entire of order 0** in `s` for these nuclear operators — no Hadamard
   growth theorem is needed, no Phragmén–Lindelöf, no U1. Jensen alone suffices.
2. **The region is the friendly one.** `0 < Re s < ½` is where the Mayer operator is most
   convergent and where the repo's builders already evaluate to `10⁻¹⁵` residuals. U1-eff's
   difficulty was carrying `Re s > 1` estimates *down* to `Re s ≈ ¼`; here one works in the strip
   natively.
3. **`q` enters only through `λ_q ∈ [1, 2)`, a bounded parameter.** A `q`-uniform sup-norm bound
   is a statement about a one-parameter family of explicit kernels on a compact parameter range —
   the same shape as the `PROVED` U2b estimates (`sup_{q≥5} Σ e^{−σℓ}/(1−e^{−ℓ}) ≤ 0.4861`),
   which is the evidence that this style of bound is achievable in this repo.
4. **The lower bound at one point is the delicate half**, and it is measurable *now*: the existing
   receipts already record `min |det|` on every contour (`0.0627` at `q = 18`, `0.0408` at
   `q = 21` — `LAW_ROUTEB_Q18Q21.md` §3), i.e. the empirical `m` is already in hand and is not
   collapsing with `q`. That is a free pre-registration for the lane.
5. **It also delivers B5b.** The same Jensen bound on a larger disc bounds the *total* count,
   which is what B5b needs, replacing the `MEASURED` `(a, b)` with proved constants.

### 6.4 The finite range, and how the two halves compose

B5-J, if it succeeds, will most naturally give `C` for `q ≥ q₂` with an explicit but possibly
large `q₂`. The complement `5 ≤ q < q₂` is then a **finite** list of groups, each of which the
**Aletheia `winding_box` path can certify individually** — this is `LAW_ROUTEB_DEEPCOUNT.md` §8.2
and `LAW_ROUTEB_SUBSTRATUM.md` §8.4, already on the board (`q = 9` recommended first, being stable
across `N = 12, 16, 20`). Finite certification + eventual theorem = the bound for all `q`. Neither
half is sufficient alone; **both are already scoped in this lane**, which is the strongest
practical argument for B5-J over any route requiring U1.

### 6.5 Ranked next steps

1. **B5-J (recommended).** Jensen counting on `det(1 − L_{s,±})`: `q`-uniform sup-bound on a disc
   in `0 < Re s < ½` plus a one-point lower bound. Frontier + Aristotle-able in pieces. This is
   the only candidate that yields an **effective, `q`-uniform** `C`.
2. **N-B4 and N-B4b (cheap, blocking).** Verify HJL Lemma 5.3 against the journal PDF or arXiv
   source (§1.1), and prove the `A_Γ` bound (§1.4). Both are small; both are currently
   `TODO-VERIFY`/`GAP` on the *input* side of a chain whose output is being quoted as a number.
   **Do these before anyone cites `Q₀ = 1465`.**
3. **Certify one row** (`q = 9`) through the Arb `winding_box` path — converts one `MEASURED` cell
   to a theorem and validates the probe against the certified engine.
4. **`t₀`-dependence** (M3): repeat one `q` in a second height window. Currently the single
   largest unexamined assumption in the theorem statement.
5. **`δ₀ = 0.25 / 0.3` sweep** — would move `Q₀` from `1465` toward `~420` if `C` holds.
6. **Do not** re-base on B3. §1.5: (B4★) supersedes it and removes three `UNKNOWN` constants.

---

## 7. Consolidated status ledger

| # | Step | Statement | Status |
|---|---|---|---|
| B4.1 | HJL Lemma 5.3 | `−(φ'/φ)(½+ir) − Σ_k (1−s_k)/((s_k−½)²+r²) ≥ 2 log q_M > 0` | **`PROVED-cited`** (HJL 97 L.5.3 / He 83 p.160, via G–J §5); **`TODO-VERIFY` N-B4** (transcription channel) |
| B4.2 | `q_M = q` for `G_q` | degenerating elliptic order `= q`; orders 2, 3 fixed | **`PROVED-here`** from G–J Ex. 5.8 |
| B4.3 | Poisson identity (1.4) | pole at depth `d` ⇒ `+2d/(d²+(r−γ)²)`; exceptional `s_k∈(½,1]` ⇒ negative | **`PROVED-here`** |
| B4.4 | `A_Γ` bounded, `q`-independent | `\|A_Γ(t₀)\| ≤ 0.25` for `t₀ ≥ 2` | **`GAP`** — obligation N-B4b |
| B4.5 | coefficient discrepancy `1−s_k` vs `2(s_k−½)` | live, unresolved | **`TODO-VERIFY`**; non-load-bearing (§1.5, both `≥ 0`) |
| **B4★** | **`P_q(r) ≥ 2 log q − A_Γ`, pointwise, no unknown constant** | | **`PROVED-here`** given B4.1 + B4.4 |
| B5 | deep count `≤ C`, `q`- and `t₀`-uniform, `δ₀ = 0.2` | `C(0.2) ≈ 1.0` | **`GAP`**; **`MEASURED`** (10 groups, one window, non-certified) |
| B5b | shallow count `≤ a + b log q`, `t₀`-uniform | `a = 1.149`, `b = 0.402` | **`GAP`**; **`MEASURED`**, and not a true upper bound (sliver `Re ∈ (0.487, ½)` uncounted) |
| B5c | bracket `(π²/3)δ₀ b < 2` | `0.2645 < 2` ✓ | **`PROVED-here`** given B5b |
| B6 | Classes I/II/III bounds and (4.4) | `2C/δ₀ + (π²/6)C + (π²/3)δ₀(a+b log q)` | **`PROVED-here`** |
| B7 | `Q₀` formula and `Q₀ = 1465` | §5.1–5.2 | **`PROVED-here`** given B4★, B5, B5b |
| — | `t₀`-uniformity of B5 / B5b | asserted, unprobed | **`GAP`** (M3) |
| — | pole of `φ_q` ⇒ zero of `Z_{G_q}` | | **`GAP`** — repo U3 / M1F N2-G6, unchanged |
| — | B3 (`G_{M_q,0}` asymptotic, `0<C<1`, `O((log Q)^{3/4})`) | | **removed from the critical path** (§1.5) |

---

## 8. What this document claims, and does not

**Claims.** (i) The Route-B chain is complete and the arithmetic closes, giving an explicit
`Q₀(C)` formula and, at the measured `C(0.2) ≈ 1.0`, the number `Q₀ = 1465`. (ii) The positivity
input is pointwise and constant-free, so B3 leaves the critical path and three `UNKNOWN` constants
go with it. (iii) The bookkeeping question is answered: `−φ'/φ` counts poles of `φ` only; cusp
eigenvalues never enter it; the `Σ_k` term removes the residual poles in `(½, 1]`, and all removed
terms are non-negative, which is why the transcription discrepancy of §1.5 is survivable.
(iv) Route B needs a **second** counting bound, B5b, that the skeleton did not name and the
measurement lane did not test. (v) The `b_q → 0` degeneration to `Γ_θ`'s order-2 `{ρ/2}` pole
lattice explains *why* B5 should be true but cannot yield an effective `Q₀` without U1-eff.
(vi) The one candidate that can is Jensen counting on the transfer-operator determinant, B5-J.

**Does not claim.** That the law holds for any `q`. That `C(0.2) = 1.0` — it is a float-winding
measurement on ten groups in one height window, explicitly `NON-RIGOROUS PROBE`. That `Q₀ = 1465`
is unconditional; it is conditional on two unproved counting bounds and one unverified archimedean
bound, and it moves by six orders of magnitude if `C` is off by a factor of two. That anything
here is `t₀`-uniform in evidence. That Hejhal's proof is known — §2 and the reconstruction in §1.4
inherit the parent skeleton's `RECONSTRUCTED` label. No novelty is claimed for HJL Lemma 5.3, for
the Poisson representation, or for the Jensen-counting idea; the contribution here is the
assembly, the constants, and the two named gaps.

---

**Sources.** arXiv:1603.01494 (Garbin–Jorgenson, *Spectral asymptotics on sequences of
elliptically degenerating Riemann surfaces*, L'Enseign. Math. 64 (2018) 161–206) — full text read
via ar5iv; Huntley–Jorgenson–Lundelius, J. Funct. Anal. **149** (1997) 58–82, Lemma 5.3 (quoted
through S1, not read directly); Hejhal, LNM 1001 vol. 2 (1983), p. 160 and Thm 7.11 / Cor 7.12
(**not consulted** — blocked HITL library item; the constraint of the parent skeleton is honoured);
arXiv:0912.2236 (MMS, the transfer-operator determinant identity); repo: `LAW_ANCHOR_T1_THETA.md`,
`LAW_U2B_CLOSURE.md`, `LAW_ROUTEB_{DEEPCOUNT,SUBSTRATUM,Q18Q21}.md`,
`LAW_SH_EFFECTIVIZATION_SKELETON.md`.

No git was run. No existing file was modified.
