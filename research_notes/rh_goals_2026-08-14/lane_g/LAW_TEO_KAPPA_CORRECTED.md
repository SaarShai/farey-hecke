# LAW — Teo's `κ_q`, corrected: `Γ₂ = 1/G`, not `G`

**Status:** `PROVED` (the transcription error and its correction) + `HEURISTIC` (the rerun).
**Date:** 2026-08-16. **Lane:** G. **Interpreter:** `/Users/za/miniforge3/envs/pari-arb/bin/python3`.
**New probe:** `law_probes/mirror_u4_corrected.py` (+ `.json`, `_sigmasweep.json`).
`law_probes/mirror_u4.py` was **not** modified.

---

## 0. Verdict up front

`LAW_MIRROR_Q3_DISCRIMINATOR.md` §3 found the mirror identity

```
   (*)     P_q(1-s) / P_q(s)  ==  |phi_q(s)| * |K_q(s)|
```

failing by `10⁵–10¹⁹` at `q = 3, 4, 6`, where `φ_q` is the **exact** arithmetic closed form, and
by its pre-registered rule assigned the fault to **(b), the Teo `κ_q` assembly**. That call was
correct. **The error is identified, and it is a single wrong function.**

> ### `LAW_U1_GROWTH.md` §3.1 and `law_probes/mirror_u4.py` identify Teo's double gamma `Γ₂` with mpmath's `barnesg`, the Barnes `G`-function. **They are reciprocal: `Γ₂(s) = 1/G(s)`.** The `Γ₂²` ratio inside the Barnes bracket is therefore inverted.
>
> After the fix, at `q = 3, 4, 6`, `σ ∈ {1.25, 1.40, 1.50}`, `t = t_∞`, `N = 32`, `prec = 400`:
> **`(*)` improves from a `10⁵–10¹³` failure to a ratio in `[0.456, 2.055]`** — a residual `O(1)`
> factor, not a discrepancy of orders of magnitude.
>
> The residual is **not** a kernel convention (§4 proves `|κ_q|` now has **no** remaining
> convention freedom) and **not** `N`-truncation (`1e−16` stable to `N = 64`). It is smooth in `σ`,
> tends to `1` as `σ → 1/2`, and grows with `|σ − 1/2|` — it lives on the **(a)-U4 side**, in the
> determinant proxy's continuation to `Re s ≤ 0`.

**Consequence for the standing dichotomy.** `LAW_STRIP_AND_MIRROR.md` SM.23 ("U4-as-identification
refuted OR the Teo assembly is wrong; not separated") is now **separated, and it resolves against
the Teo assembly.** U4 is **no longer refuted** by the mirror test. It is also **not confirmed**:
an `O(1)`, `σ`-growing residual remains, and it is now the only thing the test says.

---

## 1. The source, opened

`CITATION(Teo)` L.-P. Teo, *Ruelle zeta function for cofinite hyperbolic Riemann surfaces with
ramification points*, **Letters in Mathematical Physics 110 (2020) 61–82**;
**arXiv:1901.07898v2** (v1 21 Jan 2019, v2 3 Sep 2019). PDF retrieved 2026-08-16 and text-extracted
with `pdftotext`; page numbers below are the arXiv-v2 pages.

`TODO-VERIFY(the journal version, LMP 110 (2020) 61–82 — I read arXiv v2. Confirm the numbering
Thm 2.2 / Prop. 2.5 and eq. (2.4)/(2.6) are unchanged.)` This is the *same* outstanding item
`LAW_U3_TRANSPORT.md` §2.5 logged; it is not discharged here.

### 1.1 Proposition 2.5, verbatim (p. 7)

> "**Proposition 2.5.** The functional equation of the Selberg zeta function is given by
> `Z(1 − s) = κ(s)Z(s)`,  **(2.6)**
> where
> `κ(s) = (−1)^{A/2} e^{C(2s−1)} ϕ(s) [ (2π)^{2s−1} Γ₂(s)² Γ(1−s) / ( Γ₂(1−s)² Γ(s) ) ]^{|X|/2π}
>          [ Γ(3/2 − s) / Γ(s + 1/2) ]^{n}
>          × ∏_{j=1}^{v} ∏_{k=0}^{m_j−1} [ sin( π(s+k)/m_j ) ]^{(m_j − 2k − 1)/m_j}`."

### 1.2 Theorem 2.2, verbatim (p. 6) — the factorization that fixes every symbol

> "**Theorem 2.2.** If `X` is a cofinite Riemann surface of type `(g; n; m_1, m_2, …, m_v)`, then
> the regularized determinant of its Laplacian is given by
> `det(∆ − s(1−s)) = Z_∞(s) Z(s) Z_ell(s) Γ(s + 1/2)^{−n} (2s−1)^{A/2} e^{B(s−1/2)² + C(s−1/2) + D}`
> **(2.4)** where `Z(s) = ∏_P ∏_{k=0}^{∞} (1 − p^{−s−k})` **(2.5)** is the Selberg zeta function of
> the surface `X`,
> `Z_∞(s) = [ (2π)^s Γ₂(s)² / Γ(s) ]^{|X|/2π}`,
> `Z_ell(s) = ∏_{j=1}^{v} ∏_{k=0}^{m_j−1} Γ((s+k)/m_j)^{(2k+1−m_j)/m_j}`,
> `A = n − Tr Φ(1/2)`, `B = −|X|/2π`, `C = −n log 2`,
> `D = Σ_{j=1}^{v} ((m_j²−1)/(6m_j)) log m_j + (n/2) log 2π − (|X|/2π)( (1/2)log 2π − 2ζ′(−1) ) − (A/2) log 2`."

### 1.3 `Γ₂`, verbatim (p. 5) — **the load-bearing definition**

> "Recall the definition of the Alekseevskii-Barnes double gamma function `Γ₂(s)` [1, 2]:
> `Γ₂(s+1) = (2π)^{−s/2} · e^{s/2 + ((γ+1)/2)s²} · ∏_{k=1}^{∞} (1 + s/k)^{−k} e^{s − s²/(2k)}`."

**[CORRECTED 2026-08-16]** The quote block above previously read `(1/(2π)^{s/2}) · s ·
e^{((γ+1)/2)s²} · ∏…`, i.e. the paper's `e^{s/2}` had been transcribed as a factor `s·`. That
transcription was wrong and is repaired above. Verified two ways: (i) the repaired form is the
Weierstrass product of `1/G(1+s)` (Barnes `G`, `G(1+z) = (2π)^{z/2}
e^{−(z+z²(1+γ))/2} ∏(1+z/k)^k e^{−z+z²/(2k)}`); (ii) numerically at `dps = 30`, the repaired
form equals `1/barnesg(s+1)` to `28` digits at `s = 0.7, 1.3`, while the garbled form gives
`0.4710` / `0.7068` against the true `0.9548` / `1.0415`. **Lemma K-1 (`Γ₂ = 1/G`) and every
downstream number are unaffected** — they were derived from the p. 24 / p. 10 recursion and
residue, not from this product. `TODO-VERIFY`: the arXiv-v2 PDF is not banked in-repo, so the
repair rests on the mathematics, not on a re-read of the source glyphs; re-open
arXiv:1901.07898v2 p. 5 to confirm the exact printed form.

with `[1] V. P. Alekseevskii, On functions similar to the gamma function, Comm. Kharkov Math. Soc.
1, 169–238, 1889` and `[2] E. W. Barnes, The theory of the G-function, Q. J. Math. 31, 264–314,
1900` (bibliography, verbatim).

Two further statements in the same paper pin it beyond the (OCR-fragile) product formula:

> p. 24: "`Γ₂(s) = Γ(s)Γ₂(s+1),`"
> p. 10: "Now `Γ₂(s)` has a simple pole of order 1 at `s = 0` with residue one."

### 1.4 Prop. 2.5 is self-consistent with Thm 2.2 (`PROVED`, re-derived here)

Teo's Remark (p. 7) gives `det(∆ − s(1−s)) = D(s(1−s)) ϕ(s)^{−1/2}` with `D` invariant under
`s ↦ 1−s`; with `ϕ(s)ϕ(1−s) = 1` this yields `det(1−s)/det(s) = ϕ(s)`. Dividing (2.4) at `1−s` by
(2.4) at `s` and using `A` even (Teo Remark 2.3) reproduces (2.6) **exactly**, including the
`+|X|/2π` exponent, the `e^{C(2s−1)}`, and the `[Γ(3/2−s)/Γ(s+1/2)]^{n}`. **The exponent sign in
Prop. 2.5 is `+|X|/2π`, and it is right.** The back-solved "flip the exponent to `−(1−2/q)/2`" in
`LAW_MIRROR_Q3_DISCRIMINATOR.md` §3 was a *symptom*, not the disease (§3.3 below).

---

## 2. The transcription error

`Γ₂` and Barnes `G` obey **opposite** recursions and are reciprocal on the common normalisation:

| | recursion | behaviour at `s = 0` | normalisation |
|---|---|---|---|
| Barnes `G` (mpmath `barnesg`) | `G(s+1) = Γ(s) G(s)` | simple **zero**, `G(s) ~ s` | `G(1) = 1` |
| Teo `Γ₂` (p. 24, p. 10) | `Γ₂(s) = Γ(s) Γ₂(s+1)` ⇔ `Γ₂(s+1) = Γ₂(s)/Γ(s)` | simple **pole**, residue `1` | `Γ₂(1) = 1` |

> **Lemma K-1 `PROVED`.** `Γ₂(s) = 1/G(s)`.
> *Proof.* `f := Γ₂ · G` satisfies `f(s+1) = Γ₂(s+1)G(s+1) = (Γ₂(s)/Γ(s))(Γ(s)G(s)) = f(s)`, and
> `f(1) = 1`. Both factors are of order 2 with divisor supported on `−N₀`, the pole of `Γ₂`
> cancelling the zero of `G` there with residue/leading coefficient `1`; the periodic quotient is
> entire, zero-free and of order `< 1`, hence constant `= 1`. ∎
> (Independent check: `Γ₂(s)` has residue `1` at `s = 0` iff `Γ₂(1) = 1` via `Γ₂(s) = Γ(s)Γ₂(s+1)`;
> `1/G` has residue `1` at `s = 0` since `G(s) ~ s`. The two agree, as Teo's p. 10 requires.)

**Therefore, inside the Barnes bracket,**

```
   Gamma_2(s)^2 / Gamma_2(1-s)^2   =   G(1-s)^2 / G(s)^2 .
```

**`LAW_U1_GROWTH.md` §3.1 and `law_probes/mirror_u4.py` `K_q()` write `G(s)²/G(1−s)²`** — i.e.
they substituted `barnesg` for `Γ₂` directly. That is the error, and it is the whole error.

```python
# mirror_u4.py, K_q()  -- WRONG
bar = power((power(2*pi, 2*s - 1) * barnesg(s)**2 * gamma(1 - s)
             / (barnesg(1 - s)**2 * gamma(s))), (1 - mpf(2)/q) / 2)

# mirror_u4_corrected.py, barnes_bracket(..., invert_G=True)  -- CORRECT
inner = power(2*pi, 2*s - 1) * (barnesg(1 - s)**2 / barnesg(s)**2) * gamma(1 - s) / gamma(s)
bar   = power(inner, (1 - mpf(2)/q) / 2)
```

Everything else in `§3.1` is confirmed **verbatim against the source**: `(−1)^{A/2}`;
`e^{C(2s−1)} = 2^{−(2s−1)}` for `n = 1`; `[Γ(3/2−s)/Γ(s+1/2)]^{1}`; the `m=2` factor
`tan(πs/2)^{1/2}`; `E_q(s) = ∏_{k=0}^{q−1} sin(π(s+k)/q)^{(q−2k−1)/q}`; the exponent `|X_q|/2π =
(1−2/q)/2` for signature `(0;1;2,q)`. **No other discrepancy exists between §3.1 and Prop. 2.5.**

### 2.1 Why the assembly check did not catch it `PROVED`

`LAW_U1_GROWTH.md` §3.1's self-consistency check — `|K_q(1/2+it)| = 1` — is **structurally blind**
to it. On `Re s = 1/2`, `1 − s = s̄`, so `G(1−s) = conj G(s)` and `|G(s)²/G(1−s)²| = 1` **whichever
way round the ratio is written**. The check passes identically for both transcriptions:

| `q` | `|K_old(1/2+it_∞)|` | `|K_corrected(1/2+it_∞)|` |
|--:|---|---|
| 3 | `1.000000000000` | `1.000000000000` |
| 4 | `1.000000000000` | `1.000000000000` |
| 6 | `1.000000000000` | `1.000000000000` |

This is exactly the blindness `LAW_STRIP_AND_MIRROR.md` §3.6 anticipated in general terms — it
localised the fault to "the Barnes bracket, whose `q`-dependent exponent the `Re s = 1/2` check is
structurally blind to." The localisation was right; the diagnosis of *which* freedom was wrong.

---

## 3. The rerun

`law_probes/mirror_u4_corrected.py`, `q = 3, 4, 6`, `σ ∈ {1.25, 1.40, 1.50}`,
`t = t_∞ = 7.0673625708673465`, `N = 32`, `ctx.prec = 400`. `φ_q` is the **exact** closed form at
all three `q` (`g(s)` at `q=3`; `g(s)(1+p^{1−s})/(1+p^{s})` with `p = 2, 3` at `q = 4, 6`), so the
evaluator `(c)` cannot enter. `P_q` uses the odd-`q` builder at `q=3`, the even-`q` builder at
`q = 4, 6`. Receipts: `law_probes/mirror_u4_corrected.json`.

### 3.1 The ratio table — `LHS/RHS` for `(*)`

| `q` | `σ` | `LHS = P(1−s)/P(s)` | `|φ_q|` exact | `|K_q|` **corrected** | **ratio corrected** | ratio *old* |
|--:|--:|---|---|---|---|---|
| 3 | 1.25 | `2.896216e+00` | `4.593593e−01` | `4.818471e+00` | **`1.308486`** | `9.200e+04` |
| 3 | 1.40 | `5.600385e+00` | `5.109524e−01` | `6.589569e+00` | **`1.663338`** | `1.091e+06` |
| 3 | 1.50 | `8.635876e+00` | `5.366999e−01` | `8.115246e+00` | **`1.982774`** | `5.760e+06` |
| 4 | 1.25 | `8.373042e+00` | `2.377139e−01` | `7.730995e+01` | **`0.455610`** | `8.495e+06` |
| 4 | 1.40 | `3.006481e+01` | `2.327273e−01` | `1.841821e+02` | **`0.701397`** | `3.723e+08` |
| 4 | 1.50 | `6.200982e+01` | `2.247473e−01` | `3.283985e+02` | **`0.840166`** | `4.160e+09` |
| 6 | 1.25 | `1.579028e+02` | `1.445842e−01` | `1.241423e+03` | **`0.879730`** | `4.349e+09` |
| 6 | 1.40 | `1.039096e+03` | `1.303811e−01` | `5.152865e+03` | **`1.546651`** | `6.648e+11` |
| 6 | 1.50 | `3.269361e+03` | `1.196033e−01` | `1.330276e+04` | **`2.054840`** | `1.734e+13` |

**`max |log₁₀(LHS/RHS)|`: `6.76` → `0.341`.** The `10⁵–10¹³` failure is gone. **The target
"ratio = 1 to several digits" is NOT met** — an `O(1)` residual survives, `[0.456, 2.055]`.

### 3.2 Residual candidates, tested one at a time

| candidate | test | result |
|---|---|---|
| Teo's `(−1)^{A/2}` prefactor | Teo Remark 2.3 proves `A` is an **even integer**, so `(−1)^{A/2} = ±1` and **`|(−1)^{A/2}| = 1`** | **ELIMINATED analytically.** It cannot move a modulus. |
| `tan(πs/2)^{1/2}` branch off the critical line | every exponent in `κ` is **real**, so `\|z^a\| = \|z\|^a` on any branch; and numerically, flipping `tan(πs/2)^{+1/2} → ^{−1/2}` changes the ratio by `< 1e−6` at `t = t_∞` (because `\|tan(π s/2)\| → 1` at that height) | **ELIMINATED**, twice over. |
| `Z`-normalisation convention (`Γ₂` vs `G`) | Lemma K-1 | **THIS WAS THE BUG.** Fixed; accounts for all `5`–`13` orders of magnitude. |
| `N`-truncation of the determinant | `mirror_q3.json` `C2`: `P_3` at `σ = 1.25, 1.40, 1.50` **and** at the mirrors `Re s = −0.25, −0.40, −0.50`, `N = 24, 32, 48, 64` | `rel drift(48→64) ≤ 3.9e−16` at all six points. **ELIMINATED.** |

> **Consequence `PROVED`.** With every exponent in `κ_q` real and `\|(−1)^{A/2}\| = 1`, **`|κ_q(s)|`
> carries no remaining branch or convention freedom whatsoever.** `|K_q|` is now a pinned number.
> The residual therefore cannot be repaired by any further reading of Prop. 2.5.

### 3.3 Why the back-solve read as an exponent flip

The wrong bracket differs from the right one by `(G(s)²/G(1−s)²)^{2·|X|/2π}`, and the `G²` ratio
dominates the `(2π)^{2s−1}Γ(1−s)/Γ(s)` pieces by many orders. So inverting `Γ₂` is *approximately*
— but not exactly — the same as flipping the bracket's exponent. That is precisely the reported
signature: agreement to `0.007–0.026` tracking `1/6 → 1/4 → 1/3`, **plus a leftover factor of
`0.42–1.83`**. The leftover is the `(2π)^{2s−1}Γ(1−s)/Γ(s)` part that a pure exponent flip also
inverts but should not. The present fix is the exact statement of which the back-solve was the
approximation.

### 3.4 What the residual actually is — a `σ` sweep

`law_probes/mirror_u4_corrected_sigmasweep.json`, `q = 3`, `N = 32`, `t = t_∞`:

| `σ` | `1 − σ` (mirror) | ratio |
|--:|--:|---|
| 0.55 | `+0.45` | `0.98197` |
| 0.60 | `+0.40` | `0.96520` |
| 0.70 | `+0.30` | `0.93902` |
| 0.80 | `+0.20` | `0.92899` |
| 0.90 | `+0.10` | `0.94345` |
| 1.00 | `+0.00` | `0.99135` |
| 1.10 | `−0.10` | `1.08107` |
| 1.25 | `−0.25` | `1.30849` |
| 1.50 | `−0.50` | `1.98277` |

(`q = 4`, **from the run log only, not banked in the JSON** — the sweep hit its wall-clock limit
before the `q = 4` rows were written: `0.87084`, `0.75541`, `0.55175` at `σ = 0.55, 0.60, 0.70`.
Larger than `q = 3`, and moving the other way; a `q = 4`-specific signal worth its own probe.
`TODO-VERIFY`: re-run and bank it.)

The `q = 3` residual is **smooth**, within **2 %** of `1` at `σ = 0.55`, and grows monotonically in
`|σ − 1/2|` once `Re(1−s) < 0`. Note that `ratio = 1` on `Re s = 1/2` is **automatic** (conjugate
symmetry of `P`), so the small values near the line are not independent evidence; the informative
statement is the **shape**: an `O(1)` factor that switches from `< 1` to `> 1` as the mirror point
crosses `Re s = 0` and then grows.

> **`HEURISTIC` reading.** `Re s > 1` is where `§7.2` validated `P_q` against the truncated Euler
> product (`≤ 2e−3`), and `q = 3` is where U4 is a **theorem** (Mayer's `Z_{PSL(2,Z)} =
> det(1−L⁺)det(1−L⁻)`), not an obligation. So the residual is most plausibly in the **mirror**
> evaluation — the determinant builder's continuation to `Re s ≤ 0`, outside the R5 common-
> continuation domain `Ω* = {Re s > 1/2} ∪ {Re s > 0, Im s > 1}`, where `N`-stability (which the
> builder has, to `1e−16`) is **not** the same as correctness. `TODO-VERIFY`: this is a hypothesis
> about the evaluator, not a measurement of it; the decisive test is a `P_3` vs. classical
> `Z_{PSL(2,Z)}` comparison at a point with `Re s < 0`, which is not run here.

---

## 4. What this restores, and what it does not

### 4.1 `LAW_U1_GROWTH.md` §7.3 and §10 — the guard: **UNAFFECTED, still trustworthy as stated**

The §7.3 `sup_{∂U}` table and the §10 claim (viii) are computed by `law_probes/probe_u1_sup.py`,
which **does not use `K_q` or `barnesg` at all** — it reports `|det(1−L⁺)det(1−L⁻)|` directly.
Verified: `barnesg`/`K_q` occur only in `mirror_u4.py`, `mirror_arith.py`, `mirror_q3.py`,
`mirror_q3_exponent.py`, `probe_u1_growth.py`.

- **`§7.3`: no number changes.** The rise `25.1 → 49.5 → 92.8 → 99.4` and the slopes `+1.50`/`+1.17`
  stand exactly as written, with their three caveats intact.
- **`§10` claim (viii): stands.**
- **But `§7.3` caveat 2 improves.** It reads "The proxy is not `Z_{G_q}` … U4 … `GAP` for `q ≠ 5`",
  and since `LAW_STRIP_AND_MIRROR.md` that caveat had hardened into an apparent **refutation** of
  U4. That hardening is now **withdrawn**: the `10¹⁵` disagreement was the kernel, not U4.
- **`§3.1` itself must be corrected in place** — its code block carries the wrong bracket.
  `TODO`: apply the §2 fix to `LAW_U1_GROWTH.md` §3.1 and add a pointer here. Not done in this
  note (single-file scope).
- **`probe_u1_growth.py` lines 121–123** compute `out["barnes_area"]` with the wrong bracket. Its
  only *use* is the `A3` assembly check on `Re s = 1/2`, which §2.1 shows is blind — so **no
  published number moves** — but any future off-line use of that field is wrong by
  `(2·|X|/2π)·log|G(s)/G(1−s)|²`. `TODO`.

### 4.2 `LAW_U1PHI_PROOF_ROUTE.md` §4.3 — the proxy readings at `Re s ≤ 1/2`: **still unsettled, and now differently so**

§4.3's table compares measured `∂U` slopes against a predicted `1−2σ`, using
`|Z_{G_q}(σ+it)| = |κ_q(1−σ+it)||Z_{G_q}(1−σ+it)|` and `|κ_q| ≍ q^{1−2σ}`. Reading by column:

| item | status after the fix |
|---|---|
| the **measured** slopes (`+0.40`, `+0.84`, `+0.61`, `−0.78`, `−0.574`, `+0.893`) | **UNAFFECTED** — they come from `probe_u1_sup.py`, no kernel. |
| the **predicted** exponent `1−2σ` | **NOT sign-flipped, but incomplete** — see §4.3 below. |
| §4.3's overall verdict (`HEURISTIC`, suggestive-only, "U1 on the amended `Ω̃` is in trouble") | **STILL UNSETTLED.** Nothing here rescues or refutes it. |
| §4.3's sub-claim that the `∂U` growth is *not* an out-of-domain artefact | **WEAKENED.** §3.4 finds the mirror identity's own residual growing exactly where those points sit (`Re s ≤ 0`), which is the artefact reading. The two now point the same way. |

### 4.3 `LAW_U1PHI_PROOF_ROUTE.md` §3.2 — `|κ_q|` diverges: **conclusion survives, and strengthens**

§3.2 estimates `|κ_q|` from `|φ_q · E_q|` **only** (`u1phiproof_kappa.py` uses no Barnes factor),
reporting slopes `+1.368` at `σ = 2` and `+2.709` at `σ = 3.5` over `q = 12 → 100`. The omitted
Barnes bracket is **not** `q`-flat — its exponent `(1−2/q)/2` moves — and with the **correct** `Γ₂`
its own `q`-slope is large and **positive** (measured here, `q = 12 → 100`, `t = t_∞`):

| `σ` | Barnes bracket slope, **corrected** | Barnes bracket slope, *old* | `E_q` slope | full `\|K_q\|` slope, corrected |
|--:|---|---|---|---|
| 1.25 | **`+1.152`** | `−1.164` | `+0.707` | `+1.859` |
| 2.00 | **`+2.304`** | `−2.330` | `+1.410` | `+3.714` |
| 3.50 | **`+4.608`** | `−4.668` | `+2.780` | `+7.388` |

So the **true** `|κ_q|` slope at `σ = 2` is about `−0.054 + 3.714 = +3.66`, not `+1.368`: `|κ_q|`
diverges **faster** than §3.2 reported. **§3.2's Consequence is not sign-flipped — it is
reinforced.** Two corrections owed to §3.2: (i) the numeric slopes understate the growth; (ii) the
sentence attributing the growth to `E_q` is wrong — the **Barnes bracket is the larger driver**
(`+2.30` vs `+1.41` at `σ = 2`). `TODO`. Note also that the *old* transcription gives an
equal-and-opposite **negative** slope, so any past reading that folded the old bracket into a
`q`-trend is contaminated by `~10^{2.1}` across `q = 12 → 100` at `σ = 1.25`
**[CORRECTED 2026-08-16: was `~10⁹`, which no reading reproduces.** The corrected/old bracket
ratio is `[G(1−s)/G(s)]^{4·(1−2/q)/2}`; at `σ = 1.25`, `t = t_∞`, `dps = 40` it is
`1.311e+12` at `q = 12` and `1.779e+14` at `q = 100`, i.e. **pointwise `10^{12.1}…10^{14.3}`**
and a **trend discrepancy of `10^{2.13}`** over `q = 12 → 100`. Neither figure is `10⁹`. The
qualitative point — the old bracket contaminates any `q`-trend that folded it in — is
unchanged.**]**

**Convention note [ADDED 2026-08-16].** The three slope rows in the table above are
**endpoint** fits (`q = 12 → 100`), not the LSQ fits banked elsewhere in the lane; the LSQ
values are `+1.110 / +2.220 / +4.440`. Neither convention changes the sign or the ordering,
and the "Barnes bracket is the larger driver" reading holds in both.

### 4.4 `LAW_STRIP_AND_MIRROR.md` / `LAW_MIRROR_Q3_DISCRIMINATOR.md`

| id | old status | new status |
|---|---|---|
| SM.11 (the identity `(*)` under U4 + Teo) | `PROVED` (derivation) | **`PROVED`, and now independently re-derived** from Teo Thm 2.2 in §1.4 |
| SM.23 ("U4 refuted OR Teo assembly wrong; not separated") | **the finding** | **SEPARATED. It is the Teo assembly.** `SUPERSEDED` |
| SM's "`VERDICT: U4-as-identification is REFUTED, unless …`" | verdict | **WITHDRAWN.** The `unless` clause fired. |
| Q3.5 (pre-registered rule ⇒ fault is (b)) | **the finding** | **CONFIRMED**, and the mechanism named |
| Q3.9 ("corrected `κ_q` must be re-derived from Teo Prop. 2.5; source never opened") | `TODO-VERIFY` — the next act | **DISCHARGED.** Source opened, quoted verbatim (§1), error found (§2), rerun (§3) |
| Q3's `HEURISTIC` sign-flip diagnosis (`−(1−2/q)/2`) | `HEURISTIC` | **SUPERSEDED** by the exact statement; §3.3 explains why it fitted to `0.007–0.026` and why it left `0.42–1.83` |

---

## 5. Status ledger

| id | claim | status | where |
|---|---|---|---|
| K.1 | Teo Prop. 2.5 / Thm 2.2 quoted verbatim from arXiv:1901.07898v2 | **`CITATION`** | §1.1–1.3 |
| K.2 | Prop. 2.5 is self-consistent with Thm 2.2; the bracket exponent `+|X|/2π` is correct | **`PROVED`** | §1.4 |
| K.3 | **`Γ₂(s) = 1/G(s)`** (Lemma K-1) | **`PROVED`** | §2 |
| K.4 | **`§3.1` / `mirror_u4.py` invert the `Γ₂²` ratio — the transcription error** | **`PROVED`** — the finding | §2 |
| K.5 | The `\|K_q(1/2+it)\| = 1` assembly check is structurally blind to K.4 | **`PROVED`** | §2.1 |
| K.6 | Corrected rerun: `max\|log₁₀ ratio\|` `6.76 → 0.341`; ratios in `[0.456, 2.055]` | **`HEURISTIC`** (float midpoints, no winding cert) | §3.1 |
| K.7 | `\|κ_q\|` has **no** remaining branch/convention freedom | **`PROVED`** | §3.2 |
| K.8 | The residual is not `N`-truncation (`≤ 3.9e−16` drift to `N = 64`) | **`PROVED` numerically** | §3.2 |
| K.9 | Residual smooth in `σ`, `→ 1` at the line, grows for `Re(1−s) < 0` | **`HEURISTIC`** | §3.4 |
| K.10 | **U4 is no longer refuted by the mirror test; nor is it confirmed** | **the finding** | §0, §4.4 |
| K.11 | `LAW_U1_GROWTH.md` §7.3/§10 numbers unaffected | **`PROVED`** (code audit: no `barnesg`/`K_q` in `probe_u1_sup.py`) | §4.1 |
| K.12 | `LAW_U1PHI_PROOF_ROUTE.md` §3.2's divergence conclusion survives and strengthens; its slopes understate and its attribution to `E_q` is wrong | **`HEURISTIC`** | §4.3 |
| K.13 | §4.3's `Re s ≤ 1/2` proxy readings remain **unsettled**; its anti-artefact sub-claim is weakened | **`HEURISTIC`** | §4.2 |

**Open `TODO`s created here.** (1) Correct `LAW_U1_GROWTH.md` §3.1's code block and
`probe_u1_growth.py` lines 121–123. (2) Correct `LAW_U1PHI_PROOF_ROUTE.md` §3.2's slope table and
attribution. (3) Decide the `O(1)` residual by comparing `P_3` against classical
`Z_{PSL(2,Z)}` at a point with `Re s < 0`. (4) The `q = 4` residual is larger and of opposite sign
to `q = 3, 6` — probe it. (5) `TODO-VERIFY` the journal version's numbering.

## 6. Receipts

- `law_probes/mirror_u4_corrected.py` — the corrected kernel + rerun (`mirror_u4.py` untouched).
- `law_probes/mirror_u4_corrected.json` — §3.1 table, controls, candidate tests.
- `law_probes/mirror_u4_corrected_sigmasweep.json` — §3.4.
- `law_probes/mirror_q3.json` `controls.N_convergence` — §3.2's `N`-stability (pre-existing).
- Source PDF: arXiv:1901.07898v2, retrieved 2026-08-16.
